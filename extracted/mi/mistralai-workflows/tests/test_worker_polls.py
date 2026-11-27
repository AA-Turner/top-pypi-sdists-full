import pytest

from mistralai.workflows.core.execution.sticky_session.sticky_worker_session import set_activity_as_sticky_to_worker
from mistralai.workflows.core.rate_limiting.rate_limit import RateLimit, set_rate_limit
from mistralai.workflows.core.worker_polls import (
    distinct_rate_limit_keys,
    estimate_connection_polls,
    format_poll_warning,
    group_activities_by_worker_config,
)

MAIN_TASK_QUEUE = "main-queue"
STICKY_TASK_QUEUE = f"{MAIN_TASK_QUEUE}-sticky-worker-session-abc"


CONNECTION_STREAM_LIMIT = 100


def _rate_limited_activities(n_rate_limit_keys: int) -> list:
    activities = []
    for key in range(n_rate_limit_keys):

        async def rate_limited_activity():
            pass

        set_rate_limit(rate_limited_activity, RateLimit(time_window_in_sec=1, max_execution=1, key=f"key-{key}"))
        activities.append(rate_limited_activity)
    return activities


class TestGroupActivitiesByWorkerConfig:
    def test_splits_sticky_rate_limited_and_main_workers(self):
        rate_limited = _rate_limited_activities(1)

        async def sticky_activity():
            pass

        set_activity_as_sticky_to_worker(sticky_activity)

        async def plain_activity():
            pass

        groups = group_activities_by_worker_config(
            [plain_activity, sticky_activity, *rate_limited], MAIN_TASK_QUEUE, STICKY_TASK_QUEUE
        )

        main_groups = [g for g in groups if g.is_main]
        sticky_groups = [g for g in groups if g.is_sticky]
        rate_limited_groups = [g for g in groups if not g.is_main and not g.is_sticky]

        assert len(groups) == 3
        assert len(main_groups) == 1
        assert main_groups[0].activities == [plain_activity, sticky_activity, *rate_limited]
        assert len(sticky_groups) == 1
        assert sticky_groups[0].worker_config.task_queue == STICKY_TASK_QUEUE
        assert sticky_groups[0].activities == [sticky_activity]
        assert len(rate_limited_groups) == 1
        assert rate_limited_groups[0].rate_limit_key == "key-0"
        assert rate_limited_groups[0].worker_config.max_task_queue_activities_per_second == 1.0

    def test_sticky_activities_skip_the_rate_limit_worker(self):
        async def sticky_rate_limited_activity():
            pass

        set_activity_as_sticky_to_worker(sticky_rate_limited_activity)
        set_rate_limit(sticky_rate_limited_activity, RateLimit(time_window_in_sec=1, max_execution=1, key="shared"))

        groups = group_activities_by_worker_config([sticky_rate_limited_activity], MAIN_TASK_QUEUE, STICKY_TASK_QUEUE)

        assert len(groups) == 2
        main_groups = [g for g in groups if g.is_main]
        sticky_groups = [g for g in groups if g.is_sticky]
        assert len(main_groups) == 1
        assert len(sticky_groups) == 1
        assert all(g.rate_limit_key is None for g in groups)

    def test_same_key_with_different_rates_yields_two_workers(self):
        async def first_activity():
            pass

        async def second_activity():
            pass

        set_rate_limit(first_activity, RateLimit(time_window_in_sec=1, max_execution=1, key="shared"))
        set_rate_limit(second_activity, RateLimit(time_window_in_sec=2, max_execution=4, key="shared"))

        groups = group_activities_by_worker_config(
            [first_activity, second_activity], MAIN_TASK_QUEUE, STICKY_TASK_QUEUE
        )

        rate_limited_groups = [g for g in groups if not g.is_main and not g.is_sticky]
        assert len(rate_limited_groups) == 2
        assert {g.rate_limit_key for g in rate_limited_groups} == {"shared"}
        assert {g.worker_config.max_task_queue_activities_per_second for g in rate_limited_groups} == {1.0, 2.0}

    def test_rate_limited_task_queue_is_derived_from_the_main_task_queue_parameter(self):
        groups = group_activities_by_worker_config(_rate_limited_activities(1), "another-queue", STICKY_TASK_QUEUE)

        rate_limited_groups = [g for g in groups if not g.is_main and not g.is_sticky]
        assert rate_limited_groups[0].worker_config.task_queue.startswith("another-queue-rate-limited-")

    def test_default_key_is_the_activity_name(self):
        async def my_rate_limited_activity():
            pass

        set_rate_limit(my_rate_limited_activity, RateLimit(time_window_in_sec=1, max_execution=1, key=None))

        groups = group_activities_by_worker_config([my_rate_limited_activity], MAIN_TASK_QUEUE, STICKY_TASK_QUEUE)

        rate_limited_groups = [g for g in groups if not g.is_main and not g.is_sticky]
        assert len(rate_limited_groups) == 1
        assert rate_limited_groups[0].rate_limit_key == "my_rate_limited_activity"


