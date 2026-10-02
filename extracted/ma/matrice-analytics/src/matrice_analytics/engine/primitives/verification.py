"""``verification`` -- hold an alert candidate until the VSS VLM confirms it.

Normative source: ``VLM-VERIFY-INTERFACES.md`` §3.  The server side is ``POST /vss/verify``.

**Non-blocking by construction.**  A VLM call costs 3-7 s and serialises on Thor, while
:meth:`Verification.process` runs once per frame per zone bucket at up to 25 fps.  So this stage
never waits: it *submits* a job to the engine-owned worker (``engine/verify``) on a candidate
frame and *applies* the verdict on a later one.  The stage itself does no I/O and spawns
nothing -- the one sanctioned thread lives in the worker (see the note beside the "no threads"
rule in ``base.py``).

The state machine, per bucket, every key :attr:`Lifetime.PERSISTENT` and every duration from
:attr:`FrameContext.frame_ts` (**PY-13**)::

    IDLE --candidate--> submit --> PENDING --verdict--> CONFIRMED | COOLDOWN | IDLE
    CONFIRMED --clear_after_quiet_seconds with no candidate--> IDLE
    COOLDOWN  --cooldown_seconds--> IDLE, or a candidate above the rejected level re-submits

Suppression is what makes the feature affordable: without PENDING the stage would ask the same
question ~150 times before the first answer lands, and the worker's drop-oldest queue would
throw the real alerts away.  ``PERSISTENT`` rather than ``WINDOW`` because a window-scoped
cooldown would clear at every 60 s boundary and a rejected alert would come back once a minute.
"""

from __future__ import annotations

import dataclasses
import logging
import re
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, ClassVar, Final

from matrice_analytics.engine.manifest.models import VerificationConfig
from matrice_analytics.engine.primitives.base import (
    FrameContext,
    PrimitiveEvent,
    PrimitiveOutput,
    Scalar,
    WindowOutput,
    register,
    resolve_value,
)
from matrice_analytics.engine.state import Lifetime, StateStore

if TYPE_CHECKING:  # the worker package is engine-owned and imported lazily (see _bound_worker)
    from matrice_analytics.engine.verify import Verdict, VerificationWorker

__all__ = [
    "CONFIRMED",
    "COOLDOWN",
    "IDLE",
    "PENDING",
    "Verification",
    "VerificationSourceError",
]

logger = logging.getLogger(__name__)

IDLE: Final[str] = "idle"
PENDING: Final[str] = "pending"
CONFIRMED: Final[str] = "confirmed"
COOLDOWN: Final[str] = "cooldown"

#: 2020-01-01T00:00:00Z.  The server rejects anything earlier (422): such a ``frame_ts`` is a
#: stream-relative clock (``has_absolute_time: false``) with no recording hour to look up.
_EPOCH_2020: Final[float] = 1_577_836_800.0
_RTP_MAX: Final[int] = 2**32 - 1
_OBJECT_ID: Final[re.Pattern[str]] = re.compile(r"^[0-9a-fA-F]{24}$")

# State keys (all PERSISTENT).
_STATE = "state"
_SINCE = "since"  # frame_ts the current state was entered
_QUIET_SINCE = "quiet_since"  # last candidate while CONFIRMED (or the confirm itself)
_PENDING_LEVEL = "pending_level"  # source value that was submitted
_COOLDOWN_LEVEL = "cooldown_level"  # the level a COOLDOWN was entered at (escalation bar)
_VOTES_CONFIRMED = "votes_confirmed"
_VOTES_TOTAL = "votes_total"
_WARNED = "warned_unsendable"  # last unsendable reason logged, so 25 fps does not spam

_FLAG_KEYS: Final[tuple[str, ...]] = (
    "verified",
    "verification_pending",
    "verification_suppressed",
    "verification_rejected",
    "verification_dropped",
    "verification_skipped",
)
_FINAL_BY_POLICY: Final[frozenset[str]] = frozenset({"unverifiable", "unavailable", "bad_request"})


class VerificationSourceError(ValueError):
    """``verification.source`` resolved to a value that is not a number.

    A string (``incident_quantise.level``, say) cannot be compared with ``above``; treating it as
    zero would make the stage silently never verify anything, so it raises instead (``09`` §3).
    """


@dataclasses.dataclass(slots=True)
class _Flags:
    """What happened on this one frame; never stored."""

    suppressed: bool = False
    rejected: bool = False
    dropped: bool = False
    skipped: bool = False
    policy_pass: bool = False


