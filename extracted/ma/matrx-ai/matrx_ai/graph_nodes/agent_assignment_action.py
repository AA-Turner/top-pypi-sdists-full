"""Durable coordinated assignment of resolved values to an ordinary agent.

The assignment engine never knows about agents. It persists immutable value
maps, leases them, and calls the executor below. The executor converts each
map into the same strict host request used by ``ai.agent.start``; the agent
system therefore remains oblivious to planning, retries, and coordination.
"""

from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable
from uuid import NAMESPACE_URL, uuid5

from matrx_assignment import (
    AssignmentBatchResult,
    AssignmentCoordinator,
    AssignmentExecutionOutput,
    AssignmentPlan,
    AssignmentPlanner,
    AssignmentSessionRequest,
    AssignmentSessionSummary,
    AssignmentSource,
)
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_graph.actions import register_node
from matrx_graph.contract_kinds import ContractDirection, ContractFamily, contract_from_model
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

from matrx_ai._ext import get_ext, has_ext
from matrx_ai.graph_nodes.agent_action import (
    AgentStartStrictInput,
    _resolve_conversation_start_fields,
    resolve_step_agent,
)
from matrx_ai.graph_nodes.shared import AiExecutionResult, normalize_completed


class AgentAssignmentBatchInput(BaseModel):
    """Strict runtime override for one durable coordinated agent session."""

    model_config = ConfigDict(extra="forbid")

    agent: AgentStartStrictInput = Field(
        description="Saved-agent invocation template applied once to every resolved assignment."
    )
    plan: AssignmentPlan = Field(
        description="Coordinated rows, random options, or Cartesian values to materialize once."
    )
    session_key: str | None = Field(
        default=None,
        min_length=1,
        max_length=500,
        description=(
            "Optional caller-owned idempotency key. Workflow execution identity "
            "is used when omitted, so a node retry resumes the same session."
        ),
    )
    max_attempts: int = Field(
        default=3, ge=1, le=20, description="Maximum execution attempts allowed for each item."
    )
    lease_seconds: int = Field(
        default=900,
        ge=30,
        le=86_400,
        description="Seconds an item claim remains valid without renewal.",
    )
    max_concurrency: int = Field(
        default=5,
        ge=1,
        le=100,
        description="Maximum assignment items executed concurrently by this run.",
    )
    retry_delay_seconds: int = Field(
        default=0,
        ge=0,
        le=86_400,
        description="Delay before a retryable item becomes claimable again.",
    )
    metadata: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="Caller metadata preserved on the durable assignment session.",
    )

    @model_validator(mode="after")
    def require_fresh_per_item_conversations(self) -> AgentAssignmentBatchInput:
        if self.agent.conversation_id is not None or self.agent.is_new is not None:
            raise ValueError(
                "coordinated agent assignments own one durable conversation per item; "
                "agent.conversation_id and agent.is_new must be omitted"
            )
        return self


_AGENT_OUTPUT_KIND = contract_from_model(
    family=ContractFamily.ACTION_IO,
    source_name="ai.agent.start",
    direction=ContractDirection.OUTPUT,
    model=AiExecutionResult,
    source_id="ai.agent.start",
).kind

AssignmentProgressCallback = Callable[[int, int], Awaitable[None]]
AssignmentSessionCallback = Callable[[AssignmentSessionSummary], Awaitable[None]]


