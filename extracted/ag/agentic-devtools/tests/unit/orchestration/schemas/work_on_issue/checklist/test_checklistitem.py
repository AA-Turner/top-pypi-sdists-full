"""Tests for ChecklistItem model."""

from agentic_devtools.orchestration.schemas.work_on_issue.checklist import ChecklistItem


class TestChecklistItem:
    """Tests for ChecklistItem construction and serialization."""

    def test_construction(self):
        item = ChecklistItem(
            description="Implement API",
            acceptance_criteria="Passes all tests",
        )
        assert item.description == "Implement API"
        assert item.estimated_complexity == "medium"
        assert item.is_complete is False

    def test_model_dump(self):
        item = ChecklistItem(
            description="Write tests",
            acceptance_criteria="100% coverage",
            estimated_complexity="high",
            is_complete=True,
        )
        data = item.model_dump()
        assert data["is_complete"] is True
        assert data["estimated_complexity"] == "high"

    def test_round_trip(self):
        original = ChecklistItem(
            description="Task",
            acceptance_criteria="Done",
        )
        raw = original.model_dump_json()
        restored = ChecklistItem.model_validate_json(raw)
        assert original == restored

    def test_rejects_invalid_complexity(self):
        from pydantic import ValidationError

        try:
            ChecklistItem(
                description="Task",
                acceptance_criteria="Done",
                estimated_complexity="extreme",
            )
        except ValidationError as exc:
            assert any(error["loc"] == ("estimated_complexity",) for error in exc.errors())
        else:
            raise AssertionError("Expected ValidationError for invalid complexity")
