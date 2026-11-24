"""Text extraction from PDFs — native, OCR-fallback, and block/word maps.

THE ONE ENTRY (PDF-PLAN U2): :func:`extract_text_pages` is the single PDF text extractor. The
async, stream and bytes forms below are thin wrappers that only pick an executor, a temp file or
a queue - none of them has extraction logic of its own - and :func:`native_page_text` is the one
place a page's native text is read (the file-analysis native detector calls it too). Do not add a
second extractor; ``scripts/check_pdf_one_text_extractor.py`` fails the commit when a new file
imports an old one.

THE EXTRACTOR IS PURE: it reads bytes and returns pages. It never touches the database, storage
or any host service. Writing or reusing the ``docproc.processed_documents`` row (the content-hash
cache) is the CALLER's job, in ``aidream/services/documents/persistence.py``. Test:
``tests/test_pdf_extractor_is_pure.py``.

All functions are sync. Their ``_async`` variants run on the OCR executor when
OCR is enabled, otherwise on the CPU executor.
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator, Callable, Mapping
from typing import Any, NamedTuple

import pypdfium2 as pdfium

from ..concurrency import run_in_cpu_executor, run_in_ocr_executor
from ..stream_bridge import iter_sync_stream
from ..internal import load_pymupdf
from ..models import PdfExtractStart, PdfPageText, PdfTextBlock, PdfTextWord
from ..tmp import pdf_temp_file
from .ocr import ocr_image_bytes, ocr_pymupdf_page
from ..render_budget import bounded_render_dpi

_log = logging.getLogger(__name__)


#: A page whose native text is at least this long is judged on QUALITY as well
#: as length — below it there is not enough signal for a ratio to mean anything.
_PRINTABLE_RATIO_MIN_CHARS = 20

#: Native text with a smaller share of printable characters than this is
#: treated as unreadable and sent to OCR.
_MIN_PRINTABLE_RATIO = 0.6


def _tesseract():  # noqa: ANN202
    """pytesseract, the matrx-files[ocr] extra, imported at the point of OCR."""
    from matrx_files._extras import require

    return require("pytesseract", "ocr", "OCR")


def printable_ratio(text: str) -> float:
    """Share of ``text`` that is real, readable content (0.0–1.0).

    Whitespace counts as printable; C0 control bytes and the like do not.
    An empty string scores 0.0.
    """
    if not text:
        return 0.0
    good = sum(1 for ch in text if ch.isprintable() or ch.isspace())
    return good / len(text)


def native_text_needs_ocr(text: str, use_ocr_threshold: int) -> bool:
    """Whether a page's NATIVE text is unusable and OCR should run.

    Two independent failure modes, because a length test alone misses the
    second one (Arman's ruling, 2026-08-21):

    1. **Too little text** — the original test: fewer than *use_ocr_threshold*
       non-blank characters. Catches scanned/image-only pages.
    2. **Unreadable text** — a page with a broken font encoding returns
       PLENTY of characters that are pure control bytes
       (``\x00\x01\x02…``). A real PDF in this repo returns 4,184 such
       characters: it sails past the length test, so OCR never ran and the
       caller received 4KB of garbage that LOOKED like a successful
       extraction. ``force_ocr`` on the same page recovers real text.

    A threshold of 0 disables the LENGTH test only — an explicit "don't OCR
    short pages". Unreadable text is always unreadable, so the quality test
    still applies.
    """
    stripped = text.strip()
    if use_ocr_threshold > 0 and len(stripped) < use_ocr_threshold:
        return True
    if len(stripped) >= _PRINTABLE_RATIO_MIN_CHARS:
        return printable_ratio(stripped) < _MIN_PRINTABLE_RATIO
    return False


def native_page_text(page: Any) -> str:
    """A page's NATIVE text layer, exactly as the extractor reads it (reading order, no sorting).

    The single reader of ``get_text("text")`` for page text: the extractor below and the
    file-analysis ``text_extraction_native`` detector both call it, so the two can never disagree.
    """
    return page.get_text("text", sort=False)


def _pymupdf_text_blocks(page: Any) -> list[PdfTextBlock]:
    blocks: list[PdfTextBlock] = []
    for block in page.get_text("blocks", sort=False):
        x0, y0, x1, y1, text, block_number, block_type = block[:7]
        blocks.append(
            PdfTextBlock(
                block_number=int(block_number),
                block_type=int(block_type),
                x0=float(x0),
                y0=float(y0),
                x1=float(x1),
                y1=float(y1),
                text=str(text),
            )
        )
    return blocks


def _pymupdf_text_words(page: Any) -> list[PdfTextWord]:
    words: list[PdfTextWord] = []
    for word in page.get_text("words", sort=False):
        x0, y0, x1, y1, text, block_number, line_number, word_number = word[:8]
        words.append(
            PdfTextWord(
                word=str(text),
                x0=float(x0),
                y0=float(y0),
                x1=float(x1),
                y1=float(y1),
                block_number=int(block_number),
                line_number=int(line_number),
                word_number=int(word_number),
            )
        )
    return words


class BlankPageTest(NamedTuple):
    """When a page nobody has read, with NO native text at all, is provably blank and never sent to OCR.

    The page is rendered small in grey (``dpi``) and every pixel that differs from the page's median
    grey by ``min_contrast`` levels or more counts as ink. The page is blank only when its ink, in
    pixels per million, is at most ``max_ink_ppm``. Both numbers are the caller's (a host reads them
    from its knobs); this package only measures. When the measure cannot be taken the page is read.
    """

    max_ink_ppm: int
    min_contrast: int
    dpi: int = 150


def page_ink_ppm(page: Any, min_contrast: int, dpi: int = 150) -> int:
    """Ink on a PyMuPDF page, in pixels per million: pixels whose grey differs from the page's median
    grey by ``min_contrast`` levels or more (dark writing on light paper and light on dark alike).
    Rounded UP, so one ink pixel is never 0."""
    pymupdf = load_pymupdf()
    rect = page.rect
    pix = page.get_pixmap(
        dpi=bounded_render_dpi(rect.width, rect.height, dpi), colorspace=pymupdf.csGRAY, alpha=False
    )
    from PIL import Image

    img = Image.frombuffer("L", (pix.width, pix.height), pix.samples, "raw", "L", pix.stride, 1)
    hist = img.histogram()
    total = sum(hist)
    if not total:
        return 1_000_000
    seen, median = 0, 0
    for level, count in enumerate(hist):
        seen += count
        if seen * 2 >= total:
            median = level
            break
    ink = sum(count for level, count in enumerate(hist) if abs(level - median) >= min_contrast)
    return -(-ink * 1_000_000 // total)


def _blank_ink_ppm(page: Any, test: BlankPageTest) -> int | None:
    """The page's ink when it is provably blank under ``test``; None when it is not, or unsure."""
    try:
        ink = page_ink_ppm(page, test.min_contrast, test.dpi)
    except Exception as exc:  # noqa: BLE001 — a measure that cannot be taken means "read the page"
        _log.warning("[matrx-pdf] blank-page measure failed; the page is read by OCR: %r", exc)
        return None
    return ink if ink <= test.max_ink_ppm else None


