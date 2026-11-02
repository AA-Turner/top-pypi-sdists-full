"""Stamp: watermark, page numbers, Bates numbering and header/footer templates (PDF-PLAN U11).

One engine. A *stamp* is a line of text with tokens, a position, a font and an opacity, drawn into a
content stream that ``pikepdf`` adds to each chosen page (over the page, or behind it). The stamp is
laid out in the rectangle a person SEES: the page's /Rotate and its crop box are applied, so a footer
on a rotated page is still at the bottom of the screen.

Tokens inside ``text``:

- ``{page}``  page number          ``{pages}``  page count        ``{date}``  today (ISO, UTC)
- ``{title}`` document title       ``{bates}``  Bates number (the spec's ``bates_start`` and ``bates_digits``)
- ``{bates:000001}`` Bates number that starts at 1 and is 6 digits wide (the digits set start and width)

Bates numbers count the STAMPED pages in order, so they are monotone with no gaps. The first and last
number are recorded in the file's Info dictionary (``/MatrxBatesFirst``, ``/MatrxBatesLast``) so a
later merge or a lawyer's index can read the range back.

Fonts are the standard PDF fonts (Helvetica, Times, Courier, regular or bold) in WinAnsi; a character
outside it is replaced and counted in ``metadata["replaced_characters"]``.
"""

from __future__ import annotations

import math
import re
from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

from ..concurrency import run_in_cpu_executor
from ..models import PdfBinaryResult, PdfPageRange
from ._pike import inherited, is_signed, load_pikepdf, open_pdf, save_pdf

StampPosition = Literal[
    "top-left", "top-center", "top-right",
    "center",
    "bottom-left", "bottom-center", "bottom-right",
]
StampFont = Literal["helvetica", "times", "courier"]

_BASE_FONTS: dict[tuple[str, bool], str] = {
    ("helvetica", False): "Helvetica",
    ("helvetica", True): "Helvetica-Bold",
    ("times", False): "Times-Roman",
    ("times", True): "Times-Bold",
    ("courier", False): "Courier",
    ("courier", True): "Courier-Bold",
}
_METRIC_NAMES = dict(_BASE_FONTS)  # same names in pdfminer's metrics table

_TOKEN = re.compile(r"\{(page|pages|date|title|bates)(?::(\d+))?\}")
_HEX = re.compile(r"^#?([0-9a-fA-F]{6})$")


class PdfStampSpec(BaseModel):
    """One piece of text to put on the chosen pages."""

    text: str = Field(min_length=1, max_length=500)
    position: StampPosition = "bottom-center"
    font: StampFont = "helvetica"
    bold: bool = False
    size: float = Field(default=10.0, gt=1, le=200)
    color: str = "#000000"
    opacity: float = Field(default=1.0, gt=0, le=1)
    #: Degrees, counter-clockwise, about the middle of the text. 45 is the classic diagonal watermark.
    rotation: float = Field(default=0.0, ge=-360, le=360)
    margin: float = Field(default=28.0, ge=0, le=400)
    #: Behind the page content (a watermark that does not cover the text) instead of over it.
    behind: bool = False
    bates_start: int = Field(default=1, ge=0, le=10**12)
    bates_digits: int = Field(default=6, ge=1, le=12)

    @field_validator("color")
    @classmethod
    def _color(cls, value: str) -> str:
        if not _HEX.match(value):
            raise ValueError("Colour must be a hex value like #cc0000.")
        return value if value.startswith("#") else f"#{value}"


class PdfHeaderFooterTemplate(BaseModel):
    """A header and footer: up to three texts on each line (left, centre, right). Stored as a plain object so a
    person, a tool rail and an agent all hand the same shape."""

    name: str = Field(min_length=1, max_length=80)
    header_left: str = ""
    header_center: str = ""
    header_right: str = ""
    footer_left: str = ""
    footer_center: str = ""
    footer_right: str = ""
    font: StampFont = "helvetica"
    bold: bool = False
    size: float = Field(default=9.0, gt=1, le=72)
    color: str = "#444444"
    margin: float = Field(default=28.0, ge=0, le=200)
    bates_start: int = Field(default=1, ge=0, le=10**12)
    bates_digits: int = Field(default=6, ge=1, le=12)

    def to_specs(self) -> list[PdfStampSpec]:
        slots = [
            ("top-left", self.header_left), ("top-center", self.header_center), ("top-right", self.header_right),
            ("bottom-left", self.footer_left), ("bottom-center", self.footer_center), ("bottom-right", self.footer_right),
        ]
        return [
            PdfStampSpec(
                text=text, position=pos, font=self.font, bold=self.bold, size=self.size, color=self.color,
                margin=self.margin, bates_start=self.bates_start, bates_digits=self.bates_digits,
            )
            for pos, text in slots
            if text.strip()
        ]


