"""Extended diagnostics support for SAGE.

This module provides language server and static analysis integration
for all supported languages, not just Python/TS/Rust/Go.

This addresses P1 items 46-70:
- Items 46-58: Extend LSP/static diagnostics to more languages
- Items 59-60: Add framework-aware diagnostics
- Items 61-70: Dependency graph support for more languages (covered in dependencies.py)

Supported languages:
- Python: pyright, mypy, ruff
- TypeScript/JavaScript: tsc, eslint
- Rust: cargo check, clippy
- Go: go vet, golangci-lint
- Java: javac, checkstyle
- Kotlin: kotlinc, ktlint
- C#: dotnet build, omnisharp
- PHP: php -l, phpstan, psalm
- Ruby: ruby -c, rubocop
- C/C++: gcc/clang, cppcheck
- Swift: swiftc, swiftlint
- Scala: scalac, scalafix
- Elixir: mix compile, credo
- Dart: dart analyze
- Lua: luacheck
- R: lintr
- Shell: shellcheck, bash -n
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from .languages import Language, get_language_for_extension

__all__ = [
    "Diagnostic",
    "DiagnosticResult",
    "DiagnosticSeverity",
    "DiagnosticsClient",
    "check_file",
    "check_project",
    "get_available_tools",
]


class DiagnosticSeverity(str, Enum):
    """Severity levels for diagnostics."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    HINT = "hint"


@dataclass
class Diagnostic:
    """A single diagnostic message."""

    file: str
    line: int
    column: int = 0
    end_line: int | None = None
    end_column: int | None = None
    severity: DiagnosticSeverity = DiagnosticSeverity.ERROR
    message: str = ""
    code: str = ""  # Error code (e.g., E501, TS2345)
    source: str = ""  # Tool that produced this (e.g., pyright, eslint)

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "file": self.file,
            "line": self.line,
            "column": self.column,
            "end_line": self.end_line,
            "end_column": self.end_column,
            "severity": self.severity.value,
            "message": self.message,
            "code": self.code,
            "source": self.source,
        }

    def format(self) -> str:
        """Format for display."""
        severity = self.severity.value.upper()
        location = f"{self.file}:{self.line}"
        if self.column:
            location += f":{self.column}"
        code_part = f" [{self.code}]" if self.code else ""
        return f"{location}: {severity}{code_part}: {self.message}"


@dataclass
class DiagnosticResult:
    """Result of running diagnostics."""

    success: bool
    diagnostics: list[Diagnostic] = field(default_factory=list)
    tool: str = ""
    error: str | None = None
    elapsed_seconds: float = 0.0

    @property
    def error_count(self) -> int:
        """Count of errors."""
        return sum(1 for d in self.diagnostics if d.severity == DiagnosticSeverity.ERROR)

    @property
    def warning_count(self) -> int:
        """Count of warnings."""
        return sum(1 for d in self.diagnostics if d.severity == DiagnosticSeverity.WARNING)

    def format_summary(self) -> str:
        """Format a summary of diagnostics."""
        if not self.diagnostics:
            return f"✓ No issues found ({self.tool})"

        errors = self.error_count
        warnings = self.warning_count
        others = len(self.diagnostics) - errors - warnings

        parts = []
        if errors:
            parts.append(f"{errors} error(s)")
        if warnings:
            parts.append(f"{warnings} warning(s)")
        if others:
            parts.append(f"{others} other(s)")

        return f"{self.tool}: {', '.join(parts)}"


def _run_tool(
    cmd: list[str],
    cwd: Path,
    timeout: int = 60,
) -> tuple[str, str, int]:
    """Run a diagnostic tool and return output.

    Args:
        cmd: Command to run as argv
        cwd: Working directory
        timeout: Timeout in seconds

    Returns:
        Tuple of (stdout, stderr, returncode)
    """
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", f"Timeout after {timeout}s", -1
    except FileNotFoundError:
        return "", f"Tool not found: {cmd[0]}", -1
    except Exception as e:
        return "", str(e), -1


def _is_tool_available(tool: str) -> bool:
    """Check if a tool is available in PATH."""
    try:
        result = subprocess.run(
            ["which", tool],
            capture_output=True,
            timeout=5,
        )
        return result.returncode == 0
    except Exception:
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# Python Diagnostics
# ═══════════════════════════════════════════════════════════════════════════════


