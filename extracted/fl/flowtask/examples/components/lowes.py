import asyncio
from flowtask.components.Lowes import Lowes
import pandas as pd

async def get_reviews():
    data = [
        {
            "sku": "1000625115",
            "model": "86QNED80URA",
            "brand": "LG"
        },
    ]
    df = pd.DataFrame(data)
    target = Lowes(
        type='reviews',
        use_proxies=True,
        paid_proxy=True,
        api_token=__import__('os').environ.get('LOWES_API_TOKEN', '')  # SECURITY: Use LOWES_API_TOKEN env var
    )
    target.input = df
    async with target as comp:
        try:
            result = await comp.run()
            print(len(result), type(result))
            print('RESULT >> ')
            print(result)
        except Exception as e:
            print(f'Error: {e}')

async def get_details():
    data = [
        {
            "sku": "1000625115",
            "model": "86QNED80URA",
            "brand": "LG",
            "store_id": "1845",
            "zipcode": "60639",
            "state_code": "IL"
        },
    ]
    df = pd.DataFrame(data)
    target = Lowes(
        type='product_details',
        use_proxies=True,
        paid_proxy=True,
        api_token=__import__('os').environ.get('LOWES_API_TOKEN', '')  # SECURITY: Use LOWES_API_TOKEN env var
    )
    target.input = df
    async with target as comp:
        try:
            result = await comp.run()
            print(len(result), type(result))
            print('RESULT >> ')
            print(result)
        except Exception as e:
            print(f'Error: {e}')

async def get_products():
    data = [
        {
            "search_term": "Backyard Heartland",
            "brand": "Heartland"
        },
    ]
    df = pd.DataFrame(data)
    target = Lowes(
        type='product_info',
        use_proxies=True,
        proxy_type='oxylabs',
        paid_proxy=True,
        api_token=__import__('os').environ.get('LOWES_API_TOKEN', '')  # SECURITY: Use LOWES_API_TOKEN env var
    )
    target.input = df
    async with target as comp:
        try:
            result = await comp.run()
            print(len(result), type(result))
            print('RESULT >> ')
            print(result)
        except Exception as e:
            print(f'Error: {e}')

if __name__ == '__main__':
    asyncio.run(get_products())
