"""Auto-generated stub for module: zone_occupancy."""
from typing import Any

# Constants
logger: Any

# Classes
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

