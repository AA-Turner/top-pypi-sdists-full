"""Comprehensive tests for sage/core/diagnostics.py - Extended diagnostics support."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sage.core.diagnostics import (
    Diagnostic,
    DiagnosticResult,
    DiagnosticSeverity,
    DiagnosticsClient,
    _is_tool_available,
    _run_tool,
)


# =============================================================================
# Tests for DiagnosticSeverity enum
# =============================================================================


class TestDiagnosticSeverity:
    """Tests for DiagnosticSeverity enum."""

    def test_error_value(self):
        """ERROR has correct value."""
        assert DiagnosticSeverity.ERROR.value == "error"

    def test_warning_value(self):
        """WARNING has correct value."""
        assert DiagnosticSeverity.WARNING.value == "warning"

    def test_info_value(self):
        """INFO has correct value."""
        assert DiagnosticSeverity.INFO.value == "info"

    def test_hint_value(self):
        """HINT has correct value."""
        assert DiagnosticSeverity.HINT.value == "hint"

    def test_is_string_enum(self):
        """DiagnosticSeverity is a string enum."""
        assert isinstance(DiagnosticSeverity.ERROR, str)
        assert DiagnosticSeverity.ERROR == "error"


# =============================================================================
# Tests for Diagnostic dataclass
# =============================================================================


class TestDiagnostic:
    """Tests for Diagnostic dataclass."""

    def test_create_minimal(self):
        """Create with minimal fields."""
        d = Diagnostic(file="test.py", line=10)
        assert d.file == "test.py"
        assert d.line == 10
        assert d.column == 0
        assert d.end_line is None
        assert d.end_column is None
        assert d.severity == DiagnosticSeverity.ERROR
        assert d.message == ""
        assert d.code == ""
        assert d.source == ""

    def test_create_full(self):
        """Create with all fields."""
        d = Diagnostic(
            file="test.py",
            line=10,
            column=5,
            end_line=12,
            end_column=10,
            severity=DiagnosticSeverity.WARNING,
            message="Some warning",
            code="W001",
            source="ruff",
        )
        assert d.column == 5
        assert d.end_line == 12
        assert d.severity == DiagnosticSeverity.WARNING
        assert d.code == "W001"
        assert d.source == "ruff"

    def test_to_dict(self):
        """Serialize to dictionary."""
        d = Diagnostic(
            file="test.py",
            line=10,
            column=5,
            severity=DiagnosticSeverity.ERROR,
            message="Error message",
            code="E001",
            source="pyright",
        )
        result = d.to_dict()
        assert result["file"] == "test.py"
        assert result["line"] == 10
        assert result["column"] == 5
        assert result["severity"] == "error"
        assert result["message"] == "Error message"
        assert result["code"] == "E001"
        assert result["source"] == "pyright"

    def test_format_basic(self):
        """Format for display - basic."""
        d = Diagnostic(
            file="test.py",
            line=10,
            severity=DiagnosticSeverity.ERROR,
            message="Error message",
        )
        formatted = d.format()
        assert "test.py:10" in formatted
        assert "ERROR" in formatted
        assert "Error message" in formatted

    def test_format_with_column(self):
        """Format for display - with column."""
        d = Diagnostic(
            file="test.py",
            line=10,
            column=5,
            severity=DiagnosticSeverity.WARNING,
            message="Warning",
        )
        formatted = d.format()
        assert "test.py:10:5" in formatted
        assert "WARNING" in formatted

    def test_format_with_code(self):
        """Format for display - with code."""
        d = Diagnostic(
            file="test.py",
            line=10,
            severity=DiagnosticSeverity.ERROR,
            message="Error",
            code="E001",
        )
        formatted = d.format()
        assert "[E001]" in formatted


# =============================================================================
# Tests for DiagnosticResult dataclass
# =============================================================================


class TestDiagnosticResult:
    """Tests for DiagnosticResult dataclass."""

    def test_create_success_empty(self):
        """Create success result with no diagnostics."""
        r = DiagnosticResult(success=True, tool="pytest")
        assert r.success is True
        assert r.diagnostics == []
        assert r.tool == "pytest"
        assert r.error is None

    def test_create_success_with_diagnostics(self):
        """Create success result with diagnostics."""
        diags = [
            Diagnostic("test.py", 1, message="Warning"),
            Diagnostic("test.py", 2, message="Another warning"),
        ]
        r = DiagnosticResult(success=True, diagnostics=diags, tool="ruff")
        assert len(r.diagnostics) == 2

    def test_create_failure(self):
        """Create failure result."""
        r = DiagnosticResult(
            success=False,
            tool="pyright",
            error="Tool not found",
        )
        assert r.success is False
        assert r.error == "Tool not found"

    def test_error_count(self):
        """Count errors in diagnostics."""
        diags = [
            Diagnostic("a.py", 1, severity=DiagnosticSeverity.ERROR),
            Diagnostic("b.py", 2, severity=DiagnosticSeverity.WARNING),
            Diagnostic("c.py", 3, severity=DiagnosticSeverity.ERROR),
        ]
        r = DiagnosticResult(success=False, diagnostics=diags, tool="x")
        assert r.error_count == 2

    def test_warning_count(self):
        """Count warnings in diagnostics."""
        diags = [
            Diagnostic("a.py", 1, severity=DiagnosticSeverity.ERROR),
            Diagnostic("b.py", 2, severity=DiagnosticSeverity.WARNING),
            Diagnostic("c.py", 3, severity=DiagnosticSeverity.WARNING),
        ]
        r = DiagnosticResult(success=False, diagnostics=diags, tool="x")
        assert r.warning_count == 2

    def test_format_summary_no_issues(self):
        """Format summary - no issues."""
        r = DiagnosticResult(success=True, tool="ruff")
        summary = r.format_summary()
        assert "No issues found" in summary
        assert "ruff" in summary

    def test_format_summary_errors_only(self):
        """Format summary - errors only."""
        diags = [
            Diagnostic("a.py", 1, severity=DiagnosticSeverity.ERROR),
            Diagnostic("b.py", 2, severity=DiagnosticSeverity.ERROR),
        ]
        r = DiagnosticResult(success=False, diagnostics=diags, tool="pyright")
        summary = r.format_summary()
        assert "2 error(s)" in summary

    def test_format_summary_mixed(self):
        """Format summary - mixed."""
        diags = [
            Diagnostic("a.py", 1, severity=DiagnosticSeverity.ERROR),
            Diagnostic("b.py", 2, severity=DiagnosticSeverity.WARNING),
            Diagnostic("c.py", 3, severity=DiagnosticSeverity.INFO),
        ]
        r = DiagnosticResult(success=False, diagnostics=diags, tool="x")
        summary = r.format_summary()
        assert "1 error(s)" in summary
        assert "1 warning(s)" in summary
        assert "1 other(s)" in summary


# =============================================================================
# Tests for _run_tool function
# =============================================================================


class TestRunTool:
    """Tests for _run_tool helper function."""

    @patch("subprocess.run")
    def test_run_success(self, mock_run):
        """Run tool successfully."""
        mock_run.return_value = MagicMock(
            stdout="output",
            stderr="",
            returncode=0,
        )
        stdout, stderr, code = _run_tool(["echo", "hello"], Path("."))
        assert stdout == "output"
        assert stderr == ""
        assert code == 0

    @patch("subprocess.run")
    def test_run_failure(self, mock_run):
        """Run tool with failure."""
        mock_run.return_value = MagicMock(
            stdout="",
            stderr="error",
            returncode=1,
        )
        stdout, stderr, code = _run_tool(["false"], Path("."))
        assert stderr == "error"
        assert code == 1

    @patch("subprocess.run")
    def test_run_timeout(self, mock_run):
        """Run tool with timeout."""
        import subprocess

        mock_run.side_effect = subprocess.TimeoutExpired("cmd", 60)
        stdout, stderr, code = _run_tool(["sleep", "100"], Path("."))
        assert "Timeout" in stderr
        assert code == -1

    @patch("subprocess.run")
    def test_run_not_found(self, mock_run):
        """Run tool not found."""
        mock_run.side_effect = FileNotFoundError()
        stdout, stderr, code = _run_tool(["nonexistent"], Path("."))
        assert "not found" in stderr
        assert code == -1

    @patch("subprocess.run")
    def test_run_exception(self, mock_run):
        """Run tool with exception."""
        mock_run.side_effect = Exception("Some error")
        stdout, stderr, code = _run_tool(["cmd"], Path("."))
        assert "Some error" in stderr
        assert code == -1


# =============================================================================
# Tests for _is_tool_available function
# =============================================================================


class TestIsToolAvailable:
    """Tests for _is_tool_available function."""

    @patch("subprocess.run")
    def test_tool_available(self, mock_run):
        """Tool is available."""
        mock_run.return_value = MagicMock(returncode=0)
        assert _is_tool_available("python") is True

    @patch("subprocess.run")
    def test_tool_not_available(self, mock_run):
        """Tool is not available."""
        mock_run.return_value = MagicMock(returncode=1)
        assert _is_tool_available("nonexistent") is False

    @patch("subprocess.run")
    def test_tool_check_exception(self, mock_run):
        """Tool check throws exception."""
        mock_run.side_effect = Exception()
        assert _is_tool_available("cmd") is False


# =============================================================================
# Tests for DiagnosticsClient class
# =============================================================================


class TestDiagnosticsClient:
    """Tests for DiagnosticsClient class."""

    @patch("sage.core.diagnostics._is_tool_available")
    def test_init(self, mock_available):
        """Initialize client."""
        mock_available.return_value = False
        client = DiagnosticsClient(Path("."))
        assert client.cwd == Path(".").resolve()

    @patch("sage.core.diagnostics._is_tool_available")
    def test_is_tool_available(self, mock_available):
        """Check tool availability."""
        mock_available.return_value = True
        client = DiagnosticsClient(Path("."))
        # The tools were checked during init
        assert isinstance(client._available_tools, dict)

    @patch("sage.core.diagnostics._is_tool_available")
    def test_check_file_not_found(self, mock_available):
        """Check file that doesn't exist."""
        mock_available.return_value = False
        client = DiagnosticsClient(Path("."))
        result = client.check_file("nonexistent_file.py")
        assert result.success is False
        assert "not found" in result.error

    @patch("sage.core.diagnostics._is_tool_available")
    def test_get_available_checkers(self, mock_available):
        """Get available checkers."""
        mock_available.return_value = True
        client = DiagnosticsClient(Path("."))
        checkers = client.get_available_checkers()
        # Should return a dict
        assert isinstance(checkers, dict)

    @patch("sage.core.diagnostics._is_tool_available")
    def test_check_project(self, mock_available):
        """Check project returns list."""
        mock_available.return_value = False
        client = DiagnosticsClient(Path("."))
        results = client.check_project()
        assert isinstance(results, list)


