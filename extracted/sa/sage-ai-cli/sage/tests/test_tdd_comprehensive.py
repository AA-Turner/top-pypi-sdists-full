"""Comprehensive tests for sage/core/tdd.py - TDD enforcement."""

import pytest
from pathlib import Path
import tempfile
from unittest.mock import patch, MagicMock
import subprocess

from sage.core.tdd import (
    TDDResult,
    TDDEnforcer,
    get_tdd_enforcer,
    validate_code_write,
    configure_tdd,
    _tdd_enforcer,
)


# =============================================================================
# Tests for TDDResult dataclass
# =============================================================================


class TestTDDResult:
    """Tests for TDDResult dataclass."""

    def test_create_default(self):
        """Create with defaults."""
        result = TDDResult(passed=True)
        assert result.passed is True
        assert result.tests_run == 0
        assert result.tests_passed == 0
        assert result.tests_failed == 0
        assert result.coverage_percent == 0.0
        assert result.coverage_required == 100.0
        assert result.missing_test_file is False
        assert result.error is None
        assert result.output == ""
        assert result.files_tested == []

    def test_create_with_values(self):
        """Create with values."""
        result = TDDResult(
            passed=True,
            tests_run=10,
            tests_passed=9,
            tests_failed=1,
            coverage_percent=85.5,
            coverage_required=80.0,
            missing_test_file=False,
            error=None,
            output="Test output",
            files_tested=["main.py"],
        )
        assert result.tests_run == 10
        assert result.tests_passed == 9
        assert result.tests_failed == 1
        assert result.coverage_percent == 85.5
        assert "main.py" in result.files_tested

    def test_coverage_met_true(self):
        """Coverage met when above threshold."""
        result = TDDResult(passed=True, coverage_percent=100.0, coverage_required=100.0)
        assert result.coverage_met is True

    def test_coverage_met_false(self):
        """Coverage not met when below threshold."""
        result = TDDResult(passed=False, coverage_percent=80.0, coverage_required=100.0)
        assert result.coverage_met is False

    def test_all_tests_pass_true(self):
        """All tests pass when none failed."""
        result = TDDResult(passed=True, tests_run=5, tests_passed=5, tests_failed=0)
        assert result.all_tests_pass is True

    def test_all_tests_pass_false(self):
        """Not all tests pass when some failed."""
        result = TDDResult(passed=False, tests_run=5, tests_passed=4, tests_failed=1)
        assert result.all_tests_pass is False

    def test_all_tests_pass_no_tests(self):
        """No tests pass when none run."""
        result = TDDResult(passed=False, tests_run=0, tests_passed=0, tests_failed=0)
        assert result.all_tests_pass is False

    def test_summary_missing_test_file(self):
        """Summary for missing test file."""
        result = TDDResult(passed=False, missing_test_file=True)
        summary = result.summary()
        assert "TDD BLOCKED" in summary
        assert "No test file" in summary

    def test_summary_error(self):
        """Summary for error."""
        result = TDDResult(passed=False, error="Something went wrong")
        summary = result.summary()
        assert "TDD ERROR" in summary
        assert "Something went wrong" in summary

    def test_summary_tests_failed(self):
        """Summary for failed tests."""
        result = TDDResult(
            passed=False, tests_run=10, tests_passed=7, tests_failed=3
        )
        summary = result.summary()
        assert "TDD FAILED" in summary
        assert "3/10" in summary

    def test_summary_coverage_not_met(self):
        """Summary for insufficient coverage."""
        result = TDDResult(
            passed=False,
            tests_run=5,
            tests_passed=5,
            tests_failed=0,
            coverage_percent=85.0,
            coverage_required=100.0,
        )
        summary = result.summary()
        assert "TDD BLOCKED" in summary
        assert "Coverage" in summary
        assert "85.0%" in summary

    def test_summary_passed(self):
        """Summary for passing TDD."""
        result = TDDResult(
            passed=True,
            tests_run=5,
            tests_passed=5,
            tests_failed=0,
            coverage_percent=100.0,
            coverage_required=100.0,
        )
        summary = result.summary()
        assert "TDD PASSED" in summary
        assert "5 tests" in summary
        assert "100.0% coverage" in summary


