"""A typed agent's evaluator packet feeds the criteria gate as-is.

``criteria_bundle`` is the kind a Run Typed Agent step answers in when it assesses
one lane of a fail-closed gate. Its answer carries ``__kind`` (content-ir rule 1),
so the gate must accept a bundle that names its kind, and refuse one that names a
different kind.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from matrx_graph.nodes.data.criteria_gate import (
    CriteriaBundle,
    CriteriaGateConfig,
    CriteriaGateExecutor,
    CriteriaGateInput,
)
from matrx_graph.types.result import Failure, Success


def _bundle(**extra: object) -> dict[str, object]:
    return {
        **extra,
        "evaluator_id": "lane-a",
        "available_evidence_refs": ["ev-1"],
        "assessments": [
            {
                "criterion_id": "c1",
                "verdict": "met",
                "evidence_refs": ["ev-1"],
                "rationale": "observed_fact: the log shows it.",
                "evaluator_id": "lane-a",
                "confidence": 0.9,
            }
        ],
        "contradictions": [],
    }


def test_the_bundle_is_the_registered_kind_criteria_bundle() -> None:
    assert CriteriaBundle.kind_slug == "criteria_bundle"
    schema = CriteriaBundle.model_json_schema(by_alias=True)
    assert schema["properties"]["__kind"]["const"] == "criteria_bundle"


@pytest.mark.asyncio
async def test_a_typed_agent_answer_passes_the_gate_unchanged() -> None:
    config = CriteriaGateConfig.model_validate(
        {"criteria": [{"criterion_id": "c1", "label": "One"}], "required_evaluator_ids": ["lane-a"]}
    )
    inputs = CriteriaGateInput.model_validate({"bundles": [_bundle(__kind="criteria_bundle")]})
    result = await CriteriaGateExecutor().execute(None, inputs, config)  # type: ignore[arg-type]
    assert isinstance(result, Success), result


@pytest.mark.asyncio
async def test_a_blocked_lane_still_fails_closed() -> None:
    config = CriteriaGateConfig.model_validate(
        {
            "criteria": [{"criterion_id": "c1", "label": "One"}],
            "required_evaluator_ids": ["lane-a", "lane-b"],
        }
    )
    inputs = CriteriaGateInput.model_validate({"bundles": [_bundle(__kind="criteria_bundle")]})
    result = await CriteriaGateExecutor().execute(None, inputs, config)  # type: ignore[arg-type]
    assert isinstance(result, Failure)


def test_a_bundle_naming_another_kind_is_refused() -> None:
    with pytest.raises(ValidationError):
        CriteriaGateInput.model_validate({"bundles": [_bundle(__kind="criterion_coverage")]})
