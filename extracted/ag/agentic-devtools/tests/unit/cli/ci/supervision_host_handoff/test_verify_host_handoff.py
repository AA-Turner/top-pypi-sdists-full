import hashlib
import json
from collections.abc import Sequence
from datetime import UTC, datetime, timedelta, timezone

import pytest

from agentic_devtools._bundled_skills.skills.fingerprint import canonicalize_json
from agentic_devtools.cli.ci.supervision_host_handoff import (
    HOST_ROOT_SESSION_ID,
    HostHandoffRejectionReason,
    verify_host_handoff,
)

NOW = datetime(2026, 10, 22, 1, 0, tzinfo=UTC)
EXPECTED = {
    "repository": "swai-factory/agentic-devtools",
    "role": "admission",
    "mode": "maintain",
    "supervisor_run_id": "2026-10-22T00:00:00Z-a1b2c3",
    "checkpoint": "checkpoint-42",
}
MARKER = "<!-- ai-pr-loop-host-handoff:v1 -->"
LABEL = "🤖 AI PR Loop ·"


def _payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "repository": EXPECTED["repository"],
        "target": "admission",
        "admission_role": EXPECTED["role"],
        "mode": EXPECTED["mode"],
        "supervisor_run_id": EXPECTED["supervisor_run_id"],
        "checkpoint": EXPECTED["checkpoint"],
        "host_root_session": HOST_ROOT_SESSION_ID,
        "issued_at": "2026-10-22T00:10:00Z",
        "expires_at": "2026-10-22T01:05:00Z",
    }
    payload.update(overrides)
    unsigned = dict(payload)
    unsigned.pop("fingerprint", None)
    payload["fingerprint"] = hashlib.sha256(canonicalize_json(unsigned)).hexdigest()
    return payload


def _comment(payload: dict[str, object] | None = None, **node_overrides: object) -> dict[str, object]:
    body = f"{MARKER}\n{canonicalize_json(payload or _payload()).decode()}\n\n{LABEL}"
    node: dict[str, object] = {
        "body": body,
        "author": {"login": "HostUser"},
        "lastEditedAt": None,
    }
    node.update(node_overrides)
    return node


def _verify(comments: Sequence[object], *, now: datetime = NOW, **kwargs: object):
    return verify_host_handoff(
        comments,
        trusted_logins={"hostuser"},
        expected=EXPECTED,
        now=now,
        **kwargs,
    )


def _assert_rejected(
    comments: Sequence[object],
    reason: HostHandoffRejectionReason,
    *,
    now: datetime = NOW,
) -> None:
    result = _verify(comments, now=now)
    assert not result.accepted
    assert result.reason is reason
    assert result.payload is None


def test_accepts_canonical_trusted_comment_with_ai_pr_loop_suffix() -> None:
    result = _verify([_comment()])

    assert result.accepted
    assert result.reason is None
    assert result.payload == _payload()


def test_accepts_issued_at_now_and_exactly_fifty_five_minute_lifetime() -> None:
    payload = _payload(issued_at="2026-10-22T01:00:00Z", expires_at="2026-10-22T01:55:00Z")

    assert _verify([_comment(payload)]).accepted


def test_rejects_issue_time_one_fractional_instant_after_now() -> None:
    payload = _payload(issued_at="2026-10-22T01:00:00.00000000000000000001Z")

    _assert_rejected([_comment(payload)], HostHandoffRejectionReason.FUTURE_ISSUED_AT)


def test_accepts_expiry_one_fractional_instant_after_now() -> None:
    payload = _payload(expires_at="2026-10-22T01:00:00.00000000000000000001Z")

    assert _verify([_comment(payload)]).accepted


def test_rejects_lifetime_one_fractional_instant_over_fifty_five_minutes() -> None:
    payload = _payload(issued_at="2026-10-22T00:00:00Z", expires_at="2026-10-22T00:55:00.00000000000000000001Z")
    now = datetime(2026, 10, 22, 0, 30, tzinfo=UTC)

    _assert_rejected([_comment(payload)], HostHandoffRejectionReason.LIFETIME_EXCEEDED, now=now)


