r"""Provide a configurable factory for LangChain document loader
models."""

from __future__ import annotations

__all__ = ["ConfigurableLoaderFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from zenpyre.document_loaders.factory.base import BaseLoaderFactory
from zenpyre.document_loaders.resolve import resolve_document_loader

if TYPE_CHECKING:
    from langchain_core.document_loaders import BaseLoader


class ConfigurableLoaderFactory(BaseLoaderFactory, MultilineDisplayMixin):
    """A concrete document loader factory that accepts either a pre-
    built :class:`~langchain_core.document_loaders.BaseLoader` instance
    or a configuration dictionary.

    When a dict is provided it is resolved at each :meth:`make_loader`
    call via :func:`~resolve_document_loader`, which uses ``objectory``
    to instantiate the configured class.  When an instance is provided
    it is returned as-is.

    Args:
        loader: A fully configured
            :class:`~langchain_core.document_loaders.BaseLoader`
            instance, or a :class:`dict` containing an ``objectory``
            factory specification (must include a ``"_target_"`` key
            pointing to the fully-qualified class name).

    Example:
        ```pycon
        >>> from typing import Iterator
        >>> from langchain_core.document_loaders import BaseLoader
        >>> from langchain_core.documents import Document
        >>> from zenpyre.document_loaders.factory import ConfigurableLoaderFactory
        >>> class MyLoader(BaseLoader):
        ...     def lazy_load(self) -> Iterator[Document]:
        ...         return iter([])
        ...
        >>> factory = ConfigurableLoaderFactory(MyLoader())
        >>> loader = factory.make_loader()

        ```
    """

    def __init__(self, loader: BaseLoader | dict[str, Any]) -> None:
        self._loader = loader

    def make_loader(self) -> BaseLoader:
        return resolve_document_loader(self._loader)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"loader": self._loader}
