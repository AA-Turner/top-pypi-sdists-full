from .base import ProductCompetitorsBase


class LowesScrapper(ProductCompetitorsBase):
    domain: str = 'lowes.com'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expected_columns = [
            'price',
            'availability',
            'product_name',
            'product_description',
            'product_id'
        ]
        self.headless = False

    async def connect(self):
        """Creates the Driver and Connects to the Site."""
        self._driver = await self.get_driver()
        await self.start()

    async def disconnect(self):
        """Disconnects the Driver and closes the Connection."""
        if self._driver:
            self.close_driver()

    async def product_information(self, response: object, idx: int, row: dict) -> tuple:
        """Get the product information from Lowes."""
        try:
            document = self.get_bs(response)
            competitors_found = {}

            # Inicializar valores vacíos para todos los competidores
            for competitor in self.competitors:
                self.set_empty_values(row, competitor)

            # Find all product cards in the carousel
            carousel = document.find('div', {'class': 'carousel-inner-container'})
            if carousel:
                for product in carousel.find_all('div', {'class': 'product-card-wrapper'}):
                    try:
                        # Extract product info
                        product_link = product.find('a', {'class': 'carousel-container'})
                        if not product_link:
                            continue

                        # Get product name and brand
                        title_div = product_link.find('span', {'class': 'brand-name'})
                        if not title_div:
                            continue
                        
                        brand = title_div.text.strip()
                        full_name = title_div.find_next('span', {'class': 'product-desc'}).text.strip()

                        # Check if this brand is in our competitors list and we haven't found it yet
                        if brand not in self.competitors or brand in competitors_found:
                            continue

                        # Get product URL and SKU
                        url = f"https://www.lowes.com{product_link.get('href')}"
                        sku = product_link.get('data-productid', '')

                        # Get price
                        price_div = product.find('span', {'class': 'final-price'})
                        price = price_div.text.strip() if price_div else None

                        # Get rating and reviews
                        rating_div = product.find('span', {'class': 'rating'})
                        rating = None
                        num_reviews = None
                        if rating_div:
                            try:
                                rating = rating_div.get('aria-label', '').split(' ')[0]
                                reviews_span = product.find('span', {'class': 'rating-count'})
                                num_reviews = reviews_span.text.strip() if reviews_span else None
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
            self._logger.error(f'Error getting product information from Lowes: {err}')
            return idx, row 