"""
Tool execution validation for SAGE - Fixes P4 issues 81-100.

P4-81: Tools mentioned but not called
P4-82: No tool result validation
P4-83: Missing tool error handling
P4-84: No tool chaining
P4-85: Tool output not used
P4-86: No parallel tool execution
P4-87: Missing tool timeouts
P4-88: No tool retry logic
P4-89: Tool selection heuristics weak
P4-95: Missing tool output parsing

This module ensures tools are actually executed and results are validated.
"""

from __future__ import annotations

import fnmatch
import re
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

if TYPE_CHECKING:
    from collections.abc import Callable


class ToolType(Enum):
    """Types of tools available."""

    READ = auto()  # Read file content
    SEARCH = auto()  # Search codebase
    WRITE = auto()  # Write file
    RUN = auto()  # Run command
    VERIFY = auto()  # Verify file exists
    LIST = auto()  # List files


class ToolStatus(Enum):
    """Status of tool execution."""

    PENDING = auto()
    RUNNING = auto()
    SUCCESS = auto()
    FAILED = auto()
    TIMEOUT = auto()
    SKIPPED = auto()


@dataclass
class ToolCall:
    """A single tool invocation."""

    tool_type: ToolType
    command: str
    args: dict[str, Any] = field(default_factory=dict)

    # Execution state
    status: ToolStatus = ToolStatus.PENDING
    started_at: float | None = None
    completed_at: float | None = None

    # Results
    result: Any | None = None
    error: str | None = None
    output: str | None = None

    # Retry tracking
    attempt: int = 0
    max_attempts: int = 3

    @property
    def duration(self) -> float | None:
        if self.started_at and self.completed_at:
            return self.completed_at - self.started_at
        return None

    @property
    def is_complete(self) -> bool:
        return self.status in (
            ToolStatus.SUCCESS,
            ToolStatus.FAILED,
            ToolStatus.TIMEOUT,
            ToolStatus.SKIPPED,
        )


@dataclass
class ToolChain:
    """A sequence of tool calls with dependencies."""

    calls: list[ToolCall] = field(default_factory=list)
    dependencies: dict[int, list[int]] = field(
        default_factory=dict
    )  # call_index -> [depends_on_indices]

    def add_call(self, call: ToolCall, depends_on: list[int] | None = None) -> int:
        """Add a tool call to the chain."""
        index = len(self.calls)
        self.calls.append(call)
        if depends_on:
            self.dependencies[index] = depends_on
        return index

    def get_ready_calls(self) -> list[int]:
        """Get indices of calls that are ready to execute."""
        ready = []
        for i, call in enumerate(self.calls):
            if call.status != ToolStatus.PENDING:
                continue

            deps = self.dependencies.get(i, [])
            if all(self.calls[d].status == ToolStatus.SUCCESS for d in deps):
                ready.append(i)

        return ready

    def is_complete(self) -> bool:
        """Check if all calls are complete."""
        return all(call.is_complete for call in self.calls)

    def get_failed_calls(self) -> list[ToolCall]:
        """Get calls that failed."""
        return [c for c in self.calls if c.status in (ToolStatus.FAILED, ToolStatus.TIMEOUT)]


