"""CLI entry point for PR checks (agdt-pr-checks).

Single source of truth for both local pre-push hooks and CI targeted checks.
Both paths run identical validation — Python lint/format/type checks,
markdownlint on changed markdown, structure and drift guards execute in
parallel, while per-file coverage checks run sequentially for reliability.

Usage:
    python -m agentic_devtools.cli.checks              # format --check (CI default)
    python -m agentic_devtools.cli.checks --format-fix # format auto-fix (pre-push hook)

Exit codes:
    0  — all checks passed
    N  — N check(s) failed (1-9)
    10 — ruff reformatted files (auto-fixable; pre-push hook can auto-amend)
"""

from __future__ import annotations

import json
import os
import sys
import time
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

from agentic_devtools.cli.checks.changed_files import (
    DiffUnavailableError,
    find_consumer_test_paths,
    get_changed_files,
)
from agentic_devtools.cli.checks.lint import (
    format_check_files,
    format_fix_files,
    lint_files,
    markdownlint_files,
    mypy_check_files,
)
from agentic_devtools.cli.checks.setup_drift import (
    _is_setup_doc,
    _is_setup_source,
    check_drift,
    ensure_placeholder_docs,
)
from agentic_devtools.cli.checks.setup_drift_changed_files import _build_drift_file_list
from agentic_devtools.cli.checks.structure import validate_test_structure
from agentic_devtools.cli.checks.tests import _find_test_path, run_changed_tests, run_one_coverage


@dataclass
class _CheckResult:
    """Outcome of a single parallel check."""

    label: str
    passed: bool
    output: str
    duration: float = 0.0


# ---------------------------------------------------------------------------
# Check wrappers — each returns a _CheckResult with captured output
# ---------------------------------------------------------------------------


def _check_structure(cwd: Path) -> _CheckResult:
    t0 = time.monotonic()
    violations = validate_test_structure(cwd)
    dt = time.monotonic() - t0
    if violations:
        lines = [f"  - {v}" for v in violations]
        lines.append(f"FAIL: {len(violations)} violation(s)")
        return _CheckResult("Validate test structure", False, "\n".join(lines), dt)
    count = len(list((cwd / "tests" / "unit").rglob("test_*.py")))
    return _CheckResult(
        "Validate test structure",
        True,
        f"OK — {count} unit test file(s) validated, no violations found.",
        dt,
    )


def _check_lint(files: list[str], cwd: str) -> _CheckResult:
    t0 = time.monotonic()
    passed, output = lint_files(files, cwd=cwd)
    return _CheckResult("Lint changed files", passed, output, time.monotonic() - t0)


def _check_format(files: list[str], cwd: str) -> _CheckResult:
    t0 = time.monotonic()
    passed, output = format_check_files(files, cwd=cwd)
    return _CheckResult("ruff format --check", passed, output, time.monotonic() - t0)


def _check_mypy(files: list[str], cwd: str) -> _CheckResult:
    t0 = time.monotonic()
    passed, output = mypy_check_files(files, cwd=cwd)
    return _CheckResult("mypy type checking", passed, output, time.monotonic() - t0)


def _check_markdownlint(files: list[str], cwd: str) -> _CheckResult:
    t0 = time.monotonic()
    passed, output = markdownlint_files(files, cwd=cwd)
    return _CheckResult("markdownlint changed files", passed, output, time.monotonic() - t0)


def _check_coverage(source_file: str, cwd: Path) -> _CheckResult:
    t0 = time.monotonic()
    passed, output = run_one_coverage(source_file, cwd=cwd)
    return _CheckResult(f"Coverage: {source_file}", passed, output, time.monotonic() - t0)


def _check_extra_tests(test_files: list[str], cwd: Path) -> _CheckResult:
    t0 = time.monotonic()
    passed, output = run_changed_tests(test_files, cwd=cwd)
    return _CheckResult("Additional changed tests", passed, output, time.monotonic() - t0)


