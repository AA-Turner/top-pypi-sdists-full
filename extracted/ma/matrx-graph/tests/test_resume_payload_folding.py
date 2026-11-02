"""Client-authored resume keys land in the node's declared ``extras`` map.

Arman's ruling, 2026-08-21: "Extra keys belong in a place where you hold the
extra keys — inside an object, not at the top level. At the top level nothing
can read them, because nothing knows what to look for."

``control.human_input`` is resumed with whatever the UI collected. Those keys
used to be recorded at the ROOT of the node's output, which is why the node
could never declare an honest output kind. They now fold one level down,
keeping their names.

Opt-in: a node whose output model has no ``extras`` field is untouched.
"""

from __future__ import annotations

from typing import Any, ClassVar

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
)
from matrx_graph.executor.client_payload import (
    declares_extras,
    fold_undeclared_into_extras,
)
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict, Field, JsonValue

from tests._fixtures import FakeEmitter, make_app_context


# --------------------------------------------------------------------------
# the helper in isolation
# --------------------------------------------------------------------------


class _WithExtras(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = ""
    extras: dict[str, JsonValue] = Field(default_factory=dict)


class _WithoutExtras(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = ""


def test_declared_keys_stay_at_the_root_and_the_rest_fold():
    folded = fold_undeclared_into_extras(
        {"text": "blue", "ticket_id": "T-9", "confidence": 0.8}, _WithExtras
    )
    assert folded == {"text": "blue", "extras": {"ticket_id": "T-9", "confidence": 0.8}}


def test_a_node_without_an_extras_field_is_untouched():
    """Opt-in — this must change nothing for every other node."""
    assert declares_extras(_WithoutExtras) is False
    payload = {"text": "blue", "stray": 1}
    assert fold_undeclared_into_extras(payload, _WithoutExtras) == payload


def test_reserved_engine_keys_are_neither_folded_nor_dropped():
    folded = fold_undeclared_into_extras(
        {"text": "blue", "matrx_decision": {"authority": "human"}, "stray": 1},
        _WithExtras,
        reserved=frozenset({"matrx_decision"}),
    )
    assert folded["matrx_decision"] == {"authority": "human"}
    assert folded["extras"] == {"stray": 1}


def test_a_client_supplied_extras_map_is_merged_not_discarded():
    folded = fold_undeclared_into_extras(
        {"text": "blue", "extras": {"from_client": 1}, "stray": 2}, _WithExtras
    )
    assert folded["extras"] == {"from_client": 1, "stray": 2}


def test_a_root_key_wins_over_the_same_name_inside_client_extras():
    """A root key is what the UI actually collected; losing it is the bug."""
    folded = fold_undeclared_into_extras(
        {"text": "blue", "extras": {"stray": "stale"}, "stray": "real"}, _WithExtras
    )
    assert folded["extras"]["stray"] == "real"


def test_folding_always_leaves_an_extras_map_even_when_empty():
    assert fold_undeclared_into_extras({"text": "blue"}, _WithExtras) == {
        "text": "blue",
        "extras": {},
    }


# --------------------------------------------------------------------------
# through a real interrupt/resume
# --------------------------------------------------------------------------


class _AskInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class _AskConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Ask:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.ask_with_extras",
        display_name="Ask",
        description="Interrupts, then is resumed with a client payload.",
        category=NodeCategory.AGENT,
        input_schema=_AskInput,
        output_schema=_WithExtras,
        config_schema=_AskConfig,
        handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),),
        determinism=ActionTier.NON_DETERMINISTIC,
        can_interrupt=True,
    )

    async def execute(
        self, ctx: NodeExecutionContext, inputs: _AskInput, config: _AskConfig
    ) -> NodeResult[_WithExtras]:
        ctx.interrupt({"prompt": "anything?"})
        return success(_WithExtras())


def _graph_data() -> dict[str, Any]:
    return {
        "nodes": [
            {
                "id": "ask",
                "type": "test.ask_with_extras",
                "position": {"x": 0, "y": 0},
                "data": {},
            }
        ],
        "edges": [],
    }


async def test_resume_folds_the_client_payload_into_extras() -> None:
    registry = NodeRegistry()
    registry.register(_Ask())
    graph = compile_graph(Definition.model_validate(_graph_data()), registry=registry)
    checkpointer = MemoryCheckpointer()
    scheduler = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)

    result = await scheduler.run(run_id="run-fold-1")
    assert result.status is RunStatus.INTERRUPTED

    checkpoints = await checkpointer.list_checkpoints("run-fold-1")
    interrupt_cp = next(cp for cp in checkpoints if cp.interrupt_payload)

    resumed = await scheduler.resume(
        run_id="run-fold-1",
        checkpoint_id=interrupt_cp.checkpoint_id,
        # The UI collected more than the node declares.
        resume_value={"text": "blue", "ticket_id": "T-9", "urgency": "high"},
    )
    assert resumed.status is RunStatus.COMPLETED, resumed.error

    output = resumed.last_outputs["ask"]
    # Declared field at the root; everything else one level down, names intact.
    assert output["text"] == "blue"
    assert output["extras"] == {"ticket_id": "T-9", "urgency": "high"}
    assert "ticket_id" not in output, "undeclared keys must not sit at the root"