@register(name="verification")
class Verification:
    """``verification`` -- gate (or shadow) a candidate on a VLM verdict, for one bucket.

    Outputs, every frame, zeros included: ``verified_rank``, ``verified``,
    ``verification_pending``, ``verification_suppressed``, ``verification_rejected``,
    ``verification_dropped``, ``verification_skipped``, ``verification_votes_confirmed``,
    ``verification_votes_total`` (see
    :attr:`~matrice_analytics.engine.manifest.models.VerificationConfig.STATIC_OUTPUTS`).

    On a *passing* frame every event the source stage raised under its own name is re-raised
    under this stage's name, so ``severity_from: <this stage>`` works exactly like
    ``severity_from: incident_quantise``.

    The mailbox is ``state.prefix`` -- ``<camera>/<app>/<bucket>/<stage>`` -- which is stable
    across a session rebuild, so a verdict submitted by the old instance reaches the new one.
    """

    name: ClassVar[str] = "verification"
    Config: ClassVar[type[VerificationConfig]] = VerificationConfig

    __slots__ = ("_config", "_frames", "_kind", "_source_stage", "_state", "_vote", "_worker")

    def __init__(self, config: VerificationConfig, state: StateStore) -> None:
        """Bind a validated config to a store already scoped to this bucket and stage.

        The worker is **not** built here: an app that never raises a candidate (and the
        validator's synthetic camera, whose id is not an ObjectID) never touches it.
        """
        self._config = config
        self._state = state
        self._kind = config.stage_name
        self._source_stage = config.source.partition(".")[0]
        self._frames: dict[str, Any] = config.frames.model_dump()
        self._vote: dict[str, Any] = config.vote.model_dump()
        self._worker: VerificationWorker | None = None

    # -- the frame ----------------------------------------------------------

    def process(self, ctx: FrameContext) -> PrimitiveOutput:
        """Collect any verdict, then decide this frame.

        Collect first, always: a verdict that lands on a quiet frame must still move the state,
        or it is lost on exactly the frame where nothing is detected.
        """
        now = ctx.frame_ts
        value = self._source_value(ctx)
        candidate = value > self._config.above
        flags = _Flags()

        state = self._collect(now, flags)
        state = self._expire(state, now)
        if candidate:
            state = self._on_candidate(ctx, value, state, flags)
            if state == CONFIRMED:
                self._state.set(_QUIET_SINCE, now, lifetime=Lifetime.PERSISTENT)

        passing = candidate and (
            self._config.mode == "shadow" or state == CONFIRMED or flags.policy_pass
        )
        values: dict[str, Scalar] = {
            "verified_rank": float(value) if passing else 0.0,
            "verified": int(state == CONFIRMED or flags.policy_pass),
            "verification_pending": int(state == PENDING),
            "verification_suppressed": int(flags.suppressed),
            "verification_rejected": int(flags.rejected),
            "verification_dropped": int(flags.dropped),
            "verification_skipped": int(flags.skipped),
            "verification_votes_confirmed": int(self._state.get(_VOTES_CONFIRMED, 0) or 0),
            "verification_votes_total": int(self._state.get(_VOTES_TOTAL, 0) or 0),
        }
        events: tuple[PrimitiveEvent, ...] = ()
        if passing:
            events = tuple(
                dataclasses.replace(event, kind=self._kind)
                for event in ctx.previous[self._source_stage].events
                if event.kind == self._source_stage
            )
        return PrimitiveOutput(values=values, events=events)

    def _source_value(self, ctx: FrameContext) -> float:
        """The candidate magnitude, via the engine's one resolver.

        :func:`~.base.resolve_value` raises :class:`~.base.SourceResolutionError` for a missing
        stage or key -- ``09`` §3, an unresolvable source is an error, never a silent zero.
        """
        raw = resolve_value(ctx.previous, self._config.source)
        if isinstance(raw, bool):
            return float(raw)
        if isinstance(raw, (int, float)):
            return float(raw)
        raise VerificationSourceError(
            f"{self._kind}.source {self._config.source!r} published {raw!r}, a "
            f"{type(raw).__name__}; it must be a number to compare with above: "
            f"{self._config.above}. Point it at a numeric key (e.g. level_rank, not level)."
        )

    # -- the state machine --------------------------------------------------

    def _collect(self, now: float, flags: _Flags) -> str:
        """``take()`` the mailbox and apply a verdict, returning the state after it."""
        state = str(self._state.get(_STATE, IDLE) or IDLE)
        if state != PENDING and self._worker is None:
            return state  # nothing was ever submitted from this instance and nothing is owed
        verdict = self._bound_worker().take(self._state.prefix, now)
        if verdict is None:
            return state
        if state != PENDING:
            logger.warning(
                "verification %s: discarded a %r verdict that arrived in state %s",
                self._state.prefix,
                verdict.status,
                state,
            )
            return state
        return self._apply(verdict, now, flags)

    def _apply(self, verdict: Verdict, now: float, flags: _Flags) -> str:
        """Map one verdict onto the next state (spec §3, "State machine")."""
        status = verdict.status
        if status == "confirmed":
            nxt = CONFIRMED
        elif status == "dropped":
            nxt = IDLE
            flags.dropped = True
        elif status == "rejected":
            nxt = COOLDOWN
        else:
            if status not in _FINAL_BY_POLICY:
                logger.error(
                    "verification %s: unknown verdict status %r; treating it as unavailable",
                    self._state.prefix,
                    status,
                )
            policy = (
                self._config.on_unverifiable
                if status == "unverifiable"
                else self._config.on_unavailable
            )
            nxt = CONFIRMED if policy == "pass" else COOLDOWN
        if nxt == COOLDOWN:
            flags.rejected = True
            level = float(self._state.get(_PENDING_LEVEL, 0.0) or 0.0)
            self._state.set(_COOLDOWN_LEVEL, level, lifetime=Lifetime.PERSISTENT)
        if nxt == CONFIRMED:
            self._state.set(_QUIET_SINCE, now, lifetime=Lifetime.PERSISTENT)
        self._state.set(
            _VOTES_CONFIRMED, int(verdict.votes_confirmed), lifetime=Lifetime.PERSISTENT
        )
        self._state.set(_VOTES_TOTAL, int(verdict.votes_total), lifetime=Lifetime.PERSISTENT)
        self._enter(nxt, now)
        logger.info(
            "verification %s: verdict %s (%d/%d votes, reason %r) -> %s",
            self._state.prefix,
            status,
            int(verdict.votes_confirmed),
            int(verdict.votes_total),
            verdict.reason,
            nxt,
        )
        return nxt

    def _expire(self, state: str, now: float) -> str:
        """Leave CONFIRMED after a quiet spell, and COOLDOWN once it has been served.

        Checked on every frame *before* this frame's candidate is recorded, so a stream gap
        longer than ``clear_after_quiet_seconds`` re-verifies the next candidate rather than
        waving it through on a verdict about a different episode.
        """
        if state == CONFIRMED:
            quiet_since = float(self._state.get(_QUIET_SINCE, now) or now)
            if now - quiet_since >= self._config.clear_after_quiet_seconds:
                return self._enter(IDLE, now)
        elif state == COOLDOWN:
            since = float(self._state.get(_SINCE, now) or now)
            if now - since >= self._config.cooldown_seconds:
                return self._enter(IDLE, now)
        return state

    def _on_candidate(self, ctx: FrameContext, value: float, state: str, flags: _Flags) -> str:
        """Submit from IDLE, or from COOLDOWN on an escalation; suppress everything else."""
        escalation = state == COOLDOWN and value > float(
            self._state.get(_COOLDOWN_LEVEL, 0.0) or 0.0
        )
        if state == IDLE or escalation:
            return self._submit(ctx, value, state, flags)
        flags.suppressed = True
        return state

    def _submit(self, ctx: FrameContext, value: float, state: str, flags: _Flags) -> str:
        """Hand one job to the worker; never blocks.

        A candidate that cannot be sent is ``verification_skipped`` and passes or blocks by
        ``on_unavailable`` -- the verifier cannot be asked, which is the same situation as the
        verifier being down.  The state does not move, so the next candidate tries again.
        """
        reason = _unsendable(ctx)
        if reason is None:
            # Lazy for the same reason as _bound_worker.
            from matrice_analytics.engine.verify import VerifyJob  # noqa: PLC0415

            job = VerifyJob(
                camera_id=ctx.camera_id,
                rtp_timestamp=_rtp(ctx),
                timestamp_ms=int(ctx.frame_ts * 1000),
                query=self._config.query,
                frames=dict(self._frames),
                vote=dict(self._vote),
                frame_ts=ctx.frame_ts,
            )
            if self._bound_worker().submit(self._state.prefix, job):
                self._state.set(_PENDING_LEVEL, value, lifetime=Lifetime.PERSISTENT)
                return self._enter(PENDING, ctx.frame_ts)
            # Closed (teardown). Unbind so the next candidate asks worker_for() afresh.
            self._worker = None
            reason = "the verification worker is closed"
        flags.skipped = True
        flags.policy_pass = self._config.on_unavailable == "pass"
        if self._state.get(_WARNED) != reason:
            self._state.set(_WARNED, reason, lifetime=Lifetime.PERSISTENT)
            logger.warning(
                "verification %s: candidate not sent (%s); on_unavailable=%s applies",
                self._state.prefix,
                reason,
                self._config.on_unavailable,
            )
        return state

    def _enter(self, state: str, now: float) -> str:
        self._state.set(_STATE, state, lifetime=Lifetime.PERSISTENT)
        self._state.set(_SINCE, now, lifetime=Lifetime.PERSISTENT)
        return state

    def _bound_worker(self) -> VerificationWorker:
        """The process-wide worker, bound on first use.

        Imported here, not at module top: the worker package owns the one sanctioned thread,
        and an app with no ``verification`` stage must never import it (``base.py``).
        """
        if self._worker is None:
            from matrice_analytics.engine.verify import worker_for  # noqa: PLC0415

            self._worker = worker_for()
        return self._worker

    # -- window -------------------------------------------------------------

    def window(self, frames: Sequence[PrimitiveOutput]) -> WindowOutput:
        """Each flag as "at any point this window" (its max), the votes as they stand.

        ``verified_rank`` is the window's peak passing rank -- the same peak-not-mean reading
        ``incident_quantise`` publishes for its rank (**PY-1**).  The votes are read from the
        store, not ``frames[-1]``, so a capped retention list cannot lose them.
        """
        values: dict[str, Scalar] = {
            "verified_rank": max(
                (float(frame.values.get("verified_rank", 0.0) or 0.0) for frame in frames),
                default=0.0,
            ),
        }
        for key in _FLAG_KEYS:
            values[key] = max((int(frame.values.get(key, 0) or 0) for frame in frames), default=0)
        values["verification_votes_confirmed"] = int(self._state.get(_VOTES_CONFIRMED, 0) or 0)
        values["verification_votes_total"] = int(self._state.get(_VOTES_TOTAL, 0) or 0)
        return WindowOutput(values=values)

    def reset(self) -> None:
        """Window boundary: clear WINDOW keys only -- every key here is PERSISTENT and survives.

        Runs every 60 s, so it must never touch the worker; teardown is
        ``EngineBackend.close()`` -> ``close_all_workers()``.
        """
        self._state.end_window()


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _unsendable(ctx: FrameContext) -> str | None:
    """Why this candidate can never succeed at the server, or ``None``.

    Checked before submit, not in the worker: a request certain to 422 must not occupy one of
    the queue's slots, where it would evict a real alert.
    """
    if ctx.frame_ts < _EPOCH_2020:
        return (
            f"frame_ts {ctx.frame_ts:.3f} is before 2020-01-01 -- a stream-relative clock "
            "(has_absolute_time=false) with no recording to look up (PY-13)"
        )
    if not _OBJECT_ID.match(ctx.camera_id):
        return f"camera_id {ctx.camera_id!r} is not a 24-hex ObjectID"
    return None


def _rtp(ctx: FrameContext) -> int:
    """``StreamInfo.rtp_number`` as the uint32 the API wants, or ``0`` ("locate by time").

    The wire field is a string and ``""`` is the documented "not an RTSP source" sentinel.
    Anything that is not a decimal in ``1..2**32-1`` becomes ``0``: the server then falls back to
    lookup by ``timestamp_ms``, which is always sent -- so a stale or garbled RTP (the session
    keeps its construction-time value on frames with no anchor) is recoverable, whereas raising
    here would lose the alert.
    """
    raw: object = ctx.stream.rtp_number if ctx.stream is not None else ""
    if isinstance(raw, bool):
        return 0
    if isinstance(raw, int):
        number = raw
    else:
        text = str(raw).strip()
        if not (text.isascii() and text.isdecimal()):
            return 0
        number = int(text)
    return number if 1 <= number <= _RTP_MAX else 0
