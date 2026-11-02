"""Tests for normalize_tree function."""

from agentic_devtools.epic_tree.config import EpicTreeConfig
from agentic_devtools.epic_tree.normalizer import normalize_tree


class TestNormalizeTree:
    """Tests for depth-aware auto-derivation of issueType and labels."""

    def test_auto_derives_issue_type_from_depth(self):
        """Missing issueType is derived from depth using config defaults."""
        config = EpicTreeConfig()
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [
                    {
                        "ref": "f1",
                        "title": "Feature",
                        "body": "Body",
                        "subtasks": [
                            {"ref": "s1", "title": "Subtask", "body": "Body"},
                        ],
                    }
                ],
            },
        }
        result = normalize_tree(doc, config)
        assert result.document["epic"]["issueType"] == "Epic"
        assert result.document["epic"]["features"][0]["issueType"] == "Feature"
        assert result.document["epic"]["features"][0]["subtasks"][0]["issueType"] == "Subtask"

    def test_auto_derives_labels_from_depth(self):
        """Missing labels are derived from depth using config defaults."""
        config = EpicTreeConfig()
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [],
            },
        }
        result = normalize_tree(doc, config)
        assert result.document["epic"]["labels"] == ["epic"]

    def test_preserves_explicit_values(self):
        """Explicit issueType and labels are not overwritten."""
        config = EpicTreeConfig()
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "issueType": "CustomType",
                "labels": ["custom"],
                "features": [],
            },
        }
        result = normalize_tree(doc, config)
        assert result.document["epic"]["issueType"] == "CustomType"
        assert result.document["epic"]["labels"] == ["custom"]

    def test_does_not_mutate_input(self):
        """normalize_tree returns a new dict without mutating the input."""
        config = EpicTreeConfig()
        doc = {
            "schemaVersion": "1.0",
            "epic": {"ref": "e1", "title": "E", "body": "", "features": []},
        }
        import copy

        original = copy.deepcopy(doc)
        normalize_tree(doc, config)
        assert doc == original

    def test_config_override_defaults(self):
        """Config-provided default_issue_types overrides built-in defaults."""
        config = EpicTreeConfig(
            default_issue_types={0: "Initiative", 1: "Story", 2: "Task"},
            default_labels={0: ["initiative"], 1: ["story"], 2: ["task"]},
        )
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [
                    {
                        "ref": "f1",
                        "title": "Feature",
                        "body": "Body",
                        "subtasks": [
                            {"ref": "s1", "title": "Subtask", "body": "Body"},
                        ],
                    }
                ],
            },
        }
        result = normalize_tree(doc, config)
        assert result.document["epic"]["issueType"] == "Initiative"
        assert result.document["epic"]["labels"] == ["initiative"]
        assert result.document["epic"]["features"][0]["issueType"] == "Story"
        assert result.document["epic"]["features"][0]["labels"] == ["story"]
        assert result.document["epic"]["features"][0]["subtasks"][0]["issueType"] == "Task"
        assert result.document["epic"]["features"][0]["subtasks"][0]["labels"] == ["task"]

    def test_handles_non_dict_epic(self):
        """Non-dict epic returns document unchanged."""
        config = EpicTreeConfig()
        doc = {"schemaVersion": "1.0", "epic": "not a dict"}
        result = normalize_tree(doc, config)
        assert result.document["epic"] == "not a dict"

    def test_skips_non_dict_features(self):
        """Non-dict items in features array are skipped during normalization."""
        config = EpicTreeConfig()
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": ["not-a-dict", 42, None],
            },
        }
        result = normalize_tree(doc, config)
        # Non-dict features are left unchanged
        assert result.document["epic"]["features"] == ["not-a-dict", 42, None]

    def test_skips_non_dict_subtasks(self):
        """Non-dict items in subtasks array are skipped during normalization."""
        config = EpicTreeConfig()
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [
                    {
                        "ref": "f1",
                        "title": "Feature",
                        "body": "Body",
                        "subtasks": ["not-a-dict", None],
                    }
                ],
            },
        }
        result = normalize_tree(doc, config)
        assert result.document["epic"]["features"][0]["subtasks"] == ["not-a-dict", None]

    def test_no_derivation_when_depth_not_in_config(self):
        """When depth has no default in config, issueType/labels are not set."""
        config = EpicTreeConfig(default_issue_types={}, default_labels={})
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [],
            },
        }
        result = normalize_tree(doc, config)
        assert "issueType" not in result.document["epic"]
        assert "labels" not in result.document["epic"]

    def test_null_values_treated_as_missing(self):
        """Explicit null values for issueType and labels are treated as missing."""
        config = EpicTreeConfig()
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "issueType": None,
                "labels": None,
                "features": [],
            },
        }
        result = normalize_tree(doc, config)
        assert result.document["epic"]["issueType"] == "Epic"
        assert result.document["epic"]["labels"] == ["epic"]

    def test_empty_labels_list_is_explicit(self):
        """An empty labels list [] is treated as explicit and NOT overwritten."""
        config = EpicTreeConfig()
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "labels": [],
                "features": [],
            },
        }
        result = normalize_tree(doc, config)
        assert result.document["epic"]["labels"] == []

    def test_depth_clamping_with_max_depth_2(self):
        """With maxDepth=2, deepest level is Feature."""
        config = EpicTreeConfig(max_depth=2)
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [
                    {
                        "ref": "f1",
                        "title": "Feature",
                        "body": "Body",
                        "subtasks": [
                            {"ref": "s1", "title": "Subtask", "body": "Body"},
                        ],
                    }
                ],
            },
        }
        result = normalize_tree(doc, config)
        # With max_depth=2, depth 1 clamps to effective depth 1 (Feature)
        # but depth 2 clamps to effective depth 1 as well
        subtask = result.document["epic"]["features"][0]["subtasks"][0]
        assert subtask["issueType"] == "Feature"
        assert subtask["labels"] == ["feature"]

    def test_warning_depth_preserves_unclamped_nesting(self):
        """Mismatch warnings report the raw depth even when a valid node is clamped."""
        config = EpicTreeConfig(max_depth=2)
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [
                    {
                        "ref": "f1",
                        "title": "Feature",
                        "body": "Body",
                        "subtasks": [
                            {
                                "ref": "s1",
                                "title": "Subtask",
                                "body": "Body",
                                "issueType": "Subtask",
                            },
                        ],
                    }
                ],
            },
        }
        result = normalize_tree(doc, config)
        assert len(result.warnings) == 1
        assert result.warnings[0].ref == "s1"
        assert result.warnings[0].depth == 2
        assert result.warnings[0].expected_value == "feature"

    def test_returns_normalization_result(self):
        """normalize_tree returns a NormalizationResult with document and warnings."""
        from agentic_devtools.epic_tree.normalization_models import NormalizationResult

        config = EpicTreeConfig()
        doc = {"schemaVersion": "1.0", "epic": {"ref": "e1", "title": "E", "body": "", "features": []}}
        result = normalize_tree(doc, config)
        assert isinstance(result, NormalizationResult)
        assert isinstance(result.document, dict)
        assert isinstance(result.warnings, list)

    def test_empty_dict_input(self):
        """Empty dict input returns deep-copied empty dict with empty warnings."""
        config = EpicTreeConfig()
        doc: dict = {}
        result = normalize_tree(doc, config)
        assert result.document == {}
        assert result.warnings == []

    def test_missing_epic_key(self):
        """Missing epic key returns deep-copied unmodified document."""
        config = EpicTreeConfig()
        doc = {"schemaVersion": "1.0", "other": "data"}
        result = normalize_tree(doc, config)
        assert result.document == {"schemaVersion": "1.0", "other": "data"}
        assert result.warnings == []

    def test_multi_level_tree_all_omitted(self):
        """Multi-level tree with all metadata omitted is fully normalized."""
        config = EpicTreeConfig()
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [
                    {
                        "ref": "f1",
                        "title": "F1",
                        "body": "B",
                        "subtasks": [
                            {"ref": "s1", "title": "S1", "body": "B"},
                            {"ref": "s2", "title": "S2", "body": "B"},
                        ],
                    },
                    {
                        "ref": "f2",
                        "title": "F2",
                        "body": "B",
                        "subtasks": [
                            {"ref": "s3", "title": "S3", "body": "B"},
                        ],
                    },
                ],
            },
        }
        result = normalize_tree(doc, config)
        epic = result.document["epic"]
        assert epic["issueType"] == "Epic"
        assert epic["labels"] == ["epic"]
        for feat in epic["features"]:
            assert feat["issueType"] == "Feature"
            assert feat["labels"] == ["feature"]
            for st in feat["subtasks"]:
                assert st["issueType"] == "Subtask"
                assert st["labels"] == ["subtask"]

    def test_mixed_tree_only_omitted_get_derived(self):
        """Mixed tree: only nodes with omitted fields get derived values."""
        config = EpicTreeConfig()
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "issueType": "CustomEpic",
                "features": [
                    {
                        "ref": "f1",
                        "title": "Feature",
                        "body": "Body",
                        "subtasks": [
                            {"ref": "s1", "title": "Subtask", "body": "Body", "labels": ["custom"]},
                        ],
                    }
                ],
            },
        }
        result = normalize_tree(doc, config)
        # Explicit issueType preserved on epic
        assert result.document["epic"]["issueType"] == "CustomEpic"
        # Labels derived for epic (was missing)
        assert result.document["epic"]["labels"] == ["epic"]
        # Feature gets both derived
        assert result.document["epic"]["features"][0]["issueType"] == "Feature"
        assert result.document["epic"]["features"][0]["labels"] == ["feature"]
        # Subtask has explicit labels (normalized) but gets derived issueType
        assert result.document["epic"]["features"][0]["subtasks"][0]["issueType"] == "Subtask"
        assert result.document["epic"]["features"][0]["subtasks"][0]["labels"] == ["custom"]

    def test_label_normalization_trim_lowercase_dedup(self):
        """Existing labels are trimmed, lowercased, and deduplicated."""
        config = EpicTreeConfig()
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "labels": ["Epic", "EPIC", "epic", "Q3"],
                "features": [],
            },
        }
        result = normalize_tree(doc, config)
        assert result.document["epic"]["labels"] == ["epic", "q3"]

    def test_label_normalization_whitespace_trimmed(self):
        """Labels with leading/trailing whitespace are trimmed."""
        config = EpicTreeConfig()
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "labels": ["  epic  ", " Feature ", "Q3 "],
                "features": [],
            },
        }
        result = normalize_tree(doc, config)
        assert result.document["epic"]["labels"] == ["epic", "feature", "q3"]

    def test_derived_labels_are_normalized(self):
        """Derived labels from config are normalized like explicit labels."""
        config = EpicTreeConfig(default_labels={0: [" Epic ", "EPIC", "Roadmap "]})
        doc = {
            "schemaVersion": "1.0",
            "epic": {"ref": "e1", "title": "Epic", "body": "Body", "features": []},
        }
        result = normalize_tree(doc, config)
        assert result.document["epic"]["labels"] == ["epic", "roadmap"]

    def test_childless_epic_normalized(self):
        """A childless epic (no features) is still normalized."""
        config = EpicTreeConfig()
        doc = {
            "schemaVersion": "1.0",
            "epic": {"ref": "e1", "title": "Epic", "body": "Body"},
        }
        result = normalize_tree(doc, config)
        assert result.document["epic"]["issueType"] == "Epic"
        assert result.document["epic"]["labels"] == ["epic"]
        assert result.warnings == []

    def test_non_list_labels_not_normalized(self):
        """Labels that are not a list (but not None/absent) are left untouched."""
        config = EpicTreeConfig()
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "labels": 42,
                "features": [],
            },
        }
        result = normalize_tree(doc, config)
        # Non-list labels value is preserved as-is (not normalized or derived)
        assert result.document["epic"]["labels"] == 42

    def test_deep_nesting_beyond_depth_2_is_clamped_and_normalized(self):
        """Nodes at depth > 2 are clamped to Subtask and normalized."""
        config = EpicTreeConfig()
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [
                    {
                        "ref": "f1",
                        "title": "Feature",
                        "body": "Body",
                        "subtasks": [
                            {
                                "ref": "s1",
                                "title": "Subtask",
                                "body": "Body",
                                "subtasks": [
                                    {"ref": "ss1", "title": "Sub-subtask", "body": "Body"},
                                ],
                            }
                        ],
                    }
                ],
            },
        }
        result = normalize_tree(doc, config)
        subtask = result.document["epic"]["features"][0]["subtasks"][0]
        assert subtask["issueType"] == "Subtask"
        # depth-3 node is clamped to effective depth 2 (Subtask)
        sub_subtask = subtask["subtasks"][0]
        assert sub_subtask["issueType"] == "Subtask"
        assert sub_subtask["labels"] == ["subtask"]
