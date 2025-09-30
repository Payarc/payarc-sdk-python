import asyncio
import pprint

from src.payarc.payarc import Payarc
from dotenv import load_dotenv
import os

load_dotenv()

payarc = Payarc(
    bearer_token=os.getenv('PAYARC_KEY'),
    bearer_token_agent=os.getenv('AGENT_KEY'),
    base_url=os.getenv('PAYARC_BASE_URL'),
    version=os.getenv('PAYARC_VERSION')
)

print("Payarc SDK initialized with base URL:", payarc.bearer_token_agent)


async def create_charge_example():
    charge_data = {
        "amount": 1782,
        "currency": "usd",
        "source": {
            "card_number": "4012000098765439",
            "exp_month": "03",
            "exp_year": "2025",
        }
    }

    try:
        charge = await payarc.charges['create'](charge_data)
        print('Success, the charge is:', charge)
    except Exception as error:
        print('Error detected:', error)


async def create_charge_by_card_id():
    charge_data = {
        "amount": 3785,
        "currency": "usd",
        "source": {
            "card_id": "card_Ly9v09NN2P59M0m1",
            "customer_id": "cus_jMNKVMPKnNxPVnDp"
        }
    }
    try:
        charge = await payarc.charges['create'](charge_data)
        print('Success, the charge is:', charge)
    except Exception as error:
        print('Error detected:', error)


async def create_charge_by_token():
    charge_data = {
        "amount": 3785,
        "currency": "usd",
        "source": {
            "token_id": "tok_mEL8xxxxLqLL8wYl"
        }
    }
    try:
        charge = await payarc.charges['create'](charge_data)
        print('Success, the charge is:', charge)
    except Exception as error:
        print('Error detected:', error)


async def create_charge_by_customer_id():
    charge_data = {
        "amount": 3785,
        "currency": "usd",
        "source": {
            "customer_id": "cus_jMNKVMPKnNxPVnDp"
        }
    }
    try:
        charge = await payarc.charges['create'](charge_data)
        print('Success, the charge is:', charge)
    except Exception as error:
        print('Error detected:', error)


async def create_instructional_funding_charge():
    charge_data = {
        "amount": 120,
        "currency": "usd",
        "source": {
            "card_number": "4012000098765439",
            "exp_month": "03",
            "exp_year": "2025",
            "splits": [
                {
                    "mid": "0709900000109900",
                    "amount": 20,
                    "description": "Application fee"
                },
                {
                    "mid": "0609900000551514",
                    "amount": 100,
                    "description": "Platform fee"
                }
            ]
        }
    }
    try:
        charge = await payarc.charges['create'](charge_data)
        print('Success, the charge is:', charge)
    except Exception as error:
        print('Error detected:', error)


async def adjust_splits_by_charge_id(id):
    splits_data = {
        "splits": [
            {
                "mid": "0709900000109900",
                "amount": 30,
                "description": "Application fee updated"
            },
            {
                "mid": "0609900000551514",
                "amount": 90,
                "description": "Platform fee updated"
            }
        ]
    }
    try:
        charge = await payarc.charges['adjust_splits'](id, splits_data)
        print('Success, the charge with adjusted splits is:', charge)
    except Exception as error:
        print('Error detected:', error)


async def list_charge_splits(params=None):
    try:
        splits = await payarc.charges['list_splits'](params)
        pprint.pprint(splits)
    except Exception as error:
        print('Error detected:', error)


async def adjust_splits_by_charge_obj():
    try:
        charge = await payarc.charges['retrieve']('ch_WBMROoBWnnnDbOyn')
        splits_data = {
            "splits": [
                {
                    "mid": "0709900000109900",
                    "amount": 45,
                    "description": "Application fee updated"
                },
                {
                    "mid": "0609900000551514",
                    "amount": 45,
                    "description": "Platform fee updated"
                }
            ]
        }
        updated_charge = await charge['adjust_splits'](splits_data)
        print('Success, the charge with adjusted splits is:', updated_charge)
    except Exception as error:
        print('Error detected:', error)


