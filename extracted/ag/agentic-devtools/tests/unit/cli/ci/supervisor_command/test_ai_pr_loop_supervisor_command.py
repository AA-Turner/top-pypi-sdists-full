"""Tests for the supervisor CLI entry point."""

import json
import sys
from unittest.mock import patch

import pytest


def _scan_with_source_errors(*_args, source_errors=(), **_kwargs):
    return {"errors": list(source_errors)}


def test_ai_pr_loop_supervisor_command_reports_scan(monkeypatch, capsys) -> None:
    from agentic_devtools.cli.ci.supervisor_command import ai_pr_loop_supervisor_command

    monkeypatch.setattr(sys, "argv", ["agdt-ai-pr-loop-supervisor", "--repo", "o/r"])
    monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
    with (
        patch("agentic_devtools.cli.ci.supervisor_command.shutil.which", return_value="gh"),
        patch("agentic_devtools.cli.ci.supervisor_command.resolve_github_repo", return_value="o/r"),
        patch("agentic_devtools.cli.ci.supervisor_command.load_supervisor_config") as load_config,
        patch("agentic_devtools.cli.ci.supervisor_command.load_agent_tasks", return_value=([], "")),
        patch("agentic_devtools.cli.ci.supervisor_command.scan_supervisor", return_value={"ok": True, "errors": []}),
        patch("agentic_devtools.cli.ci.supervisor_command.GitHubActionsProvider"),
        patch("agentic_devtools.cli.ci.supervisor_command._write_step_summary"),
    ):
        from agentic_devtools.cli.ci.supervisor import SupervisorConfig
        from agentic_devtools.cli.ci.supervisor_command import SupervisorRuntimeConfig

        load_config.return_value = SupervisorRuntimeConfig("report_only", 10, SupervisorConfig())
        ai_pr_loop_supervisor_command()

    assert json.loads(capsys.readouterr().out) == {"errors": [], "ok": True}


def test_ai_pr_loop_supervisor_command_uses_separate_scan_budget(monkeypatch, capsys) -> None:
    from agentic_devtools.cli.ci.supervisor_command import ai_pr_loop_supervisor_command

    monkeypatch.setattr(sys, "argv", ["agdt-ai-pr-loop-supervisor", "--repo", "o/r", "--max-candidates", "3"])
    monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
    with (
        patch("agentic_devtools.cli.ci.supervisor_command.shutil.which", return_value="gh"),
        patch("agentic_devtools.cli.ci.supervisor_command.resolve_github_repo", return_value="o/r"),
        patch("agentic_devtools.cli.ci.supervisor_command.load_supervisor_config") as load_config,
        patch("agentic_devtools.cli.ci.supervisor_command.load_agent_tasks", return_value=([], "")),
        patch(
            "agentic_devtools.cli.ci.supervisor_command.scan_supervisor",
            return_value={"ok": True, "errors": []},
        ) as scan,
        patch("agentic_devtools.cli.ci.supervisor_command.GitHubActionsProvider"),
        patch("agentic_devtools.cli.ci.supervisor_command._write_step_summary"),
    ):
        from agentic_devtools.cli.ci.supervisor import SupervisorConfig
        from agentic_devtools.cli.ci.supervisor_command import SupervisorRuntimeConfig

        load_config.return_value = SupervisorRuntimeConfig("report_only", 5, SupervisorConfig())
        ai_pr_loop_supervisor_command()

    assert json.loads(capsys.readouterr().out) == {"errors": [], "ok": True}
    assert scan.call_args.kwargs["max_candidates"] == 3
    assert scan.call_args.kwargs["max_scan_prs"] == 12


def test_ai_pr_loop_supervisor_command_rejects_missing_gh(monkeypatch) -> None:
    from agentic_devtools.cli.ci.supervisor_command import ai_pr_loop_supervisor_command

    monkeypatch.setattr(sys, "argv", ["agdt-ai-pr-loop-supervisor"])
    with patch("agentic_devtools.cli.ci.supervisor_command.shutil.which", return_value=None):
        with pytest.raises(SystemExit) as exc:
            ai_pr_loop_supervisor_command()
    assert exc.value.code == 10


