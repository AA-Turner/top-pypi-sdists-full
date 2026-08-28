"""``velocity_state`` -- per-track speed, heading and stationarity, named **once**.

Normative source: ``_contracts/09-tobe-engine-architecture.md`` §3 and
``clauding/STAGE_BC_PLAN.md`` §2 (workstream B3).

This primitive does not exist anywhere in the legacy tree.  Six use cases each grew their
own, under **ten different names for one concept**::

    velocity_threshold_px_per_sec          loitering_detection.py:109        (18.0)
    velocity_threshold_px_per_sec          abandoned_object_detection.py:132 (15.0)
    stationary_ratio_threshold             loitering_detection.py:110        (0.70)
    stationary_ratio_threshold             abandoned_object_detection.py:133 (0.75)
    short_term_displacement_threshold_px   stopped_vehicle_monitoring.py:36  (20.0, dead)
    long_term_drift_threshold_px           stopped_vehicle_monitoring.py:37  (25.0, dead)
    short_term_displacement_threshold_px   illegal_parking_detection.py:61   (10.0)
    long_term_drift_threshold_px           illegal_parking_detection.py:62   (12.0, dead)
    movement_threshold_percent             parking_analytics_tracker.py:63   (5.0)
    wrong_way_min_velocity                 vehicle_monitoring_wrong_way.py:76 (2.0 px/*frame*)

Naming it once is most of the value (``08`` §2).  Four substantive decisions follow from
reading those six, and each is a behaviour change worth stating out loud:

**Speed is net displacement over a time window, not a per-frame delta.**  Four of the six
compute ``|p_t - p_{t-1}| / dt`` and then need a second mechanism -- a ratio-of-frames
deque (loitering), an EMA (abandoned), an all-pairs displacement scan (stopped vehicle) --
to undo the jitter the first mechanism introduced.  A box that wobbles by three pixels on a
motionless person reports 75 px/s at 25 fps.  Net displacement across
:attr:`~matrice_analytics.engine.manifest.models.VelocityStateConfig.window_seconds`
answers the question those three mechanisms were approximating, once, in
:math:`O(1)` per frame rather than the :math:`O(n^2)` all-pairs loop at
``stopped_vehicle_monitoring.py:1586``.

**Every duration comes from** :attr:`~.base.FrameContext.frame_ts` (**PY-13**).  The legacy
six run on three mutually incompatible clocks: ``time.time()`` (stopped vehicle, illegal
parking), a parsed ``stream_time`` (dwell detection), and ``frame_counter / nominal_fps``
(loitering, abandoned).  Only the second survives replay, and none of them survives a
stream whose real fps differs from its declared one.  There is no clock call in this
module at all.

**One reference point, and it is the box centre.**  The legacy tree has four conventions
for the "same" idea -- ``y2``, ``y2 - 0.10h``, ``y2 - 0.25h`` and the plain centre.  A
foot point is a *ground-plane* concept: it belongs to zone membership (workstream B2),
where being on the floor is the whole question.  For a speed *magnitude* it is strictly
worse, because it inherits the full jitter of the bottom edge, whereas the centre averages
the jitter of two opposing edges.

**The resolution comes from the frame, or the stage does not run.**  Bounding boxes are
normalized 0-1 always (contract Section 4, **BE-10**/**BE-12**), so a threshold written in
*pixels* per second cannot be evaluated without the frame size.  It is read from
:meth:`~.base.FrameContext.require_resolution` -- the one standard channel, backed by
``StreamInfo.resolution``.

This module previously carried a private ``frame_resolution`` state key with a 1920x1080
fallback and a warn-once.  Both are **deleted**.  A guessed frame size does not degrade the
answer gracefully: it multiplies every measured speed by ``real_width / 1920``, so on a
640x480 camera a car crawling at 6 px/s is reported at 18 px/s and
``stationary_below_px_per_sec: 10`` silently stops firing.  The output stays plausible, the
threshold stops meaning what the manifest says it means, and the only trace is one log line
from process start.  Failing loudly is the requirement (contract Section 5).

**Track ids arrive on the detections, and their absence is never a shrug.**  The runtime
stamps :attr:`~.base.PipelineDetection.track_id` from the tracker stage before this stage
runs, so :func:`require_track_ids` reads ``det.track_id``.  It used to return an empty tuple
whenever *any* earlier stage had published tracks, which meant "the tracker associated 4
objects but their ids never reached the detections" and "the tracker associated nothing this
frame" were the same code path -- and the first of those made this primitive publish ``""``
and ``0.0`` for the life of the process while the tracker reported a busy scene.  The two are
now separated by :func:`tracker_stage`: the first raises, the second is counted and logged by
:func:`note_unassociated_frame`.

**``heading_from_line`` (MLAPP-151, 2026-08-06): the expected direction may come from a
drawn line instead of a hand-typed angle.**  ``expected_heading_deg`` alone has no
relationship to anything an operator draws on the camera -- it is a bare number in a heading
convention nobody has to confirm until it is already wrong.  ``vehicle_monitoring_wrong_way``
shipped exactly that: a placeholder angle that was never tuned per camera, so wrong-way
flagging did not track real traffic direction while every other per-frame reading (this
primitive's own ``avg_speed``, ``stationary_count``) worked correctly -- confirmed against a
live deployment, not just read from code. ``heading_from_line: true`` derives
:attr:`~matrice_analytics.engine.manifest.models.VelocityStateConfig.expected_heading_deg`
from one drawn line's ``start -> end`` direction instead, the same two-point-line workflow
``line_crossing.method: abline`` already uses (:func:`resolve_geometry`,
:class:`~.geometry.SceneGeometry`) -- resolved **once, at construction**
(:meth:`VelocityState._resolve_expected`), not per frame, for the same reason
``line_crossing._setup_abline`` pre-computes its own invariants once. Deliberately not
``line_crossing`` itself: that primitive counts a *completed* two-line crossing, a discrete
event, whereas wrong-way needs this primitive's existing *continuous* per-frame heading test
-- ``heading_from_line`` changes only where :attr:`expected_heading_deg` comes from, and
touches no other line in :meth:`VelocityState.process`.

**``expose_wrong_way_state`` (2026-08-10): the wire's box label may come from the heading
test too, not just its class.**  ``vehicle_monitoring_wrong_way`` set ``heading_from_line``
correctly and its incidents fired correctly -- ``wrong_way_count`` and the confirmed-frames
lifecycle both worked -- and the live overlay still showed every vehicle labeled by its
detected class (``car``, ``truck``, ...), never ``wrong_way``/``correct_way``, because nothing
in this primitive ever built a :attr:`~.base.PrimitiveOutput.wire_detections` override.  The
per-track flag this needed already existed --
:attr:`~.base.TrackState.attributes` ``["wrong_way"]``, set on every track below regardless of
this flag -- there was simply no path from that attribute to the wire.  This closes that gap
the same way ``line_crossing.expose_corridor_state`` relabels Footfall's boxes ``in``/``out``:
reuse the state a per-track loop already computes, do not build a second one.  A track still
accumulating its first :attr:`~matrice_analytics.engine.manifest.models.VelocityStateConfig.window_seconds`
of samples -- or classified :data:`STATIONARY`/:data:`UNKNOWN_STATE` -- has no *determined*
heading state to report and is left off the override entirely, so its box keeps showing its
detected class rather than being forced into either label; ``line_crossing`` makes the
identical choice for a track not yet in its corridor.  Deliberately gated on its own flag
rather than always-on: every other app using ``heading: true`` (there is currently exactly
one) keeps today's behaviour with no change.

**``heading_auto_learn_fallback`` (2026-08-25): a backup reference direction for the camera
that has no line drawn yet.**  ``heading_from_line`` made the reference direction something an
operator draws instead of types, but it is still a hard precondition -- zero lines drawn and
the stage refuses to start at all (:meth:`_resolve_expected`, :class:`GeometryError`), which is
right for "ambiguous" (two or more lines) but wrong for "not configured yet", the state every
camera is in before someone draws on it.  ``wrong_way_tracker.py`` -- the legacy usecase this
primitive was built to replace -- already had an answer for exactly that gap: an ``AUTO``
reference source that learns the dominant direction from observed traffic when no
``USER_ZONE`` is set, via a dominance-clustering estimator over accumulated per-track motion
samples (``_update_auto_reference``).  ``heading_auto_learn_fallback: true`` ports that
estimator into this primitive as :meth:`VelocityState._update_auto_learn`, gated so it only
ever runs in the one case a line is genuinely absent: :attr:`_expected` stays ``None`` (so
:meth:`_is_wrong_way` reports every track as *not* wrong-way, the same "not evaluated yet" the
legacy ``LEARNING`` status meant) until enough distinct, currently-moving tracks agree on one
dominant direction, at which point :attr:`_expected` is set exactly as if a line had produced
it. A camera that already has its line drawn never reaches this path -- :meth:`_resolve_expected`
already returned a fixed angle at construction, "resolved once" as before. Learned state is
:attr:`~matrice_analytics.engine.state.Lifetime.PERSISTENT`, the same lifetime ``samples`` uses,
so a window boundary does not reset a direction that took several minutes of traffic to learn.
"""

