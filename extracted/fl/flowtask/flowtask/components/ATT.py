"""
AT&T Prepaid Product Scraper Component.

This component scrapes product data from the AT&T Prepaid phones listing page
using Selenium for browser automation and JSON-LD structured data extraction.

Exposed Classes:
    - ATT: The main AT&T scraper component.
"""
import asyncio
import json
import re
import random
from typing import Any, Optional
from collections.abc import Callable

from bs4 import BeautifulSoup
import pandas as pd
from navconfig.logging import logging

from ..exceptions import (
    ComponentError,
    DataNotFound,
    ConfigError,
)
from ..interfaces.flow import FlowComponent
from ..interfaces import SeleniumService
from ..interfaces.http import ua


logging.getLogger(name='selenium.webdriver').setLevel(logging.WARNING)
logging.getLogger(name='WDM').setLevel(logging.WARNING)

# Base URL for AT&T Prepaid phones listing page
ATT_PREPAID_LISTING_URL = "https://www.att.com/buy/prepaid-phones/"
ATT_PREPAID_PLANS_URL = "https://www.att.com/prepaid/plans/"
ATT_BASE_URL = "https://www.att.com"

# Desktop User-Agents for scraping
DESKTOP_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) "
    "Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
]


class ATT(FlowComponent, SeleniumService):
    """
    AT&T Prepaid Product Scraper.

    Scrapes product data from the AT&T Prepaid phones listing page using
    Selenium for browser automation and JSON-LD for structured data extraction.

    Supports two input modes:
        - **With previous DataFrame**: Iterates over rows containing product
          URLs or SKUs, enriching each row with scraped data.
        - **Standalone**: Scrapes the full listing page to discover all
          available prepaid phones, then visits each product detail page.

    **Configuration**

    | Parameter | Required | Description |
    |---|---|---|
    | type | Yes | Function to execute (e.g., ``product_info``) |
    | max_concurrent | No | Max concurrent Selenium tasks (default: 3) |
    | delay | No | Delay between requests in seconds (default: 2.0) |

    **Example**

    ```yaml
    steps:
      - ATT:
          type: product_info
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
        self._fn: str = kwargs.pop('type', None)
        self.max_concurrent: int = kwargs.get('max_concurrent', 3)
        self.delay: float = kwargs.get('delay', 2.0)
        if not self._fn:
            raise ConfigError(
                "ATT: require a `type` function to be called, "
                "e.g., type: product_info"
            )
        super(ATT, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs,
        )
        self.semaphore = asyncio.Semaphore(self.max_concurrent)

    async def start(self, **kwargs) -> bool:
        """Initialize the component and validate configuration.

        If a previous component provided data, loads it as a DataFrame.
        Validates that the requested ``type`` function exists.
        """
        await super(ATT, self).start(**kwargs)
        if self.previous:
            self.data = self.input
            if not isinstance(self.data, pd.DataFrame):
                raise ComponentError(
                    "ATT: Incompatible input — expected a Pandas DataFrame."
                )
            self._logger.info(
                f"ATT: Received DataFrame with {len(self.data)} rows "
                f"from previous component."
            )
        if not hasattr(self, self._fn):
            raise ConfigError(
                f"ATT: Function '{self._fn}' not found in ATT component."
            )

    async def close(self, **kwargs) -> bool:
        """Close the Selenium driver."""
        self.close_driver()
        return True

    # ------------------------------------------------------------------
    # JSON-LD Extraction Helpers
    # ------------------------------------------------------------------

    def _extract_json_ld_product(self, page_source: str) -> Optional[dict]:
        """Extract the Product JSON-LD object from page source.

        Args:
            page_source: Raw HTML page source string.

        Returns:
            The parsed Product JSON-LD dict, or None if not found.
        """
        soup = BeautifulSoup(page_source, 'html.parser')
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                raw = script.string or script.get_text(strip=True)
                if not raw:
                    continue
                data = json.loads(raw)
            except (json.JSONDecodeError, Exception):
                continue

            # JSON-LD can be a single object or a list
            candidates = data if isinstance(data, list) else [data]
            for item in candidates:
                if not isinstance(item, dict):
                    continue
                # Check for Product type (could be nested in @graph)
                if item.get('@type') == 'Product':
                    return item
                # Check @graph array
                graph = item.get('@graph', [])
                for node in graph:
                    if isinstance(node, dict) and node.get('@type') == 'Product':
                        return node
        return None

    def _parse_product_json_ld(self, product: dict, url: str) -> dict:
        """Parse a Product JSON-LD object into a flat dictionary.

        Args:
            product: The JSON-LD Product dict.
            url: The product page URL.

        Returns:
            A flat dictionary with standardized product fields.
        """
        # Name
        name = product.get('name', '')

        # Brand
        brand_obj = product.get('brand', {})
        if isinstance(brand_obj, dict):
            brand = brand_obj.get('name', '')
        else:
            brand = str(brand_obj)

        # SKU
        sku = product.get('sku', '')

        # Description
        description = product.get('description', '')

        # Images
        images = product.get('image', [])
        if isinstance(images, str):
            images = [images]
        image_url = images[0] if images else None

        # Price — from offers
        price = None
        offers = product.get('offers', {})
        if isinstance(offers, list):
            # Take the first offer
            offers = offers[0] if offers else {}
        if isinstance(offers, dict):
            price_val = offers.get('price')
            if price_val is not None:
                try:
                    price = float(price_val)
                except (ValueError, TypeError):
                    pass

        # Rating & Reviews
        avg_rating = None
        num_reviews = None
        aggregate = product.get('aggregateRating', {})
        if isinstance(aggregate, dict):
            rv = aggregate.get('ratingValue')
            rc = aggregate.get('reviewCount') or aggregate.get('ratingCount')
            if rv is not None:
                try:
                    avg_rating = float(str(rv).replace(',', '.'))
                except (ValueError, TypeError):
                    pass
            if rc is not None:
                try:
                    num_reviews = int(str(rc).replace(',', ''))
                except (ValueError, TypeError):
                    pass

        # Specifications — from additionalProperty
        specifications = {}
        for prop in product.get('additionalProperty', []):
            if isinstance(prop, dict):
                prop_name = prop.get('name', '')
                prop_value = prop.get('value', '')
                if prop_name:
                    specifications[prop_name] = prop_value

        return {
            'sku': sku,
            'brand': brand,
            'product_name': name,
            'image_url': image_url,
            'images': json.dumps(images, ensure_ascii=False),
            'price': price,
            'url': url,
            'specifications': json.dumps(
                specifications, ensure_ascii=False
            ),
            'product_description': description,
            'num_reviews': num_reviews,
            'avg_rating': avg_rating,
        }

    # ------------------------------------------------------------------
    # Listing Page Scraping
    # ------------------------------------------------------------------

    async def _scrape_listing(self) -> list[dict]:
        """Scrape the AT&T Prepaid listing page to get all device URLs.

        Navigates to the listing page and extracts device data from the
        ``window.__NEXT_DATA__`` JavaScript object embedded in the page.

        Returns:
            A list of dicts with basic device info (name, url, price, etc.).
        """
        self._logger.info(
            f"ATT: Navigating to listing page: {ATT_PREPAID_LISTING_URL}"
        )
        await self.get_page(ATT_PREPAID_LISTING_URL)
        await asyncio.sleep(3)

        # Extract __NEXT_DATA__ via JavaScript
        try:
            next_data_raw = self._driver.execute_script(
                "return JSON.stringify("
                "window.__NEXT_DATA__?.props?.pageProps?.devices?.items "
                "|| window.__NEXT_DATA__?.props?.initialReduxState?.devices?.items "
                "|| []"
                ");"
            )
            devices = json.loads(next_data_raw) if next_data_raw else []
        except Exception as exc:
            self._logger.warning(
                f"ATT: Could not extract __NEXT_DATA__: {exc}. "
                "Falling back to DOM parsing."
            )
            devices = []

        if not devices:
            # Fallback: parse links from the DOM
            self._logger.info("ATT: Falling back to DOM link extraction.")
            soup = BeautifulSoup(
                self._driver.page_source, 'html.parser'
            )
            links = soup.find_all(
                'a', href=re.compile(r'/buy/prepaid-phones/.*\.html')
            )
            seen = set()
            for link in links:
                href = link.get('href', '')
                full_url = (
                    f"{ATT_BASE_URL}{href}"
                    if href.startswith('/') else href
                )
                if full_url not in seen:
                    seen.add(full_url)
                    devices.append({'PDPPageURL': href})

        listing_results = []
        for device in devices:
            pdp_url = device.get('PDPPageURL', '')
            if not pdp_url:
                continue
            full_url = (
                f"{ATT_BASE_URL}{pdp_url}"
                if pdp_url.startswith('/') else pdp_url
            )
            listing_results.append({
                'url': full_url,
                'product_name': device.get('shortDisplayName', ''),
                'brand': device.get('brand', ''),
                'sku': device.get('skuId', ''),
                'price': device.get('FinalPrice'),
                'avg_rating': device.get('starRatings'),
                'num_reviews': device.get('numOfStarReviews'),
                'image_url': device.get('mobileImageUrl', ''),
            })

        self._logger.info(
            f"ATT: Found {len(listing_results)} devices on listing page."
        )
        return listing_results

    # ------------------------------------------------------------------
    # Product Detail Scraping
    # ------------------------------------------------------------------

    async def _scrape_product_detail(self, url: str) -> Optional[dict]:
        """Scrape a single product detail page (PDP).

        Navigates to the PDP, extracts JSON-LD Product data, and returns
        a flat dict with all product fields.

        Args:
            url: The full URL to the product detail page.

        Returns:
            A dict with product data, or None on failure.
        """
        async with self.semaphore:
            try:
                self._logger.info(f"ATT: Scraping PDP: {url}")
                await self.get_page(url)
                await asyncio.sleep(self.delay)

                page_source = self._driver.page_source
                product_ld = self._extract_json_ld_product(page_source)

                if product_ld:
                    result = self._parse_product_json_ld(product_ld, url)
                    self._logger.info(
                        f"ATT: Extracted product '{result.get('product_name', 'N/A')}' "
                        f"from JSON-LD."
                    )
                    return result

                # Fallback: basic DOM extraction if JSON-LD is missing
                self._logger.warning(
                    f"ATT: No JSON-LD Product found for {url}. "
                    "Attempting DOM fallback."
                )
                return self._extract_from_dom(page_source, url)

            except Exception as exc:
                self._logger.error(
                    f"ATT: Error scraping product at {url}: {exc}"
                )
                return None

    def _extract_from_dom(
        self, page_source: str, url: str
    ) -> Optional[dict]:
        """Fallback DOM-based extraction when JSON-LD is unavailable.

        Args:
            page_source: Raw HTML page source.
            url: The product page URL.

        Returns:
            A dict with whatever product data could be extracted, or None.
        """
        try:
            soup = BeautifulSoup(page_source, 'html.parser')

            # Title
            title_el = soup.select_one('h1')
            title = title_el.get_text(strip=True) if title_el else ''

            # Price — look for common price patterns
            price = None
            price_el = soup.find(
                string=re.compile(r'\$[\d,]+\.?\d*')
            )
            if price_el:
                m = re.search(r'\$([\d,]+\.?\d*)', price_el)
                if m:
                    try:
                        price = float(m.group(1).replace(',', ''))
                    except ValueError:
                        pass

            # Image
            img_el = soup.select_one('img[src*="hero"]') or soup.select_one(
                'img[alt*="phone"]'
            )
            image_url = img_el.get('src', '') if img_el else ''

            return {
                'sku': '',
                'brand': '',
                'product_name': title,
                'image_url': image_url,
                'images': '[]',
                'price': price,
                'url': url,
                'specifications': '{}',
                'product_description': '',
                'num_reviews': None,
                'avg_rating': None,
            }
        except Exception as exc:
            self._logger.error(f"ATT: DOM fallback failed for {url}: {exc}")
            return None

    # ------------------------------------------------------------------
    # Type: product_info
    # ------------------------------------------------------------------

    async def product_info(self):
        """Scrape AT&T Prepaid product information.

        This is the main ``type`` method. It supports two modes:

        - **With DataFrame**: Enriches each row by visiting its product URL.
        - **Standalone**: Discovers all devices from the listing page,
          visits each PDP for full details.

        Returns:
            A pandas DataFrame with product data.
        """
        # Ensure Selenium driver is available
        self.headless = True
        self.as_mobile = False

        if not self._driver:
            await self.get_driver()

        # Override User-Agent with a desktop version
        desktop_ua = random.choice(DESKTOP_USER_AGENTS)
        self._driver.execute_cdp_cmd(
            'Network.setUserAgentOverride', {'userAgent': desktop_ua}
        )
        self._logger.info(
            f"ATT: Set desktop User-Agent: {desktop_ua[:50]}..."
        )

        if self.previous and self.data is not None and not self.data.empty:
            # ── Mode 1: Enrich existing DataFrame ──
            return await self._product_info_from_dataframe()
        else:
            # ── Mode 2: Standalone — scrape entire listing ──
            return await self._product_info_standalone()

    async def _product_info_standalone(self) -> pd.DataFrame:
        """Standalone mode: scrape listing + all product detail pages.

        Returns:
            A DataFrame with all discovered products.
        """
        # Step 1: Get all device URLs from the listing page
        listing = await self._scrape_listing()
        if not listing:
            raise DataNotFound(
                "ATT: No devices found on the listing page.",
                status=404,
            )

        # Step 2: Visit each PDP for full details (sequentially via semaphore)
        all_products = []
        tasks = [
            self._scrape_product_detail(device['url'])
            for device in listing
        ]
        results = await self._processing_tasks(
            tasks,
            description='ATT: Scraping product details',
            concurrently=False,  # Sequential for Selenium (single driver)
        )

        for result in results:
            if result is not None:
                all_products.append(result)

        if not all_products:
            raise DataNotFound(
                "ATT: Could not extract any product details.",
                status=404,
            )

        self.data = pd.DataFrame(all_products)
        self.data['origin'] = 'att_prepaid'

        self._logger.notice(
            f"ATT: Scraped {len(self.data)} products successfully."
        )
        return self.data

    async def _product_info_from_dataframe(self) -> pd.DataFrame:
        """DataFrame mode: enrich each row with scraped product data.

        Expects the DataFrame to have a ``url`` column (or we'll build
        URLs from ``sku``).

        Returns:
            The enriched DataFrame.
        """
        # Ensure output columns exist
        for col in (
            'sku', 'brand', 'product_name', 'image_url', 'images',
            'price', 'url', 'specifications', 'product_description',
            'num_reviews', 'avg_rating',
        ):
            if col not in self.data.columns:
                self.data[col] = None

        for idx, row in self.data.iterrows():
            product_url = row.get('url', '')
            if not product_url:
                self._logger.warning(
                    f"ATT: Row {idx} has no 'url', skipping."
                )
                continue

            product_data = await self._scrape_product_detail(product_url)
            if product_data:
                for key, value in product_data.items():
                    if key in self.data.columns:
                        self.data.at[idx, key] = value
                    else:
                        self.data.at[idx, key] = value

            # Rate limiting between products
            await asyncio.sleep(random.uniform(0.5, 1.5))

        self.data['origin'] = 'att_prepaid'
        self._logger.notice(
            f"ATT: Enriched {len(self.data)} rows from DataFrame."
        )
        return self.data

    # ------------------------------------------------------------------
    # Plans Scraping
    # ------------------------------------------------------------------

    def _is_online_only(self, text: str) -> bool:
        """Return True if the given text contains an 'Online Only' marker.

        Args:
            text: Text content to check.

        Returns:
            True if the plan is marked as Online Only.
        """
        return bool(re.search(r'online\s+only', text, re.IGNORECASE))

    def _extract_price_from_text(self, text: str) -> Optional[float]:
        """Extract the first dollar-price found in a text string.

        Args:
            text: Text that may contain a price like "$35/mo." or "35".

        Returns:
            Price as float, or None if not found.
        """
        m = re.search(r'\$?([\d]+(?:\.\d{1,2})?)\s*/\s*mo', text, re.IGNORECASE)
        if m:
            try:
                return float(m.group(1))
            except ValueError:
                pass
        return None

    def _plans_from_next_data_js(self) -> list[dict]:
        """Extract all non-Online-Only plans directly from ``window.__NEXT_DATA__``.

        AT&T stores all plan data server-side in the Next.js page payload at
        ``props.pageProps.sections[N].components["0"].tabs[T].plans[P]``.

        Online-Only plans are identified by the presence of a ``promoText``
        field in ``plan.content`` — non-Online-Only plans omit that field.

        Returns:
            List of plan dicts with keys: plan_name, price, specs.
            Returns an empty list if the data is unavailable or malformed.
        """
        script = """
