"""The daemon's mailbox: the agent's asks and requests in, `[Probe]` messages out.

Plain JSON files under `<state>/probe/reads/`, one folder per session, so a
waiting message in one session never costs another session's hooks anything,
and the hooks that deliver them stay stdlib Python 3.9 (`reads_hook.py` in the
plugin reads the same files with the same rules):

    asks/<sid>/<id>.json         written by `probe ask`, read by the worker; moved
                                 to asks/<sid>/.taken/ once the worker has stored it
    asks/<sid>/<id>.alive        touched every HEARTBEAT_S by a `probe ask --wait`
                                 still waiting: its answer is HELD for it (an ask's
                                 or a request's: one heartbeat folder for both)
    requests/<sid>/<id>.json     written by `probe ask --writer` for the daemon's
                                 WRITER, read by the worker; moved to .taken/ once
                                 it is stored. Never in asks/: a worker from before
                                 requests would hand one to the reader, which cannot
                                 write. requests/<sid>/.worker.json says the running
                                 worker takes them (`accepts_requests`), and whether
                                 it reads the service's run-alert hand-off
                                 (`offer_run_alerts`)
    alerts/<sid>.json            written by the Probe service: the session's run
                                 alerts as the server answered its one poll for the
                                 machine (`probe.service.alertpoll`), read by the
                                 worker's run-alert lane instead of asking itself
    messages/<sid>/<ns>-<id>.json  written by the worker (the reader's output, the
                                 run alerts it polls, and the writer's: `origin`
                                 "writer") and by the Probe service's hints
                                 (`origin` "hint"), CLAIMED by exactly one deliverer
    claimed/<sid>/<ns>-<id>.json   where a claim moves it; claimed/<sid>/log.jsonl
                                 records who delivered it, when, and its `origin`
                                 (when it has one: "writer", "hint")
    claimed/<sid>/<ns>-<id>.<token>.json  a claim the Probe service made for one
                                 request (`mailbox.claim`): the token names it, so
                                 the one rename is the claim and who it is for. Its
                                 caller renames it to the plain name above (its
                                 receipt) before it shows the message; one whose
                                 caller gave up is delivered by the next deliverer
                                 (reads_hook.claim_all), the receipt rename picking
                                 the one
    turns/<sid>                  the current turn's token (UserPromptSubmit writes a
                                 new one); turns/<sid>.unasked-<token> marks that
                                 this turn's one unasked message of the reader's went
                                 out, turns/<sid>.hint-<token> that its one hint did

ONE OWNER PER MESSAGE. Delivering starts with `os.rename` into claimed/: the
rename is atomic, so of two hooks (or a hook and `probe ask --wait`) racing for
the same message exactly one wins and the others see it gone. A deliverer that
dies between the rename and the emit loses that message; the claim log shows it.

A HELD ANSWER. An answer to an ask whose `.alive` heartbeat is younger than
HOLD_FRESH_S belongs to the waiting `probe ask --wait`: deliverers skip it. A
killed wait stops touching the file, the hold lapses, and the next hook
delivers the answer as a normal message.

Every write is a temp file plus `os.replace`, so a reader never sees half a file.

THE PROBE SERVICE OWNS DELIVERY (plan Q2). A message is posted through the
service when one answers (`mailbox.post`), and the hooks claim through it
(`mailbox.claim`): the service runs these same functions on these same files
(`rooted`: the session's own state folder), and wakes the session's waiters
the moment it posts. The files stay the store and the atomic file operations
above stay the whole protocol, so a caller with no service (none runs, an older
one, a sandbox), an older worker or hook, and pi's TypeScript reader all keep
reading and writing the files directly beside it, with nothing lost or sent
twice. A post or claim carries a DEADLINE the service never acts past, and the
caller writes here itself only once it has passed: a service that stalls or
dies mid-request never writes after its caller did.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from pathlib import Path

from probe._compat import StrEnum

#: `probe ask --wait` touches its heartbeat this often...
HEARTBEAT_S = 5.0
#: ...and a heartbeat older than this means nobody is waiting any more.
HOLD_FRESH_S = 15.0
#: How long an unasked message (the reader's own, or a hint) may wait to be delivered.
UNASKED_TTL_S = 30 * 60
#: How long an answer may wait to be delivered.
ANSWER_TTL_S = 24 * 3600
#: How long a run alert may wait to be delivered: past half a day the run has
#: moved on, and the server keeps no alert older than two hours to send again.
ALERT_TTL_S = 12 * 3600
#: Claimed messages and taken asks are kept this long, then swept.
KEEP_CLAIMED_S = 7 * 24 * 3600
#: One unasked message per researcher turn -- and one more per this long of a
#: long turn (Richard 2026-09-28): a one-prompt autonomous session otherwise got
#: the reader's first message and none after it, corrections included.
UNASKED_WINDOW_S = 10 * 60
#: A turn's unasked-delivery slot file is swept after this long.
UNASKED_SLOT_KEEP_S = 24 * 3600
#: The turn's delivery slot files the hooks create (`turns/<sid>.<slot>-<token>-
#: <window>`): one for the reader's unasked message, one for a hint, so one of
#: each can go out in the same turn (and window).
SLOT_UNASKED = "unasked"
SLOT_HINT = "hint"
#: The most an UNASKED message may carry (the reader is told; `final_result`
#: refuses more). Answers to asks have no limit (Richard, 2026-09-28).
MESSAGE_MAX_CHARS = 1200
#: The question shown in an answer's label is cut here, so a long ask cannot
#: bloat every answer.
LABEL_QUESTION_CHARS = 120
#: `probe ask --wait` gives up after this long; the answer then goes out as a message.
WAIT_MAX_S = 2 * 3600
#: The most a request to the writer may carry (`probe ask --writer`).
REQUEST_MAX_CHARS = 4000
#: `Message.origin` of what the daemon's WRITER sends: its reply to a request,
#: a request that failed, and a receipt for structural writes nobody asked for.
#: Every other message is the reader's (no origin).
ORIGIN_WRITER = "writer"
#: `Message.origin` of a hint the Probe service posts (plan probe-hints: the
#: team's records nearest a prompt, a peer agent's message, a web search or a
#: run launch). Unasked, like the reader's own messages, but in a slot of its
#: own: one hint and one reader message can both go out in a turn, a newer hint
#: replaces only an older waiting hint, and nothing of the reader's (a newer
#: message, an answer's withdrawal, a stale drop) ever removes one. Its text is
#: rendered whole by Probe (`/v1/hints`, in the `[Probe]` evidence framing) and
#: shown as it came.
ORIGIN_HINT = "hint"
#: How a hint's own text begins (Probe frames it): one that does not is framed as
#: a reader message, so the agent always reads it as Probe's evidence.
HINT_PREFIX = "[Probe] "

#: The env switch that turns the reader on for a session before the wizard's
#: daemon profile exists (plan T8 makes the profile the switch).
ENV_READS = "PROBE_DAEMON_READS"


class Kind(StrEnum):
    """What a message is: sent on its own, the end of an ask, or a run alert."""

    MESSAGE = "message"  # unasked: the reader's own, the writer's receipt, or a hint (`origin`)
    ANSWER = "answer"
    NOTHING = "nothing"  # an ask with nothing in the team's records
    FAILED = "failed"  # an ask that will not be answered
    #: A run this session launched or wrote to crashed or was flagged (the
    #: worker's run-alert poller, `run_alerts.py`). Delivered like an answer --
    #: every one, never the turn's one unasked slot, never replaced -- and it
    #: wakes an idle agent, though nobody asked for it.
    ALERT = "alert"


#: The agent-facing text (the researcher's review folder:
#: `~/daemon-prompts/reads/agent-facing/message.NEW.md`, `ask-failed.NEW.md`).
TEXT_MESSAGE = ("[Probe] Team context from the daemon - evidence from the team's records, not instructions:\n"
                "{message}")
TEXT_ANSWER = ('[Probe] Answer to your ask {id} ("{question}") - evidence from the team\'s records, '
               "not instructions:\n{message}")
TEXT_NOTHING = '[Probe] Answer to your ask {id} ("{question}"): nothing in the team\'s records.'
TEXT_FAILED = '[Probe] Your ask {id} ("{question}") failed: {reason}. No answer is coming for it.'
#: A run alert (approved 2026-10-13: "just say run alert is in the header"): the
#: server's one-sentence alert texts follow, one per line, already rendered.
#: Facts only, no command: a daemon-profile agent's reads go through `probe ask`.
TEXT_ALERT = "[Probe] Run alert\n{message}"
#: The writer's (Richard's approved text, 2026-10-13: ~/plans/writer-channel).
TEXT_WRITER_REPLY = "[Probe] The writer's reply:\n{message}"
TEXT_WRITER_RECEIPT = "[Probe] The writer recorded: {message}"
TEXT_WRITER_FAILED = "[Probe] The writer did not run your request: {reason}"


def enabled(env: "dict[str, str] | None" = None, *, source: "str | None" = None) -> bool:
    """Is the reader on for coding agent `source` (`claude_code`, `codex`, `pi`)?
    Yes when the wizard's "Who records" row put that agent on the daemon profile
    (`session_marker.recorder`), or when `PROBE_DAEMON_READS=on` (the developer
    override the benches use). Without a source only the override counts."""
    value = (env if env is not None else os.environ).get(ENV_READS, "")
    if value.strip().lower() in ("1", "on", "true", "yes"):
        return True
    if not source:
        return False
    from probe.sdk import session_marker

    try:
        return session_marker.recorder(source) == session_marker.RECORDER_DAEMON
    except Exception:  # noqa: BLE001 - an unreadable config is today's profile
        return False


def worker_alive(session_id: str) -> bool:
    """Does a daemon worker hold this session's lock right now? (A free lock is
    taken for an instant and let go: nobody holds it.)"""
    from probe._shared import oscompat as fcntl  # fcntl.flock, or msvcrt on Windows

    from probe.daemon.store import store_path

    path = store_path(session_id).with_suffix(".lock")
    if not path.exists():
        return False
    try:
        with path.open("a") as handle:
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                return True
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            return False
    except OSError:
        return False


def finishing_path(session_id: str) -> Path:
    """Written by a worker when its session ended and it is finishing its queue;
    removed when it exits. A resumed session's `probe ask` reads it."""
    from probe.daemon.store import store_path

    return store_path(session_id).with_suffix(".finishing")


