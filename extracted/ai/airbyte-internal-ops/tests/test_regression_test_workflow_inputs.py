# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""The `run_regression_tests` tool's contract with the workflow it dispatches."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Any, NamedTuple, cast
from unittest.mock import patch

import pytest
import requests
import yaml
from fastmcp import Context

from airbyte_ops_mcp import github_actions
from airbyte_ops_mcp.github_actions import WorkflowDispatchResult
from airbyte_ops_mcp.mcp import connector_qa
from airbyte_ops_mcp.mcp.connector_qa import (
    READ_TIMEOUT_MINUTES_MAX,
    REGRESSION_TEST_WORKFLOW_FILE,
    ConnectorRepo,
    TestRunStatus,
    run_regression_tests,
)
from airbyte_ops_mcp.regression_tests.seed_state import (
    SEED_STATE_NEEDS_CONNECTION,
    SEED_STATE_NEEDS_DISPATCH,
    seed_state_error,
)
from tests.test_regression_seed_state import REFUSED_SEEDS, SEED

pytestmark = pytest.mark.unit

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = REPO_ROOT / ".github/workflows" / REGRESSION_TEST_WORKFLOW_FILE
CONNECTION_ID = "00000000-0000-0000-0000-000000000000"

needs_bash = pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")


def _declared_inputs() -> set[str]:
    """The inputs the dispatched workflow actually accepts.

    GitHub rejects a dispatch carrying an input the workflow does not declare,
    so a name that drifts here fails at trigger time, in someone else's session.

    The *intersection* of both trigger blocks, because the workflow is both
    dispatched and called as a sub-workflow, and the two input lists are edited
    by hand. An input declared only under `workflow_dispatch` satisfies the tool
    that dispatches it and fails whoever calls the workflow as a sub-workflow, so
    a union here would pass on exactly the drift this test exists to catch.
    """
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text())
    # `on:` parses as the boolean True in YAML 1.1.
    triggers = workflow[True] if True in workflow else workflow["on"]

    return set.intersection(
        *(
            set(triggers[trigger]["inputs"])
            for trigger in ("workflow_dispatch", "workflow_call")
        )
    )


def _dispatch(**kwargs: Any) -> dict[str, str]:
    """Run the tool with the dispatch stubbed; return the inputs it sent."""
    sent: dict[str, str] = {}

    def _fake_dispatch(*, inputs: dict[str, str], **_kwargs: Any):
        sent.update(inputs)
        return WorkflowDispatchResult(workflow_url="https://example.com/workflow")

    with patch.object(
        connector_qa, "trigger_workflow_dispatch", _fake_dispatch
    ), patch.object(
        connector_qa, "resolve_ci_trigger_github_token", lambda: "token"
    ), patch.object(
        connector_qa,
        "query_connection_workspace_details",
        lambda _connection_ids: [{"dataplane_name": "US"}],
    ):
        run_regression_tests(
            connector_name="source-pokeapi",
            pr=1,
            repo=ConnectorRepo.AIRBYTE,
            ctx=cast(Context, object()),
            **kwargs,
        )

    return sent


def _refused(**kwargs: Any) -> str:
    """Run the tool expecting it to refuse before dispatch; return its message."""
    dispatched: list[dict[str, str]] = []

    with patch.object(
        connector_qa,
        "trigger_workflow_dispatch",
        lambda *, inputs, **_kwargs: dispatched.append(inputs),
    ), patch.object(connector_qa, "resolve_ci_trigger_github_token", lambda: "token"):
        response = run_regression_tests(
            connector_name="source-pokeapi",
            pr=1,
            repo=ConnectorRepo.AIRBYTE,
            **kwargs,
            ctx=cast(Context, object()),
        )

    assert response.status is TestRunStatus.FAILED
    assert not dispatched
    return response.message


def _job(job_id: str = "regression-test") -> dict[str, Any]:
    return yaml.safe_load(WORKFLOW_PATH.read_text())["jobs"][job_id]


def _step(step_id: str, job_id: str = "regression-test") -> dict[str, Any]:
    (step,) = [step for step in _job(job_id)["steps"] if step.get("id") == step_id]
    return step


class _StepRun(NamedTuple):
    returncode: int
    outputs: dict[str, str]
    stdout: str


_EXPRESSION = re.compile(r"\$\{\{ (.+?) \}\}")


def _run_step(
    step_id: str,
    tmp_path: Path,
    *,
    env: dict[str, str],
    expressions: dict[str, str] | None = None,
    path_prefix: tuple[str, ...] = (),
    job_id: str = "regression-test",
) -> _StepRun:
    """Run a step's script under bash as GitHub would; return its exit code, outputs and stdout.

    `expressions` resolves the `${{ ... }}` the script holds; one the test did
    not resolve fails here, so a new expression gets a value on purpose. The
    script runs from the checkout, as on the runner.
    """

    def resolve(match: re.Match[str]) -> str:
        assert expressions and match[1] in expressions, f"unresolved {match[0]}"
        return expressions[match[1]]

    script = _EXPRESSION.sub(resolve, _step(step_id, job_id)["run"])
    output = tmp_path / f"{step_id}_github_output"
    output.touch()
    result = subprocess.run(
        ["bash", "-e", "-c", script],
        cwd=REPO_ROOT,
        env={
            "GITHUB_OUTPUT": str(output),
            # The test's interpreter first, so `python3` is one that runs the
            # repository's code wherever the test runs.
            "PATH": os.pathsep.join(
                [*path_prefix, str(Path(sys.executable).parent), "/usr/bin", "/bin"]
            ),
            **env,
        },
        capture_output=True,
        text=True,
        check=False,
    )
    outputs = dict(line.split("=", 1) for line in output.read_text().splitlines())
    return _StepRun(result.returncode, outputs, result.stdout)


READ_INPUTS_ENV = {
    "READ_TIMEOUT_MINUTES": "${{ inputs.read_timeout_minutes }}",
    "MAX_RECORDS": "${{ inputs.max_records }}",
    "CONNECTION_ID": "${{ inputs.connection_id }}",
    "STATE_JSON_GIVEN": "${{ inputs.state_json != '' }}",
}


def _run_read_inputs(
    tmp_path: Path,
    *,
    read_timeout_minutes: str = "",
    max_records: str = "",
    connection_id: str = "",
    state_json: str | None = None,
    state_json_given: bool | None = None,
) -> _StepRun:
    """Run the read-inputs step as GitHub would, with the seed in the dispatch payload."""
    # The inputs reach the script only through these variables, and the seed
    # itself is not among them (see the step).
    assert _step("read-inputs")["env"] == READ_INPUTS_ENV
    event = tmp_path / "event.json"
    inputs = {} if state_json is None else {"state_json": state_json}
    event.write_text(json.dumps({"inputs": inputs}))
    runner_temp = tmp_path / "runner_temp"
    runner_temp.mkdir(exist_ok=True)
    if state_json_given is None:
        state_json_given = bool(state_json)

    return _run_step(
        "read-inputs",
        tmp_path,
        env={
            "READ_TIMEOUT_MINUTES": read_timeout_minutes,
            "MAX_RECORDS": max_records,
            "CONNECTION_ID": connection_id,
            "STATE_JSON_GIVEN": "true" if state_json_given else "false",
            "GITHUB_EVENT_PATH": str(event),
            "RUNNER_TEMP": str(runner_temp),
        },
    )


def _run_read_step(
    tmp_path: Path,
    inputs_outputs: dict[str, str],
    *,
    with_state: str = "",
    catalog_mode: str = "connection_id",
) -> list[str]:
    """Run the READ step's script with `uv` stubbed; return the CLI's argv."""
    read_step = _step("run-read")
    # The seed as a path and the cap as digits, both from read-inputs.
    assert (
        read_step["env"]["SEED_STATE_PATH"]
        == "${{ steps.read-inputs.outputs.seed_state_path }}"
    )
    assert (
        read_step["env"]["MAX_RECORDS"]
        == "${{ steps.read-inputs.outputs.max_records }}"
    )
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    argv_file = tmp_path / "argv"
    stub = bin_dir / "uv"
    stub.write_text('#!/bin/bash\nprintf "%s\\n" "$@" > "$ARGV_FILE"\n')
    stub.chmod(0o755)
    catalog = tmp_path / "configured_catalog.json"
    catalog.write_text("{}")

    run = _run_step(
        "run-read",
        tmp_path,
        env={
            "SEED_STATE_PATH": inputs_outputs.get("seed_state_path", ""),
            "MAX_RECORDS": inputs_outputs.get("max_records", ""),
            "READ_TIMEOUT_SECONDS": inputs_outputs["read_timeout_seconds"],
            "ARGV_FILE": str(argv_file),
        },
        expressions={
            "steps.setup.outputs.catalog_mode": catalog_mode,
            "steps.setup.outputs.configured_catalog_path": str(catalog),
            "inputs.with_state": with_state,
            "steps.setup.outputs.common_args": "--connector-name source-pokeapi",
            "steps.setup.outputs.read_output_dir": str(tmp_path / "read"),
        },
        path_prefix=(str(bin_dir),),
    )

    assert run.returncode == 0, run.stdout
    return argv_file.read_text().splitlines()


def _read_step_budget(outputs: dict[str, str]) -> tuple[int, int]:
    """The READ step's `timeout-minutes` and `--read-timeout`, from read-inputs' outputs.

    Resolves only the two expression shapes the step uses, so rewriting either
    into another shape fails here instead of passing unchecked.
    """
    read_step = _step("run-read")
    timeout = re.fullmatch(
        r"\$\{\{ fromJSON\(steps\.read-inputs\.outputs\.(\w+)\) \}\}",
        read_step["timeout-minutes"],
    )
    assert timeout, read_step["timeout-minutes"]
    flag = re.search(r'--read-timeout "\$(\w+)"', read_step["run"])
    assert flag, "the READ step no longer passes --read-timeout from its env"
    seconds = re.fullmatch(
        r"\$\{\{ steps\.read-inputs\.outputs\.(\w+) \}\}",
        read_step["env"][flag[1]],
    )
    assert seconds, read_step["env"][flag[1]]
    return int(outputs[timeout[1]]), int(outputs[seconds[1]])


@needs_bash
@pytest.mark.parametrize(
    ("read_timeout_minutes", "step_minutes", "read_timeout_s"),
    [
        pytest.param("", 180, 10200, id="empty-is-the-default"),
        pytest.param("1", 11, 60, id="shortest"),
        pytest.param("240", 250, 14400, id="longer"),
        pytest.param(str(READ_TIMEOUT_MINUTES_MAX), 310, 18000, id="the-cap"),
    ],
)
def test_the_read_step_hands_the_cli_a_budget_that_ends_before_the_step(
    tmp_path: Path, read_timeout_minutes: str, step_minutes: int, read_timeout_s: int
) -> None:
    """GitHub kills a step at its `timeout-minutes` and leaves no report.

    The CLI fits both reads, the comparison and the report inside
    `--read-timeout`, so that budget has to end first: the step gets the
    budget plus ten minutes, with room for `uv run` to start the CLI.
    """
    run = _run_read_inputs(tmp_path, read_timeout_minutes=read_timeout_minutes)

    assert run.returncode == 0, run.stdout
    assert _read_step_budget(run.outputs) == (step_minutes, read_timeout_s)


@needs_bash
@pytest.mark.parametrize(
    "read_timeout_minutes",
    [
        pytest.param("0", id="zero"),
        pytest.param(str(READ_TIMEOUT_MINUTES_MAX + 1), id="above-the-cap"),
        pytest.param("-5", id="negative"),
        pytest.param("90.5", id="fractional"),
        pytest.param("060", id="leading-zero-reads-as-octal-in-bash"),
        pytest.param(" 60", id="padded"),
        pytest.param("1e3", id="exponent"),
        pytest.param("9" * 30, id="overflows-bash-arithmetic"),
    ],
)
def test_the_workflow_refuses_a_read_budget_outside_1_to_the_cap(
    tmp_path: Path, read_timeout_minutes: str
) -> None:
    """The MCP tool checks this before dispatch; a direct dispatch or a calling
    workflow does not go through it."""
    run = _run_read_inputs(tmp_path, read_timeout_minutes=read_timeout_minutes)

    assert run.returncode != 0
    assert run.outputs == {}
    assert "::error::read_timeout_minutes" in run.stdout


@needs_bash
def test_the_job_holds_the_longest_read_step_and_judges_the_inputs_first(
    tmp_path: Path,
) -> None:
    """At the cap the READ step is 310 minutes, inside the job's 360 (the
    GitHub-hosted limit), with fifty minutes left for setup, the build, SPEC,
    CHECK, DISCOVER and the uploads. The inputs are judged before SPEC, so a
    bad value fails the run before the connector is built."""
    run = _run_read_inputs(tmp_path, read_timeout_minutes=str(READ_TIMEOUT_MINUTES_MAX))
    step_minutes, _ = _read_step_budget(run.outputs)
    step_ids = [step.get("id") for step in _job()["steps"]]

    assert _job()["timeout-minutes"] == 360
    assert _job()["timeout-minutes"] - step_minutes == 50
    assert step_ids.index("read-inputs") < step_ids.index("run-spec")


