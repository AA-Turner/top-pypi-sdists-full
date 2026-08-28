"""Stub file for engine.primitives directory."""
from typing import Any, Optional

# Constants
REGISTRY: Any = ...  # From base
Scalar: Any = ...  # From base
logger: Any = ...  # From dwell
DEFAULT_INSET_PX: int = ...  # From geometry
GEOMETRY_STATE_KEY: str = ...  # From geometry
NoMatchPolicy: Any = ...  # From geometry
OverlapPolicy: Any = ...  # From geometry
Point: Any = ...  # From geometry
ReferencePoint: Any = ...  # From geometry
logger: Any = ...  # From keypoint_pose
OUTSIDE_EXTENT: Any = ...  # From line_crossing
WARMUP_FRAMES: int = ...  # From line_crossing
logger: Any = ...  # From segmentation_area
Box: Any = ...  # From track
logger: Any = ...  # From velocity_state
logger: Any = ...  # From zone_occupancy

# Functions
# From base
def conformance_problems(impl: Any[Any]) -> list[str]:
    """
    Explain why ``impl`` is not a conforming primitive, or return ``[]``.
    
        ``isinstance(x, Primitive)`` answers yes/no; this answers "which member is missing and
        what should its signature be", which is what an app author or a reviewer actually
        needs.  Used by :meth:`PrimitiveRegistry.register` so a bad implementation fails at
        import time rather than on the first frame.
    
        Args:
            impl: The candidate class.
            custom: Check against :class:`CustomPrimitive` (``Config`` + ``process``) rather
                than the full :class:`Primitive`.
    
        Returns:
            A list of human-readable problems, empty when ``impl`` conforms.
    """
    ...

# From base
def register(impl: Any[Any] | None = None) -> Any:
    """
    Register on the default :data:`REGISTRY` (see :meth:`PrimitiveRegistry.register`).
    
        Example:
            >>> @register
            ... class ZoneOccupancy:
            ...     name = "zone_occupancy"
            ...     Config = ZoneOccupancyConfig
            ...     ...
    """
    ...

# From base
def resolve_value(outputs: Any[str, Any], source: str) -> Any:
    """
    Resolve a ``metrics[].source`` against a frame's stage outputs.
    
        ``<stage>.<value>``, where ``<value>`` may itself contain dots
        (``detect.person.count`` is stage ``detect``, value ``person.count``).
    
        Args:
            outputs: Stage name -> that stage's output, i.e. what
                :attr:`FrameContext.previous` holds.
            source: The manifest source string.
    
        Returns:
            The scalar the manifest asked for.
    
        Raises:
            SourceResolutionError: The stage or the value is missing.  ``09`` §3: *an
                unresolvable source is a manifest load error -- not a metric that reads zero
                forever*.  The message names what *is* available, because the usual cause is a
                one-character typo in ``app.yaml``.
    """
    ...

# From geometry
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

# From geometry
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

# From geometry
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

# From geometry
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

# From geometry
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

# From geometry
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

# From geometry
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

# From geometry
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

# From geometry
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

# From incident_quantise
def level_rank(level: str) -> int:
    """
    Severity as a comparable integer: ``none`` 0, ``info`` 1 ... ``critical`` 5.
    
        Ranked against the **wire vocabulary**
        (:data:`~matrice_analytics.engine.manifest.models.SEVERITY_LEVELS`), never against the
        position of a rung in ``levels:``.  A config may declare any subset of the ladder in
        either ``order``, so a list-position rank would make ``critical`` outrank ``high`` in
        one app and not in another -- the rank has to mean "how bad", not "how far down the
        YAML".
    
        Args:
            level: A severity name, or :data:`NO_LEVEL`.
    
        Returns:
            ``0`` for :data:`NO_LEVEL` or an unknown name, otherwise ``1``-based position in
            ``info, low, medium, high, critical``.
    """
    ...

# From keypoint_pose
def joint_midpoint(keypoints: Any[Any], first: int, second: int, min_confidence: float) -> tuple[float, float] | None:
    """
    Midpoint of two joints, or ``None`` when either is not confidently visible.
    
        ``fall_detection.py:1652-1655``: **both** joints must clear the threshold or the result is
        ``None``.  That is the right rule and it is kept -- averaging a confident shoulder with a
        hallucinated one produces a torso vector that is neither.
    
        Args:
            keypoints: This detection's joints, normalized 0-1.
            first: Index of the first joint, e.g. ``COCO17_JOINTS["left_shoulder"]``.
            second: Index of the second.
            min_confidence: Per-joint visibility floor.
    
        Returns:
            ``(x, y)`` normalized 0-1, or ``None``.
    """
    ...

# From keypoint_pose
def torso_angle_degrees(keypoints: Any[Any], min_confidence: float) -> float | None:
    """
    Angle of the torso away from upright, in degrees, or ``None`` when unmeasurable.
    
        ``0`` is upright, ``90`` is horizontal, ``180`` is inverted.  The torso vector is
        shoulder-centre minus hip-centre, both confidence-gated pair midpoints, and the angle is
        scale-invariant -- which is the reason to prefer this rule over a pixel one, and the reason
        this primitive needs no frame resolution for it.
    
        **One deliberate divergence from ``fall_detection.py:1663-1665``.**  Legacy computes
        ``degrees(atan2(abs(dx), abs(dy)))``, which confines the result to ``[0, 90]`` and makes an
        **inverted person indistinguishable from an upright one** -- both read ``0``.  This
        function keeps the sign of the vertical component, so the range is ``[0, 180]``.  For every
        pose where the shoulders are above the hips the two agree *exactly* (with ``dy < 0``,
        ``atan2(|dx|, -dy) == atan2(|dx|, |dy|)``), so a legacy ``pose_angle_thresh_deg: 45``
        carries over unchanged; they differ only where legacy was blind, and there the difference is
        that a person on their head now reads ``~180`` and matches ``torso_angle_gt: 45`` instead of
        reading ``0`` and matching nothing.
    
        Args:
            keypoints: This detection's joints, normalized 0-1.
            min_confidence: Per-joint visibility floor; all four of shoulders and hips must clear it.
    
        Returns:
            Degrees in ``[0, 180]``, or ``None`` when either midpoint is unavailable.  ``None`` is
            **not** ``0.0``: an unmeasured torso is not an upright one, and conflating them is how
            ``fall_detection`` confirms a fall from a bounding box alone (``:1719-1721``).
    """
    ...

# From ratio_compliance
def association_score(subject: Any, attribute: Any) -> float:
    """
    How strongly ``attribute`` belongs to ``subject``, in ``0..1``.
    
        **Intersection over the smaller box**, not intersection over union -- and the config
        field is nevertheless called ``iou_threshold``
        (:class:`~matrice_analytics.engine.manifest.models.RatioComplianceConfig`), which is a
        misnomer inherited from the manifest schema.  The reason for the divergence is
        arithmetic, not taste:
    
        A person box is roughly ``0.10 x 0.60`` of a normalized frame (area ``0.060``); the
        hardhat on their head is roughly ``0.05 x 0.04`` (area ``0.002``).  Even when the
        hardhat is *entirely inside* the person, true IoU is ``0.002 / 0.060 = 0.033`` -- below
        the documented default ``iou_threshold: 0.1``.  Scoring by IoU would therefore
        associate **nothing** at the default, every subject would read non-compliant, and
        ``compliance_pct`` would be a plausible-looking constant 0.  That is exactly the
        silent-wrong-number failure mode this engine exists to remove (``09`` §3), so the score
        is normalised by the smaller of the two areas, for which a fully-contained attribute
        scores ``1.0``.
    
        Args:
            subject: The detection being assessed, e.g. a ``person``.
            attribute: The detection that may belong to it, e.g. a ``hardhat``.
    
        Returns:
            ``intersection / min(area(subject), area(attribute))``, or ``0.0`` when the boxes
            are disjoint or either is degenerate.
    """
    ...

# From segmentation_area
def decode_simple_rle_area(counts: str) -> int:
    """
    Foreground pixel count from a base64 ``simple_rle`` run-length string.
    
        The decoded bytes are little-endian ``uint32`` run lengths that alternate
        background/foreground **starting with background**, laid out row-major over the mask's
        ``size`` (contract ``04`` §5.1).  The foreground area is therefore the sum of the runs at
        **odd** indices -- no allocation of the mask itself, no numpy, ``O(runs)``.
    
        Args:
            counts: The base64 ``counts`` string as the producer sends it.
    
        Returns:
            Total foreground pixels.  ``0`` for an empty string, which is a legitimate
            "nothing segmented" rather than an error.
    
        Raises:
            ValueError: The string is not base64, or its decoded length is not a multiple of 4.
                Both mean the payload is not what it claims to be, and a truncated final run
                would silently under-report the area.
    
        Example:
            >>> import base64, struct
            >>> counts = base64.b64encode(struct.pack("<4I", 2, 3, 4, 7)).decode()
            >>> decode_simple_rle_area(counts)  # 3 + 7 foreground pixels
            10
    """
    ...

# From segmentation_area
def measure_mask(mask: Any | None) -> Any | None:
    """
    Measure one mask, or return ``None`` when it carries nothing usable.
    
        The three-tier cascade of ``landslide_detection.py:283-313``, minus its silent tiers:
        a pre-computed :attr:`~.base.MaskRef.area_px`, then :attr:`~.base.MaskRef.rle`, then
        :attr:`~.base.MaskRef.polygon`.  The denominator is always the mask's own
        :attr:`~.base.MaskRef.size`, which is the correction to legacy's Tier 2 -- that tier
        divides a polygon area by the *frame* area while Tier 1 divides by the mask's, so the two
        tiers of one function publish two different quantities under one name.
    
        A polygon with no ``size`` is treated as already normalized 0-1, because that is the only
        other coordinate space this engine has.
    
        Returns:
            The measurement, or ``None`` when there is no mask, no usable size, or no carrier.
            ``None`` is what :attr:`SegmentationArea.on_missing_mask` then decides about -- it is
            never quietly turned into ``0.0``.
    
        Raises:
            ValueError: The mask claims an encoding this module cannot decode, or its ``rle`` is
                malformed.  Loud, because a mis-decoded mask is a plausible wrong number.
    """
    ...

# From segmentation_area
def polygon_area(points: Any[Any[float]]) -> float:
    """
    Unsigned area of a simple polygon, by the shoelace formula.
    
        ``cv2.contourArea`` returns exactly this for a simple (non-self-intersecting) contour, so
        replacing the legacy call (``landslide_detection.py:302``) with 4 lines of stdlib is
        behaviour-preserving rather than an approximation -- and it removes a cv2 import from a
        module the engine is forbidden to have one in (**PY-20**).
    
        Args:
            points: ``[(x, y), ...]`` vertices, in either winding order, in any one unit.
    
        Returns:
            The area in that unit squared; ``0.0`` for fewer than three vertices, which is a
            degenerate contour and not an error.
    """
    ...

# From track
def assign(cost: list[list[float]], threshold: float) -> tuple[list[tuple[int, int]], list[int], list[int]]:
    """
    Optimal assignment, then drop every pair costing more than ``threshold``.
    
        The order matters and is the legacy behaviour
        (``advanced_tracker/matching.linear_assignment``): solving first and gating second
        keeps the assignment globally optimal, where gating first would let a cheap-but-wrong
        pair win because the right one was pruned.
    
        Args:
            cost: An ``n x m`` cost matrix.
            threshold: The maximum acceptable cost.  **This is a cost, not an IoU** --
                ``TrackConfig.match_thresh`` of ``0.8`` accepts an IoU as low as ``0.2``.  The
                legacy field name reads like a similarity and is not one; the semantics are
                preserved here rather than quietly inverted, because inverting them would
                change the behaviour of every migrated app.
    
        Returns:
            ``(pairs, unmatched_rows, unmatched_columns)``.
    """
    ...

# From track
def hungarian(cost: list[list[float]]) -> list[tuple[int, int]]:
    """
    Optimal one-to-one assignment minimising total cost (Jonker-Volgenant).
    
        The shortest-augmenting-path form of the Hungarian algorithm, ``O(n^2 m)``.  It is here
        rather than ``scipy.optimize.linear_sum_assignment`` because a primitive may not import
        scipy (**PY-20**); it returns the same optimum, and at the frame sizes this runs at
        (tens of boxes) the pure-Python cost is irrelevant next to being able to import the
        engine at all.
    
        Greedy nearest-neighbour matching was the alternative and is rejected on purpose: it
        swaps the ids of two objects that cross, and an id swap is invisible in the counts
        while corrupting every downstream dwell and unique count.
    
        Args:
            cost: An ``n x m`` cost matrix.  Rows and columns may differ in length.
    
        Returns:
            ``(row, column)`` pairs, at most ``min(n, m)`` of them, sorted by row.  Every cost
            is assigned -- the caller drops the pairs it considers too expensive.
    """
    ...

