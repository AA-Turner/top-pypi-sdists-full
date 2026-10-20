"""``ai.mandate.start`` — Run Mandate: run the JOB, whoever your org gave it to.

WHY THIS IS A DIFFERENT STEP FROM RUN AGENT (Arman's ruling, 2026-09-10)
-----------------------------------------------------------------------
Run Agent and Run Mandate "have nothing in common and it would be silly and
stupid to attempt to make them the same… a mandate is not a representation of
an agent. It's a representation of some sort of intelligence… Agents work with
an ID, a version number, and then mapping of inputs and outputs. And a mandate
doesn't have that sort of thing."

So:

* **Run Agent** (``ai.agent.start``) names an agent: id + version + the input
  and output mapping. It has NO mandate field, and refuses one loudly.
* **Run Mandate** (this node) names a Mandate KEY. It has no agent id and no
  version, because neither is its to choose — the database is. Its Holder may
  be an agent OR a whole workflow, and the workflow case runs as a durable
  child run (the step-side lift).

Mandates exist inside workflows for exactly one reason: so a person can tweak
ONE part of a system-wide workflow — by rebinding the job to a different doer —
without copying the workflow. Building a workflow out of mandates for its own
sake is not the point.

Everything after "which thing runs" is the SAME code Run Agent uses:
``resolve_step_agent_full`` → ``build_agent_request`` → ``run_step_agent``.
This is not a second way to run intelligence; it is the same way, entered by a
different door.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import ConfigDict, Field

from matrx_ai._ext import has_ext
from matrx_ai.graph_nodes.agent_action import (
    _AGENT_RESULT_BOOKKEEPING,
    _AGENT_RESULT_QUORUM,
    _AGENT_RESULT_WITNESSES,
    AgentRunCommonInput,
    AgentStartConfig,
    StepWorkflowMandate,
    _run_workflow_held_mandate,
    _strip_inert_burned_tool_fields,
    build_agent_request,
    mandate_key_field,
    require_agent_host,
    resolve_step_agent_full,
    run_step_agent,
)
from matrx_ai.graph_nodes.iteration_limit import resolve_step_iteration_limit
from matrx_ai.graph_nodes.shared import AiExecutionResult, normalize_completed_result

logger = logging.getLogger(__name__)

_NODE_TYPE = "ai.mandate.start"


class MandateStartStrictInput(AgentRunCommonInput):
    """Run Mandate's request body: the job, plus the shared run lift.

    ``mandate_key`` is REQUIRED — a Run Mandate step with no job named is not a
    step at all. There is deliberately no ``agent_id`` and no ``is_version``:
    who does the job is the database's answer, re-asked on every run, and a
    frozen id beside it would be exactly the hardcoded agent the Mandate system
    exists to abolish.
    """

    model_config = ConfigDict(extra="forbid")

    mandate_key: str = mandate_key_field(required=True)
    #: THE STATE AT THE CALL POINT: every value the mandate's provision offers, by its offered name
    #: (Arman, 2026-10-14). The mandate's BINDING decides what the doer receives: which values, joined
    #: how, under which of its own variable names. Nothing upstream shapes values for one agent.
    provision_values: dict[str, Any] | None = Field(
        default=None,
        description=("Every value the mandate's provision offers at this point, by offered name. The "
                     "mandate's binding picks and joins them into the doer's inputs."),
    )


class MandateStartInput(MandateStartStrictInput):
    """Run Mandate input plus authored top-level variable connection points.

    Extras are allowed for the same reason Run Agent allows them: a workflow
    author exposes the doer's variable names as node ports, and an edge feeding
    one arrives as a top-level extra keyed by the variable name.
    """

    model_config = ConfigDict(extra="allow")


def agent_variables_outside_provision(inputs: MandateStartInput) -> list[str]:
    """The doer's variable names this step was fed OUTSIDE ``provision_values``.

    A Run Mandate step hands the mandate its STATE by the provision's offered names, and the
    mandate's BINDING decides what the doer receives (Arman, 2026-10-19). A value fed under
    the doer's own variable names (a top-level port, or the ``variables`` dict) skips the
    binding — the step is either a faked mandate (really Run Agent) or a real one bypassing
    its binding. An upstream agent result broadcast down an unmapped edge is bookkeeping,
    not variables, and is ignored here exactly as the request builder drops it.
    """
    extras = dict(inputs.model_extra or {})
    _strip_inert_burned_tool_fields(extras)
    present = [k for k in extras if k in _AGENT_RESULT_BOOKKEEPING]
    if len(present) >= _AGENT_RESULT_QUORUM and (_AGENT_RESULT_WITNESSES & set(present)):
        extras = {k: v for k, v in extras.items() if k not in _AGENT_RESULT_BOOKKEEPING}
    names = sorted(extras)
    names += sorted(f"variables.{k}" for k in (inputs.variables or {}))
    return names


def refuse_agent_variables_outside_provision(inputs: MandateStartInput, node_id: str) -> None:
    """Refuse, before anything resolves or spends, a step that feeds the doer by name."""
    names = agent_variables_outside_provision(inputs)
    if not names:
        return
    raise ValueError(
        f"{_NODE_TYPE}:{node_id} (mandate {inputs.mandate_key!r}) was fed {names} outside "
        "provision_values. A Run Mandate step hands the mandate its state — every value it has, "
        "under the provision's offered names — as provision_values, and the mandate's binding "
        "picks what the doer gets. Fix: wire those values into provision_values (in code, "
        "aidream/workflows/step_state.hand_state_to_mandate). If they are simply the agent's own "
        "inputs, one-to-one, this is not a mandate step: make it a Run Agent step "
        "(ai.agent.start) naming that agent."
    )


def _state_as_extras(inputs: MandateStartInput) -> MandateStartInput:
    """A workflow Holder takes the state on its own input surface: the provision values ride as the supplied
    offer (by offered name) and the workflow runner applies the mandate's binding to them."""
    if inputs.provision_values is None:
        return inputs
    extras = dict(inputs.model_extra or {})
    return MandateStartInput.model_validate(
        {**inputs.model_dump(exclude={"provision_values"}, exclude_none=True), **inputs.provision_values, **extras}
    )


