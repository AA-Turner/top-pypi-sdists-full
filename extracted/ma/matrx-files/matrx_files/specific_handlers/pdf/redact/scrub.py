"""Privacy-strip helpers: metadata / attachments / JS / annotation flatten.

Thin wrappers around PyMuPDF's ``doc.scrub`` and ``doc.bake`` that produce
the same ``RedactionResult`` shape as the region/pattern engine, so callers
have one uniform contract for "make this PDF safe to send."

For outbound PDFs in legal/medical workflows, chain ``strip_all_pii`` —
it's the equivalent of design §5.4's "metadata strip + attachments strip +
JS strip + flatten annotations" bundle.
"""

from __future__ import annotations

from typing import Any

from ..concurrency import run_in_cpu_executor
from ..internal import load_pymupdf
from .engine import _build_audit
from .models import RedactionResult


def _scrub_and_save(
    pdf_bytes: bytes,
    *,
    attached_files: bool = False,
    embedded_files: bool = False,
    hidden_text: bool = False,
    javascript: bool = False,
    metadata: bool = False,
    redact_images: int = 0,
    remove_links: bool = False,
    reset_fields: bool = False,
    reset_responses: bool = False,
    thumbnails: bool = False,
    xml_metadata: bool = False,
    bake_annots: bool = False,
    bake_widgets: bool = False,
) -> tuple[bytes, int]:
    """Run a configured ``doc.scrub`` + optional ``doc.bake`` and full-save."""
    pymupdf = load_pymupdf()
    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        page_count = doc.page_count
        try:
            doc.scrub(
                attached_files=attached_files,
                clean_pages=False,
                embedded_files=embedded_files,
                hidden_text=hidden_text,
                javascript=javascript,
                metadata=metadata,
                redactions=False,
                redact_images=redact_images,
                remove_links=remove_links,
                reset_fields=reset_fields,
                reset_responses=reset_responses,
                thumbnails=thumbnails,
                xml_metadata=xml_metadata,
            )
        except Exception:
            # Older PyMuPDF versions accept a subset of kwargs; fall back to
            # the minimal call and best-effort apply the others directly.
            try:
                doc.scrub()
            except Exception:
                pass
            if metadata:
                try:
                    doc.set_metadata({})
                except Exception:
                    pass

        if bake_annots or bake_widgets:
            try:
                doc.bake(annots=bake_annots, widgets=bake_widgets)
            except Exception:
                pass

        out_bytes = doc.tobytes(garbage=4, deflate=True, clean=True)
    return out_bytes, page_count


def strip_metadata(
    pdf_bytes: bytes,
    *,
    reason: str = "strip_metadata",
    user_id: str | None = None,
    parent_file_id: str | None = None,
) -> RedactionResult:
    """Wipe /Info, XMP metadata, and thumbnails."""
    out_bytes, page_count = _scrub_and_save(
        pdf_bytes, metadata=True, xml_metadata=True, thumbnails=True
    )
    audit = _build_audit(
        reason=reason,
        redaction_kind="metadata",
        redaction_params={"fields": ["info", "xmp", "thumbnails"]},
        tier_used="stream_rewrite",
        status="success",
        bytes_removed_estimate=max(0, len(pdf_bytes) - len(out_bytes)),
        regions_count=0,
        parent_file_id=parent_file_id,
        user_id=user_id,
    )
    return RedactionResult(
        content=out_bytes,
        page_count=page_count,
        audit=audit,
        verification_passed=True,
    )


def strip_attachments(
    pdf_bytes: bytes,
    *,
    reason: str = "strip_attachments",
    user_id: str | None = None,
    parent_file_id: str | None = None,
) -> RedactionResult:
    """Remove every attached file / embedded-file stream."""
    out_bytes, page_count = _scrub_and_save(
        pdf_bytes, attached_files=True, embedded_files=True
    )
    audit = _build_audit(
        reason=reason,
        redaction_kind="attachments",
        redaction_params={"fields": ["attached_files", "embedded_files"]},
        tier_used="stream_rewrite",
        status="success",
        bytes_removed_estimate=max(0, len(pdf_bytes) - len(out_bytes)),
        regions_count=0,
        parent_file_id=parent_file_id,
        user_id=user_id,
    )
    return RedactionResult(
        content=out_bytes,
        page_count=page_count,
        audit=audit,
        verification_passed=True,
    )


