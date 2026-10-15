# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""`sandbox-case-run.yml`'s contract with its callers, checked without GitHub.

The input-validation and finalize steps are shell scripts; they run here under
bash with the environment GitHub Actions would give them.
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

from airbyte_ops_mcp.regression_tests.repro_case import (
    ReproCase,
    ReproductionVerdict,
    ReproGoal,
    SideEvaluation,
    SideOutcome,
    case_result,
)

pytestmark = pytest.mark.unit

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = REPO_ROOT / ".github" / "workflows"
RUN_WORKFLOW = WORKFLOWS / "sandbox-case-run.yml"
SMOKE_WORKFLOW = WORKFLOWS / "sandbox-case-run-smoke.yml"
SETUP_ACTION = REPO_ROOT / ".github" / "actions" / "setup-saas-sandbox" / "action.yml"
REFERENCE_CASE = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "regression_cases"
    / "source-slack"
    / "threads-fractional-cursor-429"
)

needs_jq = pytest.mark.skipif(
    shutil.which("jq") is None or shutil.which("bash") is None,
    reason="the workflow's shell steps need bash and jq",
)


def _load(path: Path) -> dict[Any, Any]:
    return yaml.safe_load(path.read_text())


def _triggers(workflow: dict[Any, Any]) -> dict[str, Any]:
    # `on:` parses as the boolean True in YAML 1.1.
    return workflow[True] if True in workflow else workflow["on"]


def _steps(path: Path) -> list[dict[str, Any]]:
    document = _load(path)
    if "runs" in document:
        return document["runs"]["steps"]
    return [step for job in document["jobs"].values() for step in job.get("steps", [])]


def _step(step_id: str) -> dict[str, Any]:
    (step,) = [step for step in _steps(RUN_WORKFLOW) if step.get("id") == step_id]
    return step


def _keys(value: Any) -> Any:
    """The nested key structure of a JSON document, ignoring the values."""
    if isinstance(value, dict):
        return {key: _keys(item) for key, item in value.items()}
    return None


def _shape(document: dict[str, Any]) -> Any:
    """The keys of a result, with `sides` (null when there is no verdict) opaque."""
    return {**_keys(document), "sides": None}


def test_dispatch_and_call_inputs_match():
    """A caller and a dispatcher must be able to pass exactly the same inputs."""
    triggers = _triggers(_load(RUN_WORKFLOW))
    dispatch = triggers["workflow_dispatch"]["inputs"]
    call = triggers["workflow_call"]["inputs"]

    assert set(dispatch) == set(call)
    for name, spec in dispatch.items():
        other = call[name]
        expected_type = "string" if spec["type"] == "choice" else spec["type"]
        assert other["type"] == expected_type, name
        assert other["required"] == spec["required"], name
        assert other.get("default") == spec.get("default"), name


def test_no_expression_is_spliced_into_a_shell_script():
    """Inputs reach the shell through `env`, never through `${{ }}` in `run:`."""
    for path in (RUN_WORKFLOW, SMOKE_WORKFLOW, SETUP_ACTION):
        for step in _steps(path):
            assert "${{" not in step.get("run", ""), (path.name, step.get("name"))


def test_the_sandbox_token_is_revoked_before_the_target_is_checked_out():
    """The target may be a fork PR, so no step from its checkout on holds the token."""
    steps = _steps(RUN_WORKFLOW)
    names = [step.get("name") for step in steps]
    revoke = names.index("Revoke the SaaS Sandbox checkout token")
    users = [
        step.get("name")
        for step in steps
        if "steps.sandbox-token.outputs.token" in yaml.safe_dump(step)
    ]

    assert (
        names.index("Set up SaaS Sandbox") < revoke < names.index("Checkout the target")
    )
    assert users == ["Set up SaaS Sandbox", "Revoke the SaaS Sandbox checkout token"]
    assert steps[revoke]["if"].startswith("always()")
    token_step = next(step for step in steps if step.get("id") == "sandbox-token")
    assert token_step["with"]["skip-token-revoke"] is True


