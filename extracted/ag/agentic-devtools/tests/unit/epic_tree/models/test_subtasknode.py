"""Tests for SubtaskNode model."""

import pytest
from pydantic import ValidationError

from agentic_devtools.epic_tree.models import IssueNode, SubtaskNode


class TestSubtaskNode:
    """Tests for the SubtaskNode Pydantic model."""

    def test_inherits_from_issuenode(self):
        """SubtaskNode is a subclass of IssueNode."""
        node = SubtaskNode(ref="s1", title="Subtask", body="Work", labels=("subtask",), issueType="Subtask")
        assert isinstance(node, IssueNode)

    def test_no_child_collections(self):
        """SubtaskNode has no child collection fields (subtasks/features)."""
        node = SubtaskNode(ref="s1", title="Subtask", body="Work")
        assert not hasattr(node, "subtasks")
        assert not hasattr(node, "features")

    def test_frozen_immutability(self):
        """SubtaskNode instances are immutable."""
        node = SubtaskNode(ref="s1", title="Subtask", body="Work")
        with pytest.raises(ValidationError):
            node.title = "Modified"  # type: ignore[misc]

    def test_model_dump_camelcase(self):
        """model_dump with by_alias=True produces camelCase keys."""
        node = SubtaskNode(
            ref="s1",
            title="T",
            body="B",
            labels=("a",),
            issueType="Subtask",
            order=1,
            blockedBy=("x",),
            blocks=("y",),
        )
        data = node.model_dump(by_alias=True, mode="json")
        assert "issueType" in data
        assert "blockedBy" in data
        assert "blocks" in data
        assert isinstance(data["labels"], list)
        assert isinstance(data["blockedBy"], list)
        assert isinstance(data["blocks"], list)
