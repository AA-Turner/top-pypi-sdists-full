"""Data models for Pass G — Code Reference Cross-Referencing."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ReferenceKind(Enum):
    """Classification of a code reference extracted from a plan (FR-001, FR-007)."""

    FILE_PATH = "file_path"
    MODULE_PATH = "module_path"
    CLASS_NAME = "class_name"
    FUNCTION_NAME = "function_name"
    METHOD_NAME = "method_name"
    CLI_COMMAND = "cli_command"
    UNCLASSIFIED = "unclassified"


@dataclass
class Reference:
    """A code reference extracted from plan text (FR-001, FR-004)."""

    text: str
    kind: ReferenceKind
    plan_location: str
    context_sentence: str
    occurrence_index: int = 0

    def __post_init__(self) -> None:
        """Validate constructor arguments for public API safety."""
        if not isinstance(self.occurrence_index, int) or isinstance(self.occurrence_index, bool):
            raise ValueError(f"occurrence_index must be a non-negative integer, got {self.occurrence_index!r}")
        if self.occurrence_index < 0:
            raise ValueError(f"occurrence_index must be a non-negative integer, got {self.occurrence_index!r}")


class MatchStatus(Enum):
    """Result of matching a reference against the repository inventory (FR-003)."""

    MATCHED = "matched"
    INVALID = "invalid"
    AMBIGUOUS = "ambiguous"
    PARTIAL = "partial"
    SKIPPED = "skipped"
    NEW_SYMBOL = "new_symbol"


@dataclass
class Candidate:
    """A potential match suggestion for an unresolved reference (FR-008)."""

    symbol_name: str
    file_path: str
    similarity_score: float
    kind: ReferenceKind


@dataclass
class Finding:
    """Complete result for a single reference classification (FR-013, FR-014)."""

    reference: Reference
    status: MatchStatus
    candidates: list[Candidate] = field(default_factory=list)
    confidence_level: str = ""
    explanation: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable dict for stable output (FR-013, FR-016)."""
        return {
            "reference": {
                "text": self.reference.text,
                "kind": self.reference.kind.value,
                "plan_location": self.reference.plan_location,
                "context_sentence": self.reference.context_sentence,
            },
            "status": self.status.value,
            "candidates": [
                {
                    "symbol_name": c.symbol_name,
                    "file_path": c.file_path,
                    "similarity_score": c.similarity_score,
                    "kind": c.kind.value,
                }
                for c in self.candidates
            ],
            "confidence_level": self.confidence_level,
            "explanation": self.explanation,
        }
