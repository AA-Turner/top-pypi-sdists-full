"""Tool definition dataclass (FR-002).

A ``ToolDefinition`` describes a registered tool's metadata — name,
description, category, input/output schemas, mutating flag, timeout,
and thread-safety.  Instances are frozen (immutable after creation).
"""

from __future__ import annotations

import dataclasses
from typing import Any


@dataclasses.dataclass(frozen=True)
class ToolDefinition:
    """Immutable metadata descriptor for a registered tool.

    Attributes:
        name: Unique tool identifier (e.g. ``"jira_add_comment"``).
        description: Human-readable description for LLM consumption.
        category: Domain category (git, jira, azure_devops, github,
            filesystem, testing, state).
        input_schema: JSON Schema dict describing accepted parameters.
        output_schema: JSON Schema dict describing the output structure.
        mutating: Whether this tool performs side effects.
        timeout_seconds: Maximum execution time before cooperative timeout.
        thread_safe: Whether concurrent invocations are safe.
    """

    name: str
    description: str
    category: str
    input_schema: dict[str, Any]
    output_schema: dict[str, Any] = dataclasses.field(default_factory=lambda: {"type": "object"})
    mutating: bool = False
    timeout_seconds: float = 30.0
    thread_safe: bool = True

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dictionary suitable for JSON encoding."""
        return dataclasses.asdict(self)
