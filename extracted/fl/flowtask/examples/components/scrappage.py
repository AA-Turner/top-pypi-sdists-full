import asyncio
from selenium.webdriver.common.by import By
from flowtask.components.ScrapPage import ScrapPage
from flowtask.components.ScrapSearch import ScrapSearch

async def scrapping():
    # Scrapping a Sample Page with HTTPx or Selenium.
    cookies = {
        "SID": "9627390e-b423-459f-83ee-7964dd05c9a8",
        "bby_rdp": "l",
        "CTT": "4e07e03ff03f5debc4e09ac4db9239ac",
        "bby_cbc_lb": "p-browse-e",
        "intl_splash": "false"
    }
    scrap = ScrapPage(
        url="https://www.bestbuy.com/?intl=nosplash",
        # url="https://trocglobal.com/",
        use_proxy=False,
        use_selenium=True,
        # accept_cookies=('id', 'cn-accept-cookie'),
        inner_tag=('tag_name', 'body'),  # only return the innerHTML of this tag
        cookies=cookies,
        # wait_until=(By.CLASS_NAME, 'product-name'),
        screenshot={
            "filename": 'screenshot.png',
            "directory": 'screenshots',
            "portion": ('tag_name', 'body')
        }
    )
    async with scrap as comp:
        try:
            result = await comp.run()
            print(len(result), type(result))
            # print('RESULT >> ')
            # print(result)
        except Exception as e:
            print(f'Error: {e}')

async def scrapping_search():
    # Search by a Product, retrieve the URL (based on rules) and scrap the page.
    cookies = {
        "SID": "9627390e-b423-459f-83ee-7964dd05c9a8",
        "bby_rdp": "l",
        "CTT": "4e07e03ff03f5debc4e09ac4db9239ac",
        "bby_cbc_lb": "p-browse-e",
        "intl_splash": "false"
    }
    scrap = ScrapSearch(
        url_function="bby_products",
        product_sku="6554466",
        brand="Bose",
        use_proxy=True,
        use_free_proxy=False,
        find_element=('li', {'class': ['sku-item']}),
        use_selenium=True,
        inner_tag=('tag_name', 'body'),  # only return the innerHTML of this tag
        cookies=cookies,
        screenshot={
            "filename": 'product-screenshot.png',
            "directory": 'screenshots',
            "portion": ('tag_name', 'body')
        }
    )
    async with scrap as comp:
        try:
            result = await comp.run()
            print(len(result), type(result))
            # print('RESULT >> ')
            # print(result)
        except Exception as e:
            print(f'Error: {e}')

if __name__ == '__main__':
    # asyncio.run(scrapping())
    asyncio.run(scrapping_search())
