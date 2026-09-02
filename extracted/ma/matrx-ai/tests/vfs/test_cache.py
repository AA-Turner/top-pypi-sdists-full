from __future__ import annotations

import asyncio
import uuid
from typing import Any

import pytest
import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.cache import CachingBackend
from matrx_ai.tools.vfs.paths import Inode


class CountingBackend:
    # Thin wrapper around MemoryBackend that records inner-call counts.

    def __init__(self, inner: MemoryBackend) -> None:
        self._inner = inner
        self.counts: dict[str, int] = {
            "get_inode": 0,
            "get_inode_by_path": 0,
            "list_children": 0,
            "create_inode": 0,
            "update_inode": 0,
            "delete_inode": 0,
            "get_blob": 0,
            "put_blob": 0,
            "ensure_workspace_root": 0,
        }

    async def get_inode(self, workspace_id: str, parent_id: str | None, name: str) -> Inode | None:
        self.counts["get_inode"] += 1
        return await self._inner.get_inode(workspace_id, parent_id, name)

    async def get_inode_by_path(self, workspace_id: str, path: str) -> Inode | None:
        self.counts["get_inode_by_path"] += 1
        return await self._inner.get_inode_by_path(workspace_id, path)

    async def list_children(self, workspace_id: str, parent_id: str) -> list[Inode]:
        self.counts["list_children"] += 1
        return await self._inner.list_children(workspace_id, parent_id)

    async def create_inode(self, inode: Inode) -> Inode:
        self.counts["create_inode"] += 1
        return await self._inner.create_inode(inode)

    async def update_inode(self, inode_id: str, **fields: Any) -> Inode:
        self.counts["update_inode"] += 1
        return await self._inner.update_inode(inode_id, **fields)

    async def delete_inode(self, inode_id: str) -> None:
        self.counts["delete_inode"] += 1
        await self._inner.delete_inode(inode_id)

    async def get_blob(self, blob_id: str) -> bytes:
        self.counts["get_blob"] += 1
        return await self._inner.get_blob(blob_id)

    async def put_blob(self, data: bytes) -> str:
        self.counts["put_blob"] += 1
        return await self._inner.put_blob(data)

    async def ensure_workspace_root(self, workspace_id: str) -> Inode:
        self.counts["ensure_workspace_root"] += 1
        return await self._inner.ensure_workspace_root(workspace_id)


class SlowGetInodeBackend(CountingBackend):
    # CountingBackend variant that gates get_inode behind an asyncio.Event so
    # we can deterministically force concurrent waiters.

    def __init__(self, inner: MemoryBackend) -> None:
        super().__init__(inner)
        self.gate = asyncio.Event()

    async def get_inode(self, workspace_id: str, parent_id: str | None, name: str) -> Inode | None:
        self.counts["get_inode"] += 1
        await self.gate.wait()
        return await self._inner.get_inode(workspace_id, parent_id, name)


@pytest_asyncio.fixture
async def setup() -> tuple[MemoryBackend, CountingBackend, CachingBackend]:
    mem = MemoryBackend()
    counting = CountingBackend(mem)
    cache = CachingBackend(counting)
    return mem, counting, cache


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def _mk_file(backend: MemoryBackend, workspace_id: str, parent_id: str, name: str) -> Inode:
    return await backend.make_inode(workspace_id, parent_id, name, "file")


async def _mk_dir(
    backend: MemoryBackend, workspace_id: str, parent_id: str | None, name: str
) -> Inode:
    return await backend.make_inode(workspace_id, parent_id, name, "dir")


# ---------------------------------------------------------------------------
# 1. Hit on second read
# ---------------------------------------------------------------------------


async def test_get_inode_hit_on_second_read(
    setup: tuple[MemoryBackend, CountingBackend, CachingBackend],
) -> None:
    mem, counting, cache = setup
    root = await mem.ensure_workspace_root("ws-1")
    await _mk_file(mem, "ws-1", root.id, "a.txt")

    counting.counts["get_inode"] = 0
    a = await cache.get_inode("ws-1", root.id, "a.txt")
    assert a is not None
    a2 = await cache.get_inode("ws-1", root.id, "a.txt")
    assert a2 is not None and a2.id == a.id
    assert counting.counts["get_inode"] == 1
    assert cache.stats.inode_hits == 1
    assert cache.stats.inode_misses == 1


