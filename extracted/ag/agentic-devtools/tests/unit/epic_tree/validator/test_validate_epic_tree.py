"""Tests for validate_epic_tree() function."""

import json
from pathlib import Path

from agentic_devtools.epic_tree.config import EpicTreeConfig
from agentic_devtools.epic_tree.errors import ValidationReport
from agentic_devtools.epic_tree.validator import validate_epic_tree

FIXTURES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "fixtures" / "epic-tree"


def _load_fixture(name: str) -> dict:
    """Load a JSON fixture file by name."""
    return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))


class TestValidateEpicTreeHappyPath:
    """Tests for valid documents returning ValidationReport(valid=True)."""

    def test_valid_fixture_returns_no_errors(self):
        """valid-epic.json passes validation with empty errors."""
        doc = _load_fixture("valid-epic.json")
        report = validate_epic_tree(doc)
        assert report.valid is True
        assert report.errors == []

    def test_empty_features_valid(self):
        """An epic with empty features array is valid."""
        doc = _load_fixture("empty-arrays.json")
        report = validate_epic_tree(doc)
        assert report.valid is True

    def test_returns_validation_report_type(self):
        """validate_epic_tree returns a ValidationReport instance."""
        doc = _load_fixture("valid-epic.json")
        report = validate_epic_tree(doc)
        assert isinstance(report, ValidationReport)


class TestValidateEpicTreeSchemaErrors:
    """Tests for schema structural validation errors."""

    def test_missing_required_fields(self):
        """Missing required fields are reported."""
        doc = {"schemaVersion": "1.0"}  # missing 'epic'
        report = validate_epic_tree(doc)
        assert report.valid is False
        categories = [e.category for e in report.errors]
        assert "required" in categories

    def test_missing_ref_on_feature(self):
        """Missing ref on feature is reported."""
        doc = _load_fixture("missing-ref-feature.json")
        report = validate_epic_tree(doc)
        assert report.valid is False
        assert any("ref" in e.message for e in report.errors)

    def test_invalid_blocks_type(self):
        """Non-string items in blocks are reported."""
        doc = _load_fixture("invalid-blocks-type.json")
        report = validate_epic_tree(doc)
        assert report.valid is False

    def test_unknown_property(self):
        """Additional properties are reported."""
        doc = _load_fixture("unknown-property-subtask.json")
        report = validate_epic_tree(doc)
        assert report.valid is False
        assert any("additionalProperties" in e.category for e in report.errors)

    def test_nested_subtasks_rejected(self):
        """Subtask with nested subtasks is rejected (additionalProperties)."""
        doc = _load_fixture("subtask-with-nested-subtasks.json")
        report = validate_epic_tree(doc)
        assert report.valid is False


class TestValidateEpicTreeSemanticErrors:
    """Tests for semantic validation errors."""

    def test_duplicate_refs(self):
        """Duplicate refs produce duplicate_ref error."""
        doc = _load_fixture("duplicate-refs.json")
        report = validate_epic_tree(doc)
        assert report.valid is False
        dup_errors = [e for e in report.errors if e.category == "duplicate_ref"]
        assert len(dup_errors) >= 1
        assert "shared-ref" in dup_errors[0].message
        assert len(dup_errors[0].paths) == 2

    def test_invalid_ref_format(self):
        """Ref with invalid characters produces invalid_ref_format error."""
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "invalid ref!",
                "title": "Epic",
                "body": "Body",
                "features": [],
            },
        }
        report = validate_epic_tree(doc)
        assert report.valid is False
        # Should be caught by schema first (pattern)
        assert len(report.errors) >= 1

    def test_unresolved_reference(self):
        """Reference to non-existent ref produces unresolved_reference error."""
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "blocks": ["nonexistent"],
                "features": [],
            },
        }
        report = validate_epic_tree(doc)
        assert report.valid is False
        unresolved = [e for e in report.errors if e.category == "unresolved_reference"]
        assert len(unresolved) >= 1
        assert "nonexistent" in unresolved[0].message

    def test_cycle_detected(self):
        """Circular dependency produces cycle_detected error."""
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
                        "blockedBy": ["f2"],
                        "subtasks": [],
                    },
                    {
                        "ref": "f2",
                        "title": "Feature 2",
                        "body": "Body",
                        "blockedBy": ["f1"],
                        "subtasks": [],
                    },
                ],
            },
        }
        report = validate_epic_tree(doc)
        assert report.valid is False
        cycles = [e for e in report.errors if e.category == "cycle_detected"]
        assert len(cycles) >= 1
        assert "f1" in cycles[0].message
        assert "f2" in cycles[0].message

    def test_depth_exceeded(self):
        """Node at depth >= max_depth produces depth_exceeded error."""
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
        report = validate_epic_tree(doc, config=config)
        assert report.valid is False
        depth_errs = [e for e in report.errors if e.category == "depth_exceeded"]
        assert len(depth_errs) >= 1

    def test_multiple_simultaneous_errors(self):
        """Multiple semantic errors are all reported in one report."""
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "blocks": ["nonexistent1"],
                "features": [
                    {
                        "ref": "e1",
                        "title": "Feature (dup ref)",
                        "body": "Body",
                        "blockedBy": ["nonexistent2"],
                        "subtasks": [],
                    },
                ],
            },
        }
        report = validate_epic_tree(doc)
        assert report.valid is False
        categories = {e.category for e in report.errors}
        assert "duplicate_ref" in categories
        assert "unresolved_reference" in categories


