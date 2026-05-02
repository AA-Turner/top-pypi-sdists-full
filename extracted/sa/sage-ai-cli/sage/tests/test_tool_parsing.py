"""Tests for tool parsing and validation - P0 items 18-25.

Tests verify:
- Tool command extraction is robust
- Tool validation catches malformed commands
- Tool error handling is comprehensive
- Tool result validation works correctly
- Tool output parsing is accurate
- Tool selection heuristics are appropriate
"""

import tempfile
import time
from pathlib import Path

from sage.core.tool_validation import (
    ToolCall,
    ToolChain,
    ToolExecutionValidator,
    ToolExecutor,
    ToolOutputParser,
    ToolSelectionHeuristics,
    ToolStatus,
    ToolType,
    execute_tool,
    validate_tool_execution,
)


class TestToolCommandExtraction:
    """P0 item 18: Robust tool command extraction."""

    def test_extract_read_commands(self):
        """Should extract READ tool commands."""
        validator = ToolExecutionValidator()

        content = """
        Let me read the file:
        READ: `src/main.py`
        Reading file: config.json
        """

        mentions = validator.extract_tool_mentions(content)

        assert len(mentions) >= 2
        read_mentions = [m for m in mentions if m.tool_type == ToolType.READ]
        assert len(read_mentions) >= 2

    def test_extract_search_commands(self):
        """Should extract SEARCH tool commands."""
        validator = ToolExecutionValidator()

        content = """
        SEARCH: def main
        Searching for: class Handler
        """

        mentions = validator.extract_tool_mentions(content)

        search_mentions = [m for m in mentions if m.tool_type == ToolType.SEARCH]
        assert len(search_mentions) >= 2

    def test_extract_write_commands(self):
        """Should extract WRITE (FILE:) tool commands."""
        validator = ToolExecutionValidator()

        content = """
        Creating file: `new_file.py`
        FILE: `src/module.py`
        """

        mentions = validator.extract_tool_mentions(content)

        write_mentions = [m for m in mentions if m.tool_type == ToolType.WRITE]
        assert len(write_mentions) >= 1

    def test_extract_run_commands(self):
        """Should extract RUN tool commands."""
        validator = ToolExecutionValidator()

        content = """
        Running: pytest tests/
        RUN: `npm install`
        """

        mentions = validator.extract_tool_mentions(content)

        run_mentions = [m for m in mentions if m.tool_type == ToolType.RUN]
        assert len(run_mentions) >= 2

    def test_handles_malformed_commands(self):
        """Should handle malformed commands gracefully."""
        validator = ToolExecutionValidator()

        # Various edge cases
        content = """
        READ:
        READ:`file without space`
        SEARCH:pattern
        """

        # Should not crash
        mentions = validator.extract_tool_mentions(content)
        assert isinstance(mentions, list)

    def test_extracts_file_paths_with_special_chars(self):
        """Should extract file paths with special characters."""
        validator = ToolExecutionValidator()

        content = """
        READ: `src/components/MyComponent-v2.tsx`
        READ: `config.d.ts`
        READ: `__init__.py`
        """

        mentions = validator.extract_tool_mentions(content)
        read_mentions = [m for m in mentions if m.tool_type == ToolType.READ]
        assert len(read_mentions) >= 3


class TestToolValidation:
    """P0 item 19: Tool validation before execution."""

    def test_validates_executed_vs_mentioned(self):
        """Should validate which mentioned tools were executed."""
        validator = ToolExecutionValidator()

        content = """
        READ: `src/main.py`
        SEARCH: def main
        RUN: pytest
        """

        # Only some tools were actually executed
        executed = [
            ToolCall(tool_type=ToolType.READ, command="src/main.py", status=ToolStatus.SUCCESS),
        ]

        executed_mentions, unexecuted_mentions = validator.validate_execution(content, executed)

        assert len(executed_mentions) >= 1
        assert len(unexecuted_mentions) >= 2  # SEARCH and RUN weren't executed

    def test_validate_tool_execution_function(self):
        """The validate_tool_execution helper should work correctly."""
        content = """
        READ: `file1.py`
        READ: `file2.py`
        """

        executed = [
            ToolCall(tool_type=ToolType.READ, command="file1.py", status=ToolStatus.SUCCESS),
        ]

        result = validate_tool_execution(content, executed)

        assert result["executed_count"] >= 1
        assert result["unexecuted_count"] >= 1
        assert not result["all_tools_executed"]


