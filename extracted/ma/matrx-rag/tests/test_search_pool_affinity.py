from __future__ import annotations

import ast
from matrx_utils.source_guard import stable_source
import textwrap

import pytest

import matrx_rag.search as search_module


def test_recall_lease_contains_no_nested_orm_checkout_or_external_call() -> None:
    """Every await inside acquire_connection must use the explicit connection."""
    tree = ast.parse(textwrap.dedent(stable_source(search_module.search)))
    lease_blocks: list[ast.AsyncWith] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.AsyncWith):
            continue
        if any(
            isinstance(item.context_expr, ast.Call)
            and isinstance(item.context_expr.func, ast.Name)
            and item.context_expr.func.id == "acquire_connection"
            for item in node.items
        ):
            lease_blocks.append(node)

    assert lease_blocks
    forbidden_calls = {"values", "expand_query", "hyde_passage", "embed", "_cohere_rerank"}
    found = {
        call.func.attr if isinstance(call.func, ast.Attribute) else call.func.id
        for block in lease_blocks
        for awaited in ast.walk(block)
        if isinstance(awaited, ast.Await)
        for call in ast.walk(awaited.value)
        if isinstance(call, ast.Call)
        and (isinstance(call.func, ast.Attribute) or isinstance(call.func, ast.Name))
        and (call.func.attr if isinstance(call.func, ast.Attribute) else call.func.id)
        in forbidden_calls
    }
    assert found == set(), f"connection lease contains nested/external awaits: {found}"


@pytest.mark.asyncio
async def test_candidate_read_is_one_statement_on_the_caller_connection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Bodies, priority, importance and Source name for every candidate: ONE read on
    the recall connection (it replaced three serial reads + the service's title read)."""
    expected_connection = object()
    reads: list[tuple] = []

    class _Query:
        def annotate(self, **kwargs: object) -> _Query:
            assert set(kwargs) == {"importance_sum", "source_name", "page_section_title"}
            return self

        async def fetch_via(self, connection: object, *fields: str) -> list[dict[str, object]]:
            reads.append((connection, fields))
            return [{"id": "chunk-1", "priority": 3, "importance_sum": None, "source_name": "Doc"}]

    class _Any:
        def __getattr__(self, name):
            return lambda *a, **k: self

    class _Chunks:
        @classmethod
        def filter(cls, *args: object, **kwargs: object):
            if kwargs.get("id__in") == ["chunk-1"]:
                assert kwargs == {"id__in": ["chunk-1"], "deleted_at__isnull": True}
                return _Query()
            return _Any()

    monkeypatch.setattr(search_module, "get_db_model", lambda _name: _Chunks)
    rows = await search_module._hydrate_candidates(expected_connection, ["chunk-1"])
    assert len(reads) == 1 and reads[0][0] is expected_connection
    assert {"content_text", "priority", "importance_sum", "source_name", "page_section_title"} <= set(reads[0][1])
    assert rows["chunk-1"]["source_name"] == "Doc"
    assert await search_module._hydrate_candidates(expected_connection, []) == {}
