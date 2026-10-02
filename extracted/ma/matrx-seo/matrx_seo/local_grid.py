"""Local SEO rank grid — pure geometry, matching and summary (no I/O).

Contract: ``common-docs/projects/outside-skill-packs/OPENSEO-TOOLS-SPEC.md`` §5.4.
Reference behavior: every-app/open-seo at ``0ffff93``,
``src/server/mcp/tools/local-seo-tools.ts`` (``buildRankGridPoints``,
``rankGridZoom``, ``matchGridItem``, ``renderGrid``) and
``local-seo-shared.ts`` (coordinate formatters). Their test vectors are pinned in
``tests/test_local_grid.py``.

What a grid is: one Google Maps search per point of a square around a center,
so a business can see how far its Maps presence reaches. Three things make the
numbers honest, and all three live here so every caller gets them:

* **Geometry** — row 0 is the NORTH edge (the rendered grid reads like a map);
  ``lat_step = spacing/110.574``, ``lon_step = spacing/(111.32·max(|cos lat|, 0.01))``
  (the floor keeps a near-polar center from exploding); every coordinate is
  rounded to 7 decimals.
* **Zoom** — without an explicit zoom the provider infers one per point, which
  yields "No Search Results" at some points and incomparable ranks; a fixed zoom
  fails the other way (a business one grid step east falls outside a zoom-14
  viewport). So the zoom is DERIVED from the spacing:
  ``clamp(floor(log2(24045·cos(lat)/spacing)), 4, 18)`` and sent explicitly.
* **A null rank is read against the result count** — "not found among 20 full
  results" (outranked) and "not found among 3 results" (a sparse SERP) are
  different sentences to a person, so :func:`null_rank_reading` says which.

Matching precedence (census §3.4, spec §5.4): **cid, then place_id, then a
case-insensitive title substring**, across ALL rows — a later row with the exact
cid beats an earlier row whose title merely contains the name.
"""

from __future__ import annotations

import asyncio
import contextlib
import math
import re
from collections.abc import Awaitable, Callable, Iterable, Sequence
from dataclasses import dataclass, field
from typing import Any, Literal

KM_PER_DEGREE_LATITUDE = 110.574
KM_PER_DEGREE_LONGITUDE = 111.32
MIN_LONGITUDE_COSINE = 0.01
#: A world tile is 40075·cos(lat)/2^z km wide and a portrait viewport ~1.5
#: tiles, so the largest zoom whose viewport still spans ~1.25× the spacing is
#: log2(24045·cos(lat)/spacing) (their derivation, verified live by them).
ZOOM_NUMERATOR_KM = 24045
MIN_ZOOM = 4
MAX_ZOOM = 18
ALLOWED_GRID_SIZES = (3, 5)
MIN_SPACING_KM = 0.25
MAX_SPACING_KM = 10.0

#: Google business_data endpoints take a coordinate radius in METERS (clamped
#: 200–199,999); business_listings/search takes whole KILOMETERS (≥1; it rejects
#: fractional radii). Everything upstream speaks kilometers.
BUSINESS_DATA_MIN_RADIUS_M = 200
BUSINESS_DATA_MAX_RADIUS_M = 199_999

MatchedBy = Literal["cid", "place_id", "name"]


def format_coordinate(value: float) -> str:
    """7-decimal coordinate with trailing zeros dropped — JS
    ``Number(v.toFixed(7)).toString()``: ``40.0`` → ``"40"``."""
    text = f"{round(float(value), 7):.7f}".rstrip("0").rstrip(".")
    return "0" if text in ("-0", "") else text


def _cosine(latitude: float) -> float:
    return max(abs(math.cos(math.radians(latitude))), MIN_LONGITUDE_COSINE)


