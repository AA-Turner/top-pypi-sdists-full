"""A worker re-running a request keeps that request's witnessed class (2026-10-16).

Crash recovery re-ran a person's interrupted chat turn under ``system_app_context``. With no
route on the context, the turn read as background ``system`` work: the protected-account guard
refused it as an automated run, and every other person's recovered turn escaped the usage gate.
"""

from matrx_connect import (
    RESUMED_RUN_WITNESS_KEY,
    AppContext,
    gate_origin_class,
    reconcile_origin,
    resumed_run_witness,
)
from matrx_connect.emitters.console_emitter import ConsoleEmitter

REQUEST_ID = "9068fa79-5391-4148-82b7-d851840e0625"
PERSON = "4cf62e4e-2679-484f-b652-034e697418df"
ORIGINAL_WITNESS = {"route": "/ai/agents/8d02d271", "auth_type": "token", "declared_class": "human"}


def _worker_ctx(record: dict | None, **overrides) -> AppContext:
    metadata = {RESUMED_RUN_WITNESS_KEY: record} if record is not None else {}
    fields = {"request_id": REQUEST_ID, "user_id": PERSON, "origin_class": "system", "metadata": metadata}
    fields.update(overrides)
    return AppContext(emitter=ConsoleEmitter("test", accumulate=False), **fields)


def _record(**changes) -> dict:
    record = resumed_run_witness(
        request_id=REQUEST_ID, user_id=PERSON, origin_class="human", origin_witness=ORIGINAL_WITNESS
    )
    record.update(changes)
    return record


def test_without_the_record_a_resumed_turn_reads_as_system() -> None:
    assert gate_origin_class(_worker_ctx(None)) == "system"


def test_resumed_request_keeps_its_original_witnessed_class() -> None:
    ctx = _worker_ctx(_record())
    final, witness = reconcile_origin(ctx)
    assert final == "human"
    assert gate_origin_class(ctx) == "human"
    # The row it writes satisfies chat.user_request's human-requires-route CHECK.
    assert witness["route"] == ORIGINAL_WITNESS["route"]
    assert witness["auth_type"] == "token"
    assert witness["resumed_run"] == {"request_id": REQUEST_ID, "origin_class": "human"}
    assert "contradictions" not in witness


def test_a_different_request_never_inherits_the_record() -> None:
    ctx = _worker_ctx(_record(), request_id="11111111-1111-1111-1111-111111111111")
    assert gate_origin_class(ctx) == "system"


def test_a_live_request_is_always_its_own_witness() -> None:
    ctx = _worker_ctx(_record(origin_class="human"), route="/ai/chat", auth_type="token", origin_class="")
    assert gate_origin_class(ctx) == "api"


def test_a_record_that_cannot_support_its_class_is_not_trusted() -> None:
    for bad in (
        _record(route=None),
        _record(auth_type="anonymous"),
        _record(origin_class="admin"),
    ):
        final, witness = reconcile_origin(_worker_ctx(bad))
        assert final == "system"
        assert witness["contradictions"]


def test_machine_classes_resume_as_themselves() -> None:
    record = resumed_run_witness(
        request_id=REQUEST_ID, user_id=PERSON, origin_class="scheduled", origin_witness={}
    )
    assert gate_origin_class(_worker_ctx(record)) == "scheduled"


def test_forks_of_a_resumed_turn_read_from_their_own_facts() -> None:
    from matrx_connect.context.app_context import PARENT_ORIGIN_CLASS_KEY

    ctx = _worker_ctx(_record(), conversation_id="1507ab15-d721-49d6-a92e-db73880f2a8e")
    child = ctx.fork_for_child_agent("22222222-2222-2222-2222-222222222222")
    # Every child owns its own turn: a fresh request id, the resumed turn as its parent
    # and as the tree root it spends, is admitted and is stopped under.
    assert child.request_id != REQUEST_ID
    assert child.parent_request_id == REQUEST_ID
    assert child.tree_request_id == REQUEST_ID
    assert gate_origin_class(child) == "child_agent"
    # The person started this tree: the sub-agent never records an automated parent.
    assert PARENT_ORIGIN_CLASS_KEY not in child.metadata
    step = ctx.fork_for_workflow_step("33333333-3333-3333-3333-333333333333")
    assert gate_origin_class(step) == "workflow"


def test_forks_of_a_plain_worker_run_still_record_it() -> None:
    from matrx_connect.context.app_context import PARENT_ORIGIN_CLASS_KEY

    ctx = _worker_ctx(None, conversation_id="1507ab15-d721-49d6-a92e-db73880f2a8e")
    child = ctx.fork_for_child_agent("22222222-2222-2222-2222-222222222222")
    assert child.metadata[PARENT_ORIGIN_CLASS_KEY] == "system"


def test_a_record_for_another_person_is_not_trusted() -> None:
    final, witness = reconcile_origin(_worker_ctx(_record(user_id="11111111-1111-4111-8111-111111111111")))
    assert final == "system"
    assert any("different person" in c for c in witness["contradictions"])


def test_a_record_that_names_nobody_is_refused_never_assumed() -> None:
    """A record built before it carried ``user_id`` cannot prove whose request it was."""
    old = _record()
    old.pop("user_id")
    final, witness = reconcile_origin(_worker_ctx(old))
    assert final == "system"
    assert witness["contradictions"]
