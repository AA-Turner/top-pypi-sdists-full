"""**Vector store** stores embedded data and performs vector search.

One of the most common ways to store and search over unstructured data is to
embed it and store the resulting embedding vectors, and then query the store
and retrieve the data that are 'most similar' to the embedded query.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import (
    Any,
    Self,
    Iterable,
    Sequence,
    TypeAlias
)

Vector: TypeAlias = NotImplemented
VectorDocument: TypeAlias = NotImplemented

class VectorStore(ABC):
    """Interface for vector store."""

    def add_vectors(
        self,
        vectors: Iterable[Vector],
        metadatas: list[dict] | None = None,
        *,
        ids: list[str] | None = None,
        **kwargs: Any,
    ) -> list[str]:
        """Run more texts through the embeddings and add to the `VectorStore`.

        Args:
            texts: Iterable of strings to add to the `VectorStore`.
            metadatas: Optional list of metadatas associated with the texts.
            ids: Optional list of IDs associated with the texts.
            **kwargs: `VectorStore` specific parameters.
                One of the kwargs should be `ids` which is a list of ids
                associated with the texts.

        Returns:
            List of IDs from adding the texts into the `VectorStore`.

        Raises:
            ValueError: If the number of metadatas does not match the number of texts.
            ValueError: If the number of IDs does not match the number of texts.
        """
        raise NotImplementedError()


    def delete(self, ids: list[str] | None = None, **kwargs: Any) -> bool | None:
        """Delete by vector ID or other criteria.

        Args:
            ids: List of IDs to delete. If `None`, delete all.
            **kwargs: Other keyword arguments that subclasses might use.

        Returns:
            `True` if deletion is successful, `False` otherwise, `None` if not
                implemented.
        """
        msg = "delete method must be implemented by subclass."
        raise NotImplementedError(msg)

    def get_by_ids(self, ids: Sequence[str], /) -> list[VectorDocument]:
        """Get documents by their IDs.

        The returned documents are expected to have the ID field set to the ID of the
        document in the vector store.

        Fewer documents may be returned than requested if some IDs are not found or
        if there are duplicated IDs.

        Users should not assume that the order of the returned documents matches
        the order of the input IDs. Instead, users should rely on the ID field of the
        returned documents.

        This method should **NOT** raise exceptions if no documents are found for
        some IDs.

        Args:
            ids: List of IDs to retrieve.

        Returns:
            List of `Document` objects.
        """
        msg = f"{self.__class__.__name__} does not yet support get_by_ids."
        raise NotImplementedError(msg)

    def add_documents(self, documents: list[VectorDocument], **kwargs: Any) -> list[str]:
        """Add or update documents in the `VectorStore`.

        Args:
            documents: Documents to add to the `VectorStore`.
            **kwargs: Additional keyword arguments.

                If kwargs contains IDs and documents contain ids, the IDs in the kwargs
                will receive precedence.

        Returns:
            List of IDs of the added texts.
        """
        raise NotImplementedError()

    def similarity_search_by_vector(
        self, vector: list[float], k: int = 4, **kwargs: Any
    ) -> list[VectorDocument]:
        """Return docs most similar to embedding vector.

        Args:
            embedding: Embedding to look up documents similar to.
            k: Number of `Document` objects to return.
            **kwargs: Arguments to pass to the search method.

        Returns:
            List of `Document` objects most similar to the query vector.
        """
        raise NotImplementedError


    @classmethod
    def from_documents(
        cls,
        documents: list[VectorDocument],
        **kwargs: Any,
    ) -> Self:
        """Return `VectorStore` initialized from documents and embeddings.

        Args:
            documents: List of `Document` objects to add to the `VectorStore`.
            embedding: Embedding function to use.
            **kwargs: Additional keyword arguments.

        Returns:
            `VectorStore` initialized from documents and embeddings.
        """

        return NotImplementedError

    # @classmethod
    # @abstractmethod
    # def from_vectors(
    #     cls,
    #     texts: list[VectorDocument],
    #     metadatas: list[dict] | None = None,
    #     *,
    #     ids: list[str] | None = None,
    #     **kwargs: Any,
    # ) -> Self:
    #     """Return `VectorStore` initialized from texts and embeddings.

    #     Args:
    #         texts: Texts to add to the `VectorStore`.
    #         embedding: Embedding function to use.
    #         metadatas: Optional list of metadatas associated with the texts.
    #         ids: Optional list of IDs associated with the texts.
    #         **kwargs: Additional keyword arguments.

    #     Returns:
    #         `VectorStore` initialized from texts and embeddings.
    #     """
