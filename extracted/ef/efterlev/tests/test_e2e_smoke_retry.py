"""Tests for the gap-stage retry helper in `scripts/e2e_smoke.py`.

Mirrors `tests/test_evals_harness_retry.py` for the parallel helper added
to `scripts/e2e_smoke.py` (PR follow-up to PR #191's harness retry; both
exist because PR #191's retry only covers `evals/harness.run_fixture()`).
Per DECISIONS 2026-05-09 the gap agent on Haiku 4.5 hits a non-trivial
validator-rejection rate; single retry converts most stochastic
rejections into successful runs without changing the validator
discipline.

Tests monkeypatch `_run_stage` so no real LLM is invoked.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


def _load_e2e_smoke():
    """Import scripts/e2e_smoke.py as a module (it lives outside `src/`).

    Must register the module in sys.modules BEFORE exec_module — otherwise
    the dataclasses runtime can't resolve field types via
    `sys.modules.get(cls.__module__).__dict__` (Python 3.12 internal in
    dataclasses.py). See the original failure shape:
    `AttributeError: 'NoneType' object has no attribute '__dict__'` at
    dataclasses.py:749.
    """
    smoke_path = Path(__file__).resolve().parent.parent / "scripts" / "e2e_smoke.py"
    spec = importlib.util.spec_from_file_location("e2e_smoke", smoke_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["e2e_smoke"] = module
    spec.loader.exec_module(module)
    return module


def _make_stage_result(module, exit_code: int):
    """Build a StageResult with the given exit code (other fields placeholder)."""
    return module.StageResult(
        stage="03-agent-gap",
        command=["uv", "run", "efterlev", "agent", "gap", "--target", "."],
        exit_code=exit_code,
        stdout="",
        stderr="" if exit_code == 0 else "error: stochastic Haiku rejection",
        duration_s=0.1,
    )


def test_retry_returns_first_result_when_first_attempt_succeeds(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """First-attempt success — no retry, single _run_stage call."""
    module = _load_e2e_smoke()
    calls: list[str] = []

    def fake(stage, command, workspace, outputs_dir):
        calls.append(stage)
        return _make_stage_result(module, 0)

    monkeypatch.setattr(module, "_run_stage", fake)
    result = module._run_gap_stage_with_retry(tmp_path, tmp_path)
    assert result.exit_code == 0
    assert len(calls) == 1


def test_retry_returns_second_result_when_second_attempt_succeeds(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """First-attempt failure, second succeeds — retry kicks in,
    final result is the second attempt's (exit 0)."""
    module = _load_e2e_smoke()
    exit_codes = iter([1, 0])
    call_count = {"n": 0}

    def fake(stage, command, workspace, outputs_dir):
        call_count["n"] += 1
        return _make_stage_result(module, next(exit_codes))

    monkeypatch.setattr(module, "_run_stage", fake)
    result = module._run_gap_stage_with_retry(tmp_path, tmp_path)
    assert result.exit_code == 0
    assert call_count["n"] == 2


def test_retry_returns_second_failure_code_when_both_attempts_fail(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Both attempts fail — return the SECOND attempt's exit code so callers
    see the most recent failure state, matching evals/harness retry shape."""
    module = _load_e2e_smoke()
    exit_codes = iter([1, 2])
    call_count = {"n": 0}

    def fake(stage, command, workspace, outputs_dir):
        call_count["n"] += 1
        return _make_stage_result(module, next(exit_codes))

    monkeypatch.setattr(module, "_run_stage", fake)
    result = module._run_gap_stage_with_retry(tmp_path, tmp_path)
    assert result.exit_code == 2
    assert call_count["n"] == 2


def test_retry_caps_at_two_attempts(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Cap at exactly 2 attempts — deterministic failures still surface
    rather than getting masked by unbounded retry."""
    module = _load_e2e_smoke()
    call_count = {"n": 0}

    def always_fails(stage, command, workspace, outputs_dir):
        call_count["n"] += 1
        return _make_stage_result(module, 99)

    monkeypatch.setattr(module, "_run_stage", always_fails)
    result = module._run_gap_stage_with_retry(tmp_path, tmp_path)
    assert result.exit_code == 99
    assert call_count["n"] == 2