async def get_charge_by_id(id):
    try:
        charge = await payarc.charges['retrieve'](id)
        print('Success, the charge is:', charge)
    except Exception as error:
        print('Error detected:', error)


async def list_charges(options=None):
    try:
        charges = await payarc.charges['list'](options)
        print(charges)
    except Exception as error:
        print('Error detected:', error)


async def refund_charge(id, options=None):
    try:
        refund = await payarc.charges['create_refund'](id, options)
        print('Success, the refund is:', refund)
    except Exception as error:
        print('Error detected:', error)


async def refund_charge_by_obj(id, options=None):
    try:
        charge = await payarc.charges['retrieve'](id)
        refund = await charge['create_refund'](options)
        print('Success, the refund is:', refund)
    except Exception as error:
        print('Error detected:', error)


async def refund_ach_charge_by_obj(id, options=None):
    try:
        charge = await payarc.charges['retrieve'](id)
        refund = await charge['create_refund'](options)
        print('Success, the refund is:', refund)
    except Exception as error:
        print('Error detected:', error)


async def create_webhook_example():
    webhook_data = {
        # 'key': 'merchant.onboarded.webhook',
        'key': 'lead.category.updated.webhook',
        'value': 12,
    }
    try:
        webhook = await payarc.user_settings['agent']['webhooks']['create'](webhook_data)
        print('Webhook created:', webhook)
    except Exception as error:
        print('Error detected:', error)


async def update_webhook_example():
    webhook_data = {
        'key': 'merchant.onboarded.webhook',
        'value': 1,
    }
    try:
        webhook = await payarc.user_settings['agent']['webhooks']['update'](webhook_data)
        print('Webhook updated:', webhook)
    except Exception as error:
        print('Error detected:', error)


async def update_webhook_example_by_obj():
    try:
        webhooks = await payarc.user_settings['agent']['webhooks']['list']()
        webhook = webhooks['webhooks'][1] if webhooks['webhooks'] else None
        if webhook:
            webhook['value'] = 13
            updated_webhook = await webhook['update']()
            print('Webhook updated:', updated_webhook)
    except Exception as error:
        print('Error detected:', error)


async def list_webhooks_example():
    try:
        webhooks = await payarc.user_settings['agent']['webhooks']['list']()
        print('Webhooks list:', webhooks)
    except Exception as error:
        print('Error detected:', error)


async def delete_webhook_example():
    try:
        response = await payarc.user_settings['agent']['webhooks']['delete']('merchant.onboarded.webhook')
        print('Webhook deleted:', response)
    except Exception as error:
        print('Error detected:', error)


async def create_customer_example():
    customer_data = {
        "email": "anon+50@example.com",
        "cards": [
            {
                "card_source": "INTERNET",
                "card_number": "4012000098765439",
                "exp_month": "04",
                "exp_year": "2025",
                "cvv": "997",
                "card_holder_name": "John Doe",
                "address_line1": "123 Main Street",
                "city": "Greenwich",
                "state": "CT",
                "zip": "06830",
                "country": "US",
            },
            {
                "card_source": "INTERNET",
                "card_number": "4012000098765439",
                "exp_month": "11",
                "exp_year": "2025",
                "cvv": "998",
                "card_holder_name": "John Doe",
                "address_line1": "123 Main Street Apt 3",
                "city": "Greenwich",
                "state": "CT",
                "zip": "06830",
                "country": "US",
            }
        ]
    }
    try:
        customer = await payarc.customers['create'](customer_data)
        print('Customer created:', customer)
    except Exception as error:
        print('Error detected:', error)


async def update_customer_example():
    try:
        customer = await payarc.customers['update'] \
            ('cus_3',
             {
                 "name": 'John Doe II',
                 "description": 'Example customer',
                 "phone": '1234567890'
             })
        print('Customer updated successfully:', customer)
    except Exception as error:
        print('Error detected:', error)


async def get_customer_by_id(id):
    try:
        customer = await payarc.customers['retrieve'](id)
        print('Customer retrieved successfully:', customer)
    except Exception as error:
        print('Error detected:', error)


