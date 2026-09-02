"""
Routing interface (FEAT-234).

Backend-agnostic road-network distance/duration provider. Exposes an N×N
distance/duration matrix over an ordered list of coordinates, delegating
to a pluggable backend (Valhalla, OSRM, or a geodesic fallback) selected
by configuration. See ``sdd/specs/osrm-routing-migration.spec.md`` for the
full architectural design.

This module defines the shared data models, the backend contract
(``RoutingBackend``), the always-available offline fallback
(``GeodesicBackend``), and ``RoutingService`` — the orchestration layer
(HTTP session, Redis cache, retry/backoff, chunking). ``ValhallaBackend``
and ``OSRMBackend`` are added by TASK-151.
"""
import asyncio
import hashlib
import json
import logging
import random
from abc import ABC, abstractmethod
from typing import Any, Literal, Optional

import aiohttp
import polyline
from aiohttp.resolver import AsyncResolver
from geopy.distance import geodesic
from pydantic import BaseModel, Field, PrivateAttr
from shapely.geometry import LineString

from ..conf import (
    ROUTING_BACKEND,
    ROUTING_COSTING,
    ROUTING_DETOUR_FACTOR,
    ROUTING_GEOMETRY_TTL,
    ROUTING_MATRIX_TTL,
    ROUTING_MAX_MATRIX_SIZE,
    ROUTING_MAX_ROUTE_LOCATIONS,
    ROUTING_SERVICE_URL,
    ROUTING_SIMPLIFY_TOLERANCE_M,
    ROUTING_TIMEOUT,
    HTTPCLIENT_MAX_SEMAPHORE,
)
from .cache import CacheSupport


Coordinate = tuple[float, float]  # (latitude, longitude)


def round_coordinate(coordinate: Coordinate, ndigits: int = 6) -> Coordinate:
    """Round a (latitude, longitude) pair to a fixed precision.

    Used both to index a ``DistanceMatrix`` for lookups and to derive
    stable cache keys (TASK-150), so the two must never drift apart.

    Args:
        coordinate: A (latitude, longitude) pair.
        ndigits: Number of decimal digits to round to.

    Returns:
        The rounded (latitude, longitude) pair.
    """
    latitude, longitude = coordinate
    return (round(latitude, ndigits), round(longitude, ndigits))


class RouteLeg(BaseModel):
    """One directed origin -> destination measurement.

    ``degraded`` answers a different question from
    ``DistanceMatrix.degraded`` and the two may disagree. Per leg it
    means *this measurement is a straight-line estimate, not a
    road-network measurement* — true for an unroutable cell the backend
    returned as null (islands, Alaska, any pair with no road path
    between them) and for every ``GeodesicBackend`` value. At matrix
    level it means *the backend I asked for failed*.

    Defaults to ``False``, which is also what a pre-FEAT-236 cache
    entry deserializes to. That is correct rather than a silent lie:
    ``RoutingService.distance_matrix()`` never caches a degraded
    matrix, so every stored entry is by construction all-road-network.
    """

    distance_miles: float = Field(..., ge=0.0)
    duration_minutes: float = Field(..., ge=0.0)
    degraded: bool = False


class DistanceMatrix(BaseModel):
    """N×N road-network matrix over an ordered coordinate list.

    ``legs[i][j]`` is the trip from ``locations[i]`` to ``locations[j]``.
    Matrices are directional: ``legs[i][j]`` and ``legs[j][i]`` may differ
    (one-way streets, turn restrictions), even though ``GeodesicBackend``
    happens to produce symmetric values.
    """

    locations: list[Coordinate]
    legs: list[list[RouteLeg]]
    backend: str
    costing: str
    degraded: bool = False

    _index: dict[Coordinate, int] = PrivateAttr(default_factory=dict)

    def model_post_init(self, __context: Any) -> None:
        """Build a rounded-coordinate -> position index once per instance."""
        self._index = {
            round_coordinate(coordinate): position
            for position, coordinate in enumerate(self.locations)
        }

    def lookup(self, origin: Coordinate, destination: Coordinate) -> RouteLeg:
        """Return the leg between two coordinates present in this matrix.

        Args:
            origin: (latitude, longitude) of the trip origin.
            destination: (latitude, longitude) of the trip destination.

        Returns:
            The directional ``RouteLeg`` for ``origin -> destination``.

        Raises:
            KeyError: If either coordinate is not present in ``locations``.
        """
        origin_key = round_coordinate(origin)
        destination_key = round_coordinate(destination)
        if origin_key not in self._index:
            raise KeyError(f"Coordinate not in matrix: {origin}")
        if destination_key not in self._index:
            raise KeyError(f"Coordinate not in matrix: {destination}")
        i = self._index[origin_key]
        j = self._index[destination_key]
        return self.legs[i][j]


GeometryDetail = Literal["none", "overview", "full"]


