"""Find and replace text in a PDF (PDF-PLAN U14), honestly bounded.

PDF text is positioned runs of glyphs, not a flowing paragraph, so a replace is a RE-SET of the run, not an
edit of a document. What this does, and says it does:

- It rewrites the text strings in the page's own content stream (pikepdf), in the font the run already uses.
- A match is REPLACEABLE only when it sits inside one text string, the font is a simple one-byte font
  (Type1 or TrueType with Standard, WinAnsi or MacRoman encoding, or none), and every character of the new
  text exists in that font (for an embedded subset font: has a width in its /Widths table).
- The rest of the line is NOT moved: a longer replacement can run into the next word. The preview shows
  each line before and after so that is seen before anything is saved.
- Matches found by text extraction but not replaceable are listed with the reason (split across runs,
  Type0/composite font, glyph missing, inside a form XObject), never skipped silently.
- A page with no text layer (a scan) is refused: run "Recognize text" first, then replace.
- Signed files: the caller writes a NEW file (the seal would break).
"""

from __future__ import annotations

import re
from typing import Any

from ..concurrency import run_in_cpu_executor
from ..models import PdfBinaryResult
from ._pike import inherited, is_signed, load_pikepdf, open_pdf, save_pdf
from .ocr import page_text_counts

MAX_FIND_LEN = 200
MAX_PREVIEW_ROWS = 200
_SIMPLE_ENCODINGS = {None, "/WinAnsiEncoding", "/MacRomanEncoding", "/StandardEncoding"}


def _font_info(pikepdf: Any, page: Any, name: str) -> dict[str, Any]:
    """Whether the font behind ``name`` can be re-set, and which characters it can show."""
    res = inherited(page.obj, "/Resources")
    fonts = res.get("/Font") if res is not None else None
    font = fonts.get(name) if fonts is not None else None
    if font is None:
        return {"ok": False, "why": "the font of this text could not be found"}
    sub = str(font.get("/Subtype", ""))
    if sub not in ("/Type1", "/TrueType", "/MMType1"):
        return {"ok": False, "why": f"the text uses a {sub.lstrip('/') or 'composite'} font that cannot be re-set safely"}
    enc = font.get("/Encoding")
    if isinstance(enc, pikepdf.Dictionary):
        if "/Differences" in enc:
            return {"ok": False, "why": "the font has a custom character map"}
        enc = enc.get("/BaseEncoding")
    enc_name = str(enc) if enc is not None else None
    if enc_name not in _SIMPLE_ENCODINGS:
        return {"ok": False, "why": "the font has a custom character map"}
    widths = font.get("/Widths")
    first = int(font.get("/FirstChar", 0)) if widths is not None else 0
    wlist = [float(w) for w in widths] if widths is not None else None
    return {"ok": True, "codec": "mac_roman" if enc_name == "/MacRomanEncoding" else "cp1252", "widths": wlist, "first": first, "name": str(font.get("/BaseFont", name))}


def _encodable(info: dict[str, Any], text: str) -> str | None:
    """None when the font can show every character of ``text``; else why not."""
    try:
        raw = text.encode(info["codec"])
    except UnicodeEncodeError as exc:
        return f"the font cannot show the character {text[exc.start]!r}"
    w, first = info["widths"], info["first"]
    if w is not None:
        for b in raw:
            i = b - first
            if i < 0 or i >= len(w) or w[i] <= 0:
                return f"the embedded font has no glyph for {bytes([b]).decode(info['codec'], 'replace')!r}"
    return None


def _pattern(find: str, match_case: bool, whole_word: bool) -> re.Pattern[str]:
    body = re.escape(find)
    if whole_word:
        body = rf"(?<!\w){body}(?!\w)"
    return re.compile(body, 0 if match_case else re.IGNORECASE)


def _scan(
    pdf: Any, find: str, replace: str, match_case: bool, whole_word: bool, pages: set[int] | None, apply: bool
) -> dict[str, Any]:
    pikepdf = load_pikepdf()
    rx = _pattern(find, match_case, whole_word)
    rows: list[dict[str, Any]] = []
    replaced = 0
    for pno, page in enumerate(pdf.pages, start=1):
        if pages is not None and pno not in pages:
            continue
        font_name: str | None = None
        info_cache: dict[str, dict[str, Any]] = {}
        out_ops: list[Any] = []
        changed = False
        try:
            ops = list(pikepdf.parse_content_stream(page))
        except Exception as exc:
            rows.append({"page": pno, "replaceable": False, "reason": f"the page content could not be read ({exc.__class__.__name__})", "before": "", "after": ""})
            continue
        for operands, operator in ops:
            op = str(operator)
            if op == "Tf" and operands:
                font_name = str(operands[0])
            targets: list[tuple[int, Any]] = []
            if op in ("Tj", "'", '"') and operands:
                targets = [(len(operands) - 1, operands[-1])]
            elif op == "TJ" and operands:
                targets = [(-1, operands[0])]
            if not targets:
                out_ops.append((operands, operator))
                continue
            info = None
            if font_name is not None:
                info = info_cache.get(font_name) or info_cache.setdefault(font_name, _font_info(pikepdf, page, font_name))
            new_operands = list(operands)
            items = list(operands[0]) if op == "TJ" else [operands[-1]]
            for k, item in enumerate(items):
                if not isinstance(item, pikepdf.String):
                    continue
                if info is None or not info["ok"]:
                    codec = "cp1252"
                else:
                    codec = info["codec"]
                text = bytes(item).decode(codec, "replace")
                if not rx.search(text):
                    continue
                if info is None or not info["ok"]:
                    why = (info or {}).get("why", "the font of this text could not be found")
                    for m in rx.finditer(text):
                        rows.append({"page": pno, "replaceable": False, "reason": why, "before": text, "after": ""})
                    continue
                problem = _encodable(info, replace)
                after = rx.sub(lambda _m: replace, text)
                if problem:
                    rows.append({"page": pno, "replaceable": False, "reason": problem, "before": text, "after": after})
                    continue
                count = len(rx.findall(text))
                rows.append({"page": pno, "replaceable": True, "reason": "", "before": text, "after": after, "count": count})
                if apply:
                    items[k] = pikepdf.String(after.encode(info["codec"]))
                    changed = True
                    replaced += count
            if apply and changed:
                if op == "TJ":
                    new_operands = [pikepdf.Array(items)]
                else:
                    new_operands[-1] = items[0]
            out_ops.append((new_operands, operator))
        if apply and changed:
            page.obj["/Contents"] = pdf.make_stream(pikepdf.unparse_content_stream(out_ops))
    return {"rows": rows, "replaced": replaced}


