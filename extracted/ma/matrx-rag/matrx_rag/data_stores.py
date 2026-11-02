"""Lazy data-store discovery + scoped retrieval.

A data store is a NAMED, CURATED bucket of content the agent can reach
into via three model-initiated tools:

  * ``knowledge_browse(action="stores")``            — discover what's available
  * ``knowledge_browse(action="store", data_store_id=…)`` — see what's IN one
  * ``knowledge_search(data_store_id=…, query=…)``   — search within one

(Those were the separate ``rag_list_data_stores`` / ``rag_get_data_store`` /
``rag_search_data_store`` tools until the 2026-07-18 knowledge consolidation.)

Plus the existing ``knowledge_search`` tool now requires SOME scope key
(data_store_id, include_sources, or active ctx_scope_id) before it will
run any SQL — see search.py.

Why "lazy":
The post-incident contract is that retrieval NEVER happens automatically.
The agent's system prompt may carry a tiny static hint that data stores
exist (cached on the agent row, not generated per-request), but the
agent has to actively call list_data_stores before it knows what's there.
Awareness mode defaults to ``none``.

Database access goes entirely through the package's matrx-orm models
(``get_db_model``) — including the typed grant-entitlement ACL and polymorphic
label lookups across host tables in ``_enrich_member_labels``. No raw
asyncpg in this module.
"""

from __future__ import annotations

import logging
import uuid
from collections import Counter
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from matrx_rag._ext import get_db_model

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DataStoreSummary:
    """Lightweight shape returned by list_data_stores — kept tiny so a
    user with 50 stores doesn't blow the model's context."""

    id: str
    name: str
    short_code: str | None
    description: str | None
    kind: str
    member_count: int
    is_active: bool
    # 'owner' (created_by) | 'org' (org member) | 'granted' (library grant, read-only)
    access: str = "owner"
    read_only: bool = False


@dataclass(frozen=True)
class DataStoreMember:
    source_kind: str
    source_id: str
    added_at: str
    notes: str | None
    label: str | None = None  # populated by enrichers when available


@dataclass(frozen=True)
class DataStoreDetail:
    id: str
    name: str
    short_code: str | None
    description: str | None
    kind: str
    organization_id: str | None
    is_active: bool
    settings: dict[str, Any]
    members: list[DataStoreMember] = field(default_factory=list)
    # 'owner' | 'org' | 'granted'. read_only is True only for 'granted' (shared
    # library content) — write endpoints gate on ownership (can_access_data_store).
    access: str = "owner"
    read_only: bool = False


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------


async def create_data_store(
    *,
    name: str,
    description: str | None,
    kind: str,
    created_by: str,
    organization_id: str,
    short_code: str | None = None,
    settings: dict[str, Any] | None = None,
) -> str:
    """Create a new data store in ``organization_id``. Returns the new id.

    THE REQUEST CONTEXT IS CARRIED, NEVER REBUILT (rule 4): the organization is
    REQUIRED and is read by the caller off its request context
    (``context_organization_id(ctx)``) or off the record it is processing.
    Until 2026-09-17 it defaulted to ``None``, which the
    ``public._stamp_org_default`` BEFORE-INSERT trigger turned into the
    CREATOR'S PERSONAL organization — a store the team that asked for it could
    not see, with no error anywhere.
    """
    organization_id = str(organization_id or "").strip()
    if not organization_id:
        raise ValueError(
            f"create_data_store(name={name!r}): the organization this store belongs "
            "to is required. Read it off the request context or off the record you "
            "are processing — a missing organization is never filled in here, and "
            "the database would silently file the store in the creator's personal "
            "workspace."
        )
    # The JSONBField serializer accepts a native dict for ``settings``.
    DataStores = get_db_model("DataStores")
    inst = await DataStores.create(
        organization_id=organization_id,
        name=name,
        short_code=short_code,
        description=description,
        kind=kind,
        settings=settings or {},
        created_by=created_by,
    )
    return str(inst.id)


