"""Forcing tests for the opt-in atomic bounded-backlog persistence primitive."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime, timedelta

import pytest

import matrx_scheduler
from matrx_scheduler.backlog import BACKLOG_REARM_METADATA_KEY, BacklogRearmRequest


ACTOR_ID = "11111111-1111-1111-1111-111111111111"
OTHER_ACTOR_ID = "22222222-2222-2222-2222-222222222222"
ORG_ID = "33333333-3333-3333-8333-333333333333"
OTHER_ORG_ID = "44444444-4444-4444-8444-444444444444"
TASK_ID = "55555555-5555-5555-8555-555555555555"
RUN_ID = "66666666-6666-6666-8666-666666666666"


@pytest.fixture
def backend(fake_supabase):
    async def registered(task, agent_task):
        return task.get("kind") == "tool" and agent_task and agent_task.get("variables", {}).get("tool_name") == "gmail.backlog"

    matrx_scheduler.configure_db(models=fake_supabase.db_models())
    matrx_scheduler.configure(
        supabase_client=fake_supabase,
        surface="test",
        transaction=fake_supabase.transaction,
        backlog_task_validator=registered,
    )
    return fake_supabase


def _request(**overrides) -> BacklogRearmRequest:
    values = {
        "task_id": TASK_ID,
        "user_id": ACTOR_ID,
        "organization_id": ORG_ID,
        "predecessor_run_id": RUN_ID,
        "claim_token": "claim-token-1",
        "recovery_key": "v1:opaque-recovery-key",
        "due_at": datetime.now(UTC) + timedelta(seconds=30),
    }
    values.update(overrides)
    return BacklogRearmRequest(**values)


def test_rearm_request_refuses_unbounded_terminal_text() -> None:
    """A bounded tool result cannot turn the durable scheduler row unbounded."""
    with pytest.raises(ValueError, match="at most 2000"):
        _request(result_summary="x" * 2_001)


def _seed(backend, **overrides):
    now = datetime.now(UTC)
    task = {
        "id": TASK_ID,
        "user_id": ACTOR_ID,
        "organization_id": ORG_ID,
        "kind": "tool",
        "title": "bounded backlog",
        "queue": "recoveries",
        "enabled": True,
        "deleted_at": None,
        "expires_at": None,
    }
    run = {
        "id": RUN_ID,
        "task_id": TASK_ID,
        "user_id": ACTOR_ID,
        "organization_id": ORG_ID,
        "status": "running",
        "claim_token": "claim-token-1",
        "claim_expires_at": now + timedelta(minutes=5),
        "metadata": {"claim_protocol": 2},
        "due_at": now,
        "queue": "recoveries",
    }
    task.update(overrides.pop("task", {}))
    run.update(overrides.pop("run", {}))
    backend.rows["sch_task"].append(task)
    backend.rows["sch_agent_task"].append(
        {"id": TASK_ID, "prompt": "", "variables": {"tool_name": "gmail.backlog"}}
    )
    backend.rows["sch_run"].append(run)
    backend.rows["sch_run"].extend(overrides.pop("runs", []))
    assert not overrides
    return task, run


@pytest.mark.asyncio
async def test_finalizes_owned_run_and_creates_one_derived_successor(backend):
    """Removing either terminalization or successor insertion breaks the durable handoff."""
    task, predecessor = _seed(backend)

    outcome = await matrx_scheduler.finalize_and_rearm_backlog(_request())

    assert outcome.status == "rearmed"
    assert predecessor["status"] == "success"
    assert predecessor["claim_token"] is None
    successor = next(row for row in backend.rows["sch_run"] if row["id"] == outcome.successor_run_id)
    assert successor["status"] == "queued"
    assert successor["task_id"] == TASK_ID
    assert successor["user_id"] == task["user_id"]
    assert successor["organization_id"] == task["organization_id"]
    assert successor["queue"] == task["queue"]
    assert successor["metadata"][BACKLOG_REARM_METADATA_KEY]["recovery_key"] == "v1:opaque-recovery-key"
    assert successor["metadata"][BACKLOG_REARM_METADATA_KEY]["predecessor_run_id"] == RUN_ID
    receipt = predecessor["metadata"][BACKLOG_REARM_METADATA_KEY]
    assert receipt["successor_run_id"] == successor["id"]
    assert receipt["authority_digest"] != "claim-token-1"
    assert task["last_run_at"] == predecessor["finished_at"]


@pytest.mark.asyncio
async def test_rearm_persists_supplied_bounded_terminal_evidence_exactly(backend):
    """The completed backlog item retains the tool result the next worker needs."""
    _, predecessor = _seed(backend)
    output_ref = {"kind": "gmail_thread", "id": "thread-728"}
    metadata = {"processed_messages": 24, "cursor": "mailbox-page-7"}

    outcome = await matrx_scheduler.finalize_and_rearm_backlog(
        _request(
            result_summary="Triaged 24 invoices from the operations mailbox",
            error_message="2 invoices need a human vendor match",
            output_ref=output_ref,
            result_metadata=metadata,
        )
    )

    assert outcome.status == "rearmed"
    assert predecessor["result_summary"] == "Triaged 24 invoices from the operations mailbox"
    assert predecessor["error_message"] == "2 invoices need a human vendor match"
    assert predecessor["output_ref"] == output_ref
    assert predecessor["result_metadata"] == metadata


@pytest.mark.asyncio
async def test_rearm_omitting_terminal_evidence_preserves_recorded_progress(backend):
    """A rearm receipt must not erase progress recorded before the terminal write."""
    _, predecessor = _seed(
        backend,
        run={
            "result_summary": "Processed 17 recycling pickup tickets before lease renewal",
            "error_message": "",
            "output_ref": {"kind": "work_order_batch", "id": "route-19"},
            "result_metadata": {"units_done": 17, "cursor": "route-19-stop-17"},
        },
    )

    outcome = await matrx_scheduler.finalize_and_rearm_backlog(_request())

    assert outcome.status == "rearmed"
    assert predecessor["result_summary"] == "Processed 17 recycling pickup tickets before lease renewal"
    assert predecessor["error_message"] == ""
    assert predecessor["output_ref"] == {"kind": "work_order_batch", "id": "route-19"}
    assert predecessor["result_metadata"] == {"units_done": 17, "cursor": "route-19-stop-17"}


@pytest.mark.asyncio
async def test_successor_insert_failure_rolls_back_the_terminal_predecessor(backend):
    """If successor creation fails, the predecessor remains owned and nonterminal."""
    _seed(backend)
    backend.fail_next_run_create = True

    with pytest.raises(RuntimeError, match="simulated successor insert failure"):
        await matrx_scheduler.finalize_and_rearm_backlog(_request())

    restored = backend.rows["sch_run"][0]
    assert restored["status"] == "running"
    assert restored["claim_token"] == "claim-token-1"
    assert restored["metadata"] == {"claim_protocol": 2}
    assert len(backend.rows["sch_run"]) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "run_patch",
    [
        {"claim_token": "new-owner-token"},
        {"claim_expires_at": datetime.now(UTC) - timedelta(seconds=1)},
    ],
    ids=["lost-token", "expired-lease"],
)
async def test_lost_or_expired_authority_writes_neither_terminal_nor_successor(backend, run_patch):
    """A stale holder must not finish its run or seed another execution."""
    _, predecessor = _seed(backend, run=run_patch)

    outcome = await matrx_scheduler.finalize_and_rearm_backlog(_request())

    assert outcome.status == "authority_lost"
    assert predecessor["status"] == "running"
    assert len(backend.rows["sch_run"]) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "task_patch",
    [
        {"enabled": False},
        {"deleted_at": datetime.now(UTC)},
        {"kind": "ping"},
        {"organization_id": OTHER_ORG_ID},
    ],
    ids=["disabled", "deleted", "non-tool", "wrong-org"],
)
async def test_ineligible_task_never_finalizes_or_rearms(backend, task_patch):
    """Disabled, deleted, unregistered, or wrongly-bound tasks cannot opt in by run data alone."""
    _, predecessor = _seed(backend, task=task_patch)

    outcome = await matrx_scheduler.finalize_and_rearm_backlog(_request())

    assert outcome.status == "task_ineligible"
    assert predecessor["status"] == "running"
    assert len(backend.rows["sch_run"]) == 1


@pytest.mark.asyncio
async def test_trigger_row_refuses_on_demand_rearm(backend):
    """A task with any trigger row is scheduled work, never this opt-in path."""
    _, predecessor = _seed(backend)
    backend.rows["sch_trigger"].append({"id": "77777777-7777-7777-8777-777777777777", "task_id": TASK_ID})

    outcome = await matrx_scheduler.finalize_and_rearm_backlog(_request())

    assert outcome.status == "task_ineligible"
    assert predecessor["status"] == "running"


@pytest.mark.asyncio
async def test_triggered_predecessor_refuses_rearm_after_its_trigger_row_was_deleted(backend):
    """Deleting a trigger cannot turn its already-triggered run into on-demand authority."""
    _, predecessor = _seed(
        backend,
        run={"trigger_id": "77777777-7777-7777-8777-777777777777"},
    )

    outcome = await matrx_scheduler.finalize_and_rearm_backlog(_request())

    assert outcome.status == "task_ineligible"
    assert outcome.reason == "predecessor was created by a trigger"
    assert predecessor["status"] == "running"
    assert len(backend.rows["sch_run"]) == 1


@pytest.mark.asyncio
async def test_duplicate_retry_does_not_repeat_atomic_task_reporting(backend):
    """The terminal transaction owns last_run_at, so replay has no observer gap or duplicate."""
    task, predecessor = _seed(backend)

    first = await matrx_scheduler.finalize_and_rearm_backlog(_request())
    reported_at = task["last_run_at"]
    replay = await matrx_scheduler.finalize_and_rearm_backlog(_request())

    assert first.status == "rearmed"
    assert replay.status == "already_rearmed"
    assert task["last_run_at"] == reported_at == predecessor["finished_at"]


@pytest.mark.asyncio
@pytest.mark.parametrize("matching", [True, False], ids=["same-key", "different-key"])
async def test_active_collision_is_adopted_only_for_exact_recovery_key(backend, matching):
    """A competing active run is coverage only when its persisted identity exactly matches."""
    _, predecessor = _seed(backend)
    key = "v1:opaque-recovery-key" if matching else "v1:other-recovery-key"
    backend.rows["sch_run"].append(
        {
            "id": "88888888-8888-8888-8888-888888888888",
            "task_id": TASK_ID,
            "user_id": ACTOR_ID,
            "organization_id": ORG_ID,
            "queue": "recoveries",
            "trigger_id": None,
            "status": "queued",
            "due_at": datetime.now(UTC),
            "metadata": {BACKLOG_REARM_METADATA_KEY: {"version": 1, "recovery_key": key, "predecessor_run_id": RUN_ID, "authority_digest": "a" * 64}},
        }
    )

    outcome = await matrx_scheduler.finalize_and_rearm_backlog(_request())

    assert outcome.status == ("rearmed" if matching else "collision_refused")
    if matching:
        assert outcome.successor_run_id == "88888888-8888-8888-8888-888888888888"
        assert predecessor["status"] == "success"
    else:
        # The fake transaction snapshot makes this assertion prove the outer
        # predecessor transition was rolled back with the rejected collision.
        assert predecessor["status"] == "running"
        assert predecessor["metadata"] == {"claim_protocol": 2}


@pytest.mark.asyncio
async def test_sequential_duplicate_retry_requires_the_original_key_and_authority(backend):
    """A retry returns the first successor only with the original recovery key and claim token."""
    _seed(backend)
    first = await matrx_scheduler.finalize_and_rearm_backlog(_request())
    replay = await matrx_scheduler.finalize_and_rearm_backlog(_request())
    wrong_token = await matrx_scheduler.finalize_and_rearm_backlog(_request(claim_token="different"))
    wrong_key = await matrx_scheduler.finalize_and_rearm_backlog(_request(recovery_key="v1:different"))

    assert first.status == "rearmed"
    assert replay.status == "already_rearmed"
    assert replay.successor_run_id == first.successor_run_id
    assert wrong_token.status == "authority_lost"
    assert wrong_key.status == "authority_lost"
    assert len(backend.rows["sch_run"]) == 2


@pytest.mark.asyncio
async def test_created_successor_can_finish_and_rearm_the_next_bounded_batch(backend):
    """A prior recovery descriptor is ancestry, not a false terminal receipt on the next run."""
    _seed(backend)
    first = await matrx_scheduler.finalize_and_rearm_backlog(_request())
    successor = next(row for row in backend.rows["sch_run"] if row["id"] == first.successor_run_id)
    successor.update(
        status="running",
        claim_token="claim-token-2",
        claim_expires_at=datetime.now(UTC) + timedelta(minutes=5),
    )

    second = await matrx_scheduler.finalize_and_rearm_backlog(
        _request(
            predecessor_run_id=successor["id"],
            claim_token="claim-token-2",
            recovery_key="v1:opaque-recovery-key",
        )
    )

    assert second.status == "rearmed"
    assert successor["status"] == "success"
    assert len(backend.rows["sch_run"]) == 3


@pytest.mark.asyncio
async def test_successor_cannot_switch_to_a_different_recovery_key(backend):
    """An executing successor stays within the recovery execution that created it."""
    _seed(backend)
    first = await matrx_scheduler.finalize_and_rearm_backlog(_request())
    successor = next(row for row in backend.rows["sch_run"] if row["id"] == first.successor_run_id)
    successor.update(
        status="running",
        claim_token="claim-token-2",
        claim_expires_at=datetime.now(UTC) + timedelta(minutes=5),
    )

    outcome = await matrx_scheduler.finalize_and_rearm_backlog(
        _request(
            predecessor_run_id=successor["id"],
            claim_token="claim-token-2",
            recovery_key="v1:unrelated-recovery",
        )
    )

    assert outcome.status == "authority_lost"
    assert successor["status"] == "running"
    assert len(backend.rows["sch_run"]) == 2


@pytest.mark.asyncio
async def test_registry_validation_reads_the_tool_child_under_the_locked_order(backend):
    """The validator sees the tool child only after task and predecessor locks are held."""
    _seed(backend)

    await matrx_scheduler.finalize_and_rearm_backlog(_request())

    assert backend.lock_events[:4] == ["sch_task", "sch_run", "sch_agent_task", "sch_trigger"]


@pytest.mark.asyncio
@pytest.mark.parametrize("malformed", [None, "v1:not-a-record", [], {}], ids=["null", "string", "list", "empty-dict"])
async def test_malformed_present_recovery_metadata_cannot_be_treated_as_absent(backend, malformed):
    """A present but malformed rearm marker fails closed without terminalizing the predecessor."""
    _, predecessor = _seed(backend)
    predecessor["metadata"][BACKLOG_REARM_METADATA_KEY] = malformed

    outcome = await matrx_scheduler.finalize_and_rearm_backlog(_request())

    assert outcome.status == "authority_lost"
    assert predecessor["status"] == "running"
    assert len(backend.rows["sch_run"]) == 1


@pytest.mark.asyncio
async def test_same_key_successor_with_foreign_derived_fields_is_refused(backend):
    """A matching recovery key does not authorize adopting another actor's queued run."""
    _, predecessor = _seed(backend)
    backend.rows["sch_run"].append(
        {
            "id": "99999999-9999-9999-8999-999999999999",
            "task_id": TASK_ID,
            "user_id": OTHER_ACTOR_ID,
            "organization_id": ORG_ID,
            "queue": "recoveries",
            "trigger_id": None,
            "status": "queued",
            "due_at": datetime.now(UTC),
            "metadata": {BACKLOG_REARM_METADATA_KEY: {"version": 1, "recovery_key": "v1:opaque-recovery-key", "predecessor_run_id": RUN_ID, "authority_digest": "a" * 64}},
        }
    )

    outcome = await matrx_scheduler.finalize_and_rearm_backlog(_request())

    assert outcome.status == "collision_refused"
    assert predecessor["status"] == "running"
    assert len(backend.rows["sch_run"]) == 2


