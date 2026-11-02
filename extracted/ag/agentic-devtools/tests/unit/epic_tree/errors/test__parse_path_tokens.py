"""Tests for _parse_path_tokens() in errors.py."""

from agentic_devtools.epic_tree.errors import _parse_path_tokens


class TestParsePathTokensDotNotation:
    """Tests for dot-notation path parsing."""

    def test_simple_dot_path(self):
        """Simple dot-separated path returns string tokens."""
        assert _parse_path_tokens("epic.features") == ["epic", "features"]

    def test_dot_path_with_bracket_index(self):
        """Dot-notation with bracket indices returns mixed tokens."""
        result = _parse_path_tokens("epic.features[0].subtasks[1]")
        assert result == ["epic", "features", 0, "subtasks", 1]

    def test_single_segment(self):
        """Single segment without dots returns one token."""
        assert _parse_path_tokens("epic") == ["epic"]

    def test_bracket_only(self):
        """Segment that is just an index."""
        assert _parse_path_tokens("items[3]") == ["items", 3]


class TestParsePathTokensJsonPointer:
    """Tests for JSON Pointer path parsing."""

    def test_json_pointer_simple(self):
        """JSON Pointer with string segments."""
        assert _parse_path_tokens("/epic/features/0") == ["epic", "features", 0]

    def test_json_pointer_numeric(self):
        """JSON Pointer numeric segments become integers."""
        assert _parse_path_tokens("/epic/features/10") == ["epic", "features", 10]

    def test_json_pointer_escape_tilde(self):
        """JSON Pointer ~0 decodes to tilde."""
        assert _parse_path_tokens("/a~0b") == ["a~b"]

    def test_json_pointer_escape_slash(self):
        """JSON Pointer ~1 decodes to slash."""
        assert _parse_path_tokens("/a~1b/~0c") == ["a/b", "~c"]


class TestParsePathTokensEdgeCases:
    """Tests for edge cases."""

    def test_empty_string(self):
        """Empty string returns empty list."""
        assert _parse_path_tokens("") == []

    def test_root_pointer(self):
        """Root JSON Pointer '/' with nothing after returns empty list."""
        result = _parse_path_tokens("/")
        # "/" means the path points to the root - no tokens
        assert result == []

    def test_multiple_bracket_indices(self):
        """Path with consecutive bracket indices."""
        assert _parse_path_tokens("a[0][1]") == ["a", 0, 1]