async def update_data_store(
    *,
    store_id: str,
    name: str | None = None,
    description: str | None = None,
    short_code: str | None = None,
    is_active: bool | None = None,
    settings: dict[str, Any] | None = None,
) -> None:
    """Patch a data store. Pass None to leave a field unchanged."""
    # Collect only the explicitly-supplied fields (None == "leave unchanged").
    patch: dict[str, Any] = {}
    if name is not None:
        patch["name"] = name
    if description is not None:
        patch["description"] = description
    if short_code is not None:
        patch["short_code"] = short_code
    if is_active is not None:
        patch["is_active"] = is_active
    if settings is not None:
        patch["settings"] = settings
    if not patch:
        return

    DataStores = get_db_model("DataStores")
    await DataStores.update_where(
        {"id": store_id},
        updated_at=datetime.now(UTC),
        **patch,
    )


async def delete_data_store(store_id: str) -> None:
    """Move a data store to Trash (delete means archive, 2026-09-27).

    Sets ``deleted_at``; its memberships follow through the
    ``platform.soft_delete_edge`` cascade and come back on restore. Every
    reader below leaves trashed stores out.
    """
    DataStores = get_db_model("DataStores")
    await DataStores.update_where({"id": store_id, "deleted_at__isnull": True}, deleted_at=datetime.now(UTC))


# ---------------------------------------------------------------------------
# Members
# ---------------------------------------------------------------------------


async def add_member(
    *,
    store_id: str,
    source_kind: str,
    source_id: str,
    added_by: str,
    notes: str | None = None,
) -> None:
    # Decision 3 (Shared Knowledge Resources, settled 2026-07-23): adding a
    # file to a MATRX LIBRARY store moves the file to the library org under
    # the system owner (contributor kept as author in file metadata). This is
    # the ONE choke point every publish path shares — deliberately Python,
    # never a DB trigger (P4 owns rag./docproc. trigger DDL). Gate is BOTH
    # kind='library' AND the store living in the canonical library org —
    # ``kind`` alone is caller-supplied text (any user can create a
    # kind='library' store of their own), and a rehome firing on a tenant's
    # store would steal their file. A kind='library' store OUTSIDE the
    # library org is logged loudly and treated as an ordinary store.
    DataStores = get_db_model("DataStores")
    store = await DataStores.get_or_none(id=store_id, deleted_at__isnull=True)
    if store is None:
        raise ValueError(f"add_member: data store {store_id} does not exist")
    if getattr(store, "kind", None) == "library" and source_kind == "cld_file":
        from matrx_orm import call_function

        from matrx_rag.db import PACKAGE_DB_NAME

        library_org = await call_function(PACKAGE_DB_NAME, "public", "system_org_id", "library")
        library_org = str(library_org) if library_org is not None else None
        store_org = (
            str(store.organization_id) if getattr(store, "organization_id", None) else None
        )
        if library_org is None:
            raise ValueError(
                "add_member: iam.system_orgs has no 'library' org — the Matrx Library "
                "org is not seeded; refusing to publish into a library store."
            )
        if store_org == library_org:
            from matrx_rag.library import rehome_library_member_file

            await rehome_library_member_file(
                file_id=source_id,
                library_organization_id=library_org,
                contributor_hint=added_by,
            )
        else:
            logger.error(
                "add_member: store %s is kind='library' but lives in org %s, not the "
                "Matrx Library org %s — NOT rehoming file %s (treating as a normal "
                "store). A real library store in the wrong org is a curation defect.",
                store_id,
                store_org,
                library_org,
                source_id,
            )

    # Idempotent membership write keyed on the (data_store_id, source_kind,
    # source_id) primary key. On conflict EXCLUDED.added_at takes the value
    # below, mirroring the previous raw ``added_at = now()`` re-touch.
    #
    # This table carries an AFTER INSERT/UPDATE trigger
    # (``sync_data_store_member_association``) that writes
    # ``platform.associations`` as a side effect of THIS upsert — a write this
    # call is not itself instrumented for, because ``data_store_members``
    # carries no actor requirement of its own. ``actor_named_for_write`` opens
    # the transaction that upsert would otherwise run bare (or joins one
    # already open) and names an actor first, from the calling code's own
    # module, whenever nothing already declared one — the case a detached
    # background ingest task hits every time. See ``matrx_orm.write_actor``
    # for the class this closes (2026-09-19).
    from matrx_orm import actor_named_for_write

    from matrx_rag.db import PACKAGE_DB_NAME

    DataStoreMembers = get_db_model("DataStoreMembers")
    async with actor_named_for_write(PACKAGE_DB_NAME):
        await DataStoreMembers.upsert(
            {
                # A membership is a component of its store: the store's organization.
                "organization_id": str(store.organization_id),
                "data_store_id": store_id,
                "source_kind": source_kind,
                "source_id": source_id,
                "added_by": added_by,
                "notes": notes,
                "added_at": datetime.now(UTC),
                # Re-adding a source revives a soft-deleted membership.
                "deleted_at": None,
            },
            on_conflict=["data_store_id", "source_kind", "source_id"],
            update_fields=["notes", "added_by", "added_at", "deleted_at"],
        )


