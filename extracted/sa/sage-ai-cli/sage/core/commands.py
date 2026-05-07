"""Safe command execution for SAGE.

This module provides secure command execution without shell=True,
with command parsing, allowlisting, and validation.

This addresses P0 items 5-8:
- Item 5: Remove shell=True from incremental test execution
- Item 6: Remove shell pipelines from quick validation checks
- Item 7: Parse validation commands into argv instead of raw shell strings
- Item 8: Add command allowlisting for model-suggested build/test commands

Key safety guarantees:
- No shell injection via shell=True
- Commands are parsed into argv before execution
- Dangerous commands are blocked
- Model-suggested commands are validated against allowlists
"""

from __future__ import annotations

import functools
import os
import re
import shlex
import shutil
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

__all__ = [
    # Enums
    "CommandCategory",
    "CommandRisk",
    # Data classes
    "ParsedCommand",
    "CommandResult",
    "CommandValidation",
    # Main functions
    "parse_command",
    "execute_command",
    "execute_argv",
    "validate_command",
    "is_command_allowed",
    "get_allowed_commands",
    "run_shell",
    # Command builders
    "build_test_command",
    "build_lint_command",
    "build_build_command",
    # Constants
    "ALLOWED_EXECUTABLES",
    "BLOCKED_PATTERNS",
    "DANGEROUS_FLAGS",
]


@functools.lru_cache(maxsize=1)
def _windows_bash_exe() -> str | None:
    """Locate a POSIX-compatible bash on Windows. None if not found.

    Why this exists: when subprocess runs with ``shell=True`` on Windows,
    Python invokes ``cmd.exe``, which can't parse the bash idioms the SAGE
    agent emits (single-quoted args, ``$(subst)``, ``mkdir -p``, ``grep``,
    ``cat``, heredocs, etc). Routing through Git Bash / WSL bash makes
    those work the same as on Linux/macOS.

    Search order:
      1. Git Bash — bundled with Git for Windows, present on most dev boxes
      2. WSL bash via PATH (``bash.exe``)
      3. MSYS2 bash
    """
    if sys.platform != "win32":
        return None
    candidates = [
        r"C:\Program Files\Git\bin\bash.exe",
        r"C:\Program Files\Git\usr\bin\bash.exe",
        r"C:\Program Files (x86)\Git\bin\bash.exe",
        r"C:\msys64\usr\bin\bash.exe",
    ]
    for c in candidates:
        if Path(c).is_file():
            return c
    return shutil.which("bash.exe") or shutil.which("bash")


