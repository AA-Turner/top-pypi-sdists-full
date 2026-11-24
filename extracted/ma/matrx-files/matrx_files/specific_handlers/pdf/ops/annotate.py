"""Write markup annotations the browser editors cannot (PDF-PLAN U10, decision 1: pikepdf only).

PDF.js's writer (``saveDocument``) makes highlights, text boxes, drawings and stamps. Everything else
Acrobat's comment tools make is written here, onto the bytes the browser already saved, by
dictionary: underline and strike-out (text markup from a selection), rectangle, oval, line and arrow
(Square, Circle, Line with an open-arrow ending), the sticky note (Text with a Popup, author and
time) and links (a web address or a page of this document). Every annotation carries its own
appearance stream, so Acrobat, Preview, Chrome and pdf.js all draw it the same.

Saved annotations are changed or removed by their object reference (the id pdf.js reports, "45R"):
``update`` replaces a note's text, ``delete`` takes the annotation (and its popup) off the page.

Coordinates are PDF user space of the page (points, origin bottom-left, before the page's /Rotate),
which is what pdf.js's ``viewport.convertToPdfPoint`` gives.
"""

from __future__ import annotations

import math
import re
import uuid
from datetime import UTC, datetime
from typing import Any

from ._pike import load_pikepdf, open_pdf, save_pdf

KINDS = ("underline", "strikeout", "square", "circle", "line", "arrow", "note", "link")
_REF = re.compile(r"^(\d+)R(\d*)$")
_HEX = re.compile(r"^#?([0-9a-fA-F]{6})$")
_KAPPA = 0.5522847498


def pdf_date(now: datetime | None = None) -> str:
    t = (now or datetime.now(UTC)).astimezone(UTC)
    return t.strftime("D:%Y%m%d%H%M%SZ")


def _rgb(color: str | None, default: tuple[float, float, float]) -> tuple[float, float, float]:
    m = _HEX.match(color or "")
    if not m:
        return default
    h = m.group(1)
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255)


def _num(v: float) -> str:
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return s if s not in ("", "-0") else "0"


def _norm(rect: list[float]) -> tuple[float, float, float, float]:
    if len(rect) != 4:
        raise ValueError("A mark needs a box of four numbers.")
    x0, y0, x1, y1 = (float(v) for v in rect)
    return min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)


def _ref_of(ref: str) -> tuple[int, int]:
    m = _REF.match(ref.strip())
    if not m:
        raise ValueError(f"'{ref}' is not an annotation reference.")
    return int(m.group(1)), int(m.group(2) or 0)


def _appearance(pdf: Any, bbox: tuple[float, float, float, float], content: str, opacity: float) -> Any:
    pikepdf = load_pikepdf()
    resources: dict[str, Any] = {}
    if opacity < 1:
        gs = pikepdf.Dictionary(Type=pikepdf.Name.ExtGState, CA=opacity, ca=opacity)
        resources["/ExtGState"] = pikepdf.Dictionary({"/G0": gs})
        content = "/G0 gs\n" + content
    stream = pikepdf.Stream(pdf, content.encode("latin-1"))
    stream.Type = pikepdf.Name.XObject
    stream.Subtype = pikepdf.Name.Form
    stream.BBox = pikepdf.Array([float(v) for v in bbox])
    stream.Resources = pikepdf.Dictionary(resources)
    return pikepdf.Dictionary(N=stream)


def _ellipse_path(x0: float, y0: float, x1: float, y1: float) -> str:
    cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
    kx, ky = rx * _KAPPA, ry * _KAPPA
    n = _num
    return (
        f"{n(cx + rx)} {n(cy)} m\n"
        f"{n(cx + rx)} {n(cy + ky)} {n(cx + kx)} {n(cy + ry)} {n(cx)} {n(cy + ry)} c\n"
        f"{n(cx - kx)} {n(cy + ry)} {n(cx - rx)} {n(cy + ky)} {n(cx - rx)} {n(cy)} c\n"
        f"{n(cx - rx)} {n(cy - ky)} {n(cx - kx)} {n(cy - ry)} {n(cx)} {n(cy - ry)} c\n"
        f"{n(cx + kx)} {n(cy - ry)} {n(cx + rx)} {n(cy - ky)} {n(cx + rx)} {n(cy)} c\n"
    )


