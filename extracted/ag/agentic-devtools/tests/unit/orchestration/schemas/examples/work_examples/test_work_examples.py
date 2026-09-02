"""Tests for work-on-issue domain example factories."""

from agentic_devtools.orchestration.schemas.examples import (
    make_checklist_item,
    make_implementation_plan,
    make_implementation_summary,
    make_quality_gate_result,
    make_test_failure_diagnosis,
)
from agentic_devtools.orchestration.schemas.work_on_issue import (
    ChecklistItem,
    ImplementationPlan,
    ImplementationSummary,
    QualityGateResult,
)
from agentic_devtools.orchestration.schemas.work_on_issue import (
    TestFailureDiagnosis as FailureDiagnosis,
)


class TestWorkExamples:
    """Tests for work-on-issue domain example factories."""

    def test_make_implementation_plan_returns_valid(self):
        result = make_implementation_plan()
        assert isinstance(result, ImplementationPlan)
        assert len(result.tasks) > 0

    def test_make_checklist_item_returns_valid(self):
        result = make_checklist_item()
        assert isinstance(result, ChecklistItem)

    def test_make_test_failure_diagnosis_returns_valid(self):
        result = make_test_failure_diagnosis()
        assert isinstance(result, FailureDiagnosis)

    def test_make_quality_gate_result_returns_valid(self):
        result = make_quality_gate_result()
        assert isinstance(result, QualityGateResult)

    def test_make_implementation_summary_returns_valid(self):
        result = make_implementation_summary()
        assert isinstance(result, ImplementationSummary)

    def test_factories_return_new_instances(self):
        a = make_checklist_item()
        b = make_checklist_item()
        assert a is not b

    def test_kwargs_override(self):
        result = make_checklist_item(description="Custom task")
        assert result.description == "Custom task"