class TestValidateEpicTreeConfigRules:
    """Tests for config-driven validation rules."""

    def test_disallowed_label(self):
        """Label not in allowed set produces disallowed_label error."""
        config = EpicTreeConfig(allowed_labels={0: ["epic", "automation"]})
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "labels": ["forbidden-label"],
                "features": [],
            },
        }
        report = validate_epic_tree(doc, config=config)
        assert report.valid is False
        label_errs = [e for e in report.errors if e.category == "disallowed_label"]
        assert len(label_errs) >= 1

    def test_disallowed_label_tuple(self):
        """Tuple labels are normalised to a list so validation is not bypassed.

        This tests the semantic-check layer directly via ``_check_config_rules``
        because JSON Schema (jsonschema ≥ 4) rejects non-list sequences at the
        structural pass and returns before the semantic pass is reached.
        """
        from agentic_devtools.epic_tree.validator import _check_config_rules

        config = EpicTreeConfig(allowed_labels={0: ["epic", "automation"]})
        node = {"ref": "e1", "title": "Epic", "body": "Body", "labels": ("forbidden-label",), "features": []}
        report = ValidationReport()
        _check_config_rules([(node, "epic", 0)], config, report)
        label_errs = [e for e in report.errors if e.category == "disallowed_label"]
        assert len(label_errs) >= 1

    def test_disallowed_issue_type(self):
        """Issue type not in allowed set produces disallowed_issue_type error."""
        config = EpicTreeConfig(allowed_issue_types={0: ["Epic"]})
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "issueType": "InvalidType",
                "features": [],
            },
        }
        report = validate_epic_tree(doc, config=config)
        assert report.valid is False
        type_errs = [e for e in report.errors if e.category == "disallowed_issue_type"]
        assert len(type_errs) >= 1

    def test_missing_body_section(self):
        """Missing required body section produces missing_body_section error."""
        config = EpicTreeConfig(required_body_sections={0: ["Summary"]})
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "No summary section here",
                "features": [],
            },
        }
        report = validate_epic_tree(doc, config=config)
        assert report.valid is False
        section_errs = [e for e in report.errors if e.category == "missing_body_section"]
        assert len(section_errs) >= 1

    def test_body_section_present_passes(self):
        """Body containing required section heading passes."""
        config = EpicTreeConfig(required_body_sections={0: ["Summary"]})
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "## Summary\nThis is the summary.",
                "features": [],
            },
        }
        report = validate_epic_tree(doc, config=config)
        assert report.valid is True


