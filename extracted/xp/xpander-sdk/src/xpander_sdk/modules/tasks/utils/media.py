"""Capability-aware attachment preparation (images + PDFs).

Rescues attachments the legacy path silently drops (oversized images,
BMP/TIFF) or that providers reject (``type:'file'`` PDFs on OpenAI-compat
gateways) by transforming them to something the resolved model accepts.

Invariants (the prior-revert insurance):
- The healthy path is byte-identical to legacy ``fetch_image``/``fetch_file``:
  a valid png/jpeg/gif/webp under the byte cap passes through un-re-encoded.
- Every transformed image is freshly encoded by Pillow, valid by construction.
- Pillow/pypdf missing or ``XPANDER_MEDIA_PIPELINE=legacy`` -> exact legacy
  behavior (validate-or-drop images, native File PDFs).
"""

import asyncio
import base64
import os
from io import BytesIO
from typing import Any, Optional, Tuple

from loguru import logger

from xpander_sdk.modules.tasks.utils.files import (
    _FETCH_TIMEOUT,
    _MAX_INLINE_TEXT_CHARS,
    _download,
    _looks_like_pdf,
    _pdf_markdown_or_none,
    _sniff_image,
    fetch_file,
    fetch_image,
)
from xpander_sdk.modules.tasks.utils.model_capabilities import (
    ModelCapabilities,
    media_pipeline_disabled,
)

# Decode-bomb ceiling: a small file can declare a huge canvas that allocates
# gigabytes on decode. We check the declared pixel count from the header (no full
# decode) and refuse above this, so an oversized image is rejected, not OOM'd.
_MAX_IMAGE_PIXELS = int(os.getenv("XPANDER_MAX_IMAGE_PIXELS", str(40_000_000)))

# Formats Pillow can rescue but providers reject as-is (kept out of
# files._IMAGE_SIGNATURES so the legacy passthrough gate stays strict).
_CONVERTIBLE_SIGNATURES = (
    (b"BM", "bmp"),
    (b"II*\x00", "tiff"),
    (b"MM\x00*", "tiff"),
)

_JPEG_QUALITY_STEPS = (85, 65, 50)

# Scanned-PDF heuristic: real text averages far more than this per page.
_SCANNED_PDF_CHARS_PER_PAGE = 50

SCANNED_PDF_NOTE = "appears to be a scanned PDF (no extractable text); use an OCR tool on the URL to read it"
HUGE_FILE_NOTE = (
    "too large to attach inline; fetch it via your tools/workspace using the URL"
)
NO_INJECTION_NOTE = "content is NOT included in this message; fetch it via your tools/workspace using the URL"
NOT_A_PDF_NOTE = "the link did not return a PDF (it may have expired); fetch it via your tools/workspace using the URL"
PDF_AS_TEXT_NOTE = (
    "included as extracted text; any images, charts or diagrams it contains are not part of "
    "that text, so use a tool on the URL if you need to see them"
)


def _pillow():
    try:
        from PIL import Image as PILImage

        # Do not set PILImage.MAX_IMAGE_PIXELS here: it is process-global (thread-unsafe)
        # and would make the header-only probe in _too_many_pixels raise. The explicit
        # pixel check refuses a bomb before any full decode instead.
        return PILImage
    except Exception:
        return None


def _too_many_pixels(data: bytes, pil_module) -> bool:
    """Whether the image header declares more pixels than the decode ceiling (header only, no full decode)."""
    try:
        with pil_module.open(BytesIO(data)) as probe:
            w, h = probe.size
        return (w * h) > _MAX_IMAGE_PIXELS
    except Exception:
        # An unreadable header is handled by the real decode / sniff downstream.
        return False


def _pypdf():
    try:
        import pypdf

        return pypdf
    except Exception:
        return None


def _sniff_convertible(data: bytes) -> Optional[str]:
    for sig, fmt in _CONVERTIBLE_SIGNATURES:
        if data.startswith(sig):
            return fmt
    return None


def _agno_image_from_bytes(content: bytes, fmt: str, mime: str):
    from agno.media import Image

    return Image.from_base64(
        base64_content=base64.b64encode(content).decode("utf-8"),
        format=fmt,
        mime_type=mime,
    )


