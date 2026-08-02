"""_spawn_bg must retain a strong ref so a fire-and-forget report can't be GC'd."""
import asyncio

import pytest

from xpander_sdk.modules.backend.frameworks import agno


@pytest.mark.asyncio
async def test_spawn_bg_runs_and_retains_then_discards():
    ran = {}

    async def _work():
        await asyncio.sleep(0)
        ran["done"] = True

    agno._spawn_bg(_work())
    # While pending, a strong ref is held (no GC drop).
    assert len(agno._BG_REPORT_TASKS) >= 1
    await asyncio.sleep(0.01)
    assert ran.get("done") is True
    # Cleaned up via done callback.
    assert all(not t.done() or t not in agno._BG_REPORT_TASKS for t in list(agno._BG_REPORT_TASKS))
