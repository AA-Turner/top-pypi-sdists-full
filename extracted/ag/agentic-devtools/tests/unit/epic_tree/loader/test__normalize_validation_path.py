"""Tests for _normalize_validation_path helper in epic_tree.loader."""

from agentic_devtools.epic_tree.loader import _normalize_validation_path


class TestNormalizeValidationPath:
    """Tests for _normalize_validation_path."""

    def test_empty_string_unchanged(self):
        """Empty string (root JSON Pointer) passes through unchanged."""
        assert _normalize_validation_path("") == ""

    def test_already_json_pointer_unchanged(self):
        """Paths already starting with / pass through unchanged."""
        assert _normalize_validation_path("/epic") == "/epic"
        assert _normalize_validation_path("/epic/features/0") == "/epic/features/0"
        assert _normalize_validation_path("/epic/features/0/subtasks/1") == "/epic/features/0/subtasks/1"

    def test_root_node_dot_notation(self):
        """Top-level dot-notation 'epic' becomes '/epic'."""
        assert _normalize_validation_path("epic") == "/epic"

    def test_feature_dot_notation(self):
        """'epic.features[0]' becomes '/epic/features/0'."""
        assert _normalize_validation_path("epic.features[0]") == "/epic/features/0"

    def test_subtask_dot_notation(self):
        """'epic.features[0].subtasks[1]' becomes '/epic/features/0/subtasks/1'."""
        assert _normalize_validation_path("epic.features[0].subtasks[1]") == "/epic/features/0/subtasks/1"

    def test_multi_digit_index(self):
        """Bracket indices with multiple digits are handled correctly."""
        assert _normalize_validation_path("epic.features[12].subtasks[0]") == "/epic/features/12/subtasks/0"
