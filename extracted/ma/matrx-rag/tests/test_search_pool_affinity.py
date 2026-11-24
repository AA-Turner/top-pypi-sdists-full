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


def test_no_lease_is_held_while_awaiting_anything_but_its_own_statement() -> None:
    """Hold-and-wait guard: inside a ``search()`` lease, every await passes the leased
    connection. The recall doors take their own pool checkout, so awaiting them (or a
    gather of them) under a lease held one idle connection per search while the doors
    queued for more from the same pool — five concurrent searches in one Knowledge
    request filled the 10-slot pool (database_pool_saturation, 2026-11-03)."""
    tree = ast.parse(textwrap.dedent(stable_source(search_module.search)))
    offenders: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.AsyncWith):
            continue
        for item in node.items:
            call = item.context_expr
            if not (
                isinstance(call, ast.Call)
                and isinstance(call.func, ast.Name)
                and call.func.id == "acquire_connection"
                and isinstance(item.optional_vars, ast.Name)
            ):
                continue
            leased = item.optional_vars.id
            for stmt in node.body:
                for awaited in ast.walk(stmt):
                    if not isinstance(awaited, ast.Await) or not isinstance(awaited.value, ast.Call):
                        continue
                    passed = {
                        n.id for arg in [*awaited.value.args, *(k.value for k in awaited.value.keywords)]
                        for n in ast.walk(arg) if isinstance(n, ast.Name)
                    }
                    if leased not in passed:
                        offenders.append(f"line {awaited.lineno}: {ast.unparse(awaited.value)[:80]}")
    assert offenders == [], f"a lease is held across awaits that do not use it: {offenders}"
