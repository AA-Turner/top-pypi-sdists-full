"""Tests for _submit_summary_ado_legacy()."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.orchestration.tools.review_bindings import (
    _submit_summary_ado_legacy,
)


class TestSubmitSummaryAdoLegacy:
    """Tests for _submit_summary_ado_legacy() — always routes to azure_devops."""

    def test_forces_azure_devops_provider(self) -> None:
        """Legacy summary alias always passes provider=azure_devops."""
        with patch("agentic_devtools.orchestration.tools.review_bindings._add_pull_request_comment") as mock_add:
            mock_add.return_value = {"success": True}
            _submit_summary_ado_legacy(pull_request_id=1, summary="All good")

        mock_add.assert_called_once()
        assert mock_add.call_args.kwargs.get("provider") == "azure_devops"

    def test_caller_cannot_override_provider(self) -> None:
        """Provider passed by caller is overwritten to azure_devops."""
        with patch("agentic_devtools.orchestration.tools.review_bindings._add_pull_request_comment") as mock_add:
            mock_add.return_value = {"success": True}
            _submit_summary_ado_legacy(pull_request_id=1, summary="All good", provider="github")

        mock_add.assert_called_once()
        assert mock_add.call_args.kwargs.get("provider") == "azure_devops"