def test_the_sandbox_pin_is_one_full_sha():
    pin = (REPO_ROOT / ".github" / "saas-sandbox-ref").read_text()

    assert re.fullmatch(r"[0-9a-f]{40}\n?", pin)


def test_the_smoke_runs_the_reference_case_under_distinct_artifact_names():
    jobs = _load(SMOKE_WORKFLOW)["jobs"]
    calls = [job["with"] for job in jobs.values() if "uses" in job]

    assert {call["goal"] for call in calls} == {"fixed", "reproduced"}
    # One call reads the case from a commit, as validate does.
    assert [bool(call.get("case_ref")) for call in calls].count(True) == 1
    names = [call["result_artifact_name"] for call in calls]
    assert len(set(names)) == len(names)
    for call in calls:
        case_dir = REPO_ROOT / call["case_root"] / call["connector_name"] / call["case"]
        assert case_dir == REFERENCE_CASE
    assert ReproCase.load(REFERENCE_CASE).primary_keys


def _run_script(
    script: str, env: dict[str, str], tmp_path: Path, cwd: Path = REPO_ROOT
) -> tuple[subprocess.CompletedProcess[str], dict[str, str]]:
    tmp_path.mkdir(parents=True, exist_ok=True)
    github_output = tmp_path / "github_output"
    github_output.touch()
    completed = subprocess.run(
        ["bash", "-e", "-c", script],
        cwd=cwd,
        env={
            "PATH": os.environ["PATH"],
            "RUNNER_TEMP": str(tmp_path),
            "GITHUB_OUTPUT": str(github_output),
            "GITHUB_STEP_SUMMARY": str(tmp_path / "summary.md"),
            **env,
        },
        capture_output=True,
        text=True,
        check=False,
    )
    outputs = dict(
        line.split("=", 1) for line in github_output.read_text().splitlines()
    )
    return completed, outputs


_VALID_INPUTS = {
    "CONNECTOR_NAME": "source-slack",
    "CASE_NAME": "threads-fractional-cursor",
    "GOAL": "fixed",
    "CONTROL_IMAGE": "airbyte/source-slack:3.2.19",
    "PR": "84839",
    "CONNECTOR_REF": "",
    "CASE_REF": "",
    "CASE_ROOT": "regression_cases",
    "RESULT_ARTIFACT_NAME": "sandbox-case-result",
    "REQUEST_ID": "",
}


@needs_jq
def test_valid_inputs_resolve_the_target_and_case(tmp_path):
    completed, outputs = _run_script(_step("inputs")["run"], _VALID_INPUTS, tmp_path)

    assert completed.returncode == 0, completed.stdout
    assert outputs == {
        "artifact_name": "sandbox-case-result",
        "target_ref": "refs/pull/84839/head",
        "case_path": "regression_cases/source-slack/threads-fractional-cursor",
    }

    sha = "4d07056bddb097a417c5c8895a3885ae25a24628"
    _completed, outputs = _run_script(
        _step("inputs")["run"],
        {**_VALID_INPUTS, "PR": "", "CONNECTOR_REF": sha},
        tmp_path / "ref",
    )
    assert outputs["target_ref"] == sha


@needs_jq
@pytest.mark.parametrize(
    "changes",
    [
        {"CONNECTOR_NAME": "../source-slack"},
        {"CASE_NAME": "a/b"},
        {"CASE_NAME": "x; rm -rf /"},
        {"GOAL": "anything"},
        {"CASE_ROOT": "src"},
        {"CASE_ROOT": "regression_cases/../src"},
        {"CONTROL_IMAGE": "airbyte/source-stripe:1.0.0"},
        {"CONTROL_IMAGE": "evil/source-slack:3.2.19"},
        {"PR": ""},
        {"PR": "84839", "CONNECTOR_REF": "4d07056bddb097a417c5c8895a3885ae25a24628"},
        {"PR": "", "CONNECTOR_REF": "master"},
        {"PR": "84839 --extra"},
        {"CASE_REF": "main"},
        {"RESULT_ARTIFACT_NAME": "Bad Name"},
        {"REQUEST_ID": "a b"},
    ],
)
def test_invalid_inputs_stop_the_run(tmp_path, changes):
    completed, outputs = _run_script(
        _step("inputs")["run"], {**_VALID_INPUTS, **changes}, tmp_path
    )

    assert completed.returncode != 0
    assert "case_path" not in outputs
    assert (tmp_path / "sandbox-case-error").read_text().startswith("invalid inputs:")
    # The record of a rejected run still goes out under the caller's name.
    if "RESULT_ARTIFACT_NAME" not in changes:
        assert outputs["artifact_name"] == "sandbox-case-result"
    else:
        assert "artifact_name" not in outputs


