import re
from bs4 import BeautifulSoup as bs
from .base import ScrapperBase


class RocketReachScrapper(ScrapperBase):
    """
    RocketReachScrapper Model.
    """
    domain: str = 'https://rocketreach.co/'
    search_term: str = "site:rocketreach.co '{}'"
    keywords: list = [
        ' Information',
        ' Information - ',
        ' Information - RocketReach',
        ': Contact Details'
    ]

    def define_search_term(self, term: str):
        # standardized_term = self._standardize_name(term)
        standardized_term = term.strip()
        return self.search_term.format(standardized_term)

    def _extract_codes(self, value):
        """
        Extracts NAICS/SIC codes from RocketReach company info.
        """
        codes = []
        for link in value.find_all("a"):  # Iterate over <a> elements
            match = re.search(r"\b\d+\b", link.text)  # Extract only numbers
            if match:
                codes.append(match.group())  # Store only the number part
        return codes  # Return the list of codes

    async def scrapping(self, document: bs, idx: int, row: dict):
        """
        Scrape company information from LeadIQ.
        Updates the existing row with new data from LeadIQ.
        """
        # Start with the existing row data
        result = row.copy()

        # Actualizamos solo los campos específicos de LeadIQ
        result.update({
            'source_platform': 'rocketreach',
            'scrape_status': 'pending',
            'search_term': self.search_term_used
        })
        try:
            # Extract `company-header` details
            company_header = document.select_one(".company-header")
            if company_header:
                # Extract company logo
                img_tag = company_header.select_one(".company-logo")
                result["logo_url"] = img_tag["src"] if img_tag else None

                # Extract company name
                title_tag = company_header.select_one(".company-title")
                if title_tag:
                    result["company_name"] = title_tag.text.replace(" Information", "").strip()

            # Extract company description from `headline-summary`
            headline_summary = document.select_one(".headline-summary p")
            result["company_description"] = headline_summary.text.strip() if headline_summary else None

            # Extract details from the information table
            info_table = document.select(".headline-summary table tbody tr")
            for row in info_table:
                key = row.select_one("td strong")
                value = row.select_one("td:nth-of-type(2)")

                if key and value:
                    key_text = key.text.strip().lower()
                    value_text = value.text.strip()

                    if "website" in key_text:
                        result["website"] = value.select_one("a")["href"] if value.select_one("a") else value_text

                    elif "ticker" in key_text:
                        result["stock_symbol"] = value_text

                    elif "revenue" in key_text:
                        result["revenue_range"] = value_text

                    elif "funding" in key_text:
                        result["funding"] = value_text

                    elif "employees" in key_text:
                        result["employee_count"] = value_text.split()[0]
                        result['number_employees'] = value_text

                    elif "founded" in key_text:
                        result["founded"] = value_text

                    elif "address" in key_text:
                        result["headquarters"] = value.select_one("a").text.strip() if value.select_one("a") else value_text

                    elif "phone" in key_text:
                        result["phone_number"] = value.select_one("a").text.strip() if value.select_one("a") else value_text

                    elif "industry" in key_text:
                        result["industry"] = [i.strip() for i in value_text.split(",")]

                    elif "keywords" in key_text:
                        result["keywords"] = [i.strip() for i in value_text.split(",")]

                    elif "sic" in key_text:
                        result["sic_code"] = self._extract_codes(value)

                    elif "naics" in key_text:
                        result["naics_code"] = self._extract_codes(value)

            # Validate if any meaningful data was found
            has_data = any([
                result.get('company_name'),
                result.get('logo_url'),
                result.get('headquarters'),
                result.get('phone_number'),
                result.get('website'),
                result.get('stock_symbol'),
                result.get('naics_code'),
                result.get('sic_code'),
                result.get('employee_count'),
                result.get('revenue_range'),
                result.get('company_description')
            ])
            result['scrape_status'] = 'success' if has_data else 'no_data'
            return idx, result

        except Exception as e:
            self._logger.error(f"Error parsing LeadIQ data: {str(e)}")
            result['scrape_status'] = f'error: {str(e)[:50]}'
            return idx, result
