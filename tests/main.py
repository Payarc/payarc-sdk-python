import asyncio
import json

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


async def create_charge_example():
    charge_data = {
        "amount": 1785,
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
        print(customers[0]['card']['data'])
        print(pagination)
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


async def get_candiate_merchant_by_id(id):
    try:
        candidate = await payarc.applications['retrieve'](id)
        print('Candidate retrieved successfully:', candidate)
    except Exception as error:
        print('Error detected:', error)


# Run the example
if __name__ == "__main__":
    # asyncio.run(create_charge_example())
    # asyncio.run(list_charges({'limit': 50, 'page': 2}))
    # asyncio.run(get_charge_by_id('ach_g9dDE7GDdeDG08eA'))
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
    # asyncio.run(add_card_to_customer())
    # asyncio.run(add_bank_account_to_customer())
    # asyncio.run(create_charge_by_card_id())
    # asyncio.run(create_charge_by_token())
    # asyncio.run(create_charge_by_customer_id())
    # asyncio.run(create_charge_by_bank_account())
    # asyncio.run(create_ach_charge_by_bank_account_details())
    # asyncio.run(create_candidate_merchant())
    # asyncio.run(list_applications())
    # asyncio.run(get_candiate_merchant_by_id('appl_3alndgy6xoep49y8'))
    asyncio.run(create_candidate_in_behalf_of_other_agent())
