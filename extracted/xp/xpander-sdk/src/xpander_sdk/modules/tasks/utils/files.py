import base64
import mimetypes
from io import BytesIO
from typing import List, Optional, Tuple
from urllib.parse import urlparse
import os
from pydantic import BaseModel
from loguru import logger
import httpx
import asyncio

# Provider per-image ceiling (Bedrock/Anthropic ~5MB); env-overridable.
_MAX_IMAGE_BYTES = int(os.getenv("XPANDER_MAX_INLINE_IMAGE_BYTES", str(5 * 1024 * 1024)))
_MAX_DOC_BYTES = int(os.getenv("XPANDER_MAX_INLINE_DOC_BYTES", str(15 * 1024 * 1024)))
_FETCH_TIMEOUT = float(os.getenv("XPANDER_FILE_FETCH_TIMEOUT", "15"))

# Char ceilings for inlining human-readable file text into the prompt. A large
# CSV/JSON pasted in full blows the context window, so cap per-file and total
# and keep the URL (already listed) for the agent to fetch the rest if needed.
_MAX_INLINE_TEXT_CHARS = int(os.getenv("XPANDER_MAX_INLINE_TEXT_CHARS", "8000"))
_MAX_INLINE_TOTAL_CHARS = int(os.getenv("XPANDER_MAX_INLINE_TOTAL_CHARS", "24000"))


def truncate_inline_text(content: str, url: str, remaining: int) -> str:
    """Clip inlined file *content* to *remaining* (and the per-file cap), noting the URL for the rest."""
    cap = min(_MAX_INLINE_TEXT_CHARS, max(0, remaining))
    if len(content) <= cap:
        return content
    return content[:cap] + f"\n... [truncated: {len(content):,} chars total - full file at {url}]"

# Leading-byte signatures for the only raster formats vision providers accept.
_IMAGE_SIGNATURES = (
    (b"\x89PNG\r\n\x1a\n", "png", "image/png"),
    (b"\xff\xd8\xff", "jpeg", "image/jpeg"),
    (b"GIF87a", "gif", "image/gif"),
    (b"GIF89a", "gif", "image/gif"),
)

_DOCUMENT_EXTS = {".docx", ".doc", ".xlsx", ".xls", ".pptx"}


class FileCategorization(BaseModel):
    images: List[str]
    pdfs: List[str]
    files: List[str]
    documents: List[str] = []


def categorize_files(file_urls: list[str]) -> FileCategorization:
    """
    Categorize a list of file URLs into images, PDFs, and human-readable files
    based on file extensions. Does not load the files.

    Args:
        file_urls (list[str]): List of file URLs

    Returns:
        FileCategorization: Pydantic model with categorized URLs
    """
    image_exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
    pdf_exts = {".pdf"}
    human_readable_exts = {
        # SVG is XML: models read it as text, image pipelines reject it.
        ".svg",
        ".txt",
        ".csv",
        ".json",
        ".xml",
        ".html",
        ".htm",
        ".md",
        ".rst",
        ".yaml",
        ".yml",
        ".py",
        ".js",
        ".ts",
        ".java",
        ".c",
        ".cpp",
        ".h",
        ".cs",
        ".go",
        ".rb",
        ".php",
        ".sh",
    }

    result = {"images": [], "pdfs": [], "files": [], "documents": []}

    for url in file_urls:
        path = urlparse(url).path
        _, ext = os.path.splitext(path.lower())

        if ext in image_exts:
            result["images"].append(url)
        elif ext in pdf_exts:
            result["pdfs"].append(url)
        elif ext in _DOCUMENT_EXTS:
            result["documents"].append(url)
        elif ext in human_readable_exts:
            result["files"].append(url)

    return FileCategorization(**result)


async def fetch_urls(
    urls: list[str], disable_attachment_injection: Optional[bool] = False
) -> list[dict[str, str]]:
    """
    Fetches the content of multiple URLs asynchronously.

    Args:
        urls (list[str]): List of URLs to fetch.

    Returns:
        list[dict[str, str]]: A list of dictionaries containing the URL and its content.
                              Example: [{"url": "...", "content": "..."}]
        disable_attachment_injection (Optional[bool]): Optional selection if to disable attachment injection to the context window.
    """

    async def fetch(client: httpx.AsyncClient, url: str) -> dict[str, str]:
        try:
            if disable_attachment_injection:
                return {"url": url}
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            return {"url": url, "content": response.text}
        except Exception as e:
            return {"url": url, "content": f"Error: {str(e)}"}

    async with httpx.AsyncClient() as client:
        tasks = [fetch(client, url) for url in urls]
        return await asyncio.gather(*tasks)