# =============================================================================
# Tests for parsing functions (mocked tool output)
# =============================================================================


class TestParsePyrightOutput:
    """Tests for pyright output parsing."""

    @patch("sage.core.diagnostics._run_tool")
    @patch("sage.core.diagnostics._is_tool_available")
    def test_parse_pyright_json(self, mock_available, mock_run):
        """Parse pyright JSON output."""
        mock_available.return_value = True
        mock_run.return_value = (
            json.dumps(
                {
                    "generalDiagnostics": [
                        {
                            "file": "test.py",
                            "severity": 1,  # Error
                            "message": "Type error",
                            "rule": "reportGeneralTypeIssues",
                            "range": {"start": {"line": 10, "character": 5}},
                        }
                    ]
                }
            ),
            "",
            1,
        )

        from sage.core.diagnostics import _check_python_pyright

        result = _check_python_pyright("test.py", Path("."))
        assert len(result.diagnostics) == 1
        assert result.diagnostics[0].line == 11  # 0-indexed to 1-indexed
        assert result.diagnostics[0].message == "Type error"


class TestParseRuffOutput:
    """Tests for ruff output parsing."""

    @patch("sage.core.diagnostics._run_tool")
    def test_parse_ruff_json(self, mock_run):
        """Parse ruff JSON output."""
        mock_run.return_value = (
            json.dumps(
                [
                    {
                        "filename": "test.py",
                        "location": {"row": 5, "column": 10},
                        "message": "Unused import",
                        "code": "F401",
                    }
                ]
            ),
            "",
            1,
        )

        from sage.core.diagnostics import _check_python_ruff

        result = _check_python_ruff("test.py", Path("."))
        assert len(result.diagnostics) == 1
        assert result.diagnostics[0].line == 5
        assert result.diagnostics[0].code == "F401"


