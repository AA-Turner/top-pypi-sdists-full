from bs4 import BeautifulSoup
from .ScrapPage import ScrapPage
from ..exceptions import ComponentError


class ScrapSearch(ScrapPage):
    """
    Search by a Product, retrieve the URL (based on rules) and scrap the page.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          ScrapSearch:
          # attributes here
        ```
    """
    _version = "1.0.0"
    # TODO: Idea is for making the search functions pluggable.
    def __init__(self, **kwargs):
        self.find_element: tuple = kwargs.pop('find_element', ('li', {'class': ['sku-item']}))
        super().__init__(**kwargs)
        self.product_sku: str = kwargs.pop('product_sku', None)
        self.brand: str = kwargs.pop('brand', None)

    async def _bby_products(self):
        front_url = "https://www.bestbuy.com/site/searchpage.jsp?cp="
        middle_url = "&searchType=search&st="
        page_count = 1
        # TODO: Get the Brand and Model from the Component.
        model = self.product_sku
        brand = self.brand
        search_term = f'{brand}%20{model}'
        end_url = "&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All%20Categories&ks=960&keys=keys"  # noqa
        url = front_url + str(page_count) + middle_url + search_term + end_url
        print('SEARCH URL: ', url)
        return url

    async def _search_bby_products(self, content: str) -> str:
        soup = BeautifulSoup(content, 'html.parser')
        # Find all elements with class "sku-item"
        product_items = soup.find_all(*self.find_element)
        # Iterate over each product item
        url = None
        for item in product_items:
            # Get the "data-sku-id" attribute
            sku_id = item.get("data-sku-id")
            # Check if the SKU ID matches your target SKU ID
            if sku_id == self.product_sku:
                print(f"Found matching SKU ID: {sku_id}")
                # Now look for the child with class "sku-title"
                pd = item.find('h4', {'class': ['sku-title']})
                anchor = pd.a
                url = "https://www.bestbuy.com{url}".format(
                    url=anchor['href']
                )
                print('Product URL: ', url)
        return url

    async def run(self):
        # Run works differently for ScrapPage:
        self._result = None
        screenshot = None
        # 1. Get the Product List URL
        fn = getattr(self, f"_{self.url_function}", None)
        if not fn:
            raise ComponentError(
                f"Function {self.url_function} not found."
            )
        url = await fn()
        if self.use_selenium is True:
            await self.get_page(url, self.cookies)
            content = self.driver().page_source
            # 2. Search the Product
            search_fn = getattr(self, f"_search_{self.url_function}", None)
            if search_fn:
                url = await search_fn(content)
                if url:
                    # 3. Get the URL
                    self.url = url
                    # 4. Run the Scrapping Tool to extract the Product page.
                    content, screenshot = await self.run_selenium()
                    if self.return_driver is True:
                        self._result = self.driver()
                    else:
                        self._result = self._build_result_content(
                            content,
                            screenshot
                        )
        return self._result
