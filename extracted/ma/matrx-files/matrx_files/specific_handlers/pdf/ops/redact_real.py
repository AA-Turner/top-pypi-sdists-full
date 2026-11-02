"""PDF-PLAN U12: redaction that really removes content, on the permissive stack (pikepdf, pdfplumber,
pypdfium2, Pillow). Never PyMuPDF (the guard ``scripts/check_no_new_pymupdf_imports.py`` fails a new importer).

What "removed" means here, for every box:

- text: the glyphs under the box are cut out of the page's content stream (and of any form XObject it
  draws); the advance of each cut glyph is kept so the rest of the line does not move;
- images: the pixels under the box are blanked in a fresh copy of the image (shared images are never edited
  in place); inline images under the box are dropped;
- annotations and form fields whose rectangle touches the box are deleted and the field tree is pruned;
- metadata and XMP text equal to a removed string is deleted, outline titles too; page thumbnails are dropped;
- a solid box is painted last so the page still shows where something was.

Nothing is trusted: every page is re-read after the rewrite (pdfplumber characters, pypdfium2 text and the image
pixels under each box). A page that cannot be PROVEN clean (an unreadable font encoding, an image that will not
decode, text the rewrite missed) is flattened to a picture of itself with the boxes burned in, and the result
says so (``tier``: stream_rewrite, rasterize or mixed).

Coordinates in and out are the VISIBLE page in points, origin top-left (what the viewer shows: crop box and
rotation applied). The removed text is held in memory only to scrub metadata; it is never returned in an audit
and never stored.
"""

from __future__ import annotations

import io
import re
import zlib
from decimal import Decimal
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

from ..concurrency import run_in_cpu_executor
from ..models import PdfBinaryResult
from ._pike import inherited, load_pikepdf, open_pdf, save_pdf
from .stamp import _num, _visible_box, _visual_to_user

_MAX_DEPTH = 8
_RASTER_DPI = 200


class RedactBox(BaseModel):
    """One region to remove, on the visible page, points, origin top-left."""

    page_number: int = Field(ge=1)
    x0: float
    y0: float
    x1: float
    y1: float

    @model_validator(mode="after")
    def _ordered(self) -> "RedactBox":
        if self.x1 <= self.x0 or self.y1 <= self.y0:
            raise ValueError("A redaction box needs x1 > x0 and y1 > y0.")
        return self


class RedactSanitize(BaseModel):
    """Whole-file clean-up that goes with a redaction."""

    #: Removed strings are always taken out of metadata; True also wipes Info and XMP entirely.
    clear_metadata: bool = False
    attachments: bool = True
    javascript: bool = True


Rect = tuple[float, float, float, float]

# ---------------------------------------------------------------------------
# Find (read-only): review before apply
# ---------------------------------------------------------------------------


class RedactFindSpec(BaseModel):
    pii: bool = True
    tier: Literal["low", "medium", "high"] = "medium"
    #: Pattern-catalog ids (``redact/patterns.PATTERN_CATALOG``) in addition to the personal-information set.
    pattern_ids: list[str] = Field(default_factory=list)
    literals: list[str] = Field(default_factory=list, max_length=50)
    regexes: list[str] = Field(default_factory=list, max_length=20)
    case_sensitive: bool = False


def _catalog_matchers(spec: RedactFindSpec) -> list[tuple[str, str, re.Pattern[str], Any]]:
    """The existing analysis PII detector's patterns and validators, reused as they are."""
    from ..redact.patterns import PATTERN_CATALOG
    from ..redact.validators import VALIDATORS

    out: list[tuple[str, str, re.Pattern[str], Any]] = []
    wanted = set(spec.pattern_ids)
    for entry in PATTERN_CATALOG:
        pid = entry["id"]
        use = pid in wanted or (spec.pii and entry.get("category") == "pii" and spec.tier in entry.get("tiers", ()))
        if not use:
            continue
        rx = (entry.get("tier_regex") or {}).get(spec.tier) or entry.get("regex")
        if not rx:
            continue
        out.append((pid, entry.get("label", pid), re.compile(rx, entry.get("flags", 0)), VALIDATORS.get(entry.get("validator") or "")))
    return out


def _page_lines(page: Any) -> list[tuple[str, list[Any]]]:
    """Text lines of a pdfplumber page as (text, owner char per text index, None for a space)."""
    chars = [c for c in page.chars if c.get("text")]
    if not chars:
        return []
    chars.sort(key=lambda c: (c["top"], c["x0"]))
    lines: list[list[Any]] = []
    for c in chars:
        for line in lines:
            if abs(line[0]["top"] - c["top"]) <= 3.0:
                line.append(c)
                break
        else:
            lines.append([c])
    out: list[tuple[str, list[Any]]] = []
    for line in sorted(lines, key=lambda ln: ln[0]["top"]):
        line.sort(key=lambda c: c["x0"])
        text: list[str] = []
        owners: list[Any] = []
        prev = None
        for c in line:
            if prev is not None and c["x0"] - prev["x1"] > max(1.0, 0.25 * (prev["x1"] - prev["x0"])) and not prev["text"].isspace():
                text.append(" ")
                owners.append(None)
            for ch in c["text"]:
                text.append(ch)
                owners.append(c if not ch.isspace() else None)
            prev = c
        out.append(("".join(text), owners))
    return out


def _frame(page: Any) -> tuple[float, float]:
    """Offset to subtract from pdfplumber coordinates to reach the viewer's visible frame."""
    return float(page.bbox[0]), float(page.bbox[1])


