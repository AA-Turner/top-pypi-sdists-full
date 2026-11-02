from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel, Field, model_validator


@runtime_checkable
class AiChunkProcessor(Protocol):
    """Callable contract for AI-based chunk processing.

    Callers supply a concrete async function (or any async callable object)
    that accepts a single text chunk and returns a plain dict. The utility
    library never imports an AI SDK directly — the consumer owns that logic.
    """

    async def __call__(self, chunk: str) -> dict[str, Any]: ...


class PdfPipelineOptions(BaseModel):
    extract_text: bool = True
    force_ocr: bool = False
    use_ocr_threshold: int = 100
    extract_tables: bool = False
    chunk_and_process_with_ai: bool = False
    chunk_size: int = 2000
    overlap_size: int = 200
    template_name: str = "default"
    include_page_markers: bool = False
    include_page_metadata: bool = False
    include_block_metadata: bool = False
    include_word_metadata: bool = False
    include_chunk_metadata: bool = False
    # Set to a full cloud URI to upload the extracted text after processing.
    # Supports any configured backend, e.g.:
    #   "s3://bucket/pdf_results/"
    #   "server://uploads/pdf_results/"
    # Leave as None (default) to skip upload.
    upload_result_to: str | None = None


class PdfPageRange(BaseModel):
    start: int = Field(ge=1)
    end: int = Field(ge=1)

    @model_validator(mode="after")
    def _validate_order(self) -> "PdfPageRange":
        if self.start > self.end:
            raise ValueError("Page range start must be <= end.")
        return self


class PdfCropBox(BaseModel):
    x0: float
    y0: float
    x1: float
    y1: float


class PdfBinaryResult(BaseModel):
    content: bytes = Field(repr=False)
    page_count: int
    operation: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class PdfSplitPart(BaseModel):
    content: bytes = Field(repr=False)
    filename: str
    page_count: int
    page_numbers: list[int]


class PdfTextBlock(BaseModel):
    block_number: int
    block_type: int
    x0: float
    y0: float
    x1: float
    y1: float
    text: str


class PdfTextWord(BaseModel):
    word: str
    x0: float
    y0: float
    x1: float
    y1: float
    block_number: int
    line_number: int
    word_number: int


class PdfPageText(BaseModel):
    page_number: int
    page_index: int
    width: float
    height: float
    rotation: int
    text: str
    extraction_method: str
    char_count: int
    source_path: str | None = None
    blocks: list[PdfTextBlock] | None = None
    words: list[PdfTextWord] | None = None


class PdfExtractStart(BaseModel):
    """First item yielded by ``extract_text_pages_stream`` — the document is
    open and the page count is known before any page has been extracted."""

    total_pages: int


class PdfPageScanned(BaseModel):
    """Generic per-page progress marker yielded by the ``*_stream`` analyzers
    whose per-page step has no payload of its own (e.g. repeated-regions
    scanning)."""

    page_number: int


class PdfPageSpan(BaseModel):
    page_number: int
    page_index: int
    page_char_start: int
    page_char_end: int
    chunk_char_start: int
    chunk_char_end: int


class PdfTextChunk(BaseModel):
    chunk_id: str
    chunk_index: int
    text: str
    document_char_start: int
    document_char_end: int
    char_count: int
    page_numbers: list[int]
    page_spans: list[PdfPageSpan]
    overlap_previous_chars: int = 0
    overlap_next_chars: int = 0
    previous_overlap_text: str | None = None
    next_overlap_text: str | None = None
    token_estimate: int
    source_document: str | None = None


class PdfChunkedTextResult(BaseModel):
    text: str
    chunks: list[PdfTextChunk]
    page_count: int
    chunk_size: int
    overlap_size: int


class PdfResult(BaseModel):
    raw_text: str | None = None
    pages: list[PdfPageText] | None = None
    chunks: list[str] | None = None
    chunk_records: list[PdfTextChunk] | None = None
    ai_processed: list[dict[str, Any]] | None = None
    tables_path: str | None = None
    cloud_uri: str | None = None
    file_id: str | None = None
    storage_uri: str | None = None


__all__ = [
    "AiChunkProcessor",
    "PdfPipelineOptions",
    "PdfPageRange",
    "PdfCropBox",
    "PdfBinaryResult",
    "PdfSplitPart",
    "PdfTextBlock",
    "PdfTextWord",
    "PdfPageText",
    "PdfPageSpan",
    "PdfTextChunk",
    "PdfChunkedTextResult",
    "PdfResult",
]
