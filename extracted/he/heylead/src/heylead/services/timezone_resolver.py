"""Timezone resolver — infer prospect timezone from location string.

Maps LinkedIn location strings (e.g., "San Francisco Bay Area", "London, England")
to IANA timezones. Used by the scheduler to send during prospect business hours.

No external dependencies — uses a heuristic lookup table for common regions.
"""

from __future__ import annotations

import logging
import re
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)

# ── Mapping: location keywords → UTC offset hours ──
# Ordered from most specific to least specific.
_LOCATION_TO_OFFSET: list[tuple[list[str], float]] = [
    # US
    (["pacific", "san francisco", "bay area", "los angeles", "seattle",
      "portland", "las vegas", "sacramento", "san diego", "silicon valley",
      "california", "oregon", "washington state", "nevada"], -8),
    (["mountain", "denver", "salt lake", "phoenix", "boise",
      "colorado", "utah", "arizona", "new mexico", "montana", "idaho", "wyoming"], -7),
    (["central", "chicago", "dallas", "houston", "austin", "minneapolis",
      "nashville", "kansas city", "milwaukee", "san antonio", "oklahoma",
      "texas", "illinois", "wisconsin", "minnesota", "iowa", "missouri",
      "louisiana", "tennessee", "arkansas", "nebraska", "oklahoma"], -6),
    (["eastern", "new york", "boston", "miami", "atlanta", "washington dc",
      "philadelphia", "charlotte", "pittsburgh", "detroit", "raleigh",
      "florida", "georgia", "ohio", "michigan", "virginia", "north carolina",
      "south carolina", "maryland", "massachusetts", "connecticut",
      "new jersey", "pennsylvania", "district of columbia"], -5),
    (["hawaii", "honolulu"], -10),
    (["alaska", "anchorage"], -9),

    # Canada
    (["toronto", "ottawa", "montreal", "quebec"], -5),
    (["vancouver", "british columbia"], -8),
    (["calgary", "edmonton", "alberta"], -7),
    (["winnipeg", "manitoba", "saskatchewan"], -6),
    (["halifax", "nova scotia", "new brunswick"], -4),

    # UK & Ireland
    (["london", "united kingdom", "england", "uk", "scotland", "wales",
      "ireland", "dublin", "belfast", "manchester", "birmingham", "leeds",
      "glasgow", "liverpool", "edinburgh", "bristol", "cambridge", "oxford"], 0),

    # Western Europe
    (["paris", "berlin", "amsterdam", "brussels", "madrid", "barcelona",
      "munich", "frankfurt", "zurich", "vienna", "copenhagen", "oslo", "stockholm",
      "milan", "rome", "lisbon", "warsaw", "prague", "budapest", "helsinki",
      "france", "germany", "netherlands", "belgium", "spain", "italy",
      "switzerland", "austria", "sweden", "norway", "denmark", "finland",
      "poland", "czech", "hungary", "portugal", "romania", "croatia",
      "serbia", "slovenia", "slovakia", "luxembourg"], 1),

    # Eastern Europe
    (["athens", "bucharest", "sofia", "istanbul", "kyiv", "tallinn",
      "riga", "vilnius", "greece", "turkey", "ukraine", "estonia",
      "latvia", "lithuania", "bulgaria"], 2),

    # Middle East
    (["riyadh", "dubai", "abu dhabi", "doha", "bahrain", "kuwait",
      "saudi arabia", "uae", "united arab emirates", "qatar"], 3),
    (["israel", "tel aviv", "jerusalem"], 2),

    # South Asia
    (["mumbai", "delhi", "bangalore", "hyderabad", "chennai", "pune",
      "kolkata", "india", "sri lanka", "nepal"], 5.5),
    (["pakistan", "karachi", "lahore", "islamabad"], 5),
    (["bangladesh", "dhaka"], 6),

    # East Asia
    (["singapore", "kuala lumpur", "malaysia", "jakarta", "indonesia",
      "bangkok", "thailand", "vietnam", "ho chi minh", "hanoi",
      "philippines", "manila", "cambodia", "myanmar"], 7),
    (["hong kong", "beijing", "shanghai", "shenzhen", "guangzhou",
      "taiwan", "taipei", "china", "perth"], 8),
    (["tokyo", "japan", "osaka", "seoul", "south korea", "korea"], 9),

    # Oceania
    (["sydney", "melbourne", "brisbane", "canberra", "australia",
      "new south wales", "victoria", "queensland"], 10),
    (["auckland", "wellington", "new zealand", "christchurch"], 12),

    # Latin America
    (["mexico city", "guadalajara", "monterrey", "mexico"], -6),
    (["bogota", "colombia", "lima", "peru", "quito", "ecuador"], -5),
    (["sao paulo", "rio de janeiro", "brasil", "brazil"], -3),
    (["buenos aires", "argentina", "santiago", "chile", "uruguay"], -3),

    # Africa
    (["johannesburg", "cape town", "south africa", "nairobi", "kenya",
      "lagos", "nigeria", "cairo", "egypt", "casablanca", "morocco",
      "accra", "ghana"], 2),
]

