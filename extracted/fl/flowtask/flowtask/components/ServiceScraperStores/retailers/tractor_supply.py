"""Tractor Supply Co. store-locator search strategy.

Unlike Verizon's geo-radius search API, Tractor Supply's site is a
Next.js app that server-renders one page per US state
(https://www.tractorsupply.com/tsc/store-locations/<state-slug>) and embeds
the full store list for that state as JSON inside a `__NEXT_DATA__`
<script> tag (a React Query "dehydrated" cache, keyed
`['storesByState', 'get', '<STATE_ABBR>']`) - no separate XHR/JSON API call
is needed once the page has loaded.

Verified 2026-08-11 against a real (non-headless) Chrome session:
headless Chrome gets served a generic Akamai block page (no
`__NEXT_DATA__`, no store data) - this site requires the same
`headless: false` + virtual-display approach as Verizon. It's also
noticeably rate-sensitive: back-to-back state requests with no delay
started returning "Access Denied" after the very first one, but the same
requests spaced ~8s apart succeeded - set `request_delay` generously
(6-8s or more) in the task YAML for this scrapper.
"""
import json
import re
from datetime import date

import pandas as pd

from .base import RetailerStrategy, build_direction_url, group_consecutive_day_hours

#: USPS state abbreviation -> tractorsupply.com/tsc/store-locations/<slug>
#: (verified for CO/colorado, NY/new-york, NC/north-carolina; the rest
#: follow the same lowercase-hyphenated pattern). Puerto Rico/territories
#: omitted - not confirmed. DC 404s (no store there) but is left in since
#: ServiceScraperStores already tolerates a failed/empty seed.
STATE_ABBR_TO_SLUG = {
    "AL": "alabama", "AK": "alaska", "AZ": "arizona", "AR": "arkansas",
    "CA": "california", "CO": "colorado", "CT": "connecticut",
    "DE": "delaware", "DC": "district-of-columbia", "FL": "florida",
    "GA": "georgia", "HI": "hawaii", "ID": "idaho", "IL": "illinois",
    "IN": "indiana", "IA": "iowa", "KS": "kansas", "KY": "kentucky",
    "LA": "louisiana", "ME": "maine", "MD": "maryland",
    "MA": "massachusetts", "MI": "michigan", "MN": "minnesota",
    "MS": "mississippi", "MO": "missouri", "MT": "montana",
    "NE": "nebraska", "NV": "nevada", "NH": "new-hampshire",
    "NJ": "new-jersey", "NM": "new-mexico", "NY": "new-york",
    "NC": "north-carolina", "ND": "north-dakota", "OH": "ohio",
    "OK": "oklahoma", "OR": "oregon", "PA": "pennsylvania",
    "RI": "rhode-island", "SC": "south-carolina", "SD": "south-dakota",
    "TN": "tennessee", "TX": "texas", "UT": "utah", "VT": "vermont",
    "VA": "virginia", "WA": "washington", "WV": "west-virginia",
    "WI": "wisconsin", "WY": "wyoming",
}
STATE_SLUGS = list(STATE_ABBR_TO_SLUG.values())

DAY_NAMES = [
    ("mon", "Monday"), ("tue", "Tuesday"), ("wed", "Wednesday"),
    ("thu", "Thursday"), ("fri", "Friday"), ("sat", "Saturday"),
    ("sun", "Sunday"),
]

NEXT_DATA_RE = re.compile(
    r'<script id="__NEXT_DATA__" type="application/json"[^>]*>(.*?)</script>',
    re.S,
)


