"""Invisible text layer from words someone else recognised (a phone's Vision pass, Matrx Scan S2).

``ocr.py`` only drives OCRmyPDF, which recognises the words itself. This is the "words in" writer:
the caller hands each page its recognised words with their boxes in the page image's pixel space, and
every word is drawn in render mode 3 (invisible) over the place it sits, so the PDF is searchable,
selectable and copyable exactly where the picture shows the word.

Permissive stack only (pikepdf, PDF-PLAN decision 1 — never PyMuPDF). The font is a glyphless Type0
font (Identity-H, two-byte CIDs) with a ToUnicode CMap, the same idea as Tesseract's / OCRmyPDF's
GlyphLessFont: invisible text needs no glyph shapes, only the right Unicode behind each code, so ANY
language reads back — Cyrillic, Greek, Arabic, Hebrew, CJK, emoji (characters above U+FFFF map through
UTF-16 surrogate pairs in the CMap). Each distinct character in the document gets its own CID; words are
written in logical (typed) order, so right-to-left text copies out as it was typed. A word whose box is
not a finite number, or lands absurdly far off the page, is skipped and counted
(``metadata["skipped_words"]``), never written as ``nan`` into the content stream. A character is only
ever left out when a document carries more than 65,534 distinct characters; that is counted in
``metadata["replaced_characters"]`` — nothing is dropped silently.
"""

from __future__ import annotations

import base64
import math
import unicodedata
from collections.abc import Mapping, Sequence
from typing import Any

from pydantic import BaseModel, Field, field_validator

from ..concurrency import run_in_cpu_executor
from ._pike import inherited, open_pdf, save_pdf
from .stamp import _num, _visible_box, _visual_to_user

_FONT_NAME = "MxTextLayer"
_GLYPH_WIDTH = 500  # every CID is half an em wide; Tz stretches the word onto its box
_MAX_CID = 0xFFFE
_OFF_PAGE_FACTOR = 4.0  # a box more than this many page sizes away is nonsense, not a word

# A 660-byte TrueType with one glyph (GID 1): an advance of half an em and a full-height box outline,
# never painted (render mode 3). Embedding it — rather than leaving the font for each reader to
# substitute — gives every character a real box, so readers keep lone symbols (pdfium dropped a word
# that was a single "✅" when the font was not embedded). Built with fontTools' FontBuilder
# (unitsPerEm 1000, glyphs .notdef + glyph, both the 0,0..500,1000 rectangle); fontTools is not a
# runtime dependency, the bytes are the font.
_GLYPHLESS_TTF = base64.b64decode(
    "AAEAAAAKAIAAAwAgT1MvMkTeRSAAAAEoAAAAYGNtYXAADABGAAABkAAAACxnbHlmUcZiKAAAAcQAAAAwaGVhZC9LRAYAAACsAAAA"
    "NmhoZWEF3QH2AAAA5AAAACRobXR4AfQAAAAAAYgAAAAGbG9jYQAYAAwAAAG8AAAABm1heHAABAAGAAABCAAAACBuYW1lGZ8ZNAAA"
    "AfQAAABycG9zdG1/dc8AAAJoAAAALAABAAAAAQAA+4mjWV8PPPUAAwPoAAAAAOcgf58AAAAA5yB/nwAAAAAB9APoAAAAAwACAAAA"
    "AAAAAAEAAAPoAAAAAAH0AAAAAAH0AAEAAAAAAAAAAAAAAAAAAAABAAEAAAACAAQAAQAAAAAAAgAAAAAAAAAAAAAAAAAAAAAAAwH0"
    "AZAABQAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPz8/PwAAAAAAAAPoAAAAAAPoAAAA"
    "AAAAAAAAAAAAAAAAAAAgAAAB9AAAAAAAAAAAAAIAAAADAAAAFAADAAEAAAAUAAQAGAAAAAIAAgAAAAD//wAA//8AAQAAAAAADAAY"
    "AAAAAQAAAAAB9APoAAMAADERIREB9APo/BgAAQAAAAAB9APoAAMAADERIREB9APo/BgAAAAEADYAAQAAAAAAAQANAAAAAQAAAAAA"
    "AgAHAA0AAwABBAkAAQAaABQAAwABBAkAAgAOAC5HbHlwaExlc3NGb250UmVndWxhcgBHAGwAeQBwAGgATABlAHMAcwBGAG8AbgB0"
    "AFIAZQBnAHUAbABhAHIAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAECBWdseXBo"
)


#: Decimals a word box keeps (pixels): stored layers are rounded to this.
BOX_DECIMALS = 1