# Default: assume UTC if we can't determine timezone
_DEFAULT_OFFSET = 0

# Business hours window
DEFAULT_BUSINESS_START = 8   # 8 AM local
DEFAULT_BUSINESS_END = 18    # 6 PM local
DEFAULT_BUSINESS_DAYS = [0, 1, 2, 3, 4]  # Monday-Friday


def resolve_utc_offset(location: str) -> float:
    """Resolve a LinkedIn location string to a UTC offset in hours.

    Returns the offset (e.g., -8 for PST, 1 for CET).
    Returns 0 (UTC) if location is empty or unrecognized.
    """
    if not location:
        return _DEFAULT_OFFSET

    loc_lower = location.lower().strip()

    for keywords, offset in _LOCATION_TO_OFFSET:
        for kw in keywords:
            if kw in loc_lower:
                return offset

    return _DEFAULT_OFFSET


def is_business_hours(
    utc_offset: float,
    start_hour: int = DEFAULT_BUSINESS_START,
    end_hour: int = DEFAULT_BUSINESS_END,
    business_days: list[int] | None = None,
) -> bool:
    """Check if the current time is within business hours for the given UTC offset.

    Args:
        utc_offset: Hours offset from UTC (e.g., -8 for PST).
        start_hour: Start of business hours (local time, 0-23).
        end_hour: End of business hours (local time, 0-23).
        business_days: Days of week (0=Monday, 6=Sunday). Default Mon-Fri.

    Returns True if current moment is within the prospect's local business hours.
    """
    if business_days is None:
        business_days = DEFAULT_BUSINESS_DAYS

    now_utc = datetime.now(timezone.utc)
    local_time = now_utc + timedelta(hours=utc_offset)

    # Check day of week (0=Monday in Python)
    if local_time.weekday() not in business_days:
        return False

    # Check hour
    local_hour = local_time.hour
    return start_hour <= local_hour < end_hour


def seconds_until_business_hours(
    utc_offset: float,
    start_hour: int = DEFAULT_BUSINESS_START,
    end_hour: int = DEFAULT_BUSINESS_END,
    business_days: list[int] | None = None,
) -> int:
    """Calculate seconds until the next business hours window for the given offset.

    Returns 0 if currently within business hours.
    """
    if business_days is None:
        business_days = DEFAULT_BUSINESS_DAYS

    now_utc = datetime.now(timezone.utc)
    local_now = now_utc + timedelta(hours=utc_offset)

    # If currently in business hours, return 0
    if local_now.weekday() in business_days and start_hour <= local_now.hour < end_hour:
        return 0

    # Find next business day + start hour
    candidate = local_now.replace(hour=start_hour, minute=0, second=0, microsecond=0)
    if candidate <= local_now:
        candidate += timedelta(days=1)

    # Find next business day
    for _ in range(8):  # At most 7 days to next business day
        if candidate.weekday() in business_days:
            break
        candidate += timedelta(days=1)

    # Convert back to UTC and compute delta
    target_utc = candidate - timedelta(hours=utc_offset)
    delta = (target_utc - now_utc).total_seconds()
    return max(0, int(delta))


def get_prospect_location(prospect: dict) -> str:
    """Extract location from a prospect/contact dict (various field names)."""
    loc = prospect.get("location") or ""
    if isinstance(loc, dict):
        loc = loc.get("name") or loc.get("default") or loc.get("city") or ""

    if not loc:
        # Try profile_json
        profile = prospect.get("profile_json")
        if isinstance(profile, dict):
            loc = profile.get("location") or ""
            if isinstance(loc, dict):
                loc = loc.get("name") or ""

    return str(loc).strip()
