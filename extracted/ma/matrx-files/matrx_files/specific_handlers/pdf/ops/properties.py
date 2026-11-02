"""Document properties and XMP: read and write title, author, subject, keywords (PDF-PLAN U11).

Written in BOTH places a reader looks: the Info dictionary and the XMP packet, so Preview, Acrobat
and a search index agree. ``None`` leaves a field alone; an empty string clears it.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from ..concurrency import run_in_cpu_executor
from ..models import PdfBinaryResult
from ._pike import inherited, is_signed, load_pikepdf, open_pdf, save_pdf

#: field -> (Info key, XMP key, XMP value is a list)
_FIELDS: dict[str, tuple[str, str, bool]] = {
    "title": ("/Title", "dc:title", False),
    "author": ("/Author", "dc:creator", True),
    "subject": ("/Subject", "dc:description", False),
    "keywords": ("/Keywords", "pdf:Keywords", False),
}
EDITABLE = tuple(_FIELDS)

#: pikepdf names an XMP key "{namespace-uri}local"; the panel and the tests speak "dc:title".
_XMP_NS = {
    "{http://purl.org/dc/elements/1.1/}": "dc:",
    "{http://ns.adobe.com/pdf/1.3/}": "pdf:",
}


def _short_xmp_key(key: str) -> str:
    for uri, prefix in _XMP_NS.items():
        if key.startswith(uri):
            return prefix + key[len(uri):]
    return key


def _info(pdf: Any, key: str) -> str:
    try:
        value = pdf.docinfo.get(key)
        return "" if value is None else str(value)
    except Exception:
        return ""


def _fonts(pdf: Any, limit: int = 60) -> list[str]:
    seen: list[str] = []
    try:
        for page in pdf.pages:
            res = inherited(page.obj, "/Resources")
            fonts = res.get("/Font") if res is not None else None
            for _, font in (fonts.items() if fonts is not None else []):
                name = str(font.get("/BaseFont", "")).lstrip("/")
                if name and name not in seen:
                    seen.append(name)
                    if len(seen) >= limit:
                        return seen
    except Exception:
        pass
    return seen


def read_properties_bytes(pdf_bytes: bytes, *, password: str = "") -> dict[str, Any]:
    with open_pdf(pdf_bytes, password) as pdf:
        first = pdf.pages[0] if len(pdf.pages) else None
        size = None
        if first is not None:
            box = inherited(first.obj, "/CropBox") or inherited(first.obj, "/MediaBox")
            if box is not None:
                x0, y0, x1, y1 = (float(v) for v in box)
                w, h = abs(x1 - x0), abs(y1 - y0)
                rot = int(inherited(first.obj, "/Rotate") or 0) % 360
                size = {"width_pt": round(h if rot in (90, 270) else w, 2), "height_pt": round(w if rot in (90, 270) else h, 2)}
        xmp = None
        try:
            with pdf.open_metadata(set_pikepdf_as_editor=False, update_docinfo=False) as meta:
                xmp = {
                    short: (list(v) if isinstance(v, (list, set)) else str(v))
                    for short, v in ((_short_xmp_key(k), v) for k, v in meta.items())
                    if short in {"dc:title", "dc:creator", "dc:description", "pdf:Keywords"}
                }
        except Exception:
            xmp = None
        mark = pdf.Root.get("/MarkInfo")
        return {
            "title": _info(pdf, "/Title"),
            "author": _info(pdf, "/Author"),
            "subject": _info(pdf, "/Subject"),
            "keywords": _info(pdf, "/Keywords"),
            "creator": _info(pdf, "/Creator"),
            "producer": _info(pdf, "/Producer"),
            "created": _info(pdf, "/CreationDate"),
            "modified": _info(pdf, "/ModDate"),
            "bates_first": _info(pdf, "/MatrxBatesFirst"),
            "bates_last": _info(pdf, "/MatrxBatesLast"),
            "page_count": len(pdf.pages),
            "page_size": size,
            "pdf_version": str(pdf.pdf_version),
            "tagged": bool(mark is not None and mark.get("/Marked", False)),
            "signed": is_signed(pdf),
            "encrypted": bool(pdf.is_encrypted),
            "has_xmp": "/Metadata" in pdf.Root,
            "xmp": xmp,
            "fonts": _fonts(pdf),
        }


def set_properties_bytes(
    pdf_bytes: bytes,
    *,
    title: str | None = None,
    author: str | None = None,
    subject: str | None = None,
    keywords: str | None = None,
    password: str = "",
) -> PdfBinaryResult:
    updates = {"title": title, "author": author, "subject": subject, "keywords": keywords}
    if all(v is None for v in updates.values()):
        raise ValueError("Give at least one property to change: title, author, subject or keywords.")
    with open_pdf(pdf_bytes, password) as pdf:
        signed = is_signed(pdf)
        total = len(pdf.pages)
        with pdf.open_metadata(set_pikepdf_as_editor=False, update_docinfo=False) as meta:
            for name, value in updates.items():
                if value is None:
                    continue
                info_key, xmp_key, is_list = _FIELDS[name]
                value = value.strip()
                if value:
                    pdf.docinfo[info_key] = value
                    meta[xmp_key] = [value] if is_list else value
                else:
                    if info_key in pdf.docinfo:
                        del pdf.docinfo[info_key]
                    if xmp_key in meta:
                        del meta[xmp_key]
            meta["xmp:MetadataDate"] = datetime.now(timezone.utc).isoformat()
        content = save_pdf(pdf)
    return PdfBinaryResult(
        content=content,
        page_count=total,
        operation="set_properties",
        metadata={"changed": [k for k, v in updates.items() if v is not None], "signed": signed},
    )


async def read_properties_bytes_async(pdf_bytes: bytes, *, password: str = "") -> dict[str, Any]:
    return await run_in_cpu_executor(lambda: read_properties_bytes(pdf_bytes, password=password))


async def set_properties_bytes_async(pdf_bytes: bytes, **kwargs: Any) -> PdfBinaryResult:
    return await run_in_cpu_executor(lambda: set_properties_bytes(pdf_bytes, **kwargs))


__all__ = [
    "EDITABLE",
    "read_properties_bytes",
    "read_properties_bytes_async",
    "set_properties_bytes",
    "set_properties_bytes_async",
]
