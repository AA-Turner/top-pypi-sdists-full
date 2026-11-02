"""Compare two PDFs (PDF-PLAN U14): a text diff per page plus a visual diff, and a list of changed regions.

Text: pdfplumber words, ``difflib`` on the word sequence of each page. Visual: both pages rendered with
pypdfium2, differenced, and the changed pixels merged into boxes (fractions of the page, origin top-left,
the shape ``@ai-matrx/diff`` PageCompare draws). Pages are matched by position (page 1 with page 1);
pages only one file has are reported as added or removed. Read-only: nothing is written.
"""

from __future__ import annotations

import difflib
import io
from typing import Any

from ..concurrency import run_in_cpu_executor
from ._pike import open_pdf

#: Pages compared per call (each is rendered twice).
MAX_COMPARE_PAGES = 200
_RENDER_SCALE = 0.75
_BLOCK = 12
#: A pixel counts as changed when its brightness differs by more than this (0-255).
_PIXEL_THRESHOLD = 40
_MAX_TEXT_CHANGES = 60


def _decrypt(pdf_bytes: bytes, password: str) -> bytes:
    with open_pdf(pdf_bytes, password) as pdf:
        out = io.BytesIO()
        pdf.save(out)
        return out.getvalue()


def _page_words(plumber_pdf: Any, i: int) -> list[str]:
    if i >= len(plumber_pdf.pages):
        return []
    return [w["text"] for w in plumber_pdf.pages[i].extract_words(use_text_flow=False, keep_blank_chars=False)]


def text_changes(before: list[str], after: list[str]) -> list[dict[str, str]]:
    """Word-level changes as {op, before, after}; adjacent edits are already merged by difflib."""
    changes: list[dict[str, str]] = []
    sm = difflib.SequenceMatcher(a=before, b=after, autojunk=False)
    for tag, a0, a1, b0, b1 in sm.get_opcodes():
        if tag == "equal":
            continue
        changes.append({"op": tag, "before": " ".join(before[a0:a1]), "after": " ".join(after[b0:b1])})
    return changes


def _render(doc: Any, i: int):
    from PIL import Image  # noqa: F401  (pypdfium2 returns PIL images)

    return doc[i].render(scale=_RENDER_SCALE).to_pil().convert("L")


def changed_regions(img_a: Any, img_b: Any) -> tuple[list[dict[str, float]], float]:
    """Boxes (fractions of page A) where the two renderings differ, and the fraction of pixels that differ."""
    import numpy as np
    from PIL import Image, ImageChops

    if img_b.size != img_a.size:
        canvas = Image.new("L", img_a.size, 255)
        canvas.paste(img_b.resize(img_a.size))
        img_b = canvas
    diff = np.asarray(ImageChops.difference(img_a, img_b)) > _PIXEL_THRESHOLD
    total = diff.size or 1
    ratio = float(diff.sum()) / total
    if not diff.any():
        return [], 0.0
    h, w = diff.shape
    gh, gw = -(-h // _BLOCK), -(-w // _BLOCK)
    padded = np.zeros((gh * _BLOCK, gw * _BLOCK), dtype=bool)
    padded[:h, :w] = diff
    grid = padded.reshape(gh, _BLOCK, gw, _BLOCK).any(axis=(1, 3))
    # Join blocks that touch (8-neighbour) or sit within 2 blocks: one changed sentence is one box.
    seen = np.zeros_like(grid, dtype=bool)
    boxes: list[tuple[int, int, int, int]] = []
    for gy in range(gh):
        for gx in range(gw):
            if not grid[gy, gx] or seen[gy, gx]:
                continue
            stack = [(gy, gx)]
            seen[gy, gx] = True
            y0 = y1 = gy
            x0 = x1 = gx
            while stack:
                cy, cx = stack.pop()
                y0, y1, x0, x1 = min(y0, cy), max(y1, cy), min(x0, cx), max(x1, cx)
                for ny in range(max(0, cy - 2), min(gh, cy + 3)):
                    for nx in range(max(0, cx - 2), min(gw, cx + 3)):
                        if grid[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True
                            stack.append((ny, nx))
            boxes.append((x0, y0, x1, y1))
    regions = [
        {
            "x": round(x0 * _BLOCK / w, 4),
            "y": round(y0 * _BLOCK / h, 4),
            "width": round(min(w, (x1 + 1) * _BLOCK) / w - x0 * _BLOCK / w, 4),
            "height": round(min(h, (y1 + 1) * _BLOCK) / h - y0 * _BLOCK / h, 4),
        }
        for x0, y0, x1, y1 in boxes
    ]
    regions.sort(key=lambda r: (r["y"], r["x"]))
    return regions, ratio


def compare_pdf_bytes(
    a_bytes: bytes,
    b_bytes: bytes,
    *,
    a_password: str = "",
    b_password: str = "",
    pages: list[int] | None = None,
) -> dict[str, Any]:
    """The comparison of ``a`` (before) and ``b`` (after). ``pages`` limit to those 1-based positions."""
    import pdfplumber
    import pypdfium2 as pdfium

    a = _decrypt(a_bytes, a_password)
    b = _decrypt(b_bytes, b_password)
    doc_a, doc_b = pdfium.PdfDocument(a), pdfium.PdfDocument(b)
    pl_a, pl_b = pdfplumber.open(io.BytesIO(a)), pdfplumber.open(io.BytesIO(b))
    try:
        na, nb = len(doc_a), len(doc_b)
        total = max(na, nb)
        wanted = sorted({p for p in (pages or range(1, total + 1)) if 1 <= p <= total})
        if len(wanted) > MAX_COMPARE_PAGES:
            raise ValueError(f"Compare at most {MAX_COMPARE_PAGES} pages at once. Choose a page range.")
        out_pages: list[dict[str, Any]] = []
        for p in wanted:
            i = p - 1
            if i >= na or i >= nb:
                out_pages.append(
                    {"page": p, "status": "added" if i >= na else "removed", "text_changes": [], "regions": [], "pixel_change": 1.0, "size_changed": False,
                     "words_before": len(_page_words(pl_a, i)), "words_after": len(_page_words(pl_b, i))}
                )
                continue
            wa, wb = _page_words(pl_a, i), _page_words(pl_b, i)
            changes = text_changes(wa, wb)
            ia, ib = _render(doc_a, i), _render(doc_b, i)
            regions, ratio = changed_regions(ia, ib)
            size_changed = ia.size != ib.size
            status = "same" if not changes and not regions and not size_changed else "changed"
            out_pages.append(
                {"page": p, "status": status, "text_changes": changes[:_MAX_TEXT_CHANGES], "text_changes_total": len(changes),
                 "regions": regions, "pixel_change": round(ratio, 5), "size_changed": size_changed,
                 "words_before": len(wa), "words_after": len(wb)}
            )
        return {
            "pages_before": na,
            "pages_after": nb,
            "pages": out_pages,
            "changed_pages": [x["page"] for x in out_pages if x["status"] != "same"],
            "identical": all(x["status"] == "same" for x in out_pages) and na == nb,
        }
    finally:
        doc_a.close()
        doc_b.close()
        pl_a.close()
        pl_b.close()


async def compare_pdf_bytes_async(a_bytes: bytes, b_bytes: bytes, **kwargs: Any) -> dict[str, Any]:
    return await run_in_cpu_executor(lambda: compare_pdf_bytes(a_bytes, b_bytes, **kwargs))


__all__ = ["MAX_COMPARE_PAGES", "changed_regions", "compare_pdf_bytes", "compare_pdf_bytes_async", "text_changes"]
