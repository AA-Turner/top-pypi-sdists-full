"""tool.call — "Run an Action": the ONE workflow step that runs any registered Action by name.

Takes an Action name from config + an input (``payload``) and runs it through the one router,
``run_action(name, input, door="step")``, exactly as the Action's own generated step door does:
lazy names resolve (``mcp.<server>.<tool>``, ``api.<connector>.<endpoint>``, ``workflow.*``,
``agent.*``), the input is validated against the Action's schema, the apply gate and the
idempotency ledger apply, and the run's app is carried as-is (actor, organization and runtime
execution id, so a spending Action's cost nests under the workflow run). The key is the
attempt-independent step key (``step_idempotency_key``), so a retry or a re-run from a checkpoint
replays the first answer. A run being stopped refuses to start (``run_stopping``); an Action that
does not open the ``step`` door is refused (``door_closed``). A step-only node (no work function)
runs as a step here, through its executor. The output is nested under ``output`` (a stable output
schema regardless of which Action runs).

This is the generic complement to dragging a specific registered node
onto the canvas. Use ``tool.call`` when the target action is chosen
dynamically (by config, by runtime state, by end-user input).

Node Result System (Wave 1, semantics change): the payload is strictly
``{action, output}`` — the old ``success``/``error``/``error_details``
fields AND the top-level spreading of the inner action's fields are gone.
Downstream edges wire ``output.<field>``. An inner action's Failure becomes
tool.call's OWN Failure (inner code/message/details preserved — including
``details.usage`` for cost settlement).
"""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.actions.decorator import resolve_action_executor
from matrx_graph.errors import ExecutionError, NodeRegistryError
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, Success, failure, success
from matrx_graph.types.usl import field_extras


class ToolCallInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    payload: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="Arguments passed to the invoked action (merged with top-level "
        "inputs when merge_inputs is on).",
        # The picked Action's own inputs (its required ones included) live here: the step form
        # shows them open, never folded under "More options".
        json_schema_extra=field_extras(priority="primary"),
    )


class ToolCallOutput(BaseModel):
    """Success payload (Node Result System, Wave 1 semantics change).

    Strictly ``{action, output}`` — the inner action's full typed output
    lives under ``output`` and downstream edges wire ``output.<field>``.
    The pre-envelope top-level field SPREADING (``extra="allow"``) and the
    ``success``/``error``/``error_details`` payload fields are gone; an
    inner Failure is tool.call's own node Failure.
    """

    model_config = ConfigDict(extra="forbid")

    action: str = Field(description="The name of the action that was invoked.")
    output: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="The action's full typed output. Wire downstream fields as output.<field>.",
    )


class ToolCallConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action_name: str = Field(
        min_length=1,
        description="The Action to run: pick it from the list of everything this workspace can do, "
        "including your connected apps and your own APIs.",
        json_schema_extra=field_extras(widget="action_picker"),
    )
    merge_inputs: bool = Field(
        default=True,
        description=(
            "If true, the values wired into this step are passed to the Action together with its "
            "input, so a value can be given inline without nesting it."
        ),
        json_schema_extra=field_extras(widget="toggle"),
    )

    def effective_output_json_schema(self) -> dict[str, Any]:
        """The TOP-LEVEL output shape, which is fully known before the run.

        ``dynamic_output`` on this node means "the inner action's payload has
        no static kind" — it was never meant to mean "nobody knows what the
        top level looks like". But every reader treated it that way: with no
        effective schema, ``dry_run`` could rule nothing out, so an edge
        mapping a key ``tool.call`` cannot possibly deliver sailed through the
        joint check and died at run time with EdgeRoutingError — the same
        class as ``data.transform``'s ``result`` (run 6511ffd1, 2026-09-12).

        ``ToolCallOutput`` is ``extra="forbid"``: the payload is exactly
        ``{action, output}`` and never anything else, so declaring that CLOSED
        is the truth, not a tightening. What stays open is the inside of
        ``output`` — untyped here, because that genuinely is the dispatched
        action's business. Downstream wires ``output.<field>``.
        """
        return {
            "type": "object",
            "title": "ToolCallOutput",
            "description": (
                "The dispatched action's result. Wire downstream fields as "
                "output.<field>; the inner shape depends on the action."
            ),
            "properties": {
                "action": {"type": "string", "title": "action"},
                "output": {"type": "object", "title": "output"},
            },
            "additionalProperties": False,
        }


class ToolCallExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="tool.call",
        category=NodeCategory.TOOL,
        display_name="Run an Action",
        description="Run any Action from the catalog: a connected app's tool, "
        "your own API, a workflow, an agent or any built-in Action, with its input.",
        input_schema=ToolCallInput,
        output_schema=ToolCallOutput,
        config_schema=ToolCallConfig,
        # The dispatched action is chosen at RUN time, so no static kind can
        # describe this node's output. dynamic_output keeps the registry from
        # auto-deriving a fixed workflow_io contract kind that would be
        # stamped (wrongly) onto whatever the target action actually returned.
        dynamic_output=True,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
        icon="wrench",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: ToolCallInput,
        config: ToolCallConfig,
    ) -> NodeResult[ToolCallOutput]:
        from matrx_graph.actions.decorator import _step_result, step_idempotency_key
        from matrx_graph.actions.registry import default_action_registry
        from matrx_graph.executor.execution import current_execution

        name = config.action_name
        raw_inputs = inputs.model_dump(mode="json")
        merged: dict[str, Any]
        if config.merge_inputs:
            top = {k: v for k, v in raw_inputs.items() if k != "payload"}
            merged = {**top, **(raw_inputs.get("payload") or {})}
        else:
            merged = raw_inputs.get("payload") or {}

        # A run being stopped never starts a side effect it would then have to undo.
        execution = current_execution()
        if execution is not None and execution.stopping is not None and await execution.stopping():
            return failure("run_stopping", f"The run is being stopped, so {name} was not started.")

        try:
            spec = await default_action_registry().resolve(name, app=ctx.app)
        except NodeRegistryError:
            spec = None
        if spec is not None and not (spec.engine == "code" and spec.work is None):
            # THE one router (``run_action``) on the step door, exactly as an Action's own generated
            # step runs: the run's carried app (actor, organization, execution id — never rebuilt),
            # the apply gate, the idempotency ledger keyed by the attempt-independent step key, so a
            # retry or a re-run from a checkpoint replays the first answer instead of acting twice.
            if "step" not in spec.doors:
                return failure(
                    "door_closed",
                    f"{name} cannot be run from a workflow step; it opens only {sorted(spec.doors)}.",
                )
            result = await _step_result(spec, ctx.app, merged, step_idempotency_key(ctx), run_id=ctx.run_id)
            if not isinstance(result, Success):
                return result
            out = result.result
            output_dict = out.model_dump(mode="json") if isinstance(out, BaseModel) else dict(out)
            from matrx_graph.content_ir.envelope import stamp_kind_marker

            stamp_kind_marker(output_dict, spec.node_spec.output_kind)
            return success(ToolCallOutput(action=spec.name, output=output_dict))
        return await self._run_step_only(ctx, merged, config)

    async def _run_step_only(
        self, ctx: NodeExecutionContext, merged: dict[str, Any], config: ToolCallConfig
    ) -> NodeResult[ToolCallOutput]:
        """A step-only node (no work function of its own): it IS a step, so it runs as one, here."""
        try:
            target = resolve_action_executor(config.action_name)
        except NodeRegistryError as e:
            return failure("unknown_action", str(e))

        try:
            action_inputs = target.spec.input_schema.model_validate(merged)
        except Exception as e:  # noqa: BLE001 — pydantic + custom validators
            return failure(
                "invalid_input",
                f"tool.call → {config.action_name}: input validation failed: {e}",
            )

        # Reuse this node's context — actions see the same user/org/emitter.
        action_output = await target.execute(ctx, action_inputs, config)

        # Node Result System: the wrapped action may return the NodeResult
        # envelope. Interpret it through the shared helper — a Success
        # unwraps to its payload; an inner Failure becomes tool.call's OWN
        # Failure, preserving the inner code/message/details (including
        # details.usage so the scheduler's cost settlement survives).
        from matrx_graph.types.result import interpret_node_result

        try:
            interpreted = interpret_node_result(action_output)
        except TypeError as e:
            raise ExecutionError(f"tool.call → {config.action_name}: {e}") from e
        if interpreted.error is not None:
            return failure(
                interpreted.error.code,
                interpreted.error.message,
                details=interpreted.error.details,
            )
        action_output = interpreted.payload
        if not isinstance(action_output, BaseModel):
            raise ExecutionError(
                f"tool.call → {config.action_name}: interpreted payload is "
                f"{type(action_output).__name__}, expected BaseModel."
            )
        output_dict = action_output.model_dump(mode="json")
        # The inner action's payload is a node output crossing a named
        # boundary — it just happens to travel NESTED under `output` instead
        # of at a settled root, so the scheduler's settlement stamping (which
        # only ever touches the root, and tool.call declares no output_kind of
        # its own) never reaches it. Unstamped, the wrapped action's identity
        # evaporated the moment it entered the envelope: a consumer of
        # tool.call could see WHICH action ran but not WHAT it produced. Same
        # helper, same rules as settlement — the target's registered
        # output_kind, never over a marker the payload declared itself.
        from matrx_graph.content_ir.envelope import stamp_kind_marker

        stamp_kind_marker(output_dict, target.spec.output_kind)
        return success(ToolCallOutput(action=config.action_name, output=output_dict))
