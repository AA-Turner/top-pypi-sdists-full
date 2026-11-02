"""THE THREE PIPES acceptance suite.

The load-bearing test is ``test_same_pipeline_four_ways_identical_results``:
ONE multi-step pipeline, run fully-code / fully-human / fully-AI / mixed,
asserting the downstream result is byte-identical every time. If that
property breaks, the pipe selector is not a pipe selector — it is three
different node types wearing one name.
"""

from __future__ import annotations

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
from matrx_graph.nodes.pipe import (
    AiPipeRequest,
    PipeStepConfig,
    select_pipe,
    set_ai_pipe_runner,
)
from matrx_graph.nodes.pipe.step import PipeStepOutput
from matrx_graph.types.context import NodeExecutionContext

from tests._fixtures import make_app_context

# The two decisions the pipeline makes. Every pipe must produce EXACTLY
# these values, which is how "identical downstream result" is provable.
TIER = {"tier": "gold", "score": 9}
HEADLINE = {"headline": "Gold-tier plan"}

CLASSIFY_SCHEMA = {
    "type": "object",
    "properties": {"tier": {"type": "string"}, "score": {"type": "number"}},
    "required": ["tier", "score"],
}
PLAN_SCHEMA = {
    "type": "object",
    "properties": {"headline": {"type": "string"}},
    "required": ["headline"],
}


def test_pipe_step_registered_output_is_typed_json_without_wrapping() -> None:
    output = PipeStepOutput.model_validate({"tier": "gold", "score": 9})

    assert output.model_dump(mode="json") == {"tier": "gold", "score": 9}


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


def _step(node_id: str, x: int, contract_name: str, schema: dict, expression: str, slot: str):
    """One pipe.step wired for all three pipes at once.

    Authoring every pipe on every step is what makes a run-scope switch
    ("do this whole thing as a human") meaningful — the point of the primitive.
    """
    return {
        "id": node_id,
        "type": "pipe.step",
        "position": {"x": x, "y": 0},
        "data": {
            "config": {
                "contract": {
                    "name": contract_name,
                    "question": "Decide: {inputs}",
                    "output_schema": schema,
                },
                "pipes": {
                    "code": {"node_type": "data.transform", "config": {"expression": expression}},
                    "human": {"enabled": True},
                    "ai": {"mandate_key": slot},
                },
                "policy": {"pipe": "code", "fallback": []},
            }
        },
    }


def _pipeline() -> dict:
    return {
        "nodes": [
            _step(
                "classify", 0, "Classify the brand", CLASSIFY_SCHEMA, repr(TIER), "growth.classify"
            ),
            _step(
                "plan", 220, "Write the plan headline", PLAN_SCHEMA, repr(HEADLINE), "growth.plan"
            ),
            # The WITNESS. An ordinary code step fed by BOTH pipe steps, so its
            # output is a direct readout of what the rest of the graph received
            # from each. It always runs in the final segment, on every pipe.
            {
                "id": "sink",
                "type": "data.transform",
                "position": {"x": 440, "y": 0},
                "data": {
                    "config": {
                        "expression": (
                            "{'tier': inputs['tier'], 'score': inputs['score'], "
                            "'headline': inputs['headline']}"
                        )
                    }
                },
            },
        ],
        "edges": [
            {"id": "e1", "source": "classify", "target": "plan"},
            {"id": "e2", "source": "plan", "target": "sink"},
            {"id": "e3", "source": "classify", "target": "sink"},
        ],
    }


def _graph(registry: NodeRegistry):
    return compile_graph(Definition.model_validate(_pipeline()), registry=registry)


async def _stub_ai(_ctx: NodeExecutionContext, request: AiPipeRequest) -> dict:
    """Stand-in for a purpose-built agent — answers its Mandate's contract."""
    return {"growth.classify": TIER, "growth.plan": HEADLINE}[request.mandate_key]


@pytest.fixture(autouse=True)
def _ai_runner():
    set_ai_pipe_runner(_stub_ai)
    yield
    set_ai_pipe_runner(None)