@needs_bash
@pytest.mark.parametrize(
    "max_records",
    [
        pytest.param("0", id="zero"),
        pytest.param("-1", id="negative"),
        pytest.param("5 --no-http-replay", id="a-second-flag"),
        pytest.param("abc", id="not-a-number"),
        pytest.param("1.5", id="fractional"),
        pytest.param("01", id="leading-zero"),
        pytest.param(" 5", id="padded"),
        pytest.param("1e3", id="exponent"),
    ],
)
def test_the_workflow_refuses_a_cap_that_is_not_a_whole_number_of_records(
    tmp_path: Path, max_records: str
) -> None:
    """A value that is not digits never reaches the CLI's command line, where
    `5 --no-http-replay` once split into a second flag."""
    run = _run_read_inputs(tmp_path, max_records=max_records)

    assert run.returncode != 0
    assert "max_records" not in run.outputs
    assert "::error::max_records" in run.stdout


@needs_bash
def test_the_read_step_hands_the_cli_the_cap_and_the_seed_as_single_arguments(
    tmp_path: Path,
) -> None:
    run = _run_read_inputs(
        tmp_path, max_records="500", connection_id=CONNECTION_ID, state_json=SEED
    )
    assert run.returncode == 0, run.stdout

    argv = _run_read_step(tmp_path, run.outputs, with_state="true")

    seed_path = run.outputs["seed_state_path"]
    assert argv[argv.index("--max-records") + 1] == "500"
    assert argv[argv.index("--state-path") + 1] == seed_path
    assert Path(seed_path).read_text() == SEED
    assert argv[argv.index("--read-timeout") + 1] == "10200"
    # The seed replaces the connection's state, so with_state is not also sent.
    assert "--with-state" not in argv
    assert "--no-state" not in argv


@needs_bash
@pytest.mark.parametrize(
    ("with_state", "state_flags"),
    [
        pytest.param("", [], id="unset"),
        pytest.param("true", ["--with-state"], id="warm"),
        pytest.param("false", ["--no-state"], id="cold"),
    ],
)
def test_without_a_seed_or_a_cap_the_read_step_passes_neither(
    tmp_path: Path, with_state: str, state_flags: list[str]
) -> None:
    run = _run_read_inputs(tmp_path)

    argv = _run_read_step(tmp_path, run.outputs, with_state=with_state)

    assert "--max-records" not in argv
    assert "--state-path" not in argv
    assert [arg for arg in argv if arg in ("--with-state", "--no-state")] == state_flags


@needs_bash
def test_the_read_step_passes_the_generated_catalog_in_gsm_mode(tmp_path: Path) -> None:
    run = _run_read_inputs(tmp_path)

    argv = _run_read_step(tmp_path, run.outputs, catalog_mode="gsm")

    assert argv[argv.index("--catalog-path") + 1].endswith("configured_catalog.json")


@needs_bash
@pytest.mark.parametrize(("state_json", "reason"), REFUSED_SEEDS)
def test_the_workflow_refuses_a_seed_by_the_tools_own_rules(
    tmp_path: Path, state_json: str, reason: str
) -> None:
    """The step runs `seed_state.py` from the checkout; this pins that it does,
    and that a bad seed fails the run before SPEC rather than at READ."""
    run = _run_read_inputs(tmp_path, connection_id=CONNECTION_ID, state_json=state_json)

    assert run.returncode != 0
    assert "seed_state_path" not in run.outputs
    assert f"::error::{seed_state_error(state_json)}" in run.stdout.splitlines()


@needs_bash
def test_a_seed_without_a_connection_is_refused_before_spec(tmp_path: Path) -> None:
    """Without a connection the generated catalog is all full_refresh, and
    the seed would be ignored while the run still called the read seeded."""
    run = _run_read_inputs(tmp_path, state_json=SEED)

    assert run.returncode != 0
    assert "seed_state_path" not in run.outputs
    assert f"::error::{SEED_STATE_NEEDS_CONNECTION}" in run.stdout.splitlines()


@needs_bash
def test_a_seed_from_a_calling_workflow_is_refused(tmp_path: Path) -> None:
    """A calling workflow's inputs are not in the event payload, and taking the
    seed through the environment would print it in the job log."""
    run = _run_read_inputs(
        tmp_path, connection_id=CONNECTION_ID, state_json=None, state_json_given=True
    )

    assert run.returncode != 0
    assert "seed_state_path" not in run.outputs
    assert f"::error::{SEED_STATE_NEEDS_DISPATCH}" in run.stdout.splitlines()


@needs_bash
def test_the_seed_is_masked_before_it_prints_and_never_sits_in_a_step(
    tmp_path: Path,
) -> None:
    """The runner prints a step's `env:` and `with:` in its log header before
    the step runs, so a seed there would be in the job log, which outlives the
    artifacts, before anything could mask it."""
    run = _run_read_inputs(tmp_path, connection_id=CONNECTION_ID, state_json=SEED)
    assert run.returncode == 0, run.stdout

    lines = run.stdout.splitlines()
    first_mention = next(index for index, line in enumerate(lines) if SEED in line)
    assert lines[first_mention] == f"::add-mask::{SEED}"

    mentions = [
        step.get("name")
        for step in _job()["steps"]
        if re.search(r"inputs\.state_json\s*\}\}", json.dumps(step))
    ]
    assert mentions == [], "a step takes the seed's value, which its header prints"
    assert (
        _step("read-inputs")["env"]["STATE_JSON_GIVEN"]
        == "${{ inputs.state_json != '' }}"
    )


EU_SEED_STEP_ENV = {
    "STATE_JSON_GIVEN": "${{ inputs.state_json != '' }}",
    "CONNECTION_ID": "${{ inputs.connection_id }}",
    "RUN_PREFIX": "${{ steps.paths.outputs.prefix }}",
}
EU_RUN_PREFIX = "gs://internal-airbyte-ai-infra-connector-regression-eu/gh/123-1"


class _EuSeedRun(NamedTuple):
    run: _StepRun
    gcloud_calls: list[str]
    staged: str | None
    seed_file: Path


def _run_eu_seed_step(
    tmp_path: Path,
    *,
    connection_id: str = "",
    state_json: str | None = None,
    state_json_given: bool | None = None,
) -> _EuSeedRun:
    """Run the EU job's seed step as GitHub would, with `gcloud` stubbed to
    record its arguments and keep a copy of the file it uploads."""
    # As in the US job, the seed itself is not among the step's inputs.
    assert (
        _step("stage-seed-state", job_id="regression-test-eu")["env"]
        == EU_SEED_STEP_ENV
    )
    event = tmp_path / "event.json"
    inputs = {} if state_json is None else {"state_json": state_json}
    event.write_text(json.dumps({"inputs": inputs}))
    runner_temp = tmp_path / "runner_temp"
    runner_temp.mkdir(exist_ok=True)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    gcloud = bin_dir / "gcloud"
    gcloud.write_text(
        '#!/bin/sh\nprintf "%s\\n" "$*" >> "$GCLOUD_ARGS_FILE"\ncp "$3" "$GCLOUD_STAGED"\n'
    )
    gcloud.chmod(0o755)
    gcloud_args = tmp_path / "gcloud-args"
    staged = tmp_path / "staged"
    if state_json_given is None:
        state_json_given = bool(state_json)

    run = _run_step(
        "stage-seed-state",
        tmp_path,
        env={
            "STATE_JSON_GIVEN": "true" if state_json_given else "false",
            "CONNECTION_ID": connection_id,
            "RUN_PREFIX": EU_RUN_PREFIX,
            "GITHUB_EVENT_PATH": str(event),
            "RUNNER_TEMP": str(runner_temp),
            "GCLOUD_ARGS_FILE": str(gcloud_args),
            "GCLOUD_STAGED": str(staged),
        },
        path_prefix=(str(bin_dir),),
        job_id="regression-test-eu",
    )
    return _EuSeedRun(
        run,
        gcloud_args.read_text().splitlines() if gcloud_args.exists() else [],
        staged.read_text() if staged.exists() else None,
        runner_temp / "seed_state.json",
    )


@needs_bash
def test_the_eu_seed_is_masked_staged_from_a_file_and_never_sits_in_a_step(
    tmp_path: Path,
) -> None:
    """The EU job's log is a US job log: a seed in a step's `env:` would be
    printed there before anything could mask it. The step stages the file
    seed_state.py writes from the dispatch payload, then removes it."""
    seed_run = _run_eu_seed_step(tmp_path, connection_id=CONNECTION_ID, state_json=SEED)
    assert seed_run.run.returncode == 0, seed_run.run.stdout

    lines = seed_run.run.stdout.splitlines()
    first_mention = next(index for index, line in enumerate(lines) if SEED in line)
    assert lines[first_mention] == f"::add-mask::{SEED}"
    assert seed_run.gcloud_calls == [
        f"storage cp {seed_run.seed_file} {EU_RUN_PREFIX}/state.json"
    ]
    assert seed_run.staged == SEED
    assert not seed_run.seed_file.exists()
    assert seed_run.run.outputs == {"staged": "true"}

    job = _job("regression-test-eu")
    assert not re.search(r"inputs\.state_json\s*\}\}", json.dumps(job.get("env", {})))
    mentions = [
        step.get("name")
        for step in job["steps"]
        if re.search(r"inputs\.state_json\s*\}\}", json.dumps(step))
    ]
    assert mentions == [], "a step takes the seed's value, which its header prints"


@needs_bash
def test_no_eu_seed_stages_nothing(tmp_path: Path) -> None:
    seed_run = _run_eu_seed_step(tmp_path, connection_id=CONNECTION_ID)

    assert seed_run.run.returncode == 0, seed_run.run.stdout
    assert seed_run.gcloud_calls == []
    assert seed_run.run.outputs == {}


def _run_eu_build_job(tmp_path: Path, **env: str) -> list[str]:
    """Run the EU job's build-job step with `uv` stubbed; return the argv it
    hands `build-job-spec`. `uv run python` still runs, so the step's own
    deadline arithmetic is exercised."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    argv_file = tmp_path / "build-job-spec-argv"
    stub = bin_dir / "uv"
    stub.write_text(
        "#!/bin/sh\n"
        'if [ "$1" = run ] && [ "$2" = python ]; then shift 2; exec python3 "$@"; fi\n'
        'printf "%s\\n" "$@" > "$ARGV_FILE"\n'
    )
    stub.chmod(0o755)
    job = _job("regression-test-eu")

    run = _run_step(
        "build-job",
        tmp_path,
        env={
            "GITHUB_TIMEOUT_MINUTES": str(job["env"]["GITHUB_TIMEOUT_MINUTES"]),
            "GITHUB_WORKSPACE": str(tmp_path),
            "JOB_ID": "gh-123-1",
            "SOURCE_URI": f"{EU_RUN_PREFIX}/source.tar.gz",
            "RUN_PREFIX": EU_RUN_PREFIX,
            "RUN_ID": "123",
            "CONNECTOR": "source-pokeapi",
            "CONNECTION_ID": CONNECTION_ID,
            "READ_TIMEOUT_SECONDS": "10200",
            "JOB_STARTED_AT": str(int(time.time())),
            "ARGV_FILE": str(argv_file),
            "TARGET_IMAGE": BUILT_IMAGE,
            **env,
        },
        path_prefix=(str(bin_dir),),
        job_id="regression-test-eu",
    )

    assert run.returncode == 0, run.stdout
    return argv_file.read_text().splitlines()


EU_READ_INPUTS_ENV = {
    "READ_TIMEOUT_MINUTES": "${{ inputs.read_timeout_minutes }}",
    "MAX_RECORDS": "${{ inputs.max_records }}",
}


def _run_eu_read_inputs(
    tmp_path: Path, *, read_timeout_minutes: str = "", max_records: str = ""
) -> _StepRun:
    assert (
        _step("read-inputs", job_id="regression-test-eu")["env"] == EU_READ_INPUTS_ENV
    )
    return _run_step(
        "read-inputs",
        tmp_path,
        env={"READ_TIMEOUT_MINUTES": read_timeout_minutes, "MAX_RECORDS": max_records},
        job_id="regression-test-eu",
    )


def _eu_cli_args(tmp_path: Path, read_inputs: _StepRun) -> list[str]:
    """The regression-test arguments the EU job hands the VM, from read-inputs' outputs."""
    build_job = _step("build-job", job_id="regression-test-eu")
    assert (
        build_job["env"]["READ_TIMEOUT_SECONDS"]
        == "${{ steps.read-inputs.outputs.read_timeout_seconds }}"
    )
    assert (
        build_job["env"]["MAX_RECORDS"]
        == "${{ steps.read-inputs.outputs.max_records }}"
    )
    argv = _run_eu_build_job(
        tmp_path,
        READ_TIMEOUT_SECONDS=read_inputs.outputs["read_timeout_seconds"],
        MAX_RECORDS=read_inputs.outputs.get("max_records", ""),
    )
    return json.loads(argv[argv.index("--cli-args-json") + 1])


