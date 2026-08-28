"""``dwell`` -- time-in-state per track, measured in frame time.

Normative source: ``_contracts/09-tobe-engine-architecture.md`` §3 and
``clauding/STAGE_BC_PLAN.md`` §2 (workstream B3).

Seventeen use cases implement a dwell clock privately and no two agree.  The survey found
three incompatible idioms:

* ``loitering_detection.py:977-1377`` -- ``presence_seconds += 1 / nominal_fps`` per frame.
  Correct only if inference runs on *every* frame at exactly the declared rate; on a
  skip-N pipeline it under-reports by a factor of N, silently.
* ``dwell_detection.py:756-999`` -- wall-clock from a parsed ``stream_time``, falling back
  to ``time.time()``.  The fallback is **PY-13**: a replayed hour of footage produces dwell
  times measured against the replay's wall clock, so a two-minute loiter in the recording
  reads as however long the replay took.
* ``parking_analytics_tracker.py:42`` -- ``last_seen_frame - first_seen_frame + 1``, a
  *span*.  A track seen at frame 0 and again at frame 9000 reports a five-minute dwell it
  never had.

This primitive does none of those.  Duration is accumulated from
:attr:`~.base.FrameContext.frame_ts` deltas, which is the only definition that survives
replay, backfill and a variable frame rate identically (**PY-13**).  There is no
``time.time()`` in this module and no ``fps`` arithmetic.

**The gap rule, and the one thing it is not.**  A gap between two satisfied frames is
credited to the session when it is shorter than ``track_timeout_seconds``, and ends the
session when it is longer.  That is one rule covering what the legacy tree spreads over a
frozen accumulator plus an ID-healing IoU match (loitering), an un-penalised 3-second stale
window (dwell detection), and nothing at all (parking).  A person walking behind a pillar
for two seconds is still standing there; a track id reused ten minutes later is a different
person.

The rule is an **occlusion** policy, and it now applies only to occlusion.  A gated
``dwell`` has two ways to stop being satisfied and they are not the same event:

* the track is **not in this frame at all** -- it is behind the pillar, the detector missed
  it, the tracker dropped it for a frame.  Nothing observed says the state ended, so the gap
  is credited: that is the rule above, and it is right.
* the track **is** in this frame and the state predicate or the gate says, in so many words,
  that it is somewhere else -- ``velocity_state`` measured it moving, ``state_machine`` lost
  its confirmation, the box landed outside the zone.  The state genuinely ended.  Crediting
  that gap is how a car that parks, **drives off for three seconds** and re-parks gets three
  seconds of *driving* counted as parked time, and how a 15-second
  ``threshold_seconds`` fires on two unrelated 10-second parks.  It was found in
  ``illegal_parking_detection``, a pure-config app, where nothing in the manifest could have
  revealed it (``_migration/wave-d1/group3-custom-logic/PORT_REPORT.md`` §5.1).  Legacy
  cleared the violation after ``violation_clear_sec`` of motion; this stage ends the session.

Not seen and seen-but-elsewhere are therefore separated, and a **third** case is separated
from both: *seen, and the gate has no opinion yet*.  A track that has just come back from an
occlusion has too little history for ``velocity_state`` to have measured it, so its state is
:data:`~.velocity_state.UNKNOWN_STATE` -- "we have not decided", which is not "it left".
Treating that as a departure would have thrown away the clock of every track occluded for
longer than the gate stage's own ``window_seconds``, i.e. broken the occlusion rule through
the gate.  An undecided frame neither accumulates nor ends: the session simply waits.  See
:meth:`Dwell._gate_verdict`.

**The gate is the point.**  ``gate: {velocity_state: stationary}`` on a ``dwell`` stage is
what turns ``loitering_detection.py`` -- 2,000 lines of EMA smoothing, jump clamping,
ratio-of-frames deques and ID healing -- into six lines of manifest.  See
:meth:`Dwell._gate_verdict` for how a gate is evaluated against
:attr:`~.base.FrameContext.previous`.

**Sessions are keyed by ``det.track_id``**, which the runtime stamps from the tracker stage
before this stage sees the frame (``runtime/session.py``).  When it is missing,
:func:`~.velocity_state.require_track_ids` decides whether that is an error or a counted
warning; what it may not be is a shrug, because a dwell clock with no ids never starts and
"nobody is loitering" is what an empty room looks like too.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping, Sequence
from typing import ClassVar, Final

from matrice_analytics.engine.contract.schemas import GLOBAL_ZONE, UNASSIGNED_ZONE
from matrice_analytics.engine.manifest.models import DwellConfig
from matrice_analytics.engine.primitives.base import (
    FrameContext,
    PrimitiveOutput,
    Scalar,
    TrackState,
    WindowOutput,
    register,
)
from matrice_analytics.engine.primitives.velocity_state import (
    STATIONARY,
    require_track_ids,
)
from matrice_analytics.engine.state import Lifetime, StateStore

__all__ = ["DWELLING", "OVER_THRESHOLD", "UNASSIGNED_ZONE", "Dwell", "DwellGateError"]

logger = logging.getLogger(__name__)


# :data:`UNASSIGNED_ZONE` is imported from ``contract/schemas.py``, not defined here.  This
# module used to declare its own copy of the literal and ``primitives/geometry.py`` declared a
# second; the bucket a no-match detection lands in is the value ``dwell`` must *exclude* from
# ``state: in_zone`` -- "unassigned" is the absence of a zone, and counting time spent there is
# how a camera with a mis-drawn polygon reports a full house (**PY-10**).  Two spellings of the
# id would have made this stage and ``zone_occupancy`` disagree about which detections are in a
# zone, silently, in the direction of over-reporting.  Re-exported for the stages that gate on
# it.  Never ``"__global__"`` (**PY-6**).

DWELLING: Final[str] = "dwelling"
"""Per-track label: a session past ``min_presence_seconds``, below ``threshold_seconds``."""

OVER_THRESHOLD: Final[str] = "over_threshold"
"""Per-track label: a session that has crossed ``threshold_seconds``.

