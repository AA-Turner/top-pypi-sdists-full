r"""Provide a configurable factory for LangChain Runnable models."""

from __future__ import annotations

__all__ = ["ConfigurableRunnableFactory"]

from typing import TYPE_CHECKING, Any, TypeVar

from coola.display import MultilineDisplayMixin

from zenpyre.runnables import resolve_runnable
from zenpyre.runnables.factory.base import BaseRunnableFactory

if TYPE_CHECKING:
    from langchain_core.runnables import Runnable

Input = TypeVar("Input")
Output = TypeVar("Output")


class ConfigurableRunnableFactory(BaseRunnableFactory[Input, Output], MultilineDisplayMixin):
    """A concrete Runnable factory that accepts either a pre-built
    :class:`~langchain_core.runnables.Runnable` instance or a
    configuration dictionary.

    When a dict is provided it is resolved at each :meth:`make_runnable`
    call via :func:`~zenpyre.runnables.resolve_runnable`, which uses
    ``objectory`` to instantiate the configured class.  When an
    instance is provided it is returned as-is.

    Args:
        runnable: A fully configured
            :class:`~langchain_core.runnables.Runnable`
            instance, or a :class:`dict` containing an ``objectory``
            factory specification (must include a ``"_target_"`` key
            pointing to the fully-qualified class name).

    Example:
        ```pycon
        >>> from typing import Any
        >>> from langchain_core.runnables import Runnable
        >>> from zenpyre.runnables.factory import ConfigurableRunnableFactory
        >>> class MyRunnable(Runnable[Any, Any]):
        ...     def invoke(self, input: Any, config: Any = None, **kwargs: Any) -> Any:
        ...         return input
        ...
        >>> factory = ConfigurableRunnableFactory(MyRunnable())
        >>> runnable = factory.make_runnable()

        ```
    """

    def __init__(self, runnable: Runnable[Input, Output] | dict[str, Any]) -> None:
        self._runnable = runnable

    def make_runnable(self) -> Runnable[Input, Output]:
        return resolve_runnable(self._runnable)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"runnable": self._runnable}
