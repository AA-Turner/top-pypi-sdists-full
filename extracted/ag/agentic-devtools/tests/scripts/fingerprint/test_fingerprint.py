"""Tests for the fingerprint skill validator."""

from __future__ import annotations

import hashlib
import importlib
import importlib.util
import io
import json
import subprocess
import sys
from pathlib import Path

import pytest


def _load_fingerprint():
    bundled_name = "agentic_devtools._bundled_skills.skills.fingerprint"
    if f"--cov={bundled_name}" in sys.argv:
        return importlib.import_module(bundled_name)
    if bundled_name in sys.modules:
        return sys.modules[bundled_name]
    path = Path(__file__).parents[3] / ".agents" / "skills" / "fingerprint.py"
    spec = importlib.util.spec_from_file_location("fingerprint_skill", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


fingerprint = _load_fingerprint()


def _projection() -> dict:
    sha = "a" * 40
    return {
        "repository": "swai-factory/agentic-devtools",
        "base_branch": "main",
        "base_sha": sha,
        "source_branch": "feature/test",
        "head_sha": sha,
        "expected_head": sha,
        "pr_number": 4142,
        "draft": False,
        "mergeability": "mergeable",
        "conflict_state": "clean",
        "latest_ccr_reviewed_sha": None,
        "auto_merge_label_present": False,
        "authorized_auto_merge_label": False,
        "ai_pr_loop_approval": {"state": "absent", "reviewed_sha": None},
        "run_authorized": True,
        "handoff_authorization": None,
        "required_ci_runs": [
            {
                "run_id": 1,
                "head_sha": sha,
                "status": "queued",
                "conclusion": None,
                "required": True,
            }
        ],
        "unresolved_review_threads": [
            {
                "thread_id": "thread-1",
                "finding_decision": "valid",
                "latest_comment_id": 1,
                "latest_updated_at": "2026-09-15T13:00:00Z",
            }
        ],
        "active_task_ids": ["task-1"],
        "finding_evaluations": [],
        "additional_preconditions": [
            {
                "name": "dispatch_capability",
                "value": {"http_status": None, "retry_authorized": True, "record_status": "present"},
            },
            {
                "name": "issue_proposal_dedup",
                "value": None,
            },
            {
                "name": "monitor_freshness_consistency",
                "value": {
                    "actions_source_identity": None,
                    "event_source_identity": None,
                    "actions_run_id": None,
                    "event_run_id": None,
                    "actions_pr_number": None,
                    "event_pr_number": None,
                    "actions_head_sha": None,
                    "event_head_sha": None,
                    "actions_transition": None,
                    "event_transition": None,
                    "actions_observed_at": None,
                    "event_observed_at": None,
                    "verified_at": None,
                    "fresh_until": None,
                    "freshness_ttl_seconds": 300,
                },
            },
            {
                "name": "packaging_hold",
                "value": {"evidence_status": "current", "marker": None, "p0_hold": False},
            },
            {"name": "prior_repair_tuples", "value": []},
            {"name": "proposed_repair_tuple", "value": None},
            {
                "name": "thread_task_evidence",
                "value": {"active_task_ids": ["task-1"], "evidence_status": "current"},
            },
        ],
    }


@pytest.mark.parametrize(
    ("value", "expected"),
    [(None, False), ("", False), ("text", True), (1, False), (False, False)],
)
def test_is_string(value, expected) -> None:
    assert fingerprint._is_string(value) is expected


def test_is_sha_and_timestamp() -> None:
    assert fingerprint._is_sha("a" * 40)
    assert not fingerprint._is_sha("A" * 40)
    assert not fingerprint._is_sha("a" * 39)
    assert fingerprint._is_timestamp("2026-09-15T13:00:00Z")
    assert fingerprint._is_timestamp("2026-09-15T13:00:00.123Z")
    assert not fingerprint._is_timestamp("2026-02-30T13:00:00Z")
    assert not fingerprint._is_timestamp("2026-09-15 13:00:00Z")


def test_require_keys_rejects_non_mapping_and_extra_or_missing_keys() -> None:
    with pytest.raises(ValueError):
        fingerprint._require_keys([], {"key"}, "value")
    with pytest.raises(ValueError):
        fingerprint._require_keys({"key": 1, "extra": 2}, {"key"}, "value")


def test_validate_repair_tuple_rejects_invalid_values() -> None:
    valid = {"head_sha": "a" * 40, "finding_key": "finding", "thread_id": "thread"}
    fingerprint._validate_repair_tuple(valid, "tuple")
    for invalid in (
        {"head_sha": "bad", "finding_key": "finding", "thread_id": "thread"},
        {"head_sha": "a" * 40, "finding_key": "", "thread_id": "thread"},
    ):
        with pytest.raises(ValueError):
            fingerprint._validate_repair_tuple(invalid, "tuple")


def test_validate_projection_accepts_canonical_projection() -> None:
    fingerprint._validate_projection(_projection())


@pytest.mark.parametrize(
    ("verified_at", "fresh_until", "ttl"),
    [
        (None, None, -1),
        (None, None, True),
        (None, None, 1.5),
        (None, None, None),
        ("2026-09-15T13:00:00Z", "2026-09-15T12:59:59Z", 300),
        ("2026-09-15T13:00:00Z", "2026-09-15T13:05:01Z", 300),
        ("2026-09-15T13:00:00Z", "2026-09-15T13:00:00.000001Z", 0),
        ("2026-09-15T13:00:00.123Z", "2026-09-15T13:05:00.123001Z", 300),
        ("2026-09-15T13:00:00.0000001Z", "2026-09-15T13:00:00Z", 300),
        ("2026-09-15T13:00:00Z", "2026-09-15T13:00:00.0000001Z", 0),
        ("2026-09-15T13:00:00.123Z", "2026-09-15T13:05:00.1230001Z", 300),
    ],
)
def test_main_rejects_invalid_monitor_interval(monkeypatch, capsys, verified_at, fresh_until, ttl) -> None:
    projection = _projection()
    projection["additional_preconditions"][2]["value"].update(
        verified_at=verified_at, fresh_until=fresh_until, freshness_ttl_seconds=ttl
    )
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(projection)))

    assert fingerprint.main() == 2
    output = capsys.readouterr()
    assert output.out == ""
    assert output.err.startswith("invalid fingerprint projection:")


