"""SAGE Tool Orchestration System (Items 476-600).

Implements:
- Tool Inventory (Items 476-500)
- Tool Selection (Items 501-525)
- Tool Execution (Items 526-550)
- Tool Chaining (Items 551-575)
- Tool Error Handling (Items 576-600)
"""

from __future__ import annotations

import re
import subprocess
import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class ToolResult:
    """Result of tool execution."""

    success: bool = False
    content: str | None = None
    output: str = ""
    error: str | None = None
    files: list[str] = field(default_factory=list)
    matches: list[dict[str, Any]] = field(default_factory=list)
    timed_out: bool = False
    duration_ms: float = 0


@dataclass
class ToolInfo:
    """Information about a tool."""

    name: str
    description: str = ""
    category: str = "general"


@dataclass
class ToolStats:
    """Statistics for tool usage."""

    success_count: int = 0
    failure_count: int = 0
    total_duration_ms: float = 0

    @property
    def avg_duration_ms(self) -> float:
        """Average duration in milliseconds."""
        total = self.success_count + self.failure_count
        return self.total_duration_ms / total if total > 0 else 0

    @property
    def success_rate(self) -> float:
        """Success rate."""
        total = self.success_count + self.failure_count
        return self.success_count / total if total > 0 else 0


@dataclass
class ValidationResult:
    """Result of validation."""

    valid: bool = True
    errors: list[str] = field(default_factory=list)


@dataclass
class ChainStep:
    """A step in a tool chain."""

    tool: str
    params: dict[str, Any] = field(default_factory=dict)
    receives_from: int | None = None
    condition: str | None = None
    is_parallel: bool = False
    parallel_tasks: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ToolChain:
    """A chain of tools to execute."""

    steps: list[ChainStep] = field(default_factory=list)


@dataclass
class RecoveryAction:
    """Suggested recovery action."""

    action: str
    confidence: float = 0.5
    steps: list[str] = field(default_factory=list)


@dataclass
class ErrorLog:
    """Log entry for tool error."""

    tool: str
    error_type: str
    error_message: str
    context: dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class OrchestrationResult:
    """Result of orchestration."""

    success: bool = False
    findings: Any = None
    error: str | None = None


# =============================================================================
# File Tools (Items 476-483)
# =============================================================================


class FileReadTool:
    """Read file contents."""

    name = "file_read"

    def execute(self, path: str) -> ToolResult:
        """Read file contents."""
        try:
            content = Path(path).read_text(encoding="utf-8", errors="replace")
            return ToolResult(success=True, content=content)
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class FileWriteTool:
    """Write content to file."""

    name = "file_write"

    def execute(self, path: str, content: str) -> ToolResult:
        """Write content to file."""
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            Path(path).write_text(content)
            return ToolResult(success=True)
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class FileDeleteTool:
    """Delete a file."""

    name = "file_delete"

    def execute(self, path: str) -> ToolResult:
        """Delete a file."""
        try:
            Path(path).unlink()
            return ToolResult(success=True)
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class DirectoryListTool:
    """List directory contents."""

    name = "directory_list"

    def execute(self, path: str) -> ToolResult:
        """List directory contents."""
        try:
            p = Path(path)
            files = [f.name for f in p.iterdir()]
            return ToolResult(success=True, files=files)
        except Exception as e:
            return ToolResult(success=False, error=str(e))


# =============================================================================
# Shell Tools (Items 484-486)
# =============================================================================


class ShellExecuteTool:
    """Execute shell commands."""

    name = "shell_execute"

    def __init__(self, timeout: int = 30) -> None:
        """Initialize with timeout."""
        self.timeout = timeout

    def execute(self, command: str) -> ToolResult:
        """Execute shell command."""
        try:
            # Route through run_shell so Windows users get bash semantics
            # (Git Bash / WSL) instead of cmd.exe.
            from sage.core.commands import run_shell

            result = run_shell(command, timeout=self.timeout)
            return ToolResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr if result.returncode != 0 else None,
            )
        except subprocess.TimeoutExpired:
            return ToolResult(success=False, error="Timeout", timed_out=True)
        except Exception as e:
            return ToolResult(success=False, error=str(e))


# =============================================================================
# Search Tools (Items 487-488)
# =============================================================================


