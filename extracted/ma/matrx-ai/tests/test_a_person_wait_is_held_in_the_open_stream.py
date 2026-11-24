"""A CALL PARKED ON A PERSON IS WAITED FOR IN THE OPEN STREAM (RESUME-AND-RECOVERY section 1b, rules P1-P4,
P8, P10).

The person path: an ask's call returns ``delegated_pending`` from its dispatch; ``ToolExecutor.execute`` then
waits for the person's answer in the same stream, only for a client that opted in with the PERSON read, only
for a run somebody reads live, never past the row's own expiry. A taken answer is the stored row's own content
(the same end as the client-tool hold); a given-up wait parks exactly as today. The wait treats a lease taken
away as ``superseded``; the expiry sweep never leaves a lease on the row it resolves.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest
from matrx_connect import AppContext
from matrx_connect.context.app_context import clear_app_context, set_app_context

from matrx_ai.db._conversation_rebuild_impl import _rebuild_tool_result_content
from matrx_ai.orchestrator.execution_state import ExecutionState, _execution_state
from matrx_ai.tools import delegated_hold as hold
from matrx_ai.tools.executor import ToolExecutor
from matrx_ai.tools.models import ToolContext, ToolDefinition

CONV = "11111111-1111-1111-1111-111111111111"
PARKED = {"parked_on": {"kind": "action_request", "action_request_id": "ask-1"}}


def _hooks(*, person_ms: int = 1_800_000, client_ms: int = 600_000, **over) -> hold.HoldHooks:
    base = dict(
        hold_ms=lambda reason="client_tool": person_ms if reason == "person" else client_ms,
        poll_ms=lambda: 50, may_hold=lambda: True, lease_ms=lambda: 30_000,
        slow_poll_ms=lambda: 2000, fast_window_ms=lambda: 10_000,
        max_hold_ms=lambda reason="client_tool": person_ms if reason == "person" else 55 * 60_000,
    )
    return hold.HoldHooks(**{**base, **over})


def _parked_row(**over) -> SimpleNamespace:
    base = dict(
        id="tool-row", call_id="call-ask", status="delegated", is_client_delegated=True, resolved_at=None,
        metadata=dict(PARKED), expires_at=datetime.now(UTC) + timedelta(days=1),
    )
    return SimpleNamespace(**{**base, **over})


def _answered_row() -> SimpleNamespace:
    return SimpleNamespace(
        id="tool-row", call_id="call-ask", tool_name="ask_person", tool_name_as_called="ask_person",
        output='{"status": "answered", "result": {"choice": "blue"}}', output_type="json", is_error=False,
        error_type=None, error_message=None, output_chars=51, output_preview=None, model_stub_at=None,
        metadata=dict(PARKED), status="completed", held_until="lease",
    )


class _Run:
    """One person-parked call after its dispatch, with the row, the lease and the wait doubled at their seams."""

    def __init__(self, monkeypatch: pytest.MonkeyPatch, *, reads: list[str], row: SimpleNamespace | None = None,
                 outcome: hold.HoldOutcome | None = None, claimed: bool = True, hooks: hold.HoldHooks | None = None,
                 checkpoint: bool = True, **ctx_over) -> None:
        self.events: list = []
        self.infos: list = []
        self.claims: list[float] = []
        self.waits: list[float] = []
        self.ctx_over = ctx_over
        self.checkpoint = checkpoint
        run = self

        class Emitter:
            async def send_tool_event(self, event):
                run.events.append(event)

            async def send_info(self, info):
                run.infos.append(info)

        async def read_row(**kwargs):
            assert kwargs == {"id": "tool-row"}
            return [row if row is not None else _parked_row()]

        async def claim(row_id, *, conversation_id, hold):
            run.claims.append(hold.seconds)
            return claimed

        async def wait(row_id, *, conversation_id, call_id, hold, stop_reason=None):
            run.waits.append(hold.seconds)
            assert outcome is not None, "this call must not wait"
            return outcome

        from matrx_ai.db import cxm

        monkeypatch.setattr(cxm.tool_call, "filter_items", read_row)
        monkeypatch.setattr(hold, "_hooks", hooks if hooks is not None else _hooks())
        monkeypatch.setattr(hold, "claim", claim)
        monkeypatch.setattr(hold, "wait_for_result", wait)
        self.emitter = Emitter()
        self.metadata = {"client_reads": reads} if reads else {}
        self.state = ExecutionState()
        self.state.tool_dispatch_response = SimpleNamespace(messages=["the assistant tool_use"])

    async def hold_for_person(self):
        async def checkpoint():
            return "assistant-row"

        ctx_fields = dict(emitter=self.emitter, store=True, metadata=self.metadata)
        ctx_fields.update(self.ctx_over)
        token = set_app_context(AppContext(**ctx_fields))
        state_token = _execution_state.set(self.state)
        try:
            executor = ToolExecutor(registry=SimpleNamespace(bindings_for_tool=lambda _name: []))
            return await executor._hold_for_person(
                ToolDefinition(name="ask_person"),
                ToolContext(call_id="call-ask", tool_name="ask_person", conversation_id=CONV, emitter=self.emitter,
                            assistant_checkpoint=checkpoint if self.checkpoint else None),
                "tool-row",
                0.0,
            )
        finally:
            _execution_state.reset(state_token)
            clear_app_context(token)


#: The wire words a client names in ``client.reads`` (the contract, spelled out).
BOTH = ["delegated-hold-v1", "delegated-hold-person-v1"]


@pytest.mark.asyncio
async def test_the_client_tool_read_alone_never_holds_a_question(monkeypatch) -> None:
    run = _Run(monkeypatch, reads=["delegated-hold-v1"])
    assert await run.hold_for_person() is None
    assert run.claims == [] and run.infos == [] and run.events == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ctx_over",
    [
        {"parent_request_id": "22222222-2222-2222-2222-222222222222"},  # a child agent run
        {"is_internal_agent": True},
        {"system_run": True, "parent_request_id": "22222222-2222-2222-2222-222222222222"},
        {"store": False},
    ],
    ids=["child_run", "internal_agent", "system_run", "unsaved"],
)
async def test_a_run_nobody_reads_live_never_holds_a_question(monkeypatch, ctx_over) -> None:
    run = _Run(monkeypatch, reads=BOTH, **ctx_over)
    assert await run.hold_for_person() is None
    assert run.claims == []


@pytest.mark.asyncio
async def test_a_muted_helper_never_holds_a_question(monkeypatch) -> None:
    run = _Run(monkeypatch, reads=BOTH)
    run.metadata["client_delegation_disabled"] = True
    assert await run.hold_for_person() is None
    assert run.claims == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "row",
    [
        _parked_row(metadata={}),  # not parked on a person
        _parked_row(metadata={"parked_on": {"kind": "browser_handoff"}}),
        _parked_row(status="completed", resolved_at=datetime.now(UTC)),  # answered before the wait began
        _parked_row(is_client_delegated=False),
    ],
    ids=["no_parked_on", "other_kind", "already_answered", "not_delegated"],
)
async def test_only_a_row_still_parked_on_an_ask_is_held(monkeypatch, row) -> None:
    run = _Run(monkeypatch, reads=BOTH, row=row)
    assert await run.hold_for_person() is None
    assert run.claims == []


@pytest.mark.asyncio
async def test_no_durable_tool_use_means_no_hold(monkeypatch) -> None:
    run = _Run(monkeypatch, reads=BOTH, checkpoint=False)
    assert await run.hold_for_person() is None
    assert run.claims == []


@pytest.mark.asyncio
async def test_the_person_knob_at_zero_never_holds(monkeypatch) -> None:
    run = _Run(monkeypatch, reads=BOTH, hooks=_hooks(person_ms=0))
    assert await run.hold_for_person() is None
    assert run.claims == []


@pytest.mark.asyncio
async def test_the_window_stays_one_lease_under_the_rows_own_expiry(monkeypatch) -> None:
    soon = _parked_row(expires_at=datetime.now(UTC) + timedelta(seconds=600))
    run = _Run(monkeypatch, reads=BOTH, row=soon, outcome=hold.HoldOutcome(taken=False, reason="timeout"))
    await run.hold_for_person()
    (seconds,) = run.claims
    assert 560 < seconds <= 570, "ten minutes left, minus one 30 s lease, under the 30-minute knob"


@pytest.mark.asyncio
async def test_a_row_expiring_within_two_leases_is_not_held(monkeypatch) -> None:
    soon = _parked_row(expires_at=datetime.now(UTC) + timedelta(seconds=50))
    run = _Run(monkeypatch, reads=BOTH, row=soon)
    assert await run.hold_for_person() is None
    assert run.claims == []


@pytest.mark.asyncio
async def test_a_failed_claim_parks_as_today_and_says_nothing(monkeypatch) -> None:
    run = _Run(monkeypatch, reads=BOTH, claimed=False)
    assert await run.hold_for_person() is None
    assert run.infos == [] and run.waits == []


@pytest.mark.asyncio
async def test_an_answer_taken_under_the_hold_is_the_stored_row(monkeypatch) -> None:
    row = _answered_row()
    run = _Run(monkeypatch, reads=BOTH, outcome=hold.HoldOutcome(taken=True, row=row, waited_ms=4200))
    result = await run.hold_for_person()

    (waiting,) = run.infos
    assert waiting.code == "delegated_hold_waiting"
    assert waiting.metadata["reason"] == "person" and waiting.metadata["action_request_id"] == "ask-1"
    assert waiting.metadata["call_id"] == "call-ask" and waiting.metadata["until"]
    assert run.waits == [1800.0]
    assert run.state.tool_dispatch_response is None, "an interrupt must never answer the held call"
    assert result is not None and result.delegated_pending is False and result.success is True
    assert result.client_resolved_content == _rebuild_tool_result_content([row])[0]
    done = run.events[-1]
    assert done.event == "tool_completed" and done.data["held"] is True and done.data["waited_ms"] == 4200


@pytest.mark.asyncio
async def test_a_given_up_person_wait_says_so_and_parks(monkeypatch) -> None:
    run = _Run(monkeypatch, reads=BOTH, outcome=hold.HoldOutcome(taken=False, reason="superseded", waited_ms=900))
    assert await run.hold_for_person() is None
    assert [i.code for i in run.infos] == ["delegated_hold_waiting", "delegated_hold_released"]
    assert run.infos[-1].metadata["reason"] == "superseded"


def test_each_reason_reads_its_own_limit(monkeypatch) -> None:
    monkeypatch.setattr(hold, "_hooks", _hooks(person_ms=1_800_000, client_ms=600_000))
    person = hold.settings(reason="person")
    client = hold.settings()
    assert person is not None and person.seconds == 1800.0
    assert client is not None and client.seconds == 600.0
    monkeypatch.setattr(hold, "_hooks", _hooks(person_ms=0))
    assert hold.settings(reason="person") is None and hold.settings() is not None


class _Row:
    def __init__(self) -> None:
        self.status = "delegated"
        self.resolved_at = None
        self.held_until: datetime | None = None
        self.writes: list[str] = []

    def view(self) -> SimpleNamespace:
        return SimpleNamespace(id="row-1", status=self.status, resolved_at=self.resolved_at,
                               held_until=self.held_until, is_error=False)

    async def holder_write(self, row_id, *, conversation_id, held_until, renew) -> int:
        if self.status != "delegated" or self.resolved_at is not None:
            return 0
        if (renew or held_until is None) and self.held_until is None:
            return 0
        self.held_until = held_until
        self.writes.append("release" if held_until is None else ("renew" if renew else "claim"))
        return 1


@pytest.mark.asyncio
async def test_a_lease_taken_away_is_superseded_and_parks_without_a_release(monkeypatch) -> None:
    row = _Row()

    async def read(_row_id):
        return row.view()

    monkeypatch.setattr(hold, "_read_row", read)
    monkeypatch.setattr(hold, "_write", row.holder_write)
    monkeypatch.setattr(hold, "_hooks", _hooks())
    found = hold.settings()  # any reason: a lease taken away means the same thing
    assert found is not None and await hold.claim("row-1", conversation_id="conv", hold=found)
    task = asyncio.create_task(hold.wait_for_result("row-1", conversation_id="conv", call_id="call", hold=found))
    await asyncio.sleep(0)
    row.held_until = None  # the turn-start door released the person-wait (rule P9)
    hold.wake("conv", "call")
    outcome = await asyncio.wait_for(task, 1)
    assert not outcome.taken and outcome.reason == "superseded"
    assert row.writes == ["claim"], "nothing to release: the lease is already gone"
    assert row.status == "delegated"


@pytest.mark.asyncio
async def test_the_expiry_sweep_never_leaves_a_lease_on_what_it_resolves(monkeypatch) -> None:
    from matrx_ai.db import cx_managers
    from matrx_ai.tools import logger as tool_logger

    expired = SimpleNamespace(id="row-x", status="delegated")

    async def filter_items(**kwargs):
        return [expired]

    writes: list[dict] = []

    async def update_row(self, row_id, data, *, coordinator=None):
        writes.append(data)

    monkeypatch.setattr(cx_managers, "server_maintenance_available", lambda: True)
    monkeypatch.setattr(tool_logger, "_cxm", lambda: SimpleNamespace(tool_call=SimpleNamespace(
        filter_items=filter_items)))
    monkeypatch.setattr(tool_logger.ToolExecutionLogger, "_update_row", update_row)
    assert await tool_logger.ToolExecutionLogger().expire_delegated_calls() == 1
    (data,) = writes
    assert data["resolution_source"] == "timeout_sweep"
    assert "held_until" in data and data["held_until"] is None


# ── Review round: each P3 gate alone, real forks, a failing checkpoint, a failed give-up, the batch end ──────


def _person_ctx(**over) -> AppContext:
    fields = dict(emitter=SimpleNamespace(), store=True, metadata={"client_reads": list(BOTH)}, origin_class="human")
    fields.update(over)
    return AppContext(**fields)


def _allowed(ctx: AppContext) -> bool:
    token = set_app_context(ctx)
    try:
        return ToolExecutor._person_hold_allowed()
    finally:
        clear_app_context(token)


def test_a_person_turn_that_opted_in_may_hold() -> None:
    assert _allowed(_person_ctx()) is True


@pytest.mark.parametrize(
    "over",
    [
        {"parent_request_id": "22222222-2222-2222-2222-222222222222"},
        {"store": False},
        {"is_internal_agent": True},
        {"metadata": {"client_reads": list(BOTH), "client_delegation_disabled": True}},
        {"metadata": {"client_reads": ["delegated-hold-v1"]}},
    ],
    ids=["parent_request_id", "store_false", "internal_agent", "muted_helper", "client_tool_read_only"],
)
def test_each_gate_alone_refuses_the_hold(over) -> None:
    """One field changed from a turn that may hold: each gate refuses on its own."""
    assert _allowed(_person_ctx(**over)) is False


def test_a_system_run_alone_refuses_the_hold(monkeypatch) -> None:
    """``system_run`` cannot be built without ``parent_request_id`` (AppContext refuses it), so the gate is
    proven alone on a context that only flips ``system_run`` after construction."""
    ctx = _person_ctx()
    object.__setattr__(ctx, "system_run", True)
    assert ctx.parent_request_id is None
    assert _allowed(ctx) is False


def test_a_workflow_step_or_child_run_that_inherits_the_reads_never_holds() -> None:
    """The real forks copy the parent's metadata (``client_reads`` included) and are refused by P3 anyway:
    a workflow step is an internal agent, a child agent run has its parent's request."""
    parent = _person_ctx(request_id="33333333-3333-3333-3333-333333333333")
    step = parent.fork_for_workflow_step("44444444-4444-4444-4444-444444444444")
    child = parent.fork_for_child_agent("55555555-5555-5555-5555-555555555555")
    assert step.metadata.get("client_reads") == list(BOTH), "the step really carries the person read"
    assert _allowed(step) is False
    assert child.parent_request_id == parent.request_id, "the child names its caller's turn"
    assert _allowed(child) is False


