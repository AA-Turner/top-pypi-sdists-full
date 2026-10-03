"""An update with an empty match is an UPDATE with no WHERE — every row. Refused like delete."""

import asyncio
from types import SimpleNamespace

from matrx_ai.tools.implementations import database


def test_empty_match_update_is_refused_before_any_db_work(monkeypatch) -> None:
    async def _boom(*_a, **_k):
        raise AssertionError("resolved a write target for an unbounded update")

    monkeypatch.setattr(database, "_resolve_write_target", _boom)
    ctx = SimpleNamespace(call_id="c1")
    result = asyncio.run(database.db_update({"table": "public.note", "data": {"title": "x"}, "match": {}}, ctx))
    assert not result.success
    assert "unbounded UPDATE" in result.error.message
