"""The daemon's model: Pydantic AI's OpenAI-compatible client pointed at Probe (S2).

Every model call goes through `POST /v1/companion/chat/completions` on the
team's Probe server, authenticated with the daemon's key, metered on the
daemon's own meter (D9, R2). The server picks the model (`model="default"`) unless
`PROBE_COMPANION_MODEL` names one from its allowlist (the bake-off).
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from probe.sdk import config as sdk_config
from probe.sdk.session_marker import WIZARD_HINT

ROUTE_PREFIX = "/v1/companion"
ENV_MODEL = "PROBE_COMPANION_MODEL"
#: The reader's model, per session (daemon reads); unset, the server's `reader`
#: alias picks it (`companion.readerModel`).
ENV_READ_MODEL = "PROBE_COMPANION_READ_MODEL"
#: The header that tells the model route which lane a call is for: each lane has
#: its own in-flight slots on the server, and a call that sends it may run 30
#: minutes (without it the server keeps an old client's 150 s).
LANE_HEADER = "X-Probe-Daemon-Lane"
LANE_WRITE = "write"
LANE_READ = "read"
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

_HTTP_CLIENT = None


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
    """One HTTP client per process (both lanes, every turn), with keepalive."""
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
            timeout=httpx.Timeout(DEFAULT_TIMEOUT_S), follow_redirects=True)
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


def build(ep: Endpoint, lane: str = LANE_WRITE):
    """A Pydantic AI model for one of the daemon's two lanes. Imported lazily: the
    `daemon` extra. Each request times out after DEFAULT_TIMEOUT_S and is retried
    at most MAX_RETRIES times by the client. The writer asks for
    PROBE_COMPANION_MODEL or the server's default; the reader for
    PROBE_COMPANION_READ_MODEL or the server's `reader` alias."""
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.openai import OpenAIProvider
    from pydantic_ai.settings import ModelSettings

    from openai import AsyncOpenAI

    # The OpenAI client on this process's one keepalive HTTP client, with the
    # daemon's bounds and the lane's header.
    client = AsyncOpenAI(base_url=ep.model_base_url, api_key=ep.key, timeout=DEFAULT_TIMEOUT_S,
                         max_retries=MAX_RETRIES, default_headers={LANE_HEADER: lane}, http_client=_http_client())
    provider = OpenAIProvider(openai_client=client)
    name = (os.environ.get(ENV_READ_MODEL) or "reader") if lane == LANE_READ else (os.environ.get(ENV_MODEL) or "default")
    return OpenAIChatModel(name, provider=provider, settings=ModelSettings(timeout=DEFAULT_TIMEOUT_S))
