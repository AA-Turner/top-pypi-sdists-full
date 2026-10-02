r"""Provide a resolution utility for creating LangChain document loader
models."""

from __future__ import annotations

__all__ = ["resolve_document_loader"]

from typing import TYPE_CHECKING, Any

from langchain_core.document_loaders import BaseLoader

from zenpyre.utils.resolve import resolve_object

if TYPE_CHECKING:
    from zenpyre.utils.config import BaseConfig


def resolve_document_loader(
    document_loader: BaseLoader | dict[str, Any] | BaseConfig,
) -> BaseLoader:
    """Resolve a LangChain
    :class:`~langchain_core.document_loaders.BaseLoader` instance from
    an existing object, a configuration dictionary, or a
    :class:`~zenpyre.utils.config.BaseConfig`.

    If ``document_loader`` is already a
    :class:`~langchain_core.document_loaders.BaseLoader` instance it is
    returned as-is.  If it is a :class:`dict` or a
    :class:`~zenpyre.utils.config.BaseConfig`, it is treated as an
    ``objectory`` factory configuration and instantiated via
    :func:`objectory.factory`. See
    :func:`~zenpyre.utils.resolve.resolve_object` for details.

    Args:
        document_loader: Either a fully configured
            :class:`~langchain_core.document_loaders.BaseLoader`
            instance, a :class:`dict` containing an ``objectory``
            factory specification (must include a ``"_target_"`` key
            pointing to the fully-qualified class name), or a
            :class:`~zenpyre.utils.config.BaseConfig` whose
            ``to_kwargs()`` includes a ``"_target_"`` key.

    Returns:
        A configured :class:`~langchain_core.document_loaders.BaseLoader`
        instance.

    Raises:
        TypeError: If the resolved object is not a
            :class:`~langchain_core.document_loaders.BaseLoader`
            instance.

    Example:
        ```pycon
        >>> from langchain_core.document_loaders import BaseLoader
        >>> from zenpyre.document_loaders import resolve_document_loader
        >>> class MyLoader(BaseLoader):
        ...     def lazy_load(self):
        ...         return iter([])
        ...
        >>> # From an existing instance:
        >>> document_loader = resolve_document_loader(MyLoader())
        >>> # From a configuration dictionary:
        >>> document_loader = resolve_document_loader(  # doctest: +SKIP
        ...     {
        ...         "_target_": "langchain_core.document_loaders.LangSmithLoader",
        ...         "project_name": "my-project",
        ...     }
        ... )

        ```
    """
    return resolve_object(document_loader, cls=BaseLoader)