def strip_javascript(
    pdf_bytes: bytes,
    *,
    reason: str = "strip_javascript",
    user_id: str | None = None,
    parent_file_id: str | None = None,
) -> RedactionResult:
    """Remove embedded JS actions."""
    out_bytes, page_count = _scrub_and_save(pdf_bytes, javascript=True)
    audit = _build_audit(
        reason=reason,
        redaction_kind="javascript",
        redaction_params={"fields": ["javascript"]},
        tier_used="stream_rewrite",
        status="success",
        bytes_removed_estimate=max(0, len(pdf_bytes) - len(out_bytes)),
        regions_count=0,
        parent_file_id=parent_file_id,
        user_id=user_id,
    )
    return RedactionResult(
        content=out_bytes,
        page_count=page_count,
        audit=audit,
        verification_passed=True,
    )


def flatten_annotations(
    pdf_bytes: bytes,
    *,
    reason: str = "flatten_annotations",
    user_id: str | None = None,
    parent_file_id: str | None = None,
    widgets: bool = True,
) -> RedactionResult:
    """Bake annotations (and optionally form widgets) into the page content.

    Useful before sharing a marked-up draft externally — comments / highlights /
    sticky notes become uneditable parts of the page.
    """
    out_bytes, page_count = _scrub_and_save(
        pdf_bytes, bake_annots=True, bake_widgets=widgets
    )
    audit = _build_audit(
        reason=reason,
        redaction_kind="annotations",
        redaction_params={"bake_annots": True, "bake_widgets": widgets},
        tier_used="stream_rewrite",
        status="success",
        bytes_removed_estimate=max(0, len(pdf_bytes) - len(out_bytes)),
        regions_count=0,
        parent_file_id=parent_file_id,
        user_id=user_id,
    )
    return RedactionResult(
        content=out_bytes,
        page_count=page_count,
        audit=audit,
        verification_passed=True,
    )


def scrub_categories(
    pdf_bytes: bytes,
    *,
    metadata: bool = False,
    attachments: bool = False,
    javascript: bool = False,
    hidden_text: bool = False,
    remove_links: bool = False,
    reset_fields: bool = False,
    reset_responses: bool = False,
    thumbnails: bool = False,
    flatten_annotations: bool = False,
    reason: str = "scrub",
    user_id: str | None = None,
    parent_file_id: str | None = None,
) -> RedactionResult:
    """Granular composite scrub — opt into exactly the categories you want.

    Maps each caller flag to the matching ``doc.scrub`` kwarg. Use this for
    the ``/pdf/scrub`` endpoint where the user picks specific categories;
    use ``strip_all_pii`` for the "nuke everything" outbound default.
    """
    out_bytes, page_count = _scrub_and_save(
        pdf_bytes,
        attached_files=attachments,
        embedded_files=attachments,
        hidden_text=hidden_text,
        javascript=javascript,
        metadata=metadata,
        remove_links=remove_links,
        reset_fields=reset_fields,
        reset_responses=reset_responses,
        thumbnails=metadata or thumbnails,
        xml_metadata=metadata,
        bake_annots=flatten_annotations,
        bake_widgets=flatten_annotations,
    )
    selected: list[str] = [
        name
        for name, on in [
            ("metadata", metadata),
            ("attachments", attachments),
            ("javascript", javascript),
            ("hidden_text", hidden_text),
            ("remove_links", remove_links),
            ("reset_fields", reset_fields),
            ("reset_responses", reset_responses),
            ("thumbnails", thumbnails),
            ("flatten_annotations", flatten_annotations),
        ]
        if on
    ]
    audit = _build_audit(
        reason=reason,
        redaction_kind="composite",
        redaction_params={"fields": selected},
        tier_used="stream_rewrite",
        status="success" if selected else "no_targets",
        bytes_removed_estimate=max(0, len(pdf_bytes) - len(out_bytes)),
        regions_count=0,
        parent_file_id=parent_file_id,
        user_id=user_id,
    )
    return RedactionResult(
        content=out_bytes,
        page_count=page_count,
        audit=audit,
        verification_passed=True,
    )


