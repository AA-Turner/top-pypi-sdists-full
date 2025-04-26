from asyncio import Lock
from typing import Any, Callable, Dict, List, Union

from . import (
    ThrottlerConfig,
    ThrottlerConfigGlobal,
    TokenBucket,
    TokenThrottlerException,
    default_config,
)
from .storage import BucketStorageAsync
from .validate import (
    validate_bucket,
    validate_bucket_config,
    validate_bucket_key,
    validate_cost,
    validate_identifier,
    validate_storage,
)


class TokenThrottlerAsync:
    def __init__(
        self,
        cost: int,
        storage: BucketStorageAsync,
        config: Union[ThrottlerConfig, ThrottlerConfigGlobal] = default_config,
    ) -> None:
        self._cost: int = cost
        self._storage: BucketStorageAsync = storage
        self._lock: Lock = Lock()
        self._config: Union[ThrottlerConfig, ThrottlerConfigGlobal] = config
        validate_cost(self._cost)
        validate_storage(self._storage, BucketStorageAsync)

    async def wait_time(self, identifier: str) -> int:
        buckets: Union[Dict[str, TokenBucket], None] = await self.get_all_buckets(
            identifier
        )
        if not buckets:
            return 0
        return max([b.wait_time for b in buckets.values() if b.wait_time > 0])

    def _add_identifier(self, identifier: str) -> None:
        validate_identifier(identifier)
        if identifier not in self._storage.buckets:
            self._storage.buckets[identifier] = {}

    async def get_bucket(
        self, identifier: str, bucket_key: str
    ) -> Union[TokenBucket, None]:
        validate_identifier(identifier)
        validate_bucket_key(bucket_key)
        return await self._storage.get_bucket(identifier, bucket_key)

    async def get_all_buckets(
        self, identifier: str
    ) -> Union[Dict[str, TokenBucket], None]:
        validate_identifier(identifier)
        return await self._storage.get_all_buckets(identifier)

    async def add_bucket(self, identifier: str, bucket: TokenBucket) -> None:
        validate_bucket(bucket, TokenBucket)
        self._add_identifier(identifier)
        bucket.identifier = identifier
        bucket.cost = self._cost
        await self._storage.add_bucket(bucket)

    async def remove_bucket(self, identifier: str, bucket_key: str) -> None:
        validate_identifier(identifier)
        validate_bucket_key(bucket_key)
        await self._storage.remove_bucket(identifier, bucket_key)

    async def remove_all_buckets(self, identifier: str) -> None:
        validate_identifier(identifier)
        await self._storage.remove_all_buckets(identifier)

    async def add_from_dict(
        self,
        identifier: str,
        bucket_config: List[Dict[str, Any]],
        remove_old_buckets: bool = False,
    ) -> None:
        validate_bucket_config(bucket_config, TokenBucket)
        self._add_identifier(identifier)

        if remove_old_buckets:
            await self.remove_all_buckets(identifier)

        for bucket in bucket_config:
            token_bucket: TokenBucket = TokenBucket(
                replenish_time=int(bucket["replenish_time"]),
                max_tokens=int(bucket["max_tokens"]),
            )
            await self.add_bucket(identifier, token_bucket)

    async def consume(self, identifier: str) -> bool:
        return_value: bool = True
        validate_identifier(identifier)
        if identifier not in self._storage.buckets.keys():
            if not self._config.IDENTIFIER_FAIL_SAFE:
                raise KeyError(f"Invalid identifier: `{identifier}`")
            else:
                return return_value

        if self._config.ENABLE_THREAD_LOCK:
            await self._lock.acquire()

        for bucket_key in self._storage.buckets[identifier].keys():
            if not await self._storage.consume(identifier, str(bucket_key)):
                return_value = False

        if self._lock.locked():
            self._lock.release()

        return return_value

    def enable(self, identifier: str) -> Any:
        def wrapper(fn: Callable):
            async def inner(*args, **kwargs):
                if not await self.consume(identifier):
                    raise TokenThrottlerException()
                return await fn(*args, **kwargs)

            return inner

        return wrapper
