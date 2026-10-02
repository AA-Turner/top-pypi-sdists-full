r"""Provide a concrete default factory for LangChain document loader
models."""

from __future__ import annotations

__all__ = ["LoaderFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from zenpyre.document_loaders.factory.base import BaseLoaderFactory

if TYPE_CHECKING:
    from langchain_core.document_loaders import BaseLoader


class LoaderFactory(BaseLoaderFactory, MultilineDisplayMixin):
    """A concrete document loader factory that wraps a pre-built
    :class:`~langchain_core.document_loaders.BaseLoader` instance.

    Use this when the document loader is already instantiated and you
    simply want to wrap it in the :class:`~BaseLoaderFactory`
    interface — for example, when injecting a fixed loader into a
    component that expects a factory.

    Args:
        loader: A fully configured
            :class:`~langchain_core.document_loaders.BaseLoader`
            instance to return from :meth:`make_loader`.

    Example:
        ```pycon
        >>> from typing import Iterator
        >>> from langchain_core.document_loaders import BaseLoader
        >>> from langchain_core.documents import Document
        >>> from zenpyre.document_loaders.factory import LoaderFactory
        >>> class MyLoader(BaseLoader):
        ...     def lazy_load(self) -> Iterator[Document]:
        ...         return iter([])
        ...
        >>> factory = LoaderFactory(MyLoader())
        >>> loader = factory.make_loader()

        ```
    """

    def __init__(self, loader: BaseLoader) -> None:
        self._loader = loader

    def make_loader(self) -> BaseLoader:
        return self._loader

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"loader": self._loader}
