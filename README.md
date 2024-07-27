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

### Object `payarc.applications`
##### Object `payarc.applications` is used by Agents and ISVs to manage candidate merchant when acquiring new customer. As such you can create, list, get details, and manage documents required in boarding process.  
    create - this function add new candidate into database. See documentation for available attributes, possible values for some of them and which are mandatory. 
    list - returns a list of application object representing future merchants. Use this function to find the interested identifier. 
    retrieve - based on identifier or an object returned from list function, this function will return details 
    delete - in case candidate merchant is no longer needed it will remove information for it.
    addDocument - this function is adding base64 encoded document to existing candidate merchant. For different types of document required in the process contact Payarc. See examples how the function could be invoked
    deleteDocument - this function removes document, when document is no longer valid.
    submit - this function initialize the process of sing off contract between Payarc and your client
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


## Listing Charges

### Example: List Charges with No Constraints

This example demonstrates how to list all charges without any constraints:

```python
async def list_charges(options=None):
    try:
        charges = await payarc.charges['list'](options)
        print(charges)
    except Exception as error:
        print('Error detected:', error)

asyncio.run(list_charges({}))
```

## Retrieving a Charge

### Example: Retrieve a Charge

This example shows how to retrieve a specific charge by its ID:

```python
async def get_charge_by_id(id):
    try:
        charge = await payarc.charges['retrieve'](id)
        print('Success, the charge is:', charge)
    except Exception as error:
        print('Error detected:', error)

asyncio.run(get_charge_by_id('ch_nbDB*******RnMORX'))
```

### Example: Retrieve a ACH Charge

his example shows how to retrieve a specific ACH charge by its ID:

```python
async def get_charge_by_id(id):
    try:
        charge = await payarc.charges['retrieve'](id)
        print('Success, the charge is:', charge)
    except Exception as error:
        print('Error detected:', error)

asyncio.run(get_charge_by_id('ach_DB*******RnTYY'))
```

## Refunding a Charge

### Example: Refund a Charge

This example demonstrates how to refund a charge:

```python
async def refund_charge_by_obj(id, options=None):
    try:
        charge = await payarc.charges['retrieve'](id)
        refund = await charge['create_refund'](options)
        print('Success, the refund is:', refund)
    except Exception as error:
        print('Error detected:', error)

asyncio.run(refund_charge_by_obj('ch_M*********noOWL', {
                                      'reason': 'requested_by_customer',
                                      'description': 'The customer returned the product'
                                      }
                                 ))
```

Alternatively, you can refund a charge using the `create_refund` method on the Payarc instance:
```python
async def refund_charge(id, options=None):
    try:
        refund = await payarc.charges['create_refund'](id, options)
        print('Success, the refund is:', refund)
    except Exception as error:
        print('Error detected:', error)
asyncio.run(refund_charge('ch_M*******noOWL'))

```

### Example: Refund an ACH Charge

This example demonstrates how to refund an ACH charge with charge object:

```python
async def refund_ach_charge_by_obj(id, options=None):
    try:
        charge = await payarc.charges['retrieve'](id)
        refund = await charge['create_refund'](options)
        print('Success, the refund is:', refund)
    except Exception as error:
        print('Error detected:', error)
 asyncio.run(refund_ach_charge_by_obj('ach_g9dDE7GDdeDG08eA', {}))
```
This example demonstrates how to refund an ACH charge with charge identifier:

```python
async def refund_charge(id, options=None):
    try:
        refund = await payarc.charges['create_refund'](id, options)
        print('Success, the refund is:', refund)
    except Exception as error:
        print('Error detected:', error)
        
 asyncio.run(refund_charge('ach_g9dDE7GDdeDG08eA'))
```

## Managing Customers

### Example: Create a Customer with Credit Card Information
This example shows how to create a new customer with credit card information:

```python
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
        
 asyncio.run(create_customer_example())
```

### Example: Update a Customer

This example demonstrates how to update an existing customer's information when only ID is known:

```python
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

 asyncio.run(update_customer('cus_**********njA'))
```

### Example: Update an Already Found Customer

This example shows how to update a customer object:

```python
async def update_customer_by_obj(id):
    try:
        customer = await payarc.customers['retrieve'](id)
        updated_customer = await customer['update']({
            "description": 'Senior Example customer'
        })
        print('Customer updated successfully:', updated_customer)
    except Exception as error:
        print('Error detected:', error)

asyncio.run(update_customer_by_obj('cus_DP*********njA'))
```
### Example: List Customers with a Limit

This example demonstrates how to list customers with a specified limit:
```python
async def list_customer_with_limit(limit):
    try:
        data = await payarc.customers['list']({'limit': limit})
        customers = data['customers']
        pagination = data['pagination']
        print(customers[0]['card']['data'])
        print(pagination)
    except Exception as error:
        print('Error detected:', error)
        
asyncio.run(list_customer_with_limit(3))
```

### Example: Add a New Card to a Customer

This example shows how to add a new card to an existing customer:

```python
async def add_card_to_customer():
    try:
        customer = await payarc.customers['retrieve']('cus_j*********Dp')
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
        
asyncio.run(add_card_to_customer())
```
### Example: Add a New Bank Account to a Customer

This example shows how to add new bank account to a customer. See full list of bank account attributes in API documentation
```python
async def add_bank_account_to_customer():
    try:
        customer = await payarc.customers['retrieve']('cus_j*******nDp')
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
        
asyncio.run(add_bank_account_to_customer())
```

## Manage Candidate Merchants
### Create new Candidate Merchant
In the process of connecting your clients with Payarc a selection is made based on Payarc's criteria. Process begins with filling information for the merchant and creating an entry in the database. Here is an example how this process could start
```python
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
        
asyncio.run(create_candidate_merchant())
```
In this example attribute `Lead` is an object representing the business as the attribute `Owners` is and array of objects representing the owners of this business. Note this is the minimum information required. For successful boarding you should provide as much information as you can, for reference see documentation. In some case the logged user has to create application in behalf of some other agent. in this case the `object_id` of this agent must be sent in the object sent to function `payarc.applications.create`.To obtain the list of agent you can use function `listSubAgents` as it is shown on examples:
```python
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
        
asyncio.run(create_candidate_in_behalf_of_other_agent())
```
### Retrieve Information for Candidate Merchant
To continue with onboarding process you might need to provide additional information or to inquiry existing leads. In the SDK  following functions exists: `list` and `retrieve`. 

List all candidate merchant for current agent
```python
async def list_applications():
    try:
        response = await payarc.applications['list']()
        applications = response['applications']
        print(applications)
    except Exception as error:
        print('Error detected:', error)

asyncio.run(list_applications())
```
Retrieve data for current candidate merchant
```python
async def get_candiate_merchant_by_id(id):
    try:
        candidate = await payarc.applications['retrieve'](id)
        print('Candidate retrieved successfully:', candidate)
    except Exception as error:
        print('Error detected:', error)
   
asyncio.run(get_candiate_merchant_by_id('app_**********njA'))
```
## License [MIT](LICENSE)