# From track
def iou(a: Any, b: Any) -> float:
    """
    Intersection over union of two boxes.
    
        Args:
            a: First box, ``(xmin, ymin, xmax, ymax)``.
            b: Second box.
    
        Returns:
            ``0.0`` for disjoint or degenerate boxes, up to ``1.0`` for identical ones.
    """
    ...

# From track
def observations_from(detections: Any[Any]) -> list[Any]:
    """
    Build tracker observations from detections -- exposed for tests.
    
        Lets a test drive :class:`_Tracker` directly with the same conversion
        :meth:`Track.process` uses, rather than re-deriving it and drifting.
    """
    ...

# From velocity_state
def heading_degrees(dx: float, dy: float) -> float:
    """
    Direction of travel in degrees: 0 = east/right, counter-clockwise positive.
    
        ``atan2(-dy, dx)`` -- the ``y`` is negated because image coordinates grow *downwards*,
        so a detection moving up the frame has a negative ``dy`` and must read as +90, not -90.
        This is the convention ``crowdflow.py:101-117`` gets right and
        ``fall_detection.py:1665`` deliberately swaps; stating it here means the next primitive
        does not have to guess.
    
        Args:
            dx: Horizontal displacement, any consistent unit.
            dy: Vertical displacement, same unit, positive = downwards.
    
        Returns:
            Degrees in ``[0, 360)``.
    """
    ...

# From velocity_state
def heading_to_unit_vector(heading: float) -> tuple[float, float]:
    """
    The exact inverse of :func:`heading_degrees`: a heading back to a unit ``(dx, dy)``.
    
        Needed only by the ``heading_auto_learn_fallback`` estimator
        (:meth:`VelocityState._update_auto_learn`), which must average several tracks'
        *directions*, weighted by speed, to find the dominant one -- averaging two headings of,
        say, 350 and 10 degrees the naive way gives 180, the opposite of the two nearly-agreeing
        directions that produced it. Going back to vectors and averaging those is the same fix
        ``wrong_way_tracker.py``'s own estimator got for free by never leaving vector space.
    """
    ...

# From velocity_state
def note_unassociated_frame(ctx: Any, stage: str, tracker: str) -> float:
    """
    Count and log a frame where the tracker associated nothing (**loud, not silent**).
    
        "A tracker ran and associated nothing" is legitimate -- for a few frames at stream
        start, while ``track.min_hits`` confirms, or when every detection sits below
        ``new_track_thresh``.  It is *not* legitimate for a whole stream, and that is
        indistinguishable from a quiet camera unless somebody counts it.  So it is counted
        (:data:`UNASSOCIATED_FRAMES_KEY`, ``PERSISTENT``) and logged on a decelerating schedule
        rather than raised.
    
        Returns:
            How many such frames this stage has seen since process start.
    """
    ...

# From velocity_state
def reference_point(det: Any) -> tuple[float, float]:
    """
    The normalized 0-1 point whose motion *is* the object's motion: the box centre.
    
        See the module docstring for why this is the centre and not one of the three foot
        points the legacy tree uses.  Kept a module function rather than a method so ``dwell``
        and a custom primitive can agree with this one without inheriting anything (``09`` §3).
    """
    ...

# From velocity_state
def require_track_ids(ctx: Any, stage: str) -> tuple[tuple[int, Any], ...]:
    """
    This frame's detections paired with their tracker ids.
    
        Shared by :mod:`~matrice_analytics.engine.primitives.velocity_state` and
        :mod:`~matrice_analytics.engine.primitives.dwell`, which have identical needs and
        identical failure modes.  ``state_machine`` deliberately does **not** use it: its config
        model declares no ``REQUIRES``, so a manifest may legally run it untracked.
    
        The ids are read from ``det.track_id``, which the **runtime** fills in from the tracker
        stage's :attr:`~.base.PrimitiveOutput.tracks` before this stage sees the frame.  A
        caller-supplied id is used as-is.
    
        Args:
            ctx: The frame.
            stage: The calling stage's name, for the error message.
            state: The calling stage's store, so a tracker that associates nothing can be
                *counted* rather than silently tolerated.  Optional only for a direct caller
                that has none.
    
        Returns:
            ``(track_id, detection)`` pairs, in frame order.  Empty when the frame is empty --
            a quiet camera is not an error -- or when a tracker ran and associated nothing,
            which is counted and logged by :func:`note_unassociated_frame`.
    
        Raises:
            TrackingRequiredError: There are detections and none of them carries a ``track_id``,
                and either no tracker ran at all, or one ran and published tracks that never
                reached the detections.  See :class:`TrackingRequiredError` for why the second
                case is an error and not a shrug: it is the defect that starved this primitive,
                and the only way to keep it from coming back silently.
    """
    ...

# From velocity_state
def signed_heading_delta(heading: float, expected: float) -> float:
    """
    The smallest absolute angle between two headings, in degrees ``[0, 180]``.
    
        Wrapping done once, here: 350 vs 10 is 20 degrees apart, not 340.  Every legacy
        comparison of two angles in this tree either avoids the problem by using a dot product
        (``wrong_way_tracker.py``) or does not compare angles at all.
    """
    ...

# From velocity_state
def tracker_stage(ctx: Any) -> tuple[str, int] | None:
    """
    The upstream tracker stage in this pipeline, as ``(stage name, tracks published)``.
    
        Answers the question the silent-zero bug turned on: *did a tracker run?*  A stage is a
        tracker if it publishes :data:`TRACKER_MARKER_VALUE`, which ``track`` does on every
        frame, or if it published a non-empty ``tracks`` map.  Both are checked because the
        first is the reliable signal and the second keeps a hand-built test double working.
    
        Args:
            ctx: The frame.  Only :attr:`~.base.FrameContext.previous` is read.
            prefer: A specific stage name to follow, for a manifest running two trackers.  When
                given, only that stage is considered -- following "whichever tracker happens to
                be first" would silently count against the wrong one.
    
        Returns:
            ``(stage name, len(tracks))`` for the tracker, or ``None`` when no stage before this
            one is a tracker.  A count of ``0`` means the tracker ran and associated nothing.
    """
    ...

# Classes
# From base
class Clock:
    # The engine's only source of "now".
    #
    #     Injectable so that replay, backfill and generated tests are driven by frame time
    #     rather than by the host's wall clock (**PY-13**).  Windowing
    #     (``engine/runtime/window.py``) consumes this; primitives should read
    #     :attr:`FrameContext.frame_ts` and never call a clock at all.

    def now(self: Any) -> float:
        """
        Current time in epoch seconds.
        """
        ...


# From base
class CustomPrimitive:
    # A full pipeline stage written by an app author (``09`` §6).
    #
    #     Narrower than :class:`Primitive` on purpose: no ``name`` (the manifest stage supplies
    #     it) and no ``window`` (the runtime aggregates the ``values`` a custom stage publishes,
    #     using each metric's ``agg_type``).  ``reset`` is optional; the runtime calls it if it
    #     is there.
    #
    #     The loader enforces exactly ``Config`` + ``process``
    #     (``manifest/loader.py:_resolve_custom_impl``), so this protocol and that check must
    #     stay in step.
    #
    #     Custom code must not touch the wire format, re-implement a primitive, do network I/O,
    #     load a model, or spawn a thread -- each is a current pathology with a name in
    #     ``12-defect-register.md`` (**PY-15** for the last one).

    def __init__(self: Any, config: Any, state: Any) -> None: ...

    def process(self: Any, ctx: Any) -> Any: ...


# From base
class FrameClock:
    # The default clock: it advances only when a frame says so (**PY-13**).
    #
    #     Feeding it the real frame timestamp makes a replayed hour of footage produce exactly
    #     the windows the live run produced.  ``time.time()`` cannot do that, which is the whole
    #     defect.
    #
    #     Example:
    #         >>> clock = FrameClock()
    #         >>> clock.advance(1_700_000_000.0)
    #         >>> clock.now() == 1_700_000_000.0
    #         True

    def advance(self: Any, frame_ts: float) -> None:
        """
        Move the clock to ``frame_ts``.
        
                Args:
                    frame_ts: The real frame timestamp, epoch seconds.
        
                Raises:
                    ValueError: ``frame_ts`` goes backwards.  Out-of-order frames would reopen a
                        closed window and double-publish it; the caller must decide to drop or to
                        reset, and cannot decide it by accident.
        """
        ...

    def now(self: Any) -> float:
        """
        The timestamp of the most recent frame.
        """
        ...

    def reset(self: Any, frame_ts: float = 0.0) -> None:
        """
        Force the clock to ``frame_ts``, e.g. when a stream restarts.
        """
        ...


# From base
class FrameContext:
    # Everything a primitive is given for one frame, in one zone.
    #
    #     A plain frozen dataclass rather than a Pydantic model **on purpose**: this is
    #     constructed once per frame *per zone* -- at 25 fps with four zones that is 100
    #     validations a second per camera -- and its contents have already been validated
    #     upstream (``StreamInfo`` for ``fps``, :class:`PipelineDetection` for the detections).
    #     The models in ``engine/contract`` and ``engine/manifest`` sit on cold paths and stay
    #     Pydantic; the hot path does not.
    #
    #     Frozen, with ``detections`` copied to a tuple and ``previous`` wrapped read-only, so a
    #     primitive cannot mutate the set the next primitive in the pipeline is about to see.

    def camera_id(self: Any) -> str:
        """
        The camera this frame came from, or ``""`` when no stream is attached.
        """
        ...

    def frame_id(self: Any) -> str:
        """
        The frame's media anchor, or ``""``. Useful when raising an event.
        """
        ...

    def of_entity(self: Any, *entities: Any) -> tuple[Any, ...]:
        """
        This frame's detections restricted to ``entities``.
        
                The one convenience on this type.  It is here rather than on a base class because
                every primitive needs it and none of them may inherit anything (``09`` §3) -- and
                it is a filter over data the caller already has, not a shared behaviour that could
                grow into another ``BaseProcessor``.
        """
        ...

    def require_resolution(self: Any, what: str) -> tuple[int, int]:
        """
        ``resolution``, or a loud error naming who needed it and why.
        
                Bounding boxes are normalized 0-1; anything expressed in pixels -- zone polygons,
                a px/s speed threshold, an inset distance -- needs this to be meaningful. Guessing
                a default produces output that is plausible and wrong by the ratio of the guessed
                frame size to the real one, which is far worse than not starting.
        """
        ...

    def resolution(self: Any) -> tuple[int, int] | None:
        """
        ``(width, height)`` in pixels, or ``None`` when unknown.
        
                ``None`` and ``(0, 0)`` both mean "not configured" and both come back as ``None``,
                so callers have one thing to check. Use :meth:`require_resolution` when the
                primitive cannot work without it.
        """
        ...

    def zone_config(self: Any) -> 'Any | None':
        """
        The camera's zone geometry, normalized 0-1, or ``None`` when unconfigured.
        """
        ...


# From base
class Keypoint:
    # One pose joint, ``(x, y, confidence)``, **normalized 0-1** like a bounding box.
    #
    #     A tuple rather than a model because that is the wire shape
    #     (``_contracts/04-asis-live-frame-contract.md:678-706``: a fixed-length list of
    #     ``[x, y, confidence]``) and because a skeleton is 17 of these per person per frame --
    #     validating a Pydantic model 425 times a second at 25 fps buys nothing that the intake
    #     parse has not already checked.
    #
    #     **Both coordinate conventions in one field is defect PY-7**, so there is only one here.
    #     The legacy tree's keypoints are absolute pixels -- ``hands_above_head_margin_px`` is
    #     compared directly against a joint ``y`` (``fence_climbing_detection_pose.py:139``) and
    #     ``head_h = shoulder_y - y1`` mixes a joint ``y`` with a bbox edge
    #     (``face_covering_detection_pose.py:175``) -- while every box in this engine is
    #     normalized 0-1 and a box outside that range is rejected outright (**BE-10**/**BE-12**).
    #     Mixing the two in one :class:`FrameContext` is how a silent 1920x error happens, so
    #     ``runtime/session.py`` normalizes at intake and everything downstream reads 0-1.
    #
    #     :attr:`confidence` is the per-joint visibility score.  **A payload with no confidence
    #     channel yields 0.0, never 1.0.**  Legacy forges ``1.0`` (``fall_detection.py:86``,
    #     ``:103``, ``:112``, and the same lines in both siblings), which makes every
    #     ``min_keypoint_confidence`` gate pass unconditionally whatever the manifest says -- a
    #     config field that cannot fail is worse than no field.

    ...

