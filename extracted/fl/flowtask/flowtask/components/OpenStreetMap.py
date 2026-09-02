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
import time
from collections.abc import Callable
from typing import Any, Optional

import aiohttp
import pandas as pd
from aiohttp.resolver import AsyncResolver
from geopy.distance import geodesic
from rapidfuzz import fuzz
from tqdm import tqdm

from ..exceptions import ComponentError, DataNotFound
from . import FlowComponent


DEFAULT_OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Splits a leading house number ("123", "123-A", "1200B") from the rest of a
# street address so it can be matched against the OSM ``addr:housenumber`` and
# ``addr:street`` tags separately.
_HOUSENUMBER_RE = re.compile(r'^\s*(\d+[\w-]*)\s+(.+?)\s*$')
# Overpass uses RE2-style regex inside ``~"..."``; escape every metacharacter
# and drop the double quotes that would otherwise terminate the literal.
_REGEX_META_RE = re.compile(r'([.\^$*+?()\[\]{}|\\])')

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
# Used to condense HTML error pages (a reverse proxy in front of Overpass
# returns full XHTML on 5xx) into one log-friendly line.
_HTML_TITLE_RE = re.compile(r'<title>\s*(.*?)\s*</title>', re.IGNORECASE | re.DOTALL)
_HTML_TAG_RE = re.compile(r'<[^>]+>')


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

    Discover results carry their coordinates in ``lat``/``lon`` columns by
    default. Set ``output_lat_column``/``output_lon_column`` to rename them
    (e.g. to ``latitude``/``longitude``) — parity with geocode mode. Each
    axis is renamed only when explicitly configured, so flows that consume
    the default ``lat``/``lon`` keep working unchanged.

    Modes
    -----
    ``mode: discover`` (default)
        The behaviour described above: discover every POI matching the
        ``filters`` inside each ZIP area.

    ``mode: geocode``
        *Forward geocoding* — the inverse problem. Given a DataFrame of
        already-known places (name + street + city + state + zipcode),
        compose a per-row Overpass query and resolve each row to its
        latitude/longitude. Useful when you already have the entities
        (e.g. a FEMA hotel registry) and only need their coordinates,
        and you run your own Overpass instance (no public rate limit).

        Every query is anchored to a ZIP-centroid coordinate via an
        ``around:<radius>,<lat>,<lon>`` spatial filter (resolved against
        the Overpass spatial index — fast and tile-local), so it never
        resolves a country/postal-area polygon. The centroid is read
        from ``lat_column``/``lon_column`` and is therefore mandatory.
        (US ZIP ``boundary=postal_code`` relations are largely absent
        from OSM, which is why area-scoped geocoding does not work and
        the spatial-radius approach is used instead.)

        For every row it issues a **single** unioned query (one
        round-trip) with two branches, then classifies each result in
        Python into a precision tier:

        1. Exact address — ``addr:housenumber`` + ``addr:street`` near
           the centroid (accepted regardless of name).
        2. Lodging by name — ``tourism`` lodging / ``building=hotel``
           near the centroid, fetched **by tag only** (no server-side
           ``name`` regex, which Overpass cannot index) and matched to
           the FEMA name locally; must clear the similarity threshold.

        Candidates are ranked by fuzzy similarity (``rapidfuzz``)
        between the input name and the OSM ``name`` tag, with proximity
        to the centroid as the tie-breaker. The original DataFrame is
        returned with ``output_lat_column``/``output_lon_column``
        (default ``latitude``/``longitude``) plus ``osm_id``,
        ``osm_type``, ``geocode_tier``, ``geocode_score``,
        ``geocode_matched_name`` and ``geocode_distance_m`` filled in;
        rows with no match are left null.

        ```yaml
        OpenStreetMap:
          mode: geocode
          overpass_url: http://192.168.1.16:12345/api/interpreter
          overpass_url_fallback:           # retried on the next attempt(s)
            - https://overpass-api.de/api/interpreter
            - https://overpass.kumi.systems/api/interpreter
          name_column: hotel_name
          street_column: street_address
          zipcode_column: zipcode
          lat_column: zip_centroid_lat    # input: ZIP centroid
          lon_column: zip_centroid_lon
          output_lat_column: latitude     # output: resolved hotel coords
          output_lon_column: longitude
          search_radius_meters: 8000
          name_similarity_threshold: 0.6
          semaphore_limit: 16
        ```
    """

    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ) -> None:
        self.mode: str = str(kwargs.pop('mode', 'discover')).lower()
        # discover-mode query strategy:
        #   'area'   (default) — current behaviour: resolve the country area
        #            + postal-code area + addr:postcode tag scan (+ optional
        #            around when a centroid is given).
        #   'around' — spatial-only: query `around:<radius>,<lat>,<lon>` and
        #            skip the (expensive) country/postal-area resolution.
        #            Requires lat_column/lon_column. Much faster on large runs.
        self.search_strategy: str = str(
            kwargs.pop('search_strategy', 'area')
        ).lower()
        self.zipcode_column: str = kwargs.pop('zipcode_column', 'zipcode')
        self.country_code: str = kwargs.pop('country_code', 'US')
        self.filters: list[str] = kwargs.pop('filters', []) or []
        # geocode-mode address columns
        self.name_column: str = kwargs.pop('name_column', 'name')
        self.street_column: str = kwargs.pop('street_column', 'street_address')
        self.city_column: str = kwargs.pop('city_column', 'city')
        self.state_column: str = kwargs.pop('state_column', 'state')
        self.name_similarity_threshold: float = float(
            kwargs.pop('name_similarity_threshold', 0.6)
        )
        # OSM ``tourism`` values treated as lodging in geocode mode. The
        # name-based branch fetches these by tag (cheap, no server-side name
        # regex) and the FEMA name is matched against them locally.
        self.lodging_tags: list[str] = kwargs.pop('lodging_tags', None) or [
            'hotel', 'motel', 'guest_house', 'hostel', 'resort', 'apartment',
        ]
        # Output coordinate columns. In geocode mode the resolved coordinates
        # always land here (the input ``lat_column``/``lon_column`` carry the
        # ZIP centroid used to anchor the spatial ``around`` search). In
        # discover mode the result coordinates are emitted as ``lat``/``lon``
        # by default; they are only renamed to these when the user explicitly
        # sets ``output_lat_column``/``output_lon_column`` (keeps existing
        # discover flows that consume ``lat``/``lon`` working unchanged).
        self._output_lat_explicit: bool = 'output_lat_column' in kwargs
        self._output_lon_explicit: bool = 'output_lon_column' in kwargs
        self.output_lat_column: str = kwargs.pop('output_lat_column', 'latitude')
        self.output_lon_column: str = kwargs.pop('output_lon_column', 'longitude')
        # tqdm progress bar for both discover and geocode modes (so a long
        # run visibly advances and is clearly not hung). Set False for
        # quiet/headless logs.
        self.show_progress: bool = bool(kwargs.pop('show_progress', True))
        self.element_types: list[str] = kwargs.pop(
            'element_types', ['node', 'way', 'relation']
        )
        self.semaphore_limit: int = int(kwargs.pop('semaphore_limit', 4))
        self.request_timeout: int = int(kwargs.pop('request_timeout', 180))
        self.overpass_url: str = kwargs.pop('overpass_url', DEFAULT_OVERPASS_URL)
        # Optional fallback Overpass endpoint(s) tried on retry when the
        # primary server fails (network error or 429/502/503/504). Accepts a
        # single URL string or a list of URLs. On each retry the next URL in
        # the rotation [primary, *fallbacks] is used, so a transient outage of
        # one server can recover against another instead of just waiting.
        _fallback = kwargs.pop('overpass_url_fallback', None)
        if not _fallback:
            self.overpass_url_fallback: list[str] = []
        elif isinstance(_fallback, str):
            self.overpass_url_fallback = [_fallback]
        else:
            self.overpass_url_fallback = list(_fallback)
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

        # Endpoint rotation: primary first, then any fallbacks. De-duplicated
        # while preserving order so a fallback that equals the primary is not
        # tried twice in a row.
        self._overpass_urls: list[str] = []
        for _url in (self.overpass_url, *self.overpass_url_fallback):
            if _url and _url not in self._overpass_urls:
                self._overpass_urls.append(_url)

        self._semaphore: Optional[asyncio.Semaphore] = None
        self._session: Optional[aiohttp.ClientSession] = None
        self._counter: int = 0
        self._failed: int = 0
        self._endpoint_penalties: dict[str, float] = {}
        self._endpoint_cooldown: float = 60.0

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
        if self.mode not in ('discover', 'geocode'):
            raise ComponentError(
                f"OpenStreetMap: unknown mode {self.mode!r} "
                "(expected 'discover' or 'geocode')."
            )
        if self.mode == 'geocode':
            # Geocode mode anchors every query to a ZIP-centroid coordinate
            # (around:) to stay fast and avoid resolving country/ZIP areas,
            # so the centroid columns are mandatory.
            if not self.lat_column or not self.lon_column:
                raise ComponentError(
                    "OpenStreetMap geocode mode requires 'lat_column' and "
                    "'lon_column' (the ZIP centroid used to anchor the search)."
                )
            for col in (self.lat_column, self.lon_column):
                if col not in self.data.columns:
                    raise DataNotFound(
                        f"Missing centroid column '{col}' in the input DataFrame."
                    )
            # Need at least a name or a street to compose the tag filter; the
            # other address columns are optional discriminators.
            required_any = [self.name_column, self.street_column]
            if not any(c in self.data.columns for c in required_any):
                raise DataNotFound(
                    "OpenStreetMap geocode mode requires at least one of "
                    f"'{self.name_column}' or '{self.street_column}' columns."
                )
        else:
            if self.zipcode_column not in self.data.columns:
                raise DataNotFound(
                    f"Missing '{self.zipcode_column}' column in the input DataFrame."
                )
            if not self.filters:
                raise ComponentError(
                    "OpenStreetMap requires at least one entry in 'filters'."
                )
            if self.search_strategy not in ('area', 'around'):
                raise ComponentError(
                    f"OpenStreetMap: unknown search_strategy "
                    f"{self.search_strategy!r} (expected 'area' or 'around')."
                )
            if self.search_strategy == 'around' and not (
                self.lat_column and self.lon_column
            ):
                raise ComponentError(
                    "OpenStreetMap search_strategy='around' requires "
                    "'lat_column' and 'lon_column' (the ZIP centroid)."
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
        if re.fullmatch(r'[A-Za-z0-9_:]+', cond):
            return f'["{cond}"]'
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
        # Fast path: spatial-only query anchored at the ZIP centroid. Skips
        # resolving the country/postal-area polygons entirely (Overpass uses
        # its spatial index instead), which is the dominant per-query cost.
        if self.search_strategy == 'around' and lat is not None and lon is not None:
            around = f'(around:{self.search_radius_meters},{lat},{lon})'
            body = '\n  '.join(
                f'{etype}{bracket}{around};'
                for etype in self.element_types
            )
            return (
                f'[out:json][timeout:{self.request_timeout}];\n'
                f'(\n  {body}\n);\n'
                f'out center tags;\n'
            )
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

    @staticmethod
    def _overpass_runtime_error(payload: Any) -> Optional[str]:
        """Return Overpass's ``remark`` when a 200 response is really a failure.

        When a query exceeds its in-query ``[timeout:]`` or ``[maxsize:]``
        (i.e. it fails *under* any reverse-proxy gateway timeout), Overpass
        replies with **HTTP 200** carrying a ``remark`` string and an empty
        ``elements`` list. Without this check those would be counted as a
        successful empty result and silently drop data instead of retrying.

        Returns the remark text for a genuine runtime failure, else ``None``.
        """
        if not isinstance(payload, dict):
            return None
        remark = payload.get('remark')
        if not remark or not isinstance(remark, str):
            return None
        low = remark.lower()
        if (
            'runtime error' in low
            or 'timed out' in low
            or 'out of memory' in low
        ):
            return remark.strip()
        return None

    @staticmethod
    def _summarize_error_body(body: str, limit: int = 160) -> str:
        """Condense an Overpass/proxy error body into one log-friendly line.

        5xx responses from a reverse proxy in front of Overpass are full
        HTML error pages; logging the raw markup is noise. Prefer the page
        ``<title>`` (e.g. ``"504 Gateway Time-out"``), otherwise strip tags
        and collapse whitespace.
        """
        if not body or not body.strip():
            return '(empty body)'
        text = body.strip()
        m = _HTML_TITLE_RE.search(text)
        if m and m.group(1).strip():
            return m.group(1).strip()[:limit]
        if '<' in text and '>' in text:
            text = _HTML_TAG_RE.sub(' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:limit] if text else '(no message)'

    def _pick_endpoint(self, attempt: int) -> str:
        """Pick the best endpoint, preferring healthy ones on attempt 0."""
        now = time.monotonic()
        if attempt == 0 and len(self._overpass_urls) > 1:
            healthy = [
                u for u in self._overpass_urls
                if now >= self._endpoint_penalties.get(u, 0)
            ]
            if healthy:
                return healthy[0]
        return self._overpass_urls[attempt % len(self._overpass_urls)]

    def _penalize_endpoint(self, url: str) -> None:
        """Mark an endpoint as degraded for the cooldown period."""
        self._endpoint_penalties[url] = (
            time.monotonic() + self._endpoint_cooldown
        )

    async def _post_overpass(self, query: str) -> Optional[dict]:
        """POST a query to Overpass with retry/backoff on rate limits.

        When ``overpass_url_fallback`` is configured each retry targets the
        next endpoint in the rotation ``[primary, *fallbacks]`` so a transient
        outage of one server can recover against another.
        """
        attempt = 0
        while True:
            retry_after: Optional[str] = None
            status: Optional[int] = None
            url = self._pick_endpoint(attempt)
            try:
                async with self._session.post(
                    url,
                    data={"data": query},
                ) as response:
                    status = response.status
                    if status == 200:
                        # content_type=None: accept valid JSON even if the
                        # server labels it with a non-standard content-type.
                        # A 200 with a genuinely non-JSON (e.g. HTML) body is
                        # treated as a retryable failure, not an exception.
                        try:
                            payload = await response.json(content_type=None)
                        except (ValueError, aiohttp.ClientResponseError):
                            body = await response.text()
                            self._logger.warning(
                                f"Overpass 200 non-JSON body (attempt "
                                f"{attempt + 1}) on {url}: "
                                f"{self._summarize_error_body(body)}"
                            )
                            payload = None
                        # A 200 can still be a server-side query failure: an
                        # exceeded in-query [timeout:]/[maxsize:] comes back as
                        # 200 + a "remark" with no elements. Retry that (so it
                        # can rotate to a fallback endpoint) instead of
                        # accepting it as a silent empty success. Keep any
                        # partial results when elements ARE present.
                        if payload is not None:
                            remark = self._overpass_runtime_error(payload)
                            if remark and not (payload.get('elements') or []):
                                self._logger.warning(
                                    f"Overpass runtime error (attempt "
                                    f"{attempt + 1}) on {url}: {remark[:160]}"
                                )
                            else:
                                return payload
                    elif status in (429, 502, 503, 504):
                        body = await response.text()
                        retry_after = response.headers.get('Retry-After')
                        self._penalize_endpoint(url)
                        self._logger.warning(
                            f"Overpass {status} (attempt {attempt + 1}) "
                            f"on {url}: {self._summarize_error_body(body)}"
                        )
                    else:
                        body = await response.text()
                        self._logger.error(
                            f"Overpass error {status} on {url}: "
                            f"{self._summarize_error_body(body)}"
                        )
                        return None
            except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
                self._penalize_endpoint(url)
                self._logger.warning(
                    f"Overpass network error (attempt {attempt + 1}) "
                    f"on {url}: {exc}"
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
        """Run discover tasks in bounded chunks with a tqdm progress bar.

        Discover sibling of :meth:`_gather_geocode`. Updates the bar as each
        request completes — so a long multi-ZIP/filter run visibly advances
        and a stall is obvious — and surfaces the running fetched-element and
        failed-query counts.
        """
        results: list[list[dict]] = []
        bar = tqdm(
            total=len(tasks),
            desc="OSM discover",
            unit="req",
            disable=not self.show_progress,
        )
        with bar:
            for i in range(0, len(tasks), self.chunk_size):
                chunk = tasks[i:i + self.chunk_size]
                # as_completed updates the bar per finished request rather
                # than per chunk, giving finer-grained liveness feedback.
                for fut in asyncio.as_completed(chunk):
                    try:
                        results.append(await fut)
                    except Exception as exc:  # noqa: BLE001
                        self._failed += 1
                        self._logger.error(f"Overpass task failed: {exc}")
                    bar.update(1)
                    bar.set_postfix(elements=self._counter, failed=self._failed)
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

    def _apply_output_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Rename the discover ``lat``/``lon`` columns to the configured ones.

        Parity with geocode mode: when the user explicitly sets
        ``output_lat_column``/``output_lon_column``, the corresponding default
        coordinate column is renamed. Each axis is handled independently and
        only on explicit opt-in, so discover flows that consume the default
        ``lat``/``lon`` are left untouched.
        """
        rename_map: dict[str, str] = {}
        if self._output_lat_explicit and 'lat' in df.columns:
            rename_map['lat'] = self.output_lat_column
        if self._output_lon_explicit and 'lon' in df.columns:
            rename_map['lon'] = self.output_lon_column
        if not rename_map:
            return df
        return df.rename(columns=rename_map)

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

    # ------------------------------------------------------------------ #
    # Geocode mode (forward geocoding: address -> lat/lon)
    # ------------------------------------------------------------------ #
    @staticmethod
    def _regex_escape(text: str) -> str:
        """Escape a literal for use inside an Overpass ``~"..."`` regex.

        Strips double quotes (which would terminate the literal) and
        backslash-escapes every regex metacharacter so the value matches
        verbatim, case-insensitively, against the OSM tag.
        """
        cleaned = (text or '').replace('"', ' ').strip()
        return _REGEX_META_RE.sub(r'\\\1', cleaned)

    @staticmethod
    def _cell(row: pd.Series, column: Optional[str]) -> Optional[str]:
        """Return a stripped string cell, or ``None`` when missing/NaN."""
        if not column or column not in row:
            return None
        value = row[column]
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return None
        text = str(value).strip()
        return text or None

    def _build_geocode_query(
        self, row: pd.Series, lat: float, lon: float
    ) -> Optional[str]:
        """Compose ONE centroid-anchored Overpass query for a row.

        When ``filters`` is set, each filter is expanded into one clause
        per element type (exact-match only — no regex).  This lets the
        same geocode pipeline resolve hotels, colleges, hospitals, or
        any other POI category.

        When ``filters`` is empty, falls back to the default lodging
        tags (``tourism=hotel``, ``building=hotel``, …) for backwards
        compatibility with hotel-geocoding flows.

        Address matching (tier 1) is done in Python by
        :meth:`_is_address_match` against the returned candidates.

        Returns ``None`` when the row has neither a usable street nor a name.
        """
        name = self._cell(row, self.name_column)
        street = self._cell(row, self.street_column)
        if not name and not street:
            return None
        types = self.element_types
        around = f'(around:{self.search_radius_meters},{lat},{lon})'
        branches: list[str] = []

        if self.filters:
            for osm_filter in self.filters:
                bracket = self._normalize_filter(osm_filter)
                branches.extend(
                    f'{t}{bracket}{around};' for t in types
                )
        else:
            for tag in self.lodging_tags:
                branches.extend(
                    f'{t}["tourism"="{tag}"]{around};' for t in types
                )
            branches.extend(
                f'{t}["building"="hotel"]{around};' for t in types
            )

        if not branches:
            return None
        body = '\n  '.join(branches)
        return (
            f'[out:json][timeout:{self.request_timeout}];\n'
            f'(\n  {body}\n);\nout center tags;\n'
        )

    def _is_address_match(self, row: pd.Series, tags: dict) -> bool:
        """True when an OSM element's address tags match the row's street.

        Used to re-derive the tier-1 (exact-address) classification in
        Python after the unioned query, since the response no longer tells
        us which branch produced each element.
        """
        street = self._cell(row, self.street_column)
        if not street:
            return False
        m = _HOUSENUMBER_RE.match(street)
        if not m:
            return False
        housenumber, street_name = m.group(1), m.group(2)
        osm_hn = (tags.get('addr:housenumber') or '').strip().lower()
        osm_street = (tags.get('addr:street') or '').strip().lower()
        if not osm_hn or osm_hn != housenumber.strip().lower():
            return False
        return street_name.strip().lower() in osm_street

    @staticmethod
    def _name_score(input_name: Optional[str], osm_name: Optional[str]) -> float:
        """Fuzzy similarity in [0, 1] between two place names."""
        if not input_name or not osm_name:
            return 0.0
        return fuzz.token_set_ratio(input_name.lower(), osm_name.lower()) / 100.0

    @staticmethod
    def _distance_m(
        lat1: float, lon1: float, lat2: Any, lon2: Any
    ) -> Optional[float]:
        try:
            return geodesic((lat1, lon1), (float(lat2), float(lon2))).meters
        except (ValueError, TypeError):
            return None

    async def _geocode_row(self, idx: Any, row: pd.Series) -> tuple[Any, Optional[dict]]:
        """Resolve a single row to coordinates via the precision cascade.

        Candidates within a tier are ranked by name similarity first and,
        on ties, by proximity to the ZIP centroid (closest wins).
        """
        async with self._semaphore:
            try:
                clat = float(row[self.lat_column])
                clon = float(row[self.lon_column])
            except (TypeError, ValueError, KeyError):
                return idx, None
            query = self._build_geocode_query(row, clat, clon)
            if query is None:
                return idx, None
            payload = await self._post_overpass(query)
            if payload is None:
                self._failed += 1
                return idx, None

            input_name = self._cell(row, self.name_column)
            elements = payload.get('elements') or []
            # Classify each candidate into tier 1 (exact address) or tier 2
            # (lodging-by-name) from its tags, then rank: prefer the more
            # precise tier, then higher name similarity, then proximity.
            addr_best: Optional[dict] = None
            addr_key: tuple = (-1.0, float('inf'))
            name_best: Optional[dict] = None
            name_key: tuple = (-1.0, float('inf'))
            seen: set = set()
            for el in elements:
                flat = self._flatten_element(el, '', 'geocode')
                if flat is None or flat['lat'] is None or flat['lon'] is None:
                    continue
                key_id = (flat['osm_type'], flat['osm_id'])
                if key_id in seen:
                    continue
                seen.add(key_id)
                score = self._name_score(input_name, flat.get('name'))
                dist = self._distance_m(clat, clon, flat['lat'], flat['lon'])
                rank = (score, -(dist if dist is not None else float('inf')))
                flat['_score'] = score
                flat['_dist'] = dist
                if self._is_address_match(row, flat.get('raw_tags') or {}):
                    if rank > addr_key:
                        addr_key, addr_best = rank, flat
                else:
                    if rank > name_key:
                        name_key, name_best = rank, flat

            # Tier 1: exact structured address — accept regardless of name.
            if addr_best is not None:
                return idx, self._geocode_result(idx, addr_best, tier=1)
            # Tier 2: lodging-by-name — must clear the similarity threshold.
            if name_best is not None and name_best['_score'] >= self.name_similarity_threshold:
                return idx, self._geocode_result(idx, name_best, tier=2)
            return idx, None

    def _geocode_result(self, idx: Any, best: dict, tier: int) -> dict:
        self._counter += 1
        return {
            'latitude': best['lat'],
            'longitude': best['lon'],
            'osm_id': best['osm_id'],
            'osm_type': best['osm_type'],
            'geocode_tier': tier,
            'geocode_score': round(best['_score'], 4),
            'geocode_matched_name': best.get('name'),
            'geocode_distance_m': (
                round(best['_dist'], 1) if best['_dist'] is not None else None
            ),
        }

    async def _gather_geocode(self, tasks: list) -> list:
        """Run geocode tasks in bounded chunks with a tqdm progress bar.

        Geocode-only sibling of :meth:`_gather_chunked` (which discover mode
        uses and which this must NOT alter). Updates the bar as each row
        completes — so a long 57k run visibly advances and a stall is
        obvious — and surfaces the running matched/failed counts.
        """
        results: list = []
        bar = tqdm(
            total=len(tasks),
            desc="OSM geocode",
            unit="row",
            disable=not self.show_progress,
        )
        with bar:
            for i in range(0, len(tasks), self.chunk_size):
                chunk = tasks[i:i + self.chunk_size]
                # as_completed updates the bar per finished row rather than
                # per chunk, giving finer-grained liveness feedback.
                for fut in asyncio.as_completed(chunk):
                    try:
                        results.append(await fut)
                    except Exception as exc:  # noqa: BLE001
                        self._failed += 1
                        self._logger.error(f"OpenStreetMap geocode task failed: {exc}")
                    bar.update(1)
                    bar.set_postfix(matched=self._counter, failed=self._failed)
        return results

    async def _geocode_run(self) -> pd.DataFrame:
        lat_col = self.output_lat_column
        lon_col = self.output_lon_column
        out_cols = [
            lat_col, lon_col, 'osm_id', 'osm_type', 'geocode_tier',
            'geocode_score', 'geocode_matched_name', 'geocode_distance_m',
        ]
        for col in out_cols:
            if col not in self.data.columns:
                self.data[col] = None

        self._logger.notice(
            f"OpenStreetMap geocode: resolving {len(self.data)} rows "
            f"against {self.overpass_url} "
            f"(around:{self.search_radius_meters}m)"
        )
        tasks = [self._geocode_row(idx, row) for idx, row in self.data.iterrows()]
        results = await self._gather_geocode(tasks)

        # Pre-fill output coordinates with the input centroid so rows
        # that fail to match still retain their original position.
        if self.lat_column in self.data.columns:
            self.data[lat_col] = self.data[self.lat_column]
        if self.lon_column in self.data.columns:
            self.data[lon_col] = self.data[self.lon_column]

        matched = 0
        for item in results:
            if not item:
                continue
            idx, payload = item
            if not payload:
                continue
            matched += 1
            self.data.at[idx, lat_col] = payload['latitude']
            self.data.at[idx, lon_col] = payload['longitude']
            self.data.at[idx, 'osm_id'] = payload['osm_id']
            self.data.at[idx, 'osm_type'] = payload['osm_type']
            self.data.at[idx, 'geocode_tier'] = payload['geocode_tier']
            self.data.at[idx, 'geocode_score'] = payload['geocode_score']
            self.data.at[idx, 'geocode_matched_name'] = payload['geocode_matched_name']
            self.data.at[idx, 'geocode_distance_m'] = payload['geocode_distance_m']

        self._logger.notice(
            f"OpenStreetMap geocode: matched {matched}/{len(self.data)} rows; "
            f"{self._failed} failed queries."
        )
        self.add_metric('osm_rows_total', int(len(self.data)))
        self.add_metric('osm_rows_matched', int(matched))
        self.add_metric('osm_failed_queries', int(self._failed))
        self._result = self.data
        return self._result

    async def run(self) -> pd.DataFrame:
        if self.mode == 'geocode':
            return await self._geocode_run()
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
        skipped = 0
        for zipcode in zipcodes:
            coords = zip_coords.get(zipcode)
            # In 'around' strategy a centroid is mandatory; skip ZIPs without
            # one rather than silently falling back to a slow area query.
            if self.search_strategy == 'around' and coords is None:
                skipped += 1
                self._logger.warning(
                    f"search_strategy='around': zip {zipcode} has no centroid; "
                    "skipped."
                )
                continue
            lat, lon = coords if coords else (None, None)
            for osm_filter in self.filters:
                tasks.append(
                    self._fetch(zipcode, osm_filter, lat=lat, lon=lon)
                )
        if skipped:
            self.add_metric('osm_zips_skipped_no_centroid', int(skipped))
        all_results = await self._gather_chunked(tasks)

        rows: list[dict] = []
        for batch in all_results:
            rows.extend(batch)

        if not rows:
            self.add_metric('osm_elements_fetched', 0)
            self.add_metric('osm_failed_queries', self._failed)
            raise DataNotFound(
                "OpenStreetMap: no elements returned for any zipcode."
            )

        df = pd.DataFrame(rows)
        deduped = self._dedup(df)
        enriched = self._merge_input_columns(deduped)

        enriched = self._apply_output_columns(enriched)

        self._logger.notice(
            f"OpenStreetMap: fetched {len(df)} raw elements, "
            f"{len(deduped)} after de-dup; {self._failed} failed queries."
        )
        self.add_metric('osm_elements_fetched', int(len(df)))
        self.add_metric('osm_elements_deduped', int(len(deduped)))
        self.add_metric('osm_failed_queries', int(self._failed))

        self._result = enriched.reset_index(drop=True)
        return self._result