async def _bind_provision_values(inputs: MandateStartInput, resolved: Any) -> MandateStartInput:
    """Run the step's provision values (THE STATE at the point) through the mandate's BINDING (the host's
    one consumption pipeline): the variables the doer runs on replace the raw state. Edge-fed variables
    (top-level extras) still ride beside them; a binding variable of the same name wins.

    Without ``provision_values`` the step behaves exactly as before. It REFUSES, never runs unbound, when:
    the point handed an empty state (nothing was captured), the host offers no pipeline, or the mandate has
    no binding map — the default pin would hand the doer every value of the state by name.
    """
    supplied = inputs.provision_values
    if supplied is None:
        return inputs
    where = f"{_NODE_TYPE}: mandate {inputs.mandate_key!r}"
    if not supplied:
        raise ValueError(f"{where} was handed an empty state — the point before it captured nothing, so "
                         "there is nothing to bind. See that step's error.")
    materialize = getattr(resolved, "materialize", None)
    if materialize is None:
        raise ValueError(f"{where} was handed its provision values, but this host offers no consumption "
                         "pipeline to apply the mandate's binding — the doer cannot receive the state unbound.")
    if not getattr(resolved, "consumption_map", None):
        raise ValueError(f"{where} has no binding map: the whole state would reach the doer by name. Bind the "
                         "doer's inputs on the mandate's Binding tab (its default consumption map).")
    variables = await materialize(dict(supplied))
    extras = dict(inputs.model_extra or {})
    return MandateStartInput.model_validate(
        {**inputs.model_dump(exclude={"provision_values"}, exclude_none=True), **extras, **variables}
    )


