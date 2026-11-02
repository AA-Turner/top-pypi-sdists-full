"""The connection state machine behind ``dreamscale.connect``: a pure transition table.

One policy has one connection, in one of six states. Every change of state is a row in
``TRANSITIONS``; anything not in the table is illegal and raises. The table carries no I/O:
``dreamscale.policy.facade`` drives it and performs the named effect after each transition,
so the rules can be read and tested here without a network.

Sessions are only ever opened because of a user call. A lost link releases the session
(classify, confirm the close); the next ``predict``/``next_action`` reopens it. Nothing opens
a billed session that nobody is using.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class State(StrEnum):
    OPENING = "opening"
    QUEUED = "queued"
    READY = "ready"
    RELEASED = "released"
    RECONNECTING = "reconnecting"
    CLOSED = "closed"


class Event(StrEnum):
    # A user call needs a session and none is open.
    OPEN = "open"
    # The control plane queued the session (shared pool full): position and ETA follow.
    SERVER_QUEUED = "server_queued"
    # The session is ready and the data plane is connected.
    SESSION_READY = "session_ready"
    # An open attempt failed for a reason on the retry list (network, 429, 5xx).
    OPEN_FAILED_RETRYABLE = "open_failed_retryable"
    # An open attempt failed for any other reason (credits, auth, cap, model, contract).
    OPEN_FAILED_FATAL = "open_failed_fatal"
    # The backoff elapsed: try the next attempt.
    RETRY = "retry"
    # Three consecutive attempts failed.
    ATTEMPTS_EXHAUSTED = "attempts_exhausted"
    # The backoff elapsed but no caller is waiting any more: don't open a session nobody
    # asked for; the next call will.
    ABANDONED = "abandoned"
    # Nothing in flight for the idle window.
    IDLE_ELAPSED = "idle_elapsed"
    # The data plane dropped, the request stalled, or the server ended the session.
    LINK_LOST = "link_lost"
    # The lost session turned out to be a fatal end (credits), or its close could not
    # be confirmed in time.
    DROP_FAILED = "drop_failed"
    # Three consecutive error frames from the server with no chunk between them.
    REQUESTS_FAILED = "requests_failed"
    # close() or atexit.
    CLOSE = "close"


class Effect(StrEnum):
    NONE = "none"
    # Start the open task (create session, wait until ready, connect the data plane).
    START_OPEN = "start_open"
    # Show the queue position.
    ANNOUNCE_QUEUE = "announce_queue"
    # The session is usable: arm the idle timer.
    ARM_IDLE = "arm_idle"
    # Sleep the backoff, then fire RETRY.
    SCHEDULE_RETRY = "schedule_retry"
    # Remember the error; every later call raises it.
    LATCH_FAILURE = "latch_failure"
    # Idle: close the session the normal way (detach when kept warm, else delete).
    RELEASE_SESSION = "release_session"
    # Lost: classify the old session, then delete it until the server confirms.
    DROP_SESSION = "drop_session"
    # Stop whatever is in progress and close any session.
    SHUTDOWN = "shutdown"


class IllegalTransition(RuntimeError):
    pass


TRANSITIONS: dict[tuple[State, Event], tuple[State, Effect]] = {
    (State.OPENING, Event.SERVER_QUEUED): (State.QUEUED, Effect.ANNOUNCE_QUEUE),
    (State.OPENING, Event.SESSION_READY): (State.READY, Effect.ARM_IDLE),
    (State.OPENING, Event.OPEN_FAILED_RETRYABLE): (State.RECONNECTING, Effect.SCHEDULE_RETRY),
    (State.OPENING, Event.OPEN_FAILED_FATAL): (State.CLOSED, Effect.LATCH_FAILURE),
    (State.OPENING, Event.ABANDONED): (State.RELEASED, Effect.NONE),
    (State.OPENING, Event.CLOSE): (State.CLOSED, Effect.SHUTDOWN),
    (State.QUEUED, Event.SERVER_QUEUED): (State.QUEUED, Effect.ANNOUNCE_QUEUE),
    (State.QUEUED, Event.SESSION_READY): (State.READY, Effect.ARM_IDLE),
    (State.QUEUED, Event.OPEN_FAILED_RETRYABLE): (State.RECONNECTING, Effect.SCHEDULE_RETRY),
    (State.QUEUED, Event.OPEN_FAILED_FATAL): (State.CLOSED, Effect.LATCH_FAILURE),
    (State.QUEUED, Event.ABANDONED): (State.RELEASED, Effect.NONE),
    (State.QUEUED, Event.CLOSE): (State.CLOSED, Effect.SHUTDOWN),
    (State.READY, Event.IDLE_ELAPSED): (State.RELEASED, Effect.RELEASE_SESSION),
    (State.READY, Event.LINK_LOST): (State.RELEASED, Effect.DROP_SESSION),
    (State.READY, Event.REQUESTS_FAILED): (State.CLOSED, Effect.SHUTDOWN),
    (State.READY, Event.CLOSE): (State.CLOSED, Effect.SHUTDOWN),
    (State.RELEASED, Event.OPEN): (State.OPENING, Effect.START_OPEN),
    (State.RELEASED, Event.DROP_FAILED): (State.CLOSED, Effect.LATCH_FAILURE),
    (State.RELEASED, Event.REQUESTS_FAILED): (State.CLOSED, Effect.LATCH_FAILURE),
    (State.RELEASED, Event.CLOSE): (State.CLOSED, Effect.SHUTDOWN),
    (State.RECONNECTING, Event.RETRY): (State.OPENING, Effect.START_OPEN),
    (State.RECONNECTING, Event.ATTEMPTS_EXHAUSTED): (State.CLOSED, Effect.LATCH_FAILURE),
    (State.RECONNECTING, Event.ABANDONED): (State.RELEASED, Effect.NONE),
    (State.RECONNECTING, Event.CLOSE): (State.CLOSED, Effect.SHUTDOWN),
    (State.CLOSED, Event.CLOSE): (State.CLOSED, Effect.NONE),
}

# Open attempts: delays before attempt 1, 2 and 3. After the third failure the next call
# raises. Together with the creation floor this stays far below the control plane's
# 10 session creations per minute per user.
RETRY_DELAYS_S: tuple[float, ...] = (0.0, 2.0, 5.0)
MAX_OPEN_ATTEMPTS = len(RETRY_DELAYS_S)
# A server Retry-After longer than this is not honoured: the caller is still waiting.
MAX_RETRY_DELAY_S = 30.0
# Minimum spacing between two session creations by one policy.
CREATE_FLOOR_S = 6.0
# A caller with less than this left on its own deadline does not open a session.
MIN_OPEN_WINDOW_S = 2.0
# Consecutive timeouts bounded by callers' own deadlines, with no answer in between, that
# count as a dead link (a short predict timeout must not hide a dead data plane).
DEADLINE_TIMEOUTS_AS_DROP = 3
# The SDK closes an idle session after this long; the next call reopens it.
IDLE_RELEASE_S = 60.0
# A request with no answer for this long is a dead link (shared pools answer in < 1 s).
REQUEST_STALL_S = 8.0
# How long to keep retrying the DELETE of a lost session before giving up.
DROP_CONFIRM_S = 10.0
# One GET to classify a lost session (credits versus a dead unit) before deleting it.
CLASSIFY_TIMEOUT_S = 2.0


@dataclass
class Transition:
    previous: State
    event: Event
    state: State
    effect: Effect


@dataclass
class ConnectionMachine:
    """The current state plus the transition log. ``fire`` is the only way to move."""

    state: State = State.OPENING
    history: list[Transition] = field(default_factory=list)

    def fire(self, event: Event) -> Transition:
        try:
            next_state, effect = TRANSITIONS[(self.state, event)]
        except KeyError:
            raise IllegalTransition(f"{event.value} in state {self.state.value}") from None
        transition = Transition(self.state, event, next_state, effect)
        self.state = next_state
        self.history.append(transition)
        return transition

    def can(self, event: Event) -> bool:
        return (self.state, event) in TRANSITIONS

    @property
    def is_ready(self) -> bool:
        return self.state is State.READY

    @property
    def is_closed(self) -> bool:
        return self.state is State.CLOSED


def retry_delay_s(attempt: int, *, retry_after_s: float | None = None) -> float:
    """Delay before open attempt ``attempt`` (1-based); a server Retry-After wins."""
    delay = RETRY_DELAYS_S[min(max(attempt, 1), MAX_OPEN_ATTEMPTS) - 1]
    if retry_after_s is not None and retry_after_s > delay:
        return min(float(retry_after_s), MAX_RETRY_DELAY_S)
    return delay
