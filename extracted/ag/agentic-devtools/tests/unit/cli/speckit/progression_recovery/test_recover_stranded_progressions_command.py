"""The scheduled recovery command reports isolated failures."""

import json
from unittest.mock import Mock, patch

import pytest

from agentic_devtools.cli.speckit.progression_recovery import recover_stranded_progressions_command


def test_command_recovers_each_issue_and_fails_on_errors(monkeypatch, capsys):
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    monkeypatch.setenv("GITHUB_TOKEN", "workflow-token")
    worker = Mock()
    worker.processing_issues.return_value = [42, 43]
    worker.recover.side_effect = [RuntimeError("error"), {"issue_number": 43, "status": "replayed"}]
    with patch("agentic_devtools.cli.speckit.progression_recovery.ProgressionRecovery", return_value=worker):
        with pytest.raises(SystemExit, match="1"):
            recover_stranded_progressions_command()
    results = json.loads(capsys.readouterr().out)
    assert [result["issue_number"] for result in results] == [42, 43]
    assert results[0]["status"] == "error"


@pytest.mark.parametrize("token_env", ["GITHUB_TOKEN", "GH_TOKEN", "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"])
def test_command_token_conventions_and_success(monkeypatch, capsys, token_env):
    for name in ["GITHUB_TOKEN", "GH_TOKEN", "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"]:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv(token_env, "workflow-token")
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    worker = Mock()
    worker.processing_issues.return_value = [42]
    worker.recover.return_value = {"issue_number": 42, "status": "skip"}
    with patch("agentic_devtools.cli.speckit.progression_recovery.ProgressionRecovery", return_value=worker) as factory:
        recover_stranded_progressions_command()
    factory.assert_called_once_with("owner/repo", "workflow-token")
    assert json.loads(capsys.readouterr().out)[0]["status"] == "skip"


def test_global_inspection_failure_is_reported(monkeypatch, capsys):
    monkeypatch.setenv("GITHUB_TOKEN", "workflow-token")
    with patch(
        "agentic_devtools.cli.speckit.progression_recovery.ProgressionRecovery", side_effect=ValueError("invalid")
    ):
        with pytest.raises(SystemExit, match="1"):
            recover_stranded_progressions_command()
    assert json.loads(capsys.readouterr().out)[0]["status"] == "error"
