"""Tests for get_repository_id helper."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli import azure_devops


class TestGetRepositoryId:
    """Tests for get_repository_id function."""

    def test_uses_rest_as_first_lookup_option(self, mock_azure_devops_env):
        """Test repository ID is resolved from REST before Azure CLI is attempted."""
        with patch(
            "agentic_devtools.cli.azure_devops.helpers._get_repository_id_via_rest", return_value="repo-guid-123"
        ):
            with patch("agentic_devtools.cli.azure_devops.helpers.run_safe") as mock_run_safe:
                repo_id = azure_devops.get_repository_id()

        assert repo_id == "repo-guid-123"
        mock_run_safe.assert_not_called()

    def test_falls_back_to_az_when_rest_lookup_fails(self):
        """Test Azure CLI is used when REST lookup fails."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "repo-guid-123\n"

        with patch(
            "agentic_devtools.cli.azure_devops.helpers._get_repository_id_via_rest",
            side_effect=RuntimeError("REST failed"),
        ):
            with patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="test-pat"):
                with patch("agentic_devtools.cli.azure_devops.helpers.run_safe", return_value=mock_result):
                    repo_id = azure_devops.get_repository_id()

        assert repo_id == "repo-guid-123"

    def test_raises_when_rest_and_az_fail(self):
        """Test error contains both REST and Azure CLI failures."""
        cli_result = MagicMock()
        cli_result.returncode = 1
        cli_result.stderr = "VS800075"

        with patch(
            "agentic_devtools.cli.azure_devops.helpers._get_repository_id_via_rest",
            side_effect=RuntimeError("Forbidden"),
        ):
            with patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="test-pat"):
                with patch("agentic_devtools.cli.azure_devops.helpers.run_safe", return_value=cli_result):
                    with pytest.raises(RuntimeError, match="REST lookup failed") as exc_info:
                        azure_devops.get_repository_id(
                            organization="https://dev.azure.com/swica",
                            project="DragonflyMgmt",
                            repository="dfly-platform-management",
                        )

        assert "Azure CLI fallback failed" in str(exc_info.value)

    def test_raises_when_rest_fails_and_az_returns_empty_result(self):
        """Test empty Azure CLI fallback result is surfaced after REST failure."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""

        with patch(
            "agentic_devtools.cli.azure_devops.helpers._get_repository_id_via_rest",
            side_effect=RuntimeError("Forbidden"),
        ):
            with patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="test-pat"):
                with patch("agentic_devtools.cli.azure_devops.helpers.run_safe", return_value=mock_result):
                    with pytest.raises(RuntimeError, match="Empty repository ID"):
                        azure_devops.get_repository_id()

    def test_decodes_percent_encoded_values_for_azure_cli_fallback(self):
        """Test Azure CLI fallback uses decoded project/repository names."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "repo-guid-123\n"

        with patch(
            "agentic_devtools.cli.azure_devops.helpers._get_repository_id_via_rest",
            side_effect=RuntimeError("Forbidden"),
        ):
            with patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="test-pat"):
                with patch(
                    "agentic_devtools.cli.azure_devops.helpers.run_safe",
                    return_value=mock_result,
                ) as mock_run_safe:
                    repo_id = azure_devops.get_repository_id(
                        organization="https://dev.azure.com/swica",
                        project="Dragonfly%20Mgmt",
                        repository="dfly-platform%20management",
                    )

        assert repo_id == "repo-guid-123"
        called_cmd = mock_run_safe.call_args[0][0]
        assert "Dragonfly Mgmt" in called_cmd
        assert "dfly-platform management" in called_cmd
        assert "Dragonfly%20Mgmt" not in called_cmd
        assert "dfly-platform%20management" not in called_cmd

    def test_sets_pat_env_for_azure_cli_fallback(self):
        """Test Azure CLI fallback receives PAT via AZURE_DEVOPS_EXT_PAT."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "repo-guid-123\n"

        with patch(
            "agentic_devtools.cli.azure_devops.helpers._get_repository_id_via_rest",
            side_effect=RuntimeError("Forbidden"),
        ):
            with patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="test-pat"):
                with patch(
                    "agentic_devtools.cli.azure_devops.helpers.run_safe",
                    return_value=mock_result,
                ) as mock_run_safe:
                    repo_id = azure_devops.get_repository_id()

        assert repo_id == "repo-guid-123"
        assert mock_run_safe.call_args.kwargs["env"]["AZURE_DEVOPS_EXT_PAT"] == "test-pat"

    def test_raises_when_rest_fails_and_pat_not_available(self):
        """Test OSError from get_pat is wrapped in RuntimeError with REST failure context."""
        with patch(
            "agentic_devtools.cli.azure_devops.helpers._get_repository_id_via_rest",
            side_effect=RuntimeError("Forbidden"),
        ):
            with patch(
                "agentic_devtools.cli.azure_devops.helpers.get_pat",
                side_effect=OSError("AZURE_DEV_OPS_COPILOT_PAT is not set"),
            ):
                with pytest.raises(RuntimeError, match="REST lookup failed") as exc_info:
                    azure_devops.get_repository_id()

        assert "Azure CLI fallback failed" in str(exc_info.value)
        assert "PAT not available" in str(exc_info.value)
        assert exc_info.value.__cause__ is not None
        assert isinstance(exc_info.value.__cause__, OSError)

    def test_escapes_percent_signs_in_project_name_on_windows(self):
        """Test a literal % in a decoded project name is doubled before the az CLI call on Windows."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "repo-guid-456\n"

        with patch(
            "agentic_devtools.cli.azure_devops.helpers._get_repository_id_via_rest",
            side_effect=RuntimeError("REST failed"),
        ):
            with patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="test-pat"):
                with patch(
                    "agentic_devtools.cli.azure_devops.helpers.run_safe",
                    return_value=mock_result,
                ) as mock_run_safe:
                    with patch("agentic_devtools.cli.azure_devops.helpers.sys") as mock_sys:
                        mock_sys.platform = "win32"
                        azure_devops.get_repository_id(
                            organization="https://dev.azure.com/org",
                            project="Proj%25Name",  # %25 decodes to literal %
                            repository="my-repo",
                        )

        called_cmd = mock_run_safe.call_args[0][0]
        # After unquote: "Proj%Name"; after _escape_for_cmd on win32: "Proj%%Name"
        assert "Proj%%Name" in called_cmd

    def test_escapes_percent_signs_in_organization_on_windows(self):
        """Test a literal % in organization is doubled before the az CLI call on Windows."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "repo-guid-789\n"

        with patch(
            "agentic_devtools.cli.azure_devops.helpers._get_repository_id_via_rest",
            side_effect=RuntimeError("REST failed"),
        ):
            with patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="test-pat"):
                with patch(
                    "agentic_devtools.cli.azure_devops.helpers.run_safe",
                    return_value=mock_result,
                ) as mock_run_safe:
                    with patch("agentic_devtools.cli.azure_devops.helpers.sys") as mock_sys:
                        mock_sys.platform = "win32"
                        azure_devops.get_repository_id(
                            organization="https://dev.azure.com/%NAME%",
                            project="MyProject",
                            repository="my-repo",
                        )

        called_cmd = mock_run_safe.call_args[0][0]
        # After _escape_for_cmd on win32: %% doubled, ^ prefixed for shell ops
        assert any("%%NAME%%" in arg for arg in called_cmd)

    def test_raises_when_rest_fails_and_az_cli_missing(self):
        """Test missing Azure CLI is wrapped with REST failure context."""
        with patch(
            "agentic_devtools.cli.azure_devops.helpers._get_repository_id_via_rest",
            side_effect=RuntimeError("Forbidden"),
        ):
            with patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="test-pat"):
                with patch(
                    "agentic_devtools.cli.azure_devops.helpers.run_safe",
                    side_effect=FileNotFoundError("az not found"),
                ):
                    with pytest.raises(RuntimeError, match="REST lookup failed") as exc_info:
                        azure_devops.get_repository_id()

        assert "Azure CLI fallback failed: Azure CLI not found" in str(exc_info.value)
        assert exc_info.value.__cause__ is not None
        assert isinstance(exc_info.value.__cause__, FileNotFoundError)
