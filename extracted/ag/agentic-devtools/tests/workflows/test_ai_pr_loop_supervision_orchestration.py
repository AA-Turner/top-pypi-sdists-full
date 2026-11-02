"""Workflow simulations for the mutation-capable AI PR Loop supervisor."""

from __future__ import annotations

import json
from typing import Any

import pytest

from agentic_devtools.cli.ci import supervision_control_command as control_command
from agentic_devtools.cli.ci.supervision_control_command import (
    CONTROL_MARKER,
    IGNORE_LABEL,
    LOOP_WORKFLOW_FILES,
    SUPERVISED_LABEL,
    main,
)


class _FakeGitHub:
    def __init__(self, workflows: dict[str, bool], prs: dict[int, dict[str, Any]]) -> None:
        self.workflows = workflows
        self.prs = prs
        self.comments: list[str] = []
        self.issue_created = False
        self.labels: set[str] = set()

    def run_json(self, arguments: list[str]) -> object:
        if arguments[:2] == ["api", "user"]:
            return {"login": "automation"}
        if arguments[:2] == ["label", "list"]:
            search = arguments[arguments.index("--search") + 1]
            return [{"name": label} for label in self.labels if search in label]
        if arguments[:2] == ["issue", "list"]:
            if not self.issue_created:
                return []
            if arguments[arguments.index("--author") + 1] != "automation":
                return []
            return [
                {
                    "number": 42,
                    "body": CONTROL_MARKER,
                    "author": {"login": "automation"},
                    "labels": [],
                }
            ]
        if arguments[:2] == ["api", "graphql"]:
            return {
                "data": {
                    "repository": {
                        "issue": {
                            "comments": {
                                "nodes": [{"author": {"login": "automation"}, "body": body} for body in self.comments],
                                "pageInfo": {"hasPreviousPage": False, "hasNextPage": False, "endCursor": None},
                            }
                        }
                    }
                }
            }
        if arguments[:2] == ["workflow", "list"]:
            return [
                {
                    "name": name,
                    "path": f".github/workflows/{name}",
                    "state": "active" if enabled else "disabled_manually",
                }
                for name, enabled in self.workflows.items()
            ]
        if arguments[:2] == ["pr", "view"]:
            number = int(arguments[2])
            return {
                **self.prs[number],
                "labels": [{"name": label} for label in self.prs[number]["labels"]],
            }
        raise AssertionError(f"unexpected GitHub read: {arguments}")

    def run_text(self, arguments: list[str]) -> str:
        if arguments[:2] == ["label", "create"]:
            self.labels.add(arguments[2])
            return arguments[2]
        if arguments[:2] == ["issue", "create"]:
            assert SUPERVISED_LABEL in self.labels
            self.issue_created = True
            return "https://github.com/owner/repo/issues/42"
        if arguments[:2] == ["issue", "comment"]:
            self.comments.append(arguments[arguments.index("--body") + 1])
            return "https://github.com/owner/repo/issues/42#issuecomment-1"
        if arguments[:2] == ["pr", "edit"]:
            pr = self.prs[int(arguments[2])]
            labels = set(pr["labels"])
            label = arguments[-1]
            if arguments[-2] == "--add-label":
                labels.add(label)
            else:
                labels.discard(label)
            pr["labels"] = sorted(labels)
            return f"https://github.com/owner/repo/pull/{arguments[2]}"
        if arguments[:2] == ["workflow", "disable"]:
            self.workflows[arguments[2]] = False
            return ""
        if arguments[:2] == ["workflow", "enable"]:
            self.workflows[arguments[2]] = True
            return ""
        raise AssertionError(f"unexpected GitHub write: {arguments}")


def _install_fake_github(
    monkeypatch: pytest.MonkeyPatch,
    workflows: dict[str, bool],
    prs: dict[int, dict[str, Any]] | None = None,
) -> _FakeGitHub:
    fake = _FakeGitHub(workflows, prs or {})
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    monkeypatch.setenv("AGDT_SUPERVISION_LEASE_ID", "test-lease")
    monkeypatch.setattr(control_command, "_run_gh", fake.run_json)
    monkeypatch.setattr(control_command, "_run_gh_text", fake.run_text)
    return fake


def test_healthy_queue_publishes_a_checkpoint(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _install_fake_github(monkeypatch, dict.fromkeys(LOOP_WORKFLOW_FILES, True))
    payload = json.dumps({"selected": [], "deferred": [], "terminal_reason": "healthy_queue"})

    assert main(["--repo", "owner/repo", "checkpoint", "--run-id", "100", "--payload", payload]) == 0

    result = json.loads(capsys.readouterr().out)
    assert result["run_id"] == "100"
    checkpoint = json.loads(result["checkpoint"].split("\n", 1)[1])
    assert checkpoint["payload"]["terminal_reason"] == "healthy_queue"


def test_localized_defect_quarantines_only_the_affected_pr(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    prs: dict[int, dict[str, Any]] = {
        11: {"number": 11, "headRefOid": "head-11", "labels": []},
        12: {"number": 12, "headRefOid": "head-12", "labels": []},
    }
    _install_fake_github(monkeypatch, {}, prs)
    monkeypatch.setenv("GITHUB_RUN_ID", "localized-run")

    assert main(["--repo", "owner/repo", "quarantine", "--pr", "11=head-11"]) == 0

    assert IGNORE_LABEL in prs[11]["labels"]
    assert IGNORE_LABEL not in prs[12]["labels"]
    assert json.loads(capsys.readouterr().out)["receipt"]["changed"] == [11]


def test_systemic_defect_restores_the_exact_workflow_states(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    initial_states = {name: index != 0 for index, name in enumerate(LOOP_WORKFLOW_FILES)}
    workflows = dict(initial_states)
    _install_fake_github(monkeypatch, workflows)
    monkeypatch.setenv("GITHUB_RUN_ID", "systemic-run")

    assert main(["--repo", "owner/repo", "hold"]) == 0
    receipt = json.loads(capsys.readouterr().out)["receipt"]
    assert set(workflows.values()) == {False}

    assert main(["--repo", "owner/repo", "resume", "--receipt", json.dumps(receipt)]) == 0

    assert workflows == initial_states
    assert json.loads(capsys.readouterr().out)["states"] == initial_states
