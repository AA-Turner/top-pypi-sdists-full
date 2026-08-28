"""Shared geometry for the zone primitives: one coordinate convention, declared policies.

Normative sources: ``_contracts/05-asis-zones-and-geometry.md`` (the whole document -- it is
the most trap-laden area in the system) and ``clauding/STAGE_BC_PLAN.md`` §2 (B2).

Ported from ``analytics/geometry.py`` (``point_in_polygon``, ``build_zone_polygons_px``,
``assign_detections_to_zones``) and ``post_processing/utils/counting_utils.py``
(``polygon_offset_inward``), with four behaviours changed on purpose.  Each change has a
defect id:

**PY-7 -- one coordinate convention.**  Two classes called ``ZoneConfig`` exist in this
package with *opposite* units (``analytics/schemas.py:410`` normalized 0-1,
``post_processing/core/config.py:122`` pixels), and the persisted payload is pixels-or-
normalized depending on whether a sibling ``resolution`` key happens to be present
(``05`` §3).  That is the likeliest source of a silent 1920x error during migration.  Here
there is exactly one rule: **everything crossing this module's boundary is normalized 0-1,
and pixels are derived internally** from ``StreamInfo.resolution`` by
:meth:`SceneGeometry.from_zone_config`.  Nothing outside this module handles a pixel.

Pixels are derived rather than avoided because two things are genuinely pixel-defined: the
20 px auto-inset band of ``line_crossing.method: polygon``, and parity with the legacy
counters we must diff clean against.

**Fail loudly, never silently skip.**  ``build_zone_polygons_px`` skips a polygon with
fewer than 3 vertices with a ``logger.warning`` (``geometry.py:281``) and the engine
disables zone processing entirely when ``resolution`` is missing.  Both present to an
operator as "the numbers are wrong" rather than "the config is broken", which is exactly
the failure mode contract Section 5 outlaws.  Every equivalent condition here raises
:class:`GeometryError` at *setup*.

**PY-10 -- declared behaviours, not accidents.**  ``assign_detections_to_zones``
(``geometry.py:225``) silently drops a detection that matches no zone (``:246``) with no
counter anywhere, and resolves an overlap by ``break``-ing on the first match (``:256``) --
i.e. by ``dict`` insertion order, i.e. undefined.  Both are now named policies:
:data:`NoMatchPolicy` and :data:`OverlapPolicy`, defaulting to ``"unassigned"`` and
``"first_match"`` so the *default* is today's shape while the loss becomes countable.

**PY-6 -- the no-zone sentinel is ``"global"``.**  Never ``"__global__"``
(``usecases/people_counting.py:307``).  Migrating an app across the two splits its
ClickHouse history into two unrelated series.  :data:`GLOBAL_ZONE` and
:data:`UNASSIGNED_ZONE` are **owned by** ``contract/schemas.py`` and only re-exported here,
so no zone primitive has to spell either and no module can spell one differently.

No ``numpy``, no ``cv2``.  The legacy path calls ``cv2.pointPolygonTest``; importing
OpenCV to answer "is this point in this polygon" is part of why every runtime import pulls
179 legacy modules plus torch (**PY-20**).  The pure-Python crossing test below is
edge-inclusive, matching ``cv2.pointPolygonTest(...) >= 0``.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import TYPE_CHECKING, Final, Literal

from matrice_analytics.engine.contract.schemas import (
    GLOBAL_ZONE,
    UNASSIGNED_ZONE,
    ZoneConfig,
)
from matrice_analytics.engine.contract.schemas import (
    zone_identity as _contract_zone_identity,
)
from matrice_analytics.engine.state import StateStore

if TYPE_CHECKING:  # pragma: no cover - typing only
    from matrice_analytics.engine.contract.schemas import StreamInfo
    from matrice_analytics.engine.primitives.base import FrameContext, PipelineDetection

__all__ = [
    "DEFAULT_INSET_PX",
    "GEOMETRY_STATE_KEY",
    "GLOBAL_ZONE",
    "IDENTITY_REPLACEMENT",
    "IDENTITY_SEPARATOR",
    "GeometryError",
    "NoMatchPolicy",
    "OverlapPolicy",
    "Point",
    "Polygon",
    "ReferencePoint",
    "SceneGeometry",
    "Segment",
    "UNASSIGNED_ZONE",
    "ZoneAssignment",
    "assign_detections_to_zones",
    "check_geometry_matches_frame",
    "detection_reference_point",
    "point_in_polygon",
    "polygon_offset_inward",
    "resolve_geometry",
    "segment_side",
    "to_pixels",
    "zone_identity",
]


# ---------------------------------------------------------------------------
# Vocabulary
# ---------------------------------------------------------------------------

Point = tuple[float, float]
"""An ``(x, y)`` pair.  **Pixels** everywhere inside this module; the only normalized
coordinates are the ones arriving on a :class:`~matrice_analytics.engine.contract.schemas.ZoneConfig`
or a detection's bounding box, and they are converted on entry (**PY-7**)."""

ReferencePoint = Literal["foot_center", "bbox_center", "foot_75"]
"""Which point of a bounding box decides membership.

``foot_center`` -- bottom-centre -- is the default for both zone primitives because a
person's feet are where they actually stand; ``bbox_center`` puts a tall person in the zone
behind the one they are standing in.  ``analytics/geometry.py:184`` spells this
``use_foot_center: bool`` and defaults it to ``False``, so the new engine's default is a
deliberate change.

``foot_75`` -- 75% of the way down the box (``y = ymin + 0.75 * (ymax - ymin)``) -- exists
for one reason: it is the exact point ``post_processing/utils/counting_utils.py``'s
``VectorABLineCounter.update()`` computes when its own confusingly-named
``use_foot_center=True`` (its default) is set (``counting_utils.py:612``,
``curr_center = [(x1 + x2) / 2.0, y1 + 0.75 * (y2 - y1)]``) -- despite the parameter name, it
is neither the bottom edge nor the centre. Several legacy ground-truth benchmarks (footfall
among them) were validated against crossings measured at exactly this point, not at
``foot_center`` (100% down) or ``bbox_center`` (50% down). Use it only when bit-for-bit
parity with one of those specific benchmarks is required -- for a new app, ``foot_center`` is
still the right default; this is a migration-parity option, not a generally better choice.
"""

