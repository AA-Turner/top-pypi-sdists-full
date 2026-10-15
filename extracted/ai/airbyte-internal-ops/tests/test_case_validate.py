# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""Tests for the validate workflow's decisions: what to do after the gate and
the runs, and the bounded wait before merging.

The PR is a scripted sequence of reads, and the clock only advances when the
code sleeps, so every outcome is reached deterministically.
"""

from __future__ import annotations

import json
import os
import stat
import sys
from collections.abc import Iterable
from typing import Any

import pytest

from airbyte_ops_mcp.regression_tests.case_validate import (
    COMMENT_MARKER,
    STATUS_DESCRIPTION_LIMIT,
    decide_validation,
    gh_merge,
    runs_from_needs,
    wait_and_merge,
)

pytestmark = pytest.mark.unit

SHA = "a" * 40
OTHER = "b" * 40
RUN_URL = "https://github.com/airbytehq/airbyte-ops-mcp/actions/runs/1"
GATE_PASS = {"status": "pass", "problems": []}
RUNS_PASS = {
    "reproduce-1": ("success", "PASS (reproduced)", "true"),
    "reproduce-2": ("success", "PASS (reproduced)", "true"),
}


def _pr(**overrides: Any) -> dict[str, Any]:
    return {
        "state": "OPEN",
        "headRefOid": SHA,
        "baseRefName": "main",
        "isCrossRepository": False,
        "mergeStateStatus": "BLOCKED",
        **overrides,
    }


def _decide(**overrides: Any):
    arguments: dict[str, Any] = {
        "gate": GATE_PASS,
        "gate_refusal": None,
        "runs": RUNS_PASS,
        "pr": _pr(),
        "validated_sha": SHA,
        "merge_enabled": True,
        "run_url": RUN_URL,
    }
    return decide_validation(**{**arguments, **overrides})


def test_a_validated_pr_merges_when_the_switch_is_on():
    decision = _decide()

    assert (decision.action, decision.state, decision.description) == (
        "merge",
        "pending",
        "validated; merging",
    )
    assert decision.comment is None


def test_a_validated_pr_is_only_reported_when_the_switch_is_off():
    decision = _decide(merge_enabled=False)

    assert (decision.action, decision.state, decision.description) == (
        "report",
        "success",
        "validated; auto-merge off",
    )


@pytest.mark.parametrize(
    "overrides,reason",
    [
        (
            {"gate": None, "gate_refusal": "the PR head is a fork"},
            "the PR head is a fork",
        ),
        ({"gate": None}, "the gate produced no report"),
        (
            {"gate": {"status": "fail", "problems": ["origin.json is required"]}},
            "origin.json is required",
        ),
        (
            {
                "runs": {
                    **RUNS_PASS,
                    "reproduce-2": ("failure", "FAIL (not reproduced)", "false"),
                }
            },
            "reproduce-2: FAIL (not reproduced) (failure)",
        ),
        (
            {"runs": {"reproduce-1": ("skipped", "", "")}},
            "reproduce-1: no verdict (skipped)",
        ),
        (
            {
                "runs": {
                    **RUNS_PASS,
                    "reproduce-1": ("success", "PASS (reproduced)", "false"),
                }
            },
            "reproduce-1: PASS (reproduced) (success)",
        ),
        ({"pr": _pr(headRefOid=OTHER)}, f"the PR head moved from {SHA} to {OTHER}"),
        ({"pr": _pr(state="CLOSED")}, "the PR is closed"),
        (
            {"pr": _pr(isCrossRepository=True)},
            "the PR head is not a branch of this repository",
        ),
        ({"pr": _pr(baseRefName="dev")}, "the PR targets 'dev', not 'main'"),
        ({"pr": None}, "could not re-read the PR"),
    ],
)
def test_any_failed_check_fails_with_a_comment(overrides, reason):
    decision = _decide(**overrides)

    assert (decision.action, decision.state) == ("fail", "failure")
    assert decision.description.startswith("validation failed: ")
    assert len(decision.description) <= STATUS_DESCRIPTION_LIMIT
    assert decision.comment is not None
    assert decision.comment.splitlines()[0] == COMMENT_MARKER.format(sha=SHA)
    assert f"- {reason}" in decision.comment
    assert RUN_URL in decision.comment


def test_case_content_in_the_comment_cannot_escape_its_code_block():
    gate = {"status": "fail", "problems": ["```\n@everyone [x](https://evil)"]}

    decision = _decide(gate=gate)

    assert decision.comment is not None
    body = decision.comment.split("```text\n", 1)[1]
    assert body.count("```") == 1
    assert len(decision.description) <= STATUS_DESCRIPTION_LIMIT


def test_runs_are_read_from_the_workflow_needs():
    needs = {
        "gate": {"result": "success", "outputs": {"head_sha": SHA}},
        "reproduce-1": {
            "result": "success",
            "outputs": {"verdict": "PASS (reproduced)", "passed": "true"},
        },
        "reproduce-2": {"result": "skipped", "outputs": {}},
    }

    assert runs_from_needs(needs) == {
        "reproduce-1": ("success", "PASS (reproduced)", "true"),
        "reproduce-2": ("skipped", "", ""),
    }


class FakePr:
    """A PR whose reads follow a script; an Exception entry is raised."""

    def __init__(self, reads: Iterable[dict[str, Any] | Exception]) -> None:
        self.reads = list(reads)
        self.merges = 0
        self.now = 0.0
        self.reject_merges = 0

    def read(self) -> dict[str, Any]:
        entry = self.reads.pop(0) if len(self.reads) > 1 else self.reads[0]
        if isinstance(entry, Exception):
            raise entry
        return entry

    def merge(self) -> None:
        self.merges += 1
        if self.merges <= self.reject_merges:
            raise RuntimeError("Pull request is not mergeable")

    def sleep(self, seconds: float) -> None:
        self.now += seconds


def _wait(pr: FakePr, timeout: float = 600):
    return wait_and_merge(
        SHA,
        timeout_seconds=timeout,
        read_pr=pr.read,
        merge=pr.merge,
        sleep=pr.sleep,
        clock=lambda: pr.now,
        log=lambda message: None,
    )


def test_it_waits_until_mergeable_then_merges():
    pr = FakePr([_pr(), _pr(mergeStateStatus="CLEAN")])

    outcome = _wait(pr)

    assert outcome.result == "merged"
    assert pr.merges == 1
    assert outcome.status == ("success", "validated; merged")


def test_unstable_counts_as_mergeable():
    # The gate's own pending status keeps the PR UNSTABLE, never CLEAN.
    pr = FakePr([_pr(mergeStateStatus="UNSTABLE")])

    assert _wait(pr).result == "merged"
    assert pr.merges == 1


def test_a_merge_by_someone_else_at_the_validated_head_counts():
    pr = FakePr([_pr(state="MERGED")])

    assert _wait(pr).result == "merged"
    assert pr.merges == 0


def test_a_merge_at_another_head_is_reported():
    pr = FakePr([_pr(state="MERGED", headRefOid=OTHER)])

    outcome = _wait(pr)

    assert outcome.result == "merged_unvalidated_head"
    assert outcome.status[0] == "failure"


@pytest.mark.parametrize(
    "read,result",
    [
        (_pr(headRefOid=OTHER), "head_moved"),
        (_pr(state="CLOSED"), "closed"),
        (_pr(baseRefName="release"), "pr_changed"),
        (_pr(isCrossRepository=True), "pr_changed"),
    ],
)
def test_a_moved_or_closed_pr_is_never_merged(read, result):
    pr = FakePr([_pr(), read])

    assert _wait(pr).result == result
    assert pr.merges == 0


def test_a_pr_that_never_becomes_mergeable_times_out_without_merging():
    pr = FakePr([_pr(mergeStateStatus="BLOCKED")])

    outcome = _wait(pr, timeout=60)

    assert outcome.result == "not_merged"
    assert outcome.status == ("success", "validated; not merged (BLOCKED)")
    assert pr.merges == 0
    assert pr.now <= 80


def test_a_rejected_merge_is_retried():
    pr = FakePr([_pr(mergeStateStatus="CLEAN")])
    pr.reject_merges = 1

    assert _wait(pr).result == "merged"
    assert pr.merges == 2


def test_a_merge_rejected_three_times_fails():
    pr = FakePr([_pr(mergeStateStatus="CLEAN")])
    pr.reject_merges = 99

    outcome = _wait(pr)

    assert outcome.result == "merge_failed"
    assert pr.merges == 3
    assert outcome.detail == "Pull request is not mergeable"


def test_a_rejection_then_a_timeout_is_a_failed_merge_not_a_quiet_one():
    pr = FakePr([_pr(mergeStateStatus="CLEAN"), _pr(mergeStateStatus="BLOCKED")])
    pr.reject_merges = 1

    outcome = _wait(pr, timeout=60)

    assert outcome.result == "merge_failed"
    assert outcome.detail == "Pull request is not mergeable"


def test_read_errors_are_retried_then_give_up():
    flaky = FakePr(
        [RuntimeError("502"), RuntimeError("502"), RuntimeError("502"), _pr()]
    )
    flaky.reads.append(_pr(mergeStateStatus="CLEAN"))

    assert _wait(flaky).result == "merged"

    broken = FakePr([RuntimeError("502")])
    outcome = _wait(broken)
    assert outcome.result == "watch_error"
    assert outcome.status == ("failure", "validated; watch_error")


def test_read_errors_stop_at_the_deadline():
    pr = FakePr([RuntimeError("502")])

    outcome = _wait(pr, timeout=30)

    assert outcome.result == "watch_error"
    assert pr.now <= 30


_FAKE_GH = """\
import json, os, sys
with open(os.environ["FAKE_GH_LOG"], "a") as log:
    log.write(json.dumps(sys.argv[1:]) + "\\n")
