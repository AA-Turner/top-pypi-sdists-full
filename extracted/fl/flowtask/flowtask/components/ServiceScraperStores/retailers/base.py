"""Interface a retailer must implement to plug into ServiceScraperStores."""
import pandas as pd


class RetailerStrategy:
    """Base class for a per-retailer store-locator search strategy.

    A strategy only knows how to talk to ONE retailer's store locator - the
    ServiceScraperStores component owns the Selenium driver, the seed loop,
    and the reconciliation against the reference dataframe.

    A "seed" is whatever unit of work `get_seeds()` decides to hand to
    `search()` one at a time - it can be a (latitude, longitude) tuple (as
    for a geo-radius search API, see VerizonStrategy), a state slug (as for
    a full state-by-state crawl, see TractorSupplyStrategy), or anything
    else a retailer's locator needs. ServiceScraperStores treats it as an
    opaque value.

    At minimum, `field_map` must produce canonical `store_name`, `city`,
    `state_code`, `latitude` and `longitude` columns - the reconciliation
    step (name + city + state matching against the pipeline's reference
    dataframe) depends on them.
    """

    #: Initial page Selenium navigates to before searching, if any. Leave
    #: None for strategies (like TractorSupplyStrategy) that navigate
    #: directly to a per-seed URL inside search() instead.
    store_locator_url: str = None
    #: Raw API/HTML key -> canonical column name.
    field_map: dict = {}

    def get_seeds(self, reference: pd.DataFrame) -> list:
        """Return the list of seeds to feed one at a time to search()."""
        raise NotImplementedError

    def search(self, driver, seed, **kwargs) -> list:
        """Run one seed's search, return a list of raw store dicts."""
        raise NotImplementedError

    def store_key(self, raw_store: dict):
        """Dedup key for a raw store dict (called before the field_map rename)."""
        raise NotImplementedError

    def postprocess(self, scraped: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """Retailer-specific column derivations, applied to the scraped
        dataframe right after the field_map rename (and before
        reconciliation against the reference dataframe). Default: no-op.
        """
        return scraped

    def normalize_store_status(self, value):
        """Applied to the merged (post-reconciliation) `store_status`
        column, if present. Default: pass the raw value through unchanged.
        """
        return value


def build_direction_url(row) -> str:
    """'Directions from current location' Google Maps deep link, from a
    row with store_address (or, failing that, street_address)/city/
    state_code/zipcode columns. Shared across strategies - the link format
    has nothing retailer-specific about it.
    """
    address = row.get("store_address")
    if pd.isna(address) or not str(address).strip():
        address = row.get("street_address")
    parts = [address, row.get("city"), row.get("state_code"), row.get("zipcode"), "USA"]
    parts = [str(p).strip() for p in parts if pd.notna(p) and str(p).strip()]
    if not parts:
        return None
    address = ", ".join(parts).replace(" ", "+")
    return f"https://www.google.com/maps/dir/Current+Location/{address}/"


def group_consecutive_day_hours(day_hours: list) -> str:
    """Shared formatter for a week of opening hours.

    `day_hours` is a list of `(day_abbr, "9:00am - 9:00pm" | None)` tuples
    in week order. Consecutive days sharing the same hours are grouped,
    e.g. [('mon','9-9'), ('tue','9-9'), ('sun','10-6')] ->
    'mon-tue. 9-9 | sun. 10-6'.
    """
    groups = []
    current_days, current_hours = [], None
    for abbr, hours in day_hours:
        if current_days and hours == current_hours:
            current_days.append(abbr)
        else:
            if current_days:
                groups.append((current_days, current_hours))
            current_days, current_hours = [abbr], hours
    if current_days:
        groups.append((current_days, current_hours))

    parts = []
    for group_days, hours in groups:
        if hours is None:
            continue
        label = group_days[0] if len(group_days) == 1 else f"{group_days[0]}-{group_days[-1]}"
        parts.append(f"{label}. {hours}")
    return " | ".join(parts) if parts else None
