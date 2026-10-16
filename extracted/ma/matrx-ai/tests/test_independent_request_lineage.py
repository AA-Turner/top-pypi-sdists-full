"""Every independent child run is its own request record, LINKED to its parent.

Agent Factory review 4 N4-7 (live build 38ffaf7f): five sequential mandate runs in one
ambient context all reported the goal step's ``request_id``; only that run got a
``chat.user_request`` row, and the others' ``chat.request.user_request_id`` pointed into
another conversation. Now a mandate run is ``independent_request=True`` (its own row) and
that row carries ``metadata.parent_request_id`` — lineage kept, per-run joins correct.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

USER_ID = "22222222-2222-2222-2222-222222222222"
PARENT = "33333333-3333-3333-3333-333333333333"


@pytest.mark.asyncio
async def test_sequential_independent_runs_each_get_their_own_request_linked_to_the_parent():
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext, set_app_context

    from matrx_ai.agents.executor import run_agent
    from matrx_ai.db.conversation_gate import PARENT_REQUEST_ID_KEY, _lineage_metadata, mark_request_durable

    # R45: a link names only a request with a record — this parent has one (a spine
    # request / an ensured user_request); a recordless parent gets no link
    # (test_tree_cap_has_no_side_doors.py).
    mark_request_durable(PARENT)
    set_app_context(AppContext(emitter=ConsoleEmitter(), user_id=USER_ID, request_id=PARENT, store=False))
    seen: list[dict[str, Any]] = []

    async def _capture_execute(user_input: Any = None, *, max_iterations: Any = None, **_: Any) -> Any:
        from matrx_connect.context.app_context import get_app_context

        ctx = get_app_context()
        seen.append({"request_id": ctx.request_id, "lineage": _lineage_metadata(ctx),
                     "completion": dict(agents[-1].request_metadata)})
        return SimpleNamespace(
            output="ok", assistant_response=None, config=SimpleNamespace(model="m", metadata={}),
            usage=None, usage_history=[], metadata={},
        )

    agents: list[Any] = []
    for step in ("goal", "tool_choice", "instructions"):
        agent = SimpleNamespace(
            name=step, config=SimpleNamespace(model="m", metadata={}), source_id=None,
            source_is_version=False, execute=_capture_execute, request_metadata={"mandate_key": step},
        )
        agents.append(agent)
        result = await run_agent(agent, label=step, source_app="t", source_feature=step,  # type: ignore[arg-type]
                                 emit_lifecycle=False, system_run=True, independent_request=True)
        assert result.success

    ids = [s["request_id"] for s in seen]
    assert len(set(ids)) == 3 and PARENT not in ids, ids
    assert all(s["lineage"] == {PARENT_REQUEST_ID_KEY: PARENT} for s in seen), seen
    # The completion write replaces the row's metadata with the agent's request metadata
    # (live 20dbbff4: every step row lost the link at completion) — the link rides there too.
    assert all(s["completion"].get(PARENT_REQUEST_ID_KEY) == PARENT for s in seen), seen


@pytest.mark.asyncio
async def test_a_shared_child_run_keeps_the_parent_request_and_claims_no_lineage():
    """``independent_request=False`` (agent_call's sub-steps) is unchanged: the parent's id."""
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext, set_app_context

    from matrx_ai.agents.executor import run_agent
    from matrx_ai.db.conversation_gate import _lineage_metadata

    set_app_context(AppContext(emitter=ConsoleEmitter(), user_id=USER_ID, request_id=PARENT, store=False))
    seen: dict[str, Any] = {}

    async def _capture_execute(user_input: Any = None, *, max_iterations: Any = None, **_: Any) -> Any:
        from matrx_connect.context.app_context import get_app_context

        ctx = get_app_context()
        seen.update(request_id=ctx.request_id, lineage=_lineage_metadata(ctx))
        return SimpleNamespace(
            output="ok", assistant_response=None, config=SimpleNamespace(model="m", metadata={}),
            usage=None, usage_history=[], metadata={},
        )

    agent = SimpleNamespace(name="x", config=SimpleNamespace(model="m", metadata={}), source_id=None,
                            source_is_version=False, execute=_capture_execute)
    await run_agent(agent, label="x", source_app="t", source_feature="x", emit_lifecycle=False,  # type: ignore[arg-type]
                    system_run=True)
    assert seen == {"request_id": PARENT, "lineage": {}}
