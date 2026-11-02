"""PDF to Word, Excel and PowerPoint (PDF-PLAN U14), built from the page's own words and tables.

Permissive stack only: pdfplumber reads the words, fonts and tables; python-docx, openpyxl and python-pptx
write the file. (Not pdf2docx, which is copyleft; not LibreOffice, whose PDF import rewrites layout in
ways nobody can predict.) The result is honest about what it is: the TEXT and TABLES come across, the
LAYOUT is approximated.

Limits, stated in every result under ``limits``:
- Word: paragraphs, headings (by font size), bold, tables. Columns become one flow; pictures, shapes
  and page headers/footers' positions are not carried.
- Excel: each table (found by its ruling lines) becomes a sheet. A page without a table adds nothing; a PDF with no tables gets one
  "Text" sheet of its lines.
- PowerPoint: one slide per page, each paragraph a text box at its position and size. Pictures are not carried.
- A scanned page has no text to carry: run "Recognize text" first. Pages like that are listed.
"""

from __future__ import annotations

import io
import statistics
from dataclasses import dataclass, field
from typing import Any

from ..concurrency import run_in_cpu_executor
from ..models import PdfBinaryResult
from ._pike import open_pdf

TARGETS: dict[str, tuple[str, str]] = {
    "docx": ("docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
    "xlsx": ("xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
    "pptx": ("pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation"),
}
MAX_CONVERT_PAGES = 300
LIMITS = {
    "docx": "Text, headings, bold and tables come across. Columns flow as one column; pictures and shapes are not carried.",
    "xlsx": "Each table with ruling lines becomes a sheet. Text outside tables is not carried (a PDF with no tables gets one Text sheet).",
    "pptx": "One slide per page; each paragraph is a text box at its place. Pictures and shapes are not carried.",
}


@dataclass
class Para:
    text: str
    size: float
    bold: bool
    x0: float
    top: float
    x1: float
    bottom: float
    runs: list[tuple[str, bool]] = field(default_factory=list)


@dataclass
class PageModel:
    width: float
    height: float
    paras: list[Para]
    tables: list[list[list[str]]]
    images: int


def _is_bold(fontname: str) -> bool:
    n = (fontname or "").lower()
    return "bold" in n or "black" in n or "heavy" in n


def _outside(word: dict[str, Any], boxes: list[tuple[float, float, float, float]]) -> bool:
    cx, cy = (word["x0"] + word["x1"]) / 2, (word["top"] + word["bottom"]) / 2
    return not any(x0 <= cx <= x1 and t <= cy <= b for x0, t, x1, b in boxes)


def read_pages(pdf_bytes: bytes) -> list[PageModel]:
    import pdfplumber

    pages: list[PageModel] = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            tables = []
            boxes = []
            try:
                for t in page.find_tables():
                    rows = [[(c or "").replace("\n", " ").strip() for c in row] for row in t.extract()]
                    if rows and any(any(c for c in r) for r in rows):
                        tables.append(rows)
                        boxes.append(t.bbox)
            except Exception:  # an odd ruling must not stop the text from coming across
                tables, boxes = [], []
            words = [w for w in page.extract_words(extra_attrs=["size", "fontname"], keep_blank_chars=False) if _outside(w, boxes)]
            words.sort(key=lambda w: (round(w["top"] / 3), w["x0"]))
            lines: list[list[dict[str, Any]]] = []
            for w in words:
                if lines and abs(lines[-1][0]["top"] - w["top"]) < max(2.0, w["size"] * 0.5):
                    lines[-1].append(w)
                else:
                    lines.append([w])
            paras: list[Para] = []
            for line in lines:
                line.sort(key=lambda w: w["x0"])
                size = statistics.median(w["size"] for w in line)
                text = " ".join(w["text"] for w in line)
                bold = sum(_is_bold(w["fontname"]) for w in line) * 2 > len(line)
                runs = [(w["text"], _is_bold(w["fontname"])) for w in line]
                x0, x1 = line[0]["x0"], line[-1]["x1"]
                top, bottom = min(w["top"] for w in line), max(w["bottom"] for w in line)
                prev = paras[-1] if paras else None
                if prev and top - prev.bottom < size * 0.6 and abs(prev.size - size) < 0.6 and prev.bold == bold and abs(prev.x0 - x0) < size * 3:
                    prev.text += " " + text
                    prev.runs.append((" ", False))
                    prev.runs.extend(runs)
                    prev.bottom, prev.x1 = bottom, max(prev.x1, x1)
                else:
                    paras.append(Para(text, size, bold, x0, top, x1, bottom, runs))
            pages.append(PageModel(float(page.width), float(page.height), paras, tables, len(page.images)))
    return pages


def _body_size(pages: list[PageModel]) -> float:
    sizes = [p.size for pg in pages for p in pg.paras for _ in p.text.split()]
    return statistics.median(sizes) if sizes else 11.0


def _to_docx(pages: list[PageModel]) -> bytes:
    from docx import Document
    from docx.shared import Pt

    doc = Document()
    body = _body_size(pages)
    for n, pg in enumerate(pages):
        if n:
            doc.add_page_break()
        items: list[tuple[float, str, Any]] = [(p.top, "p", p) for p in pg.paras]
        # A table has no stored position here; place it after the text above its first row's words.
        for t in pg.tables:
            items.append((float("inf"), "t", t))
        items.sort(key=lambda it: it[0])
        for _, kind, obj in items:
            if kind == "p":
                if obj.size >= body * 1.5:
                    doc.add_heading(obj.text, level=1)
                elif obj.size >= body * 1.2 and obj.bold:
                    doc.add_heading(obj.text, level=2)
                else:
                    para = doc.add_paragraph()
                    for text, bold in _merge_runs(obj.runs):
                        run = para.add_run(text)
                        run.bold = bold or None
                        if abs(obj.size - body) > 0.6:
                            run.font.size = Pt(round(obj.size, 1))
            else:
                cols = max(len(r) for r in obj)
                table = doc.add_table(rows=len(obj), cols=cols)
                table.style = "Table Grid"
                for r, row in enumerate(obj):
                    for c, cell in enumerate(row):
                        table.cell(r, c).text = cell
    out = io.BytesIO()
    doc.save(out)
    return out.getvalue()


def _merge_runs(runs: list[tuple[str, bool]]) -> list[tuple[str, bool]]:
    merged: list[tuple[str, bool]] = []
    for text, bold in runs:
        if text == " ":
            if merged:
                merged[-1] = (merged[-1][0] + " ", merged[-1][1])
            continue
        if merged and merged[-1][1] == bold:
            merged[-1] = (merged[-1][0] + text if merged[-1][0].endswith(" ") else merged[-1][0] + " " + text, bold)
        else:
            merged.append((text if not merged else " " + text, bold))
    return merged


def _to_xlsx(pages: list[PageModel]) -> tuple[bytes, int]:
    from openpyxl import Workbook

    wb = Workbook()
    wb.remove(wb.active)
    count = 0
    for n, pg in enumerate(pages, start=1):
        for t, rows in enumerate(pg.tables, start=1):
            ws = wb.create_sheet(f"p{n}-table{t}"[:31])
            for row in rows:
                ws.append([_cell(c) for c in row])
            count += 1
    if count == 0:
        ws = wb.create_sheet("Text")
        ws.append(["Page", "Text"])
        for n, pg in enumerate(pages, start=1):
            for p in pg.paras:
                ws.append([n, p.text])
    out = io.BytesIO()
    wb.save(out)
    return out.getvalue(), count


def _cell(text: str) -> Any:
    t = text.strip()
    if not t:
        return None
    try:
        return int(t.replace(",", "")) if t.replace(",", "").lstrip("-").isdigit() else float(t.replace(",", ""))
    except ValueError:
        return t


def _to_pptx(pages: list[PageModel]) -> bytes:
    from pptx import Presentation
    from pptx.util import Emu, Pt

    prs = Presentation()
    first = pages[0]
    prs.slide_width, prs.slide_height = Emu(int(first.width * 12700)), Emu(int(first.height * 12700))
    blank = prs.slide_layouts[6]
    for pg in pages:
        slide = prs.slides.add_slide(blank)
        sx, sy = prs.slide_width / pg.width, prs.slide_height / pg.height
        for p in pg.paras:
            box = slide.shapes.add_textbox(
                Emu(int(p.x0 * sx)), Emu(int(p.top * sy)), Emu(max(int((p.x1 - p.x0) * sx * 1.1), 12700 * 20)), Emu(int((p.bottom - p.top) * sy))
            )
            tf = box.text_frame
            tf.word_wrap = True
            run = tf.paragraphs[0].add_run()
            run.text = p.text
            run.font.size = Pt(max(6.0, round(p.size, 1)))
            run.font.bold = p.bold or None
        for rows in pg.tables:
            cols = max(len(r) for r in rows)
            shape = slide.shapes.add_table(len(rows), cols, Emu(int(36 * 12700)), Emu(int(pg.height * 0.55 * 12700)), Emu(int((pg.width - 72) * 12700)), Emu(int(len(rows) * 18 * 12700)))
            for r, row in enumerate(rows):
                for c, cell in enumerate(row):
                    shape.table.cell(r, c).text = cell
    out = io.BytesIO()
    prs.save(out)
    return out.getvalue()


def convert_pdf_bytes(pdf_bytes: bytes, *, target: str, source_password: str = "") -> PdfBinaryResult:
    """``target`` is docx, xlsx or pptx. Text and tables come across; the result's ``limits`` say what does not."""
    target = (target or "").lower().lstrip(".")
    if target not in TARGETS:
        raise ValueError(f"Convert to one of {', '.join(TARGETS)}.")
    with open_pdf(pdf_bytes, source_password) as pdf:
        n = len(pdf.pages)
        if n > MAX_CONVERT_PAGES:
            raise ValueError(f"This PDF has {n} pages and one conversion handles at most {MAX_CONVERT_PAGES}. Extract a page range first.")
        buf = io.BytesIO()
        pdf.save(buf)
    pages = read_pages(buf.getvalue())
    if not pages:
        raise ValueError("This PDF has no pages to convert.")
    meta: dict[str, Any] = {
        "target": target,
        "mime_type": TARGETS[target][1],
        "extension": TARGETS[target][0],
        "limits": LIMITS[target],
        "pages_without_text": [i for i, pg in enumerate(pages, start=1) if not pg.paras and not pg.tables],
        "tables": sum(len(pg.tables) for pg in pages),
        "pictures_not_carried": sum(pg.images for pg in pages),
    }
    if target == "docx":
        data = _to_docx(pages)
    elif target == "pptx":
        data = _to_pptx(pages)
    else:
        data, sheets = _to_xlsx(pages)
        meta["sheets"] = sheets or 1
        if sheets == 0:
            meta["no_tables_found"] = True
    return PdfBinaryResult(content=data, page_count=len(pages), operation=f"convert_{target}", metadata=meta)


async def convert_pdf_bytes_async(pdf_bytes: bytes, **kwargs: Any) -> PdfBinaryResult:
    return await run_in_cpu_executor(lambda: convert_pdf_bytes(pdf_bytes, **kwargs))


__all__ = ["LIMITS", "MAX_CONVERT_PAGES", "TARGETS", "convert_pdf_bytes", "convert_pdf_bytes_async", "read_pages"]