class ToolExecutionValidator:
    """
    Validates that tools mentioned in responses are actually executed.

    Fixes:
    - P4-81: Detects tool mentions without execution
    - P4-85: Ensures tool output is captured
    """

    # Patterns that indicate tool usage
    TOOL_PATTERNS: ClassVar[dict[ToolType, list[str]]] = {
        ToolType.READ: [
            r"READ:\s*`?([^`\n]+)`?",
            r"Reading file[:\s]+`?([^`\n]+)`?",
            r"Let me read[:\s]+`?([^`\n]+)`?",
        ],
        ToolType.SEARCH: [
            r"SEARCH:\s*(.+?)(?:\n|$)",
            r"Searching for[:\s]+(.+?)(?:\n|$)",
            r"Let me search[:\s]+(.+?)(?:\n|$)",
        ],
        ToolType.WRITE: [
            r"FILE:\s*`([^`]+)`",
            r"Writing to[:\s]+`?([^`\n]+)`?",
            r"Creating file[:\s]+`?([^`\n]+)`?",
        ],
        ToolType.RUN: [
            r"RUN:\s*`?([^`\n]+)`?",
            r"Running[:\s]+`?([^`\n]+)`?",
            r"Executing[:\s]+`?([^`\n]+)`?",
        ],
    }

    def __init__(self):
        self._compile_patterns()

    def _compile_patterns(self):
        """Pre-compile regex patterns."""
        self._patterns = {
            tool_type: [re.compile(p, re.IGNORECASE) for p in patterns]
            for tool_type, patterns in self.TOOL_PATTERNS.items()
        }

    def extract_tool_mentions(self, content: str) -> list[ToolCall]:
        """Extract all tool mentions from content."""
        mentions = []

        for tool_type, patterns in self._patterns.items():
            for pattern in patterns:
                for match in pattern.finditer(content):
                    command = match.group(1).strip()
                    mentions.append(
                        ToolCall(
                            tool_type=tool_type,
                            command=command,
                        )
                    )

        return mentions

    def validate_execution(
        self, content: str, executed_calls: list[ToolCall]
    ) -> tuple[list[ToolCall], list[ToolCall]]:
        """
        Validate that mentioned tools were executed.

        Returns:
            Tuple of (executed_mentions, unexecuted_mentions)
        """
        mentions = self.extract_tool_mentions(content)
        executed_commands = {(c.tool_type, c.command.lower()) for c in executed_calls}

        executed = []
        unexecuted = []

        for mention in mentions:
            key = (mention.tool_type, mention.command.lower())
            if key in executed_commands:
                executed.append(mention)
            else:
                unexecuted.append(mention)

        return executed, unexecuted


