"""Tests for :func:`agentic_devtools.cli.setup.provider_connectivity.check_provider_connectivity`."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.setup.provider_connectivity import check_provider_connectivity


class TestCheckProviderConnectivity:
    """Exercise dispatcher behavior for provider pre-flight checks."""

    def test_non_positive_timeout_returns_validation_failure(self, tmp_path: Path) -> None:
        """Non-positive timeout is rejected before provider-specific dispatch."""
        assert check_provider_connectivity("jira", tmp_path, timeout=0) == (
            False,
            "Connectivity timeout must be greater than 0 seconds",
        )
        assert check_provider_connectivity("github", tmp_path, timeout=-1.0) == (
            False,
            "Connectivity timeout must be greater than 0 seconds",
        )

    def test_dispatches_to_jira_helper(self, tmp_path: Path) -> None:
        """Jira provider is routed to the Jira connectivity helper."""
        with patch(
            "agentic_devtools.cli.setup.provider_connectivity._check_jira_connectivity",
            return_value=(True, None),
        ) as mock_check:
            assert check_provider_connectivity("JIRA", tmp_path, timeout=5.0) == (True, None)

        mock_check.assert_called_once_with(tmp_path, 5.0)

    def test_dispatches_to_github_helper(self, tmp_path: Path) -> None:
        """GitHub provider is routed to the GitHub connectivity helper."""
        with patch(
            "agentic_devtools.cli.setup.provider_connectivity._check_github_connectivity",
            return_value=(True, None),
        ) as mock_check:
            assert check_provider_connectivity("github", tmp_path, timeout=5.0) == (True, None)

        mock_check.assert_called_once_with(tmp_path, 5.0)

    def test_dispatches_to_markdown_helper(self, tmp_path: Path) -> None:
        """Markdown provider is routed to the markdown workspace helper."""
        with patch(
            "agentic_devtools.cli.setup.provider_connectivity._check_markdown_connectivity",
            return_value=(True, None),
        ) as mock_check:
            assert check_provider_connectivity("markdown", tmp_path, timeout=5.0) == (True, None)

        mock_check.assert_called_once_with(tmp_path, timeout=5.0)

    def test_generic_exception_is_wrapped_as_false(self, tmp_path: Path) -> None:
        """Unexpected internal exceptions are converted into a non-fatal connectivity failure."""
        with patch(
            "agentic_devtools.cli.setup.provider_connectivity._check_jira_connectivity",
            side_effect=RuntimeError("unexpected internal error"),
        ):
            is_connected, error = check_provider_connectivity("jira", tmp_path, timeout=5.0)

        assert is_connected is False
        assert "unexpected internal error" in (error or "")

    def test_unknown_provider_returns_false(self, tmp_path: Path) -> None:
        """Unsupported provider slugs fail gracefully with a clear message."""
        is_connected, error = check_provider_connectivity("not-a-real-provider", tmp_path, timeout=5.0)

        assert is_connected is False
        assert error == "Unsupported issue provider: not-a-real-provider"