class RouteShape(BaseModel):
    """The traced path of ONE ordered itinerary.

    Unlike ``DistanceMatrix``, ``locations`` here is an ordered chain:
    ``locations[i] -> locations[i + 1]`` is a leg. ``points`` is the
    full traced path across every leg, concatenated. ``to_geojson()``,
    ``to_wkt()`` and ``polyline6`` all derive from the same ``points``
    list, so the three representations cannot disagree.
    """

    locations: list[Coordinate]  # the ordered stops requested
    points: list[Coordinate]  # the traced path, (lat, lon)
    polyline6: str  # encoded, precision 6, as Valhalla returned it
    distance_miles: float = Field(..., ge=0.0)
    duration_minutes: float = Field(..., ge=0.0)
    backend: str  # "valhalla" | "osrm" | "geodesic"
    costing: str
    degraded: bool = False  # True when this is a straight-line approximation

    def simplified(self, tolerance_m: float) -> "RouteShape":
        """Return a copy whose ``points`` are Douglas-Peucker simplified.

        Args:
            tolerance_m: Simplification tolerance in metres, converted
                to degrees for ``shapely``'s ``simplify()`` via a flat
                ``/ 111320.0`` (metres per degree of *latitude*, which
                is ~constant). This is only exact at the equator: a
                degree of *longitude* shortens with ``cos(latitude)``,
                so the effective east-west tolerance is progressively
                tighter (i.e. simplifies less aggressively than
                requested) at higher latitudes. Negligible in practice
                for the measured/documented case (continental US,
                ~30-45°N — see ``docs/components/SchedulingVisits.md``)
                but worth remembering before relying on the exact
                point-count reduction near the poles. Values ``<= 0``
                return ``self`` unchanged.

        Returns:
            A new ``RouteShape`` with simplified ``points`` and a
            re-encoded ``polyline6`` describing that simplified line.
            The first and last points are always preserved exactly.
        """
        if tolerance_m <= 0:
            return self
        tolerance_deg = tolerance_m / 111320.0
        line = LineString([(lon, lat) for lat, lon in self.points])
        simplified_line = line.simplify(tolerance_deg, preserve_topology=False)
        simplified_points = [(lat, lon) for lon, lat in simplified_line.coords]
        if len(simplified_points) < 2:
            simplified_points = [self.points[0], self.points[-1]]
        else:
            simplified_points[0] = self.points[0]
            simplified_points[-1] = self.points[-1]
        return self.model_copy(
            update={
                "points": simplified_points,
                "polyline6": polyline.encode(simplified_points, 6),
            }
        )

    def to_geojson(self) -> dict[str, Any]:
        """Return this route as a GeoJSON ``LineString``.

        Returns:
            A dict with ``coordinates`` as ``[lon, lat]`` pairs —
            GeoJSON's coordinate order, the reverse of this model's
            internal ``(lat, lon)`` ``points``.
        """
        return {
            "type": "LineString",
            "coordinates": [[lon, lat] for lat, lon in self.points],
        }

    def to_wkt(self) -> str:
        """Return this route as WKT, for ``ST_GeomFromText(..., 4326)``.

        Returns:
            ``"LINESTRING (lon lat, lon lat, ...)"``, derived from the
            same ``points`` list as ``to_geojson()`` so the two can
            never disagree.
        """
        coords = ", ".join(f"{lon} {lat}" for lat, lon in self.points)
        return f"LINESTRING ({coords})"


class RoutingBackend(ABC):
    """Adapter for one routing engine."""

    name: str

    @abstractmethod
    async def matrix(
        self,
        locations: list[Coordinate],
        session: Any,
    ) -> DistanceMatrix:
        """Compute the N×N distance/duration matrix for ``locations``.

        Args:
            locations: Ordered (latitude, longitude) pairs.
            session: Shared HTTP session (unused by offline backends).

        Returns:
            A ``DistanceMatrix`` covering every pair in ``locations``.
        """
        ...

    @abstractmethod
    async def route_shape(
        self,
        locations: list[Coordinate],
        session: Any,
    ) -> RouteShape:
        """Trace the ordered itinerary ``locations`` as one path.

        Args:
            locations: Ordered (latitude, longitude) waypoints;
                ``locations[i] -> locations[i + 1]`` is one leg.
            session: Shared HTTP session (unused by offline backends).

        Returns:
            A ``RouteShape`` describing the traced path across every leg.
        """
        ...


class GeodesicBackend(RoutingBackend):
    """Offline fallback backend. Never fails, never touches the network.

    Distance is ``geodesic(a, b).miles * detour_factor``; duration is
    derived arithmetically as ``distance_miles / average_speed * 60``
    (minutes), matching the semantics of
    ``SchedulingVisits.get_distance()`` (miles) and the historical
    ``(distance_miles / average_speed) * 60`` time formula.
    """

    name = "geodesic"

    def __init__(
        self,
        detour_factor: Optional[float] = None,
        average_speed: float = 40.0,
        **_ignored: Any,
    ) -> None:
        """Initialize the geodesic fallback backend.

        Args:
            detour_factor: Multiplier applied to straight-line distance.
                Defaults to ``flowtask.conf.ROUTING_DETOUR_FACTOR``.
            average_speed: Assumed average speed in mph, used to derive
                duration from distance.
            **_ignored: Swallows backend-specific kwargs (e.g.
                ``service_url``, ``costing``, ``timeout``) so
                ``RoutingService`` can construct any registered backend
                uniformly.
        """
        self.detour_factor = (
            detour_factor if detour_factor is not None else ROUTING_DETOUR_FACTOR
        )
        self.average_speed = average_speed

    async def matrix(
        self,
        locations: list[Coordinate],
        session: Any = None,
    ) -> DistanceMatrix:
        """Build a geodesic-estimate matrix for ``locations``.

        Always returns ``degraded=False`` — matching the
        ``RoutingBackend`` ABC's ``(locations, session)`` signature
        exactly, so any backend can be invoked uniformly through
        ``self._backend.matrix(locations, session=...)``. When this
        backend stands in for a *failed* backend, the caller
        (``RoutingService.distance_matrix()``) marks the returned matrix
        degraded itself via ``model_copy(update={"degraded": True})``
        rather than this method taking a ``degraded`` argument that no
        other backend's ``matrix()`` accepts.

        Args:
            locations: Ordered (latitude, longitude) pairs.
            session: Unused; accepted for interface compatibility.

        Returns:
            A ``DistanceMatrix`` with ``backend="geodesic"``,
            ``degraded=False`` at matrix level, and every off-diagonal
            ``RouteLeg.degraded`` set to ``True`` — each value here IS a
            straight-line estimate, whatever role this backend is
            playing (FEAT-236).
        """
        legs: list[list[RouteLeg]] = []
        for i, origin in enumerate(locations):
            row: list[RouteLeg] = []
            for j, destination in enumerate(locations):
                if i == j:
                    row.append(
                        RouteLeg(distance_miles=0.0, duration_minutes=0.0)
                    )
                    continue
                distance_miles = (
                    geodesic(origin, destination).miles * self.detour_factor
                )
                duration_minutes = (distance_miles / self.average_speed) * 60
                row.append(
                    RouteLeg(
                        distance_miles=distance_miles,
                        duration_minutes=duration_minutes,
                        degraded=True,
                    )
                )
            legs.append(row)
        return DistanceMatrix(
            locations=locations,
            legs=legs,
            backend=self.name,
            costing="n/a",
        )

    async def route_shape(
        self,
        locations: list[Coordinate],
        session: Any = None,
    ) -> RouteShape:
        """Chain ``locations`` into straight segments — the offline fallback.

        Args:
            locations: Ordered (latitude, longitude) waypoints.
            session: Unused; accepted for interface compatibility.

        Returns:
            A ``RouteShape`` with ``points == locations`` (no
            interpolation), ``degraded=True``, and distance/duration
            derived the same way as ``matrix()``.
        """
        distance_miles = 0.0
        for origin, destination in zip(locations, locations[1:]):
            distance_miles += (
                geodesic(origin, destination).miles * self.detour_factor
            )
        duration_minutes = (distance_miles / self.average_speed) * 60
        return RouteShape(
            locations=locations,
            points=list(locations),
            polyline6=polyline.encode(locations, 6),
            distance_miles=distance_miles,
            duration_minutes=duration_minutes,
            backend=self.name,
            costing="n/a",
            degraded=True,
        )