async def update_customer(id):
    try:
        updated_customer = await payarc.customers['update'](id, {
            "name": 'John Doe II',
            "description": 'Example customer',
            "phone": '1234567890'
        })
        print('Customer updated successfully:', updated_customer)
    except Exception as error:
        print('Error detected:', error)


async def update_customer_by_obj(id):
    try:
        customer = await payarc.customers['retrieve'](id)
        updated_customer = await customer['update']({
            "description": 'Senior Example customer'
        })
        print('Customer updated successfully:', updated_customer)
    except Exception as error:
        print('Error detected:', error)


async def create_ach_charge_by_bank_account():
    try:
        customer = await payarc.customers['retrieve']('cus_jMNKVMPKnNxPVnDp')
        charge = await customer['charges']['create']({
            'amount': 6699,
            'sec_code': 'WEB',
            'source': {
                'bank_account_id': 'bnk_eJjbbbbbblL'
            }
        })
        print('Charge created successfully:', charge)
    except Exception as error:
        print('Error detected:', error)


async def create_ach_charge_by_bank_account_details():
    try:
        customer = await payarc.customers['retrieve']('cus_jMNKVMPKnNxPVnDp')
        charge = await customer['charges']['create']({
            'amount': 6699,
            'sec_code': 'WEB',
            'source': {
                'account_number': '123432575352',
                'routing_number': '123345349',
                'first_name': 'FirstName III',
                'last_name': 'LastName III',
                'account_type': 'Personal Savings',
            }
        })
        print('Charge created successfully:', charge)
    except Exception as error:
        print('Error detected:', error)


async def list_customer_with_limit(limit):
    try:
        data = await payarc.customers['list']({'limit': limit})
        customers = data['customers']
        pagination = data['pagination']
        print(customers)
        print(pagination)
    except Exception as error:
        print('Error detected:', error)


async def delete_customer_by_id(id):
    try:
        customer = await payarc.customers['delete'](id)
        print('Customer deleted successfully', customer)
    except Exception as error:
        print('Error detected:', error)


async def add_card_to_customer():
    try:
        customer = await payarc.customers['retrieve']('cus_jMNKVMPKnNxPVnDp')
        card = await customer['cards']['create']({
            'card_source': 'INTERNET',
            'card_number': '5146315000000055',
            'exp_month': '03',
            'exp_year': '2025',
            'cvv': '997',
            'card_holder_name': 'John Doe',
            'address_line1': '123 Main Street ap 5',
            'city': 'Greenwich',
            'state': 'CT',
            'zip': '06830',
            'country': 'US',
        })
        print('Card added successfully:', card)
    except Exception as error:
        print('Error detected:', error)


async def add_bank_account_to_customer():
    try:
        customer = await payarc.customers['retrieve']('cus_jMNKVMPKnNxPVnDp')
        bank_account = await customer['bank_accounts']['create']({
            'account_number': '123432575352',
            'routing_number': '123345349',
            'first_name': 'John III',
            'last_name': 'LastName III',
            'account_type': 'Personal Savings',
            'sec_code': 'WEB'
        })
        print('Bank account added successfully:', bank_account)
    except Exception as error:
        print('Error detected:', error)


async def create_candidate_merchant():
    try:
        merccandidate = {
            "Lead":
                {
                    "Industry": "business_ops_consutling",
                    "MerchantName": "My applications company",
                    "LegalName": "Best Co in w",
                    "ContactFirstName": "Joan",
                    "ContactLastName": "Dhow",
                    "ContactEmail": "contact+23@mail.com",
                    "DiscountRateProgram": "interchange"
                },
            "Owners": [
                {
                    "FirstName": "First",
                    "LastName": "Last",
                    "Title": "President",
                    "OwnershipPct": 100,
                    "Address": "Somewhere",
                    "City": "City Of Test",
                    "SSN": "4546-0034",
                    "State": "WY",
                    "ZipCode": "10102",
                    "BirthDate": "1993-06-24",
                    "Email": "nikoj@negointeresuva.com",
                    "PhoneNo": "2346456784"
                }
            ]
        }
        candidate = await payarc.applications['create'](merccandidate)
        print('Candidate created successfully:', candidate)
    except Exception as error:
        print('Error detected:', error)


