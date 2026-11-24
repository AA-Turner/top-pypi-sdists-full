"""control.map — iterate a list and Send each item to a target node.

Pure dispatcher. Each ``Send`` becomes a distinct invocation of the target
in the next super-step; the children run in parallel up to the target's
fan-out bound (``data.concurrency`` — a number, or ``{"$input": name}`` so the
caller sets it per run — / the ``workflow.fan_out`` knobs, never above the ceiling;
the rest queue; a paid target runs one probe item first). For fan-in, pair
with ``control.gather`` or write to a channel with the ``topic_map`` reducer
inside the target node.

``until`` / ``wave_size`` (G3) pace the dispatch: every Send carries the pace and the scheduler
holds the items in index order, wave by wave, and stops sending once ``until`` is true over what
came back (``executor/paced_dispatch.py``). ``max_dispatches`` (G7) is a number or an expression,
default the list's length, never above the knob ``workflow.for_each.max_items``.
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.errors import ExecutionError
from matrx_graph.nodes._sandbox import safe_eval, validate_expression
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
    max_dispatches: int | str | None = Field(
        default=None,
        description=(
            "Hard cap on dispatched invocations (audit P2-7; G7). A number, or an expression over "
            "this step's inputs (`len(inputs['items'])`); empty = the list's length. Never above "
            "the platform knob workflow.for_each.max_items. A data-driven list larger than the "
            "cap FAILS the node (parks, recoverable) instead of fanning out unbounded — one "
            "upstream surprise must not spawn a million invocations. How many items run AT ONCE "
            "is the target step's data.concurrency (a number, or {\"$input\": name} so the caller "
            "sets it per run), else the workflow.fan_out knob (never above its ceiling)."
        ),
        json_schema_extra=field_extras(widget="text"),
    )
    until: str | None = Field(
        default=None,
        description=(
            "Stop sending once this is true (G3). An expression over what came back so far: "
            "inputs['results'] (each finished item's result, in item order), inputs['settled'] "
            "({item_index, status, value} per settled item), inputs['sent'], inputs['total'] "
            "and this step's other inputs. Items already working finish; the "
            "rest are skipped and named."
        ),
        json_schema_extra=field_extras(widget="text"),
    )
    wave_size: str | None = Field(
        default=None,
        description=(
            "Send the items in waves of this many, in item order (G3): the next wave starts only "
            "when every item of the one before has finished, and its size is read again over the "
            "same inputs as `until` (e.g. inputs['target'] - <how many are good>). 0 or less "
            "sends no more."
        ),
        json_schema_extra=field_extras(widget="text"),
    )
    wave_gap: str | None = Field(
        default=None,
        description=(
            "Seconds to wait before each wave after the first (a number, or an expression over the "
            "same inputs as `until`): a provider that wants its calls spaced out (search pages 1.5 s "
            "apart) is paced here, visibly. Empty or 0: the next wave starts at once."
        ),
        json_schema_extra=field_extras(widget="text"),
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


async def check_dispatch_cap(
    where: str, items: list[JsonValue], max_dispatches: int | str | None, extra: dict[str, JsonValue]
) -> int:
    """G7: the step's cap (a number, an expression, or the list's length) bounded by the platform
    knob ``workflow.for_each.max_items``; a list over it fails loudly. Returns the cap applied."""
    from matrx_graph import knobs as graph_knobs

    platform_cap = await graph_knobs.for_each_max_items()
    if max_dispatches is None:
        own = len(items)
    elif isinstance(max_dispatches, str):
        try:
            raw = safe_eval(max_dispatches, {**extra, "items": items})
            own = int(raw)
        except ExecutionError:
            raise
        except Exception as exc:  # noqa: BLE001 — a bad cap fails in words, never runs unbounded
            raise ExecutionError(
                f"{where}: max_dispatches {max_dispatches!r} did not give a whole number "
                f"({type(exc).__name__}: {exc})."
            ) from exc
    else:
        own = int(max_dispatches)
    if own < 1:
        own = 1 if not items else own
    if len(items) > platform_cap:
        raise ExecutionError(
            f"{where}: {len(items)} items is more than the platform allows one For each to send "
            f"(workflow.for_each.max_items={platform_cap}). Raise the knob deliberately or split "
            "the list upstream — unbounded fan-out is a resource-exhaustion hazard."
        )
    if len(items) > own:
        raise ExecutionError(
            f"{where}: {len(items)} items exceeds max_dispatches={own}. Raise the cap "
            "deliberately (config.max_dispatches) or chunk the list upstream — unbounded "
            "fan-out is a resource-exhaustion hazard."
        )
    return min(own, platform_cap)


def pace_of(
    until: str | None,
    wave_size: str | None,
    extra: dict[str, JsonValue],
    total: int,
    wave_gap: str | None = None,
) -> dict[str, JsonValue] | None:
    """The pace every Send of a paced dispatch carries (G3), or None. Each expression is checked
    against the sandbox here, so a doomed one fails the dispatcher before any item is sent."""
    until = until.strip() if isinstance(until, str) and until.strip() else None
    wave_size = wave_size.strip() if isinstance(wave_size, str) and wave_size.strip() else None
    wave_gap = str(wave_gap).strip() if wave_gap is not None and str(wave_gap).strip() else None
    if wave_gap is not None and wave_size is None:
        wave_size = "1"  # a gap between waves needs waves: one item at a time unless the author says
    if until is None and wave_size is None:
        return None
    for expr in (until, wave_size, wave_gap):
        if expr is not None:
            validate_expression(expr)
    return {"until": until, "wave_size": wave_size, "wave_gap": wave_gap, "scope": extra, "total": total}


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
        extra = {k: v for k, v in inputs.model_dump(mode="json").items() if k != "items"}
        await check_dispatch_cap("control.map", inputs.items, config.max_dispatches, extra)
        pace = pace_of(config.until, config.wave_size, extra, len(inputs.items), config.wave_gap)
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
            ctx.send(config.target_node_id, payload, pace=pace)
            dispatched += 1
        return success(MapOutput(dispatched=dispatched))
