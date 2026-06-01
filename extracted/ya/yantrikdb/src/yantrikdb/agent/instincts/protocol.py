"""Protocol definitions for instincts, urges, and companion state."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Protocol, runtime_checkable


@dataclass
class UrgeSpec:
    """Output of an instinct evaluation — a desire to say or do something."""

    instinct_name: str
    reason: str
    urgency: float  # 0.0 to 1.0
    suggested_message: str = ""
    action: Optional[str] = None
    context: dict = field(default_factory=dict)
    cooldown_key: str = ""


@dataclass
class CompanionState:
    """Read-only snapshot of companion state, passed to instincts."""

    last_interaction_ts: float
    current_ts: float
    session_active: bool
    conversation_turn_count: int
    recent_valence_avg: Optional[float] = None
    pending_triggers: list[dict] = field(default_factory=list)
    active_patterns: list[dict] = field(default_factory=list)
    open_conflicts_count: int = 0
    memory_count: int = 0
    config_user_name: str = "User"


@runtime_checkable
class Instinct(Protocol):
    """Protocol that all instincts must implement."""

    name: str
    description: str

    def evaluate(self, state: CompanionState) -> list[UrgeSpec]:
        """Periodic evaluation during background tick. Return urge specs."""
        ...

    def on_interaction(self, state: CompanionState, user_text: str) -> list[UrgeSpec]:
        """Lightweight check on every user interaction. Return urge specs."""
        ...
