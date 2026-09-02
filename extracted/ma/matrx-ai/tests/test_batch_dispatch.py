from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from matrx_ai.orchestrator.concurrent_engine import ConcurrentEngine, EngineConfig
from matrx_ai.orchestrator.parallel_executor import parallel_execute


@pytest.mark.asyncio
async def test_concurrent_engine_dispatches_whole_initial_batch() -> None:
    entered = 0
    all_entered = asyncio.Event()
    release = asyncio.Event()

    async def worker(item: int) -> int:
        nonlocal entered
        entered += 1
        if entered == 40:
            all_entered.set()
        await release.wait()
        return item

    engine = ConcurrentEngine(
        EngineConfig(
            initial_concurrency=1,
            max_concurrency=1,
            retry_sweep=False,
        )
    )
    task = asyncio.create_task(engine.run(list(range(40)), worker))
    await asyncio.wait_for(all_entered.wait(), timeout=0.5)
    assert entered == 40
    release.set()
    result = await task
    assert result.succeeded_count == 40


@pytest.mark.asyncio
async def test_parallel_executor_ignores_legacy_caller_cap(monkeypatch) -> None:
    entered = 0
    all_entered = asyncio.Event()
    release = asyncio.Event()

    async def execute_ai_request(config, *, metadata):
        nonlocal entered
        entered += 1
        if entered == 40:
            all_entered.set()
        await release.wait()
        return SimpleNamespace(request=SimpleNamespace(config=config))

    monkeypatch.setattr(
        "matrx_ai.orchestrator.executor.execute_ai_request", execute_ai_request
    )
    configs = [SimpleNamespace(index=i) for i in range(40)]
    task = asyncio.create_task(parallel_execute(configs, concurrency=1))
    await asyncio.wait_for(all_entered.wait(), timeout=0.5)
    assert entered == 40
    release.set()
    results = await task
    assert len(results) == 40
    assert all(result.success for result in results)