def _check_setup_expectations(cwd: Path) -> _CheckResult:
    """Validate setup expectations doc if setup-related files changed.

    Runs two sub-checks under one label:
    1. Content validation (existing ``validate_expectations()`` validator).
    2. Setup-expectations drift gate (new ``check_drift()`` pure function).
    """
    t0 = time.monotonic()

    # --- Gather changed files for content-validation relevance check ---
    content_patterns = [
        "agentic_devtools/cli/setup/**",
        "docs/setup-expectations/**",
        "scripts/validate_setup_expectations.py",
        ".github/instructions/setup-expectations.instructions.md",
    ]
    content_relevant: list[str] = []
    for pattern in content_patterns:
        try:
            content_relevant.extend(get_changed_files(pattern=pattern, cwd=cwd))
        except DiffUnavailableError:
            pass

    # --- Gather changed files for drift-gate relevance check ---
    # Filter to setup-source and setup-doc paths only so unrelated changes do
    # not incorrectly trigger the drift gate or the ensure_placeholder_docs I/O.
    _all_drift_files, deleted_paths = _build_drift_file_list(cwd)
    drift_files = sorted(f for f in _all_drift_files if _is_setup_source(f) or _is_setup_doc(f))

    # --- Skip entirely if nothing relevant changed ---
    dt = time.monotonic() - t0
    if not content_relevant and not drift_files:
        return _CheckResult(
            "Setup expectations",
            True,
            "Setup expectations check skipped: no relevant files changed.",
            dt,
        )

    errors: list[str] = []

    # --- Sub-check 1: content validation ---
    # Runs whenever any relevant change is detected (content_relevant or drift_files).
    # Drift files (D/R paths) are excluded from content_relevant by get_changed_files
    # --diff-filter=d, so the validator must run based on the combined trigger set.
    # (The early-return above ensures at least one of them is non-empty here.)
    from agentic_devtools.cli.setup.expectations_validator import validate_expectations

    content_result = validate_expectations(repo_root=cwd)
    if not content_result.passed:
        errors.extend(content_result.errors)

    # --- Sub-check 2: drift gate ---
    if drift_files:
        # FR-008 precondition
        docs_dir = cwd / "docs" / "setup-expectations"
        try:
            ensure_placeholder_docs(docs_dir, deleted_paths=deleted_paths)
        except (ValueError, OSError) as exc:
            errors.append(str(exc))

        drift_result = check_drift(drift_files)
        if not drift_result.passed:
            errors.append(drift_result.message)

    dt = time.monotonic() - t0
    if not errors:
        return _CheckResult("Setup expectations", True, "Setup expectations doc is consistent.", dt)

    output_lines = ["Setup expectations check failed:"]
    for err in errors:
        lines = err.splitlines()
        output_lines.append(f"  - {lines[0]}" if lines else "  -")
        output_lines.extend(f"    {line}" for line in lines[1:])
    return _CheckResult("Setup expectations", False, "\n".join(output_lines), dt)


