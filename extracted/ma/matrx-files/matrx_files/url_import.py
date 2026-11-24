"""Import a web address into the files service — the one door for "a file from a URL".

A client never fetches a web address itself (the media law: resolve every MediaRef, file_id is
identity). It hands the address here; the bytes are fetched SERVER-SIDE through the package's one
safe external fetcher (``cloud_sync._media_resolution._fetch_external_url_into_ref`` — every hop a
public address via ``matrx_utils.outbound_guard.public_only_client``, streamed under a size cap),
then stored exactly the way ``POST /files/upload`` stores (``FileService.upload_simple``, the
organization the request was admitted with, the actor carried), under the ``files.import``
pathway. The answer is the stored file — its ``file_id`` is the identity from then on.

A refusal is a :class:`UrlImportRefused`: it names its own HTTP status, code and the sentence a
person reads, so the router's one exception mapper passes it through unchanged.
"""

from __future__ import annotations

import base64
import mimetypes
from dataclasses import dataclass
from typing import Any
from urllib.parse import unquote, urlsplit

from matrx_utils import hash_text
from matrx_utils.row_access import SHOWN_TO_TYPE_DEFAULT

from .cloud_sync import _media_resolution
from .cloud_sync.media_ref import MediaRef
from .media_sniff import SNIFF_HEAD_BYTES, sniff_mime_type
from .placement import resolve as resolve_placement
from .placement import sanitize_file_name

__all__ = ["IMPORT_PATHWAY", "UrlImportRefused", "UrlImportResult", "import_url"]

IMPORT_PATHWAY = "files.import"
IMPORT_SOURCE = "Web"


class UrlImportRefused(Exception):
    """The address could not become a file; ``str(self)`` is the sentence a person reads."""

    def __init__(self, message: str, *, code: str, http_status: int) -> None:
        super().__init__(message)
        self.code = code
        self.http_status = http_status
        self.user_message = message


@dataclass(frozen=True)
class UrlImportResult:
    """The stored file (the ``upload_simple`` result) and where it was filed."""

    result: Any
    file_path: str
    mime_type: str
    source_url: str


def _checked_url(url: str) -> str:
    text = (url or "").strip()
    if not text:
        raise UrlImportRefused("No web address was given.", code="url_missing", http_status=400)
    parts = urlsplit(text)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise UrlImportRefused(
            "Only web (http or https) addresses can be imported.", code="url_not_web", http_status=400
        )
    return text


def _refusal_for(resolver_error: str) -> UrlImportRefused:
    """The fetcher's short reason as the sentence a person reads, with its own status."""
    head = resolver_error.split(":", 1)[0]
    if head == "external_fetch_refused":
        return UrlImportRefused(
            "That address is not a public web address, so it was not fetched.",
            code="url_not_public",
            http_status=400,
        )
    if head.startswith("external_fetch_http_"):
        status = head.removeprefix("external_fetch_http_")
        return UrlImportRefused(
            f"The site answered {status} for that address.", code="url_fetch_http_error", http_status=502
        )
    if head == "external_fetch_too_large":
        return UrlImportRefused(
            f"That file is too large to import ({resolver_error.split(':', 1)[-1].strip()}).",
            code="url_too_large",
            http_status=413,
        )
    if head == "external_fetch_timeout":
        return UrlImportRefused(
            "The site did not answer in time.", code="url_fetch_timeout", http_status=504
        )
    return UrlImportRefused(
        f"That address could not be fetched ({resolver_error}).", code="url_fetch_failed", http_status=502
    )


def _file_name(url: str, mime_type: str) -> str:
    """The address's own last segment, made unique per address (a short hash), with an extension."""
    segment = unquote(urlsplit(url).path.rsplit("/", 1)[-1])
    stem, dot, ext = segment.rpartition(".")
    if not dot or not stem:
        stem, ext = segment, ""
    ext = ext.lower() if ext else (mimetypes.guess_extension(mime_type) or "").lstrip(".")
    stem = sanitize_file_name(stem or "import")[:120]
    tag = hash_text(url, length=8)
    return f"{stem}-{tag}.{ext}" if ext else f"{stem}-{tag}"


async def import_url(
    file_service: Any,
    *,
    url: str,
    user_id: str,
    organization_id: str | None,
    max_bytes: int | None = None,
    timeout_seconds: float | None = None,
) -> UrlImportResult:
    """Fetch ``url`` server-side (public addresses only) and store it as the actor's file.

    ``organization_id`` is the organization the request was admitted with — never chosen here.
    Raises :class:`UrlImportRefused` with the person's sentence when the address cannot be used.
    """
    source_url = _checked_url(url)
    ref = MediaRef(url=source_url)
    await _media_resolution._fetch_external_url_into_ref(
        ref, max_bytes=max_bytes, timeout_seconds=timeout_seconds
    )
    if ref.resolver_error:
        raise _refusal_for(ref.resolver_error)
    content = base64.b64decode(ref.base64_data or "")
    if not content:
        raise UrlImportRefused("That address answered with no content.", code="url_empty", http_status=502)

    mime_type = sniff_mime_type(
        claimed=ref.mime_type, head_bytes=content[:SNIFF_HEAD_BYTES], filename=urlsplit(source_url).path
    )
    name = _file_name(source_url, mime_type or "application/octet-stream")
    placement = resolve_placement(IMPORT_PATHWAY, tokens={"source": IMPORT_SOURCE}, original_name=name)
    file_path = f"{placement.folder_path}/{placement.file_name}"
    result = await file_service.upload_simple(
        content,
        file_path=file_path,
        mime_type=mime_type,
        published_to_web=False,
        shown_to=SHOWN_TO_TYPE_DEFAULT,  # the file type's "Shown to" knob
        user_id=user_id,
        organization_id=organization_id,
        metadata={"source_url": source_url},
        pathway=IMPORT_PATHWAY,
    )
    return UrlImportResult(result=result, file_path=file_path, mime_type=mime_type, source_url=source_url)