def _plain(pdf_bytes: bytes, password: str) -> bytes:
    """pdfplumber and pdfium read plain bytes: a file opened with a password is re-saved without one first."""
    if not password:
        return pdf_bytes
    with open_pdf(pdf_bytes, password) as pdf:
        return save_pdf(pdf)


def _unrotated(plain: bytes) -> tuple[bytes, list[int], list[tuple[float, float]]]:
    """A copy with /Rotate removed (text reads in lines), plus each page's rotation and unrotated size."""
    with open_pdf(plain) as pdf:
        rots, sizes = [], []
        for page in pdf.pages:
            x0, y0, w, h, rot = _visible_box(page.obj)
            rots.append(rot)
            sizes.append((w, h))
            if "/Rotate" in page.obj:
                page.obj.Rotate = 0
            elif inherited(page.obj, "/Rotate") is not None:
                page.obj.Rotate = 0
        return save_pdf(pdf), rots, sizes


def _to_visible(x0: float, y0: float, x1: float, y1: float, rot: int, w: float, h: float) -> Rect:
    """Map a top-left box on the unrotated page to the page as displayed (clockwise /Rotate)."""
    if rot == 90:
        pts = [(h - y0, x0), (h - y1, x1)]
    elif rot == 180:
        pts = [(w - x0, h - y0), (w - x1, h - y1)]
    elif rot == 270:
        pts = [(y0, w - x0), (y1, w - x1)]
    else:
        return x0, y0, x1, y1
    return min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)


def find_redaction_hits_bytes(pdf_bytes: bytes, spec: RedactFindSpec | dict[str, Any], *, password: str = "") -> dict[str, Any]:
    """Every place the spec matches, as boxes the person reviews before anything is changed. ``text`` is the
    matched text so the reviewer can accept or reject it; the response goes to the file's owner and is never stored."""
    import pdfplumber

    spec = spec if isinstance(spec, RedactFindSpec) else RedactFindSpec(**spec)
    flags = 0 if spec.case_sensitive else re.IGNORECASE
    matchers = _catalog_matchers(spec)
    for lit in spec.literals:
        if lit.strip():
            matchers.append(("literal", "Words you entered", re.compile(re.escape(lit.strip()), flags), None))
    for rx in spec.regexes:
        try:
            matchers.append(("regex", "Custom pattern", re.compile(rx, flags), None))
        except re.error as exc:
            raise ValueError(f"That pattern is not a valid regular expression: {exc}") from exc
    if not matchers:
        raise ValueError("Choose what to look for: personal information, a pattern, words or a regular expression.")

    hits: list[dict[str, Any]] = []
    textless: list[int] = []
    flat, rotations, sizes = _unrotated(_plain(pdf_bytes, password))
    with pdfplumber.open(io.BytesIO(flat)) as doc:
        page_count = len(doc.pages)
        for pno, page in enumerate(doc.pages, start=1):
            lines = _page_lines(page)
            if not lines:
                textless.append(pno)
                continue
            ox, oy = _frame(page)
            seen: set[tuple[int, int, int, str]] = set()
            for li, (text, owners) in enumerate(lines):
                for pid, label, rx, validator in matchers:
                    for m in rx.finditer(text):
                        raw = m.group(0)
                        if not raw.strip() or (validator is not None and not validator(raw)):
                            continue
                        span = [c for c in owners[m.start():m.end()] if c is not None]
                        key = (li, m.start(), m.end(), pid)
                        if not span or key in seen:
                            continue
                        seen.add(key)
                        bx0, by0, bx1, by1 = _to_visible(
                            min(c["x0"] for c in span) - ox, min(c["top"] for c in span) - oy,
                            max(c["x1"] for c in span) - ox, max(c["bottom"] for c in span) - oy,
                            rotations[pno - 1], *sizes[pno - 1],
                        )
                        hits.append(
                            {
                                "hit_id": f"p{pno}-l{li}-{m.start()}-{pid}",
                                "page_number": pno,
                                "x0": round(bx0, 2), "y0": round(by0, 2), "x1": round(bx1, 2), "y1": round(by1, 2),
                                "pattern_id": pid,
                                "label": label,
                                "text": raw,
                            }
                        )
    return {"hits": hits, "page_count": page_count, "pages_without_text": textless}


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------


def _user_rect(page_obj: Any, box: RedactBox) -> Rect:
    """The box in the page's user space (axis-aligned: rotation is a multiple of 90)."""
    x0, y0, w, h, rot = _visible_box(page_obj)
    vh = w if rot in (90, 270) else h
    a, b, c, d, e, f = _visual_to_user(x0, y0, w, h, rot)
    pts = [(box.x0, vh - box.y0), (box.x1, vh - box.y0), (box.x1, vh - box.y1), (box.x0, vh - box.y1)]
    xs = [a * X + c * Y + e for X, Y in pts]
    ys = [b * X + d * Y + f for X, Y in pts]
    return min(xs), min(ys), max(xs), max(ys)


def _inside(r: Rect, x: float, y: float) -> bool:
    return r[0] <= x <= r[2] and r[1] <= y <= r[3]


def _overlaps(a: Rect, b: Rect) -> bool:
    return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]


def _inverse(m: Any) -> Any:
    """Inverse of a PDF matrix (computed here: ``Matrix.inverse()`` is not trusted)."""
    det = m.a * m.d - m.b * m.c
    if abs(det) < 1e-12:
        raise ValueError("degenerate matrix")
    a, b, c, d = m.d / det, -m.b / det, -m.c / det, m.a / det
    return load_pikepdf().Matrix(a, b, c, d, -(m.e * a + m.f * c), -(m.e * b + m.f * d))


