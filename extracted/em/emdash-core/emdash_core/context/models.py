"""Data models for the context provider system."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class ContextProviderSpec:
    """Specification for a context provider."""

    name: str
    description: str
    requires_graph: bool = True


@dataclass
class ContextItem:
    """A single context item extracted from code."""

    qualified_name: str
    entity_type: str  # 'Function', 'Class', 'File'
    description: Optional[str] = None
    file_path: Optional[str] = None
    score: float = 1.0
    touch_count: int = 1
    last_touched: Optional[datetime] = None
    neighbors: list[str] = field(default_factory=list)

    def __post_init__(self):
        if self.last_touched is None:
            object.__setattr__(self, "last_touched", datetime.now())


@dataclass
class SessionContext:
    """Context for a terminal session."""

    session_id: str
    terminal_id: str
    items: list[ContextItem] = field(default_factory=list)
    created_at: Optional[datetime] = None
    last_active: Optional[datetime] = None

    def __post_init__(self):
        now = datetime.now()
        if self.created_at is None:
            self.created_at = now
        if self.last_active is None:
            self.last_active = now
