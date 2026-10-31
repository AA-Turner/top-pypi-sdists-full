# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""`saas-sandbox-pin-bump.yml`'s structure and shell steps, checked without GitHub."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from tests.test_sandbox_case_run_workflow import (
    PIN_BUMP_WORKFLOW,
    REPO_ROOT,
    WORKFLOWS,
    _load,
    _run_script,
    _triggers,
    needs_jq,
)

pytestmark = pytest.mark.unit

PIN = "a" * 40
TARGET = "b" * 40
CASES = [
    "regression_cases/source-slack/threads-fractional-global-cursor",
    "tests/fixtures/regression_cases/source-slack/threads-fractional-cursor-429",
]


def _jobs() -> dict[str, Any]:
    return _load(PIN_BUMP_WORKFLOW)["jobs"]


def _step(job: str, name_or_id: str) -> dict[str, Any]:
    (step,) = [
        step
        for step in _jobs()[job]["steps"]
        if name_or_id in (step.get("id"), step.get("name"))
    ]
    return step


def _repo_copy(tmp_path: Path) -> Path:
    """The pin and two cases' `origin.json`, laid out as in the repository."""
    root = tmp_path / "repo"
    (root / ".github").mkdir(parents=True)
    (root / ".github" / "saas-sandbox-ref").write_text(PIN + "\n")
    for case in CASES:
        (root / case).mkdir(parents=True)
        shutil.copy(REPO_ROOT / case / "origin.json", root / case / "origin.json")
    return root