class TestEstimateConnectionPolls:
    @pytest.mark.parametrize(
        "max_activity_task_pollers, expected_total",
        [
            # 5 workflow + 5 activity polls on the main worker + 19 rate-limited workers × 5
            (5, 105),
            # 5 workflow + 2 activity polls on the main worker + 19 rate-limited workers × 2
            (2, 45),
        ],
    )
    def test_totals_include_every_worker_and_the_main_workflow_polls(self, max_activity_task_pollers, expected_total):
        activities = _rate_limited_activities(19)

        groups = group_activities_by_worker_config(activities, MAIN_TASK_QUEUE, STICKY_TASK_QUEUE)
        estimate = estimate_connection_polls(groups, max_activity_task_pollers, 5, CONNECTION_STREAM_LIMIT)

        assert estimate.total_polls == expected_total
        assert estimate.worker_count == 20
        assert estimate.activity_polls_per_worker == max_activity_task_pollers
        assert estimate.main_workflow_polls == 5
        assert estimate.sticky_worker_count == 0
        assert estimate.rate_limited_worker_count == 19
        assert estimate.rate_limit_keys == sorted(f"key-{i}" for i in range(19))

    def test_same_key_with_different_rates_counts_workers_but_lists_the_key_once(self):
        async def first_activity():
            pass

        async def second_activity():
            pass

        set_rate_limit(first_activity, RateLimit(time_window_in_sec=1, max_execution=1, key="shared"))
        set_rate_limit(second_activity, RateLimit(time_window_in_sec=2, max_execution=4, key="shared"))

        groups = group_activities_by_worker_config(
            [first_activity, second_activity], MAIN_TASK_QUEUE, STICKY_TASK_QUEUE
        )
        estimate = estimate_connection_polls(groups, 5, 5, CONNECTION_STREAM_LIMIT)

        assert estimate.rate_limited_worker_count == 2
        assert estimate.rate_limit_keys == ["shared"]
        assert estimate.multi_rate_keys == ["shared"]
        assert distinct_rate_limit_keys(groups) == ["shared"]

    def test_distinct_keys_are_not_flagged_as_multi_rate(self):
        groups = group_activities_by_worker_config(_rate_limited_activities(3), MAIN_TASK_QUEUE, STICKY_TASK_QUEUE)

        assert estimate_connection_polls(groups, 5, 5, CONNECTION_STREAM_LIMIT).multi_rate_keys == []

    def test_sticky_worker_counts_as_activity_polls_only(self):
        async def sticky_activity():
            pass

        set_activity_as_sticky_to_worker(sticky_activity)

        groups = group_activities_by_worker_config([sticky_activity], MAIN_TASK_QUEUE, STICKY_TASK_QUEUE)
        estimate = estimate_connection_polls(groups, 3, 7, CONNECTION_STREAM_LIMIT)

        # main (7 workflow + 3 activity) + sticky worker (3 activity)
        assert estimate.total_polls == 13
        assert estimate.worker_count == 2
        assert estimate.sticky_worker_count == 1


