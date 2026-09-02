import asyncio
import threading
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.providers.anthropic.anthropic_api import AnthropicChat


class _EmptyStream:
    def __aiter__(self) -> "_EmptyStream":
        return self

    async def __anext__(self) -> Any:
        raise StopAsyncIteration

    async def get_final_message(self) -> SimpleNamespace:
        return SimpleNamespace(stop_reason="end_turn")


class _StreamManager:
    async def __aenter__(self) -> _EmptyStream:
        return _EmptyStream()

    async def __aexit__(self, *_args: Any) -> None:
        return None


@pytest.mark.asyncio
async def test_anthropic_stream_request_setup_runs_off_event_loop() -> None:
    setup_started = threading.Event()
    release_setup = threading.Event()

    def _stream(**_kwargs: Any) -> _StreamManager:
        setup_started.set()
        assert release_setup.wait(timeout=1)
        return _StreamManager()

    chat = object.__new__(AnthropicChat)
    chat.debug = False
    chat._reasoning_open = False
    chat._reasoning_signaled = False
    chat.client = SimpleNamespace(messages=SimpleNamespace(stream=_stream))
    chat.to_unified_response = lambda *_args: SimpleNamespace(usage=None)

    execution = asyncio.create_task(chat._execute_streaming({}, SimpleNamespace(), "claude"))
    assert await asyncio.to_thread(setup_started.wait, 0.5)

    # This checkpoint can run only if synchronous SDK payload transformation
    # is not occupying the event-loop thread.
    await asyncio.wait_for(asyncio.sleep(0), timeout=0.1)

    release_setup.set()
    await asyncio.wait_for(execution, timeout=0.5)
