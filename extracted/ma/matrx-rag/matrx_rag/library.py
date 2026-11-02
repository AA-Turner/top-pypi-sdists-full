"""Reference library — public/shared docs (MTUS, statutes, regs).

Helpers for inserting and ingesting reference content into the
``rag.library_docs`` table. Library docs are visible to:

  * Every authenticated user when the doc sits on the SYSTEM ORG
    (``matrx-system``, 39c38960-d30c-4840-b0c1-c9960de95582, marked
    ``global_readable`` in ``iam.system_orgs``); platform documents are ``published_to_web``.
  * Members of the org when ``organization_id`` is a normal tenant org.

NO NULL ORG (owner ruling 2026-08-21, db-rules §2/§6e). Until migration 0167
this module documented and implemented the global lane as "every authenticated
user when ``organization_id IS NULL``". NULL is not a scope. ``organization_id``
is NOT NULL on this table now; global content is owned by the system org and a
missing org is filled from the creator's personal org by the
``public._stamp_org_default`` backstop. Do not reintroduce a NULL lane, and do
not ask — §2 records the ruling as settled.

THE SCOPE IS A WORD, NOT A MISSING VALUE (2026-09-17). Both ingest entry points
take ``scope="global" | "organization"`` (:data:`LibraryScope`). Until then
``organization_id=None`` carried two different meanings at once — "this is a
platform document" and "my caller lost its organization" — so the second
silently became the first, and a tenant's document landed in the world-readable
system org. ``organization_id`` is now REQUIRED for ``scope='organization'``,
REFUSED for ``scope='global'``, and ``published_to_web`` is derived from the scope
(THE REQUEST CONTEXT IS CARRIED, NEVER REBUILT, rule 4).

Two ingest paths:

* ``upsert_library_doc`` — for inline text (statute, MTUS section, policy text). Writes the
  row and returns the doc id; the host lands the words as the doc's ``inline`` Source
  (``library_doc:<id>``), then calls ``ingest_library_doc(id)`` to chunk + embed.
* ``ingest_library_pdf(local_path, ...)`` — for a PDF you already have
  on disk. Inserts a library row + runs the PDF pipeline against it
  with the library's source_kind.

Usage example (CLI / batch script)::

    doc_id = await upsert_library_doc(
        title="MTUS §9792.20 General Approaches",
        short_code="MTUS-9792.20",
        kind="guideline",
        scope="global",          # a PLATFORM reference document
        jurisdiction="US-CA",
        version="2024-Edition",
    )
    # host: land the text as Source ``library_doc:<doc_id>`` (aidream rag.library.upsert node)
    await ingest_library_doc(doc_id)
"""

from __future__ import annotations

import hashlib
import json
import logging
import uuid
from datetime import UTC, datetime
from typing import Any, Literal

from matrx_orm import call_function
from matrx_utils.row_access import publish_columns

from matrx_rag._ext import get_db_model
from matrx_rag.db import PACKAGE_DB_NAME
from matrx_rag.ingestion import SYSTEM_ORG_ID, ingest_source

logger = logging.getLogger(__name__)

# `SYSTEM_ORG_ID` is imported from ingestion (ONE definition per package). It is
# the ONLY correct owner for global/system library content — NOT the Matrx
# Library org, which exists to own shared data STORES and is deliberately NOT
# global_readable (its audience is controlled per-store through
# `rag.data_store_grants`, so flipping that bit would bypass the grant system).


def _coerce_date(v: Any) -> Any:
    """Convert ISO date strings to ``datetime.date`` objects so asyncpg's
    ``date`` type encoder accepts them. Pass-through for already-date
    values and None.
    """
    if v is None:
        return None
    from datetime import date, datetime

    if isinstance(v, date):
        return v
    if isinstance(v, str):
        return datetime.fromisoformat(v).date()
    return v


