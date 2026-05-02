import asyncio
import pandas as pd
from flowtask.components.ServiceScrapper import ServiceScrapper

async def scrappe_events():
    df = pd.DataFrame([{
        'url': 'https://www.consumeraffairs.com/insurance/assurant-phone-insurance.html',
    }])
    costco = ServiceScrapper(
        scrapper='costco',
        function='special_events',
        column_name='url',
        input=df
    )
    try:
        async with costco as comp:
            print(f' :: Starting Component {comp} ::')
            result = await comp.run()
            print(len(result), type(result))
            print('RESULT >> ')
            print(result)
    except Exception as err:
        print('ERROR >> ', err)


if __name__ == '__main__':
    asyncio.run(scrappe_events())