# From base
class MaskRef:
    # A segmentation mask as the engine carries it -- **a reference, not pixels**.
    #
    #     Engine-internal like :attr:`PipelineDetection.entity`, with one exception:
    #     :meth:`PipelineDetection.to_wire` re-emits :attr:`rle` (when present) as the wire's
    #     declared, RLE-only ``Detection.segmentation`` field -- never :attr:`polygon` or a
    #     rasterized :attr:`area_px`, since this engine does not encode pixels for the wire (no
    #     numpy/cv2, **PY-20**) and a decoded shape has nothing ready-to-emit.
    #
    #     Three carriers, because the producers ship three and each is cheaper than the last to
    #     turn into an area (``landslide_detection.py:283-313`` cascades over exactly these):
    #
    #     :attr:`area_px`
    #         A foreground pixel count already computed upstream
    #         (``merged_det["segmentation_area"] = mask_info["area_pixels"]``,
    #         ``landslide_detection.py:836``).  Free -- no decode at all.
    #     :attr:`rle`
    #         The base64 ``simple_rle`` the live producer sends
    #         (``_contracts/04-asis-live-frame-contract.md:657-671``).  Decoded by
    #         :func:`~matrice_analytics.engine.primitives.segmentation_area.decode_simple_rle_area`
    #         with ``base64`` and ``int.from_bytes`` -- **no numpy, no cv2** (**PY-20**).
    #     :attr:`polygon`
    #         A contour.  ``cv2.contourArea`` returns the unsigned shoelace area of a simple
    #         polygon, so the pure-Python shoelace in
    #         :func:`~matrice_analytics.engine.primitives.segmentation_area.polygon_area` is
    #         behaviour-preserving rather than an approximation.
    #
    #     :attr:`size` is the mask's **own** array shape, ``(height, width)``, in model input
    #     space.  It is the denominator, which is why ``segmentation_area`` needs no frame
    #     resolution: a mask covers the whole frame in model space, so ``area_px / (h * w)`` is
    #     resolution-free.  That is the choice legacy Tier 1 made
    #     (``landslide_detection.py:285-291``) and the reason this primitive never calls
    #     :meth:`FrameContext.require_resolution`.

    ...

# From base
class PipelineDetection:
    # A wire :class:`~matrice_analytics.engine.contract.schemas.Detection` plus the
    #     fields the pipeline adds before a primitive sees it.
    #
    #     ``09`` §3 says ``FrameContext.detections`` are "already entity-remapped and
    #     zone-assigned", but the wire ``Detection`` carries neither an ``entity`` nor a
    #     ``zone``: ``category`` is the *model's* class label, which is precisely what entity
    #     remapping exists to stop primitives from depending on.  Rather than redeclare the
    #     detection (the contract owns it -- **O1**), this subclasses it, so
    #     :class:`~matrice_analytics.engine.contract.schemas.BoundingBox`, the 0-1 range check
    #     (**BE-10**, **BE-12**) and the confidence check keep applying unchanged.
    #
    #     :meth:`to_wire` converts back.  Use it -- the extra two fields must not reach the
    #     payload, and ``extra="forbid"`` on the wire model means a stray one is a hard failure
    #     at emit rather than a silent extra key.

    def from_detection(cls: Any, detection: Any) -> 'Any':
        """
        Attach pipeline fields to a wire detection.
        
                ``mask`` and ``keypoints`` are keyword-only and default to "absent" because the wire
                :class:`~matrice_analytics.engine.contract.schemas.Detection` cannot carry them --
                they come from the raw producer dict, which ``runtime/session.py`` parses.
        """
        ...

    def to_wire(self: Any) -> Any:
        """
        Drop the pipeline-internal fields, yielding the contract's detection.
        
                ``entity`` and ``zone`` are engine concepts: the payload's per-zone structure
                already carries the zone (**FROZEN-2**) and its ``category`` is the model label the
                overlay draws.  Emitting either would be a new, undeclared wire field.
                :attr:`keypoints` is dropped for the same reason.
        
                :attr:`mask` is the one field that conditionally survives: its ``rle`` (when the
                producer sent a ready-to-emit ``simple_rle`` string) becomes ``Detection.segmentation``
                below, byte for byte -- a genuinely declared wire field (:class:`WireSegmentationMask`
                on :class:`Detection`), not a leak, since ``extra="forbid"`` would reject anything not
                named on that model.  A mask that only carries a polygon or a precomputed
                :attr:`~.MaskRef.area_px` has nothing ready-to-emit -- this method never rasterizes or
                encodes pixels (no numpy/cv2, **PY-20**) -- so ``segmentation`` stays ``None`` for it,
                same as for a detector-only stream.  This method still names every wire field
                explicitly rather than copying whatever :class:`PipelineDetection` happens to hold, so
                an engine-internal field cannot leak into a payload by being added upstream.
        """
        ...


# From base
class Primitive:
    # The one interface (``09`` §3).  A protocol, so there is nothing to inherit.
    #
    #     An implementation is any class with these members -- no registration in a base class,
    #     no ``super().__init__()``, no ``BaseProcessor``.  That is the point: the ~20 payload
    #     helpers and their duplicate deprecated twins accumulated on
    #     ``core/base.py:617-781`` *because* there was somewhere shared to put them.
    #
    #     Implementations are pure over ``(detections, state, config)``: given the same frames
    #     and the same starting state they produce the same outputs, which is what makes the
    #     generated determinism test (**O5**) meaningful.
    #
    #     Note:
    #         ``isinstance(obj, Primitive)`` checks only that the members exist -- that is all a
    #         ``runtime_checkable`` protocol can do.  Use :func:`conformance_problems` when you
    #         want the *reasons* something does not conform.

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Construct with a validated config and an already-scoped state store.
        
                The store is scoped to ``<camera_id>/<app_id>/<zone>/<primitive>`` by the runtime,
                so an implementation writes bare names (``state.set("seen", ...)``) and cannot
                collide with another camera, app, zone or stage.
        
                **All** mutable state goes through ``state``.  A plain ``self._counts`` dict is a
                review defect: it is invisible to a future Redis backing (``09`` §4, **D6**).
        """
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Handle one frame, in one zone.  No I/O, no threads, no models (``09`` §6).
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear window-scoped state at the aggregation boundary.
        
                **Not** a full reset.  ``09`` §4 rule 2: window sums clear here; cumulative totals
                clear only when the process does (**FROZEN-4**).  Implementations express this by
                calling :meth:`~matrice_analytics.engine.state.store.StateStore.end_window`, or by
                clearing named keys -- what they must not do is clear a total, because the
                backend's rollup formula assumes those only reset on restart.
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Collapse this stage's per-frame outputs into the 60-second aggregation.
        
                Given the outputs this same instance returned from :meth:`process` during the
                window, in frame order.
        """
        ...


# From base
class PrimitiveEvent:
    # An **incident candidate** -- something happened, at a frame time.
    #
    #     Deliberately not an incident: severity here is a free string and the runtime maps it
    #     through :func:`matrice_analytics.engine.contract.schemas.parse_severity` on the way to
    #     the wire.  A primitive that imported the wire ``Severity`` enum would know the wire
    #     format, and then so would the next one (**O1**).
    #
    #     Incident *lifecycle* -- confirmation frames, find-or-create on ``incident_id``,
    #     up-only escalation, closing -- belongs to the runtime, not here.  A primitive says
    #     "this is happening now"; nothing more.

    ...

# From base
class PrimitiveOutput:
    # What one pipeline stage produces for one frame, in one zone (``09`` §3).

    ...

# From base
class PrimitiveRegistrationError:
    # A class cannot be registered as a primitive implementation.

    ...

# From base
class PrimitiveRegistry:
    # Manifest primitive name -> implementation class.
    #
    #     This is how the runtime turns a validated manifest into a pipeline without knowing a
    #     single app's name (``09`` §1): it reads ``pipeline[].kind``, looks the class up here,
    #     and constructs it with the stage's already-validated config and a scoped state store.
    #
    #     The key set is closed -- it is
    #     :data:`matrice_analytics.engine.manifest.models.PRIMITIVES`, the same 17 names the
    #     manifest schema accepts.  Registering anything else raises, because a primitive no
    #     manifest can name is dead code and a manifest naming a primitive that is not here must
    #     fail loudly at load, not silently emit nothing.
    #
    #     Example:
    #         >>> registry = PrimitiveRegistry()
    #         >>> @registry.register
    #         ... class Detect:
    #         ...     name = "detect"
    #         ...     Config = DetectConfig
    #         ...     def __init__(self, config, state): ...
    #         ...     def process(self, ctx): return PrimitiveOutput()
    #         ...     def window(self, frames): return WindowOutput()
    #         ...     def reset(self): ...
    #         >>> registry.get("detect") is Detect
    #         True

    def __init__(self: Any) -> None: ...

    def create(self: Any, name: str, config: Any, state: Any) -> Any:
        """
        Instantiate the primitive registered for ``name``.
        
                Args:
                    name: The manifest primitive key.
                    config: The stage's validated config, an instance of the class's ``Config``.
                    state: A store already scoped to
                        ``<camera_id>/<app_id>/<zone>/<primitive>`` (``09`` §4).
        
                Returns:
                    The constructed primitive.
        
                Raises:
                    KeyError: Nothing is registered for ``name``.
                    TypeError: ``config`` is not an instance of the class's ``Config`` model.
        """
        ...

    def get(self: Any, name: str) -> Any[Any]:
        """
        The class registered for ``name``.
        
                Raises:
                    KeyError: Nothing is registered for it.  The message distinguishes "not
                        implemented yet" (``08`` §2 marks four primitives 🔜) from "not a
                        primitive at all", because the fix differs.
        """
        ...

    def missing(self: Any) -> tuple[str, ...]:
        """
        Manifest primitives with no implementation yet, sorted.
        
                The runtime's startup check: a manifest naming one of these must fail loudly
                (``09`` §5), and this is the list it fails against.
        """
        ...

    def names(self: Any) -> tuple[str, ...]:
        """
        Registered primitive names, sorted -- deterministic for tests and logs.
        """
        ...

    def register(self: Any, impl: Any[Any] | None = None) -> Any:
        """
        Register an implementation.  Usable bare or with an explicit name.
        
                ``@registry.register`` takes the key from ``cls.name``;
                ``@registry.register(name="detect")`` states it, and then ``cls.name`` must agree
                (two spellings of one key is how the legacy catalogue ended up with two
                registration lists that disagree -- ``09`` §9).
        
                Args:
                    impl: The class, when used as a bare decorator.
                    name: The manifest primitive key, when stated explicitly.
        
                Returns:
                    The class (bare form) or a decorator (keyword form).
        
                Raises:
                    PrimitiveRegistrationError: The name is unknown to the manifest schema,
                        already taken, disagrees with ``cls.name``, or the class does not conform.
        """
        ...


# From base
class PrimitiveValueError:
    # A :attr:`PrimitiveOutput.values` entry is not a publishable scalar.
    #
    #     Caught at construction rather than at emit: by the time the contract rejects a
    #     ``None`` the frame that produced it is gone, and the failure reads as "the payload is
    #     malformed" rather than "this primitive returned nothing for this key".

    ...

# From base
class SourceResolutionError:
    # A ``metrics[].source`` does not resolve against the pipeline's outputs.
    #
    #     ``09`` §3: *an unresolvable source is a manifest load error -- not a metric that reads
    #     zero forever*.  The current engine's silent-zero behaviour is indistinguishable from a
    #     genuinely quiet camera, which is why this raises.

    ...

# From base
class TrackState:
    # One tracked object as a primitive sees it.
    #
    #     Carried on :attr:`PrimitiveOutput.tracks` so that a later stage (``dwell``,
    #     ``velocity_state``, a custom primitive) can read it without re-implementing tracking --
    #     the thing every use case does today, and the reason 17 of them hand-rolled a dwell
    #     clock.

    def duration_seconds(self: Any) -> float:
        """
        How long this track has been observed, in frame time.
        """
        ...


# From base
class WallClock:
    # ``time.time()``, for the few places that genuinely mean wall-clock.
    #
    #     Never the default.  Passing this where a :class:`FrameClock` belongs is exactly
    #     **PY-13** (``engine_session.py:595``), so it is a named type you have to opt into
    #     rather than a bare call buried in a session.

    def now(self: Any) -> float:
        """
        Current wall-clock time in epoch seconds.
        """
        ...


# From base
class WindowOutput:
    # What one stage contributes to the 60-second aggregation (``09`` §3).
    #
    #     Separate from :class:`PrimitiveOutput` because it means something different: these
    #     values are already collapsed over the window and are published once, whereas a
    #     ``PrimitiveOutput.values`` entry is a per-frame sample that ``metrics[].agg_type`` still
    #     has to collapse.  Conflating the two is how a percentage gets published as a
    #     60-second *sum* (**PY-1**).
    #
    #     There are no ``tracks`` here: a track is a per-frame fact, and the window is over.

    ...

