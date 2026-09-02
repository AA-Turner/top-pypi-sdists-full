"""Tool result dataclass (FR-003).

A ``ToolResult`` represents the outcome of a tool invocation — success
or failure — with structured fields for error categorization, timing,
and dry-run indication.
"""

from __future__ import annotations

import dataclasses
import json
from typing import Any


@dataclasses.dataclass(frozen=True)
class ToolResult:
    """Immutable result of a single tool invocation.

    Attributes:
        success: Whether the invocation completed without error.
        output: The tool's return value (any JSON-serializable data).
        error_type: Error category when ``success=False`` (e.g.
            ``"validation_error"``, ``"execution_error"``, ``"timeout"``).
        error_message: Human-readable error description.
        dry_run: Whether the invocation was skipped due to dry-run mode.
        duration_ms: Wall-clock execution time in milliseconds.
    """

    success: bool
    output: Any = None
    error_type: str | None = None
    error_message: str | None = None
    dry_run: bool = False
    duration_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dictionary suitable for JSON encoding."""
        return dataclasses.asdict(self)

    def to_json(self) -> str:
        """Serialize to a JSON string."""
        return json.dumps(self.to_dict(), default=str)
