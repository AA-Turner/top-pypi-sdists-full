"""Tests for SetupReport.to_dict() method."""

from agentic_devtools.cli.setup.report import PhaseResult, SetupReport


class TestToDict:
    """SetupReport.to_dict() serialization with summary counts."""

    def _make_report(self, **kwargs: object) -> SetupReport:
        defaults: dict[str, object] = {
            "schema_version": 1,
            "timestamp": "2026-01-15T10:00:00+00:00",
            "exit_code": 0,
            "exit_code_name": "OK",
            "phases": [],
            "details": {},
            "mode": "setup",
            "git_root": None,
        }
        defaults.update(kwargs)
        return SetupReport(**defaults)  # type: ignore[arg-type]

    def test_to_dict_schema_version_is_integer_one(self) -> None:
        report = self._make_report()
        d = report.to_dict()
        assert d["schema_version"] == 1
        assert isinstance(d["schema_version"], int)

    def test_to_dict_includes_summary_counts(self) -> None:
        phases = [
            PhaseResult(name="a", status="success"),
            PhaseResult(name="b", status="failed", error="err"),
            PhaseResult(name="c", status="skipped"),
            PhaseResult(name="d", status="success"),
        ]
        report = self._make_report(phases=phases)
        d = report.to_dict()
        assert d["total_phases"] == 4
        assert d["passed"] == 2
        assert d["failed"] == 1
        assert d["skipped"] == 1

    def test_to_dict_unrecognized_status_only_in_total(self) -> None:
        phases = [
            PhaseResult(name="a", status="success"),
            PhaseResult(name="b", status="pending"),
            PhaseResult(name="c", status="unknown"),
        ]
        report = self._make_report(phases=phases)
        d = report.to_dict()
        assert d["total_phases"] == 3
        assert d["passed"] == 1
        assert d["failed"] == 0
        assert d["skipped"] == 0

    def test_to_dict_mode_and_git_root_serialized(self) -> None:
        report = self._make_report(mode="check", git_root="/home/user/repo")
        d = report.to_dict()
        assert d["mode"] == "check"
        assert d["git_root"] == "/home/user/repo"

    def test_to_dict_git_root_null_when_none(self) -> None:
        report = self._make_report(git_root=None)
        d = report.to_dict()
        assert d["git_root"] is None

    def test_to_dict_preserves_existing_keys(self) -> None:
        phases = [PhaseResult(name="x", status="success", duration_ms=42, error=None)]
        report = self._make_report(
            phases=phases,
            details={"key": "value"},
            exit_code=3,
            exit_code_name="VERSION_BLOCKED",
        )
        d = report.to_dict()
        assert d["timestamp"] == "2026-01-15T10:00:00+00:00"
        assert d["exit_code"] == 3
        assert d["exit_code_name"] == "VERSION_BLOCKED"
        assert d["details"] == {"key": "value"}
        assert d["phases"][0]["name"] == "x"
        assert d["phases"][0]["status"] == "success"
        assert d["phases"][0]["duration_ms"] == 42
        assert d["phases"][0]["error"] is None
