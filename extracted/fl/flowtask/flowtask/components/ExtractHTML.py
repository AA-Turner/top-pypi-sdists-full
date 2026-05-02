

import asyncio
from datetime import datetime
from typing import Optional
from collections.abc import Callable
from bs4 import BeautifulSoup
from lxml import etree
from .flow import FlowComponent
from ..interfaces.dataframes import PandasDataframe


class ExtractHTML(FlowComponent, PandasDataframe):
    """
    ExtractHTML

        Overview:
        Extract HTML using XPATH or BS CSS Selectors.



        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          ExtractHTML:
          custom_parser: trustpilot_reviews
          as_dataframe: true
        ```
    """
    _version = "1.0.0"
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self._xpath: Optional[str] = kwargs.get('xpath', None)
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        if self.previous:
            self._input = self.input

        if not self._input:
            raise ValueError("No input provided.")

        if not isinstance(self._input, dict):
            raise TypeError("Input must be a dictionary.")

    async def close(self):
        pass

    def get_soup(self, content: str, parser: str = 'html.parser'):
        """Get a BeautifulSoup Object."""
        return BeautifulSoup(content, parser)

    def trustpilot_reviews(self, xml_obj, **kwargs):
        xpath = '//article[@data-service-review-card-paper="true"]'
        # Extract using XPATH
        elements = xml_obj.xpath(xpath)
        results = []
        date_formats = [
            "%b. %d, %Y",
            "%B %d, %Y",
            "%b %d, %Y",
        ]
        for el in elements:
            soup = self.get_soup(etree.tostring(el))
            # Extract using BS CSS Selectors
            consumer_profile = soup.find('a', {"name": "consumer-profile"})
            username = consumer_profile.find('span').get_text(strip=True)
            user_url = consumer_profile.get('href')
            rating_div = soup.find('div', {"data-service-review-rating": True})
            # Extract title
            title_h2 = soup.find("h2", {"data-service-review-title-typography": "true"})
            review_title = title_h2.get_text(strip=True) if title_h2 else None
            rating = rating_div.get('data-service-review-rating')
            review_body = soup.find('p', {"data-service-review-text-typography": "true"})
            review = review_body.get_text(strip=True) if review_body else None
            review_date_p = soup.find('p', {"data-service-review-date-of-experience-typography": "true"})
            review_date_str = review_date_p.get_text(strip=True) if review_date_p else None
            review_date = None
            if review_date_str:
                if ":" in review_date_str:
                    review_date_str = review_date_str.split(":", 1)[1].strip()
                for date_format in date_formats:
                    try:
                        review_date = datetime.strptime(review_date_str, date_format)
                        break 
                    except ValueError:
                        continue

                if not review_date:
                    print(f"Error to convert the date '{review_date_str}'")
            if not review:
                continue
            results.append(
                {
                    "origin": "trustpilot",
                    "username": username,
                    #"user_url": user_url,
                    "review_date": review_date,
                    "rating": rating,
                    #"title": review_title,
                    "review": review
                }
            )
        return results

    def consumeraffairs_reviews(self, xml_obj, **kwargs):
        xpath = '//div[@id="reviews-container"]//div[@itemprop="reviews"]'
        elements = xml_obj.xpath(xpath)
        results = []
        date_formats = [
            "%b. %d, %Y",
            "%B %d, %Y",
            "%b %d, %Y",
        ]
        for el in elements:
            soup = self.get_soup(etree.tostring(el))
            consumer_profile = soup.find('span', class_='rvw__inf-nm')
            username = consumer_profile.get_text(strip=True) if consumer_profile else None
            rating_div = soup.find('div', class_='rvw__hdr-stat')
            rating_meta = rating_div.find('meta', itemprop='ratingValue') if rating_div else None
            rating = rating_meta.get('content') if rating_meta else None
            review_body_tag = soup.find('div', class_='rvw__top-text')
            review = review_body_tag.get_text(strip=True) if review_body_tag else None
            date_tag = soup.find('p', class_='rvw__rvd-dt')
            review_date_str = date_tag.get_text(strip=True).replace("Reviewed ", "") if date_tag else None

            review_date = None
            if review_date_str:
                review_date_str = review_date_str.replace("Reviewed ", "").replace("Updated review: ", "").replace("Original Review: ", "")
                review_date_str = review_date_str.replace("Sept.", "Sep.")
                for date_format in date_formats:
                    try:
                        review_date = datetime.strptime(review_date_str, date_format)
                        break
                    except ValueError:
                        continue

                if not review_date:
                    print(f"Error to convert the date '{review_date_str}'")

            if not review:
                continue
            results.append(
                {
                    "origin": "consumeraffairs",
                    "username": username,
                    "review_date": review_date,
                    "rating": rating,
                    "review": review
                }
            )
        return results

    async def run(self):
        results = []
        parser = None
        if hasattr(self, 'custom_parser'):
            parser = getattr(self, self.custom_parser, None)
        for filename, result in self._input.items():
            html_obj = result.get('html', None)
            if html_obj is None:
                raise ValueError("No HTML object found.")
            if parser:
                results += parser(html_obj)
            else:
                # Extract using BS CSS Selectors
                pass
        if getattr(self, 'as_dataframe', False) is True:
            df = await self.create_dataframe(results)
            self._result = df
        else:
            self._result = results
        return self._result