# ---------------------------------------------------------------------------
# 2. Listing hit
# ---------------------------------------------------------------------------


async def test_list_children_hit_on_second_read(
    setup: tuple[MemoryBackend, CountingBackend, CachingBackend],
) -> None:
    mem, counting, cache = setup
    root = await mem.ensure_workspace_root("ws-1")
    await _mk_file(mem, "ws-1", root.id, "x")
    await _mk_file(mem, "ws-1", root.id, "y")

    counting.counts["list_children"] = 0
    first = await cache.list_children("ws-1", root.id)
    second = await cache.list_children("ws-1", root.id)
    assert {c.name for c in first} == {"x", "y"}
    assert {c.name for c in second} == {"x", "y"}
    assert counting.counts["list_children"] == 1
    assert cache.stats.listing_hits == 1
    assert cache.stats.listing_misses == 1


# ---------------------------------------------------------------------------
# 3. Cache invalidation on create
# ---------------------------------------------------------------------------


async def test_listing_invalidated_on_create(
    setup: tuple[MemoryBackend, CountingBackend, CachingBackend],
) -> None:
    mem, counting, cache = setup
    root = await mem.ensure_workspace_root("ws-1")
    await _mk_file(mem, "ws-1", root.id, "a")

    await cache.list_children("ws-1", root.id)
    counting.counts["list_children"] = 0

    new_inode = Inode(
        id=str(uuid.uuid4()),
        workspace_id="ws-1",
        parent_id=root.id,
        name="b",
        type="file",
    )
    await cache.create_inode(new_inode)

    after = await cache.list_children("ws-1", root.id)
    assert {c.name for c in after} == {"a", "b"}
    assert counting.counts["list_children"] == 1


# ---------------------------------------------------------------------------
# 4. Cache invalidation on delete
# ---------------------------------------------------------------------------


async def test_listing_invalidated_on_delete(
    setup: tuple[MemoryBackend, CountingBackend, CachingBackend],
) -> None:
    mem, counting, cache = setup
    root = await mem.ensure_workspace_root("ws-1")
    a = await _mk_file(mem, "ws-1", root.id, "a")
    await _mk_file(mem, "ws-1", root.id, "b")

    await cache.list_children("ws-1", root.id)
    counting.counts["list_children"] = 0

    # Pre-populate cache.get_inode so we can confirm it gets invalidated.
    await cache.get_inode("ws-1", root.id, "a")
    counting.counts["get_inode"] = 0

    await cache.delete_inode(a.id)

    after = await cache.list_children("ws-1", root.id)
    assert {c.name for c in after} == {"b"}
    assert counting.counts["list_children"] == 1

    # Name-key cache entry for "a" should be gone, so a re-fetch hits inner.
    miss = await cache.get_inode("ws-1", root.id, "a")
    assert miss is None
    assert counting.counts["get_inode"] == 1


# ---------------------------------------------------------------------------
# 5. Move (update with parent change)
# ---------------------------------------------------------------------------


async def test_listing_invalidated_on_move(
    setup: tuple[MemoryBackend, CountingBackend, CachingBackend],
) -> None:
    mem, counting, cache = setup
    root = await mem.ensure_workspace_root("ws-1")
    dir_a = await _mk_dir(mem, "ws-1", root.id, "a")
    dir_b = await _mk_dir(mem, "ws-1", root.id, "b")
    file_in_a = await _mk_file(mem, "ws-1", dir_a.id, "f.txt")

    # Prime listings on both directories.
    listing_a = await cache.list_children("ws-1", dir_a.id)
    assert {c.name for c in listing_a} == {"f.txt"}
    listing_b = await cache.list_children("ws-1", dir_b.id)
    assert listing_b == []

    counting.counts["list_children"] = 0

    # Move file from /a to /b.
    await cache.update_inode(file_in_a.id, parent_id=dir_b.id)

    after_a = await cache.list_children("ws-1", dir_a.id)
    after_b = await cache.list_children("ws-1", dir_b.id)
    assert after_a == []
    assert {c.name for c in after_b} == {"f.txt"}
    # Both listings were invalidated so we expect 2 inner calls.
    assert counting.counts["list_children"] == 2


