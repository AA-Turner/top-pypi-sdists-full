r"""Contain code to inspect embeddings."""

from __future__ import annotations

__all__ = ["inspect_embeddings"]

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.vectorstores import VectorStore

logger: logging.Logger = logging.getLogger(__name__)


def inspect_embeddings(vector_store: VectorStore, n: int = 2) -> None:
    """Log a summary of documents retrieved from a vector store.

    Retrieves the first ``n`` documents via
    :meth:`~langchain_core.vectorstores.VectorStore.similarity_search`
    and logs each document's ID, source metadata, and text content.

    .. note::
        Unlike the Chroma-specific implementation, this function works
        on any :class:`~langchain_core.vectorstores.VectorStore` backend
        but does not show embedding vectors, as there is no standard
        cross-provider API for retrieving raw embeddings.

    Args:
        vector_store: Any
            :class:`~langchain_core.vectorstores.VectorStore` instance
            to inspect.
        n: Number of documents to preview. Defaults to ``2``.
    """
    docs = vector_store.similarity_search("", k=n)

    if not docs:
        logger.info("No documents found in the vector store")
        return

    logger.info("Retrieved %s documents from the vector store", f"{len(docs):,}")

    for _i, doc in enumerate(docs):
        logger.info("Chunk ID:   %s", doc.id)
        logger.info("Source:     %s", doc.metadata.get("source"))
        logger.info("Text:       %s\n", doc.page_content)
