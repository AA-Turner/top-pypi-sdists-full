"""Tests for esi.rate_limiting module and the rate_limited_task decorator."""

from unittest.mock import MagicMock, patch

from celery import Task
from celery.exceptions import Retry
from redis.exceptions import LockNotOwnedError

from django.core.cache import cache
from django.test import TestCase

from esi.decorators import rate_limited_task
from esi.exceptions import ESIBucketLimitException, TaskBucketLimitException
from esi.rate_limiting import (
    ESIRateLimitBucket,
    ESIRateLimiter,
    TaskRateLimitBucket,
    TaskRateLimiter,
    force_string,
    interval_to_seconds,
    kwargs_to_list,
    limit_to_rate,
    task_bucket_slug_key,
)


class TestIntervalToSeconds(TestCase):
    def test_seconds(self):
        self.assertEqual(interval_to_seconds("s"), 1)

    def test_minutes(self):
        self.assertEqual(interval_to_seconds("m"), 60)

    def test_hours(self):
        self.assertEqual(interval_to_seconds("h"), 3600)

    def test_days(self):
        self.assertEqual(interval_to_seconds("d"), 86400)

    def test_multi_seconds(self):
        self.assertEqual(interval_to_seconds("30s"), 30)

    def test_multi_minutes(self):
        self.assertEqual(interval_to_seconds("15m"), 900)

    def test_multi_hours(self):
        self.assertEqual(interval_to_seconds("2h"), 7200)


class TestForceString(TestCase):
    def test_dict_passthrough(self):
        self.assertEqual(force_string({"a": 1, "b": 2}), {"a": 1, "b": 2})

    def test_list_passthrough(self):
        self.assertEqual(force_string([1, 2, 3]), [1, 2, 3])

    def test_scalar_int_passthrough(self):
        self.assertEqual(force_string(42), 42)

    def test_scalar_str_passthrough(self):
        self.assertEqual(force_string("hello"), "hello")

    def test_nested_dict(self):
        self.assertEqual(force_string({"key": [1, 2]}), {"key": [1, 2]})


class TestKwargsToList(TestCase):
    def test_basic_conversion(self):
        self.assertEqual(kwargs_to_list({"a": 1}), ["a-1"])

    def test_sorted_by_key(self):
        result = kwargs_to_list({"z": "last", "a": "first"})
        self.assertEqual(result, ["a-first", "z-last"])

    def test_unsorted_input_produces_sorted_output(self):
        result = kwargs_to_list({"b": 2, "a": 1})
        self.assertEqual(result, ["a-1", "b-2"])

    def test_empty_dict(self):
        self.assertEqual(kwargs_to_list({}), [])


class TestTaskBucketSlugKey(TestCase):
    def test_no_restrict_returns_task_name_only(self):
        result = task_bucket_slug_key("my.task", {"self": None, "char_id": 99})
        self.assertEqual(result, "my.task")

    def test_with_single_restrict(self):
        result = task_bucket_slug_key(
            "my.task",
            {"self": None, "char_id": 99},
            restrict_to=["char_id"],
        )
        self.assertEqual(result, "my.task_char_id-99")

    def test_with_multiple_restrict_sorted(self):
        result = task_bucket_slug_key(
            "my.task",
            {"self": None, "corp_id": 7, "char_id": 99},
            restrict_to=["char_id", "corp_id"],
        )
        self.assertEqual(result, "my.task_char_id-99_corp_id-7")

    def test_restrict_none_excludes_all_kwargs(self):
        result = task_bucket_slug_key("my.task", {"self": None, "x": 1}, restrict_to=None)
        self.assertEqual(result, "my.task")


class TestLimitToRate(TestCase):
    def test_per_second(self):
        self.assertAlmostEqual(limit_to_rate("10/s"), 0.1)

    def test_per_minute(self):
        self.assertAlmostEqual(limit_to_rate("60/m"), 1.0)

    def test_100_per_15_minutes(self):
        self.assertAlmostEqual(limit_to_rate("100/15m"), 9.0)

    def test_1_per_10_seconds(self):
        self.assertAlmostEqual(limit_to_rate("1/10s"), 10.0)


class TestESIRateLimitBucket(TestCase):
    def test_init_attributes(self):
        bucket = ESIRateLimitBucket("my_bucket", 100, 60)
        self.assertEqual(bucket.slug, "my_bucket")
        self.assertEqual(bucket.limit, 100)
        self.assertEqual(bucket.window, 60)

    def test_str_contains_slug_limit_window(self):
        bucket = ESIRateLimitBucket("my_bucket", 100, 60)
        s = str(bucket)
        self.assertIn("my_bucket", s)
        self.assertIn("100", s)
        self.assertIn("60", s)


