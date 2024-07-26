# Payarc SDK for Python

The Payarc SDK allows developers to integrate Payarc's payment processing capabilities into their applications with ease. This SDK provides a comprehensive set of APIs to handle transactions, customer management, and candidate merchant management.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

You can install the Payarc SDK using pip (for Python projects).

```bash
$ pip install payarc
```

## Usage

Before you can use the Payarc SDK, you need to initialize it with your API key and the URL base point. This is required for authenticating your requests and specifying the endpoint for the APIs. For each environment (prod, sandbox) both parameters have different values. This information should stay on your server and security measures must be taken not to share it with your customers. Provided examples use package [python-dotenv](https://pypi.org/project/python-dotenv/) to store this information and provide it on the constructor. It is not mandatory to use this approach as your setup could be different.
In case you want to take benefits of candidate merchant functionality you need so-called Agent identification token. This token could be obtained from the portal.

You have to create `.env` file in root of your project and update the following rows after =
```ini
PAYARC_ENV=''
PAYARC_KEY=''
AGENT_KEY=''
```
then install [python-dotenv](https://pypi.org/project/python-dotenv/) package
```bash
```bash
$ pip install python-dotenv
```

You have to create object from SDK to call different methods depends on business needs. Optional you can load `.env` file into configuration by adding the following code:
```python
from dotenv import load_dotenv
import os
load_dotenv()
```

then you create instance of the SDK
```python
/**
 * Creates an instance of Payarc.
 * @param {string} bearer_token - The bearer token for authentication.Mandatory parameter to construct the object
 * @param {string} [base_url='sandbox'] - The url of access points possible values prod or sandbox, as sandbox is the default one. Vary for testing playground and production. can be set in environment file too.
 * @param {string} [api_version='/v1/'] - The version of access points for now 1(it has default value thus could be omitted).
 * @param {string} [version='1.0'] - API version.
 * @param {string} bearer_token_agent - The bearer token for agent authentication. Only required if you need functionality around candidate merchant
 * 
 */
from payarc import Payarc

payarc = Payarc(
    bearer_token=os.getenv('PAYARC_KEY'),
    bearer_token_agent=os.getenv('AGENT_KEY'),
    base_url=os.getenv('PAYARC_BASE_URL'),
    version=os.getenv('PAYARC_VERSION')
)
```
if no errors you are good to go.

## API Reference
- Documentation for existing payment API provided by Payarc can be found on https://docs.payarc.net/
- Documentation for existing candidate merchant management API can be found on https://docs.apply.payarc.net/

## Examples
SDK is build around object payarc. From this object you can access properties and function that will support your operations.

### Object `payarc.charges`
#### Object `payarc.charges` is used to manipulate payments in the system. This object has following functions: 
    create - this function will create a payment intent or charge accepting various configurations and parameters. See examples for some use cases. 
    retrieve - this function returns json object 'Charge' with details
    list - returns an object with attribute 'charges' a list of json object holding information for charges and object in attribute 'pagination'
    create_refund - function to perform a refund over existing charge

### Object ``payarc.customer``
#### Object `payarc.customer` is representing your customers with personal details, addresses and credit cards and/or bank accounts. Saved for future needs
    create - this function will create object stored in the database for a customer. it will provide identifier unique for each in order to identify and inquiry details. See examples and docs for more information
    retrieve - this function extract details for specific customer from database
    list - this function allows you to search amongst customers you had created. It is possible to search based on some criteria. See examples and documentation for more details  
    update - this function allows you to modify attributes of customer object.

First, initialize the Payarc SDK with your API key:

```python
payarc = Payarc(
    bearer_token=os.getenv('PAYARC_KEY'),
    bearer_token_agent=os.getenv('AGENT_KEY'),
    base_url=os.getenv('PAYARC_BASE_URL'),
    version=os.getenv('PAYARC_VERSION')
)
``` 


## Creating a Charge
### Example: Create a Charge with Minimum Information
To create a `payment(charge)` from a customer, minimum information required is:
- `amount` converted in cents,
- `currency` equal to 'usd',
- `source` the credit card which will be debited with the amount above.

For credit card minimum needed attributes are `card number` and `expiration date`. For full list of attributes see API documentation.
This example demonstrates how to create a charge with the minimum required information:

```python
import asyncio

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
        
        
if __name__ == "__main__":
    asyncio.run(create_charge_example())
```
### Example: Create a Charge by Token
To create a payment(charge) from a customer, minimum information required is:
- `amount` converted in cents,
- `currency` equal to 'usd',
- `source` an object that has attribute `token_id`. this can be obtained by the [CREATE TOKEN API](https://docs.payarc.net/#ee16415a-8d0c-4a71-a5fe-48257ca410d7) for token creation.
This example shows how to create a charge using a token:

```python
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
```

### Example: Create a Charge by Card ID

Charge can be generated over specific credit card (cc) if you know the cc's ID and customer's ID to which this card belongs.
This example demonstrates how to create a charge using a card ID:

```python
async def create_charge_by_card_id():
    charge_data = {
        "amount": 3785,
        "currency": "usd",
        "source": {
            "card_id": "card_Ly9tetrt59M0m1",
            "customer_id": "cus_jMNetettyynDp"
        }
    }
    try:
        charge = await payarc.charges['create'](charge_data)
        print('Success, the charge is:', charge)
    except Exception as error:
        print('Error detected:', error)

 asyncio.run(create_charge_by_card_id())
```
### Example: Create a Charge by Customer ID

This example shows how to create a charge using a customer ID:

```python
async def create_charge_by_customer_id():
    charge_data = {
        "amount": 5785,
        "currency": "usd",
        "source": {
            "customer_id": "cus_jMNetettyynDp"
        }
    }
    try:
        charge = await payarc.charges['create'](charge_data)
        print('Success, the charge is:', charge)
    except Exception as error:
        print('Error detected:', error)

 asyncio.run(create_charge_by_customer_id())
```

### Example: Create a Charge by Bank account ID

This example shows how to create an ACH charge when you know the bank account 

```python
async def create_charge_by_bank_account():
    try:
        customer = await payarc.customers['retrieve']('cus_jMNKVMPKnNxPVnDp')
        charge = await customer['charges']['create']({
            'amount':6699,
            'sec_code': 'WEB',
            'source': {
                'bank_account_id': 'bnk_eJjbbbbbblL'
            }
        })
        print('Charge created successfully:', charge)
    except Exception as error:
        print('Error detected:', error)
        
asyncio.run(create_charge_by_bank_account())
```

Example make ACH charge with new bank account. Details for bank account are send in attribute source

```python
async def create_ach_charge_by_bank_account_details():
    try:
        customer = await payarc.customers['retrieve']('cus_jMNKVMPKnNxPVnDp')
        charge = await customer['charges']['create']({
            'amount': 6699,
            'sec_code': 'WEB',
            'source': {
                 'account_number':'123432575352',
                 'routing_number':'123345349',
                 'first_name': 'FirstName III',
                 'last_name':'LastName III',
                 'account_type': 'Personal Savings',
            }
        })
        print('Charge created successfully:', charge)
    except Exception as error:
        print('Error detected:', error)

asyncio.run(create_ach_charge_by_bank_account_details())
```