"""Tests for mark_pull_request_draft function."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools import state
from agentic_devtools.cli import azure_devops


class TestMarkPullRequestDraft:
    """Tests for mark_pull_request_draft command."""

    def test_dry_run(self, temp_state_dir, clear_state_before, capsys):
        """Test dry run output."""
        state.set_pull_request_id(12345)
        state.set_dry_run(True)

        azure_devops.mark_pull_request_draft()

        captured = capsys.readouterr()
        assert "[DRY RUN]" in captured.out
        assert "12345" in captured.out
        assert "draft" in captured.out.lower()

    def test_dry_run_shows_org_project(self, temp_state_dir, clear_state_before, capsys):
        """Test dry run shows organization and project."""
        state.set_pull_request_id(12345)
        state.set_dry_run(True)

        azure_devops.mark_pull_request_draft()

        captured = capsys.readouterr()
        assert "Org/Project:" in captured.out

    def test_missing_pull_request_id(self, temp_state_dir, clear_state_before):
        """Test raises error when pull request ID is missing."""
        state.set_dry_run(True)
        with pytest.raises(KeyError, match="pull_request_id"):
            azure_devops.mark_pull_request_draft()

    def test_rejects_invalid_explicit_pull_request_id(self, temp_state_dir, clear_state_before):
        """Test explicit pull request IDs must be positive integers."""
        with pytest.raises(ValueError, match="pull_request_id"):
            azure_devops.mark_pull_request_draft(pull_request_id=0)

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_mark_draft_merges_partial_organization_override(self, mock_run, temp_state_dir, clear_state_before):
        """Test an organization-only override still uses state-derived project."""
        mock_version = MagicMock()
        mock_version.returncode = 0
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"
        mock_update = MagicMock()
        mock_update.returncode = 0
        mock_update.stdout = '{"pullRequestId": 12345, "repository": {}}'

        mock_run.side_effect = [mock_version, mock_ext, mock_update]

        state.set_value("project", "state-project")

        azure_devops.mark_pull_request_draft(
            pull_request_id=12345,
            organization="https://dev.azure.com/captured-org",
        )

        update_call = mock_run.call_args_list[2]
        cmd = update_call[0][0]
        assert cmd[cmd.index("--organization") + 1] == "https://dev.azure.com/captured-org"
        assert cmd[cmd.index("--project") + 1] == "state-project"

    def test_rejects_non_boolean_dry_run_override(self, temp_state_dir, clear_state_before):
        """Test an explicit non-boolean dry_run override is rejected instead of silently accepted."""
        state.set_pull_request_id(12345)
        with pytest.raises(ValueError, match="dry_run must be a boolean"):
            azure_devops.mark_pull_request_draft(dry_run="false")  # type: ignore[arg-type]

    def test_rejects_blank_organization_override(self, temp_state_dir, clear_state_before):
        """Test a blank organization override is rejected instead of silently accepted."""
        state.set_pull_request_id(12345)
        with pytest.raises(ValueError, match="organization must be a non-empty string"):
            azure_devops.mark_pull_request_draft(organization="   ")

    def test_rejects_non_string_organization_override(self, temp_state_dir, clear_state_before):
        """Test a non-string organization override is rejected instead of silently accepted."""
        state.set_pull_request_id(12345)
        with pytest.raises(ValueError, match="organization must be a non-empty string"):
            azure_devops.mark_pull_request_draft(organization=123)  # type: ignore[arg-type]

    def test_rejects_blank_project_override(self, temp_state_dir, clear_state_before):
        """Test a blank project override is rejected instead of silently accepted."""
        state.set_pull_request_id(12345)
        with pytest.raises(ValueError, match="project must be a non-empty string"):
            azure_devops.mark_pull_request_draft(project="   ")

    def test_rejects_non_string_project_override(self, temp_state_dir, clear_state_before):
        """Test a non-string project override is rejected instead of silently accepted."""
        state.set_pull_request_id(12345)
        with pytest.raises(ValueError, match="project must be a non-empty string"):
            azure_devops.mark_pull_request_draft(project=123)  # type: ignore[arg-type]

    def test_dry_run_override_ignores_mutated_state(self, temp_state_dir, clear_state_before, capsys):
        """Test the explicit dry_run override wins even if state changes afterward."""
        state.set_pull_request_id(12345)
        state.set_dry_run(False)

        azure_devops.mark_pull_request_draft(dry_run=True)

        captured = capsys.readouterr()
        assert "[DRY RUN]" in captured.out

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_dry_run_override_false_still_executes_when_state_is_dry_run(
        self, mock_run, temp_state_dir, clear_state_before
    ):
        """Test an explicit dry_run=False override performs the real mutation."""
        mock_version = MagicMock()
        mock_version.returncode = 0
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"
        mock_update = MagicMock()
        mock_update.returncode = 0
        mock_update.stdout = '{"pullRequestId": 12345, "repository": {}}'

        mock_run.side_effect = [mock_version, mock_ext, mock_update]

        state.set_pull_request_id(12345)
        state.set_dry_run(True)

        azure_devops.mark_pull_request_draft(dry_run=False)

        assert mock_run.call_count == 3


class TestMarkPullRequestDraftActualCall:
    """Tests for mark_pull_request_draft with mocked API calls."""

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_successful_mark_draft(self, mock_run, temp_state_dir, clear_state_before, capsys):
        """Test successful mark as draft."""
        # Mock az --version check
        mock_version = MagicMock()
        mock_version.returncode = 0

        # Mock extension check
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"

        # Mock pr update
        mock_update = MagicMock()
        mock_update.returncode = 0
        mock_update.stdout = '{"pullRequestId": 12345, "isDraft": true, "repository": {"webUrl": "https://test"}}'

        mock_run.side_effect = [mock_version, mock_ext, mock_update]

        state.set_pull_request_id(12345)

        azure_devops.mark_pull_request_draft()

        captured = capsys.readouterr()
        assert "12345" in captured.out
        assert "draft" in captured.out.lower()

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_mark_draft_includes_draft_flag(self, mock_run, temp_state_dir, clear_state_before):
        """Test that mark_pull_request_draft passes --draft true to az CLI."""
        mock_version = MagicMock()
        mock_version.returncode = 0
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"
        mock_update = MagicMock()
        mock_update.returncode = 0
        mock_update.stdout = '{"pullRequestId": 12345, "repository": {}}'

        mock_run.side_effect = [mock_version, mock_ext, mock_update]

        state.set_pull_request_id(12345)

        azure_devops.mark_pull_request_draft()

        # Check that --draft true was in the command
        update_call = mock_run.call_args_list[2]
        cmd = update_call[0][0]
        assert "--draft" in cmd
        draft_idx = cmd.index("--draft")
        assert cmd[draft_idx + 1] == "true"

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_mark_draft_failure(self, mock_run, temp_state_dir, clear_state_before, capsys):
        """Test mark draft fails when az command fails."""
        mock_version = MagicMock()
        mock_version.returncode = 0
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"
        mock_update = MagicMock()
        mock_update.returncode = 1
        mock_update.stderr = "Failed to update PR"

        mock_run.side_effect = [mock_version, mock_ext, mock_update]

        state.set_pull_request_id(12345)

        with pytest.raises(SystemExit) as exc_info:
            azure_devops.mark_pull_request_draft()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error marking PR as draft" in captured.err

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_mark_draft_uses_explicit_pull_request_id(self, mock_run, temp_state_dir, clear_state_before):
        """Test explicit pull request IDs bypass state lookup."""
        mock_version = MagicMock()
        mock_version.returncode = 0
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"
        mock_update = MagicMock()
        mock_update.returncode = 0
        mock_update.stdout = '{"pullRequestId": 77, "repository": {}}'

        mock_run.side_effect = [mock_version, mock_ext, mock_update]

        azure_devops.mark_pull_request_draft(pull_request_id=77)

        update_call = mock_run.call_args_list[2]
        cmd = update_call[0][0]
        assert cmd[cmd.index("--id") + 1] == "77"

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_mark_draft_raises_runtime_error_when_exit_on_error_disabled(
        self, mock_run, temp_state_dir, clear_state_before
    ):
        """Test non-CLI callers receive a normal exception on failure."""
        mock_version = MagicMock()
        mock_version.returncode = 0
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"
        mock_update = MagicMock()
        mock_update.returncode = 1
        mock_update.stderr = "Failed to update PR"

        mock_run.side_effect = [mock_version, mock_ext, mock_update]

        with pytest.raises(RuntimeError, match="Failed to update PR"):
            azure_devops.mark_pull_request_draft(pull_request_id=12345, exit_on_error=False)

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_mark_draft_uses_captured_organization_and_project(self, mock_run, temp_state_dir, clear_state_before):
        """Test explicit organization/project override state-derived config."""
        mock_version = MagicMock()
        mock_version.returncode = 0
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"
        mock_update = MagicMock()
        mock_update.returncode = 0
        mock_update.stdout = '{"pullRequestId": 12345, "repository": {}}'

        mock_run.side_effect = [mock_version, mock_ext, mock_update]

        azure_devops.mark_pull_request_draft(
            pull_request_id=12345,
            organization="https://dev.azure.com/captured-org",
            project="captured-project",
        )

        update_call = mock_run.call_args_list[2]
        cmd = update_call[0][0]
        assert cmd[cmd.index("--organization") + 1] == "https://dev.azure.com/captured-org"
        assert cmd[cmd.index("--project") + 1] == "captured-project"

    @patch("agentic_devtools.cli.azure_devops.commands.verify_az_cli")
    def test_mark_draft_converts_verify_az_cli_system_exit_when_disabled(
        self, mock_verify, temp_state_dir, clear_state_before
    ):
        """Test verify_az_cli's SystemExit becomes a RuntimeError for non-CLI callers."""
        mock_verify.side_effect = SystemExit(1)

        with pytest.raises(RuntimeError, match="Azure CLI"):
            azure_devops.mark_pull_request_draft(pull_request_id=12345, exit_on_error=False)

    @patch("agentic_devtools.cli.azure_devops.commands.verify_az_cli")
    def test_mark_draft_propagates_verify_az_cli_system_exit_when_enabled(
        self, mock_verify, temp_state_dir, clear_state_before
    ):
        """Test verify_az_cli's SystemExit still terminates CLI callers."""
        mock_verify.side_effect = SystemExit(1)

        with pytest.raises(SystemExit):
            azure_devops.mark_pull_request_draft(pull_request_id=12345)

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_mark_draft_converts_parse_json_response_system_exit_when_disabled(
        self, mock_run, temp_state_dir, clear_state_before
    ):
        """Test malformed successful output becomes a RuntimeError for non-CLI callers."""
        mock_version = MagicMock()
        mock_version.returncode = 0
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"
        mock_update = MagicMock()
        mock_update.returncode = 0
        mock_update.stdout = "not-json"

        mock_run.side_effect = [mock_version, mock_ext, mock_update]

        with pytest.raises(RuntimeError, match="Failed to parse PR response"):
            azure_devops.mark_pull_request_draft(pull_request_id=12345, exit_on_error=False)

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_mark_draft_propagates_parse_json_response_system_exit_when_enabled(
        self, mock_run, temp_state_dir, clear_state_before
    ):
        """Test malformed successful output still exits CLI callers."""
        mock_version = MagicMock()
        mock_version.returncode = 0
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"
        mock_update = MagicMock()
        mock_update.returncode = 0
        mock_update.stdout = "not-json"

        mock_run.side_effect = [mock_version, mock_ext, mock_update]

        with pytest.raises(SystemExit):
            azure_devops.mark_pull_request_draft(pull_request_id=12345)
