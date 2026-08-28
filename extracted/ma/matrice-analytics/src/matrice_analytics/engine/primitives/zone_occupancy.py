"""``zone_occupancy`` -- polygon membership and per-zone counts.

Normative sources: ``_contracts/05-asis-zones-and-geometry.md`` §4 (what the legacy
assignment does) and ``clauding/STAGE_BC_PLAN.md`` §2 (B2).  Ported from
``analytics/geometry.py:225`` (``assign_detections_to_zones``) and
``analytics/engine.py:315-400`` (``_setup_zone_processors``).

Three behaviour changes, each with a defect id:

**PY-10 -- the loss is countable.**  ``assign_detections_to_zones`` drops a detection that
matches no zone (``geometry.py:246``) and nothing counts what was lost, so a polygon drawn
on the wrong half of the frame is indistinguishable from an empty room.  Here
``unassigned_count`` is published every frame under *every* ``on_no_match`` policy,
including ``drop``.

**PY-10 -- overlap is a decision.**  The legacy loop ``break``s on the first containing
zone, so two overlapping polygons resolve by ``dict`` insertion order -- effectively
undefined.  ``on_overlap`` names the choice, and ``first_match`` resolves in *drawing*
order (:class:`~matrice_analytics.engine.primitives.geometry.SceneGeometry` preserves it).

**PY-7 -- one coordinate convention.**  Detections and zones both arrive normalized 0-1;
pixels are derived once at setup by ``SceneGeometry``.  Nothing in this file multiplies by
a resolution.

**PY-6 -- the no-zone sentinel is ``"global"``**, never ``"__global__"``
(``usecases/people_counting.py:307``).  A detection outside every zone lands in
``"unassigned"``, which is a *different* thing from ``"global"``: ``"global"`` means the
app has no zones at all.

**No zones drawn -- the implicit global bucket counts, it does not lose.**
:meth:`~matrice_analytics.engine.primitives.geometry.SceneGeometry.empty` documents "an
app with no ``zones:`` block runs in the single ``GLOBAL_ZONE`` bucket", and
``runtime/session.py`` honours that (``buckets = {GLOBAL_ZONE: tuple(detections)}``
unconditionally). This stage must honour it too: when :meth:`~.geometry.SceneGeometry.select_zones`
returns no polygons *because the camera has none drawn*, every in-frame detection counts
toward ``occupancy`` -- it is not routed through ``assign_detections_to_zones`` and is not
``unassigned``. ``on_no_match`` only governs detections that fall outside *drawn* zones;
with zero zones drawn there is nothing to fall outside of.

Zone identity is the drawn name, via
:func:`~matrice_analytics.engine.primitives.geometry.zone_identity` -- backlog **Q1**, and
that function is the single edit when it is answered.
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from typing import ClassVar

from matrice_analytics.engine.manifest.models import ZoneOccupancyConfig
from matrice_analytics.engine.primitives.base import (
    FrameContext,
    PrimitiveOutput,
    WindowOutput,
    register,
)
from matrice_analytics.engine.primitives.geometry import (
    NoMatchPolicy,
    OverlapPolicy,
    Polygon,
    SceneGeometry,
    ZoneAssignment,
    assign_detections_to_zones,
    check_geometry_matches_frame,
    resolve_geometry,
)
from matrice_analytics.engine.state import Lifetime, StateStore

__all__ = ["ZoneOccupancy"]

logger = logging.getLogger(__name__)

_OVERLAP_POLICIES: frozenset[str] = frozenset({"first_match", "all_match", "error"})

# -- state keys -------------------------------------------------------------
# Named here rather than inline so the lifetime of each is visible in one place (09 §4
# rule 2: getting window-vs-cumulative backwards is the most common custom-code bug).
_FRAMES = "frames"                       # WINDOW
_OCCUPANCY_PEAK = "occupancy_peak"       # WINDOW
_OCCUPANCY_LAST = "occupancy_last"       # WINDOW  -- the most recent frame's occupancy
_OCCUPANCY_SUM = "occupancy_sum"         # WINDOW
_UNASSIGNED_WINDOW = "unassigned_window"  # WINDOW
_ZONE_PEAK = "zone_peak"                 # WINDOW  (zone identity -> int)
_ZONE_LAST = "zone_last"                 # WINDOW  (zone identity -> int, most recent frame)
_ZONE_SUM = "zone_sum"                   # WINDOW  (zone identity -> int)
_UNASSIGNED_TOTAL = "unassigned_total"   # PERSISTENT -- since process start (FROZEN-4)


@register(name="zone_occupancy")
class ZoneOccupancy:
    """Count detections per zone, and count the ones that fit in none.

    Per-frame ``values``:

    ``per_zone.<zone>.count``
        Detections whose reference point is inside that zone, this frame.  Keyed by
        :func:`~matrice_analytics.engine.primitives.geometry.zone_identity`, **not** by the
        raw drawn name: a dot in the name would break the key it is spliced into, since the
        manifest validates a ``zones: all`` stage's per-zone sources against
        ``^per_zone\\.[^.]+\\.count$``.  ``zone_identity`` maps it to ``_`` once, for the
        output key, the window key and the state accumulator alike.
    ``occupancy``
        **Distinct** detections inside at least one zone.  Under ``on_overlap: all_match``
        this is deliberately *less than* the sum of the per-zone counts -- occupancy counts
        people, the per-zone counts count memberships. On a camera with **no zones drawn
        at all**, there is no "at least one zone" to test: every detection counts here
        instead, the documented implicit global bucket (:meth:`~.geometry.SceneGeometry.empty`).
    ``unassigned_count``
        Detections inside no *drawn* zone, counted under every ``on_no_match`` policy
        (**PY-10**).  Always ``0`` when the camera has no zones drawn at all -- that case is
        ``occupancy`` in full, not a loss.
    ``peak_occupancy`` / ``avg_occupancy``
        The window's high-water mark and mean **so far** -- the same accumulators
        :meth:`window` reads at the boundary, read one frame earlier.  A per-frame consumer
        (``FrameOutcome.metric_values``, an incident's ``human_text``) gets "the peak/mean
        so far this window", not an absent key, which is what these two names hand back
        before the window closes.  Final at the boundary; live and monotonically settling
        before it.

    Window ``values`` collapse those over the aggregation window, and every reading has its
    **own name** so no two can be confused (**PY-1**) and none of them depends on a
    ``metrics[].agg_type`` the runtime deliberately does not apply: ``occupancy`` and
    ``per_zone.<zone>.count`` hold the window's **last frame**, ``peak_occupancy`` and
    ``per_zone.<zone>.count_peak`` its **peak**, ``avg_occupancy`` and
    ``per_zone.<zone>.avg`` its **mean**, ``unassigned_count`` the window's sum,
    ``unassigned_total`` the loss since process start and ``frames`` how many frames the window
    saw.

    Example:
        >>> zone_occupancy = ZoneOccupancy(config, state, geometry=geometry)  # doctest: +SKIP
        >>> zone_occupancy.process(ctx).values["per_zone.Polygon 1.count"]    # doctest: +SKIP
        3
    """

    name: ClassVar[str] = "zone_occupancy"
    Config: ClassVar[type[ZoneOccupancyConfig]] = ZoneOccupancyConfig

    __slots__ = ("_config", "_geometry", "_implicit_global", "_on_overlap", "_state", "_zones")

    def __init__(
        self,
        config: ZoneOccupancyConfig,
        state: StateStore,
        *,
        geometry: SceneGeometry | None = None,
        on_overlap: OverlapPolicy | None = None,
    ) -> None:
        """Resolve the geometry now, so a broken installation fails at setup.

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
        self._config = config
        self._state = state
        self._geometry = resolve_geometry(state, geometry)

        if on_overlap is None:
            on_overlap = "first_match"
        if on_overlap not in _OVERLAP_POLICIES:
            raise ValueError(
                f"zone_occupancy on_overlap={on_overlap!r} is not one of "
                f"{sorted(_OVERLAP_POLICIES)}. It comes from the manifest's zones: block; "
                "an unknown value would silently fall back to insertion order, which is the "
                "undefined behaviour PY-10 is about."
            )
        self._on_overlap: OverlapPolicy = on_overlap

        # select_zones raises when the manifest names a zone this camera has not got --
        # otherwise the stage publishes per_zone.<missing>.count = 0 forever, and a zero is
        # indistinguishable from a quiet zone.
        self._zones: tuple[Polygon, ...] = self._geometry.select_zones(config.zones)

        # Empty here means the camera has no zone geometry drawn at all -- select_zones
        # only ever returns () in that case (a named-but-missing zone raises instead). That
        # is SceneGeometry.empty()'s documented "single implicit global bucket" case, not a
        # loss, so _assign short-circuits assign_detections_to_zones entirely below and
        # every detection counts toward occupancy.
        self._implicit_global: bool = not self._zones

        if self._implicit_global:
            logger.warning(
                "zone_occupancy stage %r has no zone geometry: every detection counts "
                "toward the implicit global zone (whole-frame occupancy), per "
                "SceneGeometry.empty()'s documented fallback. To measure per-zone "
                "occupancy instead, draw zones for this camera and set zones.required: "
                "true in the manifest.",
                config.stage_name,
            )

    # -- per frame ----------------------------------------------------------

    def process(self, ctx: FrameContext) -> PrimitiveOutput:
        """Assign this frame's detections to zones and publish the counts.

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
        assignment = self._assign(ctx)

        values: dict[str, float | int | str] = {}
        for zone in self._zones:
            values[f"per_zone.{zone.identity}.count"] = len(assignment.by_zone[zone.identity])
        values["occupancy"] = assignment.assigned_count
        values["unassigned_count"] = assignment.no_match_count

        self._accumulate(assignment)

        # Live, so-far-this-window readings. `_accumulate` just updated these accumulators
        # for this frame -- `.window()` only ever reads them back at the boundary, so a
        # per-frame consumer (FrameOutcome.metric_values, an incident's human_text) saw
        # neither key at all until the window closed, indistinguishable from a stage that
        # does not exist. Publishing "the peak/mean so far" here costs one state read each
        # (already O(1), no new accumulator) and does not change window-boundary resolution:
        # `.window()` still publishes both keys unconditionally, and window.py's
        # `_metric_value` checks the WindowOutput first -- this addition is never consulted
        # there.
        frame_count = int(self._state.get(_FRAMES, 0) or 0)
        values["peak_occupancy"] = int(self._state.get(_OCCUPANCY_PEAK, 0) or 0)
        values["avg_occupancy"] = (
            float(self._state.get(_OCCUPANCY_SUM, 0) or 0) / frame_count if frame_count else 0.0
        )
        return PrimitiveOutput(values=values)

    def _assign(self, ctx: FrameContext) -> ZoneAssignment:
        """Partition ``ctx.detections`` under the declared policies.

        The geometry was resolved once at setup, so this checks it still describes the frames
        arriving -- ``ctx.stream`` is what makes that possible, and a mismatch is the silent
        1920x error (**PY-7**).  See
        :func:`~matrice_analytics.engine.primitives.geometry.check_geometry_matches_frame`.
        """
        check_geometry_matches_frame(self._geometry, ctx, self._config.stage_name)

        if self._implicit_global:
            # No polygons to test against -- and none to test with, since SceneGeometry.empty()
            # carries a (0, 0) resolution. assign_detections_to_zones's "empty zones is a
            # no-match" contract is right for *it* (a general partitioner has no camera-level
            # concept of "there simply is no geometry"), but wrong here: this is the documented
            # single implicit global bucket, so every detection this frame counts toward
            # occupancy and none are unassigned.
            count = len(ctx.detections)
            return ZoneAssignment(by_zone={}, unassigned=(), no_match_count=0, assigned_count=count)

        return assign_detections_to_zones(
            ctx.detections,
            self._zones,
            self._geometry.resolution,
            reference_point=self._config.reference_point,
            on_no_match=self._no_match_policy,
            on_overlap=self._on_overlap,
            # Nothing downstream of a count needs a re-stamped copy of every detection, and
            # copying a pydantic model per detection per frame is the kind of cost that only
            # shows up at 25 fps across four zones.
            stamp_zone=False,
        )

    @property
    def _no_match_policy(self) -> NoMatchPolicy:
        """``zone_occupancy.on_no_match`` -- see :data:`NoMatchPolicy` (**PY-10**)."""
        return self._config.on_no_match

    def _accumulate(self, assignment: ZoneAssignment) -> None:
        """Fold this frame into the window accumulators.

        Every write states its :class:`~matrice_analytics.engine.state.Lifetime` (``09`` §4
        rule 2).  The window peaks and sums clear at ``end_window``; ``unassigned_total`` is
        cumulative and clears only when the process does (**FROZEN-4**).
        """
        state = self._state
        state.incr(_FRAMES, 1, lifetime=Lifetime.WINDOW)
        state.incr(_OCCUPANCY_SUM, assignment.assigned_count, lifetime=Lifetime.WINDOW)
        state.incr(_UNASSIGNED_WINDOW, assignment.no_match_count, lifetime=Lifetime.WINDOW)
        state.incr(_UNASSIGNED_TOTAL, assignment.no_match_count, lifetime=Lifetime.PERSISTENT)

        peak = state.get(_OCCUPANCY_PEAK, 0)
        if assignment.assigned_count > peak:
            state.set(_OCCUPANCY_PEAK, assignment.assigned_count, lifetime=Lifetime.WINDOW)
        # The *last* reading is a separate accumulator, not a derivation of the peak: the window
        # publishes both under two names, because it is published verbatim and `agg_type` cannot
        # turn a peak into a current level (see `window`).
        state.set(_OCCUPANCY_LAST, assignment.assigned_count, lifetime=Lifetime.WINDOW)

        zone_peak: dict[str, int] = dict(state.get(_ZONE_PEAK) or {})
        zone_sum: dict[str, int] = dict(state.get(_ZONE_SUM) or {})
        zone_last: dict[str, int] = {}
        for identity, detections in assignment.by_zone.items():
            count = len(detections)
            zone_peak[identity] = max(zone_peak.get(identity, 0), count)
            zone_sum[identity] = zone_sum.get(identity, 0) + count
            zone_last[identity] = count
        state.set(_ZONE_PEAK, zone_peak, lifetime=Lifetime.WINDOW)
        state.set(_ZONE_SUM, zone_sum, lifetime=Lifetime.WINDOW)
        state.set(_ZONE_LAST, zone_last, lifetime=Lifetime.WINDOW)

    # -- per window ---------------------------------------------------------

    def window(self, frames: Sequence[PrimitiveOutput]) -> WindowOutput:
        """Collapse the window.

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
        state = self._state
        frame_count = int(state.get(_FRAMES, 0) or 0)
        peak = int(state.get(_OCCUPANCY_PEAK, 0) or 0)
        occupancy_sum = float(state.get(_OCCUPANCY_SUM, 0) or 0)
        zone_peak: dict[str, int] = dict(state.get(_ZONE_PEAK) or {})
        zone_last: dict[str, int] = dict(state.get(_ZONE_LAST) or {})
        zone_sum: dict[str, int] = dict(state.get(_ZONE_SUM) or {})

        values: dict[str, float | int | str] = {
            "frames": frame_count,
            "occupancy": int(state.get(_OCCUPANCY_LAST, 0) or 0),
            "peak_occupancy": peak,
            "avg_occupancy": (occupancy_sum / frame_count) if frame_count else 0.0,
            "unassigned_count": int(state.get(_UNASSIGNED_WINDOW, 0) or 0),
            "unassigned_total": int(state.get(_UNASSIGNED_TOTAL, 0) or 0),
        }
        for zone in self._zones:
            identity = zone.identity
            values[f"per_zone.{identity}.count"] = zone_last.get(identity, 0)
            values[f"per_zone.{identity}.count_peak"] = zone_peak.get(identity, 0)
            values[f"per_zone.{identity}.avg"] = (
                zone_sum.get(identity, 0) / frame_count if frame_count else 0.0
            )
        return WindowOutput(values=values)

    def reset(self) -> None:
        """Clear window state at the aggregation boundary -- and nothing else.

        ``09`` §4 rule 2.  ``unassigned_total`` is
        :attr:`~matrice_analytics.engine.state.Lifetime.PERSISTENT` and survives, because
        the backend's rollup formula assumes a cumulative total only resets when the process
        does (**FROZEN-4**).  Calling ``state.clear()`` here is exactly the bug the two
        lifetimes exist to prevent.
        """
        self._state.end_window()

    # -- introspection ------------------------------------------------------

    @property
    def zone_identities(self) -> tuple[str, ...]:
        """The zone identities this stage publishes, in drawing order (**Q1** seam)."""
        return tuple(zone.identity for zone in self._zones)

    def __repr__(self) -> str:
        return (
            f"ZoneOccupancy(stage={self._config.stage_name!r}, "
            f"zones={list(self.zone_identities)!r}, "
            f"reference_point={self._config.reference_point!r}, "
            f"on_no_match={self._no_match_policy!r}, on_overlap={self._on_overlap!r})"
        )
