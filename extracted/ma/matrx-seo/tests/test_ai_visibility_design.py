"""T2–T15 of the AI-visibility panel design tools, pinned to worked examples.

Use case throughout: Tidewater E-Cycle, a regional electronics-recycling and
certified data-destruction company (tidewater-ecycle.com) whose buyers are IT
and compliance leads retiring laptops that held client data. Every expected
value is a literal or worked by hand from the brief, never computed by the
function under test. Each test names the break it catches.
"""

from __future__ import annotations

import hashlib
from decimal import Decimal
from typing import Any

import pytest

from matrx_seo.ai_visibility_design import (
    METRICS,
    DesignKnobs,
    GateDecision,
    PricedCandidate,
    ProposedRegisterTerms,
    RegisterIdentity,
    allocate_and_price,
    append_ledger,
    assert_blind_mandate,
    build_blind_brief,
    build_charter,
    build_run_manifest_record,
    canonical_hash,
    configuration_hash,
    contamination_scan,
    coverage_matrix,
    decompose_variance,
    domain_forms,
    entity_mentions_from_register,
    estimate,
    freeze_register,
    freeze_version,
    ledger_is_append_only,
    normalize_and_dedupe,
    plan_variance_pilot,
    reconcile_qa,
    scan_output,
    scan_rendered_request,
    scan_text,
    seed_register,
    similarity_pairs,
    source_manifest_hash,
    text_hash,
    validate_schemas,
)

NOW = "2026-09-27T15:00:00Z"
ENV = {"artifact_id": "tidewater-register", "created_by": "design-run", "created_at": NOW}


def _register() -> dict[str, Any]:
    reg = seed_register(
        RegisterIdentity(
            brand_name="Tidewater E-Cycle",
            brand_aliases=["Tidewater Ecycle"],
            domains=["https://www.tidewater-ecycle.com/services"],
            people=["Marisol Okafor"],
            products=["SecureWipe Pickup"],
            campaign_terms=["Drive Destruction Week"],
            competitors=["Harborline Recyclers", "ShredPoint"],
        ),
        **ENV,
    )
    return reg.model_dump(mode="json")


# --- T2 -----------------------------------------------------------------------


def test_canonical_hash_is_sha256_of_sorted_compact_utf8_json() -> None:
    # Break: key order or whitespace leaking into the digest.
    expected = "sha256:" + hashlib.sha256('{"a":[1,"é"],"b":2}'.encode()).hexdigest()
    assert canonical_hash({"b": 2, "a": [1, "é"]}) == expected
    assert canonical_hash({"a": [1, "é"], "b": 2}) == expected


def test_source_manifest_hash_covers_only_the_sources_array() -> None:
    # Break: hashing the envelope (self-referential digest) instead of `sources`.
    sources = [{"source_id": "source-001", "url": "https://tidewater-ecycle.com/r2"}]
    a = source_manifest_hash({"sources": sources, "warnings": ["x"], "created_at": NOW})
    b = source_manifest_hash(
        {"sources": sources, "warnings": [], "created_at": "2026-01-01T00:00:00Z"}
    )
    assert a == b == canonical_hash(sources)
    assert a != source_manifest_hash({"sources": [*sources, {"source_id": "source-002"}]})


def test_prompt_hash_is_of_the_exact_text() -> None:
    # Break: normalizing before hashing, so two different prompts share a hash.
    assert text_hash("Where can I recycle old laptops?") != text_hash(
        "where can i recycle old laptops"
    )


# --- T3 -----------------------------------------------------------------------


@pytest.mark.parametrize(
    ("raw", "forms"),
    [
        (
            "https://www.tidewater-ecycle.com/services",
            ["tidewater-ecycle.com", "www.tidewater-ecycle.com"],
        ),
        ("tidewater-ecycle.com", ["tidewater-ecycle.com", "www.tidewater-ecycle.com"]),
        (
            "HTTP://Shop.Tidewater-Ecycle.com:8443/",
            ["shop.tidewater-ecycle.com", "www.shop.tidewater-ecycle.com"],
        ),
    ],
)
def test_domain_forms_have_with_and_without_www(raw: str, forms: list[str]) -> None:
    assert domain_forms(raw) == forms


def test_register_seeds_identity_and_merges_agent_terms_without_duplicates() -> None:
    # Break: dropping agent-1 terms, or double-listing a casefold duplicate.
    reg = seed_register(
        RegisterIdentity(
            brand_name="Tidewater E-Cycle",
            domains=["tidewater-ecycle.com"],
            competitors=["ShredPoint"],
        ),
        proposed=ProposedRegisterTerms(
            brands=[{"term": "tidewater e-cycle", "source_id": "source-004"}],
            slogans=[{"term": "Recycled right, erased for good", "source_id": "source-002"}],
            competitor_terms=[{"term": "Harborline Recyclers", "source_id": "source-007"}],
        ),
        **ENV,
    ).model_dump(mode="json")
    assert reg["target_terms"]["brands"] == ["Tidewater E-Cycle"]
    assert reg["target_terms"]["slogans"] == ["Recycled right, erased for good"]
    assert reg["target_terms"]["domains"] == ["tidewater-ecycle.com", "www.tidewater-ecycle.com"]
    assert reg["competitor_terms"] == ["ShredPoint", "Harborline Recyclers"]


