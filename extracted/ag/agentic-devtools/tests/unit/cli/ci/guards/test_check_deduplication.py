"""Eligibility checks must never consume successful dispatch budget."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.guards import check_deduplication


class TestCheckDeduplication:
    @pytest.mark.parametrize("count,skip", [(0, False), (2, False), (3, True), (8, True)])
    def test_repeated_checks_are_read_only(self, count: int, skip: bool) -> None:
        provider = MagicMock()
        provider.find_comment.return_value = (100, f"<!-- repair-dispatch:abc123:{count} -->") if count else None

        assert check_deduplication(provider, 42, "abc123") == (skip, count)
        assert check_deduplication(provider, 42, "abc123") == (skip, count)
        provider.post_comment.assert_not_called()
        provider.update_comment.assert_not_called()

    @pytest.mark.parametrize("count,skip", [(0, False), (2, False), (3, True), (8, True)])
    def test_scoped_checks_use_confirmed_receipts_without_writes(self, count, skip) -> None:
        provider = MagicMock()
        with patch(
            "agentic_devtools.cli.ci.repair_accounting.RepairDispatchLedger.read",
            return_value=({str(index) for index in range(count)}, False, 1),
        ):
            assert check_deduplication(provider, 42, "abc123", review_id=10, work_key="work") == (skip, count)
        provider.post_comment.assert_not_called()
        provider.update_comment.assert_not_called()

    def test_changed_head_has_zero_confirmed_dispatches(self) -> None:
        provider = MagicMock()
        provider.find_comment.return_value = (100, "<!-- repair-dispatch:abc123:8 -->")

        assert check_deduplication(provider, 42, "def456") == (False, 0)
        provider.post_comment.assert_not_called()
        provider.update_comment.assert_not_called()
