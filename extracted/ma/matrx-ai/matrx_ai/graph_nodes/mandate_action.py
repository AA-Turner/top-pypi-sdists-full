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

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import ConfigDict

from matrx_ai._ext import has_ext
from matrx_ai.graph_nodes.agent_action import (
    AgentRunCommonInput,
    AgentStartConfig,
    StepWorkflowMandate,
    _run_workflow_held_mandate,
    build_agent_request,
    mandate_key_field,
    require_agent_host,
    resolve_step_agent_full,
    run_step_agent,
)
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


class MandateStartInput(MandateStartStrictInput):
    """Run Mandate input plus authored top-level variable connection points.

    Extras are allowed for the same reason Run Agent allows them: a workflow
    author exposes the doer's variable names as node ports, and an edge feeding
    one arrives as a top-level extra keyed by the variable name.
    """

    model_config = ConfigDict(extra="allow")


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
    node_id = getattr(ctx, "node_id", None) or "?"
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
            ctx, inputs, resolved, declared_variables=declared_variables
        )
    request = build_agent_request(
        ctx, inputs, resolved, node_type=_NODE_TYPE, declared_variables=declared_variables
    )
    completed = await run_step_agent(ctx, resolved.agent_id, request)

    # A host agent_runner may return an ALREADY-normalized AiExecutionResult
    # (a compiled Orchestra whose final step IS the result). Pass it through.
    if isinstance(completed, AiExecutionResult):
        return success(completed)
    return await asyncio.to_thread(normalize_completed_result, completed)
