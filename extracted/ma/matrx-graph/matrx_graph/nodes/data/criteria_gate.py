from __future__ import annotations

from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success


CriterionVerdict = Literal["met", "not_met", "unknown", "not_applicable"]


class CriterionDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    criterion_id: str = Field(
        min_length=1,
        description="Stable unique id of this criterion; assessments and contradictions reference it.",
    )
    label: str = Field(
        min_length=1,
        description="Human-readable name of the criterion, shown in the gate's coverage report.",
    )
    required: bool = Field(
        default=True,
        description="True = this criterion can block completion; false = tracked but advisory only.",
    )
    evidence_required: bool = Field(
        default=True,
        description="True = the assessment must cite at least one evidence reference or the gate blocks.",
    )
    allow_not_applicable: bool = Field(
        default=False,
        description="Permit a 'not_applicable' verdict on a required criterion without blocking.",
    )


class CriterionAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    criterion_id: str = Field(
        min_length=1,
        description="Id of the declared criterion this assessment answers (must match config.criteria).",
    )
    verdict: CriterionVerdict = Field(
        description="The evaluator's finding: 'met', 'not_met', 'unknown', or 'not_applicable'."
    )
    evidence_refs: list[str] = Field(
        default_factory=list,
        description="Ids of the evidence items supporting this verdict; each must appear in available_evidence_refs.",
    )
    rationale: str = Field(
        min_length=1,
        description="Plain-language explanation of why the evaluator reached this verdict.",
    )
    evaluator_id: str = Field(
        min_length=1,
        description="Id of the evaluator (agent or lane) that produced this assessment.",
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Evaluator's confidence in the verdict, 0.0 (guess) to 1.0 (certain).",
    )


class MaterialContradiction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contradiction_id: str = Field(
        min_length=1, description="Stable unique id of this contradiction record."
    )
    criterion_ids: list[str] = Field(
        min_length=1,
        description="Declared criteria whose evidence or verdicts conflict (at least one).",
    )
    evidence_refs: list[str] = Field(
        min_length=1,
        description="Evidence items on both sides of the conflict; each must appear in available_evidence_refs.",
    )
    description: str = Field(
        min_length=1,
        description="Plain-language statement of what conflicts and why it matters.",
    )
    material: bool = Field(
        default=True,
        description="True = the conflict could change the gate outcome; unresolved material contradictions block.",
    )
    resolved: bool = Field(
        default=False,
        description="True once the conflict has been settled; how it was settled goes in disposition.",
    )
    disposition: str | None = Field(
        default=None,
        description="How a resolved contradiction was settled (which side won and why).",
    )


@kind(
    "criteria_bundle",
    disposition="record",
    label="Criteria Bundle",
    family="workflow_io",
    example={
        "evaluator_id": "recovery_readiness",
        "assessments": [
            {
                "criterion_id": "RECOVERY_ASSET_INTEGRITY",
                "verdict": "met",
                "evidence_refs": ["EV-7"],
                "rationale": "observed_fact: EV-7 records the backup hash matching the vault copy.",
                "evaluator_id": "recovery_readiness",
                "confidence": 0.86,
            }
        ],
        "available_evidence_refs": ["EV-7"],
        "contradictions": [],
    },
    maturity="distilled",
)
class CriteriaBundle(KindModel, kind="criteria_bundle"):
    """One evaluator's independently produced assurance packet.

    A registered kind: a Run Typed Agent step that assesses one lane of a
    fail-closed gate answers in it, and its answer reaches this gate as-is
    (``__kind`` included) through ``CriteriaGateInput.bundles``.
    """

    evaluator_id: str = Field(
        min_length=1,
        description="Id of the evaluator lane that produced this bundle; every assessment inside must carry the same id.",
    )
    assessments: list[CriterionAssessment] = Field(
        default_factory=list,
        description="This evaluator's per-criterion verdicts (at most one per criterion).",
    )
    available_evidence_refs: list[str] = Field(
        default_factory=list,
        description="Evidence ids this evaluator had available; assessments may only cite these.",
    )
    contradictions: list[MaterialContradiction] = Field(
        default_factory=list,
        description="Conflicts this evaluator found between evidence items or verdicts.",
    )


class CriteriaGateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    assessments: list[CriterionAssessment] = Field(
        default_factory=list,
        description="Per-criterion verdicts supplied directly (outside any evaluator bundle), at most one per criterion.",
    )
    available_evidence_refs: list[str] = Field(
        default_factory=list,
        description="The full set of evidence ids that exist for this run; every cited reference must be in it.",
    )
    contradictions: list[MaterialContradiction] = Field(
        default_factory=list,
        description="Known conflicts between evidence items or verdicts, supplied directly.",
    )
    bundles: list[CriteriaBundle] = Field(
        default_factory=list,
        description=(
            "Parallel evaluator packets to flatten and validate before gating. "
            "Direct assessments, evidence, and contradictions may also be supplied."
        ),
    )


class CriteriaGateConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    criteria: list[CriterionDefinition] = Field(
        min_length=1,
        description="The checklist this gate enforces — every declared criterion must be assessed exactly once.",
    )
    required_evaluator_ids: list[str] = Field(
        default_factory=list,
        description=(
            "Evaluator/lane ids that must each contribute exactly one bundle. "
            "This makes parallel review coverage fail closed."
        ),
    )
    block_on_not_met: bool = Field(
        default=True,
        description="Block completion when any required criterion's verdict is 'not_met'.",
    )
    block_on_unknown: bool = Field(
        default=True,
        description="Block completion when any required criterion's verdict is 'unknown' (unresolved).",
    )
    block_on_unresolved_material_contradictions: bool = Field(
        default=True,
        description="Block completion while any contradiction marked material remains unresolved.",
    )

    @model_validator(mode="after")
    def unique_criterion_ids(self) -> CriteriaGateConfig:
        ids = [criterion.criterion_id for criterion in self.criteria]
        duplicates = sorted({criterion_id for criterion_id in ids if ids.count(criterion_id) > 1})
        if duplicates:
            raise ValueError(f"duplicate criterion ids: {', '.join(duplicates)}")
        evaluator_duplicates = sorted(
            {
                evaluator_id
                for evaluator_id in self.required_evaluator_ids
                if self.required_evaluator_ids.count(evaluator_id) > 1
            }
        )
        if evaluator_duplicates:
            raise ValueError(f"duplicate required evaluator ids: {', '.join(evaluator_duplicates)}")
        return self


class CriterionCoverage(KindModel, kind="criterion_coverage"):
    """One criterion's coverage — a kind of its own, NESTED (the §4.4 law).

    A gate reports many of these, and a repeated nested structure inside a kind
    is minted rather than smeared across the parent: a reviewer surface renders
    a self-describing row without knowing what produced it, and a single
    criterion can travel an edge as a value in its own right.
    """

    criterion_id: str = Field(description="Id of the declared criterion this row covers.")
    label: str = Field(description="Human-readable name of the criterion, from its definition.")
    required: bool = Field(
        description="Whether this criterion was declared blocking (required) in the gate config."
    )
    verdict: CriterionVerdict = Field(
        description="The accepted verdict for this criterion: 'met', 'not_met', 'unknown', or 'not_applicable'."
    )
    evidence_refs: list[str] = Field(
        description="Evidence ids the accepted assessment cited for this verdict."
    )
    rationale: str = Field(
        description="The evaluator's explanation of why this verdict was reached."
    )
    evaluator_id: str = Field(
        description="Id of the evaluator whose assessment was accepted for this criterion."
    )
    confidence: float = Field(description="The accepted assessment's confidence, 0.0 to 1.0.")


class GateViolation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str
    criterion_id: str | None = None
    reference_id: str | None = None
    message: str


class CriteriaGateOutput(KindModel, kind="criteria_gate_result"):
    verdict: Literal["passed"] = Field(
        default="passed",
        description="Always 'passed' — a blocked gate returns a structured failure, never this output.",
    )
    criteria: list[CriterionCoverage] = Field(
        description="Per-criterion coverage report: the accepted verdict, evidence, and evaluator for each declared criterion."
    )
    required_count: int = Field(
        description="How many declared criteria were marked required (blocking)."
    )
    assessed_count: int = Field(
        description="How many declared criteria received an accepted assessment."
    )
    evidence_reference_count: int = Field(
        description="How many distinct evidence ids were available across the direct input and all bundles."
    )
    contradiction_count: int = Field(
        description="How many contradiction records were considered (direct plus bundled)."
    )


