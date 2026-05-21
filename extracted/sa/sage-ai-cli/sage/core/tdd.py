"""TDD (Test-Driven Development) enforcement for SAGE.

This module enforces TDD practices automatically during code execution:
- Runs tests after every code write
- Requires 100% coverage on modified files
- Blocks code changes that break tests or miss coverage

This is NOT a command - it's integrated into the execution cycle.
"""

from __future__ import annotations

import logging
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

from sage.core.procedural_workflow import (
    FailureLoopDetector,
    _detect_repetition,
)
from sage.core.shell import (
    DockerSandbox,
    _extract_scoped_prefix,
    _get_test_error_summary,
    _parse_test_output,
    _resolve_scoped_directory,
    execute_command as _execute_command,
)
from sage.core.validation import _find_actual_test_directory

logger = logging.getLogger(__name__)

# Global failure loop detector for TDD gates
_failure_loop_detector = FailureLoopDetector()

__all__ = [
    "TDDResult",
    "TDDEnforcer",
    "TDDGate",
    "get_tdd_enforcer",
    "validate_code_write",
    "configure_tdd",
    "_normalize_retry_signature",
    "_RetryProgressTracker",
]


@dataclass
class TDDResult:
    """Result of TDD validation."""

    passed: bool
    tests_run: int = 0
    tests_passed: int = 0
    tests_failed: int = 0
    coverage_percent: float = 0.0
    coverage_required: float = 100.0
    missing_test_file: bool = False
    error: str | None = None
    output: str = ""
    files_tested: list[str] = field(default_factory=list)

    @property
    def coverage_met(self) -> bool:
        """Check if coverage requirement is met."""
        return self.coverage_percent >= self.coverage_required

    @property
    def all_tests_pass(self) -> bool:
        """Check if all tests pass."""
        return self.tests_failed == 0 and self.tests_run > 0

    def summary(self) -> str:
        """Generate a summary string."""
        if self.missing_test_file:
            return "TDD BLOCKED: No test file found for modified code"
        if self.error:
            return f"TDD ERROR: {self.error}"
        if not self.all_tests_pass:
            return f"TDD FAILED: {self.tests_failed}/{self.tests_run} tests failed"
        if not self.coverage_met:
            return (
                f"TDD BLOCKED: Coverage {self.coverage_percent:.1f}% "
                f"< required {self.coverage_required:.1f}%"
            )
        return f"TDD PASSED: {self.tests_passed} tests, {self.coverage_percent:.1f}% coverage"


