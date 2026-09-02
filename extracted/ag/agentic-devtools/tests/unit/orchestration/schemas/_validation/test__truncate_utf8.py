from agentic_devtools.orchestration.schemas._validation import _truncate_utf8


class TestTruncateUtf8:
    def test_returns_empty_when_max_bytes_is_non_positive(self) -> None:
        assert _truncate_utf8("abc", 0) == ""
        assert _truncate_utf8("abc", -1) == ""

    def test_returns_dot_prefix_when_max_bytes_smaller_than_ellipsis(self) -> None:
        assert _truncate_utf8("abcdef", 2) == ".."
