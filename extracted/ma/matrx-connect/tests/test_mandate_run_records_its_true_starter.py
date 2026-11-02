"""Every way a mandate run can start records its TRUE starter on the conversation and the ledger.

Found 2026-10-16 (Arman: "All of the agent calls ... have been improperly marked"): every
server-side mandate run that ``run_mandate`` / a named agent / the factory forked from machine
work with no caller conversation was persisted ``origin_class='child_agent'`` — "started by
another agent" — although no agent started it. Live, last 30 days: 1,424 aidream root runs from
services, 771 MCP-agent-service / factory runs, 687 runs inside workflow runs (with the run id on
the row), 240 inside schedule runs.

Persistence reads ``reconcile_origin`` — the one seam that stamps ``chat.conversation`` and
``chat.user_request`` (which ``runtime._ai_calls.origin`` reads). Gates keep reading the DECLARED
``ctx.origin_class`` (still ``child_agent`` for a machine-parent fork) so no gate moves.

The GUARD (``test_no_server_side_starter_is_ever_stored_as_a_person_or_a_child``): every
server-side starter is enumerated; none may persist as ``human`` / ``client_auto`` or as
``child_agent`` without a parent conversation.
"""

from __future__ import annotations

import pytest

from matrx_connect import AppContext, reconcile_origin
from matrx_connect.emitters.console_emitter import ConsoleEmitter

CONV = "10101010-1010-4010-8010-101010101010"
CHILD = "20202020-2020-4020-8020-202020202020"
RUN = "30303030-3030-4030-8030-303030303030"


def _ctx(**overrides) -> AppContext:
    return AppContext(emitter=ConsoleEmitter("test", accumulate=False), **overrides)


def _persisted(ctx: AppContext) -> str:
    return reconcile_origin(ctx)[0]


# (starter name, the context the mandate run is started FROM, what it must record)
def _starters() -> list[tuple[str, AppContext, str]]:
    workflow_step = _ctx(
        execution_kind="workflow_run", execution_id=RUN, request_id="r-wf"
    ).fork_for_workflow_step(CONV)
    return [
        # ai.mandate.start node: the step context itself runs the agent.
        ("workflow node (ai.mandate.start)", workflow_step, "workflow"),
        # A service a workflow node calls, which calls run_mandate -> child_agent_context.
        ("run_mandate inside a workflow step", workflow_step.fork_for_child_agent(CHILD), "workflow"),
        # A service running under system_app_context / detached_task (the factory pipeline, sweeps).
        (
            "run_mandate from a system service / agent factory",
            _ctx(origin_class="system", request_id="r-sys", source_app="mcp-agent-service",
                 source_feature="agent-factory").fork_for_child_agent(CHILD),
            "system",
        ),
        # The scheduler's run context.
        (
            "run_mandate from a schedule",
            _ctx(origin_class="scheduled", conversation_type="scheduled", execution_kind="sch_run", execution_id=RUN,
                 request_id="r-sch").fork_for_child_agent(CHILD),
            "scheduled",
        ),
        # Background work that named no class at all.
        ("run_mandate from blank background work", _ctx(request_id="r-bg").fork_for_child_agent(CHILD), "system"),
    ]


@pytest.mark.parametrize("name,ctx,expected", _starters(), ids=[s[0] for s in _starters()])
def test_server_side_starter_records_its_true_origin(name: str, ctx: AppContext, expected: str) -> None:
    final, witness = reconcile_origin(ctx)
    assert final == expected, f"{name} persisted {final!r}, its starter is {expected!r}"
    assert "contradictions" not in witness


def test_the_gates_still_read_the_declared_fork_class() -> None:
    """Persistence-only: the usage gate leaves system/scheduled ungated, so the DECLARED class a
    machine-parent fork carries (what every gate reads) must not move."""
    for klass in ("system", "scheduled", "workflow"):
        root = _ctx(origin_class=klass).fork_for_child_agent(CHILD)
        assert root.origin_class == "child_agent"


def test_mcp_agent_service_http_caller_is_api() -> None:
    mcp = _ctx(route="mcp:agent_run", auth_type="token", is_authenticated=True,
               source_app="mcp-agent-service", source_feature="agent-service")
    assert _persisted(mcp.fork_for_child_agent(CHILD)) == "api"


def test_a_person_in_chat_stays_human() -> None:
    person = _ctx(origin_class="human", route="/ai/chat", auth_type="token", conversation_id=CONV)
    assert _persisted(person) == "human"


def test_a_real_sub_agent_of_a_running_conversation_stays_child_agent() -> None:
    for parent in (
        _ctx(origin_class="system", conversation_id=CONV),
        _ctx(origin_class="human", route="/ai/chat", auth_type="token", conversation_id=CONV),
    ):
        child = parent.fork_for_child_agent(CHILD)
        assert child.parent_conversation_id == CONV
        assert _persisted(child) == "child_agent"


def test_no_server_side_starter_is_ever_stored_as_a_person_or_a_child() -> None:
    """THE GUARD. A server-side mandate run is never a person, never a chat, never an
    orphan 'child'."""
    for name, ctx, _ in _starters():
        final = _persisted(ctx)
        assert final not in ("human", "client_auto"), f"{name} stored as a person: {final!r}"
        assert ctx.conversation_type != "standard", f"{name} stored as a chat conversation"
        if final == "child_agent":
            assert ctx.parent_conversation_id, f"{name} stored as a child with no parent"
