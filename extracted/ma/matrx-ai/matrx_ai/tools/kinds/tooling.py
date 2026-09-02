"""Kinds for the platform's own tool-management tool results.

Ledger rows: the 43 ``bundle:list_*`` listers (KIND_TOOL_LEDGER, agent
``claude-tools-01``).
"""

from __future__ import annotations

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind


@kind(
    "tool_bundle_listing",
    label="Tool Bundle Listing",
    family="tooling",
    example={
        "bundle": "supabase",
        "tools_loaded": ["execute_sql", "list_tables"],
        "count": 2,
        "skipped_unresolved": [],
        "server_slug": "supabase",
    },
    # PLACEHOLDER — this captures the outer structure honestly and completely;
    # there is no richer shape being flattened away. One generic handler
    # (``implementations/bundle_lister.py``) serves all 43 ``bundle:list_*``
    # rows and returns exactly these five keys, so the whole family is ONE kind
    # rather than 43 near-duplicate slugs (NOMENCLATURE.md).
    #
    # ``tools_loaded`` and ``skipped_unresolved`` are canonical tool NAMES, not
    # tool objects: the lister's job is to swap the active toolset, and the
    # member definitions it resolved are already the registry's to describe. A
    # kind that nested full tool definitions here would be inventing data this
    # result does not carry.
    maturity="placeholder",
)
class ToolBundleListing(KindModel):
    """What a ``bundle:list_<name>`` lister returns after swapping the toolset."""

    bundle: str = ""
    tools_loaded: list[str] = []
    count: int = 0
    skipped_unresolved: list[str] = []
    #: Set only for MCP-auto-managed bundles; ``None`` for hand-curated ones.
    server_slug: str | None = None
