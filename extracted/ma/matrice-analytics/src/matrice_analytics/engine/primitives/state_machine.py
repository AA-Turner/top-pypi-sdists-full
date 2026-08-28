"""``state_machine`` -- N-of-M temporal confirmation with recovery hysteresis.

Normative source: ``_contracts/09-tobe-engine-architecture.md`` §3 and
``clauding/STAGE_BC_PLAN.md`` §2 (workstream B3).

Ported from the two places the legacy tree already gets this roughly right, which do not
know about each other:

* ``analytics/incident_lifecycle.py`` -- the zone-level confirm/decay machine.  A severity
  must hold for ``consecutive_frames_default`` frames before it is published, and an
  incident stays open for ``consecutive_frames_empty`` clear frames after the last
  detection.  That second number is the recovery hysteresis, spelled as a cooldown.
* ``analytics/base_processor.py:258-292`` -- per-track soft decay.  A one-frame miss
  decrements the counter by 1 instead of resetting it, "so a brief occlusion does not force
  the track to re-qualify from scratch".

Both halves are here, because the difference between them is only *what* is being confirmed:

**Zone level** is the primary machine and drives the three published values.  The condition
is "this zone has any detections this frame" -- the pipeline has already entity-remapped
and zone-partitioned, so a stage placed after a ``detect`` that filters to ``person`` is
confirming "a person is present", and one placed after a ``ratio_compliance`` is confirming
"the compliance stage saw its subjects".

**Per track**, opportunistically, when detections carry tracker ids.  Unlike ``dwell`` and
``velocity_state``, :class:`~matrice_analytics.engine.manifest.models.StateMachineConfig`
declares **no** ``REQUIRES``, so a manifest may legally run this stage with no ``track:``
before it.  Demanding a tracker here would reject manifests the schema accepts, so the
per-track counters are a bonus on :attr:`~.base.PrimitiveOutput.tracks` rather than a
precondition.

⚠ **PY-11.**  ``confirm_frames`` below 3 is rejected by
:func:`~matrice_analytics.engine.manifest.models._validate_confirm_frames` at manifest load.
There is deliberately **no** ``max(3, value)`` anywhere in this file.  The old engine
clamped it (``base_processor.py:78``) so the manifest said one thing and the runtime did
another; the author believed a value that never ran.  If a config reaches here with
``confirm_frames < 3`` that is a manifest-layer bug to fix there, not to paper over here.

There is no clock in this module: confirmation is counted in frames, and
:attr:`~.base.FrameContext.frame_ts` is carried onto the per-track state so a downstream
stage can convert (**PY-13**).
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar, Final

from matrice_analytics.engine.contract.schemas import GLOBAL_ZONE
from matrice_analytics.engine.manifest.models import StateMachineConfig
from matrice_analytics.engine.primitives.base import (
    FrameContext,
    PrimitiveOutput,
    TrackState,
    WindowOutput,
    register,
)
from matrice_analytics.engine.state import Lifetime, StateStore

__all__ = [
    "CONFIRMED",
    "IDLE",
    "PENDING",
    "RECOVERING",
    "StateMachine",
]


IDLE: Final[str] = "idle"
"""Nothing seen, nothing pending.  The resting state."""

PENDING: Final[str] = "pending"
"""Evidence is accumulating but has not reached ``confirm_frames``."""

CONFIRMED: Final[str] = "confirmed"
"""Confirmed **and** holding this frame."""

RECOVERING: Final[str] = "recovering"
"""Confirmed, but the condition has gone away and ``recovery_frames`` is counting down.

