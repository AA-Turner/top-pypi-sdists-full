"""Source adapter dispatch — turns ``(source_kind, source_id)`` into the
canonical content + metadata that ingestion can chunk and embed.

Phase 1 supports:

* ``note``        → ``workbench.notes``            (label + content)
* ``code_file``   → ``code.code_files``          (path + content + language)
* ``cld_file``    → ``files.files``                  (text MIME types only — PDFs
                                                    land in Phase 2 with Document AI)
* ``transcript``  → ``transcripts.transcripts``         (title + flattened segments)
* ``scraped``     → ``scraper.scrape_parsed_page``  (url + raw_text body)
* ``repository``  → ``code.code_repositories``   (manifest text — code_files
                                                    children are ingested
                                                    separately as code_file rows)
* ``research``    → ``research.rs_source`` (+ rs_topic / rs_content) (a research
                                                    source's title + scraped body;
                                                    owner via rs_topic.created_by)
* ``library_doc`` → ``rag.library_docs``           (org-scoped + system-org global content)
* ``document``    → ``content.document``           (every document type: Spaces pages render
                                                    their ``content.space_payload`` blocks;
                                                    annotations carry the highlighted text +
                                                    comment + what they annotate; the rest are
                                                    title + markdown body)

Each adapter returns a ``ResolvedSource`` carrying:
  * ``text``            — canonical extracted text (empty when binary).
  * ``mime_type``       — best-known MIME.
  * ``language``        — for code, the language attr.
  * ``owner_id``        — auth.users.id of the row owner.
  * ``organization_id`` — when set on the row.
  * ``metadata``        — passthrough fields the chunker / search filters
                          will key on (file path, folder, tags, …).

Adapters are async + use the rag pool. They never raise on missing rows;
they return ``None`` so the caller can treat "source vanished between
job enqueue and pickup" as a benign no-op.
"""

from __future__ import annotations

import base64
import binascii
import hashlib
import logging
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from typing import Any, Literal

from matrx_files.cloud_sync.media_ref import MediaRef
from matrx_orm import Q
from matrx_utils import vcprint
from matrx_utils.ctx import system_file_access
from matrx_utils.row_access import is_published

from matrx_rag._ext import (
    decode_content_blocks,
    get_cloud_file_manager,
    get_db_model,
    get_human_authored_text,
    get_univer_current_reader,
    get_univer_text_renderer,
)
from matrx_rag.secret_guard import guard_text, secrets_metadata


logger = logging.getLogger(__name__)

# Every resolver below EXCEPT _resolve_library_doc reads a HOST-owned table
# (notes, code_files, files, transcripts, scrape_parsed_page,
# code_repositories, projects.tasks, projects.projects, chat.conversation /
# chat.message, rs_source / rs_topic / rs_content). Those tables belong to
# the host's services; matrx-rag resolves their generated Model classes by
# name through the ``get_db_model`` injection seam (matrx_rag._ext) rather
# than importing the host's model modules — the standard host-read pattern
# used throughout this package. Every access below goes through matrx-orm;
# SQL fragments and driver pools are not part of this module's persistence surface.


class UnsupportedMimeError(Exception):
    """Raised when a resolver fetched the row, can identify the bytes,
    but has no wired-up extraction path for that MIME (e.g. an audio
    file, an .xlsx, a .docx that the pdf_pipeline / image_pipeline /
    text resolvers don't cover yet).

    Distinct from "source not found" — that still returns ``None`` so a
    deleted source mid-pipeline is a benign no-op. ``UnsupportedMimeError``
    means "the row exists and is owned by the caller but the ingestion
    pipeline can't handle this content type" — the caller MUST surface
    this to the user, not silently leave the document at
    ``status='pending'`` forever.
    """

    def __init__(
        self,
        *,
        source_kind: str,
        source_id: str,
        mime_type: str | None,
        file_name: str | None = None,
        hint: str | None = None,
        binary_pipeline: bool = False,
    ) -> None:
        self.source_kind = source_kind
        self.source_id = source_id
        self.mime_type = mime_type or "unknown"
        self.file_name = file_name
        # True ⇒ the TEXT resolver can't handle it, but a dedicated binary
        # pipeline (pdf_pipeline / image_pipeline) CAN and will — the caller
        # should defer to ``ingest_source``'s binary dispatch, not report a
        # failure. False ⇒ genuinely unwired (audio, .docx, .xlsx).
        self.binary_pipeline = binary_pipeline
        self.hint = hint or (
            "Supported MIMEs: text/* + application/json|xml|yaml + PDFs + "
            "common image formats. Other types need a dedicated extraction "
            "pipeline."
        )
        super().__init__(
            f"Unsupported MIME for ingestion: source_kind={source_kind} "
            f"source_id={source_id} mime_type={self.mime_type} "
            f"file_name={file_name!r}. {self.hint}"
        )


SourceKind = Literal[
    "note",
    "code_file",
    "cld_file",
    "library_doc",
    "transcript",
    "scraped",
    "repository",
    "task",
    "project",
    "cx_message",
    "research",
    "document",
    # workbench.udt_workbooks (token ``workbook``) and workbench.udt_documents
    # (token ``udt_document``, Univer cloud docs): the latest snapshot rendered
    # through the host's ``univer_text_renderer`` seam.
    "workbook",
    "udt_document",
    # canvas.canvas_items (token ``canvas_item``): title + description + the content's strings.
    "canvas_item",
]

# Text-only MIME types we'll ingest in Phase 1. PDFs / images / audio are
# Phase 2 with Document AI.
TEXT_MIMES = {
    "text/plain",
    "text/markdown",
    "text/html",
    "text/x-python",
    "text/x-typescript",
    "text/x-javascript",
    "text/x-go",
    "text/x-java",
    "text/x-rust",
    "text/x-c",
    "text/x-c++",
    "application/json",
    "application/xml",
    "application/x-yaml",
    "application/yaml",
    "text/csv",
    "text/tab-separated-values",
}


def normalize_mime(mime_type: str | None) -> str:
    """Canonical MIME for membership checks: lowercased, parameters stripped.

    Stored mimes routinely carry parameters (``text/plain;charset=utf-8`` —
    browsers/TUS write them verbatim). Every ``in TEXT_MIMES`` / ``in
    IMAGE_MIMES`` / ``== application/pdf`` check MUST compare the normalized
    form, or a plain text file fails ingest as ``unsupported_mime`` purely
    because of its charset suffix (live incident: job 78228058, 2026-06-17).
    ``aidream``'s ``is_rag_ingestible`` normalizes the same way — the two
    gates must never diverge.
    """
    if not mime_type:
        return ""
    return mime_type.lower().split(";", 1)[0].strip()


# MIMEs handled by ``rag.pdf_pipeline`` — fetched, OCR'd, LLM-cleaned, then
# chunked via the page-aware splitter.  PDFs do NOT go through the
# generic ``ingest_source`` path because they need per-page extraction
# and the cleanup/concurrency cap.
PDF_MIMES = {"application/pdf"}

_PDF_SUFFIXES = (".pdf",)
_IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".heic", ".heif", ".bmp")

BinaryPipeline = Literal["pdf", "image", ""]


