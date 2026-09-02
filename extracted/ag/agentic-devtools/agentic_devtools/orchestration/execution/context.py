"""Execution context container — dependency injection for node factories.

Bundles the three protocol dependencies every node factory needs, plus
optional configuration such as retry limits and model hints.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .protocols import ReasoningProvider, ToolRegistry, TraceEmitter
from .types import JSONValue


@dataclass(frozen=True)
class ExecutionContext:
    """Immutable container injected into node factories.

    Attributes:
        reasoning: LLM-facing provider for structured reasoning.
        tools: Tool registry for all side effects and data reads.
        tracer: Observability sink for trace events.
        config: Arbitrary JSON-safe configuration hints (model overrides,
            retry limits, timeouts, etc.).
    """

    reasoning: ReasoningProvider
    tools: ToolRegistry
    tracer: TraceEmitter
    config: dict[str, JSONValue] = field(default_factory=dict)
