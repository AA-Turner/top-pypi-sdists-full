"""W0 — the five engine proofs the agent_build workflow stands on.

Agent Studio rebuild, lane 2A (common-docs/systems/masterwork/
agent-creation-studio/projects/rebuild/BUILD-PLAN.md §A Lane 2A, D1, D3).
Each test is the in-process half of one proof; the live half is recorded in
that folder's W0.md. Every graph here uses BUILT-IN nodes only (the
agent_build stand-ins are ``data.transform`` steps) so the exact same
definition can be saved and run on the live server — see
``w0_skeleton_definition()``.

1. One workflow, one conditional back-edge from ``decide`` to the first gate:
   the gate re-fires, the second pass's if/else joins fire, and the branch not
   taken resolves (prunes) instead of blocking the join.
2. A ``data.transform`` dict literal writes an answer into the state (and the
   ``|`` merge is NOT available — the literal must name every state key).
3. A ``control.human_input`` ``decision`` gate parks, resumes with a person's
   answer, and resumes with the default-answer fallback; a gate on a side
   branch DOES hold the main branch (D3's evidence).
4. A process kill mid-run, then a fresh scheduler resumes: finished steps are
   not re-run; a side-effect step that finished in the killed super-step has a
   recorded outcome, so it is not repeated either (the node body still keys
   its write on ``stable_idempotency_key`` for the worker-retry case).
5. Every port's kind is enforced: a declared input kind refuses a bad payload
   before execute, a declared output kind fails a bad output, with the
   committed ``KIND_ENFORCEMENT`` constant (no monkeypatch).
"""

from __future__ import annotations

import asyncio
import time
from datetime import UTC, datetime
from typing import Any, ClassVar

import pytest
from pydantic import BaseModel, ConfigDict

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph import kinds as kinds_mod
from matrx_graph.decisions import DECISION_KEY, default_answer_decision, human_decision
from matrx_graph.kinds import KIND_ENFORCEMENT, KindEntry, invalidate_kind_catalog_cache
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success

from tests._fixtures import FakeEmitter, make_app_context

USER = "11111111-1111-4111-8111-111111111111"
DEADLINE = datetime(2026, 10, 21, 12, 0, tzinfo=UTC)

#: The state's keys, in step order. ``rerun_idx`` is the index of the first
#: step to re-run; a gate runs its step when the step has no answer yet or
#: ``rerun_idx`` is at or before it (D1).
STATE_KEYS = ("contract", "instructions", "rerun_idx", "send_backs", "verdict")


def _state_literal(**overrides: str) -> str:
    """A dict literal naming EVERY state key — the only lawful write (proof 2)."""
    parts = []
    for key in STATE_KEYS:
        parts.append(f"'{key}': {overrides.get(key, f'inputs[{key!r}]')}")
    return "{" + ", ".join(parts) + "}"


def _n(node_id: str, node_type: str, x: int = 0, **data: Any) -> dict[str, Any]:
    return {"id": node_id, "type": node_type, "position": {"x": x, "y": 0}, "data": data}


def _transform(node_id: str, expression: str, x: int = 0) -> dict[str, Any]:
    return _n(node_id, "data.transform", x, config={"expression": expression})


def _gate(node_id: str, step_key: str, step_idx: int, x: int) -> dict[str, Any]:
    return _n(
        node_id,
        "control.branch",
        x,
        config={"predicate": f"inputs['{step_key}'] is None or inputs['rerun_idx'] <= {step_idx}"},
    )