def classify_binary_pipeline(mime_type: str | None, file_name: str | None) -> BinaryPipeline:
    """Which dedicated binary pipeline (if any) owns this file.

    THE single source of truth for "does a non-text extraction pipeline exist
    for these bytes". ``ingestion._maybe_dispatch_pdf`` routes on it and
    ``_resolve_cld_file`` uses it to tell "handled elsewhere" apart from
    "genuinely unwired" — before this existed the two disagreed, and every
    PDF ingest printed a red ``no extraction pipeline wired`` banner while the
    PDF pipeline was, in fact, happily running.

    Matches on MIME **or** filename suffix: cld_files rows routinely carry a
    generic ``application/octet-stream`` from a TUS upload.
    """
    from matrx_rag.image_pipeline import IMAGE_MIMES

    mime = normalize_mime(mime_type)
    name = (file_name or "").lower()

    if mime in PDF_MIMES or name.endswith(_PDF_SUFFIXES):
        return "pdf"
    if mime in IMAGE_MIMES or name.endswith(_IMAGE_SUFFIXES):
        return "image"
    return ""


@dataclass
class ResolvedSource:
    source_kind: SourceKind
    source_id: str
    field_id: str | None
    owner_id: str
    organization_id: str | None
    text: str
    mime_type: str | None
    language: str | None
    source_hash: str
    metadata: dict[str, object] = field(default_factory=dict)


async def resolve(
    source_kind: SourceKind,
    source_id: str,
    field_id: str | None = None,
    *,
    user_id: str | None = None,
) -> ResolvedSource | None:
    """Resolve a source body, with the platform secret guard applied.

    This is the ONE door every source kind comes through, so it is where the
    content-level secret guard lives (2026-09-13 incident: a note containing a
    raw ``.env`` dump was indexed verbatim and served back through
    ``knowledge_search``). The resolver dispatch itself is
    :func:`_resolve_dispatch`; this wrapper redacts secret VALUES out of the
    resolved text before any caller can chunk, embed or store it, records the
    count + credential NAMES on ``metadata`` and screams in the log. Ingestion
    is never blocked — the source is indexed minus its credentials.
    """
    resolved = await _resolve_dispatch(source_kind, source_id, field_id, user_id=user_id)
    if resolved is None or not resolved.text:
        return resolved
    clean, count, names = guard_text(
        resolved.text,
        source_kind=str(source_kind),
        source_id=resolved.source_id,
        where="sources.resolve",
    )
    if count <= 0:
        return resolved
    metadata = dict(resolved.metadata or {})
    metadata.update(secrets_metadata(count, names))
    return replace(resolved, text=clean, metadata=metadata)


async def _resolve_dispatch(
    source_kind: SourceKind,
    source_id: str,
    field_id: str | None = None,
    *,
    user_id: str | None = None,
) -> ResolvedSource | None:
    """Dispatch resolver by ``source_kind``.

    ``user_id`` is REQUIRED for all resolvers except ``library_doc`` (which is
    global by design). Every user-owned source kind (note, code_file,
    cld_file, transcript, scraped, repository, task, project, cx_message,
    research) fails closed on a missing user_id — a None returns None
    immediately so an upstream wiring bug cannot silently leak rows across
    tenants (P0-11 cross-tenant exfiltration fix).
    """
    if source_kind == "note":
        if not user_id:
            return None
        return await _resolve_note(source_id, user_id=user_id)
    if source_kind == "code_file":
        if not user_id:
            return None
        return await _resolve_code_file(source_id, user_id=user_id)
    if source_kind == "cld_file":
        if not user_id:
            return None
        return await _resolve_cld_file(source_id, field_id, user_id=user_id)
    if source_kind == "library_doc":
        return await _resolve_library_doc(source_id)
    if source_kind == "transcript":
        if not user_id:
            return None
        return await _resolve_transcript(source_id, user_id=user_id)
    if source_kind == "scraped":
        if not user_id:
            return None
        return await _resolve_scraped(source_id, user_id=user_id)
    if source_kind == "repository":
        if not user_id:
            return None
        return await _resolve_repository(source_id, user_id=user_id)
    if source_kind == "task":
        if not user_id:
            return None
        return await _resolve_task(source_id, user_id=user_id)
    if source_kind == "project":
        if not user_id:
            return None
        return await _resolve_project(source_id, user_id=user_id)
    if source_kind == "cx_message":
        if not user_id:
            return None
        return await _resolve_cx_message(source_id, user_id=user_id)
    if source_kind == "research":
        if not user_id:
            return None
        return await _resolve_research(source_id, user_id=user_id)
    if source_kind == "document":
        if not user_id:
            return None
        return await _resolve_document(source_id, user_id=user_id)
    if source_kind == "canvas_item":
        if not user_id:
            return None
        return await _resolve_canvas_item(source_id, user_id=user_id)
    if source_kind in _UDT_KINDS:
        if not user_id:
            return None
        return await _resolve_udt(source_kind, source_id, user_id=user_id)
    raise ValueError(f"Unknown source_kind: {source_kind!r}")


async def _resolve_note(note_id: str, *, user_id: str) -> ResolvedSource | None:
    """ACL: ``workbench.notes.created_by`` must match the caller — fail-closed so a
    row we do NOT own is indistinguishable from one that doesn't exist (P0-11
    cross-tenant exfiltration fix)."""
    Notes = get_db_model("Notes")
    rows = await Notes.filter(
        id=note_id, created_by=user_id, deleted_at__isnull=True
    ).values("id", "created_by", "organization_id", "label", "content", "home_scope_id", "tags", "metadata")
    row = rows[0] if rows else None
    if row is None:
        return None
    label = row["label"] or ""
    content = row["content"] or ""
    text = (label + "\n\n" + content).strip()
    body_for_hash = text
    return ResolvedSource(
        source_kind="note",
        source_id=str(row["id"]),
        field_id=None,
        owner_id=str(row["created_by"]),
        organization_id=str(row["organization_id"]) if row["organization_id"] else None,
        text=text,
        mime_type="text/markdown",
        language=None,
        source_hash=_hash(body_for_hash),
        metadata={
            "title": label,
            "home_scope_id": str(row["home_scope_id"]) if row["home_scope_id"] else "",
            "tags": list(row["tags"] or []),
            "row_metadata": _coerce_jsonb(row["metadata"]),
        },
    )


# ── content.document ─────────────────────────────────────────────────────────
#: Spaces block types whose own ``text`` renders with a markdown prefix.
_SPACE_PREFIX = {"bulleted": "- ", "numbered": "1. ", "quote": "> ", "callout": "> "}
#: Spaces block types that carry no searchable text of their own (layout or a
#: pointer to another document, which is ingested as its own row).
_SPACE_SILENT = {"divider", "column", "columnList", "page"}


def _rich_text(value: object) -> str:
    """A Spaces rich-text run list (``[{"text": "..."}, ...]``) → plain text."""
    if isinstance(value, str):
        return value
    if not isinstance(value, list):
        return ""
    return "".join(str(run.get("text") or "") for run in value if isinstance(run, dict))


def render_space_blocks(snapshot: object) -> str:
    """Render a ``content.space_payload.snapshot`` (``{"blocks": [...]}``) to markdown.

    Headings keep their level, lists / to-dos / quotes keep their markers, inline
    databases contribute their title, images their caption; layout blocks and
    child-page pointers contribute nothing (a child page is its own document).
    Children render after their parent, in order.
    """
    snap = _coerce_jsonb(snapshot)
    lines: list[str] = []

    def walk(blocks: object) -> None:
        if not isinstance(blocks, list):
            return
        for blk in blocks:
            if not isinstance(blk, dict):
                continue
            kind = str(blk.get("type") or "")
            props = blk.get("props") if isinstance(blk.get("props"), dict) else {}
            text = _rich_text(blk.get("text")).strip()
            line = ""
            if kind in _SPACE_SILENT:
                line = ""
            elif kind == "heading":
                level = props.get("level") if isinstance(props.get("level"), int) else 2
                line = ("#" * max(1, min(6, level)) + " " + text) if text else ""
            elif kind == "todo":
                line = ("- [x] " if props.get("checked") else "- [ ] ") + text if text else ""
            elif kind in _SPACE_PREFIX:
                line = _SPACE_PREFIX[kind] + text if text else ""
            elif kind == "code":
                lang = str(props.get("language") or "")
                line = f"```{lang}\n{text}\n```" if text else ""
            elif kind == "image":
                line = _rich_text(props.get("caption")).strip()
            elif kind == "database":
                title = str(props.get("title") or "").strip()
                line = f"Table: {title}" if title else ""
            else:
                line = text
            if line:
                lines.append(line)
            walk(blk.get("children"))

    walk(snap.get("blocks"))
    return "\n\n".join(lines)


