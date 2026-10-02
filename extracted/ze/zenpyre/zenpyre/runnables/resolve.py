r"""Provide a resolution utility for creating LangChain Runnable
models."""

from __future__ import annotations

__all__ = ["resolve_runnable"]

from typing import TYPE_CHECKING, Any, TypeVar

from langchain_core.runnables import Runnable

from zenpyre.utils.resolve import resolve_object

if TYPE_CHECKING:
    from zenpyre.utils.config import BaseConfig

Input = TypeVar("Input")
Output = TypeVar("Output")


def resolve_runnable(
    runnable: Runnable[Input, Output] | dict[str, Any] | BaseConfig,
) -> Runnable[Input, Output]:
    """Resolve a LangChain :class:`~langchain_core.runnables.Runnable`
    instance from an existing object, a configuration dictionary, or a
    :class:`~zenpyre.utils.config.BaseConfig`.

    If ``runnable`` is already a
    :class:`~langchain_core.runnables.Runnable` instance it is
    returned as-is.  If it is a :class:`dict` or a
    :class:`~zenpyre.utils.config.BaseConfig`, it is treated as an
    ``objectory`` factory configuration and instantiated via
    :func:`objectory.factory`. See
    :func:`~zenpyre.utils.resolve.resolve_object` for details.

    Args:
        runnable: Either a fully configured
            :class:`~langchain_core.runnables.Runnable`
            instance, a :class:`dict` containing an ``objectory``
            factory specification (must include a ``"_target_"`` key
            pointing to the fully-qualified class name), or a
            :class:`~zenpyre.utils.config.BaseConfig` whose
            ``to_kwargs()`` includes a ``"_target_"`` key.

    Returns:
        A configured :class:`~langchain_core.runnables.Runnable`
        instance.

    Raises:
        TypeError: If the resolved object is not a
            :class:`~langchain_core.runnables.Runnable`
            instance.

    Example:
        ```pycon
        >>> from langchain_core.runnables import Runnable
        >>> from zenpyre.runnables import resolve_runnable
        >>> class MyRunnable(Runnable):
        ...     def invoke(self, input: Any, config: Any = None, **kwargs: Any) -> Any:
        ...         return input
        ...
        >>> # From an existing instance:
        >>> runnable = resolve_runnable(MyRunnable())
        >>> # From a configuration dictionary:
        >>> runnable = resolve_runnable(
        ...     {"_target_": "langchain_core.runnables.RunnablePassthrough"}
        ... )

        ```
    """
    return resolve_object(runnable, cls=Runnable)
