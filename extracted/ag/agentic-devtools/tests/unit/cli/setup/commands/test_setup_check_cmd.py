"""Tests for setup_check_cmd."""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.setup import commands
from agentic_devtools.cli.setup.dependency_checker import DependencyStatus
from agentic_devtools.cli.setup.exit_codes import ExitCode


def _statuses(git_found: bool) -> list:
    return [
        DependencyStatus(name="git", found=git_found, required=True, category="Required"),
        DependencyStatus(name="gh", found=True, category="Recommended"),
    ]


@pytest.fixture(autouse=True)
def _fake_ca_bundle(tmp_path: Path):
    """Provide a fake CA bundle so the CA-bundle synthesis in setup_check_cmd finds it."""
    bundle = tmp_path / ".agdt" / "certs" / "unified-ca-bundle.pem"
    bundle.parent.mkdir(parents=True, exist_ok=True)
    bundle.write_text("-----BEGIN CERTIFICATE-----\nfake\n-----END CERTIFICATE-----\n")
    with patch("pathlib.Path.home", return_value=tmp_path):
        yield


class TestSetupCheckCmd:
    """Tests for setup_check_cmd (no-flag backward-compatible path)."""

    def test_exits_zero_when_all_required_found(self, monkeypatch):
        """Completes normally when all required deps are present."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check"])
        with patch.object(commands, "check_all_dependencies", return_value=_statuses(True)):
            commands.setup_check_cmd()  # Should not raise

    def test_exits_with_missing_required_dep_when_dep_missing(self, monkeypatch):
        """Exits with MISSING_REQUIRED_DEP (2) when a required dependency is missing."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check"])
        with patch.object(commands, "check_all_dependencies", return_value=_statuses(False)):
            with pytest.raises(SystemExit) as exc_info:
                commands.setup_check_cmd()
        assert exc_info.value.code == 2

    def test_does_not_install_anything(self, monkeypatch):
        """Does not call install_copilot_cli or install_gh_cli."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check"])
        with patch.object(commands, "check_all_dependencies", return_value=_statuses(True)):
            with patch.object(commands, "install_copilot_cli") as mock_copilot:
                with patch.object(commands, "install_gh_cli") as mock_gh:
                    commands.setup_check_cmd()
        mock_copilot.assert_not_called()
        mock_gh.assert_not_called()

    def test_help_flag_exits_zero(self, monkeypatch):
        """-h displays help and exits 0."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check", "-h"])
        with pytest.raises(SystemExit) as exc_info:
            commands.setup_check_cmd()
        assert exc_info.value.code == 0

    def test_unknown_flag_exits_non_zero(self, monkeypatch):
        """Unknown flags fail fast."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check", "--bogus"])
        with pytest.raises(SystemExit) as exc_info:
            commands.setup_check_cmd()
        assert exc_info.value.code == 2


class TestSetupCheckCmdFixFlag:
    """Tests for setup_check_cmd with --fix flag."""

    def test_fix_healthy_exits_zero(self, monkeypatch):
        """--fix exits 0 when all deps are present (no-op on healthy env)."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check", "--fix"])
        with patch.object(commands, "check_all_dependencies", return_value=_statuses(True)):
            with pytest.raises(SystemExit) as exc_info:
                commands.setup_check_cmd()
        assert exc_info.value.code == 0

    def test_fix_missing_dep_exits_nonzero(self, monkeypatch):
        """--fix exits non-zero when a required dep is missing and no repair registered."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check", "--fix"])
        with patch.object(commands, "check_all_dependencies", return_value=_statuses(False)):
            with pytest.raises(SystemExit) as exc_info:
                commands.setup_check_cmd()
        assert exc_info.value.code == 2

    def test_fix_prints_ok_when_repair_succeeds(self, monkeypatch, capsys):
        """--fix prints OK when exit_code is 0 even if problems list is non-empty."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check", "--fix"])
        statuses = _statuses(False)  # git is missing initially

        # Build a mock DoctorResult that simulates a successful repair:
        # problems is non-empty (original detected list) but exit_code is OK.
        from agentic_devtools.cli.setup.doctor import DoctorResult
        from agentic_devtools.cli.setup.report import make_report

        mock_report = make_report(ExitCode.OK.value, phases=[], details={}, mode="check-fix")
        mock_result = DoctorResult(
            report=mock_report,
            problems=[statuses[0]],  # original problem preserved, repair succeeded
            repair_outcomes=[],
        )

        with patch.object(commands, "check_all_dependencies", return_value=statuses):
            with patch("agentic_devtools.cli.setup.doctor.run_doctor", return_value=mock_result):
                with pytest.raises(SystemExit) as exc_info:
                    commands.setup_check_cmd()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "OK" in captured.out

    def test_fix_does_not_print_ok_when_repair_fails(self, monkeypatch, capsys):
        """--fix does not print OK when exit_code is non-zero after a failed repair."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check", "--fix"])
        statuses = _statuses(False)

        from agentic_devtools.cli.setup.doctor import DoctorResult
        from agentic_devtools.cli.setup.report import make_report

        mock_report = make_report(ExitCode.MISSING_REQUIRED_DEP.value, phases=[], details={}, mode="check-fix")
        mock_result = DoctorResult(
            report=mock_report,
            problems=[statuses[0]],
            repair_outcomes=[],
        )

        with patch.object(commands, "check_all_dependencies", return_value=statuses):
            with patch("agentic_devtools.cli.setup.doctor.run_doctor", return_value=mock_result):
                with pytest.raises(SystemExit):
                    commands.setup_check_cmd()

        captured = capsys.readouterr()
        assert "OK" not in captured.out

    def test_fix_prints_repair_summary_applied(self, monkeypatch, capsys):
        """--fix prints 'fixed' for each repair_outcome with applied=True."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check", "--fix"])
        statuses = _statuses(True)

        from agentic_devtools.cli.setup.doctor import DoctorResult, RepairOutcome
        from agentic_devtools.cli.setup.fixloop import ErrorClass
        from agentic_devtools.cli.setup.report import make_report

        dep = DependencyStatus(name="path-profile", found=True, required=True, category="Required")
        mock_report = make_report(ExitCode.OK.value, phases=[], details={}, mode="check-fix")
        mock_result = DoctorResult(
            report=mock_report,
            problems=[],
            repair_outcomes=[
                RepairOutcome(
                    error_class=ErrorClass.PATH_PROFILE_NOT_UPDATED,
                    dependency=dep,
                    success=True,
                    applied=True,
                )
            ],
        )

        with patch.object(commands, "check_all_dependencies", return_value=statuses):
            with patch("agentic_devtools.cli.setup.doctor.run_doctor", return_value=mock_result):
                with pytest.raises(SystemExit):
                    commands.setup_check_cmd()

        captured = capsys.readouterr()
        assert "path-profile: fixed" in captured.out

    def test_fix_prints_repair_summary_noop(self, monkeypatch, capsys):
        """--fix prints 'ok (no-op)' for each repair_outcome with applied=False and success=True."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check", "--fix"])
        statuses = _statuses(True)

        from agentic_devtools.cli.setup.doctor import DoctorResult, RepairOutcome
        from agentic_devtools.cli.setup.fixloop import ErrorClass
        from agentic_devtools.cli.setup.report import make_report

        dep = DependencyStatus(name="git-hooks", found=True, required=False, category="Optional")
        mock_report = make_report(ExitCode.OK.value, phases=[], details={}, mode="check-fix")
        mock_result = DoctorResult(
            report=mock_report,
            problems=[],
            repair_outcomes=[
                RepairOutcome(
                    error_class=ErrorClass.GIT_HOOKS_NOT_CONFIGURED,
                    dependency=dep,
                    success=True,
                    applied=False,
                )
            ],
        )

        with patch.object(commands, "check_all_dependencies", return_value=statuses):
            with patch("agentic_devtools.cli.setup.doctor.run_doctor", return_value=mock_result):
                with pytest.raises(SystemExit):
                    commands.setup_check_cmd()

        captured = capsys.readouterr()
        assert "git-hooks: ok (no-op)" in captured.out

    def test_fix_prints_repair_summary_failed_with_message(self, monkeypatch, capsys):
        """--fix prints 'failed (message)' when success=False and error_message is set."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check", "--fix"])
        statuses = _statuses(True)

        from agentic_devtools.cli.setup.doctor import DoctorResult, RepairOutcome
        from agentic_devtools.cli.setup.fixloop import ErrorClass
        from agentic_devtools.cli.setup.report import make_report

        dep = DependencyStatus(name="path-profile", found=False, required=True, category="Required")
        mock_report = make_report(ExitCode.MISSING_REQUIRED_DEP.value, phases=[], details={}, mode="check-fix")
        mock_result = DoctorResult(
            report=mock_report,
            problems=[dep],
            repair_outcomes=[
                RepairOutcome(
                    error_class=ErrorClass.PATH_PROFILE_NOT_UPDATED,
                    dependency=dep,
                    success=False,
                    error_message="permission denied",
                    applied=False,
                )
            ],
        )

        with patch.object(commands, "check_all_dependencies", return_value=statuses):
            with patch("agentic_devtools.cli.setup.doctor.run_doctor", return_value=mock_result):
                with pytest.raises(SystemExit):
                    commands.setup_check_cmd()

        captured = capsys.readouterr()
        assert "path-profile: failed (permission denied)" in captured.out

    def test_fix_prints_repair_summary_failed_without_message(self, monkeypatch, capsys):
        """--fix prints 'failed' when success=False and no error_message."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check", "--fix"])
        statuses = _statuses(True)

        from agentic_devtools.cli.setup.doctor import DoctorResult, RepairOutcome
        from agentic_devtools.cli.setup.fixloop import ErrorClass
        from agentic_devtools.cli.setup.report import make_report

        dep = DependencyStatus(name="git-hooks", found=False, required=False, category="Optional")
        mock_report = make_report(ExitCode.OK.value, phases=[], details={}, mode="check-fix")
        mock_result = DoctorResult(
            report=mock_report,
            problems=[],
            repair_outcomes=[
                RepairOutcome(
                    error_class=ErrorClass.GIT_HOOKS_NOT_CONFIGURED,
                    dependency=dep,
                    success=False,
                    error_message=None,
                    applied=False,
                )
            ],
        )

        with patch.object(commands, "check_all_dependencies", return_value=statuses):
            with patch("agentic_devtools.cli.setup.doctor.run_doctor", return_value=mock_result):
                with pytest.raises(SystemExit):
                    commands.setup_check_cmd()

        captured = capsys.readouterr()
        assert "git-hooks: failed" in captured.out
        assert "git-hooks: failed (" not in captured.out

    def test_fix_report_mode_is_check_fix(self, monkeypatch, capsys):
        """Report emitted in check-fix mode when --fix is passed."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check", "--fix", "--json"])
        with patch.object(commands, "check_all_dependencies", return_value=_statuses(True)):
            with pytest.raises(SystemExit):
                commands.setup_check_cmd()
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["mode"] == "check-fix"


