"""Auto-generated stub for module: dwell."""
from typing import Any

# Constants
logger: Any

# Classes
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