def test_both_jobs_resolve_the_read_inputs_with_one_script() -> None:
    resolve = (
        "python3 src/airbyte_ops_mcp/regression_tests/read_inputs.py "
        '"$READ_TIMEOUT_MINUTES" "$MAX_RECORDS" "$GITHUB_OUTPUT"'
    )
    assert resolve in _step("read-inputs")["run"].splitlines()
    assert _step("read-inputs", job_id="regression-test-eu")["run"].strip() == resolve
    # Every other EU step takes what read-inputs resolved, never the inputs.
    for step in _job("regression-test-eu")["steps"]:
        if step.get("id") != "read-inputs":
            text = json.dumps(step)
            assert "inputs.read_timeout_minutes" not in text, step["name"]
            assert "inputs.max_records" not in text, step["name"]


@needs_bash
@pytest.mark.parametrize(
    ("read_timeout_minutes", "read_timeout_s"),
    [
        pytest.param("", "10200", id="empty-is-the-default"),
        pytest.param("1", "60", id="shortest"),
        pytest.param(str(READ_TIMEOUT_MINUTES_MAX), "18000", id="the-cap"),
    ],
)
def test_the_eu_job_always_hands_the_cli_the_resolved_read_timeout(
    tmp_path: Path, read_timeout_minutes: str, read_timeout_s: str
) -> None:
    """Without `--read-timeout` the CLI's own 240 minutes would apply, not the
    170 the input promises."""
    run = _run_eu_read_inputs(tmp_path, read_timeout_minutes=read_timeout_minutes)
    assert run.returncode == 0, run.stdout

    args = _eu_cli_args(tmp_path, run)

    assert args.count("--read-timeout") == 1
    assert args[args.index("--read-timeout") + 1] == read_timeout_s
    assert "--max-records" not in args


@needs_bash
@pytest.mark.parametrize(
    "read_timeout_minutes",
    [
        pytest.param("0", id="zero"),
        pytest.param(str(READ_TIMEOUT_MINUTES_MAX + 1), id="above-the-cap"),
        pytest.param("600", id="past-the-github-job"),
        pytest.param("999", id="three-digits"),
        pytest.param("ten", id="not-a-number"),
        pytest.param("-5", id="negative"),
        pytest.param("90.5", id="fractional"),
        # Shell arithmetic would run the subscript's command substitution.
        pytest.param("a[$(touch {marker})]", id="an-arithmetic-expression"),
    ],
)
def test_the_eu_job_refuses_a_read_budget_outside_1_to_the_cap_before_submitting(
    tmp_path: Path, read_timeout_minutes: str
) -> None:
    marker = tmp_path / "evaluated"
    run = _run_eu_read_inputs(
        tmp_path, read_timeout_minutes=read_timeout_minutes.format(marker=marker)
    )

    assert run.returncode != 0
    assert run.outputs == {}
    assert "::error::read_timeout_minutes" in run.stdout
    assert not marker.exists()
    names = [step["name"] for step in _job("regression-test-eu")["steps"]]
    assert (
        names.index("Resolve READ inputs")
        < names.index("Authenticate to GCP with Workload Identity Federation")
        < names.index("Submit EU Batch job")
    )


@needs_bash
@pytest.mark.parametrize(
    "max_records",
    [
        pytest.param("ten", id="not-a-number"),
        pytest.param("0", id="zero"),
        pytest.param("5 --no-http-replay", id="a-second-flag"),
        pytest.param("1.5", id="fractional"),
    ],
)
def test_the_eu_job_refuses_a_cap_that_is_not_a_whole_number_before_submitting(
    tmp_path: Path, max_records: str
) -> None:
    run = _run_eu_read_inputs(tmp_path, max_records=max_records)

    assert run.returncode != 0
    assert "max_records" not in run.outputs
    assert "::error::max_records" in run.stdout


@needs_bash
def test_the_eu_job_hands_the_cli_the_resolved_cap(tmp_path: Path) -> None:
    run = _run_eu_read_inputs(tmp_path, max_records="500")
    assert run.returncode == 0, run.stdout

    args = _eu_cli_args(tmp_path, run)

    assert args[args.index("--max-records") + 1] == "500"


@needs_bash
def test_the_eu_batch_deadline_is_what_the_github_job_has_left(tmp_path: Path) -> None:
    """Past GitHub's limit the run is cancelled and the job's verdict never
    read, so the deadline lands ten minutes before it, counted from the job's
    first step."""
    started_at = int(time.time()) - 300
    argv = _run_eu_build_job(tmp_path, JOB_STARTED_AT=str(started_at))
    # Bounded by the step's own run time: a cold `uv run` under a loaded
    # suite can take longer than any fixed slack.
    elapsed_after = int(time.time()) - started_at

    deadline = int(argv[argv.index("--max-run-duration-seconds") + 1])
    limit = _job("regression-test-eu")["timeout-minutes"] * 60
    assert limit - 10 * 60 - elapsed_after <= deadline <= limit - 10 * 60 - 300


@needs_bash
@pytest.mark.parametrize(
    ("staged", "flag"),
    [("true", "--seed-state-staged"), ("false", "--no-seed-state-staged")],
    ids=["staged", "not-staged"],
)
def test_the_eu_job_tells_the_vm_whether_a_seed_was_staged(
    tmp_path: Path, staged: str, flag: str
) -> None:
    """The VM then has to download a staged seed or stop, and skips the
    download when none was staged."""
    build_job = _step("build-job", job_id="regression-test-eu")
    assert (
        build_job["env"]["SEED_STATE_STAGED"]
        == "${{ steps.stage-seed-state.outputs.staged == 'true' }}"
    )

    argv = _run_eu_build_job(tmp_path, SEED_STATE_STAGED=staged)

    assert flag in argv
    assert ("--seed-state-staged" in argv) is (staged == "true")


@needs_bash
@pytest.mark.parametrize(
    ("connection_id", "state_json", "error"),
    [
        (CONNECTION_ID, None, SEED_STATE_NEEDS_DISPATCH),
        ("", SEED, SEED_STATE_NEEDS_CONNECTION),
    ],
    ids=["from-a-calling-workflow", "without-a-connection"],
)
def test_an_eu_seed_is_refused_by_the_us_rules_before_staging(
    tmp_path: Path, connection_id: str, state_json: str | None, error: str
) -> None:
    """A calling workflow's inputs are not in the event payload, so the step
    has a flag and no seed; the step fails before anything is uploaded."""
    seed_run = _run_eu_seed_step(
        tmp_path,
        connection_id=connection_id,
        state_json=state_json,
        state_json_given=True,
    )

    assert seed_run.run.returncode != 0
    assert f"::error::{error}" in seed_run.run.stdout.splitlines()
    assert seed_run.gcloud_calls == []
    assert not seed_run.seed_file.exists()


def test_disable_http_replay_reaches_the_workflow() -> None:
    assert _dispatch(disable_http_replay=True)["disable_http_replay"] == "true"


def test_state_json_reaches_the_workflow_verbatim() -> None:
    """The workflow writes the string to disk as-is; re-serializing it here
    would be a second place for the JSON to go wrong."""
    sent = _dispatch(state_json=SEED, connection_id=CONNECTION_ID)

    assert sent["state_json"] == SEED


def test_state_json_is_omitted_by_default() -> None:
    """Omitted rather than sent as "": an empty string is also "no seed", but
    the workflow should not have to know that."""
    assert "state_json" not in _dispatch()


@pytest.mark.parametrize(("state_json", "reason"), REFUSED_SEEDS)
def test_a_malformed_seed_state_is_rejected_before_dispatch(
    state_json: str, reason: str
) -> None:
    """Fail at the tool, not minutes later inside the workflow."""
    message = _refused(state_json=state_json, connection_id=CONNECTION_ID)

    assert message == seed_state_error(state_json)
    assert reason in message


def test_a_seed_without_a_connection_is_rejected_before_dispatch() -> None:
    assert _refused(state_json=SEED) == SEED_STATE_NEEDS_CONNECTION


def _dispatch_failure(exc: Exception) -> str:
    """Run the tool with the dispatch raising `exc`; return the tool's message."""

    def _raise(**_kwargs: Any) -> WorkflowDispatchResult:
        raise exc

    with patch.object(connector_qa, "trigger_workflow_dispatch", _raise), patch.object(
        connector_qa, "resolve_ci_trigger_github_token", lambda: "token"
    ), patch.object(
        connector_qa,
        "query_connection_workspace_details",
        lambda _connection_ids: [{"dataplane_name": "US"}],
    ):
        response = run_regression_tests(
            connector_name="source-pokeapi",
            pr=1,
            repo=ConnectorRepo.AIRBYTE,
            connection_id=CONNECTION_ID,
            state_json=SEED,
            ctx=cast(Context, object()),
        )

    assert response.status is TestRunStatus.FAILED
    assert response.workflow_url is None
    return response.message


def test_a_dispatch_github_refuses_is_reported_not_raised() -> None:
    """A seed past GitHub's 65,535-character input limit comes back as a 422;
    the caller gets the API's words, not a traceback with the seed in it."""
    response = SimpleNamespace(
        status_code=422, json=lambda: {"message": "Inputs exceed 65,535 characters"}
    )

    message = _dispatch_failure(
        requests.HTTPError("422 Client Error", response=response)
    )

    assert message == "Workflow dispatch failed: 422 Inputs exceed 65,535 characters"


def test_a_dispatch_that_never_reaches_github_is_reported_not_raised() -> None:
    message = _dispatch_failure(requests.ConnectionError("connection refused"))

    assert message == "Workflow dispatch failed: connection refused"


def _dispatch_through_github(post: Any, get: Any) -> Any:
    """Run the tool through the real dispatch helper with GitHub's POST and GET
    stubbed; return the tool's response."""
    with patch.object(github_actions.requests, "post", post), patch.object(
        github_actions.requests, "get", get
    ), patch.object(connector_qa, "resolve_ci_trigger_github_token", lambda: "token"):
        return run_regression_tests(
            connector_name="source-pokeapi",
            pr=1,
            repo=ConnectorRepo.AIRBYTE,
            ctx=cast(Context, object()),
        )


def _unreachable(*_args: Any, **_kwargs: Any) -> Any:
    raise requests.ConnectionError("connection reset")


def test_a_run_lookup_that_fails_after_the_dispatch_is_still_queued() -> None:
    """GitHub took the dispatch, so the run is queued: calling it failed would
    invite a retry that queues a second run."""
    accepted = SimpleNamespace(raise_for_status=lambda: None)

    response = _dispatch_through_github(
        post=lambda *_args, **_kwargs: accepted, get=_unreachable
    )

    assert response.status is TestRunStatus.QUEUED
    assert response.workflow_url == (
        f"https://github.com/{connector_qa.REGRESSION_TEST_REPO_OWNER}/"
        f"{connector_qa.REGRESSION_TEST_REPO_NAME}/actions/workflows/"
        f"{connector_qa.REGRESSION_TEST_WORKFLOW_FILE}"
    )
    assert response.github_run_id is None


def test_a_dispatch_github_rejects_through_the_helper_is_still_failed() -> None:
    def _reject() -> None:
        raise requests.HTTPError(
            "422 Client Error",
            response=SimpleNamespace(
                status_code=422, json=lambda: {"message": "Unexpected inputs"}
            ),
        )

    response = _dispatch_through_github(
        post=lambda *_args, **_kwargs: SimpleNamespace(raise_for_status=_reject),
        get=_unreachable,
    )

    assert response.status is TestRunStatus.FAILED
    assert response.message == "Workflow dispatch failed: 422 Unexpected inputs"
    assert response.workflow_url is None


def test_replay_is_left_on_by_default() -> None:
    """Omitted rather than sent as "false": the workflow default is already off."""
    assert "disable_http_replay" not in _dispatch()


