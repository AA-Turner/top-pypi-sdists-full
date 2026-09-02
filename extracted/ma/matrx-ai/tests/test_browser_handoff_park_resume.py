"""WS-6 — the durable park/resume protocol exercised end to end against the REAL
`matrx-runtime` ExecutionEngine + InMemoryExecutionStore and the REAL pending-call
ledger seam, with only the browser side faked (S5 §8).

Definition of Done proved here: an execution parks and resumes EXACTLY ONCE
across a simulated manager restart and duplicate resume attempts, and NO open
socket or in-memory future owns continuity — the kill-the-process test.
"""

from __future__ import annotations

import pytest
from matrx_runtime import (
    ExecutionEngine,
    ExecutionStatus,
    InMemoryExecutionStore,
)

from matrx_ai.browser_handoff import (
    BrowserHandoffCoordinator,
    CHECKPOINT_KIND,
    HandoffOpenRequest,
    HandoffReason,
    HandoffResolutionKind,
    ParkOutcome,
    ReconcileActionKind,
    Reconciler,
    set_handoff_ledger,
)
from browser_handoff_fakes import (
    Clock,
    ControllerConflict,
    FakeHandoffLedger,
    FakeHandoffSource,
)

pytestmark = pytest.mark.asyncio

RUN_ID = "run-1"
PROFILE = "profile-1"
CONV = "conv-1"
CALL = "call-abc"


class World:
    """Everything durable (survives a restart) vs. everything in-process (dies).

    Durable: `store` (the runtime ExecutionStore = the DB), `handoffs` +
    `controllers` (browser.handoff rows), `ledger.rows` (chat.tool_call). A
    restart rebuilds engine/coordinator/source/ledger objects over these dicts.
    """

    def __init__(self) -> None:
        self.clock = Clock()
        self.store = InMemoryExecutionStore()
        self.handoffs: dict = {}
        self.controllers: dict = {}
        self.ledger_rows: dict = {}
        self._rebuild()

    def _rebuild(self) -> None:
        self.engine = ExecutionEngine(self.store)
        self.source = FakeHandoffSource(
            self.clock, handoffs=self.handoffs, controllers=self.controllers
        )
        self.ledger = FakeHandoffLedger(self.clock, rows=self.ledger_rows)
        set_handoff_ledger(self.ledger)
        self.coord = BrowserHandoffCoordinator(self.engine, self.source)

    def restart(self) -> None:
        """Simulate a full manager/process kill: drop every in-process object,
        keep only the durable stores, rebuild."""
        self.engine = self.source = self.ledger = self.coord = None
        self._rebuild()

    async def start_run_execution(self, *, holder="worker-A") -> str:
        """A conversation-hosted browser run: a leased RUNNING execution the
        park will suspend."""
        self.source.seed_run(RUN_ID, revision=1)
        scope = self.engine.execution(
            type="conversation", link_kind="conversation", link_id=CONV, holder=holder
        )
        await scope.begin()
        return scope.id

    def open_req(self, execution_id: str, *, call_id=CALL, conv=CONV) -> HandoffOpenRequest:
        return HandoffOpenRequest(
            run_id=RUN_ID,
            profile_id=PROFILE,
            reason=HandoffReason.MFA_REQUIRED,
            safe_instructions="Please complete the verification step.",
            requested_by_execution_id=execution_id,
            requested_by_user_id="user-1",
            conversation_id=conv,
            pending_call_id=call_id,
            expected_controller_revision=1,
        )

    def quiesced(self, *, drained=True):
        from browser_handoff_fakes import _inventory

        from matrx_ai.browser_handoff import WorkerQuiesced

        return WorkerQuiesced(
            run_id=RUN_ID,
            controller_revision=2,
            queue_drained=drained,
            inventory=_inventory(self.clock),
            quiesced_at=self.clock.now(),
        )


async def _park(w: World, *, holder="worker-A") -> tuple[str, str]:
    ex_id = await w.start_run_execution(holder=holder)
    receipt = await w.coord.park(
        w.open_req(ex_id), w.quiesced(), holder=holder, now=w.clock.now()
    )
    assert receipt.outcome is ParkOutcome.PARKED
    # Everything durable is on disk before the "stream ends":
    ex = await w.engine.get_execution(ex_id)
    assert ex.status is ExecutionStatus.WAITING_INPUT  # invariant 6: not paused
    assert ex.lease_holder is None  # lease released on park
    cp = await w.engine.latest_checkpoint(ex_id)
    assert cp.state["kind"] == CHECKPOINT_KIND  # invariant 5
    assert cp.state["resolution_key"] == receipt.resolution_key
    assert w.ledger_rows[CALL]["status"] == "delegated"
    assert w.handoffs[receipt.handoff_id]["state"] == "requested"
    return ex_id, receipt.handoff_id