class TestToolErrorHandling:
    """P0 item 20: Comprehensive tool error handling."""

    def test_handles_missing_handler(self):
        """Should handle missing tool handler gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            executor = ToolExecutor(Path(tmpdir))

            # SEARCH doesn't have a default handler
            call = ToolCall(tool_type=ToolType.SEARCH, command="test pattern")
            result = executor.execute(call)

            assert result.status == ToolStatus.FAILED
            assert "No handler registered" in result.error

    def test_handles_file_not_found(self):
        """Should handle file not found errors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            executor = ToolExecutor(Path(tmpdir))

            call = ToolCall(tool_type=ToolType.READ, command="nonexistent.py")
            result = executor.execute(call)

            assert result.status == ToolStatus.FAILED
            assert "not found" in result.error.lower()

    def test_retries_on_failure(self):
        """Should retry on failure up to max_attempts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            executor = ToolExecutor(Path(tmpdir))

            call = ToolCall(
                tool_type=ToolType.READ,
                command="nonexistent.py",
                max_attempts=2,
            )

            result = executor.execute(call)

            assert result.attempt == 2  # Should have tried twice

    def test_records_error_message(self):
        """Should record detailed error messages."""
        with tempfile.TemporaryDirectory() as tmpdir:
            executor = ToolExecutor(Path(tmpdir))

            call = ToolCall(tool_type=ToolType.READ, command="bad/path/file.py")
            result = executor.execute(call)

            assert result.status == ToolStatus.FAILED
            assert result.error is not None
            assert len(result.error) > 0


class TestToolResultValidation:
    """P0 item 21: Tool result validation."""

    def test_successful_read_returns_content(self):
        """Successful READ should return file content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test file
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("print('hello')")

            executor = ToolExecutor(Path(tmpdir))
            call = ToolCall(tool_type=ToolType.READ, command="test.py")
            result = executor.execute(call)

            assert result.status == ToolStatus.SUCCESS
            assert result.result is not None
            assert "print" in result.result

    def test_verify_returns_boolean(self):
        """VERIFY should return boolean indicating existence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "exists.py"
            test_file.write_text("# exists")

            executor = ToolExecutor(Path(tmpdir))

            # Existing file
            call = ToolCall(tool_type=ToolType.VERIFY, command="exists.py")
            result = executor.execute(call)
            assert result.status == ToolStatus.SUCCESS
            assert result.result is True

            # Non-existing file
            call2 = ToolCall(tool_type=ToolType.VERIFY, command="nonexistent.py")
            result2 = executor.execute(call2)
            assert result2.status == ToolStatus.SUCCESS
            assert result2.result is False

    def test_list_returns_file_list(self):
        """LIST should return matching files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            (Path(tmpdir) / "file1.py").write_text("# 1")
            (Path(tmpdir) / "file2.py").write_text("# 2")
            (Path(tmpdir) / "other.txt").write_text("text")

            executor = ToolExecutor(Path(tmpdir))
            call = ToolCall(tool_type=ToolType.LIST, command="*.py")
            result = executor.execute(call)

            assert result.status == ToolStatus.SUCCESS
            assert isinstance(result.result, list)
            assert len(result.result) == 2
            assert all(f.endswith(".py") for f in result.result)

    def test_tracks_execution_duration(self):
        """Should track execution duration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("content")

            executor = ToolExecutor(Path(tmpdir))
            call = ToolCall(tool_type=ToolType.READ, command="test.py")
            result = executor.execute(call)

            assert result.started_at is not None
            assert result.completed_at is not None
            assert result.duration is not None
            assert result.duration >= 0


class TestToolOutputParsing:
    """P0 item 22: Accurate tool output parsing."""

    def test_parse_python_file_output(self):
        """Should parse Python file content correctly."""
        parser = ToolOutputParser()

        content = """
import os
from pathlib import Path

class MyClass:
    pass

def my_function():
    pass