class TestValidateEpicTreeBranchCoverage:
    """Additional tests for branch coverage."""

    def test_valid_epic_passes_all_checks(self):
        """A fully valid document passes both schema and semantic validation."""
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [],
            },
        }
        report = validate_epic_tree(doc)
        assert report.valid is True

    def test_valid_tree_with_subtasks(self):
        """Full tree with features and subtasks passes validation."""
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
        report = validate_epic_tree(doc)
        assert report.valid is True

    def test_no_allowed_labels_for_depth(self):
        """When config has no allowed_labels for a depth, labels are not checked."""
        config = EpicTreeConfig(allowed_labels={1: ["feature"]})  # Only depth 1
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "labels": ["anything-goes"],
                "features": [],
            },
        }
        report = validate_epic_tree(doc, config=config)
        assert report.valid is True

    def test_labels_non_list_caught_by_schema(self):
        """Non-list labels value is caught by JSON Schema validation."""
        config = EpicTreeConfig(allowed_labels={0: ["epic"]})
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "labels": "not-a-list",
                "features": [],
            },
        }
        report = validate_epic_tree(doc, config=config)
        assert report.valid is False

    def test_issue_type_none_validates_derived_default(self):
        """Null/None issueType is checked against the auto-derived default value."""
        # The default issueType for depth 0 is "Epic", which IS allowed → no error.
        config = EpicTreeConfig(allowed_issue_types={0: ["Epic"]})
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "issueType": None,
                "features": [],
            },
        }
        report = validate_epic_tree(doc, config=config)
        type_errs = [e for e in report.errors if e.category == "disallowed_issue_type"]
        assert len(type_errs) == 0

    def test_absent_issue_type_catches_disallowed_derived_default(self):
        """When issueType is omitted, the auto-derived default is validated against the allowlist."""
        # Default for depth 0 is "Epic"; only "CustomEpic" is allowed → error.
        config = EpicTreeConfig(allowed_issue_types={0: ["CustomEpic"]})
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [],
            },
        }
        report = validate_epic_tree(doc, config=config)
        assert report.valid is False
        type_errs = [e for e in report.errors if e.category == "disallowed_issue_type"]
        assert len(type_errs) == 1
        assert "Epic" in type_errs[0].message

    def test_absent_labels_catches_disallowed_derived_defaults(self):
        """When labels are omitted, auto-derived default labels are validated against the allowlist."""
        # Default for depth 0 is ["epic"]; only "custom-epic" is allowed → error.
        config = EpicTreeConfig(allowed_labels={0: ["custom-epic"]})
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [],
            },
        }
        report = validate_epic_tree(doc, config=config)
        assert report.valid is False
        label_errs = [e for e in report.errors if e.category == "disallowed_label"]
        assert len(label_errs) == 1
        assert "epic" in label_errs[0].message

    def test_absent_labels_pass_when_derived_defaults_are_allowed(self):
        """When labels are omitted and the derived defaults are in the allowlist, no error."""
        config = EpicTreeConfig(allowed_labels={0: ["epic", "automation"]})
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [],
            },
        }
        report = validate_epic_tree(doc, config=config)
        label_errs = [e for e in report.errors if e.category == "disallowed_label"]
        assert len(label_errs) == 0

    def test_no_required_body_sections_for_depth(self):
        """When config has no required_body_sections for a depth, body is not checked."""
        config = EpicTreeConfig(required_body_sections={1: ["Details"]})  # Only depth 1
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "",
                "features": [],
            },
        }
        report = validate_epic_tree(doc, config=config)
        assert report.valid is True

    def test_node_without_blocks_or_blocked_by(self):
        """Nodes without blocks/blockedBy skip dependency checks."""
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
                        "subtasks": [],
                    },
                ],
            },
        }
        report = validate_epic_tree(doc)
        assert report.valid is True

    def test_empty_features_and_subtasks_arrays(self):
        """Empty features and subtasks arrays are traversed without error."""
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
                        "subtasks": [],
                    },
                ],
            },
        }
        report = validate_epic_tree(doc)
        assert report.valid is True

    def test_blocks_with_valid_references(self):
        """Valid blocks references pass dependency checks."""
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [
                    {
                        "ref": "f1",
                        "title": "Feature 1",
                        "body": "Body",
                        "blocks": ["f2"],
                        "subtasks": [],
                    },
                    {
                        "ref": "f2",
                        "title": "Feature 2",
                        "body": "Body",
                        "subtasks": [],
                    },
                ],
            },
        }
        report = validate_epic_tree(doc)
        assert report.valid is True

    def test_blocked_by_with_valid_references(self):
        """Valid blockedBy references pass dependency checks."""
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [
                    {
                        "ref": "f1",
                        "title": "Feature 1",
                        "body": "Body",
                        "blockedBy": ["f2"],
                        "subtasks": [],
                    },
                    {
                        "ref": "f2",
                        "title": "Feature 2",
                        "body": "Body",
                        "subtasks": [],
                    },
                ],
            },
        }
        report = validate_epic_tree(doc)
        assert report.valid is True

    def test_allowed_issue_type_passes(self):
        """Issue type in allowed set passes."""
        config = EpicTreeConfig(allowed_issue_types={0: ["Epic", "Initiative"]})
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "issueType": "Epic",
                "features": [],
            },
        }
        report = validate_epic_tree(doc, config=config)
        type_errs = [e for e in report.errors if e.category == "disallowed_issue_type"]
        assert len(type_errs) == 0

    def test_unresolved_blocked_by_reference(self):
        """Unresolved blockedBy reference produces error."""
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
                        "blockedBy": ["ghost"],
                        "subtasks": [],
                    },
                ],
            },
        }
        report = validate_epic_tree(doc)
        assert report.valid is False
        errs = [e for e in report.errors if e.category == "unresolved_reference"]
        assert len(errs) >= 1
        assert "ghost" in errs[0].message

    def test_three_node_cycle(self):
        """Three-node cycle is detected (covers DFS back-propagation)."""
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
                        "body": "Body",
                        "blocks": ["f2"],
                        "subtasks": [],
                    },
                    {
                        "ref": "f2",
                        "title": "F2",
                        "body": "Body",
                        "blocks": ["f3"],
                        "subtasks": [],
                    },
                    {
                        "ref": "f3",
                        "title": "F3",
                        "body": "Body",
                        "blocks": ["f1"],
                        "subtasks": [],
                    },
                ],
            },
        }
        report = validate_epic_tree(doc)
        assert report.valid is False
        cycles = [e for e in report.errors if e.category == "cycle_detected"]
        assert len(cycles) >= 1

    def test_non_string_in_blocks_caught_by_schema(self):
        """Non-string items in blocks are caught by JSON Schema validation."""
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "blocks": [123],
                "features": [],
            },
        }
        report = validate_epic_tree(doc)
        assert report.valid is False

    def test_default_config_used_when_none(self):
        """When config=None, default EpicTreeConfig is used."""
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [],
            },
        }
        report = validate_epic_tree(doc, config=None)
        assert report.valid is True

    def test_depth_within_limit_passes(self):
        """Nodes within max depth pass depth check."""
        config = EpicTreeConfig(max_depth=3)
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
        report = validate_epic_tree(doc, config=config)
        depth_errs = [e for e in report.errors if e.category == "depth_exceeded"]
        assert len(depth_errs) == 0


