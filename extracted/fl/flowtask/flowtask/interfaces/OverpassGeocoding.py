"""Reverse geocoding against an Overpass API instance (FEAT-238).

Overpass is not a geocoder, but it holds everything a reverse geocode
needs: ``is_in(lat,lon)`` names the administrative areas containing a
point, and ``around:`` finds the features near it. Combining the two in
one query resolves a coordinate to a street address without a paid
geocoding API and without leaving the local network — the repo already
runs a North America Overpass instance (``docker/overpass``) with
``OVERPASS_USE_AREAS=true``, which is what ``is_in`` requires.

Resolution proceeds outward through :attr:`OverpassReverseGeocoder.radii`
and stops at the first radius that finds an addressed feature (a node or
way carrying both ``addr:housenumber`` and ``addr:street``). Points with
nothing addressable nearby — empty rural coordinates — degrade to the
nearest named road, then to ``"<County>, <ST>"``, then to nothing;
they never raise.

Typical use::

    async with OverpassReverseGeocoder(url=OVERPASS_URL) as geocoder:
        results = await geocoder.reverse_many(market_anchors)
        address = results[anchor].formatted
"""
from __future__ import annotations

import asyncio
import logging
import math
import random
from dataclasses import dataclass
from typing import Iterable, Optional

import aiohttp


DEFAULT_OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Search radii, in metres, tried in order until an addressed feature is
# found. 150 m resolves essentially every retail location (the measured
# hits for Decatur GA, Manhattan NY and Dallas TX were 30-48 m away);
# the wider rings only ever run for genuinely remote points.
DEFAULT_RADII: tuple[int, ...] = (150, 600, 2500)

# OSM admin_level values, by role. Cities are level 8 in most of the US,
# but some places (New York City's boroughs) have no level-8 area at all,
# hence the level-7 fallback.
_CITY_LEVELS = ("8", "7")
_STATE_LEVEL = "4"
_COUNTY_LEVEL = "6"

_EARTH_RADIUS_M = 6_371_000.0


def _valid_postcode(value: Optional[str]) -> Optional[str]:
    """Drop postcodes that are obviously junk rather than emit them.

    OSM is crowd-tagged and carries genuine garbage: a building at 2700
    Floyd Street in Dallas is tagged ``addr:postcode="0"``, which would
    otherwise render as ``"... Dallas, TX 0"``. Anything shorter than
    four characters, or without a digit, is rejected. The rule stays
    deliberately loose so it accepts US ZIPs (``75204``, ``75204-1234``)
    and Canadian codes (``M5V 3L9``) alike.

    Args:
        value: A raw ``addr:postcode`` tag value.

    Returns:
        The trimmed postcode, or ``None`` when it fails the sanity check.
    """
    if not value:
        return None
    candidate = str(value).strip()
    if len(candidate) < 4 or not any(char.isdigit() for char in candidate):
        return None
    return candidate