def w0_skeleton_definition() -> dict[str, Any]:
    """The D1 shape with two writer steps, built-ins only.

    intake → gate_contract ─true→ write_contract(produce stand-in) → save_contract ─┐
                           └false────────────────────────────────────────────────────┴→ gate_instr
    gate_instr ─true→ write_instr → save_instr ─┐
               └false───────────────────────────┴→ decide
    decide ══[verdict == 'send_back']══► gate_contract   (conditional BACK-EDGE)
    decide ──[verdict != 'send_back']──► done

    decide sends back once (rerun_idx=1: re-run only the instructions step),
    then passes. Expected: contract written once, instructions twice.
    """
    return {
        "version": "1",
        "entry_nodes": ["intake"],
        "nodes": [
            _transform(
                "intake",
                "{'contract': None, 'instructions': None, 'rerun_idx': 0, "
                "'send_backs': 0, 'verdict': 'none'}",
            ),
            _gate("gate_contract", "contract", 0, 200),
            # The ai.agent.produce stand-in: answers depend on the round.
            _transform(
                "write_contract", "{'answer': 'contract-r' + str(inputs['send_backs'])}", 400
            ),
            _transform("save_contract", _state_literal(contract="inputs['answer']"), 600),
            _gate("gate_instr", "instructions", 1, 800),
            _transform(
                "write_instr", "{'answer': 'instructions-r' + str(inputs['send_backs'])}", 1000
            ),
            _transform("save_instr", _state_literal(instructions="inputs['answer']"), 1200),
            # agent.proof.decide stand-in: one send-back to step 1, then pass.
            _transform(
                "decide",
                _state_literal(
                    rerun_idx="1 if inputs['send_backs'] < 1 else inputs['rerun_idx']",
                    send_backs="inputs['send_backs'] + 1 if inputs['send_backs'] < 1 "
                    "else inputs['send_backs']",
                    verdict="'send_back' if inputs['send_backs'] < 1 else 'pass'",
                ),
                1400,
            ),
            _transform("done", _state_literal(), 1600),
        ],
        "edges": [
            {"id": "e_intake_gc", "source": "intake", "target": "gate_contract"},
            {
                "id": "e_gc_wc",
                "source": "gate_contract",
                "target": "write_contract",
                "sourceHandle": "true",
            },
            {
                "id": "e_gc_sc",
                "source": "gate_contract",
                "target": "save_contract",
                "sourceHandle": "true",
            },
            {"id": "e_wc_sc", "source": "write_contract", "target": "save_contract"},
            {"id": "e_sc_gi", "source": "save_contract", "target": "gate_instr"},
            {
                "id": "e_gc_gi",
                "source": "gate_contract",
                "target": "gate_instr",
                "sourceHandle": "false",
            },
            {
                "id": "e_gi_wi",
                "source": "gate_instr",
                "target": "write_instr",
                "sourceHandle": "true",
            },
            {
                "id": "e_gi_si",
                "source": "gate_instr",
                "target": "save_instr",
                "sourceHandle": "true",
            },
            {"id": "e_wi_si", "source": "write_instr", "target": "save_instr"},
            {"id": "e_si_decide", "source": "save_instr", "target": "decide"},
            {
                "id": "e_gi_decide",
                "source": "gate_instr",
                "target": "decide",
                "sourceHandle": "false",
            },
            {
                "id": "e_decide_back",
                "source": "decide",
                "target": "gate_contract",
                "data": {"kind": "conditional", "condition": "inputs['verdict'] == 'send_back'"},
            },
            {
                "id": "e_decide_done",
                "source": "decide",
                "target": "done",
                "data": {"kind": "conditional", "condition": "inputs['verdict'] != 'send_back'"},
            },
        ],
        "channels": [],
        "metadata": {"w0": "agent_build back-edge skeleton"},
    }


def _registry(*extra: Any) -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    for executor in extra:
        reg.register(executor, overwrite=True)
    return reg


def _completed_nodes(emitter: FakeEmitter) -> list[str]:
    return [
        p["node_id"]
        for (m, p) in emitter.events
        if m == "data" and isinstance(p, dict) and p.get("event") == "node_completed"
    ]


# ─────────────────────────────── proof 1 + 2: back-edge, joins, prunes, state


def test_proof1_the_decide_edge_is_the_only_back_edge() -> None:
    graph = compile_graph(
        Definition.model_validate(w0_skeleton_definition()), registry=_registry()
    )
    back = {eid for eid, e in graph.edges.items() if e.is_back_edge}
    assert back == {"e_decide_back"}


