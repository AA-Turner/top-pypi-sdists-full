r"""Contain code to inspect embeddings."""

from __future__ import annotations

__all__ = ["inspect_embeddings"]

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_chroma import Chroma

logger: logging.Logger = logging.getLogger(__name__)

_PREVIEW_DIMS = 5


def inspect_embeddings(
    vector_store: Chroma,
    n: int = 2,
) -> None:
    """Log a summary of raw embeddings retrieved from a Chroma vector
    store.

    Fetches embeddings, documents, metadata, and IDs from
    ``vector_store`` and logs a preview of the first ``n`` entries.
    Each entry shows its ID, source metadata, document text, embedding
    dimensionality, and the first few values of its vector.

    .. note::
        This function uses :meth:`~langchain_chroma.Chroma.get`, which
        is specific to Chroma and not available on all
        :class:`~langchain_core.vectorstores.VectorStore` backends.

    Args:
        vector_store: A :class:`~langchain_chroma.Chroma` vector store
            instance to inspect.
        n: Number of embeddings to preview. Defaults to ``2``.
    """
    db_data = vector_store.get(include=["embeddings", "documents", "metadatas"])

    embeddings = db_data["embeddings"]
    documents = db_data["documents"]
    metadatas = db_data["metadatas"]
    ids = db_data["ids"]

    if embeddings is None or documents is None or metadatas is None or ids is None:
        logger.info("No embeddings found in the vector store.")
        return

    logger.info("Retrieved %s embeddings from the vector store.\n", f"{len(embeddings):,}")

    for i in range(min(n, len(embeddings))):
        vector = embeddings[i]
        preview = vector[:_PREVIEW_DIMS]
        preview_str = ", ".join(f"{v:.4f}" for v in preview)
        ellipsis = ", ..." if len(vector) > _PREVIEW_DIMS else ""

        logger.info("Chunk ID:   %s", ids[i])
        logger.info("Source:     %s", metadatas[i].get("source"))
        logger.info("Text:       %s", documents[i])
        logger.info("Dimensions: %s numbers long", len(vector))
        logger.info("Vector:     [%s%s]\n", preview_str, ellipsis)
