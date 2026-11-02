from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_utils import vcprint

from matrx_graph.content_ir.model import KindModel
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras


class SendInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    items: list[JsonValue] = Field(
        default_factory=list,
        description="The list to fan out — one message sent to the target node per item.",
    )


class SendOutput(KindModel, kind="dispatch_result"):
    dispatched: int = Field(description="How many items were dispatched to the target node.")


class SendConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target_node_id: str = Field(
        min_length=1,
        description="Node id to invoke for each item in the input list.",
        json_schema_extra=field_extras(widget="text", help="The target node's id"),
    )
    payload_key: str = Field(
        default="value",
        description=(
            "Name under which each item is passed to the target node's inputs. "
            "E.g. if payload_key='url', the target receives {'url': <item>}."
        ),
        json_schema_extra=field_extras(widget="text"),
    )
    max_dispatches: int = Field(
        default=1000,
        ge=1,
        le=10_000,
        description=(
            "Hard cap on dispatched invocations (audit P2-7). Beyond it "
            "the node FAILS (parks, recoverable) instead of fanning out "
            "unbounded."
        ),
        json_schema_extra=field_extras(widget="number"),
    )


class SendExecutor:
    """Dynamic fanout: emit one Send per item in the input list.

    Each Send becomes a distinct invocation of `target_node_id` in the next
    super-step, so the targets run in parallel. This is the core primitive
    behind `control.map` and map/reduce patterns.

    Determinism: IDEMPOTENT — the dispatch is a function of inputs alone, so
    replaying after a crash reproduces the same fanout without side effects.
    """

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="control.send",
        category=NodeCategory.CONTROL,
        display_name="Send Items",
        description="Send each item to another step to be worked on separately.",
        input_schema=SendInput,
        output_schema=SendOutput,
        config_schema=SendConfig,
        output_kind="dispatch_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        determinism=ActionTier.IDEMPOTENT,
        icon="send",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: SendInput,
        config: SendConfig,
    ) -> NodeResult[SendOutput]:
        if len(inputs.items) > config.max_dispatches:
            from matrx_graph.errors import ExecutionError

            raise ExecutionError(
                f"control.send: {len(inputs.items)} items exceeds "
                f"max_dispatches={config.max_dispatches}. Raise the cap "
                "deliberately or chunk the list upstream."
            )
        if not inputs.items and "items" not in inputs.model_fields_set:
            # An empty list is a legitimate result. Nothing reaching ``items``
            # is an authoring mistake that looks IDENTICAL to it: the node
            # succeeds, dispatches nothing, and the target simply never runs.
            # The payload cannot tell the two apart — it is 0 either way.
            #
            # And the common case is not "nothing arrived", it is "the list
            # arrived under another name": an upstream ``data.transform``
            # hands over ``{"result": [...]}``, which ``extra="allow"``
            # swallows silently. Name the keys that DID arrive so the author
            # can see their list sitting right there. Deliberately NOT
            # auto-mapped: an empty send is legal, and guessing which key was
            # meant is a decision this node does not get to make.
            arrived = sorted(inputs.model_extra or {})
            carrying = [key for key in arrived if isinstance((inputs.model_extra or {})[key], list)]
            detail = ""
            if carrying:
                detail = (
                    f" A list DID arrive, under {carrying!r} — map it to `items` "
                    "(the sender's output key is not `items`)."
                )
            elif arrived:
                detail = f" The inputs that arrived were {arrived!r}."
            vcprint(
                f"[control.send] nothing reached this node's `items` input, so ZERO "
                f"items were dispatched to '{config.target_node_id}' and it will not "
                f"run.{detail}",
                color="yellow",
            )

        dispatched = 0
        for item in inputs.items:
            ctx.send(config.target_node_id, {config.payload_key: item})
            dispatched += 1
        return success(SendOutput(dispatched=dispatched))
