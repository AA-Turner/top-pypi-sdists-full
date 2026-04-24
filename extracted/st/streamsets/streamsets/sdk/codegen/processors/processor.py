#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2025
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class Code:
    """Utility class to hold generate script of recreating pipeline."""

    def __init__(self, content: str) -> None:
        """The __init__ of the Code class.

        Args:
            content: Generated script as string.
        """
        self._content = content

    def __str__(self) -> str:
        """String representation of containing script."""
        return self._content

    def save(self, path: "Path") -> "Path":
        """Save script content to given path.

        Args:
            path: Location where to save containing script.

        Return:
            Path where generate script was saved.
        """
        with open(path, "w") as f:
            f.write(self._content)

        return path


class Processor(ABC):

    @abstractmethod
    def run(self) -> Code:
        """Here we should return processor output string wrapped with Code object."""