class TDDEnforcer:
    """Enforces TDD practices on code writes.

    Automatically validates that:
    1. Test files exist for modified code
    2. All tests pass after modification
    3. Code coverage meets threshold (default 100%)
    """

    # File extensions that require TDD enforcement
    CODE_EXTENSIONS = {".py"}

    # Directories to skip TDD enforcement
    SKIP_DIRS = {"tests", "test", "__pycache__", ".git", "node_modules", "venv", ".venv"}

    # Test file patterns
    TEST_PATTERNS = [
        "test_{name}.py",  # test_module.py
        "{name}_test.py",  # module_test.py
        "tests/test_{name}.py",  # tests/test_module.py
        "tests/{name}_test.py",  # tests/module_test.py
    ]

    def __init__(
        self,
        project_root: Path | None = None,
        coverage_threshold: float = 100.0,
        enabled: bool = True,
        strict: bool = True,
    ):
        """Initialize TDD enforcer.

        Args:
            project_root: Project root directory (auto-detected if None)
            coverage_threshold: Required coverage percentage (default 100%)
            enabled: Whether TDD enforcement is enabled
            strict: If True, block writes that fail TDD
        """
        self.project_root = project_root or self._find_project_root()
        self.coverage_threshold = coverage_threshold
        self.enabled = enabled
        self.strict = strict

    def _find_project_root(self) -> Path:
        """Find project root by looking for pyproject.toml or .git."""
        cwd = Path.cwd()
        for parent in [cwd, *cwd.parents]:
            if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
                return parent
        return cwd

    def should_enforce(self, filepath: Path) -> bool:
        """Check if TDD should be enforced for this file.

        Args:
            filepath: Path to the file being written

        Returns:
            True if TDD enforcement applies
        """
        if not self.enabled:
            return False

        # Only enforce for code files
        if filepath.suffix not in self.CODE_EXTENSIONS:
            return False

        # Skip test files themselves
        if filepath.name.startswith("test_") or filepath.name.endswith("_test.py"):
            return False

        # Skip files in excluded directories
        parts = filepath.parts
        for skip_dir in self.SKIP_DIRS:
            if skip_dir in parts:
                return False

        # Skip __init__.py files (usually empty or imports only)
        if filepath.name == "__init__.py":
            return False

        # Skip conftest.py files
        if filepath.name == "conftest.py":
            return False

        return True

    def find_test_file(self, source_file: Path) -> Path | None:
        """Find the corresponding test file for a source file.

        Args:
            source_file: Path to the source file

        Returns:
            Path to test file if found, None otherwise
        """
        name = source_file.stem
        parent = source_file.parent

        # Try patterns relative to source file
        for pattern in self.TEST_PATTERNS:
            test_name = pattern.format(name=name)
            test_path = parent / test_name
            if test_path.exists():
                return test_path

        # Try patterns relative to project root
        if self.project_root:
            for pattern in self.TEST_PATTERNS:
                test_name = pattern.format(name=name)
                test_path = self.project_root / test_name
                if test_path.exists():
                    return test_path

            # Try sage/tests/ directory
            test_path = self.project_root / "sage" / "tests" / f"test_{name}.py"
            if test_path.exists():
                return test_path

            # Try tests/sage/ directory
            test_path = self.project_root / "tests" / "sage" / f"test_{name}.py"
            if test_path.exists():
                return test_path

            # Try tests/ directory
            test_path = self.project_root / "tests" / f"test_{name}.py"
            if test_path.exists():
                return test_path

        return None

    def run_tests(self, source_file: Path, test_file: Path) -> TDDResult:
        """Run tests for a source file with coverage.

        Args:
            source_file: Path to the source file
            test_file: Path to the test file

        Returns:
            TDDResult with test and coverage information
        """
        # Get the module path for coverage
        try:
            relative_source = source_file.relative_to(self.project_root)
            cov_source = str(relative_source.parent)
        except ValueError:
            cov_source = str(source_file.parent)

        # Build pytest command with coverage
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            str(test_file),
            f"--cov={cov_source}",
            "--cov-report=term-missing",
            "--cov-report=",  # Suppress HTML
            "-v",
            "--tb=short",
            "-x",  # Stop on first failure
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=120,  # 2 minute timeout
                check=False,
            )

            # Parse results
            output = result.stdout + result.stderr
            tests_run, tests_passed, tests_failed = self._parse_test_results(output)
            coverage = self._parse_coverage(output, source_file.name)

            return TDDResult(
                passed=result.returncode == 0 and coverage >= self.coverage_threshold,
                tests_run=tests_run,
                tests_passed=tests_passed,
                tests_failed=tests_failed,
                coverage_percent=coverage,
                coverage_required=self.coverage_threshold,
                output=output,
                files_tested=[str(source_file)],
            )

        except subprocess.TimeoutExpired:
            return TDDResult(
                passed=False,
                error="Tests timed out (120s limit)",
                files_tested=[str(source_file)],
            )
        except Exception as e:
            return TDDResult(
                passed=False,
                error=str(e),
                files_tested=[str(source_file)],
            )

    def _parse_test_results(self, output: str) -> tuple[int, int, int]:
        """Parse test counts from pytest output."""
        # Look for "X passed, Y failed" pattern
        passed = 0
        failed = 0

        # Match "N passed"
        passed_match = re.search(r"(\d+) passed", output)
        if passed_match:
            passed = int(passed_match.group(1))

        # Match "N failed"
        failed_match = re.search(r"(\d+) failed", output)
        if failed_match:
            failed = int(failed_match.group(1))

        # Match "N error"
        error_match = re.search(r"(\d+) error", output)
        if error_match:
            failed += int(error_match.group(1))

        total = passed + failed
        return total, passed, failed

    def _parse_coverage(self, output: str, filename: str) -> float:
        """Parse coverage percentage from pytest-cov output."""
        for line in output.split("\n"):
            if filename in line:
                # Look for percentage in the line
                match = re.search(r"(\d+(?:\.\d+)?)\s*%", line)
                if match:
                    return float(match.group(1))
        return 0.0

    def validate_write(self, filepath: Path, _content: str) -> TDDResult:
        """Validate a file write against TDD requirements.

        This is the main entry point called after writing a file.

        Args:
            filepath: Path to the file that was written
            _content: Content that was written (unused)

        Returns:
            TDDResult indicating whether the write passes TDD requirements
        """
        # Check if TDD applies
        if not self.should_enforce(filepath):
            return TDDResult(
                passed=True,
                output="TDD enforcement not required for this file",
            )

        # Find test file
        test_file = self.find_test_file(filepath)
        if test_file is None:
            result = TDDResult(
                passed=not self.strict,
                missing_test_file=True,
                error=f"No test file found for {filepath.name}. Expected: test_{filepath.stem}.py",
            )
            return result

        # Run tests with coverage
        return self.run_tests(filepath, test_file)


