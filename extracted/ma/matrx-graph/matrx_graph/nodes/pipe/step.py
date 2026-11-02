"""``pipe.step`` — one step, three interchangeable pipes.

The step declares a CONTRACT once (what it is, what a valid result looks
like). Which pipe satisfies that contract — code, a person, or an agent — is
configuration, selectable per run, and downstream steps cannot tell the
difference. See FEATURE.md beside this file for the decision record.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, JsonValue, RootModel

from matrx_graph.decisions import DECISION_KEY, build_escalation_payload
from matrx_graph.executor.schema_validation import validate_instance
from matrx_graph.nodes._template import render_template_string
from matrx_graph.nodes.pipe.contract import (
    Pipe,
    PipeSelection,
    PipeStepConfig,
    dig,
    select_pipe,
)
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import (
    Failure,
    NodeResult,
    failure,
    interpret_node_result,
    success,
)


class AiPipeRequest(BaseModel):
    """Everything an AI pipe runner needs, and nothing engine-specific.

    Deliberately transport-free so the injected runner can be an Mandate
    call, a direct agent run, or a test double.
    """

    model_config = ConfigDict(extra="forbid")

    mandate_key: str
    agent_id: str
    instruction: str
    inputs: dict[str, JsonValue]
    output_schema: dict[str, JsonValue]
    output_kind: str | None
    step_name: str


AiPipeRunner = Callable[[NodeExecutionContext, AiPipeRequest], Awaitable[dict[str, JsonValue]]]

_ai_runner: AiPipeRunner | None = None


def set_ai_pipe_runner(runner: AiPipeRunner | None) -> None:
    """Register the host's AI-pipe implementation (None unregisters).

    Same injection seam as ``set_subgraph_resolver``: matrx-graph owns the
    step abstraction and the code + human pipes outright, and never imports
    an AI package. aidream wires this in ``package_integration.py``. With no
    runner registered the AI pipe fails LOUDLY at the moment it is selected —
    it never silently degrades to another pipe.
    """
    global _ai_runner
    _ai_runner = runner


def ai_pipe_configured() -> bool:
    return _ai_runner is not None


class PipeStepInput(BaseModel):
    # Permissive: whatever upstream steps wired in is the material this step
    # reasons over, and it is interpolated into the question / handed to the
    # agent / passed to the delegate node.
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "x-contract-dynamic": "author-wired upstream values; the step contract types the OUTPUT"
        },
    )


class PipeStepOutput(RootModel[dict[str, JsonValue]]):
    """Typed JSON object after validation against the authored step contract.

    The exact fields remain author-defined and are compiled from
    ``config.contract.output_schema``. The registered runtime boundary is
    nevertheless precise: an object whose values are valid JSON. RootModel
    preserves the existing flat payload shape when dumped, so downstream
    nodes still receive the authored fields rather than a wrapper key.
    """


def _contract_errors(payload: Any, config: PipeStepConfig, pipe: Pipe) -> Failure | None:
    if not isinstance(payload, dict):
        return failure(
            "contract_violation",
            f"The {pipe} pipe for '{config.contract.name}' produced a "
            f"{type(payload).__name__}, but this step's contract declares an "
            "object. Every pipe must satisfy the same contract — that is what "
            "makes them interchangeable.",
            details={"pipe": pipe, "received_type": type(payload).__name__},
        )
    # The reserved provenance key is ENGINE state, never part of the author's
    # contract — same exclusion the scheduler applies on resume, so a stamped
    # value validates identically no matter which pipe produced it.
    subject = {k: v for k, v in payload.items() if k != DECISION_KEY}
    errors = validate_instance(config.contract.output_schema, subject)
    if errors:
        return failure(
            "contract_violation",
            f"The {pipe} pipe for '{config.contract.name}' produced a result "
            "that does not satisfy this step's contract:\n  - " + "\n  - ".join(errors),
            details={"pipe": pipe, "field_errors": errors},
        )
    return None


class PipeStepExecutor:
    """One step whose executor is configuration, not identity."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="pipe.step",
        category=NodeCategory.PIPE,
        display_name="Flexible Step",
        description=(
            "Do one step of the work — and choose whether code does it, a "
            "person does it, or an agent does it. The result is the same "
            "shape either way, so you can switch without rebuilding anything."
        ),
        input_schema=PipeStepInput,
        output_schema=PipeStepOutput,
        config_schema=PipeStepConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
        can_interrupt=True,
        dynamic_output=True,
        icon="git-fork",
        tags=("pipe", "human", "ai", "decision"),
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: PipeStepInput,
        config: PipeStepConfig,
    ) -> NodeResult[PipeStepOutput]:
        namespace = inputs.model_dump(mode="json")
        run_variables = getattr(ctx.app, "initial_variables", None)
        selection = select_pipe(config, node_id=ctx.node_id, run_variables=run_variables)

        if selection.pipe is None:
            wanted = selection.requested or config.policy.pipe
            return failure(
                "no_pipe_available",
                f"Step '{config.contract.name}' was asked to run on the "
                f"{wanted} pipe, which is not set up on this step"
                + (
                    f" (available: {', '.join(selection.available)})."
                    if selection.available
                    else " — and no pipe is set up on it at all."
                )
                + _how_to_fix(wanted),
                details={
                    "requested_pipe": wanted,
                    "available_pipes": selection.available,
                },
            )

        await _announce(ctx, config, selection)

        if selection.pipe == "human":
            return self._ask_person(ctx, config, namespace, selection)
        if selection.pipe == "ai":
            return await self._run_agent(ctx, config, namespace)
        return await self._run_code(ctx, config, inputs)

    # -- human -----------------------------------------------------------
    def _ask_person(
        self,
        ctx: NodeExecutionContext,
        config: PipeStepConfig,
        namespace: dict[str, Any],
        selection: PipeSelection,
    ) -> NodeResult[PipeStepOutput]:
        prompt, _ = render_template_string(
            config.contract.prompt_text(), namespace, whole_key="inputs"
        )
        guidance, _ = render_template_string(
            config.pipes.human.instructions, namespace, whole_key="inputs"
        )
        # schema_hint IS the contract: the engine validates the person's
        # answer against it at resume (schema_validation.
        # resume_value_validation_errors) and records the validated value as
        # this node's output. That is why a human-produced result is
        # indistinguishable from a code- or AI-produced one downstream.
        payload: dict[str, Any] = {
            "prompt": prompt,
            "schema_hint": dict(config.contract.output_schema),
            "context": namespace,
            "default_answer": dict(config.pipes.human.default_answer),
            # Pipe provenance + the escalation contract, durable on the
            # interrupt checkpoint. An escalator (G-HUMAN-TIMEOUT) reads
            # these to decide when to take over and with which pipe; nothing
            # here waits in process memory.
            "pipe": "human",
            "step_name": config.contract.name,
            "guidance": guidance,
        }
        # The deadline is frozen ABSOLUTE into durable checkpoint state by the
        # platform's ONE escalation primitive — the same block control.human_input
        # publishes, so the escalation sweeper reads one shape for every asking
        # node in the engine.
        escalation = build_escalation_payload(config.policy.escalation)
        if escalation is not None:
            payload["escalation"] = escalation
        ctx.interrupt(payload)
        # unreachable — ctx.interrupt() raises GraphInterrupt
        return success(PipeStepOutput())

    # -- ai --------------------------------------------------------------
    async def _run_agent(
        self,
        ctx: NodeExecutionContext,
        config: PipeStepConfig,
        namespace: dict[str, Any],
    ) -> NodeResult[PipeStepOutput]:
        if _ai_runner is None:
            return failure(
                "no_ai_pipe_runner",
                "The AI pipe is selected but no AI runner is registered. Call "
                "matrx_graph.nodes.pipe.set_ai_pipe_runner(fn) at app startup "
                "(aidream wires this in package_integration.py).",
            )
        instruction_parts = [config.contract.prompt_text(), config.pipes.ai.instructions]
        instruction, _ = render_template_string(
            "\n\n".join(part for part in instruction_parts if part.strip()),
            namespace,
            whole_key="inputs",
        )
        request = AiPipeRequest(
            mandate_key=config.pipes.ai.mandate_key.strip(),
            agent_id=config.pipes.ai.agent_id.strip(),
            instruction=instruction,
            inputs=namespace,
            output_schema=dict(config.contract.output_schema),
            output_kind=config.contract.output_kind,
            step_name=config.contract.name,
        )
        try:
            produced = await _ai_runner(ctx, request)
        except Exception as exc:  # noqa: BLE001 — becomes a structured node failure
            return failure(
                "ai_pipe_failed",
                f"The agent for '{config.contract.name}' failed: {exc}",
                details={"pipe": "ai", "error": str(exc)},
            )
        violation = _contract_errors(produced, config, "ai")
        if violation is not None:
            return violation
        return success(PipeStepOutput.model_validate(produced))

    # -- code ------------------------------------------------------------
    async def _run_code(
        self,
        ctx: NodeExecutionContext,
        config: PipeStepConfig,
        inputs: PipeStepInput,
    ) -> NodeResult[PipeStepOutput]:
        from matrx_graph.executor.registry import default_registry

        registry = ctx.registry or default_registry()
        code = config.pipes.code
        try:
            delegate = registry.get(code.node_type)
        except Exception as exc:  # noqa: BLE001 — NodeRegistryError, as a failure
            return failure(
                "code_pipe_unknown_node",
                f"The code pipe for '{config.contract.name}' delegates to "
                f"'{code.node_type}', which no executor is registered for: {exc}",
                details={"pipe": "code", "node_type": code.node_type},
            )
        spec = delegate.spec
        namespace = inputs.model_dump(mode="json")
        # An authored map narrows/renames the step's inputs for the delegate;
        # unmapped, the delegate receives the whole namespace (unchanged
        # behavior). A path that does not resolve becomes an explicit None so
        # the delegate's own validation names the missing field.
        payload = (
            {field: dig(namespace, path) for field, path in code.inputs.items()}
            if code.inputs
            else namespace
        )
        try:
            delegate_inputs = spec.input_schema.model_validate(payload)
            delegate_config = spec.config_schema.model_validate(dict(code.config))
        except Exception as exc:  # noqa: BLE001
            return failure(
                "code_pipe_bad_binding",
                f"The code pipe for '{config.contract.name}' could not hand its "
                f"values to '{code.node_type}': {exc}",
                details={"pipe": "code", "node_type": code.node_type},
            )
        raw = await delegate.execute(ctx, delegate_inputs, delegate_config)
        interpreted = interpret_node_result(raw)
        if interpreted.error is not None:
            return Failure(error=interpreted.error)
        produced_model = interpreted.payload
        produced = produced_model.model_dump(mode="json") if produced_model else {}
        picked = dig(produced, code.output_path)
        violation = _contract_errors(picked, config, "code")
        if violation is not None:
            return violation
        return success(PipeStepOutput.model_validate(picked))


def _how_to_fix(pipe: Pipe) -> str:
    if pipe == "ai":
        return (
            " Bind an Mandate (or a saved agent) to this step's AI pipe, or "
            "give the step a fallback pipe."
        )
    if pipe == "code":
        return (
            " Choose the action this step's code pipe should run, or give the step a fallback pipe."
        )
    return " Turn this step's human pipe back on, or give the step a fallback pipe."


async def _announce(
    ctx: NodeExecutionContext, config: PipeStepConfig, selection: PipeSelection
) -> None:
    """Say which pipe ran, in the run's own timeline.

    Provenance is deliberately kept OUT of the payload: a downstream step
    that could read which pipe produced its input would break the property
    this whole node exists to guarantee. The run timeline is where the
    answer belongs.
    """
    label = {"code": "automatically", "human": "by a person", "ai": "by an agent"}[
        selection.pipe or "code"
    ]
    note = f"{config.contract.name} — {label}"
    if selection.substituted:
        note += f" (asked for {selection.requested}, which isn't set up on this step)"
    await ctx.progress(note)