@pytest.mark.parametrize(
    ("verified_at", "fresh_until", "ttl"),
    [
        (None, None, 300),
        (None, "2026-09-15T13:05:00Z", 300),
        ("2026-09-15T13:00:00Z", None, 300),
        ("2026-09-15T13:00:00Z", "2026-09-15T13:00:00Z", 0),
        ("2026-09-15T13:00:00Z", "2026-09-15T13:04:59Z", 300),
        ("2026-09-15T13:00:00Z", "2026-09-15T13:05:00Z", 300),
        ("2026-09-15T13:00:00.123Z", "2026-09-15T13:05:00.123Z", 300),
        ("2026-09-15T13:00:00.1230000Z", "2026-09-15T13:05:00.123Z", 300),
        ("2026-09-15T13:00:00.123Z", "2026-09-15T13:05:00.1230000Z", 300),
        ("2026-09-15T13:00:00.0000001Z", "2026-09-15T13:05:00.0000001Z", 300),
        ("2026-09-15T13:59:59.999999Z", "2026-09-15T14:00:00Z", 1),
        ("2026-09-15T13:00:00Z", "2026-09-15T13:05:00Z", 10**12),
    ],
)
def test_fingerprint_projection_accepts_valid_or_unknown_monitor_interval(verified_at, fresh_until, ttl) -> None:
    projection = _projection()
    projection["additional_preconditions"][2]["value"].update(
        verified_at=verified_at, fresh_until=fresh_until, freshness_ttl_seconds=ttl
    )
    expected = hashlib.sha256(fingerprint.canonicalize_json(projection)).hexdigest()

    assert fingerprint.fingerprint_projection(projection) == expected


