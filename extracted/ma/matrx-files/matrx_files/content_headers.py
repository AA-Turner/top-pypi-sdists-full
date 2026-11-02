"""Single source of truth for an object's HTTP content headers.

Every cloud object the platform stores must carry a correct ``Content-Type``
and a sane ``Content-Disposition`` — at *write* time (baked onto the S3
object), at *re-stamp* time (the backfill that fixes already-written
objects), and at *read* time (the streaming download path). Historically
the write path set neither, so every object landed as
``binary/octet-stream`` and public CDN URLs downloaded instead of rendering.

This leaf module is stdlib-only (``mimetypes`` + ``urllib``) so it can be
imported from both ``backends/`` and ``cloud_sync/`` with zero circular-import
risk. ``cloud_sync/download_stream.py`` re-exports the read-side helpers from
here so write-time, read-time, and backfill-time decisions are provably
identical and can never drift.
"""

from __future__ import annotations

import mimetypes
from dataclasses import dataclass
from urllib.parse import quote as _url_quote

# Mimes a browser would happily execute / render as active content — never
# serve these inline regardless of the caller's preference. Mirrors the
# DANGEROUS_INLINE_MIMES set in aidream's media_sniff.py (kept in sync by
# hand; matrx-utils may not import aidream).
DANGEROUS_INLINE_MIMES = frozenset({
    "text/html",
    "application/xhtml+xml",
    "application/xml",
    "image/svg+xml",
    "application/javascript",
    "text/javascript",
})

# Backwards-compatible alias for the previous private name in download_stream.
_DANGEROUS_INLINE_MIMES = DANGEROUS_INLINE_MIMES

_FALLBACK_CONTENT_TYPE = "application/octet-stream"


def _safe_filename_for_header(name: str) -> str:
    """Strip the filename to ASCII for the legacy ``filename="..."`` token.

    RFC-6266 allows a non-ASCII ``filename*`` token; older clients fall back
    to the ASCII token. Replace control chars + quotes that would break it.
    """
    out = []
    for ch in (name or "file"):
        o = ord(ch)
        if o < 32 or o == 127 or ch in ('"', "\\"):  # CTLs (incl. DEL) break the header
            out.append("_")
        elif o < 128:
            out.append(ch)
        else:
            out.append("_")
    return "".join(out) or "file"


def build_content_disposition(file_name: str, *, force_attachment: bool) -> str:
    """RFC-5987 / RFC-6266 compliant Content-Disposition header (with filename)."""
    disposition = "attachment" if force_attachment else "inline"
    ascii_name = _safe_filename_for_header(file_name)
    quoted = _url_quote(file_name, safe="")
    return f'{disposition}; filename="{ascii_name}"; filename*=UTF-8\'\'{quoted}'


def sniffed_content_type(record: dict, *, allow_inline: bool = False) -> tuple[str, bool]:
    """Return ``(effective_content_type, force_attachment)``.

    Coerces dangerous-inline mimes to ``application/octet-stream`` regardless
    of the caller's preference. When ``allow_inline=True``, image/video/
    audio/PDF are served inline; everything else still forces attachment.

    This is the policy SSOT — the write path, the re-stamp backfill, and the
    read-side download streamer all resolve disposition through here.
    """
    claimed = (record.get("mime_type") or "").lower().strip()
    guessed = mimetypes.guess_type(record.get("file_name") or "")[0] or ""
    candidate = (claimed or guessed or _FALLBACK_CONTENT_TYPE).lower()
    if candidate in DANGEROUS_INLINE_MIMES:
        return _FALLBACK_CONTENT_TYPE, True
    if not allow_inline:
        return candidate, True
    if candidate.startswith(("image/", "video/", "audio/")) or candidate == "application/pdf":
        return candidate, False
    return candidate, True


@dataclass(frozen=True)
class ObjectHeaders:
    """The two headers every stored object carries.

    ``content_disposition`` is a BARE keyword (``"inline"`` / ``"attachment"``)
    — no filename. The signed ``download_url`` supplies the real filename per
    request via ``ResponseContentDisposition``; the baked default only governs
    bare public-CDN access, where a generic keyword is exactly right.
    """
    content_type: str
    content_disposition: str  # "inline" | "attachment"


def resolve_object_headers(
    *,
    mime_type: str | None,
    file_name: str | None = None,
) -> ObjectHeaders:
    """Definitive ``(content_type, content_disposition)`` for ANY stored object.

    - ``content_type`` is never ``binary/octet-stream`` for a known type:
      declared ``mime_type`` wins, else a guess from ``file_name``'s extension,
      else the octet-stream fallback (genuinely unknown bytes only).
    - ``content_disposition`` is ``inline`` for image/video/audio/PDF and
      ``attachment`` for everything else; dangerous-inline types (html, svg,
      xml, js) are coerced to octet-stream + attachment (stored-XSS guard).

    Reuses :func:`sniffed_content_type` so write/read/backfill share one policy.
    """
    content_type, force_attachment = sniffed_content_type(
        {"mime_type": mime_type, "file_name": file_name},
        allow_inline=True,
    )
    return ObjectHeaders(
        content_type=content_type,
        content_disposition="attachment" if force_attachment else "inline",
    )


__all__ = [
    "DANGEROUS_INLINE_MIMES",
    "ObjectHeaders",
    "build_content_disposition",
    "resolve_object_headers",
    "sniffed_content_type",
]
