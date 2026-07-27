"""TDD tests for structured tool execution.

This file defines the target API for structured tool calls, replacing
the text-based READ:/SEARCH:/RUN: protocol with typed, validated objects.

The goal is to make the runtime own tool execution completely, rather than
parsing free-text commands from model output.

Run with: pytest sage/tests/test_structured_tools.py -v
"""

from __future__ import annotations

from pathlib import Path

import pytest

# =============================================================================
# TEST 1: ToolCall dataclass structure
# =============================================================================


class TestToolCallStructure:
    """Tests that tool calls are structured, typed objects."""

    def test_tool_call_dataclass_exists(self):
        """ToolCall must be a dataclass with typed fields."""
        from sage.core.tools import ToolCall, ToolType

        # Create a READ tool call
        call = ToolCall(
            tool_type=ToolType.READ,
            arguments={"path": "sage/main.py"},
        )

        assert call.tool_type == ToolType.READ
        assert call.arguments["path"] == "sage/main.py"
        assert call.validated is False  # Default

    def test_tool_type_enum_covers_all_tools(self):
        """ToolType enum must include all supported tools."""
        from sage.core.tools import ToolType

        # All supported tool types
        expected_types = {"READ", "SEARCH", "RUN", "FILE", "SHELL"}

        actual_types = {t.name for t in ToolType}

        assert expected_types.issubset(actual_types), (
            f"Missing tool types: {expected_types - actual_types}"
        )

    def test_tool_call_validation(self):
        """ToolCall must support validation."""
        from sage.core.tools import ToolCall, ToolType, validate_tool_call

        # Valid READ call
        valid_call = ToolCall(
            tool_type=ToolType.READ,
            arguments={"path": "sage/main.py"},
        )

        validated = validate_tool_call(valid_call)
        assert validated.validated is True

        # Invalid READ call (missing path)
        invalid_call = ToolCall(
            tool_type=ToolType.READ,
            arguments={},
        )

        with pytest.raises(ValueError) as exc_info:
            validate_tool_call(invalid_call)

        assert "path" in str(exc_info.value).lower()

    def test_tool_call_serialization(self):
        """ToolCall must be JSON-serializable."""
        from sage.core.tools import ToolCall, ToolType

        call = ToolCall(
            tool_type=ToolType.SEARCH,
            arguments={"pattern": "def main", "path": "."},
        )

        # Should be serializable
        serialized = call.to_dict()
        assert serialized["tool_type"] == "SEARCH"
        assert serialized["arguments"]["pattern"] == "def main"

        # Should be deserializable
        restored = ToolCall.from_dict(serialized)
        assert restored.tool_type == ToolType.SEARCH
        assert restored.arguments["pattern"] == "def main"


# =============================================================================
# TEST 2: Text-to-structured conversion
# =============================================================================


class TestTextToStructuredConversion:
    """Tests that text commands are converted to structured calls."""

    def test_parse_read_command(self):
        """READ: text should become ToolCall."""
        from sage.core.tools import ToolType, parse_tool_command

        text = "READ: sage/main.py"
        call = parse_tool_command(text)

        assert call is not None
        assert call.tool_type == ToolType.READ
        assert call.arguments["path"] == "sage/main.py"

    def test_parse_search_command(self):
        """SEARCH: text should become ToolCall."""
        from sage.core.tools import ToolType, parse_tool_command

        text = "SEARCH: def _validate"
        call = parse_tool_command(text)

        assert call is not None
        assert call.tool_type == ToolType.SEARCH
        assert call.arguments["pattern"] == "def _validate"

    def test_parse_run_command(self):
        """RUN: text should become ToolCall."""
        from sage.core.tools import ToolType, parse_tool_command

        text = "RUN: pytest sage/tests/test_main.py -v"
        call = parse_tool_command(text)

        assert call is not None
        assert call.tool_type == ToolType.RUN
        assert "pytest" in call.arguments["command"]

    def test_parse_file_block(self):
        """FILE: block should become ToolCall."""
        from sage.core.tools import ToolType, parse_tool_command

        text = """FILE: test_output.py
def test_something():
    pass
"""
        call = parse_tool_command(text)

        assert call is not None
        assert call.tool_type == ToolType.FILE
        assert call.arguments["path"] == "test_output.py"
        assert "def test_something" in call.arguments["content"]

    def test_invalid_syntax_returns_none(self):
        """Invalid tool syntax should return None, not raise."""
        from sage.core.tools import parse_tool_command

        # XML syntax (invalid)
        assert parse_tool_command("<execute_tool>read</execute_tool>") is None

        # YAML syntax (invalid)
        assert parse_tool_command("tool_name: read_file\nparameters:") is None

        # Plain text (not a command)
        assert parse_tool_command("I will read the file") is None

    def test_batch_parse_multiple_commands(self):
        """Multiple commands should be parsed as a list."""
        from sage.core.tools import ToolType, parse_tool_commands

        text = """READ: file1.py
READ: file2.py
SEARCH: pattern
RUN: pytest
"""
        calls = parse_tool_commands(text)

        assert len(calls) == 4
        assert calls[0].tool_type == ToolType.READ
        assert calls[1].tool_type == ToolType.READ
        assert calls[2].tool_type == ToolType.SEARCH
        assert calls[3].tool_type == ToolType.RUN


