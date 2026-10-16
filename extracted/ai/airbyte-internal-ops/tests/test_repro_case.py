# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""Tests for SaaS Sandbox reproduction cases.

The sandbox CLI is replaced by a small executable on `PATH` that records how it
was called, so the code under test spawns real processes.
"""

from __future__ import annotations

import copy
import json
import os
import re
import shutil
import stat
import sys
from collections.abc import Sequence
from pathlib import Path

import pytest

from airbyte_ops_mcp.cli import cloud
from airbyte_ops_mcp.regression_tests.models import (
    LEGACY_STATE_KEY,
    Command,
    ComparableOutputs,
)
from airbyte_ops_mcp.regression_tests.repro_case import (
    CASE_RESULT_FILE,
    CREDENTIAL_PLACEHOLDER,
    CaseExpectations,
    CaseOrigin,
    InjectedFailure,
    ReproCase,
    ReproGoal,
    SandboxCli,
    SandboxError,
    SandboxSide,
    SideEvaluation,
    SideOutcome,
    StreamFinding,
    check_twin_gaps,
    classify_findings,
    evaluate_reproduction,
    evaluate_side,
    origin_metadata_problems,
    render_config,
    restore_side,
    set_up_scenario,
)

pytestmark = pytest.mark.unit

CASE_DIR = Path(__file__).parent / "fixtures" / "repro_case" / "minimal"
REPO_ROOT = Path(__file__).parents[1]
# Both the real cases and the reference case the case-run smoke workflow uses.
COMMITTED_CASES = sorted(
    path
    for root in ("regression_cases", "tests/fixtures/regression_cases")
    for path in (REPO_ROOT / root).glob("*/*/expectations.json")
)
EXPECTED_ERROR = "No format in ['%s', '%s'] matching 1698686995.0"
EXPECTED_RECORDS = [("C1", "1700000000.000100"), ("C1", "1700000060.000100")]
EXPECTED_STATE = {"state": {"float_ts": "1700000060"}, "other": 1}

_FAKE_SANDBOX = """\
import json, os, sys
with open(os.environ["FAKE_LOG"], "a") as log:
    log.write(json.dumps({
        "argv": sys.argv[1:],
        "env": {k: os.environ.get(k) for k in (
            "SAAS_API_URL", "SAAS_API_KEY", "SAAS_WORKSPACE_ID", "XDG_STATE_HOME"
        )},
    }) + "\\n")
args = sys.argv[1:]
if args[:2] == ["scenario", "apply"]:
    print(json.dumps({"id": "scn-1", "name": args[2]}))
elif args[:2] == ["scenario", "credentials"]:
    print(json.dumps({"provider": "slack", "api_key": "xoxb-saas-secret"}))
elif args[:2] == ["scenario", "restore"]:
    code = int(os.environ.get("FAKE_RESTORE_EXIT", "0"))
    if code:
        sys.exit(code)
    counter = os.environ["FAKE_LOG"] + ".generation"
    generation = int(open(counter).read()) + 1 if os.path.exists(counter) else 11
    open(counter, "w").write(str(generation))
    print(json.dumps({"ok": True, "generation": generation}))
elif args[:2] == ["scenario", "state"]:
    path = os.environ.get("FAKE_TRACES")
    # By default every side made one plain request to the twin.
    traces = json.load(open(path)) if path else [
        {"generation": g, "method": "GET", "path": "/api/x", "status": 200}
        for g in range(11, 21)
    ]
    print(json.dumps({"channels": [], "traces": traces}))
"""


def _install(bin_dir: Path, name: str, body: str) -> None:
    path = bin_dir / name
    path.write_text(f"#!{sys.executable}\n{body}")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


@pytest.fixture
def fake_sandbox(tmp_path, monkeypatch):
    """A fake `sandbox` on PATH plus the sandbox connection env; returns its calls."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    log = tmp_path / "calls.jsonl"
    log.touch()
    _install(bin_dir, "sandbox", _FAKE_SANDBOX)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("FAKE_LOG", str(log))
    # Keep CLI calls off the real runner's outputs, summary and masking.
    for name in ("GITHUB_ACTIONS", "GITHUB_OUTPUT", "GITHUB_STEP_SUMMARY"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("SAAS_API_URL", "http://127.0.0.1:8088")
    monkeypatch.setenv("SAAS_API_KEY", "local-key")
    monkeypatch.setenv("SAAS_WORKSPACE_ID", "00000000-0000-4000-8000-000000000002")
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))

    def calls() -> list[dict]:
        return [json.loads(line) for line in log.read_text().splitlines()]

    return calls


def _set_traces(tmp_path: Path, monkeypatch, traces: object) -> None:
    path = tmp_path / "traces.json"
    path.write_text(traces if isinstance(traces, str) else json.dumps(traces))
    monkeypatch.setenv("FAKE_TRACES", str(path))


def _trace(generation: int, status: int = 200, unsupported: str | None = None) -> dict:
    trace = {
        "provider": "slack",
        "method": "GET",
        "path": "/api/conversations.replies",
        "status": status,
        "generation": generation,
    }
    if unsupported is not None:
        trace["unsupported"] = unsupported
    return trace


def _message(message_type: str, **payload: object) -> str:
    return json.dumps({"type": message_type, **payload})


def _write_side(
    tmp_path: Path,
    name: str,
    *,
    records: Sequence[tuple[str, str]] = (),
    state: dict | None = None,
    error: str | None = None,
    protocol: bool = True,
    success: bool = True,
    stderr: str = "",
) -> dict:
    lines = []
    if protocol:
        lines.append(_message("LOG", log={"level": "INFO", "message": "hi"}))
    for channel, ts in records:
        lines.append(
            _message(
                "RECORD",
                record={
                    "stream": "threads",
                    "data": {"channel_id": channel, "ts": ts, "text": "x"},
                    "emitted_at": 1,
                },
            )
        )
    if error is not None:
        lines.append(
            _message(
                "TRACE",
                trace={
                    "type": "ERROR",
                    "emitted_at": 1,
                    "error": {
                        "message": "Something went wrong in the connector.",
                        "internal_message": error,
                        "failure_type": "system_error",
                    },
                },
            )
        )
    stdout = tmp_path / f"{name}-stdout.txt"
    stdout.write_text("\n".join(lines))
    stderr_file = tmp_path / f"{name}-stderr.txt"
    stderr_file.write_text(stderr)
    return {
        "success": success,
        "exit_code": 0 if success else 1,
        "stdout_file": str(stdout),
        "stderr_file": str(stderr_file),
        # What `ComparableOutputs.final_states` would hold for this run.
        "_final_states": {(None, "threads"): state} if state is not None else {},
    }


def _evaluate(result: dict, case: ReproCase, side: SandboxSide | None = None):
    return evaluate_side(
        result,
        case,
        sandbox_side=side or SandboxSide(),
        final_states=result["_final_states"],
    )


@pytest.fixture
def case() -> ReproCase:
    return ReproCase.load(CASE_DIR)


# --- Loading -----------------------------------------------------------------


def test_the_case_loads_its_files_and_primary_keys(case):
    assert case.name == "minimal"
    assert case.state_path == CASE_DIR / "state.json"
    assert case.primary_keys == {"threads": [["channel_id"], ["ts"]]}
    assert case.behavior_path == CASE_DIR.resolve() / "sandbox" / "behavior.json"
    assert case.expectations.control_error_contains == EXPECTED_ERROR


@pytest.mark.parametrize(
    "path,content",
    [
        # Expected records must use exactly the primary key fields.
        ("expectations.json", {"records": {"threads": [{"ts": "1"}]}}),
        ("sandbox/behavior.json", ["not", "an", "object"]),
        # A state file selects a warm read, so it must be a usable state.
        ("state.json", "null"),
        ("state.json", "{not json"),
        ("state.json", "1"),
        # The same expected record twice would collapse into one.
        (
            "expectations.json",
            {
                "records": {
                    "threads": [
                        {"channel_id": "C1", "ts": "1"},
                        {"ts": "1", "channel_id": "C1"},
                    ]
                }
            },
        ),
        # A final state for a stream the catalog does not configure.
        (
            "expectations.json",
            {
                "records": {"threads": []},
                "final_state": {"thread": {"float_ts": "1"}},
            },
        ),
        ("catalog.json", {"streams": [{}]}),
        ("expectations.json", None),
        ("sandbox/dataset.json", None),
    ],
)
def test_a_malformed_case_fails_to_load(tmp_path, path, content):
    shutil.copytree(CASE_DIR, tmp_path / "case")
    if content is None:
        (tmp_path / "case" / path).unlink()
    elif isinstance(content, str):
        # Raw file text, for contents that are not valid JSON.
        (tmp_path / "case" / path).write_text(content)
    else:
        (tmp_path / "case" / path).write_text(json.dumps(content))

    with pytest.raises(ValueError):
        ReproCase.load(tmp_path / "case")