def test_every_input_the_tool_sends_is_declared_by_the_workflow() -> None:
    """The two sides are edited independently and only meet at dispatch time.

    A name that exists on one side and not the other is not a test failure
    anywhere else -- it is a rejected dispatch for whoever calls the tool next.
    """
    sent = _dispatch(
        connection_id=CONNECTION_ID,
        skip_compare=True,
        skip_read_action=True,
        override_test_image="airbyte/source-pokeapi:1.0.0",
        override_control_image="airbyte/source-pokeapi:0.9.0",
        selected_streams=["pokemon"],
        enable_debug_logs=True,
        with_state=True,
        disable_http_replay=True,
        max_records=123,
        state_json=SEED,
        output_mode="masked",
        read_timeout_minutes=240,
    )

    assert sent, "the tool sent no inputs, so this asserts nothing"
    assert set(sent) <= _declared_inputs()


def test_max_records_reaches_the_workflow_as_a_string() -> None:
    """Dispatch inputs are strings; the workflow's read-inputs step judges it."""
    assert _dispatch(max_records=500)["max_records"] == "500"


def test_max_records_is_omitted_by_default() -> None:
    assert "max_records" not in _dispatch()


@pytest.mark.parametrize("max_records", [0, -1])
def test_a_cap_below_one_is_rejected_before_dispatch(max_records: int) -> None:
    """A cap of zero would read nothing and pass; it is a mistake, not a run."""
    assert "max_records" in _refused(max_records=max_records)


@pytest.mark.parametrize("mode", ["masked", "raw"])
def test_the_output_mode_reaches_the_workflow_verbatim(mode: str) -> None:
    assert _dispatch(output_mode=mode)["output_mode"] == mode


def test_the_output_mode_is_omitted_by_default() -> None:
    """Omitted rather than sent as "": the CLI applies its own default, masked
    on a connection run and raw otherwise."""
    assert "output_mode" not in _dispatch()


def test_an_unknown_output_mode_is_rejected_before_dispatch() -> None:
    dispatched: list[dict[str, str]] = []

    with patch.object(
        connector_qa,
        "trigger_workflow_dispatch",
        lambda *, inputs, **_kwargs: dispatched.append(inputs),
    ), patch.object(connector_qa, "resolve_ci_trigger_github_token", lambda: "token"):
        response = run_regression_tests(
            connector_name="source-pokeapi",
            pr=1,
            repo=ConnectorRepo.AIRBYTE,
            ctx=cast(Context, object()),
            output_mode="scrambled",  # type: ignore[arg-type]
        )

    assert response.status is TestRunStatus.FAILED
    assert "output_mode" in response.message
    assert not dispatched


def test_a_masked_run_with_debug_logs_is_dispatched_and_says_they_are_off() -> None:
    """Debug logs are off on masked runs for now; the CLI switches them off, so
    the tool passes both inputs through and only says so."""
    sent: dict[str, str] = {}

    def _fake_dispatch(*, inputs: dict[str, str], **_kwargs: Any):
        sent.update(inputs)
        return WorkflowDispatchResult(workflow_url="https://example.com/workflow")

    with patch.object(
        connector_qa, "trigger_workflow_dispatch", _fake_dispatch
    ), patch.object(connector_qa, "resolve_ci_trigger_github_token", lambda: "token"):
        response = run_regression_tests(
            connector_name="source-pokeapi",
            pr=1,
            repo=ConnectorRepo.AIRBYTE,
            ctx=cast(Context, object()),
            output_mode="masked",
            enable_debug_logs=True,
        )

    assert response.status is TestRunStatus.QUEUED
    assert sent["output_mode"] == "masked"
    assert sent["enable_debug_logs"] == "true"
    assert "Debug logs will be off" in response.message


def test_a_connection_run_with_debug_logs_and_no_mode_says_they_are_off() -> None:
    """Unset resolves to masked on a connection run, by the CLI's rule, so the
    caller is told the same as for an explicit `masked`; the mode itself is
    still left for the CLI to resolve."""
    sent: dict[str, str] = {}

    def _fake_dispatch(*, inputs: dict[str, str], **_kwargs: Any):
        sent.update(inputs)
        return WorkflowDispatchResult(workflow_url="https://example.com/workflow")

    with patch.object(
        connector_qa, "trigger_workflow_dispatch", _fake_dispatch
    ), patch.object(
        connector_qa, "resolve_ci_trigger_github_token", lambda: "token"
    ), patch.object(
        connector_qa,
        "query_connection_workspace_details",
        lambda _connection_ids: [{"dataplane_name": "US"}],
    ):
        response = run_regression_tests(
            connector_name="source-pokeapi",
            pr=1,
            repo=ConnectorRepo.AIRBYTE,
            ctx=cast(Context, object()),
            connection_id=CONNECTION_ID,
            enable_debug_logs=True,
        )

    assert response.status is TestRunStatus.QUEUED
    assert "output_mode" not in sent
    assert sent["connection_id"] == CONNECTION_ID
    assert sent["enable_debug_logs"] == "true"
    assert "Debug logs will be off" in response.message


@pytest.mark.parametrize(
    "kwargs",
    [
        pytest.param(
            {"connection_id": CONNECTION_ID, "output_mode": "raw"},
            id="connection-raw",
        ),
        pytest.param({}, id="gsm-unset"),
    ],
)
def test_a_run_that_resolves_to_raw_is_not_told_its_debug_logs_are_off(
    kwargs: dict[str, Any],
) -> None:
    with patch.object(
        connector_qa,
        "trigger_workflow_dispatch",
        lambda **_kwargs: WorkflowDispatchResult(
            workflow_url="https://example.com/workflow"
        ),
    ), patch.object(
        connector_qa, "resolve_ci_trigger_github_token", lambda: "token"
    ), patch.object(
        connector_qa,
        "query_connection_workspace_details",
        lambda _connection_ids: [{"dataplane_name": "US"}],
    ):
        response = run_regression_tests(
            connector_name="source-pokeapi",
            pr=1,
            repo=ConnectorRepo.AIRBYTE,
            ctx=cast(Context, object()),
            enable_debug_logs=True,
            **kwargs,
        )

    assert response.status is TestRunStatus.QUEUED
    assert "Debug logs will be off" not in response.message


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        pytest.param(
            {"output_mode": "masked"}, {"output_mode": "masked"}, id="masked-alone"
        ),
        pytest.param(
            {"enable_debug_logs": True},
            {"enable_debug_logs": "true"},
            id="debug-logs-alone",
        ),
        pytest.param(
            {"output_mode": "raw", "enable_debug_logs": True},
            {"output_mode": "raw", "enable_debug_logs": "true"},
            id="raw-with-debug-logs",
        ),
    ],
)
def test_masked_or_debug_logs_alone_is_dispatched(
    kwargs: dict[str, Any], expected: dict[str, str]
) -> None:
    sent = _dispatch(**kwargs)

    assert {key: sent.get(key) for key in expected} == expected


@pytest.mark.parametrize("read_timeout_minutes", [1, 240, READ_TIMEOUT_MINUTES_MAX])
def test_read_timeout_minutes_reaches_the_workflow_as_a_string(
    read_timeout_minutes: int,
) -> None:
    """Dispatch inputs are strings; the workflow's read-inputs step reads it."""
    sent = _dispatch(read_timeout_minutes=read_timeout_minutes)

    assert sent["read_timeout_minutes"] == str(read_timeout_minutes)


def test_read_timeout_minutes_is_omitted_by_default() -> None:
    """Omitted, so the workflow's own default of 170 minutes applies."""
    assert "read_timeout_minutes" not in _dispatch()


@pytest.mark.parametrize("read_timeout_minutes", [0, -1, READ_TIMEOUT_MINUTES_MAX + 1])
def test_a_read_budget_outside_1_to_the_cap_is_rejected_before_dispatch(
    read_timeout_minutes: int,
) -> None:
    """Past the cap the 6-hour job limit would kill the run before its report."""
    assert "read_timeout_minutes" in _refused(read_timeout_minutes=read_timeout_minutes)


# Every expression the setup step holds, resolved as an ordinary dispatch
# would: a new expression fails `_run_step` until it gets a value here.
_SETUP_EXPRESSIONS = {
    "inputs.connector_name": "source-pokeapi",
    "inputs.connection_id": "",
    "inputs.skip_compare": "false",
    "inputs.override_test_image": "",
    "inputs.override_control_image": "",
    "inputs.selected_streams": "",
    "inputs.enable_debug_logs": "false",
    "inputs.disable_http_replay": "false",
    "inputs.discover_missing_streams": "false",
}

BUILT_IMAGE = "airbyte/source-pokeapi:dev"


def _run_setup_step(
    tmp_path: Path,
    output_mode: str,
    *,
    loaded_image: str = BUILT_IMAGE,
    **inputs: str,
) -> _StepRun:
    """Run the setup step with `output_mode` and the loaded target image as
    the environment carries them, and a runner temp directory for the step to
    make the masking key in. `inputs` overrides the dispatch's inputs."""
    env = _step("setup")["env"]
    assert env["OUTPUT_MODE"] == "${{ inputs.output_mode }}"
    assert env["LOADED_TARGET_IMAGE"] == "${{ steps.load-target-image.outputs.image }}"
    runner_temp = tmp_path / "runner_temp"
    runner_temp.mkdir(exist_ok=True)
    return _run_step(
        "setup",
        tmp_path,
        env={
            "OUTPUT_MODE": output_mode,
            "LOADED_TARGET_IMAGE": loaded_image,
            "RUNNER_TEMP": str(runner_temp),
        },
        expressions={
            **_SETUP_EXPRESSIONS,
            **{f"inputs.{name}": value for name, value in inputs.items()},
        },
    )


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
@pytest.mark.parametrize(
    "output_mode,expected",
    [
        pytest.param("masked", " --output-mode masked", id="masked"),
        pytest.param("raw", " --output-mode raw", id="raw"),
        pytest.param("", "", id="empty-is-the-cli-default"),
    ],
)
def test_the_setup_step_passes_a_known_output_mode_to_every_command(
    tmp_path: Path, output_mode: str, expected: str
) -> None:
    run = _run_setup_step(tmp_path, output_mode)

    assert run.returncode == 0, run.stdout
    common_args = run.outputs["common_args"]
    assert ("--output-mode" in common_args) == bool(expected)
    assert expected in common_args + " " if expected else True


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
@pytest.mark.parametrize(
    "output_mode",
    [
        pytest.param("masked --no-http-replay", id="smuggled-flag"),
        pytest.param("MASKED", id="wrong-case"),
        pytest.param("plain", id="unknown"),
    ],
)
def test_the_setup_step_refuses_an_output_mode_that_is_not_masked_or_raw(
    tmp_path: Path, output_mode: str
) -> None:
    """A workflow_call input is a free string expanded unquoted into every
    command's arguments, so an unknown value fails the run before SPEC."""
    run = _run_setup_step(tmp_path, output_mode)

    assert run.returncode == 1
    assert "::error::output_mode must be masked or raw" in run.stdout
    assert "common_args" not in run.outputs


@needs_bash
@pytest.mark.parametrize("output_mode", ["", "masked", "raw"])
def test_the_setup_step_makes_one_masking_key_under_runner_temp_and_hands_over_its_path(
    tmp_path: Path, output_mode: str
) -> None:
    """One key per run, so the four commands' tokens pair: made in the setup
    step, kept under the runner's temp directory outside the artifacts and
    readable by the runner alone, and passed to every command as a path,
    whatever the mode -- the CLI ignores it on a raw run."""
    run = _run_setup_step(tmp_path, output_mode)

    assert run.returncode == 0, run.stdout
    key_path = Path(run.outputs["mask_key_path"])
    assert key_path == tmp_path / "runner_temp" / "mask_key"
    assert not str(key_path).startswith(run.outputs["artifacts_dir"])
    assert key_path.stat().st_mode & 0o777 == 0o600
    key = key_path.read_text().strip()
    assert re.fullmatch(r"[0-9a-f]{64}", key)
    assert f" --mask-key-path {key_path} " in run.outputs["common_args"] + " "
    assert key not in run.outputs["common_args"]


@needs_bash
def test_the_masking_key_is_masked_before_it_prints_and_never_sits_in_a_step(
    tmp_path: Path,
) -> None:
    """As for the seed: the key is registered with add-mask before anything
    could print it and is printed nowhere else; it reaches the four commands
    only as a path, through the common arguments, and never through a step's
    `env:` or `with:`, which the runner prints in the log header."""
    run = _run_setup_step(tmp_path, "")
    assert run.returncode == 0, run.stdout
    key = Path(run.outputs["mask_key_path"]).read_text().strip()

    mentions = [line for line in run.stdout.splitlines() if key in line]
    assert mentions == [f"::add-mask::{key}"]
    assert key not in json.dumps(run.outputs)

    for step in _job()["steps"]:
        header = json.dumps({"env": step.get("env"), "with": step.get("with")})
        assert "mask_key" not in header, step.get("name")
    commands = [
        step
        for step in _job()["steps"]
        if "connector regression-test " in str(step.get("run", ""))
    ]
    assert [step["id"] for step in commands] == [
        "run-spec",
        "run-check",
        "run-discover",
        "run-read",
    ]
    assert all(
        "${{ steps.setup.outputs.common_args }}" in step["run"] for step in commands
    )


