"""A context that becomes a system run never writes into the chat it ran inside.

Every stored run writes its full history. A machine call made inside a person's
turn (title labeler, held code call, RAG judge) that kept the person's
conversation would file its prompt, answer and config into that person's chat
(reproduced live 2026-10-05, conversation de7652ea). The transition into a
system run therefore mints its own conversation + request, linked to the parent.
"""

from matrx_connect import AppContext, ConsoleEmitter

PERSON_CONV = "11111111-1111-4111-8111-111111111111"
PERSON_REQ = "22222222-2222-4222-8222-222222222222"


def _person() -> AppContext:
    return AppContext(
        emitter=ConsoleEmitter("test", accumulate=False),
        user_id="u",
        conversation_id=PERSON_CONV,
        request_id=PERSON_REQ,
    )


def test_becoming_a_system_run_mints_its_own_conversation_and_request() -> None:
    machine = _person().with_overrides(system_run=True, store=True)
    assert machine.conversation_id != PERSON_CONV
    assert machine.parent_conversation_id == PERSON_CONV
    assert machine.request_id != PERSON_REQ
    assert machine.parent_request_id == PERSON_REQ


def test_an_explicit_conversation_is_kept() -> None:
    own = "33333333-3333-4333-8333-333333333333"
    machine = _person().with_overrides(system_run=True, conversation_id=own)
    assert machine.conversation_id == own
    assert machine.request_id == PERSON_REQ


def test_an_existing_system_run_keeps_its_conversation() -> None:
    machine = _person().with_overrides(system_run=True)
    again = machine.with_overrides(system_run=True, store=True)
    assert again.conversation_id == machine.conversation_id


def test_other_overrides_never_move_the_conversation() -> None:
    assert _person().with_overrides(store=True).conversation_id == PERSON_CONV


# ── lineage never names a workflow invocation's conversation ──────────────────
# A workflow step runs under ``fork_for_workflow_step`` with a minted per-
# invocation conversation id (uuid5). A graph-action node (news.map_signals …)
# never writes that row, so a mandate it runs (system_run) or a child it forks
# that names it as parent hits the gate's parent_missing path every time —
# 334 ``conversation_parent_lineage_unavailable`` rows on 2026-10-05, all from
# news-monitor workflow steps. Workflow-born work is correlated by its
# execution tree and parent_request_id, never by a conversation parent.

STEP_CONV = "ef2a354e-e4e3-5354-8ad2-96d03752a095"


def _workflow_step() -> AppContext:
    return _person().fork_for_workflow_step(STEP_CONV)


def test_a_system_run_inside_a_workflow_step_names_no_conversation_parent() -> None:
    machine = _workflow_step().with_overrides(system_run=True, store=True)
    assert machine.conversation_id not in (STEP_CONV, PERSON_CONV)
    assert machine.parent_conversation_id is None
    assert machine.parent_request_id == PERSON_REQ


def test_a_child_agent_forked_inside_a_workflow_step_names_no_conversation_parent() -> None:
    child = _workflow_step().fork_for_child_agent("44444444-4444-4444-8444-444444444444")
    assert child.parent_conversation_id is None


def test_a_child_of_a_persons_chat_keeps_its_parent() -> None:
    child = _person().fork_for_child_agent("44444444-4444-4444-8444-444444444444")
    assert child.parent_conversation_id == PERSON_CONV
