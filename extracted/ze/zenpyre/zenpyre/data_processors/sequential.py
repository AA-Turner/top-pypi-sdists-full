r"""Define a processor that applies a sequence of processors
sequentially."""

from __future__ import annotations

__all__ = ["SequentialProcessor"]

import logging
from typing import Any

from coola.utils.format import repr_indent, repr_sequence, str_indent, str_sequence

from zenpyre.data_processors.base import BaseProcessor

logger: logging.Logger = logging.getLogger(__name__)


class SequentialProcessor(BaseProcessor[Any, Any]):
    """Processor that applies a sequence of processors one after
    another, passing the output of each as the input to the next.

    Mirrors the design of :class:`torch.nn.Sequential`: processors
    are composed in the order they are provided, and the final output
    is the result of the last processor.  If no processors are
    provided, :meth:`process` returns the input unchanged.

    Args:
        *processors: Zero or more :class:`~zenpyre.data_processors.base.BaseProcessor`
            instances to apply in order.

    Example:
        ```pycon
        >>> from zenpyre.data_processors import LambdaProcessor, SequentialProcessor
        >>> p = SequentialProcessor(
        ...     LambdaProcessor(fn=lambda x: x * 2),
        ...     LambdaProcessor(fn=str),
        ... )
        >>> p.process(21)
        '42'
        >>> SequentialProcessor().process(42)
        42

        ```
    """

    def __init__(self, *processors: BaseProcessor[Any, Any]) -> None:
        self._processors = list(processors)

    def __repr__(self) -> str:
        args = repr_indent(repr_sequence(self._processors))
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def __str__(self) -> str:
        args = str_indent(str_sequence(self._processors))
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def process(self, data: Any) -> Any:
        """Apply each processor in sequence and return the final result.

        Passes ``data`` to the first processor, then feeds each
        processor's output as the input of the next.

        Args:
            data: The initial input data passed to the first processor.

        Returns:
            The output of the last processor in the sequence.
        """
        result = data
        for processor in self._processors:
            result = processor.process(result)
        return result