# ---------------------------------------------------------------------------
# 1. Happy path — park, claim, return, resume once.
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("label", ["signed_in", "approved", "could_not_complete"])
async def test_happy_path_parks_and_resumes_once(label):
    w = World()
    ex_id, hid = await _park(w)
    await w.source.claim(hid, user_id="user-1")

    r = await w.coord.resume(hid, user_id="user-1", outcome_label=label, holder="worker-B")
    assert r.resolved and r.resume_driven and not r.already_resolved

    ex = await w.engine.get_execution(ex_id)
    assert ex.status is ExecutionStatus.RUNNING  # resumed exactly once
    assert w.ledger_rows[CALL]["status"] == "resolved"
    assert w.handoffs[hid]["state"] == "returned"
    assert w.handoffs[hid]["outcome_label"] == label
    assert w.ledger.resolve_calls == 1


# ---------------------------------------------------------------------------
# 2. Duplicate return — N closers, ONE resolution, ONE continuation.
# ---------------------------------------------------------------------------
async def test_duplicate_return_resolves_exactly_once():
    w = World()
    ex_id, hid = await _park(w)
    await w.source.claim(hid, user_id="user-1")

    import asyncio

    results = await asyncio.gather(
        *[w.coord.resume(hid, user_id="user-1", outcome_label="signed_in", holder=f"w{i}") for i in range(5)]
    )
    winners = [r for r in results if r.resume_driven]
    assert len(winners) == 1  # exactly one resume driver
    completions = [r for r in results if r.resolved and not r.already_resolved]
    assert len(completions) == 1  # exactly one tool completion
    ex = await w.engine.get_execution(ex_id)
    assert ex.status is ExecutionStatus.RUNNING


# ---------------------------------------------------------------------------
# 3. Duplicate resume claim — engine.start CAS elects one driver.
# ---------------------------------------------------------------------------
async def test_duplicate_resume_claim_one_driver():
    w = World()
    ex_id, hid = await _park(w)
    await w.source.claim(hid, user_id="user-1")
    resolution = await w.source.return_control(hid, user_id="user-1", outcome_label="signed_in")
    await w.ledger.resolve(resolution)  # pretend R4 already done

    import asyncio

    driven = await asyncio.gather(
        *[w.coord._claim_resume(ex_id, holder=f"w{i}", lease_seconds=None) for i in range(4)]
    )
    assert sum(driven) == 1  # exactly one won the WAITING_INPUT→RUNNING CAS


# ---------------------------------------------------------------------------
# 4. Kill-the-process — no in-memory future owns continuity (the DoD).
# ---------------------------------------------------------------------------
async def test_kill_the_process_then_resume_exactly_once():
    w = World()
    ex_id, hid = await _park(w)
    await w.source.claim(hid, user_id="user-1")

    # The whole hosting process dies while parked. Only the durable stores live.
    w.restart()

    # The human returns AFTER the restart, against a freshly-built coordinator
    # that has zero in-memory state about this handoff.
    r = await w.coord.resume(hid, user_id="user-1", outcome_label="signed_in", holder="worker-C")
    assert r.resolved and r.resume_driven

    ex = await w.engine.get_execution(ex_id)
    assert ex.status is ExecutionStatus.RUNNING
    assert w.ledger_rows[CALL]["status"] == "resolved"

    # A duplicate resume after the fact is an idempotent no-op — pressing Return
    # twice never surfaces an error.
    r2 = await w.coord.resume(hid, user_id="user-1", outcome_label="signed_in", holder="worker-C")
    assert not r2.resume_driven and r2.resolved and r2.already_resolved
    # The ledger CAS — not the call count — is what makes completion exactly-once:
    # the row is resolved once, by the first (superseding) return.
    assert w.ledger_rows[CALL]["resolution_source"] == "completed"


