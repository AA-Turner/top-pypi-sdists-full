"""``ai.agent.produce`` — run an agent BOUND to the kind it must answer in.

The one-line difference from ``ai.agent.start``: this node's output IS the
platform kind the step declares, already validated, instead of the run
ENVELOPE with the answer buried inside ``final_text`` as a JSON string.

Why it exists (Arman's ruling, 2026-08-20)
------------------------------------------
Measured on live Study Pack run ``fedd6591-bec8-4813-98a3-91ec884698dc``: the
notes step's ``output_kind`` was ``agent_result`` (usage, messages, metadata),
``structured_output`` was **null**, and the kind-shaped data sat in
``final_text`` as a string. Getting from there to something renderable took
FOUR hops — agent → ``ai.util.parse_llm_json`` → ``data.map_template`` →
``data.transform`` — and the kind was LOST at the agent boundary and hand-
reconstructed downstream by seven projection nodes. Every one of those nodes
was a workaround for an agent that never saw its own declaration.

So the declaration is handed to the agent. The node reads the kind slug the
graph declared for it (``data.output_kind``, surfaced as
:attr:`NodeExecutionContext.output_kind`), turns it into a strict, provider-
portable ``response_format`` through the ONE binder
(``matrx_ai.kinds.response_format_for_kind``), and returns the model's parsed,
schema-validated answer as the node payload. The scheduler then validates that
payload against the SAME kind and stamps it on the outcome row — so
``output_kind`` / ``output_kind_ok`` describe the actual answer, and any
surface that renders the kind can render the step with no projection lane.

What this node refuses to do
----------------------------
* Run without a declared kind. A step whose whole contract is "produce X" and
  that never says which X is not a step, it is a guess.
* Run against an unbindable kind. An unenforceable ``response_format``
  degrades silently to prose, which is worse than no binding at all.
* Run when the graph's declaration and the MANDATE's declared ``output_kind``
  disagree. Two declarations about what a paid run produces cannot both be
  true, and picking one on the executor's own authority is how drift becomes
  invisible.
* Let an authored ``config_overrides`` unbind the kind — the binding is
  layered ABOVE every author/binding/run-scope layer (see
  ``build_agent_request``'s ``top_config_overrides``).

Everything else — mandate resolution, conversation gating, tools, context,
variables, streaming, cost — is the SAME code ``ai.agent.start`` runs. This is
not a second way to run an agent; it is the same way, with the declaration
carried through instead of dropped.
"""

from __future__ import annotations

import logging
from typing import Any

from matrx_graph.actions import register_node
from matrx_graph.errors import ExecutionError
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import RESERVED_PAYLOAD_FIELDS, NodeResult, failure, success
from pydantic import BaseModel, ConfigDict

from matrx_ai.graph_nodes.agent_action import (
    AgentStartConfig,
    AgentStartInput,
    build_agent_request,
    require_agent_host,
    resolve_step_agent_full,
    run_step_agent,
)
from matrx_ai.graph_nodes.shared import AiExecutionResult, normalize_completed_result
from matrx_ai.kinds import is_bindable_kind, response_format_for_kind

logger = logging.getLogger(__name__)

_NODE_TYPE = "ai.agent.produce"


class AgentProduceInput(AgentStartInput):
    """Identical to ``ai.agent.start``'s input — same agent, same contract.

    Deliberately a subclass and not a trimmed copy: everything the API supports
    the workflow supports, by construction. The kind is NOT an input field — it
    is the node instance's ``data.output_kind`` declaration, the same value the
    scheduler validates the result against. A second place to say it would be a
    second thing that can disagree.
    """


class AgentProducedOutput(BaseModel):
    """The kind's own payload, verbatim — this node's output IS the answer.

    Permissive by construction (``extra="allow"``, no declared fields): the
    real shape is the declared kind's ``emitted_json_schema``, which the
    provider was bound to and the scheduler checks against. Same pattern
    ``io.user_input`` uses for author-defined fields — the pydantic class is
    the transport, the kind is the contract.
    """

    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "x-contract-dynamic": (
                "the node instance's declared output_kind is the real schema; "
                "the model is bound to it via response_format"
            )
        },
    )


def _declared_kind(ctx: NodeExecutionContext) -> str:
    kind = (getattr(ctx, "output_kind", None) or "").strip()
    if not kind:
        raise ExecutionError(
            f"{_NODE_TYPE} step '{getattr(ctx, 'node_id', '?')}' declares no output "
            "kind. This node exists to make an agent answer IN a registered "
            "platform kind, so the kind is not optional: set the node's "
            "`output_kind` (data.output_kind) to the kind slug this step "
            "produces — e.g. 'flashcard_set'. For a free-text or free-JSON "
            "agent step, use ai.agent.start instead."
        )
    if not is_bindable_kind(kind):
        raise ExecutionError(
            f"{_NODE_TYPE} step '{getattr(ctx, 'node_id', '?')}' declares "
            f"output kind '{kind}', which names a FORMAT, not a structure — "
            "there is nothing to bind the model to. Declare a registered "
            "structural kind, or use ai.agent.start for free-form output."
        )
    return kind


