"""Tool execution framework for SAGE.

This module provides the tool execution infrastructure for SAGE's
agentic capabilities, including file operations, shell execution,
and search functionality.

P3 Items 123-126: Extract tool execution from main.py.
P0-4: Structured tool execution with validation.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from sage.core.commands import execute_command

__all__ = [
    "ToolType",
    "ToolResult",
    "ToolContext",
    "ToolExecutor",
    "FileWriteTool",
    "FileReadTool",
    "ShellTool",
    "SearchTool",
    "WebFetchTool",
    # P0-4: Structured tool parsing
    "ToolValidationResult",
    "ToolParser",
    "validate_tool_syntax",
    "parse_tool_command",
    # P0-2: Structured tool calls
    "ToolCall",
    "validate_tool_call",
    "parse_tool_commands",
    "execute_tool_call",
    # P1-6: Execution ledger
    "ExecutionLedger",
]


class ToolType(Enum):
    """Types of tools available to SAGE.

    Includes both internal types and text-command aliases (READ, SEARCH, etc.)
    for backwards compatibility with the text-based tool protocol.
    """

    # Internal tool types
    FILE_WRITE = "file_write"
    FILE_READ = "file_read"
    FILE_DELETE = "file_delete"
    SHELL = "shell"
    SEARCH_CODE = "search_code"
    SEARCH_FILES = "search_files"
    WEB_FETCH = "web_fetch"
    GIT = "git"
    LINT = "lint"
    TEST = "test"

    # Text-command aliases (P0-2: Structured tool protocol)
    READ = "read"  # Maps to FILE_READ
    SEARCH = "search"  # Maps to SEARCH_CODE
    RUN = "run"  # Maps to SHELL
    FILE = "file"  # Maps to FILE_WRITE
    BASH = "bash"  # Maps to SHELL


class ToolStatus(Enum):
    """Tool execution status."""

    SUCCESS = "success"
    ERROR = "error"
    DENIED = "denied"
    TIMEOUT = "timeout"


@dataclass
class ToolResult:
    """Result of a tool execution."""

    tool_type: ToolType
    status: ToolStatus
    output: str | None = None
    error: str | None = None
    files_modified: list[str] = field(default_factory=list)
    files_created: list[str] = field(default_factory=list)
    files_deleted: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def success(self) -> bool:
        return self.status == ToolStatus.SUCCESS

    def to_dict(self) -> dict:
        return {
            "tool_type": self.tool_type.value,
            "status": self.status.value,
            "output": self.output,
            "error": self.error,
            "files_modified": self.files_modified,
            "files_created": self.files_created,
            "files_deleted": self.files_deleted,
            "metadata": self.metadata,
        }


# =============================================================================
# P0-2: Structured Tool Calls
# =============================================================================


@dataclass
class ToolCall:
    """A structured tool call with typed fields.

    This replaces the text-based READ:/SEARCH:/RUN: protocol with
    a validated, typed object that the runtime can process directly.

    P0-2: This is the core data structure for structured tool execution.
    """

    tool_type: ToolType
    arguments: dict[str, Any] = field(default_factory=dict)
    validated: bool = False
    source_line: str = ""  # Original text that created this call

    def to_dict(self) -> dict:
        """Serialize for JSON/logging."""
        return {
            "tool_type": self.tool_type.name,
            "arguments": self.arguments,
            "validated": self.validated,
        }

    @classmethod
    def from_dict(cls, data: dict) -> ToolCall:
        """Deserialize from dict."""
        tool_type = ToolType[data["tool_type"]]
        return cls(
            tool_type=tool_type,
            arguments=data.get("arguments", {}),
            validated=data.get("validated", False),
        )


def validate_tool_call(call: ToolCall) -> ToolCall:
    """Validate a ToolCall and return a validated copy.

    Args:
        call: The tool call to validate

    Returns:
        A new ToolCall with validated=True

    Raises:
        ValueError: If validation fails
    """
    # Validate based on tool type
    if call.tool_type in (ToolType.READ, ToolType.FILE_READ):
        if "path" not in call.arguments:
            raise ValueError("READ tool requires 'path' argument")
        path = call.arguments["path"]
        if not path or not path.strip():
            raise ValueError("READ tool 'path' cannot be empty")

    elif call.tool_type in (ToolType.SEARCH, ToolType.SEARCH_CODE):
        if "pattern" not in call.arguments:
            raise ValueError("SEARCH tool requires 'pattern' argument")

    elif call.tool_type in (ToolType.RUN, ToolType.BASH, ToolType.SHELL):
        if "command" not in call.arguments:
            raise ValueError("RUN tool requires 'command' argument")

    elif call.tool_type in (ToolType.FILE, ToolType.FILE_WRITE):
        if "path" not in call.arguments:
            raise ValueError("FILE tool requires 'path' argument")
        if "content" not in call.arguments:
            raise ValueError("FILE tool requires 'content' argument")

    # Return validated copy
    return ToolCall(
        tool_type=call.tool_type,
        arguments=call.arguments.copy(),
        validated=True,
        source_line=call.source_line,
    )


# =============================================================================
# P1-6: Execution Ledger
# =============================================================================


@dataclass
class ExecutionLedger:
    """Tracks all tool executions for evidence-based claim validation.

    P1-6: This ledger is the single source of truth for what actually happened
    during a session. Claims should be derived from this ledger, not parsed
    from model prose.
    """

    files_read: list[str] = field(default_factory=list)
    files_written: list[str] = field(default_factory=list)
    commands_run: list[str] = field(default_factory=list)
    search_patterns: list[str] = field(default_factory=list)
    tests_run: list[str] = field(default_factory=list)
    tests_passed: bool = False
    project_root: str | None = None

    @property
    def total_reads(self) -> int:
        return len(self.files_read)

    @property
    def total_writes(self) -> int:
        return len(self.files_written)

    @property
    def total_commands(self) -> int:
        return len(self.commands_run)

    def record_execution(
        self,
        call: ToolCall,
        success: bool = True,
        output: str = "",
    ) -> None:
        """Record a tool execution in the ledger."""
        if call.tool_type in (ToolType.READ, ToolType.FILE_READ):
            path = call.arguments.get("path", "")
            if path and success:
                self.files_read.append(path)

        elif call.tool_type in (ToolType.FILE, ToolType.FILE_WRITE):
            path = call.arguments.get("path", "")
            if path and success:
                self.files_written.append(path)

        elif call.tool_type in (ToolType.RUN, ToolType.BASH, ToolType.SHELL):
            command = call.arguments.get("command", "")
            if command:
                self.commands_run.append(command)
                # Check if this is a test command
                if "pytest" in command or "test" in command.lower():
                    self.tests_run.append(command)
                    if success and ("passed" in output.lower() or "✓" in output):
                        self.tests_passed = True

        elif call.tool_type in (ToolType.SEARCH, ToolType.SEARCH_CODE):
            pattern = call.arguments.get("pattern", "")
            if pattern:
                self.search_patterns.append(pattern)

    def can_claim_read_count(self, count: int) -> bool:
        """Check if we can claim to have read at least N files."""
        return len(self.files_read) >= count

    def can_claim_write_count(self, count: int) -> bool:
        """Check if we can claim to have written at least N files."""
        return len(self.files_written) >= count

    def can_claim_tests_passed(self) -> bool:
        """Check if we can claim tests passed."""
        return self.tests_passed and len(self.tests_run) > 0

    def bind_project_root(self, root: str | Path | None = None) -> str:
        """Bind the project root once per session.

        P1-7: This method ensures the project root is determined once at session
        start and reused throughout. This prevents path resolution issues when
        the cwd changes during execution.

        Args:
            root: Optional explicit root path. If not provided and not already
                  bound, will use the current working directory.

        Returns:
            The bound project root path as a string.
        """
        if self.project_root is not None:
            # Already bound - return cached value
            return self.project_root

        if root is not None:
            self.project_root = str(Path(root).resolve())
        else:
            # Default to current working directory
            self.project_root = str(Path.cwd().resolve())

        return self.project_root

    def get_project_root(self) -> str | None:
        """Get the bound project root, if any."""
        return self.project_root

    def to_dict(self) -> dict:
        """Serialize for debugging/logging."""
        return {
            "files_read": self.files_read,
            "files_written": self.files_written,
            "commands_run": self.commands_run,
            "search_patterns": self.search_patterns,
            "tests_run": self.tests_run,
            "tests_passed": self.tests_passed,
            "project_root": self.project_root,
        }


@dataclass
class ToolContext:
    """Context for tool execution."""

    cwd: Path
    allowed_paths: list[Path] = field(default_factory=list)
    blocked_patterns: list[str] = field(
        default_factory=lambda: [
            r".*\.env$",
            r".*\.env\..*$",
            r".*\.pem$",
            r".*\.key$",
            r".*id_rsa.*$",
            r".*credentials.*",
            r".*secrets.*",
            r".*\.aws.*",
        ]
    )
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    shell_timeout: int = 60  # seconds
    dry_run: bool = False
    require_confirmation: bool = True

    def is_path_allowed(self, path: Path) -> bool:
        """Check if a path is allowed for modification.

        Security checks performed:
        1. Null byte injection
        2. Path traversal (both Unix and Windows style)
        3. Symlink resolution - ensures final path is within bounds
        4. Absolute paths outside allowed roots
        5. Blocked filename patterns (.env, keys, etc.)
        """
        path_str = str(path)

        # Security: Block null bytes
        if "\x00" in path_str:
            return False

        # Security: Normalize and check for Windows-style path traversal
        # Convert backslashes to forward slashes for security checks
        normalized_path_str = path_str.replace("\\", "/")

        # Block path traversal patterns (both Unix and Windows style)
        if ".." in normalized_path_str:
            return False

        # Block absolute paths outside allowed roots
        if path.is_absolute():
            allowed_roots = [self.cwd.resolve()] + [p.resolve() for p in self.allowed_paths]
            if not any(self._is_subpath(path.resolve(), root) for root in allowed_roots):
                return False

        # Security: Additional check for traversal in original string
        if ".." in path_str:
            # Resolve to check if it escapes
            try:
                resolved = (self.cwd / path).resolve()
                allowed_roots = [self.cwd.resolve()] + [p.resolve() for p in self.allowed_paths]
                if not any(self._is_subpath(resolved, root) for root in allowed_roots):
                    return False
            except (OSError, ValueError):
                return False

        # Resolve to absolute path for further checks
        try:
            abs_path = (self.cwd / path).resolve() if not path.is_absolute() else path.resolve()
        except (OSError, ValueError):
            return False

        # Security: Check if path is a symlink and resolve to final target
        # This prevents symlink-based escapes from the allowed paths
        try:
            if abs_path.is_symlink():
                # Get the final resolved path (follows all symlinks)
                final_path = abs_path.resolve()
                allowed_roots = [self.cwd.resolve()] + [p.resolve() for p in self.allowed_paths]
                if not any(self._is_subpath(final_path, root) for root in allowed_roots):
                    return False
        except (OSError, ValueError):
            return False

        # Must be within cwd or allowed paths
        allowed_roots = [self.cwd.resolve()] + [p.resolve() for p in self.allowed_paths]
        if not any(self._is_subpath(abs_path, root) for root in allowed_roots):
            return False

        # Check blocked patterns against full path and filename
        path_str = str(abs_path)
        filename = abs_path.name
        for pattern in self.blocked_patterns:
            if re.match(pattern, path_str, re.IGNORECASE):
                return False
            if re.match(pattern, filename, re.IGNORECASE):
                return False

        return True

    def _is_subpath(self, path: Path, parent: Path) -> bool:
        """Check if path is under parent."""
        try:
            path.relative_to(parent)
            return True
        except ValueError:
            return False


# Process-wide RunGuard singleton. The Novellia bug class is "we rejected
# package.json but then ran npm install on it anyway" — the guard tracks
# pending rejections across tool invocations within one Sage session.
_RUN_GUARD = None


def get_run_guard():
    """Return the process-wide RunGuard, lazily constructed."""
    global _RUN_GUARD
    if _RUN_GUARD is None:
        try:
            from sage.core.run_guard import RunGuard
            _RUN_GUARD = RunGuard()
        except Exception:
            return None
    return _RUN_GUARD


def _notify_run_guard_rejection(filepath: str, signal: str | None) -> None:
    g = get_run_guard()
    if g is not None and signal:
        try:
            g.record_rejection(filepath, signal)
        except Exception:
            pass


def _notify_run_guard_clean(filepath: str) -> None:
    g = get_run_guard()
    if g is not None:
        try:
            g.record_clean_write(filepath)
        except Exception:
            pass


class FileWriteTool:
    """Tool for writing files safely."""

    def __init__(self, context: ToolContext):
        self.context = context

    def write(
        self,
        filepath: str,
        content: str,
        create_dirs: bool = True,
        backup: bool = True,
    ) -> ToolResult:
        """Write content to a file.

        Args:
            filepath: Relative or absolute path
            content: File content
            create_dirs: Create parent directories if needed
            backup: Create backup of existing file

        Returns:
            ToolResult
        """
        target = Path(filepath)
        if not target.is_absolute():
            target = self.context.cwd / filepath

        # Security check
        if not self.context.is_path_allowed(target):
            return ToolResult(
                tool_type=ToolType.FILE_WRITE,
                status=ToolStatus.DENIED,
                error=f"Path not allowed: {filepath}",
            )

        # Size check
        if len(content.encode()) > self.context.max_file_size:
            return ToolResult(
                tool_type=ToolType.FILE_WRITE,
                status=ToolStatus.ERROR,
                error=f"Content too large: {len(content)} bytes",
            )

        # Content sanity — reject prose-as-code, SAGE protocol leaks,
        # English-word package names, prompt echoes (the Novellia bug class).
        try:
            from sage.core.content_validator import validate_content
            check = validate_content(filepath, content)
            if not check.ok:
                # Notify the run guard so subsequent install commands on this
                # rejected manifest get blocked too (Novellia regression).
                _notify_run_guard_rejection(filepath, check.signal)
                return ToolResult(
                    tool_type=ToolType.FILE_WRITE,
                    status=ToolStatus.ERROR,
                    error=f"REJECTED ({check.signal}): {check.reason}",
                    metadata={"validator_signal": check.signal,
                              "validator_reason": check.reason},
                )
            else:
                # Clean write — clear any prior rejection block on this file
                _notify_run_guard_clean(filepath)
        except Exception:
            # If the validator itself is broken, fail-open rather than fail-closed
            # (better to write maybe-bad content than block the agent entirely).
            pass

        if self.context.dry_run:
            return ToolResult(
                tool_type=ToolType.FILE_WRITE,
                status=ToolStatus.SUCCESS,
                output=f"[DRY RUN] Would write {len(content)} bytes to {filepath}",
                metadata={"dry_run": True},
            )

        try:
            existed = target.exists()

            # Create backup
            if existed and backup:
                backup_path = target.with_suffix(target.suffix + ".bak")
                backup_path.write_text(target.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")

            # Create directories
            if create_dirs:
                target.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            target.write_text(content)

            # TDD enforcement: Run tests after writing code files
            tdd_output = ""
            tdd_passed = True
            if target.suffix == ".py":
                from sage.core.tdd import validate_code_write

                tdd_result = validate_code_write(target, content)
                if not tdd_result.passed and tdd_result.tests_run > 0:
                    # Tests failed or coverage insufficient - rollback
                    if existed and backup:
                        backup_path = target.with_suffix(target.suffix + ".bak")
                        if backup_path.exists():
                            target.write_text(backup_path.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
                    elif not existed:
                        target.unlink()

                    return ToolResult(
                        tool_type=ToolType.FILE_WRITE,
                        status=ToolStatus.ERROR,
                        error=f"TDD BLOCKED: {tdd_result.summary()}",
                        metadata={
                            "tdd_result": {
                                "passed": False,
                                "tests_run": tdd_result.tests_run,
                                "tests_failed": tdd_result.tests_failed,
                                "coverage": tdd_result.coverage_percent,
                                "required_coverage": tdd_result.coverage_required,
                            }
                        },
                    )
                tdd_output = f"\n{tdd_result.summary()}"
                tdd_passed = tdd_result.passed

            return ToolResult(
                tool_type=ToolType.FILE_WRITE,
                status=ToolStatus.SUCCESS,
                output=f"Wrote {len(content)} bytes to {filepath}{tdd_output}",
                files_modified=[str(filepath)] if existed else [],
                files_created=[str(filepath)] if not existed else [],
                metadata={
                    "tdd_validated": tdd_passed,
                }
                if target.suffix == ".py"
                else {},
            )

        except Exception as e:
            return ToolResult(
                tool_type=ToolType.FILE_WRITE,
                status=ToolStatus.ERROR,
                error=str(e),
            )


class FileReadTool:
    """Tool for reading files."""

    def __init__(self, context: ToolContext):
        self.context = context
        self.max_lines = 1000
        self.max_size = 1024 * 1024  # 1MB

    def read(
        self,
        filepath: str,
        max_lines: int | None = None,
        start_line: int = 1,
    ) -> ToolResult:
        """Read a file.

        Args:
            filepath: Path to file
            max_lines: Maximum lines to read
            start_line: Starting line number (1-indexed)

        Returns:
            ToolResult with file content
        """
        target = Path(filepath)
        if not target.is_absolute():
            target = self.context.cwd / filepath

        # Security check - verify path is allowed (handles symlinks, traversal, etc.)
        if not self.context.is_path_allowed(target):
            return ToolResult(
                tool_type=ToolType.FILE_READ,
                status=ToolStatus.DENIED,
                error=f"Path not allowed: {filepath}",
            )

        if not target.exists():
            return ToolResult(
                tool_type=ToolType.FILE_READ,
                status=ToolStatus.ERROR,
                error=f"File not found: {filepath}",
            )

        if not target.is_file():
            return ToolResult(
                tool_type=ToolType.FILE_READ,
                status=ToolStatus.ERROR,
                error=f"Not a file: {filepath}",
            )

        try:
            # Check size
            size = target.stat().st_size
            if size > self.max_size:
                return ToolResult(
                    tool_type=ToolType.FILE_READ,
                    status=ToolStatus.ERROR,
                    error=f"File too large: {size} bytes (max {self.max_size})",
                )

            content = target.read_text(encoding="utf-8", errors="replace")
            lines = content.split("\n")
            total_lines = len(lines)

            # Apply line limits
            max_l = max_lines or self.max_lines
            start_idx = max(0, start_line - 1)
            end_idx = min(start_idx + max_l, total_lines)

            selected_lines = lines[start_idx:end_idx]
            truncated = end_idx < total_lines

            # Add line numbers
            numbered = [
                f"{i}: {line}" for i, line in enumerate(selected_lines, start=start_idx + 1)
            ]

            output = "\n".join(numbered)
            if truncated:
                output += f"\n... ({total_lines - end_idx} more lines)"

            return ToolResult(
                tool_type=ToolType.FILE_READ,
                status=ToolStatus.SUCCESS,
                output=output,
                metadata={
                    "total_lines": total_lines,
                    "lines_shown": len(selected_lines),
                    "truncated": truncated,
                },
            )

        except Exception as e:
            return ToolResult(
                tool_type=ToolType.FILE_READ,
                status=ToolStatus.ERROR,
                error=str(e),
            )


class ShellTool:
    """Tool for executing shell commands safely."""

    # Commands that are always blocked
    BLOCKED_COMMANDS = {
        "rm -rf /",
        "rm -rf /*",
        "mkfs",
        "dd if=/dev/zero",
        ":(){:|:&};:",
        "chmod -R 777 /",
        "chmod 777 /",
        "shutdown",
        "reboot",
        "halt",
        "poweroff",
    }

    # Patterns for dangerous commands
    DANGEROUS_PATTERNS = [
        r"^sudo\s+",  # sudo commands
        r"^doas\s+",  # doas commands (OpenBSD sudo alternative)
        r"rm\s+.*-rf\s+/(?!\w)",  # rm -rf / or rm -rf /*
        r"rm\s+-rf\s+/(?!\w)",  # rm -rf /
        r">\s*/dev/sd[a-z]",  # Write to raw devices
        r"dd\s+.*of=/dev/sd",  # dd to raw devices
        r"dd\s+.*of=/dev/sda",  # dd to raw devices
        r"chmod.*777\s+/(?!\w|\S)",  # chmod 777 on root
        r"mkfs\.",  # mkfs commands
    ]

    def __init__(self, context: ToolContext):
        self.context = context
        self.history: list[tuple[str, ToolResult]] = []

    def execute(
        self,
        command: str,
        timeout: int | None = None,
        cwd: Path | None = None,
    ) -> ToolResult:
        """Execute a shell command.

        Args:
            command: Shell command to execute
            timeout: Timeout in seconds
            cwd: Working directory (default: context.cwd)

        Returns:
            ToolResult with command output
        """
        # Safety checks
        if self._is_blocked(command):
            result = ToolResult(
                tool_type=ToolType.SHELL,
                status=ToolStatus.DENIED,
                error=f"Blocked dangerous command: {command}",
            )
            self.history.append((command, result))
            return result

        work_dir = cwd or self.context.cwd
        timeout_secs = timeout or self.context.shell_timeout

        if self.context.dry_run:
            result = ToolResult(
                tool_type=ToolType.SHELL,
                status=ToolStatus.SUCCESS,
                output=f"[DRY RUN] Would execute: {command}",
                metadata={"dry_run": True},
            )
            self.history.append((command, result))
            return result

        # P0-10-15: Use safe command execution instead of shell=True
        cmd_result = execute_command(
            command,
            cwd=work_dir,
            timeout=timeout_secs,
            allow_shell=True,  # Complex commands may need shell
            validate=False,  # Already validated by _is_blocked
        )

        output = cmd_result.stdout
        if cmd_result.stderr:
            output += f"\n[stderr]\n{cmd_result.stderr}"

        if cmd_result.timed_out:
            status = ToolStatus.TIMEOUT
            error = f"Command timed out after {timeout_secs}s"
        elif cmd_result.error:
            status = ToolStatus.ERROR
            error = cmd_result.error
        else:
            status = ToolStatus.SUCCESS if cmd_result.success else ToolStatus.ERROR
            error = cmd_result.stderr if not cmd_result.success else None

        result = ToolResult(
            tool_type=ToolType.SHELL,
            status=status,
            output=output,
            error=error,
            metadata={
                "return_code": cmd_result.returncode,
                "command": command,
            },
        )
        self.history.append((command, result))
        return result

    def _is_blocked(self, command: str) -> bool:
        """Check if a command is blocked."""
        cmd_lower = command.lower().strip()

        # Check exact blocks
        if cmd_lower in self.BLOCKED_COMMANDS:
            return True

        # Check patterns
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return True

        return False


class SearchTool:
    """Tool for searching code and files."""

    def __init__(self, context: ToolContext):
        self.context = context

    def search_code(
        self,
        pattern: str,
        file_pattern: str = "*",
        max_results: int = 50,
        case_sensitive: bool = False,
    ) -> ToolResult:
        """Search for pattern in code.

        Args:
            pattern: Search pattern (regex)
            file_pattern: Glob pattern for files
            max_results: Maximum results to return
            case_sensitive: Case sensitive search

        Returns:
            ToolResult with matches
        """
        try:
            # Use ripgrep if available, else grep
            rg_available = (
                subprocess.run(
                    ["rg", "--version"],
                    capture_output=True,
                    stdin=subprocess.DEVNULL,
                ).returncode
                == 0
            )

            if rg_available:
                cmd = ["rg", "--line-number", "--max-count", str(max_results)]
                if not case_sensitive:
                    cmd.append("-i")
                if file_pattern != "*":
                    cmd.extend(["--glob", file_pattern])
                cmd.append(pattern)
            else:
                cmd = ["grep", "-rn"]
                if not case_sensitive:
                    cmd.append("-i")
                cmd.extend(["--include", file_pattern, pattern, "."])

            proc = subprocess.run(
                cmd,
                cwd=self.context.cwd,
                capture_output=True,
                text=True,
                timeout=30,
                stdin=subprocess.DEVNULL,
            )

            lines = proc.stdout.strip().split("\n") if proc.stdout else []
            matches = lines[:max_results]

            return ToolResult(
                tool_type=ToolType.SEARCH_CODE,
                status=ToolStatus.SUCCESS,
                output="\n".join(matches) if matches else "No matches found",
                metadata={
                    "pattern": pattern,
                    "match_count": len(matches),
                    "truncated": len(lines) > max_results,
                },
            )

        except subprocess.TimeoutExpired:
            return ToolResult(
                tool_type=ToolType.SEARCH_CODE,
                status=ToolStatus.TIMEOUT,
                error="Search timed out",
            )
        except Exception as e:
            return ToolResult(
                tool_type=ToolType.SEARCH_CODE,
                status=ToolStatus.ERROR,
                error=str(e),
            )

    def search_files(
        self,
        pattern: str,
        max_results: int = 100,
    ) -> ToolResult:
        """Search for files by name pattern.

        Args:
            pattern: Glob or regex pattern
            max_results: Maximum results

        Returns:
            ToolResult with matching file paths
        """
        try:
            matches = []
            for path in self.context.cwd.rglob(pattern):
                if len(matches) >= max_results:
                    break
                # Skip hidden and common ignore dirs
                rel_path = path.relative_to(self.context.cwd)
                parts = rel_path.parts
                if any(
                    p.startswith(".") or p in {"node_modules", "__pycache__", "venv", ".venv"}
                    for p in parts
                ):
                    continue
                matches.append(str(rel_path))

            return ToolResult(
                tool_type=ToolType.SEARCH_FILES,
                status=ToolStatus.SUCCESS,
                output="\n".join(matches) if matches else "No files found",
                metadata={
                    "pattern": pattern,
                    "file_count": len(matches),
                },
            )

        except Exception as e:
            return ToolResult(
                tool_type=ToolType.SEARCH_FILES,
                status=ToolStatus.ERROR,
                error=str(e),
            )


class WebFetchTool:
    """Tool for fetching web content."""

    # Blocked URL schemes
    BLOCKED_SCHEMES = {"file", "ftp", "javascript", "data"}

    # Blocked hosts (SSRF prevention)
    BLOCKED_HOSTS = {
        "localhost",
        "127.0.0.1",
        "0.0.0.0",
        "::1",
    }

    # Blocked IP ranges (SSRF prevention)
    BLOCKED_IP_PREFIXES = [
        "10.",  # Private Class A
        "172.16.",
        "172.17.",
        "172.18.",
        "172.19.",
        "172.20.",
        "172.21.",
        "172.22.",
        "172.23.",
        "172.24.",
        "172.25.",
        "172.26.",
        "172.27.",
        "172.28.",
        "172.29.",
        "172.30.",
        "172.31.",  # Private Class B
        "192.168.",  # Private Class C
        "169.254.",  # Link-local
    ]

    def __init__(self, context: ToolContext):
        self.context = context
        self._session = None

    def _is_blocked_url(self, url: str) -> tuple[bool, str]:
        """Check if a URL should be blocked for security reasons."""
        from urllib.parse import urlparse

        try:
            parsed = urlparse(url)
        except Exception:
            return True, "Invalid URL format"

        # Check scheme
        scheme = parsed.scheme.lower()
        if scheme in self.BLOCKED_SCHEMES:
            return True, f"Blocked scheme: {scheme}"
        if scheme not in {"http", "https"}:
            return True, f"Unsupported scheme: {scheme}"

        # Check host
        host = parsed.hostname or ""
        host_lower = host.lower()

        if host_lower in self.BLOCKED_HOSTS:
            return True, f"Blocked host: {host}"

        # Check IP prefixes
        for prefix in self.BLOCKED_IP_PREFIXES:
            if host.startswith(prefix):
                return True, f"Blocked internal IP: {host}"

        return False, ""

    def fetch(
        self,
        url: str,
        timeout: int = 10,
    ) -> ToolResult:
        """Fetch content from a URL.

        Args:
            url: URL to fetch
            timeout: Request timeout

        Returns:
            ToolResult with page content
        """
        # Security: Check for blocked URLs (SSRF prevention)
        blocked, reason = self._is_blocked_url(url)
        if blocked:
            return ToolResult(
                tool_type=ToolType.WEB_FETCH,
                status=ToolStatus.DENIED,
                error=f"URL blocked: {reason}",
                metadata={"url": url},
            )

        try:
            import httpx
        except ImportError:
            return ToolResult(
                tool_type=ToolType.WEB_FETCH,
                status=ToolStatus.ERROR,
                error="httpx not installed",
            )

        try:
            with httpx.Client(timeout=timeout) as client:
                response = client.get(url)
                response.raise_for_status()

                content_type = response.headers.get("content-type", "")

                if "text/html" in content_type:
                    # Try to extract text from HTML
                    try:
                        from bs4 import BeautifulSoup

                        soup = BeautifulSoup(response.text, "html.parser")
                        # Remove script and style elements
                        for script in soup(["script", "style"]):
                            script.decompose()
                        text = soup.get_text(separator="\n", strip=True)
                    except ImportError:
                        text = response.text
                else:
                    text = response.text

                # Truncate if too long
                max_chars = 50000
                if len(text) > max_chars:
                    text = text[:max_chars] + "\n...(truncated)"

                return ToolResult(
                    tool_type=ToolType.WEB_FETCH,
                    status=ToolStatus.SUCCESS,
                    output=text,
                    metadata={
                        "url": url,
                        "status_code": response.status_code,
                        "content_type": content_type,
                    },
                )

        except Exception as e:
            return ToolResult(
                tool_type=ToolType.WEB_FETCH,
                status=ToolStatus.ERROR,
                error=str(e),
                metadata={"url": url},
            )


class ToolExecutor:
    """Central executor for all tools."""

    def __init__(self, context: ToolContext):
        self.context = context
        self.file_write = FileWriteTool(context)
        self.file_read = FileReadTool(context)
        self.shell = ShellTool(context)
        self.search = SearchTool(context)
        self.web_fetch = WebFetchTool(context)
        self.history: list[ToolResult] = []

    def execute(
        self,
        tool_type: ToolType,
        **kwargs: Any,
    ) -> ToolResult:
        """Execute a tool by type.

        Args:
            tool_type: Type of tool to execute
            **kwargs: Tool-specific arguments

        Returns:
            ToolResult
        """
        if tool_type == ToolType.FILE_WRITE:
            result = self.file_write.write(**kwargs)
        elif tool_type == ToolType.FILE_READ:
            result = self.file_read.read(**kwargs)
        elif tool_type == ToolType.SHELL:
            result = self.shell.execute(**kwargs)
        elif tool_type == ToolType.SEARCH_CODE:
            result = self.search.search_code(**kwargs)
        elif tool_type == ToolType.SEARCH_FILES:
            result = self.search.search_files(**kwargs)
        elif tool_type == ToolType.WEB_FETCH:
            result = self.web_fetch.fetch(**kwargs)
        else:
            result = ToolResult(
                tool_type=tool_type,
                status=ToolStatus.ERROR,
                error=f"Unknown tool type: {tool_type}",
            )

        self.history.append(result)
        return result

    def get_history(self, limit: int = 10) -> list[ToolResult]:
        """Get recent tool execution history."""
        return self.history[-limit:]

    def clear_history(self) -> None:
        """Clear tool history."""
        self.history.clear()


# =============================================================================
# P0-4: Structured Tool Parsing and Validation
# =============================================================================


@dataclass
class ToolValidationResult:
    """Result of tool syntax validation.

    This is used BEFORE tool execution to detect bad tool syntax patterns
    from LLM output that should never be executed.
    """

    valid: bool
    tool_name: str | None = None
    arguments: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    error_type: str | None = None  # "invalid_syntax", "described_not_executed", "bad_path"
    raw_text: str = ""

    def to_dict(self) -> dict:
        return {
            "valid": self.valid,
            "tool_name": self.tool_name,
            "arguments": self.arguments,
            "error": self.error,
            "error_type": self.error_type,
        }


class ToolParser:
    """Structured tool command parser with validation.

    This parser validates tool commands from LLM output BEFORE execution.
    It detects and rejects:
    - Invalid tool syntax (XML tags, function calls, YAML)
    - Tool descriptions instead of executions
    - Invalid file paths (garbage, hypothetical)
    - Malformed arguments
    """

    # Valid SAGE tool commands (uppercase canonical names)
    VALID_TOOLS = {
        "READ",
        "WRITE",
        "EDIT",
        "DELETE",
        "BASH",
        "RUN",
        "SHELL",
        "SEARCH",
        "GREP",
        "FIND",
        "WEB",
        "FETCH",
        "ASK",
        "QUESTION",
        "PLAN",
        "TASK",
    }

    # Patterns that indicate INVALID tool syntax (LLM hallucination)
    INVALID_SYNTAX_PATTERNS = [
        # XML-style tool calls (Claude/Anthropic style)
        (r"<tool_use>", "XML tool_use tag"),
        (r"<function_call[\s>]", "XML function_call tag"),  # Match with space or closing >
        (
            r"<function_call\s+name\s*=",
            "XML function_call with name attribute",
        ),  # <function_call name='...'>
        (r"<invoke>", "XML invoke tag"),
        (r"</tool>", "XML closing tool tag"),
        (r"</function_call>", "XML closing function_call tag"),
        (r"<tool\s+name=", "XML tool with name attribute"),
        # Function-call style (OpenAI style)
        (r"^\s*\{?\s*\"?name\"?\s*:\s*\"?\w+\"?\s*,\s*\"?arguments\"?\s*:", "JSON function call"),
        (r"functions\.\w+\(", "Function dot notation"),
        # YAML-style - expanded patterns
        (r"^---\s*\n\s*tool:\s*\w+", "YAML tool header"),
        (r"^\s*tool:\s*\w+\s*\n\s*args:", "YAML tool with args"),
        (r"tool_name:\s*\w+", "YAML tool_name key"),  # tool_name: read
        (r"parameters:\s*\n", "YAML parameters key"),  # parameters:\n
        (r"function:\s*\w+\s*\n\s*args:", "YAML function with args"),
        # Tool descriptions (saying what to do instead of doing it)
        (r"I will use (the )?(READ|WRITE|EDIT|BASH|RUN|SEARCH)\b", "described tool intention"),
        (r"I would use (the )?(READ|WRITE|EDIT|BASH|RUN|SEARCH)\b", "described hypothetical tool"),
        (r"I should use (the )?(READ|WRITE|EDIT|BASH|RUN|SEARCH)\b", "described tool suggestion"),
        (r"Let me use (the )?(READ|WRITE|EDIT|BASH|RUN|SEARCH)\b", "described tool intention"),
        (r"Using (the )?(READ|WRITE|EDIT|BASH|RUN|SEARCH) tool", "described tool usage"),
        (r"I'll (use|run|execute) (the )?(READ|WRITE|EDIT|BASH)\b", "described future action"),
    ]

    # Patterns for invalid file paths (garbage, hypothetical)
    INVALID_PATH_PATTERNS = [
        # Garbage/unreadable paths
        (r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "contains control characters"),
        (r"[^\x00-\x7F]{5,}", "contains too many non-ASCII characters"),
        (r"^\s*\.\.\.", "ellipsis path"),
        (r"^\s*<[^>]+>", "placeholder path"),
        (r"^\s*\[.*\]", "bracketed placeholder"),
        (r"your[_-]?(?:path|file|project)", "placeholder 'your' path"),
        (r"example[_-]?(?:path|file)", "example placeholder"),
        (r"/path/to/", "generic placeholder path"),
        (r"c:\\path\\to\\", "Windows placeholder path"),
        # Hypothetical/descriptive
        (r"(?:some|any|the)[_\s]file", "vague file reference"),
        (r"file(?:name)?[_\s]here", "placeholder filename"),
    ]

    @classmethod
    def validate_tool_syntax(cls, text: str) -> ToolValidationResult:
        """Validate that text is NOT using invalid tool syntax.

        Returns ToolValidationResult with valid=False if bad patterns detected.
        This should be called on LLM output BEFORE attempting to parse tools.
        """
        text_lower = text.lower()

        for pattern, error_desc in cls.INVALID_SYNTAX_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
                return ToolValidationResult(
                    valid=False,
                    error=f"Invalid tool syntax: {error_desc}",
                    error_type="invalid_syntax",
                    raw_text=text[:500],
                )

        return ToolValidationResult(valid=True, raw_text=text[:500])

    @classmethod
    def validate_file_path(cls, path: str) -> ToolValidationResult:
        """Validate that a file path is not garbage or placeholder.

        Returns ToolValidationResult with valid=False if bad path detected.
        """
        if not path or not path.strip():
            return ToolValidationResult(
                valid=False,
                error="Empty file path",
                error_type="bad_path",
                raw_text=path or "",
            )

        path = path.strip()

        for pattern, error_desc in cls.INVALID_PATH_PATTERNS:
            if re.search(pattern, path, re.IGNORECASE):
                return ToolValidationResult(
                    valid=False,
                    error=f"Invalid file path: {error_desc}",
                    error_type="bad_path",
                    raw_text=path,
                )

        # Additional checks
        if len(path) > 1000:
            return ToolValidationResult(
                valid=False,
                error="File path too long",
                error_type="bad_path",
                raw_text=path[:100] + "...",
            )

        # Check for reasonable file path structure
        # Must have at least one alphanumeric character
        if not re.search(r"[a-zA-Z0-9]", path):
            return ToolValidationResult(
                valid=False,
                error="File path has no valid characters",
                error_type="bad_path",
                raw_text=path,
            )

        return ToolValidationResult(valid=True, raw_text=path)

    @classmethod
    def parse_tool_command(cls, line: str) -> ToolValidationResult:
        """Parse a single SAGE tool command line.

        Expected format: TOOL_NAME: argument
        e.g., READ: src/main.py
              BASH: pytest tests/
              WRITE: config.json
              {"content": "..."}

        Returns ToolValidationResult with parsed tool info or error.
        """
        line = line.strip()
        if not line:
            return ToolValidationResult(
                valid=False,
                error="Empty tool command",
                error_type="invalid_syntax",
                raw_text="",
            )

        # First check for invalid syntax patterns
        syntax_check = cls.validate_tool_syntax(line)
        if not syntax_check.valid:
            return syntax_check

        # Match TOOL: argument pattern
        match = re.match(r"^([A-Z_]+):\s*(.*)$", line, re.DOTALL)
        if not match:
            return ToolValidationResult(
                valid=False,
                error="Tool command must be TOOL_NAME: argument",
                error_type="invalid_syntax",
                raw_text=line[:200],
            )

        tool_name = match.group(1).upper()
        argument = match.group(2).strip()

        # Validate tool name
        if tool_name not in cls.VALID_TOOLS:
            return ToolValidationResult(
                valid=False,
                error=f"Unknown tool: {tool_name}",
                error_type="invalid_syntax",
                raw_text=line[:200],
            )

        # For file-based tools, validate the path
        if tool_name in {"READ", "WRITE", "EDIT", "DELETE"}:
            path_check = cls.validate_file_path(argument)
            if not path_check.valid:
                return path_check

        return ToolValidationResult(
            valid=True,
            tool_name=tool_name,
            arguments={"target": argument},
            raw_text=line,
        )

    @classmethod
    def extract_tools_from_response(cls, response_text: str) -> list[ToolValidationResult]:
        """Extract and validate all tool commands from an LLM response.

        Returns a list of ToolValidationResults for each detected tool command.
        Invalid tools are included with valid=False.
        """
        results: list[ToolValidationResult] = []

        # First, check for global invalid patterns (e.g., XML tags anywhere)
        global_check = cls.validate_tool_syntax(response_text)
        if not global_check.valid:
            results.append(global_check)
            return results

        # Look for tool command patterns
        lines = response_text.split("\n")
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Check for TOOL: pattern
            if re.match(r"^[A-Z_]+:\s*", line):
                # Handle multi-line tool commands (e.g., WRITE with content block)
                if line.startswith("WRITE:") or line.startswith("EDIT:"):
                    # Look for content block following
                    full_command = line
                    j = i + 1
                    # Check if next line starts JSON content
                    if j < len(lines) and lines[j].strip().startswith("{"):
                        # Collect until closing brace
                        brace_count = 0
                        content_lines = []
                        while j < len(lines):
                            content_line = lines[j]
                            content_lines.append(content_line)
                            brace_count += content_line.count("{") - content_line.count("}")
                            j += 1
                            if brace_count <= 0:
                                break
                        full_command = line + "\n" + "\n".join(content_lines)
                        i = j - 1

                    result = cls.parse_tool_command(full_command.split("\n")[0])
                    results.append(result)
                else:
                    result = cls.parse_tool_command(line)
                    results.append(result)

            i += 1

        return results


# Convenience functions for use in other modules
def validate_tool_syntax(text: str) -> ToolValidationResult:
    """Validate that text doesn't contain invalid tool syntax patterns."""
    return ToolParser.validate_tool_syntax(text)


