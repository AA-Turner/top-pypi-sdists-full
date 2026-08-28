"""``line_crossing`` -- directional A/B counting over an inset band or a two-line trap zone.

Normative sources: ``_contracts/05-asis-zones-and-geometry.md`` §4 and
``clauding/STAGE_BC_PLAN.md`` §2 (B2).  Ported from
``post_processing/utils/counting_utils.py`` -- ``ABLineCounter`` (``:280``) and
``PolygonCounter`` (``:666``) -- reached through
``analytics/geometry.py:95`` (``create_counter_from_zone_config``).  The counting state
machines are correct and are ported, not redesigned; what changes is everything around
them:

**Fail loudly at setup, not per frame.**  ``create_counter_from_zone_config`` accepts *at
least* 2 lines for ``abline`` (``geometry.py:131``) and silently uses the first two, and
``AnalyticsEngine._apply_zone_config`` only raises at ``engine.py:673`` if the count is
wrong at that one call site.  With one line there is no crossing order and with three there
is no pairing, so the direction is undefined and the counter reports zero *forever* -- which
reads to an operator as a quiet doorway.  Here ``abline`` requires **exactly 2** lines and
``polygon`` **exactly 1** zone, checked in ``__init__``.  That is the same requirement the
manifest already states in ``LineCrossingConfig.geometry_requirements()``; this is where it
is enforced.

**PY-7 -- one coordinate convention.**  Lines and zones arrive normalized 0-1 and are
resolved to pixels once by
:class:`~matrice_analytics.engine.primitives.geometry.SceneGeometry`.  The 20 px auto-inset
band (``analytics/geometry.py:29,153``) is pixel-defined, which is why pixels are derived
at all.

**PY-13 -- no wall clock.**  The legacy counters carry a ``frame_index`` and
``counting_utils`` imports ``time``; nothing here reads a clock.  The only time this
primitive knows is ``ctx.frame_ts``, and warmup is counted in frames.

**09 §4 -- all state in the ``StateStore``.**  ``ABLineCounter`` keeps
``self.track_region`` / ``self.track_entered_from`` / ``self.total_in`` as instance
attributes; every one of them is a keyed value here, with an explicit
:class:`~matrice_analytics.engine.state.Lifetime`.  Cumulative totals are
``PERSISTENT`` (**FROZEN-4**: "since last restart"); the per-window deltas are ``WINDOW``.

**Track ids are a hard dependency.**  ``LineCrossingConfig.REQUIRES = ("track",)``, so the
manifest loader already rejects a pipeline without one.  Ids are read from
``ctx.detections[].track_id``, which the runtime stamps from the tracker stage's
:attr:`~.base.PrimitiveOutput.tracks` before this stage sees the frame
(``runtime/session.py``); :meth:`LineCrossing.process` re-checks against ``ctx.previous`` and
raises rather than counting zero, because a counter that silently needs something it has not
got is the failure mode this engine exists to remove.

Three ways this counter can have no ids, and they are **three different outcomes**, because
one of them used to swallow the other two: no tracker in the pipeline is an error; a tracker
whose ids never reached the detections is an error (it is the defect that made this stage
count zero across a doorway a person had just walked through); a tracker that ran and
associated nothing is counted -- ``untracked`` per frame, plus a logged, counted
:data:`~.velocity_state.UNASSOCIATED_FRAMES_KEY` -- and returns no points.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar

from matrice_analytics.engine.manifest.models import LineCrossingConfig
from matrice_analytics.engine.primitives.base import (
    FrameContext,
    PipelineDetection,
    PrimitiveOutput,
    Scalar,
    WindowOutput,
    register,
)
from matrice_analytics.engine.primitives.geometry import (
    DEFAULT_INSET_PX,
    GeometryError,
    Point,
    Polygon,
    SceneGeometry,
    Segment,
    check_geometry_matches_frame,
    detection_reference_point,
    resolve_geometry,
)
from matrice_analytics.engine.primitives.velocity_state import (
    note_unassociated_frame,
    tracker_stage,
)
from matrice_analytics.engine.state import Lifetime, StateStore

__all__ = ["LineCrossing"]


#: ``ABLineCounter.OUTSIDE_SEGMENT_EXTENT`` -- the point is beyond the *ends* of the two
#: lines, so it is walking past the doorway rather than through it.  Crossing logic is
#: suspended for such a point rather than guessed at.
OUTSIDE_EXTENT = -2

#: ``PolygonCounter.initial_warmup_frames``.  For the first few frames every track already
#: inside the inner polygon is counted once, so a camera that starts on a busy scene does
#: not report an empty room until everybody happens to walk out and back in.
WARMUP_FRAMES = 5

# -- state keys -------------------------------------------------------------
_TOTAL_IN = "total_in"            # PERSISTENT -- since process start (FROZEN-4)
_TOTAL_OUT = "total_out"          # PERSISTENT
_WINDOW_IN = "window_in"          # WINDOW
_WINDOW_OUT = "window_out"        # WINDOW
_REGIONS = "regions"              # PERSISTENT -- track_id -> region (abline)
_ENTERED_FROM = "entered_from"    # PERSISTENT -- track_id -> region it entered the zone from
_TRACK_STATES = "track_states"    # PERSISTENT -- track_id -> inside|outside|buffer (polygon)
_COUNTED_IDS = "counted_ids"      # PERSISTENT -- track ids already counted in (polygon)
_FRAME_INDEX = "frame_index"      # PERSISTENT -- warmup counter, in frames not seconds
_UNTRACKED = "untracked"          # WINDOW -- detections with no track id, i.e. uncountable


@register(name="line_crossing")
class LineCrossing:
    """Count directional crossings, ``in`` / ``out`` / ``net``.

    Two methods, selected by ``LineCrossingConfig.method``:

    ``abline``
        A trap zone between **exactly two** lines.  A track counts only on a *full*
        traversal -- ``A -> zone -> B`` or ``B -> zone -> A`` -- so loitering on the
        threshold does not ratchet the counter.  ``in_direction`` says which traversal is
        ``in``.
    ``polygon``
        **Exactly one** zone, with an inner band auto-inset by ``inset_px`` (default
        :data:`~matrice_analytics.engine.primitives.geometry.DEFAULT_INSET_PX`).  The band
        between the outer boundary and the inner one is hysteresis: a track jittering on the
        boundary sits in the band and changes nothing.  Entering the inner polygon is ``in``
        under ``A_to_B`` and ``out`` under ``B_to_A``.

    Per-frame ``values``:

    ``in`` / ``out``
        Crossings completed **this frame** -- the increments, not the totals, so a metric
        with ``agg_type: sum`` adds up to the window's traffic.  This mirrors
        ``ABLineCounter.new_in`` / ``new_out``.
    ``net``
        ``in - out`` for this frame.
    ``total_in`` / ``total_out`` / ``total_net``
        Cumulative since process start (**FROZEN-4**).
    ``present``
        How many tracks are currently inside.
    ``untracked``
        Detections in this frame with no ``track_id``.  They cannot be counted, so the loss
        is published rather than dropped (**PY-10** in spirit).
    """

    name: ClassVar[str] = "line_crossing"
    Config: ClassVar[type[LineCrossingConfig]] = LineCrossingConfig

    __slots__ = (
        "_config",
        "_geometry",
        "_inner",
        "_line_a",
        "_line_b",
        "_outer",
        "_side_a_toward_zone",
        "_side_b_toward_zone",
        "_state",
        "_track_stage",
    )

    def __init__(
        self,
        config: LineCrossingConfig,
        state: StateStore,
        *,
        geometry: SceneGeometry | None = None,
        track_stage: str | None = None,
    ) -> None:
        """Resolve and **validate** the geometry now.

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
        self._config = config
        self._state = state
        self._track_stage = track_stage
        self._geometry = resolve_geometry(state, geometry)

        self._line_a: Segment | None = None
        self._line_b: Segment | None = None
        self._outer: Polygon | None = None
        self._inner: Polygon | None = None
        self._side_a_toward_zone: int = 1
        self._side_b_toward_zone: int = 1

        if config.method == "abline":
            self._setup_abline()
        else:
            self._setup_polygon()

    # -- setup --------------------------------------------------------------

    def _setup_abline(self) -> None:
        """Require exactly two lines and pre-compute the trap zone's invariants.

        Raises:
            GeometryError: Not exactly two lines.  ``create_counter_from_zone_config``
                accepts "at least 2" and takes the first two, so a third line drawn for a
                different app on the same camera silently changes which pair counts.
        """
        lines = self._geometry.lines
        if len(lines) != 2:
            raise GeometryError(
                f"line_crossing stage {self._config.stage_name!r} uses method: abline, "
                f"which needs exactly 2 lines; this camera has {len(lines)} "
                f"({', '.join(repr(n) for n in lines) or 'none'}). abline infers direction "
                "from the order two parallel lines are crossed in: with one line there is "
                "no order and with three there is no pairing, so the direction is undefined "
                "and the counter would report zero forever. Draw exactly two lines, or use "
                "method: polygon."
            )
        self._line_a, self._line_b = tuple(lines.values())

        # Which side of each line the trap zone is on: the side the *other* line's midpoint
        # is on.  Pre-computed once, exactly as ABLineCounter.__init__ does it.
        mid_a = _midpoint(self._line_a.start, self._line_a.end)
        mid_b = _midpoint(self._line_b.start, self._line_b.end)
        self._side_a_toward_zone = self._line_a.side_of(mid_b)
        self._side_b_toward_zone = self._line_b.side_of(mid_a)

    def _setup_polygon(self) -> None:
        """Require exactly one zone and build the auto-inset inner band.

        Raises:
            GeometryError: Not exactly one zone, or the inset collapses it.
        """
        zones = self._geometry.zones
        if len(zones) != 1:
            raise GeometryError(
                f"line_crossing stage {self._config.stage_name!r} uses method: polygon, "
                f"which counts entries across a band inset from exactly 1 zone boundary; "
                f"this camera has {len(zones)} "
                f"({', '.join(repr(n) for n in zones) or 'none'}). With two zones the pair "
                "the legacy counter picks depends on dict order -- name the one you mean by "
                "drawing only it, or use method: abline."
            )
        self._outer = next(iter(zones.values()))
        inset = self._config.inset_px if self._config.inset_px is not None else DEFAULT_INSET_PX
        self._inner = self._outer.inset(float(inset))

    # -- per frame ----------------------------------------------------------

    def process(self, ctx: FrameContext) -> PrimitiveOutput:
        """Advance the counter by one frame.

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
        points = self._tracked_points(ctx)
        between: dict[int, str] = {}
        just_crossed: dict[int, str] = {}
        if self._config.method == "abline":
            new_in, new_out, present, between, just_crossed = self._update_abline(points)
        else:
            new_in, new_out, present = self._update_polygon(points)

        if self._config.in_direction == "B_to_A":
            new_in, new_out = new_out, new_in
            forward_label, backward_label = "out", "in"
        else:
            forward_label, backward_label = "in", "out"

        total_in = self._state.incr(_TOTAL_IN, new_in, lifetime=Lifetime.PERSISTENT)
        total_out = self._state.incr(_TOTAL_OUT, new_out, lifetime=Lifetime.PERSISTENT)
        self._state.incr(_WINDOW_IN, new_in, lifetime=Lifetime.WINDOW)
        self._state.incr(_WINDOW_OUT, new_out, lifetime=Lifetime.WINDOW)

        untracked = sum(1 for det in ctx.detections if det.track_id is None)
        if untracked:
            self._state.incr(_UNTRACKED, untracked, lifetime=Lifetime.WINDOW)

        values: dict[str, Scalar] = {
            "in": new_in,
            "out": new_out,
            "net": new_in - new_out,
            "total_in": int(total_in),
            "total_out": int(total_out),
            "total_net": int(total_in - total_out),
            "present": present,
            "untracked": untracked,
        }
        # `expose_corridor_state` alone drives wire_detections/live_category/per_category,
        # unchanged from before `include_completed_crossings` existed -- this is Footfall's
        # own "corridor occupancy" concept, and no other flag touches it.
        wire_detections = None
        if self._config.expose_corridor_state:
            directions = {
                track_id: (forward_label if side == "forward" else backward_label)
                for track_id, side in between.items()
            }
            values["live_category.in"] = sum(1 for side in directions.values() if side == "in")
            values["live_category.out"] = sum(1 for side in directions.values() if side == "out")
            # Cumulative, mirroring total_in/total_out exactly -- tracking_stats.total_counts
            # and current_new_counts read these via the per_category.<entity> convention.
            values["per_category.in"] = int(total_in)
            values["per_category.out"] = int(total_out)
            wire_detections = tuple(
                det.model_copy(update={"category": directions[int(det.track_id)]})
                for det in ctx.detections
                if det.track_id is not None and int(det.track_id) in directions
            )

        # `include_completed_crossings` is fully independent and never touches
        # wire_detections/live_category/per_category -- those are `expose_corridor_state`'s
        # own concept (currently-between-the-lines occupancy), and a downstream custom stage
        # setting its OWN wire_detections from this data would collide with line_crossing's
        # (session.py logs "N stages set wire_detections this frame" -- a real signal for an
        # accidental double-set elsewhere, which this pattern would otherwise silence for
        # every app that wants both). Instead, these publish as plain comma-separated ID
        # strings (Scalar = float | int | str) -- ignored by window.py's ZoneCounters (no
        # per_category./live_category. prefix), readable only by a downstream custom stage
        # via `ctx.previous["line_crossing"].values` (e.g. tailgating_detection's
        # `_crossing_track_ids`, which needs WHICH track_id caused this frame's `in`/`out`,
        # not just how many).
        if self._config.include_completed_crossings:
            in_ids = [track_id for track_id, side in just_crossed.items() if (forward_label if side == "forward" else backward_label) == "in"]
            out_ids = [track_id for track_id, side in just_crossed.items() if (forward_label if side == "forward" else backward_label) == "out"]
            values["in_track_ids"] = ",".join(str(t) for t in in_ids)
            values["out_track_ids"] = ",".join(str(t) for t in out_ids)

        return PrimitiveOutput(values=values, wire_detections=wire_detections)

    def _tracked_points(self, ctx: FrameContext) -> list[tuple[int, Point]]:
        """``(track_id, reference point in pixels)`` for every countable detection.

        Positions come from ``ctx.detections`` because that is the only place a bounding box
        exists -- ``TrackState`` carries identity and timing, not geometry.  The ids are on
        the same detections, stamped by the runtime from the tracker stage's ``tracks``.
        ``ctx.previous`` is what proves a tracker *ran*, and ``ctx.stream`` is what proves the
        lines were resolved against the frame size actually arriving (**PY-7**): a trap zone
        built at 1920x1080 and fed 640x480 frames sits in the wrong part of the scene and
        counts zero forever, which reads as a quiet doorway.

        Raises:
            ValueError: There are detections, none of them has an id, and either no tracker
                ran at all or one ran whose ids never reached the detections.  The second
                case used to return ``()`` here, which is how a person walking through the
                trap zone produced ``in: 0`` on every frame with nothing in the logs.
        """
        check_geometry_matches_frame(self._geometry, ctx, self._config.stage_name)
        detections: Sequence[PipelineDetection] = ctx.detections
        tracked = [det for det in detections if det.track_id is not None]
        if detections and not tracked:
            self._no_ids(ctx, len(detections))
        resolution = self._geometry.resolution
        return [
            (
                int(det.track_id),  # type: ignore[arg-type]
                detection_reference_point(det, self._config.reference_point, resolution),
            )
            for det in tracked
        ]

    def _no_ids(self, ctx: FrameContext, detections: int) -> None:
        """Decide what "detections but no track ids" means, and never let it be nothing.

        Three causes, three outcomes -- the whole point of this method.  Collapsing them is
        what made the starved counter invisible:

        * **no tracker in the pipeline** -- raise.  A crossing counter without stable ids
          reports zero forever, and ``LineCrossingConfig.REQUIRES`` already said so.
        * **a tracker that associated objects whose ids did not reach the detections** --
          raise.  The runtime owns ``PipelineDetection.track_id``; ids that exist upstream
          and are absent here are a broken pipeline, not a quiet doorway.
        * **a tracker that associated nothing** -- count it (``untracked`` this frame, plus
          the logged, cumulative counter) and count no crossings.  This is legitimate for a
          few frames while ``track.min_hits`` confirms, and illegitimate for a whole stream;
          the counter is what tells those apart.
        """
        tracker = tracker_stage(ctx, prefer=self._track_stage)
        if tracker is None:
            raise ValueError(
                f"line_crossing stage {self._config.stage_name!r} saw "
                f"{detections} detection(s), none with a track_id, and no upstream "
                f"stage published tracks (pipeline so far: "
                f"{', '.join(sorted(ctx.previous)) or 'nothing'}). Directional counting "
                "needs stable ids: without them every frame looks like a new object and the "
                "counter reports zero forever. Put a 'track' stage before this one "
                "(LineCrossingConfig.REQUIRES already says so)."
            )
        name, published = tracker
        if published:
            raise ValueError(
                f"line_crossing stage {self._config.stage_name!r} saw {detections} "
                f"detection(s) with no track_id while tracker stage {name!r} reported "
                f"{published} associated track(s) on the same frame. The ids exist upstream "
                "and did not reach the detections, so this counter would report 0 crossings "
                "for the life of the process while people walk through the trap zone -- the "
                "defect this stage's docstring is about. The runtime owns "
                "PipelineDetection.track_id and stamps it from the tracker stage's "
                "PrimitiveOutput.tracks (runtime/session.py)."
            )
        note_unassociated_frame(ctx, self._config.stage_name, name, state=self._state)

    # -- the two counters ---------------------------------------------------

    def _region(self, point: Point) -> int:
        """Which of the trap zone's three regions ``point`` is in.

        ``-1`` outside line A, ``0`` between the lines, ``+1`` outside line B, or
        :data:`OUTSIDE_EXTENT` when the point projects beyond the ends of either segment.
        Ported from ``ABLineCounter._get_region``.
        """
        line_a, line_b = self._line_a, self._line_b
        if line_a is None or line_b is None:  # pragma: no cover - _setup_abline guarantees it
            raise GeometryError("abline regions requested before the two lines were resolved")
        if not (0.0 <= line_a.projection_param(point) <= 1.0):
            return OUTSIDE_EXTENT
        if not (0.0 <= line_b.projection_param(point) <= 1.0):
            return OUTSIDE_EXTENT
        side_a = line_a.side_of(point)
        side_b = line_b.side_of(point)
        if side_a == self._side_a_toward_zone and side_b == self._side_b_toward_zone:
            return 0
        if side_a != self._side_a_toward_zone:
            return -1
        return 1

    def _update_abline(
        self, points: Sequence[tuple[int, Point]]
    ) -> tuple[int, int, int, dict[int, str], dict[int, str]]:
        """One frame of the two-line trap-zone counter (``ABLineCounter.update``).

        A crossing is counted only on the *exit* from the trap zone, and only when the entry
        and exit sides differ -- ``A -> zone -> B`` is one traversal, ``A -> zone -> A`` is
        somebody changing their mind and is not counted.

        Returns:
            ``(new_in, new_out, present, between, just_crossed)`` in ``A_to_B`` orientation;
            the caller applies ``in_direction``.

            ``between`` maps the track id of every track currently in region 0 (between the
            lines) to ``"forward"`` (came from before A, heading toward B) or ``"backward"``
            (the reverse) -- only populated when ``expose_corridor_state`` is set, since no
            other caller needs it.

            ``just_crossed`` maps the track id of every track that COMPLETED a crossing on
            this exact frame to the same ``"forward"``/``"backward"`` labeling -- always
            computed (it is a byproduct of the counting loop already running, at negligible
            cost), but only USED by the caller when ``include_completed_crossings`` is set.
            Deliberately a separate dict from ``between``, not merged into it: a track that
            just left region 0 is, by construction, no longer *in* region 0 on this same
            frame, so it can never appear in ``between`` -- these are two different track
            populations on any given frame, kept independently selectable so an app can opt
            into either, both, or neither without affecting the other's meaning.
        """
        regions: dict[int, int] = dict(self._state.get(_REGIONS) or {})
        entered_from: dict[int, int] = dict(self._state.get(_ENTERED_FROM) or {})
        new_in = 0
        new_out = 0
        seen: set[int] = set()
        # A track's `region`/`entered_from` bookkeeping above already knows, for one frame
        # only, which track_id just completed a crossing and which direction -- captured here
        # so `include_completed_crossings` can surface it without a second state machine.
        # Not persisted: a completed crossing is a one-frame event, never a standing fact.
        just_crossed: dict[int, str] = {}

        for track_id, point in points:
            seen.add(track_id)
            region = self._region(point)
            previous = regions.get(track_id)

            if region == OUTSIDE_EXTENT:
                regions[track_id] = OUTSIDE_EXTENT
                continue

            if previous is not None and previous != OUTSIDE_EXTENT:
                if previous != 0 and region == 0:
                    entered_from[track_id] = previous
                elif previous == 0 and region != 0:
                    came_from = entered_from.get(track_id)
                    if came_from == -1 and region == 1:
                        new_in += 1
                        just_crossed[track_id] = "forward"
                    elif came_from == 1 and region == -1:
                        new_out += 1
                        just_crossed[track_id] = "backward"
                    entered_from.pop(track_id, None)

            regions[track_id] = region

        for track_id in list(regions):
            if track_id not in seen:
                del regions[track_id]
                entered_from.pop(track_id, None)

        self._state.set(_REGIONS, regions, lifetime=Lifetime.PERSISTENT)
        self._state.set(_ENTERED_FROM, entered_from, lifetime=Lifetime.PERSISTENT)

        total_in = float(self._state.get(_TOTAL_IN, 0) or 0)
        total_out = float(self._state.get(_TOTAL_OUT, 0) or 0)
        forward, backward = (new_in, new_out)
        if self._config.in_direction == "B_to_A":
            forward, backward = (new_out, new_in)
        present = max(0, int(total_in + forward - total_out - backward))

        between: dict[int, str] = {}
        if self._config.expose_corridor_state:
            for track_id, region in regions.items():
                if region != 0:
                    continue
                # A track spawned directly inside the corridor has no entered_from side to
                # read; legacy's own ambiguous-origin fallback is "in" (footfall.py's
                # _get_in_out_label), so "forward" (== in_direction's "in" side) here matches.
                between[track_id] = "backward" if entered_from.get(track_id) == 1 else "forward"

        return new_in, new_out, present, between, just_crossed

    def _update_polygon(self, points: Sequence[tuple[int, Point]]) -> tuple[int, int, int]:
        """One frame of the inset-band counter (``PolygonCounter.update``).

        Three states per track -- ``inside`` (in the inner polygon), ``buffer`` (in the band
        between inner and outer) and ``outside``.  A track only becomes ``outside`` by
        leaving the outer boundary, so boundary jitter parks it in ``buffer`` and changes
        nothing.  ``counted_ids`` makes a re-entry by the same track id not increment ``in``
        a second time.

        Returns:
            ``(new_in, new_out, present)`` in ``A_to_B`` orientation.
        """
        inner, outer = self._inner, self._outer
        if inner is None or outer is None:  # pragma: no cover - _setup_polygon guarantees it
            raise GeometryError("polygon counting requested before the zone was resolved")
        states: dict[int, str] = dict(self._state.get(_TRACK_STATES) or {})
        counted: dict[int, int] = dict(self._state.get(_COUNTED_IDS) or {})
        frame_index = int(self._state.get(_FRAME_INDEX, 0) or 0)
        warming_up = frame_index < WARMUP_FRAMES

        new_in = 0
        new_out = 0
        present = 0
        updated: dict[int, str] = {}

        for track_id, point in points:
            previous = states.get(track_id)
            first_seen = previous is None
            previous = previous or "outside"

            in_inner = inner.contains(point)
            in_outer = outer.contains(point)
            if in_inner:
                if previous != "inside" and track_id not in counted:
                    # Outside warmup a track must be *seen* outside first: a track whose
                    # very first sighting is already inside walked in before we were looking.
                    if warming_up or not first_seen:
                        new_in += 1
                        counted[track_id] = 1
                state = "inside"
            elif not in_outer:
                if previous == "inside":
                    new_out += 1
                state = "outside"
            else:
                state = previous

            updated[track_id] = state
            if state == "inside":
                present += 1

        self._state.set(_TRACK_STATES, updated, lifetime=Lifetime.PERSISTENT)
        self._state.set(_COUNTED_IDS, counted, lifetime=Lifetime.PERSISTENT)
        self._state.set(_FRAME_INDEX, frame_index + 1, lifetime=Lifetime.PERSISTENT)
        return new_in, new_out, present

    # -- per window ---------------------------------------------------------

    def window(self, frames: Sequence[PrimitiveOutput]) -> WindowOutput:
        """Collapse the window: crossings **sum**, totals carry over.

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
        state = self._state
        window_in = int(state.get(_WINDOW_IN, 0) or 0)
        window_out = int(state.get(_WINDOW_OUT, 0) or 0)
        total_in = int(state.get(_TOTAL_IN, 0) or 0)
        total_out = int(state.get(_TOTAL_OUT, 0) or 0)
        return WindowOutput(
            values={
                "in": window_in,
                "out": window_out,
                "net": window_in - window_out,
                "total_in": total_in,
                "total_out": total_out,
                "total_net": total_in - total_out,
                "untracked": int(state.get(_UNTRACKED, 0) or 0),
            }
        )

    def reset(self) -> None:
        """Clear the window deltas; keep the totals and the per-track state.

        ``09`` §4 rule 2.  Clearing ``regions`` here would make every track look new on the
        first frame of every window, so a person mid-traversal at the boundary would never
        be counted -- a per-window undercount that no test of a single window can see.
        """
        self._state.end_window()

    # -- introspection ------------------------------------------------------

    def __repr__(self) -> str:
        target = (
            f"lines={[self._line_a.name, self._line_b.name]!r}"
            if self._config.method == "abline" and self._line_a and self._line_b
            else f"zone={self._outer.name!r}" if self._outer else "unconfigured"
        )
        return (
            f"LineCrossing(stage={self._config.stage_name!r}, "
            f"method={self._config.method!r}, {target}, "
            f"in_direction={self._config.in_direction!r})"
        )


def _midpoint(start: Point, end: Point) -> Point:
    """The midpoint of a segment, in pixels."""
    return ((start[0] + end[0]) / 2.0, (start[1] + end[1]) / 2.0)
