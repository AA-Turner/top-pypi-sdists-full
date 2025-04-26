import pickle
from datetime import timedelta
from typing import Dict, List, Union

from redis.asyncio import Redis

from ... import TokenBucket
from .. import BucketStorageAsync


class RedisStorageAsync(BucketStorageAsync):
    def __init__(self, redis: Redis, delimiter: str) -> None:
        super().__init__()
        self.redis: Redis = redis
        self.delimiter: str = delimiter

    def _create_bucket(self, cache_key: str) -> TokenBucket:
        bucket_info: List[str] = cache_key.split(self.delimiter)
        token_bucket: TokenBucket = TokenBucket(
            int(bucket_info[1]), int(bucket_info[-1])
        )
        token_bucket.cost = int(bucket_info[2])
        token_bucket.identifier = bucket_info[0]
        return token_bucket

    async def _delete_bucket(self, cache_key: str) -> None:
        await self.redis.delete(cache_key)

    async def _save_bucket(self, cache_key: str, bucket: TokenBucket) -> None:
        await self.redis.setex(
            cache_key,
            timedelta(seconds=bucket.replenish_time),
            pickle.dumps(bucket),
        )

    async def get_bucket(
        self, identifier: str, bucket_key: str
    ) -> Union[TokenBucket, None]:
        cache_key: Union[str, None] = self.buckets.get(identifier, {}).get(
            bucket_key, None
        )
        if not cache_key:
            return None
        bucket: Union[bytes, None] = await self.redis.get(cache_key)
        if not bucket:
            return None
        return pickle.loads(bucket)

    async def get_all_buckets(
        self, identifier: str
    ) -> Union[Dict[str, TokenBucket], None]:
        buckets: Dict[str, TokenBucket] = {}
        stored_buckets: Union[Dict[str, str], None] = self.buckets.get(identifier, None)
        if not stored_buckets:
            return None
        for bucket_key in stored_buckets:
            bucket: Union[TokenBucket, None] = await self.get_bucket(
                identifier, bucket_key
            )
            if not bucket:  # pragma: no cover
                continue
            buckets[bucket_key] = bucket
        return None if not buckets else buckets

    async def add_bucket(self, bucket: TokenBucket) -> None:
        cache_key: str = f"{self.delimiter}".join(
            map(
                str,
                [
                    bucket.identifier,
                    bucket.replenish_time,
                    bucket.cost,
                    bucket.max_tokens,
                ],
            )
        )
        self.buckets[str(bucket.identifier)][str(bucket.replenish_time)] = cache_key
        await self._save_bucket(cache_key, bucket)

    async def remove_bucket(self, identifier: str, bucket_key: str) -> None:
        if identifier not in self.buckets:
            return None
        bucket: Union[str, None] = self.buckets.get(identifier, {}).get(
            bucket_key, None
        )
        if bucket:
            await self._delete_bucket(self.buckets[identifier][bucket_key])
            del self.buckets[identifier][bucket_key]
        if not self.buckets[identifier]:
            del self.buckets[identifier]

    async def remove_all_buckets(self, identifier: str) -> None:
        if identifier not in self.buckets:
            return None
        for bucket_key in self.buckets[identifier]:
            await self._delete_bucket(self.buckets[identifier][bucket_key])
        del self.buckets[identifier]

    async def replenish(self, bucket: TokenBucket) -> None:
        pass  # pragma: no cover

    async def consume(self, identifier: str, bucket_key: str) -> bool:
        cache_key: str = self.buckets[identifier][bucket_key]
        bucket: Union[TokenBucket, None] = await self.get_bucket(identifier, bucket_key)
        if not bucket:
            bucket = self._create_bucket(cache_key)
            await self.add_bucket(bucket)
        bucket_state: bool = bucket.consume()
        if bucket_state:
            await self._save_bucket(cache_key, bucket)
        return bucket_state