_NESTED_COMMAND_RE = re.compile(
    r"^\s*(READ|SEARCH|SEARCH_WEB|RUN|BASH|WEB_FETCH|FILE|WRITE|EDIT)\s*:",
    re.IGNORECASE,
)


def _argument_starts_with_command(arg: str) -> bool:
    """Detect 'READ: SEARCH: *.py' — argument is itself another command.

    This is a small-model failure mode: instead of emitting two separate
    tool lines, it crams them on one line. Executing it as-is reads a
    non-existent file named "SEARCH: *.py".
    """
    return bool(_NESTED_COMMAND_RE.match(arg or ""))


def parse_tool_command(text: str) -> ToolCall | None:
    """Parse a tool command and return a ToolCall.

    P0-2: This converts text commands to structured ToolCall objects.

    Args:
        text: A line like "READ: path/to/file" or a FILE: block with content

    Returns:
        ToolCall if valid command, None if invalid or not a command
    """
    # Handle multi-line FILE: blocks
    if text.strip().upper().startswith("FILE:"):
        lines = text.split("\n")
        first_line = lines[0].strip()
        path = first_line[5:].strip()  # Extract path after "FILE:"
        # Reject FILE: <COMMAND>: foo (nested command in path)
        if _argument_starts_with_command(path):
            return None
        content = "\n".join(lines[1:]) if len(lines) > 1 else ""
        if path:
            return ToolCall(
                tool_type=ToolType.FILE,
                arguments={"path": path, "content": content},
                validated=False,
                source_line=first_line,
            )
        return None

    # For single-line commands, use the first line only
    line = text.split("\n", maxsplit=1)[0].strip()

    # Check for invalid syntax first
    syntax_check = ToolParser.validate_tool_syntax(line)
    if not syntax_check.valid:
        return None

    # Parse the command
    result = ToolParser.parse_tool_command(line)
    if not result.valid:
        return None

    # Reject nested commands: "READ: SEARCH: *.py"
    target_arg = result.arguments.get("target", "")
    if _argument_starts_with_command(target_arg):
        return None

    # Convert to ToolCall
    tool_name = result.tool_name
    if not tool_name:
        return None

    # Map tool names to ToolType
    tool_type_map = {
        "READ": ToolType.READ,
        "SEARCH": ToolType.SEARCH,
        "RUN": ToolType.RUN,
        "BASH": ToolType.BASH,
        "FILE": ToolType.FILE,
        "WRITE": ToolType.FILE_WRITE,
        "EDIT": ToolType.FILE_WRITE,
    }

    tool_type = tool_type_map.get(tool_name.upper())
    if not tool_type:
        return None

    # Convert "target" argument to appropriate key based on tool type
    target = result.arguments.get("target", "")
    arguments = {}

    if tool_type in (ToolType.READ, ToolType.FILE_READ):
        arguments["path"] = target
    elif tool_type in (ToolType.SEARCH, ToolType.SEARCH_CODE):
        arguments["pattern"] = target
    elif tool_type in (ToolType.RUN, ToolType.BASH, ToolType.SHELL):
        arguments["command"] = target
    elif tool_type in (ToolType.FILE, ToolType.FILE_WRITE):
        arguments["path"] = target
        arguments["content"] = ""  # Will be filled by parse_tool_commands for FILE blocks
    else:
        arguments = result.arguments.copy()

    return ToolCall(
        tool_type=tool_type,
        arguments=arguments,
        validated=False,
        source_line=line,
    )