"""

        result = parser.parse_read_output(content, "test.py")

        assert result["file_path"] == "test.py"
        assert result["has_code"] is True
        assert "os" in result["imports"]
        assert "pathlib" in result["imports"]
        assert "MyClass" in result["classes"]
        assert "my_function" in result["functions"]

    def test_parse_search_output(self):
        """Should parse search results correctly."""
        parser = ToolOutputParser()

        results = [
            {"file_path": "src/main.py", "line_number": 10, "content": "def main()"},
            {"file_path": "src/main.py", "line_number": 20, "content": "main()"},
            {"file_path": "src/utils.py", "line_number": 5, "content": "from main import"},
        ]

        parsed = parser.parse_search_output(results)

        assert parsed["total_matches"] == 3
        assert parsed["unique_files"] == 2
        assert "src/main.py" in parsed["files"]
        assert "src/utils.py" in parsed["files"]

    def test_parse_non_python_file(self):
        """Should handle non-Python files."""
        parser = ToolOutputParser()

        content = '{"key": "value"}'
        result = parser.parse_read_output(content, "config.json")

        assert result["file_path"] == "config.json"
        assert result["imports"] == []  # No imports for JSON
        assert result["functions"] == []

    def test_detect_code_files(self):
        """Should detect code files by extension."""
        parser = ToolOutputParser()

        code_files = ["test.py", "app.js", "module.ts", "main.go", "lib.rs"]
        non_code_files = ["readme.md", "config.yaml", "data.csv"]

        for f in code_files:
            result = parser.parse_read_output("content", f)
            assert result["has_code"] is True, f"Expected {f} to be detected as code"

        for f in non_code_files:
            result = parser.parse_read_output("content", f)
            assert result["has_code"] is False, f"Expected {f} to not be detected as code"


class TestToolSelectionHeuristics:
    """P0 item 23: Appropriate tool selection."""

    def test_suggests_read_for_file_mentions(self):
        """Should suggest READ for mentioned files."""
        heuristics = ToolSelectionHeuristics()

        suggestions = heuristics.suggest_tools("Check `src/main.py` for errors")

        read_suggestions = [s for s in suggestions if s.tool_type == ToolType.READ]
        assert len(read_suggestions) >= 1
        assert any("main.py" in s.command for s in read_suggestions)

    def test_suggests_search_for_find_tasks(self):
        """Should suggest SEARCH for find tasks."""
        heuristics = ToolSelectionHeuristics()

        suggestions = heuristics.suggest_tools("Find all usages of 'calculate_total'")

        search_suggestions = [s for s in suggestions if s.tool_type == ToolType.SEARCH]
        assert len(search_suggestions) >= 1

    def test_suggests_verify_for_existence_checks(self):
        """Should suggest VERIFY for existence checks."""
        heuristics = ToolSelectionHeuristics()

        suggestions = heuristics.suggest_tools("Check if `config.json` exists")

        verify_suggestions = [s for s in suggestions if s.tool_type == ToolType.VERIFY]
        assert len(verify_suggestions) >= 1

    def test_suggests_list_for_listing_tasks(self):
        """Should suggest LIST for listing tasks."""
        heuristics = ToolSelectionHeuristics()

        suggestions = heuristics.suggest_tools("List all *.py files in the project")

        list_suggestions = [s for s in suggestions if s.tool_type == ToolType.LIST]
        assert len(list_suggestions) >= 1


class TestToolChaining:
    """P0 item 24: Tool chaining works correctly."""

    def test_chain_sequential_execution(self):
        """Tools should execute sequentially by default."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            (Path(tmpdir) / "file1.py").write_text("# file 1")
            (Path(tmpdir) / "file2.py").write_text("# file 2")

            executor = ToolExecutor(Path(tmpdir))

            chain = ToolChain()
            chain.add_call(ToolCall(tool_type=ToolType.READ, command="file1.py"))
            chain.add_call(ToolCall(tool_type=ToolType.READ, command="file2.py"))

            result = executor.execute_chain(chain, parallel=False)

            assert result.is_complete()
            assert all(c.status == ToolStatus.SUCCESS for c in result.calls)

    def test_chain_respects_dependencies(self):
        """Chain should respect dependencies."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "file.py").write_text("content")

            executor = ToolExecutor(Path(tmpdir))

            chain = ToolChain()
            idx0 = chain.add_call(ToolCall(tool_type=ToolType.VERIFY, command="file.py"))
            chain.add_call(
                ToolCall(tool_type=ToolType.READ, command="file.py"),
                depends_on=[idx0],
            )

            result = executor.execute_chain(chain, parallel=False)

            # First should complete before second
            assert result.calls[0].status == ToolStatus.SUCCESS
            assert result.calls[1].status == ToolStatus.SUCCESS

    def test_chain_skips_on_failed_dependency(self):
        """Chain should skip calls with failed dependencies."""
        with tempfile.TemporaryDirectory() as tmpdir:
            executor = ToolExecutor(Path(tmpdir))

            chain = ToolChain()
            idx0 = chain.add_call(ToolCall(tool_type=ToolType.READ, command="nonexistent.py"))
            chain.add_call(
                ToolCall(tool_type=ToolType.VERIFY, command="test.py"),
                depends_on=[idx0],
            )

            result = executor.execute_chain(chain, parallel=False)

            assert result.calls[0].status == ToolStatus.FAILED
            assert result.calls[1].status == ToolStatus.SKIPPED

    def test_get_ready_calls(self):
        """Should correctly identify ready calls."""
        chain = ToolChain()
        idx0 = chain.add_call(ToolCall(tool_type=ToolType.READ, command="a.py"))
        idx1 = chain.add_call(ToolCall(tool_type=ToolType.READ, command="b.py"))
        chain.add_call(
            ToolCall(tool_type=ToolType.VERIFY, command="c.py"),
            depends_on=[idx0, idx1],
        )

        # Initially, first two are ready
        ready = chain.get_ready_calls()
        assert 0 in ready
        assert 1 in ready
        assert 2 not in ready


class TestToolTimeouts:
    """P0 item 25: Tool timeout handling."""

    def test_timeout_is_tracked(self):
        """Timeout should be tracked in tool call."""
        call = ToolCall(tool_type=ToolType.READ, command="test.py")

        assert call.status == ToolStatus.PENDING
        assert call.started_at is None
        assert call.completed_at is None

    def test_executor_has_default_timeout(self):
        """Executor should have default timeout."""
        with tempfile.TemporaryDirectory() as tmpdir:
            executor = ToolExecutor(Path(tmpdir))
            assert executor.DEFAULT_TIMEOUT == 30.0

    def test_timeout_status_recorded(self):
        """Timeout status should be recorded."""
        # This test verifies the timeout handling logic exists
        with tempfile.TemporaryDirectory() as tmpdir:
            executor = ToolExecutor(Path(tmpdir))

            # Register a slow handler
            def slow_handler(_call):
                time.sleep(5)
                return "done"

            executor.register_handler(ToolType.SEARCH, slow_handler)

            call = ToolCall(tool_type=ToolType.SEARCH, command="test")
            result = executor.execute(call, timeout=0.1)

            assert result.status == ToolStatus.TIMEOUT
            assert "timed out" in result.error.lower()


class TestExecuteTool:
    """Test the convenience execute_tool function."""

    def test_execute_tool_reads_file(self):
        """execute_tool should read files correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.txt"
            test_file.write_text("test content")

            result = execute_tool(Path(tmpdir), ToolType.READ, "test.txt")

            assert result.status == ToolStatus.SUCCESS
            assert "test content" in result.result

    def test_execute_tool_handles_errors(self):
        """execute_tool should handle errors gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = execute_tool(Path(tmpdir), ToolType.READ, "nonexistent.py")

            assert result.status == ToolStatus.FAILED
            assert result.error is not None


class TestToolCallDataclass:
    """Test the ToolCall dataclass behavior."""

    def test_default_values(self):
        """ToolCall should have correct default values."""
        call = ToolCall(tool_type=ToolType.READ, command="test.py")

        assert call.status == ToolStatus.PENDING
        assert call.attempt == 0
        assert call.max_attempts == 3
        assert call.result is None
        assert call.error is None

    def test_is_complete_property(self):
        """is_complete should work correctly."""
        call = ToolCall(tool_type=ToolType.READ, command="test.py")

        call.status = ToolStatus.PENDING
        assert not call.is_complete

        call.status = ToolStatus.RUNNING
        assert not call.is_complete

        call.status = ToolStatus.SUCCESS
        assert call.is_complete

        call.status = ToolStatus.FAILED
        assert call.is_complete

        call.status = ToolStatus.TIMEOUT
        assert call.is_complete

        call.status = ToolStatus.SKIPPED
        assert call.is_complete

    def test_duration_property(self):
        """duration should calculate correctly."""
        call = ToolCall(tool_type=ToolType.READ, command="test.py")

        # No times set
        assert call.duration is None

        # Set times
        call.started_at = 100.0
        call.completed_at = 102.5

        assert call.duration == 2.5