def _transform_image(
    data: bytes, caps: ModelCapabilities, pil_module
) -> Tuple[bytes, str, str]:
    """Decode, downscale to the long-edge target, and re-encode under the byte cap; raises when unrescuable."""
    # Refuse before decoding when the header declares more pixels than the ceiling -
    # explicit and thread-safe, unlike mutating the global warnings filter.
    if _too_many_pixels(data, pil_module):
        raise ValueError(f"image canvas exceeds the {_MAX_IMAGE_PIXELS}px ceiling")
    img = pil_module.open(BytesIO(data))
    img.load()

    long_edge = max(img.size)
    if long_edge > caps.max_image_px:
        scale = caps.max_image_px / long_edge
        img = img.resize(
            (max(1, int(img.width * scale)), max(1, int(img.height * scale)))
        )

    has_alpha = img.mode in ("RGBA", "LA", "PA") or (
        img.mode == "P" and "transparency" in img.info
    )
    if has_alpha:
        buf = BytesIO()
        img.save(buf, format="PNG", optimize=True)
        if buf.tell() <= caps.max_image_bytes:
            return buf.getvalue(), "png", "image/png"
        img = img.convert("RGB")

    if img.mode != "RGB":
        img = img.convert("RGB")
    for quality in _JPEG_QUALITY_STEPS:
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)
        if buf.tell() <= caps.max_image_bytes:
            return buf.getvalue(), "jpeg", "image/jpeg"
    raise ValueError(
        f"image still exceeds {caps.max_image_bytes} bytes after downscale+recompress"
    )


def prepare_image(
    url: str,
    caps: ModelCapabilities,
    known_size: Optional[int] = None,
    timeout: float = _FETCH_TIMEOUT,
) -> Optional[Any]:
    """Return an inline Agno Image for *url* under *caps*; None for the huge tier; raises when unrescuable.

    Healthy images (valid provider-accepted format under the byte cap) pass through
    byte-identical to legacy. Oversized/BMP/TIFF images are downscaled/converted via
    Pillow instead of dropped. Kill switch or missing Pillow -> exact legacy behavior.
    """
    if media_pipeline_disabled():
        return fetch_image(url=url)

    if known_size is not None and known_size > caps.max_fetch_bytes:
        return None

    content, ctype = _download(url, max_bytes=caps.max_fetch_bytes, timeout=timeout)
    if ctype and not (
        ctype.startswith("image/")
        or ctype in ("application/octet-stream", "binary/octet-stream")
    ):
        raise ValueError(f"non-image content-type {ctype!r}: {url}")

    sniffed = _sniff_image(content)
    pil_module = _pillow()
    if sniffed is not None and len(content) <= caps.max_image_bytes:
        # Pass bytes through byte-identical only when the declared canvas is also
        # within budget. A small file declaring a huge canvas (decompression bomb)
        # falls through to the transform path, which refuses it before decoding.
        if pil_module is None or not _too_many_pixels(content, pil_module):
            fmt, mime = sniffed
            return _agno_image_from_bytes(content, fmt, mime)

    if pil_module is None:
        # Legacy behavior without Pillow: validate-or-drop at the legacy ceiling.
        if sniffed is None:
            raise ValueError(f"bytes are not a supported image: {url}")
        raise ValueError(
            f"image exceeds {caps.max_image_bytes} bytes and Pillow is unavailable: {url}"
        )

    if sniffed is None and _sniff_convertible(content) is None:
        raise ValueError(f"bytes are not a supported image: {url}")

    data, fmt, mime = _transform_image(content, caps, pil_module)
    logger.info(
        f"transformed image {url} -> {fmt} {len(data)} bytes (was {len(content)})"
    )
    return _agno_image_from_bytes(data, fmt, mime)


def _pdf_reader(data: bytes, pypdf_module):
    return pypdf_module.PdfReader(BytesIO(data))


def _truncate_pdf(data: bytes, max_pages: int, pypdf_module) -> Tuple[bytes, int, int]:
    reader = _pdf_reader(data, pypdf_module)
    total = len(reader.pages)
    writer = pypdf_module.PdfWriter()
    for page in reader.pages[:max_pages]:
        writer.add_page(page)
    buf = BytesIO()
    writer.write(buf)
    return buf.getvalue(), min(max_pages, total), total


def _extract_pdf_text(data: bytes, pypdf_module) -> Tuple[str, int]:
    reader = _pdf_reader(data, pypdf_module)
    pages = reader.pages
    text = "\n".join((page.extract_text() or "") for page in pages)
    return text, max(1, len(pages))


def _agno_file_from_bytes(content: bytes, url: str):
    from agno.media import File

    filename = os.path.basename(url.split("?")[0])
    return File.from_base64(
        base64_content=base64.b64encode(content).decode("utf-8"),
        filename=filename,
        name=os.path.splitext(filename)[0].replace("_", " "),
        format="pdf",
        mime_type="application/pdf",
    )