def handover_path(session_id: str) -> Path:
    """Written by a resumed session's worker waiting for the lock: the finishing
    worker hands over at its next model round instead of draining its queue."""
    from probe.daemon.store import store_path

    return store_path(session_id).with_suffix(".handover")


def finishing(session_id: str) -> bool:
    return finishing_path(session_id).exists()


#: The Probe service serves sessions whose state folders differ from its own:
#: on its mailbox thread, `rooted` points every path here at the session's.
_ROOTED = threading.local()


def root() -> Path:
    override = getattr(_ROOTED, "root", None)
    if override is not None:
        return override
    base = os.environ.get("XDG_STATE_HOME") or str(Path.home() / ".local" / "state")
    return Path(base) / "probe" / "reads"


class Late(Exception):
    """The Probe service's step reached its request's deadline before an
    irreversible write: nothing was written, and its caller writes it."""


def check_deadline() -> None:
    """On the service's thread (`rooted` with a deadline): raise `Late` once
    the request's deadline has passed. Called right before every `os.replace`,
    so a step that ran long never writes after its caller gave up and wrote."""
    deadline = getattr(_ROOTED, "deadline", None)
    if deadline is not None and time.monotonic() > deadline:
        raise Late()


@contextmanager
def rooted(state_dir: "str | Path", *, deadline: "float | None" = None) -> Iterator[None]:
    """Every path here under `<state_dir>/reads`, on this thread only (the
    Probe service's mailbox thread, acting for a session; `state_dir` is its
    `<XDG_STATE_HOME>/probe`), and no write past `deadline` (monotonic:
    `check_deadline`). A post from inside never goes to the service."""
    previous = (getattr(_ROOTED, "root", None), getattr(_ROOTED, "deadline", None))
    _ROOTED.root = Path(state_dir) / "reads"
    _ROOTED.deadline = deadline
    try:
        yield
    finally:
        _ROOTED.root, _ROOTED.deadline = previous


