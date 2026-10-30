# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""EU Cloud Batch runner contract tests (S6, S11, S13, S14)."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path
from typing import NamedTuple
from urllib.parse import unquote, urlsplit

import pytest
import yaml

from airbyte_ops_mcp.regression_tests.eu_runner.job_spec import (
    build_batch_job,
    validate_environment,
)
from airbyte_ops_mcp.regression_tests.eu_runner.timeouts import (
    max_run_duration_seconds,
)
from airbyte_ops_mcp.regression_tests.eu_runner.verdict import build_verdict

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/connector-regression-test.yml"
VM_SCRIPT = ROOT / "src/airbyte_ops_mcp/regression_tests/eu_runner/vm-run.sh"


def _workflow() -> dict:
    return yaml.safe_load(WORKFLOW.read_text())


def _eu_job() -> dict:
    return _workflow()["jobs"]["regression-test-eu"]


def _selected_vm_commands(has_connection_id: bool, skip_read: bool) -> list[str]:
    text = VM_SCRIPT.read_text()
    start = text.index("select_commands() {")
    end = text.index("\n}\n", start) + 2
    function = text[start:end]
    result = subprocess.run(
        [
            "bash",
            "-c",
            (
                f'{function}\nselect_commands "$HAS_CONNECTION_ID" "$SKIP_READ"\n'
                + 'printf "%s\\n" "${COMMANDS[@]}"'
            ),
        ],
        env={
            **os.environ,
            "HAS_CONNECTION_ID": str(has_connection_id).lower(),
            "SKIP_READ": str(skip_read).lower(),
        },
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.splitlines()


CLEANUP_IF = (
    "cancelled() || steps.submit-batch.outcome == 'failure' "
    "|| steps.wait-batch.outcome == 'failure'"
)


def _cleanup_step() -> dict:
    (step,) = [
        step
        for step in _eu_job()["steps"]
        if "gcloud batch jobs delete" in step.get("run", "")
    ]
    return step


class _BatchStepRun(NamedTuple):
    returncode: int
    outputs: list[str]
    summary: str
    gcloud_calls: list[str]
    sleeps: list[str]


def _run_batch_step(run: str, tmp_path: Path, states: list[str], **env: str):
    """Run a Batch step's script with `gcloud` and `sleep` stubbed.

    Each `describe` answers with the next of `states`, as JSON or as the bare
    state its `--format` asks for; `FAIL`, or running out, is a failed call.
    """
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    gcloud = bin_dir / "gcloud"
    gcloud.write_text(
        "#!/bin/sh\n"
        'printf "%s\\n" "$*" >> "$GCLOUD_ARGS_FILE"\n'
        '[ "$3" = describe ] || exit 0\n'
        'state="$(head -n 1 "$GCLOUD_STATES")"\n'
        'tail -n +2 "$GCLOUD_STATES" > "$GCLOUD_STATES.next"\n'
        'mv "$GCLOUD_STATES.next" "$GCLOUD_STATES"\n'
        'if [ -z "$state" ] || [ "$state" = FAIL ]; then\n'
        '  echo "ERROR: (gcloud.batch.jobs.describe) HTTP 503" >&2\n'
        "  exit 1\n"
        "fi\n"
        'case "$*" in\n'
        '  *--format=json*) printf \'{"uid": "job-uid-1", "status": {"state": "%s"}}\\n\' "$state" ;;\n'
        '  *) printf "%s\\n" "$state" ;;\n'
        "esac\n"
    )
    sleep = bin_dir / "sleep"
    sleep.write_text('#!/bin/sh\nprintf "%s\\n" "$1" >> "$SLEEPS_FILE"\n')
    for stub in (gcloud, sleep):
        stub.chmod(0o755)
    states_path = tmp_path / "states"
    states_path.write_text("".join(f"{state}\n" for state in states))
    paths = {
        name: tmp_path / name
        for name in ("github-output", "github-summary", "gcloud-args", "sleeps")
    }
    for path in paths.values():
        path.write_text("")

    result = subprocess.run(
        ["bash", "-e", "-o", "pipefail", "-c", run],
        env={
            **os.environ,
            "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
            "JOB_ID": "gh-123-1",
            "GCLOUD_STATES": str(states_path),
            "GCLOUD_ARGS_FILE": str(paths["gcloud-args"]),
            "SLEEPS_FILE": str(paths["sleeps"]),
            "GITHUB_OUTPUT": str(paths["github-output"]),
            "GITHUB_STEP_SUMMARY": str(paths["github-summary"]),
            **env,
        },
        capture_output=True,
        text=True,
        check=False,
    )
    return _BatchStepRun(
        result.returncode,
        paths["github-output"].read_text().splitlines(),
        paths["github-summary"].read_text(),
        paths["gcloud-args"].read_text().splitlines(),
        paths["sleeps"].read_text().splitlines(),
    )


def _run_wait(tmp_path: Path, states: list[str]) -> _BatchStepRun:
    wait = next(step for step in _eu_job()["steps"] if step.get("id") == "wait-batch")
    return _run_batch_step(wait["run"], tmp_path, states)


def _run_cleanup(
    tmp_path: Path,
    states: list[str],
    *,
    cancelled: bool,
    submit_outcome: str = "success",
):
    return _run_batch_step(
        _cleanup_step()["run"],
        tmp_path,
        states,
        CANCELLED=str(cancelled).lower(),
        SUBMIT_OUTCOME=submit_outcome,
    )


def _cleanup_runs(
    *, cancelled: bool, wait_outcome: str, submit_outcome: str = "success"
) -> bool:
    """The cleanup step's `if`, which `CLEANUP_IF` pins, for one run."""
    return cancelled or submit_outcome == "failure" or wait_outcome == "failure"


def _run_spec() -> dict:
    return build_batch_job(
        job_id="gh-123-1",
        source_archive_uri="gs://bucket/source.tar.gz",
        run_prefix_uri="gs://bucket/gh/123-1",
        cli_args=["--command", "spec"],
        github_run_id="RUN #ABC",
        connector="Source_PokeAPI",
        max_run_duration_seconds=max_run_duration_seconds(360, elapsed_seconds=120),
    )


def _valid_finalize_verdict(*, success: bool = True, incomplete: bool = False) -> dict:
    return {
        "schema_version": 2,
        "output_mode": "masked",
        "commands": [],
        "success": success,
        "regression_detected": False,
        "both_failed": False,
        "incomplete": incomplete,
        "not_exercised": False,
        "totals": {
            "stream_count": 0,
            "control_record_count": 0,
            "target_record_count": 0,
        },
        "checks": [],
    }


def _verdict_from_a_regression_the_summary_passed(tmp_path: Path) -> dict:
    """The verdict of a run whose spec comparison failed while every command
    exited 0, built the way the VM builds it."""
    output_dir = tmp_path / "out"
    (output_dir / "spec").mkdir(parents=True)
    (output_dir / "spec" / "regression_report.json").write_text(
        json.dumps(
            {
                "output_mode": "masked",
                "target": {"exit_code": 0},
                "control": {"exit_code": 0},
                "success": False,
                "regression_detected": True,
                "both_failed": False,
                "incomplete": False,
                "comparison": {"spec": {"passed": False}},
            }
        )
    )
    (output_dir / "summary.json").write_text(
        json.dumps(
            {
                "exit_code": 0,
                "success": True,
                "both_failed": False,
                "incomplete": False,
                "commands": [{"command": "spec", "exit_code": 0, "passed": True}],
            }
        )
    )
    return build_verdict(output_dir)


def test_s11_batch_environment_excludes_credential_like_keys() -> None:
    with pytest.raises(ValueError, match="GCP_PROD_DB_ACCESS_CREDENTIALS"):
        validate_environment({"GCP_PROD_DB_ACCESS_CREDENTIALS": "x"})


def test_s11_batch_job_uses_eu_network_identity_and_masking_telemetry() -> None:
    job = _run_spec()
    task = job["taskGroups"][0]["taskSpec"]
    variables = task["environment"]["variables"]
    allocation = job["allocationPolicy"]
    network = allocation["network"]["networkInterfaces"][0]

    assert allocation["location"]["allowedLocations"] == ["regions/europe-west9"]
    assert network["network"].endswith("/networks/connector-regression-eu")
    assert network["subnetwork"].endswith("/subnetworks/connector-regression-eu")
    assert network["noExternalIpAddress"] is True
    assert allocation["serviceAccount"]["email"].startswith(
        "connector-regression-eu-job@"
    )
    assert job["logsPolicy"]["destination"] == "CLOUD_LOGGING"
    assert variables == {
        "DO_NOT_TRACK": "1",
        "SOURCE_ARCHIVE_URI": "gs://bucket/source.tar.gz",
        "RUN_PREFIX_URI": "gs://bucket/gh/123-1",
        "CLI_ARGS_JSON": json.dumps(["--command", "spec"]),
        "SEED_STATE_STAGED": "false",
        "TARGET_IMAGE": "",
    }
    assert job["labels"] == {
        "github_run_id": "run_abc",
        "connector": "source_pokeapi",
    }
    assert task["maxRunDuration"] == "20880s"


def test_a_staged_seed_reaches_the_vm_as_a_flag_only() -> None:
    """The flag says a seed is there to download; the seed stays in the
    bucket, out of the job's metadata."""
    job = build_batch_job(
        job_id="gh-123-1",
        source_archive_uri="gs://bucket/source.tar.gz",
        run_prefix_uri="gs://bucket/gh/123-1",
        cli_args=["--command", "read"],
        github_run_id="123",
        connector="source-pokeapi",
        max_run_duration_seconds=3600,
        seed_state_staged=True,
    )
    variables = job["taskGroups"][0]["taskSpec"]["environment"]["variables"]

    assert variables["SEED_STATE_STAGED"] == "true"
    validate_environment(variables)


def test_the_staged_target_image_reaches_the_vm_by_name() -> None:
    """The VM downloads `target-image.tar` from the run prefix and loads it
    only when told which image it must hold."""
    job = build_batch_job(
        job_id="gh-123-1",
        source_archive_uri="gs://bucket/source.tar.gz",
        run_prefix_uri="gs://bucket/gh/123-1",
        cli_args=["--test-image", "airbyte/source-pokeapi:dev"],
        github_run_id="123",
        connector="source-pokeapi",
        max_run_duration_seconds=3600,
        target_image="airbyte/source-pokeapi:dev",
    )
    variables = job["taskGroups"][0]["taskSpec"]["environment"]["variables"]

    assert variables["TARGET_IMAGE"] == "airbyte/source-pokeapi:dev"
    validate_environment(variables)


def test_s13_workflow_outputs_and_cleanup_are_defined() -> None:
    workflow = _workflow()
    job = _eu_job()
    outputs = workflow[True]["workflow_call"]["outputs"]
    for name in outputs:
        assert f"steps.finalize.outputs.{name}" in job["outputs"][name]
    # The job is deleted only on a cancelled run or a wait that stopped for
    # good, and the summary says which.
    cleanup = _cleanup_step()
    assert cleanup["if"] == CLEANUP_IF
    assert cleanup["env"]["CANCELLED"] == "${{ job.status == 'cancelled' }}"
    assert "the run was cancelled" in cleanup["run"]
    assert "the wait for it stopped" in cleanup["run"]
    assert '>> "$GITHUB_STEP_SUMMARY"' in cleanup["run"]
    finalize = next(step for step in job["steps"] if step.get("id") == "finalize")
    assert "CANCELLED" in finalize.get("env", {})
    assert finalize["env"]["BATCH_STATE"] == "${{ steps.wait-batch.outputs.state }}"
    assert "success=false" in finalize["run"]
    assert "internal_failure=true" in finalize["run"]
    assert "validate_verdict" in finalize["run"]
    assert finalize["env"]["RUN_PREFIX"] == "${{ steps.paths.outputs.prefix }}"
    assert "RUN_PREFIX" in finalize["run"]


def test_finalize_invalid_verdict_emits_internal_failure_and_prefix_urls(
    tmp_path: Path,
) -> None:
    finalize = next(step for step in _eu_job()["steps"] if step.get("id") == "finalize")
    verdict = tmp_path / "verdict.json"
    verdict.write_text('{"success": "private customer data"}')
    output = tmp_path / "output"
    summary = tmp_path / "summary"
    env = {
        **os.environ,
        "CANCELLED": "false",
        "BATCH_STATE": "SUCCEEDED",
        "RUN_PREFIX": "gs://internal-airbyte-ai-infra-connector-regression-eu/gh/123-1",
        "VERDICT_PATH": str(verdict),
        "GITHUB_OUTPUT": str(output),
        "GITHUB_STEP_SUMMARY": str(summary),
    }

    result = subprocess.run(
        ["bash", "-e", "-o", "pipefail", "-c", finalize["run"]],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    lines = output.read_text().splitlines()
    for key, value in (
        ("success", "false"),
        ("internal_failure", "true"),
        ("both_failed", "false"),
        ("incomplete", "false"),
        ("not_exercised", "false"),
    ):
        assert lines.count(f"{key}={value}") == 1
        assert sum(line.startswith(f"{key}=") for line in lines) == 1
    assert sum(line.startswith("summary_url=") for line in lines) == 1
    assert sum(line.startswith("report_url=") for line in lines) == 1
    assert all(
        "/gh/123-1/" in line
        for line in lines
        if line.startswith(("summary_url=", "report_url="))
    )
    assert "EU outputs were kept for 2 days for debugging" in summary.read_text()
    assert "private customer data" not in result.stdout
    assert "private customer data" not in result.stderr


@pytest.mark.parametrize(
    "scenario",
    [
        "pass",
        "failed",
        "regression-the-summary-passed",
        "incomplete",
        "not-exercised",
        "internal-failure",
        "cancelled",
        "delete-failure",
        "empty-prefix",
        "bucket-prefix",
        "batch-failed",
        "batch-state-missing",
    ],
)
def test_finalize_deletes_run_prefix_only_after_a_clean_pass(
    tmp_path: Path, scenario: str
) -> None:
    finalize = next(step for step in _eu_job()["steps"] if step.get("id") == "finalize")
    run_prefix = "gs://internal-airbyte-ai-infra-connector-regression-eu/gh/123-1"
    verdict = _valid_finalize_verdict()
    cancelled = "false"
    batch_state = "SUCCEEDED"
    gcloud_exit_code = "0"
    expected_exit_code = 0
    should_delete = scenario in {"pass", "delete-failure"}

    if scenario == "failed":
        verdict["success"] = False
        expected_exit_code = 1
    elif scenario == "regression-the-summary-passed":
        verdict = _verdict_from_a_regression_the_summary_passed(tmp_path)
        expected_exit_code = 1
    elif scenario == "incomplete":
        verdict["success"] = False
        verdict["incomplete"] = True
        expected_exit_code = 1
    elif scenario == "not-exercised":
        verdict["success"] = False
        verdict["not_exercised"] = True
        expected_exit_code = 1
    elif scenario == "internal-failure":
        verdict = {"success": "invalid"}
        expected_exit_code = 1
    elif scenario == "cancelled":
        cancelled = "true"
        expected_exit_code = 1
    elif scenario == "delete-failure":
        gcloud_exit_code = "1"
    elif scenario == "empty-prefix":
        run_prefix = ""
        expected_exit_code = 1
        should_delete = False
    elif scenario == "bucket-prefix":
        run_prefix = "gs://internal-airbyte-ai-infra-connector-regression-eu/gh/"
        should_delete = False
    elif scenario == "batch-failed":
        # The verdict upload went through and a later upload failed the job.
        batch_state = "FAILED"
        expected_exit_code = 1
        should_delete = False
    elif scenario == "batch-state-missing":
        batch_state = ""
        expected_exit_code = 1
        should_delete = False

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    gcloud = bin_dir / "gcloud"
    gcloud.write_text(
        "#!/usr/bin/env bash\n"
        'printf "%s\\n" "$*" >> "$GCLOUD_ARGS_FILE"\n'
        'exit "${GCLOUD_EXIT_CODE:-0}"\n'
    )
    gcloud.chmod(0o755)

    verdict_path = tmp_path / "verdict.json"
    verdict_path.write_text(json.dumps(verdict))
    output_path = tmp_path / "github-output"
    summary_path = tmp_path / "github-summary"
    gcloud_args_path = tmp_path / "gcloud-args"
    env = {
        **os.environ,
        "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
        "CANCELLED": cancelled,
        "BATCH_STATE": batch_state,
        "RUN_PREFIX": run_prefix,
        "VERDICT_PATH": str(verdict_path),
        "GITHUB_OUTPUT": str(output_path),
        "GITHUB_STEP_SUMMARY": str(summary_path),
        "GCLOUD_ARGS_FILE": str(gcloud_args_path),
        "GCLOUD_EXIT_CODE": gcloud_exit_code,
    }

    result = subprocess.run(
        ["bash", "-e", "-o", "pipefail", "-c", finalize["run"]],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == expected_exit_code, result.stderr
    assert (
        f"not_exercised={str(verdict.get('not_exercised', False)).lower()}"
        in output_path.read_text()
    )
    calls = (
        gcloud_args_path.read_text().splitlines() if gcloud_args_path.exists() else []
    )
    if should_delete:
        assert calls == [f"storage rm --recursive {run_prefix}/"]
    else:
        assert calls == []

    summary = summary_path.read_text() if summary_path.exists() else ""
    if scenario == "pass":
        assert "EU outputs deleted on pass" in summary
        assert run_prefix in summary
        assert "report and summary links above no longer resolve" in summary
        assert "Batch logs are kept (2-day log retention)" in summary
    elif scenario in {"delete-failure", "bucket-prefix"}:
        assert "::warning::" in result.stdout
        assert "EU output deletion failed" in summary
        assert "2-day bucket lifecycle will remove them" in summary
    elif scenario != "empty-prefix":
        assert "EU outputs were kept for 2 days for debugging" in summary
    if scenario in {"batch-failed", "batch-state-missing"}:
        outputs = output_path.read_text().splitlines()
        assert "success=false" in outputs
        assert "internal_failure=true" in outputs
        assert "Workflow failed due to internal infrastructure error(s)" in (
            result.stdout
        )
        ended = "FAILED" if scenario == "batch-failed" else "in an unknown state"
        assert f"**EU Batch job ended {ended}:**" in summary


def test_finalize_fails_after_writing_outputs() -> None:
    finalize = next(step for step in _eu_job()["steps"] if step.get("id") == "finalize")
    run = finalize["run"]
    output_write = run.index('} | tee -a "$GITHUB_OUTPUT"')
    internal_check = run.index('if [ "$internal_failure" = "true" ]; then')
    internal_error = run.index(
        "::error::Workflow failed due to internal infrastructure error(s)"
    )
    internal_exit = run.index("exit 1", internal_check)
    verdict_check = run.index('if [ "$success" != "true" ]; then')
    verdict_error = run.index(
        "::error::Regression test failed - see the run summary for the per-command verdict"
    )
    verdict_exit = run.index("exit 1", verdict_check)

    assert (
        output_write
        < internal_check
        < internal_error
        < internal_exit
        < verdict_check
        < verdict_error
        < verdict_exit
    )


def test_eu_workflow_does_not_download_summary_json() -> None:
    assert not any(
        "gcloud storage cp" in step.get("run", "") and "summary.json" in step["run"]
        for step in _eu_job()["steps"]
    )


def test_summary_logs_link_opens_the_batch_job_query(tmp_path: Path) -> None:
    """A run script is plain bash, where `%%` stays two characters; only a
    printf format halves it."""
    render = next(
        step
        for step in _eu_job()["steps"]
        if step.get("name") == "Render EU run summary"
    )
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    uv_args = tmp_path / "uv-args"
    uv = bin_dir / "uv"
    uv.write_text('#!/bin/sh\nprintf "%s\\n" "$@" > "$UV_ARGS_FILE"\n')
    uv.chmod(0o755)
    env = {
        **os.environ,
        "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
        "JOB_ID": "gh-123-1",
        "JOB_UID": "gh-123-1-0a1b2c3d-4e5f",
        "RUN_PREFIX": "gs://internal-airbyte-ai-infra-connector-regression-eu/gh/123-1",
        "RUNNER_TEMP": str(tmp_path),
        "GITHUB_STEP_SUMMARY": str(tmp_path / "summary"),
        "UV_ARGS_FILE": str(uv_args),
    }

    subprocess.run(
        ["bash", "-e", "-o", "pipefail", "-c", render["run"]],
        env=env,
        check=True,
    )

    args = uv_args.read_text().splitlines()
    url = urlsplit(args[args.index("--logs-url") + 1])
    page, *parameters = url.path.split(";")
    fields = dict(parameter.split("=", 1) for parameter in parameters)
    assert "%%" not in url.geturl()
    assert page == "/logs/query"
    assert unquote(fields["query"]) == 'labels.job_uid="gh-123-1-0a1b2c3d-4e5f"'
    assert unquote(fields["storageScope"]) == (
        "storage,projects/internal-airbyte-ai-infra/locations/europe-west9"
        "/buckets/connector-regression-eu/views/_AllLogs"
    )
    assert url.query == "project=internal-airbyte-ai-infra"


def test_batch_poll_describes_once_and_exits_for_terminal_states() -> None:
    wait = next(step for step in _eu_job()["steps"] if step.get("id") == "wait-batch")
    assert wait["run"].count("gcloud batch jobs describe") == 1
    assert "--format=json" in wait["run"]
    assert "DELETION_IN_PROGRESS" in wait["run"]
    assert "CANCELLED" in wait["run"]


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_one_failed_describe_neither_ends_the_wait_nor_deletes_the_job(
    tmp_path: Path,
) -> None:
    """An auth refresh, a 5xx or a network blip between two good polls."""
    wait = _run_wait(tmp_path, ["RUNNING", "FAIL", "RUNNING", "SUCCEEDED"])

    assert wait.returncode == 0
    assert "state=SUCCEEDED" in wait.outputs
    assert "job_uid=job-uid-1" in wait.outputs
    assert [call.split()[2] for call in wait.gcloud_calls] == ["describe"] * 4
    assert wait.sleeps == ["30", "30", "30"]
    assert not _cleanup_runs(cancelled=False, wait_outcome="success")


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_the_wait_backs_off_and_stops_after_five_failed_describes_in_a_row(
    tmp_path: Path,
) -> None:
    wait = _run_wait(tmp_path, ["RUNNING", "FAIL", "RUNNING", *["FAIL"] * 5])

    assert wait.returncode == 1
    assert not any(line.startswith("state=") for line in wait.outputs)
    assert wait.sleeps == ["30", "30", "30", "30", "60", "120", "240"]
    assert _cleanup_runs(cancelled=False, wait_outcome="failure")


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
@pytest.mark.parametrize("cancelled", [True, False], ids=["cancelled", "wait-stopped"])
def test_cleanup_deletes_a_running_job_and_says_why(
    tmp_path: Path, cancelled: bool
) -> None:
    cleanup = _run_cleanup(tmp_path, ["RUNNING"], cancelled=cancelled)

    assert cleanup.returncode == 0
    assert cleanup.gcloud_calls[1:] == [
        (
            "batch jobs delete gh-123-1 --project internal-airbyte-ai-infra "
            + "--location europe-west9 --quiet"
        )
    ]
    reason = (
        "the run was cancelled"
        if cancelled
        else "the wait for it stopped (see the wait step's log)"
    )
    assert cleanup.summary == f"**EU Batch job deleted while RUNNING:** {reason}.\n"


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_cleanup_deletes_a_job_whose_submit_step_failed(tmp_path: Path) -> None:
    """A submit that errors after Batch accepted the job, so the wait is skipped."""
    assert _cleanup_runs(
        cancelled=False, submit_outcome="failure", wait_outcome="skipped"
    )
    cleanup = _run_cleanup(
        tmp_path, ["QUEUED"], cancelled=False, submit_outcome="failure"
    )

    assert cleanup.returncode == 0
    assert cleanup.gcloud_calls[1:] == [
        (
            "batch jobs delete gh-123-1 --project internal-airbyte-ai-infra "
            + "--location europe-west9 --quiet"
        )
    ]
    assert cleanup.summary == (
        "**EU Batch job deleted while QUEUED:** its submit step failed, so "
        "nothing waited for it.\n"
    )


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
@pytest.mark.parametrize(
    ("states", "summary"),
    [
        (
            ["SUCCEEDED"],
            (
                "**EU Batch job kept:** the run was cancelled, but the job had "
                + "already ended (SUCCEEDED).\n"
            ),
        ),
        (
            ["FAIL"],
            (
                "**EU Batch job not deleted:** the run was cancelled, and its state "
                + "could not be read.\n"
            ),
        ),
    ],
    ids=["already-ended", "state-unknown"],
)
def test_cleanup_keeps_a_job_it_cannot_see_running(
    tmp_path: Path, states: list[str], summary: str
) -> None:
    cleanup = _run_cleanup(tmp_path, states, cancelled=True)

    assert cleanup.returncode == 0
    assert not any("delete" in call for call in cleanup.gcloud_calls)
    assert cleanup.summary == summary


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_vm_runner_without_connection_runs_spec_only() -> None:
    assert _selected_vm_commands(has_connection_id=False, skip_read=False) == ["spec"]


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_vm_runner_with_connection_runs_check_discover_and_read() -> None:
    assert _selected_vm_commands(has_connection_id=True, skip_read=False) == [
        "spec",
        "check",
        "discover",
        "read",
    ]


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_vm_runner_with_connection_can_skip_read() -> None:
    assert _selected_vm_commands(has_connection_id=True, skip_read=True) == [
        "spec",
        "check",
        "discover",
    ]


def test_vm_summary_folds_not_exercised_from_command_outputs(tmp_path: Path) -> None:
    text = VM_SCRIPT.read_text()
    start = text.index('python3 - "$OUT" "$rc" "$WORK" <<\'PY\'')
    program_start = text.index("\n", start) + 1
    program_end = text.index("\nPY\n", program_start)
    work_dir = tmp_path / "work"
    output_dir = tmp_path / "out"
    work_dir.mkdir()
    output_dir.mkdir()
    (work_dir / "read.exit-code").write_text("0")
    (work_dir / "read.github-output").write_text("not_exercised=true\n")

    subprocess.run(
        [sys.executable, "-", str(output_dir), "0", str(work_dir)],
        input=text[program_start:program_end],
        text=True,
        check=True,
    )

    summary = json.loads((output_dir / "summary.json").read_text())
    assert summary["not_exercised"] is True
    assert set(summary) == {
        "exit_code",
        "success",
        "both_failed",
        "incomplete",
        "not_exercised",
        "commands",
    }


# `gcs_get` is stubbed as `curl -sf` behaves: on an HTTP error it writes nothing
# and exits 22, a 403, a 404, a 5xx and a failed token call (a 401) alike. The
# real one reads `split_gs_uri` with `mapfile`, which macOS's bash 3.2 lacks.
_VM_SEED_STUBS = """
gcs_get() {
  printf '%s %s\\n' "$1" "$2" >> "$GCS_CALLS"
  local status
  status="$(head -n 1 "$GCS_STATUSES")"
  tail -n +2 "$GCS_STATUSES" > "$GCS_STATUSES.next"
  mv "$GCS_STATUSES.next" "$GCS_STATUSES"
  [[ "$status" == 200 ]] || return 22
  printf '%s' '[{"type": "STREAM"}]' > "$2"
}
sleep() { printf '%s\\n' "$1" >> "$SLEEPS"; }
"""


class _VmSeedRun(NamedTuple):
    returncode: int
    stderr: str
    state_args: list[str] | None
    gcs_calls: list[str]
    sleeps: list[str]
    uv_calls: list[list[str]]


def _run_vm_seed(
    tmp_path: Path, *, staged: str | None, statuses: list[int]
) -> _VmSeedRun:
    """Run the VM's seed download, then its command loop, with the network
    and the CLI stubbed."""
    text = VM_SCRIPT.read_text()
    seed_start = text.index("STATE_ARGS=()\n")
    seed_end = text.index("\nselect_commands() {", seed_start)
    loop_start = text.index('rc=0\nlast_command=""\n')
    loop_end = text.index("\ndone\n", loop_start) + len("\ndone\n")
    work = tmp_path / "work"
    (work / "out").mkdir(parents=True)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    uv = bin_dir / "uv"
    uv.write_text('#!/bin/sh\nprintf \'%s\\n\' --- "$@" >> "$UV_ARGS_FILE"\n')
    uv.chmod(0o755)
    files = {
        name: tmp_path / name
        for name in ("gcs-calls", "gcs-statuses", "sleeps", "state-args", "uv-args")
    }
    for path in files.values():
        path.write_text("")
    files["gcs-statuses"].write_text("".join(f"{status}\n" for status in statuses))
    env = {
        **os.environ,
        "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
        "WORK": str(work),
        "RUN_PREFIX_URI": "gs://bucket/gh/123-1",
        "GCS_CALLS": str(files["gcs-calls"]),
        "GCS_STATUSES": str(files["gcs-statuses"]),
        "SLEEPS": str(files["sleeps"]),
        "STATE_ARGS_FILE": str(files["state-args"]),
        "UV_ARGS_FILE": str(files["uv-args"]),
    }
    env.pop("SEED_STATE_STAGED", None)
    if staged is not None:
        env["SEED_STATE_STAGED"] = staged

    run = subprocess.run(
        [
            "bash",
            "-c",
            "\n".join(
                [
                    "set -euo pipefail",
                    _VM_SEED_STUBS,
                    text[seed_start:seed_end],
                    'printf "%s\\n" reached ${STATE_ARGS[@]+"${STATE_ARGS[@]}"} > "$STATE_ARGS_FILE"',
                    # The loop expands STATE_ARGS under `set -u`, which bash 3.2
                    # refuses for an empty array, so it runs only for a seed.
                    "[[ ${#STATE_ARGS[@]} -gt 0 ]] || exit 0",
                    'OUT="$WORK/out"',
                    'MASK_KEY_PATH="$WORK/mask_key"',
                    "COMMANDS=(spec check discover read)",
                    "CLI_ARGS=(--connector-name source-example --connection-id c-1)",
                    "HAS_CONNECTION_ID=true",
                    "HAS_CATALOG_PATH=false",
                    text[loop_start:loop_end],
                ]
            ),
        ],
        env=env,
        capture_output=True,
        text=True,
    )
    reached = files["state-args"].read_text().splitlines()
    return _VmSeedRun(
        run.returncode,
        run.stderr,
        reached[1:] if reached[:1] == ["reached"] else None,
        files["gcs-calls"].read_text().splitlines(),
        files["sleeps"].read_text().splitlines(),
        [call.splitlines() for call in files["uv-args"].read_text().split("---\n")[1:]],
    )


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
@pytest.mark.parametrize("status", [403, 404, 500])
def test_a_requested_seed_that_does_not_download_stops_the_vm(
    tmp_path: Path, status: int
) -> None:
    """A read without the seed starts from another state and could still
    pass. The VM stops before any command; the job then fails, which the
    workflow's Finalize reports as an internal failure."""
    run = _run_vm_seed(tmp_path, staged="true", statuses=[status] * 3)

    assert run.returncode == 1
    assert "requested seed state could not be downloaded" in run.stderr
    assert run.state_args is None
    assert run.uv_calls == []
    assert len(run.gcs_calls) == 3
    assert run.sleeps == ["10", "20"]


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_a_requested_seed_reaches_read_as_state_path_after_a_transient_error(
    tmp_path: Path,
) -> None:
    run = _run_vm_seed(tmp_path, staged="true", statuses=[500, 200])
    state_path = str(tmp_path / "work" / "state.json")

    assert run.returncode == 0, run.stderr
    assert run.gcs_calls == [f"gs://bucket/gh/123-1/state.json {state_path}"] * 2
    assert run.state_args == ["--state-path", state_path]
    commands = {call[call.index("--command") + 1]: call for call in run.uv_calls}
    assert list(commands) == ["spec", "check", "discover", "read"]
    read = commands.pop("read")
    assert read[read.index("--state-path") + 1] == state_path
    assert all("--state-path" not in call for call in commands.values())


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
@pytest.mark.parametrize("staged", ["false", None], ids=["false", "unset"])
def test_without_a_seed_the_vm_downloads_none_and_passes_no_state_path(
    tmp_path: Path, staged: str | None
) -> None:
    run = _run_vm_seed(tmp_path, staged=staged, statuses=[404])

    assert run.returncode == 0, run.stderr
    assert run.gcs_calls == []
    assert run.state_args == []


TARGET_IMAGE = "airbyte/source-pokeapi:dev"
CONTROL_IMAGE = "airbyte/source-pokeapi:0.3.0"


def _vm_function(text: str, name: str) -> str:
    start = text.index(f"{name}() {{")
    return text[start : text.index("\n}\n", start) + 3]


def _docker_stub(bin_dir: Path) -> None:
    """A `docker` that records its arguments and answers `load` with
    $DOCKER_LOAD_OUTPUT; every other call succeeds."""
    bin_dir.mkdir(exist_ok=True)
    docker = bin_dir / "docker"
    docker.write_text(
        "#!/bin/sh\n"
        'printf "%s\\n" "$*" >> "$DOCKER_CALLS"\n'
        '[ "$1" = load ] && printf "%s\\n" "$DOCKER_LOAD_OUTPUT"\n'
        "exit 0\n"
    )
    docker.chmod(0o755)


class _VmLoadRun(NamedTuple):
    returncode: int
    stderr: str
    reached: bool
    gcs_calls: list[str]
    docker_calls: list[str]


def _run_vm_load(
    tmp_path: Path, *, target_image: str, docker_load_output: str = ""
) -> _VmLoadRun:
    """Run the VM's image load as the script has it, with `gcs_get` and
    `docker` stubbed; `reached` says whether the script went on past it."""
    text = VM_SCRIPT.read_text()
    call = 'if [[ -n "${TARGET_IMAGE:-}" ]]; then\n  load_target_image\nfi\n'
    assert text.count(call) == 1
    work = tmp_path / "work"
    work.mkdir()
    bin_dir = tmp_path / "bin"
    _docker_stub(bin_dir)
    files = {name: tmp_path / name for name in ("gcs-calls", "docker-calls")}
    for path in files.values():
        path.write_text("")
    reached = tmp_path / "reached"
    run = subprocess.run(
        [
            "bash",
            "-c",
            "\n".join(
                [
                    "set -euo pipefail",
                    'gcs_get() { printf "%s %s\\n" "$1" "$2" >> "$GCS_CALLS"; : > "$2"; }',
                    _vm_function(text, "load_target_image"),
                    call,
                    'printf reached > "$REACHED"',
                ]
            ),
        ],
        env={
            **os.environ,
            "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
            "WORK": str(work),
            "RUN_PREFIX_URI": "gs://bucket/gh/123-1",
            "TARGET_IMAGE": target_image,
            "DOCKER_LOAD_OUTPUT": docker_load_output,
            "GCS_CALLS": str(files["gcs-calls"]),
            "DOCKER_CALLS": str(files["docker-calls"]),
            "REACHED": str(reached),
        },
        capture_output=True,
        text=True,
    )
    return _VmLoadRun(
        run.returncode,
        run.stderr,
        reached.exists(),
        files["gcs-calls"].read_text().splitlines(),
        files["docker-calls"].read_text().splitlines(),
    )


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_the_vm_loads_the_staged_image(tmp_path: Path) -> None:
    run = _run_vm_load(
        tmp_path,
        target_image=TARGET_IMAGE,
        docker_load_output=f"Loaded image: {TARGET_IMAGE}",
    )
    archive = tmp_path / "work" / "target-image.tar"

    assert run.returncode == 0, run.stderr
    assert run.reached
    assert run.gcs_calls == [f"gs://bucket/gh/123-1/target-image.tar {archive}"]
    assert run.docker_calls == [f"load --input {archive}"]
    assert not archive.exists()


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
@pytest.mark.parametrize(
    "docker_load_output",
    [
        pytest.param(
            f"Loaded image: {TARGET_IMAGE}\nLoaded image: {CONTROL_IMAGE}",
            id="a-second-tag-could-replace-the-control",
        ),
        pytest.param("Loaded image: airbyte/source-other:dev", id="another-image"),
        pytest.param("Loaded image ID: sha256:abc", id="untagged"),
        pytest.param("", id="nothing"),
    ],
)
def test_the_vm_stops_before_any_command_on_an_archive_that_loads_anything_else(
    tmp_path: Path, docker_load_output: str
) -> None:
    """The archive is the PR's to write. The job's failure is the run's
    internal failure, which Finalize reports."""
    run = _run_vm_load(
        tmp_path, target_image=TARGET_IMAGE, docker_load_output=docker_load_output
    )

    assert run.returncode == 1
    assert f"did not load exactly {TARGET_IMAGE}" in run.stderr
    assert not run.reached


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_a_run_that_names_its_own_image_loads_nothing(tmp_path: Path) -> None:
    run = _run_vm_load(tmp_path, target_image="")

    assert run.returncode == 0, run.stderr
    assert run.reached
    assert run.gcs_calls == []
    assert run.docker_calls == []


class _VmPullRun(NamedTuple):
    returncode: int
    stderr: str
    reached: bool
    docker_calls: list[str]


def _run_vm_pulls(
    tmp_path: Path, cli_args: list[str], *, target_image: str
) -> _VmPullRun:
    """Run the VM's `--test-image` guard and image pulls with `docker` stubbed."""
    text = VM_SCRIPT.read_text()
    start = text.index('if [[ " ${CLI_ARGS[*]} " != *" --test-image "* ]]; then')
    end = text.index("\n  done\ndone\n", start) + len("\n  done\ndone\n")
    bin_dir = tmp_path / "bin"
    _docker_stub(bin_dir)
    docker_calls = tmp_path / "docker-calls"
    docker_calls.write_text("")
    reached = tmp_path / "reached"
    run = subprocess.run(
        [
            "bash",
            "-c",
            "\n".join(
                [
                    "set -euo pipefail",
                    _vm_function(text, "pull_image"),
                    "CLI_ARGS=(" + " ".join(f"'{arg}'" for arg in cli_args) + ")",
                    text[start:end],
                    'printf reached > "$REACHED"',
                ]
            ),
        ],
        env={
            **os.environ,
            "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
            "TARGET_IMAGE": target_image,
            "DOCKER_CALLS": str(docker_calls),
            "REACHED": str(reached),
        },
        capture_output=True,
        text=True,
    )
    return _VmPullRun(
        run.returncode,
        run.stderr,
        reached.exists(),
        docker_calls.read_text().splitlines(),
    )


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
@pytest.mark.parametrize(
    ("control_image", "pulls"),
    [
        pytest.param(
            CONTROL_IMAGE,
            [
                f"pull -q mirror.gcr.io/{CONTROL_IMAGE}",
                f"tag mirror.gcr.io/{CONTROL_IMAGE} {CONTROL_IMAGE}",
            ],
            id="the-control-only",
        ),
        pytest.param(TARGET_IMAGE, [], id="never-over-the-loaded-image"),
    ],
)
def test_the_vm_never_pulls_over_the_loaded_test_image(
    tmp_path: Path, control_image: str, pulls: list[str]
) -> None:
    run = _run_vm_pulls(
        tmp_path,
        [
            "--connector-name",
            "source-pokeapi",
            "--test-image",
            TARGET_IMAGE,
            "--control-image",
            control_image,
        ],
        target_image=TARGET_IMAGE,
    )

    assert run.returncode == 0, run.stderr
    assert run.reached
    assert run.docker_calls == pulls


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_a_skip_compare_override_image_is_pulled_as_before(tmp_path: Path) -> None:
    run = _run_vm_pulls(
        tmp_path,
        [
            "--connector-name",
            "source-pokeapi",
            "--skip-compare",
            "--test-image",
            CONTROL_IMAGE,
        ],
        target_image="",
    )

    assert run.returncode == 0, run.stderr
    assert run.docker_calls == [
        f"pull -q mirror.gcr.io/{CONTROL_IMAGE}",
        f"tag mirror.gcr.io/{CONTROL_IMAGE} {CONTROL_IMAGE}",
    ]


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_the_vm_stops_rather_than_let_the_cli_build(tmp_path: Path) -> None:
    """The CLI builds from source when it has no `--test-image`."""
    run = _run_vm_pulls(
        tmp_path, ["--connector-name", "source-pokeapi"], target_image=""
    )

    assert run.returncode == 1
    assert "the VM does not build the connector" in run.stderr
    assert not run.reached
    assert run.docker_calls == []


def test_the_vm_never_builds_or_fetches_the_pr_source() -> None:
    """The image comes built and checked; it is loaded after Docker starts,
    and the guard, the pulls and the load all come before the first command."""
    text = VM_SCRIPT.read_text()

    for absent in ("connector-source", "connector-repo", "--repo-root", "gradle"):
        assert absent not in text, absent
    assert (
        text.index("systemctl start docker")
        < text.index("\n  load_target_image\nfi\n")
        < text.index('!= *" --test-image "*')
        < text.index('pull_image "$image"')
        < text.index("uv run airbyte-ops cloud connector regression-test")
    )


METADATA_URL = "http://169.254.169.254/computeMetadata/v1/"
CONTAINER_RULE = "-I DOCKER-USER -d 169.254.169.254 -p tcp ! --dport 53 -j REJECT"
PROXY_USER_RULE = (
    "-I OUTPUT -d 169.254.169.254 -p tcp ! --dport 53 "
    "-m owner --uid-owner regression-proxy -j REJECT"
)

# Every command the block and its self-test run, each logging its name and
# arguments to one file so their order shows. `runuser` runs what follows
# `--`; the others answer with an exit code from the environment.
_METADATA_BLOCK_STUBS = {
    "iptables": 'log iptables "$@"\nexit "${IPTABLES_RC:-0}"\n',
    "id": 'log id "$@"\nexit "${ID_RC:-1}"\n',
    "useradd": 'log useradd "$@"\n',
    "apt-get": 'log apt-get "$@"\n',
    "docker": (
        'log docker "$@"\n'
        'case "$*" in\n'
        '  *" wget "*) exit "${WGET_RC:-1}" ;;\n'
        '  *" nslookup "*) exit "${NSLOOKUP_RC:-0}" ;;\n'
        "esac\n"
    ),
    "runuser": (
        'log runuser "$@"\nwhile [ "$1" != -- ]; do shift; done\nshift\nexec "$@"\n'
    ),
    "curl": 'log curl "$@"\nexit "${CURL_RC:-7}"\n',
}


class _VmBlockRun(NamedTuple):
    returncode: int
    stderr: str
    reached: bool
    calls: list[str]
    mitmdump_user: str


def _run_vm_metadata_block(tmp_path: Path, **env: str) -> _VmBlockRun:
    """Run the VM's metadata block and self-test as the script has them, from
    the line after Docker starts to the export of the proxy's user, with only
    the stubs on PATH, so no real `iptables`, `docker` or `runuser` runs."""
    text = VM_SCRIPT.read_text()
    definitions_start = text.index("MITMDUMP_USER=regression-proxy\n")
    definitions_end = text.index('\necho "== Docker"\n', definitions_start)
    start = text.index("systemctl start docker || true\n") + len(
        "systemctl start docker || true\n"
    )
    export = 'export REGRESSION_MITMDUMP_USER="$MITMDUMP_USER"\n'
    end = text.index(export, start) + len(export)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for name, body in _METADATA_BLOCK_STUBS.items():
        stub = bin_dir / name
        stub.write_text(
            f"#!{shutil.which('bash')}\n"
            'log() { printf "%s\\n" "$*" >> "$CALLS"; }\n' + body
        )
        stub.chmod(0o755)
    calls = tmp_path / "calls"
    calls.write_text("")
    reached = tmp_path / "reached"
    run = subprocess.run(
        [
            str(shutil.which("bash")),
            "-c",
            "\n".join(
                [
                    "set -euo pipefail",
                    _vm_function(text, "pull_image"),
                    text[definitions_start:definitions_end],
                    text[start:end],
                    'printf "%s" "$REGRESSION_MITMDUMP_USER" > "$REACHED"',
                ]
            ),
        ],
        env={
            "PATH": str(bin_dir),
            "CALLS": str(calls),
            "REACHED": str(reached),
            **env,
        },
        capture_output=True,
        text=True,
    )
    return _VmBlockRun(
        run.returncode,
        run.stderr,
        reached.exists(),
        calls.read_text().splitlines(),
        reached.read_text() if reached.exists() else "",
    )


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_the_vm_blocks_the_metadata_server_then_checks_the_block_holds(
    tmp_path: Path,
) -> None:
    """Containers first, then the proxy's own user, whose requests the
    container rule does not see; then the self-test, before the proxy's user
    is handed to the CLI."""
    run = _run_vm_metadata_block(tmp_path)

    assert run.returncode == 0, run.stderr
    assert run.reached
    assert run.mitmdump_user == "regression-proxy"
    assert run.calls == [
        f"iptables {CONTAINER_RULE}",
        "id -u regression-proxy",
        (
            "useradd --system --create-home --home-dir /var/lib/regression-proxy "
            + "--shell /usr/sbin/nologin regression-proxy"
        ),
        f"iptables {PROXY_USER_RULE}",
        "docker pull -q mirror.gcr.io/library/busybox:1.36.1",
        "docker tag mirror.gcr.io/library/busybox:1.36.1 library/busybox:1.36.1",
        (
            "docker run --rm library/busybox:1.36.1 wget -q -T 5 -O /dev/null "
            + f"--header Metadata-Flavor: Google {METADATA_URL}"
        ),
        (
            "runuser -u regression-proxy -- curl -sf -m 5 -o /dev/null "
            + f"-H Metadata-Flavor: Google {METADATA_URL}"
        ),
        f"curl -sf -m 5 -o /dev/null -H Metadata-Flavor: Google {METADATA_URL}",
        "docker run --rm library/busybox:1.36.1 nslookup storage.googleapis.com",
    ]


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
@pytest.mark.parametrize(
    ("env", "message"),
    [
        pytest.param(
            {"WGET_RC": "0"},
            "A container reached the metadata server.",
            id="a-container-reaches-it",
        ),
        pytest.param(
            {"CURL_RC": "0"},
            "The proxy's user reached the metadata server.",
            id="the-proxy-user-reaches-it",
        ),
        pytest.param(
            {"NSLOOKUP_RC": "1"},
            "A container could not resolve a name.",
            id="containers-lose-dns",
        ),
    ],
)
def test_the_self_test_stops_the_run_unless_the_block_holds(
    tmp_path: Path, env: dict[str, str], message: str
) -> None:
    """The job's failure is the run's internal failure, which Finalize reports."""
    run = _run_vm_metadata_block(tmp_path, **env)

    assert run.returncode == 1
    assert message in run.stderr
    assert "stopping before any command runs" in run.stderr
    assert not run.reached


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_a_rule_that_does_not_apply_stops_the_run(tmp_path: Path) -> None:
    """For example, no DOCKER-USER chain: Docker did not start."""
    run = _run_vm_metadata_block(tmp_path, IPTABLES_RC="1")

    assert run.returncode == 1
    assert not run.reached
    assert run.calls == [f"iptables {CONTAINER_RULE}"]


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_an_existing_proxy_user_is_not_added_again(tmp_path: Path) -> None:
    run = _run_vm_metadata_block(tmp_path, ID_RC="0")

    assert run.returncode == 0, run.stderr
    assert not [call for call in run.calls if call.startswith("useradd")]


def test_the_metadata_block_holds_before_any_image_or_command_runs() -> None:
    """After Docker starts, so its chain exists; before the PR's image is
    loaded and before the first command. The CLI gets the proxy's user only
    after the self-test passed, and the Python the proxy runs from lives
    where that user can reach it."""
    text = VM_SCRIPT.read_text()

    assert (
        text.index("systemctl start docker")
        < text.index("\nblock_metadata_server\n")
        < text.index("\nif ! metadata_block_holds; then\n")
        < text.index('export REGRESSION_MITMDUMP_USER="$MITMDUMP_USER"')
        < text.index("\n  load_target_image\nfi\n")
        < text.index('pull_image "$image"')
        < text.index("uv run airbyte-ops cloud connector regression-test")
    )
    assert text.index('export UV_PYTHON_INSTALL_DIR="$WORK/python"') < text.index(
        "uv python install"
    )


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_vm_gcs_transfers_quote_object_names(tmp_path: Path) -> None:
    text = VM_SCRIPT.read_text()
    functions = []
    for name in ("split_gs_uri", "gcs_get", "gcs_put"):
        start = text.index(f"{name}() {{")
        end = text.index("\n}\n", start) + 2
        functions.append(text[start:end])

    curl_bin = tmp_path / "bin"
    curl_bin.mkdir()
    curl_log = tmp_path / "curl-args"
    curl = curl_bin / "curl"
    curl.write_text('#!/bin/sh\nprintf \'%s\\n\' "$@" >> "$CURL_ARGS_FILE"\n')
    curl.chmod(0o755)

    env = {
        **os.environ,
        "PATH": f"{curl_bin}{os.pathsep}{os.environ['PATH']}",
        "CURL_ARGS_FILE": str(curl_log),
        "RUNNER_TEMP": str(tmp_path),
    }
    run_script = "\n".join(
        [
            "set -euo pipefail",
            "metadata_token() { printf token; }",
            *functions,
            'gcs_get "gs://bucket/gh/123-1/source.tar.gz" "$RUNNER_TEMP/download.tar.gz"',
            'gcs_put "$RUNNER_TEMP/upload.tar.gz" "gs://bucket/gh/123-1/source.tar.gz"',
        ]
    )
    subprocess.run(
        ["bash", "-e", "-o", "pipefail", "-c", run_script],
        env=env,
        check=True,
    )

    urls = [
        line
        for line in curl_log.read_text().splitlines()
        if line.startswith("https://")
    ]
    assert urls == [
        "https://storage.googleapis.com/storage/v1/b/bucket/o/"
        + "gh%2F123-1%2Fsource.tar.gz?alt=media",
        "https://storage.googleapis.com/upload/storage/v1/b/bucket/o"
        + "?uploadType=media&name=gh%2F123-1%2Fsource.tar.gz",
    ]


@pytest.mark.parametrize(
    ("discover_output", "success", "discover_passed"),
    [
        ("success=false\nregression_detected=true\n", False, False),
        ("success=true\nregression_detected=false\n", True, True),
    ],
    ids=["exit-0-with-success-false", "exit-0-with-success-true"],
)
def test_vm_summary_fails_a_command_that_exits_0_with_success_false(
    tmp_path: Path, discover_output: str, success: bool, discover_passed: bool
) -> None:
    """The CLI exits 0 on a failed verdict so the remaining commands still
    run; its `success` output says the command failed, and the summary keeps
    the real exit code beside it."""
    text = VM_SCRIPT.read_text()
    opener = 'python3 - "$OUT" "$rc" "$WORK" <<\'PY\'\n'
    start = text.index(opener) + len(opener)
    summary_script = tmp_path / "summary.py"
    summary_script.write_text(text[start : text.index("\nPY\n", start) + 1])
    work = tmp_path / "work"
    out = work / "out"
    out.mkdir(parents=True)
    for command, output in (
        ("spec", "success=true\n"),
        ("check", "success=true\n"),
        ("discover", discover_output),
        ("read", "success=true\n"),
    ):
        (work / f"{command}.exit-code").write_text("0\n")
        (work / f"{command}.github-output").write_text(output)

    subprocess.run(
        [sys.executable, str(summary_script), str(out), "0", str(work)], check=True
    )

    summary = json.loads((out / "summary.json").read_text())
    assert summary["exit_code"] == 0
    assert summary["success"] is success
    assert {item["command"]: item for item in summary["commands"]}["discover"] == {
        "command": "discover",
        "exit_code": 0,
        "passed": discover_passed,
    }
    assert all(
        item["passed"] for item in summary["commands"] if item["command"] != "discover"
    )


def test_s13_eu_workflow_does_not_upload_artifacts_or_pass_secrets() -> None:
    job = _eu_job()
    rendered = json.dumps(job)
    assert not any(
        "actions/upload-artifact" in step.get("uses", "") for step in job["steps"]
    )
    assert "secrets." not in rendered
    assert "inputs.output_mode" not in rendered
    assert "inputs.enable_debug_logs" not in rendered


def test_s9_workflow_refuses_raw_eu_output_mode_before_dispatch() -> None:
    resolve = _workflow()["jobs"]["resolve-residency"]
    assert any(
        "EU-resident connections always run masked; output_mode=raw is refused."
        in step.get("run", "")
        for step in resolve["steps"]
    )


def test_s13_batch_deadline_ends_inside_the_workflow_job_timeout() -> None:
    """GitHub cancels the job at its timeout, and a Batch job still running
    then is never read, so the deadline is what the job has left when it
    submits, less ten minutes for provisioning and reading the result."""
    job = _eu_job()
    assert job["timeout-minutes"] == 360
    assert job["env"]["GITHUB_TIMEOUT_MINUTES"] == job["timeout-minutes"]
    for elapsed in (0, 300, 3600):
        deadline = max_run_duration_seconds(360, elapsed_seconds=elapsed)
        assert elapsed + deadline == (360 - 10) * 60
    with pytest.raises(ValueError, match="no time left"):
        max_run_duration_seconds(360, elapsed_seconds=350 * 60)
    assert job["steps"][0]["id"] == "job-start"
    build_job = next(step for step in job["steps"] if step.get("id") == "build-job")
    assert build_job["env"]["JOB_STARTED_AT"] == "${{ steps.job-start.outputs.epoch }}"
    assert (
        'max_run_duration_seconds(int(os.environ["GITHUB_TIMEOUT_MINUTES"]), '
        'int(time.time()) - int(os.environ["JOB_STARTED_AT"]))' in build_job["run"]
    )


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_s11_vm_runner_shell_and_masking() -> None:
    subprocess.run(["bash", "-n", str(VM_SCRIPT)], check=True)
    text = VM_SCRIPT.read_text()
    assert (
        "export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
        in text
    )
    assert "--output-mode masked" in text


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
@pytest.mark.parametrize(
    ("ending", "exit_code"), [("exit 0", 0), ("exit 3", 3), ("false", 1)]
)
def test_vm_runner_makes_the_mask_key_under_work_and_removes_it_on_exit(
    tmp_path: Path, ending: str, exit_code: int
) -> None:
    """The key is made once under $WORK, never under $OUT, readable by its
    owner only and printed nowhere; it goes when the script exits, on a pass,
    a failure or a `set -e` stop, and the script keeps its exit code."""
    text = VM_SCRIPT.read_text()
    start = text.index('MASK_KEY_PATH="$WORK/mask_key"\n')
    last_line = 'chmod 600 "$MASK_KEY_PATH"\n'
    end = text.index(last_line, start) + len(last_line)
    work = tmp_path / "work"
    out = work / "out"
    out.mkdir(parents=True)
    key_copy = tmp_path / "key-copy"
    key_path_file = tmp_path / "key-path"

    run = subprocess.run(
        [
            "bash",
            "-c",
            "\n".join(
                [
                    "set -euo pipefail",
                    'OUT="$WORK/out"',
                    text[start:end],
                    'cp -p "$MASK_KEY_PATH" "$KEY_COPY"',
                    'printf "%s" "$MASK_KEY_PATH" > "$KEY_PATH_FILE"',
                    ending,
                ]
            ),
        ],
        env={
            **os.environ,
            "WORK": str(work),
            "KEY_COPY": str(key_copy),
            "KEY_PATH_FILE": str(key_path_file),
        },
        capture_output=True,
        text=True,
    )

    assert run.returncode == exit_code
    assert run.stdout == ""
    assert run.stderr == ""
    key_path = Path(key_path_file.read_text())
    assert key_path == work / "mask_key"
    assert out not in key_path.parents
    assert re.fullmatch(r"[0-9a-f]{64}\n", key_copy.read_text())
    assert key_copy.stat().st_mode & 0o777 == 0o600
    assert not key_path.exists()


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_vm_runner_passes_the_mask_key_path_to_every_command(tmp_path: Path) -> None:
    text = VM_SCRIPT.read_text()
    start = text.index('rc=0\nlast_command=""\n')
    end = text.index("\ndone\n", start) + len("\ndone\n")
    work = tmp_path / "work"
    (work / "out").mkdir(parents=True)
    uv_bin = tmp_path / "bin"
    uv_bin.mkdir()
    uv_log = tmp_path / "uv-args"
    uv = uv_bin / "uv"
    uv.write_text('#!/bin/sh\nprintf \'%s\\n\' --- "$@" >> "$UV_ARGS_FILE"\n')
    uv.chmod(0o755)

    run = subprocess.run(
        [
            "bash",
            "-c",
            "\n".join(
                [
                    "set -euo pipefail",
                    'OUT="$WORK/out"',
                    'MASK_KEY_PATH="$WORK/mask_key"',
                    "COMMANDS=(spec check discover read)",
                    "CLI_ARGS=(--connector-name source-example --connection-id c-1)",
                    'STATE_ARGS=(--state-path "$WORK/state.json")',
                    "HAS_CONNECTION_ID=true",
                    "HAS_CATALOG_PATH=false",
                    text[start:end],
                ]
            ),
        ],
        env={
            **os.environ,
            "PATH": f"{uv_bin}{os.pathsep}{os.environ['PATH']}",
            "WORK": str(work),
            "UV_ARGS_FILE": str(uv_log),
        },
        capture_output=True,
        text=True,
    )

    assert run.returncode == 0, run.stderr
    calls = [call.splitlines() for call in uv_log.read_text().split("---\n")[1:]]
    assert [call[call.index("--command") + 1] for call in calls] == [
        "spec",
        "check",
        "discover",
        "read",
    ]
    for call in calls:
        assert call.count("--mask-key-path") == 1, call
        assert call[call.index("--mask-key-path") + 1] == str(work / "mask_key")


def test_vm_runner_never_prints_or_uploads_the_mask_key() -> None:
    """The commands get the key as a path only. No line that names it prints
    it, the script never traces its commands, and every upload comes from
    $OUT or a named file beside it, so the key under $WORK is in none."""
    text = VM_SCRIPT.read_text()
    key_lines = [line for line in text.splitlines() if "mask_key" in line.lower()]
    assert key_lines
    for line in key_lines:
        assert not re.search(r"\b(echo|printf|cat|tee|head|tail|xxd|od)\b", line), line
    assert "set -x" not in text
    assert "xtrace" not in text
    assert re.findall(r'^\s*gcs_put "([^"]+)"', text, flags=re.MULTILINE) == [
        "$OUT/summary.json",
        "$WORK/verdict.json",
        "$WORK/out.tar.gz",
        "$OUT/report.html",
    ]
    assert (
        "tar --exclude='*.mitm' --exclude='*.har' "
        '-czf "$WORK/out.tar.gz" -C "$WORK" out\n'
    ) in text


@pytest.mark.skipif(
    shutil.which("bash") is None or shutil.which("tar") is None,
    reason="needs bash and tar",
)
def test_s6_vm_archive_leaves_out_http_captures(tmp_path: Path) -> None:
    """The CLI leaves each side's capture in $OUT and relies on the upload to
    drop it. The line that builds the uploaded archive, run as the script has
    it, keeps every capture out at any depth and everything else in."""
    text = VM_SCRIPT.read_text()
    upload = 'gcs_put "$WORK/out.tar.gz" "$RUN_PREFIX_URI/out.tar.gz"\n'
    end = text.index(upload)
    archive_line = text[text.rindex("\n", 0, end - 1) + 1 : end]
    assert archive_line.startswith("tar ")
    work = tmp_path / "work"
    captures = {
        f"out/{command}/{side}/http_traffic.{suffix}"
        for command in ("spec", "read")
        for side in ("control", "target")
        for suffix in ("mitm", "har")
    }
    kept = {
        "out/summary.json",
        "out/report.html",
        "out/read/regression_report.json",
        "out/read/connection_data/catalog.json",
        "out/read/target/mitmdump.log",
        "out/read/target/airbyte_messages/record.jsonl",
    }
    for name in captures | kept:
        path = work / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}\n")

    subprocess.run(
        ["bash", "-c", archive_line], env={**os.environ, "WORK": str(work)}, check=True
    )

    with tarfile.open(work / "out.tar.gz") as archive:
        names = set(archive.getnames())
    assert kept <= names
    assert not [name for name in names if name.endswith((".mitm", ".har"))]