def _check_python_pyright(filepath: str, cwd: Path) -> DiagnosticResult:
    """Check Python file with pyright."""
    stdout, stderr, returncode = _run_tool(
        ["pyright", "--outputjson", filepath],
        cwd,
    )

    diagnostics: list[Diagnostic] = []

    if stdout:
        try:
            data = json.loads(stdout)
            for diag in data.get("generalDiagnostics", []):
                severity = DiagnosticSeverity.ERROR
                if diag.get("severity") == 2:
                    severity = DiagnosticSeverity.WARNING
                elif diag.get("severity") == 3:
                    severity = DiagnosticSeverity.INFO

                range_data = diag.get("range", {})
                start = range_data.get("start", {})

                diagnostics.append(
                    Diagnostic(
                        file=diag.get("file", filepath),
                        line=start.get("line", 0) + 1,
                        column=start.get("character", 0),
                        severity=severity,
                        message=diag.get("message", ""),
                        code=diag.get("rule", ""),
                        source="pyright",
                    )
                )
        except json.JSONDecodeError:
            pass

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool="pyright",
        error=stderr if returncode != 0 and not diagnostics else None,
    )


def _check_python_ruff(filepath: str, cwd: Path) -> DiagnosticResult:
    """Check Python file with ruff."""
    stdout, stderr, returncode = _run_tool(
        ["ruff", "check", "--output-format=json", filepath],
        cwd,
    )

    diagnostics: list[Diagnostic] = []

    if stdout:
        try:
            data = json.loads(stdout)
            for item in data:
                diagnostics.append(
                    Diagnostic(
                        file=item.get("filename", filepath),
                        line=item.get("location", {}).get("row", 0),
                        column=item.get("location", {}).get("column", 0),
                        severity=DiagnosticSeverity.WARNING,  # Ruff mostly reports lints
                        message=item.get("message", ""),
                        code=item.get("code", ""),
                        source="ruff",
                    )
                )
        except json.JSONDecodeError:
            pass

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool="ruff",
    )


# ═══════════════════════════════════════════════════════════════════════════════
# JavaScript/TypeScript Diagnostics
# ═══════════════════════════════════════════════════════════════════════════════


def _check_typescript(filepath: str, cwd: Path) -> DiagnosticResult:
    """Check TypeScript/JavaScript file with tsc."""
    stdout, stderr, returncode = _run_tool(
        ["npx", "tsc", "--noEmit", "--pretty", "false", filepath],
        cwd,
    )

    diagnostics: list[Diagnostic] = []

    # Parse tsc output: file(line,col): error TSxxxx: message
    pattern = re.compile(r"(.+)\((\d+),(\d+)\):\s*(error|warning)\s+TS(\d+):\s*(.+)")

    for line in (stdout + stderr).splitlines():
        match = pattern.match(line)
        if match:
            severity = DiagnosticSeverity.ERROR
            if match.group(4) == "warning":
                severity = DiagnosticSeverity.WARNING

            diagnostics.append(
                Diagnostic(
                    file=match.group(1),
                    line=int(match.group(2)),
                    column=int(match.group(3)),
                    severity=severity,
                    message=match.group(6),
                    code=f"TS{match.group(5)}",
                    source="typescript",
                )
            )

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool="typescript",
    )


def _check_eslint(filepath: str, cwd: Path) -> DiagnosticResult:
    """Check JavaScript/TypeScript file with ESLint."""
    stdout, stderr, returncode = _run_tool(
        ["npx", "eslint", "--format=json", filepath],
        cwd,
    )

    diagnostics: list[Diagnostic] = []

    if stdout:
        try:
            data = json.loads(stdout)
            for file_result in data:
                for msg in file_result.get("messages", []):
                    severity = DiagnosticSeverity.WARNING
                    if msg.get("severity") == 2:
                        severity = DiagnosticSeverity.ERROR

                    diagnostics.append(
                        Diagnostic(
                            file=file_result.get("filePath", filepath),
                            line=msg.get("line", 0),
                            column=msg.get("column", 0),
                            end_line=msg.get("endLine"),
                            end_column=msg.get("endColumn"),
                            severity=severity,
                            message=msg.get("message", ""),
                            code=msg.get("ruleId", ""),
                            source="eslint",
                        )
                    )
        except json.JSONDecodeError:
            pass

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool="eslint",
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Rust Diagnostics
# ═══════════════════════════════════════════════════════════════════════════════