@pytest.mark.parametrize(
    "change",
    [
        lambda p: p.update(repository=""),
        lambda p: p.update(base_sha="bad"),
        lambda p: p.update(pr_number=True),
        lambda p: p.update(draft=None),
        lambda p: p.update(mergeability="bad"),
        lambda p: p.update(conflict_state="bad"),
        lambda p: p.update(latest_ccr_reviewed_sha="bad"),
        lambda p: p["ai_pr_loop_approval"].update(state="absent", reviewed_sha="a" * 40),
        lambda p: p["ai_pr_loop_approval"].update(state="pending", reviewed_sha=None),
        lambda p: p.update(handoff_authorization={"target": "bad"}),
        lambda p: p["required_ci_runs"][0].update(status="completed"),
        lambda p: p["required_ci_runs"][0].update(status="queued", conclusion="failure"),
        lambda p: (
            p["required_ci_runs"].append(
                {
                    "run_id": 2,
                    "head_sha": "a" * 40,
                    "status": "queued",
                    "conclusion": None,
                    "required": True,
                }
            ),
            p["required_ci_runs"].reverse(),
        ),
        lambda p: p["unresolved_review_threads"][0].update(latest_updated_at="bad"),
        lambda p: (
            p["unresolved_review_threads"].append(
                {
                    "thread_id": "thread-2",
                    "finding_decision": "valid",
                    "latest_comment_id": 1,
                    "latest_updated_at": "2026-09-15T13:00:00Z",
                }
            ),
            p["unresolved_review_threads"].reverse(),
        ),
        lambda p: p.update(active_task_ids=[1]),
        lambda p: p.update(additional_preconditions=[]),
        lambda p: p.update(additional_preconditions="bad"),
        lambda p: p["additional_preconditions"][0].update(value={"retry_authorized": True}),
        lambda p: p["ai_pr_loop_approval"].update(state="invalid"),
        lambda p: (
            p["ai_pr_loop_approval"].update(state="pending", reviewed_sha="a" * 40),
            p.update(active_task_ids=[1]),
        ),
        lambda p: (
            p.update(
                handoff_authorization={
                    "target": "admission",
                    "admission_role": "role",
                    "mode": "drain",
                    "supervisor_run_id": "run",
                    "checkpoint": "checkpoint",
                }
            ),
            p.update(active_task_ids=[1]),
        ),
        lambda p: p.update(
            handoff_authorization={
                "target": "bad",
                "admission_role": "role",
                "mode": "drain",
                "supervisor_run_id": "run",
                "checkpoint": "checkpoint",
            }
        ),
        lambda p: p.update(
            handoff_authorization={
                "target": "admission",
                "admission_role": "",
                "mode": "drain",
                "supervisor_run_id": "run",
                "checkpoint": "checkpoint",
            }
        ),
        lambda p: p.update(required_ci_runs="bad"),
        lambda p: p["required_ci_runs"][0].update(run_id="bad"),
        lambda p: p["required_ci_runs"][0].update(required="bad"),
        lambda p: (
            p["required_ci_runs"][0].update(status="completed", conclusion="success"),
            p.update(active_task_ids=[1]),
        ),
        lambda p: p.update(unresolved_review_threads="bad"),
        lambda p: p.update(finding_evaluations="bad"),
        lambda p: (
            p.update(
                finding_evaluations=[
                    {
                        "finding_id": "finding",
                        "visibility": "visible",
                        "review_id": "review",
                        "review_id_match": True,
                        "reviewed_head_match": True,
                        "response_author_authorized": True,
                        "authorized_evaluation_marker": True,
                        "resolution_allowed": True,
                        "reviewed_sha": None,
                        "decision": "valid",
                        "updated_by": "agent",
                        "updated_at": "2026-09-15T13:00:00Z",
                    }
                ]
            ),
            p.update(active_task_ids=[1]),
        ),
        lambda p: p.update(
            finding_evaluations=[
                {
                    "finding_id": "finding-2",
                    "visibility": "visible",
                    "review_id": "review",
                    "review_id_match": True,
                    "reviewed_head_match": True,
                    "response_author_authorized": True,
                    "authorized_evaluation_marker": True,
                    "resolution_allowed": True,
                    "reviewed_sha": None,
                    "decision": "valid",
                    "updated_by": "agent",
                    "updated_at": "2026-09-15T13:00:00Z",
                },
                {
                    "finding_id": "finding-1",
                    "visibility": "visible",
                    "review_id": "review",
                    "review_id_match": True,
                    "reviewed_head_match": True,
                    "response_author_authorized": True,
                    "authorized_evaluation_marker": True,
                    "resolution_allowed": True,
                    "reviewed_sha": None,
                    "decision": "valid",
                    "updated_by": "agent",
                    "updated_at": "2026-09-15T13:00:00Z",
                },
            ]
        ),
        lambda p: p["additional_preconditions"].__setitem__(
            0,
            {
                "name": "dispatch_capability",
                "value": {"http_status": "bad", "retry_authorized": True, "record_status": "present"},
            },
        ),
        lambda p: (
            p["additional_preconditions"][1].update(
                value={
                    "dedup_marker": "marker",
                    "open_search_complete": True,
                    "closed_search_complete": True,
                    "existing_issue": None,
                }
            ),
            p["additional_preconditions"][3].update(value={"evidence_status": "bad", "marker": None, "p0_hold": False}),
        ),
        lambda p: p["additional_preconditions"][2]["value"].update(actions_source_identity=1),
        lambda p: p["additional_preconditions"][2]["value"].update(actions_head_sha="bad"),
        lambda p: p["additional_preconditions"][2]["value"].update(actions_observed_at="bad"),
        lambda p: p["additional_preconditions"][3].update(
            value={"evidence_status": "bad", "marker": None, "p0_hold": False}
        ),
        lambda p: (
            p["additional_preconditions"][4].update(
                value=[{"head_sha": "a" * 40, "finding_key": "finding", "thread_id": "thread"}]
            ),
            p.update(active_task_ids=[1]),
        ),
        lambda p: (
            p["additional_preconditions"][5].update(
                value={"head_sha": "a" * 40, "finding_key": "finding", "thread_id": "thread"}
            ),
            p["additional_preconditions"][4].update(value="bad"),
        ),
        lambda p: p["additional_preconditions"][4].update(value="bad"),
        lambda p: p["additional_preconditions"][4].update(
            value=[
                {"head_sha": "b" * 40, "finding_key": "finding", "thread_id": "thread"},
                {"head_sha": "a" * 40, "finding_key": "finding", "thread_id": "thread"},
            ]
        ),
        lambda p: p["additional_preconditions"][6].update(value={"active_task_ids": [1], "evidence_status": "current"}),
    ],
)
def test_validate_projection_rejects_malformed_or_unsorted_projection(change) -> None:
    projection = _projection()
    change(projection)
    with pytest.raises(ValueError):
        fingerprint._validate_projection(projection)


