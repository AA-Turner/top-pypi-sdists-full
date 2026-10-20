"""PROMPT CACHE MARKS — where the platform puts cache points, and for how long.

The platform places every cache point itself; no author ever places one (the per-message
``cache_boundary`` flag was retired 2026-10-16: on the system message it did nothing, and the
end of the authored template is a better place the platform can find on its own).

Three marks, at most, on a wire that takes explicit marks (Anthropic):

1. **System mark** — end of the stable system text (or the last tool when there is none).
2. **Template mark** — end of the last AUTHORED template message that the variable fill did
   not change, before any typed or filled content. Few-shot pairs and fixed authored turns
   are cached across runs that differ only in their input.
3. **Rolling mark** — the last message, so the conversation caches as it grows.

Long cache (``UnifiedConfig.extended_prompt_cache``, the agent setting) keeps the stable
prefix longer: marks 1 and 2 carry ``ttl: "1h"``; the rolling mark stays at the 5-minute
default, because Anthropic requires every 1-hour mark to come before any 5-minute mark.
On wires without explicit marks it maps to that provider's own retention knob, or is said
to be a no-op (``long_cache_note``). Facts: common-docs projects/agent-evaluation/research/
provider-caching.md.

How the template mark finds its place: ``UnifiedConfig.replace_variables`` (the one fill,
always run on a first turn) stamps each authored message's metadata with
``TEMPLATE_METADATA_KEY`` = ``"stable"`` (the fill left it as authored) or ``"filled"``. The
metadata round-trips through ``cx_message.metadata``, so later turns find the same place.
"""

from __future__ import annotations

from typing import Any

#: Message metadata key stamped by the fill on every authored template message.
TEMPLATE_METADATA_KEY = "cache_template"
TEMPLATE_STABLE = "stable"
TEMPLATE_FILLED = "filled"

#: Anthropic's per-request ceiling on cache_control marks.
MAX_ANTHROPIC_CACHE_MARKS = 4

#: OpenAI models that take ``prompt_cache_retention: "24h"`` (provider docs, 2026-10-16).
#: GPT-5.6 and later replaced it with ``prompt_cache_options.ttl`` = "30m" only.
OPENAI_EXTENDED_RETENTION_MODELS: tuple[str, ...] = (
    "gpt-5.5",
    "gpt-5.5-pro",
    "gpt-5.4",
    "gpt-5.2",
    "gpt-5.1",
    "gpt-5.1-codex",
    "gpt-5.1-codex-mini",
    "gpt-5.1-codex-max",
    "gpt-5.1-chat-latest",
    "gpt-5",
    "gpt-5-codex",
    "gpt-4.1",
)


def cache_control(*, long: bool) -> dict[str, str]:
    """One Anthropic cache mark. ``long`` = the 1-hour lifetime."""
    return {"type": "ephemeral", "ttl": "1h"} if long else {"type": "ephemeral"}


def _content_signature(message: Any) -> str:
    parts = []
    for content in getattr(message, "content", None) or []:
        fields = getattr(content, "__dict__", None)
        if isinstance(fields, dict):
            parts.append({k: v for k, v in fields.items() if not k.startswith("_")})
        else:
            parts.append(content)
    return repr(parts)


def snapshot_signatures(messages: Any) -> dict[int, str]:
    """Each message's content signature by identity, taken BEFORE the fill."""
    return {id(m): _content_signature(m) for m in messages or []}


def stamp_template_messages(template_messages: Any, before: dict[int, str]) -> None:
    """After the fill: mark each authored message stable (unchanged) or filled."""
    for message in template_messages or []:
        metadata = getattr(message, "metadata", None)
        if not isinstance(metadata, dict):
            try:
                message.metadata = metadata = {}
            except (AttributeError, TypeError):
                continue
        unchanged = before.get(id(message)) == _content_signature(message)
        metadata[TEMPLATE_METADATA_KEY] = TEMPLATE_STABLE if unchanged else TEMPLATE_FILLED


def _carries_data(message: Any) -> bool:
    from matrx_ai.config.template_substitution import data_tail, is_data

    return any(is_data(c) or data_tail(c) for c in getattr(message, "content", None) or [])


def template_mark_index(messages: Any) -> int | None:
    """The index of the message the template mark goes on, or ``None``.

    The leading run of authored messages the fill left unchanged, stopping at the first
    message that is not authored, was filled, carries typed data, or is a trailing prefill
    (the reply continues from it; it is not a cached prefix).
    """
    from matrx_ai.config.message_flags import flags_of

    found: int | None = None
    for index, message in enumerate(messages or []):
        metadata = getattr(message, "metadata", None)
        if not isinstance(metadata, dict) or metadata.get(TEMPLATE_METADATA_KEY) != TEMPLATE_STABLE:
            break
        if _carries_data(message) or flags_of(message).get("prefill"):
            break
        found = index
    return found


def openai_takes_extended_retention(model: str | None) -> bool:
    name = (model or "").strip().lower()
    return any(name == m or name.startswith(m + "-20") for m in OPENAI_EXTENDED_RETENTION_MODELS)


#: Anthropic's cache tiers by their own names — the name IS the lifetime (provider fact).
#: The rolling (history) mark is always "5m"; "1h" covers only marks 1 and 2 (system +
#: authored template) when long cache is on.
ANTHROPIC_CACHE_TIER_SECS: dict[str, int] = {"5m": 5 * 60, "1h": 60 * 60}


def history_cache_ttl(provider: str | None, *, long: bool) -> tuple[int | None, str | None, int | None]:
    """``(history_ttl_secs, write_tier, prefix_ttl_secs)`` for the wire's real marks.

    The history — what a context trim rewrites — sits behind the ROLLING mark. On
    Anthropic that mark never carries ``ttl: "1h"`` (every 1h mark must come before
    every 5m mark), so a trim always re-writes at the 5-minute price and the history
    lives 5 minutes, long cache or not; long cache keeps only the stable prefix for an
    hour (``prefix_ttl_secs``). ``None`` = this module has no fact for the provider
    (the caller keeps its own default).
    """
    name = (provider or "").lower()
    if "anthropic" in name or "claude" in name:
        tiers = ANTHROPIC_CACHE_TIER_SECS
        return tiers["5m"], "5m", tiers["1h" if long else "5m"]
    return None, None, None


def long_cache_note(provider: str, model: str | None, *, applied: str | None) -> str:
    """The sentence the Model view and the log carry for the long-cache setting."""
    label = model or provider
    if applied:
        return f"Long cache on {label}: {applied}."
    why = {
        "google": "Gemini caches repeated prefixes implicitly and has no lifetime setting here",
        "openai": "this model has no longer cache retention to ask for",
    }.get(provider, "this provider caches automatically and has no lifetime setting")
    return f"Long cache on {label}: nothing extra is sent — {why}."


__all__ = [
    "MAX_ANTHROPIC_CACHE_MARKS",
    "OPENAI_EXTENDED_RETENTION_MODELS",
    "TEMPLATE_FILLED",
    "TEMPLATE_METADATA_KEY",
    "TEMPLATE_STABLE",
    "cache_control",
    "history_cache_ttl",
    "long_cache_note",
    "openai_takes_extended_retention",
    "snapshot_signatures",
    "stamp_template_messages",
    "template_mark_index",
]