from __future__ import annotations

import logging
import math
from collections.abc import Mapping, Sequence
from typing import Any, ClassVar, Final

from matrice_analytics.engine.contract.schemas import GLOBAL_ZONE
from matrice_analytics.engine.manifest.models import VelocityStateConfig
from matrice_analytics.engine.primitives.base import (
    FrameContext,
    PipelineDetection,
    PrimitiveOutput,
    Scalar,
    TrackState,
    WindowOutput,
    register,
)
from matrice_analytics.engine.primitives.geometry import (
    GeometryError,
    SceneGeometry,
    resolve_geometry,
)
from matrice_analytics.engine.state import Lifetime, StateStore

__all__ = [
    "STATIONARY",
    "TRACKER_MARKER_VALUE",
    "TrackingRequiredError",
    "UNKNOWN_STATE",
    "VelocityState",
    "heading_degrees",
    "heading_to_unit_vector",
    "reference_point",
    "require_track_ids",
    "signed_heading_delta",
    "tracker_stage",
]

logger = logging.getLogger(__name__)


STATIONARY: Final[str] = "stationary"
"""The one spelling of "not moving".

``gate: {velocity_state: stationary}`` on a ``dwell`` stage is the config that replaces
``loitering_detection.py`` wholesale, so the string has to be fixed rather than
conventional.  A track below
:attr:`~matrice_analytics.engine.manifest.models.VelocityStateConfig.stationary_below_px_per_sec`
is labelled this **regardless** of what ``classes`` would have called it -- see
:meth:`VelocityState._classify`.
"""

UNKNOWN_STATE: Final[str] = ""
"""A track with too little history to have a speed yet.

Empty rather than ``"unknown"``: it is the default of
:attr:`~.base.TrackState.state`, so "we have not decided" has one representation.  A
newly-appeared track must not be counted stationary -- it has a *measured* speed of zero
only because it has been measured once.  Reporting it as stationary is how a busy corridor
reads as a room full of loiterers on the frame after a tracker reset.
"""

