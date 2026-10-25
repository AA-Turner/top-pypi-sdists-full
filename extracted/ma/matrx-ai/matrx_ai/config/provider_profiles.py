"""Per-provider send facts, read by the send boundary AND the translators — one table.

``TURN_CONTEXT_AFTER_CACHE_LINE`` — THE CACHE LINE LAW (Arman, 2026-10-16): "NOTHING, other
than the removal of LARGE tool outputs should ever modify text behind the cache line." True =
this provider gets the per-turn context block (live date and time, selection, values, attached
skills…) AFTER the cached prefix, never in the system channel, where it would change the cached
prefix every turn. Every chat provider is True (2026-10-16: Anthropic, OpenAI, then Google, xAI,
Groq, Cerebras, Together, generic OpenAI-compatible incl. Moonshot).

Who reads it:

* the send boundary (``send_boundary.order_for_wire``) — decides whether this send places the
  block in the person's turn, before their typed text (THE REQUEST ENDS WITH WHAT THE PERSON
  TYPED, Arman 2026-10-19);
* the translators (``BaseTranslator.get_system_text`` — the cache gate of the system channel —
  and ``get_trailing_context_text``) — keep the block out of the system text.

A provider missing here is False: its block stays in the system text. Guards:
``tests/test_turn_context_rides_after_the_cache_line_on_every_provider.py``,
``tests/test_request_ends_with_what_the_person_typed.py``.
"""

from __future__ import annotations

from typing import Any

TURN_CONTEXT_AFTER_CACHE_LINE: dict[str, bool] = {
    "anthropic": True,
    "openai": True,
    "google": True,
    "xai": True,
    "groq": True,
    "cerebras": True,
    "together": True,
    "generic_openai": True,
}

#: Chat wire routes (``ai.api.translator_key``) whose translator family differs from the prefix.
_WIRE_FAMILY: dict[str, str] = {
    "moonshot_chat": "generic_openai",
    "device_chat": "generic_openai",
    "generic_openai_chat": "generic_openai",
    "openai_responses": "openai",
}

#: The execution channel of an OpenAI-compatible endpoint from the host registry.
_GENERIC_CLIENT_ATTR = "generic_openai_chat"


def turn_context_after_cache_line(provider: str | None) -> bool:
    """True when ``provider`` (a translator family key) carries the block after the cache line."""
    return bool(TURN_CONTEXT_AFTER_CACHE_LINE.get(str(provider or ""), False))


def chat_provider_of(profile: Any) -> str | None:
    """The translator family a ``ResolvedCallProfile`` renders through, or ``None`` (not a chat send).

    Only a chat turn that produces text renders a message list with the person's turn: an image,
    video, speech (TTS: audio out, no text out), decision or extraction route returns ``None``.
    """
    if profile is None:
        return None
    capabilities = getattr(profile, "capabilities", None)
    if capabilities is not None:
        if bool(getattr(capabilities, "produces_audio", False)) and not bool(
            getattr(capabilities, "produces_text", True)
        ):
            return None
        interaction = getattr(capabilities, "interaction", None)
        if interaction not in (None, "turn"):
            return None
    if str(getattr(profile, "client_attr", "") or "") == _GENERIC_CLIENT_ATTR:
        return "generic_openai"
    wire = str(getattr(profile, "wire_format", "") or "")
    if wire in _WIRE_FAMILY:
        return _WIRE_FAMILY[wire]
    if wire in TURN_CONTEXT_AFTER_CACHE_LINE:
        return wire
    if not wire.endswith("_chat"):
        return None
    return wire.removesuffix("_chat")


#: Chat-Completions-shaped wire routes: the only wires where a model the catalog declares
#: ``strict_role_alternation`` (probe-proven to reject user, user) keeps the per-turn block in the
#: documented fallback, the end of the system message (``place_trailing_on_chat_messages``).
#: Anthropic, Gemini, OpenAI Responses and xAI take the block as its own turn on any model.
STRICT_ALTERNATION_WIRES: frozenset[str] = frozenset(
    {
        "groq_chat",
        "cerebras_chat",
        "together_chat",
        "openai_chat",
        "moonshot_chat",
        "device_chat",
        "generic_openai_chat",
    }
)


def requires_strict_role_alternation(profile: Any) -> bool:
    """True when this send must not add a second user turn: the model profile's catalog fact
    (``strict_role_alternation``) on a Chat-Completions-shaped wire."""
    capabilities = getattr(profile, "capabilities", None)
    if not bool(getattr(capabilities, "requires_strict_role_alternation", False)):
        return False
    wire = str(getattr(profile, "wire_format", "") or "")
    return wire in STRICT_ALTERNATION_WIRES or str(getattr(profile, "client_attr", "") or "") == _GENERIC_CLIENT_ATTR


__all__ = [
    "STRICT_ALTERNATION_WIRES",
    "TURN_CONTEXT_AFTER_CACHE_LINE",
    "chat_provider_of",
    "requires_strict_role_alternation",
    "turn_context_after_cache_line",
]