class TestValidateEpicTreeInternalFunctions:
    """Tests for internal validation functions (direct calls for branch coverage)."""

    def test_collect_all_nodes_skips_non_dict_features(self):
        """_collect_all_nodes skips non-dict items in features."""
        from agentic_devtools.epic_tree.validator import _collect_all_nodes

        node = {"ref": "e1", "features": ["not-a-dict", None, 42]}
        result: list = []
        _collect_all_nodes(node, "epic", 0, result)
        # Only the epic node itself is collected
        assert len(result) == 1
        assert result[0][0] == node

    def test_collect_all_nodes_skips_non_dict_subtasks(self):
        """_collect_all_nodes skips non-dict items in subtasks."""
        from agentic_devtools.epic_tree.validator import _collect_all_nodes

        node = {"ref": "f1", "subtasks": ["not-a-dict", None]}
        result: list = []
        _collect_all_nodes(node, "epic.features[0]", 1, result)
        assert len(result) == 1

    def test_collect_all_nodes_empty_features(self):
        """_collect_all_nodes handles empty features list."""
        from agentic_devtools.epic_tree.validator import _collect_all_nodes

        node = {"ref": "e1", "features": []}
        result: list = []
        _collect_all_nodes(node, "epic", 0, result)
        assert len(result) == 1

    def test_collect_all_nodes_empty_subtasks(self):
        """_collect_all_nodes handles empty subtasks list."""
        from agentic_devtools.epic_tree.validator import _collect_all_nodes

        node = {"ref": "f1", "subtasks": []}
        result: list = []
        _collect_all_nodes(node, "epic.features[0]", 1, result)
        assert len(result) == 1

    def test_check_ref_format_non_string_ref_skipped(self):
        """_check_ref_format skips nodes where ref is not a string."""
        from agentic_devtools.epic_tree.errors import ValidationReport
        from agentic_devtools.epic_tree.validator import _check_ref_format

        nodes = [
            ({"ref": 123}, "epic", 0),
            ({"ref": None}, "epic.features[0]", 1),
            ({}, "epic.features[1]", 1),
        ]
        report = ValidationReport()
        _check_ref_format(nodes, report)
        assert report.valid is True

    def test_check_ref_uniqueness_non_string_ref_skipped(self):
        """_check_ref_uniqueness skips nodes where ref is not a string."""
        from agentic_devtools.epic_tree.errors import ValidationReport
        from agentic_devtools.epic_tree.validator import _check_ref_uniqueness

        nodes = [
            ({"ref": 123}, "epic", 0),
            ({"ref": None}, "epic.features[0]", 1),
            ({}, "epic.features[1]", 1),
        ]
        report = ValidationReport()
        _check_ref_uniqueness(nodes, report)
        assert report.valid is True

    def test_check_config_rules_non_list_labels_skipped(self):
        """_check_config_rules skips label check when labels is not a list."""
        from agentic_devtools.epic_tree.errors import ValidationReport
        from agentic_devtools.epic_tree.validator import _check_config_rules

        config = EpicTreeConfig(allowed_labels={0: ["epic"]})
        nodes = [({"ref": "e1", "labels": "not-a-list"}, "epic", 0)]
        report = ValidationReport()
        _check_config_rules(nodes, config, report)
        assert report.valid is True

    def test_check_config_rules_no_allowed_labels_for_depth(self):
        """_check_config_rules skips label check when no config for that depth."""
        from agentic_devtools.epic_tree.errors import ValidationReport
        from agentic_devtools.epic_tree.validator import _check_config_rules

        config = EpicTreeConfig(allowed_labels={1: ["feature"]})
        nodes = [({"ref": "e1", "labels": ["anything"]}, "epic", 0)]
        report = ValidationReport()
        _check_config_rules(nodes, config, report)
        assert report.valid is True

    def test_check_config_rules_no_required_body_for_depth(self):
        """_check_config_rules skips body check when no config for that depth."""
        from agentic_devtools.epic_tree.errors import ValidationReport
        from agentic_devtools.epic_tree.validator import _check_config_rules

        config = EpicTreeConfig(required_body_sections={1: ["Details"]})
        nodes = [({"ref": "e1", "body": ""}, "epic", 0)]
        report = ValidationReport()
        _check_config_rules(nodes, config, report)
        assert report.valid is True

    def test_check_config_rules_issue_type_none_falls_back_to_default(self):
        """_check_config_rules falls back to the config default when issueType is None."""
        from agentic_devtools.epic_tree.errors import ValidationReport
        from agentic_devtools.epic_tree.validator import _check_config_rules

        # Default for depth 0 is "Epic", which IS allowed → no error.
        config = EpicTreeConfig(allowed_issue_types={0: ["Epic"]})
        nodes = [
            ({"ref": "e1", "issueType": None}, "epic", 0),
        ]
        report = ValidationReport()
        _check_config_rules(nodes, config, report)
        assert report.valid is True

    def test_check_config_rules_empty_string_issue_type_validated(self):
        """_check_config_rules validates an empty-string issueType against the allowlist."""
        from agentic_devtools.epic_tree.errors import ValidationReport
        from agentic_devtools.epic_tree.validator import _check_config_rules

        config = EpicTreeConfig(allowed_issue_types={0: ["Epic"]})
        nodes = [
            ({"ref": "e2", "issueType": ""}, "epic", 0),
        ]
        report = ValidationReport()
        _check_config_rules(nodes, config, report)
        # Empty string is present-but-not-in-allowlist → error
        assert report.valid is False
        type_errs = [e for e in report.errors if e.category == "disallowed_issue_type"]
        assert len(type_errs) == 1

    def test_check_dependencies_non_string_blocked_ref_skipped(self):
        """_check_dependencies skips non-string items in blocks/blockedBy."""
        from agentic_devtools.epic_tree.errors import ValidationReport
        from agentic_devtools.epic_tree.validator import _check_dependencies

        nodes = [
            ({"ref": "e1", "blocks": [123, None], "blockedBy": [456]}, "epic", 0),
        ]
        report = ValidationReport()
        _check_dependencies(nodes, report)
        assert report.valid is True

    def test_check_dependencies_empty_blocks_and_blocked_by(self):
        """_check_dependencies handles nodes with no blocks/blockedBy."""
        from agentic_devtools.epic_tree.errors import ValidationReport
        from agentic_devtools.epic_tree.validator import _check_dependencies

        nodes = [
            ({"ref": "e1"}, "epic", 0),
            ({"ref": "f1", "blocks": [], "blockedBy": []}, "epic.features[0]", 1),
        ]
        report = ValidationReport()
        _check_dependencies(nodes, report)
        assert report.valid is True

    def test_detect_cycles_no_cycle_with_shared_deps(self):
        """DFS correctly marks BLACK nodes and doesn't revisit them."""
        from agentic_devtools.epic_tree.validator import _detect_cycles_in_graph

        # Diamond: a->b, a->c, b->d, c->d (no cycle)
        graph = {"a": {"b", "c"}, "b": {"d"}, "c": {"d"}, "d": set()}
        result = _detect_cycles_in_graph(graph)
        assert result == []

    def test_detect_cycles_multi_component_graph(self):
        """DFS handles disconnected components."""
        from agentic_devtools.epic_tree.validator import _detect_cycles_in_graph

        graph = {"a": {"b"}, "b": set(), "c": {"d"}, "d": {"c"}}
        result = _detect_cycles_in_graph(graph)
        assert len(result) == 1
        assert "c" in result[0]
        assert "d" in result[0]
        # a and b should not be in any SCC
        all_cycle_nodes = [node for scc in result for node in scc]
        assert "a" not in all_cycle_nodes

    def test_validate_epic_tree_non_dict_epic_after_schema(self):
        """When schema passes but epic is not a dict, return valid report."""
        from unittest.mock import patch

        from agentic_devtools.epic_tree.validator import validate_epic_tree

        doc = {"schemaVersion": "1.0", "epic": "not-a-dict"}
        # Mock the schema validator to return no errors
        with patch("agentic_devtools.epic_tree.validator.Draft201909Validator") as mock_validator_cls:
            mock_validator_cls.return_value.iter_errors.return_value = iter([])
            report = validate_epic_tree(doc)
        assert report.valid is True

    def test_required_property_extracted_from_params(self):
        """When jsonschema error has params with property, it is extracted."""
        from unittest.mock import MagicMock, patch

        from agentic_devtools.epic_tree.validator import validate_epic_tree

        mock_error = MagicMock()
        mock_error.absolute_path = ["epic"]
        mock_error.validator = "required"
        mock_error.message = "some custom message"
        mock_error.params = {"property": "ref"}
        mock_error.validator_value = ["ref", "title"]
        mock_error.instance = {"title": "Test"}

        with patch("agentic_devtools.epic_tree.validator.Draft201909Validator") as mock_cls:
            mock_cls.return_value.iter_errors.return_value = iter([mock_error])
            report = validate_epic_tree({"schemaVersion": "1.0", "epic": {}})

        assert report.valid is False
        assert report.errors[0].category == "required"

    def test_required_property_fallback_loop(self):
        """When params and regex both fail, fallback iterates validator_value."""
        from unittest.mock import MagicMock, patch

        from agentic_devtools.epic_tree.validator import validate_epic_tree

        mock_error = MagicMock()
        mock_error.absolute_path = ["epic"]
        mock_error.validator = "required"
        mock_error.message = "no match here"  # regex won't match
        mock_error.params = None
        mock_error.validator_value = ["ref", "title"]
        mock_error.instance = {"title": "Test"}  # "ref" is missing

        with patch("agentic_devtools.epic_tree.validator.Draft201909Validator") as mock_cls:
            mock_cls.return_value.iter_errors.return_value = iter([mock_error])
            report = validate_epic_tree({"schemaVersion": "1.0", "epic": {}})

        assert report.valid is False

    def test_additional_properties_no_extra_keys(self):
        """additionalProperties error with no identifiable extra keys."""
        from unittest.mock import MagicMock, patch

        from agentic_devtools.epic_tree.validator import validate_epic_tree

        mock_error = MagicMock()
        mock_error.absolute_path = ["epic"]
        mock_error.validator = "additionalProperties"
        mock_error.message = "Additional properties are not allowed"
        mock_error.instance = {"ref": "e1"}
        mock_error.schema = {"properties": {"ref": {}}}  # All keys are known

        with patch("agentic_devtools.epic_tree.validator.Draft201909Validator") as mock_cls:
            mock_cls.return_value.iter_errors.return_value = iter([mock_error])
            report = validate_epic_tree({"schemaVersion": "1.0", "epic": {}})

        assert report.valid is False

    def test_ref_format_check_direct_with_invalid_ref_string(self):
        """_check_ref_format reports errors for invalid ref strings."""
        from agentic_devtools.epic_tree.errors import ValidationReport
        from agentic_devtools.epic_tree.validator import _check_ref_format

        nodes = [
            ({"ref": "valid-ref"}, "epic", 0),
            ({"ref": "invalid ref!"}, "epic.features[0]", 1),
        ]
        report = ValidationReport()
        _check_ref_format(nodes, report)
        assert report.valid is False
        assert report.errors[0].category == "invalid_ref_format"

    def test_detect_cycles_dfs_back_propagation(self):
        """DFS correctly propagates cycle detection through chain."""
        from agentic_devtools.epic_tree.validator import _detect_cycles_in_graph

        # a -> b -> c -> a (3-node cycle where back-propagation matters)
        graph = {"a": {"b"}, "b": {"c"}, "c": {"a"}}
        result = _detect_cycles_in_graph(graph)
        assert len(result) == 1
        assert len(result[0]) == 3  # cycle involves a, b, c

    def test_check_config_labels_non_list_via_internal(self):
        """Direct _check_config_rules call with non-list labels at right depth."""
        from agentic_devtools.epic_tree.errors import ValidationReport
        from agentic_devtools.epic_tree.validator import _check_config_rules

        config = EpicTreeConfig(allowed_labels={0: ["epic"]})
        nodes = [({"ref": "e1", "labels": 42}, "epic", 0)]
        report = ValidationReport()
        _check_config_rules(nodes, config, report)
        # Non-list labels are skipped (no error about label)
        label_errs = [e for e in report.errors if e.category == "disallowed_label"]
        assert len(label_errs) == 0

    def test_required_property_fallback_all_present(self):
        """When fallback loop finds all fields present, property_name stays None."""
        from unittest.mock import MagicMock, patch

        from agentic_devtools.epic_tree.validator import validate_epic_tree

        mock_error = MagicMock()
        mock_error.absolute_path = ["epic"]
        mock_error.validator = "required"
        mock_error.message = "no match here"
        mock_error.params = None
        # All required fields ARE in instance (edge case)
        mock_error.validator_value = ["ref", "title"]
        mock_error.instance = {"ref": "e1", "title": "Test"}

        with patch("agentic_devtools.epic_tree.validator.Draft201909Validator") as mock_cls:
            mock_cls.return_value.iter_errors.return_value = iter([mock_error])
            report = validate_epic_tree({"schemaVersion": "1.0", "epic": {}})

        assert report.valid is False

    def test_check_config_empty_labels_list(self):
        """Empty labels list at depth with allowed_labels produces no errors."""
        from agentic_devtools.epic_tree.errors import ValidationReport
        from agentic_devtools.epic_tree.validator import _check_config_rules

        config = EpicTreeConfig(allowed_labels={0: ["epic"]})
        nodes = [({"ref": "e1", "labels": []}, "epic", 0)]
        report = ValidationReport()
        _check_config_rules(nodes, config, report)
        assert report.valid is True

    def test_check_dependencies_empty_blocks_list(self):
        """Nodes with empty blocks list are handled without error."""
        from agentic_devtools.epic_tree.errors import ValidationReport
        from agentic_devtools.epic_tree.validator import _check_dependencies

        nodes = [
            ({"ref": "e1", "blocks": [], "blockedBy": []}, "epic", 0),
            ({"ref": "f1"}, "epic.features[0]", 1),
        ]
        report = ValidationReport()
        _check_dependencies(nodes, report)
        assert report.valid is True

    def test_check_config_label_in_allowed_list(self):
        """Label that IS in the allowed list does not produce an error."""
        from agentic_devtools.epic_tree.errors import ValidationReport
        from agentic_devtools.epic_tree.validator import _check_config_rules

        config = EpicTreeConfig(allowed_labels={0: ["epic", "automation"]})
        nodes = [({"ref": "e1", "labels": ["epic", "automation"]}, "epic", 0)]
        report = ValidationReport()
        _check_config_rules(nodes, config, report)
        assert report.valid is True

    def test_check_config_body_non_string_skipped(self):
        """Non-string body at depth with required_body_sections is skipped."""
        from agentic_devtools.epic_tree.errors import ValidationReport
        from agentic_devtools.epic_tree.validator import _check_config_rules

        config = EpicTreeConfig(required_body_sections={0: ["Summary"]})
        nodes = [({"ref": "e1", "body": None}, "epic", 0)]
        report = ValidationReport()
        _check_config_rules(nodes, config, report)
        assert report.valid is True

    def test_check_dependencies_blocks_loop_iterates(self):
        """Multiple blocks items are iterated including valid ones."""
        from agentic_devtools.epic_tree.errors import ValidationReport
        from agentic_devtools.epic_tree.validator import _check_dependencies

        nodes = [
            ({"ref": "e1", "blocks": ["f1", "f2"]}, "epic", 0),
            ({"ref": "f1"}, "epic.features[0]", 1),
            ({"ref": "f2"}, "epic.features[1]", 1),
        ]
        report = ValidationReport()
        _check_dependencies(nodes, report)
        assert report.valid is True

    def test_check_dependencies_node_without_string_ref(self):
        """Nodes without a string ref are skipped in ref collection."""
        from agentic_devtools.epic_tree.errors import ValidationReport
        from agentic_devtools.epic_tree.validator import _check_dependencies

        nodes = [
            ({"ref": None}, "epic", 0),
            ({}, "epic.features[0]", 1),
            ({"ref": 123}, "epic.features[1]", 1),
        ]
        report = ValidationReport()
        _check_dependencies(nodes, report)
        assert report.valid is True

    def test_detect_cycles_ancestor_not_included(self):
        """Nodes that merely lead into a cycle are not reported as cycle members.

        Given c → a and a ↔ b (a cycle), c is an ancestor of the cycle but is
        not part of it. _detect_cycles_in_graph() must return SCCs containing
        only cycle members (i.e. [['a', 'b']] for this graph).
        """
        from agentic_devtools.epic_tree.validator import _detect_cycles_in_graph

        graph = {"a": {"b"}, "b": {"a"}, "c": {"a"}}
        result = _detect_cycles_in_graph(graph)
        all_cycle_nodes = [node for scc in result for node in scc]
        assert "a" in all_cycle_nodes
        assert "b" in all_cycle_nodes
        assert "c" not in all_cycle_nodes  # ancestor only, not part of the cycle

    def test_root_level_schema_error_preserves_path(self):
        """Schema errors at the document root include the RFC 6901 root path ''.

        Previously, paths=[err.path] if err.path else [] would drop the empty
        string '' (the root pointer) because '' is falsy in Python.
        """
        # Missing 'epic' at the document root → absolute_path = [] → pointer = ""
        doc = {"schemaVersion": "1.0"}
        report = validate_epic_tree(doc)
        assert report.valid is False
        required_errors = [e for e in report.errors if e.category == "required"]
        assert required_errors, "expected at least one 'required' error"
        assert any(e.paths == [""] for e in required_errors)


