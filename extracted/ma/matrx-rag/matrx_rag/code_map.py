"""The code map of one code file: the ONE write path for its entities and edges.

``save_code_map`` takes PLAIN data (pieces already saved, named by their chunk id) and writes, in the
knowledge-graph tables ``kg_entities`` / ``kg_edges``:

* one ``code_file`` entity (canonical ``file:<source_kind>:<source_id>``);
* one ``symbol_<kind>`` entity per symbol (canonical ``sym:<language>:<file_path>:<name>``; two symbols
  sharing a canonical collapse to one row, last wins) and a ``defines`` edge file → symbol carrying the
  symbol's piece as ``source_chunk_id``;
* one ``module`` entity per imported module (``mod:<language>:<module>``, first wins) and an ``imports``
  edge file → module per import statement;
* a ``calls`` edge caller symbol → callee symbol when the callee resolved to a symbol piece, else
  caller → an ``unresolved_symbol`` entity (``unres:<language>:<name>``, first wins) with
  ``attrs.resolution = "external"``. A call whose caller is not a symbol piece is dropped.

A file with no calls and no imports writes nothing. Entity upserts conflict on
``(organization_id, kind, canonical_id)``; edges are plain inserts (re-ingest removes a piece's old
edges through the chunk cascade). Statements run in sequence, not one transaction: the map is
idempotent and a partial write heals on the next save.

Callers: ``ingestion.materialize_code_graph`` (the Python ingest's adapter, deleted with
``ingest_source``) and the host's workflow step that saves a code file's map. The caller decides who
may write — this function trusts its organization and person.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from matrx_rag._ext import get_db_model

_ENTITY_KEY = ["organization_id", "kind", "canonical_id"]


@dataclass(frozen=True)
class CodeMapResult:
    entities_written: int = 0
    edges_written: int = 0


def _landed(result: Any, sent: int) -> int:
    return result if isinstance(result, int) else (len(result) if result is not None else sent)


async def save_code_map(
    *,
    organization_id: str,
    created_by: str | None,
    source_kind: str,
    source_id: str,
    file_path: str,
    language: str | None,
    symbols: Iterable[Mapping[str, Any]],
    calls: Iterable[Mapping[str, Any]],
    imports: Iterable[Mapping[str, Any]],
) -> CodeMapResult:
    """Write one code file's map.

    ``symbols``: ``{chunk_id, name, kind, parent_symbol?, line_start?, line_end?}``.
    ``calls``: ``{caller_chunk_id, callee_name, callee_chunk_id?, line?}``.
    ``imports``: ``{module, names?, line?}``.
    """
    if not organization_id:
        raise ValueError("save_code_map needs the organization the map is written in.")
    calls = list(calls)
    imports = list(imports)
    if not calls and not imports:
        return CodeMapResult()

    org = organization_id
    creator = created_by or None
    language = language or "unknown"
    file_canonical = f"file:{source_kind}:{source_id}"

    sym_by_chunk_id: dict[str, dict[str, Any]] = {}
    for s in symbols:
        sym_by_chunk_id[str(s["chunk_id"])] = {
            "canonical": f"sym:{language}:{file_path}:{s.get('name')}",
            "name": s.get("name") or "<anonymous>",
            "kind": str(s.get("kind") or "symbol"),
            "chunk_id": str(s["chunk_id"]),
            "parent": s.get("parent_symbol"),
            "line_start": s.get("line_start"),
            "line_end": s.get("line_end"),
        }

    KgEntities = get_db_model("KgEntities")
    KgEdges = get_db_model("KgEdges")
    now_utc = datetime.now(UTC)
    entities = 0
    edges = 0

    # 1. file entity.
    file_rows = await KgEntities.bulk_upsert(
        [
            {
                "organization_id": org,
                "created_by": creator,
                "kind": "code_file",
                "name": file_path,
                "canonical_id": file_canonical,
                "attrs": {"language": language, "source_id": source_id},
                "updated_at": now_utc,
            }
        ],
        conflict_fields=_ENTITY_KEY,
        update_fields=["name", "attrs", "updated_at"],
    )
    file_entity_id = str(file_rows[0].id)
    entities += len(file_rows)

    # 2. symbol entities — one bulk upsert cannot touch a row twice, so dedupe by the conflict key
    #    first (last wins) and fan the returned ids back out per piece.
    sym_rows_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for sym in sym_by_chunk_id.values():
        sym_kind = f"symbol_{sym['kind']}"
        sym_rows_by_key[(sym_kind, sym["canonical"])] = {
            "organization_id": org,
            "created_by": creator,
            "kind": sym_kind,
            "name": sym["name"],
            "canonical_id": sym["canonical"],
            "attrs": {
                "language": language,
                "file_path": file_path,
                "chunk_id": sym["chunk_id"],
                "parent_symbol": sym["parent"],
                "line_start": sym["line_start"],
                "line_end": sym["line_end"],
            },
            "updated_at": now_utc,
        }
    sym_entity_ids: dict[str, str] = {}
    if sym_rows_by_key:
        upserted = await KgEntities.bulk_upsert(
            list(sym_rows_by_key.values()),
            conflict_fields=_ENTITY_KEY,
            update_fields=["name", "attrs", "updated_at"],
        )
        entities += len(upserted)
        id_by_key = {(str(row.kind), str(row.canonical_id)): str(row.id) for row in upserted}
        for chunk_id, sym in sym_by_chunk_id.items():
            sym_entity_ids[chunk_id] = id_by_key[(f"symbol_{sym['kind']}", sym["canonical"])]

    # 3. defines edges: file → symbol (the id conflict target is server-generated: plain inserts).
    if sym_entity_ids:
        rows = [
            {
                "organization_id": org,
                "src_id": file_entity_id,
                "dst_id": eid,
                "kind": "defines",
                "source_chunk_id": chunk_id,
                "attrs": {"language": language},
            }
            for chunk_id, eid in sym_entity_ids.items()
        ]
        edges += _landed(await KgEdges.bulk_insert_ignore(rows, on_conflict=["id"]), len(rows))

    # 4. import edges: file → module. Module entities first-wins; on conflict only name + updated_at.
    module_rows_by_key: dict[str, dict[str, Any]] = {}
    for imp in imports:
        key = f"mod:{language}:{imp['module']}"
        if key not in module_rows_by_key:
            module_rows_by_key[key] = {
                "organization_id": org,
                "created_by": creator,
                "kind": "module",
                "name": imp["module"],
                "canonical_id": key,
                "attrs": {"language": language},
                "updated_at": now_utc,
            }
    module_entity_ids: dict[str, str] = {}
    if module_rows_by_key:
        upserted = await KgEntities.bulk_upsert(
            list(module_rows_by_key.values()),
            conflict_fields=_ENTITY_KEY,
            update_fields=["name", "updated_at"],
        )
        entities += len(upserted)
        module_entity_ids = {str(row.canonical_id): str(row.id) for row in upserted}
    import_rows = [
        {
            "organization_id": org,
            "src_id": file_entity_id,
            "dst_id": module_entity_ids[f"mod:{language}:{imp['module']}"],
            "kind": "imports",
            # source_chunk_id absent → NULL: an import belongs to the file, not a piece.
            "attrs": {"names": imp.get("names"), "line": imp.get("line"), "language": language},
        }
        for imp in imports
    ]
    if import_rows:
        edges += _landed(await KgEdges.bulk_insert_ignore(import_rows, on_conflict=["id"]), len(import_rows))

    # 5. calls edges. Unresolved callees get an 'unresolved_symbol' entity (first wins; on conflict
    #    only updated_at).
    def _resolved(call: Mapping[str, Any]) -> str | None:
        callee = call.get("callee_chunk_id")
        return sym_entity_ids.get(str(callee)) if callee else None

    unresolved_rows_by_canonical: dict[str, dict[str, Any]] = {}
    for call in calls:
        if sym_entity_ids.get(str(call["caller_chunk_id"])) is None or _resolved(call) is not None:
            continue
        canonical = f"unres:{language}:{call['callee_name']}"
        if canonical not in unresolved_rows_by_canonical:
            unresolved_rows_by_canonical[canonical] = {
                "organization_id": org,
                "created_by": creator,
                "kind": "unresolved_symbol",
                "name": call["callee_name"],
                "canonical_id": canonical,
                "attrs": {"language": language},
                "updated_at": now_utc,
            }
    unresolved_entity_ids: dict[str, str] = {}
    if unresolved_rows_by_canonical:
        upserted = await KgEntities.bulk_upsert(
            list(unresolved_rows_by_canonical.values()),
            conflict_fields=_ENTITY_KEY,
            update_fields=["updated_at"],
        )
        entities += len(upserted)
        unresolved_entity_ids = {str(row.canonical_id): str(row.id) for row in upserted}

    call_rows: list[dict[str, Any]] = []
    for call in calls:
        caller = str(call["caller_chunk_id"])
        src_id = sym_entity_ids.get(caller)
        if src_id is None:
            continue
        attrs: dict[str, Any] = {"callee_name": call["callee_name"], "line": call.get("line"), "language": language}
        dst_id = _resolved(call)
        if dst_id is None:
            dst_id = unresolved_entity_ids[f"unres:{language}:{call['callee_name']}"]
            attrs["resolution"] = "external"
        call_rows.append(
            {
                "organization_id": org,
                "src_id": src_id,
                "dst_id": dst_id,
                "kind": "calls",
                "source_chunk_id": caller,
                "attrs": attrs,
            }
        )
    if call_rows:
        edges += _landed(await KgEdges.bulk_insert_ignore(call_rows, on_conflict=["id"]), len(call_rows))

    return CodeMapResult(entities_written=entities, edges_written=edges)


__all__ = ["CodeMapResult", "save_code_map"]