# Global TDD enforcer instance
_tdd_enforcer: TDDEnforcer | None = None


def get_tdd_enforcer() -> TDDEnforcer:
    """Get or create the global TDD enforcer."""
    global _tdd_enforcer
    if _tdd_enforcer is None:
        _tdd_enforcer = TDDEnforcer()
    return _tdd_enforcer


def validate_code_write(filepath: str | Path, content: str) -> TDDResult:
    """Validate a code write against TDD requirements.

    This function is called automatically after writing code files.

    Args:
        filepath: Path to the file that was written
        content: Content that was written

    Returns:
        TDDResult with validation status
    """
    enforcer = get_tdd_enforcer()
    return enforcer.validate_write(Path(filepath), content)


def configure_tdd(
    enabled: bool = True,
    coverage_threshold: float = 100.0,
    strict: bool = True,
    project_root: Path | None = None,
) -> None:
    """Configure TDD enforcement settings.

    Args:
        enabled: Whether TDD enforcement is enabled
        coverage_threshold: Required coverage percentage
        strict: If True, block writes that fail TDD
        project_root: Project root directory
    """
    global _tdd_enforcer
    _tdd_enforcer = TDDEnforcer(
        project_root=project_root,
        coverage_threshold=coverage_threshold,
        enabled=enabled,
        strict=strict,
    )


