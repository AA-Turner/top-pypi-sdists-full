"""control.map — iterate a list and Send each item to a target node.

Pure dispatcher. Each ``Send`` becomes a distinct invocation of the target
in the next super-step; the children run in parallel up to the target's
fan-out bound (``data.concurrency`` — a number, or ``{"$input": name}`` so the
caller sets it per run — / the ``workflow.fan_out`` knobs, never above the ceiling;
the rest queue; a paid target runs one probe item first). For fan-in, pair
with ``control.gather`` or write to a channel with the ``topic_map`` reducer
inside the target node.
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.errors import ExecutionError
from matrx_graph.nodes._template import run_facts_of, substitute_template
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras


class MapInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    items: list[JsonValue] = Field(
        default_factory=list,
        description="The list to fan out — one invocation of the target node per item.",
    )


class MapOutput(KindModel, kind="map_result"):
    dispatched: int = Field(
        description="How many child invocations were dispatched (one per item)."
    )


class MapConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target_node_id: str = Field(
        min_length=1,
        description="Node id to invoke once per item. Each invocation runs in parallel.",
        json_schema_extra=field_extras(widget="text", help="Target node id on this canvas"),
    )
    payload_key: str = Field(
        default="value",
        description="Key the target receives each item under.",
        json_schema_extra=field_extras(widget="text"),
    )
    include_index: bool = Field(
        default=False,
        description="If true, the target also receives `{index: N}`.",
        json_schema_extra=field_extras(widget="toggle"),
    )
    max_dispatches: int = Field(
        default=1000,
        ge=1,
        le=10_000,
        description=(
            "Hard cap on dispatched invocations (audit P2-7). A data-"
            "driven list larger than this FAILS the node (parks, "
            "recoverable) instead of fanning out unbounded — one upstream "
            "surprise must not spawn a million invocations. How many "
            "items run AT ONCE is the target step's data.concurrency "
            "(a number, or {\"$input\": name} so the caller sets it per run), "
            "else the workflow.fan_out knob (never above its ceiling)."
        ),
        json_schema_extra=field_extras(widget="number"),
    )
    payload_template: dict[str, JsonValue] | None = Field(
        default=None,
        description=(
            "Optional per-item payload shape. When set, each dispatched "
            "payload is this template with every string value '$item' "
            "replaced by the item and '$item.<dot.path>' replaced by that "
            "path into the item (digit segments index lists); '$in' / "
            "'$in.<dot.path>' resolve against this node's OTHER inputs "
            "(everything delivered on its edges besides `items`), so "
            "upstream values can ride along on every dispatch; all other "
            "values pass through literally, recursing into nested "
            "dicts/lists. A path that does not resolve FAILS the node "
            "(parks, recoverable). When None, the classic "
            "`{payload_key: item}` shape is used."
        ),
        json_schema_extra=field_extras(widget="json"),
    )


class MapExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="control.map",
        category=NodeCategory.CONTROL,
        display_name="For Each",
        description="Run a step once for each item in a list, in parallel.",
        input_schema=MapInput,
        output_schema=MapOutput,
        config_schema=MapConfig,
        output_kind="map_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        determinism=ActionTier.IDEMPOTENT,
        icon="split-square-horizontal",
    )

    async def execute(
        self, ctx: NodeExecutionContext, inputs: MapInput, config: MapConfig
    ) -> NodeResult[MapOutput]:
        if len(inputs.items) > config.max_dispatches:
            raise ExecutionError(
                f"control.map: {len(inputs.items)} items exceeds "
                f"max_dispatches={config.max_dispatches}. Raise the cap "
                "deliberately (config.max_dispatches) or chunk the list "
                "upstream — unbounded fan-out is a resource-exhaustion "
                "hazard."
            )
        extra = {k: v for k, v in inputs.model_dump(mode="json").items() if k != "items"}
        dispatched = 0
        for index, item in enumerate(inputs.items):
            if config.payload_template is not None:
                payload = substitute_template(
                    config.payload_template, item, index=index, extra=extra, run=run_facts_of(ctx)
                )
            else:
                payload = {config.payload_key: item}
            if config.include_index:
                payload["index"] = index
            ctx.send(config.target_node_id, payload)
            dispatched += 1
        return success(MapOutput(dispatched=dispatched))
