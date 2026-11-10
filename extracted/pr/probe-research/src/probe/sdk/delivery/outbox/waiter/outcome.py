"""What a wait on the worker ended with (one enum, R15), and the result it hands back."""

from __future__ import annotations

from dataclasses import dataclass, field

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
    #: No Probe service here took them to send (none answered, or none took the drain).
    NO_SENDER = "no_sender"
    #: As NO_SENDER, and the key passed in code never reached a service (plan D21): only a
    #: process holding that key can send them.
    KEY_NOT_HANDED = "key_not_handed"
    #: An older release's worker held the queue and did not step aside (R3).
    OLD_WORKER = "old_worker"
    #: A write of the run is of a journal version or op kind the Probe service's drain here does not
    #: read (M4): it waits, in order, for a newer service.
    NEEDS_NEWER_SERVICE = "needs_newer_service"
    #: The close itself neither reached the server nor the outbox (full, or unwritable).
    CLOSE_UNRECORDED = "close_unrecorded"
    #: Everything was delivered, but the server refused some of it once it stored it (infra
    #: I15d: a 202 batch refused at apply). The refusals are on the run (`ingest.refusals`).
    DATA_REFUSED = "data_refused"
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
    #: The Probe service's version, for `NEEDS_NEWER_SERVICE`.
    service_version: str | None = None
    #: The outbox folder, for `KEY_NOT_HANDED` (the recovery names it).
    outbox: str | None = None
    #: For `KEY_NOT_HANDED`: the run's server when not the default (the recovery's drain must name it).
    server: str | None = None
    #: For `DATA_REFUSED`: the run read's `ingest.refusals` of this attempt, each with its kind,
    #: counts and the server's sentence (`message.text`).
    refusals: list = field(default_factory=list)

    @property
    def is_delivered(self) -> bool:
        return self.outcome == WaitOutcome.DELIVERED

    @property
    def is_still_sending(self) -> bool:
        return self.outcome in STILL_SENDING
