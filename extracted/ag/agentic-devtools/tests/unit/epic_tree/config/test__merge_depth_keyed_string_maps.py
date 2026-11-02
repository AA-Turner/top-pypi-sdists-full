"""Tests for _merge_depth_keyed_string_maps function."""

from agentic_devtools.epic_tree.config import _merge_depth_keyed_string_maps


class TestMergeDepthKeyedStringMaps:
    """Tests for _merge_depth_keyed_string_maps."""

    def test_disjoint_keys_all_preserved(self):
        """Disjoint inputs preserve all keys from both sources."""
        high = {0: "Initiative"}
        low = {1: "Feature", 2: "Subtask"}
        result = _merge_depth_keyed_string_maps(high, low)
        assert result == {0: "Initiative", 1: "Feature", 2: "Subtask"}

    def test_overlap_high_wins(self):
        """Overlapping keys use high-precedence values."""
        high = {0: "Initiative"}
        low = {0: "Epic", 1: "Feature"}
        result = _merge_depth_keyed_string_maps(high, low)
        assert result == {0: "Initiative", 1: "Feature"}

    def test_both_empty(self):
        """Both empty dicts produces empty result."""
        assert _merge_depth_keyed_string_maps({}, {}) == {}

    def test_high_empty(self):
        """Empty high preserves all low values."""
        low = {0: "Epic", 1: "Feature"}
        result = _merge_depth_keyed_string_maps({}, low)
        assert result == {0: "Epic", 1: "Feature"}

    def test_low_empty(self):
        """Empty low preserves all high values."""
        high = {0: "Epic", 1: "Feature"}
        result = _merge_depth_keyed_string_maps(high, {})
        assert result == {0: "Epic", 1: "Feature"}

    def test_full_overlap_high_wins(self):
        """Full overlap where all keys match uses high values."""
        high = {0: "A", 1: "B"}
        low = {0: "X", 1: "Y"}
        result = _merge_depth_keyed_string_maps(high, low)
        assert result == {0: "A", 1: "B"}