async def create_candidate_in_behalf_of_other_agent():
    try:
        merccandidate = {
            "Lead":
                {
                    "Industry": "cbd",
                    "MerchantName": "My applications company",
                    "LegalName": "Best Co in w",
                    "ContactFirstName": "Joan",
                    "ContactLastName": "Dhow",
                    "ContactEmail": "contact+23@mail.com",
                    "DiscountRateProgram": "interchange"
                },
            "Owners": [
                {
                    "FirstName": "First",
                    "LastName": "Last",
                    "Title": "President",
                    "OwnershipPct": 100,
                    "Address": "Somewhere",
                    "City": "City Of Test",
                    "SSN": "4546-0034",
                    "State": "WY",
                    "ZipCode": "10102",
                    "BirthDate": "1993-06-24",
                    "Email": "nikoj@negointeresuva.com",
                    "PhoneNo": "2346456784"
                }
            ]
        }
        sub_agent = await payarc.applications['list_sub_agents']()
        merccandidate['agentId'] = sub_agent[0]['object_id'] if sub_agent else None
        candidate = await payarc.applications['create'](merccandidate)
        print('Candidate created successfully:', candidate)
    except Exception as error:
        print('Error detected:', error)


async def list_applications():
    try:
        response = await payarc.applications['list']()
        applications = response['applications']
        print(applications)
    except Exception as error:
        print('Error detected:', error)


async def list_inc_documents():
    try:
        response = await payarc.applications['list']()
        applicant = response['applications'][-1]
        details = await applicant['retrieve']()
        print(details['Documents'])
    except Exception as error:
        print('Error detected:', error)


async def get_candiate_merchant_by_id(id):
    try:
        candidate = await payarc.applications['retrieve'](id)
        print('Candidate retrieved successfully:', candidate)
    except Exception as error:
        print('Error detected:', error)


async def get_lead_status(id):
    try:
        candidate = await payarc.applications['status'](id)
        print('Candidate retrieved successfully:', candidate)
    except Exception as error:
        print('Error detected:', error)


async def update_candidate_merchant(id):
    try:
        updated_candidate = await payarc.applications['update'](id,
                                                                {
                                                                    "MerchantBankAccountNo": "987396827",
                                                                    "MerchantBankRoutingNo": "1848505",
                                                                    "BankInstitutionName": "Bank of something"
                                                                })
        print('Candidate updated successfully:', updated_candidate)
    except Exception as error:
        print('Error detected:', error)


async def add_document_to_candidate_merchant(id):
    try:
        candidate = await payarc.applications['retrieve'](id)
        document = await candidate['data']['add_document']({
            "DocumentType": "Business Bank Statement",
            "DocumentName": "sample document 1",
            "DocumentIndex": 12243,
            "DocumentDataBase64": "data:image/jpeg;base64,"
                                  "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 "
        })
        print('Document added successfully:', document)
    except Exception as error:
        print('Error detected:', error)


async def remove_document_from_candidate_merchant():
    try:
        candidates = await payarc.applications['list']()
        applicant = candidates['applications'][-1]
        details = await applicant['retrieve']()
        document = details.get('Documents', {}).get('data', [None])[0]
        print(document)
        # if document:
        #     deleted_doc = await document['delete']()
        #     print('Document deleted successfully:', deleted_doc)
    except Exception as error:
        print('Error detected:', error)


async def remove_document_by_id():
    try:
        deleted_doc = await payarc.applications['delete_document']('doc_3joyr7mlwbg659vx')
        print('Document deleted successfully:', deleted_doc)
    except Exception as error:
        print('Error detected:', error)


async def submit_application():
    try:
        application = await payarc.applications['submit']('appl_3aln*******8y8')
        print('Application submitted successfully:', application)
    except Exception as error:
        print('Error detected:', error)


async def create_plan():
    plan_data = {
        'name': 'Monthly billing regular',
        'amount': 999,
        'interval': 'month',
        'statement_descriptor': '2024 MerchantT. Rglr srvc'
    }
    try:
        plan = await payarc.billing['plan']['create'](plan_data)
        print('Plan created:', plan)
    except Exception as error:
        print('Error detected:', error)