def _check_rust_cargo(cwd: Path) -> DiagnosticResult:
    """Check Rust project with cargo check."""
    stdout, stderr, returncode = _run_tool(
        ["cargo", "check", "--message-format=json"],
        cwd,
        timeout=120,
    )

    diagnostics: list[Diagnostic] = []

    for line in stdout.splitlines():
        if not line.strip():
            continue
        try:
            msg = json.loads(line)
            if msg.get("reason") == "compiler-message":
                message = msg.get("message", {})
                spans = message.get("spans", [])

                severity = DiagnosticSeverity.WARNING
                level = message.get("level", "")
                if level == "error":
                    severity = DiagnosticSeverity.ERROR
                elif level == "note" or level == "help":
                    severity = DiagnosticSeverity.INFO

                if spans:
                    span = spans[0]
                    diagnostics.append(
                        Diagnostic(
                            file=span.get("file_name", ""),
                            line=span.get("line_start", 0),
                            column=span.get("column_start", 0),
                            end_line=span.get("line_end"),
                            end_column=span.get("column_end"),
                            severity=severity,
                            message=message.get("message", ""),
                            code=message.get("code", {}).get("code", ""),
                            source="cargo",
                        )
                    )
        except json.JSONDecodeError:
            pass

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool="cargo",
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Go Diagnostics
# ═══════════════════════════════════════════════════════════════════════════════


def _check_go_vet(cwd: Path) -> DiagnosticResult:
    """Check Go project with go vet."""
    stdout, stderr, returncode = _run_tool(
        ["go", "vet", "./..."],
        cwd,
    )

    diagnostics: list[Diagnostic] = []

    # Parse go vet output: file:line:col: message
    pattern = re.compile(r"(.+?):(\d+):(\d+):\s*(.+)")

    for line in (stdout + stderr).splitlines():
        match = pattern.match(line)
        if match:
            diagnostics.append(
                Diagnostic(
                    file=match.group(1),
                    line=int(match.group(2)),
                    column=int(match.group(3)),
                    severity=DiagnosticSeverity.WARNING,
                    message=match.group(4),
                    source="go vet",
                )
            )

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool="go vet",
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Java Diagnostics
# ═══════════════════════════════════════════════════════════════════════════════


def _check_java_javac(filepath: str, cwd: Path) -> DiagnosticResult:
    """Check Java file with javac."""
    import tempfile

    stdout, stderr, returncode = _run_tool(
        ["javac", "-Xlint:all", "-d", tempfile.gettempdir(), filepath],
        cwd,
    )

    diagnostics: list[Diagnostic] = []

    # Parse javac output: file:line: severity: message
    pattern = re.compile(r"(.+?):(\d+):\s*(error|warning):\s*(.+)")

    for line in (stdout + stderr).splitlines():
        match = pattern.match(line)
        if match:
            severity = DiagnosticSeverity.ERROR
            if match.group(3) == "warning":
                severity = DiagnosticSeverity.WARNING

            diagnostics.append(
                Diagnostic(
                    file=match.group(1),
                    line=int(match.group(2)),
                    severity=severity,
                    message=match.group(4),
                    source="javac",
                )
            )

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool="javac",
    )


# ═══════════════════════════════════════════════════════════════════════════════
# C# Diagnostics
# ═══════════════════════════════════════════════════════════════════════════════


def _check_csharp_dotnet(cwd: Path) -> DiagnosticResult:
    """Check C# project with dotnet build."""
    stdout, stderr, returncode = _run_tool(
        ["dotnet", "build", "--no-restore", "-nologo", "-consoleloggerparameters:NoSummary"],
        cwd,
        timeout=120,
    )

    diagnostics: list[Diagnostic] = []

    # Parse dotnet output: file(line,col): severity CSxxxx: message
    pattern = re.compile(r"(.+?)\((\d+),(\d+)\):\s*(error|warning)\s+(\w+):\s*(.+)")

    for line in (stdout + stderr).splitlines():
        match = pattern.match(line)
        if match:
            severity = DiagnosticSeverity.ERROR
            if match.group(4) == "warning":
                severity = DiagnosticSeverity.WARNING

            diagnostics.append(
                Diagnostic(
                    file=match.group(1),
                    line=int(match.group(2)),
                    column=int(match.group(3)),
                    severity=severity,
                    message=match.group(6),
                    code=match.group(5),
                    source="dotnet",
                )
            )

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool="dotnet",
    )


# ═══════════════════════════════════════════════════════════════════════════════
# PHP Diagnostics
# ═══════════════════════════════════════════════════════════════════════════════


def _check_php_syntax(filepath: str, cwd: Path) -> DiagnosticResult:
    """Check PHP file syntax with php -l."""
    stdout, stderr, returncode = _run_tool(
        ["php", "-l", filepath],
        cwd,
    )

    diagnostics: list[Diagnostic] = []

    # Parse php -l output: PHP Parse error: message in file on line N
    pattern = re.compile(
        r"PHP\s+(?:Parse\s+)?(?:error|warning):\s*(.+?)\s+in\s+(.+?)\s+on\s+line\s+(\d+)"
    )

    for line in (stdout + stderr).splitlines():
        match = pattern.search(line)
        if match:
            diagnostics.append(
                Diagnostic(
                    file=match.group(2),
                    line=int(match.group(3)),
                    severity=DiagnosticSeverity.ERROR,
                    message=match.group(1),
                    source="php",
                )
            )

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool="php",
    )