def arrow_head(x1: float, y1: float, x2: float, y2: float, width: float) -> tuple[tuple[float, float], tuple[float, float]]:
    """The two outer points of an open arrowhead at (x2, y2), Acrobat's proportions (about 30 degrees)."""
    ang = math.atan2(y2 - y1, x2 - x1)
    size = max(6.0, width * 4.5)
    a, b = ang + math.pi - math.pi / 6, ang + math.pi + math.pi / 6
    return (x2 + size * math.cos(a), y2 + size * math.sin(a)), (x2 + size * math.cos(b), y2 + size * math.sin(b))


def _base(pdf: Any, subtype: str, rect: tuple[float, float, float, float], spec: dict[str, Any], page_obj: Any, now: str) -> Any:
    pikepdf = load_pikepdf()
    r, g, b = _rgb(spec.get("color"), (1.0, 0.3, 0.3))
    annot = pikepdf.Dictionary(
        Type=pikepdf.Name.Annot,
        Subtype=pikepdf.Name("/" + subtype),
        Rect=pikepdf.Array([float(v) for v in rect]),
        F=4,  # Print
        NM=pikepdf.String(f"matrx-{uuid.uuid4()}"),
        M=pikepdf.String(now),
        CreationDate=pikepdf.String(now),
        C=pikepdf.Array([r, g, b]),
        P=page_obj,
    )
    opacity = float(spec.get("opacity") if spec.get("opacity") is not None else 1)
    if opacity < 1:
        annot.CA = max(0.0, min(1.0, opacity))
    if spec.get("contents"):
        annot.Contents = pikepdf.String(str(spec["contents"]))
    if spec.get("author"):
        annot.T = pikepdf.String(str(spec["author"]))
    return annot


def _note_icon(rect: tuple[float, float, float, float], rgb: tuple[float, float, float]) -> str:
    """Acrobat's "Comment" icon: a speech bubble filled with the note's color, outlined, with three lines."""
    x0, y0, x1, y1 = rect
    w, h = x1 - x0, y1 - y0
    r, g, b = rgb
    n = _num
    bx0, by0, bx1, by1 = x0 + 1, y0 + h * 0.25, x1 - 1, y1 - 1
    tail = f"{n(x0 + w * 0.3)} {n(by0)} l {n(x0 + w * 0.22)} {n(y0 + 1)} l {n(x0 + w * 0.5)} {n(by0)} l"
    lines = "".join(
        f"{n(bx0 + 3)} {n(by1 - (by1 - by0) * f)} m {n(bx1 - 3)} {n(by1 - (by1 - by0) * f)} l\n" for f in (0.3, 0.5, 0.7)
    )
    return (
        f"{n(r)} {n(g)} {n(b)} rg 0.25 0.25 0.25 RG 1 w\n"
        f"{n(bx0)} {n(by1)} m {n(bx1)} {n(by1)} l {n(bx1)} {n(by0)} l {tail} {n(bx0)} {n(by0)} l h B\n"
        f"0.25 0.25 0.25 RG 0.8 w\n{lines}S\n"
    )


