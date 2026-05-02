import asyncio
from flowtask.components.Walmart import Walmart
import pandas as pd

async def get_reviews():
    data = [
        {
            "itemId": "2282978809",
            "model": "86QNED80URA",
            "brand": "LG"
        },
    ]
    df = pd.DataFrame(data)
    import os
    # SECURITY: API token removed from hardcoded values. Use WALMART_API_TOKEN environment variable
    target = Walmart(
        type='reviews',
        use_proxies=True,
        paid_proxy=True,
        api_token=os.environ.get('WALMART_API_TOKEN', '')
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
    asyncio.run(get_reviews())
