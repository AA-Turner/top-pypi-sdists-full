"""The auto-merge workflows' merge step, run against a fake ``gh``.

``gh pr merge --auto`` is refused with "is in unstable status" when every
required check passed and only a non-required one is still going or failed,
which is the state a job lands in when it starts a minute or two after the
pull request opens. The job used to fail and leave the pull request unmerged
until someone re-ran it. The step now merges directly on "unstable" or
"clean", after confirming GitHub still reports the pull request as one of the
two, and fails with GitHub's own message on anything else. The step's shell is
exercised here, so the decision is tested without GitHub.
"""

from __future__ import annotations

import os
import stat
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
import yaml  # type: ignore[import-untyped]

WORKFLOWS = Path(__file__).resolve().parent.parent / ".github" / "workflows"
MERGE_WORKFLOWS = [
    "release-auto-merge.yml",
    "regenerate-auto-merge.yml",
    "uv-lock-auto-merge.yml",
    "dependabot-auto-merge.yml",
]

PR_URL = "https://github.com/alrayyes/forge-dashboard-sdk-python/pull/280"
UNSTABLE = "GraphQL: Pull request Pull request is in unstable status (enablePullRequestAutoMerge)"
CLEAN = "GraphQL: Pull request Pull request is in clean status (enablePullRequestAutoMerge)"
CONFLICT = "X Pull request #280 is not mergeable: the merge commit cannot be cleanly created."
REQUIRED_PENDING = "X Pull request #280 is not mergeable: 6 of 6 required status checks are expected."


def merge_step_script(workflow: str) -> str:
    """The ``run`` script of the one step that calls ``gh pr merge``."""
    parsed: dict[str, Any] = yaml.safe_load((WORKFLOWS / workflow).read_text())
    scripts = [
        step["run"] for job in parsed["jobs"].values() for step in job["steps"] if "gh pr merge" in step.get("run", "")
    ]
    assert len(scripts) == 1, f"{workflow} should have exactly one merge step"
    return str(scripts[0])


@dataclass
class Answer:
    out: str = ""
    rc: int = 0


@dataclass
class Result:
    code: int
    output: str
    calls: list[str]


FAKE_GH = """#!/usr/bin/env bash
echo "$*" >> "$FAKE_LOG"
if [ "$1 $2" = "pr view" ]; then
  printf '%s\\n' "$FAKE_STATE"
  exit 0
fi
for arg in "$@"; do
  if [ "$arg" = "--auto" ]; then
    printf '%s\\n' "$FAKE_AUTO_OUT"
    exit "$FAKE_AUTO_RC"
  fi
done
printf '%s\\n' "$FAKE_DIRECT_OUT"
exit "$FAKE_DIRECT_RC"
"""


def run_step(
    workflow: str, tmp_path: Path, auto: Answer, direct: Answer | None = None, state: str = "UNSTABLE"
) -> Result:
    direct = direct or Answer()
    gh = tmp_path / "gh"
    gh.write_text(FAKE_GH)
    gh.chmod(gh.stat().st_mode | stat.S_IEXEC)
    log = tmp_path / "calls.log"
    log.write_text("")
    proc = subprocess.run(  # noqa: S603 -- bash running the workflow's own step against a fake gh
        ["bash", "-c", merge_step_script(workflow)],  # noqa: S607
        env={
            "PATH": f"{tmp_path}:{os.environ['PATH']}",
            "PR_URL": PR_URL,
            "GH_TOKEN": "secret-release-token",
            "FAKE_LOG": str(log),
            "FAKE_AUTO_OUT": auto.out,
            "FAKE_AUTO_RC": str(auto.rc),
            "FAKE_DIRECT_OUT": direct.out,
            "FAKE_DIRECT_RC": str(direct.rc),
            "FAKE_STATE": state,
        },
        capture_output=True,
        text=True,
        check=False,
    )
    return Result(proc.returncode, proc.stdout + proc.stderr, [line for line in log.read_text().splitlines() if line])


AUTO_CALL = f"pr merge --auto --squash {PR_URL}"
DIRECT_CALL = f"pr merge --squash {PR_URL}"
VIEW_CALL = f"pr view {PR_URL} --json mergeStateStatus --jq .mergeStateStatus"


@pytest.mark.parametrize("workflow", MERGE_WORKFLOWS)
class TestMergeStep:
    def test_arms_auto_merge_and_stops_when_github_accepts_it(self, workflow: str, tmp_path: Path) -> None:
        result = run_step(workflow, tmp_path, Answer())

        assert result.code == 0
        assert result.calls == [AUTO_CALL]

    @pytest.mark.parametrize(("refusal", "state"), [(UNSTABLE, "UNSTABLE"), (CLEAN, "CLEAN")])
    def test_merges_directly_when_nothing_is_left_to_wait_for(
        self, workflow: str, tmp_path: Path, refusal: str, state: str
    ) -> None:
        result = run_step(workflow, tmp_path, Answer(refusal, 1), state=state)

        assert result.code == 0
        assert result.calls == [AUTO_CALL, VIEW_CALL, DIRECT_CALL]

    @pytest.mark.parametrize("state", ["BLOCKED", "BEHIND", "DIRTY", "UNKNOWN"])
    def test_does_not_merge_directly_if_the_state_changed_in_between(
        self, workflow: str, tmp_path: Path, state: str
    ) -> None:
        # The direct merge is made with a token that can bypass branch
        # protection, so it only runs while GitHub still says nothing is
        # required but the merge itself.
        result = run_step(workflow, tmp_path, Answer(UNSTABLE, 1), state=state)

        assert result.code != 0
        assert result.calls == [AUTO_CALL, VIEW_CALL]
        assert state in result.output

    def test_fails_visibly_and_merges_nothing_on_any_other_refusal(self, workflow: str, tmp_path: Path) -> None:
        result = run_step(workflow, tmp_path, Answer(CONFLICT, 1))

        assert result.code != 0
        assert result.calls == [AUTO_CALL]
        assert "cannot be cleanly created" in result.output

    def test_fails_when_the_direct_merge_is_refused(self, workflow: str, tmp_path: Path) -> None:
        result = run_step(workflow, tmp_path, Answer(UNSTABLE, 1), Answer(REQUIRED_PENDING, 1))

        assert result.code != 0
        assert result.calls == [AUTO_CALL, VIEW_CALL, DIRECT_CALL]
        assert "required status checks" in result.output

    def test_does_not_print_the_token(self, workflow: str, tmp_path: Path) -> None:
        result = run_step(workflow, tmp_path, Answer(UNSTABLE, 1))

        assert "secret-release-token" not in result.output