# Backend registry: maps `ROUTING_BACKEND` / `RoutingService(backend=...)`
# names to the `RoutingBackend` subclass that implements them.
# TASK-151 registers "valhalla" and "osrm" via `register_backend()`.
_BACKEND_REGISTRY: dict[str, type[RoutingBackend]] = {
    "geodesic": GeodesicBackend,
}


def register_backend(name: str, backend_cls: type[RoutingBackend]) -> None:
    """Register a routing backend class under a config-selectable name.

    Args:
        name: The value of `ROUTING_BACKEND` / `RoutingService(backend=...)`
            that selects this backend (e.g. ``"valhalla"``, ``"osrm"``).
        backend_cls: The `RoutingBackend` subclass to instantiate.
    """
    _BACKEND_REGISTRY[name] = backend_cls


class ValhallaBackend(RoutingBackend):
    """Valhalla ``/sources_to_targets`` adapter — the deployed primary backend.

    Sends a mandatory ``costing`` field with every request. Valhalla
    returns distance in **kilometres** and time in **seconds**.
    """

    name = "valhalla"

    def __init__(
        self,
        service_url: Optional[str] = None,
        costing: Optional[str] = None,
        timeout: Optional[int] = None,
        detour_factor: Optional[float] = None,
        average_speed: float = 40.0,
        **_ignored: Any,
    ) -> None:
        """Initialize the Valhalla adapter.

        Args:
            service_url: Valhalla service base URL. Defaults to
                ``conf.ROUTING_SERVICE_URL``.
            costing: Valhalla costing profile. Defaults to
                ``conf.ROUTING_COSTING``.
            timeout: Per-request timeout in seconds. Defaults to
                ``conf.ROUTING_TIMEOUT``.
            detour_factor: Used only for the null-cell geodesic fallback.
            average_speed: Used only for the null-cell geodesic fallback.
            **_ignored: Swallows kwargs meant for other backends.
        """
        self.service_url = service_url or ROUTING_SERVICE_URL
        self.costing = costing or ROUTING_COSTING
        self.timeout = timeout or ROUTING_TIMEOUT
        self.logger = logging.getLogger(__name__)
        self._geodesic = GeodesicBackend(
            detour_factor=detour_factor, average_speed=average_speed
        )

    async def matrix(
        self, locations: list[Coordinate], session: aiohttp.ClientSession
    ) -> DistanceMatrix:
        """Query Valhalla ``/sources_to_targets`` and normalize the result.

        Args:
            locations: Ordered (latitude, longitude) pairs, used as both
                sources and targets.
            session: Shared HTTP session.

        Returns:
            A `DistanceMatrix` with distances in miles and durations in
            minutes. `degraded=True` if any cell was unroutable.
        """
        payload = {
            "sources": [{"lat": lat, "lon": lon} for lat, lon in locations],
            "targets": [{"lat": lat, "lon": lon} for lat, lon in locations],
            "costing": self.costing,
        }
        url = f"{self.service_url}/sources_to_targets"
        async with session.post(
            url, json=payload, timeout=aiohttp.ClientTimeout(total=self.timeout)
        ) as response:
            response.raise_for_status()
            data = await response.json(content_type=None)

        degraded = False
        legs: list[list[RouteLeg]] = []
        rows = data["sources_to_targets"]
        for i, row_data in enumerate(rows):
            row: list[RouteLeg] = []
            for j, cell in enumerate(row_data):
                if i == j:
                    row.append(
                        RouteLeg(distance_miles=0.0, duration_minutes=0.0)
                    )
                    continue
                distance_km = cell.get("distance") if cell else None
                duration_s = cell.get("time") if cell else None
                if distance_km is None or duration_s is None:
                    degraded = True
                    leg_degraded = True
                    distance_miles = (
                        geodesic(locations[i], locations[j]).miles
                        * self._geodesic.detour_factor
                    )
                    duration_minutes = (
                        distance_miles / self._geodesic.average_speed
                    ) * 60
                else:
                    leg_degraded = False
                    # Valhalla distance -> KILOMETRES; time -> SECONDS.
                    distance_miles = distance_km * 0.621371
                    duration_minutes = duration_s / 60.0
                row.append(
                    RouteLeg(
                        distance_miles=distance_miles,
                        duration_minutes=duration_minutes,
                        degraded=leg_degraded,
                    )
                )
            legs.append(row)
        return DistanceMatrix(
            locations=locations,
            legs=legs,
            backend=self.name,
            costing=self.costing,
            degraded=degraded,
        )

    async def route_shape(
        self, locations: list[Coordinate], session: aiohttp.ClientSession
    ) -> RouteShape:
        """Query Valhalla ``/route`` and trace the ordered itinerary.

        Args:
            locations: Ordered (latitude, longitude) waypoints;
                ``locations[i] -> locations[i + 1]`` is one leg.
            session: Shared HTTP session.

        Returns:
            A ``RouteShape`` with distance in miles and duration in
            minutes, ``points`` concatenated across every leg with the
            duplicated junction point dropped at each waypoint.

        Raises:
            aiohttp.ClientError: If Valhalla reports ``trip.status != 0``.
        """
        payload = {
            "locations": [{"lat": lat, "lon": lon} for lat, lon in locations],
            "costing": self.costing,
            "units": "miles",
            "directions_type": "none",
            "shape_format": "polyline6",
        }
        url = f"{self.service_url}/route"
        async with session.post(
            url, json=payload, timeout=aiohttp.ClientTimeout(total=self.timeout)
        ) as response:
            response.raise_for_status()
            data = await response.json(content_type=None)

        trip = data["trip"]
        if trip.get("status") != 0:
            raise aiohttp.ClientError(
                f"Valhalla route request failed with status="
                f"{trip.get('status')!r}: {trip.get('status_message')!r}"
            )

        points: list[Coordinate] = []
        distance_miles = 0.0
        duration_minutes = 0.0
        for leg in trip["legs"]:
            leg_points = polyline.decode(leg["shape"], 6)
            if points and leg_points and points[-1] == leg_points[0]:
                leg_points = leg_points[1:]
            points.extend(leg_points)
            summary = leg["summary"]
            # units="miles" is honoured by /route -- do NOT apply the
            # km->mi 0.621371 factor used by /sources_to_targets above.
            distance_miles += summary["length"]
            duration_minutes += summary["time"] / 60.0

        # Re-encode rather than concatenate Valhalla's per-leg polyline6
        # strings: with >1 leg the junction point was already deduped out
        # of `points` above, so a naive `"".join(shape for shape in legs)`
        # would encode that duplicate right back in. Re-encoding from the
        # final, deduped `points` is what keeps `polyline6` and `points`
        # in agreement — the same one-decode-derive-everything discipline
        # `simplified()`/`to_geojson()`/`to_wkt()` rely on. Lossless: a
        # decode -> encode round-trip at the same precision (6) reproduces
        # the exact same coordinates.
        return RouteShape(
            locations=locations,
            points=points,
            polyline6=polyline.encode(points, 6),
            distance_miles=distance_miles,
            duration_minutes=duration_minutes,
            backend=self.name,
            costing=self.costing,
            degraded=False,
        )


