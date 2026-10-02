r"""Provide the base factory interface for creating LangChain Runnable
models."""

from __future__ import annotations

__all__ = ["BaseRunnableFactory"]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from langchain_core.runnables import Runnable


Input = TypeVar("Input")
Output = TypeVar("Output")


class BaseRunnableFactory(ABC, Generic[Input, Output]):
    """Abstract base class for Runnable factories.

    Subclasses implement :meth:`make_runnable` to instantiate and
    return a configured
    :class:`~langchain_core.runnables.Runnable` object.  This
    pattern decouples ``Runnable`` creation from the rest of the
    codebase, making it easy to swap implementations without
    changing call sites.

    Example:
        ```pycon
        >>> from typing import Any
        >>> from langchain_core.runnables import Runnable
        >>> from zenpyre.runnables.factory import BaseRunnableFactory
        >>> class MyRunnableFactory(BaseRunnableFactory):
        ...     def make_runnable(self) -> Runnable[Any, Any]:
        ...         class MyRunnable(Runnable[Any, Any]):
        ...             def invoke(self, input: Any, config: Any = None, **kwargs: Any) -> Any:
        ...                 return input
        ...         return MyRunnable()
        ...
        >>> factory = MyRunnableFactory()
        >>> runnable = factory.make_runnable()

        ```
    """

    @abstractmethod
    def make_runnable(self) -> Runnable[Input, Output]:
        """Create and return a configured Runnable instance.

        Returns:
            A :class:`~langchain_core.runnables.Runnable`
            instance ready for use.
        """
