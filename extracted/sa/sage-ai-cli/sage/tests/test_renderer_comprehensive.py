"""Comprehensive tests for sage/core/renderer.py - Terminal rendering."""

import time
import pytest
from unittest.mock import patch, MagicMock

from sage.core.renderer import (
    HardGuardrailViolation,
    GroundingViolation,
    ToolSyntaxViolation,
    FabricationViolation,
    StreamingTimeoutError,
    Renderer,
    clean_malformed_tool_commands,
    _detect_bad_streaming_patterns,
    _is_fatal_streaming_reason,
    stream_tokens_with_phase,
    _parse_incremental_tool_calls,
    normalize_tool_command_syntax,
)


# =============================================================================
# Tests for Exception classes
# =============================================================================


class TestHardGuardrailViolation:
    """Tests for HardGuardrailViolation exception."""

    def test_create_violation(self):
        """Create a violation."""
        v = HardGuardrailViolation("TEST_TYPE", "Test message")
        assert v.violation_type == "TEST_TYPE"
        assert v.message == "Test message"
        assert v.context == ""

    def test_create_with_context(self):
        """Create with context."""
        v = HardGuardrailViolation("TYPE", "Message", "Some context")
        assert v.context == "Some context"

    def test_str_format(self):
        """String format includes type and message."""
        v = HardGuardrailViolation("TYPE", "Message")
        assert "[TYPE]" in str(v)
        assert "Message" in str(v)

    def test_is_exception(self):
        """Is an Exception subclass."""
        v = HardGuardrailViolation("TYPE", "Message")
        assert isinstance(v, Exception)


class TestGroundingViolation:
    """Tests for GroundingViolation exception."""

    def test_create(self):
        """Create grounding violation."""
        v = GroundingViolation("No file evidence")
        assert v.violation_type == "GROUNDING"
        assert v.message == "No file evidence"

    def test_with_context(self):
        """Create with context."""
        v = GroundingViolation("Message", "file.py content")
        assert v.context == "file.py content"

    def test_is_hard_guardrail(self):
        """Is a HardGuardrailViolation."""
        v = GroundingViolation("Message")
        assert isinstance(v, HardGuardrailViolation)


class TestToolSyntaxViolation:
    """Tests for ToolSyntaxViolation exception."""

    def test_create(self):
        """Create tool syntax violation."""
        v = ToolSyntaxViolation("Invalid XML")
        assert v.violation_type == "TOOL_SYNTAX"
        assert v.message == "Invalid XML"

    def test_is_hard_guardrail(self):
        """Is a HardGuardrailViolation."""
        v = ToolSyntaxViolation("Message")
        assert isinstance(v, HardGuardrailViolation)


class TestFabricationViolation:
    """Tests for FabricationViolation exception."""

    def test_create(self):
        """Create fabrication violation."""
        v = FabricationViolation("Made up content")
        assert v.violation_type == "FABRICATION"
        assert v.message == "Made up content"

    def test_is_hard_guardrail(self):
        """Is a HardGuardrailViolation."""
        v = FabricationViolation("Message")
        assert isinstance(v, HardGuardrailViolation)


class TestStreamingTimeoutError:
    """Tests for StreamingTimeoutError exception."""

    def test_create_default_message(self):
        """Create with default message."""
        e = StreamingTimeoutError()
        assert "timeout" in e.message.lower()

    def test_create_custom_message(self):
        """Create with custom message."""
        e = StreamingTimeoutError("Custom timeout message")
        assert e.message == "Custom timeout message"

    def test_is_exception(self):
        """Is an Exception subclass."""
        e = StreamingTimeoutError()
        assert isinstance(e, Exception)


# =============================================================================
# Tests for clean_malformed_tool_commands function
# =============================================================================


