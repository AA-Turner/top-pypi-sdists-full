r"""Provide a concrete default factory for LangChain Runnable models."""

from __future__ import annotations

__all__ = ["RunnableFactory"]

from typing import TYPE_CHECKING, Any, TypeVar

from coola.display import MultilineDisplayMixin

from zenpyre.runnables.factory.base import BaseRunnableFactory

if TYPE_CHECKING:
    from langchain_core.runnables import Runnable

Input = TypeVar("Input")
Output = TypeVar("Output")


class RunnableFactory(BaseRunnableFactory[Input, Output], MultilineDisplayMixin):
    """A concrete Runnable factory that wraps a pre-built
    :class:`~langchain_core.runnables.Runnable` instance.

    Use this when the runnable is already instantiated and you
    simply want to wrap it in the :class:`~BaseRunnableFactory`
    interface — for example, when injecting a fixed runnable into a
    component that expects a factory.

    Args:
        runnable: A fully configured
            :class:`~langchain_core.runnables.Runnable`
            instance to return from :meth:`make_runnable`.

    Example:
        ```pycon
        >>> from typing import Any
        >>> from langchain_core.runnables import Runnable
        >>> from zenpyre.runnables.factory import RunnableFactory
        >>> class MyRunnable(Runnable[Any, Any]):
        ...     def invoke(self, input: Any, config: Any = None, **kwargs: Any) -> Any:
        ...         return input
        ...
        >>> factory = RunnableFactory(MyRunnable())
        >>> runnable = factory.make_runnable()

        ```
    """

    def __init__(self, runnable: Runnable[Input, Output]) -> None:
        self._runnable = runnable

    def make_runnable(self) -> Runnable[Input, Output]:
        return self._runnable

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"runnable": self._runnable}
