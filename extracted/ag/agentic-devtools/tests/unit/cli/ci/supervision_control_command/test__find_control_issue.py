"""Tests for the _find_control_issue symbol."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.supervision_control import CONTROL_MARKER
from agentic_devtools.cli.ci.supervision_control_command import _find_control_issue


def test_find_control_issue_uses_authenticated_author_and_searches_all_issues(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[list[str]] = []

    def read_provider(arguments: list[str]) -> object:
        calls.append(arguments)
        if arguments == ["api", "user"]:
            return {"login": "automation"}
        if arguments[arguments.index("--author") + 1] == "github-actions[bot]":
            return []
        return [
            {
                "number": 42,
                "body": CONTROL_MARKER,
                "author": {"login": "automation"},
                "labels": [],
                "state": "CLOSED",
            }
        ]

    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh", read_provider)

    assert _find_control_issue("owner/repo") == 42
    assert calls == [
        ["api", "user"],
        [
            "issue",
            "list",
            "--repo",
            "owner/repo",
            "--state",
            "all",
            "--search",
            "ai-pr-loop-supervision:control:v1",
            "--author",
            "automation",
            "--limit",
            "1000",
            "--json",
            "number,body,author,labels",
        ],
        [
            "issue",
            "list",
            "--repo",
            "owner/repo",
            "--state",
            "all",
            "--search",
            "ai-pr-loop-supervision:control:v1",
            "--author",
            "github-actions[bot]",
            "--limit",
            "1000",
            "--json",
            "number,body,author,labels",
        ],
    ]


@pytest.mark.parametrize("identity", [None, {}, {"login": ""}, {"login": "  "}])
def test_find_control_issue_rejects_unavailable_authenticated_identity(
    monkeypatch: pytest.MonkeyPatch,
    identity: object,
) -> None:
    calls: list[list[str]] = []

    def read_provider(arguments: list[str]) -> object:
        calls.append(arguments)
        return identity

    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh", read_provider)

    with pytest.raises(RuntimeError, match="authenticated GitHub identity is unavailable"):
        _find_control_issue("owner/repo")

    assert calls == [["api", "user"]]


def test_find_control_issue_queries_each_trusted_author(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[list[str]] = []

    def read_provider(arguments: list[str]) -> object:
        calls.append(arguments)
        if "--author" in arguments and arguments[arguments.index("--author") + 1] == "github-actions[bot]":
            return [
                {
                    "number": 42,
                    "body": CONTROL_MARKER,
                    "author": {"login": "github-actions[bot]"},
                    "labels": [],
                }
            ]
        return []

    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._trusted_control_authors",
        lambda: {
            "automation",
            "github-actions[bot]",
        },
    )
    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh", read_provider)

    assert _find_control_issue("owner/repo") == 42
    assert [arguments[arguments.index("--author") + 1] for arguments in calls] == [
        "automation",
        "github-actions[bot]",
    ]