# ---------------------------------------------------------------------------
# 4b. Manager restart mid-sequence — reconciler re-drives from durable rows.
# ---------------------------------------------------------------------------
async def test_restart_between_4_1_and_4_3_reconciler_resumes():
    """Died AFTER the human-episode CAS (state='returning') but BEFORE the tool
    completion — the reconciler re-runs R4–R5 (S5 §4.4 row 1)."""
    w = World()
    ex_id, hid = await _park(w)
    await w.source.claim(hid, user_id="user-1")
    # 4.1 happened (return_control closed the episode) but the process died
    # before ledger.resolve.
    await w.source.return_control(hid, user_id="user-1", outcome_label="signed_in")
    assert w.handoffs[hid]["state"] == "returning"
    assert w.handoffs[hid]["tool_resolved_at"] is None

    w.restart()
    recon = Reconciler(w.engine, w.source, holder="worker-R")
    actions = await recon.run()

    assert any(a.kind is ReconcileActionKind.RESUMED_RETURN for a in actions)
    ex = await w.engine.get_execution(ex_id)
    assert ex.status is ExecutionStatus.RUNNING
    assert w.ledger_rows[CALL]["status"] == "resolved"


async def test_restart_between_4_3_and_R5_reconciler_dispatches_resume():
    """Died AFTER the tool completion (state='returned') but BEFORE the resume
    was opened — the reconciler opens it (S5 §4.4 row 2)."""
    w = World()
    ex_id, hid = await _park(w)
    await w.source.claim(hid, user_id="user-1")
    resolution = await w.source.return_control(hid, user_id="user-1", outcome_label="signed_in")
    await w.ledger.resolve(resolution)
    await w.source.mark_tool_resolved(hid)  # state='returned', resume not dispatched
    assert w.handoffs[hid]["resume_dispatched_at"] is None

    w.restart()
    recon = Reconciler(w.engine, w.source, holder="worker-R")
    actions = await recon.run()

    assert any(a.kind is ReconcileActionKind.DISPATCHED_RESUME for a in actions)
    ex = await w.engine.get_execution(ex_id)
    assert ex.status is ExecutionStatus.RUNNING


# ---------------------------------------------------------------------------
# 5. Never-returned — timeout placeholder, then a LATE return supersedes it.
# ---------------------------------------------------------------------------
async def test_never_returned_then_late_return_supersedes():
    w = World()
    ex_id, hid = await _park(w)
    await w.source.claim(hid, user_id="user-1")

    # Advance past the pending-call expiry; the ledger sweep writes a placeholder.
    w.clock.advance(31 * 24 * 3600)
    w.ledger.sweep_timeout(CALL)
    assert w.ledger_rows[CALL]["resolution_source"] == "timeout_sweep"

    # A genuine return on day 31 SUPERSEDES the placeholder and resumes (S5 §6).
    r = await w.coord.resume(hid, user_id="user-1", outcome_label="signed_in", holder="worker-B")
    assert r.resolved and r.resume_driven
    assert w.ledger_rows[CALL]["resolution_source"] == "completed"
    ex = await w.engine.get_execution(ex_id)
    assert ex.status is ExecutionStatus.RUNNING


# ---------------------------------------------------------------------------
# 6. Cancelled — typed cancellation reaches the model; run resumes to report it.
# ---------------------------------------------------------------------------
async def test_cancelled_resolution_completes_the_call():
    w = World()
    ex_id, hid = await _park(w)
    await w.source.claim(hid, user_id="user-1")

    resolution = await w.source.cancel(hid, user_id="user-2")
    assert resolution.kind is HandoffResolutionKind.CANCELLED
    r = await w.coord._drive_resolution(resolution, holder="worker-B")
    assert r.resolved and r.resume_driven
    assert w.controllers[RUN_ID]["controller_kind"] == "stopped"


# ---------------------------------------------------------------------------
# 7. Park refusal — un-drained worker: NO row, NO delegate, NO park.
# ---------------------------------------------------------------------------
async def test_park_refusal_leaves_nothing_behind():
    w = World()
    ex_id = await w.start_run_execution()
    receipt = await w.coord.park(w.open_req(ex_id), w.quiesced(drained=False), holder="worker-A")
    assert receipt.outcome is ParkOutcome.REFUSED
    assert w.handoffs == {}  # no handoff row
    assert CALL not in w.ledger_rows  # no delegated row
    ex = await w.engine.get_execution(ex_id)
    assert ex.status is ExecutionStatus.RUNNING  # not parked