class TestPollEstimateLimits:
    @pytest.mark.parametrize(
        "limit, expected_threshold, expected_headroom",
        [
            (100, 80, -5),
            (200, 160, 95),
            (None, None, None),
        ],
    )
    def test_threshold_and_headroom_follow_the_configured_limit(self, limit, expected_threshold, expected_headroom):
        groups = group_activities_by_worker_config(_rate_limited_activities(19), MAIN_TASK_QUEUE, STICKY_TASK_QUEUE)

        estimate = estimate_connection_polls(groups, 5, 5, limit)

        assert estimate.total_polls == 105
        assert estimate.warning_threshold == expected_threshold
        assert estimate.headroom == expected_headroom


class TestFormatPollWarning:
    def _warning(self, *, limit: int | None = CONNECTION_STREAM_LIMIT, activity_polls: int = 5, n_keys: int = 19):
        groups = group_activities_by_worker_config(_rate_limited_activities(n_keys), MAIN_TASK_QUEUE, STICKY_TASK_QUEUE)
        estimate = estimate_connection_polls(groups, activity_polls, 5, limit)
        return format_poll_warning(estimate)

    def test_warns_above_threshold_with_names_and_remedies(self):
        warning = self._warning()

        assert warning is not None
        assert "80" in warning
        assert "of the 100 concurrent streams allowed per connection" in warning
        assert "at least 105 concurrent poll streams" in warning
        assert "rate-limit keys [" in warning
        assert all(f"key-{i}" in warning for i in range(19))
        assert "MAX_ACTIVITY_TASK_POLLERS" in warning
        assert "sharing one rate-limit key" in warning
        # The risk is the per-connection stream limit, not the namespace poller quota.
        assert "namespace" not in warning

    def test_states_that_only_poll_streams_are_counted_and_reports_headroom(self):
        warning = self._warning()

        assert warning is not None
        assert "counts poll streams only" in warning
        assert "respond and heartbeat" in warning
        # 105 polls against a 100-stream limit
        assert "leaving -5 of the 100" in warning

    def test_reports_positive_headroom_below_the_limit(self):
        # 5 workflow + 20 workers × 4 activity = 85 polls: past the 80 threshold, 15 streams left.
        warning = self._warning(activity_polls=4)

        assert warning is not None
        assert "leaving 15 of the 100" in warning

    def test_lists_each_rate_limit_key_once_and_hints_at_aligning_rates(self):
        async def first_activity():
            pass

        async def second_activity():
            pass

        set_rate_limit(first_activity, RateLimit(time_window_in_sec=1, max_execution=1, key="shared"))
        set_rate_limit(second_activity, RateLimit(time_window_in_sec=2, max_execution=4, key="shared"))
        groups = group_activities_by_worker_config(
            [first_activity, second_activity], MAIN_TASK_QUEUE, STICKY_TASK_QUEUE
        )

        warning = format_poll_warning(estimate_connection_polls(groups, 40, 5, CONNECTION_STREAM_LIMIT))

        assert warning is not None
        assert "rate-limit keys [shared]" in warning
        assert "shared, shared" not in warning
        assert "Rate-limit keys [shared] are used with different rates" in warning

    def test_no_alignment_hint_when_keys_have_a_single_rate(self):
        warning = self._warning()

        assert warning is not None
        assert "different rates" not in warning

    def test_returns_none_below_threshold(self):
        assert self._warning(activity_polls=2) is None

    def test_returns_none_when_no_limit_is_configured(self):
        assert self._warning(limit=None) is None

    def test_threshold_scales_with_the_configured_limit(self):
        # 105 polls against a 200-stream limit: threshold is 160, so no warning.
        assert self._warning(limit=200) is None
