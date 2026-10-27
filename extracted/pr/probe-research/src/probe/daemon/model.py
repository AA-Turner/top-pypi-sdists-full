"""The daemon's model: Pydantic AI's OpenAI-compatible client pointed at Probe (S2).

Every model call goes through `POST /v1/companion/chat/completions` on the
team's Probe server, authenticated with the daemon's key, metered on the
daemon's own meter (D9, R2). The server picks the model (`model="default"`) unless
`PROBE_COMPANION_MODEL` names one from its allowlist (the bake-off).
"""

from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass
from typing import Any

from probe._compat import StrEnum
from probe.daemon import runctx

from probe.sdk import config as sdk_config
from probe.sdk.agent_session import AGENT_HEADER, AGENT_SESSION_HEADER, valid_session_id
from probe.sdk.session_marker import WIZARD_HINT

ROUTE_PREFIX = "/v1/companion"
ENV_MODEL = "PROBE_COMPANION_MODEL"
#: The reader's model, per session (daemon reads); unset, the server's `reader`
#: alias picks it (`companion.readerModel`).
ENV_READ_MODEL = "PROBE_COMPANION_READ_MODEL"
#: The team-note audit's model (daemon-team-note-audit); unset, the server's
#: `auditor` alias picks it (`companion.auditorModel`).
ENV_AUDIT_MODEL = "PROBE_COMPANION_AUDIT_MODEL"
AUDITOR_MODEL_ALIAS = "auditor"
#: The header that tells the model route which lane a call is for: each lane has
#: its own in-flight slots on the server, and a call that sends it may run 30
#: minutes (without it the server keeps an old client's 150 s).
LANE_HEADER = "X-Probe-Daemon-Lane"
LANE_WRITE = "write"
LANE_READ = "read"
LANE_AUDIT = "audit"
#: The writer's event indexer (daemon cost round 5): a cheap model that turns a
#: run's new events into one line per step with their event ids. The server
#: serves it on its own lane: a 30 s deadline, no refusal fallback (a refusal is
#: an error); it settles as the writer.
LANE_INDEX = "index"
#: The indexer's model, per session; unset, the server's `index` alias picks it.
ENV_INDEX_MODEL = "PROBE_COMPANION_INDEX_MODEL"
INDEX_MODEL_ALIAS = "index"
#: Daemon cost round 7 (F4): the model `probe daemon task` helpers run on. Their
#: calls keep their parent's lane (its slots, its meter) and ask for the server's
#: `task` alias, a cheaper model, while the server says it serves one
#: (TASK_MODEL_HEADER: on, on every chat answer); else -- an older server, or its
#: `companion_task_model` empty -- the parent's own model, as before. The
#: environment variable names a model outright (the bench).
TASK_MODEL_HEADER = "x-probe-task-model"
ENV_TASK_MODEL = "PROBE_COMPANION_TASK_MODEL"
TASK_MODEL_ALIAS = "task"
ENV_KEY = "PROBE_DAEMON_KEY"
#: One model request's timeout, and how often the client itself retries a failed
#: one. A call may take 30 minutes (Richard, 2026-09-28: a 1M context, a cold
#: cache): the timeouts are raised innermost first so the layer that fails is the
#: one that reports -- LiteLLM 1,800 s < the server's deadline 1,830 s < the
#: ingress 1,860 s < this client 1,900 s. The writer's lease (240 s) is renewed
#: WHILE a run is in progress (`agent.keep_lease`), not only between rounds.
DEFAULT_TIMEOUT_S = 1900.0
MAX_RETRIES = 1
#: A non-streaming call is silent until its answer: TCP keepalive probes the
#: connection every so often so a NAT between this machine and Probe (a cloud NAT
#: drops an idle flow after ~350 s) keeps it through a 30-minute call.
KEEPALIVE_IDLE_S = 60
KEEPALIVE_INTERVAL_S = 30
KEEPALIVE_COUNT = 5

