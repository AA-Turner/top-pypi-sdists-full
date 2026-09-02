"""Core data models for hierarchy infrastructure.

Defines the foundational types used throughout the hierarchy package:
``HierarchyLevel`` enum, ``HierarchyMetadata`` dataclass for hierarchy.yml
content, ``CascadeEvent`` for cascade trigger tracking, and ``ArtifactProfile``
for level-aware artifact depth configuration.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class HierarchyLevel(Enum):
    """Three-level hierarchy classification with standalone fallback.

    EPIC, FEATURE, and TASK are the three hierarchical levels required by FR-002.
    STANDALONE is a non-hierarchical classification for existing flat specs that
    do not participate in any parent/child relationship (NFR-001 backward compat).
    """

    EPIC = "epic"
    FEATURE = "feature"
    TASK = "task"
    STANDALONE = "standalone"


class CascadeDirection(Enum):
    """Direction of a cascade trigger event."""

    PARENT_TO_CHILD = "parent_to_child"
    SIBLING_TO_SIBLING = "sibling_to_sibling"


@dataclass
class ChildInfo:
    """A child entry in hierarchy metadata.

    Attributes:
        number: GitHub issue number.
        title: Human-readable issue title.
        order: Optional ordering position for cascade sequencing. Parsed from
            ``children`` entries in hierarchy.yml when present, and left as
            ``None`` for older hierarchy files or programmatic construction.
    """

    number: int
    title: str
    order: int | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a dict."""
        result: dict[str, Any] = {"number": self.number, "title": self.title}
        if self.order is not None:
            result["order"] = self.order
        return result


@dataclass
class HierarchyMetadata:
    """Hierarchy metadata stored in hierarchy.yml at each spec directory level.

    Attributes:
        level: The hierarchy level classification.
        parent: Parent issue number (None for top-level epics / standalone).
        children: Ordered list of child entries.
        informational_children: Children beyond the depth cap (FR-009).
    """

    level: HierarchyLevel
    parent: int | None = None
    children: list[ChildInfo] = field(default_factory=list)
    informational_children: list[ChildInfo] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a dict suitable for YAML output."""
        return {
            "level": self.level.value,
            "parent": self.parent,
            "children": [c.to_dict() for c in self.children],
            "informational_children": [c.to_dict() for c in self.informational_children],
        }


@dataclass
class CascadeEvent:
    """Represents a cascade trigger event between issues.

    Attributes:
        source_issue: The issue number that completed its phase.
        target_issue: The issue number to be triggered next.
        direction: Whether this is parent→child or sibling→sibling.
        skipped_issues: Issues skipped during cascade (closed, skip label, etc.).
    """

    source_issue: int
    target_issue: int
    direction: CascadeDirection
    skipped_issues: list[int] = field(default_factory=list)


@dataclass
class ArtifactProfile:
    """Level-aware artifact depth configuration.

    Defines which spec artifacts are included/excluded for each hierarchy level,
    and what context is inherited from parent specs.

    Attributes:
        level: The hierarchy level this profile applies to.
        included_artifacts: Artifacts to generate (e.g., ["spec.md", "plan.md"]).
        excluded_artifacts: Artifacts to skip (e.g., ["tasks.md"] for epics).
        inherited_context: Parent artifacts to inject (e.g., ["spec.md", "plan.md"] for tasks).
    """

    level: HierarchyLevel
    included_artifacts: list[str] = field(default_factory=list)
    excluded_artifacts: list[str] = field(default_factory=list)
    inherited_context: list[str] = field(default_factory=list)
