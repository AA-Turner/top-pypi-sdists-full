r"""Provide the base factory interface for creating LangChain document
loader models."""

from __future__ import annotations

__all__ = ["BaseLoaderFactory"]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.document_loaders import BaseLoader


class BaseLoaderFactory(ABC):
    """Abstract base class for document loader factories.

    Subclasses implement :meth:`make_loader` to instantiate and return
    a configured :class:`~langchain_core.document_loaders.BaseLoader`
    object.  This pattern decouples document loader creation from the
    rest of the codebase, making it easy to swap loaders (e.g. file,
    web, database) without changing call sites.

    Example:
        ```pycon
        >>> from typing import Iterator
        >>> from langchain_core.document_loaders import BaseLoader
        >>> from langchain_core.documents import Document
        >>> from zenpyre.document_loaders.factory import BaseLoaderFactory
        >>> class MyLoaderFactory(BaseLoaderFactory):
        ...     def make_loader(self) -> BaseLoader:
        ...         class MyLoader(BaseLoader):
        ...             def lazy_load(self) -> Iterator[Document]:
        ...                 return iter([])
        ...         return MyLoader()
        ...

        ```
    """

    @abstractmethod
    def make_loader(self) -> BaseLoader:
        """Create and return a configured document loader instance.

        Returns:
            A :class:`~langchain_core.document_loaders.BaseLoader`
            instance ready for use.
        """
