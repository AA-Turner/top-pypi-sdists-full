from abc import ABC, abstractmethod
from typing import List

from abstra_internals.repositories.code_markers.models import CodeMarker


class CodeMarkerProvider(ABC):
    """
    Abstract base class for code marker providers.

    Each provider is responsible for analyzing code and returning
    markers for a specific type of issue (syntax errors, missing
    requirements, etc.).
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the unique identifier for this provider."""
        pass

    @abstractmethod
    def get_markers(self, code: str) -> List[CodeMarker]:
        """
        Analyze the given code and return a list of markers.

        Args:
            code: The source code to analyze

        Returns:
            List of CodeMarker objects representing issues found
        """
        pass

    def supports_file_type(self, file_type: str) -> bool:
        """
        Check if this provider supports the given file type.

        Args:
            file_type: The file type to check (e.g., "python", "json")

        Returns:
            True if this provider can analyze the file type
        """
        return file_type == "python"