def grid_zoom(spacing_km: float, latitude: float) -> int:
    """The Maps zoom every grid point is searched at (see module docstring)."""
    if spacing_km <= 0:
        raise ValueError("spacing_km must be positive")
    zoom = math.floor(math.log2(ZOOM_NUMERATOR_KM * _cosine(latitude) / spacing_km))
    return min(MAX_ZOOM, max(MIN_ZOOM, zoom))


@dataclass(frozen=True)
class GridPoint:
    row: int
    col: int
    lat: float
    lng: float


def build_grid(
    center_lat: float, center_lng: float, size: int, spacing_km: float
) -> list[GridPoint]:
    """Row-major points, row 0 the northern edge, coordinates rounded to 7 dp."""
    if size not in ALLOWED_GRID_SIZES:
        raise ValueError(f"grid_size must be one of {ALLOWED_GRID_SIZES}, got {size}")
    if not (MIN_SPACING_KM <= spacing_km <= MAX_SPACING_KM):
        raise ValueError(
            f"spacing_km must be between {MIN_SPACING_KM} and {MAX_SPACING_KM}, got {spacing_km}"
        )
    if not (-90 <= center_lat <= 90 and -180 <= center_lng <= 180):
        raise ValueError(f"center ({center_lat}, {center_lng}) is not a valid coordinate")
    middle = (size - 1) / 2
    lat_step = spacing_km / KM_PER_DEGREE_LATITUDE
    lon_step = spacing_km / (KM_PER_DEGREE_LONGITUDE * _cosine(center_lat))
    return [
        GridPoint(
            row=row,
            col=col,
            lat=round(center_lat + (middle - row) * lat_step, 7),
            lng=round(center_lng + (col - middle) * lon_step, 7),
        )
        for row in range(size)
        for col in range(size)
    ]


def maps_coordinate(lat: float, lng: float, zoom: int | None = None) -> str:
    """``"lat,lng"`` with an optional ``,<zoom>z`` — the Maps / Local Finder form."""
    base = f"{format_coordinate(lat)},{format_coordinate(lng)}"
    return base if zoom is None else f"{base},{int(zoom)}z"


def listing_search_coordinate(lat: float, lng: float, radius_km: float) -> str:
    """``"lat,lng,radius_km"`` for business_listings/search — whole km, at least 1."""
    radius = max(1, round(float(radius_km)))
    return f"{format_coordinate(lat)},{format_coordinate(lng)},{radius}"


def business_data_coordinate(lat: float, lng: float, radius_km: float) -> str:
    """``"lat,lng,radius_m"`` for Google business_data endpoints — meters, clamped."""
    radius_m = min(
        BUSINESS_DATA_MAX_RADIUS_M, max(BUSINESS_DATA_MIN_RADIUS_M, round(float(radius_km) * 1000))
    )
    return f"{format_coordinate(lat)},{format_coordinate(lng)},{radius_m}"


def distance_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Great-circle distance (haversine, mean Earth radius 6371.0088 km)."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * 6371.0088 * math.asin(min(1.0, math.sqrt(a)))


# ── matching ──────────────────────────────────────────────────────────────


def _text(value: Any) -> str | None:
    return value if isinstance(value, str) and value.strip() else None


def match_business(
    items: Sequence[Any],
    *,
    cid: str | None = None,
    place_id: str | None = None,
    name: str | None = None,
) -> tuple[dict[str, Any] | None, MatchedBy | None]:
    """The row that is the target business, and how it was matched.

    Precedence across ALL rows: an exact ``cid``, then an exact ``place_id``,
    then a case-insensitive substring of ``title``. Returns ``(None, None)``
    when nothing matches."""
    rows = [item for item in items if isinstance(item, dict)]
    if cid:
        for item in rows:
            if str(item.get("cid") or "") == str(cid):
                return item, "cid"
    if place_id:
        for item in rows:
            if str(item.get("place_id") or "") == str(place_id):
                return item, "place_id"
    needle = (name or "").strip().casefold()
    if needle:
        for item in rows:
            title = _text(item.get("title"))
            if title and needle in title.casefold():
                return item, "name"
    return None, None


