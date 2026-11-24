"""THE VECTOR RECALL TIME LIMIT IS THE HOST'S KNOB (2026-11-15).

``rag.recall_vector`` was canceled at the pool's 10 s ``command_timeout`` whenever the ~2.5 GB
vector index was cold (``db_statement_canceled`` rows in ``ops.system_error``); the search then
answered from its other lanes and silently lost the meaning lane. The limit is now injected by the
host (``matrx_rag.configure(recall_vector_timeout_seconds=...)``; aidream binds the
``knowledge.search_vector_recall_timeout_s`` knob) and passed to the door as the driver's
per-statement timeout. Unconfigured, the door passes ``None`` — the pool's own setting.
"""

from __future__ import annotations

import pytest

from matrx_rag import _ext, search


@pytest.fixture
def captured(monkeypatch):
    seen: dict[str, object] = {}

    async def fake_call_function(database, schema, function, *args, mode="scalar", timeout=None, **kw):  # noqa: ASYNC109
        seen["function"] = function
        seen["timeout"] = timeout
        return [{"chunk_id": "k1"}]

    import matrx_orm

    monkeypatch.setattr(matrx_orm, "call_function", fake_call_function)
    monkeypatch.delitem(_ext._registry, "recall_vector_timeout_seconds", raising=False)
    yield seen
    _ext._registry.pop("recall_vector_timeout_seconds", None)


async def _recall() -> list[str]:
    return await search._recall_vector_door(
        "rag.embeddings_x", [0.1, 0.2], user_id="u1", readable=None, k=10, filters={}
    )


async def test_recall_vector_passes_the_configured_timeout(captured):
    async def thirty() -> float:
        return 30

    _ext.configure(recall_vector_timeout_seconds=thirty)
    assert await _recall() == ["k1"]
    assert captured == {"function": "recall_vector", "timeout": 30.0}


async def test_unconfigured_recall_vector_keeps_the_pool_default(captured):
    assert await _recall() == ["k1"]
    assert captured["timeout"] is None
