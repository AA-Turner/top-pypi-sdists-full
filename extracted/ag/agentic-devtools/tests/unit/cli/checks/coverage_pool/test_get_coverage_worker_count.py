"""Tests for get_coverage_worker_count."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.checks.coverage_pool import get_coverage_worker_count


class TestGetCoverageWorkerCount:
    """Tests for selecting bounded coverage concurrency."""

    def test_no_sources_uses_no_workers(self):
        assert get_coverage_worker_count(0, env={"AGDT_CHECKS_COVERAGE_WORKERS": "2"}) == 0

    def test_invalid_environment_value_raises_when_no_sources(self):
        with pytest.raises(ValueError, match="positive integer"):
            get_coverage_worker_count(0, env={"AGDT_CHECKS_COVERAGE_WORKERS": "invalid"})

    def test_default_uses_at_most_four_workers(self):
        assert get_coverage_worker_count(10, env={}, cpu_count=8) == 4

    def test_environment_value_is_respected_and_capped_by_sources(self):
        assert (
            get_coverage_worker_count(
                2,
                env={"AGDT_CHECKS_COVERAGE_WORKERS": "6"},
                cpu_count=8,
            )
            == 2
        )

    def test_environment_value_can_reduce_concurrency(self):
        assert (
            get_coverage_worker_count(
                5,
                env={"AGDT_CHECKS_COVERAGE_WORKERS": "2"},
                cpu_count=8,
            )
            == 2
        )

    def test_environment_value_is_capped_by_cpu_budget(self):
        assert (
            get_coverage_worker_count(
                10,
                env={"AGDT_CHECKS_COVERAGE_WORKERS": "99"},
                cpu_count=4,
            )
            == 4
        )

    def test_invalid_environment_value_raises(self):
        with pytest.raises(ValueError, match="positive integer"):
            get_coverage_worker_count(1, env={"AGDT_CHECKS_COVERAGE_WORKERS": "fast"})

    def test_nonpositive_environment_value_raises(self):
        with pytest.raises(ValueError, match="positive integer"):
            get_coverage_worker_count(1, env={"AGDT_CHECKS_COVERAGE_WORKERS": "0"})

    def test_negative_source_count_raises(self):
        with pytest.raises(ValueError, match="source_count"):
            get_coverage_worker_count(-1, env={})

    def test_default_environment_uses_cpu_count(self, monkeypatch):
        monkeypatch.delenv("AGDT_CHECKS_COVERAGE_WORKERS", raising=False)
        assert get_coverage_worker_count(3, cpu_count=2) == 2

    def test_missing_cpu_count_uses_one_worker(self, monkeypatch):
        monkeypatch.delenv("AGDT_CHECKS_COVERAGE_WORKERS", raising=False)
        monkeypatch.setattr("agentic_devtools.cli.checks.coverage_pool.os.cpu_count", lambda: None)
        assert get_coverage_worker_count(3) == 1