async def test_proof1_send_back_re_fires_the_first_gate_and_skips_answered_steps() -> None:
    registry = _registry()
    graph = compile_graph(Definition.model_validate(w0_skeleton_definition()), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)

    result = await scheduler.run(run_id="w0-backedge", max_steps=60)

    assert result.status is RunStatus.COMPLETED, result.error
    done = _completed_nodes(emitter)
    # The first gate fired twice: once from intake, once over the back-edge.
    assert done.count("gate_contract") == 2
    # Round 2 skipped the contract step (answered, rerun_idx=1 is after it) …
    assert done.count("write_contract") == 1
    assert done.count("save_contract") == 1
    # … and re-ran the instructions step: the second-pass join at gate_instr
    # fired from the FALSE edge while the pruned TRUE path resolved.
    assert done.count("gate_instr") == 2
    assert done.count("write_instr") == 2
    assert done.count("decide") == 2
    # ``done`` was pruned on round 1 (send_back) and fires on round 2.
    assert done.count("done") == 1
    final = result.last_outputs["done"]
    assert final["contract"] == "contract-r0", "the earlier answer is kept"
    assert final["instructions"] == "instructions-r1", "the re-run step wrote round 2's answer"
    assert final["verdict"] == "pass"
    assert final["send_backs"] == 1


async def test_proof2_a_dict_literal_writes_the_answer_into_the_state() -> None:
    registry = _registry()
    graph = compile_graph(Definition.model_validate(w0_skeleton_definition()), registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry)
    result = await scheduler.run(run_id="w0-transform", max_steps=60)
    assert result.status is RunStatus.COMPLETED, result.error
    saved = result.last_outputs["save_contract"]
    # Spread FLAT: the state keys are the output keys; no 'result', no extras.
    assert set(saved) == set(STATE_KEYS)
    assert saved["contract"] == "contract-r0"


def test_proof2_the_merge_operator_is_refused_so_the_literal_is_required() -> None:
    from matrx_graph.errors import ExecutionError
    from matrx_graph.nodes._sandbox import validate_expression

    with pytest.raises(ExecutionError, match="BitOr"):
        validate_expression("inputs | {'contract': inputs['answer']}")


# ─────────────────────────────── proof 3: the workflow-offer decision gate


def _offer_graph(*, side_branch: bool) -> dict[str, Any]:
    offer = _n(
        "offer",
        "control.human_input",
        200,
        config={
            "preset": "decision",
            "title": "This could be a workflow",
            "prompt": "Keep going as one agent, or build it as a workflow?",
            "default_answer": "keep_going",
            "escalation": {"after_seconds": 300, "fallback": "default_answer"},
            "decision": {
                "items": [
                    {
                        "key": "fit",
                        "label": "How to build it",
                        "value": "keep_going",
                        "choices": ["pick_one"],
                        "options": [
                            {"value": "keep_going", "label": "Keep going as one agent"},
                            {"value": "workflow", "label": "Build it as a workflow"},
                        ],
                        "required": True,
                    }
                ],
                "submit_label": "Go",
            },
        },
    )
    nodes = [
        _transform("contract", "{'fit': 'workflow'}"),
        offer,
        _transform("goal", "{'goal': 'g'}", 200),
        _transform("tools", "{'tools': 't'}", 400),
        _transform("instructions", "{'instructions': 'i'}", 600),
        _transform("after_offer", "{'chosen': inputs['answer']}", 400),
    ]
    edges = [
        {"id": "e_c_offer", "source": "contract", "target": "offer"},
        {"id": "e_offer_after", "source": "offer", "target": "after_offer"},
        {"id": "e_goal_tools", "source": "goal", "target": "tools"},
        {"id": "e_tools_instr", "source": "tools", "target": "instructions"},
    ]
    if side_branch:
        edges.append({"id": "e_c_goal", "source": "contract", "target": "goal"})
    else:
        edges.append({"id": "e_after_goal", "source": "after_offer", "target": "goal"})
    return {"version": "1", "entry_nodes": ["contract"], "nodes": nodes, "edges": edges}


