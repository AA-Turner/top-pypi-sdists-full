import pytest

from agentic_devtools.cli.ci.dispatch_state import DispatchIdentity, DispatchRecord, DispatchState, transition_record

SHA = "a" * 40


def test_requires_order_and_persists_task_before_link() -> None:
    record = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))

    with pytest.raises(ValueError):
        transition_record(record, "task_created", task_id="task-12")

    record = transition_record(record, "marker_succeeded", marker_comment_id=4)
    record = transition_record(record, "preparation_succeeded")
    record = record.with_state("creating", attempt_capability=None, attempt_capability_digest=None)
    record = transition_record(record, "task_created", task_id="task-12")

    assert transition_record(record, "link_succeeded").state is DispatchState.LINKED
    with pytest.raises(ValueError):
        transition_record(record, "task_created", task_id="task-13")


def test_requires_evidence_for_uncertain_and_abandoned_states() -> None:
    record = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))

    with pytest.raises(ValueError):
        transition_record(record, "marker_uncertain")
    with pytest.raises(ValueError):
        transition_record(record, "abandon")

    uncertain = transition_record(
        record,
        "marker_uncertain",
        reason="timeout",
        evidence={"operation": "marker"},
    )
    assert uncertain.state is DispatchState.NEEDS_RECONCILIATION
    abandoned = transition_record(
        record,
        "abandon",
        reason="operator",
        evidence={"operation": "dispatch"},
    )
    assert abandoned.state is DispatchState.ABANDONED


def test_abandon_rejects_new_remote_identifiers_not_already_persisted() -> None:
    record = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))

    with pytest.raises(ValueError, match="abandonment cannot introduce or change marker_comment_id"):
        transition_record(
            record,
            "abandon",
            marker_comment_id=9,
            reason="operator",
            evidence={"operation": "dispatch"},
        )
    with pytest.raises(ValueError, match="abandonment cannot introduce or change task_id"):
        transition_record(
            record,
            "abandon",
            task_id="task-1",
            reason="operator",
            evidence={"operation": "dispatch"},
        )


def test_uses_operation_aware_reconciliation_targets() -> None:
    marker_uncertain = transition_record(
        DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1)),
        "marker_uncertain",
        reason="timeout",
        evidence={"pages": 1},
    )
    with pytest.raises(ValueError):
        transition_record(marker_uncertain, "reconcile_unique", task_id="task-1")
    reserved = transition_record(marker_uncertain, "reconcile_unique", marker_comment_id=9)
    assert reserved.state is DispatchState.RESERVED
    assert reserved.marker_comment_id == 9
    assert transition_record(marker_uncertain, "reconcile_miss").state is DispatchState.INTENT

    uncertain_task_record = transition_record(
        transition_record(
            transition_record(
                DispatchRecord.new(DispatchIdentity("repo", 7, "b" * 40, 1)),
                "marker_succeeded",
                marker_comment_id=4,
            ),
            "preparation_succeeded",
        ).with_state("creating", attempt_capability=None, attempt_capability_digest=None),
        "task_uncertain",
        reason="timeout",
        evidence={"pages": 1},
    )
    task_uncertain = transition_record(
        uncertain_task_record,
        "reconcile_unique",
        task_id="task-2",
    )
    assert task_uncertain.state is DispatchState.CREATED
    with pytest.raises(ValueError):
        transition_record(uncertain_task_record, "reconcile_marker_miss")


def test_preserves_retry_count_after_preparation_succeeds() -> None:
    record = transition_record(
        DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1)),
        "marker_succeeded",
        marker_comment_id=4,
    )
    record = transition_record(record, "pre_write_failure")
    assert record.retry_count == 1

    record = transition_record(record, "preparation_succeeded")

    assert record.state is DispatchState.CREATING
    assert record.retry_count == 1


def test_preserves_marker_intent_across_pre_write_failures() -> None:
    record = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))

    for retry_count in range(1, 4):
        record = transition_record(record, "pre_write_failure")
        assert record.state is DispatchState.INTENT
        assert record.retry_count == retry_count

    terminal = transition_record(record, "pre_write_failure")

    assert terminal.state is DispatchState.ABANDONED
    assert terminal.retry_count == 4
    assert terminal.reason == "pre-write retry exhaustion"
    assert terminal.evidence == {"operation": "pre-write", "retry_count": 4}


def test_resets_retry_count_after_reconciled_miss_breaks_the_failure_streak() -> None:
    marker_record = transition_record(DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1)), "pre_write_failure")
    marker_uncertain = transition_record(
        marker_record,
        "marker_uncertain",
        reason="timeout",
        evidence={"pages": 1},
    )
    marker_reset = transition_record(marker_uncertain, "reconcile_marker_miss")

    assert marker_reset.state is DispatchState.INTENT
    assert marker_reset.retry_count == 0
    assert transition_record(marker_reset, "pre_write_failure").retry_count == 1

    task_record = transition_record(marker_reset, "marker_succeeded", marker_comment_id=4)
    task_record = transition_record(task_record, "pre_write_failure")
    task_uncertain = transition_record(
        transition_record(task_record, "preparation_succeeded").with_state(
            "creating",
            attempt_capability=None,
            attempt_capability_digest=None,
        ),
        "task_uncertain",
        reason="timeout",
        evidence={"pages": 1},
    )
    task_reset = transition_record(task_uncertain, "reconcile_task_miss")

    assert task_reset.state is DispatchState.RESERVED
    assert task_reset.retry_count == 0
    assert transition_record(task_reset, "pre_write_failure").retry_count == 1


