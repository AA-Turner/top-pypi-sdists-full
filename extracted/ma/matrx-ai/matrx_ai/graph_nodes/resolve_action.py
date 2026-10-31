"""ai.judge.resolve — pick the best of N gathered arms, or merge them, with reasons.

The pattern it closes (owner, 2026-10-18): run the same JOB on the same input
several ways side by side — single-job agent chains next to one multi-job agent
— gather the arms, then "have the manager agent resolve the best". Fan-out and
fan-in already exist (``control.map`` → arms → ``control.gather``); this is the
step after the gather::

    control.map ─► arm A ─┐
                ─► arm B ─┼─► control.gather ─► ai.judge.resolve
                ─► arm C ─┘

What it is built on — nothing here is a second implementation:

* **The judge is an agent the author picks** (``agent_id``). A workflow step runs an
  agent DIRECTLY (aidream CLAUDE.md, 2026-10-28) — the same run path Run Agent uses
  (``build_agent_request`` → ``run_step_agent``), bound to this node's strict answer
  shape. No agent id and no prompt live in code, there is no default agent and no
  seed fallback: a step with no agent refuses with ``judge_agent_missing`` naming
  the field to set. (Until 2026-10-29 the judge hid behind the code-side mandate
  ``evaluators.arm_resolver``; that key survives only as the ledger identity.)
* **The verdict lands on the judge accuracy ledger** (``platform.judge_verdict``)
  through ``matrx_ai.evaluators.ledger.record_verdict`` — the same row shape the
  Judge and Selector write, in ``comparative`` mode, so "which arm won and why"
  is queryable per workflow run and the agreement bit can be stamped later by a
  human pick (Workflow Battle) exactly like any other judge.
* **Holes are named, never dropped.** ``control.gather`` compacts its values and
  reports every missing dispatch in ``holes`` / ``item_indexes``; this node maps
  each value back to its DISPATCHED index, so arm 2 is still arm 2 when arm 1
  failed, and every missing arm is listed in ``missing_arms`` and shown to the
  judge as missing.

Comparison, not absolute scoring (Judge invariant 2, D-14): the per-arm
assessment is a RANK among the arms present (1 = best), never a 0-100 grade.
"""

from __future__ import annotations

import asyncio
import json
import uuid
from typing import Any, Literal

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from matrx_graph.types.usl import field_extras
from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_ai.graph_nodes._strict_json import StrictJsonError
from matrx_ai.graph_nodes.class_pin import model_class_extras, offering_id_field

NODE_NAME = "ai.judge.resolve"
#: The judge's identity on the accuracy ledger (``platform.judge_verdict.judge_key``).
#: It is the former mandate key, kept so verdicts before and after 2026-10-29 group as
#: one judge — it names a ledger contract, never a mandate the step resolves.
RESOLVER_JUDGE_KEY = "evaluators.arm_resolver"
#: The ledger identity of this judge. Bump on any change to the verdict
#: vocabulary or the meaning of a field — two contracts never share one record.
RESOLVER_JUDGE_VERSION = 1
RESOLVER_VERDICTS: tuple[str, ...] = ("pick", "merge", "none")

ResolveVerdict = Literal["pick", "merge", "none"]


class ArmResolverError(StrictJsonError):
    """The judge answered outside its contract (bad arm, missing merge, …)."""


# ============================================================================
# Shapes
# ============================================================================


class GatheredHole(BaseModel):
    """One ``control.gather`` hole — the arm that produced nothing."""

    model_config = ConfigDict(extra="allow")

    item_index: int
    status: str = "skipped"
    error: dict[str, JsonValue] | None = None


class ResolveArmsInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    job: str = Field(
        min_length=1,
        description="The job every arm was given, in plain words.",
        json_schema_extra=field_extras(widget="textarea", multiline_rows=3),
    )
    criteria: list[str] = Field(
        default_factory=list,
        description="What makes one result better than another, one point per entry.",
    )
    job_input: JsonValue = Field(
        default=None,
        description="The input every arm worked on, when the judge should see it.",
    )
    arms: list[JsonValue] = Field(
        default_factory=list,
        description=(
            "The gathered results, one per arm that succeeded. Wire a gather's "
            "`structured_outputs` or `final_texts` here."
        ),
    )
    item_indexes: list[int] = Field(
        default_factory=list,
        description="Wire the gather's `item_indexes`: which arm each result came from.",
    )
    holes: list[GatheredHole] = Field(
        default_factory=list,
        description="Wire the gather's `holes`: arms that produced nothing.",
    )
    expected: int | None = Field(
        default=None,
        ge=0,
        description="Wire the gather's `expected`: how many arms were run.",
    )
    arm_labels: list[str] = Field(
        default_factory=list,
        description="A short name per arm, in the order the arms were run.",
    )
    allow_merge: bool = Field(
        default=True,
        description="Let the judge combine arms into one merged result.",
    )
    agent_id: str | None = Field(
        default=None,
        description=(
            "The judge agent this step runs. Pick one of your saved agents; it is handed "
            "the job, criteria, job_input, arms, missing_arms, allow_merge and "
            "allowed_verdicts as variables and must answer in this step's verdict shape."
        ),
        json_schema_extra=field_extras(widget="agent_picker"),
    )
    is_version: bool = Field(
        default=False,
        description="Pin to this version: run the exact saved version named above.",
        json_schema_extra=field_extras(widget="toggle"),
    )
    model: str | None = Field(
        default=None,
        description=(
            "Leave empty to run the model the judge agent names; set it only to "
            "override that for this workflow."
        ),
        json_schema_extra=field_extras(widget="model_picker", **model_class_extras()),
    )
    offering_id: str | None = offering_id_field()
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


class ArmAssessment(BaseModel):
    """The judge's view of one present arm. ``rank`` is comparative: 1 = best."""

    model_config = ConfigDict(extra="forbid")

    arm_index: int = Field(description="The arm's run position (0-based).")
    rank: int = Field(ge=1, description="Rank among the arms present; 1 is best.")
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)


class _ResolverLlmOutput(BaseModel):
    """What the judge Holder must answer with (strict JSON)."""

    model_config = ConfigDict(extra="forbid")

    verdict: ResolveVerdict
    winner_arm_index: int | None = Field(
        default=None,
        description="The winning arm's run position when verdict is 'pick'; null otherwise.",
    )
    reasons: list[str] = Field(
        min_length=1, description="Why this verdict, one concrete point per entry."
    )
    confidence: float = Field(ge=0.0, le=1.0)
    arm_assessments: list[ArmAssessment] = Field(default_factory=list)
    merged_result: str | None = Field(
        default=None,
        description=(
            "When verdict is 'merge': the merged result, in the same form as the arms "
            "(JSON text when the arms are objects). Null otherwise."
        ),
    )


class MissingArm(BaseModel):
    model_config = ConfigDict(extra="forbid")

    arm_index: int
    label: str
    status: str = Field(description="'skipped', 'pruned', 'failed', or 'missing'.")
    error: dict[str, JsonValue] | None = None


class ArmResolution(BaseModel):
    """Output of ``ai.judge.resolve`` (kind ``arm_resolution``)."""

    model_config = ConfigDict(extra="forbid")

    verdict: ResolveVerdict
    winner_arm_index: int | None = None
    winner_label: str = ""
    winner_result: JsonValue = Field(
        default=None, description="The winning arm's result when verdict is 'pick'."
    )
    merged_result: JsonValue = Field(
        default=None, description="The merged result when verdict is 'merge'."
    )
    reasons: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    arm_assessments: list[ArmAssessment] = Field(default_factory=list)
    missing_arms: list[MissingArm] = Field(default_factory=list)
    arm_count: int = Field(default=0, description="How many arms were run.")
    judged_count: int = Field(default=0, description="How many arms the judge saw.")
    ledger_id: str | None = Field(
        default=None,
        description="The platform.judge_verdict row recording this verdict.",
    )


# ============================================================================
# Pure helpers
# ============================================================================


def _label(labels: list[str], index: int) -> str:
    if 0 <= index < len(labels) and labels[index].strip():
        return labels[index].strip()
    return f"Arm {index + 1}"