@needs_bash
def test_the_job_removes_the_masking_key_last_whatever_happened(
    tmp_path: Path,
) -> None:
    """The key has no use once READ is over: the last step removes it on
    every outcome, tolerates a key already gone, and does nothing when setup
    never made one, so it cannot fail a run or outlive the job."""
    job = _job()
    remove = _step("remove-mask-key")
    key_path = tmp_path / "runner_temp" / "mask_key"
    key_path.parent.mkdir()
    key_path.write_text("not a real key\n")
    expressions = {"steps.setup.outputs.mask_key_path": str(key_path)}

    present = _run_step("remove-mask-key", tmp_path, env={}, expressions=expressions)
    gone = _run_step("remove-mask-key", tmp_path, env={}, expressions=expressions)
    never_made = _run_step(
        "remove-mask-key",
        tmp_path,
        env={},
        expressions={"steps.setup.outputs.mask_key_path": ""},
    )

    assert job["steps"][-1] == remove
    assert remove["if"] == "always()"
    assert "env" not in remove and "with" not in remove
    assert present.returncode == 0, present.stdout
    assert not key_path.exists()
    assert gone.returncode == 0, gone.stdout
    assert never_made.returncode == 0, never_made.stdout


def _upload_steps() -> list[dict[str, Any]]:
    return [
        step
        for step in _job()["steps"]
        if str(step.get("uses", "")).startswith("actions/upload-artifact@")
    ]


def test_a_clean_pass_deletes_its_artifacts_after_the_summary_and_nothing_else_does() -> (
    None
):
    """The artifacts of a pass hold nothing anyone comes back for, and on a
    raw connection run they hold real records, so they go at the end of the
    job rather than at the end of their retention. Every other outcome keeps
    them, and the condition names each one; a failed delete cannot turn a
    pass red, and the summary says which way it went. Only the masking key's
    removal comes after it."""
    job = _job()
    names = [step.get("name") for step in job["steps"]]
    (delete,) = [
        step for step in job["steps"] if step.get("name") == "Delete artifacts on pass"
    ]
    condition = delete["if"]
    uploads = _upload_steps()

    assert names.index("Delete artifacts on pass") == len(names) - 2
    assert names.index("Write Summary Table to Summary") == len(names) - 3
    assert names[-1] == "Remove the masking key"
    assert condition.startswith("${{ !cancelled() && ")
    assert "steps.final-status.outputs.success == 'true'" in condition
    assert "steps.final-status.outputs.internal_failure != 'true'" in condition
    assert "steps.run-read.outputs.incomplete != 'true'" in condition
    assert delete["continue-on-error"] is True
    assert delete["env"]["GH_TOKEN"] == "${{ github.token }}"
    assert len(uploads) == 5
    assert all(step.get("id") for step in uploads)
    for step in uploads:
        assert (
            f"steps.{step['id']}.outputs.artifact-id" in delete["env"]["ARTIFACT_IDS"]
        )
    # The image artifact too: its id is the build job's output, which the PR's
    # code could write, so it is looked up by the name the workflow set.
    assert delete["env"]["IMAGE_ARTIFACT_NAME"] == (
        "${{ needs.build-target-image.outputs.artifact_name }}"
    )
    assert delete["env"]["RUN_ID"] == "${{ github.run_id }}"
    assert (
        "needs.build-target-image.outputs.artifact"
        not in (delete["env"]["ARTIFACT_IDS"])
    )
    assert "deleted on pass" in delete["run"]
    assert "kept (delete failed, see the job log)" in delete["run"]


def test_every_checkout_in_the_regression_job_keeps_its_token_off_disk() -> None:
    """The job's token can delete artifacts (`actions: write`). The delete
    step takes it from the environment and nothing in the job runs `git`
    after the checkout, so the token has no reason to sit in `.git/config`."""
    job = _job()
    checkouts = [step for step in job["steps"] if _uses(step, "actions/checkout")]

    assert checkouts
    for step in checkouts:
        assert step["with"]["persist-credentials"] is False, step["name"]
    for step in job["steps"]:
        for line in step.get("run", "").splitlines():
            assert not re.search(r"(^|[\s;&|(`])git(\s|$)", line), (
                step.get("name"),
                line,
            )


def test_only_the_job_may_delete_artifacts() -> None:
    """`actions: write` sits on the job, not on the workflow, so nothing else
    in the file gains it; a workflow_call caller grants it itself, or the
    delete step fails and the artifacts are kept."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text())

    assert workflow["permissions"] == {"contents": "read"}
    assert _job()["permissions"] == {"contents": "read", "actions": "write"}


IMAGE_ARTIFACT_NAME = "regression-target-image-123-1"
IMAGE_ARTIFACT_LOOKUP = (
    "api --jq .artifacts[].id repos/airbytehq/airbyte-ops-mcp/actions/runs/123/"
    f"artifacts?name={IMAGE_ARTIFACT_NAME}"
)


def _run_delete_step(
    tmp_path: Path,
    artifact_ids: str,
    *,
    gone: str = "",
    broken: str = "",
    image_artifact_name: str = "",
    image_artifact_ids: str = "",
    lookup_broken: bool = False,
) -> tuple[_StepRun, list[str], str]:
    """Run the delete step with `gh` stubbed; return the run, the calls made and the summary.

    The stub answers a 404 for `gone`, a 500 for `broken` and success otherwise;
    a lookup by name answers `image_artifact_ids`, or a 500 when `lookup_broken`.
    """
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    calls = tmp_path / "gh_calls"
    calls.touch()
    stub = bin_dir / "gh"
    stub.write_text(
        "#!/bin/bash\n"
        'printf "%s\\n" "$*" >> "$GH_CALLS"\n'
        'case "$*" in *"/artifacts?name="*)\n'
        '  if [ "$LOOKUP_BROKEN" = true ]; then echo "gh: Server Error (HTTP 500)" >&2; exit 1; fi\n'
        '  [ -z "$LOOKUP_IDS" ] || printf "%s\\n" $LOOKUP_IDS\n'
        "  exit 0 ;;\n"
        "esac\n"
        'ID="${@: -1}"\n'
        'ID="${ID##*/}"\n'
        'if [ "$ID" = "$GONE_ID" ]; then echo "gh: Not Found (HTTP 404)" >&2; exit 1; fi\n'
        'if [ "$ID" = "$BROKEN_ID" ]; then echo "gh: Server Error (HTTP 500)" >&2; exit 1; fi\n'
    )
    stub.chmod(0o755)
    summary = tmp_path / "summary.md"
    summary.touch()

    run = _run_step(
        "delete-artifacts",
        tmp_path,
        env={
            "ARTIFACT_IDS": artifact_ids,
            "REPOSITORY": "airbytehq/airbyte-ops-mcp",
            "RUN_ID": "123",
            "GH_TOKEN": "token",
            "GH_CALLS": str(calls),
            "GONE_ID": gone,
            "BROKEN_ID": broken,
            "IMAGE_ARTIFACT_NAME": image_artifact_name,
            # Not `IMAGE_ARTIFACT_IDS`: the step assigns that name itself,
            # and an inherited variable stays exported.
            "LOOKUP_IDS": image_artifact_ids,
            "LOOKUP_BROKEN": str(lookup_broken).lower(),
            "GITHUB_STEP_SUMMARY": str(summary),
        },
        path_prefix=(str(bin_dir),),
    )
    return run, calls.read_text().splitlines(), summary.read_text()


@needs_bash
def test_the_delete_step_deletes_each_id_once_skips_blanks_and_tolerates_a_404(
    tmp_path: Path,
) -> None:
    """A skipped upload leaves a blank where its id would be, and an artifact
    already expired answers 404: neither is a failure."""
    run, calls, summary = _run_delete_step(tmp_path, "11  \n 22 \n\n33", gone="22")

    assert run.returncode == 0, run.stdout
    assert calls == [
        f"api -X DELETE repos/airbytehq/airbyte-ops-mcp/actions/artifacts/{artifact}"
        for artifact in ("11", "22", "33")
    ]
    assert "Artifact 22 is already gone" in run.stdout
    assert summary == "- **Artifacts:** deleted on pass\n"


@needs_bash
def test_a_clean_pass_deletes_the_image_artifact_it_looked_up_by_name(
    tmp_path: Path,
) -> None:
    """A skipped build leaves the name empty, and then nothing is looked up."""
    run, calls, summary = _run_delete_step(
        tmp_path, "11", image_artifact_name=IMAGE_ARTIFACT_NAME, image_artifact_ids="44"
    )

    assert run.returncode == 0, run.stdout
    assert calls == [
        IMAGE_ARTIFACT_LOOKUP,
        "api -X DELETE repos/airbytehq/airbyte-ops-mcp/actions/artifacts/11",
        "api -X DELETE repos/airbytehq/airbyte-ops-mcp/actions/artifacts/44",
    ]
    assert summary == "- **Artifacts:** deleted on pass\n"

    skipped_build = tmp_path / "skipped-build"
    skipped_build.mkdir()
    run, calls, _summary = _run_delete_step(skipped_build, "11")
    assert run.returncode == 0, run.stdout
    assert calls == [
        "api -X DELETE repos/airbytehq/airbyte-ops-mcp/actions/artifacts/11"
    ]


@needs_bash
def test_an_image_artifact_the_api_cannot_find_by_name_keeps_the_artifacts_and_says_so(
    tmp_path: Path,
) -> None:
    """The other artifacts still go; the step fails and the summary says kept."""
    run, calls, summary = _run_delete_step(
        tmp_path, "11", image_artifact_name=IMAGE_ARTIFACT_NAME, lookup_broken=True
    )

    assert run.returncode == 1
    assert calls == [
        IMAGE_ARTIFACT_LOOKUP,
        "api -X DELETE repos/airbytehq/airbyte-ops-mcp/actions/artifacts/11",
    ]
    assert f"::warning::Could not look up the artifact {IMAGE_ARTIFACT_NAME}" in (
        run.stdout
    )
    assert summary == "- **Artifacts:** kept (delete failed, see the job log)\n"


@needs_bash
def test_a_delete_the_api_refuses_keeps_the_artifacts_and_says_so(
    tmp_path: Path,
) -> None:
    """The loop goes on past a refusal, the step fails (continue-on-error
    keeps the job green) and the summary says the artifacts were kept."""
    run, calls, summary = _run_delete_step(tmp_path, "11 22", broken="11")

    assert run.returncode == 1
    assert len(calls) == 2
    assert "::warning::Could not delete artifact 11: gh: Server Error (HTTP 500)" in (
        run.stdout
    )
    assert "Deleted artifact 22" in run.stdout
    assert summary == "- **Artifacts:** kept (delete failed, see the job log)\n"


def test_force_eu_runner_is_dispatch_only_and_preserves_call_inputs() -> None:
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text())
    triggers = workflow[True] if True in workflow else workflow["on"]
    dispatch_inputs = triggers["workflow_dispatch"]["inputs"]
    call_inputs = triggers["workflow_call"]["inputs"]
    expected_call_input_names = {
        "connector_name",
        "pr",
        "repo",
        "connection_id",
        "skip_compare",
        "skip_read_action",
        "override_test_image",
        "override_control_image",
        "selected_streams",
        "enable_debug_logs",
        "disable_http_replay",
        "with_state",
        "max_records",
        "state_json",
        "output_mode",
        "read_timeout_minutes",
        "discover_missing_streams",
        "injected_sync_mode",
    }

    assert dispatch_inputs["force_eu_runner"] == {
        "description": (
            "Route a connectionless run (for example, a public-image spec smoke "
            "test) to the EU runner. Refused when connection_id is set."
        ),
        "required": False,
        "type": "boolean",
        "default": False,
    }
    assert set(call_inputs) == expected_call_input_names


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_force_eu_runner_is_refused_with_connection_id(tmp_path: Path) -> None:
    step = _step("validate-force-eu-runner", job_id="resolve-residency")
    assert step["env"]["CONNECTION_ID"] == "${{ inputs.connection_id }}"

    run = _run_step(
        "validate-force-eu-runner",
        tmp_path,
        env={"FORCE_EU_RUNNER": "true", "CONNECTION_ID": CONNECTION_ID},
        job_id="resolve-residency",
    )

    assert run.returncode == 1
    assert (
        "::error::force_eu_runner is only for runs without connection_id; "
        "residency comes from the lookup"
    ) in run.stdout


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_force_eu_runner_with_empty_connection_resolves_to_eu(
    tmp_path: Path,
) -> None:
    jobs = yaml.safe_load(WORKFLOW_PATH.read_text())["jobs"]
    assert jobs["resolve-residency"]["env"]["FORCE_EU_RUNNER"] == (
        "${{ inputs.force_eu_runner == true }}"
    )
    assert _step("residency-default", job_id="resolve-residency")["if"] == (
        "inputs.connection_id == '' && env.FORCE_EU_RUNNER != 'true'"
    )

    run = _run_step(
        "resolve-vars",
        tmp_path,
        env={
            "FORCE_EU_RUNNER": "true",
            "RESIDENCY": "",
            "DATAPLANE_GROUP": "",
            "OUTPUT_MODE": "",
        },
        job_id="resolve-residency",
    )

    assert run.returncode == 0, run.stdout
    assert run.outputs["residency"] == "eu"
    assert run.outputs["dataplane_group"] == "forced"


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_force_eu_runner_keeps_the_raw_output_refusal(tmp_path: Path) -> None:
    run = _run_step(
        "resolve-vars",
        tmp_path,
        env={
            "FORCE_EU_RUNNER": "true",
            "RESIDENCY": "",
            "DATAPLANE_GROUP": "",
            "OUTPUT_MODE": "raw",
        },
        job_id="resolve-residency",
    )

    assert run.returncode == 1
    assert (
        "::error::EU-resident connections always run masked; "
        "output_mode=raw is refused."
    ) in run.stdout


def test_regression_jobs_are_routed_by_residency() -> None:
    """EU runs cannot reach the normal regression-test job."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text())
    jobs = workflow["jobs"]

    assert jobs["regression-test"]["needs"] == [
        "resolve-residency",
        "build-target-image",
    ]
    assert jobs["regression-test"]["if"] == (
        "!cancelled() && needs.resolve-residency.outputs.residency == 'us' && "
        "(needs.build-target-image.result == 'success' || "
        "needs.build-target-image.result == 'skipped')"
    )
    assert jobs["regression-test-eu"]["needs"] == [
        "resolve-residency",
        "build-target-image",
    ]
    assert jobs["regression-test-eu"]["if"] == (
        "!cancelled() && needs.resolve-residency.outputs.residency == 'eu' && "
        "(needs.build-target-image.result == 'success' || "
        "needs.build-target-image.result == 'skipped')"
    )
    assert "dataplane_group" in jobs["resolve-residency"]["outputs"]