print(os.environ["FAKE_GH_REPLY"])
"""


@pytest.fixture
def fake_gh(tmp_path, monkeypatch):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    executable = bin_dir / "gh"
    executable.write_text(f"#!{sys.executable}\n{_FAKE_GH}")
    executable.chmod(executable.stat().st_mode | stat.S_IXUSR)
    log = tmp_path / "gh.log"
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("FAKE_GH_LOG", str(log))

    def calls() -> list[list[str]]:
        return [json.loads(line) for line in log.read_text().splitlines()]

    return calls


def test_the_merge_is_a_pinned_squash_with_a_fixed_title(fake_gh, monkeypatch):
    monkeypatch.setenv("FAKE_GH_REPLY", json.dumps({"merged": True, "sha": "c" * 40}))

    gh_merge("airbytehq/airbyte-ops-mcp", 12, SHA, "the title", "the message")

    (call,) = fake_gh()
    assert call[:4] == [
        "api",
        "--method",
        "PUT",
        "repos/airbytehq/airbyte-ops-mcp/pulls/12/merge",
    ]
    fields = dict(field.split("=", 1) for field in call[5::2])
    assert fields == {
        "merge_method": "squash",
        "sha": SHA,
        "commit_title": "the title",
        "commit_message": "the message",
    }
    assert "--auto" not in call


def test_a_merge_github_did_not_make_raises(fake_gh, monkeypatch):
    monkeypatch.setenv("FAKE_GH_REPLY", json.dumps({"merged": False, "message": "no"}))

    with pytest.raises(RuntimeError, match="GitHub did not merge: no"):
        gh_merge("airbytehq/airbyte-ops-mcp", 12, SHA, "t", "m")


@pytest.mark.parametrize(
    "overrides",
    [{"sha": "main"}, {"connector": "source-x\nstatus=pass"}, {"case": "../etc"}],
)
def test_the_merge_command_refuses_unchecked_values(overrides):
    from airbyte_ops_mcp.cli.cloud import regression_case_merge

    arguments = {
        "pr": 12,
        "sha": SHA,
        "connector": "source-slack",
        "case": "new-case",
        "repo": "airbytehq/airbyte-ops-mcp",
        **overrides,
    }
    with pytest.raises(SystemExit):
        regression_case_merge(**arguments)
