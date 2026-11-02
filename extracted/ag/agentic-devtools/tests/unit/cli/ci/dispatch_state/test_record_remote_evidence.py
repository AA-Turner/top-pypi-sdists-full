from pathlib import Path

import pytest

from agentic_devtools.cli.ci.dispatch_state import (
    DispatchIdentity,
    DispatchState,
    consume_task_creation_capability,
    create_intent,
    record_remote_evidence,
    transition_dispatch,
)

SHA = "a" * 40


def test_records_default_uncertain_event_for_marker_write(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = DispatchIdentity("repo", 7, SHA, 1)
    create_intent(path, identity)

    uncertain = record_remote_evidence(path, identity, reason="timeout", evidence={"op": "marker"})

    assert uncertain.state is DispatchState.NEEDS_RECONCILIATION
    assert uncertain.evidence["operation"] == "marker"


def test_records_explicit_reconciliation_evidence(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = DispatchIdentity("repo", 7, SHA, 1)
    create_intent(path, identity)
    transition_dispatch(path, identity, "marker_succeeded", marker_comment_id=3)
    creating = transition_dispatch(path, identity, "preparation_succeeded")
    consume_task_creation_capability(path, creating)
    transition_dispatch(path, identity, "task_uncertain", reason="timeout", evidence={"pages": 1})

    explicit = record_remote_evidence(
        path,
        identity,
        reason="still uncertain",
        evidence={"pages": 2},
        event="reconcile_incomplete",
    )

    assert explicit.state is DispatchState.NEEDS_RECONCILIATION
    assert explicit.evidence["operation"] == "task"


def test_rejects_conflicting_uncertain_operation(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = DispatchIdentity("repo", 7, SHA, 1)
    create_intent(path, identity)

    with pytest.raises(ValueError, match="does not match the uncertain operation"):
        record_remote_evidence(
            path,
            identity,
            reason="timeout",
            evidence={"operation": "marker"},
            event="task_uncertain",
        )


def test_rejects_conflicting_reconciliation_operation(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = DispatchIdentity("repo", 7, SHA, 1)
    create_intent(path, identity)
    record_remote_evidence(path, identity, reason="timeout", evidence={"pages": 1})

    with pytest.raises(ValueError, match="persisted uncertain operation"):
        record_remote_evidence(
            path,
            identity,
            reason="still uncertain",
            evidence={"operation": "task"},
            event="reconcile_incomplete",
        )


def test_raises_when_record_does_not_exist(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        record_remote_evidence(
            tmp_path / "dispatch.json",
            DispatchIdentity("repo", 7, SHA, 1),
            reason="missing",
            evidence={"operation": "task"},
        )
