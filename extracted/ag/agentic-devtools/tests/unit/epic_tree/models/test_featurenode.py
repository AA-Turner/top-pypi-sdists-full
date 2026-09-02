"""Tests for FeatureNode model."""

import pytest
from pydantic import ValidationError

from agentic_devtools.epic_tree.models import FeatureNode, IssueNode, SubtaskNode


class TestFeatureNode:
    """Tests for the FeatureNode Pydantic model."""

    def test_inherits_from_issuenode(self):
        """FeatureNode is a subclass of IssueNode."""
        node = FeatureNode(ref="f1", title="Feature", body="Desc", subtasks=())
        assert isinstance(node, IssueNode)

    def test_subtasks_preserves_order(self):
        """subtasks tuple preserves declaration order from source data."""
        s1 = SubtaskNode(ref="s1", title="First", body="")
        s2 = SubtaskNode(ref="s2", title="Second", body="")
        s3 = SubtaskNode(ref="s3", title="Third", body="")
        node = FeatureNode(ref="f1", title="Feature", body="", subtasks=(s1, s2, s3))
        assert node.subtasks[0].ref == "s1"
        assert node.subtasks[1].ref == "s2"
        assert node.subtasks[2].ref == "s3"

    def test_empty_subtasks(self):
        """FeatureNode can have an empty subtasks tuple."""
        node = FeatureNode(ref="f1", title="Feature", body="", subtasks=())
        assert node.subtasks == ()

    def test_frozen_immutability(self):
        """FeatureNode instances are immutable."""
        node = FeatureNode(ref="f1", title="Feature", body="", subtasks=())
        with pytest.raises(ValidationError):
            node.ref = "modified"  # type: ignore[misc]

    def test_model_validate_from_dict(self):
        """FeatureNode can be constructed from nested dict via model_validate."""
        data = {
            "ref": "f1",
            "title": "Feature",
            "body": "Body",
            "labels": ["feature"],
            "issueType": "Feature",
            "subtasks": [
                {
                    "ref": "s1",
                    "title": "Subtask 1",
                    "body": "Work",
                    "labels": ["subtask"],
                    "issueType": "Subtask",
                }
            ],
        }
        node = FeatureNode.model_validate(data)
        assert node.ref == "f1"
        assert len(node.subtasks) == 1
        assert node.subtasks[0].ref == "s1"
        assert isinstance(node.subtasks[0], SubtaskNode)

    def test_model_dump_camelcase(self):
        """model_dump with by_alias=True produces camelCase keys with lists."""
        node = FeatureNode(
            ref="f1",
            title="F",
            body="B",
            labels=("a",),
            issueType="Feature",
            subtasks=(SubtaskNode(ref="s1", title="S", body="", labels=(), issueType="Subtask"),),
        )
        data = node.model_dump(by_alias=True, mode="json")
        assert "issueType" in data
        assert "subtasks" in data
        assert isinstance(data["subtasks"], list)
        assert "issueType" in data["subtasks"][0]