class TestCollectAllValidation:
    """Tests for collect-all (no short-circuit) validation behavior."""

    def test_unresolved_reference_and_cycle_both_reported(self):
        """Unresolved references AND cycles both appear in one report."""
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "blocks": ["nonexistent"],
                "features": [
                    {
                        "ref": "f1",
                        "title": "F1",
                        "body": "Body",
                        "blockedBy": ["f2"],
                        "subtasks": [],
                    },
                    {
                        "ref": "f2",
                        "title": "F2",
                        "body": "Body",
                        "blockedBy": ["f1"],
                        "subtasks": [],
                    },
                ],
            },
        }
        report = validate_epic_tree(doc)
        assert report.valid is False
        categories = {e.category for e in report.errors}
        assert "unresolved_reference" in categories
        assert "cycle_detected" in categories

    def test_two_independent_cycles_two_entries(self):
        """Two independent cycles produce 2 separate cycle_detected entries."""
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
                        "body": "Body",
                        "blockedBy": ["f2"],
                        "subtasks": [],
                    },
                    {
                        "ref": "f2",
                        "title": "F2",
                        "body": "Body",
                        "blockedBy": ["f1"],
                        "subtasks": [],
                    },
                    {
                        "ref": "f3",
                        "title": "F3",
                        "body": "Body",
                        "blockedBy": ["f4"],
                        "subtasks": [],
                    },
                    {
                        "ref": "f4",
                        "title": "F4",
                        "body": "Body",
                        "blockedBy": ["f3"],
                        "subtasks": [],
                    },
                ],
            },
        }
        report = validate_epic_tree(doc)
        assert report.valid is False
        cycles = [e for e in report.errors if e.category == "cycle_detected"]
        assert len(cycles) == 2

    def test_self_referencing_node_cycle(self):
        """Self-referencing node produces a cycle_detected entry."""
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "blocks": ["e1"],
                "features": [],
            },
        }
        report = validate_epic_tree(doc)
        assert report.valid is False
        cycles = [e for e in report.errors if e.category == "cycle_detected"]
        assert len(cycles) == 1
        assert "e1" in cycles[0].message

    def test_multi_error_five_errors_three_categories(self):
        """Tree with >=5 errors across >=3 categories reports all."""
        config = EpicTreeConfig(max_depth=2)
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "blocks": ["ghost1", "ghost2"],
                "features": [
                    {
                        "ref": "f1",
                        "title": "F1",
                        "body": "Body",
                        "blockedBy": ["f2"],
                        "subtasks": [
                            {"ref": "s1", "title": "S1", "body": "Body"},
                            {"ref": "s2", "title": "S2", "body": "Body"},
                        ],
                    },
                    {
                        "ref": "f2",
                        "title": "F2",
                        "body": "Body",
                        "blockedBy": ["f1"],
                        "subtasks": [],
                    },
                ],
            },
        }
        report = validate_epic_tree(doc, config=config)
        assert report.valid is False
        categories = {e.category for e in report.errors}
        assert len(report.errors) >= 5
        assert len(categories) >= 3

    def test_valid_tree_returns_valid_empty(self):
        """Valid tree returns valid=True, empty errors, empty warnings."""
        doc = _load_fixture("valid-epic.json")
        report = validate_epic_tree(doc)
        assert report.valid is True
        assert report.errors == []
        assert report.warnings == []


