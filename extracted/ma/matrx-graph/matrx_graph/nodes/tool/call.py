"""tool.call — dynamic action dispatcher.

Takes an action name from config + a payload from inputs, looks the action up
in the action registry at execution time, validates the payload against the
action's Pydantic input_schema, invokes the action's executor, and returns
the action's output nested under ``output`` (a stable output schema
regardless of which action runs).

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
from matrx_graph.types.result import NodeResult, failure, success
from matrx_graph.types.usl import field_extras


class ToolCallInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    payload: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="Arguments passed to the invoked action (merged with top-level "
        "inputs when merge_inputs is on).",
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
        description="Name of the registered action to invoke (e.g. 'news_api.top_headlines').",
        json_schema_extra=field_extras(widget="action_picker"),
    )
    merge_inputs: bool = Field(
        default=True,
        description=(
            "If true, merge `inputs.payload` with `inputs` (top-level) before "
            "passing to the action. Lets callers pass args inline without "
            "nesting under 'payload'."
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
        display_name="Run Action",
        description="Run any available action, chosen by name while the workflow runs.",
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
        try:
            target = resolve_action_executor(config.action_name)
        except NodeRegistryError as e:
            return failure("unknown_action", str(e))

        raw_inputs = inputs.model_dump(mode="json")
        merged: dict[str, Any]
        if config.merge_inputs:
            top = {k: v for k, v in raw_inputs.items() if k != "payload"}
            merged = {**top, **(raw_inputs.get("payload") or {})}
        else:
            merged = raw_inputs.get("payload") or {}

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
