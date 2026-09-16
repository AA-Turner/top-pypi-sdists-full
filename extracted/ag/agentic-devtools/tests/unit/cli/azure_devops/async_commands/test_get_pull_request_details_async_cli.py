"""Tests for the get_pull_request_details_async_cli function."""

import sys
from unittest.mock import patch

import pytest

from agentic_devtools.cli.azure_devops.async_commands import get_pull_request_details_async_cli


class TestGetPullRequestDetailsAsyncCli:
    """Tests for the help-aware PR details CLI entry point."""

    @pytest.mark.parametrize("help_option", ["-h", "--help"])
    def test_help_is_side_effect_free(self, help_option, capsys):
        """Help prints usage without reading state or starting a task."""
        with patch.object(sys, "argv", ["agdt-get-pull-request-details", help_option]):
            with patch("agentic_devtools.cli.azure_devops.async_commands.get_value") as mock_get_value:
                with patch(
                    "agentic_devtools.cli.azure_devops.async_commands.run_function_in_background"
                ) as mock_background:
                    with pytest.raises(SystemExit) as exc_info:
                        get_pull_request_details_async_cli()

        captured = capsys.readouterr()
        assert exc_info.value.code == 0
        assert "usage:" in captured.out
        assert "pull_request_id" in captured.out
        mock_get_value.assert_not_called()
        mock_background.assert_not_called()

    @pytest.mark.parametrize("help_option", ["-hh", "-hx"])
    def test_repeated_or_trailing_short_help_is_side_effect_free(self, help_option, capsys):
        """A combined short option starting with -h still triggers genuine help."""
        with patch.object(sys, "argv", ["agdt-get-pull-request-details", help_option]):
            with patch("agentic_devtools.cli.azure_devops.async_commands.get_value") as mock_get_value:
                with patch(
                    "agentic_devtools.cli.azure_devops.async_commands.run_function_in_background"
                ) as mock_background:
                    with pytest.raises(SystemExit) as exc_info:
                        get_pull_request_details_async_cli()

        captured = capsys.readouterr()
        assert exc_info.value.code == 0
        assert "usage:" in captured.out
        mock_get_value.assert_not_called()
        mock_background.assert_not_called()

    def test_invalid_explicit_help_value_is_a_parser_error(self, capsys):
        """An explicit value on --help is a parser error, not genuine help."""
        with patch.object(sys, "argv", ["agdt-get-pull-request-details", "--help=foo"]):
            with patch("agentic_devtools.cli.azure_devops.async_commands.get_value") as mock_get_value:
                with patch(
                    "agentic_devtools.cli.azure_devops.async_commands.run_function_in_background"
                ) as mock_background:
                    with pytest.raises(SystemExit) as exc_info:
                        get_pull_request_details_async_cli()

        captured = capsys.readouterr()
        assert exc_info.value.code == 2
        assert "usage:" in captured.err
        mock_get_value.assert_not_called()
        mock_background.assert_not_called()

    def test_option_termination_before_help_is_unrecognized(self, capsys):
        """A literal "--help" positional after "--" is not treated as help."""
        with patch.object(sys, "argv", ["agdt-get-pull-request-details", "--", "--help"]):
            with patch("agentic_devtools.cli.azure_devops.async_commands.get_value") as mock_get_value:
                with patch(
                    "agentic_devtools.cli.azure_devops.async_commands.run_function_in_background"
                ) as mock_background:
                    with pytest.raises(SystemExit) as exc_info:
                        get_pull_request_details_async_cli()

        captured = capsys.readouterr()
        assert exc_info.value.code == 2
        assert "unrecognized arguments" in captured.err
        mock_get_value.assert_not_called()
        mock_background.assert_not_called()

    def test_normal_invocation_dispatches_without_exiting(self):
        """A normal invocation (no help option) queues the async command."""
        with patch.object(sys, "argv", ["agdt-get-pull-request-details"]):
            with patch("agentic_devtools.cli.azure_devops.async_commands.get_pull_request_details_async") as mock_async:
                get_pull_request_details_async_cli()

        mock_async.assert_called_once_with()
