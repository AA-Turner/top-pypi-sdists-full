import asyncio
import time
from types import SimpleNamespace

import pytest

from matrx_ai.memory.observational_memory import ObservationalMemory
from matrx_ai.memory.types import Message, MessageRole


def _slow_count(text: str) -> int:
    time.sleep(0.1)
    return len(text)


@pytest.mark.asyncio
async def test_get_status_keeps_cold_token_counter_off_event_loop() -> None:
    memory = object.__new__(ObservationalMemory)
    memory.observed_message_ids = set()
    memory.count_tokens_fn = _slow_count
    memory.config = SimpleNamespace(
        share_token_budget=False,
        observation=SimpleNamespace(token_threshold=30_000),
        reflection=SimpleNamespace(token_threshold=40_000),
    )
    memory.buffering = SimpleNamespace(is_async_observation_enabled=lambda: False)
    record = SimpleNamespace(
        observation_token_count=0,
        buffered_observations=[],
    )

    async def get_record(thread_id: str, resource_id: str):
        return record

    memory.get_or_create_record = get_record
    message = Message(
        id="message-1",
        thread_id="thread-1",
        resource_id="resource-1",
        role=MessageRole.USER,
        content="responsive loop",
    )
    loop_progressed = asyncio.Event()

    async def mark_progress() -> None:
        await asyncio.sleep(0.01)
        loop_progressed.set()

    progress_task = asyncio.create_task(mark_progress())
    status_task = asyncio.create_task(memory.get_status("thread-1", "resource-1", [message]))
    await asyncio.wait_for(loop_progressed.wait(), timeout=0.05)
    status = await status_task
    await progress_task

    assert status.message_tokens == len("responsive loop")
    assert message.token_count == len("responsive loop")
