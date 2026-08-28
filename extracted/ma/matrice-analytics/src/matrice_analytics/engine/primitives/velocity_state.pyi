"""Auto-generated stub for module: velocity_state."""
from typing import Any, Optional

# Constants
logger: Any

# Functions
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
def reference_point(det: Any) -> tuple[float, float]:
    """
    The normalized 0-1 point whose motion *is* the object's motion: the box centre.
    
        See the module docstring for why this is the centre and not one of the three foot
        points the legacy tree uses.  Kept a module function rather than a method so ``dwell``
        and a custom primitive can agree with this one without inheriting anything (``09`` §3).
    """
    ...
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
def signed_heading_delta(heading: float, expected: float) -> float:
    """
    The smallest absolute angle between two headings, in degrees ``[0, 180]``.
    
        Wrapping done once, here: 350 vs 10 is 20 degrees apart, not 340.  Every legacy
        comparison of two angles in this tree either avoids the problem by using a dot product
        (``wrong_way_tracker.py``) or does not compare angles at all.
    """
    ...
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

