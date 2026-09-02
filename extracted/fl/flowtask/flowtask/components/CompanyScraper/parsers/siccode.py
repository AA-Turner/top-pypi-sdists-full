import time
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException
)
from .base import ScrapperBase


class SicCodeScrapper(ScrapperBase):
    """
    SicCodeScrapper Model.
    """
    domain: str = 'siccode.com'
    search_term: str = "site:siccode.com '{}' +NAICS"
    keywords: list = [
        ' - ZIP',
        ' - ZIP '
    ]

    def define_search_term(self, term: str):
        cleaned = term.strip().lower()
        return self.search_term.format(cleaned)

    # async def get(self, url, headers: dict):
    #     self.use_proxy = True
    #     self._free_proxy = False
    #     driver = await self.get_driver()
    #     try:
    #         try:
    #             driver.get(url)
    #             # WebDriverWait(driver, 2).until(
    #             #     EC.presence_of_element_located((By.ID, "main"))
    #             # )
    #             return bs(driver.page_source, 'html.parser')
    #         except TimeoutException:
    #             return None
    #     finally:
    #         self.close_driver()

    async def scrapping(self, document: bs, idx: int, row: dict):
        """
        Scrapes company information from siccode.com and updates the row.
        """
        result = row.copy()
        result.update({
            'source_platform': 'siccode',
            'scrape_status': 'pending',
            'search_term': self.search_term_used
        })

        try:
            header = document.select_one("div.main-title")
            # Extract company name
            result["company_name"] = (
                header.select_one("h1.size-h2 a span") and
                header.select_one("h1.size-h2 a span").text.strip()
            )
            # Extract Industry Category
            result["industry_category"] = header.select_one("b.p-category").text.strip()

            # Extract SIC and NAICS Codes
            desc = document.find('div', {'id': 'description'})
            sic_code_elem = desc.select_one("a.sic")
            naics_code_elem = desc.select_one("a.naics")

            sic = sic_code_elem.text.split("SIC CODE")[-1].strip() if sic_code_elem else None
            naics = naics_code_elem.text.split("NAICS CODE")[-1].strip() if naics_code_elem else None
            result["sic_code"], result["industry"] = sic.split(' - ')
            result["naics_code"], result["category"] = naics.split(' - ')
            # Extract Location Details
            overview = document.find('div', {'id': 'overview'})
            result['company_description'] = overview.select_one("p.p-note").text.strip()

            result["city"] = overview.select_one(".p-locality") and overview.select_one(".p-locality").text.strip()
            result["state"] = overview.select_one(".p-region") and overview.select_one(".p-region").text.strip()
            result["zip_code"] = overview.select_one(".p-postal-code") and overview.select_one(".p-postal-code").text.strip()
            result["country"] = overview.select_one(".p-country-name") and overview.select_one(".p-country-name").text.strip()
            result["metro_area"] = overview.select_one("div[title]") and overview.select_one("div[title]").text.strip()

            # Construct Headquarters Address
            result["headquarters"] = ", ".join(
                filter(None, [result.get("city"), result.get("state"), result.get("zip_code"), result.get("country")])
            )

            # Check if we found any meaningful data
            has_data = any([
                result.get("company_name"),
                result.get("category"),
                result.get("sic_code"),
                result.get("naics_code"),
                result.get("headquarters"),
                result.get("revenue_range"),
                result.get("years_in_business"),
                result.get("company_size"),
            ])

            result['scrape_status'] = 'success' if has_data else 'no_data'

            return idx, result

        except Exception as e:
            self._logger.error(f"Error parsing SICCode data: {str(e)}")
            result['scrape_status'] = f'error: {str(e)[:50]}'
            return idx, result
