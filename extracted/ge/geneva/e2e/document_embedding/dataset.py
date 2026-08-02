from __future__ import annotations

import logging
import os

import pyarrow as pa
import pyarrow.dataset as ds

SOURCE_METADATA_PATH = "s3://ray-example-data/digitalcorpora/metadata/"
SOURCE_METADATA_REGION = os.environ.get("DOC_METADATA_REGION", "us-west-2")

_LOG = logging.getLogger(__name__)


def _normalize_s3_path(uri: str) -> str:
    """
    PyArrow + S3FileSystem expect paths without the s3:// scheme when a filesystem
    is provided. This strips the scheme if present.
    """
    if uri.startswith("s3://"):
        return uri[len("s3://") :]
    return uri


def load_document_metadata(
    num_docs: int, source: str = SOURCE_METADATA_PATH, region: str = SOURCE_METADATA_REGION
) -> pa.Table:
    """
    Load a small slice of the digitalcorpora metadata parquet dataset.

    The dataset lives in a public S3 bucket and contains two columns:
    - file_name
    - uploaded_pdf_path (S3 path to the PDF)

    Args:
        num_docs: Maximum number of rows to load. Reads fragments until the
                  requested count is reached.
        source: Parquet dataset URI.

    Returns:
        A PyArrow Table with up to num_docs rows. Empty table if nothing was read.
    """
    try:
        fs = pa.fs.S3FileSystem(anonymous=True, region=region)
        dataset = ds.dataset(_normalize_s3_path(source), format="parquet", filesystem=fs)
    except Exception as exc:  # pragma: no cover - network issues are environment-specific
        _LOG.warning("Failed to open dataset %s: %s", source, exc)
        return pa.table({"file_name": [], "uploaded_pdf_path": []})

    tables: list[pa.Table] = []
    remaining = max(num_docs, 0)

    for fragment in dataset.get_fragments():
        try:
            table = fragment.to_table(columns=["file_name", "uploaded_pdf_path"])
        except Exception as exc:  # pragma: no cover
            _LOG.warning("Failed to read fragment %s: %s", fragment, exc)
            continue
        if len(table) == 0:
            continue

        if remaining and len(table) > remaining:
            table = table.slice(0, remaining)

        tables.append(table)
        remaining -= len(table)
        if remaining <= 0:
            break

    if not tables:
        _LOG.warning("No document metadata rows loaded from %s", source)
        return pa.table({"file_name": [], "uploaded_pdf_path": []})

    result = pa.concat_tables(tables)
    _LOG.info(
        "Loaded %s documents from %s (requested %s)", len(result), source, num_docs
    )
    return result
