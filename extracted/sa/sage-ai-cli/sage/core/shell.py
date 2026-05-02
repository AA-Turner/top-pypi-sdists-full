"""Shell command execution utilities for SAGE.

This module contains functions for:
- Running shell commands with scoped directory support
- Extracting shell/bash blocks from text
- Quoting strings for safe shell use
- Reading files with line numbers

Extracted from main.py for better code organization (P3-73).

P0-10-15: Now uses safe execution via commands.py instead of shell=True.

P2-25: Unified Command Safety Policy
=====================================
This module works with sage/core/commands.py to provide consistent command safety:

1. commands.py provides:
   - CommandRisk enum (SAFE, NEEDS_REVIEW, BLOCKED)
   - validate_command() for allowlist checking
   - execute_command() as the primary execution entry point

2. shell.py provides:
   - SAFE_READONLY_COMMANDS: Commands safe for analysis mode
   - BLOCKED_READONLY_PATTERNS: Dangerous patterns to block
   - is_safe_readonly_command(): Validation for read-only flows
   - run_readonly_shell(): Safe execution wrapper

All command execution should go through:
- execute_command() for general execution with validation
- run_readonly_shell() for read-only analysis contexts
"""

from __future__ import annotations

import atexit
import logging
import os
import re
import shlex
import subprocess
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path

from sage.core.commands import CommandResult, execute_command

logger = logging.getLogger(__name__)

__all__ = [
    "extract_scoped_prefix",
    "resolve_scoped_directory",
    "portable_grep",
    "run_shell",
    "safe_shell_exec",
    "shell_quote",
    "extract_bash_blocks",
    "sanitize_shell_block",
    "strip_search_comment",
    "read_file_context",
    "CommandResult",
    # TDD-specific functions
    "run_tdd_test",
    "detect_test_framework",
    "parse_test_output",
    "has_test_errors",
    "get_test_error_summary",
    # P0-7: Read-only command validation
    "is_safe_readonly_command",
    "run_readonly_shell",
    # Sandbox
    "SandboxResult",
    "DockerSandbox",
]


@dataclass
class SandboxResult:
    """Result from sandbox execution."""

    exit_code: int
    stdout: str
    stderr: str
    duration: float
    command: str
    timed_out: bool = False


