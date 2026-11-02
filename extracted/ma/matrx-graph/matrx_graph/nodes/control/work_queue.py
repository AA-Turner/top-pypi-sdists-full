"""control.work_queue — process the run's work set in waves until it drains.

The processing half of the work-set pair (matrx_graph.workset; discovery is
``control.work_seed``). Each firing:

1. Reclaims expired leases (crash recovery — dead workers' items return to
   pending, or dead-letter past their attempt budget).
2. Claims up to ``batch_size`` pending items (atomic, lease-fenced) and Sends
   each to ``target_node_id`` — the item's id rides the Send, and the engine
   settles it (succeeded/failed) when the worker invocation's outcome is
   recorded.
3. Checks the drain condition. Items still pending or in flight → the node
   Sends ITSELF a continuation, so it fires again next super-step — which,
   under the Pregel barrier, is exactly "after this wave's workers finish or
   the moment new work appears". Drained → emits on the ``done`` handle with
   the final tally, and downstream continues.

Because workers can ``control.work_seed`` MORE items while processing (their
appends land during execution; their settle lands after, at outcome-record
time), ``pending == 0 and in_progress == 0`` is proof that no further
discovery is coming from processing — the drain check is race-free by
ordering, not by luck.

Wire downstream nodes from the ``done`` handle (fires once, at drain).
Workers publish results the fan-out way: an ``output_channel`` with an
append reducer, read by anything after ``done``. The per-wave ``wave``
handle exists for live visual taps and fires every firing.
"""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.nodes._template import run_facts_of, substitute_template
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.events import WorkSetProgressEvent
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, EdgeKind, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras
from matrx_graph.workset import get_work_set_store


class WorkQueueInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    wave: int = Field(
        default=0,
        description="Internal wave counter carried by the queue's own "
        "continuation — leave unmapped.",
    )


class WorkQueueOutput(KindModel, kind="work_queue_wave_result"):
    done: bool = Field(description="True when the work set fully drained.")
    wave: int = Field(description="The wave number this firing ran.")
    dispatched: int = Field(description="Items sent to the worker this wave.")
    discovered: int = Field(description="Total items ever discovered.")
    succeeded: int = Field(description="Items completed successfully so far.")
    failed: int = Field(
        description="Items that failed permanently so far (including "
        "abandoned items past their retry budget)."
    )


class WorkQueueConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target_node_id: str = Field(
        min_length=1,
        description="Node id to run once per claimed item, in parallel.",
        json_schema_extra=field_extras(widget="text", help="Target node id on this canvas"),
    )
    set_name: str = Field(
        default="default",
        min_length=1,
        description="Which work set to process — must match the Discover Work step feeding it.",
        json_schema_extra=field_extras(widget="text"),
    )
    batch_size: int = Field(
        default=25,
        ge=1,
        le=1000,
        description="How many items to run in parallel per wave.",
        json_schema_extra=field_extras(widget="number"),
    )
    lease_seconds: int = Field(
        default=600,
        ge=30,
        le=86_400,
        description=(
            "How long a claimed item may run before it's considered lost "
            "and retried (crash recovery). Set above the worker's slowest "
            "honest duration."
        ),
        json_schema_extra=field_extras(widget="number"),
    )
    payload_key: str = Field(
        default="value",
        description="Key the worker receives each item's data under (when "
        "no payload template is set).",
        json_schema_extra=field_extras(widget="text"),
    )
    payload_template: dict[str, JsonValue] | None = Field(
        default=None,
        description=(
            "Optional per-item payload shape — '$item' / '$item.<dot.path>' "
            "resolve against the item's data, like For Each."
        ),
        json_schema_extra=field_extras(widget="json"),
    )


class WorkQueueExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="control.work_queue",
        category=NodeCategory.CONTROL,
        display_name="Process Work Queue",
        description=(
            "Run a step for every item on this run's work list — in "
            "parallel batches, wave after wave, until everything (including "
            "work discovered along the way) is finished."
        ),
        input_schema=WorkQueueInput,
        output_schema=WorkQueueOutput,
        config_schema=WorkQueueConfig,
        output_kind="work_queue_wave_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(
                id="done",
                direction=HandleDirection.OUTPUT,
                accepted_kinds=(EdgeKind.CONDITIONAL, EdgeKind.DATA),
                required=False,
            ),
            HandleSpec(
                id="wave",
                direction=HandleDirection.OUTPUT,
                accepted_kinds=(EdgeKind.CONDITIONAL, EdgeKind.DATA),
                required=False,
            ),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
        icon="layers",
        # The continuation Send re-fires this node while an inbound edge may
        # still be unresolved on later firings — 'any' is the loop-shaped
        # join, exactly like control.loop's return edge.
        default_join_policy="any",
        # A wave is a CLAIM against the durable work list, not a pure function
        # of its inputs. Replaying a recorded wave after a crash re-sends the
        # items that wave claimed, but their leases may have lapsed while the
        # run was down - the next wave's reclaim then re-claims the very item
        # the replay is running, and its side effect happens twice. Re-running
        # the queue on resume instead rebuilds the wave from the store: a lapsed
        # claim is reclaimed and re-dispatched ONCE, a live one is left to its
        # lease. Guard: tests/test_workset_chaos.py.
        re_execute_on_resume=True,
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: WorkQueueInput,
        config: WorkQueueConfig,
    ) -> NodeResult[WorkQueueOutput]:
        store = get_work_set_store()
        wave = inputs.wave + 1

        reclaimed = await store.reclaim_expired(ctx.run_id, config.set_name)

        claims = await store.claim(
            ctx.run_id,
            config.set_name,
            limit=config.batch_size,
            holder=ctx.run_id,
            lease_seconds=config.lease_seconds,
            wave=wave,
        )
        for claim in claims:
            if config.payload_template is not None:
                payload: dict[str, Any] = substitute_template(
                    config.payload_template, claim.payload, run=run_facts_of(ctx)
                )
            else:
                payload = {config.payload_key: claim.payload}
            ctx.send(config.target_node_id, payload, work_item_id=claim.id)

        counts = await store.counts(ctx.run_id, config.set_name)
        # Drained = nothing pending AND nothing in flight. Items claimed THIS
        # firing count as in_progress in `counts`, so a wave that just
        # dispatched can never read as done.
        done = counts.drained and not claims

        if done:
            ctx.emit(
                "done",
                {
                    "discovered": counts.discovered,
                    "succeeded": counts.succeeded,
                    "failed": counts.failed + counts.dead_letter,
                },
            )
        else:
            # Continuation: fire again next super-step. Under the Pregel
            # barrier that step also contains this wave's workers, so the
            # next firing runs exactly when they're done (or immediately, to
            # pick up freshly appended waves).
            ctx.send(ctx.node_id, {"wave": wave})
            ctx.emit("wave", {"wave": wave, "dispatched": len(claims)})

        # Live progress for the canvas — best-effort, never load-bearing
        # (mirrors ctx.progress). Recorded to wf_node_events by the host's
        # event recorder so a re-opened run restores the same badges.
        try:
            await ctx.app.emitter.send_data(
                WorkSetProgressEvent(
                    run_id=ctx.run_id,
                    step=ctx.step,
                    node_id=ctx.node_id,
                    set_name=config.set_name,
                    wave=wave,
                    dispatched=len(claims),
                    pending=counts.pending,
                    in_progress=counts.in_progress,
                    succeeded=counts.succeeded,
                    failed=counts.failed,
                    dead_letter=counts.dead_letter,
                    discovered=counts.discovered,
                    done=done,
                )
            )
        except Exception:  # noqa: BLE001 — progress is best-effort
            import logging

            logging.getLogger(__name__).warning(
                "work_set_progress emit failed (run=%s node=%s) — UI tick lost",
                ctx.run_id[:8],
                ctx.node_id,
                exc_info=True,
            )
        if reclaimed:
            import logging

            logging.getLogger(__name__).warning(
                "[wf:%s] work_queue '%s' reclaimed %d expired item lease(s) "
                "(set=%s) — a prior worker crashed or overran its lease",
                ctx.run_id[:8],
                ctx.node_id,
                reclaimed,
                config.set_name,
            )

        return success(
            WorkQueueOutput(
                done=done,
                wave=wave,
                dispatched=len(claims),
                discovered=counts.discovered,
                succeeded=counts.succeeded,
                failed=counts.failed + counts.dead_letter,
            )
        )
