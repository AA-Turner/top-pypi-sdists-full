"""Tests for create_subtask CLI command."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli import jira
from agentic_devtools.cli.jira import create_commands


class TestCreateSubtaskDryRun:
    """Tests for create_subtask command in dry run mode."""

    def test_create_subtask_dry_run(self, temp_state_dir, clear_state_before, capsys):
        """Test create_subtask in dry run mode."""
        jira.set_jira_value("project_key", "TESTPROJ")
        jira.set_jira_value("parent_key", "PROJECT-1234")
        jira.set_jira_value("summary", "Test Subtask")
        jira.set_jira_value("role", "developer")
        jira.set_jira_value("desired_outcome", "subtask work")
        jira.set_jira_value("benefit", "progress")
        jira.set_jira_value("dry_run", True)

        jira.create_subtask()

        captured = capsys.readouterr()
        assert "[DRY RUN]" in captured.out
        assert "PROJECT-1234" in captured.out
        assert "Test Subtask" in captured.out

    def test_create_subtask_dry_run_shows_resolved_type(self, temp_state_dir, clear_state_before, capsys):
        """Test create_subtask dry run displays the locally-resolved subtask type name."""
        jira.set_jira_value("project_key", "TESTPROJ")
        jira.set_jira_value("parent_key", "PROJECT-1234")
        jira.set_jira_value("summary", "Test Subtask")
        jira.set_jira_value("role", "developer")
        jira.set_jira_value("desired_outcome", "subtask work")
        jira.set_jira_value("benefit", "progress")
        jira.set_jira_value("subtask_type", "Unteraufgabe")
        jira.set_jira_value("dry_run", True)

        jira.create_subtask()

        captured = capsys.readouterr()
        assert "[DRY RUN] Would create Unteraufgabe under PROJECT-1234" in captured.out

    def test_create_subtask_dry_run_does_not_hit_network(self, temp_state_dir, clear_state_before):
        """Test that dry run never triggers Jira network discovery."""
        jira.set_jira_value("project_key", "TESTPROJ")
        jira.set_jira_value("parent_key", "PROJECT-1234")
        jira.set_jira_value("summary", "Test Subtask")
        jira.set_jira_value("role", "developer")
        jira.set_jira_value("desired_outcome", "subtask work")
        jira.set_jira_value("benefit", "progress")
        jira.set_jira_value("dry_run", True)

        with patch.object(create_commands, "_build_jira_config") as mock_build:
            jira.create_subtask()

        mock_build.assert_not_called()

    def test_create_subtask_missing_parent(self, temp_state_dir, clear_state_before):
        """Test create_subtask fails with missing parent_key."""
        jira.set_jira_value("project_key", "TESTPROJ")
        jira.set_jira_value("summary", "Test")
        jira.set_jira_value("role", "dev")
        jira.set_jira_value("desired_outcome", "work")
        jira.set_jira_value("benefit", "progress")

        with pytest.raises(SystemExit) as exc_info:
            jira.create_subtask()
        assert exc_info.value.code == 1

    def test_create_subtask_missing_summary(self, temp_state_dir, clear_state_before):
        """Test create_subtask fails with missing summary."""
        jira.set_jira_value("project_key", "TESTPROJ")
        jira.set_jira_value("parent_key", "PROJECT-1234")
        jira.set_jira_value("role", "dev")
        jira.set_jira_value("desired_outcome", "work")
        jira.set_jira_value("benefit", "progress")

        with pytest.raises(SystemExit) as exc_info:
            jira.create_subtask()
        assert exc_info.value.code == 1

    def test_create_subtask_missing_role(self, temp_state_dir, clear_state_before):
        """Test create_subtask fails with missing role."""
        jira.set_jira_value("project_key", "TESTPROJ")
        jira.set_jira_value("parent_key", "PROJECT-1234")
        jira.set_jira_value("summary", "Test")
        jira.set_jira_value("desired_outcome", "work")
        jira.set_jira_value("benefit", "progress")

        with pytest.raises(SystemExit) as exc_info:
            jira.create_subtask()
        assert exc_info.value.code == 1

    def test_create_subtask_missing_desired_outcome(self, temp_state_dir, clear_state_before):
        """Test create_subtask fails with missing desired_outcome."""
        jira.set_jira_value("project_key", "TESTPROJ")
        jira.set_jira_value("parent_key", "PROJECT-1234")
        jira.set_jira_value("summary", "Test")
        jira.set_jira_value("role", "dev")
        jira.set_jira_value("benefit", "progress")

        with pytest.raises(SystemExit) as exc_info:
            jira.create_subtask()
        assert exc_info.value.code == 1

    def test_create_subtask_missing_benefit(self, temp_state_dir, clear_state_before):
        """Test create_subtask fails with missing benefit."""
        jira.set_jira_value("project_key", "TESTPROJ")
        jira.set_jira_value("parent_key", "PROJECT-1234")
        jira.set_jira_value("summary", "Test")
        jira.set_jira_value("role", "dev")
        jira.set_jira_value("desired_outcome", "work")

        with pytest.raises(SystemExit) as exc_info:
            jira.create_subtask()
        assert exc_info.value.code == 1


class TestCreateSubtaskWithMock:
    """Tests for create_subtask with mocked API calls."""

    def test_create_subtask_uses_discovered_subtask_type(
        self,
        temp_state_dir,
        clear_state_before,
        mock_jira_env,
        capsys,
    ):
        """Test subtask creation uses the Jira-discovered subtask issue type."""
        jira.set_jira_value("project_key", "TESTPROJ")
        jira.set_jira_value("parent_key", "PROJECT-1234")
        jira.set_jira_value("summary", "Test Subtask")
        jira.set_jira_value("role", "developer")
        jira.set_jira_value("desired_outcome", "subtask work")
        jira.set_jira_value("benefit", "progress")

        with (
            patch.object(create_commands, "get_subtask_type_name", return_value="Unteraufgabe"),
            patch.object(
                create_commands,
                "create_issue_sync",
                return_value={"key": "PROJECT-9999"},
            ) as mock_create_issue_sync,
        ):
            jira.create_subtask()

        captured = capsys.readouterr()
        assert "Sub-task created successfully" in captured.out
        assert mock_create_issue_sync.call_args.kwargs["issue_type"] == "Unteraufgabe"
        assert mock_create_issue_sync.call_args.kwargs["parent_key"] == "PROJECT-1234"

    def test_create_subtask_reports_jira_error_details(
        self,
        temp_state_dir,
        clear_state_before,
        mock_jira_env,
        capsys,
    ):
        """Test subtask creation surfaces Jira API error details."""
        jira.set_jira_value("project_key", "TESTPROJ")
        jira.set_jira_value("parent_key", "PROJECT-1234")
        jira.set_jira_value("summary", "Test Subtask")
        jira.set_jira_value("role", "developer")
        jira.set_jira_value("desired_outcome", "subtask work")
        jira.set_jira_value("benefit", "progress")

        exc = RuntimeError("400 Client Error")
        response = MagicMock()
        response.json.return_value = {
            "errorMessages": [],
            "errors": {"issuetype": "The issue type selected is invalid."},
        }
        response.text = "{}"
        exc.response = response

        with (
            patch.object(create_commands, "get_subtask_type_name", return_value="Unteraufgabe"),
            patch.object(
                create_commands,
                "create_issue_sync",
                side_effect=exc,
            ),
        ):
            with pytest.raises(SystemExit) as exc_info:
                jira.create_subtask()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error creating subtask: 400 Client Error" in captured.err
        assert "Messages: []" in captured.err
        assert "Errors: {'issuetype': 'The issue type selected is invalid.'}" in captured.err
        assert "400 Client Error —" in captured.err

    def test_create_subtask_success(
        self,
        temp_state_dir,
        clear_state_before,
        mock_jira_env,
        mock_requests_module,
        capsys,
    ):
        """Test successful subtask creation."""
        jira.set_jira_value("project_key", "TESTPROJ")
        jira.set_jira_value("parent_key", "PROJECT-1234")
        jira.set_jira_value("summary", "Test Subtask")
        jira.set_jira_value("role", "developer")
        jira.set_jira_value("desired_outcome", "subtask work")
        jira.set_jira_value("benefit", "progress")

        jira.create_subtask()

        captured = capsys.readouterr()
        assert "PROJECT-9999" in captured.out
        assert "Sub-task created successfully" in captured.out

    def test_create_subtask_api_error(self, temp_state_dir, clear_state_before, mock_jira_env):
        """Test create_subtask handles API error."""
        jira.set_jira_value("project_key", "TESTPROJ")
        jira.set_jira_value("parent_key", "PROJECT-1234")
        jira.set_jira_value("summary", "Test Subtask")
        jira.set_jira_value("role", "developer")
        jira.set_jira_value("desired_outcome", "subtask work")
        jira.set_jira_value("benefit", "progress")

        mock_module = MagicMock()
        mock_module.post.side_effect = Exception("API Error")
        with patch.object(create_commands, "_get_requests", return_value=mock_module):
            with pytest.raises(SystemExit) as exc_info:
                jira.create_subtask()
            assert exc_info.value.code == 1
