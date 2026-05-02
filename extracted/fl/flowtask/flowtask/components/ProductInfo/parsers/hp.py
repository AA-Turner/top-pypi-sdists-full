import re
import asyncio
from typing import Dict, Any, Optional, List
import httpx
from bs4 import BeautifulSoup
from .base import ParserBase

class HPParser(ParserBase):
    """
    Parser for HP product information.
    
    Extracts product details from HP's website using Selenium for dynamic content.
    """
    domain = "hp.com"
    search_format = "site:hp.com {}"  # Sin la palabra 'product' como en Epson
    product_url_pattern = "hp.com/us-en/shop/pdp/"  # Patrón para URLs de producto válidas
    
    async def parse(self, url: str, search_term: str, retailer: str = None) -> Dict[str, Any]:
        """
        Parse product information from an HP URL using Selenium.
        
        Args:
            url: HP product URL
            search_term: Original search term
            
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
            # Utilizamos Selenium ya que la página de HP tiene contenido dinámico
            driver = await self.get_driver()
            await self.get_page(url)
            
            # Ejecutamos un scroll para cargar todo el contenido
            self._execute_scroll(scroll_pause_time=1.5, max_scrolls=5)
            
            # Extraer contenido de la página
            page_content = driver.page_source
            soup = BeautifulSoup(page_content, "html.parser")
            
            # 1. Extract product name - usando el selector exacto de la captura
            product_name_elem = soup.select_one("h1[data-test-hook='@hpstellar/core/typography']")
            if product_name_elem:
                result["product_name"] = product_name_elem.text.strip()
            
            # 2. Extract price - directamente desde el atributo data-widget-item-price
            price_attr_elem = soup.select_one("[data-widget-item-price]")
            if price_attr_elem:
                price_value = price_attr_elem.get("data-widget-item-price")
                if price_value:
                    result["price"] = f"${price_value}"
            # Si no se encuentra con el atributo, intentar con el selector de la captura
            elif not result["price"]:
                price_elem = soup.select_one("span[data-test-hook='@hpstellar/core/typography'][class*='sale-subscription-price']")
                if price_elem:
                    result["price"] = price_elem.text.strip()
                      
            # 4. Extract model code - directamente desde el atributo data-widget-item-sku
            sku_elem = soup.select_one("[data-widget-item-sku]")
            if sku_elem:
                result["model_code"] = sku_elem.get("data-widget-item-sku")
            
            # Si no se encontró el código en el atributo, intentar con span.sku
            if not result["model_code"]:
                model_elem = soup.select_one("span.sku")
                if model_elem:
                    text = model_elem.text.strip()
                    # Eliminar el prefijo "Product #" si está presente
                    if "Product #" in text:
                        result["model_code"] = text.replace("Product # ", "").strip()
                    else:
                        result["model_code"] = text
            
            # 5. Extract SINGLE product image - usando el selector exacto de la captura
            # Intentar primero con el botón específico
            main_img = soup.select_one("button[data-gtm-category='linkClick'][data-gtm-id='gallery'] img")
            
            # Si no encuentra con ese selector, probar con el otro selector visible en las capturas
            if not main_img:
                main_img = soup.select_one("[data-test-hook='@hpstellar/core/image-with-placeholder'] img")
            
            if main_img:
                src = main_img.get("src") or main_img.get("data-src")
                if src:
                    # Asegurar que la URL sea absoluta
                    if not src.startswith(("http://", "https://")):
                        src = f"https://{self.domain}{src}" if src.startswith("/") else f"https://{self.domain}/{src}"
                    result["images"] = [src]  # Guardamos una sola imagen como lista
            
            result["parse_status"] = "success"
            
        except httpx.RequestError as e:
            result["parse_status"] = f"error: request failed - {str(e)}"
        except Exception as e:
            self._logger.error(f"Error parsing HP product: {str(e)}")
            result["parse_status"] = f"error: {str(e)}"
        finally:
            # Asegurar que cerramos el driver
            self.close_driver()
            
        return result 

    def get_product_urls(self, search_results: List[Dict[str, str]], max_urls: int = 5) -> List[str]:
        """
        Extract relevant product URLs from search results.
        
        Args:
            search_results: List of search result dictionaries
            max_urls: Maximum number of URLs to return
            
        Returns:
            List of product URLs that match the HP product pattern
        """
        urls = []
        for result in search_results[:max_urls]:
            url = result.get('link') or result.get('href') or result.get('url')
            # Verificar que la URL sea de una página de producto de HP
            if url and self.domain in url and self.product_url_pattern in url:
                urls.append(url)
        return urls 