async def update_plan():
    try:
        plans = await payarc.billing['plan']['list']()
        plan = plans['plans'][0]
        if plan:
            updated_plan = await plan['update']({'name': 'Monthly billing regular II'})
            print('Plan updated:', updated_plan)
    except Exception as error:
        print('Error detected:', error)


async def update_plan_by_id(id):
    try:
        updated_plan = await payarc.billing['plan']['update'](id,
                                                              {
                                                                  'name': 'Monthly billing regular II'
                                                              }
                                                              )
        print('Plan updated:', updated_plan)
    except Exception as error:
        print('Error detected:', error
              )


async def delete_plan(id):
    try:
        plan = await payarc.billing['plan']['delete'](id)
        print('Plan deleted:', plan)
    except Exception as error:
        print('Error detected:', error)


async def create_subscription():
    try:
        plans = await payarc.billing['plan']['list']({'search': 'iron'})
        subscriber = {
            'customer_id': 'cus_DPNMVjx4AMNNVnjA',
        }
        plans = plans['plans']
        if plans:
            plan = plans[0]
            if plan:
                subscription = await plan['create_subscription'](subscriber)
                print('Subscription created:', subscription)
    except Exception as error:
        print('Error detected:', error)


async def create_subscription_by_plan_id():
    try:
        subscriber = {
            'customer_id': 'cus_D**********njA',
        }
        subscription = await payarc.billing['plan']['create_subscription']('plan_3aln*******8y8', subscriber)
        print('Subscription created:', subscription)
    except Exception as error:
        print('Error detected:', error)


async def list_subscription():
    try:
        subscriptions = await payarc.billing['plan']['subscription']['list']({'search': 'iron'})
        print('Subscriptions:', subscriptions)
    except Exception as error:
        print('Error detected:', error)


async def update_subscription():
    try:
        subscription = await payarc.billing['plan']['subscription']['update']('sub_Vg0rxj00AVrjPAoX',
                                                                              {'description': 'Monthly for VIP'})
        print('Subscription updated:', subscription)
    except Exception as error:
        print('Error detected:', error)


async def list_campaign():
    try:
        campaigns = await payarc.split_campaigns['list']()
        print('Campaigns:', campaigns)
    except Exception as error:
        print('Error detected:', error)


async def list_all_processing_merchants():
    try:
        merchants = await payarc.split_campaigns['list_accounts']()
        print('Merchants:', merchants['campaign_accounts'])
    except Exception as error:
        print('Error detected:', error)


async def create_campaign():
    try:
        campaign = await payarc.split_campaigns['create']({
            'name': 'Mega bonus',
            'description': "Compliment for my favorite customers",
            'notes': "Only for VIPs",
            'base_charge': 33.33,
            'perc_charge': 7.77,
            'is_default': '0',
            'accounts': []
        })
        print('Campaign created:', campaign)
    except Exception as error:
        print('Error detected:', error)


async def get_campaign_by_id(id):
    try:
        campaign = await payarc.split_campaigns['retrieve'](id)
        print('Campaign retrieved:', campaign)
    except Exception as error:
        print('Error detected:', error)


async def update_campaign():
    try:
        payload = {
            'notes': "new version of notes"
        }

        campaign = await payarc.split_campaigns['update']('cmp_o3maq0gklr78p6n5', payload)
        print('Campaign updated:', campaign)
    except Exception as error:
        print('Error detected:', error)


async def list_agent_charges(options=None):
    try:
        agent_charges = await payarc.charges['agent']['list'](
            options)
        print('Agent Charges:', agent_charges)
    except Exception as error:
        print('Error detected:', error)


async def list_cases():
    try:
        cases = await payarc.disputes['list']()
        print('Cases:', cases)
    except Exception as error:
        print('Error detected:', error)


async def list_agent_deposits(options=None):
    try:
        deposits = await payarc.deposits['list'](options)
        print("Agent Deposits:")
        pprint.pprint(deposits, width=120, compact=True)
    except Exception as error:
        print('Error detected:', error)


