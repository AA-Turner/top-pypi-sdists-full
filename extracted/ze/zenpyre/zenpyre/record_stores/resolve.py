r"""Provide a resolution utility for creating zenpyre BaseRecordStore
models."""

from __future__ import annotations

__all__ = ["resolve_record_store"]

from typing import TYPE_CHECKING, Any

from zenpyre.record_stores.base import BaseRecordStore
from zenpyre.utils.resolve import resolve_object

if TYPE_CHECKING:
    from zenpyre.utils.config import BaseConfig


def resolve_record_store(
    record_store: BaseRecordStore | dict[str, Any] | BaseConfig,
) -> BaseRecordStore:
    """Resolve a :class:`~zenpyre.record_stores.base.BaseRecordStore`
    instance from an existing object, a configuration dictionary, or a
    :class:`~zenpyre.utils.config.BaseConfig`.

    If ``record_store`` is already a
    :class:`~zenpyre.record_stores.base.BaseRecordStore` instance
    it is returned as-is.  If it is a :class:`dict` or a
    :class:`~zenpyre.utils.config.BaseConfig`, it is treated as an
    ``objectory`` factory configuration and instantiated via
    :func:`objectory.factory`. See
    :func:`~zenpyre.utils.resolve.resolve_object` for details.

    Args:
        record_store: Either a fully configured
            :class:`~zenpyre.record_stores.base.BaseRecordStore`
            instance, a :class:`dict` containing an ``objectory``
            factory specification (must include a ``"_target_"`` key
            pointing to the fully-qualified class name), or a
            :class:`~zenpyre.utils.config.BaseConfig` whose
            ``to_kwargs()`` includes a ``"_target_"`` key.

    Returns:
        A configured
        :class:`~zenpyre.record_stores.base.BaseRecordStore`
        instance.

    Raises:
        TypeError: If the resolved object is not a
            :class:`~zenpyre.record_stores.base.BaseRecordStore`
            instance.

    Example:
        ```pycon
        >>> from zenpyre.record_stores import InMemoryRecordStore, resolve_record_store
        >>> # From an existing instance:
        >>> record_store = resolve_record_store(InMemoryRecordStore())
        >>> # From a configuration dictionary:
        >>> record_store = resolve_record_store(
        ...     {"_target_": "zenpyre.record_stores.InMemoryRecordStore"}
        ... )

        ```
    """
    return resolve_object(record_store, cls=BaseRecordStore)