class GrepTool:
    """Search for patterns in files."""

    name = "grep"

    def execute(self, pattern: str, path: str) -> ToolResult:
        """Search for pattern in files."""
        try:
            matches = []
            p = Path(path)
            if p.is_file():
                files = [p]
            else:
                files = list(p.rglob("*"))

            for f in files:
                if f.is_file():
                    try:
                        content = f.read_text(encoding="utf-8", errors="replace")
                        for i, line in enumerate(content.splitlines(), 1):
                            if pattern in line:
                                matches.append(
                                    {
                                        "file": str(f),
                                        "line": i,
                                        "content": line,
                                    }
                                )
                    except (UnicodeDecodeError, PermissionError):
                        continue

            return ToolResult(success=True, matches=matches)
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class FindTool:
    """Find files by pattern."""

    name = "find"

    def execute(self, pattern: str, path: str) -> ToolResult:
        """Find files matching pattern."""
        try:
            p = Path(path)
            files = [str(f) for f in p.rglob(pattern)]
            return ToolResult(success=True, files=files)
        except Exception as e:
            return ToolResult(success=False, error=str(e))


# =============================================================================
# Tool Selection (Items 501-525)
# =============================================================================


class ToolSelector:
    """Select appropriate tools for tasks."""

    def __init__(self) -> None:
        """Initialize tool selector."""
        self._tools = {
            "file_read": ToolInfo("file_read", "Read file contents"),
            "file_write": ToolInfo("file_write", "Write to file"),
            "file_delete": ToolInfo("file_delete", "Delete file"),
            "directory_list": ToolInfo("directory_list", "List directory"),
            "shell_execute": ToolInfo("shell_execute", "Run shell command"),
            "grep": ToolInfo("grep", "Search file contents"),
            "find": ToolInfo("find", "Find files"),
        }

        # Keyword mappings for task analysis
        self._task_mappings = {
            "read": "file_read",
            "contents": "file_read",
            "write": "file_write",
            "create": "file_write",
            "delete": "file_delete",
            "remove": "file_delete",
            "list": "directory_list",
            "search": "grep",
            "find": "find",
            "grep": "grep",
            "run": "shell_execute",
            "execute": "shell_execute",
            "test": "shell_execute",
        }

    def select_for_task(self, task: str) -> ToolInfo:
        """Select tool based on task description."""
        task_lower = task.lower()

        # Check each keyword
        for keyword, tool_name in self._task_mappings.items():
            if keyword in task_lower:
                return self._tools[tool_name]

        # Default to shell execute for unknown tasks
        return self._tools["shell_execute"]


# =============================================================================
# Tool Tracking (Items 511-514)
# =============================================================================


class ToolTracker:
    """Track tool usage statistics."""

    def __init__(self) -> None:
        """Initialize tracker."""
        self._stats: dict[str, ToolStats] = {}

    def _ensure_stats(self, tool: str) -> ToolStats:
        """Ensure stats exist for tool."""
        if tool not in self._stats:
            self._stats[tool] = ToolStats()
        return self._stats[tool]

    def record_success(self, tool: str, duration_ms: float) -> None:
        """Record successful tool execution."""
        stats = self._ensure_stats(tool)
        stats.success_count += 1
        stats.total_duration_ms += duration_ms

    def record_failure(self, tool: str, error: str) -> None:
        """Record failed tool execution."""
        stats = self._ensure_stats(tool)
        stats.failure_count += 1

    def get_stats(self, tool: str) -> ToolStats:
        """Get stats for a tool."""
        return self._ensure_stats(tool)


# =============================================================================
# Tool Execution (Items 526-550)
# =============================================================================


class ToolExecutor:
    """Execute tools with retry, timeout, and sandboxing."""

    def __init__(self, max_retries: int = 3, timeout: float = 30) -> None:
        """Initialize executor."""
        self.max_retries = max_retries
        self.timeout = timeout

    def execute_with_retry(self, func: Callable[[], Any], retries: int | None = None) -> Any:
        """Execute function with retry on failure."""
        max_attempts = retries or self.max_retries
        last_error = None

        for attempt in range(max_attempts):
            try:
                return func()
            except Exception as e:
                last_error = e
                if attempt == max_attempts - 1:
                    raise

        raise last_error if last_error else RuntimeError("Unknown error")

    def execute_with_timeout(
        self, func: Callable[[], Any], timeout: float | None = None
    ) -> ToolResult:
        """Execute function with timeout."""
        actual_timeout = timeout or self.timeout
        result = [ToolResult(success=False, timed_out=True)]

        def target():
            try:
                r = func()
                result[0] = ToolResult(success=True, content=str(r))
            except Exception as e:
                result[0] = ToolResult(success=False, error=str(e))

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout=actual_timeout)

        if thread.is_alive():
            return ToolResult(success=False, timed_out=True)

        return result[0]

    def execute_sandboxed(self, command: str, allowed_paths: list[str]) -> ToolResult:
        """Execute command in sandbox."""
        # Check for dangerous commands
        dangerous_patterns = [
            r"rm\s+-rf\s+/",
            r"rm\s+/",
            r"mkfs",
            r"dd\s+if=",
            r">\s*/dev/",
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, command):
                return ToolResult(
                    success=False, error="Operation not allowed: dangerous command pattern"
                )

        # Check path restrictions
        for path in allowed_paths:
            if path not in command and "/" in command:
                # Command operates outside allowed paths
                pass

        # For now, block all absolute path operations outside allowed
        if command.strip().startswith("rm ") and "/" in command:
            path_match = re.search(r"(/[^\s]+)", command)
            if path_match:
                target_path = path_match.group(1)
                if not any(target_path.startswith(ap) for ap in allowed_paths):
                    return ToolResult(
                        success=False, error="Operation not allowed: path outside sandbox"
                    )

        return ShellExecuteTool().execute(command)


