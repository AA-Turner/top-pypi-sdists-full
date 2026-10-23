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

* **The judge is a mandate** (:data:`ARM_RESOLVER_MANDATE`). The node holds the
  call through ``hold_code_call`` and runs on the Holder's model and prompt;
  no agent id and no prompt live in code. An unbound mandate refuses with a
  ``judge_unbound`` failure naming the key and where to bind it.
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

import json
import uuid
from typing import Any, Literal

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from matrx_graph.types.usl import field_extras
from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_ai.code_call_mandate_keys import ARM_RESOLVER_MANDATE
from matrx_ai.graph_nodes._strict_json import StrictJsonError, node_panel_hooks
from matrx_ai.graph_nodes.class_pin import model_class_extras, offering_id_field
from matrx_ai.mandates import (
    MandateResolutionUnavailable,
    Offer,
    RunOptions,
    carried_principal,
    get_mandate_runner,
)
from matrx_ai.orchestrator.mandate_carrier import MANDATE_HOLDER_METADATA_KEY

NODE_NAME = "ai.judge.resolve"
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
    model: str | None = Field(
        default=None,
        description=(
            "Leave empty to run the model this step's mandate Holder names; set it only to "
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
    held_metadata: dict[str, Any],
    model: str | None,
) -> str | None:
    """One ``platform.judge_verdict`` row per verdict, linked to the workflow run."""
    from matrx_ai.evaluators.judge import EntityRef, JudgeContract, JudgeOutcome, JudgeSubject
    from matrx_ai.evaluators.ledger import record_verdict

    app = getattr(ctx, "app", None)
    run_id = getattr(ctx, "run_id", None)
    rubric = "\n".join(c.strip() for c in inputs.criteria if c.strip()) or None
    contract = JudgeContract(
        key=ARM_RESOLVER_MANDATE,
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
        mandate=ARM_RESOLVER_MANDATE,
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
        "mandate_holder": held_metadata.get(MANDATE_HOLDER_METADATA_KEY),
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

    on_delta, on_reset = node_panel_hooks(getattr(getattr(ctx, "app", None), "emitter", None))
    try:
        held = (
            await get_mandate_runner().prepare(
                ARM_RESOLVER_MANDATE,
                Offer.given_values(
                    {
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
                ),
                who=carried_principal(),
                opts=RunOptions(door="package_code_call", consumer=NODE_NAME),
            )
        ).held_call()
    except MandateResolutionUnavailable as exc:
        return failure(
            "judge_unbound",
            f"No judge is bound to this step yet. Bind an agent to the mandate "
            f"'{ARM_RESOLVER_MANDATE}' at /mandates/{ARM_RESOLVER_MANDATE}.",
            details={"mandate_key": ARM_RESOLVER_MANDATE, "reason": exc.reason},
        )

    answer = await held.send_pydantic(
        user=held.authored_user(),
        output_cls=_ResolverLlmOutput,
        model=inputs.model,
        offering_id=inputs.offering_id,
        unset_max_tokens=4096,
        metadata=dict(inputs.metadata),
        on_delta=on_delta,
        on_reset=on_reset,
    )
    _check_answer(answer, present, allow_merge=inputs.allow_merge)

    ledger_id = await _record(
        ctx,
        inputs,
        answer=answer,
        present=present,
        missing=missing,
        held_metadata=held.metadata,
        model=held.pick_model(inputs.model),
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
    "ARM_RESOLVER_MANDATE",
    "ArmAssessment",
    "ArmResolution",
    "ArmResolverError",
    "MissingArm",
    "ResolveArmsInput",
    "lay_out_arms",
    "resolve_arms",
]
