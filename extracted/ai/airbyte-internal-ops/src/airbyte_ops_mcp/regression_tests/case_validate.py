# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""The decisions `sandbox-case-validate.yml` makes after the gate and the runs.

A dispatch-only workflow cannot run before it is on `main`, so the logic that
decides whether a case PR merges lives here, where it is unit-tested, and the
workflow only wires it up:

- `decide_validation`: from the gate report, the two `reproduced` runs and a
  fresh read of the PR, whether to fail (status + comment), only report (the
  merge switch is off) or merge.
- `wait_and_merge`: wait, for a bounded time, until GitHub reports the PR
  mergeable, then squash-merge it through the REST merge endpoint pinned to
  the validated head (`sha`). That endpoint never enables auto-merge or
  enqueues the PR, so nothing is left armed and a push after validation
  cannot merge an unvalidated head.
"""

from __future__ import annotations

import json
import subprocess
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import asdict, dataclass
from typing import Any, Literal

COMMENT_MARKER = "<!-- sandbox-case-validate:failed {sha} -->"
# GitHub rejects longer commit status descriptions.
STATUS_DESCRIPTION_LIMIT = 140
# `UNSTABLE` must count: the gate's own `pending` status (not a required
# check) keeps a case PR out of `CLEAN` for the whole run. GitHub still
# enforces the ruleset on the merge itself.
MERGEABLE_STATES = frozenset({"CLEAN", "UNSTABLE", "HAS_HOOKS"})
REPRODUCE_JOBS = ("reproduce-1", "reproduce-2")

Action = Literal["fail", "report", "merge"]
StatusState = Literal["pending", "success", "failure"]
MergeResult = Literal[
    "merged",
    "not_merged",
    "merged_unvalidated_head",
    "head_moved",
    "closed",
    "pr_changed",
    "merge_failed",
    "watch_error",
]
SUCCESSFUL_MERGE_RESULTS = frozenset({"merged", "not_merged"})


def _description(text: str) -> str:
    text = " ".join(text.split())
    if len(text) <= STATUS_DESCRIPTION_LIMIT:
        return text
    return text[: STATUS_DESCRIPTION_LIMIT - 1] + "…"


@dataclass(frozen=True)
class Decision:
    action: Action
    state: StatusState
    description: str
    comment: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def pr_problems(pr: Mapping[str, Any] | None, validated_sha: str) -> list[str]:
    """Why the PR, as it is now, may no longer merge the validated head."""
    if pr is None:
        return ["could not re-read the PR"]
    problems = []
    if pr.get("state") != "OPEN":
        problems.append(f"the PR is {str(pr.get('state', 'unknown')).lower()}")
    if pr.get("headRefOid") != validated_sha:
        problems.append(
            f"the PR head moved from {validated_sha} to {pr.get('headRefOid')}"
        )
    if pr.get("baseRefName") != "main":
        problems.append(f"the PR targets {pr.get('baseRefName')!r}, not 'main'")
    if pr.get("isCrossRepository") is not False:
        problems.append("the PR head is not a branch of this repository")
    return problems


def _comment(validated_sha: str, reasons: Sequence[str], run_url: str) -> str:
    # Reasons quote PR content, so they go in a code block: no mentions, links
    # or markup from a case can reach the comment.
    body = "\n".join(f"- {reason}" for reason in reasons).replace("```", "'''")
    return (
        f"{COMMENT_MARKER.format(sha=validated_sha)}\n"
        f"**Sandbox case validation failed** for {validated_sha}.\n\n"
        f"```text\n{body}\n```\n\n"
        f"Run: {run_url}\n"
    )


def decide_validation(
    *,
    gate: Mapping[str, Any] | None,
    gate_refusal: str | None,
    runs: Mapping[str, tuple[str, str, str]],
    pr: Mapping[str, Any] | None,
    validated_sha: str,
    merge_enabled: bool,
    run_url: str,
) -> Decision:
    """What `finalize` does for one validate run.

    `gate` is the gate's JSON report, or None when the gate job stopped before
    writing one (then `gate_refusal` says why). `runs` maps each reproduce job
    to its `(result, verdict, passed)`; `pr` is a fresh read of the PR.
    """
    reasons: list[str] = []
    if gate is None:
        reasons.append(gate_refusal or "the gate produced no report")
    elif gate.get("status") != "pass":
        reasons += gate.get("problems") or [f"the gate says {gate.get('status')}"]
    else:
        for job in REPRODUCE_JOBS:
            result, verdict, passed = runs.get(job, ("", "", ""))
            # The run's `passed` output backs up its job result.
            if result != "success" or passed != "true":
                reasons.append(
                    f"{job}: {verdict or 'no verdict'} ({result or 'not run'})"
                )
    reasons += pr_problems(pr, validated_sha)
    if reasons:
        return Decision(
            action="fail",
            state="failure",
            description=_description(f"validation failed: {reasons[0]}"),
            comment=_comment(validated_sha, reasons, run_url),
        )
    if not merge_enabled:
        return Decision("report", "success", "validated; auto-merge off")
    return Decision("merge", "pending", "validated; merging")


@dataclass(frozen=True)
class MergeOutcome:
    result: MergeResult
    merge_state: str | None = None
    detail: str | None = None

    @property
    def succeeded(self) -> bool:
        return self.result in SUCCESSFUL_MERGE_RESULTS

    @property
    def status(self) -> tuple[StatusState, str]:
        """The final commit status for this outcome."""
        if self.result == "merged":
            return "success", "validated; merged"
        if self.result == "not_merged":
            return "success", f"validated; not merged ({self.merge_state})"
        return "failure", _description(f"validated; {self.result}")

    def to_dict(self) -> dict[str, Any]:
        state, description = self.status
        return {**asdict(self), "state": state, "description": description}


def wait_and_merge(
    validated_sha: str,
    *,
    timeout_seconds: float,
    read_pr: Callable[[], Mapping[str, Any]],
    merge: Callable[[], None],
    sleep: Callable[[float], None] = time.sleep,
    clock: Callable[[], float] = time.monotonic,
    poll_seconds: float = 20,
    max_read_errors: int = 3,
    max_merge_attempts: int = 3,
    log: Callable[[str], None] = print,
) -> MergeOutcome:
    """Merge the PR at `validated_sha` once GitHub reports it mergeable.

    `read_pr` returns the fields `gh_read_pr` reads. `merge` merges pinned to
    `validated_sha` and raises if GitHub refuses, so a head that moves between
    a read and the merge makes the merge fail instead of landing it; when it
    returns, the PR is merged at that head.
    """
    deadline = clock() + timeout_seconds
    read_errors = 0
    merge_attempts = 0
    merge_state: str | None = None
    last_rejection: str | None = None

    def wait() -> None:
        sleep(max(0.0, min(poll_seconds, deadline - clock())))

    while True:
        try:
            pr = read_pr()
        except Exception as exc:
            read_errors += 1
            log(f"could not read the PR ({read_errors} in a row): {exc}")
            if read_errors > max_read_errors or clock() >= deadline:
                return MergeOutcome("watch_error", merge_state, str(exc))
            wait()
            continue
        read_errors = 0
        if pr.get("state") == "MERGED":
            # Merged by someone else meanwhile; only the validated head counts.
            if pr.get("headRefOid") == validated_sha:
                return MergeOutcome("merged", merge_state)
            return MergeOutcome(
                "merged_unvalidated_head", merge_state, str(pr.get("headRefOid"))
            )
        problems = pr_problems(pr, validated_sha)
        if problems:
            result: MergeResult = "pr_changed"
            if pr.get("state") != "OPEN":
                result = "closed"
            elif pr.get("headRefOid") != validated_sha:
                result = "head_moved"
            return MergeOutcome(result, merge_state, "; ".join(problems))
        merge_state = pr.get("mergeStateStatus")
        if merge_state in MERGEABLE_STATES:
            if merge_attempts >= max_merge_attempts:
                return MergeOutcome("merge_failed", merge_state, last_rejection)
            merge_attempts += 1
            try:
                merge()
            except Exception as exc:
                last_rejection = str(exc)
                log(f"merge attempt {merge_attempts} was rejected: {exc}")
            else:
                return MergeOutcome("merged", merge_state)
        if clock() >= deadline:
            if last_rejection is not None:
                return MergeOutcome("merge_failed", merge_state, last_rejection)
            return MergeOutcome("not_merged", merge_state)
        wait()


def _gh(*arguments: str) -> str:
    result = subprocess.run(
        ["gh", *arguments], capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"`gh {' '.join(arguments[:2])}` exited {result.returncode}: "
            + result.stderr.strip()[-500:]
        )
    return result.stdout


def gh_read_pr(repo: str, pr: int) -> dict[str, Any]:
    """The PR fields the decisions read, through `gh`."""
    return json.loads(
        _gh(
            "pr",
            "view",
            str(pr),
            "--repo",
            repo,
            "--json",
            "state,headRefOid,baseRefName,isCrossRepository,mergeStateStatus",
        )
    )


def gh_merge(repo: str, pr: int, validated_sha: str, title: str, message: str) -> None:
    """Squash-merge through the REST endpoint, pinned to `validated_sha`.

    Unlike `gh pr merge`, it never enables auto-merge or enqueues the PR when
    it cannot merge now; it refuses instead. The squash commit gets a fixed
    title and message rather than the PR's author-controlled ones.
    """
    response = json.loads(
        _gh(
            "api",
            "--method",
            "PUT",
            f"repos/{repo}/pulls/{pr}/merge",
            "-f",
            "merge_method=squash",
            "-f",
            f"sha={validated_sha}",
            "-f",
            f"commit_title={title}",
            "-f",
            f"commit_message={message}",
        )
    )
    if response.get("merged") is not True:
        raise RuntimeError(f"GitHub did not merge: {response.get('message')}")


def runs_from_needs(needs: Mapping[str, Any]) -> dict[str, tuple[str, str, str]]:
    """Each reproduce job's `(result, verdict, passed)` from the workflow's `needs`."""
    runs = {}
    for job in REPRODUCE_JOBS:
        entry = needs.get(job) or {}
        outputs = entry.get("outputs") or {}
        runs[job] = (
            str(entry.get("result") or ""),
            str(outputs.get("verdict") or ""),
            str(outputs.get("passed") or ""),
        )
    return runs
