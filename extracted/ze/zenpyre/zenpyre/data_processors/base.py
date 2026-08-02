r"""Define the abstract interface for data processors."""

from __future__ import annotations

__all__ = ["BaseProcessor"]

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class BaseProcessor(ABC, Generic[U, T]):
    """Abstract base class for data processors.

    A processor takes an input of type ``U`` and returns an output of
    type ``T``.  Unlike :class:`~zenpyre.ingestors.base.BaseIngestor`,
    which fetches data from a configured source, a processor always
    receives its input explicitly via :meth:`process`.  This makes
    processors composable — the output of one can be passed directly as
    the input of another.

    Type parameters:
        U: The input type accepted by :meth:`process`.
        T: The output type returned by :meth:`process`.

    Subclasses must implement :meth:`process`.

    Example:
        ```pycon
        >>> from zenpyre.data_processors import BaseProcessor
        >>> class UpperCaseProcessor(BaseProcessor[str, str]):
        ...     def process(self, data: str) -> str:
        ...         return data.upper()
        ...
        >>> UpperCaseProcessor().process("hello")
        'HELLO'

        ```
    """

    @abstractmethod
    def process(self, data: U) -> T:
        """Process the input data and return the result.

        Args:
            data: The input data to process.

        Returns:
            The processed output.  Its type and structure are defined
            by the concrete implementation.
        """
