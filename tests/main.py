import asyncio
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
    asyncio.run(get_customer_by_id('cus_DPNMVjx4AMNNVnjA'))
    asyncio.run(update_customer('cus_DPNMVjx4AMNNVnjA'))
    # asyncio.run(create_charge_by_card_id())
    # asyncio.run(create_charge_by_token())
    # asyncio.run(create_charge_by_customer_id())
    # asyncio.run(create_charge_by_bank_account())
    # asyncio.run(create_ach_charge_by_bank_account_details())