def test_freezing_the_register_hash_changes_when_a_term_changes() -> None:
    # Break: a freeze hash that ignores the terms (a later edit goes unnoticed).
    base = _register()
    _, first = freeze_register(base)
    base["competitor_terms"].append("GreenBin Data Services")
    _, second = freeze_register(base)
    assert first != second and first.startswith("sha256:")


def test_charter_declares_all_six_estimands_with_the_brief_does_not_prove_lines() -> None:
    # Break: an estimand missing, or its "does not prove" line reworded.
    charter = build_charter(
        DesignKnobs(lanes=["closed_model"]),
        site_name="Tidewater E-Cycle",
        locales=["en-US"],
        **ENV,
    )
    by_name = {e.name: e for e in charter.estimands}
    assert set(by_name) == {
        "unaided_brand_presence",
        "aided_brand_knowledge",
        "competitive_mention_share",
        "citation_presence",
        "answer_framing",
        "campaign_response",
    }
    assert (
        by_name["citation_presence"].does_not_prove
        == "traffic, clicks, or that the citation shaped the answer"
    )
    assert by_name["citation_presence"].eligible_lanes == ["retrieval"]
    assert charter.lanes == ["closed_model"]
    assert charter.source_manifest_hash is None
    assert any("hash" in w for w in charter.warnings)


# --- T1 strict schemas ----------------------------------------------------------


def test_strict_schema_rejects_an_unknown_key_and_accepts_the_model_built_register() -> None:
    # Break: extra="forbid" dropped, so an agent's invented field slips through.
    reg = _register()
    ok = {c.id: c for c in validate_schemas({"contamination_register": reg})}
    assert ok["schema:contamination_register.yaml"].passed is True
    reg["scan_policy"] = {"fuzzy": "off"}
    bad = {c.id: c for c in validate_schemas({"contamination_register": reg})}
    assert bad["schema:contamination_register.yaml"].passed is False


def test_a_null_source_hash_without_a_warning_fails_the_envelope() -> None:
    # Break: a provisional null hash that nobody announced.
    reg = _register()
    reg["warnings"] = []
    checks = {c.id: c for c in validate_schemas({"contamination_register": reg})}
    assert checks["schema:contamination_register.yaml"].passed is False


# --- T4 -----------------------------------------------------------------------


def _cand(text: str, **cell: Any) -> dict[str, Any]:
    base = {
        "candidate_id": "prompt-001a",
        "text": text,
        "proximity_band": "B3_problem_need",
        "aided_status": "unaided",
        "partition": "core",
        "campaign_exposed": False,
    }
    return base | cell


@pytest.mark.parametrize(
    ("text", "outcome", "kind"),
    [
        ("is tidewater e-cycle legit for hard drive shredding", "fail", "token"),
        ("who handles pickup for tidewater-ecycle.com customers", "fail", "domain"),
        ("does TidewaterEcycle certify data destruction", "fail", "compact"),
        ("any tidewaterecycle reviews", "fail", "compact"),
        ("what does shredpointe charge per drive", "review", "fuzzy"),
        ("how do we get rid of 200 old laptops with client data on them", "pass", None),
    ],
)
def test_unaided_core_scan_outcomes(text: str, outcome: str, kind: str | None) -> None:
    # Break: substring matching, or a fuzzy near-miss treated as a hard fail.
    [scan] = contamination_scan([_cand(text)], _register())
    assert scan.outcome == outcome
    kinds = {r.match_kind for r in scan.rule_results}
    assert (kind in kinds) if kind else not kinds


def test_a_short_term_never_matches_inside_another_word() -> None:
    # Break: "Pickup" matching inside "pickups-and-deliveries"-style words.
    reg = _register()
    reg["target_terms"]["products"] = ["Wipe"]
    assert scan_text("our wiper blades are worn", reg) == []
    assert [h.term for h in scan_text("can we wipe drives on site", reg)] == ["Wipe"]


