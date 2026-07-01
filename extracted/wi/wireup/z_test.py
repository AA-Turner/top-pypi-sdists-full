from collections.abc import Sequence
from dataclasses import dataclass

import wireup
from wireup._annotations import injectable


@dataclass
class Cache:
    source: str


@injectable(qualifier="redis")
def make_cache() -> Cache:
    return Cache(source="redis")


@injectable
def make_cache_default() -> Cache:
    return Cache(source="default")


type Cache2 = Cache


@wireup.injectable
class AllCaches:
    def __init__(self, caches: Sequence[Cache]) -> None:
        self.caches = caches


container = wireup.create_sync_container(injectables=[make_cache, make_cache_default, AllCaches])

with container.override.injectable(Sequence[Cache], new=[]):
    print(container.get(AllCaches).caches)
print(container.get(AllCaches).caches)
