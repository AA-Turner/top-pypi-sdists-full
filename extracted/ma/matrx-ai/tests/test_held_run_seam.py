"""A refused run is HELD, not lost: every gate refusal at the one paid-call seam hands the host
what the run was about to send (Arman, 2026-10-11: "If we are not saving the exact run so that I can
go and watch it run one time ... then it's not helping me").

SUT: ``UnifiedAIClient._dispatch_with_billing_net`` + ``providers/held_run_seam.py``. The recorder
sees the refusal, the request config (messages, model, tools) and the agent facts ``Agent.execute``
noted (agent id, version flag, variables, user input). A broken recorder never changes the refusal.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_connect.emitters.silent_emitter import SilentEmitter

from matrx_ai.providers import held_run_seam as seam
from matrx_ai.providers import run_approval_gate as gate
from matrx_ai.providers.unified_client import UnifiedAIClient

USER = "0f0e0d0c-0b0a-4908-8706-050403020100"
AGENT = "1b941f40-e846-4828-a9cb-4f3da7f19df7"
PROFILE = SimpleNamespace(
    vendor="openai", model_name="gpt-test", endpoint_id="openai-test", base_url=None, offering_metadata={}
)
CONFIG = SimpleNamespace(model="gpt-test", messages=["system: judge", "user: compare"], tools=["web_search"])


def _refuse(ctx: Any) -> gate.RunApprovalRequiredError:
    return gate.RunApprovalRequiredError(
        approval_id="", subject_kind="protected_account", subject_id=str(ctx.user_id),
        status="refused", approval_url="",
    )


@pytest.fixture
def recorded() -> list[dict[str, Any]]:
    seen: list[dict[str, Any]] = []

    def _recorder(exc: BaseException, ctx: Any, config: Any, profile: Any, agent: dict[str, Any] | None) -> None:
        seen.append({"exc": exc, "ctx": ctx, "config": config, "profile": profile, "agent": agent})

    seam.set_held_run_recorder(_recorder)
    gate.set_run_approval_resolver(_refuse)
    gate.reset_run_approval_gate_state()
    yield seen
    seam.set_held_run_recorder(None)
    gate.set_run_approval_resolver(None)
    gate.reset_run_approval_gate_state()


async def _paid_call(request_id: str, spent: list[str]) -> BaseException | None:
    ctx = AppContext(
        emitter=SilentEmitter(), user_id=USER, auth_type="token", is_authenticated=True,
        request_id=request_id, agent_id=AGENT, origin_class="system",
    )
    token = set_app_context(ctx)
    facts = seam.note_agent_run(
        agent_id=AGENT, is_version=False, variables={"question": "Is the replay better?"}, user_input=None,
        name="Hindsight Replay Judge",
    )
    try:

        async def _provider() -> str:
            spent.append(request_id)
            return "ok"

        await UnifiedAIClient._dispatch_with_billing_net(_provider, profile=PROFILE, config=CONFIG)
    except BaseException as exc:  # noqa: BLE001
        return exc
    finally:
        seam.reset_agent_run(facts)
        clear_app_context(token)
    return None


def test_a_refused_run_hands_the_host_what_it_would_have_sent(recorded: list[dict[str, Any]]) -> None:
    spent: list[str] = []
    exc = asyncio.run(_paid_call("00000000-0000-4000-8000-000000000001", spent))
    assert isinstance(exc, gate.RunApprovalRequiredError)
    assert spent == []
    assert len(recorded) == 1
    held = recorded[0]
    assert held["exc"] is exc
    assert held["config"] is CONFIG
    assert held["profile"] is PROFILE
    assert held["ctx"].request_id == "00000000-0000-4000-8000-000000000001"
    assert held["agent"]["agent_id"] == AGENT
    assert held["agent"]["variables"] == {"question": "Is the replay better?"}


def test_a_broken_recorder_never_changes_the_refusal(recorded: list[dict[str, Any]]) -> None:
    def _boom(*_: Any) -> None:
        raise RuntimeError("recorder down")

    seam.set_held_run_recorder(_boom)
    spent: list[str] = []
    exc = asyncio.run(_paid_call("00000000-0000-4000-8000-000000000002", spent))
    assert isinstance(exc, gate.RunApprovalRequiredError)
    assert spent == []


def test_an_admitted_run_records_nothing(recorded: list[dict[str, Any]]) -> None:
    gate.set_run_approval_resolver(lambda _ctx: None)
    spent: list[str] = []
    assert asyncio.run(_paid_call("00000000-0000-4000-8000-000000000003", spent)) is None
    assert spent == ["00000000-0000-4000-8000-000000000003"]
    assert recorded == []


def test_the_agent_facts_are_gone_after_the_run() -> None:
    token = seam.note_agent_run(agent_id=AGENT, is_version=True, variables={}, user_input="hi", name="x")
    assert seam.current_agent_run()["is_version"] is True
    seam.reset_agent_run(token)
    assert seam.current_agent_run() is None
