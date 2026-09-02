import re
from typing import Dict, Any, Optional, List
from bs4 import BeautifulSoup
from .base import ParserBase

class CanonParser(ParserBase):
    """
    Parser for Canon product information.
    
    Extracts product details from Canon's USA and Canada websites using Selenium.
    """
    domain_us = "usa.canon.com"
    domain_ca = "canon.ca"
    product_url_pattern_us = "usa.canon.com/shop/p/"
    product_url_pattern_ca = "canon.ca/en/product"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.region = "us"  # Default region
        self.retailer = None  # Store retailer info
        
    def determine_region(self, retailer: Optional[str]) -> str:
        """
        Determine region based on retailer information.
        
        Args:
            retailer: Retailer string that may contain region information
            
        Returns:
            'ca' for Canada, 'us' for United States (default)
        """
        if retailer:
            retailer_lower = retailer.lower()
            if 'canada' in retailer_lower:
                return 'ca'
            elif 'us' in retailer_lower:
                return 'us'
        return 'us'  # Default to US if no region found
        
    def create_search_query(self, term: str) -> str:
        """
        Create region-specific search query.
        
        Args:
            term: Search term (typically product model)
            
        Returns:
            Formatted search query for the appropriate region
        """
        # Determine region based on stored retailer info
        self.region = self.determine_region(self.retailer)
        domain = self.domain_ca if self.region == 'ca' else self.domain_us
        return f"site:{domain} {term}"
    
    async def parse(self, url: str, search_term: str, retailer: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse product information from a Canon URL using Selenium.
        
        Args:
            url: Canon product URL
            search_term: Original search term
            retailer: Optional retailer information to determine region
            
        Returns:
            Dictionary with product information
        """
        self.retailer = retailer  # Store retailer info for use in other methods
        self.region = self.determine_region(retailer)
        
        result = {
            "source_url": url,
            "search_term": search_term,
            "model_code": None,
            "product_name": None,
            "price": None,
            "specs": None,
            "images": None,
            "parse_status": "pending",
            "region": self.region
        }
        
        try:
            self.headless = True
            driver = await self.get_driver()
            await self.get_page(url)
            
            page_content = driver.page_source
            soup = BeautifulSoup(page_content, "html.parser")
            
            if self.region == 'ca':
                # Selectores para el sitio de Canadá
                # Extract model code - usando un selector más robusto
                model_elem = soup.select_one("p[class*='ItemCode']")  # Busca cualquier p que contenga 'ItemCode' en su clase
                if not model_elem:
                    # Alternativa: buscar por el texto "Item Code" y navegar a su contenido
                    model_elems = soup.find_all(string=lambda text: text and "Item Code" in text)
                    if model_elems:
                        # Encontrar el elemento padre y extraer el texto completo
                        model_elem = model_elems[0].parent
                
                if model_elem:
                    # Obtener el texto y limpiarlo
                    model_text = model_elem.text.strip()
                    # Eliminar "Item Code:" y cualquier espacio extra
                    model_text = model_text.replace("Item Code: ", "").strip()
                    result["model_code"] = model_text
                
                # Extract product name
                name_elem = soup.select_one("h1.ProductName")  # Ajustar según el sitio real
                if name_elem:
                    result["product_name"] = name_elem.text.strip()
                
            else:
                # Selectores para el sitio de USA
                product_name_elem = soup.select_one("span.base[data-ui-id='page-title-wrapper'][itemprop='name']")
                if product_name_elem:
                    result["product_name"] = product_name_elem.text.strip()
                
                sku_elem = soup.select_one("div.value[itemprop='sku']")
                if sku_elem:
                    result["model_code"] = sku_elem.text.strip()
            
            # Extract price (común para ambos sitios, ajustar si es necesario)
            price_elem = soup.select_one("[data-price-type='finalPrice'] .price")
            if price_elem:
                result["price"] = price_elem.text.strip()
            
            # Extract image (común para ambos sitios, ajustar si es necesario)
            main_img = soup.select_one("img[data-role='product-image']")
            if main_img:
                src = main_img.get("src")
                if src:
                    domain = self.domain_ca if self.region == 'ca' else self.domain_us
                    if not src.startswith(("http://", "https://")):
                        src = f"https://{domain}{src}" if src.startswith("/") else f"https://{domain}/{src}"
                    result["images"] = [src]
            
            result["parse_status"] = "success"
            
        except Exception as e:
            self._logger.error(f"Error parsing Canon product: {str(e)}")
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
            List of product URLs that match the Canon product pattern
        """
        urls = []
        pattern = self.product_url_pattern_ca if self.region == 'ca' else self.product_url_pattern_us
        domain = self.domain_ca if self.region == 'ca' else self.domain_us
        
        for result in search_results[:max_urls]:
            url = result.get('link') or result.get('href') or result.get('url')
            if url and domain in url and pattern in url:
                urls.append(url)
        return urls 