class LayerWord(BaseModel):
    """One recognised word: its text and its box ``[x0, y0, x1, y1]`` (pixels, origin top-left).

    ``angle`` is the direction the word reads in on the image, clockwise degrees (0 | 90 | 180 | 270):
    0 is upright, left to right; a page image turned 90 degrees clockwise turns its words to 90 (they read
    top to bottom). ``rotate_layer`` sets it; the writer draws the invisible word along that direction."""

    text: str
    box: tuple[float, float, float, float]
    angle: int = 0

    @field_validator("box")
    @classmethod
    def _tenth_of_a_pixel(cls, box: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
        # A tenth of a pixel is far below what a reader or a selection can show; full float precision
        # tripled every stored layer (one copy per page row, per version).
        return tuple(round(v, BOX_DECIMALS) if math.isfinite(v) else v for v in box)  # type: ignore[return-value]


class LayerPage(BaseModel):
    """One page's words, in the pixel space of an image ``width_px`` x ``height_px``.

    ``picture_box`` is where that image sits on the PDF page — ``(x0, y0, x1, y1)`` as fractions of the
    page's visible width and height, origin top-left — when the picture was fitted into a page of another
    shape (a page size the person picked: white margins around it). ``None`` = the image fills the page.
    The words are drawn over the picture, so they move and scale with it."""

    width_px: float = Field(gt=0, allow_inf_nan=False)
    height_px: float = Field(gt=0, allow_inf_nan=False)
    words: list[LayerWord] = Field(default_factory=list)
    picture_box: tuple[float, float, float, float] | None = None

    @field_validator("picture_box")
    @classmethod
    def _inside_the_page(cls, box: tuple[float, float, float, float] | None) -> tuple[float, float, float, float] | None:
        if box is None:
            return None
        x0, y0, x1, y1 = box
        if not (_finite(x0, y0, x1, y1) and -1e-6 <= x0 < x1 <= 1 + 1e-6 and -1e-6 <= y0 < y1 <= 1 + 1e-6):
            raise ValueError(f"picture_box {box} is not a box inside the page (fractions 0-1, x0 < x1, y0 < y1)")
        return box


def _utf16_hex(ch: str) -> str:
    return ch.encode("utf-16-be").hex().upper()


def _to_unicode_cmap(cids: Mapping[str, int]) -> bytes:
    items = sorted(cids.items(), key=lambda kv: kv[1])
    out = [
        "/CIDInit /ProcSet findresource begin", "12 dict begin", "begincmap",
        "/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def",
        "/CMapName /Adobe-Identity-UCS def", "/CMapType 2 def",
        "1 begincodespacerange", "<0000> <FFFF>", "endcodespacerange",
    ]
    for i in range(0, len(items), 100):
        chunk = items[i:i + 100]
        out.append(f"{len(chunk)} beginbfchar")
        out.extend(f"<{cid:04X}> <{_utf16_hex(ch)}>" for ch, cid in chunk)
        out.append("endbfchar")
    out += ["endcmap", "CMapName currentdict /CMap defineresource pop", "end", "end"]
    return ("\n".join(out) + "\n").encode("ascii")


def _glyphless_font(pdf: Any, cids: Mapping[str, int]) -> Any:
    import pikepdf

    descriptor = pdf.make_indirect(pikepdf.Dictionary(
        Type=pikepdf.Name.FontDescriptor, FontName=pikepdf.Name.GlyphLessFont, Flags=5,
        FontBBox=[0, 0, _GLYPH_WIDTH, 1000], ItalicAngle=0, Ascent=1000, Descent=0,
        CapHeight=1000, StemV=80, FontFile2=pdf.make_indirect(pikepdf.Stream(pdf, _GLYPHLESS_TTF)),
    ))
    # Every CID draws GID 1 of the embedded font; the meaning lives only in the ToUnicode CMap.
    cid_to_gid = b"\x00\x00" + b"\x00\x01" * len(cids)
    descendant = pdf.make_indirect(pikepdf.Dictionary(
        Type=pikepdf.Name.Font, Subtype=pikepdf.Name.CIDFontType2, BaseFont=pikepdf.Name.GlyphLessFont,
        CIDSystemInfo=pikepdf.Dictionary(Registry=pikepdf.String("Adobe"),
                                         Ordering=pikepdf.String("Identity"), Supplement=0),
        FontDescriptor=descriptor, DW=_GLYPH_WIDTH, CIDToGIDMap=pdf.make_indirect(pikepdf.Stream(pdf, cid_to_gid)),
    ))
    return pdf.make_indirect(pikepdf.Dictionary(
        Type=pikepdf.Name.Font, Subtype=pikepdf.Name.Type0, BaseFont=pikepdf.Name.GlyphLessFont,
        Encoding=pikepdf.Name("/Identity-H"), DescendantFonts=[descendant],
        ToUnicode=pdf.make_indirect(pikepdf.Stream(pdf, _to_unicode_cmap(cids))),
    ))


def _visual_order(word: str) -> str:
    """A word's characters in the left-to-right order they sit on the page.

    PDF readers (pdfium, pypdf, and the viewers built on them) rebuild right-to-left text from the
    glyphs' positions, so Arabic and Hebrew are written in visual order and copy back out in the
    order they were typed. A word with no right-to-left letter is returned unchanged. Inside a
    right-to-left word, runs of left-to-right letters and digits keep their own order. Marks
    (harakat, niqqud) are reversed with their letters — the readers expect them before the base in
    visual order and put them back after it.
    """
    if not any(unicodedata.bidirectional(c) in ("R", "AL") for c in word):
        return word
    runs: list[tuple[bool, list[str]]] = []
    for c in word:
        ltr = unicodedata.bidirectional(c) in ("L", "EN", "AN")
        if runs and runs[-1][0] == ltr:
            runs[-1][1].append(c)
        else:
            runs.append((ltr, [c]))
    return "".join("".join(r if ltr else r[::-1]) for ltr, r in reversed(runs))


#: Text matrix (a b c d) per word angle: the reading direction (a, b) and the glyphs' up (c, d) in PDF space
#: (y up). A clockwise turn on the image is a clockwise turn on the page.
_WORD_MATRIX = {0: "1 0 0 1", 90: "0 -1 1 0", 180: "-1 0 0 -1", 270: "0 1 -1 0"}


def rotate_layer(layer: LayerPage, degrees: int) -> LayerPage:
    """``layer`` as it lies on its image after the image is turned ``degrees`` clockwise (0 | 90 | 180 |
    270): every box moves with the pixels, the pixel size swaps on a quarter turn, and each word's reading
    direction turns with it — the same words, landing on the turned page where the picture now shows them.
    A turned layer has no ``picture_box``: where the turned picture sits is the new page's (the build says)."""
    turn = int(degrees) % 360
    if turn not in (0, 90, 180, 270):
        raise ValueError(f"a text layer turns by 0, 90, 180 or 270 degrees, not {degrees}")
    if turn == 0:
        return layer
    w, h = layer.width_px, layer.height_px

    def _point(x: float, y: float) -> tuple[float, float]:
        if turn == 90:
            return h - y, x
        if turn == 180:
            return w - x, h - y
        return y, w - x

    words = []
    for word in layer.words:
        x0, y0, x1, y1 = word.box
        (ax, ay), (bx, by) = _point(x0, y0), _point(x1, y1)
        words.append(LayerWord(text=word.text, box=(min(ax, bx), min(ay, by), max(ax, bx), max(ay, by)),
                               angle=(word.angle + turn) % 360))
    size = (h, w) if turn in (90, 270) else (w, h)
    return LayerPage(width_px=size[0], height_px=size[1], words=words)


def _finite(*values: float) -> bool:
    return all(math.isfinite(v) for v in values)


def add_text_layer_bytes(pdf_bytes: bytes, pages: Mapping[int, LayerPage]) -> tuple[bytes, dict[str, Any]]:
    """Return ``pdf_bytes`` with an invisible word layer on each page named in ``pages`` (1-based)."""
    pdf = open_pdf(pdf_bytes)
    import pikepdf

    cids: dict[str, int] = {}
    replaced = 0
    skipped = 0
    words_written = 0
    font = None
    with pdf:
        page_ops: list[tuple[Any, list[bytes]]] = []
        for page_number, layer in sorted(pages.items()):
            if not 1 <= page_number <= len(pdf.pages) or not layer.words:
                continue
            page = pdf.pages[page_number - 1]
            x0, y0, w, h, rot = _visible_box(page.obj)
            vw, vh = (h, w) if rot in (90, 270) else (w, h)
            # The words sit on the picture: over the whole page, or over the box a fitted picture fills.
            fx0, fy0, fx1, fy1 = layer.picture_box or (0.0, 0.0, 1.0, 1.0)
            sx, sy = vw * (fx1 - fx0) / layer.width_px, vh * (fy1 - fy0) / layer.height_px
            dx, dy = vw * fx0, vh * fy0
            ops: list[bytes] = [b"q", " ".join(_num(v) for v in _visual_to_user(x0, y0, w, h, rot)).encode() + b" cm",
                                b"BT", b"3 Tr"]
            for word in layer.words:
                text = word.text.strip()
                if not text:
                    continue
                bx0, by0, bx1, by1 = word.box
                if not _finite(bx0, by0, bx1, by1):
                    skipped += 1
                    continue
                # Baseline origin, reading direction and glyph height by the word's angle: upright words sit on
                # the box's bottom-left corner; a turned word starts at the corner its first letter turned to.
                angle = word.angle % 360
                if angle in (90, 270):
                    size, box_w = max((bx1 - bx0) * sx, 1.0), max((by1 - by0) * sy, 0.1)
                else:
                    size, box_w = max((by1 - by0) * sy, 1.0), max((bx1 - bx0) * sx, 0.1)
                ox, oy = {0: (bx0, by1), 90: (bx0, by0), 180: (bx1, by0), 270: (bx1, by1)}.get(angle, (bx0, by1))
                matrix = _WORD_MATRIX.get(angle, _WORD_MATRIX[0])
                px, py = dx + ox * sx, vh - (dy + oy * sy)
                limit_x, limit_y = vw * _OFF_PAGE_FACTOR, vh * _OFF_PAGE_FACTOR
                if (not _finite(size, box_w, px, py) or size > limit_y or box_w > limit_x
                        or abs(px) > limit_x or abs(py) > limit_y):
                    skipped += 1
                    continue
                codes = bytearray()
                for ch in _visual_order(text):
                    cid = cids.get(ch)
                    if cid is None:
                        if len(cids) >= _MAX_CID:
                            replaced += 1
                            continue
                        cid = cids[ch] = len(cids) + 1
                    codes += cid.to_bytes(2, "big")
                if not codes:
                    continue
                natural = (len(codes) // 2) * size * _GLYPH_WIDTH / 1000.0
                ops.append(f"/{_FONT_NAME} {_num(size)} Tf".encode())
                ops.append(f"{_num(100.0 * box_w / natural)} Tz".encode())
                ops.append(f"{matrix} {_num(px)} {_num(py)} Tm".encode())
                ops.append(b"<" + codes.hex().upper().encode() + b"> Tj")
                words_written += 1
            ops += [b"ET", b"Q"]
            page_ops.append((page, ops))
        if page_ops:
            font = _glyphless_font(pdf, cids)
        for page, ops in page_ops:
            res = page.obj.get("/Resources")
            if res is None:
                inherited_res = inherited(page.obj, "/Resources")
                res = inherited_res if inherited_res is not None else pikepdf.Dictionary()
                page.obj.Resources = res
            if "/Font" not in res:
                res.Font = pikepdf.Dictionary()
            res.Font[f"/{_FONT_NAME}"] = font
            page.contents_add(pikepdf.Stream(pdf, b"\n".join(ops) + b"\n"), prepend=False)
        out = save_pdf(pdf)
    return out, {
        "pages": len(pages), "words": words_written, "skipped_words": skipped,
        "replaced_characters": replaced, "distinct_characters": len(cids),
    }


async def add_text_layer_bytes_async(
    pdf_bytes: bytes, pages: Mapping[int, LayerPage]
) -> tuple[bytes, dict[str, Any]]:
    return await run_in_cpu_executor(add_text_layer_bytes, pdf_bytes, pages)


def box_of(box: Any) -> tuple[float, float, float, float] | None:
    """``(x0, y0, x1, y1)`` of a box given as four numbers or as a quad (``top_left`` .. ``bottom_left``)."""
    if box is None:
        return None
    corners = [
        getattr(box, name, None) if not isinstance(box, Mapping) else box.get(name)
        for name in ("top_left", "top_right", "bottom_right", "bottom_left")
    ]
    if all(c is not None for c in corners):
        xs = [float(c[0]) for c in corners]
        ys = [float(c[1]) for c in corners]
        return min(xs), min(ys), max(xs), max(ys)
    x0, y0, x1, y1 = (float(v) for v in box)
    return x0, y0, x1, y1


def words_from_lines(lines: Sequence[Any]) -> list[LayerWord]:
    """Flatten recognised lines (each with ``words``, else its own ``text`` and ``box``) to words."""
    words: list[LayerWord] = []
    for line in lines:
        line_words = list(getattr(line, "words", None) or [])
        if line_words:
            words.extend(LayerWord(text=wd.text, box=box_of(wd.box)) for wd in line_words if box_of(wd.box))
        elif box_of(getattr(line, "box", None)) and getattr(line, "text", ""):
            words.append(LayerWord(text=line.text, box=box_of(line.box)))
    return words


__all__ = ["LayerPage", "LayerWord", "box_of", "rotate_layer", "add_text_layer_bytes", "add_text_layer_bytes_async", "words_from_lines"]