@pytest.mark.parametrize(
    ("cell", "text", "outcome"),
    [
        (
            {
                "proximity_band": "B0_direct_brand_product",
                "aided_status": "target_aided",
                "partition": "aided",
            },
            "does Tidewater E-Cycle give certificates of destruction",
            "pass",
        ),
        (
            {
                "proximity_band": "B1_comparison_purchase",
                "aided_status": "competitor_aided",
                "partition": "rotating",
            },
            "is ShredPoint or a local recycler better for hard drives",
            "pass",
        ),
        (
            {
                "proximity_band": "B2_category",
                "aided_status": "category_aided",
                "partition": "rotating",
            },
            "best electronics recyclers like ShredPoint",
            "fail",
        ),
        (
            {
                "proximity_band": "B3_problem_need",
                "aided_status": "unaided",
                "partition": "rotating",
            },
            "anything happening for Drive Destruction Week",
            "fail",
        ),
        (
            {
                "proximity_band": "B3_problem_need",
                "aided_status": "unaided",
                "partition": "rotating",
                "campaign_exposed": True,
            },
            "anything happening for Drive Destruction Week",
            "pass",
        ),
    ],
)
def test_exceptions_follow_band_and_prompted_state(
    cell: dict[str, Any], text: str, outcome: str
) -> None:
    # Break: aided rules ignored (Brand questions failed) or over-applied
    # (competitors allowed anywhere).
    [scan] = contamination_scan([_cand(text, **cell)], _register())
    assert scan.outcome == outcome


# --- T5 -----------------------------------------------------------------------


def _buyer_jobs() -> dict[str, Any]:
    return {
        "jobs": [
            {
                "job_id": "job-001",
                "statement": "Retire laptops that held client data with proof they were destroyed",
                "information_acts": ["diagnose", "plan"],
                "journey_states": ["problem_identification"],
                "constraints": [
                    "HIPAA records on the drives",
                    "needs a certificate of destruction",
                ],
                "roles": ["IT or compliance lead", "office manager"],
                "language_samples": [
                    {
                        "text": "we have 200 old laptops with patient data, what do we do",
                        "source_id": "source-011",
                        "evidence_grade": "A",
                    },
                    {
                        "text": "tidewater e-cycle picked ours up last year",
                        "source_id": "source-012",
                        "evidence_grade": "A",
                    },
                    {
                        "text": "is shredpoint cheaper than a local recycler",
                        "source_id": "source-013",
                        "evidence_grade": "B",
                    },
                ],
                "supporting_source_ids": ["source-011", "source-012"],
                "evidence_grade": "A",
            },
            {
                "job_id": "job-002",
                "statement": "Get Tidewater E-Cycle to schedule a pickup",
                "roles": ["office manager"],
                "evidence_grade": "C",
            },
        ]
    }


def test_blind_brief_drops_register_hits_and_counts_them() -> None:
    # Break: a buyer fragment naming the brand or a competitor reaching the blind writer.
    build = build_blind_brief(_buyer_jobs(), _register(), locales=["en-US"], **ENV)
    fragments = [f.fragment for f in build.brief.safe_language_fragments]
    assert fragments == ["we have 200 old laptops with patient data, what do we do"]
    assert build.dropped_fragments == 2
    assert [j.job_id for j in build.brief.approved_jobs] == ["job-001"]
    assert [r.label for r in build.brief.anonymized_roles] == [
        "IT or compliance lead",
        "office manager",
    ]
    assert scan_text(build.brief.model_dump_json(), _register()) == []
    assert build.blind_brief_hash == canonical_hash(build.brief.model_dump(mode="json"))


def test_blind_brief_keeps_only_approved_jobs() -> None:
    build = build_blind_brief(
        _buyer_jobs(), _register(), locales=["en-US"], approved_job_ids=[], **ENV
    )
    assert build.brief.approved_jobs == [] and build.brief.safe_language_fragments == []


def test_rendered_request_with_a_seeded_brand_is_refused_and_hashed() -> None:
    # Break: the guard scanning only the user message while a context block carries the name.
    blocks = [
        {"role": "system", "text": "Write natural questions a buyer would type."},
        {"role": "user", "text": "Slot: retire laptops with client data."},
        {"role": "context", "text": "Brand profile: Tidewater E-Cycle, Norfolk VA"},
    ]
    scan = scan_rendered_request(blocks, _register())
    assert scan.allowed is False
    assert {(h["block"], h["term_class"]) for h in scan.hits} == {(2, "brands")}
    clean = scan_rendered_request(blocks[:2], _register())
    assert clean.allowed is True and clean.request_hash != scan.request_hash


def test_output_scan_flags_only_unaided_candidates_with_hits() -> None:
    universe = {
        "canonical_cells": [
            {
                "aided_status": "unaided",
                "candidates": [
                    {
                        "candidate_id": "prompt-001a",
                        "text": "safest way to dispose of old hard drives",
                    },
                    {"candidate_id": "prompt-001b", "text": "does tidewater e-cycle wipe drives"},
                ],
            },
            {
                "aided_status": "target_aided",
                "candidates": [
                    {"candidate_id": "prompt-009a", "text": "is Tidewater E-Cycle R2 certified"},
                ],
            },
        ]
    }
    assert list(scan_output(universe, _register())) == ["prompt-001b"]


@pytest.mark.parametrize(
    ("definition", "problems"),
    [
        ({"auto_context_disabled": True, "tools": []}, 0),
        ({"auto_context_disabled": False, "tools": []}, 1),
        ({"auto_context_disabled": True, "tools": ["web_search"]}, 1),
        ({}, 1),
    ],
)
def test_blind_writer_mandate_must_have_no_context_and_no_tools(
    definition: dict[str, Any], problems: int
) -> None:
    assert len(assert_blind_mandate(definition)) == problems