# From detect
class Detect:
    # Thresholded class presence and counts for one zone, one frame.
    #
    #     Publishes, into :attr:`PrimitiveOutput.values`:
    #
    #     ``<entity>.count``
    #         Admitted detections of that entity this frame, one key per
    #         :attr:`DetectConfig.classes` entry.  Always present, ``0`` when the entity is
    #         absent -- an omitted key would make ``metrics[].source`` unresolvable and turn a
    #         quiet camera into a manifest load error (``09`` §3).
    #
    #     ``total``
    #         The sum of the per-entity counts.
    #
    #     ``max_confidence``
    #         The highest admitted confidence, ``0.0`` when nothing was admitted.
    #
    #     :meth:`window` publishes the same three names **plus** ``<entity>.count_peak`` and
    #     ``total_peak``.  The un-suffixed names carry the window's *last-frame* value and the
    #     suffixed ones its *peak*, because a window output is published as-is and therefore has to
    #     say which reading it is -- ``agg_type`` cannot choose between them.  See :meth:`window`.
    #
    #     Example:
    #         >>> from matrice_analytics.engine.state import InMemoryStateStore
    #         >>> config = DetectConfig(classes=["person"])
    #         >>> stage = Detect(config, InMemoryStateStore().for_primitive("c1", "a1", "global", "detect"))
    #         >>> out = stage.process(ctx)                       # doctest: +SKIP
    #         >>> out.values["person.count"]                     # doctest: +SKIP
    #         3

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Bind a validated config and an already-scoped state store.
        
                Args:
                    config: The stage's validated :class:`DetectConfig`.
                    state: A store scoped to ``<camera_id>/<app_id>/<zone>/<primitive>``
                        (``09`` §4).  Every mutable value this primitive owns lives here; there is
                        deliberately no ``self._counts`` (**D6**).
        
                Note:
                    ``min_confidence`` defaults to ``0.0`` rather than to a guessed model
                    threshold.  ``DetectConfig.min_confidence`` documents itself as an *override*
                    of ``model.confidence_threshold``, and a primitive cannot see the model block
                    (``09`` §1) -- so with no override the pipeline's own thresholding stands and
                    this stage adds none of its own.  Inventing a default here would silently drop
                    detections the app asked to keep.
        """
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Count this frame's admitted detections, per entity and in total.
        
                Args:
                    ctx: One frame in one zone.  Detections are already entity-remapped and
                        zone-assigned, so this reads :attr:`PipelineDetection.entity` and never the
                        model's ``category`` (``09`` §3).
        
                Returns:
                    The per-entity counts, the total and the peak confidence.
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear the window peaks at the aggregation boundary -- and nothing else.
        
                ``09`` §4 rule 2 in one line: :meth:`StateStore.end_window` drops every
                :attr:`Lifetime.WINDOW` key and leaves the
                :attr:`Lifetime.PERSISTENT` smoothing windows alone.  Clearing those would make
                every object in frame re-ramp its confidence window once a minute, which reads
                downstream as a count that dips at :00 -- a wrong number that looks like flaky
                analytics rather than like a bug.
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Publish **both** readings of the window, under two names each -- never a sum.
        
                A count is a level, not an event: summing 1,500 per-frame "3 people" samples
                publishes 4,500 people.  Conflating the two is exactly **PY-1**, which is why
                :class:`WindowOutput` is a separate type from :class:`PrimitiveOutput` in the first
                place.
        
                The peak is not the *only* honest collapse of a level, though, and pretending it was
                is a defect of its own.  A :class:`WindowOutput` is published verbatim -- the runtime
                does not re-apply ``metrics[].agg_type`` to a registered primitive, deliberately -- so
                while this method published one number per name, a manifest asking for
                ``current_occupancy`` (``agg_type: last``) and ``peak_occupancy`` (``agg_type: max``)
                off the same source got the *peak* twice and ``current_occupancy`` was simply wrong.
                The rule is: **a stage's window value is what it is; if you need two readings, publish
                two names.**  So:
        
                ``<entity>.count`` / ``total``
                    The value on the window's **last** frame -- "how many are in view now", which is
                    what ``agg_type: last`` means.
                ``<entity>.count_peak`` / ``total_peak``
                    The window's **high-water mark** -- "how many at the busiest moment", which is what
                    ``agg_type: max`` means.
                ``max_confidence``
                    The window maximum.  One name, one reading: it is already declared as a maximum, and
                    the confidence on an arbitrary last frame answers no question.
        
                Args:
                    frames: This stage's per-frame outputs for the window, in frame order.  Folded into
                        the *peaks* so those are right whether or not the runtime retained them; the
                        last readings come from the store only, because retention is capped and
                        ``frames[-1]`` is therefore not reliably the window's last frame.
        
                Returns:
                    The last and peak per-entity counts, the last and peak totals, and the peak
                    confidence.
        """
        ...


# From dwell
class Dwell:
    # Time-in-state per track, aggregated over one zone.
    #
    #     Publishes exactly the four values
    #     :attr:`~matrice_analytics.engine.manifest.models.DwellConfig.STATIC_OUTPUTS` declares:
    #
    #     ======================== ==========================================================
    #     ``avg_seconds``          Mean session length over qualifying live sessions.
    #     ``max_seconds``          Longest qualifying live session.
    #     ``over_threshold_count`` Sessions past ``threshold_seconds`` **right now**.
    #     ``active_count``         Qualifying sessions not yet timed out.
    #     ======================== ==========================================================
    #
    #     "Qualifying" means ``seconds >= min_presence_seconds`` -- the flicker suppressor.  A
    #     track that appears for two frames and vanishes never reaches it and never moves a
    #     number.
    #
    #     "Live" means ``frame_ts - last_seen <= track_timeout_seconds``, so a session survives an
    #     occlusion and keeps counting through it.  ``active_count`` therefore includes the person
    #     currently behind the pillar, which is the honest answer to "how many are dwelling".
    #
    #     :meth:`window` re-reads ``over_threshold_count`` at window scope, where it means
    #     something different, and publishes ``active_count_peak`` alongside ``active_count`` --
    #     plus ``over_threshold_count_last`` and ``over_threshold_count_peak``, which are the gauge
    #     this method computes every frame -- so that every reading has its own name and none of
    #     them depends on an ``agg_type`` the runtime does not apply.  See its docstring (**PY-1**).

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Bind a validated config to a state store already scoped to this stage.
        
                ``state: stationary`` is desugared here into the gate it implies, so there is one
                gate-evaluation path rather than a state predicate that duplicates it.  An explicit
                ``gate:`` always wins, which is how an app names a ``velocity_state`` stage that the
                manifest gave a custom ``name:``.
        
                Args:
                    config: The validated ``dwell:`` block.
                    state: Scoped to ``<camera_id>/<app_id>/<zone>/<stage>`` by the runtime.
                    zoned: Whether the runtime is running this app **per zone**.  Supplied by the
                        runtime the same way ``geometry`` and ``on_overlap`` are
                        (``runtime/session.py:_construct`` inspects the signature), because it is the
                        one fact this stage cannot see for itself: ``ctx.zone == "global"`` looks the
                        same in a single-bucket app and in the always-present ``global`` bucket of a
                        zoned one, and ``state: in_zone`` must fail loudly in the first and skip
                        quietly in the second.  ``ctx.zone_config`` cannot stand in for it -- a
                        camera may have polygons drawn for a *different* app.
                    bucket: The bucket this instance was built for.  Supplied the same way and for the
                        same reason: :meth:`window` has no :class:`FrameContext`, so without it this
                        stage cannot tell at window scope that it is the ``unassigned`` instance --
                        the one bucket where ``state: in_zone`` can never open a session and must
                        therefore publish **nothing** rather than a resolved ``0``
                        (:attr:`_measures_nothing`).
        """
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Advance every open session by this frame's elapsed time.
        
                Args:
                    ctx: This frame, in this zone.  Every duration is a difference of
                        :attr:`~.base.FrameContext.frame_ts` values (**PY-13**).
        
                Returns:
                    The four declared values plus a :class:`~.base.TrackState` per live session, or
                    **no values at all** in the ``unassigned`` bucket (:attr:`_measures_nothing`).
        
                Raises:
                    TrackingRequiredError: No tracker ran, or one ran and its ids never reached the
                        detections -- see :func:`~.velocity_state.require_track_ids`.
                    DwellGateError: The stage is configured against something the pipeline cannot
                        supply -- see :class:`DwellGateError`.
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear window-scoped state only (``09`` §4 rule 2).
        
                ``sessions`` is :attr:`Lifetime.PERSISTENT` and **survives**.  This is the whole
                reason the lifetime enum exists: a person still standing there when the window ticks
                keeps their clock.  Clearing it would cap every measurable dwell at 60 seconds and
                make ``threshold_seconds: 90`` unreachable -- a manifest the schema accepts and the
                runtime could never satisfy.
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Collapse the window.  ``over_threshold_count`` changes meaning here (**PY-1**).
        
                Per frame it is *how many are over the threshold right now*.  Summed over 1500
                frames one loiterer reports 1500, which is the published-a-gauge-as-a-sum defect.
                At window scope it is the number of **distinct tracks** that crossed the threshold
                at any point in the window -- "how many people loitered this minute" -- read from a
                :attr:`Lifetime.WINDOW` key, because a per-frame scalar carries no identity.  This
                is the same set ``dwell_detection.py`` keeps as ``_loitering_alerted_tracks``, given
                a defined lifetime.
        
                ``active_count`` is a *level*, and a level has two honest window readings, so it gets
                two names: ``active_count`` is the count on the window's **last** frame (what
                ``agg_type: last`` means) and ``active_count_peak`` is the **peak concurrent** count
                (what ``agg_type: max`` means).  One name could only carry one of them, because a
                :class:`WindowOutput` is published verbatim -- the runtime does not re-apply
                ``agg_type`` to a registered primitive -- so a manifest asking for the other reading
                silently got this one.
        
                **The gauge keeps its own two names, next to the identity count.**  "How many are
                loitering right now" is the headline number of ``loitering_detection`` and the live
                ``loitering_count`` wire key, and until now the window had no name for it: the gauge is
                computed every frame and ``over_threshold_count`` at window scope answers a different
                question.  So the identity count is left exactly as it was -- renaming it would silently
                change ``illegal_parking``'s ``total_violations``, which is *distinct crossers* and
                correct -- and the two gauge readings are published **alongside** it:
        
                ========================== ================================================================
                ``over_threshold_count``      distinct tracks that crossed the threshold this window
                ``over_threshold_count_last`` how many were over it on the window's **last** frame
                ``over_threshold_count_peak`` the most that were over it **at once**
                ========================== ================================================================
        
                The ``_last`` suffix is explicit rather than implied because the un-suffixed name is
                already taken by the identity count.  That is the one place this stage departs from the
                engine's ``<name>`` / ``<name>_peak`` convention (``active_count`` /
                ``active_count_peak``), and it departs deliberately: the convention assumes the bare
                name is the level, and here it is not.  All three are different numbers -- one loiterer
                who leaves and one who arrives is ``2`` distinct, ``1`` last and ``1`` peak -- and
                ``agg_type`` cannot derive any of them from another, because a :class:`WindowOutput` is
                published verbatim.
        
                ``max_seconds`` is the longest session seen, and ``avg_seconds`` averages the frames
                that had anyone in them -- averaging in the empty frames would make a busy minute
                with a quiet start read lower than a uniformly quieter one.
        
                Args:
                    frames: This stage's outputs for the window, in frame order.
        
                Returns:
                    The seven readings above, or an **empty** :class:`WindowOutput` in the
                    ``unassigned`` bucket (:attr:`_measures_nothing`) -- the published rows are built
                    from this, so an empty one is what removes them rather than sending ``0``.
        """
        ...


# From dwell
class DwellGateError:
    # A ``dwell`` stage is configured against something the pipeline cannot supply.
    #
    #     Raised for the three cases that would otherwise present as "the dwell metric is always
    #     zero", which is indistinguishable from a genuinely empty scene (``09`` §3):
    #
    #     * ``state: in_zone`` on a pipeline that has **no zones at all**;
    #     * a ``gate:`` naming a stage that is not in the pipeline, or is not *before* this one;
    #     * ``state: stationary`` with no ``velocity_state`` stage and no explicit gate.
    #
    #     Not raised for ``state: in_zone`` in the ``global`` bucket of a *zoned* app: a zoned app
    #     always runs that bucket as well, so raising there killed every session that combined
    #     ``state: in_zone`` with zones -- the combination the setting exists for.  See
    #     :meth:`Dwell._state_verdict`.

    ...

# From geometry
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

# From geometry
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