class TDDGate:
    """Enforced TDD Gate - Code cannot proceed without verified test failure.

    The "Contract of Truth" between SAGE and the developer.

    CRITICAL ENFORCEMENT:
    - Collection errors (import errors, syntax errors) are treated as BLOCKING failures
    - Tests MUST pass (green) before proceeding to next task
    - No implementation code is accepted until red phase is verified
    """

    MAX_RETRIES = 10

    def __init__(self, sandbox: DockerSandbox):
        self.sandbox = sandbox
        self.red_verified = False
        self.green_verified = False
        self.test_cmd = "pytest -v"
        self.last_failure_output: str | None = None
        self.retry_count = 0
        self.last_error_type: str | None = None  # "collection", "failure", "timeout"

    def set_test_command(self, cmd: str) -> None:
        """Set the test command to use."""
        self.test_cmd = cmd

    def _resolve_test_command_context(self, cwd: Path) -> tuple[Path, str, str | None] | None:
        """Resolve an optional scoped test command into an execution cwd and inner command."""
        scope, inner_cmd = _extract_scoped_prefix(self.test_cmd)
        scoped_cwd = cwd
        if scope:
            scoped_cwd_result, error = _resolve_scoped_directory(scope, cwd)
            if error:
                return None
            assert scoped_cwd_result is not None
            scoped_cwd = scoped_cwd_result
        return scoped_cwd, inner_cmd.strip(), scope

    def _build_test_command_variants(self, command: str, cwd: Path) -> list[str]:
        """Return preferred fallback variants for pytest-based commands."""
        variants: list[str] = []

        def add(candidate: str) -> None:
            candidate = candidate.strip()
            if candidate and candidate not in variants:
                variants.append(candidate)

        add(command)

        venv_python = cwd / ".venv" / "bin" / "python"
        venv_pytest = cwd / ".venv" / "bin" / "pytest"

        if "python -m pytest" in command:
            if venv_python.exists():
                add(
                    command.replace(
                        "python -m pytest", f"{shlex.quote(str(venv_python))} -m pytest", 1
                    )
                )
            add(command.replace("python -m pytest", "pytest", 1))
            if venv_pytest.exists():
                add(command.replace("python -m pytest", shlex.quote(str(venv_pytest)), 1))
        elif re.match(r"^\s*pytest\b", command):
            if venv_pytest.exists():
                add(re.sub(r"^\s*pytest\b", shlex.quote(str(venv_pytest)), command, count=1))
            if venv_python.exists():
                add(
                    re.sub(
                        r"^\s*pytest\b",
                        f"{shlex.quote(str(venv_python))} -m pytest",
                        command,
                        count=1,
                    )
                )

        return variants

    @staticmethod
    def _should_retry_with_alternate_test_command(command: str, output: str) -> bool:
        """Return True when pytest failed for environment reasons worth retrying."""
        lower_output = output.lower()
        if "python -m pytest" in command and "no module named pytest" in lower_output:
            return True
        return bool(
            re.match(r"^\s*pytest\b", command)
            and (
                "no such file or directory: 'pytest'" in lower_output
                or "pytest: command not found" in lower_output
                or "/bin/sh: pytest: not found" in lower_output
            )
        )

    def verify_red(self, expected_failure: str | None = None) -> tuple[bool, str]:
        """RED Phase: Verify tests fail before implementation.

        SAGE cannot write implementation code until this passes.
        """
        if not self.sandbox.is_available():
            # Fallback to local execution if Docker not available
            return self._local_verify_red(expected_failure)

        is_red, message = self.sandbox.verify_test_failure(self.test_cmd, expected_failure)
        if is_red:
            self.red_verified = True
            self.last_failure_output = message
        return is_red, message

    def verify_green(self) -> tuple[bool, str]:
        """GREEN Phase: Verify tests pass after implementation.

        SAGE cannot proceed to refactor until this passes.
        CRITICAL: Also detects collection errors and treats them as failures.
        """
        if not self.red_verified:
            return (
                False,
                "❌ Cannot verify GREEN: RED phase not completed. Write failing tests first.",
            )

        if not self.sandbox.is_available():
            return self._local_verify_green()

        is_green, message = self.sandbox.verify_test_success(self.test_cmd)
        if is_green:
            self.green_verified = True
        return is_green, message

    def verify_tests_pass(self, cwd: Path) -> tuple[bool, str, dict]:
        """Verify tests pass with comprehensive error detection.

        This is the main enforcement function that handles:
        - Collection errors (import errors, syntax errors)
        - Test failures
        - Test errors

        Returns:
            (is_passing, message, parsed_output)
        """
        try:
            resolved = self._resolve_test_command_context(cwd)
            if resolved is None:
                return (
                    False,
                    "❌ TEST EXECUTION ERROR: Invalid scoped test command",
                    {"error": "invalid scoped test command"},
                )

            scoped_cwd, inner_cmd, scope = resolved
            last_result = None
            chosen_command = inner_cmd

            for candidate_cmd in self._build_test_command_variants(inner_cmd, scoped_cwd):
                chosen_command = candidate_cmd
                last_result = _execute_command(
                    candidate_cmd,
                    cwd=scoped_cwd,
                    timeout=300,
                    allow_shell=True,
                    validate=False,
                )
                if not self._should_retry_with_alternate_test_command(
                    candidate_cmd, last_result.output
                ):
                    break

            assert last_result is not None
            result = last_result
            output = result.output

            if chosen_command != inner_cmd:
                self.test_cmd = f"[cwd={scope}] {chosen_command}" if scope else chosen_command

            # Parse test output with enhanced error detection
            parsed = _parse_test_output(output)

            # CRITICAL: Check for collection errors FIRST
            if parsed["has_collection_errors"]:
                self.last_error_type = "collection"
                error_summary = _get_test_error_summary(output)
                return (
                    False,
                    f"❌ TEST COLLECTION ERRORS - BLOCKING\n{error_summary}\n\n"
                    f"Full output:\n{output[:2000]}",
                    parsed,
                )

            # Check for test failures
            if parsed["failed"] > 0 or parsed["errors"] > 0:
                self.last_error_type = "failure"
                return (
                    False,
                    f"❌ TESTS FAILING: {parsed['failed']} failed, {parsed['errors']} errors\n"
                    f"Failures: {', '.join(parsed['failure_details'][:5])}\n\n"
                    f"Output:\n{output[:1500]}",
                    parsed,
                )

            # All tests pass
            if result.returncode == 0 and parsed["passed"] > 0:
                self.green_verified = True
                self.last_error_type = None
                return (
                    True,
                    f"✅ ALL TESTS PASSED: {parsed['passed']} passed",
                    parsed,
                )

            # Edge case: no tests found
            if parsed["total"] == 0:
                actual_test_dir = _find_actual_test_directory(scoped_cwd)
                location_hint = (
                    f" Verified test directory: {actual_test_dir}/."
                    if actual_test_dir
                    else " Create or repair runnable tests in the project's real test directory."
                )
                return (
                    False,
                    "⚠️ NO TESTS FOUND - Cannot verify green phase. "
                    "The current validation command did not collect any runnable tests."
                    + location_hint,
                    parsed,
                )

            return (
                False,
                f"❌ Unexpected test state: returncode={result.returncode}\n{output[:1000]}",
                parsed,
            )

        except subprocess.TimeoutExpired:
            self.last_error_type = "timeout"
            # Feed timeout into failure loop detector
            is_loop = _failure_loop_detector.record_error("TEST TIMEOUT: Tests took too long")

            # P1-D: If we're in a failure loop, indicate this
            if is_loop:
                _, loop_reason = _failure_loop_detector.is_in_loop()
                return (
                    False,
                    f"❌ FAILURE LOOP DETECTED: {loop_reason}. "
                    "Stopping to prevent infinite retry spiral.",
                    {"timeout": True, "failure_loop": True, "loop_reason": loop_reason},
                )

            return (
                False,
                "❌ TEST TIMEOUT: Tests took too long to complete. "
                "Check for infinite loops or blocking operations.",
                {"timeout": True},
            )
        except Exception as e:
            # Feed execution errors (including parser crashes) into failure loop detector
            # This catches KeyError, AttributeError, etc. from parser contract mismatches
            error_str = str(e)
            is_loop = _failure_loop_detector.record_error(f"TEST EXECUTION ERROR: {error_str}")

            # P1-D: If we're in a failure loop, indicate this in the error message
            # so retry logic can stop immediately
            if is_loop:
                _, loop_reason = _failure_loop_detector.is_in_loop()
                return (
                    False,
                    f"❌ FAILURE LOOP DETECTED: {loop_reason}. "
                    f"Original error: {e}. "
                    "Stopping to prevent infinite retry spiral.",
                    {"error": error_str, "failure_loop": True, "loop_reason": loop_reason},
                )

            return (
                False,
                f"❌ TEST EXECUTION ERROR: {e}",
                {"error": error_str},
            )

    def run_tests(self, command: str | None = None, cwd: Path | None = None) -> tuple[bool, str]:
        """Convenience method to run tests and return (success, output)."""
        if command:
            self.set_test_command(command)
        # Use current directory if none provided
        target_cwd = cwd or Path.cwd()
        is_passing, message, _ = self.verify_tests_pass(target_cwd)
        return is_passing, message

    def reset(self) -> None:
        """Reset the TDD gate for a new cycle."""
        self.red_verified = False
        self.green_verified = False
        self.last_failure_output = None
        self.retry_count = 0
        self.last_error_type = None

    def increment_retry(self) -> int:
        """Increment retry count and return new count."""
        self.retry_count += 1
        return self.retry_count

    def can_retry(self) -> bool:
        return self.retry_count < self.MAX_RETRIES

    def _local_verify_red(self, _expected_failure: str | None = None) -> tuple[bool, str]:
        """Fallback: verify test failure locally."""
        try:
            result = subprocess.run(
                self.test_cmd.split(),
                capture_output=True,
                text=True,
                timeout=120,
                cwd=self.sandbox.cwd,
                check=False,
            )

            output = result.stderr + result.stdout

            # Check for collection errors - these also count as failures
            parsed = _parse_test_output(output)
            if parsed["has_collection_errors"]:
                self.red_verified = True
                self.last_failure_output = output
                self.last_error_type = "collection"
                return (
                    True,
                    "🔴 RED VERIFIED (local): Tests currently fail due to collection errors.\n"
                    f"{output[:500]}",
                )

            if result.returncode != 0:
                self.red_verified = True
                self.last_failure_output = output
                return (
                    True,
                    f"🔴 RED VERIFIED (local): Tests currently fail.\n{output[:500]}",
                )
            return False, "❌ TDD VIOLATION: Tests already passing!"
        except Exception as e:
            # Feed execution errors into failure loop detector
            _failure_loop_detector.record_error(f"LOCAL RED VERIFY ERROR: {e}")
            return False, f"❌ Could not run tests: {e}"

    def _local_verify_green(self) -> tuple[bool, str]:
        """Fallback: verify test success locally with enhanced error detection."""
        try:
            result = subprocess.run(
                self.test_cmd.split(),
                capture_output=True,
                text=True,
                timeout=120,
                cwd=self.sandbox.cwd,
                check=False,
            )
            output = result.stderr + result.stdout

            # Parse with enhanced error detection
            parsed = _parse_test_output(output)

            # CRITICAL: Collection errors are blocking
            if parsed["has_collection_errors"]:
                self.last_error_type = "collection"
                error_summary = _get_test_error_summary(output)
                return False, f"❌ COLLECTION ERRORS - MUST FIX BEFORE PROCEEDING\n{error_summary}"

            # We need to import _has_test_errors here or from shell
            from sage.core.shell import has_test_errors as _has_test_errors_local
            if result.returncode == 0 and not _has_test_errors_local(output):
                self.green_verified = True
                return True, f"✅ GREEN: All tests passing! ({parsed['passed']} passed)"

            return False, f"❌ Tests still failing.\n{output[:500]}"
        except Exception as e:
            # Feed execution errors into failure loop detector
            _failure_loop_detector.record_error(f"LOCAL GREEN VERIFY ERROR: {e}")
            return False, f"❌ Could not run tests: {e}"

    def get_status(self) -> str:
        """Get TDD gate status."""
        if not self.red_verified:
            return "🔴 RED: Write failing tests first"
        if not self.green_verified:
            return "🟡 IMPLEMENTATION: Make tests pass"
        return "🟢 GREEN: Ready to refactor"

    def get_retry_context(self) -> str:
        """Get context about retry state for smarter fixes."""
        context = (
            f"Retry attempt {self.retry_count} "
            "(continue until tests pass or a real no-progress blocker is detected)"
        )
        if self.last_error_type == "collection":
            context += "\nError type: COLLECTION ERRORS (import/syntax issues)"
            context += "\nFix priority: Check imports, verify module paths exist"
        elif self.last_error_type == "failure":
            context += "\nError type: TEST FAILURES (assertion failures)"
            context += "\nFix priority: Check test logic and implementation"
        elif self.last_error_type == "timeout":
            context += "\nError type: TIMEOUT (tests too slow)"
            context += "\nFix priority: Check for infinite loops, add timeouts"
        return context


