"""Costco Wholesale store-locator search strategy.

Unlike Tractor Supply's site (one page per state, all stores embedded),
Costco requires a TWO-level crawl:

1. A per-state directory page (costco.com/sitemaps/warehouses-by-state/<ABBR>)
   that is just a list of links to individual warehouse pages - it does
   NOT embed store data itself.
2. Each individual warehouse page (costco.com/w/-/<state-slug>/<city-slug>/<number>)
   embeds a clean, standard `schema.org` `LocalBusiness` JSON-LD block with
   address/phone/geo/hours - no escaping, no RSC-stream wrapping.

Verified 2026-08-11 against a real (non-headless) Chrome session: headless
Chrome gets served a generic ~185KB block page (wrong <title>); the same
request non-headless returns the real ~3MB page. Both the directory page
and the individual warehouse pages need `headless: false`.

With ~600 US warehouses, this crawl is ~50 directory fetches + ~600
individual-page fetches - budget `request_delay` and runtime accordingly.

For a quick test run, pass `args: {limit: 10}` in the task YAML to stop
after the first 10 warehouses found (see search()) instead of crawling
every state.
"""
import json
import re
import time
import random
from datetime import date

import pandas as pd

from .base import RetailerStrategy, build_direction_url, group_consecutive_day_hours

#: Standard USPS state abbreviations + DC. Costco's directory URL takes the
#: bare abbreviation directly (e.g. /sitemaps/warehouses-by-state/FL) -
#: no name-to-slug translation needed, unlike Tractor Supply.
US_STATE_ABBRS = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL",
    "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME",
    "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH",
    "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI",
    "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI",
    "WY",
]

WAREHOUSE_LINK_RE = re.compile(r'href="(/w/-/[a-z0-9-]+/[a-z0-9-]+/(\d+))"')

DAY_ORDER = [
    ("mon", "Monday"), ("tue", "Tuesday"), ("wed", "Wednesday"),
    ("thu", "Thursday"), ("fri", "Friday"), ("sat", "Saturday"),
    ("sun", "Sunday"),
]