NoMatchPolicy = Literal["unassigned", "drop", "error"]
"""What happens to a detection inside no zone (**PY-10**).

``unassigned`` (default)
    Route it to the :data:`UNASSIGNED_ZONE` bucket and **count it**.  Today's behaviour is
    ``drop`` with no counter, so a mis-drawn polygon looks identical to an empty room.
``drop``
    Discard it -- but it is still counted in ``unassigned_count``, so the loss stays
    visible.  Silence is never a policy here.
``error``
    Raise.  For an installation where every detection provably falls in a zone and one
    that does not means the geometry is stale.
"""

OverlapPolicy = Literal["first_match", "all_match", "error"]
"""What happens to a detection inside more than one zone (**PY-10**).

``first_match`` (default)
    The first zone in drawing order wins.  This is today's behaviour, but *deterministic*:
    :class:`SceneGeometry` preserves the order the zones were authored in rather than
    relying on ``dict`` insertion order at an arbitrary call site.
``all_match``
    Count it in every zone that contains it.  ``sum(per_zone counts) >= occupancy``, by
    design -- ``occupancy`` counts distinct detections.
``error``
    Raise.  Overlap is a drawing mistake for this app.
"""

# :data:`UNASSIGNED_ZONE` is re-exported, not defined here.  It lives beside
# :data:`GLOBAL_ZONE` in ``contract/schemas.py`` because it is a *zone id* -- it reaches
# ``raw_analytics.zoneId`` -- and two modules spelling one id independently splits a
# ClickHouse series exactly the way ``"__global__"`` vs ``"global"`` does (**PY-6**).  This
# module used to define it and ``primitives/dwell.py`` used to define it again; both now read
# the one definition.  Re-exported so no zone primitive has to reach past this module for the
# two sentinels it needs.

DEFAULT_INSET_PX = 20
"""The auto-inset of ``line_crossing.method: polygon``'s inner band, in pixels.

``analytics/geometry.py:29`` (``_DEFAULT_INNER_POLYGON_OFFSET``).  Pixel-defined, which is
why :class:`SceneGeometry` derives pixels at all rather than staying normalized.
"""

GEOMETRY_STATE_KEY = "scene_geometry"
"""Where a primitive looks for its :class:`SceneGeometry` when the runtime did not pass one.

The runtime (C2) resolves geometry once per camera at session setup -- from
:meth:`SceneGeometry.from_stream_info` or :meth:`SceneGeometry.from_context` -- and should hand
it to each geometry primitive as the ``geometry=`` keyword.  This state key is the second
source, so a runtime that prefers to publish rather than inject has one agreed name instead of
four; ``resolve_geometry(..., ctx=ctx)`` is the third, for a caller holding only a frame.  See
:func:`resolve_geometry` for why the object is built once per camera and not per frame.
"""


class GeometryError(ValueError):
    """Geometry is unusable, and running anyway would report a wrong number forever.

    Raised at **setup** (:class:`SceneGeometry` construction, or a primitive's ``__init__``)
    for everything knowable there.  The two exceptions are conditions that only exist once
    frames arrive: an ``on_no_match``/``on_overlap`` of ``"error"``
    (:func:`assign_detections_to_zones`) and a frame whose resolution contradicts the geometry
    (:func:`check_geometry_matches_frame`).  Contract Section 5: *a missing required field is a
    startup error, not a silent default*.  The legacy path does the opposite in three
    places -- a missing ``resolution`` disables zone processing, a 2-vertex polygon is
    skipped with a warning, and ``abline`` with one line counts zero forever -- and all
    three reach an operator as "the analytics are wrong".
    """


# ---------------------------------------------------------------------------
# Zone identity -- the Q1 seam
# ---------------------------------------------------------------------------


IDENTITY_SEPARATOR: Final[str] = "."
"""The character that structures an output key, and therefore cannot appear *inside* one.

``per_zone.<zone>.count`` is parsed by splitting on dots -- the manifest validates a
``zones: all`` stage's per-zone sources against ``^per_zone\\.[^.]+\\.count$``
(``manifest/models.py``, ``ZoneOccupancyConfig.output_patterns``) and
:func:`~matrice_analytics.engine.primitives.base.resolve_value` partitions on the first one.
A zone the operator drew as ``"Gate 1.2"`` would produce ``per_zone.Gate 1.2.count``, which
that pattern rejects, so the metric would be an unresolvable source at manifest load -- for a
zone name the streaming UI accepts.  :func:`zone_identity` removes the character; see there.
"""

IDENTITY_REPLACEMENT: Final[str] = "_"
"""What :data:`IDENTITY_SEPARATOR` becomes inside a zone identity."""


def zone_identity(zone_name: str) -> str:
    """The identity a zone is keyed by, everywhere.

    **This function is the Q1 seam.  It is the one edit.**

    Backlog **Q1** (``05`` §8) asks whether the engine keeps name-as-identity for ML zones
    or introduces stable ids.  Today the name *is* the identity: the fe-streaming payload
    keys geometry by the human-drawn name (``05`` §2, ``buildZoneConfig``), so renaming
    ``"Polygon 1"`` in the UI changes ``raw_analytics.zoneId`` and orphans every row that
    came before -- the chart splits into two series with no link between them.

    Q1 does not block the geometry maths, so this builds against names as today.  What it
    must not do is scatter that assumption: every place a zone name becomes an output key,
    a state key or an assignment bucket goes through *this function*.  When Q1 lands, the
    body becomes a lookup of the stable id (and the callers, unchanged, start keying by it).

    Grep for ``zone_identity`` to see the complete blast radius of that decision.

    **The one transformation applied today** is that a dot becomes an underscore.  Zone names
    are operator-drawn in the streaming UI, which accepts ``"Gate 1.2"``, and a dot inside a
    zone identity breaks the ``per_zone.<zone>.count`` key it is spliced into -- see
    :data:`IDENTITY_SEPARATOR`.  Doing it *here* is what makes it safe: the output key, the
    window key, the state accumulator key and the assignment bucket are all this one value, so
    they cannot disagree.  Sanitising at the point a key is built instead -- one ``.replace``
    per call site -- is how the two spellings of a zone id get into ClickHouse (**PY-6**).

    Two names that collide under the substitution (``"Gate 1.2"`` and ``"Gate 1_2"`` on one
    camera) are rejected at setup by :class:`SceneGeometry`, because merging two zones'
    counts into one series silently is worse than refusing to start.

    Args:
        zone_name: The zone name as drawn in the streaming UI, e.g. ``"Polygon 1"``.

    Returns:
        The identity to key by.  The name, with any dot replaced by an underscore.
    """
    # Delegates to the canonical seam in the contract layer. The rule has two callers --
    # the primitives here and ``ZoneOccupancyConfig.output_names()`` in the manifest -- and
    # ``manifest`` may not import ``primitives``, so the function lives at the layer both
    # can reach. Re-exported from this module so that grepping ``zone_identity`` from the
    # primitive side still shows the full blast radius of the Q1 decision.
    return _contract_zone_identity(zone_name)


