"""OCR to a searchable PDF (PDF-PLAN U14): an invisible text layer laid over the scanned page images.

OCRmyPDF (MPL-2.0, permissive for our use) drives Tesseract and writes the text layer with its own
renderer; the page images are kept. Nothing here needs Ghostscript: pages are rasterized with
pypdfium2 and the output is a plain PDF (``output_type="pdf"``, not PDF/A).

Rotation (the U1 known limit: "scanned pages with /Rotate 90 OCR as garbage"): OCRmyPDF reasons about
the page as it is DISPLAYED, so a page with a /Rotate flag that disagrees with how its image was
scanned came out with a text layer that did not line up. This module OCRs a copy whose /Rotate flags are
cleared (the image in its native orientation, with OCRmyPDF's orientation fix switched on so a sideways
scan is read correctly), then puts each page's ORIGINAL /Rotate back. The text layer is laid on the image
itself, so it stays aligned whatever the flag is, and the page looks exactly as it did before.

Modes (``mode``):
- ``skip``  (default): pages that already have text are left alone; only image-only pages are read.
- ``redo``: pages with a previous OCR layer are read again and the old layer is replaced.
- ``force``: every selected page is rasterized and read, even pages with real text (the text is lost
  in favour of the image: say so before using it).

Free: runs on the server's own CPU, no model, no cost. A page cap keeps one call bounded.
"""

from __future__ import annotations

import inspect
import io
import re
import tempfile
from pathlib import Path
from typing import Any

from ..concurrency import run_in_ocr_executor
from ..models import PdfBinaryResult
from ._pike import is_signed, load_pikepdf, open_pdf, save_pdf

OCR_MODES = ("skip", "redo", "force")
#: One call reads at most this many pages; more needs page ranges (a worker is not held for minutes).
MAX_OCR_PAGES = 150
_LANG = re.compile(r"^[a-z]{3}(?:_[A-Za-z0-9]+)?$")


def _load_ocrmypdf() -> Any:
    try:
        import ocrmypdf

        if not getattr(ocrmypdf, "__file__", None):  # an empty namespace left by an interrupted install
            raise ImportError("ocrmypdf is an empty namespace package")
        return ocrmypdf
    except ImportError as exc:  # pragma: no cover - the platform image installs it
        raise ImportError(
            "Reading scanned pages needs the `ocrmypdf` package (and the tesseract program). "
            "Install it with: pip install 'ocrmypdf>=16'",
            name="ocrmypdf",
        ) from exc


def _clean_languages(languages: list[str] | None) -> str:
    langs = [str(x).strip() for x in (languages or ["eng"]) if str(x).strip()] or ["eng"]
    bad = [x for x in langs if not _LANG.match(x)]
    if bad:
        raise ValueError(f"Not a language code: {', '.join(bad)}. Use Tesseract codes such as eng, deu, fra.")
    return "+".join(langs)


def page_text_counts(pdf_bytes: bytes) -> list[int]:
    """How many characters of real text each page carries (pypdfium2). 0 means image-only or empty."""
    import pypdfium2 as pdfium

    doc = pdfium.PdfDocument(pdf_bytes)
    try:
        out: list[int] = []
        for i in range(len(doc)):
            tp = doc[i].get_textpage()
            try:
                out.append(len((tp.get_text_range() or "").strip()))
            finally:
                tp.close()
        return out
    finally:
        doc.close()


def _ocr_kwargs(ocrmypdf: Any, wanted: dict[str, Any]) -> dict[str, Any]:
    """Pass only the options this OCRmyPDF release has (the image and a dev box may differ)."""
    try:
        accepted = set(inspect.signature(ocrmypdf.ocr).parameters)
    except (TypeError, ValueError):  # pragma: no cover
        return wanted
    return {k: v for k, v in wanted.items() if k in accepted}


