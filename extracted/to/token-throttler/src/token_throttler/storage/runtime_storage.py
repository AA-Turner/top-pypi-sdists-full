from datetime import datetime, timezone
from typing import Dict, Union

from .. import TokenBucket
from . import BucketStorage


class RuntimeStorage(BucketStorage):
    def get_bucket(self, identifier: str, bucket_key: str) -> Union[TokenBucket, None]:
        return self.buckets.get(identifier, {}).get(bucket_key, None)

    def get_all_buckets(self, identifier: str) -> Union[Dict[str, TokenBucket], None]:
        return self.buckets.get(identifier, None)

    def add_bucket(self, bucket: TokenBucket) -> None:
        self.buckets[bucket.identifier][str(bucket.replenish_time)] = bucket

    def remove_bucket(self, identifier: str, bucket_key: str) -> None:
        if identifier not in self.buckets:
            return None
        bucket: Union[TokenBucket, None] = self.get_bucket(identifier, bucket_key)
        if bucket:
            del self.buckets[bucket.identifier][str(bucket.replenish_time)]
        if not self.buckets[identifier]:
            del self.buckets[identifier]

    def remove_all_buckets(self, identifier: str) -> None:
        if identifier not in self.buckets:
            return None
        del self.buckets[identifier]

    def replenish(self, bucket: TokenBucket):
        current_time: float = datetime.now(timezone.utc).timestamp()

        if (current_time < bucket.last_replenished) or (
            current_time - bucket.last_replenished < bucket.replenish_time
        ):
            return

        bucket.replenish()

    def consume(self, identifier: str, bucket_key: str) -> bool:
        bucket: TokenBucket = self.buckets[identifier][str(bucket_key)]
        self.replenish(bucket)
        return bucket.consume()
