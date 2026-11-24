"""An episode's state (the data doc's eight) and the four the Episodes tab draws, from ONE mapping (D7)."""

from __future__ import annotations

from ....compat import StrEnum
from ..live.attempt import AttemptOutcome, AttemptPhase
from ..outcome import DropReason, SampleOutcome
from ..result import SampleErrorReason
from ..samples import FinishReason


class EpisodeState(StrEnum):
    """How a rollout (or its episode) stands: live `queued`, `running`, `scoring`; ended the other five."""

    QUEUED = "queued"
    RUNNING = "running"
    SCORING = "scoring"
    COMPLETED = "completed"
    CUT_OFF = "cut_off"  # stopped at its length limit
    TIMED_OUT = "timed_out"
    ERROR = "error"
    CANCELLED = "cancelled"


class EpisodeStatus(StrEnum):
    """The four the Episodes tab draws (a dot and a word); the exact state and reason stay in Details."""

    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"


STATUS_OF_STATE = {
    EpisodeState.QUEUED: EpisodeStatus.QUEUED,
    EpisodeState.RUNNING: EpisodeStatus.RUNNING,
    EpisodeState.SCORING: EpisodeStatus.RUNNING,
    EpisodeState.COMPLETED: EpisodeStatus.COMPLETED,
    EpisodeState.CUT_OFF: EpisodeStatus.COMPLETED,
    EpisodeState.TIMED_OUT: EpisodeStatus.ERROR,
    EpisodeState.ERROR: EpisodeStatus.ERROR,
    EpisodeState.CANCELLED: EpisodeStatus.ERROR,
}
#: An episode's state from its rollouts': a running one first, then queued, then scoring, then the worst ending.
_EPISODE_ORDER = (EpisodeState.RUNNING, EpisodeState.QUEUED, EpisodeState.SCORING, EpisodeState.CANCELLED,
                  EpisodeState.TIMED_OUT, EpisodeState.ERROR, EpisodeState.CUT_OFF, EpisodeState.COMPLETED)  # fmt: skip
_LIVE_PHASES = {AttemptPhase.QUEUED: EpisodeState.QUEUED, AttemptPhase.SCORING: EpisodeState.SCORING}
_ENDED_OUTCOMES = {AttemptOutcome.CANCELED: EpisodeState.CANCELLED, AttemptOutcome.ABORTED: EpisodeState.CANCELLED,
                   AttemptOutcome.ERROR: EpisodeState.ERROR}  # fmt: skip
_ERROR_STATES = {SampleErrorReason.CANCELED: EpisodeState.CANCELLED, SampleErrorReason.TIMEOUT: EpisodeState.TIMED_OUT,
                 SampleErrorReason.GROUP_HAS_ABORTED: EpisodeState.CANCELLED}  # fmt: skip
_DROP_STATES = {DropReason.ABORTED: EpisodeState.CANCELLED, DropReason.ERROR: EpisodeState.ERROR,
                DropReason.INVALID_REWARD: EpisodeState.ERROR}  # fmt: skip


def to_episode_status(state: EpisodeState) -> EpisodeStatus:
    """The drawn status of a state: queued → Queued; running, scoring → Running; completed, cut off → Completed;
    timed out, error, cancelled → Error."""
    return STATUS_OF_STATE[state]


def derive_rollout_state(
    *, outcome: SampleOutcome, error_reason: str | None = None, finish_reason: str | None = None,
    drop_reason: str | None = None, has_error: bool = False, phase: str | None = None, ended: str | None = None,
) -> tuple[EpisodeState, str | None]:  # fmt: skip
    """One rollout's state and its exact reason. `has_error`: its result is `error`; `phase`: a live attempt's newest
    progress phase; `ended`: the outcome its attempt's end part named (an `ended` sample still waits on its bundle)."""
    if outcome is SampleOutcome.IN_FLIGHT:
        return _LIVE_PHASES.get(phase or "", EpisodeState.RUNNING), phase or None
    if outcome is SampleOutcome.ENDED:
        return _ENDED_OUTCOMES.get(ended or "", EpisodeState.SCORING), ended or None
    if error_reason:
        return _ERROR_STATES.get(error_reason, EpisodeState.ERROR), error_reason
    if drop_reason in _DROP_STATES:
        return _DROP_STATES[drop_reason], drop_reason
    if has_error or finish_reason == FinishReason.ERROR:
        return EpisodeState.ERROR, finish_reason
    if finish_reason == FinishReason.ABORT:
        return EpisodeState.CANCELLED, finish_reason
    if finish_reason == FinishReason.LENGTH:
        return EpisodeState.CUT_OFF, finish_reason
    return EpisodeState.COMPLETED, drop_reason or finish_reason


def derive_episode_state(states: list[tuple[EpisodeState, str | None]]) -> tuple[EpisodeState, str | None]:
    """An episode's state from its rollouts' (`derive_rollout_state`): a live rollout keeps it live, else the worst
    ending (a crash or timeout ends the play for every agent)."""
    if not states:
        return EpisodeState.QUEUED, None
    return min(states, key=lambda item: _EPISODE_ORDER.index(item[0]))