A downstream stage gates on this string, the same way this stage gates on
:data:`~.velocity_state.STATIONARY`.
"""

# Session tuple layout, stored as a plain list so a durable backing can serialise it.
_START: Final[int] = 0
_LAST: Final[int] = 1
_SECONDS: Final[int] = 2

# Three-valued verdict for one track on one frame, from :meth:`Dwell._state_verdict` and
# :meth:`Dwell._gate_verdict`.  Two values would collapse "it is somewhere else" into "no
# reading yet", and those have opposite consequences for an open session: the first ends it,
# the second must leave it alone (see the module docstring).
_IN_STATE: Final[int] = 1
_LEFT_STATE: Final[int] = 0
_UNDECIDED: Final[int] = -1

#: PERSISTENT counter: frames on which ``state: in_zone`` ran in the ``global`` bucket of a
#: **zoned** app and therefore measured nothing.  By design (the per-zone pipelines do the
#: measuring) but not free of consequence -- a metric declared ``zone: global`` against this
#: stage reads 0 -- so it is counted and logged rather than either raised or ignored.
_GLOBAL_BUCKET_SKIPS: Final[str] = "in_zone_global_bucket_skips"


class DwellGateError(ValueError):
    """A ``dwell`` stage is configured against something the pipeline cannot supply.

    Raised for the three cases that would otherwise present as "the dwell metric is always
    zero", which is indistinguishable from a genuinely empty scene (``09`` §3):

    * ``state: in_zone`` on a pipeline that has **no zones at all**;
    * a ``gate:`` naming a stage that is not in the pipeline, or is not *before* this one;
    * ``state: stationary`` with no ``velocity_state`` stage and no explicit gate.

    Not raised for ``state: in_zone`` in the ``global`` bucket of a *zoned* app: a zoned app
    always runs that bucket as well, so raising there killed every session that combined
    ``state: in_zone`` with zones -- the combination the setting exists for.  See
    :meth:`Dwell._state_verdict`.
    """


@register(name="dwell")
class Dwell:
    """Time-in-state per track, aggregated over one zone.

    Publishes exactly the four values
    :attr:`~matrice_analytics.engine.manifest.models.DwellConfig.STATIC_OUTPUTS` declares:

    ======================== ==========================================================
    ``avg_seconds``          Mean session length over qualifying live sessions.
    ``max_seconds``          Longest qualifying live session.
    ``over_threshold_count`` Sessions past ``threshold_seconds`` **right now**.
    ``active_count``         Qualifying sessions not yet timed out.
    ======================== ==========================================================

    "Qualifying" means ``seconds >= min_presence_seconds`` -- the flicker suppressor.  A
    track that appears for two frames and vanishes never reaches it and never moves a
    number.

    "Live" means ``frame_ts - last_seen <= track_timeout_seconds``, so a session survives an
    occlusion and keeps counting through it.  ``active_count`` therefore includes the person
    currently behind the pillar, which is the honest answer to "how many are dwelling".

    :meth:`window` re-reads ``over_threshold_count`` at window scope, where it means
    something different, and publishes ``active_count_peak`` alongside ``active_count`` --
    plus ``over_threshold_count_last`` and ``over_threshold_count_peak``, which are the gauge
    this method computes every frame -- so that every reading has its own name and none of
    them depends on an ``agg_type`` the runtime does not apply.  See its docstring (**PY-1**).
    """

    name: ClassVar[str] = "dwell"
    Config: ClassVar[type[DwellConfig]] = DwellConfig

    __slots__ = ("_bucket", "_config", "_gate", "_state", "_zoned")

    def __init__(
        self,
        config: DwellConfig,
        state: StateStore,
        *,
        zoned: bool = False,
        bucket: str = GLOBAL_ZONE,
    ) -> None:
        """Bind a validated config to a state store already scoped to this stage.

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
        self._config = config
        self._state = state
        self._zoned = bool(zoned)
        self._bucket = bucket or GLOBAL_ZONE
        gate = dict(config.gate) if config.gate else {}
        if config.state == STATIONARY and not gate:
            gate = {"velocity_state": STATIONARY}
        self._gate: Mapping[str, str] = gate

    @property
    def _measures_nothing(self) -> bool:
        """This instance is ``state: in_zone`` in a bucket where no session can ever open.

        Two such buckets, and both used to publish a resolved ``0.0`` rather than nothing.

        ``unassigned`` is *the absence of a zone* (**PY-10**), so :meth:`_state_verdict` returns
        ``_LEFT_STATE`` for every track there.  It **is** an emission zone
        (``Session._resolve_emission_zones``), so its readings reach the wire: every window
        published one ``0`` row per dwell-sourced metric, forever, next to the real per-zone row.

        The ``global`` bucket of a **zoned** app is the same defect wearing a different hat.
        :meth:`_state_verdict` returns ``_UNDECIDED`` there and :meth:`_note_global_bucket_skip`
        already logs that "a metric declared ``zone: global`` against this stage will read 0
        forever" -- but the stage went on to publish that ``0`` anyway.  ``global`` is not an
        emission zone, so no row shipped; instead it fed two things that do read it: a
        ``zone: global`` metric, and every **metric-threshold incident**, which
        ``Session._active_for`` evaluates in the global bucket.  A threshold over an ``in_zone``
        dwell metric could therefore never fire on a zoned camera, and the alert that did not
        happen is indistinguishable from a quiet site.

        Unzoned is untouched: there ``global`` is the whole frame, an ``in_zone`` dwell against
        it is a manifest error, and :meth:`_state_verdict` still raises ``DwellGateError`` for
        it.  Silence here would hide that.

        Publishing nothing instead is the rule the rest of the engine already follows -- ``09``
        §3, "a metric that reads zero forever is indistinguishable from a quiet camera".  A
        value that is absent is skipped by ``window._build_metrics`` (``if value is None:
        continue``) rather than emitted, which is the whole point: the row disappears instead
        of lying.  ``unique_count`` and ``zone_occupancy`` still publish their ``unassigned``
        readings, and those are real -- a suddenly non-zero ``unassigned`` series is how an
        operator finds out a polygon is drawn wrong, and this does not take that away.
        """
        if self._config.state != "in_zone":
            return False
        return self._bucket == UNASSIGNED_ZONE or (self._zoned and self._bucket == GLOBAL_ZONE)

    # -- the frame ----------------------------------------------------------

    def process(self, ctx: FrameContext) -> PrimitiveOutput:
        """Advance every open session by this frame's elapsed time.

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
        if self._measures_nothing:
            # Before require_track_ids: a bucket that cannot measure must not also be the one
            # that raises "no tracker ran". The per-zone instances make that call.
            if self._zoned and self._bucket == GLOBAL_ZONE:
                # The short-circuit now returns before _state_verdict, which is where this used
                # to be counted. Keep the diagnostic: it is the one line that says a zoned app
                # is asking the whole-frame bucket a question only a zone can answer.
                self._note_global_bucket_skip(ctx)
            return PrimitiveOutput(values={}, tracks={})
        tracked = require_track_ids(ctx, self.name, state=self._state)
        sessions: dict[int, list[float]] = self._state.get("sessions") or {}
        crossed: dict[int, float] = self._state.get("crossed_ids") or {}

        satisfied: dict[int, str] = {}
        left: set[int] = set()
        for track_id, det in tracked:
            if track_id in satisfied:
                continue
            verdict = self._state_verdict(det.zone, ctx)
            if verdict == _IN_STATE:
                verdict = self._gate_verdict(ctx, track_id)
            if verdict == _IN_STATE:
                satisfied[track_id] = det.entity
                # Two boxes on one id, the first of which was out of state: any box in the
                # state satisfies, so the earlier verdict is withdrawn rather than left to
                # end a session this frame also accumulates.
                left.discard(track_id)
            elif verdict == _LEFT_STATE:
                left.add(track_id)

        self._end_left_state(sessions, left)
        self._accumulate(sessions, satisfied, ctx.frame_ts)
        self._reap(sessions, ctx.frame_ts)

        tracks: dict[int, TrackState] = {}
        durations: list[float] = []
        over_now = 0
        for track_id, session in sessions.items():
            seconds = session[_SECONDS]
            if seconds < self._config.min_presence_seconds:
                continue
            durations.append(seconds)
            over = seconds >= self._config.threshold_seconds
            if over:
                over_now += 1
                crossed.setdefault(track_id, ctx.frame_ts)
            attributes: dict[str, Scalar] = {
                "dwell_seconds": seconds,
                "over_threshold": int(over),
            }
            tracks[track_id] = TrackState(
                track_id=track_id,
                entity=satisfied.get(track_id, ""),
                zone=ctx.zone or GLOBAL_ZONE,
                first_seen=session[_START],
                last_seen=session[_LAST],
                state=OVER_THRESHOLD if over else DWELLING,
                attributes=attributes,
            )

        self._state.set("sessions", sessions, lifetime=Lifetime.PERSISTENT)
        self._state.set("crossed_ids", crossed, lifetime=Lifetime.WINDOW)
        self._state.set(
            "peak_active",
            max(int(self._state.get("peak_active") or 0), len(durations)),
            lifetime=Lifetime.WINDOW,
        )
        # The window publishes the peak *and* the last reading under two names; a WindowOutput is
        # published verbatim, so one name cannot serve `agg_type: last` and `agg_type: max` both.
        self._state.set("last_active", len(durations), lifetime=Lifetime.WINDOW)
        # `over_now` is the same shape of thing -- a gauge -- and until now it had no window name
        # at all, because `over_threshold_count` at window scope answers the *identity* question
        # instead. Recorded here so the window can publish both readings of the gauge without
        # re-deriving them from per-frame samples it is not given (`window()` receives the frames,
        # but the peak of a level must survive a `reset()` boundary the same way `peak_active`
        # does, and reading it from one place keeps the two consistent).
        self._state.set(
            "peak_over_threshold",
            max(int(self._state.get("peak_over_threshold") or 0), over_now),
            lifetime=Lifetime.WINDOW,
        )
        self._state.set("last_over_threshold", over_now, lifetime=Lifetime.WINDOW)

        return PrimitiveOutput(
            values={
                "avg_seconds": sum(durations) / len(durations) if durations else 0.0,
                "max_seconds": max(durations) if durations else 0.0,
                "over_threshold_count": over_now,
                "active_count": len(durations),
            },
            tracks=tracks,
        )

    # -- the clock ----------------------------------------------------------

    def _accumulate(
        self,
        sessions: dict[int, list[float]],
        satisfied: Mapping[int, str],
        now: float,
    ) -> None:
        """Credit each satisfied track with the time since it was last satisfied.

        A session is ``[start, last, seconds]``.  ``seconds`` is an accumulator, not
        ``last - start``: the difference is a track that leaves the state and comes back,
        where the span would silently include the absence
        (``parking_analytics_tracker.py:42``).

        The gap between two satisfied frames is credited when it is under
        ``track_timeout_seconds`` and restarts the session when it is over.  That single
        comparison is the occlusion policy, and it is *only* the occlusion policy: any frame
        in the gap on which the track was seen and decidedly out of the state has already
        ended the session in :meth:`_end_left_state`, so the gap this method can see spans
        frames where the track was absent or undecided.  The two used to be one code path,
        which credited three seconds of driving to a parking clock.
        """
        timeout = self._config.track_timeout_seconds
        for track_id in satisfied:
            session = sessions.get(track_id)
            if session is None:
                sessions[track_id] = [now, now, 0.0]
                continue
            gap = now - session[_LAST]
            if gap > timeout:
                # A different object wearing a recycled id, or a re-entry after a real
                # absence. Either way the old duration is not this one's.
                sessions[track_id] = [now, now, 0.0]
                continue
            if gap > 0.0:
                session[_SECONDS] += gap
            session[_LAST] = now

    def _end_left_state(self, sessions: dict[int, list[float]], left: set[int]) -> None:
        """End the session of every track that is **here** and is no longer in the state.

        The counterpart to :meth:`_reap`, and the distinction between them is the whole fix:
        :meth:`_reap` ends a session because the track has been *unseen* too long, which is a
        timeout; this ends one because the track was *seen somewhere else*, which is an
        observation and needs no timeout at all.  A car that pulls out of a bay is not parked
        one frame later, whatever ``track_timeout_seconds`` says.

        The session is dropped, not frozen.  Freezing it would keep a driving car in
        ``active_count`` and ``over_threshold_count`` for up to ``track_timeout_seconds``,
        which is the same over-report by a shorter route; and keeping the accumulator alive
        across a real departure would let two unrelated 10-second parks satisfy
        ``threshold_seconds: 15``.  ``crossed_ids`` is :attr:`Lifetime.WINDOW` and untouched
        here, so a track that *did* cross the threshold before it left still counts toward the
        window's distinct-crosser total -- the violation happened, and it is not un-happened by
        driving away.

        The part-frame between the last satisfied frame and this one is deliberately **not**
        credited: the state ended somewhere inside that interval and this stage cannot say
        where, so it does not guess in the direction that inflates the number.  At any real
        frame rate the difference is one frame interval.

        No hysteresis lives here.  One frame of "moving" ends a parking session, and that is
        safe because it is the *gate's* job to be sure: ``velocity_state`` measures net
        displacement over ``window_seconds`` rather than a per-frame delta (which is why a
        jittering box reads stationary), and ``state_machine`` has ``min_confirmation_frames``.
        Adding a second, private smoothing window here is exactly the duplication this engine
        replaced -- and it would have to be a new config field, which this primitive cannot
        introduce on its own.
        """
        for track_id in left:
            sessions.pop(track_id, None)

    def _reap(self, sessions: dict[int, list[float]], now: float) -> None:
        """Drop sessions whose track has been out of state past ``track_timeout_seconds``.

        Reaping on the *frame* clock rather than on a frame count is what makes this
        identical under replay: a 10-second timeout is ten seconds of footage whether the
        pipeline sampled it at 5 fps or 25.
        """
        timeout = self._config.track_timeout_seconds
        for track_id in list(sessions):
            if now - sessions[track_id][_LAST] > timeout:
                del sessions[track_id]

    # -- the predicate and the gate -----------------------------------------

    def _state_verdict(self, zone: str, ctx: FrameContext) -> int:
        """Whether a detection is in the state this stage measures -- in three values.

        ``present``      -- it was detected at all.  The stages before this one have already
                            filtered to the entities that matter.
        ``in_zone``      -- it is assigned to a real zone, not to the ``unassigned`` bucket.
        ``stationary``   -- desugared to a gate in :meth:`__init__`, so the presence test
                            here is the same as ``present`` and the motion test happens in
                            :meth:`_gate_verdict`.

        :data:`_LEFT_STATE` rather than a plain ``False`` for the ``unassigned`` bucket under
        ``in_zone``: the detection is *here* and it is demonstrably not in a zone, which ends
        an open session (:meth:`_end_left_state`) instead of leaving the gap to be credited.
        Note that in a *zoned* app a track that walks out of a zone leaves that zone's bucket
        altogether -- the runtime partitions the detections before the pipeline runs -- so it
        reaches this stage as an absence and the occlusion rule applies.  This branch is the
        one case where the detection is in the bucket and out of the state.

        **The ``global`` bucket under ``state: in_zone``.**  A zoned app runs the ``global``
        bucket *as well as* one pipeline per zone -- by design: metrics declared
        ``zone: global`` read it and incidents are evaluated against it
        (``runtime/session.py``).  This method used to raise there, which meant
        ``state: in_zone`` could not coexist with zones at all: nothing wraps a primitive in a
        ``try``, so the first frame of the first zoned app killed the session.  It now
        **skips** that bucket -- :data:`_UNDECIDED`, so nothing accumulates *and* nothing is
        ended, because a bucket that declines to measure must not be the reason a session
        dies -- and lets the per-zone pipelines do the measuring, which is where a per-zone
        question is answered.  ``global`` is deliberately *not* treated as "any zone": the global
        bucket's detections are stamped ``zone: "global"`` -- the partition's zone stamp lands
        on the per-zone copies (``geometry.assign_detections_to_zones``) -- so "any zone"
        would have to mean "every detection including the ones in no zone", which
        over-reports exactly the way **PY-10** describes.

        The skip is counted and logged, because a metric declared ``zone: global`` against
        this stage does read 0 and somebody has to be able to find out why.

        Raises:
            DwellGateError: ``state: in_zone`` on a pipeline that is **not zoned at all**.
                Failing loudly beats publishing zero forever: with no partition, "time in
                zone" has no referent, and the app author needs to know that on the first
                frame and not from a flat dashboard a week later (``09`` §5).

                ``ctx.zone_config`` separates the two causes, which have different fixes: the
                camera genuinely has no polygons (fix the installation, or use
                ``state: 'present'``), or it has them and this app never opted into zones --
                add a ``zones:`` block or a ``zone_occupancy`` stage, which is what makes the
                runtime partition (``Session._resolve_zones``).
        """
        if self._config.state != "in_zone":
            return _IN_STATE
        if ctx.zone == GLOBAL_ZONE:
            if self._zoned:
                self._note_global_bucket_skip(ctx)
                return _UNDECIDED
            drawn = sorted(ctx.zone_config.zones) if ctx.zone_config else []
            raise DwellGateError(
                f"dwell.state is 'in_zone' but this pipeline runs only the {GLOBAL_ZONE!r} "
                "bucket, so time-in-zone has nothing to measure and every value here would "
                "be 0 for the life of the process. "
                + (
                    f"Camera {ctx.camera_id!r} does have zones drawn "
                    f"({', '.join(repr(z) for z in drawn)}), so this app did not opt into "
                    "them -- add a `zones:` block (or a zone_occupancy stage) to the "
                    "manifest and the runtime will run one pipeline per zone."
                    if drawn
                    else "No zones are drawn on this camera. Draw zones in the streaming UI, "
                    "or use dwell.state: 'present'."
                )
            )
        return _IN_STATE if zone not in (GLOBAL_ZONE, UNASSIGNED_ZONE) else _LEFT_STATE

    def _note_global_bucket_skip(self, ctx: FrameContext) -> None:
        """Count the skipped ``global`` frames and say so, on a decelerating schedule."""
        count = self._state.incr(_GLOBAL_BUCKET_SKIPS, 1, lifetime=Lifetime.PERSISTENT)
        if count in (1.0, 10.0) or count % 1_000 == 0:
            logger.warning(
                "dwell stage %r has state: 'in_zone' and is also running in the %r bucket, "
                "which a zoned app always runs; that bucket measures nothing and now publishes "
                "nothing (frame %d of it since process start). The per-zone pipelines carry the "
                "real numbers -- read them with a metric declared zone: per_zone. A metric "
                "declared zone: global against this stage emits no row at all, and a "
                "metric-threshold incident over one can never fire, because thresholds are "
                "evaluated in this bucket.",
                self._config.stage_name,
                GLOBAL_ZONE,
                int(count),
            )

    def _gate_verdict(self, ctx: FrameContext, track_id: int) -> int:
        """Whether every gate condition holds for this track, this frame -- in three values.

        A gate entry is ``<stage name>: <required state>``.  It is checked in two places, in
        order:

        1. that stage's :attr:`~.base.PrimitiveOutput.tracks` entry for this track id --
           the per-object answer, which is what ``velocity_state`` publishes;
        2. failing that, the stage's ``values["state"]`` -- the zone-level answer, which is
           what ``state_machine`` publishes.

        The fallback is what lets one gate syntax cover both "*this* person is stationary"
        and "the zone is confirmed occupied", without a second key in the manifest.

        **Closed is not one thing.**  Both :data:`_LEFT_STATE` and :data:`_UNDECIDED` keep the
        clock from *running* -- neither one is "in state" -- and they differ only in what they
        do to a session that is already open:

        ``_LEFT_STATE``   the stage named a state, and it is not the wanted one.  A positive
                          reading of something else: the car is ``moving``, the zone went back
                          to ``empty``.  The dwell ended (:meth:`_end_left_state`).
        ``_UNDECIDED``    the stage has **no reading** for this track -- no ``tracks`` entry
                          for the id, or an entry whose state is the empty string, which is
                          how :data:`~.velocity_state.UNKNOWN_STATE` spells "not measured
                          yet", or no zone-level ``state`` value at all.  Nothing observed
                          says the dwell ended, so an open session is left alone and the
                          occlusion rule still owns the gap.

        That second row is what keeps the gate from breaking the occlusion policy it sits on
        top of.  ``velocity_state`` evicts a track's samples after its own ``window_seconds``,
        so a person who reappears from behind a pillar after four seconds has one sample and
        no measurable speed -- ``UNKNOWN_STATE`` -- for the next few frames.  Reading that as
        "she left" would delete a clock the occlusion rule exists to preserve, and it would
        happen on every occlusion longer than the *gate's* window rather than the one
        ``track_timeout_seconds`` names.

        A stage that publishes tracks but has none for this id therefore keeps the gate shut
        without ending anything.  Shut is still deliberate: "the velocity stage has no opinion
        about this track" is not "this track is stationary", and treating it as such is how a
        track that has just appeared starts a loitering clock.

        With more than one gate entry the verdict is order-independent, because dict order is
        the manifest's insertion order and no output may depend on it (**PY-9**): any single
        ``_LEFT_STATE`` decides the frame, otherwise any ``_UNDECIDED`` does, otherwise every
        entry held.

        Raises:
            DwellGateError: The gated stage is not in :attr:`~.base.FrameContext.previous`.
                Either it is missing from the pipeline or it is declared *after* this one,
                and in both cases the gate would silently never open.
        """
        verdict = _IN_STATE
        for stage, wanted in self._gate.items():
            output = ctx.previous.get(stage)
            if output is None:
                raise DwellGateError(
                    f"dwell.gate names stage {stage!r}, which has not run before this "
                    f"stage. Stages available here: "
                    f"{', '.join(sorted(ctx.previous)) or '(none)'}. Add it to the "
                    f"pipeline above the dwell stage -- a gate on a stage that never runs "
                    f"never opens, and this dwell would report 0 forever. "
                    + (
                        "This gate is implied by dwell.state: 'stationary'; add a "
                        "`- velocity_state:` stage, or set gate: explicitly to name a "
                        "velocity_state stage that carries a custom `name:`."
                        if self._config.gate is None
                        else ""
                    )
                )
            track_state = output.tracks.get(track_id)
            if track_state is not None:
                if track_state.state == wanted:
                    continue
                # An empty state is UNKNOWN_STATE: the stage has this track and has not
                # decided about it. Everything else is a named, contradictory reading.
                if not track_state.state:
                    verdict = _UNDECIDED
                    continue
                return _LEFT_STATE
            if not output.tracks:
                zone_state = output.values.get("state")
                if zone_state is not None and str(zone_state) == wanted:
                    continue
                if zone_state is None or not str(zone_state):
                    verdict = _UNDECIDED
                    continue
                return _LEFT_STATE
            # The stage published tracks and none of them is this one: no opinion about it.
            verdict = _UNDECIDED
        return verdict

    # -- the window ---------------------------------------------------------

    def window(self, frames: Sequence[PrimitiveOutput]) -> WindowOutput:
        """Collapse the window.  ``over_threshold_count`` changes meaning here (**PY-1**).

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
        if self._measures_nothing:
            return WindowOutput(values={})
        active_frames = [frame for frame in frames if int(frame.values.get("active_count", 0)) > 0]
        averages = [float(frame.values.get("avg_seconds", 0.0)) for frame in active_frames]
        maxima = [float(frame.values.get("max_seconds", 0.0)) for frame in frames]
        crossed: Mapping[int, float] = self._state.get("crossed_ids") or {}
        return WindowOutput(
            values={
                "avg_seconds": sum(averages) / len(averages) if averages else 0.0,
                "max_seconds": max(maxima) if maxima else 0.0,
                "over_threshold_count": len(crossed),
                "over_threshold_count_last": int(self._state.get("last_over_threshold") or 0),
                "over_threshold_count_peak": int(self._state.get("peak_over_threshold") or 0),
                "active_count": int(self._state.get("last_active") or 0),
                "active_count_peak": int(self._state.get("peak_active") or 0),
            }
        )

    def reset(self) -> None:
        """Clear window-scoped state only (``09`` §4 rule 2).

        ``sessions`` is :attr:`Lifetime.PERSISTENT` and **survives**.  This is the whole
        reason the lifetime enum exists: a person still standing there when the window ticks
        keeps their clock.  Clearing it would cap every measurable dwell at 60 seconds and
        make ``threshold_seconds: 90`` unreachable -- a manifest the schema accepts and the
        runtime could never satisfy.
        """
        self._state.end_window()