@pytest.mark.parametrize("link", ["state.json", "sandbox"])
def test_a_case_with_a_symlink_fails_to_load(tmp_path, link):
    """A case can come from an unreviewed PR, so nothing in it may point outside it."""
    shutil.copytree(CASE_DIR, tmp_path / "case")
    moved = tmp_path / f"elsewhere-{link}"
    (tmp_path / "case" / link).rename(moved)
    (tmp_path / "case" / link).symlink_to(moved)

    with pytest.raises(ValueError, match="symlinks"):
        ReproCase.load(tmp_path / "case")


def test_a_symlinked_case_directory_fails_to_load(tmp_path):
    (tmp_path / "case").symlink_to(CASE_DIR)

    with pytest.raises(ValueError, match="symlinks"):
        ReproCase.load(tmp_path / "case")


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"records": {}},
        {"records": {"threads": "x"}},
        {"records": {"threads": []}, "surprise": 1},
        {"records": {"threads": []}, "control_error_contains": ""},
    ],
)
def test_malformed_expectations_are_rejected(payload):
    with pytest.raises(ValueError):
        CaseExpectations.from_json(payload)


def test_the_case_loads_its_origin(case):
    assert case.origin == CaseOrigin(
        ticket="https://github.com/airbytehq/oncall/issues/13342",
        affected_image="airbyte/source-slack:3.2.19",
        affected_ref="4d07056bddb097a417c5c8895a3885ae25a24628",
        sandbox_ref="7b8a09d7c7a6769a245f577872c21356d5b8ecfd",
    )
    assert case.origin.image_repository == "airbyte/source-slack"
    assert case.origin.image_tag == "3.2.19"


def test_origin_is_optional(tmp_path):
    shutil.copytree(CASE_DIR, tmp_path / "case")
    (tmp_path / "case" / "origin.json").unlink()

    assert ReproCase.load(tmp_path / "case").origin is None


_ORIGIN = {
    "ticket": "https://github.com/airbytehq/oncall/issues/1",
    "affected_image": "airbyte/source-slack:3.2.19",
    "affected_ref": "4d07056bddb097a417c5c8895a3885ae25a24628",
}


@pytest.mark.parametrize(
    "changes",
    [
        {"ticket": "oncall#1"},
        {"affected_image": "airbyte/source-slack"},
        {"affected_image": "airbyte/source-slack@sha256:abc"},
        {"affected_ref": "master"},
        {"affected_ref": "4d07056"},
        {"repo": "airbyte-internal"},
        {"surprise": 1},
        {"sandbox_ref": "7b8a09d"},
        {"sandbox_ref": 7},
    ],
)
def test_malformed_origins_are_rejected(changes):
    with pytest.raises(ValueError):
        CaseOrigin.from_json({**_ORIGIN, **changes})


def test_an_origin_must_name_the_affected_ref():
    with pytest.raises(ValueError, match="affected_ref"):
        CaseOrigin.from_json(
            {key: value for key, value in _ORIGIN.items() if key != "affected_ref"}
        )


def test_the_affected_source_must_be_the_affected_release():
    origin = CaseOrigin.from_json(_ORIGIN)
    metadata = {
        "data": {
            "dockerRepository": "airbyte/source-slack",
            "dockerImageTag": "3.2.19",
        }
    }
    assert origin_metadata_problems(origin, metadata) == []

    metadata["data"]["dockerImageTag"] = "3.2.20"
    (problem,) = origin_metadata_problems(origin, metadata)
    assert "dockerImageTag '3.2.20'" in problem


@pytest.mark.parametrize(
    "expectations", COMMITTED_CASES, ids=lambda path: path.parent.name
)
def test_every_committed_case_loads(expectations):
    """A malformed case should fail here, not when a workflow is dispatched."""
    case = ReproCase.load(expectations.parent)

    assert case.primary_keys
    assert CREDENTIAL_PLACEHOLDER in case.config_template_path.read_text()


def test_render_config_substitutes_the_credential(tmp_path, case):
    path = render_config(case.config_template_path, "xoxb-1", tmp_path / "c.json")

    assert json.loads(path.read_text())["credentials"]["api_token"] == "xoxb-1"

    template = tmp_path / "t.json"
    template.write_text(json.dumps({"api_token": "literal"}))
    with pytest.raises(ValueError, match="SANDBOX_CREDENTIAL"):
        render_config(template, "xoxb-1", tmp_path / "c.json")


# --- Sandbox CLI ---------------------------------------------------------------


def test_sandbox_cli_requires_the_shared_connection_variables(
    fake_sandbox, monkeypatch
):
    monkeypatch.delenv("SAAS_WORKSPACE_ID")

    with pytest.raises(SandboxError, match="SAAS_WORKSPACE_ID"):
        SandboxCli()


@pytest.mark.parametrize("with_behavior", [True, False])
def test_setup_drives_the_sandbox_cli_without_local_mode(
    fake_sandbox, tmp_path, with_behavior
):
    shutil.copytree(CASE_DIR, tmp_path / "case")
    sandbox_dir = (tmp_path / "case" / "sandbox").resolve()
    if not with_behavior:
        (sandbox_dir / "behavior.json").unlink()

    scenario_id, config_path, credential = set_up_scenario(
        ReproCase.load(tmp_path / "case"),
        SandboxCli(),
        scenario_name="minimal-1",
        config_destination=tmp_path / "out" / "config.json",
    )

    assert (scenario_id, credential) == ("scn-1", "xoxb-saas-secret")
    assert json.loads(config_path.read_text())["credentials"]["api_token"] == credential
    calls = fake_sandbox()
    # The failure rules go in with the dataset, so the baseline snapshot holds both.
    behavior = ["--behavior", str(sandbox_dir / "behavior.json")]
    assert [call["argv"] for call in calls] == [
        [
            "scenario",
            "apply",
            "minimal-1",
            "--dataset",
            str(sandbox_dir / "dataset.json"),
            *(behavior if with_behavior else []),
            "--json",
        ],
        ["scenario", "snapshot", "scn-1", "baseline"],
        ["scenario", "credentials", "scn-1", "--json"],
    ]
    for call in calls:
        # `--local` is rejected whenever SAAS_API_URL is set, and a private
        # --state-dir would not see the state `sandbox exec` uses.
        assert "--local" not in call["argv"]
        assert not any(arg.startswith("--state-dir") for arg in call["argv"])
        assert all(call["env"].values())


def test_a_restore_without_a_generation_is_a_restore_failure(tmp_path, fake_sandbox):
    bin_dir = tmp_path / "bin2"
    bin_dir.mkdir()
    _install(bin_dir, "sandbox", "print('{\"ok\": true}')\n")
    environment = {**os.environ, "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}"}

    side = restore_side(SandboxCli(environment=environment), "scn-1")

    assert side.restore_error is not None
    assert side.generation is None


def test_twin_gaps_are_scoped_to_the_sides_generation(
    fake_sandbox, tmp_path, monkeypatch
):
    _set_traces(
        tmp_path,
        monkeypatch,
        [
            _trace(12, 400, "parameter; name=limit"),
            _trace(12, 501),
            _trace(12),
            _trace(11, 400, "operation"),
        ],
    )

    side = check_twin_gaps(SandboxCli(), "scn-1", SandboxSide(generation=12))

    assert side.twin_gaps == (
        "GET /api/conversations.replies: parameter; name=limit",
        "GET /api/conversations.replies: unsupported operation (HTTP 501)",
    )


def test_a_side_beyond_trace_retention_cannot_be_cleared(
    fake_sandbox, tmp_path, monkeypatch
):
    _set_traces(tmp_path, monkeypatch, [_trace(12)] * 1000)

    side = check_twin_gaps(SandboxCli(), "scn-1", SandboxSide(generation=12))

    assert side.twin_gaps == ()
    assert "evicted" in (side.gap_check_error or "")


# --- Verdict -------------------------------------------------------------------


