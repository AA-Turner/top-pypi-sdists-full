"""``ai.conversation.revise`` — "Check and Revise".

Placed in line after any agent or mandate step: checks the answer and, on a
miss, sends ONE host-authored turn into the SAME conversation with the check
report as a context entry, re-checks, and stops at a bound. A thin transport
over :func:`matrx_ai.revision.revise_until_passing` — the podcast code path
calls the same function (design DESIGN.md §5; owner rulings 2026-10-07).

* ``max_revisions = 0`` means check only. Blank → knob
  ``workflow.response_checks.max_revisions`` (start 1), clamped to the knob
  ``max_revisions_ceiling`` (start 4).
* ``conversation_id`` is an IDENTITY input: read only from the mapped value,
  never from a broadcast — the step must never append to someone else's thread.
* A miss writes ONE warning per invocation through ``ctx.warn`` (never one per
  attempt). A warning never fails the run; only a strict check
  (``on_exhausted: fail``) whose tries are used up fails the step,
  ``response_check_failed``.
* The per-run revision budget is read from DURABLE rows (``workflow.run_log``).
"""

from __future__ import annotations

from matrx_graph.actions import register_node
from matrx_graph.checks import ResponseCheckSpec
from matrx_graph.content_ir.model import KindModel
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.identity_inputs import identity_input
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from matrx_graph.types.usl import field_extras
from pydantic import BaseModel, ConfigDict, Field, JsonValue


class ConversationReviseInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    answer: str = Field(
        default="",
        description="The answer to check — usually the upstream step's final_text.",
        json_schema_extra=field_extras(widget="textarea", multiline_rows=3),
    )
    conversation_id: str | None = Field(
        default=None,
        description=(
            "The conversation that produced the answer. Revisions are sent into it. "
            "Blank: the answer is checked, and a miss cannot be revised."
        ),
        json_schema_extra={**field_extras(widget="text"), **identity_input()},
    )
    request_id: str | None = Field(default=None, description="The request that produced the answer.")
    values: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="Targets the checks read by name, e.g. target_word_count, host_count.",
        json_schema_extra=field_extras(widget="json"),
    )
    checks: list[ResponseCheckSpec] = Field(
        default_factory=list,
        description="What to check. v1 types: 'length' and 'host'.",
        json_schema_extra=field_extras(widget="json"),
    )
    max_revisions: int | None = Field(
        default=None,
        ge=0,
        le=10,
        description="How many revision turns at most. 0 = check only. Blank = the platform default.",
    )


class ConversationReviseOutput(KindModel, kind="response_check_revision"):
    """The step's result — registered kind ``response_check_revision`` (published by
    the host, aidream ``aidream/kinds/response_checks.py``)."""

    conversation_id: str = Field(default="", description="The conversation that was checked.")
    request_id: str | None = Field(default=None, description="The request behind the final text.")
    final_text: str = Field(default="", description="The answer that flows on.")
    outcome: str = Field(
        description="passed, revised, off_target, not_revisable or failed.",
    )
    reason: str = Field(default="", description="Why it was not revised, when it was not.")
    check: dict[str, JsonValue] = Field(
        default_factory=dict, description="The final answer's check report."
    )
    attempts: list[dict[str, JsonValue]] = Field(
        default_factory=list, description="One summary per attempt, first answer included."
    )
    revision_turns: int = Field(default=0, description="Revision turns sent.")
    revision_cost_usd: float = Field(default=0.0, description="What the revision turns cost.")


def _key_base(ctx: NodeExecutionContext) -> str:
    # (run, node, dispatch, item) — attempt and step are deliberately OUT: an
    # engine retry or a resumed step must find the turns the first try paid for.
    return f"{ctx.run_id}:{ctx.node_id}:{ctx.dispatch_id or 'root'}:{ctx.item_index}"


