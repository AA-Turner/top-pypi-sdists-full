"""Hints: the team's nearest records, shown to a coding agent (Probe hints T3).

When a session's researcher prompt, a peer agent's message, a web search or a
Probe run launch looks near the team's work, the agent is shown the few team
records nearest to it at its next prompt or tool call. The lookup runs here,
once per machine, and never blocks anything:

    the feed      every session a recorder of this service holds now
                  (`recorders.py`; its claim held, so not while capture is off,
                  the folder is disabled or another recorder has it), registered
                  live and unconfined, not `off`. Its recorder is the tap's loop
                  (`tap.hosted`), which reads the transcript into the journal and
                  hands no line out, so this lane keeps its own offset in the
                  same file: one stat a second per session, and only the new
                  bytes read (the page cache has them: the recorder just read
                  them). New whole lines are parsed with the daemon's adapter
                  (`probe.daemon.adapters`, the worker's parse) and its
                  `.probe.config` filter (`exclusions.Filter`, the worker's), so
                  the events are the daemon's. A session first seen starts near
                  its end: only lines younger than FRESH_S there count
    triggers      a researcher prompt (`prompt`); a peer agent's message (META,
                  tool `events.PEER_TOOL`, `peer`; its sender's session excluded,
                  found from its socket in Claude Code's `sessions/<pid>.json`:
                  the sender's own transcript holds the message it sent); a
                  WebSearch / WebFetch call (`search`); a shell call that starts
                  a Probe run for certain: `probe exec` opening a new run, or
                  `probe run start` (`command`). Nothing else
    the lookup    POST /v1/hints on one kept connection, with the read-only key
                  of the session's CLI config (KEYS), TIMEOUT_S, failing open:
                  no answer is no hint. The text goes through the capture's
                  secret scan first (`scrubbed`), as all transcript text that
                  leaves the machine does. `ml` is the session's ML gate (the
                  daemon worker's store facts, read only) or null
    limits        one request per session per SESSION_GAP_S (a newer trigger
                  replaces the one waiting, but a search or a command never a
                  prompt or a peer's message); a token bucket for the machine
                  (BUCKET_PER_MIN, BUCKET_BURST); holds as `alertpoll` keeps
                  them (`_scopes`): a 429 holds that key on that server
                  LIMITED_S, a 401 / 403 the key REFUSED_S, a 404 the server
                  MISSING_S; `mode: off` quiets that key on that server
                  OFF_RECHECK_S for every session; the last REPEATS texts of a
                  session are never sent again
    delivery      `fire` with a `hint` (as Probe rendered it, at most
                  MAX_HINT_CHARS: a longer one is dropped whole): an unasked
                  message with origin
                  `mailbox.ORIGIN_HINT` (a slot of its own beside the reader's),
                  posted in this process with the mailbox
                  service's own step (`MailHost.post`); the reads hook hands it
                  over at the agent's next prompt or tool call (daemon and inline
                  sessions: both plugins run it). Never when every record in it
                  was delivered to the session already (the claim log, and a
                  ledger of which records each hint carried) or is waiting in
                  one; a record whose date changed counts as new. Those records'
                  doc ids go with each request (`exclude_doc_ids`) for the
                  server to leave out. A newer researcher prompt, or the end of
                  the agent's turn, withdraws a hint still waiting
    off           PROBE_HINTS=off in a session's environment (its recorder's
                  `env`: every PROBE_* variable the agent's shell had), or in
                  the service's own

One log line per lookup (trigger, mode, fire, reason, top score, latency,
delivered or why not), never the text. Two daemon threads of its own (the tail,
the lookups), neither waited for at exit; both idle without a timer while no
session is followed; everything they do is caught and logged.

Stdlib only at import (the service's start path); the daemon's adapters, its
filter and the mailbox are imported on the lane's threads.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import re
import secrets
import shlex
import stat
import threading
import time
from collections import Counter, OrderedDict
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

from .alertpoll import Endpoint, Fetcher, endpoint
from .protocol import Mode

#: `off` (or 0 / false / no) in the service's environment, or in a session's,
#: turns the lane off there.
HINTS_ENV = "PROBE_HINTS"
ROUTE = "/v1/hints"
#: Every followed transcript is looked at this often.
POLL_S = 1.0
#: A served session's hint marker (`mailbox.hints_live_path`) is touched at most
#: this often; its daemon reads one older than `model.HINTS_LIVE_TTL_S` (120 s)
#: as no hint lane here, and its reader wakes at prompts again.
HINTS_LIVE_BEAT_S = 30.0
#: Test-only: a shorter POLL_S (nothing in production sets it).
POLL_ENV = "PROBE_SERVICE_HINTS_POLL_S"
#: One request, connect to last byte.
TIMEOUT_S = 5.0
#: The most text a request carries (the contract's client limit).
MAX_TEXT_CHARS = 8000
#: The longest hint posted: one the server sends longer is dropped whole, never
#: cut mid-line into the agent's context (Probe renders ~170 chars a record).
MAX_HINT_CHARS = 4000
#: Text kept past MAX_TEXT_CHARS for the secret scan, so a credential the cut
#: would split is found whole first (a PEM private key runs ~1.7 kB).
SCAN_MARGIN_CHARS = 4096
#: One request per session per this long; a newer trigger replaces a waiting one
#: (a search or a command never a prompt or a peer's message: _ASKED_FIRST).
SESSION_GAP_S = 10.0
#: The machine's token bucket.
BUCKET_PER_MIN = 20.0
BUCKET_BURST = 5.0
#: A 429 holds that key on that server this long (as `alertpoll`, never the machine).
LIMITED_S = 60.0
#: `mode: off` (the team's setting): that key on that server is not asked again
#: for this long, from any session of this machine.
OFF_RECHECK_S = 10 * 60.0
#: The server refused the key (401 / 403): that key waits this long, on every server.
REFUSED_S = 5 * 60.0
#: A server without the route (404, a CLI ahead of its API): that server waits as long as `off`.
MISSING_S = OFF_RECHECK_S
#: The most record doc ids a request names as shown already (`exclude_doc_ids`).
MAX_EXCLUDE_DOC_IDS = 50
#: A session's last this-many request texts are never sent again (R16).
REPEATS = 32
#: Sessions with a lookup waiting, at most: the oldest goes past it.
MAX_PENDING = 64
#: One read of a transcript, at most; a line longer than this is skipped.
MAX_READ_BYTES = 2 * 1024 * 1024
#: A session first seen is read from this far before its end...
INITIAL_BACK_BYTES = 64 * 1024
#: ...and there only lines this young (by their own stamp) trigger: a first
#: prompt written just before the lane looked, never the history of a resumed one.
FRESH_S = 30.0
#: A Codex session names a folder: its rollout is looked for this often until found.
RESOLVE_EVERY_S = 15.0
#: The CLI config's credentials, the read-only one first: the route only reads.
KEYS = ("mcp_token", "token", "companion_token")
WEB_SEARCH = "WebSearch"
WEB_FETCH = "WebFetch"
MAIN_STREAM = "main"
#: Where each hint's records are kept (`<service dir>/hints/<sid>.jsonl`), and
#: for how long (`mailbox.KEEP_CLAIMED_S`: the claim log's own files).
LEDGER_DIR = "hints"
KEEP_LEDGER_S = 7 * 24 * 3600.0
#: Ledgers past KEEP_LEDGER_S are looked for at most this often.
SWEEP_EVERY_S = 24 * 3600.0
LEDGER_TAIL_BYTES = 256 * 1024
CLAIM_LOG_TAIL_BYTES = 256 * 1024
#: Only a session id is excluded for a peer's message: a name could match any doc id.
_SESSION_ID = re.compile(r"[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}")
#: A peer's address in its event's `command`: `<name> (uds:<socket>)`.
_ADDRESS = re.compile(r"\((uds:[^()]+)\)\s*\Z")
#: Claude Code's socket for a session, `<pid>.sock` (`/run/user/<uid>/cc-socks/`,
#: older builds `/tmp/cc-socks/`), and its record of the session, `<pid>.json`.
_SOCKET_PID = re.compile(r"(\d+)\.sock")
#: Claude Code's session records looked through for one socket, at most, and
#: the size of one (a few hundred bytes).
MAX_SESSION_FILES = 512
MAX_SESSION_FILE_BYTES = 64 * 1024
#: A sender found is remembered this long (a pid, and so a socket, is reused
#: only by a later process); one not found is looked for again after SENDER_MISS_S.
SENDER_KEEP_S = 10 * 60.0
SENDER_MISS_S = 30.0
MAX_SENDERS = 256
#: What a shell runs in front of a command it starts.
_WRAPPERS = frozenset({"env", "nohup", "time", "command", "exec", "nice", "stdbuf", "caffeinate"})
#: `probe exec`'s options that take a value, and those that open a run here.
_EXEC_VALUES = frozenset({"--cwd", "--project", "--experiment", "--slug", "--name", "--description", "--tag",
                          "--external-id", "--config", "--parent", "--relation", "--intent", "--authored-by",
                          "--launcher", "--outputs", "--input", "--output"})
_EXEC_OPENS = frozenset({"--project", "--experiment", "--slug", "--name", "--description", "--tag",
                         "--external-id", "--config", "--intent"})
_HELP = frozenset({"--help", "-h"})
_SHELL_OPERATORS = frozenset({"&&", "||", ";", "|", "&", "(", ")", ";;", "|&"})
#: A shell line longer than this is never read as a launch: `gate.shell_part`
#: is quadratic in heredoc markers (32 kB of them take seconds), and the tail
#: thread reads every session.
MAX_COMMAND_CHARS = MAX_TEXT_CHARS
#: A "prompt" that is no researcher's message: a `!command` (Claude Code's
#: bash-mode turns, Codex's `<user_shell_command>`), whose output the capture
#: withholds (the consent screen), or a `[Probe]` message the agent was handed.
_NOT_PROMPTS = ("<bash-input>", "<bash-stdout>", "<bash-stderr>", "<user_shell_command>", "[Probe]")
#: The CLI's environment overrides of the config's endpoint and keys
#: (`sdk.config.resolve`, `daemon.model.endpoint`): a session with one talks to
#: another deployment or as another key, so the lane never asks for it.
_ENV_OVERRIDES = ("PROBE_BASE_URL", "PROBE_MCP_TOKEN", "PROBE_TOKEN", "PROBE_DAEMON_KEY")


class Trigger:
    PROMPT = "prompt"
    PEER = "peer"
    SEARCH = "search"
    COMMAND = "command"


#: The triggers a waiting lookup is never replaced by a search or a command for
#: (the server's `prompt` class: the one shown before the others are calibrated).
_ASKED_FIRST = frozenset({Trigger.PROMPT, Trigger.PEER})


class Skip:
    """Why a hint that fired was not posted (the log line and `stats`)."""

    STALE = "stale"  # a newer researcher prompt came while it was looked up
    REPEAT = "repeat"  # every record in it was delivered, or waits in a hint
    NOT_POSTED = "not_posted"  # the mailbox step wrote nothing
    TOO_LONG = "too_long"  # longer than MAX_HINT_CHARS: dropped whole


def disabled(env) -> bool:
    return str(env.get(HINTS_ENV) or "").strip().lower() in ("off", "0", "false", "no")


def _poll_interval() -> float:
    try:
        value = float(os.environ.get(POLL_ENV) or POLL_S)
    except ValueError:
        return POLL_S
    return value if value > 0 else POLL_S


def _safe(sid: str) -> str:
    """`probe.daemon.mailbox._safe`: a session id as a file stem."""
    return "".join(c for c in sid if c.isalnum() or c in "-_") or "session"


def _epoch(stamp: object) -> float | None:
    if not isinstance(stamp, str) or not stamp:
        return None
    try:
        return datetime.fromisoformat(stamp.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


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


# -- triggers ---------------------------------------------------------------------


def _segments(text: str) -> list[list[str]]:
    """A shell line's simple commands, as words; [] when any line of it cannot
    be split. `text` is `gate.shell_part`'s (quoted strings and heredoc bodies
    blanked), so a newline left in it ends a command, as `;` does."""
    segments: list[list[str]] = [[]]
    for line in text.replace("\\\n", " ").split("\n"):
        lexer = shlex.shlex(line, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        lexer.commenters = ""
        segments.append([])
        try:
            for token in lexer:
                if token in _SHELL_OPERATORS or (token and set(token) <= set("&|;()")):
                    segments.append([])
                else:
                    segments[-1].append(token)
        except ValueError:
            return []  # an unbalanced quote: nothing in it is certain
    return [s for s in segments if s]


def _probe_args(words: list[str]) -> list[str] | None:
    """The arguments of `probe` when it is the command these words run
    (after variable assignments and plain wrappers: `env`, `nohup`, `uv run`)."""
    i = 0
    while i < len(words):
        word = words[i]
        name = os.path.basename(word)
        if "=" in word and not word.startswith("-") and re.match(r"[A-Za-z_][A-Za-z0-9_]*=", word):
            i += 1
        elif name in _WRAPPERS:
            i += 1
            while i < len(words) and (words[i].startswith("-") or (name == "env" and "=" in words[i])):
                i += 1
        elif name == "uv" and i + 1 < len(words) and words[i + 1] == "run":
            i += 2
            while i < len(words) and words[i].startswith("-"):
                i += 1
        elif name == "probe":
            return words[i + 1:]
        else:
            return None
    return None


def _opens_with_exec(args: list[str]) -> bool:
    """`probe exec <args>`: does it open a NEW run? `probe exec RUN -- cmd`
    takes one that exists (as the CLI reads it: a word before `--` is the run,
    unless an option that opens one here is given; then it starts the command)."""
    if "--" in args:
        own, command = args[: args.index("--")], args[args.index("--") + 1:]
    else:
        own, command = args, []
    if any(a in _HELP for a in own):
        return False
    words: list[str] = []
    opens = False
    i = 0
    while i < len(own):
        arg = own[i]
        name = arg.split("=", 1)[0]
        if arg.startswith("-"):
            opens = opens or name in _EXEC_OPENS
            i += 2 if name in _EXEC_VALUES and "=" not in arg else 1
            continue
        words.append(arg)
        i += 1
    if "--" in args:
        return bool(command) and (not words or opens)
    return opens and bool(words)


def launches_run(command: str) -> bool:
    """Does this shell line certainly start a Probe run: `probe exec` opening
    a new one, or `probe run start` (never with `--help`)? Text a command only
    writes (heredoc bodies, quoted strings) is not read as run."""
    if not command or len(command) > MAX_COMMAND_CHARS or "probe" not in command:
        return False
    try:
        from probe.daemon.gate import shell_part

        text = shell_part(command)
    except Exception:  # noqa: BLE001 -- unparsable: nothing is certain
        return False
    for words in _segments(text):
        args = _probe_args(words)
        if not args:
            continue
        if args[0] == "exec" and _opens_with_exec(args[1:]):
            return True
        if args[:2] == ["run", "start"] and not any(a in _HELP for a in args[2:]):
            return True
    return False


def sender_of(event) -> str | None:
    """A peer message's sender as the harness gave it: `uds:<socket>` (another
    Claude Code session), a session id, or a helper agent's id or path."""
    args = event.tool_input or {}
    sender = args.get("from") if isinstance(args.get("from"), str) else None
    if not sender:
        command = event.command() or ""
        hit = _ADDRESS.search(command)
        sender = hit.group(1) if hit else command
    return sender.strip() or None