@pytest.mark.asyncio
async def test_malformed_current_predecessor_receipt_fails_closed(backend):
    """A receipt that claims this predecessor without a successor cannot authorize a retry."""
    _, predecessor = _seed(backend)
    predecessor["metadata"][BACKLOG_REARM_METADATA_KEY] = {
        "version": 1,
        "recovery_key": "v1:opaque-recovery-key",
        "predecessor_run_id": RUN_ID,
    }

    outcome = await matrx_scheduler.finalize_and_rearm_backlog(_request())

    assert outcome.status == "authority_lost"
    assert predecessor["status"] == "running"
    assert len(backend.rows["sch_run"]) == 1


@pytest.mark.asyncio
async def test_matching_receipt_on_a_nonterminal_predecessor_is_not_a_retry(backend):
    """Only a committed success row can return an already-rearmed outcome."""
    _, predecessor = _seed(backend)
    digest = hashlib.sha256(b"v1:opaque-recovery-key\x00claim-token-1").hexdigest()
    predecessor["metadata"][BACKLOG_REARM_METADATA_KEY] = {
        "version": 1,
        "recovery_key": "v1:opaque-recovery-key",
        "predecessor_run_id": RUN_ID,
        "authority_digest": digest,
        "successor_run_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
    }

    outcome = await matrx_scheduler.finalize_and_rearm_backlog(_request())

    assert outcome.status == "authority_lost"
    assert predecessor["status"] == "running"
    assert len(backend.rows["sch_run"]) == 1
