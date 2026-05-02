from typing import Any, List, Dict
from bs4 import BeautifulSoup as bs
from abc import abstractmethod
from ....interfaces import SeleniumService, HTTPService
import re
import logging

class ScrapperBase(SeleniumService, HTTPService):
    """
    ScrapperBase Model.


    Define how scrappers should be work.-
    """
    domain: str
    search_term: str
    cookies: Any
    keywords: List[str]

    def __init__(self, *args, **kwargs):
        self.cookies = kwargs.get('cookies', None)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._counter: int = 0
        self.search_term_used: str = ''
        super().__init__(*args, **kwargs)

    @abstractmethod
    async def scrapping(self, document: bs, idx: int, row: dict):
        pass

    @abstractmethod
    def define_search_term(self, term: str):
        pass

    async def get(self, url, headers: dict):
        return await self._get(url, headers=headers, use_proxy=True)

    def _parse_address(self, address: str) -> Dict[str, str]:
        """
        Parse address string to extract state, zipcode and country.

        Args:
            address (str): Raw address string

        Returns:
            Dict with parsed address components:
            {
                'address': str,
                'state': str,
                'zipcode': str,
                'country': str
            }
        """
        if not address:
            return {
                'address': None,
                'state': None,
                'zipcode': None,
                'country': None
            }

        # Mantener la dirección original
        result = {'address': address}

        # Primera regex para formato completo
        pattern1 = r'^.*,\s+([^,]+?)\s+([\w\s-]+)\s+([A-Z]{2})$'
        # Segunda regex como fallback
        pattern2 = r'^.*,\s*([^,]+?),\s+([\w\s-]+?)\s*([A-Z]{2})'

        try:
            # Intentar con la primera regex
            match = re.search(pattern1, address)
            if not match:
                # Si no hay match, intentar con la segunda
                match = re.search(pattern2, address)

            if match:
                result['state'] = match.group(1).strip()
                result['zipcode'] = match.group(2).strip()
                result['country'] = match.group(3).strip()
            else:
                self._logger.warning(f"Could not parse address: {address}")
                result.update({
                    'state': None,
                    'zipcode': None,
                    'country': None
                })
        except Exception as e:
            self._logger.error(f"Error parsing address {address}: {str(e)}")
            result.update({
                'state': None,
                'zipcode': None,
                'country': None
            })

        return result

    def _standardize_name(self, text: str) -> str:
        """Estandariza el formato del texto: lowercase y guiones en lugar de espacios."""
        # Primero limpiamos caracteres especiales y espacios extras
        cleaned = text.strip().lower().replace(' ', '-')
        return f"\'{cleaned}\'"
