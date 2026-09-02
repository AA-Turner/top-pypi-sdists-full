"""Tests for route_create_epic (agdt-create-epic routing layer, issue #2117)."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli import jira
from agentic_devtools.cli.jira import create_epic_router


def _run(argv):
    """Invoke route_create_epic with background spawn and tracking mocked.

    Returns a tuple of (raised SystemExit code or None, spawn mock).
    """
    with (
        patch.object(create_epic_router, "run_function_in_background") as spawn,
        patch.object(create_epic_router, "print_task_tracking_info"),
    ):
        code = None
        try:
            create_epic_router.route_create_epic(argv)
        except SystemExit as exc:
            code = exc.code
        return code, spawn


def _last_validation_record(captured_err):
    """Return the parsed NDJSON validation record from the last stderr line."""
    lines = [line for line in captured_err.strip().splitlines() if line.strip()]
    return json.loads(lines[-1])


class TestTreeModeRouting:
    """User Story 1 - file input enters tree mode (FR-001, FR-003, FR-009)."""

    def test_file_enters_tree_mode(self, temp_state_dir, clear_state_before):
        code, spawn = _run(["plan.json"])
        assert code is None
        module, function = spawn.call_args[0]
        assert module == "agentic_devtools.cli.jira.create_epic_router"
        assert function == "run_tree_mode"
        kwargs = spawn.call_args.kwargs["func_kwargs"]
        assert kwargs["file_path"] == "plan.json"
        assert kwargs["basis"] == create_epic_router.BASIS_FILE_PRESENT

    def test_file_forwards_flags(self, temp_state_dir, clear_state_before):
        _, spawn = _run(["plan.json", "--dry-run", "--start-from", "feat-1", "--provider", " GitHub "])
        kwargs = spawn.call_args.kwargs["func_kwargs"]
        assert kwargs["start_from"] == "feat-1"
        assert kwargs["provider"] == "github"
        assert kwargs["dry_run"] is True

    def test_unsupported_provider_deferred_in_tree_mode(self, temp_state_dir, clear_state_before):
        # Tree mode must not reject provider values (e.g. markdown); it defers to #2118.
        code, spawn = _run(["plan.json", "--provider", "markdown"])
        assert code is None
        assert spawn.call_args.kwargs["func_kwargs"]["provider"] == "markdown"

    def test_start_from_forwarded_unchanged(self, temp_state_dir, clear_state_before):
        _, spawn = _run(["plan.json", "--start-from", "  Feature/Node ="])
        assert spawn.call_args.kwargs["func_kwargs"]["start_from"] == "  Feature/Node ="

    def test_file_overrides_legacy_state(self, temp_state_dir, clear_state_before):
        jira.set_jira_value("project_key", "PROJECT")
        code, spawn = _run(["plan.json"])
        assert code is None
        assert spawn.call_args.kwargs["func_kwargs"]["basis"] == create_epic_router.BASIS_FILE_OVERRIDES_LEGACY

    def test_router_does_not_open_file(self, temp_state_dir, clear_state_before):
        with patch("builtins.open", side_effect=AssertionError("router must not open the file")):
            code, _ = _run(["does-not-exist.json"])
        assert code is None


class TestLegacyModeRouting:
    """User Story 2 - preserve legacy single-epic behavior (FR-004)."""

    def test_legacy_happy_path_dispatches(self, temp_state_dir, clear_state_before):
        jira.set_jira_value("project_key", "PROJECT")
        jira.set_jira_value("summary", "Epic")
        jira.set_jira_value("epic_name", "Name")
        code, spawn = _run([])
        assert code is None
        module, function = spawn.call_args[0]
        assert function == "run_legacy_mode"
        assert spawn.call_args.kwargs["func_kwargs"] == {"dry_run_override": False}

    def test_dry_run_flag_forwarded_to_legacy(self, temp_state_dir, clear_state_before):
        jira.set_jira_value("project_key", "PROJECT")
        jira.set_jira_value("summary", "Epic")
        jira.set_jira_value("epic_name", "Name")
        _, spawn = _run(["--dry-run"])
        assert spawn.call_args.kwargs["func_kwargs"] == {"dry_run_override": True}

    def test_provider_jira_compatible_with_legacy(self, temp_state_dir, clear_state_before):
        jira.set_jira_value("project_key", "PROJECT")
        jira.set_jira_value("summary", "Epic")
        jira.set_jira_value("epic_name", "Name")
        code, spawn = _run(["--provider", "jira"])
        assert code is None
        assert spawn.call_args[0][1] == "run_legacy_mode"

    def test_empty_string_legacy_key_selects_legacy(self, temp_state_dir, clear_state_before):
        # Presence of a legacy key selects legacy mode even when the value is empty.
        jira.set_jira_value("labels", "")
        code, spawn = _run([])
        # project_key missing -> preserved pre-spawn failure (exit 1), no spawn.
        assert code == 1
        spawn.assert_not_called()

    def test_preserved_pre_spawn_failure_when_required_missing(self, temp_state_dir, clear_state_before):
        # A legacy key is present but required project_key is absent.
        jira.set_jira_value("role", "developer")
        code, spawn = _run([])
        assert code == 1
        spawn.assert_not_called()


class TestNoFileValidationPrecedence:
    """User Story 3 - deterministic no-file rejection precedence (FR-005, FR-012)."""

    def test_missing_input(self, temp_state_dir, clear_state_before, capsys):
        code, spawn = _run([])
        assert code == 2
        spawn.assert_not_called()
        err = capsys.readouterr().err
        assert "JSON" in err and "legacy" in err
        record = _last_validation_record(err)
        assert record["event"] == create_epic_router.VALIDATION_EVENT
        assert record["reason"] == create_epic_router.REASON_MISSING_INPUT
        assert "provider" not in record

    def test_start_from_requires_file(self, temp_state_dir, clear_state_before, capsys):
        code, _ = _run(["--start-from", "feat-1"])
        assert code == 2
        record = _last_validation_record(capsys.readouterr().err)
        assert record["reason"] == create_epic_router.REASON_START_FROM_REQUIRES_FILE
        assert record["start_from"] == "feat-1"

    def test_provider_requires_file(self, temp_state_dir, clear_state_before, capsys):
        code, _ = _run(["--provider", "github"])
        assert code == 2
        record = _last_validation_record(capsys.readouterr().err)
        assert record["reason"] == create_epic_router.REASON_PROVIDER_REQUIRES_FILE
        assert record["provider"] == "github"

    def test_start_from_precedence_over_provider(self, temp_state_dir, clear_state_before, capsys):
        code, _ = _run(["--start-from", "feat-1", "--provider", "github"])
        assert code == 2
        record = _last_validation_record(capsys.readouterr().err)
        assert record["reason"] == create_epic_router.REASON_START_FROM_REQUIRES_FILE
        assert record["provider"] == "github"
        assert record["start_from"] == "feat-1"

    def test_unsupported_provider_precedence(self, temp_state_dir, clear_state_before, capsys):
        # Unsupported provider wins even when start-from and missing-input also apply.
        code, _ = _run(["--start-from", "feat-1", "--provider", "markdown"])
        assert code == 2
        err = capsys.readouterr().err
        record = _last_validation_record(err)
        assert record["reason"] == create_epic_router.REASON_UNSUPPORTED_PROVIDER
        assert record["provider"] == "markdown"
        assert "github, jira" in err

    def test_provider_jira_no_file_no_state_is_missing_input(self, temp_state_dir, clear_state_before, capsys):
        code, _ = _run(["--provider", "jira"])
        assert code == 2
        record = _last_validation_record(capsys.readouterr().err)
        assert record["reason"] == create_epic_router.REASON_MISSING_INPUT
        assert record["provider"] == "jira"

    def test_validation_record_is_single_line_ndjson(self, temp_state_dir, clear_state_before, capsys):
        _run(["--start-from", 'line1\nline2="q"'])
        err = capsys.readouterr().err
        record_line = err.strip().splitlines()[-1]
        assert record_line.count("\n") == 0
        parsed = json.loads(record_line)
        assert parsed["start_from"] == 'line1\nline2="q"'
        assert err.endswith("\n")


class TestHelpBehavior:
    """FR-008 - --help short-circuits routing and validation."""

    @pytest.mark.parametrize(
        "argv",
        [["--help"], ["--help", "--provider", "bogus"], ["--help", "--start-from", "x"]],
    )
    def test_help_exits_zero_without_records(self, temp_state_dir, clear_state_before, capsys, argv):
        code, spawn = _run(argv)
        assert code == 0
        spawn.assert_not_called()
        captured = capsys.readouterr()
        assert "usage" in captured.out.lower()
        assert "validation_error" not in captured.err

    def test_help_short_circuits_legacy_state(self, temp_state_dir, clear_state_before, capsys):
        jira.set_jira_value("project_key", "PROJECT")
        code, spawn = _run(["--help"])
        assert code == 0
        spawn.assert_not_called()
        captured = capsys.readouterr()
        assert "usage" in captured.out.lower()
        assert create_epic_router.ROUTING_EVENT not in captured.out
