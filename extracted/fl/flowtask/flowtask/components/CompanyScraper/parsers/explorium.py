from bs4 import BeautifulSoup as bs
from .base import ScrapperBase
import json


class ExploriumScrapper(ScrapperBase):
    """
    ExploriumScrapper Model.
    """
    domain: str = 'explorium.ai'
    search_term: str = 'site:explorium.ai {}'
    keywords: list = [
        'overview - services',
    ]

    def define_search_term(self, term: str):
        cleaned = term.strip().lower()
        return self.search_term.format(cleaned)

    async def scrapping(self, document: bs, idx: int, row: dict):
        """
        Scrape company information from Explorium.
        Updates the existing row with new data from Explorium.
        """
        # Start with the existing row data
        result = row.copy()

        # Actualizamos solo los campos específicos de Explorium
        result.update({
            'source_platform': 'explorium',
            'scrape_status': 'pending',
            'search_term': self.search_term_used
        })

        try:
            # Extraer información de la compañía
            company_info = document.find('div', {'class': 'company-info'})
            if company_info:
                # Nombre de la compañía
                company_name = company_info.find('h1', {'class': 'company-name'})
                if company_name:
                    result['company_name'] = company_name.text.strip()

                # Dirección
                address = company_info.find('div', {'class': 'address'})
                if address:
                    address_info = self._parse_address(address.text.strip())
                    result.update(address_info)

                # Otros detalles de la compañía
                details = company_info.find_all('div', {'class': 'detail-item'})
                for detail in details:
                    label = detail.find('span', {'class': 'label'})
                    value = detail.find('span', {'class': 'value'})
                    if label and value:
                        field = label.text.strip().lower()
                        val = value.text.strip()

                        if 'phone' in field:
                            result['phone_number'] = val
                        elif 'website' in field:
                            result['website'] = val
                        elif 'employees' in field:
                            result['employee_count'] = val
                        elif 'revenue' in field:
                            result['revenue_range'] = val
                        elif 'naics' in field:
                            result['naics_code'] = val
                        elif 'sic' in field:
                            result['sic_code'] = val

            # 🔍 Extract NAICS & SIC codes and industry descriptions
            result.update(self._extract_naics_sic(document))

            # Extract company logo, headquarters, country, and description
            result.update(self._extract_company_info(document))

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
                result.get('logo_url')
            ])

            # Establecemos el estado según si encontramos datos o no
            result['scrape_status'] = 'success' if has_data else 'no_data'

            # Siempre devolvemos el resultado, tenga datos o no
            return idx, result

        except Exception as e:
            self._logger.error(f"Error parsing Explorium data: {str(e)}")
            result['scrape_status'] = f'error: {str(e)[:50]}'
            return idx, result

    def _extract_naics_sic(self, document: bs):
        """
        Extract NAICS & SIC codes along with their industry descriptions.

        Returns:
            dict: A dictionary containing 'naics_code', 'sic_code', and 'industry' (comma-separated).
        """
        result = {
            'naics_code': None,
            'sic_code': None,
            'industry': None
        }

        naics_codes = []
        sic_codes = []
        industries = []

        # Extract NAICS section
        naics_section = document.find('div', {'data-id': 'company-stat-naics'})
        if naics_section:
            naics_entries = naics_section.find_all('p', {'class': 'ExpTypography-root'})
            for entry in naics_entries:
                code = entry.text.strip().strip(',')
                industry_desc = entry.get('aria-label', '').strip()
                if code:
                    naics_codes.append(code)
                if industry_desc:
                    industries.append(industry_desc)

        # Extract SIC section
        sic_section = document.find('div', {'data-id': 'company-stat-sic'})
        if sic_section:
            sic_entries = sic_section.find_all('p', {'class': 'ExpTypography-root'})
            for entry in sic_entries:
                code = entry.text.strip().strip(',')
                industry_desc = entry.get('aria-label', '').strip()
                if code:
                    sic_codes.append(code)
                if industry_desc:
                    industries.append(industry_desc)

        # Convert lists to comma-separated strings
        if naics_codes:
            result['naics_code'] = ', '.join(naics_codes)
        if sic_codes:
            result['sic_code'] = ', '.join(sic_codes)
        if industries:
            result['industry'] = ', '.join(industries)

        return result

    def _extract_company_info(self, document: bs):
        """
        Extract headquarters, country, company description, and logo.
        """
        result = {
            'headquarters': None,
            'country': None,
            'company_description': None,
            'logo_url': None
        }

        # Extract headquarters address
        address_section = document.find('div', {'data-id': 'info-address'})
        if address_section:
            address_element = address_section.find('p', {'aria-label': True})
            if address_element:
                address_text = address_element.get('aria-label', '').strip()
                result['headquarters'] = address_text

                # Extract country (last word in the address)
                country = address_text.split(',')[-1].strip()
                result['country'] = country if country else None

        # Extract company description
        name_element = document.find('h1', {'data-id': 'txt-company-name'})
        description_element = document.find('p', {'class': 'ExpTypography-root ExpTypography-body1'})
        if name_element and description_element:
            company_name = name_element.text.strip()
            company_desc = description_element.text.strip()
            result['company_description'] = f"{company_name}: {company_desc}"

        # Extract company logo
        logo_element = document.find('img', {'alt': True, 'src': True})
        if logo_element:
            result['logo_url'] = logo_element['src']

        return result
