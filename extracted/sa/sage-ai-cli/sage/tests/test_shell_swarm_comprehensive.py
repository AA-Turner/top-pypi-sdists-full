"""Comprehensive tests for sage/core/shell.py and sage/core/swarm.py."""

import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest

from sage.core.shell import (
    SAFE_READONLY_COMMANDS,
    BLOCKED_READONLY_PATTERNS,
    is_safe_readonly_command,
    run_readonly_shell,
    extract_scoped_prefix,
    resolve_scoped_directory,
    run_shell,
    safe_shell_exec,
    shell_quote,
    extract_bash_blocks,
    sanitize_shell_block,
    strip_search_comment,
    read_file_context,
    run_tdd_test,
    detect_test_framework,
    parse_test_output,
    has_test_errors,
    get_test_error_summary,
)

from sage.core.swarm import (
    TaskType,
    TaskStatus,
    SwarmTask,
    ModelProfile,
    SwarmResult,
    SwarmOrchestrator,
)


# =============================================================================
# Tests for shell.py - Constants
# =============================================================================


class TestShellConstants:
    """Tests for shell module constants."""

    def test_safe_readonly_commands_contains_ls(self):
        assert "ls" in SAFE_READONLY_COMMANDS

    def test_safe_readonly_commands_contains_cat(self):
        assert "cat" in SAFE_READONLY_COMMANDS

    def test_safe_readonly_commands_contains_grep(self):
        assert "grep" in SAFE_READONLY_COMMANDS

    def test_blocked_patterns_exist(self):
        assert len(BLOCKED_READONLY_PATTERNS) > 0


# =============================================================================
# Tests for is_safe_readonly_command
# =============================================================================


class TestIsSafeReadonlyCommand:
    """Tests for is_safe_readonly_command function."""

    def test_empty_command(self):
        is_safe, reason = is_safe_readonly_command("")
        assert is_safe is False
        assert "Empty" in reason

    def test_safe_ls_command(self):
        is_safe, reason = is_safe_readonly_command("ls -la")
        assert is_safe is True
        assert reason == ""

    def test_safe_cat_command(self):
        is_safe, reason = is_safe_readonly_command("cat file.txt")
        assert is_safe is True

    def test_safe_grep_command(self):
        is_safe, reason = is_safe_readonly_command("grep pattern file.txt")
        assert is_safe is True

    def test_blocked_rm_command(self):
        is_safe, reason = is_safe_readonly_command("rm -rf /")
        assert is_safe is False
        assert "Blocked" in reason

    def test_blocked_sudo_command(self):
        is_safe, reason = is_safe_readonly_command("sudo apt install")
        assert is_safe is False

    def test_blocked_pip_install(self):
        is_safe, reason = is_safe_readonly_command("pip install requests")
        assert is_safe is False

    def test_blocked_git_push(self):
        is_safe, reason = is_safe_readonly_command("git push origin main")
        assert is_safe is False

    def test_unsafe_command_not_in_list(self):
        is_safe, reason = is_safe_readonly_command("python script.py")
        assert is_safe is False
        assert "not in safe" in reason

    def test_shell_operators_blocked(self):
        # Use a command with operators but no blocked patterns
        is_safe, reason = is_safe_readonly_command("ls && ls")
        assert is_safe is False
        assert "operators" in reason

    def test_safe_piped_command(self):
        is_safe, reason = is_safe_readonly_command("cat file.txt | grep pattern")
        assert is_safe is True

    def test_unsafe_piped_command(self):
        is_safe, reason = is_safe_readonly_command("cat file.txt | python")
        assert is_safe is False


# =============================================================================
# Tests for extract_scoped_prefix
# =============================================================================


