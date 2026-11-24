"""Every wait on a person has a deadline — the engine half.

2026-11-14: an Agent Studio build parked on "Keep it anyway?" and sat there for
good, because a question's deadline was opt-in and that step declared none. 132
live runs were parked the same way.

The engine's part of the fix is ONE seam: where the scheduler parks a run, a
wait on a person is saved WITH its deadline, whether or not the asking step
declared anything. These tests drive real graphs to a real park and read what
was saved. Each is paired with the case that proves it can fail (no host
standard wait → no stamp; a timer park → no stamp).
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.db import run_store as run_store_module
from matrx_graph.decisions import (
    DEFAULT_DEADLINE_SECONDS,
    DecisionFallback,
    StandardWait,
    adopted_escalation,
    configure_standard_wait,
    escalation_from_interrupt,
    unanswered_reason,
    with_wait_deadline,
)
from matrx_graph.failure import Cause

from tests._fixtures import make_app_context

WEEK = 604_800


@pytest.fixture(autouse=True)
def _no_host_left_behind():
    configure_standard_wait(None)
    yield
    configure_standard_wait(None)


def _host_says(wait: StandardWait | None, seen: list[dict] | None = None) -> None:
    async def provider(**scope):
        if seen is not None:
            seen.append(scope)
        return wait

    configure_standard_wait(provider)


def _graph(node_type: str, config: dict) -> dict:
    return {
        "nodes": [
            {"id": "ask", "type": node_type, "position": {"x": 0, "y": 0}, "data": {"config": config}}
        ],
        "edges": [],
    }


async def _park(definition: dict) -> tuple[dict, dict]:
    """Run to the park. Returns (the payload on the run's result, the payload on the checkpoint)."""
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    checkpointer = MemoryCheckpointer()
    run_id = f"run-{uuid4()}"
    result = await Scheduler(graph, checkpointer, make_app_context(), registry=registry).run(run_id=run_id)
    assert result.status is RunStatus.INTERRUPTED
    saved = next(cp for cp in await checkpointer.list_checkpoints(run_id) if cp.interrupt_payload)
    return result.interrupt["payload"], saved.interrupt_payload


def _seconds_until(block: dict) -> float:
    return (datetime.fromisoformat(block["deadline_at"]) - datetime.now(UTC)).total_seconds()


# ── the stamp ────────────────────────────────────────────────────────────────


async def test_a_question_that_declared_nothing_is_saved_with_the_standard_deadline():
    """THE FIX. The step says nothing about a deadline; the run parks with one anyway — on the
    result the route writes to the run row AND on the checkpoint, the same instant on both."""
    seen: list[dict] = []
    _host_says(StandardWait(after_seconds=WEEK), seen)

    on_result, on_checkpoint = await _park(_graph("control.human_input", {"prompt": "Keep it anyway?"}))

    block = escalation_from_interrupt(on_checkpoint)
    assert block is not None, "a wait on a person was saved with no deadline"
    assert on_result["escalation"] == block
    assert block["fallback"] == "end_run"  # nothing is decided FOR the person
    assert block["source"] == "standard"
    assert block["after_seconds"] == WEEK
    assert WEEK - 60 < _seconds_until(block) <= WEEK
    assert set(seen[0]) == {"organization_id", "user_id"}  # the host resolves it for the asker's org


async def test_with_no_host_standard_wait_nothing_is_stamped():
    """The pair that proves the test above can fail: take the host's standard wait away and
    the same graph parks with no deadline (a bare install has nothing that would act on one)."""
    _on_result, on_checkpoint = await _park(_graph("control.human_input", {"prompt": "Keep it anyway?"}))
    assert escalation_from_interrupt(on_checkpoint) is None


async def test_a_declared_outcome_with_no_wait_of_its_own_takes_the_standard_wait():
    """`escalation: {fallback: default_answer}` — the author chose WHAT happens and left HOW LONG
    to the admin setting. The outcome stays theirs."""
    _host_says(StandardWait(after_seconds=WEEK))
    config = {"prompt": "Ship it?", "default_answer": "yes", "escalation": {"fallback": "default_answer"}}

    _on_result, on_checkpoint = await _park(_graph("control.human_input", config))

    block = escalation_from_interrupt(on_checkpoint)
    assert block is not None
    assert block["fallback"] == "default_answer"
    assert block["after_seconds"] == WEEK
    assert "source" not in block  # the author's policy, not the platform's
    since = datetime.fromisoformat(block["waiting_since"])
    assert datetime.fromisoformat(block["deadline_at"]) == since + timedelta(seconds=WEEK)


async def test_a_declared_wait_is_never_touched():
    _host_says(StandardWait(after_seconds=WEEK))
    config = {"prompt": "Ship it?", "escalation": {"after_seconds": 900, "fallback": "agent"}}

    _on_result, on_checkpoint = await _park(_graph("control.human_input", config))

    block = escalation_from_interrupt(on_checkpoint)
    assert block["after_seconds"] == 900 and block["fallback"] == "agent"
    assert 800 < _seconds_until(block) <= 900


async def test_end_run_is_a_declared_outcome_with_the_authors_own_reason():
    _host_says(StandardWait(after_seconds=WEEK))
    config = {
        "prompt": "Approve the invoice?",
        "escalation": {"after_seconds": 3600, "fallback": "end_run", "end_reason": "The invoice was not approved in time."},
    }

    _on_result, on_checkpoint = await _park(_graph("control.human_input", config))

    block = escalation_from_interrupt(on_checkpoint)
    assert block["fallback"] == DecisionFallback.END_RUN.value
    assert unanswered_reason(on_checkpoint, waited="1 hour") == "The invoice was not approved in time."


async def test_a_host_that_says_always_wait_gets_no_deadline():
    _host_says(None)
    _on_result, on_checkpoint = await _park(_graph("control.human_input", {"prompt": "Keep it anyway?"}))
    assert escalation_from_interrupt(on_checkpoint) is None


async def test_a_timer_park_is_waiting_on_the_clock_and_gets_no_deadline():
    """flow.sleep parks the run interrupted too. It is not waiting on anyone — a person's
    deadline on it would END a run that is merely asleep."""
    _host_says(StandardWait(after_seconds=WEEK))
    _on_result, on_checkpoint = await _park(_graph("flow.sleep", {"duration_seconds": 3600}))
    assert "matrx_sleep" in on_checkpoint
    assert "escalation" not in on_checkpoint


async def test_a_failed_lookup_parks_the_run_as_asked_and_never_fails_it():
    async def broken(**_scope):
        raise RuntimeError("settings store is down")

    configure_standard_wait(broken)
    _on_result, on_checkpoint = await _park(_graph("control.human_input", {"prompt": "Keep it anyway?"}))
    assert on_checkpoint["prompt"] == "Keep it anyway?"
    assert escalation_from_interrupt(on_checkpoint) is None  # the host's sweep adopts it


async def test_a_declared_outcome_with_no_host_uses_the_package_fallback():
    payload = {"prompt": "Ship it?", "escalation": {"fallback": "default_answer", "after_seconds": None,
                                                    "waiting_since": "2026-11-14T00:00:00+00:00"}}
    stamped = await with_wait_deadline(payload)
    block = escalation_from_interrupt(stamped)
    assert block["after_seconds"] == DEFAULT_DEADLINE_SECONDS
    assert block["deadline_at"] == "2026-11-15T00:00:00+00:00"


def test_a_wait_adopted_late_counts_from_now_not_from_when_it_was_asked():
    """A run parked in July and adopted in November gets the whole wait — never a deadline
    that had already passed before anyone was told there was one."""
    asked = datetime(2026, 7, 22, tzinfo=UTC)
    now = datetime(2026, 11, 14, tzinfo=UTC)
    block = adopted_escalation(StandardWait(after_seconds=WEEK), asked_at=asked, now=now)
    assert block["waiting_since"] == asked.isoformat()
    assert block["deadline_at"] == (now + timedelta(seconds=WEEK)).isoformat()
    assert block["fallback"] == "end_run"


def test_the_run_row_envelope_and_the_checkpoint_read_the_same():
    block = adopted_escalation(StandardWait(after_seconds=WEEK))
    payload = {"prompt": "?", "escalation": block}
    assert escalation_from_interrupt(payload) == block
    assert escalation_from_interrupt({"node_id": "ask", "payload": payload}) == block


# ── the reason a person reads ────────────────────────────────────────────────


def test_the_reason_names_the_question_the_wait_and_what_to_do():
    reason = unanswered_reason({"title": "This agent did not pass its proof", "prompt": "Keep it?"}, waited="7 days")
    assert reason == (
        "Nobody answered “This agent did not pass its proof” within 7 days, so this run was ended."
    )


def test_the_reason_falls_back_to_the_prompt_and_says_why_nothing_else_answered():
    reason = unanswered_reason(
        {"prompt": "Which   title\nshould we use?"},
        because="The step has no default answer that could be used in their place.",
    )
    assert "“Which title should we use?”" in reason
    assert "before the deadline" in reason
    assert "no default answer" in reason


# ── ending the run ───────────────────────────────────────────────────────────


class _Runs:
    """workflow.run in memory: just enough for the guarded terminal write and the walk down."""

    def __init__(self, rows: dict[str, dict]):
        self.rows = rows

    async def update_where(self, filters: dict, **updates):
        updates.pop("returning", None)
        row = self.rows.get(str(filters["id"]))
        parked_on = filters.get("last_checkpoint_id")
        if row is None or row["status"] not in filters["status__in"] or (
            parked_on is not None and row.get("last_checkpoint_id") != parked_on
        ):
            return SimpleNamespace(rows_affected=0, updated_rows=[])
        row.update(updates)
        return SimpleNamespace(rows_affected=1, updated_rows=[])

    def filter(self, **filters):
        async def values(*_columns):
            return [
                {"id": run_id}
                for run_id, row in self.rows.items()
                if row.get("parent_run_id") in filters["parent_run_id__in"]
                and row["status"] in filters["status__in"]
                and "subgraph_parent" in (row.get("metadata") or {})
            ]

        return SimpleNamespace(values=values)


@pytest.fixture
def runs(monkeypatch):
    def install(rows: dict[str, dict]) -> _Runs:
        store = _Runs(rows)
        monkeypatch.setattr(run_store_module, "get_model", lambda _name: store)
        return store

    return install


@pytest.mark.parametrize("status", ["interrupted", "awaiting_input"])
async def test_an_unanswered_wait_ends_the_run_with_its_reason(runs, status):
    run_id = str(uuid4())
    store = runs({run_id: {"status": status}})

    ended = await run_store_module.RunStore().end_unanswered(
        run_id, reason="Nobody answered “Keep it anyway?” within 7 days, so this run was ended.",
        node_id="ask_keep", deadline_at="2026-11-21T00:00:00+00:00",
    )

    row = store.rows[run_id]
    assert ended == [run_id]
    assert row["status"] == "failed" and row["completed_at"] is not None
    assert row["error"]["message"].startswith("Nobody answered “Keep it anyway?”")
    assert row["error"]["cause"] == Cause.NOBODY_ANSWERED == "nobody_answered"
    assert row["error"]["node_id"] == "ask_keep"


@pytest.mark.parametrize("status", ["running", "completed", "cancelled", "failed"])
async def test_a_run_that_is_no_longer_waiting_is_never_ended(runs, status):
    """THE HUMAN ALWAYS WINS. They answered first (the run is running, or already done): the
    write is refused and the row is exactly as it was."""
    run_id = str(uuid4())
    store = runs({run_id: {"status": status}})

    ended = await run_store_module.RunStore().end_unanswered(run_id, reason="Nobody answered.")

    assert ended == []
    assert store.rows[run_id] == {"status": status}


async def test_a_run_that_moved_on_to_a_new_question_is_never_ended_for_the_old_one(runs):
    """The person answered question A; the run went on and parked on question B. The deadline
    that ran out was A's. Still `interrupted` — but ending it would name A and rob B of its wait."""
    run_id, question_a, question_b = (str(uuid4()) for _ in range(3))
    store = runs({run_id: {"status": "interrupted", "last_checkpoint_id": question_b}})
    engine = run_store_module.RunStore()

    assert await engine.end_unanswered(run_id, reason="Nobody answered A.", checkpoint_id=question_a) == []
    assert store.rows[run_id]["status"] == "interrupted"

    assert await engine.end_unanswered(run_id, reason="Nobody answered B.", checkpoint_id=question_b) == [run_id]
    assert store.rows[run_id]["status"] == "failed"


async def test_called_workflows_waiting_under_an_ended_run_end_with_it(runs):
    """The question a caller relays is its called workflow's question. Ending the caller and
    leaving the called run parked would strand it for good."""
    top, child, grandchild, fork, done = (str(uuid4()) for _ in range(5))
    store = runs({
        top: {"status": "interrupted"},
        child: {"status": "interrupted", "parent_run_id": top, "metadata": {"subgraph_parent": {}}},
        grandchild: {"status": "interrupted", "parent_run_id": child, "metadata": {"subgraph_parent": {}}},
        # A fork of the run is a run of its own, and a finished child is finished.
        fork: {"status": "interrupted", "parent_run_id": top, "metadata": {}},
        done: {"status": "completed", "parent_run_id": top, "metadata": {"subgraph_parent": {}}},
    })

    ended = await run_store_module.RunStore().end_unanswered(top, reason="Nobody answered.")
    assert ended == [top, child, grandchild]  # each one's page is told (the host writes its event)

    assert [store.rows[r]["status"] for r in (top, child, grandchild)] == ["failed"] * 3
    assert store.rows[child]["error"]["ended_with_run"] == top
    assert store.rows[fork]["status"] == "interrupted"
    assert store.rows[done]["status"] == "completed"
