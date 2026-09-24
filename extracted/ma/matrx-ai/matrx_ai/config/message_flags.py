"""Message FLAGS — an instruction to the translator about a message, never content.

The primitives table (common-docs/systems/agents/typed-messages/FEATURE.md) names
three flags an author sets on a message. The provider never sees a flag as
content; each translator decides what it means on its wire:

* ``prefill`` — a TRAILING assistant message the reply must continue from.
  Native only on models that declare the ``assistant_prefill`` capability
  (Anthropic removed it on Sonnet 5 / Opus 5 / Fable / the 4.6-4.8 line; OpenAI
  and Gemini never had it). Once the reply exists the prefill is CONSUMED: the
  reply carries its text, and the flagged message never reaches a wire again.
* ``cache_boundary`` — "cache everything up to and including this message".
  Anthropic: a ``cache_control`` breakpoint on the message's last block. OpenAI
  caches prefixes automatically; Gemini caches implicitly — both announce a
  no-op instead of pretending.
* ``example`` — a few-shot turn. Sent as an ordinary turn; the flag rides the
  persisted message metadata so the runner collapses example pairs.

Storage: an authored agent-definition message carries ``flags`` at top level;
``UnifiedMessage.from_dict`` validates it and keeps it at ``metadata["flags"]``
so it round-trips through ``cx_message.metadata`` with no new column.

THE COMPATIBILITY LAW: a flag a model cannot honour is never silently dropped.
The org knob ``agents.messages / flag_compatibility_mode`` (``refuse`` | ``convert``
| ``drop``, default ``refuse``) decides; the host resolves it and stamps
``config.metadata["flag_compatibility_mode"]``. ``convert`` turns a prefill into a
system-channel instruction ("begin your reply with exactly: …") and the reply is
marked "asked for, not forced" with whether it actually starts with the text.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, ValidationError

FLAG_KEYS: tuple[str, ...] = ("prefill", "cache_boundary", "example")

#: Where a runtime message keeps its flags (cx_message.metadata round-trips it).
FLAGS_METADATA_KEY = "flags"

#: Where the host stamps the org's compatibility mode on ``config.metadata``.
COMPAT_MODE_METADATA_KEY = "flag_compatibility_mode"

#: Where the answer records how its prefill was honoured (runner reads it).
PREFILL_RESULT_METADATA_KEY = "prefill"

CompatMode = Literal["refuse", "convert", "drop"]
COMPAT_MODES: tuple[str, ...] = ("refuse", "convert", "drop")
#: Mirrors the seeded knob default (aidream ai_091) for hosts with no knob register.
DEFAULT_COMPAT_MODE: CompatMode = "refuse"

#: The knob the host resolves (feature, key).
COMPAT_MODE_KNOB = ("agents.messages", "flag_compatibility_mode")

CacheBoundarySupport = Literal["breakpoint", "automatic", "implicit", "none"]

#: How each chat wire honours a cache boundary. A wire not listed = "none".
CACHE_BOUNDARY_BY_WIRE: dict[str, CacheBoundarySupport] = {
    "anthropic_chat": "breakpoint",
    "openai_chat": "automatic",
    "google_chat": "implicit",
}

CONVERT_PREFILL_SLOT = "prefill"


class MessageFlags(BaseModel):
    """The validated flag set. Only ``true`` means anything; ``false`` is absence."""

    model_config = ConfigDict(extra="forbid")

    prefill: bool | None = None
    cache_boundary: bool | None = None
    example: bool | None = None

    def as_dict(self) -> dict[str, bool]:
        return {k: True for k in FLAG_KEYS if getattr(self, k) is True}


class InvalidMessageFlags(ValueError):
    """An authored flag set breaks a placement rule (which role, which position)."""


class MessageFlagRefusal(ValueError):
    """A flag the model cannot honour under the org's ``refuse`` mode.

    Raised BEFORE the provider call — nothing is spent. ``user_message`` is the
    sentence the builder also shows beside the greyed toggle.
    """

    def __init__(self, user_message: str, *, code: str = "message_flag_refused") -> None:
        super().__init__(user_message)
        self.user_message = user_message
        self.code = code


def parse_flags(raw: Any) -> dict[str, bool]:
    """Validate a raw ``flags`` value → ``{flag: True}``. Unknown keys raise."""
    if raw is None or raw == {}:
        return {}
    if not isinstance(raw, dict):
        raise InvalidMessageFlags(f"flags must be an object, got {type(raw).__name__}")
    try:
        return MessageFlags.model_validate(raw).as_dict()
    except ValidationError as exc:
        raise InvalidMessageFlags(f"invalid message flags {raw!r}: {exc.errors()[0]['msg']}") from exc


def _role_of(message: Any) -> str:
    role = message.get("role") if isinstance(message, dict) else getattr(message, "role", None)
    return str(getattr(role, "value", role) or "")


def flags_of(message: Any) -> dict[str, bool]:
    """The flags on a runtime ``UnifiedMessage`` (metadata) or an authored dict."""
    if isinstance(message, dict):
        raw = message.get("flags")
        if raw is None:
            raw = (message.get("metadata") or {}).get(FLAGS_METADATA_KEY)
        return parse_flags(raw)
    meta = getattr(message, "metadata", None) or {}
    raw = meta.get(FLAGS_METADATA_KEY) if isinstance(meta, dict) else None
    try:
        return parse_flags(raw)
    except InvalidMessageFlags:
        return {}


def text_of(message: Any) -> str:
    """The concatenated text of a message (authored dict or ``UnifiedMessage``)."""
    content = message.get("content") if isinstance(message, dict) else getattr(message, "content", None)
    if isinstance(content, str):
        return content
    parts: list[str] = []
    for block in content or []:
        if isinstance(block, dict):
            if block.get("type", "text") in ("text", "input_text", "output_text"):
                text = block.get("text")
                if isinstance(text, str):
                    parts.append(text)
        else:
            text = getattr(block, "text", None)
            if isinstance(text, str) and getattr(block, "type", "text") in ("text", "input_text", "output_text"):
                parts.append(text)
    return "".join(parts)


def validate_message_flags(messages: Sequence[Any]) -> None:
    """The placement rules, over an authored message list (system included).

    * ``example`` — user or assistant messages only.
    * ``prefill`` — only the LAST message, only an assistant, and it must carry text.
    * ``cache_boundary`` — any message.
    """
    last = len(messages) - 1
    for index, message in enumerate(messages):
        flags = flags_of(message)
        if not flags:
            continue
        role = _role_of(message)
        if flags.get("example") and role not in ("user", "assistant"):
            raise InvalidMessageFlags(
                f"message {index} ({role}) is flagged as an example; only user and assistant "
                "messages can be examples"
            )
        if flags.get("prefill"):
            if role != "assistant":
                raise InvalidMessageFlags(
                    f"message {index} ({role}) is flagged prefill; only an assistant message can be a prefill"
                )
            if index != last:
                raise InvalidMessageFlags(
                    f"message {index} is flagged prefill but is not the last message; a prefill "
                    "must be the final assistant turn the reply continues from"
                )
            if not text_of(message).strip():
                raise InvalidMessageFlags(f"message {index} is flagged prefill but has no text to continue from")


@dataclass
class FlagPlan:
    """What the translator should send, and what the answer must be told."""

    wire_messages: list[Any]
    prefill_text: str | None = None
    prefill_mode: Literal["native", "convert", "drop"] | None = None
    notes: list[str] = field(default_factory=list)
    convert_instruction: str | None = None
    cache_boundaries: int = 0
    examples: int = 0
    #: The trailing prefill message itself (the live object), so the answer
    #: can retire it once the reply carries its text.
    prefill_message: Any = None


def resolve_compat_mode(raw: Any) -> CompatMode:
    value = raw.strip().lower() if isinstance(raw, str) else raw
    if value in COMPAT_MODES:
        return value  # type: ignore[return-value]
    return DEFAULT_COMPAT_MODE


def prefill_refusal_sentence(model_label: str) -> str:
    return (
        f"{model_label} cannot continue a reply from a prefill — the provider rejects a "
        "conversation that ends on an assistant message. Remove the Prefill flag, pick a "
        "model that supports prefill, or ask an admin to set message-flag compatibility to "
        "convert."
    )


def plan_message_flags(
    messages: Sequence[Any],
    *,
    supports_prefill: bool,
    cache_boundary_support: CacheBoundarySupport,
    model_label: str,
    mode: Any = DEFAULT_COMPAT_MODE,
) -> FlagPlan:
    """Decide the wire for one provider call. Pure: never mutates ``messages``.

    A prefill-flagged message that is NOT the last message was consumed by an
    earlier reply (which already carries its text) and is left off the wire.
    """
    compat = resolve_compat_mode(mode)
    wire: list[Any] = []
    plan = FlagPlan(wire_messages=wire)
    last = len(messages) - 1
    for index, message in enumerate(messages):
        flags = flags_of(message)
        if flags.get("example"):
            plan.examples += 1
        if flags.get("cache_boundary"):
            plan.cache_boundaries += 1
        if flags.get("prefill") and _role_of(message) == "assistant":
            if index != last:
                continue  # consumed — its text lives at the start of the reply
            text = text_of(message).rstrip()
            if not text:
                continue
            plan.prefill_message = message
            if supports_prefill:
                plan.prefill_text = text
                plan.prefill_mode = "native"
                wire.append(message)
                continue
            if compat == "refuse":
                raise MessageFlagRefusal(prefill_refusal_sentence(model_label), code="prefill_unsupported")
            plan.prefill_text = text
            plan.prefill_mode = compat
            if compat == "convert":
                plan.convert_instruction = (
                    "Begin your reply with exactly the following text, then continue it naturally "
                    f"(do not repeat or quote it separately):\n{text}"
                )
                plan.notes.append(
                    f"{model_label} cannot take a prefill, so it was asked to begin its reply with "
                    "the prefill text — asked for, not forced."
                )
            else:
                plan.notes.append(
                    f"{model_label} cannot take a prefill, so the prefill was not sent "
                    "(organization setting: drop)."
                )
            continue
        wire.append(message)

    if plan.cache_boundaries and cache_boundary_support != "breakpoint":
        why = {
            "automatic": "this provider caches repeated prompt prefixes automatically, so nothing extra is sent",
            "implicit": "this provider caches repeated prompt prefixes implicitly; explicit context caching is not used, so nothing extra is sent",
            "none": "this provider has no prompt caching, so nothing is sent",
        }[cache_boundary_support]
        plan.notes.append(f"Cache boundary on {model_label}: {why}.")
    return plan


def apply_prefill_to_reply(response_messages: Sequence[Any], plan: FlagPlan) -> dict[str, Any] | None:
    """Make the answer honest about its prefill; return the metadata recorded.

    native  → the provider returned only the continuation; the prefill text is
              prepended to the first text block so the stored and shown reply
              is the whole reply.
    convert → the model wrote the start itself; record whether it complied.
    drop    → record that the prefill was not sent.
    """
    if not plan.prefill_mode or plan.prefill_text is None:
        return None
    target = None
    for message in response_messages or []:
        if _role_of(message) == "assistant":
            target = message
            break
    record: dict[str, Any] = {"mode": plan.prefill_mode, "text": plan.prefill_text}
    if target is None:
        return record
    if plan.prefill_mode == "native":
        for block in getattr(target, "content", None) or []:
            text = getattr(block, "text", None)
            if isinstance(text, str) and getattr(block, "type", "text") == "text":
                block.text = plan.prefill_text + text
                break
        record["forced"] = True
        record["starts_with_prefill"] = True
    elif plan.prefill_mode == "convert":
        record["forced"] = False
        record["starts_with_prefill"] = text_of(target).lstrip().startswith(plan.prefill_text.strip())
    else:
        record["forced"] = False
        record["starts_with_prefill"] = text_of(target).lstrip().startswith(plan.prefill_text.strip())
    meta = getattr(target, "metadata", None)
    if isinstance(meta, dict):
        meta[PREFILL_RESULT_METADATA_KEY] = record
    # The prefill is CONSUMED: its text now lives at the start of the reply (or
    # was asked for / dropped). Hide the authored turn from the person — they
    # see the whole reply once. It stays VISIBLE TO THE MODEL on purpose: the
    # persisted window is numbered over model-visible messages, so hiding it
    # there would shift the reply off its reserved row (a stranded pending
    # assistant row, measured 2026-09-22). Replays never send it anyway: a
    # prefill that is not the last message is consumed (plan_message_flags).
    retired_meta = getattr(plan.prefill_message, "metadata", None)
    if isinstance(retired_meta, dict):
        retired_meta["is_visible_to_user"] = False
    return record


__all__ = [
    "CACHE_BOUNDARY_BY_WIRE",
    "COMPAT_MODES",
    "COMPAT_MODE_KNOB",
    "COMPAT_MODE_METADATA_KEY",
    "CONVERT_PREFILL_SLOT",
    "DEFAULT_COMPAT_MODE",
    "FLAGS_METADATA_KEY",
    "FLAG_KEYS",
    "FlagPlan",
    "InvalidMessageFlags",
    "MessageFlagRefusal",
    "MessageFlags",
    "PREFILL_RESULT_METADATA_KEY",
    "apply_prefill_to_reply",
    "flags_of",
    "parse_flags",
    "plan_message_flags",
    "prefill_refusal_sentence",
    "resolve_compat_mode",
    "text_of",
    "validate_message_flags",
]