async def remove_member(
    *,
    store_id: str,
    source_kind: str,
    source_id: str,
) -> None:
    # Delete means archive: the membership is soft-deleted (add_member's
    # upsert revives it by clearing deleted_at).
    DataStoreMembers = get_db_model("DataStoreMembers")
    await DataStoreMembers.update_where(
        {
            "data_store_id": store_id,
            "source_kind": source_kind,
            "source_id": source_id,
            "deleted_at__isnull": True,
        },
        deleted_at=datetime.now(UTC),
    )


# ---------------------------------------------------------------------------
# Read API used by tools
# ---------------------------------------------------------------------------


async def _person_organization_ids(user_id: str) -> list[str]:
    """Every organization the person is an active member of (none = personal only)."""
    Memberships = get_db_model("Memberships")
    rows = await Memberships.filter(
        user_id=user_id,
        container_type="organization",
        status="active",
        deleted_at__isnull=True,
    ).values("organization_id")
    return sorted({str(r["organization_id"]) for r in rows if r.get("organization_id")})


async def _entitled_store_ids(organization_ids: list[str | None], *, limit: int = 200) -> list[str]:
    """Store ids the person may READ via a library grant (global | org | industry)
    in ANY of their organizations — three set-based queries however many
    organizations she has (a per-organization loop took ~45s at 144). An empty
    list still sees ``global`` grants. Capped so a tenant subscribed to many
    library stores cannot flood the model's list_data_stores context.
    """
    from matrx_orm import Q

    DataStoreGrants = get_db_model("DataStoreGrants")
    OrgIndustries = get_db_model("OrgIndustries")
    import asyncio

    orgs = [str(o) for o in organization_ids if o]
    direct = Q(audience="global")
    if orgs:
        direct = direct | (Q(audience="organization") & Q(organization_id__in=orgs))

    async def _direct() -> list[dict[str, Any]]:
        return await DataStoreGrants.filter(direct).distinct().limit(int(limit)).values("data_store_id")

    async def _industry() -> list[dict[str, Any]]:
        if not orgs:
            return []
        industries = await OrgIndustries.filter(organization_id__in=orgs).values("industry_id")
        ids = sorted({str(r["industry_id"]) for r in industries if r.get("industry_id")})
        if not ids:
            return []
        return await (
            DataStoreGrants.filter(audience="industry", industry_id__in=ids)
            .distinct()
            .limit(int(limit))
            .values("data_store_id")
        )

    direct_rows, industry_rows = await asyncio.gather(_direct(), _industry())
    seen: dict[str, None] = {}
    for r in (*direct_rows, *industry_rows):
        seen.setdefault(str(r["data_store_id"]), None)
    return list(seen)[: int(limit)]


