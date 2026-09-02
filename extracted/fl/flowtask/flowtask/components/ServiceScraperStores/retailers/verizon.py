"""Verizon store-locator search strategy.

Ported from the navigator-dataintegrator-tasks repo
(programs/verizon/functions/store_indirect_scraper.py), where it started
life as a one-off UserFunc before being generalized into this component.
"""
import json
import re
from datetime import date

import pandas as pd

from .base import RetailerStrategy, build_direction_url, group_consecutive_day_hours


class VerizonStrategy(RetailerStrategy):
    """Verizon's public Store Locator (Next.js app) doesn't render store
    data in the initial HTML - the page geocodes the search and calls the
    JSON endpoint below. That endpoint sits behind Akamai bot-detection
    (keys off more than cookies - also fingerprints the TLS/HTTP client),
    so replaying cookies into a plain `requests` session is unreliable.
    Instead ServiceScraperStores keeps one real (non-headless) Chrome
    session open for the whole run and this strategy issues every search
    as an in-page `fetch()` (via `execute_async_script`), so it always goes
    out through the browser's own network stack - exactly like a real
    visitor typing in the search box.
    """
    BASE_URL = "https://www.verizon.com"
    store_locator_url = f"{BASE_URL}/nextgendigital/nos/storelocator/searchresults/"
    SEARCH_API = f"{BASE_URL}/digital/nsa/nos/gw/retail/searchresultsdata"

    FETCH_SCRIPT = """
    const callback = arguments[arguments.length - 1];
    fetch(arguments[0], {
        method: 'POST',
        headers: {'content-type': 'application/json'},
        body: arguments[1]
    }).then(r => r.json()).then(data => callback({ok: true, data: data}))
      .catch(err => callback({ok: false, error: String(err)}));
    """

    field_map = {
        "storeNumber": "store_number",
        "id": "api_store_id",
        "storeName": "store_name",
        "businessName": "business_name",
        "channel": "channel",
        "channelName": "channel_name",
        "subChannelName": "subchannel_name",
        "phoneNumber": "phone_number",
        "netaceLocationCode": "location_code",
        "address1": "store_address",
        "city": "city",
        "state": "state_code",
        "zipCode": "zipcode",
        "storeStatus": "store_status",
        "distance": "distance_miles",
        "region": "region_name",
        "area": "area_name",
        "storeUrl": "url",
        "opening_date": "opening_date",
        "hoursMon": "hours_mon",
        "hoursTue": "hours_tue",
        "hoursWed": "hours_wed",
        "hoursThu": "hours_thu",
        "hoursFri": "hours_fri",
        "hoursSat": "hours_sat",
        "hoursSun": "hours_sun",
        "store_latitude": "latitude",
        "store_longitude": "longitude",
    }

    DAY_COLUMNS = [
        ("mon", "hours_mon"), ("tue", "hours_tue"), ("wed", "hours_wed"),
        ("thu", "hours_thu"), ("fri", "hours_fri"), ("sat", "hours_sat"),
        ("sun", "hours_sun"),
    ]

    def get_seeds(self, reference: pd.DataFrame, precision: float = 0.15, **kwargs) -> list:
        """Reduce the reference list to one search per nearby cluster of
        stores (a ~20 mile search radius means points closer than
        `precision` degrees apart would mostly return the same result set).
        """
        seeds = reference[["latitude", "longitude"]].dropna().copy()
        seeds["lat_bucket"] = (seeds["latitude"] / precision).round() * precision
        seeds["lon_bucket"] = (seeds["longitude"] / precision).round() * precision
        seeds = seeds.drop_duplicates(subset=["lat_bucket", "lon_bucket"])
        return list(seeds[["latitude", "longitude"]].itertuples(index=False, name=None))

    def search(self, driver, seed, range_miles=20, max_stores=25, **kwargs):
        latitude, longitude = seed
        payload = json.dumps({
            "latitude": latitude,
            "longitude": longitude,
            "filterPromoStores": False,
            "range": range_miles,
            "noOfStores": max_stores,
            "excludeIndirect": False,
            "retrieveBy": "GEO",
        })
        result = driver.execute_async_script(self.FETCH_SCRIPT, self.SEARCH_API, payload)
        if not result.get("ok"):
            raise RuntimeError(result.get("error"))
        body = result["data"]
        stores = body.get("body", {}).get("data", {}).get("stores", []) or []
        for store in stores:
            location = store.get("location") or {}
            store["store_latitude"] = location.get("latitude")
            store["store_longitude"] = location.get("longitude")
        return stores

    def store_key(self, raw_store):
        return raw_store.get("storeNumber") or raw_store.get("id")

    @staticmethod
    def _short_store_id(store_number) -> str:
        """'VZN' + digits with the leading letter and leading zeros
        stripped (e.g. 'A00000251235' -> 'VZN251235').
        """
        if pd.isna(store_number):
            return None
        digits = re.sub(r"\D", "", str(store_number))
        if not digits:
            return None
        return f"VZN{int(digits)}"

    def _full_store_url(self, store_url) -> str:
        """The API returns storeUrl as a relative path; turn it into a
        full URL that can be copy-pasted straight into a browser."""
        if pd.isna(store_url):
            return None
        url = str(store_url).strip()
        if not url:
            return None
        if url.startswith("http://") or url.startswith("https://"):
            return url
        if not url.startswith("/"):
            url = f"/{url}"
        return f"{self.BASE_URL}{url}"

    @staticmethod
    def _normalize_hours(raw) -> str:
        """'10:00 AM 07:30 PM' -> '10:00am - 07:30pm'."""
        if pd.isna(raw):
            return None
        text = str(raw).strip()
        if not text:
            return None
        parts = text.split()
        if len(parts) != 4:
            return text.lower().replace(" ", "")
        start = f"{parts[0]}{parts[1].lower()}"
        end = f"{parts[2]}{parts[3].lower()}"
        return f"{start} - {end}"

    def _build_open_hours(self, row) -> str:
        """Concatenate hours_mon..hours_sun into one readable string,
        grouping consecutive days that share the same hours."""
        days = [(abbr, self._normalize_hours(row.get(col))) for abbr, col in self.DAY_COLUMNS]
        return group_consecutive_day_hours(days)

    def postprocess(self, scraped: pd.DataFrame, channel_filter: str = "IND", **kwargs) -> pd.DataFrame:
        if channel_filter and "channel" in scraped.columns:
            scraped = scraped[scraped["channel"] == channel_filter].copy()
        if "store_number" in scraped.columns:
            scraped["store_id"] = scraped["store_number"].apply(self._short_store_id)
        if "url" in scraped.columns:
            scraped["url"] = scraped["url"].apply(self._full_store_url)
        if not scraped.empty:
            scraped["updated_date"] = pd.Timestamp(date.today())
            scraped["direction_url"] = scraped.apply(build_direction_url, axis=1)
            scraped["open_hours"] = scraped.apply(self._build_open_hours, axis=1)
        return scraped

    def normalize_store_status(self, value) -> bool:
        """verizon.stores.store_status is a real boolean column; the API
        (and a 'missing_on_web' row with no scrape match) gives us a status
        string like 'Open' instead."""
        if pd.isna(value):
            return False
        return str(value).strip().lower() == "open"