def trigger_of(event) -> tuple[str, str, list[str]] | None:
    """`(trigger, text, its senders)` for an event that asks for a lookup, else
    None. A sender is an address the lane resolves to a session to exclude
    (`Senders`)."""
    from probe.daemon.events import PEER_TOOL, Kind

    if event.stream != MAIN_STREAM:
        return None
    if event.kind == Kind.PROMPT:
        text = event.text or ""
        return None if text.lstrip().startswith(_NOT_PROMPTS) else (Trigger.PROMPT, text, [])
    if event.kind == Kind.META and event.tool == PEER_TOOL:
        sender = sender_of(event)
        return Trigger.PEER, event.text or "", [sender] if sender else []
    if event.kind != Kind.TOOL_CALL:
        return None
    args = event.tool_input or {}
    if event.tool == WEB_SEARCH:
        query = args.get("query")
        return (Trigger.SEARCH, query, []) if isinstance(query, str) else None
    if event.tool == WEB_FETCH:
        parts = [v for v in (args.get("url"), args.get("prompt")) if isinstance(v, str) and v.strip()]
        return (Trigger.SEARCH, "\n".join(parts), []) if parts else None
    command = args.get("command") if isinstance(args.get("command"), str) else args.get("cmd")
    if isinstance(command, str) and launches_run(command):
        return Trigger.COMMAND, command, []
    return None