def _uses(step: dict[str, Any], action: str) -> bool:
    return str(step.get("uses", "")).startswith(f"{action}@")


def test_the_build_job_holds_no_credentials() -> None:
    """A Java connector's build runs the PR's own Gradle on the runner, so
    the job that builds holds no secret, cannot mint a cloud token, and leaves
    no GitHub token in either checkout's git config."""
    job = _job("build-target-image")
    text = yaml.safe_dump(job)
    checkouts = [step for step in job["steps"] if _uses(step, "actions/checkout")]

    assert job["permissions"] == {"contents": "read"}
    assert "secrets." not in text
    assert "id-token" not in text
    assert "github.token" not in text
    assert "google-github-actions/" not in text
    assert len(checkouts) == 2
    for step in checkouts:
        assert step["with"]["persist-credentials"] is False, step["name"]


def test_the_build_job_saves_and_restores_no_cache() -> None:
    """A cache saved after the build could carry the PR's changes into a job
    that holds credentials, and into every later run on the branch."""
    steps = _job("build-target-image")["steps"]
    (setup_uv,) = [step for step in steps if _uses(step, "astral-sh/setup-uv")]
    (setup_java,) = [step for step in steps if _uses(step, "actions/setup-java")]

    assert setup_uv["with"]["enable-cache"] is False
    assert "cache" not in setup_java["with"]
    for step in steps:
        assert not _uses(step, "actions/cache"), step["name"]
        if step is not setup_uv:
            assert not any("cache" in key for key in step.get("with", {})), step["name"]


def test_no_job_that_holds_credentials_restores_a_cache() -> None:
    """Code the PR's build leaves running can read the build job's runtime
    token from a later step and write a cache entry itself, so turning off the
    build job's own cache is not enough."""
    jobs = yaml.safe_load(WORKFLOW_PATH.read_text())["jobs"]
    keyed = {
        job_id
        for job_id, job in jobs.items()
        if "secrets." in yaml.safe_dump(job)
        or job.get("permissions", {}).get("id-token") == "write"
    }

    assert {"resolve-residency", "regression-test", "regression-test-eu"} <= keyed
    for job_id in keyed:
        for step in jobs[job_id]["steps"]:
            name = (job_id, step.get("name", step.get("uses")))
            assert not _uses(step, "actions/cache"), name
            if _uses(step, "astral-sh/setup-uv"):
                assert step["with"]["enable-cache"] is False, name
            if _uses(step, "actions/setup-java") or _uses(step, "actions/setup-python"):
                assert "cache" not in step.get("with", {}), name


def test_the_build_job_runs_on_every_run_that_brings_no_image() -> None:
    """US and EU runs alike: only a skip-compare run with its own image
    builds nothing; in comparison mode the override is ignored, as before.
    The US setup step and the EU build-job step make the same choice."""
    job = _job("build-target-image")

    assert job["needs"] == ["resolve-residency", "fetch-enterprise-source"]
    assert job["if"] == (
        "!cancelled() && needs.resolve-residency.result == 'success' && "
        "!(inputs.skip_compare == true && inputs.override_test_image != '')"
    )


def test_only_a_job_that_runs_no_pr_code_holds_the_enterprise_token() -> None:
    """The private airbyte-enterprise PR is fetched with an app token in its
    own job, which only checks out and uploads, and the build job downloads
    that source instead of checking it out."""
    fetch = _job("fetch-enterprise-source")
    build = _job("build-target-image")
    (checkout,) = [s for s in fetch["steps"] if _uses(s, "actions/checkout")]
    (download,) = [s for s in build["steps"] if _uses(s, "actions/download-artifact")]
    (connector_checkout,) = [
        s
        for s in build["steps"]
        if _uses(s, "actions/checkout") and "repository" in s["with"]
    ]

    assert fetch["if"].startswith("inputs.repo == 'airbyte-enterprise'")
    assert fetch["permissions"] == {"contents": "read"}
    assert not any("run" in step for step in fetch["steps"])
    assert checkout["with"]["persist-credentials"] is False
    assert checkout["with"]["path"] == "connector-repo"
    assert download["with"]["path"] == "connector-repo"
    assert download["if"] == (
        "steps.resolve-connector-ref.outputs.repo == 'airbyte-enterprise'"
    )
    assert connector_checkout["if"] == (
        "steps.resolve-connector-ref.outputs.repo != 'airbyte-enterprise'"
    )


@needs_bash
@pytest.mark.parametrize(
    ("skip_compare", "override", "loaded_image", "expected"),
    [
        pytest.param("false", "", BUILT_IMAGE, BUILT_IMAGE, id="comparison"),
        pytest.param(
            "false",
            "airbyte/source-pokeapi:1.0.0",
            BUILT_IMAGE,
            BUILT_IMAGE,
            id="comparison-ignores-the-override",
        ),
        pytest.param("true", "", BUILT_IMAGE, BUILT_IMAGE, id="skip-compare"),
        pytest.param(
            "true",
            "airbyte/source-pokeapi:1.0.0",
            "",
            "airbyte/source-pokeapi:1.0.0",
            id="skip-compare-with-override-builds-nothing",
        ),
    ],
)
def test_every_command_gets_a_test_image_so_none_builds_from_source(
    tmp_path: Path, skip_compare: str, override: str, loaded_image: str, expected: str
) -> None:
    """The CLI builds from source only when `--test-image` is missing, so it
    is always passed. `--connector-name` stays for the GSM config and the
    control image lookups."""
    run = _run_setup_step(
        tmp_path,
        "",
        loaded_image=loaded_image,
        skip_compare=skip_compare,
        override_test_image=override,
    )

    assert run.returncode == 0, run.stdout
    args = run.outputs["common_args"].split()
    assert args.count("--test-image") == 1
    assert args[args.index("--test-image") + 1] == expected
    assert args[args.index("--connector-name") + 1] == "source-pokeapi"
    assert "--repo-root" not in args
    assert ("--skip-compare" in args) == (skip_compare == "true")


@needs_bash
def test_the_setup_step_refuses_to_run_without_a_target_image(tmp_path: Path) -> None:
    """Without `--test-image` the CLI would build the PR here, next to the
    credentials."""
    run = _run_setup_step(tmp_path, "", loaded_image="")

    assert run.returncode == 1
    assert "::error::No target image" in run.stdout
    assert "common_args" not in run.outputs


def test_nothing_in_the_regression_job_builds_or_checks_out_the_pr() -> None:
    job = _job()
    text = yaml.safe_dump(job)

    assert not any(_uses(step, "actions/setup-java") for step in job["steps"])
    for step in job["steps"]:
        if _uses(step, "actions/checkout"):
            assert "repository" not in step.get("with", {}), step["name"]
    assert "/head" not in text
    assert "--repo-root" not in text
    assert "build-target-image --" not in text


def test_the_build_job_builds_the_pr_as_the_regression_job_used_to() -> None:
    """The PR's head from the same repository, at the path `--repo-root`
    pointed at, through the CLI's own build, so the image keeps its tag."""
    job = _job("build-target-image")
    resolve = _step("resolve-connector-ref", "build-target-image")
    (checkout,) = [
        step
        for step in job["steps"]
        if _uses(step, "actions/checkout") and "repository" in step["with"]
    ]
    (java,) = [step for step in job["steps"] if _uses(step, "actions/setup-java")]

    assert 'REPO="airbyte"' in resolve["run"]
    assert "resolved_ref=refs/pull/${{ inputs.pr }}/head" in resolve["run"]
    assert checkout["with"]["repository"] == (
        "airbytehq/${{ steps.resolve-connector-ref.outputs.repo }}"
    )
    assert checkout["with"]["ref"] == (
        "${{ steps.resolve-connector-ref.outputs.resolved_ref }}"
    )
    assert checkout["with"]["path"] == "connector-repo"
    assert java["with"]["java-version"] == "21"
    assert _step("build", "build-target-image")["run"] == (
        "uv run airbyte-ops cloud connector build-target-image "
        '--connector-name "$CONNECTOR_NAME" '
        '--repo-root "$GITHUB_WORKSPACE/connector-repo"'
    )


def test_the_image_travels_as_a_one_day_artifact_named_for_the_attempt() -> None:
    build = _job("build-target-image")
    (upload,) = [
        step for step in build["steps"] if _uses(step, "actions/upload-artifact")
    ]
    (save,) = [
        step for step in build["steps"] if step["name"] == "Save the target image"
    ]
    download = _step("download-target-image")
    load = _step("load-target-image")

    assert build["outputs"]["image"] == "${{ steps.build.outputs.image }}"
    assert upload["with"]["name"] == build["outputs"]["artifact_name"]
    assert "${{ github.run_id }}-${{ github.run_attempt }}" in upload["with"]["name"]
    assert upload["with"]["retention-days"] == 1
    assert upload["with"]["path"] == "${{ runner.temp }}/target-image.tar"
    assert '--output "$RUNNER_TEMP/target-image.tar"' in save["run"]
    assert download["with"]["name"] == (
        "${{ needs.build-target-image.outputs.artifact_name }}"
    )
    assert load["env"]["ARCHIVE"] == f"{download['with']['path']}/target-image.tar"
    assert load["env"]["IMAGE"] == "${{ needs.build-target-image.outputs.image }}"
    for step in (download, load):
        assert step["if"] == "needs.build-target-image.result == 'success'"