async def list_agent_batches(options=None):
    try:
        batches = await payarc.batches['agent']['list'](options)
        print("Agent Batches:")
        pprint.pprint(batches, width=120, compact=True)
    except Exception as error:
        print('Error detected:', error)


async def get_batch_details(options=None):
    try:
        batch = await payarc.batches['agent']['details'](options)
        print("Batch Details:")
        pprint.pprint(batch, width=120, compact=True)
    except Exception as error:
        print('Error detected:', error)


async def get_batch_details_by_obj(options=None):
    try:
        batches = await payarc.batches['agent']['list'](options)
        batch = batches['batches'][1]
        details = await batch['details']()
        print("Batch Details:")
        pprint.pprint(details, width=120, compact=True)
    except Exception as error:
        print('Error detected:', error)


async def get_case(id):
    try:
        case = await payarc.disputes['retrieve'](id)
        print('Case:', case)
    except Exception as error:
        print('Error detected:', error)


async def submit_case():
    document_base64 = "iVBORw0KGgoAAAANSUhEUgAAAIUAAABsCAYAAABEkXF2AAAABHNCSVQICAgIfAhkiAAAAupJREFUeJzt3cFuEkEcx/E/001qUQ+E4NF48GB4BRM9+i59AE16ANlE4wv4Mp5MjI8gZ+ONEMJBAzaWwZsVf2VnstPZpfb7STh06ewu5JuFnSzQ8d5vDfiLa3sHcHiIAoIoIIgCgiggitwbWM/f2vniTe7NoIZ7Dz9Y0X0qy7NHYfbLtn6dfzOoYXPlUl4+IIgCooGXj10ngzM77p81vVmY2Y9vL+xi9Tn4f41HYVZYx3Wb3yws9oWBlw8IooAgCgiigCAKCKKAIAoIooAgCoikGU3nqpvy3qesPvv6+/2+LZfLpHUcsrrPD0cKCKKAIAoIooAgCgiigCAKCOecs7q3iJXbZDLZWVaWZfR4733lLbfZbBbchzZvvV4vy+PmSAFBFBBEAUEUEEQBQRQQRAFR5DzfD81FxMxVpMg9l3HT938fjhQQRAFBFBBEAUEUEEQBQRQQRe5z7SptnYejGkcKCKKAIAoIooAgCgiigCAKiKQoYj6bMB6Pd8aMRqPoz22kfCalzfmXm45nDoIoIIgCgiggiAKCKCCIAiJrFKnfTxHS9vdX5P7+ibZwpIAgCgiigCAKCKKAIAoIooDomNl2352hc+WY3+NYzyf2c345V3EyGNmdwevo8anbr3Lbfu/j+9fndrH69Ofv+48+WtF9JuM4UkAQBQRRQBAFBFFAEAUEUUBUfo9m6jUPzjl7eWr26vRyWVmW9u59GT2+Suo1B4vFImn8/4ojBQRRQBAFBFFAEAUEUUAQBUTHe7/3eorUeYrQ9RSprmP/UtZ/6OP/xfUUqI0oIIgCgiggiqY36Ddz25x/uZZ1PXmcNj60H6H1H/p4sV1F/VvjZx84HJx9IFrl733wexy3U/b3FO7ogR0dD7OsezqdVt4/HFZvNzQ+t9T9C40P6ty9erElfEKsbblnDHNrekYzFu8pIIgCgiggiAKCKCAqzz5Ccr+7T3133fb1DG0//ro4UkAQBQRRQBAFBFFAEAXEb3wL3JblytFeAAAAAElFTkSuQmCC"
    try:
        case = await payarc.disputes['add_document']('dis_MVB1AV901Rb1VAW0',
                                                     {
                                                         'DocumentDataBase64': document_base64,
                                                         'text': 'It is the true true'
                                                     })
        print('Case submitted:', case)
    except Exception as error:
        print('Error detected:', error)