def lay_out_arms(
    inputs: ResolveArmsInput,
) -> tuple[list[dict[str, Any]], list[MissingArm], int]:
    """Map every gathered value back to its DISPATCHED arm and name every gap.

    Returns ``(present, missing, arm_count)``. ``present`` entries carry
    ``arm_index`` / ``label`` / ``result``. A hole never shifts what a value
    pairs with, and an arm that produced nothing is never silently dropped.
    """
    if inputs.item_indexes and len(inputs.item_indexes) != len(inputs.arms):
        raise ArmResolverError(
            f"{NODE_NAME}: `item_indexes` has {len(inputs.item_indexes)} entries but "
            f"`arms` has {len(inputs.arms)} — wire both from the same gather."
        )
    indexes = list(inputs.item_indexes) or list(range(len(inputs.arms)))
    if len(set(indexes)) != len(indexes):
        raise ArmResolverError(f"{NODE_NAME}: `item_indexes` repeats an arm: {indexes}")
    hole_by_index = {h.item_index: h for h in inputs.holes}
    candidates = [len(inputs.arm_labels), len(inputs.arms)]
    if inputs.expected is not None:
        candidates.append(inputs.expected)
    if indexes:
        candidates.append(max(indexes) + 1)
    if hole_by_index:
        candidates.append(max(hole_by_index) + 1)
    arm_count = max(candidates)

    present: list[dict[str, Any]] = []
    by_index = dict(zip(indexes, inputs.arms, strict=True))
    missing: list[MissingArm] = []
    for index in range(arm_count):
        label = _label(inputs.arm_labels, index)
        if index in by_index and by_index[index] is not None:
            present.append({"arm_index": index, "label": label, "result": by_index[index]})
            continue
        hole = hole_by_index.get(index)
        missing.append(
            MissingArm(
                arm_index=index,
                label=label,
                status=(hole.status if hole else "missing"),
                error=(hole.error if hole else None),
            )
        )
    return present, missing, arm_count


def _check_answer(
    answer: _ResolverLlmOutput, present: list[dict[str, Any]], *, allow_merge: bool
) -> None:
    """The contract owns the vocabulary — out-of-contract answers RAISE, never coerce."""
    present_indexes = {arm["arm_index"] for arm in present}
    if answer.verdict == "pick":
        if answer.winner_arm_index not in present_indexes:
            raise ArmResolverError(
                f"{NODE_NAME}: the judge picked arm {answer.winner_arm_index!r}, which is not "
                f"one of the arms it was shown {sorted(present_indexes)}."
            )
    elif answer.verdict == "merge":
        if not allow_merge:
            raise ArmResolverError(f"{NODE_NAME}: the judge merged, but this step forbids merging.")
        if not (answer.merged_result or "").strip():
            raise ArmResolverError(f"{NODE_NAME}: the judge said 'merge' but gave no merged result.")
    elif answer.winner_arm_index is not None:
        raise ArmResolverError(f"{NODE_NAME}: verdict 'none' may not name a winner.")
    for assessment in answer.arm_assessments:
        if assessment.arm_index not in present_indexes:
            raise ArmResolverError(
                f"{NODE_NAME}: the judge assessed arm {assessment.arm_index}, which it was not shown."
            )


def _merged_value(text: str | None, present: list[dict[str, Any]]) -> JsonValue:
    """Merged text back into the arms' form: JSON when the arms are structured."""
    if text is None:
        return None
    if any(isinstance(arm["result"], dict | list) for arm in present):
        try:
            return json.loads(text)
        except ValueError:
            return text
    return text


def _uuid_or_none(value: str | None) -> str | None:
    try:
        return str(uuid.UUID(str(value))) if value else None
    except ValueError:
        return None


