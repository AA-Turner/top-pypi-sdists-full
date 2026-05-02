from abc import abstractmethod
import re
import logging
from typing import Dict, Any, Optional, List
from bs4 import BeautifulSoup
from ....interfaces import HTTPService, SeleniumService

class ParserBase(HTTPService, SeleniumService):
    """
    Base class for product information parsers.
    
    Defines the interface and common functionality for all product parsers.
    """
    domain: str
    search_format: str
    model_pattern: Optional[str] = None  # Hacemos que sea opcional con valor predeterminado None
    
    def __init__(self, *args, **kwargs):
        self.cookies = kwargs.get('cookies', None)
        self._logger = logging.getLogger(self.__class__.__name__)
        super().__init__(*args, **kwargs)
    
    @abstractmethod
    async def parse(self, url: str, search_term: str) -> Dict[str, Any]:
        """
        Parse product information from a URL.
        
        Args:
            url: URL to parse
            search_term: Original search term
            
        Returns:
            Dictionary with extracted product information
        """
        pass
    
    def create_search_query(self, term: str) -> str:
        """
        Create a search query for the given term.
        
        Args:
            term: Search term (typically product model)
            
        Returns:
            Formatted search query
        """
        return self.search_format.format(term)
    
    def extract_model_code(self, url: str) -> Optional[str]:
        """
        Extract model code from URL using the regex pattern if defined.
        
        Args:
            url: URL to extract model code from
            
        Returns:
            Extracted model code or None if not found or pattern not defined
        """
        if not hasattr(self, 'model_pattern') or self.model_pattern is None:
            return None  # Si no hay patrón definido, devolvemos None
            
        match = re.search(self.model_pattern, url)
        if match and match.group(1):
            return match.group(1)
        return None
    
    def get_product_urls(self, search_results: List[Dict[str, str]], max_urls: int = 5) -> List[str]:
        """
        Extract relevant product URLs from search results.
        
        Args:
            search_results: List of search result dictionaries
            max_urls: Maximum number of URLs to return
            
        Returns:
            List of product URLs
        """
        urls = []
        for result in search_results[:max_urls]:
            url = result.get('link') or result.get('href') or result.get('url')
            if url and self.domain in url:
                urls.append(url)
        return urls 