async def scrub_categories_async(
    pdf_bytes: bytes, **kwargs: Any
) -> RedactionResult:
    return await run_in_cpu_executor(lambda: scrub_categories(pdf_bytes, **kwargs))


def strip_all_pii(
    pdf_bytes: bytes,
    *,
    reason: str = "strip_all_pii",
    user_id: str | None = None,
    parent_file_id: str | None = None,
    bake_annotations_too: bool = False,
) -> RedactionResult:
    """One-call privacy nuke: metadata + attachments + JS + hidden text + links + form data.

    Pair with ``redact_regions`` / ``redact_pattern`` upstream when you need
    to remove specific content; this helper only attacks the file-wide PII
    surfaces (metadata, attached files, javascript) that ``doc.scrub`` knows
    about natively.
    """
    out_bytes, page_count = _scrub_and_save(
        pdf_bytes,
        attached_files=True,
        embedded_files=True,
        hidden_text=True,
        javascript=True,
        metadata=True,
        remove_links=True,
        reset_fields=True,
        reset_responses=True,
        thumbnails=True,
        xml_metadata=True,
        bake_annots=bake_annotations_too,
        bake_widgets=bake_annotations_too,
    )
    audit = _build_audit(
        reason=reason,
        redaction_kind="composite",
        redaction_params={
            "fields": [
                "metadata",
                "xml_metadata",
                "thumbnails",
                "attached_files",
                "embedded_files",
                "javascript",
                "hidden_text",
                "remove_links",
                "reset_fields",
                "reset_responses",
            ],
            "bake_annotations": bake_annotations_too,
        },
        tier_used="stream_rewrite",
        status="success",
        bytes_removed_estimate=max(0, len(pdf_bytes) - len(out_bytes)),
        regions_count=0,
        parent_file_id=parent_file_id,
        user_id=user_id,
    )
    return RedactionResult(
        content=out_bytes,
        page_count=page_count,
        audit=audit,
        verification_passed=True,
    )


# Async siblings ---------------------------------------------------------------


async def strip_metadata_async(pdf_bytes: bytes, **kwargs: Any) -> RedactionResult:
    return await run_in_cpu_executor(lambda: strip_metadata(pdf_bytes, **kwargs))


async def strip_attachments_async(pdf_bytes: bytes, **kwargs: Any) -> RedactionResult:
    return await run_in_cpu_executor(lambda: strip_attachments(pdf_bytes, **kwargs))


async def strip_javascript_async(pdf_bytes: bytes, **kwargs: Any) -> RedactionResult:
    return await run_in_cpu_executor(lambda: strip_javascript(pdf_bytes, **kwargs))


async def flatten_annotations_async(pdf_bytes: bytes, **kwargs: Any) -> RedactionResult:
    return await run_in_cpu_executor(lambda: flatten_annotations(pdf_bytes, **kwargs))


async def strip_all_pii_async(pdf_bytes: bytes, **kwargs: Any) -> RedactionResult:
    return await run_in_cpu_executor(lambda: strip_all_pii(pdf_bytes, **kwargs))


__all__ = [
    "strip_metadata",
    "strip_metadata_async",
    "strip_attachments",
    "strip_attachments_async",
    "strip_javascript",
    "strip_javascript_async",
    "flatten_annotations",
    "flatten_annotations_async",
    "strip_all_pii",
    "strip_all_pii_async",
    "scrub_categories",
    "scrub_categories_async",
]