@pytest.mark.parametrize(
    "side_kwargs,sandbox_side,outcome,finding",
    [
        (
            {"records": EXPECTED_RECORDS, "state": EXPECTED_STATE},
            None,
            SideOutcome.SATISFIES,
            None,
        ),
        (
            {"records": EXPECTED_RECORDS[:1], "state": EXPECTED_STATE},
            None,
            SideOutcome.VIOLATES,
            "missing 1 record",
        ),
        (
            {"records": EXPECTED_RECORDS, "state": {"state": {"float_ts": "1"}}},
            None,
            SideOutcome.VIOLATES,
            "final state",
        ),
        # A record emitted twice is the boundary bug class the lane exists for.
        (
            {
                "records": [*EXPECTED_RECORDS, EXPECTED_RECORDS[0]],
                "state": EXPECTED_STATE,
            },
            None,
            SideOutcome.VIOLATES,
            "more than once",
        ),
        ({"error": EXPECTED_ERROR, "success": False}, None, SideOutcome.VIOLATES, None),
        (
            {"error": "ConnectionError", "success": False},
            None,
            SideOutcome.INCONCLUSIVE,
            "ConnectionError",
        ),
        (
            {"success": False, "stderr": "boom\nSegmentation fault"},
            None,
            SideOutcome.INCONCLUSIVE,
            "Segmentation fault",
        ),
        # Harness failures take precedence over whatever the logs contain.
        (
            {"error": EXPECTED_ERROR, "success": False},
            SandboxSide(restore_error="exited 1"),
            SideOutcome.INCONCLUSIVE,
            None,
        ),
        (
            {"records": EXPECTED_RECORDS, "state": EXPECTED_STATE},
            SandboxSide(twin_gaps=("GET /x: parameter; name=y",)),
            SideOutcome.TWIN_GAP,
            "GET /x: parameter; name=y",
        ),
        # No protocol messages means the connector never ran: a launcher failure.
        (
            {"protocol": False, "success": False, "stderr": EXPECTED_ERROR},
            None,
            SideOutcome.INCONCLUSIVE,
            None,
        ),
    ],
)
def test_a_side_is_judged_against_the_case(
    tmp_path, case, side_kwargs, sandbox_side, outcome, finding
):
    evaluation = _evaluate(
        _write_side(tmp_path, "s", **side_kwargs), case, sandbox_side
    )

    assert evaluation.outcome is outcome
    if finding is not None:
        assert any(finding in text for text in evaluation.findings)


def test_a_launcher_json_line_does_not_count_as_connector_output(tmp_path, case):
    result = _write_side(tmp_path, "c", protocol=False)
    Path(result["stdout_file"]).write_text(
        json.dumps({"type": "launcher", "msg": "starting relay"})
    )

    evaluation = _evaluate(result, case)

    assert evaluation.outcome is SideOutcome.INCONCLUSIVE
    assert "no Airbyte protocol output" in evaluation.reason


def test_unhashable_message_fields_are_skipped_not_fatal(tmp_path, case):
    """Connector stdout is arbitrary JSON, so odd shapes must not crash the parse."""
    result = _write_side(tmp_path, "c", protocol=False)
    Path(result["stdout_file"]).write_text(
        "\n".join(
            json.dumps(line)
            for line in (
                {"type": ["RECORD"]},
                {"type": {"x": 1}},
                {"type": "RECORD", "record": {"stream": ["threads"], "data": {}}},
            )
        )
    )

    evaluation = _evaluate(result, case)

    # Only the last line is a protocol message, and it matches no stream, so
    # the side completed without a record: nothing to judge, but no crash.
    assert evaluation.outcome is SideOutcome.INCONCLUSIVE
    assert evaluation.reason.startswith("completed without emitting a record for")


def test_null_message_payloads_are_skipped_not_fatal(tmp_path, case):
    result = _write_side(tmp_path, "t", records=EXPECTED_RECORDS, state=EXPECTED_STATE)
    with open(result["stdout_file"], "a") as stdout:
        stdout.write("\n" + _message("RECORD", record=None))
        stdout.write("\n" + _message("TRACE", trace=None))

    assert _evaluate(result, case).outcome is SideOutcome.SATISFIES


def test_a_global_state_counts_toward_the_final_state(tmp_path, case):
    """Final states come from the shared helper, which unpacks GLOBAL state."""
    result = _write_side(tmp_path, "t", records=EXPECTED_RECORDS)

    evaluation = evaluate_side(
        result,
        case,
        sandbox_side=SandboxSide(),
        final_states={("default", "threads"): EXPECTED_STATE},
    )

    assert evaluation.outcome is SideOutcome.SATISFIES


def test_legacy_state_cannot_satisfy_a_per_stream_final_state(tmp_path, case):
    """Missing every per-stream state on both sides would otherwise pass `reproduced`."""
    result = _write_side(tmp_path, "t", records=EXPECTED_RECORDS)

    evaluation = evaluate_side(
        result,
        case,
        sandbox_side=SandboxSide(),
        final_states={LEGACY_STATE_KEY: {"threads": EXPECTED_STATE}},
    )

    assert evaluation.outcome is SideOutcome.INCONCLUSIVE
    assert "LEGACY" in evaluation.reason


@pytest.mark.parametrize(
    "final_states,outcome",
    [
        # No state for the stream at all is a miss, even when null is expected.
        ({}, SideOutcome.VIOLATES),
        # An emitted null is what the case asks for.
        ({(None, "threads"): None}, SideOutcome.SATISFIES),
    ],
)
def test_an_expected_null_state_needs_the_stream_to_emit_one(
    tmp_path, final_states, outcome
):
    shutil.copytree(CASE_DIR, tmp_path / "case")
    expectations = json.loads((tmp_path / "case" / "expectations.json").read_text())
    expectations["final_state"] = {"threads": None}
    (tmp_path / "case" / "expectations.json").write_text(json.dumps(expectations))
    case = ReproCase.load(tmp_path / "case")
    result = _write_side(tmp_path, "t", records=EXPECTED_RECORDS)

    evaluation = evaluate_side(
        result, case, sandbox_side=SandboxSide(), final_states=final_states
    )

    assert evaluation.outcome is outcome
    if outcome is SideOutcome.VIOLATES:
        assert "threads: emitted no final state" in evaluation.findings


def test_the_generic_trace_message_does_not_match_the_expected_error(tmp_path):
    shutil.copytree(CASE_DIR, tmp_path / "case")
    expectations = json.loads((tmp_path / "case" / "expectations.json").read_text())
    expectations["control_error_contains"] = "Something went wrong"
    (tmp_path / "case" / "expectations.json").write_text(json.dumps(expectations))
    case = ReproCase.load(tmp_path / "case")
    result = _write_side(tmp_path, "c", error="unrelated crash", success=False)

    assert _evaluate(result, case).outcome is SideOutcome.INCONCLUSIVE


@pytest.mark.parametrize(
    "control,target,success,label",
    [
        ("violates", "satisfies", True, "PASS (reproduced and fixed)"),
        ("satisfies", "satisfies", False, "FAIL (not reproduced)"),
        ("violates", "violates", False, "FAIL (not fixed)"),
        ("inconclusive", "satisfies", False, "FAIL (inconclusive)"),
        ("violates", "inconclusive", False, "FAIL (inconclusive)"),
        ("twin_gap", "satisfies", False, "FAIL (twin gap)"),
        # A twin gap tells the caller to switch to a live account, so it wins.
        ("inconclusive", "twin_gap", False, "FAIL (twin gap)"),
    ],
)
def test_the_reproduction_verdict(control, target, success, label):
    verdict = evaluate_reproduction(
        SideEvaluation(SideOutcome(control), control),
        SideEvaluation(SideOutcome(target), target),
    )

    assert (verdict.success, verdict.label) == (success, label)


@pytest.mark.parametrize(
    "control,target,success,label",
    [
        ("violates", "violates", True, "PASS (reproduced)"),
        ("violates", "satisfies", False, "FAIL (not reproduced)"),
        ("satisfies", "violates", False, "FAIL (not reproduced)"),
        ("violates", "inconclusive", False, "FAIL (inconclusive)"),
        ("twin_gap", "violates", False, "FAIL (twin gap)"),
    ],
)
def test_the_reproduced_goal_needs_both_sides_to_violate(
    control, target, success, label
):
    verdict = evaluate_reproduction(
        SideEvaluation(SideOutcome(control), control),
        SideEvaluation(SideOutcome(target), target),
        ReproGoal.REPRODUCED,
    )

    assert (verdict.success, verdict.label) == (success, label)
    assert verdict.regression_detected is False


# --- Empty streams ---------------------------------------------------------------

VACUOUS_STRIPE_DIR = (
    Path(__file__).parent / "fixtures" / "repro_case" / "vacuous-stripe"
)
EMPTY_STREAM_REASON = "completed without emitting a record for"
# What a side that reached the twin looks like after `check_twin_gaps`.
REACHED_TWIN = SandboxSide(generation=1, requests=3)


MINIMAL_EXPECTATIONS = json.loads((CASE_DIR / "expectations.json").read_text())


def _case_with(
    tmp_path: Path, extra_streams: Sequence[str] = (), **changes: object
) -> ReproCase:
    """The minimal case with top-level expectation keys replaced (None removes one).

    `extra_streams` are configured in the catalog, shaped like `threads`.
    """
    directory = tmp_path / "case"
    shutil.copytree(CASE_DIR, directory)
    for name in extra_streams:
        _add_stream(directory, name)
    expectations = json.loads((directory / "expectations.json").read_text())
    for key, value in changes.items():
        if value is None:
            expectations.pop(key, None)
        else:
            expectations[key] = value
    (directory / "expectations.json").write_text(json.dumps(expectations))
    return ReproCase.load(directory)