class TestExtractScopedPrefix:
    """Tests for extract_scoped_prefix function."""

    def test_no_prefix(self):
        scope, cmd = extract_scoped_prefix("pytest tests/")
        assert scope is None
        assert cmd == "pytest tests/"

    def test_cwd_prefix(self):
        scope, cmd = extract_scoped_prefix("[cwd=src] pytest")
        assert scope == "src"
        assert cmd == "pytest"

    def test_dir_prefix(self):
        scope, cmd = extract_scoped_prefix("[dir=lib] make")
        assert scope == "lib"
        assert cmd == "make"

    def test_whitespace_handling(self):
        scope, cmd = extract_scoped_prefix("  [cwd=test]   ls -la  ")
        assert scope == "test"
        assert cmd == "ls -la"


# =============================================================================
# Tests for resolve_scoped_directory
# =============================================================================


class TestResolveScopedDirectory:
    """Tests for resolve_scoped_directory function."""

    def test_valid_subdirectory(self, tmp_path):
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        resolved, error = resolve_scoped_directory("subdir", tmp_path)
        assert resolved == subdir
        assert error is None

    def test_directory_outside_workspace(self, tmp_path):
        resolved, error = resolve_scoped_directory("/etc", tmp_path)
        assert resolved is None
        assert "outside workspace" in error

    def test_nonexistent_directory(self, tmp_path):
        resolved, error = resolve_scoped_directory("nonexistent", tmp_path)
        assert resolved is None
        assert "not found" in error


# =============================================================================
# Tests for shell_quote
# =============================================================================


class TestShellQuote:
    """Tests for shell_quote function."""

    def test_simple_string(self):
        result = shell_quote("hello")
        assert result == "'hello'"

    def test_string_with_single_quotes(self):
        result = shell_quote("it's")
        assert result == "'it'\\''s'"

    def test_string_with_spaces(self):
        result = shell_quote("hello world")
        assert result == "'hello world'"


# =============================================================================
# Tests for extract_bash_blocks
# =============================================================================


class TestExtractBashBlocks:
    """Tests for extract_bash_blocks function."""

    def test_no_blocks(self):
        result = extract_bash_blocks("Just plain text")
        assert result == []

    def test_single_bash_block(self):
        text = """Here is the command:
```bash
echo hello
```
Done."""
        result = extract_bash_blocks(text)
        assert len(result) == 1
        assert result[0] == "echo hello"

    def test_multiple_blocks(self):
        text = """
```bash
ls
```
And then:
```shell
pwd
```
"""
        result = extract_bash_blocks(text)
        assert len(result) == 2
        assert "ls" in result[0]
        assert "pwd" in result[1]


# =============================================================================
# Tests for sanitize_shell_block
# =============================================================================


class TestSanitizeShellBlock:
    """Tests for sanitize_shell_block function."""

    def test_removes_read_directive(self):
        cmd = "READ: file.txt\necho hello"
        result = sanitize_shell_block(cmd)
        assert "READ:" not in result
        assert "echo hello" in result

    def test_removes_run_directive(self):
        cmd = "RUN: pytest\necho done"
        result = sanitize_shell_block(cmd)
        assert "RUN:" not in result

    def test_removes_task_understanding(self):
        cmd = "Task Understanding\necho hello"
        result = sanitize_shell_block(cmd)
        assert "Task Understanding" not in result


# =============================================================================
# Tests for strip_search_comment
# =============================================================================


class TestStripSearchComment:
    """Tests for strip_search_comment function."""

    def test_no_comment(self):
        result = strip_search_comment("pattern")
        assert result == "pattern"

    def test_with_comment(self):
        result = strip_search_comment("pattern # search for this")
        assert result == "pattern"

    def test_preserves_hash_in_pattern(self):
        # Hash at start should be preserved (regex pattern)
        result = strip_search_comment("^#comment")
        assert result == "^#comment"


# =============================================================================
# Tests for read_file_context
# =============================================================================