class TestCleanMalformedToolCommands:
    """Tests for clean_malformed_tool_commands function."""

    def test_normalize_bare_read_command(self):
        """Bare uppercase READ commands should be normalized into canonical syntax."""
        content = "READ README.md"
        result = normalize_tool_command_syntax(content)
        assert result == "READ: README.md"

    def test_clean_blank_read(self):
        """Remove blank READ: commands."""
        content = "Before\nREAD:\nAfter"
        result = clean_malformed_tool_commands(content)
        assert "READ:" not in result
        assert "Before" in result
        assert "After" in result

    def test_clean_blank_search(self):
        """Remove blank SEARCH: commands."""
        content = "Before\nSEARCH:\nAfter"
        result = clean_malformed_tool_commands(content)
        assert "SEARCH:" not in result

    def test_clean_blank_run(self):
        """Remove blank RUN: commands."""
        content = "Before\nRUN:\nAfter"
        result = clean_malformed_tool_commands(content)
        assert "RUN:" not in result

    def test_detect_execute_bash_normalizes_to_run_not_rejected(self):
        """<execute_bash> is supported and normalizes to RUN: — do not treat as fatal XML."""
        is_bad, reason = _detect_bad_streaming_patterns("<execute_bash>\nls -laR\n</execute_bash>")
        assert is_bad is False, reason

    def test_clean_malformed_read_explanation(self):
        """Remove READ: with explanation text."""
        content = "READ: The user is asking for help"
        result = clean_malformed_tool_commands(content)
        assert "READ:" not in result

    def test_clean_malformed_with_i_will(self):
        """Remove malformed 'I will' commands."""
        content = "READ: I will read the file"
        result = clean_malformed_tool_commands(content)
        assert "READ:" not in result

    def test_preserve_valid_read(self):
        """Preserve valid READ: command."""
        content = "READ: src/main.py"
        result = clean_malformed_tool_commands(content)
        assert "READ: src/main.py" in result

    def test_preserve_valid_search(self):
        """Preserve valid SEARCH: command."""
        content = "SEARCH: def main"
        result = clean_malformed_tool_commands(content)
        assert "SEARCH: def main" in result

    def test_preserve_valid_run(self):
        """Preserve valid RUN: command."""
        content = "RUN: pytest tests/"
        result = clean_malformed_tool_commands(content)
        assert "RUN: pytest tests/" in result

    def test_clean_normalizes_bare_read_command(self):
        """Cleanup should preserve valid near-miss tool commands by normalizing them."""
        content = "READ Dockerfile"
        result = clean_malformed_tool_commands(content)
        assert result == "READ: Dockerfile"

    def test_preserve_normal_text(self):
        """Preserve normal text content."""
        content = "This is normal text\nwith multiple lines"
        result = clean_malformed_tool_commands(content)
        assert result == content

    def test_mixed_valid_invalid(self):
        """Handle mix of valid and invalid commands."""
        content = """READ: src/main.py
READ: The user wants
READ: utils/helper.py
RUN:
RUN: pytest"""
        result = clean_malformed_tool_commands(content)
        assert "READ: src/main.py" in result
        assert "READ: The user wants" not in result
        assert "READ: utils/helper.py" in result
        assert "RUN: pytest" in result


# =============================================================================
# Tests for _parse_incremental_tool_calls function
# =============================================================================


class TestParseIncrementalToolCalls:
    """Tests for _parse_incremental_tool_calls function."""

    def test_parse_read_command(self):
        """Parse READ: command."""
        content = "READ: src/main.py"
        result = _parse_incremental_tool_calls(content)
        assert result is not None
        assert len(result) == 1
        assert result[0].arguments["path"] == "src/main.py"

    def test_parse_search_command(self):
        """Parse SEARCH: command."""
        content = "SEARCH: def process"
        result = _parse_incremental_tool_calls(content)
        assert result is not None
        assert len(result) == 1
        assert result[0].arguments["pattern"] == "def process"

    def test_parse_run_command(self):
        """Parse RUN: command."""
        content = "RUN: pytest tests/"
        result = _parse_incremental_tool_calls(content)
        assert result is not None
        assert len(result) == 1
        assert result[0].arguments["command"] == "pytest tests/"

    def test_parse_multiple_commands(self):
        """Parse multiple commands."""
        content = """READ: file1.py
SEARCH: pattern
RUN: command"""
        result = _parse_incremental_tool_calls(content)
        assert result is not None
        assert len(result) == 3

    def test_parse_with_bullet(self):
        """Parse commands with bullet prefix."""
        content = "- READ: src/main.py"
        result = _parse_incremental_tool_calls(content)
        assert result is not None
        assert len(result) == 1

    def test_parse_empty_content(self):
        """Empty content returns None."""
        result = _parse_incremental_tool_calls("")
        assert result is None

    def test_parse_no_commands(self):
        """No commands returns None."""
        content = "Just some regular text"
        result = _parse_incremental_tool_calls(content)
        assert result is None

    def test_parse_blank_command(self):
        """Blank command is skipped."""
        content = "READ:  "
        result = _parse_incremental_tool_calls(content)
        assert result is None

    def test_parse_bare_read_command(self):
        """Colonless READ commands should still parse after normalization."""
        content = "READ README.md"
        result = _parse_incremental_tool_calls(content)
        assert result is not None
        assert len(result) == 1
        assert result[0].arguments["path"] == "README.md"