def _quad_rect(ctm: Any, pts: Any) -> Rect:
    q = [ctm.transform(p) for p in pts]
    return min(p[0] for p in q), min(p[1] for p in q), max(p[0] for p in q), max(p[1] for p in q)


# ---------------------------------------------------------------------------
# Fonts: how wide each glyph is, to know where it sits
# ---------------------------------------------------------------------------


class _Font:
    def __init__(self, font: Any) -> None:
        self.two_byte = False
        self.exact = True
        self._widths: dict[int, float] = {}
        self._default = 0.0
        self._metrics: dict[str, float] | None = None
        subtype = str(font.get("/Subtype", ""))
        if subtype == "/Type0":
            self._type0(font)
        else:
            self._simple(font, subtype)

    def _type0(self, font: Any) -> None:
        self.two_byte = True
        enc = font.get("/Encoding")
        self.exact = enc is not None and not hasattr(enc, "read_bytes") and str(enc).startswith("/Identity")
        desc = (font.get("/DescendantFonts") or [None])[0]
        self._default = float(desc.get("/DW", 1000)) if desc is not None else 1000.0
        items = list(desc.get("/W") or []) if desc is not None else []
        i = 0
        while i < len(items):
            first = int(items[i])
            nxt = items[i + 1] if i + 1 < len(items) else None
            if nxt is not None and hasattr(nxt, "__iter__") and not isinstance(nxt, (int, float, Decimal)):
                for k, wv in enumerate(nxt):
                    self._widths[first + k] = float(wv)
                i += 2
            else:
                if i + 2 < len(items):
                    for code in range(first, int(items[i + 1]) + 1):
                        self._widths[code] = float(items[i + 2])
                i += 3

    def _simple(self, font: Any, subtype: str) -> None:
        widths = font.get("/Widths")
        first = int(font.get("/FirstChar", 0))
        desc = font.get("/FontDescriptor")
        self._default = float(desc.get("/MissingWidth", 0)) if desc is not None else 0.0
        if widths is not None:
            scale = 1.0
            if subtype == "/Type3":
                fm = font.get("/FontMatrix")
                scale = float(fm[0]) * 1000.0 if fm else 1.0
            for k, wv in enumerate(widths):
                self._widths[first + k] = float(wv) * scale
            return
        base = str(font.get("/BaseFont", "")).lstrip("/").split("+", 1)[-1].replace(" ", "").lower()
        try:
            from pdfminer.fontmetrics import FONT_METRICS
        except Exception:  # pragma: no cover
            FONT_METRICS = {}  # type: ignore[assignment]
        bold = "bold" in base
        if "courier" in base:
            key = "Courier-Bold" if bold else "Courier"
        elif "times" in base:
            key = "Times-Bold" if bold else "Times-Roman"
        else:
            key = "Helvetica-Bold" if bold else "Helvetica"
        if key in FONT_METRICS and any(s in base for s in ("helvetica", "arial", "times", "courier")):
            self._metrics = FONT_METRICS[key][1]
            self._default = 556.0
        else:
            self.exact = False
            self._default = 500.0

    def split(self, raw: bytes) -> list[tuple[int, int]]:
        if self.two_byte:
            return [(int.from_bytes(raw[i:i + 2].ljust(2, b"\0"), "big"), min(2, len(raw) - i)) for i in range(0, len(raw), 2)]
        return [(b, 1) for b in raw]

    def width(self, code: int) -> float:
        if code in self._widths:
            return self._widths[code]
        if self._metrics is not None:
            return float(self._metrics.get(bytes([code & 0xFF]).decode("cp1252", errors="replace"), self._default))
        return self._default

    def encode(self, code: int, nbytes: int) -> bytes:
        return code.to_bytes(2, "big")[:nbytes] if nbytes == 2 else bytes([code & 0xFF])


# ---------------------------------------------------------------------------
# Content-stream rewrite (and, with ``check_only``, the proof pass over the result)
# ---------------------------------------------------------------------------


class _Stats:
    def __init__(self) -> None:
        self.glyphs = 0
        self.images = 0
        self.inline_images = 0
        self.unproven: list[str] = []

    def mark(self) -> tuple[int, int, int, int]:
        return self.glyphs, self.images, self.inline_images, len(self.unproven)


