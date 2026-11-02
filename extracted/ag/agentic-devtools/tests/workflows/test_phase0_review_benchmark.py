"""Canonical deterministic benchmark for Phase 0 review fixtures."""

from __future__ import annotations

import math
import os
import time
from pathlib import Path

import pytest

from agentic_devtools.cli.phase0_review.commands import run_review

_PERF_ENV = "AGDT_RUN_PHASE0_REVIEW_BENCHMARK"
_DEFAULT_P95_SECONDS = 60.0


def _fixture_cases() -> tuple[Path, list[Path]]:
    repo_root = Path(__file__).parents[2]
    fixture_root = repo_root / "tests" / "fixtures" / "reviewing-agent-benchmark"
    cases = sorted(path for path in fixture_root.iterdir() if path.is_dir())
    assert len(cases) >= 30
    return repo_root, cases


def test_phase0_review_benchmark_verdicts() -> None:
    """Verify benchmark-case verdicts.

    Default run: one approved fixture and one discrepancy fixture (fast smoke subset).
    Full cohort: set ``AGDT_RUN_PHASE0_REVIEW_BENCHMARK=1`` to exercise all 30 cases.
    """
    repo_root, cases = _fixture_cases()
    if os.environ.get(_PERF_ENV) != "1":
        discrepancy = next((case for case in cases if "discrepancy" in case.name), None)
        assert discrepancy is not None, "benchmark fixtures must include a discrepancy case"
        cases = [cases[0], discrepancy]
    for case in cases:
        report = run_review(
            repo_root=repo_root,
            input_path=case / "payload.json",
            integrity_path=case / "phase0-integrity.json",
        )
        expected = "CHANGES REQUESTED" if "discrepancy" in case.name else "APPROVED"
        assert f"## Verdict\n{expected}" in report


def test_phase0_review_benchmark_p95() -> None:
    """Assert the benchmark p95 ceiling only during explicit performance runs."""
    if os.environ.get(_PERF_ENV) != "1":
        pytest.skip(f"set {_PERF_ENV}=1 to run the opt-in performance assertion")

    repo_root, cases = _fixture_cases()
    durations: list[float] = []
    for case in cases:
        started = time.monotonic()
        run_review(
            repo_root=repo_root,
            input_path=case / "payload.json",
            integrity_path=case / "phase0-integrity.json",
        )
        durations.append(time.monotonic() - started)
    ordered = sorted(durations)
    p95 = ordered[math.ceil(0.95 * len(ordered)) - 1]
    assert p95 <= float(os.environ.get("AGDT_PHASE0_REVIEW_BENCHMARK_P95_SECONDS", _DEFAULT_P95_SECONDS))
