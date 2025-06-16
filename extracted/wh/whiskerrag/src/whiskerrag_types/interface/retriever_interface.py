from abc import ABC, abstractmethod
from typing import Any, Generic, List, TypeVar

from whiskerrag_types.model.retrieval import RetrievalChunk, RetrievalRequest

T = TypeVar("T", bound=RetrievalRequest)
R = TypeVar("R", bound=RetrievalChunk)


class BaseRetriever(Generic[T, R], ABC):
    """Retriever interface."""

    def __init__(self, **kwargs: Any) -> None:
        pass

    @abstractmethod
    async def retrieve(self, params: T, tenant_id: str) -> List[R]:
        """
        Retrieve data based on the given parameters.
        Args:
            params (T): The parameters for retrieval.
            tenant_id (str): The tenant ID.
        Returns:
            List[R]: A list of retrieval results.
        """
        pass