def prepare_pdf(
    url: str,
    caps: ModelCapabilities,
    known_size: Optional[int] = None,
    timeout: float = _FETCH_TIMEOUT,
    allow_text: bool = True,
    text_budget: Optional[int] = None,
) -> Tuple[str, Optional[Any], Optional[str]]:
    """Route a PDF under *caps*: returns (action, payload, note) with action in {"file","text","url_only"}.

    Native-PDF providers get an inline File (page-truncated when over the page cap);
    others get pypdf-extracted text; scanned/huge PDFs stay URL-only with a note for
    the agent. Kill switch or missing pypdf -> legacy inline File. ``allow_text=False``
    (attachment injection disabled) never returns text, so a caller that discards text
    payloads still gets the native attachment rather than nothing. ``text_budget`` is how
    many chars of Markdown the caller can actually deliver, and defaults to the per-file cap.
    """
    if media_pipeline_disabled():
        return "file", fetch_file(url=url), None

    if known_size is not None and known_size > caps.max_fetch_bytes:
        return "url_only", None, HUGE_FILE_NOTE

    pypdf_module = _pypdf()
    if pypdf_module is None:
        return "file", fetch_file(url=url), None

    try:
        content, _ = _download(url, max_bytes=caps.max_fetch_bytes, timeout=timeout)
    except ValueError:
        return "url_only", None, HUGE_FILE_NOTE

    # A .pdf URL's extension is not trustworthy - an expired/redirected presigned link
    # returns HTML with HTTP 200. Do not attach non-PDF bytes as a PDF.
    if not _looks_like_pdf(content):
        return "url_only", None, NOT_A_PDF_NOTE

    native_possible = caps.supports_native_pdf and len(content) <= caps.max_pdf_bytes

    # Text-based PDFs: the Markdown carries the same content at roughly a third of the
    # input tokens of a native attachment, which bills every page twice (text + page
    # image). Scanned PDFs fail the density gate and take the native path below.
    markdown = _pdf_markdown_or_none(content) if allow_text else None
    if markdown is not None:
        # Inlined text is clipped at the caller's budget while a native attachment carries
        # the whole PDF, so the token saving is only free while the Markdown fits.
        budget = _MAX_INLINE_TEXT_CHARS if text_budget is None else text_budget
        if not (native_possible and len(markdown) > budget):
            # Only a model that could have rendered the pages loses anything by reading text.
            return "text", markdown, (PDF_AS_TEXT_NOTE if native_possible else None)
        logger.debug(
            f"pdf markdown ({len(markdown)} chars) exceeds the inline cap; attaching natively: {url}"
        )

    if native_possible:
        try:
            page_count = len(_pdf_reader(content, pypdf_module).pages)
        except Exception:
            # Unparseable by pypdf but provider-native: ship it as-is, like legacy.
            return "file", _agno_file_from_bytes(content, url), None
        if page_count <= caps.max_pdf_pages:
            return "file", _agno_file_from_bytes(content, url), None
        truncated, kept, total = _truncate_pdf(
            content, caps.max_pdf_pages, pypdf_module
        )
        note = f"attached first {kept} of {total} pages; full file at the URL"
        return "file", _agno_file_from_bytes(truncated, url), note

    if not allow_text:
        return "url_only", None, NO_INJECTION_NOTE

    try:
        text, page_count = _extract_pdf_text(content, pypdf_module)
    except Exception as e:
        logger.warning(f"pdf text extraction failed for {url}: {e}")
        return (
            "url_only",
            None,
            HUGE_FILE_NOTE if len(content) > caps.max_pdf_bytes else SCANNED_PDF_NOTE,
        )

    if len(text.strip()) / page_count < _SCANNED_PDF_CHARS_PER_PAGE:
        return "url_only", None, SCANNED_PDF_NOTE
    return "text", text, None


async def aprepare_image(
    url: str, caps: ModelCapabilities, known_size: Optional[int] = None
):
    """prepare_image off the event loop (Pillow decode/encode is CPU-bound)."""
    return await asyncio.to_thread(prepare_image, url, caps, known_size)


async def aprepare_pdf(
    url: str,
    caps: ModelCapabilities,
    known_size: Optional[int] = None,
    allow_text: bool = True,
    text_budget: Optional[int] = None,
) -> Tuple[str, Optional[Any], Optional[str]]:
    """prepare_pdf off the event loop (pypdf parse and anydoc conversion are CPU-bound)."""
    return await asyncio.to_thread(
        prepare_pdf, url, caps, known_size, _FETCH_TIMEOUT, allow_text, text_budget
    )
