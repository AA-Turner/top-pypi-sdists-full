from dataclasses import replace
from typing import Any, cast

import pytest

from agentic_devtools.cli.ci.dispatch_state import DispatchIdentity, DispatchRecord, DispatchState

SHA = "a" * 40


def test_validation_rejects_invalid_fields() -> None:
    identity = DispatchIdentity("repo", 7, SHA, 1)
    record = DispatchRecord.new(identity)
    invalid = [
        replace(record, repo="Repo"),
        replace(record, token="wrong"),
        replace(record, state=cast(Any, "intent")),
        replace(record, created_at=""),
        replace(record, updated_at=""),
        replace(record, attempt_capability=""),
        replace(record, attempt_capability_digest="not-a-digest"),
        replace(record, ordinal=4),
        replace(record, retry_count=True),
        replace(record, marker_comment_id=1),
        replace(record, task_id="task-1"),
        replace(record, marker_comment_id=0),
        replace(record, task_id="bad/id"),
        replace(record, reason=cast(Any, 123)),
        replace(record, reason="github_pat_aaaaaaaaaaaaaaaaaaaa"),
        replace(record, evidence=cast(Any, [])),
        replace(record, evidence={"prompt": "secret"}),
        replace(record, state=DispatchState.CREATING),
        replace(record, state=DispatchState.RESERVED, attempt_capability_digest="a" * 64),
        replace(record, state=DispatchState.RESERVED, marker_comment_id=1, task_id="task-1"),
        replace(record, state=DispatchState.CREATING, marker_comment_id=1, task_id="task-1"),
        replace(record, state=DispatchState.CREATED, marker_comment_id=1),
        replace(record, state=DispatchState.CREATED, marker_comment_id=1, task_id=cast(Any, 1)),
        replace(
            record,
            state=DispatchState.ABORTED_AFTER_FINAL_DISPATCH,
            marker_comment_id=1,
            task_id="task-1",
        ),
    ]
    for candidate in invalid:
        with pytest.raises(ValueError):
            candidate.validate()
    with pytest.raises(ValueError):
        replace(record, state=DispatchState.NEEDS_RECONCILIATION, reason="x").validate()
    with pytest.raises(ValueError):
        replace(
            record,
            state=DispatchState.NEEDS_RECONCILIATION,
            reason="x",
            evidence={"operation": "task"},
            task_id="task-1",
        ).validate()
    with pytest.raises(ValueError, match="evidence.operation"):
        replace(
            record,
            state=DispatchState.NEEDS_RECONCILIATION,
            reason="x",
            evidence={"operation": "other"},
        ).validate()
    with pytest.raises(ValueError, match="cannot persist marker_comment_id"):
        replace(
            record,
            state=DispatchState.NEEDS_RECONCILIATION,
            reason="x",
            evidence={"operation": "marker"},
            marker_comment_id=1,
        ).validate()
    with pytest.raises(ValueError, match="requires the persisted marker_comment_id"):
        replace(
            record,
            state=DispatchState.NEEDS_RECONCILIATION,
            reason="x",
            evidence={"operation": "task"},
        ).validate()
    with pytest.raises(ValueError, match="retry_count=4 is only valid"):
        replace(record, state=DispatchState.RESERVED, marker_comment_id=1, retry_count=4).validate()
    with pytest.raises(ValueError, match="retry_count cannot exceed"):
        replace(
            record, state=DispatchState.ABANDONED, reason="x", evidence={"operation": "dispatch"}, retry_count=5
        ).validate()


def test_with_state_bounds_and_redacts_evidence() -> None:
    class TokenLikeObject:
        def __str__(self) -> str:
            return "Bearer " + "abc123"

    identity = DispatchIdentity("repo", 7, SHA, 1)
    record = DispatchRecord.new(identity)
    updated = record.with_state(
        "needs_reconciliation",
        reason="timeout",
        evidence={
            "operation": "marker",
            "accessToken": "secret",
            "nested": {"api_key": "secret", "ok": "value"},
            "items": (1, object()),
            "message": "github_pat_aaaaaaaaaaaaaaaaaaaa",
            "error": TokenLikeObject(),
        },
    )
    assert "accessToken" not in updated.evidence
    assert updated.evidence["nested"] == {"ok": "value"}
    assert isinstance(updated.evidence["items"][1], str)
    assert updated.evidence["message"] == "[REDACTED]"
    assert updated.evidence["error"] == "[REDACTED]"
    bounded = record.with_state("needs_reconciliation", reason="x", evidence={"operation": "marker", "x": "y" * 5000})
    assert len(bounded.evidence["x"]) == 512


def test_with_state_bounds_and_redacts_reason() -> None:
    record = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))

    updated = record.with_state(
        "needs_reconciliation",
        reason="github_pat_aaaaaaaaaaaaaaaaaaaa " + ("x" * 600),
        evidence={"operation": "marker"},
    )

    assert updated.reason is not None
    assert updated.reason.startswith("[REDACTED]")
    assert "github_pat_" not in updated.reason
    assert len(updated.reason) == 512


def test_with_state_redacts_basic_authorization_credentials() -> None:
    record = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))

    updated = record.with_state(
        "needs_reconciliation",
        reason="Authorization: Basic dXNlcjpzZWNyZXQ=",
        evidence={"operation": "marker", "message": "Basic dXNlcjpzZWNyZXQ="},
    )

    assert updated.reason == "[REDACTED]"
    assert updated.evidence["message"] == "[REDACTED]"


def test_from_dict_rejects_unredacted_reason() -> None:
    record = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1)).with_state(
        "needs_reconciliation",
        reason="timeout",
        evidence={"operation": "marker"},
    )

    with pytest.raises(ValueError):
        DispatchRecord.from_dict({**record.to_dict(), "reason": "github_pat_aaaaaaaaaaaaaaaaaaaa"})


def test_from_dict_rejects_invalid_reconciliation_operation_and_marker_shape() -> None:
    record = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1)).with_state(
        "needs_reconciliation",
        reason="timeout",
        evidence={"operation": "task"},
        marker_comment_id=3,
    )

    with pytest.raises(ValueError):
        DispatchRecord.from_dict({**record.to_dict(), "evidence": {"operation": "other"}})
    with pytest.raises(ValueError):
        DispatchRecord.from_dict({**record.to_dict(), "marker_comment_id": None})
    with pytest.raises(ValueError):
        DispatchRecord.from_dict({**record.to_dict(), "evidence": {"operation": "marker"}})


def test_with_state_rejects_immutable_field_changes() -> None:
    record = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))
    for field_name, value in (
        ("repo", "other"),
        ("pull_request_id", 8),
        ("sha", "b" * 40),
        ("ordinal", 2),
        ("token", "wrong"),
        ("created_at", "now"),
    ):
        with pytest.raises(ValueError):
            record.with_state("intent", **{field_name: value})
