"""Compact JSON command output and module entry point."""

import json
import runpy
import sys
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.pipeline.delivery import InitialDeliveryOutcome
from agentic_devtools.cli.ci.pipeline.delivery_bridge import main
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

MODULE = "agentic_devtools.cli.ci.pipeline.delivery_bridge"
SHA = "ab" * 20
ARGS = ["--repository", "owner/repo", "--pr-number", "42", "--head-sha", SHA]


def test_prints_single_compact_json_line(capsys: pytest.CaptureFixture[str]) -> None:
    result = {
        "repository": "owner/repo",
        "prNumber": 42,
        "headSha": SHA,
        "outcome": "DELIVERED",
        "complete": True,
        "diffEvidence": "NON_ZERO_DIFF",
    }
    with patch(f"{MODULE}._run_bridge", return_value=result) as bridge:
        assert main(ARGS) == 0

    bridge.assert_called_once_with("owner/repo", 42, SHA)
    output = capsys.readouterr()
    assert output.out == json.dumps(result, separators=(",", ":")) + "\n"
    assert output.err == ""


def test_failure_propagates_without_json(capsys: pytest.CaptureFixture[str]) -> None:
    with patch(f"{MODULE}._run_bridge", side_effect=RuntimeError("unavailable")):
        with pytest.raises(RuntimeError, match="unavailable"):
            main(ARGS)

    assert capsys.readouterr().out == ""


def test_module_entry_exits_successfully(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["delivery-bridge", *ARGS])
    monkeypatch.delitem(sys.modules, MODULE)
    with (
        patch("agentic_devtools.cli.ci.github_provider.GitHubActionsProvider") as provider,
        patch(
            "agentic_devtools.cli.ci.pipeline.delivery.classify_initial_delivery_with_head",
            return_value=(SHA, InitialDeliveryOutcome.DELIVERED),
        ) as classify,
    ):
        with pytest.raises(SystemExit) as exc:
            runpy.run_module(MODULE, run_name="__main__")

    assert exc.value.code == 0
    provider.assert_called_once_with(repo="owner/repo", token=None)
    classify.assert_called_once_with(provider.return_value, 42, completion_confirmed=True, initial_plan_sha=None)
    assert json.loads(capsys.readouterr().out)["complete"] is True


def test_module_entry_propagates_actual_authority_rate_limit_without_json(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["delivery-bridge", *ARGS])
    monkeypatch.delitem(sys.modules, MODULE)
    error = ProviderRateLimitError(30, provider="github")
    with patch("agentic_devtools.cli.ci.github_provider.GitHubActionsProvider") as provider:
        provider.return_value.get_pr_metadata.side_effect = error

        with pytest.raises(ProviderRateLimitError) as exc:
            runpy.run_module(MODULE, run_name="__main__")

    assert exc.value is error
    provider.return_value.get_pr_metadata.assert_called_once_with(42)
    assert capsys.readouterr().out == ""
