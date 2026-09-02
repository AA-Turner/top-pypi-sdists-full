"""Tests for update_pipeline function."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools import state
from agentic_devtools.cli.azure_devops.pipeline_commands import update_pipeline


class TestUpdatePipelineDryRun:
    """Tests for update_pipeline command in dry-run mode."""

    def test_dry_run_with_new_name(self, temp_state_dir, clear_state_before, capsys):
        """Test dry run output with new_name parameter."""
        state.set_dry_run(True)
        state.set_value("pipeline.id", "123")
        state.set_value("pipeline.new_name", "renamed-pipeline")

        update_pipeline()

        captured = capsys.readouterr()
        assert "DRY-RUN" in captured.out
        assert "renamed-pipeline" in captured.out
        assert "New Name" in captured.out

    def test_dry_run_with_yaml_path(self, temp_state_dir, clear_state_before, capsys):
        """Test dry run output with yaml_path parameter."""
        state.set_dry_run(True)
        state.set_value("pipeline.id", "123")
        state.set_value("pipeline.yaml_path", "/pipelines/new.yml")

        update_pipeline()

        captured = capsys.readouterr()
        assert "DRY-RUN" in captured.out
        assert "/pipelines/new.yml" in captured.out
        assert "YAML" in captured.out

    def test_dry_run_with_new_folder(self, temp_state_dir, clear_state_before, capsys):
        """Test dry run output with new_folder_path parameter."""
        state.set_dry_run(True)
        state.set_value("pipeline.id", "123")
        state.set_value("pipeline.new_folder_path", "/NewFolder")

        update_pipeline()

        captured = capsys.readouterr()
        assert "DRY-RUN" in captured.out
        assert "/NewFolder" in captured.out
        assert "Folder" in captured.out


class TestUpdatePipelineValidation:
    """Tests for update_pipeline validation logic."""

    def test_missing_pipeline_id(self, temp_state_dir, clear_state_before, capsys):
        """Test exits when pipeline.id is missing."""
        state.set_value("pipeline.new_name", "new-name")

        with pytest.raises(SystemExit) as exc_info:
            update_pipeline()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "pipeline.id" in captured.err

    def test_missing_update_parameters(self, temp_state_dir, clear_state_before, capsys):
        """Test exits when no update parameters are provided."""
        state.set_value("pipeline.id", "123")

        with pytest.raises(SystemExit) as exc_info:
            update_pipeline()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "At least one update parameter" in captured.err


class TestUpdatePipelineApiCall:
    """Tests for update_pipeline with mocked API calls."""

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_successful_update_name(self, mock_run, temp_state_dir, clear_state_before, capsys):
        """Test successful pipeline name update."""
        mock_version = MagicMock()
        mock_version.returncode = 0
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"
        mock_update = MagicMock()
        mock_update.returncode = 0
        mock_update.stdout = '{"id": 123, "name": "new-name", "_links": {"web": {"href": "https://dev.azure.com/org/project/_build?definitionId=123"}}}'

        mock_run.side_effect = [mock_version, mock_ext, mock_update]

        state.set_value("pipeline.id", "123")
        state.set_value("pipeline.new_name", "new-name")

        update_pipeline()

        captured = capsys.readouterr()
        assert "Pipeline updated successfully" in captured.out
        assert "new-name" in captured.out
        assert "https://dev.azure.com" in captured.out

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_successful_update_without_url(self, mock_run, temp_state_dir, clear_state_before, capsys):
        """Test successful pipeline update without URL in response."""
        mock_version = MagicMock()
        mock_version.returncode = 0
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"
        mock_update = MagicMock()
        mock_update.returncode = 0
        mock_update.stdout = '{"id": 123, "name": "updated"}'

        mock_run.side_effect = [mock_version, mock_ext, mock_update]

        state.set_value("pipeline.id", "123")
        state.set_value("pipeline.yaml_path", "/new.yml")

        update_pipeline()

        captured = capsys.readouterr()
        assert "Pipeline updated successfully" in captured.out
        assert "URL:" not in captured.out

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_az_cli_failure(self, mock_run, temp_state_dir, clear_state_before, capsys):
        """Test exits on az CLI failure."""
        mock_version = MagicMock()
        mock_version.returncode = 0
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"
        mock_update = MagicMock()
        mock_update.returncode = 1
        mock_update.stderr = "Pipeline not found"

        mock_run.side_effect = [mock_version, mock_ext, mock_update]

        state.set_value("pipeline.id", "999")
        state.set_value("pipeline.new_name", "new-name")

        with pytest.raises(SystemExit) as exc_info:
            update_pipeline()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error updating pipeline" in captured.err

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_json_parse_error(self, mock_run, temp_state_dir, clear_state_before, capsys):
        """Test exits on JSON parse error."""
        mock_version = MagicMock()
        mock_version.returncode = 0
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"
        mock_update = MagicMock()
        mock_update.returncode = 0
        mock_update.stdout = "not-valid-json"

        mock_run.side_effect = [mock_version, mock_ext, mock_update]

        state.set_value("pipeline.id", "123")
        state.set_value("pipeline.new_folder_path", "/NewFolder")

        with pytest.raises(SystemExit) as exc_info:
            update_pipeline()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error parsing response" in captured.err