@pytest.mark.asyncio
async def test_a_checkpoint_that_raises_parks_without_a_hold(monkeypatch) -> None:
    from matrx_connect.streaming import error_capture

    captured: list[str] = []

    async def capture(exc, **kw):
        captured.append(kw.get("kind"))

    monkeypatch.setattr(error_capture, "capture_error", capture)
    run = _Run(monkeypatch, reads=BOTH)

    async def broken():
        raise ConnectionError("pool: the assistant row could not be flushed")

    run.checkpoint = True
    original = run.hold_for_person

    async def with_broken_checkpoint():
        token = set_app_context(AppContext(emitter=run.emitter, store=True, metadata=run.metadata))
        try:
            executor = ToolExecutor(registry=SimpleNamespace(bindings_for_tool=lambda _name: []))
            return await executor._hold_for_person(
                ToolDefinition(name="ask_person"),
                ToolContext(call_id="call-ask", tool_name="ask_person", conversation_id=CONV,
                            emitter=run.emitter, assistant_checkpoint=broken),
                "tool-row", 0.0,
            )
        finally:
            clear_app_context(token)

    del original
    assert await with_broken_checkpoint() is None, "never an exception out of execute"
    assert run.claims == [] and run.infos == []
    assert captured == ["person_hold_checkpoint_failed"], "the failure is announced"


