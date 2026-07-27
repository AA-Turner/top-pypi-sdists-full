"""Tests for the TDD loop.

The loop generates a failing test, then iterates impl + test until
green (no fixed retry cap, per user request) — with stuck detection
to prevent infinite loops on impossible tests.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

import pytest

from sage.core.spec_decomposer import Feature
from sage.core.tdd_loop import (
    FeatureResult,
    RoundResult,
    StuckTracker,
    run_feature_tdd,
)


class TestStuckTracker:
    def test_progress_resets_stuck_count(self) -> None:
        t = StuckTracker(threshold=3)
        t.record(failures=5)
        t.record(failures=3)
        assert not t.is_stuck()
        t.record(failures=2)
        assert not t.is_stuck()

    def test_flat_failures_eventually_marks_stuck(self) -> None:
        t = StuckTracker(threshold=3)
        t.record(failures=5)
        t.record(failures=5)
        t.record(failures=5)
        assert t.is_stuck()

    def test_increasing_failures_also_marks_stuck(self) -> None:
        t = StuckTracker(threshold=3)
        t.record(failures=5)
        t.record(failures=6)
        t.record(failures=7)
        assert t.is_stuck()

    def test_zero_failures_never_stuck(self) -> None:
        t = StuckTracker(threshold=3)
        t.record(failures=0)
        t.record(failures=0)
        t.record(failures=0)
        assert not t.is_stuck()  # 0 means green, not stuck


class TestRunFeatureTdd:
    def test_writes_test_file_before_impl(self, tmp_path: Path) -> None:
        # Track call order
        call_log: list[str] = []

        def fake_gen(prompt: str) -> str:
            # First call generates the test, subsequent calls the impl
            if "Write a failing test" in prompt:
                call_log.append("test")
                return "def test_x(): assert True"
            else:
                call_log.append("impl")
                return "def x(): return 1"

        def fake_runner(test_path: Path, impl_path: Path) -> tuple[bool, str, int]:
            return True, "1 passed", 0

        result = run_feature_tdd(
            Feature(name="x", description="d", layer="backend", acceptance=["a"]),
            impl_path=tmp_path / "impl.py",
            test_path=tmp_path / "test_x.py",
            generate=fake_gen,
            run_tests=fake_runner,
        )
        assert call_log[0] == "test", "test must be generated before impl"
        assert result.ok

    def test_returns_ok_when_tests_pass_first_try(self, tmp_path: Path) -> None:
        def fake_gen(prompt: str) -> str:
            return "x"

        def fake_runner(test_path: Path, impl_path: Path) -> tuple[bool, str, int]:
            return True, "1 passed", 0

        result = run_feature_tdd(
            Feature(name="x", description="d", layer="backend", acceptance=["a"]),
            impl_path=tmp_path / "impl.py",
            test_path=tmp_path / "test_x.py",
            generate=fake_gen,
            run_tests=fake_runner,
        )
        assert isinstance(result, FeatureResult)
        assert result.ok
        assert not result.stuck

    def test_iterates_on_failure_then_succeeds(self, tmp_path: Path) -> None:
        call_count = {"n": 0}

        def fake_gen(prompt: str) -> str:
            call_count["n"] += 1
            return "y"

        run_count = {"n": 0}

        def fake_runner(test_path: Path, impl_path: Path) -> tuple[bool, str, int]:
            run_count["n"] += 1
            # Fail twice, then succeed
            if run_count["n"] < 3:
                return False, "2 failed", 2
            return True, "passed", 0

        result = run_feature_tdd(
            Feature(name="x", description="d", layer="backend", acceptance=["a"]),
            impl_path=tmp_path / "impl.py",
            test_path=tmp_path / "test_x.py",
            generate=fake_gen,
            run_tests=fake_runner,
        )
        assert result.ok
        assert result.rounds > 1

    def test_marks_stuck_after_no_progress(self, tmp_path: Path) -> None:
        def fake_gen(prompt: str) -> str:
            return "x"

        def fake_runner(test_path: Path, impl_path: Path) -> tuple[bool, str, int]:
            # Always fail with same count → must mark stuck after threshold
            return False, "5 failed", 5

        result = run_feature_tdd(
            Feature(name="x", description="d", layer="backend", acceptance=["a"]),
            impl_path=tmp_path / "impl.py",
            test_path=tmp_path / "test_x.py",
            generate=fake_gen,
            run_tests=fake_runner,
            stuck_threshold=3,
        )
        assert not result.ok
        assert result.stuck
        assert result.failures == 5
