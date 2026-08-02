# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
UDFs for the document embedding pipeline.

Steps:
1) Download PDF bytes from public S3
2) Extract page text with pypdf
3) Chunk text with RecursiveCharacterTextSplitter
4) Embed chunks with sentence-transformers/all-MiniLM-L6-v2
"""

from __future__ import annotations

import io
import logging
from contextlib import suppress
from typing import Any

import pyarrow as pa
import requests
import urllib3.util.ssl_ as _ssl_util

import geneva

# Workaround for boto3/botocore expecting urllib3.util.ssl_.DEFAULT_CIPHERS,
# which was removed in urllib3 2.5. Define a reasonable default when missing.
if not hasattr(_ssl_util, "DEFAULT_CIPHERS"):  # pragma: no cover - env specific
    _ssl_util.DEFAULT_CIPHERS = "HIGH:!aNULL:!eNULL:!MD5:!RC4"  # pyright: ignore[reportAttributeAccessIssue]

EMBED_MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384
MAX_PDF_PAGES = 100
CHUNK_SIZE = 2048
CHUNK_OVERLAP = 200
EMBEDDING_BATCH_SIZE = 10
NUM_GPU_NODES = 8

_LOG = logging.getLogger(__name__)

_PAGE_STRUCT = pa.struct(
    [pa.field("page_number", pa.int32()), pa.field("text", pa.large_string())]
)
_CHUNK_STRUCT = pa.struct(
    [
        pa.field("page_number", pa.int32()),
        pa.field("chunk_id", pa.int32()),
        pa.field("chunk", pa.large_string()),
    ]
)


def _to_https(path: str) -> str:
    """Convert s3://bucket/key to https://bucket.s3.amazonaws.com/key."""
    if path.startswith("s3://"):
        without_scheme = path[5:]
        bucket, _, key = without_scheme.partition("/")
        return f"https://{bucket}.s3.amazonaws.com/{key}"
    return path


def _get_splitter() -> Any:
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )


@geneva.udf(version="0.1", data_type=pa.large_binary())
def download_pdf(uploaded_pdf_path: str | None) -> bytes | None:
    """Fetch PDF bytes from a publicly readable S3 path."""
    if not uploaded_pdf_path:
        return None

    url = _to_https(uploaded_pdf_path)
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return resp.content
    except Exception as exc:  # pragma: no cover - network failures should not crash
        _LOG.warning("Failed to download %s: %s", uploaded_pdf_path, exc)
        return None


@geneva.udf(version="0.1", data_type=pa.list_(_PAGE_STRUCT))
def extract_pages(pdf_bytes: bytes | None) -> list[dict[str, Any]] | None:
    """Extract text for each page in the PDF."""
    if not pdf_bytes:
        return None

    try:
        import pypdf

        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        if len(reader.pages) > MAX_PDF_PAGES:
            _LOG.info(
                "Skipping PDF with %s pages (> %s)", len(reader.pages), MAX_PDF_PAGES
            )
            return None

        pages: list[dict[str, Any]] = []
        for page_number, page in enumerate(reader.pages):
            text = page.extract_text()
            if not text:
                continue
            pages.append({"page_number": page_number, "text": text})

        return pages or None
    except Exception as exc:  # pragma: no cover - protect pipeline
        _LOG.warning("Failed to parse PDF: %s", exc)
        return None


_SPLITTER: Any | None = None


@geneva.udf(version="0.1", data_type=pa.list_(_CHUNK_STRUCT))
def chunk_pages(pages: list[dict[str, Any]] | None) -> list[dict[str, Any]] | None:
    """Split page text into overlapping chunks (uses shared splitter)."""
    if not pages:
        return None

    global _SPLITTER  # noqa: PLW0603
    if _SPLITTER is None:
        _SPLITTER = _get_splitter()
    splitter = _SPLITTER
    if splitter is None:  # pragma: no cover
        raise RuntimeError("Text splitter failed to initialize")

    chunks: list[dict[str, Any]] = []
    for page in pages:
        text = page.get("text")
        page_number = int(page.get("page_number", 0))
        if not text:
            continue

        for idx, chunk_text in enumerate(splitter.split_text(text)):
            chunks.append(
                {
                    "page_number": page_number,
                    "chunk_id": int(idx),
                    "chunk": chunk_text,
                }
            )

    return chunks or None


@geneva.udf(
    version="0.1",
    data_type=pa.list_(pa.list_(pa.float32(), EMBEDDING_DIM)),
    batch_size=EMBEDDING_BATCH_SIZE,
    concurrency=NUM_GPU_NODES,
)
class ChunkEmbedder:
    """Generate embeddings for each chunk using SentenceTransformers."""

    def __init__(self, model_id: str = EMBED_MODEL_ID) -> None:
        self.model_id = model_id
        self._model: Any | None = None

    def setup(self) -> None:
        import torch
        from sentence_transformers import SentenceTransformer

        device = "cuda" if torch.cuda.is_available() else "cpu"
        self._model = SentenceTransformer(self.model_id, device=device)
        model = self._model
        if model is None:  # pragma: no cover
            raise RuntimeError("SentenceTransformer model failed to initialize")
        # compile can speed up inference on newer versions; safe no-op otherwise
        with suppress(AttributeError):
            model.compile()

    def __call__(self, chunks: list[dict[str, Any]] | None) -> list[list[float]] | None:
        if chunks is None:
            return None

        if self._model is None:
            self.setup()
        model = self._model
        if model is None:  # pragma: no cover
            raise RuntimeError("SentenceTransformer model failed to initialize")

        texts = [c.get("chunk") for c in chunks if c and c.get("chunk")]
        if not texts:
            return []

        embeddings = model.encode(
            texts,
            batch_size=EMBEDDING_BATCH_SIZE,
        )
        return embeddings.tolist()


__all__ = [
    "download_pdf",
    "extract_pages",
    "chunk_pages",
    "ChunkEmbedder",
    "EMBEDDING_DIM",
    "EMBED_MODEL_ID",
    "CHUNK_SIZE",
    "CHUNK_OVERLAP",
    "MAX_PDF_PAGES",
    "EMBEDDING_BATCH_SIZE",
    "NUM_GPU_NODES",
]
