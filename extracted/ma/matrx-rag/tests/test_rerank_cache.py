"""The durable rerank-result cache: identical inputs give identical scores with no provider call.

Red before matrx_rag.rerank_cache existed (every rerank was a fresh, drifting provider call).
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

import matrx_rag
from matrx_rag import rerank_cache
from matrx_rag.rerank_cache import cached_rerank, rerank_cache_key

ORG = "884d1ce8-7b49-4fba-a2f3-0f7dd7c83d4f"
ORG_B = "11111111-2222-4333-8444-555555555555"
USER = "00000000-0000-4000-8000-000000000001"


class FakeRerankCache:
    """In-memory stand-in for the generated rag RerankCache model."""

    rows: dict[tuple[str, str], dict[str, Any]] = {}
    fail: str | None = None

    @classmethod
    async def update_where(cls, filters: dict[str, Any], **updates: Any) -> Any:
        if cls.fail == "read":
            raise RuntimeError("cache read down")
        # The read must name the organization: a key-only filter would serve another org's row.
        row = cls.rows.get((filters["organization_id"], filters["cache_key"]))
        if row is None:
            return SimpleNamespace(rows_affected=0, updated_rows=[])
        row["hit_count"] += 1
        row["deleted_at"] = updates.get("deleted_at", row.get("deleted_at"))
        return SimpleNamespace(rows_affected=1, updated_rows=[dict(row)])

    @classmethod
    async def insert_ignore(cls, data: dict[str, Any], *, on_conflict: list[str]) -> None:
        if cls.fail == "write":
            raise RuntimeError("cache write down")
        assert on_conflict == ["organization_id", "cache_key"]
        cls.rows.setdefault((data["organization_id"], data["cache_key"]), {**data, "hit_count": 0})


class CountingReranker:
    def __init__(self, model: str = "rerank-test-1") -> None:
        self.model = model
        self.calls = 0

    async def rerank(self, query: str, documents: list[str]) -> matrx_rag.RerankResult:
        self.calls += 1
        # Drifting scores, like a real cross-encoder: never equal across calls.
        return matrx_rag.RerankResult(
            scores=[0.5 + i * 0.01 + self.calls * 1e-4 for i in range(len(documents))],
            model=self.model,
        )


@pytest.fixture(autouse=True)
def _wired(monkeypatch):
    matrx_rag._ext._reset_for_tests()
    FakeRerankCache.rows = {}
    FakeRerankCache.fail = None
    matrx_rag.configure(db_models={"RerankCache": FakeRerankCache})
    captured: list[dict[str, Any]] = []

    async def fake_capture(exc, **kw):
        captured.append({"exc": exc, **kw})

    monkeypatch.setattr(rerank_cache, "capture_error", fake_capture)
    yield captured
    matrx_rag._ext._reset_for_tests()


def _run(reranker, query, docs, org=ORG):
    return asyncio.run(cached_rerank(reranker, query, docs, organization_id=org, user_id=USER))


def test_same_key_returns_cached_result_without_provider_call():
    r = CountingReranker()
    docs = ["alpha passage", "beta passage", "gamma passage"]
    first, hit1 = _run(r, "what is assurance?", docs)
    second, hit2 = _run(r, "what is assurance?", docs)
    assert (hit1, hit2) == (False, True)
    assert r.calls == 1
    assert second.scores == first.scores
    assert second.model == first.model


def test_changed_document_content_misses():
    r = CountingReranker()
    _run(r, "q", ["alpha", "beta"])
    _, hit = _run(r, "q", ["alpha", "beta (edited)"])
    assert hit is False
    assert r.calls == 2
    assert rerank_cache_key("m", "q", ["a", "b"]) != rerank_cache_key("m", "q", ["b", "a"])


def test_different_model_misses():
    docs = ["alpha", "beta"]
    _run(CountingReranker("rerank-a"), "q", docs)
    other = CountingReranker("rerank-b")
    _, hit = _run(other, "q", docs)
    assert hit is False
    assert other.calls == 1


@pytest.mark.parametrize("where", ["read", "write"])
def test_cache_error_reranks_live_and_is_captured(where, _wired):
    FakeRerankCache.fail = where
    r = CountingReranker()
    result, hit = _run(r, "q", ["alpha", "beta"])
    assert hit is False
    assert r.calls == 1
    assert len(result.scores) == 2
    assert [c["kind"] for c in _wired] == ["rag_rerank_cache_failed"]
    assert _wired[0]["context"]["op"] == where


def test_reranker_without_declared_model_is_live_every_time():
    class Undeclared:
        calls = 0

        async def rerank(self, query, documents):
            Undeclared.calls += 1
            return matrx_rag.RerankResult(scores=[0.1] * len(documents), model="x")

    _run(Undeclared(), "q", ["a"])
    _run(Undeclared(), "q", ["a"])
    assert Undeclared.calls == 2
    assert FakeRerankCache.rows == {}


def test_no_organization_neither_reads_nor_writes():
    r = CountingReranker()
    _run(r, "q", ["a"])  # org A pays and caches
    _, hit = _run(r, "q", ["a"], org=None)
    assert hit is False
    assert r.calls == 2
    assert len(FakeRerankCache.rows) == 1


def test_one_organizations_row_is_never_served_to_another():
    r = CountingReranker()
    first, _ = _run(r, "q", ["alpha", "beta"], org=ORG)
    second, hit = _run(r, "q", ["alpha", "beta"], org=ORG_B)
    assert hit is False
    assert r.calls == 2
    assert second.scores != first.scores  # org B got its own live answer, not org A's row


def test_same_key_in_two_organizations_is_two_rows():
    r = CountingReranker()
    _run(r, "q", ["alpha"], org=ORG)
    _run(r, "q", ["alpha"], org=ORG_B)
    keys = {k for _, k in FakeRerankCache.rows}
    assert len(FakeRerankCache.rows) == 2 and len(keys) == 1
    assert {o for o, _ in FakeRerankCache.rows} == {ORG, ORG_B}


def test_a_separator_inside_the_query_cannot_collide():
    assert rerank_cache_key("m\x1fq", "x", ["a"]) != rerank_cache_key("m", "q\x1fx", ["a"])
    assert rerank_cache_key("m:a", "b", []) != rerank_cache_key("m", "a:b", [])


def test_a_hit_revives_an_archived_row():
    r = CountingReranker()
    _run(r, "q", ["alpha"])
    (row,) = FakeRerankCache.rows.values()
    row["deleted_at"] = "2026-01-01T00:00:00Z"
    _, hit = _run(r, "q", ["alpha"])
    assert hit is True and row["deleted_at"] is None