def _finalize_env(tmp_path: Path, **overrides: str) -> dict[str, str]:
    return {
        **_VALID_INPUTS,
        "INPUTS_OUTCOME": "success",
        "READ_STARTED": "true",
        "OUTPUT_DIR": str(tmp_path / "out"),
        "CASE_SOURCE_REF": "a" * 40,
        "TARGET_COMMIT": "b" * 40,
        "READ_EXIT_CODE": "0",
        "RUN_URL": "https://github.com/airbytehq/airbyte-ops-mcp/actions/runs/1",
        "SANDBOX_REF": "c" * 40,
        **overrides,
    }


def _verdict(label: str = "PASS (reproduced and fixed)") -> dict[str, Any]:
    verdict = ReproductionVerdict(
        success=label.startswith("PASS"),
        regression_detected=False,
        label=label,
        detail="control violates; target satisfies",
        control=SideEvaluation(SideOutcome.VIOLATES, "crashed with the expected error"),
        target=SideEvaluation(
            SideOutcome.TWIN_GAP, "twin gap", ("GET /api/x: unsupported",)
        ),
        goal=ReproGoal.FIXED,
    )
    return case_result(
        verdict,
        ReproCase.load(REFERENCE_CASE),
        control_image="airbyte/source-slack:3.2.19",
        target_image="airbyte/source-slack:dev",
    )


def test_the_smoke_checks_every_result_key():
    """The smoke's `assert` job pins the key list; it must follow the contract."""
    (check,) = [
        step["run"]
        for step in _load(SMOKE_WORKFLOW)["jobs"]["assert"]["steps"]
        if "run" in step
    ]

    for key in _verdict():
        assert f'"{key}"' in check, key
    assert ".sandbox_ref == $pin" in check


def test_a_case_result_lists_the_twin_gaps_and_both_sides():
    result = _verdict()

    assert result["twin_gaps"] == ["GET /api/x: unsupported"]
    assert result["sides"]["target"]["outcome"] == "twin_gap"
    assert result["case"] == {
        "connector": "source-slack",
        "name": "threads-fractional-cursor-429",
        "root": None,
        "ref": None,
    }


@needs_jq
def test_finalize_completes_the_clis_result(tmp_path):
    (tmp_path / "out").mkdir()
    (tmp_path / "out" / "result.json").write_text(json.dumps(_verdict()))

    completed, outputs = _run_script(
        _step("finalize")["run"], _finalize_env(tmp_path), tmp_path
    )

    assert completed.returncode == 0, completed.stderr
    assert outputs == {"verdict": "PASS (reproduced and fixed)", "passed": "true"}
    result = json.loads((tmp_path / "out" / "result.json").read_text())
    assert result["case"]["root"] == "regression_cases"
    assert result["case"]["ref"] == "a" * 40
    assert result["target"] == {
        "image": "airbyte/source-slack:dev",
        "pr": 84839,
        "connector_ref": None,
        "commit": "b" * 40,
    }
    assert result["run_url"].endswith("/runs/1")
    assert result["sandbox_ref"] == "c" * 40
    summary = (tmp_path / "summary.md").read_text()
    assert "GET /api/x: unsupported" in summary
    assert "c" * 40 in summary


