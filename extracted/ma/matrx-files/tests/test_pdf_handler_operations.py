from __future__ import annotations

import pymupdf

from matrx_files.specific_handlers.pdf import (
    PDFHandler,
    PdfCropBox,
    PdfPageRange,
    PdfPipelineOptions,
)



def _sample_pdf(page_count: int = 3) -> bytes:
    doc = pymupdf.open()
    try:
        for page_num in range(1, page_count + 1):
            page = doc.new_page(width=300, height=400)
            page.insert_text((72, 72), f"Sample page {page_num}")
        return doc.tobytes()
    finally:
        doc.close()


def _page_count(pdf_bytes: bytes) -> int:
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    try:
        return doc.page_count
    finally:
        doc.close()


def test_extract_pages_from_bytes_preserves_selected_order() -> None:
    handler = PDFHandler(app_name="test_pdf_handler")

    result = handler.extract_pages_from_bytes(_sample_pdf(), pages=[3, 1])

    assert result.page_count == 2
    assert result.metadata["source_pages"] == [3, 1]
    assert _page_count(result.content) == 2


def test_crop_rotate_and_delete_pages_from_bytes() -> None:
    handler = PDFHandler(app_name="test_pdf_handler")
    pdf_bytes = _sample_pdf()

    cropped = handler.crop_pages_in_bytes(
        pdf_bytes,
        crop_box=PdfCropBox(x0=0, y0=0, x1=200, y1=300),
        pages=[1],
    )
    cropped_doc = pymupdf.open(stream=cropped.content, filetype="pdf")
    try:
        assert cropped_doc[0].cropbox.width == 200
        assert cropped_doc[0].cropbox.height == 300
    finally:
        cropped_doc.close()

    rotated = handler.rotate_pages_in_bytes(pdf_bytes, rotation=90, pages=[2])
    rotated_doc = pymupdf.open(stream=rotated.content, filetype="pdf")
    try:
        assert rotated_doc[1].rotation == 90
    finally:
        rotated_doc.close()

    deleted = handler.delete_pages_from_bytes(
        pdf_bytes,
        page_ranges=[PdfPageRange(start=2, end=2)],
    )
    assert deleted.page_count == 2
    assert _page_count(deleted.content) == 2


def test_merge_and_split_pdf_bytes() -> None:
    handler = PDFHandler(app_name="test_pdf_handler")
    pdf_bytes = _sample_pdf()

    merged = handler.merge_pdfs_from_bytes(
        [
            {"content": pdf_bytes, "pages": [1]},
            {"content": pdf_bytes, "page_ranges": [{"start": 2, "end": 3}]},
        ]
    )
    assert merged.page_count == 3
    assert _page_count(merged.content) == 3

    split = handler.split_pdf_bytes(pdf_bytes, max_pages_per_part=2)
    assert [part.page_count for part in split] == [2, 1]
    assert [part.page_numbers for part in split] == [[1, 2], [3]]


def test_extract_text_from_bytes() -> None:
    handler = PDFHandler(app_name="test_pdf_handler")

    text = handler.extract_text_from_bytes_sync(_sample_pdf(), use_ocr_threshold=0)

    assert "Sample page 1" in text
    assert "Sample page 3" in text


def test_page_aware_extraction_keeps_page_markers_and_line_breaks() -> None:
    handler = PDFHandler(app_name="test_pdf_handler")
    pdf_bytes = _sample_pdf(2)

    pages = handler.extract_text_pages_from_bytes(
        pdf_bytes,
        use_ocr_threshold=0,
        include_blocks=True,
        include_words=True,
    )
    text = handler.format_page_text(
        pages,
        include_page_markers=True,
        document_label="sample.pdf",
    )

    assert len(pages) == 2
    assert pages[0].page_number == 1
    assert pages[0].blocks is not None
    assert pages[0].words is not None
    assert pages[0].words[0].word == "Sample"
    assert "--- PDF_PAGE_START document=sample.pdf page=1 ---" in text
    assert "--- PDF_PAGE_END document=sample.pdf page=2 ---" in text
    assert "Sample page 1\n" in text


def test_page_aware_chunking_tracks_source_pages_and_overlap() -> None:
    handler = PDFHandler(app_name="test_pdf_handler")
    pages = handler.extract_text_pages_from_bytes(
        _sample_pdf(4),
        use_ocr_threshold=0,
    )

    chunked = handler.chunk_page_text(
        pages,
        chunk_size=45,
        overlap_size=10,
        include_page_markers=True,
        document_label="sample.pdf",
    )

    assert len(chunked.chunks) > 1
    assert chunked.chunks[0].page_numbers == [1]
    assert chunked.chunks[0].page_spans[0].page_number == 1
    assert chunked.chunks[1].overlap_previous_chars > 0
    assert chunked.chunks[0].overlap_next_chars > 0
    assert chunked.chunks[0].chunk_id.startswith("sample.pdf:chunk:")


async def test_full_pipeline_can_return_page_metadata(tmp_path) -> None:
    handler = PDFHandler(app_name="test_pdf_handler")
    pdf_path = tmp_path / "sample.pdf"
    pdf_path.write_bytes(_sample_pdf(2))

    result = await handler.full_pipeline(
        str(pdf_path),
        PdfPipelineOptions(
            include_page_markers=True,
            include_page_metadata=True,
            include_block_metadata=True,
            include_word_metadata=True,
            include_chunk_metadata=True,
            chunk_and_process_with_ai=True,
            chunk_size=45,
            overlap_size=10,
            use_ocr_threshold=0,
        ),
        ai_processor=lambda chunk: _fake_ai_processor(chunk),
    )

    assert result.raw_text is not None
    assert "--- PDF_PAGE_START" in result.raw_text
    assert result.pages is not None
    assert result.pages[0].page_number == 1
    assert result.pages[0].blocks is not None
    assert result.pages[0].words is not None
    assert result.chunk_records is not None
    assert result.chunk_records[0].page_spans
    assert result.ai_processed is not None


async def _fake_ai_processor(chunk: str) -> dict[str, str]:
    return {"content": chunk[:10]}
