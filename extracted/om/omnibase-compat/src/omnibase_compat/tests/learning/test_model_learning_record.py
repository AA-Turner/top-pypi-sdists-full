# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Tests for ModelLearningRecord and its enums — OMN-14039."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from omnibase_compat.learning import (
    EnumFailureClass,
    EnumLearningOutcome,
    EnumLearningProcessId,
    ModelLearningRecord,
)


def _make_record(**kwargs: Any) -> ModelLearningRecord:
    defaults: dict[str, Any] = {
        "process_id": EnumLearningProcessId.MERGE_SWEEP,
        "context_key": {"repo": "omnibase_infra", "check_name": "pytest"},
        "outcome": EnumLearningOutcome.SUCCESS,
        "evidence_ref": "https://github.com/OmniNode-ai/omnibase_infra/pull/1",
        "recorded_at": datetime(2026, 7, 6, tzinfo=UTC),
    }
    defaults.update(kwargs)
    return ModelLearningRecord(**defaults)


@pytest.mark.unit
def test_learning_process_id_is_stable() -> None:
    assert "merge_sweep" in EnumLearningProcessId._value2member_map_
    assert "delegation" in EnumLearningProcessId._value2member_map_
    assert "dispatch_worker" in EnumLearningProcessId._value2member_map_
    assert "ci_fix" in EnumLearningProcessId._value2member_map_
    assert "steel" in EnumLearningProcessId._value2member_map_
    assert "plan_governor" in EnumLearningProcessId._value2member_map_


@pytest.mark.unit
def test_failure_class_taxonomy_is_stable() -> None:
    expected = {
        "network_egress_timeout",
        "runner_capacity_starvation",
        "queue_scheduling_stall",
        "flaky_check_cancelled",
        "genuine_code_failure",
        "contract_gate_violation",
        "occ_companion_defect",
        "env_install_drift",
        "auth_scope_missing",
        "upstream_throttle",
    }
    assert expected == set(EnumFailureClass._value2member_map_)


@pytest.mark.unit
def test_learning_record_requires_process_id() -> None:
    with pytest.raises(ValidationError):
        ModelLearningRecord(  # type: ignore[call-arg]
            context_key={"repo": "omnibase_infra"},
            outcome=EnumLearningOutcome.SUCCESS,
            evidence_ref="https://example.invalid/pr/1",
            recorded_at=datetime(2026, 7, 6, tzinfo=UTC),
        )


@pytest.mark.unit
def test_learning_record_frozen() -> None:
    record = _make_record()
    with pytest.raises(ValidationError):
        record.outcome = EnumLearningOutcome.FAILURE


@pytest.mark.unit
def test_learning_record_extra_fields_forbidden() -> None:
    with pytest.raises(ValidationError):
        _make_record(unknown_field="oops")


@pytest.mark.unit
def test_learning_record_defaults() -> None:
    record = _make_record()
    assert record.failure_class is None
    assert record.remedy is None
    assert record.remedy_recipe_id is None


@pytest.mark.unit
def test_learning_record_context_key_must_be_non_empty() -> None:
    with pytest.raises(ValidationError, match="context_key must have at least one dimension"):
        _make_record(context_key={})


@pytest.mark.unit
def test_learning_record_evidence_ref_must_be_non_empty() -> None:
    with pytest.raises(ValidationError):
        _make_record(evidence_ref="")


@pytest.mark.unit
def test_failure_class_required_when_outcome_failure() -> None:
    with pytest.raises(ValidationError, match="failure_class is required"):
        _make_record(outcome=EnumLearningOutcome.FAILURE, failure_class=None)


@pytest.mark.unit
def test_failure_class_forbidden_when_outcome_success() -> None:
    with pytest.raises(ValidationError, match="failure_class must be None"):
        _make_record(
            outcome=EnumLearningOutcome.SUCCESS,
            failure_class=EnumFailureClass.GENUINE_CODE_FAILURE,
        )


@pytest.mark.unit
def test_learning_record_full_failure_fields() -> None:
    record = _make_record(
        process_id=EnumLearningProcessId.DISPATCH_WORKER,
        context_key={"repo": "omnibase_infra", "task_class": "fix"},
        outcome=EnumLearningOutcome.FAILURE,
        failure_class=EnumFailureClass.RUNNER_CAPACITY_STARVATION,
        remedy="scaled runner pool",
        remedy_recipe_id="recipe-runner-scale-01",
    )
    assert record.process_id == EnumLearningProcessId.DISPATCH_WORKER
    assert record.failure_class == EnumFailureClass.RUNNER_CAPACITY_STARVATION
    assert record.remedy == "scaled runner pool"
    assert record.remedy_recipe_id == "recipe-runner-scale-01"


@pytest.mark.unit
def test_learning_record_context_key_values_are_strings() -> None:
    record = _make_record(context_key={"task_type": "code_review", "model_tier": "local"})
    assert record.context_key == {"task_type": "code_review", "model_tier": "local"}