def test_validate_projection_checks_nested_preconditions_and_evaluations() -> None:
    projection = _projection()
    projection["additional_preconditions"][1]["value"] = {
        "dedup_marker": 1,
        "open_search_complete": True,
        "closed_search_complete": True,
        "existing_issue": None,
    }
    with pytest.raises(ValueError):
        fingerprint._validate_projection(projection)

    projection = _projection()
    projection["finding_evaluations"] = [
        {
            "finding_id": "finding",
            "visibility": "visible",
            "review_id": "review",
            "review_id_match": True,
            "reviewed_head_match": True,
            "response_author_authorized": True,
            "authorized_evaluation_marker": True,
            "resolution_allowed": True,
            "reviewed_sha": None,
            "decision": "valid",
            "updated_by": "agent",
            "updated_at": "bad",
        }
    ]
    with pytest.raises(ValueError):
        fingerprint._validate_projection(projection)


def test_fingerprint_projection_is_sha256_of_canonical_json() -> None:
    projection = _projection()
    expected = hashlib.sha256(fingerprint.canonicalize_json(projection)).hexdigest()
    assert fingerprint.fingerprint_projection(projection) == expected
    with pytest.raises(TypeError):
        fingerprint.fingerprint_projection(None)


@pytest.mark.parametrize(
    ("payload", "expected"),
    [
        ({"b": 1, "a": [None, True, False, "text", 1.5, 0.001]}, b'{"a":[null,true,false,"text",1.5,0.001],"b":1}'),
        (1e20, b"100000000000000000000"),
        (1e22, b"1e+22"),
        (1e-7, b"1e-7"),
        (1.5e30, b"1.5e+30"),
        (-1.5, b"-1.5"),
        (-0.0, b"0"),
    ],
)
def test_canonicalize_json_handles_jcs_values(payload, expected) -> None:
    assert fingerprint.canonicalize_json(payload) == expected


@pytest.mark.parametrize(
    "payload",
    [
        float("inf"),
        {"\ud800": "value"},
        {1: "value"},
        object(),
        2**54 + 1,
    ],
)
def test_canonicalize_json_rejects_unsupported_values(payload) -> None:
    with pytest.raises(TypeError):
        fingerprint.canonicalize_json(payload)


def test_json_hooks_reject_duplicate_and_non_finite_values() -> None:
    with pytest.raises(ValueError, match="duplicate JSON member"):
        json.loads('{"key": 1, "key": 2}', object_pairs_hook=fingerprint._reject_duplicate_keys)
    with pytest.raises(ValueError, match="non-finite"):
        json.loads("NaN", parse_constant=fingerprint._reject_non_finite)


def test_main_emits_sorted_canonical_record(monkeypatch, capsys) -> None:
    projection = _projection()
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(projection)))
    assert fingerprint.main() == 0
    output = json.loads(capsys.readouterr().out)
    assert output["fingerprint_algorithm"] == "sha256-jcs"
    assert output["fingerprint_projection"] == projection
    assert output["evidence_fingerprint"] == fingerprint.fingerprint_projection(projection)


@pytest.mark.parametrize("payload", ["null", '{"repository": 1}', '{"key": 1, "key": 2}', "NaN"])
def test_main_rejects_invalid_input(monkeypatch, capsys, payload) -> None:
    monkeypatch.setattr(sys, "stdin", io.StringIO(payload))
    assert fingerprint.main() == 2
    assert capsys.readouterr().err.startswith("invalid fingerprint projection:")


def test_main_rejects_integer_overflow_without_traceback(monkeypatch, capsys) -> None:
    projection = _projection()
    projection["pr_number"] = 10**1000
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(projection)))

    assert fingerprint.main() == 2
    output = capsys.readouterr()
    assert output.out == ""
    assert output.err.startswith("invalid fingerprint projection:")
    assert "Traceback" not in output.err


def test_script_runs_without_agentic_devtools_on_sys_path() -> None:
    path = Path(__file__).parents[3] / ".agents" / "skills" / "fingerprint.py"
    result = subprocess.run(
        [sys.executable, "-S", str(path)],
        input=json.dumps(_projection()),
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert json.loads(result.stdout)["fingerprint_algorithm"] == "sha256-jcs"
    assert result.stderr == ""