class TestESIRateLimiter(TestCase):
    def setUp(self):
        self.limiter = ESIRateLimiter()
        self.bucket = ESIRateLimitBucket("test_esi_bucket", 5, 30)
        cache.clear()

    def test_slug_to_key(self):
        self.assertEqual(self.limiter._slug_to_key("my_slug"), "esi:bucket:my_slug")

    def test_init_bucket_creates_when_missing(self):
        self.limiter.init_bucket(self.bucket)
        self.assertEqual(self.limiter.get_bucket(self.bucket), 5)

    def test_init_bucket_does_not_overwrite_existing(self):
        self.limiter.init_bucket(self.bucket)
        self.limiter.decr_bucket(self.bucket)
        self.limiter.init_bucket(self.bucket)
        self.assertEqual(self.limiter.get_bucket(self.bucket), 4)

    def test_get_bucket_returns_default_when_key_missing(self):
        # Default value is 1 when the key does not exist
        self.assertEqual(self.limiter.get_bucket(self.bucket), 1)

    def test_get_timeout_returns_0_when_capacity_remains(self):
        self.limiter.init_bucket(self.bucket)
        self.assertEqual(self.limiter.get_timeout(self.bucket), 0)

    def test_get_timeout_returns_positive_when_exhausted(self):
        self.limiter.set_bucket(self.bucket, 0)
        self.assertGreater(self.limiter.get_timeout(self.bucket), 0)

    def test_decr_bucket_reduces_value(self):
        self.limiter.init_bucket(self.bucket)
        self.limiter.decr_bucket(self.bucket)
        self.assertEqual(self.limiter.get_bucket(self.bucket), 4)

    def test_decr_bucket_by_delta(self):
        self.limiter.init_bucket(self.bucket)
        self.limiter.decr_bucket(self.bucket, delta=3)
        self.assertEqual(self.limiter.get_bucket(self.bucket), 2)

    def test_set_bucket_stores_value(self):
        self.limiter.set_bucket(self.bucket, 10)
        self.assertEqual(self.limiter.get_bucket(self.bucket), 10)

    def test_check_bucket_passes_when_capacity_available(self):
        self.limiter.init_bucket(self.bucket)
        self.limiter.check_bucket(self.bucket)  # should not raise

    def test_check_bucket_raises_when_exhausted(self):
        self.limiter.set_bucket(self.bucket, 0)
        with self.assertRaises(ESIBucketLimitException):
            self.limiter.check_bucket(self.bucket)

    def test_check_bucket_exception_carries_bucket_and_reset(self):
        self.limiter.set_bucket(self.bucket, 0)
        with self.assertRaises(ESIBucketLimitException) as ctx:
            self.limiter.check_bucket(self.bucket)
        self.assertEqual(ctx.exception.bucket, self.bucket)
        self.assertGreater(ctx.exception.reset, 0)

    def test_check_decr_bucket_decrements_on_success(self):
        self.limiter.init_bucket(self.bucket)
        self.limiter.check_decr_bucket(self.bucket)
        self.assertEqual(self.limiter.get_bucket(self.bucket), 4)

    def test_check_decr_bucket_raises_on_limit(self):
        self.limiter.set_bucket(self.bucket, 0)
        with self.assertRaises(ESIBucketLimitException):
            self.limiter.check_decr_bucket(self.bucket, raise_on_limit=True)

    def test_check_decr_bucket_sleeps_when_raise_disabled(self):
        self.limiter.set_bucket(self.bucket, 0)
        with patch("esi.rate_limiting.time.sleep") as mock_sleep:
            self.limiter.check_decr_bucket(self.bucket, raise_on_limit=False)
        mock_sleep.assert_called_once()


class TestTaskRateLimitBucket(TestCase):
    def test_init_attributes(self):
        bucket = TaskRateLimitBucket("test_slug", 10, 60)
        self.assertEqual(bucket.slug, "test_slug")
        self.assertEqual(bucket.limit, 10)
        self.assertEqual(bucket.window, 60)

    def test_ttl_is_window_divided_by_limit(self):
        bucket = TaskRateLimitBucket("test_slug", 10, 60)
        self.assertAlmostEqual(bucket.ttl, 6.0)

    def test_ttl_single_task_per_window(self):
        bucket = TaskRateLimitBucket("test_slug", 1, 10)
        self.assertAlmostEqual(bucket.ttl, 10.0)

    def test_from_rate_per_second(self):
        bucket = TaskRateLimitBucket.from_rate("my_task", "10/s")
        self.assertEqual(bucket.slug, "my_task")
        self.assertEqual(bucket.limit, 10)
        self.assertEqual(bucket.window, 1)
        self.assertAlmostEqual(bucket.ttl, 0.1)

    def test_from_rate_per_minute(self):
        bucket = TaskRateLimitBucket.from_rate("my_task", "60/m")
        self.assertEqual(bucket.limit, 60)
        self.assertEqual(bucket.window, 60)
        self.assertAlmostEqual(bucket.ttl, 1.0)

    def test_from_rate_multi_minute(self):
        bucket = TaskRateLimitBucket.from_rate("my_task", "100/15m")
        self.assertEqual(bucket.limit, 100)
        self.assertEqual(bucket.window, 900)
        self.assertAlmostEqual(bucket.ttl, 9.0)

    def test_str_contains_slug_limit_window(self):
        bucket = TaskRateLimitBucket("my_slug", 10, 60)
        s = str(bucket)
        self.assertIn("my_slug", s)
        self.assertIn("10", s)
        self.assertIn("60", s)


