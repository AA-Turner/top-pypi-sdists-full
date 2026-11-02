"""Every child agent run owns its own turn — and still belongs to its tree.

THE CONTRACT (owner ruling 2026-10-23: a child run is recorded exactly like a normal
chat). ``fork_for_child_agent`` mints the child's own ``request_id`` (its own
``chat.user_request``), records the caller's as ``parent_request_id`` and freezes the
tree root as ``root_request_id``; ``tree_request_id`` is the one key the cost cap,
admission memos and stop controls read. Before 2026-10-23 the fork copied the caller's
``request_id``, so every helper's rows, cost and outcome were filed on its caller's turn.
"""

from __future__ import annotations

import asyncio

from matrx_connect.context.app_context import (
    AppContext,
    PARENT_RUN_IDENTITY_KEYS,
    tree_request_id_of,
)
from matrx_connect.request_controls import RequestControlRegistry, register_request_tree

ROOT = "11111111-1111-4111-8111-111111111111"
CONVERSATION = "1507ab15-d721-49d6-a92e-db73880f2a8e"


def _top(**overrides: object) -> AppContext:
    from matrx_connect.emitters import SilentEmitter

    fields: dict[str, object] = {
        "emitter": SilentEmitter(),
        "user_id": "22222222-2222-4222-8222-222222222222",
        "request_id": ROOT,
        "conversation_id": CONVERSATION,
        "origin_class": "human",
    }
    fields.update(overrides)
    return AppContext(**fields)  # type: ignore[arg-type]


def test_a_child_owns_its_own_turn_and_names_its_tree() -> None:
    parent = _top()
    assert parent.tree_request_id == ROOT  # a top-level run is its own root
    child = parent.fork_for_child_agent("33333333-3333-4333-8333-333333333333")
    assert child.request_id and child.request_id != ROOT
    assert child.parent_request_id == ROOT
    assert child.root_request_id == ROOT
    assert child.tree_request_id == ROOT


def test_the_root_is_frozen_at_the_first_fork() -> None:
    child = _top().fork_for_child_agent("33333333-3333-4333-8333-333333333333")
    grandchild = child.fork_for_child_agent("44444444-4444-4444-8444-444444444444")
    assert grandchild.request_id not in (ROOT, child.request_id)
    assert grandchild.parent_request_id == child.request_id
    assert grandchild.tree_request_id == ROOT


def test_a_root_fork_gets_its_own_turn_under_the_boundary() -> None:
    # A mandate / job run under a route boundary with no conversation.
    root_fork = _top(conversation_id=None).fork_for_child_agent("55555555-5555-4555-8555-555555555555")
    assert root_fork.request_id != ROOT
    assert root_fork.tree_request_id == ROOT


def test_the_callers_identity_never_rides_onto_the_childs_turn() -> None:
    parent = _top(
        metadata={
            "launch_binding_id": "b",
            "workflow_node_id": "n",
            "voice_session_id": "v",
            "mandate_key": "parent.job",
            "parent_request_id": "stale",
            "kept": "yes",
        }
    )
    child = parent.fork_for_child_agent("33333333-3333-4333-8333-333333333333")
    assert not (set(child.metadata) & PARENT_RUN_IDENTITY_KEYS)
    assert child.metadata["kept"] == "yes"


def test_a_system_run_transition_inherits_the_tree() -> None:
    child = _top().fork_for_child_agent("33333333-3333-4333-8333-333333333333")
    machine = child.with_overrides(system_run=True)
    assert machine.request_id not in (ROOT, child.request_id)
    assert machine.parent_request_id == child.request_id
    assert machine.tree_request_id == ROOT


def test_tree_request_id_of_reads_any_context_shape() -> None:
    assert tree_request_id_of(None) == ""
    assert tree_request_id_of(_top()) == ROOT
    assert tree_request_id_of(_top().fork_for_child_agent("33333333-3333-4333-8333-333333333333")) == ROOT


def test_stop_on_any_id_of_the_tree_stops_every_run_in_it() -> None:
    registry = RequestControlRegistry()
    RequestControlRegistry._instance = registry
    try:
        child = _top().fork_for_child_agent("33333333-3333-4333-8333-333333333333")
        grandchild = child.fork_for_child_agent("44444444-4444-4444-8444-444444444444")
        register_request_tree(child)
        register_request_tree(grandchild)
        sibling = _top().fork_for_child_agent("66666666-6666-4666-8666-666666666666")
        register_request_tree(sibling)
        # Stop pressed on a helper's own turn id stops the tree.
        asyncio.run(registry.cancel(grandchild.request_id))
        assert registry.is_cancelled(ROOT)
        assert registry.is_cancelled(child.request_id)
        assert registry.is_cancelled(sibling.request_id)
        # An unrelated request is untouched.
        assert not registry.is_cancelled("77777777-7777-4777-8777-777777777777")
    finally:
        RequestControlRegistry._instance = None


def test_stop_on_the_parent_reaches_a_helper_and_retry_now_is_consumed_once() -> None:
    registry = RequestControlRegistry()
    child = _top().fork_for_child_agent("33333333-3333-4333-8333-333333333333")
    registry.link_tree(child.request_id, child.tree_request_id)
    asyncio.run(registry.retry_now(ROOT))
    assert asyncio.run(registry.consume_retry_now(child.request_id)) is True
    assert asyncio.run(registry.consume_retry_now(child.request_id)) is False
    asyncio.run(registry.interrupt(ROOT))
    assert registry.is_interrupted(child.request_id)