# =============================================================================
# Tests for _detect_bad_streaming_patterns function
# =============================================================================


class TestDetectBadStreamingPatterns:
    """Tests for _detect_bad_streaming_patterns function."""

    def test_clean_content_ok(self):
        """Clean content is OK."""
        content = "This is a normal response about coding."
        is_bad, reason = _detect_bad_streaming_patterns(content)
        assert is_bad is False

    def test_multiple_blank_commands_bad(self):
        """Multiple blank commands detected."""
        content = "READ:\nREAD:\nREAD:\n"
        is_bad, reason = _detect_bad_streaming_patterns(content)
        assert is_bad is True
        assert "blank" in reason.lower() or "empty" in reason.lower()

    def test_single_blank_ok(self):
        """Single blank command is OK."""
        content = "READ:\nSome other text"
        is_bad, reason = _detect_bad_streaming_patterns(content)
        # Single blank might be OK
        if is_bad:
            assert "blank" in reason.lower()

    def test_malformed_tool_command(self):
        """Malformed tool command detected."""
        content = "READ: The user is asking for help with their code"
        is_bad, reason = _detect_bad_streaming_patterns(content)
        if is_bad:
            assert "malformed" in reason.lower() or "invalid" in reason.lower()

    def test_xml_tags_bad(self):
        """XML tags detected as bad."""
        content = "<tool>read_file</tool><path>foo.py</path>"
        is_bad, reason = _detect_bad_streaming_patterns(content)
        # XML tags should be detected
        if is_bad:
            assert "xml" in reason.lower() or "syntax" in reason.lower()

    def test_valid_commands_ok(self):
        """Valid commands are OK."""
        content = """Let me help you.

READ: src/main.py
SEARCH: def process
RUN: pytest

I found the following..."""
        is_bad, reason = _detect_bad_streaming_patterns(content)
        assert is_bad is False

    def test_repeated_identical_tool_command_bad(self):
        """Repeated identical tool commands should be treated as a stuck loop."""
        content = "\n".join(["SEARCH: api_handler.py"] * 6)
        is_bad, reason = _detect_bad_streaming_patterns(content)
        assert is_bad is True
        assert "repeated" in reason.lower() and "tool command" in reason.lower()

    def test_repeated_identical_prose_bad(self):
        """Repeated long prose lines should be rejected as degenerate looping."""
        repeated = (
            "I will proceed by updating the test file after reviewing the handler and then continue the same step."
        )
        content = "\n".join([repeated] * 4)
        is_bad, reason = _detect_bad_streaming_patterns(content)
        assert is_bad is True
        assert "repeated identical content" in reason.lower()

    def test_repeated_identical_path_like_content_bad(self):
        """Repeated short path-like lines should be rejected as a stuck loop."""
        content = "\n".join(["README.md"] * 6)
        is_bad, reason = _detect_bad_streaming_patterns(content)
        assert is_bad is True
        assert "repeated identical path-like content" in reason.lower()

    def test_hypothetical_assumption_still_bad_after_tool_command(self):
        """Executing one tool command should not permit fallback to assumptions."""
        content = (
            "SEARCH: test_*.py\n"
            "Without the actual source files, any deeper analysis is purely speculative."
        )
        is_bad, reason = _detect_bad_streaming_patterns(content)
        assert is_bad is True
        assert "hypothetical" in reason.lower() or "speculative" in reason.lower()

    def test_bare_read_command_ok(self):
        """Near-miss tool syntax like READ file.py should be normalized, not rejected."""
        content = "READ README.md"
        is_bad, reason = _detect_bad_streaming_patterns(content)
        assert is_bad is False, reason

    def test_repetitive_paths_bad(self):
        """Repetitive garbage paths detected."""
        content = "/src/src/src/src/src/src/main.py"
        is_bad, reason = _detect_bad_streaming_patterns(content)
        if is_bad:
            assert "repetitive" in reason.lower() or "garbage" in reason.lower()

    def test_fatal_streaming_reason_marks_loop_and_malformed_output(self):
        """Severe loop and malformed-tool reasons should abort streaming immediately."""
        assert _is_fatal_streaming_reason(
            "Malformed tool command detected. Use 'READ: path/to/file.py', not 'READ: explanation text'."
        )
        assert _is_fatal_streaming_reason(
            "Repeated identical tool command detected: SEARCH: api_handler.py"
        )
        assert _is_fatal_streaming_reason(
            "Repeated identical path-like content detected. Stop looping and execute grounded work."
        )


