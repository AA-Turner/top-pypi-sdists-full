r"""Provide a resolution utility for creating zenpyre BaseIngestor
models."""

from __future__ import annotations

__all__ = ["resolve_ingestor"]

from typing import TYPE_CHECKING, Any, TypeVar

from zenpyre.ingestors.base import BaseIngestor
from zenpyre.utils.resolve import resolve_object

if TYPE_CHECKING:
    from zenpyre.utils.config import BaseConfig

T = TypeVar("T")


def resolve_ingestor(
    ingestor: BaseIngestor[T] | dict[str, Any] | BaseConfig,
) -> BaseIngestor[T]:
    """Resolve a :class:`~zenpyre.ingestors.base.BaseIngestor` instance
    from an existing object, a configuration dictionary, or a
    :class:`~zenpyre.utils.config.BaseConfig`.

    If ``ingestor`` is already a
    :class:`~zenpyre.ingestors.base.BaseIngestor` instance it is
    returned as-is.  If it is a :class:`dict` or a
    :class:`~zenpyre.utils.config.BaseConfig`, it is treated as an
    ``objectory`` factory configuration and instantiated via
    :func:`objectory.factory`. See
    :func:`~zenpyre.utils.resolve.resolve_object` for details.

    Args:
        ingestor: Either a fully configured
            :class:`~zenpyre.ingestors.base.BaseIngestor`
            instance, a :class:`dict` containing an ``objectory``
            factory specification (must include a ``"_target_"`` key
            pointing to the fully-qualified class name), or a
            :class:`~zenpyre.utils.config.BaseConfig` whose
            ``to_kwargs()`` includes a ``"_target_"`` key.

    Returns:
        A configured :class:`~zenpyre.ingestors.base.BaseIngestor`
        instance.

    Raises:
        TypeError: If the resolved object is not a
            :class:`~zenpyre.ingestors.base.BaseIngestor`
            instance.

    Example:
        ```pycon
        >>> from zenpyre.ingestors import resolve_ingestor
        >>> from zenpyre.ingestors.base import BaseIngestor
        >>> class MyIngestor(BaseIngestor):
        ...     def ingest(self) -> Any:
        ...         return {"hello": "world"}
        ...
        >>> # From an existing instance:
        >>> ingestor = resolve_ingestor(MyIngestor())
        >>> # From a configuration dictionary:
        >>> ingestor = resolve_ingestor(  # doctest: +SKIP
        ...     {"_target_": "my_package.ingestors.MyIngestor"}
        ... )

        ```
    """
    return resolve_object(ingestor, cls=BaseIngestor)
