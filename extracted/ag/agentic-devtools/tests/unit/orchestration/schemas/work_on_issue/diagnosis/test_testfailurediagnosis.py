"""Tests for TestFailureDiagnosis and RepairAction models."""

from agentic_devtools.orchestration.schemas.work_on_issue.diagnosis import (
    RepairAction,
)
from agentic_devtools.orchestration.schemas.work_on_issue.diagnosis import (
    TestFailureDiagnosis as FailureDiagnosis,
)


class TestRepairAction:
    """Tests for RepairAction model."""

    def test_construction(self):
        action = RepairAction(
            file_path="src/main.py",
            replacement_code="fixed code",
        )
        assert action.file_path == "src/main.py"
        assert action.line is None
        assert action.original_code == ""

    def test_full_construction(self):
        action = RepairAction(
            file_path="f.py",
            line=42,
            original_code="old",
            replacement_code="new",
            explanation="Fix bug",
        )
        assert action.line == 42
        assert action.explanation == "Fix bug"


class TestDiagnosisModel:
    """Tests for TestFailureDiagnosis model."""

    def test_construction(self):
        diagnosis = FailureDiagnosis(
            test_name="test_something",
            error_message="AssertionError",
            root_cause="Logic error",
        )
        assert diagnosis.test_name == "test_something"
        assert diagnosis.repair_actions == []

    def test_with_repair_actions(self):
        diagnosis = FailureDiagnosis(
            test_name="test_it",
            error_message="Error",
            root_cause="Bug",
            repair_actions=[
                RepairAction(file_path="f.py", replacement_code="fix"),
            ],
        )
        assert len(diagnosis.repair_actions) == 1

    def test_round_trip(self):
        original = FailureDiagnosis(
            test_name="test_x",
            error_message="err",
            root_cause="cause",
        )
        raw = original.model_dump_json()
        restored = FailureDiagnosis.model_validate_json(raw)
        assert original == restored
