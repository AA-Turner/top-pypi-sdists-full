"""Concrete media resolvers. A resolver turns a media item the provider can't
accept into a ``TextContent`` the model CAN read, or signals a clean drop.

Wired today:
  • DOCUMENT (PDF) — extract text via the matrx-utils PDF extractor, capped at a
    'reasonable' length, swap in as text. Real, no model call.

Host-provided resolvers install image, video, and YouTube conversion without making
this standalone package import the host application.
"""

from __future__ import annotations

import asyncio
import base64
from typing import Any

from matrx_ai.config import TextContent
from matrx_ai.providers.provider_io_capabilities import MediaContainer

from .handler import MediaResolveContext, ResolverResult, register_media_resolver

# "Reasonable" length for extracted document text injected into the model context.
# A CAPS constant (code push to change, not env). ~100k chars ≈ 25k tokens — generous
# but bounded so a huge PDF can't blow the context window. Over the limit → truncate
# and say so in the notice.
MAX_EXTRACTED_DOCUMENT_CHARS = 100_000


def _document_name(content: Any) -> str:
    return (
        getattr(content, "file_name", None)
        or getattr(content, "filename", None)
        or "document"
    )


def _decode_text(raw: bytes) -> str | None:
    for enc in ("utf-8", "utf-16", "latin-1"):
        try:
            return raw.decode(enc)
        except Exception:  # noqa: BLE001
            continue
    return None


# ── per-format extractors (each gated — the lib is optional in a minimal install) ──
def _extract_pdf(raw: bytes) -> str | None:
    from matrx_files.specific_handlers.pdf.extract import (
        extract_text_from_bytes_sync,
    )

    return extract_text_from_bytes_sync(raw, use_ocr_threshold=0)


def _extract_office(raw: bytes, mime: str, file_name: str) -> str | None:
    """docx/pptx/xlsx → clean markdown via the canonical matrx-files Office
    codec (tables, headings, slide notes, per-sheet data — not just paragraph
    text). One codec for chat attachments AND RAG ingest, so a model reads the
    same representation the pipeline stores."""
    from matrx_files.specific_handlers.office import extract_office

    extraction = extract_office(raw, mime_type=mime, file_name=file_name)
    return extraction.markdown or None


def _extract_html(raw: bytes) -> str | None:
    text = _decode_text(raw)
    if text is None:
        return None
    try:
        from markdownify import markdownify

        return markdownify(text)
    except Exception:  # noqa: BLE001 — fall back to a crude tag strip
        import re

        return re.sub(r"<[^>]+>", " ", text)


def _document_format(mime: str, name: str) -> str:
    """Classify a document into an extractor family. Returns '' for unsupported."""
    from matrx_files.specific_handlers.office import classify_office

    mime = (mime or "").lower()
    name = (name or "").lower()
    if "pdf" in mime or name.endswith(".pdf"):
        return "pdf"
    # Any Office family (docx/pptx/xlsx + legacy doc/ppt/xls) → the codec.
    if classify_office(mime, name) is not None:
        return "office"
    if "html" in mime or name.endswith((".html", ".htm")):
        return "html"
    text_exts = (
        ".txt", ".md", ".markdown", ".csv", ".tsv", ".json", ".xml", ".yaml", ".yml",
        ".log", ".rst", ".ini", ".toml", ".py", ".js", ".ts", ".java", ".c", ".cpp",
        ".go", ".rs", ".rb", ".sh", ".sql",
    )
    if (
        mime.startswith("text/")
        or "json" in mime
        or "xml" in mime
        or "csv" in mime
        or "yaml" in mime
        or name.endswith(text_exts)
    ):
        return "text"
    return ""


_EXTRACTORS = {
    "pdf": _extract_pdf,
    "html": _extract_html,
}


def _extract_document_text(raw: bytes, fmt: str, name: str = "", mime: str = "") -> str | None:
    if fmt == "text":
        return _decode_text(raw)
    if fmt == "office":
        return _extract_office(raw, mime, name)
    extractor = _EXTRACTORS.get(fmt)
    if extractor is None:
        return None
    return extractor(raw)


async def _resolve_document(content: Any, ctx: MediaResolveContext) -> ResolverResult:
    name = _document_name(content)
    mime = getattr(content, "mime_type", "") or ""
    fmt = _document_format(mime, name)
    if not fmt:
        return ResolverResult(
            replacement=None,
            action="dropped",
            user_message=f"Document '{name}' removed — this document type isn't extractable yet (PDF, Word, PowerPoint, Excel, and text formats are).",
            system_message=f"unsupported document format (mime={mime!r}, name={name!r}); dropped.",
        )
    b64 = getattr(content, "base64_data", None)
    if not b64:
        return ResolverResult(
            replacement=None,
            action="dropped",
            user_message=f"Document '{name}' removed — its content wasn't available to extract.",
            system_message="DocumentContent had no base64_data (boundary didn't resolve bytes); dropped.",
        )
    try:
        raw = base64.b64decode(b64)
    except Exception as exc:  # noqa: BLE001
        return ResolverResult(
            replacement=None,
            action="dropped",
            user_message=f"Document '{name}' removed — couldn't decode its data.",
            system_message=f"base64 decode failed: {exc!r}",
        )
    try:
        text = (await asyncio.to_thread(_extract_document_text, raw, fmt, name, mime) or "").strip()
    except Exception as exc:  # noqa: BLE001 — extractor lib missing or parse failure → clean drop
        return ResolverResult(
            replacement=None,
            action="dropped",
            user_message=f"Document '{name}' removed — couldn't extract its text.",
            system_message=f"{fmt} extraction failed: {exc!r}",
        )
    if not text:
        return ResolverResult(
            replacement=None,
            action="dropped",
            user_message=f"Document '{name}' removed — no extractable text (a scanned image, perhaps).",
            system_message=f"{fmt} extractor returned empty text.",
        )
    truncated = len(text) > MAX_EXTRACTED_DOCUMENT_CHARS
    if truncated:
        text = text[:MAX_EXTRACTED_DOCUMENT_CHARS]
    body = f"[Document extracted to text — {name}{' (truncated)' if truncated else ''}]\n\n{text}"
    return ResolverResult(
        replacement=TextContent(
            text=body,
            metadata={
                "original_type": "document",
                "extracted_from": fmt,
                "truncated": truncated,
            },
        ),
        action="extracted",
        user_message=(
            f"'{name}' converted to text — {ctx.model_name} can't read {fmt.upper()} files directly, "
            f"so its contents were extracted{' (truncated — the document was very long)' if truncated else ''}."
        ),
        system_message=(
            f"DocumentContent → text via {fmt} extractor "
            f"({len(text)} chars{', truncated' if truncated else ''})."
        ),
    )


def register_builtin_media_resolvers() -> None:
    """Register standalone resolvers; hosts inject conversions needing host services."""
    register_media_resolver(MediaContainer.DOCUMENT, _resolve_document)


__all__ = [
    "MAX_EXTRACTED_DOCUMENT_CHARS",
    "register_builtin_media_resolvers",
]
