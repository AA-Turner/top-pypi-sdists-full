"""Canonical ReasoningPlan shape.

Every FrameworkLifecycleBridge subclass implements
``extract_reasoning_plan(framework_handle) -> ReasoningPlan | None``. The
substrate merges the result into trace metadata so the platform's
agent_prompt / reasoning_plan consumers receive a consistent shape across
frameworks (LangGraph, CrewAI, Strands, etc.).

Backend consumers: ``trace.metadata.reasoning_plan`` (full plan) and
``trace.metadata.agent_prompt`` (lifted when the graph has a single static
agent prompt). See backend/src/monitor/judges/context_extractor.py.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ReasoningPlanNode:
    name: str
    agent_prompt: str | None = None


@dataclass
class ReasoningPlan:
    framework: str
    nodes: list[ReasoningPlanNode] = field(default_factory=list)
    edges: list[dict[str, str]] = field(default_factory=list)
    entry_point: str | None = None
    agent_prompt: str | None = None

    @property
    def node_count(self) -> int:
        return len(self.nodes)

    @property
    def edge_count(self) -> int:
        return len(self.edges)

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["node_count"] = self.node_count
        out["edge_count"] = self.edge_count
        return out