# =============================================================================
# TEST 3: Tool execution with structured calls
# =============================================================================


class TestStructuredToolExecution:
    """Tests that structured tool calls are executed correctly."""

    def test_execute_read_tool(self):
        """Execute READ tool call."""
        from sage.core.tools import ToolCall, ToolType, execute_tool_call

        call = ToolCall(
            tool_type=ToolType.READ,
            arguments={"path": "sage/__init__.py"},
            validated=True,
        )

        result = execute_tool_call(call)

        assert result.success is True
        assert result.output is not None
        assert len(result.output) > 0

    def test_execute_search_tool(self, tmp_path):
        from sage.core.tools import ToolCall, ToolType, execute_tool_call
        (tmp_path / "my_file.py").write_text("def my_test_function(): pass")

        call = ToolCall(
            tool_type=ToolType.SEARCH,
            arguments={"pattern": "def my_test_function", "path": str(tmp_path)},
            validated=True,
        )

        result = execute_tool_call(call)

        assert result.success is True
        assert "my_file.py" in result.output

    def test_unvalidated_call_raises(self):
        """Unvalidated tool calls should not execute."""
        from sage.core.tools import ToolCall, ToolType, execute_tool_call

        call = ToolCall(
            tool_type=ToolType.READ,
            arguments={"path": "sage/main.py"},
            validated=False,  # Not validated
        )

        with pytest.raises(ValueError) as exc_info:
            execute_tool_call(call)

        assert "not validated" in str(exc_info.value).lower()


# =============================================================================
# TEST 4: Execution ledger tracking
# =============================================================================


class TestExecutionLedger:
    """Tests that tool execution is tracked in a ledger."""

    def test_ledger_tracks_file_reads(self):
        """Ledger must track files read."""
        from sage.core.tools import ExecutionLedger, ToolCall, ToolType

        ledger = ExecutionLedger()

        call = ToolCall(
            tool_type=ToolType.READ,
            arguments={"path": "sage/main.py"},
            validated=True,
        )

        ledger.record_execution(call, success=True)

        assert "sage/main.py" in ledger.files_read
        assert ledger.total_reads == 1

    def test_ledger_tracks_file_writes(self):
        """Ledger must track files written."""
        from sage.core.tools import ExecutionLedger, ToolCall, ToolType

        ledger = ExecutionLedger()

        call = ToolCall(
            tool_type=ToolType.FILE,
            arguments={"path": "output.py", "content": "# test"},
            validated=True,
        )

        ledger.record_execution(call, success=True)

        assert "output.py" in ledger.files_written
        assert ledger.total_writes == 1

    def test_ledger_tracks_commands(self):
        """Ledger must track commands run."""
        from sage.core.tools import ExecutionLedger, ToolCall, ToolType

        ledger = ExecutionLedger()

        call = ToolCall(
            tool_type=ToolType.RUN,
            arguments={"command": "pytest tests/"},
            validated=True,
        )

        ledger.record_execution(call, success=True, output="5 passed")

        assert "pytest tests/" in ledger.commands_run
        assert ledger.total_commands == 1

    def test_ledger_derives_claims(self):
        """Claims must be derivable from ledger."""
        from sage.core.tools import ExecutionLedger, ToolCall, ToolType

        ledger = ExecutionLedger()

        # Simulate reading files
        for path in ["file1.py", "file2.py", "file3.py"]:
            call = ToolCall(
                tool_type=ToolType.READ,
                arguments={"path": path},
                validated=True,
            )
            ledger.record_execution(call, success=True)

        # Claim: "I analyzed 3 files"
        assert ledger.can_claim_read_count(3) is True
        assert ledger.can_claim_read_count(5) is False

    def test_ledger_serialization(self):
        """Ledger must be serializable for debugging."""
        from sage.core.tools import ExecutionLedger, ToolCall, ToolType

        ledger = ExecutionLedger()

        call = ToolCall(
            tool_type=ToolType.READ,
            arguments={"path": "test.py"},
            validated=True,
        )
        ledger.record_execution(call, success=True)

        data = ledger.to_dict()

        assert "files_read" in data
        assert "test.py" in data["files_read"]

    def test_ledger_binds_project_root_once(self):
        """P1-7: Project root should be bound once and cached."""
        from sage.core.tools import ExecutionLedger

        ledger = ExecutionLedger()

        # First bind sets the root
        root1 = ledger.bind_project_root("/test/path1")
        assert root1 == "/test/path1"
        assert ledger.project_root == "/test/path1"

        # Second bind returns cached value, doesn't change it
        root2 = ledger.bind_project_root("/test/path2")
        assert root2 == "/test/path1"  # Still the first value
        assert ledger.project_root == "/test/path1"

    def test_ledger_binds_default_root(self):
        """Project root should default to cwd if not provided."""
        from sage.core.tools import ExecutionLedger

        ledger = ExecutionLedger()

        root = ledger.bind_project_root()

        assert root is not None
        assert Path(root).exists()

    def test_ledger_get_project_root(self):
        """get_project_root returns None before binding."""
        from sage.core.tools import ExecutionLedger

        ledger = ExecutionLedger()

        # Not bound yet
        assert ledger.get_project_root() is None

        # After binding
        ledger.bind_project_root("/test/path")
        assert ledger.get_project_root() == "/test/path"


