"""A skill catalog slice past its window is served AT ONCE and reloaded behind the turn.

Measured 2026-10-17: the 300 s window expired between one person's sends on a server, so
nearly every /chat/new turn reloaded the skill catalog on its own clock (``skills_merged``
p50 188 ms, p90 376 ms in production). Stale-while-revalidate: the stale copy answers, ONE
background reload replaces it, and only a never-loaded slice is read on the caller's clock.
"""

from __future__ import annotations

import asyncio
import time

import pytest

from matrx_ai.skills import providers


@pytest.fixture(autouse=True)
def _clean_cache():
    providers.invalidate_skill_catalog_cache()
    providers._refreshing.clear()
    yield
    providers.invalidate_skill_catalog_cache()
    providers._refreshing.clear()


@pytest.mark.asyncio
async def test_a_stale_slice_answers_without_waiting_and_reloads_once() -> None:
    old, new = ["old-row"], ["new-row"]
    providers._skills_cache["k"] = (time.monotonic() - providers._CATALOG_TTL_SECONDS - 1, old)
    release = asyncio.Event()
    loads = 0

    async def load() -> list[str]:
        nonlocal loads
        loads += 1
        await release.wait()
        return new

    # Three turns arrive while the slice is stale and the reload has not finished.
    for _ in range(3):
        got = await asyncio.wait_for(providers._serve_cached(providers._skills_cache, "k", load), 1)
        assert got is old
    release.set()
    for task in list(providers._refreshing.values()):
        await task
    assert loads == 1
    assert providers._skills_cache["k"][1] is new


@pytest.mark.asyncio
async def test_a_failed_background_reload_keeps_serving_the_copy() -> None:
    old = ["old-row"]
    providers._skills_cache["k"] = (time.monotonic() - providers._CATALOG_TTL_SECONDS - 1, old)

    async def load() -> list[str]:
        raise RuntimeError("database blip")

    assert await providers._serve_cached(providers._skills_cache, "k", load) is old
    for task in list(providers._refreshing.values()):
        await task
    assert providers._skills_cache["k"][1] is old


@pytest.mark.asyncio
async def test_a_slice_never_loaded_is_read_on_the_callers_clock() -> None:
    async def load() -> list[str]:
        return ["fresh"]

    assert await providers._serve_cached(providers._skills_cache, "k", load) == ["fresh"]
    assert providers._skills_cache["k"][1] == ["fresh"]