# Run the example
if __name__ == "__main__":
    # asyncio.run(create_charge_example())
    # asyncio.run(create_instructional_funding_charge())
    # asyncio.run(adjust_splits_by_charge_id('ch_WBMROoBWnnnDbOyn'))
    # asyncio.run(adjust_splits_by_charge_obj())
    # asyncio.run(list_charge_splits({'limit': 25, 'page': 2}))
    asyncio.run(create_webhook_example())
    # asyncio.run(update_webhook_example())
    # asyncio.run(update_webhook_example_by_obj())
    # asyncio.run(list_webhooks_example())
    asyncio.run(delete_webhook_example())
    # asyncio.run(list_charges({'limit': 50, 'page': 1}))
    # asyncio.run(list_agent_charges({'from_date': '2025-05-27', 'to_date': '2025-05-28'}))
    # asyncio.run(get_charge_by_id('ch_WBMROoBWnnnDbOyn'))
    # asyncio.run(refund_charge('ach_g9dDE7GDdeDG08eA'))
    # asyncio.run(refund_ach_charge_by_obj('ach_g9dDE7GDdeDG08eA', {}))
    # asyncio.run(refund_charge_by_obj('ch_MnBROWLXBBXnoOWL',
    #                                  {'reason': 'requested_by_customer',
    #                                   'description': 'The customer returned the product, did not like it'}))
    # asyncio.run(create_customer_example())
    # asyncio.run(get_customer_by_id('cus_jMNKVMPKnNxPVnDp'))
    # asyncio.run(update_customer('cus_DPNMVjx4AMNNVnjA'))
    # asyncio.run(update_customer_by_obj('cus_DPNMVjx4AMNNVnjA'))
    # asyncio.run(list_customer_with_limit(3))
    # asyncio.run(delete_customer_by_id('cus_xPpAV4DNjnpKVNjK'))
    # asyncio.run(add_card_to_customer())
    # asyncio.run(add_bank_account_to_customer())
    # asyncio.run(create_charge_by_card_id())
    # asyncio.run(create_charge_by_token())
    # asyncio.run(create_charge_by_customer_id())
    # asyncio.run(create_charge_by_bank_account())
    # asyncio.run(create_ach_charge_by_bank_account_details())
    # asyncio.run(create_candidate_merchant())
    # asyncio.run(list_applications())
    # asyncio.run(get_candiate_merchant_by_id('appl_9d6woe30xye3jz0q'))
    # asyncio.run(get_lead_status('appl_jq0vmgzpq5ela96w'))
    # asyncio.run(create_candidate_in_behalf_of_other_agent())
    # asyncio.run(list_inc_documents())
    # asyncio.run(update_candidate_merchant('appl_3alndgy6xoep49y8'))
    # asyncio.run(add_document_to_candidate_merchant('appl_3alndgy6xoep49y8'))
    # asyncio.run(remove_document_from_candidate_merchant())
    # asyncio.run(remove_document_by_id())
    # asyncio.run(create_plan())
    # asyncio.run(update_plan())
    # asyncio.run(delete_plan("plan_0d640ccc"))
    # asyncio.run(create_subscription())
    # asyncio.run(list_subscription())
    # asyncio.run(update_subscription())
    # asyncio.run(list_campaign())
    # asyncio.run(list_all_processing_merchants())
    # asyncio.run(create_campaign())
    # asyncio.run(get_campaign_by_id('cmp_o3**********86n5'))
    # asyncio.run(update_campaign())
    # asyncio.run(list_cases())
    # asyncio.run(list_agent_deposits({
    #     'from_date': '2024-11-01',
    #     'to_date': '2024-11-04'
    # }))
    # asyncio.run(list_agent_batches({
    #     'from_date': '2025-05-30',
    #     'to_date': '2025-05-30'
    # }))
    # asyncio.run(get_batch_details({
    #     # 'batch_reference_number': 'bat_90042693274',
    #     'mid': '0671900000038430',
    #     'batch_date': '2025-05-30'
    # }))
    # asyncio.run(get_batch_details_by_obj({
    #     'from_date': '2025-05-30',
    #     'to_date': '2025-05-30'
    # }))
    # asyncio.run(get_case('dis_MVB1AV901Rb1VAW0'))
    # asyncio.run(submit_case())
