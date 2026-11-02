"""Tests for benchmark_scenarios."""

from __future__ import annotations

import os
import subprocess
import sys
from unittest.mock import patch

from agentic_devtools.cli.checks.benchmark import benchmark_scenarios
from agentic_devtools.git_env import sanitize_git_environment

MODULE = "agentic_devtools.cli.checks.benchmark"


class TestBenchmarkScenarios:
    """Tests for measuring the three requested benchmark scenarios."""

    @patch(f"{MODULE}.subprocess.run")
    @patch(f"{MODULE}.run_one_coverage", return_value=(True, "ok"))
    def test_measures_small_giant_and_full_suite(self, mock_coverage, mock_run, tmp_path, monkeypatch):
        monkeypatch.setenv("GIT_DIR", "sentinel")
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout="200 passed", stderr="")

        rows = benchmark_scenarios(tmp_path)

        assert [row[0] for row in rows] == ["Typical small change", "Giant-file change", "Full suite"]
        assert all(result == "passed" for _, _, result in rows)
        assert mock_coverage.call_count == 2
        assert "GIT_DIR" not in mock_run.call_args.kwargs["env"]
        mock_run.assert_called_once_with(
            [sys.executable, "-m", "pytest", "-o", "addopts=", "-q"],
            cwd=tmp_path,
            capture_output=True,
            text=True,
            timeout=7200,
            shell=False,
            env=sanitize_git_environment(os.environ),
        )

    @patch(f"{MODULE}.subprocess.run")
    @patch(f"{MODULE}.run_one_coverage", return_value=(False, "failed"))
    def test_records_coverage_and_suite_failures(self, _mock_coverage, mock_run, tmp_path):
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=2, stdout="", stderr="")

        rows = benchmark_scenarios(tmp_path)

        assert [row[2] for row in rows] == ["failed", "failed", "failed (exit 2)"]

    @patch(f"{MODULE}.subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="pytest", timeout=7200))
    @patch(f"{MODULE}.run_one_coverage", return_value=(True, "ok"))
    def test_records_full_suite_timeout(self, _mock_coverage, _mock_run, tmp_path):
        rows = benchmark_scenarios(tmp_path)

        assert rows[-1][2] == "timed out after 7200s"

    @patch(f"{MODULE}.subprocess.run")
    @patch(f"{MODULE}.run_one_coverage", return_value=(True, "ok"))
    @patch(f"{MODULE}.Path.cwd")
    def test_defaults_to_current_directory(self, mock_cwd, mock_coverage, mock_run, tmp_path):
        mock_cwd.return_value = tmp_path
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")

        benchmark_scenarios()

        assert all(call.kwargs["cwd"] == tmp_path for call in mock_coverage.call_args_list)
        assert mock_run.call_args.kwargs["cwd"] == tmp_path