#: The refusal fallback (2026-10-06). When the configured model's safety
#: classifier refuses a call, the server re-sends it to its fallback model and
#: names that model in SERVED_MODEL_HEADER. The refused content stays in the
#: session, so the session's worker (its process, or its run in the daemon host) sends the name back in
#: PREFER_MODEL_HEADER on every later call: the server then skips the refusing
#: model instead of paying a refused attempt first. A server without the
#: fallback never sets the header; one that does not know PREFER_MODEL_HEADER
#: ignores it.
SERVED_MODEL_HEADER = "x-probe-served-model"
PREFER_MODEL_HEADER = "X-Probe-Prefer-Model"
_CHAT_PATH = "/chat/completions"
#: The server's context sizes for the two lanes, sent on every chat answer: a
#: change reaches every client from its next request, with no release. Absent
#: (an older server), the client's own sizes stand; a server size only LOWERS one.
CONTEXT_CAP_HEADERS = {LANE_WRITE: "x-probe-context-tokens", LANE_READ: "x-probe-read-context-tokens"}
#: A server size below this is ignored: one batch of new events holds ~40K
#: estimated (up to ~85K real) tokens, so a smaller size would compact, or start
#: the reader fresh, before every request. The server refuses the same floor.
MIN_SERVER_CONTEXT_TOKENS = 100_000
_SERVER_CONTEXT_TOKENS: dict[str, int] = {}
_server_context_tokens = runctx.Shared(globals(), "_SERVER_CONTEXT_TOKENS", dict)


class WriterHistory(StrEnum):
    """What the writer's saved conversation keeps after a run (`WRITER_HISTORY_HEADER`,
    daemon cost round 5). FULL keeps everything; LEAN keeps the messages the writer
    was sent (and a compaction's summary) and drops its own answers and tool
    traffic, so the next run's request still extends this run's first one byte for
    byte -- the only prefix the model's prompt cache serves."""

    FULL = "full"
    LEAN = "lean"


class WriterEvents(StrEnum):
    """How a run's new events reach the writer (`WRITER_EVENTS_HEADER`): RAW rendered,
    or INDEX -- a cheap model's one line per step with event ids (`index.py`)."""

    RAW = "raw"
    INDEX = "index"


class PromptWake(StrEnum):
    """Whether a researcher prompt wakes the reader (`READER_PROMPT_WAKE_HEADER`)."""

    ON = "on"
    OFF = "off"


#: Settings the server sends on every chat answer beside the context sizes
#: (daemon cost round 4): the writer's least gap in seconds between two runs.
#: Absent (an older server), 0 stands. The environment variables win over the
#: server (the bench and a researcher's own override). `x-probe-reader-gate`,
#: which the server still sends for an older CLI's reader gate, is ignored.
WRITER_GAP_HEADER = "x-probe-writer-min-gap-s"
ENV_WRITER_GAP = "PROBE_DAEMON_WRITER_GAP_S"
WRITER_HISTORY_HEADER = "x-probe-writer-history"
WRITER_EVENTS_HEADER = "x-probe-writer-events"
ENV_WRITER_HISTORY = "PROBE_DAEMON_WRITER_HISTORY"
ENV_WRITER_EVENTS = "PROBE_DAEMON_WRITER_EVENTS"
#: Whether the researcher's prompt alone wakes the daemon's reader: OFF only
#: while Probe hints serve this session (`hints_live`), which every chat request
#: tells the server (HINTS_LIVE_HEADER: on | off) and the server answers OFF to;
#: ON otherwise, and what an older server's silence means. Asks and the
#: READ_EVERY_S new-events wake are never switched off. The environment
#: variable wins over both.
READER_PROMPT_WAKE_HEADER = "x-probe-reader-prompt-wake"
ENV_READER_PROMPT_WAKE = "PROBE_READER_PROMPT_WAKE"
#: Daemon cost round 7 (2026-10-25), on every chat answer like the gap. Absent (an
#: older server), each is off: today's behaviour (a new process starts from what
#: its session last heard until its first answer: `restore_pushed`). The
#: environment variables win.
#: Whether a researcher's prompt waits for the writer's least gap like a turn end
#: (`worker.Worker.deferrable`): on | off.
WRITER_PROMPT_WAITS_HEADER = "x-probe-writer-prompt-waits"
ENV_WRITER_PROMPT_WAITS = "PROBE_DAEMON_WRITER_PROMPT_WAITS"
#: How long, in seconds, a writer conversation may sit idle before the next run
#: starts fresh instead of resuming it (the model's prompt cache lives ~30 min, so
#: a resumed conversation past it is re-read at the full price); 0 = never.
WRITER_COLD_FRESH_HEADER = "x-probe-writer-cold-fresh-s"
ENV_WRITER_COLD_FRESH = "PROBE_DAEMON_WRITER_COLD_FRESH_S"
MAX_WRITER_COLD_FRESH_S = 86_400
#: More than this many folder-check "new file" events in one batch reach the
#: writer as a list of paths, not their contents (`bite.rendered`); 0 = never.
WRITER_FILE_BURST_HEADER = "x-probe-writer-file-burst"
ENV_WRITER_FILE_BURST = "PROBE_DAEMON_WRITER_FILE_BURST"
MAX_WRITER_FILE_BURST = 10_000
HINTS_LIVE_HEADER = "x-probe-hints-live"
#: The hint lane touches a served session's marker every HINTS_LIVE_BEAT_S
#: (`service.hints`); one older than this means no hint lane serves it now (the
#: service stopped, the session left its recorder, hints were switched off).
HINTS_LIVE_TTL_S = 120.0
#: A pushed gap above this is clamped: a session is never recorded less than hourly.
MAX_WRITER_GAP_S = 3600
_PUSHED: dict[str, object] = {}