# --- T6 / T7 ------------------------------------------------------------------


def test_exact_duplicates_merge_keeping_the_stronger_evidence() -> None:
    # Break: keeping the first-seen (weaker) candidate, or merging non-duplicates.
    result = normalize_and_dedupe(
        [
            {
                "candidate_id": "prompt-004b",
                "text": "How do I wipe a laptop before recycling it?",
                "evidence_grade": "C",
            },
            {
                "candidate_id": "prompt-004a",
                "text": "how do i WIPE a laptop before recycling it",
                "evidence_grade": "A",
            },
            {
                "candidate_id": "prompt-005a",
                "text": "cost to shred 50 hard drives",
                "evidence_grade": "B",
            },
            {"candidate_id": "prompt-006a", "text": "recycling?", "evidence_grade": "B"},
        ]
    )
    assert [(m.kept, m.merged) for m in result.merges] == [("prompt-004a", ["prompt-004b"])]
    assert result.unique is False
    assert {r.candidate_id: r.flags for r in result.records}["prompt-006a"] == ["too_short"]


def test_similarity_nominates_near_duplicates_within_a_locale_only() -> None:
    # Break: pairing across locales, or nominating unrelated prompts.
    cands = [
        {
            "candidate_id": "prompt-010a",
            "locale": "en-US",
            "text": "best place to recycle old laptops",
        },
        {
            "candidate_id": "prompt-010b",
            "locale": "en-US",
            "text": "best place to recycle old laptops near me",
        },
        {
            "candidate_id": "prompt-011a",
            "locale": "en-CA",
            "text": "best place to recycle old laptops",
        },
        {
            "candidate_id": "prompt-012a",
            "locale": "en-US",
            "text": "how long do hard drives keep data",
        },
    ]
    result = similarity_pairs(cands)
    assert [(p.a, p.b, p.action) for p in result.pairs] == [
        ("prompt-010a", "prompt-010b", "nominate")
    ]


def test_embedding_similarity_requires_a_recorded_model_version() -> None:
    with pytest.raises(ValueError, match="embedding_model"):
        similarity_pairs([], embed=lambda texts: [[1.0] for _ in texts])
    result = similarity_pairs(
        [
            {
                "candidate_id": "prompt-020a",
                "locale": "en-US",
                "text": "dispose of office computers safely",
            },
            {
                "candidate_id": "prompt-020b",
                "locale": "en-US",
                "text": "get rid of work PCs securely",
            },
        ],
        embed=lambda texts: [[1.0, 0.0], [0.99, 0.05]],
        embedding_model="text-embedding-3-small@2026-06",
    )
    assert [p.nominated_by for p in result.pairs] == [["embedding"]]
    assert result.embedding_model == "text-embedding-3-small@2026-06"


# --- T8 -----------------------------------------------------------------------


def _universe() -> dict[str, Any]:
    return {
        "canonical_cells": [
            {
                "canonical_cell_id": "cell-001",
                "candidates": [{"candidate_id": "prompt-001a"}, {"candidate_id": "prompt-001b"}],
            },
            {"canonical_cell_id": "cell-002", "candidates": [{"candidate_id": "prompt-002a"}]},
        ]
    }


def test_reconcile_derives_accepted_ids_and_counts_from_decisions() -> None:
    # Break: accepted IDs taken from the model instead of the pass decisions.
    qa = {
        "decisions": [
            {"candidate_id": "prompt-001a", "status": "pass"},
            {"candidate_id": "prompt-001b", "status": "quarantine"},
            {"candidate_id": "prompt-002a", "status": "pass"},
        ]
    }
    result = reconcile_qa(qa, _universe(), baseline_fields_blinded=True)
    assert result.valid is True
    assert result.qa["accepted_candidate_ids"] == ["prompt-001a", "prompt-002a"]
    assert result.qa["counts"] == {
        "total_candidates": 3,
        "pass": 2,
        "revise": 0,
        "quarantine": 1,
        "reject": 0,
        "accepted": 2,
    }
    assert result.qa["baseline_fields_blinded"] is True


@pytest.mark.parametrize(
    ("qa", "error"),
    [
        (
            {
                "decisions": [
                    {"candidate_id": "prompt-001a", "status": "pass"},
                    {"candidate_id": "prompt-002a", "status": "pass"},
                ]
            },
            "missing decisions",
        ),
        (
            {
                "decisions": [
                    {"candidate_id": c, "status": "pass"}
                    for c in ("prompt-001a", "prompt-001b", "prompt-002a", "prompt-999z")
                ]
            },
            "unknown candidate",
        ),
        (
            {
                "decisions": [
                    {"candidate_id": c, "status": "pass"}
                    for c in ("prompt-001a", "prompt-001b", "prompt-002a")
                ],
                "accepted_candidate_ids": ["prompt-001a"],
            },
            "accepted_candidate_ids disagree",
        ),
        (
            {
                "decisions": [
                    {"candidate_id": c, "status": "pass"}
                    for c in ("prompt-001a", "prompt-001b", "prompt-002a")
                ],
                "counts": {"pass": 3},
            },
            "counts disagree",
        ),
        (
            {
                "decisions": [
                    {"candidate_id": c, "status": "approve"}
                    for c in ("prompt-001a", "prompt-001b", "prompt-002a")
                ]
            },
            "invalid status",
        ),
    ],
)
def test_reconcile_mismatch_is_invalid_never_a_warning(qa: dict[str, Any], error: str) -> None:
    result = reconcile_qa(qa, _universe())
    assert result.valid is False
    assert any(error in e for e in result.errors)