# ---------------------------------------------------------------------------
# 8. Two-controller race — one controller; the loser is refused.
# ---------------------------------------------------------------------------
async def test_two_controller_race_second_open_is_refused():
    w = World()
    ex_id, hid = await _park(w)
    # A second park attempt on the same live run (stale expected revision) loses
    # the controller CAS.
    with pytest.raises(ControllerConflict):
        await w.source.open_handoff(w.open_req(ex_id, call_id="call-2"))


# ---------------------------------------------------------------------------
# 9. Stale fencing token — a pre-handoff command is refused after resume.
# ---------------------------------------------------------------------------
async def test_stale_fencing_token_refused_after_resume():
    w = World()
    ex_id, hid = await _park(w)
    stale_revision = 1  # the agent's command was minted before the handoff
    await w.source.claim(hid, user_id="user-1")
    await w.coord.resume(hid, user_id="user-1", outcome_label="signed_in", holder="worker-B")
    # After resume the controller revision has advanced well past 1.
    assert not w.source.command_accepted(RUN_ID, stale_revision)
    # A command carrying the fresh token IS accepted.
    fresh = w.controllers[RUN_ID]["controller_revision"]
    assert w.source.command_accepted(RUN_ID, fresh)


# ---------------------------------------------------------------------------
# 10. Orphaned park — WAITING_INPUT + browser checkpoint + no handoff row.
# ---------------------------------------------------------------------------
async def test_orphaned_park_screams_and_closes():
    w = World()
    ex_id, hid = await _park(w)
    # Corrupt the durable state: the handoff row vanished but the parked
    # execution + checkpoint remain (should be impossible; P2 precedes P3).
    del w.handoffs[hid]
    w.restart()
    recon = Reconciler(w.engine, w.source, holder="worker-R")
    actions = await recon.run()
    assert any(a.kind is ReconcileActionKind.ORPHAN_ALARM for a in actions)
    ex = await w.engine.get_execution(ex_id)
    assert ex.status is ExecutionStatus.FAILED  # never left stranded


# ---------------------------------------------------------------------------
# 11. Never-claimed expiry — reconciler drives the expiry resolution.
# ---------------------------------------------------------------------------
async def test_never_claimed_expiry_via_reconciler():
    w = World()
    ex_id, hid = await _park(w)
    # Nobody claims; advance past the claim window.
    w.clock.advance(FakeHandoffSource.CLAIM_WINDOW_S + 1)
    recon = Reconciler(w.engine, w.source, holder="worker-R")
    actions = await recon.run()
    assert any(a.kind is ReconcileActionKind.DROVE_EXPIRY for a in actions)
    assert w.ledger_rows[CALL]["resolution_source"] == "expired"
    ex = await w.engine.get_execution(ex_id)
    assert ex.status is ExecutionStatus.RUNNING  # resumes to tell the user plainly


# ---------------------------------------------------------------------------
# 12. Partial park (died after P3, before P5) leaves no false resume.
# ---------------------------------------------------------------------------
async def test_partial_park_before_suspend_no_false_continuity():
    """A process death after the delegate but before the WAITING_INPUT flip
    leaves the execution RUNNING+leased — recovered by the runtime lease reaper,
    never by an in-memory continuation. A resume attempt is a safe no-op."""
    w = World()
    ex_id = await w.start_run_execution(holder="worker-A")
    # Drive P1–P4 by hand, stopping before P5.
    ticket = await w.source.open_handoff(w.open_req(ex_id))
    await w.ledger.delegate(
        call_id=CALL, conversation_id=CONV, execution_id=ex_id,
        handoff_id=ticket.handoff_id, expires_at=w.clock.now(),
    )
    await w.engine.save_checkpoint(ex_id, {"kind": CHECKPOINT_KIND, "handoff_id": ticket.handoff_id})
    # process dies here — no request_input/release_to_waiting ran.
    w.restart()
    ex = await w.engine.get_execution(ex_id)
    assert ex.status is ExecutionStatus.RUNNING  # never falsely parked
    # A stray resume claim finds it not-waiting and does nothing.
    driven = await w.coord._claim_resume(ex_id, holder="worker-Z", lease_seconds=None)
    assert driven is False
