from enum import StrEnum
from typing import Any

from matrx_utils import vcprint


class FinishReason(StrEnum):
    """Unified finish reasons across all providers"""

    # Success cases
    STOP = "stop"
    MAX_TOKENS = "max_tokens"

    # Tool/function related
    TOOL_CALLS = "tool_calls"
    MALFORMED_FUNCTION_CALL = "malformed_function_call"
    UNEXPECTED_TOOL_CALL = "unexpected_tool_call"

    # Content filtering / Safety
    CONTENT_FILTER = "content_filter"
    SAFETY = "safety"
    RECITATION = "recitation"
    PROHIBITED_CONTENT = "prohibited_content"
    SPII = "spii"

    # Image generation specific
    IMAGE_SAFETY = "image_safety"
    IMAGE_PROHIBITED_CONTENT = "image_prohibited_content"
    NO_IMAGE = "no_image"
    IMAGE_RECITATION = "image_recitation"

    # Anthropic-specific
    REFUSAL = "refusal"
    MODEL_CONTEXT_WINDOW_EXCEEDED = "model_context_window_exceeded"

    # Other
    LANGUAGE = "language"
    BLOCKLIST = "blocklist"
    END_TURN = "end_turn"
    ERROR = "error"
    OTHER = "other"

    def is_success(self) -> bool:
        """Returns True if the model completed naturally with no truncation or errors."""
        return self in {
            self.STOP,
            self.TOOL_CALLS,
            self.END_TURN,
        }

    def is_truncated(self) -> bool:
        """Returns True if the response was cut short by a token limit.

        MAX_TOKENS means the model hit the output cap and stopped mid-response —
        this is NOT a success. The output is incomplete and the caller must be
        notified so the user isn't silently handed a truncated answer.
        """
        return self == self.MAX_TOKENS

    def is_retryable(self) -> bool:
        """Returns True if this error can be retried."""
        return self in {
            self.MALFORMED_FUNCTION_CALL,
            self.UNEXPECTED_TOOL_CALL,
        }

    def is_error(self) -> bool:
        """Returns True if this is a fatal error that should stop execution."""
        return self in {
            self.CONTENT_FILTER,
            self.SAFETY,
            self.RECITATION,
            self.PROHIBITED_CONTENT,
            self.SPII,
            self.IMAGE_SAFETY,
            self.IMAGE_PROHIBITED_CONTENT,
            self.NO_IMAGE,
            self.IMAGE_RECITATION,
            self.LANGUAGE,
            self.BLOCKLIST,
            self.ERROR,
            self.REFUSAL,
            self.MODEL_CONTEXT_WINDOW_EXCEEDED,
            # Retryable errors also count as errors (after retry exhaustion)
            self.MALFORMED_FUNCTION_CALL,
            self.UNEXPECTED_TOOL_CALL,
        }

    @classmethod
    def from_google(cls, google_reason: Any) -> "FinishReason":
        """Convert Google finish reason to unified format"""
        if not google_reason:
            return cls.STOP

        reason_str = str(google_reason).upper()
        if "." in reason_str:
            reason_str = reason_str.split(".")[-1]

        mapping = {
            "STOP": cls.STOP,
            "MAX_TOKENS": cls.MAX_TOKENS,
            "SAFETY": cls.SAFETY,
            "RECITATION": cls.RECITATION,
            "LANGUAGE": cls.LANGUAGE,
            "BLOCKLIST": cls.BLOCKLIST,
            "PROHIBITED_CONTENT": cls.PROHIBITED_CONTENT,
            "SPII": cls.SPII,
            "MALFORMED_FUNCTION_CALL": cls.MALFORMED_FUNCTION_CALL,
            "UNEXPECTED_TOOL_CALL": cls.UNEXPECTED_TOOL_CALL,
            "IMAGE_SAFETY": cls.IMAGE_SAFETY,
            "IMAGE_PROHIBITED_CONTENT": cls.IMAGE_PROHIBITED_CONTENT,
            "NO_IMAGE": cls.NO_IMAGE,
            "IMAGE_RECITATION": cls.IMAGE_RECITATION,
            "OTHER": cls.OTHER,
            "FINISH_REASON_UNSPECIFIED": cls.STOP,
        }
        return mapping.get(reason_str, cls.OTHER)

    @classmethod
    def from_anthropic(cls, stop_reason: str) -> "FinishReason":
        if stop_reason == "end_turn":
            return cls.STOP
        elif stop_reason == "max_tokens":
            return cls.MAX_TOKENS
        elif stop_reason == "tool_use":
            return cls.TOOL_CALLS
        elif stop_reason == "stop_sequence":
            return cls.STOP
        elif stop_reason == "refusal":
            return cls.REFUSAL
        elif stop_reason == "model_context_window_exceeded":
            return cls.MODEL_CONTEXT_WINDOW_EXCEEDED
        else:
            vcprint(stop_reason, "WARNING: Unknown Anthropic stop reason", color="yellow")
            return cls.OTHER

    @classmethod
    def to_anthropic(cls, finish_reason: "FinishReason") -> str:
        if finish_reason == cls.STOP:
            return "stop_sequence"
        elif finish_reason == cls.MAX_TOKENS:
            return "max_tokens"
        elif finish_reason == cls.TOOL_CALLS:
            return "tool_use"
        else:
            vcprint(
                finish_reason,
                "WARNING: Unknown Anthropic finish reason",
                color="yellow",
            )
            return "other_reason"


