"""Tests for ImplementationPlan model."""

import json

from agentic_devtools.orchestration.schemas.work_on_issue.plan import (
    ImplementationPlan,
    PlanTask,
    RiskAssessment,
    TaskDependency,
)


class TestImplementationPlan:
    """Tests for ImplementationPlan construction and serialization."""

    def test_construction(self):
        plan = ImplementationPlan(
            summary="Add user preferences",
            tasks=[
                PlanTask(task_id="T1", description="Create schema"),
            ],
        )
        assert plan.summary == "Add user preferences"
        assert len(plan.tasks) == 1

    def test_nested_models(self):
        plan = ImplementationPlan(
            summary="Complex plan",
            tasks=[
                PlanTask(
                    task_id="T1",
                    description="First task",
                    affected_files=["a.py"],
                    dependencies=[TaskDependency(task_id="T0")],
                    estimated_complexity="high",
                ),
            ],
            risks=[
                RiskAssessment(
                    description="Risk",
                    likelihood="high",
                    impact="medium",
                    mitigation="Test first",
                ),
            ],
            estimated_effort="2 hours",
        )
        assert plan.tasks[0].dependencies[0].task_id == "T0"
        assert plan.risks[0].mitigation == "Test first"

    def test_model_dump(self):
        plan = ImplementationPlan(
            summary="Test",
            tasks=[PlanTask(task_id="T1", description="Do thing")],
        )
        data = plan.model_dump()
        assert data["summary"] == "Test"
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["task_id"] == "T1"

    def test_round_trip(self):
        original = ImplementationPlan(
            summary="Plan",
            tasks=[PlanTask(task_id="T1", description="Task")],
            risks=[],
        )
        raw = original.model_dump_json()
        restored = ImplementationPlan.model_validate_json(raw)
        assert original == restored

    def test_validate_from_json(self):
        raw = json.dumps(
            {
                "summary": "From JSON",
                "tasks": [
                    {
                        "task_id": "T1",
                        "description": "JSON task",
                        "affected_files": ["x.py"],
                        "dependencies": [],
                        "estimated_complexity": "low",
                    }
                ],
                "risks": [],
                "estimated_effort": "1h",
            }
        )
        plan = ImplementationPlan.model_validate_json(raw)
        assert plan.tasks[0].estimated_complexity == "low"

    def test_rejects_invalid_constrained_values(self):
        from pydantic import ValidationError

        try:
            ImplementationPlan(
                summary="Bad plan",
                tasks=[
                    {
                        "task_id": "T1",
                        "description": "Task",
                        "dependencies": [{"task_id": "T0", "dependency_type": "unknown"}],
                        "estimated_complexity": "extreme",
                    }
                ],
                risks=[
                    {
                        "description": "Risk",
                        "likelihood": "possible",
                        "impact": "severe",
                    }
                ],
            )
        except ValidationError as exc:
            error_locations = {error["loc"] for error in exc.errors()}
            assert ("tasks", 0, "dependencies", 0, "dependency_type") in error_locations
            assert ("tasks", 0, "estimated_complexity") in error_locations
            assert ("risks", 0, "likelihood") in error_locations
            assert ("risks", 0, "impact") in error_locations
        else:
            raise AssertionError("Expected ValidationError for invalid constrained values")