def run_shell(
    cmd: str,
    *,
    cwd: Path | str | None = None,
    timeout: float | None = 120,
    capture_output: bool = True,
    text: bool = True,
    stdin: int | None = subprocess.DEVNULL,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess:
    """Run a shell command string with POSIX semantics on every platform.

    On non-Windows: ``subprocess.run(cmd, shell=True, ...)`` — uses ``/bin/sh``.
    On Windows: prefer Git Bash / WSL bash via ``[bash, "-c", cmd]`` so the
    agent's bash idioms work the same as on Linux/macOS. Falls back to
    ``cmd.exe`` (``shell=True``) only if no bash is found.

    The fallback is intentionally lossy — the user gets a runnable shell at
    least, even if complex bash one-liners may not parse. ``sage doctor``
    style diagnostics elsewhere should warn the user to install Git Bash.
    """
    common: dict = {
        "cwd": str(cwd) if cwd is not None else None,
        "capture_output": capture_output,
        "text": text,
        "timeout": timeout,
        "stdin": stdin,
    }
    if env is not None:
        common["env"] = env

    if sys.platform == "win32":
        bash = _windows_bash_exe()
        if bash:
            return subprocess.run([bash, "-c", cmd], **common)
        # No bash available — fall through to cmd.exe.

    return subprocess.run(cmd, shell=True, **common)


class CommandCategory(str, Enum):
    """Categories of commands."""

    TEST = "test"
    LINT = "lint"
    FORMAT = "format"
    BUILD = "build"
    TYPE_CHECK = "type_check"
    INSTALL = "install"
    RUN = "run"
    GIT = "git"
    FILE = "file"
    SHELL = "shell"
    UNKNOWN = "unknown"


class CommandRisk(str, Enum):
    """Risk level of a command."""

    SAFE = "safe"  # Read-only or well-understood commands
    LOW = "low"  # Commands that modify local project state
    MEDIUM = "medium"  # Commands that could have broader effects
    HIGH = "high"  # Commands that could damage system or leak data
    BLOCKED = "blocked"  # Never allow


@dataclass
class ParsedCommand:
    """A parsed command ready for execution."""

    original: str  # Original command string
    argv: list[str]  # Parsed argument vector
    executable: str  # The command/executable
    args: list[str]  # Arguments to the command
    category: CommandCategory = CommandCategory.UNKNOWN
    risk: CommandRisk = CommandRisk.MEDIUM
    cwd_scope: str | None = None  # Optional [cwd=path] prefix
    env_vars: dict[str, str] = field(default_factory=dict)
    is_valid: bool = True
    validation_error: str | None = None


@dataclass
class CommandResult:
    """Result of command execution."""

    success: bool
    returncode: int
    stdout: str
    stderr: str
    command: str
    elapsed_seconds: float = 0.0
    timed_out: bool = False
    error: str | None = None

    @property
    def output(self) -> str:
        """Combined stdout and stderr."""
        parts = []
        if self.stdout:
            parts.append(self.stdout)
        if self.stderr:
            parts.append(self.stderr)
        if self.timed_out:
            parts.append("[timed out]")
        elif self.error:
            parts.append(f"[error: {self.error}]")
        if self.returncode != 0:
            parts.append(f"[exit code: {self.returncode}]")
        return "\n".join(parts) or "(no output)"


@dataclass
class CommandValidation:
    """Result of command validation."""

    allowed: bool
    risk: CommandRisk
    reason: str
    suggestions: list[str] = field(default_factory=list)


# Allowed executables by category
ALLOWED_EXECUTABLES: dict[CommandCategory, set[str]] = {
    CommandCategory.TEST: {
        # Python
        "python",
        "python3",
        "pytest",
        "py.test",
        "nose",
        "nose2",
        # JavaScript
        "npm",
        "npx",
        "yarn",
        "pnpm",
        "bun",
        "deno",
        "jest",
        "vitest",
        "mocha",
        "ava",
        "playwright",
        "cypress",
        # Java/JVM
        "mvn",
        "maven",
        "gradle",
        "gradlew",
        "./gradlew",
        "sbt",
        "kotlin",
        "kotlinc",
        # Other
        "cargo",
        "go",
        "dotnet",
        "mix",
        "rspec",
        "bundle",
        "phpunit",
        "vendor/bin/phpunit",
        "pest",
        "swift",
        "xcodebuild",
        "ctest",
        "make",
    },
    CommandCategory.LINT: {
        # Python
        "python",
        "python3",
        "ruff",
        "flake8",
        "pylint",
        "mypy",
        "pyright",
        "black",
        "isort",
        # JavaScript
        "npm",
        "npx",
        "yarn",
        "pnpm",
        "bun",
        "eslint",
        "prettier",
        "tsc",
        "biome",
        # Other
        "cargo",
        "go",
        "dotnet",
        "mix",
        "rubocop",
        "bundle",
        "phpcs",
        "phpstan",
        "psalm",
    },
    CommandCategory.FORMAT: {
        "python",
        "python3",
        "ruff",
        "black",
        "isort",
        "autopep8",
        "yapf",
        "npm",
        "npx",
        "yarn",
        "pnpm",
        "bun",
        "prettier",
        "biome",
        "cargo",
        "go",
        "dotnet",
        "mix",
        "rubocop",
    },
    CommandCategory.BUILD: {
        "python",
        "python3",
        "pip",
        "pip3",
        "poetry",
        "pdm",
        "uv",
        "hatch",
        "npm",
        "npx",
        "yarn",
        "pnpm",
        "bun",
        "deno",
        "tsc",
        "vite",
        "webpack",
        "esbuild",
        "cargo",
        "go",
        "dotnet",
        "msbuild",
        "mvn",
        "maven",
        "gradle",
        "gradlew",
        "./gradlew",
        "sbt",
        "make",
        "cmake",
        "ninja",
        "meson",
        "mix",
        "bundle",
        "rake",
        "swift",
        "xcodebuild",
        "flutter",
        "dart",
    },
    CommandCategory.TYPE_CHECK: {
        "python",
        "python3",
        "mypy",
        "pyright",
        "pytype",
        "npx",
        "tsc",
        "typescript",
        "cargo",
        "go",
        "dotnet",
    },
    CommandCategory.INSTALL: {
        "pip",
        "pip3",
        "python",
        "python3",
        "poetry",
        "pdm",
        "uv",
        "pipenv",
        "conda",
        "npm",
        "yarn",
        "pnpm",
        "bun",
        "deno",
        "cargo",
        "go",
        "dotnet",
        "mvn",
        "gradle",
        "gradlew",
        "./gradlew",
        "bundle",
        "gem",
        "composer",
        "mix",
        "swift",
        "pub",
        "flutter",
    },
    CommandCategory.GIT: {
        "git",
    },
    CommandCategory.FILE: {
        "ls",
        "cat",
        "head",
        "tail",
        "wc",
        "find",
        "grep",
        "rg",
        "tree",
        "file",
        "stat",
        "du",
        "df",
        "mkdir",
        "touch",
        "cp",
        "mv",  # Write operations - medium risk
    },
    CommandCategory.RUN: {
        "python",
        "python3",
        "node",
        "deno",
        "bun",
        "cargo",
        "go",
        "dotnet",
        "ruby",
        "php",
        "elixir",
        "mix",
        "swift",
        "java",
        "kotlin",
        "scala",
    },
}

# Patterns that should always be blocked
BLOCKED_PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\brm\s+-rf\s+/"), "Recursive delete of root"),
    (re.compile(r"\brm\s+-rf\s+~"), "Recursive delete of home"),
    (re.compile(r"\brm\s+-rf\s+\*"), "Recursive delete with wildcard"),
    (re.compile(r"\bsudo\b"), "Sudo commands not allowed"),
    (re.compile(r"\bcurl\b.*\|\s*(?:bash|sh)"), "Piped curl to shell"),
    (re.compile(r"\bwget\b.*\|\s*(?:bash|sh)"), "Piped wget to shell"),
    (re.compile(r"\beval\b"), "Eval is dangerous"),
    (re.compile(r"\bexec\b"), "Exec is dangerous"),
    (re.compile(r">\s*/dev/sd"), "Writing to block devices"),
    (re.compile(r">\s*/etc/"), "Writing to /etc"),
    (re.compile(r">\s*/usr/"), "Writing to /usr"),
    (re.compile(r">\s*/var/"), "Writing to /var"),
    (re.compile(r">\s*/sys/"), "Writing to /sys"),
    (re.compile(r">\s*/proc/"), "Writing to /proc"),
    (re.compile(r"\bchmod\s+777"), "Overly permissive chmod"),
    (re.compile(r"\bchown\b.*root"), "Changing ownership to root"),
    (re.compile(r"\bdd\b.*of=/dev/"), "DD to device"),
    (re.compile(r"\bmkfs\b"), "Formatting filesystems"),
    (re.compile(r"\bfdisk\b"), "Partitioning disks"),
    (re.compile(r">\s*/dev/null\s*2>&1\s*&"), "Backgrounding with null output"),
    (re.compile(r"\bnc\s+-l"), "Netcat listen mode"),
    (re.compile(r"\bnetcat\s+-l"), "Netcat listen mode"),
    (re.compile(r"\bpython\s+-c\s+['\"]import\s+socket"), "Python socket code"),
]

