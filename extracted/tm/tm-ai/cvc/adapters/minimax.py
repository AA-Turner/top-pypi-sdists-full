"""cvc.adapters.minimax -- MiniMax (M3 / M2.7 / M2.5 / M2.1 / M2) adapter.

MiniMax exposes the **Anthropic Messages API** wire format at
``https://api.minimax.io/anthropic`` -- NOT OpenAI Chat Completions.
We subclass :class:`AnthropicAdapter` and only override the base URL +
default model. Tool calling, streaming, prompt caching, and usage
accounting are inherited as-is from AnthropicAdapter because the wire
format is identical to Anthropic's own API.

Authentication
--------------
``Authorization: Bearer <key>`` header -- NOT Anthropic's native ``x-api-key``!
Reference: ``cvc/agent/_vendor/hermes/agent/anthropic_adapter.py::_requires_bearer_auth``,
which explicitly lists the MiniMax endpoints as Bearer-auth. This was
the source of the v2.91.34-v2.91.36 bug: we sent x-api-key, MiniMax
rejected with 401.

API base
--------
International: https://api.minimax.io/anthropic
China:         https://api.minimaxi.com/anthropic

The international endpoint is the default. China users can override
via the ``MINIMAX_BASE_URL`` env var or the ``base_url`` argument to
``create_adapter()``.

Models (verified Jun 2026 -- https://platform.minimax.io/docs/guides/models-intro)
--------------------------------------------------------------------------------
Pricing: https://platform.minimax.io/docs/guides/pricing-paygo

- MiniMax-M3              -- 1M-token context, multimodal (text + image + video),
                              agentic reasoning + tool use, frontier coding (Jun 2026)
                              $0.30 / $1.20 per MTok
- MiniMax-M2.7            -- 200K ctx, recursive self-improvement (Mar 2026)
                              $0.30 / $1.20 per MTok
- MiniMax-M2.7-highspeed  -- Same as M2.7, 2x faster inference
                              $0.60 / $2.40 per MTok
- MiniMax-M2.5            -- 200K ctx, SOTA coding/agent (Feb 2026, legacy)
                              $0.30 / $1.20 per MTok
- MiniMax-M2.5-highspeed  -- Same as M2.5, 2x faster inference
                              $0.60 / $2.40 per MTok
- MiniMax-M2.1            -- 230B total params, 10B activated per inference
                              (Dec 2025, legacy)
                              $0.30 / $1.20 per MTok
- MiniMax-M2.1-highspeed  -- Same as M2.1, 2x faster inference
                              $0.60 / $2.40 per MTok
- MiniMax-M2              -- 200k ctx, 128k max output, original agentic-era
                              release (Oct 2025, legacy)
                              $0.30 / $1.20 per MTok

Wire-format notes
-----------------
MiniMax's Anthropic-compat layer accepts the standard Anthropic Messages
API body shape (``model``, ``messages``, ``system``, ``max_tokens``,
``temperature``, ``tools``, ``stream``).

Beta headers (per the upstream vendored reference): we send
``anthropic-beta: interleaved-thinking-2025-05-14``. We deliberately
do NOT send ``fine-grained-tool-streaming-2025-05-14`` (the upstream confirms
MiniMax rejects it on tool-use messages) or ``context-1m-2025-08-07``
(MiniMax's 1M context is native, not beta-gated).

We do NOT send ``anthropic-version`` -- MiniMax doesn't require it
(the upstream's ``build_anthropic_client`` only adds it via the SDK for
native Anthropic; Bearer-auth providers get just the SDK's default
auth_token / x-api-key which we override here to Bearer).

CVC-level notes
---------------
CVC's agent loop uses standard Anthropic-style tool calling via
``cvc.agent.llm.AgentLLM`` (which has its own per-provider dispatch).
The :class:`MiniMaxAdapter` here is used by the **non-agent** code paths
(proxy, gateway, dashboard) that go through the
``cvc.adapters.create_adapter`` factory. The runtime ``cvc`` command
itself constructs ``AgentLLM(provider="minimax", ...)`` directly. Both
paths must agree on:
  - base URL: host only (AgentLLM adds /anthropic/v1/messages)
  - auth:    Authorization: Bearer <key>
  - beta:    anthropic-beta: interleaved-thinking-2025-05-14
"""

from __future__ import annotations

import httpx

from cvc.adapters.anthropic import AnthropicAdapter

# ---- API base URLs -------------------------------------------------------
# International (default). China users can override via base_url=...
# to the China endpoint when calling create_adapter().
#
# NOTE: We store the FULL endpoint (with /anthropic path) here so the
# adapter factory can pass a base_url to AgentLLM that includes the
# provider prefix. AgentLLM's __init__ normalises this to host-only
# and prepends /anthropic/v1/messages back as the messages path -- so
# the final URL is always https://api.minimax.io/anthropic/v1/messages
# regardless of whether the caller passes the full or host-only form.
MINIMAX_API_BASE_INTL = "https://api.minimax.io/anthropic"
MINIMAX_API_BASE_CN   = "https://api.minimaxi.com/anthropic"
MINIMAX_API_BASE      = MINIMAX_API_BASE_INTL   # default

# ---- Default model (verified Jun 2026) -----------------------------------
# M3 is the current flagship (1M ctx, multimodal, frontier coding, agentic).
# We default to M3 because it's the same price as M2.7 ($0.30 / $1.20 per
# MTok as of Jun 2026) and gives the user the full 1M context window out of
# the box. Users can override per-session via `cvc --model MiniMax-M2.7`.
DEFAULT_MODEL = "MiniMax-M3"


# ---- Available models registry ------------------------------------------
# Exposed so `cvc setup` can list them and so tests can verify the
# MiniMax /anthropic/v1/models endpoint matches what we advertise here.
MINIMAX_MODELS: tuple[str, ...] = (
    "MiniMax-M3",
    "MiniMax-M2.7",
    "MiniMax-M2.7-highspeed",
    "MiniMax-M2.5",
    "MiniMax-M2.5-highspeed",
    "MiniMax-M2.1",
    "MiniMax-M2.1-highspeed",
    "MiniMax-M2",
)


class MiniMaxAdapter(AnthropicAdapter):
    """Anthropic-Messages-API-compat adapter pointed at the MiniMax API.

    The wire format is identical to Anthropic's own Messages API, so all
    we override is the base URL, the auth header, and the beta header.
    Tool calling, streaming, and usage accounting are inherited from
    AnthropicAdapter.
    """

    def __init__(
        self,
        api_key: str,
        model: str = DEFAULT_MODEL,
        base_url: str = MINIMAX_API_BASE,
    ) -> None:
        if not api_key:
            raise ValueError(
                "MiniMax API key is required but was not provided. "
                "Please check your config.json or environment variables."
            )
        # Skip AnthropicAdapter.__init__ -- its base_url is hardcoded to
        # https://api.anthropic.com and its headers are Anthropic-native.
        # Mirror its init but point at MiniMax and use Bearer auth
        # (NOT x-api-key -- MiniMax's /anthropic endpoint requires Bearer).
        self._api_key = api_key
        self._model = model
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "anthropic-beta": "interleaved-thinking-2025-05-14",
                "content-type": "application/json",
            },
            timeout=120.0,
        )


__all__ = [
    "MINIMAX_API_BASE",
    "MINIMAX_API_BASE_INTL",
    "MINIMAX_API_BASE_CN",
    "MINIMAX_MODELS",
    "DEFAULT_MODEL",
    "MiniMaxAdapter",
]
