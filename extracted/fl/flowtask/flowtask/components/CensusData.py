"""CensusData component.

Fetches a US Census ACS / Decennial table as a ``pandas.DataFrame`` and
caches the result to disk so repeat pipeline runs are free.

Example YAML (minimal):

```yaml
- CensusData:
    year: 2024
    table: DP05
```

Full-parameter YAML:

```yaml
- CensusData:
    year: 2024
    table: DP05
    survey: acs5
    dataset: null           # override; wins over prefix inference
    geography: zcta         # one of: zcta, state, county, tract, block_group, place
    state_filter: null      # required for sub-state geos; "*" fans out all 52
    keep_suffixes:          # columns to keep (anchored at end-of-name)
      - E
      - PE
    api_key_env: CENSUS_BUREAU_API_KEY   # env var override
    cache: true
    cache_dir: null         # default ~/.flowtask/cache/census
    max_concurrent_requests: 8
```

Output:

    self._result = {
        "data": pd.DataFrame,       # the table data
        "variables": pd.DataFrame,  # the variables catalog
    }

Downstream components access ``component.result["data"]``.
"""

from __future__ import annotations

import asyncio
import datetime
import os
from pathlib import Path
from typing import Any

import aiohttp
import pandas as pd

from flowtask.components import FlowComponent
from flowtask.components._census import (
    STATE_CODES,
    CacheKey,
    apply_sentinels,
    build_data_url,
    build_variables_url,
    cache_read,
    cache_write,
    default_cache_dir,
    fan_out,
    fetch_json,
    filter_by_suffix,
    normalize_label,
    rename_geography_column,
    resolve_dataset,
    scrub_url,
)
from flowtask.components._census.transform import _build_variables_df
from flowtask.exceptions import ComponentError

try:
    from flowtask.conf import CENSUS_BUREAU_API_KEY as _DEFAULT_API_KEY
except ImportError:
    _DEFAULT_API_KEY = None

# ---------------------------------------------------------------------------
# Year bounds — ACS 5-year data starts in 2009
# ---------------------------------------------------------------------------

_MIN_YEAR: int = 2009
_MAX_YEAR: int = datetime.date.today().year + 1

# ---------------------------------------------------------------------------
# Geography geo-clause builders
# ---------------------------------------------------------------------------

_GEO_CLAUSES: dict[str, str] = {
    "zcta": "zip code tabulation area:*",
    "state": "state:*",
    "county": "county:*",
    "tract": "tract:*",
    "block_group": "block group:*",
    "place": "place:*",
}

_SUB_STATE_GEOS: frozenset[str] = frozenset({"county", "tract", "block_group", "place"})

_CENSUS_API_SIGNUP_URL = "https://api.census.gov/data/key_signup.html"


def _build_geo_clause(geography: str, state_fips: str | None) -> str:
    """Build the ``for=`` (and optionally ``in=``) geo clause for the Census API.

    Args:
        geography: The geography type (e.g. ``"zcta"``, ``"county"``).
        state_fips: FIPS code of the state to restrict to, or ``None`` for
            nationwide / ZCTA requests.

    Returns:
        The geo clause string, e.g.
        ``"zip code tabulation area:*"`` or
        ``"county:*&in=state:06"``.
    """
    base = _GEO_CLAUSES.get(geography, geography)
    if state_fips is not None and geography in _SUB_STATE_GEOS:
        return f"{base}&in=state:{state_fips}"
    return base


def _rows_to_df(rows: list[list[str]]) -> pd.DataFrame:
    """Convert the Census API response (header row + data rows) to a DataFrame.

    Args:
        rows: A list of lists; the first element is the header row.

    Returns:
        A DataFrame with string columns, ready for numeric coercion.
    """
    if not rows or len(rows) < 2:
        return pd.DataFrame()
    headers = rows[0]
    data = rows[1:]
    return pd.DataFrame(data, columns=headers)


# ---------------------------------------------------------------------------
# Component
# ---------------------------------------------------------------------------