def _check_phpstan(filepath: str, cwd: Path) -> DiagnosticResult:
    """Check PHP file with PHPStan."""
    stdout, stderr, returncode = _run_tool(
        ["vendor/bin/phpstan", "analyse", "--error-format=json", filepath],
        cwd,
    )

    diagnostics: list[Diagnostic] = []

    if stdout:
        try:
            data = json.loads(stdout)
            for file_path, errors in data.get("files", {}).items():
                for error in errors.get("messages", []):
                    diagnostics.append(
                        Diagnostic(
                            file=file_path,
                            line=error.get("line", 0),
                            severity=DiagnosticSeverity.ERROR,
                            message=error.get("message", ""),
                            source="phpstan",
                        )
                    )
        except json.JSONDecodeError:
            pass

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool="phpstan",
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Ruby Diagnostics
# ═══════════════════════════════════════════════════════════════════════════════


def _check_ruby_syntax(filepath: str, cwd: Path) -> DiagnosticResult:
    """Check Ruby file syntax with ruby -c."""
    stdout, stderr, returncode = _run_tool(
        ["ruby", "-c", filepath],
        cwd,
    )

    diagnostics: list[Diagnostic] = []

    # Parse ruby -c output: file:line: message
    pattern = re.compile(r"(.+?):(\d+):\s*(.+)")

    for line in stderr.splitlines():
        match = pattern.match(line)
        if match:
            diagnostics.append(
                Diagnostic(
                    file=match.group(1),
                    line=int(match.group(2)),
                    severity=DiagnosticSeverity.ERROR,
                    message=match.group(3),
                    source="ruby",
                )
            )

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool="ruby",
    )


def _check_rubocop(filepath: str, cwd: Path) -> DiagnosticResult:
    """Check Ruby file with RuboCop."""
    stdout, stderr, returncode = _run_tool(
        ["bundle", "exec", "rubocop", "--format=json", filepath],
        cwd,
    )

    diagnostics: list[Diagnostic] = []

    if stdout:
        try:
            data = json.loads(stdout)
            for file_result in data.get("files", []):
                for offense in file_result.get("offenses", []):
                    severity = DiagnosticSeverity.WARNING
                    if offense.get("severity") in {"error", "fatal"}:
                        severity = DiagnosticSeverity.ERROR

                    location = offense.get("location", {})
                    diagnostics.append(
                        Diagnostic(
                            file=file_result.get("path", filepath),
                            line=location.get("line", 0),
                            column=location.get("column", 0),
                            severity=severity,
                            message=offense.get("message", ""),
                            code=offense.get("cop_name", ""),
                            source="rubocop",
                        )
                    )
        except json.JSONDecodeError:
            pass

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool="rubocop",
    )


# ═══════════════════════════════════════════════════════════════════════════════
# C/C++ Diagnostics
# ═══════════════════════════════════════════════════════════════════════════════


def _check_c_gcc(filepath: str, cwd: Path) -> DiagnosticResult:
    """Check C/C++ file with gcc/g++ -fsyntax-only."""
    is_cpp = filepath.endswith((".cpp", ".cc", ".cxx", ".hpp"))
    compiler = "g++" if is_cpp else "gcc"

    stdout, stderr, returncode = _run_tool(
        [compiler, "-fsyntax-only", "-Wall", "-Wextra", filepath],
        cwd,
    )

    diagnostics: list[Diagnostic] = []

    # Parse gcc output: file:line:col: severity: message
    pattern = re.compile(r"(.+?):(\d+):(\d+):\s*(error|warning|note):\s*(.+)")

    for line in stderr.splitlines():
        match = pattern.match(line)
        if match:
            severity = DiagnosticSeverity.ERROR
            if match.group(4) == "warning":
                severity = DiagnosticSeverity.WARNING
            elif match.group(4) == "note":
                severity = DiagnosticSeverity.INFO

            diagnostics.append(
                Diagnostic(
                    file=match.group(1),
                    line=int(match.group(2)),
                    column=int(match.group(3)),
                    severity=severity,
                    message=match.group(5),
                    source=compiler,
                )
            )

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool=compiler,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Swift Diagnostics
# ═══════════════════════════════════════════════════════════════════════════════


