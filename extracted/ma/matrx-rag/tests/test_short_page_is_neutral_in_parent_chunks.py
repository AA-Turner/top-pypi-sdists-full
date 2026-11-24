"""A short verbatim page joins its neighbours; it never names or splits a section.

Break caught: ``chunk_pdf_pages`` treated ``short_page_verbatim`` as a section of its own, so a
one-line page in the middle of a lease forced a parent cut on both sides and became a tiny parent
labelled 'short_page_verbatim' (search section metadata degraded).
"""

from matrx_rag.llm import SHORT_PAGE_KIND, CleanedPage
from matrx_rag.pdf_pipeline import _ExtractedPage, chunk_pdf_pages

PROSE = "The tenant shall return the unit in the condition received, ordinary wear excepted. " * 6


def _pages(kinds_and_text):
    pages = [_ExtractedPage(page_index=i, text=t, used_ocr=False, char_count=len(t)) for i, (_, t) in enumerate(kinds_and_text)]
    cleaned = [CleanedPage(text=t, section_kind=k) for k, t in kinds_and_text]
    return pages, cleaned


def _parents(chunks):
    return [c for c in chunks if c.metadata.get("role") == "parent"]


def test_a_short_page_mid_section_does_not_split_the_parent_or_name_it():
    pages, cleaned = _pages(
        [
            ("lease", PROSE),
            (SHORT_PAGE_KIND, "Initials: M.O. / R.K."),
            ("lease", PROSE),
        ]
    )
    parents = _parents(chunk_pdf_pages(pages, cleaned))
    assert len(parents) == 1
    assert parents[0].metadata["section_kind"] == "lease"
    assert parents[0].metadata["section_kinds_in_span"] == ["lease"]


def test_a_real_section_change_after_a_short_page_still_cuts():
    pages, cleaned = _pages(
        [
            ("lease", PROSE),
            (SHORT_PAGE_KIND, "Initials: M.O. / R.K."),
            ("invoice", PROSE),
        ]
    )
    parents = _parents(chunk_pdf_pages(pages, cleaned))
    assert [p.metadata["section_kind"] for p in parents] == ["lease", "invoice"]


def test_a_document_of_only_short_pages_labels_no_section():
    pages, cleaned = _pages([(SHORT_PAGE_KIND, "Call the boiler technician back"), (SHORT_PAGE_KIND, "Thursday")])
    parents = _parents(chunk_pdf_pages(pages, cleaned))
    assert len(parents) == 1 and parents[0].metadata["section_kind"] == ""