def _add_stream(case_dir: Path, name: str) -> None:
    """Configure a second stream, shaped like `threads`, in the case's catalog."""
    catalog = json.loads((case_dir / "catalog.json").read_text())
    stream = copy.deepcopy(catalog["streams"][0])
    stream["stream"]["name"] = name
    catalog["streams"].append(stream)
    (case_dir / "catalog.json").write_text(json.dumps(catalog))


def _append_records(result: dict, stream: str, count: int) -> None:
    with open(result["stdout_file"], "a") as stdout:
        for index in range(count):
            stdout.write(
                "\n"
                + _message(
                    "RECORD",
                    record={
                        "stream": stream,
                        "data": {"channel_id": "C9", "ts": f"{index}.0"},
                        "emitted_at": 1,
                    },
                )
            )


def _judge(result: dict, case: ReproCase, final_states: dict) -> SideEvaluation:
    return evaluate_side(
        result, case, sandbox_side=REACHED_TWIN, final_states=final_states
    )


@pytest.mark.parametrize(
    "findings,counts,outcome",
    [
        ((), {}, SideOutcome.SATISFIES),
        (
            (StreamFinding("a", "a: missing 1 record(s)"),),
            {"a": 0},
            SideOutcome.INCONCLUSIVE,
        ),
        # A stream the counts do not know is empty.
        ((StreamFinding("a", "a: missing 1 record(s)"),), {}, SideOutcome.INCONCLUSIVE),
        (
            (
                StreamFinding("b", "b: missing 1 record(s)"),
                StreamFinding("a", "a: missing 1 record(s)"),
            ),
            {"a": 2, "b": 0},
            SideOutcome.VIOLATES,
        ),
        # A finding about no stream in particular always counts.
        ((StreamFinding(None, "something else"),), {}, SideOutcome.VIOLATES),
    ],
)
def test_classify_findings(findings, counts, outcome):
    evaluation = classify_findings(findings, counts)

    assert evaluation.outcome is outcome
    assert evaluation.findings == tuple(finding.message for finding in findings)


def test_the_inconclusive_reason_names_the_empty_streams_in_order():
    evaluation = classify_findings(
        [StreamFinding("b", "b: x"), StreamFinding("a", "a: y")], {}
    )

    assert evaluation.reason == (
        "completed without emitting a record for a, b, so nothing was reproduced there"
    )


@pytest.mark.parametrize(
    "final_states",
    [
        {},
        # An empty read still emits its start cursor; that is not evidence.
        {(None, "threads"): {"state": {"float_ts": "1"}}},
        {(None, "threads"): EXPECTED_STATE},
    ],
)
def test_a_side_that_emitted_no_expected_record_is_inconclusive(
    tmp_path, case, final_states
):
    evaluation = _judge(_write_side(tmp_path, "s"), case, final_states)

    assert evaluation.outcome is SideOutcome.INCONCLUSIVE
    assert evaluation.reason.startswith(f"{EMPTY_STREAM_REASON} threads")
    assert any("threads: missing 2 record(s)" in text for text in evaluation.findings)


def test_records_for_a_stream_the_case_does_not_judge_are_not_evidence(tmp_path, case):
    result = _write_side(tmp_path, "s")
    _append_records(result, "users", 3)

    evaluation = _judge(result, case, {(None, "threads"): EXPECTED_STATE})

    assert evaluation.outcome is SideOutcome.INCONCLUSIVE
    assert evaluation.reason.startswith(EMPTY_STREAM_REASON)


@pytest.mark.parametrize(
    "replies,outcome",
    [
        # `replies` emitted nothing, so its miss cannot be the violation.
        (0, SideOutcome.INCONCLUSIVE),
        (1, SideOutcome.VIOLATES),
    ],
)
def test_an_empty_stream_cannot_supply_a_violation_next_to_a_correct_one(
    tmp_path, replies, outcome
):
    case = _case_with(
        tmp_path,
        extra_streams=("replies",),
        records={
            **MINIMAL_EXPECTATIONS["records"],
            "replies": [{"channel_id": "C1", "ts": "1.0"}],
        },
    )
    result = _write_side(tmp_path, "s", records=EXPECTED_RECORDS)
    # Emitted, but not the expected key: a miss on a stream that read data.
    _append_records(result, "replies", replies)

    evaluation = _judge(result, case, {(None, "threads"): EXPECTED_STATE})

    assert evaluation.outcome is outcome
    assert any("replies: missing 1 record(s)" in text for text in evaluation.findings)
    if outcome is SideOutcome.INCONCLUSIVE:
        assert evaluation.reason.startswith(f"{EMPTY_STREAM_REASON} replies")


@pytest.mark.parametrize(
    "records,state,outcome",
    [
        (0, None, SideOutcome.INCONCLUSIVE),
        (0, {"cursor": "0"}, SideOutcome.INCONCLUSIVE),
        (0, {"cursor": "9"}, SideOutcome.SATISFIES),
        (2, None, SideOutcome.VIOLATES),
        (2, {"cursor": "0"}, SideOutcome.VIOLATES),
        (2, {"cursor": "9"}, SideOutcome.SATISFIES),
    ],
)
def test_a_stream_judged_only_by_its_final_state(tmp_path, records, state, outcome):
    case = _case_with(
        tmp_path,
        extra_streams=("channels",),
        final_state={
            **MINIMAL_EXPECTATIONS["final_state"],
            "channels": {"cursor": "9"},
        },
    )
    result = _write_side(tmp_path, "s", records=EXPECTED_RECORDS)
    _append_records(result, "channels", records)
    final_states = {(None, "threads"): EXPECTED_STATE}
    if state is not None:
        final_states[(None, "channels")] = state

    evaluation = _judge(result, case, final_states)

    assert evaluation.outcome is outcome
    if outcome is SideOutcome.INCONCLUSIVE:
        assert evaluation.reason.startswith(f"{EMPTY_STREAM_REASON} channels")


@pytest.mark.parametrize(
    "final_state,emitted,outcome",
    [
        # Nothing expected and nothing emitted is what such a case asks for.
        (None, None, SideOutcome.SATISFIES),
        (
            {"threads": {"state": {"float_ts": "9"}}},
            {"state": {"float_ts": "9"}},
            SideOutcome.SATISFIES,
        ),
        ({"threads": {"state": {"float_ts": "9"}}}, None, SideOutcome.INCONCLUSIVE),
        (
            {"threads": {"state": {"float_ts": "9"}}},
            {"state": {"float_ts": "1"}},
            SideOutcome.INCONCLUSIVE,
        ),
    ],
)
def test_a_stream_expected_to_emit_no_records(tmp_path, final_state, emitted, outcome):
    case = _case_with(tmp_path, records={"threads": []}, final_state=final_state)
    final_states = {(None, "threads"): emitted} if emitted is not None else {}

    evaluation = _judge(_write_side(tmp_path, "s"), case, final_states)

    assert evaluation.outcome is outcome
    if outcome is SideOutcome.INCONCLUSIVE:
        assert evaluation.reason.startswith(f"{EMPTY_STREAM_REASON} threads")


def test_a_failed_side_with_the_expected_error_still_violates(tmp_path, case):
    """The failed-run branch comes first, so an empty failing side is unaffected."""
    result = _write_side(tmp_path, "c", error=EXPECTED_ERROR, success=False)

    assert _judge(result, case, {}).outcome is SideOutcome.VIOLATES


def _recorded_stripe_side(side: str) -> dict:
    return {
        "success": True,
        "exit_code": 0,
        "stdout_file": str(VACUOUS_STRIPE_DIR / "outputs" / f"{side}-stdout.txt"),
        "stderr_file": "",
    }


@pytest.mark.parametrize("goal", list(ReproGoal))
def test_the_recorded_empty_stripe_run_no_longer_passes(goal):
    """The stripe 6.0.13 control and the affected-ref target both read a dataset
    with no events (source-stripe #84355, 2026-10-13).

    Both sides completed with only a start cursor and missed the one expected
    customer; before this rule `reproduced` passed on that.
    """
    case = ReproCase.load(VACUOUS_STRIPE_DIR / "case")
    # Each side's last recorded STATE: only a start cursor.
    cursors = {"control": "1789356044", "target": "1789356050"}
    control, target = (
        evaluate_side(
            _recorded_stripe_side(side),
            case,
            sandbox_side=REACHED_TWIN,
            final_states={(None, "customers"): {"updated": cursors[side]}},
        )
        for side in ("control", "target")
    )

    for evaluation in (control, target):
        assert evaluation.outcome is SideOutcome.INCONCLUSIVE
        assert evaluation.reason.startswith(f"{EMPTY_STREAM_REASON} customers")
        assert evaluation.findings == (
            "customers: missing 1 record(s) [('\"cus_SAMESECOND0001\"',)]",
        )
    assert evaluate_reproduction(control, target, goal).label == "FAIL (inconclusive)"


