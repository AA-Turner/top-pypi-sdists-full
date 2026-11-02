"""Tests for the SupervisionControl symbol."""

from __future__ import annotations

import hashlib
import json

import pytest

from agentic_devtools.cli.ci.supervision_control import (
    CONTROL_MARKER,
    IGNORE_LABEL,
    SUPERVISED_LABEL,
    Checkpoint,
    ControlError,
    HoldReceipt,
    PRObservation,
    QuarantineReceipt,
    SupervisionControl,
)


def _observation(number: int, head: str, *labels: str) -> PRObservation:
    return PRObservation(number, head, frozenset(labels))


def test_quarantine_is_head_guarded_and_idempotent() -> None:
    control = SupervisionControl()
    observations = [_observation(7, "head-7"), _observation(8, "head-8", SUPERVISED_LABEL)]

    result = control.quarantine(observations, {7: "head-7", 8: "head-8"}, run_id="run-1")

    assert result is not None
    expected_heads = json.dumps(sorted({7: "head-7", 8: "head-8"}.items()), separators=(",", ":"))
    assert result.idempotency_key == f"run-1:quarantine:{hashlib.sha256(expected_heads.encode()).hexdigest()}"
    assert result.changed == (7, 8)
    assert result.labels[7] == frozenset({IGNORE_LABEL, SUPERVISED_LABEL})
    assert result.labels[8] == frozenset({IGNORE_LABEL, SUPERVISED_LABEL})
    retry = control.quarantine(
        [
            _observation(7, "head-7", IGNORE_LABEL, SUPERVISED_LABEL),
            _observation(8, "head-8", SUPERVISED_LABEL),
        ],
        {7: "head-7", 8: "head-8"},
        run_id="run-1",
    )
    assert retry is not None
    assert retry.changed == (8,)
    assert retry.idempotency_key == result.idempotency_key
    with pytest.raises(ControlError, match="stale"):
        control.quarantine(observations, {7: "different"}, run_id="run-1")


def test_restore_requires_matching_checkpoint_ownership() -> None:
    control = SupervisionControl()
    checkpoint = control.quarantine((_observation(7, "head-7"),), {7: "head-7"}, run_id="run-1")
    assert checkpoint is not None

    restored = control.restore_prs(
        (_observation(7, "head-7", IGNORE_LABEL, SUPERVISED_LABEL),),
        checkpoint.receipt,
    )

    assert restored.changed == (7,)
    assert restored.labels[7] == frozenset({SUPERVISED_LABEL})
    noop = control.restore_prs(
        (_observation(7, "head-7", IGNORE_LABEL, SUPERVISED_LABEL),),
        QuarantineReceipt("other", (), {}),
    )
    assert noop.changed == ()
    assert noop.labels == {}


def test_quarantine_only_records_ignore_added_when_it_was_previously_absent() -> None:
    control = SupervisionControl()
    # PR 7 already carries the ignore label (pre-existing/user-owned); quarantine
    # only needs to add SUPERVISED_LABEL for it.
    result = control.quarantine(
        (_observation(7, "head-7", IGNORE_LABEL),),
        {7: "head-7"},
        run_id="run-1",
    )

    assert result is not None
    assert result.changed == (7,)
    assert result.receipt.ignore_added == ()


def test_restore_never_removes_a_pre_existing_ignore_label() -> None:
    control = SupervisionControl()
    result = control.quarantine(
        (_observation(7, "head-7", IGNORE_LABEL),),
        {7: "head-7"},
        run_id="run-1",
    )
    assert result is not None

    restored = control.restore_prs(
        (_observation(7, "head-7", IGNORE_LABEL, SUPERVISED_LABEL),),
        result.receipt,
    )

    assert restored.changed == ()
    assert restored.labels == {}


def test_restore_is_a_full_noop_after_fully_idempotent_quarantine() -> None:
    control = SupervisionControl()
    already_quarantined = _observation(7, "head-7", IGNORE_LABEL, SUPERVISED_LABEL)
    assert control.quarantine((already_quarantined,), {7: "head-7"}, run_id="run-1") is None
    synthesized_receipt = QuarantineReceipt("run-1", (), {7: "head-7"}, ())

    restored = control.restore_prs((already_quarantined,), synthesized_receipt)

    assert restored.changed == ()
    assert restored.labels == {}


@pytest.mark.parametrize(
    "observations",
    [
        (_observation(7, "head-moved", IGNORE_LABEL),),
        (),
    ],
    ids=("stale-head", "missing-head"),
)
def test_restore_rejects_stale_or_missing_heads_for_noop_receipts(
    observations: tuple[PRObservation, ...],
) -> None:
    receipt = QuarantineReceipt("run-1", (), {7: "head-7"}, ())

    with pytest.raises(ControlError, match="stale or missing head"):
        SupervisionControl().restore_prs(observations, receipt)


def test_restore_skips_owned_pr_with_no_recorded_head() -> None:
    control = SupervisionControl()
    receipt = QuarantineReceipt("run-1", (7,), {}, (7,))

    with pytest.raises(ControlError, match="does not own any observed PR"):
        control.restore_prs((_observation(7, "head-7", IGNORE_LABEL),), receipt)


