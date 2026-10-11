"""The run-approval gate: a waiting/rejected agent, mandate or automation is refused at the
paid-call seam BEFORE money is spent — once per request, from memory, never a person's own turn.

SUT: ``UnifiedAIClient._dispatch_with_billing_net`` (the one seam every paid provider call
passes) and ``matrx_ai.providers.run_approval_gate``.

Doubles: the host resolver (a dict keyed by agent id, with a call log) and the provider
dispatch (a coroutine recording that money was spent).

Breaks named:
* a held subject reaches the provider (money spent with no approval);
* the refusal is silent or carries no link to its approval;
* a person's own interactive turn (human / delegated_member) is held;
* a run admitted at its first paid call is cut off at a later one (a run is a request);
* no resolver / a raising resolver blocks work.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_connect.emitters.silent_emitter import SilentEmitter

from matrx_ai.providers import run_approval_gate as gate
from matrx_ai.providers.unified_client import UnifiedAIClient

USER = "0f0e0d0c-0b0a-4908-8706-050403020100"
HELD_AGENT = "1b941f40-e846-4828-a9cb-4f3da7f19df7"
FREE_AGENT = "6b6b4e45-4699-4860-8dea-d8a60e07d69a"
URL = "https://manage.aimatrx.com/administration/billing/approvals?id=ap-1"
PROFILE = SimpleNamespace(
    vendor="openai", model_name="gpt-test", endpoint_id="openai-test", base_url=None, offering_metadata={}
)


class _Memory:
    def __init__(self) -> None:
        self.held: set[str] = set()
        self.asked: list[str] = []

    def __call__(self, ctx: Any) -> gate.RunApprovalRequiredError | None:
        self.asked.append(str(ctx.request_id))
        if str(getattr(ctx, "agent_id", "") or "") in self.held:
            return gate.RunApprovalRequiredError(
                approval_id="ap-1", subject_kind="agent", subject_id=str(ctx.agent_id),
                status="waiting", approval_url=URL,
            )
        return None


@pytest.fixture
def memory() -> _Memory:
    mem = _Memory()
    gate.set_run_approval_resolver(mem)
    gate.reset_run_approval_gate_state()
    yield mem
    gate.set_run_approval_resolver(None)
    gate.reset_run_approval_gate_state()


def _rid(n: int) -> str:
    return f"00000000-0000-4000-8000-{n:012d}"


def _ctx(request_id: str, *, agent_id: str = HELD_AGENT, origin_class: str = "scheduled") -> AppContext:
    return AppContext(
        emitter=SilentEmitter(), user_id=USER, auth_type="token", is_authenticated=True,
        request_id=request_id, agent_id=agent_id, origin_class=origin_class,
    )


async def _paid_call(ctx: AppContext, spent: list[str]) -> BaseException | None:
    token = set_app_context(ctx)
    try:

        async def _provider() -> str:
            spent.append(ctx.request_id)
            return "ok"

        await UnifiedAIClient._dispatch_with_billing_net(_provider, profile=PROFILE)
    except BaseException as exc:  # noqa: BLE001
        return exc
    finally:
        clear_app_context(token)
    return None


def test_a_held_subject_is_refused_before_the_provider_with_its_link(memory: _Memory) -> None:
    memory.held.add(HELD_AGENT)
    spent: list[str] = []
    exc = asyncio.run(_paid_call(_ctx(_rid(1)), spent))
    assert isinstance(exc, gate.RunApprovalRequiredError)
    assert spent == []
    # The person reads plain words; the id and admin link live only in the technical text + envelope.
    assert URL not in str(exc) and "approval limit" in str(exc)
    assert URL in exc.technical_message
    assert exc.envelope()["approval_url"] == URL
    assert exc.is_caller_refusal is True
    assert exc.error_info.is_retryable is False


def test_an_unheld_subject_runs(memory: _Memory) -> None:
    memory.held.add(HELD_AGENT)
    spent: list[str] = []
    assert asyncio.run(_paid_call(_ctx(_rid(2), agent_id=FREE_AGENT), spent)) is None
    assert spent == [_rid(2)]


@pytest.mark.parametrize("origin", ["human", "delegated_member"])
def test_a_persons_own_turn_is_never_held(memory: _Memory, origin: str) -> None:
    memory.held.add(HELD_AGENT)
    spent: list[str] = []
    assert asyncio.run(_paid_call(_ctx(_rid(3), origin_class=origin), spent)) is None
    assert spent == [_rid(3)]
    assert memory.asked == []


@pytest.mark.parametrize("origin", ["scheduled", "workflow", "child_agent", "api", "system", "client_auto"])
def test_every_machine_origin_is_gated(memory: _Memory, origin: str) -> None:
    memory.held.add(HELD_AGENT)
    spent: list[str] = []
    exc = asyncio.run(_paid_call(_ctx(_rid(4), origin_class=origin), spent))
    assert isinstance(exc, gate.RunApprovalRequiredError)
    assert spent == []


def test_a_running_run_is_never_cut_in_half(memory: _Memory) -> None:
    spent: list[str] = []
    ctx = _ctx(_rid(5))
    assert asyncio.run(_paid_call(ctx, spent)) is None
    memory.held.add(HELD_AGENT)  # the run crossed the line and was flagged mid-flight
    assert asyncio.run(_paid_call(ctx, spent)) is None
    assert spent == [_rid(5), _rid(5)]
    assert memory.asked == [_rid(5)]  # decided once per request
    # the NEXT run waits
    assert isinstance(asyncio.run(_paid_call(_ctx(_rid(6)), spent)), gate.RunApprovalRequiredError)


def test_no_resolver_gates_nothing() -> None:
    gate.set_run_approval_resolver(None)
    gate.reset_run_approval_gate_state()
    spent: list[str] = []
    assert asyncio.run(_paid_call(_ctx(_rid(7)), spent)) is None
    assert spent == [_rid(7)]


def test_a_raising_resolver_admits_the_run() -> None:
    def broken(_ctx: Any) -> None:
        raise RuntimeError("memory gone")

    gate.set_run_approval_resolver(broken)
    gate.reset_run_approval_gate_state()
    try:
        spent: list[str] = []
        assert asyncio.run(_paid_call(_ctx(_rid(8)), spent)) is None
        assert spent == [_rid(8)]
    finally:
        gate.set_run_approval_resolver(None)


def test_the_refusal_is_found_through_wrapping_layers() -> None:
    inner = gate.RunApprovalRequiredError(
        approval_id="ap-1", subject_kind="mandate", subject_id="seo.x", status="rejected", approval_url=URL
    )
    try:
        try:
            raise inner
        except gate.RunApprovalRequiredError as e:
            raise RuntimeError("mandate failed") from e
    except RuntimeError as outer:
        assert gate.run_approval_refusal_in(outer) is inner
    assert "declined" in str(inner) and "was rejected" in inner.technical_message
