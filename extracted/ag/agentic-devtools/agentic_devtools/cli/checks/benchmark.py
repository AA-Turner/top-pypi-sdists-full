"""Reproducible benchmarks for targeted-check coverage scenarios."""

from __future__ import annotations

import os
import platform
import subprocess
import sys
import time
from collections.abc import Sequence
from pathlib import Path

from agentic_devtools.cli.checks.tests import run_one_coverage
from agentic_devtools.git_env import sanitize_git_environment

BenchmarkRow = tuple[str, float, str]
_COVERAGE_SCENARIOS = (
    ("Typical small change", "agentic_devtools/cli/checks/lint.py"),
    ("Giant-file change", "agentic_devtools/cli/ci/github_provider.py"),
)


def render_markdown(rows: Sequence[BenchmarkRow], *, hardware: str) -> str:
    """Render benchmark measurements as a Markdown table."""
    lines = [
        f"Hardware: {hardware.replace('|', '\\|')}",
        "",
        "| Scenario | Seconds | Result |",
        "|---|---:|---|",
    ]
    lines.extend(f"| {name} | {elapsed:.2f} | {result.replace('|', '\\|')} |" for name, elapsed, result in rows)
    return "\n".join(lines)


def benchmark_scenarios(workspace: Path | None = None) -> list[BenchmarkRow]:
    """Measure each scenario once; the full-suite pytest run is timing-only, not gate validation."""
    root = workspace or Path.cwd()
    rows: list[BenchmarkRow] = []
    for name, source_file in _COVERAGE_SCENARIOS:
        started = time.perf_counter()
        passed, _ = run_one_coverage(source_file, cwd=root, coverage_workers=1)
        rows.append((name, time.perf_counter() - started, "passed" if passed else "failed"))

    started = time.perf_counter()
    try:
        # This direct pytest subprocess is measurement-only; it does not replace the targeted gate.
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-o", "addopts=", "-q"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=7200,
            shell=False,
            env=sanitize_git_environment(os.environ),
        )
    except subprocess.TimeoutExpired:
        suite_result = "timed out after 7200s"
    else:
        suite_result = "passed" if result.returncode == 0 else f"failed (exit {result.returncode})"
    rows.append(("Full suite", time.perf_counter() - started, suite_result))
    return rows


def main() -> int:
    """Run the benchmark scenarios and print their Markdown results."""
    rows = benchmark_scenarios()
    hardware = f"{platform.platform()}, {platform.processor() or 'unknown CPU'}, {os.cpu_count() or 1} logical CPUs"
    print(render_markdown(rows, hardware=hardware))
    return 0 if all(result == "passed" for _, _, result in rows) else 1