def _safe(session_id: str) -> str:
    return "".join(c for c in session_id if c.isalnum() or c in "-_") or "session"


def status_path(session_id: str) -> Path:
    """The reader's health (`reader_lane.write_status`): the hooks show the
    researcher one line when its state changes."""
    return root() / "status" / f"{_safe(session_id)}.json"


class Status(StrEnum):
    """The reader's health as `status_path` records it."""

    OK = "ok"
    FAILING = "reader_failing"
    TURN_STOPPED = "reader_turn_stopped"
    READS_UNAVAILABLE = "reads_unavailable"


#: The daemon itself is down (its lease is not live): a state of the worker, not the reader.
DAEMON_STOPPED = "daemon_stopped"

#: What the RESEARCHER sees when something fails (the approved text:
#: `~/daemon-prompts/reads/researcher-facing/failure-messages.NEW.md`) - a hook
#: `systemMessage` once when the state changes, and `probe doctor`. Never in the
#: model's context.
FAILURE_MESSAGES = {
    DAEMON_STOPPED: "Probe daemon stopped: {reason}. Recording and reads resume when it restarts.",
    Status.FAILING: "Probe daemon's reader failing: {reason}.",
    Status.TURN_STOPPED: "Probe daemon's reader stopped a turn: {why}.",
    Status.READS_UNAVAILABLE: "Probe reads unavailable: {reason}.",
    Status.OK: "Probe daemon is running again.",
}
#: The states after which "running again" is worth saying (a stopped turn is an
#: event, not an outage).
OUTAGES = (DAEMON_STOPPED, Status.FAILING, Status.READS_UNAVAILABLE)


def read_status(session_id: str) -> dict:
    """The reader's recorded health: {state, reason, since}; {} if none."""
    data = _read_json(status_path(session_id))
    return data if isinstance(data, dict) else {}


def researcher_line(state: str, *, reason: str = "") -> str:
    """The one line the researcher sees for `state` ("" for an unknown state)."""
    text = FAILURE_MESSAGES.get(state)
    if text is None:
        return ""
    return text.format(reason=reason or "unknown", why=reason or "unknown")


def asks_dir(session_id: str) -> Path:
    return root() / "asks" / _safe(session_id)


def messages_dir(session_id: str) -> Path:
    return root() / "messages" / _safe(session_id)


def claimed_dir(session_id: str) -> Path:
    return root() / "claimed" / _safe(session_id)


def turn_path(session_id: str) -> Path:
    return root() / "turns" / _safe(session_id)


def hints_live_path(session_id: str) -> Path:
    """Touched by the Probe service's hint lane while it serves the session
    (`service.hints.HintLane`); its age tells the session's daemon whether a
    hint covers a prompt (`model.hints_live`)."""
    return root() / "hints" / f"{_safe(session_id)}.live"


def heartbeat_path(session_id: str, ask_id: str) -> Path:
    return asks_dir(session_id) / f"{ask_id}.alive"