def test_restore_rejects_missing_owned_pr_observations() -> None:
    control = SupervisionControl()
    receipt = QuarantineReceipt("run-1", (7, 8), {7: "head-7", 8: "head-8"}, (7, 8))

    with pytest.raises(ControlError, match="missing owned PR observations: \\[8\\]"):
        control.restore_prs((_observation(7, "head-7", IGNORE_LABEL),), receipt)


def test_hold_and_resume_preserve_exact_workflow_receipt() -> None:
    control = SupervisionControl()
    result = control.hold({"loop.yml": True, "watchdog.yml": False}, run_id="run-2")

    assert result is not None
    assert result.idempotency_key == "run-2:hold"
    retry = control.hold({"loop.yml": False, "watchdog.yml": True}, run_id="run-2")
    assert retry is not None
    assert retry.receipt.changed_workflows == ("watchdog.yml",)
    assert retry.idempotency_key == result.idempotency_key
    assert result.receipt == HoldReceipt(
        run_id="run-2",
        changed_workflows=("loop.yml",),
        previous_states={"loop.yml": True, "watchdog.yml": False},
    )
    assert control.resume({"loop.yml": False, "watchdog.yml": False}, result.receipt) == {
        "loop.yml": True,
        "watchdog.yml": False,
    }
    with pytest.raises(ControlError, match="watchdog.yml"):
        control.resume({"loop.yml": False}, result.receipt)


def test_resume_allows_already_restored_workflows_after_partial_failure() -> None:
    control = SupervisionControl()
    result = control.hold({"first.yml": True, "second.yml": True, "disabled.yml": False}, run_id="run-2")
    assert result is not None

    assert control.resume(
        {"first.yml": True, "second.yml": False, "disabled.yml": False},
        result.receipt,
    ) == {"first.yml": True, "second.yml": True, "disabled.yml": False}


def test_resume_rejects_receipt_with_inconsistent_changed_workflows() -> None:
    control = SupervisionControl()
    receipt = HoldReceipt("run-2", ("disabled.yml",), {"disabled.yml": False})

    with pytest.raises(ControlError, match="changed workflows"):
        control.resume({"disabled.yml": False}, receipt)


def test_resume_rejects_any_workflow_enabled_during_the_hold() -> None:
    control = SupervisionControl()
    result = control.hold({"loop.yml": True, "watchdog.yml": False}, run_id="run-2")
    assert result is not None

    with pytest.raises(ControlError, match="watchdog.yml"):
        control.resume({"loop.yml": False, "watchdog.yml": True}, result.receipt)


def test_hold_is_idempotent_when_everything_is_already_disabled() -> None:
    control = SupervisionControl()
    assert control.hold({"loop.yml": False, "watchdog.yml": False}, run_id="run-9") is None


def test_checkpoint_is_compact_and_idempotent() -> None:
    control = SupervisionControl()
    checkpoint = Checkpoint(
        "run-3",
        {"selected": [7], "deferred": [8], "terminal_reason": "deadline"},
        "repo",
    )

    encoded = control.encode_checkpoint(checkpoint)
    assert encoded.startswith(CONTROL_MARKER)
    assert json.loads(encoded.split("\n", 1)[1])["run_id"] == "run-3"
    assert control.decode_checkpoint(encoded) == checkpoint
    assert control.decode_checkpoint(encoded) == control.decode_checkpoint(encoded)
    with pytest.raises(ControlError, match="marker"):
        control.decode_checkpoint("{}")


def test_decode_checkpoint_rejects_malformed_terminal_label() -> None:
    control = SupervisionControl()
    encoded = control.encode_checkpoint(Checkpoint("run-3", {"step": 1}, "repo"))

    with pytest.raises(ControlError, match="terminal label is malformed"):
        control.decode_checkpoint(f"{encoded}\n🤖 AI PR Loop ·")


def test_healthy_queue_only_checkpoints() -> None:
    control = SupervisionControl()

    checkpoint = Checkpoint("healthy-run", {"selected": [1], "mutations": []}, "repo")

    assert control.decode_checkpoint(control.encode_checkpoint(checkpoint)) == checkpoint


def test_localized_defect_quarantines_only_affected_pr() -> None:
    control = SupervisionControl()
    observations = [
        PRObservation(1, "head-1", frozenset()),
        PRObservation(2, "head-2", frozenset()),
    ]

    result = control.quarantine((observations[0],), {1: "head-1"}, run_id="localized-run")

    assert result is not None
    assert result.changed == (1,)
    assert result.labels[1] == frozenset({IGNORE_LABEL, SUPERVISED_LABEL})
    assert 2 not in result.labels


def test_systemic_defect_holds_and_restores_exact_workflows() -> None:
    control = SupervisionControl()
    result = control.hold({"ai-pr-loop.yml": True, "ai-pr-loop-watchdog.yml": True}, run_id="systemic-run")

    assert result is not None
    receipt = result.receipt
    assert receipt.changed_workflows == ("ai-pr-loop-watchdog.yml", "ai-pr-loop.yml")
    assert control.resume({"ai-pr-loop.yml": False, "ai-pr-loop-watchdog.yml": False}, receipt) == {
        "ai-pr-loop.yml": True,
        "ai-pr-loop-watchdog.yml": True,
    }