_HTTP_CLIENT = None
_PREFERRED_MODEL: str | None = None
#: The session this process's daemon serves (`bind_hints`), whose hint marker
#: `hints_live` reads; None: no session, so no hints.
_HINTS_SID: str | None = None
#: The coding-agent session this process's daemon watches (`bind_session`), as
#: `(agent, session id)`; None: no session, so no session headers.
_WATCHED: tuple[str, str] | None = None
#: Each a module global in a one-session process, the run's own in the daemon host
#: (`runctx.Shared`): what the server pushed and the fallback it served belong to
#: the session that heard them, and an httpx client to the event loop that made it.
_pushed = runctx.Shared(globals(), "_PUSHED", dict)
_http = runctx.Shared(globals(), "_HTTP_CLIENT")
_preferred = runctx.Shared(globals(), "_PREFERRED_MODEL")
_hints_sid = runctx.Shared(globals(), "_HINTS_SID")
_watched = runctx.Shared(globals(), "_WATCHED")

#: An agent label the server accepts on `X-Probe-Agent` (`app/runs/agent_session.py`).
_AGENT_LABEL = re.compile(r"\A[a-z][a-z0-9_]{0,31}\Z")


def bind_hints(session_id: str | None) -> None:
    """The session whose hint marker this process reads (the worker's, at start)."""
    _hints_sid.set(session_id)


def bind_session(agent: str | None, session_id: str | None) -> None:
    """The coding-agent session this process's daemon watches (the worker's, at
    start): named on every `/v1/companion/*` call (`session_headers`), as the
    reader's MCP calls name it, so the server settles each call's dollars into
    that session (swarm visibility D5). A malformed pair names nothing."""
    ok = isinstance(agent, str) and bool(_AGENT_LABEL.match(agent)) and valid_session_id(session_id)
    _watched.set((agent, session_id) if ok else None)


def session_headers() -> dict[str, str]:
    """`X-Probe-Agent` + `X-Probe-Agent-Session` for the watched session, or {}."""
    watched = _watched.get()
    if watched is None:
        return {}
    return {AGENT_HEADER: watched[0], AGENT_SESSION_HEADER: watched[1]}


async def _name_watched_session(request) -> None:
    """Every `/v1/companion/*` request this process's client sends -- the model
    gateway, the command check -- names the watched session,
    unless the caller named one itself."""
    if ROUTE_PREFIX + "/" not in request.url.path:
        return
    for name, value in session_headers().items():
        if name not in request.headers:
            request.headers[name] = value