async def _document_type_slug(document_type_id: object) -> str:
    if not document_type_id:
        return ""
    Categories = get_db_model("Categories", schema="platform")
    rows = await Categories.filter(id=document_type_id).values("slug")
    return str(rows[0]["slug"] or "") if rows else ""


async def _space_text(row: dict[str, Any]) -> str:
    SpacePayload = get_db_model("SpacePayload", schema="content")
    rows = await SpacePayload.filter(
        document_id=row["id"], content_version=row["content_version"]
    ).values("snapshot")
    rendered = render_space_blocks(rows[0]["snapshot"]) if rows else ""
    # No payload at this version → the stored body projection is the honest fallback.
    return rendered or (row["body"] or "")


async def _annotation_parts(document_id: str) -> tuple[list[str], list[dict[str, str]]]:
    """The highlighted passages and what they annotate, from the ``annotates`` edges."""
    Associations = get_db_model("Associations", schema="platform")
    edges = await Associations.filter(
        source_type="document", source_id=document_id, role="annotates", deleted_at__isnull=True
    ).values("target_type", "target_id", "payload")
    quotes: list[str] = []
    targets: list[dict[str, str]] = []
    for edge in edges:
        payload = _coerce_jsonb(edge["payload"])
        anchors = payload.get("anchors") if isinstance(payload.get("anchors"), list) else [payload]
        for anchor in anchors:
            if isinstance(anchor, dict) and str(anchor.get("exact") or "").strip():
                quotes.append(str(anchor["exact"]).strip())
        targets.append({"type": str(edge["target_type"] or ""), "id": str(edge["target_id"] or "")})
    return quotes, targets


async def _target_title(target: dict[str, str]) -> str:
    try:
        if target["type"] == "document":
            Document = get_db_model("Document", schema="content")
            rows = await Document.filter(id=target["id"]).values("title")
            return str(rows[0]["title"] or "") if rows else ""
        if target["type"] == "note":
            Notes = get_db_model("Notes")
            rows = await Notes.filter(id=target["id"]).values("label")
            return str(rows[0]["label"] or "") if rows else ""
    except Exception:  # noqa: BLE001 — a missing title never blocks indexing
        logger.debug("sources: annotation target title lookup failed for %s", target, exc_info=True)
    return ""


async def _resolve_document(document_id: str, *, user_id: str) -> ResolvedSource | None:
    """A ``content.document`` row of ANY type — Spaces pages, Markdown Studio
    annotations, notes and every other document type.

    ACL: ``created_by`` must match the caller (fail-closed, exactly like ``note``);
    soft-deleted and archived rows resolve to ``None``. Who may READ the chunks is
    decided at search time by the kernel on the row itself
    (``iam.has_access_for(person, 'document', id)``), so a Spaces page shared with
    an organization is found by its members and a personal one only by its owner.
    """
    Document = get_db_model("Document", schema="content")
    rows = await Document.filter(
        id=document_id, created_by=user_id, deleted_at__isnull=True, archived_at__isnull=True
    ).values(
        "id", "created_by", "organization_id", "document_type_id", "title", "format", "body",
        "content_version", "visibility", "metadata",
    )
    row = rows[0] if rows else None
    if row is None:
        return None
    slug = await _document_type_slug(row["document_type_id"])
    title = (row["title"] or "").strip()
    fmt = row["format"] or ""
    extra: dict[str, object] = {}
    if fmt == "spaces" or slug == "space":
        body = await _space_text(row)
    elif slug == "annotation":
        quotes, targets = await _annotation_parts(str(row["id"]))
        parts = [f"> {q}" for q in quotes]
        if (row["body"] or "").strip():
            parts.append(row["body"].strip())
        for target in targets:
            name = await _target_title(target)
            parts.append(f"Annotates {target['type']}" + (f": {name}" if name else f" {target['id']}"))
        body = "\n\n".join(parts)
        extra = {"annotates": targets, "highlights": quotes}
    else:
        body = row["body"] or ""
    text = "\n\n".join(p for p in (f"# {title}" if title else "", body.strip()) if p).strip()
    if not text:
        return None
    visibility = row["visibility"]
    return ResolvedSource(
        source_kind="document",
        source_id=str(row["id"]),
        field_id=None,
        owner_id=str(row["created_by"]),
        organization_id=str(row["organization_id"]) if row["organization_id"] else None,
        text=text,
        mime_type="text/markdown",
        language=None,
        source_hash=_hash(text),
        metadata={
            "title": title,
            "document_type": slug,
            "format": fmt,
            "content_version": row["content_version"],
            "visibility": getattr(visibility, "value", visibility),
            "row_metadata": _coerce_jsonb(row["metadata"]),
            **extra,
        },
    )


# ── workbench.udt_workbooks / workbench.udt_documents ─────────────────────────
#: source_kind → (row model, title column, snapshot model, snapshot FK column).
_UDT_KINDS: dict[str, tuple[str, str, str, str]] = {
    "workbook": ("UdtWorkbooks", "workbook_name", "UdtWorkbookSnapshots", "workbook_id"),
    "udt_document": ("UdtDocuments", "document_name", "UdtDocumentSnapshots", "document_id"),
}


async def _resolve_udt(source_kind: str, source_id: str, *, user_id: str) -> ResolvedSource | None:
    """A workbook (``workbook``) or Univer cloud document (``udt_document``).

    ACL: ``created_by`` must match the caller (fail-closed, exactly like ``note`` and
    ``document``); soft-deleted rows resolve to ``None``. Who may READ the chunks is
    decided at search time by the kernel on the row (``iam.has_access_for(person,
    '<token>', id)``). The body is the LATEST snapshot, rendered by the host's
    ``univer_text_renderer`` seam (the same renderer the workbook/document tools use).
    """
    row_model, title_col, snap_model, fk_col = _UDT_KINDS[source_kind]
    Row = get_db_model(row_model, schema="workbench")
    rows = await Row.filter(id=source_id, created_by=user_id, deleted_at__isnull=True).values(
        "id", "created_by", "organization_id", title_col, "description", "visibility", "metadata"
    )
    row = rows[0] if rows else None
    if row is None:
        return None
    Snap = get_db_model(snap_model, schema="workbench")
    snaps = await Snap.filter(**{fk_col: source_id}).order_by("-created_at").limit(1).values("id", "snapshot")
    snapshot = _coerce_jsonb(snaps[0]["snapshot"]) if snaps else {}
    # A record people are co-editing holds more than its last save: index what they see now.
    collab: dict[str, Any] | None = None
    current_reader = get_univer_current_reader()
    if current_reader is not None:
        live = await current_reader(source_kind, source_id, user_id)
        if live is not None:
            snapshot, collab = (live[0] or {}), live[1]
    body = str(get_univer_text_renderer()(source_kind, snapshot) or "").strip() if snapshot else ""
    title = str(row[title_col] or "").strip()
    description = str(row["description"] or "").strip()
    text = "\n\n".join(p for p in (f"# {title}" if title else "", description, body) if p).strip()
    if not body and not description:
        return None
    visibility = row["visibility"]
    return ResolvedSource(
        source_kind=source_kind,  # type: ignore[arg-type]
        source_id=str(row["id"]),
        field_id=None,
        owner_id=str(row["created_by"]),
        organization_id=str(row["organization_id"]) if row["organization_id"] else None,
        text=text,
        mime_type="text/markdown",
        language=None,
        source_hash=_hash(text),
        metadata={
            "title": title,
            "snapshot_id": str(snaps[0]["id"]) if snaps else "",
            "visibility": getattr(visibility, "value", visibility),
            "row_metadata": _coerce_jsonb(row["metadata"]),
            **({"collab": collab} if collab else {}),
        },
    )


