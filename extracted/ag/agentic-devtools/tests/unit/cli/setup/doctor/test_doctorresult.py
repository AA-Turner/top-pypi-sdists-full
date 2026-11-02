"""Tests for DoctorResult and RepairOutcome dataclasses."""

from agentic_devtools.cli.setup.dependency_checker import DependencyStatus
from agentic_devtools.cli.setup.doctor import DoctorResult, RepairOutcome
from agentic_devtools.cli.setup.exit_codes import ExitCode
from agentic_devtools.cli.setup.fixloop import ErrorClass
from agentic_devtools.cli.setup.report import make_report


def _make_status(name: str = "git", *, required: bool = True, found: bool = False) -> DependencyStatus:
    return DependencyStatus(name=name, found=found, required=required)


def _make_report(exit_code: int = 0, mode: str = "check"):
    return make_report(exit_code, mode=mode)


class TestRepairOutcome:
    """RepairOutcome dataclass stores repair attempt details correctly."""

    def test_successful_repair_outcome(self):
        """success=True and no error_message for a successful repair."""
        dep = _make_status()
        outcome = RepairOutcome(
            error_class=ErrorClass.MISSING_DEPENDENCY,
            dependency=dep,
            success=True,
        )
        assert outcome.success is True
        assert outcome.error_message is None
        assert outcome.error_class is ErrorClass.MISSING_DEPENDENCY
        assert outcome.dependency is dep

    def test_failed_repair_outcome(self):
        """success=False and error_message stored for a failed repair."""
        dep = _make_status()
        outcome = RepairOutcome(
            error_class=ErrorClass.MISSING_DEPENDENCY,
            dependency=dep,
            success=False,
            error_message="network unreachable",
        )
        assert outcome.success is False
        assert outcome.error_message == "network unreachable"


class TestDoctorResult:
    """DoctorResult dataclass stores report, problems, and repair outcomes."""

    def test_defaults_have_empty_lists(self):
        """problems and repair_outcomes default to empty lists."""
        report = _make_report()
        result = DoctorResult(report=report)
        assert result.problems == []
        assert result.repair_outcomes == []

    def test_stores_problems(self):
        """problems list is preserved as-is."""
        dep = _make_status()
        report = _make_report(exit_code=ExitCode.MISSING_REQUIRED_DEP.value)
        result = DoctorResult(report=report, problems=[dep])
        assert result.problems == [dep]

    def test_stores_repair_outcomes(self):
        """repair_outcomes list is preserved as-is."""
        dep = _make_status()
        outcome = RepairOutcome(
            error_class=ErrorClass.MISSING_DEPENDENCY,
            dependency=dep,
            success=True,
        )
        report = _make_report()
        result = DoctorResult(report=report, repair_outcomes=[outcome])
        assert result.repair_outcomes == [outcome]

    def test_report_mode_check(self):
        """Report mode 'check' is preserved on the result."""
        report = _make_report(mode="check")
        result = DoctorResult(report=report)
        assert result.report.mode == "check"

    def test_report_mode_check_fix(self):
        """Report mode 'check-fix' is preserved on the result."""
        report = _make_report(mode="check-fix")
        result = DoctorResult(report=report)
        assert result.report.mode == "check-fix"
