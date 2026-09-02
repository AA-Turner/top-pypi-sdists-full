"""Kind for the ``value_store`` tool result (KIND_TOOL_LEDGER, ``lead-w2c``).

One union across the five actions: `list` (bounded descriptor page),
`describe`/`put` (one ValueDescriptor dump, `put` adding ``stored``), `get`
(the sized read with its paging keys — the cap keys ARE part of the shape),
and `groom` (the queued stub/retain receipt). Placeholder tier: descriptor
rows stay opaque ``dict``s; ``content`` is the caller's value and stays open.
"""

from __future__ import annotations

from pydantic import JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind


@kind(
    "value_store_result",
    label="Value Store Result",
    family="conversation_values",
    example={
        "key": "meeting_summary",
        "kind": "json",
        "total_chars": 1204,
        "offset": 0,
        "returned_chars": 500,
        "next_offset": 500,
        "has_more": True,
        "content": "[partial 0:500 of 1204] {\"summary\": …",
    },
    maturity="placeholder",
)
class ValueStoreResult(KindModel):
    #: `list` — bounded descriptor page.
    total: int | None = None
    shown: int | None = None
    values: list[dict] | None = None
    #: `describe` / `put` — one ValueDescriptor dump (`put` adds `stored`).
    key: str | None = None
    description: str | None = None
    kind: str | None = None
    chars: int | None = None
    truncated: bool | None = None
    preview: str | None = None
    json_keys: list[str] | None = None
    fence: str | None = None
    stored: bool | None = None
    #: `get` — the sized read (agent-declared max_chars honored) + paging keys.
    field: str | None = None
    total_chars: int | None = None
    offset: int | None = None
    returned_chars: int | None = None
    next_offset: int | None = None
    has_more: bool | None = None
    content: JsonValue | None = None
    retained_inline: bool | None = None
    #: `groom` — the queued stub/retain receipt.
    queued_stub_keys: list[str] | None = None
    queued_retain_keys: list[str] | None = None
    note: str | None = None