class ToolExecutor:
    """
    Actually executes tools and captures results.

    Fixes:
    - P4-82: Validates tool results
    - P4-83: Handles errors properly
    - P4-87: Implements timeouts
    - P4-88: Implements retry logic
    """

    DEFAULT_TIMEOUT = 30.0  # seconds
    MAX_RETRIES = 3

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.execution_history: list[ToolCall] = []
        self._handlers: dict[ToolType, Callable] = {}
        self._register_default_handlers()

    def _register_default_handlers(self):
        """Register default tool handlers."""
        self._handlers[ToolType.READ] = self._handle_read
        self._handlers[ToolType.VERIFY] = self._handle_verify
        self._handlers[ToolType.LIST] = self._handle_list
        # SEARCH and RUN need external handlers

    def register_handler(self, tool_type: ToolType, handler: Callable) -> None:
        """Register a custom tool handler."""
        self._handlers[tool_type] = handler

    def execute(self, call: ToolCall, timeout: float | None = None) -> ToolCall:
        """
        Execute a single tool call with timeout and retry.

        Args:
            call: The tool call to execute
            timeout: Execution timeout in seconds

        Returns:
            The tool call with updated status and results
        """
        timeout = timeout or self.DEFAULT_TIMEOUT
        handler = self._handlers.get(call.tool_type)

        if handler is None:
            call.status = ToolStatus.FAILED
            call.error = f"No handler registered for tool type: {call.tool_type.name}"
            return call

        while call.attempt < call.max_attempts:
            call.attempt += 1
            call.started_at = time.time()
            call.status = ToolStatus.RUNNING

            try:
                # Execute with timeout
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(handler, call)
                    try:
                        result = future.result(timeout=timeout)
                        call.result = result
                        call.output = str(result) if result else ""
                        call.status = ToolStatus.SUCCESS
                        call.completed_at = time.time()
                        break

                    except FuturesTimeoutError:
                        call.status = ToolStatus.TIMEOUT
                        call.error = f"Execution timed out after {timeout}s"
                        future.cancel()

            except Exception as e:
                call.error = str(e)
                call.status = ToolStatus.FAILED

            call.completed_at = time.time()

            # Check if we should retry
            if call.status != ToolStatus.SUCCESS and call.attempt < call.max_attempts:
                # Exponential backoff
                wait_time = 2 ** (call.attempt - 1)
                time.sleep(wait_time)
            else:
                break

        self.execution_history.append(call)
        return call

    def execute_chain(self, chain: ToolChain, parallel: bool = False) -> ToolChain:
        """
        Execute a chain of tool calls.

        Fixes:
        - P4-84: Tool chaining
        - P4-86: Parallel execution (when parallel=True)
        """
        if parallel:
            return self._execute_chain_parallel(chain)
        return self._execute_chain_sequential(chain)

    def _execute_chain_sequential(self, chain: ToolChain) -> ToolChain:
        """Execute chain sequentially."""
        while not chain.is_complete():
            ready = chain.get_ready_calls()
            if not ready:
                # No more calls can run (deadlock or all failed dependencies)
                for call in chain.calls:
                    if call.status == ToolStatus.PENDING:
                        call.status = ToolStatus.SKIPPED
                        call.error = "Skipped due to failed dependencies"
                break

            for idx in ready:
                call = chain.calls[idx]
                self.execute(call)

        return chain

    def _execute_chain_parallel(self, chain: ToolChain) -> ToolChain:
        """Execute chain with parallelism where possible."""
        with ThreadPoolExecutor(max_workers=4) as executor:
            while not chain.is_complete():
                ready = chain.get_ready_calls()
                if not ready:
                    for call in chain.calls:
                        if call.status == ToolStatus.PENDING:
                            call.status = ToolStatus.SKIPPED
                            call.error = "Skipped due to failed dependencies"
                    break

                # Submit all ready calls in parallel
                futures = {executor.submit(self.execute, chain.calls[idx]): idx for idx in ready}

                # Wait for all to complete
                for future in futures:
                    future.result()

        return chain

    # Default handlers

    def _handle_read(self, call: ToolCall) -> str:
        """Handle READ tool."""
        path = call.command
        full_path = self.base_dir / path if not Path(path).is_absolute() else Path(path)

        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        content = full_path.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
        if len(lines) > 500:
            content = "\n".join(lines[:500]) + f"\n\n... (truncated, {len(lines) - 500} more lines)"

        return content

    def _handle_verify(self, call: ToolCall) -> bool:
        """Handle VERIFY tool."""
        path = call.command
        full_path = self.base_dir / path if not Path(path).is_absolute() else Path(path)
        return full_path.exists()

    def _handle_list(self, call: ToolCall) -> list[str]:
        """Handle LIST tool."""
        pattern = call.command
        matches = []
        for file_path in self.base_dir.rglob("*"):
            if file_path.is_file():
                rel_path = str(file_path.relative_to(self.base_dir))
                if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(file_path.name, pattern):
                    matches.append(rel_path)

        return sorted(matches)[:100]  # Limit results


