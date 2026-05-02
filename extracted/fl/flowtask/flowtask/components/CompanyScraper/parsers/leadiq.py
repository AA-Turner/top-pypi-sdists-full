from bs4 import BeautifulSoup as bs
from .base import ScrapperBase
import json


class LeadiqScrapper(ScrapperBase):
    """
    LeadiqScrapper Model.
    """
    domain: str = 'leadiq.com'
    search_term: str = "site:leadiq.com {}"
    keywords: list = [
        'Email Formats & Email Address',
        'Company Overview',
        'Employee Directory',
        'Contact Details & Competitors',
        'Email Format'
    ]

    def define_search_term(self, term: str):
        standardized_term = self._standardize_name(term)
        search_term = self.search_term.format(standardized_term)
        return search_term

    async def scrapping(self, document: bs, idx: int, row: dict):
        """
        Scrape company information from LeadIQ.
        Updates the existing row with new data from LeadIQ.
        """
        # Start with the existing row data
        result = row.copy()

        # Actualizamos solo los campos específicos de LeadIQ
        result.update({
            'source_platform': 'leadiq',
            'scrape_status': 'pending',
            'search_term': self.search_term_used
        })

        try:
            # Get company name and logo URL from logo image
            logo = document.find('img', {'alt': True, 'width': '76.747'})
            if logo:
                result['company_name'] = logo.get('alt')
                result['logo_url'] = logo.get('src')

            # Get company revenue range from highlight-right section
            highlight_right = document.find('div', {'class': 'highlight-right'})
            if highlight_right:
                revenue_span = highlight_right.find('span', {'class': 'start'})
                if revenue_span:
                    start_value = revenue_span.text.strip()
                    end_span = revenue_span.find_next_sibling('span', {'class': 'end'})
                    if end_span:
                        end_value = end_span.text.strip()
                        result['revenue_range'] = f"{start_value} - {end_value}"
                    else:
                        result['revenue_range'] = start_value

            # First find the highlight-left section that contains company info
            highlight_left = document.find('div', {'class': 'highlight-left'})
            if not highlight_left:
                self._logger.warning("Could not find highlight-left section")
                return idx, result

            # Then find the card span within highlight-left
            overview_section = highlight_left.find('div', {'class': 'card span'})
            if not overview_section:
                return idx, result

            # Extract information from dl/dt/dd elements
            dl_element = overview_section.find('dl')
            if dl_element:
                for item in dl_element.find_all('div', {'class': 'item'}):
                    dt = item.find('dt')
                    dd = item.find('dd')
                    if dt and dd:
                        field = dt.text.strip().lower()
                        value = dd.text.strip()

                        # Map fields to our column names
                        if field == 'headquarters':
                            address_info = self._parse_address(value)
                            result.update(address_info)
                            # Extract country from headquarters
                            parts = value.split()
                            result['country'] = parts[-1] if len(parts) > 1 else None
                        elif field == 'phone number':
                            phone = value.replace('****', '0000')
                            result['phone_number'] = phone
                        elif field == 'website':
                            website = dd.find('a')
                            result['website'] = website['href'] if website else value
                        elif field == 'stock symbol':
                            result['stock_symbol'] = value
                        elif field == 'naics code':
                            result['naics_code'] = value
                        elif field == 'employees':
                            result['employee_count'] = value
                        elif field == 'sic code':
                            result['sic_code'] = value

            # Extract information from the hero section
            hero_section = document.find('div', {'class': 'card hero snug'})
            if hero_section:
                # Company name
                company_name_element = hero_section.find('h1')
                if company_name_element:
                    result['company_name'] = company_name_element.text.strip()

                # Industry, location, and number of employees
                info_p = hero_section.find('p', {'class': 'info'})
                if info_p:
                    spans = info_p.find_all('span')
                    if len(spans) >= 3:
                        result['industry'] = spans[0].text.strip()
                        result['location'] = spans[1].text.strip()
                        result['number_employees'] = spans[2].text.strip()

                # Company description
                description_p = hero_section.find('pre')
                if description_p:
                    result['company_description'] = description_p.text.strip()

            # Extract similar companies
            similar_companies = []
            similar_section = document.find('div', {'id': 'similar'})
            if similar_section:
                for company in similar_section.find_all('li'):
                    company_link = company.find('a')
                    if not company_link:
                        continue

                    company_logo = company_link.find('img')
                    company_name = company_link.find('h3')

                    # Find revenue span
                    revenue_spans = company_link.find_all('span')
                    revenue_span = None
                    for span in revenue_spans:
                        if span.find('span', {'class': 'start'}):
                            revenue_span = span
                            break

                    if company_name:
                        similar_company = {
                            'name': company_name.text.strip(),  # No escapamos las comillas
                            'leadiq_url': company_link['href'],
                            'logo_url': company_logo['src'] if company_logo else None,
                        }

                        # Extract revenue range
                        if revenue_span:
                            start = revenue_span.find('span', {'class': 'start'})
                            end = revenue_span.find('span', {'class': 'end'})

                            if start:
                                start_value = start.text.strip()
                                if end:
                                    end_value = end.text.strip()
                                    similar_company['revenue_range'] = f"{start_value} - {end_value}"
                                else:
                                    similar_company['revenue_range'] = start_value

                        similar_companies.append(similar_company)

            if similar_companies:
                try:
                    result['similar_companies'] = json.dumps(
                        similar_companies,
                        ensure_ascii=False,
                        allow_nan=False,
                        separators=(',', ':')
                    )
                except Exception as e:
                    self._logger.error(
                        f"Error formatting similar companies JSON: {str(e)}"
                    )
                    result['similar_companies'] = None

            # Actualizamos el contador y el estado
            self._counter += 1

            # Verificamos si se encontró algún dato
            has_data = any([
                result.get('company_name'),
                result.get('logo_url'),
                result.get('address'),
                result.get('phone_number'),
                result.get('website'),
                result.get('stock_symbol'),
                result.get('naics_code'),
                result.get('employee_count'),
                result.get('revenue_range'),
                result.get('similar_companies')
            ])

            # Establecemos el estado según si encontramos datos o no
            result['scrape_status'] = 'success' if has_data else 'no_data'
            # Siempre devolvemos el resultado, tenga datos o no
            return idx, result

        except Exception as e:
            self._logger.error(f"Error parsing LeadIQ data: {str(e)}")
            result['scrape_status'] = f'error: {str(e)[:50]}'
            return idx, result
