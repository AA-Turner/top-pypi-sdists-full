"""Pydantic v2 models for the epic-tree document structure.

Provides typed, immutable models that mirror the epic-tree JSON Schema:
- :class:`IssueNode` — shared base with common fields
- :class:`SubtaskNode` — leaf-level work item (no children)
- :class:`FeatureNode` — mid-level node with subtasks
- :class:`EpicNode` — root-level epic node with features
- :class:`EpicTree` — document root with schema version and epic node
"""

from __future__ import annotations

import re

from pydantic import BaseModel, ConfigDict, field_validator

_REF_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")


class IssueNode(BaseModel):
    """Shared base model for all epic-tree node types.

    Provides the common fields present at every level of the tree:
    ref, title, body, labels, issueType, and optional order/blockedBy/blocks.
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True, extra="forbid")

    ref: str
    title: str
    body: str
    labels: tuple[str, ...] | None = None
    issueType: str | None = None
    order: int | None = None
    blockedBy: tuple[str, ...] = ()
    blocks: tuple[str, ...] = ()

    @field_validator("ref")
    @classmethod
    def _validate_ref(cls, v: str) -> str:
        if not _REF_PATTERN.match(v):
            msg = f"ref must match pattern ^[a-zA-Z0-9_-]+$, got '{v}'"
            raise ValueError(msg)
        return v

    @field_validator("title")
    @classmethod
    def _validate_title(cls, v: str) -> str:
        if not v:
            msg = "title must not be empty"
            raise ValueError(msg)
        return v

    @field_validator("order")
    @classmethod
    def _validate_order(cls, v: int | None) -> int | None:
        if v is not None and v < 1:
            msg = "order must be a positive integer (>= 1)"
            raise ValueError(msg)
        return v


class SubtaskNode(IssueNode):
    """Leaf-level model representing an atomic unit of work.

    Inherits all fields from :class:`IssueNode` with no additional
    child collection fields.
    """


class FeatureNode(IssueNode):
    """Mid-level model representing a capability or deliverable within an epic.

    Inherits from :class:`IssueNode` and adds an ordered tuple of subtasks.
    """

    subtasks: tuple[SubtaskNode, ...]


class EpicNode(IssueNode):
    """Root-level epic node containing features.

    Inherits from :class:`IssueNode` and adds an ordered tuple of features.
    """

    features: tuple[FeatureNode, ...]


class EpicTree(BaseModel):
    """Document root model for an epic-tree JSON file.

    Contains the schema version and the root epic node.
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True, extra="forbid")

    schemaVersion: str
    epic: EpicNode
