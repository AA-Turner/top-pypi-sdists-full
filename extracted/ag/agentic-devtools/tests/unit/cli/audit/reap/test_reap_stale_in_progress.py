"""Tests for reap_stale_in_progress()."""

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.audit.config import LABEL_IN_PROGRESS
from agentic_devtools.cli.audit.reap import DEFAULT_MAX_AGE_HOURS, reap_stale_in_progress


def _ago(hours: float) -> datetime:
    return datetime.now(tz=timezone.utc) - timedelta(hours=hours)


class TestReapStaleInProgress:
    """Stale in-progress label recovery."""

    def test_reaps_pr_older_than_max_age(self) -> None:
        provider = MagicMock()
        provider.list_prs_with_label.return_value = [101]
        provider.get_label_applied_at.return_value = _ago(30)

        result = reap_stale_in_progress(provider, max_age_hours=24)

        assert result["reaped"] == [101]
        assert result["skipped"] == []
        assert result["checked"] == 1
        provider.remove_label.assert_called_once_with(101, LABEL_IN_PROGRESS)

    def test_skips_recent_pr(self) -> None:
        provider = MagicMock()
        provider.list_prs_with_label.return_value = [102]
        provider.get_label_applied_at.return_value = _ago(1)

        result = reap_stale_in_progress(provider, max_age_hours=24)

        assert result["reaped"] == []
        assert result["skipped"] == [102]
        provider.remove_label.assert_not_called()

    def test_skips_pr_with_unknown_timestamp(self) -> None:
        provider = MagicMock()
        provider.list_prs_with_label.return_value = [103]
        provider.get_label_applied_at.return_value = None

        result = reap_stale_in_progress(provider, max_age_hours=24)

        assert result["skipped"] == [103]
        provider.remove_label.assert_not_called()

    def test_remove_label_failure_marks_skipped(self) -> None:
        provider = MagicMock()
        provider.list_prs_with_label.return_value = [104]
        provider.get_label_applied_at.return_value = _ago(50)
        provider.remove_label.side_effect = RuntimeError("api down")

        result = reap_stale_in_progress(provider, max_age_hours=24)

        assert result["reaped"] == []
        assert result["skipped"] == [104]

    def test_no_prs_returns_empty_summary(self) -> None:
        provider = MagicMock()
        provider.list_prs_with_label.return_value = []

        result = reap_stale_in_progress(provider)

        assert result == {"checked": 0, "reaped": [], "skipped": []}

    def test_uses_default_max_age_when_unspecified(self) -> None:
        provider = MagicMock()
        provider.list_prs_with_label.return_value = [105]
        provider.get_label_applied_at.return_value = _ago(DEFAULT_MAX_AGE_HOURS - 1)

        result = reap_stale_in_progress(provider)

        assert result["skipped"] == [105]

    def test_mixed_batch(self) -> None:
        provider = MagicMock()
        provider.list_prs_with_label.return_value = [201, 202, 203]
        ages = {201: _ago(30), 202: _ago(2), 203: None}
        provider.get_label_applied_at.side_effect = lambda pr, _label: ages[pr]

        result = reap_stale_in_progress(provider, max_age_hours=24)

        assert result["reaped"] == [201]
        assert sorted(result["skipped"]) == [202, 203]
        assert result["checked"] == 3

    def test_raises_on_zero_max_age_hours(self) -> None:
        provider = MagicMock()
        with pytest.raises(ValueError, match="must be a positive number"):
            reap_stale_in_progress(provider, max_age_hours=0)
        provider.list_prs_with_label.assert_not_called()

    def test_raises_on_negative_max_age_hours(self) -> None:
        provider = MagicMock()
        with pytest.raises(ValueError, match="must be a positive number"):
            reap_stale_in_progress(provider, max_age_hours=-1.5)
        provider.list_prs_with_label.assert_not_called()

    def test_skips_pr_with_naive_datetime_timestamp(self) -> None:
        provider = MagicMock()
        provider.list_prs_with_label.return_value = [106]
        # naive datetime — no tzinfo
        provider.get_label_applied_at.return_value = datetime(2024, 1, 1, 0, 0, 0)

        result = reap_stale_in_progress(provider, max_age_hours=24)

        assert result["reaped"] == []
        assert result["skipped"] == [106]
        provider.remove_label.assert_not_called()
