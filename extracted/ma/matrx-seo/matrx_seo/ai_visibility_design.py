"""The deterministic half of AI-visibility panel DESIGN — no DB, no HTTP, no LLM.

The design workflow (`seo.ai_visibility_panel_design`) runs seven agents and
four human gates. Everything that can be computed is computed here, so no agent
ever does arithmetic, counts, hashing, blinding or reference checking. The
methods are adapted from newsjack's `build-ai-visibility-panel` skill family
(MIT, pinned 092d882, Elvis Sun and contributors); their deterministic grader's
check IDs are ported VERBATIM by :func:`validate_artifacts`, so our verdicts and
theirs are comparable check for check.

Tools (brief "Tool specs — the deterministic parts"):

========  ===================================================================
T1        :func:`validate_artifacts` — every structural check grade.py runs on
          the fourteen artifacts, same IDs, plus strict ``schema:<file>``
          checks against the Pydantic contract models below.
T2        :func:`canonical_hash`, :func:`text_hash`, :func:`source_manifest_hash`.
T3        :func:`build_charter`, :func:`seed_register`, :func:`freeze_register`.
T4        :func:`scan_text`, :func:`contamination_scan`.
T5        :func:`build_blind_brief`, :func:`scan_rendered_request`,
          :func:`scan_output`, :func:`assert_blind_mandate`.
T6        :func:`normalize_prompt`, :func:`normalize_and_dedupe`.
T7        :func:`similarity_pairs` (nominate only, never delete).
T8        :func:`reconcile_qa`.
T9        :func:`coverage_matrix`.
T10       :func:`allocate_and_price`.
T11       :func:`freeze_version`, :func:`append_ledger`.
T12       :func:`estimate`, :func:`build_panel_metrics` → :class:`PanelMetrics`.
T13       :func:`plan_variance_pilot`, :func:`decompose_variance`.
T14       :func:`entity_mentions`, :func:`entity_mentions_from_register`.
T15       :func:`configuration_hash`, :func:`build_run_manifest_record`.
========  ===================================================================

**The blinding wall API (for the service guard, lane D).** The guard in
``aidream/services/seo/ai_visibility_blind_wall.py`` calls, in order:

1. ``build_blind_brief(buyer_jobs, register, ...)`` → :class:`BlindBriefBuild`
   (``brief``, ``dropped_fragments``, ``dropped_values``, ``blind_brief_hash``).
   Only whitelisted fields leave; any value hitting the register is dropped and
   counted (the count goes on the Gate 3 card).
2. ``assert_blind_mandate(definition)`` → list of problems (empty = OK): the
   writer mandate must declare ``auto_context_disabled = true`` and no tools.
3. ``scan_rendered_request(blocks, register)`` on the FULLY rendered request as
   the provider receives it (system, user, every context block) →
   :class:`RequestScan`. ``allowed is False`` → refuse the dispatch and record
   ``request_hash``.
4. ``scan_output(universe_or_candidates, register)`` after the call → hits per
   candidate; any hit in an unaided candidate is a wall breach.

🚨 NULL IS UNMEASURED, NEVER ZERO (same doctrine as ``ai_visibility_panel.py``):
every rate here is ``None`` until something valid was observed.
"""

from __future__ import annotations

import collections
import difflib
import hashlib
import json
import math
import random
import re
import unicodedata
from collections.abc import Callable, Iterable, Mapping, Sequence
from decimal import Decimal
from statistics import NormalDist
from typing import Any, Literal, get_args

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)

from .ai_visibility_panel import FALLBACK_COST_PER_PROMPT_ENGINE
from .providers.dataforseo.ai_answers import AI_ANSWER_LOCATION_ENGINES, answer_mentions_target

# ---------------------------------------------------------------------------
# Names and enums (contract codes — never renamed; human text uses display names)
# ---------------------------------------------------------------------------

SCHEMA_VERSION = "1.0.0"

#: The fourteen artifacts: contract name → the file name their grader keys on.
ARTIFACT_FILES: dict[str, str] = {
    "panel_report": "panel_report.md",
    "tracking_plan": "tracking_plan.md",
    "measurement_charter": "measurement_charter.json",
    "source_manifest": "source_manifest.json",
    "icp_hypotheses": "icp_hypotheses.json",
    "buyer_jobs": "buyer_jobs.json",
    "contamination_register": "contamination_register.yaml",
    "blind_design_brief": "blind_design_brief.json",
    "prompt_architecture": "prompt_architecture.json",
    "prompt_universe": "prompt_universe.json",
    "prompt_qa": "prompt_qa.json",
    "panel": "panel.yaml",
    "run_manifest_template": "run_manifest_template.json",
    "panel_change_ledger": "panel_change_ledger.json",
}
REQUIRED_ARTIFACTS: tuple[str, ...] = tuple(ARTIFACT_FILES.values())
JSON_ARTIFACTS = tuple(n for n in REQUIRED_ARTIFACTS if n.endswith(".json"))
YAML_ARTIFACTS = tuple(n for n in REQUIRED_ARTIFACTS if n.endswith(".yaml"))
MACHINE_ARTIFACTS = JSON_ARTIFACTS + YAML_ARTIFACTS

SHA_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
RFC3339_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")
SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")

#: Verbatim from their grade.py ENUMS.
ENUMS: dict[str, set[Any]] = {
    "information_act": {
        "explain",
        "diagnose",
        "plan",
        "generate",
        "compare",
        "recommend",
        "verify",
        "navigate",
        "buy",
        "implement",
        "troubleshoot",
    },
    "journey_state": {
        "problem_identification",
        "exploration",
        "requirements_building",
        "supplier_selection",
        "adoption",
        "post_purchase",
    },
    "funnel": {"TOFU", "MOFU", "BOFU", None},
    "proximity_band": {
        "B0_direct_brand_product",
        "B1_comparison_purchase",
        "B2_category",
        "B3_problem_need",
        "B4_job_goal",
        "B5_broad_discovery_story",
    },
    "aided_status": {"target_aided", "competitor_aided", "category_aided", "unaided"},
    "lane": {"closed_model", "retrieval", "consumer_surface", "campaign_experiment"},
    "partition": {"core", "rotating", "sentinel", "control", "aided"},
    "transformation": {
        "verbatim",
        "lightly_normalized",
        "search_query_expanded",
        "human_written",
        "llm_expanded",
        "translated",
        "locale_transcreated",
    },
    "evidence_grade": {"A", "B", "C", "D"},
}

InformationAct = Literal[
    "explain",
    "diagnose",
    "plan",
    "generate",
    "compare",
    "recommend",
    "verify",
    "navigate",
    "buy",
    "implement",
    "troubleshoot",
]
JourneyState = Literal[
    "problem_identification",
    "exploration",
    "requirements_building",
    "supplier_selection",
    "adoption",
    "post_purchase",
]
Funnel = Literal["TOFU", "MOFU", "BOFU"] | None
ProximityBand = Literal[
    "B0_direct_brand_product",
    "B1_comparison_purchase",
    "B2_category",
    "B3_problem_need",
    "B4_job_goal",
    "B5_broad_discovery_story",
]
AidedStatus = Literal["target_aided", "competitor_aided", "category_aided", "unaided"]
Lane = Literal["closed_model", "retrieval", "consumer_surface", "campaign_experiment"]
Partition = Literal["core", "rotating", "sentinel", "control", "aided"]
Transformation = Literal[
    "verbatim",
    "lightly_normalized",
    "search_query_expanded",
    "human_written",
    "llm_expanded",
    "translated",
    "locale_transcreated",
]
EvidenceGrade = Literal["A", "B", "C", "D"]
SourceClass = Literal[
    "company_asserted", "buyer_behavior", "independent", "search_proxy", "llm_hypothesis"
]
SourceType = Literal[
    "product",
    "pricing",
    "support",
    "technical",
    "review",
    "forum",
    "interview",
    "query",
    "procurement",
    "news",
    "other",
]
Permission = Literal["public", "user_authorized", "generated"]
FactType = Literal[
    "capability",
    "limitation",
    "segment",
    "trigger",
    "job",
    "criterion",
    "language",
    "competitor",
    "market_event",
    "other",
]
Confidence = Literal["high", "medium", "low"]
VariantRole = Literal["observed_language", "natural_paraphrase", "sensitivity"]
TurnForm = Literal["single_turn", "scripted_multi_turn"]
QAStatus = Literal["pass", "revise", "quarantine", "reject"]
PanelStatus = Literal["draft", "provisional_directional", "frozen"]
TermClass = Literal[
    "brands",
    "products",
    "domains",
    "people",
    "slogans",
    "proprietary_categories",
    "campaign_terms",
    "flattering_claims",
    "competitor_terms",
]
TARGET_TERM_CLASSES: tuple[str, ...] = (
    "brands",
    "products",
    "domains",
    "people",
    "slogans",
    "proprietary_categories",
    "campaign_terms",
    "flattering_claims",
)
ALL_TERM_CLASSES: tuple[str, ...] = (*TARGET_TERM_CLASSES, "competitor_terms")

MetricName = Literal[
    "unaided_brand_presence",
    "aided_brand_knowledge",
    "competitive_mention_share",
    "citation_presence",
    "answer_framing",
    "campaign_response",
]

#: Display names (BUILD-CONTRACT "Names").
PARTITION_NAMES = {
    "core": "tracked set",
    "rotating": "discovery set",
    "sentinel": "tripwire",
    "control": "false-positive check",
    "aided": "prompted set",
}
LANE_NAMES = {
    "closed_model": "no web access",
    "retrieval": "with web search",
    "consumer_surface": "the real app",
    "campaign_experiment": "campaign test",
}
AIDED_NAMES = {
    "unaided": "unprompted",
    "target_aided": "we're named",
    "category_aided": "category named",
    "competitor_aided": "competitors named",
}
BAND_NAMES = {
    "B0_direct_brand_product": "Brand",
    "B1_comparison_purchase": "Shortlist",
    "B2_category": "Category",
    "B3_problem_need": "Problem",
    "B4_job_goal": "Goal",
    "B5_broad_discovery_story": "Market",
}


class MetricDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    metric: MetricName
    display_name: str
    numerator: str
    denominator: str
    eligible_partitions: tuple[Partition, ...]
    eligible_lanes: tuple[Lane, ...]
    does_not_prove: str


#: The six estimands — numerator/denominator/eligibility/does_not_prove are the
#: brief's table, verbatim.
METRICS: dict[str, MetricDefinition] = {
    m.metric: m
    for m in (
        MetricDefinition(
            metric="unaided_brand_presence",
            display_name="Named, unprompted",
            numerator="valid answers naming the target",
            denominator=(
                "all valid observations in the declared unprompted set, lane, engine, "
                "locale and wave"
            ),
            eligible_partitions=("core", "sentinel"),
            eligible_lanes=("closed_model", "retrieval"),
            does_not_prove="market share, awareness, audience reach, or revenue attribution",
        ),
        MetricDefinition(
            metric="aided_brand_knowledge",
            display_name="Known when named",
            numerator=(
                'valid answers to "we\'re named" questions that identify the target and state '
                "no fact contradicting the confirmed fact ledger"
            ),
            denominator="all valid observations in the prompted set",
            eligible_partitions=("aided",),
            eligible_lanes=("closed_model", "retrieval"),
            does_not_prove=(
                "that anyone asks these questions, or that unprompted answers mention you"
            ),
        ),
        MetricDefinition(
            metric="competitive_mention_share",
            display_name="Share of mentions",
            numerator="target mentions",
            denominator=(
                "mentions of any tracked entity (target + register competitors) in the same "
                "unprompted observations"
            ),
            eligible_partitions=("core",),
            eligible_lanes=("closed_model", "retrieval"),
            does_not_prove="market share; the share of real buyers who choose you",
        ),
        MetricDefinition(
            metric="citation_presence",
            display_name="Cited as a source",
            numerator="valid answers citing a target-domain URL",
            denominator="valid observations in which the engine exposed citations",
            eligible_partitions=("core", "rotating", "sentinel", "control", "aided"),
            eligible_lanes=("retrieval",),
            does_not_prove="traffic, clicks, or that the citation shaped the answer",
        ),
        MetricDefinition(
            metric="answer_framing",
            display_name="How answers describe you",
            numerator=(
                "answers carrying each key message, or each framing the decision analyst codes"
            ),
            denominator="valid answers that name the target",
            eligible_partitions=("core", "rotating", "sentinel", "control", "aided"),
            eligible_lanes=("closed_model", "retrieval"),
            does_not_prove="that the framing is correct, persuasive or seen by buyers",
        ),
        MetricDefinition(
            metric="campaign_response",
            display_name="Campaign response",
            numerator="change in a pre-registered treatment set",
            denominator="matched controls",
            eligible_partitions=("core", "control"),
            eligible_lanes=("campaign_experiment",),
            does_not_prove=(
                'anything, until a pre-registered design exists; shown as "not set up", never zero'
            ),
        ),
    )
}

EVIDENCE_LADDER: list[str] = [
    "1. A mention, framing or citation in this panel's answers",
    "2. Source or referral traffic",
    "3. Self-reported discovery",
    "4. Qualified lead or conversion",
    "5. Incremental outcome from an experiment or counterfactual",
]
CONDITIONAL_NOTE = (
    "Every number here is conditional on this panel: its questions, engines, lanes, locales "
    "and dates. It is not a probability sample of real buyers, and a panel mention is rung 1 "
    "of 5 on the evidence ladder, never attribution."
)


# ---------------------------------------------------------------------------
# T2 — canonical hashing
# ---------------------------------------------------------------------------