LibraryScope = Literal["global", "organization"]
"""Who a library document belongs to, said OUT LOUD by the caller.

``"global"`` — a PLATFORM reference document (a statute, an MTUS section, an
ACOEM guideline). It is owned by the system org, which ``iam.system_orgs``
marks ``global_readable``, and is ``published_to_web``.

``"organization"`` — a tenant's own reference content, owned by that tenant's
organization, NOT published to the web (``shown_to`` follows the type's knob).

Until 2026-09-17 the two were distinguished by ``organization_id is None``, so
"I am a platform document" and "my caller lost its organization" were the SAME
call, and the second one silently became the first. The scope is now a word the
caller says; the organization is required for ``"organization"`` and refused for
``"global"``, and ``published_to_web`` is derived from the scope, never from a missing
value (THE REQUEST CONTEXT IS CARRIED, NEVER REBUILT, rule 4)."""


def _resolve_library_scope(
    scope: LibraryScope, organization_id: str | None, *, what: str
) -> tuple[str, bool]:
    """(organization_id, published_to_web) for a declared scope — or a refusal.

    The platform tenant is ``SYSTEM_ORG_ID``, the ONE constant this package
    already holds for global content (``matrx_rag.ingestion``); nothing here
    invents a tenant and nothing falls back to one.
    """
    organization_id = str(organization_id or "").strip()
    if scope == "global":
        if organization_id and organization_id != SYSTEM_ORG_ID:
            raise ValueError(
                f"{what}: scope='global' means the PLATFORM owns this document, so it "
                f"cannot also name organization {organization_id!r}. Use "
                "scope='organization' for a tenant's own library content."
            )
        return SYSTEM_ORG_ID, True
    if scope == "organization":
        if not organization_id:
            raise ValueError(
                f"{what}: scope='organization' requires the organization this document "
                "belongs to — read it off the request context "
                "(``context_organization_id(ctx)``) or off the record you are "
                "processing. A missing organization is never silently promoted to "
                "platform-global content, and never left for the database to stamp."
            )
        return organization_id, False
    raise ValueError(
        f"{what}: scope must be 'global' or 'organization'; got {scope!r}"
    )


