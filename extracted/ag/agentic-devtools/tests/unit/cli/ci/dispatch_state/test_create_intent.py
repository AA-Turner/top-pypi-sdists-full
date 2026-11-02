from pathlib import Path

import pytest

from agentic_devtools.cli.ci.dispatch_state import (
    DispatchIdentity,
    DispatchState,
    create_intent,
    load_dispatch_record,
    save_dispatch_record_atomic,
    transition_dispatch,
    transition_record,
)

SHA = "a" * 40


def test_round_trips_and_uses_canonical_key(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = DispatchIdentity("Repo-Name", 7, SHA, 1)

    record = create_intent(path, identity)

    assert record.state is DispatchState.INTENT
    assert record.token == f"agdt-dispatch-repo-name-7-{SHA}-1"
    assert load_dispatch_record(path, identity) == record


def test_is_idempotent_and_enforces_order_and_limit(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = DispatchIdentity("repo", 7, SHA, 1)
    first = create_intent(path, identity)
    replayed = create_intent(path, identity)
    assert first.state is DispatchState.INTENT
    assert replayed.state is DispatchState.NEEDS_RECONCILIATION
    assert replayed.reason == "replayed intent requires marker reconciliation"
    assert replayed.evidence == {"operation": "marker", "source": "create_intent_replay"}
    assert load_dispatch_record(path, identity) == replayed
    with pytest.raises(ValueError):
        create_intent(path, DispatchIdentity("repo", 7, SHA, 3))
    recovered = transition_dispatch(path, identity, "reconcile_marker_miss")
    assert recovered.state is DispatchState.INTENT

    abandoned = transition_dispatch(
        path,
        identity,
        "abandon",
        reason="operator",
        evidence={"operation": "dispatch"},
    )
    assert abandoned.state is DispatchState.ABANDONED
    second = create_intent(path, DispatchIdentity("repo", 7, SHA, 2))
    second = transition_record(
        second,
        "abandon",
        reason="operator",
        evidence={"operation": "dispatch"},
    )
    save_dispatch_record_atomic(path, second)
    third = create_intent(path, DispatchIdentity("repo", 7, SHA, 3))
    with pytest.raises(ValueError):
        create_intent(path, DispatchIdentity("repo", 7, SHA, 4))
    third = transition_record(
        third,
        "abandon",
        reason="operator",
        evidence={"operation": "dispatch"},
    )
    save_dispatch_record_atomic(path, third)
    assert create_intent(path, DispatchIdentity("repo", 7, SHA, 3)) == third

    ordered_path = tmp_path / "ordered.json"
    ordered_identity = DispatchIdentity("repo", 7, "1" * 40, 1)
    ordered = create_intent(ordered_path, ordered_identity)
    ordered = transition_record(ordered, "abandon", reason="operator", evidence={"operation": "dispatch"})
    save_dispatch_record_atomic(ordered_path, ordered)
    with pytest.raises(ValueError):
        create_intent(ordered_path, DispatchIdentity("repo", 7, "1" * 40, 3))
