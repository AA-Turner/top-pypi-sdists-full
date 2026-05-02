import asyncio
from flowtask.components.BestBuy import BestBuy
import pandas as pd

print(BestBuy.__mro__)

async def main():
    # create a sample dataframe:
    data = [
        {"location_code": "485", "zipcode": "85395", "Brand": "Bose", "sku": "6550610"},
        {"location_code": "44", "zipcode": "53045", "Brand": "Bose", "sku": "6550610"},
        {"location_code": "56", "zipcode": "75104", "Brand": "Bose", "sku": "6550610"},
        {"location_code": "1489", "zipcode": "53147", "Brand": "Bose", "sku": "6550610"},
        {"location_code": "1112", "zipcode": "85706", "Brand": "Bose", "sku": "6550610"},
        {"location_code": "1113", "zipcode": "92243", "Brand": "Bose", "sku": "6550610"},
    ]
    df = pd.DataFrame(data)
    bby = BestBuy(
        type='availability',
        use_proxies=True,
        paid_proxy=True,
        sku="6550610",
        brand="Bose"
    )
    bby.input = df
    async with bby as comp:
        try:
            result = await comp.run()
            print(len(result), type(result))
            print('RESULT >> ')
            print(result)
        except Exception as e:
            print(f'Error: {e}')


async def get_reviews():
    data = [
        {"sku": "6509757", "model": "86QNED80URA", "brand": "LG"},
    ]
    df = pd.DataFrame(data)
    bby = BestBuy(
        type='reviews',
        use_proxies=True,
        paid_proxy=True
    )
    bby.input = df
    async with bby as comp:
        try:
            result = await comp.run()
            print(len(result), type(result))
            print('RESULT >> ')
            print(result)
        except Exception as e:
            print(f'Error: {e}')

async def get_product():
    data = [
        {"model": "V11HA85020", "brand": "epson"},
        {"model": "V11HB35020", "brand": "epson"},
        {"model": "V11HB38420", "brand": "epson"},
        {"model": "B11B261201", "brand": "epson"},
        {"model": "B11B252201", "brand": "epson"},
        {"model": "B11B258201", "brand": "epson"},
        {"model": "B11B272202", "brand": "epson"},

    ]
    df = pd.DataFrame(data)
    bby = BestBuy(
        type='product',
        use_proxies=True,
        paid_proxy=True
    )
    bby.input = df
    async with bby as comp:
        try:
            result = await comp.run()
            print(len(result), type(result))
            print('RESULT >> ')
            print(result)
        except Exception as e:
            print(f'Error: {e}')

if __name__ == '__main__':
    # asyncio.run(main())
    # asyncio.run(get_product())
    asyncio.run(get_reviews())
