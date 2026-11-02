from __future__ import annotations

import pytest
from pydantic import ValidationError

from matrx_graph.nodes.data.criteria_gate import (
    CriteriaGateConfig,
    CriteriaGateExecutor,
    CriteriaGateInput,
)
from matrx_graph.types.result import Failure, Success


def _config() -> CriteriaGateConfig:
    return CriteriaGateConfig.model_validate(
        {
            "criteria": [
                {"criterion_id": "evidence", "label": "Evidence preserved"},
                {"criterion_id": "recovery", "label": "Recovery verified"},
            ]
        }
    )


def _inputs() -> CriteriaGateInput:
    return CriteriaGateInput.model_validate(
        {
            "available_evidence_refs": ["ev-log", "ev-backup"],
            "assessments": [
                {
                    "criterion_id": "recovery",
                    "verdict": "met",
                    "evidence_refs": ["ev-backup"],
                    "rationale": "The restoration asset passed integrity checks.",
                    "evaluator_id": "recovery-lane",
                    "confidence": 0.98,
                },
                {
                    "criterion_id": "evidence",
                    "verdict": "met",
                    "evidence_refs": ["ev-log"],
                    "rationale": "The acquisition record contains provenance fields.",
                    "evaluator_id": "evidence-lane",
                    "confidence": 0.96,
                },
            ],
        }
    )


@pytest.mark.asyncio
async def test_gate_pass_requires_every_declared_criterion_exactly_once() -> None:
    result = await CriteriaGateExecutor().execute(None, _inputs(), _config())  # type: ignore[arg-type]

    assert isinstance(result, Success)
    assert [item.criterion_id for item in result.result.criteria] == ["evidence", "recovery"]
    assert result.result.required_count == 2
    assert result.result.assessed_count == 2


@pytest.mark.asyncio
async def test_gate_blocks_missing_duplicate_unknown_and_unresolved_contradiction() -> None:
    payload = _inputs().model_dump(mode="json")
    payload["assessments"] = [payload["assessments"][0], payload["assessments"][0]]
    payload["assessments"][0]["evidence_refs"] = ["missing-evidence"]
    payload["contradictions"] = [
        {
            "contradiction_id": "conflict-1",
            "criterion_ids": ["recovery"],
            "evidence_refs": ["ev-backup"],
            "description": "A new indicator conflicts with the recovery verdict.",
            "material": True,
            "resolved": False,
        }
    ]

    result = await CriteriaGateExecutor().execute(
        None,
        CriteriaGateInput.model_validate(payload),
        _config(),  # type: ignore[arg-type]
    )

    assert isinstance(result, Failure)
    assert result.error.code == "criteria_gate_blocked"
    report = result.error.details["report"]  # type: ignore[index]
    codes = {violation["code"] for violation in report["violations"]}
    assert codes == {
        "duplicate_assessment",
        "missing_assessment",
        "unknown_evidence_reference",
        "unresolved_material_contradiction",
    }
    assert report["verdict"] == "blocked"


def test_gate_configuration_rejects_duplicate_criterion_ids() -> None:
    with pytest.raises(ValidationError, match="duplicate criterion ids: evidence"):
        CriteriaGateConfig.model_validate(
            {
                "criteria": [
                    {"criterion_id": "evidence", "label": "One"},
                    {"criterion_id": "evidence", "label": "Two"},
                ]
            }
        )


@pytest.mark.asyncio
async def test_gate_flattens_parallel_bundles_and_requires_every_lane_once() -> None:
    config = CriteriaGateConfig.model_validate(
        {
            "criteria": [
                {"criterion_id": "scope", "label": "Scope established"},
                {"criterion_id": "authority", "label": "Authority confirmed"},
            ],
            "required_evaluator_ids": ["technical", "authority"],
        }
    )
    inputs = CriteriaGateInput.model_validate(
        {
            "bundles": [
                {
                    "evaluator_id": "technical",
                    "available_evidence_refs": ["ev-1"],
                    "assessments": [
                        {
                            "criterion_id": "scope",
                            "verdict": "met",
                            "evidence_refs": ["ev-1"],
                            "rationale": "Confirmed by the incident timeline.",
                            "evaluator_id": "technical",
                            "confidence": 0.9,
                        }
                    ],
                },
                {
                    "evaluator_id": "authority",
                    "available_evidence_refs": ["ev-2"],
                    "assessments": [
                        {
                            "criterion_id": "authority",
                            "verdict": "met",
                            "evidence_refs": ["ev-2"],
                            "rationale": "Named approver is in the packet.",
                            "evaluator_id": "authority",
                            "confidence": 0.95,
                        }
                    ],
                },
            ]
        }
    )

    result = await CriteriaGateExecutor().execute(None, inputs, config)  # type: ignore[arg-type]

    assert isinstance(result, Success)
    assert result.result.assessed_count == 2
    assert result.result.evidence_reference_count == 2


@pytest.mark.asyncio
async def test_gate_blocks_missing_duplicate_or_mismatched_parallel_lanes() -> None:
    config = CriteriaGateConfig.model_validate(
        {
            "criteria": [{"criterion_id": "scope", "label": "Scope established"}],
            "required_evaluator_ids": ["technical", "authority"],
        }
    )
    bundle = {
        "evaluator_id": "technical",
        "available_evidence_refs": ["ev-1"],
        "assessments": [
            {
                "criterion_id": "scope",
                "verdict": "met",
                "evidence_refs": ["ev-1"],
                "rationale": "Timeline evidence.",
                "evaluator_id": "authority",
                "confidence": 0.8,
            }
        ],
    }
    inputs = CriteriaGateInput.model_validate({"bundles": [bundle, bundle]})

    result = await CriteriaGateExecutor().execute(None, inputs, config)  # type: ignore[arg-type]

    assert isinstance(result, Failure)
    codes = {
        violation["code"]
        for violation in result.error.details["report"]["violations"]  # type: ignore[index]
    }
    assert "missing_evaluator_bundle" in codes
    assert "duplicate_evaluator_bundle" in codes
    assert "assessment_evaluator_mismatch" in codes