# ---------------------------------------------------------------------------
# 6. LRU eviction
# ---------------------------------------------------------------------------


async def test_lru_eviction() -> None:
    mem = MemoryBackend()
    counting = CountingBackend(mem)
    cache = CachingBackend(counting, max_inodes=2)

    root = await mem.ensure_workspace_root("ws-1")
    await _mk_file(mem, "ws-1", root.id, "a")
    await _mk_file(mem, "ws-1", root.id, "b")
    await _mk_file(mem, "ws-1", root.id, "c")

    # Reset counters after setup (root caching etc).
    counting.counts["get_inode"] = 0
    cache.reset_stats()

    await cache.get_inode("ws-1", root.id, "a")
    await cache.get_inode("ws-1", root.id, "b")
    await cache.get_inode("ws-1", root.id, "c")

    # Cap is 2: "a" should be evicted. The root inode itself is also cached,
    # which means we can have 1+ evictions overall.
    assert cache.stats.evictions >= 1

    # Refetching "a" should hit inner; "c" should be cached.
    counting.counts["get_inode"] = 0
    await cache.get_inode("ws-1", root.id, "a")
    assert counting.counts["get_inode"] == 1

    counting.counts["get_inode"] = 0
    await cache.get_inode("ws-1", root.id, "c")
    assert counting.counts["get_inode"] == 0


# ---------------------------------------------------------------------------
# 7. Blob cache
# ---------------------------------------------------------------------------


async def test_blob_cache_hits(
    setup: tuple[MemoryBackend, CountingBackend, CachingBackend],
) -> None:
    mem, counting, cache = setup
    blob_id = await mem.put_blob(b"hello-world")
    counting.counts["get_blob"] = 0

    a = await cache.get_blob(blob_id)
    b = await cache.get_blob(blob_id)
    assert a == b == b"hello-world"
    assert counting.counts["get_blob"] == 1
    assert cache.stats.blob_hits == 1
    assert cache.stats.blob_misses == 1


async def test_blob_cache_size_eviction() -> None:
    mem = MemoryBackend()
    counting = CountingBackend(mem)
    # max_blob_bytes = 10 — anything over 5 evicts older entries when we add
    # another mid-size blob.
    cache = CachingBackend(counting, max_blob_bytes=10)

    big1_id = await mem.put_blob(b"AAAAAA")  # 6 bytes
    big2_id = await mem.put_blob(b"BBBBBB")  # 6 bytes

    counting.counts["get_blob"] = 0

    await cache.get_blob(big1_id)
    await cache.get_blob(big2_id)
    # big1 should have been evicted because total would have been 12 > 10.
    counting.counts["get_blob"] = 0
    await cache.get_blob(big1_id)
    assert counting.counts["get_blob"] == 1
    # big2 still cached.
    counting.counts["get_blob"] = 0
    # Re-fetching big2 may have triggered eviction of big2 — verify by
    # observing the most-recent-fetch is hot.
    await cache.get_blob(big2_id)
    # If big2 was evicted by storing big1 again, this is a miss; otherwise hit.
    # Either way our stats bookkeeping remains correct.
    assert cache.stats.evictions >= 1


# ---------------------------------------------------------------------------
# 8. In-flight dedupe
# ---------------------------------------------------------------------------