def item_rank(item: dict[str, Any] | None) -> int | None:
    """The provider's rank for a row: ``rank_absolute``, else ``rank_group``."""
    if item is None:
        return None
    for key in ("rank_absolute", "rank_group"):
        value = item.get(key)
        if isinstance(value, int) and not isinstance(value, bool):
            return value
    return None


# ── one point, the run, the summary ───────────────────────────────────────


@dataclass
class PointResult:
    row: int
    col: int
    lat: float
    lng: float
    rank: int | None = None
    results_count: int | None = None
    top_result: dict[str, Any] | None = None
    error: str | None = None
    run_id: str | None = None
    reused: bool = False
    #: Never dispatched: the dispatch budget ran out first. Never billed.
    pending: bool = False
    extra: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "row": self.row,
            "col": self.col,
            "lat": self.lat,
            "lng": self.lng,
            "rank": self.rank,
            "results_count": self.results_count,
            "top_result": self.top_result,
        }
        if self.error is not None:
            out["error"] = self.error
        if self.run_id is not None:
            out["run_id"] = self.run_id
        if self.pending:
            out["pending"] = True
        return out


def point_from_items(
    point: GridPoint,
    items: Sequence[Any],
    *,
    cid: str | None,
    place_id: str | None,
    name: str | None,
) -> tuple[PointResult, dict[str, Any] | None, MatchedBy | None]:
    """Score one point's SERP rows: the target's rank, how many rows came back,
    and who ranked first — so a null rank is interpretable."""
    rows = [item for item in items if isinstance(item, dict)]
    match, matched_by = match_business(rows, cid=cid, place_id=place_id, name=name)
    first = rows[0] if rows else None
    top = (
        None
        if first is None
        else {"name": _text(first.get("title")), "cid": _text(str(first.get("cid") or ""))}
    )
    return (
        PointResult(
            row=point.row,
            col=point.col,
            lat=point.lat,
            lng=point.lng,
            rank=item_rank(match),
            results_count=len(rows),
            top_result=top,
        ),
        match,
        matched_by,
    )


PointOutcome = Literal["abort", "empty", "point"]

#: DataForSEO status codes that mean every remaining call would fail (and
#: possibly bill) the same way: 401xx authentication, 402xx payment/balance.
_ABORT_CODE_RE = re.compile(r"\b40[12]\d\d\b")
_ABORT_WORDS = (
    "payment required",
    "insufficient",
    "not enough funds",
    "balance",
    "authentication failed",
    "not authorized",
    "unauthorized",
    "credential is missing",
    "credentials",
)
_ABORT_TYPES = frozenset(
    {
        "BudgetExceededError",
        "SpendApprovalExceededError",
        "SecretNotFoundError",
        "PermissionError",
    }
)
#: 40501 "No Search Results": a valid, billed, EMPTY answer — never an error.
_EMPTY_RE = re.compile(r"\b40501\b|no search results", re.IGNORECASE)


def classify_point_failure(type_name: str, text: str) -> PointOutcome:
    """What one failed grid point means for the rest of the grid.

    ``abort`` — insufficient credit, provider authentication, or one of our own
    spend/credential gates: every remaining point would fail the same way, so
    stop dispatching. ``empty`` — "No Search Results": the point searched fine
    and nobody is listed there. ``point`` — only this point failed; keep going
    and mark it (it may still have been charged)."""
    lowered = (text or "").casefold()
    if _EMPTY_RE.search(text or ""):
        return "empty"
    if type_name in _ABORT_TYPES:
        return "abort"
    if _ABORT_CODE_RE.search(text or "") or any(word in lowered for word in _ABORT_WORDS):
        return "abort"
    return "point"


