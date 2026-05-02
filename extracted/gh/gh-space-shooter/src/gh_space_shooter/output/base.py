"""Base class for output format providers."""

from abc import ABC, abstractmethod
from typing import Iterator
from PIL import Image


class OutputProvider(ABC):
    """Abstract base class for output format providers."""

    def __init__(self, path: str):
        """
        Initialize the provider with an output file path.

        Args:
            path: Path to the output file
        """
        self.path = path

    @abstractmethod
    def encode(self, frames: Iterator[Image.Image], frame_duration: int) -> bytes:
        """
        Encode frames into the output format.

        Args:
            frames: Iterator of PIL Images

        Returns:
            Encoded output as bytes
        """
        pass

    @abstractmethod
    def write(self, data: bytes) -> None:
        """
        Write encoded data to a file.

        Args:
            data: Encoded data to write
        """
        pass