# =============================================================================
# TEST 5: Pre-display validation with structured awareness
# =============================================================================


class TestStructuredPreDisplayValidation:
    """Tests that pre-display validation understands structured tools."""

    def test_repeated_paths_allowed_in_batch_read(self):
        """Repeated path segments in batch READ should not abort."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        # This pattern caused false positive aborts
        content = """READ: ai-platform/backend/config.py
READ: ai-platform/backend/models.py
READ: ai-platform/backend/schemas.py
READ: ai-platform/backend/app.py
READ: ai-platform/backend/auth.py
"""

        # Parse as structured commands first
        from sage.core.tools import parse_tool_commands

        calls = parse_tool_commands(content)

        # If we have valid tool calls, the repeated "backend" is legitimate
        assert len(calls) == 5

        # The validator should be aware of this context
        # This test documents the requirement - implementation may vary
        is_bad, reason = _detect_bad_streaming_patterns(content, tool_calls=calls)

        # Should NOT abort for legitimate batch reads
        assert not is_bad, f"Should not abort batch reads: {reason}"

    def test_xml_tool_syntax_still_blocked(self):
        """XML tool syntax should still be blocked."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        content = "<execute_tool>read</execute_tool>"

        is_bad, reason = _detect_bad_streaming_patterns(content)

        assert is_bad, "XML tool syntax must be blocked"

    def test_described_tools_still_blocked(self):
        """'I will use READ' should still be blocked."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        content = "I will use the READ tool to examine the file"

        is_bad, reason = _detect_bad_streaming_patterns(content)

        assert is_bad, "Described tools must be blocked"


# =============================================================================
# TEST 6: Integration with existing runtime
# =============================================================================


class TestStructuredToolsIntegration:
    """Tests integration with existing SAGE runtime."""

    def test_extract_tool_commands_returns_structured(self):
        """_extract_tool_commands should return ToolCall objects."""
        from sage.core.tools import ToolCall, ToolType
        from sage.cli_core import _extract_tool_commands_structured

        text = """Let me read the files:
READ: sage/main.py
SEARCH: def _validate
RUN: pytest tests/
"""
        calls = _extract_tool_commands_structured(text)

        assert len(calls) == 3
        assert all(isinstance(c, ToolCall) for c in calls)
        assert calls[0].tool_type == ToolType.READ
        assert calls[0].arguments["path"] == "sage/main.py"
        assert calls[1].tool_type == ToolType.SEARCH
        assert calls[1].arguments["pattern"] == "def _validate"
        assert calls[2].tool_type == ToolType.RUN
        assert calls[2].arguments["command"] == "pytest tests/"

    def test_runtime_uses_execution_ledger(self):
        """Runtime should update ExecutionLedger on tool execution."""
        from sage.core.tools import ExecutionLedger, ToolCall, ToolType

        ledger = ExecutionLedger()

        # Simulate tool execution
        read_call = ToolCall(
            tool_type=ToolType.READ,
            arguments={"path": "sage/main.py"},
            validated=True,
        )
        ledger.record_execution(read_call, success=True)

        assert "sage/main.py" in ledger.files_read
        assert ledger.can_claim_read_count(1)

    def test_backward_compatible_parsing(self):
        """Existing text commands should still work."""
        from sage.core.tools import ToolType, parse_tool_command

        # These are the existing formats
        old_formats = [
            ("READ: path/to/file.py", ToolType.READ),
            ("SEARCH: pattern", ToolType.SEARCH),
            ("RUN: pytest", ToolType.RUN),
        ]

        for text, expected_type in old_formats:
            call = parse_tool_command(text)
            assert call is not None, f"Failed to parse: {text}"
            assert call.tool_type == expected_type

    def test_validation_functions_accept_structured_calls(self):
        """Validation functions should work with structured calls."""
        from sage.cli_core import _detect_tool_description_vs_execution

        # Response with actual tool commands
        response = """READ: file1.py