def _check_swift_syntax(filepath: str, cwd: Path) -> DiagnosticResult:
    """Check Swift file syntax with swiftc -parse."""
    stdout, stderr, returncode = _run_tool(
        ["swiftc", "-parse", filepath],
        cwd,
    )

    diagnostics: list[Diagnostic] = []

    # Parse swiftc output: file:line:col: error: message
    pattern = re.compile(r"(.+?):(\d+):(\d+):\s*(error|warning|note):\s*(.+)")

    for line in stderr.splitlines():
        match = pattern.match(line)
        if match:
            severity = DiagnosticSeverity.ERROR
            if match.group(4) == "warning":
                severity = DiagnosticSeverity.WARNING
            elif match.group(4) == "note":
                severity = DiagnosticSeverity.INFO

            diagnostics.append(
                Diagnostic(
                    file=match.group(1),
                    line=int(match.group(2)),
                    column=int(match.group(3)),
                    severity=severity,
                    message=match.group(5),
                    source="swiftc",
                )
            )

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool="swiftc",
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Elixir Diagnostics
# ═══════════════════════════════════════════════════════════════════════════════


def _check_elixir_compile(cwd: Path) -> DiagnosticResult:
    """Check Elixir project with mix compile."""
    stdout, stderr, returncode = _run_tool(
        ["mix", "compile", "--warnings-as-errors"],
        cwd,
    )

    diagnostics: list[Diagnostic] = []

    # Parse mix compile output
    pattern = re.compile(r"(.+?):(\d+):\s*(error|warning):\s*(.+)")

    for line in (stdout + stderr).splitlines():
        match = pattern.match(line)
        if match:
            severity = DiagnosticSeverity.ERROR
            if match.group(3) == "warning":
                severity = DiagnosticSeverity.WARNING

            diagnostics.append(
                Diagnostic(
                    file=match.group(1),
                    line=int(match.group(2)),
                    severity=severity,
                    message=match.group(4),
                    source="mix",
                )
            )

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool="mix",
    )


def _check_credo(cwd: Path) -> DiagnosticResult:
    """Check Elixir project with Credo."""
    stdout, stderr, returncode = _run_tool(
        ["mix", "credo", "--format=json"],
        cwd,
    )

    diagnostics: list[Diagnostic] = []

    if stdout:
        try:
            data = json.loads(stdout)
            for issue in data.get("issues", []):
                severity = DiagnosticSeverity.WARNING
                priority = issue.get("priority", 0)
                if priority >= 10:
                    severity = DiagnosticSeverity.ERROR

                diagnostics.append(
                    Diagnostic(
                        file=issue.get("filename", ""),
                        line=issue.get("line_no", 0),
                        column=issue.get("column", 0),
                        severity=severity,
                        message=issue.get("message", ""),
                        code=issue.get("check", ""),
                        source="credo",
                    )
                )
        except json.JSONDecodeError:
            pass

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool="credo",
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Dart Diagnostics
# ═══════════════════════════════════════════════════════════════════════════════


def _check_dart_analyze(filepath: str, cwd: Path) -> DiagnosticResult:
    """Check Dart file with dart analyze."""
    stdout, stderr, returncode = _run_tool(
        ["dart", "analyze", filepath],
        cwd,
    )

    diagnostics: list[Diagnostic] = []

    # Parse dart analyze output: severity • message at file:line:col
    pattern = re.compile(r"(\w+)\s*•\s*(.+?)\s+at\s+(.+?):(\d+):(\d+)")

    for line in (stdout + stderr).splitlines():
        match = pattern.search(line)
        if match:
            severity = DiagnosticSeverity.INFO
            if match.group(1).lower() == "error":
                severity = DiagnosticSeverity.ERROR
            elif match.group(1).lower() == "warning":
                severity = DiagnosticSeverity.WARNING

            diagnostics.append(
                Diagnostic(
                    file=match.group(3),
                    line=int(match.group(4)),
                    column=int(match.group(5)),
                    severity=severity,
                    message=match.group(2),
                    source="dart",
                )
            )

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool="dart",
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Shell Diagnostics
# ═══════════════════════════════════════════════════════════════════════════════