# =============================================================================
# Tests for TDDEnforcer class constants
# =============================================================================


class TestTDDEnforcerConstants:
    """Tests for TDDEnforcer constants."""

    def test_code_extensions(self):
        """CODE_EXTENSIONS contains Python."""
        assert ".py" in TDDEnforcer.CODE_EXTENSIONS

    def test_skip_dirs(self):
        """SKIP_DIRS contains expected directories."""
        assert "tests" in TDDEnforcer.SKIP_DIRS
        assert "test" in TDDEnforcer.SKIP_DIRS
        assert "__pycache__" in TDDEnforcer.SKIP_DIRS
        assert ".git" in TDDEnforcer.SKIP_DIRS
        assert "node_modules" in TDDEnforcer.SKIP_DIRS
        assert "venv" in TDDEnforcer.SKIP_DIRS
        assert ".venv" in TDDEnforcer.SKIP_DIRS

    def test_test_patterns(self):
        """TEST_PATTERNS contains expected patterns."""
        assert "test_{name}.py" in TDDEnforcer.TEST_PATTERNS
        assert "{name}_test.py" in TDDEnforcer.TEST_PATTERNS


# =============================================================================
# Tests for TDDEnforcer initialization
# =============================================================================


class TestTDDEnforcerInit:
    """Tests for TDDEnforcer initialization."""

    def test_default_init(self):
        """Initialize with defaults."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "pyproject.toml").write_text("[project]")
            with patch.object(Path, "cwd", return_value=Path(tmpdir)):
                enforcer = TDDEnforcer()
                assert enforcer.coverage_threshold == 100.0
                assert enforcer.enabled is True
                assert enforcer.strict is True

    def test_custom_init(self):
        """Initialize with custom values."""
        with tempfile.TemporaryDirectory() as tmpdir:
            enforcer = TDDEnforcer(
                project_root=Path(tmpdir),
                coverage_threshold=80.0,
                enabled=False,
                strict=False,
            )
            assert enforcer.project_root == Path(tmpdir)
            assert enforcer.coverage_threshold == 80.0
            assert enforcer.enabled is False
            assert enforcer.strict is False


# =============================================================================
# Tests for _find_project_root method
# =============================================================================


class TestFindProjectRoot:
    """Tests for _find_project_root method."""

    def test_finds_pyproject(self):
        """Finds pyproject.toml."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "pyproject.toml").write_text("[project]")
            with patch.object(Path, "cwd", return_value=Path(tmpdir)):
                enforcer = TDDEnforcer()
                root = enforcer._find_project_root()
                assert (root / "pyproject.toml").exists()

    def test_finds_git(self):
        """Finds .git directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / ".git").mkdir()
            with patch.object(Path, "cwd", return_value=Path(tmpdir)):
                enforcer = TDDEnforcer()
                root = enforcer._find_project_root()
                assert (root / ".git").exists()


# =============================================================================
# Tests for should_enforce method
# =============================================================================


class TestShouldEnforce:
    """Tests for should_enforce method."""

    def test_disabled_returns_false(self):
        """Returns False when disabled."""
        enforcer = TDDEnforcer(enabled=False)
        result = enforcer.should_enforce(Path("main.py"))
        assert result is False

    def test_non_python_returns_false(self):
        """Returns False for non-Python files."""
        enforcer = TDDEnforcer()
        assert enforcer.should_enforce(Path("main.js")) is False
        assert enforcer.should_enforce(Path("config.yaml")) is False
        assert enforcer.should_enforce(Path("README.md")) is False

    def test_test_file_returns_false(self):
        """Returns False for test files."""
        enforcer = TDDEnforcer()
        assert enforcer.should_enforce(Path("test_main.py")) is False
        assert enforcer.should_enforce(Path("main_test.py")) is False

    def test_skip_dirs_returns_false(self):
        """Returns False for files in skip directories."""
        enforcer = TDDEnforcer()
        assert enforcer.should_enforce(Path("tests/helper.py")) is False
        assert enforcer.should_enforce(Path("__pycache__/main.cpython.pyc")) is False
        assert enforcer.should_enforce(Path("venv/lib/site.py")) is False

    def test_init_returns_false(self):
        """Returns False for __init__.py."""
        enforcer = TDDEnforcer()
        assert enforcer.should_enforce(Path("__init__.py")) is False
        assert enforcer.should_enforce(Path("src/__init__.py")) is False

    def test_conftest_returns_false(self):
        """Returns False for conftest.py."""
        enforcer = TDDEnforcer()
        assert enforcer.should_enforce(Path("conftest.py")) is False

    def test_normal_python_returns_true(self):
        """Returns True for normal Python files."""
        enforcer = TDDEnforcer()
        assert enforcer.should_enforce(Path("main.py")) is True
        assert enforcer.should_enforce(Path("src/module.py")) is True


# =============================================================================
# Tests for find_test_file method
# =============================================================================


class TestFindTestFile:
    """Tests for find_test_file method."""

    def test_finds_test_prefix_pattern(self):
        """Finds test_{name}.py pattern."""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "module.py"
            source.write_text("code")
            test = Path(tmpdir) / "test_module.py"
            test.write_text("tests")

            enforcer = TDDEnforcer(project_root=Path(tmpdir))
            result = enforcer.find_test_file(source)

            assert result == test

    def test_finds_test_suffix_pattern(self):
        """Finds {name}_test.py pattern."""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "module.py"
            source.write_text("code")
            test = Path(tmpdir) / "module_test.py"
            test.write_text("tests")

            enforcer = TDDEnforcer(project_root=Path(tmpdir))
            result = enforcer.find_test_file(source)

            assert result == test

    def test_finds_in_tests_directory(self):
        """Finds test in tests/ directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "module.py"
            source.write_text("code")
            tests_dir = Path(tmpdir) / "tests"
            tests_dir.mkdir()
            test = tests_dir / "test_module.py"
            test.write_text("tests")

            enforcer = TDDEnforcer(project_root=Path(tmpdir))
            result = enforcer.find_test_file(source)

            assert result == test

    def test_returns_none_when_not_found(self):
        """Returns None when no test file found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "module.py"
            source.write_text("code")

            enforcer = TDDEnforcer(project_root=Path(tmpdir))
            result = enforcer.find_test_file(source)

            assert result is None


# =============================================================================
# Tests for _parse_test_results method
# =============================================================================


class TestParseTestResults:
    """Tests for _parse_test_results method."""

    def test_parse_passed_only(self):
        """Parse output with only passed tests."""
        enforcer = TDDEnforcer()
        output = "=== 10 passed in 1.23s ==="
        total, passed, failed = enforcer._parse_test_results(output)
        assert total == 10
        assert passed == 10
        assert failed == 0

    def test_parse_passed_and_failed(self):
        """Parse output with passed and failed tests."""
        enforcer = TDDEnforcer()
        output = "=== 5 failed, 10 passed in 2.34s ==="
        total, passed, failed = enforcer._parse_test_results(output)
        assert total == 15
        assert passed == 10
        assert failed == 5

    def test_parse_with_errors(self):
        """Parse output with errors."""
        enforcer = TDDEnforcer()
        output = "=== 2 error, 3 failed, 5 passed in 1.00s ==="
        total, passed, failed = enforcer._parse_test_results(output)
        assert total == 10
        assert passed == 5
        assert failed == 5  # 3 failed + 2 error

    def test_parse_no_results(self):
        """Parse output with no test results."""
        enforcer = TDDEnforcer()
        output = "No tests found"
        total, passed, failed = enforcer._parse_test_results(output)
        assert total == 0
        assert passed == 0
        assert failed == 0


# =============================================================================
# Tests for _parse_coverage method
# =============================================================================


class TestParseCoverage:
    """Tests for _parse_coverage method."""

    def test_parse_coverage_line(self):
        """Parse coverage from output."""
        enforcer = TDDEnforcer()
        output = """
