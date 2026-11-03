"""What a wait on the worker ended with (one enum, R15), and the result it hands back."""

from __future__ import annotations

from dataclasses import dataclass

from probe.foundation.compat.compat import StrEnum


class WaitOutcome(StrEnum):
    """How waiting for one run's writes ended."""

    #: Every write of the run reached the server (checked in the folders, R10).
    DELIVERED = "delivered"
    #: The rest landed; the server refused some for good (they are in failed/).
    REFUSED = "refused"
    #: The server refused the credential, or the outbox is paused: nothing moves until a person acts.
    LOGIN_REFUSED = "login_refused"
    PAUSED = "paused"
    #: The rest landed; writes that kept failing were set aside in held/ (R12), or nothing of
    #: the run moved for twice the stall window.
    STALLED = "stalled"
    #: The server could not be reached for the outage window.
    UNREACHABLE = "unreachable"
    #: The worker kept dying with nothing delivered.
    WORKER_CRASH_LOOP = "worker_crash_loop"
    #: No worker could be started here (no subprocess, a frozen interpreter).
    NO_SENDER = "no_sender"
    #: An older release's worker held the queue and did not step aside (R3).
    OLD_WORKER = "old_worker"
    #: The close itself neither reached the server nor the outbox (full, or unwritable).
    CLOSE_UNRECORDED = "close_unrecorded"
    #: Ctrl-C: the caller stops waiting; the worker keeps sending.
    STOPPED_WAITING = "stopped_waiting"
    #: The caller's own limit ran out (`flush_timeout`, a SIGTERM's grace); the worker keeps sending.
    OUT_OF_TIME = "out_of_time"


#: Outcomes after which the writes are still being sent: the caller returns as `wait=False`.
STILL_SENDING = frozenset({WaitOutcome.STOPPED_WAITING, WaitOutcome.OUT_OF_TIME})


@dataclass
class WaitResult:
    """Where one run's writes stood when the wait ended."""

    outcome: WaitOutcome
    run_ref: str
    pending: int = 0
    pending_bytes: int = 0
    held: int = 0
    failed: int = 0
    discarded: int = 0
    #: Writes of the run the workers delivered while this wait lasted.
    delivered: int = 0
    first_error: str | None = None
    waited_seconds: float = 0.0
    #: Who held the lease, for `OLD_WORKER` (pid and release).
    holder: str | None = None

    @property
    def is_delivered(self) -> bool:
        return self.outcome == WaitOutcome.DELIVERED

    @property
    def is_still_sending(self) -> bool:
        return self.outcome in STILL_SENDING
