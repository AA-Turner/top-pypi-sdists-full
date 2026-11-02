"""Tests for _merge_depth_keyed_maps function."""

from agentic_devtools.epic_tree.config import _merge_depth_keyed_maps


class TestMergeDepthKeyedMaps:
    """Tests for _merge_depth_keyed_maps."""

    def test_disjoint_keys_all_preserved(self):
        """Disjoint inputs preserve all keys from both sources."""
        high = {0: ["epic"]}
        low = {1: ["feature"], 2: ["subtask"]}
        result = _merge_depth_keyed_maps(high, low)
        assert result == {0: ["epic"], 1: ["feature"], 2: ["subtask"]}

    def test_overlap_high_wins(self):
        """Overlapping keys use high-precedence values."""
        high = {0: ["initiative"]}
        low = {0: ["epic"], 1: ["feature"]}
        result = _merge_depth_keyed_maps(high, low)
        assert result == {0: ["initiative"], 1: ["feature"]}

    def test_both_empty(self):
        """Both empty dicts produces empty result."""
        assert _merge_depth_keyed_maps({}, {}) == {}

    def test_high_empty(self):
        """Empty high preserves all low values."""
        low = {0: ["epic"], 1: ["feature"]}
        result = _merge_depth_keyed_maps({}, low)
        assert result == {0: ["epic"], 1: ["feature"]}

    def test_low_empty(self):
        """Empty low preserves all high values."""
        high = {0: ["epic"], 1: ["feature"]}
        result = _merge_depth_keyed_maps(high, {})
        assert result == {0: ["epic"], 1: ["feature"]}

    def test_full_overlap_high_wins(self):
        """Full overlap where all keys match uses high values."""
        high = {0: ["a"], 1: ["b"]}
        low = {0: ["x"], 1: ["y"]}
        result = _merge_depth_keyed_maps(high, low)
        assert result == {0: ["a"], 1: ["b"]}
