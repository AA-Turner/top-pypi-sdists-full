"""A signed-out guest gets N free AI actions; the next NEW action is refused.

SUT: ``UnifiedAIClient._dispatch_with_billing_net`` — the one seam every paid
provider call passes — and the gate it calls,
``matrx_ai.providers.guest_ai_allowance.admit_guest_ai_action``.

Doubles: the two registry managers (``users.guest_executions`` and
``users.guest_execution_log``, behaving like the tables: count / exists /
create on real column filters) and the provider dispatch itself (a coroutine
that records that it ran — the stand-in for "money was spent").

Breaks named:
* nothing counts guest AI use → the 4th action reaches the provider;
* the refusal arrives after the provider was called (money already spent);
* the refusal's code or numbers drift from the envelope the client parses;
* a signed-in person is counted or refused;
* one action's sub-agents / tool-loop iterations / concurrent helpers (same
  carried request_id) count more than once;
* the count is per process only — a second process (memo empty) re-counts an
  action already in the durable ledger;
* an unreadable allowance blocks the guest or passes silently.
"""

from __future__ import annotations

import asyncio
import itertools
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_connect.emitters.silent_emitter import SilentEmitter

from matrx_ai.db import _registry
from matrx_ai.providers import guest_ai_allowance as gate
from matrx_ai.providers.unified_client import UnifiedAIClient

FP = "3f9a1c0b7d2e4f6a8b0c1d2e3f4a5b6c"
GUEST_UUID = "6b1f6f8e-2d0c-4a55-9b7e-1c2d3e4f5a6b"
PROFILE = SimpleNamespace(
    vendor="openai",
    model_name="gpt-test",
    endpoint_id="openai-test",
    base_url=None,
    offering_metadata={},
)


class _Guests:
    def __init__(self) -> None:
        self.rows = [SimpleNamespace(id="guest-row-1", fingerprint=FP, auth_user_id=GUEST_UUID)]

    async def filter_all_guest_executions(self, **kw: Any) -> list[SimpleNamespace]:
        await asyncio.sleep(0)
        return [r for r in self.rows if all(getattr(r, k) == v for k, v in kw.items())]


class _Ledger:
    """users.guest_execution_log: append-only rows filtered by column."""

    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []
        self._ids = itertools.count(1)

    def _match(self, kw: dict[str, Any]) -> list[dict[str, Any]]:
        return [r for r in self.rows if all(r.get(k) == v for k, v in kw.items())]

    async def exists(self, **kw: Any) -> bool:
        await asyncio.sleep(0)
        return bool(self._match(kw))

    async def count(self, **kw: Any) -> int:
        await asyncio.sleep(0)
        return len(self._match(kw))

    async def create_guest_execution_log(self, **data: Any) -> dict[str, Any]:
        await asyncio.sleep(0)
        row = {"id": next(self._ids), **data}
        self.rows.append(row)
        return row

    def ai_rows(self) -> list[dict[str, Any]]:
        return self._match({"resource_type": "ai_action"})


@pytest.fixture
def tables(monkeypatch: pytest.MonkeyPatch) -> SimpleNamespace:
    guests, ledger = _Guests(), _Ledger()
    real_get = _registry.get_instance

    def _get(name: str) -> Any:
        if name == "guest_executions_manager":
            return guests
        if name == "guest_execution_log_manager":
            return ledger
        return real_get(name)

    monkeypatch.setattr(_registry, "get_instance", _get)

    async def _three() -> int:
        return 3

    gate.set_guest_ai_allowance_resolver(_three)
    gate.reset_guest_ai_allowance_state()
    yield SimpleNamespace(guests=guests, ledger=ledger)
    gate.set_guest_ai_allowance_resolver(None)
    gate.reset_guest_ai_allowance_state()


def _guest_ctx(request_id: str) -> AppContext:
    return AppContext(
        emitter=SilentEmitter(),
        user_id=GUEST_UUID,
        auth_type="fingerprint",
        is_authenticated=False,
        fingerprint_id=FP,
        request_id=request_id,
    )


def _signed_in_ctx(request_id: str) -> AppContext:
    return AppContext(
        emitter=SilentEmitter(),
        user_id="0f0e0d0c-0b0a-4908-8706-050403020100",
        auth_type="token",
        is_authenticated=True,
        request_id=request_id,
    )


async def _paid_call(ctx: AppContext, spent: list[str]) -> Any:
    """One paid provider call under ``ctx`` — through the real seam."""
    token = set_app_context(ctx)
    try:

        async def _provider() -> str:
            spent.append(ctx.request_id)
            return "ok"

        return await UnifiedAIClient._dispatch_with_billing_net(_provider, profile=PROFILE)
    finally:
        clear_app_context(token)


def _rid(n: int) -> str:
    return f"00000000-0000-4000-8000-{n:012d}"


