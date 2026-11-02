"""plan.step — a step that hasn't resolved yet (the Plan Node primitive).

Design of record: docs/workflow/PLAN_NODE_DESIGN.md (aidream repo root).

The definition holds ONE anchor node per plan, carrying ``plan_id``; the plan's
soul (notes, contract, samples, internal graph, lineage, history) lives in the
``workflow.plan`` row family. The parent graph therefore always sees one node
with a stable boundary contract — internal churn (split, merge, decomposition,
emission) never touches the rest of the graph.

Execution resolves through a host-installed resolver (the ``subgraph.call``
pattern — this package never imports the host). The resolver decides between:

- **child run** — the plan has an internal graph (or a promoted workflow):
  run it as a child, map boundary I/O.
- **stand-in** — the plan has a pinned sample output: substitute it instantly
  (n8n pin-data semantics).
- **junction** — a sketch/intent plan with no samples passes its input through
  unchanged (Airflow EmptyOperator): the graph never refuses to run because a
  thought is immature.
- **not built** (production runs only) — a run of a published version that
  REACHES a plan with no internal graph, no promoted workflow and no allowed
  stand-in stops that branch: a typed ``plan_not_built`` failure ("This step is
  planned but not built yet: <title>") plus a review flag. Publishing never
  refuses a plan; branches that never reach one run normally.

Standalone fallback (no resolver installed): serve ``config.stand_in_output``
when present, else pass inputs through — so an in-memory graph with plan nodes
runs anywhere, with zero database.

Sync note: ``config.output_schema_json`` / ``config.stand_in_output`` are
DENORMALIZED copies of the plan row's contract + pinned sample, written into
the anchor node's config by the ONE plan service whenever the row changes
(compile is sync and must not read the DB). The row is truth; the config is
what compile needs.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue, RootModel

from matrx_graph.errors import GraphInterrupt
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from matrx_graph.types.usl import field_extras

PlanRunner = Callable[
    [NodeExecutionContext, "PlanStepConfig", "PlanStepInput"],
    Awaitable[dict[str, Any]],
]

_resolver: PlanRunner | None = None


def set_plan_resolver(resolver: PlanRunner | None) -> None:
    """Register the host resolver that executes a plan (child run / stand-in /
    junction / production refusal). Passing None unregisters (for tests)."""
    global _resolver
    _resolver = resolver


class PlanStepInput(BaseModel):
    # Permissive: whatever upstream routes in flows through (junction mode) or
    # seeds the internal graph (child-run mode).
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "x-contract-dynamic": "a plan impersonates any future step; its real input shape lives on the workflow.plan row"
        },
    )


class PlanStepOutput(RootModel[dict[str, JsonValue]]):
    # The concrete fields remain dynamic because the effective schema comes
    # from config.output_schema_json at compile time. The runtime boundary is
    # nevertheless closed to JSON values instead of leaking untyped Any.
    root: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="The plan's output object, validated against its effective compile-time schema.",
    )


class PlanStepConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    plan_id: str | None = Field(
        default=None,
        description="The workflow.plan row this node anchors. Null only for a "
        "standalone in-memory graph with inline config.",
        json_schema_extra=field_extras(hidden=True),
    )
    output_schema_json: dict[str, JsonValue] | None = Field(
        default=None,
        description="Denormalized copy of the plan's candidate output contract "
        "(JSON Schema). Written by the plan service; read at compile time.",
        json_schema_extra=field_extras(hidden=True),
    )
    stand_in_output: dict[str, JsonValue] | None = Field(
        default=None,
        description="Denormalized copy of the pinned sample output this plan "
        "serves when impersonating the unbuilt step.",
        json_schema_extra=field_extras(hidden=True),
    )
    stand_in_scenario: str = Field(
        default="happy",
        description="Which named sample scenario to serve (happy / empty / error / custom).",
        json_schema_extra=field_extras(hidden=True),
    )
    allow_stand_in_in_production: bool = Field(
        default=False,
        description="Explicit opt-in: let this plan's pretend result run in "
        "production. Off = production runs stop here until the step is real.",
        json_schema_extra=field_extras(hidden=True),
    )

    def effective_output_json_schema(self) -> dict[str, Any]:
        """The plan's candidate output contract IS the node's output shape
        (read at compile time because ``NodeSpec.dynamic_output`` is True).
        An uncontracted plan is an open object — downstream sees untyped JSON
        until the contract phase, which is honest."""
        if isinstance(self.output_schema_json, dict) and self.output_schema_json:
            return self.output_schema_json
        return {"type": "object", "properties": {}}


class PlanStepExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="plan.step",
        category=NodeCategory.PLAN,
        display_name="Plan",
        description=(
            "A step you haven't figured out yet. Name it, connect it, and let "
            "it stand in for the real thing — then turn it into whatever it "
            "should become."
        ),
        input_schema=PlanStepInput,
        output_schema=PlanStepOutput,
        config_schema=PlanStepConfig,
        # No named kind: the effective schema is the plan's own candidate
        # contract (the io.user_input posture).
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
        can_interrupt=True,
        dynamic_output=True,
        icon="lightbulb",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: PlanStepInput,
        config: PlanStepConfig,
    ) -> NodeResult[PlanStepOutput]:
        if _resolver is not None and config.plan_id:
            try:
                result = await _resolver(ctx, config, inputs)
            except GraphInterrupt:
                # An interrupt deep inside the plan's internal graph surfaces
                # on the PARENT scheduler, same as subgraph.call.
                raise
            except Exception as e:  # noqa: BLE001
                return failure("plan_execution_failed", str(e), details={"error": str(e)})
            mode = result.get("mode")
            if mode == "not_built":
                # A production run REACHED a plan with nothing real behind it
                # (no internal graph, no promoted workflow, no allowed stand-in).
                # Planned steps never block publishing (Arman 2026-10-26) — so
                # the honest stop happens here, only on the branch that reaches
                # it: a typed failure (routes down an error edge when one is
                # wired, else parks the run), plus a review flag so the owner
                # sees which idea a real run needed. Never a silent pass-through.
                title = str(result.get("plan_name") or "").strip() or "this step"
                message = f"This step is planned but not built yet: {title}"
                details = {"plan_id": config.plan_id, "plan_name": title}
                await ctx.flag_for_review(
                    "plan.not_built",
                    message,
                    category="unexpected_path",
                    severity="error",
                    source="engine",
                    payload=details,
                )
                return failure("plan_not_built", message, details=details)
            if result.get("production_refuses"):
                # A draft run passed this step on a stand-in or a pass-through that a published
                # run refuses: it is not proof the path works, and the run says so.
                title = str(result.get("plan_name") or "").strip() or "this step"
                await ctx.flag_for_review(
                    "plan.stand_in_served",
                    f"Passed on a stand-in in this draft run — a published run stops here: {title}",
                    category="unexpected_path",
                    severity="warning",
                    source="engine",
                    payload={"plan_id": config.plan_id, "plan_name": title, "mode": mode},
                )
            return success(PlanStepOutput.model_validate(result.get("output", {})))

        # Standalone fallback — no resolver (in-memory graphs, tests).
        if config.stand_in_output is not None:
            return success(PlanStepOutput.model_validate(config.stand_in_output))
        return success(PlanStepOutput.model_validate(inputs.model_dump(mode="json")))
