"""Tests for ``_is_token_bounded_match()``."""

from agentic_devtools.cli.speckit.verify_artifacts import _is_token_bounded_match


class TestIsTokenBoundedMatch:
    """Whether a match span is bounded by non-path-token characters."""

    def test_returns_true_for_isolated_token_in_prose(self) -> None:
        text = "inspect missing.py here"
        start = text.index("missing.py")
        end = start + len("missing.py")

        assert _is_token_bounded_match(text, (start, end)) is True

    def test_returns_false_when_preceded_by_slash(self) -> None:
        text = "path/to/missing.py"
        start = text.index("missing.py")
        end = start + len("missing.py")

        assert _is_token_bounded_match(text, (start, end)) is False

    def test_returns_false_when_preceded_by_dot(self) -> None:
        text = "pkg.missing.py"
        start = text.index("missing.py")
        end = start + len("missing.py")

        assert _is_token_bounded_match(text, (start, end)) is False

    def test_returns_false_when_preceded_by_alnum(self) -> None:
        text = "amissing.py"
        # "missing.py" starts at index 1
        start = 1
        end = start + len("missing.py")

        assert _is_token_bounded_match(text, (start, end)) is False

    def test_returns_false_when_followed_by_alnum(self) -> None:
        text = "missing.pyx"
        start = 0
        end = len("missing.py")

        assert _is_token_bounded_match(text, (start, end)) is False

    def test_returns_false_when_followed_by_underscore(self) -> None:
        text = "missing.py_extra"
        start = 0
        end = len("missing.py")

        assert _is_token_bounded_match(text, (start, end)) is False

    def test_returns_false_when_followed_by_extension_dot_then_alnum(self) -> None:
        text = "missing.py.bak"
        start = 0
        end = len("missing.py")

        assert _is_token_bounded_match(text, (start, end)) is False

    def test_returns_true_when_followed_by_dot_then_space(self) -> None:
        text = "inspect missing.py. then done"
        start = text.index("missing.py")
        end = start + len("missing.py")

        assert _is_token_bounded_match(text, (start, end)) is True

    def test_returns_true_at_start_of_string(self) -> None:
        text = "missing.py here"
        start = 0
        end = len("missing.py")

        assert _is_token_bounded_match(text, (start, end)) is True

    def test_returns_true_at_end_of_string(self) -> None:
        text = "inspect missing.py"
        start = text.index("missing.py")
        end = len(text)

        assert _is_token_bounded_match(text, (start, end)) is True

    def test_returns_true_when_preceded_by_backtick(self) -> None:
        text = "`missing.py`"
        start = 1
        end = start + len("missing.py")

        assert _is_token_bounded_match(text, (start, end)) is True

    def test_returns_true_when_surrounded_by_parentheses(self) -> None:
        text = "(missing.py)"
        start = 1
        end = start + len("missing.py")

        assert _is_token_bounded_match(text, (start, end)) is True
