"""The code map has ONE write path: ``save_code_map`` (plain data in), and ``materialize_code_graph``
is a thin adapter over it.

The golden rows below were recorded from ``materialize_code_graph`` BEFORE it became an adapter
(2026-10-28), for one hand-built fixture that exercises every branch: a module preamble (no entity),
a window child (no entity, its calls dropped), two chunks sharing one symbol canonical (last wins), a
resolved call, a callee that resolves only to a window (external), repeated unresolved callees
(first wins), and a module imported twice (one entity, two edges).
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_rag import code_map as code_map_module
from matrx_rag.chunking import Chunk
from matrx_rag.code_chunker import CallEdge, CodeAnalysis, ImportEdge
from matrx_rag.code_map import CodeMapResult, save_code_map
from matrx_rag.ingestion import materialize_code_graph
from matrx_rag.sources import ResolvedSource

ORG = "o-1"
OWNER = "u-1"
SRC = "src-1"
NOW = "<now>"


class _Row:
    def __init__(self, data: dict[str, Any]) -> None:
        self.kind = data["kind"]
        self.canonical_id = data["canonical_id"]
        self.id = f"ent:{data['kind']}:{data['canonical_id']}"


def _install(monkeypatch) -> list[tuple[Any, ...]]:
    calls: list[tuple[Any, ...]] = []

    def _norm(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [{k: (NOW if k == "updated_at" else v) for k, v in r.items()} for r in rows]

    class KgEntities:
        @staticmethod
        async def bulk_upsert(rows, *, conflict_fields, update_fields):
            calls.append(("entities", _norm(rows), list(conflict_fields), list(update_fields)))
            return [_Row(r) for r in rows]

    class KgEdges:
        @staticmethod
        async def bulk_insert_ignore(rows, *, on_conflict):
            calls.append(("edges", _norm(rows), list(on_conflict)))
            return len(rows)

    models = {"KgEntities": KgEntities, "KgEdges": KgEdges}
    monkeypatch.setattr(code_map_module, "get_db_model", lambda name: models[name])
    return calls


def _chunk(cid: str, kind: str, **meta: Any) -> Chunk:
    return Chunk(chunk_id=cid, parent_chunk_id=None, chunk_index=0, chunk_kind=kind, content_text=cid,
                 token_count=1, language="python", metadata=meta or None)


def _fixture() -> tuple[ResolvedSource, CodeAnalysis]:
    chunks = [
        _chunk("c-mod", "code_module", role="module", symbol_kind="module"),
        _chunk("c-box", "code_class", role="parent", symbol_kind="class_definition", symbol_name="Box",
               parent_symbol=None, line_start=10, line_end=20),
        _chunk("c-open", "code_symbol", role="leaf", symbol_kind="function_definition", symbol_name="open",
               parent_symbol="Box", line_start=11, line_end=13),
        _chunk("c-alpha", "code_symbol", role="leaf", symbol_kind="function_definition", symbol_name="alpha",
               parent_symbol=None, line_start=1, line_end=3),
        _chunk("c-beta", "code_symbol", role="parent", symbol_kind="function_definition", symbol_name="beta",
               parent_symbol=None, line_start=4, line_end=8),
        _chunk("c-beta-w1", "code_window", role="child", symbol_kind="function_definition", symbol_name="beta",
               parent_symbol=None, line_start=4, line_end=8),
        # Same canonical as c-open (canonical ignores the parent symbol): one entity, last wins.
        _chunk("c-open2", "code_symbol", role="leaf", symbol_kind="function_definition", symbol_name="open",
               parent_symbol="Crate", line_start=30, line_end=31),
        _chunk("c-anon", "code_symbol", role="leaf", symbol_kind="", symbol_name="lam", line_start=40, line_end=40),
    ]
    calls = [
        CallEdge("c-alpha", "alpha", "beta", "c-beta", 2),
        CallEdge("c-open", "open", "alpha", "c-alpha", 12),
        CallEdge("c-beta", "beta", "print", None, 5),
        CallEdge("c-alpha", "alpha", "print", None, 3),
        CallEdge("c-beta-w1", "beta", "join", None, 6),  # window caller: dropped
        CallEdge("c-anon", "lam", "beta", "c-beta-w1", 40),  # callee is only a window: external
        CallEdge("c-ghost", "ghost", "alpha", "c-alpha", 50),  # caller not a symbol: dropped
    ]
    imports = [
        ImportEdge("os", ["*"], 1),
        ImportEdge("typing", ["Any", "cast"], 2),
        ImportEdge("os", ["path"], 3),
    ]
    resolved = ResolvedSource(source_kind="code_file", source_id=SRC, field_id=None, owner_id=OWNER,
                              organization_id=ORG, text="", mime_type=None, language="python",
                              source_hash="h", metadata={"path": "pkg/mod.py"})
    return resolved, CodeAnalysis(chunks=chunks, calls=calls, imports=imports)


FILE_CANON = f"file:code_file:{SRC}"
FILE_ID = f"ent:code_file:{FILE_CANON}"
KEY = ["organization_id", "kind", "canonical_id"]


def _sym_attrs(cid: str, parent: Any, ls: int, le: int) -> dict[str, Any]:
    return {"language": "python", "file_path": "pkg/mod.py", "chunk_id": cid, "parent_symbol": parent,
            "line_start": ls, "line_end": le}


def _sym(kind: str, name: str, cid: str, parent: Any, ls: int, le: int) -> dict[str, Any]:
    return {"organization_id": ORG, "created_by": OWNER, "kind": kind, "name": name,
            "canonical_id": f"sym:python:pkg/mod.py:{name}", "attrs": _sym_attrs(cid, parent, ls, le),
            "updated_at": NOW}


def _id(kind: str, canon: str) -> str:
    return f"ent:{kind}:{canon}"


FN = "symbol_function_definition"
OPEN_ID = _id(FN, "sym:python:pkg/mod.py:open")
ALPHA_ID = _id(FN, "sym:python:pkg/mod.py:alpha")
BETA_ID = _id(FN, "sym:python:pkg/mod.py:beta")
BOX_ID = _id("symbol_class_definition", "sym:python:pkg/mod.py:Box")
LAM_ID = _id("symbol_symbol", "sym:python:pkg/mod.py:lam")
PRINT_ID = _id("unresolved_symbol", "unres:python:print")
UNRES_BETA_ID = _id("unresolved_symbol", "unres:python:beta")


def _defines(cid: str, eid: str) -> dict[str, Any]:
    return {"organization_id": ORG, "src_id": FILE_ID, "dst_id": eid, "kind": "defines",
            "source_chunk_id": cid, "attrs": {"language": "python"}}


def _call(src: str, dst: str, cid: str, name: str, line: int, external: bool) -> dict[str, Any]:
    attrs: dict[str, Any] = {"callee_name": name, "line": line, "language": "python"}
    if external:
        attrs["resolution"] = "external"
    return {"organization_id": ORG, "src_id": src, "dst_id": dst, "kind": "calls", "source_chunk_id": cid,
            "attrs": attrs}


GOLDEN: list[tuple[Any, ...]] = [
    ("entities", [{"organization_id": ORG, "created_by": OWNER, "kind": "code_file", "name": "pkg/mod.py",
                   "canonical_id": FILE_CANON, "attrs": {"language": "python", "source_id": SRC},
                   "updated_at": NOW}], KEY, ["name", "attrs", "updated_at"]),
    ("entities", [
        _sym("symbol_class_definition", "Box", "c-box", None, 10, 20),
        _sym(FN, "open", "c-open2", "Crate", 30, 31),
        _sym(FN, "alpha", "c-alpha", None, 1, 3),
        _sym(FN, "beta", "c-beta", None, 4, 8),
        _sym("symbol_symbol", "lam", "c-anon", None, 40, 40),
    ], KEY, ["name", "attrs", "updated_at"]),
    ("edges", [
        _defines("c-box", BOX_ID), _defines("c-open", OPEN_ID), _defines("c-alpha", ALPHA_ID),
        _defines("c-beta", BETA_ID), _defines("c-open2", OPEN_ID), _defines("c-anon", LAM_ID),
    ], ["id"]),
    ("entities", [
        {"organization_id": ORG, "created_by": OWNER, "kind": "module", "name": m, "canonical_id": f"mod:python:{m}",
         "attrs": {"language": "python"}, "updated_at": NOW} for m in ("os", "typing")
    ], KEY, ["name", "updated_at"]),
    ("edges", [
        {"organization_id": ORG, "src_id": FILE_ID, "dst_id": _id("module", f"mod:python:{m}"), "kind": "imports",
         "attrs": {"names": names, "line": line, "language": "python"}}
        for m, names, line in (("os", ["*"], 1), ("typing", ["Any", "cast"], 2), ("os", ["path"], 3))
    ], ["id"]),
    ("entities", [
        {"organization_id": ORG, "created_by": OWNER, "kind": "unresolved_symbol", "name": n,
         "canonical_id": f"unres:python:{n}", "attrs": {"language": "python"}, "updated_at": NOW}
        for n in ("print", "beta")
    ], KEY, ["updated_at"]),
    ("edges", [
        _call(ALPHA_ID, BETA_ID, "c-alpha", "beta", 2, False),
        _call(OPEN_ID, ALPHA_ID, "c-open", "alpha", 12, False),
        _call(BETA_ID, PRINT_ID, "c-beta", "print", 5, True),
        _call(ALPHA_ID, PRINT_ID, "c-alpha", "print", 3, True),
        _call(LAM_ID, UNRES_BETA_ID, "c-anon", "beta", 40, True),
    ], ["id"]),
]


@pytest.mark.asyncio
async def test_the_python_adapter_writes_exactly_the_golden_rows(monkeypatch) -> None:
    calls = _install(monkeypatch)
    resolved, analysis = _fixture()
    await materialize_code_graph(resolved=resolved, analysis=analysis)
    assert calls == GOLDEN


@pytest.mark.asyncio
async def test_save_code_map_from_plain_data_writes_the_same_rows_and_counts_them(monkeypatch) -> None:
    calls = _install(monkeypatch)
    resolved, analysis = _fixture()
    symbols = [
        {"chunk_id": c.chunk_id, "name": c.metadata["symbol_name"], "kind": c.metadata.get("symbol_kind"),
         "parent_symbol": c.metadata.get("parent_symbol"), "line_start": c.metadata.get("line_start"),
         "line_end": c.metadata.get("line_end")}
        for c in analysis.chunks
        if c.chunk_kind in ("code_symbol", "code_class") and (c.metadata or {}).get("symbol_name")
    ]
    result = await save_code_map(
        organization_id=ORG, created_by=OWNER, source_kind="code_file", source_id=SRC, file_path="pkg/mod.py",
        language="python", symbols=symbols,
        calls=[{"caller_chunk_id": c.caller_chunk_id, "callee_name": c.callee_name,
                "callee_chunk_id": c.callee_chunk_id, "line": c.line} for c in analysis.calls],
        imports=[{"module": i.module, "names": i.names, "line": i.line} for i in analysis.imports],
    )
    assert calls == GOLDEN
    # 1 file + 5 symbols + 2 modules + 2 unresolved; 6 defines + 3 imports + 5 calls.
    assert result == CodeMapResult(entities_written=10, edges_written=14)


@pytest.mark.asyncio
async def test_no_calls_and_no_imports_writes_nothing(monkeypatch) -> None:
    calls = _install(monkeypatch)
    result = await save_code_map(
        organization_id=ORG, created_by=OWNER, source_kind="code_file", source_id=SRC, file_path="a.py",
        language="python", symbols=[{"chunk_id": "c1", "name": "f", "kind": "function_definition"}],
        calls=[], imports=[],
    )
    assert calls == [] and result == CodeMapResult(entities_written=0, edges_written=0)


@pytest.mark.asyncio
async def test_a_missing_organization_is_refused_before_any_write(monkeypatch) -> None:
    calls = _install(monkeypatch)
    with pytest.raises(ValueError):
        await save_code_map(
            organization_id="", created_by=OWNER, source_kind="code_file", source_id=SRC, file_path="a.py",
            language="python", symbols=[], calls=[], imports=[{"module": "os"}],
        )
    assert calls == []