async def _record(
    ctx: NodeExecutionContext | None,
    inputs: ResolveArmsInput,
    *,
    answer: _ResolverLlmOutput,
    present: list[dict[str, Any]],
    missing: list[MissingArm],
    agent_id: str,
    model: str | None,
) -> str | None:
    """One ``platform.judge_verdict`` row per verdict, linked to the workflow run."""
    from matrx_ai.evaluators.judge import EntityRef, JudgeContract, JudgeOutcome, JudgeSubject
    from matrx_ai.evaluators.ledger import record_verdict

    app = getattr(ctx, "app", None)
    run_id = getattr(ctx, "run_id", None)
    rubric = "\n".join(c.strip() for c in inputs.criteria if c.strip()) or None
    contract = JudgeContract(
        key=RESOLVER_JUDGE_KEY,
        version=RESOLVER_JUDGE_VERSION,
        question=(
            "Of these results of the same job on the same input, which is best — "
            "or should they be merged, or is none good enough?"
        ),
        mode="comparative",
        subject_kind="workflow_arms",
        verdict_values=RESOLVER_VERDICTS,
        rubric_name="workflow criteria" if rubric else None,
        rubric=rubric,
        rubric_provenance="H",
        model=model,
        consumer=NODE_NAME,
    )
    ranks = {a.arm_index: a.rank for a in answer.arm_assessments}
    candidate_refs: list[dict[str, Any]] = [
        {
            "arm_index": arm["arm_index"],
            "label": arm["label"],
            "present": True,
            "rank": ranks.get(arm["arm_index"]),
            "winner": answer.verdict == "pick" and answer.winner_arm_index == arm["arm_index"],
        }
        for arm in present
    ] + [
        {"arm_index": m.arm_index, "label": m.label, "present": False, "status": m.status}
        for m in missing
    ]
    candidate_refs.sort(key=lambda ref: ref["arm_index"])
    winner_label = next(
        (arm["label"] for arm in present if arm["arm_index"] == answer.winner_arm_index), ""
    )
    subject = JudgeSubject(
        label=winner_label or answer.verdict,
        ref=EntityRef(ref_type="workflow_run", ref_id=_uuid_or_none(run_id)),
    )
    outcome = JudgeOutcome(
        verdict=answer.verdict,
        confidence=answer.confidence,
        reasoning="\n".join(answer.reasons),
        evidence=list(answer.reasons),
        judge_key=contract.key,
        judge_version=contract.version,
        mode=contract.mode,
    )
    invocation = {
        "model": model,
        "workflow_run_id": run_id,
        "thread_id": getattr(ctx, "thread_id", None),
        "node_id": getattr(ctx, "node_id", None),
        "step": getattr(ctx, "step", None),
        "winner_arm_index": answer.winner_arm_index,
        "arm_count": len(present) + len(missing),
        "judge_agent_id": agent_id,
    }
    return await record_verdict(
        contract=contract,
        subject=subject,
        reference=None,
        outcome=outcome,
        invocation=invocation,
        organization_id=getattr(app, "organization_id", None),
        user_id=_uuid_or_none(getattr(app, "user_id", None)),
        candidate_refs=candidate_refs,
    )


def judge_variables(
    inputs: ResolveArmsInput, present: list[dict[str, Any]], missing: list[MissingArm]
) -> dict[str, Any]:
    """The values the judge agent is handed, by name (its declared ``{{name}}`` variables)."""
    return {
        "job": inputs.job,
        "criteria": list(inputs.criteria),
        "job_input": inputs.job_input,
        "arms": present,
        "missing_arms": [m.model_dump(mode="json") for m in missing],
        "allow_merge": inputs.allow_merge,
        "allowed_verdicts": ", ".join(
            v for v in RESOLVER_VERDICTS if inputs.allow_merge or v != "merge"
        ),
    }


async def _run_judge_agent(
    ctx: NodeExecutionContext,
    inputs: ResolveArmsInput,
    present: list[dict[str, Any]],
    missing: list[MissingArm],
) -> tuple[_ResolverLlmOutput, str | None] | NodeResult[Any]:
    """Run the author's judge agent DIRECTLY — Run Agent's own path, bound to the verdict shape."""
    from matrx_ai.config.response_format import response_format_for_model
    from matrx_ai.graph_nodes.agent_action import (
        AgentStartInput,
        build_agent_request,
        require_agent_host,
        resolve_step_agent_full,
        run_step_agent,
    )
    from matrx_ai.graph_nodes.shared import AiExecutionResult, normalize_completed_result

    require_agent_host(NODE_NAME)
    node_id = getattr(ctx, "node_id", None) or "?"
    overrides: dict[str, Any] = {}
    if inputs.model:
        overrides["model"] = inputs.model
        if inputs.offering_id:
            overrides["offering_id"] = inputs.offering_id
    step = AgentStartInput(
        agent_id=inputs.agent_id,
        is_version=inputs.is_version,
        variables=judge_variables(inputs, present, missing),
        config_overrides=overrides or None,
        max_output_tokens=4096,
    )
    resolved = await resolve_step_agent_full(step, consumer=f"{NODE_NAME}:{node_id}")
    request = build_agent_request(
        ctx,
        step,
        resolved,
        node_type=NODE_NAME,
        top_config_overrides={
            "response_format": response_format_for_model(_ResolverLlmOutput).model_dump(
                mode="json", by_alias=True, exclude_none=True
            )
        },
    )
    completed = await run_step_agent(ctx, resolved.agent_id, request)
    if isinstance(completed, AiExecutionResult):
        normalized = completed
    else:
        outcome = await asyncio.to_thread(normalize_completed_result, completed)
        if outcome.status == "error":
            # The failed paid turn already carries its billed usage — hand it on as itself.
            return outcome  # type: ignore[return-value]
        normalized = outcome.result
    payload = normalized.structured_output
    if not isinstance(payload, dict):
        raise ArmResolverError(
            f"{NODE_NAME}: the judge agent answered without a verdict object.",
            raw_output=(normalized.final_text or "")[:2000],
        )
    try:
        answer = _ResolverLlmOutput.model_validate(
            {k: v for k, v in payload.items() if k != "__kind"}
        )
    except ValueError as exc:
        raise ArmResolverError(
            f"{NODE_NAME}: the judge agent's verdict is outside the contract: {exc}",
            raw_output=json.dumps(payload, default=str)[:2000],
        ) from exc
    model_id = (normalized.metadata or {}).get("model_id") or inputs.model
    return answer, (str(model_id) if model_id else None)