def _marker_fresh(path_of, now: float | None) -> bool:
    """This process's session's marker `path_of(sid)` touched within HINTS_LIVE_TTL_S."""
    sid = _hints_sid.get()
    if not sid:
        return False
    try:
        touched = path_of(sid).stat().st_mtime
    except OSError:
        return False
    return (time.time() if now is None else now) - touched <= HINTS_LIVE_TTL_S


def hints_live(now: float | None = None) -> bool:
    """Does the Probe service's hint lane serve this process's session now: its
    marker (`mailbox.hints_live_path`) touched within HINTS_LIVE_TTL_S?"""
    from probe.daemon import mailbox

    return _marker_fresh(mailbox.hints_live_path, now)


def window_hints_live(now: float | None = None) -> bool:
    """Do the Probe service's WINDOW hints serve this process's session now: its
    marker (`mailbox.hints_window_path`) touched within HINTS_LIVE_TTL_S? Then
    they cover the reader's 30-minute check-ins (plan hints-window-trigger W4)."""
    from probe.daemon import mailbox

    return _marker_fresh(mailbox.hints_window_path, now)


async def _prefer_served_model(request) -> None:
    if request.url.path.endswith(_CHAT_PATH):
        preferred = _preferred.get()
        if preferred:
            request.headers[PREFER_MODEL_HEADER] = preferred
        request.headers[HINTS_LIVE_HEADER] = PromptWake.ON.value if hints_live() else PromptWake.OFF.value


async def _remember_served_model(response) -> None:
    if not response.request.url.path.endswith(_CHAT_PATH):
        return
    served = response.headers.get(SERVED_MODEL_HEADER)
    if served:
        _preferred.set(served)
    remember_context_sizes(response.headers)
    remember_pushed_settings(response.headers)
    _confirm_restored(response.headers)


def remember_pushed_settings(headers: Any) -> None:
    """Keep the reader's prompt wake, the writer's gap and the writer's layout
    (history, events) from a chat answer's headers. A missing or malformed value
    leaves the last good one."""
    wake = (headers.get(READER_PROMPT_WAKE_HEADER) or "").strip().lower()
    if wake in {m.value for m in PromptWake}:
        _pushed.get()[READER_PROMPT_WAKE_HEADER] = PromptWake(wake)
    raw = headers.get(WRITER_GAP_HEADER)
    try:
        gap = int(str(raw).strip()) if raw is not None else None
    except ValueError:
        gap = None
    if gap is not None and gap >= 0:
        _pushed.get()[WRITER_GAP_HEADER] = min(gap, MAX_WRITER_GAP_S)
    for header, kind in ((WRITER_HISTORY_HEADER, WriterHistory), (WRITER_EVENTS_HEADER, WriterEvents),
                         (WRITER_PROMPT_WAITS_HEADER, PromptWake), (TASK_MODEL_HEADER, PromptWake)):
        value = (headers.get(header) or "").strip().lower()
        if value in {m.value for m in kind}:
            _pushed.get()[header] = kind(value)
    for header, cap in ((WRITER_COLD_FRESH_HEADER, MAX_WRITER_COLD_FRESH_S),
                        (WRITER_FILE_BURST_HEADER, MAX_WRITER_FILE_BURST)):
        number = _whole(headers.get(header))
        if number is not None:
            _pushed.get()[header] = min(number, cap)


#: The pushed settings a worker keeps in its session store (`Worker`), so a new
#: process uses the last ones it heard before its first chat answer (review
#: 10-25: until then F2 and F3 read as off, and a resumed cold conversation was
#: re-read at the full price).
PUSHED_KEPT = (WRITER_GAP_HEADER, WRITER_HISTORY_HEADER, WRITER_EVENTS_HEADER, WRITER_PROMPT_WAITS_HEADER,
               WRITER_COLD_FRESH_HEADER, WRITER_FILE_BURST_HEADER)
#: The settings `restore_pushed` took from the store, until this process's first
#: chat answer: then each one that answer did not carry is dropped, so a server
#: that never sends it (an older one, a rollback) means off again (review 10-25).
_RESTORED: set[str] = set()
_restored = runctx.Shared(globals(), "_RESTORED", set)  # each run's own in the daemon host


