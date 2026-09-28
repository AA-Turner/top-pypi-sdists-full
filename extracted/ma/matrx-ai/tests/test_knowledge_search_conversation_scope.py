"""`knowledge_search` searches within the scopes its conversation is attached to — and says so.

A conversation tagged into a scope (``conversation → scope`` edges) is asking about that
scope's content. When the agent passes no ``scope_ids`` of its own, the tool asks the host
(``rag_conversation_scopes`` seam) for the conversation's scopes, forwards them to the search,
and ANNOUNCES it in the result, naming the scopes and how to widen. A failed lookup is said
out loud too; the search then runs unscoped. ``scope_ids=[]`` means "search everything".
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

import pytest

from matrx_ai.tools.implementations.rag import knowledge_search

SCOPE = "5b0f7c3e-1d2a-4c8e-9f3a-2e6d8b1a7c40"


@dataclass
class _Hit:
    chunk_id: str = "chunk-1"
    source_kind: str = "scrape_parsed_page"
    source_id: str = "258142bf-9d67-451d-9ed8-b086e8fbc92b"
    content_text: str = "a passage"
    score: float = 0.5


@dataclass
class _Resp:
    query: str = "q"
    hits: list[Any] = field(default_factory=lambda: [_Hit()])
    total_candidates: int = 1
    relevance_verdict: str = "relevant"


class _Ctx:
    user_id = "00000000-0000-4000-8000-0000000fffa3"
    organization_id = "80ad3283-ea87-4e83-9cee-7b2f2404472c"
    conversation_id = "c0ffee00-0000-4000-8000-000000000001"
    call_id = "call_scope"


@pytest.fixture
def host(monkeypatch):
    import matrx_ai._ext as ext

    state: dict[str, Any] = {"search_kwargs": None, "lookups": 0}

    def _install(scopes_fn: Any | None) -> dict[str, Any]:
        async def _search(query: str, **kw: Any):
            state["search_kwargs"] = kw
            return _Resp(query=query)

        registry: dict[str, Any] = {"rag_search": _search}
        if scopes_fn is not None:

            async def _scopes(**kw: Any):
                state["lookups"] += 1
                state["lookup_kwargs"] = kw
                return await scopes_fn(**kw)

            registry["rag_conversation_scopes"] = _scopes
        monkeypatch.setattr(ext, "get_ext", lambda name: registry[name])
        monkeypatch.setattr(ext, "has_ext", lambda name: name in registry)
        return state

    return _install


def _model_meta(res: Any) -> dict[str, Any]:
    return json.loads(res.provider_content[-1].text)


async def test_conversation_scopes_flow_into_the_search_and_are_announced(host):
    async def scopes(**_kw: Any):
        return [{"id": SCOPE, "name": "Acme Corp"}]

    state = host(scopes)
    res = await knowledge_search({"query": "renewal terms"}, _Ctx())

    assert res.success
    assert state["search_kwargs"]["scope_ids"] == [SCOPE]
    assert state["lookup_kwargs"]["conversation_id"] == _Ctx.conversation_id
    note = res.output["scope_note"]
    assert "Acme Corp" in note and "scope_ids=[]" in note
    assert res.output["searched_scope_ids"] == [SCOPE]
    # The model reads the provider blocks, not `output` — the announcement rides there too.
    assert _model_meta(res)["scope_note"] == note


async def test_agent_supplied_scope_ids_win_and_skip_the_lookup(host):
    async def scopes(**_kw: Any):
        return [{"id": SCOPE, "name": "Acme Corp"}]

    state = host(scopes)
    mine = "6c1e8d4f-2e3b-4d9f-8a4b-3f7e9c2b8d51"
    res = await knowledge_search({"query": "q", "scope_ids": [mine]}, _Ctx())
    assert res.success
    assert state["search_kwargs"]["scope_ids"] == [mine]
    assert state["lookups"] == 0
    assert "scope_note" not in res.output


async def test_empty_scope_ids_searches_everything(host):
    async def scopes(**_kw: Any):
        return [{"id": SCOPE, "name": "Acme Corp"}]

    state = host(scopes)
    res = await knowledge_search({"query": "q", "scope_ids": []}, _Ctx())
    assert res.success
    # [] would fail closed in the engine (no valid scope ids → no hits); it means "everything".
    assert state["search_kwargs"]["scope_ids"] is None
    assert state["lookups"] == 0


async def test_failed_scope_lookup_is_said_and_the_search_runs_unscoped(host):
    async def scopes(**_kw: Any):
        raise RuntimeError("associations read timed out")

    state = host(scopes)
    res = await knowledge_search({"query": "q"}, _Ctx())
    assert res.success
    assert state["search_kwargs"]["scope_ids"] is None
    note = res.output["scope_note"]
    assert "could not" in note.lower() and "associations read timed out" in note
    assert _model_meta(res)["scope_note"] == note


PROJECT = "7d2f9e5a-3f4c-4e0a-9b5c-4a8f0d3c9e62"
DOC = "8e3a0f6b-4a5d-4f1b-8c6d-5b9a1e4d0f73"


class _ProjectCtx(_Ctx):
    project_id = PROJECT


async def test_a_project_brings_its_scopes_and_filed_sources_and_says_so(host):
    """A conversation working in a project searches the project's scopes AND the
    Sources filed under it (2026-09-27), and the result names both."""

    async def attached(**_kw: Any):
        return {
            "scopes": [{"id": SCOPE, "name": "Acme Corp", "via_project": "Renewal 2026"}],
            "projects": [{"id": PROJECT, "name": "Renewal 2026"}],
            "document_ids": [DOC],
        }

    state = host(attached)
    res = await knowledge_search({"query": "renewal terms"}, _ProjectCtx())

    assert res.success
    assert state["lookup_kwargs"]["project_id"] == PROJECT
    assert state["search_kwargs"]["scope_ids"] == [SCOPE]
    assert state["search_kwargs"]["scope_document_ids"] == [DOC]
    note = res.output["scope_note"]
    assert "Acme Corp" in note and "Renewal 2026" in note and "1 Source(s)" in note
    assert "scope_ids=[]" in note
    assert res.output["searched_source_ids"] == [DOC]
    assert _model_meta(res)["scope_note"] == note


async def test_a_project_with_only_filed_sources_still_narrows(host):
    async def attached(**_kw: Any):
        return {"scopes": [], "projects": [{"id": PROJECT, "name": "Renewal 2026"}], "document_ids": [DOC]}

    state = host(attached)
    res = await knowledge_search({"query": "q"}, _ProjectCtx())
    assert state["search_kwargs"]["scope_ids"] is None
    assert state["search_kwargs"]["scope_document_ids"] == [DOC]
    assert "Renewal 2026" in res.output["scope_note"]