# ============================================================================
# The node
# ============================================================================


@register_node(
    name=NODE_NAME,
    display_name="Pick the Best Result",
    description="Have AI pick the best of several results, or merge them, with reasons.",
    category=NodeCategory.LLM,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=ResolveArmsInput,
    output_schema=ArmResolution,
    output_kind="arm_resolution",
    icon="trophy",
    tags=("ai", "judge", "resolve", "compare", "fan-in"),
)
async def resolve_arms(
    ctx: NodeExecutionContext, inputs: ResolveArmsInput
) -> NodeResult[ArmResolution]:
    present, missing, arm_count = lay_out_arms(inputs)
    if not present:
        # Nothing to judge is an answer, not a paid call — and never a silent pass.
        return success(
            ArmResolution(
                verdict="none",
                reasons=["No arm produced a result."],
                missing_arms=missing,
                arm_count=arm_count,
            )
        )

    if not (inputs.agent_id or "").strip():
        return failure(
            "judge_agent_missing",
            f"{NODE_NAME}: no judge agent is set on this step. Pick the agent that judges "
            "the arms in the step's 'agent_id' field (an agent you can open and edit); "
            "nothing runs until one is chosen.",
            details={"field": "agent_id"},
        )
    ran = await _run_judge_agent(ctx, inputs, present, missing)
    if not isinstance(ran, tuple):
        return ran  # the judge's failed turn, as itself
    answer, model_id = ran
    _check_answer(answer, present, allow_merge=inputs.allow_merge)

    ledger_id = await _record(
        ctx,
        inputs,
        answer=answer,
        present=present,
        missing=missing,
        agent_id=str(inputs.agent_id),
        model=model_id,
    )
    if ledger_id is None and ctx is not None and hasattr(ctx, "warn"):
        await ctx.warn(
            "verdict not recorded",
            "The verdict stands, but its judge-ledger row was not written.",
        )

    winner = next((a for a in present if a["arm_index"] == answer.winner_arm_index), None)
    return success(
        ArmResolution(
            verdict=answer.verdict,
            winner_arm_index=answer.winner_arm_index if answer.verdict == "pick" else None,
            winner_label=winner["label"] if winner and answer.verdict == "pick" else "",
            winner_result=winner["result"] if winner and answer.verdict == "pick" else None,
            merged_result=(
                _merged_value(answer.merged_result, present) if answer.verdict == "merge" else None
            ),
            reasons=list(answer.reasons),
            confidence=answer.confidence,
            arm_assessments=sorted(answer.arm_assessments, key=lambda a: a.rank),
            missing_arms=missing,
            arm_count=arm_count,
            judged_count=len(present),
            ledger_id=ledger_id,
        )
    )


__all__ = [
    "RESOLVER_JUDGE_KEY",
    "ArmAssessment",
    "ArmResolution",
    "ArmResolverError",
    "MissingArm",
    "ResolveArmsInput",
    "judge_variables",
    "lay_out_arms",
    "resolve_arms",
]
