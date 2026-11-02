"""Tests for benchmark main."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.cli.checks.benchmark import main

MODULE = "agentic_devtools.cli.checks.benchmark"


class TestMain:
    """Tests for benchmark CLI behavior."""

    @patch(f"{MODULE}.benchmark_scenarios", return_value=[("Full suite", 2.0, "passed")])
    def test_success_prints_table(self, _mock_benchmarks, capsys):
        assert main() == 0
        assert "| Full suite | 2.00 | passed |" in capsys.readouterr().out

    @patch(f"{MODULE}.benchmark_scenarios", return_value=[("Full suite", 2.0, "failed")])
    def test_failure_returns_nonzero(self, _mock_benchmarks):
        assert main() == 1