def test_rejects_retry_count_override_outside_pre_write_failure() -> None:
    record = transition_record(
        DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1)),
        "marker_succeeded",
        marker_comment_id=4,
    )
    record = transition_record(record, "pre_write_failure")

    with pytest.raises(ValueError, match="retry_count"):
        transition_record(record, "preparation_succeeded", retry_count=0)


def test_allows_redundant_retry_count_on_non_retry_transition() -> None:
    record = transition_record(
        DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1)),
        "marker_succeeded",
        marker_comment_id=4,
    )
    record = transition_record(record, "pre_write_failure")

    creating = transition_record(record, "preparation_succeeded", retry_count=1)

    assert creating.state is DispatchState.CREATING
    assert creating.retry_count == 1


def test_returns_to_reserved_after_pre_write_failure_from_creating() -> None:
    record = transition_record(
        transition_record(
            DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1)),
            "marker_succeeded",
            marker_comment_id=4,
        ),
        "preparation_succeeded",
    )

    recovered = transition_record(record, "pre_write_failure")

    assert recovered.state is DispatchState.RESERVED
    assert recovered.marker_comment_id == 4
    assert recovered.retry_count == 1


def test_rejects_pre_write_failure_after_creation_capability_consumption() -> None:
    creating = transition_record(
        transition_record(
            DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1)),
            "marker_succeeded",
            marker_comment_id=4,
        ),
        "preparation_succeeded",
    )
    consumed = creating.with_state(
        "creating",
        attempt_capability=creating.attempt_capability,
        attempt_capability_digest=None,
    )

    with pytest.raises(ValueError, match="capability consumption"):
        transition_record(consumed, "pre_write_failure")


def test_rejects_replay_state_changes() -> None:
    created = transition_record(
        transition_record(
            transition_record(
                DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1)),
                "marker_succeeded",
                marker_comment_id=4,
            ),
            "preparation_succeeded",
        ).with_state("creating", attempt_capability=None, attempt_capability_digest=None),
        "task_created",
        task_id="task-1",
    )

    with pytest.raises(ValueError, match="replay cannot include state changes"):
        transition_record(created, "replay", task_id="task-2")


def test_supports_recovery_and_terminal_transitions() -> None:
    record = DispatchRecord.new(DispatchIdentity("repo", 7, "d" * 40, 1))
    record = transition_record(record, "marker_success", marker_comment_id=3)
    record = transition_record(record, "pre_write_failure")
    record = transition_record(record, "preparation_succeeded")
    record = record.with_state("creating", attempt_capability=None, attempt_capability_digest=None)
    created = transition_record(record, "task_success", task_id="task-1")
    linked = transition_record(created, "link_exists")

    assert transition_record(linked, "downstream_success").state is DispatchState.SUCCEEDED
    assert transition_record(linked, "replay") == linked
    assert transition_record(created, "link_failed").state is DispatchState.CREATED
    assert transition_record(created, "link_success").state is DispatchState.LINKED
    with pytest.raises(ValueError):
        transition_record(
            transition_record(created, "link_success"),
            "final_dispatch",
        )


def test_rejects_remote_identifier_mutation_after_persistence() -> None:
    record = DispatchRecord.new(DispatchIdentity("repo", 7, "c" * 40, 1))
    record = transition_record(record, "marker_success", marker_comment_id=3)
    record = transition_record(record, "preparation_succeeded")
    record = record.with_state("creating", attempt_capability=None, attempt_capability_digest=None)
    created = transition_record(record, "task_success", task_id="task-1")

    with pytest.raises(ValueError):
        transition_record(created, "link_success", task_id="task-2")
    linked = transition_record(created, "link_success")
    with pytest.raises(ValueError):
        transition_record(linked, "downstream_success", marker_comment_id=4)


def test_allows_final_dispatch_only_for_third_ordinal() -> None:
    record = DispatchRecord.new(DispatchIdentity("repo", 7, "e" * 40, 3))
    record = transition_record(record, "marker_success", marker_comment_id=3)
    record = transition_record(record, "preparation_succeeded")
    record = record.with_state("creating", attempt_capability=None, attempt_capability_digest=None)
    record = transition_record(record, "task_success", task_id="task-1")
    linked = transition_record(record, "link_success")

    assert transition_record(linked, "final_dispatch").state is DispatchState.ABORTED_AFTER_FINAL_DISPATCH


def test_abandons_after_four_pre_write_failures() -> None:
    record = transition_record(
        DispatchRecord.new(DispatchIdentity("repo", 7, "f" * 40, 1)),
        "marker_succeeded",
        marker_comment_id=4,
    )
    for _ in range(3):
        record = transition_record(record, "preparation_succeeded")
        record = transition_record(record, "pre_write_failure")
        assert record.state is DispatchState.RESERVED

    record = transition_record(record, "preparation_succeeded")
    terminal = transition_record(record, "pre_write_failure")

    assert terminal.state is DispatchState.ABANDONED


def test_rejects_task_results_before_creation_capability_consumption() -> None:
    creating = transition_record(
        transition_record(
            DispatchRecord.new(DispatchIdentity("repo", 7, "d" * 40, 1)),
            "marker_succeeded",
            marker_comment_id=4,
        ),
        "preparation_succeeded",
    )

    for event in ("task_created", "task_success", "task_uncertain"):
        with pytest.raises(ValueError, match="capability consumption"):
            transition_record(
                creating,
                event,
                task_id="task-1" if event != "task_uncertain" else None,
                reason="timeout" if event == "task_uncertain" else None,
                evidence={"operation": "task"} if event == "task_uncertain" else None,
            )
