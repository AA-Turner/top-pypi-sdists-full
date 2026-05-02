import asyncio
from flowtask.components.Amazon import Amazon
import pandas as pd

async def get_reviews():
    data = [
        {"asin": "B0CVSJ9F9L", "sku": "6535922", "model": "86QNED80URA", "brand": "LG"},
    ]
    df = pd.DataFrame(data)
    target = Amazon(
        type='reviews',
        use_proxies=True,
        paid_proxy=True
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
        {"asin": "B0CVSJ9F9L", "sku": "6535922", "model": "86QNED80URA", "brand": "LG"},
    ]
    df = pd.DataFrame(data)
    target = Amazon(
        type='product_info',
        use_proxies=True,
        paid_proxy=True,
        proxy_type='oxylabs'
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
