from dataclasses import dataclass
from typing import Literal

MarkerSeverity = Literal["error", "warning", "info", "hint"]


@dataclass
class CodeMarker:
    """
    Represents a code marker for inline editor feedback.

    Attributes:
        line: Line number where the marker starts (1-based)
        column: Column number where the marker starts (1-based)
        until_line: Line number where the marker ends (1-based)
        until_column: Column number where the marker ends (1-based)
        message: Human-readable description of the issue
        severity: Severity level of the marker
        source: Identifier for the provider that created this marker
    """

    line: int
    column: int
    until_line: int
    until_column: int
    message: str
    severity: MarkerSeverity
    source: str  # "syntax", "requirements", etc.

    def to_dict(self) -> dict:
        return {
            "line": self.line,
            "column": self.column,
            "until_line": self.until_line,
            "until_column": self.until_column,
            "message": self.message,
            "severity": self.severity,
            "source": self.source,
        }
