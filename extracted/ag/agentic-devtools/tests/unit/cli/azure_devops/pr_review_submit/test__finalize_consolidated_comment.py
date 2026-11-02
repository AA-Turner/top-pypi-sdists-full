"""Tests for _finalize_consolidated_comment."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops.pr_review_submit import _finalize_consolidated_comment

_REFRESH = "agentic_devtools.cli.azure_devops.pr_review_refresh"


class TestFinalizeConsolidatedComment:
    def test_calls_refresh_core_final(self):
        with patch(f"{_REFRESH}.refresh_core") as refresh_core:
            _finalize_consolidated_comment(7, "reqs")
        refresh_core.assert_called_once_with(7, dry_run=False, force=True, final=True, requests_module="reqs")