class TestParseEslintOutput:
    """Tests for ESLint output parsing."""

    @patch("sage.core.diagnostics._run_tool")
    def test_parse_eslint_json(self, mock_run):
        """Parse ESLint JSON output."""
        mock_run.return_value = (
            json.dumps(
                [
                    {
                        "filePath": "app.js",
                        "messages": [
                            {
                                "severity": 2,  # Error
                                "line": 10,
                                "column": 5,
                                "message": "Unexpected var",
                                "ruleId": "no-var",
                            }
                        ],
                    }
                ]
            ),
            "",
            1,
        )

        from sage.core.diagnostics import _check_eslint

        result = _check_eslint("app.js", Path("."))
        assert len(result.diagnostics) == 1
        assert result.diagnostics[0].severity == DiagnosticSeverity.ERROR
        assert result.diagnostics[0].code == "no-var"


class TestParseRubocopOutput:
    """Tests for RuboCop output parsing."""

    @patch("sage.core.diagnostics._run_tool")
    def test_parse_rubocop_json(self, mock_run):
        """Parse RuboCop JSON output."""
        mock_run.return_value = (
            json.dumps(
                {
                    "files": [
                        {
                            "path": "app.rb",
                            "offenses": [
                                {
                                    "severity": "warning",
                                    "location": {"line": 5, "column": 1},
                                    "message": "Missing frozen string literal",
                                    "cop_name": "Style/FrozenStringLiteralComment",
                                }
                            ],
                        }
                    ]
                }
            ),
            "",
            0,
        )

        from sage.core.diagnostics import _check_rubocop

        result = _check_rubocop("app.rb", Path("."))
        assert len(result.diagnostics) == 1
        assert result.diagnostics[0].severity == DiagnosticSeverity.WARNING