Distinct from :data:`CONFIRMED` on purpose.  ``active`` is still 1 -- that is what
hysteresis *means* -- but an operator watching a state flip between "confirmed" and
"recovering" is watching a flapping detector, and the old machine's single ``incident_active``
boolean hid exactly that.
"""


@register(name="state_machine")
class StateMachine:
    """N-of-M confirmation with asymmetric recovery, for one zone.

    Publishes exactly the four values
    :attr:`~matrice_analytics.engine.manifest.models.StateMachineConfig.STATIC_OUTPUTS`
    declares:

    ==================== ==============================================================
    ``state``            :data:`IDLE` / :data:`PENDING` / :data:`CONFIRMED` / :data:`RECOVERING`.
    ``active``           ``1`` while confirmed, including through recovery.  ``0`` otherwise.
    ``confirmed_frames`` The current evidence counter, capped at ``confirm_frames``.
    ``confirmed_new``    ``1`` on the frame the machine newly reaches CONFIRMED, else ``0``.
    ==================== ==============================================================

    :meth:`window` publishes those four plus ``confirmed_frames_peak``, so the counter's
    current value and its window high-water mark have separate names rather than depending on a
    ``metrics[].agg_type`` the runtime deliberately does not apply. ``confirmed_new`` at window
    scope is the *count* of confirm transitions this window (summed, like ``unique_count.new``),
    not a 0/1 flag -- see the field's note on
    :attr:`~matrice_analytics.engine.manifest.models.StateMachineConfig.STATIC_WINDOW_OUTPUTS`
    for why this is the primitive an episode-counting app should reach for when there is no
    object identity to run ``unique_count`` against.

    The counter is asymmetric by design:

    * **rise** -- ``+1`` per frame the condition holds, capped at ``confirm_frames``.
    * **soft decay** (default) -- ``-1`` per clear frame while still unconfirmed.  One
      dropped frame must not discard four frames of evidence.
    * **hard decay** -- back to ``0`` on the first clear frame.  For conditions where a
      single gap genuinely invalidates the evidence.
    * **recovery** -- once confirmed, the counter stops mattering; ``recovery_frames``
      *consecutive* clear frames drop it.  Any frame in which the condition holds resets
      that countdown.

    Example:
        With ``confirm_frames: 5, recovery_frames: 3, decay: soft`` and a condition that
        holds for frames 1-4, misses frame 5, then holds for 6-7::

            frame  1  2  3  4  5  6  7
            hits   1  2  3  4  3  4  5
            active 0  0  0  0  0  0  1

        With ``decay: hard`` the same sequence never confirms: frame 5 resets to 0.
    """

    name: ClassVar[str] = "state_machine"
    Config: ClassVar[type[StateMachineConfig]] = StateMachineConfig

    __slots__ = ("_config", "_state")

    def __init__(self, config: StateMachineConfig, state: StateStore) -> None:
        """Bind a validated config to a state store already scoped to this stage.

        Args:
            config: The validated ``state_machine:`` block.  ``confirm_frames`` is taken
                **as written** -- see the PY-11 note in the module docstring.
            state: Scoped to ``<camera_id>/<app_id>/<zone>/<stage>`` by the runtime.
        """
        self._config = config
        self._state = state

    # -- the frame ----------------------------------------------------------

    def process(self, ctx: FrameContext) -> PrimitiveOutput:
        """Advance the machine by one frame.

        Args:
            ctx: This frame, in this zone.  The condition is
                ``len(ctx.detections) > 0`` -- whatever the stages before this one left in
                the zone.

        Returns:
            The three declared values, plus a :class:`~.base.TrackState` per tracked object
            carrying that object's own counter and state.
        """
        holds = bool(ctx.detections)
        was_confirmed = bool(self._state.get("confirmed") or False)
        hits, clear_run, confirmed = self._advance(
            hits=int(self._state.get("hits") or 0),
            clear_run=int(self._state.get("clear_run") or 0),
            confirmed=was_confirmed,
            holds=holds,
        )
        self._state.set("hits", hits, lifetime=Lifetime.PERSISTENT)
        self._state.set("clear_run", clear_run, lifetime=Lifetime.PERSISTENT)
        self._state.set("confirmed", confirmed, lifetime=Lifetime.PERSISTENT)

        state = self._label(hits, confirmed, holds)
        # An event, not a level: exactly one frame per episode reads 1, the same shape as
        # unique_count.new -- see the class docstring and the STATIC_WINDOW_OUTPUTS note.
        confirmed_new = confirmed and not was_confirmed
        if confirmed:
            self._state.incr("active_frames", 1, lifetime=Lifetime.WINDOW)
        if confirmed_new:
            self._state.incr("confirmed_new_count", 1, lifetime=Lifetime.WINDOW)
        self._state.set(
            "peak_hits",
            max(int(self._state.get("peak_hits") or 0), hits),
            lifetime=Lifetime.WINDOW,
        )

        return PrimitiveOutput(
            values={
                "state": state,
                "active": int(confirmed),
                "confirmed_frames": hits,
                "confirmed_new": int(confirmed_new),
            },
            tracks=self._advance_tracks(ctx),
        )

    def _advance(self, *, hits: int, clear_run: int, confirmed: bool, holds: bool) -> tuple[int, int, bool]:
        """One step of the counter.  Pure, so the table in the class docstring is testable.

        Args:
            hits: The evidence counter entering this frame.
            clear_run: Consecutive clear frames entering this frame.  Only meaningful once
                ``confirmed``.
            confirmed: Whether the state is currently held.
            holds: Whether the condition holds this frame.

        Returns:
            ``(hits, clear_run, confirmed)`` leaving this frame.
        """
        target = self._config.confirm_frames
        if holds:
            hits = min(target, hits + 1)
            clear_run = 0
            if hits >= target:
                confirmed = True
            return hits, clear_run, confirmed

        if confirmed:
            clear_run += 1
            if clear_run >= self._config.recovery_frames:
                return 0, 0, False
            return hits, clear_run, True

        # Not yet confirmed: this is the soft/hard decision (base_processor.py:265-272).
        hits = max(0, hits - 1) if self._config.decay == "soft" else 0
        return hits, 0, False

    @staticmethod
    def _label(hits: int, confirmed: bool, holds: bool) -> str:
        """Name the four positions of the machine."""
        if confirmed:
            return CONFIRMED if holds else RECOVERING
        return PENDING if hits > 0 else IDLE

    # -- per-track (opportunistic) ------------------------------------------

    def _advance_tracks(self, ctx: FrameContext) -> dict[int, TrackState]:
        """Run the same counter per tracker id, when there are tracker ids.

        This is ``base_processor.py:258-292`` -- soft-decay track confirmation -- with the
        decay rule taken from config instead of hardcoded, and with the counters in the
        state store instead of two instance dicts.

        Returns an empty mapping when nothing is tracked; that is the documented "no
        ``track:`` stage" case, not an error (see the module docstring).
        """
        present = {det.track_id: det for det in ctx.detections if det.track_id is not None}
        counters: dict[int, list[float]] = self._state.get("track_counters") or {}
        if not present and not counters:
            return {}

        target = self._config.confirm_frames
        tracks: dict[int, TrackState] = {}
        for track_id in present:
            row = counters.get(track_id)
            if row is None:
                # [hits, first_seen, last_seen] -- frame time, never wall-clock (PY-13).
                counters[track_id] = [1.0, ctx.frame_ts, ctx.frame_ts]
            else:
                row[0] = min(target, row[0] + 1)
                row[2] = ctx.frame_ts

        for track_id in list(counters):
            if track_id in present:
                continue
            row = counters[track_id]
            row[0] = max(0.0, row[0] - 1) if self._config.decay == "soft" else 0.0
            if row[0] <= 0.0:
                del counters[track_id]

        for track_id, row in counters.items():
            hits = int(row[0])
            det = present.get(track_id)
            tracks[track_id] = TrackState(
                track_id=track_id,
                entity=det.entity if det is not None else "",
                zone=ctx.zone or GLOBAL_ZONE,
                first_seen=row[1],
                last_seen=row[2],
                state=self._label(hits, hits >= target, track_id in present),
                attributes={"confirmed_frames": hits, "active": int(hits >= target)},
            )
        self._state.set("track_counters", counters, lifetime=Lifetime.PERSISTENT)
        return tracks

    # -- the window ---------------------------------------------------------

    def window(self, frames: Sequence[PrimitiveOutput]) -> WindowOutput:
        """Collapse the window.  ``active`` changes meaning here (**PY-1**).

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
        active_frames = int(self._state.get("active_frames") or 0)
        peak = int(self._state.get("peak_hits") or 0)
        # `hits` is PERSISTENT and is therefore literally the current counter -- the honest
        # "last" reading, and unlike `frames[-1]` it is right when the runtime capped retention.
        current = int(self._state.get("hits") or 0)
        last_state = str(frames[-1].values.get("state", IDLE)) if frames else IDLE
        # Read from the WINDOW counter, not summed from `frames`, for the same reason
        # unique_count.window() reads its own counter: the runtime caps how many per-frame
        # outputs it retains, and the counter is still correct when frames is truncated.
        confirmed_new = int(self._state.get("confirmed_new_count") or 0)
        return WindowOutput(
            values={
                "state": last_state,
                "active": int(active_frames > 0),
                "confirmed_frames": current,
                "confirmed_frames_peak": peak,
                "confirmed_new": confirmed_new,
            }
        )

    def reset(self) -> None:
        """Clear window-scoped state only (``09`` §4 rule 2).

        ``hits``, ``clear_run``, ``confirmed`` and ``track_counters`` are
        :attr:`Lifetime.PERSISTENT` and survive.  A state confirmed at second 59 is still
        confirmed at second 61; re-qualifying from scratch every minute would make
        ``confirm_frames`` mean "per window", which no manifest says.
        """
        self._state.end_window()
