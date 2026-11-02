"""RAG awareness — Tier-1 context injection.

Builds a compact ``<rag_awareness>`` XML block that gets injected into
the agent's system prompt on every request via the existing context-
injection pipeline. The block tells the agent:

  - what library content is globally available (MTUS, statutes, …),
  - what personal sources the user has indexed (with section histograms),
  - which RAG tools to reach for,
  - simple rules of thumb for when to use which tool.

Why this matters: agents frequently fail to use the right tool simply
because they don't know it exists. Inline awareness in the system
prompt is the cheapest way to fix that — a few hundred tokens cost less
than one wrong-tool turn.

The block is intentionally token-light. It lists summary stats and at
most ~10 sources. For deep discovery, the agent calls
``knowledge_browse(action="sources")``.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

# Cap how many recent sources we list to keep the prompt block light.
_MAX_SOURCES_LISTED = 10
_MAX_SECTIONS_LISTED = 6


_TOOL_HINTS = """\
  <available_tools>
    knowledge_search  — semantic search across files/notes/code/library; default tool
    knowledge_browse  — action="sources" what's indexed · "chunk" full text of a hit ·
                        "entity" who/what a name appears in · "stores"/"store" curated buckets
    knowledge_compare — split-query for "compare X to standard Y" questions
    verify            — action="answer" self-check answer faithfulness (high-stakes only)
  </available_tools>
  <usage_hints>
    - For "what does MTUS say about X?" → knowledge_search with library_filter implied
    - For "is the patient's treatment consistent with MTUS?" → knowledge_compare
    - For "summarize my notes about X" → knowledge_browse action="sources" first,
      then knowledge_search
    - For "find the auth helper function" → knowledge_search with source_kinds=["code_file"]
    - A snippet is not the whole passage — knowledge_browse action="chunk" reads the rest
    - When citing facts, retrieve first; do not invent details from memory
  </usage_hints>"""


def _xml_attr(s: str) -> str:
    """Minimal escaping for values placed inside double-quoted XML attrs."""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")[:200]
    )


# ============================================================================
# Static-fragment builder (Phase 4C, post-incident)
# ============================================================================
#
# The old request-hot-path builder ``build_rag_awareness_block`` was DELETED
# (2026-07-09, raw-SQL campaign): dormant since the auto-injection incident
# ( /Users/armanisadeghi/code/common-docs/projects/knowledge-system/README.md §6), zero importers. Awareness blocks are
# STATIC fragments cached on the agent row (agx_agent.rag_awareness_fragment).
#
# The new builder runs at agent SAVE time and on data_store_changed
# notifications, NOT on the request hot path. It produces a tiny string
# (≤300 tokens) and persists it to the agent row.

_HINT_TEMPLATE_NONE = ""

_HINT_TEMPLATE_HINT = """\
<rag_hint>
  You have access to {n_stores} curated data store(s) you can search.
  Call knowledge_browse(action="stores") to discover them, then
  knowledge_search(data_store_id=..., query=...) to retrieve.
  Do NOT call knowledge_search without first picking a data_store_id, an
  include_sources list, or operating within an active scope.
</rag_hint>"""

_HINT_TEMPLATE_INLINE_SMALL_OPEN = """\
<rag_data_stores>
"""
_HINT_TEMPLATE_INLINE_SMALL_LINE = (
    '  <store id="{id}" name="{name}" kind="{kind}" members="{members}">{description}</store>\n'
)
_HINT_TEMPLATE_INLINE_SMALL_CLOSE = """\
  Use knowledge_search(data_store_id=..., query=...) to search one.