async def _park_offer(run_id: str, *, side_branch: bool):
    registry = _registry()
    graph = compile_graph(Definition.model_validate(_offer_graph(side_branch=side_branch)), registry=registry)
    checkpointer = MemoryCheckpointer()
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, checkpointer, make_app_context(emitter), registry=registry)
    result = await scheduler.run(run_id=run_id, max_steps=40)
    return graph, registry, checkpointer, emitter, result


async def test_proof3_the_decision_gate_parks_with_its_deadline_and_default() -> None:
    _, _, _, _, result = await _park_offer("w0-offer-park", side_branch=False)
    assert result.status is RunStatus.INTERRUPTED
    payload = result.interrupt["payload"] if "payload" in result.interrupt else result.interrupt
    flat = str(payload)
    assert "keep_going" in flat and "escalation" in flat


async def test_proof3_a_person_answer_resumes_the_same_run() -> None:
    graph, registry, checkpointer, _, result = await _park_offer("w0-offer-human", side_branch=False)
    assert result.status is RunStatus.INTERRUPTED
    cp = await checkpointer.latest_checkpoint("w0-offer-human")
    resumed = await Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry).resume(
        run_id="w0-offer-human",
        checkpoint_id=cp.checkpoint_id,
        resume_value={"answer": {"answers": {"fit": {"verdict": "pick_one", "value": "workflow"}}}},
        decision=human_decision(user_id=USER, deadline_at=DEADLINE),
    )
    assert resumed.status is RunStatus.COMPLETED, resumed.error
    assert resumed.last_outputs["offer"][DECISION_KEY]["authority"] == "human"
    assert "instructions" in resumed.last_outputs


async def test_proof3_the_default_answer_fallback_resumes_the_decision_gate() -> None:
    """What the escalation sweeper does at the deadline: ``_decide_by_default``
    resumes with ``{'answer': <default_answer>}`` stamped DEFAULT. On a
    ``decision`` preset the answer must satisfy the derived item schema."""
    graph, registry, checkpointer, _, result = await _park_offer("w0-offer-default", side_branch=False)
    assert result.status is RunStatus.INTERRUPTED
    cp = await checkpointer.latest_checkpoint("w0-offer-default")
    resumed = await Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry).resume(
        run_id="w0-offer-default",
        checkpoint_id=cp.checkpoint_id,
        # exactly the sweeper's shape (sweeper._decide_by_default)
        resume_value={"answer": "keep_going"},
        decision=default_answer_decision(deadline_at=DEADLINE),
    )
    assert resumed.status is RunStatus.COMPLETED, resumed.error
    assert resumed.last_outputs["offer"][DECISION_KEY]["authority"] == "default"
    # the engine settled the item from the durable spec: the default option was picked
    assert resumed.last_outputs["offer"]["decision"][0]["value"] == "keep_going"


async def test_proof3_a_two_choice_form_gate_times_out_to_its_default() -> None:
    """The shape that works on today's engine: preset 'form' whose schema is a
    two-value enum. The sweeper's exact resume shape satisfies it."""
    definition = _offer_graph(side_branch=False)
    offer = next(n for n in definition["nodes"] if n["id"] == "offer")
    cfg = offer["data"]["config"]
    cfg.pop("decision")
    cfg["preset"] = "form"
    cfg["schema_hint"] = {
        "type": "object",
        "properties": {"answer": {"type": "string", "enum": ["keep_going", "workflow"]}},
        "required": ["answer"],
    }
    registry = _registry()
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    checkpointer = MemoryCheckpointer()
    parked = await Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry).run(
        run_id="w0-offer-form", max_steps=40
    )
    assert parked.status is RunStatus.INTERRUPTED
    cp = await checkpointer.latest_checkpoint("w0-offer-form")
    resumed = await Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry).resume(
        run_id="w0-offer-form",
        checkpoint_id=cp.checkpoint_id,
        resume_value={"answer": "keep_going"},
        decision=default_answer_decision(deadline_at=DEADLINE),
    )
    assert resumed.status is RunStatus.COMPLETED, resumed.error
    assert resumed.last_outputs["offer"][DECISION_KEY]["authority"] == "default"
    assert resumed.last_outputs["after_offer"]["chosen"] == "keep_going"
    assert "instructions" in resumed.last_outputs