class _Rewriter:
    def __init__(self, pdf: Any, rects: list[Rect], stats: _Stats, check_only: bool = False) -> None:
        self.pdf = pdf
        self.rects = rects
        self.stats = stats
        self.check_only = check_only
        self._fonts: dict[Any, _Font | None] = {}
        self._serial = 0

    def _hit(self, x: float, y: float) -> bool:
        return any(_inside(r, x, y) for r in self.rects)

    def _touches(self, rect: Rect) -> bool:
        return any(_overlaps(rect, r) for r in self.rects)

    def _fresh_name(self, res: Any, kind: str, prefix: str) -> str:
        if kind not in res:
            res[kind] = load_pikepdf().Dictionary()
        while True:
            self._serial += 1
            name = f"/{prefix}{self._serial}"
            if name not in res[kind]:
                return name

    def own(self, res: Any) -> Any:
        """A private copy of a resource dictionary, so one shared with other pages is never edited for them."""
        pikepdf = load_pikepdf()
        new = pikepdf.Dictionary()
        for k, v in res.items():
            if k in ("/XObject", "/Font") and v._type_code == pikepdf.ObjectType.dictionary:
                new[k] = pikepdf.Dictionary({kk: vv for kk, vv in v.items()})
            else:
                new[k] = v
        return new

    def _font(self, res: Any, name: Any) -> _Font | None:
        fonts = res.get("/Font") if res is not None else None
        fobj = fonts.get(str(name)) if fonts is not None else None
        if fobj is None:
            return None
        key = fobj.objgen if getattr(fobj, "is_indirect", False) else id(fobj)
        if key not in self._fonts:
            try:
                self._fonts[key] = _Font(fobj)
            except Exception:
                self._fonts[key] = None
        return self._fonts[key]

    def run(self, instructions: Any, res: Any, ctm: Any, depth: int = 0) -> list[Any]:
        pikepdf = load_pikepdf()
        Matrix, Ins, Op = pikepdf.Matrix, pikepdf.ContentStreamInstruction, pikepdf.Operator
        out: list[Any] = []
        gstack: list[tuple[Any, tuple[Any, ...]]] = []
        tc = tw = rise = size = tl = 0.0
        tz = 1.0
        font: _Font | None = None
        tm = tlm = Matrix()

        for ins in instructions:
            if isinstance(ins, pikepdf.ContentStreamInlineImage):
                if self._touches(_quad_rect(ctm, ((0, 0), (1, 0), (1, 1), (0, 1)))):
                    if self.check_only:
                        self.stats.unproven.append("an inline image is under the box")
                    else:
                        self.stats.inline_images += 1
                        continue
                out.append(ins)
                continue
            ops, op = list(ins.operands), str(ins.operator)
            if op == "q":
                gstack.append((ctm, (tc, tw, tz, tl, rise, size, font)))
            elif op == "Q":
                if gstack:
                    ctm, (tc, tw, tz, tl, rise, size, font) = gstack.pop()
            elif op == "cm":
                ctm = Matrix(*[float(v) for v in ops]) @ ctm
            elif op == "BT":
                tm = tlm = Matrix()
            elif op == "Tc":
                tc = float(ops[0])
            elif op == "Tw":
                tw = float(ops[0])
            elif op == "Tz":
                tz = float(ops[0]) / 100.0
            elif op == "TL":
                tl = float(ops[0])
            elif op == "Ts":
                rise = float(ops[0])
            elif op == "Tf":
                font, size = self._font(res, ops[0]), float(ops[1])
            elif op in ("Td", "TD"):
                tx, ty = float(ops[0]), float(ops[1])
                if op == "TD":
                    tl = -ty
                tlm = Matrix(1, 0, 0, 1, tx, ty) @ tlm
                tm = tlm
            elif op == "Tm":
                tm = tlm = Matrix(*[float(v) for v in ops])
            elif op == "T*":
                tlm = Matrix(1, 0, 0, 1, 0, -tl) @ tlm
                tm = tlm
            elif op in ("Tj", "TJ", "'", '"'):
                if op == "'":
                    tlm = Matrix(1, 0, 0, 1, 0, -tl) @ tlm
                    tm = tlm
                elif op == '"':
                    tw, tc = float(ops[0]), float(ops[1])
                    tlm = Matrix(1, 0, 0, 1, 0, -tl) @ tlm
                    tm = tlm
                items = list(ops[0]) if op == "TJ" else [ops[-1]]
                new_items, tm, changed = self._show(items, font, size, tc, tw, tz, rise, tm, ctm)
                if not changed:
                    out.append(ins)
                    continue
                if op == "'":
                    out.append(Ins([], Op("T*")))
                elif op == '"':
                    out += [Ins([ops[0]], Op("Tw")), Ins([ops[1]], Op("Tc")), Ins([], Op("T*"))]
                out.append(Ins([pikepdf.Array(new_items)], Op("TJ")))
                continue
            elif op == "Do" and ops:
                swapped = self._do(ops[0], res, ctm, depth)
                if swapped is not None:
                    out.append(Ins([pikepdf.Name(swapped)], Op("Do")))
                    continue
            out.append(ins)
        return out

    def _show(self, items: list[Any], font: _Font | None, size: float, tc: float, tw: float, tz: float, rise: float, tm: Any, ctm: Any):
        pikepdf = load_pikepdf()
        has_text = any(isinstance(i, pikepdf.String) for i in items)
        if has_text and (font is None or size == 0):
            self.stats.unproven.append("text whose font could not be read")
            return items, tm, False
        if has_text and not font.exact:
            self.stats.unproven.append("text in a font whose glyph widths are estimated")
        full = tm @ ctm
        x = 0.0
        out: list[Any] = []
        changed = False
        for item in items:
            if not isinstance(item, pikepdf.String):
                x += -float(item) / 1000.0 * size * tz
                out.append(item)
                continue
            raw, keep = bytes(item), bytearray()
            for code, nbytes in font.split(raw):
                w = font.width(code)
                space = tw if (nbytes == 1 and code == 32) else 0.0
                px, py = full.transform((x + (w / 2000.0 * size) * tz, rise + 0.3 * size))
                if self._hit(px, py):
                    if keep:
                        out.append(pikepdf.String(bytes(keep)))
                        keep = bytearray()
                    out.append(round(-(w + (tc + space) * 1000.0 / size), 3))
                    self.stats.glyphs += 1
                    changed = True
                else:
                    keep += font.encode(code, nbytes)
                x += (w / 1000.0 * size + tc + space) * tz
            if keep:
                out.append(pikepdf.String(bytes(keep)))
        return out, pikepdf.Matrix(1, 0, 0, 1, x, 0) @ tm, changed

    def _do(self, name: Any, res: Any, ctm: Any, depth: int) -> str | None:
        pikepdf = load_pikepdf()
        xobjs = res.get("/XObject") if res is not None else None
        xo = xobjs.get(str(name)) if xobjs is not None else None
        if xo is None:
            return None
        subtype = str(xo.get("/Subtype", ""))
        if subtype == "/Image":
            if not self._touches(_quad_rect(ctm, ((0, 0), (1, 0), (1, 1), (0, 1)))):
                return None
            new = self._blank_image(xo, ctm)
            if new is None:
                return None
            key = self._fresh_name(res, "/XObject", "MxRedImg")
            res.XObject[key] = new
            self.stats.images += 1
            return key
        if subtype == "/Form" and depth < _MAX_DEPTH:
            matrix = xo.get("/Matrix")
            inner = (pikepdf.Matrix(*[float(v) for v in matrix]) if matrix is not None else pikepdf.Matrix()) @ ctm
            bbox = xo.get("/BBox")
            if bbox is not None:
                bx0, by0, bx1, by1 = (float(v) for v in bbox)
                if not self._touches(_quad_rect(inner, ((bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1)))):
                    return None
            fres = self.own(xo.get("/Resources") if xo.get("/Resources") is not None else res)
            before = self.stats.mark()
            rewritten = self.run(pikepdf.parse_content_stream(xo), fres, inner, depth + 1)
            if self.check_only or before == self.stats.mark():
                return None
            new = pikepdf.Stream(self.pdf, pikepdf.unparse_content_stream(rewritten))
            for k, v in xo.items():
                if k not in ("/Length", "/Filter", "/DecodeParms", "/Resources"):
                    new[k] = v
            new.Resources = fres
            key = self._fresh_name(res, "/XObject", "MxRedForm")
            res.XObject[key] = new
            return key
        return None

    def _blank_image(self, xo: Any, ctm: Any) -> Any | None:
        pikepdf = load_pikepdf()
        try:
            from PIL import ImageDraw

            if xo.get("/ImageMask"):
                raise ValueError("stencil mask")
            pil = pikepdf.PdfImage(xo).as_pil_image()
        except Exception:
            self.stats.unproven.append("an image under the box could not be decoded")
            return None
        w, h = pil.size
        inv = _inverse(ctm)
        boxes: list[tuple[int, int, int, int]] = []
        for r in self.rects:
            pts = [inv.transform(p) for p in ((r[0], r[1]), (r[2], r[1]), (r[2], r[3]), (r[0], r[3]))]
            us, vs = [p[0] for p in pts], [p[1] for p in pts]
            u0, u1, v0, v1 = max(0.0, min(us)), min(1.0, max(us)), max(0.0, min(vs)), min(1.0, max(vs))
            if u1 > u0 and v1 > v0:
                boxes.append((int(u0 * w), int((1 - v1) * h), min(w, int(u1 * w) + 1), min(h, int((1 - v0) * h) + 1)))
        if not boxes:
            return None
        gray = pil.mode in ("L", "1")
        pil = pil.convert("L" if gray else "RGB")
        if self.check_only:
            if any(pil.crop(b).getbbox() is not None for b in boxes):
                self.stats.unproven.append("image pixels under the box are not blank")
            return None
        draw = ImageDraw.Draw(pil)
        for b in boxes:
            draw.rectangle((b[0], b[1], b[2] - 1, b[3] - 1), fill=0)
        new = pikepdf.Stream(self.pdf, zlib.compress(pil.tobytes()))
        new.Type, new.Subtype = pikepdf.Name.XObject, pikepdf.Name.Image
        new.Width, new.Height, new.BitsPerComponent = w, h, 8
        new.ColorSpace = pikepdf.Name.DeviceGray if gray else pikepdf.Name.DeviceRGB
        new.Filter = pikepdf.Name.FlateDecode
        return new


