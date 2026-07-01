"""
cvc.operations.engram_injectors — Provider-aware Engram placement.

The base contract (:class:`EngramInjector`) knows how to prepend a
compiled Engram to an OpenAI-format message list.  Subclasses tune the
placement and add provider-specific metadata so downstream adapters can
emit optimal cache-control headers.

Why this matters
----------------
Every provider caches prefixes differently.  A naive ``messages.insert(0,
system)`` is correct but loses roughly 30–50% of the caching headroom on
Anthropic because the dev system prompt and the Engram end up in one
combined block with a single cache breakpoint.  By emitting two
breakpoints (dev prompt + Engram) we keep the dev prompt cached even
when the Engram changes (e.g., topic shift).

Contract
--------
Every injector:

* Takes ``(messages, engram)`` and returns a new message list.
* Never mutates the input list.
* Is a no-op when the engram is empty.
* Adds the Engram as the first "system-ish" block so it rides the
  provider's stable prefix.
* Tags the injected message with ``_cvc_engram_hash`` + role-specific
  hints so callers/adapters can recognise it.

Supported providers: ``anthropic``, ``openai``, ``google``, ``ollama``,
``lmstudio``, ``github``, ``vertex``.
"""

from __future__ import annotations

import logging
from typing import Any

from cvc.operations.cognome import CompiledEngram

logger = logging.getLogger("cvc.operations.engram_injectors")

# Internal metadata keys we stamp on the injected message.  These are
# dropped at the provider-HTTP boundary by the adapters (or ignored as
# unknown fields on OpenAI-compatible transports that accept them).
_META_ENGRAM_HASH = "_cvc_engram_hash"
_META_CACHE_BREAKPOINT = "_cvc_cache_breakpoint"
_META_INJECTOR = "_cvc_injector"


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------

class EngramInjector:
    """
    Default injector — used by OpenAI, Ollama, LMStudio, GitHub, Vertex.

    Places the Engram as a new system message **after** any existing
    system messages so the developer's own system prompt stays at the
    front (maximum stable prefix → automatic prompt caching).
    """

    name: str = "default"

    def inject(
        self,
        messages: list[dict[str, Any]],
        engram: CompiledEngram,
    ) -> list[dict[str, Any]]:
        if not engram.preamble:
            return messages
        insert_at = self._find_insert_index(messages)
        out = list(messages)
        out.insert(insert_at, self._build_engram_message(engram))
        return out

    # ------------------------------------------------------------------
    # Hooks
    # ------------------------------------------------------------------

    def _find_insert_index(self, messages: list[dict[str, Any]]) -> int:
        """Insert after the last contiguous system message (or at index 0)."""
        idx = 0
        for i, m in enumerate(messages):
            if m.get("role") == "system":
                idx = i + 1
            else:
                break
        return idx

    def _build_engram_message(self, engram: CompiledEngram) -> dict[str, Any]:
        return {
            "role": "system",
            "content": engram.preamble,
            _META_ENGRAM_HASH: engram.engram_hash,
            _META_INJECTOR: self.name,
        }


# ---------------------------------------------------------------------------
# Anthropic — emits a second cache breakpoint
# ---------------------------------------------------------------------------

class AnthropicEngramInjector(EngramInjector):
    """
    Inserts the Engram as a system message tagged for a dedicated
    cache_control breakpoint.

    The Anthropic adapter (and :class:`cvc.agent.llm.AgentLLM`
    ``_chat_anthropic``/``_stream_anthropic``) detects the
    ``_cvc_cache_breakpoint`` tag and emits the Engram as its own
    ``{"type": "text", "cache_control": ...}`` block — giving us a
    second reusable breakpoint.  Result: dev system prompt stays
    cached across topic shifts.
    """

    name: str = "anthropic"

    def _build_engram_message(self, engram: CompiledEngram) -> dict[str, Any]:
        msg = super()._build_engram_message(engram)
        msg[_META_CACHE_BREAKPOINT] = True
        return msg


# ---------------------------------------------------------------------------
# Google Gemini — uses systemInstruction
# ---------------------------------------------------------------------------

class GoogleEngramInjector(EngramInjector):
    """
    For Google Gemini the Engram still rides as a system role message;
    the ``_chat_google`` path already consolidates system content into
    ``systemInstruction``.  We merely mark the message so the adapter
    layer can route it as a separate cached content block if the
    provider supports explicit caching.
    """

    name: str = "google"

    def _build_engram_message(self, engram: CompiledEngram) -> dict[str, Any]:
        msg = super()._build_engram_message(engram)
        # Gemini explicit cachedContent API — adapter opt-in, non-breaking.
        msg[_META_CACHE_BREAKPOINT] = True
        return msg


# ---------------------------------------------------------------------------
# Ollama / LMStudio — no caching, plain prepend
# ---------------------------------------------------------------------------

class OllamaEngramInjector(EngramInjector):
    name: str = "ollama"


# ---------------------------------------------------------------------------
# Selector
# ---------------------------------------------------------------------------

_REGISTRY: dict[str, type[EngramInjector]] = {
    "anthropic": AnthropicEngramInjector,
    "google": GoogleEngramInjector,
    "gemini": GoogleEngramInjector,
    "vertex": GoogleEngramInjector,  # Vertex = Gemini on GCP
    "ollama": OllamaEngramInjector,
    "lmstudio": OllamaEngramInjector,
    "openai": EngramInjector,
    "github": EngramInjector,
    "": EngramInjector,
}


def select_injector(provider: str) -> EngramInjector:
    """Return the injector tuned for *provider* (default on unknown)."""
    key = (provider or "").lower().strip()
    cls = _REGISTRY.get(key, EngramInjector)
    return cls()


def is_engram_message(message: dict[str, Any]) -> bool:
    """True if *message* was produced by any injector in this module."""
    return bool(message.get(_META_ENGRAM_HASH))


def strip_engram_metadata(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Remove all ``_cvc_*`` metadata keys from messages so the provider
    HTTP payload is clean.  Adapters that understand the metadata should
    consume it BEFORE calling this helper.
    """
    out: list[dict[str, Any]] = []
    for m in messages:
        if any(k.startswith("_cvc_") for k in m):
            clean = {k: v for k, v in m.items() if not k.startswith("_cvc_")}
            out.append(clean)
        else:
            out.append(m)
    return out


def engram_cache_breakpoint_index(messages: list[dict[str, Any]]) -> int | None:
    """
    Return the index of the Engram message tagged as a cache breakpoint,
    or ``None`` if there is no such marker.

    Adapters call this to decide where to emit the second
    ``cache_control`` block for providers that support it.
    """
    for i, m in enumerate(messages):
        if m.get(_META_CACHE_BREAKPOINT) and m.get(_META_ENGRAM_HASH):
            return i
    return None
