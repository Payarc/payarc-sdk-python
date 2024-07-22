import json

import httpx
from functools import partial


class Payarc:
    def __init__(self, bearer_token, base_url='sandbox', api_version='/v1/', version='1.0', bearer_token_agent=None):
        if not bearer_token:
            raise ValueError('Bearer token is required')

        self.bearer_token = bearer_token
        self.version = version
        self.base_url = 'https://api.payarc.net' if base_url == 'prod' else 'https://test.payarc.net' if base_url == 'sandbox' else base_url
        self.base_url = f"{self.base_url}{api_version}" if api_version == '/v1/' else f"{self.base_url}/v{api_version}/"
        self.bearer_token_agent = bearer_token_agent

        self.charges = {
            'create': self.__create_charge,
            'retrieve': self.__get_charge,
            'list': self.__list_charge,
            'create_refund': self.__refund_charge
        }
        self.customers = {
            'create': self.create_customer,
            'retrieve': self.retrieve_customer,
            'list': self.list_customer,
            'update': self.update_customer,
        }
        self.applicants = {
            'create': self.add_lead,
            'list': self.apply_apps,
            'retrieve': self.retrieve_applicant,
            'delete': self.delete_applicant,
            'add_document': self.add_applicant_document,
            'submit': self.submit_applicant_for_signature,
            'delete_document': self.delete_applicant_document
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
            elif 'source' in charge_data and (charge_data['source'].startswith('bnk_') or 'sec_code' in charge_data):
                if charge_data['source'].startswith('bnk_'):
                    charge_data['bank_account_id'] = charge_data['source'][4:]
                    del charge_data['source']
                if 'bank_account_id' in charge_data and charge_data['bank_account_id'].startswith('bnk_'):
                    charge_data['bank_account_id'] = charge_data['bank_account_id'][4:]
                charge_data['type'] = 'debit'
                async with httpx.AsyncClient() as client:
                    resp = await client.post(f"{self.base_url}achcharges", json=charge_data,
                                             headers={'Authorization': f"Bearer {self.bearer_token}"})
                    return self.add_object_id(resp.json()['data'])
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
        if isinstance(charge, dict):
            charge_id = charge.get('object_id', charge)
        else:
            charge_id = charge

        if charge_id.startswith('ch_'):
            charge_id = charge_id[3:]

        if charge_id.startswith('ach_'):
            result = await self.__refund_ach_charge(charge, params)
            return result
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
            return self.add_object_id(response.json().get('data'))

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
            return self.manage_error({'source': 'API Refund ACH Charge'},
                                     error.response if error.response else {})
        except Exception as error:
            return self.manage_error({'source': 'API Refund ACH Charge'}, str(error))
        else:
            return self.add_object_id(response.json().get('data'))

    async def create_customer(self, customer_data=None):
        customer_data = customer_data or {}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}customers", json=customer_data,
                                             headers={'Authorization': f"Bearer {self.bearer_token}"})
            customer = self.add_object_id(response.json()['data'])
            if 'cards' in customer_data and customer_data['cards']:
                card_tokens = await asyncio.gather(
                    *[self.gen_token_for_card(card_data) for card_data in customer_data['cards']])
                attached_cards = await asyncio.gather(
                    *[self.update_customer(customer['customer_id'], {'token_id': token['id']}) for token in
                      card_tokens])
                return await self.retrieve_customer(customer['object_id'])
            return customer
        except httpx.HTTPStatusError as error:
            return self.manage_error({'source': 'API Create customers'}, error.response)
        except Exception as error:
            return self.manage_error({'source': 'API Create customers'}, str(error))

    async def retrieve_customer(self, customer_id):
        if customer_id.startswith('cus_'):
            customer_id = customer_id[4:]
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}customers/{customer_id}",
                                            headers={'Authorization': f"Bearer {self.bearer_token}"})
            return self.add_object_id(response.json()['data'])
        except httpx.HTTPStatusError as error:
            return self.manage_error({'source': 'API retrieve customer info'}, error.response)
        except Exception as error:
            return self.manage_error({'source': 'API retrieve customer info'}, str(error))

    async def gen_token_for_card(self, token_data=None):
        token_data = token_data or {}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}tokens", json=token_data,
                                             headers={'Authorization': f"Bearer {self.bearer_token}"})
            return response.json()['data']
        except httpx.HTTPStatusError as error:
            return self.manage_error({'source': 'API for tokens'}, error.response)
        except Exception as error:
            return self.manage_error({'source': 'API for tokens'}, str(error))

    async def add_card_to_customer(self, customer_id, card_data):
        try:
            if isinstance(customer_id, dict):
                customer_id = customer_id.get('object_id', customer_id)
            if customer_id.startswith('cus_'):
                customer_id = customer_id[4:]
            card_token = await self.gen_token_for_card(card_data)
            attached_cards = await self.update_customer(customer_id, {'token_id': card_token['id']})
            return self.add_object_id(card_token['card']['data'])
        except httpx.HTTPStatusError as error:
            return self.manage_error({'source': 'API add card to customer'}, error.response)
        except Exception as error:
            return self.manage_error({'source': 'API add card to customer'}, str(error))

    async def list_customer(self, search_data=None):
        search_data = search_data or {}
        limit = search_data.get('limit', 25)
        page = search_data.get('page', 1)
        search = search_data.get('search', {})
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}customers",
                                            headers={'Authorization': f"Bearer {self.bearer_token}"},
                                            params={**{'limit': limit, 'page': page}, **search})
            customers = [self.add_object_id(customer) for customer in response.json()['data']]
            pagination = response.json()['meta'].get('pagination', {})
            pagination.pop('links', None)
            return {'customers': customers, 'pagination': pagination}
        except httpx.HTTPStatusError as error:
            return self.manage_error({'source': 'API List customers'}, error.response)
        except Exception as error:
            return self.manage_error({'source': 'API List customers'}, str(error))

    async def update_customer(self, customer_id, customer_data=None):
        customer_data = customer_data or {}
        if customer_id.startswith('cus_'):
            customer_id = customer_id[4:]
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(f"{self.base_url}customers/{customer_id}", json=customer_data,
                                            headers={'Authorization': f"Bearer {self.bearer_token}"})
            return self.add_object_id(response.json()['data'])
        except httpx.HTTPStatusError as error:
            return self.manage_error({'source': 'API update customer info'}, error.response)
        except Exception as error:
            return self.manage_error({'source': 'API update customer info'}, str(error))

    async def add_lead(self, lead_data=None):
        lead_data = lead_data or {}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}leads", json=lead_data,
                                             headers={'Authorization': f"Bearer {self.bearer_token}"})
            return self.add_object_id(response.json()['data'])
        except httpx.HTTPStatusError as error:
            return self.manage_error({'source': 'API add leads'}, error.response)
        except Exception as error:
            return self.manage_error({'source': 'API add leads'}, str(error))

    async def apply_apps(self, search_data=None):
        search_data = search_data or {}
        limit = search_data.get('limit', 25)
        page = search_data.get('page', 1)
        search = search_data.get('search', {})
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}applications",
                                            headers={'Authorization': f"Bearer {self.bearer_token}"},
                                            params={**{'limit': limit, 'page': page}, **search})
            applications = [self.add_object_id(application) for application in response.json()['data']]
            pagination = response.json()['meta'].get('pagination', {})
            pagination.pop('links', None)
            return {'applications': applications, 'pagination': pagination}
        except httpx.HTTPStatusError as error:
            return self.manage_error({'source': 'API List applications'}, error.response)
        except Exception as error:
            return self.manage_error({'source': 'API List applications'}, str(error))

    async def retrieve_applicant(self, applicant_id):
        if applicant_id.startswith('app_'):
            applicant_id = applicant_id[4:]
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}applications/{applicant_id}",
                                            headers={'Authorization': f"Bearer {self.bearer_token}"})
            return self.add_object_id(response.json()['data'])
        except httpx.HTTPStatusError as error:
            return self.manage_error({'source': 'API retrieve applicant info'}, error.response)
        except Exception as error:
            return self.manage_error({'source': 'API retrieve applicant info'}, str(error))

    async def delete_applicant(self, applicant_id):
        if applicant_id.startswith('app_'):
            applicant_id = applicant_id[4:]
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(f"{self.base_url}applications/{applicant_id}",
                                               headers={'Authorization': f"Bearer {self.bearer_token}"})
            return response.json()['data']
        except httpx.HTTPStatusError as error:
            return self.manage_error({'source': 'API delete applicant info'}, error.response)
        except Exception as error:
            return self.manage_error({'source': 'API delete applicant info'}, str(error))

    async def add_applicant_document(self, applicant_id, document_data=None):
        document_data = document_data or {}
        try:
            if applicant_id.startswith('app_'):
                applicant_id = applicant_id[4:]
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}applications/{applicant_id}/documents",
                                             json=document_data,
                                             headers={'Authorization': f"Bearer {self.bearer_token}"})
            return self.add_object_id(response.json()['data'])
        except httpx.HTTPStatusError as error:
            return self.manage_error({'source': 'API add applicant document'}, error.response)
        except Exception as error:
            return self.manage_error({'source': 'API add applicant document'}, str(error))

    async def delete_applicant_document(self, applicant_id, document_id):
        try:
            if applicant_id.startswith('app_'):
                applicant_id = applicant_id[4:]
            async with httpx.AsyncClient() as client:
                response = await client.delete(f"{self.base_url}applications/{applicant_id}/documents/{document_id}",
                                               headers={'Authorization': f"Bearer {self.bearer_token}"})
            return response.json()['data']
        except httpx.HTTPStatusError as error:
            return self.manage_error({'source': 'API delete applicant document'}, error.response)
        except Exception as error:
            return self.manage_error({'source': 'API delete applicant document'}, str(error))

    async def submit_applicant_for_signature(self, applicant_id):
        try:
            if applicant_id.startswith('app_'):
                applicant_id = applicant_id[4:]
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}applications/{applicant_id}/submit",
                                             headers={'Authorization': f"Bearer {self.bearer_token}"})
            return self.add_object_id(response.json()['data'])
        except httpx.HTTPStatusError as error:
            return self.manage_error({'source': 'API submit applicant for signature'}, error.response)
        except Exception as error:
            return self.manage_error({'source': 'API submit applicant for signature'}, str(error))

    def add_object_id(self, obj):
        def handle_object(obj):
            if 'id' in obj or 'customer_id' in obj:
                if obj['object'] == 'Charge':
                    obj['object_id'] = f"ch_{obj['id']}"
                    obj['create_refund'] = partial(self.__refund_charge, obj)
                elif obj['object'] == 'customer':
                    obj['object_id'] = f"cus_{obj['customer_id']}"
                    obj['update'] = self.update_customer
                    obj['cards'] = {}
                    obj['cards']['create'] = self.add_card_to_customer
                    if 'bank_accounts' not in obj:
                        obj['bank_accounts'] = {}
                    obj['bank_accounts']['create'] = self.add_bank_acc_to_customer
                    if 'charges' not in obj:
                        obj['charges'] = {}
                    obj['charges']['create'] = lambda: self.__create_charge(obj)
                elif obj['object'] == 'Token':
                    obj['object_id'] = f"tok_{obj['id']}"
                elif obj['object'] == 'Card':
                    obj['object_id'] = f"card_{obj['id']}"
                elif obj['object'] == 'BankAccount':
                    obj['object_id'] = f"bnk_{obj['id']}"
                elif obj['object'] == 'ACHCharge':
                    obj['object_id'] = f"ach_{obj['id']}"
                    obj['createRefund'] = lambda: self.__refund_charge(obj)
                elif obj['object'] == 'ApplyApp':
                    obj['object_id'] = f"appl_{obj['id']}"
                    obj['retrieve'] = lambda: self.retrieve_applicant(obj)
                    obj['delete'] = lambda: self.delete_applicant(obj)
                    obj['addDocument'] = lambda: self.add_applicant_document(obj)
                    obj['submit'] = lambda: self.submit_applicant_for_signature(obj)
                    obj['update'] = lambda: self.update_applicant(obj)
                    obj['listSubAgents'] = lambda: self.sub_agents(obj)
                elif obj['object'] == 'ApplyDocuments':
                    obj['object_id'] = f"doc_{obj['id']}"
                    obj['delete'] = lambda: self.delete_applicant_document(obj)
                elif obj['object'] == 'Campaign':
                    obj['object_id'] = f"cmp_{obj['id']}"
                    obj['update'] = lambda: self.update_campaign(obj)
                    obj['retrieve'] = lambda: self.get_dtl_campaign(obj)
                elif obj['object'] == 'User':
                    obj['object_id'] = f"usr_{obj['id']}"
                elif obj['object'] == 'Subscription':
                    obj['object_id'] = f"sub_{obj['id']}"
                    obj['cancel'] = lambda: self.cancel_subscription(obj)
                    obj['update'] = lambda: self.update_subscription(obj)
            elif 'MerchantCode' in obj:
                obj['object_id'] = f"appl_{obj['MerchantCode']}"
                obj['object'] = 'ApplyApp'
                del obj['MerchantCode']
                obj['retrieve'] = lambda: self.retrieve_applicant(obj)
                obj['delete'] = lambda: self.delete_applicant(obj)
                obj['addDocument'] = lambda: self.add_applicant_document(obj)
                obj['submit'] = lambda: self.submit_applicant_for_signature(obj)
                obj['update'] = lambda: self.update_applicant(obj)
                obj['listSubAgents'] = lambda: self.sub_agents(obj)
            elif 'plan_id' in obj:
                obj['object_id'] = obj['plan_id']
                obj['object'] = 'Plan'
                del obj['plan_id']
                obj['retrieve'] = lambda: self.get_plan(obj)
                obj['update'] = lambda: self.update_plan(obj)
                obj['delete'] = lambda: self.delete_plan(obj)
                obj['createSubscription'] = lambda: self.create_subscription(obj)

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
        error_json = error.json() if hasattr(error, 'json') else error
        seed.update({
            'object': f"Error {self.version}",
            'type': 'TODO put here error type',
            'errorMessage': error_json.get('message', error if isinstance(error, str) else 'unKnown'),
            'errorCode': getattr(error, 'status_code', 'unKnown'),
            'errorList': error_json.get('errors', 'unKnown'),
            'errorException': error_json.get('exception', 'unKnown'),
            'errorDataMessage': error_json.get('data', {}).get('message', 'unKnown')
        })
        return seed