@pytest.mark.asyncio
async def test_a_give_up_whose_read_failed_still_takes_a_result_resolved_under_the_lease(monkeypatch) -> None:
    resolved_under_lease = SimpleNamespace(id="row-1", status="completed", resolved_at=datetime.now(UTC),
                                           held_until=datetime.now(UTC) + timedelta(seconds=20), is_error=False)
    reads = {"n": 0}

    async def flaky_read(_row_id):
        reads["n"] += 1
        if reads["n"] == 1:
            raise ConnectionError("read reset")
        return resolved_under_lease

    async def failed_write(*_a, **_k):
        return 0  # the release found nothing to release: a result landed first

    async def quiet(*_a, **_k):
        return None

    monkeypatch.setattr(hold, "_hooks", _hooks())
    monkeypatch.setattr(hold, "_read_row", flaky_read)
    monkeypatch.setattr(hold, "_write", failed_write)
    monkeypatch.setattr(hold, "_report", quiet)
    outcome = await hold._give_up("row-1", conversation_id="conv", reason="timeout", started=0.0)
    assert outcome.taken is True and outcome.row is resolved_under_lease, (
        "its resolver told the caller the open stream continues: parking here would strand the turn"
    )


@pytest.mark.asyncio
async def test_a_give_up_that_cannot_read_at_all_parks_without_raising(monkeypatch) -> None:
    async def down(*_a, **_k):
        raise ConnectionError("database unreachable")

    async def quiet(*_a, **_k):
        return None

    monkeypatch.setattr(hold, "_hooks", _hooks())
    monkeypatch.setattr(hold, "_read_row", down)
    monkeypatch.setattr(hold, "_write", down)
    monkeypatch.setattr(hold, "_report", quiet)
    outcome = await hold._give_up("row-1", conversation_id="conv", reason="timeout", started=0.0)
    assert outcome.taken is False and outcome.reason == "database"