async def list_data_stores(
    *,
    user_id: str,
    organization_id: str | None = None,
    include_inactive: bool = False,
) -> list[DataStoreSummary]:
    """List every data store the person can reach, across ALL their organizations.

    Visibility:
      * stores with ``created_by = user_id`` (personal)                -> access 'owner'
      * stores of any organization the user is an active member of      -> access 'org'
      * stores published via a library grant to any of those orgs (RO) -> access 'granted'

    ``organization_id`` is an OPTIONAL, explicit filter (an on-page organization
    filter); None means every organization. It is NEVER the selected/active
    organization — reach is the person's own memberships (access-belongs-to-
    the-person, 2026-09-25). Until then this list showed only the selected
    organization's stores and refused to answer without one.

    Returns lightweight rows — name + description + counts. The model
    pages this whole list into context, so keep it short.
    """
    filter_org = str(organization_id or "").strip() or None

    DataStores = get_db_model("DataStores")
    DataStoreMembers = get_db_model("DataStoreMembers")

    fields = ("id", "name", "short_code", "description", "kind", "is_active")

    import asyncio

    personal_qb = DataStores.alive().filter(created_by=user_id)
    if filter_org:
        personal_qb = personal_qb.filter(organization_id=filter_org)
    if not include_inactive:
        personal_qb = personal_qb.filter(is_active=True)
    # Independent reads run together: round trips, not rows, are the cost here.
    member_orgs, personal_rows = await asyncio.gather(
        _person_organization_ids(user_id), personal_qb.values(*fields)
    )
    if filter_org:
        member_orgs = [o for o in member_orgs if o == filter_org]

    # Visibility is an OR across ownership legs (personal OR org-shared).
    # QueryBuilder filters compose with AND only, so run one query per leg
    # and merge by id (a store matching both legs appears once).
    # alive(): a store in Trash is not listed (delete means archive).
    by_id: dict[str, dict[str, Any]] = {}
    access_by_id: dict[str, str] = {}
    for r in personal_rows:
        sid = str(r["id"])
        by_id[sid] = r
        access_by_id[sid] = "owner"

    async def _org_rows() -> list[dict[str, Any]]:
        if not member_orgs:
            return []
        org_qb = DataStores.alive().filter(organization_id__in=member_orgs)
        if not include_inactive:
            org_qb = org_qb.filter(is_active=True)
        return await org_qb.values(*fields)

    org_rows, entitled = await asyncio.gather(_org_rows(), _entitled_store_ids(member_orgs))
    for r in org_rows:
        sid = str(r["id"])
        if sid not in by_id:
            by_id[sid] = r
            access_by_id[sid] = "org"

    # Read-only library grants (global | org | industry) — Shared Knowledge
    # Resources. Entitlements, not ownership: they appear so the caller can
    # SEARCH them, flagged read_only. Per-chunk read access re-authorizes anyway.
    granted_ids = [gid for gid in entitled if gid not in by_id]

    async def _granted_rows() -> list[dict[str, Any]]:
        if not granted_ids:
            return []
        granted_qb = DataStores.alive().filter(id__in=granted_ids)
        if not include_inactive:
            granted_qb = granted_qb.filter(is_active=True)
        return await granted_qb.values(*fields)

    # Member counts ride the same round trip as the granted rows (one query, every id that
    # might be listed) — a count for a store that turns out to be archived is simply unused.
    count_ids = list(dict.fromkeys([*by_id.keys(), *granted_ids]))

    async def _member_rows() -> list[dict[str, Any]]:
        if not count_ids:
            return []
        return await DataStoreMembers.filter(
            data_store_id__in=count_ids, deleted_at__isnull=True
        ).values("data_store_id")

    granted_rows, member_rows = await asyncio.gather(_granted_rows(), _member_rows())
    for r in granted_rows:
        sid = str(r["id"])
        by_id[sid] = r
        access_by_id[sid] = "granted"

    if not by_id:
        return []

    counts = Counter(str(r["data_store_id"]) for r in member_rows)

    # Mirror the old ORDER BY is_active DESC, name ASC (is_active is NOT NULL).
    ordered = sorted(by_id.items(), key=lambda kv: (not bool(kv[1]["is_active"]), kv[1]["name"]))
    return [
        DataStoreSummary(
            id=store_id,
            name=r["name"],
            short_code=r["short_code"],
            description=r["description"],
            kind=r["kind"],
            member_count=int(counts.get(store_id, 0)),
            is_active=bool(r["is_active"]),
            access=access_by_id.get(store_id, "owner"),
            read_only=access_by_id.get(store_id) == "granted",
        )
        for store_id, r in ordered
    ]


