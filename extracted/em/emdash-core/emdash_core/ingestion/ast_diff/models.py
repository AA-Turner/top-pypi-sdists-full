"""Data models for AST-based symbol diffs."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ChangeKind(str, Enum):
    """Kind of change detected for a symbol."""

    ADDED = "added"
    REMOVED = "removed"
    SIGNATURE_CHANGED = "signature_changed"
    BODY_CHANGED = "body_changed"
    RENAMED = "renamed"
    MOVED = "moved"


class SymbolKind(str, Enum):
    """Kind of code symbol."""

    FUNCTION = "function"
    CLASS = "class"


# Severity scores for each change kind
SEVERITY_MAP: dict[ChangeKind, float] = {
    ChangeKind.ADDED: 0.0,
    ChangeKind.REMOVED: 1.0,
    ChangeKind.SIGNATURE_CHANGED: 1.0,
    ChangeKind.BODY_CHANGED: 0.5,
    ChangeKind.RENAMED: 0.8,
    ChangeKind.MOVED: 0.6,
}


@dataclass
class SymbolChange:
    """A single symbol-level change between two refs."""

    symbol_kind: SymbolKind
    change_kind: ChangeKind
    qualified_name: str
    file_path: str
    old_qualified_name: Optional[str] = None
    old_file_path: Optional[str] = None
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    severity: float = 1.0
    details: dict = field(default_factory=dict)


@dataclass
class SymbolDiff:
    """Result of diffing symbols between two git refs."""

    base_ref: str
    head_ref: str
    changes: list[SymbolChange] = field(default_factory=list)
    files_analyzed: int = 0
    parse_errors: list[str] = field(default_factory=list)