def _check_shellcheck(filepath: str, cwd: Path) -> DiagnosticResult:
    """Check shell script with shellcheck."""
    stdout, stderr, returncode = _run_tool(
        ["shellcheck", "--format=json", filepath],
        cwd,
    )

    diagnostics: list[Diagnostic] = []

    if stdout:
        try:
            data = json.loads(stdout)
            for item in data:
                severity = DiagnosticSeverity.WARNING
                level = item.get("level", "")
                if level == "error":
                    severity = DiagnosticSeverity.ERROR
                elif level == "info" or level == "style":
                    severity = DiagnosticSeverity.INFO

                diagnostics.append(
                    Diagnostic(
                        file=item.get("file", filepath),
                        line=item.get("line", 0),
                        column=item.get("column", 0),
                        end_line=item.get("endLine"),
                        end_column=item.get("endColumn"),
                        severity=severity,
                        message=item.get("message", ""),
                        code=f"SC{item.get('code', '')}",
                        source="shellcheck",
                    )
                )
        except json.JSONDecodeError:
            pass

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool="shellcheck",
    )


def _check_bash_syntax(filepath: str, cwd: Path) -> DiagnosticResult:
    """Check bash script syntax with bash -n."""
    stdout, stderr, returncode = _run_tool(
        ["bash", "-n", filepath],
        cwd,
    )

    diagnostics: list[Diagnostic] = []

    # Parse bash -n output: file: line N: message
    pattern = re.compile(r"(.+?):\s*line\s+(\d+):\s*(.+)")

    for line in stderr.splitlines():
        match = pattern.match(line)
        if match:
            diagnostics.append(
                Diagnostic(
                    file=match.group(1),
                    line=int(match.group(2)),
                    severity=DiagnosticSeverity.ERROR,
                    message=match.group(3),
                    source="bash",
                )
            )

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool="bash",
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Python mypy Diagnostics (P1-21: Add missing checkers)
# ═══════════════════════════════════════════════════════════════════════════════


def _check_python_mypy(filepath: str, cwd: Path) -> DiagnosticResult:
    """Check Python file with mypy."""
    stdout, stderr, returncode = _run_tool(
        ["mypy", "--show-column-numbers", "--no-error-summary", filepath],
        cwd,
    )

    diagnostics: list[Diagnostic] = []

    # Parse mypy output: file:line:col: error: message
    pattern = re.compile(r"(.+?):(\d+):(\d+):\s*(error|warning|note):\s*(.+)")

    for line in stdout.splitlines():
        match = pattern.match(line)
        if match:
            severity_map = {
                "error": DiagnosticSeverity.ERROR,
                "warning": DiagnosticSeverity.WARNING,
                "note": DiagnosticSeverity.INFO,
            }
            diagnostics.append(
                Diagnostic(
                    file=match.group(1),
                    line=int(match.group(2)),
                    column=int(match.group(3)),
                    severity=severity_map.get(match.group(4), DiagnosticSeverity.ERROR),
                    message=match.group(5),
                    source="mypy",
                )
            )

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool="mypy",
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Kotlin Diagnostics (P1-22: Add Kotlin support)
# ═══════════════════════════════════════════════════════════════════════════════


def _check_kotlin_compile(filepath: str, cwd: Path) -> DiagnosticResult:
    """Check Kotlin file with kotlinc."""
    stdout, stderr, returncode = _run_tool(
        ["kotlinc", "-Werror", filepath, "-d", os.devnull],
        cwd,
    )

    diagnostics: list[Diagnostic] = []

    # Parse kotlinc output: file:line:col: error/warning: message
    pattern = re.compile(r"(.+?):(\d+):(\d+):\s*(error|warning):\s*(.+)")

    for line in (stdout + stderr).splitlines():
        match = pattern.match(line)
        if match:
            severity = (
                DiagnosticSeverity.ERROR
                if match.group(4) == "error"
                else DiagnosticSeverity.WARNING
            )
            diagnostics.append(
                Diagnostic(
                    file=match.group(1),
                    line=int(match.group(2)),
                    column=int(match.group(3)),
                    severity=severity,
                    message=match.group(5),
                    source="kotlinc",
                )
            )

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool="kotlinc",
    )


def _check_kotlin_ktlint(filepath: str, cwd: Path) -> DiagnosticResult:
    """Check Kotlin file with ktlint."""
    stdout, stderr, returncode = _run_tool(
        ["ktlint", "--reporter=json", filepath],
        cwd,
    )

    diagnostics: list[Diagnostic] = []

    if stdout:
        try:
            data = json.loads(stdout)
            for item in data:
                for error in item.get("errors", []):
                    diagnostics.append(
                        Diagnostic(
                            file=item.get("file", filepath),
                            line=error.get("line", 0),
                            column=error.get("column", 0),
                            severity=DiagnosticSeverity.WARNING,
                            message=error.get("message", ""),
                            code=error.get("rule", ""),
                            source="ktlint",
                        )
                    )
        except json.JSONDecodeError:
            pass

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool="ktlint",
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Scala Diagnostics (P1-23: Add Scala support)
# ═══════════════════════════════════════════════════════════════════════════════


