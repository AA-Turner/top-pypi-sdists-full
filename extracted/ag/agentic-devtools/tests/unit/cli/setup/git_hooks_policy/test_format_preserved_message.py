"""Tests for format_preserved_message."""

from __future__ import annotations

from agentic_devtools.cli.setup.fixloop import _STDOUT_PATTERNS
from agentic_devtools.cli.setup.git_hooks_policy import (
    HOOKS_DISABLED_MESSAGE,
    NON_BOOLEAN_WARNING_PREFIX,
    PRESERVED_MESSAGE_PREFIX,
    PRESERVED_MESSAGE_SUFFIX,
    format_preserved_message,
)


class TestFormatPreservedMessage:
    """Tests for format_preserved_message."""

    def test_includes_the_preserved_value(self) -> None:
        """The existing hooks path is quoted in the first line."""
        message = format_preserved_message(".husky/_")
        assert message.startswith(PRESERVED_MESSAGE_PREFIX)
        assert "'.husky/_'" in message

    def test_is_two_lines_prefix_then_suffix(self) -> None:
        """Renders exactly two lines: the notice and the opt-out hint."""
        lines = format_preserved_message("/custom/hooks").splitlines()
        assert len(lines) == 2
        assert lines[0] == f"{PRESERVED_MESSAGE_PREFIX}'/custom/hooks' — leaving it unchanged."
        assert lines[1] == PRESERVED_MESSAGE_SUFFIX

    def test_messages_do_not_match_any_fixloop_stdout_pattern(self) -> None:
        """New stdout must not be misclassified by the fix-loop stdout classifier."""
        candidates = [
            HOOKS_DISABLED_MESSAGE,
            NON_BOOLEAN_WARNING_PREFIX,
            format_preserved_message(".husky/_"),
            format_preserved_message("/custom/hooks"),
        ]
        for candidate in candidates:
            for pattern, error_class in _STDOUT_PATTERNS:
                assert pattern.search(candidate) is None, f"{candidate!r} matched {error_class}"
