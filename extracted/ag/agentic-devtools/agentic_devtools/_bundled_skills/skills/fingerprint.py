"""Validate and hash AI PR Loop mutation-gate projections."""

from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from datetime import datetime
from typing import Any


def _jcs_float(value: float) -> str:
    """Serialize *value* using the JSON Canonicalization Scheme number format."""
    if value == 0.0:
        return "0"

    sign = ""
    if value < 0:
        sign = "-"
        value = -value

    representation = repr(value)
    if "e" in representation:
        coefficient, exponent_text = representation.split("e")
        python_exponent = int(exponent_text)
        digits = coefficient.replace(".", "")
        exponent_offset = python_exponent + 1
    else:
        if "." in representation:
            integer_part, fractional_part = representation.split(".")
        else:  # pragma: no cover
            integer_part, fractional_part = representation, ""
        if integer_part == "0":
            leading_zeros = len(fractional_part) - len(fractional_part.lstrip("0"))
            exponent_offset = -leading_zeros
        else:
            exponent_offset = len(integer_part)
        digits = (integer_part + fractional_part).rstrip("0").lstrip("0") or "0"

    digit_count = len(digits)
    if digit_count <= exponent_offset <= 21:
        return sign + digits + "0" * (exponent_offset - digit_count)
    if 0 < exponent_offset <= 21:
        return sign + digits[:exponent_offset] + "." + digits[exponent_offset:]
    if -6 < exponent_offset <= 0:
        return sign + "0." + "0" * (-exponent_offset) + digits
    exponent = exponent_offset - 1
    coefficient = digits if digit_count == 1 else digits[0] + "." + digits[1:]
    exponent_sign = "+" if exponent >= 0 else "-"
    return sign + coefficient + "e" + exponent_sign + str(abs(exponent))


def canonicalize_json(payload: Any) -> bytes:
    """Serialize a JSON-compatible value to canonical UTF-8 JSON bytes."""

    def _validate_utf8_string(value: str, *, context: str) -> str:
        try:
            value.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise TypeError(f"canonicalize_json requires UTF-8 encodable {context}") from exc
        return value

    def _validate(value: Any) -> Any:
        if value is None or type(value) in (bool, int):
            return value
        if type(value) is str:
            return _validate_utf8_string(value, context="strings")
        if type(value) is float:
            if not math.isfinite(value):
                raise TypeError("canonicalize_json does not support non-finite floats")
            return value
        if isinstance(value, (list, tuple)):
            return [_validate(item) for item in value]
        if isinstance(value, dict):
            for key in value:
                if not isinstance(key, str):
                    raise TypeError(f"canonicalize_json requires string keys, got {key!r} ({type(key).__name__})")
                _validate_utf8_string(key, context="object member names")
            return {key: _validate(val) for key, val in value.items()}
        raise TypeError(f"canonicalize_json does not support value of type {type(value).__name__}: {value!r}")

    validated = _validate(payload)

    def _canonical(value: Any) -> str:
        if value is None:
            return "null"
        if value is True:
            return "true"
        if value is False:
            return "false"
        if type(value) is int:
            as_float = float(value)
            if int(as_float) != value:
                raise TypeError(
                    "canonicalize_json does not support integers not exactly"
                    f" representable as IEEE-754 double: {value!r}"
                )
            return _jcs_float(as_float)
        if type(value) is float:
            return _jcs_float(value)
        if type(value) is str:
            return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        if isinstance(value, list):
            return "[" + ",".join(_canonical(item) for item in value) + "]"
        if isinstance(value, dict):
            keys = sorted(value, key=lambda key: key.encode("utf-16-be"))
            return "{" + ",".join(f"{_canonical(key)}:{_canonical(value[key])}" for key in keys) + "}"
        raise TypeError(f"canonicalize_json does not support value of type {type(value).__name__}")  # pragma: no cover

    return _canonical(validated).encode("utf-8")