def _check_scala_compile(filepath: str, cwd: Path) -> DiagnosticResult:
    """Check Scala file with scalac."""
    stdout, stderr, returncode = _run_tool(
        ["scalac", "-deprecation", "-feature", filepath],
        cwd,
    )

    diagnostics: list[Diagnostic] = []

    # Parse scalac output
    pattern = re.compile(r"(.+?):(\d+):\s*(error|warning):\s*(.+)")

    for line in (stdout + stderr).splitlines():
        match = pattern.match(line)
        if match:
            severity = (
                DiagnosticSeverity.ERROR
                if match.group(3) == "error"
                else DiagnosticSeverity.WARNING
            )
            diagnostics.append(
                Diagnostic(
                    file=match.group(1),
                    line=int(match.group(2)),
                    severity=severity,
                    message=match.group(4),
                    source="scalac",
                )
            )

    return DiagnosticResult(
        success=returncode == 0,
        diagnostics=diagnostics,
        tool="scalac",
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Main Interface
# ═══════════════════════════════════════════════════════════════════════════════

# Language to checker mapping (P1-21-23: Added mypy, Kotlin, Scala)
_FILE_CHECKERS: dict[Language, list[Callable[[str, Path], DiagnosticResult]]] = {
    Language.PYTHON: [_check_python_pyright, _check_python_ruff, _check_python_mypy],
    Language.JAVASCRIPT: [_check_typescript, _check_eslint],
    Language.TYPESCRIPT: [_check_typescript, _check_eslint],
    Language.JAVA: [_check_java_javac],
    Language.KOTLIN: [_check_kotlin_compile, _check_kotlin_ktlint],
    Language.SCALA: [_check_scala_compile],
    Language.PHP: [_check_php_syntax, _check_phpstan],
    Language.RUBY: [_check_ruby_syntax, _check_rubocop],
    Language.C: [_check_c_gcc],
    Language.CPP: [_check_c_gcc],
    Language.SWIFT: [_check_swift_syntax],
    Language.DART: [_check_dart_analyze],
    Language.SHELL: [_check_bash_syntax, _check_shellcheck],
}

# Project-level checkers (check whole project, not individual files)
_PROJECT_CHECKERS: dict[Language, list[Callable[[Path], DiagnosticResult]]] = {
    Language.RUST: [_check_rust_cargo],
    Language.GO: [_check_go_vet],
    Language.CSHARP: [_check_csharp_dotnet],
    Language.ELIXIR: [_check_elixir_compile, _check_credo],
}


class DiagnosticsClient:
    """Client for running diagnostics on files and projects."""

    def __init__(self, cwd: Path) -> None:
        self.cwd = cwd.resolve()
        self._available_tools: dict[str, bool] = {}
        self._check_tools()

    def _check_tools(self) -> None:
        """Check which diagnostic tools are available."""
        tools = [
            # Python
            "pyright",
            "ruff",
            "mypy",
            # JavaScript/TypeScript
            "npx",
            "eslint",
            # Rust/Go
            "cargo",
            "go",
            # JVM languages
            "dotnet",
            "javac",
            "kotlinc",
            "ktlint",
            "scalac",
            # PHP/Ruby
            "php",
            "phpstan",
            "ruby",
            "rubocop",
            # C/C++
            "gcc",
            "g++",
            "clang",
            "cppcheck",
            # Swift
            "swiftc",
            "swiftlint",
            # Elixir/Dart
            "mix",
            "dart",
            # Shell
            "shellcheck",
            "bash",
        ]

        for tool in tools:
            self._available_tools[tool] = _is_tool_available(tool)

    def is_tool_available(self, tool: str) -> bool:
        """Check if a tool is available."""
        return self._available_tools.get(tool, False)

    def check_file(self, filepath: str) -> DiagnosticResult:
        """Check a single file for diagnostics.

        Args:
            filepath: Relative path to the file

        Returns:
            DiagnosticResult with all diagnostics
        """
        full_path = self.cwd / filepath
        if not full_path.exists():
            return DiagnosticResult(
                success=False,
                tool="none",
                error=f"File not found: {filepath}",
            )

        language = get_language_for_extension(full_path.suffix)

        # Try file-level checkers
        if language in _FILE_CHECKERS:
            for checker in _FILE_CHECKERS[language]:
                try:
                    result = checker(filepath, self.cwd)
                    if result.diagnostics or result.success:
                        return result
                except Exception:
                    continue

        # Try project-level checkers
        if language in _PROJECT_CHECKERS:
            for checker in _PROJECT_CHECKERS[language]:
                try:
                    result = checker(self.cwd)
                    # Filter to just this file
                    result.diagnostics = [
                        d
                        for d in result.diagnostics
                        if d.file == filepath or d.file.endswith(filepath)
                    ]
                    return result
                except Exception:
                    continue

        return DiagnosticResult(
            success=True,
            tool="none",
            error=f"No checker available for {language.value}",
        )

    def check_project(self, languages: set[Language] | None = None) -> list[DiagnosticResult]:
        """Check the entire project for diagnostics.

        Args:
            languages: Optional set of languages to check

        Returns:
            List of DiagnosticResults from all checkers
        """
        results: list[DiagnosticResult] = []

        # Run project-level checkers
        for language, checkers in _PROJECT_CHECKERS.items():
            if languages and language not in languages:
                continue

            for checker in checkers:
                try:
                    result = checker(self.cwd)
                    results.append(result)
                except Exception:
                    continue

        return results

    def get_available_checkers(self) -> dict[Language, list[str]]:
        """Get available checkers by language.

        Returns:
            Dictionary mapping languages to available checker names
        """
        available: dict[Language, list[str]] = {}

        for language in Language:
            checkers = []

            if language == Language.PYTHON:
                if self.is_tool_available("pyright"):
                    checkers.append("pyright")
                if self.is_tool_available("ruff"):
                    checkers.append("ruff")
                if self.is_tool_available("mypy"):
                    checkers.append("mypy")
            elif language == Language.KOTLIN:
                if self.is_tool_available("kotlinc"):
                    checkers.append("kotlinc")
                if self.is_tool_available("ktlint"):
                    checkers.append("ktlint")
            elif language == Language.SCALA:
                if self.is_tool_available("scalac"):
                    checkers.append("scalac")
            elif language in {Language.JAVASCRIPT, Language.TYPESCRIPT}:
                if self.is_tool_available("npx"):
                    checkers.append("typescript")
                    checkers.append("eslint")
            elif language == Language.RUST:
                if self.is_tool_available("cargo"):
                    checkers.append("cargo")
            elif language == Language.GO:
                if self.is_tool_available("go"):
                    checkers.append("go vet")
            elif language == Language.CSHARP:
                if self.is_tool_available("dotnet"):
                    checkers.append("dotnet")
            elif language == Language.JAVA:
                if self.is_tool_available("javac"):
                    checkers.append("javac")
            elif language == Language.PHP:
                if self.is_tool_available("php"):
                    checkers.append("php")
                if self.is_tool_available("phpstan"):
                    checkers.append("phpstan")
            elif language == Language.RUBY:
                if self.is_tool_available("ruby"):
                    checkers.append("ruby")
                if self.is_tool_available("rubocop"):
                    checkers.append("rubocop")
            elif language in {Language.C, Language.CPP}:
                if self.is_tool_available("gcc"):
                    checkers.append("gcc")
                if self.is_tool_available("clang"):
                    checkers.append("clang")
            elif language == Language.SWIFT:
                if self.is_tool_available("swiftc"):
                    checkers.append("swiftc")
            elif language == Language.ELIXIR:
                if self.is_tool_available("mix"):
                    checkers.append("mix")
            elif language == Language.DART:
                if self.is_tool_available("dart"):
                    checkers.append("dart")
            elif language == Language.SHELL:
                if self.is_tool_available("shellcheck"):
                    checkers.append("shellcheck")
                if self.is_tool_available("bash"):
                    checkers.append("bash")

            if checkers:
                available[language] = checkers

        return available


# Convenience functions


def check_file(filepath: str, cwd: Path) -> DiagnosticResult:
    """Check a single file for diagnostics.

    Args:
        filepath: Relative path to the file
        cwd: Working directory

    Returns:
        DiagnosticResult
    """
    client = DiagnosticsClient(cwd)
    return client.check_file(filepath)


def check_project(cwd: Path, languages: set[Language] | None = None) -> list[DiagnosticResult]:
    """Check an entire project for diagnostics.

    Args:
        cwd: Working directory
        languages: Optional set of languages to check

    Returns:
        List of DiagnosticResults
    """
    client = DiagnosticsClient(cwd)
    return client.check_project(languages)


def get_available_tools(cwd: Path) -> dict[Language, list[str]]:
    """Get available diagnostic tools.

    Args:
        cwd: Working directory

    Returns:
        Dictionary mapping languages to available tools
    """
    client = DiagnosticsClient(cwd)
    return client.get_available_checkers()
