"""Tests for IssueNode base model."""

import pytest
from pydantic import ValidationError

from agentic_devtools.epic_tree.models import IssueNode


class TestIssueNode:
    """Tests for the IssueNode Pydantic base model."""

    def test_construction_with_all_fields(self):
        """IssueNode can be constructed with all fields specified."""
        node = IssueNode(
            ref="epic-1",
            title="My Epic",
            body="Description here",
            labels=("epic", "automation"),
            issueType="Epic",
            order=1,
            blockedBy=("other-ref",),
            blocks=("downstream-ref",),
        )
        assert node.ref == "epic-1"
        assert node.title == "My Epic"
        assert node.body == "Description here"
        assert node.labels == ("epic", "automation")
        assert node.issueType == "Epic"
        assert node.order == 1
        assert node.blockedBy == ("other-ref",)
        assert node.blocks == ("downstream-ref",)

    def test_optional_fields_default_values(self):
        """Optional fields have correct defaults."""
        node = IssueNode(
            ref="node-1",
            title="Title",
            body="Body",
        )
        assert node.order is None
        assert node.blockedBy == ()
        assert node.blocks == ()
        assert node.labels is None
        assert node.issueType is None

    def test_frozen_immutability(self):
        """IssueNode instances are immutable (frozen=True)."""
        node = IssueNode(
            ref="node-1",
            title="Title",
            body="Body",
        )
        with pytest.raises(ValidationError):
            node.ref = "modified"  # type: ignore[misc]

    def test_construction_from_dict_with_model_validate(self):
        """IssueNode can be constructed from a dictionary via model_validate."""
        data = {
            "ref": "node-1",
            "title": "Title",
            "body": "Body",
            "labels": ["label-a", "label-b"],
            "issueType": "Feature",
            "order": 5,
            "blockedBy": ["dep-1"],
            "blocks": ["dep-2"],
        }
        node = IssueNode.model_validate(data)
        assert node.ref == "node-1"
        assert node.labels == ("label-a", "label-b")
        assert node.blockedBy == ("dep-1",)
        assert node.blocks == ("dep-2",)

    def test_ref_validation_rejects_invalid(self):
        """ref field rejects characters outside [a-zA-Z0-9_-]."""
        with pytest.raises(ValidationError):
            IssueNode(ref="invalid ref!", title="T", body="B")

    def test_title_validation_rejects_empty(self):
        """title field rejects empty string."""
        with pytest.raises(ValidationError):
            IssueNode(ref="valid-ref", title="", body="B")

    def test_order_validation_rejects_zero(self):
        """order field rejects 0 (must be >= 1)."""
        with pytest.raises(ValidationError):
            IssueNode(ref="valid-ref", title="T", body="B", order=0)

    def test_order_validation_rejects_negative(self):
        """order field rejects negative values."""
        with pytest.raises(ValidationError):
            IssueNode(ref="valid-ref", title="T", body="B", order=-1)

    def test_polymorphic_access(self):
        """A function accepting IssueNode can read all common fields from any concrete type."""
        from agentic_devtools.epic_tree.models import EpicNode, FeatureNode, SubtaskNode

        subtask = SubtaskNode(ref="s1", title="S", body="sb", labels=("x",), issueType="Subtask")
        feature = FeatureNode(ref="f1", title="F", body="fb", labels=("y",), issueType="Feature", subtasks=(subtask,))
        epic = EpicNode(ref="e1", title="E", body="eb", labels=("z",), issueType="Epic", features=(feature,))

        for node in (subtask, feature, epic):
            assert isinstance(node, IssueNode)
            assert node.ref
            assert node.title
            assert node.body is not None
