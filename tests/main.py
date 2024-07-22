import asyncio

from src.payarc.payarc import Payarc

PORT = 2999
PAYARC_ENV = 'http://localapi5.payarc.net'
PAYARC_VERSION = 1
PAYARC_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIyNiIsImp0aSI6IjZkNTA1YTA2YjdlNWMwYTk5OGU4MWQ2YjJjYmJmMWFjNzFkMGFlNWU0MmE2MjIxMzk5NGZhYzE4MzI1ZWVlNDhhOGQ0MDRkZTVjNDc5NTYyIiwiaWF0IjoxNjU5MDIwNjUyLCJuYmYiOjE2NTkwMjA2NTIsImV4cCI6MTgxNjY4OTg1Miwic3ViIjoiMTU0MTQiLCJzY29wZXMiOiIqIn0.KDaegyhna7eFAQRQfIuYv-nVFPI2G7iMyCR4fyEFwtirXOxAky7Sie0Oc8HJXiuQ9k7UaNhGF3akFo_8vipTBfQD6L-_wbr8Nj3vf_EuX2Yjz35e5HBBwaJ3b5vGXJGsu_UlpgIntLYPW6DRFSWAdzTtv0t6uyW_98oVvhm-Yxf6stj-UR3mHA18tjP1ISti53Oc2BrIKH_s58eFFdyzj6q1Q63r05uAQ9XC96Gl35ZCnaGEzcWgviTxCrKVfMuRKCzFKB-rJPlRM1lfzGcz-5wvWuqp0jWgsS383I7Pn1uXRWTxasHM93-ioa7TCWlOtyvmrs1_HIG8x9c2QgUoPXGhKzCA8pYiYyeWfguPX250P03B3hks3hZSMu6L9f1xbCBBFH484oMdxYn-CUAOQhysFN7b9-O6PW0Ge2XhsCA3rs3c9vEewTlPggoa8WHr4tTOS1GdCFxneFPzHjsbB3C-ig7r7Qq6594nw-Bb_l2ONsVmsQ19GTU08zwq4hKtdKyPI879pvh9f-IDqJliHAc1qXga5pqX_Cj4pkcTihltdQ3Q0KyKp-Wi3O0Xi6afw8EXcrVLlDnVtyic8sbBpl8Gh8EVOL1zq8D4qwrWH-oZSITmZaBqRiTz-UaKmRyMVg0yVxAfGfqjXtNYkINJEQxwS2X-Id_Mr0sUb72LmyE'
# AGENT_KEY='eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxNDEzMSIsImp0aSI6IjQ1ZjY3ZDI4YmY2MWY0MWQ5ZGI4MmM2NDgyNWYzYjA5ODMxNzlmNTM3NjIxYmFhMTUzNzQ1NGYzOGI1NDNhZDRlYzBlM2M2Y2E4YWI2NWEzIiwiaWF0IjoxNzE4Njk3NDQ1LCJuYmYiOjE3MTg2OTc0NDUsImV4cCI6MTg3NjM3NzQ0NSwic3ViIjoiMjcxMzAiLCJzY29wZXMiOlsiKiJdfQ.HUFhytxuiGihb5GDKWqbfNkHf5_5irtGbO47M59sl_9rk02oJ5U00HfT6-G6IyJUmVtJ_wbk5KBVdSgyNSVQB15I-eGzF8ljQkGbOoyPMZp5VHHCjFeKHI5VMA_POlRFchGn3wXnsoox1ckQZW2tqUUu2yeUw1Rycb2kEGhqsw2jWGj5JOnUFfebIHDy1RNtFBfMtaxSnVaArU-vSTibWUREkJzAMTVNlhuKPD3m0ufIli_9444RBPsuD8Vot4nHfjyHZOriP0VsTepft0CFXVj8ENf5pPdxeI8UnrQ99EMkFy6AYBd0cx3aZmcNXLDnCJFz9I6u06vRvcpb4YzW3120zWGiLyRyrFv65tSMD5vXlA1_AasRYQArNYz5EYABsQcHmT44Mh9OwGgx5TUupMmtnx-m9lbV8Zl7uxnMc3QcEIIfdFtjaIMdLvbj0JTcjsxQHxKQpc1v5nsirFXCg2Q73Za4CDs1L7U5j_DOn85RC3MaOKbJlU3e9JBXBaESJNx-3EqYW5HvIlHL0VgE8cA-FIu_VGF9BDXYh6mtc1EBidiX7KZes6GFJzbixm8a3Rgcj5zIeqhHpIqgD1lB6dCOFjB8ve01if3iTPnKJY9_bzrZH8NC6j-iKsEsfxxg_iINMNzAPPyV40E77oxqIO7VXsgVlZGJDE_vknn71hc'
AGENT_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxNDEzMSIsImp0aSI6IjhmMGI3Mjk1MWU4ZjFmNDVkZTBkMGNiNDUzNzQ0NmM2ZDNiZjQ2YmU1MzUzM2Y0ZTdjM2Y1NTgxYjQ4NmQ5NzgxMzBjZmY5Yjg5NzQ0MTJjIiwiaWF0IjoxNzIwNjA0MDI0LjAwNzM1OCwibmJmIjoxNzIwNjA0MDI0LjAwNzM2LCJleHAiOjE3NTIxNDAwMjMuOTkwOTI3LCJzdWIiOiIyNjgyNCIsInNjb3BlcyI6W119.MJd00DURXiEND3skh94tTm_KryrDpMzaamhAN_7H_Oo80OZicf7G3Y0fJbEir2RUeiHDup5kRY7R3oZ6Y4BBkFHe-DGSZtwca9wgmrzBpNFaDt2l0dBUmvBUAK80V_OEajHb911VInjWyZ5UgUhm0gMFSj5dqh8eZrmmsgS8J4vwtJd2ONTR-z2HUqdGYGc4PRh0q-69KEnESddETlE5O_NxY8jy-wwzv5TbjAasv8ddjFBuKXw_s8kgxlG1r9coLev4ECZqC2fDcC1dlTVZ1tBpMPel6wMjevuG6_GF5ZDaV44_LoOXC3cLfu3CkFIYv3RKR7sALrXjrVHGdmmeWXaTqSJ8_APtYyMXuPkWuszhZX04wgJ0cZv8haijd0gBk8esw9xlde2Iy5ZzrJFtVaBE3i_eI5q9Ptfsh-k0EUzwri4AaNX4S0jczvPDbhf4X59jiKVxBfG2xRRCVGZqXNYySHM7t7tm1e59GGkLAX2Edrsi8GglqRX4b-DFteCTNjPGCQCS7KtCEvJlZ5w2m9EddUnUvjv5j9l9llQ5HLhjLvS03X2OnJfRvTaOro-JGH4fo1F-aRK9zJZhDs2yGckIJZmk4dQQz4kwZj-A0_I1aJDKA0sxfDyXjw2St-B3rn7hPwJcRnJEVg_xCiqvUN-bpfEx7b9NgRntvOwf4ic'
payarc = Payarc(bearer_token=PAYARC_KEY, bearer_token_agent=AGENT_KEY, base_url=PAYARC_ENV, version=PAYARC_VERSION)


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


# Run the example
if __name__ == "__main__":
    # asyncio.run(create_charge_example())
    # asyncio.run(list_charges({'limit': 50, 'page': 2}))
    # asyncio.run(get_charge_by_id('ch_nbDBOMWRyyRnMORX'))
    # asyncio.run(refund_charge('ch_MnBROWLXBBXnoOWL'))
    asyncio.run(refund_charge_by_obj('ch_MnBROWLXBBXnoOWL',
                                     {'reason': 'requested_by_customer',
                                      'description': 'The customer returned the product, did not like it'}))