class OSRMBackend(RoutingBackend):
    """OSRM ``/table`` adapter — implemented and tested, not deployed.

    OSRM returns distance in **metres** and duration in **seconds**. The
    vehicle profile is baked into the graph at ``osrm-extract`` time, so
    `ROUTING_COSTING` does not apply here: a non-default value is logged
    and ignored rather than sent (OSRM's `/table` endpoint has no costing
    parameter at all).
    """

    name = "osrm"

    def __init__(
        self,
        service_url: Optional[str] = None,
        costing: Optional[str] = None,
        timeout: Optional[int] = None,
        detour_factor: Optional[float] = None,
        average_speed: float = 40.0,
        **_ignored: Any,
    ) -> None:
        """Initialize the OSRM adapter.

        Args:
            service_url: OSRM service base URL. Defaults to
                ``conf.ROUTING_SERVICE_URL``.
            costing: Ignored (with a warning) unless it equals the
                default ``"auto"`` profile — OSRM has no costing concept.
            timeout: Per-request timeout in seconds. Defaults to
                ``conf.ROUTING_TIMEOUT``.
            detour_factor: Used only for the null-cell geodesic fallback.
            average_speed: Used only for the null-cell geodesic fallback.
            **_ignored: Swallows kwargs meant for other backends.
        """
        self.service_url = service_url or ROUTING_SERVICE_URL
        self.timeout = timeout or ROUTING_TIMEOUT
        self.logger = logging.getLogger(__name__)
        self._geodesic = GeodesicBackend(
            detour_factor=detour_factor, average_speed=average_speed
        )
        resolved_costing = costing or ROUTING_COSTING
        if resolved_costing != "auto":
            self.logger.warning(
                "OSRMBackend ignores ROUTING_COSTING=%r: OSRM bakes the "
                "vehicle profile into the graph at osrm-extract time, "
                "before this request is ever made.",
                resolved_costing,
            )
        self.costing = resolved_costing

    async def matrix(
        self, locations: list[Coordinate], session: aiohttp.ClientSession
    ) -> DistanceMatrix:
        """Query OSRM ``/table`` and normalize the result.

        Args:
            locations: Ordered (latitude, longitude) pairs.
            session: Shared HTTP session.

        Returns:
            A `DistanceMatrix` with distances in miles and durations in
            minutes. `degraded=True` if any cell was unroutable.

        Raises:
            aiohttp.ClientError: If OSRM's ``code`` field is not ``"Ok"``.
        """
        # NOTE: OSRM path coordinates are `{longitude},{latitude}` — the
        # reverse of every internal (latitude, longitude) tuple.
        coords = ";".join(f"{lon},{lat}" for lat, lon in locations)
        url = (
            f"{self.service_url}/table/v1/driving/{coords}"
            "?annotations=duration,distance"
        )
        async with session.get(
            url, timeout=aiohttp.ClientTimeout(total=self.timeout)
        ) as response:
            response.raise_for_status()
            data = await response.json(content_type=None)

        if data.get("code") != "Ok":
            raise aiohttp.ClientError(
                f"OSRM table request failed with code={data.get('code')!r}"
            )

        distances = data["distances"]
        durations = data["durations"]
        degraded = False
        legs: list[list[RouteLeg]] = []
        for i in range(len(locations)):
            row: list[RouteLeg] = []
            for j in range(len(locations)):
                if i == j:
                    row.append(
                        RouteLeg(distance_miles=0.0, duration_minutes=0.0)
                    )
                    continue
                distance_m = distances[i][j]
                duration_s = durations[i][j]
                if distance_m is None or duration_s is None:
                    degraded = True
                    leg_degraded = True
                    distance_miles = (
                        geodesic(locations[i], locations[j]).miles
                        * self._geodesic.detour_factor
                    )
                    duration_minutes = (
                        distance_miles / self._geodesic.average_speed
                    ) * 60
                else:
                    leg_degraded = False
                    # OSRM distance -> METRES; duration -> SECONDS.
                    distance_miles = distance_m / 1609.344
                    duration_minutes = duration_s / 60.0
                row.append(
                    RouteLeg(
                        distance_miles=distance_miles,
                        duration_minutes=duration_minutes,
                        degraded=leg_degraded,
                    )
                )
            legs.append(row)
        return DistanceMatrix(
            locations=locations,
            legs=legs,
            backend=self.name,
            costing=self.costing,
            degraded=degraded,
        )

    async def route_shape(
        self, locations: list[Coordinate], session: aiohttp.ClientSession
    ) -> RouteShape:
        """Query OSRM ``/route`` and trace the ordered itinerary.

        Args:
            locations: Ordered (latitude, longitude) waypoints.
            session: Shared HTTP session.

        Returns:
            A ``RouteShape`` with distance converted metres -> miles and
            duration converted seconds -> minutes. Unlike Valhalla's
            ``/route``, OSRM has no ``units`` parameter, so this
            conversion IS required here.

        Raises:
            aiohttp.ClientError: If OSRM's ``code`` field is not ``"Ok"``.
        """
        # NOTE: OSRM path coordinates are `{longitude},{latitude}` — the
        # reverse of every internal (latitude, longitude) tuple.
        coords = ";".join(f"{lon},{lat}" for lat, lon in locations)
        url = (
            f"{self.service_url}/route/v1/driving/{coords}"
            "?overview=full&geometries=polyline6"
        )
        async with session.get(
            url, timeout=aiohttp.ClientTimeout(total=self.timeout)
        ) as response:
            response.raise_for_status()
            data = await response.json(content_type=None)

        if data.get("code") != "Ok":
            raise aiohttp.ClientError(
                f"OSRM route request failed with code={data.get('code')!r}"
            )

        route = data["routes"][0]
        points = polyline.decode(route["geometry"], 6)
        distance_miles = route["distance"] * 0.000621371
        duration_minutes = route["duration"] / 60.0

        return RouteShape(
            locations=locations,
            points=points,
            polyline6=polyline.encode(points, 6),
            distance_miles=distance_miles,
            duration_minutes=duration_minutes,
            backend=self.name,
            costing=self.costing,
            degraded=False,
        )