def canonical_json(value: Any) -> str:
    """Canonical UTF-8 JSON: sorted keys, no incidental whitespace."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def canonical_hash(value: Any) -> str:
    """``sha256:<hex>`` of :func:`canonical_json` (identical to their grader's digest)."""
    if isinstance(value, BaseModel):
        value = value.model_dump(mode="json")
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def text_hash(text: str) -> str:
    """``prompt_hash``: SHA-256 of the exact UTF-8 text (no normalization)."""
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def source_manifest_hash(manifest_or_sources: Mapping[str, Any] | Sequence[Any]) -> str:
    """Hash of the ``sources`` ARRAY only — copied into every artifact's envelope."""
    sources = (
        manifest_or_sources.get("sources")
        if isinstance(manifest_or_sources, Mapping)
        else manifest_or_sources
    )
    if not isinstance(sources, list):
        raise ValueError("source_manifest_hash needs the manifest's `sources` array")
    return canonical_hash(sources)


def is_real_hash(value: Any) -> bool:
    return isinstance(value, str) and bool(SHA_RE.match(value))


# ---------------------------------------------------------------------------
# Pydantic contract models (the fourteen artifacts; extra="forbid"; the only alias is the
# tolerant ``__kind`` marker every closed object declares)
# ---------------------------------------------------------------------------


class _Strict(BaseModel):
    """Closed contract object that DECLARES ``__kind`` in the tolerant form (the platform's
    schema law): a marker an agent carried onto a record is accepted and kept as data, never
    required and never invented. Every other key stays forbidden."""

    model_config = ConfigDict(
        extra="forbid", validate_by_name=True, validate_by_alias=True, serialize_by_alias=True
    )

    kind_marker: str | None = Field(
        default=None,
        alias="__kind",
        description="The registered kind this payload is an instance of, when it is one.",
        exclude_if=lambda v: v is None,
    )


class Envelope(_Strict):
    schema_version: Literal["1.0.0"] = SCHEMA_VERSION
    artifact_id: str = Field(min_length=1)
    created_at: str = Field(pattern=RFC3339_RE.pattern)
    created_by: str = Field(min_length=1)
    source_manifest_hash: str | None = Field(default=None, pattern=SHA_RE.pattern)
    warnings: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _null_hash_is_announced(self) -> Envelope:
        if self.source_manifest_hash is None and not any(
            "hash" in w.casefold() for w in self.warnings
        ):
            raise ValueError(
                "source_manifest_hash is null without a warning naming the missing hash"
            )
        return self


class Source(_Strict):
    source_id: str = Field(min_length=1)
    url: str | None
    title: str
    publisher: str | None = None
    published_at: str | None = None
    accessed_at: str
    source_class: SourceClass
    source_type: SourceType
    permission: Permission
    evidence_grade: EvidenceGrade
    span: str = Field(min_length=1)
    span_locator: str = Field(min_length=1)
    fact_type: FactType
    confidence: Confidence
    content_hash: str | None = None

    @model_validator(mode="after")
    def _permission_rules(self) -> Source:
        if self.permission == "generated":
            if (
                self.source_class != "llm_hypothesis"
                or self.evidence_grade != "D"
                or self.url is not None
            ):
                raise ValueError("generated sources require llm_hypothesis, grade D, url null")
        elif not self.url:
            raise ValueError("public/user_authorized evidence needs a URL or file locator")
        return self


class SourceManifest(Envelope):
    sources: list[Source]


class Estimand(_Strict):
    name: MetricName
    numerator: str
    denominator: str
    eligible_partitions: list[Partition]
    eligible_lanes: list[Lane]
    does_not_prove: str


class PerimeterArea(_Strict):
    area: str
    covered_by: list[str] | None = None
    canonical_cell_ids: list[str] | None = None
    waiver: str | None = None


class MeasurementCharter(Envelope):
    business_decision: str
    estimands: list[Estimand]
    target_population: str
    exclusions: list[str] = Field(default_factory=list)
    #: The contract names these fields without fixing their inner shape.
    products: list[str | dict[str, Any]] = Field(default_factory=list)
    markets: list[str] = Field(default_factory=list)
    locales: list[str]
    time_horizon: str
    surfaces: list[str]
    lanes: list[Lane]
    lane_policies: dict[Lane, str] = Field(default_factory=dict)
    surface_policies: dict[str, dict[str, Any]] = Field(default_factory=dict)
    reporting_strata: list[str]
    run_budget: dict[str, Any] | str
    review_budget: dict[str, Any] | str
    precision_status: str
    approver: str | None = None
    approval_status: Literal["pending", "approved"] = "pending"
    perimeter: list[PerimeterArea] = Field(default_factory=list)


class Icp(_Strict):
    icp_id: str
    label: str
    context: dict[str, Any] = Field(default_factory=dict)
    triggers: list[Any] = Field(default_factory=list)
    roles: list[Any] = Field(default_factory=list)
    constraints: list[Any] = Field(default_factory=list)
    disqualifiers: list[Any] = Field(default_factory=list)
    standing_claim_ids: list[str] = Field(default_factory=list)
    supporting_source_ids: list[str] = Field(default_factory=list)
    counterevidence_source_ids: list[str] = Field(default_factory=list)
    confidence: Confidence
    status: str
    open_questions: list[str] = Field(default_factory=list)


class IcpHypotheses(Envelope):
    gate_status: Literal["ready_for_human_review", "needs_research", "approved"]
    icps: list[Icp]


class LanguageSample(_Strict):
    text: str
    source_id: str
    span: str | None = None
    locale: str | None = None
    evidence_grade: EvidenceGrade | None = None


class BuyerJob(_Strict):
    job_id: str
    icp_ids: list[str]
    statement: str
    struggling_moment: str | None = None
    desired_progress: str | None = None
    workarounds: list[str] = Field(default_factory=list)
    forces: dict[str, Any] = Field(default_factory=dict)
    information_acts: list[InformationAct] = Field(default_factory=list)
    journey_states: list[JourneyState] = Field(default_factory=list)
    criteria: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    roles: list[str] = Field(default_factory=list)
    language_samples: list[LanguageSample] = Field(default_factory=list)
    supporting_source_ids: list[str] = Field(default_factory=list)
    counterevidence_source_ids: list[str] = Field(default_factory=list)
    evidence_grade: EvidenceGrade
    confidence: Confidence
    status: str


class BuyerJobs(Envelope):
    gate_status: Literal["ready_for_human_review", "needs_research", "approved"]
    jobs: list[BuyerJob]


class TargetTerms(_Strict):
    brands: list[str] = Field(default_factory=list)
    products: list[str] = Field(default_factory=list)
    domains: list[str] = Field(default_factory=list)
    people: list[str] = Field(default_factory=list)
    slogans: list[str] = Field(default_factory=list)
    proprietary_categories: list[str] = Field(default_factory=list)
    campaign_terms: list[str] = Field(default_factory=list)
    flattering_claims: list[str] = Field(default_factory=list)


class AllowedException(_Strict):
    band: ProximityBand
    term_classes: list[TermClass]
    aided_status: AidedStatus | None = None
    partition: Partition | None = None
    reason: str


class TermProvenance(_Strict):
    term: str
    term_class: TermClass
    source: str


class ContaminationRegister(Envelope):
    target_terms: TargetTerms
    competitor_terms: list[str] = Field(default_factory=list)
    allowed_exceptions: list[AllowedException] = Field(default_factory=list)
    term_provenance: list[TermProvenance] = Field(default_factory=list)
    frozen_hash: str | None = None


class BriefJob(_Strict):
    job_id: str
    statement: str
    information_acts: list[InformationAct] = Field(default_factory=list)
    journey_states: list[JourneyState] = Field(default_factory=list)
    evidence_grade: EvidenceGrade
    evidence_ids: list[str] = Field(default_factory=list)


class BriefRole(_Strict):
    persona_id: str
    label: str


class BriefConstraint(_Strict):
    constraint_id: str
    label: str


class BriefFragment(_Strict):
    fragment: str
    evidence_id: str
    evidence_grade: EvidenceGrade | None = None
    locale: str | None = None


class BlindDesignBrief(Envelope):
    approved_jobs: list[BriefJob]
    anonymized_roles: list[BriefRole] = Field(default_factory=list)
    material_constraints: list[BriefConstraint] = Field(default_factory=list)
    locales: list[str] = Field(default_factory=list)
    safe_language_fragments: list[BriefFragment] = Field(default_factory=list)
    required_strata: dict[str, Any] = Field(default_factory=dict)
    dropped_fragment_count: int = 0


class CellSpec(_Strict):
    cell_spec_id: str
    job_id: str
    icp_ids: list[str]
    information_act: InformationAct
    journey_state: JourneyState
    funnel: Funnel
    proximity_band: ProximityBand
    aided_status: AidedStatus
    campaign_exposed: bool
    persona_id: str
    locale: str
    language: str
    material_constraints: list[str]
    expected_answer_kind: str
    turn_form: TurnForm
    lane_eligibility: list[Lane]
    partition: Partition
    evidence_grade: EvidenceGrade
    reason_source_ids: list[str]
    target_variants: int = 2
    required: bool = True
    review_by: str | None = None


class PromptArchitecture(Envelope):
    cells: list[CellSpec]
    prohibited_cells: list[dict[str, Any]] = Field(default_factory=list)
    coverage_gaps: list[dict[str, Any]] = Field(default_factory=list)
    allocation: dict[str, Any] = Field(default_factory=dict)


class GenerationProvenance(_Strict):
    model: str
    prompt_hash: str | None = None


class Candidate(_Strict):
    candidate_id: str
    variant_role: VariantRole
    text: str = Field(min_length=1)
    language: str | None = None
    locale: str | None = None
    transformation: Transformation
    source_ids: list[str]
    evidence_grade: EvidenceGrade
    locale_review_status: Literal["not_required", "pending", "approved"]
    generation_provenance: GenerationProvenance
    promoted: bool | None = None
    promotion: dict[str, Any] | None = None


class CanonicalCell(CellSpec):
    canonical_cell_id: str
    candidates: list[Candidate]


class PromptUniverse(Envelope):
    canonical_cells: list[CanonicalCell] = Field(min_length=1)
    blind_brief_hash: str | None = None


class QADecision(_Strict):
    candidate_id: str
    status: QAStatus
    rule_results: list[dict[str, Any]] = Field(default_factory=list)
    duplicate_decision: dict[str, Any] | None = None
    route_to: str | None = None
    reason: str
    review_confidence: Confidence


QA_COUNT_KEYS = ("total_candidates", "pass", "revise", "quarantine", "reject", "accepted")


class PromptQA(Envelope):
    baseline_fields_blinded: bool
    decisions: list[QADecision]
    accepted_candidate_ids: list[str]
    #: A mapping, not a model: the contract key "pass" is a Python keyword and
    #: aliases are banned. Exactly the six keys, each a non-negative int.
    counts: dict[str, int]

    @model_validator(mode="after")
    def _count_keys(self) -> PromptQA:
        if set(self.counts) != set(QA_COUNT_KEYS) or any(v < 0 for v in self.counts.values()):
            raise ValueError(f"counts must hold exactly {list(QA_COUNT_KEYS)}")
        return self


class PartitionCells(_Strict):
    canonical_cell_ids: list[str]


class WeightFactor(_Strict):
    factor_id: str
    value: float
    confidence: Confidence
    version: str
    source_id: str | None = None
    decision_id: str | None = None
    approver: str | None = None

    @model_validator(mode="after")
    def _provenance(self) -> WeightFactor:
        if not self.source_id and not (self.decision_id and self.approver):
            raise ValueError("a weight factor needs a source_id, or a decision_id and approver")
        return self


class WeightComponent(_Strict):
    method: str
    factors: list[WeightFactor] = Field(default_factory=list)
    rationale: str | None = None


class PanelWeights(_Strict):
    exposure: WeightComponent
    priority: WeightComponent


class PanelStatistics(_Strict):
    cluster_unit: Literal["canonical_cell_id"] = "canonical_cell_id"
    pilot_status: str
    uncertainty_method: str | None = None
    min_cells_for_rate: int | None = None
    bootstrap_draws: int | None = None


class Approval(_Strict):
    gate: int | str
    status: Literal["pending", "approved", "edited", "continued_pending"]
    approver: str | None = None
    decided_at: str | None = None
    note: str | None = None


class Panel(Envelope):
    panel_id: str
    version: str = Field(pattern=SEMVER_RE.pattern)
    status: PanelStatus
    charter_id: str | None = None
    estimands: list[Estimand] = Field(default_factory=list)
    partitions: dict[Partition, PartitionCells]
    selected_candidate_ids: list[str] = Field(min_length=1)
    selected_variants: dict[str, Any] = Field(default_factory=dict)
    lanes: list[Lane] = Field(default_factory=list)
    surfaces: list[str] = Field(default_factory=list)
    locales: list[str] = Field(default_factory=list)
    engines: list[str] = Field(default_factory=list)
    repetitions: dict[str, Any] = Field(default_factory=dict)
    randomization: dict[str, Any] = Field(default_factory=dict)
    controls: dict[str, Any] = Field(default_factory=dict)
    weight: PanelWeights
    statistics: PanelStatistics
    refresh_policy: dict[str, Any] = Field(default_factory=dict)
    next_review: str | None = None
    limitations: list[str]
    approvals: list[Approval]
    waivers: list[dict[str, Any]] = Field(default_factory=list)
    change_ledger_id: str | None = None


class RunObservationTemplate(BaseModel):
    """The contract says additional fields are allowed here; aliases are not."""

    model_config = ConfigDict(extra="allow")

    exact_prompt: str
    configuration_hash: str | None
    provider: str
    model: str
    surface: str
    lane: str
    locale: str
    search_policy: str
    retrieval_used: bool | None
    session_state: str
    response_payload_hash: str | None
    citation_payload_hash: str | None
    timestamp: str
    retry_status: str
    validity_status: str
    parser_version: str


class RunManifestTemplate(Envelope):
    panel_id: str
    panel_version: str
    observation_template: RunObservationTemplate
    validity_rules: list[str] = Field(default_factory=list)


class LedgerChange(_Strict):
    change_id: str
    at: str
    version: str
    actor: str
    type: str
    summary: str
    affects: list[str] = Field(default_factory=list)
    overlap_bridge: dict[str, Any] | None = None


class PanelChangeLedger(Envelope):
    panel_id: str
    changes: list[LedgerChange]


ARTIFACT_MODELS: dict[str, type[BaseModel]] = {
    "measurement_charter.json": MeasurementCharter,
    "source_manifest.json": SourceManifest,
    "icp_hypotheses.json": IcpHypotheses,
    "buyer_jobs.json": BuyerJobs,
    "contamination_register.yaml": ContaminationRegister,
    "blind_design_brief.json": BlindDesignBrief,
    "prompt_architecture.json": PromptArchitecture,
    "prompt_universe.json": PromptUniverse,
    "prompt_qa.json": PromptQA,
    "panel.yaml": Panel,
    "run_manifest_template.json": RunManifestTemplate,
    "panel_change_ledger.json": PanelChangeLedger,
}


def make_envelope(
    *,
    artifact_id: str,
    created_by: str,
    created_at: str,
    source_manifest_hash: str | None = None,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    """The common envelope; a null hash always carries its warning."""
    notes = list(warnings or [])
    if source_manifest_hash is None and not any("hash" in w.casefold() for w in notes):
        notes.append("hash_not_computed: compute source_manifest_hash before freeze")
    return {
        "schema_version": SCHEMA_VERSION,
        "artifact_id": artifact_id,
        "created_at": created_at,
        "created_by": created_by,
        "source_manifest_hash": source_manifest_hash,
        "warnings": notes,
    }


# ---------------------------------------------------------------------------
# T1 — validate_artifacts (their grade.py checks, IDs verbatim)
# ---------------------------------------------------------------------------


class CheckResult(_Strict):
    id: str
    passed: bool
    severity: Literal["critical", "error", "warning"] = "error"
    evidence: Any = None


class _Checks:
    def __init__(self) -> None:
        self.items: list[CheckResult] = []

    def add(self, ident: str, passed: bool, evidence: Any, *, severity: str = "error") -> None:
        self.items.append(
            CheckResult(id=ident, passed=bool(passed), severity=severity, evidence=evidence)
        )


def checks_passed(checks: Iterable[CheckResult]) -> bool:
    """True when every error/critical check passed (warnings never block)."""
    return all(c.passed for c in checks if c.severity in ("error", "critical"))


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _unique_nonempty(values: Iterable[Any]) -> set[str]:
    return {str(v) for v in values if v is not None and str(v).strip()}


def _grader_normalize(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w]+", " ", value.casefold())).strip()


def term_in_text(term: str, text: str) -> bool:
    """Their grader's token-sequence match (never a substring inside a word)."""
    needle = _grader_normalize(term)
    haystack = f" {_grader_normalize(text)} "
    return bool(needle and f" {needle} " in haystack)


def _recursive_values(value: Any, keys: set[str]) -> list[Any]:
    found: list[Any] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key in keys:
                found.extend(_as_list(child))
            found.extend(_recursive_values(child, keys))
    elif isinstance(value, list):
        for child in value:
            found.extend(_recursive_values(child, keys))
    return found


def _recursive_source_refs(value: Any) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {
                "source_id",
                "source_ids",
                "reason_source_ids",
                "supporting_source_ids",
                "counterevidence_source_ids",
            } or key.endswith("_source_ids"):
                refs |= _unique_nonempty(_as_list(child))
            refs |= _recursive_source_refs(child)
    elif isinstance(value, list):
        for child in value:
            refs |= _recursive_source_refs(child)
    return refs


def flatten_universe(
    universe: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Cells, and candidates each merged with their cell's flat fields."""
    cells = universe.get("canonical_cells")
    if not isinstance(cells, list):
        return [], []
    candidates: list[dict[str, Any]] = []
    valid_cells: list[dict[str, Any]] = []
    for raw_cell in cells:
        if not isinstance(raw_cell, dict):
            continue
        valid_cells.append(raw_cell)
        for raw_candidate in _as_list(raw_cell.get("candidates")):
            if not isinstance(raw_candidate, dict):
                continue
            merged = dict(raw_cell)
            merged.pop("candidates", None)
            merged.update(raw_candidate)
            merged["_cell"] = raw_cell
            candidates.append(merged)
    return valid_cells, candidates


def _decision_map(qa: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for decision in _as_list(qa.get("decisions")):
        if isinstance(decision, dict) and decision.get("candidate_id") is not None:
            result[str(decision["candidate_id"])] = decision
    return result


def _accepted_ids(qa: Mapping[str, Any], decisions: dict[str, dict[str, Any]]) -> set[str]:
    explicit = _unique_nonempty(_as_list(qa.get("accepted_candidate_ids")))
    if explicit:
        return explicit
    return {i for i, d in decisions.items() if d.get("status") == "pass"}


def _normalize_artifact_keys(artifacts: Mapping[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in artifacts.items():
        name = ARTIFACT_FILES.get(key, key)
        out[name] = value.model_dump(mode="json") if isinstance(value, BaseModel) else value
    return out


def _validate_envelopes(artifacts: dict[str, Any], checks: _Checks) -> None:
    hashes: dict[str, str] = {}
    panel = artifacts.get("panel.yaml")
    provisional = isinstance(panel, dict) and panel.get("status") == "provisional_directional"
    for name in MACHINE_ARTIFACTS:
        value = artifacts.get(name)
        if not isinstance(value, dict):
            continue
        missing = [
            key
            for key in (
                "schema_version",
                "artifact_id",
                "created_at",
                "created_by",
                "source_manifest_hash",
                "warnings",
            )
            if key not in value
        ]
        checks.add(f"envelope:{name}", not missing, missing or "complete")
        if missing:
            continue
        checks.add(
            f"schema_version:{name}",
            value.get("schema_version") == "1.0.0",
            value.get("schema_version"),
        )
        checks.add(
            f"created_at:{name}",
            isinstance(value.get("created_at"), str)
            and bool(RFC3339_RE.match(value["created_at"])),
            value.get("created_at"),
        )
        source_hash = value.get("source_manifest_hash")
        hash_valid = is_real_hash(source_hash)
        provisional_null = provisional and source_hash is None
        checks.add(
            f"source_hash_shape:{name}",
            hash_valid or provisional_null,
            source_hash
            if not provisional_null
            else "null; permitted provisionally and required before freeze",
            severity="warning" if provisional_null else "error",
        )
        if provisional_null:
            warnings = value.get("warnings")
            checks.add(
                f"source_hash_warning:{name}",
                isinstance(warnings, list) and any("hash" in str(w).casefold() for w in warnings),
                warnings,
            )
        checks.add(
            f"warnings_array:{name}",
            isinstance(value.get("warnings"), list),
            type(value.get("warnings")).__name__,
        )
        if isinstance(value.get("source_manifest_hash"), str):
            hashes[name] = value["source_manifest_hash"]
    distinct = sorted(set(hashes.values()))
    checks.add(
        "source_manifest_hash_consistent",
        len(distinct) <= 1,
        {"distinct_hashes": distinct, "artifacts": hashes},
    )


def _validate_source_manifest(artifacts: dict[str, Any], checks: _Checks) -> set[str]:
    manifest = artifacts.get("source_manifest.json")
    sources = manifest.get("sources") if isinstance(manifest, dict) else None
    if not isinstance(sources, list):
        checks.add("sources_array", False, "source_manifest.sources is not an array")
        return set()
    declared = manifest.get("source_manifest_hash")
    if is_real_hash(declared):
        computed = canonical_hash(sources)
        checks.add(
            "source_manifest_hash_content",
            declared == computed,
            {"declared": declared, "computed": computed},
        )
    source_map: dict[str, dict[str, Any]] = {}
    bad: list[str] = []
    for index, source in enumerate(sources):
        if not isinstance(source, dict) or not source.get("source_id"):
            bad.append(f"index {index}: missing source_id")
            continue
        ident = str(source["source_id"])
        if ident in source_map:
            bad.append(f"duplicate {ident}")
        source_map[ident] = source
        permission = source.get("permission")
        if permission not in {"public", "user_authorized", "generated"}:
            bad.append(f"{ident}: invalid permission")
        if source.get("evidence_grade") not in ENUMS["evidence_grade"]:
            bad.append(f"{ident}: invalid evidence_grade")
        if source.get("source_class") not in {
            "company_asserted",
            "buyer_behavior",
            "independent",
            "search_proxy",
            "llm_hypothesis",
        }:
            bad.append(f"{ident}: invalid source_class")
        if permission == "generated":
            if (
                source.get("source_class") != "llm_hypothesis"
                or source.get("evidence_grade") != "D"
                or source.get("url") is not None
            ):
                bad.append(f"{ident}: generated sources require llm_hypothesis, grade D, url null")
        elif not source.get("url"):
            bad.append(f"{ident}: evidence source missing URL/locator")
        if not source.get("span") or not source.get("span_locator"):
            bad.append(f"{ident}: missing short evidence span/locator")
    checks.add("source_records_valid", not bad, bad or f"{len(source_map)} sources")
    counts = collections.Counter(str(s.get("source_class")) for s in source_map.values())
    checks.add(
        "source_mix_target", counts["company_asserted"] >= 1, dict(counts), severity="warning"
    )
    checks.add(
        "source_mix_independent", counts["independent"] >= 2, dict(counts), severity="warning"
    )
    checks.add(
        "source_mix_buyer_language",
        counts["buyer_behavior"] + counts["search_proxy"] >= 3,
        dict(counts),
        severity="warning",
    )
    return set(source_map)


def _validate_graph(
    artifacts: dict[str, Any], source_ids: set[str], checks: _Checks
) -> dict[str, Any]:
    icp = artifacts.get("icp_hypotheses.json", {})
    jobs_art = artifacts.get("buyer_jobs.json", {})
    architecture = artifacts.get("prompt_architecture.json", {})
    universe = artifacts.get("prompt_universe.json", {})
    qa = artifacts.get("prompt_qa.json", {})
    if not all(isinstance(i, dict) for i in (icp, jobs_art, architecture, universe, qa)):
        return {}

    icps = [i for i in _as_list(icp.get("icps")) if isinstance(i, dict)]
    jobs = [i for i in _as_list(jobs_art.get("jobs")) if isinstance(i, dict)]
    specs = [i for i in _as_list(architecture.get("cells")) if isinstance(i, dict)]
    cells, candidates = flatten_universe(universe)
    decisions = _decision_map(qa)
    accepted = _accepted_ids(qa, decisions)

    id_groups = {
        "icp_id": [i.get("icp_id") for i in icps],
        "job_id": [i.get("job_id") for i in jobs],
        "cell_spec_id": [i.get("cell_spec_id") for i in specs],
        "canonical_cell_id": [i.get("canonical_cell_id") for i in cells],
        "candidate_id": [i.get("candidate_id") for i in candidates],
    }
    id_sets: dict[str, set[str]] = {}
    for key, values in id_groups.items():
        present = [str(v) for v in values if v is not None and str(v)]
        id_sets[key] = set(present)
        checks.add(
            f"unique:{key}",
            len(present) == len(set(present)) and len(present) == len(values),
            {"count": len(present), "unique": len(set(present)), "records": len(values)},
        )

    all_refs: set[str] = set()
    for name, artifact in artifacts.items():
        if name != "source_manifest.json" and isinstance(artifact, (dict, list)):
            all_refs |= _recursive_source_refs(artifact)
    unresolved = sorted(all_refs - source_ids)
    checks.add(
        "source_references_resolve", not unresolved, unresolved or f"{len(all_refs)} references"
    )

    job_icp_refs = _unique_nonempty(v for job in jobs for v in _as_list(job.get("icp_ids")))
    checks.add(
        "job_icp_references_resolve",
        job_icp_refs <= id_sets["icp_id"],
        sorted(job_icp_refs - id_sets["icp_id"]) or "resolved",
    )
    spec_job_refs = _unique_nonempty(s.get("job_id") for s in specs)
    checks.add(
        "architecture_job_references_resolve",
        spec_job_refs <= id_sets["job_id"],
        sorted(spec_job_refs - id_sets["job_id"]) or "resolved",
    )
    cell_spec_refs = _unique_nonempty(c.get("cell_spec_id") for c in cells)
    cell_job_refs = _unique_nonempty(c.get("job_id") for c in cells)
    checks.add(
        "universe_spec_references_resolve",
        cell_spec_refs <= id_sets["cell_spec_id"],
        sorted(cell_spec_refs - id_sets["cell_spec_id"]) or "resolved",
    )
    checks.add(
        "universe_job_references_resolve",
        cell_job_refs <= id_sets["job_id"],
        sorted(cell_job_refs - id_sets["job_id"]) or "resolved",
    )

    candidate_ids = id_sets["candidate_id"]
    checks.add(
        "qa_one_decision_per_candidate",
        set(decisions) == candidate_ids,
        {
            "missing": sorted(candidate_ids - set(decisions)),
            "unknown": sorted(set(decisions) - candidate_ids),
        },
    )
    checks.add(
        "qa_accepted_ids_resolve",
        accepted <= candidate_ids,
        sorted(accepted - candidate_ids) or "resolved",
    )
    invalid_accepts = sorted(i for i in accepted if decisions.get(i, {}).get("status") != "pass")
    checks.add("qa_accepted_are_pass", not invalid_accepts, invalid_accepts or "all pass")
    counts = qa.get("counts")
    if counts is not None:
        status_counts = collections.Counter(
            str(d.get("status"))
            for d in decisions.values()
            if d.get("status") in {"pass", "revise", "quarantine", "reject"}
        )
        expected = {
            "total_candidates": len(decisions),
            "pass": status_counts["pass"],
            "revise": status_counts["revise"],
            "quarantine": status_counts["quarantine"],
            "reject": status_counts["reject"],
            "accepted": len(accepted),
        }
        if isinstance(counts, dict):
            mismatches: dict[str, Any] = {
                k: {"expected": v, "actual": counts.get(k)}
                for k, v in expected.items()
                if counts.get(k) != v
            }
        else:
            mismatches = {"shape": type(counts).__name__}
        checks.add(
            "qa_counts_reconcile",
            isinstance(counts, dict) and not mismatches,
            mismatches or expected,
        )
    checks.add(
        "qa_baseline_blinded",
        qa.get("baseline_fields_blinded") is True,
        qa.get("baseline_fields_blinded"),
    )

    required_cell_fields = {
        "canonical_cell_id",
        "cell_spec_id",
        "job_id",
        "icp_ids",
        "information_act",
        "journey_state",
        "funnel",
        "proximity_band",
        "aided_status",
        "campaign_exposed",
        "persona_id",
        "locale",
        "language",
        "material_constraints",
        "expected_answer_kind",
        "turn_form",
        "lane_eligibility",
        "partition",
        "evidence_grade",
        "reason_source_ids",
        "candidates",
    }
    missing_cell = {
        str(c.get("canonical_cell_id", f"index-{i}")): sorted(required_cell_fields - set(c))
        for i, c in enumerate(cells)
        if required_cell_fields - set(c)
    }
    checks.add("canonical_cell_fields_complete", not missing_cell, missing_cell or "complete")

    required_candidate_fields = {
        "candidate_id",
        "variant_role",
        "text",
        "transformation",
        "source_ids",
        "evidence_grade",
        "locale_review_status",
        "generation_provenance",
    }
    missing_cand = {
        str(c.get("candidate_id", f"index-{i}")): sorted(required_candidate_fields - set(c))
        for i, c in enumerate(candidates)
        if required_candidate_fields - set(c)
    }
    checks.add("candidate_fields_complete", not missing_cand, missing_cand or "complete")

    enum_errors: list[str] = []
    for record in candidates:
        ident = str(record.get("candidate_id"))
        for field in (
            "information_act",
            "journey_state",
            "funnel",
            "proximity_band",
            "aided_status",
            "partition",
            "transformation",
            "evidence_grade",
        ):
            if record.get(field) not in ENUMS[field]:
                enum_errors.append(f"{ident}: {field}={record.get(field)!r}")
        lanes = _as_list(record.get("lane_eligibility"))
        bad_lanes = [lane for lane in lanes if lane not in ENUMS["lane"]]
        if bad_lanes:
            enum_errors.append(f"{ident}: invalid lanes {bad_lanes}")
    checks.add("prompt_enums_valid", not enum_errors, enum_errors or "valid")

    consistency: list[str] = []
    for record in candidates:
        ident = str(record.get("candidate_id"))
        band = record.get("proximity_band")
        aided = record.get("aided_status")
        partition = record.get("partition")
        if band == "B0_direct_brand_product" and aided != "target_aided":
            consistency.append(f"{ident}: B0 must be target_aided")
        if aided == "target_aided" and band not in {
            "B0_direct_brand_product",
            "B1_comparison_purchase",
        }:
            consistency.append(f"{ident}: target_aided outside B0/B1")
        if aided == "competitor_aided" and band != "B1_comparison_purchase":
            consistency.append(f"{ident}: competitor_aided outside B1")
        if aided == "category_aided" and band != "B2_category":
            consistency.append(f"{ident}: category_aided outside B2")
        if aided == "target_aided" and partition != "aided":
            consistency.append(f"{ident}: target_aided must use aided partition")
        if record.get("campaign_exposed") is True and partition == "core":
            consistency.append(f"{ident}: campaign-exposed prompt in core")
    checks.add("band_aided_partition_consistent", not consistency, consistency or "consistent")

    accepted_records = [c for c in candidates if str(c.get("candidate_id")) in accepted]
    normalized: dict[str, list[str]] = collections.defaultdict(list)
    for record in accepted_records:
        text = record.get("text")
        if isinstance(text, str):
            normalized[_grader_normalize(text)].append(str(record.get("candidate_id")))
    duplicates = {t: ids for t, ids in normalized.items() if t and len(ids) > 1}
    checks.add("accepted_prompts_exact_unique", not duplicates, duplicates or "unique")

    grade_d_core = []
    for record in accepted_records:
        if record.get("partition") != "core" or record.get("evidence_grade") != "D":
            continue
        promotion = record.get("promotion")
        promoted = record.get("promoted") is True or (
            isinstance(promotion, dict) and promotion.get("approved") is True
        )
        if not promoted:
            grade_d_core.append(str(record.get("candidate_id")))
    checks.add("no_unpromoted_grade_d_core", not grade_d_core, grade_d_core or "none")

    return {
        "cells": cells,
        "candidates": candidates,
        "accepted_ids": accepted,
        "accepted": accepted_records,
        "decisions": decisions,
    }


def contamination_terms(register: Mapping[str, Any]) -> dict[str, list[str]]:
    """Their grader's grouping: target (all but campaign), campaign, competitor."""
    target = register.get("target_terms")
    target = target if isinstance(target, dict) else {}
    result: dict[str, list[str]] = {
        "target": [],
        "campaign": [str(i) for i in _as_list(target.get("campaign_terms")) if str(i)],
        "competitor": [str(i) for i in _as_list(register.get("competitor_terms")) if str(i)],
    }
    for key, values in target.items():
        if key != "campaign_terms":
            result["target"].extend(str(i) for i in _as_list(values) if str(i))
    return result


def _validate_contamination(
    artifacts: dict[str, Any], graph: dict[str, Any], checks: _Checks
) -> None:
    register = artifacts.get("contamination_register.yaml")
    if not isinstance(register, dict):
        return
    terms = contamination_terms(register)
    leaks: list[str] = []
    for record in graph.get("accepted", []):
        ident = str(record.get("candidate_id"))
        text = str(record.get("text", ""))
        aided = record.get("aided_status")
        partition = record.get("partition")
        if aided != "target_aided":
            for term in terms["target"]:
                if term_in_text(term, text):
                    leaks.append(f"{ident}: target term {term!r} outside target_aided")
        competitor_allowed = (
            aided == "target_aided"
            and record.get("proximity_band") == "B1_comparison_purchase"
            and partition == "aided"
        )
        if aided != "competitor_aided" and not competitor_allowed:
            for term in terms["competitor"]:
                if term_in_text(term, text):
                    leaks.append(f"{ident}: competitor term {term!r} outside competitor_aided")
        if record.get("campaign_exposed") is not True:
            for term in terms["campaign"]:
                if term_in_text(term, text):
                    leaks.append(f"{ident}: campaign term {term!r} without campaign_exposed")
        if aided == "unaided" and partition == "core":
            for term in terms["target"] + terms["campaign"] + terms["competitor"]:
                if term_in_text(term, text):
                    leaks.append(f"{ident}: unaided-core leak {term!r}")
    checks.add("accepted_prompt_contamination_zero", not leaks, leaks or "zero leaks")

    brief = artifacts.get("blind_design_brief.json")
    serialized = json.dumps(brief, ensure_ascii=False) if isinstance(brief, dict) else ""
    brief_leaks = sorted(
        {t for t in terms["target"] + terms["campaign"] if term_in_text(t, serialized)}
    )
    checks.add("blind_brief_target_free", not brief_leaks, brief_leaks or "target-free")


def _validate_panel(artifacts: dict[str, Any], graph: dict[str, Any], checks: _Checks) -> None:
    panel = artifacts.get("panel.yaml")
    if not isinstance(panel, dict):
        return
    weight = panel.get("weight", panel.get("weights"))
    weight_ok = isinstance(weight, dict) and "exposure" in weight and "priority" in weight
    checks.add("weights_exposure_priority_separate", weight_ok, weight if weight_ok else "missing")

    selected = _unique_nonempty(
        _recursive_values(panel, {"selected_candidate_ids", "candidate_ids", "selected_candidates"})
    )
    if not selected:
        selected = _unique_nonempty(_recursive_values(panel, {"candidate_id"}))
    checks.add("panel_selected_candidates_present", bool(selected), sorted(selected) or "none")
    accepted = set(graph.get("accepted_ids", set()))
    checks.add(
        "panel_selected_candidates_qa_approved",
        bool(selected) and selected <= accepted,
        sorted(selected - accepted) if selected else "none selected",
    )

    report = artifacts.get("panel_report.md")
    tracking = artifacts.get("tracking_plan.md")
    joined = "\n".join(t for t in (report, tracking) if isinstance(t, str))
    has_phrase = "conditional on this panel" in joined.casefold()
    checks.add(
        "conditional_panel_language",
        has_phrase,
        "phrase present" if has_phrase else "phrase missing",
    )
    missing_ids = sorted(i for i in accepted if isinstance(report, str) and i not in report)
    checks.add(
        "report_lists_accepted_prompts",
        not missing_ids,
        missing_ids or f"{len(accepted)} accepted IDs present",
    )
    missing_text = sorted(
        str(r.get("candidate_id"))
        for r in graph.get("accepted", [])
        if isinstance(report, str)
        and isinstance(r.get("text"), str)
        and r["text"] not in report
        and r["text"].replace("|", r"\|") not in report
    )
    checks.add(
        "report_lists_exact_prompt_text",
        not missing_text,
        missing_text or f"{len(accepted)} exact prompt texts present",
    )

    status = panel.get("status")
    approvals = panel.get("approvals")
    pending = False
    if isinstance(approvals, list):
        pending = any(isinstance(i, dict) and i.get("status") == "pending" for i in approvals)
    elif isinstance(approvals, dict):
        pending = any(
            v == "pending" or (isinstance(v, dict) and v.get("status") == "pending")
            for v in approvals.values()
        )
    checks.add(
        "pending_gates_not_frozen",
        not pending or status in {"provisional_directional", "provisional"},
        {"status": status, "approvals_pending": pending},
    )


def validate_schemas(artifacts: Mapping[str, Any]) -> list[CheckResult]:
    """Strict ``schema:<file>`` checks against our contract models (extra="forbid")."""
    named = _normalize_artifact_keys(artifacts)
    out: list[CheckResult] = []
    for name in REQUIRED_ARTIFACTS:
        value = named.get(name)
        if name.endswith(".md"):
            ok = isinstance(value, str) and bool(value.strip())
            out.append(
                CheckResult(
                    id=f"schema:{name}",
                    passed=ok,
                    evidence="markdown text" if ok else "missing or not text",
                )
            )
            continue
        model = ARTIFACT_MODELS[name]
        try:
            model.model_validate(value)
        except ValidationError as exc:
            errors = [
                f"{'.'.join(str(p) for p in e['loc'])}: {e['msg']}" for e in exc.errors()[:25]
            ]
            out.append(
                CheckResult(
                    id=f"schema:{name}",
                    passed=False,
                    evidence={"error_count": exc.error_count(), "errors": errors},
                )
            )
        else:
            out.append(CheckResult(id=f"schema:{name}", passed=True, evidence="valid"))
    return out


def validate_artifacts(
    artifacts: Mapping[str, Any],
    *,
    parse_errors: Sequence[str] | None = None,
    strict_schema: bool = True,
) -> list[CheckResult]:
    """T1. Every structural check their grade.py runs on the fourteen artifacts.

    ``artifacts`` maps artifact name (``panel`` or ``panel.yaml``) → parsed
    content: dicts for the twelve machine artifacts, strings for
    ``panel_report`` and ``tracking_plan``. ``parse_errors`` carries any
    upstream JSON/YAML parse failure (their ``required_artifacts_parse``).
    Check IDs are theirs, verbatim; ``strict_schema`` appends our
    ``schema:<file>`` checks after them.
    """
    named = _normalize_artifact_keys(artifacts)
    checks = _Checks()
    errors = list(parse_errors or [])
    for name in REQUIRED_ARTIFACTS:
        value = named.get(name)
        if value is None or (isinstance(value, str) and not value):
            errors.append(f"missing or empty {name}")
    checks.add(
        "required_artifacts_parse",
        not errors,
        errors or f"{len(REQUIRED_ARTIFACTS)} artifacts",
        severity="critical",
    )
    if not errors:
        _validate_envelopes(named, checks)
        source_ids = _validate_source_manifest(named, checks)
        graph = _validate_graph(named, source_ids, checks)
        _validate_contamination(named, graph, checks)
        _validate_panel(named, graph, checks)
    results = checks.items
    if strict_schema:
        results = results + validate_schemas(named)
    return results


# ---------------------------------------------------------------------------
# T3 — charter and register
# ---------------------------------------------------------------------------


#: T4/T5 near-miss spelling defaults (knobs ``fuzzy_min_token_length`` / ``fuzzy_ratio``).
FUZZY_MIN_TOKEN_LENGTH = 7
FUZZY_RATIO = 0.86
#: T7 near-duplicate nomination defaults (knobs ``similarity_*_threshold``).
SIMILARITY_JACCARD_THRESHOLD = 0.6
SIMILARITY_CHAR3_THRESHOLD = 0.85
SIMILARITY_EMBEDDING_THRESHOLD = 0.92


class FuzzyMatch(_Strict):
    """How close a long single-token spelling must be to count as a near miss (T4/T5).

    The host passes the platform knobs in; the defaults are the fallback values.
    """

    min_token_length: int = Field(default=FUZZY_MIN_TOKEN_LENGTH, ge=3, le=40)
    ratio: float = Field(default=FUZZY_RATIO, gt=0, le=1)


class DesignKnobs(_Strict):
    """The ``seo.ai_visibility`` knobs (BUILD-CONTRACT defaults)."""

    tier: Literal["diagnostic", "standard", "research", "campaign"] = "diagnostic"
    variants_per_slot: int = 2
    repeats_per_wave: int = 3
    engines: list[str] = Field(
        default_factory=lambda: ["chat_gpt", "claude", "gemini", "perplexity"]
    )
    lanes: list[Lane] = Field(default_factory=lambda: ["retrieval", "closed_model"])
    cadence_days: int = 7
    gate_wait_hours: int = 72
    min_cells_for_rate: int = 20
    bootstrap_draws: int = 2000
    analyst_sampling: Literal["first_repeat", "all_repeats", "none"] = "first_repeat"
    evidence_intake: str = "monthly"
    panel_review: str = "quarterly"
    # --- design tuning (knobs since 2026-09-27; the defaults below are the fallback the host
    # announces when a knob row is missing, and the values the pure tests use) ---
    #: T10's allocation table, keyed by tier code (platform-locked knob ``tiers``).
    tiers: dict[str, TierSpec] = Field(default_factory=lambda: dict(TIERS))
    #: Recommended unprompted shares, percent (org knob ``share_bands``). Advisory: a share
    #: outside its band is a notice, never a refusal.
    share_bands: dict[str, tuple[float, float]] = Field(default_factory=lambda: dict(SHARE_BANDS))
    #: Per-answer price when the org has no measured history (knob ``fallback_cost_per_call_usd``).
    fallback_cost_per_call_usd: Decimal = FALLBACK_COST_PER_PROMPT_ENGINE
    #: T4/T5 near-miss spelling match (knobs ``fuzzy_min_token_length`` / ``fuzzy_ratio``).
    fuzzy_min_token_length: int = Field(default=FUZZY_MIN_TOKEN_LENGTH, ge=3, le=40)
    fuzzy_ratio: float = Field(default=FUZZY_RATIO, gt=0, le=1)
    #: T7 near-duplicate nomination thresholds (knobs ``similarity_*_threshold``).
    similarity_jaccard_threshold: float = Field(default=SIMILARITY_JACCARD_THRESHOLD, gt=0, le=1)
    similarity_char3_threshold: float = Field(default=SIMILARITY_CHAR3_THRESHOLD, gt=0, le=1)
    similarity_embedding_threshold: float = Field(
        default=SIMILARITY_EMBEDDING_THRESHOLD, gt=0, le=1
    )

    @field_validator("tiers")
    @classmethod
    def _every_tier_defined(cls, value: dict[str, TierSpec]) -> dict[str, TierSpec]:
        missing = sorted(set(get_args(cls.model_fields["tier"].annotation)) - set(value))
        if missing:
            raise ValueError(f"the tier table must define every tier; missing {missing}")
        return value

    @field_validator("share_bands")
    @classmethod
    def _known_bands(cls, value: dict[str, tuple[float, float]]) -> dict[str, tuple[float, float]]:
        unknown = sorted(set(value) - set(SHARE_BANDS))
        if unknown:
            raise ValueError(f"unknown share bands {unknown}; known: {sorted(SHARE_BANDS)}")
        for name, (low, high) in value.items():
            if not 0 <= low <= high <= 100:
                raise ValueError(f"share band {name} must satisfy 0 <= low <= high <= 100")
        return value

    @property
    def fuzzy(self) -> FuzzyMatch:
        """The near-miss matching settings, for the T4/T5 scanners."""
        return FuzzyMatch(min_token_length=self.fuzzy_min_token_length, ratio=self.fuzzy_ratio)


# The knob names — every DesignKnobs field except the tolerant ``__kind`` marker every contract
# object declares (a marker is data, never a setting, so it has no knob row).
DESIGN_KNOB_KEYS: tuple[str, ...] = tuple(n for n in DesignKnobs.model_fields if n != "kind_marker")


LANE_POLICIES: dict[str, str] = {
    "closed_model": (
        "No search, tools, files, retrieval or history; fixed system, model and sampling; "
        "fresh session (DataForSEO web_search: false)"
    ),
    "retrieval": (
        "Web search on; record whether retrieval ran, queries when exposed, and citation "
        "metadata (DataForSEO web_search: true)"
    ),
    "consumer_surface": (
        "Declared clean or account archetype, device, locale and personalization state; "
        "never merged with API rollups"
    ),
    "campaign_experiment": (
        "Pre-registered frozen evergreen, unaided resonance, aided association and matched "
        "unaffected controls"
    ),
}


def build_charter(
    knobs: DesignKnobs,
    *,
    site_name: str,
    artifact_id: str,
    created_by: str,
    created_at: str,
    locales: Sequence[str],
    business_decision: str | None = None,
    target_population: str | None = None,
    products: Sequence[str] = (),
    markets: Sequence[str] = (),
    exclusions: Sequence[str] = (),
    perimeter: Sequence[Mapping[str, Any]] = (),
    source_manifest_hash: str | None = None,
) -> MeasurementCharter:
    """T3. The charter from knobs + site: six estimands, lanes, budgets, perimeter."""
    lanes = list(dict.fromkeys(knobs.lanes))
    estimands = [
        Estimand(
            name=m.metric,
            numerator=m.numerator,
            denominator=m.denominator,
            eligible_partitions=list(m.eligible_partitions),
            eligible_lanes=list(m.eligible_lanes),
            does_not_prove=m.does_not_prove,
        )
        for m in METRICS.values()
    ]
    return MeasurementCharter(
        **make_envelope(
            artifact_id=artifact_id,
            created_by=created_by,
            created_at=created_at,
            source_manifest_hash=source_manifest_hash,
        ),
        business_decision=business_decision
        or f"Decide what this panel can safely monitor about how AI answers treat {site_name}",
        estimands=estimands,
        target_population=target_population
        or f"People asking AI assistants questions that {site_name}'s buyers ask",
        exclusions=list(exclusions),
        products=list(products),
        markets=list(markets),
        locales=list(locales),
        time_horizon=f"weekly waves every {knobs.cadence_days} days; review {knobs.panel_review}",
        surfaces=[f"api:{engine}" for engine in knobs.engines],
        lanes=lanes,
        lane_policies={lane: LANE_POLICIES[lane] for lane in lanes},
        surface_policies={
            f"api:{engine}": {"engine": engine, "provider": "dataforseo"}
            for engine in knobs.engines
        },
        reporting_strata=[
            "partition",
            "lane",
            "aided_status",
            "engine",
            "locale",
            "market_side",
            "wave_id",
        ],
        run_budget={
            "tier": knobs.tier,
            "variants_per_slot": knobs.variants_per_slot,
            "repeats_per_wave": knobs.repeats_per_wave,
            "engines": list(knobs.engines),
            "cadence_days": knobs.cadence_days,
        },
        review_budget={
            "analyst_sampling": knobs.analyst_sampling,
            "evidence_intake": knobs.evidence_intake,
            "panel_review": knobs.panel_review,
        },
        precision_status="pending_variance_pilot",
        perimeter=[PerimeterArea.model_validate(dict(p)) for p in perimeter],
    )


def domain_forms(domain: str) -> list[str]:
    """``https://www.Example.com/x`` → ``["example.com", "www.example.com"]``."""
    host = domain.strip().casefold()
    host = re.sub(r"^[a-z][a-z0-9+.-]*://", "", host)
    host = host.split("/", 1)[0].split("?", 1)[0].split("#", 1)[0]
    host = host.rsplit("@", 1)[-1].split(":", 1)[0].strip(".")
    if not host:
        return []
    bare = host[4:] if host.startswith("www.") else host
    return list(dict.fromkeys([bare, f"www.{bare}"]))


class RegisterIdentity(_Strict):
    """What we already know about the target (brand profile, web.site, competitors)."""

    brand_name: str
    brand_aliases: list[str] = Field(default_factory=list)
    site_name: str | None = None
    domains: list[str] = Field(default_factory=list)
    people: list[str] = Field(default_factory=list)
    products: list[str] = Field(default_factory=list)
    slogans: list[str] = Field(default_factory=list)
    proprietary_categories: list[str] = Field(default_factory=list)
    campaign_terms: list[str] = Field(default_factory=list)
    flattering_claims: list[str] = Field(default_factory=list)
    competitors: list[str] = Field(default_factory=list)


class ProposedTerm(_Strict):
    term: str
    source_id: str


class ProposedRegisterTerms(_Strict):
    """Agent 1's ``proposed_register_terms`` (each term with a source ID)."""

    brands: list[ProposedTerm] = Field(default_factory=list)
    products: list[ProposedTerm] = Field(default_factory=list)
    domains: list[ProposedTerm] = Field(default_factory=list)
    people: list[ProposedTerm] = Field(default_factory=list)
    slogans: list[ProposedTerm] = Field(default_factory=list)
    proprietary_categories: list[ProposedTerm] = Field(default_factory=list)
    campaign_terms: list[ProposedTerm] = Field(default_factory=list)
    flattering_claims: list[ProposedTerm] = Field(default_factory=list)
    competitor_terms: list[ProposedTerm] = Field(default_factory=list)


#: Brand slots may name the target's brands and products (brief T4).
DEFAULT_ALLOWED_EXCEPTIONS: tuple[AllowedException, ...] = (
    AllowedException(
        band="B0_direct_brand_product",
        term_classes=["brands", "products", "domains"],
        aided_status="target_aided",
        partition="aided",
        reason="Brand questions name the supplied alias and stay in the prompted set",
    ),
)


def seed_register(
    identity: RegisterIdentity,
    *,
    artifact_id: str,
    created_by: str,
    created_at: str,
    proposed: ProposedRegisterTerms | None = None,
    source_manifest_hash: str | None = None,
    allowed_exceptions: Sequence[AllowedException] = DEFAULT_ALLOWED_EXCEPTIONS,
) -> ContaminationRegister:
    """T3. Seed the register from identity data, then merge agent 1's proposals."""
    buckets: dict[str, list[str]] = {c: [] for c in ALL_TERM_CLASSES}
    seen: dict[str, set[str]] = {c: set() for c in ALL_TERM_CLASSES}
    provenance: list[TermProvenance] = []

    def add(term_class: str, term: str, source: str) -> None:
        clean = " ".join(unicodedata.normalize("NFKC", term).split())
        key = clean.casefold()
        if not clean or key in seen[term_class]:
            return
        seen[term_class].add(key)
        buckets[term_class].append(clean)
        provenance.append(TermProvenance(term=clean, term_class=term_class, source=source))

    add("brands", identity.brand_name, "identity:brand_name")
    for alias in identity.brand_aliases:
        add("brands", alias, "identity:brand_aliases")
    if identity.site_name:
        add("brands", identity.site_name, "identity:site_name")
    for domain in identity.domains:
        for form in domain_forms(domain):
            add("domains", form, "identity:domain")
    for field, term_class in (
        ("people", "people"),
        ("products", "products"),
        ("slogans", "slogans"),
        ("proprietary_categories", "proprietary_categories"),
        ("campaign_terms", "campaign_terms"),
        ("flattering_claims", "flattering_claims"),
        ("competitors", "competitor_terms"),
    ):
        for term in getattr(identity, field):
            add(term_class, term, f"identity:{field}")
    if proposed is not None:
        for term_class in ALL_TERM_CLASSES:
            for item in getattr(proposed, term_class):
                if term_class == "domains":
                    for form in domain_forms(item.term) or [item.term]:
                        add(term_class, form, f"source:{item.source_id}")
                else:
                    add(term_class, item.term, f"source:{item.source_id}")
    return ContaminationRegister(
        **make_envelope(
            artifact_id=artifact_id,
            created_by=created_by,
            created_at=created_at,
            source_manifest_hash=source_manifest_hash,
        ),
        target_terms=TargetTerms(**{c: buckets[c] for c in TARGET_TERM_CLASSES}),
        competitor_terms=buckets["competitor_terms"],
        allowed_exceptions=list(allowed_exceptions),
        term_provenance=provenance,
    )


def _register_terms_payload(register: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "target_terms": register.get("target_terms") or {},
        "competitor_terms": register.get("competitor_terms") or [],
        "allowed_exceptions": register.get("allowed_exceptions") or [],
    }


def freeze_register(
    register: ContaminationRegister | Mapping[str, Any],
) -> tuple[dict[str, Any], str]:
    """T3. Freeze at Gate 1: hash the terms + exceptions; returns (register, hash)."""
    data = register.model_dump(mode="json") if isinstance(register, BaseModel) else dict(register)
    digest = canonical_hash(_register_terms_payload(data))
    data["frozen_hash"] = digest
    return data, digest


def register_terms(register: Mapping[str, Any] | ContaminationRegister) -> list[dict[str, str]]:
    """Flat ``[{term, term_class}]`` (the Gate 1 card's ``register_terms``)."""
    data = register.model_dump(mode="json") if isinstance(register, BaseModel) else register
    out: list[dict[str, str]] = []
    target = data.get("target_terms") or {}
    for term_class in TARGET_TERM_CLASSES:
        for term in _as_list(target.get(term_class)):
            out.append({"term": str(term), "term_class": term_class})
    for term in _as_list(data.get("competitor_terms")):
        out.append({"term": str(term), "term_class": "competitor_terms"})
    return out


# ---------------------------------------------------------------------------
# T4 — contamination scan
# ---------------------------------------------------------------------------

MatchKind = Literal["token", "compact", "domain", "fuzzy"]
# FUZZY_MIN_TOKEN_LENGTH / FUZZY_RATIO / FuzzyMatch live above DesignKnobs (knob defaults).


def _tokens(value: str) -> list[str]:
    folded = unicodedata.normalize("NFKC", value).casefold()
    return re.findall(r"\w+", folded, flags=re.UNICODE)


class TermHit(_Strict):
    term: str
    term_class: TermClass
    match_kind: MatchKind
    matched_text: str


def _match_term(
    term: str, text_tokens: list[str], term_class: str, fuzzy: FuzzyMatch | None = None
) -> tuple[MatchKind, str] | None:
    fuzzy = fuzzy or FuzzyMatch()
    needle = _tokens(term)
    if not needle or not text_tokens:
        return None
    n = len(needle)
    kind: MatchKind = "domain" if term_class == "domains" else "token"
    for i in range(len(text_tokens) - n + 1):
        if text_tokens[i : i + n] == needle:
            return kind, " ".join(text_tokens[i : i + n])
    compact = "".join(needle)
    if len(compact) >= 4:
        # Token-boundary compact matching ("A.I. Matrx" ~ "AI Matrx" ~ "AIMatrx"):
        # concatenations of WHOLE consecutive tokens only, so "table" never
        # matches inside "injectable" (answer_mentions_target's rule, tightened).
        for i in range(len(text_tokens)):
            joined = ""
            for j in range(i, min(len(text_tokens), i + n + 3)):
                joined += text_tokens[j]
                if joined == compact and (j > i or n > 1):
                    return "compact", " ".join(text_tokens[i : j + 1])
                if len(joined) >= len(compact):
                    break
    if n == 1 and len(compact) >= fuzzy.min_token_length:
        for token in text_tokens:
            if len(token) >= fuzzy.min_token_length - 1 and token != compact:
                ratio = difflib.SequenceMatcher(None, compact, token).ratio()
                if ratio >= fuzzy.ratio:
                    return "fuzzy", token
    return None


def _register_classes(register: Mapping[str, Any] | ContaminationRegister) -> dict[str, list[str]]:
    data = register.model_dump(mode="json") if isinstance(register, BaseModel) else register
    target = data.get("target_terms") or {}
    classes: dict[str, list[str]] = {
        c: [str(t) for t in _as_list(target.get(c)) if str(t).strip()] for c in TARGET_TERM_CLASSES
    }
    classes["competitor_terms"] = [
        str(t) for t in _as_list(data.get("competitor_terms")) if str(t).strip()
    ]
    for domain in list(classes["domains"]):
        for form in domain_forms(domain):
            if form not in classes["domains"]:
                classes["domains"].append(form)
    return classes


def scan_text(
    text: str,
    register: Mapping[str, Any] | ContaminationRegister,
    *,
    fuzzy: FuzzyMatch | None = None,
) -> list[TermHit]:
    """Every register term found in ``text`` (NFKC, casefold, token sequences).

    ``fuzzy`` is the near-miss setting (the host passes the platform knobs).
    """
    text_tokens = _tokens(text or "")
    hits: list[TermHit] = []
    for term_class, terms in _register_classes(register).items():
        for term in terms:
            found = _match_term(term, text_tokens, term_class, fuzzy)
            if found is not None:
                hits.append(
                    TermHit(
                        term=term, term_class=term_class, match_kind=found[0], matched_text=found[1]
                    )
                )
    return hits


class RuleResult(_Strict):
    rule_id: str
    term: str
    term_class: TermClass
    match_kind: MatchKind
    outcome: Literal["fail", "allowed", "review"]
    detail: str


class CandidateScan(_Strict):
    candidate_id: str
    outcome: Literal["pass", "review", "fail"]
    rule_results: list[RuleResult] = Field(default_factory=list)


def _exception_allows(
    record: Mapping[str, Any], term_class: str, exceptions: list[Mapping[str, Any]]
) -> bool:
    for exc in exceptions:
        if exc.get("band") != record.get("proximity_band"):
            continue
        if term_class not in _as_list(exc.get("term_classes")):
            continue
        if exc.get("aided_status") and exc.get("aided_status") != record.get("aided_status"):
            continue
        if exc.get("partition") and exc.get("partition") != record.get("partition"):
            continue
        return True
    return False


def contamination_scan(
    candidates: Iterable[Mapping[str, Any]],
    register: Mapping[str, Any] | ContaminationRegister,
    *,
    fuzzy: FuzzyMatch | None = None,
) -> list[CandidateScan]:
    """T4. ``rule_results`` per candidate.

    Candidates are flat records (a universe candidate merged with its cell —
    see :func:`flatten_universe`). A fuzzy match is ``review`` (a human or QA
    decides), never a fail. Unprompted tracked-set leaks are hard fails no
    exception can excuse. Otherwise the contract's aided rules and the
    register's ``allowed_exceptions`` (by band) decide.
    """
    data = register.model_dump(mode="json") if isinstance(register, BaseModel) else register
    exceptions = [e for e in _as_list(data.get("allowed_exceptions")) if isinstance(e, Mapping)]
    results: list[CandidateScan] = []
    for record in candidates:
        ident = str(record.get("candidate_id"))
        aided = record.get("aided_status")
        partition = record.get("partition")
        rules: list[RuleResult] = []
        for hit in scan_text(str(record.get("text", "")), data, fuzzy=fuzzy):
            cls = hit.term_class
            if hit.match_kind == "fuzzy":
                outcome, rule, detail = (
                    "review",
                    "fuzzy_register_match",
                    "near match on a long token",
                )
            elif aided == "unaided" and partition == "core":
                outcome, rule, detail = (
                    "fail",
                    "unaided_core_leak",
                    "register term in unprompted tracked set",
                )
            elif cls == "campaign_terms":
                allowed = record.get("campaign_exposed") is True
                outcome = "allowed" if allowed else "fail"
                rule, detail = (
                    "campaign_term",
                    (
                        "campaign-exposed prompt"
                        if allowed
                        else "campaign term without campaign_exposed"
                    ),
                )
            elif cls == "competitor_terms":
                allowed = aided == "competitor_aided" or (
                    aided == "target_aided"
                    and record.get("proximity_band") == "B1_comparison_purchase"
                    and partition == "aided"
                )
                allowed = allowed or _exception_allows(record, cls, exceptions)
                outcome = "allowed" if allowed else "fail"
                rule, detail = (
                    "competitor_term",
                    (
                        "competitors-named slot"
                        if allowed
                        else "competitor term outside competitors-named"
                    ),
                )
            else:
                allowed = aided == "target_aided" and (
                    _exception_allows(record, cls, exceptions)
                    or cls in ("brands", "products", "domains")
                )
                outcome = "allowed" if allowed else "fail"
                rule, detail = (
                    "target_term",
                    ("we're-named slot" if allowed else f"target {cls} term outside we're-named"),
                )
            rules.append(
                RuleResult(
                    rule_id=rule,
                    term=hit.term,
                    term_class=cls,
                    match_kind=hit.match_kind,
                    outcome=outcome,
                    detail=detail,
                )
            )
        verdict: Literal["pass", "review", "fail"] = "pass"
        if any(r.outcome == "fail" for r in rules):
            verdict = "fail"
        elif any(r.outcome == "review" for r in rules):
            verdict = "review"
        results.append(CandidateScan(candidate_id=ident, outcome=verdict, rule_results=rules))
    return results


# ---------------------------------------------------------------------------
# T5 — the blinding wall (pure parts)
# ---------------------------------------------------------------------------


class DroppedValue(_Strict):
    field: str
    reason: str
    term_classes: list[str]


class BlindBriefBuild(_Strict):
    brief: BlindDesignBrief
    dropped_fragments: int
    dropped_values: list[DroppedValue] = Field(default_factory=list)
    blind_brief_hash: str


def build_blind_brief(
    buyer_jobs: Mapping[str, Any],
    register: Mapping[str, Any] | ContaminationRegister,
    *,
    artifact_id: str,
    created_by: str,
    created_at: str,
    locales: Sequence[str],
    required_strata: Mapping[str, Any] | None = None,
    approved_job_ids: Iterable[str] | None = None,
    source_manifest_hash: str | None = None,
    fuzzy: FuzzyMatch | None = None,
) -> BlindBriefBuild:
    """T5. Build the writer's brief from a FIELD WHITELIST over approved jobs.

    Only job statements, acts, stages, grades and evidence IDs; anonymized role
    labels; constraints; locales; buyer-language fragments; required strata.
    Every value is scanned against the register (all classes, competitors
    included); a hit drops the value and is counted, never rewritten.
    """
    approved = set(approved_job_ids) if approved_job_ids is not None else None
    dropped: list[DroppedValue] = []
    dropped_fragments = 0

    def clean(field: str, value: str) -> bool:
        hits = scan_text(value, register, fuzzy=fuzzy)
        if hits:
            dropped.append(
                DroppedValue(
                    field=field,
                    reason="register hit",
                    term_classes=sorted({h.term_class for h in hits}),
                )
            )
            return False
        return True

    jobs: list[BriefJob] = []
    roles: dict[str, str] = {}
    constraints: dict[str, str] = {}
    fragments: list[BriefFragment] = []
    for job in _as_list(buyer_jobs.get("jobs")):
        if not isinstance(job, Mapping):
            continue
        job_id = str(job.get("job_id"))
        if approved is not None and job_id not in approved:
            continue
        statement = str(job.get("statement") or "")
        if statement and clean(f"jobs.{job_id}.statement", statement):
            jobs.append(
                BriefJob(
                    job_id=job_id,
                    statement=statement,
                    information_acts=[
                        a
                        for a in _as_list(job.get("information_acts"))
                        if a in ENUMS["information_act"]
                    ],
                    journey_states=[
                        s
                        for s in _as_list(job.get("journey_states"))
                        if s in ENUMS["journey_state"]
                    ],
                    evidence_grade=job.get("evidence_grade")
                    if job.get("evidence_grade") in ENUMS["evidence_grade"]
                    else "D",
                    evidence_ids=sorted(
                        _unique_nonempty(_as_list(job.get("supporting_source_ids")))
                    ),
                )
            )
        for role in _as_list(job.get("roles")):
            label = str(role).strip()
            if label and label.casefold() not in {r.casefold() for r in roles.values()}:
                if clean(f"jobs.{job_id}.roles", label):
                    roles[f"role-{len(roles) + 1:03d}"] = label
        for constraint in _as_list(job.get("constraints")):
            label = str(constraint).strip()
            if label and label.casefold() not in {c.casefold() for c in constraints.values()}:
                if clean(f"jobs.{job_id}.constraints", label):
                    constraints[f"constraint-{len(constraints) + 1:03d}"] = label
        for sample in _as_list(job.get("language_samples")):
            if not isinstance(sample, Mapping) or not sample.get("text"):
                continue
            text = str(sample["text"])
            if not clean(f"jobs.{job_id}.language_samples", text):
                dropped_fragments += 1
                continue
            grade = sample.get("evidence_grade")
            fragments.append(
                BriefFragment(
                    fragment=text,
                    evidence_id=str(sample.get("source_id") or ""),
                    evidence_grade=grade if grade in ENUMS["evidence_grade"] else None,
                    locale=sample.get("locale"),
                )
            )
    brief = BlindDesignBrief(
        **make_envelope(
            artifact_id=artifact_id,
            created_by=created_by,
            created_at=created_at,
            source_manifest_hash=source_manifest_hash,
        ),
        approved_jobs=jobs,
        anonymized_roles=[BriefRole(persona_id=k, label=v) for k, v in roles.items()],
        material_constraints=[
            BriefConstraint(constraint_id=k, label=v) for k, v in constraints.items()
        ],
        locales=list(locales),
        safe_language_fragments=fragments,
        required_strata=dict(required_strata or {}),
        dropped_fragment_count=dropped_fragments,
    )
    return BlindBriefBuild(
        brief=brief,
        dropped_fragments=dropped_fragments,
        dropped_values=dropped,
        blind_brief_hash=canonical_hash(brief.model_dump(mode="json")),
    )


class RenderedBlock(_Strict):
    role: str
    text: str


class RequestScan(_Strict):
    allowed: bool
    request_hash: str
    hits: list[dict[str, Any]] = Field(default_factory=list)


def scan_rendered_request(
    blocks: Sequence[RenderedBlock | Mapping[str, Any] | str],
    register: Mapping[str, Any] | ContaminationRegister,
    *,
    fuzzy: FuzzyMatch | None = None,
) -> RequestScan:
    """T5. Scan the fully rendered unaided request; any hit → refuse (allowed False).

    ``blocks`` are the request exactly as the provider receives it (system,
    user, every context block). ``request_hash`` is recorded either way.
    """
    normalized: list[dict[str, str]] = []
    for index, block in enumerate(blocks):
        if isinstance(block, str):
            normalized.append({"role": f"block-{index}", "text": block})
        elif isinstance(block, RenderedBlock):
            normalized.append(block.model_dump())
        else:
            normalized.append(
                {
                    "role": str(block.get("role", f"block-{index}")),
                    "text": str(block.get("text", "")),
                }
            )
    hits: list[dict[str, Any]] = []
    for index, block in enumerate(normalized):
        for hit in scan_text(block["text"], register, fuzzy=fuzzy):
            hits.append({"block": index, "role": block["role"], **hit.model_dump()})
    return RequestScan(allowed=not hits, request_hash=canonical_hash(normalized), hits=hits)


def scan_output(
    universe_or_candidates: Mapping[str, Any] | Iterable[Mapping[str, Any]],
    register: Mapping[str, Any] | ContaminationRegister,
    *,
    unaided_only: bool = True,
    fuzzy: FuzzyMatch | None = None,
) -> dict[str, list[TermHit]]:
    """T5. Scan writer output; returns candidate_id → hits (only those with hits)."""
    if isinstance(universe_or_candidates, Mapping):
        _, records = flatten_universe(universe_or_candidates)
    else:
        records = [dict(r) for r in universe_or_candidates]
    out: dict[str, list[TermHit]] = {}
    for record in records:
        if unaided_only and record.get("aided_status") not in (None, "unaided"):
            continue
        hits = scan_text(str(record.get("text", "")), register, fuzzy=fuzzy)
        if hits:
            out[str(record.get("candidate_id"))] = hits
    return out


def assert_blind_mandate(definition: Mapping[str, Any]) -> list[str]:
    """T5. The unaided writer mandate must have auto context off and no tools."""
    problems: list[str] = []
    if definition.get("auto_context_disabled") is not True:
        problems.append("auto_context_disabled must be true")
    tools = definition.get("tools")
    if tools:
        problems.append(f"writer mandate must declare no tools (has {len(_as_list(tools))})")
    return problems


# ---------------------------------------------------------------------------
# T6 — normalize and dedupe
# ---------------------------------------------------------------------------


def normalize_prompt(text: str) -> str:
    """NFKC, casefold, punctuation strip, whitespace collapse."""
    folded = unicodedata.normalize("NFKC", text or "").casefold()
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]+", " ", folded)).strip()


class NormalizedCandidate(_Strict):
    candidate_id: str
    normalized: str
    exact_hash: str
    token_count: int
    flags: list[Literal["too_short", "too_long", "multi_question"]] = Field(default_factory=list)


class ExactMerge(_Strict):
    action: Literal["merge_exact"] = "merge_exact"
    kept: str
    merged: list[str]
    normalized: str


class DedupeResult(_Strict):
    records: list[NormalizedCandidate]
    merges: list[ExactMerge]
    unique: bool


_GRADE_RANK = {"A": 0, "B": 1, "C": 2, "D": 3}


def normalize_and_dedupe(
    candidates: Iterable[Mapping[str, Any]], *, min_tokens: int = 3, max_tokens: int = 45
) -> DedupeResult:
    """T6. Exact duplicates merged (stronger evidence kept); shape flags are review only."""
    records: list[NormalizedCandidate] = []
    groups: dict[str, list[tuple[int, str, str]]] = collections.defaultdict(list)
    for order, cand in enumerate(candidates):
        text = str(cand.get("text", ""))
        norm = normalize_prompt(text)
        tokens = norm.split()
        flags: list[Any] = []
        if len(tokens) < min_tokens:
            flags.append("too_short")
        if len(tokens) > max_tokens:
            flags.append("too_long")
        if text.count("?") > 1:
            flags.append("multi_question")
        ident = str(cand.get("candidate_id"))
        records.append(
            NormalizedCandidate(
                candidate_id=ident,
                normalized=norm,
                exact_hash=text_hash(norm),
                token_count=len(tokens),
                flags=flags,
            )
        )
        groups[norm].append((order, ident, str(cand.get("evidence_grade") or "D")))
    merges: list[ExactMerge] = []
    for norm, members in groups.items():
        if not norm or len(members) < 2:
            continue
        ranked = sorted(members, key=lambda m: (_GRADE_RANK.get(m[2], 9), m[0]))
        merges.append(
            ExactMerge(kept=ranked[0][1], merged=[m[1] for m in ranked[1:]], normalized=norm)
        )
    return DedupeResult(records=records, merges=merges, unique=not merges)


# ---------------------------------------------------------------------------
# T7 — similarity pairs (nominate only)
# ---------------------------------------------------------------------------


class SimilarPair(_Strict):
    a: str
    b: str
    locale: str | None
    token_jaccard: float
    char3_cosine: float
    embedding_cosine: float | None = None
    nominated_by: list[Literal["token_jaccard", "char3_cosine", "embedding"]]
    action: Literal["nominate"] = "nominate"


class SimilarityResult(_Strict):
    pairs: list[SimilarPair]
    embedding_model: str | None
    thresholds: dict[str, float]


def _char3(text: str) -> collections.Counter[str]:
    padded = f"  {text} "
    return collections.Counter(padded[i : i + 3] for i in range(len(padded) - 2))


def _cosine_counts(a: collections.Counter[str], b: collections.Counter[str]) -> float:
    dot = sum(v * b.get(k, 0) for k, v in a.items())
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def _cosine_vec(a: Sequence[float], b: Sequence[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=False))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


def similarity_pairs(
    candidates: Sequence[Mapping[str, Any]],
    *,
    jaccard_threshold: float = SIMILARITY_JACCARD_THRESHOLD,
    char3_threshold: float = SIMILARITY_CHAR3_THRESHOLD,
    embed: Callable[[list[str]], list[list[float]]] | None = None,
    embedding_model: str | None = None,
    embedding_threshold: float = SIMILARITY_EMBEDDING_THRESHOLD,
) -> SimilarityResult:
    """T7. Near-duplicate NOMINATIONS within a locale; never deletes anything.

    The three thresholds are knobs (``similarity_*_threshold``); the host passes them in.

    ``embed`` is an optional injected callable (one fixed, recorded model
    version → ``embedding_model``); lexical signals always run.
    """
    if embed is not None and not embedding_model:
        raise ValueError("an embedding callable needs its recorded embedding_model version")
    items = [
        (str(c.get("candidate_id")), c.get("locale"), normalize_prompt(str(c.get("text", ""))))
        for c in candidates
    ]
    vectors: list[list[float]] | None = embed([i[2] for i in items]) if embed and items else None
    token_sets = [set(i[2].split()) for i in items]
    grams = [_char3(i[2]) for i in items]
    pairs: list[SimilarPair] = []
    for x in range(len(items)):
        for y in range(x + 1, len(items)):
            if items[x][1] != items[y][1]:
                continue
            union = token_sets[x] | token_sets[y]
            jac = len(token_sets[x] & token_sets[y]) / len(union) if union else 0.0
            cos = _cosine_counts(grams[x], grams[y])
            emb = _cosine_vec(vectors[x], vectors[y]) if vectors is not None else None
            by: list[Any] = []
            if jac >= jaccard_threshold:
                by.append("token_jaccard")
            if cos >= char3_threshold:
                by.append("char3_cosine")
            if emb is not None and emb >= embedding_threshold:
                by.append("embedding")
            if by:
                pairs.append(
                    SimilarPair(
                        a=items[x][0],
                        b=items[y][0],
                        locale=items[x][1],
                        token_jaccard=round(jac, 4),
                        char3_cosine=round(cos, 4),
                        embedding_cosine=round(emb, 4) if emb is not None else None,
                        nominated_by=by,
                    )
                )
    return SimilarityResult(
        pairs=pairs,
        embedding_model=embedding_model if embed else None,
        thresholds={
            "token_jaccard": jaccard_threshold,
            "char3_cosine": char3_threshold,
            "embedding": embedding_threshold,
        },
    )


# ---------------------------------------------------------------------------
# T8 — reconcile QA
# ---------------------------------------------------------------------------


class QAReconcile(_Strict):
    valid: bool
    errors: list[str]
    qa: dict[str, Any]


def reconcile_qa(
    qa: Mapping[str, Any],
    universe: Mapping[str, Any],
    *,
    baseline_fields_blinded: bool | None = None,
) -> QAReconcile:
    """T8. Code writes ``accepted_candidate_ids`` and ``counts``; the model never does.

    Exactly one decision per universe candidate, no unknown IDs, no duplicate
    decisions, valid statuses. If the model supplied its own accepted IDs or
    counts and they disagree with the derived ones, the output is INVALID
    (never a warning). The returned ``qa`` carries the derived values.
    """
    _, candidates = flatten_universe(universe)
    order = [str(c.get("candidate_id")) for c in candidates]
    universe_ids = set(order)
    errors: list[str] = []
    seen: dict[str, dict[str, Any]] = {}
    for decision in _as_list(qa.get("decisions")):
        if not isinstance(decision, Mapping) or decision.get("candidate_id") is None:
            errors.append("decision without candidate_id")
            continue
        ident = str(decision["candidate_id"])
        if ident in seen:
            errors.append(f"duplicate decision for {ident}")
        if decision.get("status") not in {"pass", "revise", "quarantine", "reject"}:
            errors.append(f"{ident}: invalid status {decision.get('status')!r}")
        seen[ident] = dict(decision)
    missing = [i for i in order if i not in seen]
    unknown = sorted(set(seen) - universe_ids)
    if missing:
        errors.append(f"missing decisions: {missing}")
    if unknown:
        errors.append(f"unknown candidate ids: {unknown}")
    accepted = [i for i in order if seen.get(i, {}).get("status") == "pass"]
    status_counts = collections.Counter(d.get("status") for d in seen.values())
    counts = {
        "total_candidates": len(seen),
        "pass": status_counts["pass"],
        "revise": status_counts["revise"],
        "quarantine": status_counts["quarantine"],
        "reject": status_counts["reject"],
        "accepted": len(accepted),
    }
    supplied_ids = qa.get("accepted_candidate_ids")
    if supplied_ids is not None and set(map(str, _as_list(supplied_ids))) != set(accepted):
        errors.append("accepted_candidate_ids disagree with the pass decisions")
    supplied_counts = qa.get("counts")
    if supplied_counts is not None and supplied_counts != counts:
        errors.append("counts disagree with the decision array")
    out = dict(qa)
    out["accepted_candidate_ids"] = accepted
    out["counts"] = counts
    if baseline_fields_blinded is not None:
        out["baseline_fields_blinded"] = baseline_fields_blinded
    return QAReconcile(valid=not errors, errors=errors, qa=out)


# ---------------------------------------------------------------------------
# T9 — coverage matrix
# ---------------------------------------------------------------------------

SINGLE_AXES = (
    "proximity_band",
    "aided_status",
    "job_id",
    "information_act",
    "journey_state",
    "persona_id",
    "locale",
    "partition",
    "evidence_grade",
)
MULTI_AXES = ("lane_eligibility",)


class AxisCounts(_Strict):
    axis: str
    additive: bool
    counts: dict[str, int]
    total: int
    sums_to_total: bool | None


class PerimeterResult(_Strict):
    area: str
    covered: bool
    cell_ids: list[str] = Field(default_factory=list)
    waiver: str | None = None


class CoverageMatrix(_Strict):
    total_cells: int
    total_candidates: int
    accepted_candidates: int | None
    axes: list[AxisCounts]
    perimeter: list[PerimeterResult]
    perimeter_complete: bool
    market_issues: list[str]


def coverage_matrix(
    universe: Mapping[str, Any],
    *,
    accepted_ids: Iterable[str] | None = None,
    perimeter: Sequence[Mapping[str, Any]] = (),
    review_by: Mapping[str, str] | None = None,
) -> CoverageMatrix:
    """T9. Every count every document prints, from the canonical-cell array.

    Single-valued axes sum to the cell total (checked); multi-valued axes are
    labeled non-additive. Every perimeter area maps to a slot or a waiver.
    Market (B5) slots need evidence and a review-by date (cell ``review_by``
    or the ``review_by`` map keyed by canonical_cell_id).
    """
    cells, candidates = flatten_universe(universe)
    accepted = set(accepted_ids) if accepted_ids is not None else None
    if accepted is not None:
        keep = {
            str(c.get("canonical_cell_id"))
            for c in candidates
            if str(c.get("candidate_id")) in accepted
        }
        cells = [c for c in cells if str(c.get("canonical_cell_id")) in keep]
    total = len(cells)
    axes: list[AxisCounts] = []
    for axis in SINGLE_AXES:
        counts = collections.Counter(str(c.get(axis)) for c in cells)
        axes.append(
            AxisCounts(
                axis=axis,
                additive=True,
                counts=dict(sorted(counts.items())),
                total=total,
                sums_to_total=sum(counts.values()) == total,
            )
        )
    for axis in MULTI_AXES:
        counts = collections.Counter(str(v) for c in cells for v in _as_list(c.get(axis)))
        axes.append(
            AxisCounts(
                axis=axis,
                additive=False,
                counts=dict(sorted(counts.items())),
                total=total,
                sums_to_total=None,
            )
        )
    cell_ids = {str(c.get("canonical_cell_id")) for c in cells}
    cells_by_icp: dict[str, set[str]] = collections.defaultdict(set)
    for c in cells:
        for icp in _as_list(c.get("icp_ids")):
            cells_by_icp[str(icp)].add(str(c.get("canonical_cell_id")))
    results: list[PerimeterResult] = []
    for area in perimeter:
        refs = {str(i) for i in _as_list(area.get("canonical_cell_ids"))} & cell_ids
        for icp in _as_list(area.get("covered_by")):
            refs |= cells_by_icp.get(str(icp), set())
        waiver = area.get("waiver")
        results.append(
            PerimeterResult(
                area=str(area.get("area")),
                covered=bool(refs) or bool(waiver),
                cell_ids=sorted(refs),
                waiver=waiver,
            )
        )
    dates = review_by or {}
    market: list[str] = []
    for c in cells:
        if c.get("proximity_band") != "B5_broad_discovery_story":
            continue
        ident = str(c.get("canonical_cell_id"))
        if not _as_list(c.get("reason_source_ids")):
            market.append(f"{ident}: Market slot without evidence")
        if not (c.get("review_by") or dates.get(ident)):
            market.append(f"{ident}: Market slot without a review-by date")
    return CoverageMatrix(
        total_cells=total,
        total_candidates=len(candidates),
        accepted_candidates=(
            sum(1 for c in candidates if str(c.get("candidate_id")) in accepted)
            if accepted is not None
            else None
        ),
        axes=axes,
        perimeter=results,
        perimeter_complete=all(r.covered for r in results),
        market_issues=market,
    )


# ---------------------------------------------------------------------------
# T10 — allocation and wave price
# ---------------------------------------------------------------------------


class TierSpec(_Strict):
    tier: str
    unaided_slots: tuple[int, int]
    variants: tuple[int, int]
    repeats: int | None
    control_slots: tuple[int, int] | None = None
    note: str


#: Brief 6's starting allocation table.
TIERS: dict[str, TierSpec] = {
    "diagnostic": TierSpec(
        tier="diagnostic",
        unaided_slots=(30, 48),
        variants=(2, 2),
        repeats=3,
        note="plus deeper tripwires",
    ),
    "standard": TierSpec(
        tier="standard",
        unaided_slots=(60, 120),
        variants=(2, 2),
        repeats=3,
        note="5-8 repeats for unstable slots",
    ),
    "research": TierSpec(
        tier="research",
        unaided_slots=(200, 400),
        variants=(1, 2),
        repeats=None,
        note="repeats set by the variance pilot",
    ),
    "campaign": TierSpec(
        tier="campaign",
        unaided_slots=(24, 40),
        variants=(1, 2),
        repeats=None,
        control_slots=(24, 40),
        note="treatment plus matched control; repeats from the pilot",
    ),
}
UNAIDED_PARTITIONS = ("core", "rotating", "sentinel", "control")
API_LANES = ("closed_model", "retrieval")
#: Recommended unprompted shares (brief 6): tracked 70-80%, tripwire + check 5-10%.
SHARE_BANDS = {"core": (70.0, 80.0), "sentinel+control": (5.0, 10.0), "rotating": (10.0, 25.0)}
# TIERS / SHARE_BANDS are the defaults of the ``tiers`` / ``share_bands`` knobs; resolve
# DesignKnobs' forward reference to TierSpec now that it exists.
DesignKnobs.model_rebuild()


class PricedCandidate(_Strict):
    candidate_id: str
    partition: Partition
    lane_eligibility: list[Lane]
    city: str | None = None


class Allocation(_Strict):
    tier: str
    unaided_slots: dict[str, int]
    unaided_shares_pct: dict[str, float]
    shares_sum_to_100: bool
    disjoint: bool
    prompted_slots: int
    notices: list[str]


class WavePrice(_Strict):
    calls: int
    calls_by_engine: dict[str, int]
    calls_by_lane: dict[str, int]
    gemini_without_city: int
    ineligible_combinations: int
    cost_per_call_usd: Decimal
    measured: bool
    basis: str
    answer_cost_usd: Decimal
    analyst_calls: int
    analyst_cost_usd: Decimal
    total_usd: Decimal
    status: Literal["within_budget", "conflict", "no_budget"]
    notices: list[str]


class AllocationAndPrice(_Strict):
    allocation: Allocation
    price: WavePrice


def _largest_remainder_pct(counts: dict[str, int]) -> dict[str, float]:
    total = sum(counts.values())
    if not total:
        return {k: 0.0 for k in counts}
    # Tenths of a percent, largest remainder → the displayed shares sum to exactly 100.0.
    raw = {k: v * 1000 / total for k, v in counts.items()}
    floors = {k: math.floor(v) for k, v in raw.items()}
    short = 1000 - sum(floors.values())
    for k in sorted(raw, key=lambda k: raw[k] - floors[k], reverse=True)[:short]:
        floors[k] += 1
    return {k: v / 10 for k, v in floors.items()}


def allocate_and_price(
    partitions: Mapping[str, Sequence[str]],
    selected: Sequence[PricedCandidate | Mapping[str, Any]],
    *,
    knobs: DesignKnobs,
    measured_cost_per_call: Decimal | None = None,
    analyst_cost_per_call: Decimal | None = None,
    repeats_by_partition: Mapping[str, int] | None = None,
    budget_usd: Decimal | None = None,
    city_on_gemini: Literal["run_without_city", "ineligible"] = "run_without_city",
) -> AllocationAndPrice:
    """T10. Tier allocation, disjoint set math, and the price of ONE wave.

    ``partitions``: partition → canonical_cell_ids. Unprompted sets must be
    disjoint and their displayed shares sum to exactly 100%; the prompted set
    is allocated separately. Price = Σ selected candidates × eligible engines
    per lane (Gemini takes no city) × repeats × per-call cost, plus analyst
    calls per ``analyst_sampling``. Only the API lanes are priced here.
    """
    # The tier table, the share bands and the fallback price are knobs carried on ``knobs``.
    tier = knobs.tiers[knobs.tier]
    notices: list[str] = []
    unaided = {p: list(dict.fromkeys(partitions.get(p, []))) for p in UNAIDED_PARTITIONS}
    all_ids = [i for p in UNAIDED_PARTITIONS for i in unaided[p]] + list(
        partitions.get("aided", [])
    )
    disjoint = len(all_ids) == len(set(all_ids))
    if not disjoint:
        dupes = sorted(i for i, n in collections.Counter(all_ids).items() if n > 1)
        notices.append(f"slots in more than one set: {dupes}")
    counts = {p: len(v) for p, v in unaided.items()}
    shares = _largest_remainder_pct(counts)
    total_unaided = sum(counts.values())
    low, high = tier.unaided_slots
    if total_unaided and not low <= total_unaided <= high:
        notices.append(
            f"{total_unaided} unprompted slots is outside the {tier.tier} range {low}-{high}"
        )
    if total_unaided:
        grouped = {
            "core": shares["core"],
            "sentinel+control": shares["sentinel"] + shares["control"],
            "rotating": shares["rotating"],
        }
        for name, (lo, hi) in knobs.share_bands.items():
            if not lo <= grouped[name] <= hi:
                notices.append(
                    f"{name} share {grouped[name]:.1f}% is outside the usual {lo:.0f}-{hi:.0f}%"
                )
    allocation = Allocation(
        tier=tier.tier,
        unaided_slots=counts,
        unaided_shares_pct=shares,
        shares_sum_to_100=(round(sum(shares.values()), 6) == 100.0) if total_unaided else False,
        disjoint=disjoint,
        prompted_slots=len(partitions.get("aided", [])),
        notices=list(notices),
    )

    per_call = (
        measured_cost_per_call if measured_cost_per_call and measured_cost_per_call > 0 else None
    )
    price_per_call = per_call if per_call is not None else knobs.fallback_cost_per_call_usd
    analyst_price = (
        analyst_cost_per_call
        if analyst_cost_per_call and analyst_cost_per_call > 0
        else price_per_call
    )
    # The org's knob wins; the tier table's repeats are the starting default it was seeded from.
    base_repeats = knobs.repeats_per_wave or tier.repeats or 1
    by_engine: collections.Counter[str] = collections.Counter()
    by_lane: collections.Counter[str] = collections.Counter()
    first_repeat_calls = 0
    gemini_no_city = 0
    ineligible = 0
    unpriced_lanes: set[str] = set()
    for raw in selected:
        cand = (
            raw if isinstance(raw, PricedCandidate) else PricedCandidate.model_validate(dict(raw))
        )
        repeats = (repeats_by_partition or {}).get(cand.partition, base_repeats)
        for lane in cand.lane_eligibility:
            if lane not in knobs.lanes:
                continue
            if lane not in API_LANES:
                unpriced_lanes.add(lane)
                continue
            for engine in knobs.engines:
                if cand.city and engine not in AI_ANSWER_LOCATION_ENGINES and lane == "retrieval":
                    if city_on_gemini == "ineligible":
                        ineligible += 1
                        continue
                    gemini_no_city += 1
                by_engine[engine] += repeats
                by_lane[lane] += repeats
                first_repeat_calls += 1
    calls = sum(by_engine.values())
    if unpriced_lanes:
        notices.append(f"lanes not priced here (no API cost model): {sorted(unpriced_lanes)}")
    if gemini_no_city:
        notices.append(
            f"{gemini_no_city} city-specific combinations run on Gemini without the city "
            "and are reported as their own stratum"
        )
    analyst_calls = {"first_repeat": first_repeat_calls, "all_repeats": calls, "none": 0}[
        knobs.analyst_sampling
    ]
    answer_cost = (price_per_call * calls).quantize(Decimal("0.0001"))
    analyst_cost = (analyst_price * analyst_calls).quantize(Decimal("0.0001"))
    total = answer_cost + analyst_cost
    status: Literal["within_budget", "conflict", "no_budget"] = "no_budget"
    if budget_usd is not None:
        status = "within_budget" if total <= budget_usd else "conflict"
        if status == "conflict":
            from .config import person_cost_text

            notices.append(
                f"one wave costs {person_cost_text(total)} against a "
                f"{person_cost_text(budget_usd)} budget"
            )
    return AllocationAndPrice(
        allocation=allocation,
        price=WavePrice(
            calls=calls,
            calls_by_engine=dict(by_engine),
            calls_by_lane=dict(by_lane),
            gemini_without_city=gemini_no_city,
            ineligible_combinations=ineligible,
            cost_per_call_usd=price_per_call,
            measured=per_call is not None,
            basis=(
                "your own completed AI-answer runs"
                if per_call is not None
                else (
                    "our published per-answer rate, because this organization has no "
                    "measured runs yet"
                )
            ),
            answer_cost_usd=answer_cost,
            analyst_calls=analyst_calls,
            analyst_cost_usd=analyst_cost,
            total_usd=total,
            status=status,
            notices=notices,
        ),
    )


# ---------------------------------------------------------------------------
# T11 — freeze a version
# ---------------------------------------------------------------------------


class GateDecision(_Strict):
    gate: Literal[1, 2, 3, 4]
    status: Literal["not_reached", "open", "approved", "edited", "continued_pending"]


class FrozenVersion(_Strict):
    version: str
    bump: Literal["initial", "minor", "patch", "none"]
    status: Literal["frozen", "provisional_directional"]
    reasons: list[str]
    content_hashes: dict[str, str | None]
    overlap_bridge: dict[str, Any] | None
    ledger_entry: LedgerChange | None


def _semver(value: str) -> tuple[int, int, int]:
    match = SEMVER_RE.match(value or "")
    if not match:
        raise ValueError(f"not a semantic version: {value!r}")
    return int(match[1]), int(match[2]), int(match[3])


def _panel_facets(panel: Mapping[str, Any]) -> dict[str, Any]:
    partitions = panel.get("partitions") or {}
    core = (partitions.get("core") or {}).get("canonical_cell_ids") or []
    return {
        "tracked_set": sorted(map(str, core)),
        "weights": panel.get("weight") or panel.get("weights"),
        "metrics": sorted(canonical_json(e) for e in _as_list(panel.get("estimands"))),
        "engine_mix": sorted(map(str, _as_list(panel.get("engines")))),
        "lanes": sorted(map(str, _as_list(panel.get("lanes")))),
        "everything": canonical_hash(
            {k: v for k, v in panel.items() if k not in _ENVELOPE_AND_STATE}
        ),
    }


_ENVELOPE_AND_STATE = {
    "schema_version",
    "artifact_id",
    "created_at",
    "created_by",
    "warnings",
    "version",
    "status",
    "approvals",
}


def freeze_version(
    panel: Mapping[str, Any],
    *,
    gates: Sequence[GateDecision | Mapping[str, Any]],
    content_hashes: Mapping[str, str | None],
    prior_panel: Mapping[str, Any] | None = None,
    actor: str,
    at: str,
    change_id: str | None = None,
) -> FrozenVersion:
    """T11. The next immutable version and whether it may be ``frozen``.

    Tracked set, weights, metrics or engine/lane mix changed → minor bump plus
    an overlap bridge; any other change → patch; identical content → no new
    version. ``frozen`` only with every content hash real and all four gates
    approved (or edited by a human); otherwise ``provisional_directional`` — a
    label, never a block.
    """
    decisions = {
        (g.gate if isinstance(g, GateDecision) else int(g["gate"])): (
            g.status if isinstance(g, GateDecision) else str(g["status"])
        )
        for g in gates
    }
    reasons: list[str] = []
    for gate in (1, 2, 3, 4):
        if decisions.get(gate) not in ("approved", "edited"):
            reasons.append(f"gate {gate} is {decisions.get(gate, 'not_reached')}")
    missing_hashes = sorted(k for k, v in content_hashes.items() if not is_real_hash(v))
    if missing_hashes:
        reasons.append(f"missing real hashes: {missing_hashes}")
    if not content_hashes:
        reasons.append("no content hashes recorded")
    status: Literal["frozen", "provisional_directional"] = (
        "frozen" if not reasons else "provisional_directional"
    )

    bridge: dict[str, Any] | None = None
    if prior_panel is None:
        version, bump, summary = "0.1.0", "initial", "first version"
    else:
        old, new = _panel_facets(prior_panel), _panel_facets(panel)
        major, minor, patch = _semver(str(prior_panel.get("version")))
        structural = [
            k
            for k in ("tracked_set", "weights", "metrics", "engine_mix", "lanes")
            if old[k] != new[k]
        ]
        if structural:
            version, bump = f"{major}.{minor + 1}.0", "minor"
            summary = f"changed {', '.join(structural)}"
            overlap = sorted(set(old["tracked_set"]) & set(new["tracked_set"]))
            bridge = {
                "from_version": prior_panel.get("version"),
                "to_version": version,
                "overlap_canonical_cell_ids": overlap,
                "removed": sorted(set(old["tracked_set"]) - set(new["tracked_set"])),
                "added": sorted(set(new["tracked_set"]) - set(old["tracked_set"])),
                "changed": structural,
            }
        elif old["everything"] != new["everything"]:
            version, bump, summary = (
                f"{major}.{minor}.{patch + 1}",
                "patch",
                "non-structural change",
            )
        else:
            version, bump, summary = str(prior_panel.get("version")), "none", "no change"
    entry = None
    if bump != "none":
        entry = LedgerChange(
            change_id=change_id or f"change-{version}",
            at=at,
            version=version,
            actor=actor,
            type="version_created" if bump == "initial" else f"{bump}_bump",
            summary=f"{summary}; {status}",
            affects=list(bridge["changed"]) if bridge else [],
            overlap_bridge=bridge,
        )
    return FrozenVersion(
        version=version,
        bump=bump,
        status=status,
        reasons=reasons,
        content_hashes=dict(content_hashes),
        overlap_bridge=bridge,
        ledger_entry=entry,
    )


def append_ledger(
    changes: Sequence[Mapping[str, Any] | LedgerChange], entry: LedgerChange
) -> list[dict[str, Any]]:
    """Append-only: returns a NEW list; history is never edited or reordered."""
    existing = [c.model_dump() if isinstance(c, LedgerChange) else dict(c) for c in changes]
    if any(c.get("change_id") == entry.change_id for c in existing):
        raise ValueError(f"change {entry.change_id} is already in the ledger")
    return [*existing, entry.model_dump()]


def ledger_is_append_only(
    old: Sequence[Mapping[str, Any]], new: Sequence[Mapping[str, Any]]
) -> bool:
    return len(new) >= len(old) and all(
        canonical_json(dict(a)) == canonical_json(dict(b)) for a, b in zip(old, new, strict=False)
    )


# ---------------------------------------------------------------------------
# T12 — the six metrics (shapes returned by the metrics API unchanged)
# ---------------------------------------------------------------------------


class Stratum(_Strict):
    partition: str | None = None
    lane: str | None = None
    aided_status: str | None = None
    engine: str | None = None
    locale: str | None = None
    market_side: str | None = None
    wave_id: str | None = None


class Interval(_Strict):
    low: float
    high: float
    method: str
    level: float


class MetricEstimate(_Strict):
    metric: MetricName
    display_name: str
    does_not_prove: str
    stratum: Stratum
    numerator: int | None
    denominator: int | None
    distinct_slots: int
    valid_observations: int
    invalid_observations: int
    rate: float | None = Field(default=None, ge=0, le=1)
    interval: Interval | None = None
    shown_as: Literal["rate", "counts", "not_set_up", "unmeasured"]
    effective_sample_size: float | None = None


class PairedComparison(_Strict):
    metric: MetricName
    stratum: Stratum
    from_wave: str
    to_wave: str
    overlap_slots: int
    change: float | None = None
    interval: Interval | None = None


class PanelMetrics(_Strict):
    panel_id: str
    panel_status: str
    panel_version: str | None = None
    conditional_note: str = CONDITIONAL_NOTE
    evidence_ladder: list[str] = Field(default_factory=lambda: list(EVIDENCE_LADDER))
    unclassified_questions: int = 0
    min_cells_for_rate: int
    metrics: list[MetricEstimate]
    comparisons: list[PairedComparison] = Field(default_factory=list)
    #: All six metric definitions, always — so a metric with no estimate yet still shows its
    #: name and its "does not prove" line on screen (never a bare "not measured").
    definitions: list[MetricDefinition] = Field(default_factory=lambda: list(METRICS.values()))


class MetricObservation(_Strict):
    """One answer, reduced to what T12/T13 need (built from response rows)."""

    canonical_cell_id: str
    candidate_id: str | None = None
    partition: Partition | None = None
    lane: Lane | None = None
    aided_status: AidedStatus | None = None
    engine: str | None = None
    locale: str | None = None
    market_side: str | None = None
    wave_id: str | None = None
    repeat_index: int | None = None
    variant_role: str | None = None
    time_block: str | None = None
    validity_status: Literal["valid", "invalid", "retry"] = "valid"
    target_mentioned: bool | None = None
    #: Aided knowledge: identified the target AND stated no contradicting fact. None = not coded.
    target_identified: bool | None = None
    entities_mentioned: list[dict[str, Any]] | None = None
    citations_exposed: bool | None = None
    target_cited: bool | None = None
    #: Framing/key-message codes present in this answer; None = not coded.
    framings: list[str] | None = None


class CampaignDesign(_Strict):
    """A pre-registered campaign test. Without one, campaign_response is "not set up"."""

    design_id: str
    registered_at: str
    treatment_cell_ids: list[str] = Field(min_length=1)
    control_cell_ids: list[str] = Field(min_length=1)


class EstimateRun(_Strict):
    metrics: list[MetricEstimate]
    comparisons: list[PairedComparison]
    bootstrap_seed: int
    bootstrap_draws: int


_STRATUM_KEYS = ("partition", "lane", "aided_status", "engine", "locale", "market_side", "wave_id")


def _stratum_of(obs: MetricObservation, *, drop_wave: bool = False) -> tuple[Any, ...]:
    return tuple(None if (drop_wave and k == "wave_id") else getattr(obs, k) for k in _STRATUM_KEYS)


def _wilson(x: int, n: int, level: float) -> Interval:
    z = NormalDist().inv_cdf(0.5 + level / 2)
    p = x / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return Interval(
        low=max(0.0, centre - half), high=min(1.0, centre + half), method="wilson", level=level
    )


def _percentile(sorted_values: list[float], q: float) -> float:
    if not sorted_values:
        return math.nan
    pos = q * (len(sorted_values) - 1)
    lo, hi = math.floor(pos), math.ceil(pos)
    return sorted_values[lo] + (sorted_values[hi] - sorted_values[lo]) * (pos - lo)


def _bootstrap_ratio(
    slots: list[tuple[float, float, float]],
    *,
    draws: int,
    rng: random.Random,
    level: float,
    method: str,
) -> Interval | None:
    """slots: (weight, numerator, denominator); resample whole slots."""
    stats: list[float] = []
    k = len(slots)
    for _ in range(draws):
        num = den = 0.0
        for _ in range(k):
            w, a, b = slots[rng.randrange(k)]
            num += w * a
            den += w * b
        if den > 0:
            stats.append(num / den)
    if not stats:
        return None
    stats.sort()
    alpha = (1 - level) / 2
    return Interval(
        low=max(0.0, _percentile(stats, alpha)),
        high=min(1.0, _percentile(stats, 1 - alpha)),
        method=method,
        level=level,
    )


def _kish(weights: list[float]) -> float | None:
    total = sum(weights)
    squares = sum(w * w for w in weights)
    return (total * total) / squares if squares else None


def _obs_value(
    metric: str, obs: MetricObservation, framing: str | None
) -> tuple[float, float] | None:
    """(numerator, denominator) contribution of one VALID observation, or None if unmeasured."""
    if metric == "unaided_brand_presence":
        return None if obs.target_mentioned is None else (float(obs.target_mentioned), 1.0)
    if metric == "aided_brand_knowledge":
        return None if obs.target_identified is None else (float(obs.target_identified), 1.0)
    if metric == "competitive_mention_share":
        if obs.entities_mentioned is None:
            return None
        entities = {
            (str(e.get("entity")).casefold(), e.get("kind"))
            for e in obs.entities_mentioned
            if isinstance(e, Mapping)
        }
        target = sum(1 for _, kind in entities if kind == "target")
        return float(target), float(len(entities))
    if metric == "citation_presence":
        if obs.citations_exposed is not True or obs.target_cited is None:
            return None
        return float(obs.target_cited), 1.0
    if metric == "answer_framing":
        if obs.target_mentioned is not True or obs.framings is None:
            return None
        return float(framing in obs.framings), 1.0
    return None


def _eligible(metric: str, obs: MetricObservation) -> bool:
    definition = METRICS[metric]
    if (
        obs.lane not in definition.eligible_lanes
        or obs.partition not in definition.eligible_partitions
    ):
        return False
    if metric in ("unaided_brand_presence", "competitive_mention_share"):
        return obs.aided_status == "unaided"
    if metric == "aided_brand_knowledge":
        return obs.aided_status == "target_aided"
    return True


def _estimate_group(
    metric: str,
    stratum: Stratum,
    group: list[MetricObservation],
    *,
    framing: str | None,
    display_name: str,
    weights: Mapping[str, float] | None,
    min_cells: int,
    draws: int,
    rng: random.Random,
    level: float,
) -> MetricEstimate:
    definition = METRICS[metric]
    valid = [o for o in group if o.validity_status == "valid"]
    invalid = len(group) - len(valid)
    per_slot: dict[str, list[float]] = {}
    obs_per_slot: collections.Counter[str] = collections.Counter()
    for obs in valid:
        value = _obs_value(metric, obs, framing)
        if value is None:
            continue
        slot = per_slot.setdefault(obs.canonical_cell_id, [0.0, 0.0])
        slot[0] += value[0]
        slot[1] += value[1]
        obs_per_slot[obs.canonical_cell_id] += 1
    measured = {k: v for k, v in per_slot.items() if v[1] > 0}
    base = dict(
        metric=metric,
        display_name=display_name,
        does_not_prove=definition.does_not_prove,
        stratum=stratum,
        valid_observations=len(valid),
        invalid_observations=invalid,
    )
    if not measured:
        return MetricEstimate(
            **base, numerator=None, denominator=None, distinct_slots=0, shown_as="unmeasured"
        )
    numerator = int(round(sum(v[0] for v in measured.values())))
    denominator = int(round(sum(v[1] for v in measured.values())))
    slot_weights = [float((weights or {}).get(k, 1.0)) for k in measured]
    ess = _kish(slot_weights)
    if len(measured) < min_cells:
        return MetricEstimate(
            **base,
            numerator=numerator,
            denominator=denominator,
            distinct_slots=len(measured),
            shown_as="counts",
            effective_sample_size=ess,
        )
    weighted = weights is not None
    triples = [(w, v[0], v[1]) for w, v in zip(slot_weights, measured.values(), strict=True)]
    total_w_den = sum(w * b for w, _, b in triples)
    rate = sum(w * a for w, a, _ in triples) / total_w_den if total_w_den else None
    binary = metric != "competitive_mention_share"
    one_per_slot = all(obs_per_slot[k] == 1 for k in measured)
    if binary and one_per_slot and not weighted:
        interval = _wilson(numerator, denominator, level)
    else:
        interval = _bootstrap_ratio(
            triples,
            draws=draws,
            rng=rng,
            level=level,
            method="stratified_slot_cluster_bootstrap" if weighted else "slot_cluster_bootstrap",
        )
    return MetricEstimate(
        **base,
        numerator=numerator,
        denominator=denominator,
        distinct_slots=len(measured),
        rate=rate,
        interval=interval,
        shown_as="rate",
        effective_sample_size=ess,
    )


def _paired(
    metric: str,
    stratum: Stratum,
    before: list[MetricObservation],
    after: list[MetricObservation],
    *,
    from_wave: str,
    to_wave: str,
    min_cells: int,
    draws: int,
    rng: random.Random,
    level: float,
) -> PairedComparison:
    def slot_values(rows: list[MetricObservation]) -> dict[str, list[float]]:
        out: dict[str, list[float]] = {}
        for obs in rows:
            if obs.validity_status != "valid":
                continue
            value = _obs_value(metric, obs, None)
            if value is None:
                continue
            slot = out.setdefault(obs.canonical_cell_id, [0.0, 0.0])
            slot[0] += value[0]
            slot[1] += value[1]
        return {k: v for k, v in out.items() if v[1] > 0}

    a, b = slot_values(before), slot_values(after)
    overlap = sorted(set(a) & set(b))
    if len(overlap) < min_cells:
        return PairedComparison(
            metric=metric,
            stratum=stratum,
            from_wave=from_wave,
            to_wave=to_wave,
            overlap_slots=len(overlap),
        )

    def diff(keys: list[str]) -> float | None:
        da = sum(a[k][1] for k in keys)
        db = sum(b[k][1] for k in keys)
        if not da or not db:
            return None
        return sum(b[k][0] for k in keys) / db - sum(a[k][0] for k in keys) / da

    change = diff(overlap)
    stats: list[float] = []
    for _ in range(draws):
        sample = [overlap[rng.randrange(len(overlap))] for _ in overlap]
        value = diff(sample)
        if value is not None:
            stats.append(value)
    stats.sort()
    alpha = (1 - level) / 2
    interval = (
        Interval(
            low=_percentile(stats, alpha),
            high=_percentile(stats, 1 - alpha),
            method="paired_slot_cluster_bootstrap",
            level=level,
        )
        if stats
        else None
    )
    return PairedComparison(
        metric=metric,
        stratum=stratum,
        from_wave=from_wave,
        to_wave=to_wave,
        overlap_slots=len(overlap),
        change=change,
        interval=interval,
    )


COMPARABLE_METRICS = (
    "unaided_brand_presence",
    "aided_brand_knowledge",
    "competitive_mention_share",
    "citation_presence",
)


def estimate(
    observations: Sequence[MetricObservation | Mapping[str, Any]],
    *,
    min_cells_for_rate: int = 20,
    bootstrap_draws: int = 2000,
    seed: int = 0,
    level: float = 0.95,
    weights: Mapping[str, float] | None = None,
    campaign_design: CampaignDesign | None = None,
    framing_labels: Mapping[str, str] | None = None,
    wave_order: Sequence[str] | None = None,
) -> EstimateRun:
    """T12. The six metrics per stratum, plus paired wave-over-wave comparisons.

    Strata = partition × lane × prompted state × engine × locale × market side ×
    wave; lanes and prompted states never share a denominator. Valid
    observations only (invalid counted and shown). Wilson only for one binary
    observation per slot, unweighted; otherwise a slot-cluster bootstrap with
    ``seed`` and ``bootstrap_draws`` recorded on the run. Kish effective sample
    size over slot weights. Fewer than ``min_cells_for_rate`` distinct slots →
    counts, no rate. Nothing measured → ``unmeasured`` (never zero).
    ``campaign_response`` is ``not_set_up`` unless a pre-registered
    ``campaign_design`` exists. ``weights`` maps canonical_cell_id → combined
    weight (exposure × priority), normalized within the rollup by the ratio.
    """
    rows = [
        o if isinstance(o, MetricObservation) else MetricObservation.model_validate(dict(o))
        for o in observations
    ]
    rng = random.Random(seed)
    results: list[MetricEstimate] = []
    kwargs = dict(
        weights=weights, min_cells=min_cells_for_rate, draws=bootstrap_draws, rng=rng, level=level
    )

    for metric in (
        "unaided_brand_presence",
        "aided_brand_knowledge",
        "competitive_mention_share",
        "citation_presence",
    ):
        groups: dict[tuple[Any, ...], list[MetricObservation]] = collections.defaultdict(list)
        for obs in rows:
            if _eligible(metric, obs):
                groups[_stratum_of(obs)].append(obs)
        for key in sorted(groups, key=lambda k: tuple("" if v is None else str(v) for v in k)):
            results.append(
                _estimate_group(
                    metric,
                    Stratum(**dict(zip(_STRATUM_KEYS, key, strict=True))),
                    groups[key],
                    framing=None,
                    display_name=METRICS[metric].display_name,
                    **kwargs,
                )
            )

    framing_groups: dict[tuple[Any, ...], list[MetricObservation]] = collections.defaultdict(list)
    codes: set[str] = set()
    for obs in rows:
        if _eligible("answer_framing", obs):
            framing_groups[_stratum_of(obs)].append(obs)
            codes |= set(obs.framings or [])
    labels = framing_labels or {}
    framing_name = METRICS["answer_framing"].display_name
    for key in sorted(framing_groups, key=lambda k: tuple("" if v is None else str(v) for v in k)):
        for code in sorted(codes):
            results.append(
                _estimate_group(
                    "answer_framing",
                    Stratum(**dict(zip(_STRATUM_KEYS, key, strict=True))),
                    framing_groups[key],
                    framing=code,
                    display_name=f"{framing_name}: {labels.get(code, code)}",
                    **kwargs,
                )
            )

    campaign = METRICS["campaign_response"]
    if campaign_design is None:
        results.append(
            MetricEstimate(
                metric="campaign_response",
                display_name=campaign.display_name,
                does_not_prove=campaign.does_not_prove,
                stratum=Stratum(lane="campaign_experiment"),
                numerator=None,
                denominator=None,
                distinct_slots=0,
                valid_observations=0,
                invalid_observations=0,
                shown_as="not_set_up",
            )
        )
    else:
        for arm, ids in (
            ("treatment", campaign_design.treatment_cell_ids),
            ("control", campaign_design.control_cell_ids),
        ):
            members = set(ids)
            group = [
                o
                for o in rows
                if o.lane == "campaign_experiment" and o.canonical_cell_id in members
            ]
            results.append(
                _estimate_group(
                    "campaign_response",
                    Stratum(partition=arm, lane="campaign_experiment"),
                    group,
                    framing=None,
                    display_name=f"{campaign.display_name}: {arm}",
                    **kwargs,
                )
                if group
                else MetricEstimate(
                    metric="campaign_response",
                    display_name=f"{campaign.display_name}: {arm}",
                    does_not_prove=campaign.does_not_prove,
                    stratum=Stratum(partition=arm, lane="campaign_experiment"),
                    numerator=None,
                    denominator=None,
                    distinct_slots=0,
                    valid_observations=0,
                    invalid_observations=0,
                    shown_as="unmeasured",
                )
            )

    comparisons: list[PairedComparison] = []
    waves = list(wave_order) if wave_order else sorted({o.wave_id for o in rows if o.wave_id})
    for metric in COMPARABLE_METRICS:
        by_stratum: dict[tuple[Any, ...], dict[str, list[MetricObservation]]] = (
            collections.defaultdict(lambda: collections.defaultdict(list))
        )
        for obs in rows:
            if obs.wave_id and _eligible(metric, obs):
                by_stratum[_stratum_of(obs, drop_wave=True)][obs.wave_id].append(obs)
        for key in sorted(by_stratum, key=lambda k: tuple("" if v is None else str(v) for v in k)):
            per_wave = by_stratum[key]
            present = [w for w in waves if w in per_wave]
            for before, after in zip(present, present[1:], strict=False):
                comparisons.append(
                    _paired(
                        metric,
                        Stratum(**dict(zip(_STRATUM_KEYS, key, strict=True))),
                        per_wave[before],
                        per_wave[after],
                        from_wave=before,
                        to_wave=after,
                        min_cells=min_cells_for_rate,
                        draws=bootstrap_draws,
                        rng=rng,
                        level=level,
                    )
                )
    return EstimateRun(
        metrics=results,
        comparisons=comparisons,
        bootstrap_seed=seed,
        bootstrap_draws=bootstrap_draws,
    )


def build_panel_metrics(
    *,
    panel_id: str,
    panel_status: str,
    panel_version: str | None,
    run: EstimateRun,
    min_cells_for_rate: int,
    unclassified_questions: int = 0,
) -> PanelMetrics:
    """Wrap a T12 run in the API shape (GET /ai-visibility/panels/{id}/metrics)."""
    return PanelMetrics(
        panel_id=panel_id,
        panel_status=panel_status,
        panel_version=panel_version,
        unclassified_questions=unclassified_questions,
        min_cells_for_rate=min_cells_for_rate,
        metrics=run.metrics,
        comparisons=run.comparisons,
    )


# ---------------------------------------------------------------------------
# T13 — the variance pilot
# ---------------------------------------------------------------------------


class PilotPlan(_Strict):
    canonical_cell_ids: list[str]
    repeats: int
    time_blocks: int
    engines: list[str]
    lanes: list[str]
    runs: int
    seed: int
    notices: list[str]


def plan_variance_pilot(
    sentinel_cells: Sequence[Mapping[str, Any]],
    *,
    engines: Sequence[str],
    lanes: Sequence[str],
    target_cells: int = 16,
    repeats: int = 6,
    time_blocks: int = 2,
    seed: int = 0,
) -> PilotPlan:
    """T13. 12–20 diverse tripwires × 6–8 repeats × ≥2 time blocks.

    Diversity: round-robin across (band, job) so no single slot family
    dominates; order is seeded and recorded.
    """
    notices: list[str] = []
    target = min(max(target_cells, 12), 20)
    reps = min(max(repeats, 6), 8)
    blocks = max(time_blocks, 2)
    if (target, reps, blocks) != (target_cells, repeats, time_blocks):
        notices.append(f"pilot clamped to {target} slots × {reps} repeats × {blocks} time blocks")
    rng = random.Random(seed)
    families: dict[tuple[str, str], list[str]] = collections.defaultdict(list)
    for cell in sentinel_cells:
        families[(str(cell.get("proximity_band")), str(cell.get("job_id")))].append(
            str(cell.get("canonical_cell_id"))
        )
    queues = [sorted(v) for _, v in sorted(families.items())]
    for queue in queues:
        rng.shuffle(queue)
    chosen: list[str] = []
    while len(chosen) < target and any(queues):
        for queue in queues:
            if queue and len(chosen) < target:
                chosen.append(queue.pop(0))
    if len(chosen) < 12:
        notices.append(f"only {len(chosen)} tripwire slots available; the pilot wants 12-20")
    runs = len(chosen) * reps * blocks * len(engines) * len(lanes)
    return PilotPlan(
        canonical_cell_ids=chosen,
        repeats=reps,
        time_blocks=blocks,
        engines=list(engines),
        lanes=list(lanes),
        runs=runs,
        seed=seed,
        notices=notices,
    )


class VarianceDecomposition(_Strict):
    observations: int
    valid_observations: int
    slots: int
    mean: float | None
    between_slot: float | None
    within_slot: float | None
    variant: float | None
    time_block: float | None
    engine: float | None
    invalid_rate: float | None
    intraclass_correlation: float | None
    recommendation: Literal["more_slots", "more_repeats", "balanced", "insufficient_data"]
    reason: str


def _var(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    m = sum(values) / len(values)
    return sum((v - m) ** 2 for v in values) / (len(values) - 1)


def _group_mean_variance(rows: list[tuple[str, float]]) -> float | None:
    groups: dict[str, list[float]] = collections.defaultdict(list)
    for key, value in rows:
        groups[key].append(value)
    if len(groups) < 2:
        return None
    return _var([sum(v) / len(v) for v in groups.values()])


def decompose_variance(
    observations: Sequence[MetricObservation | Mapping[str, Any]],
) -> VarianceDecomposition:
    """T13. Read the pilot: between-slot vs within-slot (run) variance, plus
    variant, time-block and engine components and the invalid rate, on the
    binary "named, unprompted" outcome. High intraclass correlation → more
    slots; low → more repeats."""
    rows = [
        o if isinstance(o, MetricObservation) else MetricObservation.model_validate(dict(o))
        for o in observations
    ]
    valid = [o for o in rows if o.validity_status == "valid" and o.target_mentioned is not None]
    invalid_rate = (
        (len(rows) - sum(1 for o in rows if o.validity_status == "valid")) / len(rows)
        if rows
        else None
    )
    by_slot: dict[str, list[float]] = collections.defaultdict(list)
    for o in valid:
        by_slot[o.canonical_cell_id].append(float(o.target_mentioned))
    if len(by_slot) < 2 or all(len(v) < 2 for v in by_slot.values()):
        return VarianceDecomposition(
            observations=len(rows),
            valid_observations=len(valid),
            slots=len(by_slot),
            mean=None,
            between_slot=None,
            within_slot=None,
            variant=None,
            time_block=None,
            engine=None,
            invalid_rate=invalid_rate,
            intraclass_correlation=None,
            recommendation="insufficient_data",
            reason="needs at least two slots with repeated observations",
        )
    within = sum(_var(v) * (len(v) - 1) for v in by_slot.values()) / max(
        1, sum(len(v) - 1 for v in by_slot.values())
    )
    mean_n = sum(len(v) for v in by_slot.values()) / len(by_slot)
    between = max(0.0, _var([sum(v) / len(v) for v in by_slot.values()]) - within / mean_n)
    icc = between / (between + within) if (between + within) > 0 else None
    variant = _group_mean_variance(
        [
            (f"{o.canonical_cell_id}|{o.variant_role}", float(o.target_mentioned))
            for o in valid
            if o.variant_role
        ]
    )
    block = _group_mean_variance(
        [(str(o.time_block), float(o.target_mentioned)) for o in valid if o.time_block]
    )
    engine = _group_mean_variance(
        [(str(o.engine), float(o.target_mentioned)) for o in valid if o.engine]
    )
    if icc is None:
        rec, reason = "insufficient_data", "no variance in the outcome"
    elif icc >= 0.5:
        rec, reason = (
            "more_slots",
            f"intraclass correlation {icc:.2f}: repeats of a slot mostly agree",
        )
    elif icc <= 0.2:
        rec, reason = (
            "more_repeats",
            f"intraclass correlation {icc:.2f}: run-to-run wobble dominates",
        )
    else:
        rec, reason = "balanced", f"intraclass correlation {icc:.2f}"
    return VarianceDecomposition(
        observations=len(rows),
        valid_observations=len(valid),
        slots=len(by_slot),
        mean=sum(float(o.target_mentioned) for o in valid) / len(valid),
        between_slot=between,
        within_slot=within,
        variant=variant,
        time_block=block,
        engine=engine,
        invalid_rate=invalid_rate,
        intraclass_correlation=icc,
        recommendation=rec,
        reason=reason,
    )


# ---------------------------------------------------------------------------
# T14 — entity mentions
# ---------------------------------------------------------------------------


class EntityMention(_Strict):
    entity: str
    kind: Literal["target", "competitor"]
    matched_terms: list[str]


def _mentioned_terms(text: str, terms: Sequence[str]) -> list[str]:
    return [t for t in dict.fromkeys(terms) if t.strip() and answer_mentions_target(text, [t])[0]]


def entity_mentions(
    answer_text: str,
    *,
    target_entity: str,
    target_terms: Sequence[str],
    competitors: Mapping[str, Sequence[str]],
) -> list[EntityMention]:
    """T14. ``answer_mentions_target`` extended to competitors → ``entities_mentioned``."""
    text = unicodedata.normalize("NFKC", answer_text or "")
    out: list[EntityMention] = []
    matched = _mentioned_terms(text, target_terms)
    if matched:
        out.append(EntityMention(entity=target_entity, kind="target", matched_terms=matched))
    for name, terms in competitors.items():
        hits = _mentioned_terms(text, [name, *terms])
        if hits:
            out.append(EntityMention(entity=name, kind="competitor", matched_terms=hits))
    return out


def entity_mentions_from_register(
    answer_text: str,
    register: Mapping[str, Any] | ContaminationRegister,
    *,
    target_entity: str,
    competitor_groups: Mapping[str, Sequence[str]] | None = None,
) -> list[EntityMention]:
    """T14 over the frozen register: target = brands + products + domain forms;
    each competitor term is its own entity unless ``competitor_groups`` merges them."""
    classes = _register_classes(register)
    target_terms = classes["brands"] + classes["products"] + classes["domains"]
    competitors: dict[str, Sequence[str]] = dict(competitor_groups or {})
    grouped = {t.casefold() for terms in competitors.values() for t in terms} | {
        n.casefold() for n in competitors
    }
    for term in classes["competitor_terms"]:
        if term.casefold() not in grouped:
            competitors[term] = []
    return entity_mentions(
        answer_text, target_entity=target_entity, target_terms=target_terms, competitors=competitors
    )


# ---------------------------------------------------------------------------
# T15 — run manifest record
# ---------------------------------------------------------------------------

_SECRET_KEY_RE = re.compile(
    r"(api[_-]?key|secret|token|password|authorization|credential|cookie|bearer)", re.IGNORECASE
)
_RAW_PROMPT_KEYS = {"system_prompt", "developer_prompt", "hidden_instructions"}


def configuration_hash(config: Mapping[str, Any]) -> tuple[str, list[str]]:
    """Hash of the run configuration with secrets removed and raw hidden
    prompts replaced by their hashes. Returns (hash, the keys it redacted)."""
    redacted: list[str] = []

    def clean(value: Any, path: str) -> Any:
        if isinstance(value, Mapping):
            out: dict[str, Any] = {}
            for key, child in value.items():
                here = f"{path}.{key}" if path else str(key)
                if _SECRET_KEY_RE.search(str(key)):
                    redacted.append(here)
                    continue
                if key in _RAW_PROMPT_KEYS and isinstance(child, str):
                    redacted.append(here)
                    out[f"{key}_hash"] = text_hash(child)
                    continue
                out[str(key)] = clean(child, here)
            return out
        if isinstance(value, list):
            return [clean(v, path) for v in value]
        return value

    cleaned = clean(config, "")
    return canonical_hash(cleaned), redacted


class RunManifestRecord(_Strict):
    """One observation — the contract's exact field names, nothing else."""

    exact_prompt: str
    configuration_hash: str
    provider: str
    model: str
    surface: str
    lane: Lane
    locale: str
    search_policy: Literal["required", "allowed", "unavailable", "off"]
    retrieval_used: bool | None
    session_state: str
    response_payload_hash: str | None
    citation_payload_hash: str | None
    timestamp: str = Field(pattern=RFC3339_RE.pattern)
    retry_status: str
    validity_status: Literal["valid", "invalid", "retry"]
    parser_version: str


def build_run_manifest_record(
    *,
    exact_prompt: str,
    config: Mapping[str, Any],
    provider: str,
    model: str,
    surface: str,
    lane: Lane,
    locale: str,
    retrieval_used: bool | None,
    session_state: str,
    response_payload: Any | None,
    citation_payload: Any | None,
    timestamp: str,
    retry_status: str,
    validity_status: Literal["valid", "invalid", "retry"],
    parser_version: str,
) -> RunManifestRecord:
    """T15. One record per observation; secrets never stored, payloads hashed."""
    config_hash, _ = configuration_hash(config)
    search_policy = (
        "off" if lane == "closed_model" else "required" if lane == "retrieval" else "allowed"
    )
    return RunManifestRecord(
        exact_prompt=exact_prompt,
        configuration_hash=config_hash,
        provider=provider,
        model=model,
        surface=surface,
        lane=lane,
        locale=locale,
        search_policy=search_policy,
        retrieval_used=retrieval_used,
        session_state=session_state,
        response_payload_hash=canonical_hash(response_payload)
        if response_payload is not None
        else None,
        citation_payload_hash=canonical_hash(citation_payload)
        if citation_payload is not None
        else None,
        timestamp=timestamp,
        retry_status=retry_status,
        validity_status=validity_status,
        parser_version=parser_version,
    )


def rollup_family(lane: str) -> Literal["api", "consumer_surface", "campaign"]:
    """API and real-app observations never share a rollup."""
    if lane == "consumer_surface":
        return "consumer_surface"
    if lane == "campaign_experiment":
        return "campaign"
    return "api"


__all__ = [
    "ARTIFACT_FILES",
    "DESIGN_KNOB_KEYS",
    "ARTIFACT_MODELS",
    "CONDITIONAL_NOTE",
    "ENUMS",
    "EVIDENCE_LADDER",
    "METRICS",
    "REQUIRED_ARTIFACTS",
    "FUZZY_MIN_TOKEN_LENGTH",
    "FUZZY_RATIO",
    "SHARE_BANDS",
    "SIMILARITY_CHAR3_THRESHOLD",
    "SIMILARITY_EMBEDDING_THRESHOLD",
    "SIMILARITY_JACCARD_THRESHOLD",
    "TIERS",
    "AllocationAndPrice",
    "BlindBriefBuild",
    "BlindDesignBrief",
    "BuyerJobs",
    "CampaignDesign",
    "CandidateScan",
    "CheckResult",
    "ContaminationRegister",
    "CoverageMatrix",
    "DedupeResult",
    "DesignKnobs",
    "EntityMention",
    "EstimateRun",
    "FrozenVersion",
    "FuzzyMatch",
    "GateDecision",
    "IcpHypotheses",
    "Interval",
    "MeasurementCharter",
    "MetricEstimate",
    "MetricObservation",
    "PairedComparison",
    "Panel",
    "PanelChangeLedger",
    "PanelMetrics",
    "PilotPlan",
    "PricedCandidate",
    "PromptArchitecture",
    "PromptQA",
    "PromptUniverse",
    "ProposedRegisterTerms",
    "QAReconcile",
    "RegisterIdentity",
    "RenderedBlock",
    "RequestScan",
    "RunManifestRecord",
    "RunManifestTemplate",
    "SimilarityResult",
    "SourceManifest",
    "Stratum",
    "TermHit",
    "VarianceDecomposition",
    "allocate_and_price",
    "append_ledger",
    "assert_blind_mandate",
    "build_blind_brief",
    "build_charter",
    "build_panel_metrics",
    "build_run_manifest_record",
    "canonical_hash",
    "checks_passed",
    "configuration_hash",
    "contamination_scan",
    "coverage_matrix",
    "decompose_variance",
    "domain_forms",
    "entity_mentions",
    "entity_mentions_from_register",
    "estimate",
    "flatten_universe",
    "freeze_register",
    "freeze_version",
    "ledger_is_append_only",
    "make_envelope",
    "normalize_and_dedupe",
    "normalize_prompt",
    "plan_variance_pilot",
    "reconcile_qa",
    "register_terms",
    "rollup_family",
    "scan_output",
    "scan_rendered_request",
    "scan_text",
    "seed_register",
    "similarity_pairs",
    "source_manifest_hash",
    "term_in_text",
    "text_hash",
    "validate_artifacts",
    "validate_schemas",
]