class GridAborted(RuntimeError):
    """A point failed in a way every remaining point would repeat. Carries the
    points already searched so the caller can say what was spent."""

    def __init__(self, cause: BaseException, searched: list[PointResult]) -> None:
        self.cause = cause
        self.searched = searched
        super().__init__(str(cause))


class GridAllFailed(RuntimeError):
    """Every point failed: a systemic failure, never "does not rank"."""

    def __init__(self, last: BaseException, searched: list[PointResult]) -> None:
        self.last = last
        self.searched = searched
        super().__init__(str(last))


#: What a point's error says the agent should do next.
RETRY_SENTENCE = "call rank_grid again with the same arguments to retry it"


def point_error(cause: str) -> str:
    """A failed point's error: the cause, the money, and the next step."""
    cause = " ".join(str(cause).split())[:240] or "unknown error"
    return f"failed: {cause}; may still be charged — {RETRY_SENTENCE}"


TIMED_OUT = (
    "stopped at the dispatch budget while the provider call was still running; "
    "may still be charged — " + RETRY_SENTENCE
)


async def run_grid(
    points: Sequence[GridPoint],
    search: Callable[[GridPoint], Awaitable[PointResult]],
    *,
    concurrency: int,
    deadline: float | None = None,
    clock: Callable[[], float] | None = None,
) -> list[PointResult]:
    """Search every point, ``concurrency`` at a time, in row-major order.

    ``search`` returns the scored point or raises. An ``empty`` failure becomes
    a searched point with 0 results; a ``point`` failure is marked ``error``
    with its cause and next step, and the grid continues; an ``abort`` failure
    stops the remaining batches from dispatching (and billing) and raises
    :class:`GridAborted`. If every point failed, raises :class:`GridAllFailed`
    with the last error — never an empty grid that reads as "does not rank".

    ``deadline`` (on ``clock``, default ``time.monotonic``) is the dispatch
    budget: a batch is dispatched only when the budget still covers the slowest
    batch seen so far, the rest are returned ``pending`` (never dispatched, never
    billed), and a batch still running at the deadline is stopped with its
    points marked as such — so a grid always RETURNS inside the budget instead of
    dying as a bare timeout after spending."""
    import time

    if concurrency < 1:
        raise ValueError("concurrency must be at least 1")
    now = clock or time.monotonic
    results: list[PointResult] = []
    last_error: BaseException | None = None
    slowest_batch = 0.0

    async def one(point: GridPoint) -> PointResult | BaseException:
        try:
            return await search(point)
        except Exception as exc:  # noqa: BLE001 — classified below, never swallowed
            return exc

    def mark_pending(rest: Sequence[GridPoint]) -> None:
        for p in rest:
            results.append(PointResult(row=p.row, col=p.col, lat=p.lat, lng=p.lng, pending=True))

    for start in range(0, len(points), concurrency):
        batch = list(points[start : start + concurrency])
        if deadline is not None and start > 0 and deadline - now() < slowest_batch:
            mark_pending(points[start:])
            break
        started = now()
        tasks = [asyncio.ensure_future(one(p)) for p in batch]
        if deadline is None:
            await asyncio.wait(tasks)
        else:
            await asyncio.wait(tasks, timeout=max(deadline - now(), 0))
        slowest_batch = max(slowest_batch, now() - started)
        abort: BaseException | None = None
        for point, task in zip(batch, tasks, strict=True):
            if not task.done():
                task.cancel()
                with contextlib.suppress(asyncio.CancelledError, Exception):
                    await task
                results.append(
                    PointResult(
                        row=point.row, col=point.col, lat=point.lat, lng=point.lng, error=TIMED_OUT
                    )
                )
                continue
            outcome = task.result()
            if isinstance(outcome, PointResult):
                results.append(outcome)
                continue
            kind = classify_point_failure(type(outcome).__name__, _failure_text(outcome))
            if kind == "empty":
                results.append(
                    PointResult(
                        row=point.row,
                        col=point.col,
                        lat=point.lat,
                        lng=point.lng,
                        rank=None,
                        results_count=0,
                        top_result=None,
                        run_id=getattr(outcome, "run_id", None),
                    )
                )
                continue
            last_error = outcome
            results.append(
                PointResult(
                    row=point.row,
                    col=point.col,
                    lat=point.lat,
                    lng=point.lng,
                    error=point_error(str(outcome)),
                    run_id=getattr(outcome, "run_id", None),
                )
            )
            if kind == "abort" and abort is None:
                abort = outcome
        if abort is not None:
            raise GridAborted(abort, results)
        if deadline is not None and now() >= deadline and start + concurrency < len(points):
            mark_pending(points[start + concurrency :])
            break
    searched = [r for r in results if not r.pending]
    if searched and all(r.error is not None for r in searched) and last_error is not None:
        raise GridAllFailed(last_error, results)
    return results