# -- a peer's session ----------------------------------------------------------


def claude_sessions_dir(env: dict) -> Path:
    """Where Claude Code keeps a record of each running session (`<pid>.json`:
    its `sessionId`, its `messagingSocketPath`), for a session with `env`."""
    base = env.get("CLAUDE_CONFIG_DIR") or os.path.join(env.get("HOME") or str(Path.home()), ".claude")
    return Path(base) / "sessions"


class Senders:
    """A peer message's sender to the session id that sent it. Another Claude
    Code session's message names its socket (`uds:<path>`), never its session:
    the session is the record whose `messagingSocketPath` is that path, else the
    record of the socket's pid (`<pid>.sock` -> `<pid>.json`, a build that
    records no path). A sender that is a session id already is one; a helper
    agent (its id, a Codex agent path) is none. Remembered per address."""

    def __init__(self, sessions_dir: Callable[[dict], Path] = claude_sessions_dir,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self._dir_of = sessions_dir
        self.clock = clock
        #: address -> (session id or None, until when it holds)
        self._known: OrderedDict = OrderedDict()

    def resolve(self, sender: str, env: dict) -> str | None:
        if _SESSION_ID.fullmatch(sender):
            return sender
        if not sender.startswith("uds:"):
            return None
        address = sender[len("uds:"):]
        now = self.clock()
        hit = self._known.get(address)
        if hit is not None and now < hit[1]:
            return hit[0]
        try:
            sid = self._look(self._dir_of(env), address)
        except Exception:  # noqa: BLE001 -- unknown: nothing excluded
            sid = None
        self._known[address] = (sid, now + (SENDER_KEEP_S if sid else SENDER_MISS_S))
        self._known.move_to_end(address)
        while len(self._known) > MAX_SENDERS:
            self._known.popitem(last=False)
        return sid

    @staticmethod
    def _look(folder: Path, address: str) -> str | None:
        from .mailwatch import read_json

        try:
            names = sorted(os.listdir(folder))[:MAX_SESSION_FILES]
        except OSError:
            return None
        for name in names:
            if not name.endswith(".json"):
                continue
            data = read_json(str(folder / name), MAX_SESSION_FILE_BYTES)
            if isinstance(data, dict) and data.get("messagingSocketPath") == address:
                sid = data.get("sessionId")
                return sid if isinstance(sid, str) and _SESSION_ID.fullmatch(sid) else None
        pid = _SOCKET_PID.fullmatch(os.path.basename(address))
        if pid is None:
            return None
        data = read_json(str(folder / f"{pid.group(1)}.json"), MAX_SESSION_FILE_BYTES)
        if not isinstance(data, dict):
            return None
        recorded = data.get("messagingSocketPath")
        if isinstance(recorded, str) and recorded and recorded != address:
            return None  # that pid's session listens elsewhere: not this sender
        sid = data.get("sessionId")
        return sid if isinstance(sid, str) and _SESSION_ID.fullmatch(sid) else None


# -- the session's ML state (R1) ----------------------------------------------------


def ml_state(state: str, sid: str) -> dict | None:
    """`{signal, p_ml}` from the session's daemon worker's store (the ML gate's
    facts), read only; None when there is no store, the gate never answered, or
    the store cannot be read now (locked, missing, another format)."""
    path = Path(state) / "daemon" / f"{_safe(sid)}.sqlite"
    if not path.is_file():
        return None
    import sqlite3

    from probe.daemon.gate import FACT_ANSWERS, FACT_SIGNAL

    try:
        conn = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True, timeout=0.2)
    except (OSError, sqlite3.Error):
        return None
    try:
        rows = conn.execute("SELECT key, value FROM facts WHERE key IN (?, ?)", (FACT_SIGNAL, FACT_ANSWERS)).fetchall()
        facts = {key: json.loads(value) for key, value in rows}
    except (sqlite3.Error, ValueError, TypeError):
        return None
    finally:
        conn.close()
    signal = facts.get(FACT_SIGNAL)
    answers = facts.get(FACT_ANSWERS) if isinstance(facts.get(FACT_ANSWERS), list) else []
    p_ml = next((float(p) for p in reversed(answers)
                 if isinstance(p, (int, float)) and not isinstance(p, bool)), None)
    if signal is None and p_ml is None:
        return None
    return {"signal": signal is not None, "p_ml": p_ml}


