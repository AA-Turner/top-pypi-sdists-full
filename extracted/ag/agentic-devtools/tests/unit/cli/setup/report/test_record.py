"""Tests for SetupReport.record() method."""

from agentic_devtools.cli.setup.report import PhaseResult, SetupReport


class TestRecord:
    """SetupReport.record() ordered-dict dedup semantics."""

    def _make_report(self) -> SetupReport:
        return SetupReport(
            schema_version=1,
            timestamp="2026-01-15T10:00:00+00:00",
            exit_code=0,
            exit_code_name="OK",
        )

    def test_record_appends_new_phase(self) -> None:
        report = self._make_report()
        report.record(PhaseResult(name="version_check", status="success", duration_ms=10))
        assert len(report.phases) == 1
        assert report.phases[0].name == "version_check"
        assert report.phases[0].status == "success"

    def test_record_updates_existing_phase_in_place(self) -> None:
        report = self._make_report()
        report.record(PhaseResult(name="version_check", status="success", duration_ms=10))
        report.record(PhaseResult(name="version_check", status="failed", duration_ms=20, error="timeout"))
        assert len(report.phases) == 1
        assert report.phases[0].status == "failed"
        assert report.phases[0].duration_ms == 20
        assert report.phases[0].error == "timeout"

    def test_record_preserves_first_seen_order(self) -> None:
        report = self._make_report()
        report.record(PhaseResult(name="a", status="success"))
        report.record(PhaseResult(name="b", status="success"))
        report.record(PhaseResult(name="c", status="success"))
        # Update 'a' — should stay at index 0
        report.record(PhaseResult(name="a", status="failed"))
        assert [p.name for p in report.phases] == ["a", "b", "c"]
        assert report.phases[0].status == "failed"

    def test_record_any_status_string_accepted(self) -> None:
        report = self._make_report()
        report.record(PhaseResult(name="custom", status="pending"))
        report.record(PhaseResult(name="other", status="unknown_state"))
        assert report.phases[0].status == "pending"
        assert report.phases[1].status == "unknown_state"

    def test_record_updates_existing_constructor_phase_in_place(self) -> None:
        report = SetupReport(
            schema_version=1,
            timestamp="2026-01-15T10:00:00+00:00",
            exit_code=0,
            exit_code_name="OK",
            phases=[PhaseResult(name="version_check", status="success", duration_ms=10)],
        )
        report.record(PhaseResult(name="version_check", status="failed", duration_ms=20, error="timeout"))
        assert len(report.phases) == 1
        assert report.phases[0].status == "failed"
        assert report.phases[0].duration_ms == 20
        assert report.phases[0].error == "timeout"