# --- T9 -----------------------------------------------------------------------


def _cell(cid: str, band: str, partition: str, lanes: list[str], **extra: Any) -> dict[str, Any]:
    return {
        "canonical_cell_id": cid,
        "proximity_band": band,
        "aided_status": "unaided",
        "job_id": "job-001",
        "information_act": "plan",
        "journey_state": "exploration",
        "persona_id": "role-001",
        "locale": "en-US",
        "partition": partition,
        "evidence_grade": "B",
        "lane_eligibility": lanes,
        "icp_ids": ["icp-001"],
        "reason_source_ids": ["source-011"],
        "candidates": [{"candidate_id": f"{cid}a"}],
    } | extra


def test_coverage_counts_sum_and_multi_valued_axes_are_non_additive() -> None:
    universe = {
        "canonical_cells": [
            _cell("cell-001", "B3_problem_need", "core", ["closed_model", "retrieval"]),
            _cell("cell-002", "B4_job_goal", "core", ["retrieval"]),
            _cell(
                "cell-003",
                "B5_broad_discovery_story",
                "rotating",
                ["retrieval"],
                reason_source_ids=[],
            ),
        ]
    }
    matrix = coverage_matrix(
        universe,
        perimeter=[
            {"area": "laptop and desktop recycling", "covered_by": ["icp-001"]},
            {"area": "battery recycling", "waiver": "no buyer evidence yet"},
            {"area": "ITAD for hospitals"},
        ],
    )
    axes = {a.axis: a for a in matrix.axes}
    assert axes["proximity_band"].counts == {
        "B3_problem_need": 1,
        "B4_job_goal": 1,
        "B5_broad_discovery_story": 1,
    }
    assert axes["partition"].sums_to_total is True
    assert axes["lane_eligibility"].counts == {"closed_model": 1, "retrieval": 3}
    assert axes["lane_eligibility"].additive is False
    assert [p.covered for p in matrix.perimeter] == [True, True, False]
    assert matrix.perimeter_complete is False
    assert matrix.market_issues == [
        "cell-003: Market slot without evidence",
        "cell-003: Market slot without a review-by date",
    ]


# --- T10 ----------------------------------------------------------------------


def test_wave_price_follows_lane_and_engine_eligibility_with_gemini_taking_no_city() -> None:
    # Worked by hand: A = 2 lanes × 4 engines × 3 repeats = 24; B (city, retrieval only)
    # = 4 engines × 3 = 12, one of them Gemini without the city. 36 × $0.05 = $1.80;
    # analyst first repeat = 8 + 4 = 12 × $0.05 = $0.60; total $2.40.
    result = allocate_and_price(
        {"core": ["cell-001", "cell-002"]},
        [
            PricedCandidate(
                candidate_id="prompt-001a",
                partition="core",
                lane_eligibility=["closed_model", "retrieval"],
            ),
            PricedCandidate(
                candidate_id="prompt-002a",
                partition="core",
                lane_eligibility=["retrieval"],
                city="Norfolk",
            ),
        ],
        knobs=DesignKnobs(),
        measured_cost_per_call=Decimal("0.05"),
        budget_usd=Decimal("2.00"),
    )
    price = result.price
    assert price.calls == 36
    assert price.calls_by_engine == {"chat_gpt": 9, "claude": 9, "gemini": 9, "perplexity": 9}
    assert price.gemini_without_city == 1
    assert price.analyst_calls == 12
    assert price.total_usd == Decimal("2.4000")
    assert price.measured is True
    assert price.status == "conflict"


def test_city_slots_can_be_made_ineligible_on_gemini_and_fallback_price_is_disclosed() -> None:
    result = allocate_and_price(
        {"core": ["cell-002"]},
        [
            {
                "candidate_id": "prompt-002a",
                "partition": "core",
                "lane_eligibility": ["retrieval"],
                "city": "Norfolk",
            }
        ],
        knobs=DesignKnobs(analyst_sampling="none"),
        city_on_gemini="ineligible",
        budget_usd=Decimal("5"),
    )
    assert result.price.calls == 9
    assert result.price.ineligible_combinations == 1
    assert result.price.measured is False
    assert "no measured runs" in result.price.basis
    assert result.price.total_usd == Decimal("0.1800")
    assert result.price.status == "within_budget"