# ---------------------------------------------------------------------------
# Apply
# ---------------------------------------------------------------------------


def _text_under(plain: bytes, boxes: list[RedactBox]) -> list[str]:
    """The text inside the boxes, read from the ORIGINAL file; held in memory to scrub metadata, never stored."""
    import pdfplumber

    found: list[str] = []
    with pdfplumber.open(io.BytesIO(plain)) as doc:
        for b in boxes:
            if b.page_number > len(doc.pages):
                continue
            page = doc.pages[b.page_number - 1]
            ox, oy = _frame(page)
            words = [
                c for c in page.chars
                if b.x0 <= (c["x0"] + c["x1"]) / 2 - ox <= b.x1 and b.y0 <= (c["top"] + c["bottom"]) / 2 - oy <= b.y1
            ]
            words.sort(key=lambda c: (round(c["top"]), c["x0"]))
            s = "".join(c["text"] for c in words).strip()
            if s:
                found.append(s)
    return found


def _fill_ops(rects: list[Rect]) -> bytes:
    body = ["q", "0 g"] + [f"{_num(r[0])} {_num(r[1])} {_num(r[2] - r[0])} {_num(r[3] - r[1])} re f" for r in rects] + ["Q"]
    return ("\n".join(body) + "\n").encode()


def _prune_fields(pdf: Any, gone: set[tuple[int, int]]) -> int:
    """Drop the form fields (and kids) whose widget was removed. Returns how many fields went."""
    acro = pdf.Root.get("/AcroForm")
    if acro is None or "/Fields" not in acro:
        return 0
    removed = 0

    def keep(node: Any) -> bool:
        nonlocal removed
        if node.is_indirect and node.objgen in gone:
            removed += 1
            return False
        if "/Kids" in node:
            kids = [k for k in node.Kids if keep(k)]
            if not kids:
                if not node.is_indirect or node.objgen not in gone:
                    removed += 1
                return False
            node.Kids = load_pikepdf().Array(kids)
        return True

    pikepdf = load_pikepdf()
    acro.Fields = pikepdf.Array([f for f in acro.Fields if keep(f)])
    return removed


