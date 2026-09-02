"""Tests for EpicTree model."""

import pytest
from pydantic import ValidationError

from agentic_devtools.epic_tree.models import EpicNode, EpicTree, FeatureNode, IssueNode, SubtaskNode


class TestEpicTree:
    """Tests for the EpicTree Pydantic model (document root)."""

    def test_document_root_structure(self):
        """EpicTree has schemaVersion and epic fields."""
        epic = EpicNode(ref="e1", title="Epic", body="Desc", features=())
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        assert tree.schemaVersion == "1.0"
        assert tree.epic.ref == "e1"

    def test_epic_node_inherits_from_issuenode(self):
        """EpicNode is a subclass of IssueNode."""
        epic = EpicNode(ref="e1", title="Epic", body="Desc", features=())
        assert isinstance(epic, IssueNode)

    def test_schema_version_field(self):
        """EpicTree exposes schemaVersion field."""
        epic = EpicNode(ref="e1", title="Epic", body="Desc", features=())
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        assert tree.schemaVersion == "1.0"

    def test_features_preserves_order(self):
        """features tuple preserves declaration order."""
        f1 = FeatureNode(ref="f1", title="First", body="", subtasks=())
        f2 = FeatureNode(ref="f2", title="Second", body="", subtasks=())
        f3 = FeatureNode(ref="f3", title="Third", body="", subtasks=())
        epic = EpicNode(ref="e1", title="Epic", body="", features=(f1, f2, f3))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        assert tree.epic.features[0].ref == "f1"
        assert tree.epic.features[1].ref == "f2"
        assert tree.epic.features[2].ref == "f3"

    def test_frozen_immutability(self):
        """EpicTree instances are immutable."""
        epic = EpicNode(ref="e1", title="Epic", body="", features=())
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        with pytest.raises(ValidationError):
            tree.schemaVersion = "2.0"  # type: ignore[misc]

    def test_model_validate_from_fixture_dict(self):
        """EpicTree can be constructed from a full fixture dict via model_validate."""
        data = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "epic-standardize-creation",
                "title": "Standardize and automate epic creation",
                "body": "An epic-creation agent runs a defined interview.",
                "labels": ["epic", "automation"],
                "issueType": "Epic",
                "order": 1,
                "blockedBy": [],
                "blocks": ["feature-schema-validation"],
                "features": [
                    {
                        "ref": "feature-schema-validation",
                        "title": "Epic Tree Schema & Validation",
                        "body": "The foundation.",
                        "labels": ["feature", "schema"],
                        "issueType": "Feature",
                        "order": 1,
                        "blockedBy": ["epic-standardize-creation"],
                        "blocks": ["subtask-author-schema"],
                        "subtasks": [
                            {
                                "ref": "subtask-author-schema",
                                "title": "Author the versioned JSON Schema",
                                "body": "Define the schema.",
                                "labels": ["subtask", "schema"],
                                "issueType": "Subtask",
                                "order": 1,
                                "blockedBy": ["feature-schema-validation"],
                                "blocks": [],
                            },
                            {
                                "ref": "subtask-pydantic-models",
                                "title": "Create Pydantic models",
                                "body": "Mirror the JSON Schema.",
                                "labels": ["subtask", "models"],
                                "issueType": "Subtask",
                                "order": 2,
                                "blockedBy": ["subtask-author-schema"],
                                "blocks": [],
                            },
                        ],
                    },
                    {
                        "ref": "feature-submission",
                        "title": "Provider Submission",
                        "body": "Submit the epic tree.",
                        "labels": ["feature", "submission"],
                        "issueType": "Feature",
                        "order": 2,
                        "blockedBy": ["feature-schema-validation"],
                        "blocks": [],
                        "subtasks": [],
                    },
                ],
            },
        }
        tree = EpicTree.model_validate(data)
        assert tree.schemaVersion == "1.0"
        assert tree.epic.ref == "epic-standardize-creation"
        assert len(tree.epic.features) == 2
        assert tree.epic.features[0].ref == "feature-schema-validation"
        assert tree.epic.features[1].ref == "feature-submission"
        assert len(tree.epic.features[0].subtasks) == 2
        assert tree.epic.features[0].subtasks[0].ref == "subtask-author-schema"
        assert tree.epic.features[0].subtasks[1].ref == "subtask-pydantic-models"
        assert tree.epic.features[1].subtasks == ()

    def test_model_dump_structure(self):
        """model_dump produces nested structure with epic wrapper."""
        epic = EpicNode(
            ref="e1",
            title="E",
            body="B",
            labels=("l",),
            issueType="Epic",
            features=(
                FeatureNode(
                    ref="f1",
                    title="F",
                    body="FB",
                    labels=(),
                    issueType="Feature",
                    subtasks=(SubtaskNode(ref="s1", title="S", body="SB", labels=(), issueType="Subtask"),),
                ),
            ),
        )
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        data = tree.model_dump(by_alias=True, mode="json")
        # Root level
        assert "schemaVersion" in data
        assert "epic" in data
        # Epic level
        epic_data = data["epic"]
        assert "issueType" in epic_data
        assert "blockedBy" in epic_data
        assert "blocks" in epic_data
        # Feature level
        feat = epic_data["features"][0]
        assert "issueType" in feat
        # Subtask level
        sub = feat["subtasks"][0]
        assert "issueType" in sub

    def test_optional_labels_and_issuetype(self):
        """labels and issueType are optional (None by default)."""
        epic = EpicNode(ref="e1", title="Epic", body="", features=())
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        assert tree.epic.labels is None
        assert tree.epic.issueType is None

    def test_round_trip_serialization(self):
        """Parsing serialized JSON produces structurally identical model."""
        data = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "",
                "labels": ["epic"],
                "issueType": "Epic",
                "features": [
                    {
                        "ref": "f1",
                        "title": "Feature",
                        "body": "body",
                        "labels": ["feature"],
                        "issueType": "Feature",
                        "subtasks": [],
                    }
                ],
            },
        }
        tree = EpicTree.model_validate(data)
        dumped = tree.model_dump(by_alias=True, mode="json")
        tree2 = EpicTree.model_validate(dumped)
        assert tree == tree2