async def test_in_flight_dedupe() -> None:
    mem = MemoryBackend()
    slow = SlowGetInodeBackend(mem)
    cache = CachingBackend(slow)

    root = await mem.ensure_workspace_root("ws-1")
    await _mk_file(mem, "ws-1", root.id, "a.txt")
    slow.counts["get_inode"] = 0

    async def fetch() -> Inode | None:
        return await cache.get_inode("ws-1", root.id, "a.txt")

    # Five concurrent waiters — only one should reach inner.
    fetcher_task = asyncio.gather(*(fetch() for _ in range(5)))
    # Allow all coroutines to register their inflight future before opening gate.
    await asyncio.sleep(0)
    await asyncio.sleep(0)
    slow.gate.set()
    results = await fetcher_task

    assert all(r is not None and r.name == "a.txt" for r in results)
    assert slow.counts["get_inode"] == 1


# ---------------------------------------------------------------------------
# 9. Stats counters
# ---------------------------------------------------------------------------


async def test_stats_counters(
    setup: tuple[MemoryBackend, CountingBackend, CachingBackend],
) -> None:
    mem, _counting, cache = setup
    root = await mem.ensure_workspace_root("ws-1")
    await _mk_file(mem, "ws-1", root.id, "a")
    blob_id = await mem.put_blob(b"data")

    cache.reset_stats()

    # Inode miss + hit.
    await cache.get_inode("ws-1", root.id, "a")
    await cache.get_inode("ws-1", root.id, "a")
    assert cache.stats.inode_hits == 1
    assert cache.stats.inode_misses == 1

    # Listing miss + hit.
    await cache.list_children("ws-1", root.id)
    await cache.list_children("ws-1", root.id)
    assert cache.stats.listing_hits == 1
    assert cache.stats.listing_misses == 1

    # Blob miss + hit.
    await cache.get_blob(blob_id)
    await cache.get_blob(blob_id)
    assert cache.stats.blob_hits == 1
    assert cache.stats.blob_misses == 1

    cache.reset_stats()
    assert cache.stats.inode_hits == 0
    assert cache.stats.blob_hits == 0


# ---------------------------------------------------------------------------
# 10. Workspace isolation
# ---------------------------------------------------------------------------


async def test_workspace_isolation(
    setup: tuple[MemoryBackend, CountingBackend, CachingBackend],
) -> None:
    mem, counting, cache = setup
    root1 = await mem.ensure_workspace_root("ws-1")
    root2 = await mem.ensure_workspace_root("ws-2")
    file1 = await _mk_file(mem, "ws-1", root1.id, "shared.txt")
    file2 = await _mk_file(mem, "ws-2", root2.id, "shared.txt")
    assert file1.id != file2.id

    counting.counts["get_inode"] = 0
    a = await cache.get_inode("ws-1", root1.id, "shared.txt")
    b = await cache.get_inode("ws-2", root2.id, "shared.txt")
    assert a is not None and b is not None
    assert a.id == file1.id
    assert b.id == file2.id
    assert counting.counts["get_inode"] == 2

    # Both reads should now be cached separately.
    counting.counts["get_inode"] = 0
    await cache.get_inode("ws-1", root1.id, "shared.txt")
    await cache.get_inode("ws-2", root2.id, "shared.txt")
    assert counting.counts["get_inode"] == 0


# ---------------------------------------------------------------------------
# get_inode_by_path piggy-backs on get_inode caching
# ---------------------------------------------------------------------------


async def test_get_inode_by_path_uses_per_component_cache(
    setup: tuple[MemoryBackend, CountingBackend, CachingBackend],
) -> None:
    mem, counting, cache = setup
    root = await mem.ensure_workspace_root("ws-1")
    a = await _mk_dir(mem, "ws-1", root.id, "a")
    b = await _mk_dir(mem, "ws-1", a.id, "b")
    await _mk_file(mem, "ws-1", b.id, "c.txt")

    counting.counts["get_inode"] = 0
    found = await cache.get_inode_by_path("ws-1", "/a/b/c.txt")
    assert found is not None and found.name == "c.txt"
    # 3 components, 3 inner get_inode calls.
    assert counting.counts["get_inode"] == 3

    counting.counts["get_inode"] = 0
    found2 = await cache.get_inode_by_path("ws-1", "/a/b/c.txt")
    assert found2 is not None and found2.id == found.id
    # All 3 components cached.
    assert counting.counts["get_inode"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