def _build(pdf: Any, page: Any, spec: dict[str, Any], now: str) -> list[Any]:
    """The annotation dictionaries for one ``add`` (a note brings its popup)."""
    pikepdf = load_pikepdf()
    kind = spec.get("kind")
    if kind not in KINDS:
        raise ValueError(f"Unknown kind of mark: {kind!r}.")
    width = max(0.25, float(spec.get("width") or 2))
    rgb = _rgb(spec.get("color"), (1.0, 0.3, 0.3))
    stroke = f"{_num(rgb[0])} {_num(rgb[1])} {_num(rgb[2])} RG"
    opacity = float(spec.get("opacity") if spec.get("opacity") is not None else 1)
    page_obj = page.obj

    if kind in ("underline", "strikeout"):
        try:
            quads = [list(map(float, q)) for q in spec.get("quads") or []]
        except (TypeError, ValueError):  # a box with a missing or non-numeric corner is a refusal, not a crash
            quads = []
        if not quads or any(len(q) != 8 for q in quads):
            raise ValueError("An underline or strike-out needs the selected text's boxes.")
        xs = [q[i] for q in quads for i in (0, 2, 4, 6)]
        ys = [q[i] for q in quads for i in (1, 3, 5, 7)]
        rect = (min(xs) - 1, min(ys) - 1, max(xs) + 1, max(ys) + 1)
        annot = _base(pdf, "Underline" if kind == "underline" else "StrikeOut", rect, spec, page_obj, now)
        annot.QuadPoints = pikepdf.Array([v for q in quads for v in q])
        ops = []
        for q in quads:
            # QuadPoints order (what Acrobat writes): top-left, top-right, bottom-left, bottom-right.
            top = (q[1] + q[3]) / 2
            bottom = (q[5] + q[7]) / 2
            h = abs(top - bottom) or 10
            lw = max(0.5, h / 14)
            y = bottom + h * 0.08 if kind == "underline" else (top + bottom) / 2
            ops.append(f"{_num(lw)} w {_num(q[4])} {_num(y)} m {_num(q[6])} {_num(y)} l S")
        annot.AP = _appearance(pdf, rect, f"{stroke}\n" + "\n".join(ops) + "\n", opacity)
        return [annot]

    if kind in ("square", "circle"):
        x0, y0, x1, y1 = _norm(spec["rect"])
        if x1 - x0 < 1 or y1 - y0 < 1:
            raise ValueError("A shape needs some size.")
        rect = (x0, y0, x1, y1)
        annot = _base(pdf, "Square" if kind == "square" else "Circle", rect, spec, page_obj, now)
        annot.BS = pikepdf.Dictionary(Type=pikepdf.Name.Border, W=width, S=pikepdf.Name.S)
        i = width / 2
        path = (
            f"{_num(x0 + i)} {_num(y0 + i)} {_num(x1 - x0 - width)} {_num(y1 - y0 - width)} re\n"
            if kind == "square"
            else _ellipse_path(x0 + i, y0 + i, x1 - i, y1 - i)
        )
        annot.AP = _appearance(pdf, rect, f"{stroke} {_num(width)} w\n{path}S\n", opacity)
        return [annot]

    if kind in ("line", "arrow"):
        pts = [float(v) for v in spec.get("points") or []]
        if len(pts) != 4:
            raise ValueError("A line needs its two ends.")
        x1, y1, x2, y2 = pts
        if math.hypot(x2 - x1, y2 - y1) < 1:
            raise ValueError("A line needs some length.")
        path = f"{_num(x1)} {_num(y1)} m {_num(x2)} {_num(y2)} l S\n"
        xs, ys = [x1, x2], [y1, y2]
        if kind == "arrow":
            (ax, ay), (bx, by) = arrow_head(x1, y1, x2, y2, width)
            path += f"{_num(ax)} {_num(ay)} m {_num(x2)} {_num(y2)} l {_num(bx)} {_num(by)} l S\n"
            xs += [ax, bx]
            ys += [ay, by]
        pad = width + 1
        rect = (min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)
        annot = _base(pdf, "Line", rect, spec, page_obj, now)
        annot.L = pikepdf.Array(pts)
        annot.BS = pikepdf.Dictionary(Type=pikepdf.Name.Border, W=width, S=pikepdf.Name.S)
        if kind == "arrow":
            annot.LE = pikepdf.Array([pikepdf.Name("/None"), pikepdf.Name.OpenArrow])
        annot.AP = _appearance(pdf, rect, f"{stroke} {_num(width)} w 1 J 1 j\n{path}", opacity)
        return [annot]

    if kind == "note":
        x0, y0, x1, y1 = _norm(spec["rect"])
        # The icon is a fixed 20 x 20 points (Acrobat's), anchored at the box's top-left.
        rect = (x0, y1 - 20, x0 + 20, y1)
        annot = _base(pdf, "Text", rect, spec, page_obj, now)
        annot.Name = pikepdf.Name.Comment
        annot.Open = False
        annot.F = 4 | 8 | 16  # Print, NoZoom, NoRotate
        annot.AP = _appearance(pdf, rect, _note_icon(rect, rgb), 1.0)
        annot_ref = pdf.make_indirect(annot)
        mx0, _my0, mx1, my1 = (float(v) for v in page.mediabox)
        px0 = min(rect[2] + 4, mx1 - 180)
        popup = pikepdf.Dictionary(
            Type=pikepdf.Name.Annot,
            Subtype=pikepdf.Name.Popup,
            Rect=pikepdf.Array([max(mx0, px0), max(0.0, my1 - 120 - (my1 - rect[3])), max(mx0, px0) + 180, rect[3]]),
            Parent=annot_ref,
            Open=False,
            F=4 | 8 | 16,
            P=page_obj,
        )
        popup_ref = pdf.make_indirect(popup)
        annot_ref.Popup = popup_ref
        return [annot_ref, popup_ref]

    # link
    x0, y0, x1, y1 = _norm(spec["rect"])
    if x1 - x0 < 2 or y1 - y0 < 2:
        raise ValueError("A link needs a box to click.")
    annot = _base(pdf, "Link", (x0, y0, x1, y1), spec, page_obj, now)
    del annot["/C"]
    annot.Border = pikepdf.Array([0, 0, 0])
    annot.H = pikepdf.Name.I
    url = str(spec.get("url") or "").strip()
    dest_page = spec.get("dest_page")
    if url:
        if not re.match(r"^(https?:|mailto:|tel:)", url, re.I):
            url = "https://" + url
        annot.A = pikepdf.Dictionary(S=pikepdf.Name.URI, URI=pikepdf.String(url))
    elif dest_page:
        n = int(dest_page)
        if n < 1 or n > len(pdf.pages):
            raise ValueError(f"This document has no page {n}.")
        annot.Dest = pikepdf.Array([pdf.pages[n - 1].obj, pikepdf.Name.Fit])
    else:
        raise ValueError("A link needs a web address or a page.")
    return [annot]


