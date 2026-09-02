"""Example factories for work-on-issue domain models.

Provides factory functions that return new, realistic instances of work-on-issue models.
"""

from __future__ import annotations

from typing import Any

from ..work_on_issue.checklist import ChecklistItem
from ..work_on_issue.diagnosis import RepairAction, TestFailureDiagnosis
from ..work_on_issue.plan import (
    ImplementationPlan,
    PlanTask,
    RiskAssessment,
    TaskDependency,
)
from ..work_on_issue.quality import QualityGateResult
from ..work_on_issue.summary import ImplementationSummary


def make_task_dependency(**kwargs: Any) -> TaskDependency:
    """Create a realistic TaskDependency instance."""
    defaults: dict[str, Any] = {
        "task_id": "T001",
        "dependency_type": "blocks",
    }
    defaults.update(kwargs)
    return TaskDependency(**defaults)


def make_risk_assessment(**kwargs: Any) -> RiskAssessment:
    """Create a realistic RiskAssessment instance."""
    defaults: dict[str, Any] = {
        "description": "Database migration may cause downtime if table locks are acquired",
        "likelihood": "medium",
        "impact": "high",
        "mitigation": "Use online DDL operations and test migration on staging first",
    }
    defaults.update(kwargs)
    return RiskAssessment(**defaults)


def make_plan_task(**kwargs: Any) -> PlanTask:
    """Create a realistic PlanTask instance."""
    defaults: dict[str, Any] = {
        "task_id": "T002",
        "description": "Add database migration for new user_preferences table",
        "affected_files": [
            "migrations/003_add_user_preferences.sql",
            "src/models/user_preferences.py",
        ],
        "dependencies": [make_task_dependency()],
        "estimated_complexity": "medium",
    }
    defaults.update(kwargs)
    return PlanTask(**defaults)


def make_implementation_plan(**kwargs: Any) -> ImplementationPlan:
    """Create a realistic ImplementationPlan instance."""
    defaults: dict[str, Any] = {
        "summary": "Implement user preferences feature with database storage and API endpoints",
        "tasks": [
            make_plan_task(task_id="T001", description="Create database schema", dependencies=[]),
            make_plan_task(task_id="T002"),
        ],
        "risks": [make_risk_assessment()],
        "estimated_effort": "4-6 hours",
    }
    defaults.update(kwargs)
    return ImplementationPlan(**defaults)


def make_checklist_item(**kwargs: Any) -> ChecklistItem:
    """Create a realistic ChecklistItem instance."""
    defaults: dict[str, Any] = {
        "description": "Implement user preferences API endpoint with CRUD operations",
        "acceptance_criteria": "GET/POST/PUT/DELETE endpoints return correct status codes and persist data",
        "estimated_complexity": "medium",
        "is_complete": False,
    }
    defaults.update(kwargs)
    return ChecklistItem(**defaults)


def make_repair_action(**kwargs: Any) -> RepairAction:
    """Create a realistic RepairAction instance."""
    defaults: dict[str, Any] = {
        "file_path": "src/services/user_service.py",
        "line": 78,
        "original_code": "return self.db.query(User).filter_by(id=user_id)",
        "replacement_code": "return self.db.query(User).filter_by(id=user_id).first()",
        "explanation": "Missing .first() causes the query to return a Query object instead of a User instance",
    }
    defaults.update(kwargs)
    return RepairAction(**defaults)


def make_test_failure_diagnosis(**kwargs: Any) -> TestFailureDiagnosis:
    """Create a realistic TestFailureDiagnosis instance."""
    defaults: dict[str, Any] = {
        "test_name": "tests.test_user_service.TestGetUser.test_returns_user_by_id",
        "error_message": (
            "AssertionError: Expected User(id=1, name='Alice') but got <sqlalchemy.orm.query.Query object>"
        ),
        "root_cause": ("The query method returns a Query object instead of executing and returning the first result."),
        "repair_actions": [make_repair_action()],
    }
    defaults.update(kwargs)
    return TestFailureDiagnosis(**defaults)


def make_implementation_summary(**kwargs: Any) -> ImplementationSummary:
    """Create a realistic ImplementationSummary instance."""
    defaults: dict[str, Any] = {
        "summary": "Implemented user preferences feature with full CRUD API and database storage",
        "files_changed": ["src/services/user_service.py", "src/models/__init__.py"],
        "files_created": [
            "src/models/user_preferences.py",
            "migrations/003_add_user_preferences.sql",
        ],
        "tests_added": [
            "tests/test_user_preferences_api.py",
            "tests/test_user_preferences_model.py",
        ],
        "notes": "Database migration is backward-compatible; rollback script included in migration file.",
    }
    defaults.update(kwargs)
    return ImplementationSummary(**defaults)


def make_quality_gate_result(**kwargs: Any) -> QualityGateResult:
    """Create a realistic QualityGateResult instance."""
    defaults: dict[str, Any] = {
        "gate": "unit_tests",
        "passed": True,
        "details": "All 247 tests passed in 12.3 seconds",
        "metric_value": "247/247",
    }
    defaults.update(kwargs)
    return QualityGateResult(**defaults)