class AttachmentDecision(BaseModel):
    url: str
    category: str  # image | pdf | document | readable | other
    action: str  # inline | text_extract | url_only | skip
    reason: Optional[str] = None
    size: Optional[int] = None


class AttachmentPlan(BaseModel):
    items: List[AttachmentDecision] = []
    notes: List[str] = []

    def by_category(self, category: str) -> List[AttachmentDecision]:
        return [item for item in self.items if item.category == category]


async def estimate_sizes(urls: List[str], timeout: float = 2.0) -> dict:
    """Best-effort parallel size probe -> {url: bytes or None}; HEAD first, ranged-GET fallback for HEAD-hostile hosts."""
    if not urls:
        return {}

    async def _probe(client: httpx.AsyncClient, url: str) -> Optional[int]:
        try:
            resp = await client.head(url)
            raw = resp.headers.get("content-length")
            if resp.status_code < 400 and raw is not None:
                return int(raw)
        except Exception:
            pass
        try:
            resp = await client.get(url, headers={"Range": "bytes=0-0"})
            content_range = resp.headers.get("content-range") or ""
            if "/" in content_range:
                total = content_range.rsplit("/", 1)[1].strip()
                if total.isdigit():
                    return int(total)
            # Host ignored the range and served the whole body.
            raw = resp.headers.get("content-length")
            if raw is not None and int(raw) > 1:
                return int(raw)
        except Exception:
            pass
        return None

    async with httpx.AsyncClient(follow_redirects=True, timeout=timeout) as client:
        results = await asyncio.gather(*[_probe(client, u) for u in urls], return_exceptions=True)
    return {u: (r if isinstance(r, int) else None) for u, r in zip(urls, results)}


def plan_attachments(
    urls: List[str],
    caps,
    sizes: Optional[dict] = None,
) -> AttachmentPlan:
    """Decide per-URL attachment handling from (categories, capabilities, known sizes) - pure, no downloads."""
    plan = AttachmentPlan()
    if not urls:
        return plan
    sizes = sizes or {}
    cat = categorize_files(file_urls=urls)
    categories = (
        [("image", u) for u in cat.images]
        + [("pdf", u) for u in cat.pdfs]
        + [("document", u) for u in cat.documents]
        + [("readable", u) for u in cat.files]
    )
    known = {u for _, u in categories}
    categories += [("other", u) for u in urls if u not in known]

    skipped_images = 0
    inlined_images = 0
    for category, url in categories:
        size = sizes.get(url)
        if category == "image":
            if not caps.supports_vision:
                plan.items.append(AttachmentDecision(url=url, category=category, action="skip", reason="model has no vision", size=size))
                skipped_images += 1
            elif size is not None and size > caps.max_fetch_bytes:
                plan.items.append(AttachmentDecision(url=url, category=category, action="url_only", reason="huge", size=size))
                plan.notes.append(f"{url}: too large to attach inline; fetch it via your tools/workspace using the URL")
            elif inlined_images >= caps.max_images:
                plan.items.append(AttachmentDecision(url=url, category=category, action="url_only", reason="max_images", size=size))
            else:
                plan.items.append(AttachmentDecision(url=url, category=category, action="inline", size=size))
                inlined_images += 1
        elif category == "pdf":
            if size is not None and size > caps.max_fetch_bytes:
                plan.items.append(AttachmentDecision(url=url, category=category, action="url_only", reason="huge", size=size))
                plan.notes.append(f"{url}: too large to attach inline; fetch it via your tools/workspace using the URL")
            elif caps.supports_native_pdf:
                plan.items.append(AttachmentDecision(url=url, category=category, action="inline", size=size))
            else:
                plan.items.append(AttachmentDecision(url=url, category=category, action="text_extract", reason="provider rejects file blobs", size=size))
        elif category in ("document", "readable"):
            plan.items.append(AttachmentDecision(url=url, category=category, action="text_extract", size=size))
        else:
            plan.items.append(AttachmentDecision(url=url, category=category, action="url_only", size=size))

    if skipped_images:
        plural = "s" if skipped_images != 1 else ""
        plan.notes.append(
            f"{skipped_images} image{plural} listed above cannot be viewed by this model; "
            "use tools to process them if needed"
        )
    return plan