def _plan(tmp_path: Path, root: Path, main_sha: str) -> dict[str, str]:
    """Run the plan step with a `gh` that reports `main_sha` as saas-sandbox `main`."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    (bin_dir / "gh").write_text(f"#!/bin/sh\necho {main_sha}\n")
    (bin_dir / "gh").chmod(0o755)
    script = f'PATH="{bin_dir}:$PATH"\n' + _step("plan", "plan")["run"]
    completed, outputs = _run_script(script, {}, tmp_path / "plan", cwd=root)
    assert completed.returncode == 0, completed.stderr
    return outputs


def test_runs_weekly_and_only_from_main():
    triggers = _triggers(_load(PIN_BUMP_WORKFLOW))
    preflight = _step("plan", "Preflight")

    assert set(triggers) == {"schedule", "workflow_dispatch"}
    assert preflight["env"]["REF"] == "${{ github.ref }}"
    assert '[ "$REF" = "refs/heads/main" ]' in preflight["run"]


def test_every_case_runs_reproduced_at_the_target():
    cases = _jobs()["cases"]

    assert cases["uses"] == "./.github/workflows/sandbox-case-run.yml"
    assert cases["strategy"]["fail-fast"] is False
    assert cases["with"]["goal"] == "reproduced"
    assert cases["with"]["sandbox_ref"] == "${{ needs.plan.outputs.target }}"


def test_the_merge_needs_every_case_the_switch_and_both_smokes():
    pr = _jobs()["pr"]
    smokes = _step("pr", "smokes")
    automerge = _step("pr", "automerge")

    # The PR is written whatever the cases returned.
    assert "needs.cases.result" not in pr["if"]
    assert smokes["if"] == (
        "steps.bump.outputs.failed == '0'"
        " && vars.SANDBOX_PIN_AUTOBUMP_ENABLED == 'true'"
    )
    assert smokes["env"]["HEAD_SHA"] == "${{ steps.push.outputs.head_sha }}"
    assert "head_sha=$HEAD_SHA" in smokes["run"]
    assert automerge["if"] == "steps.smokes.outcome == 'success'"
    assert '--auto --squash --match-head-commit "$HEAD_SHA"' in automerge["run"]
    # No other step can merge.
    merging = [s.get("id") for s in pr["steps"] if "gh pr merge" in s.get("run", "")]
    assert merging == ["push", "automerge"]
    assert "--disable-auto" in _step("pr", "push")["run"]
    assert _step("pr", "Fail on any failed case")["if"] == "always()"


def test_both_smokes_trigger_on_a_bump_pr():
    """A smoke skipped by `paths` would read as "never started", so check none is."""
    for name in ("sandbox-case-gate-smoke.yml", "sandbox-case-run-smoke.yml"):
        paths = _triggers(_load(WORKFLOWS / name))["pull_request"]["paths"]
        assert ".github/saas-sandbox-ref" in paths, name
        assert name in _step("pr", "smokes")["run"]


@needs_jq
def test_plan_stops_when_the_pin_is_already_at_main(tmp_path):
    assert _plan(tmp_path, _repo_copy(tmp_path), PIN) == {"pin": PIN}


@needs_jq
def test_plan_lists_every_case(tmp_path):
    outputs = _plan(tmp_path, _repo_copy(tmp_path), TARGET)

    assert outputs["target"] == TARGET
    include = json.loads(outputs["matrix"])["include"]
    assert [
        f"{e['case_root']}/{e['connector_name']}/{e['case']}" for e in include
    ] == CASES
    assert [e["result_artifact_name"] for e in include] == ["pin-case-0", "pin-case-1"]
    origin = json.loads((REPO_ROOT / CASES[1] / "origin.json").read_text())
    assert include[1]["control_image"] == origin["affected_image"]
    assert include[1]["connector_ref"] == origin["affected_ref"]


@needs_jq
@pytest.mark.parametrize("second", ["pass", "fail", "missing", "old-sandbox"])
def test_bump_moves_everything_and_fails_unless_every_case_passed(tmp_path, second):
    root = _repo_copy(tmp_path)
    planned = _plan(tmp_path, root, TARGET)
    results = tmp_path / "bump" / "results"
    verdicts = {
        "pass": ("PASS (reproduced)", True),
        "fail": ("FAIL (not reproduced)", False),
    }
    for index, outcome in enumerate(["pass", second]):
        if outcome == "missing":
            continue
        verdict, passed = verdicts.get(outcome, verdicts["pass"])
        sandbox_ref = PIN if outcome == "old-sandbox" else TARGET
        (results / f"pin-case-{index}").mkdir(parents=True)
        (results / f"pin-case-{index}" / "result.json").write_text(
            json.dumps(
                {"verdict": verdict, "passed": passed, "sandbox_ref": sandbox_ref}
            )
        )

    completed, outputs = _run_script(
        _step("pr", "bump")["run"],
        {
            "PIN": PIN,
            "TARGET": TARGET,
            "MATRIX": planned["matrix"],
            "GH_REPO": "airbytehq/airbyte-ops-mcp",
            "GITHUB_SERVER_URL": "https://github.com",
            "GITHUB_RUN_ID": "1",
        },
        tmp_path / "bump",
        cwd=root,
    )

    assert completed.returncode == 0, completed.stderr
    assert outputs == (
        {"failed": "0", "failed_cases": ""}
        if second == "pass"
        else {
            "failed": "1",
            "failed_cases": "source-slack/threads-fractional-cursor-429",
        }
    )
    assert (root / ".github" / "saas-sandbox-ref").read_text() == TARGET + "\n"
    for case in CASES:
        before = (REPO_ROOT / case / "origin.json").read_text()
        after = (root / case / "origin.json").read_text()
        # Only `sandbox_ref` changes, in the files' own formatting.
        assert after == before.replace(json.loads(before)["sandbox_ref"], TARGET)
    body = (tmp_path / "bump" / "body.md").read_text()
    assert f"compare/{PIN}...{TARGET}" in body
    assert body.count("❌") == (0 if second == "pass" else 1)


def _smoke_api(tmp_path: Path, runs: dict[str, list[dict[str, Any]] | None]) -> Path:
    """A `gh` answering the runs endpoint per workflow file, and logging its calls."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for name, workflow_runs in runs.items():
        if workflow_runs is None:
            continue
        (tmp_path / f"{name}.json").write_text(
            json.dumps({"workflow_runs": workflow_runs})
        )
    (bin_dir / "gh").write_text(
        '#!/bin/bash\necho "$2" >> "$GH_LOG"\n'
        # No file for a workflow: the API call fails.
        'name="${2#*/workflows/}"; cat "$GH_DIR/${name%%/*}.json"\n'
    )
    (bin_dir / "gh").chmod(0o755)
    return bin_dir


@needs_jq
@pytest.mark.parametrize(
    "gate,run,failure",
    [
        ("success", "success", None),
        ("success", "failure", "sandbox-case-run-smoke.yml concluded failure"),
        ("cancelled", "success", "sandbox-case-gate-smoke.yml concluded cancelled"),
        (None, "success", "sandbox-case-gate-smoke.yml never started"),
        ("in_progress", "success", "timed out waiting for sandbox-case-gate-smoke.yml"),
        ("api-error", "success", "timed out waiting for sandbox-case-gate-smoke.yml"),
    ],
)
def test_the_smoke_wait_passes_only_when_both_succeeded(tmp_path, gate, run, failure):
    def runs(state: str | None) -> list[dict[str, Any]] | None:
        if state is None:
            return []
        if state == "api-error":
            return None
        if state == "in_progress":
            return [{"run_number": 2, "status": "in_progress", "conclusion": None}]
        # An older success never counts over the newest run.
        return [
            {"run_number": 1, "status": "completed", "conclusion": "success"},
            {"run_number": 2, "status": "completed", "conclusion": state},
        ]

    bin_dir = _smoke_api(
        tmp_path,
        {
            "sandbox-case-gate-smoke.yml": runs(gate),
            "sandbox-case-run-smoke.yml": runs(run),
        },
    )
    completed, outputs = _run_script(
        f'PATH="{bin_dir}:$PATH"\n' + _step("pr", "smokes")["run"],
        {
            "GH_REPO": "airbytehq/airbyte-ops-mcp",
            "GH_DIR": str(tmp_path),
            "GH_LOG": str(tmp_path / "gh.log"),
            "HEAD_SHA": TARGET,
            "SMOKE_TIMEOUT_SECONDS": "0",
            "SMOKE_GRACE_SECONDS": "0",
            "SMOKE_POLL_SECONDS": "0",
        },
        tmp_path / "out",
    )

    assert (completed.returncode == 0) is (failure is None), completed.stdout
    if failure:
        assert outputs["failure"].startswith(failure)
    calls = (tmp_path / "gh.log").read_text()
    assert f"head_sha={TARGET}&event=pull_request" in calls


