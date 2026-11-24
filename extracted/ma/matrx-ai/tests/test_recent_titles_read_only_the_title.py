"""Reading ten whole conversation rows to get their titles walked each row's metadata on the event loop
and froze the API for 3-4 s (event_loop_stall fe7a93000da027c8)."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

import matrx_ai.agents.services.conversation_labeler as labeler


class _Query:
    def __init__(self) -> None:
        self.only_fields: tuple[str, ...] = ()

    def filter(self, **_k: object) -> _Query:
        return self

    def order_by(self, *_a: object) -> _Query:
        return self

    def limit(self, _n: int) -> _Query:
        return self

    def only(self, *fields: str) -> _Query:
        self.only_fields = fields
        return self

    async def all(self) -> list[SimpleNamespace]:
        return [SimpleNamespace(id="c1", title="Quarterly plan")]


@pytest.mark.asyncio
async def test_recent_titles_load_only_id_and_title(monkeypatch: pytest.MonkeyPatch) -> None:
    query = _Query()
    monkeypatch.setattr(labeler, "cxm", SimpleNamespace(conversation=SimpleNamespace(model=query)))
    monkeypatch.setattr(labeler, "_title_cache", SimpleNamespace(get=lambda _k: None, set=lambda _k, _v: None))
    assert await labeler._fetch_recent_titles("u1") == [{"id": "c1", "title": "Quarterly plan"}]
    assert query.only_fields == ("id", "title")
