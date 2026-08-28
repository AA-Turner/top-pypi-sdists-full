"""Auto-generated stub for module: geometry."""
from typing import Any

# Constants
DEFAULT_INSET_PX: int
GEOMETRY_STATE_KEY: str
NoMatchPolicy: Any
OverlapPolicy: Any
Point: Any
ReferencePoint: Any

# Functions
def assign_detections_to_zones(detections: Any['Any'], zones: Any[Any], resolution: tuple[int, int]) -> Any:
    """
    Partition detections across zones under **declared** policies (**PY-10**).
    
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
    ...
def check_geometry_matches_frame(geometry: Any, ctx: 'Any', stage: str) -> None:
    """
    Assert that geometry built at setup still describes the frames arriving (**PY-7**).
    
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
    ...
def detection_reference_point(detection: 'Any', mode: Any, resolution: tuple[int, int]) -> Any:
    """
    The pixel point that decides which zone ``detection`` is in.
    
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
    ...
def point_in_polygon(point: Any, vertices: Any[Any]) -> bool:
    """
    Is ``point`` inside ``vertices``, edge included?
    
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
    ...
def polygon_offset_inward(vertices: Any[Any], offset: float) -> tuple[Any, ...]:
    """
    Inset a polygon by ``offset`` pixels along each edge's inward normal.
    
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
    ...
def resolve_geometry(state: Any, explicit: Any | None) -> Any:
    """
    The geometry a primitive should use: injected, else published, else built from a frame.
    
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
    ...
def segment_side(point: Any, start: Any, end: Any) -> int:
    """
    Which side of the directed line ``start->end`` does ``point`` lie on?
    
        Ported from ``ABLineCounter._scalar_side``.  Collinear counts as ``+1``, matching the
        legacy ``cross >= 0``: the tie has to break *somewhere* and breaking it differently
        would change every A/B count we have to diff clean against.
    
        Returns:
            ``+1`` or ``-1``.
    """
    ...
def to_pixels(point: Any[float], resolution: tuple[int, int]) -> Any:
    """
    Convert one normalized 0-1 ``(x, y)`` to pixels in ``resolution`` (**PY-7**).
    
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
    ...
def zone_identity(zone_name: str) -> str:
    """
    The identity a zone is keyed by, everywhere.
    
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
    ...

# Classes
class GeometryError:
    # Geometry is unusable, and running anyway would report a wrong number forever.
    #
    #     Raised at **setup** (:class:`SceneGeometry` construction, or a primitive's ``__init__``)
    #     for everything knowable there.  The two exceptions are conditions that only exist once
    #     frames arrive: an ``on_no_match``/``on_overlap`` of ``"error"``
    #     (:func:`assign_detections_to_zones`) and a frame whose resolution contradicts the geometry
    #     (:func:`check_geometry_matches_frame`).  Contract Section 5: *a missing required field is a
    #     startup error, not a silent default*.  The legacy path does the opposite in three
    #     places -- a missing ``resolution`` disables zone processing, a 2-vertex polygon is
    #     skipped with a warning, and ``abline`` with one line counts zero forever -- and all
    #     three reach an operator as "the analytics are wrong".

    ...
class Polygon:
    # One named zone, resolved to pixels.
    #
    #     Immutable and built once at setup: converting normalized to pixels per frame is both
    #     wasted work and a second place for the conversion to be wrong (**PY-7**).

    def contains(self: Any, point: Any) -> bool:
        """
        Is ``point`` (pixels) inside this zone, edge included?
        """
        ...

    def identity(self: Any) -> str:
        """
        This zone's identity -- see :func:`zone_identity` (the **Q1** seam).
        """
        ...

    def inset(self: Any, offset_px: float) -> 'Any':
        """
        A copy inset by ``offset_px`` pixels (see :func:`polygon_offset_inward`).
        """
        ...