@needs_jq
def test_finalize_writes_an_error_result_when_there_is_no_verdict(tmp_path):
    (tmp_path / "sandbox-case-error").write_text("case regression_cases/x not found")

    completed, outputs = _run_script(
        _step("finalize")["run"],
        _finalize_env(
            tmp_path,
            READ_EXIT_CODE="",
            READ_STARTED="",
            TARGET_COMMIT="",
            SANDBOX_REF="",
        ),
        tmp_path,
        # Nothing from the checkout is needed, e.g. when it never happened.
        cwd=tmp_path,
    )

    assert completed.returncode == 0, completed.stderr
    assert outputs == {"verdict": "ERROR", "passed": "false"}
    result = json.loads((tmp_path / "out" / "result.json").read_text())
    assert _shape(result) == _shape(_verdict())
    assert result["error"] == "case regression_cases/x not found"
    assert result["sides"] is None
    assert result["target"]["commit"] is None
    # The sandbox was never set up, so no commit of it was used.
    assert result["sandbox_ref"] is None
    assert result["control"]["image"] == "airbyte/source-slack:3.2.19"


@needs_jq
@pytest.mark.parametrize(
    "content",
    [
        json.dumps({**_verdict(), "verdict": "PASS (trust me)", "passed": True}),
        json.dumps({**_verdict(), "passed": "yes"}),
        '{"verdict": "PASS (reproduced and fixed)", "passed": tr',
    ],
    ids=["unknown-verdict", "non-boolean-passed", "truncated"],
)
def test_finalize_replaces_a_result_that_is_not_a_known_verdict(tmp_path, content):
    """The outputs and the uploaded record must agree, so a bad record is replaced."""
    (tmp_path / "out").mkdir()
    (tmp_path / "out" / "result.json").write_text(content)

    completed, outputs = _run_script(
        _step("finalize")["run"], _finalize_env(tmp_path), tmp_path
    )

    assert completed.returncode == 0, completed.stderr
    assert outputs == {"verdict": "ERROR", "passed": "false"}
    result = json.loads((tmp_path / "out" / "result.json").read_text())
    assert (result["verdict"], result["passed"]) == ("ERROR", False)
    assert "unreadable result.json" in result["error"]
    assert _shape(result) == _shape(_verdict())


@needs_jq
@pytest.mark.parametrize(
    "changes,error",
    [
        ({"READ_EXIT_CODE": "", "READ_STARTED": "true"}, "READ did not finish"),
        ({"READ_EXIT_CODE": "1"}, "READ produced no verdict (exit code 1)"),
        ({"READ_EXIT_CODE": "", "READ_STARTED": ""}, "stopped before READ"),
    ],
)
def test_finalize_says_where_a_run_without_a_verdict_stopped(tmp_path, changes, error):
    _completed, outputs = _run_script(
        _step("finalize")["run"], _finalize_env(tmp_path, **changes), tmp_path
    )

    assert outputs["verdict"] == "ERROR"
    result = json.loads((tmp_path / "out" / "result.json").read_text())
    assert error in result["error"]


@needs_jq
def test_finalize_survives_rejected_inputs(tmp_path):
    """A malformed input must not break the record or reach the summary unfenced."""
    (tmp_path / "sandbox-case-error").write_text("invalid inputs: bad pr")

    completed, outputs = _run_script(
        _step("finalize")["run"],
        _finalize_env(
            tmp_path,
            INPUTS_OUTCOME="failure",
            READ_EXIT_CODE="",
            READ_STARTED="",
            PR="abc](https://evil.example)",
            CASE_SOURCE_REF="",
            TARGET_COMMIT="",
        ),
        tmp_path,
        cwd=tmp_path,
    )

    assert completed.returncode == 0, completed.stderr
    assert outputs == {"verdict": "ERROR", "passed": "false"}
    result = json.loads((tmp_path / "out" / "result.json").read_text())
    assert _shape(result) == _shape(_verdict())
    assert result["target"]["pr"] is None
    assert result["run_url"].endswith("/runs/1")
    assert not list((tmp_path / "out").glob("*.tmp"))
    assert "evil.example" not in (tmp_path / "summary.md").read_text()
