r"""Define a processor that applies a callable to its input."""

from __future__ import annotations

__all__ = ["LambdaProcessor"]

from typing import TYPE_CHECKING, Any, TypeVar

from coola.display import InlineDisplayMixin

from zenpyre.data_processors.base import BaseProcessor

if TYPE_CHECKING:
    from collections.abc import Callable

T = TypeVar("T")
U = TypeVar("U")


class LambdaProcessor(BaseProcessor[U, T], InlineDisplayMixin):
    """Processor that applies a callable to its input and returns the
    result.

    Unlike :class:`~zenpyre.data_processors.LambdaSequenceProcessor`,
    which applies ``fn`` to each item of a sequence independently, this
    class calls ``fn`` once on the whole input.  Useful for wrapping any
    single-value transformation in a pipeline without writing a
    dedicated processor class.

    Args:
        fn: A callable that takes the input of type ``U`` and returns a
            value of type ``T``.

    Example:
        ```pycon
        >>> from zenpyre.data_processors import LambdaProcessor
        >>> processor = LambdaProcessor(fn=len)
        >>> processor.process(["a", "b", "c"])
        3
        >>> processor = LambdaProcessor(fn=sorted)
        >>> processor.process([3, 1, 2])
        [1, 2, 3]

        ```
    """

    def __init__(self, fn: Callable[[U], T]) -> None:
        self._fn = fn

    def process(self, data: U) -> T:
        """Apply ``fn`` to ``data`` and return the result.

        Args:
            data: The input to process.

        Returns:
            The output of ``fn`` applied to ``data``.
        """
        return self._fn(data)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"fn": self._fn}