return (function() {
    try {
        var data = window.__NEXT_DATA__;
        if (!data) return '[]';
        var sections = (data.props || {}).pageProps && data.props.pageProps.sections || [];
        var plans = [];

        for (var s = 0; s < sections.length; s++) {
            var components = sections[s].components || {};
            var compKeys = Object.keys(components);
            for (var ck = 0; ck < compKeys.length; ck++) {
                var comp = components[compKeys[ck]];
                var tabs = comp.tabs || [];
                if (!tabs.length || !tabs[0].plans) continue;

                // Found the plans tabs section
                for (var t = 0; t < tabs.length; t++) {
                    var tabPlans = tabs[t].plans || [];
                    for (var p = 0; p < tabPlans.length; p++) {
                        var content = tabPlans[p].content || {};

                        // Online-Only plans have a promoText field; skip them
                        if (content.promoText) continue;

                        // Plan name (strip HTML tags)
                        var headingRaw = (content.heading || {}).heading || '';
                        var name = headingRaw.replace(/<[^>]+>/g, '').trim();

                        // Price
                        var priceDetails = content.priceDetails || [{}];
                        var price = parseFloat(priceDetails[0].linePrice || '0') || null;

                        // Features from accordion content
                        var accordionItems = (content.accordion || {}).accordionContent || [];
                        var features = [];
                        for (var f = 0; f < accordionItems.length; f++) {
                            var fh = ((accordionItems[f].heading || {}).heading || '')
                                .replace(/<[^>]+>/g, '').trim();
                            if (fh) features.push(fh);
                        }

                        if (name) {
                            plans.push({plan_name: name, price: price, specs: features});
                        }
                    }
                }
                // Stop after finding the first tabs-with-plans section
                if (plans.length) return JSON.stringify(plans);
            }
        }
        return JSON.stringify(plans);
    } catch(e) {
        return '[]';
    }
})();
"""
        try:
            raw = self._driver.execute_script(script)
            return json.loads(raw) if raw else []
        except Exception as exc:
            self._logger.warning(f"ATT plans __NEXT_DATA__ JS failed: {exc}")
            return []

    def _parse_plans_from_next_data(self, next_data: dict) -> list[dict]:
        """Try to extract plan info from the __NEXT_DATA__ JSON object.

        Walks common key paths where AT&T embeds plan data.

        Args:
            next_data: Parsed __NEXT_DATA__ dict from the page.

        Returns:
            List of raw plan dicts (may be empty if path not found).
        """
        # Try common paths used by AT&T's Next.js pages
        candidates = [
            next_data
            .get('props', {})
            .get('pageProps', {})
            .get('plans', []),
            next_data
            .get('props', {})
            .get('initialReduxState', {})
            .get('plans', {})
            .get('items', []),
            next_data
            .get('props', {})
            .get('pageProps', {})
            .get('planData', {})
            .get('plans', []),
        ]
        for candidate in candidates:
            if candidate:
                return candidate
        return []

    _PLAN_KEYWORDS = [
        'Unlimited Saver',
        'Unlimited Enhanced',
        'Unlimited Ultra',
        'Unlimited Premium',
        'Unlimited Extra',
        'Unlimited Starter',
        'Unlimited Basic',
    ]

    _PLAN_KEYWORDS = [
        'Unlimited Saver',
        'Unlimited Enhanced',
        'Unlimited Ultra',
        'Unlimited Premium',
        'Unlimited Extra',
        'Unlimited Starter',
        'Unlimited Basic',
    ]

    def _extract_plans_via_js(self) -> list[dict]:
        """Use JavaScript to locate plan cards in the live rendered DOM.

        Queries all heading elements (h1-h5) and checks their ``innerText``
        against known plan name keywords.  ``innerText`` concatenates text
        across child elements, so it handles React-split text like
        ``<span>Unlimited </span><span>Saver</span><sup>SM</sup>``.

        From each matched heading, walks up the DOM to find the smallest
        ancestor that contains both a price (``N/mo``) and at least one
        feature list item (``<li>``), then extracts plan data from it.

        Returns:
            List of plan dicts with keys: plan_name, price, specs.
            Returns an empty list if the JS execution fails.
        """
        keywords_js = json.dumps(self._PLAN_KEYWORDS)
        script = f"""