def pushed_snapshot() -> dict[str, str]:
    """The pushed settings heard so far, as their header values."""
    return {h: str(getattr(v, "value", v)) for h, v in _pushed.get().items() if h in PUSHED_KEPT}


def restore_pushed(saved: Any) -> None:
    """Take `saved` (a `pushed_snapshot`) for each setting not heard yet in this
    process; anything malformed is skipped, like a malformed header."""
    if not isinstance(saved, dict):
        return
    before = set(_pushed.get())
    remember_pushed_settings({h: v for h, v in saved.items() if h in PUSHED_KEPT and h not in _pushed.get()
                              and isinstance(v, str)})
    _restored.get().update(set(_pushed.get()) - before)


def _confirm_restored(headers: Any) -> None:
    """The first chat answer settles what `restore_pushed` took: a setting it did
    not carry is dropped."""
    for header in list(_restored.get()):
        if headers.get(header) is None:
            _pushed.get().pop(header, None)
    _restored.get().clear()


def _whole(raw: Any) -> int | None:
    """`raw` as a whole number >= 0, else None (missing or malformed)."""
    try:
        number = int(str(raw).strip()) if raw is not None else None
    except ValueError:
        return None
    return number if number is not None and number >= 0 else None


def _setting(env: str, header: str, cap: int) -> int:
    """A whole-number writer setting: the environment variable, else the server's,
    else 0 (off)."""
    number = _whole(os.environ.get(env))
    if number is None:
        number = int(_pushed.get().get(header, 0))  # type: ignore[call-overload]
    return min(number, cap)


def reader_prompt_wake() -> bool:
    """`PROBE_READER_PROMPT_WAKE`, else ON while no hint serves this session
    (`hints_live`), else the server's switch, else ON: does a researcher prompt
    alone wake the daemon's reader?"""
    env = (os.environ.get(ENV_READER_PROMPT_WAKE) or "").strip().lower()
    if env in {m.value for m in PromptWake}:
        return env == PromptWake.ON
    if not hints_live():
        return True
    return _pushed.get().get(READER_PROMPT_WAKE_HEADER, PromptWake.ON) == PromptWake.ON


def writer_min_gap_s() -> float:
    """`PROBE_DAEMON_WRITER_GAP_S`, else the server's gap, else 0 (no gap)."""
    env = os.environ.get(ENV_WRITER_GAP)
    if env is not None:
        try:
            return float(min(max(int(env), 0), MAX_WRITER_GAP_S))
        except ValueError:
            pass
    return float(_pushed.get().get(WRITER_GAP_HEADER, 0))  # type: ignore[arg-type]


def writer_prompt_waits() -> bool:
    """`PROBE_DAEMON_WRITER_PROMPT_WAITS`, else the server's switch, else OFF: does
    a researcher's prompt wait for the writer's least gap like a turn end?"""
    env = (os.environ.get(ENV_WRITER_PROMPT_WAITS) or "").strip().lower()
    if env in {m.value for m in PromptWake}:
        return env == PromptWake.ON
    return _pushed.get().get(WRITER_PROMPT_WAITS_HEADER, PromptWake.OFF) == PromptWake.ON


def task_model_name() -> str | None:
    """`PROBE_COMPANION_TASK_MODEL`, else the server's `task` alias while the
    server says it serves one, else None: a task runs on its parent's model."""
    env = (os.environ.get(ENV_TASK_MODEL) or "").strip()
    if env:
        return env
    return TASK_MODEL_ALIAS if _pushed.get().get(TASK_MODEL_HEADER) == PromptWake.ON else None


#: The task models this process built, by (lane, name, endpoint): one OpenAI client each.
_TASK_MODELS: dict[tuple[str, str, str, str], Any] = {}
#: Each run's own in the daemon host: a model holds an HTTP client of its run's loop.
_task_models = runctx.Shared(globals(), "_TASK_MODELS", dict)