async def _resolve_code_file(file_id: str, *, user_id: str) -> ResolvedSource | None:
    """ACL: ``code.code_files.created_by`` must match the caller — fail-closed
    so a row we do NOT own is indistinguishable from one that doesn't exist
    (P0-11 cross-tenant exfiltration fix)."""
    CodeFiles = get_db_model("CodeFiles")
    rows = await CodeFiles.filter(
        id=file_id, created_by=user_id, deleted_at__isnull=True
    ).values("id", "created_by", "organization_id", "path", "name", "content", "language", "tags", "metadata")
    row = rows[0] if rows else None
    if row is None:
        return None
    text = row["content"] or ""
    language = row["language"] or "plaintext"
    return ResolvedSource(
        source_kind="code_file",
        source_id=str(row["id"]),
        field_id=None,
        owner_id=str(row["created_by"]),
        organization_id=str(row["organization_id"]) if row["organization_id"] else None,
        text=text,
        mime_type=_mime_for_language(language),
        language=language,
        source_hash=_hash(text),
        metadata={
            "path": row["path"],
            "name": row["name"],
            "tags": list(row["tags"] or []),
            "row_metadata": _coerce_jsonb(row["metadata"]),
        },
    )


async def _has_active_grant(*, resource_id: Any, resource_type: str, user_id: str) -> bool:
    """Whether ``user_id`` holds an active ``iam.permissions`` grant (direct or
    via org membership) on ``resource_type``/``resource_id``. Mirrors the
    ``perm_active`` + org-membership clauses in
    ``matrx_rag.file_acl_sql.file_row_access_predicate``."""
    Permissions = get_db_model("Permissions")
    now = datetime.now(UTC)
    direct = await (
        Permissions.filter(
            resource_id=resource_id,
            resource_type=resource_type,
            granted_to_user_id=user_id,
            status="active",
        )
        .filter(Q(expires_at__isnull=True) | Q(expires_at__gt=now))
        .exists()
    )
    if direct:
        return True
    Memberships = get_db_model("Memberships")
    org_ids = await Memberships.filter(
        user_id=user_id,
        container_type="organization",
        status="active",
        deleted_at__isnull=True,
    ).values_list(
        "organization_id", flat=True
    )
    if not org_ids:
        return False
    return await (
        Permissions.filter(
            resource_id=resource_id,
            resource_type=resource_type,
            granted_to_organization_id__in=list(org_ids),
            status="active",
        )
        .filter(Q(expires_at__isnull=True) | Q(expires_at__gt=now))
        .exists()
    )


async def _file_row_accessible(row: dict[str, Any], *, user_id: str) -> bool:
    """Python-side equivalent of ``file_row_access_predicate`` (owner / org
    membership / published_to_web / direct grant / folder-inherited grant),
    evaluated over an already-fetched ``files.files`` row dict."""
    if row["created_by"] is not None and str(row["created_by"]) == user_id:
        return True
    if is_published(row):
        return True
    if row["organization_id"] is not None:
        Memberships = get_db_model("Memberships")
        if await Memberships.exists(
            organization_id=row["organization_id"],
            user_id=user_id,
            container_type="organization",
            status="active",
            deleted_at__isnull=True,
        ):
            return True
    if await _has_active_grant(resource_id=row["id"], resource_type="file", user_id=user_id):
        return True
    if row["parent_folder_id"] is not None and await _has_active_grant(
        resource_id=row["parent_folder_id"], resource_type="folder", user_id=user_id
    ):
        return True
    return False


