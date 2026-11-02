"""Tests for SmartModuleTestRunner."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from agentic_devtools.cli.checks.smart_module_tests import SmartModuleTestRunner

MODULE = "agentic_devtools.cli.checks.smart_module_tests"


class TestSmartModuleTestRunner:
    """Tests for selecting and running smart module tests."""

    def test_builds_worksteal_coverage_args_with_directories_before_files(self, tmp_path, monkeypatch):
        (tmp_path / "tests" / "unit" / "cli" / "git").mkdir(parents=True)
        (tmp_path / "tests" / "test_git_extra.py").write_text("def test_extra(): pass\n", encoding="utf-8")
        (tmp_path / "tests" / "test_git_directory.py").mkdir()
        (tmp_path / "tests" / "unit" / "cli" / "azure_devops").mkdir(parents=True)
        monkeypatch.setattr(
            f"{MODULE}.get_xdist_args",
            lambda path, *, coverage_workers, distribution: ["-n", "3", "--dist", distribution],
        )

        args = SmartModuleTestRunner(["git", "azure_devops"], tmp_path).pytest_args()

        assert args[:3] == [
            str(tmp_path / "tests" / "unit" / "cli" / "git"),
            str(tmp_path / "tests" / "unit" / "cli" / "azure_devops"),
            str(tmp_path / "tests" / "test_git_extra.py"),
        ]
        assert args[args.index("-n") + 1] == "3"
        assert args[args.index("--dist") + 1] == "worksteal"
        assert "--cov=agentic_devtools/cli/git" in args
        assert "--cov=agentic_devtools/cli/azure_devops" in args
        assert "--cov-report=xml" in args
        assert "--cov-fail-under=100" in args
        assert "--override-ini=addopts=" in args

    def test_uses_only_selected_module_coverage_scope(self, tmp_path):
        test_dir = tmp_path / "tests" / "unit" / "cli" / "jira"
        test_dir.mkdir(parents=True)
        (test_dir / "test_jira.py").touch()
        unrelated_dir = tmp_path / "tests" / "unit" / "cli" / "git"
        unrelated_dir.mkdir(parents=True)
        for index in range(31):
            (unrelated_dir / f"test_{index}.py").touch()

        args = SmartModuleTestRunner(["jira"], tmp_path).pytest_args()

        assert str(test_dir) in args
        assert "--cov=agentic_devtools/cli/jira" in args
        assert "--cov=agentic_devtools/cli/git" not in args
        assert "-n" not in args

    def test_selects_core_standalone_files_and_full_core_coverage_scope(self, tmp_path):
        for path in ("tests/unit/state", "tests/test_version.py"):
            target = tmp_path / path
            if path.endswith(".py"):
                target.parent.mkdir(parents=True, exist_ok=True)
                target.touch()
            else:
                target.mkdir(parents=True)

        args = SmartModuleTestRunner(["core"], tmp_path).pytest_args()

        assert args[:2] == [str(tmp_path / "tests/unit/state"), str(tmp_path / "tests/test_version.py")]
        assert "--cov=agentic_devtools.state" in args
        assert "--cov=agentic_devtools.cli.testing" in args
        assert len([arg for arg in args if arg.startswith("--cov=")]) == 9

    def test_returns_no_args_when_selected_modules_have_no_test_paths(self, tmp_path):
        assert SmartModuleTestRunner(["git"], tmp_path).pytest_args() == []

    def test_selects_ci_regressions_with_exact_workflow_wiring(self, tmp_path):
        test_paths = (
            "tests/unit/cli/ci/critique_adjudicator/test_critique_adjudicator.py",
            "tests/unit/cli/ci/pipeline/critique_gate/test_critique_gate_exception_passed.py",
        )
        for relative_path in test_paths:
            target = tmp_path / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.touch()

        args = SmartModuleTestRunner(["ci"], tmp_path).pytest_args()

        assert args[:2] == [str(tmp_path / path) for path in test_paths]
        assert [arg for arg in args if arg.startswith("--cov=")] == [
            "--cov=agentic_devtools.cli.ci.critique_adjudicator",
            "--cov=agentic_devtools.cli.ci.pipeline.critique_gate",
        ]

        workflow_path = Path(__file__).resolve().parents[5] / ".github/workflows/pr-smart-module-tests.yml"
        workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
        steps = workflow["jobs"]["smart-module-tests"]["steps"]
        filter_step = next(step for step in steps if step.get("id") == "filter")
        aggregate = next(step for step in steps if step.get("name") == "Check if any module changed")
        scoped = next(step for step in steps if step.get("name") == "Run scoped tests with per-module coverage")
        filters = yaml.safe_load(filter_step["with"]["filters"])
        assert set(filters["ci"]) == {
            "agentic_devtools/cli/ci/critique_adjudicator.py",
            "agentic_devtools/cli/ci/pipeline/critique_gate.py",
            "agentic_devtools/cli/ci/windows_specific.py",
            "agentic_devtools/cli/ci/windows_specific_cli.py",
            "agentic_devtools/cli/ci/windows_fixture_bytes.py",
            *test_paths,
            "tests/unit/cli/ci/windows_specific/**",
            "tests/unit/cli/ci/windows_specific_cli/**",
            "tests/unit/cli/ci/windows_fixture_bytes/**",
        }
        flags = json.loads(scoped["env"]["AGDT_SMART_MODULE_FLAGS"])
        assert flags["ci"] == "${{ steps.filter.outputs.ci }}"
        assert aggregate["id"] == "has-modules"
        run = aggregate["run"].replace("\\\n", " ")
        operand = '"${{ steps.filter.outputs.ci }}" == "true"'
        assert run.count(operand) == 1
        before, after = run.split(operand)
        assert before.rstrip().endswith("||") or after.lstrip().startswith("||")
        assert not before.rstrip().endswith("&&")
        assert not after.lstrip().startswith("&&")
        output_line = 'echo "result=true" >> "$GITHUB_OUTPUT"'
        assert run.index("if [[") < run.index(operand) < run.index("]]; then") < run.index(output_line)
        assert "steps.has-modules.outputs.result == 'true'" in scoped["if"]

    def test_run_warns_and_skips_when_there_are_no_selected_tests(self, tmp_path, capsys):
        with patch(f"{MODULE}.subprocess.run") as mock_run:
            result = SmartModuleTestRunner([], tmp_path).run()

        assert result == 0
        assert "No test paths found" in capsys.readouterr().out
        mock_run.assert_not_called()

    @patch(f"{MODULE}.subprocess.run")
    def test_run_sets_sysmon_and_propagates_pytest_failure(self, mock_run, tmp_path, monkeypatch):
        monkeypatch.setenv("GIT_DIR", "sentinel")
        monkeypatch.setenv("GIT_CONFIG_KEY_9", "core.bare")
        (tmp_path / "tests" / "unit" / "cli" / "jira").mkdir(parents=True)
        monkeypatch.delenv("COVERAGE_CORE", raising=False)
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=2)

        result = SmartModuleTestRunner(["jira"], tmp_path).run()

        assert result == 2
        assert "GIT_DIR" not in mock_run.call_args.kwargs["env"]
        assert "GIT_CONFIG_KEY_9" not in mock_run.call_args.kwargs["env"]
        assert mock_run.call_args.kwargs["env"]["COVERAGE_CORE"] == "sysmon"
        assert mock_run.call_args.kwargs["shell"] is False
        assert mock_run.call_args.kwargs["cwd"] == str(tmp_path)

    @patch(f"{MODULE}.subprocess.run")
    def test_run_preserves_explicit_coverage_core(self, mock_run, tmp_path, monkeypatch, capsys):
        test_dir = tmp_path / "tests" / "unit" / "cli" / "jira"
        test_dir.mkdir(parents=True)
        monkeypatch.setenv("COVERAGE_CORE", "ctrace")
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0)

        SmartModuleTestRunner(["jira"], tmp_path).run()

        assert mock_run.call_args.kwargs["env"]["COVERAGE_CORE"] == "ctrace"
        output = capsys.readouterr().out
        assert f"Test paths:\n  {test_dir}" in output
        assert "Coverage flags:\n  --cov=agentic_devtools/cli/jira" in output

    def test_from_environment_accepts_enabled_module_flags(self, monkeypatch, tmp_path):
        monkeypatch.setenv("AGDT_SMART_MODULE_FLAGS", json.dumps({"git": "true", "jira": "false"}))

        runner = SmartModuleTestRunner.from_environment(workspace=tmp_path)

        assert runner.selected_modules == ["git"]

    @pytest.mark.parametrize(
        "flags",
        [
            "{",
            "[]",
            '{"unknown": "true"}',
            '{"git": "yes"}',
        ],
    )
    def test_from_environment_rejects_malformed_module_flags(self, monkeypatch, tmp_path, flags):
        monkeypatch.setenv("AGDT_SMART_MODULE_FLAGS", flags)

        with pytest.raises(ValueError, match="AGDT_SMART_MODULE_FLAGS"):
            SmartModuleTestRunner.from_environment(workspace=tmp_path)

    def test_constructor_rejects_unknown_modules(self, tmp_path):
        with pytest.raises(ValueError, match="Unknown smart module"):
            SmartModuleTestRunner(["unknown"], tmp_path)