def _extraction_matches(pdf_bytes: bytes, rx: re.Pattern[str], pages: set[int] | None) -> int:
    """How many times the text extractor sees the phrase: the number a person would search for."""
    import pypdfium2 as pdfium

    doc = pdfium.PdfDocument(pdf_bytes)
    try:
        total = 0
        for i in range(len(doc)):
            if pages is not None and i + 1 not in pages:
                continue
            tp = doc[i].get_textpage()
            try:
                total += len(rx.findall(re.sub(r"\s+", " ", tp.get_text_range() or "")))
            finally:
                tp.close()
        return total
    finally:
        doc.close()


def _check(find: str, pages: list[int] | None, page_count: int) -> set[int] | None:
    if not find or not find.strip():
        raise ValueError("Type the text to find.")
    if len(find) > MAX_FIND_LEN:
        raise ValueError(f"The text to find can be at most {MAX_FIND_LEN} characters.")
    if pages:
        bad = [p for p in pages if p < 1 or p > page_count]
        if bad:
            raise ValueError(f"This PDF has {page_count} pages; page {bad[0]} does not exist.")
        return set(pages)
    return None


def find_replace_preview(
    pdf_bytes: bytes, *, find: str, replace: str, match_case: bool = False, whole_word: bool = False,
    pages: list[int] | None = None, source_password: str = "",
) -> dict[str, Any]:
    """What a replace would change, line by line, and what it cannot. Writes nothing."""
    with open_pdf(pdf_bytes, source_password) as pdf:
        page_count = len(pdf.pages)
        wanted = _check(find, pages, page_count)
        data = save_pdf(pdf)
        scan = _scan(pdf, find, replace, match_case, whole_word, wanted, apply=False)
        signed = is_signed(pdf)
    counts = page_text_counts(data)
    scanned = [p for p in range(1, page_count + 1) if counts[p - 1] == 0 and (wanted is None or p in wanted)]
    rows = scan["rows"]
    can = sum(r.get("count", 1) for r in rows if r["replaceable"])
    seen = _extraction_matches(data, _pattern(find, match_case, whole_word), wanted)
    return {
        "find": find,
        "replace": replace,
        "found_in_text": seen,
        "replaceable": can,
        "not_replaceable": max(0, seen - can),
        "rows": rows[:MAX_PREVIEW_ROWS],
        "rows_total": len(rows),
        "pages_without_text": scanned,
        "refused": bool(scanned) and seen == 0,
        "signed": signed,
        "label": "Text re-set: the rest of each line is not moved, and the file's tagged structure is not updated.",
    }


def replace_pdf_bytes(
    pdf_bytes: bytes, *, find: str, replace: str, match_case: bool = False, whole_word: bool = False,
    pages: list[int] | None = None, source_password: str = "",
) -> PdfBinaryResult:
    """Apply the replace to every replaceable match. Raises when there is nothing to change or a page is a scan."""
    with open_pdf(pdf_bytes, source_password) as pdf:
        page_count = len(pdf.pages)
        wanted = _check(find, pages, page_count)
        data = save_pdf(pdf)
    counts = page_text_counts(data)
    scanned = [p for p in range(1, page_count + 1) if counts[p - 1] == 0 and (wanted is None or p in wanted)]
    if scanned and len(scanned) == len([p for p in range(1, page_count + 1) if wanted is None or p in wanted]):
        raise ValueError("These pages are scans with no text to replace. Run Recognize text first, then replace.")
    with open_pdf(pdf_bytes, source_password) as pdf:
        signed = is_signed(pdf)
        scan = _scan(pdf, find, replace, match_case, whole_word, wanted, apply=True)
        if scan["replaced"] == 0:
            reasons = sorted({r["reason"] for r in scan["rows"] if not r["replaceable"]})
            hint = f" Reason: {'; '.join(reasons)}." if reasons else ""
            raise ValueError(f"Nothing could be replaced: no replaceable match for {find!r}.{hint}")
        content = save_pdf(pdf)
    return PdfBinaryResult(
        content=content,
        page_count=page_count,
        operation="replace_text",
        metadata={
            "replaced": scan["replaced"],
            "not_replaced": sum(1 for r in scan["rows"] if not r["replaceable"]),
            "pages_without_text": scanned,
            "signed": signed,
            "label": "Text re-set",
        },
    )


async def find_replace_preview_async(pdf_bytes: bytes, **kwargs: Any) -> dict[str, Any]:
    return await run_in_cpu_executor(lambda: find_replace_preview(pdf_bytes, **kwargs))


async def replace_pdf_bytes_async(pdf_bytes: bytes, **kwargs: Any) -> PdfBinaryResult:
    return await run_in_cpu_executor(lambda: replace_pdf_bytes(pdf_bytes, **kwargs))


__all__ = ["find_replace_preview", "find_replace_preview_async", "replace_pdf_bytes", "replace_pdf_bytes_async"]
