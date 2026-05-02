import asyncio
from flowtask.components.ScrapPage import ScrapPage

async def scrapping():
    # Scrapping a Sample Page with HTTPx or Selenium.
    scrap = ScrapPage(
        urls=["https://cnnespanol.cnn.com/", "https://docs.python.org/3/library/functions.html"],
        use_proxy=False,
        use_selenium=True,
        accept_cookies=('id', 'onetrust-accept-btn-handler'),
        driver_options={},
        screenshot={
            "filename": 'screenshot.png',
            "directory": 'screenshots',
        }
    )
    async with scrap as comp:
        try:
            result = await comp.run()
            print(len(result), type(result))
            print('RESULT >> ')
            print(result)
        except Exception as e:
            print(f'Error: {e}')

if __name__ == '__main__':
    asyncio.run(scrapping())