class _Ordered:
    """Wraps one built-in executor so the test, not the event loop, decides
    which of two sibling invocations FINISHES first.

    ``lead`` records the task it runs in and, once its execute has ended
    (returned or raised — a gate raises its interrupt), opens ``ended``.
    ``follow`` holds its execute until ``ended`` is open AND the lead's whole
    invocation task is done, so the scheduler is handed the lead's result
    first — through asyncio's FIFO done-callbacks, never a sleep.
    """

    def __init__(self, inner: Any, node_id: str, ended: asyncio.Event, lead_task: list[asyncio.Task[Any]], *, lead: bool) -> None:
        self._inner = inner
        self._node_id = node_id
        self._ended = ended
        self._lead_task = lead_task
        self._lead = lead
        self.spec = inner.spec

    def __getattr__(self, name: str) -> Any:
        return getattr(self._inner, name)

    async def execute(self, ctx: NodeExecutionContext, inputs: Any, config: Any) -> Any:
        if ctx.node_id != self._node_id:
            return await self._inner.execute(ctx, inputs, config)
        if self._lead:
            task = asyncio.current_task()
            assert task is not None and "_run_invocation" in task.get_coro().__qualname__, (
                "the lead's execute must run inside its own invocation task"
            )
            self._lead_task.append(task)
            try:
                return await self._inner.execute(ctx, inputs, config)
            finally:
                self._ended.set()
        await asyncio.wait_for(self._ended.wait(), timeout=30)
        await asyncio.wait({self._lead_task[0]}, timeout=30)
        assert self._lead_task[0].done(), "the lead invocation never finished"
        return await self._inner.execute(ctx, inputs, config)