async def get_data_store(
    *,
    store_id: str,
    user_id: str,
    organization_id: str | None = None,
    member_limit: int = 200,
) -> DataStoreDetail | None:
    """Fetch a single data store + its members. Returns None when the
    user can't see it.

    🚨 ACCESS IS THE CANONICAL CHECK, NEVER THE ACTIVE ORGANIZATION
    (Arman, 2026-09-23: "if you're trying to read your data, we don't give a
    fuck how you got access to it, as long as you have access"). Until then this
    read admitted "any store stamped with the caller's ACTIVE organization" —
    which handed a colleague's PERSONAL store to every co-member, and refused a
    person her own shared store whenever a different workspace was selected.
    ``iam.has_access_for(user, 'data_store', id, level)`` is the whole answer:
    owner, org membership, explicit grants, reachability, and the
    Shared-Knowledge library grants (``rag.data_store_grants``) are all folded
    into it. ``organization_id`` is accepted for call-site compatibility and
    decides nothing here.
    """
    del organization_id  # tenancy, never permission — see the docstring.
    from matrx_orm import platform_access_check

    DataStores = get_db_model("DataStores")
    DataStoreMembers = get_db_model("DataStoreMembers")

    if not user_id or not _is_uuid(str(store_id)):
        return None
    if not await platform_access_check(str(user_id), "data_store", str(store_id), "viewer"):
        return None
    store = await DataStores.get_or_none(id=store_id, deleted_at__isnull=True)
    if store is None:
        return None
    # ``access`` is a LABEL for the screen, derived after the decision: who may
    # change this store (editor) vs who may only read it (a library grant).
    if str(getattr(store, "created_by", "") or "") == str(user_id):
        access = "owner"
    elif await platform_access_check(str(user_id), "data_store", str(store_id), "editor"):
        access = "org"
    else:
        access = "granted"

    member_rows = (
        await DataStoreMembers.filter(data_store_id=store_id, deleted_at__isnull=True)
        .order_by("-added_at")
        .limit(int(member_limit))
        .values("source_kind", "source_id", "added_at", "notes")
    )
    members = [
        DataStoreMember(
            source_kind=r["source_kind"],
            source_id=r["source_id"],
            added_at=r["added_at"].isoformat() if r["added_at"] else "",
            notes=r["notes"],
        )
        for r in member_rows
    ]
    # Enrich labels best-effort. We only enrich the small set we
    # returned (capped by member_limit).
    members = await _enrich_member_labels(members)
    raw_settings = store.settings
    settings = raw_settings if isinstance(raw_settings, dict) else {}
    return DataStoreDetail(
        id=str(store.id),
        name=store.name,
        short_code=store.short_code,
        description=store.description,
        kind=store.kind,
        organization_id=str(store.organization_id) if store.organization_id else None,
        is_active=bool(store.is_active),
        settings=settings,
        members=members,
        access=access,
        read_only=(access == "granted"),
    )


