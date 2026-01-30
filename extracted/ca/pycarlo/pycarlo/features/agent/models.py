from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class AgentSpanFilter:
    """Filter for agent spans by agent, workflow, task, or span name."""

    agent: Optional[str] = None
    workflow: Optional[str] = None
    task: Optional[str] = None
    span_name: Optional[str] = None

    def to_dict(self) -> dict[str, dict[str, str]]:
        """Convert to GraphQL input format."""
        result: dict[str, dict[str, str]] = {}
        if self.agent is not None:
            result["agent"] = {"value": self.agent}
        if self.workflow is not None:
            result["workflow"] = {"value": self.workflow}
        if self.task is not None:
            result["task"] = {"value": self.task}
        if self.span_name is not None:
            result["spanName"] = {"value": self.span_name}
        return result


@dataclass
class SpanAttributeFilter:
    """Filter spans by attribute map key-value pairs.

    Used to filter agent spans by custom attributes stored in the attr_map column.
    Example: key="montecarlo.ci_build_id", value="build-123"
    """

    key: str
    value: str

    def to_dict(self) -> dict[str, str]:
        """Convert to GraphQL input format."""
        return {"key": self.key, "value": self.value}


@dataclass
class SpanQueryResult:
    """Result from querying agent spans via getAgentSpanSampleV2."""

    columns: list[str]
    rows: list[list[Any]]
    has_error: bool
    error: Optional[str] = None

    @property
    def row_count(self) -> int:
        """Returns the number of rows in the result."""
        return len(self.rows)
