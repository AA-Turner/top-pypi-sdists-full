from .base import ProductCompetitorsBase


class BestBuyScrapper(ProductCompetitorsBase):
    domain: str = 'bestbuy.com'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headless = False

    async def product_information(self, response: object, idx: int, row: dict) -> tuple:
        """Get the product information from BestBuy."""
        try:
            document = self.get_bs(response)
            competitors_found = {}

            # Inicializar valores vacíos para todos los competidores
            for competitor in self.competitors:
                self.set_empty_values(row, competitor)

            # Find all product cards in the carousel
            carousel = document.find('ul', {'class': 'c-carousel-list'})
            if carousel:
                for product in carousel.find_all('li', {'class': 'product-carousel-v2_brix-item'}):
                    try:
                        # Extract product info
                        product_link = product.find('a', {'data-testid': 'product-link'})
                        if not product_link:
                            continue

                        # Get product name and brand
                        title_div = product_link.find('div', {'class': 'title-block__title'})
                        if not title_div:
                            continue
                        
                        full_name = title_div.text.strip()
                        brand = full_name.split(' - ')[0] if ' - ' in full_name else ''

                        # Check if this brand is in our competitors list and we haven't found it yet
                        if brand not in self.competitors or brand in competitors_found:
                            continue

                        # Get product URL and SKU
                        url = f"https://www.bestbuy.com{product_link.get('href')}"
                        sku = product_link.get('data-cy', '').replace('product-link-', '')

                        # Get price
                        price_div = product.find('div', {'class': 'priceView-hero-price'})
                        price = price_div.text.strip() if price_div else None

                        # Get rating and reviews
                        rating_p = product.find('p', {'class': 'visually-hidden'})
                        rating = None
                        num_reviews = None
                        if rating_p:
                            rating_text = rating_p.text
                            try:
                                rating = rating_text.split('rating,')[1].split('out')[0].strip() if 'rating,' in rating_text else None
                                num_reviews = rating_text.split('with')[1].split('reviews')[0].strip() if 'with' in rating_text else None
                            except (IndexError, AttributeError):
                                pass

                        # Store competitor info
                        row.update({
                            f'competitor_brand_{brand}': brand,
                            f'competitor_name_{brand}': full_name,
                            f'competitor_url_{brand}': url,
                            f'competitor_sku_{brand}': sku,
                            f'competitor_price_{brand}': price,
                            f'competitor_rating_{brand}': rating,
                            f'competitor_reviews_{brand}': num_reviews
                        })
                        competitors_found[brand] = True

                        # Si ya encontramos todos los competidores, podemos salir
                        if len(competitors_found) == len(self.competitors):
                            break
                    except Exception as err:
                        self._logger.warning(f'Error processing product in carousel: {err}')
                        continue

            return idx, row
        except Exception as err:
            self._logger.error(f'Error getting product information from BestBuy: {err}')
            return idx, row 