async def _park_side_branch(run_id: str, *, gate_finishes_first: bool):
    """Park the side-branch graph with the finishing order of the two
    siblings (``offer``, the gate, and ``goal``, the main branch) FIXED."""
    base = _registry()
    ended: asyncio.Event = asyncio.Event()
    lead_task: list[asyncio.Task[Any]] = []
    lead, follow = ("offer", "goal") if gate_finishes_first else ("goal", "offer")
    by_node = {"offer": "control.human_input", "goal": "data.transform"}
    registry = _registry(
        _Ordered(base.get(by_node[lead]), lead, ended, lead_task, lead=True),
        _Ordered(base.get(by_node[follow]), follow, ended, lead_task, lead=False),
    )
    graph = compile_graph(Definition.model_validate(_offer_graph(side_branch=True)), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    result = await scheduler.run(run_id=run_id, max_steps=40)
    return emitter, result


async def test_proof3_a_side_branch_gate_holds_the_main_branch() -> None:
    """D3's evidence question: with the gate on a SIDE branch, does the main
    branch keep going? Once the gate has interrupted, the engine parks the
    WHOLE run at that super-step: siblings already in that step commit,
    nothing after them runs.

    The order is fixed on purpose. RUN-AHEAD (scheduler ``_await_step``)
    starts a node the moment its inputs are finished, and stops only when a
    member of the step interrupts — so a sibling that finishes BEFORE the gate
    has raised lets its successor start early (CI run 39849765611: the gate's
    kind admission waited on an unreachable catalog, ``goal`` finished first
    and ``tools`` ran ahead). That is run-ahead's design, not this proof; this
    proof is the hold that follows the interrupt, so the gate finishes first."""
    emitter, result = await _park_side_branch("w0-offer-side", gate_finishes_first=True)
    assert result.status is RunStatus.INTERRUPTED
    done = _completed_nodes(emitter)
    assert "goal" in done, "the sibling in the gate's own super-step commits"
    assert "tools" not in done and "instructions" not in done, (
        "the main branch is held while the side-branch gate waits"
    )


# ─────────────────────────────── proof 4: kill mid-run, resume, no repeats


class _Kill(BaseException):
    """A process death: not an Exception, so no node-failure handling sees it."""


class _AnyIO(BaseModel):
    model_config = ConfigDict(extra="allow")


class _NoConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


def _spec(node_type: str, tier: ActionTier) -> NodeSpec:
    return NodeSpec(
        type=node_type,
        category=NodeCategory.DATA,
        display_name=node_type,
        description=node_type,
        input_schema=_AnyIO,
        output_schema=_AnyIO,
        config_schema=_NoConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        determinism=tier,
    )


class _Apply:
    """agent.definition.apply stand-in: a keyed write (the store dedupes)."""

    spec: ClassVar[NodeSpec] = _spec("test.w0_apply", ActionTier.SIDE_EFFECT)

    def __init__(self) -> None:
        self.executions = 0
        self.rows: dict[str, str] = {}
        self.keys: list[str] = []

    async def execute(self, ctx: NodeExecutionContext, inputs: _AnyIO, _c: _NoConfig) -> NodeResult[_AnyIO]:
        self.executions += 1
        key = ctx.stable_idempotency_key
        self.keys.append(key)
        self.rows.setdefault(key, f"agent-{len(self.rows) + 1}")
        return success(_AnyIO(agent_id=self.rows[key]))


class _Killer:
    """Hangs on its first call until the test kills the process (cancels the
    run task mid-await) — a death at a real await point, with no node-failure
    handling in the way."""

    spec: ClassVar[NodeSpec] = _spec("test.w0_killer", ActionTier.PURE)

    def __init__(self) -> None:
        self.calls = 0
        self.started = asyncio.Event()

    async def execute(self, _ctx: NodeExecutionContext, inputs: _AnyIO, _c: _NoConfig) -> NodeResult[_AnyIO]:
        self.calls += 1
        if self.calls == 1:
            self.started.set()
            await asyncio.Event().wait()  # never returns: the process dies here
        return success(_AnyIO(**inputs.model_dump(mode="json"), checked=True))


def _is_kill(exc: BaseException) -> bool:
    if isinstance(exc, _Kill):
        return True
    if isinstance(exc, BaseExceptionGroup):
        return any(_is_kill(e) for e in exc.exceptions)
    return False


def _kill_graph(*, same_step: bool) -> dict[str, Any]:
    nodes = [
        _transform("intake", "{'spec': 'ok'}"),
        _n("apply", "test.w0_apply", 200),
        _n("killer", "test.w0_killer", 400),
        _transform("finish", "{'ok': True}", 600),
    ]
    if same_step:
        edges = [
            {"id": "e1", "source": "intake", "target": "apply"},
            {"id": "e2", "source": "intake", "target": "killer"},
            {"id": "e3", "source": "apply", "target": "finish"},
            {"id": "e4", "source": "killer", "target": "finish"},
        ]
    else:
        edges = [
            {"id": "e1", "source": "intake", "target": "apply"},
            {"id": "e2", "source": "apply", "target": "killer"},
            {"id": "e3", "source": "killer", "target": "finish"},
        ]
    return {"version": "1", "entry_nodes": ["intake"], "nodes": nodes, "edges": edges}


async def _kill_and_resume(run_id: str, *, same_step: bool):
    apply, killer = _Apply(), _Killer()
    registry = _registry(apply, killer)
    graph = compile_graph(Definition.model_validate(_kill_graph(same_step=same_step)), registry=registry)
    checkpointer = MemoryCheckpointer()
    task = asyncio.create_task(
        Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry).run(
            run_id=run_id, max_steps=20
        )
    )
    await asyncio.wait_for(killer.started.wait(), timeout=10)
    await asyncio.sleep(0.05)  # let a same-step sibling finish its body
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    latest = await checkpointer.latest_checkpoint(run_id)
    assert latest is not None, "a durable checkpoint exists before the death"
    # A fresh process: a new scheduler, nothing in memory carried over.
    result = await Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry).resume(
        run_id=run_id, checkpoint_id=latest.checkpoint_id
    )
    return apply, killer, result


async def test_proof4_a_finished_side_effect_is_not_repeated_after_a_kill() -> None:
    apply, killer, result = await _kill_and_resume("w0-kill-later", same_step=False)
    assert result.status is RunStatus.COMPLETED, result.error
    assert apply.executions == 1, "the checkpointed apply step replayed from its stored output"
    assert killer.calls == 2
    assert len(apply.rows) == 1


