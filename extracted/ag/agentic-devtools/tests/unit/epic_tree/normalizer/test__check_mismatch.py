"""Tests for _check_mismatch function."""

from agentic_devtools.epic_tree.config import EpicTreeConfig
from agentic_devtools.epic_tree.normalization_models import NormalizationWarning
from agentic_devtools.epic_tree.normalizer import _check_mismatch


class TestCheckMismatch:
    """Tests for mismatch warning emission."""

    def test_warns_on_issue_type_mismatch(self):
        """Emits warning when issueType contradicts effective depth."""
        config = EpicTreeConfig()
        warnings: list[NormalizationWarning] = []
        node = {"ref": "f1", "issueType": "Epic"}
        _check_mismatch(node, effective_depth=1, config=config, warnings=warnings)
        assert len(warnings) == 1
        assert warnings[0].field == "issueType"
        assert warnings[0].actual_value == "epic"
        assert warnings[0].expected_value == "feature"

    def test_warns_on_label_hierarchy_mismatch(self):
        """Emits warning when label contains hierarchy keyword at wrong depth."""
        config = EpicTreeConfig()
        warnings: list[NormalizationWarning] = []
        node = {"ref": "s1", "labels": ["epic"]}
        _check_mismatch(node, effective_depth=2, config=config, warnings=warnings)
        assert len(warnings) == 1
        assert warnings[0].field == "labels"
        assert warnings[0].actual_value == "epic"
        assert warnings[0].expected_value == "subtask"

    def test_warns_once_for_duplicate_label_mismatch_values(self):
        """Duplicate labels that normalize to the same value emit one warning."""
        config = EpicTreeConfig()
        warnings: list[NormalizationWarning] = []
        node = {"ref": "s1", "labels": ["EPIC", "epic"]}
        _check_mismatch(node, effective_depth=2, config=config, warnings=warnings)
        assert len(warnings) == 1
        assert warnings[0].field == "labels"
        assert warnings[0].actual_value == "epic"

    def test_no_warning_when_values_match(self):
        """No warning when explicit values match expected depth."""
        config = EpicTreeConfig()
        warnings: list[NormalizationWarning] = []
        node = {"ref": "e1", "issueType": "Epic", "labels": ["epic"]}
        _check_mismatch(node, effective_depth=0, config=config, warnings=warnings)
        assert warnings == []

    def test_no_warning_for_compound_labels(self):
        """No warning for compound/non-hierarchy labels like 'Feature Request'."""
        config = EpicTreeConfig()
        warnings: list[NormalizationWarning] = []
        node = {"ref": "s1", "labels": ["Feature Request", "epic-tree", "feature-flag"]}
        _check_mismatch(node, effective_depth=2, config=config, warnings=warnings)
        # None of these are exact hierarchy keywords
        assert warnings == []

    def test_mismatch_at_clamped_depth(self):
        """Node at raw depth 3 with issueType 'Feature' warns because effective depth 2 expects 'Subtask'."""
        config = EpicTreeConfig()
        warnings: list[NormalizationWarning] = []
        node = {"ref": "deep1", "issueType": "Feature"}
        # effective_depth = min(3, 3-1) = 2
        _check_mismatch(node, effective_depth=2, config=config, warnings=warnings)
        assert len(warnings) == 1
        assert warnings[0].expected_value == "subtask"
        assert warnings[0].actual_value == "feature"

    def test_warning_uses_raw_depth_when_provided(self):
        """Warnings report the unclamped depth for deeply nested nodes."""
        config = EpicTreeConfig()
        warnings: list[NormalizationWarning] = []
        node = {"ref": "deep1", "issueType": "Feature"}
        _check_mismatch(node, effective_depth=2, raw_depth=3, config=config, warnings=warnings)
        assert warnings[0].depth == 3

    def test_no_warning_on_absent_values(self):
        """No warning when issueType and labels are absent."""
        config = EpicTreeConfig()
        warnings: list[NormalizationWarning] = []
        node = {"ref": "e1"}
        _check_mismatch(node, effective_depth=0, config=config, warnings=warnings)
        assert warnings == []

    def test_no_warning_on_null_values(self):
        """No warning when issueType and labels are null."""
        config = EpicTreeConfig()
        warnings: list[NormalizationWarning] = []
        node = {"ref": "e1", "issueType": None, "labels": None}
        _check_mismatch(node, effective_depth=0, config=config, warnings=warnings)
        assert warnings == []

    def test_warning_value_format_normalized(self):
        """Warning actual_value is normalized (trimmed+lowercased)."""
        config = EpicTreeConfig()
        warnings: list[NormalizationWarning] = []
        node = {"ref": "f1", "issueType": "  EPIC  "}
        _check_mismatch(node, effective_depth=1, config=config, warnings=warnings)
        assert warnings[0].actual_value == "epic"
        assert warnings[0].expected_value == "feature"

    def test_issue_type_warning_before_labels(self):
        """issueType warning is emitted before labels warning."""
        config = EpicTreeConfig()
        warnings: list[NormalizationWarning] = []
        node = {"ref": "f1", "issueType": "Epic", "labels": ["epic"]}
        _check_mismatch(node, effective_depth=1, config=config, warnings=warnings)
        assert len(warnings) == 2
        assert warnings[0].field == "issueType"
        assert warnings[1].field == "labels"

    def test_no_issue_type_warning_when_depth_not_in_config(self):
        """No issueType warning when effective depth has no config entry."""
        config = EpicTreeConfig(default_issue_types={0: "Epic"})
        warnings: list[NormalizationWarning] = []
        node = {"ref": "f1", "issueType": "Task"}
        # depth 1 not in default_issue_types → no expected value → no warning
        _check_mismatch(node, effective_depth=1, config=config, warnings=warnings)
        assert warnings == []

    def test_no_labels_warning_when_depth_not_in_config(self):
        """No labels warning when effective depth has no default_labels entry."""
        config = EpicTreeConfig(default_labels={0: ["epic"]})
        warnings: list[NormalizationWarning] = []
        node = {"ref": "f1", "labels": ["something"]}
        # depth 1 not in default_labels → no expected value → no warning
        _check_mismatch(node, effective_depth=1, config=config, warnings=warnings)
        assert warnings == []

    def test_non_string_labels_skipped_in_mismatch(self):
        """Non-string items in labels list are skipped during mismatch check."""
        config = EpicTreeConfig()
        warnings: list[NormalizationWarning] = []
        node = {"ref": "f1", "labels": [123, None, "epic"]}
        # Only "epic" is checked; 123 and None are skipped
        _check_mismatch(node, effective_depth=0, config=config, warnings=warnings)
        # "epic" matches depth 0's expected label → no warning
        assert warnings == []

    def test_ref_none_uses_unknown_sentinel(self):
        """When ref is None, warning uses '<unknown>' as ref string."""
        config = EpicTreeConfig()
        warnings: list[NormalizationWarning] = []
        node = {"ref": None, "issueType": "Epic"}
        _check_mismatch(node, effective_depth=1, config=config, warnings=warnings)
        assert len(warnings) == 1
        assert warnings[0].ref == "<unknown>"
        assert isinstance(warnings[0].ref, str)

    def test_ref_non_string_type_uses_unknown_sentinel(self):
        """When ref is a non-string type (e.g. int), warning uses '<unknown>' as ref string."""
        config = EpicTreeConfig()
        warnings: list[NormalizationWarning] = []
        node = {"ref": 42, "issueType": "Epic"}
        _check_mismatch(node, effective_depth=1, config=config, warnings=warnings)
        assert len(warnings) == 1
        assert warnings[0].ref == "<unknown>"
        assert isinstance(warnings[0].ref, str)