async def run_agent_assignment_batch(
    app: AppContext,
    inputs: AgentAssignmentBatchInput,
    *,
    source: AssignmentSource,
    idempotency_key: str,
    holder: str,
    progress: AssignmentProgressCallback | None = None,
    session_started: AssignmentSessionCallback | None = None,
) -> AssignmentBatchResult:
    """Run or resume one durable batch through the ordinary agent executor."""

    required = (
        "agent_runner",
        "AgentStartRequest",
        "assignment_store_factory",
        "assignment_conversation_exists",
    )
    missing = [name for name in required if not has_ext(name)]
    if missing:
        raise RuntimeError(
            "agent assignment execution requires host injection for " + ", ".join(missing)
        )

    materialized = AssignmentPlanner().materialize(inputs.plan)
    request = AssignmentSessionRequest(
        idempotency_key=idempotency_key,
        plan=inputs.plan,
        source=source,
        max_attempts=inputs.max_attempts,
        lease_seconds=inputs.lease_seconds,
        max_concurrency=inputs.max_concurrency,
        retry_delay_seconds=inputs.retry_delay_seconds,
        result_kind=_AGENT_OUTPUT_KIND,
        metadata=inputs.metadata,
    )
    store = get_ext("assignment_store_factory")(app)
    if inspect.isawaitable(store):
        store = await store
    session = await store.create_or_get_session(request, materialized)
    if session_started is not None:
        await session_started(session)
    coordinator = AssignmentCoordinator(store, holder=holder)

    agent_runner = get_ext("agent_runner")
    AgentStartRequest = get_ext("AgentStartRequest")
    conversation_exists = get_ext("assignment_conversation_exists")

    # ONE door for "which agent does this step run" — a batch may name a
    # Mandate exactly like a single agent step, resolved once for the whole
    # batch (every item runs the same job, so resolving per item would let a
    # mid-batch rebind split one batch across two agents).
    agent_id, agent_is_version, agent_mandate_overrides = await resolve_step_agent(
        inputs.agent, consumer=f"ai.agent.assignment_batch:{holder}"
    )

    async def execute(claim):
        conversation_id = claim.item.conversation_id
        if not conversation_id:
            raise RuntimeError("assignment item is missing its durable conversation_id")
        request_id = str(uuid5(NAMESPACE_URL, f"{claim.item.id}:agent-request"))
        child_ctx = app.fork_for_workflow_step(conversation_id).with_overrides(
            request_id=request_id,
            operation_id=claim.attempt_id,
        )
        payload = inputs.agent.model_dump(
            exclude_none=True,
            exclude={"agent_id", "mandate_key", "conversation_id", "is_new"},
        )
        payload["is_version"] = agent_is_version
        if agent_mandate_overrides:
            payload["config_overrides"] = {
                **agent_mandate_overrides,
                **(payload.get("config_overrides") or {}),
            }
        payload["conversation_id"] = conversation_id
        exists = conversation_exists(conversation_id)
        if inspect.isawaitable(exists):
            exists = await exists
        payload["is_new"] = not exists
        # store is REQUIRED on the host request (ConversationStartRequest);
        # AgentStartInput defaults it to True, but exclude_none can't drop a
        # bool so this only fills the case where the node input omits it.
        # ONE resolver for the host request's required conversation-start
        # fields — conversation_id/is_new are already set above, so this fills
        # `store` and inherits the RUN's organization (plain-sentence refusal
        # when there is none), exactly like a plain agent step.
        _resolve_conversation_start_fields(payload, organization_id=app.organization_id)
        payload["variables"] = {
            **(payload.get("variables") or {}),
            **claim.item.values,
        }
        agent_request = AgentStartRequest.model_validate(payload)
        token = set_app_context(child_ctx)
        try:
            completed = await agent_runner(agent_id, agent_request, child_ctx)
        finally:
            clear_app_context(token)
        result = normalize_completed(completed)
        return AssignmentExecutionOutput(
            value=result.model_dump(mode="json"),
            kind=_AGENT_OUTPUT_KIND,
            conversation_id=result.conversation_id or conversation_id,
        )

    return await coordinator.run(
        session.id,
        request,
        execute,
        progress=progress,
    )


@register_node(
    name="ai.agent.assignment_batch",
    display_name="Run Agent in Batches",
    description="Run a saved agent once for every combination of inputs, reliably.",
    category=NodeCategory.AGENT,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=AgentAssignmentBatchInput,
    output_schema=AssignmentBatchResult,
    output_kind="agent_assignment_batch_result",
    icon="list-restart",
    tags=("ai", "agent", "assignment", "batch", "durable"),
)
async def agent_assignment_batch(
    ctx: NodeExecutionContext,
    inputs: AgentAssignmentBatchInput,
) -> NodeResult[AssignmentBatchResult]:
    materialized = AssignmentPlanner().materialize(inputs.plan)
    idempotency_key = inputs.session_key or (
        f"workflow:{ctx.stable_idempotency_key}:{materialized.plan_fingerprint}"
    )

    async def report_progress(done: int, total: int) -> None:
        await ctx.progress(
            f"Completed {done} of {total} assignments",
            fraction=done / total if total else 1.0,
            current=done,
            total=total,
        )

    result = await run_agent_assignment_batch(
        ctx.app,
        inputs,
        source=AssignmentSource(
            kind="workflow",
            execution_id=ctx.app.execution_id,
            workflow_run_id=ctx.run_id,
            workflow_node_id=ctx.node_id,
        ),
        idempotency_key=idempotency_key,
        holder=f"workflow:{ctx.run_id}:{ctx.node_id}:{ctx.attempt}",
        progress=report_progress,
    )
    return success(result)
