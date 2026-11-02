"""Tests for SetupReport dataclass."""

import pytest

from agentic_devtools.cli.setup.report import PhaseResult, SetupReport, make_report


class TestSetupReport:
    """SetupReport construction and serialization."""

    def test_construction(self) -> None:
        report = SetupReport(
            schema_version=1,
            timestamp="2026-01-15T10:00:00+00:00",
            exit_code=0,
            exit_code_name="OK",
            phases=[],
            details={},
        )
        assert report.schema_version == 1
        assert report.exit_code == 0
        assert report.exit_code_name == "OK"

    def test_to_dict_serialization(self) -> None:
        report = SetupReport(
            schema_version=1,
            timestamp="2026-01-15T10:00:00+00:00",
            exit_code=10,
            exit_code_name="VERSION_BLOCKED",
            phases=[PhaseResult(name="version_check", status="failed", duration_ms=5, error="blocked")],
            details={"detected_version": "1.0.0"},
        )
        d = report.to_dict()
        assert d["schema_version"] == 1
        assert d["exit_code"] == 10
        assert d["exit_code_name"] == "VERSION_BLOCKED"
        assert len(d["phases"]) == 1
        assert d["phases"][0]["name"] == "version_check"
        assert d["details"]["detected_version"] == "1.0.0"

    def test_make_report_sets_exit_code_name(self) -> None:
        report = make_report(exit_code=0)
        assert report.exit_code_name == "OK"
        assert report.schema_version == 1
        assert report.timestamp  # non-empty

    def test_make_report_with_phases(self) -> None:
        phases = [PhaseResult(name="test", status="success", duration_ms=1)]
        report = make_report(exit_code=0, phases=phases)
        assert len(report.phases) == 1

    def test_to_dict_serializes_details(self) -> None:
        report = make_report(exit_code=99, details={"error_type": "RuntimeError"})
        d = report.to_dict()
        assert d["details"] == {"error_type": "RuntimeError"}

    def test_make_report_mode_default(self) -> None:
        report = make_report(exit_code=0)
        assert report.mode == "setup"

    def test_make_report_mode_and_git_root(self) -> None:
        report = make_report(exit_code=0, mode="check", git_root="/tmp/repo")
        assert report.mode == "check"
        assert report.git_root == "/tmp/repo"

    def test_make_report_raises_on_invalid_mode(self) -> None:
        with pytest.raises(
            ValueError,
            match=r"Invalid setup report mode: 'chec'.*Expected one of: setup, check, check-fix, dry-run",
        ):
            make_report(exit_code=0, mode="chec")

    def test_autorun_enabled_field_default_none(self) -> None:
        report = SetupReport(
            schema_version=1,
            timestamp="2026-01-15T10:00:00+00:00",
            exit_code=0,
            exit_code_name="OK",
        )
        assert report.autorun_enabled is None

    def test_autorun_enabled_true_in_to_dict(self) -> None:
        report = SetupReport(
            schema_version=1,
            timestamp="2026-01-15T10:00:00+00:00",
            exit_code=0,
            exit_code_name="OK",
            autorun_enabled=True,
        )
        assert report.autorun_enabled is True
        d = report.to_dict()
        assert d["autorun_enabled"] is True

    def test_autorun_enabled_false_in_to_dict(self) -> None:
        report = SetupReport(
            schema_version=1,
            timestamp="2026-01-15T10:00:00+00:00",
            exit_code=0,
            exit_code_name="OK",
            autorun_enabled=False,
        )
        assert report.autorun_enabled is False
        d = report.to_dict()
        assert d["autorun_enabled"] is False

    def test_set_refresh_outcome_stores_serialized_dict(self) -> None:
        """set_refresh_outcome stores the serialized outcome under details.refresh_outcome."""
        from agentic_devtools.cli.setup.refresh_outcome import RefreshOutcome

        report = SetupReport(
            schema_version=1,
            timestamp="2026-01-15T10:00:00+00:00",
            exit_code=0,
            exit_code_name="OK",
        )
        report.set_refresh_outcome(RefreshOutcome.success())
        assert report.details["refresh_outcome"] == {
            "status": "success",
            "reason": None,
            "error": None,
        }
        assert report.to_dict()["details"]["refresh_outcome"]["status"] == "success"

    def test_set_refresh_outcome_failed(self) -> None:
        """set_refresh_outcome preserves reason and error for a failed outcome."""
        from agentic_devtools.cli.setup.refresh_outcome import RefreshOutcome

        report = SetupReport(
            schema_version=1,
            timestamp="2026-01-15T10:00:00+00:00",
            exit_code=0,
            exit_code_name="OK",
        )
        report.set_refresh_outcome(RefreshOutcome.failed("provider_unreachable", "boom"))
        assert report.details["refresh_outcome"] == {
            "status": "failed",
            "reason": "provider_unreachable",
            "error": "boom",
        }