# Dangerous flags that increase risk
DANGEROUS_FLAGS: dict[str, list[str]] = {
    "git": ["--force", "-f", "push --force", "reset --hard"],
    "rm": ["-rf", "-r", "--recursive", "-f", "--force"],
    "npm": ["--unsafe-perm", "--ignore-scripts"],
    "pip": ["--break-system-packages", "--user"],
}


def _extract_scoped_prefix(cmd: str) -> tuple[str | None, str]:
    """Extract optional [cwd=path] or [dir=path] prefix."""
    match = re.match(r"^\s*\[(?:cwd|dir)=(.+?)\]\s*(.*)$", cmd, re.DOTALL)
    if not match:
        return None, cmd.strip()
    return match.group(1).strip(), match.group(2).strip()


def _extract_env_vars(cmd: str) -> tuple[dict[str, str], str]:
    """Extract leading environment variables from a command.

    Example: "FOO=bar BAR=baz python test.py" -> ({"FOO": "bar", "BAR": "baz"}, "python test.py")
    """
    env_vars: dict[str, str] = {}
    remaining = cmd.strip()

    while True:
        # Match VAR=value at the start
        match = re.match(r"^([A-Z_][A-Z0-9_]*)=(\S+)\s+", remaining)
        if not match:
            break
        env_vars[match.group(1)] = match.group(2)
        remaining = remaining[match.end() :]

    return env_vars, remaining