class DockerSandbox:
    """Ephemeral Docker container sandbox for isolated code execution.

    Key features:
    - Ephemeral containers destroyed after each session
    - Project mounted with configurable write access
    - Network isolation option
    - Resource limits (CPU, memory)
    - stdout/stderr capture for SAGE context
    """

    # Default Docker image for Python/Node projects
    DEFAULT_IMAGE = "python:3.12-slim"

    # Alternative images for different project types
    PROJECT_IMAGES = {
        "python": "python:3.12-slim",
        "node": "node:20-slim",
        "rust": "rust:1.75-slim",
        "go": "golang:1.22-alpine",
        "java": "openjdk:21-slim",
        "ruby": "ruby:3.3-slim",
    }

    def __init__(
        self,
        cwd: Path,
        image: str | None = None,
        network_enabled: bool = False,
        memory_limit: str = "512m",
        cpu_limit: float = 1.0,
    ):
        self.cwd = cwd
        self.image = image or self._detect_project_image()
        self.network_enabled = network_enabled
        self.memory_limit = memory_limit
        self.cpu_limit = cpu_limit
        self.container_id: str | None = None
        self.session_id = str(uuid.uuid4())[:8]
        self._docker_available = self._check_docker()

        # Register cleanup on exit
        atexit.register(self.cleanup)

    def _check_docker(self) -> bool:
        """Check if Docker is available."""
        try:
            result = subprocess.run(["docker", "info"], capture_output=True, timeout=5)
            return result.returncode == 0
        except Exception:
            return False

    def _detect_project_image(self) -> str:
        """Detect the best Docker image based on project files."""
        if (self.cwd / "Cargo.toml").exists():
            return self.PROJECT_IMAGES["rust"]
        if (self.cwd / "go.mod").exists():
            return self.PROJECT_IMAGES["go"]
        if (self.cwd / "package.json").exists():
            return self.PROJECT_IMAGES["node"]
        if (self.cwd / "Gemfile").exists():
            return self.PROJECT_IMAGES["ruby"]
        if (self.cwd / "pom.xml").exists() or (self.cwd / "build.gradle").exists():
            return self.PROJECT_IMAGES["java"]
        # Default to Python
        return self.PROJECT_IMAGES["python"]

    def is_available(self) -> bool:
        """Check if sandbox is available."""
        return self._docker_available

    def start(self) -> bool:
        """Start the sandbox container."""
        if not self._docker_available:
            return False

        if self.container_id:
            return True  # Already running

        container_name = f"sage-sandbox-{self.session_id}"

        # Build docker run command
        cmd = [
            "docker",
            "run",
            "-d",  # Detached
            "--name",
            container_name,
            "-w",
            "/workspace",
            "-v",
            f"{self.cwd}:/workspace",
            "--memory",
            self.memory_limit,
            f"--cpus={self.cpu_limit}",
        ]

        # Network isolation
        if not self.network_enabled:
            cmd.extend(["--network", "none"])

        # Security options
        cmd.extend(
            [
                "--security-opt",
                "no-new-privileges",
                "--cap-drop",
                "ALL",
                "--read-only",  # Read-only root filesystem
                "--tmpfs",
                "/tmp:rw,noexec,nosuid,size=100m",  # Writable /tmp
            ]
        )

        # Image and keep-alive command
        cmd.extend([self.image, "tail", "-f", "/dev/null"])

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                self.container_id = result.stdout.strip()[:12]
                return True
            else:
                # Container might already exist, try to start it
                subprocess.run(["docker", "start", container_name], capture_output=True, timeout=30)
                id_result = subprocess.run(
                    ["docker", "ps", "-q", "-f", f"name={container_name}"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if id_result.stdout.strip():
                    self.container_id = id_result.stdout.strip()[:12]
                    return True
        except Exception as e:
            logger.debug("Failed to start sandbox container: %s", e)

        return False

    def execute(
        self,
        command: str,
        timeout: int = 120,
        env: dict[str, str] | None = None,
    ) -> SandboxResult:
        """Execute a command in the sandbox.

        Returns structured result with exit code, stdout, stderr.
        """
        start_time = time.time()

        if not self.container_id:
            if not self.start():
                return SandboxResult(
                    exit_code=-1,
                    stdout="",
                    stderr="Sandbox not available. Docker may not be installed.",
                    duration=0,
                    command=command,
                )

        # Build exec command
        cmd = ["docker", "exec"]

        # Add environment variables
        if env:
            for key, value in env.items():
                cmd.extend(["-e", f"{key}={value}"])

        cmd.extend([self.container_id, "sh", "-c", command])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            duration = time.time() - start_time

            return SandboxResult(
                exit_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                duration=duration,
                command=command,
            )
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return SandboxResult(
                exit_code=-1,
                stdout="",
                stderr=f"Command timed out after {timeout}s",
                duration=duration,
                command=command,
                timed_out=True,
            )
        except Exception as e:
            duration = time.time() - start_time
            return SandboxResult(
                exit_code=-1,
                stdout="",
                stderr=str(e),
                duration=duration,
                command=command,
            )

    def run_tests(self, test_cmd: str = "pytest -v") -> SandboxResult:
        """Run tests in the sandbox with enhanced output capture."""
        # Install dependencies first if needed
        if "pytest" in test_cmd:
            self.execute("pip install -q pytest 2>/dev/null || true", timeout=60)
        elif "npm test" in test_cmd:
            self.execute("npm install --silent 2>/dev/null || true", timeout=120)

        return self.execute(test_cmd, timeout=300)

    def verify_test_failure(
        self, test_cmd: str, expected_failure: str | None = None
    ) -> tuple[bool, str]:
        """TDD Gate: Verify that tests actually fail before implementation.

        Returns (is_failing, message).
        """
        result = self.run_tests(test_cmd)

        # Check if tests failed
        is_failing = result.exit_code != 0

        if not is_failing:
            return False, (
                "❌ TDD VIOLATION: Tests are already passing!\n"
                "You must write a FAILING test first that proves the feature is missing.\n"
                f"Output:\n{result.stdout[:1000]}"
            )

        # Check for expected failure pattern if specified
        if expected_failure:
            output = result.stdout + result.stderr
            if expected_failure.lower() not in output.lower():
                return False, (
                    f"❌ TDD VIOLATION: Tests failed, but not with the expected error.\n"
                    f"Expected: {expected_failure}\n"
                    f"Actual output:\n{output[:1000]}"
                )

        return True, result.stdout + result.stderr

    def verify_test_success(self, test_cmd: str) -> tuple[bool, str]:
        """TDD Gate: Verify that tests pass after implementation.

        Returns (is_passing, message).
        """
        result = self.run_tests(test_cmd)
        is_passing = result.exit_code == 0

        if not is_passing:
            return False, (
                "❌ TDD FAILURE: Tests are still failing after implementation!\n"
                f"Output:\n{result.stdout + result.stderr}"
            )

        return True, result.stdout + result.stderr

    def cleanup(self) -> None:
        """Stop and remove the sandbox container."""
        if self.container_id:
            try:
                # Use stop with short timeout then rm
                subprocess.run(
                    ["docker", "stop", "-t", "2", self.container_id],
                    capture_output=True,
                    timeout=10,
                )
                subprocess.run(
                    ["docker", "rm", "-f", self.container_id], capture_output=True, timeout=10
                )
            except Exception as e:
                logger.debug(f"Docker sandbox cleanup failed: {e}")
                pass
            self.container_id = None


# P0-7: Safe read-only commands that can run in analysis mode
SAFE_READONLY_COMMANDS = frozenset(
    [
        "ls",
        "cat",
        "head",
        "tail",
        "grep",
        "find",
        "wc",
        "file",
        "tree",
        "pwd",
        "which",
        "type",
        "echo",
        "less",
        "more",
        "stat",
        "du",
        "df",
        "uptime",
        "whoami",
        "id",
        "env",
        "rg",
        "fd",
        "bat",
        "exa",  # Modern CLI tools
    ]
)

# P0-7: Dangerous patterns that should never execute in read-only mode
BLOCKED_READONLY_PATTERNS = [
    r"\brm\b",
    r"\bmv\b",
    r"\bcp\b",
    r"\bchmod\b",
    r"\bchown\b",
    r"\bsudo\b",
    r"\b(pip|npm|cargo|yarn|pnpm)\s+install\b",
    r"\bgit\s+(push|commit|checkout|reset|rebase|merge)\b",
    r"\bcurl\b.*\|\s*(bash|sh)",
    r"\bwget\b.*\|\s*(bash|sh)",
    r">\s*[/~]",  # Redirect to files
    r"\beval\b",
    r"\bexec\b",
    r"\bmkdir\b",
    r"\btouch\b",
    r"\bwrite\b",
]


def is_safe_readonly_command(command: str) -> tuple[bool, str]:
    """
    Check if command is safe for read-only execution.

    P0-7: Stop executing RUN: commands with weak validation in read-only flows.

    Args:
        command: Shell command to validate

    Returns:
        Tuple of (is_safe, reason if not safe)
    """
    if not command or not command.strip():
        return False, "Empty command"

    # Check for blocked patterns first
    for pattern in BLOCKED_READONLY_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return False, f"Blocked pattern: {pattern}"

    # Extract base command
    parts = command.strip().split()
    if not parts:
        return False, "Empty command"

    base_cmd = parts[0].split("/")[-1]  # Handle /bin/ls etc

    # Must start with a safe command
    if base_cmd not in SAFE_READONLY_COMMANDS:
        return False, f"Command '{base_cmd}' not in safe read-only list"

    # Check for shell operators that could chain dangerous commands
    if any(op in command for op in [";", "&&", "||", "`", "$("]):
        return False, "Shell operators not allowed in read-only mode"

    # For piped commands, check each segment
    if "|" in command:
        segments = command.split("|")
        for seg in segments:
            seg_parts = seg.strip().split()
            if seg_parts:
                seg_cmd = seg_parts[0].split("/")[-1]
                if seg_cmd not in SAFE_READONLY_COMMANDS:
                    return False, f"Piped command '{seg_cmd}' not safe"

    return True, ""


def run_readonly_shell(cmd: str, cwd: Path, timeout: int = 30) -> str:
    """
    Run a shell command in read-only mode with strict validation.

    P0-7: Safe command execution for read-only analysis flows.

    Args:
        cmd: Shell command to run
        cwd: Current working directory
        timeout: Command timeout in seconds

    Returns:
        Command output or error message
    """
    is_safe, reason = is_safe_readonly_command(cmd)
    if not is_safe:
        return f"[blocked: {reason}]"

    return run_shell(cmd, cwd, timeout)


def extract_scoped_prefix(value: str) -> tuple[str | None, str]:
    """Extract an optional `[cwd=path]` or `[dir=path]` prefix.

    Args:
        value: String that may contain a scoped prefix

    Returns:
        Tuple of (scope_path or None, remaining_value)

    Examples:
        >>> extract_scoped_prefix("[cwd=src] pytest")
        ('src', 'pytest')
        >>> extract_scoped_prefix("pytest")
        (None, 'pytest')
    """
    match = re.match(r"^\s*\[(?:cwd|dir)=(.+?)\]\s*(.*)$", value, re.DOTALL)
    if not match:
        return None, value.strip()
    return match.group(1).strip(), match.group(2).strip()


def resolve_scoped_directory(scope: str, cwd: Path) -> tuple[Path | None, str | None]:
    """Resolve a scoped child directory under the workspace root.

    Args:
        scope: Relative or absolute path to resolve
        cwd: Current working directory (workspace root)

    Returns:
        Tuple of (resolved_path or None, error_message or None)
    """
    workspace_root = cwd.resolve()
    try:
        candidate = Path(scope)
        target = candidate.resolve() if candidate.is_absolute() else (cwd / candidate).resolve()
    except (OSError, ValueError) as exc:
        return None, f"[error: invalid scoped directory {scope!r}: {exc}]"

    if not str(target).startswith(str(workspace_root)):
        return None, f"[error: scoped directory outside workspace: {scope}]"
    if not target.exists() or not target.is_dir():
        return None, f"[error: scoped directory not found: {scope}]"
    return target, None


_UNIX_TO_WINDOWS: dict[str, str] = {
    # File/directory operations
    "ls":      "dir",
    "ls -la":  "dir /A",
    "ls -l":   "dir",
    "cat":     "type",
    "grep":    "findstr",
    "cp":      "copy",
    "mv":      "move",
    "rm":      "del",
    "rm -rf":  "rd /s /q",
    "rmdir":   "rd",
    "mkdir":   "mkdir",
    "touch":   "type nul >",
    "which":   "where",
    "echo":    "echo",
    "clear":   "cls",
    "pwd":     "cd",
    "env":     "set",
    "export":  "set",
    "chmod":   "icacls",
    "chown":   "icacls",
    # Python — always use 'py' on Windows (the launcher, always in PATH)
    "python3": "py",
    "python":  "py",
    # pip — use py -m pip so the launcher picks the right Python
    "pip3":    "py -m pip",
    "pip":     "py -m pip",
}

# Commands that should use forward slashes even on Windows
# (tools that accept them: git, npm, node, docker, gcloud, gh, python/py)
_FORWARD_SLASH_COMMANDS = {
    "git", "npm", "npx", "node", "docker", "gcloud", "gh",
    "python", "python3", "py", "pip", "pip3",
}


# Default file globs used by SAGE's SEARCH tool. Mirrors the previous
# `grep -rn --include=...` invocation so model-facing behavior stays the same.
_PORTABLE_GREP_DEFAULT_GLOBS: tuple[str, ...] = (
    "*.py", "*.js", "*.ts", "*.jsx", "*.tsx", "*.go", "*.rs", "*.java",
    "*.yaml", "*.yml", "*.json", "*.toml", "*.md",
    "Dockerfile", "requirements*.txt",
)


def portable_grep(
    pattern: str,
    cwd: Path,
    *,
    globs: tuple[str, ...] | None = None,
    files_only: bool = False,
    max_results: int = 40,
    skip_dirs: set[str] | None = None,
) -> str:
    """Run a recursive text search portably across all operating systems.

    Replaces shell pipelines like `grep -rn ... | head -N`, which require GNU
    grep + a POSIX shell and therefore don't work on Windows cmd.exe or
    PowerShell. Uses pure-Python fnmatch + iteration so the same SEARCH tool
    behaves identically on macOS, Linux, and Windows.

    Args:
        pattern: Regex (Python ``re``) to search for line-by-line.
        cwd: Directory to search recursively.
        globs: Filename glob patterns to include. None uses
            ``_PORTABLE_GREP_DEFAULT_GLOBS``.
        files_only: If True, return one line per matching file (like ``grep -l``).
            Otherwise emit ``relpath:line:content`` rows (like ``grep -rn``).
        max_results: Stop after this many output lines.
        skip_dirs: Directory names to skip during traversal. Defaults to
            ``project.SKIP_DIRS`` plus ``.sage``.

    Returns:
        Newline-joined results, or empty string if no matches.
    """
    import fnmatch

    from sage.core.project import SKIP_DIRS, safe_walk

    active_globs = globs if globs is not None else _PORTABLE_GREP_DEFAULT_GLOBS
    active_skip = (skip_dirs if skip_dirs is not None else SKIP_DIRS) | {".sage"}

    try:
        regex = re.compile(pattern)
    except re.error:
        # Fall back to literal substring matching if the pattern isn't valid regex.
        regex = re.compile(re.escape(pattern))

    def _matches_globs(name: str) -> bool:
        return any(fnmatch.fnmatch(name, g) for g in active_globs)

    out: list[str] = []
    seen_files: set[str] = set()
    for path in safe_walk(cwd, skip_dirs=active_skip, max_files=20000):
        if not _matches_globs(path.name):
            continue
        try:
            rel = path.relative_to(cwd).as_posix()
        except ValueError:
            rel = str(path)

        try:
            with path.open("r", encoding="utf-8", errors="replace") as fh:
                for line_no, line in enumerate(fh, start=1):
                    if regex.search(line):
                        if files_only:
                            if rel not in seen_files:
                                seen_files.add(rel)
                                out.append(rel)
                            break
                        out.append(f"{rel}:{line_no}:{line.rstrip()}")
                    if len(out) >= max_results:
                        break
        except (OSError, UnicodeError):
            continue
        if len(out) >= max_results:
            break

    return "\n".join(out)


def _translate_for_windows(cmd: str) -> str:
    """Translate Unix commands to Windows equivalents when running on Windows.

    Handles:
    - Command name translation (ls→dir, cat→type, python3→py, pip→py -m pip)
    - Leaves path separators alone for tools that accept forward slashes

    Only applies on Windows; no-op on macOS/Linux.
    """
    if sys.platform != "win32":
        return cmd

    stripped = cmd.strip()

    # Translate multi-word commands first (e.g. "rm -rf", "ls -la")
    for unix_cmd in sorted(_UNIX_TO_WINDOWS, key=len, reverse=True):
        if stripped == unix_cmd or stripped.startswith(unix_cmd + " "):
            win_cmd = _UNIX_TO_WINDOWS[unix_cmd]
            return win_cmd + stripped[len(unix_cmd):]

    return cmd


def run_shell(cmd: str, cwd: Path, timeout: int = 30) -> str:
    """Run a shell command and return combined stdout+stderr.

    Supports scoped directory prefixes like `[cwd=subdir] command`.
    On Windows, translates common Unix commands (ls, cat, grep…) to their
    cmd.exe equivalents so the same model output works on all platforms.

    Args:
        cmd: Shell command to run (may include [cwd=path] prefix)
        cwd: Current working directory
        timeout: Command timeout in seconds

    Returns:
        Combined stdout and stderr output, or error message
    """
    scope, inner_cmd = extract_scoped_prefix(cmd)
    scoped_cwd = cwd
    if scope:
        scoped_cwd_result, error = resolve_scoped_directory(scope, cwd)
        if error:
            return error
        assert scoped_cwd_result is not None
        scoped_cwd = scoped_cwd_result
        cmd = inner_cmd
    if not cmd.strip():
        return "[error: empty command]"

    cmd = _translate_for_windows(cmd)

    result = execute_command(
        cmd,
        cwd=scoped_cwd,
        timeout=timeout,
        allow_shell=True,
        validate=False,
    )

    return result.output


def safe_shell_exec(
    cmd: str,
    cwd: Path,
    timeout: int = 30,
    validate: bool = True,
) -> CommandResult:
    """Execute a shell command safely with full validation.

    This is the preferred API for new code. It returns a structured
    CommandResult and validates commands by default.

    Args:
        cmd: Shell command to run
        cwd: Current working directory
        timeout: Command timeout in seconds
        validate: Whether to validate against allowlists (default True)

    Returns:
        CommandResult with success status, output, and error info
    """
    scope, inner_cmd = extract_scoped_prefix(cmd)
    scoped_cwd = cwd
    if scope:
        scoped_cwd_result, error = resolve_scoped_directory(scope, cwd)
        if error:
            return CommandResult(
                success=False,
                returncode=-1,
                stdout="",
                stderr=error,
                command=cmd,
                error=error,
            )
        assert scoped_cwd_result is not None
        scoped_cwd = scoped_cwd_result
        cmd = inner_cmd

    return execute_command(
        cmd,
        cwd=scoped_cwd,
        timeout=timeout,
        allow_shell=True,  # Allow shell for backward compat
        validate=validate,
    )


def shell_quote(s: str) -> str:
    """Quote a string for safe shell use.

    Args:
        s: String to quote

    Returns:
        Single-quoted string with proper escaping
    """
    return "'" + s.replace("'", "'\\''") + "'"


def extract_bash_blocks(text: str) -> list[str]:
    """Extract ```bash or ```shell code blocks from model output.

    Args:
        text: Text containing potential code blocks

    Returns:
        List of command strings from bash/shell code blocks
    """
    blocks = []
    for m in re.finditer(r"```(?:bash|shell|sh)\s*\n(.*?)```", text, re.DOTALL):
        cmd = m.group(1).strip()
        if cmd:
            blocks.append(cmd)
    return blocks


def sanitize_shell_block(cmd: str) -> str:
    """Remove non-shell pseudo-tool directives from a shell block.

    Filters out READ:, SEARCH:, RUN:, FILE: directives and other
    non-command lines that may appear in model output.

    Args:
        cmd: Raw command block from model output

    Returns:
        Cleaned command string
    """
    cleaned: list[str] = []
    for raw in cmd.splitlines():
        line = raw.strip()
        if not line:
            continue
        if re.match(r"^(?:[-*]\s*)?(READ|SEARCH|RUN|FILE):\s*", line):
            continue
        if line.startswith("Task Understanding"):
            continue
        cleaned.append(raw)
    return "\n".join(cleaned).strip()


def strip_search_comment(pattern: str) -> str:
    """Remove trailing instructional comments from SEARCH patterns.

    Args:
        pattern: Search pattern that may have trailing comments

    Returns:
        Clean pattern without trailing # comments
    """
    return re.sub(r"\s+#.*$", "", pattern).strip()


def read_file_context(filepath: str, cwd: Path, max_lines: int = 200) -> str | None:
    """Read a file or directory and return grounded context.

    Args:
        filepath: Relative path to file
        cwd: Current working directory
        max_lines: Maximum number of lines to read

    Returns:
        Formatted file content with line numbers, directory listing, or None if not found
    """
    target = (cwd / filepath).resolve()
    if not str(target).startswith(str(cwd.resolve())):
        return None
    if not target.exists():
        return None
    if target.is_dir():
        try:
            entries = sorted(target.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
            shown = entries[:max_lines]
            display_path = filepath or "."
            lines = []
            for entry in shown:
                suffix = "/" if entry.is_dir() else ""
                lines.append(f"  {entry.name}{suffix}")
            truncated = (
                f"\n... ({len(shown)}/{len(entries)} entries shown)"
                if len(entries) > len(shown)
                else ""
            )
            return f"Directory: {display_path}\n" + "\n".join(lines) + truncated
        except Exception:
            return None
    if not target.is_file():
        return None
    try:
        full_content = target.read_text("utf-8", errors="replace")
        all_lines = full_content.splitlines()
        lines = all_lines[:max_lines]
        numbered = "\n".join(f"{i + 1:>4}| {l}" for i, l in enumerate(lines))
        truncated = (
            f"\n... ({len(lines)}/{len(all_lines)} lines shown)"
            if len(lines) == max_lines and len(all_lines) > max_lines
            else ""
        )
        return f"File: {filepath}\n{numbered}{truncated}"
    except Exception:
        return None


# =============================================================================
# TDD-Specific Shell Functions
# =============================================================================


def run_tdd_test(
    test_cmd: str, cwd: Path, timeout: int = 60, expect_failure: bool = False
) -> tuple[bool, str, str]:
    """Run a test command for TDD workflow.

    Args:
        test_cmd: Test command to run (e.g., 'pytest tests/test_foo.py -v')
        cwd: Current working directory
        timeout: Command timeout in seconds
        expect_failure: If True, success means tests failed (RED phase)

    Returns:
        Tuple of (success, message, raw_output)
        - success: True if the TDD phase requirement is met
        - message: Human-readable status message
        - raw_output: Raw command output
    """
    result = safe_shell_exec(test_cmd, cwd, timeout=timeout, validate=False)

    if not result.success and result.returncode == -1:
        # Command failed to execute (not a test failure)
        return False, f"Failed to execute test command: {result.error}", result.output

    # Check if tests passed or failed
    tests_passed = result.returncode == 0

    if expect_failure:
        # RED phase: we expect tests to fail
        if tests_passed:
            return (
                False,
                "TDD RED PHASE FAILED: Tests passed but should fail (no implementation yet)",
                result.output,
            )
        else:
            return (
                True,
                "TDD RED PHASE OK: Tests fail as expected - ready for implementation",
                result.output,
            )
    # GREEN phase: we expect tests to pass
    elif tests_passed:
        return (True, "TDD GREEN PHASE OK: All tests pass", result.output)
    else:
        return (
            False,
            "TDD GREEN PHASE FAILED: Tests still failing after implementation",
            result.output,
        )


def detect_test_framework(cwd: Path) -> str | None:
    """Detect which test framework is used in the project.

    Args:
        cwd: Project root directory

    Returns:
        Test command string or None if no framework detected
    """
    # Check for common config files
    if (cwd / "pytest.ini").exists() or (cwd / "pyproject.toml").exists():
        # Check if pytest is configured
        pyproject = cwd / "pyproject.toml"
        if pyproject.exists():
            content = pyproject.read_text(encoding="utf-8", errors="replace")
            if "pytest" in content or "[tool.pytest" in content:
                return "python -m pytest -v --tb=short"

    if (cwd / "setup.py").exists() or (cwd / "requirements.txt").exists():
        return "python -m pytest -v --tb=short"

    if (cwd / "package.json").exists():
        # Node.js project
        pkg = cwd / "package.json"
        content = pkg.read_text(encoding="utf-8", errors="replace")
        if "jest" in content:
            return "npm test"
        if "mocha" in content:
            return "npm test"

    if (cwd / "Cargo.toml").exists():
        return "cargo test"

    if (cwd / "go.mod").exists():
        return "go test ./..."

    # Default to pytest for Python-like directories
    # Use a more efficient check that avoids full tree expansion if possible
    has_py = False
    for root, dirs, files in os.walk(cwd):
        # Skip common non-source directories
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in {
            "node_modules", "__pycache__", "venv", ".venv", "dist", "build"
        }]
        if any(f.endswith(".py") for f in files):
            has_py = True
            break
            
    if has_py:
        return "python -m pytest -v --tb=short"

    return None


def parse_test_output(output: str) -> dict:
    """Parse test output to extract structured results.

    Args:
        output: Raw test command output

    Returns:
        Dict with keys: passed, failed, errors, skipped, total, failure_details,
                       collection_errors, has_collection_errors, error_messages
    """
    result = {
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "skipped": 0,
        "total": 0,
        "failure_details": [],
        "collection_errors": 0,
        "has_collection_errors": False,
        "error_messages": [],
    }

    # CRITICAL: Detect test collection errors FIRST
    # These are import errors, syntax errors, or missing modules that prevent tests from running
    collection_error_patterns = [
        r"(\d+)\s+errors?\s+during\s+collection",
        r"ERROR\s+collecting",
        r"ImportError:",
        r"ModuleNotFoundError:",
        r"SyntaxError:",
        r"collected\s+0\s+items\s*/\s*(\d+)\s+errors?",
    ]

    for pattern in collection_error_patterns:
        match = re.search(pattern, output, re.IGNORECASE)
        if match:
            result["has_collection_errors"] = True
            if match.groups():
                try:
                    result["collection_errors"] = int(match.group(1))
                except (ValueError, IndexError):
                    result["collection_errors"] = 1
            else:
                result["collection_errors"] = 1
            break

    # Extract specific error messages for context
    error_lines = re.findall(r"((?:Import|Module|Syntax|Name|Attribute)Error:[^\n]+)", output)
    result["error_messages"] = error_lines[:5]  # Keep top 5 errors

    # pytest output parsing
    pytest_summary = re.search(
        r"(\d+) passed(?:, (\d+) failed)?(?:, (\d+) error)?(?:, (\d+) skipped)?", output
    )
    if pytest_summary:
        result["passed"] = int(pytest_summary.group(1) or 0)
        result["failed"] = int(pytest_summary.group(2) or 0)
        result["errors"] = int(pytest_summary.group(3) or 0)
        result["skipped"] = int(pytest_summary.group(4) or 0)
        result["total"] = sum(
            [result["passed"], result["failed"], result["errors"], result["skipped"]]
        )

    # Also check for pytest-style failure summaries (X failed)
    failed_match = re.search(r"(\d+) failed", output)
    if failed_match:
        result["failed"] = int(failed_match.group(1))

    # Check for errors in short test summary
    error_match = re.search(r"(\d+) error", output)
    if error_match:
        result["errors"] = max(result["errors"], int(error_match.group(1)))

    # Extract failure details
    failure_blocks = re.findall(r"FAILED ([\w/]+\.py::\w+)", output)
    result["failure_details"] = failure_blocks

    # Add backwards-compatible aliases for simple schema consumers
    # This allows code that expects total_passed/total_failed/is_success to work
    result["total_passed"] = result["passed"]
    result["total_failed"] = result["failed"]
    result["is_success"] = (
        result["passed"] > 0
        and result["failed"] == 0
        and result["errors"] == 0
        and not result["has_collection_errors"]
    )

    return result


def has_test_errors(output: str) -> bool:
    """Check if test output indicates any errors (collection or test failures).

    Args:
        output: Raw test command output

    Returns:
        True if there are any errors that need fixing
    """
    parsed = parse_test_output(output)
    return parsed["has_collection_errors"] or parsed["failed"] > 0 or parsed["errors"] > 0


def get_test_error_summary(output: str) -> str:
    """Get a human-readable summary of test errors.

    Args:
        output: Raw test command output

    Returns:
        Summary string describing the errors
    """
    parsed = parse_test_output(output)

    if parsed["has_collection_errors"]:
        error_count = parsed["collection_errors"]
        error_msgs = "\n".join(parsed["error_messages"]) if parsed["error_messages"] else ""
        return (
            f"❌ TEST COLLECTION FAILED: {error_count} error(s) during collection\n"
            f"Tests cannot run until these import/syntax errors are fixed:\n{error_msgs}"
        )

    if parsed["failed"] > 0 or parsed["errors"] > 0:
        return (
            f"❌ TEST FAILURES: {parsed['failed']} failed, {parsed['errors']} errors, "
            f"{parsed['passed']} passed"
        )

    if parsed["passed"] > 0:
        return f"✅ ALL TESTS PASSED: {parsed['passed']} passed"

    return "⚠️ No tests were run"


# Backward compatibility aliases (prefixed versions for main.py)
_extract_scoped_prefix = extract_scoped_prefix
_resolve_scoped_directory = resolve_scoped_directory
_run_shell = run_shell
_safe_shell_exec = safe_shell_exec
_shell_quote = shell_quote
_extract_bash_blocks = extract_bash_blocks
_sanitize_shell_block = sanitize_shell_block
_strip_search_comment = strip_search_comment
_read_file_context = read_file_context
_run_tdd_test = run_tdd_test
_detect_test_framework = detect_test_framework
_parse_test_output = parse_test_output
_has_test_errors = has_test_errors
_get_test_error_summary = get_test_error_summary