READ: file2.py

Based on the files above..."""

        is_descriptive, tools = _detect_tool_description_vs_execution(response)

        # Should NOT be flagged as descriptive when tools are present
        assert is_descriptive is False


class TestStripInlineDescription:
    """Tests for stripping trailing parenthetical prose from RUN: commands.

    The model sometimes emits commands with a trailing English description:
        RUN: ls -laR | head -200 (list top 200 lines of the project)

    The literal `(...)` is then passed to /bin/sh -c, which fails with a
    syntax error. The extractor must strip the prose annotation while
    leaving legitimate shell parens intact (e.g. `find . \\( -name "*.py" \\)`).
    """

    def test_strips_simple_prose_annotation(self):
        from sage.cli_core import _strip_inline_description
        assert _strip_inline_description(
            "ls -laR | head -200 (list top 200 lines of the project)"
        ) == "ls -laR | head -200"

    def test_strips_annotation_after_find_command(self):
        from sage.cli_core import _strip_inline_description
        assert _strip_inline_description(
            "find . -maxdepth 2 -type d | head -80 (top 80 directories)"
        ) == "find . -maxdepth 2 -type d | head -80"

    def test_leaves_escaped_find_grouping_intact(self):
        from sage.cli_core import _strip_inline_description
        cmd = "find . \\( -name '*.py' -o -name '*.js' \\)"
        assert _strip_inline_description(cmd) == cmd

    def test_leaves_command_substitution_intact(self):
        from sage.cli_core import _strip_inline_description
        cmd = 'echo "today is $(date)"'
        assert _strip_inline_description(cmd) == cmd

    def test_leaves_subshell_with_shell_metachars_intact(self):
        from sage.cli_core import _strip_inline_description
        cmd = "(cd /tmp && ls -la)"
        assert _strip_inline_description(cmd) == cmd

    def test_leaves_single_word_paren_intact(self):
        # A single bare token like `(verbose)` is ambiguous — don't strip.
        # But a multi-word English phrase is clearly prose.
        from sage.cli_core import _strip_inline_description
        cmd = "make build (verbose)"
        # Single token — leave as-is, too risky to strip.
        assert _strip_inline_description(cmd) == cmd

    def test_strips_multi_word_natural_language(self):
        from sage.cli_core import _strip_inline_description
        assert _strip_inline_description(
            "pytest tests/ -v (run all tests with verbose output)"
        ) == "pytest tests/ -v"

    def test_no_paren_at_end_is_unchanged(self):
        from sage.cli_core import _strip_inline_description
        cmd = "npm install"
        assert _strip_inline_description(cmd) == cmd


class TestExtractToolCommandsStripsParenAnnotation:
    """End-to-end: _extract_tool_commands and _extract_tool_commands_structured
    must strip trailing prose annotations from RUN: commands before returning.
    """

    def test_extract_tool_commands_strips_prose_paren(self):
        from sage.cli_core import _extract_tool_commands
        text = "RUN: ls -laR | head -200 (list top 200 lines of the project)\n"
        cmds = _extract_tool_commands(text)
        assert cmds == [("RUN", "ls -laR | head -200")]

    def test_extract_tool_commands_structured_strips_prose_paren(self):
        from sage.core.tools import ToolType
        from sage.cli_core import _extract_tool_commands_structured
        text = "RUN: find . -maxdepth 2 -type d | head -80 (top 80 directories)\n"
        calls = _extract_tool_commands_structured(text)
        assert len(calls) == 1
        assert calls[0].tool_type == ToolType.RUN
        assert calls[0].arguments["command"] == "find . -maxdepth 2 -type d | head -80"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
