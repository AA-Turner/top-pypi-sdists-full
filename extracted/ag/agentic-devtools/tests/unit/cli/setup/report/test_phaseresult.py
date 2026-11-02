"""Tests for PhaseResult dataclass."""

from agentic_devtools.cli.setup.report import PhaseResult


class TestPhaseResult:
    """PhaseResult construction and field defaults."""

    def test_construction_with_all_fields(self) -> None:
        pr = PhaseResult(name="test_phase", status="success", duration_ms=42, error=None)
        assert pr.name == "test_phase"
        assert pr.status == "success"
        assert pr.duration_ms == 42
        assert pr.error is None

    def test_construction_with_defaults(self) -> None:
        pr = PhaseResult(name="test_phase", status="failed")
        assert pr.duration_ms == 0
        assert pr.error is None

    def test_construction_with_error(self) -> None:
        pr = PhaseResult(name="failing", status="failed", duration_ms=100, error="Something broke")
        assert pr.error == "Something broke"