</rag_data_stores>"""


async def compute_awareness_fragment(
    *,
    user_id: str,
    organization_id: str | None,
    awareness_mode: str,
) -> str | None:
    """Build a static awareness fragment for an agent's system prompt.

    Called from:
      * agent save handler (when the agent's owner / org / awareness_mode
        changes)
      * the data_store_changed listener (when the visible store list
        changes for any agent owner)

    Returns:
      None     when awareness_mode='none' OR no stores are visible.
      A small  XML/text string otherwise. Keep it tiny — every byte rides
      every request. Empirically <300 tokens for ≤5 stores.
    """
    mode = (awareness_mode or "none").lower()
    if mode == "none":
        return None
    try:
        # Use the same read-access rules as list_data_stores — a fragment
        # that mentions a store the user can't see is worse than no
        # fragment at all.
        from matrx_rag.data_stores import list_data_stores

        # The agent's organization NEVER narrows what it is told it can search: reach is the
        # owner's own memberships and grants (access-ladder: the active/home organization is not a
        # list filter). Passing it here dropped every store outside the agent's organization.
        stores = await list_data_stores(
            user_id=user_id,
            organization_id=None,
            include_inactive=False,
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("rag.awareness.compute_awareness_fragment failed: %s", exc)
        return None

    if not stores:
        return None

    if mode == "hint":
        return _HINT_TEMPLATE_HINT.format(n_stores=len(stores))

    if mode == "inline_small":
        # Cap at 5 — anything more bloats the prompt.
        if len(stores) > 5:
            return _HINT_TEMPLATE_HINT.format(n_stores=len(stores))
        body = _HINT_TEMPLATE_INLINE_SMALL_OPEN
        for s in stores:
            description = (s.description or "").strip()
            if len(description) > 120:
                description = description[:117] + "..."
            body += _HINT_TEMPLATE_INLINE_SMALL_LINE.format(
                id=_xml_attr(s.id),
                name=_xml_attr(s.name),
                kind=_xml_attr(s.kind),
                members=int(s.member_count),
                description=_xml_attr(description),
            )
        body += _HINT_TEMPLATE_INLINE_SMALL_CLOSE
        return body

    # Unknown mode — be safe, return nothing.
    return None


async def refresh_agent_awareness_fragment(agent_id: str) -> str | None:
    """Recompute + persist the awareness fragment for one agent.

    Called from the agent save handler and from the NOTIFY listener loop.
    Reads (user_id, organization_id, rag_awareness_mode) off the row and
    runs compute_awareness_fragment, then writes back the result. Returns
    the new fragment (or None when mode='none').
    """
    from datetime import UTC, datetime

    from matrx_rag._ext import get_db_model

    Definition = get_db_model("Definition", schema="agent")
    rows = await Definition.filter(id=agent_id).values(
        "created_by", "organization_id", "rag_awareness_mode"
    )
    row = rows[0] if rows else None
    if not row:
        logger.warning("agx_agent not found for awareness refresh: %s", agent_id)
        return None
    fragment = await compute_awareness_fragment(
        user_id=str(row["created_by"]) if row["created_by"] else None,
        organization_id=str(row["organization_id"]) if row["organization_id"] else None,
        awareness_mode=row["rag_awareness_mode"],
    )
    await Definition.update_where(
        {"id": agent_id},
        rag_awareness_fragment=fragment,
        rag_awareness_refreshed_at=datetime.now(UTC),
    )
    return fragment


async def fetch_cached_awareness_fragment(agent_id: str) -> str | None:
    """Read the cached awareness fragment for an agent.

    Single primary-key fetch — designed to be safe on the request hot
    path. Returns None when the agent doesn't exist OR
    rag_awareness_mode='none' OR the fragment hasn't been computed yet.

    Integration note for the host (aidream / matrx-ai agent loader):
    when an agent's config is loaded for a request, this fragment should
    be appended to the system prompt via
    SystemInstruction.inject_context_block(). The wiring belongs in the
    agent-config loader (matrx-ai), not in the request hot path. Call
    this here ONLY if the agent loader can't include the column in its
    primary fetch. Otherwise read the column off the row directly.
    """
    from matrx_rag._ext import get_db_model

    try:
        Definition = get_db_model("Definition", schema="agent")
        rows = await Definition.filter(id=agent_id, rag_awareness_mode__ne="none").values(
            "rag_awareness_fragment"
        )
        return rows[0]["rag_awareness_fragment"] if rows else None
    except Exception as exc:  # noqa: BLE001
        logger.warning("fetch_cached_awareness_fragment failed for %s: %s", agent_id, exc)
        return None


async def refresh_agents_for_data_store(
    *,
    data_store_id: str,
    organization_id: str | None,
) -> int:
    """Refresh fragments for every agent whose owner/org could see the
    changed data store. Used by the LISTEN loop on
    `rag_data_store_changed`. Returns the number of agents updated.

    Visibility rule mirrors list_data_stores:
      * agents owned by the same user as the data store, OR
      * agents in the same organization (when org_id is non-null).
    """
    from matrx_orm import Q

    from matrx_rag._ext import get_db_model

    DataStores = get_db_model("DataStores")
    store_rows = await DataStores.filter(id=data_store_id).values("created_by", "organization_id")
    store = store_rows[0] if store_rows else None
    if not store and not organization_id:
        return 0
    owner = str(store["created_by"]) if store and store["created_by"] else None
    org = (
        str(store["organization_id"]) if store and store["organization_id"] else None
    ) or organization_id

    # Visibility is an OR across two optional legs (owner OR org); a leg with
    # no value contributes nothing (mirrors the old ``$N::uuid IS NOT NULL``
    # guard — a NULL param must not become an ``IS NULL`` match here).
    Definition = get_db_model("Definition", schema="agent")
    leg_q = None
    if owner:
        leg_q = Q(created_by=owner)
    if org:
        leg_q = (leg_q | Q(organization_id=org)) if leg_q is not None else Q(organization_id=org)
    if leg_q is None:
        candidate_rows: list[dict] = []
    else:
        candidate_rows = await Definition.filter(
            leg_q, rag_awareness_mode__ne="none", is_active=True
        ).values("id")
    refreshed = 0
    for row in candidate_rows:
        try:
            await refresh_agent_awareness_fragment(str(row["id"]))
            refreshed += 1
        except Exception as exc:  # noqa: BLE001
            logger.warning("refresh_agent_awareness_fragment %s: %s", row["id"], exc)
    return refreshed


__all__ = [
    "compute_awareness_fragment",
    "fetch_cached_awareness_fragment",
    "refresh_agent_awareness_fragment",
    "refresh_agents_for_data_store",
]