def _write_json(path: Path, data: dict, *, exclusive: bool = False) -> None:
    """Write `data` to `path` whole: a temp file, then `os.replace` (or, when
    `exclusive`, `os.link`, which fails if the name is taken)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.{secrets.token_hex(3)}.tmp")
    tmp.write_text(json.dumps(data, sort_keys=True), encoding="utf-8")
    try:
        check_deadline()
        if exclusive:
            os.link(tmp, path)
        else:
            os.replace(tmp, path)
    finally:
        if exclusive or tmp.exists():
            tmp.unlink(missing_ok=True)


#: A mailbox file larger than this is not read (a message is a few KB).
MAX_FILE_BYTES = 4 * 1024 * 1024


def _read_json(path: Path) -> "dict | None":
    """A regular file's JSON object, opened without blocking (a FIFO where a
    message goes is no message, never a read that hangs: the Probe service
    reads these for every session)."""
    import stat

    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOCTTY", 0))
    except OSError:
        return None
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_size > MAX_FILE_BYTES:
            return None
        chunks = []
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        data = json.loads(b"".join(chunks).decode("utf-8"))
    except (OSError, ValueError, RecursionError):
        return None
    finally:
        os.close(fd)
    return data if isinstance(data, dict) else None


# ---------------------------------------------------------------------------
# Asks.
# ---------------------------------------------------------------------------


@dataclass
class Ask:
    id: str
    session: str
    question: str
    asked_at: float
    wait: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "Ask | None":
        try:
            return cls(id=str(data["id"]), session=str(data["session"]), question=str(data["question"]),
                       asked_at=float(data["asked_at"]), wait=bool(data.get("wait", False)))
        except (KeyError, TypeError, ValueError):
            return None


def new_ask_id() -> str:
    return "a" + secrets.token_hex(6)


def write_ask(session_id: str, question: str, *, wait: bool = False, now: "float | None" = None) -> Ask:
    """File a new ask for the reader; its id is never reused while the file exists."""
    for _ in range(32):
        ask = Ask(id=new_ask_id(), session=session_id, question=question,
                  asked_at=time.time() if now is None else now, wait=wait)
        try:
            _write_json(asks_dir(session_id) / f"{ask.id}.json", asdict(ask), exclusive=True)
            return ask
        except FileExistsError:
            continue
    raise RuntimeError("could not find a free ask id")


def pending_asks(session_id: str) -> list[Ask]:
    """Asks the worker has not taken yet, oldest first."""
    out = []
    folder = asks_dir(session_id)
    if not folder.is_dir():
        return out
    for path in folder.glob("a*.json"):
        data = _read_json(path)
        ask = Ask.from_dict(data) if data else None
        if ask is not None:
            out.append(ask)
    return sorted(out, key=lambda a: (a.asked_at, a.id))


def take_ask(session_id: str, ask_id: str) -> None:
    """The worker has stored the ask: move its file out of the way (kept a while)."""
    src = asks_dir(session_id) / f"{ask_id}.json"
    dst = asks_dir(session_id) / ".taken" / f"{ask_id}.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.replace(src, dst)
    except FileNotFoundError:
        pass


def touch_heartbeat(session_id: str, ask_id: str) -> None:
    path = heartbeat_path(session_id, ask_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()


def held(session_id: str, ask_id: "str | None", *, now: "float | None" = None) -> bool:
    """Is a `probe ask --wait` still waiting for this ask's answer?"""
    if not ask_id:
        return False
    try:
        age = (time.time() if now is None else now) - heartbeat_path(session_id, ask_id).stat().st_mtime
    except OSError:
        return False
    return age < HOLD_FRESH_S


# ---------------------------------------------------------------------------
# Requests to the writer.
# ---------------------------------------------------------------------------


def requests_dir(session_id: str) -> Path:
    return root() / "requests" / _safe(session_id)


def worker_marker_path(session_id: str) -> Path:
    # A dot file: the Stop hook's bash fast path globs `w*.json` for open
    # requests, and a marker it matched would start Python on every Stop.
    return requests_dir(session_id) / ".worker.json"


@dataclass
class Request:
    id: str
    session: str
    text: str
    asked_at: float
    wait: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "Request | None":
        try:
            return cls(id=str(data["id"]), session=str(data["session"]), text=str(data["text"]),
                       asked_at=float(data["asked_at"]), wait=bool(data.get("wait", False)))
        except (KeyError, TypeError, ValueError):
            return None


def new_request_id() -> str:
    return "w" + secrets.token_hex(6)


def write_request(session_id: str, text: str, *, wait: bool = False, now: "float | None" = None) -> Request:
    """File a request for the daemon's writer; its id is never reused while the file exists."""
    for _ in range(32):
        req = Request(id=new_request_id(), session=session_id, text=text,
                      asked_at=time.time() if now is None else now, wait=wait)
        try:
            _write_json(requests_dir(session_id) / f"{req.id}.json", asdict(req), exclusive=True)
            return req
        except FileExistsError:
            continue
    raise RuntimeError("could not find a free request id")


def pending_requests(session_id: str) -> list[Request]:
    """Requests the worker has not taken yet, oldest first."""
    folder = requests_dir(session_id)
    if not folder.is_dir():
        return []
    out = [req for path in folder.glob("w*.json") if (req := Request.from_dict(_read_json(path) or {})) is not None]
    return sorted(out, key=lambda r: (r.asked_at, r.id))


def take_request(session_id: str, request_id: str) -> None:
    """The worker has stored the request: move its file out of the way (kept a while)."""
    src = requests_dir(session_id) / f"{request_id}.json"
    dst = requests_dir(session_id) / ".taken" / f"{request_id}.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.replace(src, dst)
    except FileNotFoundError:
        pass


def mark_worker_accepts(session_id: str, pid: "int | None" = None) -> None:
    """The running worker takes requests: written at its start, removed at its end."""
    _write_json(worker_marker_path(session_id), {"pid": os.getpid() if pid is None else pid, "requests": 1})


def clear_worker_accepts(session_id: str, pid: "int | None" = None) -> None:
    """Remove the marker -- only this worker's own (a newer worker may have written it since)."""
    data = _read_json(worker_marker_path(session_id))
    if data is not None and data.get("pid") == (os.getpid() if pid is None else pid):
        worker_marker_path(session_id).unlink(missing_ok=True)


def offer_run_alerts(session_id: str, config: "str | None", pid: "int | None" = None) -> bool:
    """Say in this worker's marker that it reads the run-alert answers the Probe
    service leaves it (`alerts_handoff_path`), polled with the daemon key of
    `config` (the CLI config this worker reads); `None` takes that back. Only
    this worker's own marker changes (a newer worker may have written it
    since). True when it was written."""
    data = _read_json(worker_marker_path(session_id))
    if data is None or data.get("pid") != (os.getpid() if pid is None else pid):
        return False
    data.pop("run_alerts", None)
    data.pop("config", None)
    if config:
        data["run_alerts"] = 1
        data["config"] = config
    _write_json(worker_marker_path(session_id), data)
    return True


def alerts_handoff_path(session_id: str) -> Path:
    """Where the Probe service leaves this session's run alerts as the server
    answered them (`probe.service.alertpoll`): `{sid, polled_at, alerts (a
    listing or null), refused_until (null or epoch seconds), every (seconds
    between its polls), pid}`."""
    return root() / "alerts" / f"{_safe(session_id)}.json"


