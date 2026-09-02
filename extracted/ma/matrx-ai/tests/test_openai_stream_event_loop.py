from __future__ import annotations

import asyncio
import time
from types import SimpleNamespace

import pytest

from matrx_ai.providers.openai.openai_api import OpenAIChat


class _Stream:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return None

    def __aiter__(self):
        return self

    async def __anext__(self):
        raise StopAsyncIteration

    async def get_final_response(self):
        return SimpleNamespace(output=[], usage=None)


class _Responses:
    def __init__(self):
        self.kwargs = None

    def stream(self, **kwargs):
        self.kwargs = kwargs
        # Reproduce the SDK failure mode only when the large typed body is sent
        # as ordinary keyword arguments. The repaired adapter passes it as one
        # already-final wire body through extra_body.
        if "tools" in kwargs:
            time.sleep(0.1)
        return _Stream()


class _Emitter:
    async def send_chunk(self, _content):
        return None


@pytest.mark.asyncio
async def test_large_openai_wire_body_skips_sdk_recursive_transform_on_loop() -> None:
    responses = _Responses()
    chat = object.__new__(OpenAIChat)
    chat.client = SimpleNamespace(responses=responses)
    chat._reasoning_started = {}
    chat._reasoning_signaled_ids = set()
    chat.to_unified_response = lambda response, _model: response

    wire_body = {
        "model": "gpt-5.5",
        "input": [{"role": "user", "content": "hello"}],
        "tools": [
            {
                "type": "function",
                "name": f"tool_{index}",
                "parameters": {"type": "object", "properties": {}},
            }
            for index in range(500)
        ],
    }
    ticks = 0

    async def ticker() -> None:
        nonlocal ticks
        for _ in range(3):
            await asyncio.sleep(0)
            ticks += 1

    await asyncio.gather(
        chat._execute_streaming(wire_body, _Emitter(), "gpt-5.5"),
        ticker(),
    )

    assert ticks == 3
    assert responses.kwargs == {
        "input": "",
        "model": "wire-body",
        "extra_body": {**wire_body, "stream": True},
    }
