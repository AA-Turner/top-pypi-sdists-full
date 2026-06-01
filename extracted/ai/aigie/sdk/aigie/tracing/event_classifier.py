"""Framework-agnostic event classifier.

Each framework binding implements ``FrameworkEventClassifier`` (exposed
via its adapter's ``event_classifier()`` method) to map raw framework
callback events into a canonical ``EventKind`` so emission dispatches
uniformly. Filter rules become pure functions of the event, separate
from emission logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class EventKind(Enum):
    DROP = "drop"
    CHAIN = "chain"
    WORKFLOW_ROOT = "workflow_root"
    SUBGRAPH_WORKFLOW = "subgraph_workflow"
    LLM = "llm"
    TOOL = "tool"


@dataclass(frozen=True)
class FrameworkEvent:
    """Raw event surface common to every framework binding's classifier."""

    name: str
    parent_run_id: str | None
    framework_metadata: dict = field(default_factory=dict)
    tags: tuple[str, ...] = ()


class FrameworkEventClassifier(ABC):
    """Every framework binding MUST provide one of these via its adapter's
    ``event_classifier()`` method. Pure functions only — no I/O."""

    @abstractmethod
    def classify_chain_event(self, event: FrameworkEvent) -> EventKind:
        """Classify an on_chain_start-equivalent event."""

    @abstractmethod
    def classify_llm_event(self, event: FrameworkEvent) -> EventKind:
        """Classify an on_llm_start-equivalent event."""

    @abstractmethod
    def classify_tool_event(self, event: FrameworkEvent) -> EventKind:
        """Classify an on_tool_start-equivalent event."""
