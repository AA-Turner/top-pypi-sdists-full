"""Tests for NormalizationWarning dataclass."""

from agentic_devtools.epic_tree.normalization_models import NormalizationWarning


class TestNormalizationWarning:
    """Tests for NormalizationWarning construction and field access."""

    def test_construction(self):
        """NormalizationWarning can be constructed with all required fields."""
        warning = NormalizationWarning(
            ref="f1",
            depth=1,
            field="issueType",
            actual_value="epic",
            expected_value="feature",
        )
        assert warning.ref == "f1"
        assert warning.depth == 1
        assert warning.field == "issueType"
        assert warning.actual_value == "epic"
        assert warning.expected_value == "feature"

    def test_frozen(self):
        """NormalizationWarning is immutable (frozen dataclass)."""
        import dataclasses

        import pytest

        warning = NormalizationWarning(ref="s1", depth=2, field="labels", actual_value="epic", expected_value="subtask")
        with pytest.raises(dataclasses.FrozenInstanceError):
            warning.ref = "changed"  # type: ignore[misc]