# =============================================================================
# Tests for regex-based parsers
# =============================================================================


class TestRegexParsers:
    """Tests for regex-based diagnostic parsers."""

    @patch("sage.core.diagnostics._run_tool")
    def test_parse_gcc_output(self, mock_run):
        """Parse GCC output."""
        mock_run.return_value = (
            "",
            "test.c:10:5: error: expected ';' before '}'\n"
            "test.c:15:1: warning: unused variable 'x'\n",
            1,
        )

        from sage.core.diagnostics import _check_c_gcc

        result = _check_c_gcc("test.c", Path("."))
        assert len(result.diagnostics) == 2
        assert result.diagnostics[0].severity == DiagnosticSeverity.ERROR
        assert result.diagnostics[1].severity == DiagnosticSeverity.WARNING

    @patch("sage.core.diagnostics._run_tool")
    def test_parse_go_vet_output(self, mock_run):
        """Parse go vet output."""
        mock_run.return_value = (
            "",
            "main.go:10:5: printf call has arguments but no formatting directives\n",
            1,
        )

        from sage.core.diagnostics import _check_go_vet

        result = _check_go_vet(Path("."))
        assert len(result.diagnostics) == 1
        assert result.diagnostics[0].file == "main.go"
        assert result.diagnostics[0].line == 10

    @patch("sage.core.diagnostics._run_tool")
    def test_parse_typescript_output(self, mock_run):
        """Parse TypeScript output."""
        mock_run.return_value = (
            "app.ts(10,5): error TS2304: Cannot find name 'foo'\n",
            "",
            1,
        )

        from sage.core.diagnostics import _check_typescript

        result = _check_typescript("app.ts", Path("."))
        assert len(result.diagnostics) == 1
        assert result.diagnostics[0].file == "app.ts"
        assert result.diagnostics[0].code == "TS2304"


# =============================================================================
# Integration tests
# =============================================================================


class TestDiagnosticsIntegration:
    """Integration tests for diagnostics module."""

    def test_diagnostic_full_workflow(self):
        """Test full diagnostic workflow."""
        # Create diagnostics
        d1 = Diagnostic(
            file="src/main.py",
            line=10,
            column=5,
            severity=DiagnosticSeverity.ERROR,
            message="Undefined variable 'x'",
            code="E0602",
            source="pylint",
        )
        d2 = Diagnostic(
            file="src/main.py",
            line=15,
            severity=DiagnosticSeverity.WARNING,
            message="Line too long",
            code="E501",
            source="ruff",
        )

        # Create result
        result = DiagnosticResult(
            success=False,
            diagnostics=[d1, d2],
            tool="combined",
        )

        # Check counts
        assert result.error_count == 1
        assert result.warning_count == 1

        # Check formatting
        summary = result.format_summary()
        assert "1 error(s)" in summary
        assert "1 warning(s)" in summary

        # Check diagnostic serialization
        d1_dict = d1.to_dict()
        assert d1_dict["code"] == "E0602"
        assert d1_dict["source"] == "pylint"

    def test_multiple_diagnostics_same_file(self):
        """Multiple diagnostics in same file."""
        diags = [
            Diagnostic("test.py", i, message=f"Issue {i}")
            for i in range(1, 11)
        ]
        result = DiagnosticResult(success=False, diagnostics=diags, tool="checker")
        assert result.error_count == 10

    def test_diagnostic_formatting_variants(self):
        """Test different diagnostic formatting variants."""
        # Error without code
        d1 = Diagnostic("a.py", 1, severity=DiagnosticSeverity.ERROR, message="Error")
        assert "[" not in d1.format()

        # Warning with code
        d2 = Diagnostic(
            "b.py", 2, severity=DiagnosticSeverity.WARNING, message="Warn", code="W001"
        )
        assert "[W001]" in d2.format()
        assert "WARNING" in d2.format()

        # Info severity
        d3 = Diagnostic("c.py", 3, severity=DiagnosticSeverity.INFO, message="Info")
        assert "INFO" in d3.format()

        # Hint severity
        d4 = Diagnostic("d.py", 4, severity=DiagnosticSeverity.HINT, message="Hint")
        assert "HINT" in d4.format()