def test_rejects_when_no_marker_candidate_exists() -> None:
    _assert_rejected([], HostHandoffRejectionReason.NO_RECORD)
    _assert_rejected([{"body": "unrelated"}], HostHandoffRejectionReason.NO_RECORD)


def test_untrusted_body_cannot_claim_or_embed_trusted_login() -> None:
    node = _comment()
    node["author"] = {"login": "attacker"}
    node["body"] = f"hostuser {node['body']}"

    _assert_rejected([node], HostHandoffRejectionReason.UNTRUSTED_AUTHOR)


@pytest.mark.parametrize(
    "author",
    [None, {}, {"login": None}, {"login": 42}, {"login": ""}],
)
def test_missing_or_non_string_login_is_untrusted(author: object) -> None:
    node = _comment()
    node["author"] = author

    _assert_rejected([node], HostHandoffRejectionReason.UNTRUSTED_AUTHOR)


def test_trusted_login_is_case_insensitive() -> None:
    result = verify_host_handoff(
        [_comment(author={"login": "HOSTUSER"})],
        trusted_logins={"HostUser"},
        expected=EXPECTED,
        now=NOW,
    )

    assert result.accepted


def test_rejects_edited_comment() -> None:
    _assert_rejected(
        [_comment(lastEditedAt="2026-10-22T00:30:00Z")],
        HostHandoffRejectionReason.EDITED_COMMENT,
    )


def test_valid_non_utc_offset_edit_timestamp_is_still_edited() -> None:
    _assert_rejected(
        [_comment(lastEditedAt="2026-10-22T01:30:00+01:00")],
        HostHandoffRejectionReason.EDITED_COMMENT,
    )


def test_untrusted_candidate_is_ignored_when_trusted_record_exists() -> None:
    untrusted = _comment()
    untrusted["author"] = {"login": "attacker"}

    assert _verify([untrusted, _comment()]).accepted


@pytest.mark.parametrize(
    "body",
    [
        f"prefix {MARKER}\n{{}}\n\n{LABEL}",
        f"{MARKER}\n{{}}\nextra\n\n{LABEL}",
        f"{MARKER}\r\n{{}}\r\n\r\n{LABEL}",
        f"{MARKER}\n{{}}",
        f"{MARKER}\n{{}}\n\n{LABEL} extra",
    ],
)
def test_rejects_malformed_marker_or_wrapper(body: str) -> None:
    _assert_rejected([_comment(body=body)], HostHandoffRejectionReason.MALFORMED_MARKER)


@pytest.mark.parametrize(
    "overrides",
    [
        {"lastEditedAt": "not-a-timestamp"},
        {"lastEditedAt": "2026-02-30T00:00:00Z"},
        {"lastEditedAt": 7},
    ],
)
def test_rejects_malformed_comment_node(overrides: dict[str, object]) -> None:
    node = _comment()
    node.update(overrides)

    _assert_rejected([node], HostHandoffRejectionReason.MALFORMED_COMMENT_NODE)


def test_malformed_marker_precedes_malformed_comment_node() -> None:
    node = _comment(body=f"prefix {MARKER}", lastEditedAt="invalid")

    _assert_rejected([node], HostHandoffRejectionReason.MALFORMED_MARKER)


def test_missing_last_edited_at_is_malformed_node() -> None:
    node = _comment()
    node.pop("lastEditedAt")

    _assert_rejected([node], HostHandoffRejectionReason.MALFORMED_COMMENT_NODE)


def test_detects_duplicate_json_members_before_payload_validation() -> None:
    duplicated = '{"repository":"old","repository":"swai-factory/agentic-devtools"}'
    node = _comment(body=f"{MARKER}\n{duplicated}\n\n{LABEL}")

    _assert_rejected([node], HostHandoffRejectionReason.DUPLICATE_JSON_KEY)


def test_duplicate_json_key_precedes_malformed_json() -> None:
    duplicated_and_malformed = '{"repository":"first","repository":"second"} trailing'
    node = _comment(body=f"{MARKER}\n{duplicated_and_malformed}\n\n{LABEL}")

    _assert_rejected([node], HostHandoffRejectionReason.DUPLICATE_JSON_KEY)