# --- Expectations v2 -------------------------------------------------------------

CHECK_ERROR = "no stream slices were found"
QUOTA_ERROR = "Daily YouTube API project quota is exhausted."


def _check_case(tmp_path: Path) -> ReproCase:
    return _case_with(
        tmp_path,
        records=None,
        final_state=None,
        command="check",
        check_status="SUCCEEDED",
        control_error_contains=CHECK_ERROR,
    )


def _failure_case(tmp_path: Path) -> ReproCase:
    return _case_with(
        tmp_path,
        records=None,
        final_state=None,
        target_error_contains=QUOTA_ERROR,
        target_failure_type="transient_error",
    )


def _error_line(
    message: str, internal: str = "boom", failure_type: str = "system_error"
) -> str:
    return _message(
        "TRACE",
        trace={
            "type": "ERROR",
            "emitted_at": 1,
            "error": {
                "message": message,
                "internal_message": internal,
                "failure_type": failure_type,
            },
        },
    )


def _side_with_lines(
    tmp_path: Path, name: str, lines: Sequence[str], **result: object
) -> dict:
    stdout = tmp_path / f"{name}-stdout.txt"
    stdout.write_text(
        "\n".join([_message("LOG", log={"level": "INFO", "message": "hi"}), *lines])
    )
    return {
        "success": True,
        "exit_code": 0,
        "stdout_file": str(stdout),
        "stderr_file": "",
        **result,
    }


def test_a_check_case_loads(tmp_path):
    case = _check_case(tmp_path)

    assert case.expectations.mode == "check"
    assert case.expectations.records == {}


def test_a_failure_case_loads_with_its_injected_failures(tmp_path):
    case = _failure_case(tmp_path)

    assert case.expectations.mode == "failure"
    # The minimal case's behavior.json rate-limits conversations.replies.
    assert case.injected_failures == (
        InjectedFailure(
            status=429,
            provider="slack",
            method="GET",
            path="/api/conversations.replies",
        ),
    )


# The shape `sandbox scenario state` returns: no operation id, no query.
YOUTUBE_REPORTS_TRACE = {
    "provider": "youtube_analytics",
    "method": "GET",
    "path": "/v1/jobs/job-1/reports",
    "status": 429,
    "run_id": "run-1",
    "generation": 1,
    "started_at": "2026-10-14T00:00:00+00:00",
    "duration_ms": 1.5,
}


@pytest.mark.parametrize(
    "failure,trace,answered",
    [
        (
            InjectedFailure(
                429, "slack", method="GET", path="/api/conversations.replies"
            ),
            _trace(1, 429),
            True,
        ),
        # The rule's status from another endpoint is the twin's own answer.
        (
            InjectedFailure(429, "slack", method="GET", path="/api/conversations.list"),
            _trace(1, 429),
            False,
        ),
        (
            InjectedFailure(
                403, "slack", method="GET", path="/api/conversations.replies"
            ),
            _trace(1, 429),
            False,
        ),
        (
            InjectedFailure(
                429, "slack", method="POST", path="/api/conversations.replies"
            ),
            _trace(1, 429),
            False,
        ),
        # A `{param}` path template matches one concrete segment, as the
        # sandbox matches it; traces carry no operation id to match instead.
        (
            InjectedFailure(
                429, "youtube_analytics", method="GET", path="/v1/jobs/{job_id}/reports"
            ),
            YOUTUBE_REPORTS_TRACE,
            True,
        ),
        (
            InjectedFailure(
                429, "youtube_analytics", method="GET", path="/v1/jobs/{job_id}/reports"
            ),
            {**YOUTUBE_REPORTS_TRACE, "path": "/v1/jobs/job-1/reports/report-1"},
            False,
        ),
        (
            InjectedFailure(
                429, "stripe", method="GET", path="/api/conversations.replies"
            ),
            _trace(1, 429),
            False,
        ),
    ],
)
def test_an_injected_failure_answers_only_requests_its_rule_matches(
    failure, trace, answered
):
    assert failure.answered(trace) is answered


@pytest.mark.parametrize(
    "match,message",
    [
        ({"operation": "get.api.conversations.replies"}, "match by method and path"),
        (
            {
                "method": "GET",
                "path": "/api/conversations.replies",
                "query": {"a": "1"},
            },
            "cannot match on query",
        ),
    ],
)
def test_a_failure_rule_traces_cannot_attribute_is_refused(tmp_path, match, message):
    directory = tmp_path / "case"
    shutil.copytree(CASE_DIR, directory)
    rule = {"id": "r", "match": match, "when": {"first": 1}, "status": 429}
    (directory / "sandbox" / "behavior.json").write_text(
        json.dumps({"version": 1, "providers": {"slack": {"failures": [rule]}}})
    )
    (directory / "expectations.json").write_text(
        json.dumps({"target_error_contains": QUOTA_ERROR})
    )

    with pytest.raises(ValueError, match=message):
        ReproCase.load(directory)


def test_a_failure_case_needs_a_failure_rule(tmp_path):
    directory = tmp_path / "case"
    shutil.copytree(CASE_DIR, directory)
    (directory / "sandbox" / "behavior.json").write_text(
        json.dumps({"version": 1, "providers": {"slack": {"failures": []}}})
    )
    (directory / "expectations.json").write_text(
        json.dumps({"target_error_contains": QUOTA_ERROR})
    )

    with pytest.raises(ValueError, match="at least one failure rule"):
        ReproCase.load(directory)


def test_a_new_stream_needs_expected_records(tmp_path):
    with pytest.raises(ValueError, match="needs expected records"):
        _case_with(
            tmp_path, records={"threads": []}, final_state=None, new_streams=["threads"]
        )


@pytest.mark.parametrize(
    "payload,message",
    [
        ({"command": "spec", "records": {"threads": []}}, "`command`"),
        (
            {"command": "check", "control_error_contains": "x"},
            "needs `check_status`",
        ),
        (
            {"command": "check", "check_status": "SUCCEEDED"},
            "`control_error_contains`",
        ),
        (
            {
                "command": "check",
                "check_status": "FAILED",
                "control_error_contains": "x",
            },
            "`check_status`",
        ),
        (
            {
                "command": "check",
                "check_status": "SUCCEEDED",
                "control_error_contains": "x",
                "records": {"threads": []},
            },
            "cannot be combined",
        ),
        ({"check_status": "SUCCEEDED", "records": {"threads": []}}, "needs `command"),
        ({"target_failure_type": "config_error"}, "needs `target_error_contains`"),
        (
            {"target_error_contains": "x", "target_failure_type": "oops"},
            "`target_failure_type`",
        ),
        (
            {"target_error_contains": "x", "records": {"threads": []}},
            "cannot be combined",
        ),
        ({"target_error_contains": ""}, "non-empty"),
        ({"records": {"threads": []}, "allow_duplicate_pks": "threads"}, "list"),
        ({"records": {"threads": []}, "new_streams": ["a", "a"]}, "twice"),
        ({"records": {"threads": []}, "record_fields": {"threads": []}}, "non-empty"),
    ],
)
def test_malformed_v2_expectations_are_rejected(payload, message):
    with pytest.raises(ValueError, match=re.escape(message)):
        CaseExpectations.from_json(payload)


@pytest.mark.parametrize(
    "changes,message",
    [
        ({"allow_duplicate_pks": ["users"]}, "`allow_duplicate_pks` names 'users'"),
        ({"new_streams": ["users"]}, "`new_streams` names 'users'"),
        (
            {
                "record_fields": {
                    "threads": [{"channel_id": "C1", "ts": "1700000000.000100"}]
                }
            },
            "at least one other field",
        ),
        (
            {"record_fields": {"threads": [{"channel_id": "C1", "text": "x"}]}},
            "primary key fields",
        ),
        (
            {
                "record_fields": {
                    "threads": [{"channel_id": "C9", "ts": "1.0", "text": "x"}]
                }
            },
            "does not expect",
        ),
    ],
)
def test_v2_keys_must_fit_the_case(tmp_path, changes, message):
    with pytest.raises(ValueError, match=re.escape(message)):
        _case_with(tmp_path, **changes)


def test_a_failure_case_needs_an_injected_failure(tmp_path):
    directory = tmp_path / "case"
    shutil.copytree(CASE_DIR, directory)
    (directory / "sandbox" / "behavior.json").unlink()
    (directory / "expectations.json").write_text(
        json.dumps({"target_error_contains": QUOTA_ERROR})
    )

    with pytest.raises(ValueError, match=re.escape("needs sandbox/behavior.json")):
        ReproCase.load(directory)


# Records mode -------------------------------------------------------------------


def test_allowed_duplicates_are_not_a_finding(tmp_path):
    case = _case_with(tmp_path, allow_duplicate_pks=["threads"])
    result = _write_side(
        tmp_path,
        "s",
        records=[*EXPECTED_RECORDS, EXPECTED_RECORDS[0]],
        state=EXPECTED_STATE,
    )

    assert (
        _judge(result, case, result["_final_states"]).outcome is SideOutcome.SATISFIES
    )


