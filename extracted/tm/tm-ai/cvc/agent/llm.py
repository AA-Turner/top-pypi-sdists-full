"""
cvc.agent.llm — Unified LLM client with tool calling for all providers.

Handles the API specifics of tool calling for each provider:
  - Anthropic: Messages API with tools
  - OpenAI: Chat Completions with function calling
  - Google: Gemini generateContent with function declarations
  - Ollama: OpenAI-compatible chat with tools

Supports both blocking and streaming responses.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import random
from dataclasses import dataclass, field
from typing import Any, AsyncIterator

import httpx

logger = logging.getLogger("cvc.agent.llm")

# ---------------------------------------------------------------------------
# Performance constants
# ---------------------------------------------------------------------------
# Granular timeouts: fast connect, generous read for streaming
_CONNECT_TIMEOUT = 10.0    # TCP + TLS handshake (seconds)
_READ_TIMEOUT = 180.0      # Streaming read (seconds) — default for most models
_READ_TIMEOUT_SLOW = 120.0 # Streaming read for thinking models (Gemini 3 Pro)
_READ_TIMEOUT_31_PRO = 90.0  # Gemini 3.1 Pro: LOW thinking ≈ <30s TTFT;
                               # if >90s the API is likely ignoring thinkingLevel
                               # and defaulting to HIGH (Deep Think Mini → minutes).
_WRITE_TIMEOUT = 60.0      # Request body upload (generous for large prompts)
_POOL_TIMEOUT = 10.0       # Waiting for a connection from the pool

# Transient error retry settings
_TRANSIENT_STATUS_CODES = {429, 500, 502, 503}  # Rate-limit, server errors
# v2.72.0 — env-tunable retry depth (CVC_STREAM_RETRIES, default 3, matches
# upstream streaming resilience). Provider-side flake protection for long agentic
# loops where one bad packet must not freeze a 100-iteration build.
_MAX_TRANSIENT_RETRIES = max(1, int(os.environ.get("CVC_STREAM_RETRIES", "3")))
_TRANSIENT_RETRY_BASE_DELAY = 1.0  # seconds, doubles each retry
_JITTER_MAX = 1.0  # max random jitter added to each retry delay

# v3.5.8 — connection-level retry for anthropic-compat providers (MiniMax, etc.)
# On Windows, the first connect to api.minimax.io frequently raises a
# ConnectError / RemoteProtocolError because the OS-level cert store and
# proxy resolution differs from macOS/Linux. Without this guard the user
# sees a raw exception and "MiniMax M3 is not working". We retry the
# _transport_ layer (handshake + first byte) only, never mid-stream, so
# partial answers cannot be corrupted.
_CONN_RETRYABLE_EXC = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
    httpx.WriteTimeout,
    httpx.PoolTimeout,
    httpx.RemoteProtocolError,
    httpx.NetworkError,
    ConnectionError,
    OSError,
)
_MAX_CONN_RETRIES = 2  # extra attempts after the first; total budget 3 POSTs

_TIMEOUT = httpx.Timeout(
    connect=_CONNECT_TIMEOUT,
    read=_READ_TIMEOUT,
    write=_WRITE_TIMEOUT,
    pool=_POOL_TIMEOUT,
)

# Connection pool limits — keep connections alive to skip TLS on subsequent requests
_POOL_LIMITS = httpx.Limits(
    max_connections=20,
    max_keepalive_connections=10,
    keepalive_expiry=120,  # seconds
)

# Whether to try HTTP/2 (requires httpx[http2] / h2 package)
try:
    import h2  # noqa: F401
    _HTTP2_AVAILABLE = True
except ImportError:
    _HTTP2_AVAILABLE = False


class RetriesExhaustedError(RuntimeError):
    """Raised when all transient-error retries are exhausted.

    The outer agent loop should *not* re-retry these — the inner retry
    loop has already waited through exponential backoff.
    """


@dataclass
class ToolCall:
    """A single tool call from the LLM."""
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class LLMResponse:
    """Unified response from any provider."""
    text: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)
    finish_reason: str = "stop"
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cache_read_tokens: int = 0
    _provider_meta: dict[str, Any] = field(default_factory=dict)

    @property
    def has_tool_calls(self) -> bool:
        return len(self.tool_calls) > 0


@dataclass
class StreamEvent:
    """A single event from a streaming LLM response."""
    type: str          # "text_delta", "tool_call_start", "tool_call_delta", "done", "usage"
    text: str = ""
    tool_call: ToolCall | None = None
    tool_call_index: int = 0
    args_delta: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cache_read_tokens: int = 0
    _provider_meta: dict[str, Any] = field(default_factory=dict)


def _friendly_anthropic_error(
    exc: "httpx.HTTPStatusError",
    provider: str,
    model: str,
) -> str | None:
    """Translate anthropic-compat HTTP error responses into one-liners.

    MiniMax / Kimi / DeepSeek all speak the Anthropic Messages API. When
    they 4xx, the body is JSON like ``{"type":"error","error":{"type":
    "authentication_error","message":"…"}}`` — useless to the user. We
    translate the common cases (auth, permission, not_found, rate_limit,
    bad_request) into plain English, prefixed with the provider name so
    the user knows which provider is misbehaving.

    Returns None if the error doesn't match a known case — in which case
    the caller re-raises the original ``HTTPStatusError`` with full
    context.
    """
    try:
        status = exc.response.status_code
        body_text = (exc.response.text or "").strip()
        try:
            payload = exc.response.json()
        except Exception:
            payload = {}
    except Exception:
        return None

    err_type = ""
    err_msg = ""
    if isinstance(payload, dict):
        err = payload.get("error") or {}
        if isinstance(err, dict):
            err_type = (err.get("type") or "").strip()
            err_msg = (err.get("message") or "").strip()

    # Status 401 — bad/missing API key. Most common case.
    if status == 401:
        return (
            f"{provider}: authentication failed (401). "
            f"Check that your API key is valid for {provider} and "
            f"has access to {model}. "
            f"Set it via 'cvc setup', $env:{provider.upper().replace('-', '_')}_API_KEY, "
            f"or ~/.cvc/config.yaml."
        )
    # Status 403 — account-level block (insufficient credits, region block, etc.)
    if status == 403:
        return (
            f"{provider}: access denied (403). "
            f"Your {provider} account may be out of credits, "
            f"region-restricted, or not authorized to use {model}. "
            f"Reason from server: {err_msg or 'no detail'}"
        )
    # Status 404 — wrong model name or wrong base URL.
    if status == 404:
        return (
            f"{provider}: model or endpoint not found (404). "
            f"Either {model!r} is not a real model on {provider}, "
            f"or your base URL is wrong. "
            f"Try 'cvc setup --provider {provider}' to confirm. "
            f"Server said: {err_msg or 'not found'}"
        )
    # Status 429 — rate-limited. Already handled by the higher-level
    # _TRANSIENT_STATUS_CODES path, but if it leaks through, be friendly.
    if status == 429:
        return (
            f"{provider}: rate-limited (429). "
            f"Wait a few seconds and retry. {err_msg}"
        )
    # Status 400 — invalid request. The Anthropic shape usually has a
    # 'type' that pinpoints the field. Surface the type + truncated msg.
    if status == 400:
        if err_type:
            return (
                f"{provider}: rejected the request (400, "
                f"{err_type}). {err_msg[:200]}"
            )
        return (
            f"{provider}: bad request (400). "
            f"The request body was rejected. {err_msg[:200]}"
        )
    # 402 — Anthropic uses this for billing-required endpoints
    # (rare for anthropic-compat providers, but worth catching).
    if status == 402:
        return (
            f"{provider}: payment required (402). "
            f"Add credits at your {provider} dashboard."
        )
    # 5xx — server-side problem. Don't translate; let the higher-level
    # retry path take care of it.
    return None


class AgentLLM:
    """
    Unified LLM client that supports tool calling across all providers.

    Handles the translation between each provider's tool calling format
    and a common interface used by the agent loop.
    """

    # Common model name corrections (typo / shorthand → actual API name)
    _MODEL_ALIASES: dict[str, str] = {
        # Google Gemini aliases
        # NOTE: gemini-3-pro-preview / gemini-3-flash-preview require Google
        # allowlist access and are NOT available to standard Gemini API keys.
        # Keep the explicit names so users who *do* have access can use them,
        # but point bare shorthands at the stable GA models.
        "gemini-3.5": "gemini-3.5-flash",
        "gemini-3.1": "gemini-3.1-pro",
        "gemini-3": "gemini-3-flash-preview",   # safe fast default
        "gemini-pro": "gemini-3.1-pro",
        "gemini-flash": "gemini-3.5-flash",
        "gemini-3.5-flash": "gemini-3.5-flash",
        "gemini-3.1-pro": "gemini-3.1-pro",
        "gemini-3.1-flash-lite": "gemini-3.1-flash-lite",
        "gemini-2.5-flash": "gemini-2.5-flash",
        "gemini-2.5-pro": "gemini-2.5-pro",
        "gemini-1.5-flash": "gemini-1.5-flash",
        "gemini-1.5-pro": "gemini-1.5-pro",
        # Anthropic aliases
        "claude-opus": "claude-opus-4-8",
        "claude-sonnet": "claude-sonnet-4-6",
        "claude-haiku": "claude-haiku-4-5",
        "opus": "claude-opus-4-8",
        "opus-4.8": "claude-opus-4-8",
        "sonnet": "claude-sonnet-4-6",
        "sonnet-4.6": "claude-sonnet-4-6",
        "haiku": "claude-haiku-4-5",
        "claude-3-5-sonnet": "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku": "claude-3-5-haiku-20241022",
        "claude-3-opus": "claude-3-opus-20240229",
        # NVIDIA NIM aliases — Build endpoint, free tier
        "nemotron": "nvidia/nemotron-3-super-120b-instruct",
        "nemotron-3-super": "nvidia/nemotron-3-super-120b-instruct",
        "nemotron-super": "nvidia/nemotron-3-super-120b-instruct",
        "kimi-k2": "moonshotai/kimi-k2-instruct",
        "minimax-m2": "minimaxai/minimax-m2",
        # MiniMax (api.minimax.io) — Anthropic-Messages-API-compatible, M3 is the flagship
        "minimax": "MiniMax-M3",
        "minimax-m3": "MiniMax-M3",
        "minimax-m2.7": "MiniMax-M2.7",
        "minimax-m2.5": "MiniMax-M2.5",
        "minimax-m2.1": "MiniMax-M2.1",
        "glm-5": "zai-org/glm-4.6",
        # OpenAI aliases
        "gpt-4o": "gpt-4o",
        "gpt-4o-mini": "gpt-4o-mini",
        "o1-mini": "o1-mini",
        "o1-preview": "o1-preview",
    }

    def __init__(
        self,
        provider: str,
        api_key: str,
        model: str,
        base_url: str = "",
        no_think: bool = False,
    ) -> None:
        self.provider = provider.lower()
        # Canonicalize "copilot" → "github" (single canonical name everywhere).
        if self.provider == "copilot":
            self.provider = "github"
        self.api_key = api_key
        self.base_url = base_url
        self.no_think = no_think  # If True, disable model thinking (faster, lower quality)

        # Auto-correct common model name mistakes (except for GitHub provider which uses exact dynamic IDs)
        if self.provider != "github":
            corrected = self._MODEL_ALIASES.get(model)
            if corrected:
                logger.info("Auto-corrected model name '%s' → '%s'", model, corrected)
                model = corrected
        self.model = model

        # Build the httpx client for the provider
        headers: dict[str, str] = {"Content-Type": "application/json"}

        if self.provider == "anthropic":
            self._api_url = base_url or "https://api.anthropic.com"
            self._api_messages_path = "/v1/messages"  # Anthropic native
            headers.update({
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "anthropic-beta": "prompt-caching-2024-07-31",
            })
        elif self.provider == "openai":
            self._api_url = base_url or "https://api.openai.com"
            self._api_messages_path = "/v1/chat/completions"  # not used by OpenAI path
            headers["Authorization"] = f"Bearer {api_key}"
        elif self.provider == "google":
            self._api_url = base_url or "https://generativelanguage.googleapis.com"
            self._api_messages_path = "/v1/chat/completions"  # not used by Google path
        elif self.provider == "vertex":
            # base_url must be the full Vertex AI OpenAI-compat endpoint
            # e.g. https://us-central1-aiplatform.googleapis.com/v1/
            #          projects/{project}/locations/{location}/endpoints/openapi
            self._api_url = base_url or ""
            self._api_messages_path = "/chat/completions"  # Vertex-specific
            if not self._api_url:
                raise ValueError(
                    "Vertex AI requires a base_url (built from Project ID + Location). "
                    "Run 'cvc setup' to configure Vertex AI."
                )
            # Vertex AI uses ADC OAuth2 tokens — obtain and auto-refresh
            from cvc.adapters.vertex import get_vertex_access_token, get_vertex_credentials
            self._vertex_credentials = None
            try:
                self._vertex_credentials, _ = get_vertex_credentials()
                token, self._vertex_credentials = get_vertex_access_token(self._vertex_credentials)
                headers["Authorization"] = f"Bearer {token}"
            except Exception as exc:
                logger.warning("Vertex AI ADC auth failed: %s", exc)
                # Fall back to api_key if provided (for testing / service accounts)
                if api_key:
                    headers["Authorization"] = f"Bearer {api_key}"
        elif self.provider == "ollama":
            self._api_url = base_url or "http://localhost:11434"
            self._api_messages_path = "/api/chat"  # Ollama native (not /v1/chat/completions)
        elif self.provider == "lmstudio":
            # LM Studio exposes a full OpenAI-compatible API at localhost:1234
            # No API key required — set a placeholder so the Authorization header
            # doesn't cause a rejection on stricter LM Studio builds.
            self._api_url = base_url or "http://localhost:1234"
            self._api_messages_path = "/v1/chat/completions"
            headers["Authorization"] = f"Bearer {api_key or 'lm-studio'}"
        elif self.provider == "github":
            self._github_oauth_token = api_key
            self._github_token_expiry = 0
            self._api_url = base_url or "https://api.individual.githubcopilot.com"
            self._api_messages_path = "/chat/completions"  # GitHub Copilot uses bare path
            # Headers will be set by _ensure_github_token()
        elif self.provider == "nvidia":
            # NVIDIA NIM (Build) — OpenAI-compatible, free tier with Nemotron 3 Super 120B (262k ctx)
            # Default model: nvidia/nemotron-3-super-120b-instruct
            self._api_url = base_url or "https://integrate.api.nvidia.com"
            self._api_messages_path = "/v1/chat/completions"
            headers["Authorization"] = f"Bearer {api_key}"
        elif self.provider == "minimax":
            # MiniMax (api.minimax.io) — Anthropic-Messages-API-compatible, M3 is the flagship
            # Base URL: https://api.minimax.io/anthropic (Anthropic protocol, NOT OpenAI)
            # Pricing: https://platform.minimax.io/docs/guides/pricing-paygo (Jun 2026)
            # Default model: MiniMax-M3 (1M ctx, multimodal, $0.30/$1.20 per MTok)
            #
            # Auth: Authorization: Bearer <key> — NOT x-api-key!
            # Reference: cvc/agent/_vendor/hermes/agent/anthropic_adapter.py:_requires_bearer_auth
            # and build_anthropic_client() — upstream confirms MiniMax's /anthropic
            # endpoint requires Bearer auth (not Anthropic's native x-api-key).
            # See upstream#6039, #16748.
            #
            # Beta headers: we send `anthropic-beta: interleaved-thinking-2025-05-14`.
            # Upstream strips `fine-grained-tool-streaming-2025-05-14` for MiniMax
            # (rejected with connection errors on tool-use) and `context-1m-2025-08-07`
            # (not needed for MiniMax — its 1M context is native, not beta-gated).
            #
            # Path: /v1/messages. Upstream's full base URL is
            # "https://api.minimax.io/anthropic" — the SDK adds /v1/messages.
            # But our AgentLLM uses raw httpx (not the Anthropic SDK), and
            # httpx.URL(...).join("/v1/messages") strips the last path segment,
            # producing "https://api.minimax.io/v1/messages" (wrong).
            # The fix: normalise the base URL to the host only and carry the
            # full path in _api_messages_path. This handles BOTH:
            #   - cvc's own base_url default ("https://api.minimax.io") → no-op
            #   - cvc/agent/chat.py passing "https://api.minimax.io/anthropic" → we strip /anthropic
            #   - user env var MINIMAX_BASE_URL="https://api.minimax.io/anthropic" → same
            #   - China endpoint "https://api.minimaxi.com/anthropic" → same
            norm = (base_url or "https://api.minimax.io").rstrip("/")
            if norm.endswith("/anthropic"):
                norm = norm[: -len("/anthropic")]
            self._api_url = norm
            self._api_messages_path = "/anthropic/v1/messages"
            headers["Authorization"] = f"Bearer {api_key}"
            # Safe beta: enables interleaved thinking on M2.7+ and M3. We do NOT
            # send fine-grained-tool-streaming (rejected by MiniMax) or
            # context-1m (not needed).
            headers["anthropic-beta"] = "interleaved-thinking-2025-05-14"
        elif self.provider != "anthropic":
            # Generic provider fallback (v3.3.43+).
            # Routes any provider from the Hermes catalog that doesn't
            # have an explicit branch above through the right transport:
            #   api_mode=anthropic_messages  → Bearer + /v1/messages path
            #   api_mode=chat_completions    → Bearer + /chat/completions path
            #   api_mode=openai_chat         → same as chat_completions
            #   api_mode=codex_responses     → same as chat_completions
            try:
                import cvc.providers.hermes_catalog  # noqa: F401  (side-effect import)
            except Exception:
                pass
            from cvc.providers.base import get_provider as _get_profile
            _prof = _get_profile(self.provider)
            if _prof is None:
                raise ValueError(
                    f"Unknown provider: {provider}. "
                    f"cvc supports these providers — run 'cvc setup' to see the full list: "
                    f"anthropic, openai, google, vertex, ollama, lmstudio, github, "
                    f"nvidia, minimax, and any OpenAI-compatible provider from the "
                    f"Hermes catalog (zai, kimi, stepfun, alibaba, opencode, kilo, "
                    f"huggingface, novita, xai, xiaomi, tencent, arcee, gmi, "
                    f"ollama-cloud, deepseek, azure-foundry, …)."
                )

            api_mode = _prof.api_mode

            if api_mode == "anthropic_messages":
                # Anthropic-Messages-API-compatible (e.g. minimax, minimax-cn)
                # Use the same scheme+host only strategy as the OpenAI-compat
                # branch so catalog base_urls like
                # https://api.minimaxi.com/anthropic/v1 resolve correctly.
                from urllib.parse import urlparse, urlunparse
                raw = (base_url or _prof.base_url or "").strip()
                if not raw:
                    raise ValueError(f"Provider '{provider}' has no base_url configured.")
                _p = urlparse(raw)
                scheme_host = urlunparse((_p.scheme, _p.netloc, "", "", "", ""))
                full_path = _p.path or ""
                if full_path and full_path != "/":
                    # Preserve the full base path. Append only the missing
                    # suffix. Handles all three catalog shapes:
                    #   "https://api.minimax.io"            → "https://api.minimax.io" + "/anthropic/v1/messages"
                    #   "https://api.minimax.io/anthropic"  → "https://api.minimax.io" + "/anthropic/v1/messages"
                    #   "https://api.minimaxi.com/anthropic/v1" → "https://api.minimaxi.com" + "/anthropic/v1/messages"
                    norm_path = full_path.rstrip("/")
                    if norm_path.endswith("/anthropic"):
                        self._api_url = scheme_host
                        self._api_messages_path = "/anthropic/v1/messages"
                    elif "/anthropic/" in norm_path or norm_path.endswith("/anthropic"):
                        # Path already includes /anthropic/<version>
                        self._api_url = scheme_host
                        self._api_messages_path = norm_path + "/messages"
                    else:
                        # Generic prefix (e.g. /api/v1) — append full Anthropic path
                        self._api_url = scheme_host
                        self._api_messages_path = norm_path + "/anthropic/v1/messages"
                else:
                    self._api_url = raw
                    self._api_messages_path = "/anthropic/v1/messages"
                headers["Authorization"] = f"Bearer {api_key}"
                headers["anthropic-beta"] = "interleaved-thinking-2025-05-14"
                logger.info(
                    "AgentLLM: routed provider=%s via Anthropic-Messages fallback "
                    "(base_url=%s, path=%s, model=%s)",
                    self.provider, self._api_url, self._api_messages_path, self.model,
                )

            elif api_mode in ("chat_completions", "openai_chat", "codex_responses"):
                # OpenAI Chat-Completions-compatible (zai, kimi, stepfun, alibaba,
                # opencode, kilo, huggingface, novita, xai, xiaomi, tencent,
                # arcee, gmi, ollama-cloud, deepseek, azure-foundry, …)
                raw_base = (base_url or _prof.base_url or "").strip().rstrip("/")
                if not raw_base:
                    raise ValueError(
                        f"Provider '{provider}' has no base_url configured. "
                        f"Either pass --api-base or set the base URL in cvc setup. "
                        f"Profile env vars: {_prof.env_vars}"
                    )
                # The catalog often gives us a base_url that already contains
                # a path prefix (e.g. https://api.z.ai/api/paas/v4 or
                # https://api.kimi.com/coding/v1). httpx's URL.join() strips
                # the last path segment when given an absolute path that
                # starts with /, so we MUST:
                #   1. Build _api_url as just scheme://host (no path).
                #   2. Carry the entire path (including /v\d+) in
                #      _api_messages_path.
                # Without this fix, zai would resolve to
                #   https://api.z.ai/v4/chat/completions  (missing /api/paas)
                # instead of the correct
                #   https://api.z.ai/api/paas/v4/chat/completions.
                import re as _re
                from urllib.parse import urlparse, urlunparse
                _parsed = urlparse(raw_base)
                scheme_host = urlunparse((_parsed.scheme, _parsed.netloc, "", "", "", ""))
                full_path = _parsed.path  # e.g. "/api/paas/v4" or "/v1" or ""
                if full_path and full_path != "/":
                    self._api_url = scheme_host
                    self._api_messages_path = full_path.rstrip("/") + "/chat/completions"
                else:
                    self._api_url = raw_base
                    self._api_messages_path = "/chat/completions"

                if _prof.auth_type == "bearer":
                    headers["Authorization"] = f"Bearer {api_key}"
                elif _prof.auth_type == "none":
                    pass  # local / no-auth (ollama)
                elif api_key:
                    headers["Authorization"] = f"Bearer {api_key}"

                logger.info(
                    "AgentLLM: routed provider=%s via OpenAI-compat fallback "
                    "(base_url=%s, path=%s, model=%s)",
                    self.provider, self._api_url, self._api_messages_path, self.model,
                )

            else:
                raise ValueError(
                    f"Unknown provider api_mode '{api_mode}' for provider '{provider}'. "
                    f"Run 'cvc setup' to switch to a supported provider."
                )

        # Use HTTP/2 for cloud providers (reduces latency via multiplexing)
        # Local providers (Ollama, LM Studio) stay on HTTP/1.1
        _use_http2 = _HTTP2_AVAILABLE and self.provider in (
            "anthropic", "openai", "google", "github", "vertex", "nvidia", "minimax",
            # Generic OpenAI-compat cloud providers from the Hermes catalog
            "zai", "kimi-for-coding", "stepfun", "alibaba", "alibaba-coding-plan",
            "opencode", "opencode-go", "kilo", "huggingface", "novita", "xai",
            "xiaomi", "tencent-tokenhub", "arcee", "gmi", "ollama-cloud",
            "deepseek", "minimax-cn", "openrouter",
        )

        # Gemini 3 Pro models can be slow due to thinking (even at LOW).
        # Gemini 3.1 Pro is particularly slow if the API defaults to HIGH
        # (Deep Think Mini → several minutes).  Use a short timeout for
        # 3.1 Pro so we can fail fast and auto-fall back to Flash.
        _is_31_pro = (
            self.provider == "google"
            and "gemini-3.1" in self.model
            and "pro" in self.model
            and "flash" not in self.model
        )
        _is_slow_model = (
            self.provider == "google"
            and "gemini-3-pro" in self.model
            and "gemini-3.1" not in self.model  # 3.0 Pro only
        )
        if _is_31_pro:
            _read_timeout = _READ_TIMEOUT_31_PRO
        elif _is_slow_model:
            _read_timeout = _READ_TIMEOUT_SLOW
        else:
            _read_timeout = _READ_TIMEOUT
        _timeout = httpx.Timeout(
            connect=_CONNECT_TIMEOUT,
            read=_read_timeout,
            write=_WRITE_TIMEOUT,
            pool=_POOL_TIMEOUT,
        )

        self._client = httpx.AsyncClient(
            base_url=self._api_url,
            headers=headers,
            timeout=_timeout,
            limits=_POOL_LIMITS,
            http2=_use_http2,
        )

        # Flag: has the TCP+TLS connection been warmed up?
        self._connection_warmed = False

        # Shared COGNOME memory runtime (attached later by the caller).
        # When set, every chat()/chat_stream() call routes through
        # runtime.resolve_messages() first so the LLM sees the workspace's
        # compiled Engram.  See cvc.operations.cognome_runtime.
        self._memory_runtime: Any | None = None

    def set_memory_runtime(self, runtime: Any | None) -> None:
        """
        Attach (or detach) the shared COGNOME runtime for this client.

        This is the single integration point used by the CLI agent, the
        proxy, the gateway, and sub-agents.  Once attached, memory
        injection is fully automatic — no per-call boilerplate.
        """
        self._memory_runtime = runtime

    async def _apply_memory(
        self, messages: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """
        Route *messages* through the COGNOME runtime if one is attached.

        Never raises — memory is an enhancement, never a blocker.  After
        the runtime injects an Engram we stamp :attr:`_last_engram_hash`
        so the Anthropic code path can target the Engram as a dedicated
        cache_control breakpoint.  All internal ``_cvc_*`` metadata keys
        are stripped before the HTTP request so they never leak to
        providers that reject unknown fields (e.g. OpenAI strict mode).
        """
        runtime = self._memory_runtime
        # Reset per-call engram state.
        self._last_engram_hash: str | None = None
        self._last_engram_text: str | None = None
        if runtime is None:
            return messages
        try:
            updated, engram = await runtime.resolve_messages(
                messages, provider=self.provider, model=self.model,
            )
            if engram is not None:
                self._last_engram_hash = engram.engram_hash
                self._last_engram_text = engram.preamble
            # Strip CVC-internal metadata keys before HTTP.
            if updated is messages:
                return messages
            cleaned: list[dict[str, Any]] = []
            for m in updated:
                if any(k.startswith("_cvc_") for k in m):
                    cleaned.append({k: v for k, v in m.items() if not k.startswith("_cvc_")})
                else:
                    cleaned.append(m)
            return cleaned
        except Exception as exc:  # pragma: no cover — defensive
            logger.warning("AgentLLM memory inject failed (non-fatal): %s", exc)
            return messages

    async def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
        temperature: float = 0.7,
        max_tokens: int = 8192,
        thinking_level: str = "",
    ) -> LLMResponse:
        """
        Send a chat request with tool definitions and return a unified response.

        Parameters
        ----------
        thinking_level : str
            Gemini 3 thinking level hint: "LOW" for fast conversational turns,
            "HIGH" for deep reasoning (tool iterations).  Ignored for non-Google
            providers and Gemini 2.5 (which uses thinkingBudget).
        """
        # Automatic COGNOME memory injection — single shared path for
        # CLI, proxy, gateway, and sub-agents.  No-op if no runtime
        # attached or memory is disabled.
        messages = await self._apply_memory(messages)
        import time as _time  # local to avoid module import overhead
        _start = _time.perf_counter()
        if self.provider == "anthropic":
            resp = await self._chat_anthropic(messages, tools, temperature, max_tokens)
        elif self.provider == "minimax":
            # MiniMax is Anthropic-Messages-API-compatible (https://api.minimax.io/anthropic)
            # NOT OpenAI-compat — use the Anthropic code path.
            resp = await self._chat_anthropic(messages, tools, temperature, max_tokens)
        elif self.provider == "openai":
            resp = await self._chat_openai(messages, tools, temperature, max_tokens)
        elif self.provider == "google":
            resp = await self._chat_google(messages, tools, temperature, max_tokens, thinking_level=thinking_level)
        elif self.provider == "ollama":
            resp = await self._chat_ollama(messages, tools, temperature, max_tokens)
        elif self.provider in ("lmstudio", "github", "vertex", "nvidia"):
            # OpenAI-compat with Bearer auth (already set in __init__)
            resp = await self._chat_openai(messages, tools, temperature, max_tokens)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
        # Observer hook: record the assistant turn with engram provenance.
        # Never raises, fire-and-forget.
        try:
            runtime = self._memory_runtime
            if runtime is not None:
                runtime.record_response_event(
                    resp.text or "",
                    engram_hash=getattr(self, "_last_engram_hash", None),
                    usage={
                        "input_tokens": resp.prompt_tokens,
                        "output_tokens": resp.completion_tokens,
                        "cache_read_tokens": resp.cache_read_tokens,
                    },
                    duration_ms=(_time.perf_counter() - _start) * 1000.0,
                )
        except Exception as exc:  # pragma: no cover — defensive
            logger.debug("observer record_response_event failed: %s", exc)
        return resp

    async def chat_stream(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
        temperature: float = 0.7,
        max_tokens: int = 8192,
        thinking_level: str = "",
        effort_level: str = "",
    ) -> AsyncIterator[StreamEvent]:
        """
        Stream a chat response token-by-token. Yields StreamEvent objects.
        Falls back to non-streaming for providers that don't support it well.

        Parameters
        ----------
        thinking_level : str
            Gemini 3 thinking level hint: "LOW" for fast conversational turns,
            "HIGH" for deep reasoning (tool iterations).  Ignored for non-Google
            providers and Gemini 2.5 (which uses thinkingBudget).
        effort_level : str
            Cross-provider effort/thinking level: "low", "medium", "high".
            Maps to thinking budgets for Anthropic, reasoning_effort for OpenAI,
            thinking level for Google.
        """
        # Automatic COGNOME memory injection — same path as non-streaming.
        messages = await self._apply_memory(messages)
        if self.provider == "anthropic":
            async for event in self._stream_anthropic(messages, tools, temperature, max_tokens, effort_level=effort_level):
                yield event
        elif self.provider == "minimax":
            # MiniMax is Anthropic-Messages-API-compatible — use the Anthropic stream.
            async for event in self._stream_anthropic(messages, tools, temperature, max_tokens, effort_level=effort_level):
                yield event
        elif self.provider == "openai":
            async for event in self._stream_openai(messages, tools, temperature, max_tokens, effort_level=effort_level):
                yield event
        elif self.provider == "google":
            # Use effort_level to override thinking_level if provided
            if effort_level:
                thinking_level = {"low": "LOW", "medium": "MEDIUM", "high": "HIGH"}.get(effort_level.lower(), thinking_level)
            async for event in self._stream_google(messages, tools, temperature, max_tokens, thinking_level=thinking_level):
                yield event
        elif self.provider == "ollama":
            async for event in self._stream_ollama(messages, tools, temperature, max_tokens):
                yield event
        elif self.provider in ("lmstudio", "github", "vertex", "nvidia"):
            # OpenAI-compat streaming
            async for event in self._stream_openai(messages, tools, temperature, max_tokens):
                yield event
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    async def warm_connection(self) -> None:
        """
        Pre-warm the TCP + TLS connection to the API provider.

        Call this ONCE during startup (while the user sees the banner)
        so the first real request skips the ~500ms-2s handshake.
        """
        if self._connection_warmed:
            return
        try:
            if self.provider == "anthropic":
                # Lightweight request — Anthropic returns 405 but connection is established
                await self._client.request("HEAD", "/v1/messages", timeout=5.0)
            elif self.provider == "minimax":
                # MiniMax is Anthropic-Messages-API-compatible at /anthropic/v1/messages
                await self._client.request("HEAD", self._api_messages_path, timeout=5.0)
            elif self.provider in ("openai", "github", "nvidia"):
                await self._client.request("HEAD", "/v1/chat/completions", timeout=5.0)
            elif self.provider == "vertex":
                await self._client.request("HEAD", "/chat/completions", timeout=5.0)
            elif self.provider == "google":
                # Just establish TCP+TLS to the API host
                await self._client.request("HEAD", "/", timeout=5.0)
            elif self.provider in ("ollama", "lmstudio"):
                # Local — check if server is alive
                await self._client.get("/", timeout=3.0)
        except Exception:
            # Connection warming is best-effort — never fail on this
            pass
        self._connection_warmed = True

    async def close(self) -> None:
        await self._client.aclose()

    # ── Anthropic helpers ───────────────────────────────────────────────

    @staticmethod
    def _anthropic_system_blocks(system_parts: list[str]) -> list[dict[str, Any]]:
        """
        Convert a list of system message strings into Anthropic's
        ``system`` block format, placing a ``cache_control`` marker on
        up to four segments.

        Anthropic supports up to 4 cache breakpoints.  We mark the last
        four blocks so the dev system prompt, the Engram, and any extra
        sub-agent scaffolding each get their own cache window.  This is
        the concrete payoff of Phase 2: the dev system prompt stays
        cached across topic shifts even when the Engram changes.
        """
        if not system_parts:
            return []
        blocks: list[dict[str, Any]] = [
            {"type": "text", "text": s} for s in system_parts if s
        ]
        if not blocks:
            return []
        # Anthropic's limit is 4 cache breakpoints per request.
        for blk in blocks[-4:]:
            blk["cache_control"] = {"type": "ephemeral"}
        return blocks

    # ── Anthropic ────────────────────────────────────────────────────────

    async def _chat_anthropic(
        self,
        messages: list[dict],
        tools: list[dict],
        temperature: float,
        max_tokens: int,
    ) -> LLMResponse:
        # Split system messages
        system_parts = []
        conv_messages = []
        for m in messages:
            if m["role"] == "system":
                system_parts.append(m["content"])
            else:
                conv_messages.append(self._to_anthropic_message(m))

        # Anthropic requires alternating user/assistant
        conv_messages = self._fix_anthropic_alternation(conv_messages)

        body: dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": conv_messages,
        }

        if system_parts:
            body["system"] = self._anthropic_system_blocks(system_parts)

        # Convert tools to Anthropic format
        if tools:
            anthropic_tools = []
            for t in tools:
                fn = t.get("function", t)
                anthropic_tools.append({
                    "name": fn.get("name", ""),
                    "description": fn.get("description", ""),
                    "input_schema": fn.get("parameters", fn.get("input_schema", {})),
                })
            body["tools"] = anthropic_tools

        resp = await self._chat_anthropic_post_with_retry(body)
        # v3.5.8 — translate anthropic-compat HTTP errors into user-facing
        # one-liners instead of raw JSON dumps. MiniMax returns the same
        # status codes and error body shape as Anthropic, so this covers
        # both native Anthropic and MiniMax / Kimi / DeepSeek endpoints.
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            friendly = _friendly_anthropic_error(exc, self.provider, self.model)
            if friendly is not None:
                raise RuntimeError(friendly) from exc
            raise
        data = resp.json()

        # Parse response
        text_parts = []
        tool_calls = []
        for block in data.get("content", []):
            if block.get("type") == "text":
                text_parts.append(block["text"])
            elif block.get("type") == "tool_use":
                tool_calls.append(ToolCall(
                    id=block["id"],
                    name=block["name"],
                    arguments=block.get("input", {}),
                ))

        usage = data.get("usage", {})
        return LLMResponse(
            text="\n".join(text_parts),
            tool_calls=tool_calls,
            finish_reason="tool_calls" if tool_calls else "stop",
            prompt_tokens=usage.get("input_tokens", 0),
            completion_tokens=usage.get("output_tokens", 0),
            cache_read_tokens=usage.get("cache_read_input_tokens", 0),
        )

    async def _chat_anthropic_post_with_retry(self, body: dict) -> httpx.Response:
        """POST to the anthropic-compat endpoint with transport-level retry.

        Retries only the connection / handshake layer (see _CONN_RETRYABLE_EXC).
        Does not retry on HTTP 4xx / 5xx (those go through existing higher-level
        paths). Handles Windows-specific cold-connect failures to
        api.minimax.io without duplicating a request once the server has
        already read the body.
        """
        last_exc: BaseException | None = None
        for attempt in range(_MAX_CONN_RETRIES + 1):
            try:
                resp = await self._client.post(self._api_messages_path, json=body)
                if attempt > 0:
                    logger.info(
                        "anthropic-compat POST succeeded on retry %d/%d "
                        "(provider=%s, model=%s)",
                        attempt, _MAX_CONN_RETRIES, self.provider, self.model,
                    )
                return resp
            except _CONN_RETRYABLE_EXC as exc:
                last_exc = exc
                if attempt >= _MAX_CONN_RETRIES:
                    break
                backoff = _TRANSIENT_RETRY_BASE_DELAY * (2 ** attempt)
                jitter = random.uniform(0, _JITTER_MAX)
                delay = backoff + jitter
                logger.warning(
                    "anthropic-compat POST transport error (provider=%s, "
                    "model=%s, attempt %d/%d): %s — retrying in %.2fs",
                    self.provider, self.model, attempt + 1,
                    _MAX_CONN_RETRIES + 1, type(exc).__name__, delay,
                )
                await asyncio.sleep(delay)
            except Exception:
                raise
        assert last_exc is not None
        raise ConnectionError(
            f"MiniMax/anthropic-compat POST failed after "
            f"{_MAX_CONN_RETRIES + 1} attempts (provider={self.provider}, "
            f"model={self.model}, url={self._api_url}{self._api_messages_path}). "
            f"Last error: {type(last_exc).__name__}: {last_exc}"
        ) from last_exc

    def _to_anthropic_message(self, msg: dict) -> dict:
        """Convert a message to Anthropic format."""
        role = msg["role"]
        if role == "system":
            role = "user"

        # Handle tool results
        if role == "tool":
            return {
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": msg.get("tool_call_id", ""),
                    "content": msg.get("content", ""),
                }],
            }

        # Handle assistant messages with tool calls
        if role == "assistant" and msg.get("tool_calls"):
            content = []
            if msg.get("content"):
                content.append({"type": "text", "text": msg["content"]})
            for tc in msg["tool_calls"]:
                fn = tc.get("function", {})
                args = fn.get("arguments", "{}")
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except json.JSONDecodeError:
                        args = {}
                content.append({
                    "type": "tool_use",
                    "id": tc.get("id", ""),
                    "name": fn.get("name", ""),
                    "input": args,
                })
            return {"role": "assistant", "content": content}

        # Handle multimodal content (list of parts — could include images,
        # tool_use blocks, or text blocks). Pass through tool_use blocks
        # verbatim so the request body keeps the tool_use ↔ tool_result
        # pairing the upstream API requires. v2.91.43: previously
        # tool_use blocks were silently dropped here, which broke the
        # conversation for providers that store assistant messages in
        # Anthropic content-block format (anthropic, minimax, kimi,
        # deepseek) — every turn after the first tool call would send
        # an assistant message with no tool_use but a tool_result with
        # a dangling tool_use_id, and the API returned empty.
        raw_content = msg.get("content", "")
        if isinstance(raw_content, list):
            blocks = []
            for item in raw_content:
                if not isinstance(item, dict):
                    continue
                item_type = item.get("type", "")
                if item_type == "text":
                    blocks.append({"type": "text", "text": item.get("text", "")})
                elif item_type == "image_url":
                    url = item.get("image_url", {}).get("url", "")
                    if url.startswith("data:"):
                        header, data = url.split(",", 1)
                        mime = header.split(":")[1].split(";")[0]
                        blocks.append({
                            "type": "image",
                            "source": {"type": "base64", "media_type": mime, "data": data},
                        })
                elif item_type == "image":
                    # Already Anthropic-style source block
                    blocks.append(item)
                elif item_type == "tool_use":
                    # v2.91.43: pass through Anthropic-style tool_use
                    # blocks unchanged. Required for the assistant →
                    # tool_result pairing to survive round-trips when
                    # the gateway stores assistant messages in
                    # Anthropic content-block format (the fix at
                    # gateway.py:6010 and gateway.py:7348).
                    blocks.append({
                        "type": "tool_use",
                        "id": item.get("id", ""),
                        "name": item.get("name", ""),
                        "input": item.get("input", {}),
                    })
            return {"role": role, "content": blocks}

        return {"role": role, "content": raw_content}

    @staticmethod
    def _fix_anthropic_alternation(messages: list[dict]) -> list[dict]:
        """
        Anthropic requires strict user/assistant alternation.
        Fix consecutive same-role messages by merging them.
        """
        if not messages:
            return messages

        fixed = [messages[0]]
        for msg in messages[1:]:
            if msg["role"] == fixed[-1]["role"]:
                # Merge content
                prev_content = fixed[-1].get("content", "")
                curr_content = msg.get("content", "")
                if isinstance(prev_content, str) and isinstance(curr_content, str):
                    fixed[-1]["content"] = prev_content + "\n" + curr_content
                elif isinstance(prev_content, list) and isinstance(curr_content, list):
                    fixed[-1]["content"] = prev_content + curr_content
                elif isinstance(prev_content, str) and isinstance(curr_content, list):
                    fixed[-1]["content"] = [{"type": "text", "text": prev_content}] + curr_content
                elif isinstance(prev_content, list) and isinstance(curr_content, str):
                    fixed[-1]["content"] = prev_content + [{"type": "text", "text": curr_content}]
            else:
                fixed.append(msg)

        return fixed

    @staticmethod
    def _fix_github_claude_messages(messages: list[dict]) -> list[dict]:
        """
        Sanitize message history for GitHub Copilot's Claude proxy.

        GitHub Copilot's /chat/completions endpoint is OpenAI-compatible.
        The proxy handles Anthropic translation internally, so messages MUST
        stay in OpenAI format:
          - role: "tool" with tool_call_id (NOT converted to user + tool_result)
          - assistant tool_calls as OpenAI tool_calls (NOT tool_use content blocks)
          - content arrays may only contain type: "text" or "image_url"

        This method:
        1. Ensures content arrays only have valid OpenAI types (text, image_url)
        2. Ensures every role="tool" message has a matching tool_call in the
           preceding assistant message (drops orphans to prevent 400 errors)
        3. Ensures content is never None (some providers reject null content)
        """
        if not messages:
            return messages

        logger.debug("GitHub Claude message fix: sanitizing %d messages", len(messages))

        sanitized: list[dict] = []

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content")

            # ── Sanitize content arrays ─────────────────────────────────────
            # OpenAI content arrays only support type "text" and "image_url".
            # Convert any other block types (tool_use, tool_result, etc.) to text.
            if isinstance(content, list):
                clean_blocks = []
                for block in content:
                    if not isinstance(block, dict):
                        # Plain string in array — wrap as text block
                        clean_blocks.append({"type": "text", "text": str(block)})
                    elif block.get("type") in ("text", "image_url"):
                        clean_blocks.append(block)
                    elif block.get("type") == "tool_use":
                        # Should not appear in OpenAI format — convert to text
                        clean_blocks.append({
                            "type": "text",
                            "text": f"[Tool call: {block.get('name', '?')}({json.dumps(block.get('input', {}))})]",
                        })
                    elif block.get("type") == "tool_result":
                        # Should not appear in OpenAI format — convert to text
                        clean_blocks.append({
                            "type": "text",
                            "text": f"[Tool output]: {block.get('content', '')}",
                        })
                    else:
                        # Unknown block type — convert to text
                        clean_blocks.append({
                            "type": "text",
                            "text": str(block.get("text", block.get("content", str(block)))),
                        })
                content = clean_blocks if clean_blocks else ""

            # Ensure content is never None
            if content is None:
                content = ""

            # ── Rebuild the message ─────────────────────────────────────────
            out: dict[str, Any] = {"role": role, "content": content}

            # Preserve OpenAI tool_calls on assistant messages
            if role == "assistant" and msg.get("tool_calls"):
                out["tool_calls"] = msg["tool_calls"]

            # Preserve tool_call_id on tool result messages
            if role == "tool" and msg.get("tool_call_id"):
                out["tool_call_id"] = msg["tool_call_id"]

            sanitized.append(out)

        # ── Validate tool result → tool_call matching ───────────────────────
        # Each role="tool" message's tool_call_id must exist in the preceding
        # assistant message's tool_calls. Orphaned tool results cause 400 errors.
        validated: list[dict] = []

        for msg in sanitized:
            if msg["role"] == "tool":
                tool_call_id = msg.get("tool_call_id", "")
                # Find the most recent assistant message with tool_calls
                prev_assistant = None
                for j in range(len(validated) - 1, -1, -1):
                    if validated[j].get("role") == "assistant" and validated[j].get("tool_calls"):
                        prev_assistant = validated[j]
                        break

                if prev_assistant:
                    valid_ids = {
                        tc.get("id", "")
                        for tc in prev_assistant.get("tool_calls", [])
                    }
                    if tool_call_id in valid_ids:
                        validated.append(msg)
                    else:
                        # Orphaned tool result — convert to user message
                        logger.warning(
                            "Orphaned tool result (id=%s) — converting to user message",
                            tool_call_id,
                        )
                        validated.append({
                            "role": "user",
                            "content": f"[Previous tool output]: {msg.get('content', '')}",
                        })
                else:
                    # No preceding assistant with tool_calls — convert to user message
                    logger.warning(
                        "Tool result without preceding tool_calls (id=%s) — converting",
                        msg.get("tool_call_id", ""),
                    )
                    validated.append({
                        "role": "user",
                        "content": f"[Previous tool output]: {msg.get('content', '')}",
                    })
            else:
                validated.append(msg)

        logger.debug(
            "GitHub Claude message fix: %d messages → %d validated",
            len(messages), len(validated),
        )
        return validated

    # ── Vertex AI token refresh ──────────────────────────────────────────

    def _refresh_vertex_token(self) -> None:
        """Refresh the Vertex AI OAuth2 token if expired (~1hr lifetime)."""
        creds = getattr(self, "_vertex_credentials", None)
        if creds is None:
            return
        if not creds.valid:
            from cvc.adapters.vertex import get_vertex_access_token
            token, self._vertex_credentials = get_vertex_access_token(creds)
            self._client.headers["Authorization"] = f"Bearer {token}"

    # ── OpenAI ───────────────────────────────────────────────────────────

    async def _ensure_github_token(self) -> None:
        """Ensure we have a valid Copilot session token.

        Strategy:
          1. If `_github_oauth_token` is set inline, use legacy fetch_copilot_token path.
          2. Otherwise, draw from the CredentialPool (multi-credential rotation).
          3. On 401/expiry mid-session, the pool rotates on the next call.
        """
        import time
        now = time.time()
        if getattr(self, "_github_token_expiry", 0) > now + 300:
            return  # still valid

        import asyncio
        import httpx

        # ─── Single canonical path: CredentialPool + vscode-chat spoof ───
        # (Legacy inline-OAuth branch removed — it shipped the wrong headers
        #  and landed requests in the Premium-Request bucket instead of the
        #  included IDE-chat bucket. All Copilot auth now flows through the
        #  upstream-equivalent path below.)
        from cvc.agent.credential_pool import (
            get_pool, PooledCredential, AUTH_TYPE_OAUTH,
        )
        from cvc.auth.copilot_auth import (
            exchange_copilot_token, copilot_request_headers, resolve_copilot_token,
        )
        import uuid as _uuid
        pool = get_pool()

        def _is_auth_failure(exc: BaseException) -> bool:
            msg = str(exc)
            return ("401" in msg) or ("403" in msg) or ("Unauthorized" in msg) or ("Forbidden" in msg)

        async def _bootstrap_inline() -> "PooledCredential | None":
            """Add inline OAuth token (from gc.api_keys.github / cvc copilot login) to pool if not already there."""
            inline = getattr(self, "_github_oauth_token", None)
            if not inline:
                return None
            existing = pool.list("copilot")
            for c in existing:
                if c.access_token == inline:
                    return c  # already in pool
            return pool.add(PooledCredential(
                provider="copilot",
                id=_uuid.uuid4().hex[:8],
                label="inline-config",
                auth_type=AUTH_TYPE_OAUTH,
                source="inline",
                access_token=inline,
            ))

        async def _bootstrap_resolver() -> "PooledCredential | None":
            token, source = await asyncio.to_thread(resolve_copilot_token)
            if not token:
                return None
            existing = pool.list("copilot")
            for c in existing:
                if c.access_token == token:
                    return c
            return pool.add(PooledCredential(
                provider="copilot",
                id=_uuid.uuid4().hex[:8],
                label=source,
                auth_type=AUTH_TYPE_OAUTH,
                source=source,
                access_token=token,
            ))

        # Make sure the inline token from config.json is in the pool BEFORE selection.
        # This is the fix for: stale pool entry shadowing a valid api_keys.github token.
        await _bootstrap_inline()

        last_exc: BaseException | None = None
        # Try up to N pool credentials, marking each one exhausted on auth failure.
        max_attempts = max(1, len(pool.list("copilot")) + 1)
        for _attempt in range(max_attempts):
            cred = pool.select("copilot")
            if cred is None:
                cred = await _bootstrap_inline() or await _bootstrap_resolver()
            if cred is None:
                from rich.console import Console
                import sys
                Console().print(
                    "[bold red]No Copilot credentials available.[/bold red] "
                    "Run [bold cyan]cvc copilot login[/bold cyan] or "
                    "set COPILOT_GITHUB_TOKEN."
                )
                sys.exit(1)
            try:
                api_token, expires_at, api_url = await asyncio.to_thread(
                    exchange_copilot_token, cred.access_token,
                )
            except Exception as exc:
                last_exc = exc
                if _is_auth_failure(exc):
                    # Stale/revoked pool token — evict it and rotate.
                    code = 403 if "403" in str(exc) or "Forbidden" in str(exc) else 401
                    pool.mark_exhausted(cred, code, str(exc))
                    continue
                # Non-auth failure — don't burn other creds, surface immediately.
                break
            # Success.
            self._copilot_active_credential_id = cred.id
            self._api_url = api_url or "https://api.individual.githubcopilot.com"
            self._client.base_url = httpx.URL(self._api_url)
            self._client.headers.update({
                "Authorization": f"Bearer {api_token}",
                **copilot_request_headers(is_agent_turn=True),
            })
            self._github_token_expiry = expires_at
            pool.mark_used(cred)
            return

        # All attempts failed.
        from rich.console import Console
        import sys
        Console().print(
            f"[bold red]Copilot authentication failed:[/bold red] {last_exc}\n"
            "Run [bold cyan]cvc copilot login[/bold cyan] to re-authenticate."
        )
        sys.exit(1)

    async def _chat_openai(
        self,
        messages: list[dict],
        tools: list[dict],
        temperature: float,
        max_tokens: int,
    ) -> LLMResponse:
        if self.provider == "vertex":
            self._refresh_vertex_token()
        if self.provider == "github":
            await self._ensure_github_token()
            if "claude" in self.model.lower():
                messages = self._fix_github_claude_messages(messages)

        body: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        # Vertex AI OpenAI-compat endpoint requires "google/" prefix for Gemini models
        if self.provider == "vertex" and not self.model.startswith(("google/", "meta/", "mistral")):
            body["model"] = f"google/{self.model}"

        if "o1" in self.model.lower():
            body.pop("temperature", None)
            if "max_tokens" in body:
                body["max_completion_tokens"] = body.pop("max_tokens")

        if self.provider == "github" and "claude" in self.model.lower():
            if "max_tokens" in body and body["max_tokens"] > 4096:
                body["max_tokens"] = 4096

        if tools:
            body["tools"] = tools
            body["tool_choice"] = "auto"

        path = "/chat/completions" if self.provider in ("github", "vertex") else "/v1/chat/completions"
        resp = await self._client.post(path, json=body)
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code in _TRANSIENT_STATUS_CODES:
                ra = (
                    e.response.headers.get("retry-after")
                    or e.response.headers.get("Retry-After")
                )
                hint = f" (retry after {ra}s)" if ra else ""
                raise RetriesExhaustedError(
                    f"Rate-limited ({e.response.status_code}){hint}. "
                    f"Wait a moment and try again."
                )
            if e.response.status_code == 400 and self.provider == "github":
                try:
                    err_data = e.response.json()
                    err_code = err_data.get("error", {}).get("code")
                    if err_code == "model_not_supported":
                        raise RuntimeError("Your GitHub Copilot tier does not have access to this model. Please upgrade your plan or use /model to select an available one.")
                    elif err_code == "unsupported_api_for_model":
                        raise RuntimeError("This model does not support chat completions via the Copilot API.")
                    else:
                        raise RuntimeError(f"GitHub Copilot API 400 Bad Request: {e.response.text}")
                except json.JSONDecodeError:
                    raise RuntimeError(f"GitHub Copilot API 400 Bad Request: {e.response.text}")
            raise
        data = resp.json()

        choice = data.get("choices", [{}])[0]
        msg = choice.get("message", {})

        tool_calls = []
        for tc in msg.get("tool_calls", []):
            fn = tc.get("function", {})
            args_str = fn.get("arguments", "{}")
            try:
                args = json.loads(args_str)
            except json.JSONDecodeError:
                args = {"raw": args_str}
            tool_calls.append(ToolCall(
                id=tc.get("id", ""),
                name=fn.get("name", ""),
                arguments=args,
            ))

        usage = data.get("usage", {})
        return LLMResponse(
            text=msg.get("content", "") or "",
            tool_calls=tool_calls,
            finish_reason=choice.get("finish_reason", "stop"),
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            cache_read_tokens=usage.get("prompt_tokens_details", {}).get("cached_tokens", 0),
        )

    # ── Google Gemini ────────────────────────────────────────────────────

    def _build_gemini_body(
        self,
        messages: list[dict],
        tools: list[dict],
        temperature: float,
        max_tokens: int,
        thinking_level: str = "",
    ) -> dict[str, Any]:
        """Build the Gemini request body from messages and tools."""
        # Gemini 3 models require temperature=1.0 to avoid looping/degraded output
        if "gemini-3" in self.model:
            temperature = 1.0

        # Convert messages to Gemini format
        gemini_contents = []
        system_text = ""

        for m in messages:
            if m["role"] == "system":
                system_text += m.get("content", "") + "\n"
                continue

            role = "user" if m["role"] in ("user", "tool") else "model"
            parts = []

            if m["role"] == "tool":
                # Function response
                parts.append({
                    "functionResponse": {
                        "name": m.get("name", "tool"),
                        "response": {"result": m.get("content", "")},
                    }
                })
            elif m.get("tool_calls"):
                # Use raw Gemini parts if available — preserves thoughtSignature
                # for Gemini 3 models (mandatory for function calling).
                raw_parts = m.get("_gemini_parts")
                if raw_parts:
                    parts = list(raw_parts)  # use stored parts as-is
                else:
                    # Fallback: reconstruct from tool_calls (non-Gemini history)
                    for tc in m["tool_calls"]:
                        fn = tc.get("function", {})
                        args = fn.get("arguments", "{}")
                        if isinstance(args, str):
                            try:
                                args = json.loads(args)
                            except json.JSONDecodeError:
                                args = {}
                        parts.append({
                            "functionCall": {
                                "name": fn.get("name", ""),
                                "args": args,
                            }
                        })
                    if m.get("content"):
                        parts.insert(0, {"text": m["content"]})
            else:
                content = m.get("content", "")
                # Handle multimodal content (list of parts with images)
                if isinstance(content, list):
                    for item in content:
                        item_type = item.get("type", "")
                        if item_type == "text":
                            parts.append({"text": item.get("text", "")})
                        elif item_type == "image":
                            source = item.get("source", {})
                            parts.append({
                                "inlineData": {
                                    "mimeType": source.get("media_type", "image/png"),
                                    "data": source.get("data", ""),
                                }
                            })
                        elif item_type == "image_url":
                            # OpenAI-style data URL
                            url = item.get("image_url", {}).get("url", "")
                            if url.startswith("data:"):
                                # Parse data:mime;base64,DATA
                                header, data = url.split(",", 1)
                                mime = header.split(":")[1].split(";")[0]
                                parts.append({
                                    "inlineData": {
                                        "mimeType": mime,
                                        "data": data,
                                    }
                                })
                else:
                    parts.append({"text": content})

            gemini_contents.append({"role": role, "parts": parts})

        # Merge consecutive same-role contents (e.g. multiple tool results)
        # Gemini requires strict user/model alternation.
        gemini_contents = self._merge_gemini_contents(gemini_contents)

        # Convert tools to Gemini format
        gemini_tools = []
        if tools:
            declarations = []
            for t in tools:
                fn = t.get("function", t)
                declarations.append({
                    "name": fn.get("name", ""),
                    "description": fn.get("description", ""),
                    "parameters": fn.get("parameters", {}),
                })
            gemini_tools = [{"functionDeclarations": declarations}]

        gen_config: dict[str, Any] = {
            "temperature": temperature,
            "maxOutputTokens": max_tokens,
        }

        # ── Gemini Thinking Configuration ─────────────────────────────────
        # Gemini 3 models default to HIGH dynamic thinking when no
        # thinkingConfig is sent → 30-100s latency on Pro.
        #
        # Supported levels by model:
        #   gemini-3-pro-preview (3.0):  LOW, HIGH only (MEDIUM = 400 error!)
        #   gemini-3.1-pro-preview (3.1): LOW, MEDIUM, HIGH
        #   gemini-3-flash-preview:       MINIMAL, LOW, MEDIUM, HIGH
        #
        # Strategy:
        #   • --no-think     → MINIMAL (Flash) / LOW (Pro)
        #   • Caller level   → use exactly that (chat.py controls routing)
        #   • No level given → LOW (Pro safe default), MEDIUM (Flash)
        #
        # Gemini 2.5 uses thinkingBudget (integer tokens) — legacy.
        #
        # Thinking Level Support Matrix (confirmed from Google docs):
        #   gemini-3-pro-preview (3.0):   LOW, HIGH (default=HIGH)
        #   gemini-3.1-pro-preview (3.1): LOW, MEDIUM, HIGH (default=HIGH=Deep Think Mini!)
        #   gemini-3-flash-preview:        MINIMAL, LOW, MEDIUM, HIGH (default=HIGH)
        #
        # WARNING: HIGH is the default if no thinkingConfig is sent!
        # HIGH on 3.1 Pro = Deep Think Mini → several minutes latency.
        # Always send an explicit thinkingLevel to avoid slow defaults.
        _is_gemini3 = "gemini-3" in self.model
        _is_flash = "flash" in self.model

        if _is_gemini3:
            if self.no_think:
                # --no-think: force minimum thinking
                level = "MINIMAL" if _is_flash else "LOW"
                gen_config["thinkingConfig"] = {"thinkingLevel": level}
            elif thinking_level:
                # Explicit level from caller — chat.py controls routing.
                gen_config["thinkingConfig"] = {
                    "thinkingLevel": thinking_level.upper(),
                }
            else:
                # No explicit level — safe speed-first defaults.
                # Pro: LOW (fast, avoids HIGH=Deep Think Mini)
                # Flash: MEDIUM (Flash is fast enough for MEDIUM)
                _default = "MEDIUM" if _is_flash else "LOW"
                gen_config["thinkingConfig"] = {"thinkingLevel": _default}
        elif "2.5" in self.model:
            # Gemini 2.5: use thinkingBudget (legacy, still works well)
            if self.no_think:
                gen_config["thinkingConfig"] = {"thinkingBudget": 0}
            else:
                gen_config["thinkingConfig"] = {
                    "thinkingBudget": min(max_tokens * 2, 16384),
                }

        body: dict[str, Any] = {
            "contents": gemini_contents,
            "generationConfig": gen_config,
        }

        if system_text.strip():
            body["systemInstruction"] = {"parts": [{"text": system_text.strip()}]}

        if gemini_tools:
            body["tools"] = gemini_tools

        # Debug: log the exact thinking config being sent to the API
        _tc = gen_config.get("thinkingConfig")
        if _tc:
            logger.debug(
                "Gemini thinkingConfig for %s: %s",
                self.model, _tc,
            )

        return body

    async def _chat_google(
        self,
        messages: list[dict],
        tools: list[dict],
        temperature: float,
        max_tokens: int,
        thinking_level: str = "",
    ) -> LLMResponse:
        body = self._build_gemini_body(messages, tools, temperature, max_tokens, thinking_level=thinking_level)

        url = f"/v1beta/models/{self.model}:generateContent?key={self.api_key}"

        # Retry loop for transient server errors (503, 429, 500, 502)
        last_exc: Exception | None = None
        _last_status = 0
        for attempt in range(_MAX_TRANSIENT_RETRIES + 1):
            resp = await self._client.post(url, json=body)

            if resp.status_code in _TRANSIENT_STATUS_CODES:
                _last_status = resp.status_code
                # Honour Retry-After header when present
                retry_after = resp.headers.get("retry-after") or resp.headers.get("Retry-After")
                if retry_after:
                    try:
                        delay = float(retry_after) + random.uniform(0, _JITTER_MAX)
                    except (ValueError, TypeError):
                        delay = _TRANSIENT_RETRY_BASE_DELAY * (2 ** attempt) + random.uniform(0, _JITTER_MAX)
                else:
                    delay = _TRANSIENT_RETRY_BASE_DELAY * (2 ** attempt) + random.uniform(0, _JITTER_MAX)
                logger.debug(
                    "Gemini %d (attempt %d/%d) — retrying in %.1fs…",
                    resp.status_code, attempt + 1, _MAX_TRANSIENT_RETRIES + 1, delay,
                )
                last_exc = RetriesExhaustedError(
                    f"Gemini {resp.status_code} for model '{self.model}' "
                    f"(tried {_MAX_TRANSIENT_RETRIES + 1} times). "
                    f"The model may be temporarily overloaded or in preview with limited capacity."
                )
                await asyncio.sleep(delay)
                continue
            break  # non-transient status — stop retrying
        else:
            # All retries exhausted — raise as RetriesExhaustedError so
            # the outer agent loop knows not to re-retry.
            raise last_exc  # type: ignore[misc]

        if resp.status_code == 403:
            _is_preview = "gemini-3" in self.model and "preview" in self.model
            if _is_preview:
                raise RuntimeError(
                    f"Access denied (403) to '{self.model}'.\n"
                    f"gemini-3-pro-preview requires Google allowlist access — "
                    f"not available to standard Gemini API keys.\n\n"
                    f"Switch to a GA model: cvc agent --model gemini-3-flash-preview"
                )
            raise RuntimeError(
                f"API key rejected (403) for model '{self.model}'.\n"
                f"Your Google API key is invalid, expired, or was auto-revoked "
                f"(Google revokes keys that appear in logs or public output).\n\n"
                f"Fix: Generate a new key at → https://aistudio.google.com/app/apikey\n"
                f"Then run: cvc setup"
            )

        if resp.status_code == 404:
            raise RuntimeError(
                f"Model '{self.model}' not found (404). "
                f"Valid Google models include: gemini-2.5-flash, gemini-2.5-pro, "
                f"gemini-2.0-flash, gemini-1.5-flash, gemini-1.5-pro, "
                f"gemini-3-flash-preview, gemini-3.1-pro-preview. "
                f"Run 'cvc setup' to reconfigure or use --model to override."
            )

        if resp.status_code == 400:
            error_body = resp.text
            logger.error("Gemini 400 Bad Request: %s", error_body[:1000])
            raise RuntimeError(
                f"Gemini returned 400 Bad Request for model '{self.model}'.\n"
                f"Response: {error_body[:500]}\n\n"
                f"If using a Gemini 3 model, ensure thought signatures are "
                f"being preserved. Try 'gemini-3-flash-preview' as an alternative."
            )

        resp.raise_for_status()
        data = resp.json()

        # Parse Gemini response
        candidates = data.get("candidates", [])
        if not candidates:
            return LLMResponse(text="(no response from Gemini)")

        # Store the raw response parts — these contain thoughtSignature
        # fields that must be passed back for Gemini 3 function calling.
        raw_response_parts = candidates[0].get("content", {}).get("parts", [])

        text_parts = []
        tool_calls = []

        for i, part in enumerate(raw_response_parts):
            # Skip thinking parts — they're internal reasoning, not user output
            if part.get("thought") and "text" in part:
                continue
            if "text" in part:
                text_parts.append(part["text"])
            elif "functionCall" in part:
                fc = part["functionCall"]
                tool_calls.append(ToolCall(
                    id=f"call_{i}",
                    name=fc.get("name", ""),
                    arguments=fc.get("args", {}),
                ))

        usage = data.get("usageMetadata", {})
        return LLMResponse(
            text="\n".join(text_parts),
            tool_calls=tool_calls,
            finish_reason="tool_calls" if tool_calls else "stop",
            prompt_tokens=usage.get("promptTokenCount", 0),
            completion_tokens=usage.get("candidatesTokenCount", 0),
            _provider_meta={"gemini_parts": raw_response_parts},
        )

    async def _stream_google(
        self,
        messages: list[dict],
        tools: list[dict],
        temperature: float,
        max_tokens: int,
        thinking_level: str = "",
    ) -> AsyncIterator[StreamEvent]:
        """Stream from Google Gemini API using SSE (streamGenerateContent).

        Auto-retries with a safe fallback thinking config if the model rejects
        the initial thinking configuration.

        Also retries up to 2 times on transient server errors (503, 429, 500, 502).
        """
        body = self._build_gemini_body(messages, tools, temperature, max_tokens, thinking_level=thinking_level)

        url = f"/v1beta/models/{self.model}:streamGenerateContent?key={self.api_key}&alt=sse"

        # ── Auto-fallback detection ───────────────────────────────────
        # If a Pro model times out or gets persistent 429s, fall back to
        # Flash so the user isn't stuck.
        _is_pro = (
            ("pro" in self.model and "flash" not in self.model)
            and ("gemini" in self.model)
        )
        _fell_back = False  # True once we switch to Flash

        # Retry loop for transient server errors (503/429/500/502) + timeout
        last_exc: Exception | None = None
        for attempt in range(_MAX_TRANSIENT_RETRIES):
            _yielded_content = False  # Track if any content was streamed
            try:
                async for event in self._stream_google_body(body, url, messages, tools, temperature, max_tokens):
                    if event.type in ("text_delta", "tool_call_start"):
                        _yielded_content = True
                    yield event
                return  # success — exit
            except httpx.TimeoutException as exc:
                # ── Pro model timeout → auto-fallback to Flash ────────
                if _is_pro and not _yielded_content and not _fell_back:
                    logger.warning(
                        "%s timed out — falling back to gemini-3-flash-preview",
                        self.model,
                    )
                    yield StreamEvent(
                        type="text_delta",
                        text=(
                            f"\n> ⚡ *{self.model} timed out. "
                            "Switching to Flash for speed…*\n\n"
                        ),
                    )
                    url = (
                        f"/v1beta/models/gemini-3-flash-preview"
                        f":streamGenerateContent?key={self.api_key}&alt=sse"
                    )
                    body = dict(body)
                    gc = dict(body.get("generationConfig", {}))
                    gc["thinkingConfig"] = {"thinkingLevel": "MEDIUM"}
                    body["generationConfig"] = gc
                    _fell_back = True
                    continue  # retry with Flash
                raise RuntimeError(
                    f"Gemini timed out for model '{self.model}'. "
                    f"Try: cvc agent --model gemini-3-flash-preview"
                ) from exc
            except RuntimeError as exc:
                err_lower = str(exc).lower()
                _is_transient = any(code in err_lower for code in ("503", "502", "429", "500", "overloaded", "unavailable", "capacity"))
                _is_429 = "429" in err_lower or "rate" in err_lower or "capacity" in err_lower

                # ── 429 on Pro → auto-fallback to Flash ───────────────
                if _is_429 and _is_pro and not _fell_back:
                    logger.warning(
                        "%s rate-limited (429) — falling back to gemini-3-flash-preview",
                        self.model,
                    )
                    yield StreamEvent(
                        type="text_delta",
                        text=(
                            f"\n> ⚡ *{self.model} rate-limited. "
                            "Switching to Flash…*\n\n"
                        ),
                    )
                    url = (
                        f"/v1beta/models/gemini-3-flash-preview"
                        f":streamGenerateContent?key={self.api_key}&alt=sse"
                    )
                    body = dict(body)
                    gc = dict(body.get("generationConfig", {}))
                    gc["thinkingConfig"] = {"thinkingLevel": "MEDIUM"}
                    body["generationConfig"] = gc
                    _fell_back = True
                    continue  # retry with Flash

                if _is_transient and attempt < _MAX_TRANSIENT_RETRIES - 1:
                    delay = _TRANSIENT_RETRY_BASE_DELAY * (2 ** attempt) + random.uniform(0, _JITTER_MAX)
                    logger.debug(
                        "Gemini streaming transient error (attempt %d/%d) — retrying in %.1fs…",
                        attempt + 1, _MAX_TRANSIENT_RETRIES, delay,
                    )
                    last_exc = exc
                    await asyncio.sleep(delay)
                    continue
                raise  # non-transient or last attempt — propagate
            except httpx.HTTPStatusError as exc:
                _status = exc.response.status_code

                # ── 429 on Pro → auto-fallback to Flash ───────────────
                if _status == 429 and _is_pro and not _fell_back:
                    logger.warning(
                        "%s HTTP 429 — falling back to gemini-3-flash-preview",
                        self.model,
                    )
                    yield StreamEvent(
                        type="text_delta",
                        text=(
                            f"\n> ⚡ *{self.model} rate-limited. "
                            "Switching to Flash…*\n\n"
                        ),
                    )
                    url = (
                        f"/v1beta/models/gemini-3-flash-preview"
                        f":streamGenerateContent?key={self.api_key}&alt=sse"
                    )
                    body = dict(body)
                    gc = dict(body.get("generationConfig", {}))
                    gc["thinkingConfig"] = {"thinkingLevel": "MEDIUM"}
                    body["generationConfig"] = gc
                    _fell_back = True
                    continue  # retry with Flash

                if _status in _TRANSIENT_STATUS_CODES and attempt < _MAX_TRANSIENT_RETRIES - 1:
                    delay = _TRANSIENT_RETRY_BASE_DELAY * (2 ** attempt) + random.uniform(0, _JITTER_MAX)
                    logger.debug(
                        "Gemini streaming HTTP %d (attempt %d/%d) — retrying in %.1fs…",
                        _status, attempt + 1, _MAX_TRANSIENT_RETRIES, delay,
                    )
                    last_exc = exc
                    await asyncio.sleep(delay)
                    continue
                raise RuntimeError(
                    f"Gemini streaming error ({_status}) for model '{self.model}'. "
                    f"Try: cvc agent --model gemini-3-flash-preview"
                ) from exc

    async def _stream_google_body(
        self,
        body: dict,
        url: str,
        messages: list[dict],
        tools: list[dict],
        temperature: float,
        max_tokens: int,
        _retry_fallback: bool = False,
    ) -> AsyncIterator[StreamEvent]:
        """Inner streaming implementation with automatic thinking-budget fallback."""
        tool_calls: list[ToolCall] = []
        all_raw_parts: list[dict] = []  # accumulate raw parts for thoughtSignature
        prompt_tokens = 0
        completion_tokens = 0
        finish_reason = ""  # Track why Gemini stopped
        has_any_content = False

        try:
            async with self._client.stream("POST", url, json=body) as resp:
                # ── Transient server errors (503, 429, 500, 502) ──────────
                if resp.status_code in _TRANSIENT_STATUS_CODES and not _retry_fallback:
                    # Honour Retry-After header when present
                    retry_after = resp.headers.get("retry-after") or resp.headers.get("Retry-After")
                    if retry_after:
                        try:
                            delay = float(retry_after) + random.uniform(0, _JITTER_MAX)
                        except (ValueError, TypeError):
                            delay = _TRANSIENT_RETRY_BASE_DELAY * 2 + random.uniform(0, _JITTER_MAX)
                    else:
                        delay = _TRANSIENT_RETRY_BASE_DELAY * 2 + random.uniform(0, _JITTER_MAX)
                    logger.debug(
                        "Gemini streaming %d — retrying in %.1fs…",
                        resp.status_code, delay,
                    )
                    await asyncio.sleep(delay)
                    # Retry once via recursive call (with _retry_fallback to prevent infinite loop)
                    async for event in self._stream_google_body(
                        body, url, messages, tools, temperature, max_tokens,
                        _retry_fallback=True,
                    ):
                        yield event
                    return
                elif resp.status_code in _TRANSIENT_STATUS_CODES:
                    raise RetriesExhaustedError(
                        f"Gemini {resp.status_code} for model '{self.model}' after retry. "
                        f"The model may be temporarily overloaded or in preview with limited capacity."
                    )

                if resp.status_code == 403:
                    _is_preview = "gemini-3" in self.model and "preview" in self.model
                    if _is_preview:
                        raise RuntimeError(
                            f"Access denied (403) to '{self.model}'.\n"
                            f"gemini-3-pro-preview requires Google allowlist access — "
                            f"not available to standard Gemini API keys.\n\n"
                            f"Switch to a GA model: cvc agent --model gemini-3-flash-preview"
                        )
                    raise RuntimeError(
                        f"API key rejected (403) for model '{self.model}'.\n"
                        f"Your Google API key is invalid, expired, or was auto-revoked "
                        f"(Google revokes keys that appear in logs or public output).\n\n"
                        f"Fix: Generate a new key at → https://aistudio.google.com/app/apikey\n"
                        f"Then run: cvc setup"
                    )

                if resp.status_code == 404:
                    raise RuntimeError(
                        f"Model '{self.model}' not found (404). "
                        f"Valid Google models: gemini-2.5-flash, gemini-2.5-pro, "
                        f"gemini-2.0-flash, gemini-1.5-flash, gemini-1.5-pro, "
                        f"gemini-3-flash-preview, gemini-3.1-pro-preview.\n"
                        f"Run [bold]cvc setup[/bold] or use [bold]--model gemini-2.5-flash[/bold] to override."
                    )
                if resp.status_code == 400:
                    # Read the body for error details
                    body_bytes = b""
                    async for chunk in resp.aiter_bytes():
                        body_bytes += chunk
                    error_body = body_bytes.decode("utf-8", errors="replace")
                    logger.error("Gemini 400 Bad Request: %s", error_body[:1000])

                    # Auto-retry: if error is about thinking config and we
                    # haven't retried yet, switch to the other param style.
                    is_thinking_error = (
                        "thinkingBudget" in error_body
                        or "thinkingConfig" in error_body
                        or "thinking_budget" in error_body.lower()
                        or "thinking_level" in error_body.lower()
                        or "thinking level" in error_body.lower()
                        or "thinking mode" in error_body.lower()
                        or "thinkingLevel" in error_body
                        or "Budget" in error_body
                    )
                    if is_thinking_error and not _retry_fallback:
                        # Fallback: use the correct param style per model family.
                        # Gemini 3 → fallback to LOW (safest, all models support it)
                        # Gemini 2.5 → use thinkingBudget (legacy)
                        if "gemini-3" in self.model:
                            # Fallback: force LOW thinking (universally supported)
                            logger.info(
                                "thinkingConfig rejected — retrying with LOW (safe fallback)"
                            )
                            fallback_thinking = {"thinkingLevel": "LOW"}
                        else:
                            logger.info(
                                "thinkingBudget rejected — retrying with thinkingBudget=1024"
                            )
                            fallback_thinking = {"thinkingBudget": 1024}

                        fallback_body = dict(body)
                        gc = dict(fallback_body.get("generationConfig", {}))
                        if fallback_thinking is None:
                            gc.pop("thinkingConfig", None)  # remove entirely
                        else:
                            gc["thinkingConfig"] = fallback_thinking
                        fallback_body["generationConfig"] = gc
                        async for event in self._stream_google_body(
                            fallback_body, url, messages, tools, temperature, max_tokens,
                            _retry_fallback=True,
                        ):
                            yield event
                        return

                    raise RuntimeError(
                        f"Gemini 400 Bad Request for model '{self.model}'.\n"
                        f"{error_body[:400]}\n\n"
                        f"Try: [bold]cvc agent --model gemini-3-flash-preview[/bold]"
                    )
                resp.raise_for_status()

                async for line in resp.aiter_lines():
                    if not line.startswith("data: "):
                        continue
                    data_str = line[6:]
                    if data_str.strip() == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data_str)
                    except json.JSONDecodeError:
                        continue

                    # Check for API-level errors in the chunk
                    if "error" in chunk:
                        err = chunk["error"]
                        err_msg = err.get("message", str(err))[:300]
                        logger.error("Gemini API error in stream: %s", err_msg)
                        raise RuntimeError(f"Gemini API error: {err_msg}")

                    # Extract candidates
                    candidates = chunk.get("candidates", [])
                    if candidates:
                        candidate = candidates[0]

                        # Capture finishReason (only the last one matters)
                        fr = candidate.get("finishReason", "")
                        if fr:
                            finish_reason = fr

                        parts = candidate.get("content", {}).get("parts", [])
                        # Accumulate raw parts (preserves thoughtSignature for Gemini 3)
                        all_raw_parts.extend(parts)
                        for i, part in enumerate(parts):
                            # Skip thought-only parts (no user-visible text)
                            if part.get("thought") and "text" in part:
                                # Thinking part — don't yield as text_delta
                                # but DO keep in all_raw_parts for context
                                continue
                            if "text" in part:
                                has_any_content = True
                                yield StreamEvent(type="text_delta", text=part["text"])
                            elif "functionCall" in part:
                                has_any_content = True
                                fc = part["functionCall"]
                                tc = ToolCall(
                                    id=f"call_{len(tool_calls)}",
                                    name=fc.get("name", ""),
                                    arguments=fc.get("args", {}),
                                )
                                tool_calls.append(tc)
                                yield StreamEvent(type="tool_call_start", tool_call=tc)

                    # Extract usage metadata
                    usage = chunk.get("usageMetadata", {})
                    if usage:
                        prompt_tokens = usage.get("promptTokenCount", prompt_tokens)
                        completion_tokens = usage.get("candidatesTokenCount", completion_tokens)

        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            if status in _TRANSIENT_STATUS_CODES:
                raise RuntimeError(
                    f"Gemini {status} for model '{self.model}'. "
                    f"The model may be temporarily overloaded or in preview with limited capacity."
                ) from e
            raise RuntimeError(f"Gemini streaming error ({status}): {e}") from e

        # Detect blocked / empty responses and raise actionable errors
        if not has_any_content and finish_reason:
            _BLOCKED_REASONS = {"SAFETY", "RECITATION", "BLOCKLIST", "PROHIBITED_CONTENT"}
            if finish_reason in _BLOCKED_REASONS:
                raise RuntimeError(
                    f"Gemini blocked the response (reason: {finish_reason}). "
                    f"This usually happens with very large tool outputs. "
                    f"Try a shorter query or use a different model."
                )
            elif finish_reason == "MAX_TOKENS":
                logger.warning("Gemini hit MAX_TOKENS with 0 visible output — "
                               "thinking may have consumed the entire budget.")
                # Don't raise — let the retry logic in the agentic loop handle it
            elif finish_reason not in ("STOP", ""):
                logger.warning("Gemini finished with reason '%s' and 0 content", finish_reason)

        yield StreamEvent(
            type="done",
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            _provider_meta={
                "gemini_parts": all_raw_parts if all_raw_parts else [],
                "finish_reason": finish_reason,
            },
        )

    @staticmethod
    def _merge_gemini_contents(contents: list[dict]) -> list[dict]:
        """Merge consecutive same-role Gemini content blocks.

        Gemini requires strict user/model alternation.  Multiple tool
        results (role=user) must be merged into a single Content with
        multiple functionResponse parts.
        """
        if not contents:
            return contents
        merged = [contents[0]]
        for content in contents[1:]:
            if content["role"] == merged[-1]["role"]:
                merged[-1]["parts"].extend(content["parts"])
            else:
                merged.append(content)
        return merged

    # ── Ollama (native /api/chat endpoint) ──────────────────────────────
    #
    # IMPORTANT: We use Ollama's NATIVE /api/chat endpoint, NOT the
    # OpenAI-compat /v1/chat/completions endpoint. The compat layer has a
    # known bug (ollama#12557) where it silently drops tool_calls when
    # stream=true. The native API has fully supported streaming + tool
    # calling since May 2025 (ollama#10415).
    #
    # Critical fix: num_ctx MUST be set. Ollama defaults to 4096 tokens
    # which truncates the system prompt + all 17 tool schemas, causing the
    # model to never see the tool definitions and silently produce text
    # instead of tool calls.

    _OLLAMA_NUM_CTX = 32768  # Safe default: covers system prompt + all tools

    @staticmethod
    def _to_ollama_messages(messages: list[dict]) -> list[dict]:
        """
        Convert OpenAI-format messages to Ollama's /api/chat format.

        Ollama multimodal (llava, llama3.2-vision, etc.) requires images as a
        separate ``images`` list of base64 strings on the message dict, NOT
        embedded inside a content list.  Plain text messages are passed through
        unchanged.
        """
        result = []
        for m in messages:
            content = m.get("content", "")
            if isinstance(content, list):
                # Multimodal: extract text and images separately
                text_parts: list[str] = []
                images: list[str] = []
                for item in content:
                    t = item.get("type", "")
                    if t == "text":
                        text_parts.append(item.get("text", ""))
                    elif t == "image_url":
                        url = item.get("image_url", {}).get("url", "")
                        if url.startswith("data:"):
                            # Strip the data:<mime>;base64, prefix
                            b64 = url.split(",", 1)[1] if "," in url else url
                            images.append(b64)
                msg: dict[str, Any] = {
                    "role": m["role"],
                    "content": " ".join(text_parts).strip(),
                }
                if images:
                    msg["images"] = images
                # Preserve any extra keys (tool_call_id, name, etc.)
                for k in ("tool_call_id", "name", "tool_calls"):
                    if k in m:
                        msg[k] = m[k]
                result.append(msg)
            else:
                result.append(m)
        return result

    async def _chat_ollama(
        self,
        messages: list[dict],
        tools: list[dict],
        temperature: float,
        max_tokens: int,
    ) -> LLMResponse:
        body: dict[str, Any] = {
            "model": self.model,
            "messages": self._to_ollama_messages(messages),
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                # FIX: Without num_ctx, Ollama defaults to 4096 tokens which
                # silently truncates the tool schemas — the model never sees
                # tool definitions and can't make tool calls.
                "num_ctx": self._OLLAMA_NUM_CTX,
            },
        }

        if tools:
            body["tools"] = tools

        try:
            resp = await self._client.post("/api/chat", json=body)
            resp.raise_for_status()
        except httpx.ConnectError:
            raise ConnectionError(
                f"Cannot connect to Ollama at {self._api_url}.\n"
                "Make sure Ollama is running. Start it with: ollama serve\n"
                "Download from: https://ollama.com/download"
            )
        except httpx.HTTPStatusError as exc:
            body_text = exc.response.text
            if exc.response.status_code == 404 or "not found" in body_text.lower():
                raise RuntimeError(
                    f"Model '{self.model}' is not installed in Ollama.\n"
                    f"Pull it first: ollama pull {self.model}\n"
                    f"Browse models: https://ollama.com/library"
                ) from exc
            raise RuntimeError(f"Ollama API error {exc.response.status_code}: {body_text}") from exc

        data = resp.json()
        msg = data.get("message", {})
        tool_calls_raw = msg.get("tool_calls", [])

        tool_calls = []
        for i, tc in enumerate(tool_calls_raw):
            fn = tc.get("function", {})
            args = fn.get("arguments", {})
            # FIX: Some Ollama model versions return arguments as a JSON string
            # rather than a pre-parsed dict. Normalise to dict in both cases.
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except (json.JSONDecodeError, ValueError):
                    args = {"raw": args}
            tool_calls.append(ToolCall(
                id=f"call_{i}",
                name=fn.get("name", ""),
                arguments=args,
            ))

        return LLMResponse(
            text=msg.get("content", "") or "",
            tool_calls=tool_calls,
            finish_reason="tool_calls" if tool_calls else "stop",
            prompt_tokens=data.get("prompt_eval_count", 0),
            completion_tokens=data.get("eval_count", 0),
        )

    # ── Streaming Implementations ────────────────────────────────────────

    async def _stream_anthropic(
        self,
        messages: list[dict],
        tools: list[dict],
        temperature: float,
        max_tokens: int,
        effort_level: str = "",
    ) -> AsyncIterator[StreamEvent]:
        """Stream from Anthropic Messages API using SSE."""
        system_parts = []
        conv_messages = []
        for m in messages:
            if m["role"] == "system":
                system_parts.append(m["content"])
            else:
                conv_messages.append(self._to_anthropic_message(m))

        conv_messages = self._fix_anthropic_alternation(conv_messages)

        body: dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": conv_messages,
            "stream": True,
        }

        # Extended Thinking support for Anthropic
        if effort_level and effort_level.lower() in ("medium", "high"):
            budget_map = {"medium": 8192, "high": 32768}
            thinking_budget = budget_map.get(effort_level.lower(), 8192)
            body["thinking"] = {
                "type": "enabled",
                "budget_tokens": thinking_budget,
            }
            # Anthropic requires temperature=1 when thinking is enabled
            body["temperature"] = 1.0

        # PERF: Use Anthropic prompt caching — emit one cache_control
        # block per system message (up to Anthropic's limit of 4).  When
        # the COGNOME runtime injects an Engram as a separate system
        # message, the dev system prompt keeps its own cache breakpoint
        # so topic shifts (which change the Engram) don't invalidate it.
        if system_parts:
            body["system"] = self._anthropic_system_blocks(system_parts)

        if tools:
            anthropic_tools = []
            for t in tools:
                fn = t.get("function", t)
                anthropic_tools.append({
                    "name": fn.get("name", ""),
                    "description": fn.get("description", ""),
                    "input_schema": fn.get("parameters", fn.get("input_schema", {})),
                })
            body["tools"] = anthropic_tools

        tool_calls: list[ToolCall] = []
        tool_input_buffers: dict[int, str] = {}
        prompt_tokens = 0
        completion_tokens = 0
        cache_read = 0

        # Connect-time retry (v3.5.8). Retries only the handshake and
        # first byte — never mid-stream, so partial answers cannot be
        # corrupted. See _CONN_RETRYABLE_EXC for the exception list.
        stream_resp_cm = None
        for attempt in range(_MAX_CONN_RETRIES + 1):
            try:
                stream_resp_cm = self._client.stream("POST", self._api_messages_path, json=body)
                break
            except _CONN_RETRYABLE_EXC as exc:
                last_exc = exc
                if attempt >= _MAX_CONN_RETRIES:
                    raise ConnectionError(
                        f"MiniMax/anthropic-compat STREAM failed to open "
                        f"after {_MAX_CONN_RETRIES + 1} attempts "
                        f"(provider={self.provider}, model={self.model}, "
                        f"url={self._api_url}{self._api_messages_path}). "
                        f"Last error: {type(exc).__name__}: {exc}"
                    ) from exc
                backoff = _TRANSIENT_RETRY_BASE_DELAY * (2 ** attempt)
                jitter = random.uniform(0, _JITTER_MAX)
                delay = backoff + jitter
                logger.warning(
                    "anthropic-compat STREAM open failed (provider=%s, "
                    "model=%s, attempt %d/%d): %s — retrying in %.2fs",
                    self.provider, self.model, attempt + 1,
                    _MAX_CONN_RETRIES + 1, type(exc).__name__, delay,
                )
                await asyncio.sleep(delay)
        async with stream_resp_cm as resp:
            try:
                resp.raise_for_status()
            except httpx.HTTPStatusError as exc:
                friendly = _friendly_anthropic_error(exc, self.provider, self.model)
                if friendly is not None:
                    raise RuntimeError(friendly) from exc
                raise
            async for line in resp.aiter_lines():
                if not line.startswith("data: "):
                    continue
                data_str = line[6:]
                if data_str.strip() == "[DONE]":
                    break
                try:
                    event = json.loads(data_str)
                except json.JSONDecodeError:
                    continue

                event_type = event.get("type", "")

                if event_type == "content_block_start":
                    block = event.get("content_block", {})
                    if block.get("type") == "tool_use":
                        idx = event.get("index", len(tool_calls))
                        tc = ToolCall(
                            id=block.get("id", f"call_{idx}"),
                            name=block.get("name", ""),
                            arguments={},
                        )
                        tool_calls.append(tc)
                        tool_input_buffers[idx] = ""
                        yield StreamEvent(type="tool_call_start", tool_call=tc, tool_call_index=idx)

                elif event_type == "content_block_delta":
                    delta = event.get("delta", {})
                    if delta.get("type") == "text_delta":
                        yield StreamEvent(type="text_delta", text=delta.get("text", ""))
                    elif delta.get("type") == "input_json_delta":
                        idx = event.get("index", 0)
                        partial = delta.get("partial_json", "")
                        if idx in tool_input_buffers:
                            tool_input_buffers[idx] += partial

                elif event_type == "content_block_stop":
                    idx = event.get("index", 0)
                    if idx in tool_input_buffers and idx < len(tool_calls):
                        try:
                            tool_calls[idx].arguments = json.loads(tool_input_buffers[idx])
                        except json.JSONDecodeError:
                            tool_calls[idx].arguments = {"raw": tool_input_buffers[idx]}

                elif event_type == "message_delta":
                    usage = event.get("usage", {})
                    completion_tokens = usage.get("output_tokens", completion_tokens)

                elif event_type == "message_start":
                    msg_data = event.get("message", {})
                    usage = msg_data.get("usage", {})
                    prompt_tokens = usage.get("input_tokens", 0)
                    cache_read = usage.get("cache_read_input_tokens", 0)

        yield StreamEvent(
            type="done",
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cache_read_tokens=cache_read,
        )

    async def _stream_openai(
        self,
        messages: list[dict],
        tools: list[dict],
        temperature: float,
        max_tokens: int,
        effort_level: str = "",
    ) -> AsyncIterator[StreamEvent]:
        """Stream from OpenAI Chat Completions API using SSE."""
        if self.provider == "vertex":
            self._refresh_vertex_token()
        if self.provider == "github":
            await self._ensure_github_token()
            if "claude" in self.model.lower():
                messages = self._fix_github_claude_messages(messages)

        body: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
            "stream_options": {"include_usage": True},
        }

        # Vertex AI OpenAI-compat endpoint requires "google/" prefix for Gemini models
        if self.provider == "vertex" and not self.model.startswith(("google/", "meta/", "mistral")):
            body["model"] = f"google/{self.model}"

        if self.provider == "github":
            body.pop("stream_options", None)
            if "claude" in self.model.lower():
                if "max_tokens" in body and body["max_tokens"] > 4096:
                    body["max_tokens"] = 4096

        if "o1" in self.model.lower():
            body.pop("temperature", None)
            if "max_tokens" in body:
                body["max_completion_tokens"] = body.pop("max_tokens")

        # OpenAI reasoning_effort support (for o-series and GPT-5+ models)
        if effort_level and effort_level.lower() in ("low", "medium", "high"):
            body["reasoning_effort"] = effort_level.lower()

        if tools:
            body["tools"] = tools
            body["tool_choice"] = "auto"

        tool_calls: dict[int, ToolCall] = {}
        tool_args_buffers: dict[int, str] = {}
        prompt_tokens = 0
        completion_tokens = 0

        path = "/chat/completions" if self.provider in ("github", "vertex") else "/v1/chat/completions"

        async with self._client.stream("POST", path, json=body) as resp:
            # ── Transient errors (429, 500, 502, 503) ─────────────
            if resp.status_code in _TRANSIENT_STATUS_CODES:
                await resp.aread()
                ra = (
                    resp.headers.get("retry-after")
                    or resp.headers.get("Retry-After")
                )
                hint = f" (retry after {ra}s)" if ra else ""
                raise RetriesExhaustedError(
                    f"Rate-limited ({resp.status_code}){hint}. "
                    f"Wait a moment and try again."
                )

            if resp.status_code == 400 and self.provider == "github":
                await resp.aread()
            try:
                resp.raise_for_status()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 400 and self.provider == "github":
                    try:
                        err_data = e.response.json()
                        err_code = err_data.get("error", {}).get("code")
                        if err_code == "model_not_supported":
                            raise RuntimeError("Your GitHub Copilot tier does not have access to this model. Please upgrade your plan or use /model to select an available one.")
                        elif err_code == "unsupported_api_for_model":
                            raise RuntimeError("This model does not support chat completions via the Copilot API.")
                        else:
                            raise RuntimeError(f"GitHub Copilot API 400 Bad Request: {e.response.text}")
                    except json.JSONDecodeError:
                        raise RuntimeError(f"GitHub Copilot API 400 Bad Request: {e.response.text}")
                raise
            async for line in resp.aiter_lines():
                if not line.startswith("data: "):
                    continue
                data_str = line[6:]
                if data_str.strip() == "[DONE]":
                    break
                try:
                    chunk = json.loads(data_str)
                except json.JSONDecodeError:
                    continue

                choice = (chunk.get("choices") or [{}])[0]
                delta = choice.get("delta", {})

                # Text content
                if delta.get("content"):
                    yield StreamEvent(type="text_delta", text=delta["content"])

                # Tool calls
                for tc_delta in delta.get("tool_calls", []):
                    idx = tc_delta.get("index", 0)
                    if idx not in tool_calls:
                        fn = tc_delta.get("function", {})
                        tc = ToolCall(
                            id=tc_delta.get("id", f"call_{idx}"),
                            name=fn.get("name", ""),
                            arguments={},
                        )
                        tool_calls[idx] = tc
                        tool_args_buffers[idx] = ""
                        yield StreamEvent(type="tool_call_start", tool_call=tc, tool_call_index=idx)

                    fn_delta = tc_delta.get("function", {})
                    if fn_delta.get("arguments"):
                        tool_args_buffers[idx] = tool_args_buffers.get(idx, "") + fn_delta["arguments"]

                # Usage info
                usage = chunk.get("usage")
                if usage:
                    prompt_tokens = usage.get("prompt_tokens", 0)
                    completion_tokens = usage.get("completion_tokens", 0)

        # Finalize tool call arguments
        for idx, tc in tool_calls.items():
            raw = tool_args_buffers.get(idx, "{}")
            try:
                tc.arguments = json.loads(raw)
            except json.JSONDecodeError:
                tc.arguments = {"raw": raw}

        yield StreamEvent(
            type="done",
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
        )

    async def _stream_ollama(
        self,
        messages: list[dict],
        tools: list[dict],
        temperature: float,
        max_tokens: int,
    ) -> AsyncIterator[StreamEvent]:
        """
        Stream from Ollama's native /api/chat endpoint.

        Tool call handling:
          Ollama sends tool_calls in ONE intermediate done:false chunk as a
          complete list (not incrementally like OpenAI). We accumulate them
          with a global index so IDs are unique across the entire response,
          then yield a tool_call_start event for each one as it arrives.

        num_ctx:
          Must be set explicitly — Ollama defaults to 4096 which truncates
          tool schemas and causes silent tool-call failures.
        """
        body: dict[str, Any] = {
            "model": self.model,
            "messages": self._to_ollama_messages(messages),
            "stream": True,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                # FIX: Must set num_ctx or tool schemas get silently truncated
                "num_ctx": self._OLLAMA_NUM_CTX,
            },
        }

        if tools:
            body["tools"] = tools

        prompt_tokens = 0
        completion_tokens = 0
        # Global tool call counter so IDs are unique across chunks
        tc_global_idx = 0

        try:
            async with self._client.stream("POST", "/api/chat", json=body) as resp:
                # Must read the body before calling raise_for_status() inside a
                # streaming context — httpx raises ResponseNotRead otherwise when
                # it tries to include resp.text in the HTTPStatusError message.
                if resp.status_code >= 400:
                    await resp.aread()
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line.strip():
                        continue
                    try:
                        chunk = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    msg = chunk.get("message", {})

                    # Text content delta — skip qwen3/thinking-mode "thinking"
                    # field; only forward the visible "content" to the user.
                    content = msg.get("content", "")
                    if content:
                        yield StreamEvent(type="text_delta", text=content)

                    # Tool calls — Ollama sends complete tool_calls in a single
                    # intermediate chunk (done:false). Accumulate with global index.
                    for tc_raw in msg.get("tool_calls", []):
                        fn = tc_raw.get("function", {})
                        args = fn.get("arguments", {})
                        # FIX: Normalise arguments — may be JSON string in some builds
                        if isinstance(args, str):
                            try:
                                args = json.loads(args)
                            except (json.JSONDecodeError, ValueError):
                                args = {"raw": args}
                        tc = ToolCall(
                            id=f"call_{tc_global_idx}",
                            name=fn.get("name", ""),
                            arguments=args,
                        )
                        yield StreamEvent(
                            type="tool_call_start",
                            tool_call=tc,
                            tool_call_index=tc_global_idx,
                        )
                        tc_global_idx += 1

                    if chunk.get("done"):
                        prompt_tokens = chunk.get("prompt_eval_count", 0)
                        completion_tokens = chunk.get("eval_count", 0)

        except httpx.ConnectError:
            raise ConnectionError(
                f"Cannot connect to Ollama at {self._api_url}.\n"
                "Make sure Ollama is running. Start it with: ollama serve"
            )
        except httpx.HTTPStatusError as exc:
            body_text = exc.response.text
            if exc.response.status_code == 404 or "not found" in body_text.lower():
                raise RuntimeError(
                    f"Model '{self.model}' is not installed in Ollama.\n"
                    f"Pull it with: ollama pull {self.model}"
                ) from exc
            raise

        yield StreamEvent(
            type="done",
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
        )