class CensusData(FlowComponent):
    """Fetch a US Census ACS / Decennial table as a pandas DataFrame.

    Downloads the requested table from the Census Bureau Data API
    (``api.census.gov``), applies sentinel-to-NaN mapping, filters columns
    by suffix, renames the geography column, and caches the result to disk
    as a Parquet file.

    The variables catalog for the table is fetched and cached in parallel
    and exposed via ``self._result["variables"]``.

Example:

```yaml
- CensusData:
    year: 2024
    table: DP05
    survey: acs5
    dataset: null           # override; wins over prefix inference
    geography: zcta         # one of: zcta, state, county, tract, block_group, place
    state_filter: null      # required for sub-state geos; "*" fans out all 52
    keep_suffixes:          # columns to keep (anchored at end-of-name)
      - E
      - PE
    api_key_env: CENSUS_BUREAU_API_KEY   # env var override
    cache: true
    cache_dir: null         # default ~/.flowtask/cache/census
    max_concurrent_requests: 8
```

Output:

    self._result = {
        "data": pd.DataFrame,       # the table data
        "variables": pd.DataFrame,  # the variables catalog
    }
    """

    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Any = None,
        stat: Any = None,
        **kwargs: Any,
    ) -> None:
        self.year: int = int(kwargs.pop("year", 2024))
        self.table: str = str(kwargs.pop("table", "")).upper()
        self.survey: str = str(kwargs.pop("survey", "acs5"))
        self.dataset: str | None = kwargs.pop("dataset", None)
        self.geography: str = str(kwargs.pop("geography", "zcta"))
        self.state_filter: str | None = kwargs.pop("state_filter", None)
        self.keep_suffixes: list[str] = list(kwargs.pop("keep_suffixes", ["E", "PE"]))
        self.api_key_env: str = str(kwargs.pop("api_key_env", "CENSUS_BUREAU_API_KEY"))
        self.cache: bool = bool(kwargs.pop("cache", True))
        self.cache_dir: str | None = kwargs.pop("cache_dir", None)
        self.max_concurrent_requests: int = int(
            kwargs.pop("max_concurrent_requests", 8)
        )

        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

        self._session: aiohttp.ClientSession | None = None
        self._semaphore: asyncio.Semaphore | None = None
        self._resolved_dataset: str = ""
        self._api_key: str | None = None
        self._cache_dir: Path | None = None

    async def start(self, **kwargs: Any) -> bool:
        """Validate parameters, resolve dataset, create HTTP session and semaphore.

        Returns:
            ``True`` on success.

        Raises:
            ComponentError: On invalid parameters or missing API key.
        """
        if not self.table:
            raise ComponentError("CensusData: 'table' parameter is required.", status=406)
        if self.year < _MIN_YEAR or self.year > _MAX_YEAR:
            raise ComponentError(
                f"CensusData: 'year' must be a 4-digit Census vintage year "
                f"(between {_MIN_YEAR} and {_MAX_YEAR}), got {self.year!r}.",
                status=406,
            )
        valid_geos = set(_GEO_CLAUSES.keys())
        if self.geography not in valid_geos:
            raise ComponentError(
                f"CensusData: 'geography' must be one of {sorted(valid_geos)}, "
                f"got {self.geography!r}.",
                status=406,
            )
        if not self.keep_suffixes:
            raise ComponentError(
                "CensusData: 'keep_suffixes' must not be empty.  "
                "Specify at least ['E'] to keep estimate columns.",
                status=406,
            )

        # Sub-state geography requires state_filter.
        if self.geography in _SUB_STATE_GEOS and self.state_filter is None:
            raise ComponentError(
                f"CensusData: geography '{self.geography}' requires 'state_filter' "
                f"(a FIPS code, e.g. '06', or '*' to fan out all 52 jurisdictions).",
                status=406,
            )

        # block_group + "*" is not supported (memory risk).
        if self.geography == "block_group" and self.state_filter == "*":
            raise ComponentError(
                "CensusData: geography='block_group' with state_filter='*' is not "
                "supported in v1 due to memory constraints.  Provide an explicit "
                "FIPS code instead (e.g. state_filter: '06').",
                status=406,
            )

        # ZCTA + state_filter: warn and ignore.
        if self.geography == "zcta" and self.state_filter is not None:
            self._logger.warning(
                "CensusData: geography='zcta' does not support state_filter; "
                "the filter will be ignored (ZCTAs cross state lines)."
            )

        # Resolve dataset path.
        self._resolved_dataset = resolve_dataset(
            self.table, self.survey, self.dataset
        )

        # Resolve API key.
        api_key: str | None = os.environ.get(self.api_key_env) or _DEFAULT_API_KEY
        if not api_key:
            raise ComponentError(
                f"CensusData: API key not found.  Set the '{self.api_key_env}' "
                f"environment variable.  Sign up at {_CENSUS_API_SIGNUP_URL}",
                status=401,
            )
        self._api_key = api_key

        # Resolve cache directory.
        if self.cache:
            if self.cache_dir:
                self._cache_dir = Path(self.cache_dir)
            else:
                self._cache_dir = default_cache_dir()
            try:
                self._cache_dir.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                self._logger.warning(
                    "CensusData: cannot create cache directory '%s': %s. "
                    "Cache will be disabled.",
                    self._cache_dir,
                    exc,
                )
                self._cache_dir = None

        # Create HTTP session and semaphore.
        self._session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=300)
        )
        self._semaphore = asyncio.Semaphore(self.max_concurrent_requests)

        self._logger.info(
            "CensusData: year=%d, table=%s, dataset=%s, geography=%s",
            self.year,
            self.table,
            self._resolved_dataset,
            self.geography,
        )
        return True

    async def run(self) -> dict[str, pd.DataFrame]:
        """Fetch the Census table and variables catalog.

        Returns:
            ``{"data": pd.DataFrame, "variables": pd.DataFrame}``

        Raises:
            ComponentError: On API errors or data issues.
        """
        data_df = await self._fetch_data()
        variables_df = await self._fetch_variables()

        self._result = {"data": data_df, "variables": variables_df}

        # When export_dataframe is set, expose only the data DataFrame so that
        # downstream components like PandasToFile or TableOutput can consume it directly.
        if getattr(self, "export_dataframe", False):
            self._result = data_df

        # Emit observability metrics.
        rows_fetched = len(data_df) if not data_df.empty else 0
        self.add_metric("census_rows_fetched", rows_fetched)
        self.add_metric("census_variables_count", len(variables_df))

        return self._result

    async def _fetch_data(self) -> pd.DataFrame:
        """Fetch and transform the Census table data.

        Returns:
            The fully-processed DataFrame.
        """
        # Determine the set of (geo_clause, state, cache_key) tuples.
        if self.geography == "zcta" or (
            self.geography not in _SUB_STATE_GEOS
        ):
            # Single nationwide request (ZCTA or state-level).
            shards = [(
                _build_geo_clause(self.geography, None),
                None,
            )]
        elif self.state_filter == "*":
            # Fan-out across all 52 jurisdictions.
            shards = [
                (_build_geo_clause(self.geography, fips), fips)
                for fips in STATE_CODES
            ]
        else:
            # Single state.
            shards = [(
                _build_geo_clause(self.geography, self.state_filter),
                self.state_filter,
            )]

        shard_dfs: list[pd.DataFrame] = []

        if self.state_filter == "*" and self.geography in _SUB_STATE_GEOS:
            # Fan-out path.
            shard_dfs = await self._fan_out_data(shards)
        else:
            # Single-shard path.
            geo_clause, state = shards[0]
            cache_key = CacheKey(
                year=self.year,
                dataset=self._resolved_dataset,
                table=self.table,
                geography=self.geography,
                state=state,
            )
            df = await self._fetch_or_cache_shard(geo_clause, cache_key)
            shard_dfs = [df]

        combined = pd.concat(shard_dfs, ignore_index=True) if len(shard_dfs) > 1 else shard_dfs[0]

        # Numeric coercion → sentinels → suffix filter → rename geo column.
        combined = self._coerce_and_clean(combined)
        return combined

    async def _fan_out_data(
        self, shards: list[tuple[str, str | None]]
    ) -> list[pd.DataFrame]:
        """Fan-out across all states with per-shard cache checks.

        Args:
            shards: List of (geo_clause, state_fips) pairs.

        Returns:
            List of DataFrames, one per shard.
        """
        # Check cache for each shard first; collect states that need fetching.
        cached_results: dict[str | None, pd.DataFrame] = {}
        states_to_fetch: list[str] = []
        cache_hits: int = 0
        cache_misses: int = 0

        for geo_clause, state in shards:
            if state is None:
                continue
            cache_key = CacheKey(
                year=self.year,
                dataset=self._resolved_dataset,
                table=self.table,
                geography=self.geography,
                state=state,
            )
            if self._cache_dir is not None:
                cached = cache_read(cache_key, self._cache_dir, self._logger)
                if cached is not None:
                    cached_results[state] = cached
                    cache_hits += 1
                    continue
            states_to_fetch.append(state)
            cache_misses += 1

        self.add_metric("census_cache_hits", cache_hits)
        self.add_metric("census_cache_misses", cache_misses)
        self.add_metric("census_states_fetched", len(states_to_fetch))

        # Fetch missing states via fan_out.
        if states_to_fetch:
            raw_payloads = await fan_out(
                self._session,
                lambda s: build_data_url(
                    self.year,
                    self._resolved_dataset,
                    self.table,
                    _build_geo_clause(self.geography, s),
                    self._api_key,
                ),
                states_to_fetch,
                self._semaphore,
                self._logger,
            )
            for state, rows in zip(states_to_fetch, raw_payloads):
                df = _rows_to_df(rows)
                if self._cache_dir is not None:
                    cache_key = CacheKey(
                        year=self.year,
                        dataset=self._resolved_dataset,
                        table=self.table,
                        geography=self.geography,
                        state=state,
                    )
                    cache_write(df, cache_key, self._cache_dir, self._logger)
                cached_results[state] = df

        # Reassemble in original state order.
        result = []
        for _, state in shards:
            df = cached_results.get(state)
            if df is not None:
                result.append(df)
        return result

    async def _fetch_or_cache_shard(
        self, geo_clause: str, cache_key: CacheKey
    ) -> pd.DataFrame:
        """Fetch one shard (or return from cache).

        Args:
            geo_clause: The Census API geo clause.
            cache_key: The cache key for this shard.

        Returns:
            The raw (string-typed) DataFrame for this shard.
        """
        # Cache check.
        if self.cache and self._cache_dir is not None:
            cached = cache_read(cache_key, self._cache_dir, self._logger)
            if cached is not None:
                self._logger.info(
                    "CensusData: cache hit for %s/%s/%s (state=%s)",
                    self.year, self._resolved_dataset, self.table, cache_key.state
                )
                self.add_metric("census_cache_hits", 1)
                return cached

        self.add_metric("census_cache_misses", 1)

        # HTTP fetch.
        url = build_data_url(
            self.year,
            self._resolved_dataset,
            self.table,
            geo_clause,
            self._api_key,
        )
        self._logger.info(
            "CensusData: fetching %s", scrub_url(url)
        )
        async with self._semaphore:
            rows = await fetch_json(self._session, url, self._logger)

        df = _rows_to_df(rows)

        # Cache write.
        if self.cache and self._cache_dir is not None:
            cache_write(df, cache_key, self._cache_dir, self._logger)

        return df

    def _coerce_and_clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Coerce numeric columns, map sentinels, filter by suffix, rename geo.

        Args:
            df: The raw string-typed DataFrame from the Census API.

        Returns:
            The cleaned, renamed DataFrame.
        """
        if df.empty:
            return df

        # Determine the always-keep columns (non-variable columns).
        geo_col_candidates = list(
            {"GEO_ID", "NAME", "state", "county", "tract",
             "zip code tabulation area", "block group", "place",
             self.geography}
        )
        always_keep = [c for c in df.columns if c in set(geo_col_candidates)]

        # Coerce numeric.
        variable_cols = [c for c in df.columns if c not in set(always_keep)]
        for col in variable_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Apply sentinels.
        df = apply_sentinels(df, self._logger)

        # Suffix filter.
        df = filter_by_suffix(df, self.keep_suffixes, always_keep)

        # Rename geography column.
        df = rename_geography_column(df, self.geography)

        return df.reset_index(drop=True)

    async def _fetch_variables(self) -> pd.DataFrame:
        """Fetch and cache the variables catalog for the current dataset/table.

        Returns:
            DataFrame with columns:
            ``code, label, concept, predicate_type, group, normalized_label``.
        """
        cache_key = CacheKey(
            year=self.year,
            dataset=self._resolved_dataset,
            table=f"_variables_{self.table}",
            geography="zcta",  # sentinel — variables are not geography-specific
            state=None,
        )

        if self.cache and self._cache_dir is not None:
            cached = cache_read(cache_key, self._cache_dir, self._logger)
            if cached is not None:
                return cached

        url = build_variables_url(self.year, self._resolved_dataset)
        self._logger.info("CensusData: fetching variables catalog from %s", url)
        raw = await fetch_json(self._session, url, self._logger)
        variables_df = _build_variables_df(raw)

        if self.cache and self._cache_dir is not None:
            cache_write(variables_df, cache_key, self._cache_dir, self._logger)

        return variables_df

    async def close(self) -> None:
        """Close the aiohttp session if open."""
        if self._session is not None and not self._session.closed:
            await self._session.close()
            self._session = None
