"""The nearest town to a GPS position, offline, from a GeoNames extract.

The console's GPS location row reads "Near Denver, CO" rather than bare coordinates.
The names come from `places.tsv.gz` beside this file: GeoNames populated places,
trimmed and compressed by `scripts/build-place-names.py`, which records the source,
download date and population floor in the file's header. No network call is made at
build or run time, so no cube's position is ever sent to a geocoder.

Rendering: "Town, ST" in the US, where GeoNames' admin-1 code already is the postal
code, and "Town, Country" elsewhere, with the country's name rather than its code.

Four rules:

1. **Loaded on first use, never at import.** The file is ~150k rows; importing the
   app must stay cheap, and the service must start whatever state the file is in.
   `ready()` does the first load off the event loop.
2. **A missing or unreadable file costs the town, nothing else.** It is logged once,
   by exception type only, and remembered: every later lookup answers None without
   touching the disk again, so a broken file cannot become a read per request. The
   row then shows coordinates. The image build runs `check()` so a missing file is
   caught before it ships.
3. **"Near" must mean near.** Beyond `MAX_DISTANCE_KM` there is no town, rather than
   the closest one an ocean away (a bogus 0,0 reading would otherwise be "Near"
   somewhere in Ghana).
4. **The nearest place, provably.** The fleet map names every visible cube per
   request, so a linear scan per lookup is too slow. Places sit in 1° latitude x 1°
   longitude cells, searched in rings outward from the query's cell until no
   unsearched cell can hold anything closer than the best found.
"""

from __future__ import annotations

import asyncio
import gzip
import logging
import math
import threading
from array import array
from pathlib import Path

logger = logging.getLogger(__name__)

#: The shipped extract. A module attribute, read at load time, so tests can point it
#: elsewhere.
DATA_PATH = Path(__file__).with_name("places.tsv.gz")

#: The first line a places file must carry, so a raw GeoNames dump (or anything
#: else) dropped in by mistake is refused rather than half-read.
FORMAT_LINE = "# format: places/1"

#: Farther than this from every place, a position gets no town.
MAX_DISTANCE_KM = 100.0

#: Mean Earth radius (IUGG), the usual figure for great-circle distance.
EARTH_RADIUS_KM = 6371.0088

#: Admin-1 codes are postal codes here, so "Town, ST" needs no extra table.
_STATE_COUNTRIES = frozenset({"US"})


class _Index:
    """Places bucketed by 1° cell. Each cell holds unit vectors (x, y, z flattened
    into one array, so 150k places cost 3.6 MB of floats rather than 150k tuples)
    and the matching labels."""

    __slots__ = ("cells", "count")

    def __init__(self) -> None:
        self.cells: dict[tuple[int, int], tuple[array, list[str]]] = {}
        self.count = 0

    def add(self, lat: float, lng: float, label: str) -> None:
        key = (_cell_lat(lat), _cell_lng(lng))
        cell = self.cells.get(key)
        if cell is None:
            cell = self.cells[key] = (array("d"), [])
        cell[0].extend(_unit(lat, lng))
        cell[1].append(label)
        self.count += 1


# Process state. `_index` is None until the first load; `_failed` remembers a failed
# load for the life of the process (rule 2).
_index: _Index | None = None
_failed = False
_lock = threading.Lock()


def reset() -> None:
    """Forget whatever was loaded or failed. For tests."""
    global _index, _failed
    with _lock:
        _index = None
        _failed = False


def is_loaded() -> bool:
    return _index is not None


def _cell_lat(lat: float) -> int:
    # 90°N belongs to the top row of cells, not a row of its own.
    return min(89, math.floor(lat))


def _cell_lng(lng: float) -> int:
    # 180°E is 180°W.
    return (math.floor(lng) + 180) % 360 - 180


def _unit(lat: float, lng: float) -> tuple[float, float, float]:
    p, l = math.radians(lat), math.radians(lng)
    return (math.cos(p) * math.cos(l), math.cos(p) * math.sin(l), math.sin(p))


def _label(name: str, admin1: str, country: str, countries: dict[str, str]) -> str:
    if country in _STATE_COUNTRIES and admin1:
        return f"{name}, {admin1}"
    return f"{name}, {countries.get(country) or country}"


def _open_text(path: Path):
    # The shipped file is gzipped; the test fixture is plain text so it can be read
    # in review.
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8")
    return open(path, encoding="utf-8")


def _load(path: Path) -> _Index:
    """Read a places file. Raises on anything unexpected: a partly-read file would
    name some towns wrong with nothing to say so."""
    countries: dict[str, str] = {}
    rows: list[tuple[str, str, str, float, float]] = []
    with _open_text(path) as f:
        first = f.readline().rstrip("\n")
        if first != FORMAT_LINE:
            raise ValueError("not a places file")
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if parts[0] == "C" and len(parts) == 3:
                countries[parts[1]] = parts[2]
            elif parts[0] == "P" and len(parts) == 6:
                lat, lng = float(parts[4]), float(parts[5])
                if not (-90.0 <= lat <= 90.0 and -180.0 <= lng <= 180.0):
                    raise ValueError("coordinate out of range")
                rows.append((parts[1], parts[2], parts[3], lat, lng))
            else:
                raise ValueError("malformed row")
    if not rows:
        raise ValueError("no places")
    index = _Index()
    for name, admin1, country, lat, lng in rows:
        index.add(lat, lng, _label(name, admin1, country, countries))
    return index


