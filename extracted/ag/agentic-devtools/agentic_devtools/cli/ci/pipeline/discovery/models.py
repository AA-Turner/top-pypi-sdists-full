"""Discovery models — outcome enum and attempt diagnostics dataclass."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class DiscoveryOutcome(Enum):
    """Result classification for a single discovery strategy attempt."""

    SUCCESS = "success"
    EMPTY = "empty"
    ERROR = "error"
    ANCHORED_NO_REPLACEMENT = "anchored_no_replacement"


@dataclass
class DiscoveryAttempt:
    """Diagnostic record for a single discovery strategy execution.

    Attributes:
        method: Name of the strategy (e.g., "graphql", "rest-rederivation", "html-scrape").
        outcome: Classification of the attempt result.
        suggestion_count: Number of suggestions discovered (0 on failure).
        duration_ms: Wall-clock duration of the attempt in milliseconds.
        http_status: Best-effort HTTP status code (0 when not applicable).
        error_message: Raw error description, typically ``str(exc)`` (empty on success).
        details: Strategy-specific key/value metadata (e.g., reason for EMPTY, parsed
            block counts).  Empty dict when not populated.
    """

    method: str
    outcome: DiscoveryOutcome
    suggestion_count: int = 0
    duration_ms: int = 0
    http_status: int = 0
    error_message: str = ""
    details: dict = field(default_factory=dict)
