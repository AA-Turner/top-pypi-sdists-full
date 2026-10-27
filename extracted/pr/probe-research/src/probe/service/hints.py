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
                  same file: one look every POLL_S per session (an open and an
                  fstat), and only the new bytes read (the page cache has them: the recorder just read
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
                  `probe run start` (`command`); and (`window`, plan
                  hints-window-trigger W1) WINDOW_GAP_S after the last window
                  look, the researcher's prompt or the turn's first step (a
                  turn's end ends its window), at the agent's next step, when it
                  wrote at least one message since: every such message, newest
                  first, each looked up on its own (`segments`). Tool calls and
                  their output are never sent for a window. Nothing else
    the lookup    POST /v1/hints on one kept connection per lookup thread
                  (prompts and the rest on one, windows on their own), with the read-only key
                  of the session's CLI config (KEYS), TIMEOUT_S, failing open:
                  no answer is no hint. The text goes through the capture's
                  secret scan first (`scrubbed`), as all transcript text that
                  leaves the machine does
    limits        one request per session per SESSION_GAP_S, windows and the
                  rest each on their own clock: a window just sent never delays
                  the session's prompt (a newer trigger
                  replaces the one waiting, but a search or a command never a
                  prompt or a peer's message); a token bucket for the machine
                  (BUCKET_PER_MIN, BUCKET_BURST); holds as `alertpoll` keeps
                  them (`_scopes`): a 429 holds that key on that server
                  LIMITED_S, a 401 / 403 the key REFUSED_S, a 404 the server
                  MISSING_S; `mode: off` quiets that key on that server
                  OFF_RECHECK_S for every session; the last REPEATS texts of a
                  session are never sent again. A window lookup goes on its
                  own thread, so it never holds up a prompt's; it never takes
                  the machine's last tokens (WINDOW_TOKEN_RESERVE), waits
                  WINDOW_TIMEOUT_S, and
                  is held on its own (`_window_scopes`): a 404, or a 422 naming
                  `trigger`, holds window lookups on that server MISSING_S, no
                  answer LIMITED_S, a 429 that key's there LIMITED_S; prompts
                  and the rest still ask
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
    markers       `<sid>.live` (`mailbox.hints_live_path`) while the lane can
                  hint the session: its daemon's reader then leaves prompt time
                  to hints. `<sid>.window` (`mailbox.hints_window_path`) only
                  while window hints are proven working for it (`_window_works`):
                  its daemon's reader then stops its check-ins
    off           PROBE_HINTS=off in a session's environment (its recorder's
                  `env`: every PROBE_* variable the agent's shell had), or in
                  the service's own

One log line per lookup (trigger, mode, fire, reason, top score, latency,
how long after the trigger it was answered, delivered or why not), never the
text. Three daemon threads of its own (the tail, the lookups, the window
lookups), none waited for at exit; all idle without a timer while no session is
followed; everything they do is caught and logged.

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
from collections import Counter, OrderedDict, deque
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
#: Every followed transcript is looked at this often: one stat each, and only
#: new bytes read. A prompt waits half of it on average before its lookup goes
#: (1.0 s until plan hints-latency L3: ~0.5 s of a ~1.5 s hint).
POLL_S = 0.25
#: A served session's hint marker (`mailbox.hints_live_path`) is touched at most
#: this often; its daemon reads one older than `model.HINTS_LIVE_TTL_S` (120 s)
#: as no hint lane here, and its reader wakes at prompts again.
HINTS_LIVE_BEAT_S = 30.0
#: Test-only: a shorter POLL_S (nothing in production sets it).
POLL_ENV = "PROBE_SERVICE_HINTS_POLL_S"
#: One request, connect to last byte.
TIMEOUT_S = 5.0
#: A window request (plan hints-window-trigger W1/W3): the server spends up to
#: its 4 s engine budget and then at most five database statements (1.5 s
#: deadline each) before it answers.
WINDOW_TIMEOUT_S = 12.0
#: A window look comes due this long after the last window look or researcher
#: prompt (the lines' own stamps), at the agent's next step (a message or a
#: tool call), if it wrote a message since: the mailbox hands a long turn one
#: hint per 10 minutes (`mailbox.UNASKED_WINDOW_S`), so looking more often
#: only replaces a waiting one.
WINDOW_GAP_S = 600.0
#: The window's messages sent, at most (the newest); the server asks as many.
WINDOW_MAX_SEGMENTS = 32
#: One message, at most, as sent (the engine embeds 2,000 characters).
WINDOW_SEGMENT_CHARS = 2000
#: A window lookup takes a machine token only while at least this many are
#: left, so a prompt or a peer's message always finds one.
WINDOW_TOKEN_RESERVE = 2.0
#: This many window lookups in a row failing (no answer, any refusal,
#: `engine_error` or `rate_limited`), the session's or its key's, stop the
#: session's window marker until one works again.
WINDOW_FAILURES_STOP = 2
#: The session's transcript must have been read this recently for its window marker.
WINDOW_READ_FRESH_S = 60.0
#: A window clock older than this (the reader's check-in interval) means the
#: lane has not looked at the turn's work for that long (tool calls only, or a
#: window that could not go): its window marker stops and the check-in returns.
WINDOW_COVERS_S = 1800.0
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
#: The most record doc ids a request names as shown already (`exclude_doc_ids`):
#: a long turn of window hints passes 50. A server that answered a window
#: lookup accepts 200; any other may be one before them (#3402), which refuses
#: more than LEGACY_EXCLUDE_DOC_IDS with a 422.
MAX_EXCLUDE_DOC_IDS = 100
LEGACY_EXCLUDE_DOC_IDS = 50
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
#: A shell line longer than this is never read as a launch: `shell_part` is
#: quadratic in heredoc markers (32 kB of them take seconds), and the tail
#: thread reads every session.
MAX_COMMAND_CHARS = MAX_TEXT_CHARS
#: A heredoc's body (kept: the rest of its first line, which is still shell), and
#: a quoted string: text a command only writes (`shell_part`).
_HEREDOC = re.compile(r"<<-?[ \t]*(['\"]?)(\w+)\1([^\n]*)\n(?:.*?\n)??[ \t]*\2[ \t]*(?:\n|$)", re.DOTALL)
_QUOTED = re.compile(r"'[^']*'|\"(?:[^\"\\]|\\.)*\"")
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
    WINDOW = "window"


#: The triggers a waiting lookup is never replaced by a search or a command for
#: (the server's `prompt` class: the one shown before the others are calibrated).
_ASKED_FIRST = frozenset({Trigger.PROMPT, Trigger.PEER})


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


class DeliveryState:
    """Whether the hints posted to a session reach its agent (`delivery_receipt`)."""

    OK = "ok"  # a deliverer is there (its heartbeat), or a hint was shown lately
    UNPROVEN = "unproven"  # neither yet: the session's reader keeps its prompt turns and check-ins
    UNDELIVERABLE = "undeliverable"  # hints posted here keep missing chances to be shown


class Deliverer:
    """Who handed a session its messages (`delivery_receipt`'s `deliverer`)."""

    HOOK = "hook"  # Claude Code's / Codex's reads hook
    PI = "pi"  # harness-literal-ok: pi's extension, as a receipt names its deliverer
    ASK = "ask"  # a `probe ask --wait`
    OTHER = "other"


#: A deliverer's own name for itself (`mailbox.touch_alive`, the claim log's `by`) -> who.
_DELIVERER_OF = {"UserPromptSubmit": Deliverer.HOOK, "PostToolUse": Deliverer.HOOK, "Stop": Deliverer.HOOK,
                 "pi poller": Deliverer.PI, "before_agent_start": Deliverer.PI,
                 "probe ask --wait": Deliverer.ASK}
#: How long a deliverer's heartbeat proves it is there: pi's poller touches it
#: every ALIVE_EVERY_S while it runs; a hook only when it runs Python (at a
#: prompt of a session the reader serves, or when a message waits), so its
#: heartbeat says "a current hook serves this session", and a hook that stops
#: delivering shows as missed hints instead (`MISSED_UNDELIVERABLE`).
DELIVERER_FRESH_S = {Deliverer.PI: 600.0}
DELIVERER_FRESH_DEFAULT_S = 12 * 3600.0
#: A hint shown (or, from a deliverer that writes no `shown`, claimed) this
#: recently proves delivery too.
DELIVERED_RECENTLY_S = 1800.0
#: A waiting hint MISSED its chance when at least this many agent tool calls, in
#: turns whose one hint slot was still free, came MISSED_AFTER_S or more after
#: it was posted and while it still waited: a hook delivers after the next tool
#: call, pi's poller within 2 s while the agent runs.
MISSED_TOOL_CALLS = 2
MISSED_AFTER_S = 3.0
#: Hints missed since the last one shown that make a session UNDELIVERABLE.
MISSED_UNDELIVERABLE = 2
#: An undeliverable session is still asked about at a researcher's prompt, at
#: most this often: the probe whose hint, once shown, ends it.
UNDELIVERABLE_PROBE_S = 1800.0


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


def shell_part(command: str) -> str:
    """What the shell itself runs: heredoc bodies and quoted strings blanked, so
    text a command only writes (a CHANGELOG line, a doc) never reads as run."""
    return _QUOTED.sub("''", _HEREDOC.sub(lambda m: f"<<{m.group(2)}{m.group(3)}\n", command))


def _segments(text: str) -> list[list[str]]:
    """A shell line's simple commands, as words; [] when any line of it cannot
    be split. `text` is `shell_part`'s (quoted strings and heredoc bodies
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


# -- the request ------------------------------------------------------------------


def scrubbed(text: str, limit: int = MAX_TEXT_CHARS) -> str:
    """`text` as it may leave this machine: every credential the capture's one
    detector finds replaced (`probe.tap_core.secrets`, as the daemon's store and
    the tap's journal do before transcript text goes out), then cut to `limit`."""
    from probe.tap_core import secrets as detector  # not the stdlib `secrets` this module uses

    clean, _rules = detector.redact(text)
    return clean[:limit]


def window_due(stamp: float, since: float | None, messages) -> bool:
    """A window look is due at an agent step stamped `stamp`: WINDOW_GAP_S on the
    window clock (`since`: the last window look, the researcher's prompt or the
    turn's first step) and at least one agent message since (`messages`)."""
    return since is not None and bool(messages) and stamp - since >= WINDOW_GAP_S


def window_segments(messages) -> list[str]:
    """A window's `segments`: the agent's messages (kept oldest first), newest
    first, at most WINDOW_MAX_SEGMENTS, each stripped and kept to
    WINDOW_SEGMENT_CHARS plus the scan margin (`scrubbed` cuts it when sent)."""
    out: list[str] = []
    for message in reversed(list(messages)):
        message = (message or "").strip()
        if message:
            out.append(message[:WINDOW_SEGMENT_CHARS + SCAN_MARGIN_CHARS])
            if len(out) >= WINDOW_MAX_SEGMENTS:
                break
    return out


def window_text(segments) -> str:
    """A window's `text`: its segments (scanned already) joined, newest first,
    at most MAX_TEXT_CHARS (the server reads names from it)."""
    return "\n\n".join(segments)[:MAX_TEXT_CHARS]


def shows_mid_turn(adapter) -> bool:
    """Whether the harness hands a `[Probe]` message over after a tool call,
    mid-turn (`Capabilities.inject_tool`). A window hint needs it: on one that
    shows messages only at the next prompt (Kimi Code), the turn's end would
    withdraw every window hint before it is seen."""
    return bool(getattr(getattr(adapter, "capabilities", None), "inject_tool", False))


def names_trigger(data: object) -> bool:
    """A 422 whose detail names the `trigger` field: a server that knows no
    `window` lookup (any other 422 is about one request's content)."""
    detail = data.get("detail") if isinstance(data, dict) else None
    return isinstance(detail, list) and any(
        isinstance(item, dict) and "trigger" in (item.get("loc") or []) for item in detail)


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
    #: Set by `abort()` for every endpoint (the lane closing): no request, and
    #: no second try of one in flight, goes after it.
    closing = False

    def abort(self, base: str | None = None) -> None:
        if base is None:
            self.closing = True
        super().abort(base)

    def __call__(self, ep: Endpoint, body: dict) -> tuple[int | None, object]:
        """`(HTTP status, the JSON answer)`, or `(None, None)` with no answer in time."""
        if self.closing:
            return None, None
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
        limit = WINDOW_TIMEOUT_S if body.get("trigger") == Trigger.WINDOW else TIMEOUT_S
        deadline = time.monotonic() + limit
        cutoff = threading.Timer(limit, self.abort, args=(ep.base_url,))
        cutoff.daemon = True
        cutoff.start()
        try:
            return self._post(ep, f"{prefix}{ROUTE}", payload, headers, deadline, limit)
        finally:
            cutoff.cancel()

    def _post(self, ep: Endpoint, path: str, payload: bytes, headers: dict, deadline: float, limit: float):
        import http.client

        for attempt in (1, 2):
            try:
                conn = self._connection(ep.base_url)
                # One socket operation, at most this request's own limit: a kept
                # connection's next connect, and its socket now.
                conn.timeout = limit
                if conn.sock is not None:
                    conn.sock.settimeout(limit)
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
                if attempt == 2 or time.monotonic() >= deadline or self.closing:
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


#: A ledger line for a hint the lane took back before it was shown (`_take_back`).
LEDGER_WITHDRAWN = "withdrawn"
#: A hint claimed this long ago with no `shown` line, from a deliverer that
#: writes them, never reached the agent (its handoff failed after the claim).
SHOWN_AFTER_CLAIM_S = 60.0


def _jsonl(path: Path, tail_bytes: int) -> list[dict]:
    """The object lines of a JSONL file's last `tail_bytes`; [] when unreadable."""
    try:
        with path.open("rb") as handle:
            size = os.fstat(handle.fileno()).st_size
            handle.seek(max(0, size - tail_bytes))
            text = handle.read().decode("utf-8", "replace")
    except OSError:
        return []
    out = []
    for line in text.splitlines():
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        if isinstance(entry, dict):
            out.append(entry)
    return out


def _stamped(entries: list[dict]) -> dict[str, tuple[float, str, bool]]:
    """id -> (the first `at`, its `by`, whether its claimer writes `shown`
    lines: `shows`) of claim-log / shown-log lines."""
    out: dict[str, tuple[float, str, bool]] = {}
    for entry in entries:
        mid, at = entry.get("id"), entry.get("at")
        if isinstance(mid, str) and isinstance(at, (int, float)) and mid not in out:
            out[mid] = (float(at), str(entry.get("by") or ""), entry.get("shows") == 1)
    return out


def delivery_facts(sid: str, state: str, ledger: Path) -> dict:
    """What the files say about the hints the lane posted to `sid` (its ledger
    and the mailbox): `posted` and `withdrawn` (id -> when), the deliverers'
    `claims` and `shown` lines (id -> (when, by)), the hints still `waiting`,
    and the deliverer heartbeat `alive` (or None)."""
    from probe.daemon import mailbox

    posted: dict[str, float] = {}
    withdrawn: dict[str, float] = {}
    for entry in _jsonl(ledger, LEDGER_TAIL_BYTES):
        mid, at = entry.get("id"), entry.get("at")
        if not isinstance(mid, str) or not isinstance(at, (int, float)):
            continue
        if entry.get("event") == LEDGER_WITHDRAWN:
            withdrawn.setdefault(mid, float(at))
        elif isinstance(entry.get("keys"), list):
            posted.setdefault(mid, float(at))
    with mailbox.rooted(state):
        claims_path, shown_path = mailbox.claim_log_path(sid), mailbox.shown_log_path(sid)
        alive = mailbox.read_alive(sid)
        waiting = {msg.id for _path, msg in mailbox.waiting(sid)
                   if msg.origin == mailbox.ORIGIN_HINT and msg.kind == mailbox.Kind.MESSAGE}
    claims = {mid: hit for mid, hit in _stamped(_jsonl(claims_path, LEDGER_TAIL_BYTES)).items() if mid in posted}
    shown = {mid: hit for mid, hit in _stamped(_jsonl(shown_path, LEDGER_TAIL_BYTES)).items() if mid in posted}
    return {"posted": posted, "withdrawn": withdrawn, "claims": claims, "shown": shown, "waiting": waiting,
            "alive": alive}


def delivery_receipt(facts: dict, *, tool_calls, prompts, mid_turn: bool, now: float) -> dict:
    """Whether the hints posted to a session reach its agent, from
    `delivery_facts` and the session's tool-call and prompt stamps (epoch
    seconds, the transcript's own; `prompts` only those that started a turn).
    A hint REACHED the agent when a deliverer wrote its `shown` line, or when
    a deliverer that writes none claimed it (its claim line has no `shows`: one
    from before them, so an upgrade or a rollback judges every claim by the
    deliverer that made it). A hint not reached MISSED its chance when, while
    it waited, the agent made MISSED_TOOL_CALLS tool calls in turns whose one
    hint slot was still free (only on a harness that shows a hint mid-turn), or
    when a deliverer that writes `shown` lines claimed it SHOWN_AFTER_CLAIM_S
    ago and wrote none. MISSED_UNDELIVERABLE
    misses since the last hint that reached it make the session UNDELIVERABLE;
    else a fresh deliverer heartbeat, or a hint reached within
    DELIVERED_RECENTLY_S, makes it OK; else UNPROVEN. Counts are over the
    ledger's week; the `delivery` field of a `/v1/hints` request."""
    import bisect

    posted = sorted(facts["posted"].items(), key=lambda item: item[1])
    claims, shown, withdrawn = facts["claims"], facts["shown"], facts["withdrawn"]
    waiting, alive = facts["waiting"], facts["alive"]

    def reached_at(mid: str) -> float | None:
        if mid in shown:
            return shown[mid][0]
        claim = claims.get(mid)
        return claim[0] if claim is not None and not claim[2] else None

    reached = sorted(t for mid, _at in posted if (t := reached_at(mid)) is not None)
    turns = sorted(prompts)
    calls = sorted(tool_calls)

    def slot_free(t: float) -> bool:
        i = bisect.bisect_right(turns, t)
        start = turns[i - 1] if i else float("-inf")
        j = bisect.bisect_left(reached, start)
        return not (j < len(reached) and reached[j] < t)

    missed: set[str] = set()
    for index, (mid, at) in enumerate(posted):
        if reached_at(mid) is not None:
            continue
        claim = claims.get(mid)
        if claim is not None:  # by a deliverer that writes `shown` lines (`reached_at`)
            if now - claim[0] >= SHOWN_AFTER_CLAIM_S:
                missed.add(mid)  # taken, never handed over
            continue
        if not mid_turn:
            continue
        ends = [now]
        if mid in withdrawn:
            ends.append(withdrawn[mid])
        if mid not in waiting and mid not in withdrawn:
            ends.append(at + mailbox_ttl())  # expired, or replaced by the next one
            if index + 1 < len(posted):
                ends.append(posted[index + 1][1])
        end = min(ends)
        lo = bisect.bisect_left(calls, at + MISSED_AFTER_S)
        hi = bisect.bisect_left(calls, end)
        if sum(1 for t in calls[lo:hi] if slot_free(t)) >= MISSED_TOOL_CALLS:
            missed.add(mid)
    last = reached[-1] if reached else None
    since = [mid for mid, at in posted if last is None or at > last]
    by = (alive or {}).get("by") if alive else None
    if by is None and (shown or claims):
        by = max([*shown.values(), *claims.values()])[1]  # the latest line's
    deliverer = _DELIVERER_OF.get(by, Deliverer.OTHER) if by else None
    alive_age = now - float(alive["at"]) if alive else None
    fresh = alive_age is not None and alive_age <= DELIVERER_FRESH_S.get(deliverer, DELIVERER_FRESH_DEFAULT_S)
    if sum(1 for mid in since if mid in missed) >= MISSED_UNDELIVERABLE:
        state = DeliveryState.UNDELIVERABLE
    elif fresh or (last is not None and now - last <= DELIVERED_RECENTLY_S):
        state = DeliveryState.OK
    else:
        state = DeliveryState.UNPROVEN
    return {
        "state": state,
        "deliverer": deliverer,
        "posted": len(posted),
        "claimed": sum(1 for mid, _at in posted if mid in claims),
        "shown": sum(1 for mid, _at in posted if mid in shown),
        "missed": len(missed),
        "withdrawn": sum(1 for mid, _at in posted if mid in withdrawn and mid not in missed
                         and reached_at(mid) is None),
        "unshown_since_shown": sum(1 for mid in since if reached_at(mid) is None),
        "last_shown_age_s": None if last is None else round(max(0.0, now - last), 1),
        "heartbeat_age_s": None if alive_age is None else round(max(0.0, alive_age), 1),
    }


def mailbox_ttl() -> float:
    """How long a hint may wait in a mailbox (`mailbox.UNASKED_TTL_S`)."""
    from probe.daemon import mailbox

    return float(mailbox.UNASKED_TTL_S)


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
    #: A window's agent messages, newest first (`window_segments`): taken from
    #: the session's window when the lookup goes (`take_due`).
    segments: list = field(default_factory=list)
    #: The session's hints posted (`_State.posted`) when its request was built.
    posted_before: int = 0


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
    #: When the transcript was last read without an error (`clock`).
    read_ok_at: float = float("-inf")
    #: The file's size when all that was left past `offset` was an unfinished
    #: line: not read again until it grows.
    partial_at: int | None = None


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


class HintLane:
    """The service's one hint lane (see the module docstring).

    `sessions()` lists the sessions to read (`followed`), asked on the lane's
    tail thread. Seams for tests: `transport(endpoint, body) -> (status, data)`,
    `endpoint_of(env)`, `post(sid, state, message) -> bool`, `withdraw(sid,
    state) -> [ids]`, `delivered(sid, state) -> {ids}`, `waiting(sid, state) ->
    {ids}`, `senders` (where Claude Code's session records are), the clocks.
    `posted(sid)` is told of each hint posted (the server says
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
        #: The window thread's own: a fetcher's kept connections are not shared
        #: across threads. A test's `transport` serves both.
        self.window_transport = transport if transport is not None else HintFetcher(version)
        self.endpoint_of = endpoint_of
        self._post = post
        self._withdraw = withdraw
        self._delivered = delivered
        self._waiting = waiting
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
        #: (base URL, key) whose window lookups the server answered as such (a 200
        #: with `trigger_class: window`), with no 404 / 422 naming `trigger` since (W3).
        self._window_ok: dict[tuple, bool] = {}
        #: (base URL, key) -> its window lookups failed in a row, whichever session's.
        self._window_key_failures: dict[tuple, int] = {}

    # -- lifecycle --------------------------------------------------------------

    def changed(self) -> None:
        """A recording started or changed: look now (the threads start on the first)."""
        if not self.enabled or self._closed:
            return
        try:
            if not self._threads:
                for name, target, args in (("hints-tail", self._tail_loop, ()),
                                           ("hints-lookup", self._lookup_loop, (False,)),
                                           ("hints-window", self._lookup_loop, (True,))):
                    thread = threading.Thread(target=target, args=args, name=name, daemon=True)
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
        for transport in {id(t): t for t in (self.transport, self.window_transport)}.values():
            abort = getattr(transport, "abort", None)
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
        wakes at prompts again. Its `.window` marker is touched in the same beat
        only while window hints are proven working for it (`_window_works`): its
        reader then stops its check-ins (`model.window_hints_live`). Neither is
        touched unless the hints posted here reach the agent (`delivery_receipt`
        OK: a deliverer's heartbeat, or a hint shown lately)."""
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
        receipt = self._receipt(session, self._state(session.sid))
        if receipt is None or receipt["state"] != DeliveryState.OK:
            # Lookups work, but nothing says a hint reaches this agent: its
            # reader keeps its prompt turns and check-ins (plan hints-relevance R12).
            return
        from probe.daemon import mailbox

        with mailbox.rooted(session.state):
            path = mailbox.hints_live_path(session.sid)
            window = mailbox.hints_window_path(session.sid)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()  # an existing one's mtime moves to now
        if self._window_works(session, ep, now):
            window.touch()

    def _window_works(self, session: Followed, ep: Endpoint, now: float) -> bool:
        """Window hints proven working for `session` (plan hints-window-trigger
        W3): its transcript read without an error within WINDOW_READ_FRESH_S;
        its server and key answered a window lookup as one, with no 404 (or 422
        naming `trigger`) to one since; and fewer than WINDOW_FAILURES_STOP of its window lookups
        in a row failed, its own or its key's; its harness shows a hint mid-turn
        (`shows_mid_turn`); and its window clock started within WINDOW_COVERS_S
        (a turn of tool calls only, or a window that could not go, is looked at
        by no one). Until then its reader keeps its check-ins."""
        tail = self._tails.get(session.sid)
        if tail is None or now - tail.read_ok_at > WINDOW_READ_FRESH_S or not shows_mid_turn(tail.adapter):
            return False
        pair = (ep.base_url, ep.key)
        with self._cv:
            state = self._states.get(session.sid)
            failures = state.window_failures if state is not None else 0
            since = state.window_since if state is not None else None
            return (self._window_ok.get(pair, False) and failures < WINDOW_FAILURES_STOP
                    and self._window_key_failures.get(pair, 0) < WINDOW_FAILURES_STOP
                    and (since is None or self.wall() - since <= WINDOW_COVERS_S))

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
            tail.read_ok_at = self.clock()
            if tail.offset is None:
                tail.inode = info.st_ino
                tail.offset = max(0, info.st_size - INITIAL_BACK_BYTES)
                tail.skipping = tail.offset > 0  # mid-line: on from the next line
            elif info.st_ino != tail.inode or info.st_size < tail.offset:
                # Rewritten or replaced under the offset: on from its end.
                tail.inode, tail.offset, tail.skipping = info.st_ino, info.st_size, False
                tail.partial_at = None
                return
            if info.st_size <= tail.offset:
                tail.first = False
                return
            if tail.partial_at == info.st_size:
                return  # only an unfinished line past the offset, and no new byte
            size = info.st_size
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
                tail.offset, tail.partial_at = start, size
            return
        tail.partial_at = None
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

        when = stamp if stamp is not None else self.wall()
        marks = [e.kind for e in events
                 if e.stream == MAIN_STREAM and e.kind in (Kind.TOOL_CALL, Kind.PROMPT, Kind.TURN_END)]
        if marks:
            # A waiting hint's chances to be shown (`delivery_receipt`): tool
            # calls, and the prompts that start a turn. One typed into a
            # running turn (pi's steer or follow-up, a queued message) starts
            # none: its deliverer's one hint slot for the turn stays taken.
            seen = self._state(session.sid)
            with seen.lock:
                for kind in marks:
                    if kind == Kind.TOOL_CALL:
                        seen.tool_calls.append(when)
                    elif kind == Kind.TURN_END:
                        seen.turn_open = False
                    elif not seen.turn_open:
                        seen.prompts.append(when)
                        seen.turn_open = True
        ended = any(e.stream == MAIN_STREAM and e.kind == Kind.TURN_END for e in events)
        found = [(event, hit) for event in events if (hit := trigger_of(event)) is not None]
        # The agent's steps (W1): its messages and tool calls; never a tool's
        # output, nor its reasoning. None where a window hint could not be shown.
        steps = [e for e in events if e.stream == MAIN_STREAM and e.kind in (Kind.AGENT_TEXT, Kind.TOOL_CALL)]
        if not shows_mid_turn(tail.adapter):
            steps = []
        kept: set = set()
        if found or steps:
            # `.probe.config`: the worker's own filter, over the events that would
            # ask and the messages a window would send. A tool call that is only
            # counted gets the folder's verdict alone: the filter's per-call reads
            # walk trees, and nothing of it leaves.
            line_cwd = obj.get("cwd") if isinstance(obj.get("cwd"), str) else None
            asking = {id(e) for e, _ in found} | {id(e) for e in steps if e.kind == Kind.AGENT_TEXT}
            kept = {id(e) for e in tail.filter.keep([e for e in events if id(e) in asking], stream=MAIN_STREAM,
                                                    line_cwd=line_cwd)}
            kept |= {id(e) for e in steps if id(e) not in asking
                     and not tail.filter.folder_excluded(e, line_cwd=line_cwd)}
        # Before the turn end: a line can end the turn with its last message (pi),
        # and the turn's end ends its window too.
        self._window_steps(session, [e for e in steps if id(e) in kept], when)
        if ended:
            self.turn_ended(session, newer=newer)
        for event, (trigger, text, senders) in found:
            if id(event) not in kept:
                self.stats["excluded"] += 1
                # Never asked about, but still a newer prompt: a waiting hint is stale.
                text = ""
            self.trigger(session, trigger, text, senders, happened=stamp, newer=newer)

    def _window_steps(self, session: Followed, steps: list, stamp: float) -> None:
        """The agent's steps of one line, for the window (W1): its messages kept
        (the newest WINDOW_MAX_SEGMENTS), and a window look queued at the first
        step it is due (`window_due`). Its messages are taken when it goes
        (`take_due`), so one replaced while it waits loses nothing."""
        if not steps:
            return
        from probe.daemon.events import Kind

        state = self._state(session.sid)
        with self._cv:
            if state.window_since is None:
                state.window_since = stamp  # the clock starts at the session's first step seen here
            state.window_seen = stamp
            for event in steps:
                text = (event.text or "").strip() if event.kind == Kind.AGENT_TEXT else ""
                if text:
                    state.window_messages.append(text[:WINDOW_SEGMENT_CHARS + SCAN_MARGIN_CHARS])
            if not window_due(stamp, state.window_since, state.window_messages):
                return
            if session.sid in self._pending:
                return  # a lookup waits (a window, or another trigger's): again at a later step
        self._queue_window(session, state, stamp)

    def _may_ask(self, state: _State, trigger: str) -> bool:
        """An UNDELIVERABLE session is asked about only at a researcher's
        prompt, at most every UNDELIVERABLE_PROBE_S: the probe whose hint, once
        shown, ends it. Every other session, always."""
        with state.lock:
            if (state.delivery or {}).get("state") != DeliveryState.UNDELIVERABLE:
                return True
            now = self.clock()
            if trigger == Trigger.PROMPT and now - state.probe_at >= UNDELIVERABLE_PROBE_S:
                state.probe_at = now
                return True
        self.stats["undeliverable_skipped"] += 1
        return False

    def _queue_window(self, session: Followed, state: _State, stamp: float) -> None:
        """A window look, queued. With no key, the team's hints off, or a
        session its hints do not reach, none is, and the clock starts again:
        the next is WINDOW_GAP_S on."""
        if not self._may_ask(state, Trigger.WINDOW):
            with self._cv:
                state.window_since = stamp
                state.window_messages.clear()
            return
        try:
            ep = self.endpoint_of(session.env)
        except Exception:  # noqa: BLE001 -- unknown: not asked
            ep = None
        now = self.clock()
        with self._cv:
            if ep is None or now < self._off.get((ep.base_url, ep.key), float("-inf")):
                self.stats["no_key" if ep is None else "quiet"] += 1
                state.window_since = stamp
                state.window_messages.clear()
                return
            if session.sid in self._pending:
                return
            self._pending[session.sid] = Lookup(
                sid=session.sid, session=session, trigger=Trigger.WINDOW, text="", senders=[], queued=now,
                happened=stamp, epoch=state.epoch, ep=ep)
            self._evict()
            self.stats[f"trigger_{Trigger.WINDOW}"] += 1
            # notify_all: two lookup threads wait on this condition, each for its
            # own kind, and the one woken must be the one with work.
            self._cv.notify_all()

    def _evict(self) -> None:
        """Past MAX_PENDING, the oldest waiting window goes first (the least
        asked-for), else the oldest lookup. Under the lane's condition."""
        while len(self._pending) > MAX_PENDING:
            window = next((sid for sid, job in self._pending.items() if job.trigger == Trigger.WINDOW), None)
            if window is None:
                self._pending.popitem(last=False)
            else:
                del self._pending[window]
            self.stats["dropped"] += 1

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
            with self._cv:
                # The window clock starts again (W1): the prompt gets its own
                # search now, and a window look waiting would ask about older work.
                state.window_since = happened if happened is not None else self.wall()
                state.window_messages.clear()
                waiting = self._pending.get(session.sid)
                if waiting is not None and waiting.trigger == Trigger.WINDOW:
                    del self._pending[session.sid]
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
        if not self._may_ask(state, trigger):
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
            self._evict()
            self.stats[f"trigger_{trigger}"] += 1
            self._cv.notify_all()
        return True

    def turn_ended(self, session: Followed, newer: bool = True) -> None:
        """The main agent's turn is over (TURN_END): a hint still waiting was for
        it, and the next prompt's hook would hand it over stale (R5), so it goes
        (`newer` False: not one read on a first look); a lookup in flight for it
        is stale, and one still waiting out the session's gap is not sent. The
        turn's window ends with it: its messages are not looked at again, and
        the clock starts again at the next turn's first step."""
        state = self._state(session.sid)
        with state.lock:
            state.epoch += 1
            if newer:
                self._take_back(session, state, "the turn ended")
        with self._cv:
            if self._pending.pop(session.sid, None) is not None:
                self.stats["ended"] += 1
            state.window_since = None
            state.window_messages.clear()

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
            self._ledger_events(session.sid, gone, LEDGER_WITHDRAWN)
            self._log(f"hints: session {session.sid}: {len(gone)} hint(s) withdrawn ({why})")
            with contextlib.suppress(Exception):
                self._posted(session.sid)

    # -- the lookups --------------------------------------------------------------

    def _lookup_loop(self, windows: bool) -> None:
        """One lookup thread: window lookups (`windows`), or every other kind
        (`take_due`)."""
        while True:
            with self._cv:
                job = None
                while not self._closed:
                    job, wait = self.take_due(windows)
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

    def take_due(self, windows: bool) -> tuple[Lookup | None, float | None]:
        """The next lookup of one kind that may go now, window lookups
        (`windows`) or every other kind, or `(None, how long to wait)` (None:
        until something is queued). A window leaves the machine's tokens to the
        other kind's lookups due now, and WINDOW_TOKEN_RESERVE besides. Call
        with the lane's condition held."""
        now = self.clock()
        for table in (self._holds, self._off):
            for scope in [k for k, until in table.items() if until <= now]:
                del table[scope]  # past: forgotten, so neither table grows
        if not self._pending:
            return None, None
        best, best_due, best_rank = None, None, None
        others_due_now = 0  # the other kind's lookups due now (a window leaves them their tokens)
        for sid, job in list(self._pending.items()):
            state = self._state(sid)
            if job.ep is not None and (job.ep.base_url, job.ep.key) in self._off:
                del self._pending[sid]  # its team's setting is off: not asked
                continue
            window = job.trigger == Trigger.WINDOW
            if window and not state.window_messages:
                del self._pending[sid]  # a prompt started the window again: nothing to look at
                continue
            scopes = (*_scopes(job.ep), *_window_scopes(job.ep)) if window else _scopes(job.ep)
            held = max((self._holds.get(scope, float("-inf")) for scope in scopes), default=float("-inf"))
            sent = state.window_last_sent if window else state.last_sent
            due = max(job.queued, sent + SESSION_GAP_S, held)
            if window != windows:  # the other thread's
                others_due_now += due <= now
                continue
            rank = (max(due, now), due)
            if best_rank is None or rank < best_rank:
                best, best_due, best_rank = job, due, rank
        if best is None:
            return None, None
        if best_due > now:
            return None, best_due - now
        self._refill(now)
        # A window never takes the machine's last tokens, nor those the other
        # thread's lookups due now need: a prompt finds one.
        need = WINDOW_TOKEN_RESERVE + others_due_now if windows else 1.0
        if self._tokens < need:
            return None, (need - self._tokens) / (BUCKET_PER_MIN / 60.0)
        self._tokens -= 1.0
        del self._pending[best.sid]
        state = self._state(best.sid)
        if best.trigger == Trigger.WINDOW:
            state.window_last_sent = now
            # Its messages, taken now; the clock starts again at the newest step.
            best.segments = window_segments(state.window_messages)
            state.window_messages.clear()
            state.window_since = state.window_seen
        else:
            state.last_sent = now
        return best, None

    def run_due(self) -> int:
        """Every lookup due now, on this thread, taken as the two lookup
        threads take them (the other kinds first, then the windows; tests).
        How many ran."""
        ran = 0
        while True:
            with self._cv:
                job, _wait = self.take_due(False)
                if job is None:
                    job, _wait = self.take_due(True)
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
        window = job.trigger == Trigger.WINDOW
        segments: list[str] = []
        try:
            if window:
                # Each message scanned before its cut, then joined clean.
                segments = [clean for clean in (scrubbed(m, WINDOW_SEGMENT_CHARS).strip() for m in job.segments)
                            if clean]
                text = window_text(segments)
            else:
                text = scrubbed(job.text)
        except Exception as exc:  # noqa: BLE001 -- unscanned text never leaves: no request
            self.stats["unscanned"] += 1
            self._log(f"hints: session {job.sid}: the secret scan failed ({type(exc).__name__}); not asked")
            return
        if window and not segments:
            return
        exclude: list = []
        for sender in job.senders:
            sid = self.senders.resolve(sender, session.env)
            if sid and sid != job.sid and sid not in exclude:
                exclude.append(sid)
        try:
            with state.lock:
                job.posted_before = state.posted
                shown = self._shown(session, state)
        except Exception:  # noqa: BLE001 -- unknown: none named (the all-repeated rule still holds)
            shown = []
        with self._cv:
            newer_server = any(pair[0] == ep.base_url for pair in self._window_ok)
        limit = MAX_EXCLUDE_DOC_IDS if newer_server else LEGACY_EXCLUDE_DOC_IDS
        body = {"text": text, "trigger": job.trigger, "session_id": job.sid,
                "exclude_session_ids": exclude, "exclude_doc_ids": exclude_doc_ids(shown, limit),
                "client": {"harness": harness, "mode": session.mode, "cli": self.version},
                "delivery": self._receipt(session, state, fresh=True)}
        if window:
            body["segments"] = segments
            if state.epoch != job.epoch:
                # Its turn ended, or a newer prompt came: the hint would be
                # dropped (`_deliver`), so it is not asked. Best effort: a turn
                # end read after this still drops it there.
                self.stats["stale"] += 1
                return
        started = self.clock()
        try:
            status, data = (self.window_transport if window else self.transport)(ep, body)
        except Exception as exc:  # noqa: BLE001 -- fail open
            status, data = None, None
            self._log(f"hints: session {job.sid}: the request failed: {type(exc).__name__}")
        took = (self.clock() - started) * 1000.0
        # Plan hints-latency R9: every answer's delay from the trigger, posted or
        # not, so a slow lookup shows even when it fires nothing.
        answered = f"answered {(self.wall() - job.happened) * 1000:.0f} ms after the trigger"
        line = f"hints: session {job.sid} {job.trigger}" + (f" ({len(segments)} messages)" if window else "")
        unsupported = self._window_answered(job, state, status, data) if window else False
        if status is None:
            self.stats["unanswered"] += 1
            held = ""
            if window:
                # A window waits WINDOW_TIMEOUT_S on its thread: while the server
                # is not answering, none goes for LIMITED_S.
                scope = _window_scopes(ep)[0]
                with self._cv:
                    self._holds[scope] = max(self._holds.get(scope, float("-inf")), self.clock() + LIMITED_S)
                self.stats["held_window_unanswered"] += 1
                held = f"; {_SCOPE_NAMES[scope[0]]} are not asked for {LIMITED_S:.0f} s"
            self._log(f"{line}: no answer in {took:.0f} ms; no hint{held}")
            return
        if window and (unsupported or status == 429 or (status == 200 and isinstance(data, dict)
                                                        and data.get("reason") == "rate_limited")):
            # A window's own: an older server without window lookups, or one
            # costing more than the team's rate has left. Prompts still ask.
            wait = MISSING_S if unsupported else LIMITED_S
            scope = _window_scopes(ep)[0 if unsupported else 1]
            with self._cv:
                self._holds[scope] = max(self._holds.get(scope, float("-inf")), self.clock() + wait)
            self.stats[f"held_window_{status}"] += 1
            self._log(f"{line}: answered {status}; {_SCOPE_NAMES[scope[0]]} are not asked for {wait:.0f} s; "
                      f"{answered}")
            return
        if status in (401, 403, 404, 429) or (status == 200 and isinstance(data, dict)
                                               and data.get("reason") == "rate_limited"):
            wait = {401: REFUSED_S, 403: REFUSED_S, 404: MISSING_S}.get(status, LIMITED_S)
            scope = _scopes(ep)[{401: 0, 403: 0, 404: 1}.get(status, 2)]
            with self._cv:
                self._holds[scope] = max(self._holds.get(scope, float("-inf")), self.clock() + wait)
            self.stats[f"held_{status}"] += 1
            self._log(f"{line}: answered {status}; {_SCOPE_NAMES[scope[0]]} is not asked for {wait:.0f} s; "
                      f"{answered}")
            return
        if status != 200 or not isinstance(data, dict):
            self.stats["refused"] += 1
            self._log(f"{line}: answered {status} in {took:.0f} ms; no hint; {answered}")
            return
        with self._cv:
            if not window:
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
        with self._cv:
            off = self.clock() < self._off.get((ep.base_url, ep.key), float("-inf"))
        if fire and mode == "on" and isinstance(hint, str) and hint.strip():
            if self._closed:
                outcome = Skip.CLOSED
            elif off:
                # Another lookup's answer turned the team's hints off meanwhile.
                self.stats["off"] += 1
                outcome = Skip.OFF
            elif len(hint) > MAX_HINT_CHARS:
                self.stats["too_long"] += 1
                outcome = Skip.TOO_LONG
            else:
                # Posted exactly as Probe rendered it: the mailbox shows a hint as-is
                # only when it starts with `[Probe] ` (its framing), so nothing is added.
                posted, why = self._deliver(job, state, hint, data.get("records"))
                outcome = f"posted {(self.wall() - job.happened) * 1000:.0f} ms after the trigger" if posted else why
        self.stats[f"mode_{mode}"] += 1
        self._log(f"{line}: mode={mode} fire={fire} reason={data.get('reason')} "
                  f"top={_number(data.get('top_score'))} in {took:.0f} ms; {outcome}; {answered}")

    def _window_answered(self, job: Lookup, state: _State, status: int | None, data: object) -> bool:
        """What a window lookup's answer proves (W3, `_window_works`): a 200 as a
        window shows the server and key do window lookups; a 404, or a 422
        naming `trigger`, that the server does not (True: `unsupported`). No
        answer, any other status, `engine_error` or `rate_limited` is one more
        failure in a row, the session's and its key's; a failure a retry can
        pass (no answer, a 5xx, a 429, `engine_error`, `rate_limited`) puts its
        messages back for the next look, unless its turn is over (a 4xx is
        about those messages: they go). A 200 that searched ends both runs."""
        ep = job.ep
        pair = (ep.base_url, ep.key)
        answer = data if status == 200 and isinstance(data, dict) else None
        unsupported = status == 404 or (status == 422 and names_trigger(data))
        with self._cv:
            if unsupported:
                for known in [p for p in self._window_ok if p[0] == ep.base_url]:
                    del self._window_ok[known]
            if answer is not None and answer.get("trigger_class") == Trigger.WINDOW:
                self._window_ok[pair] = True
            if answer is not None and answer.get("reason") not in ("engine_error", "rate_limited"):
                state.window_failures = 0
                self._window_key_failures.pop(pair, None)
                return False
            state.window_failures += 1
            self._window_key_failures[pair] = self._window_key_failures.get(pair, 0) + 1
            retry = status is None or status >= 500 or status == 429 or answer is not None
            if retry and state.epoch == job.epoch:
                # Looked at by no one: back as the oldest of the next look's messages.
                kept = [*reversed(job.segments), *state.window_messages][-WINDOW_MAX_SEGMENTS:]
                state.window_messages.clear()
                state.window_messages.extend(kept)
        return unsupported

    def _deliver(self, job: Lookup, state: _State, hint: str, records: object) -> tuple[bool, str]:
        session = job.session
        keys = record_keys(records)
        with state.lock:
            if state.epoch != job.epoch:
                self.stats["stale"] += 1
                return False, Skip.STALE
            if job.happened < state.posted_happened:
                self.stats["superseded"] += 1
                return False, Skip.SUPERSEDED
            if keys and (
                keys <= self._seen(session, state)
                # A hint posted while this one was asked, and delivered since,
                # shares a record with it: asked after it, the server would have
                # left that record out. (One still waiting is replaced by this.)
                or (state.posted != job.posted_before and keys & self._delivered_records(session, state))
            ):
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
            state.posted += 1
            state.posted_happened = max(state.posted_happened, job.happened)
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

    def _delivered_records(self, session: Followed, state: _State) -> set:
        """The records of the ledger's hints the session was delivered (the
        claim log), none waiting. Under the session's lock."""
        if state.ledger is None:
            state.ledger = self._load_ledger(session.sid)
        try:
            ids = self._delivered(session.sid, session.state)
        except Exception:  # noqa: BLE001 -- unknown: none counts
            return set()
        return set().union(*(keys for mid, keys in state.ledger.items() if mid in ids))

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

    def _ledger_events(self, sid: str, message_ids: list, event: str) -> None:
        """One ledger line per message id: what became of a hint posted here."""
        path = self._ledger_path(sid)
        at = self.wall()
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600), "a", encoding="utf-8") as out:
                out.write("".join(json.dumps({"id": mid, "event": event, "at": at}) + "\n" for mid in message_ids))
        except OSError as exc:
            self._log(f"hints: session {sid}: the ledger could not be written: {exc}")

    def _receipt(self, session: Followed, state: _State, *, fresh: bool = False) -> dict | None:
        """The session's `delivery_receipt` (None when its files cannot be read),
        made again at most every HINTS_LIVE_BEAT_S unless `fresh`. A change into
        or out of UNDELIVERABLE is logged, and the receipt is left beside the
        session's hint marker for `probe doctor` (`mailbox.hints_delivery_path`)."""
        now = self.clock()
        with state.lock:
            if not fresh and state.delivery is not None and now - state.delivery_at < HINTS_LIVE_BEAT_S:
                return state.delivery
            calls, prompts = list(state.tool_calls), list(state.prompts)
            before = (state.delivery or {}).get("state")
        tail = self._tails.get(session.sid)
        try:
            facts = delivery_facts(session.sid, session.state, self._ledger_path(session.sid))
            receipt = delivery_receipt(facts, tool_calls=calls, prompts=prompts,
                                       mid_turn=tail is not None and shows_mid_turn(tail.adapter), now=self.wall())
        except Exception as exc:  # noqa: BLE001 -- unknown, never "fine" nor "broken"
            self._log(f"hints: session {session.sid}: delivery unknown: {type(exc).__name__}")
            return None
        with state.lock:
            state.delivery, state.delivery_at = receipt, now
        if receipt["state"] == DeliveryState.UNDELIVERABLE and before != DeliveryState.UNDELIVERABLE:
            self.stats["undeliverable"] += 1
            self._log(f"hints: session {session.sid}: its hints are not reaching the agent "
                      f"({receipt['missed']} missed, {receipt['unshown_since_shown']} not shown since the last "
                      f"one shown); its reader keeps its turns, and hints are asked only at a prompt, at most every "
                      f"{UNDELIVERABLE_PROBE_S / 60:.0f} min, until one is shown (quit the agent and resume the session)")
        elif before == DeliveryState.UNDELIVERABLE and receipt["state"] != DeliveryState.UNDELIVERABLE:
            self._log(f"hints: session {session.sid}: hints reach the agent again")
        with contextlib.suppress(Exception):
            from probe.daemon import mailbox

            with mailbox.rooted(session.state):
                # `at` and `harness` for `probe doctor` only (`service_calls.hints_unreached`).
                mailbox.write_hints_delivery(session.sid, {**receipt, "at": self.wall(), "harness": session.harness})
        return receipt

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


def _window_scopes(ep: Endpoint | None) -> tuple:
    """A window lookup's own holds, beside `_scopes`: the server, without window
    lookups (a 404, a 422 naming `trigger`) or not answering; that key on that
    server, past its team's rate (a 429, `rate_limited`)."""
    if ep is None:
        return ()
    return (("window", ep.base_url), ("window_pair", ep.base_url, ep.key))


#: How the log names a hold's scope (never the key itself).
_SCOPE_NAMES = {"key": "this key", "server": "this server", "pair": "this key on this server",
                "window": "window lookups on this server", "window_pair": "window lookups of this key on this server"}


def _repeat_key(trigger: str, text: str) -> tuple[str, str]:
    return trigger, hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()


def _number(value: object) -> str:
    return f"{value:.3f}" if isinstance(value, (int, float)) and not isinstance(value, bool) else "-"


__all__ = ["Followed", "HintFetcher", "HintLane", "Lookup", "Senders", "Trigger", "followed", "launches_run",
           "names_trigger", "sender_of", "shows_mid_turn", "trigger_of", "window_due", "window_segments",
           "window_text"]