def test_rejects_malformed_json() -> None:
    node = _comment(body=f"{MARKER}\n{{broken\n\n{LABEL}")

    _assert_rejected([node], HostHandoffRejectionReason.MALFORMED_JSON)


def test_rejects_json_that_is_not_an_object() -> None:
    node = _comment(body=f"{MARKER}\n[]\n\n{LABEL}")

    _assert_rejected([node], HostHandoffRejectionReason.MALFORMED_JSON)


def test_unknown_field_precedes_missing_field() -> None:
    payload = _payload()
    payload.pop("checkpoint")
    payload["surprise"] = "extra"
    node = _comment(payload)

    _assert_rejected([node], HostHandoffRejectionReason.UNKNOWN_FIELD)


def test_rejects_missing_field() -> None:
    payload = _payload()
    payload.pop("checkpoint")
    node = _comment(payload)

    _assert_rejected([node], HostHandoffRejectionReason.MISSING_FIELD)


@pytest.mark.parametrize(
    "field,value",
    [("mode", 1), ("fingerprint", "A" * 64), ("fingerprint", "short")],
)
def test_rejects_invalid_field_type_or_digest_shape(field: str, value: object) -> None:
    payload = _payload()
    payload[field] = value
    node = _comment(payload)

    _assert_rejected([node], HostHandoffRejectionReason.INVALID_FIELD_TYPE)


def test_rejects_noncanonical_json() -> None:
    payload = _payload()
    text = json.dumps(payload, ensure_ascii=False)
    node = _comment(body=f"{MARKER}\n{text}\n\n{LABEL}")

    _assert_rejected([node], HostHandoffRejectionReason.NONCANONICAL_JSON)