def evaluate_criteria_gate(
    inputs: CriteriaGateInput,
    config: CriteriaGateConfig,
) -> tuple[list[CriterionCoverage], list[GateViolation]]:
    definitions = {criterion.criterion_id: criterion for criterion in config.criteria}
    violations: list[GateViolation] = []

    bundle_groups: dict[str, list[CriteriaBundle]] = {}
    for bundle in inputs.bundles:
        bundle_groups.setdefault(bundle.evaluator_id, []).append(bundle)
        for assessment in bundle.assessments:
            if assessment.evaluator_id != bundle.evaluator_id:
                violations.append(
                    GateViolation(
                        code="assessment_evaluator_mismatch",
                        criterion_id=assessment.criterion_id,
                        reference_id=bundle.evaluator_id,
                        message=(
                            f"Assessment '{assessment.criterion_id}' names evaluator "
                            f"'{assessment.evaluator_id}' but arrived in bundle "
                            f"'{bundle.evaluator_id}'."
                        ),
                    )
                )

    required_evaluators = set(config.required_evaluator_ids)
    for evaluator_id, group in sorted(bundle_groups.items()):
        if required_evaluators and evaluator_id not in required_evaluators:
            violations.append(
                GateViolation(
                    code="unexpected_evaluator",
                    reference_id=evaluator_id,
                    message=f"No required evaluator lane exists for bundle '{evaluator_id}'.",
                )
            )
        if len(group) > 1:
            violations.append(
                GateViolation(
                    code="duplicate_evaluator_bundle",
                    reference_id=evaluator_id,
                    message=(
                        f"Evaluator '{evaluator_id}' produced {len(group)} bundles; "
                        "exactly one is required."
                    ),
                )
            )
    for evaluator_id in config.required_evaluator_ids:
        if evaluator_id not in bundle_groups:
            violations.append(
                GateViolation(
                    code="missing_evaluator_bundle",
                    reference_id=evaluator_id,
                    message=f"Required evaluator lane '{evaluator_id}' produced no bundle.",
                )
            )

    all_assessments = list(inputs.assessments)
    all_evidence_refs = list(inputs.available_evidence_refs)
    all_contradictions = list(inputs.contradictions)
    for bundle in inputs.bundles:
        all_assessments.extend(bundle.assessments)
        all_evidence_refs.extend(bundle.available_evidence_refs)
        all_contradictions.extend(bundle.contradictions)
    known_evidence = set(all_evidence_refs)

    assessment_groups: dict[str, list[CriterionAssessment]] = {}
    for assessment in all_assessments:
        assessment_groups.setdefault(assessment.criterion_id, []).append(assessment)

    for criterion_id, group in sorted(assessment_groups.items()):
        if criterion_id not in definitions:
            violations.append(
                GateViolation(
                    code="unexpected_criterion",
                    criterion_id=criterion_id,
                    message=f"No declared criterion exists for assessment '{criterion_id}'.",
                )
            )
        if len(group) > 1:
            violations.append(
                GateViolation(
                    code="duplicate_assessment",
                    criterion_id=criterion_id,
                    message=f"Criterion '{criterion_id}' was assessed {len(group)} times; exactly one is required.",
                )
            )

    coverage: list[CriterionCoverage] = []
    for definition in config.criteria:
        group = assessment_groups.get(definition.criterion_id, [])
        if not group:
            violations.append(
                GateViolation(
                    code="missing_assessment",
                    criterion_id=definition.criterion_id,
                    message=f"Criterion '{definition.criterion_id}' has no assessment.",
                )
            )
            continue
        assessment = group[0]
        coverage.append(
            CriterionCoverage(
                criterion_id=definition.criterion_id,
                label=definition.label,
                required=definition.required,
                verdict=assessment.verdict,
                evidence_refs=assessment.evidence_refs,
                rationale=assessment.rationale,
                evaluator_id=assessment.evaluator_id,
                confidence=assessment.confidence,
            )
        )
        if definition.evidence_required and not assessment.evidence_refs:
            violations.append(
                GateViolation(
                    code="missing_evidence",
                    criterion_id=definition.criterion_id,
                    message=f"Criterion '{definition.criterion_id}' requires at least one evidence reference.",
                )
            )
        for evidence_ref in assessment.evidence_refs:
            if evidence_ref not in known_evidence:
                violations.append(
                    GateViolation(
                        code="unknown_evidence_reference",
                        criterion_id=definition.criterion_id,
                        reference_id=evidence_ref,
                        message=f"Criterion '{definition.criterion_id}' references unknown evidence '{evidence_ref}'.",
                    )
                )
        if definition.required:
            if assessment.verdict == "not_met" and config.block_on_not_met:
                violations.append(
                    GateViolation(
                        code="required_criterion_not_met",
                        criterion_id=definition.criterion_id,
                        message=f"Required criterion '{definition.criterion_id}' is not met.",
                    )
                )
            elif assessment.verdict == "unknown" and config.block_on_unknown:
                violations.append(
                    GateViolation(
                        code="required_criterion_unknown",
                        criterion_id=definition.criterion_id,
                        message=f"Required criterion '{definition.criterion_id}' is unresolved.",
                    )
                )
            elif assessment.verdict == "not_applicable" and not definition.allow_not_applicable:
                violations.append(
                    GateViolation(
                        code="not_applicable_disallowed",
                        criterion_id=definition.criterion_id,
                        message=f"Required criterion '{definition.criterion_id}' cannot be marked not applicable.",
                    )
                )

    contradiction_ids: set[str] = set()
    for contradiction in all_contradictions:
        if contradiction.contradiction_id in contradiction_ids:
            violations.append(
                GateViolation(
                    code="duplicate_contradiction",
                    reference_id=contradiction.contradiction_id,
                    message=f"Contradiction '{contradiction.contradiction_id}' appears more than once.",
                )
            )
        contradiction_ids.add(contradiction.contradiction_id)
        for criterion_id in contradiction.criterion_ids:
            if criterion_id not in definitions:
                violations.append(
                    GateViolation(
                        code="contradiction_unknown_criterion",
                        criterion_id=criterion_id,
                        reference_id=contradiction.contradiction_id,
                        message=f"Contradiction '{contradiction.contradiction_id}' references unknown criterion '{criterion_id}'.",
                    )
                )
        for evidence_ref in contradiction.evidence_refs:
            if evidence_ref not in known_evidence:
                violations.append(
                    GateViolation(
                        code="unknown_evidence_reference",
                        reference_id=evidence_ref,
                        message=f"Contradiction '{contradiction.contradiction_id}' references unknown evidence '{evidence_ref}'.",
                    )
                )
        if (
            config.block_on_unresolved_material_contradictions
            and contradiction.material
            and not contradiction.resolved
        ):
            violations.append(
                GateViolation(
                    code="unresolved_material_contradiction",
                    reference_id=contradiction.contradiction_id,
                    message=f"Material contradiction '{contradiction.contradiction_id}' is unresolved.",
                )
            )

    return coverage, violations


class CriteriaGateExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.criteria_gate",
        category=NodeCategory.DATA,
        display_name="Completion Check",
        description="Verify that every required criterion was assessed once, supported, and resolved.",
        input_schema=CriteriaGateInput,
        output_schema=CriteriaGateOutput,
        config_schema=CriteriaGateConfig,
        output_kind="criteria_gate_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="list-checks",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: CriteriaGateInput,
        config: CriteriaGateConfig,
    ) -> NodeResult[CriteriaGateOutput]:
        _ = ctx
        coverage, violations = evaluate_criteria_gate(inputs, config)
        known_evidence = {
            *inputs.available_evidence_refs,
            *(ref for bundle in inputs.bundles for ref in bundle.available_evidence_refs),
        }
        all_contradictions = [
            *inputs.contradictions,
            *(item for bundle in inputs.bundles for item in bundle.contradictions),
        ]
        bundle_groups = {bundle.evaluator_id for bundle in inputs.bundles}
        if violations:
            report = {
                "verdict": "blocked",
                "criteria": [item.model_dump(mode="json") for item in coverage],
                "violations": [item.model_dump(mode="json") for item in violations],
                "required_count": sum(criterion.required for criterion in config.criteria),
                "assessed_count": len(coverage),
                "evidence_reference_count": len(known_evidence),
                "contradiction_count": len(all_contradictions),
                "required_evaluator_count": len(config.required_evaluator_ids),
                "received_evaluator_count": len(bundle_groups),
            }
            return failure(
                "criteria_gate_blocked",
                f"Completion blocked by {len(violations)} assurance violation(s).",
                details={"report": report},
            )
        return success(
            CriteriaGateOutput(
                criteria=coverage,
                required_count=sum(criterion.required for criterion in config.criteria),
                assessed_count=len(coverage),
                evidence_reference_count=len(known_evidence),
                contradiction_count=len(all_contradictions),
            )
        )