@register_node(
    name="ai.conversation.revise",
    display_name="Check and Revise",
    description=(
        "Check an answer against targets; on a miss, ask the same conversation to revise it."
    ),
    category=NodeCategory.AGENT,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=ConversationReviseInput,
    output_schema=ConversationReviseOutput,
    output_kind="response_check_revision",
    icon="list-checks",
    tags=("ai", "conversation", "checks", "revision"),
)
async def conversation_revise(
    ctx: NodeExecutionContext, inputs: ConversationReviseInput
) -> NodeResult[ConversationReviseOutput]:
    from matrx_graph.knobs import response_check_policy
    from matrx_graph.run_log import run_revision_turns

    from matrx_ai._ext import get_ext, has_ext
    from matrx_ai.graph_nodes.conversation_action import run_step_conversation_continue
    from matrx_ai.revision import (
        agent_revision_request,
        host_continue_sender,
        persisted_turns,
        revise_until_passing,
    )

    policy = await response_check_policy()
    wanted = policy.max_revisions if inputs.max_revisions is None else inputs.max_revisions
    max_revisions = max(0, min(wanted, policy.max_revisions_ceiling))

    budget_left: int | None = None
    if max_revisions > 0:
        try:
            budget_left = max(0, policy.max_revisions_per_run - await run_revision_turns(ctx.run_id))
        except Exception as exc:  # noqa: BLE001 — unreadable budget = do not spend
            budget_left = 0
            await ctx.warn(
                "response_check.run_budget_reached",
                f"Could not read this run's revision count ({type(exc).__name__}); not revising.",
            )

    revisable = has_ext("conversation_continuer") and has_ext("ConversationContinueRequest")

    def build(payload: dict) -> object:
        return get_ext("ConversationContinueRequest").model_validate(payload)

    async def run(conversation_id: str, request: object) -> object:
        return await run_step_conversation_continue(ctx, conversation_id, request)

    async def on_attempt(n: int, total: int) -> None:
        await ctx.progress(f"Revision {n} of {total}", current=n, total=total)

    result = await revise_until_passing(
        conversation_id=inputs.conversation_id,
        answer=inputs.answer,
        checks=inputs.checks,
        values=inputs.values,
        max_revisions=max_revisions,
        key_base=_key_base(ctx),
        send_turn=host_continue_sender(build_request=build, run=run),
        read_turns=persisted_turns,
        resolve_request=agent_revision_request,
        tolerance_pct=policy.length_tolerance_pct,
        revisable=revisable,
        not_revisable_reason="" if revisable else "the host registered no conversation continuer",
        run_budget_left=budget_left,
        request_id=inputs.request_id,
        on_attempt=on_attempt,
    )

    if result.final_result is not None:
        ctx.record_billed_usage(
            {"cost_usd": result.revision_cost_usd},
            conversation_id=inputs.conversation_id,
            request_id=result.final.request_id,
        )

    label = result.warning_label()
    if label is not None:
        # A revision is a redo the first answer should not have needed — a review flag
        # on the workflow (0117), not just a warning.
        await ctx.flag_for_review(
            label,
            _sentence(result),
            category="rework" if result.outcome == "revised" else "validation_failed",
            payload=result.payload(),
        )
    if budget_left == 0 and max_revisions > 0 and result.outcome not in ("passed", "revised"):
        await ctx.warn(
            "response_check.run_budget_reached",
            f"This run already used its {policy.max_revisions_per_run} revision turns.",
        )

    out = ConversationReviseOutput(
        conversation_id=inputs.conversation_id or "",
        request_id=result.final.request_id,
        final_text=result.final.text,
        outcome=result.outcome,
        reason=result.reason,
        check=result.final.check.model_dump(mode="json"),
        attempts=[a.summary() for a in result.attempts],
        revision_turns=result.revision_turns,
        revision_cost_usd=result.revision_cost_usd,
    )
    if result.outcome == "failed":
        return failure(
            "response_check_failed",
            _sentence(result),
            details={"revision": out.model_dump(mode="json")},
        )
    return success(out)


def _sentence(result) -> str:  # noqa: ANN001 — RevisionOutcome
    facts = "; ".join(m.detail.rstrip(".") for m in result.final.check.misses()) or "all checks passed"
    turns = result.revision_turns
    if result.outcome == "revised":
        return f"Passed after {turns} revision(s). Before: {_first_facts(result)}"
    if result.outcome == "not_revisable":
        return f"{facts}. Not revised: {result.reason}."
    return f"{facts} — after {turns} revision(s)."


def _first_facts(result) -> str:  # noqa: ANN001
    return "; ".join(m.detail.rstrip(".") for m in result.attempts[0].check.misses()) + "."