def _strip_annotations(pdf: Any, page: Any, rects: list[Rect]) -> tuple[int, int, set[tuple[int, int]]]:
    pikepdf = load_pikepdf()
    annots = page.obj.get("/Annots")
    if annots is None:
        return 0, 0, set()
    kept, gone = [], set()
    count = fields = 0
    removed_objs = []
    for a in annots:
        rect = a.get("/Rect")
        if rect is not None:
            x0, y0, x1, y1 = (float(v) for v in rect)
            hit = any(_overlaps((min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)), r) for r in rects)
        else:
            hit = False
        if hit:
            count += 1
            fields += 1 if str(a.get("/Subtype")) == "/Widget" else 0
            removed_objs.append(a)
            if a.is_indirect:
                gone.add(a.objgen)
        else:
            kept.append(a)
    final = []
    for a in kept:  # a popup of a removed note goes with it
        parent = a.get("/Parent")
        if str(a.get("/Subtype")) == "/Popup" and parent is not None and parent.is_indirect and parent.objgen in gone:
            count += 1
            continue
        final.append(a)
    if final:
        page.obj.Annots = pikepdf.Array(final)
    else:
        del page.obj["/Annots"]
    return count, fields, gone


def _scrub_metadata(pdf: Any, strings: list[str], clear: bool) -> int:
    """Remove removed strings from Info, XMP and bookmark titles. Returns how many places changed."""
    hits = 0
    # the whole removed string and each word of it (a box edge rarely lines up with the exact match)
    words = {s for s in strings} | {w for s in strings for w in s.split()}
    needles = [re.compile(re.escape(w), re.IGNORECASE) for w in sorted(words, key=len, reverse=True) if len(w) >= 4 or (len(w) >= 3 and any(ch.isdigit() for ch in w))]
    if clear:
        for k in list(pdf.docinfo.keys()):
            del pdf.docinfo[k]
        if "/Metadata" in pdf.Root:
            del pdf.Root["/Metadata"]
        return 1
    for k in list(pdf.docinfo.keys()):
        try:
            v = str(pdf.docinfo[k])
        except Exception:
            continue
        nv = v
        for n in needles:
            nv = n.sub("", nv)
        if nv != v:
            pdf.docinfo[k] = nv
            hits += 1
    meta = pdf.Root.get("/Metadata")
    if meta is not None and needles:
        try:
            xml = bytes(meta.read_bytes()).decode("utf-8")
            nx = xml
            for n in needles:
                nx = n.sub("", nx)
            if nx != xml:
                meta.write(nx.encode("utf-8"))
                hits += 1
        except Exception:
            pass
    if needles:
        try:
            with pdf.open_outline() as outline:
                def walk(items: Any) -> None:
                    nonlocal hits
                    for it in items:
                        if any(n.search(it.title or "") for n in needles):
                            it.title = "[redacted]"
                            hits += 1
                        walk(it.children)
                walk(outline.root)
        except Exception:
            pass
    return hits


def _sanitize(pdf: Any, opts: RedactSanitize) -> dict[str, int]:
    pikepdf = load_pikepdf()
    done = {"attachments": 0, "javascript": 0}
    names = pdf.Root.get("/Names")
    if opts.attachments:
        if names is not None and "/EmbeddedFiles" in names:
            del names["/EmbeddedFiles"]
            done["attachments"] += 1
        if "/AF" in pdf.Root:
            del pdf.Root["/AF"]
            done["attachments"] += 1
    if opts.javascript:
        if names is not None and "/JavaScript" in names:
            del names["/JavaScript"]
            done["javascript"] += 1
        for key in ("/OpenAction", "/AA"):
            val = pdf.Root.get(key)
            if val is not None and (key == "/AA" or (isinstance(val, pikepdf.Dictionary) and str(val.get("/S")) == "/JavaScript")):
                del pdf.Root[key]
                done["javascript"] += 1
    for page in pdf.pages:
        if "/AA" in page.obj and opts.javascript:
            del page.obj["/AA"]
        kept = []
        for a in page.obj.get("/Annots") or []:
            if opts.attachments and str(a.get("/Subtype")) == "/FileAttachment":
                done["attachments"] += 1
                continue
            if opts.javascript:
                if "/AA" in a:
                    del a["/AA"]
                    done["javascript"] += 1
                act = a.get("/A")
                if act is not None and str(act.get("/S")) == "/JavaScript":
                    del a["/A"]
                    done["javascript"] += 1
            kept.append(a)
        if "/Annots" in page.obj:
            page.obj.Annots = pikepdf.Array(kept)
    return done