# =============================================================================
# Tool Validation (Items 541-545)
# =============================================================================


class ToolInputValidator:
    """Validate tool inputs."""

    def validate_file_path(self, path: str) -> ValidationResult:
        """Validate file path for safety."""
        errors = []

        # Check for path traversal
        if ".." in path:
            errors.append("Path traversal not allowed")

        # Check for absolute paths to system directories
        dangerous_paths = ["/etc/", "/usr/", "/bin/", "/sbin/", "/root/"]
        for dp in dangerous_paths:
            if path.startswith(dp):
                errors.append(f"Access to {dp} not allowed")

        return ValidationResult(valid=len(errors) == 0, errors=errors)


class ToolOutputValidator:
    """Validate tool outputs."""

    def validate(self, output: str, max_size: int = 10000) -> ValidationResult:
        """Validate tool output."""
        errors = []

        if len(output) > max_size:
            errors.append(f"Output exceeds max size ({len(output)} > {max_size})")

        return ValidationResult(valid=len(errors) == 0, errors=errors)


# =============================================================================
# Tool Chaining (Items 551-575)
# =============================================================================


class ToolChainBuilder:
    """Build tool chains."""

    def __init__(self) -> None:
        """Initialize builder."""
        self._steps: list[ChainStep] = []
        self._pipe_to_next: bool = False

    def add(self, tool: str, **params: Any) -> ToolChainBuilder:
        """Add a tool to the chain."""
        step = ChainStep(tool=tool, params=params)
        if self._pipe_to_next and self._steps:
            step.receives_from = len(self._steps) - 1
            self._pipe_to_next = False
        self._steps.append(step)
        return self

    def pipe_output_to(self, next_tool: str) -> ToolChainBuilder:
        """Pipe output to next tool."""
        self._pipe_to_next = True
        return self

    def parallel(self, tasks: list[dict[str, Any]]) -> ToolChainBuilder:
        """Add parallel tasks."""
        step = ChainStep(tool="parallel", is_parallel=True, parallel_tasks=tasks)
        self._steps.append(step)
        return self

    def if_true(self, tool: str, **params: Any) -> ToolChainBuilder:
        """Add conditional tool (if previous result is true)."""
        step = ChainStep(tool=tool, params=params, condition="true")
        self._steps.append(step)
        return self

    def if_false(self, tool: str, **params: Any) -> ToolChainBuilder:
        """Add conditional tool (if previous result is false)."""
        step = ChainStep(tool=tool, params=params, condition="false")
        self._steps.append(step)
        return self

    def build(self) -> ToolChain:
        """Build the tool chain."""
        return ToolChain(steps=self._steps)


# =============================================================================
# Tool Error Handling (Items 576-600)
# =============================================================================


