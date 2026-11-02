"""Tests for _collect_pr_data()."""

from unittest.mock import MagicMock

from agentic_devtools.cli.audit.models import ClosedPRInfo
from agentic_devtools.cli.audit.prepare import _collect_pr_data


class TestCollectPrData:
    """Tests for the _collect_pr_data helper."""

    def test_returns_none_when_pr_not_in_eligible_list(self) -> None:
        provider = MagicMock()
        eligible_prs = [
            ClosedPRInfo(
                number=1,
                title="PR #1",
                url="https://github.com/org/repo/pull/1",
                state="closed",
                closed_at="2024-01-15T10:00:00Z",
                merged=True,
            ),
        ]

        result = _collect_pr_data(provider, 99, eligible_prs)

        assert result is None
        provider.list_all_review_comments.assert_not_called()
