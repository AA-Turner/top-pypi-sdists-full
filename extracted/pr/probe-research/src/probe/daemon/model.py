"""The daemon's model: Pydantic AI's OpenAI-compatible client pointed at Probe (S2).

Every model call goes through `POST /v1/companion/chat/completions` on the
team's Probe server, authenticated with the daemon's key, metered on the
daemon's own meter (D9, R2). The server picks the model (`model="default"`) unless
`PROBE_COMPANION_MODEL` names one from its allowlist (the bake-off).
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any

from probe._compat import StrEnum

from probe.sdk import config as sdk_config
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
#: The reader's gate (daemon cost round 4, D): a cheap model that decides, before
#: an unasked reader turn, whether the reader should look at all. The server
#: serves it on its own lane: no refusal fallback, a refusal is an error.
LANE_GATE = "gate"
#: The gate's model, per session; unset, the server's `gate` alias picks it.
ENV_GATE_MODEL = "PROBE_COMPANION_GATE_MODEL"
GATE_MODEL_ALIAS = "gate"
#: The writer's event indexer (daemon cost round 5): a cheap model that turns a
#: run's new events into one line per step with their event ids. The server
#: serves it like the gate: a 30 s deadline, no refusal fallback; it settles as
#: the writer.
LANE_INDEX = "index"
#: The indexer's model, per session; unset, the server's `index` alias picks it.
ENV_INDEX_MODEL = "PROBE_COMPANION_INDEX_MODEL"
INDEX_MODEL_ALIAS = "index"
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
#: session, so this process (one worker per session) sends the name back in
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


class GateMode(StrEnum):
    """The reader gate's mode (`READER_GATE_HEADER`): OFF never calls it; SHADOW
    calls it and records its verdict, and the reader looks anyway; ON skips the
    reader's turn when the gate says so."""

    OFF = "off"
    SHADOW = "shadow"
    ON = "on"


class PromptWake(StrEnum):
    """Whether a researcher prompt wakes the reader (`READER_PROMPT_WAKE_HEADER`)."""

    ON = "on"
    OFF = "off"


#: Settings the server sends on every chat answer beside the context sizes
#: (daemon cost round 4): the reader gate's mode and the writer's least gap in
#: seconds between two runs. Absent (an older server), OFF and 0 stand. The
#: environment variables win over the server (the bench and a researcher's own
#: override).
READER_GATE_HEADER = "x-probe-reader-gate"
WRITER_GAP_HEADER = "x-probe-writer-min-gap-s"
ENV_READER_GATE = "PROBE_DAEMON_READER_GATE"
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


def bind_hints(session_id: str | None) -> None:
    """The session whose hint marker this process reads (the worker's, at start)."""
    global _HINTS_SID
    _HINTS_SID = session_id


def hints_live(now: float | None = None) -> bool:
    """Does the Probe service's hint lane serve this process's session now: its
    marker (`mailbox.hints_live_path`) touched within HINTS_LIVE_TTL_S?"""
    if not _HINTS_SID:
        return False
    from probe.daemon import mailbox

    try:
        touched = mailbox.hints_live_path(_HINTS_SID).stat().st_mtime
    except OSError:
        return False
    return (time.time() if now is None else now) - touched <= HINTS_LIVE_TTL_S


async def _prefer_served_model(request) -> None:
    if request.url.path.endswith(_CHAT_PATH):
        if _PREFERRED_MODEL:
            request.headers[PREFER_MODEL_HEADER] = _PREFERRED_MODEL
        request.headers[HINTS_LIVE_HEADER] = PromptWake.ON.value if hints_live() else PromptWake.OFF.value


async def _remember_served_model(response) -> None:
    global _PREFERRED_MODEL
    if not response.request.url.path.endswith(_CHAT_PATH):
        return
    served = response.headers.get(SERVED_MODEL_HEADER)
    if served:
        _PREFERRED_MODEL = served
    remember_context_sizes(response.headers)
    remember_pushed_settings(response.headers)


def remember_pushed_settings(headers: Any) -> None:
    """Keep the reader gate's mode, the reader's prompt wake, the writer's gap and
    the writer's layout (history, events) from a chat answer's headers. A
    missing or malformed value leaves the last good one."""
    mode = (headers.get(READER_GATE_HEADER) or "").strip().lower()
    if mode in {m.value for m in GateMode}:
        _PUSHED[READER_GATE_HEADER] = GateMode(mode)
    wake = (headers.get(READER_PROMPT_WAKE_HEADER) or "").strip().lower()
    if wake in {m.value for m in PromptWake}:
        _PUSHED[READER_PROMPT_WAKE_HEADER] = PromptWake(wake)
    raw = headers.get(WRITER_GAP_HEADER)
    try:
        gap = int(str(raw).strip()) if raw is not None else None
    except ValueError:
        gap = None
    if gap is not None and gap >= 0:
        _PUSHED[WRITER_GAP_HEADER] = min(gap, MAX_WRITER_GAP_S)
    for header, kind in ((WRITER_HISTORY_HEADER, WriterHistory), (WRITER_EVENTS_HEADER, WriterEvents)):
        value = (headers.get(header) or "").strip().lower()
        if value in {m.value for m in kind}:
            _PUSHED[header] = kind(value)


