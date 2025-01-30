import asyncio
from src.payarc.payarc import Payarc


payarc = Payarc (
    bearer_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0Mzg4IiwianRpIjoiOTI0ODMyZjJiM2Q1MDZiZjU1M2Q0NWQzMWJkNTg0MWQ0ZWRjMjdmMjI4ODg4NWU4NWQzMDdmNjk3MWJmYjMxMTJhZjYyYzhmN2MyZTlhZTciLCJpYXQiOjE2MTExNzUxNjgsIm5iZiI6MTYxMTE3NTE2OCwiZXhwIjoxNzY4ODU1MTY4LCJzdWIiOiIxNTY1MyIsInNjb3BlcyI6IioifQ.bYo6ZQ4Jg3wjT_KibvLGpmTpWgapBfyJOXxH-1boMbVyzmj9oO_o8NpLu4aR8vGt4ZcCwmqWkuAJkYdDij0DeDuqI_7IJcBK7hRHBR4tjRbo2plmc44xnxFp5G-NbXC3lj620L2lfgBheyMRAhpkaLfwaVBQvOsq829kNmSlPhom_OhTmyBEDZi5oTFg44vKi4LfI9gORlV0wBFELrcjWoodTsMJHDk_Tiuxwkdf81XvaM6uIiJUTgnnPZM4LDINHbi9YQZ7HYORSIFn2gOyfdGSwTiY5gi13vC-ISDZxBxQWN61JMEwIheaFTubmNgUTvn7gSsp8rnSLo1Hm7p_Mh5lg6Jf2Z89509KRgO5X3iQMWMWmvAX3leSYUi0ngAXQBGdEHlyUNNy0S3dh-fJzkyFpQxkftUDX3ZKbJxCd4H4Vfe5WpgmEdjhD2wb6RI1GnPBkG6SwGy6kcHGjNKxK4hFBKZPCSwWJD7VgJP-eXQMU2J-i9tcc-zp4Acb4qjWe02FYBMKxY6FmDpFpLSvRZGXdH5Xegw6kfDIZWJF-mOB5g0ISFC_tjfxza544iEIOXlYkKzkCNXO0XbJUH6XFFv0Obd74VBrfPaHR-zxbgDmqHFRH_6bWIGAbwiwK3S8GG5RwDpk5uvEaC2F6V0M_o7ePEint8u6BCCK8WYPm7g",
    base_url='prod',
    version="/v1/"
)

async def login():
    try:
        result = await payarc.payarcConnect['login']()
        print('Result:', result)
    except Exception as error:
        print('Error detected:', error)


async def sale():
    try:
        result = await payarc.payarcConnect['sale'](tenderType="CREDIT", ecrRefNum="REF1", amount='105', deviceSerialNo='1850406725')
        print('Result:', result)
    except Exception as error:
        print('Error detected:', error)



async def void():
    try:
        result = await payarc.payarcConnect['void'](payarcTransactionId='nbDBOMBWnWXoWORX', deviceSerialNo='1850406725')
        print('Result:', result)
    except Exception as error:
        print('Error detected:', error)


async def refund():
    try:
        result = await payarc.payarcConnect['refund'](amount='50', payarcTransactionId='DMWbOLoWLWDXoOBX', deviceSerialNo='1850406725')
        print('Result:', result)
    except Exception as error:
        print('Error detected:', error)


async def blind_credit():
    try:
        result = await payarc.payarcConnect['blind_credit'](ecrRefNum="REF1", amount='50', token='IYmDAxNtma7g5228', expDate='0227', deviceSerialNo='1850406725')
        print('Result:', result)
    except Exception as error:
        print('Error detected:', error)

async def auth():
    try:
        result = await payarc.payarcConnect['auth'](ecrRefNum="REF12", amount='1000', deviceSerialNo='1850406725')
        print('Result:', result)
    except Exception as error:
        print('Error detected:', error)

async def post_auth():
    try:
        result = await payarc.payarcConnect['post_auth'](ecrRefNum="REF12", origRefNum='10', amount='500', deviceSerialNo='1850406725')
        print('Result:', result)
    except Exception as error:
        print('Error detected:', error)

async def last_transaction():
    try:
        result = await payarc.payarcConnect['last_transaction'](deviceSerialNo='1850406725')
        print('Result:', result)
    except Exception as error:
        print('Error detected:', error)

async def server_info():
    try:
        result = await payarc.payarcConnect['server_info']()
        print('Result:', result)
    except Exception as error:
        print('Error detected:', error)


async def terminals():
    try:
        result = await payarc.payarcConnect['terminals']()
        print('Result:', result)
    except Exception as error:
        print('Error detected:', error)


 
asyncio.run(login())
# asyncio.run(sale())
# asyncio.run(void())
# asyncio.run(refund())
# asyncio.run(blind_credit())
# asyncio.run(auth())
# asyncio.run(post_auth())
# asyncio.run(last_transaction())
# asyncio.run(server_info())
# asyncio.run(terminals())