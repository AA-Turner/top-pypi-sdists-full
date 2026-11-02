import json
from pathlib import Path

import pytest

from agentic_devtools.cli.ci import dispatch_state as dispatch_state_module
from agentic_devtools.cli.ci.dispatch_state import (
    DispatchIdentity,
    DispatchRecord,
    consume_task_creation_capability,
    save_dispatch_record_atomic,
    transition_dispatch,
    transition_record,
)

SHA = "a" * 40


def _creating_record(record: DispatchRecord) -> DispatchRecord:
    return transition_record(record, "preparation_succeeded", attempt_capability="local-capability")


def test_writes_atomic_payload_with_records_wrapper(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    record = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))

    save_dispatch_record_atomic(path, record)

    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["version"] == 1
    assert payload["records"][record.identity.key]["token"] == record.token


def test_allows_replay_of_same_state_record(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    record = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))
    save_dispatch_record_atomic(path, record)

    save_dispatch_record_atomic(path, DispatchRecord.from_dict(record.to_dict()))


def test_rejects_stale_same_state_record(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    intent = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))
    save_dispatch_record_atomic(path, intent)
    record = intent.with_state("reserved", marker_comment_id=3)
    save_dispatch_record_atomic(path, record)
    transition_dispatch(path, record.identity, "pre_write_failure")

    with pytest.raises(ValueError, match="stale"):
        save_dispatch_record_atomic(path, record)


def test_allows_legal_same_state_transition_payloads(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    intent = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))
    save_dispatch_record_atomic(path, intent)
    reserved = intent.with_state("reserved", marker_comment_id=3)
    save_dispatch_record_atomic(path, reserved)

    retry_incremented = transition_record(reserved, "pre_write_failure")
    save_dispatch_record_atomic(path, retry_incremented)

    persisted = DispatchRecord.from_dict(json.loads(path.read_text(encoding="utf-8"))["records"][reserved.identity.key])
    assert persisted.state.value == "reserved"
    assert persisted.retry_count == 1


def test_rejects_new_non_intent_and_fourth_ordinal(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    reserved = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1)).with_state("reserved", marker_comment_id=3)
    with pytest.raises(ValueError):
        save_dispatch_record_atomic(path, reserved)
    with pytest.raises(ValueError):
        save_dispatch_record_atomic(path, DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 4)))


def test_rejects_state_rollback_for_existing_record(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    intent = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))
    save_dispatch_record_atomic(path, intent)
    reserved = intent.with_state("reserved", marker_comment_id=4)
    save_dispatch_record_atomic(path, reserved)
    creating = _creating_record(reserved)
    save_dispatch_record_atomic(path, creating)
    created = consume_task_creation_capability(path, creating).with_state("created", task_id="task-9")
    save_dispatch_record_atomic(path, created)

    stale_intent = DispatchRecord.from_dict({**created.to_dict(), "state": "reserved", "task_id": None})
    with pytest.raises(ValueError):
        save_dispatch_record_atomic(path, stale_intent)


def test_rejects_state_skip_and_allows_legal_reconciliation_recovery(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    intent = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))
    save_dispatch_record_atomic(path, intent)
    skipped = (
        _creating_record(intent.with_state("reserved", marker_comment_id=4))
        .with_state(
            "creating",
            attempt_capability=None,
            attempt_capability_digest=None,
        )
        .with_state(
            "created",
            task_id="task-9",
        )
    )
    with pytest.raises(ValueError):
        save_dispatch_record_atomic(path, skipped)

    uncertain = intent.with_state(
        "needs_reconciliation",
        reason="uncertain marker write",
        evidence={"operation": "marker", "message": "timeout"},
    )
    save_dispatch_record_atomic(path, uncertain)
    recovered = uncertain.with_state("reserved", marker_comment_id=4, reason=None, evidence={})
    save_dispatch_record_atomic(path, recovered)