return (function() {{
    var keywords = {keywords_js};
    var plans = [];
    var seen = new WeakSet();
    var PRICE_RE = /([0-9]+(?:\\.[0-9]{{1,2}})?)[^\\n]{{0,10}}\\/\\s*mo/i;
    var ONLINE_ONLY_RE = /online\\s+only/i;

    var headings = document.querySelectorAll('h1, h2, h3, h4, h5');

    for (var i = 0; i < headings.length; i++) {{
        var heading = headings[i];
        var headingText = (heading.innerText || '').trim();

        var matchedKeyword = null;
        for (var k = 0; k < keywords.length; k++) {{
            if (headingText.indexOf(keywords[k]) !== -1) {{
                matchedKeyword = keywords[k];
                break;
            }}
        }}
        if (!matchedKeyword) continue;

        // Step 1: Find the FIRST (smallest) ancestor that contains a price.
        // We do NOT require <li> elements — AT&T renders features as <p>/<div>.
        var card = null;
        var el = heading.parentElement;
        for (var depth = 0; depth < 20 && el && el !== document.body; depth++) {{
            if (PRICE_RE.test(el.innerText || '')) {{
                card = el;
                break;
            }}
            el = el.parentElement;
        }}
        if (!card || seen.has(card)) continue;
        seen.add(card);

        // Step 2: Try the parent of the price container to get a fuller view
        // that includes the features section (which is a sibling of the price div).
        // Only use the parent if it doesn't introduce "Online Only" text.
        var planEl = card;
        var parentEl = card.parentElement;
        if (parentEl && parentEl !== document.body) {{
            var parentText = parentEl.innerText || '';
            if (!ONLINE_ONLY_RE.test(parentText)) {{
                planEl = parentEl;
            }}
        }}

        var planText = planEl.innerText || '';

        // Skip if the chosen container still has "Online Only"
        if (ONLINE_ONLY_RE.test(planText)) continue;

        // Plan name — strip "SM" / "℠" superscript
        var name = headingText
            .replace(/\\s*SM\\s*$/, '')
            .replace(/\\s*\\u2120\\s*$/, '')
            .trim();

        // Price — first digits/mo match (35.00/mo preferred over 30GB/mo)
        var pm = planText.match(PRICE_RE);
        var price = pm ? parseFloat(pm[1]) : null;

        // Features: try <li> elements first
        var features = [];
        var liEls = planEl.querySelectorAll('li');
        for (var j = 0; j < liEls.length; j++) {{
            var ft = (liEls[j].innerText || '').trim();
            if (ft.length > 3 && !/^[0-9$]/.test(ft)) {{
                features.push(ft);
            }}
        }}

        // Fallback: lines after "Here's what you'll get"
        if (features.length === 0) {{
            var lines = planText.split('\\n');
            var inF = false;
            for (var m = 0; m < lines.length; m++) {{
                var line = lines[m].trim();
                if (/what you.ll get/i.test(line)) {{ inF = true; continue; }}
                if (inF && line.length > 3
                    && !/^(shop|see offer|learn more|terms|taxes|single line|\\*|req|for all)/i.test(line)
                    && !/[0-9]+\\/mo/i.test(line)) {{
                    features.push(line);
                }}
            }}
        }}

        plans.push({{ plan_name: name, price: price, specs: features }});
    }}

    return JSON.stringify(plans);
}})();
"""
        try:
            raw = self._driver.execute_script(script)
            if not raw:
                return []
            return json.loads(raw)
        except Exception as exc:
            self._logger.warning(
                f"ATT plans: JS extraction failed: {exc}"
            )
            return []

    async def _scrape_plans_page(self) -> list[dict]:
        """Scrape the AT&T Prepaid plans page.

        Extracts all non-Online-Only plan data from ``window.__NEXT_DATA__``
        using the confirmed JSON path::

            props.pageProps.sections[N].components["0"].tabs[T].plans[P]

        Online-Only plans are identified by the presence of ``content.promoText``.

        Returns:
            List of plan dicts with keys: plan_name, price, specs.
        """
        self._logger.info(
            f"ATT: Navigating to plans page: {ATT_PREPAID_PLANS_URL}"
        )
        await self.get_page(ATT_PREPAID_PLANS_URL)

        # Wait for Next.js hydration so __NEXT_DATA__ is fully available.
        _check_js = (
            "var d = window.__NEXT_DATA__;"
            "if (!d) return false;"
            "var secs = (d.props||{}).pageProps && d.props.pageProps.sections || [];"
            "for (var i=0;i<secs.length;i++){"
            "  var comps = secs[i].components||{};"
            "  var keys = Object.keys(comps);"
            "  for (var k=0;k<keys.length;k++){"
            "    if ((comps[keys[k]].tabs||[]).length && comps[keys[k]].tabs[0].plans) return true;"
            "  }}"
            "return false;"
        )
        for _attempt in range(20):
            if self._driver.execute_script(_check_js):
                self._logger.info(
                    f"ATT: __NEXT_DATA__ plan data ready after ~{_attempt}s."
                )
                break
            await asyncio.sleep(1)
        else:
            self._logger.warning(
                "ATT: __NEXT_DATA__ plan data not detected — proceeding anyway."
            )

        # Extract directly from __NEXT_DATA__ using the confirmed JSON path.
        # All plans (both tabs) are in the server-rendered payload —
        # no tab-clicking or DOM walking required.
        plans = self._plans_from_next_data_js()
        if plans:
            self._logger.info(
                f"ATT: Extracted {len(plans)} non-Online-Only plan(s) "
                "from __NEXT_DATA__."
            )
            return [
                {
                    'plan_name': p['plan_name'],
                    'price': p['price'],
                    'specs': json.dumps(p['specs'], ensure_ascii=False),
                }
                for p in plans
            ]

        self._logger.warning(
            "ATT: __NEXT_DATA__ extraction returned no plans."
        )
        return []


    async def plans(self) -> pd.DataFrame:
        """Scrape AT&T Prepaid plan information.

        Navigates to the AT&T Prepaid plans page and extracts all plans
        that are NOT marked as "Online Only". Currently those are:

        - Unlimited Saver  ($35/mo.)
        - Unlimited Enhanced Plus ($45/mo.)
        - Unlimited Ultra  ($60/mo.)

        Each plan row contains:

        - ``plan_name``: Display name of the plan.
        - ``price``: Monthly price as a float.
        - ``specs``: JSON-encoded list of all included features/specs.

        Returns:
            A pandas DataFrame with one row per qualifying plan.
        """
        self.headless = True
        self.as_mobile = False

        if not self._driver:
            await self.get_driver()

        # Use a desktop User-Agent to avoid mobile redirects
        desktop_ua = random.choice(DESKTOP_USER_AGENTS)
        self._driver.execute_cdp_cmd(
            'Network.setUserAgentOverride', {'userAgent': desktop_ua}
        )
        self._logger.info(
            f"ATT: Set desktop User-Agent for plans: {desktop_ua[:50]}..."
        )

        plan_list = await self._scrape_plans_page()

        if not plan_list:
            raise DataNotFound(
                "ATT: No qualifying plans found on the plans page.",
                status=404,
            )

        self.data = pd.DataFrame(plan_list)
        self.data['origin'] = 'att_prepaid_plans'

        self._logger.notice(
            f"ATT: Scraped {len(self.data)} non-Online-Only plans."
        )
        return self.data

    # ------------------------------------------------------------------
    # Run dispatcher
    # ------------------------------------------------------------------

    async def run(self):
        """Dispatch to the requested type function and return results.

        Uses the same pattern as BestBuy: ``self._fn`` maps to a method
        name (e.g., ``product_info``).
        """
        fn = getattr(self, self._fn)
        if not callable(fn):
            raise ComponentError(
                f"ATT: Function '{self._fn}' is not callable."
            )
        try:
            result = await fn()
        except (ComponentError, DataNotFound, ConfigError):
            raise
        except Exception as exc:
            raise ComponentError(
                f"ATT: Error executing '{self._fn}': {exc}"
            ) from exc

        # Debug output
        if result is not None and isinstance(result, pd.DataFrame):
            print(result)
            print("::: Printing Column Information === ")
            for column, t in result.dtypes.items():
                print(
                    column, "->", t, "->", result[column].iloc[0]
                )

        self._result = result
        return self._result
