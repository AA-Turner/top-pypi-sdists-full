from collections.abc import Callable
import asyncio
import random

import pandas as pd

from ...exceptions import ComponentError, ConfigError
from ...interfaces import HTTPService, SeleniumService
from ...interfaces.flow import FlowComponent
from ...interfaces.selenium_service import VirtualDisplay
from .retailers import RETAILERS


def _has_reference_data(data) -> bool:
    return isinstance(data, pd.DataFrame) and not data.empty


def _match_key(df: pd.DataFrame, columns: list) -> pd.Series:
    key = None
    for col in columns:
        part = df[col].astype(str).str.lower().str.strip()
        key = part if key is None else key + "|" + part
    return key


class ServiceScraperStores(FlowComponent, SeleniumService, HTTPService):
    """
    ServiceScraperStores.

    Overview:

    Generic public store-locator scraper. Drives a Selenium Chrome session
    (behind a virtual Xvfb display when `headless: false`, for sites that
    block headless Chrome outright) over a set of geo-coordinate seeds
    taken from the previous step's dataframe, delegates the actual
    per-site search to a small per-retailer strategy (see
    `retailers/base.py`), and reconciles the scraped stores against that
    reference dataframe (match_status: matched / new_on_web /
    missing_on_web).

    .. table:: Properties
    :widths: auto

    +------------------------+----------+------------------------------------------------------------------------+
    | Name                   | Required | Description                                                             |
    +------------------------+----------+------------------------------------------------------------------------+
    | scrapper (str)         |   Yes    | Registered retailer key (e.g. "verizon"). See retailers/__init__.py.   |
    +------------------------+----------+------------------------------------------------------------------------+
    | headless (bool)        |   No     | Run Chrome headless (default True). Set False for sites that block     |
    |                        |          | headless Chrome - requires the `Xvfb` binary on the host.              |
    +------------------------+----------+------------------------------------------------------------------------+
    | range_miles (int)      |   No     | Search radius passed to the retailer's search (default 20). Only      |
    |                        |          | meaningful for geo-radius strategies (e.g. Verizon).                   |
    +------------------------+----------+------------------------------------------------------------------------+
    | max_stores (int)       |   No     | Max stores per search request (default 25). Only meaningful for       |
    |                        |          | geo-radius strategies (e.g. Verizon).                                  |
    +------------------------+----------+------------------------------------------------------------------------+
    | request_delay (float)  |   No     | Seconds to sleep between search requests (default 1.0). Bump this up  |
    |                        |          | for rate-sensitive sites.                                              |
    +------------------------+----------+------------------------------------------------------------------------+
    | match_columns          |   No     | Canonical (post field_map) columns on the SCRAPED side used to build   |
    | (list)                 |          | the reconciliation key (default ["store_name", "city", "state_code"]). |
    +------------------------+----------+------------------------------------------------------------------------+
    | reference_match_columns|   No     | The reference dataframe's corresponding columns, same order/length as  |
    | (list)                 |          | match_columns (default ["outlet_name", "city", "state_code"]). E.g.    |
    |                        |          | ["store_number"]/["store_number"] for an exact-ID match instead of a   |
    |                        |          | fuzzy name+city+state one, when the reference file has a reliable ID.  |
    +------------------------+----------+------------------------------------------------------------------------+
    | args (dict)            |   No     | Extra retailer-specific kwargs forwarded to the strategy's             |
    |                        |          | get_seeds()/search()/postprocess() (e.g. {channel_filter: "IND"}).     |
    +------------------------+----------+------------------------------------------------------------------------+

    A previous component's dataframe is OPTIONAL. If present, it's both
    the source of search seeds for geo-radius strategies (see
    VerizonStrategy.get_seeds) and the reference reconciled against
    (match_status: matched/new_on_web/missing_on_web). Strategies that
    crawl a fixed, retailer-defined seed list instead (e.g.
    TractorSupplyStrategy, which pages through every US state regardless
    of what's upstream) ignore it, and the result is simply the scraped
    stores with no reconciliation.

    Return:
    - DataFrame: the scraped stores, merged with the reference dataframe
      and a `match_status` column when one was supplied upstream.

    Example (reconciled against an upstream reference file):

    ```yaml
    - ServiceScraperStores:
        scrapper: verizon
        headless: false
        range_miles: 20
        max_stores: 25
        request_delay: 1.0
        args:
          channel_filter: "IND"
    ```

    Example (reconciled by an exact reference ID instead of fuzzy name+city+state):

    ```yaml
    - ServiceScraperStores:
        scrapper: tractorsupply
        headless: false
        request_delay: 6.0
        match_columns:
          - store_number
        reference_match_columns:
          - store_number
    ```

    Example (full retailer-defined crawl, no reference file):

    ```yaml
    - ServiceScraperStores:
        scrapper: tractorsupply
        headless: false
        request_delay: 6.0
    ```

    Adding a new retailer: write a `RetailerStrategy` subclass in
    `retailers/<name>.py` and register it in `retailers/__init__.py`'s
    `RETAILERS` dict - no changes needed here. See `retailers/verizon.py`,
    `retailers/tractor_supply.py` and `retailers/costco.py` for three
    different, complete, working examples (geo-radius search API,
    one-page-per-state crawl, and two-level directory+detail-page crawl,
    respectively).
    """  # noqa: E501

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ) -> None:
        self.scrapper_name: str = kwargs.get('scrapper', None)
        self.headless: bool = kwargs.get('headless', True)
        self.range_miles: int = kwargs.get('range_miles', 20)
        self.max_stores: int = kwargs.get('max_stores', 25)
        self.request_delay: float = kwargs.get('request_delay', 1.0)
        self.match_columns: list = kwargs.get('match_columns', ['store_name', 'city', 'state_code'])
        self.reference_match_columns: list = kwargs.get('reference_match_columns', ['outlet_name', 'city', 'state_code'])
        self.strategy_args: dict = kwargs.get('args', {}) or {}
        self.strategy = None
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs) -> bool:
        """Initialize the component and validate required parameters."""
        if self.previous:
            self.data = self.input

        strategy_cls = RETAILERS.get(self.scrapper_name)
        if strategy_cls is None:
            raise ConfigError(
                f"ServiceScraperStores: unknown scrapper {self.scrapper_name!r}. "
                f"Registered scrappers: {list(RETAILERS)}"
            )
        self.strategy = strategy_cls()
        return True

    async def _scrape_seeds(self, seeds: list) -> dict:
        all_stores: dict = {}
        self._logger.notice(f"ServiceScraperStores({self.scrapper_name}): starting Chrome driver")
        driver = await self.get_driver()
        if self.strategy.store_locator_url:
            self._logger.notice(
                f"ServiceScraperStores({self.scrapper_name}): loading {self.strategy.store_locator_url}"
            )
            driver.get(self.strategy.store_locator_url)
            await asyncio.sleep(4)
        total = len(seeds)
        for idx, seed in enumerate(seeds, start=1):
            self._logger.notice(
                f"ServiceScraperStores({self.scrapper_name}): seed {idx}/{total} -> {seed!r}"
            )
            try:
                stores = self.strategy.search(
                    driver, seed,
                    range_miles=self.range_miles, max_stores=self.max_stores,
                    **self.strategy_args
                )
            except Exception as err:
                self._logger.warning(f"Search failed for seed {seed!r}: {err}")
                continue
            new_count = 0
            for store in stores:
                key = self.strategy.store_key(store)
                if key:
                    all_stores[key] = store
                    new_count += 1
            self._logger.notice(
                f"ServiceScraperStores({self.scrapper_name}): seed {idx}/{total} -> "
                f"{new_count} stores found (running total: {len(all_stores)})"
            )
            await asyncio.sleep(self.request_delay + random.uniform(0, 0.5))
        return all_stores

    async def run(self):
        """Search every seed, then reconcile against any reference data."""
        has_reference = _has_reference_data(self.data)
        seeds = self.strategy.get_seeds(self.data if has_reference else pd.DataFrame(), **self.strategy_args)
        self._logger.notice(
            f"ServiceScraperStores({self.scrapper_name}): searching {len(seeds)} seeds"
            + (f" (from {len(self.data)} reference stores)" if has_reference else "")
        )

        try:
            if not self.headless:
                with VirtualDisplay():
                    all_stores = await self._scrape_seeds(seeds)
            else:
                all_stores = await self._scrape_seeds(seeds)
        except Exception as err:
            self._logger.error(f"Error while scraping {self.scrapper_name}: {err}")
            raise ComponentError(
                f"ServiceScraperStores: error while scraping {self.scrapper_name}: {err}"
            ) from err
        finally:
            self.close_driver()

        scraped = pd.DataFrame(list(all_stores.values()))
        scraped = scraped.rename(columns=self.strategy.field_map)
        keep_cols = [c for c in self.strategy.field_map.values() if c in scraped.columns]
        scraped = scraped[keep_cols]
        for coord_col in ("latitude", "longitude"):
            if coord_col in scraped.columns:
                scraped[coord_col] = pd.to_numeric(scraped[coord_col], errors="coerce")
        scraped = self.strategy.postprocess(scraped, **self.strategy_args)

        if has_reference:
            reference = self.data.copy()
            has_match_cols = all(c in scraped.columns for c in self.match_columns)
            if not scraped.empty and has_match_cols:
                scraped["_match_key"] = _match_key(scraped, self.match_columns)
                reference["_match_key"] = _match_key(reference, self.reference_match_columns)
                # Pull in reference-only columns (e.g. an Excel's market_desc,
                # subcluster_desc, ...) without duplicating anything scraped
                # already provides (city, state_code, latitude, longitude, ...).
                reference_cols = [
                    c for c in reference.columns
                    if c == "_match_key" or c not in scraped.columns
                ]
                merged = scraped.merge(
                    reference[reference_cols], on="_match_key", how="outer", indicator=True
                )
                merged["match_status"] = merged["_merge"].map({
                    "both": "matched",
                    "left_only": "new_on_web",
                    "right_only": "missing_on_web",
                })
                merged = merged.drop(columns=["_merge", "_match_key"])
            else:
                merged = reference
                merged["match_status"] = "missing_on_web"
        else:
            merged = scraped

        if "store_status" in merged.columns:
            merged["store_status"] = merged["store_status"].apply(self.strategy.normalize_store_status)

        match_summary = ""
        if "match_status" in merged.columns:
            match_summary = (
                f" | matched={(merged['match_status'] == 'matched').sum()} "
                f"new_on_web={(merged['match_status'] == 'new_on_web').sum()} "
                f"missing_on_web={(merged['match_status'] == 'missing_on_web').sum()}"
            )
        self._logger.notice(
            f"ServiceScraperStores({self.scrapper_name}): scraped {len(scraped)} stores from "
            f"the web{match_summary}"
        )
        self.add_metric("SCRAPED", len(scraped))
        self.add_metric("NUMROWS", len(merged.index))
        self.add_metric("NUMCOLS", len(merged.columns))
        self._result = merged

        if self._debug is True:
            self._print_data_(self._result, "ServiceScraperStores Results")

        return self._result

    async def close(self):
        """Clean up resources."""
        return True
