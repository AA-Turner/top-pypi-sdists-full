import re
from typing import Dict, Any, Optional, List
from bs4 import BeautifulSoup
from .base import ParserBase

class BrotherParser(ParserBase):
    """
    Parser for Brother product information.
    
    Extracts product details from Brother's USA website using Selenium.
    """
    domain = "brother-usa.com"
    search_format = "site:brother-usa.com {}"
    product_url_pattern = "brother-usa.com/products/"
    
    async def parse(self, url: str, search_term: str, retailer: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse product information from a Brother URL using Selenium.
        
        Args:
            url: Brother product URL
            search_term: Original search term
            retailer: Optional retailer information (not used for Brother)
            
        Returns:
            Dictionary with product information
        """
        result = {
            "source_url": url,
            "search_term": search_term,
            "model_code": None,
            "product_name": None,
            "price": None,
            "specs": None,
            "images": None,
            "parse_status": "pending"
        }
        
        try:
            self.headless = True
            driver = await self.get_driver()
            await self.get_page(url)
            
            page_content = driver.page_source
            soup = BeautifulSoup(page_content, "html.parser")
            
            # Extract model code - usando el selector exacto de la captura
            model_elem = soup.select_one("h1.janus-model-number")
            if model_elem:
                result["model_code"] = model_elem.text.strip()
            
            # Extract product name - usando el selector exacto de la captura
            name_elem = soup.select_one("h2.janus-product-title")
            if name_elem:
                result["product_name"] = name_elem.text.strip()
            
            # Extract price (ajustar según el sitio real)
            price_elem = soup.select_one("span.price")  # Ajustar según el sitio real
            if price_elem:
                result["price"] = price_elem.text.strip()
            
            # Extract image (ajustar según el sitio real)
            main_img = soup.select_one("img.product-image")  # Ajustar según el sitio real
            if main_img:
                src = main_img.get("src")
                if src:
                    if not src.startswith(("http://", "https://")):
                        src = f"https://{self.domain}{src}" if src.startswith("/") else f"https://{self.domain}/{src}"
                    result["images"] = [src]
            
            result["parse_status"] = "success"
            
        except Exception as e:
            self._logger.error(f"Error parsing Brother product: {str(e)}")
            result["parse_status"] = f"error: {str(e)}"
        finally:
            self.close_driver()
            
        return result

    def get_product_urls(self, search_results: List[Dict[str, str]], max_urls: int = 5) -> List[str]:
        """
        Extract relevant product URLs from search results.
        
        Args:
            search_results: List of search result dictionaries
            max_urls: Maximum number of URLs to return
            
        Returns:
            List of product URLs that match the Brother product pattern
        """
        urls = []
        for result in search_results[:max_urls]:
            url = result.get('link') or result.get('href') or result.get('url')
            if url and self.domain in url and self.product_url_pattern in url:
                urls.append(url)
        return urls 