# ---------------------------------------------------------------------------
# Primitive geometry
# ---------------------------------------------------------------------------


def to_pixels(point: Sequence[float], resolution: tuple[int, int]) -> Point:
    """Convert one normalized 0-1 ``(x, y)`` to pixels in ``resolution`` (**PY-7**).

    The only normalized-to-pixel conversion in the engine.  ``analytics/geometry.py:32``
    (``_to_pixel``) does the same arithmetic in four call sites; concentrating it here is
    what makes a 1920x error a single-function bug rather than a search.

    Args:
        point: ``(x, y)`` with each component in 0-1.
        resolution: ``(width, height)`` in pixels, both > 0.

    Returns:
        ``(x_px, y_px)`` as floats -- *not* rounded.  Polygon vertices are rounded to int
        for parity with ``build_zone_polygons_px``; a reference point is not, because
        rounding it moves a detection up to half a pixel across a boundary for no reason.

    Raises:
        GeometryError: ``resolution`` is not two positive integers.

    Example:
        >>> to_pixels((0.5, 0.5), (1920, 1080))
        (960.0, 540.0)
    """
    width, height = _checked_resolution(resolution)
    return (float(point[0]) * width, float(point[1]) * height)


def _checked_resolution(resolution: tuple[int, int] | Sequence[int]) -> tuple[int, int]:
    """Validate ``(width, height)``, loudly.

    Raises:
        GeometryError: Not a 2-sequence, or either dimension <= 0.  ``StreamInfo`` defaults
            ``resolution`` to ``(0, 0)``; letting that through would scale every zone to a
            single point at the origin and report zero occupancy forever.
    """
    if resolution is None or len(tuple(resolution)) != 2:
        raise GeometryError(
            f"resolution must be (width, height) in pixels, got {resolution!r}. Zone "
            "geometry is normalized 0-1 and pixels are derived from StreamInfo.resolution "
            "(PY-7); without it the conversion is undefined."
        )
    width, height = (int(resolution[0]), int(resolution[1]))
    if width <= 0 or height <= 0:
        raise GeometryError(
            f"resolution {(width, height)} has a non-positive dimension. Zone processing "
            "without a valid resolution must fail loudly here, not silently skip: the "
            "legacy engine skips, and the operator sees 'the numbers are wrong' instead of "
            "'the camera config is missing a resolution' (contract Section 5)."
        )
    return (width, height)


def _on_segment(px: float, py: float, ax: float, ay: float, bx: float, by: float) -> bool:
    """Is ``(px, py)`` on the closed segment ``(ax, ay)-(bx, by)``?"""
    cross = (bx - ax) * (py - ay) - (by - ay) * (px - ax)
    # Scale the collinearity tolerance with the segment length: an absolute epsilon is
    # meaningless once coordinates are in the thousands, which pixels are.
    tolerance = 1e-9 * max(1.0, abs(bx - ax) + abs(by - ay))
    if abs(cross) > tolerance:
        return False
    return min(ax, bx) - 1e-9 <= px <= max(ax, bx) + 1e-9 and min(ay, by) - 1e-9 <= py <= max(ay, by) + 1e-9


def point_in_polygon(point: Point, vertices: Sequence[Point]) -> bool:
    """Is ``point`` inside ``vertices``, edge included?

    Replaces ``cv2.pointPolygonTest(polygon, point, False) >= 0``
    (``analytics/geometry.py:170``) with the equivalent pure-Python crossing-number test
    plus an explicit on-edge check, so the zone primitives do not drag OpenCV into every
    runtime import (**PY-20**).

    The polygon is treated as implicitly closed and may be wound either way -- fe-streaming
    stores vertices in click order with no winding normalisation (``05`` §2).

    Args:
        point: ``(x, y)`` in **pixels**.
        vertices: The polygon's vertices in pixels, at least 3 of them.

    Returns:
        ``True`` when the point is strictly inside or exactly on an edge.

    Example:
        >>> square = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0)]
        >>> point_in_polygon((5.0, 5.0), square), point_in_polygon((15.0, 5.0), square)
        (True, False)
        >>> point_in_polygon((10.0, 5.0), square)  # on the edge
        True
    """
    count = len(vertices)
    if count < 3:
        return False
    x, y = float(point[0]), float(point[1])
    inside = False
    previous = count - 1
    for current in range(count):
        xi, yi = float(vertices[current][0]), float(vertices[current][1])
        xj, yj = float(vertices[previous][0]), float(vertices[previous][1])
        if _on_segment(x, y, xi, yi, xj, yj):
            return True
        if (yi > y) != (yj > y):
            crossing_x = (xj - xi) * (y - yi) / (yj - yi) + xi
            if x < crossing_x:
                inside = not inside
        previous = current
    return inside


def _distance_to_segment(point: Point, start: Point, end: Point) -> float:
    """Shortest distance from ``point`` to the closed segment ``start-end``, in pixels."""
    dx, dy = end[0] - start[0], end[1] - start[1]
    length_squared = dx * dx + dy * dy
    if length_squared < 1e-12:
        return math.hypot(point[0] - start[0], point[1] - start[1])
    t = ((point[0] - start[0]) * dx + (point[1] - start[1]) * dy) / length_squared
    t = min(1.0, max(0.0, t))
    return math.hypot(point[0] - (start[0] + t * dx), point[1] - (start[1] + t * dy))