_MIN_SAMPLES: Final[int] = 2
"""Samples needed before a track has a speed at all.  One position is a point, not a path."""

#: ``heading_auto_learn_fallback`` dominance-clustering estimator constants -- one-to-one
#: ports of ``wrong_way_tracker.py``'s ``auto_ref_*`` constructor defaults, since that
#: estimator is exactly what is being ported (see the module docstring). Not exposed as
#: config: they tune an internal algorithm's convergence, not something an app author has a
#: camera-specific reason to retune, unlike ``heading_tolerance_deg``.
_AUTO_LEARN_MIN_TRACKS: Final[int] = 5
_AUTO_LEARN_MAX_SAMPLES: Final[int] = 300
_AUTO_LEARN_DOMINANCE_RATIO: Final[float] = 0.65
_AUTO_LEARN_CONFIRM_CONFIDENCE: Final[float] = 0.7
_AUTO_LEARN_STABILITY_FRAMES: Final[int] = 60
_AUTO_LEARN_EMA_ALPHA: Final[float] = 0.05
_AUTO_LEARN_CONFIDENCE_GAIN: Final[float] = 0.02


class TrackingRequiredError(RuntimeError):
    """A temporal primitive ran without usable track ids.

    ``dwell`` and ``velocity_state`` both declare ``REQUIRES = ("track",)``
    (``manifest/models.py``), so the manifest loader rejects a pipeline that omits it.  This
    exists for the two cases the loader cannot see:

    * no tracker in the pipeline at all *and* no caller-supplied ids -- the pipeline was
      built by something other than the loader;
    * a tracker that **did** associate objects this frame whose ids never reached
      ``det.track_id``.  That is a broken runtime, not a quiet camera: the runtime owns
      :attr:`~.base.PipelineDetection.track_id` and stamps it from the tracker stage's
      :attr:`~.base.PrimitiveOutput.tracks` (``runtime/session.py``).  It used to be
      swallowed, and three primitives published zeros for the life of the process.
    """


TRACKER_MARKER_VALUE: Final[str] = "active_tracks"
""":attr:`~.base.PrimitiveOutput.values` key that identifies a stage as a **tracker**.

``track`` is the only primitive that publishes it (``TrackConfig.STATIC_OUTPUTS``), and it
publishes it on *every* frame -- including the frames where it associated nothing.  That is
what makes "a tracker ran and associated nothing" distinguishable from "no tracker is
configured": the ``tracks`` map is empty in both cases, and only this key separates them.
"""

#: PERSISTENT counter, per stage: frames on which a tracker ran and associated nothing while
#: this stage had detections to measure.  A steady non-zero here is the tracker rejecting the
#: detections; it used to be an unlogged, uncounted ``return ()``.
UNASSOCIATED_FRAMES_KEY: Final[str] = "frames_with_no_associated_tracks"


def tracker_stage(ctx: FrameContext, *, prefer: str | None = None) -> tuple[str, int] | None:
    """The upstream tracker stage in this pipeline, as ``(stage name, tracks published)``.

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
    if prefer is not None:
        output = ctx.previous.get(prefer)
        return None if output is None else (prefer, len(output.tracks))
    marker: tuple[str, int] | None = None
    published: tuple[str, int] | None = None
    for name, output in ctx.previous.items():
        if TRACKER_MARKER_VALUE in output.values:
            # The authoritative signal, and it is there on an empty frame too. A tracker that
            # associated something outranks one that did not, so two trackers cannot make the
            # busy one invisible.
            if marker is None or (output.tracks and not marker[1]):
                marker = (name, len(output.tracks))
        elif published is None and output.tracks:
            published = (name, len(output.tracks))
    return marker or published


def note_unassociated_frame(
    ctx: FrameContext,
    stage: str,
    tracker: str,
    *,
    state: StateStore | None = None,
) -> float:
    """Count and log a frame where the tracker associated nothing (**loud, not silent**).

    "A tracker ran and associated nothing" is legitimate -- for a few frames at stream
    start, while ``track.min_hits`` confirms, or when every detection sits below
    ``new_track_thresh``.  It is *not* legitimate for a whole stream, and that is
    indistinguishable from a quiet camera unless somebody counts it.  So it is counted
    (:data:`UNASSOCIATED_FRAMES_KEY`, ``PERSISTENT``) and logged on a decelerating schedule
    rather than raised.

    Returns:
        How many such frames this stage has seen since process start.
    """
    # `is not None`, never truthiness: a StateStore defines __len__, so an empty store is
    # falsey and `if state` would silently stop counting exactly the first occurrence -- the
    # one that matters most.
    count = (
        1.0
        if state is None
        else state.incr(UNASSOCIATED_FRAMES_KEY, 1, lifetime=Lifetime.PERSISTENT)
    )
    if count in (1.0, 10.0) or count % 100 == 0:
        logger.warning(
            "stage %r measured nothing on frame_ts %s in zone %r: tracker stage %r ran and "
            "associated none of the %d detection(s), so every per-track value this frame is "
            "zero. That is frame %d of this since process start. A handful at stream start is "
            "normal (a track is confirmed over track.min_hits frames); a steady stream of it "
            "means the tracker is rejecting these detections -- check track.new_track_thresh "
            "and track.match_thresh against the detection confidences.",
            stage,
            ctx.frame_ts,
            ctx.zone,
            tracker,
            len(ctx.detections),
            int(count),
        )
    return count


def require_track_ids(
    ctx: FrameContext, stage: str, *, state: StateStore | None = None
) -> tuple[tuple[int, PipelineDetection], ...]:
    """This frame's detections paired with their tracker ids.

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
    tracked = tuple((det.track_id, det) for det in ctx.detections if det.track_id is not None)
    if tracked or not ctx.detections:
        return tracked
    tracker = tracker_stage(ctx)
    if tracker is None:
        raise TrackingRequiredError(
            f"stage {stage!r} needs tracker ids: {len(ctx.detections)} detection(s) in zone "
            f"{ctx.zone!r} at frame_ts {ctx.frame_ts}, none with a track_id, and no earlier "
            f"stage published any tracks. Stages that ran before this one: "
            f"{', '.join(sorted(ctx.previous)) or '(none)'}. Add a `- track:` stage to the "
            f"pipeline before {stage!r}; without one every per-track value here is zero for "
            f"the life of the process."
        )
    tracker_name, published = tracker
    if published:
        raise TrackingRequiredError(
            f"stage {stage!r} needs tracker ids: tracker stage {tracker_name!r} associated "
            f"{published} track(s) on this frame, but none of the {len(ctx.detections)} "
            f"detection(s) in zone {ctx.zone!r} carries a track_id. The ids exist and did "
            "not reach the detections, so this stage would publish zeros while the tracker "
            "reports a busy scene -- the exact failure that made line_crossing, dwell and "
            "velocity_state read zero forever. The runtime owns PipelineDetection.track_id "
            "and must stamp it from the tracker stage's PrimitiveOutput.tracks "
            "(runtime/session.py); if you built this pipeline by hand, stamp the ids or "
            "supply them on the detections."
        )
    note_unassociated_frame(ctx, stage, tracker_name, state=state)
    return ()