class PdfPageRangeError(ValueError):
    """The requested page range does not exist in this document. ``str(exc)``
    is a sentence for the person who asked."""


class PdfHasNoPagesError(PdfPageRangeError):
    """The PDF opens but holds no readable pages (empty, encrypted or damaged).

    A refusal written for the person who uploaded it (``person_refusal``): the pipeline announces it
    on the file instead of filing it as a platform defect.
    """

    person_refusal = True

    def __init__(self, detail: str | None = None) -> None:
        super().__init__(
            detail
            or "This PDF has no readable pages. It may be empty, password-protected or damaged; "
            "try re-exporting it or upload an unlocked copy."
        )


class PdfPagesMissingError(RuntimeError):
    """The extraction stream ended without every page it was asked for.

    Raised by ``extract_text_pages_stream`` when the pages it yielded do not
    match the document's page count (or the requested slice). A caller must
    record this as a failure — never finish "done" with missing text.
    """

    def __init__(self, path: str, expected: list[int], got: list[int]) -> None:
        self.expected = expected
        self.got = got
        missing = sorted(set(expected) - set(got))
        super().__init__(
            f"PDF text extraction of {path} returned {len(got)} of {len(expected)} pages"
            f" (missing pages {missing[:20]}{'...' if len(missing) > 20 else ''})"
        )