def _line_intersection(p1: Point, p2: Point, p3: Point, p4: Point) -> Point | None:
    """Intersection of the infinite lines ``p1->p2`` and ``p3->p4``, or ``None`` if parallel.

    Ported verbatim from ``counting_utils.py:_line_intersection``.
    """
    dax, day = p2[0] - p1[0], p2[1] - p1[1]
    dbx, dby = p4[0] - p3[0], p4[1] - p3[1]
    denominator = dax * dby - day * dbx
    if abs(denominator) < 1e-10:
        return None
    t = ((p3[0] - p1[0]) * dby - (p3[1] - p1[1]) * dbx) / denominator
    return (p1[0] + t * dax, p1[1] + t * day)


def polygon_offset_inward(vertices: Sequence[Point], offset: float) -> tuple[Point, ...]:
    """Inset a polygon by ``offset`` pixels along each edge's inward normal.

    Ported from ``counting_utils.polygon_offset_inward`` (reached from
    ``analytics/geometry.py:153``), numpy removed.  Each edge is shifted inward and the new
    vertices are the intersections of consecutive shifted edges, so a corner stays a corner
    rather than becoming a bevel.

    Args:
        vertices: The outer polygon in pixels, at least 3 vertices.
        offset: Inset distance in pixels.  ``<= 0`` returns the polygon unchanged.

    Returns:
        The inset polygon, vertices rounded to int for parity with the legacy counter.

    Raises:
        GeometryError: Fewer than 3 vertices, or the inset collapses/inverts the polygon --
            i.e. ``inset_px`` is too large for this zone.  The legacy version returns the
            self-intersecting result and the counter then counts nothing, forever.
    """
    count = len(vertices)
    if count < 3:
        raise GeometryError(f"cannot inset a polygon with {count} vertices; a polygon needs at least 3")
    if offset <= 0:
        return tuple((float(v[0]), float(v[1])) for v in vertices)

    outer = [(float(v[0]), float(v[1])) for v in vertices]
    centroid_x = sum(v[0] for v in outer) / count
    centroid_y = sum(v[1] for v in outer) / count

    def inward_normal(start: Point, end: Point) -> Point:
        """Unit normal of ``start->end`` pointing toward the centroid."""
        ex, ey = end[0] - start[0], end[1] - start[1]
        length = math.hypot(ex, ey) + 1e-10
        candidate = (-ey / length, ex / length)
        mid_x, mid_y = (start[0] + end[0]) / 2.0, (start[1] + end[1]) / 2.0
        if candidate[0] * (centroid_x - mid_x) + candidate[1] * (centroid_y - mid_y) > 0:
            return candidate
        return (ey / length, -ex / length)

    inset: list[Point] = []
    for index in range(count):
        a = outer[index]
        b = outer[(index + 1) % count]
        previous = outer[(index - 1) % count]

        normal = inward_normal(a, b)
        a_off = (a[0] + normal[0] * offset, a[1] + normal[1] * offset)
        b_off = (b[0] + normal[0] * offset, b[1] + normal[1] * offset)

        previous_normal = inward_normal(previous, a)
        prev_off = (
            previous[0] + previous_normal[0] * offset,
            previous[1] + previous_normal[1] * offset,
        )
        a_off_prev = (a[0] + previous_normal[0] * offset, a[1] + previous_normal[1] * offset)

        corner = _line_intersection(prev_off, a_off_prev, a_off, b_off)
        inset.append(corner if corner is not None else a_off)

    # A correct inset satisfies two properties: every new vertex is inside the outer
    # polygon, and every new vertex is at least `offset` from its boundary.  When the offset
    # exceeds the polygon's own half-width the shifted edges cross over and the result
    # violates one or both -- it is the *negative* offset region, a plausible-looking
    # polygon in the wrong place.  The legacy version returns it and the counter then counts
    # nothing, forever, which is why this is checked rather than assumed.
    tolerance = max(1e-6 * offset, 1e-9)
    for vertex in inset:
        clearance = min(_distance_to_segment(vertex, outer[i], outer[(i + 1) % count]) for i in range(count))
        if not point_in_polygon(vertex, outer) or clearance < offset - tolerance:
            raise GeometryError(
                f"insetting this zone by {offset:g} px collapses or inverts it: the inset "
                f"corner {(round(vertex[0], 1), round(vertex[1], 1))} sits {clearance:.1f} px "
                f"from the boundary, not {offset:g}. The offset is wider than the zone. "
                "Lower line_crossing.inset_px, or draw a larger zone."
            )
    return tuple((float(round(p[0])), float(round(p[1]))) for p in inset)


def segment_side(point: Point, start: Point, end: Point) -> int:
    """Which side of the directed line ``start->end`` does ``point`` lie on?

    Ported from ``ABLineCounter._scalar_side``.  Collinear counts as ``+1``, matching the
    legacy ``cross >= 0``: the tie has to break *somewhere* and breaking it differently
    would change every A/B count we have to diff clean against.

    Returns:
        ``+1`` or ``-1``.
    """
    cross = (end[0] - start[0]) * (point[1] - start[1]) - (end[1] - start[1]) * (point[0] - start[0])
    return 1 if cross >= 0 else -1


# ---------------------------------------------------------------------------
# Resolved geometry
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Polygon:
    """One named zone, resolved to pixels.

    Immutable and built once at setup: converting normalized to pixels per frame is both
    wasted work and a second place for the conversion to be wrong (**PY-7**).
    """

    name: str
    vertices: tuple[Point, ...]
    """At least 3 vertices, in pixels, in the order they were drawn."""

    def __post_init__(self) -> None:
        if len(self.vertices) < 3:
            raise GeometryError(
                f"zone {self.name!r} has {len(self.vertices)} vertices; a polygon needs at "
                "least 3. build_zone_polygons_px (analytics/geometry.py:281) skips this "
                "case with a warning, so the zone silently reports zero forever -- it is an "
                "error here instead."
            )

    @property
    def identity(self) -> str:
        """This zone's identity -- see :func:`zone_identity` (the **Q1** seam)."""
        return zone_identity(self.name)

    def contains(self, point: Point) -> bool:
        """Is ``point`` (pixels) inside this zone, edge included?"""
        return point_in_polygon(point, self.vertices)

    def inset(self, offset_px: float) -> "Polygon":
        """A copy inset by ``offset_px`` pixels (see :func:`polygon_offset_inward`)."""
        return Polygon(name=f"{self.name}::inner", vertices=polygon_offset_inward(self.vertices, offset_px))


