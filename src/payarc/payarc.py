import asyncio
import json

import httpx
from functools import partial


class Payarc:

    url_map = {
        'prod': 'https://api.payarc.net',
        'sandbox': 'https://testapi.payarc.net'
    }

    def __init__(self, bearer_token, base_url='sandbox', api_version='/v1/', version='1.0', bearer_token_agent=None):
        if not bearer_token:
            raise ValueError('Bearer token is required')

        self.bearer_token = bearer_token
        self.version = version
        self.base_url = self.url_map.get(base_url, base_url)
        self.base_url = f"{self.base_url}/v1/" if api_version == '/v1/' else f"{self.base_url}/v{api_version.strip('/')}/"
        self.bearer_token_agent = bearer_token_agent

        self.charges = {
            'create': self.__create_charge,
            'retrieve': self.__get_charge,
            'list': self.__list_charge,
            'create_refund': self.__refund_charge
        }
        self.customers = {
            'create': self.__create_customer,
            'retrieve': self.__retrieve_customer,
            'list': self.__list_customers,
            'update': self.__update_customer,
        }
        self.applications = {
            'create': self.__add_lead,
            'list': self.__apply_apps,
            'retrieve': self.__retrieve_applicant,
            'update': self.__update_applicant,
            'delete': self.__delete_applicant,
            'add_document': self.__add_applicant_document,
            'submit': self.__submit_applicant_for_signature,
            'delete_document': self.__delete_applicant_document,
            'list_sub_agents': self.__sub_agents
        }

    async def __create_charge(self, obj, charge_data=None):
        try:
            charge_data = charge_data or obj
            if 'source' in charge_data:
                source = charge_data.pop('source')
                if isinstance(source, dict) and source:
                    charge_data.update(source)
                else:
                    charge_data['source'] = source

            if obj and 'object_id' in obj:
                charge_data['customer_id'] = obj['object_id'][4:] if obj['object_id'].startswith('cus_') else obj[
                    'object_id']

            if 'source' in charge_data and charge_data['source'].startswith('tok_'):
                charge_data['token_id'] = charge_data['source'][4:]
            elif 'source' in charge_data and charge_data['source'].startswith('cus_'):
                charge_data['customer_id'] = charge_data['source'][4:]
            elif 'source' in charge_data and charge_data['source'].startswith('card_'):
                charge_data['card_id'] = charge_data['source'][5:]
            elif ('source' in charge_data and charge_data['source'].startswith('bnk_')) or 'sec_code' in charge_data:
                if 'source' in charge_data and charge_data['source'].startswith('bnk_'):
                    charge_data['bank_account_id'] = charge_data['source'][4:]
                    del charge_data['source']
                if 'bank_account_id' in charge_data and charge_data['bank_account_id'].startswith('bnk_'):
                    charge_data['bank_account_id'] = charge_data['bank_account_id'][4:]
                charge_data['type'] = 'debit'
                async with httpx.AsyncClient() as client:
                    response = await client.post(f"{self.base_url}achcharges", json=charge_data,
                                                 headers={'Authorization': f"Bearer {self.bearer_token}"})
                    response.raise_for_status()
            elif charge_data.get('source', '').isdigit():
                charge_data['card_number'] = charge_data['source']

            if 'token_id' in charge_data and charge_data['token_id'].startswith('tok_'):
                charge_data['token_id'] = charge_data['token_id'][4:]
            if 'customer_id' in charge_data and charge_data['customer_id'].startswith('cus_'):
                charge_data['customer_id'] = charge_data['customer_id'][4:]
            if 'card_id' in charge_data and charge_data['card_id'].startswith('card_'):
                charge_data['card_id'] = charge_data['card_id'][5:]

            if 'source' in charge_data:
                del charge_data['source']
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}charges", json=charge_data,
                                             headers={'Authorization': f"Bearer {self.bearer_token}"})
                response.raise_for_status()
        except httpx.HTTPError as error:
            raise Exception(
                self.manage_error({'source': 'API Create Charge'}, error.response if error.response else {}))
        except Exception as error:
            raise Exception(self.manage_error({'source': 'API Create Charge'}, str(error)))
        else:
            return self.add_object_id(response.json()['data'])

    async def __get_charge(self, charge_id):
        try:
            async with httpx.AsyncClient() as client:
                if charge_id.startswith('ch_'):
                    charge_id = charge_id[3:]
                    response = await client.get(
                        f"{self.base_url}charges/{charge_id}",
                        headers={'Authorization': f"Bearer {self.bearer_token}"},
                        params={'include': 'transaction_metadata,extra_metadata'}
                    )
                elif charge_id.startswith('ach_'):
                    charge_id = charge_id[4:]
                    response = await client.get(
                        f"{self.base_url}achcharges/{charge_id}",
                        headers={'Authorization': f"Bearer {self.bearer_token}"},
                        params={'include': 'review'}
                    )
                else:
                    return []

                response.raise_for_status()

        except httpx.HTTPError as error:
            raise Exception(self.manage_error({'source': 'API Retrieve Charge Info'},
                                              error.response if error.response else {}))
        except Exception as error:
            raise Exception(self.manage_error({'source': 'API Retrieve Charge Info'}, str(error)))
        else:
            return self.add_object_id(response.json()['data'])

    async def __list_charge(self, search_data=None):
        if search_data is None:
            search_data = {}

        limit = search_data.get('limit', 25)
        page = search_data.get('page', 1)
        search = search_data.get('search', {})

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}charges",
                    headers={'Authorization': f"Bearer {self.bearer_token}"},
                    params={**{'limit': limit, 'page': page}, **search}
                )

            # Apply the object_id transformation to each charge
            charges = [self.add_object_id(charge) for charge in response.json()['data']]
            pagination = response.json().get('meta', {}).get('pagination', {})
            pagination.pop('links', None)

            response.raise_for_status()
        except httpx.HTTPError as error:
            raise Exception(self.manage_error({'source': 'API List charges'},
                                              error.response if error.response else {}))
        except Exception as error:
            raise Exception(self.manage_error({'source': 'API List charges'}, str(error)))
        else:
            return {'charges': charges, 'pagination': pagination}

    async def __refund_charge(self, charge, params=None):
        ach_regular = False
        if isinstance(charge, dict):
            charge_id = charge.get('object_id', charge)
        else:
            charge_id = charge

        if charge_id.startswith('ch_'):
            charge_id = charge_id[3:]

        if charge_id.startswith('ach_'):
            ach_regular = True
            response = await self.__refund_ach_charge(charge, params)
            response.raise_for_status()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}charges/{charge_id}/refunds",
                    json=params,
                    headers={'Authorization': f"Bearer {self.bearer_token}"}
                )
            response.raise_for_status()

        except httpx.HTTPError as error:
            raise Exception(
                self.manage_error({'source': 'API Refund a charge'}, error.response if error.response else {}))
        except Exception as error:
            raise Exception(self.manage_error({'source': 'API List charges'}, str(error)))
        else:
            return self.add_object_id(response.json().get('data')) if not ach_regular else response

    async def __refund_ach_charge(self, charge, params=None):
        if params is None:
            params = {}

        if isinstance(charge, dict):
            # charge is already an object
            pass
        else:
            charge = await self.__get_charge(charge)  # charge will become an object

        params['type'] = 'credit'
        params['amount'] = params.get('amount', charge.get('amount'))
        params['sec_code'] = params.get('sec_code', charge.get('sec_code'))

        if charge.get('bank_account') and charge['bank_account'].get('data') and charge['bank_account']['data'].get(
                'object_id'):
            params['bank_account_id'] = params.get('bank_account_id', charge['bank_account']['data']['object_id'])

        if 'bank_account_id' in params and params['bank_account_id'].startswith('bnk_'):
            params['bank_account_id'] = params['bank_account_id'][4:]

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}achcharges",
                    json=params,
                    headers={'Authorization': f"Bearer {self.bearer_token}"}
                )
                response.raise_for_status()

        except httpx.HTTPError as error:
            raise Exception(self.manage_error({'source': 'API Refund ACH Charge'},
                                              error.response if error.response else {}))
        except Exception as error:
            raise Exception(self.manage_error({'source': 'API Refund ACH Charge'}, str(error)))
        else:
            return self.add_object_id(response.json().get('data'))

    async def __create_customer(self, customer_data=None):
        if customer_data is None:
            customer_data = {}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}customers",
                    json=customer_data,
                    headers={'Authorization': f"Bearer {self.bearer_token}"}
                )
                response.raise_for_status()
                customer = self.add_object_id(response.json()['data'])

                if 'cards' in customer_data and customer_data['cards']:
                    card_token_promises = [self.__gen_token_for_card(card_data) for card_data in customer_data['cards']]
                    card_tokens = await asyncio.gather(*card_token_promises)

                    if card_tokens:
                        attached_cards_promises = [
                            self.__update_customer(customer['customer_id'], {'token_id': token['id']})
                            for token in card_tokens
                        ]
                        await asyncio.gather(*attached_cards_promises)
                        return await self.__retrieve_customer(customer['object_id'])

        except httpx.HTTPError as error:
            raise Exception(self.manage_error({'source': 'API Create customers'},
                                              error.response if error.response else {}))
        except Exception as error:
            raise Exception(self.manage_error({'source': 'API Create customers'}, str(error)))
        else:
            return customer

    async def __retrieve_customer(self, customer_id):
        if customer_id.startswith('cus_'):
            customer_id = customer_id[4:]
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}customers/{customer_id}",
                    headers={'Authorization': f"Bearer {self.bearer_token}"}
                )
                response.raise_for_status()
        except httpx.HTTPError as error:
            raise Exception(
                self.manage_error({'source': 'API retrieve customer info'}, error.response if error.response else {}))
        except Exception as error:
            raise Exception(self.manage_error({'source': 'API retrieve customer info'}, str(error)))
        else:
            return self.add_object_id(response.json()['data'])

    async def __gen_token_for_card(self, token_data=None):
        if token_data is None:
            token_data = {}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}tokens",
                    json=token_data,
                    headers={'Authorization': f"Bearer {self.bearer_token}"}
                )
                response.raise_for_status()
        except httpx.HTTPError as error:
            raise Exception(self.manage_error({'source': 'API for tokens'}, error.response if error.response else {}))
        except Exception as error:
            raise Exception(self.manage_error({'source': 'API for tokens'}, str(error)))
        else:
            return response.json()['data']

    async def __add_card_to_customer(self, customer_id, card_data):
        try:
            customer_id = customer_id.get('object_id', customer_id)
            if customer_id.startswith('cus_'):
                customer_id = customer_id[4:]

            card_token = await self.__gen_token_for_card(card_data)
            attached_cards = await self.__update_customer(customer_id, {'token_id': card_token['id']})
        except httpx.HTTPError as error:
            return self.manage_error({'source': 'API add card to customer'}, error.response if error.response else {})
        except Exception as error:
            return self.manage_error({'source': 'API add card to customer'}, str(error))
        else:
            return self.add_object_id(card_token['card']['data'])

    async def __add_bank_acc_to_customer(self, customer_id, acc_data):
        try:
            customer_id = customer_id.get('object_id', customer_id)
            if customer_id.startswith('cus_'):
                customer_id = customer_id[4:]

            acc_data['customer_id'] = customer_id
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}bankaccounts",
                    json=acc_data,
                    headers={'Authorization': f"Bearer {self.bearer_token}"}
                )
                response.raise_for_status()

        except httpx.HTTPError as error:
            raise Exception(self.manage_error({'source': 'API BankAccount to customer'},
                                     error.response if error.response else {}))
        except Exception as error:
            raise Exception(self.manage_error({'source': 'API BankAccount to customer'}, str(error)))
        else:
            return self.add_object_id(response.json()['data'])

    async def __list_customers(self, search_data=None):
        if search_data is None:
            search_data = {}

        limit = search_data.get('limit', 25)
        page = search_data.get('page', 1)
        constraint = search_data.get('constraint', {})

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}customers",
                    headers={'Authorization': f"Bearer {self.bearer_token}"},
                    params={'limit': limit, 'page': page, **constraint}
                )
                response.raise_for_status()
                response_data = response.json()
                # Apply the object_id transformation to each customer
                customers = [self.add_object_id(customer) for customer in response_data['data']]
                pagination = response_data.get('meta', {}).get('pagination', {})
                pagination.pop('links', None)
                return {'customers': customers, 'pagination': pagination}

        except httpx.HTTPError as http_error:
            error_response = http_error.response if http_error.response else {}
            raise Exception(self.manage_error({'source': 'API List customers'}, error_response))
        except Exception as error:
            raise Exception(self.manage_error({'source': 'API List customers'}, str(error)))

    async def __update_customer(self, customer, cust_data):
        if 'object_id' in customer:
            customer = customer['object_id']
        if customer.startswith('cus_'):
            customer = customer[4:]
        try:
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    f"{self.base_url}customers/{customer}",
                    json=cust_data,
                    headers={'Authorization': f"Bearer {self.bearer_token}"}
                )
                response.raise_for_status()
        except httpx.HTTPError as error:
            raise Exception(
                self.manage_error({'source': 'API update customer info'}, error.response if error.response else {}))
        except Exception as error:
            raise Exception(self.manage_error({'source': 'API update customer info'}, str(error)))
        else:
            return self.add_object_id(response.json()['data'])

    async def __add_lead(self, applicant):
        if 'agentId' in applicant and applicant['agentId'].startswith('usr_'):
            applicant['agentId'] = applicant['agentId'][4:]
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}agent-hub/apply/add-lead",
                    json=applicant,
                    headers={'Authorization': f"Bearer {self.bearer_token_agent}"}
                )
                response.raise_for_status()
                return self.add_object_id(response.json())
        except httpx.HTTPError as error:
            raise Exception(self.manage_error({'source': 'API add lead'}, error.response if error.response else {}))
        except Exception as error:
            raise Exception(self.manage_error({'source': 'API add lead'}, str(error)))

    async def __apply_apps(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}agent-hub/apply-apps",
                    headers={'Authorization': f"Bearer {self.bearer_token_agent}"},
                    params={
                        'limit': 0,
                        'is_archived': 0
                    }
                )
                response.raise_for_status()
                response_data = response.json()
                applications = [self.add_object_id(application) for application in response_data['data']]
                pagination = response_data.get('meta', {}).get('pagination', {})
                pagination.pop('links', None)
                return {'applications': applications, 'pagination': pagination}

        except httpx.HTTPError as http_error:
            error_response = http_error.response if http_error.response else {}
            raise Exception(self.manage_error({'source': 'API list Apply apps'}, error_response))
        except Exception as error:
            raise Exception(self.manage_error({'source': 'API list Apply apps'}, str(error)))

    async def __retrieve_applicant(self, applicant):
        try:
            if isinstance(applicant, dict):
                applicant_id = applicant.get('object_id', applicant)
            else:
                applicant_id = applicant
            if applicant_id.startswith('appl_'):
                applicant_id = applicant_id[5:]

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}agent-hub/apply-apps/{applicant_id}",
                    headers={'Authorization': f"Bearer {self.bearer_token_agent}"},
                    params={}
                )
                response.raise_for_status()
                applicant_data = response.json()

                docs_response = await client.get(
                    f"{self.base_url}agent-hub/apply-documents/{applicant_id}",
                    headers={'Authorization': f"Bearer {self.bearer_token_agent}"},
                    params={'limit': 0}
                )
                docs_response.raise_for_status()
                docs_data = docs_response.json()

                docs_data.pop('meta', None)
                applicant_data.pop('meta', None)
                applicant_data['Documents'] = docs_data
                if 'object' not in applicant_data['data']:
                    applicant_data['data']['object'] = 'ApplyApp'
                return self.add_object_id(applicant_data)

        except httpx.HTTPError as http_error:
            error_response = http_error.response if http_error.response else {}
            raise Exception(self.manage_error({'source': 'API Apply apps status'}, error_response))
        except Exception as error:
            raise Exception(self.manage_error({'source': 'API Apply apps status'}, str(error)))

    async def __delete_applicant(self, applicant):
        if isinstance(applicant, dict):
            applicant_id = applicant.get('object_id', applicant)
        else:
            applicant_id = applicant
        try:
            if applicant_id.startswith('appl_'):
                applicant_id = applicant_id[5:]

            # Perform the delete request
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    "DELETE",
                    f"{self.base_url}agent-hub/apply/delete-lead",
                    headers={'Authorization': f"Bearer {self.bearer_token_agent}"},
                    json={'MerchantCode': applicant_id}
                )
                response.raise_for_status()

            return self.add_object_id(response.json()['data'])

        except httpx.HTTPError as error:
            raise Exception(self.manage_error({'source': 'API Apply apps delete'}, error.response if error.response else {}))
        except Exception as error:
            raise Exception(self.manage_error({'source': 'API Apply apps delete'}, str(error)))

    async def __add_applicant_document(self, applicant, params):
        if isinstance(applicant, dict):
            applicant_id = applicant.get('object_id', applicant)
        else:
            applicant_id = applicant
        if applicant_id.startswith('appl_'):
            applicant_id = applicant_id[5:]

        data = {
            'MerchantCode': applicant_id,
            'MerchantDocuments': [params]
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}agent-hub/apply/add-documents", json=data,
                                             headers={'Authorization': f"Bearer {self.bearer_token_agent}"})
                response.raise_for_status()
                return self.add_object_id(response.json())
        except httpx.HTTPError as error:
            raise Exception(self.manage_error({'source': 'API Apply documents add'}, error.response if error.response else {}))
        except Exception as error:
            raise Exception(self.manage_error({'source': 'API Apply documents add'}, str(error)))

    async def __delete_applicant_document(self, document):
        if isinstance(document, dict):
            document_id = document.get('object_id', document)
        else:
            document_id = document
        try:
            if document_id.startswith('doc_'):
                document_id = document_id[4:]

            async with httpx.AsyncClient() as client:
                response = await client.request(
                    "DELETE",
                    f"{self.base_url}agent-hub/apply/delete-documents",
                    headers={'Authorization': f"Bearer {self.bearer_token_agent}"},
                    json={'MerchantDocuments': [{'DocumentCode': document_id}]}
                )
                response.raise_for_status()

            return self.add_object_id(response.json())

        except httpx.HTTPError as error:
            raise Exception(self.manage_error({'source': 'API Apply document delete'}, error.response if error.response else {}))
        except Exception as error:
            raise Exception(self.manage_error({'source': 'API Apply document delete'}, str(error)))

    async def __submit_applicant_for_signature(self, applicant):
        if isinstance(applicant, dict):
            applicant_id = applicant.get('object_id', applicant)
        else:
            applicant_id = applicant
        try:
            if applicant_id.startswith('appl_'):
                applicant_id = applicant_id[5:]

            # Perform the POST request
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}agent-hub/apply/submit-for-signature",
                    json={'MerchantCode': applicant_id},
                    headers={'Authorization': f"Bearer {self.bearer_token_agent}"}
                )
                response.raise_for_status()

            return self.add_object_id(response.json())

        except httpx.HTTPError as error:
            return self.manage_error({'source': 'API Submit for signature'}, error.response if error.response else {})
        except Exception as error:
            return self.manage_error({'source': 'API Submit for signature'}, str(error))

    async def __sub_agents(self):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}agent-hub/sub-agents",
                    headers={"Authorization": f"Bearer {self.bearer_token_agent}"}
                )
                response.raise_for_status()  # Ensure we raise an exception for HTTP errors
                data = response.json()
                sub_agents = [self.add_object_id(sub_agent) for sub_agent in data.get('data', [])]
                return sub_agents
            except httpx.HTTPError as http_error:
                # Handle HTTP errors
                raise Exception(self.manage_error({'source': 'API List sub agents'}, http_error.response if http_error.response else {}))
            except Exception as error:
                # Handle other potential errors
                raise Exception(self.manage_error({'source': 'API List sub agents'}, str(error)))

    async def __update_applicant(self, obj, new_data):
        if isinstance(obj, dict):
            data_id = obj.get('object_id', obj)
        else:
            data_id = obj

        if data_id.startswith('appl_'):
            data_id = data_id[5:]

        default_data = {
            "bank_account_type": "01",
            "slugId": "financial_information",
            "skipGIACT": True
        }
        new_data = {**default_data, **new_data}  # Merge default_data with new_data

        try:
            async with httpx.AsyncClient() as client:
                response = await client.patch(f"{self.base_url}agent-hub/apply-apps/{data_id}",
                                              json=new_data,
                                              headers={'Authorization': f"Bearer {self.bearer_token_agent}"})
                response.raise_for_status()
                if response.status_code == 200:
                    return await self.__retrieve_applicant(data_id)
                return self.add_object_id(response.json())
        except httpx.HTTPError as error:
            raise Exception(self.manage_error({'source': 'API update Application info'}, error.response if error.response else {}))
        except Exception as error:
            raise Exception(self.manage_error({'source': 'API update Application info'}, str(error)))

    def add_object_id(self, obj):
        def handle_object(obj):
            if 'id' in obj or 'customer_id' in obj:
                if obj.get('object') == 'Charge':
                    obj['object_id'] = f"ch_{obj['id']}"
                    obj['create_refund'] = partial(self.__refund_charge, obj)
                elif obj.get('object') == 'customer':
                    obj['object_id'] = f"cus_{obj['customer_id']}"
                    obj['update'] = partial(self.__update_customer, obj)
                    obj['cards'] = {}
                    obj['cards']['create'] = partial(self.__add_card_to_customer, obj)
                    if 'bank_accounts' not in obj:
                        obj['bank_accounts'] = {}
                    obj['bank_accounts']['create'] = partial(self.__add_bank_acc_to_customer, obj)
                    if 'charges' not in obj:
                        obj['charges'] = {}
                    obj['charges']['create'] = partial(self.__create_charge, obj)
                elif obj.get('object') == 'Token':
                    obj['object_id'] = f"tok_{obj['id']}"
                elif obj.get('object') == 'Card':
                    obj['object_id'] = f"card_{obj['id']}"
                elif obj.get('object') == 'BankAccount':
                    obj['object_id'] = f"bnk_{obj['id']}"
                elif obj.get('object') == 'ACHCharge':
                    obj['object_id'] = f"ach_{obj['id']}"
                    obj['create_refund'] = partial(self.__refund_charge, obj)
                elif obj.get('object') == 'ApplyApp':
                    obj['object_id'] = f"appl_{obj['id']}"
                    obj['retrieve'] = partial(self.__retrieve_applicant, obj)
                    obj['delete'] = partial(self.__delete_applicant, obj)
                    obj['add_document'] = partial(self.__add_applicant_document, obj)
                    obj['submit'] = partial(self.__submit_applicant_for_signature, obj)
                    obj['update'] = partial(self.__update_applicant, obj)
                    obj['list_sub_agents'] = partial(self.__sub_agents, obj)
                elif obj.get('object') == 'ApplyDocuments':
                    obj['object_id'] = f"doc_{obj['id']}"
                    obj['delete'] = partial(self.__delete_applicant_document, obj)
                elif obj.get('object') == 'Campaign':
                    obj['object_id'] = f"cmp_{obj['id']}"
                    obj['update'] = lambda: self.update_campaign(obj)
                    obj['retrieve'] = lambda: self.get_dtl_campaign(obj)
                elif obj.get('object') == 'User':
                    obj['object_id'] = f"usr_{obj['id']}"
                elif obj.get('object') == 'Subscription':
                    obj['object_id'] = f"sub_{obj['id']}"
                    obj['cancel'] = lambda: self.cancel_subscription(obj)
                    obj['update'] = lambda: self.update_subscription(obj)
            elif 'MerchantCode' in obj:
                obj['object_id'] = f"appl_{obj['MerchantCode']}"
                obj['object'] = 'ApplyApp'
                del obj['MerchantCode']
                obj['retrieve'] =partial(self.__retrieve_applicant, obj)
                obj['delete'] = partial(self.__delete_applicant, obj)
                obj['add_document'] = partial(self.__add_applicant_document, obj)
                obj['submit'] = partial(self.__submit_applicant_for_signature, obj)
                obj['update'] = partial(self.__update_applicant, obj)
                obj['list_sub_agents'] = partial(self.__sub_agents, obj)
            elif 'plan_id' in obj:
                obj['object_id'] = obj['plan_id']
                obj['object'] = 'Plan'
                del obj['plan_id']
                obj['retrieve'] = partial(self.retrieve_plan, obj)
                obj['update'] = partial(self.update_plan, obj)
                obj['delete'] = partial(self.delete_plan, obj)
                obj['createSubscription'] = partial(self.create_subscription, obj)

            for key in obj:
                if isinstance(obj[key], dict):
                    handle_object(obj[key])
                elif isinstance(obj[key], list):
                    for item in obj[key]:
                        if isinstance(item, dict):
                            handle_object(item)

        handle_object(obj)
        return obj

    def manage_error(self, seed=None, error=None):
        seed = seed or {}

        # Determine the error_json
        if hasattr(error, 'json'):
            try:
                error_json = error.json()
            except ValueError:
                error_json = {}
        elif isinstance(error, dict):
            error_json = error
        else:
            error_json = {}

        # Update seed with error details
        seed.update({
            'object': f"Error {self.version}",
            'type': 'TODO put here error type',
            'errorMessage': error_json.get('message', error) if isinstance(error, str) else error_json.get('message',
                                                                                                           'unKnown'),
            'errorCode': getattr(error, 'status_code', 'unKnown'),
            'errorList': error_json.get('errors', 'unKnown'),
            'errorException': error_json.get('exception', 'unKnown'),
            'errorDataMessage': error_json.get('data', {}).get('message', 'unKnown')
        })

        return seed