def resolve_page_range(
    page_count: int, page_start: int | None = None, page_end: int | None = None
) -> tuple[int, int]:
    """Clamp a 1-based inclusive request to the document: ``(first, last)``."""
    if page_count <= 0:
        raise PdfHasNoPagesError()
    first = page_start or 1
    last = min(page_end or page_count, page_count)
    if first < 1 or (page_end is not None and page_end < first):
        raise PdfPageRangeError(f"Page range {page_start}-{page_end} is not a valid range.")
    if first > page_count:
        raise PdfPageRangeError(
            f"page_start {first} is past the last page ({page_count})."
        )
    return first, last


def extract_text_pages(
    path: str,
    force_ocr: bool = False,
    use_ocr_threshold: int = 100,
    include_blocks: bool = False,
    include_words: bool = False,
    on_open: Callable[[int], None] | None = None,
    on_page: Callable[[PdfPageText], None] | None = None,
    page_start: int | None = None,
    page_end: int | None = None,
    supplied_pages: Mapping[int, tuple[str, str]] | None = None,
    blank_page: BlankPageTest | None = None,
) -> list[PdfPageText]:
    """Extract per-page text + optional bbox metadata from a PDF on disk. THE one extraction entry.

    ``blank_page`` (off when None): a page that would go to OCR, has no native text at all and
    measures provably blank under the test is never OCR'd; it carries ``blank_ink_ppm`` and no text.
    ``force_ocr`` always reads every page.

    ``supplied_pages`` maps a 1-based page number to ``(text, extraction_method)`` someone already
    recognised (a phone's Vision pass): that page takes the given text and label as is — never read,
    never OCR'd, whatever its length (the OCR threshold does not apply to it).

    ``page_start`` / ``page_end`` (1-based, inclusive) limit extraction to that
    slice — pages outside it are never read or OCR'd. ``page_end`` past the
    last page clamps to it; ``page_start`` past the last page raises
    ``PdfPageRangeError``. ``on_open`` still reports the document's full count.

    Uses native ``get_text("text")`` first; falls back to Tesseract OCR for any
    page whose extracted text is shorter than *use_ocr_threshold* characters
    (or all pages if *force_ocr* is True). When OCR cannot run or fails on a page,
    that page keeps its native text and carries ``ocr_error``; the document never fails
    for it.

    ``on_open`` / ``on_page`` are optional sync progress hooks called from the
    extraction loop (``on_open`` with the page count the moment the document
    opens, ``on_page`` with each page as it finishes). They exist so callers
    can stream progress in real time — see ``extract_text_pages_stream``.
    """
    pymupdf = load_pymupdf()
    pages: list[PdfPageText] = []
    with pymupdf.open(path) as doc:
        if on_open is not None:
            on_open(doc.page_count)
        first, last = resolve_page_range(doc.page_count, page_start, page_end)
        for page_index in range(first - 1, last):
            page = doc[page_index]
            text = ""
            method = "native"
            ocr_error: str | None = None
            blank_ink_ppm: int | None = None
            supplied = supplied_pages.get(page_index + 1) if supplied_pages else None
            if supplied is not None:
                text, method = supplied
            elif not force_ocr:
                text = native_page_text(page)

            wants_ocr = supplied is None and (force_ocr or native_text_needs_ocr(text, use_ocr_threshold))
            if wants_ocr and blank_page is not None and not force_ocr and not text.strip():
                blank_ink_ppm = _blank_ink_ppm(page, blank_page)
                wants_ocr = blank_ink_ppm is None
            if wants_ocr:
                try:
                    text = ocr_pymupdf_page(page)
                    method = "ocr"
                except Exception as exc:  # noqa: BLE001 — OCR failure is per page, never fatal
                    # The native text layer always comes through: OCR that cannot run (no
                    # Tesseract on this host) or fails on one page is announced on THAT page
                    # and the document goes on.
                    ocr_error = f"{type(exc).__name__}: {exc}"[:500]
                    if force_ocr:
                        text = native_page_text(page)
                    _log.warning(
                        "[matrx-pdf] OCR failed on page %d of %s; keeping native text (%d chars): %s",
                        page_index + 1,
                        path,
                        len(text.strip()),
                        ocr_error,
                    )

            rect = page.rect
            page_text = PdfPageText(
                page_number=page_index + 1,
                page_index=page_index,
                width=float(rect.width),
                height=float(rect.height),
                rotation=int(page.rotation),
                text=text,
                extraction_method=method,
                char_count=len(text),
                source_path=path,
                blocks=_pymupdf_text_blocks(page) if include_blocks else None,
                words=_pymupdf_text_words(page) if include_words else None,
                ocr_error=ocr_error,
                blank_ink_ppm=blank_ink_ppm,
            )
            pages.append(page_text)
            if on_page is not None:
                on_page(page_text)
    return pages


