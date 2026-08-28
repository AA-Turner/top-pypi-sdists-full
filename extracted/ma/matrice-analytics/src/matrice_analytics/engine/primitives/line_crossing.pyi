"""Auto-generated stub for module: line_crossing."""
from typing import Any

# Constants
OUTSIDE_EXTENT: Any
WARMUP_FRAMES: int

# Classes
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

