import asyncio
import pandas as pd
from flowtask.components.CompanyScraper import CompanyScraper


async def main():
    # create a sample dataframe:
    data = [
        {"Company Name": "Skeye Wholesale", "List Name": "Best Buy"},
        # {"Company Name": "NVIDIA", "List Name": "Best Buy"},
        # {"Company Name": "Acer", "List Name": "Best Buy"},
        # {"Company Name": "Adobe", "List Name": "Best Buy"},
        # {"Company Name": "Alpine Electronics of America", "List Name": "Best Buy"},
    ]
    df = pd.DataFrame(data)
    cp = CompanyScraper(
        use_proxies=True,
        paid_proxy=True,
        column_name="Company Name",
        scrappers=["rocketreach"],
        concurrently=False,
        input=df
    )
    async with cp as comp:
        try:
            result = await comp.run()
            print(len(result), type(result))
        except Exception as e:
            print(f'Error: {e}')


if __name__ == '__main__':
    asyncio.run(main())