class TestSetupCheckCmdJsonFlag:
    """Tests for setup_check_cmd with --json flag."""

    def test_json_healthy_stdout_is_valid_json(self, monkeypatch, capsys):
        """--json emits valid JSON to stdout when all deps are healthy."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check", "--json"])
        with patch.object(commands, "check_all_dependencies", return_value=_statuses(True)):
            with pytest.raises(SystemExit):
                commands.setup_check_cmd()
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["exit_code"] == 0

    def test_json_mode_is_check_without_fix(self, monkeypatch, capsys):
        """--json alone produces mode='check' (not 'check-fix')."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check", "--json"])
        with patch.object(commands, "check_all_dependencies", return_value=_statuses(True)):
            with pytest.raises(SystemExit):
                commands.setup_check_cmd()
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["mode"] == "check"

    def test_json_missing_dep_exit_code_in_output(self, monkeypatch, capsys):
        """--json encodes exit_code=2 in JSON when a required dep is missing."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check", "--json"])
        with patch.object(commands, "check_all_dependencies", return_value=_statuses(False)):
            with pytest.raises(SystemExit):
                commands.setup_check_cmd()
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["exit_code"] == 2
        assert data["exit_code_name"] == "MISSING_REQUIRED_DEP"

    def test_json_schema_version_is_1(self, monkeypatch, capsys):
        """--json output always carries schema_version=1."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check", "--json"])
        with patch.object(commands, "check_all_dependencies", return_value=_statuses(True)):
            with pytest.raises(SystemExit):
                commands.setup_check_cmd()
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["schema_version"] == 1

    def test_json_and_fix_combined_mode_is_check_fix(self, monkeypatch, capsys):
        """--json --fix produces mode='check-fix' in the JSON output."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check", "--fix", "--json"])
        with patch.object(commands, "check_all_dependencies", return_value=_statuses(True)):
            with pytest.raises(SystemExit):
                commands.setup_check_cmd()
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["mode"] == "check-fix"

    def test_json_fix_combined_includes_repair_phases(self, monkeypatch, capsys):
        """--fix --json with missing dep includes repair phase results in JSON output."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check", "--fix", "--json"])
        with patch.object(commands, "check_all_dependencies", return_value=_statuses(False)):
            with pytest.raises(SystemExit):
                commands.setup_check_cmd()
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["mode"] == "check-fix"
        # Should have phases array with at least check + repair phases
        assert "phases" in data
        phase_names = [p["name"] for p in data["phases"]]
        assert "check" in phase_names
        assert any(name.startswith("repair:") for name in phase_names)