@dataclass(frozen=True, slots=True)
class Segment:
    """One named line, resolved to pixels.

    fe-streaming infers "line" purely from a point count of exactly 2 (``05`` §2), so a
    segment is always two endpoints -- there is no polyline case to handle.
    """

    name: str
    start: Point
    end: Point

    @property
    def identity(self) -> str:
        """See :func:`zone_identity` (the **Q1** seam)."""
        return zone_identity(self.name)

    @property
    def length(self) -> float:
        """Segment length in pixels."""
        return math.hypot(self.end[0] - self.start[0], self.end[1] - self.start[1])

    def side_of(self, point: Point) -> int:
        """``+1`` or ``-1`` -- see :func:`segment_side`."""
        return segment_side(point, self.start, self.end)

    def projection_param(self, point: Point) -> float:
        """Parameter ``t`` of ``point``'s projection onto this segment.

        ``0`` at :attr:`start`, ``1`` at :attr:`end`.  ``ABLineCounter`` uses ``0 <= t <= 1``
        on *both* lines to decide whether a point is within the trap zone's longitudinal
        extent, so that a track walking past the end of the lines is not counted.
        """
        dx, dy = self.end[0] - self.start[0], self.end[1] - self.start[1]
        length_squared = dx * dx + dy * dy
        if length_squared < 1e-12:
            return 0.0
        return ((point[0] - self.start[0]) * dx + (point[1] - self.start[1]) * dy) / length_squared


@dataclass(frozen=True, slots=True)
class SceneGeometry:
    """A camera's zones and lines, resolved to pixels once, at setup.

    **The single normalized-to-pixel boundary in the engine (PY-7).**  Construct it from
    normalized geometry plus a resolution; everything downstream reads pixels and never
    sees a 0-1 coordinate again.

    Zone order is the order the zones were authored in and is preserved through
    construction, so ``on_overlap: first_match`` is *deterministic* rather than dependent on
    whichever ``dict`` a call site happened to build (**PY-10**,
    ``analytics/geometry.py:256``).
    """

    resolution: tuple[int, int]
    zones: Mapping[str, Polygon] = field(default_factory=lambda: MappingProxyType({}))
    lines: Mapping[str, Segment] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        if self.zones or self.lines:
            object.__setattr__(self, "resolution", _checked_resolution(self.resolution))
        object.__setattr__(self, "zones", MappingProxyType(dict(self.zones)))
        object.__setattr__(self, "lines", MappingProxyType(dict(self.lines)))
        _check_identities_distinct("zone", self.zones)
        _check_identities_distinct("line", self.lines)

    # -- construction -------------------------------------------------------

    @classmethod
    def empty(cls) -> "SceneGeometry":
        """No geometry configured.

        A legitimate state, not an error: an app with no ``zones:`` block runs in the single
        :data:`GLOBAL_ZONE` bucket.  ``zone_occupancy`` against this geometry sends every
        detection to ``unassigned`` and *says so* (the manifest's own
        ``GeometryRequirement`` reason); ``line_crossing`` refuses to start.
        """
        return cls(resolution=(0, 0))

    @classmethod
    def from_zone_config(cls, zone_config: ZoneConfig | None, resolution: Sequence[int] | None) -> "SceneGeometry":
        """Resolve normalized geometry to pixels, or fail loudly (**PY-7**).

        Args:
            zone_config: The **normalized 0-1**
                :class:`~matrice_analytics.engine.contract.schemas.ZoneConfig` from
                ``StreamInfo``.  ``None`` or empty yields :meth:`empty`.
            resolution: ``(width, height)`` in pixels.  Required whenever ``zone_config``
                declares anything.

        Returns:
            The resolved geometry.

        Raises:
            GeometryError: There is geometry but no usable ``resolution``, or a polygon has
                fewer than 3 vertices, or a line does not have exactly 2 endpoints.  All
                three are silent skips in the legacy path.
        """
        if zone_config is None or (not zone_config.zones and not zone_config.lines):
            return cls.empty()

        checked = _checked_resolution(tuple(resolution) if resolution is not None else None)  # type: ignore[arg-type]

        zones: dict[str, Polygon] = {}
        for name, polygon in zone_config.zones.items():
            vertices = tuple(
                (float(round(px)), float(round(py))) for px, py in (to_pixels(vertex, checked) for vertex in polygon)
            )
            zones[name] = Polygon(name=name, vertices=vertices)

        lines: dict[str, Segment] = {}
        for name, raw in zone_config.lines.items():
            endpoints = _line_endpoints(name, raw)
            lines[name] = Segment(
                name=name,
                start=to_pixels(endpoints[0], checked),
                end=to_pixels(endpoints[1], checked),
            )

        return cls(resolution=checked, zones=zones, lines=lines)

    @classmethod
    def from_stream_info(cls, stream_info: "StreamInfo") -> "SceneGeometry":
        """Resolve the geometry carried on ``stream_info`` (contract S4).

        The runtime's one call site: geometry resolution belongs in the engine's setup
        phase, once, and not in a daemon thread inside a use-case object polling an
        authenticated API every 30 s (``05`` §5,
        ``usecases/people_counting.py:109-144``).
        """
        return cls.from_zone_config(stream_info.zone_config, stream_info.resolution)

    @classmethod
    def from_context(cls, ctx: "FrameContext") -> "SceneGeometry":
        """Resolve the geometry a :class:`~.base.FrameContext` carries.

        The **standard channel**: ``ctx.zone_config`` and ``ctx.resolution`` are the two
        accessors over ``ctx.stream``, so this needs no argument beyond the frame and there is
        nothing for a caller to pass inconsistently.

        Provided because "buildable from ``ctx``" is what stops the next primitive that needs
        pixels from inventing a fourth channel; it is **not** what the two zone primitives call
        per frame.  They take a :class:`SceneGeometry` built once per camera -- see
        :func:`resolve_geometry` for why.

        Args:
            ctx: Any frame from the camera whose geometry is wanted.

        Returns:
            The resolved geometry, or :meth:`empty` when the stream declares none.

        Raises:
            GeometryError: The stream declares geometry but carries no usable resolution.
        """
        if ctx.stream is None:
            return cls.empty()
        return cls.from_zone_config(ctx.zone_config, ctx.resolution)

    # -- queries ------------------------------------------------------------

    @property
    def is_empty(self) -> bool:
        """``True`` when no zone and no line is configured."""
        return not self.zones and not self.lines

    def zone_names(self) -> tuple[str, ...]:
        """Zone names in drawing order -- the order ``first_match`` resolves in."""
        return tuple(self.zones)

    def line_names(self) -> tuple[str, ...]:
        """Line names in drawing order.  ``abline`` takes the first two as A and B."""
        return tuple(self.lines)

    def select_zones(self, wanted: Literal["all"] | Sequence[str]) -> tuple[Polygon, ...]:
        """The zones a config's ``zones:`` field selects, in drawing order.

        Args:
            wanted: ``"all"``, or the zone names the manifest listed.

        Returns:
            The selected polygons.  Empty when no geometry is configured at all.

        A name is matched against the drawn name *or* against its :func:`zone_identity`, so a
        manifest that spells a dotted zone either way selects the same polygon.  Both spellings
        are legal input; the *output* key is always the identity.

        Raises:
            GeometryError: A named zone is not in this camera's geometry *and* the camera
                does have geometry.  That is a manifest/installation mismatch which would
                otherwise publish ``per_zone.<name>.count = 0`` forever, and a zero is
                indistinguishable from a quiet zone.
        """
        if wanted == "all":
            return tuple(self.zones.values())
        names = list(wanted)
        if not self.zones:
            # No geometry at all is the manifest's own documented case ("with no zone
            # geometry every detection lands in the 'unassigned' bucket") -- countable, not
            # silent, so it is not an error.
            return ()
        by_identity = {zone.identity: zone for zone in self.zones.values()}
        missing = [name for name in names if name not in self.zones and name not in by_identity]
        if missing:
            raise GeometryError(
                f"zone(s) {', '.join(repr(m) for m in missing)} are named in the manifest "
                f"but this camera's geometry has {', '.join(repr(z) for z in self.zones) or '(none)'}. "
                "Zone identity is the drawn name today (Q1), so a rename in the streaming "
                "UI breaks this join -- fix the name in one place or the other. Running on "
                "would publish a count of 0 for a zone that does not exist, which reads "
                "exactly like a quiet zone."
            )
        return tuple(self.zones[name] if name in self.zones else by_identity[name] for name in names)