def _dedup_case(tmp_path: Path, expected: dict, destination: str = "append_dedup"):
    directory = tmp_path / "case"
    shutil.copytree(CASE_DIR, directory)
    catalog = json.loads((directory / "catalog.json").read_text())
    catalog["streams"][0]["destination_sync_mode"] = destination
    (directory / "catalog.json").write_text(json.dumps(catalog))
    expectations = {
        "records": {"threads": [{"channel_id": "C1", "ts": "1.0"}]},
        "allow_duplicate_pks": ["threads"],
        "record_fields": {"threads": [{"channel_id": "C1", "ts": "1.0", **expected}]},
    }
    (directory / "expectations.json").write_text(json.dumps(expectations))
    return ReproCase.load(directory)


def _thread(float_ts: object, text: str) -> str:
    return _message(
        "RECORD",
        record={
            "stream": "threads",
            "data": {
                "channel_id": "C1",
                "ts": "1.0",
                "float_ts": float_ts,
                "text": text,
            },
            "emitted_at": 1,
        },
    )


@pytest.mark.parametrize(
    "records,kept,destination",
    [
        # A cursor tie goes to the record emitted last.
        ([(5, "first"), (5, "last")], "last", "append_dedup"),
        # A higher cursor wins even when emitted first.
        ([(6, "newer"), (5, "older")], "newer", "append_dedup"),
        # A null cursor never beats a value.
        ([(5, "value"), (None, "null")], "value", "append_dedup"),
        ([(None, "null"), (5, "value")], "value", "append_dedup"),
        # A null cursor never beats one that compares with nothing else.
        ([("opaque", "value"), (None, "null")], "value", "append_dedup"),
        # Large integer cursors compare exactly.
        ([(2**53 + 1, "larger"), (2**53, "smaller")], "larger", "append_dedup"),
        # ISO datetimes compare as instants, not as strings.
        (
            [
                ("2026-01-01T00:00:00.500Z", "later"),
                ("2026-01-01T00:00:00Z", "earlier"),
            ],
            "later",
            "append_dedup",
        ),
        # Without deduplication the destination keeps the last record emitted.
        ([(6, "newer"), (5, "older")], "older", "append"),
    ],
)
def test_record_fields_check_the_record_a_destination_keeps(
    tmp_path, records, kept, destination
):
    case = _dedup_case(tmp_path, {"text": kept}, destination)
    result = _side_with_lines(
        tmp_path, "s", [_thread(cursor, text) for cursor, text in records]
    )

    assert _judge(result, case, {}).outcome is SideOutcome.SATISFIES
    other = next(text for _cursor, text in records if text != kept)
    case = _dedup_case(tmp_path / "other", {"text": other}, destination)
    evaluation = _judge(result, case, {})
    assert evaluation.outcome is SideOutcome.VIOLATES
    assert any("the kept record" in text for text in evaluation.findings)


@pytest.mark.parametrize(
    "created_cursor_offset,outcome",
    [
        # source-stripe 6.0.13: both events' records carry the same cursor, so
        # the created event's stale record, emitted last, is the one kept.
        (0, SideOutcome.VIOLATES),
        # 6.0.14 moves the created event's record one second back.
        (-1, SideOutcome.SATISFIES),
    ],
)
def test_the_same_second_stripe_events(tmp_path, created_cursor_offset, outcome):
    directory = tmp_path / "case"
    shutil.copytree(VACUOUS_STRIPE_DIR / "case", directory)
    expectations = json.loads((directory / "expectations.json").read_text())
    expectations["allow_duplicate_pks"] = ["customers"]
    expectations["record_fields"] = {
        "customers": [{"id": "cus_SAMESECOND0001", "metadata": {"tier": "gold"}}]
    }
    (directory / "expectations.json").write_text(json.dumps(expectations))
    case = ReproCase.load(directory)

    def customer(updated: int, metadata: dict) -> str:
        data = {"id": "cus_SAMESECOND0001", "updated": updated, "metadata": metadata}
        return _message("RECORD", record={"stream": "customers", "data": data})

    # The twin lists events newest first: the update, then the creation.
    result = _side_with_lines(
        tmp_path,
        "s",
        [
            customer(1791946971, {"tier": "gold"}),
            customer(1791946971 + created_cursor_offset, {}),
        ],
    )

    assert _judge(result, case, {}).outcome is outcome


def test_a_record_fields_miss_on_an_empty_stream_is_not_evidence(tmp_path):
    case = _dedup_case(tmp_path, {"text": "x"})

    evaluation = _judge(_side_with_lines(tmp_path, "s", []), case, {})

    assert evaluation.outcome is SideOutcome.INCONCLUSIVE
    assert evaluation.reason.startswith(EMPTY_STREAM_REASON)


ZENDESK_CONTROL_STDOUT = _message(
    "LOG",
    log={
        "level": "INFO",
        "message": "MemoryMonitor instantiated with critical threshold: 95%",
    },
)


@pytest.mark.parametrize("requests", [0, 4])
def test_a_side_that_shows_no_sign_of_a_declared_new_stream_violates(
    tmp_path, requests
):
    """source-zendesk-support 5.2.12 emits one LOG line for an unknown stream."""
    case = _case_with(tmp_path, new_streams=["threads"])
    stdout = tmp_path / "control-stdout.txt"
    stdout.write_text(ZENDESK_CONTROL_STDOUT)
    result = {"success": True, "exit_code": 0, "stdout_file": str(stdout)}

    evaluation = evaluate_side(
        result,
        case,
        sandbox_side=SandboxSide(generation=1, requests=requests),
        final_states={},
    )

    assert evaluation.outcome is SideOutcome.VIOLATES
    assert evaluation.findings == ("threads: the release does not define this stream",)


def test_without_the_declaration_the_same_output_is_inconclusive(tmp_path, case):
    stdout = tmp_path / "control-stdout.txt"
    stdout.write_text(ZENDESK_CONTROL_STDOUT)
    result = {"success": True, "exit_code": 0, "stdout_file": str(stdout)}

    evaluation = evaluate_side(
        result,
        case,
        sandbox_side=SandboxSide(generation=1, requests=0),
        final_states={},
    )

    assert evaluation.outcome is SideOutcome.INCONCLUSIVE


def test_an_incomplete_status_alone_is_no_sign_of_a_declared_new_stream(tmp_path):
    """What the CDK emits for a configured stream the source does not define."""
    case = _case_with(tmp_path, new_streams=["threads"])
    result = _side_with_lines(
        tmp_path,
        "s",
        [
            _message(
                "TRACE",
                trace={
                    "type": "STREAM_STATUS",
                    "stream_status": {
                        "stream_descriptor": {"name": "threads"},
                        "status": "INCOMPLETE",
                    },
                },
            )
        ],
    )

    evaluation = _judge(result, case, {})

    assert evaluation.outcome is SideOutcome.VIOLATES


@pytest.mark.parametrize(
    "line",
    [
        _message(
            "TRACE",
            trace={
                "type": "STREAM_STATUS",
                "stream_status": {
                    "stream_descriptor": {"name": "threads"},
                    "status": "STARTED",
                },
            },
        ),
        _message(
            "STATE",
            state={
                "type": "STREAM",
                "stream": {
                    "stream_descriptor": {"name": "threads"},
                    "stream_state": {},
                },
            },
        ),
    ],
)
def test_a_side_that_knows_a_declared_new_stream_is_judged_normally(tmp_path, line):
    case = _case_with(tmp_path, new_streams=["threads"])
    result = _write_side(tmp_path, "t", records=EXPECTED_RECORDS)
    with open(result["stdout_file"], "a") as stdout:
        stdout.write("\n" + line)

    evaluation = _judge(result, case, {(None, "threads"): EXPECTED_STATE})

    assert evaluation.outcome is SideOutcome.SATISFIES


# Failure mode -------------------------------------------------------------------