def _alert(tmp_path: Path, **outputs: str) -> dict[str, Any]:
    """Run the alert step against a `curl` that keeps the payload."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    (bin_dir / "curl").write_text(
        '#!/bin/bash\nfor a in "$@"; do [[ $a == @* ]] && cp "${a#@}" "$PAYLOAD"; done\n'
        "echo '{\"ok\": true}'\n"
    )
    (bin_dir / "curl").chmod(0o755)
    (step,) = _jobs()["alert"]["steps"]
    completed, _outputs = _run_script(
        f'PATH="{bin_dir}:$PATH"\n' + step["run"],
        {
            "PAYLOAD": str(tmp_path / "payload.json"),
            "SLACK_CHANNEL": "U123",
            "SLACK_TOKEN": "xoxb-secret",
            "TARGET": TARGET,
            "RUN_URL": "https://run",
            **outputs,
        },
        tmp_path / "out",
    )
    assert completed.returncode == 0, completed.stderr
    return json.loads((tmp_path / "payload.json").read_text())


def test_the_alert_runs_unless_cancelled_or_already_at_main():
    alert = _jobs()["alert"]
    (step,) = alert["steps"]

    assert alert["needs"] == ["plan", "cases", "pr"]
    assert alert["if"] == (
        "${{ !cancelled() && vars.SLACK_CHANNEL_SANDBOX_CASE_ALERTS != ''"
        " && (needs.plan.result != 'success' || needs.plan.outputs.target != '') }}"
    )
    assert step["continue-on-error"] is True
    assert step["env"]["SLACK_TOKEN"] == "${{ secrets.SLACK_HYDRA_BOT_TOKEN }}"


@needs_jq
@pytest.mark.parametrize(
    "outputs,expected",
    [
        (
            {"PR_RESULT": "success", "AUTO_MERGE": "true", "FAILED": "0"},
            "✅ SaaS Sandbox pin bump bbbbbbbb: every case and both smokes passed;"
            " auto-merge enabled (<https://pr|PR>, <https://run|run>)",
        ),
        (
            {"PR_RESULT": "success", "FAILED": "0"},
            "🔵 SaaS Sandbox pin bump bbbbbbbb: every case passed;"
            " SANDBOX_PIN_AUTOBUMP_ENABLED is off, so the PR waits for a human"
            " (<https://pr|PR>, <https://run|run>)",
        ),
        (
            {
                "PR_RESULT": "failure",
                "FAILED": "2",
                "FAILED_CASES": "source-a/x source-b/<y>",
            },
            "❌ SaaS Sandbox pin bump bbbbbbbb: 2 case(s) failed: source-a/x"
            " source-b/&lt;y&gt; (<https://pr|PR>, <https://run|run>)",
        ),
        (
            {
                "PR_RESULT": "failure",
                "FAILED": "0",
                "SMOKE_FAILURE": "timed out & more",
            },
            "❌ SaaS Sandbox pin bump bbbbbbbb: not merged: timed out &amp; more"
            " (<https://pr|PR>, <https://run|run>)",
        ),
        (
            {
                "PLAN_RESULT": "failure",
                "PR_RESULT": "skipped",
                "PR_URL": "",
                "TARGET": "",
            },
            "❌ SaaS Sandbox pin bump : the run failed (plan: failure, pr: skipped)"
            " (<https://run|run>)",
        ),
    ],
)
def test_the_alert_says_how_the_bump_ended(tmp_path, outputs, expected):
    message = _alert(
        tmp_path, **{"PLAN_RESULT": "success", "PR_URL": "https://pr", **outputs}
    )

    assert message["channel"] == "U123"
    assert message["text"] == expected
