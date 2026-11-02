"""
Tests for run_details_commands module.
"""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops.run_details_commands import (
    fetch_failed_job_logs,
)


class TestFetchFailedJobLogs:
    """Tests for fetch_failed_job_logs function."""

    @patch("agentic_devtools.cli.azure_devops.run_details_commands.require_requests")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands.get_pat")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands._fetch_build_timeline")
    def test_returns_error_on_timeline_failure(self, mock_timeline, mock_pat, mock_requests):
        """Should return error when timeline fetch fails."""
        mock_pat.return_value = "fake-pat"
        mock_timeline.return_value = (None, "Timeline error")

        result = fetch_failed_job_logs(123)

        assert result["success"] is False
        assert "Timeline error" in result["error"]

    @patch("agentic_devtools.cli.azure_devops.run_details_commands.require_requests")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands.get_pat")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands._fetch_build_timeline")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands._get_failed_tasks")
    def test_success_with_no_failed_tasks(self, mock_get_failed, mock_timeline, mock_pat, mock_requests):
        """Should return success when no failed tasks found."""
        mock_pat.return_value = "fake-pat"
        mock_timeline.return_value = ({"records": []}, None)
        mock_get_failed.return_value = []

        result = fetch_failed_job_logs(123)

        assert result["success"] is True
        assert result["failed_tasks"] == []

    @patch("agentic_devtools.cli.azure_devops.run_details_commands.require_requests")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands.get_pat")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands._fetch_build_timeline")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands._get_failed_tasks")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands._fetch_task_log")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands._save_log_file")
    def test_fetches_and_saves_logs(
        self,
        mock_save,
        mock_fetch_log,
        mock_get_failed,
        mock_timeline,
        mock_pat,
        mock_requests,
    ):
        """Should fetch and save logs for failed tasks with vpn_toggle=False."""
        mock_pat.return_value = "fake-pat"
        mock_timeline.return_value = ({"records": []}, None)
        mock_get_failed.return_value = [{"name": "Build", "log_url": "https://log.url/1"}]
        mock_fetch_log.return_value = ("Log content here", None)
        mock_save.return_value = "/tmp/build.log"

        # Use vpn_toggle=False to avoid VpnToggleContext path
        result = fetch_failed_job_logs(123, vpn_toggle=False)

        assert result["success"] is True
        assert len(result["log_files"]) == 1
        assert result["log_files"][0]["task_name"] == "Build"

    @patch("agentic_devtools.cli.azure_devops.run_details_commands.require_requests")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands.get_pat")
    def test_vpn_toggle_corporate_network_skips_logs(self, mock_pat, mock_requests, capsys):
        """Should skip log fetching on corporate network without VPN."""
        mock_pat.return_value = "fake-pat"

        with patch("agentic_devtools.cli.azure_devops.vpn_toggle.check_network_status") as mock_net:
            from agentic_devtools.cli.azure_devops.vpn_toggle import NetworkStatus

            mock_net.return_value = (NetworkStatus.CORPORATE_NETWORK_NO_VPN, "On corp net")

            result = fetch_failed_job_logs(123, vpn_toggle=True)

        assert result["success"] is True
        assert result["error"] == "Cannot fetch logs from corporate network (no VPN to toggle)"
        captured = capsys.readouterr()
        assert "Cannot fetch logs from corporate network" in captured.out

    @patch("agentic_devtools.cli.azure_devops.run_details_commands._save_log_file")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands._fetch_task_log")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands._get_failed_tasks")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands._fetch_build_timeline")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands.get_pat")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands.require_requests")
    def test_vpn_toggle_normal_network_fetches_logs(
        self, mock_requests, mock_pat, mock_timeline, mock_get_failed, mock_fetch_log, mock_save
    ):
        """Should fetch logs normally when vpn_toggle is True but network is fine."""
        mock_pat.return_value = "fake-pat"
        mock_timeline.return_value = ({"records": []}, None)
        mock_get_failed.return_value = [{"name": "Test", "log_url": "https://log.url/1"}]
        mock_fetch_log.return_value = ("Log content", None)
        mock_save.return_value = "/tmp/test.log"

        with patch("agentic_devtools.cli.azure_devops.vpn_toggle.check_network_status") as mock_net:
            from agentic_devtools.cli.azure_devops.vpn_toggle import NetworkStatus

            mock_net.return_value = (NetworkStatus.EXTERNAL_ACCESS_OK, "Normal network")

            result = fetch_failed_job_logs(123, vpn_toggle=True)

        assert result["success"] is True
        assert len(result["log_files"]) == 1

    @patch("agentic_devtools.cli.azure_devops.run_details_commands._save_log_file")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands._fetch_task_log")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands._get_failed_tasks")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands._fetch_build_timeline")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands.get_pat")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands.require_requests")
    def test_multiple_failed_tasks_fetches_all_logs(
        self, mock_requests, mock_pat, mock_timeline, mock_get_failed, mock_fetch_log, mock_save
    ):
        """Should iterate over multiple failed tasks and fetch logs for each."""
        mock_pat.return_value = "fake-pat"
        mock_timeline.return_value = ({"records": []}, None)
        mock_get_failed.return_value = [
            {"name": "Build", "log_url": "https://log.url/1"},
            {"name": "Test", "log_url": "https://log.url/2"},
        ]
        mock_fetch_log.side_effect = [("Log 1", None), ("Log 2", None)]
        mock_save.side_effect = ["/tmp/build.log", "/tmp/test.log"]

        result = fetch_failed_job_logs(123, vpn_toggle=False)

        assert result["success"] is True
        assert len(result["log_files"]) == 2
        assert result["log_files"][0]["task_name"] == "Build"
        assert result["log_files"][1]["task_name"] == "Test"

    @patch("agentic_devtools.cli.azure_devops.run_details_commands._save_log_file")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands._fetch_task_log")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands._get_failed_tasks")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands._fetch_build_timeline")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands.get_pat")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands.require_requests")
    def test_skips_task_when_log_fetch_returns_no_content(
        self, mock_requests, mock_pat, mock_timeline, mock_get_failed, mock_fetch_log, mock_save
    ):
        """Should skip saving when log content is empty/None."""
        mock_pat.return_value = "fake-pat"
        mock_timeline.return_value = ({"records": []}, None)
        mock_get_failed.return_value = [
            {"name": "Build", "log_url": "https://log.url/1"},
            {"name": "Test", "log_url": "https://log.url/2"},
        ]
        # First task returns no content, second returns content
        mock_fetch_log.side_effect = [(None, "Fetch error"), ("Log 2", None)]
        mock_save.return_value = "/tmp/test.log"

        result = fetch_failed_job_logs(123, vpn_toggle=False)

        assert result["success"] is True
        assert len(result["log_files"]) == 1
        assert result["log_files"][0]["task_name"] == "Test"
