"""Adversarial benchmark: a six-lane criteria gate fails closed on unsafe combinations.

Moved from ``aidream/workflows/incident_assurance_benchmark.py`` when Incident
Assurance became a generic workflow (its checklist now lives in the workflow, not in
code). The checklist below is the same twelve-criterion, six-lane shape: the gate is
started at its assurance boundary, so every release cheaply proves that one unmet,
one unknown or one unresolved material contradiction blocks completion — independent
of model availability or phrasing.
"""

from __future__ import annotations

from copy import deepcopy

import pytest

from matrx_graph.nodes.data.criteria_gate import (
    CriteriaGateConfig,
    CriteriaGateInput,
    evaluate_criteria_gate,
)

LANES: dict[str, tuple[str, str]] = {
    "evidence_provenance": ("EV_PROVENANCE", "EV_GAPS"),
    "technical_timeline": ("TECH_TIMELINE", "TECH_ROOT_CAUSE"),
    "scope_impact": ("SCOPE_BOUNDARY", "MISSION_IMPACT"),
    "containment_eradication": ("CONTAINMENT_PLAN", "ERADICATION_VERIFIED"),
    "recovery_readiness": ("RECOVERY_ASSET_INTEGRITY", "RECOVERY_MONITORING"),
    "authority_notifications": ("AUTHORITY_IDENTIFIED", "NOTIFICATION_OBLIGATIONS"),
}


def _config() -> CriteriaGateConfig:
    return CriteriaGateConfig.model_validate(
        {
            "criteria": [
                {"criterion_id": c, "label": c, "required": True, "evidence_required": True}
                for criteria in LANES.values()
                for c in criteria
            ],
            "required_evaluator_ids": list(LANES),
            "block_on_not_met": True,
            "block_on_unknown": True,
            "block_on_unresolved_material_contradictions": True,
        }
    )


def _clean() -> list[dict]:
    return [
        {
            "__kind": "criteria_bundle",
            "evaluator_id": lane,
            "available_evidence_refs": [f"evidence:{lane}:{c.lower()}" for c in criteria],
            "assessments": [
                {
                    "criterion_id": c,
                    "verdict": "met",
                    "evidence_refs": [f"evidence:{lane}:{c.lower()}"],
                    "rationale": "The sealed incident record supports this criterion.",
                    "evaluator_id": lane,
                    "confidence": 0.95,
                }
                for c in criteria
            ],
            "contradictions": [],
        }
        for lane, criteria in LANES.items()
    ]


def _set(bundles: list[dict], criterion_id: str, verdict: str) -> list[dict]:
    for bundle in bundles:
        for assessment in bundle["assessments"]:
            if assessment["criterion_id"] == criterion_id:
                assessment["verdict"] = verdict
    return bundles


def _contradict(bundles: list[dict], lane: str, criterion_ids: list[str]) -> list[dict]:
    bundle = next(b for b in bundles if b["evaluator_id"] == lane)
    bundle["contradictions"].append(
        {
            "contradiction_id": f"contradiction:{lane}",
            "criterion_ids": criterion_ids,
            "evidence_refs": [bundle["available_evidence_refs"][0]],
            "description": "Two pieces of evidence disagree on a material fact.",
            "material": True,
            "resolved": False,
            "disposition": None,
        }
    )
    return bundles


CASES = [
    ("complete and consistent", lambda b: b, set()),
    (
        "recovery from an unverified backup",
        lambda b: _set(b, "RECOVERY_ASSET_INTEGRITY", "not_met"),
        {"required_criterion_not_met"},
    ),
    (
        "notification obligations unknown",
        lambda b: _set(b, "NOTIFICATION_OBLIGATIONS", "unknown"),
        {"required_criterion_unknown"},
    ),
    (
        "tainted primary evidence",
        lambda b: _contradict(b, "evidence_provenance", ["EV_PROVENANCE", "TECH_TIMELINE"]),
        {"unresolved_material_contradiction"},
    ),
    (
        "new indicator after restore",
        lambda b: _contradict(
            _set(b, "RECOVERY_MONITORING", "not_met"),
            "recovery_readiness",
            ["RECOVERY_MONITORING", "ERADICATION_VERIFIED"],
        ),
        {"required_criterion_not_met", "unresolved_material_contradiction"},
    ),
    (
        "one lane never answered",
        lambda b: b[1:],
        {"missing_evaluator_bundle", "missing_assessment"},
    ),
]


@pytest.mark.parametrize(("title", "mutate", "codes"), CASES, ids=[c[0] for c in CASES])
def test_the_gate_blocks_exactly_the_unsafe_cases(title, mutate, codes) -> None:
    bundles = mutate(deepcopy(_clean()))
    _, violations = evaluate_criteria_gate(
        CriteriaGateInput.model_validate({"bundles": bundles}), _config()
    )
    assert {v.code for v in violations} == codes, title