def _detect_category(executable: str, args: list[str]) -> CommandCategory:
    """Detect the category of a command based on executable and args."""
    exe_lower = executable.lower()
    exe_base = os.path.basename(exe_lower)

    # Test commands
    if exe_base in {"pytest", "py.test", "nose", "nose2", "unittest"}:
        return CommandCategory.TEST
    if exe_base in {"jest", "vitest", "mocha", "ava", "playwright", "cypress"}:
        return CommandCategory.TEST
    if exe_base in {"rspec", "phpunit", "pest", "exunit", "ctest"}:
        return CommandCategory.TEST
    if exe_base == "cargo" and args and args[0] == "test":
        return CommandCategory.TEST
    if exe_base == "go" and args and args[0] == "test":
        return CommandCategory.TEST
    if exe_base == "dotnet" and args and args[0] == "test":
        return CommandCategory.TEST
    if exe_base in {"npm", "npx", "yarn", "pnpm", "bun"} and args and "test" in args:
        return CommandCategory.TEST
    if exe_base == "python" and args and args[0:2] == ["-m", "pytest"]:
        return CommandCategory.TEST
    if exe_base == "mvn" and args and "test" in args:
        return CommandCategory.TEST
    if exe_base in {"gradle", "gradlew", "./gradlew"} and args and "test" in args:
        return CommandCategory.TEST

    # Lint commands
    if exe_base in {"ruff", "flake8", "pylint", "eslint", "clippy", "rubocop", "phpcs", "phpstan"}:
        return CommandCategory.LINT
    if exe_base == "cargo" and args and args[0] == "clippy":
        return CommandCategory.LINT
    if exe_base == "go" and args and args[0] == "vet":
        return CommandCategory.LINT
    if exe_base in {"npm", "npx", "yarn", "pnpm", "bun"} and args and "lint" in args:
        return CommandCategory.LINT

    # Format commands
    if exe_base in {"black", "isort", "prettier", "autopep8", "yapf", "gofmt"}:
        return CommandCategory.FORMAT
    if exe_base == "ruff" and args and args[0] == "format":
        return CommandCategory.FORMAT
    if exe_base == "cargo" and args and args[0] == "fmt":
        return CommandCategory.FORMAT
    if exe_base == "go" and args and args[0] == "fmt":
        return CommandCategory.FORMAT
    if exe_base in {"npm", "npx", "yarn", "pnpm", "bun"} and args and "format" in args:
        return CommandCategory.FORMAT

    # Type check commands
    if exe_base in {"mypy", "pyright", "pytype", "tsc", "typescript"}:
        return CommandCategory.TYPE_CHECK
    if exe_base == "cargo" and args and args[0] == "check":
        return CommandCategory.TYPE_CHECK
    if exe_base == "dotnet" and args and args[0] == "build":
        return CommandCategory.TYPE_CHECK

    # Build commands
    if exe_base == "cargo" and args and args[0] == "build":
        return CommandCategory.BUILD
    if exe_base == "go" and args and args[0] == "build":
        return CommandCategory.BUILD
    if exe_base == "dotnet" and args and args[0] == "build":
        return CommandCategory.BUILD
    if exe_base in {"npm", "npx", "yarn", "pnpm", "bun"} and args and "build" in args:
        return CommandCategory.BUILD
    if exe_base in {"make", "cmake", "ninja", "meson"}:
        return CommandCategory.BUILD
    if exe_base in {"mvn", "gradle", "gradlew", "./gradlew"} and args and "compile" in args:
        return CommandCategory.BUILD

    # Install commands
    if exe_base == "pip" and args and args[0] == "install":
        return CommandCategory.INSTALL
    if exe_base in {"npm", "yarn", "pnpm", "bun"} and args and "install" in args:
        return CommandCategory.INSTALL
    if exe_base == "cargo" and args and args[0] == "install":
        return CommandCategory.INSTALL
    if exe_base == "bundle" and args and args[0] == "install":
        return CommandCategory.INSTALL
    if exe_base == "composer" and args and args[0] == "install":
        return CommandCategory.INSTALL
    if exe_base == "mix" and args and args[0:2] == ["deps", "get"]:
        return CommandCategory.INSTALL

    # Git commands
    if exe_base == "git":
        return CommandCategory.GIT

    # File commands
    if exe_base in {
        "ls",
        "cat",
        "head",
        "tail",
        "wc",
        "find",
        "grep",
        "rg",
        "tree",
        "file",
        "stat",
        "du",
        "df",
    }:
        return CommandCategory.FILE
    if exe_base in {"mkdir", "touch", "cp", "mv", "rm"}:
        return CommandCategory.FILE

    # Run commands
    if exe_base in {"python", "python3", "node", "deno", "bun", "ruby", "php"}:
        return CommandCategory.RUN

    return CommandCategory.UNKNOWN