def _failure_text(exc: BaseException) -> str:
    parts = [str(exc)]
    error = getattr(exc, "error", None)
    if isinstance(error, dict):
        parts.append(repr(error))
    return " ".join(parts)


def summarize(points: Iterable[PointResult]) -> dict[str, Any]:
    """``{points_found, points_searched, avg_rank (2 dp), top3, top10}`` over the
    points that searched (a failed point is searched-and-failed, never found)."""
    pts = list(points)
    searched = [p for p in pts if not p.pending]
    ranks = [p.rank for p in pts if p.rank is not None]
    return {
        "points_found": len(ranks),
        "points_searched": len(searched),
        "points_failed": sum(1 for p in pts if p.error is not None),
        "points_pending": sum(1 for p in pts if p.pending),
        "avg_rank": round(sum(ranks) / len(ranks), 2) if ranks else None,
        "top3": sum(1 for r in ranks if r <= 3),
        "top10": sum(1 for r in ranks if r <= 10),
    }


def render_grid(points: Sequence[PointResult], size: int) -> str:
    """Rank per point, north at the top: ``–`` not found, ``x`` failed, ``?``
    not searched yet (the dispatch budget ran out first)."""
    lines = []
    for row in range(size):
        cells = []
        for point in points[row * size : (row + 1) * size]:
            if point.error is not None:
                cell = "x"
            elif point.pending:
                cell = "?"
            else:
                cell = "–" if point.rank is None else str(point.rank)
            cells.append(cell.rjust(2))
        lines.append(" ".join(cells))
    return "\n".join(lines)


def null_rank_reading(results_count: int | None, depth: int) -> str | None:
    """How to read a point where the business was not found.

    ``None`` results (the search failed) → no reading. ``0`` → nobody is listed
    there for this search. Fewer than ``depth`` → a sparse SERP: the business is
    not listed there at all, not merely outranked. ``depth`` or more → outranked:
    at least ``depth`` businesses rank above it there."""
    if results_count is None:
        return None
    if results_count == 0:
        return "no_results"
    if results_count < depth:
        return "sparse"
    return "outranked"


NULL_RANK_SENTENCES = {
    "no_results": "no business was listed there for this search",
    "sparse": (
        "the search returned fewer results than the depth checked, and this business was "
        "not among them — it is not listed there, not merely outranked"
    ),
    "outranked": (
        "a full page of results came back without it — at least that many businesses "
        "outrank it there"
    ),
}


__all__ = [
    "ALLOWED_GRID_SIZES",
    "GridAborted",
    "GridAllFailed",
    "GridPoint",
    "NULL_RANK_SENTENCES",
    "PointResult",
    "build_grid",
    "business_data_coordinate",
    "classify_point_failure",
    "distance_km",
    "format_coordinate",
    "grid_zoom",
    "item_rank",
    "listing_search_coordinate",
    "maps_coordinate",
    "match_business",
    "null_rank_reading",
    "point_from_items",
    "render_grid",
    "run_grid",
    "summarize",
]
