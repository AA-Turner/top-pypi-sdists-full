import asyncio
from flowtask.components.GooglePlaces import GooglePlaces
from flowtask.components.GoogleGeoCoding import GoogleGeoCoding
import pandas as pd

async def test_places():
    # create a sample dataframe:
    data = [
        {"place_id": "ChIJgZP1lVzkV4YRG1cvFi-BC98"}
    ]
    df = pd.DataFrame(data)
    places = GooglePlaces(
        use_proxies=True,
        paid_proxy=True,
        type="traffic",
        input=df
    )
    async with places as comp:
        try:
            result = await comp.run()
            print(len(result), type(result))
            print('RESULT >> ')
            print(result)
        except Exception as e:
            print(f'Error: {e}')

async def test_geocoding():
    # create a sample dataframe:
    data = [
        {
            "store_name": "Wal-Mart Supercenter",
            "city": "Alva",
            "state_code": "OK",
            "zipcode": "73717",
            "street_address": "914 E Oakland Blvd",
        }
    ]
    df = pd.DataFrame(data)
    geocoding = GoogleGeoCoding(
        place_prefix="store_name",
        use_find_place=True,
        return_pluscode=True,
        chunk_size=50,
        columns=[
            'street_address',
            'city',
            'state_code',
            'zipcode'
        ],
        input=df
    )
    async with geocoding as comp:
        try:
            result = await comp.run()
            print(len(result), type(result))
            print('RESULT >> ')
            print(result)
        except Exception as e:
            print(f'Error: {e}')

if __name__ == '__main__':
    asyncio.run(test_places())
