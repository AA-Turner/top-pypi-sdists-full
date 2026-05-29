"""OpenStreetMap component.

Queries the public Overpass API for points of interest inside US zipcode
postal areas, given a list of tag filters (e.g. ``shop=mall``,
``building=retail``, ``name~"Mall|Shopping Center|Plaza|Outlet"``).
Runs queries asynchronously with a bounded semaphore, retries on
rate-limit/server errors, and de-duplicates results by name and
proximity before returning a single merged ``pandas.DataFrame``.
"""
from __future__ import annotations

import asyncio
import random
import re
from collections.abc import Callable
from typing import Any, Optional

import aiohttp
import pandas as pd
from aiohttp.resolver import AsyncResolver
from geopy.distance import geodesic

from ..exceptions import ComponentError, DataNotFound
from . import FlowComponent


DEFAULT_OVERPASS_URL = "https://overpass-api.de/api/interpreter"

_TAG_EQ_RE = re.compile(r'^\s*([A-Za-z0-9_:]+)\s*=\s*(.+?)\s*$')
_TAG_REGEX_RE = re.compile(
    r'^\s*([A-Za-z0-9_:]+)\s*~\s*"(.+)"\s*(?:,\s*([a-zA-Z]+))?\s*$'
)
_NAME_NOISE_RE = re.compile(
    r'\b(mall|shopping\s+center|shopping\s+centre|plaza|outlets?|the)\b',
    re.IGNORECASE,
)
_NON_ALNUM_RE = re.compile(r'[^a-z0-9]+')
_DIGITS_RE = re.compile(r'\D+')


