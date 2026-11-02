"""Batching tests for run_changed_tests."""

from __future__ import annotations

import subprocess
from collections import Counter
from subprocess import CompletedProcess
from unittest.mock import patch

from agentic_devtools.cli.checks.tests import run_changed_tests

MODULE = "agentic_devtools.cli.checks.tests"
XDIST_ARGS = ["-n", "4", "--dist", "loadfile"]


class TestRunChangedTestsBatches:
    @patch(f"{MODULE}.importlib.util.find_spec", return_value=object())
    @patch(f"{MODULE}.os.cpu_count", return_value=13)
    @patch(f"{MODULE}.subprocess.run")
    def test_xdist_batches_preserve_order_and_aggregate_failure(
        self, mock_run, _mock_cpus, _mock_xdist, tmp_path, monkeypatch
    ):
        test_dir = tmp_path / "tests"
        test_dir.mkdir()
        targets = []
        for index in range(62):
            name = f"test_{'x' * 40}_{index:02}.py"
            (test_dir / name).write_text("def test_placeholder():\n    pass\n", encoding="utf-8")
            targets.append(f"tests/{name}")

        monkeypatch.setattr(f"{MODULE}.sys.executable", "p")
        base_command = [
            "p",
            "-m",
            "pytest",
            "--no-cov",
            "-q",
            "-o",
            "addopts=",
            "-W",
            "ignore::DeprecationWarning",
            "-W",
            "ignore::PendingDeprecationWarning",
        ]
        first_xdist_command = [*base_command[:3], *XDIST_ARGS, *targets[:31], *base_command[3:]]
        command_limit = len(subprocess.list2cmdline(first_xdist_command))
        monkeypatch.setattr(f"{MODULE}._PYTEST_COMMAND_LENGTH_LIMIT", command_limit)
        assert len(subprocess.list2cmdline([*base_command, *targets[:32]])) > command_limit

        mock_run.side_effect = [
            CompletedProcess(args=[], returncode=1, stdout="first batch failed\n", stderr="diagnostic\n"),
            CompletedProcess(args=[], returncode=0, stdout="second batch passed\n", stderr=""),
        ]

        passed, output = run_changed_tests(targets, cwd=tmp_path)

        assert passed is False
        assert "first batch failed" in output
        assert "diagnostic" in output
        assert "second batch passed" in output
        assert mock_run.call_count == 2
        calls = [call.args[0] for call in mock_run.call_args_list]
        invoked_batches = []
        for command in calls:
            assert command[3:7] == XDIST_ARGS
            batch = command[7 : command.index("--no-cov")]
            assert len(batch) > 30
            invoked_batches.append(batch)

        offset = 0
        for batch in invoked_batches:
            expected_batch = targets[offset : offset + len(batch)]
            assert batch == expected_batch
            assert Counter(batch) == Counter(expected_batch)
            offset += len(batch)
        assert offset == len(targets)
        assert Counter(target for batch in invoked_batches for target in batch) == Counter(targets)
