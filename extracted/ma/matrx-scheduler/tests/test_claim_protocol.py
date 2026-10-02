from __future__ import annotations

from datetime import UTC, datetime

import pytest

import matrx_scheduler
from matrx_scheduler import queries
from matrx_scheduler.models import SchRun, SchTask


ORGANIZATION_ID = "33333333-3333-4333-8333-333333333333"


@pytest.fixture(autouse=True)
def configure_scheduler(fake_supabase) -> None:
    matrx_scheduler.configure_db(models=fake_supabase.db_models())
    matrx_scheduler.configure(
        supabase_client=fake_supabase,
        surface="test",
    )


@pytest.mark.asyncio
async def test_scheduled_claim_stamps_current_protocol(fake_supabase) -> None:
    task = SchTask(
        id="11111111-1111-1111-1111-111111111111",
        user_id="22222222-2222-2222-2222-222222222222",
        organization_id=ORGANIZATION_ID,
        kind="agent",
        title="test",
        surfaces=["test"],
        next_due_at=datetime.now(UTC),
    )

    run = await queries.claim_task(task, None, None, lease_seconds=60)

    assert run is not None
    assert fake_supabase.rows["sch_run"][0]["organization_id"] == ORGANIZATION_ID
    assert fake_supabase.rows["sch_run"][0]["metadata"] == {
        "claim_protocol": queries.CLAIM_PROTOCOL
    }


@pytest.mark.asyncio
async def test_scheduled_claim_rejects_invalid_org_before_insert(fake_supabase) -> None:
    task = SchTask(
        id="11111111-1111-1111-1111-111111111111",
        user_id="22222222-2222-2222-2222-222222222222",
        organization_id="not-a-uuid",
        kind="agent",
        title="invalid organization",
        surfaces=["test"],
        next_due_at=datetime.now(UTC),
    )

    with pytest.raises(ValueError, match="task has no valid organization_id"):
        await queries.claim_task(task, None, None, lease_seconds=60)

    assert fake_supabase.rows["sch_run"] == []


@pytest.mark.asyncio
async def test_manual_claim_preserves_metadata_and_stamps_protocol(fake_supabase) -> None:
    now = datetime.now(UTC)
    row = {
        "id": "33333333-3333-3333-3333-333333333333",
        "task_id": "11111111-1111-1111-1111-111111111111",
        "user_id": "22222222-2222-2222-2222-222222222222",
        "organization_id": ORGANIZATION_ID,
        "status": "queued",
        "due_at": now,
        "metadata": {"requested_by": "manual-test"},
    }
    fake_supabase.rows["sch_run"].append(row)

    claimed = await queries.claim_queued_run(
        SchRun(**row),
        lease_seconds=60,
        max_runtime_seconds=60,
    )

    assert claimed is not None
    assert fake_supabase.rows["sch_run"][0]["metadata"] == {
        "requested_by": "manual-test",
        "claim_protocol": queries.CLAIM_PROTOCOL,
    }


@pytest.mark.asyncio
async def test_finalize_retains_bounded_batch_failure_receipts(fake_supabase) -> None:
    run_id = "33333333-3333-3333-3333-333333333333"
    claim_token = "claim-1"
    fake_supabase.rows["sch_run"].append(
        {"id": run_id, "claim_token": claim_token, "status": "running"}
    )
    receipts = "x" * 25_000

    finalized = await queries.finalize_run(
        run_id,
        claim_token,
        status="failed",
        error_message=receipts,
    )

    assert finalized is True
    assert len(fake_supabase.rows["sch_run"][0]["error_message"]) == 20_000