@register_node(
    name=_NODE_TYPE,
    display_name="Run Mandate",
    description=(
        "Run a named job — your organization decides which agent or workflow "
        "actually does it, looked up fresh every time this step runs."
    ),
    category=NodeCategory.AGENT,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=MandateStartInput,
    output_schema=AiExecutionResult,
    output_kind="agent_result",
    config_schema=AgentStartConfig,
    icon="target",
    tags=("ai", "mandate", "agent"),
)
async def mandate_start(
    ctx: NodeExecutionContext,
    inputs: MandateStartInput,
    config: AgentStartConfig | None = None,
) -> NodeResult[AiExecutionResult]:
    require_agent_host(_NODE_TYPE)
    # MANDATE CANDIDATES — the host observes this real run: the step's inputs
    # and config are copied HERE, before the body mutates them
    # (``inputs.max_iterations``), and a candidate Holder may re-run them in the
    # background. The tap never alters the step.
    from matrx_ai.mandate_taps import tapped_door

    return await tapped_door(
        "workflow_step",
        inputs.mandate_key,
        lambda: {
            "node_type": _NODE_TYPE,
            "node_id": getattr(ctx, "node_id", None),
            "run_id": getattr(ctx, "run_id", None),
            "inputs": inputs.model_copy(),
            "config": config.model_copy() if config is not None else None,
        },
        lambda: _mandate_start_body(ctx, inputs, config),
    )


async def _mandate_start_body(
    ctx: NodeExecutionContext,
    inputs: MandateStartInput,
    config: AgentStartConfig | None,
) -> NodeResult[AiExecutionResult]:
    node_id = getattr(ctx, "node_id", None) or "?"
    refuse_agent_variables_outside_provision(inputs, node_id)
    resolved = await resolve_step_agent_full(
        inputs,
        consumer=f"{_NODE_TYPE}:{node_id}",
        # A Mandate's Holder is legitimately a whole workflow. This is the node
        # type that knows how to run that lane, so it is the one that opts in.
        allow_workflow_holder=has_ext("workflow_mandate_runner"),
    )
    declared_variables = list(getattr(config, "exposed_variables", None) or [])
    if isinstance(resolved, StepWorkflowMandate):
        return await _run_workflow_held_mandate(
            ctx, _state_as_extras(inputs), resolved, declared_variables=declared_variables
        )
    limit = await resolve_step_iteration_limit(ctx, inputs.max_iterations)
    inputs.max_iterations = limit.value
    inputs = await _bind_provision_values(inputs, resolved)
    request = build_agent_request(
        ctx,
        inputs,
        resolved,
        node_type=_NODE_TYPE,
        declared_variables=declared_variables,
        variable_sources=dict(getattr(config, "variable_sources", None) or {}),
    )
    # AI TEST MODE — the host may answer this exact step from a recorded test baseline (opt-in per
    # test session only; ``mandate_taps.MandateReplay``). Not installed / real mode → None → real run.
    from matrx_ai.mandate_taps import replay_lookup, replay_store

    run_id = getattr(ctx, "run_id", None)
    fingerprint = {
        "inputs": inputs.model_dump(mode="json", exclude_none=True),
        "agent_id": resolved.agent_id,
        "is_version": resolved.is_version,
        "config_overrides": resolved.config_overrides or {},
        "declared_variables": declared_variables,
        "variable_sources": dict(getattr(config, "variable_sources", None) or {}),
    }
    replayed = await replay_lookup("workflow_step", inputs.mandate_key, run_id, fingerprint)
    if replayed is not None:
        return success(AiExecutionResult.model_validate(replayed))

    completed = await run_step_agent(
        ctx,
        resolved.agent_id,
        request,
        mandate_key=inputs.mandate_key,
        run_stamp=resolved.run_stamp,
    )

    # A host agent_runner may return an ALREADY-normalized AiExecutionResult
    # (a compiled Orchestra whose final step IS the result). Pass it through.
    if isinstance(completed, AiExecutionResult):
        completed.metadata.setdefault("agent_id", resolved.agent_id)
        await replay_store("workflow_step", inputs.mandate_key, run_id, fingerprint,
                           completed.model_dump(mode="json"))
        return success(completed)
    result = await asyncio.to_thread(normalize_completed_result, completed)
    # WHO did the job: the doer the database resolved for this run (a research
    # row records it as agent_id, exactly as the research code path does).
    payload = getattr(result, "result", None)
    if isinstance(payload, AiExecutionResult):
        payload.metadata["agent_id"] = resolved.agent_id
        await replay_store("workflow_step", inputs.mandate_key, run_id, fingerprint,
                           payload.model_dump(mode="json"))
    return limit.name_on(result)