def test_ai_pr_loop_supervisor_command_preserves_task_loader_error(monkeypatch, capsys) -> None:
    from agentic_devtools.cli.ci.supervisor_command import ai_pr_loop_supervisor_command

    monkeypatch.setattr(sys, "argv", ["agdt-ai-pr-loop-supervisor"])
    with (
        patch("agentic_devtools.cli.ci.supervisor_command.shutil.which", return_value="gh"),
        patch("agentic_devtools.cli.ci.supervisor_command.resolve_github_repo", return_value="o/r"),
        patch("agentic_devtools.cli.ci.supervisor_command.load_supervisor_config") as load_config,
        patch(
            "agentic_devtools.cli.ci.supervisor_command.load_agent_tasks",
            return_value=([], "agent_tasks: unavailable"),
        ),
        patch("agentic_devtools.cli.ci.supervisor_command.scan_supervisor", side_effect=_scan_with_source_errors),
        patch("agentic_devtools.cli.ci.supervisor_command.GitHubActionsProvider"),
        patch("agentic_devtools.cli.ci.supervisor_command._write_step_summary"),
    ):
        from agentic_devtools.cli.ci.supervisor import SupervisorConfig
        from agentic_devtools.cli.ci.supervisor_command import SupervisorRuntimeConfig

        load_config.return_value = SupervisorRuntimeConfig("report_only", 10, SupervisorConfig())
        ai_pr_loop_supervisor_command()

    assert json.loads(capsys.readouterr().out)["errors"] == ["agent_tasks: unavailable"]


def test_ai_pr_loop_supervisor_command_records_workflow_run_error(monkeypatch, capsys) -> None:
    from agentic_devtools.cli.ci.supervisor_command import ai_pr_loop_supervisor_command

    monkeypatch.setattr(sys, "argv", ["agdt-ai-pr-loop-supervisor"])
    with (
        patch("agentic_devtools.cli.ci.supervisor_command.shutil.which", return_value="gh"),
        patch("agentic_devtools.cli.ci.supervisor_command.resolve_github_repo", return_value="o/r"),
        patch("agentic_devtools.cli.ci.supervisor_command.load_supervisor_config") as load_config,
        patch("agentic_devtools.cli.ci.supervisor_command.load_agent_tasks", return_value=([], "")),
        patch("agentic_devtools.cli.ci.supervisor_command.scan_supervisor", side_effect=_scan_with_source_errors),
        patch("agentic_devtools.cli.ci.supervisor_command.GitHubActionsProvider") as provider_cls,
        patch("agentic_devtools.cli.ci.supervisor_command._write_step_summary"),
    ):
        from agentic_devtools.cli.ci.supervisor import SupervisorConfig
        from agentic_devtools.cli.ci.supervisor_command import SupervisorRuntimeConfig

        load_config.return_value = SupervisorRuntimeConfig("report_only", 10, SupervisorConfig())
        provider_cls.return_value.list_workflow_runs.side_effect = RuntimeError("runs unavailable")
        ai_pr_loop_supervisor_command()

    assert json.loads(capsys.readouterr().out)["errors"] == ["workflow_runs: runs unavailable"]


def test_ai_pr_loop_supervisor_command_falls_back_when_provider_lacks_enrichment_flag(monkeypatch, capsys) -> None:
    from agentic_devtools.cli.ci.supervisor_command import ai_pr_loop_supervisor_command

    monkeypatch.setattr(sys, "argv", ["agdt-ai-pr-loop-supervisor"])
    provider = type("Provider", (), {})()

    def _list_workflow_runs(*args, **kwargs):
        if "include_dispatch_inputs" in kwargs:
            raise TypeError("unexpected keyword")
        return []

    provider.list_workflow_runs = _list_workflow_runs
    with (
        patch("agentic_devtools.cli.ci.supervisor_command.shutil.which", return_value="gh"),
        patch("agentic_devtools.cli.ci.supervisor_command.resolve_github_repo", return_value="o/r"),
        patch("agentic_devtools.cli.ci.supervisor_command.load_supervisor_config") as load_config,
        patch("agentic_devtools.cli.ci.supervisor_command.load_agent_tasks", return_value=([], "")),
        patch("agentic_devtools.cli.ci.supervisor_command.scan_supervisor", return_value={"errors": []}),
        patch("agentic_devtools.cli.ci.supervisor_command.GitHubActionsProvider", return_value=provider),
        patch("agentic_devtools.cli.ci.supervisor_command._write_step_summary"),
    ):
        from agentic_devtools.cli.ci.supervisor import SupervisorConfig
        from agentic_devtools.cli.ci.supervisor_command import SupervisorRuntimeConfig

        load_config.return_value = SupervisorRuntimeConfig("report_only", 10, SupervisorConfig())
        ai_pr_loop_supervisor_command()

    assert json.loads(capsys.readouterr().out)["errors"] == []