def _run_load_step(
    tmp_path: Path, image: str, docker_load_output: str
) -> tuple[_StepRun, list[str]]:
    """Run the load step with `docker` stubbed; return the run and the docker calls."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls = tmp_path / "docker_calls"
    docker = bin_dir / "docker"
    docker.write_text(
        '#!/bin/bash\necho "$*" >> "$DOCKER_CALLS"\nprintf "%s\\n" "$DOCKER_LOAD_OUTPUT"\n'
    )
    docker.chmod(0o755)
    run = _run_step(
        "load-target-image",
        tmp_path,
        env={
            "IMAGE": image,
            "ARCHIVE": "/tmp/target-image/target-image.tar",
            "DOCKER_CALLS": str(calls),
            "DOCKER_LOAD_OUTPUT": docker_load_output,
        },
        path_prefix=(str(bin_dir),),
    )
    return run, calls.read_text().splitlines() if calls.exists() else []


@needs_bash
def test_the_load_step_hands_on_the_one_image_the_archive_loaded(
    tmp_path: Path,
) -> None:
    run, calls = _run_load_step(tmp_path, BUILT_IMAGE, f"Loaded image: {BUILT_IMAGE}")

    assert run.returncode == 0, run.stdout
    assert run.outputs == {"image": BUILT_IMAGE}
    assert calls == ["load --input /tmp/target-image/target-image.tar"]


@needs_bash
@pytest.mark.parametrize(
    "docker_load_output",
    [
        pytest.param(
            f"Loaded image: {BUILT_IMAGE}\nLoaded image: airbyte/source-pokeapi:0.3.0",
            id="a-second-tag-could-replace-the-control",
        ),
        pytest.param("Loaded image: airbyte/source-other:dev", id="another-image"),
        pytest.param("Loaded image ID: sha256:abc", id="untagged"),
    ],
)
def test_the_load_step_refuses_an_archive_that_loads_anything_else(
    tmp_path: Path, docker_load_output: str
) -> None:
    run, _calls = _run_load_step(tmp_path, BUILT_IMAGE, docker_load_output)

    assert run.returncode == 1
    assert "::error::The image archive did not load exactly" in run.stdout
    assert "image" not in run.outputs


NOT_AN_IMAGE_REFERENCE = [
    pytest.param("", id="empty"),
    pytest.param("airbyte/source-pokeapi:dev; curl evil", id="command"),
    pytest.param("airbyte/source-pokeapi:$(id)", id="substitution"),
    pytest.param("airbyte/source-pokeapi:dev --privileged", id="extra-flag"),
    pytest.param("--entrypoint=sh:dev", id="leading-dash"),
    pytest.param("airbyte/source-pokeapi", id="no-tag"),
    pytest.param("airbyte/source-pokeapi:dev\nimage=evil:dev", id="newline"),
]


@needs_bash
@pytest.mark.parametrize("image", NOT_AN_IMAGE_REFERENCE)
def test_the_load_step_refuses_a_tag_that_is_not_an_image_reference(
    tmp_path: Path, image: str
) -> None:
    """The build job's outputs are the PR's to write, and the setup step puts
    the tag in ARGS, which every command step expands unquoted."""
    run, calls = _run_load_step(tmp_path, image, f"Loaded image: {image}")

    assert run.returncode == 1
    assert "::error::The build job's image output is not an image reference" in (
        run.stdout
    )
    assert calls == []
    assert "image" not in run.outputs


def test_the_eu_job_stages_the_built_image_and_never_the_pr_source() -> None:
    """The VM gets the image the credential-free job built, so nothing that
    holds the job service account builds or even sees the PR's source."""
    job = _job("regression-test-eu")
    text = yaml.safe_dump(job)
    download = _step("download-target-image", "regression-test-eu")
    stage = _step("stage-target-image", "regression-test-eu")

    assert "/head" not in text
    assert "connector-source" not in text
    assert "connector-repo" not in text
    assert "--repo-root" not in text
    assert "git init" not in text
    for step in job["steps"]:
        if _uses(step, "actions/checkout"):
            assert "repository" not in step.get("with", {}), step["name"]
    assert download["with"]["name"] == (
        "${{ needs.build-target-image.outputs.artifact_name }}"
    )
    assert stage["env"]["ARCHIVE"] == f"{download['with']['path']}/target-image.tar"
    assert stage["env"]["IMAGE"] == "${{ needs.build-target-image.outputs.image }}"
    assert stage["env"]["RUN_PREFIX"] == "${{ steps.paths.outputs.prefix }}"
    for step in (download, stage):
        assert step["if"] == "needs.build-target-image.result == 'success'"
    names = [step["name"] for step in job["steps"]]
    assert (
        names.index("Resolve EU run paths")
        < names.index("Stage the target image")
        < names.index("Build Batch job specification")
    )
    build_job = _step("build-job", "regression-test-eu")
    assert build_job["env"]["TARGET_IMAGE"] == (
        "${{ steps.stage-target-image.outputs.image }}"
    )


def _image_reference_rule(step: dict[str, Any]) -> str:
    (rule,) = [line for line in step["run"].splitlines() if "=~" in line]
    return rule.strip()


def test_the_eu_job_checks_the_tag_by_the_us_load_steps_rule() -> None:
    assert _image_reference_rule(
        _step("stage-target-image", "regression-test-eu")
    ) == _image_reference_rule(_step("load-target-image"))


def _run_eu_stage_step(tmp_path: Path, image: str) -> tuple[_StepRun, list[str]]:
    """Run the EU staging step with `gcloud` stubbed; return the run and its calls."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls = tmp_path / "gcloud_calls"
    gcloud = bin_dir / "gcloud"
    gcloud.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "$GCLOUD_CALLS"\n')
    gcloud.chmod(0o755)
    run = _run_step(
        "stage-target-image",
        tmp_path,
        env={
            "IMAGE": image,
            "ARCHIVE": "/tmp/target-image/target-image.tar",
            "RUN_PREFIX": EU_RUN_PREFIX,
            "GCLOUD_CALLS": str(calls),
        },
        path_prefix=(str(bin_dir),),
        job_id="regression-test-eu",
    )
    return run, calls.read_text().splitlines() if calls.exists() else []


@needs_bash
def test_the_eu_job_stages_the_archive_in_the_run_prefix(tmp_path: Path) -> None:
    run, calls = _run_eu_stage_step(tmp_path, BUILT_IMAGE)

    assert run.returncode == 0, run.stdout
    assert calls == [
        f"storage cp /tmp/target-image/target-image.tar {EU_RUN_PREFIX}/target-image.tar"
    ]
    assert run.outputs == {"image": BUILT_IMAGE}


@needs_bash
@pytest.mark.parametrize("image", NOT_AN_IMAGE_REFERENCE)
def test_the_eu_job_refuses_a_tag_that_is_not_an_image_reference(
    tmp_path: Path, image: str
) -> None:
    """The tag goes into the Batch job's arguments and the VM's environment."""
    run, calls = _run_eu_stage_step(tmp_path, image)

    assert run.returncode == 1
    assert "::error::The build job's image output is not an image reference" in (
        run.stdout
    )
    assert calls == []
    assert "image" not in run.outputs


@needs_bash
@pytest.mark.parametrize(
    ("skip_compare", "override", "target_image", "expected"),
    [
        pytest.param("false", "", BUILT_IMAGE, BUILT_IMAGE, id="comparison"),
        pytest.param(
            "false",
            "airbyte/source-pokeapi:1.0.0",
            BUILT_IMAGE,
            BUILT_IMAGE,
            id="comparison-ignores-the-override",
        ),
        pytest.param("true", "", BUILT_IMAGE, BUILT_IMAGE, id="skip-compare"),
        pytest.param(
            "true",
            "airbyte/source-pokeapi:1.0.0",
            "",
            "airbyte/source-pokeapi:1.0.0",
            id="skip-compare-with-override-builds-nothing",
        ),
    ],
)
def test_the_eu_job_always_hands_the_vm_a_test_image_so_none_builds_there(
    tmp_path: Path, skip_compare: str, override: str, target_image: str, expected: str
) -> None:
    """Without `--test-image` the CLI would build the PR on the VM, next to the
    job service account. The VM loads the staged image by the name it is told."""
    argv = _run_eu_build_job(
        tmp_path,
        SKIP_COMPARE=skip_compare,
        OVERRIDE_TEST_IMAGE=override,
        TARGET_IMAGE=target_image,
    )
    args = json.loads(argv[argv.index("--cli-args-json") + 1])

    assert args.count("--test-image") == 1
    assert args[args.index("--test-image") + 1] == expected
    assert args[args.index("--connector-name") + 1] == "source-pokeapi"
    assert "--repo-root" not in args
    assert ("--skip-compare" in args) == (skip_compare == "true")
    assert argv[argv.index("--target-image") + 1] == target_image


@needs_bash
def test_the_eu_job_refuses_to_submit_without_a_target_image(tmp_path: Path) -> None:
    argv_file = tmp_path / "build-job-spec-argv"
    run = _run_step(
        "build-job",
        tmp_path,
        env={
            "CONNECTOR": "source-pokeapi",
            "SKIP_COMPARE": "false",
            "TARGET_IMAGE": "",
            "ARGV_FILE": str(argv_file),
        },
        job_id="regression-test-eu",
    )

    assert run.returncode == 1
    assert "::error::No target image" in run.stdout
    assert not argv_file.exists()


def _run_final_status(tmp_path: Path, **expressions: str) -> _StepRun:
    """Run the final-status step on a run where every command passed, with
    `expressions` overriding that."""
    passed = {
        "inputs.skip_read_action": "false",
        "needs.build-target-image.result": "success",
        "steps.load-target-image.outcome": "success",
        **{
            f"steps.run-{command}.outcome": "success"
            for command in ("spec", "check", "discover", "read")
        },
        **{
            f"steps.run-{command}.outputs.success": "true"
            for command in ("spec", "check", "discover", "read")
        },
    }
    script = _step("final-status")["run"]
    resolved = dict.fromkeys(_EXPRESSION.findall(script), "")
    return _run_step(
        "final-status",
        tmp_path,
        env={},
        expressions={**resolved, **passed, **expressions},
    )


@needs_bash
@pytest.mark.parametrize(
    ("build", "load"),
    [
        pytest.param("success", "success", id="built-and-loaded"),
        pytest.param("skipped", "skipped", id="override-image"),
    ],
)
def test_a_run_with_its_target_image_is_judged_on_its_commands(
    tmp_path: Path, build: str, load: str
) -> None:
    run = _run_final_status(
        tmp_path,
        **{
            "needs.build-target-image.result": build,
            "steps.load-target-image.outcome": load,
        },
    )

    assert run.returncode == 0, run.stdout
    assert run.outputs["internal_failure"] == "false"
    assert run.outputs["success"] == "true"


@needs_bash
@pytest.mark.parametrize("load", ["failure", "skipped"])
def test_a_built_image_that_never_loaded_is_an_internal_failure(
    tmp_path: Path, load: str
) -> None:
    """No command ran, so the run has no verdict; `skipped` is a download
    that failed before the load step."""
    run = _run_final_status(
        tmp_path,
        **{
            "steps.load-target-image.outcome": load,
            **{
                f"steps.run-{command}.outcome": "skipped"
                for command in ("spec", "check", "discover", "read")
            },
            **{
                f"steps.run-{command}.outputs.success": ""
                for command in ("spec", "check", "discover", "read")
            },
        },
    )

    assert run.returncode == 1
    assert "::error::The image from build-target-image was not loaded" in run.stdout
    assert run.outputs["internal_failure"] == "true"


def test_internal_failure_defaults_to_true_when_jobs_are_skipped() -> None:
    """A failed residency resolver remains classified as an internal failure."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text())
    triggers = workflow[True] if True in workflow else workflow["on"]

    assert triggers["workflow_call"]["outputs"]["internal_failure"]["value"] == (
        "${{ jobs.regression-test.outputs.internal_failure || "
        "jobs.regression-test-eu.outputs.internal_failure || 'true' }}"
    )


def test_every_workflow_output_has_an_eu_job_fallback() -> None:
    """An EU run hands a `workflow_call` caller a defined value for every output.

    The US job is skipped on an EU run, so an output that reads only from it
    resolves to an empty string. Each output must fall back to the EU job, and
    the EU job must define it.
    """
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text())
    triggers = workflow[True] if True in workflow else workflow["on"]
    call_outputs = triggers["workflow_call"]["outputs"]
    eu_outputs = workflow["jobs"]["regression-test-eu"]["outputs"]

    assert call_outputs, "the workflow declares no outputs, so this asserts nothing"
    for name, output in call_outputs.items():
        assert f"jobs.regression-test.outputs.{name}" in output["value"], name
        assert f"jobs.regression-test-eu.outputs.{name}" in output["value"], name
        assert name in eu_outputs, name
        assert str(eu_outputs[name]).strip(), name


def _workflow_call_outputs() -> dict[str, Any]:
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text())
    triggers = workflow[True] if True in workflow else workflow["on"]
    return triggers["workflow_call"]["outputs"]


def _summary_step() -> dict[str, Any]:
    (step,) = [
        step
        for step in _job()["steps"]
        if step.get("name") == "Write Summary Table to Summary"
    ]
    return step


def test_not_exercised_travels_beside_incomplete_at_every_level() -> None:
    """The READ step's CLI output, the final-status step, the job's outputs
    and the workflow_call outputs each carry the flag, the way `incomplete`
    does, so a caller can tell an unexercised read from a failed verdict."""
    outputs = _workflow_call_outputs()
    script = _step("final-status")["run"]

    for flag in ("incomplete", "not_exercised"):
        assert outputs[flag]["value"] == (
            f"${{{{ jobs.regression-test.outputs.{flag} || "
            f"jobs.regression-test-eu.outputs.{flag} }}}}"
        )
        assert "never a pass" in outputs[flag]["description"]
        assert (
            _job()["outputs"][flag] == f"${{{{ steps.final-status.outputs.{flag} }}}}"
        )
        assert f'if [ "${{{{ steps.run-read.outputs.{flag} }}}}" = "true" ]' in script
        assert f'echo "{flag}=true" >> "$GITHUB_OUTPUT"' in script
        assert f'echo "{flag}=false" >> "$GITHUB_OUTPUT"' in script