#: Ready-made templates the tools rail offers (and agents can name).
BUILTIN_HEADER_FOOTER_TEMPLATES: tuple[PdfHeaderFooterTemplate, ...] = (
    PdfHeaderFooterTemplate(name="Page x of y", footer_center="Page {page} of {pages}"),
    PdfHeaderFooterTemplate(name="Title and page number", header_left="{title}", footer_right="{page}"),
    PdfHeaderFooterTemplate(name="Confidential", header_center="CONFIDENTIAL", footer_center="Page {page} of {pages}", bold=True, color="#aa0000"),
    PdfHeaderFooterTemplate(name="Bates footer", footer_right="{bates:000001}", footer_left="{date}"),
)


# ---------------------------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------------------------


def _text_width(text: str, font: str, bold: bool, size: float) -> float:
    """Width in points. pdfminer ships the standard-14 metrics; without it, an average advance."""
    try:
        from pdfminer.fontmetrics import FONT_METRICS

        descriptor, widths = FONT_METRICS[_METRIC_NAMES[(font, bold)]]
        by_char = widths if isinstance(widths, dict) else {}
        total = 0.0
        for ch in text:
            total += by_char.get(ch, 556 if font != "courier" else 600)
        return total * size / 1000.0
    except Exception:
        return len(text) * size * (0.6 if font == "courier" else 0.52)


def _visible_box(page_obj: Any) -> tuple[float, float, float, float, int]:
    """(x0, y0, width, height, rotate) of the rectangle a person sees, before rotation is applied."""
    box = inherited(page_obj, "/CropBox")
    if box is None:
        box = inherited(page_obj, "/MediaBox")
    if box is None:
        box = [0, 0, 612, 792]
    x0, y0, x1, y1 = (float(v) for v in box)
    x0, x1 = min(x0, x1), max(x0, x1)
    y0, y1 = min(y0, y1), max(y0, y1)
    rotate = inherited(page_obj, "/Rotate")
    rot = int(rotate) % 360 if rotate is not None else 0
    return x0, y0, x1 - x0, y1 - y0, rot


def _visual_to_user(x0: float, y0: float, w: float, h: float, rot: int) -> tuple[float, float, float, float, float, float]:
    """Matrix taking the visible (rotated) space to the page's user space."""
    if rot == 90:
        return (0, 1, -1, 0, x0 + w, y0)
    if rot == 180:
        return (-1, 0, 0, -1, x0 + w, y0 + h)
    if rot == 270:
        return (0, -1, 1, 0, x0, y0 + h)
    return (1, 0, 0, 1, x0, y0)


def _num(value: float) -> str:
    text = f"{value:.4f}".rstrip("0").rstrip(".")
    return "0" if text in ("", "-0") else text


def _pdf_string(raw: bytes) -> bytes:
    return b"(" + raw.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)") + b")"


def _expand(text: str, *, page: int, pages: int, bates_index: int, spec: PdfStampSpec, title: str, today: str) -> str:
    def sub(match: re.Match[str]) -> str:
        token, arg = match.group(1), match.group(2)
        if token == "page":
            return str(page)
        if token == "pages":
            return str(pages)
        if token == "date":
            return today
        if token == "title":
            return title
        if arg is not None:
            start, width = int(arg), len(arg)
        else:
            start, width = spec.bates_start, spec.bates_digits
        return str(start + bates_index).zfill(width)

    return _TOKEN.sub(sub, text)


def _bates_range(specs: list[PdfStampSpec], count: int) -> tuple[str, str] | None:
    """First and last Bates number as text, from the first spec that uses the token."""
    for spec in specs:
        match = next((m for m in _TOKEN.finditer(spec.text) if m.group(1) == "bates"), None)
        if match and count:
            arg = match.group(2)
            start, width = (int(arg), len(arg)) if arg is not None else (spec.bates_start, spec.bates_digits)
            prefix = spec.text[: match.start()].strip()
            first, last = str(start).zfill(width), str(start + count - 1).zfill(width)
            return (f"{prefix}{first}", f"{prefix}{last}")
    return None