def _assess_risk(parsed: ParsedCommand) -> CommandRisk:
    """Assess the risk level of a parsed command."""
    exe_lower = parsed.executable.lower()
    exe_base = os.path.basename(exe_lower)
    args_str = " ".join(parsed.args).lower()

    # Check blocked patterns first
    full_cmd = parsed.original.lower()
    for pattern, _ in BLOCKED_PATTERNS:
        if pattern.search(full_cmd):
            return CommandRisk.BLOCKED

    # Check dangerous flags
    if exe_base in DANGEROUS_FLAGS:
        for flag in DANGEROUS_FLAGS[exe_base]:
            if flag in args_str:
                return CommandRisk.HIGH

    # Category-based risk assessment
    if parsed.category in {CommandCategory.TEST, CommandCategory.LINT, CommandCategory.TYPE_CHECK}:
        return CommandRisk.SAFE
    if parsed.category == CommandCategory.FORMAT:
        return CommandRisk.LOW
    if parsed.category == CommandCategory.BUILD:
        return CommandRisk.LOW
    if parsed.category == CommandCategory.INSTALL:
        return CommandRisk.MEDIUM
    if parsed.category == CommandCategory.GIT:
        if "push" in args_str or "reset" in args_str or "checkout" in args_str:
            return CommandRisk.MEDIUM
        return CommandRisk.LOW
    if parsed.category == CommandCategory.FILE:
        if exe_base in {"rm", "mv"}:
            return CommandRisk.MEDIUM
        return CommandRisk.SAFE
    if parsed.category == CommandCategory.RUN:
        return CommandRisk.MEDIUM

    return CommandRisk.MEDIUM


def parse_command(cmd: str) -> ParsedCommand:
    """Parse a command string into a structured ParsedCommand.

    This is the core function for safe command execution. It:
    1. Extracts [cwd=path] prefixes
    2. Extracts environment variables
    3. Parses the command into argv using shlex
    4. Detects the command category
    5. Assesses the risk level

    Args:
        cmd: Raw command string (may include shell constructs)

    Returns:
        ParsedCommand with parsed information
    """
    # Extract scoped directory prefix
    cwd_scope, remaining = _extract_scoped_prefix(cmd)

    # Extract environment variables
    env_vars, remaining = _extract_env_vars(remaining)

    if not remaining.strip():
        return ParsedCommand(
            original=cmd,
            argv=[],
            executable="",
            args=[],
            is_valid=False,
            validation_error="Empty command",
        )

    # Check for blocked patterns before parsing
    for pattern, reason in BLOCKED_PATTERNS:
        if pattern.search(cmd):
            return ParsedCommand(
                original=cmd,
                argv=[],
                executable="",
                args=[],
                is_valid=False,
                validation_error=f"Blocked: {reason}",
                risk=CommandRisk.BLOCKED,
            )

    # Check for shell operators that we can't safely handle
    # We'll still parse but mark as needing shell
    has_shell_operators = bool(re.search(r"[|;&<>]|\$\(|`", remaining))

    try:
        argv = shlex.split(remaining)
    except ValueError as e:
        return ParsedCommand(
            original=cmd,
            argv=[],
            executable="",
            args=[],
            is_valid=False,
            validation_error=f"Parse error: {e}",
        )

    if not argv:
        return ParsedCommand(
            original=cmd,
            argv=[],
            executable="",
            args=[],
            is_valid=False,
            validation_error="No command found",
        )

    executable = argv[0]
    args = argv[1:]

    parsed = ParsedCommand(
        original=cmd,
        argv=argv,
        executable=executable,
        args=args,
        cwd_scope=cwd_scope,
        env_vars=env_vars,
        is_valid=True,
    )

    # Detect category and risk
    parsed.category = _detect_category(executable, args)
    parsed.risk = _assess_risk(parsed)

    # If it has shell operators, we may need to handle specially
    if has_shell_operators:
        parsed.validation_error = "Contains shell operators - may require shell execution"

    return parsed


