"""Tests for ImplementationSummary model."""

from agentic_devtools.orchestration.schemas.work_on_issue.summary import ImplementationSummary


class TestImplementationSummary:
    """Tests for ImplementationSummary construction and serialization."""

    def test_construction(self):
        summary = ImplementationSummary(summary="Done")
        assert summary.summary == "Done"
        assert summary.files_changed == []
        assert summary.files_created == []
        assert summary.tests_added == []
        assert summary.notes == ""

    def test_full_construction(self):
        summary = ImplementationSummary(
            summary="Implemented feature",
            files_changed=["a.py"],
            files_created=["b.py"],
            tests_added=["test_b.py"],
            notes="Edge case handled",
        )
        assert len(summary.files_changed) == 1
        assert summary.notes == "Edge case handled"

    def test_model_dump(self):
        summary = ImplementationSummary(summary="Test")
        data = summary.model_dump()
        assert data["summary"] == "Test"
        assert data["files_changed"] == []

    def test_round_trip(self):
        original = ImplementationSummary(
            summary="Work",
            files_changed=["x.py"],
        )
        raw = original.model_dump_json()
        restored = ImplementationSummary.model_validate_json(raw)
        assert original == restored