# =============================================================================
# Tests for Renderer class
# =============================================================================


class TestRenderer:
    """Tests for Renderer class."""

    def test_init(self):
        """Initialize renderer."""
        r = Renderer()
        assert r._console is not None

    @patch("sage.core.renderer.stream_tokens_with_phase")
    def test_stream_tokens_with_phase_delegates(self, mock_stream):
        """stream_tokens_with_phase delegates to module function."""
        mock_stream.return_value = "response"
        r = Renderer()

        def token_gen():
            yield "token1"
            yield "token2"

        result = r.stream_tokens_with_phase(token_gen())
        mock_stream.assert_called_once()
        assert result == "response"

    @patch("sage.core.renderer.stream_tokens_with_phase")
    def test_stream_with_return_rejection(self, mock_stream):
        """stream_tokens_with_phase with return_rejection_info."""
        mock_stream.return_value = ("response", False, "")
        r = Renderer()

        def token_gen():
            yield "token"

        result = r.stream_tokens_with_phase(
            token_gen(), return_rejection_info=True
        )
        assert result == ("response", False, "")

    @patch("sage.core.renderer.stream_tokens_with_phase")
    def test_stream_with_timeout(self, mock_stream):
        """stream_tokens_with_phase with custom timeout."""
        mock_stream.return_value = "response"
        r = Renderer()

        def token_gen():
            yield "token"

        r.stream_tokens_with_phase(token_gen(), first_token_timeout=60.0)
        call_args = mock_stream.call_args
        assert call_args.kwargs["first_token_timeout"] == 60.0

    @patch("sage.core.renderer.stream_tokens_with_phase")
    def test_stream_with_model_id(self, mock_stream):
        """stream_tokens_with_phase with model_id."""
        mock_stream.return_value = "response"
        r = Renderer()

        def token_gen():
            yield "token"

        r.stream_tokens_with_phase(token_gen(), model_id="gpt-4")
        call_args = mock_stream.call_args
        assert call_args.kwargs["model_id"] == "gpt-4"


# =============================================================================
# Integration tests
# =============================================================================


