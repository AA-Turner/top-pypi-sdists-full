"""A parentless child-agent fork is a ROOT run (``auto``), never a ``subagent``.

Found 2026-10-14: 8,292 of 22,035 recent ``subagent`` conversations had no parent: server
mandate / pipeline root runs forked through ``child_agent_context`` with no caller conversation.
"""

from matrx_connect import AppContext
from matrx_connect.emitters.console_emitter import ConsoleEmitter

PARENT = "11111111-1111-4111-8111-111111111111"
CHILD = "22222222-2222-4222-8222-222222222222"


def _ctx(**overrides) -> AppContext:
    return AppContext(emitter=ConsoleEmitter("test", accumulate=False), **overrides)


def test_fork_without_a_caller_conversation_is_auto():
    child = _ctx().fork_for_child_agent(CHILD)
    assert child.parent_conversation_id is None
    assert child.conversation_type == "auto"


def test_fork_from_a_workflow_run_has_no_conversation_parent_so_is_auto():
    wf = _ctx(conversation_id=PARENT, conversation_type="workflow", origin_class="workflow")
    child = wf.fork_for_child_agent(CHILD)
    assert child.parent_conversation_id is None
    assert child.conversation_type == "auto"


def test_fork_with_a_caller_conversation_stays_subagent():
    child = _ctx(conversation_id=PARENT).fork_for_child_agent(CHILD)
    assert child.parent_conversation_id == PARENT
    assert child.conversation_type == "subagent"