async def _run(run_id: str, pipes, registry: NodeRegistry) -> dict:
    """Drive the pipeline to completion, answering every human pause."""
    graph = _graph(registry)
    checkpointer = MemoryCheckpointer()
    answers = {"classify": TIER, "plan": HEADLINE}

    scheduler = Scheduler(
        graph,
        checkpointer,
        make_app_context(initial_variables={"__pipe": pipes}),
        registry=registry,
    )
    result = await scheduler.run(run_id=run_id)

    while result.status is RunStatus.INTERRUPTED:
        assert result.interrupt is not None
        node_id = result.interrupt["node_id"]
        # The person is asked the contract's question and answers its schema.
        assert result.interrupt["payload"]["pipe"] == "human"
        assert result.interrupt["payload"]["schema_hint"]["required"]
        # The LATEST interrupt checkpoint — a two-pause run has two of them.
        checkpoint = max(
            (cp for cp in await checkpointer.list_checkpoints(run_id) if cp.interrupt_payload),
            key=lambda cp: cp.step,
        )
        # A fresh scheduler: resume must not depend on in-memory state.
        scheduler = Scheduler(
            graph,
            checkpointer,
            make_app_context(initial_variables={"__pipe": pipes}),
            registry=registry,
        )
        result = await scheduler.resume(
            run_id=run_id,
            checkpoint_id=checkpoint.checkpoint_id,
            resume_value=answers[node_id],
        )

    assert result.status is RunStatus.COMPLETED, result.error
    return result.last_outputs


async def test_same_pipeline_four_ways_identical_results():
    """The whole point: the pipe that ran is invisible downstream."""
    registry = _registry()

    by_code = await _run("run-code", "code", registry)
    by_human = await _run("run-human", "human", registry)
    by_ai = await _run("run-ai", "ai", registry)
    mixed = await _run("run-mixed", {"classify": "human", "plan": "ai"}, registry)

    # The witness reads out what the rest of the graph received from BOTH pipe
    # steps. Identical on all four runs = the pipe that ran is invisible.
    expected = {**TIER, **HEADLINE}
    for outputs in (by_code, by_human, by_ai, mixed):
        assert outputs["sink"] == expected

    # A run that never paused additionally exposes each step's own output, and
    # those match the same contract values.
    assert by_code["classify"] == TIER
    assert by_code["plan"] == HEADLINE


async def test_authored_default_runs_when_no_override():
    registry = _registry()
    outputs = await _run("run-authored", None, registry)
    assert outputs["sink"] == {**TIER, **HEADLINE}


async def test_ai_pipe_without_a_runner_fails_loudly_never_silently_degrades():
    set_ai_pipe_runner(None)
    registry = _registry()
    scheduler = Scheduler(
        _graph(registry),
        MemoryCheckpointer(),
        make_app_context(initial_variables={"__pipe": "ai"}),
        registry=registry,
    )
    result = await scheduler.run(run_id="run-no-ai")
    assert result.status is RunStatus.ERRORED
    assert "no AI runner is registered" in str(result.error)


async def test_a_pipe_result_that_breaks_the_contract_is_rejected():
    """A pipe that answers the wrong shape parks the run — it never flows on."""

    async def wrong_shape(_ctx, _request):
        return {"tier": "gold"}  # missing `score`

    set_ai_pipe_runner(wrong_shape)
    registry = _registry()
    scheduler = Scheduler(
        _graph(registry),
        MemoryCheckpointer(),
        make_app_context(initial_variables={"__pipe": "ai"}),
        registry=registry,
    )
    result = await scheduler.run(run_id="run-bad-shape")
    assert result.status is RunStatus.ERRORED
    assert "does not satisfy this step's contract" in str(result.error)


async def test_human_answer_that_breaks_the_contract_is_rejected_at_resume():
    registry = _registry()
    checkpointer = MemoryCheckpointer()
    scheduler = Scheduler(
        _graph(registry),
        checkpointer,
        make_app_context(initial_variables={"__pipe": "human"}),
        registry=registry,
    )
    result = await scheduler.run(run_id="run-bad-human")
    assert result.status is RunStatus.INTERRUPTED
    checkpoint = next(
        cp for cp in await checkpointer.list_checkpoints("run-bad-human") if cp.interrupt_payload
    )
    with pytest.raises(Exception, match="does not satisfy"):
        await scheduler.resume(
            run_id="run-bad-human",
            checkpoint_id=checkpoint.checkpoint_id,
            resume_value={"tier": "gold"},
        )


# -- pipe selection (pure) ------------------------------------------------


def _config(**policy) -> PipeStepConfig:
    return PipeStepConfig.model_validate(
        {
            "contract": {"name": "Decide", "output_schema": CLASSIFY_SCHEMA},
            "pipes": {
                "code": {"node_type": "data.transform"},
                "human": {"enabled": True},
                "ai": {"mandate_key": "growth.classify"},
            },
            "policy": policy or {"pipe": "code"},
        }
    )