def _flatten_page(pdf: Any, index: int, plain: bytes, boxes: list[RedactBox]) -> None:
    """Replace page ``index`` with a picture of itself and the boxes burned in (no text, no annotations)."""
    import pypdfium2 as pdfium
    from PIL import ImageDraw

    pikepdf = load_pikepdf()
    scale = _RASTER_DPI / 72.0
    doc = pdfium.PdfDocument(plain)
    try:
        img = doc[index].render(scale=scale).to_pil().convert("RGB")
        vw, vh = doc[index].get_size()
    finally:
        doc.close()
    draw = ImageDraw.Draw(img)
    for b in boxes:
        draw.rectangle((b.x0 * scale, b.y0 * scale, b.x1 * scale, b.y1 * scale), fill=(0, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=88)
    image = pikepdf.Stream(pdf, buf.getvalue())
    image.Type, image.Subtype, image.Width, image.Height = pikepdf.Name.XObject, pikepdf.Name.Image, img.width, img.height
    image.ColorSpace, image.BitsPerComponent, image.Filter = pikepdf.Name.DeviceRGB, 8, pikepdf.Name.DCTDecode
    contents = pikepdf.Stream(pdf, f"q {_num(vw)} 0 0 {_num(vh)} 0 0 cm /MxPage Do Q\n".encode())
    page_obj = pdf.make_indirect(
        pikepdf.Dictionary(
            Type=pikepdf.Name.Page,
            MediaBox=[0, 0, vw, vh],
            Resources=pikepdf.Dictionary(XObject=pikepdf.Dictionary(MxPage=image)),
            Contents=contents,
        )
    )
    pdf.pages.insert(index, pikepdf.Page(page_obj))
    del pdf.pages[index + 1]


def _verify_pages(out_bytes: bytes, boxes_by_page: dict[int, list[RedactBox]], flat: set[int] | None = None) -> dict[int, list[str]]:
    """Re-read the OUTPUT. Returns page -> reasons it is not proven clean (empty dict: all proven)."""
    import pdfplumber
    import pypdfium2 as pdfium

    pikepdf = load_pikepdf()
    bad: dict[int, list[str]] = {}
    pl = pdfplumber.open(io.BytesIO(out_bytes))
    fm = pdfium.PdfDocument(out_bytes)
    pk = pikepdf.open(io.BytesIO(out_bytes))
    try:
        for pno, boxes in boxes_by_page.items():
            reasons: list[str] = []
            page = pl.pages[pno - 1]
            ox, oy = _frame(page)
            for c in page.chars:
                cx, cy = (c["x0"] + c["x1"]) / 2 - ox, (c["top"] + c["bottom"]) / 2 - oy
                if any(b.x0 <= cx <= b.x1 and b.y0 <= cy <= b.y1 for b in boxes):
                    reasons.append("text still readable under a box")
                    break
            pobj = pk.pages[pno - 1]
            rects = [_user_rect(pobj.obj, b) for b in boxes]
            tp = fm[pno - 1].get_textpage()
            try:
                for r in rects:
                    if tp.get_text_bounded(left=r[0], bottom=r[1], right=r[2], top=r[3]).strip():
                        reasons.append("text extraction finds text under a box")
                        break
            finally:
                tp.close()
            if flat and pno in flat:  # a picture: the boxes must render solid black
                img = fm[pno - 1].render(scale=1).to_pil().convert("L")
                for b in boxes:
                    crop = img.crop((int(b.x0) + 1, int(b.y0) + 1, max(int(b.x0) + 2, int(b.x1) - 1), max(int(b.y0) + 2, int(b.y1) - 1)))
                    if crop.getextrema()[1] > 24:
                        reasons.append("a burned-in box is not solid")
                        break
                if reasons:
                    bad[pno] = sorted(set(reasons))
                continue
            stats = _Stats()
            res = inherited(pobj.obj, "/Resources")
            if res is not None:
                _Rewriter(pk, rects, stats, check_only=True).run(pikepdf.parse_content_stream(pobj), res, pikepdf.Matrix())
            if stats.glyphs:
                reasons.append("glyphs under a box remain in the page content")
            reasons += [u for u in stats.unproven if "pixels" in u or "inline" in u]
            if reasons:
                bad[pno] = sorted(set(reasons))
    finally:
        pl.close()
        fm.close()
        pk.close()
    return bad


def redact_pdf_bytes(
    pdf_bytes: bytes,
    boxes: list[RedactBox | dict[str, Any]],
    *,
    password: str = "",
    sanitize: RedactSanitize | dict[str, Any] | None = None,
) -> PdfBinaryResult:
    """Remove everything under the boxes and prove it. The input is untouched; the output is a new file's bytes."""
    pikepdf = load_pikepdf()
    parsed = [b if isinstance(b, RedactBox) else RedactBox(**b) for b in boxes]
    if not parsed:
        raise ValueError("Mark at least one region to redact.")
    opts = sanitize if isinstance(sanitize, RedactSanitize) else RedactSanitize(**(sanitize or {}))
    plain = _plain(pdf_bytes, password)
    by_page: dict[int, list[RedactBox]] = {}
    for b in parsed:
        by_page.setdefault(b.page_number, []).append(b)

    removed_text = _text_under(plain, parsed)
    per_page: dict[int, dict[str, Any]] = {}
    gone_all: set[tuple[int, int]] = set()

    with open_pdf(plain) as pdf:
        total = len(pdf.pages)
        if max(by_page) > total:
            raise ValueError(f"The file has {total} pages; a region is on page {max(by_page)}.")
        for pno, pboxes in sorted(by_page.items()):
            page = pdf.pages[pno - 1]
            rects = [_user_rect(page.obj, b) for b in pboxes]
            stats = _Stats()
            rw = _Rewriter(pdf, rects, stats)
            res = inherited(page.obj, "/Resources")
            res = rw.own(res) if res is not None else pikepdf.Dictionary()
            page.obj.Resources = res
            body = pikepdf.unparse_content_stream(rw.run(pikepdf.parse_content_stream(page), res, pikepdf.Matrix()))
            page.obj.Contents = pikepdf.Stream(pdf, b"q\n" + body + b"\nQ\n" + _fill_ops(rects))
            notes, fields, gone = _strip_annotations(pdf, page, rects)
            gone_all |= gone
            if "/Thumb" in page.obj:
                del page.obj["/Thumb"]
            per_page[pno] = {
                "page_number": pno,
                "boxes": len(pboxes),
                "tier": "stream_rewrite",
                "glyphs_removed": stats.glyphs,
                "images_blanked": stats.images,
                "inline_images_removed": stats.inline_images,
                "annotations_removed": notes,
                "form_fields_removed": fields,
            }
        fields_pruned = _prune_fields(pdf, gone_all)
        metadata_places = _scrub_metadata(pdf, removed_text, opts.clear_metadata)
        sanitized = _sanitize(pdf, opts)
        first = save_pdf(pdf)

        bad = _verify_pages(first, by_page)
        if bad:
            for pno in bad:
                _flatten_page(pdf, pno - 1, plain, by_page[pno])
                per_page[pno]["tier"] = "rasterize"
                per_page[pno]["flattened_because"] = bad[pno]
            content = save_pdf(pdf)
            still = _verify_pages(content, by_page, set(bad))
            if still:
                raise RuntimeError("Redaction could not be proven for every page; no file was produced.", {"pages": sorted(still)})
        else:
            content = first

    tiers = {p["tier"] for p in per_page.values()}
    tier = "mixed" if len(tiers) > 1 else next(iter(tiers))
    flattened = sorted(p for p, v in per_page.items() if v["tier"] == "rasterize")
    notes_out = []
    if flattened:
        notes_out.append(
            "Pages " + ", ".join(map(str, flattened)) + " were turned into pictures with the regions burned in, "
            "because the text under them could not be proven removed in place. Those pages are no longer searchable."
        )
    return PdfBinaryResult(
        content=content,
        page_count=total,
        operation="redact",
        metadata={
            "tier": tier,
            "pages": [per_page[p] for p in sorted(per_page)],
            "regions": len(parsed),
            "glyphs_removed": sum(p["glyphs_removed"] for p in per_page.values()),
            "images_blanked": sum(p["images_blanked"] for p in per_page.values()),
            "annotations_removed": sum(p["annotations_removed"] for p in per_page.values()),
            "form_fields_removed": fields_pruned,
            "metadata_places_cleaned": metadata_places,
            "attachments_removed": sanitized["attachments"],
            "javascript_removed": sanitized["javascript"],
            "flattened_pages": flattened,
            "verified": True,
            "notes": notes_out,
        },
    )


# ---------------------------------------------------------------------------
# Sanitize report (read-only): what a file carries beyond what the page shows
# ---------------------------------------------------------------------------


def sanitize_report_bytes(pdf_bytes: bytes, *, password: str = "") -> dict[str, Any]:
    pikepdf = load_pikepdf()
    with open_pdf(pdf_bytes, password) as pdf:
        info = [str(k).lstrip("/") for k in pdf.docinfo.keys()]
        names = pdf.Root.get("/Names")
        attachments = 0
        if names is not None and "/EmbeddedFiles" in names:
            ef = names.EmbeddedFiles
            attachments = len(ef.get("/Names", [])) // 2 or len(ef.get("/Kids", []))
        js = 1 if names is not None and "/JavaScript" in names else 0
        js += 1 if "/AA" in pdf.Root else 0
        annots: dict[str, int] = {}
        hidden_pages: list[int] = []
        thumbs = 0
        for i, page in enumerate(pdf.pages, start=1):
            thumbs += 1 if "/Thumb" in page.obj else 0
            for a in page.obj.get("/Annots") or []:
                sub = str(a.get("/Subtype", "")).lstrip("/") or "Unknown"
                annots[sub] = annots.get(sub, 0) + 1
                act = a.get("/A")
                if act is not None and str(act.get("/S")) == "/JavaScript":
                    js += 1
                if sub == "FileAttachment":
                    attachments += 1
            try:
                if any(str(ins.operator) == "Tr" and int(ins.operands[0]) == 3 for ins in pikepdf.parse_content_stream(page) if not isinstance(ins, pikepdf.ContentStreamInlineImage)):
                    hidden_pages.append(i)
            except Exception:
                pass
        acro = pdf.Root.get("/AcroForm")
        return {
            "metadata_fields": info,
            "has_xmp": "/Metadata" in pdf.Root,
            "attachments": attachments,
            "javascript_actions": js,
            "annotations": annots,
            "form_fields": len(acro.get("/Fields", [])) if acro is not None else 0,
            "hidden_text_pages": hidden_pages,
            "thumbnails": thumbs,
            "bookmarks": bool(pdf.Root.get("/Outlines")),
        }


async def redact_pdf_bytes_async(pdf_bytes: bytes, boxes: list[Any], **kwargs: Any) -> PdfBinaryResult:
    return await run_in_cpu_executor(redact_pdf_bytes, pdf_bytes, boxes, **kwargs)


async def find_redaction_hits_bytes_async(pdf_bytes: bytes, spec: Any, **kwargs: Any) -> dict[str, Any]:
    return await run_in_cpu_executor(find_redaction_hits_bytes, pdf_bytes, spec, **kwargs)


async def sanitize_report_bytes_async(pdf_bytes: bytes, **kwargs: Any) -> dict[str, Any]:
    return await run_in_cpu_executor(sanitize_report_bytes, pdf_bytes, **kwargs)
