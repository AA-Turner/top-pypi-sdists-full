import re
from typing import Dict, Any, Optional
import httpx
from bs4 import BeautifulSoup
from .base import ParserBase

class EpsonParser(ParserBase):
    """
    Parser for Epson product information.
    
    Extracts product details from Epson's website.
    """
    domain = "epson.com"
    search_format = "site:epson.com {} product"
    model_pattern = r"^.*\/\b[p|s]\/([^?]+)"
    
    def extract_model_code(self, url: str) -> Optional[str]:
        """
        Extract model code from URL using the regex pattern and clean it.
        
        Args:
            url: URL to extract model code from
            
        Returns:
            Cleaned model code or None if not found
        """
        match = re.search(self.model_pattern, url)
        if match and match.group(1):
            # Extraer el código
            model_code = match.group(1)
            
            # Limpiar el prefijo SPT_ si existe
            if model_code.startswith("SPT_"):
                model_code = model_code.replace("SPT_", "", 1)
                
            return model_code
        return None
    
    async def parse(self, url: str, search_term: str, retailer: str = None) -> Dict[str, Any]:
        """
        Parse product information from an Epson URL.
        
        Args:
            url: Epson product URL
            search_term: Original search term
            retailer: Optional retailer information
            
        Returns:
            Dictionary with product information
        """
        result = {
            "source_url": url,
            "search_term": search_term,
            "model_code": self.extract_model_code(url),
            "product_name": None,
            "price": None,
            "description": None,
            "specs": None,
            "images": None,
            "parse_status": "pending"
        }
        
        try:
            # Get the page content
            response = await self._get(url, headers=self.headers, use_proxy=True)
            if not response or response.status_code != 200:
                result["parse_status"] = f"error: HTTP {response.status_code if response else 'no response'}"
                return result
                
            # Parse the HTML
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract product name
            product_name_elem = soup.select_one("h1.product-name, h1.product-title")
            if product_name_elem:
                result["product_name"] = product_name_elem.text.strip()
            
            # Extract price
            price_elem = soup.select_one("span.price, div.product-price")
            if price_elem:
                result["price"] = price_elem.text.strip()
            
            # Extract description
            desc_elem = soup.select_one("div.product-description, div.product-overview")
            if desc_elem:
                result["description"] = desc_elem.text.strip()
            
            # Extract specifications
            specs = {}
            specs_section = soup.select_one("div.product-specifications, div.tech-specs")
            if specs_section:
                for row in specs_section.select("tr, div.spec-row"):
                    label = row.select_one("th, .spec-label")
                    value = row.select_one("td, .spec-value")
                    if label and value:
                        specs[label.text.strip()] = value.text.strip()
                result["specs"] = specs
            
            # Extract images
            image_urls = []
            for img in soup.select("div.product-gallery img, img.product-image"):
                src = img.get("src") or img.get("data-src")
                if src:
                    if not src.startswith(("http://", "https://")):
                        src = f"https://{self.domain}{src}" if src.startswith("/") else f"https://{self.domain}/{src}"
                    image_urls.append(src)
            if image_urls:
                result["images"] = image_urls
            
            result["parse_status"] = "success"
            
        except httpx.RequestError as e:
            result["parse_status"] = f"error: request failed - {str(e)}"
        except Exception as e:
            self._logger.error(f"Error parsing Epson product: {str(e)}")
            result["parse_status"] = f"error: {str(e)}"
            
        return result 