def test_rejects_reconciliation_write_that_conflicts_with_persisted_operation(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    intent = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))
    save_dispatch_record_atomic(path, intent)
    reserved = intent.with_state("reserved", marker_comment_id=4)
    save_dispatch_record_atomic(path, reserved)
    creating = _creating_record(reserved)
    save_dispatch_record_atomic(path, creating)
    uncertain_task = consume_task_creation_capability(path, creating).with_state(
        "needs_reconciliation",
        reason="uncertain task write",
        evidence={"operation": "task", "message": "timeout"},
    )
    save_dispatch_record_atomic(path, uncertain_task)

    stale_intent = DispatchRecord.from_dict(
        {**uncertain_task.to_dict(), "state": "reserved", "reason": None, "evidence": {"operation": "marker"}}
    )
    with pytest.raises(ValueError, match="illegal state transition"):
        save_dispatch_record_atomic(path, stale_intent)


def test_checks_equivalent_events_until_payload_matches(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = tmp_path / "dispatch.json"
    intent = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))
    save_dispatch_record_atomic(path, intent)
    reserved = intent.with_state("reserved", marker_comment_id=4)
    transition_calls: list[str] = []
    original_transition_record = dispatch_state_module.transition_record

    def fake_transition_record(record: DispatchRecord, event: str, **changes: object) -> DispatchRecord:
        transition_calls.append(event)
        if event == "marker_succeeded":
            return original_transition_record(record, event, marker_comment_id=99)
        return original_transition_record(record, event, **changes)

    monkeypatch.setattr(dispatch_state_module, "transition_record", fake_transition_record)

    save_dispatch_record_atomic(path, reserved)

    assert transition_calls[:2] == ["marker_succeeded", "marker_success"]


def test_allows_task_reconciliation_miss_recovery(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    intent = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))
    save_dispatch_record_atomic(path, intent)
    reserved = intent.with_state("reserved", marker_comment_id=4)
    save_dispatch_record_atomic(path, reserved)
    creating = _creating_record(reserved)
    save_dispatch_record_atomic(path, creating)
    uncertain_task = consume_task_creation_capability(path, creating).with_state(
        "needs_reconciliation",
        reason="uncertain task write",
        evidence={"operation": "task", "message": "timeout"},
    )
    save_dispatch_record_atomic(path, uncertain_task)

    recovered = DispatchRecord.from_dict(
        {**uncertain_task.to_dict(), "state": "reserved", "reason": None, "evidence": {}}
    )
    save_dispatch_record_atomic(path, recovered)


def test_rejects_remote_identifier_mutation_for_existing_record(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    intent = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))
    save_dispatch_record_atomic(path, intent)
    reserved = intent.with_state("reserved", marker_comment_id=4)
    save_dispatch_record_atomic(path, reserved)
    creating = _creating_record(reserved)
    save_dispatch_record_atomic(path, creating)
    created = consume_task_creation_capability(path, creating).with_state("created", task_id="task-9")
    save_dispatch_record_atomic(path, created)

    mutated_task = DispatchRecord.from_dict({**created.to_dict(), "task_id": "task-10", "state": "linked"})
    with pytest.raises(ValueError):
        save_dispatch_record_atomic(path, mutated_task)
    mutated_marker = DispatchRecord.from_dict({**created.to_dict(), "marker_comment_id": 5, "state": "linked"})
    with pytest.raises(ValueError):
        save_dispatch_record_atomic(path, mutated_marker)


def test_rejects_out_of_order_new_insertions(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    first = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))
    save_dispatch_record_atomic(path, first)
    first_terminal = first.with_state("abandoned", reason="done", evidence={"operation": "dispatch"})
    save_dispatch_record_atomic(path, first_terminal)
    with pytest.raises(ValueError):
        save_dispatch_record_atomic(path, DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 3)))


def test_rejects_new_insert_when_previous_ordinal_is_unresolved(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    first = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))
    save_dispatch_record_atomic(path, first)
    with pytest.raises(ValueError):
        save_dispatch_record_atomic(path, DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 2)))
