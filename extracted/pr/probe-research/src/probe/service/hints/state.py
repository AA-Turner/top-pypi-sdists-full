"""a lookup and a session's hint state, the hints switch, and which sessions hints follow."""

from __future__ import annotations
import threading
from collections import OrderedDict, deque
from dataclasses import dataclass, field

from ..watch.alertpoll import Endpoint
from ...foundation.service_api.vocabularies import Mode

#: `off` (or 0 / false / no) in the service's environment, or in a session's,
#: turns the lane off there.
HINTS_ENV = "PROBE_HINTS"
#: The window's messages sent, at most (the newest); the server asks as many.
WINDOW_MAX_SEGMENTS = 32
BUCKET_BURST = 5.0


class Skip:
    """Why a hint that fired was not posted (the log line and `stats`)."""

    STALE = "stale"  # a newer researcher prompt came while it was looked up
    REPEAT = "repeat"  # every record in it was delivered, or waits in a hint
    NOT_POSTED = "not_posted"  # the mailbox step wrote nothing
    TOO_LONG = "too_long"  # longer than MAX_HINT_CHARS: dropped whole
    #: Asked before a hint from a newer trigger was posted (the other lookup
    #: thread answered first): it would replace that hint in the session's slot.
    SUPERSEDED = "superseded"
    #: The team's hints went off (`mode: off`) while it was asked.
    OFF = "off"
    #: The lane closed while it was asked.
    CLOSED = "closed"


def disabled(env) -> bool:
    return str(env.get(HINTS_ENV) or "").strip().lower() in ("off", "0", "false", "no")


# -- what a session is ------------------------------------------------------------


@dataclass
class Followed:
    """A session this lane reads: recorded here, its recorder holding it now,
    registered live (daemon or inline) by a registrant outside any sandbox."""

    sid: str
    harness: str
    mode: str
    #: The session's `<XDG_STATE_HOME>/probe`: its mailbox and its worker's store.
    state: str
    cwd: str
    transcript: str | None
    transcript_dir: str | None
    env: dict = field(default_factory=dict)


def followed(recordings, registered, *, now: float, ttl: float, default_state: str) -> list[Followed]:
    """The sessions to read, from the service's recordings (`RecorderHost.
    recordings`) and its registry's sessions. Never raises for one odd entry."""
    by_sid = {s.sid: s for s in registered}
    out: list[Followed] = []
    for rec in recordings:
        try:
            session = by_sid.get(rec.sid)
            if session is None or session.mode not in (Mode.DAEMON, Mode.INLINE) or not session.alive(now, ttl):
                continue
            if not session.unconfined:
                continue  # never this user's key for a session a sandbox registered (as `alertpoll`)
            thread, controls = rec.thread, rec.controls
            if thread is None or not thread.is_alive() or controls.stop.is_set() or controls.pause.is_set():
                continue
            if hasattr(controls, "claimed") and controls.claimed is None:
                continue  # its recorder does not hold it now: capture off, a disabled folder, another recorder
            params = rec.params if isinstance(rec.params, dict) else {}
            env = params.get("env") if isinstance(params.get("env"), dict) else {}
            if disabled(env):
                continue
            harness = params.get("harness") if isinstance(params.get("harness"), str) else session.harness
            out.append(Followed(
                sid=rec.sid, harness=harness or "", mode=session.mode,
                state=session.state_dir or params.get("state_dir") or default_state,
                cwd=str(params.get("cwd") or ""), transcript=params.get("transcript"),
                transcript_dir=params.get("transcript_dir"), env=dict(env)))
        except Exception:  # noqa: BLE001 -- one odd recording never hides the others
            continue
    return out


# -- the lane ---------------------------------------------------------------------


@dataclass
class Lookup:
    sid: str
    session: Followed
    trigger: str
    text: str
    #: Who sent a peer's message, as the harness named them (`Senders`).
    senders: list
    #: When the lane saw it (its clock), and when it happened (the line's own
    #: stamp, else when it was seen; epoch seconds).
    queued: float
    happened: float
    #: The session's researcher prompts and turn ends seen up to it: a newer
    #: one makes it stale.
    epoch: int
    #: Where it is asked, with which key (`credentials`, read when it was queued).
    ep: Endpoint | None = None
    #: A window's agent messages, newest first (`window_segments`): taken from
    #: the session's window when the lookup goes (`take_due`).
    segments: list = field(default_factory=list)
    #: The session's hints posted (`_State.posted`) when its request was built.
    posted_before: int = 0


@dataclass
class _State:
    """One session's memory, this service's life."""

    recent: OrderedDict = field(default_factory=OrderedDict)
    #: When its last lookup that was no window went, and its last window
    #: (`clock`): each kind waits SESSION_GAP_S after its own only.
    last_sent: float = float("-inf")
    window_last_sent: float = float("-inf")
    #: Researcher prompts and ends of the agent's turn seen (`Lookup.epoch`).
    epoch: int = 0
    #: Every hint's records the ledger knows of (this run's and the last week's,
    #: a previous service's included): message id -> record keys.
    ledger: dict | None = None
    lock: threading.Lock = field(default_factory=threading.Lock)
    no_key_said: bool = False
    #: The window clock (W1), under the lane's condition: the stamp of the last
    #: window look, researcher prompt or turn's first step (None from a turn's
    #: end until the next agent step), the newest agent step's, and the agent's
    #: messages since, oldest first.
    window_since: float | None = None
    window_seen: float | None = None
    window_messages: deque = field(default_factory=lambda: deque(maxlen=WINDOW_MAX_SEGMENTS))
    #: Window lookups failed in a row (no answer, refused, engine_error or
    #: rate_limited): WINDOW_FAILURES_STOP of them stop the `.window` marker.
    window_failures: int = 0
    #: Hints this lane posted for the session, and the newest trigger time
    #: (`Lookup.happened`) among them: under `lock`. Two lookup threads can
    #: answer out of order (`_deliver`).
    posted: int = 0
    posted_happened: float = float("-inf")
    #: The stamps of the agent's main-stream tool calls and the researcher's
    #: prompts seen here (the newest), under `lock`: what `delivery_receipt`
    #: counts as a waiting hint's chances.
    tool_calls: deque = field(default_factory=lambda: deque(maxlen=512))
    prompts: deque = field(default_factory=lambda: deque(maxlen=128))
    #: A prompt started a turn that has not ended (`_line`).
    turn_open: bool = False
    #: The last `delivery_receipt` and when (`clock`) it was made; under `lock`.
    delivery: dict | None = None
    delivery_at: float = float("-inf")
    #: When (`clock`) an undeliverable session was last asked about.
    probe_at: float = float("-inf")


class _Facts:
    """The daemon filter's fact store, in memory (the lane keeps no store)."""

    def __init__(self) -> None:
        self.facts: dict = {}

    def fact(self, key: str, default=None):
        return self.facts.get(key, default)

    def set_fact(self, key: str, value) -> None:
        self.facts[key] = value
