"""LLM call logging with configurable verbosity."""

from __future__ import annotations

import logging
from enum import Enum
from typing import Any

from agentic_devtools.orchestration.llm.types import LLMResponse

logger = logging.getLogger("agentic_devtools.orchestration.llm")


def _get_message_field(message: Any, field: str) -> Any:
    if isinstance(message, dict):
        return message.get(field)
    return getattr(message, field, None)


def _should_exclude_from_preview(message: Any) -> bool:
    role = _get_message_field(message, "role")
    return not isinstance(role, str) or role.lower() == "system"


class LogLevel(str, Enum):
    """Configurable log verbosity levels for LLM calls."""

    NONE = "none"  # No logging
    MINIMAL = "minimal"  # Model, tokens, latency, status only
    STANDARD = "standard"  # Above + prompt summary (first 100 chars)
    VERBOSE = "verbose"  # Full prompt and response content


class CallLogger:
    """Configurable logger for LLM calls.

    Production-safe by default: logs no prompt/response content at MINIMAL level,
    only a short prompt preview at STANDARD level, and full content at VERBOSE level.
    """

    def __init__(self, level: LogLevel = LogLevel.MINIMAL) -> None:
        self._level = level

    @property
    def level(self) -> LogLevel:
        """Return current log level."""
        return self._level

    def log_call(
        self,
        *,
        model: str,
        node_type: str = "",
        messages: list[Any] | None = None,
        response: LLMResponse | None = None,
        error: Exception | None = None,
        latency_ms: int | None = None,
    ) -> None:
        """Log an LLM call with configured verbosity.

        Args:
            model: Model identifier.
            node_type: The node type that made the call.
            messages: Input messages (logged only at VERBOSE level).
            response: LLM response (logged based on level).
            error: Error if the call failed.
            latency_ms: Call latency in milliseconds.
        """
        if self._level == LogLevel.NONE:
            return

        # Build log entry
        entry: dict[str, Any] = {
            "model": model,
            "node_type": node_type,
            "status": "error" if error else "success",
        }

        if latency_ms is not None:
            entry["latency_ms"] = latency_ms

        if response and response.usage:
            entry["input_tokens"] = response.usage.input_tokens
            entry["output_tokens"] = response.usage.output_tokens
            entry["total_tokens"] = response.usage.total_tokens
            if response.usage.estimated_cost_usd is not None:
                entry["cost_usd"] = response.usage.estimated_cost_usd

        if error:
            entry["error"] = str(error)

        if self._level in (LogLevel.STANDARD, LogLevel.VERBOSE) and messages:
            # Log prompt summary — best-effort; never raise due to unexpected message shape.
            # Skip system messages for the preview to avoid logging potentially sensitive
            # internal instructions.
            try:
                preview_msg = next(
                    (m for m in messages if not _should_exclude_from_preview(m)),
                    None,
                )
                if preview_msg is not None:
                    first_content = _get_message_field(preview_msg, "content") or ""
                    entry["prompt_preview"] = first_content[:100] + ("..." if len(first_content) > 100 else "")
            except (AttributeError, TypeError):
                pass

        if self._level == LogLevel.VERBOSE:
            try:
                if messages:
                    entry["messages"] = [
                        {"role": _get_message_field(m, "role"), "content": _get_message_field(m, "content")}
                        for m in messages
                    ]
            except (AttributeError, TypeError):
                pass
            if response:
                entry["response_text"] = response.text

        # Log at appropriate level
        if error:
            logger.warning("LLM call failed: %s", entry)
        else:
            logger.info("LLM call: %s", entry)


def log_llm_call(
    *,
    model: str,
    node_type: str = "",
    messages: list[Any] | None = None,
    response: LLMResponse | None = None,
    error: Exception | None = None,
    latency_ms: int | None = None,
    level: LogLevel = LogLevel.MINIMAL,
) -> None:
    """Convenience function to log an LLM call."""
    call_logger = CallLogger(level=level)
    call_logger.log_call(
        model=model,
        node_type=node_type,
        messages=messages,
        response=response,
        error=error,
        latency_ms=latency_ms,
    )