async def extract_text_pages_async(
    path: str,
    force_ocr: bool = False,
    use_ocr_threshold: int = 100,
    include_blocks: bool = False,
    include_words: bool = False,
) -> list[PdfPageText]:
    executor = run_in_ocr_executor if force_ocr else run_in_cpu_executor
    return await executor(
        extract_text_pages,
        path,
        force_ocr,
        use_ocr_threshold,
        include_blocks,
        include_words,
    )


async def extract_text_pages_stream(
    path: str,
    force_ocr: bool = False,
    use_ocr_threshold: int = 100,
    include_blocks: bool = False,
    include_words: bool = False,
    page_start: int | None = None,
    page_end: int | None = None,
    supplied_pages: Mapping[int, tuple[str, str]] | None = None,
    blank_page: BlankPageTest | None = None,
) -> AsyncIterator[PdfExtractStart | PdfPageText]:
    """Stream extraction as it happens: yields one ``PdfExtractStart`` (page
    count) the moment the document opens, then each ``PdfPageText`` as its
    page finishes (native or OCR).

    Runs the whole sync loop on ONE executor worker (same thread-safety
    discipline as ``extract_text_pages_async`` — the Document never leaves
    its thread); pages cross back to the event loop via a queue. An
    extraction error is re-raised here after all already-extracted pages
    have been yielded. A stream that yields fewer (or other) pages than the
    document holds raises ``PdfPagesMissingError`` at its end.
    """
    executor = run_in_ocr_executor if force_ocr else run_in_cpu_executor

    def _work(emit: Callable[[PdfExtractStart | PdfPageText], None]) -> list[PdfPageText]:
        return extract_text_pages(
            path,
            force_ocr,
            use_ocr_threshold,
            include_blocks,
            include_words,
            lambda total_pages: emit(PdfExtractStart(total_pages=total_pages)),
            emit,
            page_start,
            page_end,
            supplied_pages,
            blank_page,
        )

    # THE PAGE-COUNT INVARIANT: every page the document (or the requested
    # slice) holds is yielded exactly once, in order — otherwise the stream
    # raises instead of ending quietly with missing text.
    total_pages: int | None = None
    got: list[int] = []
    async for item in iter_sync_stream(executor, _work):
        if isinstance(item, PdfExtractStart):
            total_pages = item.total_pages
        else:
            got.append(item.page_number)
        yield item
    if total_pages is None:
        raise PdfPagesMissingError(path, [], got)
    first, last = resolve_page_range(total_pages, page_start, page_end)
    expected = list(range(first, last + 1))
    if got != expected:
        raise PdfPagesMissingError(path, expected, got)