@pytest.mark.asyncio
async def test_each_persisted_terminal_failure_invokes_sink_once(fake_supabase) -> None:
    events: list[dict] = []

    async def sink(event: dict) -> None:
        events.append(event)

    matrx_scheduler.configure(
        supabase_client=fake_supabase,
        surface="test",
        failure_sink=sink,
    )
    run_id = "44444444-4444-4444-4444-444444444444"
    fake_supabase.rows["sch_run"].append(
        {
            "id": run_id,
            "task_id": "55555555-5555-5555-5555-555555555555",
            "claim_token": "claim-2",
            "status": "running",
        }
    )

    assert await queries.finalize_run(
        run_id, "claim-2", status="cancelled", error_message="deploy drain"
    )
    assert len(events) == 1
    assert events[0]["status"] == "cancelled"
    assert events[0]["task_id"] == "55555555-5555-5555-5555-555555555555"


@pytest.mark.asyncio
async def test_failed_finalization_that_loses_its_claim_does_not_report(fake_supabase, monkeypatch) -> None:
    """A stale worker must not report a terminal verdict it did not persist."""
    reports: list[dict[str, object]] = []

    async def report(run_id: str, **kwargs: object) -> None:
        reports.append({"run_id": run_id, **kwargs})

    monkeypatch.setattr(queries, "report_finalized_run", report)
    fake_supabase.rows["sch_run"].append(
        {"id": "lost", "claim_token": "new-owner", "status": "running"}
    )

    assert await queries.finalize_run("lost", "stale-owner", status="failed") is False
    assert reports == []


@pytest.mark.asyncio
async def test_failure_sink_observes_the_committed_terminal_row(fake_supabase) -> None:
    """Reporting is post-commit: a sink sees the terminal row, never an in-flight one."""
    seen_rows: list[dict] = []

    async def sink(_event: dict) -> None:
        seen_rows.append(dict(fake_supabase.rows["sch_run"][0]))

    matrx_scheduler.configure(
        supabase_client=fake_supabase,
        surface="test",
        failure_sink=sink,
    )
    fake_supabase.rows["sch_task"].append({"id": "task-1"})
    fake_supabase.rows["sch_run"].append(
        {"id": "run-1", "task_id": "task-1", "claim_token": "claim-1", "status": "running"}
    )

    assert await queries.finalize_run("run-1", "claim-1", status="failed") is True
    assert seen_rows[0]["status"] == "failed"
    assert seen_rows[0]["claim_token"] is None
    assert seen_rows[0]["finished_at"] is not None
    assert fake_supabase.rows["sch_task"][0]["last_run_at"] is not None


@pytest.mark.asyncio
async def test_sink_failure_cannot_break_persisted_finalize(fake_supabase) -> None:
    async def sink(_event: dict) -> None:
        raise RuntimeError("sink unavailable")

    matrx_scheduler.configure(
        supabase_client=fake_supabase,
        surface="test",
        failure_sink=sink,
    )
    run_id = "66666666-6666-6666-6666-666666666666"
    fake_supabase.rows["sch_run"].append(
        {"id": run_id, "task_id": None, "claim_token": "claim-3", "status": "running"}
    )

    assert await queries.finalize_run(run_id, "claim-3", status="failed") is True
    assert fake_supabase.rows["sch_run"][0]["status"] == "failed"
    assert fake_supabase.rows["sch_run"][0]["claim_token"] is None


@pytest.mark.asyncio
async def test_failure_report_retains_repeat_guard_semantics(fake_supabase, monkeypatch) -> None:
    """A persisted failed run still reaches the repeat guard with its task."""
    noted: list[tuple[str, str | None]] = []

    async def note_failed_run(run_id: str, task_id: str | None = None) -> None:
        noted.append((run_id, task_id))

    monkeypatch.setattr("matrx_scheduler.repeat_guard.note_failed_run", note_failed_run)
    fake_supabase.rows["sch_run"].append(
        {"id": "run-guard", "task_id": "task-guard", "claim_token": "guard", "status": "running"}
    )

    assert await queries.finalize_run("run-guard", "guard", status="failed") is True
    assert noted == [("run-guard", "task-guard")]


