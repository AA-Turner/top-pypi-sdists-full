"""Kinds for the personal-content tool results: ``note`` · ``memory`` ·
``dataset`` (KIND_TOOL_LEDGER, ``lead-w2f``). All three are package-hosted
action dispatchers with NO active ``tool.binding`` row (the census's
no-binding set) — runtime proven by direct call, the ``sql`` precedent.

WHY ``note`` DOES NOT REUSE ``task_list``-style content kinds: these are the
workbench ``notes`` rows (label/folder/content/tags receipts), a tool surface,
not authored content. ``memory_tool_result`` is the memory TOOL's receipt
union — not the registered mnemonic content kinds (``memory_aid`` /
``memory_hint``, a different subject entirely).

All placeholder tier; union rule: every key any success branch can emit is
declared, action-specific keys optional.
"""

from __future__ import annotations

from pydantic import JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind


@kind(
    "note_tool_result",
    label="Note Tool Result",
    family="workbench",
    example={"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "label": "Ideas", "folder_name": "inbox", "content": "…", "tags": []},
    # PLACEHOLDER — get/list/create/update/patch/delete over workbench notes.
    maturity="placeholder",
)
class NoteToolResult(KindModel):
    #: `get` (flat full view) / `create` / `update` / `patch` receipts.
    id: str | None = None
    label: str | None = None
    folder_name: str | None = None
    content: str | None = None
    tags: list[str] | None = None
    visibility: str | None = None
    is_public: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None
    matched_at_pass: str | None = None
    warning: str | None = None
    #: `list` — item rows + the self-cap state.
    notes: list[dict] | None = None
    count: int | None = None
    shown: int | None = None
    truncated: bool | None = None
    note: str | None = None
    #: `delete` receipt.
    deleted: bool | None = None
    note_id: str | None = None


@kind(
    "memory_tool_result",
    label="Memory Tool Result",
    family="memory",
    example={"stored": True, "key": "favorite_color", "type": "preference"},
    # PLACEHOLDER — store/recall/search/update/forget receipts. NOT the
    # mnemonic content kinds (memory_aid / memory_hint).
    maturity="placeholder",
)
class MemoryToolResult(KindModel):
    #: `store` receipt.
    stored: bool | None = None
    key: str | None = None
    type: str | None = None
    #: `recall` / `search`.
    memories: list[dict] | None = None
    results: list[dict] | None = None
    count: int | None = None
    #: `update` / `forget` receipts (row counts).
    updated: int | None = None
    deleted: int | None = None


@kind(
    "dataset_tool_result",
    label="Dataset Tool Result",
    family="datasets",
    example={"tables": [{"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "table_name": "leads"}], "count": 1},
    # PLACEHOLDER — list/get/search/create/add_rows/update_row/delete_row over
    # user datasets.
    maturity="placeholder",
)
class DatasetToolResult(KindModel):
    #: `list`.
    tables: list[dict] | None = None
    count: int | None = None
    #: `get` — the requested projections.
    dataset_id: str | None = None
    metadata: dict | None = None
    fields: list[dict] | None = None
    rows: list[dict] | None = None
    offset: int | None = None
    limit: int | None = None
    #: `search`.
    search_term: str | None = None
    #: `create` receipt.
    table_id: str | None = None
    table_name: str | None = None
    description: str | None = None
    row_count: int | None = None
    field_count: int | None = None
    already_existed: bool | None = None
    #: `add_rows` / `update_row` / `delete_row` receipts.
    inserted: int | None = None
    row_ids: list[str] | None = None
    updated_row_id: str | None = None
    deleted_row_id: str | None = None


__all__ = ["NoteToolResult", "MemoryToolResult", "DatasetToolResult"]