def test_rejects_json_with_non_utf8_payload_text() -> None:
    payload = _payload(checkpoint="placeholder")
    payload["checkpoint"] = "\ud800"
    payload["fingerprint"] = "0" * 64
    text = json.dumps(payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
    node = _comment(body=f"{MARKER}\n{text}\n\n{LABEL}")

    _assert_rejected([node], HostHandoffRejectionReason.NONCANONICAL_JSON)


@pytest.mark.parametrize(
    "field,value,reason",
    [
        ("repository", "other/repo", HostHandoffRejectionReason.REPOSITORY_MISMATCH),
        ("repository", "malformed", HostHandoffRejectionReason.REPOSITORY_MISMATCH),
        ("target", "p0_implementation", HostHandoffRejectionReason.TARGET_MISMATCH),
        ("admission_role", "worker", HostHandoffRejectionReason.ROLE_MISMATCH),
        ("mode", "audit", HostHandoffRejectionReason.MODE_MISMATCH),
        ("supervisor_run_id", "older-run", HostHandoffRejectionReason.SUPERVISOR_RUN_MISMATCH),
        ("checkpoint", "older-checkpoint", HostHandoffRejectionReason.CHECKPOINT_MISMATCH),
    ],
)
def test_rejects_context_mismatch(
    field: str,
    value: str,
    reason: HostHandoffRejectionReason,
) -> None:
    _assert_rejected([_comment(_payload(**{field: value}))], reason)


def test_context_mismatch_order_is_independent_of_comment_order() -> None:
    repository_mismatch = _comment(_payload(repository="elsewhere/repo"))
    target_mismatch = _comment(_payload(target="other"))

    _assert_rejected(
        [repository_mismatch, target_mismatch],
        HostHandoffRejectionReason.REPOSITORY_MISMATCH,
    )


def test_rejects_copied_but_wrong_root_session_id() -> None:
    _assert_rejected(
        [_comment(_payload(host_root_session="copied-root-session"))],
        HostHandoffRejectionReason.WRONG_HOST_ROOT_SESSION,
    )


@pytest.mark.parametrize(
    "field,value",
    [
        ("issued_at", "2026-10-22T00:00:00+00:00"),
        ("issued_at", "2026-02-30T00:00:00Z"),
        ("issued_at", "２０２６-10-22T00:00:00Z"),
        ("issued_at", "yesterday"),
        ("expires_at", "2026-10-22T01:00:00.123+01:00"),
    ],
)
def test_rejects_invalid_payload_timestamp(field: str, value: str) -> None:
    _assert_rejected([_comment(_payload(**{field: value}))], HostHandoffRejectionReason.INVALID_TIMESTAMP)


def test_rejects_future_issue_time() -> None:
    _assert_rejected(
        [_comment(_payload(issued_at="2026-10-22T01:00:01Z"))],
        HostHandoffRejectionReason.FUTURE_ISSUED_AT,
    )


def test_expiry_at_now_is_stale() -> None:
    _assert_rejected(
        [_comment(_payload(expires_at="2026-10-22T01:00:00Z"))],
        HostHandoffRejectionReason.STALE_RECORD,
    )


def test_rejects_lifetime_longer_than_fifty_five_minutes() -> None:
    _assert_rejected(
        [_comment(_payload(expires_at="2026-10-22T01:55:01Z"))],
        HostHandoffRejectionReason.LIFETIME_EXCEEDED,
    )


def test_rejects_well_formed_but_incorrect_fingerprint() -> None:
    payload = _payload()
    payload["fingerprint"] = "0" * 64
    node = _comment(payload)

    _assert_rejected([node], HostHandoffRejectionReason.FINGERPRINT_MISMATCH)


@pytest.mark.parametrize(
    "comments,reason",
    [
        (
            [
                _comment(_payload(host_root_session="wrong")),
                _comment(lastEditedAt="2026-10-22T00:30:00Z"),
            ],
            HostHandoffRejectionReason.WRONG_HOST_ROOT_SESSION,
        ),
        (
            [
                _comment(),
                _comment(lastEditedAt="2026-10-22T00:30:00Z"),
            ],
            HostHandoffRejectionReason.EDITED_COMMENT,
        ),
        (
            [
                _comment(_payload(issued_at="2026-10-22T01:00:01Z")),
                _comment(_payload(expires_at="2026-10-22T01:00:00Z")),
            ],
            HostHandoffRejectionReason.FUTURE_ISSUED_AT,
        ),
        (
            [_comment(), _comment()],
            HostHandoffRejectionReason.MULTIPLE_MATCHING_RECORDS,
        ),
    ],
)
def test_matching_records_use_failure_precedence_and_reject_duplicates(
    comments: list[dict[str, object]],
    reason: HostHandoffRejectionReason,
) -> None:
    _assert_rejected(comments, reason)


def test_contradictory_matching_records_are_ambiguous() -> None:
    second = _payload(checkpoint="checkpoint-42")
    second["expires_at"] = "2026-10-22T01:04:00Z"
    unsigned = dict(second)
    unsigned.pop("fingerprint")
    second["fingerprint"] = hashlib.sha256(canonicalize_json(unsigned)).hexdigest()

    _assert_rejected([_comment(), _comment(second)], HostHandoffRejectionReason.MULTIPLE_MATCHING_RECORDS)


@pytest.mark.parametrize(
    "now",
    [
        datetime(2026, 10, 22, 1, 0),
        datetime(2026, 10, 22, 1, 0, tzinfo=timezone(timedelta(hours=1))),
    ],
)
def test_now_must_be_timezone_aware_utc(now: datetime) -> None:
    with pytest.raises(ValueError, match="timezone-aware UTC"):
        verify_host_handoff([], trusted_logins={"hostuser"}, expected=EXPECTED, now=now)


def test_expected_mapping_must_have_exact_string_fields() -> None:
    with pytest.raises(ValueError, match="expected"):
        verify_host_handoff(
            [_comment()],
            trusted_logins={"hostuser"},
            expected={"repository": "repo"},
            now=NOW,
        )


def test_trusted_logins_must_be_a_collection_not_a_string() -> None:
    with pytest.raises(ValueError, match="trusted_logins"):
        verify_host_handoff([], trusted_logins="hostuser", expected=EXPECTED, now=NOW)


def test_ignores_non_candidate_malformed_nodes_when_valid_record_exists() -> None:
    result = _verify([None, {"body": 42}, _comment()])

    assert result.accepted