def _check_identities_distinct(kind: str, shapes: Mapping[str, "Polygon | Segment"]) -> None:
    """Reject two shapes on one camera that share a :func:`zone_identity`.

    :func:`zone_identity` maps a dot to an underscore, so ``"Gate 1.2"`` and ``"Gate 1_2"``
    drawn on the same camera would key the same ``per_zone.Gate 1_2.count`` series and their
    counts would be added together with nothing to show it happened.  A merged series is
    unrecoverable after the fact -- the rows are already written -- so this is a setup error,
    which the operator fixes by renaming one zone in the streaming UI.
    """
    seen: dict[str, str] = {}
    for name in shapes:
        identity = zone_identity(name)
        if identity in seen:
            raise GeometryError(
                f"{kind}s {seen[identity]!r} and {name!r} both have the identity "
                f"{identity!r}, so they would publish into one series and their counts would "
                f"be silently added together. A {IDENTITY_SEPARATOR!r} in a drawn name becomes "
                f"{IDENTITY_REPLACEMENT!r} in the identity, because a dot is what structures "
                f"the 'per_zone.<zone>.count' key it is spliced into. Rename one of the two in "
                "the streaming UI."
            )
        seen[identity] = name


def _line_endpoints(name: str, raw: Sequence[float] | Sequence[Sequence[float]]) -> tuple[Point, Point]:
    """Normalize the two shapes ``ZoneConfig.lines`` accepts into two endpoints.

    ``[[x1, y1], [x2, y2]]`` (what fe-streaming persists) or the flat ``[x1, y1, x2, y2]``
    that ``counting_utils.parse_line_config`` also accepts.

    Raises:
        GeometryError: Neither shape, or the wrong number of coordinates.  A one-point
            "line" defines no direction, and the counter would count zero forever.
    """
    values = list(raw)
    if values and isinstance(values[0], (list, tuple)):
        if len(values) != 2:
            raise GeometryError(
                f"line {name!r} has {len(values)} points; a line is exactly 2 endpoints. "
                "fe-streaming infers 'line' from a point count of exactly 2 (05 section 2), "
                "so anything else means the payload was hand-edited."
            )
        return (
            (float(values[0][0]), float(values[0][1])),  # type: ignore[index]
            (float(values[1][0]), float(values[1][1])),  # type: ignore[index]
        )
    if len(values) == 4:
        return ((float(values[0]), float(values[1])), (float(values[2]), float(values[3])))  # type: ignore[arg-type]
    raise GeometryError(
        f"line {name!r} is {raw!r}; expected [[x1,y1],[x2,y2]] or [x1,y1,x2,y2] in normalized 0-1 coordinates."
    )


