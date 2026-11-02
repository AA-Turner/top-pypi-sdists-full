"""Tests for run_coverage_pool."""

from __future__ import annotations

from threading import Event, get_ident

import pytest

from agentic_devtools.cli.checks.coverage_pool import run_coverage_pool


class TestRunCoveragePool:
    """Tests for concurrent per-file coverage results."""

    def test_empty_sources_returns_empty_results(self):
        assert run_coverage_pool([], lambda source: (True, source), max_workers=1) == []

    def test_returns_results_in_submission_order(self):
        second_finished = Event()

        def check(source: str) -> tuple[bool, str]:
            if source == "first":
                assert second_finished.wait(timeout=5)
            else:
                second_finished.set()
            return True, source

        results = run_coverage_pool(
            ["first", "second"],
            check,
            max_workers=2,
        )

        assert [result[:3] for result in results] == [
            ("first", True, "first"),
            ("second", True, "second"),
        ]
        assert all(result[3] >= 0 for result in results)

    def test_reports_start_and_completion_callbacks(self):
        main_thread_id = get_ident()
        started: dict[str, int] = {}
        completed: list[str] = []
        allow_first_to_finish = Event()

        def check(source: str) -> tuple[bool, str]:
            if source == "first":
                assert allow_first_to_finish.wait(timeout=5)
            return True, source

        def on_complete(result: tuple[str, bool, str, float]) -> None:
            completed.append(result[0])
            if result[0] == "second":
                allow_first_to_finish.set()

        def on_start(source: str) -> None:
            started[source] = get_ident()

        results = run_coverage_pool(
            ["first", "second"],
            check,
            max_workers=2,
            on_start=on_start,
            on_complete=on_complete,
        )

        assert set(started) == {"first", "second"}
        assert all(thread_id != main_thread_id for thread_id in started.values())
        assert completed == ["second", "first"]
        assert [result[0] for result in results] == ["first", "second"]

    def test_captures_unexpected_worker_exception(self):
        def check(source: str) -> tuple[bool, str]:
            if source == "broken":
                raise RuntimeError("coverage exploded")
            return True, "ok"

        assert run_coverage_pool(
            ["broken"],
            check,
            max_workers=1,
        ) == [
            ("broken", False, "Unexpected exception: RuntimeError('coverage exploded')", 0.0),
        ]

    @pytest.mark.parametrize("max_workers", [0, -1])
    def test_nonpositive_worker_count_raises(self, max_workers: int):
        with pytest.raises(ValueError, match="max_workers"):
            run_coverage_pool(["source.py"], lambda source: (True, ""), max_workers=max_workers)