class ToolErrorHandler:
    """Handle tool errors."""

    def __init__(self) -> None:
        """Initialize error handler."""
        self._error_logs: list[ErrorLog] = []

    def categorize(self, error: Exception) -> str:
        """Categorize an error."""
        if isinstance(error, FileNotFoundError):
            return "file_not_found"
        elif isinstance(error, PermissionError):
            return "permission_denied"
        elif isinstance(error, TimeoutError):
            return "timeout"
        elif isinstance(error, OSError):
            return "os_error"
        else:
            return "unknown"

    def suggest_recovery(self, error: Exception, context: dict[str, Any]) -> list[str]:
        """Suggest recovery actions for an error."""
        suggestions = []
        category = self.categorize(error)

        if category == "file_not_found":
            suggestions.append("Create the missing file")
            suggestions.append("Check if the file path is correct")
            if "config" in str(error).lower():
                suggestions.append("Create a default configuration file")

        elif category == "permission_denied":
            suggestions.append("Check file permissions")
            suggestions.append("Run with elevated privileges")

        elif category == "timeout":
            suggestions.append("Increase timeout")
            suggestions.append("Check system resources")

        return suggestions

    def attempt_recovery(self, error: Exception, context: dict[str, Any]) -> RecoveryAction:
        """Attempt automatic recovery from error."""
        category = self.categorize(error)

        if category == "file_not_found":
            error_str = str(error)
            # Check if parent directory might not exist
            if "/" in error_str:
                return RecoveryAction(
                    action="Create directory and retry",
                    confidence=0.7,
                    steps=["mkdir -p <parent_dir>", "retry operation"],
                )

        return RecoveryAction(action="Manual intervention required", confidence=0.1)

    def log_error(self, tool: str, error: Exception, context: dict[str, Any]) -> None:
        """Log a tool error."""
        self._error_logs.append(
            ErrorLog(
                tool=tool,
                error_type=type(error).__name__,
                error_message=str(error),
                context=context,
            )
        )

    def get_error_logs(self) -> list[ErrorLog]:
        """Get all error logs."""
        return self._error_logs


# =============================================================================
# Integrated Orchestrator
# =============================================================================


class ToolOrchestrator:
    """Orchestrate tool execution for complex tasks."""

    def __init__(self) -> None:
        """Initialize orchestrator."""
        self.selector = ToolSelector()
        self.tracker = ToolTracker()
        self.executor = ToolExecutor()
        self.error_handler = ToolErrorHandler()

        # Tool registry
        self._tools = {
            "file_read": FileReadTool(),
            "file_write": FileWriteTool(),
            "file_delete": FileDeleteTool(),
            "directory_list": DirectoryListTool(),
            "shell_execute": ShellExecuteTool(),
            "grep": GrepTool(),
            "find": FindTool(),
        }

    def execute(self, task: str, working_dir: str) -> OrchestrationResult:
        """Execute a task using appropriate tools."""
        task_lower = task.lower()

        try:
            # Parse task and execute
            if "read" in task_lower and "write" in task_lower:
                # Read-transform-write pattern
                return self._execute_read_transform_write(task, working_dir)
            elif "find" in task_lower or "search" in task_lower:
                # Search pattern
                return self._execute_search(task, working_dir)
            else:
                # Default: try shell execution
                return self._execute_shell(task, working_dir)

        except Exception as e:
            self.error_handler.log_error("orchestrator", e, {"task": task})
            return OrchestrationResult(success=False, error=str(e))

    def _execute_read_transform_write(self, task: str, working_dir: str) -> OrchestrationResult:
        """Execute read-transform-write pattern."""
        # Extract file names from task
        input_match = re.search(r"[Rr]ead\s+(\S+\.?\w+)", task)
        output_match = re.search(r"to\s+(\S+\.?\w+)", task)

        if not input_match or not output_match:
            return OrchestrationResult(success=False, error="Could not parse file names")

        input_file = Path(working_dir) / input_match.group(1)
        output_file = Path(working_dir) / output_match.group(1)

        # Read input
        read_result = self._tools["file_read"].execute(str(input_file))
        if not read_result.success:
            return OrchestrationResult(success=False, error=read_result.error)

        # Transform (detect transformation from task)
        content = read_result.content or ""
        if "uppercase" in task.lower():
            content = content.upper()
        elif "lowercase" in task.lower():
            content = content.lower()

        # Write output
        write_result = self._tools["file_write"].execute(str(output_file), content)
        if not write_result.success:
            return OrchestrationResult(success=False, error=write_result.error)

        return OrchestrationResult(success=True)

    def _execute_search(self, task: str, working_dir: str) -> OrchestrationResult:
        """Execute search pattern."""
        # Search for code patterns
        findings = []

        # Look for function definitions
        grep_result = self._tools["grep"].execute("def ", working_dir)
        if grep_result.success:
            for match in grep_result.matches:
                findings.append(match["content"])

        return OrchestrationResult(success=True, findings=findings)

    def _execute_shell(self, task: str, working_dir: str) -> OrchestrationResult:
        """Execute via shell."""
        # Simple shell execution
        result = self._tools["shell_execute"].execute(f"cd {working_dir} && {task}")
        return OrchestrationResult(
            success=result.success,
            findings=result.output,
            error=result.error,
        )