def ocr_pdf_bytes(
    pdf_bytes: bytes,
    *,
    languages: list[str] | None = None,
    mode: str = "skip",
    pages: list[int] | None = None,
    deskew: bool = False,
    fix_orientation: bool = True,
    source_password: str = "",
) -> PdfBinaryResult:
    """Make the scanned pages of ``pdf_bytes`` searchable. ``pages`` are 1-based; None means every page."""
    if mode not in OCR_MODES:
        raise ValueError(f"Mode must be one of {', '.join(OCR_MODES)}.")
    lang = _clean_languages(languages)
    ocrmypdf = _load_ocrmypdf()
    pikepdf = load_pikepdf()

    with open_pdf(pdf_bytes, source_password) as src:
        page_count = len(src.pages)
        signed = is_signed(src)
        original_rotate = [int(src.pages[i].obj.get("/Rotate", 0) or 0) for i in range(page_count)]
        selected = sorted({int(p) for p in pages}) if pages else list(range(1, page_count + 1))
        outside = [p for p in selected if p < 1 or p > page_count]
        if outside:
            raise ValueError(f"This PDF has {page_count} pages; page {outside[0]} does not exist.")
        # Work on a decrypted, rotation-cleared copy.
        for i in range(page_count):
            if "/Rotate" in src.pages[i].obj:
                src.pages[i].obj["/Rotate"] = 0
        clean = save_pdf(src)

    before = page_text_counts(pdf_bytes if not _is_encrypted(pdf_bytes) else clean)
    if mode == "skip":
        todo = [p for p in selected if before[p - 1] == 0]
    else:
        todo = selected
    if len(todo) > MAX_OCR_PAGES:
        raise ValueError(
            f"{len(todo)} pages need reading and one request reads at most {MAX_OCR_PAGES}. Pick page ranges and run it again."
        )
    if not todo:
        return PdfBinaryResult(
            content=pdf_bytes if not _is_encrypted(pdf_bytes) else clean,
            page_count=page_count,
            operation="ocr",
            metadata={"pages_read": [], "pages_skipped": selected, "already_searchable": True, "signed": signed, "languages": lang, "mode": mode},
        )

    wanted: dict[str, Any] = {
        "language": lang,
        "output_type": "pdf",
        "rasterizer": "pypdfium",
        "pages": ",".join(str(p) for p in todo),
        "deskew": bool(deskew),
        "rotate_pages": bool(fix_orientation),
        "rotate_pages_threshold": 2.0,
        "optimize": 0,
        "progress_bar": False,
        "skip_text": mode == "skip",
        "redo_ocr": mode == "redo",
        "force_ocr": mode == "force",
        "use_threads": True,
    }
    with tempfile.TemporaryDirectory(prefix="pdf_ocr_") as work:
        src_path = Path(work) / "in.pdf"
        out_path = Path(work) / "out.pdf"
        src_path.write_bytes(clean)
        kwargs = _ocr_kwargs(ocrmypdf, wanted)
        try:
            ocrmypdf.ocr(src_path, out_path, **kwargs)
        except ocrmypdf.exceptions.MissingDependencyError as exc:
            raise ValueError(f"Text recognition is not available for these languages on this server: {exc}") from exc
        except ocrmypdf.exceptions.PriorOcrFoundError as exc:
            raise ValueError("Some of these pages already have text. Choose 'Skip pages that have text' or 'Read again'.") from exc
        except ocrmypdf.exceptions.EncryptedPdfError as exc:  # pragma: no cover - decrypted above
            raise ValueError("This PDF is password protected. Give its password to continue.") from exc
        except ocrmypdf.exceptions.InputFileError as exc:
            raise ValueError(f"This file could not be read as a PDF: {exc}") from exc
        except ocrmypdf.exceptions.ExitCodeException as exc:
            raise ValueError(f"Text recognition failed: {exc}") from exc
        result_bytes = out_path.read_bytes()

    # A page the author rotated keeps its original /Rotate (the text layer sits on the image, so it stays
    # aligned). A page with no /Rotate keeps OCRmyPDF's orientation fix: a sideways scan comes out upright.
    fixed_pages: list[int] = []
    with pikepdf.open(io.BytesIO(result_bytes)) as out:
        if len(out.pages) != page_count:  # pragma: no cover - OCRmyPDF keeps the page count
            raise ValueError("Text recognition changed the number of pages; nothing was saved.")
        for i in range(page_count):
            now = int(out.pages[i].obj.get("/Rotate", 0) or 0)
            if original_rotate[i]:
                out.pages[i].obj["/Rotate"] = original_rotate[i]
            elif now:
                fixed_pages.append(i + 1)
        final = save_pdf(out)

    after = page_text_counts(final)
    return PdfBinaryResult(
        content=final,
        page_count=page_count,
        operation="ocr",
        metadata={
            "pages_read": todo,
            "pages_skipped": [p for p in selected if p not in todo],
            "characters_before": sum(before),
            "characters_after": sum(after),
            "pages_still_empty": [p for p in todo if after[p - 1] == 0],
            "pages_turned_upright": fixed_pages,
            "languages": lang,
            "mode": mode,
            "already_searchable": False,
            "signed": signed,
        },
    )


def _is_encrypted(pdf_bytes: bytes) -> bool:
    pikepdf = load_pikepdf()
    try:
        with pikepdf.open(io.BytesIO(pdf_bytes)) as pdf:
            return bool(pdf.is_encrypted)
    except pikepdf.PasswordError:
        return True


async def ocr_pdf_bytes_async(pdf_bytes: bytes, **kwargs: Any) -> PdfBinaryResult:
    return await run_in_ocr_executor(lambda: ocr_pdf_bytes(pdf_bytes, **kwargs))


__all__ = ["MAX_OCR_PAGES", "OCR_MODES", "ocr_pdf_bytes", "ocr_pdf_bytes_async", "page_text_counts"]