def _check_skill_classification(cwd: Path) -> _CheckResult:
    """Validate every agdt.* file is classified in the fixture."""
    t0 = time.monotonic()
    fixture_path = cwd / "tests" / "fixtures" / "skill_classification_expected.json"

    from agentic_devtools.cli.checks.skill_classification import validate_skill_classification

    if not fixture_path.exists():
        dt = time.monotonic() - t0
        return _CheckResult(
            "Skill classification",
            True,
            "Skill classification check skipped: fixture not found.",
            dt,
        )

    try:
        result = validate_skill_classification(cwd, fixture_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        dt = time.monotonic() - t0
        return _CheckResult("Skill classification", False, f"Malformed fixture: {exc}", dt)

    dt = time.monotonic() - t0
    if result.is_valid:
        return _CheckResult(
            "Skill classification",
            True,
            f"OK — {result.validated_count} skill file(s) validated.",
            dt,
        )

    lines: list[str] = []
    for f in result.unregistered_files:
        lines.append(f"  unregistered: {f}")
    for m in result.mismatches:
        lines.append(f"  mismatch: {m.file} (expected={m.expected}, actual={m.actual})")
    for f in result.orphan_entries:
        lines.append(f"  orphan: {f}")
    for w in result.parse_warnings:
        lines.append(f"  warning: {w.file}: {w.message}")
    for e in result.parse_errors:
        lines.append(f"  error: {e.file}: {e.error}")
    total = (
        len(result.unregistered_files)
        + len(result.mismatches)
        + len(result.orphan_entries)
        + len(result.parse_warnings)
        + len(result.parse_errors)
    )
    lines.append(f"FAIL: {total} violation(s)")
    return _CheckResult("Skill classification", False, "\n".join(lines), dt)


def _check_customization_quality(files: list[str], cwd: Path) -> _CheckResult:
    """Validate the authoring quality of changed agent-customization Markdown.

    Violations are reported only against the changed files that fall inside the
    quality module's own selection predicate; the whole canonical corpus is
    still read by the module because the cross-file rules need it.
    """
    t0 = time.monotonic()

    from agentic_devtools.cli.checks.customization_quality import (
        check_customization_quality,
        is_selected,
    )

    selected = [f for f in files if is_selected(f)]
    if not selected:
        dt = time.monotonic() - t0
        return _CheckResult(
            "Customization quality",
            True,
            "Customization quality check skipped: no customization files changed.",
            dt,
        )

    try:
        result = check_customization_quality(cwd, selected)
    except (OSError, ValueError) as exc:
        dt = time.monotonic() - t0
        return _CheckResult("Customization quality", False, f"Unreadable customization file: {exc}", dt)

    dt = time.monotonic() - t0
    if result.is_valid:
        return _CheckResult(
            "Customization quality",
            True,
            f"OK — {len(result.checked_files)} customization file(s) validated.",
            dt,
        )

    lines = [f"  {v.rule}: {v.path}: {v.message}" for v in result.violations]
    lines.append(f"FAIL: {len(result.violations)} violation(s)")
    return _CheckResult("Customization quality", False, "\n".join(lines), dt)


def _max_workers() -> int:
    """Determine worker count: CPU count capped at 8."""
    return min(os.cpu_count() or 4, 8)


# ---------------------------------------------------------------------------
# Output condensing — strip verbose pytest/coverage noise from failure output
# ---------------------------------------------------------------------------

# Sections of pytest output that are noise for diagnosing failures.
_SKIP_PREFIXES = (
    "platform ",
    "cachedir: ",
    "rootdir: ",
    "configfile: ",
    "plugins: ",
    "collecting ",
    "collected ",
)


def _condense_output(raw: str) -> str:
    """Condense verbose check output by stripping common noise.

    Currently this helper:
    - Removes individual per-test "... PASSED" lines (with "::")
    - Removes common pytest metadata lines (platform/cachedir/rootdir/config/plugins/collecting/collected)
    - Collapses consecutive blank lines and trims trailing blanks

    It does not attempt to keep *only* failing/error lines; any other non-noise
    lines are preserved.
    """
    lines = raw.splitlines()
    kept: list[str] = []
    prev_blank = False

    for line in lines:
        stripped = line.strip()

        # Always keep blank lines (but collapse runs of blanks)
        if not stripped:
            if not prev_blank:
                kept.append("")
                prev_blank = True
            continue
        prev_blank = False

        # Skip individual PASSED test lines (e.g., "tests/unit/.../test_foo.py::TestX::test_y PASSED")
        if stripped.endswith(" PASSED") and "::" in stripped:
            continue

        # Skip pytest metadata noise
        if any(stripped.startswith(p) for p in _SKIP_PREFIXES):
            continue

        kept.append(line)

    # Remove trailing blank lines
    while kept and not kept[-1].strip():
        kept.pop()

    return "\n".join(kept)


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------


def _collect_extra_test_targets(
    changed_tests: list[str],
    changed_source: list[str],
    cwd: Path,
) -> list[str]:
    """Return changed test targets not already covered by per-file coverage.

    Includes changed ``test_*.py`` files whose source is not already covered by
    a per-file coverage run, plus consumer suites mapped from any changed shared
    test-support module (``conftest.py`` / underscore helpers), which are not
    runnable directly.
    """
    covered_dirs: set[Path] = set()
    covered_files: set[Path] = set()
    for src in changed_source:
        tp = _find_test_path(src, cwd)
        if tp:
            test_path = Path(tp)
            if not test_path.is_absolute():
                test_path = cwd / test_path
            test_path = test_path.resolve(strict=False)
            if test_path.suffix == ".py":
                covered_files.add(test_path)
            else:
                covered_dirs.add(test_path)

    def _is_covered(rel: str) -> bool:
        candidate = (cwd / rel).resolve(strict=False)
        if candidate in covered_files:
            return True
        return any(candidate == covered_dir or covered_dir in candidate.parents for covered_dir in covered_dirs)

    remaining: list[str] = []
    for test_file in changed_tests:
        if not _is_covered(test_file):
            remaining.append(test_file)

    # Shared support modules can't be run directly; map them to consumer suites.
    try:
        changed_support = get_changed_files(tests_support_only=True, cwd=cwd)
    except DiffUnavailableError:
        changed_support = []
    for support_file in changed_support:
        for consumer in find_consumer_test_paths(support_file, cwd=cwd):
            if consumer not in remaining and not _is_covered(consumer):
                remaining.append(consumer)
    return remaining


def _run_checks(cwd: Path, *, format_fix: bool = False) -> int:
    """Run all targeted checks, parallelising only independent work.

    Format auto-fix (``--format-fix``) runs first since it modifies files;
    lint / format-check / mypy / markdownlint / structure / drift checks run
    concurrently in a thread pool; per-file coverage checks run sequentially to
    avoid flaky subprocess coverage-report races.

    Returns the number of failures (0 = all passed).
    """
    # Force UTF-8 stdout so box-drawing characters survive on Windows cp1252 terminals.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    wall_t0 = time.monotonic()

    print("========================================")
    print("  Targeted Checks")
    print("========================================")

    # ── Gather changed files ──────────────────────────────────────────────
    try:
        changed_py = get_changed_files(cwd=cwd)
    except DiffUnavailableError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print("Cannot safely run targeted checks without changed-file detection.", file=sys.stderr)
        return 1
    try:
        changed_source = get_changed_files(source_only=True, cwd=cwd)
    except DiffUnavailableError:
        changed_source = []
    try:
        changed_tests = get_changed_files(tests_only=True, cwd=cwd)
    except DiffUnavailableError:
        changed_tests = []
    try:
        changed_md = get_changed_files(pattern="*.md", cwd=cwd)
    except DiffUnavailableError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print("Cannot safely run targeted checks without changed-file detection.", file=sys.stderr)
        return 1

    print(f"Changed Python files: {len(changed_py)} ({len(changed_source)} source, {len(changed_tests)} test)")
    print(f"Changed markdown files: {len(changed_md)}")

    # ── Format auto-fix (must complete before parallel phase) ─────────────
    if format_fix:
        print("\n── ruff format (auto-fix) ──")
        if changed_py:
            passed, output = format_fix_files(changed_py, cwd=str(cwd))
            print(output)
            if not passed:
                if output.startswith("ERROR:"):
                    print("\n❌ ruff format failed.")
                    return 1
                print("\n❌ Files were reformatted by ruff. Stage and amend, then push again.")
                return 10  # Distinct exit code: auto-fixable reformatting
        else:
            print("No Python files changed, skipping format.")

    # ── Build and submit parallel checks ──────────────────────────────────
    futures: list[Future[_CheckResult]] = []
    coverage_results: list[_CheckResult] = []

    with ThreadPoolExecutor(max_workers=_max_workers()) as pool:
        futures.append(pool.submit(_check_structure, cwd))

        if changed_py:
            futures.append(pool.submit(_check_lint, changed_py, str(cwd)))
            if not format_fix:
                futures.append(pool.submit(_check_format, changed_py, str(cwd)))
            futures.append(pool.submit(_check_mypy, changed_py, str(cwd)))

        if changed_md:
            futures.append(pool.submit(_check_markdownlint, changed_md, str(cwd)))

        # Additional changed test files not already covered by per-file coverage,
        # plus consumer suites mapped from any changed shared test-support module.
        remaining = _collect_extra_test_targets(changed_tests, changed_source, cwd)
        if remaining:
            futures.append(pool.submit(_check_extra_tests, remaining, cwd))

        # ── Setup expectations sync gate ──────────────────────────────────
        futures.append(pool.submit(_check_setup_expectations, cwd))

        # ── Skill classification fixture guard ────────────────────────────
        futures.append(pool.submit(_check_skill_classification, cwd))

        # ── Agent-customization authoring quality gate ────────────────────
        futures.append(pool.submit(_check_customization_quality, changed_md, cwd))

        # ── Progress counter ──────────────────────────────────────────────
        total = len(futures) + len(changed_source)
        print(f"\nRunning {total} check(s): parallel checks first, then sequential coverage...\n")
        completed = 0
        for _ in as_completed(futures):
            completed += 1
            print(f"  Progress: {completed}/{total}")

    for src in changed_source:
        print(f"  Starting coverage: {src}", flush=True)
        try:
            coverage_results.append(_check_coverage(src, cwd))
        except Exception as exc:  # noqa: BLE001
            msg = f"Unexpected exception: {exc!r}"
            coverage_results.append(_CheckResult(label=f"Coverage: {src}", passed=False, output=msg))
        completed += 1
        print(f"  Progress: {completed}/{total}")

    # ── Print results in submission order ─────────────────────────────────
    results: list[_CheckResult] = []
    for fut in futures:
        try:
            results.append(fut.result())
        except Exception as exc:  # noqa: BLE001
            msg = f"Unexpected exception: {exc!r}"
            results.append(_CheckResult(label="(unexpected error)", passed=False, output=msg))
    results.extend(coverage_results)
    failures = 0
    failed_details: list[_CheckResult] = []

    print()
    for r in results:
        icon = "✓" if r.passed else "✗"
        print(f"  {icon} {r.label} ({r.duration:.1f}s)")
        if not r.passed:
            failures += 1
            failed_details.append(r)

    # ── Detailed output for failures ──────────────────────────────────────
    if failed_details:
        # Save full verbose output to file for reference
        full_log_path = cwd / "check-output.txt"
        with open(full_log_path, "w", encoding="utf-8") as fh:
            for r in results:
                icon = "✓" if r.passed else "✗"
                fh.write(f"{icon} {r.label} ({r.duration:.1f}s)\n")
                if r.output.strip():
                    fh.write(r.output)
                    fh.write("\n\n")
        print(f"\n  Full output saved to: {full_log_path}")

        # Build condensed output for terminal and file
        condensed_lines: list[str] = []
        condensed_lines.append(f"{'─' * 60}")
        condensed_lines.append(f"  Detail for {failures} failed check(s):")
        condensed_lines.append(f"{'─' * 60}")
        for r in failed_details:
            condensed_lines.append(f"\n┌── {r.label} ──")
            for line in _condense_output(r.output).splitlines():
                condensed_lines.append(f"│ {line}")
            condensed_lines.append("└" + "─" * 40)
        condensed_text = "\n".join(condensed_lines)

        # Save condensed output to file
        condensed_log_path = cwd / "check-output-condensed.txt"
        with open(condensed_log_path, "w", encoding="utf-8") as fh:
            fh.write(condensed_text)
            fh.write("\n")
        print(f"  Condensed output saved to: {condensed_log_path}")

        # Show condensed output in terminal
        print(f"\n{condensed_text}")

    # ── Summary ───────────────────────────────────────────────────────────
    wall_dt = time.monotonic() - wall_t0
    print("\n========================================")
    if failures == 0:
        print(f"  All targeted checks passed! ({wall_dt:.1f}s)")
    else:
        print(f"  {failures} check(s) failed ({wall_dt:.1f}s)")
    print("========================================")

    # Exit code 10 is reserved for the "ruff reformatted files" signal.
    # Clamp non-format failure counts to 1–9 to avoid ambiguity.
    return 0 if failures == 0 else min(failures, 9)


def main() -> int:
    """Entry point for ``python -m agentic_devtools.cli.checks``."""
    cwd = Path.cwd()
    format_fix = "--format-fix" in sys.argv
    return _run_checks(cwd, format_fix=format_fix)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