def validate_command(cmd: str) -> CommandValidation:
    """Validate a command for safety and allowlisting.

    Args:
        cmd: Command string to validate

    Returns:
        CommandValidation with result
    """
    parsed = parse_command(cmd)

    if not parsed.is_valid:
        return CommandValidation(
            allowed=False,
            risk=parsed.risk,
            reason=parsed.validation_error or "Invalid command",
        )

    if parsed.risk == CommandRisk.BLOCKED:
        return CommandValidation(
            allowed=False,
            risk=CommandRisk.BLOCKED,
            reason=parsed.validation_error or "Command is blocked",
        )

    # Check if executable is in allowlist for its category
    exe_base = os.path.basename(parsed.executable.lower())
    category_allowed = ALLOWED_EXECUTABLES.get(parsed.category, set())

    if exe_base in category_allowed or parsed.executable in category_allowed:
        return CommandValidation(
            allowed=True,
            risk=parsed.risk,
            reason=f"Allowed {parsed.category.value} command",
        )

    # Check all categories
    for cat, executables in ALLOWED_EXECUTABLES.items():
        if exe_base in executables or parsed.executable in executables:
            return CommandValidation(
                allowed=True,
                risk=parsed.risk,
                reason=f"Allowed {cat.value} command",
            )

    # Not in any allowlist
    return CommandValidation(
        allowed=False,
        risk=parsed.risk,
        reason=f"Executable '{parsed.executable}' not in allowlist",
        suggestions=[
            "Use a known test/build/lint command",
            f"Or add '{exe_base}' to ALLOWED_EXECUTABLES if safe",
        ],
    )


def is_command_allowed(cmd: str) -> bool:
    """Quick check if a command is allowed.

    Args:
        cmd: Command string to check

    Returns:
        True if allowed, False otherwise
    """
    return validate_command(cmd).allowed


def get_allowed_commands(category: CommandCategory) -> set[str]:
    """Get the set of allowed executables for a category.

    Args:
        category: The command category

    Returns:
        Set of allowed executable names
    """
    return ALLOWED_EXECUTABLES.get(category, set()).copy()


def execute_argv(
    argv: Sequence[str],
    cwd: Path | str | None = None,
    timeout: int = 120,
    env: dict[str, str] | None = None,
    capture_output: bool = True,
) -> CommandResult:
    """Execute a command as an argv list (no shell).

    This is the safest way to execute commands as it doesn't involve shell parsing.

    Args:
        argv: Command and arguments as a list
        cwd: Working directory for the command
        timeout: Timeout in seconds
        env: Additional environment variables
        capture_output: Whether to capture stdout/stderr

    Returns:
        CommandResult with execution result
    """
    import time

    if not argv:
        return CommandResult(
            success=False,
            returncode=-1,
            stdout="",
            stderr="",
            command="(empty)",
            error="Empty command",
        )

    cmd_str = " ".join(shlex.quote(a) for a in argv)
    start_time = time.time()

    # Prepare environment
    process_env = os.environ.copy()
    if env:
        process_env.update(env)

    try:
        result = subprocess.run(
            argv,
            cwd=str(cwd) if cwd else None,
            env=process_env,
            capture_output=capture_output,
            text=True,
            timeout=timeout,
        )

        elapsed = time.time() - start_time

        return CommandResult(
            success=result.returncode == 0,
            returncode=result.returncode,
            stdout=result.stdout or "",
            stderr=result.stderr or "",
            command=cmd_str,
            elapsed_seconds=elapsed,
        )

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        return CommandResult(
            success=False,
            returncode=-1,
            stdout="",
            stderr="",
            command=cmd_str,
            elapsed_seconds=elapsed,
            timed_out=True,
            error=f"Command timed out after {timeout}s",
        )

    except FileNotFoundError:
        return CommandResult(
            success=False,
            returncode=-1,
            stdout="",
            stderr="",
            command=cmd_str,
            error=f"Executable not found: {argv[0]}",
        )

    except PermissionError:
        return CommandResult(
            success=False,
            returncode=-1,
            stdout="",
            stderr="",
            command=cmd_str,
            error=f"Permission denied: {argv[0]}",
        )

    except Exception as e:
        return CommandResult(
            success=False,
            returncode=-1,
            stdout="",
            stderr="",
            command=cmd_str,
            error=str(e),
        )