def test_unprompted_sets_are_disjoint_and_shares_sum_to_exactly_100() -> None:
    parts = {
        "core": [f"cell-{i:03d}" for i in range(26)],
        "sentinel": ["cell-100", "cell-101"],
        "control": ["cell-200"],
        "rotating": [f"cell-3{i:02d}" for i in range(6)],
        "aided": ["cell-400", "cell-401"],
    }
    alloc = allocate_and_price(parts, [], knobs=DesignKnobs()).allocation
    assert alloc.unaided_slots == {"core": 26, "rotating": 6, "sentinel": 2, "control": 1}
    assert alloc.unaided_shares_pct == {
        "core": 74.3,
        "rotating": 17.1,
        "sentinel": 5.7,
        "control": 2.9,
    }
    assert alloc.shares_sum_to_100 is True and alloc.disjoint is True
    assert alloc.prompted_slots == 2
    assert alloc.notices == []
    parts["rotating"].append("cell-001")
    assert allocate_and_price(parts, [], knobs=DesignKnobs()).allocation.disjoint is False


# --- T11 ----------------------------------------------------------------------

REAL = "sha256:" + "a" * 64
APPROVED = [GateDecision(gate=g, status="approved") for g in (1, 2, 3, 4)]


def _panel(core: list[str], **extra: Any) -> dict[str, Any]:
    return {
        "panel_id": "panel-tidewater",
        "version": "0.1.0",
        "partitions": {"core": {"canonical_cell_ids": core}},
        "weight": {
            "exposure": {"method": "equal_within_declared_strata"},
            "priority": {"method": "withheld"},
        },
        "engines": ["chat_gpt", "claude"],
        "limitations": ["Conditional on this panel."],
    } | extra


def test_first_version_is_frozen_only_with_real_hashes_and_four_approved_gates() -> None:
    frozen = freeze_version(
        _panel(["cell-001"]), gates=APPROVED, content_hashes={"panel": REAL}, actor="arman", at=NOW
    )
    assert (frozen.version, frozen.bump, frozen.status) == ("0.1.0", "initial", "frozen")
    pending = freeze_version(
        _panel(["cell-001"]),
        gates=[*APPROVED[:3], GateDecision(gate=4, status="continued_pending")],
        content_hashes={"panel": REAL},
        actor="arman",
        at=NOW,
    )
    assert pending.status == "provisional_directional"
    no_hash = freeze_version(
        _panel(["cell-001"]), gates=APPROVED, content_hashes={"panel": None}, actor="arman", at=NOW
    )
    assert no_hash.status == "provisional_directional"


def test_tracked_set_change_is_a_minor_bump_with_an_overlap_bridge() -> None:
    prior = _panel(["cell-001", "cell-002"], version="1.2.3")
    new = freeze_version(
        _panel(["cell-002", "cell-003"]),
        gates=APPROVED,
        content_hashes={"p": REAL},
        prior_panel=prior,
        actor="arman",
        at=NOW,
    )
    assert new.version == "1.3.0" and new.bump == "minor"
    assert new.overlap_bridge["overlap_canonical_cell_ids"] == ["cell-002"]
    engines = freeze_version(
        _panel(["cell-001", "cell-002"], engines=["chat_gpt"]),
        gates=APPROVED,
        content_hashes={"p": REAL},
        prior_panel=prior,
        actor="arman",
        at=NOW,
    )
    assert engines.version == "1.3.0"


def test_a_non_structural_change_is_a_patch_and_no_change_is_no_version() -> None:
    prior = _panel(["cell-001"], version="1.2.3")
    patch = freeze_version(
        _panel(["cell-001"], limitations=["Gemini runs without city."]),
        gates=APPROVED,
        content_hashes={"p": REAL},
        prior_panel=prior,
        actor="arman",
        at=NOW,
    )
    same = freeze_version(
        _panel(["cell-001"], version="1.2.3"),
        gates=APPROVED,
        content_hashes={"p": REAL},
        prior_panel=prior,
        actor="arman",
        at=NOW,
    )
    assert (patch.version, patch.bump) == ("1.2.4", "patch")
    assert (same.version, same.bump, same.ledger_entry) == ("1.2.3", "none", None)


def test_the_change_ledger_is_append_only() -> None:
    entry = freeze_version(
        _panel(["cell-001"]), gates=APPROVED, content_hashes={"p": REAL}, actor="arman", at=NOW
    ).ledger_entry
    ledger = append_ledger([], entry)
    with pytest.raises(ValueError, match="already in the ledger"):
        append_ledger(ledger, entry)
    edited = [dict(ledger[0], summary="rewritten history")]
    assert ledger_is_append_only(ledger, ledger + [{"change_id": "change-0.2.0"}]) is True
    assert ledger_is_append_only(ledger, edited) is False


# --- T12 ----------------------------------------------------------------------