Name                     Stmts   Miss  Cover
--------------------------------------------
module.py                  50     10    80%
--------------------------------------------
TOTAL                      50     10    80%
"""
        coverage = enforcer._parse_coverage(output, "module.py")
        assert coverage == 80.0

    def test_parse_coverage_with_decimals(self):
        """Parse coverage with decimal percentage."""
        enforcer = TDDEnforcer()
        output = "module.py    50    5    90.5%"
        coverage = enforcer._parse_coverage(output, "module.py")
        assert coverage == 90.5

    def test_parse_coverage_not_found(self):
        """Returns 0.0 when file not found in output."""
        enforcer = TDDEnforcer()
        output = "other.py    50    5    90%"
        coverage = enforcer._parse_coverage(output, "module.py")
        assert coverage == 0.0


# =============================================================================
# Tests for run_tests method
# =============================================================================


class TestRunTests:
    """Tests for run_tests method."""

    @patch("subprocess.run")
    def test_run_tests_success(self, mock_run):
        """Run tests successfully."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="5 passed\nmodule.py 100%",
            stderr="",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "module.py"
            source.write_text("code")
            test = Path(tmpdir) / "test_module.py"
            test.write_text("tests")

            enforcer = TDDEnforcer(project_root=Path(tmpdir))
            result = enforcer.run_tests(source, test)

            assert result.passed is True
            assert result.tests_passed == 5

    @patch("subprocess.run")
    def test_run_tests_failure(self, mock_run):
        """Run tests with failures."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="2 failed, 3 passed\nmodule.py 60%",
            stderr="",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "module.py"
            source.write_text("code")
            test = Path(tmpdir) / "test_module.py"
            test.write_text("tests")

            enforcer = TDDEnforcer(project_root=Path(tmpdir))
            result = enforcer.run_tests(source, test)

            assert result.passed is False
            assert result.tests_failed == 2

    @patch("subprocess.run")
    def test_run_tests_timeout(self, mock_run):
        """Handle test timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="pytest", timeout=120)

        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "module.py"
            source.write_text("code")
            test = Path(tmpdir) / "test_module.py"
            test.write_text("tests")

            enforcer = TDDEnforcer(project_root=Path(tmpdir))
            result = enforcer.run_tests(source, test)

            assert result.passed is False
            assert "timed out" in result.error.lower()

    @patch("subprocess.run")
    def test_run_tests_exception(self, mock_run):
        """Handle exception during tests."""
        mock_run.side_effect = Exception("Something went wrong")

        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "module.py"
            source.write_text("code")
            test = Path(tmpdir) / "test_module.py"
            test.write_text("tests")

            enforcer = TDDEnforcer(project_root=Path(tmpdir))
            result = enforcer.run_tests(source, test)

            assert result.passed is False
            assert "Something went wrong" in result.error