def task_model(parent: Any) -> Any:
    """The model a `probe daemon task` of an agent on `parent` runs on: the
    `task_model_name` model on `parent`'s lane when there is one, else `parent`
    itself. A model this module did not build (a test's, the bench's replay) is
    always its own task model."""
    name = task_model_name()
    lane = getattr(parent, PROBE_LANE_ATTR, None)
    ep = getattr(parent, PROBE_ENDPOINT_ATTR, None)
    if name is None or lane is None or ep is None:
        return parent
    try:
        # The parent's endpoint in the key: a writer rebuilt after a key rotation or
        # a context switch takes its tasks with it (review 10-25).
        key = (str(lane), name, ep.base_url, ep.key)
        models = _task_models.get()
        if key not in models:
            models[key] = build(ep, str(lane), name=name)
        return models[key]
    except Exception as exc:  # noqa: BLE001 -- a task on its parent's model beats no `bash` at all
        import logging

        logging.getLogger("probe.daemon").warning("the task model is unavailable (%s): tasks run on their "
                                                  "parent's model", type(exc).__name__)
        return parent


def writer_cold_fresh_s() -> int:
    """`PROBE_DAEMON_WRITER_COLD_FRESH_S`, else the server's, else 0 (always resume)."""
    return _setting(ENV_WRITER_COLD_FRESH, WRITER_COLD_FRESH_HEADER, MAX_WRITER_COLD_FRESH_S)


def writer_file_burst() -> int:
    """`PROBE_DAEMON_WRITER_FILE_BURST`, else the server's, else 0 (every new file
    shown as it is today)."""
    return _setting(ENV_WRITER_FILE_BURST, WRITER_FILE_BURST_HEADER, MAX_WRITER_FILE_BURST)


def writer_history() -> WriterHistory:
    """`PROBE_DAEMON_WRITER_HISTORY`, else the server's (per team), else FULL."""
    env = (os.environ.get(ENV_WRITER_HISTORY) or "").strip().lower()
    if env in {m.value for m in WriterHistory}:
        return WriterHistory(env)
    return _pushed.get().get(WRITER_HISTORY_HEADER, WriterHistory.FULL)  # type: ignore[return-value]


def writer_events() -> WriterEvents:
    """`PROBE_DAEMON_WRITER_EVENTS`, else the server's (per team), else RAW."""
    env = (os.environ.get(ENV_WRITER_EVENTS) or "").strip().lower()
    if env in {m.value for m in WriterEvents}:
        return WriterEvents(env)
    return _pushed.get().get(WRITER_EVENTS_HEADER, WriterEvents.RAW)  # type: ignore[return-value]


def remember_context_sizes(headers: Any) -> None:
    """Keep the server's size for each lane from a chat answer's headers. A
    missing, malformed or too small value leaves the last good one."""
    for lane, name in CONTEXT_CAP_HEADERS.items():
        raw = headers.get(name)
        try:
            value = int(str(raw).strip()) if raw is not None else None
        except ValueError:
            value = None
        if value is not None and value >= MIN_SERVER_CONTEXT_TOKENS:
            _server_context_tokens.get()[lane] = value


def server_context_tokens(lane: str) -> int | None:
    """The server's size for `lane` (`LANE_WRITE` / `LANE_READ`), once a chat
    answer has sent one; None before that or from an older server."""
    return _server_context_tokens.get().get(lane)


def keepalive_socket_options() -> list[tuple[int, int, int]]:
    """TCP keepalive on, with the idle time this platform lets us set."""
    import socket

    opts = [(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)]
    idle = getattr(socket, "TCP_KEEPIDLE", None) or getattr(socket, "TCP_KEEPALIVE", None)  # Linux / macOS
    if idle is not None:
        opts.append((socket.IPPROTO_TCP, idle, KEEPALIVE_IDLE_S))
    if hasattr(socket, "TCP_KEEPINTVL"):
        opts.append((socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, KEEPALIVE_INTERVAL_S))
    if hasattr(socket, "TCP_KEEPCNT"):
        opts.append((socket.IPPROTO_TCP, socket.TCP_KEEPCNT, KEEPALIVE_COUNT))
    return opts