def parse_tool_commands(text: str) -> list[ToolCall]:
    """Parse multiple tool commands from text.

    P0-2: Batch parsing for structured tool calls.

    Args:
        text: Multi-line text containing tool commands

    Returns:
        List of valid ToolCall objects
    """
    calls = []

    # Handle FILE: blocks with content
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        # Check for FILE: block with content
        if line.upper().startswith("FILE:"):
            # Extract path
            path = line[5:].strip()
            # Collect content lines until next command or end
            content_lines = []
            i += 1
            while i < len(lines):
                next_line = lines[i]
                # Check if this is a new command
                if re.match(
                    r"^(READ|SEARCH|RUN|BASH|FILE|WRITE|EDIT):\s", next_line.strip(), re.IGNORECASE
                ):
                    break
                content_lines.append(next_line)
                i += 1

            content = "\n".join(content_lines)
            calls.append(
                ToolCall(
                    tool_type=ToolType.FILE,
                    arguments={"path": path, "content": content},
                    validated=False,
                    source_line=line,
                )
            )
        else:
            call = parse_tool_command(line)
            if call:
                calls.append(call)
            i += 1

    return calls


def execute_tool_call(call: ToolCall) -> ToolResult:
    """Execute a validated tool call.

    P0-2: This is the structured execution entry point.

    Args:
        call: A validated ToolCall

    Returns:
        ToolResult with execution status and output

    Raises:
        ValueError: If call is not validated
    """
    if not call.validated:
        raise ValueError("Tool call is not validated. Call validate_tool_call() first.")

    # Execute based on tool type
    if call.tool_type in (ToolType.READ, ToolType.FILE_READ):
        path = call.arguments.get("path", "")
        try:
            content = Path(path).read_text(encoding="utf-8", errors="replace")
            return ToolResult(
                tool_type=call.tool_type,
                status=ToolStatus.SUCCESS,
                output=content,
            )
        except Exception as e:
            return ToolResult(
                tool_type=call.tool_type,
                status=ToolStatus.ERROR,
                error=str(e),
            )

    elif call.tool_type in (ToolType.SEARCH, ToolType.SEARCH_CODE):
        pattern = call.arguments.get("pattern", "")
        search_path = call.arguments.get("path", ".")
        try:
            result = subprocess.run(
                ["grep", "-r", "-n", pattern, search_path],
                capture_output=True,
                text=True,
                timeout=30,
                stdin=subprocess.DEVNULL,
            )
            return ToolResult(
                tool_type=call.tool_type,
                status=ToolStatus.SUCCESS,
                output=result.stdout,
                metadata={
                    "matches": len(result.stdout.strip().split("\n"))
                    if result.stdout.strip()
                    else 0
                },
            )
        except Exception as e:
            return ToolResult(
                tool_type=call.tool_type,
                status=ToolStatus.ERROR,
                error=str(e),
            )

    elif call.tool_type in (ToolType.RUN, ToolType.BASH, ToolType.SHELL):
        command = call.arguments.get("command", "")
        try:
            # Route through run_shell so Windows users get bash semantics
            # (Git Bash / WSL) instead of cmd.exe — the agent emits POSIX
            # idioms that cmd.exe can't parse.
            from sage.core.commands import run_shell

            result = run_shell(command, timeout=120)
            return ToolResult(
                tool_type=call.tool_type,
                status=ToolStatus.SUCCESS if result.returncode == 0 else ToolStatus.ERROR,
                output=result.stdout + result.stderr,
                metadata={"returncode": result.returncode},
            )
        except Exception as e:
            return ToolResult(
                tool_type=call.tool_type,
                status=ToolStatus.ERROR,
                error=str(e),
            )

    elif call.tool_type in (ToolType.FILE, ToolType.FILE_WRITE):
        path = call.arguments.get("path", "")
        content = call.arguments.get("content", "")
        try:
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            return ToolResult(
                tool_type=call.tool_type,
                status=ToolStatus.SUCCESS,
                files_created=[path],
            )
        except Exception as e:
            return ToolResult(
                tool_type=call.tool_type,
                status=ToolStatus.ERROR,
                error=str(e),
            )

    return ToolResult(
        tool_type=call.tool_type,
        status=ToolStatus.ERROR,
        error=f"Unsupported tool type: {call.tool_type}",
    )
