# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""Tests for SaaS Sandbox reproduction cases.

The sandbox CLI is replaced by a small executable on `PATH` that records how it
was called, so the code under test spawns real processes.
"""

from __future__ import annotations

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
    ReproCase,
    ReproGoal,
    SandboxCli,
    SandboxError,
    SandboxSide,
    SideEvaluation,
    SideOutcome,
    check_twin_gaps,
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

    # Only the last line is a protocol message, and it matches no stream.
    assert evaluation.outcome is SideOutcome.VIOLATES


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
        sides: dict[str, dict], command: str = "read", **options: object
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
            repro_case_dir=str(CASE_DIR),
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