def _rgb(color: str) -> tuple[float, float, float]:
    h = color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4))  # type: ignore[return-value]


def _select_pages(page_count: int, pages: list[int] | None, page_ranges: list[Any] | None) -> list[int]:
    chosen: list[int] = []
    if pages:
        chosen.extend(pages)
    for r in page_ranges or []:
        start, end = (r.start, r.end) if hasattr(r, "start") else (r["start"], r["end"])
        chosen.extend(range(start, end + 1))
    if not pages and not page_ranges:
        return list(range(1, page_count + 1))
    bad = sorted({p for p in chosen if p < 1 or p > page_count})
    if bad:
        raise ValueError(f"This PDF has {page_count} pages. Page {bad[0]} does not exist.")
    return sorted(set(chosen))


# ---------------------------------------------------------------------------
# The engine
# ---------------------------------------------------------------------------


def stamp_pdf_bytes(
    pdf_bytes: bytes,
    specs: list[PdfStampSpec | dict[str, Any]],
    *,
    pages: list[int] | None = None,
    page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
    password: str = "",
    operation: str = "stamp",
    extra_metadata: dict[str, Any] | None = None,
) -> PdfBinaryResult:
    pikepdf = load_pikepdf()
    parsed = [s if isinstance(s, PdfStampSpec) else PdfStampSpec(**s) for s in specs]
    if not parsed:
        raise ValueError("Give at least one piece of text to stamp.")
    today = datetime.now(timezone.utc).date().isoformat()
    replaced = 0

    with open_pdf(pdf_bytes, password) as pdf:
        total = len(pdf.pages)
        chosen = _select_pages(total, pages, page_ranges)
        if not chosen:
            raise ValueError("Choose at least one page to stamp.")
        signed = is_signed(pdf)
        title = str(pdf.docinfo.get("/Title", "")) if pdf.docinfo is not None else ""

        font_objs: dict[tuple[str, bool], Any] = {}
        gs_objs: dict[int, Any] = {}

        def font_for(spec: PdfStampSpec) -> tuple[str, Any]:
            key = (spec.font, spec.bold)
            if key not in font_objs:
                font_objs[key] = pdf.make_indirect(
                    pikepdf.Dictionary(
                        Type=pikepdf.Name.Font, Subtype=pikepdf.Name.Type1,
                        BaseFont=pikepdf.Name("/" + _BASE_FONTS[key]), Encoding=pikepdf.Name.WinAnsiEncoding,
                    )
                )
            return f"MxF_{spec.font}_{'b' if spec.bold else 'r'}", font_objs[key]

        def gs_for(opacity: float) -> tuple[str, Any]:
            pct = int(round(opacity * 100))
            if pct not in gs_objs:
                gs_objs[pct] = pdf.make_indirect(pikepdf.Dictionary(Type=pikepdf.Name.ExtGState, ca=pct / 100.0, CA=pct / 100.0))
            return f"MxGS_{pct}", gs_objs[pct]

        for index, page_number in enumerate(chosen):
            page = pdf.pages[page_number - 1]
            x0, y0, w, h, rot = _visible_box(page.obj)
            vw, vh = (h, w) if rot in (90, 270) else (w, h)
            res = page.obj.get("/Resources")
            if res is None:
                inherited_res = inherited(page.obj, "/Resources")
                res = inherited_res if inherited_res is not None else pikepdf.Dictionary()
                page.obj.Resources = res
            if "/Font" not in res:
                res.Font = pikepdf.Dictionary()
            if "/ExtGState" not in res:
                res.ExtGState = pikepdf.Dictionary()

            front: list[bytes] = []
            behind: list[bytes] = []
            for spec in parsed:
                text = _expand(spec.text, page=page_number, pages=total, bates_index=index, spec=spec, title=title, today=today)
                encoded = text.encode("cp1252", errors="replace")
                if index == 0:
                    replaced += sum(1 for a, b in zip(text, encoded.decode("cp1252", errors="replace")) if a != b)
                fname, fobj = font_for(spec)
                gname, gobj = gs_for(spec.opacity)
                res.Font[f"/{fname}"] = fobj
                res.ExtGState[f"/{gname}"] = gobj
                tw = _text_width(text, spec.font, spec.bold, spec.size)
                row, col = spec.position.split("-") if "-" in spec.position else ("center", "center")
                px = {"left": spec.margin, "center": vw / 2 - tw / 2, "right": vw - spec.margin - tw}[col]
                py = {"top": vh - spec.margin - spec.size * 0.8, "center": vh / 2 - spec.size * 0.35, "bottom": spec.margin}[row]
                cx, cy = px + tw / 2, py + spec.size * 0.35
                r, g, b = _rgb(spec.color)
                theta = math.radians(spec.rotation)
                cos_t, sin_t = math.cos(theta), math.sin(theta)
                m = _visual_to_user(x0, y0, w, h, rot)
                chunk = b"\n".join(
                    [
                        b"q",
                        f"/{gname} gs".encode(),
                        f"{_num(r)} {_num(g)} {_num(b)} rg".encode(),
                        (" ".join(_num(v) for v in m) + " cm").encode(),
                        f"1 0 0 1 {_num(cx)} {_num(cy)} cm".encode(),
                        f"{_num(cos_t)} {_num(sin_t)} {_num(-sin_t)} {_num(cos_t)} 0 0 cm".encode(),
                        b"BT",
                        f"/{fname} {_num(spec.size)} Tf".encode(),
                        f"{_num(-tw / 2)} {_num(-spec.size * 0.35)} Td".encode(),
                        _pdf_string(encoded) + b" Tj",
                        b"ET",
                        b"Q",
                    ]
                )
                (behind if spec.behind else front).append(chunk)

            # Balance whatever the page already does, then lay the stamps over (or under) it.
            page.contents_add(pikepdf.Stream(pdf, b"q\n"), prepend=True)
            page.contents_add(pikepdf.Stream(pdf, b"\nQ\n"), prepend=False)
            if behind:
                page.contents_add(pikepdf.Stream(pdf, b"\n".join(behind) + b"\n"), prepend=True)
            if front:
                page.contents_add(pikepdf.Stream(pdf, b"\n".join(front) + b"\n"), prepend=False)

        bates = _bates_range(parsed, len(chosen))
        if bates:
            pdf.docinfo["/MatrxBatesFirst"] = bates[0]
            pdf.docinfo["/MatrxBatesLast"] = bates[1]
        content = save_pdf(pdf)

    metadata: dict[str, Any] = {
        "stamped_pages": chosen,
        "stamps": len(parsed),
        "replaced_characters": replaced,
        "signed": signed,
    }
    if bates:
        metadata["bates_first"], metadata["bates_last"] = bates
    metadata.update(extra_metadata or {})
    return PdfBinaryResult(content=content, page_count=total, operation=operation, metadata=metadata)