def test_run_override_beats_the_authored_default():
    selection = select_pipe(_config(pipe="code"), node_id="n", run_variables={"__pipe": "human"})
    assert selection.pipe == "human"
    assert selection.reason == "run_override"


def test_a_per_step_override_beats_the_run_wide_default():
    variables = {"__pipe": {"*": "ai", "n": "human"}}
    assert select_pipe(_config(), node_id="n", run_variables=variables).pipe == "human"
    assert select_pipe(_config(), node_id="other", run_variables=variables).pipe == "ai"


def test_an_unbound_pipe_is_never_silently_substituted():
    config = PipeStepConfig.model_validate(
        {
            "contract": {"name": "Decide", "output_schema": CLASSIFY_SCHEMA},
            "pipes": {"human": {"enabled": True}},
            "policy": {"pipe": "ai", "fallback": []},
        }
    )
    selection = select_pipe(config, node_id="n")
    assert selection.pipe is None
    assert selection.reason == "unavailable"
    assert selection.available == ["human"]


def test_declared_fallback_substitutes_and_says_so():
    config = PipeStepConfig.model_validate(
        {
            "contract": {"name": "Decide", "output_schema": CLASSIFY_SCHEMA},
            "pipes": {"human": {"enabled": True}},
            "policy": {"pipe": "ai", "fallback": ["human"]},
        }
    )
    selection = select_pipe(config, node_id="n")
    assert selection.pipe == "human"
    assert selection.substituted is True
    assert selection.requested == "ai"


def test_a_malformed_run_override_is_ignored_never_fatal():
    assert select_pipe(_config(), node_id="n", run_variables={"__pipe": 7}).pipe == "code"
    assert select_pipe(_config(), node_id="n", run_variables={"__pipe": "wat"}).pipe == "code"


def test_the_escalation_contract_is_the_platforms_one_escalation_type():
    """ "Ask the human, fall back to the agent after N" needs no rewrite here —
    the step consumes matrx_graph.decisions unchanged and freezes an ABSOLUTE
    deadline onto the durable interrupt payload."""
    from matrx_graph.decisions import DecisionFallback

    config = _config(pipe="human", escalation={"after_seconds": 900, "fallback": "agent"})
    assert config.policy.escalation is not None
    assert config.policy.escalation.after_seconds == 900
    assert config.policy.escalation.fallback is DecisionFallback.AGENT


def test_the_contract_is_the_compiled_output_shape():
    assert _config().effective_output_json_schema() == CLASSIFY_SCHEMA


async def test_code_pipe_input_map_lets_a_strict_action_carry_a_real_step():
    """A step carries MORE than its code leg needs — the map is what stops a
    strict delegate rejecting the extras.

    ``text.slug`` forbids unknown fields, and a real step (the growth loop's
    "choose this page's URL") also carries the keyword and the sibling routes
    for the human and AI legs. Without the map that step simply has no code
    pipe, which would make THE THREE PIPES false for it.
    """
    registry = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "choose",
                    "type": "pipe.step",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {
                            "contract": {
                                "name": "Choose this page's URL",
                                "output_schema": {
                                    "type": "object",
                                    "properties": {"slug": {"type": "string"}},
                                    "required": ["slug"],
                                },
                            },
                            "pipes": {
                                "code": {
                                    "node_type": "text.slug",
                                    "inputs": {"text": "page_title"},
                                }
                            },
                            "policy": {"pipe": "code"},
                        }
                    },
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(definition, registry=registry)
    scheduler = Scheduler(
        graph=graph,
        checkpointer=MemoryCheckpointer(),
        app_context=make_app_context(),
        registry=registry,
    )
    result = await scheduler.run(
        run_id="pipe-code-input-map",
        node_inputs={
            "choose": {
                "page_title": "Emergency Roof Repair in Tampa",
                # Extras the human and AI legs read — a strict delegate would
                # reject these outright if they reached it.
                "primary_keyword": "emergency roof repair tampa",
                "sibling_routes": ["/services/roof-replacement"],
            }
        },
    )
    assert result.status is RunStatus.COMPLETED
    # The payload SAYS what it is (plan §10d-B2: text.slug's output model IS
    # the ``slug_result`` KindModel, so the discriminator is declared data —
    # not something settlement injects and a consumer has to hope for).
    assert result.last_outputs["choose"] == {
        "__kind": "slug_result",
        "slug": "emergency-roof-repair-in-tampa",
    }