def _http_client():
    """One HTTP client per process -- per run in the daemon host (`runctx`: a
    client belongs to the event loop that made it) -- for both lanes and every
    turn, with keepalive, that keeps asking for the refusal fallback once the
    server has served it."""
    client = _http.get()
    if client is None:
        import httpx

        from probe.sdk.tls import ssl_context

        # The transport does the TLS once one is passed: the shared trust goes on it
        # (and on the client, which the package-wide guard checks).
        trust = ssl_context()
        client = httpx.AsyncClient(
            verify=trust,
            transport=httpx.AsyncHTTPTransport(verify=trust, socket_options=keepalive_socket_options()),
            timeout=httpx.Timeout(DEFAULT_TIMEOUT_S), follow_redirects=True,
            event_hooks={"request": [_prefer_served_model, _name_watched_session],
                         "response": [_remember_served_model]})
        _http.set(client)
    return client


class NoKey(RuntimeError):
    """No daemon key on this machine: daemon mode is unavailable until the wizard authorizes one."""


@dataclass(frozen=True)
class Endpoint:
    base_url: str  # the Probe API, e.g. https://api.research.prbe.ai
    key: str  # the daemon key (the companion credential)

    @property
    def model_base_url(self) -> str:
        return self.base_url.rstrip("/") + ROUTE_PREFIX


def endpoint() -> Endpoint:
    """The Probe API and the daemon's key, from the environment or the CLI config."""
    cfg = sdk_config.load_context() or {}
    base = os.environ.get("PROBE_BASE_URL") or cfg.get("base_url") or sdk_config.DEFAULT_BASE_URL
    key = os.environ.get(ENV_KEY) or cfg.get("companion_token")
    if not key:
        raise NoKey(f"no daemon key on this machine: Who records in the Probe wizard approves one ({WIZARD_HINT})")
    return Endpoint(base_url=str(base), key=str(key))


#: The lane a model `build` made calls on, and the endpoint, set on the model
#: (`task_model` builds a task's model on its parent's).
PROBE_LANE_ATTR = "_probe_lane"
PROBE_ENDPOINT_ATTR = "_probe_endpoint"


def build(ep: Endpoint, lane: str = LANE_WRITE, *, name: str | None = None, retries: int = MAX_RETRIES):
    """A Pydantic AI model for one of the daemon's lanes. Imported lazily: the
    `daemon` extra. Each request times out after DEFAULT_TIMEOUT_S and is retried
    at most MAX_RETRIES times by the client. The writer asks for
    PROBE_COMPANION_MODEL or the server's default; the reader for
    PROBE_COMPANION_READ_MODEL or the server's `reader` alias; the team-note audit
    for PROBE_COMPANION_AUDIT_MODEL or the server's `auditor` alias. `name`
    overrides all three (the audit's one re-run on the writer's model). `retries`:
    the client's own retries (the indexer takes none: it falls back to raw events)."""
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.openai import OpenAIProvider
    from pydantic_ai.settings import ModelSettings

    from openai import AsyncOpenAI

    # The OpenAI client on this process's one keepalive HTTP client, with the
    # daemon's bounds and the lane's header.
    client = AsyncOpenAI(base_url=ep.model_base_url, api_key=ep.key, timeout=DEFAULT_TIMEOUT_S,
                         max_retries=retries, default_headers={LANE_HEADER: lane}, http_client=_http_client())
    provider = OpenAIProvider(openai_client=client)
    if name is None:
        name = _lane_model(lane)
    model = OpenAIChatModel(name, provider=provider, settings=ModelSettings(timeout=DEFAULT_TIMEOUT_S))
    setattr(model, PROBE_LANE_ATTR, lane)
    setattr(model, PROBE_ENDPOINT_ATTR, ep)
    return model


def _lane_model(lane: str) -> str:
    """The model name a lane asks for when the caller names none."""
    if lane == LANE_READ:
        return os.environ.get(ENV_READ_MODEL) or "reader"
    if lane == LANE_AUDIT:
        return os.environ.get(ENV_AUDIT_MODEL) or AUDITOR_MODEL_ALIAS
    if lane == LANE_INDEX:
        return os.environ.get(ENV_INDEX_MODEL) or INDEX_MODEL_ALIAS
    return os.environ.get(ENV_MODEL) or "default"