def _download(
    url: str, *, max_bytes: int, timeout: float
) -> Tuple[bytes, str]:
    """Stream a URL to bytes, aborting past `max_bytes`; returns (content, lowercased content-type)."""
    with httpx.Client(follow_redirects=True, timeout=timeout) as client:
        with client.stream("GET", url) as resp:
            resp.raise_for_status()
            ctype = (resp.headers.get("content-type") or "").split(";", 1)[0].strip().lower()
            buf = bytearray()
            for chunk in resp.iter_bytes():
                buf += chunk
                if len(buf) > max_bytes:
                    raise ValueError(f"file exceeds {max_bytes} bytes: {url}")
            return bytes(buf), ctype


def _sniff_image(data: bytes) -> Optional[Tuple[str, str]]:
    """Return (format, mime) if `data` begins with a supported image signature, else None."""
    for sig, fmt, mime in _IMAGE_SIGNATURES:
        if data.startswith(sig):
            return fmt, mime
    if len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp", "image/webp"
    return None


def fetch_image(
    url: str, *, max_bytes: int = _MAX_IMAGE_BYTES, timeout: float = _FETCH_TIMEOUT
):
    """Download a URL and wrap it as an inline Agno Image, only if the bytes are a genuine supported image.

    Providers reject remote image URLs and require inline bytes, and a URL's extension is not trustworthy
    (expired/redirected presigned links return HTML/XML with HTTP 200). So the content-type and leading
    magic bytes are validated and format/mime are derived from the bytes, not the URL. Raises on anything
    not a verifiable png/jpeg/gif/webp so callers can drop it instead of feeding garbage to the model.
    """
    content, ctype = _download(url, max_bytes=max_bytes, timeout=timeout)
    if ctype and not (ctype.startswith("image/") or ctype in ("application/octet-stream", "binary/octet-stream")):
        raise ValueError(f"non-image content-type {ctype!r}: {url}")
    sniffed = _sniff_image(content)
    if sniffed is None:
        raise ValueError(f"bytes are not a supported image: {url}")
    fmt, mime = sniffed
    content_b64 = base64.b64encode(content).decode("utf-8")
    from agno.media import Image

    return Image.from_base64(base64_content=content_b64, format=fmt, mime_type=mime)


def _docx_text(data: bytes) -> str:
    from docx import Document  # python-docx

    return "\n".join(p.text for p in Document(BytesIO(data)).paragraphs)


def _xlsx_text(data: bytes) -> str:
    from openpyxl import load_workbook

    wb = load_workbook(BytesIO(data), data_only=True, read_only=True)
    rows: List[str] = []
    for sheet in wb.sheetnames:
        for row in wb[sheet].iter_rows(values_only=True):
            rows.append("\t".join("" if c is None else str(c) for c in row))
    return "\n".join(rows)


def _pptx_text(data: bytes) -> str:
    from pptx import Presentation  # python-pptx

    out: List[str] = []
    for slide in Presentation(BytesIO(data)).slides:
        for shape in slide.shapes:
            if getattr(shape, "has_text_frame", False):
                out.append(shape.text_frame.text)
    return "\n".join(out)


def extract_document_text(
    url: str, *, max_bytes: int = _MAX_DOC_BYTES, timeout: float = _FETCH_TIMEOUT
) -> str:
    """Download an office document and extract its text; '' when the format is unsupported or its parser lib is missing."""
    _, ext = os.path.splitext(urlparse(url).path.lower())
    try:
        content, _ = _download(url, max_bytes=max_bytes, timeout=timeout)
        if ext in (".docx", ".doc"):
            return _docx_text(content)
        if ext in (".xlsx", ".xls"):
            return _xlsx_text(content)
        if ext == ".pptx":
            return _pptx_text(content)
        return ""
    except Exception as e:
        logger.warning(f"failed to extract text from document {url}: {e}")
        return ""


def fetch_file(url: str):
    """
    Fetch a remote file from URL and wrap it as a File object.
    Automatically derives filename, name, format, and mime type.

    Args:
        url (str): Remote file URL.

    Returns:
        File: Wrapped File object with base64 content.
    """
    content, _ = _download(url, max_bytes=_MAX_DOC_BYTES, timeout=_FETCH_TIMEOUT)

    # Derive filename from URL
    filename = os.path.basename(url.split("?")[0])

    # Human-friendly name (strip extension, replace underscores)
    name = os.path.splitext(filename)[0].replace("_", " ")

    # Guess format and mime type
    ext = os.path.splitext(filename)[1].lstrip(".").lower()
    mime, _ = mimetypes.guess_type(filename)
    mime = mime or "application/octet-stream"

    # Encode content
    content_b64 = base64.b64encode(content).decode("utf-8")
    from agno.media import File

    return File.from_base64(
        base64_content=content_b64,
        filename=filename,
        name=name,
        format=ext,
        mime_type=mime,
    )