async def upsert_library_doc(
    *,
    title: str,
    kind: str,
    scope: LibraryScope,
    short_code: str | None = None,
    jurisdiction: str | None = None,
    organization_id: str | None = None,
    version: str | None = None,
    storage_uri: str | None = None,
    source_url: str | None = None,
    effective_from: str | None = None,
    effective_to: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> str:
    """Insert or update a library doc row. Returns the doc id.

    Idempotent on (organization_id, short_code) when short_code is
    set — re-running an upsert with the same code updates the row
    and bumps updated_at instead of creating a duplicate.

    ``scope`` says who owns the document (:data:`LibraryScope`): ``"global"``
    is the platform's own reference content, owned by the SYSTEM ORG and
    ``published_to_web``; ``"organization"`` is a tenant's, and REQUIRES that
    tenant's ``organization_id``. Neither is inferred from a missing value, and
    the ``_stamp_org_default`` backstop — which would derive the CREATOR's
    personal org, exactly wrong for a platform reference document — is never
    reached (db-rules §2, NO NULL ORG; §6a-1 requires the access choice, written explicitly).

    The row holds no text: a library doc's words land as its ``inline`` Source (canonical
    identity ``library_doc:<id>``) through the host's landing door, which is what
    ``ingest_library_doc`` reads (``rag.library_docs.body`` is archived and empty, 2026-10-07).
    """
    effective_from_dt = _coerce_date(effective_from)
    effective_to_dt = _coerce_date(effective_to)
    # The OWNER of this document, decided by the declared scope — a distinct
    # local, never the caller's (optional) argument rewritten in place.
    owner_organization_id, published = _resolve_library_scope(
        scope, organization_id, what=f"upsert_library_doc(title={title!r})"
    )

    LibraryDocs = get_db_model("LibraryDocs")

    existing = None
    if short_code:
        # Idempotency is per OWNER: the same short_code may exist once for the
        # platform and once per tenant.
        matches = await (
            LibraryDocs.filter(short_code=short_code, organization_id=owner_organization_id)
            .limit(1)
            .all()
        )
        existing = matches[0] if matches else None

    if existing is not None:
        existing_id = str(existing.id)
        # The old UPDATE merged jsonb in SQL (``metadata || $new``); here the
        # merge happens in Python over the row we just fetched. Library
        # upserts are batch/CLI-driven, so the lost-atomicity window is not a
        # live concern; semantics (new keys win, old keys survive) match.
        existing_meta = existing.metadata
        if isinstance(existing_meta, str):
            existing_meta = json.loads(existing_meta) if existing_meta.strip() else {}
        merged_metadata = {**(existing_meta or {}), **(metadata or {})}
        await LibraryDocs.update_where(
            {"id": existing_id},
            title=title,
            kind=kind,
            jurisdiction=jurisdiction,
            doc_version=version,
            storage_uri=storage_uri,
            source_url=source_url,
            effective_from=effective_from_dt,
            effective_to=effective_to_dt,
            metadata=merged_metadata,
            updated_at=datetime.now(UTC),
        )
        return existing_id

    created = await LibraryDocs.create(
        organization_id=owner_organization_id,
        title=title,
        short_code=short_code,
        kind=kind,
        jurisdiction=jurisdiction,
        storage_uri=storage_uri,
        source_url=source_url,
        doc_version=version,
        **publish_columns(published),
        effective_from=effective_from_dt,
        effective_to=effective_to_dt,
        metadata=metadata or {},
    )
    return str(created.id)


async def ingest_library_doc(
    doc_id: str,
    *,
    organization_id: str | None = None,
    force: bool = False,
    emitter: Any | None = None,
    run_ner: bool = False,
):
    """Run the library doc through the standard ingestion pipeline.

    Library text follows the prose chunker (recursive_text); the library_doc
    resolver assembles the title + the doc's Source text for indexing.

    Shared Knowledge Resources contract:
      * The chunks take the ORGANIZATION OF THE DOC ROW — work re-entered from a
        durable record acts in that record's organization (THE REQUEST CONTEXT IS
        CARRIED, NEVER REBUILT, rule 3). The library-doc row's ``organization_id`` is
        NOT NULL since migration 0167, so a row that answers with nothing is a
        broken record and this REFUSES by name rather than parking the chunks on
        a system org nobody chose. An explicit ``organization_id`` is honored for
        a caller re-homing content and must match nothing else.
      * ``run_ner`` defaults to False: cross-tenant shared-library text has no
        tenant scopes/entities to extract, and the NER agent fan-out is wasted cost.
    """
    org = organization_id or await _resolve_library_doc_org(doc_id)
    if not org:
        raise LibraryRehomeError(
            f"ingest_library_doc(doc_id={doc_id}): the library doc row carries no "
            "organization, so its chunks have no tenant. Every library doc is "
            "written with one (scope='global' owns it to the system org, "
            "scope='organization' to the tenant) — repair the row; nothing here "
            "picks a tenant for it."
        )
    return await ingest_source(
        "library_doc",
        doc_id,
        force=force,
        emitter=emitter,
        organization_id=org,
        owner_id=_system_owner_uuid(org),
        run_ner=run_ner,
    )


async def _resolve_library_doc_org(doc_id: str) -> str | None:
    """The library_doc row's organization_id.

    NOT NULL since migration 0167 (NO NULL ORG, db-rules §2), so this returns
    None only when the row itself is missing — the `_library_system_org_id()`
    fallback below is now a missing-row path, not a "legacy global doc" path.
    """
    LibraryDocs = get_db_model("LibraryDocs")
    row = await LibraryDocs.get_or_none(id=doc_id)
    return str(row.organization_id) if row and getattr(row, "organization_id", None) else None


async def _library_system_org_id() -> str | None:
    """The dedicated Matrx Library org (system_orgs.key='library')."""
    org_id = await call_function(PACKAGE_DB_NAME, "public", "system_org_id", "library")
    return str(org_id) if org_id is not None else None


async def ingest_library_pdf(
    *,
    title: str,
    kind: str,
    local_path: str,
    scope: LibraryScope,
    short_code: str | None = None,
    jurisdiction: str | None = None,
    organization_id: str | None = None,
    version: str | None = None,
    source_url: str | None = None,
    effective_from: str | None = None,
    effective_to: str | None = None,
    emitter: Any | None = None,
    force: bool = False,
):
    """For PDF library docs: insert the row, then run the PDF pipeline
    directly so we get per-page extraction + cleanup + section labels.

    Library PDFs land as ``cld_file`` chunks BUT with the library_doc
    metadata stamped on them so retrieval can filter to library
    content via ``filters.source_kinds=['cld_file']`` AND the chunk's
    ``metadata.library_doc_id``.
    """
    import os

    from matrx_rag.pdf_pipeline import ingest_pdf

    # Resolve the owner ONCE, up front, so the row, the file and the chunks all
    # carry the same organization the declared scope names.
    owner_organization_id, file_published = _resolve_library_scope(
        scope, organization_id, what=f"ingest_library_pdf(title={title!r})"
    )
    doc_id = await upsert_library_doc(
        title=title,
        kind=kind,
        scope=scope,
        short_code=short_code,
        jurisdiction=jurisdiction,
        organization_id=owner_organization_id,
        version=version,
        storage_uri=local_path,
        source_url=source_url,
        effective_from=effective_from,
        effective_to=effective_to,
        metadata={"is_pdf": True},
    )
    # NO NULL ORG (db-rules §2): global library content is owned by the SYSTEM
    # ORG, never by a NULL. The OWNER, though, still keys off the SCOPE —
    # `_system_owner_uuid(None)` is the seeded, never-login
    # `library-system-owner-global@system.internal` row, and re-keying it to the
    # system-org uuid would derive a user that does not exist and blow the
    # auth.users FK. Owner seed: the global seed for platform content, the
    # tenant's organization for its own. Org + published_to_web: the declared scope.
    owner_seed_org = None if scope == "global" else owner_organization_id

    # Materialize a cld_files row so the PDF pipeline can write chunks
    # under the cld_file source_kind.
    Files = get_db_model("Files")
    created_file = await Files.create(
        created_by=_system_owner_uuid(owner_seed_org),
        organization_id=owner_organization_id,
        file_path=f"/library/{kind}/{short_code or doc_id}.pdf",
        storage_uri=local_path,
        file_name=f"{title}.pdf",
        mime_type="application/pdf",
        size_bytes=os.path.getsize(local_path),
        # §6a-1: a tenant's own library PDF is org work product — not published,
        # and NEVER shown_to 'only_me': that is for a user's own artifacts, and
        # using it here is what made library files unreadable to the org that owns
        # them. Platform content is published_to_web on the global_readable system org.
        **publish_columns(file_published, _system_owner_uuid(owner_seed_org) if file_published else None),
        current_version=1,
        metadata={
            "library_doc_id": doc_id,
            "library_short_code": short_code,
            "library_kind": kind,
            "library_jurisdiction": jurisdiction,
            "library_version": version,
        },
    )
    cld_id = str(created_file.id)

    return await ingest_pdf(
        cld_file_id=cld_id,
        # Global library content is world-readable because it sits on the
        # global_readable SYSTEM ORG (db-rules §6e) — allow_global_org now
        # stamps that org rather than keeping a NULL (db-rules §2).
        allow_global_org=True,
        organization_id=owner_organization_id,
        owner_id=_system_owner_uuid(owner_seed_org),
        local_path=local_path,
        file_name=f"{title}.pdf",
        storage_uri=local_path,
        emitter=emitter,
        force=force,
        extra_metadata={
            "library_doc_id": doc_id,
            "library_short_code": short_code,
            "library_kind": kind,
            "library_jurisdiction": jurisdiction,
        },
    )


def _system_owner_uuid(organization_id: str | None) -> str:
    """Stable per-scope UUID for system-owned library content. We
    derive it deterministically so it survives reruns and we can find
    library content later by owner.

    NOTE: the canonical file creator and KgChunks owner fields carry
    FKs to ``auth.users``, so this uuid must be backed by a real (never-
    login) auth.users row before it can own anything. The Matrx Library
    org's system user is seeded by aidream migration
    ``0235_library_system_owner_and_ama_reown.sql``; a missing row fails
    the FK loudly — that is the intended scream, never add a fallback.
    """
    seed = f"library-system-owner:{organization_id or 'global'}"
    digest = hashlib.sha1(seed.encode()).hexdigest()
    return f"{digest[0:8]}-{digest[8:12]}-{digest[12:16]}-{digest[16:20]}-{digest[20:32]}"


class LibraryRehomeError(RuntimeError):
    """A library ownership-rehome invariant is broken (missing library org,
    missing file, missing system-owner auth row). Always raised loudly —
    a silent skip here is how 'the industry owns this' becomes false in data."""


# Embedding tables that mirror kg_chunks' (organization_id, created_by) stamp in
# their own (organization_id, owner_id) columns.
# Keep in sync with matrx_rag.embeddings EMBEDDING_SPECS model names.
_EMBEDDING_MODEL_NAMES = (
    "EmbeddingsOai3Small1536",
    "EmbeddingsGoogleGemini21536",
    "EmbeddingsVoyage4Large1024",
    "EmbeddingsVoyageCode31024",
)

_REOWN_BATCH = 500


async def rehome_library_member_file(
    *,
    file_id: str,
    library_organization_id: str,
    contributor_hint: str | None = None,
) -> dict[str, Any]:
    """Decision 3 (Shared Knowledge Resources, settled 2026-07-23): on
    add-to-library, MOVE the file to the library org with a system owner,
    keeping the contributor recorded as author.

    Fires from ``data_stores.add_member`` for ``kind='library'`` stores in
    the Matrx Library org, and only for ``cld_file`` members. Idempotent.

    Does three things, all keyed to the ONE system owner
    ``_system_owner_uuid(library_organization_id)``:

    1. ``files.files``: ``organization_id`` → library org, ``created_by`` →
       system owner. The previous ``created_by`` is preserved as
       ``metadata.library_contributor`` (``files.files`` has no author
       column — metadata is the sanctioned home; set once, never
       overwritten by re-adds).
    2. ``KgChunks`` for (``cld_file``, file_id): ``created_by`` → system
       owner, ``organization_id`` → library org. Required — the SHA-reuse
       ingest path keeps pre-existing contributor-owned chunk rows, so a
       re-ingest alone can never fix ownership.
    3. The embedding tables' mirrored ``owner_id``/``organization_id``.

    Raises :class:`LibraryRehomeError` on any broken invariant. Never
    degrades silently.
    """
    if not library_organization_id:
        raise LibraryRehomeError(
            f"rehome_library_member_file(file_id={file_id}): library store has no "
            "organization_id — a library store must live in the Matrx Library org."
        )
    try:
        uuid.UUID(str(file_id))
    except (ValueError, AttributeError, TypeError) as exc:
        raise LibraryRehomeError(
            f"rehome_library_member_file: source_id {file_id!r} is not a uuid — "
            "cld_file members must reference files.files.id."
        ) from exc

    system_owner = _system_owner_uuid(library_organization_id)

    Files = get_db_model("Files")
    file_row = await Files.get_or_none(id=file_id)
    if file_row is None or getattr(file_row, "deleted_at", None) is not None:
        raise LibraryRehomeError(
            f"rehome_library_member_file: files.files row {file_id} is missing or "
            "deleted — refusing to bind a dead file into a library store."
        )

    prev_owner = str(file_row.created_by) if getattr(file_row, "created_by", None) else None
    prev_org = str(file_row.organization_id) if getattr(file_row, "organization_id", None) else None
    file_already_homed = prev_owner == system_owner and prev_org == str(library_organization_id)

    if not file_already_homed:
        meta = file_row.metadata
        if isinstance(meta, str):
            meta = json.loads(meta) if meta.strip() else {}
        meta = dict(meta or {})
        # Contributor attribution is recorded ONCE — the first human owner we
        # rehomed away from. Later re-adds (owner already = system) never
        # clobber it.
        if "library_contributor" not in meta:
            contributor = (
                prev_owner if prev_owner and prev_owner != system_owner else contributor_hint
            )
            if contributor:
                meta["library_contributor"] = {
                    "user_id": contributor,
                    "previous_organization_id": prev_org,
                    "recorded_at": datetime.now(UTC).isoformat(),
                }
        try:
            await Files.update_where(
                {"id": str(file_id)},
                created_by=system_owner,
                organization_id=str(library_organization_id),
                metadata=meta,
                updated_at=datetime.now(UTC),
            )
        except Exception as exc:  # noqa: BLE001 — re-raise loud + actionable
            raise LibraryRehomeError(
                f"rehome_library_member_file: failed to move file {file_id} to the "
                f"library org (owner {system_owner}). If this is an FK violation on "
                "created_by, the library system-owner auth.users row is missing — "
                "seed it (aidream migration 0235_library_system_owner_and_ama_reown)."
            ) from exc

    # Re-own any pre-existing chunks + their embedding stamps. New chunks
    # inherit the (now system-owned) file row, so this covers history only.
    KgChunks = get_db_model("KgChunks")
    chunk_rows = await KgChunks.filter(source_kind="cld_file", source_id=str(file_id)).values(
        "id", "created_by", "organization_id"
    )
    stale_ids = [
        str(r["id"])
        for r in chunk_rows
        if str(r["created_by"] or "") != system_owner
        or str(r["organization_id"] or "") != str(library_organization_id)
    ]
    chunks_reowned = 0
    if stale_ids:
        for i in range(0, len(stale_ids), _REOWN_BATCH):
            batch = stale_ids[i : i + _REOWN_BATCH]
            result = await KgChunks.filter(id__in=batch).update(
                created_by=system_owner, organization_id=str(library_organization_id)
            )
            chunks_reowned += getattr(result, "rows_affected", 0) or 0
            for model_name in _EMBEDDING_MODEL_NAMES:
                Emb = get_db_model(model_name)
                await Emb.filter(chunk_id__in=batch).update(
                    owner_id=system_owner, organization_id=str(library_organization_id)
                )

    outcome = {
        "file_id": str(file_id),
        "system_owner": system_owner,
        "library_organization_id": str(library_organization_id),
        "file_rehomed": not file_already_homed,
        "contributor": prev_owner if prev_owner != system_owner else None,
        "chunks_reowned": chunks_reowned,
    }
    logger.info("library rehome: %s", outcome)
    return outcome


async def ingest_library_source(
    *,
    store_id: str,
    source_kind: str,
    source_id: str,
    added_by: str,
    notes: str | None = None,
    force: bool = False,
    emitter: Any | None = None,
):
    """The ONE curator publish path: bind ``source`` into a library store and
    ingest it with the library profile (``run_ner=False`` + ``cleanup=False``
    — cross-tenant content has no tenant entities, and the per-page cleanup
    agent chokes on chart/table pages), producing SYSTEM-OWNED chunks.

    * ``cld_file`` members: ``add_member`` rehomes the file (Decision 3)
      BEFORE ingest, so the PDF pipeline stamps chunks from the now-system-
      owned file row.
    * non-file members (note|transcript|scraped|research|…): the source row
      stays with its user; only the derived chunks are system-owned, via the
      ``ingest_source`` owner override.

    Returns the package ``IngestionResult``.
    """
    from matrx_rag.data_stores import add_member

    DataStores = get_db_model("DataStores")
    store = await DataStores.get_or_none(id=store_id, deleted_at__isnull=True)
    if store is None:
        raise LibraryRehomeError(f"ingest_library_source: data store {store_id} not found")
    if getattr(store, "kind", None) != "library":
        raise LibraryRehomeError(
            f"ingest_library_source: store {store_id} is kind={store.kind!r}, not 'library' — "
            "this path is for curated shared-knowledge stores only."
        )
    store_org = str(store.organization_id) if getattr(store, "organization_id", None) else None
    if not store_org:
        raise LibraryRehomeError(
            f"ingest_library_source: library store {store_id} has no organization_id — "
            "a library store must live in the Matrx Library org."
        )

    # Member add first: for cld_file this fires the Decision-3 rehome inside
    # add_member, so a failed rehome never leaves a half-published file.
    await add_member(
        store_id=store_id,
        source_kind=source_kind,
        source_id=source_id,
        added_by=added_by,
        notes=notes,
    )

    system_owner = _system_owner_uuid(store_org)
    return await ingest_source(
        source_kind,  # type: ignore[arg-type]
        source_id,
        force=force,
        emitter=emitter,
        user_id=added_by,
        organization_id=store_org,
        run_ner=False,
        cleanup=False,
        # Non-file sources resolve owner from their own row (the contributor);
        # library chunks must be system-owned (Decision 3 parity for
        # note|transcript|scraped|research). cld_file ignores this — its
        # pipeline stamps from the rehomed file row.
        owner_id=system_owner,
    )


__all__ = [
    "LibraryRehomeError",
    "ingest_library_doc",
    "ingest_library_pdf",
    "ingest_library_source",
    "rehome_library_member_file",
    "upsert_library_doc",
]
