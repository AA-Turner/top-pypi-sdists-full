"""Tests for the gap-stage retry helper in `evals/harness._run_gap_with_retry`.

Per DECISIONS 2026-05-09 ("Per-metric noise-floor calibration") the
gap agent on Haiku 4.5 hits ~21% validator-rejection rate. The retry
helper converts most of those into successful runs without changing
the validator discipline. These tests cover the three retry outcomes
(first-try success, retry success, both fail) by monkeypatching the
underlying subprocess call so no real LLM is invoked.
"""

from __future__ import annotations

from pathlib import Path

import evals.harness as harness
import pytest


def test_run_gap_with_retry_returns_zero_when_first_attempt_succeeds(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """First-attempt success — no retry, single _run_efterlev call."""
    calls: list[list[str]] = []

    def fake(args: list[str], cwd: Path) -> int:
        calls.append(args)
        return 0

    monkeypatch.setattr(harness, "_run_efterlev", fake)
    exit_code = harness._run_gap_with_retry(tmp_path)
    assert exit_code == 0
    assert len(calls) == 1, f"expected 1 call, got {len(calls)}"
    assert calls[0] == ["agent", "gap", "--target", str(tmp_path)]


def test_run_gap_with_retry_returns_zero_when_second_attempt_succeeds(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """First-attempt failure, second-attempt success — retry kicks in,
    final return is the second attempt's exit code (0).
    Stderr should mention the retry so reviewers see what happened.
    """
    exit_codes = iter([1, 0])
    call_count = {"n": 0}

    def fake(args: list[str], cwd: Path) -> int:
        call_count["n"] += 1
        return next(exit_codes)

    monkeypatch.setattr(harness, "_run_efterlev", fake)
    exit_code = harness._run_gap_with_retry(tmp_path)
    assert exit_code == 0
    assert call_count["n"] == 2

    captured = capsys.readouterr()
    assert "retrying once" in captured.err
    assert "DECISIONS 2026-05-09" in captured.err


def test_run_gap_with_retry_returns_second_failure_code_when_both_attempts_fail(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Both attempts fail — return the SECOND attempt's exit code (the
    most recent failure, since callers care about the final state).
    """
    exit_codes = iter([1, 2])
    call_count = {"n": 0}

    def fake(args: list[str], cwd: Path) -> int:
        call_count["n"] += 1
        return next(exit_codes)

    monkeypatch.setattr(harness, "_run_efterlev", fake)
    exit_code = harness._run_gap_with_retry(tmp_path)
    assert exit_code == 2  # second-attempt code, not first
    assert call_count["n"] == 2


def test_run_gap_with_retry_caps_at_two_attempts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """No more than 2 attempts ever — retry is single-shot, not unbounded.
    Guards against masking deterministic prompt or fixture issues.
    """
    call_count = {"n": 0}

    def always_fails(args: list[str], cwd: Path) -> int:
        call_count["n"] += 1
        return 99

    monkeypatch.setattr(harness, "_run_efterlev", always_fails)
    exit_code = harness._run_gap_with_retry(tmp_path)
    assert exit_code == 99
    assert call_count["n"] == 2, (
        "retry must cap at 2 attempts; deterministic failures should surface"
    )