class TestSetupCheckCmdBackwardCompat:
    """Backward-compatible path: no --fix, no --json."""

    def test_no_flags_healthy_exits_zero(self, monkeypatch):
        """No flags, all deps present — exits 0 (backward compatible)."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check"])
        with patch.object(commands, "check_all_dependencies", return_value=_statuses(True)):
            commands.setup_check_cmd()  # Should not raise

    def test_no_flags_missing_dep_exits_2(self, monkeypatch):
        """No flags, required dep missing — exits 2 (MISSING_REQUIRED_DEP)."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check"])
        with patch.object(commands, "check_all_dependencies", return_value=_statuses(False)):
            with pytest.raises(SystemExit) as exc_info:
                commands.setup_check_cmd()
        assert exc_info.value.code == 2


class TestSetupCheckCmdCorruptionWarning:
    """Tests for plain-mode corruption warning in setup_check_cmd."""

    def test_plain_mode_prints_warning_to_stderr(self, monkeypatch, capsys):
        """Plain mode prints corruption warning to stderr when artifacts detected."""
        from pathlib import Path

        monkeypatch.setattr(sys, "argv", ["agdt-setup-check"])
        fake_artifacts = [
            Path("/sp1/~gentic-devtools"),
            Path("/sp1/bad.dist-info"),
            Path("/sp2/~gentic_devtools"),
        ]
        with patch.object(commands, "check_all_dependencies", return_value=_statuses(True)):
            with patch(
                "agentic_devtools.cli.setup.script_generators.required_setup.detect_corrupted_artifacts",
                return_value=fake_artifacts,
            ):
                commands.setup_check_cmd()
        captured = capsys.readouterr()
        assert "Corrupted install artifacts detected" in captured.err
        assert "/sp1/" in captured.err
        assert "/sp2/" in captured.err
        assert "~gentic-devtools" in captured.err
        assert "bad.dist-info" in captured.err

    def test_plain_mode_no_warning_when_healthy(self, monkeypatch, capsys):
        """Plain mode does not print warning when no corruption detected."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check"])
        with patch.object(commands, "check_all_dependencies", return_value=_statuses(True)):
            with patch(
                "agentic_devtools.cli.setup.script_generators.required_setup.detect_corrupted_artifacts",
                return_value=[],
            ):
                commands.setup_check_cmd()
        captured = capsys.readouterr()
        assert "Corrupted install artifacts detected" not in captured.err

    def test_plain_mode_does_not_dispatch_repair(self, monkeypatch):
        """Plain mode does not dispatch repair even with corruption detected."""
        from pathlib import Path

        monkeypatch.setattr(sys, "argv", ["agdt-setup-check"])
        fake_artifacts = [Path("/sp/~gentic-devtools")]
        with patch.object(commands, "check_all_dependencies", return_value=_statuses(True)):
            with patch(
                "agentic_devtools.cli.setup.script_generators.required_setup.detect_corrupted_artifacts",
                return_value=fake_artifacts,
            ):
                with patch("agentic_devtools.cli.setup.doctor_repair.confirm_destructive_repair") as mock_confirm:
                    commands.setup_check_cmd()
        mock_confirm.assert_not_called()

    def test_detect_called_exactly_once(self, monkeypatch):
        """detect_corrupted_artifacts is called exactly once per invocation."""
        from pathlib import Path
        from unittest.mock import MagicMock

        monkeypatch.setattr(sys, "argv", ["agdt-setup-check"])
        mock_detect = MagicMock(return_value=[Path("/sp/~gentic-devtools")])
        with patch.object(commands, "check_all_dependencies", return_value=_statuses(True)):
            with patch(
                "agentic_devtools.cli.setup.script_generators.required_setup.detect_corrupted_artifacts",
                mock_detect,
            ):
                commands.setup_check_cmd()
        mock_detect.assert_called_once()
