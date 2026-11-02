"""what one drain pass reports: ops held here or in progress, lane stalls, and the pass totals."""

from __future__ import annotations
from dataclasses import dataclass, field


class OpHeldHere(Exception):
    """This drainer must leave the op queued, untouched: not this process's to send, and
    nothing was learned about the op or its run.

    Raised while resolving the op's client, before anything is sent. The drain holds the op
    (a coalesced batch whole) with no attempt counted and nothing dead-lettered, and parks its
    run for the rest of the pass: not a stall, so no back-off follows. The seam for #2041's
    `CredentialNotHere` (a write queued under a credential this process does not hold)."""


class OpInProgress(OpHeldHere):
    """A long op made progress and is not finished: leave it queued, charge no attempt, let
    the other lanes go (plan item (g): a multipart upload moves one slice of parts per pass,
    then waits for the server's verifier). The op persisted its own progress before raising.

    ``retry_after`` None: come back on the very next pass (more parts to send). A number: its
    lane waits at least that long (server still verifying), through the same per-lane backoff
    a stall uses, with nothing counted against the op's failure budget."""

    def __init__(
        self, message: str, *, retry_after: float | None = None, wake_by: float | None = None
    ) -> None:
        super().__init__(message)
        self.retry_after = retry_after
        #: Look again within this many seconds, however far the lane's
        #: backoff has grown (`LaneStall.wake_by`).
        self.wake_by = wake_by


@dataclass
class LaneStall:
    """Why one run's lane stopped for the rest of a pass (plan 1.6)."""

    error: str
    #: The server's ``Retry-After`` on that failure, when it named one.
    retry_after: float | None = None
    #: The failure's HTTP status; None when no answer came at all (a network
    #: failure or a timeout), which a caller with a budget may stop on.
    status: int | None = None
    #: Not a failure at all: the run is HELD -- its op is not this drainer's to send (#2035), or
    #: its close waits for its writes in another queue. Nothing was sent, so this says nothing
    #: about the server (#2041 round 5: the takeover barrier read a held run as "unreachable"
    #: and stopped).
    held: bool = False
    #: Seconds after which the run must be looked at again whatever its
    #: backoff says (a close hold that expires then), or None.
    wake_by: float | None = None