# =============================================================================
# Tests for validate_write method
# =============================================================================


class TestValidateWrite:
    """Tests for validate_write method."""

    def test_skip_non_enforced_file(self):
        """Skip validation for non-enforced files."""
        enforcer = TDDEnforcer()
        result = enforcer.validate_write(Path("README.md"), "content")
        assert result.passed is True
        assert "not required" in result.output

    def test_missing_test_file_strict(self):
        """Fail when test file missing in strict mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "module.py"
            source.write_text("code")

            enforcer = TDDEnforcer(project_root=Path(tmpdir), strict=True)
            result = enforcer.validate_write(source, "content")

            assert result.passed is False
            assert result.missing_test_file is True

    def test_missing_test_file_non_strict(self):
        """Pass when test file missing in non-strict mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "module.py"
            source.write_text("code")

            enforcer = TDDEnforcer(project_root=Path(tmpdir), strict=False)
            result = enforcer.validate_write(source, "content")

            assert result.passed is True
            assert result.missing_test_file is True

    @patch.object(TDDEnforcer, "run_tests")
    def test_runs_tests_when_found(self, mock_run_tests):
        """Runs tests when test file found."""
        mock_run_tests.return_value = TDDResult(passed=True)

        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "module.py"
            source.write_text("code")
            test = Path(tmpdir) / "test_module.py"
            test.write_text("tests")

            enforcer = TDDEnforcer(project_root=Path(tmpdir))
            result = enforcer.validate_write(source, "content")

            mock_run_tests.assert_called_once()
            assert result.passed is True