class OpenStreetMap(FlowComponent):
    """OpenStreetMap (Overpass API) Component.

    Queries the Overpass API for OSM elements inside US postal-code
    areas. Iterates over every zipcode in the input dataframe, applying
    each user-provided tag filter, then merges and de-duplicates the
    results.

    Example:

    ```yaml
    OpenStreetMap:
      zipcode_column: zipcode
      lat_column: latitude
      lon_column: longitude
      search_radius_meters: 8000
      filters:
        - shop=mall
        - building=retail
        - 'name~"Mall|Shopping Center|Plaza|Outlet"'
      semaphore_limit: 4
      dedup_radius_meters: 100
      dedup_use_phone: true
    ```

    When ``lat_column`` and ``lon_column`` are provided, a radius-based
    query path (``around:<radius>,<lat>,<lon>``) is added to each
    Overpass request alongside the area and tag paths.  This catches
    POIs near the ZIP centroid even when no ``boundary=postal_code``
    relation exists in OSM and the POI lacks an ``addr:postcode`` tag.
    """

    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ) -> None:
        self.zipcode_column: str = kwargs.pop('zipcode_column', 'zipcode')
        self.country_code: str = kwargs.pop('country_code', 'US')
        self.filters: list[str] = kwargs.pop('filters', []) or []
        self.element_types: list[str] = kwargs.pop(
            'element_types', ['node', 'way', 'relation']
        )
        self.semaphore_limit: int = int(kwargs.pop('semaphore_limit', 4))
        self.request_timeout: int = int(kwargs.pop('request_timeout', 180))
        self.overpass_url: str = kwargs.pop('overpass_url', DEFAULT_OVERPASS_URL)
        self.dedup_radius_meters: float = float(
            kwargs.pop('dedup_radius_meters', 100.0)
        )
        self.dedup_use_phone: bool = bool(kwargs.pop('dedup_use_phone', True))
        self.max_retries: int = int(kwargs.pop('max_retries', 3))
        self.backoff_base: float = float(kwargs.pop('backoff_base', 2.0))
        self.chunk_size: int = int(kwargs.pop('chunk_size', 50))
        self.lat_column: Optional[str] = kwargs.pop('lat_column', None)
        self.lon_column: Optional[str] = kwargs.pop('lon_column', None)
        self.search_radius_meters: int = int(
            kwargs.pop('search_radius_meters', 8000)
        )

        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

        self._semaphore: Optional[asyncio.Semaphore] = None
        self._session: Optional[aiohttp.ClientSession] = None
        self._counter: int = 0
        self._failed: int = 0

    def _evaluate_input(self) -> None:
        if self.previous:
            self.data = self.input
        elif self.input is not None:
            self.data = self.input

    async def start(self, **kwargs) -> bool:
        self._evaluate_input()
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError(
                "OpenStreetMap requires a pandas DataFrame as input",
                status=404,
            )
        if self.zipcode_column not in self.data.columns:
            raise DataNotFound(
                f"Missing '{self.zipcode_column}' column in the input DataFrame."
            )
        if not self.filters:
            raise ComponentError(
                "OpenStreetMap requires at least one entry in 'filters'."
            )
        self._counter = 0
        self._failed = 0
        self._semaphore = asyncio.Semaphore(self.semaphore_limit)

        timeout = aiohttp.ClientTimeout(total=self.request_timeout + 30)
        resolver = AsyncResolver(nameservers=["1.1.1.1", "8.8.8.8"])
        connector = aiohttp.TCPConnector(limit=self.semaphore_limit * 2, resolver=resolver)
        self._session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            trust_env=True,
        )
        return True

    async def close(self) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()
            self._session = None

    @staticmethod
    def _normalize_filter(osm_filter: str) -> str:
        """Translate a user-friendly filter into an Overpass bracket filter."""
        cond = osm_filter.strip()
        if not cond:
            raise ComponentError("Empty Overpass filter provided.")
        if cond.startswith('['):
            return cond
        m = _TAG_REGEX_RE.match(cond)
        if m:
            key, pattern, flags = m.group(1), m.group(2), m.group(3)
            if flags:
                return f'["{key}"~"{pattern}",{flags}]'
            return f'["{key}"~"{pattern}"]'
        m = _TAG_EQ_RE.match(cond)
        if m:
            key, value = m.group(1), m.group(2).strip().strip('"')
            return f'["{key}"="{value}"]'
        raise ComponentError(
            f"Unrecognized Overpass filter syntax: {osm_filter!r}"
        )

    def _build_query(
        self,
        zipcode: str,
        osm_filter: str,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
    ) -> str:
        bracket = self._normalize_filter(osm_filter)
        area_lines = '\n  '.join(
            f'{etype}{bracket}(area.zip)(area.country);'
            for etype in self.element_types
        )
        postcode_tag = f'["addr:postcode"="{zipcode}"]'
        tag_lines = '\n  '.join(
            f'{etype}{bracket}{postcode_tag}(area.country);'
            for etype in self.element_types
        )
        if lat is not None and lon is not None:
            around = f'(around:{self.search_radius_meters},{lat},{lon})'
            radius_lines = '\n  '.join(
                f'{etype}{bracket}{around};'
                for etype in self.element_types
            )
            union_body = f'{area_lines}\n  {tag_lines}\n  {radius_lines}'
        else:
            union_body = f'{area_lines}\n  {tag_lines}'
        return (
            f'[out:json][timeout:{self.request_timeout}];\n'
            f'area["ISO3166-1"="{self.country_code}"][admin_level=2]->.country;\n'
            f'area["boundary"="postal_code"]["postal_code"="{zipcode}"]->.zip;\n'
            f'(\n  {union_body}\n);\n'
            f'out center tags;\n'
        )

    async def _post_overpass(self, query: str) -> Optional[dict]:
        """POST a query to Overpass with retry/backoff on rate limits."""
        attempt = 0
        while True:
            retry_after: Optional[str] = None
            status: Optional[int] = None
            try:
                async with self._session.post(
                    self.overpass_url,
                    data={"data": query},
                ) as response:
                    status = response.status
                    if status == 200:
                        return await response.json()
                    if status in (429, 502, 503, 504):
                        body = await response.text()
                        retry_after = response.headers.get('Retry-After')
                        self._logger.warning(
                            f"Overpass {status} (attempt {attempt + 1}): "
                            f"{body[:200]}"
                        )
                    else:
                        body = await response.text()
                        self._logger.error(
                            f"Overpass error {status}: {body[:300]}"
                        )
                        return None
            except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
                self._logger.warning(
                    f"Overpass network error (attempt {attempt + 1}): {exc}"
                )
            attempt += 1
            if attempt > self.max_retries:
                return None
            # Pick the longest sensible delay: Retry-After hint if the server
            # gave one, otherwise exponential backoff. Rate-limit responses
            # (429) get a longer floor to give the Overpass slot pool time to
            # recover. Small random jitter avoids retry herds when many tasks
            # were throttled at the same instant.
            delay = self.backoff_base ** attempt
            if retry_after:
                try:
                    delay = max(delay, float(retry_after))
                except (TypeError, ValueError):
                    pass
            if status == 429:
                delay = max(delay, 10.0 * attempt)
            delay += random.uniform(0, 1.5)
            await asyncio.sleep(delay)

    def _flatten_element(
        self,
        element: dict,
        zipcode: str,
        osm_filter: str,
    ) -> Optional[dict]:
        tags = element.get('tags') or {}
        lat = element.get('lat')
        lon = element.get('lon')
        if lat is None or lon is None:
            center = element.get('center') or {}
            lat = center.get('lat')
            lon = center.get('lon')
        housenumber = tags.get('addr:housenumber') or tags.get('housenumber')
        street = tags.get('addr:street')
        if housenumber and street:
            street_address = f"{housenumber} {street}"
        elif tags.get('addr:full'):
            street_address = tags.get('addr:full')
        else:
            street_address = street or None
        country = tags.get('addr:country') or self.country_code
        return {
            'zipcode': zipcode,
            'matched_filter': osm_filter,
            'osm_type': element.get('type'),
            'osm_id': element.get('id'),
            'name': tags.get('name'),
            'brand': tags.get('brand'),
            'brand_wikidata': tags.get('brand:wikidata'),
            'operator': tags.get('operator'),
            'shop': tags.get('shop'),
            'amenity': tags.get('amenity'),
            'healthcare': tags.get('healthcare'),
            'landuse': tags.get('landuse'),
            'housenumber': housenumber,
            'addr_full': tags.get('addr:full'),
            'addr_housenumber': tags.get('addr:housenumber'),
            'street': street,
            'street_address': street_address,
            'city': tags.get('addr:city'),
            'state': tags.get('addr:state'),
            'postcode': tags.get('addr:postcode'),
            'country': country,
            'website': tags.get('website') or tags.get('contact:website'),
            'phone': tags.get('phone') or tags.get('contact:phone'),
            'opening_hours': tags.get('opening_hours'),
            'drive_through': tags.get('drive_through'),
            'wikidata': tags.get('wikidata'),
            'lat': lat,
            'lon': lon,
            'raw_tags': tags,
        }

    async def _fetch(
        self,
        zipcode: str,
        osm_filter: str,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
    ) -> list[dict]:
        async with self._semaphore:
            query = self._build_query(zipcode, osm_filter, lat=lat, lon=lon)
            self._logger.debug(
                f"Overpass query zip={zipcode} filter={osm_filter!r}"
            )
            payload = await self._post_overpass(query)
            if payload is None:
                self._failed += 1
                return []
            elements = payload.get('elements') or []
            rows = []
            expected_country = (self.country_code or '').upper()
            for el in elements:
                row = self._flatten_element(el, zipcode, osm_filter)
                if row is None:
                    continue
                if row['lat'] is None or row['lon'] is None:
                    continue
                # Defensive: when an explicit addr:country is present, drop
                # elements whose country disagrees with the requested one.
                tag_country = (row.get('country') or '').strip().upper()
                if expected_country and tag_country and tag_country != expected_country:
                    continue
                rows.append(row)
            self._counter += len(rows)
            return rows

    async def _gather_chunked(self, tasks: list) -> list[list[dict]]:
        results: list[list[dict]] = []
        for i in range(0, len(tasks), self.chunk_size):
            chunk = tasks[i:i + self.chunk_size]
            batch = await asyncio.gather(*chunk, return_exceptions=True)
            for item in batch:
                if isinstance(item, Exception):
                    self._failed += 1
                    self._logger.error(f"Overpass task failed: {item}")
                    continue
                results.append(item)
        return results

    @staticmethod
    def _normalize_name(name: Optional[str]) -> str:
        if not name:
            return ''
        cleaned = _NAME_NOISE_RE.sub(' ', name)
        cleaned = _NON_ALNUM_RE.sub('', cleaned.lower())
        return cleaned

    @staticmethod
    def _normalize_address(row: pd.Series) -> str:
        """Build a comparable address key from address tags.

        Prefer ``housenumber + street`` because that uniquely identifies
        a physical building. Fall back to ``addr_full`` only when no
        structured number/street is available — ``addr_full`` text varies
        in formatting between mappers and is unreliable on its own.
        """
        housenumber = row.get('housenumber') or row.get('addr_housenumber')
        street = row.get('street')
        if housenumber and street:
            raw = f"{housenumber} {street}"
        else:
            raw = row.get('addr_full') or ''
        if not isinstance(raw, str):
            return ''
        return _NON_ALNUM_RE.sub('', raw.lower())

    @staticmethod
    def _normalize_phone(phone: Any) -> str:
        if not phone or not isinstance(phone, str):
            return ''
        return _DIGITS_RE.sub('', phone)[-10:]

    @staticmethod
    def _tag_richness(row: pd.Series) -> int:
        return sum(
            1 for v in row.values
            if v is not None and not (isinstance(v, float) and pd.isna(v))
        )

    def _dedup(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df

        # Step 1: collapse exact (osm_type, osm_id) duplicates that arose
        # from multiple filters matching the same element.
        df = df.copy()
        agg_filter = (
            df.groupby(['osm_type', 'osm_id'])['matched_filter']
            .apply(lambda s: ', '.join(sorted({str(x) for x in s if x})))
            .reset_index()
            .rename(columns={'matched_filter': '_matched_filters'})
        )
        df = df.drop_duplicates(subset=['osm_type', 'osm_id'], keep='first')
        df = df.merge(agg_filter, on=['osm_type', 'osm_id'], how='left')
        df['matched_filter'] = df['_matched_filters']
        df = df.drop(columns=['_matched_filters'])

        # Step 2: proximity de-dup by normalized name, with address/phone
        # discriminators to avoid collapsing legitimately distinct chain
        # stores (e.g. two Walgreens on opposite corners) that happen to
        # fall inside the proximity radius.
        df['_name_key'] = df['name'].map(self._normalize_name)
        df['_addr_key'] = df.apply(self._normalize_address, axis=1)
        df['_phone_key'] = df['phone'].map(self._normalize_phone)
        df['_richness'] = df.apply(self._tag_richness, axis=1)

        keep_indices: list[int] = []
        # Rows with no name fall back to (osm_type, osm_id) uniqueness only.
        unnamed = df[df['_name_key'] == '']
        keep_indices.extend(unnamed.index.tolist())

        named = df[df['_name_key'] != '']
        for _, group in named.groupby('_name_key'):
            survivors: list[dict] = []
            ordered = group.sort_values('_richness', ascending=False)
            for idx, row in ordered.iterrows():
                lat, lon = row['lat'], row['lon']
                addr_key = row['_addr_key']
                phone_key = row['_phone_key']
                duplicate = False
                for surv in survivors:
                    # Distinct structured address → distinct physical store,
                    # even if the points are within the proximity radius.
                    if addr_key and surv['addr'] and addr_key != surv['addr']:
                        continue
                    if (
                        self.dedup_use_phone
                        and phone_key
                        and surv['phone']
                        and phone_key != surv['phone']
                    ):
                        continue
                    try:
                        dist_m = geodesic(
                            (lat, lon), (surv['lat'], surv['lon'])
                        ).meters
                    except (ValueError, TypeError):
                        continue
                    if dist_m <= self.dedup_radius_meters:
                        duplicate = True
                        break
                if not duplicate:
                    survivors.append({
                        'idx': idx,
                        'lat': lat,
                        'lon': lon,
                        'addr': addr_key,
                        'phone': phone_key,
                    })
                    keep_indices.append(idx)

        deduped = df.loc[sorted(set(keep_indices))].copy()
        return deduped.drop(
            columns=['_name_key', '_addr_key', '_phone_key', '_richness']
        )

    def _merge_input_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Left-join the input DataFrame's extra columns onto the result by zipcode."""
        if df.empty or not isinstance(self.data, pd.DataFrame):
            return df
        if self.zipcode_column not in self.data.columns:
            return df

        # Normalize the input zipcode the same way it was normalized for queries.
        input_df = self.data.copy()
        input_df['_join_zip'] = (
            input_df[self.zipcode_column].astype(str).str.strip()
        )
        input_df = input_df.dropna(subset=['_join_zip'])
        input_df = input_df[input_df['_join_zip'] != '']
        input_df = input_df.drop_duplicates(subset=['_join_zip'], keep='first')

        # Only bring extra columns that don't already exist on the result, and
        # skip the zipcode column itself (already present as `zipcode`).
        extra_cols = [
            c for c in input_df.columns
            if c not in (self.zipcode_column, '_join_zip') and c not in df.columns
        ]
        if not extra_cols:
            return df

        df = df.copy()
        df['_join_zip'] = df['zipcode'].astype(str).str.strip()
        merged = df.merge(
            input_df[['_join_zip'] + extra_cols],
            on='_join_zip',
            how='left',
        )
        return merged.drop(columns=['_join_zip'])

    async def run(self) -> pd.DataFrame:
        zipcodes = (
            self.data[self.zipcode_column]
            .dropna()
            .astype(str)
            .str.strip()
            .replace('', pd.NA)
            .dropna()
            .unique()
            .tolist()
        )
        if not zipcodes:
            raise DataNotFound(
                f"Column '{self.zipcode_column}' contained no zipcodes."
            )

        zip_coords: dict[str, tuple[float, float]] = {}
        if self.lat_column and self.lon_column:
            for _, row in self.data.iterrows():
                zc = str(row.get(self.zipcode_column, '')).strip()
                if not zc:
                    continue
                try:
                    lat_val = float(row[self.lat_column])
                    lon_val = float(row[self.lon_column])
                except (TypeError, ValueError, KeyError):
                    continue
                if zc not in zip_coords:
                    zip_coords[zc] = (lat_val, lon_val)

        self._logger.notice(
            f"OpenStreetMap: querying {len(zipcodes)} zipcodes "
            f"x {len(self.filters)} filters "
            f"({len(zipcodes) * len(self.filters)} requests)"
            f"{f', {len(zip_coords)} with centroid coords' if zip_coords else ''}."
        )

        tasks = []
        for zipcode in zipcodes:
            coords = zip_coords.get(zipcode)
            lat, lon = coords if coords else (None, None)
            for osm_filter in self.filters:
                tasks.append(
                    self._fetch(zipcode, osm_filter, lat=lat, lon=lon)
                )
        all_results = await self._gather_chunked(tasks)

        rows: list[dict] = []
        for batch in all_results:
            rows.extend(batch)

        if not rows:
            self._logger.warning(
                "OpenStreetMap: no elements returned for any zipcode."
            )
            self._result = pd.DataFrame()
            self.add_metric('osm_elements_fetched', 0)
            self.add_metric('osm_failed_queries', self._failed)
            return self._result

        df = pd.DataFrame(rows)
        deduped = self._dedup(df)
        enriched = self._merge_input_columns(deduped)

        self._logger.notice(
            f"OpenStreetMap: fetched {len(df)} raw elements, "
            f"{len(deduped)} after de-dup; {self._failed} failed queries."
        )
        self.add_metric('osm_elements_fetched', int(len(df)))
        self.add_metric('osm_elements_deduped', int(len(deduped)))
        self.add_metric('osm_failed_queries', int(self._failed))

        self._result = enriched.reset_index(drop=True)
        return self._result