# -- the request ------------------------------------------------------------------


def scrubbed(text: str) -> str:
    """`text` as it may leave this machine: every credential the capture's one
    detector finds replaced (`probe.tap_core.secrets`, as the daemon's store and
    the tap's journal do before transcript text goes out), then cut to
    MAX_TEXT_CHARS."""
    from probe.tap_core import secrets as detector  # not the stdlib `secrets` this module uses

    clean, _rules = detector.redact(text)
    return clean[:MAX_TEXT_CHARS]


def credentials(env: dict) -> Endpoint | None:
    """The API and the read key of the CLI config the session's own processes
    read (its PROBE_CONFIG_PATH / XDG_CONFIG_HOME / HOME), its current context's
    address only (`caller.known_endpoint`: a key goes nowhere else). None when
    the session's environment overrides the endpoint or a key (_ENV_OVERRIDES)."""
    from . import caller

    if any(env.get(name) for name in _ENV_OVERRIDES):  # the session's own (its recorder's `env`)
        return None
    try:
        return endpoint(str(caller._config_path(env)), KEYS, environ=env)
    except Exception:  # noqa: BLE001
        return None


class HintFetcher(Fetcher):
    """POST /v1/hints over a kept connection per endpoint (`alertpoll.Fetcher`'s)."""

    timeout = TIMEOUT_S

    def __call__(self, ep: Endpoint, body: dict) -> tuple[int | None, object]:
        """`(HTTP status, the JSON answer)`, or `(None, None)` with no answer in time."""
        prefix = urlsplit(ep.base_url).path.rstrip("/")
        headers = {
            "Authorization": f"Bearer {ep.key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"probe-service/{self.version}",
            **self._client_headers(),
            **self._limit_headers(ep),
        }
        payload = json.dumps(body).encode("utf-8")
        deadline = time.monotonic() + TIMEOUT_S
        cutoff = threading.Timer(TIMEOUT_S, self.abort, args=(ep.base_url,))
        cutoff.daemon = True
        cutoff.start()
        try:
            return self._post(ep, f"{prefix}{ROUTE}", payload, headers, deadline)
        finally:
            cutoff.cancel()

    def _post(self, ep: Endpoint, path: str, payload: bytes, headers: dict, deadline: float):
        import http.client

        for attempt in (1, 2):
            try:
                conn = self._connection(ep.base_url)
                conn.request("POST", path, body=payload, headers=headers)
                resp = conn.getresponse()
                body = self._read(resp, deadline)
                if body is None or not resp.isclosed() or resp.will_close:
                    self.drop(ep.base_url)
                if body is None:
                    return None, None
                break
            except (http.client.RemoteDisconnected, BrokenPipeError, ConnectionResetError):
                # A kept connection the server closed meanwhile: once more, fresh
                # (the route only reads, so asking twice is safe). Never past the
                # deadline: the cutoff's own shutdown lands here too, and a second
                # try then would ask a slow server twice and wait on it again.
                self.drop(ep.base_url)
                if attempt == 2 or time.monotonic() >= deadline:
                    return None, None
            except (OSError, ValueError, http.client.HTTPException):
                self.drop(ep.base_url)
                return None, None
        try:
            data = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, ValueError, RecursionError):
            data = None
        return resp.status, data


# -- delivery ---------------------------------------------------------------------


def post_message(sid: str, state: str, message: dict) -> bool:
    """The hint in the session's mailbox: `mailbox.post`'s own step
    (`MailHost.post`: `mailbox.publish_here` under the session's state folder),
    in this process."""
    from .mailhost import MailHost

    answer = MailHost.post({"sid": sid, "state": state, "deadline_mono": time.monotonic() + TIMEOUT_S,
                            "message": message, "question": None})
    return bool(answer.get("posted"))


def withdraw_hints(sid: str, state: str) -> list[str]:
    """Every hint still waiting in the session's mailbox, taken out: the ids.
    Only hints: the mailbox's own `withdraw_unasked` is the reader's, and never
    takes one."""
    from probe.daemon import mailbox

    gone: list[str] = []
    with mailbox.rooted(state):
        for path, msg in mailbox.waiting(sid):
            if msg.origin == mailbox.ORIGIN_HINT and msg.kind == mailbox.Kind.MESSAGE:
                try:
                    path.unlink()
                except FileNotFoundError:
                    continue  # a hook delivered it first
                gone.append(msg.id)
    return gone


def waiting_hints(sid: str, state: str) -> set[str]:
    """The ids of the hints waiting in the session's mailbox now (unexpired)."""
    from probe.daemon import mailbox

    with mailbox.rooted(state):
        return {msg.id for _path, msg in mailbox.waiting(sid)
                if msg.origin == mailbox.ORIGIN_HINT and msg.kind == mailbox.Kind.MESSAGE}


def delivered_ids(sid: str, state: str) -> set[str]:
    """The message ids delivered to the session: its claim log's (the tail) and
    the files in its `claimed/` folder (a claim whose log line was lost)."""
    from probe.daemon import mailbox

    ids: set[str] = set()
    with mailbox.rooted(state):
        path = mailbox.claim_log_path(sid)
        ids |= mailbox.claimed_ids(sid)
    try:
        with path.open("rb") as handle:
            size = os.fstat(handle.fileno()).st_size
            handle.seek(max(0, size - CLAIM_LOG_TAIL_BYTES))
            tail = handle.read().decode("utf-8", "replace")
    except OSError:
        return ids
    for line in tail.splitlines():
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        if isinstance(entry, dict) and isinstance(entry.get("id"), str):
            ids.add(entry["id"])
    return ids


def record_keys(records: object) -> frozenset[str]:
    """Each shown record as `<doc id> <date>`: the same record changed is new."""
    keys = set()
    for record in records if isinstance(records, list) else []:
        if isinstance(record, dict) and isinstance(record.get("doc_id"), str) and record["doc_id"]:
            keys.add(f"{record['doc_id']} {record.get('date') or ''}")
    return frozenset(keys)


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


@dataclass
class _Tail:
    adapter: object
    filter: object
    path: Path | None = None
    inode: int | None = None
    offset: int | None = None
    skipping: bool = False
    first: bool = True
    seen_at: float = 0.0
    resolve_at: float = 0.0


@dataclass
class _State:
    """One session's memory, this service's life."""

    recent: OrderedDict = field(default_factory=OrderedDict)
    last_sent: float = float("-inf")
    #: Researcher prompts and ends of the agent's turn seen (`Lookup.epoch`).
    epoch: int = 0
    #: Every hint's records the ledger knows of (this run's and the last week's,
    #: a previous service's included): message id -> record keys.
    ledger: dict | None = None
    lock: threading.Lock = field(default_factory=threading.Lock)
    no_key_said: bool = False