def resolve_geometry(
    state: StateStore,
    explicit: SceneGeometry | None,
    *,
    ctx: "FrameContext | None" = None,
) -> SceneGeometry:
    """The geometry a primitive should use: injected, else published, else built from a frame.

    **Injection is deliberately still the primary path, and it is a construction-time
    argument rather than a per-frame one.**  Two reasons, and both are about this specific
    object:

    *Cost.*  Resolving geometry is O(zones x vertices) of multiplication plus, for
    ``line_crossing.method: polygon``, a :func:`polygon_offset_inward` that runs an O(n^2)
    clearance sweep over the inset corners.  A pipeline runs once **per zone per frame** -- 25
    fps x 4 zones is 100 constructions a second per camera -- for a value that changes only
    when an operator redraws a polygon.

    *Where the errors land.*  Every failure this module exists to surface is a **setup**
    failure by design: a polygon with two vertices, an ``inset_px`` wider than its zone, a
    manifest naming a zone the camera has not got, a missing resolution.  Building per frame
    moves all four into the hot path, where the only choices are to crash mid-stream or to
    swallow -- and swallowing is precisely the legacy behaviour (``geometry.py:281``,
    ``engine.py``'s resolution check) that reaches an operator as "the numbers are wrong".

    So the runtime (C2) builds one :class:`SceneGeometry` per camera at session setup --
    :meth:`SceneGeometry.from_stream_info` or :meth:`SceneGeometry.from_context` -- and passes
    it to every geometry stage as ``geometry=``.  The other two sources exist so that path is
    not the *only* one: :data:`GEOMETRY_STATE_KEY` is the agreed name for a runtime that
    prefers to publish rather than inject, and ``ctx=`` lets a caller that has only a frame
    (a test, a custom primitive) reach the same object through the standard channel instead of
    inventing a private one.

    Args:
        state: The primitive's already-scoped store.
        explicit: What the runtime injected, if anything.
        ctx: A frame from this camera, used only when neither of the above is available.  Its
            ``stream`` is the standard camera/frame channel.

    Returns:
        The resolved geometry, or :meth:`SceneGeometry.empty` when none is available.

    Raises:
        GeometryError: The state key holds something that is not a :class:`SceneGeometry`, or
            ``ctx``'s stream declares geometry without a resolution.
    """
    if explicit is not None:
        if not isinstance(explicit, SceneGeometry):
            raise GeometryError(
                f"geometry= must be a SceneGeometry, got {type(explicit).__name__}. Build "
                "one with SceneGeometry.from_stream_info(stream_info) -- that is the single "
                "place normalized 0-1 becomes pixels (PY-7)."
            )
        return explicit
    stored = state.get(GEOMETRY_STATE_KEY)
    if stored is None:
        return SceneGeometry.empty() if ctx is None else SceneGeometry.from_context(ctx)
    if not isinstance(stored, SceneGeometry):
        raise GeometryError(
            f"state[{GEOMETRY_STATE_KEY!r}] holds a {type(stored).__name__}, not a "
            "SceneGeometry. Whatever writes it must write the resolved object, not the raw "
            "normalized dict -- a dict here would put the pixel conversion back in the hot "
            "path and back in two places (PY-7)."
        )
    return stored


def check_geometry_matches_frame(geometry: SceneGeometry, ctx: "FrameContext", stage: str) -> None:
    """Assert that geometry built at setup still describes the frames arriving (**PY-7**).

    Building once per camera is the right trade (see :func:`resolve_geometry`) but it opens one
    hole that building per frame does not have: nothing joins the object to the stream it was
    built for.  Inject geometry resolved at 1920x1080 into a stage whose camera actually sends
    640x640 and every polygon is 3x too big -- the counts stay plausible and are wrong by the
    ratio of the two frame sizes, which is the entire **PY-7** failure mode and the one that
    survives review because no number looks obviously broken.

    ``ctx.stream`` is what makes the check possible: it is the standard channel, so the frame
    can be asked what resolution it really is.  Two cheap comparisons per frame, against a
    class of bug whose only other symptom is a wrong dashboard.

    Args:
        geometry: What the stage resolved at construction.
        ctx: The frame being processed.
        stage: The stage name, for the message.

    Raises:
        GeometryError: The frame's resolution disagrees with the one the geometry was resolved
            against, or the camera declares geometry this stage was not given.  A frame with no
            ``stream`` attached is not checked -- a test may legitimately omit it.
    """
    zone_config = ctx.zone_config
    declared = zone_config is not None and bool(zone_config.zones or zone_config.lines)

    if geometry.is_empty:
        if declared:
            raise GeometryError(
                f"stage {stage!r} was built with no geometry, but camera "
                f"{ctx.camera_id!r} declares "
                f"{len(zone_config.zones) if zone_config else 0} zone(s) and "
                f"{len(zone_config.lines) if zone_config else 0} line(s) on its stream_info. "
                "Every detection is therefore being counted as unassigned while the operator "
                "can see drawn polygons -- the numbers would read like an empty room (PY-10). "
                "The runtime must resolve geometry once per camera and pass it in: "
                "SceneGeometry.from_stream_info(stream_info), or from_context(ctx)."
            )
        return

    frame_resolution = ctx.resolution
    if frame_resolution is not None and frame_resolution != geometry.resolution:
        raise GeometryError(
            f"stage {stage!r} holds geometry resolved against "
            f"{geometry.resolution[0]}x{geometry.resolution[1]}, but camera "
            f"{ctx.camera_id!r} is sending {frame_resolution[0]}x{frame_resolution[1]} frames. "
            "Zone polygons are derived from the resolution (PY-7), so every boundary is off by "
            f"{frame_resolution[0] / geometry.resolution[0]:.3g}x horizontally and the counts "
            "would be plausible and wrong. Rebuild the geometry from this camera's "
            "StreamInfo -- one SceneGeometry per camera, not one per session."
        )


# ---------------------------------------------------------------------------
# Assignment
# ---------------------------------------------------------------------------


def detection_reference_point(
    detection: "PipelineDetection", mode: ReferencePoint, resolution: tuple[int, int]
) -> Point:
    """The pixel point that decides which zone ``detection`` is in.

    Bounding boxes are normalized 0-1 and validated as such by
    :class:`~matrice_analytics.engine.contract.schemas.BoundingBox`, so the reference point
    is computed normalized and converted once (**PY-7**).

    Args:
        detection: The pipeline detection.
        mode: ``"foot_center"`` (bottom-centre, the default), ``"bbox_center"``, or
            ``"foot_75"`` (75% down -- migration parity with specific legacy benchmarks;
            see :data:`ReferencePoint`).
        resolution: ``(width, height)`` in pixels.

    Returns:
        ``(x, y)`` in pixels.

    Example:
        A box spanning x 0.4-0.6 and y 0.2-0.8 on a 1920x1080 stream has a foot centre at
        ``(960.0, 864.0)`` and a bbox centre at ``(960.0, 540.0)``.  The two differ by 324
        pixels -- which is why the mode is a declared config field and not a bool defaulting
        to ``False`` as at ``analytics/geometry.py:184``.
    """
    box = detection.bounding_box
    x = (box.xmin + box.xmax) / 2.0
    if mode == "foot_center":
        y = box.ymax
    elif mode == "foot_75":
        y = box.ymin + 0.75 * (box.ymax - box.ymin)
    else:
        y = (box.ymin + box.ymax) / 2.0
    return to_pixels((x, y), resolution)