@pytest.mark.parametrize(
    "discover_missing_streams,injected_sync_mode,expected",
    [
        ("false", "", []),
        ("true", "", ["--discover-missing-streams"]),
        ("false", "incremental", ["--injected-sync-mode", "incremental"]),
        (
            "true",
            "full_refresh",
            [
                "--discover-missing-streams",
                "--injected-sync-mode",
                "full_refresh",
            ],
        ),
    ],
)
@needs_bash
def test_eu_build_job_passes_new_stream_inputs_to_batch(
    tmp_path: Path,
    discover_missing_streams: str,
    injected_sync_mode: str,
    expected: list[str],
) -> None:
    step = _step("build-job", "regression-test-eu")
    assert (
        step["env"]["DISCOVER_MISSING_STREAMS"]
        == "${{ inputs.discover_missing_streams }}"
    )
    assert step["env"]["INJECTED_SYNC_MODE"] == "${{ inputs.injected_sync_mode }}"
    assert "${{ inputs." not in step["run"]

    argv = _run_eu_build_job(
        tmp_path,
        DISCOVER_MISSING_STREAMS=discover_missing_streams,
        INJECTED_SYNC_MODE=injected_sync_mode,
    )

    cli_args = json.loads(argv[argv.index("--cli-args-json") + 1])
    for argument in (
        "--discover-missing-streams",
        "--injected-sync-mode",
        "incremental",
        "full_refresh",
    ):
        assert (argument in cli_args) == (argument in expected)
    assert [arg for arg in cli_args if arg in expected] == expected


@needs_bash
def test_eu_build_job_rejects_unknown_injected_sync_mode(tmp_path: Path) -> None:
    run = _run_step(
        "validate-inputs",
        tmp_path,
        job_id="regression-test-eu",
        env={
            "DISCOVER_MISSING_STREAMS": "false",
            "SELECTED_STREAMS": "",
            "INJECTED_SYNC_MODE": "append",
        },
    )

    assert run.returncode == 1
    assert (
        "::error::injected_sync_mode must be full_refresh or incremental, got 'append'"
        in run.stdout
    )


@needs_bash
@pytest.mark.parametrize("selected_streams", ["", ", , "])
def test_eu_input_validation_rejects_discover_missing_streams_without_selection(
    tmp_path: Path, selected_streams: str
) -> None:
    run = _run_step(
        "validate-inputs",
        tmp_path,
        job_id="regression-test-eu",
        env={
            "DISCOVER_MISSING_STREAMS": "true",
            "SELECTED_STREAMS": selected_streams,
            "INJECTED_SYNC_MODE": "",
        },
    )

    assert run.returncode == 1
    assert (
        "::error::selected_streams is required when discover_missing_streams is true"
        in run.stdout
    )


def test_eu_input_validation_precedes_any_source_upload() -> None:
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text())
    steps = workflow["jobs"]["regression-test-eu"]["steps"]
    validation_index = next(
        index for index, step in enumerate(steps) if step.get("id") == "validate-inputs"
    )
    first_upload_index = next(
        index
        for index, step in enumerate(steps)
        if step.get("name") == "Archive and upload operations source"
    )
    validation = steps[validation_index]

    assert validation_index < first_upload_index
    assert validation["env"]["DISCOVER_MISSING_STREAMS"] == (
        "${{ inputs.discover_missing_streams }}"
    )
    assert validation["env"]["SELECTED_STREAMS"] == "${{ inputs.selected_streams }}"
    assert validation["env"]["INJECTED_SYNC_MODE"] == "${{ inputs.injected_sync_mode }}"
    assert (
        "selected_streams is required when discover_missing_streams is true"
        in (validation["run"])
    )
    assert "injected_sync_mode must be full_refresh or incremental" in validation["run"]


def test_eu_finalize_and_workflow_call_publish_not_exercised() -> None:
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text())
    triggers = workflow[True] if True in workflow else workflow["on"]
    call_output = triggers["workflow_call"]["outputs"]["not_exercised"]["value"]
    eu_job = workflow["jobs"]["regression-test-eu"]
    finalize = next(step for step in eu_job["steps"] if step.get("id") == "finalize")

    assert "printf 'not_exercised=%s\\n' \"$not_exercised\"" in finalize["run"]
    assert "not_exercised=false" in finalize["run"]
    assert eu_job["outputs"]["not_exercised"] == (
        "${{ steps.finalize.outputs.not_exercised }}"
    )
    assert call_output == (
        "${{ jobs.regression-test.outputs.not_exercised || "
        "jobs.regression-test-eu.outputs.not_exercised }}"
    )


def test_eu_stream_injection_output_is_always_empty() -> None:
    """The EU job defines `stream_injection` only to satisfy the fallback contract.

    The JSON names streams, so it stays in the EU bucket: the finalize step
    must never set the output to anything but an empty string.
    """
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text())
    triggers = workflow[True] if True in workflow else workflow["on"]
    eu_job = workflow["jobs"]["regression-test-eu"]
    finalize = next(step for step in eu_job["steps"] if step.get("id") == "finalize")
    call_output = triggers["workflow_call"]["outputs"]["stream_injection"]
    assignments = re.findall(r"^\s*stream_injection=.*$", finalize["run"], re.MULTILINE)

    assert [line.strip() for line in assignments] == ['stream_injection=""']
    assert "stream_injection.json" not in finalize["run"]
    assert eu_job["outputs"]["stream_injection"] == (
        "${{ steps.finalize.outputs.stream_injection }}"
    )
    assert call_output["description"].endswith(
        "Always empty on the EU path: stream names never leave the EU."
    )


def test_the_read_cell_is_fed_the_not_exercised_output_and_the_legend_explains_it() -> (
    None
):
    script = _summary_step()["run"]

    assert (
        'READ_CELL="$(result_cell "${{ steps.run-read.outputs.both_failed }}" '
        '"${{ steps.run-read.outputs.success }}" '
        '"${{ steps.run-read.outputs.incomplete }}" '
        '"${{ steps.run-read.outputs.regression_detected }}" '
        '"${{ steps.run-read.outputs.not_exercised }}" '
        '"${{ steps.run-read.outputs.setup_error }}" '
        '"${{ steps.run-read.outputs.could_not_test }}")"'
    ) in script
    assert (
        "❌ (not exercised) = a target-only stream returned no records; the PR's "
        "new code path was never proven"
    ) in script
    assert "❌ (stopped early — regression detected)" in script


def test_setup_and_config_error_verdicts_are_workflow_outputs_and_summary_cells():
    job = _job()
    workflow_call_outputs = _workflow_call_outputs()
    determine = _step("final-status")["run"]
    summary = _summary_step()["run"]

    for flag in ("setup_error", "could_not_test"):
        assert job["outputs"][flag] == f"${{{{ steps.final-status.outputs.{flag} }}}}"
        assert workflow_call_outputs[flag]["value"] == (
            f"${{{{ jobs.regression-test.outputs.{flag} || "
            f"jobs.regression-test-eu.outputs.{flag} }}}}"
        )
        assert f'echo "{flag}=true" | tee -a "$GITHUB_OUTPUT"' in determine
        assert f'echo "{flag}=false" | tee -a "$GITHUB_OUTPUT"' in determine

    assert "::error::SETUP ERROR" in determine
    assert "::error::COULD NOT TEST (config error)" in determine
    assert "❌ (setup error)" in summary
    assert "❌ (could not test — config error)" in summary
    assert "READ context: SETUP ERROR" in summary
    assert "READ context: COULD NOT TEST" in summary


def _run_setup_step_with_injection(
    tmp_path: Path,
    injected_sync_mode: str,
    *,
    discover_missing_streams: str = "true",
    selected_streams: str = "users,feedback",
) -> _StepRun:
    """Run the setup step with stream injection on, `injected_sync_mode` from
    the environment, and a runner temp directory for the masking key."""
    assert (
        _step("setup")["env"]["INJECTED_SYNC_MODE"]
        == "${{ inputs.injected_sync_mode }}"
    )
    runner_temp = tmp_path / "runner_temp"
    runner_temp.mkdir(exist_ok=True)
    return _run_step(
        "setup",
        tmp_path,
        env={
            "OUTPUT_MODE": "",
            "INJECTED_SYNC_MODE": injected_sync_mode,
            "LOADED_TARGET_IMAGE": BUILT_IMAGE,
            "RUNNER_TEMP": str(runner_temp),
        },
        expressions={
            **_SETUP_EXPRESSIONS,
            "inputs.discover_missing_streams": discover_missing_streams,
            "inputs.selected_streams": selected_streams,
        },
    )


@needs_bash
@pytest.mark.parametrize(
    "both_failed,success,incomplete,regression_detected,not_exercised,cell",
    [
        ("false", "true", "false", "false", "false", "✅"),
        ("false", "false", "false", "false", "false", "❌"),
        ("false", "false", "false", "false", "true", "❌ (not exercised)"),
        ("false", "false", "false", "true", "true", "❌ (not exercised)"),
        ("false", "false", "true", "false", "true", "❌ (stopped early — incomplete)"),
        (
            "false",
            "false",
            "true",
            "true",
            "true",
            "❌ (stopped early — regression detected)",
        ),
        (
            "true",
            "false",
            "false",
            "false",
            "true",
            "❌ (both versions failed — inconclusive)",
        ),
    ],
)
def test_the_read_cell_marks_a_not_exercised_read_below_a_stop(
    both_failed: str,
    success: str,
    incomplete: str,
    regression_detected: str,
    not_exercised: str,
    cell: str,
) -> None:
    """Both versions failing and a stop each outrank it, as they do in the
    CLI's verdict; `success` is false whenever it is set, so it never hides
    behind a tick."""
    script = _summary_step()["run"]
    start = script.index("result_cell() {")
    function = script[start : script.index("\n}\n", start) + len("\n}\n")]

    run = subprocess.run(
        [
            "bash",
            "-c",
            f'{function}\nresult_cell "$@"',
            "result_cell",
            both_failed,
            success,
            incomplete,
            regression_detected,
            not_exercised,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    assert run.stdout.strip() == cell


@needs_bash
@pytest.mark.parametrize(
    "injected_sync_mode,expected",
    [
        pytest.param(
            "incremental", " --injected-sync-mode incremental", id="incremental"
        ),
        pytest.param(
            "full_refresh", " --injected-sync-mode full_refresh", id="full-refresh"
        ),
        pytest.param("", "", id="empty-prefers-full-refresh"),
    ],
)
def test_the_setup_step_passes_the_stream_injection_inputs_to_every_command(
    tmp_path: Path, injected_sync_mode: str, expected: str
) -> None:
    run = _run_setup_step_with_injection(tmp_path, injected_sync_mode)

    assert run.returncode == 0, run.stdout
    common_args = run.outputs["common_args"]
    assert " --discover-missing-streams" in common_args
    assert ("--injected-sync-mode" in common_args) == bool(expected)
    assert expected in common_args + " " if expected else True


@needs_bash
@pytest.mark.parametrize(
    "injected_sync_mode",
    [
        pytest.param("incremental --no-http-replay", id="smuggled-flag"),
        pytest.param("INCREMENTAL", id="wrong-case"),
        pytest.param("append", id="unknown"),
    ],
)
def test_the_setup_step_refuses_an_injected_sync_mode_that_is_not_known(
    tmp_path: Path, injected_sync_mode: str
) -> None:
    run = _run_setup_step_with_injection(tmp_path, injected_sync_mode)

    assert run.returncode == 1
    assert (
        "::error::injected_sync_mode must be full_refresh or incremental" in run.stdout
    )
    assert "common_args" not in run.outputs


@needs_bash
@pytest.mark.parametrize(
    "discover_missing_streams,selected_streams,injected_sync_mode,error",
    [
        pytest.param(
            "true",
            "",
            "",
            "::error::discover_missing_streams needs selected_streams",
            id="discover-without-streams",
        ),
        pytest.param(
            "false",
            "users",
            "incremental",
            "::error::injected_sync_mode only applies with discover_missing_streams",
            id="sync-mode-without-discover",
        ),
    ],
)
def test_the_setup_step_refuses_injection_inputs_that_cannot_apply(
    tmp_path: Path,
    discover_missing_streams: str,
    selected_streams: str,
    injected_sync_mode: str,
    error: str,
) -> None:
    """Before the build, which the CLI's own check would only follow."""
    run = _run_setup_step_with_injection(
        tmp_path,
        injected_sync_mode,
        discover_missing_streams=discover_missing_streams,
        selected_streams=selected_streams,
    )

    assert run.returncode == 1
    assert error in run.stdout
    assert "common_args" not in run.outputs