# From geometry
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


# From geometry
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


# From geometry
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


# From incident_quantise
class IncidentQuantise:
    # ``incident_quantise`` -- magnitude in, severity out.
    #
    #     Outputs (:attr:`PrimitiveOutput.values`):
    #
    #     ``level``
    #         The severity name this frame's magnitude reaches, or :data:`NO_LEVEL`.
    #     ``level_rank``
    #         :func:`level_rank` of it -- ``0`` for none, ``5`` for critical.  Publish this, not
    #         ``level``, to a numeric metric: ``metrics[].data`` is a number and a numeric
    #         *string* is rejected outright (contract Section 1 rule 6).
    #     ``area``
    #         Summed bounding-box area of the quantised detections, as a **fraction of the
    #         frame** (boxes are normalized 0-1, contract Section 4) -- unless
    #         :attr:`~matrice_analytics.engine.manifest.models.IncidentQuantiseConfig.area_source` is
    #         set, in which case this is that stage's ``area_ratio`` (true mask coverage) instead.
    #     ``confidence``
    #         Highest detection confidence, ``0-1``.
    #
    #     Raises one :class:`~matrice_analytics.engine.primitives.base.PrimitiveEvent` per frame
    #     while the magnitude reaches a rung, and none at :data:`NO_LEVEL`.  An empty frame is
    #     never an incident: with no detections the strategies would all quantise to ``0``, and a
    #     ladder with a ``percentage: 0`` rung would then report that rung forever on a camera
    #     watching an empty room.
    #
    #     Note:
    #         The event's ``kind`` is this **stage's name**, not an ``incidents.types[].key``.
    #         :class:`~matrice_analytics.engine.manifest.models.IncidentQuantiseConfig` carries no
    #         incident key -- the manifest joins the two the other way round, with
    #         ``incidents.types[].severity_from: <stage name>`` (``models.py:1891-1903``) -- so
    #         the stage name is the only identifier this primitive has, and the runtime resolves
    #         the incident type from it.

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Construct from a validated config and an already-scoped state store.
        
                Args:
                    config: The stage's config, validated by the manifest loader.
                    state: A store scoped to ``<camera_id>/<app_id>/<zone>/<stage>`` (``09`` §4).
        
                Raises:
                    ValueError: ``strategy: area_ratio`` with a ``threshold_area`` above ``1.0``.
                        See :meth:`_quant_area_ratio` -- a pixel² threshold against normalized
                        boxes quantises every frame to the bottom of the ladder, and a fire app
                        that reports ``low`` during a fire is worse than one that refuses to start.
        """
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Quantise this zone's detections for one frame.
        
                Args:
                    ctx: The frame's detections, already entity-remapped and zone-assigned.
        
                Returns:
                    The level, its rank, the measured area and the peak confidence, plus one event
                    when a rung was reached.
        
                Note:
                    Every detection in the zone is quantised.
                    :class:`~matrice_analytics.engine.manifest.models.IncidentQuantiseConfig` has no
                    ``classes:`` field, so the narrowing is the *model's* -- recipe E's
                    ``detect: {classes: [fire, smoke]}`` documents the intent but does not filter
                    what this stage sees.  On a multi-class model that matters; see the workstream
                    report.
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear the window peak at the aggregation boundary.
        
                :meth:`~matrice_analytics.engine.state.store.StateStore.end_window`, never
                ``clear()`` -- the distinction is the whole point of
                :class:`~matrice_analytics.engine.state.Lifetime` (``09`` §4 rule 2,
                **FROZEN-4**).
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Collapse the window to its worst frame.
        
                The **peak**, not the mean.  Severity is ordinal: the average of ``critical`` and
                ``none`` is not ``medium``, and publishing a ratio-shaped aggregate of an ordinal
                is the same class of mistake as summing a percentage (**PY-1**).  ``area`` and
                ``confidence`` are the maxima over the window for the same reason -- they are the
                evidence for the peak level.
        
                No events.  Every candidate was already raised by :meth:`process` at the frame it
                happened on; repeating them here would give the runtime's find-or-create two
                arrivals for one occurrence.
        
                Args:
                    frames: This stage's per-frame outputs for the window, in frame order.
        """
        ...


# From keypoint_pose
class KeypointPose:
    # Per-frame pose classification for one zone, published per track.
    #
    #     Outputs (:attr:`~.base.PrimitiveOutput.values`):
    #
    #     ``pose_state``
    #         The modal rule name across this frame's tracks, ``""`` when none matched -- the
    #         ``velocity_state.state`` convention.
    #     ``match_count``
    #         Tracks matching any published rule this frame.
    #     ``measured_count``
    #         Tracks that had usable keypoints.  **The pose-model outage signal**: a detector-only
    #         stream makes this ``0`` while ``detect`` reports a busy scene, and legacy has no
    #         equivalent -- ``fence_climbing_detection_pose`` publishes zero climbing alerts forever
    #         in that situation (``:130-131``) while its zone counting continues normally, so the app
    #         looks healthy.
    #
    #     Plus :attr:`~.base.PrimitiveOutput.tracks`, where each matching track carries
    #     ``state = <rule name>`` and ``attributes = {"torso_angle_deg": ..., "keypoints_seen": ...}``.
    #     **That per-track state is the load-bearing output**, because it is what ``dwell.gate``
    #     reads; the scalars above are for dashboards.
    #
    #     Rule resolution, stated because it is not inferable:
    #
    #     * Rules are evaluated in manifest order and the **first matching** one names the track.
    #     * A rule referenced by some ``any_of``'s ``of`` list is an **ingredient**: it is evaluated,
    #       but it never names a track and never counts towards ``match_count``.  That is what lets
    #       ``fall_detection`` publish one label ``down`` over the ``angle OR aspect`` pair instead of
    #       leaking the two helper names into ``pose_state`` and breaking ``dwell.gate``.

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Parse and validate the rule set once, at startup.
        
                Args:
                    config: The validated ``keypoint_pose:`` block.
                    state: Scoped to ``<camera_id>/<app_id>/<zone>/<stage>`` by the runtime.  Only the
                        window's last/peak readings live here; there is no per-track state, because
                        duration is ``dwell``'s and hysteresis is ``state_machine``'s.
        
                Raises:
                    ValueError: ``skeleton_type`` is not ``coco17``, or a rule is malformed.  Both are
                        startup refusals (``09`` §5): a pose rule that cannot be evaluated must not
                        become a stage that matches nothing.
        """
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Classify every tracked object in this zone, for this frame.
        
                Args:
                    ctx: The frame.  ``det.keypoints`` are normalized 0-1 (the runtime does that at
                        intake) and ``det.track_id`` is stamped by the tracker stage.
        
                Returns:
                    The three values plus one :class:`~.base.TrackState` per evaluated track.  Never
                    any events: a pose is a state, and turning a state into an incident is
                    ``state_machine`` plus the manifest (**O1**).
        
                Raises:
                    TrackingRequiredError: No tracker ran, or its ids never reached the detections.
                        Per-track state is this primitive's output, so an untracked pipeline would
                        publish an empty ``tracks`` map forever.
                    PrimitiveValueError: ``on_missing_keypoints: error`` and a detection carries none;
                        or a ``bbox_aspect_gt`` rule is configured on a stream with no resolution.
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear the window readings at the aggregation boundary.
        
                ``end_window()``, not ``clear()``: there is no cumulative total here today, and
                reaching for the full reset is the habit that erases one somewhere else (``09`` §4
                rule 2, **FROZEN-4**).
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Collapse the window.  ``match_count`` is a level, so it gets **two** names (**PY-1**).
        
                ``match_count`` is the count on the window's **last** frame and ``match_count_peak`` is
                the **peak concurrent** count; a ``WindowOutput`` is published verbatim, so one name
                could only answer one of those and would answer the other wrongly, in silence.
                ``pose_state`` is the pose the zone spent the most frames in -- the same reading
                ``velocity_state.window`` publishes for its ``state``.
        
                Args:
                    frames: This stage's per-frame outputs for the window, in frame order.  Read for
                        the modal pose; the counts come from the store, which is unaffected by the
                        frame-retention cap in ``runtime/window.py``.
        """
        ...


# From keypoint_pose
class PoseRule:
    # One named pose predicate, parsed and validated from a manifest ``rules[]`` entry.
    #
    #     A frozen dataclass in this module rather than a Pydantic model in ``manifest/models.py``
    #     only because the config model still declares ``rules: list[dict[str, Any]]``; the field set
    #     below is what that model should carry (see the port report).  :meth:`parse` accepts either
    #     the raw mapping or an already-typed object, so nothing here changes when it does.

    def parse(cls: Any, raw: Any, index: int, known: Any[str]) -> 'Any':
        """
        Validate one manifest rule entry.
        
                Args:
                    raw: The mapping from ``rules[]``, or any object carrying the same attributes.
                    index: Its position in ``rules``, for the error message -- an unnamed rule cannot
                        be pointed at any other way.
                    known: Names of the rules already parsed, which is what an ``any_of`` may reference.
        
                Returns:
                    The validated rule.
        
                Raises:
                    ValueError: The entry is not a mapping, names no ``test``, names an unknown one, is
                        missing the field its test needs, references an unknown joint, or forward-
                        references a rule.  Every one of these is a manifest error and every one of
                        them is silent in the legacy tree, where ``rules`` is untyped.
        """
        ...


# From line_crossing
class LineCrossing:
    # Count directional crossings, ``in`` / ``out`` / ``net``.
    #
    #     Two methods, selected by ``LineCrossingConfig.method``:
    #
    #     ``abline``
    #         A trap zone between **exactly two** lines.  A track counts only on a *full*
    #         traversal -- ``A -> zone -> B`` or ``B -> zone -> A`` -- so loitering on the
    #         threshold does not ratchet the counter.  ``in_direction`` says which traversal is
    #         ``in``.
    #     ``polygon``
    #         **Exactly one** zone, with an inner band auto-inset by ``inset_px`` (default
    #         :data:`~matrice_analytics.engine.primitives.geometry.DEFAULT_INSET_PX`).  The band
    #         between the outer boundary and the inner one is hysteresis: a track jittering on the
    #         boundary sits in the band and changes nothing.  Entering the inner polygon is ``in``
    #         under ``A_to_B`` and ``out`` under ``B_to_A``.
    #
    #     Per-frame ``values``:
    #
    #     ``in`` / ``out``
    #         Crossings completed **this frame** -- the increments, not the totals, so a metric
    #         with ``agg_type: sum`` adds up to the window's traffic.  This mirrors
    #         ``ABLineCounter.new_in`` / ``new_out``.
    #     ``net``
    #         ``in - out`` for this frame.
    #     ``total_in`` / ``total_out`` / ``total_net``
    #         Cumulative since process start (**FROZEN-4**).
    #     ``present``
    #         How many tracks are currently inside.
    #     ``untracked``
    #         Detections in this frame with no ``track_id``.  They cannot be counted, so the loss
    #         is published rather than dropped (**PY-10** in spirit).

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Resolve and **validate** the geometry now.
        
                Args:
                    config: The validated ``line_crossing`` stage config.
                    state: A store already scoped to ``<camera_id>/<app_id>/<zone>/<stage>``.
                    geometry: The camera's resolved geometry, built **once per camera** by the runtime
                        (``SceneGeometry.from_stream_info(stream_info)``, or
                        ``SceneGeometry.from_context(ctx)`` through the standard channel) and injected
                        here; when omitted it is read from
                        :data:`~matrice_analytics.engine.primitives.geometry.GEOMETRY_STATE_KEY`.
                        Construction-time rather than per-frame because every check below is a setup
                        check, and because ``polygon``'s inset runs an O(n^2) clearance sweep -- see
                        :func:`~matrice_analytics.engine.primitives.geometry.resolve_geometry`.
                    track_stage: The name of the upstream ``track`` stage in ``ctx.previous``.
                        Defaults to discovery by
                        :func:`~.velocity_state.tracker_stage`.  Needed only when a manifest runs two
                        trackers and this counter must follow a particular one.
        
                Raises:
                    GeometryError: ``method: abline`` and the camera does not have exactly 2 lines;
                        or ``method: polygon`` and it does not have exactly 1 zone; or there is no
                        geometry at all; or the resolution is missing (contract Section 5); or
                        ``inset_px`` collapses the zone.  All of these are silent zero-forever
                        failures in the legacy path.
        """
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Advance the counter by one frame.
        
                Args:
                    ctx: The frame.  Track ids come from ``ctx.detections[].track_id``, stamped by
                        the runtime from the tracker stage; the *presence* of an upstream ``track``
                        stage is verified against ``ctx.previous`` so a mis-ordered pipeline fails
                        instead of counting zero.
        
                Returns:
                    ``in``, ``out``, ``net`` for this frame, plus the cumulative totals.
        
                Raises:
                    ValueError: Detections with no track ids, and either no upstream ``track`` stage
                        or one whose ids never reached the detections -- see :meth:`_no_ids`.
                        ``LineCrossingConfig.REQUIRES = ("track",)`` means the manifest loader
                        should already have caught the first; a crossing counter without ids counts
                        nothing forever.
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear the window deltas; keep the totals and the per-track state.
        
                ``09`` §4 rule 2.  Clearing ``regions`` here would make every track look new on the
                first frame of every window, so a person mid-traversal at the boundary would never
                be counted -- a per-window undercount that no test of a single window can see.
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Collapse the window: crossings **sum**, totals carry over.
        
                A crossing is an event, so summing it over the window is the correct collapse -- the
                opposite of ``zone_occupancy``, where a headcount must not be summed (**PY-1**).
                The window deltas come from :attr:`~matrice_analytics.engine.state.Lifetime.WINDOW`
                keys, which :meth:`reset` clears; the totals come from ``PERSISTENT`` keys, which it
                does not (**FROZEN-4**).  ``frames`` would give the same answer and is accepted for
                protocol conformance; the store is the single source of truth.
        
                Nothing here needs a second name for a second reading: ``in``/``out``/``net``/
                ``untracked`` are event counts whose only collapse is the sum, and ``total_*`` are
                cumulative levels whose only collapse is their current value.  ``present`` is
                deliberately **not** published here -- it is an instantaneous level with no single right
                collapse, so it stays a per-frame sample and the runtime applies the metric's own
                ``agg_type`` to it (``last`` for "how many are inside", ``max`` for the busiest moment).
                That is the one place ``agg_type`` is load-bearing against a registered primitive, and it
                works precisely *because* this method stays quiet about the name.
        """
        ...