def apply_annotation_ops(pdf_bytes: bytes, ops: list[dict[str, Any]], *, password: str = "", now: datetime | None = None) -> bytes:
    """Apply ``add`` / ``update`` / ``delete`` operations and return the new PDF bytes."""
    pikepdf = load_pikepdf()
    if not ops:
        return pdf_bytes
    pdf = open_pdf(pdf_bytes, password)
    stamp = pdf_date(now)
    with pdf:
        for op in ops:
            kind = op.get("op")
            if kind == "add":
                n = int(op.get("page") or 0)
                if n < 1 or n > len(pdf.pages):
                    raise ValueError(f"This document has no page {n}.")
                page = pdf.pages[n - 1]
                made = _build(pdf, page, op, stamp)
                annots = page.obj.get("/Annots")
                if annots is None:
                    page.obj.Annots = pikepdf.Array([])
                    annots = page.obj.Annots
                for a in made:
                    annots.append(a if getattr(a, "is_indirect", False) else pdf.make_indirect(a))
            elif kind in ("update", "delete"):
                num, gen = _ref_of(str(op.get("ref") or ""))
                try:
                    target = pdf.get_object((num, gen))
                except Exception as exc:  # noqa: BLE001 - pikepdf raises several kinds for a missing object
                    raise ValueError(f"The mark {op.get('ref')} is not in this file.") from exc
                if not isinstance(target, pikepdf.Dictionary):
                    raise ValueError(f"The mark {op.get('ref')} is not in this file.")
                if kind == "update":
                    if "contents" in op:
                        target.Contents = pikepdf.String(str(op.get("contents") or ""))
                    if op.get("author"):
                        target.T = pikepdf.String(str(op["author"]))
                    target.M = pikepdf.String(stamp)
                    continue
                gone = {(num, gen)}
                popup = target.get("/Popup")
                if popup is not None and popup.is_indirect:
                    gone.add(popup.objgen)
                removed = False
                for page in pdf.pages:
                    annots = page.obj.get("/Annots")
                    if annots is None:
                        continue
                    kept = [a for a in annots if not (a.is_indirect and a.objgen in gone)]
                    if len(kept) != len(annots):
                        page.obj.Annots = pikepdf.Array(kept)
                        removed = True
                if not removed:
                    raise ValueError(f"The mark {op.get('ref')} is not on any page.")
            else:
                raise ValueError(f"Unknown operation {kind!r}.")
        return save_pdf(pdf)