def apply_header_footer_bytes(
    pdf_bytes: bytes,
    template: PdfHeaderFooterTemplate | dict[str, Any],
    *,
    pages: list[int] | None = None,
    page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
    password: str = "",
) -> PdfBinaryResult:
    tpl = template if isinstance(template, PdfHeaderFooterTemplate) else PdfHeaderFooterTemplate(**template)
    specs = tpl.to_specs()
    if not specs:
        raise ValueError("The template has no text. Fill in at least one header or footer position.")
    return stamp_pdf_bytes(
        pdf_bytes, specs, pages=pages, page_ranges=page_ranges, password=password,
        operation="header_footer", extra_metadata={"template": tpl.name},
    )


async def stamp_pdf_bytes_async(pdf_bytes: bytes, specs: list[Any], **kwargs: Any) -> PdfBinaryResult:
    return await run_in_cpu_executor(lambda: stamp_pdf_bytes(pdf_bytes, specs, **kwargs))


async def apply_header_footer_bytes_async(pdf_bytes: bytes, template: Any, **kwargs: Any) -> PdfBinaryResult:
    return await run_in_cpu_executor(lambda: apply_header_footer_bytes(pdf_bytes, template, **kwargs))


__all__ = [
    "BUILTIN_HEADER_FOOTER_TEMPLATES",
    "PdfHeaderFooterTemplate",
    "PdfStampSpec",
    "StampFont",
    "StampPosition",
    "apply_header_footer_bytes",
    "apply_header_footer_bytes_async",
    "stamp_pdf_bytes",
    "stamp_pdf_bytes_async",
]