class SceneGeometry:
    # A camera's zones and lines, resolved to pixels once, at setup.
    #
    #     **The single normalized-to-pixel boundary in the engine (PY-7).**  Construct it from
    #     normalized geometry plus a resolution; everything downstream reads pixels and never
    #     sees a 0-1 coordinate again.
    #
    #     Zone order is the order the zones were authored in and is preserved through
    #     construction, so ``on_overlap: first_match`` is *deterministic* rather than dependent on
    #     whichever ``dict`` a call site happened to build (**PY-10**,
    #     ``analytics/geometry.py:256``).

    def empty(cls: Any) -> 'Any':
        """
        No geometry configured.
        
                A legitimate state, not an error: an app with no ``zones:`` block runs in the single
                :data:`GLOBAL_ZONE` bucket.  ``zone_occupancy`` against this geometry sends every
                detection to ``unassigned`` and *says so* (the manifest's own
                ``GeometryRequirement`` reason); ``line_crossing`` refuses to start.
        """
        ...

    def from_context(cls: Any, ctx: 'Any') -> 'Any':
        """
        Resolve the geometry a :class:`~.base.FrameContext` carries.
        
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
        ...

    def from_stream_info(cls: Any, stream_info: 'Any') -> 'Any':
        """
        Resolve the geometry carried on ``stream_info`` (contract S4).
        
                The runtime's one call site: geometry resolution belongs in the engine's setup
                phase, once, and not in a daemon thread inside a use-case object polling an
                authenticated API every 30 s (``05`` §5,
                ``usecases/people_counting.py:109-144``).
        """
        ...

    def from_zone_config(cls: Any, zone_config: Any | None, resolution: Any[int] | None) -> 'Any':
        """
        Resolve normalized geometry to pixels, or fail loudly (**PY-7**).
        
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
        ...

    def is_empty(self: Any) -> bool:
        """
        ``True`` when no zone and no line is configured.
        """
        ...

    def line_names(self: Any) -> tuple[str, ...]:
        """
        Line names in drawing order.  ``abline`` takes the first two as A and B.
        """
        ...

    def select_zones(self: Any, wanted: Any['Any'] | Any[str]) -> tuple[Any, ...]:
        """
        The zones a config's ``zones:`` field selects, in drawing order.
        
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
        ...

    def zone_names(self: Any) -> tuple[str, ...]:
        """
        Zone names in drawing order -- the order ``first_match`` resolves in.
        """
        ...

class Segment:
    # One named line, resolved to pixels.
    #
    #     fe-streaming infers "line" purely from a point count of exactly 2 (``05`` §2), so a
    #     segment is always two endpoints -- there is no polyline case to handle.

    def identity(self: Any) -> str:
        """
        See :func:`zone_identity` (the **Q1** seam).
        """
        ...

    def length(self: Any) -> float:
        """
        Segment length in pixels.
        """
        ...

    def projection_param(self: Any, point: Any) -> float:
        """
        Parameter ``t`` of ``point``'s projection onto this segment.
        
                ``0`` at :attr:`start`, ``1`` at :attr:`end`.  ``ABLineCounter`` uses ``0 <= t <= 1``
                on *both* lines to decide whether a point is within the trap zone's longitudinal
                extent, so that a track walking past the end of the lines is not counted.
        """
        ...

    def side_of(self: Any, point: Any) -> int:
        """
        ``+1`` or ``-1`` -- see :func:`segment_side`.
        """
        ...

class ZoneAssignment:
    # The result of partitioning one frame's detections across zones.
    #
    #     Carries the *loss* as data rather than dropping it on the floor (**PY-10**):
    #     :attr:`unassigned` and :attr:`no_match_count` are always populated, including under
    #     ``on_no_match: drop``, so "the geometry is stale" is a number an operator can see.

    def counts(self: Any) -> dict[str, int]:
        """
        Zone identity -> detection count, in drawing order.
        """
        ...

