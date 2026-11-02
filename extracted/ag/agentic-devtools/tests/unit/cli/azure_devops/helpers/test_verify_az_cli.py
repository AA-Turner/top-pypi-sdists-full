"""Tests for verify_az_cli function."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.azure_devops.helpers import verify_az_cli


class TestVerifyAzCli:
    """Tests for verify_az_cli function."""

    def test_rejects_negative_timeout_before_running_az(self):
        """Reject a negative timeout before starting either Azure CLI probe."""
        with patch("agentic_devtools.cli.azure_devops.helpers.run_safe") as run_safe:
            with pytest.raises(ValueError, match="timeout must be non-negative"):
                verify_az_cli(timeout=-1)

        run_safe.assert_not_called()

    def test_does_not_exit_when_az_available(self):
        """Should complete without raising SystemExit when az CLI is installed."""
        from unittest.mock import MagicMock

        mock_result = MagicMock()
        mock_result.returncode = 0

        ext_result = MagicMock()
        ext_result.returncode = 0
        ext_result.stdout = "azure-devops"

        with patch(
            "agentic_devtools.cli.azure_devops.helpers.run_safe",
            side_effect=[mock_result, ext_result],
        ) as run_safe:
            verify_az_cli(timeout=30)  # Should not raise

        assert run_safe.call_args_list[0].kwargs["timeout"] == 30
        assert run_safe.call_args_list[1].kwargs["timeout"] == 30

    def test_exits_when_az_not_installed(self):
        """Should raise SystemExit when az CLI is not found."""
        with patch(
            "agentic_devtools.cli.azure_devops.helpers.run_safe",
            side_effect=FileNotFoundError("az not found"),
        ):
            with pytest.raises(SystemExit):
                verify_az_cli()

    def test_exits_when_azure_devops_extension_missing(self):
        """Should raise SystemExit when azure-devops extension is not installed."""
        from unittest.mock import MagicMock

        mock_result = MagicMock()
        mock_result.returncode = 0

        ext_result = MagicMock()
        ext_result.returncode = 0
        ext_result.stdout = ""

        with patch(
            "agentic_devtools.cli.azure_devops.helpers.run_safe",
            side_effect=[mock_result, ext_result],
        ):
            with pytest.raises(SystemExit):
                verify_az_cli()