def _assert_declarations_agree(ctx: NodeExecutionContext, kind: str, mandate_kind: str | None) -> None:
    """The graph's declaration and the Mandate's must be the same kind.

    A mandate that declares nothing structural (``text`` / ``json`` / unset, or
    a step pinned to a bare ``agent_id``) is not a contradiction — it is a job
    that never stated what it answers in, and the graph's declaration stands.
    Say so once, at warning level, because a mandate SHOULD carry that truth:
    every other consumer of the job (a client run, a bench run) reads the
    mandate, not this graph.
    """
    if mandate_kind is None or not is_bindable_kind(mandate_kind):
        logger.warning(
            "%s step '%s' declares output kind '%s', but its mandate declares "
            "%r — the mandate is the platform-wide statement of what this JOB "
            "answers in, so set its output_kind to '%s' too (declare_mandate("
            "output_kind=...)).",
            _NODE_TYPE,
            getattr(ctx, "node_id", "?"),
            kind,
            mandate_kind,
            kind,
        )
        return
    if mandate_kind != kind:
        raise ExecutionError(
            f"{_NODE_TYPE} step '{getattr(ctx, 'node_id', '?')}' declares output "
            f"kind '{kind}', but the mandate it runs declares '{mandate_kind}'. "
            "Both claim to describe what this paid run produces and they cannot "
            "both be right. Fix whichever one is wrong — the mandate's "
            "declare_mandate(output_kind=...) or the node's data.output_kind — "
            "before this step runs again."
        )


async def _response_format_for(ctx: NodeExecutionContext, kind: str) -> dict[str, Any]:
    bound = await response_format_for_kind(kind)
    if bound is None:
        # response_format_for_kind already logged WHY (unregistered slug, no
        # schema, or a schema the portability gate cannot make strict).
        raise ExecutionError(
            f"{_NODE_TYPE} step '{getattr(ctx, 'node_id', '?')}' could not bind "
            f"kind '{kind}' to a strict response_format, so the agent would "
            "answer in whatever shape it felt like and this step's declaration "
            "would be a lie. Fix the kind's emitted_json_schema (the binder "
            "logged the findings) — this step does not run unbound."
        )
    return bound.model_dump(mode="json", by_alias=True, exclude_none=True)


def _record_spend(ctx: NodeExecutionContext, normalized: AiExecutionResult) -> None:
    """Declare this invocation's billed usage on the engine plane.

    This node's payload is a platform kind — strict, additionalProperties:
    false — so there is nowhere in it to carry a usage block, and the
    scheduler's payload sniffing would silently lose the cost tick. Declaring
    it is the correct channel, not a workaround: what a run SPENT was never a
    property of what it RETURNED.
    """
    ctx.record_billed_usage(
        normalized.usage.model_dump(mode="json"),
        conversation_id=normalized.conversation_id or None,
        request_id=normalized.request_id or None,
    )


@register_node(
    name=_NODE_TYPE,
    display_name="Agent → Typed Result",
    description=(
        "Run one of your saved agents and get back a real, checked result of "
        "the kind this step declares — ready to render, no parsing step."
    ),
    category=NodeCategory.AGENT,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=AgentProduceInput,
    output_schema=AgentProducedOutput,
    # No spec-level kind: the kind is per node INSTANCE (data.output_kind), and
    # dynamic_output keeps the registry from minting a fingerprint contract
    # kind that would read as "this node declares a kind" while describing
    # nothing anyone can render.
    output_kind=None,
    dynamic_output=True,
    config_schema=AgentStartConfig,
    icon="bot",
    tags=("ai", "agent", "llm", "kinds"),
)
async def agent_produce(
    ctx: NodeExecutionContext, inputs: AgentProduceInput
) -> NodeResult[AgentProducedOutput]:
    require_agent_host(_NODE_TYPE)
    node_id = getattr(ctx, "node_id", None) or "?"
    kind = _declared_kind(ctx)

    resolved = await resolve_step_agent_full(inputs, consumer=f"{_NODE_TYPE}:{node_id}")
    _assert_declarations_agree(ctx, kind, resolved.declared_output_kind)

    request = build_agent_request(
        ctx,
        inputs,
        resolved,
        node_type=_NODE_TYPE,
        # ABOVE every other layer: the declaration is this node's contract, and
        # an authored config_overrides must never be able to unbind it.
        top_config_overrides={"response_format": await _response_format_for(ctx, kind)},
    )
    completed = await run_step_agent(ctx, resolved.agent_id, request)

    # A host agent_runner may hand back an already-normalized result (a
    # compiled Orchestra whose final step IS the agent result).
    if isinstance(completed, AiExecutionResult):
        outcome: NodeResult[AiExecutionResult] = success(completed)
    else:
        outcome = normalize_completed_result(completed)
    if outcome.status == "error":
        # A failed paid turn already carries its billed usage in
        # error.details['usage'] — the scheduler settles cost from there.
        return outcome  # type: ignore[return-value]

    normalized = outcome.result
    _record_spend(ctx, normalized)

    payload = normalized.structured_output
    if not isinstance(payload, dict):
        return failure(
            "kind_output_missing",
            (
                f"The agent was bound to answer in '{kind}' but returned "
                f"{'a list' if isinstance(payload, list) else 'no structured result'}. "
                "A kind-bound step has nothing to hand downstream without one."
            ),
            details={
                "declared_kind": kind,
                "usage": normalized.usage.model_dump(mode="json"),
                "conversation_id": normalized.conversation_id,
                "request_id": normalized.request_id,
                "final_text_preview": normalized.final_text[:400],
            },
        )
    collisions = sorted(RESERVED_PAYLOAD_FIELDS & payload.keys())
    if collisions:
        return failure(
            "kind_output_reserved_field",
            (
                f"Kind '{kind}' carries top-level field(s) {collisions}, which the "
                "node-result envelope reserves — a payload cannot own a key that "
                "means 'this node failed'. Rename the field in the kind."
            ),
            details={"declared_kind": kind, "fields": collisions},
        )
    return success(AgentProducedOutput.model_validate(payload))
