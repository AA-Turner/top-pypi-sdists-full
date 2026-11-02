"""Tests for run_changed_tests."""

from __future__ import annotations

import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import patch

from agentic_devtools.cli.checks.tests import run_changed_tests

MODULE = "agentic_devtools.cli.checks.tests"


class TestRunChangedTests:
    """Tests for run_changed_tests."""

    @patch(f"{MODULE}.subprocess.run")
    def test_child_environment_is_sanitized(self, mock_run, monkeypatch):
        monkeypatch.setenv("GIT_DIR", "sentinel")
        monkeypatch.setenv("GIT_INDEX_FILE", "sentinel-index")
        monkeypatch.setenv("GIT_CONFIG_KEY_0", "core.bare")
        monkeypatch.setenv("GIT_CONFIG_VALUE_0", "true")
        mock_run.return_value = CompletedProcess(args=[], returncode=0, stdout="", stderr="")

        run_changed_tests(["tests/test_foo.py"])

        env = mock_run.call_args.kwargs["env"]
        assert not any(key.startswith("GIT_CONFIG_KEY_") or key.startswith("GIT_CONFIG_VALUE_") for key in env)
        assert "GIT_DIR" not in env
        assert "GIT_INDEX_FILE" not in env

    def test_empty_list_returns_pass(self):
        passed, output = run_changed_tests([])
        assert passed is True
        assert output == ""

    @patch(f"{MODULE}.subprocess.run")
    def test_success(self, mock_run):
        mock_run.return_value = CompletedProcess(args=[], returncode=0, stdout="3 passed in 0.5s\n", stderr="")
        passed, output = run_changed_tests(["tests/test_foo.py"], cwd="/tmp")
        assert passed is True
        assert "3 passed" in output

    @patch(f"{MODULE}.subprocess.run")
    def test_failure(self, mock_run):
        mock_run.return_value = CompletedProcess(args=[], returncode=1, stdout="1 failed\n", stderr="")
        passed, output = run_changed_tests(["tests/test_foo.py"])
        assert passed is False
        assert "1 failed" in output

    @patch(f"{MODULE}.importlib.util.find_spec", return_value=object())
    @patch(f"{MODULE}.os.cpu_count", return_value=13)
    @patch(f"{MODULE}.subprocess.run")
    def test_passes_no_cov_and_quiet(self, mock_run, _mock_cpus, _mock_xdist, tmp_path):
        test_dir = tmp_path / "tests"
        test_dir.mkdir()
        for index in range(31):
            (test_dir / f"test_{index}.py").touch()
        mock_run.return_value = CompletedProcess(args=[], returncode=0, stdout="", stderr="")
        run_changed_tests(["tests"], cwd=tmp_path)
        args = mock_run.call_args[0][0]
        assert "--no-cov" in args
        assert "-q" in args
        assert args[args.index("-n") + 1] == "4"
        assert args[args.index("--dist") + 1 : args.index("--no-cov")] == ["loadfile", "tests"]

    def test_inherited_fixtures_survive_co_selected_ancestor_module(self):
        workspace = Path(__file__).resolve().parents[5]
        targets = [
            "tests/unit/cli/ci/dispatcher_wake_store/test_dispatcherwakestore.py",
            "tests/test_git_async.py",
            "tests/unit/cli/azure_devops/async_commands/test_add_pull_request_comment_async.py",
        ]

        passed, output = run_changed_tests(targets, cwd=workspace)

        assert passed, output
        assert "passed" in output

    def test_real_child_failure_is_reported(self, tmp_path):
        target = tmp_path / "test_failure.py"
        target.write_text("def test_failure():\n    assert False\n", encoding="utf-8")

        passed, output = run_changed_tests([str(target)], cwd=tmp_path)

        assert passed is False
        assert "1 failed" in output

    @patch(f"{MODULE}.importlib.util.find_spec", return_value=object())
    @patch(f"{MODULE}.os.cpu_count", return_value=13)
    @patch(f"{MODULE}.subprocess.run")
    def test_collects_ancestor_files_before_descendants_with_stable_peers(
        self, mock_run, _mock_cpus, _mock_xdist, tmp_path
    ):
        mock_run.return_value = CompletedProcess(args=[], returncode=0, stdout="", stderr="")
        (tmp_path / "tests" / "branch").mkdir(parents=True)
        branch = tmp_path / "tests" / "branch"
        for index in range(31):
            (branch / f"test_{index}.py").touch()
        deep_target = str(branch / "test_0.py") + "::test_example"
        if os.name == "nt":
            deep_target = deep_target.replace("/test_0.py", "\\test_0.py").swapcase()
        targets = ["tests/branch", deep_target, "tests/test_second.py", "tests/test_first.py"]

        run_changed_tests(targets, cwd=tmp_path)

        command = mock_run.call_args.args[0]
        assert "-n" not in command and "--dist" not in command
        assert command[3 : command.index("--no-cov")] == [
            "tests/test_second.py",
            "tests/test_first.py",
            "tests/branch",
            deep_target,
        ]

    @patch(f"{MODULE}.subprocess.run")
    def test_large_target_list_batches_below_windows_limit_and_aggregates_failures(self, mock_run):
        targets = [f"tests/unit/generated/test_{index:04d}_.py" for index in range(4308)]
        mock_run.side_effect = [
            CompletedProcess(args=[], returncode=1, stdout="first batch failed\n", stderr="diagnostic\n"),
            *[CompletedProcess(args=[], returncode=0, stdout=f"batch {index}\n", stderr="") for index in range(1, 30)],
        ]

        passed, output = run_changed_tests([*targets, targets[0]])

        assert passed is False
        assert all(fragment in output for fragment in ("first batch failed", "diagnostic", "batch 1"))
        assert mock_run.call_count > 1
        calls = [call.args[0] for call in mock_run.call_args_list]
        invoked_batches = []
        for command in calls:
            args = command[3 : command.index("--no-cov")]
            invoked_batches.append(args[args.index("--dist") + 2 :] if "--dist" in args else args)
            assert len(subprocess.list2cmdline(command)) <= 30_000
        offset = 0
        for batch in invoked_batches:
            assert Counter(batch) == Counter(targets[offset : offset + len(batch)])
            offset += len(batch)
        assert offset == len(targets)

    @patch(f"{MODULE}.subprocess.run")
    def test_single_target_over_command_limit_fails_without_execution(self, mock_run):
        target = "tests/" + ("x" * 30_000) + ".py"

        passed, output = run_changed_tests([target])

        assert passed is False
        assert target in output
        mock_run.assert_not_called()

    @patch(f"{MODULE}.get_changed_test_xdist_args", return_value=["-n", "4", "--dist", "loadfile"])
    @patch(f"{MODULE}.subprocess.run")
    def test_xdist_flags_over_command_limit_fall_back_to_serial(self, mock_run, _mock_xdist, monkeypatch):
        targets = [f"tests/test_{index}.py" for index in range(31)]
        base = [
            sys.executable,
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
            *targets,
        ]
        monkeypatch.setattr(
            f"{MODULE}._PYTEST_COMMAND_LENGTH_LIMIT",
            len(subprocess.list2cmdline(base)) + 1,
        )
        mock_run.return_value = CompletedProcess(args=[], returncode=0, stdout="", stderr="")

        passed, _ = run_changed_tests(targets)

        assert passed
        command = mock_run.call_args.args[0]
        assert "-n" not in command
        assert "--dist" not in command
