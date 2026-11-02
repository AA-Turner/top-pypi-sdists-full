"""Transport implementations for Cortex Code SDK."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any


class Transport(ABC):
    """Abstract transport for Cortex Code CLI communication.

    This is a low-level transport interface that handles raw I/O with the
    Cortex Code CLI process. Higher-level classes build on top of this to implement
    the control protocol and message routing.
    """

    @property
    def pid(self) -> int | None:
        """Process ID of the underlying CLI process, if available."""
        return None

    @abstractmethod
    async def connect(self) -> None:
        """Connect the transport and prepare for communication."""
        pass

    @abstractmethod
    async def write(self, data: str) -> None:
        """Write raw data to the transport.

        Args:
            data: Raw string data to write (typically JSON + newline)
        """
        pass

    @abstractmethod
    def read_messages(self) -> AsyncIterator[dict[str, Any]]:
        """Read and parse messages from the transport.

        Yields:
            Parsed JSON messages from the transport
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """Close the transport connection and clean up resources."""
        pass

    @abstractmethod
    def is_ready(self) -> bool:
        """Check if transport is ready for communication."""
        pass

    @abstractmethod
    async def end_input(self) -> None:
        """End the input stream (close stdin for process transports)."""
        pass


__all__ = ["Transport"]