@dataclass(frozen=True, slots=True)
class ZoneAssignment:
    """The result of partitioning one frame's detections across zones.

    Carries the *loss* as data rather than dropping it on the floor (**PY-10**):
    :attr:`unassigned` and :attr:`no_match_count` are always populated, including under
    ``on_no_match: drop``, so "the geometry is stale" is a number an operator can see.
    """

    by_zone: Mapping[str, tuple["PipelineDetection", ...]]
    """Zone identity -> the detections inside it, zones in drawing order.

    Keys are :func:`zone_identity` values (the **Q1** seam), not raw names.
    """

    unassigned: tuple["PipelineDetection", ...] = ()
    """Detections in no zone, retained under ``on_no_match: unassigned``, empty under
    ``drop``.  :attr:`no_match_count` is populated either way."""

    no_match_count: int = 0
    """How many detections matched no zone, **whatever the policy**.

    Under ``drop`` this is the only trace they existed; today there is no trace at all.
    """

    assigned_count: int = 0
    """Distinct detections inside at least one zone.

    Under ``on_overlap: all_match`` this is *less than* the sum of the per-zone counts, on
    purpose -- ``occupancy`` counts people, not memberships.
    """

    def __post_init__(self) -> None:
        object.__setattr__(self, "by_zone", MappingProxyType(dict(self.by_zone)))
        object.__setattr__(self, "unassigned", tuple(self.unassigned))

    def counts(self) -> dict[str, int]:
        """Zone identity -> detection count, in drawing order."""
        return {name: len(dets) for name, dets in self.by_zone.items()}


def assign_detections_to_zones(
    detections: Iterable["PipelineDetection"],
    zones: Sequence[Polygon],
    resolution: tuple[int, int],
    *,
    reference_point: ReferencePoint = "foot_center",
    on_no_match: NoMatchPolicy = "unassigned",
    on_overlap: OverlapPolicy = "first_match",
    stamp_zone: bool = True,
) -> ZoneAssignment:
    """Partition detections across zones under **declared** policies (**PY-10**).

    Replaces ``analytics/geometry.py:225``, which silently drops a no-match (``:246``) and
    resolves an overlap by ``break``-ing on the first ``dict`` entry (``:256``).  Same
    default outcome, three differences: the loss is counted, the order is the drawing order
    rather than whatever the caller's dict was, and both behaviours are arguments.

    Args:
        detections: This frame's detections, bounding boxes normalized 0-1.
        zones: The zones to test, in drawing order.  Empty means every detection is a
            no-match, which the caller then reports rather than hides.
        resolution: ``(width, height)`` in pixels.
        reference_point: Which point of the box decides membership.
        on_no_match: See :data:`NoMatchPolicy`.
        on_overlap: See :data:`OverlapPolicy`.
        stamp_zone: Copy each detection with ``zone`` set to the bucket it landed in.
            The runtime wants this (its pipeline runs per zone); a primitive counting in
            place does not, and copying is not free.

    Returns:
        The partition, including what did not match.

    Raises:
        GeometryError: ``on_no_match="error"`` and something matched nothing, or
            ``on_overlap="error"`` and something matched more than one zone.  Per frame,
            because that is when the condition happens -- unlike the setup errors, this one
            cannot be known earlier.
    """
    buckets: dict[str, list["PipelineDetection"]] = {zone.identity: [] for zone in zones}
    unassigned: list["PipelineDetection"] = []
    no_match_count = 0
    assigned_count = 0

    for detection in detections:
        # With no zones there is nothing to test against, and no resolution to test with:
        # SceneGeometry.empty() carries (0, 0) and to_pixels would (correctly) reject it.
        # Everything is a no-match, which the policy below then makes countable.
        point = detection_reference_point(detection, reference_point, resolution) if zones else (0.0, 0.0)
        matched = [zone for zone in zones if zone.contains(point)]

        if not matched:
            no_match_count += 1
            if on_no_match == "error":
                raise GeometryError(
                    f"detection {detection.entity!r} at pixel {point} matches none of the "
                    f"{len(zones)} configured zone(s) and zones.on_no_match is 'error'. "
                    "Either the drawn geometry no longer covers the scene, or the policy "
                    "should be 'unassigned' (the default), which counts the loss instead of "
                    "raising."
                )
            if on_no_match == "unassigned":
                unassigned.append(detection.model_copy(update={"zone": UNASSIGNED_ZONE}) if stamp_zone else detection)
            # on_no_match == "drop": deliberately not retained -- but no_match_count above
            # means the drop is still visible downstream (PY-10).
            continue

        if len(matched) > 1 and on_overlap == "error":
            raise GeometryError(
                f"detection {detection.entity!r} at pixel {point} is inside "
                f"{len(matched)} zones ({', '.join(z.name for z in matched)}) and "
                "zones.on_overlap is 'error'. Overlapping polygons resolve by drawing "
                "order under 'first_match' and are counted twice under 'all_match'; pick "
                "one, or redraw the zones so they do not overlap."
            )

        chosen = matched if on_overlap == "all_match" else matched[:1]
        assigned_count += 1
        for zone in chosen:
            buckets[zone.identity].append(
                detection.model_copy(update={"zone": zone.identity}) if stamp_zone else detection
            )

    return ZoneAssignment(
        by_zone={name: tuple(dets) for name, dets in buckets.items()},
        unassigned=tuple(unassigned),
        no_match_count=no_match_count,
        assigned_count=assigned_count,
    )