def test_guest_fourth_action_is_refused_before_the_provider(tables: SimpleNamespace) -> None:
    spent: list[str] = []

    async def _run() -> BaseException | None:
        for n in (1, 2, 3):
            assert await _paid_call(_guest_ctx(_rid(n)), spent) == "ok"
        try:
            await _paid_call(_guest_ctx(_rid(4)), spent)
        except BaseException as exc:  # noqa: BLE001
            return exc
        return None

    refused = asyncio.run(_run())
    assert isinstance(refused, gate.GuestAIAllowanceUsedError)
    assert spent == [_rid(1), _rid(2), _rid(3)], "the 4th action reached the provider"
    assert refused.envelope() == {
        "error": "guest_ai_allowance_used",
        "message": "You've used your free AI tries. Create a free account to keep going.",
        "allowance": 3,
        "used": 3,
    }
    # The stream contract: the executor and the stream crash handler read error_info.
    assert refused.error_info.error_type == "guest_ai_allowance_used"
    assert refused.error_info.is_retryable is False
    assert refused.error_info.status_code == 403
    assert refused.error_info.details == {"allowance": 3, "used": 3}
    assert refused.is_caller_refusal is True
    assert len(tables.ledger.ai_rows()) == 3, "a refused action must not be recorded as used"


def test_signed_in_person_is_never_counted_or_refused(tables: SimpleNamespace) -> None:
    spent: list[str] = []

    async def _run() -> None:
        for n in range(1, 11):
            await _paid_call(_signed_in_ctx(_rid(100 + n)), spent)

    asyncio.run(_run())
    assert len(spent) == 10
    assert tables.ledger.rows == [], "a signed-in call touched the guest ledger"


def test_one_action_counts_once_across_sub_agents_and_iterations(tables: SimpleNamespace) -> None:
    spent: list[str] = []

    async def _run() -> None:
        ctx = _guest_ctx(_rid(7))
        # A sub-agent forked mid-run keeps the parent's request_id.
        child = ctx.fork_for_child_agent(new_conversation_id="11111111-1111-4111-8111-111111111111")
        assert child.request_id == ctx.request_id
        # Parent loop iterations + concurrent sub-agent calls + a background helper.
        await asyncio.gather(
            _paid_call(ctx, spent),
            _paid_call(child, spent),
            _paid_call(child, spent),
            _paid_call(ctx, spent),
        )
        await _paid_call(ctx, spent)

    asyncio.run(_run())
    assert len(spent) == 5
    assert [r["resource_id"] for r in tables.ledger.ai_rows()] == [_rid(7)]


def test_durable_ledger_dedups_across_processes(tables: SimpleNamespace) -> None:
    spent: list[str] = []

    async def _run() -> None:
        await _paid_call(_guest_ctx(_rid(8)), spent)
        gate.reset_guest_ai_allowance_state()  # a second worker process: empty memo
        await _paid_call(_guest_ctx(_rid(8)), spent)

    asyncio.run(_run())
    assert len(tables.ledger.ai_rows()) == 1


def test_new_conversation_does_not_reset_the_count(tables: SimpleNamespace) -> None:
    """The count is per guest identity, not per conversation or feature."""
    spent: list[str] = []
    for n in (1, 2, 3):
        tables.ledger.rows.append(
            {"guest_id": "guest-row-1", "resource_type": "ai_action", "resource_id": _rid(200 + n)}
        )
    # Non-AI guest activity in the same log never counts.
    tables.ledger.rows.append(
        {"guest_id": "guest-row-1", "resource_type": "conversation", "resource_id": "c"}
    )

    async def _run() -> BaseException | None:
        try:
            await _paid_call(_guest_ctx(_rid(300)), spent)
        except BaseException as exc:  # noqa: BLE001
            return exc
        return None

    assert isinstance(asyncio.run(_run()), gate.GuestAIAllowanceUsedError)
    assert spent == []


def test_unreadable_allowance_allows_and_records_loudly(
    tables: SimpleNamespace, monkeypatch: pytest.MonkeyPatch
) -> None:
    recorded: list[dict[str, Any]] = []

    async def _record_error(exc: BaseException, **kw: Any) -> None:
        recorded.append({"exc": exc, **kw})

    monkeypatch.setattr("matrx_orm.record_error", _record_error)

    async def _broken() -> int:
        raise RuntimeError("knob auth.guest_ai/free_ai_actions is not seeded")

    gate.set_guest_ai_allowance_resolver(_broken)
    spent: list[str] = []
    asyncio.run(_paid_call(_guest_ctx(_rid(9)), spent))
    assert spent == [_rid(9)], "an unreadable allowance must not block the guest"
    assert [r["kind"] for r in recorded] == ["guest_ai_allowance_unreadable"]


# --- the executor's stream path ----------------------------------------------
# The chat/agent/sub-agent path: the refusal surfaces from the provider client
# inside ``_execute_until_complete_inner``. Harness shared with the
# out-of-credit terminal test (same doubles: only what the loop CALLS).