class TractorSupplyStrategy(RetailerStrategy):
    BASE_URL = "https://www.tractorsupply.com"
    #: search() navigates directly to each state's URL - no shared landing
    #: page to pre-load.
    store_locator_url = None

    field_map = {
        "storenum": "store_number",
        "identifier": "api_store_id",
        "store_name": "store_name",
        "address1": "store_address",
        "city": "city",
        "state": "state_code",
        "zipcode": "zipcode",
        "phone1": "phone_number",
        "country": "country_code",
        "time_zone": "tz",
        "services": "services",
        "active": "store_status",
        "operating_hours": "open_hours_raw",
        "latitude": "latitude",
        "longitude": "longitude",
    }

    def get_seeds(self, reference: pd.DataFrame, **kwargs) -> list:
        """Crawl every US state, UNLESS the reference dataframe (if any)
        carries its own `state_code` column - in that case, given this
        site's rate-sensitivity, only crawl the states actually present
        there instead of wasting requests on states with no reference
        stores to reconcile against.
        """
        if reference is not None and not reference.empty and "state_code" in reference.columns:
            abbrs = set(
                reference["state_code"].dropna().astype(str).str.upper().str.strip()
            )
            slugs = [STATE_ABBR_TO_SLUG[a] for a in abbrs if a in STATE_ABBR_TO_SLUG]
            if slugs:
                return slugs
        return list(STATE_SLUGS)

    def search(self, driver, seed, **kwargs) -> list:
        state_slug = seed
        driver.get(f"{self.BASE_URL}/tsc/store-locations/{state_slug}")
        match = NEXT_DATA_RE.search(driver.page_source)
        if not match:
            return []
        try:
            data = json.loads(match.group(1))
            queries = data["props"]["pageProps"]["dehydratedState"]["queries"]
        except (KeyError, TypeError, ValueError):
            return []
        stores = []
        for query in queries:
            key = query.get("queryKey") or []
            if not key or key[0] != "storesByState":
                continue
            store_list = query.get("state", {}).get("data", {}).get("StoreList", []) or []
            for item in store_list:
                value = item.get("value")
                if value:
                    stores.append(value)
        return stores

    def store_key(self, raw_store):
        return raw_store.get("storenum") or raw_store.get("identifier")

    @staticmethod
    def _normalize_hours(raw: str) -> str:
        """'08:00 AM - 09:00 PM' -> '08:00am - 09:00pm'."""
        if not raw:
            return None
        parts = [p.strip() for p in raw.split("-")]
        if len(parts) != 2:
            return raw.lower().replace(" ", "")
        return f"{parts[0].lower().replace(' ', '')} - {parts[1].lower().replace(' ', '')}"

    def _build_open_hours(self, raw_json) -> str:
        if pd.isna(raw_json) or not raw_json:
            return None
        try:
            hours_by_day = json.loads(raw_json)
        except (ValueError, TypeError):
            return None
        days = [
            (abbr, self._normalize_hours(hours_by_day.get(day_name)))
            for abbr, day_name in DAY_NAMES
        ]
        return group_consecutive_day_hours(days)

    @staticmethod
    def _clean_services(raw: str) -> str:
        if pd.isna(raw) or not raw:
            return None
        return ", ".join(part for part in raw.split("|") if part.strip())

    def _build_store_url(self, row) -> str:
        """Individual store page: tractorsupply.com/tsc/store_<City><ST><Zip>_<StoreNumber>
        (city with spaces stripped - verified against a real store page URL)."""
        city = row.get("city")
        state = row.get("state_code")
        zipcode = row.get("zipcode")
        store_number = row.get("store_number")
        if any(pd.isna(v) or not str(v).strip() for v in (city, state, zipcode, store_number)):
            return None
        # Raw city comes back upper-case ("BRUSH"); real store URLs use
        # TitleCase with spaces stripped (e.g. "AmericanCanyon").
        city_slug = str(city).title().replace(" ", "")
        return f"{self.BASE_URL}/tsc/store_{city_slug}-{state}-{zipcode}_{store_number}"

    def postprocess(self, scraped: pd.DataFrame, **kwargs) -> pd.DataFrame:
        if "open_hours_raw" in scraped.columns:
            scraped["open_hours"] = scraped["open_hours_raw"].apply(self._build_open_hours)
            scraped = scraped.drop(columns=["open_hours_raw"])
        if "services" in scraped.columns:
            scraped["services"] = scraped["services"].apply(self._clean_services)
        if "store_number" in scraped.columns:
            scraped["store_id"] = scraped["store_number"].apply(
                lambda n: f"TSC{n}" if pd.notna(n) else None
            )
        if not scraped.empty:
            scraped["updated_date"] = pd.Timestamp(date.today())
            scraped["url"] = scraped.apply(self._build_store_url, axis=1)
            scraped["direction_url"] = scraped.apply(build_direction_url, axis=1)
        return scraped

    def normalize_store_status(self, value) -> bool:
        """The site's `active` flag is the string "1"/"0"."""
        if pd.isna(value):
            return False
        return str(value).strip() == "1"
