"""CensusVariables component.

Fetches the ``/variables.json`` catalog for a ``(year, dataset, table)``
combination from the Census Bureau Data API and returns a ``pandas.DataFrame``
with one row per real variable.

Useful for pipeline authors building ``keep_variables:`` lists before running
the heavier ``CensusData`` component.

Example YAML (minimal):

```yaml
- CensusVariables:
    year: 2024
    table: DP05
```

Full-parameter YAML:

```yaml
- CensusVariables:
    year: 2024
    table: DP05
    survey: acs5
    dataset: null           # override; wins over prefix inference
    cache: true
    cache_dir: null         # default ~/.flowtask/cache/census
```

Output:

    self._result = pd.DataFrame   # columns: code, label, concept,
                                  #          predicate_type, group, normalized_label

Pseudo-variables (``for``, ``in``, ``ucgid``) are excluded.
Cache files are written to:
    ``<cache_dir>/<year>/<dataset>/_variables_<table>.parquet``
"""

from __future__ import annotations

import asyncio
import datetime
from pathlib import Path
from typing import Any

import aiohttp
import pandas as pd

from flowtask.components import FlowComponent
from flowtask.components._census import (
    CacheKey,
    build_variables_url,
    cache_read,
    cache_write,
    default_cache_dir,
    fetch_json,
    resolve_dataset,
)
from flowtask.components._census.transform import _build_variables_df
from flowtask.exceptions import ComponentError

# ---------------------------------------------------------------------------
# Year bounds — ACS 5-year data starts in 2009
# ---------------------------------------------------------------------------

_MIN_YEAR: int = 2009
_MAX_YEAR: int = datetime.date.today().year + 1


class CensusVariables(FlowComponent):
    """Fetch the Census variables catalog for a (year, dataset, table).

    Retrieves ``/variables.json`` from the Census Bureau Data API, filters
    out pseudo-variables, and returns a ``pandas.DataFrame`` with one row
    per real variable.

    The ``/variables.json`` endpoint is public and does not require an API key.

    See module docstring for full YAML parameter reference.
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
        # api_key_env is accepted but ignored — /variables.json is public.
        kwargs.pop("api_key_env", None)
        self.cache: bool = bool(kwargs.pop("cache", True))
        self.cache_dir: str | None = kwargs.pop("cache_dir", None)

        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

        self._session: aiohttp.ClientSession | None = None
        self._resolved_dataset: str = ""
        self._cache_dir: Path | None = None

    async def start(self, **kwargs: Any) -> bool:
        """Validate parameters, resolve dataset, create HTTP session.

        Returns:
            ``True`` on success.

        Raises:
            ComponentError: On invalid parameters.
        """
        if not self.table:
            raise ComponentError(
                "CensusVariables: 'table' parameter is required.", status=406
            )
        if self.year < _MIN_YEAR or self.year > _MAX_YEAR:
            raise ComponentError(
                f"CensusVariables: 'year' must be a 4-digit Census vintage year "
                f"(between {_MIN_YEAR} and {_MAX_YEAR}), got {self.year!r}.",
                status=406,
            )

        # Resolve dataset path (raises ComponentError for unknown prefixes).
        self._resolved_dataset = resolve_dataset(
            self.table, self.survey, self.dataset
        )

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
                    "CensusVariables: cannot create cache directory '%s': %s. "
                    "Cache will be disabled.",
                    self._cache_dir,
                    exc,
                )
                self._cache_dir = None

        # Create HTTP session.
        self._session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=120)
        )

        self._logger.info(
            "CensusVariables: year=%d, table=%s, dataset=%s",
            self.year,
            self.table,
            self._resolved_dataset,
        )
        return True

    async def run(self) -> pd.DataFrame:
        """Fetch the variables catalog.

        Returns:
            A ``pd.DataFrame`` with columns:
            ``code, label, concept, predicate_type, group, normalized_label``.
        """
        cache_key = CacheKey(
            year=self.year,
            dataset=self._resolved_dataset,
            table=f"_variables_{self.table}",
            geography="zcta",  # sentinel — variables are not geography-specific
            state=None,
        )

        # Cache check.
        if self.cache and self._cache_dir is not None:
            cached = cache_read(cache_key, self._cache_dir, self._logger)
            if cached is not None:
                self._logger.info(
                    "CensusVariables: cache hit for %s/%s/%s",
                    self.year, self._resolved_dataset, self.table
                )
                self._result = cached
                self.add_metric("census_variables_returned", len(cached))
                return self._result

        # Fetch from API.
        url = build_variables_url(self.year, self._resolved_dataset)
        self._logger.info("CensusVariables: fetching %s", url)
        raw = await fetch_json(self._session, url, self._logger)

        variables_df = _build_variables_df(raw)

        # Cache write.
        if self.cache and self._cache_dir is not None:
            cache_write(variables_df, cache_key, self._cache_dir, self._logger)

        self._result = variables_df
        self.add_metric("census_variables_returned", len(variables_df))
        return self._result

    async def close(self) -> None:
        """Close the aiohttp session if open."""
        if self._session is not None and not self._session.closed:
            await self._session.close()
            self._session = None