# From ratio_compliance
class RatioCompliance:
    # ``ratio_compliance`` -- fraction of ``subject`` detections satisfying the rule.
    #
    #     A subject is **compliant** when every entity in ``required`` is associated to it *and*
    #     no entity in ``violations`` is.  With ``required: []`` (recipe F -- a product is fine
    #     unless a defect is found on it) the first clause is vacuously true, which is why the
    #     manifest insists at least one of the two lists is non-empty: with both empty every
    #     subject is trivially compliant and the app publishes a constant 100.
    #
    #     Outputs (:attr:`PrimitiveOutput.values`), all resolvable as
    #     ``<stage>.<name>``:
    #
    #     ``subject_count``
    #         Subject detections in this zone, this frame.
    #     ``compliant_count``
    #         Subjects satisfying the rule.
    #     ``violation_count``
    #         ``subject_count - compliant_count``, **plus** orphan violation-class detections --
    #         violation boxes that belong to no subject.  Single-stage PPE models emit
    #         ``no_hardhat`` without a ``person`` box at all, and the legacy processor counted
    #         those directly (``safety.py:154-177``); dropping them would silently under-report
    #         the exact thing the app exists to find.
    #     ``compliance_pct``
    #         ``compliant_count / subject_count * 100``.
    #     ``violation_pct``
    #         ``100 - compliance_pct``.  The one output ``08`` §2 forgot; ``FIELD_REFERENCE``
    #         recipe F sources it as ``defect_rate``.
    #     ``<attr>_count``
    #         One per entity in ``required + violations``: how many of that entity were detected
    #         in this zone this frame.  The name is the raw entity name, un-sanitised, because
    #         that is what
    #         :meth:`~matrice_analytics.engine.manifest.models.RatioComplianceConfig.output_names`
    #         declares and therefore what a ``metrics[].source`` can name.
    #
    #     With **no subjects in frame** both percentages are ``0.0``, not ``100``/``0`` and not
    #     ``0``/``100``.  Nothing was assessed, so neither reading is true, and the pair is
    #     deliberately not complementary in that one degenerate case: publishing
    #     ``violation_pct: 100`` for an empty conveyor would make recipe F's ``defect_rate``
    #     read 100% every night, and publishing ``compliance_pct: 100`` for a dead camera would
    #     hide an outage behind a perfect score.  ``subject_count`` is what distinguishes
    #     "assessed and fine" from "nothing to assess" -- read it alongside.

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Construct from a validated config and an already-scoped state store.
        
                Args:
                    config: The stage's config, validated by the manifest loader.
                    state: A store scoped to ``<camera_id>/<app_id>/<zone>/<stage>`` (``09`` §4).
        
                Raises:
                    ValueError: ``required`` and ``violations`` are both empty.  The manifest model
                        rejects this too, but a config built with ``model_construct`` skips
                        validators, and a silently-100% compliance app is worse than a loud
                        constructor.
        """
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Assess this zone's subjects for one frame.
        
                Args:
                    ctx: The frame's detections, already entity-remapped and zone-assigned.
        
                Returns:
                    The compliance values for this frame.  Never any events -- compliance becomes
                    an incident through a manifest threshold on ``violation_count``, which is the
                    runtime's decision, not this primitive's (**O1**).
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear the window accumulators at the aggregation boundary.
        
                :meth:`~matrice_analytics.engine.state.store.StateStore.end_window`, not
                ``clear()``: this stage keeps no cumulative total, but calling the full reset here
                is the habit that erases one somewhere else (``09`` §4 rule 2, **FROZEN-4**).
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Collapse the window into the two values ``agg_type`` cannot recover.
        
                Only the percentages.  A ratio is not summable and it is not the mean of the
                window's totals either -- publishing one as a 60-second ``sum`` is **PY-1** -- so
                the frame-mean is computed here, over the frames that had a subject.
        
                The counts are deliberately *not* republished: they are honest per-frame samples,
                and ``metrics[].agg_type`` collapses them correctly without help.  Emitting a
                second, differently-derived ``violation_count`` here would give the runtime two
                answers to one question.
        
                Args:
                    frames: This stage's per-frame outputs for the window, in frame order.  Unused
                        -- the accumulators in the state store are the same data, already folded,
                        and survive a runtime that hands back an empty list.
        """
        ...


# From segmentation_area
class MaskMeasurement:
    # One detection's mask, measured.
    #
    #     A named triple rather than three parallel lists, because the three travel together and
    #     :attr:`measured` is what separates "0 % coverage" from "no mask at all" -- exactly the
    #     distinction legacy loses when Tier 3 substitutes the bounding box.

    ...

# From segmentation_area
class SegmentationArea:
    # Mask coverage for one zone, one frame -- as a fraction, never a percent.
    #
    #     Outputs (:attr:`~.base.PrimitiveOutput.values`), each resolvable as ``<stage>.<name>``:
    #
    #     ``area_ratio``
    #         The reduced coverage, ``0-1``.  ``max`` of the instances by default, ``sum`` when
    #         ``reduce: sum`` reproduces ``landslide_detection``'s total.  Clamped to ``1.0``
    #         unless ``clamp: false``.
    #     ``max_area_ratio``
    #         The largest single instance, whatever ``reduce`` is.  Legacy publishes both
    #         (``max_landslide_area_pct`` ``:1337``, ``total_landslide_area_pct`` ``:1338``) and an
    #         operator reads them differently: one answers "how big is the biggest slide", the
    #         other "how much ground is moving".
    #     ``instance_count``
    #         Detections of ``classes`` in this zone this frame.
    #     ``measured_count``
    #         How many of them carried a real mask.  **``measured_count < instance_count`` is the
    #         mask-outage signal**, and it exists because legacy's silent bounding-box proxy has
    #         none: a dead mask stage there publishes plausible coverage forever.
    #     ``area_px``
    #         The reduced foreground pixel count in the masks' own space -- a **diagnostic**, not a
    #         metric.  It is resolution-dependent by construction and only comparable when every
    #         mask in the frame shares one ``size``; ``area_ratio`` is the number a manifest should
    #         threshold on.  It is published because the config model declares it today (see the
    #         schema corrections in this module's port report).
    #
    #     At window scope (:meth:`window`) ``area_ratio`` is the **last** frame's coverage and
    #     ``area_ratio_peak`` is the window's high-water mark, because a ``WindowOutput`` is
    #     published verbatim and one name cannot answer both (**PY-1**).
    #
    #     Not here, on purpose: severity (that is ``incident_quantise`` or a manifest
    #     ``severity_from``), smoothing (``state_machine``), cooldown (the incident lifecycle), and
    #     ``flood_detection``'s *filter* semantics -- a primitive cannot remove a detection from the
    #     frame the next stage sees, and one that could would be action at a distance.  See the port
    #     report for that fidelity limit.

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Bind a validated config to a state store already scoped to this stage.
        
                Args:
                    config: The validated ``segmentation_area:`` block.
                    state: Scoped to ``<camera_id>/<app_id>/<zone>/<stage>`` by the runtime.  The
                        window peak lives here rather than in an instance attribute (``09`` §4 rule 1,
                        **D6**), which is also why ``__slots__`` leaves no room for one.
        
                Raises:
                    ValueError: ``normalize: none`` -- see the message.  Refused at construction, so
                        it is a startup failure (``09`` §5) rather than a metric nobody can use.
        """
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Measure this zone's masks for one frame.
        
                Args:
                    ctx: The frame.  Only ``detections`` are read -- there is no clock call and no
                        :meth:`~.base.FrameContext.require_resolution`, because the masks carry their
                        own denominator.
        
                Returns:
                    The five values above.  Never any events: coverage becomes an incident through a
                    manifest threshold, which is the runtime's decision (**O1**).
        
                Raises:
                    PrimitiveValueError: A detection of ``classes`` carries no usable mask and
                        ``on_missing_mask`` is ``error`` (the default), or a mask is malformed.  A
                        mask-free frame on a segmentation app is a broken deployment, and a
                        bounding-box proxy for it is plausible and wrong.
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear the window accumulators at the aggregation boundary.
        
                :meth:`~matrice_analytics.engine.state.store.StateStore.end_window`, not ``clear()``:
                this stage keeps no cumulative total today, and reaching for the full reset is the
                habit that erases one somewhere else (``09`` §4 rule 2, **FROZEN-4**).
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Collapse the window.  ``area_ratio`` is a level, so it gets **two** names (**PY-1**).
        
                ``area_ratio`` here is the coverage on the window's **last** frame and
                ``area_ratio_peak`` is the window's **maximum**.  A ``WindowOutput`` is published
                verbatim -- the runtime does not re-apply ``metrics[].agg_type`` to a registered
                primitive -- so a single name would answer one of those questions and answer the other
                one wrongly, in silence.  ``max_area_ratio`` at window scope is the largest single
                instance seen **anywhere in the window**, which is the only reading of a per-frame
                maximum that an operator asks for.
        
                Args:
                    frames: This stage's per-frame outputs for the window, in frame order.  Unused:
                        the accumulators in the state store hold the same data already folded, and
                        they survive a window whose retained frames were capped
                        (``runtime/window.py`` truncates at ``max_frames``, which would silently
                        lower a peak computed from this list).
        
                Returns:
                    The five window keys, or an empty output for a window with no frames -- an empty
                    aggregation is not a coverage of zero.
        """
        ...