def extract_text_pages_from_bytes(
    pdf_bytes: bytes,
    force_ocr: bool = False,
    use_ocr_threshold: int = 100,
    include_blocks: bool = False,
    include_words: bool = False,
) -> list[PdfPageText]:
    with pdf_temp_file(pdf_bytes) as tmp_path:
        return extract_text_pages(
            str(tmp_path),
            force_ocr=force_ocr,
            use_ocr_threshold=use_ocr_threshold,
            include_blocks=include_blocks,
            include_words=include_words,
        )


async def extract_text_pages_from_bytes_async(
    pdf_bytes: bytes,
    force_ocr: bool = False,
    use_ocr_threshold: int = 100,
    include_blocks: bool = False,
    include_words: bool = False,
) -> list[PdfPageText]:
    executor = run_in_ocr_executor if force_ocr else run_in_cpu_executor
    return await executor(
        extract_text_pages_from_bytes,
        pdf_bytes,
        force_ocr,
        use_ocr_threshold,
        include_blocks,
        include_words,
    )


def format_page_text(
    pages: list[PdfPageText],
    include_page_markers: bool = False,
    document_label: str | None = None,
) -> str:
    """Stitch per-page text into a single string, optionally with boundary markers."""
    parts: list[str] = []
    for page in pages:
        if include_page_markers:
            label = document_label or page.source_path or "document"
            parts.append(
                f"--- PDF_PAGE_START document={label} page={page.page_number} ---"
            )
        parts.append(page.text)
        if include_page_markers:
            label = document_label or page.source_path or "document"
            parts.append(
                f"--- PDF_PAGE_END document={label} page={page.page_number} ---"
            )
    return "\n".join(parts)


def extract_text_from_image_bytes(image_bytes: bytes) -> str:
    """Backwards-compatible re-export of the image OCR helper."""
    return ocr_image_bytes(image_bytes)


def extract_text_from_bytes_sync(
    pdf_bytes: bytes,
    force_ocr: bool = False,
    use_ocr_threshold: int = 100,
) -> str:
    """Legacy sync extractor using pypdfium2 + Tesseract.

    Kept for backwards compatibility with the standalone
    ``extract_text_from_pdf_bytes_sync`` public symbol. New code should prefer
    ``extract_text_pages_from_bytes`` + ``format_page_text``.
    """
    with pdf_temp_file(pdf_bytes) as tmp_path:
        doc = pdfium.PdfDocument(str(tmp_path))
        all_text = ""
        try:
            for page_num in range(len(doc)):
                page = doc[page_num]
                try:
                    if force_ocr:
                        bitmap = page.render(scale=bounded_render_dpi(*page.get_size(), 300) / 72)
                        pil_image = bitmap.to_pil()
                        if pil_image.mode != "RGB":
                            pil_image = pil_image.convert("RGB")
                        text = _tesseract().image_to_string(
                            pil_image, config=r"--oem 3 --psm 6"
                        )
                    else:
                        textpage = page.get_textpage()
                        text = textpage.get_text_range()
                        textpage.close()
                        if native_text_needs_ocr(text, use_ocr_threshold):
                            bitmap = page.render(scale=bounded_render_dpi(*page.get_size(), 300) / 72)
                            pil_image = bitmap.to_pil()
                            if pil_image.mode != "RGB":
                                pil_image = pil_image.convert("RGB")
                            text = _tesseract().image_to_string(
                                pil_image, config=r"--oem 3 --psm 6"
                            )
                    all_text += text
                finally:
                    page.close()
        finally:
            doc.close()
        return all_text


__all__ = [
    "native_page_text",
    "PdfHasNoPagesError",
    "PdfPageRangeError",
    "resolve_page_range",
    "extract_text_pages",
    "extract_text_pages_async",
    "extract_text_pages_from_bytes",
    "extract_text_pages_from_bytes_async",
    "format_page_text",
    "extract_text_from_image_bytes",
    "extract_text_from_bytes_sync",
]
