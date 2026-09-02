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
            vcprint(
                stop_reason, "WARNING: Unknown Anthropic stop reason", color="yellow"
            )
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