# ---------------------------------------------------------------------------
# Truncation — saying it out loud
#
# THE DEFECT THIS CLOSES (live, 2026-09-11, the Masterwork Conductor): a turn
# that was writing a large tool call hit the output ceiling at exactly its
# max_output_tokens. The provider returned stop_reason=max_tokens with an
# INCOMPLETE tool_use block, which the parser dropped — so the turn persisted
# as thinking + text with zero tool calls, the save never happened, and the
# person watching saw "Using tool workflow_author" and then nothing at all.
#
# Nothing fails silently. A turn that ran out of room says so IN the
# conversation, names the tool whose call died with it, and says plainly that
# nothing was saved — and the stored message carries a marker so the UI can
# badge it without re-deriving any of this.
# ---------------------------------------------------------------------------

#: Assistant-message metadata key stamped on a turn cut off by the output cap.
#: Value shape: {"reason": "max_tokens", "model": str, "max_output_tokens":
#: int | None, "interrupted_tool_calls": list[str]}.
TRUNCATION_METADATA_KEY = "truncation"


def interrupted_tool_names(raw_response: Any = None, messages: Any = None) -> list[str]:
    """Names of tool calls that were in flight when the turn was cut off.

    Looks at BOTH the parsed messages and the provider's raw content blocks on
    purpose: a tool call truncated mid-arguments is exactly the one the parser
    throws away, so the raw blocks are the only place it still exists. Names
    are de-duplicated, order preserved. Never raises — a diagnostic that
    crashes the turn it is describing would be worse than the silence.
    """
    found: list[str] = []

    def _add(name: Any) -> None:
        if isinstance(name, str) and name.strip() and name not in found:
            found.append(name)

    try:
        items = messages if isinstance(messages, list) else ([messages] if messages else [])
        for message in items:
            for block in getattr(message, "content", None) or []:
                if getattr(block, "type", None) in ("tool_call", "function_call"):
                    _add(getattr(block, "name", None))
    except Exception:  # noqa: BLE001 — best effort by contract
        pass

    try:
        blocks: Any = None
        if isinstance(raw_response, dict):
            blocks = raw_response.get("content")
            if blocks is None and isinstance(raw_response.get("message"), dict):
                blocks = raw_response["message"].get("content")
        for block in blocks or []:
            if not isinstance(block, dict):
                continue
            # Anthropic `tool_use`, OpenAI `function_call`/`tool_call`.
            if block.get("type") in ("tool_use", "tool_call", "function_call"):
                _add(block.get("name") or (block.get("function") or {}).get("name"))
    except Exception:  # noqa: BLE001
        pass

    return found


def truncation_notice(
    *,
    model: str | None = None,
    max_output_tokens: int | None = None,
    interrupted_tool_calls: list[str] | None = None,
) -> str:
    """The honest sentence a person reads when a turn ran out of room.

    Plain language, no codes, no paths — it is addressed to the person in the
    conversation, and it always says what happened to the work.
    """
    tools = [t for t in (interrupted_tool_calls or []) if t]
    if tools:
        named = tools[0] if len(tools) == 1 else ", ".join(tools)
        return (
            f"My reply ran out of room before I finished calling `{named}`, so that "
            "call never went through and nothing was saved. Nothing on your side is "
            "broken — I just need to do it in smaller pieces. Let me try again with "
            "a smaller change."
        )
    limit = f" (the limit is {max_output_tokens:,} tokens)" if max_output_tokens else ""
    return (
        f"My reply ran out of room{limit} and stopped part-way, so what you see above "
        "is incomplete. Ask me to continue and I'll pick up where it cut off."
    )


def truncation_marker(
    *,
    model: str | None = None,
    max_output_tokens: int | None = None,
    interrupted_tool_calls: list[str] | None = None,
) -> dict[str, Any]:
    """The metadata a truncated assistant message carries, so the UI can badge
    it without re-deriving anything."""
    return {
        "reason": str(FinishReason.MAX_TOKENS),
        "model": model or "unknown model",
        "max_output_tokens": max_output_tokens,
        "interrupted_tool_calls": [t for t in (interrupted_tool_calls or []) if t],
    }
