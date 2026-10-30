# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""`sandbox-case-validate.yml`'s wiring, checked without GitHub.

The workflow is dispatch-only and refuses any ref but `main`, so it cannot run
before it merges. Its decisions are unit-tested in `test_case_validate.py`;
these tests pin the wiring around them: what triggers it, which job may hold
which token, and that its calls match `sandbox-case-run.yml`'s contract.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

import pytest
import yaml

pytestmark = pytest.mark.unit

WORKFLOWS = Path(__file__).resolve().parents[1] / ".github" / "workflows"
VALIDATE_WORKFLOW = WORKFLOWS / "sandbox-case-validate.yml"
RUN_WORKFLOW = WORKFLOWS / "sandbox-case-run.yml"
SMOKE_WORKFLOW = WORKFLOWS / "sandbox-case-gate-smoke.yml"
REPRODUCE_JOBS = ("reproduce-1", "reproduce-2")


def _load(path: Path) -> dict[Any, Any]:
    return yaml.safe_load(path.read_text())


def _triggers(workflow: dict[Any, Any]) -> dict[str, Any]:
    # `on:` parses as the boolean True in YAML 1.1.
    return workflow[True] if True in workflow else workflow["on"]


@pytest.fixture(scope="module")
def workflow() -> dict[Any, Any]:
    return _load(VALIDATE_WORKFLOW)


def _step(job: dict[str, Any], step_id: str) -> dict[str, Any]:
    (step,) = [step for step in job["steps"] if step.get("id") == step_id]
    return step


def test_it_can_only_be_dispatched(workflow):
    assert set(_triggers(workflow)) == {"workflow_dispatch"}
    assert set(_triggers(workflow)["workflow_dispatch"]["inputs"]) == {"pr"}
    assert workflow["run-name"] == "Validate case PR #${{ inputs.pr }}"


def test_runs_for_one_pr_queue_instead_of_cancelling(workflow):
    assert workflow["concurrency"] == {
        "group": "sandbox-case-validate-${{ inputs.pr }}",
        "cancel-in-progress": False,
    }
    assert workflow["permissions"] == {"contents": "read"}


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
@pytest.mark.parametrize(
    "ref,pr,expected",
    [
        ("refs/heads/main", "12", "ok"),
        ("refs/heads/feature", "12", "refused"),
        ("refs/heads/main", "12; rm -rf /", "refused"),
        ("refs/heads/main", "012", "refused"),
    ],
)
def test_preflight_refuses_other_refs_and_odd_pr_numbers(
    workflow, tmp_path, ref, pr, expected
):
    preflight = workflow["jobs"]["gate"]["steps"][0]
    assert preflight["id"] == "preflight"
    output = tmp_path / "output"
    result = subprocess.run(
        ["bash", "-e", "-c", preflight["run"]],
        env={
            "REF": ref,
            "PR": pr,
            "GITHUB_OUTPUT": str(output),
            "PATH": "/usr/bin:/bin",
        },
        capture_output=True,
        text=True,
    )
    assert output.read_text() == f"preflight={expected}\n"
    assert (result.returncode == 0) == (expected == "ok")


def test_the_reproduce_calls_match_the_run_workflow_contract(workflow):
    call = _triggers(_load(RUN_WORKFLOW))["workflow_call"]
    declared_inputs = set(call["inputs"])
    declared_secrets = set(call.get("secrets") or {})
    run_permissions = _load(RUN_WORKFLOW)["permissions"]
    artifact_names = set()
    for name in REPRODUCE_JOBS:
        job = workflow["jobs"][name]
        assert job["uses"] == "./.github/workflows/sandbox-case-run.yml"
        assert job["needs"] == "gate"
        assert "needs.gate.outputs.status == 'pass'" in job["if"]
        # An undeclared input fails the whole run at startup.
        assert set(job["with"]) <= declared_inputs
        required = {key for key, spec in call["inputs"].items() if spec.get("required")}
        assert required <= set(job["with"])
        # An explicit map, not `inherit`: only the secrets the callee declares.
        assert set(job["secrets"]) == declared_secrets
        # A called workflow cannot get more than its caller grants.
        assert job["permissions"] == run_permissions
        assert job["with"]["goal"] == "reproduced"
        assert job["with"]["case_ref"] == "${{ needs.gate.outputs.head_sha }}"
        assert (
            job["with"]["control_image"] == "${{ needs.gate.outputs.affected_image }}"
        )
        assert job["with"]["connector_ref"] == "${{ needs.gate.outputs.affected_ref }}"
        artifact_names.add(job["with"]["result_artifact_name"])
    assert len(artifact_names) == len(REPRODUCE_JOBS)


def test_finalize_skips_cancelled_and_refused_runs(workflow):
    finalize = workflow["jobs"]["finalize"]
    assert set(finalize["needs"]) == {"gate", *REPRODUCE_JOBS}
    assert "!cancelled()" in finalize["if"]
    assert "needs.gate.outputs.preflight == 'ok'" in finalize["if"]
    assert "needs.gate.outputs.head_sha != ''" in finalize["if"]
    assert finalize["timeout-minutes"] <= 20