def _normalize_retry_signature(text: str, *, limit: int = 400) -> str:
    """Normalize retry context so repeated failures can be compared reliably."""
    normalized = re.sub(r"\s+", " ", text).strip().lower()
    for marker in (" full output:", " output:", " recent errors:", " traceback"):
        idx = normalized.find(marker)
        if idx != -1:
            normalized = normalized[:idx].strip()
    return normalized[:limit] or "<empty>"


@dataclass
class _RetryProgressTracker:
    """Detect no-progress retry loops without imposing a hard retry cap."""

    failure_signatures: list[str] = field(default_factory=list)
    response_history: list[str] = field(default_factory=list)
    file_signatures: list[str] = field(default_factory=list)
    empty_write_streak: int = 0

    def observe_failure(self, message: str) -> None:
        """Record the current failure signature."""
        self.failure_signatures.append(_normalize_retry_signature(message))

    def observe_fix_attempt(
        self,
        *,
        response: str | None = None,
        files_written: list[str] | None = None,
    ) -> str | None:
        """Return a blocker reason when the fix loop is no longer making progress."""
        if response:
            if _detect_repetition(self.response_history, response):
                return "The model repeated the same fix response."
            self.response_history.append(response)

            if _failure_loop_detector.record_response(response):
                _, loop_reason = _failure_loop_detector.is_in_loop()
                return f"Failure loop detected: {loop_reason}"

        if files_written is not None:
            if not files_written:
                self.empty_write_streak += 1
                if self.empty_write_streak >= 2:
                    return "Consecutive fix attempts produced no file changes."
            else:
                self.empty_write_streak = 0

            file_signature = "|".join(sorted(dict.fromkeys(files_written))) or "<no-files>"
            if (
                self.file_signatures
                and self.file_signatures[-1] == file_signature
                and self._same_recent_failure(2)
            ):
                return "The same files were rewritten but the same test failure persisted."
            self.file_signatures.append(file_signature)

        if self._same_recent_failure(3):
            return "The same test failure repeated 3 times — no meaningful progress."

        return None

    def _same_recent_failure(self, count: int) -> bool:
        return (
            len(self.failure_signatures) >= count
            and len(set(self.failure_signatures[-count:])) == 1
        )
