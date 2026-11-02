"""Example fixture factories for all structured LLM output schema models.

Provides factory functions that return new, realistic instances for testing.
Each factory returns a new instance per call and supports keyword argument overrides.
"""

from .review_examples import (
    make_code_suggestion,
    make_file_review_finding,
    make_file_review_result,
    make_review_decision,
    make_review_summary,
)
from .shared_examples import (
    make_confidence_score,
    make_escalation_reason,
    make_stop_condition,
)
from .work_examples import (
    make_checklist_item,
    make_implementation_plan,
    make_implementation_summary,
    make_plan_task,
    make_quality_gate_result,
    make_repair_action,
    make_risk_assessment,
    make_task_dependency,
    make_test_failure_diagnosis,
)

__all__ = [
    "make_checklist_item",
    "make_code_suggestion",
    "make_confidence_score",
    "make_escalation_reason",
    "make_file_review_finding",
    "make_file_review_result",
    "make_implementation_plan",
    "make_implementation_summary",
    "make_plan_task",
    "make_quality_gate_result",
    "make_repair_action",
    "make_review_decision",
    "make_review_summary",
    "make_risk_assessment",
    "make_stop_condition",
    "make_task_dependency",
    "make_test_failure_diagnosis",
]