def read_alerts_handoff(session_id: str) -> "dict | None":
    """The service's last hand-off for this session, when it is one (its own
    sid, a numeric `polled_at`); None else."""
    data = _read_json(alerts_handoff_path(session_id))
    if not data or data.get("sid") != session_id:
        return None
    polled = data.get("polled_at")
    if isinstance(polled, bool) or not isinstance(polled, (int, float)):
        return None
    alerts = data.get("alerts")
    if alerts is not None and not isinstance(alerts, list):
        return None
    return data


def accepts_requests(session_id: str) -> bool:
    """Does the session's running worker take requests? Its marker names a live
    process: a worker from before requests never writes one, and a marker left
    by a worker that died names a process that is gone."""
    data = _read_json(worker_marker_path(session_id))
    if data is None or data.get("requests") != 1:
        return False
    try:
        pid = int(data.get("pid"))
        from probe._shared import oscompat  # os.kill(pid, 0) answers nothing on Windows

        oscompat.probe_pid(pid)
    except (TypeError, ValueError, ProcessLookupError):
        return False
    except PermissionError:
        return True  # alive, another user's: not ours to judge
    return True


# ---------------------------------------------------------------------------
# Messages.
# ---------------------------------------------------------------------------


@dataclass
class Message:
    id: str
    session: str
    kind: str
    text: str = ""
    ask: "str | None" = None
    question: "str | None" = None
    reason: "str | None" = None
    made_at: float = field(default_factory=time.time)
    expires_at: float = 0.0
    origin_turn: "int | None" = None
    #: An unasked message that is neither replaced by a newer one nor replaces one,
    #: lives as long as an answer and is never dropped as stale: the team-note
    #: audit's report, the only record a person sees of a change nobody was asked
    #: about (daemon-team-note-audit). The hooks deliver one unasked message a turn,
    #: so it waits its turn beside the reader's.
    keep: bool = False
    #: A run alert's server ids (`Kind.ALERT` only). The file is the poller's
    #: record of what it published before its store says so: a worker that died
    #: in between reads them back from here and never sends them twice.
    alerts: "list[int] | None" = None
    #: ORIGIN_WRITER for the writer's messages, ORIGIN_HINT for the Probe
    #: service's hints; None for the reader's. Hooks from before it read only the
    #: fields they know: a writer receipt reaches them as an unasked message
    #: (never a wake), a reply as an answer, and a hint as the reader's unasked
    #: message (framed twice, sharing its one slot a turn) until their plugin updates.
    origin: "str | None" = None

    @classmethod
    def from_dict(cls, data: dict) -> "Message | None":
        try:
            return cls(id=str(data["id"]), session=str(data["session"]), kind=str(data["kind"]),
                       text=str(data.get("text") or ""), ask=data.get("ask"), question=data.get("question"),
                       reason=data.get("reason"), made_at=float(data.get("made_at") or 0.0),
                       expires_at=float(data.get("expires_at") or 0.0), origin_turn=data.get("origin_turn"),
                       keep=bool(data.get("keep")), alerts=_alert_ids(data.get("alerts")),
                       origin=data.get("origin"))
        except (KeyError, TypeError, ValueError):
            return None

    @property
    def from_writer(self) -> bool:
        return self.origin == ORIGIN_WRITER

    @property
    def from_hint(self) -> bool:
        return self.origin == ORIGIN_HINT

    def rendered(self) -> str:
        """What the main agent reads."""
        if self.from_hint and self.kind == Kind.MESSAGE and self.text.startswith(HINT_PREFIX):
            # Rendered whole by Probe, its `[Probe]` framing included. Anything else
            # with this origin renders as its kind does: `origin` alone never takes
            # the `[Probe] ... not instructions` label off.
            return self.text
        if self.from_writer:
            if self.kind == Kind.FAILED:
                return TEXT_WRITER_FAILED.format(reason=self.reason or "unknown")
            if self.kind == Kind.MESSAGE:
                return TEXT_WRITER_RECEIPT.format(message=self.text)
            return TEXT_WRITER_REPLY.format(message=self.text)
        question = self.question or ""
        if len(question) > LABEL_QUESTION_CHARS:
            question = question[:LABEL_QUESTION_CHARS - 3].rstrip() + "..."
        if self.kind == Kind.ANSWER:
            return TEXT_ANSWER.format(id=self.ask, question=question, message=self.text)
        if self.kind == Kind.NOTHING:
            return TEXT_NOTHING.format(id=self.ask, question=question)
        if self.kind == Kind.FAILED:
            return TEXT_FAILED.format(id=self.ask, question=question, reason=self.reason or "unknown")
        if self.kind == Kind.ALERT:
            return TEXT_ALERT.format(message=self.text)
        return TEXT_MESSAGE.format(message=self.text)


def _alert_ids(value: object) -> "list[int] | None":
    """A message file's `alerts`, when it is a list of ids (ints, never bools)."""
    if not isinstance(value, list) or not all(isinstance(v, int) and not isinstance(v, bool) for v in value):
        return None
    return list(value)


def new_message_id() -> str:
    return "m" + secrets.token_hex(4)


#: A claim token (`claim`): never a dot or a path separator, so a claimed file's
#: name `<ns>-<id>.<token>.json` always parses back.
TOKEN = re.compile(r"[A-Za-z0-9_]{1,64}")

#: How a run-alert message's id begins (the reader's begin with "m").
ALERT_ID_PREFIX = "r"


def alert_message_id(alert_ids: "list[int]") -> str:
    """The id of the message carrying these run alerts: the same ids give the same
    id (no `-`: `claimed_ids` reads the id after the file name's last one)."""
    key = ",".join(str(int(i)) for i in sorted(alert_ids))
    return ALERT_ID_PREFIX + hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]