@pytest.mark.asyncio
async def test_an_ask_answered_during_a_slow_sibling_continues_in_place(monkeypatch) -> None:
    """Nothing held: the ask was answered (plain compare-and-set) while a slow server tool in the same reply
    still ran. The run holds the claim, so nobody else can continue it: the batch takes the answer itself."""
    from matrx_ai.db import cxm
    from matrx_ai.tools import handle_tool_calls as htc
    from matrx_ai.tools.models import ToolResult

    answered = SimpleNamespace(**{**vars(_answered_row()), "resolved_at": datetime.now(UTC), "held_until": None,
                                  "is_client_delegated": True})

    class Executor:
        async def execute_batch(self, calls, ctx, *, client_tools=None, allowed_tools=None):
            slow = ToolResult(success=True, output={"rows": 3}, tool_name="table_query", call_id="call-slow")
            ask = ToolResult(success=False, delegated_pending=True, tool_name="ask_person", call_id="call-ask")
            return ([{"call_id": "call-slow", "content": "3 rows"}, ask.to_tool_result_content()], [slow, ask])

    async def read(**kw):
        return [answered] if kw.get("call_id") == "call-ask" else []

    monkeypatch.setattr(htc, "get_executor", lambda: Executor())
    monkeypatch.setattr(htc.ToolLifecycleManager, "get_instance", lambda: SimpleNamespace(sweep_running=True))
    monkeypatch.setattr(cxm.tool_call, "filter_items", read)
    token = set_app_context(AppContext(emitter=SimpleNamespace(), conversation_id=CONV, store=True))
    try:
        content, _usages, pending, *_rest = await htc.handle_tool_calls_v2(
            [{"call_id": "call-slow", "name": "table_query", "arguments": {}},
             {"call_id": "call-ask", "name": "ask_person", "arguments": {}}],
            iteration=1,
        )
    finally:
        clear_app_context(token)
    assert pending == [], "the answered ask is no longer open: the turn continues instead of parking"
    assert _rebuild_tool_result_content([answered])[0] in content
