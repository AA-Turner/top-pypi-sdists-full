"""Tests for SchedulerResult dataclass."""

from agentic_devtools.cli.ci.scheduler import SchedulerResult


class TestSchedulerResult:
    """Tests for the SchedulerResult frozen dataclass."""

    def test_create_with_defaults(self) -> None:
        result = SchedulerResult(
            run_mode="live",
            batch_size=1,
            pool_size=1,
            eligible_count=5,
            dispatched_count=1,
        )
        assert result.run_mode == "live"
        assert result.batch_size == 1
        assert result.pool_size == 1
        assert result.eligible_count == 5
        assert result.dispatched_count == 1
        assert result.dispatched_prs == []
        assert result.cursor_before is None
        assert result.cursor_after is None
        assert result.cursor_persisted is False
        assert result.had_dispatch_error is False

    def test_create_with_all_fields(self) -> None:
        result = SchedulerResult(
            run_mode="dry_run",
            batch_size=3,
            pool_size=10,
            eligible_count=10,
            dispatched_count=3,
            dispatched_prs=[2020, 2021, 2022],
            cursor_before=2019,
            cursor_after=2022,
            cursor_persisted=True,
            had_dispatch_error=True,
        )
        assert result.dispatched_prs == [2020, 2021, 2022]
        assert result.pool_size == 10
        assert result.cursor_before == 2019
        assert result.cursor_after == 2022
        assert result.cursor_persisted is True
        assert result.had_dispatch_error is True
