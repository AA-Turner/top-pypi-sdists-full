import abc
from typing import Dict, Union

from .. import TokenBucket


class BucketStorage(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self.buckets: Dict = {}

    @abc.abstractmethod
    def get_bucket(
        self, identifier: str, bucket_key: str
    ) -> Union[TokenBucket, None]:  # pragma: no cover
        pass

    @abc.abstractmethod
    def get_all_buckets(
        self, identifier: str
    ) -> Union[Dict[str, TokenBucket], None]:  # pragma: no cover
        pass

    @abc.abstractmethod
    def add_bucket(self, bucket: TokenBucket) -> None:  # pragma: no cover
        pass

    @abc.abstractmethod
    def remove_bucket(
        self, identifier: str, bucket_key: str
    ) -> None:  # pragma: no cover
        pass

    @abc.abstractmethod
    def remove_all_buckets(self, identifier: str) -> None:  # pragma: no cover
        pass

    @abc.abstractmethod
    def replenish(self, bucket: TokenBucket) -> None:  # pragma: no cover
        pass

    @abc.abstractmethod
    def consume(self, identifier: str, bucket_key: str) -> bool:  # pragma: no cover
        pass
