"""Tests for the _observations symbol."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.supervision_control import PRObservation
from agentic_devtools.cli.ci.supervision_control_command import _observations


def test_observations_reads_and_validates_each_expected_pr(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[list[str]] = []

    def read_provider(arguments: list[str]) -> object:
        calls.append(arguments)
        return {"number": 7, "headRefOid": "head-7", "labels": [{"name": "ai-pr-loop-ignore"}]}

    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh", read_provider)

    assert _observations("owner/repo", {7: "head-7"}) == [PRObservation(7, "head-7", frozenset({"ai-pr-loop-ignore"}))]
    assert calls == [["pr", "view", "7", "--repo", "owner/repo", "--json", "number,headRefOid,labels"]]


def test_observations_rejects_invalid_provider_data(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command._run_gh",
        lambda _arguments: {"number": 7, "headRefOid": "", "labels": []},
    )

    with pytest.raises(ValueError, match="head SHA"):
        _observations("owner/repo", {7: "head-7"})
