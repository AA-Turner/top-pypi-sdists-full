"""Tests verifying serialization (model_dump, model_validate, etc.) for all public models."""

import json

from agentic_devtools.orchestration.schemas.examples import (
    make_checklist_item,
    make_code_suggestion,
    make_escalation_reason,
    make_file_review_finding,
    make_file_review_result,
    make_implementation_plan,
    make_implementation_summary,
    make_plan_task,
    make_quality_gate_result,
    make_repair_action,
    make_review_decision,
    make_review_summary,
    make_risk_assessment,
    make_stop_condition,
    make_task_dependency,
    make_test_failure_diagnosis,
)


class TestSerialization:
    """Tests verifying round-trip serialization for all public schema models."""

    def _round_trip(self, instance):
        """Verify model_dump → model_validate and model_dump_json → model_validate_json."""
        model_class = type(instance)

        # Dict round-trip
        data = instance.model_dump()
        assert isinstance(data, dict)
        restored = model_class.model_validate(data)
        assert restored == instance

        # JSON round-trip
        json_str = instance.model_dump_json()
        assert isinstance(json_str, str)
        json.loads(json_str)  # Verify it's valid JSON
        restored_json = model_class.model_validate_json(json_str)
        assert restored_json == instance

    def test_code_suggestion(self):
        self._round_trip(make_code_suggestion())

    def test_file_review_finding(self):
        self._round_trip(make_file_review_finding())

    def test_file_review_result(self):
        self._round_trip(make_file_review_result())

    def test_review_decision(self):
        self._round_trip(make_review_decision())

    def test_review_summary(self):
        self._round_trip(make_review_summary())

    def test_implementation_plan(self):
        self._round_trip(make_implementation_plan())

    def test_plan_task(self):
        self._round_trip(make_plan_task())

    def test_task_dependency(self):
        self._round_trip(make_task_dependency())

    def test_risk_assessment(self):
        self._round_trip(make_risk_assessment())

    def test_checklist_item(self):
        self._round_trip(make_checklist_item())

    def test_failure_diagnosis(self):
        self._round_trip(make_test_failure_diagnosis())

    def test_repair_action(self):
        self._round_trip(make_repair_action())

    def test_implementation_summary(self):
        self._round_trip(make_implementation_summary())

    def test_quality_gate_result(self):
        self._round_trip(make_quality_gate_result())

    def test_escalation_reason(self):
        self._round_trip(make_escalation_reason())

    def test_stop_condition(self):
        self._round_trip(make_stop_condition())

    def test_enum_serialized_as_string(self):
        """Verify enums serialize as their string values."""
        finding = make_file_review_finding()
        data = finding.model_dump()
        assert isinstance(data["severity"], str)
        assert data["severity"] == "high"

        decision = make_review_decision()
        data = decision.model_dump()
        assert isinstance(data["verdict"], str)
        assert data["verdict"] == "request_changes"
