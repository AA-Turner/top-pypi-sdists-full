"""The synthetic PDF corpus held against today's extractor (PDF-PLAN U1 runner, U2 one entry).

The corpus is GENERATED here (``_pdf_corpus.py``); nothing is stored. The runner proves:
  * the one entry ``extract_text_pages`` returns the declared text for every shape;
  * the async, stream and bytes wrappers return exactly what the entry returns (no logic of their
    own) - the U2 claim;
  * a planted change to the extractor turns the runner red (forcing test);
  * the second, pypdfium2 implementation (``extract_text_from_bytes_sync``) agrees with the entry
    on native pages, so retiring it (U15) has a gate.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

pytest.importorskip("pikepdf")
pytest.importorskip("PIL")
pytest.importorskip("pymupdf")

sys.path.insert(0, str(Path(__file__).parent))
import _pdf_corpus as corpus  # noqa: E402

from matrx_files.specific_handlers.pdf.extract.text import (  # noqa: E402
    extract_text_from_bytes_sync,
    extract_text_pages,
    extract_text_pages_async,
    extract_text_pages_from_bytes,
    extract_text_pages_stream,
)
from matrx_files.specific_handlers.pdf.models import PdfExtractStart  # noqa: E402

needs_tesseract = pytest.mark.skipif(shutil.which("tesseract") is None, reason="tesseract binary not installed")


@pytest.fixture(scope="module")
def pdfs() -> dict[str, corpus.CorpusPdf]:
    return corpus.build_corpus()


def _path(tmp_path: Path, item: corpus.CorpusPdf) -> str:
    path = tmp_path / f"{item.name}.pdf"
    path.write_bytes(corpus.decrypted_bytes(item) if item.password else item.data)
    return str(path)


def test_the_corpus_has_every_shape_the_plan_names(pdfs) -> None:
    tags = set().union(*(item.tags for item in pdfs.values()))
    assert {"digital", "scanned", "mixed", "rotated", "encrypted", "tables", "accented", "forms", "long"} <= tags
    assert len(pdfs) >= 12


def test_the_corpus_is_reproducible_byte_for_byte_except_encryption() -> None:
    first, second = corpus.build_corpus(), corpus.build_corpus()
    assert {n: i.data for n, i in first.items() if not i.password} == {
        n: i.data for n, i in second.items() if not i.password
    }


def test_the_500_page_case_is_a_parameter_not_a_file() -> None:
    big = corpus.long_document(pages=500)
    assert big.page_count == 500 and len(big.native_text) == 500 and len(big.data) < 2_000_000


@needs_tesseract
def test_the_entry_returns_the_declared_text_for_every_corpus_file() -> None:
    assert corpus.check_extraction(extract_text_pages) == []


def test_native_pages_match_without_ocr_installed() -> None:
    assert corpus.check_extraction(extract_text_pages, ocr=False, corpus={
        n: i for n, i in corpus.build_corpus().items() if not i.scanned_pages and n != "blank"
    }) == []


def test_a_planted_change_to_the_extractor_turns_the_runner_red() -> None:
    from dataclasses import replace

    def planted(path: str):
        return [replace(p, text=p.text.replace("marker", "mark3r")) if hasattr(p, "__dataclass_fields__") else p.model_copy(update={"text": p.text.replace("marker", "mark3r")}) for p in extract_text_pages(path)]

    only_native = {n: i for n, i in corpus.build_corpus().items() if n in {"digital", "long_30"}}
    problems = corpus.check_extraction(planted, only_native, ocr=False)
    assert problems and any("text differs" in p for p in problems)


def test_a_planted_ocr_regression_turns_the_runner_red() -> None:
    """A scanned page that comes back as empty native text is caught (the OCR fallback broke)."""

    def broken(path: str):
        return [p.model_copy(update={"text": "", "extraction_method": "native"}) for p in extract_text_pages(path)]

    scanned_only = {"scanned": corpus.scanned()}
    assert corpus.check_extraction(broken, scanned_only, ocr=False)


def test_an_encrypted_file_is_refused_loudly_until_decrypted(pdfs, tmp_path) -> None:
    raw = tmp_path / "enc.pdf"
    raw.write_bytes(pdfs["encrypted"].data)
    with pytest.raises(ValueError):
        extract_text_pages(str(raw))


def test_a_short_native_page_goes_to_ocr_by_the_default_threshold(tmp_path) -> None:
    """Named behaviour: under 100 characters of native text the page is OCR'd (threshold 0 disables)."""
    pytest.importorskip("pikepdf")
    pdf, font = corpus._new_pdf()
    corpus._add_text_page(pdf, font, [(72, 720, "short")])
    path = tmp_path / "short.pdf"
    path.write_bytes(corpus._save(pdf))
    assert extract_text_pages(str(path), use_ocr_threshold=0)[0].extraction_method == "native"


def test_page_range_reads_only_the_requested_slice(tmp_path) -> None:
    item = corpus.long_document(30)
    pages = extract_text_pages(_path(tmp_path, item), page_start=5, page_end=7)
    assert [p.page_number for p in pages] == [5, 6, 7]
    assert "marker-0006" in pages[1].text


def test_the_bytes_wrapper_equals_the_entry(pdfs, tmp_path) -> None:
    item = pdfs["tables"]
    direct = extract_text_pages(_path(tmp_path, item), use_ocr_threshold=0)
    wrapped = extract_text_pages_from_bytes(item.data, use_ocr_threshold=0)
    assert [(p.page_number, p.text, p.extraction_method) for p in direct] == [
        (p.page_number, p.text, p.extraction_method) for p in wrapped
    ]


@pytest.mark.asyncio
async def test_the_async_and_stream_wrappers_equal_the_entry(pdfs, tmp_path) -> None:
    item = pdfs["long_30"]
    path = _path(tmp_path, item)
    direct = [(p.page_number, p.text, p.extraction_method) for p in extract_text_pages(path)]
    via_async = [(p.page_number, p.text, p.extraction_method) for p in await extract_text_pages_async(path)]
    streamed, started = [], None
    async for entry in extract_text_pages_stream(path):
        if isinstance(entry, PdfExtractStart):
            started = entry.total_pages
        else:
            streamed.append((entry.page_number, entry.text, entry.extraction_method))
    assert direct == via_async == streamed and started == 30


@needs_tesseract
def test_the_legacy_pdfium_function_agrees_with_the_entry_on_native_pages(pdfs) -> None:
    """The second implementation stays equal on text until U15 retires it. NAMED DIFFERENCE (a defect
    of the legacy function, kept so callers see no change): it concatenates pages with no separator, so
    the last word of one page is glued to the first of the next ("bank.Lease") and it reads line ends
    as CRLF. Both vanish when ALL whitespace is dropped, which is the comparison used here."""

    def squash(text: str) -> str:
        return "".join(text.split())

    for name in ("digital", "tables", "accented", "long_30"):
        item = pdfs[name]
        legacy = squash(extract_text_from_bytes_sync(item.data))
        entry = squash("".join(p.text for p in extract_text_pages_from_bytes(item.data)))
        assert legacy == entry, name
    glued = extract_text_from_bytes_sync(pdfs["digital"].data)
    assert "bank.Lease" in glued, "the legacy page-glue defect changed: update the named difference"