@pytest.mark.asyncio
async def test_executor_streams_the_refusal_code_and_files_no_incident(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from test_provider_out_of_credit_terminal import _run

    import matrx_ai.orchestrator.executor as executor_mod

    # capture_issue (stubbed by the shared harness) and this terminal capture sit
    # in the same skipped block; recording the latter proves the skip.
    terminal: list[Any] = []

    async def _terminal(*a: Any, **k: Any) -> None:
        terminal.append((a, k))

    monkeypatch.setattr(executor_mod, "_capture_terminal_provider_failure", _terminal)
    run = await _run(monkeypatch, gate.GuestAIAllowanceUsedError(allowance=3, used=3))

    assert run["client"].calls == 1, "a caller refusal was retried"
    assert len(run["errors"]) == 1, run["errors"]
    event = run["errors"][0]
    assert event["error_type"] == "guest_ai_allowance_used"
    assert event["code"] == "guest_ai_allowance_used"
    assert event["details"] == {"allowance": 3, "used": 3}
    assert event["user_message"] == gate.GUEST_AI_ALLOWANCE_MESSAGE
    assert terminal == [], "an expected refusal was filed as a provider failure"
    assert run["captured"] == [], "an expected refusal wrote a system_error"


# --- the request-boundary pre-check -------------------------------------------
# Break named: an exhausted guest's 4th message was stored, then refused at the
# seam mid-run, leaving a failed turn in the transcript.


def _seed_used(tables: SimpleNamespace, n: int) -> None:
    for i in range(n):
        tables.ledger.rows.append(
            {"guest_id": "guest-row-1", "resource_type": "ai_action", "resource_id": _rid(500 + i)}
        )


async def _in_ctx(ctx: AppContext, coro_fn: Any) -> Any:
    token = set_app_context(ctx)
    try:
        return await coro_fn()
    finally:
        clear_app_context(token)


def test_precheck_refuses_an_exhausted_guest_and_writes_nothing(tables: SimpleNamespace) -> None:
    _seed_used(tables, 3)
    before = list(tables.ledger.rows)

    async def _run() -> BaseException | None:
        try:
            await _in_ctx(_guest_ctx(_rid(600)), gate.precheck_guest_ai_action)
        except BaseException as exc:  # noqa: BLE001
            return exc
        return None

    refused = asyncio.run(_run())
    assert isinstance(refused, gate.GuestAIAllowanceUsedError)
    assert refused.envelope()["used"] == 3
    assert tables.ledger.rows == before, "the pre-check must never write the ledger"


def test_precheck_passes_under_the_allowance_and_for_signed_in(tables: SimpleNamespace) -> None:
    _seed_used(tables, 2)
    asyncio.run(_in_ctx(_guest_ctx(_rid(601)), gate.precheck_guest_ai_action))
    _seed_used(tables, 5)
    asyncio.run(_in_ctx(_signed_in_ctx(_rid(602)), gate.precheck_guest_ai_action))
    assert len(tables.ledger.ai_rows()) == 7, "the pre-check wrote a row"


def test_ensure_user_request_refuses_before_the_request_row_is_created(
    tables: SimpleNamespace, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The boundary every persisted AI route crosses in prep refuses first."""
    from matrx_ai.db import conversation_gate

    _seed_used(tables, 3)
    created: list[str] = []

    async def _create(*, request_id: str, user_id: str | None) -> None:
        created.append(request_id)

    async def _no_rows(**_: Any) -> list[Any]:
        return []

    async def _no_store(*_: Any) -> bool:
        return False

    monkeypatch.setattr(conversation_gate, "_store_pending_user_request", _no_store)
    monkeypatch.setattr(conversation_gate, "_create_user_request", _create)
    monkeypatch.setattr(
        conversation_gate,
        "_cxm",
        lambda: SimpleNamespace(user_request=SimpleNamespace(filter_user_requests=_no_rows)),
    )
    monkeypatch.setattr(conversation_gate, "_require_persistence_actor", lambda uid, _c: uid)

    async def _run() -> BaseException | None:
        try:
            await _in_ctx(
                _guest_ctx(_rid(700)),
                lambda: conversation_gate.ensure_user_request_exists(_rid(700), GUEST_UUID),
            )
        except BaseException as exc:  # noqa: BLE001
            return exc
        return None

    assert isinstance(asyncio.run(_run()), gate.GuestAIAllowanceUsedError)
    assert created == [], "the request row was created for a refused guest action"

    # Under the allowance the same boundary proceeds.
    tables.ledger.rows.clear()
    asyncio.run(
        _in_ctx(
            _guest_ctx(_rid(701)),
            lambda: conversation_gate.ensure_user_request_exists(_rid(701), GUEST_UUID),
        )
    )
    assert created == [_rid(701)]