@pytest.mark.parametrize(
    "result_kwargs,lines,side,outcome",
    [
        # The fix fails fast, with its own message.
        (
            {"success": False, "exit_code": 1},
            [_error_line(QUOTA_ERROR, failure_type="transient_error")],
            SandboxSide(generation=1, requests=1, injected_responses=1),
            SideOutcome.SATISFIES,
        ),
        # The right text with another failure type is not the fix.
        (
            {"success": False, "exit_code": 1},
            [_error_line(QUOTA_ERROR, failure_type="config_error")],
            SandboxSide(generation=1, requests=1, injected_responses=1),
            SideOutcome.INCONCLUSIVE,
        ),
        # The affected release retries through the injected 429 and completes.
        (
            {},
            [],
            SandboxSide(generation=1, requests=3, injected_responses=1),
            SideOutcome.VIOLATES,
        ),
        # Completing without the injected failure says nothing.
        (
            {},
            [],
            SandboxSide(generation=1, requests=3, injected_responses=0),
            SideOutcome.INCONCLUSIVE,
        ),
        # A crash before reaching the twin, such as a DNS failure.
        (
            {"success": False, "exit_code": 1},
            [_error_line(QUOTA_ERROR, failure_type="transient_error")],
            SandboxSide(generation=1, requests=0, injected_responses=0),
            SideOutcome.INCONCLUSIVE,
        ),
        # The control's own expected error still counts, once the twin was reached.
        (
            {"success": False, "exit_code": 1},
            [_error_line("generic", internal=EXPECTED_ERROR)],
            SandboxSide(generation=1, requests=2, injected_responses=1),
            SideOutcome.VIOLATES,
        ),
    ],
)
def test_a_failure_case_side(tmp_path, result_kwargs, lines, side, outcome):
    case = _failure_case(tmp_path)
    result = _side_with_lines(tmp_path, "s", lines, **result_kwargs)

    evaluation = evaluate_side(result, case, sandbox_side=side, final_states={})

    assert evaluation.outcome is outcome


# Check mode ---------------------------------------------------------------------


@pytest.mark.parametrize(
    "status,message,requests,outcome",
    [
        ("SUCCEEDED", "", 2, SideOutcome.SATISFIES),
        (
            "FAILED",
            f"Unable to connect to stream x - {CHECK_ERROR}",
            2,
            SideOutcome.VIOLATES,
        ),
        # Before the token endpoint existed, CHECK failed on DNS on both sides.
        ("FAILED", "NameResolutionError", 2, SideOutcome.INCONCLUSIVE),
        (None, "", 2, SideOutcome.INCONCLUSIVE),
        ("SUCCEEDED", "", 0, SideOutcome.INCONCLUSIVE),
        # A CHECK that reports success but then crashes is not a clean success.
        ("SUCCEEDED-crashed", "", 2, SideOutcome.INCONCLUSIVE),
        ("FAILED", CHECK_ERROR, 0, SideOutcome.INCONCLUSIVE),
    ],
)
def test_a_check_case_side(tmp_path, status, message, requests, outcome):
    case = _check_case(tmp_path)
    crashed = status == "SUCCEEDED-crashed"
    result = _side_with_lines(
        tmp_path,
        "s",
        [],
        connection_status="SUCCEEDED" if crashed else status,
        connection_status_message=message,
        success=not crashed,
        exit_code=1 if crashed else 0,
    )

    evaluation = evaluate_side(
        result,
        case,
        sandbox_side=SandboxSide(generation=1, requests=requests),
        final_states=None,
    )

    assert evaluation.outcome is outcome


def test_the_check_error_can_come_from_an_error_trace(tmp_path):
    case = _check_case(tmp_path)
    result = _side_with_lines(
        tmp_path,
        "s",
        [_error_line("check failed", internal=CHECK_ERROR)],
        connection_status="FAILED",
        connection_status_message="check failed",
    )

    assert _judge(result, case, {}).outcome is SideOutcome.VIOLATES


# Sandbox traces -----------------------------------------------------------------


def test_injected_responses_and_rejected_paths(fake_sandbox, tmp_path, monkeypatch):
    rejected = {**_trace(12, 404, "path"), "path": "/rate_limit"}
    _set_traces(
        tmp_path,
        monkeypatch,
        [_trace(12, 429), _trace(12), rejected, _trace(11, 429)],
    )

    side = check_twin_gaps(
        SandboxCli(),
        "scn-1",
        SandboxSide(generation=12),
        (
            InjectedFailure(
                429, "slack", method="GET", path="/api/conversations.replies"
            ),
            InjectedFailure(404, "slack", method="GET", path="/rate_limit"),
        ),
    )

    # A request the gateway rejected is a twin gap, never an injected failure.
    assert side.twin_gaps == ("GET /rate_limit: path",)
    assert (side.requests, side.injected_responses) == (3, 1)


# --- CLI -------------------------------------------------------------------------

_ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m")


def _logged_payload(captured: str) -> dict:
    plain = _ANSI_ESCAPE.sub("", captured)
    obj, _end = json.JSONDecoder().raw_decode(plain[plain.index("{") :])
    return obj


@pytest.fixture
def case_run(tmp_path, monkeypatch, fake_sandbox):
    """Run `regression-test` in case mode with scripted per-side outputs."""
    gh_outputs: dict[str, object] = {}
    monkeypatch.setattr(cloud, "ensure_image_available", lambda _image: True)
    monkeypatch.setattr(cloud, "track_regression_test", lambda **_kwargs: None)
    monkeypatch.setattr(cloud, "write_github_summary", lambda _content: None)
    monkeypatch.setattr(cloud, "write_github_outputs", gh_outputs.update)
    config = tmp_path / "config.json"
    config.write_text("{}")

    def _run(
        sides: dict[str, dict],
        command: str = "read",
        case_dir: Path = CASE_DIR,
        **options: object,
    ) -> dict[str, object]:
        seen: list[dict] = []

        def _fake_run(*, target_or_control, command, output_dir, **kwargs):
            seen.append({"side": target_or_control.value, "command": command, **kwargs})
            output_dir.mkdir(parents=True, exist_ok=True)
            side = dict(sides[target_or_control.value])
            final_states = side.pop("_final_states", None)
            return (
                {
                    "command": command.value,
                    "message_counts": {},
                    "record_counts_per_stream": {},
                    **side,
                },
                ComparableOutputs(final_states=final_states),
            )

        monkeypatch.setattr(cloud, "_run_connector_command", _fake_run)
        cloud.regression_test(
            test_image="airbyte/source-test:2.0.0",
            control_image="airbyte/source-test:1.0.0",
            command=command,
            config_path=str(config),
            repro_case_dir=str(case_dir),
            sandbox_scenario="scn-1",
            output_dir=str(tmp_path / "out"),
            **options,
        )
        gh_outputs["_seen"] = seen
        return gh_outputs

    return _run


def _reproducing_sides(tmp_path: Path) -> dict[str, dict]:
    return {
        "control": _write_side(
            tmp_path, "control", error=EXPECTED_ERROR, success=False
        ),
        "target": _write_side(
            tmp_path, "target", records=EXPECTED_RECORDS, state=EXPECTED_STATE
        ),
    }


def test_case_mode_passes_when_control_reproduces_and_target_is_fixed(
    tmp_path, capsys, case_run, fake_sandbox
):
    outputs = case_run(_reproducing_sides(tmp_path))

    assert outputs["success"] is True
    assert outputs["both_failed"] is False
    assert outputs["reproduction_verdict"] == "PASS (reproduced and fixed)"
    assert _logged_payload(capsys.readouterr().out)["reproduction"]["success"] is True
    # The baseline is restored before each side, control first, and each side's
    # traces are checked for twin gaps right after it.
    assert [call["argv"] for call in fake_sandbox()] == [
        ["scenario", "restore", "scn-1", "baseline"],
        ["scenario", "state", "scn-1"],
        ["scenario", "restore", "scn-1", "baseline"],
        ["scenario", "state", "scn-1"],
    ]
    seen = outputs["_seen"]
    assert [call["side"] for call in seen] == ["control", "target"]
    assert all(call["command"] is Command.READ_WITH_STATE for call in seen)
    assert all(
        call["catalog_path"] == CASE_DIR.resolve() / "catalog.json" for call in seen
    )
    report = (tmp_path / "out" / "report.md").read_text()
    assert "PASS (reproduced and fixed)" in report
    result = json.loads((tmp_path / "out" / CASE_RESULT_FILE).read_text())
    assert result["verdict"] == "PASS (reproduced and fixed)"
    assert result["passed"] is True
    assert result["goal"] == "fixed"
    assert result["case"]["name"] == "minimal"
    assert result["control"]["image"] == "airbyte/source-test:1.0.0"
    assert result["target"]["image"] == "airbyte/source-test:2.0.0"
    assert result["sides"]["control"]["outcome"] == "violates"
    assert result["sides"]["target"]["outcome"] == "satisfies"
    assert result["twin_gaps"] == []


def test_the_reproduced_goal_passes_when_both_sides_hit_the_bug(tmp_path, case_run):
    outputs = case_run(
        {
            side: _write_side(tmp_path, side, error=EXPECTED_ERROR, success=False)
            for side in ("control", "target")
        },
        repro_goal="reproduced",
    )

    assert outputs["success"] is True
    assert outputs["reproduction_verdict"] == "PASS (reproduced)"
    result = json.loads((tmp_path / "out" / CASE_RESULT_FILE).read_text())
    assert (result["verdict"], result["goal"]) == ("PASS (reproduced)", "reproduced")


