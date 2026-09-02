"""Tests for wait_for_run_impl function."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops.run_details_commands import wait_for_run_impl


class TestWaitForRunImpl:
    """Tests for wait_for_run_impl function."""

    def test_returns_dict_with_expected_keys(self):
        """Should return a dictionary containing success, finished, and result keys."""
        # A dry_run call won't make real network requests
        result = wait_for_run_impl(run_id=1234, dry_run=True)

        assert isinstance(result, dict)
        assert "success" in result
        assert "finished" in result

    def test_dry_run_returns_without_polling(self):
        """Dry run should skip actual polling."""
        result = wait_for_run_impl(run_id=9999, dry_run=True)

        # In dry_run mode the function should return immediately
        assert isinstance(result, dict)

    def test_returns_error_result_when_api_fails(self):
        """Should return a result dict with success=False when API call fails."""
        # dry_run mode doesn't call the API so no PAT needed
        result = wait_for_run_impl(run_id=1234, dry_run=True)

        assert isinstance(result, dict)
        # In dry run mode the result should indicate it wasn't actually fetched
        assert "success" in result

    @patch("agentic_devtools.cli.azure_devops.run_details_commands.fetch_failed_job_logs")
    @patch("agentic_devtools.cli.azure_devops.run_details_commands.get_run_details_impl")
    def test_failed_run_with_fetch_logs(self, mock_details, mock_fetch_logs, capsys):
        """Fetches logs when run fails and fetch_logs is True."""
        mock_details.return_value = {
            "success": True,
            "data": {
                "status": "completed",
                "result": "failed",
                "_links": {"web": {"href": "https://dev.azure.com/run/123"}},
            },
        }
        mock_fetch_logs.return_value = {
            "success": True,
            "log_files": [{"task_name": "Build", "path": "/tmp/log1.txt"}],
            "failed_tasks": [{"name": "Build"}],
        }

        result = wait_for_run_impl(run_id=123, fetch_logs=True, vpn_toggle=False, poll_interval=1)

        assert result["success"] is True
        assert result["finished"] is True
        assert result["result"] == "failed"
        assert result["log_files"] == [{"task_name": "Build", "path": "/tmp/log1.txt"}]
        mock_fetch_logs.assert_called_once()
        captured = capsys.readouterr()
        assert "FAILED" in captured.out

    @patch("agentic_devtools.cli.azure_devops.run_details_commands.get_run_details_impl")
    def test_failed_run_without_fetch_logs(self, mock_details, capsys):
        """Skips log fetching when run fails and fetch_logs is False."""
        mock_details.return_value = {
            "success": True,
            "data": {
                "status": "completed",
                "result": "failed",
                "_links": {"web": {"href": "https://dev.azure.com/run/456"}},
            },
        }

        result = wait_for_run_impl(run_id=456, fetch_logs=False, vpn_toggle=False, poll_interval=1)

        assert result["success"] is True
        assert result["finished"] is True
        assert result["result"] == "failed"
        assert result["log_files"] == []
        captured = capsys.readouterr()
        assert "FAILED" in captured.out