def test_quarantine_requires_run_id_and_observations() -> None:
    control = SupervisionControl()
    with pytest.raises(ControlError, match="run_id"):
        control.quarantine((_observation(7, "head-7"),), {7: "head-7"}, run_id=" ")
    with pytest.raises(ControlError, match="at least one PR"):
        control.quarantine((), {}, run_id="run-1")


def test_quarantine_is_idempotent_when_labels_already_applied() -> None:
    control = SupervisionControl()
    observation = _observation(7, "head-7", IGNORE_LABEL, SUPERVISED_LABEL)

    assert control.quarantine((observation,), {7: "head-7"}, run_id="run-1") is None


def test_restore_requires_receipt_run_id() -> None:
    control = SupervisionControl()
    with pytest.raises(ControlError, match="run ID"):
        control.restore_prs((), QuarantineReceipt(" ", (), {}))


def test_restore_skips_prs_not_owned_by_the_receipt() -> None:
    control = SupervisionControl()
    checkpoint = control.quarantine((_observation(7, "head-7"),), {7: "head-7"}, run_id="run-1")
    assert checkpoint is not None
    unowned = _observation(9, "head-9", IGNORE_LABEL)

    with pytest.raises(ControlError, match="does not own"):
        control.restore_prs((unowned,), checkpoint.receipt)


def test_restore_is_idempotent_when_ignore_label_already_absent() -> None:
    control = SupervisionControl()
    checkpoint = control.quarantine((_observation(7, "head-7"),), {7: "head-7"}, run_id="run-1")
    assert checkpoint is not None

    restored = control.restore_prs(
        (_observation(7, "head-7", SUPERVISED_LABEL),),
        checkpoint.receipt,
    )

    assert restored.changed == ()
    assert restored.labels[7] == frozenset({SUPERVISED_LABEL})


def test_restore_rejects_stale_head() -> None:
    control = SupervisionControl()
    checkpoint = control.quarantine((_observation(7, "head-7"),), {7: "head-7"}, run_id="run-1")
    assert checkpoint is not None

    with pytest.raises(ControlError, match="stale head"):
        control.restore_prs(
            (_observation(7, "moved", IGNORE_LABEL, SUPERVISED_LABEL),),
            checkpoint.receipt,
        )


def test_hold_requires_run_id_and_non_empty_states() -> None:
    control = SupervisionControl()
    with pytest.raises(ControlError, match="run_id and workflow states"):
        control.hold({}, run_id="run-1")
    with pytest.raises(ControlError, match="run_id and workflow states"):
        control.hold({"loop.yml": True}, run_id=" ")


def test_hold_rejects_non_string_workflow_names() -> None:
    control = SupervisionControl()
    with pytest.raises(ControlError, match="non-empty strings"):
        control.hold({"": True}, run_id="run-1")


def test_hold_rejects_non_boolean_workflow_states() -> None:
    control = SupervisionControl()
    with pytest.raises(ControlError, match="must be boolean"):
        control.hold({"loop.yml": 1}, run_id="run-1")  # type: ignore[dict-item]


def test_resume_requires_receipt_run_id() -> None:
    control = SupervisionControl()
    with pytest.raises(ControlError, match="run ID"):
        control.resume({}, HoldReceipt(" ", (), {}))


def test_encode_checkpoint_requires_run_id_and_repository() -> None:
    control = SupervisionControl()
    with pytest.raises(ControlError, match="run ID and repository"):
        control.encode_checkpoint(Checkpoint(" ", {}, "repo"))
    with pytest.raises(ControlError, match="run ID and repository"):
        control.encode_checkpoint(Checkpoint("run-1", {}, " "))


def test_decode_checkpoint_rejects_invalid_json() -> None:
    control = SupervisionControl()
    with pytest.raises(ControlError, match="JSON is invalid"):
        control.decode_checkpoint(f"{CONTROL_MARKER}\nnot-json")


def test_decode_checkpoint_rejects_non_dict_payload() -> None:
    control = SupervisionControl()
    with pytest.raises(ControlError, match="payload is invalid"):
        control.decode_checkpoint(f"{CONTROL_MARKER}\n" + json.dumps({"payload": "not-a-dict"}))


def test_decode_checkpoint_rejects_incomplete_identity() -> None:
    control = SupervisionControl()
    body = {"payload": {}, "run_id": "run-1", "repository": "", "evidence_fingerprint": "x"}
    with pytest.raises(ControlError, match="identity is incomplete"):
        control.decode_checkpoint(f"{CONTROL_MARKER}\n" + json.dumps(body))


def test_decode_checkpoint_rejects_fingerprint_mismatch() -> None:
    control = SupervisionControl()
    body = {
        "payload": {},
        "run_id": "run-1",
        "repository": "repo",
        "evidence_fingerprint": "wrong",
    }
    with pytest.raises(ControlError, match="fingerprint mismatch"):
        control.decode_checkpoint(f"{CONTROL_MARKER}\n" + json.dumps(body))