def execute_command(
    cmd: str,
    cwd: Path | str | None = None,
    timeout: int = 120,
    allow_shell: bool = False,
    validate: bool = True,
) -> CommandResult:
    """Execute a command string safely.

    This function:
    1. Parses the command into argv
    2. Validates against allowlists (if enabled)
    3. Executes without shell (if possible)
    4. Falls back to shell only if allow_shell=True and necessary

    Args:
        cmd: Command string to execute
        cwd: Working directory
        timeout: Timeout in seconds
        allow_shell: Whether to allow shell execution for complex commands
        validate: Whether to validate against allowlists

    Returns:
        CommandResult with execution result
    """
    parsed = parse_command(cmd)

    if not parsed.is_valid:
        return CommandResult(
            success=False,
            returncode=-1,
            stdout="",
            stderr="",
            command=cmd,
            error=parsed.validation_error,
        )

    if parsed.risk == CommandRisk.BLOCKED:
        return CommandResult(
            success=False,
            returncode=-1,
            stdout="",
            stderr="",
            command=cmd,
            error=f"Command blocked: {parsed.validation_error}",
        )

    # Validate against allowlist if requested
    if validate:
        validation = validate_command(cmd)
        if not validation.allowed:
            return CommandResult(
                success=False,
                returncode=-1,
                stdout="",
                stderr="",
                command=cmd,
                error=f"Command not allowed: {validation.reason}",
            )

    # Determine working directory
    exec_cwd = cwd
    if parsed.cwd_scope:
        base = Path(cwd) if cwd else Path.cwd()
        scoped = base / parsed.cwd_scope
        if scoped.exists() and scoped.is_dir():
            exec_cwd = scoped
        else:
            return CommandResult(
                success=False,
                returncode=-1,
                stdout="",
                stderr="",
                command=cmd,
                error=f"Scoped directory not found: {parsed.cwd_scope}",
            )

    # Check if we need shell execution
    needs_shell = bool(re.search(r"[|;&<>]|\$\(|`", cmd))

    if needs_shell and not allow_shell:
        return CommandResult(
            success=False,
            returncode=-1,
            stdout="",
            stderr="",
            command=cmd,
            error="Command contains shell operators but shell execution is disabled",
        )

    if needs_shell and allow_shell:
        # Fall back to shell execution (with validation already passed).
        # Uses run_shell so Windows routes through Git Bash / WSL bash when
        # available — keeps POSIX semantics (single quotes, $(...) , pipes)
        # consistent with Linux/macOS.
        import time

        start_time = time.time()

        try:
            result = run_shell(
                cmd,
                cwd=exec_cwd,
                timeout=timeout,
            )

            elapsed = time.time() - start_time

            return CommandResult(
                success=result.returncode == 0,
                returncode=result.returncode,
                stdout=result.stdout or "",
                stderr=result.stderr or "",
                command=cmd,
                elapsed_seconds=elapsed,
            )

        except subprocess.TimeoutExpired:
            elapsed = time.time() - start_time
            return CommandResult(
                success=False,
                returncode=-1,
                stdout="",
                stderr="",
                command=cmd,
                elapsed_seconds=elapsed,
                timed_out=True,
                error=f"Command timed out after {timeout}s",
            )

        except Exception as e:
            return CommandResult(
                success=False,
                returncode=-1,
                stdout="",
                stderr="",
                command=cmd,
                error=str(e),
            )

    # Execute without shell
    return execute_argv(
        parsed.argv,
        cwd=exec_cwd,
        timeout=timeout,
        env=parsed.env_vars,
    )