class TestDeterministicOrdering:
    """Tests for deterministic error ordering in reports."""

    def test_numeric_index_ordering(self):
        """Errors at features[2] appear before features[10]."""
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [{"ref": f"f{i}", "title": f"F{i}", "body": "Body", "subtasks": []} for i in range(11)],
            },
        }
        # Add unresolved refs at positions 10 and 2
        doc["epic"]["features"][10]["blocks"] = ["ghost_10"]
        doc["epic"]["features"][2]["blocks"] = ["ghost_2"]
        report = validate_epic_tree(doc)
        unresolved = [e for e in report.errors if e.category == "unresolved_reference"]
        assert len(unresolved) == 2
        # features[2] should come before features[10]
        assert "features[2]" in unresolved[0].paths[0]
        assert "features[10]" in unresolved[1].paths[0]

    def test_same_path_sorted_by_category(self):
        """Two errors at same path are sub-sorted by category."""
        config = EpicTreeConfig(
            max_depth=1,
            allowed_labels={0: ["epic"]},
            default_labels={0: ["bad-label"]},
        )
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [],
            },
        }
        report = validate_epic_tree(doc, config=config)
        assert report.valid is False
        # Should have depth_exceeded and disallowed_label at "epic" path
        epic_errors = [e for e in report.errors if "epic" in (e.paths[0] if e.paths else "")]
        categories = [e.category for e in epic_errors]
        # Verify sorted alphabetically
        assert categories == sorted(categories)

    def test_repeated_calls_same_order(self):
        """Two validate_epic_tree calls with same input produce identical order."""
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "blocks": ["ghost"],
                "features": [
                    {
                        "ref": "f1",
                        "title": "F1",
                        "body": "Body",
                        "blockedBy": ["f2"],
                        "subtasks": [],
                    },
                    {
                        "ref": "f2",
                        "title": "F2",
                        "body": "Body",
                        "blockedBy": ["f1"],
                        "subtasks": [],
                    },
                ],
            },
        }
        report1 = validate_epic_tree(doc)
        report2 = validate_epic_tree(doc)
        assert [(e.category, e.message, e.paths) for e in report1.errors] == [
            (e.category, e.message, e.paths) for e in report2.errors
        ]