class _Facts:
    """The daemon filter's fact store, in memory (the lane keeps no store)."""

    def __init__(self) -> None:
        self.facts: dict = {}

    def fact(self, key: str, default=None):
        return self.facts.get(key, default)

    def set_fact(self, key: str, value) -> None:
        self.facts[key] = value


class HintLane:
    """The service's one hint lane (see the module docstring).

    `sessions()` lists the sessions to read (`followed`), asked on the lane's
    tail thread. Seams for tests: `transport(endpoint, body) -> (status, data)`,
    `endpoint_of(env)`, `post(sid, state, message) -> bool`, `withdraw(sid,
    state) -> [ids]`, `delivered(sid, state) -> {ids}`, `waiting(sid, state) ->
    {ids}`, `ml(state, sid)`,
    `senders` (where Claude Code's session records are), the clocks. `posted(sid)` is told of each hint posted (the server says
    `mailbox.changed`)."""

    def __init__(
        self,
        *,
        sessions: Callable[[], list],
        log: Callable[[str], None],
        version: str = "0.0.0",
        environ: dict | None = None,
        transport: Callable | None = None,
        endpoint_of: Callable[[dict], Endpoint | None] = credentials,
        post: Callable[[str, str, dict], bool] = post_message,
        withdraw: Callable[[str, str], list] = withdraw_hints,
        delivered: Callable[[str, str], set] = delivered_ids,
        waiting: Callable[[str, str], set] = waiting_hints,
        ml: Callable[[str, str], dict | None] = ml_state,
        posted: Callable[[str], None] = lambda sid: None,
        senders: Senders | None = None,
        ledger_dir: Path | None = None,
        clock: Callable[[], float] = time.monotonic,
        wall: Callable[[], float] = time.time,
        poll_s: float | None = None,
    ) -> None:
        self._sessions = sessions
        self._log = log
        self.version = version
        self.enabled = not disabled(os.environ if environ is None else environ)
        self.transport = transport if transport is not None else HintFetcher(version)
        self.endpoint_of = endpoint_of
        self._post = post
        self._withdraw = withdraw
        self._delivered = delivered
        self._waiting = waiting
        self._ml = ml
        self._posted = posted
        self.senders = senders if senders is not None else Senders()
        self._ledger_dir = ledger_dir
        self.clock = clock
        self.wall = wall
        self.poll_s = _poll_interval() if poll_s is None else poll_s
        self._tails: dict[str, _Tail] = {}
        self._states: dict[str, _State] = {}
        self._pending: OrderedDict[str, Lookup] = OrderedDict()
        self._cv = threading.Condition()
        self._tokens = BUCKET_BURST
        self._filled_at = clock()
        #: Requests wait until then (`clock`) per scope (`_scopes`): a refused key,
        #: a server without the route, a 429 for a key on a server.
        self._holds: dict[tuple, float] = {}
        #: `mode: off`: (base URL, key) -> until when it is not asked again.
        self._off: dict[tuple, float] = {}
        self._wake = threading.Event()
        self._threads: list[threading.Thread] = []
        self._closed = False
        #: When the ledgers were last swept (`clock`), or None before the first.
        self._swept_at: float | None = None
        #: What happened, counted (tests and the log): triggers, skips, posts.
        self.stats: Counter = Counter()
        #: When each served session's hint marker was last touched (`clock`).
        self._beats: dict[str, float] = {}

    # -- lifecycle --------------------------------------------------------------

    def changed(self) -> None:
        """A recording started or changed: look now (the threads start on the first)."""
        if not self.enabled or self._closed:
            return
        try:
            if not self._threads:
                for name, target in (("hints-tail", self._tail_loop), ("hints-lookup", self._lookup_loop)):
                    thread = threading.Thread(target=target, name=name, daemon=True)
                    self._threads.append(thread)
                    thread.start()
            self._wake.set()
        except Exception as exc:  # noqa: BLE001 -- no hints, nothing else touched
            self._log(f"hints: could not start: {exc!r}")

    def close(self) -> None:
        self._closed = True
        self._wake.set()
        with self._cv:
            self._cv.notify_all()
        abort = getattr(self.transport, "abort", None)
        if abort is not None:
            with contextlib.suppress(Exception):
                abort()

    def _state(self, sid: str) -> _State:
        state = self._states.get(sid)
        if state is None:
            state = self._states.setdefault(sid, _State())  # both threads ask: one wins
        return state

    # -- the tail ---------------------------------------------------------------

    def _tail_loop(self) -> None:
        while not self._closed:
            # Cleared before the look: a `changed` during it makes the next one at once.
            self._wake.clear()
            try:
                active = self.read_once()
            except Exception as exc:  # noqa: BLE001 -- the thread outlives a bug
                self._log(f"hints: a read failed: {exc!r}")
                active = True
            self._wake.wait(self.poll_s if active else None)

    def read_once(self) -> bool:
        """One look at every followed session's transcript. False when none is
        followed (the tail then waits for `changed` with no timer)."""
        try:
            sessions = list(self._sessions())
        except Exception as exc:  # noqa: BLE001
            self._log(f"hints: the sessions could not be listed: {exc!r}")
            sessions = []
        seen = set()
        for session in sessions:
            seen.add(session.sid)
            try:
                self._read(session)
            except Exception as exc:  # noqa: BLE001 -- one transcript never stops another
                self._log(f"hints: session {session.sid}: a read failed: {exc!r}")
            try:
                self._beat(session)
            except Exception as exc:  # noqa: BLE001 -- a stale marker only wakes the reader
                self._log(f"hints: session {session.sid}: the hint marker failed: {exc!r}")
        # No longer read here (it ended, or its recorder let go of it). The
        # states too: a lookup in flight when its session went makes one anew.
        for sid in [s for s in {*self._tails, *self._states, *self._beats} if s not in seen]:
            self._beats.pop(sid, None)
            self._tails.pop(sid, None)
            with self._cv:
                self._pending.pop(sid, None)
                self._states.pop(sid, None)
        return bool(sessions)

    def _beat(self, session: Followed) -> None:
        """While this lane can hint `session` (followed here, a key its own config
        resolves, the server neither refusing the key nor lacking the route nor
        answering `mode: off`), its marker is touched, at most every
        HINTS_LIVE_BEAT_S: the session's daemon then leaves prompt time to hints
        (`model.hints_live`). Not touched, the marker goes stale and the reader
        wakes at prompts again."""
        now = self.clock()
        if now - self._beats.get(session.sid, float("-inf")) < HINTS_LIVE_BEAT_S:
            return
        self._beats[session.sid] = now  # looked at, touched or not: the next look in a beat
        ep = self.endpoint_of(session.env)
        if ep is None:
            return
        key, server, _pair = _scopes(ep)
        with self._cv:
            if (max(self._holds.get(key, float("-inf")), self._holds.get(server, float("-inf"))) > now
                    or self._off.get((ep.base_url, ep.key), float("-inf")) > now):
                return  # a 429 (`pair`) passes: a busy server still hints
        from probe.daemon import mailbox

        with mailbox.rooted(session.state):
            path = mailbox.hints_live_path(session.sid)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()  # an existing one's mtime moves to now

    def _tail(self, session: Followed) -> _Tail | None:
        tail = self._tails.get(session.sid)
        if tail is not None:
            return tail
        from probe.daemon import adapters
        from probe.daemon.exclusions import Filter

        try:
            adapter = adapters.for_source(session.harness)
        except LookupError:
            return None
        tail = _Tail(adapter=adapter, filter=Filter(_Facts(), session.sid, session.cwd or None),
                     seen_at=self.wall())
        self._tails[session.sid] = tail
        return tail

    def _path(self, session: Followed, tail: _Tail) -> Path | None:
        if tail.path is not None:
            return tail.path
        if session.transcript:
            tail.path = Path(session.transcript)
        elif session.transcript_dir and self.clock() >= tail.resolve_at:
            # Codex: its rollout under a dated folder (`tap.main._resolve_codex_transcript`).
            tail.resolve_at = self.clock() + RESOLVE_EVERY_S
            folder = Path(session.transcript_dir)
            found = sorted(folder.rglob(f"*{session.sid}.jsonl")) if folder.is_dir() else []
            tail.path = found[0] if found else None
        if tail.path is not None:
            with contextlib.suppress(Exception):
                tail.adapter.session_files(tail.path)
        return tail.path

    def _read(self, session: Followed) -> None:
        tail = self._tail(session)
        if tail is None:
            return
        path = self._path(session, tail)
        if path is None:
            return
        try:
            # Never a blocking open (a FIFO, a device): one path a caller named
            # must not stop every session's tail (`mailwatch.read_regular`).
            fd = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOCTTY", 0))
        except OSError:
            return
        handle = os.fdopen(fd, "rb")
        with handle:
            info = os.fstat(handle.fileno())
            if not stat.S_ISREG(info.st_mode):
                return
            if tail.offset is None:
                tail.inode = info.st_ino
                tail.offset = max(0, info.st_size - INITIAL_BACK_BYTES)
                tail.skipping = tail.offset > 0  # mid-line: on from the next line
            elif info.st_ino != tail.inode or info.st_size < tail.offset:
                # Rewritten or replaced under the offset: on from its end.
                tail.inode, tail.offset, tail.skipping = info.st_ino, info.st_size, False
                return
            if info.st_size <= tail.offset:
                tail.first = False
                return
            handle.seek(tail.offset)
            buf = handle.read(min(MAX_READ_BYTES, info.st_size - tail.offset))
        start = tail.offset
        if tail.skipping:
            nl = buf.find(b"\n")
            if nl < 0:
                tail.offset += len(buf)
                return
            tail.skipping = False
            start += nl + 1
            buf = buf[nl + 1:]
        last = buf.rfind(b"\n")
        if last < 0:
            if len(buf) >= MAX_READ_BYTES:
                tail.offset, tail.skipping = start + len(buf), True  # a line over MAX_READ_BYTES: skipped
            else:
                tail.offset = start
            return
        tail.offset = start + last + 1
        fresh_after = tail.seen_at - FRESH_S if tail.first else None
        tail.first = False
        pos = 0
        while pos <= last:
            nl = buf.find(b"\n", pos)
            line, end = buf[pos:nl], start + nl + 1
            pos = nl + 1
            self._line(session, tail, line, end, fresh_after)

    def _line(self, session: Followed, tail: _Tail, line: bytes, end: int, fresh_after: float | None) -> None:
        if not line.strip():
            return
        try:
            obj = json.loads(line)
        except (ValueError, RecursionError):
            return  # a line nested too deep for the parser too: the next one is read
        if not isinstance(obj, dict):
            return
        stamp = _epoch(tail.adapter.line_ts(obj))
        if fresh_after is not None and (stamp is None or stamp < fresh_after):
            return  # the history of a session first seen
        try:
            events = list(tail.adapter.parse_line(obj, stream=MAIN_STREAM, offset=end))
        except Exception:  # noqa: BLE001 -- a line the adapter cannot read is skipped, as the worker does
            return
        for index, event in enumerate(events):
            event.index = index
        # A first look's prompts and turn ends are no newer than a hint the last
        # service posted for them: they withdraw nothing.
        newer = fresh_after is None
        from probe.daemon.events import Kind

        if any(e.stream == MAIN_STREAM and e.kind == Kind.TURN_END for e in events):
            self.turn_ended(session, newer=newer)
        found = [(event, hit) for event in events if (hit := trigger_of(event)) is not None]
        if not found:
            return
        # `.probe.config`: the worker's own filter, over the events that would ask.
        line_cwd = obj.get("cwd") if isinstance(obj.get("cwd"), str) else None
        kept = {id(e) for e in tail.filter.keep([e for e, _ in found], stream=MAIN_STREAM, line_cwd=line_cwd)}
        for event, (trigger, text, senders) in found:
            if id(event) not in kept:
                self.stats["excluded"] += 1
                # Never asked about, but still a newer prompt: a waiting hint is stale.
                text = ""
            self.trigger(session, trigger, text, senders, happened=stamp, newer=newer)

    # -- triggers -----------------------------------------------------------------

    def trigger(self, session: Followed, trigger: str, text: str, senders: list | None = None,
                happened: float | None = None, newer: bool = True) -> bool:
        """A lookup asked for: queued (the latest per session, `_ASKED_FIRST` kept). A researcher
        prompt first withdraws the session's hint still waiting (R5; `newer`
        False: not one read on a first look). False when nothing was queued
        (an empty text queues nothing: a prompt that may not be looked up)."""
        text = (text or "").strip()[:MAX_TEXT_CHARS + SCAN_MARGIN_CHARS]  # `scrubbed` cuts it when sent
        state = self._state(session.sid)
        if trigger == Trigger.PROMPT:
            with state.lock:
                state.epoch += 1
                if newer:
                    self._take_back(session, state, "a newer prompt")
        if not text:
            return False
        try:
            ep = self.endpoint_of(session.env)
        except Exception:  # noqa: BLE001 -- unknown: not asked
            ep = None
        if ep is None:
            self.stats["no_key"] += 1
            if not state.no_key_said:
                state.no_key_said = True
                self._log(f"hints: session {session.sid}: no Probe key in its CLI config (or its environment "
                          "names another endpoint or key); no hints")
            return False
        now = self.clock()
        with self._cv:
            if now < self._off.get((ep.base_url, ep.key), float("-inf")):
                self.stats["quiet"] += 1
                return False
            if _repeat_key(trigger, text) in state.recent:
                self.stats["repeat_text"] += 1
                return False
            waiting = self._pending.get(session.sid)
            if waiting is not None and trigger not in _ASKED_FIRST and waiting.trigger in _ASKED_FIRST:
                # A prompt waiting out the gap is kept over the agent's search or
                # command: the researcher's ask is the better question.
                self.stats["outranked"] += 1
                return False
            self._pending.pop(session.sid, None)
            self._pending[session.sid] = Lookup(
                sid=session.sid, session=session, trigger=trigger, text=text, senders=list(senders or []),
                queued=now,
                happened=happened if happened is not None else self.wall(), epoch=state.epoch, ep=ep)
            while len(self._pending) > MAX_PENDING:
                self._pending.popitem(last=False)
                self.stats["dropped"] += 1
            self.stats[f"trigger_{trigger}"] += 1
            self._cv.notify()
        return True

    def turn_ended(self, session: Followed, newer: bool = True) -> None:
        """The main agent's turn is over (TURN_END): a hint still waiting was for
        it, and the next prompt's hook would hand it over stale (R5), so it goes
        (`newer` False: not one read on a first look); a lookup in flight for it
        is stale, and one still waiting out the session's gap is not sent."""
        state = self._state(session.sid)
        with state.lock:
            state.epoch += 1
            if newer:
                self._take_back(session, state, "the turn ended")
        with self._cv:
            if self._pending.pop(session.sid, None) is not None:
                self.stats["ended"] += 1

    def _take_back(self, session: Followed, state: _State, why: str) -> None:
        """A newer researcher prompt, or the end of the turn: the session's hints
        still waiting go (R5). Under the session's lock, so a lookup cannot post
        behind it."""
        try:
            gone = self._withdraw(session.sid, session.state)
        except Exception as exc:  # noqa: BLE001
            self._log(f"hints: session {session.sid}: could not withdraw a hint: {exc!r}")
            return
        if gone:
            self.stats["withdrawn"] += len(gone)
            self._log(f"hints: session {session.sid}: {len(gone)} hint(s) withdrawn ({why})")
            with contextlib.suppress(Exception):
                self._posted(session.sid)

    # -- the lookups --------------------------------------------------------------

    def _lookup_loop(self) -> None:
        while True:
            with self._cv:
                job = None
                while not self._closed:
                    job, wait = self.take_due()
                    if job is not None:
                        break
                    self._cv.wait(wait)
                if self._closed:
                    return
            try:
                self.lookup(job)
            except Exception as exc:  # noqa: BLE001 -- the thread outlives a bug; no hint
                self._log(f"hints: session {job.sid}: the lookup failed: {exc!r}")

    def _refill(self, now: float) -> None:
        rate = BUCKET_PER_MIN / 60.0
        self._tokens = min(BUCKET_BURST, self._tokens + max(0.0, now - self._filled_at) * rate)
        self._filled_at = now

    def take_due(self) -> tuple[Lookup | None, float | None]:
        """The next lookup that may go now, or `(None, how long to wait)`
        (None: until something is queued). Call with the lane's condition held."""
        now = self.clock()
        for table in (self._holds, self._off):
            for scope in [k for k, until in table.items() if until <= now]:
                del table[scope]  # past: forgotten, so neither table grows
        if not self._pending:
            return None, None
        best, best_due = None, None
        for sid, job in list(self._pending.items()):
            state = self._state(sid)
            if job.ep is not None and (job.ep.base_url, job.ep.key) in self._off:
                del self._pending[sid]  # its team's setting is off: not asked
                continue
            held = max((self._holds.get(scope, float("-inf")) for scope in _scopes(job.ep)), default=float("-inf"))
            due = max(job.queued, state.last_sent + SESSION_GAP_S, held)
            if best_due is None or due < best_due:
                best, best_due = job, due
        if best is None:
            return None, None
        if best_due > now:
            return None, best_due - now
        self._refill(now)
        if self._tokens < 1.0:
            return None, (1.0 - self._tokens) / (BUCKET_PER_MIN / 60.0)
        self._tokens -= 1.0
        del self._pending[best.sid]
        self._state(best.sid).last_sent = now
        return best, None

    def run_due(self) -> int:
        """Every lookup due now, on this thread (tests). How many ran."""
        ran = 0
        while True:
            with self._cv:
                job, _wait = self.take_due()
            if job is None:
                return ran
            self.lookup(job)
            ran += 1

    def lookup(self, job: Lookup) -> None:
        """Ask the server about one trigger; post the hint when it fires. Fails
        open: any error is one log line and no hint."""
        session, state = job.session, self._state(job.sid)
        ep = job.ep
        if ep is None:
            return  # `trigger` queues none without one
        try:
            from probe.daemon import adapters

            harness = adapters.for_source(session.harness).name
        except Exception:  # noqa: BLE001
            harness = session.harness
        try:
            ml = self._ml(session.state, job.sid) if session.mode == Mode.DAEMON else None
        except Exception:  # noqa: BLE001 -- unknown: the server's record-type rule
            ml = None
        try:
            text = scrubbed(job.text)
        except Exception as exc:  # noqa: BLE001 -- unscanned text never leaves: no request
            self.stats["unscanned"] += 1
            self._log(f"hints: session {job.sid}: the secret scan failed ({type(exc).__name__}); not asked")
            return
        exclude: list = []
        for sender in job.senders:
            sid = self.senders.resolve(sender, session.env)
            if sid and sid != job.sid and sid not in exclude:
                exclude.append(sid)
        try:
            with state.lock:
                shown = self._shown(session, state)
        except Exception:  # noqa: BLE001 -- unknown: none named (the all-repeated rule still holds)
            shown = []
        body = {"text": text, "trigger": job.trigger, "session_id": job.sid,
                "exclude_session_ids": exclude, "exclude_doc_ids": exclude_doc_ids(shown), "ml": ml,
                "client": {"harness": harness, "mode": session.mode, "cli": self.version}}
        started = self.clock()
        try:
            status, data = self.transport(ep, body)
        except Exception as exc:  # noqa: BLE001 -- fail open
            status, data = None, None
            self._log(f"hints: session {job.sid}: the request failed: {type(exc).__name__}")
        took = (self.clock() - started) * 1000.0
        line = f"hints: session {job.sid} {job.trigger}"
        if status is None:
            self.stats["unanswered"] += 1
            self._log(f"{line}: no answer in {took:.0f} ms; no hint")
            return
        if status in (401, 403, 404, 429) or (status == 200 and isinstance(data, dict)
                                               and data.get("reason") == "rate_limited"):
            wait = {401: REFUSED_S, 403: REFUSED_S, 404: MISSING_S}.get(status, LIMITED_S)
            scope = _scopes(ep)[{401: 0, 403: 0, 404: 1}.get(status, 2)]
            with self._cv:
                self._holds[scope] = max(self._holds.get(scope, float("-inf")), self.clock() + wait)
            self.stats[f"held_{status}"] += 1
            self._log(f"{line}: answered {status}; {_SCOPE_NAMES[scope[0]]} is not asked for {wait:.0f} s")
            return
        if status != 200 or not isinstance(data, dict):
            self.stats["refused"] += 1
            self._log(f"{line}: answered {status} in {took:.0f} ms; no hint")
            return
        with self._cv:
            state.recent[_repeat_key(job.trigger, job.text)] = None
            while len(state.recent) > REPEATS:
                state.recent.popitem(last=False)
            mode = data.get("mode")
            if mode == "off":
                # The team's setting, for every session of this key on this server.
                self._off[(ep.base_url, ep.key)] = self.clock() + OFF_RECHECK_S
        fire = data.get("fire") is True
        hint = data.get("hint")
        outcome = "not shown"
        if fire and mode == "on" and isinstance(hint, str) and hint.strip():
            if len(hint) > MAX_HINT_CHARS:
                self.stats["too_long"] += 1
                outcome = Skip.TOO_LONG
            else:
                # Posted exactly as Probe rendered it: the mailbox shows a hint as-is
                # only when it starts with `[Probe] ` (its framing), so nothing is added.
                posted, why = self._deliver(job, state, hint, data.get("records"))
                outcome = f"posted {(self.wall() - job.happened) * 1000:.0f} ms after the trigger" if posted else why
        self.stats[f"mode_{mode}"] += 1
        self._log(f"{line}: mode={mode} fire={fire} reason={data.get('reason')} "
                  f"top={_number(data.get('top_score'))} in {took:.0f} ms; {outcome}")

    def _deliver(self, job: Lookup, state: _State, hint: str, records: object) -> tuple[bool, str]:
        session = job.session
        keys = record_keys(records)
        with state.lock:
            if state.epoch != job.epoch:
                self.stats["stale"] += 1
                return False, Skip.STALE
            if keys and keys <= self._seen(session, state):
                self.stats["repeat"] += 1
                return False, Skip.REPEAT
            from probe.daemon import mailbox

            message = {"id": "h" + secrets.token_hex(6), "session": job.sid, "kind": mailbox.Kind.MESSAGE.value,
                       "text": hint, "made_at": self.wall(), "origin": mailbox.ORIGIN_HINT}
            if not self._post(job.sid, session.state, message):
                self.stats["not_posted"] += 1
                return False, Skip.NOT_POSTED
            # Its slot holds one hint: an earlier one still waiting was replaced
            # (`mailbox.publish_here`), so it is no longer in the mailbox's files,
            # which are all `_seen` reads.
            if state.ledger is not None:
                state.ledger[message["id"]] = keys
            self._remember(job.sid, message["id"], keys)
        self.stats["posted"] += 1
        with contextlib.suppress(Exception):
            self._posted(job.sid)
        return True, "posted"

    def _shown(self, session: Followed, state: _State) -> list:
        """Each of the ledger's hints, newest first, as its record keys, that the
        session was delivered (the claim log, `claimed/`) or that waits in its
        mailbox now (R3), read from the mailbox's own files: a hint replaced in
        its slot, withdrawn, expired or removed by any other deliverer's rules
        never counts as shown. Under the session's lock."""
        if state.ledger is None:
            state.ledger = self._load_ledger(session.sid)
        ids: set = set()
        for read in (self._delivered, self._waiting):
            try:
                ids |= read(session.sid, session.state)
            except Exception:  # noqa: BLE001 -- unknown: none of these counts
                pass
        return [keys for mid, keys in reversed(state.ledger.items()) if mid in ids]

    def _seen(self, session: Followed, state: _State) -> set:
        """The records the session was shown or has waiting (`_shown`)."""
        return set().union(*self._shown(session, state))

    # -- the ledger: which records each hint carried ------------------------------

    def _ledger_path(self, sid: str) -> Path:
        if self._ledger_dir is None:
            from . import paths

            self._ledger_dir = paths.service_dir() / LEDGER_DIR
        return self._ledger_dir / f"{_safe(sid)}.jsonl"

    def _load_ledger(self, sid: str) -> dict:
        path = self._ledger_path(sid)
        self._sweep(path.parent)
        out: dict = {}
        try:
            with path.open("rb") as handle:
                size = os.fstat(handle.fileno()).st_size
                handle.seek(max(0, size - LEDGER_TAIL_BYTES))
                text = handle.read().decode("utf-8", "replace")
        except OSError:
            return out
        for line in text.splitlines():
            try:
                entry = json.loads(line)
            except ValueError:
                continue
            if isinstance(entry, dict) and isinstance(entry.get("id"), str) and isinstance(entry.get("keys"), list):
                out[entry["id"]] = frozenset(k for k in entry["keys"] if isinstance(k, str))
        return out

    def _remember(self, sid: str, message_id: str, keys: frozenset) -> None:
        path = self._ledger_path(sid)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600), "a", encoding="utf-8") as out:
                out.write(json.dumps({"id": message_id, "keys": sorted(keys), "at": self.wall()}) + "\n")
        except OSError as exc:
            self._log(f"hints: session {sid}: the ledger could not be written: {exc}")
        self._sweep(path.parent)

    def _sweep(self, folder: Path) -> None:
        """Ledgers past KEEP_LEDGER_S go (their hints' claim files are gone
        too): at most every SWEEP_EVERY_S, so a service that runs for weeks
        does not keep every ended session's ledger."""
        if self._swept_at is not None and self.clock() - self._swept_at < SWEEP_EVERY_S:
            return
        self._swept_at = self.clock()
        now = time.time()
        with contextlib.suppress(OSError):
            for path in folder.glob("*.jsonl"):
                with contextlib.suppress(OSError):
                    if now - path.stat().st_mtime > KEEP_LEDGER_S:
                        path.unlink()


