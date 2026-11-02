"""Tests for the _control_issue symbol."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.supervision_control import CONTROL_MARKER, SUPERVISED_LABEL
from agentic_devtools.cli.ci.supervision_control_command import _control_issue


def test_control_issue_returns_existing_issue_without_creating_one(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._find_control_issue", lambda _repo: 42)
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._run_gh",
        lambda _arguments: [{"name": SUPERVISED_LABEL}],
    )

    def unexpected_create(_arguments: list[str]) -> str:
        pytest.fail("an existing control issue should not be created again")

    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh_text", unexpected_create)

    assert _control_issue("owner/repo") == 42


def test_control_issue_restores_missing_supervised_label_for_existing_issue(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_labels: set[str] = set()
    writes: list[list[str]] = []
    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._find_control_issue", lambda _repo: 42)

    def list_labels(_arguments: list[str]) -> list[dict[str, str]]:
        return [{"name": label} for label in repo_labels]

    def write(arguments: list[str]) -> str:
        writes.append(arguments)
        repo_labels.add(arguments[2])
        return arguments[2]

    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh", list_labels)
    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh_text", write)

    assert _control_issue("owner/repo") == 42

    assert writes == [["label", "create", SUPERVISED_LABEL, "--repo", "owner/repo"]]
    assert repo_labels == {SUPERVISED_LABEL}


def test_control_issue_creates_and_verifies_missing_issue(monkeypatch: pytest.MonkeyPatch) -> None:
    lookups = iter([None, 43])
    calls: list[list[str]] = []
    repo_labels: set[str] = set()

    def list_labels(_arguments: list[str]) -> list[dict[str, str]]:
        return [{"name": label} for label in repo_labels]

    def create_issue(arguments: list[str]) -> str:
        calls.append(arguments)
        if arguments[:2] == ["label", "create"]:
            repo_labels.add(arguments[2])
            return arguments[2]
        assert SUPERVISED_LABEL in repo_labels
        return "https://github.com/owner/repo/issues/43"

    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._find_control_issue",
        lambda _repo: next(lookups),
    )
    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh", list_labels)
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._run_gh_text",
        create_issue,
    )

    assert _control_issue("owner/repo") == 43
    assert calls == [
        ["label", "create", SUPERVISED_LABEL, "--repo", "owner/repo"],
        [
            "issue",
            "create",
            "--repo",
            "owner/repo",
            "--title",
            "AI PR Loop supervision control",
            "--body",
            CONTROL_MARKER,
            "--label",
            SUPERVISED_LABEL,
        ],
    ]
    assert repo_labels == {SUPERVISED_LABEL}


def test_control_issue_fails_if_supervised_label_read_back_is_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._find_control_issue", lambda _repo: None)
    calls: list[list[str]] = []
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._run_gh",
        lambda _arguments: [],
    )

    def create_label(arguments: list[str]) -> str:
        calls.append(arguments)
        return SUPERVISED_LABEL

    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh_text", create_label)

    with pytest.raises(RuntimeError, match="labels missing after ensure-labels"):
        _control_issue("owner/repo")

    assert calls == [["label", "create", SUPERVISED_LABEL, "--repo", "owner/repo"]]


def test_control_issue_rejects_creation_without_issue_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._find_control_issue", lambda _repo: None)
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._run_gh",
        lambda _arguments: [{"name": SUPERVISED_LABEL}],
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._run_gh_text",
        lambda _arguments: "created issue",
    )

    with pytest.raises(RuntimeError, match="control issue creation did not return a URL"):
        _control_issue("owner/repo")


def test_control_issue_rejects_creation_read_back_mismatch(monkeypatch: pytest.MonkeyPatch) -> None:
    lookups = iter([None, 44])
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._run_gh",
        lambda _arguments: [{"name": SUPERVISED_LABEL}],
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._find_control_issue",
        lambda _repo: next(lookups),
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._run_gh_text",
        lambda _arguments: "https://github.com/owner/repo/issues/43",
    )

    with pytest.raises(RuntimeError, match="control issue read-back mismatch"):
        _control_issue("owner/repo")