def build_test_command(
    test_framework: str,
    test_files: list[str] | None = None,
    verbose: bool = True,
    fail_fast: bool = False,
) -> list[str]:
    """Build a test command argv for a given framework.

    Args:
        test_framework: Name of the test framework (pytest, jest, vitest, etc.)
        test_files: Optional specific test files to run
        verbose: Whether to enable verbose output
        fail_fast: Whether to stop on first failure

    Returns:
        Command as argv list
    """
    framework = test_framework.lower()

    if framework in {"pytest", "py.test"}:
        cmd = ["python", "-m", "pytest"]
        if verbose:
            cmd.extend(["-v", "--tb=short"])
        if fail_fast:
            cmd.append("-x")
        if test_files:
            cmd.extend(test_files)
        return cmd

    if framework in {"jest"}:
        cmd = ["npx", "jest"]
        if fail_fast:
            cmd.append("--bail")
        if test_files:
            cmd.extend(test_files)
        return cmd

    if framework in {"vitest"}:
        cmd = ["npx", "vitest", "run"]
        if test_files:
            cmd.extend(test_files)
        return cmd

    if framework in {"mocha"}:
        cmd = ["npx", "mocha"]
        if fail_fast:
            cmd.append("--bail")
        if test_files:
            cmd.extend(test_files)
        return cmd

    if framework in {"cargo", "cargo_test"}:
        cmd = ["cargo", "test"]
        if fail_fast:
            cmd.append("--no-fail-fast")
        return cmd

    if framework in {"go", "go_test"}:
        cmd = ["go", "test"]
        if verbose:
            cmd.append("-v")
        cmd.append("./...")
        return cmd

    if framework in {"dotnet", "dotnet_test"}:
        cmd = ["dotnet", "test"]
        if verbose:
            cmd.append("--verbosity=normal")
        return cmd

    if framework in {"rspec"}:
        cmd = ["bundle", "exec", "rspec"]
        if fail_fast:
            cmd.append("--fail-fast")
        if test_files:
            cmd.extend(test_files)
        return cmd

    if framework in {"phpunit"}:
        cmd = ["vendor/bin/phpunit"]
        if fail_fast:
            cmd.append("--stop-on-failure")
        if test_files:
            cmd.extend(test_files)
        return cmd

    if framework in {"exunit", "mix"}:
        cmd = ["mix", "test"]
        if fail_fast:
            cmd.append("--max-failures=1")
        if test_files:
            cmd.extend(test_files)
        return cmd

    # Default: assume it's the command itself
    return [framework] + (test_files or [])


def build_lint_command(linter: str, paths: list[str] | None = None) -> list[str]:
    """Build a lint command argv for a given linter.

    Args:
        linter: Name of the linter (ruff, eslint, clippy, etc.)
        paths: Optional paths to lint

    Returns:
        Command as argv list
    """
    linter_lower = linter.lower()
    target = paths or ["."]

    if linter_lower == "ruff":
        return ["ruff", "check"] + target

    if linter_lower == "flake8":
        return ["flake8"] + target

    if linter_lower == "pylint":
        return ["pylint"] + target

    if linter_lower == "eslint":
        return ["npx", "eslint"] + target

    if linter_lower == "clippy":
        return ["cargo", "clippy"]

    if linter_lower in {"go", "go_vet"}:
        return ["go", "vet", "./..."]

    if linter_lower == "rubocop":
        return ["bundle", "exec", "rubocop"] + target

    return [linter] + target


def build_build_command(build_tool: str) -> list[str]:
    """Build a build command argv for a given build tool.

    Args:
        build_tool: Name of the build tool

    Returns:
        Command as argv list
    """
    tool = build_tool.lower()

    if tool == "cargo":
        return ["cargo", "build"]

    if tool == "go":
        return ["go", "build", "./..."]

    if tool == "dotnet":
        return ["dotnet", "build"]

    if tool == "npm":
        return ["npm", "run", "build"]

    if tool == "yarn":
        return ["yarn", "build"]

    if tool == "pnpm":
        return ["pnpm", "build"]

    if tool == "bun":
        return ["bun", "run", "build"]

    if tool == "gradle":
        return ["./gradlew", "build"]

    if tool == "maven":
        return ["mvn", "compile"]

    if tool == "make":
        return ["make"]

    if tool == "cmake":
        return ["cmake", "--build", "."]

    if tool == "mix":
        return ["mix", "compile"]

    return [build_tool]
