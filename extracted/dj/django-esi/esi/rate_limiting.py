import logging
import time

from django.core.cache import cache

from esi.exceptions import ESIBucketLimitException, TaskBucketLimitException
from redis.exceptions import LockNotOwnedError

logger = logging.getLogger(__name__)

seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400}


def interval_to_seconds(s) -> int:
    if len(s) == 1:
        return seconds_per_unit[s[-1]]
    else:
        return int(s[:-1]) * seconds_per_unit[s[-1]]


def force_string(kwargs):
    if isinstance(kwargs, dict):
        return {
            force_string(key): force_string(value) for key, value in kwargs.items()
        }
    elif isinstance(kwargs, list):
        return [force_string(element) for element in kwargs]
    return kwargs


def kwargs_to_list(kwargs):
    """
    Turns {'a': 1, 'b': 2} into ["a-1", "b-2"]
    """
    kwargs_list = []
    for k, v in sorted(kwargs.items(), key=lambda kv: str(kv[0])):
        kwargs_list.append(str(k) + '-' + str(force_string(v)))
    return kwargs_list


def task_bucket_slug_key(task, kwargs, restrict_to=None):
    """
    Turns a list the name of the task, the kwargs and allowed keys
    into a redis key.
    """
    keys: list[str] = [str(task)]
    if restrict_to is not None:
        restrict_kwargs = {key: kwargs[key] for key in restrict_to}
        keys += kwargs_to_list(restrict_kwargs)
    key = "_".join(keys)
    return key


def limit_to_rate(rate_limit):
    """convert things like 100/15m or 10/s to a delay in seconds"""
    lim = rate_limit.split("/")
    secs = interval_to_seconds(lim[1])
    return secs/int(lim[0])


class ESIRateLimitBucket:
    MARKET_DATA_HISTORY = ("market_data_history", 300, 60)
    CHARACTER_CORPORATION_HISTORY = ("character_corporation_history", 300, 60)

    def __init__(self, slug, limit, window):
        self.slug = slug
        self.limit = limit
        self.window = window

    @classmethod
    def choices(cls):
        return [(bucket.slug, bucket.slug.replace("_", " ").title()) for bucket in cls]

    def __str__(self):
        return f"Rate Limit: {self.slug} - {self.limit} in {self.window}Seconds"


class ESIRateLimiter:
    def __init__(self) -> None:
        pass

    def _slug_to_key(self, slug) -> str:
        return f"esi:bucket:{slug}"

    def init_bucket(self, bucket: ESIRateLimitBucket) -> None:
        # Set our bucket up if it doesn't already exist
        cache.set(
            self._slug_to_key(bucket.slug),
            bucket.limit,
            timeout=bucket.window,
            nx=True  # Don't re-create if it does exist
        )

    def get_bucket(self, bucket: ESIRateLimitBucket) -> int:
        # get the value from the bucket
        return int(
            cache.get(
                self._slug_to_key(bucket.slug),
                1  # When not found return 1
            )
        )

    def get_timeout(self, bucket: ESIRateLimitBucket) -> int:
        current_bucket = self.get_bucket(bucket)
        if current_bucket <= 0:
            timeout = cache.ttl(self._slug_to_key(bucket.slug)) + 1
            msg = (
                f"Rate limit for bucket '{bucket.slug}' exceeded: "
                f"{current_bucket}/{bucket.limit} in last {bucket.window}s. "
                f"Wait {timeout}s."
            )
            logger.warning(msg)
            return timeout  # return the time left till reset
        else:
            return 0  # we are good.

    def decr_bucket(self, bucket: ESIRateLimitBucket, delta: int = 1) -> int:
        # decrease the bucket value by <delta> from the bucket
        return cache.decr(
            self._slug_to_key(bucket.slug),
            delta
        )

    def set_bucket(self, bucket: ESIRateLimitBucket, new_limit: int = 1) -> int:
        # decrease the bucket value by <delta> from the bucket
        return cache.set(
            self._slug_to_key(bucket.slug),
            int(new_limit),
            timeout=bucket.window
        )

    def check_bucket(self, bucket: ESIRateLimitBucket) -> None:
        self.init_bucket(bucket)
        # get the value
        bucket_val = self.get_bucket(bucket)
        if bucket_val <= 0:
            timeout = self.get_timeout(bucket)
            if timeout > 0:
                raise ESIBucketLimitException(bucket, timeout)
            return

    def check_decr_bucket(self, bucket: ESIRateLimitBucket, raise_on_limit: bool = True) -> None:
        try:
            self.check_bucket(bucket)
            self.decr_bucket(bucket)
        except ESIBucketLimitException as ex:
            if raise_on_limit:
                raise ex
            else:
                time.sleep(ex.reset)


class TaskRateLimitBucket:
    def __init__(self, slug, limit, window):
        self.slug = slug
        self.limit = limit
        self.window = window
        self.ttl = window/limit

    @classmethod
    def from_rate(cls, slug, rate_string):
        limit, window = rate_string.split("/")
        window_seconds = interval_to_seconds(window)
        return cls(slug, int(limit), window_seconds)

    def __str__(self):
        return f"Rate Limit: {self.slug} - {self.limit} in {self.window}Seconds"


class TaskRateLimiter:
    def _slug_to_key(self, slug) -> str:
        return f"task:bucket:{slug}"

    def _slug_to_lock(self, slug) -> str:
        return f"lock:bucket:{slug}"

    def get_bucket(self, bucket: TaskRateLimitBucket) -> int:
        return cache.ttl(
            self._slug_to_key(bucket.slug)
        )

    def set_bucket(self, bucket: TaskRateLimitBucket) -> None:
        cache.set(
            self._slug_to_key(bucket.slug),
            bucket.slug,
            timeout=bucket.ttl
        )

    def check_bucket(self, bucket: TaskRateLimitBucket) -> None:
        try:
            with cache.lock(self._slug_to_lock(bucket.slug), timeout=bucket.ttl):
                # Use a lock to prevent dupes from multiple workers
                # worst case we go a bit slower
                timeout = self.get_bucket(bucket)
                if timeout > 0:
                    raise TaskBucketLimitException(bucket, timeout)
                self.set_bucket(bucket)
        except LockNotOwnedError:
            # took longer than lock time this is fine.
            pass
        return


TaskRateLimits = TaskRateLimiter()
ESIRateLimits = ESIRateLimiter()