def test_only_finalize_mints_a_write_token_and_only_to_merge(workflow):
    for name, job in workflow["jobs"].items():
        for step in job.get("steps", []):
            if "create-github-app-token" not in step.get("uses", ""):
                continue
            permissions = {k for k in step["with"] if k.startswith("permission-")}
            if permissions == {"permission-contents"} and (
                step["with"]["permission-contents"] == "read"
            ):
                assert step["with"]["repositories"] == "saas-sandbox"
                continue
            assert name == "finalize"
            assert step["id"] == "token"
            assert step["if"] == "steps.decide.outputs.action == 'merge'"
    finalize = workflow["jobs"]["finalize"]
    step_ids = [step.get("id") for step in finalize["steps"]]
    assert step_ids.index("decide") < step_ids.index("token") < step_ids.index("merge")
    merge = _step(finalize, "merge")
    assert merge["env"]["GH_TOKEN"] == "${{ steps.token.outputs.token }}"
    decide = _step(finalize, "decide")
    assert (
        "vars.SANDBOX_CASE_AUTOMERGE_ENABLED == 'true'"
        in decide["env"]["MERGE_ENABLED"]
    )


def test_merging_only_goes_through_the_merge_command(workflow):
    text = VALIDATE_WORKFLOW.read_text()
    assert "gh pr merge" not in text
    assert "--auto" not in text
    merge = _step(workflow["jobs"]["finalize"], "merge")
    assert "regression-case-merge" in merge["run"]
    # The fixed commit title is built from the gate's checked outputs.
    assert merge["env"]["CONNECTOR"] == "${{ needs.gate.outputs.connector }}"
    assert merge["env"]["CASE_NAME"] == "${{ needs.gate.outputs.case }}"


def test_the_status_is_always_finalized(workflow):
    finalize = workflow["jobs"]["finalize"]
    final = [
        step
        for step in finalize["steps"]
        if "statuses/" in step.get("run", "")
        and step.get("if", "").startswith("always()")
    ]
    assert len(final) == 2  # the validation status and the merge status


def test_no_expression_is_spliced_into_a_shell_script(workflow):
    # PR-derived values reach scripts through `env:` only, so a crafted value
    # cannot become shell code.
    for path in (VALIDATE_WORKFLOW, SMOKE_WORKFLOW):
        document = _load(path)
        for job in document["jobs"].values():
            for step in job.get("steps", []):
                assert "${{" not in step.get("run", ""), (path.name, step.get("name"))


def test_the_smoke_never_merges_or_runs_a_case():
    smoke = _load(SMOKE_WORKFLOW)
    assert set(_triggers(smoke)) == {"pull_request", "workflow_dispatch"}
    text = SMOKE_WORKFLOW.read_text()
    assert "permission-contents: write" not in text
    assert "sandbox-case-run.yml" not in text
    (job,) = smoke["jobs"].values()
    assert re.search(
        r"--case-dir tests/fixtures/regression_cases/", job["steps"][-1]["run"]
    )


def _alert_step(workflow: dict[Any, Any]) -> dict[str, Any]:
    (step,) = [
        step
        for step in workflow["jobs"]["finalize"]["steps"]
        if step.get("name") == "Alert on Slack"
    ]
    return step


def test_the_slack_alert_is_last_optional_and_cannot_fail_the_run(workflow):
    step = _alert_step(workflow)
    assert workflow["jobs"]["finalize"]["steps"][-1] is step
    assert step["if"] == (
        "${{ !cancelled() && vars.SLACK_CHANNEL_SANDBOX_CASE_ALERTS != '' }}"
    )
    assert step["continue-on-error"] is True
    assert step["env"]["SLACK_TOKEN"] == "${{ secrets.SLACK_HYDRA_BOT_TOKEN }}"


@pytest.mark.skipif(
    shutil.which("bash") is None or shutil.which("jq") is None,
    reason="needs bash and jq",
)
@pytest.mark.parametrize(
    "outputs,expected",
    [
        (
            {
                "ACTION": "merge",
                "MERGE_OUTCOME": "merged",
                "MERGE_DESCRIPTION": "validated; merged",
            },
            "✅ Case PR <https://github.com/o/r/pull/12|#12>: validated; merged (<https://run|run>)",
        ),
        (
            {
                "ACTION": "fail",
                "DESCRIPTION": "validation failed: <!channel> & <https://x|y>",
            },
            "❌ Case PR <https://github.com/o/r/pull/12|#12>: validation failed: "
            "&lt;!channel&gt; &amp; &lt;https://x|y&gt; (<https://run|run>)",
        ),
        (
            {},
            "❌ Case PR <https://github.com/o/r/pull/12|#12>: validation could not decide (<https://run|run>)",
        ),
    ],
)
def test_the_slack_alert_escapes_the_description(workflow, tmp_path, outputs, expected):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    payload = tmp_path / "payload.json"
    # Keeps the posted payload and answers like Slack.
    curl = bin_dir / "curl"
    curl.write_text(
        '#!/bin/bash\nfor a in "$@"; do [[ $a == @* ]] && cp "${a#@}" "$PAYLOAD"; done\n'
        'echo \'{"ok": false, "error": "channel_not_found"}\'\n'
    )
    curl.chmod(0o755)
    result = subprocess.run(
        ["bash", "-e", "-c", _alert_step(workflow)["run"]],
        env={
            "PATH": f"{bin_dir}:{os.environ.get('PATH', '/usr/bin:/bin')}",
            "PAYLOAD": str(payload),
            "RUNNER_TEMP": str(tmp_path),
            "SLACK_CHANNEL": "U123",
            "SLACK_TOKEN": "xoxb-secret",
            "PR": "12",
            "GITHUB_SERVER_URL": "https://github.com",
            "GH_REPO": "o/r",
            "RUN_URL": "https://run",
            **outputs,
        },
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "::warning::Slack alert not sent: channel_not_found" in result.stdout
    assert "xoxb-secret" not in result.stdout + result.stderr
    message = json.loads(payload.read_text())
    assert message["channel"] == "U123"
    assert message["text"] == expected