@pytest.mark.asyncio
async def test_report_refuses_nonterminal_mismatched_or_missing_ledger_rows(fake_supabase, monkeypatch) -> None:
    """A host cannot report a row until its matching terminal ledger verdict exists."""
    events: list[dict] = []
    noted: list[tuple[str, str | None]] = []

    async def sink(event: dict) -> None:
        events.append(event)

    async def note_failed_run(run_id: str, task_id: str | None = None) -> None:
        noted.append((run_id, task_id))

    matrx_scheduler.configure(supabase_client=fake_supabase, surface="test", failure_sink=sink)
    monkeypatch.setattr("matrx_scheduler.repeat_guard.note_failed_run", note_failed_run)
    fake_supabase.rows["sch_task"].append({"id": "task-unreported"})
    fake_supabase.rows["sch_run"].extend(
        [
            {"id": "still-running", "task_id": "task-unreported", "status": "running"},
            {"id": "success-row", "task_id": "task-unreported", "status": "success"},
        ]
    )

    await queries.report_finalized_run("still-running", status="failed")
    await queries.report_finalized_run("success-row", status="failed")
    await queries.report_finalized_run("missing-row", status="failed")

    assert events == []
    assert noted == []
    assert "last_run_at" not in fake_supabase.rows["sch_task"][0]


@pytest.mark.asyncio
async def test_report_uses_committed_failure_evidence_not_caller_arguments(fake_supabase) -> None:
    """The durable run row, not a caller payload, supplies sink evidence."""
    events: list[dict] = []

    async def sink(event: dict) -> None:
        events.append(event)

    matrx_scheduler.configure(supabase_client=fake_supabase, surface="test", failure_sink=sink)
    fake_supabase.rows["sch_task"].append({"id": "task-ledger"})
    fake_supabase.rows["sch_run"].append(
        {
            "id": "run-ledger",
            "task_id": "task-ledger",
            "status": "failed",
            "error_message": "the committed mailbox cursor expired",
            "result_metadata": {"cursor": "mailbox-page-7", "units_done": 24},
        }
    )

    await queries.report_finalized_run(
        "run-ledger",
        status="failed",
        error_message="fabricated caller error",
        result_metadata={"fabricated": True},
    )

    assert events[0]["error_message"] == "the committed mailbox cursor expired"
    assert events[0]["result_metadata"] == {"cursor": "mailbox-page-7", "units_done": 24}


@pytest.mark.asyncio
async def test_success_and_lost_lease_do_not_invoke_failure_sink(fake_supabase) -> None:
    events: list[dict] = []

    async def sink(event: dict) -> None:
        events.append(event)

    matrx_scheduler.configure(
        supabase_client=fake_supabase,
        surface="test",
        failure_sink=sink,
    )
    fake_supabase.rows["sch_run"].extend(
        [
            {"id": "success", "claim_token": "yes", "status": "running"},
            {"id": "lost", "claim_token": "new-owner", "status": "running"},
        ]
    )

    assert await queries.finalize_run("success", "yes", status="success") is True
    assert await queries.finalize_run("lost", "old-owner", status="failed") is False
    assert events == []


@pytest.mark.asyncio
async def test_operational_failure_uses_the_same_durable_sink(fake_supabase) -> None:
    from matrx_scheduler._ext import report_operational_failure

    events: list[dict] = []

    async def sink(event: dict) -> None:
        events.append(event)

    matrx_scheduler.configure(
        supabase_client=fake_supabase,
        surface="test",
        failure_sink=sink,
    )
    await report_operational_failure(
        RuntimeError("scan broke"),
        operation="queued_run_scan",
        context={"task_id": "task-1"},
    )

    assert events == [
        {
            "run_id": None,
            "status": "operational_failed",
            "error_message": "scan broke",
            "error_type": "RuntimeError",
            "operation": "queued_run_scan",
            "result_metadata": {"task_id": "task-1"},
        }
    ]