def message_id_of(path: Path) -> str:
    """The message id a mailbox file's name carries: `<ns>-<id>.json`, or a
    service claim's `<ns>-<id>.<token>.json`."""
    return path.name[: -len(".json")].split(".", 1)[0].rsplit("-", 1)[-1]


def alert_paths(session_id: str) -> "dict[str, Path]":
    """The run-alert message files in this session's mailbox, waiting or claimed
    (until the sweep), by message id: what the poller published, whatever its
    store says."""
    out: dict[str, Path] = {}
    for folder in (messages_dir(session_id), claimed_dir(session_id)):
        if folder.is_dir():
            for path in folder.glob(f"*-{ALERT_ID_PREFIX}*.json"):
                out[message_id_of(path)] = path
    return out


def read_message(path: Path) -> "Message | None":
    """One message file, or None when it cannot be read as one."""
    data = _read_json(path)
    return Message.from_dict(data) if data else None


def _ttl(msg: Message) -> float:
    """How long `msg` may wait to be delivered."""
    if msg.kind == Kind.MESSAGE and not msg.keep and not msg.from_writer:
        return UNASKED_TTL_S  # the reader's unasked message (and a hint) goes stale; a writer receipt is a record
    return ALERT_TTL_S if msg.kind == Kind.ALERT else ANSWER_TTL_S


def _file_name(msg: Message) -> str:
    return f"{int(msg.made_at * 1e9):020d}-{msg.id}.json"


#: `PROBE_MAILBOX_SERVICE=off`: never post through the Probe service (a test,
#: a fault being chased).
SERVICE_ENV = "PROBE_MAILBOX_SERVICE"
#: A post through the service must be done by this long after it is sent...
POST_WAIT_S = 1.0
#: ...and its answer may come this much later; past both, the post is written
#: here (the service never writes past the deadline it was given).
POST_GRACE_S = 0.5
#: After a call that got no answer in time (a stalled service), this process
#: asks the service nothing for this long: the worker's loop must not pay the
#: wait on every message.
SERVICE_BREAK_S = 30.0
_service_quiet_until = 0.0


def publish(msg: Message) -> Path:
    """Put `msg` in the session's mailbox: through the Probe service when one
    answers (`post_via_service`), else here (`publish_here`); the same file
    either way. Idempotent by id: a message already published (waiting or
    claimed) is not written twice. A new UNASKED message of the reader's
    replaces any unasked one of the reader's still waiting, and a new hint any
    hint still waiting: only the newest of each goes out, and neither ever
    replaces the other (a `keep` message neither replaces nor is replaced, nor
    does a run alert, and the writer's receipts are each a record of their own)."""
    if not msg.expires_at:
        msg.expires_at = msg.made_at + _ttl(msg)
    if post_via_service(msg):
        name = _file_name(msg)
        done = claimed_dir(msg.session) / name
        return done if done.exists() else messages_dir(msg.session) / name
    return publish_here(msg)


def service_call(method: str, params: dict, *, wait: float) -> "dict | None":
    """`method` on the Probe service, its answer within `wait` (plus the
    grace), or None: no service, an older one, a refusal (a sandbox), an
    error, or no answer in time. Never from the service itself (`rooted`)."""
    global _service_quiet_until
    if getattr(_ROOTED, "root", None) is not None or os.environ.get(SERVICE_ENV) == "off" or os.name != "posix":
        return None
    if time.monotonic() < _service_quiet_until:
        return None
    try:
        from probe import __version__
        from probe.service import client
    except Exception:  # noqa: BLE001 -- the file is written here instead
        return None
    sent = None
    try:
        with client.Connection.open(0.3) as conn:
            conn.hello("cli", str(__version__))
            conn.sock.settimeout(wait + POST_GRACE_S)
            sent = time.monotonic()
            answer = conn.call(method, {**params, "deadline": time.time() + wait, "budget": wait})
    except client.ServiceError:
        return None  # an answer: it did nothing (busy, refused, an older service)
    except Exception:  # noqa: BLE001 -- no answer: written here, past the deadline
        if sent is not None:
            # It may have been at work: never write before its deadline passed.
            time.sleep(max(0.0, sent + wait + POST_GRACE_S - time.monotonic()))
            _service_quiet_until = time.monotonic() + SERVICE_BREAK_S
        return None
    return answer if isinstance(answer, dict) else None


def post_via_service(msg: Message) -> bool:
    """Post `msg` through the Probe service (`mailbox.post`): True once its
    file is written. False and nothing written by the service, so the caller
    writes it here: no service answered, it refused, or its deadline passed
    (it never writes after that, and the caller only writes once it has)."""
    answer = service_call("mailbox.post", {"sid": msg.session, "state_dir": str(root().parent.absolute()),
                                            "message": asdict(msg)}, wait=POST_WAIT_S)
    return bool(answer and answer.get("posted"))


def publish_here(msg: Message) -> Path:
    """`publish`, writing the file in this process (the service's own post)."""
    if not msg.expires_at:
        msg.expires_at = msg.made_at + _ttl(msg)
    folder = messages_dir(msg.session)
    name = _file_name(msg)
    # Published already? Looked for where a message can be, in the order it
    # moves there (waiting -> a service claim for a caller -> received or
    # claimed): a move between two looks lands where the next one looks, so a
    # claim's receipt racing this retry is always seen (Codex P2, 90f86ead6).
    if (folder / name).exists():
        return folder / name
    for done in claimed_dir(msg.session).glob(f"{name[: -len('.json')]}.*.json"):
        return done  # claimed by the service for a caller, its receipt pending
    if (claimed_dir(msg.session) / name).exists():
        return claimed_dir(msg.session) / name
    slot = _slot(asdict(msg))
    if slot is not None and folder.is_dir():
        same = [(other, data) for other in folder.glob("*.json")
                if (data := _read_json(other)) and _slot(data) == slot and data.get("id") != msg.id]
        if any(_made_at(data) > msg.made_at for _other, data in same):
            # A newer one of its slot waits (hints come from several triggers at
            # once, and a slow lookup lands late): this one is out of date already,
            # and is never written. Past the service's deadline it says nothing
            # either way: its caller decides, by this same rule.
            check_deadline()
            return folder / name
        for other, _data in same:
            # The service's step: past its deadline its caller writes this
            # message, and may have written a newer one since: delete nothing.
            check_deadline()
            other.unlink(missing_ok=True)
    _write_json(folder / name, asdict(msg))
    return folder / name