_TOP_LEVEL_KEYS = {
    "repository",
    "base_branch",
    "base_sha",
    "source_branch",
    "head_sha",
    "expected_head",
    "pr_number",
    "draft",
    "mergeability",
    "conflict_state",
    "latest_ccr_reviewed_sha",
    "auto_merge_label_present",
    "authorized_auto_merge_label",
    "ai_pr_loop_approval",
    "run_authorized",
    "handoff_authorization",
    "required_ci_runs",
    "unresolved_review_threads",
    "active_task_ids",
    "finding_evaluations",
    "additional_preconditions",
}
_PRECONDITION_NAMES = (
    "dispatch_capability",
    "issue_proposal_dedup",
    "monitor_freshness_consistency",
    "packaging_hold",
    "prior_repair_tuples",
    "proposed_repair_tuple",
    "thread_task_evidence",
)
_SHA_PATTERN = r"[0-9a-f]{40}"


def _is_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value)


def _is_sha(value: Any) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(_SHA_PATTERN, value))


def _is_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z", value):
        return False
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return True


def _require_keys(value: Any, keys: set[str], name: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError(f"{name} must contain exactly {sorted(keys)}")
    return value


def _validate_repair_tuple(value: Any, name: str) -> None:
    tuple_value = _require_keys(value, {"head_sha", "finding_key", "thread_id"}, name)
    if not _is_sha(tuple_value["head_sha"]) or not all(
        _is_string(tuple_value[key]) for key in ("finding_key", "thread_id")
    ):
        raise ValueError(f"{name} contains an invalid repair tuple")


def _validate_projection(projection: dict[str, Any]) -> None:
    data = _require_keys(projection, _TOP_LEVEL_KEYS, "fingerprint projection")
    for key in ("repository", "base_branch", "source_branch"):
        if not _is_string(data[key]):
            raise ValueError(f"{key} must be a non-empty string")
    for key in ("base_sha", "head_sha", "expected_head"):
        if not _is_sha(data[key]):
            raise ValueError(f"{key} must be a lowercase 40-character SHA")
    if not isinstance(data["pr_number"], int) or isinstance(data["pr_number"], bool):
        raise ValueError("pr_number must be an integer")
    for key in ("draft", "auto_merge_label_present", "authorized_auto_merge_label", "run_authorized"):
        if not isinstance(data[key], bool):
            raise ValueError(f"{key} must be a boolean")
    if data["mergeability"] not in {"mergeable", "conflicting", "unknown"}:
        raise ValueError("mergeability is invalid")
    if data["conflict_state"] not in {"clean", "dirty", "blocked", "unstable", "behind", "has_hooks", "unknown"}:
        raise ValueError("conflict_state is invalid")
    if data["latest_ccr_reviewed_sha"] is not None and not _is_sha(data["latest_ccr_reviewed_sha"]):
        raise ValueError("latest_ccr_reviewed_sha is invalid")

    approval = _require_keys(data["ai_pr_loop_approval"], {"state", "reviewed_sha"}, "ai_pr_loop_approval")
    if approval["state"] not in {"approved", "rejected", "pending", "absent"}:
        raise ValueError("ai_pr_loop_approval.state is invalid")
    if approval["state"] == "absent":
        if approval["reviewed_sha"] is not None:
            raise ValueError("absent approval must have a null reviewed_sha")
    elif not _is_sha(approval["reviewed_sha"]):
        raise ValueError("ai_pr_loop_approval.reviewed_sha is invalid")

    handoff = data["handoff_authorization"]
    if handoff is not None:
        handoff = _require_keys(
            handoff,
            {"target", "admission_role", "mode", "supervisor_run_id", "checkpoint"},
            "handoff_authorization",
        )
        if handoff["target"] not in {"admission", "p0_implementation"} or handoff["mode"] not in {"drain", "maintain"}:
            raise ValueError("handoff_authorization contains an invalid target or mode")
        if not all(_is_string(handoff[key]) for key in ("admission_role", "supervisor_run_id", "checkpoint")):
            raise ValueError("handoff_authorization contains an invalid string")

    required_ci_runs = data["required_ci_runs"]
    if not isinstance(required_ci_runs, list):
        raise ValueError("required_ci_runs must be an array")
    for run in required_ci_runs:
        run = _require_keys(run, {"run_id", "head_sha", "status", "conclusion", "required"}, "required_ci_runs entry")
        if not isinstance(run["run_id"], int) or isinstance(run["run_id"], bool) or not _is_sha(run["head_sha"]):
            raise ValueError("required_ci_runs contains an invalid identity")
        if run["status"] not in {"queued", "in_progress", "completed"} or not isinstance(run["required"], bool):
            raise ValueError("required_ci_runs contains an invalid status")
        if run["status"] == "completed":
            if run["conclusion"] not in {
                "success",
                "failure",
                "neutral",
                "cancelled",
                "skipped",
                "timed_out",
                "action_required",
                "stale",
                "startup_failure",
            }:
                raise ValueError("completed CI run has an invalid conclusion")
        elif run["conclusion"] is not None:
            raise ValueError("pending CI run must have a null conclusion")
    if required_ci_runs != sorted(
        required_ci_runs,
        key=lambda run: (
            not run["required"],
            run["run_id"],
            run["head_sha"],
            run["status"],
            run["conclusion"] or "",
        ),
    ):
        raise ValueError("required_ci_runs must be sorted")

    threads = data["unresolved_review_threads"]
    if not isinstance(threads, list):
        raise ValueError("unresolved_review_threads must be an array")
    for thread in threads:
        thread = _require_keys(
            thread,
            {"thread_id", "finding_decision", "latest_comment_id", "latest_updated_at"},
            "unresolved_review_threads entry",
        )
        if (
            not _is_string(thread["thread_id"])
            or thread["finding_decision"] not in {"addressed", "valid", "rejected", "stale", "duplicate", "UNKNOWN"}
            or not isinstance(thread["latest_comment_id"], int)
            or isinstance(thread["latest_comment_id"], bool)
            or not _is_timestamp(thread["latest_updated_at"])
        ):
            raise ValueError("unresolved_review_threads contains an invalid entry")
    if threads != sorted(
        threads, key=lambda thread: (thread["thread_id"], thread["latest_comment_id"], thread["latest_updated_at"])
    ):
        raise ValueError("unresolved_review_threads must be sorted")

    task_ids = data["active_task_ids"]
    if (
        not isinstance(task_ids, list)
        or not all(_is_string(task_id) for task_id in task_ids)
        or task_ids != sorted(task_ids)
    ):
        raise ValueError("active_task_ids must be a sorted string array")

    evaluations = data["finding_evaluations"]
    if not isinstance(evaluations, list):
        raise ValueError("finding_evaluations must be an array")
    evaluation_keys = {
        "finding_id",
        "visibility",
        "review_id",
        "review_id_match",
        "reviewed_head_match",
        "response_author_authorized",
        "authorized_evaluation_marker",
        "resolution_allowed",
        "reviewed_sha",
        "decision",
        "updated_by",
        "updated_at",
    }
    for evaluation in evaluations:
        evaluation = _require_keys(evaluation, evaluation_keys, "finding_evaluations entry")
        if (
            not all(_is_string(evaluation[key]) for key in ("finding_id", "review_id", "updated_by"))
            or evaluation["visibility"] not in {"visible", "suppressed"}
            or not all(
                isinstance(evaluation[key], bool)
                for key in (
                    "review_id_match",
                    "reviewed_head_match",
                    "response_author_authorized",
                    "authorized_evaluation_marker",
                    "resolution_allowed",
                )
            )
            or (evaluation["reviewed_sha"] is not None and not _is_sha(evaluation["reviewed_sha"]))
            or evaluation["decision"] not in {"addressed", "valid", "rejected", "stale", "duplicate", "UNKNOWN"}
            or not _is_timestamp(evaluation["updated_at"])
        ):
            raise ValueError("finding_evaluations contains an invalid entry")
    evaluation_order = (
        "finding_id",
        "visibility",
        "review_id",
        "review_id_match",
        "reviewed_head_match",
        "response_author_authorized",
        "authorized_evaluation_marker",
        "resolution_allowed",
        "reviewed_sha",
        "decision",
        "updated_by",
        "updated_at",
    )
    if evaluations != sorted(
        evaluations,
        key=lambda item: tuple(
            (item[key] is not None, item[key]) if key == "reviewed_sha" else item[key] for key in evaluation_order
        ),
    ):
        raise ValueError("finding_evaluations must be sorted")

    preconditions = data["additional_preconditions"]
    if not isinstance(preconditions, list) or not all(isinstance(item, dict) for item in preconditions):
        raise ValueError("additional_preconditions must be an array of objects")
    if [item["name"] for item in preconditions if "name" in item] != list(_PRECONDITION_NAMES):
        raise ValueError("additional_preconditions must contain the sorted catalog")
    for item in preconditions:
        _require_keys(item, {"name", "value"}, "additional_preconditions entry")
    _validate_preconditions(preconditions)


def _validate_preconditions(preconditions: list[dict[str, Any]]) -> None:
    values = {item["name"]: item["value"] for item in preconditions}
    dispatch = _require_keys(
        values["dispatch_capability"], {"http_status", "retry_authorized", "record_status"}, "dispatch_capability"
    )
    if (
        (
            dispatch["http_status"] is not None
            and (not isinstance(dispatch["http_status"], int) or isinstance(dispatch["http_status"], bool))
        )
        or not isinstance(dispatch["retry_authorized"], bool)
        or dispatch["record_status"] not in {"present", "missing", "ambiguous"}
    ):
        raise ValueError("dispatch_capability is invalid")
    issue = values["issue_proposal_dedup"]
    if issue is not None:
        issue = _require_keys(
            issue,
            {"dedup_marker", "open_search_complete", "closed_search_complete", "existing_issue"},
            "issue_proposal_dedup",
        )
        if (
            (issue["dedup_marker"] is not None and not _is_string(issue["dedup_marker"]))
            or not isinstance(issue["open_search_complete"], bool)
            or not isinstance(issue["closed_search_complete"], bool)
            or (issue["existing_issue"] is not None and not _is_string(issue["existing_issue"]))
        ):
            raise ValueError("issue_proposal_dedup is invalid")
    monitor = _require_keys(
        values["monitor_freshness_consistency"],
        {
            "actions_source_identity",
            "event_source_identity",
            "actions_run_id",
            "event_run_id",
            "actions_pr_number",
            "event_pr_number",
            "actions_head_sha",
            "event_head_sha",
            "actions_transition",
            "event_transition",
            "actions_observed_at",
            "event_observed_at",
            "verified_at",
            "fresh_until",
            "freshness_ttl_seconds",
        },
        "monitor_freshness_consistency",
    )
    string_keys = {
        "actions_source_identity",
        "event_source_identity",
        "actions_run_id",
        "event_run_id",
        "actions_head_sha",
        "event_head_sha",
        "actions_transition",
        "event_transition",
        "actions_observed_at",
        "event_observed_at",
        "verified_at",
        "fresh_until",
    }
    integer_keys = {"actions_pr_number", "event_pr_number", "freshness_ttl_seconds"}
    for key in string_keys:
        if monitor[key] is not None and not _is_string(monitor[key]):
            raise ValueError(f"{key} is invalid")
    for key in ("actions_head_sha", "event_head_sha"):
        if monitor[key] is not None and not _is_sha(monitor[key]):
            raise ValueError(f"{key} is invalid")
    for key in ("actions_observed_at", "event_observed_at", "verified_at", "fresh_until"):
        if monitor[key] is not None and not _is_timestamp(monitor[key]):
            raise ValueError(f"{key} is invalid")
    for key in integer_keys:
        if key != "freshness_ttl_seconds" and monitor[key] is None:
            continue
        if not isinstance(monitor[key], int) or isinstance(monitor[key], bool):
            raise ValueError(f"{key} is invalid")
    if monitor["freshness_ttl_seconds"] < 0:
        raise ValueError("freshness_ttl_seconds must be non-negative")
    if monitor["verified_at"] is not None and monitor["fresh_until"] is not None:
        # Compare fractional digits separately: datetime truncates beyond microseconds.
        verified_at = datetime.fromisoformat(monitor["verified_at"][:19] + "+00:00")
        fresh_until = datetime.fromisoformat(monitor["fresh_until"][:19] + "+00:00")
        verified_fraction = monitor["verified_at"][20:-1].rstrip("0")
        fresh_fraction = monitor["fresh_until"][20:-1].rstrip("0")
        interval = ((fresh_until - verified_at).total_seconds(), fresh_fraction)
        if not (0, verified_fraction) <= interval <= (monitor["freshness_ttl_seconds"], verified_fraction):
            raise ValueError("monitor freshness interval must be non-negative and within freshness_ttl_seconds")
    packaging = _require_keys(values["packaging_hold"], {"evidence_status", "marker", "p0_hold"}, "packaging_hold")
    if (
        packaging["evidence_status"] not in {"current", "missing", "ambiguous"}
        or (packaging["marker"] is not None and not _is_string(packaging["marker"]))
        or not isinstance(packaging["p0_hold"], bool)
    ):
        raise ValueError("packaging_hold is invalid")
    proposed = values["proposed_repair_tuple"]
    if proposed is not None:
        _validate_repair_tuple(proposed, "proposed_repair_tuple")
    prior = values["prior_repair_tuples"]
    if not isinstance(prior, list):
        raise ValueError("prior_repair_tuples must be an array")
    for item in prior:
        _validate_repair_tuple(item, "prior_repair_tuples entry")
    if prior != sorted(prior, key=lambda item: (item["head_sha"], item["finding_key"], item["thread_id"])):
        raise ValueError("prior_repair_tuples must be sorted")
    task_evidence = _require_keys(
        values["thread_task_evidence"], {"active_task_ids", "evidence_status"}, "thread_task_evidence"
    )
    if (
        not isinstance(task_evidence["active_task_ids"], list)
        or task_evidence["active_task_ids"] != sorted(task_evidence["active_task_ids"])
        or not all(_is_string(task_id) for task_id in task_evidence["active_task_ids"])
        or task_evidence["evidence_status"] not in {"current", "missing", "ambiguous", "unsupported"}
    ):
        raise ValueError("thread_task_evidence is invalid")


def fingerprint_projection(projection: Any) -> str:
    """Return the SHA-256 JCS digest for a valid projection mapping."""
    if not isinstance(projection, dict):
        raise TypeError("fingerprint projection must be a JSON object")
    _validate_projection(projection)
    return hashlib.sha256(canonicalize_json(projection)).hexdigest()


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON member: {key}")
        result[key] = value
    return result


def _reject_non_finite(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def main() -> int:
    """Read a projection from stdin and emit its canonical fingerprint record."""
    try:
        projection = json.load(sys.stdin, object_pairs_hook=_reject_duplicate_keys, parse_constant=_reject_non_finite)
        digest = fingerprint_projection(projection)
    except (json.JSONDecodeError, TypeError, ValueError, OverflowError) as exc:
        print(f"invalid fingerprint projection: {exc}", file=sys.stderr)
        return 2
    print(
        json.dumps(
            {
                "fingerprint_algorithm": "sha256-jcs",
                "fingerprint_projection": projection,
                "evidence_fingerprint": digest,
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