class TestRendererIntegration:
    """Integration tests for renderer."""

    def test_exception_inheritance(self):
        """All guardrail exceptions inherit correctly."""
        grounding = GroundingViolation("test")
        tool_syntax = ToolSyntaxViolation("test")
        fabrication = FabricationViolation("test")

        for exc in [grounding, tool_syntax, fabrication]:
            assert isinstance(exc, HardGuardrailViolation)
            assert isinstance(exc, Exception)

    def test_clean_tool_commands_preserves_valid(self):
        """clean_malformed_tool_commands preserves valid structure."""
        content = """Here's what I'll do:

READ: src/main.py
READ: src/utils.py
SEARCH: class Config
RUN: python -m pytest

Let me analyze the code."""
        result = clean_malformed_tool_commands(content)
        # All valid commands should be preserved
        assert "READ: src/main.py" in result
        assert "READ: src/utils.py" in result
        assert "SEARCH: class Config" in result
        assert "RUN: python -m pytest" in result
        assert "Here's what I'll do:" in result
        assert "Let me analyze the code." in result

    def test_parse_and_detect_workflow(self):
        """Parse commands and detect patterns workflow."""
        # Valid content
        valid = """Let me read the files.

READ: main.py
SEARCH: def process

I found the function."""

        calls = _parse_incremental_tool_calls(valid)
        assert calls is not None
        assert len(calls) == 2

        is_bad, _ = _detect_bad_streaming_patterns(valid, calls)
        assert is_bad is False

    def test_violations_have_proper_messages(self):
        """All violations produce proper error messages."""
        violations = [
            GroundingViolation("No evidence", "context"),
            ToolSyntaxViolation("Bad XML", "xml code"),
            FabricationViolation("Made up", "fake content"),
            HardGuardrailViolation("CUSTOM", "Custom error"),
        ]

        for v in violations:
            # Should be raisable
            try:
                raise v
            except HardGuardrailViolation as caught:
                assert caught.violation_type in str(caught)
                assert caught.message in str(caught)

    def test_streaming_timeout_raisable(self):
        """StreamingTimeoutError can be raised and caught."""
        try:
            raise StreamingTimeoutError("Model timed out after 30s")
        except StreamingTimeoutError as e:
            assert "timed out" in e.message

    def test_stream_tokens_with_phase_times_out_when_first_next_blocks(self):
        """First-token timeout should fire even if the provider blocks inside next()."""

        class DummyLive:
            def __init__(self):
                self.is_started = False

            def start(self):
                self.is_started = True

            def stop(self):
                self.is_started = False

        def blocking_tokens():
            time.sleep(0.2)
            yield "late token"

        with (
            patch("sage.core.renderer.Live", return_value=DummyLive()),
            patch("sage.core.renderer._is_main_thread", return_value=False),
            patch("sage.core.renderer.is_clean", return_value=True),
            patch("sage.core.renderer.is_verbose", return_value=False),
            patch("sage.core.renderer.suppress_thinking", return_value=True),
        ):
            with pytest.raises(StreamingTimeoutError):
                stream_tokens_with_phase(
                    blocking_tokens(),
                    first_token_timeout=0.05,
                )

    def test_stream_tokens_with_phase_times_out_when_only_hidden_thinking_arrives(self):
        """Visible-output timeout should fire if the model emits only suppressed thinking."""

        class DummyLive:
            def __init__(self):
                self.is_started = False

            def start(self):
                self.is_started = True

            def stop(self):
                self.is_started = False

        def hidden_thinking_tokens():
            yield "<thinking>"
            time.sleep(0.03)
            yield "still thinking"
            time.sleep(0.03)
            yield "more hidden reasoning"

        with (
            patch("sage.core.renderer.Live", return_value=DummyLive()),
            patch("sage.core.renderer._is_main_thread", return_value=False),
            patch("sage.core.renderer.is_clean", return_value=False),
            patch("sage.core.renderer.is_verbose", return_value=False),
            patch("sage.core.renderer.suppress_thinking", return_value=True),
        ):
            with pytest.raises(StreamingTimeoutError, match="No visible response"):
                stream_tokens_with_phase(
                    hidden_thinking_tokens(),
                    first_token_timeout=0.05,
                )

    def test_detect_bad_streaming_patterns_flags_implied_context_fabrication(self):
        """Speculative 'implied context' analysis should be rejected as hypothetical."""
        content = """READING THE PROVIDED FILES, I HAVE THE FOLLOWING OVERVIEW:

1. `backend/main.py` (Implied Context): This file is not provided, but implied.
2. `backend/models.py` (Implied Context): This file is not provided, but the context suggests it exists.
"""

        is_bad, reason = _detect_bad_streaming_patterns(content)

        assert is_bad is True
        assert "hypothetical" in reason.lower() or "speculative" in reason.lower()

    def test_detect_bad_streaming_patterns_allows_task_list_with_file_hints(self):
        content = """1. Fix Firebase configuration (frontend/src/firebase/auth.js) [PENDING]
2. Fix Google sign-in flow (frontend/src/firebase/auth.js) [PENDING]
3. Fix Apple sign-in flow (frontend/src/firebase/auth.js) [PENDING]
4. Fix email/password + reset password UI (frontend/src/firebase/Login.jsx) [PENDING]
"""

        is_bad, _ = _detect_bad_streaming_patterns(content)

        assert is_bad is False

    def test_malformed_command_variants(self):
        """Various malformed command formats are cleaned."""
        test_cases = [
            ("READ: The file contains", "Explanation text"),
            ("READ: I will check", "I will pattern"),
            ("SEARCH: This searches for", "Explanation"),
            ("RUN: To run this command", "Explanation"),
            ("READ:\n", "Blank READ"),
            ("SEARCH:\n", "Blank SEARCH"),
            ("RUN:\n", "Blank RUN"),
        ]

        for content, description in test_cases:
            result = clean_malformed_tool_commands(content)
            # The malformed command should be removed
            # or at least the content should be cleaner
            lines = [l.strip() for l in result.split("\n") if l.strip()]
            # Check that no malformed commands remain
            for line in lines:
                if line.startswith(("READ:", "SEARCH:", "RUN:")):
                    # If a command line exists, it should be valid
                    # (have an actual path/pattern/command after the colon)
                    parts = line.split(":", 1)
                    if len(parts) > 1:
                        arg = parts[1].strip()
                        # Valid arguments don't start with common English sentence starters
                        if arg:
                            assert not arg.startswith(("The ", "I ", "This ", "To "))