def test_ai_pr_loop_supervisor_command_allows_provider_without_workflow_runs(monkeypatch, capsys) -> None:
    from agentic_devtools.cli.ci.supervisor_command import ai_pr_loop_supervisor_command

    monkeypatch.setattr(sys, "argv", ["agdt-ai-pr-loop-supervisor"])
    with (
        patch("agentic_devtools.cli.ci.supervisor_command.shutil.which", return_value="gh"),
        patch("agentic_devtools.cli.ci.supervisor_command.resolve_github_repo", return_value="o/r"),
        patch("agentic_devtools.cli.ci.supervisor_command.load_supervisor_config") as load_config,
        patch("agentic_devtools.cli.ci.supervisor_command.load_agent_tasks", return_value=([], "")),
        patch("agentic_devtools.cli.ci.supervisor_command.scan_supervisor", return_value={"errors": []}),
        patch("agentic_devtools.cli.ci.supervisor_command.GitHubActionsProvider", return_value=object()),
        patch("agentic_devtools.cli.ci.supervisor_command._write_step_summary"),
    ):
        from agentic_devtools.cli.ci.supervisor import SupervisorConfig
        from agentic_devtools.cli.ci.supervisor_command import SupervisorRuntimeConfig

        load_config.return_value = SupervisorRuntimeConfig("report_only", 10, SupervisorConfig())
        ai_pr_loop_supervisor_command()

    assert json.loads(capsys.readouterr().out)["errors"] == []


def test_ai_pr_loop_supervisor_command_rejects_invalid_limit(monkeypatch) -> None:
    from agentic_devtools.cli.ci.supervisor_command import ai_pr_loop_supervisor_command

    monkeypatch.setattr(sys, "argv", ["agdt-ai-pr-loop-supervisor", "--max-candidates", "0"])
    with patch("agentic_devtools.cli.ci.supervisor_command.shutil.which", return_value="gh"):
        with pytest.raises(SystemExit) as exc:
            ai_pr_loop_supervisor_command()
    assert exc.value.code == 2


def test_ai_pr_loop_supervisor_command_reports_scan_failure(monkeypatch) -> None:
    from agentic_devtools.cli.ci.supervisor_command import ai_pr_loop_supervisor_command

    monkeypatch.setattr(sys, "argv", ["agdt-ai-pr-loop-supervisor"])
    with (
        patch("agentic_devtools.cli.ci.supervisor_command.shutil.which", return_value="gh"),
        patch("agentic_devtools.cli.ci.supervisor_command.resolve_github_repo", return_value="o/r"),
        patch("agentic_devtools.cli.ci.supervisor_command.load_supervisor_config") as load_config,
        patch("agentic_devtools.cli.ci.supervisor_command.load_agent_tasks", return_value=([], "")),
        patch("agentic_devtools.cli.ci.supervisor_command.scan_supervisor", side_effect=RuntimeError("broken")),
        patch("agentic_devtools.cli.ci.supervisor_command.GitHubActionsProvider"),
    ):
        from agentic_devtools.cli.ci.supervisor import SupervisorConfig
        from agentic_devtools.cli.ci.supervisor_command import SupervisorRuntimeConfig

        load_config.return_value = SupervisorRuntimeConfig("report_only", 10, SupervisorConfig())
        with pytest.raises(SystemExit) as exc:
            ai_pr_loop_supervisor_command()
    assert exc.value.code == 1
