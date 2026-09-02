"""Tests for _parse_optional_positive_int()."""

from agentic_devtools.cli.ci.github_provider import _parse_optional_positive_int


class TestParseOptionalPositiveInt:
    """Tests for optional positive integer parsing."""

    def test_parses_positive_integer_and_string(self) -> None:
        assert _parse_optional_positive_int(42) == 42
        assert _parse_optional_positive_int("42") == 42

    def test_returns_none_for_non_positive_values(self) -> None:
        assert _parse_optional_positive_int(0) is None
        assert _parse_optional_positive_int(-1) is None
        assert _parse_optional_positive_int("0") is None

    def test_returns_none_for_invalid_types_and_text(self) -> None:
        assert _parse_optional_positive_int(True) is None
        assert _parse_optional_positive_int(None) is None
        assert _parse_optional_positive_int("not-an-int") is None