# From state_machine
class StateMachine:
    # N-of-M confirmation with asymmetric recovery, for one zone.
    #
    #     Publishes exactly the four values
    #     :attr:`~matrice_analytics.engine.manifest.models.StateMachineConfig.STATIC_OUTPUTS`
    #     declares:
    #
    #     ==================== ==============================================================
    #     ``state``            :data:`IDLE` / :data:`PENDING` / :data:`CONFIRMED` / :data:`RECOVERING`.
    #     ``active``           ``1`` while confirmed, including through recovery.  ``0`` otherwise.
    #     ``confirmed_frames`` The current evidence counter, capped at ``confirm_frames``.
    #     ``confirmed_new``    ``1`` on the frame the machine newly reaches CONFIRMED, else ``0``.
    #     ==================== ==============================================================
    #
    #     :meth:`window` publishes those four plus ``confirmed_frames_peak``, so the counter's
    #     current value and its window high-water mark have separate names rather than depending on a
    #     ``metrics[].agg_type`` the runtime deliberately does not apply. ``confirmed_new`` at window
    #     scope is the *count* of confirm transitions this window (summed, like ``unique_count.new``),
    #     not a 0/1 flag -- see the field's note on
    #     :attr:`~matrice_analytics.engine.manifest.models.StateMachineConfig.STATIC_WINDOW_OUTPUTS`
    #     for why this is the primitive an episode-counting app should reach for when there is no
    #     object identity to run ``unique_count`` against.
    #
    #     The counter is asymmetric by design:
    #
    #     * **rise** -- ``+1`` per frame the condition holds, capped at ``confirm_frames``.
    #     * **soft decay** (default) -- ``-1`` per clear frame while still unconfirmed.  One
    #       dropped frame must not discard four frames of evidence.
    #     * **hard decay** -- back to ``0`` on the first clear frame.  For conditions where a
    #       single gap genuinely invalidates the evidence.
    #     * **recovery** -- once confirmed, the counter stops mattering; ``recovery_frames``
    #       *consecutive* clear frames drop it.  Any frame in which the condition holds resets
    #       that countdown.
    #
    #     Example:
    #         With ``confirm_frames: 5, recovery_frames: 3, decay: soft`` and a condition that
    #         holds for frames 1-4, misses frame 5, then holds for 6-7::
    #
    #             frame  1  2  3  4  5  6  7
    #             hits   1  2  3  4  3  4  5
    #             active 0  0  0  0  0  0  1
    #
    #         With ``decay: hard`` the same sequence never confirms: frame 5 resets to 0.

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Bind a validated config to a state store already scoped to this stage.
        
                Args:
                    config: The validated ``state_machine:`` block.  ``confirm_frames`` is taken
                        **as written** -- see the PY-11 note in the module docstring.
                    state: Scoped to ``<camera_id>/<app_id>/<zone>/<stage>`` by the runtime.
        """
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Advance the machine by one frame.
        
                Args:
                    ctx: This frame, in this zone.  The condition is
                        ``len(ctx.detections) > 0`` -- whatever the stages before this one left in
                        the zone.
        
                Returns:
                    The three declared values, plus a :class:`~.base.TrackState` per tracked object
                    carrying that object's own counter and state.
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear window-scoped state only (``09`` §4 rule 2).
        
                ``hits``, ``clear_run``, ``confirmed`` and ``track_counters`` are
                :attr:`Lifetime.PERSISTENT` and survive.  A state confirmed at second 59 is still
                confirmed at second 61; re-qualifying from scratch every minute would make
                ``confirm_frames`` mean "per window", which no manifest says.
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Collapse the window.  ``active`` changes meaning here (**PY-1**).
        
                Per frame ``active`` is "is it held right now"; summing it over a window publishes a
                frame count as if it were a state.  At window scope it is ``1`` when the state was
                held at **any** point -- "did this happen in this minute", which is the question the
                60-second row answers.
        
                ``confirmed_frames`` is the evidence counter, a level, so it gets two window names:
                ``confirmed_frames`` is where the counter **stands** at the boundary (``agg_type:
                last``) and ``confirmed_frames_peak`` is the window's **highest** value (``agg_type:
                max``), from a :attr:`Lifetime.WINDOW` key.  A :class:`WindowOutput` is published
                verbatim, so one name would answer only one of the two and silently mis-answer the
                other.  ``state`` is the state the window *ended* in, so the next window's
                ``idle``-to-``confirmed`` transition is readable in sequence.
        
                Args:
                    frames: This stage's outputs for the window, in frame order.
        """
        ...


# From track
class Track:
    # ID association for one zone, with the method chosen by the manifest.
    #
    #     Publishes ``active_tracks`` into :attr:`PrimitiveOutput.values` and one
    #     :class:`TrackState` per emitted track into :attr:`PrimitiveOutput.tracks`.  The
    #     ``tracks`` mapping is the contract with downstream stages: ``unique_count``, ``dwell``
    #     and ``velocity_state`` read it rather than re-implementing tracking, which is the
    #     duplication this primitive exists to end.
    #
    #     Each :class:`TrackState` carries ``score`` and ``det_index`` in
    #     :attr:`TrackState.attributes`.  ``det_index`` indexes
    #     :attr:`FrameContext.detections`, so a later stage can reach the detection's box without
    #     this primitive mutating the frame's detection tuple -- primitives do not write to what
    #     the next stage is about to read (``base.FrameContext``).
    #
    #     Example:
    #         >>> from matrice_analytics.engine.state import InMemoryStateStore
    #         >>> state = InMemoryStateStore().for_primitive("cam-1", "footfall", "global", "track")
    #         >>> stage = Track(TrackConfig(method="bytetrack"), state)
    #         >>> out = stage.process(ctx)                       # doctest: +SKIP
    #         >>> sorted(out.tracks)                             # doctest: +SKIP
    #         [1, 2]

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Bind a validated config and an already-scoped state store.
        
                Args:
                    config: The stage's validated :class:`TrackConfig`.  Unlike
                        ``engine_session.py:483``, every knob here came from a manifest.
                    state: A store scoped to ``<camera_id>/<app_id>/<zone>/<primitive>``.
        
                Note:
                    The track-id namespace is
                    :func:`~matrice_analytics.engine.state.store.stable_namespace` over
                    :attr:`~matrice_analytics.engine.state.store.StateStore.prefix` -- the store's own
                    scope, and **never** ``hash()`` (**PY-9**).  The prefix already encodes camera,
                    app, zone and stage, so two cameras cannot collide and the same camera gets the
                    same namespace in every process, forever.  It is read off the protocol rather
                    than through a ``getattr``: scope identity is part of the ``StateStore``
                    contract, so a store that cannot answer is a broken store, not a fallback case.
                    An unscoped root store answers ``""``, which is no identity at all; the stage
                    name stands in there, and is stable for the same reason.
        """
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Associate this frame's detections with the running tracks.
        
                Args:
                    ctx: One frame in one zone.  Boxes are read in the contract's normalized 0-1
                        space and never converted to pixels, so this stage needs no resolution and
                        cannot make the 1920x mistake (**PY-7**).
        
                Returns:
                    ``active_tracks`` and the per-track :class:`TrackState` mapping.
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear the window peak -- and emphatically **not** the tracker.
        
                ``09`` §4 rule 2.  :meth:`StateStore.end_window` drops the
                :attr:`Lifetime.WINDOW` peak and leaves the
                :attr:`Lifetime.PERSISTENT` tracker blob untouched.  Clearing the tracker here
                would hand every object in frame a brand-new id once a minute; ``unique_count``
                would then count the same person 60 times an hour and the footfall graph would show
                a spike on every window boundary.  That is the single most expensive way to get
                ``reset()`` wrong, and it is why the lifetime is declared at write time rather than
                inferred from which method is clearing what.
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Report the window's simultaneous track count, **both** readings, under two names.
        
                A sum would publish "1,500 tracks" for one person standing still for a minute
                (**PY-1**); the *distinct* count over the window is ``unique_count``'s job, not this
                one's.  What is left is a level, and a level has two honest window readings:
        
                ``active_tracks``
                    How many were being tracked on the window's **last** frame -- ``agg_type: last``.
                ``active_tracks_peak``
                    How many at once at the **busiest** moment -- ``agg_type: max``.
        
                Both are published because a :class:`WindowOutput` is published verbatim: the runtime
                does not re-apply ``agg_type`` to a registered primitive, so one name could only ever
                carry one of the two numbers, and a manifest asking for the other got this one silently.
        
                Args:
                    frames: This stage's per-frame outputs, in frame order.  Folded into the peak so it
                        is right either way; the last reading comes from the store, because the
                        runtime caps retention and ``frames[-1]`` is then not the window's last frame.
        """
        ...


# From unique_count
class UniqueCount:
    # Distinct-object counting for one zone, deduplicated by tracker id.
    #
    #     Publishes, into :attr:`PrimitiveOutput.values`:
    #
    #     ``new``
    #         Ids seen for the first time *on this frame*.  A per-frame sample, so
    #         ``metrics[].agg_type: sum`` over a window reproduces the window figure exactly --
    #         the per-frame values are disjoint by construction.
    #
    #     ``new_in_window``
    #         The running count of first-ever-seen ids **so far this window** -- the same
    #         WINDOW-lifetime counter :meth:`window` reads at the boundary, read one frame
    #         earlier.  A metric wanting a live arrivals-so-far total sources this with
    #         ``agg_type: last``, rather than summing ``new`` per frame and getting the right
    #         answer only once the window has actually closed.
    #
    #     ``total``
    #         Distinct ids since process start (**FROZEN-4**).  A level, not an event: aggregate
    #         it with ``max`` or ``last``, never ``sum``.
    #
    #     ``per_category.<entity>``
    #         The same cumulative total, split by entity, one key per
    #         :attr:`UniqueCountConfig.categories` entry.  These sum to ``total``, because the
    #         dedup key is ``(entity, track_id)`` and not the bare id -- a tracker is free to
    #         reuse an id across classes, and a per-category breakdown that does not add up is
    #         worse than none.
    #
    #         These are also the **only** input to ``results-agg``'s ``current_counts``,
    #         ``current_new_counts`` and ``total_counts``
    #         (:class:`~matrice_analytics.engine.runtime.window.ZoneCounters` differences them
    #         across the window boundary to get arrivals), so an entity missing from
    #         :attr:`UniqueCountConfig.categories` is an entity with no volume series -- even if
    #         ``detect`` counts it every frame.
    #
    #     Requires a ``track`` stage earlier in the pipeline
    #     (:attr:`UniqueCountConfig.REQUIRES`); it reads that stage's
    #     :attr:`PrimitiveOutput.tracks`.
    #
    #     Example:
    #         >>> from matrice_analytics.engine.state import InMemoryStateStore
    #         >>> state = InMemoryStateStore().for_primitive("cam-1", "footfall", "global", "unique_count")
    #         >>> stage = UniqueCount(UniqueCountConfig(categories=["person"]), state)
    #         >>> stage.process(ctx).values["total"]              # doctest: +SKIP
    #         1

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Bind a validated config and an already-scoped state store.
        
                Args:
                    config: The stage's validated :class:`UniqueCountConfig`.
                    state: A store scoped to ``<camera_id>/<app_id>/<zone>/<primitive>``
                        (``09`` §4).  The seen-id sets live here and nowhere else (**D6**); a
                        ``self._seen`` set would be invisible to the state layer, to
                        :meth:`StateStore.end_window` and to any future durable backing.
        
                Note:
                    ``config.by`` is ``Literal["track_id"]`` -- one strategy, checked at manifest
                    load.  It is read rather than ignored so that adding a second strategy later is
                    a change here and not a silent no-op.
        """
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Fold this frame's track ids into the cumulative sets.
        
                Args:
                    ctx: One frame in one zone.  Track ids come from an upstream ``track`` stage's
                        :attr:`PrimitiveOutput.tracks` when there is one, and from
                        ``detection.track_id`` otherwise -- never both, because a tracker that
                        renumbered the ids would otherwise have every object counted twice.
        
                Returns:
                    ``new`` for this frame, plus the cumulative ``total`` and per-category
                    breakdown.
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear ``new`` at the aggregation boundary; keep ``total`` (**FROZEN-4**).
        
                One call does both, because the lifetime was declared at write time:
                :meth:`StateStore.end_window` drops ``new_in_window`` and cannot touch the seen-id
                sets.  That is the point of the enum -- ``09`` §4 rule 2 notes that today the
                distinction is implicit in *which method clears which field*
                (``base_processor.py:126-131,182``), and that getting it backwards is the most
                common bug in custom code.  Here getting it backwards is not expressible.
        
                Clearing the totals here would reset the cumulative series to zero every 60
                seconds, and the backend's rollup would read each reset as a genuine restart.
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Publish the window's ``new`` and the running ``total``.
        
                ``new`` is read from the WINDOW-lifetime counter rather than summed from ``frames``.
                The two are equal -- each frame's ``new`` counts ids nothing had seen before, so the
                per-frame values are disjoint -- but the counter is the one that is still correct
                when the runtime does not retain 1,500 per-frame outputs, and it is the value
                :meth:`reset` is about to clear.
        
                Args:
                    frames: This stage's per-frame outputs, in frame order.  Accepted for the
                        protocol; the store is authoritative.
        
                Returns:
                    ``new`` for the closing window and the cumulative ``total`` (**FROZEN-4**).
        """
        ...


# From velocity_state
class TrackingRequiredError:
    # A temporal primitive ran without usable track ids.
    #
    #     ``dwell`` and ``velocity_state`` both declare ``REQUIRES = ("track",)``
    #     (``manifest/models.py``), so the manifest loader rejects a pipeline that omits it.  This
    #     exists for the two cases the loader cannot see:
    #
    #     * no tracker in the pipeline at all *and* no caller-supplied ids -- the pipeline was
    #       built by something other than the loader;
    #     * a tracker that **did** associate objects this frame whose ids never reached
    #       ``det.track_id``.  That is a broken runtime, not a quiet camera: the runtime owns
    #       :attr:`~.base.PipelineDetection.track_id` and stamps it from the tracker stage's
    #       :attr:`~.base.PrimitiveOutput.tracks` (``runtime/session.py``).  It used to be
    #       swallowed, and three primitives published zeros for the life of the process.

    ...