class TestTaskRateLimiter(TestCase):
    def setUp(self):
        self.limiter = TaskRateLimiter()
        self.bucket = TaskRateLimitBucket("test_task_bucket", 1, 10)
        cache.clear()

    def test_slug_to_key(self):
        self.assertEqual(self.limiter._slug_to_key("my_slug"), "task:bucket:my_slug")

    def test_slug_to_lock(self):
        self.assertEqual(self.limiter._slug_to_lock("my_slug"), "lock:bucket:my_slug")

    def test_get_bucket_returns_nonpositive_when_key_missing(self):
        result = self.limiter.get_bucket(self.bucket)
        self.assertLessEqual(result, 0)

    def test_set_bucket_stores_key_with_ttl(self):
        self.limiter.set_bucket(self.bucket)
        self.assertGreater(self.limiter.get_bucket(self.bucket), 0)

    def test_check_bucket_passes_on_first_call(self):
        self.limiter.check_bucket(self.bucket)  # should not raise

    def test_check_bucket_raises_on_second_immediate_call(self):
        self.limiter.check_bucket(self.bucket)
        with self.assertRaises(TaskBucketLimitException):
            self.limiter.check_bucket(self.bucket)

    def test_check_bucket_exception_carries_bucket_and_reset(self):
        self.limiter.check_bucket(self.bucket)
        with self.assertRaises(TaskBucketLimitException) as ctx:
            self.limiter.check_bucket(self.bucket)
        self.assertEqual(ctx.exception.bucket, self.bucket)
        self.assertGreater(ctx.exception.reset, 0)

    def test_check_bucket_silently_passes_on_lock_not_owned(self):
        class _ExpiredLock:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                raise LockNotOwnedError()

        with patch.object(cache, "lock", return_value=_ExpiredLock()):
            self.limiter.check_bucket(self.bucket)  # should not raise


class TestRateLimitedTaskDecorator(TestCase):
    def setUp(self):
        cache.clear()

    def _make_task(self, name="test.rate_limited_task", retries=0):
        task = MagicMock(spec=Task)
        task.name = name
        task.request.retries = retries
        task.retry.side_effect = Retry()
        return task

    def test_executes_normally_when_not_rate_limited(self):
        mock_task = self._make_task()

        @rate_limited_task(rate="10/s")
        def my_func(self):
            return "done"

        self.assertEqual(my_func(mock_task), "done")

    def test_raises_retry_when_rate_limited(self):
        mock_task = self._make_task()

        @rate_limited_task(rate="1/10s")
        def my_func(self):
            return "done"

        my_func(mock_task)
        with self.assertRaises(Retry):
            my_func(mock_task)

    def test_retry_called_with_countdown(self):
        mock_task = self._make_task()

        @rate_limited_task(rate="1/10s")
        def my_func(self):
            return "done"

        my_func(mock_task)
        try:
            my_func(mock_task)
        except Retry:
            pass

        mock_task.retry.assert_called_once()
        _, call_kwargs = mock_task.retry.call_args
        self.assertIn("countdown", call_kwargs)
        self.assertGreater(call_kwargs["countdown"], 0)

    def test_retry_count_decremented_before_retry(self):
        """Decrement retries before calling retry() to avoid hitting max_retries."""
        mock_task = self._make_task(retries=3)

        @rate_limited_task(rate="1/10s")
        def my_func(self):
            return "done"

        my_func(mock_task)
        try:
            my_func(mock_task)
        except Retry:
            pass

        self.assertEqual(mock_task.request.retries, 2)

    def test_different_task_names_have_independent_buckets(self):
        task_a = self._make_task(name="task.a")
        task_b = self._make_task(name="task.b")

        @rate_limited_task(rate="1/10s")
        def my_func(self):
            return "done"

        my_func(task_a)
        # task_b has a different bucket key so should not be rate limited
        self.assertEqual(my_func(task_b), "done")

    def test_keys_param_scopes_bucket_to_specific_kwargs(self):
        """Tasks sharing a restricted key value share the same rate limit bucket."""
        mock_task = self._make_task()

        @rate_limited_task(rate="1/10s", keys=["corp_id"])
        def my_func(self, corp_id, char_id):
            return "done"

        my_func(mock_task, corp_id=1, char_id=10)
        # Same corp_id, different char_id → same bucket → rate limited
        with self.assertRaises(Retry):
            my_func(mock_task, corp_id=1, char_id=20)

    def test_different_key_values_have_independent_buckets(self):
        """Different values for the restricted key produce separate buckets."""
        mock_task = self._make_task()

        @rate_limited_task(rate="1/10s", keys=["corp_id"])
        def my_func(self, corp_id):
            return "done"

        my_func(mock_task, corp_id=1)
        # Different corp_id → separate bucket → not rate limited
        self.assertEqual(my_func(mock_task, corp_id=2), "done")