# =============================================================================
# Tests for module-level functions
# =============================================================================


class TestModuleFunctions:
    """Tests for module-level functions."""

    def test_get_tdd_enforcer(self):
        """get_tdd_enforcer returns TDDEnforcer instance."""
        # Reset global
        import sage.core.tdd
        sage.core.tdd._tdd_enforcer = None

        enforcer = get_tdd_enforcer()
        assert isinstance(enforcer, TDDEnforcer)

        # Same instance on second call
        enforcer2 = get_tdd_enforcer()
        assert enforcer is enforcer2

    def test_validate_code_write(self):
        """validate_code_write delegates to enforcer."""
        import sage.core.tdd
        sage.core.tdd._tdd_enforcer = None

        result = validate_code_write(Path("README.md"), "content")
        assert isinstance(result, TDDResult)

    def test_configure_tdd(self):
        """configure_tdd creates new enforcer with settings."""
        import sage.core.tdd

        with tempfile.TemporaryDirectory() as tmpdir:
            configure_tdd(
                enabled=False,
                coverage_threshold=80.0,
                strict=False,
                project_root=Path(tmpdir),
            )

            enforcer = sage.core.tdd._tdd_enforcer
            assert enforcer.enabled is False
            assert enforcer.coverage_threshold == 80.0
            assert enforcer.strict is False
            assert enforcer.project_root == Path(tmpdir)


# =============================================================================
# Integration tests
# =============================================================================


class TestTDDIntegration:
    """Integration tests for TDD module."""

    def test_full_workflow(self):
        """Full TDD validation workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a module and test file
            source = Path(tmpdir) / "module.py"
            source.write_text("def add(a, b): return a + b")
            
            test = Path(tmpdir) / "test_module.py"
            test.write_text("""
from module import add

def test_add():
    assert add(1, 2) == 3
""")

            enforcer = TDDEnforcer(project_root=Path(tmpdir))

            # Should enforce
            assert enforcer.should_enforce(source) is True

            # Should find test file
            found_test = enforcer.find_test_file(source)
            assert found_test == test

    def test_result_summary_variations(self):
        """Test all summary variations."""
        # All pass
        result1 = TDDResult(
            passed=True, tests_run=5, tests_passed=5, coverage_percent=100.0
        )
        assert "PASSED" in result1.summary()

        # Failed tests
        result2 = TDDResult(
            passed=False, tests_run=5, tests_passed=3, tests_failed=2
        )
        assert "FAILED" in result2.summary()

        # Coverage not met
        result3 = TDDResult(
            passed=False,
            tests_run=5,
            tests_passed=5,
            tests_failed=0,
            coverage_percent=80.0,
            coverage_required=100.0,
        )
        assert "BLOCKED" in result3.summary()
        assert "Coverage" in result3.summary()

        # Missing test file
        result4 = TDDResult(passed=False, missing_test_file=True)
        assert "BLOCKED" in result4.summary()
        assert "No test file" in result4.summary()

        # Error
        result5 = TDDResult(passed=False, error="Import error")
        assert "ERROR" in result5.summary()
