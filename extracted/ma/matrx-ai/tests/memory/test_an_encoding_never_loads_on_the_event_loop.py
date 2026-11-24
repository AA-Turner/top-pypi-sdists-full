"""A tiktoken encoding is never loaded on the event loop thread.

Live: tiktoken's first ``get_encoding`` downloads and parses the BPE file with a blocking ``requests.get``; in the send
boundary's token estimate that froze the whole server for 1.1-3.9s on every fresh container (event_loop_stall
aidream-api:698eecc767d01e9e, 2026-11-11). Red on the prior code: the load ran on the loop thread.
"""

from __future__ import annotations

import asyncio
import threading
import time

import pytest

from matrx_ai.memory import token_counter


@pytest.fixture
def slow_loader(monkeypatch):
    calls: list[str] = []  # the thread of every COLD load (the real ``_get_encoding`` is lru-cached after it)
    fake_encoding = type("Enc", (), {"encode": staticmethod(lambda text: text.split())})()
    cache: dict[str, object] = {}

    def _slow_get_encoding(name: str):
        if name not in cache:
            calls.append(threading.current_thread().name)
            time.sleep(0.2)
            cache[name] = fake_encoding
        return cache[name]

    monkeypatch.setattr(token_counter, "_get_encoding", _slow_get_encoding)
    monkeypatch.setattr(token_counter, "_loaded", set(), raising=False)
    monkeypatch.setattr(token_counter, "_loading", set(), raising=False)
    return calls


def test_a_call_on_the_loop_never_loads_the_encoding_there(slow_loader):
    async def _on_loop():
        loop_thread = threading.current_thread().name
        started = time.monotonic()
        first = token_counter.count_tokens_tiktoken("hello there friend", "o200k_base")
        held = time.monotonic() - started
        for _ in range(50):
            if "o200k_base" in token_counter._loaded:
                break
            await asyncio.sleep(0.02)
        second = token_counter.count_tokens_tiktoken("hello there friend", "o200k_base")
        return loop_thread, held, first, second

    loop_thread, held, first, second = asyncio.run(_on_loop())
    assert held < 0.1, f"the encoding load held the event loop for {held:.2f}s"
    assert first is None
    assert second == 3
    assert slow_loader and loop_thread not in slow_loader, slow_loader


def test_a_call_off_the_loop_loads_in_place(slow_loader):
    assert token_counter.count_tokens_tiktoken("one two", "o200k_base") == 2
    assert slow_loader == [threading.current_thread().name]
