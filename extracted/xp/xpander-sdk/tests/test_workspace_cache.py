"""Unit tests for the L1 in-memory cache + workspace write queue.

Pure asyncio — no agno, no HTTP, no agent wiring. The cache is a small
asyncio-aware data structure; these tests pin its contract:

* ``put`` stores immediately and spawns the background write
* ``get`` returns the same bytes the writer saw, even before the spawned
  write has resolved
* ``aflush`` waits for every queued write and surfaces the first error
* ``aclose`` drains and clears the in-memory store
"""

import asyncio

import pytest

from xpander_sdk.core.context_optimizer.workspace_cache import (
    WorkspaceCache,
    WorkspaceCacheEntry,
)


def _make_slow_writer(delay: float, log: list, key: str):
    async def _do_write():
        await asyncio.sleep(delay)
        log.append(key)

    return _do_write


def _make_failing_writer(message: str):
    async def _do_write():
        raise RuntimeError(message)

    return _do_write


@pytest.mark.asyncio
async def test_put_then_get_returns_same_bytes_synchronously():
    cache = WorkspaceCache()
    cache.put(
        context_id="abc",
        encrypted="ENCRYPTED_BYTES",
        size=1234,
        workspace_path="CONTEXT_OPTIMIZATION/abc.xp",
        do_write_async=_make_slow_writer(0.05, [], "abc"),
    )

    entry = cache.get("abc")
    assert isinstance(entry, WorkspaceCacheEntry)
    assert entry.encrypted == "ENCRYPTED_BYTES"
    assert entry.size == 1234
    assert entry.workspace_path == "CONTEXT_OPTIMIZATION/abc.xp"

    # Stats reflect the put + the hit.
    assert cache.stats["puts"] == 1
    assert cache.stats["mem_hits"] == 1

    await cache.aclose()


@pytest.mark.asyncio
async def test_get_miss_increments_miss_counter():
    cache = WorkspaceCache()
    assert cache.get("nonexistent") is None
    assert cache.stats["mem_misses"] == 1
    await cache.aclose()


@pytest.mark.asyncio
async def test_aflush_waits_for_all_pending_writes():
    cache = WorkspaceCache()
    log: list = []

    cache.put(
        context_id="a",
        encrypted="A",
        size=1,
        workspace_path="CONTEXT_OPTIMIZATION/a.xp",
        do_write_async=_make_slow_writer(0.05, log, "a"),
    )
    cache.put(
        context_id="b",
        encrypted="B",
        size=1,
        workspace_path="CONTEXT_OPTIMIZATION/b.xp",
        do_write_async=_make_slow_writer(0.10, log, "b"),
    )
    cache.put(
        context_id="c",
        encrypted="C",
        size=1,
        workspace_path="CONTEXT_OPTIMIZATION/c.xp",
        do_write_async=_make_slow_writer(0.02, log, "c"),
    )

    assert cache.has_pending()
    assert cache.stats["pending_writes_peak"] == 3

    await cache.aflush()

    assert sorted(log) == ["a", "b", "c"]
    assert not cache.has_pending()
    assert cache.stats["barrier_count"] == 1
    assert cache.stats["barrier_wait_ms_total"] > 0


@pytest.mark.asyncio
async def test_aflush_surfaces_first_queued_error():
    cache = WorkspaceCache()

    cache.put(
        context_id="ok",
        encrypted="OK",
        size=1,
        workspace_path="CONTEXT_OPTIMIZATION/ok.xp",
        do_write_async=_make_slow_writer(0.01, [], "ok"),
    )
    cache.put(
        context_id="boom",
        encrypted="BOOM",
        size=1,
        workspace_path="CONTEXT_OPTIMIZATION/boom.xp",
        do_write_async=_make_failing_writer("workspace went down"),
    )

    with pytest.raises(RuntimeError, match="workspace went down"):
        await cache.aflush()

    # Subsequent flush is clean (errors drained).
    await cache.aflush()

    assert cache.stats["write_failures"] == 1
    assert cache.stats["barrier_count"] == 2


@pytest.mark.asyncio
async def test_get_returns_bytes_before_background_write_resolves():
    """Read-after-write consistency — the spec's central guarantee."""
    cache = WorkspaceCache()
    write_started = asyncio.Event()
    release = asyncio.Event()

    async def _gated_write():
        write_started.set()
        await release.wait()

    cache.put(
        context_id="x",
        encrypted="PAYLOAD",
        size=7,
        workspace_path="CONTEXT_OPTIMIZATION/x.xp",
        do_write_async=_gated_write,
    )

    # Background write is in flight (not resolved). The cache must still
    # serve the bytes the writer just put.
    await write_started.wait()
    assert cache.has_pending()

    entry = cache.get("x")
    assert entry is not None
    assert entry.encrypted == "PAYLOAD"

    # Let the writer complete and drain.
    release.set()
    await cache.aflush()
    assert not cache.has_pending()

    await cache.aclose()


@pytest.mark.asyncio
async def test_aclose_drains_pending_and_clears_entries():
    cache = WorkspaceCache()
    log: list = []
    cache.put(
        context_id="z",
        encrypted="Z",
        size=1,
        workspace_path="CONTEXT_OPTIMIZATION/z.xp",
        do_write_async=_make_slow_writer(0.05, log, "z"),
    )

    await cache.aclose()

    assert log == ["z"]
    assert cache.get("z") is None
    assert not cache.has_pending()


@pytest.mark.asyncio
async def test_aclose_logs_but_does_not_raise_on_queued_failure():
    """Spec: at task end, errors are logged not raised — the task is
    finishing and propagating up serves no purpose."""
    cache = WorkspaceCache()
    cache.put(
        context_id="bad",
        encrypted="BAD",
        size=1,
        workspace_path="CONTEXT_OPTIMIZATION/bad.xp",
        do_write_async=_make_failing_writer("late failure"),
    )

    # No exception expected.
    await cache.aclose()

    assert cache.stats["write_failures"] == 1
    assert cache.get("bad") is None
