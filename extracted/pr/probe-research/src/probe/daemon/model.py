"""The daemon's model: Pydantic AI's OpenAI-compatible client pointed at Probe (S2).

Every model call goes through `POST /v1/companion/chat/completions` on the
team's Probe server, authenticated with the daemon's key, metered on the
daemon's own meter (D9, R2). The server picks the model (`model="default"`) unless
`PROBE_COMPANION_MODEL` names one from its allowlist (the bake-off).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

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

_HTTP_CLIENT = None
_PREFERRED_MODEL: str | None = None


async def _prefer_served_model(request) -> None:
    if _PREFERRED_MODEL and request.url.path.endswith(_CHAT_PATH):
        request.headers[PREFER_MODEL_HEADER] = _PREFERRED_MODEL


async def _remember_served_model(response) -> None:
    global _PREFERRED_MODEL
    if not response.request.url.path.endswith(_CHAT_PATH):
        return
    served = response.headers.get(SERVED_MODEL_HEADER)
    if served:
        _PREFERRED_MODEL = served
    remember_context_sizes(response.headers)


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


def build(ep: Endpoint, lane: str = LANE_WRITE, *, name: str | None = None):
    """A Pydantic AI model for one of the daemon's lanes. Imported lazily: the
    `daemon` extra. Each request times out after DEFAULT_TIMEOUT_S and is retried
    at most MAX_RETRIES times by the client. The writer asks for
    PROBE_COMPANION_MODEL or the server's default; the reader for
    PROBE_COMPANION_READ_MODEL or the server's `reader` alias; the team-note audit
    for PROBE_COMPANION_AUDIT_MODEL or the server's `auditor` alias. `name`
    overrides all three (the audit's one re-run on the writer's model)."""
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.openai import OpenAIProvider
    from pydantic_ai.settings import ModelSettings

    from openai import AsyncOpenAI

    # The OpenAI client on this process's one keepalive HTTP client, with the
    # daemon's bounds and the lane's header.
    client = AsyncOpenAI(base_url=ep.model_base_url, api_key=ep.key, timeout=DEFAULT_TIMEOUT_S,
                         max_retries=MAX_RETRIES, default_headers={LANE_HEADER: lane}, http_client=_http_client())
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
    return os.environ.get(ENV_MODEL) or "default"
