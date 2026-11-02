"""subgraph.call — Node Result System contract.

The payload is strictly ``{run_id, last_outputs, channel_values}`` (the old
``success``/``error`` fields are gone). A missing resolver or a failed child
run is this node's own structured Failure; a child interrupt still re-raises
``GraphInterrupt``.
"""

from __future__ import annotations

import pytest

from matrx_graph.errors import GraphInterrupt, forwards_answer
from matrx_graph.nodes.subgraph.call import (
    SubgraphCallConfig,
    SubgraphCallExecutor,
    SubgraphCallInput,
    set_subgraph_resolver,
)
from matrx_graph.types.result import Failure, Success


@pytest.fixture(autouse=True)
def _clean_resolver():
    set_subgraph_resolver(None)
    yield
    set_subgraph_resolver(None)


def _node() -> SubgraphCallExecutor:
    return SubgraphCallExecutor()


def _config() -> SubgraphCallConfig:
    return SubgraphCallConfig(definition_id="def-1")


async def test_no_resolver_registered_is_failure():
    result = await _node().execute(None, SubgraphCallInput(), _config())
    assert isinstance(result, Failure)
    assert result.error.code == "no_subgraph_resolver"


async def test_child_run_success_payload_shape():
    async def _resolver(_ctx, _config, _inputs):
        return {
            "run_id": "child-1",
            "last_outputs": {"n": {"x": 1}},
            "channel_values": {"ch": [1]},
        }

    set_subgraph_resolver(_resolver)
    result = await _node().execute(None, SubgraphCallInput(), _config())
    assert isinstance(result, Success)
    payload = result.result
    assert payload.run_id == "child-1"
    assert payload.last_outputs == {"n": {"x": 1}}
    assert payload.channel_values == {"ch": [1]}
    # The old envelope-ish payload fields are gone.
    dumped = payload.model_dump()
    assert "success" not in dumped and "error" not in dumped


async def test_child_run_error_becomes_failure_with_stable_code():
    async def _resolver(_ctx, _config, _inputs):
        raise RuntimeError("child run child-9 ended errored: boom")

    set_subgraph_resolver(_resolver)
    result = await _node().execute(None, SubgraphCallInput(), _config())
    assert isinstance(result, Failure)
    assert result.error.code == "child_run_failed"
    assert "boom" in result.error.message
    assert result.error.details == {"error": "child run child-9 ended errored: boom"}


def test_a_failed_childs_cause_is_its_code_never_its_name():
    """The scheduler passes a returned Failure's code as its type: a child named "Permissions audit" whose run
    failed is child_run_failed, never not_authorized read off the sentence (2026-10-27)."""
    from matrx_graph.errors import NodeFailureError
    from matrx_graph.failure import Cause, failure_from_exception
    from matrx_graph.types.result import NodeError

    sentence = "the workflow 'Permissions audit' ran 3 steps and ended failed (child run c-1)"
    err = NodeFailureError("call_audit", NodeError(code="child_run_failed", message=sentence))
    assert failure_from_exception(err, step_id="call_audit").cause == Cause.CHILD_RUN_FAILED


@pytest.mark.parametrize("gate", ["usage_limit_reached", "not_authorized", "spend_approval_required", "refused"])
def test_a_gate_code_passes_through_unchanged(gate):
    """A step whose code IS a gate cause keeps it, whatever the sentence says; a spend hold keeps its link."""
    from matrx_graph.errors import NodeFailureError
    from matrx_graph.failure import failure_from_exception
    from matrx_graph.types.result import NodeError

    url = "https://www.aimatrx.com/approvals/spend/x"
    node_error = NodeError(code=gate, message="the workflow 'Missing input checker' ended failed",
                           details={"approval_url": url})
    got = failure_from_exception(NodeFailureError("call", node_error), step_id="call")
    assert got.cause == gate, got.to_column()
    assert got.approval_url == url


async def test_a_child_stopped_by_a_gate_is_this_steps_cause_with_the_child_run():
    from matrx_graph.nodes.subgraph.call import SubgraphChildFailed

    async def _resolver(_ctx, _config, _inputs):
        raise SubgraphChildFailed(
            "reached its AI usage limit — the workflow 'W' ended failed (child run c-7)",
            child_run_id="c-7",
            failure={"cause": "usage_limit_reached", "message": "reached its AI usage limit"},
        )

    set_subgraph_resolver(_resolver)
    result = await _node().execute(None, SubgraphCallInput(), _config())
    assert isinstance(result, Failure)
    assert result.error.code == "usage_limit_reached"
    assert result.error.details["child_run_id"] == "c-7"


async def test_a_child_that_failed_on_its_own_is_child_run_failed():
    from matrx_graph.nodes.subgraph.call import SubgraphChildFailed

    async def _resolver(_ctx, _config, _inputs):
        raise SubgraphChildFailed("boom (child run c-8)", child_run_id="c-8", failure={"cause": "engine_error"})

    set_subgraph_resolver(_resolver)
    result = await _node().execute(None, SubgraphCallInput(), _config())
    assert result.error.code == "child_run_failed"
    assert result.error.details == {"error": "boom (child run c-8)", "child_run_id": "c-8", "child_cause": "engine_error"}


async def test_child_interrupt_reraises_graph_interrupt():
    async def _resolver(_ctx, _config, _inputs):
        raise GraphInterrupt(node_id="subgraph.call", payload={"prompt": "?"})

    set_subgraph_resolver(_resolver)
    with pytest.raises(GraphInterrupt) as asked:
        await _node().execute(None, SubgraphCallInput(), _config())
    # The child's question rides up whole, marked so the parent's resume hands
    # the answer back to this step instead of recording it as the step's output.
    assert asked.value.payload["prompt"] == "?"
    assert forwards_answer(asked.value.payload)