class TestCategoryConstants:
    """Tests that errors use the correct category constants."""

    def test_cycle_uses_constant(self):
        """Cycle error uses CATEGORY_CYCLE_DETECTED value."""
        from agentic_devtools.epic_tree.errors import CATEGORY_CYCLE_DETECTED

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
                        "body": "Body",
                        "blockedBy": ["f2"],
                        "subtasks": [],
                    },
                    {
                        "ref": "f2",
                        "title": "F2",
                        "body": "Body",
                        "blockedBy": ["f1"],
                        "subtasks": [],
                    },
                ],
            },
        }
        report = validate_epic_tree(doc)
        cycles = [e for e in report.errors if e.category == CATEGORY_CYCLE_DETECTED]
        assert len(cycles) >= 1

    def test_unresolved_reference_uses_constant(self):
        """Unresolved ref error uses CATEGORY_UNRESOLVED_REFERENCE value."""
        from agentic_devtools.epic_tree.errors import CATEGORY_UNRESOLVED_REFERENCE

        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "blocks": ["ghost"],
                "features": [],
            },
        }
        report = validate_epic_tree(doc)
        unresolved = [e for e in report.errors if e.category == CATEGORY_UNRESOLVED_REFERENCE]
        assert len(unresolved) >= 1
        assert "epic" in unresolved[0].paths[0]

    def test_depth_exceeded_uses_constant(self):
        """Depth error uses CATEGORY_DEPTH_EXCEEDED and includes depth info."""
        from agentic_devtools.epic_tree.errors import CATEGORY_DEPTH_EXCEEDED

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
                        "title": "F1",
                        "body": "Body",
                        "subtasks": [
                            {"ref": "s1", "title": "S1", "body": "Body"},
                        ],
                    }
                ],
            },
        }
        report = validate_epic_tree(doc, config=config)
        depth_errors = [e for e in report.errors if e.category == CATEGORY_DEPTH_EXCEEDED]
        assert len(depth_errors) >= 1
        assert "depth" in depth_errors[0].message.lower()

    def test_disallowed_label_uses_constant(self):
        """Disallowed label error uses CATEGORY_DISALLOWED_LABEL."""
        from agentic_devtools.epic_tree.errors import CATEGORY_DISALLOWED_LABEL

        config = EpicTreeConfig(
            allowed_labels={0: ["epic"]},
            default_labels={0: ["wrong-label"]},
        )
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [],
            },
        }
        report = validate_epic_tree(doc, config=config)
        label_errors = [e for e in report.errors if e.category == CATEGORY_DISALLOWED_LABEL]
        assert len(label_errors) >= 1
        assert "epic" in label_errors[0].paths[0]


class TestValidateEpicTreeSkipCycleCheck:
    """The ``skip_cycle_check`` flag defers cycle detection to a later graph."""

    def _cyclic_doc(self) -> dict:
        return {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [
                    {
                        "ref": "f1",
                        "title": "F1",
                        "body": "Body",
                        "blockedBy": ["f2"],
                        "subtasks": [],
                    },
                    {
                        "ref": "f2",
                        "title": "F2",
                        "body": "Body",
                        "blockedBy": ["f1"],
                        "subtasks": [],
                    },
                ],
            },
        }

    def test_cycle_reported_by_default(self):
        from agentic_devtools.epic_tree.errors import CATEGORY_CYCLE_DETECTED

        report = validate_epic_tree(self._cyclic_doc())
        cycles = [e for e in report.errors if e.category == CATEGORY_CYCLE_DETECTED]
        assert len(cycles) >= 1

    def test_cycle_suppressed_when_skipped(self):
        from agentic_devtools.epic_tree.errors import CATEGORY_CYCLE_DETECTED

        report = validate_epic_tree(self._cyclic_doc(), skip_cycle_check=True)
        cycles = [e for e in report.errors if e.category == CATEGORY_CYCLE_DETECTED]
        assert cycles == []
        assert report.valid