async def _resolve_cld_file(
    file_id: str, field_id: str | None, *, user_id: str
) -> ResolvedSource | None:
    """Resolve an accessible cloud text file to its canonical text body.

    ACL: fail-closed — the caller must be able to SEE the file, mirroring the
    cld_file branches of ``search._build_visibility_clause``: owner, member of
    the file's org, direct ``iam.permissions`` grant, folder-inherited grant,
    or published_to_web. A row the caller cannot see is indistinguishable
    from one that doesn't exist (P0-11 cross-tenant exfiltration fix). The
    share-aware predicate (vs owner-only) keeps the K2/K3 file-centric ingest
    endpoint working for write-granted non-owners — that endpoint enforces
    WRITE via the PermissionsManager before calling ingest; this layer only
    guarantees the caller isn't ingesting a file they have no access to at
    all. Note: files.files uses ``created_by`` as the owner column.

    ``metadata.text`` remains a zero-I/O fast path for pre-extracted callers.
    Normal uploads do not duplicate their body into metadata, so the fallback
    resolves bytes through the host-injected canonical FileManager. The row
    ACL above runs first; the explicit system-file marker only authorizes the
    already-checked server-side byte read when this resolver runs in a
    background worker without a request context.
    """
    Files = get_db_model("Files")
    rows = await Files.filter(id=file_id, deleted_at__isnull=True).values(
        "id",
        "created_by",
        "organization_id",
        "file_path",
        "file_name",
        "mime_type",
        "storage_uri",
        "metadata",
        "published_to_web",
        "parent_folder_id",
    )
    row = rows[0] if rows else None
    if row is None:
        return None
    if not await _file_row_accessible(row, user_id=user_id):
        return None

    mime_type = normalize_mime(row["mime_type"])
    if mime_type not in TEXT_MIMES:
        # The row exists and is owned by the caller, but the TEXT resolver has
        # no extraction path for this MIME. Two very different cases:
        #
        #  1. A binary we DO handle (PDF / image). ``ingest_source`` dispatches
        #     it to the dedicated pipeline before ever calling this resolver —
        #     but ``auto_ingest`` pre-resolves here for change-detection and
        #     cost-estimation, so it lands on us anyway. That is NORMAL. Raise
        #     the typed error (the caller defers to the binary dispatch) and say
        #     NOTHING loud: screaming "no extraction pipeline wired" at a file
        #     whose pipeline is about to run is a lie, and it trained everyone
        #     to ignore the banner.
        #  2. Genuinely unwired (audio, .xlsx, .docx). That deserves a typed,
        #     user-visible rejection rather than a silent ``None`` that would
        #     leave the document at ``status='pending'`` forever. It is not an
        #     operational ERROR: a user selecting an unsupported format must
        #     not contaminate the production error patrol.
        pipeline = classify_binary_pipeline(mime_type, row["file_name"])
        if pipeline:
            raise UnsupportedMimeError(
                source_kind="cld_file",
                source_id=str(row["id"]),
                mime_type=mime_type,
                file_name=row["file_name"],
                hint=f"Handled by the {pipeline} pipeline — not by the text resolver.",
                binary_pipeline=True,
            )
        vcprint(
            data={
                "source_kind": "cld_file",
                "source_id": str(row["id"]),
                "file_name": row["file_name"],
                "mime_type": mime_type,
                "supported": [*sorted(TEXT_MIMES), "application/pdf", "image/*"],
            },
            title="RAG INGEST — UNSUPPORTED MIME (no extraction pipeline wired)",
            color="yellow",
            pretty=True,
        )
        raise UnsupportedMimeError(
            source_kind="cld_file",
            source_id=str(row["id"]),
            mime_type=mime_type,
            file_name=row["file_name"],
        )

    metadata = _coerce_jsonb(row["metadata"]) or {}
    text_source = "metadata"
    # Allow callers / pre-processors to attach extracted text to
    # cld_files.metadata.text. Avoids a needless storage round-trip.
    if isinstance(metadata.get("text"), str):
        text = metadata["text"]
    else:
        text_source = "file_bytes"
        fm = get_cloud_file_manager()
        with system_file_access("rag-ingest-text"):
            resolved_media = await fm.resolve_media_async(
                MediaRef(file_id=str(row["id"])), needs_bytes=True
            )
        if resolved_media is None:
            raise RuntimeError(
                f"cloud file resolver returned no result for text file {row['id']}"
            )
        if resolved_media.resolver_error:
            raise RuntimeError(
                "cloud file resolver failed for text file "
                f"{row['id']}: {resolved_media.resolver_error}"
            )
        if resolved_media.base64_data is None:
            raise RuntimeError(
                f"cloud file resolver returned no bytes for text file {row['id']}"
            )
        try:
            body = base64.b64decode(resolved_media.base64_data, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise RuntimeError(
                f"cloud file resolver returned invalid bytes for text file {row['id']}"
            ) from exc
        try:
            text = body.decode("utf-8-sig")
        except UnicodeDecodeError:
            logger.warning(
                "RAG text-file decode replaced invalid UTF-8 bytes: file_id=%s file_name=%s",
                row["id"],
                row["file_name"],
            )
            text = body.decode("utf-8-sig", errors="replace")
    return ResolvedSource(
        source_kind="cld_file",
        source_id=str(row["id"]),
        field_id=field_id,
        owner_id=str(row["created_by"]),
        organization_id=str(row["organization_id"]) if row["organization_id"] else None,
        text=text,
        mime_type=mime_type,
        language=None,
        source_hash=_hash(text),
        metadata={
            "file_path": row["file_path"],
            "file_name": row["file_name"],
            "storage_uri": row["storage_uri"],
            "text_source": text_source,
            "row_metadata": metadata,
        },
    )


async def _resolve_library_doc(doc_id: str) -> ResolvedSource | None:
    LibraryDocs = get_db_model("LibraryDocs")
    ProcessedDocuments = get_db_model("ProcessedDocuments")
    # use_cache=False — an upsert immediately followed by ingest must see the fresh row.
    doc = await LibraryDocs.get_or_none(use_cache=False, id=doc_id, deleted_at__isnull=True)
    if doc is None:
        return None
    # The words live on the doc's SOURCE (``inline``, canonical identity ``library_doc:<id>``,
    # landed 2026-10-07), never on ``rag.library_docs.body`` — that column is archived and empty
    # (guard: tests/test_library_doc_body_is_never_read.py). A binary library doc has no Source
    # here: it goes through the cld_file path (``ingest_library_pdf``).
    sources = await ProcessedDocuments.filter(
        canonical_identity=f"library_doc:{doc_id}", deleted_at__isnull=True
    ).order_by("-created_at").limit(1).values("content")
    text = str((sources[0].get("content") if sources else None) or "")
    if not text.strip():
        return None
    title_prefix = doc.title
    if doc.short_code:
        title_prefix = f"{doc.short_code} — {doc.title}"
    full_text = f"{title_prefix}\n\n{text}".strip()
    return ResolvedSource(
        source_kind="library_doc",
        source_id=str(doc.id),
        field_id=None,
        # System-owned: stamp owner_id to the org's first member, or fall
        # back to a sentinel system uuid. We resolve owner_id in the
        # ingest helper rather than guessing here.
        owner_id="00000000-0000-0000-0000-000000000000",
        # NOT NULL since migration 0167 (NO NULL ORG, db-rules §2) — global docs
        # carry the system org, so this is always a real org id now.
        organization_id=str(doc.organization_id) if doc.organization_id else None,
        text=full_text,
        mime_type="text/markdown",
        language=None,
        source_hash=_hash(full_text),
        metadata={
            "title": doc.title,
            "short_code": doc.short_code,
            "kind": doc.kind,
            "jurisdiction": doc.jurisdiction,
            # `doc_version` is the EDITION string ("2020-Edition"); the column was
            # renamed off `version` in migration 0167 because `version` is the
            # canonical integer `platform._touch_row` bumps (db-rules §1a). The
            # chunk-metadata KEY stays "version" — it is the retrieval vocabulary,
            # not a column name, and renaming it would invalidate live chunks.
            "version": doc.doc_version,
            "effective_from": doc.effective_from.isoformat() if doc.effective_from else None,
            "effective_to": doc.effective_to.isoformat() if doc.effective_to else None,
            "source_url": doc.source_url,
            "row_metadata": _coerce_jsonb(doc.metadata),
        },
    )


async def _resolve_transcript(transcript_id: str, *, user_id: str) -> ResolvedSource | None:
    """Flatten a transcript's segments into one searchable document.

    ACL: ONE answer — ``iam.has_access_for(user, 'transcript', id, 'viewer')``
    (``matrx_orm.platform_access_check``). A row the person cannot reach is
    indistinguishable from a row that doesn't exist (no leak). Never
    ``created_by == user``: a public video's ONE shared transcript is owned by the
    system principal and every organization reads it (social-media-unification).

    Body shape: ``title\n\n[description?]\n\n[speaker?] text…`` joined per
    segment. Segments without ``text`` are skipped.
    """
    from matrx_orm import platform_access_check

    if not await platform_access_check(str(user_id), "transcript", str(transcript_id), "viewer"):
        return None
    Transcripts = get_db_model("Transcripts")
    rows = await (
        Transcripts.filter(id=transcript_id)
        .filter(deleted_at__isnull=True)
        .filter(Q(is_draft=False) | Q(is_draft__isnull=True))
        .values(
            "id",
            "created_by",
            "organization_id",
            "title",
            "description",
            "segments",
            "folder_name",
            "tags",
            "source_type",
            "metadata",
        )
    )
    row = rows[0] if rows else None
    if row is None:
        return None
    row = {
        **row,
        "title": row["title"] or "",
        "description": row["description"] or "",
        "folder_name": row["folder_name"] or "",
        "source_type": row["source_type"] or "",
    }

    # Flatten segments. Each segment is a dict with at least ``text``;
    # may also carry ``speaker`` / ``timecode`` we want to preserve so the
    # FE can render speaker labels and click-to-seek.
    segments = row["segments"]
    if isinstance(segments, str):
        import json

        try:
            segments = json.loads(segments)
        except Exception:
            segments = []
    if not isinstance(segments, list):
        segments = []
    lines: list[str] = []
    for seg in segments:
        if not isinstance(seg, dict):
            continue
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        speaker = (seg.get("speaker") or "").strip()
        if speaker and speaker.lower() != "unknown":
            lines.append(f"{speaker}: {text}")
        else:
            lines.append(text)
    body = "\n".join(lines)

    header_parts = [row["title"]]
    if row["description"]:
        header_parts.append(row["description"])
    full_text = ("\n\n".join(p for p in header_parts if p) + "\n\n" + body).strip()

    return ResolvedSource(
        source_kind="transcript",
        source_id=str(row["id"]),
        field_id=None,
        owner_id=str(row["created_by"]),
        organization_id=str(row["organization_id"]) if row["organization_id"] else None,
        text=full_text,
        mime_type="text/markdown",
        language=None,
        source_hash=_hash(full_text),
        metadata={
            "title": row["title"],
            "folder": row["folder_name"],
            "tags": list(row["tags"] or []),
            "source_type": row["source_type"],
            "segment_count": len(lines),
            "row_metadata": _coerce_jsonb(row["metadata"]),
        },
    )


async def _resolve_scraped(page_id: str, *, user_id: str) -> ResolvedSource | None:
    """A single scraped page (``scraper.scrape_parsed_page``).

    ACL: a scraped page belongs to a person only when it is shown to that person
    alone (``shown_to = 'only_me'``) and its ``created_by`` is ``user_id``. Any
    other row (the organization's, system-scraped) has no owner
    and is intentionally NOT returned here; the ingestion path runs per-user
    and must not pull system-owned content into a user's index. (The legacy
    ``owner_id`` / ``user_id`` / ``is_public`` columns are retired — never read
    them.)

    Body: ``content.raw_text`` (jsonb) when present, falling back to a
    URL-only manifest when the parser only stored headers. We do NOT
    fetch remote bytes here — the scraper writes the parsed body into
    ``content`` already; if it's missing, the page hasn't been parsed.
    """
    ScrapeParsedPage = get_db_model("ScrapeParsedPage")
    rows = await ScrapeParsedPage.filter(
        id=page_id, created_by=user_id, shown_to="only_me"
    ).values(
        "id", "created_by", "url", "domain", "page_name", "content", "content_type", "scraped_at"
    )
    row = rows[0] if rows else None
    if row is None:
        return None

    content = _coerce_jsonb(row["content"]) or {}
    raw_text = ""
    if isinstance(content.get("raw_text"), str):
        raw_text = content["raw_text"]
    elif isinstance(content.get("text"), str):
        raw_text = content["text"]

    url = row["url"] or ""
    page_name = row["page_name"] or ""
    header = f"{page_name}\n{url}".strip()
    full_text = (header + "\n\n" + raw_text).strip()
    if not raw_text.strip():
        # No body to index — return None so the workflow tombstones the
        # job rather than writing an empty (header-only) chunk.
        return None

    return ResolvedSource(
        source_kind="scraped",
        source_id=str(row["id"]),
        field_id=None,
        owner_id=str(row["created_by"]),
        organization_id=None,
        text=full_text,
        mime_type="text/html" if (row["content_type"] or "").lower() == "html" else "text/plain",
        language=None,
        source_hash=_hash(full_text),
        metadata={
            "url": url,
            "domain": row["domain"],
            "page_name": page_name,
            "content_type": row["content_type"],
            "scraped_at": row["scraped_at"].isoformat() if row["scraped_at"] else None,
        },
    )


async def _source_version_text(processed_document_id: str) -> str:
    """One Source version's text: its portions in order, cleaned text where cleaning produced some."""
    ProcessedDocumentPages = get_db_model("ProcessedDocumentPages")
    pages = await (
        ProcessedDocumentPages.filter(processed_document_id=processed_document_id)
        .order_by("page_number")
        .values("raw_text", "cleaned_text")
    )
    parts = [str(p["cleaned_text"] or "") if str(p["cleaned_text"] or "").strip() else str(p["raw_text"] or "") for p in pages]
    return "\n\n".join(t for t in parts if t.strip()).strip()


async def _resolve_research(source_id: str, *, user_id: str) -> ResolvedSource | None:
    """A single research source (``research.rs_source``) + its scraped body.

    Schema chain:
      * ``rs_source``  — per-source metadata (url, title, description, topic_id).
        Has NO owner column of its own.
      * ``rs_topic``   — the research project that owns the source. Ownership is
        ``rs_topic.created_by`` (the only user link in the research schema); no
        ``organization_id`` exists, so org is resolved at the ingest boundary
        (personal-org default), exactly like ``scraped`` / ``cx_message``.
      * ``rs_content`` — the scraped page body, versioned. We read the CURRENT
        version (``is_current = true``) and take ``content`` (LLM/cleaned) falling
        back to ``original_content`` (raw scrape).

    ACL: fail-closed on ``rs_topic.created_by = user_id`` so a source whose topic
    we do NOT own is indistinguishable from one that doesn't exist (P0-11
    cross-tenant exfiltration fix). A source whose topic has a NULL ``created_by``
    is never returned (it cannot satisfy the ownership contract).

    Body: ``title``/``description`` header + the scraped body. A source with no
    current body row (scrape skipped / failed / pending) returns None so the
    workflow tombstones the job rather than indexing a header-only chunk — the
    bulk of the ~2k corpus is metadata-only and is intentionally skipped until
    its page is scraped.
    """
    RsSource = get_db_model("RsSource")
    RsTopic = get_db_model("RsTopic")
    RsContent = get_db_model("RsContent")

    sources = await RsSource.filter(id=source_id).values(
        "id", "topic_id", "title", "description", "url", "hostname", "source_type"
    )
    source = sources[0] if sources else None
    if source is None:
        return None

    # ``t.created_by = $2`` was originally applied as a JOIN condition — a
    # topic with a NULL created_by (or one owned by someone else) simply
    # fails to match, exactly like this filtered fetch returning no topic.
    topics = await RsTopic.filter(id=source["topic_id"], created_by=user_id).values("created_by")
    topic = topics[0] if topics else None
    if topic is None:
        return None

    # LEFT JOIN rs_content ON source_id = s.id AND is_current = true — a
    # missing current-content row means an empty body, matching the original
    # COALESCE(c.content, c.original_content, '') over a NULL-joined row.
    contents = await RsContent.filter(source_id=source["id"], is_current=True).values(
        "content", "original_content", "processed_document_id"
    )
    content_row = contents[0] if contents else None
    body = ""
    if content_row is not None:
        body = (content_row["content"] or content_row["original_content"] or "").strip()
        if not body and content_row.get("processed_document_id"):
            # A landed capture's words live on its Source only (2026-10-07): read that version.
            body = await _source_version_text(str(content_row["processed_document_id"]))
    if not body:
        # Metadata-only source (page not scraped / scrape failed). Nothing to
        # index — return None so the job tombstones cleanly rather than
        # writing a header-only chunk.
        return None

    title = source["title"] or ""
    description = source["description"] or ""
    source_type = source["source_type"] or ""

    header_parts = [title]
    if description:
        header_parts.append(description)
    if source["url"]:
        header_parts.append(source["url"])
    header = "\n".join(p for p in header_parts if p)
    full_text = ((header + "\n\n" if header else "") + body).strip()

    return ResolvedSource(
        source_kind="research",
        source_id=str(source["id"]),
        field_id=None,
        owner_id=str(topic["created_by"]),
        # No org on the research schema — the ingest boundary resolves the
        # effective org (personal-org default) before writing kg_chunks.
        organization_id=None,
        text=full_text,
        mime_type="text/markdown",
        language=None,
        source_hash=_hash(full_text),
        metadata={
            "title": title,
            "url": source["url"],
            "hostname": source["hostname"],
            "source_type": source_type,
            "topic_id": str(source["topic_id"]),
        },
    )


async def _resolve_repository(repo_id: str, *, user_id: str) -> ResolvedSource | None:
    """A code-repository manifest (``code.code_repositories``).

    The repo's *files* are ingested as their own ``code_file`` rows; this
    resolver indexes the repo's own description / git pointer / sync
    status so a search for "the foo repo" surfaces a hit for the repo
    itself, not just one of its files.

    ACL: filter on ``created_by`` so a repo we don't own is invisible.

    NOTE (schema-drift fix): the raw SQL this replaced filtered on a
    ``code.code_repositories.user_id`` column that does not exist on the live
    table (verified against Supabase project brsgrqvjdzwihsvnfqkf,
    2026-07-11) — the table's owner column is ``created_by``, exactly like
    every other resolver in this module. That raw query would have raised
    ``UndefinedColumnError`` the first time this branch actually executed;
    the ORM conversion fixes the drift as part of the port.
    """
    CodeRepositories = get_db_model("CodeRepositories")
    rows = await CodeRepositories.filter(id=repo_id, created_by=user_id, is_active=True).values(
        "id",
        "created_by",
        "organization_id",
        "name",
        "description",
        "git_url",
        "git_branch",
        "git_provider",
        "git_commit_sha",
        "sync_status",
        "metadata",
    )
    row = rows[0] if rows else None
    if row is None:
        return None

    name = row["name"] or ""
    description = row["description"] or ""
    lines = [name]
    if description:
        lines.append(description)
    if row["git_url"]:
        lines.append(
            f"Repository URL: {row['git_url']} "
            f"(branch: {row['git_branch'] or 'main'}, "
            f"provider: {row['git_provider'] or 'unknown'})"
        )
    if row["git_commit_sha"]:
        lines.append(f"Commit: {row['git_commit_sha']}")
    full_text = "\n\n".join(p for p in lines if p).strip()
    if not full_text:
        return None

    return ResolvedSource(
        source_kind="repository",
        source_id=str(row["id"]),
        field_id=None,
        owner_id=str(row["created_by"]),
        organization_id=str(row["organization_id"]) if row["organization_id"] else None,
        text=full_text,
        mime_type="text/markdown",
        language=None,
        source_hash=_hash(full_text),
        metadata={
            "name": name,
            "git_url": row["git_url"],
            "git_branch": row["git_branch"],
            "git_provider": row["git_provider"],
            "git_commit_sha": row["git_commit_sha"],
            "sync_status": row["sync_status"],
            "row_metadata": _coerce_jsonb(row["metadata"]),
        },
    )


async def _resolve_task(task_id: str, *, user_id: str) -> ResolvedSource | None:
    """A single task row (``projects.tasks``).

    Ownership is ``projects.tasks.created_by`` — we filter on it inside the SQL
    so a task we do NOT own is indistinguishable from one that doesn't exist
    (fail-closed, no cross-tenant leak). The ingestable body is composed
    from the meaningful text columns: ``title`` (always present) +
    ``description`` (optional). ``status`` / ``priority`` are recorded in
    metadata for search filters but are NOT part of the embedded body —
    they carry no semantic content a user would search by.
    """
    Tasks = get_db_model("Tasks")
    rows = await Tasks.filter(id=task_id, created_by=user_id, deleted_at__isnull=True).values(
        "id", "created_by", "organization_id", "project_id", "title", "description", "status", "priority", "due_date"
    )
    row = rows[0] if rows else None
    if row is None:
        return None

    title = row["title"] or ""
    description = row["description"] or ""
    status = row["status"] or ""
    parts = [title]
    if description:
        parts.append(description)
    full_text = "\n\n".join(p for p in parts if p).strip()
    if not full_text:
        return None

    # ``priority::text`` in the original SQL — EnumField values are already
    # plain strings on read; str() covers both the enum and a None.
    priority = str(row["priority"]) if row["priority"] is not None else None

    return ResolvedSource(
        source_kind="task",
        source_id=str(row["id"]),
        field_id=None,
        owner_id=str(row["created_by"]),
        organization_id=str(row["organization_id"]) if row["organization_id"] else None,
        text=full_text,
        mime_type="text/markdown",
        language=None,
        source_hash=_hash(full_text),
        metadata={
            "title": title,
            "status": status,
            "priority": priority,
            "project_id": str(row["project_id"]) if row["project_id"] else None,
            "due_date": row["due_date"].isoformat() if row["due_date"] else None,
        },
    )


async def _resolve_project(project_id: str, *, user_id: str) -> ResolvedSource | None:
    """A single project row (``projects.projects``).

    NOTE: ``projects.projects`` has NO ``user_id`` column — ownership is the
    ``created_by`` column. We filter on it inside the SQL so a project we
    did NOT create is invisible (fail-closed). The ingestable body is
    ``name`` (NOT NULL) + ``description`` (optional). ``owner_id`` on the
    ResolvedSource is stamped from ``created_by`` so the kg_chunks ACL is
    consistent with every other source kind (owner == the creating user).
    """
    Projects = get_db_model("Projects")
    rows = await Projects.filter(id=project_id, created_by=user_id).values(
        "id", "created_by", "organization_id", "name", "description", "slug"
    )
    row = rows[0] if rows else None
    if row is None:
        return None
    if not row["created_by"]:
        # A project with a NULL created_by can't satisfy the ownership
        # contract — refuse rather than stamp a None owner on kg_chunks.
        return None

    name = row["name"] or ""
    description = row["description"] or ""
    slug = row["slug"] or ""
    parts = [name]
    if description:
        parts.append(description)
    full_text = "\n\n".join(p for p in parts if p).strip()
    if not full_text:
        return None

    return ResolvedSource(
        source_kind="project",
        source_id=str(row["id"]),
        field_id=None,
        owner_id=str(row["created_by"]),
        organization_id=str(row["organization_id"]) if row["organization_id"] else None,
        text=full_text,
        mime_type="text/markdown",
        language=None,
        source_hash=_hash(full_text),
        metadata={
            "name": name,
            "slug": slug,
        },
    )


def _human_authored_message_text(row: dict) -> str:
    """What the HUMAN actually said on one stored message row (D327).

    This is the ONLY text reader for `chat.message` in this package. The
    raw-payload reader it replaced (``_extract_message_text``) flattened
    ``content`` for every role; on a ``role='user'`` row ``content`` is the
    complete provider payload — the agent definition's seeded opening turn +
    resolved launch variables + what the person typed — so a retrieved chunk
    could quote a template or a host-injected notice back as her words.

    Applies the host-injected authorship projection (aidream injects
    ``matrx_ai.config.human_authored_text``; unconfigured hosts get the
    package's own implementation of the same rule) to the row's decoded
    ``role`` / ``content`` / ``user_content``. A user row whose
    ``user_content`` is present but empty means the person wrote nothing —
    the turn was authored by the host — and projects to "", which every
    caller here drops.

    The row's ``user_content`` key may be absent entirely (a caller that
    did not select it); that is treated as SQL NULL, i.e. "predates the
    authorship contract", exactly as the projection defines.
    """
    projection = get_human_authored_text()
    text = projection(
        row.get("role"),
        decode_content_blocks(row.get("content")),
        decode_content_blocks(row.get("user_content")),
    )
    return text.strip() if isinstance(text, str) else ""


#: The one ``field_id`` a conversation is indexed under: what the person typed.
TYPED_FIELD = "typed"


async def _person_turns(Message: Any, conversation_id: str) -> list[str]:
    """The person's own messages in one conversation, in order (D327 projection, model-visible
    rows only). Assistant, system and tool rows are never read."""
    rows = await (
        Message.filter(conversation_id=conversation_id, is_visible_to_model=True, role="user")
        .order_by("created_at")
        .values("role", "content", "user_content")
    )
    return [t for t in (_human_authored_message_text(r) for r in rows) if t]


async def _agent_defaults(agent_id: Any) -> dict[str, str]:
    from matrx_rag.chat_authorship import declared_defaults

    if not agent_id:
        return {}
    Definition = get_db_model("Definition", schema="agent")
    rows = await Definition.filter(id=agent_id).values("variable_definitions")
    return declared_defaults(rows[0]["variable_definitions"]) if rows else {}


async def _other_runs(
    Conversation: Any, Message: Any, *, agent_id: Any, user_id: str, exclude_id: str, limit: int
) -> list[set[str]]:
    """One set of typed lines per other recent run of the same agent by the same person."""
    from matrx_rag.chat_authorship import lines_of, variable_values

    if not agent_id or limit <= 0:
        return []
    convs = await (
        Conversation.filter(initial_agent_id=agent_id, created_by=user_id, deleted_at__isnull=True)
        .exclude(id=exclude_id)
        .order_by("-created_at")
        .limit(limit)
        .values("id", "variables")
    )
    out: list[set[str]] = []
    for c in convs:
        lines: set[str] = set()
        for _name, value in variable_values(c["variables"]):
            lines.update(lines_of(value))
        for turn in await _person_turns(Message, str(c["id"])):
            lines.update(lines_of(turn))
        out.append(lines)
    return out


async def _resolve_cx_message(source_id: str, *, user_id: str) -> ResolvedSource | None:
    """A conversation as what the PERSON typed — the only way a chat is ever indexed.

    ``source_id`` is a conversation id (a message id resolves to its conversation). The
    conversation must be the caller's own (``created_by``) and the person's own chat by the ONE
    authorship rule (:func:`matrx_rag.chat_authorship.conversation_skip_reason` over the host's
    :class:`TypedChatPolicy`): a coding-session mirror, a sub-agent fork, an agent / workflow /
    scheduled / mandate run, an automation, or an opted-out chat resolves to nothing.

    The body is the person's own messages (the D327 projection of ``role='user'`` rows, model-
    visible only) plus the variable values they entered, minus values equal to the agent's
    declared defaults and minus lines repeated verbatim across the policy's
    ``template_repeat_runs`` runs of the same agent. Assistant replies, system prompts and
    attached context are never read.

    RETIRED 2026-10-25: the whole-transcript path (``field_id`` NULL, ``"<role>: <text>"`` for
    every role, assistant replies included) and the per-message path. A NULL ``field_id``
    resolves exactly like ``"typed"`` and the result always carries ``field_id="typed"``, so a
    re-enabled save hook can never index a reply.
    """
    from matrx_rag._ext import get_typed_chat_policy
    from matrx_rag.chat_authorship import (
        CONVERSATION_AUTHORSHIP_COLUMNS,
        conversation_skip_reason,
        typed_parts,
    )

    Conversation = get_db_model("Conversation")
    Message = get_db_model("Message")
    columns = (*CONVERSATION_AUTHORSHIP_COLUMNS, "created_by", "organization_id", "variables", "initial_agent_id")
    convs = await Conversation.filter(id=source_id, created_by=user_id, deleted_at__isnull=True).values(*columns)
    if not convs:
        msgs = await Message.filter(id=source_id).values("conversation_id")
        if not msgs:
            return None
        convs = await Conversation.filter(
            id=msgs[0]["conversation_id"], created_by=user_id, deleted_at__isnull=True
        ).values(*columns)
        if not convs:
            return None
    conv = convs[0]
    policy = await get_typed_chat_policy()
    if conversation_skip_reason(conv, policy) is not None:
        return None
    conv_id = str(conv["id"])
    agent_id = conv.get("initial_agent_id")
    kept, dropped = typed_parts(
        turns=await _person_turns(Message, conv_id),
        variables=conv.get("variables"),
        defaults=await _agent_defaults(agent_id),
        other_runs=await _other_runs(
            Conversation,
            Message,
            agent_id=agent_id,
            user_id=user_id,
            exclude_id=conv_id,
            limit=policy.template_scan_runs,
        ),
        repeat_runs=policy.template_repeat_runs,
    )
    full_text = "\n".join(kept).strip()
    if not full_text:
        return None
    title = (conv.get("title") or "").strip() or "Conversation"
    return ResolvedSource(
        source_kind="cx_message",
        source_id=conv_id,
        field_id=TYPED_FIELD,
        owner_id=str(conv["created_by"]),
        organization_id=str(conv["organization_id"]) if conv["organization_id"] else None,
        text=full_text,
        mime_type="text/plain",
        language=None,
        source_hash=_hash(full_text),
        metadata={
            "title": title,
            "typed_lines": len(kept),
            "dropped_default_values": dropped["default_value"],
            "dropped_template_lines": dropped["template_line"],
        },
    )


def _canvas_strings(value: object, out: list[str], depth: int = 0) -> None:
    """Every string a canvas ``content`` holds, in order (``metadata`` keys skipped)."""
    if depth > 12:
        return
    if isinstance(value, str):
        text = value.strip()
        if text:
            out.append(text)
    elif isinstance(value, dict):
        for k, v in value.items():
            if k in ("metadata", "type", "id", "style", "styles", "className"):
                continue
            _canvas_strings(v, out, depth + 1)
    elif isinstance(value, list):
        for v in value:
            _canvas_strings(v, out, depth + 1)


async def _resolve_canvas_item(canvas_id: str, *, user_id: str) -> ResolvedSource | None:
    """One canvas item (``canvas.canvas_items``): title + description + every string its
    ``content`` carries (tables, cards, diagrams' text). Owner-only (``created_by``), live rows
    only. Chunks of this kind have no kernel token in search, so they reach their creator only."""
    CanvasItems = get_db_model("CanvasItems")
    rows = await CanvasItems.filter(id=canvas_id, created_by=user_id, deleted_at__isnull=True).values(
        "id", "created_by", "organization_id", "title", "description", "type", "content",
        "conversation_id", "source_type",
    )
    row = rows[0] if rows else None
    if row is None:
        return None
    parts: list[str] = []
    for head in (row["title"], row["description"]):
        if head and str(head).strip():
            parts.append(str(head).strip())
    content = row["content"]
    if isinstance(content, str):
        import json

        try:
            content = json.loads(content)
        except ValueError:
            pass
    _canvas_strings(content, parts)
    full_text = "\n\n".join(parts).strip()
    if not full_text:
        return None
    return ResolvedSource(
        source_kind="canvas_item",
        source_id=str(row["id"]),
        field_id=None,
        owner_id=str(row["created_by"]),
        organization_id=str(row["organization_id"]) if row["organization_id"] else None,
        text=full_text,
        mime_type="text/markdown",
        language=None,
        source_hash=_hash(full_text),
        metadata={
            "title": (row["title"] or "").strip(),
            "canvas_type": row["type"],
            "conversation_id": str(row["conversation_id"]) if row["conversation_id"] else None,
            "source_type": row["source_type"],
        },
    )


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _coerce_jsonb(value: object) -> dict[str, object]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        # asyncpg can return jsonb as str when no codec registered.
        import json

        try:
            decoded = json.loads(value)
            return decoded if isinstance(decoded, dict) else {}
        except Exception:
            return {}
    return {}


_LANG_TO_MIME = {
    "python": "text/x-python",
    "typescript": "text/x-typescript",
    "javascript": "text/x-javascript",
    "tsx": "text/x-typescript",
    "jsx": "text/x-javascript",
    "go": "text/x-go",
    "java": "text/x-java",
    "rust": "text/x-rust",
    "c": "text/x-c",
    "cpp": "text/x-c++",
    "json": "application/json",
    "yaml": "application/yaml",
    "markdown": "text/markdown",
    "plaintext": "text/plain",
}


def _mime_for_language(language: str | None) -> str:
    if not language:
        return "text/plain"
    return _LANG_TO_MIME.get(language.lower(), "text/plain")


__all__ = [
    "ResolvedSource",
    "SourceKind",
    "TEXT_MIMES",
    "normalize_mime",
    "UnsupportedMimeError",
    "resolve",
]
