"""control.work_seed — add discovered items to the run's durable work set.

The discovery half of the work-set pair (matrx_graph.workset; the processing
half is ``control.work_queue``). Call it anywhere, any number of times, at
any point in the run — an entry seeder, or a worker node's downstream that
found MORE work while processing an earlier item (later waves). Items dedupe
by canonical key within ``(run, set_name)``, so re-discovering the same unit
is a free no-op and the total never needs to be known at run start.
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.errors import ExecutionError
from matrx_graph.nodes._template import substitute_template
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras
from matrx_graph.workset import WorkItemSeed, canonical_key_for, get_work_set_store


class WorkSeedInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    items: list[JsonValue] = Field(
        default_factory=list,
        description="Newly discovered units of work to add to the set. "
        "Duplicates of already-known items are skipped automatically.",
    )


class WorkSeedOutput(KindModel, kind="work_seed_result"):
    added: int = Field(description="How many items were new to the set.")
    duplicates: int = Field(description="How many were already known (skipped — this is normal).")
    total_discovered: int = Field(
        description="Total items ever added to the set, across all discoveries."
    )


class WorkSeedConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    set_name: str = Field(
        default="default",
        min_length=1,
        description="Which work set to add to. One workflow may run several "
        "independent sets; the queue processing these items must use the "
        "same name.",
        json_schema_extra=field_extras(widget="text"),
    )
    key_template: str | None = Field(
        default=None,
        description=(
            "How to identify an item so the same one is never added twice — "
            "'$item' for the whole value or '$item.<dot.path>' for a field "
            "(e.g. '$item.url'). Leave blank to identify items by their full "
            "content automatically."
        ),
        json_schema_extra=field_extras(widget="text", placeholder="$item.url"),
    )
    max_items: int = Field(
        default=1000,
        ge=1,
        le=10_000,
        description=(
            "Hard cap on items added per call — one upstream surprise must "
            "not flood the set. The run-wide budget (max_total_invocations) "
            "bounds processing separately."
        ),
        json_schema_extra=field_extras(widget="number"),
    )


class WorkSeedExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="control.work_seed",
        category=NodeCategory.CONTROL,
        display_name="Discover Work",
        description=(
            "Add newly found items to this run's work list — at the start, "
            "or mid-run when processing uncovers more. Duplicates are "
            "skipped, so it's safe to call again and again."
        ),
        input_schema=WorkSeedInput,
        output_schema=WorkSeedOutput,
        config_schema=WorkSeedConfig,
        output_kind="work_seed_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        determinism=ActionTier.IDEMPOTENT,
        icon="list-plus",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: WorkSeedInput,
        config: WorkSeedConfig,
    ) -> NodeResult[WorkSeedOutput]:
        if len(inputs.items) > config.max_items:
            raise ExecutionError(
                f"control.work_seed: {len(inputs.items)} items exceeds "
                f"max_items={config.max_items}. Raise the cap deliberately "
                "or chunk the discovery upstream."
            )
        seeds: list[WorkItemSeed] = []
        for item in inputs.items:
            if config.key_template:
                resolved = substitute_template({"key": config.key_template}, item)
                key = str(resolved.get("key", ""))
                if not key:
                    raise ExecutionError(
                        f"control.work_seed: key_template "
                        f"{config.key_template!r} resolved empty for an item "
                        "— every discovered item needs a non-empty identity."
                    )
            else:
                key = canonical_key_for(item)
            payload = item if isinstance(item, dict) else {"value": item}
            seeds.append(WorkItemSeed(canonical_key=key, payload=payload))

        store = get_work_set_store()
        added = await store.append(ctx.run_id, config.set_name, seeds, discovered_by=ctx.node_id)
        counts = await store.counts(ctx.run_id, config.set_name)
        return success(
            WorkSeedOutput(
                added=added,
                duplicates=len(seeds) - added,
                total_discovered=counts.discovered,
            )
        )
