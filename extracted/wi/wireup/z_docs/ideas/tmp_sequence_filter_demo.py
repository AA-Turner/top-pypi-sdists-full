from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, TypeVar

import wireup
from wireup import SyncContainer, injectable

T = TypeVar("T")


class Cache(Protocol):
    def source(self) -> str: ...


@injectable(as_type=Cache)
class MemoryCache:
    def source(self) -> str:
        return "memory"


@injectable(as_type=Cache, qualifier="redis")
class RedisCache:
    def source(self) -> str:
        return "redis"


class Notifier(Protocol):
    def channel(self) -> str: ...


@injectable(as_type=Notifier)
class EmailNotifier:
    def channel(self) -> str:
        return "email"


@injectable(as_type=Notifier, qualifier="sms")
class SmsNotifier:
    def channel(self) -> str:
        return "sms"


def make_filtered_sequence_factory(interface: type[T]):
    @injectable(as_type=list[interface])  # type: ignore[valid-type]
    def filtered_sequence(container: SyncContainer) -> list[T]:
        default_cache = container.get(interface)
        caches = container.get(Sequence[interface])  # type: ignore[valid-type]
        return [cache for cache in caches if cache is not default_cache]

    return filtered_sequence


def main() -> None:
    filtered_cache_list = make_filtered_sequence_factory(Cache)
    filtered_notifier_list = make_filtered_sequence_factory(Notifier)
    container = wireup.create_sync_container(
        injectables=[
            MemoryCache,
            RedisCache,
            EmailNotifier,
            SmsNotifier,
            filtered_cache_list,
            filtered_notifier_list,
        ]
    )

    all_caches = container.get(Sequence[Cache])
    filtered = container.get(list[Cache])
    all_notifiers = container.get(Sequence[Notifier])
    filtered_notifiers = container.get(list[Notifier])

    print("all:", [cache.source() for cache in all_caches])
    print("filtered:", [cache.source() for cache in filtered])
    print("notifiers all:", [notifier.channel() for notifier in all_notifiers])
    print("notifiers filtered:", [notifier.channel() for notifier in filtered_notifiers])


if __name__ == "__main__":
    main()