def reference_point(det: PipelineDetection) -> tuple[float, float]:
    """The normalized 0-1 point whose motion *is* the object's motion: the box centre.

    See the module docstring for why this is the centre and not one of the three foot
    points the legacy tree uses.  Kept a module function rather than a method so ``dwell``
    and a custom primitive can agree with this one without inheriting anything (``09`` §3).
    """
    box = det.bounding_box
    return ((box.xmin + box.xmax) * 0.5, (box.ymin + box.ymax) * 0.5)


def heading_degrees(dx: float, dy: float) -> float:
    """Direction of travel in degrees: 0 = east/right, counter-clockwise positive.

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
    return math.degrees(math.atan2(-dy, dx)) % 360.0


def heading_to_unit_vector(heading: float) -> tuple[float, float]:
    """The exact inverse of :func:`heading_degrees`: a heading back to a unit ``(dx, dy)``.

    Needed only by the ``heading_auto_learn_fallback`` estimator
    (:meth:`VelocityState._update_auto_learn`), which must average several tracks'
    *directions*, weighted by speed, to find the dominant one -- averaging two headings of,
    say, 350 and 10 degrees the naive way gives 180, the opposite of the two nearly-agreeing
    directions that produced it. Going back to vectors and averaging those is the same fix
    ``wrong_way_tracker.py``'s own estimator got for free by never leaving vector space.
    """
    theta = math.radians(heading)
    return math.cos(theta), -math.sin(theta)


def signed_heading_delta(heading: float, expected: float) -> float:
    """The smallest absolute angle between two headings, in degrees ``[0, 180]``.

    Wrapping done once, here: 350 vs 10 is 20 degrees apart, not 340.  Every legacy
    comparison of two angles in this tree either avoids the problem by using a dot product
    (``wrong_way_tracker.py``) or does not compare angles at all.
    """
    return abs(((heading - expected + 180.0) % 360.0) - 180.0)


@register(name="velocity_state")
class VelocityState:
    """Per-track speed, motion class, heading and wrong-way flag for one zone.

    Publishes exactly the four values
    :attr:`~matrice_analytics.engine.manifest.models.VelocityStateConfig.STATIC_OUTPUTS`
    declares, and the per-track detail on :attr:`~.base.PrimitiveOutput.tracks`:

    ==================== ==============================================================
    ``state``            Modal motion class across this frame's tracks, ``""`` if none.
    ``avg_speed``        Mean px/s over tracks that have a measurable speed.
    ``stationary_count`` Tracks below ``stationary_below_px_per_sec`` **this frame**.
    ``wrong_way_count``  Tracks moving against ``expected_heading_deg`` **this frame**.
    ==================== ==============================================================

    :meth:`window` re-reads two of those at window scope, which is not the same question, and
    adds ``stationary_count_peak`` so that the last and peak readings of that level have
    separate names.  ``wrong_way_count_last`` and ``wrong_way_count_peak`` do the same for the
    wrong-way gauge, which the window otherwise reports only as a count of distinct tracks --
    see its docstring (**PY-1**).
    """

    name: ClassVar[str] = "velocity_state"
    Config: ClassVar[type[VelocityStateConfig]] = VelocityStateConfig

    __slots__ = ("_auto_learn", "_bands", "_config", "_expected", "_state")

    def __init__(
        self,
        config: VelocityStateConfig,
        state: StateStore,
        *,
        geometry: SceneGeometry | None = None,
    ) -> None:
        """Bind a validated config to a state store already scoped to this stage.

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
        self._config = config
        self._state = state
        # Frozen at construction: dict ordering decides which band wins an exact boundary,
        # so it must not be re-read from a mutable config mid-run.
        self._bands: tuple[tuple[str, float, float], ...] = tuple(
            (name, float(bounds[0]), math.inf if bounds[1] is None else float(bounds[1]))
            for name, bounds in config.classes.items()
        )
        self._expected: float | None = self._resolve_expected(config, state, geometry)
        # Only live when heading_from_line found no line and heading_auto_learn_fallback
        # said that is acceptable -- a camera with a line, or one with no fallback set, never
        # sets this, and _update_auto_learn is never called. See the module docstring.
        self._auto_learn: bool = (
            config.heading_from_line
            and config.heading_auto_learn_fallback
            and self._expected is None
        )

    @staticmethod
    def _resolve_expected(
        config: VelocityStateConfig, state: StateStore, geometry: SceneGeometry | None
    ) -> float | None:
        """The expected heading, in ``[0, 360)``, or ``None`` when wrong-way is not evaluated.

        Sources, in the order checked (enforced mutually exclusive at manifest load by
        ``VelocityStateConfig._heading_source_is_one_thing``, so at most one of the first two
        branches below can ever be live for a given config):

        * ``expected_heading_deg`` -- a static angle authored in ``app.yaml``.
        * ``heading_from_line`` -- one drawn line's ``start -> end`` direction, resolved
          **once here, at construction**, exactly like ``line_crossing._setup_abline``
          pre-computes its trap zone's invariants once rather than per frame: the geometry
          does not change frame to frame, only the operator redrawing it does, and that is a
          session restart, not a frame.
        * ``heading_auto_learn_fallback`` -- when ``heading_from_line`` found *zero* lines and
          this is set, returns ``None`` here rather than raising: there is nothing to resolve
          yet, and :meth:`_update_auto_learn` will set :attr:`_expected` later, at runtime,
          once it has learned one. Two or more lines is still always an error -- the fallback
          is for "not drawn yet", not "which one did you mean" -- so that case falls through
          to the same :class:`GeometryError` as when no fallback is configured at all.
        """
        if config.expected_heading_deg is not None:
            return config.expected_heading_deg % 360.0
        if not config.heading_from_line:
            return None
        lines = resolve_geometry(state, geometry).lines
        if len(lines) == 1:
            (segment,) = lines.values()
            dx = segment.end[0] - segment.start[0]
            dy = segment.end[1] - segment.start[1]
            return heading_degrees(dx, dy)
        if len(lines) == 0 and config.heading_auto_learn_fallback:
            return None
        raise GeometryError(
            f"velocity_state stage {config.stage_name!r} uses heading_from_line: true, "
            f"which needs exactly 1 line drawn to have an unambiguous reference "
            f"direction; this camera has {len(lines)} "
            f"({', '.join(repr(n) for n in lines) or 'none'}). With more than one line, "
            "which is *the* reference direction is undefined -- draw exactly one line, from "
            "the point correct-direction traffic reaches first, to the point it reaches "
            "second -- or set expected_heading_deg instead. With no line at all, set "
            "heading_auto_learn_fallback: true to learn the direction from traffic instead "
            "of requiring one drawn."
        )

    # -- the frame ----------------------------------------------------------

    def process(self, ctx: FrameContext) -> PrimitiveOutput:
        """Measure every tracked object in this zone over the trailing window.

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
        tracked = require_track_ids(ctx, self.name, state=self._state)
        width, height = ctx.require_resolution(
            f"velocity_state stage {self._config.stage_name!r} "
            f"(stationary_below_px_per_sec={self._config.stationary_below_px_per_sec:g})"
        )
        samples: dict[int, list[list[float]]] = self._state.get("samples") or {}

        seen_now: set[int] = set()
        for track_id, det in tracked:
            if track_id in seen_now:
                # Two boxes, one id: the tracker is confused. Keep the first, deterministically.
                continue
            seen_now.add(track_id)
            nx, ny = reference_point(det)
            samples.setdefault(track_id, []).append([ctx.frame_ts, nx * width, ny * height])

        self._trim(samples, ctx.frame_ts)

        tracks: dict[int, TrackState] = {}
        speeds: list[float] = []
        class_counts: dict[str, int] = {}
        stationary_now = 0
        wrong_way_now = 0
        wrong_way_ids: dict[int, float] = self._state.get("wrong_way_ids") or {}
        # `expose_wrong_way_state` only: track_id -> "wrong_way" | "correct_way", for every
        # track with a DETERMINED heading state this frame. Populated only when the config
        # flag is set -- see the field's docstring for why an undetermined track (still
        # accumulating samples, or stationary/unknown) is left out rather than defaulted.
        directions: dict[int, str] = {}

        # heading_auto_learn_fallback only: (track_id, heading_deg, speed) for tracks with a
        # DETERMINED, moving heading this frame -- the same "not stationary/unknown" filter
        # _is_wrong_way itself applies, fed to _update_auto_learn once the per-track loop below
        # has finished computing every track's heading for this frame.
        auto_learn_observations: list[tuple[int, float, float]] = []

        entities = {track_id: det.entity for track_id, det in tracked}
        for track_id, path in samples.items():
            track, speed, heading, state, wrong = self._evaluate_track(
                ctx, track_id, path, entities.get(track_id, "")
            )
            tracks[track_id] = track
            if state:
                speeds.append(speed)
                class_counts[state] = class_counts.get(state, 0) + 1
            if state == STATIONARY:
                stationary_now += 1
            if wrong:
                wrong_way_now += 1
                wrong_way_ids.setdefault(track_id, ctx.frame_ts)
            # Shared by expose_wrong_way_state and heading_auto_learn_fallback: both only
            # ever act on a track whose heading test actually ran this frame -- see
            # _is_wrong_way's own STATIONARY/UNKNOWN_STATE exclusion.
            determined_moving = heading is not None and state not in (STATIONARY, UNKNOWN_STATE)
            if self._config.expose_wrong_way_state and determined_moving:
                directions[track_id] = "wrong_way" if wrong else "correct_way"
            if self._auto_learn and self._expected is None and determined_moving:
                auto_learn_observations.append((track_id, heading, speed))

        if self._auto_learn and auto_learn_observations:
            self._update_auto_learn(auto_learn_observations)

        self._state.set("samples", samples, lifetime=Lifetime.PERSISTENT)
        self._state.set("wrong_way_ids", wrong_way_ids, lifetime=Lifetime.WINDOW)
        self._state.set(
            "peak_stationary",
            max(int(self._state.get("peak_stationary") or 0), stationary_now),
            lifetime=Lifetime.WINDOW,
        )
        # Recorded next to the peak, and published under its own name: a WindowOutput goes out
        # verbatim, so `stationary_count` cannot answer both `agg_type: last` and `max`.
        self._state.set("last_stationary", stationary_now, lifetime=Lifetime.WINDOW)
        # `wrong_way_now` is a gauge of exactly the same shape, and it had no window name at all
        # until now -- `wrong_way_count` at window scope answers the identity question instead.
        # Both readings are recorded here so the window can publish them alongside it.
        self._state.set(
            "peak_wrong_way",
            max(int(self._state.get("peak_wrong_way") or 0), wrong_way_now),
            lifetime=Lifetime.WINDOW,
        )
        self._state.set("last_wrong_way", wrong_way_now, lifetime=Lifetime.WINDOW)

        values: dict[str, Scalar] = {
            "state": self._modal(class_counts),
            "avg_speed": sum(speeds) / len(speeds) if speeds else 0.0,
            "stationary_count": stationary_now,
            "wrong_way_count": wrong_way_now,
        }
        # `expose_wrong_way_state` alone drives wire_detections/live_category, the same
        # split line_crossing.expose_corridor_state uses -- this is the ONE way a track's
        # wrong-way flag (attributes["wrong_way"] above) becomes a box label instead of
        # per-track detail nobody downstream reads.
        wire_detections = None
        if self._config.expose_wrong_way_state:
            values["live_category.wrong_way"] = sum(
                1 for d in directions.values() if d == "wrong_way"
            )
            values["live_category.correct_way"] = sum(
                1 for d in directions.values() if d == "correct_way"
            )
            wire_detections = self._wrong_way_wire_detections(tracked, directions)

        return PrimitiveOutput(
            values=values,
            tracks=tracks,
            wire_detections=wire_detections,
        )

    @staticmethod
    def _wrong_way_wire_detections(
        tracked: tuple[tuple[int, PipelineDetection], ...], directions: Mapping[int, str]
    ) -> tuple[PipelineDetection, ...]:
        """``expose_wrong_way_state``'s wire override: relabel by heading state, not class.

        Split out of :meth:`process` (2026-08-25, alongside ``heading_auto_learn_fallback``)
        purely to keep that method under the org's function-length cap -- no behaviour change.

        EVERY tracked detection this frame is included, not just the ones in `directions`.
        `line_crossing.expose_corridor_state` can afford to publish only the matched subset
        because "not currently between the two lines" is a real, meaningful exclusion for a
        doorway counter. There is no equivalent exclusion here: a vehicle still accumulating
        its first `window_seconds` of samples, or classified stationary/unknown, is still a
        vehicle in frame and must keep showing on the overlay -- under its detected class, per
        this field's own docstring ("left unlabeled ... their detected class passes through
        unchanged"). An earlier version of this filtered down to `directions` only, which
        silently emptied the whole overlay on any frame with even one undetermined vehicle --
        caught by a synthetic run, not by inspection.
        """
        return tuple(
            det.model_copy(update={"category": directions[track_id]})
            if track_id in directions
            else det
            for track_id, det in tracked
        )

    def _evaluate_track(
        self, ctx: FrameContext, track_id: int, path: list[list[float]], entity: str
    ) -> tuple[TrackState, float, float | None, str, bool]:
        """One track's per-frame measurement, classification and wrong-way test.

        Split out of :meth:`process` (2026-08-25, alongside ``heading_auto_learn_fallback``)
        purely to keep that method under the org's function-length/branch caps -- this is a
        move, not a behaviour change; :meth:`process` still owns every loop-wide accumulator
        (``speeds``, ``class_counts``, ``directions``, ``auto_learn_observations``, ...),
        since those aggregate across tracks rather than describing one.

        Returns:
            ``(track, speed, heading, state, wrong)`` -- ``track.attributes`` already carries
            every per-track *output* (``heading_deg``, ``wrong_way``); the four scalars are
            returned alongside it only because :meth:`process` still needs them to update its
            own accumulators.
        """
        measured, heading = self._measure(path)
        state = self._classify(measured)
        speed = 0.0 if measured is None else measured
        attributes: dict[str, Scalar] = {"speed_px_s": speed, "samples": len(path)}
        if heading is not None:
            attributes["heading_deg"] = heading
        wrong = self._is_wrong_way(state, heading)
        attributes["wrong_way"] = int(wrong)
        track = TrackState(
            track_id=track_id,
            entity=entity,
            zone=ctx.zone or GLOBAL_ZONE,
            first_seen=path[0][0],
            last_seen=path[-1][0],
            state=state,
            attributes=attributes,
        )
        return track, speed, heading, state, wrong

    # -- measurement --------------------------------------------------------

    def _trim(self, samples: dict[int, list[list[float]]], now: float) -> None:
        """Drop samples older than the window, and tracks left with nothing.

        This is also the track-eviction policy: a track absent for
        ``window_seconds`` has no samples left and disappears.  There is deliberately no
        separate ``track_timeout`` knob here -- one window, one meaning.  ``dwell`` owns
        session lifetime, and owns the ``track_timeout_seconds`` that goes with it.
        """
        cutoff = now - self._config.window_seconds
        for track_id in list(samples):
            path = [s for s in samples[track_id] if s[0] >= cutoff]
            if path:
                samples[track_id] = path
            else:
                del samples[track_id]

    def _measure(self, path: Sequence[Sequence[float]]) -> tuple[float | None, float | None]:
        """Net-displacement speed in px/s and heading in degrees over one track's window.

        Returns:
            ``(speed, heading)``.  ``speed`` is ``None`` -- *not* ``0.0`` -- when the track
            has fewer than :data:`_MIN_SAMPLES` samples or they share a timestamp.  The
            distinction matters: a zero would be indistinguishable from a measured zero and
            :meth:`_classify` would call a track that has existed for one frame
            :data:`STATIONARY`, so every tracker reset would fill the zone with loiterers.
            ``heading`` is ``None`` when there is no speed, and also when the net
            displacement is exactly zero, which has no direction.
        """
        if len(path) < _MIN_SAMPLES:
            return None, None
        first, last = path[0], path[-1]
        elapsed = last[0] - first[0]
        if elapsed <= 0.0:
            return None, None
        dx = last[1] - first[1]
        dy = last[2] - first[2]
        distance = math.hypot(dx, dy)
        heading = None if distance == 0.0 else heading_degrees(dx, dy)
        return distance / elapsed, heading

    def _classify(self, speed: float | None) -> str:
        """Map a measured speed to a motion class name.

        :attr:`~matrice_analytics.engine.manifest.models.VelocityStateConfig.stationary_below_px_per_sec`
        **wins**, whatever ``classes`` says.  Two knobs that both mean "slow enough" is how
        the legacy tree ended up with ``velocity_threshold_px_per_sec`` and a
        ``classes``-like band table disagreeing inside one use case; here the dedicated knob
        is authoritative and ``classes`` only names the bands above it.  That is also what
        makes ``gate: {velocity_state: stationary}`` mean one thing.

        Args:
            speed: px/s, or ``None`` for "not measured yet" (see :meth:`_measure`).

        Returns:
            A band name, :data:`STATIONARY`, or :data:`UNKNOWN_STATE` when the speed is
            unmeasured or falls in no band.
        """
        if speed is None:
            return UNKNOWN_STATE
        if speed < self._config.stationary_below_px_per_sec:
            return STATIONARY
        for band, low, high in self._bands:
            if low <= speed < high:
                return band
        # Bands need not tile the number line; an unclassified speed is honestly unnamed
        # rather than forced into the nearest band.
        return UNKNOWN_STATE

    def _is_wrong_way(self, state: str, heading: float | None) -> bool:
        """Whether this track is travelling against ``expected_heading_deg``.

        A stationary or unclassified track is never wrong-way: its heading is the direction
        of a few pixels of jitter, and half of that jitter points backwards.  Requiring
        motion is what ``wrong_way_tracker.py:358-363`` spends a confidence integrator on.
        """
        if self._expected is None or heading is None:
            return False
        if state in (STATIONARY, UNKNOWN_STATE):
            return False
        return signed_heading_delta(heading, self._expected) > self._config.heading_tolerance_deg

    def _update_auto_learn(self, observations: Sequence[tuple[int, float, float]]) -> None:
        """Learn the expected heading from traffic when ``heading_from_line`` found no line.

        Port of ``wrong_way_tracker.py``'s ``_update_auto_reference``: accumulate a rolling
        buffer of ``(direction, speed)`` samples across tracks, cluster it into the two sides
        of its own weighted-average guess, and only trust that guess once one side dominates
        (:data:`_AUTO_LEARN_DOMINANCE_RATIO`) *and* keeps dominating for
        :data:`_AUTO_LEARN_STABILITY_FRAMES` frames running -- a single busy frame of
        cross-traffic must not flip the learned direction. Confirmation
        (:attr:`_expected` set) ends learning for good: :meth:`process` stops feeding this
        once :attr:`_expected` is no longer ``None``, so there is no periodic re-learning here
        the way the legacy ``AUTO`` source had -- a fixed, once-confirmed direction is the
        simpler answer, and this fallback exists for "no line yet", not for a traffic pattern
        that reverses over the life of the process.

        Args:
            observations: This frame's ``(track_id, heading_deg, speed_px_s)`` for tracks with
                a determined, moving heading -- see the call site in :meth:`process`.
        """
        learner: dict[str, Any] = self._state.get("auto_heading") or {
            "samples": [],
            "vector": None,
            "confidence": 0.0,
            "stable_frames": 0,
        }
        samples: list[list[float]] = learner["samples"]
        for track_id, heading, speed in observations:
            dx, dy = heading_to_unit_vector(heading)
            samples.append([dx, dy, speed, track_id])
        if len(samples) > _AUTO_LEARN_MAX_SAMPLES:
            del samples[: len(samples) - _AUTO_LEARN_MAX_SAMPLES]

        unique_tracks = {s[3] for s in samples}
        if len(unique_tracks) < _AUTO_LEARN_MIN_TRACKS:
            self._state.set("auto_heading", learner, lifetime=Lifetime.PERSISTENT)
            return

        sum_x = sum(s[0] * s[2] for s in samples)
        sum_y = sum(s[1] * s[2] for s in samples)
        guess_mag = math.hypot(sum_x, sum_y)
        if guess_mag < 1e-9:
            # No net direction at all -- e.g. perfectly balanced two-way traffic so far.
            self._state.set("auto_heading", learner, lifetime=Lifetime.PERSISTENT)
            return
        guess = (sum_x / guess_mag, sum_y / guess_mag)

        cluster_a_strength = cluster_b_strength = 0.0
        cluster_a: list[list[float]] = []
        cluster_b: list[list[float]] = []
        for s in samples:
            dot = s[0] * guess[0] + s[1] * guess[1]
            if dot >= 0:
                cluster_a.append(s)
                cluster_a_strength += s[2]
            else:
                cluster_b.append(s)
                cluster_b_strength += s[2]

        total_strength = cluster_a_strength + cluster_b_strength
        if total_strength < 1e-9:
            self._state.set("auto_heading", learner, lifetime=Lifetime.PERSISTENT)
            return
        dominance_ratio = max(cluster_a_strength, cluster_b_strength) / total_strength

        if dominance_ratio < _AUTO_LEARN_DOMINANCE_RATIO:
            # No side dominates yet (e.g. genuinely two-way traffic) -- the stability streak
            # must restart from here, the same way wrong_way_tracker.py does.
            learner["stable_frames"] = 0
            self._state.set("auto_heading", learner, lifetime=Lifetime.PERSISTENT)
            return

        dominant = cluster_a if cluster_a_strength >= cluster_b_strength else cluster_b
        dom_x = sum(s[0] * s[2] for s in dominant)
        dom_y = sum(s[1] * s[2] for s in dominant)
        dom_mag = math.hypot(dom_x, dom_y)
        if dom_mag < 1e-9:
            self._state.set("auto_heading", learner, lifetime=Lifetime.PERSISTENT)
            return
        dominant_direction = (dom_x / dom_mag, dom_y / dom_mag)

        previous_vector = learner["vector"]
        if previous_vector is None:
            blended = dominant_direction
        else:
            vx, vy = previous_vector
            blended = (
                _AUTO_LEARN_EMA_ALPHA * dominant_direction[0] + (1 - _AUTO_LEARN_EMA_ALPHA) * vx,
                _AUTO_LEARN_EMA_ALPHA * dominant_direction[1] + (1 - _AUTO_LEARN_EMA_ALPHA) * vy,
            )
        blend_mag = math.hypot(*blended)
        if blend_mag > 1e-9:
            blended = (blended[0] / blend_mag, blended[1] / blend_mag)
        learner["vector"] = list(blended)
        learner["confidence"] = min(
            1.0, learner["confidence"] + _AUTO_LEARN_CONFIDENCE_GAIN * dominance_ratio
        )
        learner["stable_frames"] += 1

        if (
            learner["confidence"] >= _AUTO_LEARN_CONFIRM_CONFIDENCE
            and learner["stable_frames"] >= _AUTO_LEARN_STABILITY_FRAMES
        ):
            self._expected = heading_degrees(blended[0], blended[1])
            logger.info(
                "velocity_state stage %r auto-learned expected heading %.1f deg from %d "
                "tracks (confidence=%.2f, dominance_ratio=%.2f) -- no line was drawn on this "
                "camera; heading_auto_learn_fallback supplied the reference direction instead.",
                self._config.stage_name,
                self._expected,
                len(unique_tracks),
                learner["confidence"],
                dominance_ratio,
            )

        self._state.set("auto_heading", learner, lifetime=Lifetime.PERSISTENT)

    @staticmethod
    def _modal(counts: Mapping[str, int]) -> str:
        """The most common motion class; a tie goes to the alphabetically first name.

        The tie-break is arbitrary but it must not be *incidental*: ranking by dict order
        would make this value depend on ``classes`` insertion order and, once a set got
        involved anywhere upstream, on ``PYTHONHASHSEED`` -- which is **PY-9**.  Sorting
        first makes two runs over the same frames agree, which is what the generated
        determinism test (**O5**) checks.
        """
        if not counts:
            return UNKNOWN_STATE
        return max(sorted(counts), key=lambda name: counts[name])

    # -- the window ---------------------------------------------------------

    def window(self, frames: Sequence[PrimitiveOutput]) -> WindowOutput:
        """Collapse the window.  Two of the four values change meaning here (**PY-1**).

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
        speeds = [
            float(frame.values.get("avg_speed", 0.0))
            for frame in frames
            if frame.values.get("state", UNKNOWN_STATE) != UNKNOWN_STATE
        ]
        state_frames: dict[str, int] = {}
        for frame in frames:
            label = str(frame.values.get("state", UNKNOWN_STATE))
            if label:
                state_frames[label] = state_frames.get(label, 0) + 1
        wrong_way_ids: Mapping[int, float] = self._state.get("wrong_way_ids") or {}
        return WindowOutput(
            values={
                "state": self._modal(state_frames),
                "avg_speed": sum(speeds) / len(speeds) if speeds else 0.0,
                "stationary_count": int(self._state.get("last_stationary") or 0),
                "stationary_count_peak": int(self._state.get("peak_stationary") or 0),
                "wrong_way_count": len(wrong_way_ids),
                "wrong_way_count_last": int(self._state.get("last_wrong_way") or 0),
                "wrong_way_count_peak": int(self._state.get("peak_wrong_way") or 0),
            }
        )

    def reset(self) -> None:
        """Clear window-scoped state only (``09`` §4 rule 2).

        ``samples`` is :attr:`Lifetime.PERSISTENT` and survives: a vehicle that has been
        stopped for fifty seconds when the window ticks is still stopped one second later,
        and re-deriving that would take another ``window_seconds`` of frames -- during which
        it would read :data:`UNKNOWN_STATE` and vanish from ``stationary_count``.
        """
        self._state.end_window()
