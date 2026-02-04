from abc import ABC, abstractmethod
from typing import List

from abstra_internals.repositories.code_markers.models import CodeMarker
from abstra_internals.repositories.code_markers.providers.base import CodeMarkerProvider
from abstra_internals.repositories.code_markers.providers.requirements import (
    RequirementsMarkerProvider,
)
from abstra_internals.repositories.code_markers.providers.syntax import (
    SyntaxMarkerProvider,
)


class CodeMarkersRepository(ABC):
    """
    Abstract base class for code markers repositories.

    Code markers provide inline editor feedback for issues like
    syntax errors, missing requirements, etc.
    """

    @abstractmethod
    def get_markers(self, code: str, file_type: str = "python") -> List[CodeMarker]:
        """
        Get all code markers for the given code.

        Args:
            code: The source code to analyze
            file_type: The type of file being analyzed (default: "python")

        Returns:
            List of CodeMarker objects from all applicable providers
        """
        pass


class LocalCodeMarkersRepository(CodeMarkersRepository):
    """
    Local implementation of the code markers repository.

    Aggregates markers from multiple providers (syntax, requirements, etc.)
    to provide comprehensive inline editor feedback.
    """

    def __init__(self):
        self._providers: List[CodeMarkerProvider] = [
            SyntaxMarkerProvider(),
            RequirementsMarkerProvider(),
        ]

    def get_markers(self, code: str, file_type: str = "python") -> List[CodeMarker]:
        """
        Get all code markers from applicable providers.

        Args:
            code: The source code to analyze
            file_type: The type of file being analyzed

        Returns:
            List of CodeMarker objects from all providers that support the file type
        """
        markers: List[CodeMarker] = []

        for provider in self._providers:
            if provider.supports_file_type(file_type):
                markers.extend(provider.get_markers(code))

        return markers

    def register_provider(self, provider: CodeMarkerProvider) -> None:
        """
        Register an additional provider.

        Args:
            provider: The provider to register
        """
        self._providers.append(provider)


class ProductionCodeMarkersRepository(CodeMarkersRepository):
    """
    Production implementation of the code markers repository.

    Code markers are not available in production as they are
    only used for editor feedback during development.
    """

    def get_markers(self, code: str, file_type: str = "python") -> List[CodeMarker]:
        raise NotImplementedError("Code markers are not available in production.")