class CostcoStrategy(RetailerStrategy):
    BASE_URL = "https://www.costco.com"
    #: No shared landing page - search() drives its own two-level crawl
    #: (directory page, then each warehouse page) per state seed.
    store_locator_url = None

    def __init__(self):
        #: Running total of warehouses parsed so far, across all seeds -
        #: lets `limit` (see search()) cap the crawl for a quick test run
        #: without waiting on all ~600 US warehouses.
        self._scraped_count = 0

    #: search() emits canonical column names directly (no raw-key
    #: translation needed) - identity map so scraper.py's keep_cols filter
    #: doesn't drop everything.
    field_map = {
        "store_number": "store_number",
        "store_name": "store_name",
        "street_address": "street_address",
        "city": "city",
        "state_code": "state_code",
        "zipcode": "zipcode",
        "country_code": "country_code",
        "phone_number": "phone_number",
        "latitude": "latitude",
        "longitude": "longitude",
        "url": "url",
        "store_status": "store_status",
        "open_hours_raw": "open_hours_raw",
    }

    def get_seeds(self, reference: pd.DataFrame, **kwargs) -> list:
        """No reference file for Costco - always crawl every US state."""
        return list(US_STATE_ABBRS)

    @staticmethod
    def _extract_json_ld_blocks(html: str):
        """Yield parsed dicts for every `<script type="application/ld+json">`
        block. A manual brace-depth scan (not a regex) finds the matching
        closing brace - this page's JSON-LD is plain, non-escaped JSON.
        """
        for open_match in re.finditer(r'<script type="application/ld\+json"[^>]*>', html):
            start = html.find("{", open_match.end())
            if start == -1:
                continue
            depth = 0
            end = None
            for i in range(start, len(html)):
                ch = html[i]
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        end = i + 1
                        break
            if end is None:
                continue
            try:
                yield json.loads(html[start:end])
            except ValueError:
                continue

    def _parse_warehouse_page(self, html: str, path: str, number: str) -> dict:
        local_business = None
        for data in self._extract_json_ld_blocks(html):
            if data.get("@type") == "LocalBusiness":
                local_business = data
                break
        if not local_business:
            return None
        address = local_business.get("address") or {}
        geo = local_business.get("geo") or {}
        zipcode = (address.get("postalCode") or "").split("-")[0].strip() or None
        return {
            "store_number": number,
            "store_name": f"{address.get('addressLocality', '')} {address.get('addressRegion', '')}".strip() or None,
            "street_address": address.get("streetAddress"),
            "city": address.get("addressLocality"),
            "state_code": address.get("addressRegion"),
            "zipcode": zipcode,
            "country_code": address.get("addressCountry") or "US",
            "phone_number": local_business.get("telephone"),
            "latitude": geo.get("latitude"),
            "longitude": geo.get("longitude"),
            "url": local_business.get("url") or f"{self.BASE_URL}{path}",
            # Only warehouses with a live page get scraped in the first
            # place - there's no separate open/closed signal on the page.
            "store_status": True,
            "open_hours_raw": local_business.get("openingHoursSpecification"),
        }

    def search(self, driver, seed, limit=None, **kwargs) -> list:
        if limit is not None and self._scraped_count >= limit:
            # Already hit the test cap - skip this state's directory fetch
            # entirely rather than just discarding what it would find.
            return []
        state_abbr = seed
        driver.get(f"{self.BASE_URL}/sitemaps/warehouses-by-state/{state_abbr}")
        links = sorted(set(WAREHOUSE_LINK_RE.findall(driver.page_source)))
        stores = []
        for path, number in links:
            if limit is not None and self._scraped_count >= limit:
                break
            time.sleep(1.5 + random.uniform(0, 0.5))
            driver.get(f"{self.BASE_URL}{path}")
            store = self._parse_warehouse_page(driver.page_source, path, number)
            if store:
                stores.append(store)
                self._scraped_count += 1
        return stores

    def store_key(self, raw_store):
        return raw_store.get("store_number")

    @staticmethod
    def _fmt_time(value: str):
        """'20:30:00' -> '08:30pm'; '00:00:00' treated as unset (closed)."""
        if not value:
            return None
        try:
            hour, minute, _ = value.split(":")
            hour = int(hour)
        except ValueError:
            return None
        if hour == 0 and minute == "00":
            return None
        suffix = "am" if hour < 12 else "pm"
        hour12 = hour % 12 or 12
        return f"{hour12:02d}:{minute}{suffix}"

    def _build_open_hours(self, specs) -> str:
        if not isinstance(specs, list):
            return None
        by_day = {}
        for spec in specs:
            if not isinstance(spec, dict):
                continue
            days = spec.get("dayOfWeek")
            opens = self._fmt_time(spec.get("opens"))
            closes = self._fmt_time(spec.get("closes"))
            if not days or not opens or not closes:
                continue
            if isinstance(days, str):
                days = [days]
            for day_name in days:
                by_day[day_name] = f"{opens} - {closes}"
        day_hours = [(abbr, by_day.get(full)) for abbr, full in DAY_ORDER]
        return group_consecutive_day_hours(day_hours)

    def postprocess(self, scraped: pd.DataFrame, **kwargs) -> pd.DataFrame:
        if "store_number" in scraped.columns:
            # "COS" prefix, same convention as VerizonStrategy ("VZN") and
            # TractorSupplyStrategy ("TSC") - store_number stays the bare
            # warehouse number.
            scraped["store_id"] = scraped["store_number"].apply(
                lambda n: f"COS{n}" if pd.notna(n) else None
            )
        if "open_hours_raw" in scraped.columns:
            scraped["open_hours"] = scraped["open_hours_raw"].apply(self._build_open_hours)
            scraped = scraped.drop(columns=["open_hours_raw"])
        if not scraped.empty:
            scraped["updated_date"] = pd.Timestamp(date.today())
            scraped["direction_url"] = scraped.apply(build_direction_url, axis=1)
        return scraped