# From velocity_state
class VelocityState:
    # Per-track speed, motion class, heading and wrong-way flag for one zone.
    #
    #     Publishes exactly the four values
    #     :attr:`~matrice_analytics.engine.manifest.models.VelocityStateConfig.STATIC_OUTPUTS`
    #     declares, and the per-track detail on :attr:`~.base.PrimitiveOutput.tracks`:
    #
    #     ==================== ==============================================================
    #     ``state``            Modal motion class across this frame's tracks, ``""`` if none.
    #     ``avg_speed``        Mean px/s over tracks that have a measurable speed.
    #     ``stationary_count`` Tracks below ``stationary_below_px_per_sec`` **this frame**.
    #     ``wrong_way_count``  Tracks moving against ``expected_heading_deg`` **this frame**.
    #     ==================== ==============================================================
    #
    #     :meth:`window` re-reads two of those at window scope, which is not the same question, and
    #     adds ``stationary_count_peak`` so that the last and peak readings of that level have
    #     separate names.  ``wrong_way_count_last`` and ``wrong_way_count_peak`` do the same for the
    #     wrong-way gauge, which the window otherwise reports only as a count of distinct tracks --
    #     see its docstring (**PY-1**).

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Bind a validated config to a state store already scoped to this stage.
        
                Args:
                    config: The validated ``velocity_state:`` block.
                    state: Scoped to ``<camera_id>/<app_id>/<zone>/<stage>`` by the runtime.  All
                        mutable state lives here; there is no instance dict (``09`` §4 rule 1,
                        enforced by ``__slots__``).
                    geometry: The camera's resolved geometry, injected by the runtime
                        (``runtime/session.py:_construct``, which inspects this constructor's
                        signature the same way it does for ``line_crossing``) when
                        :attr:`~matrice_analytics.engine.manifest.models.VelocityStateConfig.heading_from_line`
                        is set. Unused, and safe to omit, otherwise -- see :meth:`_resolve_expected`.
        
                Raises:
                    GeometryError: ``heading_from_line: true`` and the camera does not have exactly
                        one line drawn.  See :meth:`_resolve_expected`.
        """
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Measure every tracked object in this zone over the trailing window.
        
                Args:
                    ctx: This frame, in this zone.  Every timestamp used comes from
                        :attr:`~.base.FrameContext.frame_ts` (**PY-13**) and the frame size from
                        :meth:`~.base.FrameContext.require_resolution` -- the standard channel, so
                        this stage has no private one to keep in step.
        
                Returns:
                    The four declared values plus a :class:`~.base.TrackState` per track.
        
                Raises:
                    TrackingRequiredError: No tracker ran, or one ran and its ids never reached the
                        detections -- see :func:`require_track_ids`.
                    PrimitiveValueError: The stream carries no resolution, so a px/s threshold has
                        nothing to be measured against.  Deliberately not defaulted -- see the module
                        docstring.
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear window-scoped state only (``09`` §4 rule 2).
        
                ``samples`` is :attr:`Lifetime.PERSISTENT` and survives: a vehicle that has been
                stopped for fifty seconds when the window ticks is still stopped one second later,
                and re-deriving that would take another ``window_seconds`` of frames -- during which
                it would read :data:`UNKNOWN_STATE` and vanish from ``stationary_count``.
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Collapse the window.  Two of the four values change meaning here (**PY-1**).
        
                ``stationary_count`` per frame is *how many are stationary right now*; summing 1500
                frames of one stationary car reports 1500 cars, which is exactly the percentage-
                published-as-a-sum defect.  It is a level, so it gets **two** window names: the count on
                the window's **last** frame (``stationary_count``, i.e. ``agg_type: last``) and the
                **peak concurrent** count (``stationary_count_peak``, i.e. ``agg_type: max``).  A
                :class:`WindowOutput` is published verbatim -- the runtime does not re-apply
                ``agg_type`` to a registered primitive -- so a single name would answer only one of the
                two questions and answer the other one wrongly, in silence.
        
                ``wrong_way_count`` at window scope is the number of **distinct tracks** that went
                the wrong way at any point -- "how many vehicles did this", the question an operator
                asks -- taken from a :attr:`Lifetime.WINDOW` key, because a per-frame scalar cannot
                carry identity.  That identity count is unchanged: it is the right answer to the
                question it asks, and redefining it would move ``vehicle_monitoring_wrong_way``'s live
                ``current_wrong_way_count`` series underneath the dashboards built on it.
        
                This docstring used to add: *"It needs no ``_peak``: a peak of a per-frame gauge is a
                different, smaller number and nobody wants it."*  Half right.  A peak **is** a
                different number, and somebody does want it -- together with the *last* reading, which
                is what the legacy ``current_wrong_way_count`` published (``agg_type: last``, over a
                gauge).  The gauge is computed on every frame and had no window name to go out under,
                so both of its readings are now published **beside** the identity count rather than
                replacing it:
        
                ========================== ===============================================================
                ``wrong_way_count``        distinct tracks that went the wrong way this window
                ``wrong_way_count_last``   how many were doing it on the window's **last** frame
                ``wrong_way_count_peak``   the most that were doing it **at once**
                ========================== ===============================================================
        
                The ``_last`` suffix is explicit because the bare name is already the identity count --
                the same deliberate departure from the engine's ``<name>`` / ``<name>_peak`` convention
                that ``dwell.over_threshold_count`` makes, and for the same reason.  Three vehicles that
                each go the wrong way in turn read ``3`` distinct, ``1`` last, ``1`` peak; no
                ``agg_type`` can derive one from another, because this output is published verbatim.
        
                Args:
                    frames: This stage's outputs for the window, in frame order.
        
                Returns:
                    The four keys plus ``stationary_count_peak``, ``wrong_way_count_last`` and
                    ``wrong_way_count_peak``, at window scope.
        """
        ...


# From zone_occupancy
class ZoneOccupancy:
    # Count detections per zone, and count the ones that fit in none.
    #
    #     Per-frame ``values``:
    #
    #     ``per_zone.<zone>.count``
    #         Detections whose reference point is inside that zone, this frame.  Keyed by
    #         :func:`~matrice_analytics.engine.primitives.geometry.zone_identity`, **not** by the
    #         raw drawn name: a dot in the name would break the key it is spliced into, since the
    #         manifest validates a ``zones: all`` stage's per-zone sources against
    #         ``^per_zone\.[^.]+\.count$``.  ``zone_identity`` maps it to ``_`` once, for the
    #         output key, the window key and the state accumulator alike.
    #     ``occupancy``
    #         **Distinct** detections inside at least one zone.  Under ``on_overlap: all_match``
    #         this is deliberately *less than* the sum of the per-zone counts -- occupancy counts
    #         people, the per-zone counts count memberships. On a camera with **no zones drawn
    #         at all**, there is no "at least one zone" to test: every detection counts here
    #         instead, the documented implicit global bucket (:meth:`~.geometry.SceneGeometry.empty`).
    #     ``unassigned_count``
    #         Detections inside no *drawn* zone, counted under every ``on_no_match`` policy
    #         (**PY-10**).  Always ``0`` when the camera has no zones drawn at all -- that case is
    #         ``occupancy`` in full, not a loss.
    #     ``peak_occupancy`` / ``avg_occupancy``
    #         The window's high-water mark and mean **so far** -- the same accumulators
    #         :meth:`window` reads at the boundary, read one frame earlier.  A per-frame consumer
    #         (``FrameOutcome.metric_values``, an incident's ``human_text``) gets "the peak/mean
    #         so far this window", not an absent key, which is what these two names hand back
    #         before the window closes.  Final at the boundary; live and monotonically settling
    #         before it.
    #
    #     Window ``values`` collapse those over the aggregation window, and every reading has its
    #     **own name** so no two can be confused (**PY-1**) and none of them depends on a
    #     ``metrics[].agg_type`` the runtime deliberately does not apply: ``occupancy`` and
    #     ``per_zone.<zone>.count`` hold the window's **last frame**, ``peak_occupancy`` and
    #     ``per_zone.<zone>.count_peak`` its **peak**, ``avg_occupancy`` and
    #     ``per_zone.<zone>.avg`` its **mean**, ``unassigned_count`` the window's sum,
    #     ``unassigned_total`` the loss since process start and ``frames`` how many frames the window
    #     saw.
    #
    #     Example:
    #         >>> zone_occupancy = ZoneOccupancy(config, state, geometry=geometry)  # doctest: +SKIP
    #         >>> zone_occupancy.process(ctx).values["per_zone.Polygon 1.count"]    # doctest: +SKIP
    #         3

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Resolve the geometry now, so a broken installation fails at setup.
        
                Args:
                    config: The validated ``zone_occupancy`` stage config.
                    state: A store already scoped to
                        ``<camera_id>/<app_id>/<zone>/<stage>`` by the runtime.
                    geometry: The camera's resolved geometry.  The runtime (C2) builds it **once per
                        camera** with ``SceneGeometry.from_stream_info(stream_info)`` -- or
                        ``SceneGeometry.from_context(ctx)``, the same thing through the standard
                        channel -- and injects it here; when omitted it is read from
                        :data:`~matrice_analytics.engine.primitives.geometry.GEOMETRY_STATE_KEY`.
                        It is a construction argument rather than a per-frame derivation on purpose;
                        :func:`~matrice_analytics.engine.primitives.geometry.resolve_geometry` gives
                        the two reasons.  :meth:`process` cross-checks it against ``ctx.stream`` every
                        frame, so "built once" cannot drift into "built for the wrong camera".
                    on_overlap: From the manifest's top-level ``zones:`` block
                        (``ZonesSpec.on_overlap``), which is where overlap policy lives -- it is a
                        property of the camera's geometry, not of this one stage, so it is not on
                        ``ZoneOccupancyConfig``.  Defaults to ``"first_match"``.
        
                Raises:
                    GeometryError: Geometry exists but the resolution does not (contract Section 5
                        -- zone processing must fail loudly, never silently skip); or a zone named
                        in the manifest is not drawn on this camera; or a polygon has fewer than 3
                        vertices.
                    ValueError: ``on_overlap`` is not one of :data:`OverlapPolicy`.
        """
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Assign this frame's detections to zones and publish the counts.
        
                Args:
                    ctx: The frame.  ``ctx.frame_ts`` is the only clock this primitive would ever
                        use (**PY-13**); occupancy needs no timing at all, so it uses none.
        
                Returns:
                    ``per_zone.<zone>.count`` per selected zone, plus ``occupancy`` and
                    ``unassigned_count``.
        
                Raises:
                    GeometryError: ``on_no_match`` or ``on_overlap`` is ``"error"`` and the
                        condition occurred.  Both are per-frame conditions and cannot be known at
                        setup.
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear window state at the aggregation boundary -- and nothing else.
        
                ``09`` §4 rule 2.  ``unassigned_total`` is
                :attr:`~matrice_analytics.engine.state.Lifetime.PERSISTENT` and survives, because
                the backend's rollup formula assumes a cumulative total only resets when the process
                does (**FROZEN-4**).  Calling ``state.clear()`` here is exactly the bug the two
                lifetimes exist to prevent.
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Collapse the window.
        
                The accumulators in the :class:`~matrice_analytics.engine.state.StateStore` are the
                single source of truth, not ``frames``: the store is what
                :meth:`reset` clears, so reading anything else here would let the two disagree about
                where the window boundary is.  ``frames`` would give the same answer and is accepted
                for protocol conformance.
        
                A headcount is instantaneous, so the window's collapse is never its sum -- publishing a
                percentage or a headcount as a 60-second sum is **PY-1**.  ``unassigned_count`` *is*
                summed, because a loss counter is genuinely additive.
        
                **Each reading gets its own name.**  A :class:`WindowOutput` is published verbatim: the
                runtime does not re-apply ``metrics[].agg_type`` to a registered primitive, so a name can
                only ever carry one reading and it must be obvious which.  ``occupancy`` used to hold the
                *peak* -- the same number as ``peak_occupancy``, two names for one value -- which meant a
                metric written as ``{source: zone_occupancy.occupancy, agg_type: last}`` published the
                peak and read as a current level.  Now:
        
                ``occupancy``
                    The **last** frame's headcount (``agg_type: last``).
                ``peak_occupancy``
                    The window's **high-water mark** (``agg_type: max``).
                ``avg_occupancy``
                    The **mean** over the window's frames (``agg_type: mean``).
                ``per_zone.<zone>.count`` / ``.count_peak`` / ``.avg``
                    The same three readings, per zone.
        """
        ...

    def zone_identities(self: Any) -> tuple[str, ...]:
        """
        The zone identities this stage publishes, in drawing order (**Q1** seam).
        """
        ...


from . import base, detect, dwell, geometry, incident_quantise, keypoint_pose, line_crossing, ratio_compliance, segmentation_area, state_machine, track, unique_count, velocity_state, zone_occupancy