def reader_gate_mode() -> GateMode:
    """`PROBE_DAEMON_READER_GATE`, else the server's mode, else OFF."""
    env = (os.environ.get(ENV_READER_GATE) or "").strip().lower()
    if env in {m.value for m in GateMode}:
        return GateMode(env)
    return _PUSHED.get(READER_GATE_HEADER, GateMode.OFF)  # type: ignore[return-value]


def reader_prompt_wake() -> bool:
    """`PROBE_READER_PROMPT_WAKE`, else ON while no hint serves this session
    (`hints_live`), else the server's switch, else ON: does a researcher prompt
    alone wake the daemon's reader?"""
    env = (os.environ.get(ENV_READER_PROMPT_WAKE) or "").strip().lower()
    if env in {m.value for m in PromptWake}:
        return env == PromptWake.ON
    if not hints_live():
        return True
    return _PUSHED.get(READER_PROMPT_WAKE_HEADER, PromptWake.ON) == PromptWake.ON


def writer_min_gap_s() -> float:
    """`PROBE_DAEMON_WRITER_GAP_S`, else the server's gap, else 0 (no gap)."""
    env = os.environ.get(ENV_WRITER_GAP)
    if env is not None:
        try:
            return float(min(max(int(env), 0), MAX_WRITER_GAP_S))
        except ValueError:
            pass
    return float(_PUSHED.get(WRITER_GAP_HEADER, 0))  # type: ignore[arg-type]


def writer_history() -> WriterHistory:
    """`PROBE_DAEMON_WRITER_HISTORY`, else the server's (per team), else FULL."""
    env = (os.environ.get(ENV_WRITER_HISTORY) or "").strip().lower()
    if env in {m.value for m in WriterHistory}:
        return WriterHistory(env)
    return _PUSHED.get(WRITER_HISTORY_HEADER, WriterHistory.FULL)  # type: ignore[return-value]


def writer_events() -> WriterEvents:
    """`PROBE_DAEMON_WRITER_EVENTS`, else the server's (per team), else RAW."""
    env = (os.environ.get(ENV_WRITER_EVENTS) or "").strip().lower()
    if env in {m.value for m in WriterEvents}:
        return WriterEvents(env)
    return _PUSHED.get(WRITER_EVENTS_HEADER, WriterEvents.RAW)  # type: ignore[return-value]


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
            _SERVER_CONTEXT_TOKENS[lane] = value


def server_context_tokens(lane: str) -> int | None:
    """The server's size for `lane` (`LANE_WRITE` / `LANE_READ`), once a chat
    answer has sent one; None before that or from an older server."""
    return _SERVER_CONTEXT_TOKENS.get(lane)


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
    """One HTTP client per process (both lanes, every turn), with keepalive, that
    keeps asking for the refusal fallback once the server has served it."""
    global _HTTP_CLIENT
    if _HTTP_CLIENT is None:
        import httpx

        from probe.sdk.tls import ssl_context

        # The transport does the TLS once one is passed: the shared trust goes on it
        # (and on the client, which the package-wide guard checks).
        trust = ssl_context()
        _HTTP_CLIENT = httpx.AsyncClient(
            verify=trust,
            transport=httpx.AsyncHTTPTransport(verify=trust, socket_options=keepalive_socket_options()),
            timeout=httpx.Timeout(DEFAULT_TIMEOUT_S), follow_redirects=True,
            event_hooks={"request": [_prefer_served_model], "response": [_remember_served_model]})
    return _HTTP_CLIENT


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
    return OpenAIChatModel(name, provider=provider, settings=ModelSettings(timeout=DEFAULT_TIMEOUT_S))


def _lane_model(lane: str) -> str:
    """The model name a lane asks for when the caller names none."""
    if lane == LANE_READ:
        return os.environ.get(ENV_READ_MODEL) or "reader"
    if lane == LANE_AUDIT:
        return os.environ.get(ENV_AUDIT_MODEL) or AUDITOR_MODEL_ALIAS
    if lane == LANE_GATE:
        return os.environ.get(ENV_GATE_MODEL) or GATE_MODEL_ALIAS
    if lane == LANE_INDEX:
        return os.environ.get(ENV_INDEX_MODEL) or INDEX_MODEL_ALIAS
    return os.environ.get(ENV_MODEL) or "default"