async def _enrich_member_labels(members: list[DataStoreMember]) -> list[DataStoreMember]:
    """Look up a human-readable label per member. Best-effort — tolerates
    missing source rows so a deleted file in a stale store binding doesn't
    break the listing.

    Today we enrich:
      * cld_file              -> cld_files.file_name
      * processed_document    -> processed_documents.name
      * library_doc           -> rag.library_docs.title
      * note                  -> notes.label
      * code_file             -> code_files.path

    Anything else falls back to the raw source_id.
    """
    if not members:
        return members
    by_kind: dict[str, list[DataStoreMember]] = {}
    for m in members:
        by_kind.setdefault(m.source_kind, []).append(m)

    enriched: dict[tuple[str, str], str] = {}

    if "library_doc" in by_kind:
        LibraryDocs = get_db_model("LibraryDocs")
        doc_ids = [m.source_id for m in by_kind["library_doc"] if _is_uuid(m.source_id)]
        if doc_ids:
            rows = await LibraryDocs.filter(id__in=doc_ids).values("id", "title")
            for r in rows:
                enriched[("library_doc", str(r["id"]))] = r["title"]

    # Polymorphic label lookups across host tables — each resolved through
    # get_db_model(name) (host wins when hosted; matrx-rag never imports the
    # host's model files directly).
    host_kinds = {"cld_file", "processed_document", "note", "code_file"}
    if host_kinds & by_kind.keys():
        if "cld_file" in by_kind:
            ids = [i for i in (m.source_id for m in by_kind["cld_file"]) if _is_uuid(i)]
            if ids:
                Files = get_db_model("Files")
                rows = await Files.filter(id__in=ids).values("id", "file_name")
                for r in rows:
                    enriched[("cld_file", str(r["id"]))] = r["file_name"]
        if "processed_document" in by_kind:
            ids = [i for i in (m.source_id for m in by_kind["processed_document"]) if _is_uuid(i)]
            if ids:
                ProcessedDocuments = get_db_model("ProcessedDocuments")
                rows = await ProcessedDocuments.filter(id__in=ids).values("id", "name")
                for r in rows:
                    enriched[("processed_document", str(r["id"]))] = r["name"]
        if "note" in by_kind:
            ids = [i for i in (m.source_id for m in by_kind["note"]) if _is_uuid(i)]
            if ids:
                try:
                    Notes = get_db_model("Notes")
                    rows = await Notes.filter(id__in=ids).values("id", "label")
                    for r in rows:
                        enriched[("note", str(r["id"]))] = r["label"]
                except Exception as exc:  # noqa: BLE001
                    logger.debug("note label enrich failed: %s", exc)
        if "code_file" in by_kind:
            ids = [i for i in (m.source_id for m in by_kind["code_file"]) if _is_uuid(i)]
            if ids:
                try:
                    CodeFiles = get_db_model("CodeFiles")
                    rows = await CodeFiles.filter(id__in=ids).values("id", "path")
                    for r in rows:
                        enriched[("code_file", str(r["id"]))] = r["path"]
                except Exception as exc:  # noqa: BLE001
                    logger.debug("code_file label enrich failed: %s", exc)
    return [
        DataStoreMember(
            source_kind=m.source_kind,
            source_id=m.source_id,
            added_at=m.added_at,
            notes=m.notes,
            label=enriched.get((m.source_kind, m.source_id)),
        )
        for m in members
    ]


def _is_uuid(s: str) -> bool:
    try:
        uuid.UUID(s)
        return True
    except (ValueError, TypeError):
        return False


# ---------------------------------------------------------------------------
# Scope key materialization for searches
# ---------------------------------------------------------------------------


async def materialize_member_filter(
    *,
    store_id: str,
    user_id: str,
    organization_id: str | None,
) -> list[dict[str, str]] | None:
    """Resolve a data_store_id to a list of (source_kind, source_id) pairs
    suitable for the existing search.py filters (``include_sources``).

    Returns None when the user can't see the store, or it's empty. Callers
    (the search tool) treat None as "no scope" and refuse to search.
    """
    detail = await get_data_store(
        store_id=store_id,
        user_id=user_id,
        organization_id=organization_id,
        member_limit=10000,  # if you have more than 10k, redesign the bucket.
    )
    if not detail or not detail.members:
        return None
    return [{"source_kind": m.source_kind, "source_id": m.source_id} for m in detail.members]


__all__ = [
    "DataStoreDetail",
    "DataStoreMember",
    "DataStoreSummary",
    "add_member",
    "create_data_store",
    "delete_data_store",
    "get_data_store",
    "list_data_stores",
    "materialize_member_filter",
    "remove_member",
    "update_data_store",
]