async def test_proof4_a_side_effect_finished_in_the_killed_step_is_not_repeated() -> None:
    """The kill lands while a sibling of the side-effect step is still running,
    so the super-step never checkpointed. The engine still does NOT re-run the
    side effect: its outcome was recorded when it finished, and the resumed
    step replays it (the per-node outcome store, not the step checkpoint)."""
    apply, killer, result = await _kill_and_resume("w0-kill-same", same_step=True)
    assert result.status is RunStatus.COMPLETED, result.error
    assert apply.executions == 1, apply.keys
    assert killer.calls == 2
    assert len(apply.rows) == 1


# ─────────────────────────────── proof 5: every port's kind is enforced


@pytest.fixture
def _kind_cache():
    invalidate_kind_catalog_cache()
    yield
    invalidate_kind_catalog_cache()


def _seed(slug: str, schema: dict[str, Any]) -> None:
    kinds_mod._cache[slug] = (time.monotonic(), KindEntry(slug=slug, version=1, json_schema=schema))


class _Kinded:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.w0_kinded",
        category=NodeCategory.DATA,
        display_name="kinded",
        description="kinded",
        input_schema=_AnyIO,
        output_schema=_AnyIO,
        config_schema=_NoConfig,
        input_kind="w0_state_in",
        output_kind="w0_state_out",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        determinism=ActionTier.PURE,
    )

    def __init__(self) -> None:
        self.calls = 0

    async def execute(self, _ctx: NodeExecutionContext, inputs: _AnyIO, _c: _NoConfig) -> NodeResult[_AnyIO]:
        self.calls += 1
        return success(_AnyIO(verdict=inputs.model_dump().get("emit")))


def _kinded_run(emit: Any) -> tuple[Definition, _Kinded, NodeRegistry]:
    kinded = _Kinded()
    definition = Definition.model_validate(
        {
            "version": "1",
            "entry_nodes": ["src"],
            "nodes": [
                _transform("src", "{'emit': " + repr(emit) + "}"),
                _n("k", "test.w0_kinded", 200),
            ],
            "edges": [{"id": "e", "source": "src", "target": "k"}],
        }
    )
    return definition, kinded, _registry(kinded)


_IN_SCHEMA = {"type": "object", "properties": {"emit": {"type": "string"}}, "required": ["emit"]}
_OUT_SCHEMA = {
    "type": "object",
    "properties": {"verdict": {"type": "string", "enum": ["pass", "fail"]}},
    "required": ["verdict"],
}


async def _run_kinded(emit: Any, run_id: str):
    definition, kinded, registry = _kinded_run(emit)
    graph = compile_graph(definition, registry=registry)
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry).run(
        run_id=run_id, max_steps=10
    )
    return result, kinded


def test_proof5_enforcement_is_on_as_committed() -> None:
    assert KIND_ENFORCEMENT == {"workflow_io": True}


async def test_proof5_a_conforming_payload_passes_both_ports(_kind_cache) -> None:
    _seed("w0_state_in", _IN_SCHEMA)
    _seed("w0_state_out", _OUT_SCHEMA)
    result, kinded = await _run_kinded("pass", "w0-kind-ok")
    assert result.status is RunStatus.COMPLETED, result.error
    assert kinded.calls == 1


async def test_proof5_a_bad_input_is_refused_before_execute(_kind_cache) -> None:
    _seed("w0_state_in", _IN_SCHEMA)
    _seed("w0_state_out", _OUT_SCHEMA)
    result, kinded = await _run_kinded(7, "w0-kind-bad-in")
    assert result.status is not RunStatus.COMPLETED
    assert kinded.calls == 0, "the input kind refused the payload before the body ran"


async def test_proof5_a_bad_output_fails_the_step(_kind_cache) -> None:
    _seed("w0_state_in", _IN_SCHEMA)
    _seed("w0_state_out", _OUT_SCHEMA)
    result, kinded = await _run_kinded("maybe", "w0-kind-bad-out")
    assert kinded.calls == 1
    assert result.status is not RunStatus.COMPLETED