def exclude_doc_ids(shown: list, limit: int = MAX_EXCLUDE_DOC_IDS) -> list[str]:
    """The request's `exclude_doc_ids`: the doc ids of the records in `shown`
    (each hint's record keys, `<doc id> <date>`, newest hint first), each once,
    at most `limit`. A server that honors it leaves them out before it renders
    (a hint that repeats some records); one that does not ignores it, and
    `HintLane._deliver` still skips a hint whose records were all shown."""
    out: list[str] = []
    for keys in shown:
        for key in sorted(keys):
            doc = key.rsplit(" ", 1)[0]
            if doc and doc not in out:
                out.append(doc)
                if len(out) >= limit:
                    return out
    return out


def _scopes(ep: Endpoint | None) -> tuple:
    """What a hold is kept for (as `alertpoll`): the key, wherever it is used (a
    401 / 403); the server, for every key (a 404); that key on that server (a 429)."""
    if ep is None:
        return ()
    return (("key", ep.key), ("server", ep.base_url), ("pair", ep.base_url, ep.key))


#: How the log names a hold's scope (never the key itself).
_SCOPE_NAMES = {"key": "this key", "server": "this server", "pair": "this key on this server"}


def _repeat_key(trigger: str, text: str) -> tuple[str, str]:
    return trigger, hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()


def _number(value: object) -> str:
    return f"{value:.3f}" if isinstance(value, (int, float)) and not isinstance(value, bool) else "-"


__all__ = ["Followed", "HintFetcher", "HintLane", "Lookup", "Senders", "Trigger", "followed", "launches_run",
           "ml_state", "sender_of", "trigger_of"]