def _get() -> _Index | None:
    """The index, loading it on first use. None if the file could not be read."""
    global _index, _failed
    if _index is not None:
        return _index
    if _failed:
        return None
    with _lock:
        if _index is None and not _failed:
            try:
                _index = _load(DATA_PATH)
                logger.info("place names loaded: %d places", _index.count)
            except Exception as exc:  # noqa: BLE001 - any failure means "no towns"
                _failed = True
                # Type only: the message can carry a path or a line of the file.
                logger.warning(
                    "place names unavailable, showing coordinates only: %s",
                    type(exc).__name__,
                )
    return _index


async def ready() -> None:
    """Load the file, if not yet tried, without blocking the event loop."""
    if _index is None and not _failed:
        await asyncio.to_thread(_get)


def check(path: Path | None = None) -> int:
    """Read a places file strictly and return its place count. Raises on failure.

    For the image build, which must fail on a missing or broken file rather than
    ship an image that silently shows coordinates everywhere.
    """
    return _load(path or DATA_PATH).count


def nearest_place(lat: float | None, lng: float | None) -> str | None:
    """The nearest town to (lat, lng), e.g. "Denver, CO" or "Toronto, Canada".

    None when there is no position, no town within `MAX_DISTANCE_KM`, or the place
    file could not be read.
    """
    try:
        lat, lng = float(lat), float(lng)
    except (TypeError, ValueError):
        return None
    if not (-90.0 <= lat <= 90.0 and -180.0 <= lng <= 180.0):
        return None  # also NaN, which fails every comparison
    index = _get()
    if index is None:
        return None
    return _search(index, lat, lng)


def _search(index: _Index, lat: float, lng: float) -> str | None:
    if lng >= 180.0:
        lng -= 360.0  # 180°E is 180°W, which keeps the block edges below in range
    qx, qy, qz = _unit(lat, lng)
    ci, cj = _cell_lat(lat), _cell_lng(lng)
    cos_lat = math.cos(math.radians(lat))
    max_angle = MAX_DISTANCE_KM / EARTH_RADIUS_KM
    # Ordering by dot product of unit vectors is ordering by great-circle distance,
    # and needs no trigonometry per candidate.
    best_dot, best = math.cos(max_angle), None
    cells = index.cells
    r = 0
    while True:
        for i, j in _ring(ci, cj, r):
            cell = cells.get((i, j))
            if cell is None:
                continue
            xyz, labels = cell
            for k in range(len(labels)):
                d = qx * xyz[3 * k] + qy * xyz[3 * k + 1] + qz * xyz[3 * k + 2]
                if d > best_dot:
                    best_dot, best = d, labels[k]
        # Everything within `r` cells is searched. Stop once nothing outside that
        # block can beat the best so far (or the cap, if nothing is found yet).
        best_angle = math.acos(max(-1.0, min(1.0, best_dot)))
        if _outside_bound(lat, lng, ci, cj, r, cos_lat) > best_angle:
            return best
        r += 1


def _ring(ci: int, cj: int, r: int):
    """The cells exactly `r` steps from (ci, cj), longitude wrapping, latitude not."""
    if r == 0:
        yield ci, cj
        return
    for di in range(-r, r + 1):
        i = ci + di
        if i < -90 or i > 89:
            continue
        if abs(di) == r:
            steps = range(-r, r + 1)
        else:
            steps = (-r, r)
        for dj in steps:
            yield i, (cj + dj + 180) % 360 - 180


def _outside_bound(lat, lng, ci, cj, r, cos_lat) -> float:
    """A lower bound, in radians, on the distance from (lat, lng) to any point
    outside the block of cells within `r` of (ci, cj).

    To leave the block a path must cross its latitude edges or its longitude edges.
    Latitude: any two points are at least their latitude difference apart. Longitude:
    the edges lie on meridians, which are great circles, and the distance from a
    point to the meridian `d` degrees of longitude away is asin(cos(lat) * sin(d)),
    valid while d <= 90°. Past that the bound is 0 and the search simply widens
    until the block covers the globe.
    """
    south = lat - (ci - r) if ci - r > -90 else math.inf
    north = (ci + r + 1) - lat if ci + r + 1 < 90 else math.inf
    lat_bound = math.radians(min(south, north))
    if 2 * r + 1 >= 360:
        lng_bound = math.inf
    else:
        west = lng - (cj - r)
        east = (cj + r + 1) - lng
        d = min(west, east)
        lng_bound = math.asin(cos_lat * math.sin(math.radians(d))) if d < 90 else 0.0
    return min(lat_bound, lng_bound)