def _obs(cell: str, mentioned: bool | None, **extra: Any) -> dict[str, Any]:
    return {
        "canonical_cell_id": cell,
        "partition": "core",
        "lane": "retrieval",
        "aided_status": "unaided",
        "engine": "chat_gpt",
        "locale": "en-US",
        "wave_id": "2026-W39",
        "target_mentioned": mentioned,
    } | extra


def _presence(run: Any, lane: str = "retrieval") -> Any:
    return next(
        m for m in run.metrics if m.metric == "unaided_brand_presence" and m.stratum.lane == lane
    )


def test_one_observation_per_slot_uses_wilson() -> None:
    # Worked by hand: 15 of 25, z=1.95996 → Wilson (0.4074, 0.7660).
    obs = [_obs(f"cell-{i:03d}", i < 15) for i in range(25)]
    m = _presence(estimate(obs))
    assert (m.numerator, m.denominator, m.distinct_slots, m.shown_as) == (15, 25, 25, "rate")
    assert m.rate == pytest.approx(0.6)
    assert m.interval.method == "wilson"
    assert (m.interval.low, m.interval.high) == (
        pytest.approx(0.4074, abs=5e-4),
        pytest.approx(0.7660, abs=5e-4),
    )
    assert m.does_not_prove == "market share, awareness, audience reach, or revenue attribution"


def test_repeats_use_a_seeded_slot_cluster_bootstrap_not_a_naive_interval() -> None:
    # Break: treating 3 repeats of a slot as 3 independent buyers. Half the slots are
    # always named, half never: 36 of 72. A naive Wilson on n=72 is (0.388, 0.612);
    # clustering by slot (really n=24) must be clearly wider.
    obs = [_obs(f"cell-{i:03d}", i < 12, repeat_index=r) for i in range(24) for r in range(3)]
    run = estimate(obs, bootstrap_draws=400, seed=11)
    a = _presence(run)
    b = _presence(estimate(obs, bootstrap_draws=400, seed=11))
    assert (run.bootstrap_seed, run.bootstrap_draws) == (11, 400)
    assert a.interval.method == "slot_cluster_bootstrap"
    assert (a.numerator, a.denominator, a.distinct_slots) == (36, 72, 24)
    assert a.interval == b.interval
    assert a.interval.low < 0.36 and a.interval.high > 0.64


def test_below_min_slots_shows_counts_and_no_rate() -> None:
    m = _presence(estimate([_obs(f"cell-{i:03d}", i < 7) for i in range(19)]))
    assert (m.shown_as, m.rate, m.interval, m.numerator, m.denominator) == (
        "counts",
        None,
        None,
        7,
        19,
    )


def test_nothing_valid_is_unmeasured_never_zero() -> None:
    obs = [_obs("cell-001", None), _obs("cell-002", False, validity_status="invalid")]
    m = _presence(estimate(obs))
    assert (m.shown_as, m.numerator, m.denominator, m.rate) == ("unmeasured", None, None, None)
    assert m.invalid_observations == 1


def test_lanes_and_prompted_states_never_share_a_denominator() -> None:
    obs = (
        [_obs(f"cell-{i:03d}", True) for i in range(20)]
        + [_obs(f"cell-{i:03d}", False, lane="closed_model") for i in range(20)]
        + [_obs("cell-900", True, aided_status="target_aided", partition="aided")]
    )
    run = estimate(obs)
    assert _presence(run, "retrieval").rate == 1.0
    assert _presence(run, "closed_model").rate == 0.0
    assert all(
        m.stratum.aided_status == "unaided"
        for m in run.metrics
        if m.metric == "unaided_brand_presence"
    )


def test_share_of_mentions_and_citation_presence_use_their_own_denominators() -> None:
    target = {"entity": "Tidewater E-Cycle", "kind": "target"}
    rival = {"entity": "ShredPoint", "kind": "competitor"}
    obs = [
        _obs(
            f"cell-{i:03d}",
            i < 5,
            entities_mentioned=[target, rival] if i < 5 else [rival],
            citations_exposed=i < 10,
            target_cited=i < 2,
        )
        for i in range(20)
    ]
    run = estimate(obs, min_cells_for_rate=1)
    share = next(m for m in run.metrics if m.metric == "competitive_mention_share")
    cited = next(m for m in run.metrics if m.metric == "citation_presence")
    assert (share.numerator, share.denominator) == (5, 25)
    assert share.interval.method == "slot_cluster_bootstrap"
    assert (cited.numerator, cited.denominator) == (2, 10)


def test_campaign_response_is_not_set_up_without_a_pre_registered_design() -> None:
    [m] = [m for m in estimate([]).metrics if m.metric == "campaign_response"]
    assert (m.shown_as, m.numerator, m.rate) == ("not_set_up", None, None)
    assert m.display_name == METRICS["campaign_response"].display_name


