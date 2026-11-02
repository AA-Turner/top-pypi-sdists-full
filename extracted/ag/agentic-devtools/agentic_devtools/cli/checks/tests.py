"""Test execution for changed files and coverage checks.

All functions capture subprocess output and return ``(passed, output)``
tuples so they can be called from a thread pool without interleaving stdout.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from agentic_devtools.cli.checks.xdist_policy import get_changed_test_xdist_args, get_xdist_args
from agentic_devtools.git_env import sanitize_git_environment

# The GitHub provider's unit-test directory contains more than 1,000 tests;
# its full-module branch-coverage run can take several minutes on Windows.
_COVERAGE_TIMEOUT_SECONDS = 900
_PYTEST_COMMAND_LENGTH_LIMIT = 30_000


def run_changed_tests(
    test_files: list[str],
    *,
    cwd: str | Path | None = None,
) -> tuple[bool, str]:
    """Run pytest on specific test files (no coverage). Returns (passed, output)."""
    if not test_files:
        return True, ""
    cwd_str = str(cwd) if cwd else None
    command = [
        sys.executable,
        "-m",
        "pytest",
        "--no-cov",
        "-q",
        "-o",
        "addopts=",
        "-W",
        "ignore::DeprecationWarning",
        "-W",
        "ignore::PendingDeprecationWarning",
    ]
    batches: list[list[str]] = []
    current: list[str] = []
    for test_file in dict.fromkeys(test_files):
        candidate = [*command, *current, test_file]
        if len(subprocess.list2cmdline(candidate)) > _PYTEST_COMMAND_LENGTH_LIMIT and current:
            batches.append(current)
            current = []
            candidate = [*command, test_file]
        if len(subprocess.list2cmdline(candidate)) > _PYTEST_COMMAND_LENGTH_LIMIT:
            return False, f"FAIL: pytest target exceeds the command-length limit: {test_file}"
        current.append(test_file)
    batches.append(current)

    outputs = []
    passed = True
    for batch in batches:
        # Collect ancestor-level files before descendant suites: pytest can recreate
        # descendant collectors on revisiting a parent, invalidating conftest fixtures.
        paths = {target: (Path(cwd_str or ".") / target.split("::", 1)[0]).absolute() for target in batch}
        ordered_batch = sorted(batch, key=lambda target: (len(paths[target].parts), paths[target].is_dir()))
        xdist_args = get_changed_test_xdist_args(
            ordered_batch,
            cwd_str,
            cpu_count=os.cpu_count(),
            xdist_available=importlib.util.find_spec("xdist") is not None,
        )
        batch_command = [*command[:3], *xdist_args, *ordered_batch, *command[3:]]
        if xdist_args and len(subprocess.list2cmdline(batch_command)) > _PYTEST_COMMAND_LENGTH_LIMIT:
            batch_command = [*command[:3], *ordered_batch, *command[3:]]
        result = subprocess.run(
            batch_command,
            capture_output=True,
            text=True,
            cwd=cwd_str,
            env=sanitize_git_environment(os.environ),
        )
        passed = passed and result.returncode == 0
        output = result.stdout + result.stderr
        if output.strip():
            outputs.append(output.rstrip())
    return passed, "\n".join(outputs)


def _find_test_path(source_file: str, workspace: Path) -> str | None:
    """Find the test path for a source file (1:1:1 or legacy layout)."""
    if source_file == "agentic_devtools/_bundled_skills/skills/fingerprint.py":
        return str(workspace / "tests" / "scripts" / "fingerprint")
    relative = source_file.removeprefix("agentic_devtools/")
    relative_dir = relative.removesuffix(".py")
    unit_test_dir = workspace / "tests" / "unit" / relative_dir
    if unit_test_dir.is_dir():
        return str(unit_test_dir)

    basename = Path(source_file).stem
    legacy_test_file = workspace / "tests" / f"test_{basename}.py"
    if legacy_test_file.is_file():
        return str(legacy_test_file)

    return None


def run_one_coverage(
    source_file: str,
    *,
    cwd: str | Path | None = None,
    coverage_workers: int = 1,
) -> tuple[bool, str]:
    """Run 100% branch coverage check for a single source file.

    Returns ``(passed, output)``.
    """
    workspace = Path(cwd) if cwd else Path.cwd()
    source_module = source_file.replace("/", ".").replace("\\", ".").removesuffix(".py")
    test_path = _find_test_path(source_file, workspace)

    if test_path is None:
        return False, f"FAIL: No tests found for {source_file}"

    header = f"-- {source_file} -> {test_path} --"

    # Isolate coverage data file per subprocess to avoid PermissionError
    # when multiple pytest-cov processes run in parallel on Windows.
    env = sanitize_git_environment(os.environ)
    with tempfile.TemporaryDirectory(prefix="cov_") as cov_dir:
        env["COVERAGE_FILE"] = str(Path(cov_dir) / ".coverage")
        if not env.get("COVERAGE_CORE"):
            env["COVERAGE_CORE"] = "sysmon"

        pytest_args = get_xdist_args(Path(test_path), coverage_workers=coverage_workers)
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    test_path,
                    "-v",
                    "--tb=short",
                    "-o",
                    "addopts=",
                    "-p",
                    "no:cacheprovider",
                    # pytest-xdist creates a distinct subdirectory per worker under this job base.
                    f"--basetemp={Path(cov_dir) / 'pytest'}",
                    "-W",
                    "ignore::DeprecationWarning",
                    "-W",
                    "ignore::PendingDeprecationWarning",
                    *pytest_args,
                    f"--cov={source_module}",
                    "--cov-branch",
                    "--cov-report=term-missing",
                    "--cov-fail-under=100",
                ],
                capture_output=True,
                text=True,
                cwd=str(workspace),
                env=env,
                timeout=_COVERAGE_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired:
            return False, f"{header}\nFAIL: coverage timed out after {_COVERAGE_TIMEOUT_SECONDS}s"
    lines = [header, result.stdout.rstrip()]
    if result.stderr.strip():
        lines.append(result.stderr.rstrip())
    if result.returncode != 0:
        lines.append(f"FAIL: {source_file} — tests failing or < 100% coverage")
    return result.returncode == 0, "\n".join(lines)


def run_coverage_check(
    source_files: list[str],
    *,
    cwd: str | Path | None = None,
) -> tuple[int, int]:
    """Run per-file 100% branch coverage (sequential). Returns (total, failures).

    Prefer :func:`run_one_coverage` with a thread pool for parallel execution.
    """
    failures = 0
    total = len(source_files)

    for source_file in source_files:
        passed, output = run_one_coverage(source_file, cwd=cwd)
        print(output)
        if not passed:
            failures += 1

    return total, failures
