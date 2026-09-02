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


class ZoomInfoScrapper(ScrapperBase):
    """
    ZoomInfo Model.
    """
    domain: str = 'zoominfo.com'
    search_term: str = 'site:zoominfo.com {} Overview'
    keywords: list = [
        ' - Overview, News',
        'Overview, News'
    ]

    def define_search_term(self, term: str):
        cleaned = term.strip().lower()
        return self.search_term.format(cleaned)

    async def get(self, url, headers: dict):
        self.use_proxy = True
        self._free_proxy = False
        self.use_undetected = True
        driver = await self.get_driver()
        try:
            try:
                print('URL > ', url)
                driver.get(url)
                return driver.page_source
            except TimeoutException:
                return None
        finally:
            self.close_driver()

    async def scrapping(self, document: bs, idx: int, row: dict):
        """
        Scrape company information from Zoominfo.
        Updates the existing row with new data from Zoominfo.
        """
        # Start with the existing row data
        result = row.copy()

        # Actualizamos solo los campos específicos de Explorium
        result.update({
            'source_platform': 'zoominfo',
            'scrape_status': 'pending',
            'search_term': self.search_term_used
        })

        try:

            # Extraer información de la compañía
            result.update({
                "company_name": document.select_one("h2#company-description-text-header") and document.select_one("h2#company-description-text-header").text.strip(),
                "headquarters": document.select_one(".icon-label:-soup-contains('Headquarters') + .content") and document.select_one(".icon-label:-soup-contains('Headquarters') + .content").text.strip(),
                "phone_number": document.select_one(".icon-label:-soup-contains('Phone Number') + .content") and document.select_one(".icon-label:-soup-contains('Phone Number') + .content").text.strip(),
                "website": document.select_one(".icon-label:-soup-contains('Website') + a") and document.select_one(".icon-label:-soup-contains('Website') + a")["href"],
                "revenue_range": document.select_one(".icon-label:-soup-contains('Revenue') + .content") and document.select_one(".icon-label:-soup-contains('Revenue') + .content").text.strip(),
                "stock_symbol": document.select_one(".icon-label:-soup-contains('Stock Symbol') + .content") and document.select_one(".icon-label:-soup-contains('Stock Symbol') + .content").text.strip(),
                "industry": [i.text.strip() for i in document.select("#company-chips-wrapper a")],
                "company_description": document.select_one("#company-description-text-content .company-desc") and document.select_one("#company-description-text-content .company-desc").text.strip(),
            })  # noqa

            # Extracting NAICS and SIC codes
            codes_section = document.select("#codes-wrapper .codes-content")
            result["naics_code"], result["sic_code"] = None, None  # Default to None

            for code in codes_section:
                text = code.text.strip()
                if "NAICS Code" in text:
                    result["naics_code"] = text.replace("NAICS Code", "").strip()
                elif "SIC Code" in text:
                    result["sic_code"] = text.replace("SIC Code", "").strip()

            # Extract executives
            result["executives"] = [
                {
                    "name": exec.select_one(".person-name").text.strip(),
                    "title": exec.select_one(".job-title").text.strip(),
                    "profile_link": exec.select_one(".person-name")["href"]
                }
                for exec in document.select(".org-chart .person-right-content")
                if exec.select_one(".person-name")
            ]

            # Verificamos si se encontró algún dato
            has_data = any([
                result.get('company_name'),
                result.get('headquarters'),
                result.get('country'),
                result.get('phone_number'),
                result.get('website'),
                result.get('stock_symbol'),
                result.get('naics_code'),
                result.get('sic_code'),
                result.get('employee_count'),
                result.get('revenue_range'),
                result.get('company_description'),
            ])

            # Establecemos el estado según si encontramos datos o no
            result['scrape_status'] = 'success' if has_data else 'no_data'

            # Siempre devolvemos el resultado, tenga datos o no
            return idx, result
        except Exception as e:
            self._logger.error(f"Error parsing Zoominfo data: {str(e)}")
            result['scrape_status'] = f'error: {str(e)[:50]}'
            return idx, result
