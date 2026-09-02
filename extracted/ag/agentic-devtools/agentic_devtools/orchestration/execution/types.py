"""Core type definitions for the execution model.

Provides JSON-safe boundary types used across node updates, tool results,
and structured metadata. No external dependencies beyond the Python stdlib.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, TypeVar, Union

# ---------------------------------------------------------------------------
# JSONValue — recursive JSON-safe boundary type
# ---------------------------------------------------------------------------

JSONValue = Union[str, int, float, bool, None, list["JSONValue"], dict[str, "JSONValue"]]  # noqa: UP007
"""Recursive type alias representing any JSON-serialisable value.

Used at all public boundaries in the ``execution/`` package to ensure
node updates, tool results, and trace payloads remain serialisable.
"""

# ---------------------------------------------------------------------------
# TokenUsage — optional LLM cost metadata
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TokenUsage:
    """Token/cost metadata from an LLM invocation."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost_usd: float | None = None


# ---------------------------------------------------------------------------
# ReasoningResponse[T] — generic LLM response wrapper
# ---------------------------------------------------------------------------

T = TypeVar("T")


@dataclass(frozen=True)
class ReasoningResponse(Generic[T]):
    """Wrapper for an LLM provider response.

    Attributes:
        raw_text: Original provider output for traceability/debugging.
        parsed_output: Validated structured payload when schema parsing succeeds.
        tool_calls: Provider-declared tool invocations, if any.
        usage: Optional token/cost metadata.
    """

    raw_text: str
    parsed_output: T | None = None
    tool_calls: list[dict[str, JSONValue]] = field(default_factory=list)
    usage: TokenUsage | None = None
    model: str | None = None
    provider_type: str | None = None
    latency_ms: int | None = None
    finish_reason: str | None = None