register_backend("valhalla", ValhallaBackend)
register_backend("osrm", OSRMBackend)


def _to_supported_ttl(duration: str) -> str:
    """Convert a human duration string to one `CacheSupport.parse_duration`
    (`flowtask/interfaces/cache.py:44`) actually supports.

    `CacheSupport.parse_duration` only recognizes ``s``/``m``/``h``
    suffixes; a ``d`` (days) suffix raises `ValueError`. Since
    `ROUTING_MATRIX_TTL` defaults to the day-suffixed ``"7d"``, convert it
    to an equivalent seconds value before it ever reaches `CacheSupport`.

    Args:
        duration: A human duration string (e.g. ``"7d"``, ``"60m"``, ``"2h"``).

    Returns:
        An equivalent duration string using a supported suffix.

    Raises:
        ValueError: If ``duration`` uses an unrecognized suffix.
    """
    if not duration:
        return duration
    unit = duration[-1]
    if unit in ("s", "m", "h"):
        return duration
    if unit == "d":
        value = int(duration[:-1])
        return f"{value * 86400}s"
    raise ValueError(f"Unsupported routing TTL unit: {duration!r}")


class RoutingService:
    """Backend-agnostic road-network distance/duration provider.

    Resolves a backend from configuration, serves N×N matrices with a
    Redis cache, and degrades to a geodesic estimate rather than raising
    when the routing engine is unavailable.
    """

    def __init__(
        self,
        backend: Optional[str] = None,
        service_url: Optional[str] = None,
        detour_factor: Optional[float] = None,
        costing: Optional[str] = None,
        average_speed: float = 40.0,
        matrix_ttl: Optional[str] = None,
        max_matrix_size: Optional[int] = None,
        timeout: Optional[int] = None,
        geometry_ttl: Optional[str] = None,
        max_route_locations: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the routing service.

        Args:
            backend: Backend name (``"valhalla"``, ``"osrm"``,
                ``"geodesic"``). Defaults to ``conf.ROUTING_BACKEND``.
            service_url: Backend service URL. Defaults to
                ``conf.ROUTING_SERVICE_URL``.
            detour_factor: Geodesic-fallback distance multiplier. Defaults
                to ``conf.ROUTING_DETOUR_FACTOR``.
            costing: Valhalla costing profile. Defaults to
                ``conf.ROUTING_COSTING``.
            average_speed: Geodesic-fallback speed in mph.
            matrix_ttl: Redis cache TTL as a human duration string.
                Defaults to ``conf.ROUTING_MATRIX_TTL``.
            max_matrix_size: Chunking threshold. Defaults to
                ``conf.ROUTING_MAX_MATRIX_SIZE``.
            timeout: Backend request timeout, in seconds. Defaults to
                ``conf.ROUTING_TIMEOUT``.
            geometry_ttl: Redis cache TTL for route shapes, as a human
                duration string. Defaults to ``conf.ROUTING_GEOMETRY_TTL``.
                Caches the lossless shape only (FEAT-235).
            max_route_locations: Pre-flight guard on itinerary length for
                ``route_shape()``. Defaults to
                ``conf.ROUTING_MAX_ROUTE_LOCATIONS`` (FEAT-235).
            **kwargs: ``max_retries``, ``backoff_base``,
                ``semaphore_limit``, ``redis_url`` overrides.
        """
        self.logger = logging.getLogger(__name__)
        self.backend_name = backend or ROUTING_BACKEND
        self.service_url = service_url or ROUTING_SERVICE_URL
        self.detour_factor = (
            detour_factor if detour_factor is not None else ROUTING_DETOUR_FACTOR
        )
        self.costing = costing or ROUTING_COSTING
        self.average_speed = average_speed
        self.matrix_ttl = matrix_ttl or ROUTING_MATRIX_TTL
        self.max_matrix_size = max_matrix_size or ROUTING_MAX_MATRIX_SIZE
        self.timeout = timeout or ROUTING_TIMEOUT
        self.geometry_ttl = geometry_ttl or ROUTING_GEOMETRY_TTL
        self.max_route_locations = (
            max_route_locations or ROUTING_MAX_ROUTE_LOCATIONS
        )

        self.max_retries: int = int(kwargs.pop("max_retries", 3))
        self.backoff_base: float = float(kwargs.pop("backoff_base", 2.0))
        self.semaphore_limit: int = int(
            kwargs.pop("semaphore_limit", HTTPCLIENT_MAX_SEMAPHORE)
        )
        self.redis_url: Optional[str] = kwargs.pop("redis_url", None)

        self._ttl = _to_supported_ttl(self.matrix_ttl)
        self._shape_ttl = _to_supported_ttl(self.geometry_ttl)
        self._geodesic = GeodesicBackend(
            detour_factor=self.detour_factor, average_speed=self.average_speed
        )
        self._backend: RoutingBackend = self._resolve_backend()

        self._session: Optional[aiohttp.ClientSession] = None
        self._semaphore: Optional[asyncio.Semaphore] = None
        self._cache: Optional[CacheSupport] = None

    def _resolve_backend(self) -> RoutingBackend:
        """Instantiate the configured backend from `_BACKEND_REGISTRY`."""
        if self.backend_name == "geodesic":
            return self._geodesic
        try:
            backend_cls = _BACKEND_REGISTRY[self.backend_name]
        except KeyError as exc:
            raise ValueError(
                f"Unknown routing backend {self.backend_name!r}; "
                f"registered backends: {sorted(_BACKEND_REGISTRY)}"
            ) from exc
        return backend_cls(
            service_url=self.service_url,
            costing=self.costing,
            timeout=self.timeout,
            detour_factor=self.detour_factor,
            average_speed=self.average_speed,
        )

    async def __aenter__(self) -> "RoutingService":
        """Open the shared HTTP session, semaphore, and Redis cache."""
        self._semaphore = asyncio.Semaphore(self.semaphore_limit)
        timeout = aiohttp.ClientTimeout(total=self.timeout + 30)
        resolver = AsyncResolver(nameservers=["1.1.1.1", "8.8.8.8"])
        connector = aiohttp.TCPConnector(
            limit=self.semaphore_limit * 2, resolver=resolver
        )
        self._session = aiohttp.ClientSession(
            connector=connector, timeout=timeout, trust_env=True
        )
        cache_kwargs = {"redis_url": self.redis_url} if self.redis_url else {}
        cache = CacheSupport(**cache_kwargs)
        try:
            await cache.open()
            self._cache = cache
        except Exception as exc:  # noqa: BLE001 — cache must never break routing
            self.logger.warning(
                "Routing matrix cache unavailable (%s); continuing without cache",
                exc,
            )
            self._cache = None
        return self

    async def __aexit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        """Close the shared HTTP session and Redis cache."""
        if self._session is not None and not self._session.closed:
            await self._session.close()
            self._session = None
        if self._cache is not None:
            try:
                await self._cache.close()
            except Exception:  # noqa: BLE001 — closing must never raise
                pass
            self._cache = None

    def _cache_key(self, locations: list[Coordinate]) -> str:
        """Derive a stable cache key from coordinates, backend and costing.

        Order-sensitive and precision-bound (6 decimals) so trivial float
        noise does not cause a miss, while a genuinely different location
        list, backend, or costing profile always produces a different key.
        """
        payload = {
            "locations": [round_coordinate(loc) for loc in locations],
            "backend": self.backend_name,
            "costing": self.costing,
        }
        blob = json.dumps(payload, sort_keys=True)
        digest = hashlib.sha256(blob.encode("utf-8")).hexdigest()
        return f"routing:matrix:{digest}"

    async def _cache_get(self, key: str) -> Optional[str]:
        """Read a cache entry, never raising on a cache failure."""
        if self._cache is None:
            return None
        try:
            value = await self._cache.get(key)
        except Exception as exc:  # noqa: BLE001 — cache must never break routing
            self.logger.warning(
                "Routing matrix cache read failed (%s); continuing without cache",
                exc,
            )
            return None
        return value

    async def _cache_set(
        self, key: str, value: str, ttl: Optional[str] = None
    ) -> None:
        """Write a cache entry, never raising on a cache failure.

        Args:
            key: The cache key to write.
            value: The serialized value to store.
            ttl: TTL override, already run through `_to_supported_ttl()`.
                Defaults to `self._ttl` (the matrix TTL) so existing
                `distance_matrix()` calls are unaffected.
        """
        if self._cache is None:
            return
        try:
            await self._cache.setex(key, value, ttl or self._ttl)
        except Exception as exc:  # noqa: BLE001 — cache must never break routing
            self.logger.warning(
                "Routing matrix cache write failed (%s); continuing", exc
            )

    def _shape_cache_key(self, locations: list[Coordinate]) -> str:
        """Derive a stable cache key for a route shape.

        Excludes the ``detail`` level so one entry serves both
        ``overview`` and ``full`` — only a different order, backend or
        costing profile produces a different key.
        """
        payload = {
            "locations": [round_coordinate(loc) for loc in locations],
            "backend": self.backend_name,
            "costing": self.costing,
        }
        blob = json.dumps(payload, sort_keys=True)
        digest = hashlib.sha256(blob.encode("utf-8")).hexdigest()
        return f"routing:shape:{digest}"

    async def _compute_with_retry(
        self, locations: list[Coordinate]
    ) -> DistanceMatrix:
        """Call the configured backend, retrying transient failures.

        Raises:
            aiohttp.ClientError | asyncio.TimeoutError: If every retry is
                exhausted. The caller degrades to geodesic on this.
                A non-retryable 4xx (any status in [400, 500) other than
                429) propagates immediately, on the first attempt, with
                no backoff — such an error can never succeed on retry.
        """
        attempt = 0
        while True:
            try:
                return await self._backend.matrix(locations, session=self._session)
            except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
                status = getattr(exc, "status", None)
                if status is not None and 400 <= status < 500 and status != 429:
                    self.logger.error(
                        "Routing backend %s call failed with non-retryable "
                        "status %d: %s — not retrying",
                        self._backend.name, status, exc,
                    )
                    raise
                attempt += 1
                if attempt > self.max_retries:
                    raise
                delay = self.backoff_base ** attempt
                headers = getattr(exc, "headers", None)
                if headers:
                    retry_after = headers.get("Retry-After")
                    if retry_after:
                        try:
                            delay = max(delay, float(retry_after))
                        except (TypeError, ValueError):
                            pass
                delay += random.uniform(0, 1.5)
                self.logger.warning(
                    "Routing backend %s call failed (attempt %d/%d): %s",
                    self._backend.name, attempt, self.max_retries, exc,
                )
                await asyncio.sleep(delay)

    async def _compute_chunked(
        self, locations: list[Coordinate]
    ) -> DistanceMatrix:
        """Reassemble a complete matrix from source/target batches.

        Splits ``locations`` into batches of at most `max_matrix_size`,
        computes one matrix per batch pair (diagonal blocks alone,
        off-diagonal blocks as their concatenation), then rebuilds the
        full N×N matrix by looking up each original pair from whichever
        computed sub-matrix contains it.

        This is a guard rail, not production-hardened chunking: it makes
        O(batches^2) backend calls and each off-diagonal call redundantly
        recomputes the two diagonal blocks it straddles. Per-employee
        granularity (the spec's chosen matrix scope) keeps `N` at roughly
        20-60, i.e. one to three batches under the default `max_matrix_size`
        (25), so this path is exercised routinely at this scope. If
        per-employee granularity is relaxed to a coarser (e.g. per-market)
        scope, revisit this for a single-pass reassembly instead.

        IMPORTANT — 2x off-diagonal amplification (FEAT-235 Module 5): an
        off-diagonal block sends `batch_i + batch_j`, i.e. **twice**
        `max_matrix_size` locations in one request, not `max_matrix_size`.
        `max_matrix_size` therefore caps the emitted request size at
        `2 * max_matrix_size` locations, which is why the default is 25
        (`2 x 25 = 50` locations `= 2500` pairs, Valhalla's
        `max_matrix_location_pairs` ceiling for `auto`) rather than 50.
        """
        size = self.max_matrix_size
        batches = [
            locations[i : i + size] for i in range(0, len(locations), size)
        ]
        computed: list[DistanceMatrix] = []
        for i, batch_i in enumerate(batches):
            for batch_j in batches[i:]:
                combined = batch_i if batch_i is batch_j else batch_i + batch_j
                computed.append(await self._compute_with_retry(combined))

        legs: list[list[RouteLeg]] = []
        for origin in locations:
            row: list[RouteLeg] = []
            for destination in locations:
                leg: Optional[RouteLeg] = None
                for sub_matrix in computed:
                    try:
                        leg = sub_matrix.lookup(origin, destination)
                        break
                    except KeyError:
                        continue
                if leg is None:
                    raise RuntimeError(
                        "Chunked routing matrix reassembly failed to find "
                        f"a leg for {origin} -> {destination}"
                    )
                row.append(leg)
            legs.append(row)
        return DistanceMatrix(
            locations=locations,
            legs=legs,
            backend=self._backend.name,
            costing=self.costing,
            degraded=any(m.degraded for m in computed),
        )

    async def _compute(self, locations: list[Coordinate]) -> DistanceMatrix:
        """Compute a full matrix, chunking above `max_matrix_size`."""
        if len(locations) > self.max_matrix_size:
            return await self._compute_chunked(locations)
        return await self._compute_with_retry(locations)

    async def distance_matrix(
        self, locations: list[Coordinate]
    ) -> DistanceMatrix:
        """Return the N×N matrix for ``locations`` (cache -> backend -> fallback).

        Never raises on backend failure; returns a `degraded=True` matrix
        instead. A cache failure is likewise swallowed and logged.

        Args:
            locations: Ordered (latitude, longitude) pairs.

        Returns:
            A `DistanceMatrix` covering every pair in ``locations``.
        """
        key = self._cache_key(locations)
        cached = await self._cache_get(key)
        if cached is not None:
            try:
                return DistanceMatrix.model_validate_json(cached)
            except Exception as exc:  # noqa: BLE001 — a bad cache entry is not fatal
                self.logger.warning(
                    "Routing matrix cache entry unreadable (%s); recomputing",
                    exc,
                )
        try:
            matrix = await self._compute(locations)
        except Exception as exc:  # noqa: BLE001 — deliberate: never break a run
            self.logger.warning(
                "Routing backend %s unavailable (%s); degrading to geodesic",
                self._backend.name, exc,
            )
            fallback_matrix = await self._geodesic.matrix(locations, session=None)
            return fallback_matrix.model_copy(update={"degraded": True})
        # Degraded matrices are not cached: caching them would keep serving
        # a geodesic estimate for the full TTL even after the backend heals.
        if not matrix.degraded:
            await self._cache_set(key, matrix.model_dump_json())
        return matrix

    async def _route_shape_with_retry(
        self, locations: list[Coordinate]
    ) -> RouteShape:
        """Call the configured backend's `route_shape()`, retrying transient
        failures with the same discipline as `_compute_with_retry()`.

        Raises:
            aiohttp.ClientError | asyncio.TimeoutError: If every retry is
                exhausted. The caller degrades to a geodesic shape on
                this. A non-retryable 4xx (any status in [400, 500)
                other than 429) propagates immediately, on the first
                attempt, with no backoff.
        """
        attempt = 0
        while True:
            try:
                return await self._backend.route_shape(
                    locations, session=self._session
                )
            except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
                status = getattr(exc, "status", None)
                if status is not None and 400 <= status < 500 and status != 429:
                    self.logger.error(
                        "Routing backend %s route_shape call failed with "
                        "non-retryable status %d: %s — not retrying",
                        self._backend.name, status, exc,
                    )
                    raise
                attempt += 1
                if attempt > self.max_retries:
                    raise
                delay = self.backoff_base ** attempt
                headers = getattr(exc, "headers", None)
                if headers:
                    retry_after = headers.get("Retry-After")
                    if retry_after:
                        try:
                            delay = max(delay, float(retry_after))
                        except (TypeError, ValueError):
                            pass
                delay += random.uniform(0, 1.5)
                self.logger.warning(
                    "Routing backend %s route_shape call failed "
                    "(attempt %d/%d): %s",
                    self._backend.name, attempt, self.max_retries, exc,
                )
                await asyncio.sleep(delay)

    def _apply_detail(
        self, shape: RouteShape, detail: GeometryDetail
    ) -> RouteShape:
        """Apply the requested detail level to an already-fetched shape.

        ``"none"`` is a component-level concept (whether to fetch
        geometry at all) and should never reach this method; if it
        does, it is treated as ``"full"`` (returned unchanged) since a
        shape has already been fetched or fallen back to by this point.
        """
        if detail == "overview":
            return shape.simplified(ROUTING_SIMPLIFY_TOLERANCE_M)
        return shape

    async def route_shape(
        self,
        locations: list[Coordinate],
        detail: GeometryDetail = "full",
    ) -> RouteShape:
        """Return the traced path for an ordered itinerary.

        Cache -> backend -> geodesic fallback. Never raises on backend
        failure; returns a ``degraded=True`` straight-line shape
        instead. Caches the LOSSLESS shape; ``detail`` is applied after
        the cache read, so one entry serves every detail level.

        Args:
            locations: Ordered (latitude, longitude) waypoints;
                ``locations[i] -> locations[i + 1]`` is one leg.
            detail: ``"overview"`` simplifies the returned ``points``
                via `RouteShape.simplified()`; ``"full"`` (default)
                and ``"none"`` return them unchanged.

        Returns:
            A ``RouteShape`` for the itinerary. Degraded when the
            backend is unavailable, when the backend reports a failed
            trip, or when ``locations`` exceeds
            ``conf.ROUTING_MAX_ROUTE_LOCATIONS`` (checked pre-flight,
            before any HTTP call is made).
        """
        if len(locations) > self.max_route_locations:
            self.logger.warning(
                "Itinerary of %d stops exceeds ROUTING_MAX_ROUTE_LOCATIONS "
                "(%d); degrading to a straight-line shape without "
                "calling %s",
                len(locations), self.max_route_locations, self._backend.name,
            )
            shape = await self._geodesic.route_shape(locations, session=None)
            # GeodesicBackend.route_shape() already sets degraded=True;
            # the explicit model_copy() here is a no-op kept only for
            # symmetry with distance_matrix()'s equivalent fallback (see
            # the docstring note on GeodesicBackend.matrix() above) and
            # to stay correct if that backend's default ever changes.
            return self._apply_detail(
                shape.model_copy(update={"degraded": True}), detail
            )

        key = self._shape_cache_key(locations)
        cached = await self._cache_get(key)
        if cached is not None:
            try:
                return self._apply_detail(
                    RouteShape.model_validate_json(cached), detail
                )
            except Exception as exc:  # noqa: BLE001 — a bad cache entry is not fatal
                self.logger.warning(
                    "Routing shape cache entry unreadable (%s); recomputing",
                    exc,
                )
        try:
            shape = await self._route_shape_with_retry(locations)
        except Exception as exc:  # noqa: BLE001 — deliberate: never break a run
            self.logger.warning(
                "Routing backend %s unavailable for geometry (%s); "
                "degrading to geodesic",
                self._backend.name, exc,
            )
            fallback = await self._geodesic.route_shape(locations, session=None)
            # Same no-op-but-explicit degraded=True as the pre-flight
            # branch above — see that comment.
            return self._apply_detail(
                fallback.model_copy(update={"degraded": True}), detail
            )
        # Degraded shapes are not cached, and only the LOSSLESS shape is
        # ever written — simplification happens at serve time via
        # `_apply_detail()`, so one entry serves every detail level.
        if not shape.degraded:
            await self._cache_set(
                key, shape.model_dump_json(), ttl=self._shape_ttl
            )
        return self._apply_detail(shape, detail)
