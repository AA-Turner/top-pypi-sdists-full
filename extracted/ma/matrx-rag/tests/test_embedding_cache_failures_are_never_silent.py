"""A cache read or write that fails must log a warning, never vanish.

A write-back swallowed with a bare ``pass`` hid for four months that the cache
column refused the default model's 1024-d vectors: every worker re-embedded the
whole tool catalog on every boot and nothing showed.
"""

from __future__ import annotations

import asyncio
import logging
from types import SimpleNamespace

import matrx_rag._ext as ext
from matrx_rag import embeddings


class _Provider:
    def spec_for(self, model):
        return SimpleNamespace(dim=3)

    async def embed(self, model, texts, input_type=None):
        return [[0.1, 0.2, 0.3] for _ in texts]


class _BrokenCache:
    async def get_cached(self, text, model):
        raise RuntimeError("read refused")

    async def _insert(self, key, model, vec, organization_id=None):
        raise ValueError("expected 1536 dimensions, not 3")


def test_cache_read_and_write_failures_log_a_warning(monkeypatch, caplog):
    monkeypatch.setattr(ext, "get_embedding_provider", lambda: _Provider())
    monkeypatch.setattr(ext, "get_embedding_cache", lambda: _BrokenCache())
    with caplog.at_level(logging.WARNING, logger=embeddings.__name__):
        out = asyncio.run(embeddings.embed("m", ["hello"], organization_id="org"))
    assert out == [[0.1, 0.2, 0.3]]
    messages = [r.getMessage() for r in caplog.records]
    assert any("cache read failed" in m for m in messages), messages
    assert any("cache write failed" in m and "dim=3" in m for m in messages), messages


class _CountingBrokenCache(_BrokenCache):
    def __init__(self) -> None:
        self.reads = 0
        self.writes = 0

    async def get_cached(self, text, model):
        self.reads += 1
        raise RuntimeError("read refused")

    async def _insert(self, key, model, vec, organization_id=None):
        self.writes += 1
        raise ValueError("write refused")


def test_a_failing_cache_is_tried_once_and_warned_once_per_call(monkeypatch, caplog):
    """2026-11-13 event_loop_stall 8c10d28f: tool_search embedded the whole catalog
    while the cache was failing; every text waited out its own failed read and logged
    its own full traceback (formatted by three handlers on the loop), freezing
    aidream-api ~2.1 s. One failure ends cache use for the call; one warning each."""
    cache = _CountingBrokenCache()
    monkeypatch.setattr(ext, "get_embedding_provider", lambda: _Provider())
    monkeypatch.setattr(ext, "get_embedding_cache", lambda: cache)
    texts = [f"tool {i}" for i in range(50)]
    with caplog.at_level(logging.WARNING, logger=embeddings.__name__):
        out = asyncio.run(embeddings.embed("m", texts, organization_id="org"))
    assert out == [[0.1, 0.2, 0.3]] * 50
    assert (cache.reads, cache.writes) == (1, 1)
    messages = [r.getMessage() for r in caplog.records]
    reads = [m for m in messages if "cache read failed" in m]
    writes = [m for m in messages if "cache write failed" in m]
    assert len(reads) == 1 and "remaining 50 text(s)" in reads[0], messages
    assert len(writes) == 1 and "50 vector(s) left unwritten" in writes[0], messages
