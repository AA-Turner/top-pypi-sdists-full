"""
Census dataset path resolver, URL builders, and core data models.

This module handles:
- Resolving Census dataset paths from table prefix + survey string.
- Building API URLs for data and variables endpoints.
- Scrubbing API keys from URLs before surfacing them in error messages.
- Core dataclasses: CensusQuery and CacheKey.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from flowtask.exceptions import ComponentError

# ---------------------------------------------------------------------------
# Supported geography types
# ---------------------------------------------------------------------------

GeographyType = Literal["zcta", "state", "county", "tract", "block_group", "place"]

# ---------------------------------------------------------------------------
# Dataset prefix map
#
# Key order matters: "CP" must appear before "C" so two-letter prefixes are
# matched first.  The value is the sub-path appended after "acs/<survey>/".
# Empty string means the dataset root (e.g. "acs/acs5" itself for B/C tables).
# ---------------------------------------------------------------------------

_PREFIX_PATH_MAP: dict[str, str] = {
    "DP": "profile",
    "CP": "cprofile",
    "S": "subject",
    "B": "",
    "C": "",
}


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CensusQuery:
    """Fully-resolved parameters for a single Census API request.

    Attributes:
        year: The ACS / Decennial vintage year (e.g. 2024).
        survey: The survey identifier (e.g. "acs5", "acs1").
        dataset: The resolved dataset path (e.g. "acs/acs5/profile").
        table: The table code (e.g. "DP05").
        geography: One of the supported GeographyType values.
        state_filter: FIPS code ("06"), "*" for fan-out, or None for ZCTA.
    """

    year: int
    survey: str
    dataset: str
    table: str
    geography: GeographyType
    state_filter: str | None


@dataclass(frozen=True)
class CacheKey:
    """Identifies a single cached response shard.

    Maps 1:1 to a parquet filename:
        <year>/<dataset>/<table>_<geo>[_<state>].parquet

    Attributes:
        year: The ACS / Decennial vintage year.
        dataset: The resolved dataset path (e.g. "acs/acs5/profile").
        table: The table code or a sentinel like "_variables_DP05".
        geography: The geography type.
        state: FIPS code or None for nationwide / variables requests.
    """

    year: int
    dataset: str
    table: str
    geography: GeographyType
    state: str | None


# ---------------------------------------------------------------------------
# Dataset resolution
# ---------------------------------------------------------------------------


def resolve_dataset(
    table: str,
    survey: str,
    dataset_override: str | None,
) -> str:
    """Resolve the Census API dataset path from a table code and survey.

    Args:
        table: Census table code (e.g. "DP05", "S0101", "B01001").
        survey: Survey identifier (e.g. "acs5", "acs1").
        dataset_override: If set, return this verbatim (wins over prefix inference).

    Returns:
        The full dataset path for the Census API URL
        (e.g. "acs/acs5/profile", "acs/acs5", "dec/dhc").

    Raises:
        ComponentError: When the table prefix is unknown and no override is given.
    """
    if dataset_override:
        return dataset_override

    table_upper = table.upper()

    # Check two-letter prefixes before one-letter to avoid false matches.
    for prefix, sub_path in _PREFIX_PATH_MAP.items():
        if table_upper.startswith(prefix):
            base = f"acs/{survey}"
            if sub_path:
                return f"{base}/{sub_path}"
            return base

    raise ComponentError(
        f"Unknown Census table prefix for '{table}'. "
        f"Set 'dataset' explicitly (e.g. dataset: 'dec/dhc') or use a "
        f"table that begins with one of: {list(_PREFIX_PATH_MAP.keys())}.",
        status=406,
    )


# ---------------------------------------------------------------------------
# URL builders
# ---------------------------------------------------------------------------

_BASE_URL = "https://api.census.gov/data"


def build_data_url(
    year: int,
    dataset: str,
    table: str,
    geo_clause: str,
    api_key: str,
) -> str:
    """Build a Census API data URL.

    Args:
        year: The ACS / Decennial vintage year.
        dataset: The resolved dataset path (e.g. "acs/acs5/profile").
        table: The table code (e.g. "DP05").
        geo_clause: The ``for=`` (and optionally ``in=``) clause,
            e.g. ``"zip code tabulation area:*"`` or
            ``"county:*&in=state:06"``.
        api_key: The Census Bureau API key.

    Returns:
        The fully-constructed request URL (API key included).
    """
    base = f"{_BASE_URL}/{year}/{dataset}"
    params = f"get=group({table})&for={geo_clause}&key={api_key}"
    return f"{base}?{params}"


def build_variables_url(year: int, dataset: str) -> str:
    """Build the Census API variables catalog URL.

    Args:
        year: The ACS / Decennial vintage year.
        dataset: The resolved dataset path.

    Returns:
        The variables.json endpoint URL (no API key required).
    """
    return f"{_BASE_URL}/{year}/{dataset}/variables.json"


# ---------------------------------------------------------------------------
# Security helper
# ---------------------------------------------------------------------------

_KEY_PARAM_RE = re.compile(r"([&?])key=[^&]*", re.IGNORECASE)


def scrub_url(url: str) -> str:
    """Remove the ``key=`` query parameter from a URL.

    Used when surfacing URLs in ``ComponentError`` messages or log lines so
    that the Census Bureau API key is never leaked in tracebacks.

    Args:
        url: The URL potentially containing a ``key=`` parameter.

    Returns:
        The URL with the ``key=`` parameter removed.  If the ``key=`` was
        the only query parameter the ``?`` is also removed.
    """
    # Parse to extract and rebuild cleanly.
    parsed = urlparse(url)
    qs = parse_qs(parsed.query, keep_blank_values=True)
    # Remove key (case-insensitive).
    for k in list(qs.keys()):
        if k.lower() == "key":
            del qs[k]
    new_query = urlencode(qs, doseq=True)
    scrubbed = parsed._replace(query=new_query)
    return urlunparse(scrubbed)
