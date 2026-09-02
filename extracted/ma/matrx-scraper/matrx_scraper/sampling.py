from __future__ import annotations

import hashlib
import heapq
from collections.abc import Callable, Iterable
from typing import Generic, TypeVar

T = TypeVar("T")


class StableHashSampler(Generic[T]):
    """Keep a deterministic, order-independent bounded sample of a stream."""

    def __init__(
        self,
        limit: int,
        *,
        key: Callable[[T], str],
        namespace: str = "matrx-scraper",
    ) -> None:
        if limit < 1:
            raise ValueError("limit must be at least 1")
        self._limit = limit
        self._key = key
        self._namespace = namespace.encode("utf-8")
        self._heap: list[tuple[int, str, T]] = []
        self._retained_keys: set[str] = set()

    def offer(self, item: T) -> None:
        item_key = self._key(item)
        if item_key in self._retained_keys:
            return
        score = self._score(item_key)
        entry = (-score, item_key, item)
        if len(self._heap) < self._limit:
            heapq.heappush(self._heap, entry)
            self._retained_keys.add(item_key)
            return
        worst_score = -self._heap[0][0]
        worst_key = self._heap[0][1]
        if (score, item_key) >= (worst_score, worst_key):
            return
        removed = heapq.heapreplace(self._heap, entry)
        self._retained_keys.remove(removed[1])
        self._retained_keys.add(item_key)

    def extend(self, items: Iterable[T]) -> None:
        for item in items:
            self.offer(item)

    def items(self) -> list[T]:
        """Return retained items in stable hash order."""

        return [entry[2] for entry in sorted(self._heap, key=lambda row: (-row[0], row[1]))]

    def _score(self, item_key: str) -> int:
        digest = hashlib.blake2b(
            item_key.encode("utf-8"),
            digest_size=8,
            key=self._namespace[:64],
        ).digest()
        return int.from_bytes(digest, "big")


def stable_hash_sample(
    items: Iterable[T],
    limit: int,
    *,
    key: Callable[[T], str],
    namespace: str = "matrx-scraper",
) -> list[T]:
    """Return the same bounded sample regardless of input ordering."""

    sampler = StableHashSampler(limit, key=key, namespace=namespace)
    sampler.extend(items)
    return sampler.items()


__all__ = ["StableHashSampler", "stable_hash_sample"]
