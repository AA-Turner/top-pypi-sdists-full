"""an incident and its family (the closed vocabulary the server twins)."""

from __future__ import annotations
from dataclasses import dataclass


class Family:
    """The report families (the API contract's table, rev 5): the `family` slug a report carries."""

    SERVICE_CRASH = "service_crash"
    SERVICE_ERROR = "service_error"
    UPDATE_REJECTED = "update_rejected"
    UPDATE_FAILED = "update_failed"
    TAP_LOAD = "tap_load"
    SERVICE_DOWN = "service_down"
    RECORDER = "recorder"
    WORKER = "worker"
    HOOK_HOST = "hook_host"
    HOOK = "hook"
    BACKGROUND = "background"
    #: The machine's outbox holds writes nothing here will send without a person
    #: (a refused credential, writes held for one), its oldest OUTBOX_STUCK_S old.
    OUTBOX_STUCK = "outbox_stuck"
    #: The API refuses a key the CLI config holds (the sign-in, the daemon's
    #: key, the MCP key), asked once every CREDENTIAL_CHECK_S.
    CREDENTIAL_REFUSED = "credential_refused"
    #: A live session's transcript waits CAPTURE_STALL_S past its last receipt.
    CAPTURE_STALLED = "capture_stalled"


#: About one session (`sid`); every other family is about the machine.
SESSION_FAMILIES = frozenset({Family.RECORDER, Family.WORKER})


# -- the watch ------------------------------------------------------------------


@dataclass
class Incident:
    family: str
    reason: str
    sid: str | None
    facts: dict
    #: The consent variables of each event's own environment, where it had one.
    envs: list
    #: Reported once ever: the key `watch.json` keeps once it was.
    once: str | None
    at: float
    #: The sessions whose agent ran when it was noted (None: not yet looked at).
    voters: list | None = None
    #: Looked at while discovering: those sessions are joined by the ones back
    #: once the window is over (`merge_voters`).
    partial: bool = False
    #: Its consent: `(allowed, why, the env the child gets)`; asked again at a retry.
    verdict: tuple | None = None
    #: Not sent before this (wall): a report tried again later.
    not_before: float = 0.0
    #: When it was first tried and did not land (a retry follows), else None.
    first_try: float | None = None

    @property
    def key(self) -> tuple:
        return self.family, self.sid
