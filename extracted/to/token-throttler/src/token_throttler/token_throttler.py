import asyncio
from threading import Lock
from typing import Any, Callable, Dict, List, Union

from . import (
    ThrottlerConfig,
    ThrottlerConfigGlobal,
    TokenBucket,
    TokenThrottlerException,
    default_config,
)
from .storage import BucketStorage
from .validate import (
    validate_bucket,
    validate_bucket_config,
    validate_bucket_key,
    validate_cost,
    validate_identifier,
    validate_storage,
)


class TokenThrottler:
    def __init__(
        self,
        cost: int,
        storage: BucketStorage,
        config: Union[ThrottlerConfig, ThrottlerConfigGlobal] = default_config,
    ) -> None:
        self._cost: int = cost
        self._storage: BucketStorage = storage
        self._lock: Lock = Lock()
        self._config: Union[ThrottlerConfig, ThrottlerConfigGlobal] = config
        validate_cost(self._cost)
        validate_storage(self._storage, BucketStorage)

    def wait_time(self, identifier: str) -> int:
        buckets: Union[Dict[str, TokenBucket], None] = self.get_all_buckets(identifier)
        if not buckets:
            return 0
        wait_times: list = [b.wait_time for b in buckets.values() if b.wait_time > 0]
        return max(wait_times) if wait_times else 0

    def _add_identifier(self, identifier: str) -> None:
        validate_identifier(identifier)
        if identifier not in self._storage.buckets:
            self._storage.buckets[identifier] = {}

    def get_bucket(self, identifier: str, bucket_key: str) -> Union[TokenBucket, None]:
        validate_identifier(identifier)
        validate_bucket_key(bucket_key)
        return self._storage.get_bucket(identifier, bucket_key)

    def get_all_buckets(self, identifier: str) -> Union[Dict[str, TokenBucket], None]:
        validate_identifier(identifier)
        return self._storage.get_all_buckets(identifier)

    def add_bucket(self, identifier: str, bucket: TokenBucket) -> None:
        validate_bucket(bucket, TokenBucket)
        self._add_identifier(identifier)
        bucket.identifier = identifier
        bucket.cost = self._cost
        self._storage.add_bucket(bucket)

    def remove_bucket(self, identifier: str, bucket_key: str) -> None:
        validate_identifier(identifier)
        validate_bucket_key(bucket_key)
        self._storage.remove_bucket(identifier, bucket_key)

    def remove_all_buckets(self, identifier: str) -> None:
        validate_identifier(identifier)
        self._storage.remove_all_buckets(identifier)

    def add_from_dict(
        self,
        identifier: str,
        bucket_config: List[Dict[str, Any]],
        remove_old_buckets: bool = False,
    ) -> None:
        validate_bucket_config(bucket_config, TokenBucket)
        self._add_identifier(identifier)

        if remove_old_buckets:
            self.remove_all_buckets(identifier)

        for bucket in bucket_config:
            token_bucket: TokenBucket = TokenBucket(
                replenish_time=int(bucket["replenish_time"]),
                max_tokens=int(bucket["max_tokens"]),
            )
            self.add_bucket(identifier, token_bucket)

    def consume(self, identifier: str) -> bool:
        return_value: bool = True
        validate_identifier(identifier)
        if identifier not in self._storage.buckets.keys():
            if not self._config.IDENTIFIER_FAIL_SAFE:
                raise KeyError(f"Invalid identifier: `{identifier}`")
            else:
                return return_value

        if self._config.ENABLE_THREAD_LOCK:
            self._lock.acquire()

        if not all(
            self._storage.consume(identifier, str(bucket_key))
            for bucket_key in self._storage.buckets[identifier].keys()
        ):
            return_value = False

        if self._lock.locked():
            self._lock.release()

        return return_value

    def enable(self, identifier: str) -> Any:
        def wrapper(fn: Callable):
            if not asyncio.iscoroutinefunction(fn):

                def inner(*args, **kwargs):
                    if not self.consume(identifier):
                        raise TokenThrottlerException()
                    return fn(*args, **kwargs)

                return inner
            else:

                async def inner(*args, **kwargs):
                    if not self.consume(identifier):
                        raise TokenThrottlerException()
                    return await fn(*args, **kwargs)

                return inner

        return wrapper