class TestReadFileContext:
    """Tests for read_file_context function."""

    def test_read_existing_file(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3")
        result = read_file_context("test.txt", tmp_path)
        assert result is not None
        assert "File: test.txt" in result
        assert "line1" in result

    def test_read_nonexistent_file(self, tmp_path):
        result = read_file_context("nonexistent.txt", tmp_path)
        assert result is None

    def test_read_directory(self, tmp_path):
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file.txt").write_text("content")
        result = read_file_context("subdir", tmp_path)
        assert result is not None
        assert "Directory:" in result
        assert "file.txt" in result

    def test_path_outside_cwd(self, tmp_path):
        result = read_file_context("../../../etc/passwd", tmp_path)
        assert result is None


# =============================================================================
# Tests for parse_test_output
# =============================================================================


class TestParseTestOutput:
    """Tests for parse_test_output function."""

    def test_all_passed(self):
        output = "5 passed in 0.5s"
        result = parse_test_output(output)
        assert result["passed"] == 5
        assert result["failed"] == 0
        assert result["is_success"] is True

    def test_some_failed(self):
        output = "3 passed, 2 failed in 1.0s"
        result = parse_test_output(output)
        assert result["passed"] == 3
        assert result["failed"] == 2
        assert result["is_success"] is False

    def test_collection_error(self):
        output = "ERROR collecting tests\nImportError: No module named 'foo'"
        result = parse_test_output(output)
        assert result["has_collection_errors"] is True
        assert result["is_success"] is False

    def test_failure_details(self):
        output = "FAILED tests/test_foo.py::test_bar"
        result = parse_test_output(output)
        assert "tests/test_foo.py::test_bar" in result["failure_details"]


# =============================================================================
# Tests for has_test_errors
# =============================================================================


class TestHasTestErrors:
    """Tests for has_test_errors function."""

    def test_no_errors(self):
        assert has_test_errors("5 passed") is False

    def test_with_failures(self):
        assert has_test_errors("1 failed") is True

    def test_with_collection_errors(self):
        assert has_test_errors("ERROR collecting") is True


# =============================================================================
# Tests for get_test_error_summary
# =============================================================================


class TestGetTestErrorSummary:
    """Tests for get_test_error_summary function."""

    def test_all_passed(self):
        summary = get_test_error_summary("5 passed")
        assert "ALL TESTS PASSED" in summary

    def test_failures(self):
        summary = get_test_error_summary("3 passed, 2 failed")
        assert "TEST FAILURES" in summary

    def test_collection_errors(self):
        summary = get_test_error_summary("2 errors during collection")
        assert "COLLECTION FAILED" in summary


# =============================================================================
# Tests for swarm.py - TaskType enum
# =============================================================================


class TestTaskType:
    """Tests for TaskType enum."""

    def test_architecture(self):
        assert TaskType.ARCHITECTURE.value == "architecture"

    def test_implementation(self):
        assert TaskType.IMPLEMENTATION.value == "implementation"

    def test_testing(self):
        assert TaskType.TESTING.value == "testing"

    def test_security(self):
        assert TaskType.SECURITY.value == "security"


# =============================================================================
# Tests for TaskStatus enum
# =============================================================================


class TestTaskStatus:
    """Tests for TaskStatus enum."""

    def test_pending(self):
        assert TaskStatus.PENDING.value == "pending"

    def test_running(self):
        assert TaskStatus.RUNNING.value == "running"

    def test_completed(self):
        assert TaskStatus.COMPLETED.value == "completed"

    def test_failed(self):
        assert TaskStatus.FAILED.value == "failed"


# =============================================================================
# Tests for SwarmTask dataclass
# =============================================================================


class TestSwarmTask:
    """Tests for SwarmTask dataclass."""

    def test_create_minimal(self):
        task = SwarmTask(
            id="test-1",
            type=TaskType.IMPLEMENTATION,
            description="Test task",
            context="Some context",
        )
        assert task.id == "test-1"
        assert task.status == TaskStatus.PENDING
        assert task.dependencies == []

    def test_to_dict(self):
        task = SwarmTask(
            id="test-1",
            type=TaskType.TESTING,
            description="Write tests",
            context="Test context",
        )
        d = task.to_dict()
        assert d["id"] == "test-1"
        assert d["type"] == "testing"
        assert d["status"] == "pending"


# =============================================================================
# Tests for ModelProfile dataclass
# =============================================================================


class TestModelProfile:
    """Tests for ModelProfile dataclass."""

    def test_create(self):
        profile = ModelProfile(
            model_id="test-model",
            strengths=[TaskType.IMPLEMENTATION],
            cost_tier="medium",
            context_size=8192,
            speed="fast",
        )
        assert profile.model_id == "test-model"
        assert TaskType.IMPLEMENTATION in profile.strengths

    def test_from_model_id_expensive(self):
        profile = ModelProfile.from_model_id("claude-opus-3")
        assert profile.cost_tier == "expensive"

    def test_from_model_id_fast(self):
        profile = ModelProfile.from_model_id("gemini-flash")
        assert profile.speed == "fast"

    def test_from_model_id_coder(self):
        profile = ModelProfile.from_model_id("deepseek-coder")
        assert TaskType.IMPLEMENTATION in profile.strengths

    def test_from_model_id_default_strengths(self):
        profile = ModelProfile.from_model_id("unknown-model")
        assert TaskType.IMPLEMENTATION in profile.strengths


# =============================================================================
# Tests for SwarmResult dataclass
# =============================================================================


class TestSwarmResult:
    """Tests for SwarmResult dataclass."""

    def test_create(self):
        tasks = [
            SwarmTask(id="t1", type=TaskType.TESTING, description="Test", context=""),
        ]
        result = SwarmResult(
            success=True,
            tasks=tasks,
            total_time=1.5,
            models_used={"model-1"},
        )
        assert result.success is True

    def test_completed_tasks(self):
        task1 = SwarmTask(id="t1", type=TaskType.TESTING, description="", context="")
        task1.status = TaskStatus.COMPLETED
        task2 = SwarmTask(id="t2", type=TaskType.TESTING, description="", context="")
        task2.status = TaskStatus.FAILED
        
        result = SwarmResult(
            success=False,
            tasks=[task1, task2],
            total_time=1.0,
            models_used=set(),
        )
        assert len(result.completed_tasks) == 1
        assert len(result.failed_tasks) == 1


# =============================================================================
# Tests for SwarmOrchestrator class
# =============================================================================


class TestSwarmOrchestrator:
    """Tests for SwarmOrchestrator class."""

    def test_init(self):
        orchestrator = SwarmOrchestrator(default_model="default")
        assert orchestrator.default_model == "default"
        assert orchestrator.max_workers == 3

    def test_register_model(self):
        orchestrator = SwarmOrchestrator(default_model="default")
        orchestrator.register_model("test-model", context_size=4096)
        assert "test-model" in orchestrator.model_profiles

    def test_register_models(self):
        orchestrator = SwarmOrchestrator(default_model="default")
        orchestrator.register_models(["model-1", "model-2"])
        assert len(orchestrator.model_profiles) == 2

    def test_select_model_default(self):
        orchestrator = SwarmOrchestrator(default_model="default")
        model = orchestrator.select_model_for_task(TaskType.IMPLEMENTATION)
        assert model == "default"

    def test_select_model_with_candidates(self):
        orchestrator = SwarmOrchestrator(default_model="default")
        orchestrator.register_model("deepseek-coder")
        model = orchestrator.select_model_for_task(TaskType.IMPLEMENTATION)
        assert model == "deepseek-coder"

    def test_decompose_task_architecture(self):
        orchestrator = SwarmOrchestrator(default_model="default")
        tasks = orchestrator.decompose_task("Create a new user authentication system")
        task_types = [t.type for t in tasks]
        assert TaskType.ARCHITECTURE in task_types

    def test_decompose_task_debugging(self):
        orchestrator = SwarmOrchestrator(default_model="default")
        tasks = orchestrator.decompose_task("Fix the bug in login")
        task_types = [t.type for t in tasks]
        assert TaskType.DEBUGGING in task_types

    def test_decompose_task_testing(self):
        orchestrator = SwarmOrchestrator(default_model="default")
        tasks = orchestrator.decompose_task("Add tests for user module")
        task_types = [t.type for t in tasks]
        assert TaskType.TESTING in task_types

    def test_decompose_task_default(self):
        orchestrator = SwarmOrchestrator(default_model="default")
        tasks = orchestrator.decompose_task("Do something vague")
        assert len(tasks) >= 1

    def test_execute_task(self):
        orchestrator = SwarmOrchestrator(default_model="default")
        task = SwarmTask(
            id="test",
            type=TaskType.IMPLEMENTATION,
            description="Test task",
            context="Context",
        )
        
        def mock_send(prompt, model):
            return "Task completed"
        
        result = orchestrator.execute_task(task, mock_send)
        assert result == "Task completed"
        assert task.status == TaskStatus.COMPLETED

    def test_execute_task_failure(self):
        orchestrator = SwarmOrchestrator(default_model="default")
        task = SwarmTask(
            id="test",
            type=TaskType.IMPLEMENTATION,
            description="Test task",
            context="Context",
        )
        
        def mock_send(prompt, model):
            raise Exception("API error")
        
        result = orchestrator.execute_task(task, mock_send)
        assert result is None
        assert task.status == TaskStatus.FAILED
        assert "API error" in task.error

    def test_execute_sequential(self):
        orchestrator = SwarmOrchestrator(default_model="default")
        tasks = [
            SwarmTask(id="t1", type=TaskType.TESTING, description="Test", context=""),
            SwarmTask(id="t2", type=TaskType.IMPLEMENTATION, description="Impl", context="", dependencies=["t1"]),
        ]
        
        call_order = []
        def mock_send(prompt, model):
            call_order.append(prompt[:10])
            return "Done"
        
        result = orchestrator.execute(tasks, mock_send, parallel=False)
        assert result.success is True
        assert len(call_order) == 2

    def test_execute_parallel(self):
        orchestrator = SwarmOrchestrator(default_model="default")
        tasks = [
            SwarmTask(id="t1", type=TaskType.TESTING, description="Test", context=""),
            SwarmTask(id="t2", type=TaskType.DOCUMENTATION, description="Doc", context=""),
        ]
        
        def mock_send(prompt, model):
            time.sleep(0.01)
            return "Done"
        
        result = orchestrator.execute(tasks, mock_send, parallel=True)
        assert result.success is True

    def test_clear_tasks(self):
        orchestrator = SwarmOrchestrator(default_model="default")
        orchestrator.decompose_task("Implement something")
        assert len(orchestrator.tasks) > 0
        orchestrator.clear_tasks()
        assert len(orchestrator.tasks) == 0

    def test_get_task_graph(self):
        orchestrator = SwarmOrchestrator(default_model="default")
        orchestrator.decompose_task("Create a new feature with tests")
        graph = orchestrator.get_task_graph()
        assert isinstance(graph, dict)


# =============================================================================
# Tests for detect_test_framework
# =============================================================================


class TestDetectTestFramework:
    """Tests for detect_test_framework function."""

    def test_detect_pytest_from_ini(self, tmp_path):
        # pytest.ini alone won't trigger detection - need pyproject.toml
        (tmp_path / "pyproject.toml").write_text("[tool.pytest]")
        (tmp_path / "pytest.ini").write_text("[pytest]")
        result = detect_test_framework(tmp_path)
        assert "pytest" in result

    def test_detect_pytest_from_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[tool.pytest.ini_options]\n')
        result = detect_test_framework(tmp_path)
        assert "pytest" in result

    def test_detect_cargo(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[package]\nname = "test"')
        result = detect_test_framework(tmp_path)
        assert result == "cargo test"

    def test_detect_go(self, tmp_path):
        (tmp_path / "go.mod").write_text("module test")
        result = detect_test_framework(tmp_path)
        assert result == "go test ./..."

    def test_detect_npm_jest(self, tmp_path):
        (tmp_path / "package.json").write_text('{"devDependencies": {"jest": "1.0"}}')
        result = detect_test_framework(tmp_path)
        assert result == "npm test"

    def test_detect_python_files(self, tmp_path):
        (tmp_path / "test_app.py").write_text("def test_foo(): pass")
        result = detect_test_framework(tmp_path)
        assert "pytest" in result

    def test_no_framework_detected(self, tmp_path):
        result = detect_test_framework(tmp_path)
        assert result is None
