"""Tests for get_xdist_args."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.cli.checks.xdist_policy import get_xdist_args


class TestGetXdistArgs:
    """Tests for selecting pytest-xdist only for large mapped test paths."""

    def test_missing_test_path_stays_single_process(self, tmp_path):
        assert get_xdist_args(tmp_path / "missing", coverage_workers=1, cpu_count=8) == []

    def test_small_test_directory_stays_single_process(self, tmp_path):
        test_dir = tmp_path / "tests"
        test_dir.mkdir()
        for index in range(30):
            (test_dir / f"test_{index}.py").touch()

        assert get_xdist_args(test_dir, coverage_workers=1, cpu_count=8) == []

    def test_large_directory_uses_requested_distribution_and_budgeted_workers(self, tmp_path):
        test_dir = tmp_path / "tests"
        test_dir.mkdir()
        for index in range(31):
            (test_dir / f"test_{index}.py").touch()

        assert get_xdist_args(test_dir, coverage_workers=2, cpu_count=8) == [
            "-n",
            "3",
            "--dist",
            "loadfile",
        ]
        assert get_xdist_args(
            test_dir,
            coverage_workers=2,
            cpu_count=8,
            distribution="worksteal",
        ) == [
            "-n",
            "3",
            "--dist",
            "worksteal",
        ]

    def test_single_file_path_stays_single_process(self, tmp_path):
        test_file = tmp_path / "test_one.py"
        test_file.touch()

        assert get_xdist_args(test_file, coverage_workers=1, cpu_count=8) == []

    def test_budget_of_one_stays_single_process(self, tmp_path):
        test_dir = tmp_path / "tests"
        test_dir.mkdir()
        for index in range(31):
            (test_dir / f"test_{index}.py").touch()

        assert get_xdist_args(test_dir, coverage_workers=8, cpu_count=8) == []

    def test_unavailable_cpu_count_stays_single_process(self, tmp_path, monkeypatch):
        test_dir = tmp_path / "tests"
        test_dir.mkdir()
        for index in range(31):
            (test_dir / f"test_{index}.py").touch()
        monkeypatch.setattr("agentic_devtools.cli.checks.xdist_policy.os.cpu_count", lambda: None)

        assert get_xdist_args(test_dir, coverage_workers=1) == []

    def test_nonpositive_coverage_workers_raises(self, tmp_path):
        with pytest.raises(ValueError, match="coverage_workers"):
            get_xdist_args(Path(tmp_path), coverage_workers=0, cpu_count=8)