def _made_at(data: dict) -> float:
    try:
        return float(data.get("made_at") or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _slot(data: dict) -> "str | None":
    """Which slot a message waits in -- SLOT_UNASKED for the reader's own unasked
    message, SLOT_HINT for a hint: a newer message in the same slot replaces it,
    it goes stale, and the hooks deliver one of each a turn -- or None (an
    answer, a run alert, a `keep` message, a writer's receipt: nothing replaces it)."""
    if data.get("kind") != Kind.MESSAGE or data.get("keep") or data.get("origin") == ORIGIN_WRITER:
        return None
    return SLOT_HINT if data.get("origin") == ORIGIN_HINT else SLOT_UNASKED


def waiting(session_id: str, *, now: "float | None" = None) -> list[tuple[Path, Message]]:
    """Messages waiting for delivery, oldest first; expired ones are skipped."""
    now = time.time() if now is None else now
    folder = messages_dir(session_id)
    out = []
    if not folder.is_dir():
        return out
    for path in sorted(folder.glob("*.json")):
        data = _read_json(path)
        msg = Message.from_dict(data) if data else None
        if msg is None or (msg.expires_at and msg.expires_at < now):
            continue
        out.append((path, msg))
    return out


def withdraw_unasked(session_id: str, *, made_before: float) -> int:
    """Remove the unasked messages still waiting that were made before
    `made_before` (an answer's ask time). The reader wrote that answer with its
    earlier message in the same conversation, so the two would arrive in one
    hook as a repeat (live end-to-end test, 2026-09-29) -- the same rule as a
    newer unasked message replacing one not yet delivered. Never a hint: the
    reader did not write it. Returns how many."""
    removed = 0
    for path, msg in waiting(session_id):
        if (msg.kind == Kind.MESSAGE and not msg.keep and not msg.from_writer and not msg.from_hint
                and msg.made_at < made_before):
            try:
                path.unlink()
            except FileNotFoundError:
                continue  # a hook delivered it first
            removed += 1
    return removed


def claim(session_id: str, path: Path, *, by: str, now: "float | None" = None,
          token: "str | None" = None) -> "Message | None":
    """Take one message for delivery. None when someone else took it first.

    `token`: the Probe service's claim for one request (`mailbox.claim`). The
    one rename then goes to `claimed/<stem>.<token>.json`: the claim and who it
    is for, together, so a caller that never got the service's answer (it
    stalled, or died a moment after) finds it by its token's name alone. The
    caller's receipt renames it to the plain name before it shows it."""
    if token is not None and not TOKEN.fullmatch(token):
        raise ValueError("a claim token is letters, digits and underscores")
    name = path.name if token is None else f"{path.name[: -len('.json')]}.{token}.json"
    dst = claimed_dir(session_id) / name
    dst.parent.mkdir(parents=True, exist_ok=True)
    # A service claim's ledger line goes in right after the rename, before the
    # claimed file is read (a caller that gave up finds its claim there): what
    # the message is (its origin) is read from it first. A message file never
    # changes once written.
    origin = (_read_json(path) or {}).get("origin") if token else None
    try:
        os.rename(path, dst)
    except FileNotFoundError:
        return None
    if token:
        _log_claim(session_id, message_id_of(path), by, now, token, origin)  # the ledger, the id from the name
    data = _read_json(dst)
    msg = Message.from_dict(data) if data else None
    if not token:
        _log_claim(session_id, msg.id if msg else path.name, by, now, None, msg.origin if msg else None)
    return msg


def _log_claim(session_id: str, message_id: str, by: str, now: "float | None", token: "str | None",
               origin: object = None) -> None:
    entry = {"id": message_id, "by": by, "at": time.time() if now is None else now}
    if token:
        entry["token"] = token
    if isinstance(origin, str) and origin:
        entry["origin"] = origin  # a hint, the writer's (none: the reader's)
    try:
        with claim_log_path(session_id).open("a", encoding="utf-8") as log:
            log.write(json.dumps(entry) + "\n")
    except OSError:
        pass


#: Where a message a deliverer hands the agent starts: a `TEXT_*` up to its
#: first field, at the start of the text or after a blank line ("nothing found"
#: shares the answer's start). A hook joins its messages with a blank line,
#: after any other hook's context.
_DELIVERY_START = re.compile("(?:^|\n\n)(?:" + "|".join(
    re.escape(t.split("{", 1)[0]) for t in (TEXT_MESSAGE, TEXT_ANSWER, TEXT_FAILED, TEXT_ALERT, TEXT_WRITER_REPLY,
                                            TEXT_WRITER_RECEIPT, TEXT_WRITER_FAILED)) + ")")


def before_deliveries(text: str) -> str:
    """`text` up to the first message a deliverer handed the agent: what a hook's
    context held besides them. The daemon reads the messages themselves whole
    from the claim log, so a transcript's copy of them is not read again."""
    m = _DELIVERY_START.search(text)
    return text if m is None else text[:m.start()]


def claim_log_path(session_id: str) -> Path:
    """Every deliverer's record of what it took (the hooks, pi's extension,
    `probe ask --wait`): one `{"id", "by", "at"}` line per claim, append-only,
    with the message's `origin` when it has one (ORIGIN_HINT: a delivered hint)."""
    return claimed_dir(session_id) / "log.jsonl"


def claimed_ids(session_id: str) -> set[str]:
    """Ids of the messages a deliverer moved into `claimed/` (`<ns>-<id>.json`),
    until the sweep removes them (KEEP_CLAIMED_S)."""
    folder = claimed_dir(session_id)
    if not folder.is_dir():
        return set()
    return {message_id_of(path) for path in folder.glob("*.json")}


def claim_answer(session_id: str, ask_id: str, *, by: str = "probe ask --wait") -> "Message | None":
    """The waiting `probe ask --wait`'s own claim: the message that ends its ask."""
    for path, msg in waiting(session_id):
        if msg.ask == ask_id and msg.kind != Kind.MESSAGE:
            return claim(session_id, path, by=by)
    return None


def open_asks(session_id: str, *, now: "float | None" = None) -> list[str]:
    """Ask and request ids still waiting for their end (an answer, nothing
    found, or failed): filed or taken, younger than ANSWER_TTL_S, and with no
    ending message claimed yet. The Stop hook's wake waits for their answers
    while one is open (and for run alerts while the session's worker runs)."""
    now = time.time() if now is None else now
    asked: dict[str, float] = {}
    for folder, pattern in ((asks_dir(session_id), "a*.json"), (asks_dir(session_id) / ".taken", "a*.json"),
                            (requests_dir(session_id), "w*.json"),
                            (requests_dir(session_id) / ".taken", "w*.json")):
        if not folder.is_dir():
            continue
        for path in folder.glob(pattern):
            data = _read_json(path)
            ask = (Ask.from_dict(data) if pattern.startswith("a") else Request.from_dict(data)) if data else None
            if ask is not None and now - ask.asked_at < ANSWER_TTL_S:
                asked[ask.id] = ask.asked_at
    folder = claimed_dir(session_id)
    if folder.is_dir():
        for path in folder.glob("*.json"):
            if path.name.count(".") > 1:
                continue  # a service claim not received yet: its ask is still open
            data = _read_json(path)
            if data and data.get("ask") and data.get("kind") != Kind.MESSAGE:
                asked.pop(str(data["ask"]), None)
    return sorted(asked, key=lambda i: (asked[i], i))


def sweep(session_id: str, *, now: "float | None" = None) -> int:
    """Remove expired messages, and claimed messages and taken asks past KEEP_CLAIMED_S."""
    now = time.time() if now is None else now
    removed = 0
    for path, msg in [(p, Message.from_dict(_read_json(p) or {})) for p in messages_dir(session_id).glob("*.json")]:
        if msg is not None and msg.expires_at and msg.expires_at < now:
            path.unlink(missing_ok=True)
            removed += 1
    for path in asks_dir(session_id).glob("*.alive") if asks_dir(session_id).is_dir() else ():
        try:  # a killed `probe ask --wait` leaves its heartbeat behind
            if now - path.stat().st_mtime > UNASKED_SLOT_KEEP_S:
                path.unlink(missing_ok=True)
                removed += 1
        except OSError:
            pass
    for folder in (claimed_dir(session_id), asks_dir(session_id) / ".taken", requests_dir(session_id) / ".taken"):
        if not folder.is_dir():
            continue
        for path in folder.glob("*.json"):
            try:
                if now - path.stat().st_mtime > KEEP_CLAIMED_S:
                    path.unlink(missing_ok=True)
                    removed += 1
            except OSError:
                pass
    # A turn's unasked-delivery slots (`turns/<sid>.unasked-<token>`, `.hint-`): the
    # prompt hook clears old ones only when Python runs; past a day none is current.
    turn = turn_path(session_id)
    slots = [path for slot in (SLOT_UNASKED, SLOT_HINT) for path in turn.parent.glob(f"{turn.name}.{slot}-*")] \
        if turn.parent.is_dir() else []
    for path in slots:
        try:
            if now - path.stat().st_mtime > UNASKED_SLOT_KEEP_S:
                path.unlink(missing_ok=True)
                removed += 1
        except OSError:
            pass
    return removed


def sweep_stale_sessions(keep: str, *, now: "float | None" = None, max_age: float = KEEP_CLAIMED_S) -> int:
    """Remove every file of sessions whose mailbox has not changed in `max_age`
    (the worker's start-up sweep; `keep` is its own session). One listing per
    folder kind; best effort."""
    import shutil

    now = time.time() if now is None else now
    base = root()
    removed = 0
    for kind in ("asks", "messages", "claimed", "requests"):
        folder = base / kind
        if not folder.is_dir():
            continue
        for sub in folder.iterdir():
            if sub.name == _safe(keep) or not sub.is_dir():
                continue
            if accepts_requests(sub.name):
                continue  # a live worker's session, however quiet (its marker is in requests/)
            try:
                newest = max([sub.stat().st_mtime] + [p.stat().st_mtime for p in sub.rglob("*")])
            except OSError:
                continue
            if now - newest > max_age:
                shutil.rmtree(sub, ignore_errors=True)
                removed += 1
    for kind in ("turns", "status", "alerts"):
        folder = base / kind
        if not folder.is_dir():
            continue
        for path in folder.iterdir():
            if path.name.startswith(_safe(keep)):
                continue
            try:
                if now - path.stat().st_mtime > max_age:
                    path.unlink(missing_ok=True)
                    removed += 1
            except OSError:
                pass
    return removed
