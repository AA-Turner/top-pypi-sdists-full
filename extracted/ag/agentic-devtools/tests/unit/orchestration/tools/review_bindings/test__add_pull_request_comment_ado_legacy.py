"""Tests for _add_pull_request_comment_ado_legacy()."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.orchestration.tools.review_bindings import (
    _add_pull_request_comment_ado_legacy,
)


class TestAddPullRequestCommentAdoLegacy:
    """Tests for _add_pull_request_comment_ado_legacy() — always routes to azure_devops."""

    def test_forces_azure_devops_provider(self) -> None:
        """Legacy alias always passes provider=azure_devops regardless of kwargs."""
        with patch("agentic_devtools.orchestration.tools.review_bindings._add_pull_request_comment") as mock_add:
            mock_add.return_value = {"success": True}
            _add_pull_request_comment_ado_legacy(pull_request_id=123, content="text")

        mock_add.assert_called_once()
        assert mock_add.call_args.kwargs.get("provider") == "azure_devops"

    def test_caller_cannot_override_provider(self) -> None:
        """Provider passed by caller is overwritten to azure_devops."""
        with patch("agentic_devtools.orchestration.tools.review_bindings._add_pull_request_comment") as mock_add:
            mock_add.return_value = {"success": True}
            _add_pull_request_comment_ado_legacy(pull_request_id=123, content="text", provider="github")

        mock_add.assert_called_once()
        assert mock_add.call_args.kwargs.get("provider") == "azure_devops"