@dataclass
class DrainReport:
    delivered: int = 0
    dead_lettered: int = 0
    remaining: int = 0
    auth_blocked: bool = False
    #: The refusal that set `auth_blocked`: its HTTP status and message (a 401, or a 403 that may
    #: name a missing SCOPE rather than the credential -- `key_refusal.credential_refused`), and
    #: the refused op's pinned context, since a machine-wide pass can stop on ANOTHER context's
    #: credential.
    auth_status: int | None = None
    auth_message: str | None = None
    auth_context: dict | None = None
    stopped_transient: bool = False
    #: Ops left queued behind an earlier upload of their run still waiting for
    #: its credential scan (see `Journal.waiting_positions`).
    held_back: int = 0
    #: Ops left queued because this drainer holds no credential matching the
    #: one that queued them (#2035); another process with it delivers them.
    credential_held: int = 0
    #: Stamped ops whose OWN credential the API refused this pass. Set aside
    #: with every other op of that credential; the pass goes on (#2041 review).
    credential_refused: int = 0
    #: True only when a refusal STOPPED the pass: an unstamped op (queued by an
    #: older release), whose credential nothing can tell apart from the rest.
    queue_auth_stopped: bool = False
    #: Every refusal this pass: ``{"status", "message", "context",
    #: "fingerprint"}`` (the refused key). ``auth_*`` above hold the first.
    auth_refusals: list[dict] = field(default_factory=list)
    #: Why ops were kept (`credential_held`), each reason once, for the CLI.
    held_reasons: list[str] = field(default_factory=list)
    #: Of `credential_held`, ops no credential on this machine will match as
    #: things stand (an unknown or another account: `CredentialNotHere.permanent`),
    #: the ones `probe outbox discard --held` drops.
    permanently_held: int = 0
    errors: list[str] = field(default_factory=list)
    #: The server's ``Retry-After`` on the failure that stopped this pass, in
    #: seconds, when it named one. Every retry loop waits at least this long.
    retry_after: float | None = None
    #: The pass stopped because the CALLER's deadline ran out (see
    #: `transport.deadline_scope`), not because an op failed.
    deadline_reached: bool = False
    #: Another drain held the lock for the whole of ``lock_timeout``: this pass
    #: attempted nothing.
    lock_busy: bool = False
    #: Per-run lanes (plan 1.6). A run whose head op failed transiently, by
    #: ``run_ref`` (None: ops that name no run): the op is parked in place, the
    #: rest of that run waits, and every other run's ops were still attempted.
    stalled_runs: dict[str | None, LaneStall] = field(default_factory=dict)
    #: Runs that had an op delivered or dead-lettered this pass: their backoff,
    #: if any, starts over.
    progressed_runs: set = field(default_factory=set)
    #: Runs this pass left because another drain was sending them, its drain
    #: lock let go for their upload (#3618). Also in ``stalled_runs``, held.
    busy_runs: set = field(default_factory=set)
    #: Ops the server refused because a newer attempt owns their run (a past
    #: write epoch), moved to ``discarded/`` rather than dead-lettered (T24).
    superseded: "DiscardCounts" = field(default_factory=lambda: DiscardCounts())
    #: The pass stopped for EVERY run because the server could not be reached
    #: at all (a connect failure) or stopped answering (a second response lost
    #: after sending in one pass): trying each run's head op in turn would only
    #: wait out one timeout per run.
    unreachable: bool = False
    #: Every run with an op in this pass's scan (None: not known, e.g. the pass
    #: never scanned), so a caller's backoff can forget the ones that left.
    queued_runs: set | None = None
    #: Ops held because this release does not know their kind (plan 1.11).
    unknown_kinds: int = 0
    #: Long ops (multipart uploads, plan (g)) that made progress this pass and
    #: stay queued for the next (`OpInProgress`).
    in_progress: int = 0
    #: Ops delivered inside a multi-op POST (plan 1.2); counted in
    #: ``delivered`` too.
    coalesced: int = 0
    #: Run closes held because writes of the same run, queued earlier under
    #: another credential, sit in another queue (#2041 round 3).
    close_held: int = 0
    #: Ops of runs the caller is backing off (``skip_runs``): not looked at,
    #: so the holds among them were not recounted this pass.
    skipped: int = 0
    #: ``{run_ref, op_id, error, status}`` for each op this pass dead-lettered,
    #: kept in ``dead_letters.json`` (`Journal.recent_dead_letters`) so a
    #: training process can say so while it runs (plan 1.7).
    dead_letter_records: list = field(default_factory=list)
    #: Ops a drainer's collect window held this pass (`window.CollectWindow`): queued until
    #: their run's `send_after`, never attempted, never failed. Counted in ``remaining``.
    deferred: int = 0
    #: Seconds until the soonest held run may send, or None when the window held nothing.
    send_in: float | None = None
    #: What each held run holds, by lane: a `LaneLoad`, so a drainer's sleep wakes early once
    #: new writes fill a POST (`CollectWindow.wait`).
    deferred_loads: dict = field(default_factory=dict)

    @property
    def clean(self) -> bool:
        return self.dead_lettered == 0 and self.remaining == 0 and not self.auth_blocked

    @property
    def auth_stopped(self) -> bool:
        """A refusal stopped the pass, rather than setting one credential's writes aside. A
        report naming no set-aside credential reads as stopped, as every report did before
        (#2041 review)."""
        return self.queue_auth_stopped or (self.auth_blocked and not self.credential_refused)


class CredentialNotHere(OpHeldHere):
    """This drainer holds no credential it may send the op with (#2035): the op stays queued,
    untouched, for a process that does. ``permanent``: none on this machine will match it as things
    stand (#2041 round 4); only those go with `probe outbox discard --held`."""

    def __init__(self, message: str = "", *, permanent: bool = False):
        super().__init__(message)
        self.permanent = permanent
from probe.sdk.delivery.journal.failures.discards import DiscardCounts  # noqa: E402 -- pieces need each other; the front door loads this one first