def test_answer_framing_is_reported_per_framing_among_answers_naming_the_target() -> None:
    obs = [
        _obs(f"cell-{i:03d}", i < 4, framings=["certified_data_destruction"] if i < 3 else [])
        for i in range(6)
    ]
    [m] = [
        m
        for m in estimate(
            obs, framing_labels={"certified_data_destruction": "certified data destruction"}
        ).metrics
        if m.metric == "answer_framing"
    ]
    assert (m.numerator, m.denominator) == (3, 4)
    assert m.display_name == "How answers describe you: certified data destruction"


def test_paired_comparison_uses_only_slots_present_in_both_waves() -> None:
    # Overlap cells 5..24 go from absent to named; non-overlap cells would dilute it.
    w1 = [_obs(f"cell-{i:03d}", i < 5, wave_id="2026-W38") for i in range(25)]
    w2 = [_obs(f"cell-{i:03d}", 5 <= i < 25, wave_id="2026-W39") for i in range(5, 30)]
    [cmp] = [
        c
        for c in estimate(w1 + w2, bootstrap_draws=200).comparisons
        if c.metric == "unaided_brand_presence"
    ]
    assert (cmp.from_wave, cmp.to_wave, cmp.overlap_slots) == ("2026-W38", "2026-W39", 20)
    assert cmp.change == pytest.approx(1.0)
    assert cmp.stratum.wave_id is None


# --- T13 ----------------------------------------------------------------------


def test_pilot_plan_is_clamped_and_spreads_across_slot_families() -> None:
    cells = [
        {"canonical_cell_id": f"cell-{b}{i:02d}", "proximity_band": b, "job_id": "job-001"}
        for b in ("B2_category", "B3_problem_need")
        for i in range(15)
    ]
    plan = plan_variance_pilot(
        cells,
        engines=["chat_gpt", "claude"],
        lanes=["retrieval"],
        target_cells=30,
        repeats=4,
        time_blocks=1,
        seed=3,
    )
    assert (len(plan.canonical_cell_ids), plan.repeats, plan.time_blocks) == (20, 6, 2)
    assert sum(c.startswith("cell-B2") for c in plan.canonical_cell_ids) == 10
    assert plan.runs == 20 * 6 * 2 * 2 * 1


def test_variance_decomposition_recommends_slots_or_repeats() -> None:
    stable = [
        _obs(f"cell-{i:03d}", i % 2 == 0, repeat_index=r) for i in range(10) for r in range(6)
    ]
    noisy = [_obs(f"cell-{i:03d}", r % 2 == 0, repeat_index=r) for i in range(10) for r in range(6)]
    assert decompose_variance(stable).recommendation == "more_slots"
    assert decompose_variance(noisy).recommendation == "more_repeats"
    assert decompose_variance([_obs("cell-001", True)]).recommendation == "insufficient_data"


# --- T14 / T15 ------------------------------------------------------------------


def test_entity_mentions_find_target_and_competitors_with_matched_terms() -> None:
    answer = (
        "Options include Tidewater E-Cycle (tidewater-ecycle.com) and ShredPoint; "
        "Harborline is smaller."
    )
    mentions = entity_mentions_from_register(answer, _register(), target_entity="Tidewater E-Cycle")
    assert [(m.entity, m.kind) for m in mentions] == [
        ("Tidewater E-Cycle", "target"),
        ("ShredPoint", "competitor"),
    ]
    assert "tidewater-ecycle.com" in mentions[0].matched_terms


def test_configuration_hash_never_depends_on_secrets_and_hashes_hidden_prompts() -> None:
    base = {"model": "gpt-5.5", "web_search": True, "system_prompt": "Answer plainly."}
    h1, redacted = configuration_hash(base | {"api_key": "live-key-one"})
    h2, _ = configuration_hash(base | {"api_key": "live-key-two"})
    h3, _ = configuration_hash(base | {"system_prompt": "Answer briefly."})
    assert h1 == h2 != h3
    assert redacted == ["system_prompt", "api_key"]


def test_run_manifest_record_has_exactly_the_contract_fields() -> None:
    record = build_run_manifest_record(
        exact_prompt="safest way to dispose of old hard drives",
        config={"model": "claude-sonnet-4-6", "web_search": False, "authorization": "Bearer live"},
        provider="dataforseo",
        model="claude-sonnet-4-6",
        surface="api:claude",
        lane="closed_model",
        locale="en-US",
        retrieval_used=False,
        session_state="fresh",
        response_payload={"text": "Use a certified recycler."},
        citation_payload=None,
        timestamp=NOW,
        retry_status="first_attempt",
        validity_status="valid",
        parser_version="1.0.0",
    )
    assert set(record.model_dump()) == {
        "exact_prompt",
        "configuration_hash",
        "provider",
        "model",
        "surface",
        "lane",
        "locale",
        "search_policy",
        "retrieval_used",
        "session_state",
        "response_payload_hash",
        "citation_payload_hash",
        "timestamp",
        "retry_status",
        "validity_status",
        "parser_version",
    }
    assert record.search_policy == "off"
    assert record.citation_payload_hash is None
    assert "Bearer" not in record.model_dump_json()
