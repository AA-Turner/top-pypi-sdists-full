import asyncio
from flowtask.components.Target import Target
import pandas as pd

async def get_reviews():
    data = [
        {"sku": "85412323", "model": "86QNED80URA", "brand": "LG"},
    ]
    df = pd.DataFrame(data)
    import os
    # SECURITY: API token removed from hardcoded values. Use TARGET_API_TOKEN environment variable
    target = Target(
        type='reviews',
        use_proxies=True,
        paid_proxy=True,
        api_token=os.environ.get('TARGET_API_TOKEN', '')
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