def test_case_mode_fails_when_the_control_does_not_reproduce(tmp_path, case_run):
    satisfied = {"records": EXPECTED_RECORDS, "state": EXPECTED_STATE}
    outputs = case_run(
        {
            "control": _write_side(tmp_path, "control", **satisfied),
            "target": _write_side(tmp_path, "target", **satisfied),
        }
    )

    assert outputs["success"] is False
    assert outputs["reproduction_verdict"] == "FAIL (not reproduced)"


def test_a_side_that_never_reached_the_twin_is_inconclusive(
    tmp_path, case_run, monkeypatch
):
    """Two clean exits without a request would otherwise pass `reproduced`."""
    _set_traces(tmp_path, monkeypatch, [])

    outputs = case_run(
        {
            side: _write_side(tmp_path, side, records=[], state=EXPECTED_STATE)
            for side in ("control", "target")
        },
        repro_goal="reproduced",
    )

    assert outputs["success"] is False
    assert outputs["reproduction_verdict"] == "FAIL (inconclusive)"


def test_case_mode_is_inconclusive_when_a_restore_fails(
    tmp_path, case_run, monkeypatch
):
    monkeypatch.setenv("FAKE_RESTORE_EXIT", "1")

    outputs = case_run(_reproducing_sides(tmp_path))

    assert outputs["success"] is False
    assert outputs["reproduction_verdict"] == "FAIL (inconclusive)"


def test_case_mode_reports_a_twin_gap(tmp_path, case_run, monkeypatch):
    # Generation 11 is the control side's restore, 12 the target's.
    _set_traces(tmp_path, monkeypatch, [_trace(12, 400, "parameter; name=limit")])

    outputs = case_run(_reproducing_sides(tmp_path))

    assert outputs["success"] is False
    assert outputs["reproduction_verdict"] == "FAIL (twin gap)"
    assert "FAIL (twin gap)" in (tmp_path / "out" / "report.md").read_text()
    result = json.loads((tmp_path / "out" / CASE_RESULT_FILE).read_text())
    assert result["passed"] is False
    assert result["sides"]["target"]["outcome"] == "twin_gap"
    assert len(result["twin_gaps"]) == 1


@pytest.mark.parametrize(
    "overrides,message",
    [
        ({"sandbox_scenario": None}, "together"),
        (
            {"repro_case_dir": None, "sandbox_scenario": None, "repro_goal": "fixed"},
            "--repro-goal needs them",
        ),
        ({"skip_compare": True, "control_image": None}, "comparison mode"),
        ({"config_path": None}, "--config-path"),
        ({"catalog_path": "x.json"}, "catalog and state"),
        ({"selected_streams": "threads"}, "selects its own streams"),
        # Only a read is judged against the case.
        ({"command": "check"}, "only `--command read`"),
    ],
)
def test_case_mode_rejects_conflicting_options(
    tmp_path, capsys, fake_sandbox, monkeypatch, overrides, message
):
    monkeypatch.setattr(cloud, "write_github_outputs", lambda _outputs: None)
    monkeypatch.setattr(cloud, "write_github_output", lambda *_args: None)
    kwargs = {
        "test_image": "airbyte/source-test:2.0.0",
        "control_image": "airbyte/source-test:1.0.0",
        "command": "read",
        "config_path": str(tmp_path / "config.json"),
        "repro_case_dir": str(CASE_DIR),
        "sandbox_scenario": "scn-1",
        "output_dir": str(tmp_path / "out"),
        **overrides,
    }

    with pytest.raises(SystemExit):
        cloud.regression_test(**kwargs)

    captured = capsys.readouterr()
    assert message in _ANSI_ESCAPE.sub("", captured.out + captured.err)


@pytest.mark.parametrize("on_github_actions", [False, True])
def test_the_setup_command_reports_the_scenario_and_config(
    tmp_path, capsys, fake_sandbox, monkeypatch, on_github_actions
):
    outputs: dict[str, object] = {}
    monkeypatch.setattr(cloud, "write_github_outputs", outputs.update)
    if on_github_actions:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")

    cloud.regression_case_setup(
        case_dir=str(CASE_DIR), config_output=str(tmp_path / "config.json")
    )

    assert outputs == {
        "scenario_id": "scn-1",
        "config_path": str(tmp_path / "config.json"),
        "case_dir": str(CASE_DIR.resolve()),
        "command": "read",
    }
    assert (
        json.loads((tmp_path / "config.json").read_text())["credentials"]["api_token"]
        == "xoxb-saas-secret"
    )
    # The log never shows the credential, except in the mask command itself.
    lines = capsys.readouterr().out.splitlines()
    assert [line for line in lines if "xoxb-saas-secret" in line] == (
        ["::add-mask::xoxb-saas-secret"] if on_github_actions else []
    )


def test_case_mode_is_inconclusive_when_both_sides_emit_nothing(tmp_path, case_run):
    """Both sides reached the twin (one traced request each) but read no data."""
    outputs = case_run(
        {
            side: _write_side(tmp_path, side, state={"state": {"float_ts": "1"}})
            for side in ("control", "target")
        },
        repro_goal="reproduced",
    )

    assert outputs["success"] is False
    assert outputs["reproduction_verdict"] == "FAIL (inconclusive)"
    result = json.loads((tmp_path / "out" / CASE_RESULT_FILE).read_text())
    for side in ("control", "target"):
        assert result["sides"][side]["reason"].startswith(
            f"{EMPTY_STREAM_REASON} threads"
        )


def test_a_check_case_runs_check_and_writes_its_verdict(tmp_path, case_run):
    case = _check_case(tmp_path)
    outputs = case_run(
        {
            "control": _side_with_lines(
                tmp_path,
                "control",
                [],
                connection_status="FAILED",
                connection_status_message=CHECK_ERROR,
            ),
            "target": _side_with_lines(
                tmp_path, "target", [], connection_status="SUCCEEDED"
            ),
        },
        command="check",
        case_dir=case.directory,
    )

    assert outputs["reproduction_verdict"] == "PASS (reproduced and fixed)"
    assert all(run["command"] is Command.CHECK for run in outputs["_seen"])
    # A CHECK reads nothing, so the case's catalog is not passed.
    assert all(run["catalog_path"] is None for run in outputs["_seen"])
    result = json.loads((tmp_path / "out" / CASE_RESULT_FILE).read_text())
    assert result["sides"]["control"]["outcome"] == "violates"


def test_a_check_case_refuses_a_read(tmp_path, capsys, case_run):
    case = _check_case(tmp_path)

    with pytest.raises(SystemExit):
        case_run({}, command="read", case_dir=case.directory)

    captured = _ANSI_ESCAPE.sub("", "".join(capsys.readouterr()))
    assert "This case runs only `--command check`" in captured


def test_the_setup_command_reports_a_check_cases_command(
    tmp_path, fake_sandbox, monkeypatch
):
    outputs: dict[str, object] = {}
    monkeypatch.setattr(cloud, "write_github_outputs", outputs.update)
    case = _check_case(tmp_path)

    cloud.regression_case_setup(
        case_dir=str(case.directory), config_output=str(tmp_path / "config.json")
    )

    assert outputs["command"] == "check"


@pytest.mark.parametrize(
    "result_kwargs,outcome",
    [
        # An annotated run (as printed for #82712) says success false for a
        # FAILED CHECK that exited cleanly; guarded should one reach here.
        (
            {"success": False, "exit_code": 0, "exited_cleanly": True},
            SideOutcome.VIOLATES,
        ),
        ({"success": True, "exit_code": 0}, SideOutcome.VIOLATES),
        # The expected text followed by a crash is not the bug reproducing.
        ({"success": False, "exit_code": 1}, SideOutcome.INCONCLUSIVE),
        (
            {"success": False, "exit_code": 1, "exited_cleanly": False},
            SideOutcome.INCONCLUSIVE,
        ),
    ],
)
def test_a_failed_check_counts_only_after_a_clean_exit(
    tmp_path, result_kwargs, outcome
):
    case = _check_case(tmp_path)
    result = _side_with_lines(
        tmp_path,
        "s",
        [],
        connection_status="FAILED",
        connection_status_message=CHECK_ERROR,
        **result_kwargs,
    )

    evaluation = _judge(result, case, {})

    assert evaluation.outcome is outcome
    if outcome is SideOutcome.INCONCLUSIVE:
        assert evaluation.reason == "CHECK reported FAILED but exited 1"


def test_two_crashing_checks_do_not_reproduce(tmp_path, case_run):
    case = _check_case(tmp_path)
    crashed = {
        "connection_status": "FAILED",
        "connection_status_message": CHECK_ERROR,
        "success": False,
        "exit_code": 1,
    }
    outputs = case_run(
        {
            side: _side_with_lines(tmp_path, side, [], **crashed)
            for side in ("control", "target")
        },
        command="check",
        case_dir=case.directory,
        repro_goal="reproduced",
    )

    assert outputs["reproduction_verdict"] == "FAIL (inconclusive)"
