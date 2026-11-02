"""Tests for get_changed_test_xdist_args."""

from __future__ import annotations

from agentic_devtools.cli.checks.commands import _max_workers
from agentic_devtools.cli.checks.xdist_policy import get_changed_test_xdist_args


class TestGetChangedTestXdistArgs:
    """Tests for bounded changed-test worker selection."""

    def _targets(self, tmp_path, count=31):
        test_dir = tmp_path / "tests"
        test_dir.mkdir()
        for index in range(count):
            (test_dir / f"test_{index}.py").touch()
        return [str(test_dir)]

    def test_threshold_requires_more_than_thirty_files(self, tmp_path):
        assert (
            get_changed_test_xdist_args(self._targets(tmp_path, 30), tmp_path, cpu_count=13, xdist_available=True) == []
        )

    def test_worker_reserve_matches_check_pool_cap(self, tmp_path, monkeypatch):
        monkeypatch.setattr("agentic_devtools.cli.checks.commands.os.cpu_count", lambda: 8)
        assert _max_workers() == 8
        assert get_changed_test_xdist_args(self._targets(tmp_path), tmp_path, cpu_count=8, xdist_available=True) == []

    def test_worker_boundaries_and_four_worker_cap(self, tmp_path):
        targets = self._targets(tmp_path)
        assert get_changed_test_xdist_args(targets, tmp_path, cpu_count=10, xdist_available=True) == []
        assert get_changed_test_xdist_args(targets, tmp_path, cpu_count=11, xdist_available=True) == [
            "-n",
            "2",
            "--dist",
            "loadfile",
        ]
        assert get_changed_test_xdist_args(targets, None, cpu_count=13, xdist_available=True) == [
            "-n",
            "4",
            "--dist",
            "loadfile",
        ]

    def test_non_ancestor_directories_can_use_xdist(self, tmp_path):
        targets = []
        for name in ("first", "second"):
            test_dir = tmp_path / name
            test_dir.mkdir()
            for index in range(16):
                (test_dir / f"test_{index}.py").touch()
            targets.append(str(test_dir))

        assert get_changed_test_xdist_args(targets, tmp_path, cpu_count=11, xdist_available=True) == [
            "-n",
            "2",
            "--dist",
            "loadfile",
        ]

    def test_missing_cpu_or_xdist_plugin_stays_serial(self, tmp_path):
        targets = self._targets(tmp_path)
        for cpu_count in (None, 0, -1):
            assert get_changed_test_xdist_args(targets, tmp_path, cpu_count=cpu_count, xdist_available=True) == []
        assert get_changed_test_xdist_args(targets, tmp_path, cpu_count=13, xdist_available=False) == []

    def test_ancestor_and_descendant_targets_stay_serial(self, tmp_path):
        test_dir = tmp_path / "tests"
        test_dir.mkdir()
        for index in range(31):
            (test_dir / f"test_{index}.py").touch()
        child = test_dir / "test_0.py"

        assert (
            get_changed_test_xdist_args(
                [str(child) + "::test_case", str(test_dir)],
                tmp_path,
                cpu_count=13,
                xdist_available=True,
            )
            == []
        )
