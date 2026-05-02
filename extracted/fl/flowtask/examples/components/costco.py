import asyncio
from flowtask.components.Costco import Costco
import pandas as pd

async def get_reviews():
    data = [
        {
            "product_url": "https://www.costco.com/kidkraft-atrium-breeze-wooden-outdoor-playhouse-with-sunroom--play-kitchen.product.4000317158.html",
            "product_id": "4000317158",
            "brand": "KidKraft"
        },
    ]
    df = pd.DataFrame(data)
    target = Costco(
        type='reviews',
        use_proxy=False,
        paid_proxy=False,
        input=df
    )
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