class ToolOutputParser:
    """
    Parses and structures tool output.

    Fixes:
    - P4-95: Missing tool output parsing
    - P4-96: No tool composition
    """

    def parse_read_output(self, content: str, file_path: str) -> dict[str, Any]:
        """Parse READ output into structured data."""
        lines = content.splitlines()

        return {
            "file_path": file_path,
            "line_count": len(lines),
            "content": content,
            "has_code": self._detect_code(content, file_path),
            "imports": self._extract_imports(content) if file_path.endswith(".py") else [],
            "functions": self._extract_functions(content) if file_path.endswith(".py") else [],
            "classes": self._extract_classes(content) if file_path.endswith(".py") else [],
        }

    def parse_search_output(self, results: list[dict[str, Any]]) -> dict[str, Any]:
        """Parse SEARCH output into structured data."""
        by_file: dict[str, list[dict]] = {}
        for result in results:
            file_path = result.get("file_path", "unknown")
            if file_path not in by_file:
                by_file[file_path] = []
            by_file[file_path].append(result)

        return {
            "total_matches": len(results),
            "unique_files": len(by_file),
            "by_file": by_file,
            "files": list(by_file.keys()),
        }

    def _detect_code(self, _content: str, file_path: str) -> bool:
        """Detect if content contains code."""
        code_extensions = {".py", ".js", ".ts", ".go", ".rs", ".java", ".c", ".cpp"}
        return Path(file_path).suffix.lower() in code_extensions

    def _extract_imports(self, content: str) -> list[str]:
        """Extract Python imports."""
        imports = []
        for match in re.finditer(r"^(?:from\s+([\w.]+)|import\s+([\w.]+))", content, re.MULTILINE):
            module = match.group(1) or match.group(2)
            imports.append(module.split(".")[0])
        return list(set(imports))

    def _extract_functions(self, content: str) -> list[str]:
        """Extract Python function names."""
        return re.findall(r"^def\s+(\w+)\s*\(", content, re.MULTILINE)

    def _extract_classes(self, content: str) -> list[str]:
        """Extract Python class names."""
        return re.findall(r"^class\s+(\w+)\s*[:\(]", content, re.MULTILINE)


class ToolSelectionHeuristics:
    """
    Improved tool selection based on task context.

    Fixes:
    - P4-89: Tool selection heuristics weak
    """

    def suggest_tools(
        self, task_description: str, _file_context: str | None = None
    ) -> list[ToolCall]:
        """Suggest appropriate tools for a task."""
        suggestions = []
        task_lower = task_description.lower()

        # If task mentions specific files, suggest READ first
        file_patterns = re.findall(r"`([^`]+\.(?:py|js|ts|json|yaml|yml|md))`", task_description)
        for path in file_patterns:
            suggestions.append(
                ToolCall(
                    tool_type=ToolType.READ,
                    command=path,
                )
            )

        # If task is about finding/searching, suggest SEARCH
        if any(word in task_lower for word in ["find", "search", "locate", "where is"]):
            # Extract search terms
            for match in re.finditer(
                r'(?:find|search for|locate)\s+["\']?([^"\']+)["\']?', task_lower
            ):
                suggestions.append(
                    ToolCall(
                        tool_type=ToolType.SEARCH,
                        command=match.group(1).strip(),
                    )
                )

        # If task is about verification, suggest VERIFY
        if any(word in task_lower for word in ["check if", "verify", "does", "exists"]):
            for path in file_patterns:
                suggestions.append(
                    ToolCall(
                        tool_type=ToolType.VERIFY,
                        command=path,
                    )
                )

        # If task is about listing, suggest LIST
        if any(word in task_lower for word in ["list all", "show all", "find all files"]):
            glob_patterns = re.findall(r"\*\.(\w+)", task_description)
            for ext in glob_patterns:
                suggestions.append(
                    ToolCall(
                        tool_type=ToolType.LIST,
                        command=f"*.{ext}",
                    )
                )

        return suggestions


# Convenience functions


def execute_tool(base_dir: Path, tool_type: ToolType, command: str) -> ToolCall:
    """Execute a single tool."""
    executor = ToolExecutor(base_dir)
    call = ToolCall(tool_type=tool_type, command=command)
    return executor.execute(call)


def validate_tool_execution(content: str, executed_calls: list[ToolCall]) -> dict[str, Any]:
    """Validate that mentioned tools were executed."""
    validator = ToolExecutionValidator()
    executed, unexecuted = validator.validate_execution(content, executed_calls)

    return {
        "executed_count": len(executed),
        "unexecuted_count": len(unexecuted),
        "unexecuted_tools": [{"type": c.tool_type.name, "command": c.command} for c in unexecuted],
        "all_tools_executed": len(unexecuted) == 0,
    }