def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two WGS84 points, in metres."""
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )
    return 2 * _EARTH_RADIUS_M * math.asin(math.sqrt(a))


@dataclass(frozen=True)
class ReverseGeocodeResult:
    """One coordinate resolved to its administrative and street context.

    Attributes:
        housenumber: OSM ``addr:housenumber`` of the matched feature.
        street: Street name — ``addr:street`` of the matched feature, or
            the name of the nearest named road when only that was found.
        city: Municipality, from the feature's ``addr:city`` when tagged,
            otherwise the enclosing level-8 (or level-7) admin area.
        state: State/province, preferring the admin area's ``ref``
            (``"GA"``) over its full name (``"Georgia"``).
        postcode: ``addr:postcode`` of the matched feature, when tagged.
        county: Enclosing level-6 admin area.
        distance_m: Metres from the queried point to the matched feature;
            ``None`` when nothing was matched.
        degraded: ``True`` when no fully addressed feature was found, so
            the result is a street-only, admin-only, or empty
            approximation. Purely observational.
    """

    housenumber: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[str] = None
    county: Optional[str] = None
    distance_m: Optional[float] = None
    degraded: bool = True

    @property
    def formatted(self) -> Optional[str]:
        """Human-readable one-line address, omitting whatever is missing.

        Returns:
            ``"114 East Ponce de Leon Avenue, Decatur, GA"`` when fully
            resolved, progressively shorter forms as parts are missing
            (``"Rush County, KS"``, ``"KS"``), and ``None`` when nothing
            at all is known.
        """
        parts: list[str] = []
        if self.street:
            street = (
                f"{self.housenumber} {self.street}"
                if self.housenumber
                else self.street
            )
            parts.append(street)
        # A city is a strictly better locality than the county containing
        # it, so the county only appears when no city was resolved.
        locality = self.city or self.county
        if locality:
            parts.append(locality)
        tail = " ".join(part for part in (self.state, self.postcode) if part)
        if tail:
            parts.append(tail)
        return ", ".join(parts) if parts else None


class OverpassReverseGeocoder:
    """Resolve coordinates to street addresses via an Overpass instance.

    The client is safe to reuse across many points: :meth:`reverse_many`
    de-duplicates its input and bounds concurrency with a semaphore, so a
    whole run's markets cost one HTTP request each at most (plus the
    widening retries only remote points need).

    Args:
        url: Primary Overpass endpoint.
        fallback_urls: Additional endpoints rotated through on retry, so a
            transient outage of one server can recover against another.
        radii: Search radii in metres, tried in ascending order.
        max_retries: Transport retries per query, per radius.
        backoff_base: Base of the exponential retry backoff, in seconds.
        concurrency: Maximum in-flight queries in :meth:`reverse_many`.
        timeout: Per-request timeout in seconds, also sent to Overpass as
            the in-query ``[timeout:]`` budget.
        startup_wait: Maximum seconds to wait for the Overpass server to
            become ready (the dispatcher accepting queries) when entering
            the ``async with`` context. Set to ``0`` to skip the probe.
            The default (300 s) covers a warm restart of the North
            America extract; a cold import takes hours and should be
            waited out separately.
        session: Pre-built aiohttp session. When omitted, the client opens
            (and closes) its own inside ``async with``.
    """

    def __init__(
        self,
        url: str = DEFAULT_OVERPASS_URL,
        fallback_urls: Optional[Iterable[str]] = None,
        radii: Iterable[int] = DEFAULT_RADII,
        max_retries: int = 2,
        backoff_base: float = 2.0,
        concurrency: int = 8,
        timeout: int = 60,
        startup_wait: float = 300.0,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        self.urls: list[str] = []
        for candidate in (url, *(fallback_urls or ())):
            if candidate and candidate not in self.urls:
                self.urls.append(candidate)
        if not self.urls:
            self.urls = [DEFAULT_OVERPASS_URL]
        self.radii = tuple(radii)
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self.concurrency = max(1, int(concurrency))
        self.timeout = timeout
        self.startup_wait = max(0.0, float(startup_wait))
        self._session = session
        self._owns_session = session is None
        self._logger = logging.getLogger(__name__)

    async def __aenter__(self) -> "OverpassReverseGeocoder":
        if self._session is None:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout + 10)
            )
            self._owns_session = True
        if self.startup_wait > 0:
            await self._wait_ready()
        return self

    async def _wait_ready(
        self,
        poll_interval: float = 5.0,
    ) -> None:
        """Block until the Overpass dispatcher can actually serve queries.

        The Overpass HTTP server starts before its dispatcher (the
        database layer) finishes loading. ``/api/status`` returns 200
        almost immediately, but real queries get 504
        ("Dispatcher_Client::request_read_and_idx::timeout") until the
        database files are mapped. This probe sends a tiny no-op query
        and waits for a 200 with valid JSON before declaring readiness.

        Args:
            poll_interval: Seconds between consecutive polls.
        """
        if self._session is None:
            return  # defensive; should never happen inside __aenter__

        max_wait = self.startup_wait
        elapsed = 0.0
        # A zero-cost query: ask for the count of nothing.  The
        # dispatcher must be ready for it to parse and return ``{"elements":[]}``
        # (~ 50 bytes).  This is cheaper than ``/api/status`` because it
        # exercises the exact code-path real queries need.
        probe_query = "[out:json][timeout:5];out count;"

        self._logger.info(
            "Waiting up to %.0fs for Overpass dispatcher to become ready …",
            max_wait,
        )

        while elapsed < max_wait:
            for url in self.urls:
                try:
                    async with self._session.post(
                        url, data={"data": probe_query}
                    ) as resp:
                        if resp.status == 200:
                            # Verify the body is parseable JSON — a 200
                            # with an HTML error page is still not ready.
                            try:
                                await resp.json(content_type=None)
                            except (ValueError, aiohttp.ClientResponseError):
                                continue
                            if elapsed > 0:
                                self._logger.info(
                                    "Overpass dispatcher ready at %s "
                                    "after %.0fs",
                                    url, elapsed,
                                )
                            else:
                                self._logger.info(
                                    "Overpass dispatcher ready at %s", url,
                                )
                            return
                except (aiohttp.ClientError, asyncio.TimeoutError):
                    pass
            self._logger.debug(
                "Overpass dispatcher not ready yet — retrying in %.0fs "
                "(%.0f/%.0fs)",
                poll_interval, elapsed, max_wait,
            )
            await asyncio.sleep(poll_interval)
            elapsed += poll_interval

        self._logger.warning(
            "Overpass dispatcher did not become ready within %.0fs — "
            "proceeding anyway (queries may fail with 504)",
            max_wait,
        )

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._owns_session and self._session is not None:
            await self._session.close()
            self._session = None

    # -- query -------------------------------------------------------------

    @staticmethod
    def _build_query(lat: float, lon: float, radius: int, timeout: int) -> str:
        """Build the combined `is_in` + `around` Overpass QL query.

        One round trip fetches three things: the administrative areas
        containing the point, every addressed node/way within `radius`,
        and every named road within `radius` (the street-only fallback).

        Args:
            lat: Latitude of the point to resolve.
            lon: Longitude of the point to resolve.
            radius: Search radius in metres.
            timeout: In-query Overpass time budget, in seconds.

        Returns:
            An Overpass QL program returning JSON.
        """
        return (
            f"[out:json][timeout:{timeout}];\n"
            f"is_in({lat},{lon})->.a;\n"
            ".a out tags;\n"
            "(\n"
            f'  node(around:{radius},{lat},{lon})["addr:housenumber"]["addr:street"];\n'
            f'  way(around:{radius},{lat},{lon})["addr:housenumber"]["addr:street"];\n'
            ");\n"
            "out tags center;\n"
            f"way(around:{radius},{lat},{lon})[highway][name];\n"
            "out tags center;"
        )

    async def _post(self, query: str) -> Optional[dict]:
        """POST one query, retrying across endpoints with backoff.

        Args:
            query: An Overpass QL program.

        Returns:
            The decoded JSON payload, or ``None`` when every attempt
            failed — callers degrade rather than raise.
        """
        if self._session is None:
            raise RuntimeError(
                "OverpassReverseGeocoder used outside 'async with' and "
                "without an injected session."
            )
        for attempt in range(self.max_retries + 1):
            url = self.urls[attempt % len(self.urls)]
            try:
                async with self._session.post(url, data={"data": query}) as response:
                    if response.status == 200:
                        try:
                            return await response.json(content_type=None)
                        except (ValueError, aiohttp.ClientResponseError):
                            self._logger.warning(
                                "Overpass returned a 200 with a non-JSON body "
                                "on %s (attempt %d)", url, attempt + 1,
                            )
                    elif response.status in (429, 502, 503, 504):
                        self._logger.warning(
                            "Overpass %d on %s (attempt %d)",
                            response.status, url, attempt + 1,
                        )
                    else:
                        self._logger.error(
                            "Overpass error %d on %s; giving up on this query",
                            response.status, url,
                        )
                        return None
            except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
                self._logger.warning(
                    "Overpass network error on %s (attempt %d): %s",
                    url, attempt + 1, exc,
                )
            if attempt < self.max_retries:
                await asyncio.sleep(
                    self.backoff_base ** (attempt + 1) + random.uniform(0, 0.5)
                )
        return None

    # -- parsing -----------------------------------------------------------

    @staticmethod
    def _element_center(element: dict) -> Optional[tuple[float, float]]:
        """Return an element's `(lat, lon)`, or None if it carries none."""
        if element.get("type") == "node":
            lat, lon = element.get("lat"), element.get("lon")
        else:
            center = element.get("center") or {}
            lat, lon = center.get("lat"), center.get("lon")
        if lat is None or lon is None:
            return None
        return (float(lat), float(lon))

    @staticmethod
    def _parse(payload: Optional[dict], lat: float, lon: float) -> ReverseGeocodeResult:
        """Turn one Overpass payload into a :class:`ReverseGeocodeResult`.

        Administrative context comes from the ``is_in`` areas; the street
        comes from the *nearest* addressed feature, falling back to the
        nearest named road when no feature carries a house number. The
        feature's own ``addr:*`` tags outrank the enclosing areas, since
        they describe the exact building rather than a polygon around it.

        Args:
            payload: Decoded Overpass JSON, or ``None`` for a failed query.
            lat: Latitude originally queried, for distance ranking.
            lon: Longitude originally queried.

        Returns:
            A result whose ``degraded`` flag is ``False`` only when a
            fully addressed feature was matched.
        """
        if not payload:
            return ReverseGeocodeResult()

        area_city: Optional[str] = None
        area_state: Optional[str] = None
        area_county: Optional[str] = None
        best_addressed: Optional[tuple[float, dict]] = None
        best_street: Optional[tuple[float, dict]] = None

        for element in payload.get("elements") or []:
            tags = element.get("tags") or {}
            if element.get("type") == "area":
                # Only administrative boundaries name a place; timezone and
                # statistical areas ("Metro Atlanta") share the payload and
                # must not be mistaken for a city.
                if tags.get("boundary") != "administrative":
                    continue
                level = tags.get("admin_level")
                if level in _CITY_LEVELS and area_city is None:
                    area_city = tags.get("name")
                elif level == _STATE_LEVEL and area_state is None:
                    area_state = tags.get("ref") or tags.get("name")
                elif level == _COUNTY_LEVEL and area_county is None:
                    area_county = tags.get("name")
                continue

            center = OverpassReverseGeocoder._element_center(element)
            if center is None:
                continue
            distance = _haversine_m(lat, lon, center[0], center[1])
            if tags.get("addr:housenumber") and tags.get("addr:street"):
                if best_addressed is None or distance < best_addressed[0]:
                    best_addressed = (distance, tags)
            elif tags.get("highway") and tags.get("name"):
                if best_street is None or distance < best_street[0]:
                    best_street = (distance, tags)

        if best_addressed is not None:
            distance, tags = best_addressed
            return ReverseGeocodeResult(
                housenumber=tags.get("addr:housenumber"),
                street=tags.get("addr:street"),
                city=tags.get("addr:city") or area_city,
                state=tags.get("addr:state") or area_state,
                postcode=_valid_postcode(tags.get("addr:postcode")),
                county=area_county,
                distance_m=distance,
                degraded=False,
            )

        if best_street is not None:
            distance, tags = best_street
            return ReverseGeocodeResult(
                street=tags.get("name"),
                city=area_city,
                state=area_state,
                county=area_county,
                distance_m=distance,
                degraded=True,
            )

        return ReverseGeocodeResult(
            city=area_city, state=area_state, county=area_county, degraded=True
        )

    # -- public API --------------------------------------------------------

    async def reverse(self, lat: float, lon: float) -> ReverseGeocodeResult:
        """Resolve one coordinate, widening the radius until it lands.

        Args:
            lat: Latitude to resolve.
            lon: Longitude to resolve.

        Returns:
            The first non-degraded result found; when every radius is
            exhausted, the richest degraded result seen (admin context is
            preserved even with no street). Never raises on backend
            failure — that returns an empty, degraded result.
        """
        best = ReverseGeocodeResult()
        for radius in self.radii:
            query = self._build_query(lat, lon, radius, self.timeout)
            payload = await self._post(query)
            result = self._parse(payload, lat, lon)
            if not result.degraded:
                return result
            # Keep the most informative degraded result across radii: a
            # street-only answer beats an admin-only one, which beats
            # nothing at all.
            if result.formatted and not best.formatted:
                best = result
            elif result.street and not best.street:
                best = result
        return best

    async def reverse_many(
        self, points: Iterable[tuple[float, float]]
    ) -> dict[tuple[float, float], ReverseGeocodeResult]:
        """Resolve many coordinates concurrently, de-duplicated.

        Args:
            points: Coordinates as ``(latitude, longitude)`` tuples.
                Repeats are collapsed, so a point shared by several
                callers costs exactly one query.

        Returns:
            A mapping from each *distinct* input point to its result. A
            point whose lookup failed maps to an empty degraded result
            rather than being absent, so callers can index without
            guarding.
        """
        unique = list(dict.fromkeys(tuple(point) for point in points))
        if not unique:
            return {}

        semaphore = asyncio.Semaphore(self.concurrency)

        async def _resolve(point: tuple[float, float]) -> ReverseGeocodeResult:
            async with semaphore:
                try:
                    return await self.reverse(point[0], point[1])
                except Exception as exc:  # noqa: BLE001 - one point must not sink the batch
                    self._logger.warning(
                        "Reverse geocode failed for %s: %s", point, exc
                    )
                    return ReverseGeocodeResult()

        resolved = await asyncio.gather(*(_resolve(point) for point in unique))
        return dict(zip(unique, resolved))
