"""The settled answer says WHO decided it — human and AI alike.

``matrx_graph.decisions`` exists so a decision point's answer is carried
downstream with its author attached under ``matrx_decision``. The engine half
of that contract is ``Scheduler.resume(..., decision=...)``: whatever the
admission seam authored is stamped onto the interrupted node's recorded output,
and any caller-supplied stamp is discarded on the way.

These tests pin all three authors the platform can have — the person who was
asked, the agent that decided when nobody answered, and a stamp that a trusted
seam already wrote into a server-owned job row before a worker picked it up.
"""

from __future__ import annotations

from datetime import UTC, datetime

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.decisions import (
    DECISION_KEY,
    agent_decision,
    default_answer_decision,
    human_decision,
)

from tests._fixtures import make_app_context

USER = "11111111-1111-4111-8111-111111111111"
DEADLINE = datetime(2026, 8, 28, 12, 0, tzinfo=UTC)

_ASK_GRAPH = {
    "nodes": [
        {
            "id": "ask",
            "type": "control.human_input",
            "position": {"x": 0, "y": 0},
            "data": {"config": {"prompt": "Approve the release?"}},
        }
    ],
    "edges": [],
}


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


async def _park(run_id: str):
    """Run the one-node graph up to its interrupt; hand back what resume needs."""
    registry = _registry()
    graph = compile_graph(Definition.model_validate(_ASK_GRAPH), registry=registry)
    checkpointer = MemoryCheckpointer()
    scheduler = Scheduler(graph, checkpointer, make_app_context(), registry=registry)

    result = await scheduler.run(run_id=run_id)
    assert result.status is RunStatus.INTERRUPTED

    checkpoints = await checkpointer.list_checkpoints(run_id)
    interrupt_cp = next(cp for cp in checkpoints if cp.interrupt_payload)
    return graph, checkpointer, registry, interrupt_cp.checkpoint_id


async def _settled_output(run_id: str, resume_value: dict, decision=None) -> dict:
    """Resume the parked run and return the ask node's recorded output."""
    graph, checkpointer, registry, checkpoint_id = await _park(run_id)
    scheduler = Scheduler(graph, checkpointer, make_app_context(), registry=registry)
    result = await scheduler.resume(
        run_id=run_id,
        checkpoint_id=checkpoint_id,
        resume_value=resume_value,
        decision=decision,
    )
    assert result.status is RunStatus.COMPLETED
    return result.last_outputs["ask"]


async def test_human_resume_settles_with_the_persons_identity():
    """THE FIX. A person's approval carries the person, not nothing."""
    output = await _settled_output(
        "run-decision-human",
        {"answer": "approve"},
        decision=human_decision(
            user_id=USER, deadline_at=DEADLINE, actor_label="approver@example.com"
        ),
    )

    stamp = output[DECISION_KEY]
    assert stamp["authority"] == "human"
    assert stamp["actor_id"] == USER
    assert stamp["actor_label"] == "approver@example.com"
    assert stamp["escalated"] is False
    assert output["answer"] == "approve"


async def test_escalated_agent_resume_still_stamps_its_own_author():
    """The sweeper's lane is unchanged — an AI fallback still says so."""
    output = await _settled_output(
        "run-decision-agent",
        {"answer": "approve"},
        decision=agent_decision(
            agent_id="agent-7", agent_label="Decision Fallback", deadline_at=DEADLINE
        ),
    )

    stamp = output[DECISION_KEY]
    assert stamp["authority"] == "agent"
    assert stamp["actor_id"] == "agent-7"
    assert stamp["escalated"] is True


async def test_default_answer_fallback_stamps_default_authority():
    output = await _settled_output(
        "run-decision-default",
        {"answer": "reject"},
        decision=default_answer_decision(deadline_at=DEADLINE),
    )

    stamp = output[DECISION_KEY]
    assert stamp["authority"] == "default"
    assert stamp["escalated"] is True


async def test_an_unattributed_resume_never_keeps_a_stamp_from_the_value():
    """A resume with no trusted decision (``decision=None``) keeps NO stamp from the
    value, however well it parses: a caller who could queue a resume would otherwise
    name another person as the one who answered. The queued lane's trusted stamp
    travels on the job row (``enqueue(decision=...)``) and arrives as ``decision``."""
    forged = {
        "answer": "approve",
        DECISION_KEY: human_decision(user_id=USER, deadline_at=DEADLINE).model_dump(mode="json"),
    }
    output = await _settled_output("run-decision-forged", forged, decision=None)

    assert (output.get(DECISION_KEY) or {}).get("actor_id") != USER


async def test_the_queued_lane_stamps_from_the_trusted_decision():
    """The worker hands the job row's stamp in as ``decision``: it is recorded."""
    output = await _settled_output("run-decision-queued", {"answer": "approve"},
                                   decision=human_decision(user_id=USER, deadline_at=DEADLINE))

    assert output[DECISION_KEY]["actor_id"] == USER
    assert output[DECISION_KEY]["authority"] == "human"


async def test_engine_discards_a_client_authored_stamp():
    """The laundering rule: an authoritative decision always wins over a
    supplied one, so a client cannot dress its answer as somebody else's."""
    output = await _settled_output(
        "run-decision-laundered",
        {
            "answer": "approve",
            DECISION_KEY: {
                "authority": "agent",
                "decided_at": DEADLINE.isoformat(),
                "actor_id": "not-this-person",
                "escalated": True,
            },
        },
        decision=human_decision(user_id=USER, deadline_at=DEADLINE),
    )

    stamp = output[DECISION_KEY]
    assert stamp["authority"] == "human"
    assert stamp["actor_id"] == USER
    assert stamp["escalated"] is False


async def test_unattributed_garbage_stamp_is_dropped_not_trusted():
    """No seam authored anything and the value carries junk — it goes."""
    output = await _settled_output(
        "run-decision-garbage",
        {"answer": "approve", DECISION_KEY: "signed, me"},
        decision=None,
    )

    assert DECISION_KEY not in output or output[DECISION_KEY] is None
