"""Abstract base class for context providers."""

from abc import ABC, abstractmethod
from typing import Optional

from ..models import ContextItem, ContextProviderSpec
from ...graph.connection import KuzuConnection


class ContextProvider(ABC):
    """Base class for context providers.

    Context providers extract relevant context from various sources
    (AST, git history, semantic search, etc.) to help the LLM
    understand the codebase during a session.
    """

    def __init__(self, connection: KuzuConnection, config: Optional[dict] = None):
        """Initialize context provider.

        Args:
            connection: Kuzu database connection
            config: Optional provider-specific configuration
        """
        self.connection = connection
        self.config = config or {}

    @property
    @abstractmethod
    def spec(self) -> ContextProviderSpec:
        """Get provider specification."""
        pass

    @property
    def name(self) -> str:
        """Get provider name."""
        return self.spec.name

    @abstractmethod
    def extract_context(self, modified_files: list[str]) -> list[ContextItem]:
        """Extract context items from modified files.

        Args:
            modified_files: List of file paths that were modified

        Returns:
            List of context items extracted from those files
        """
        pass

    def format_for_prompt(self, items: list[ContextItem]) -> str:
        """Format context items for LLM system prompt.

        Args:
            items: Context items to format

        Returns:
            Formatted string for inclusion in system prompt
        """
        if not items:
            return ""

        lines = [f"## Context from {self.name}\n"]
        for item in sorted(items, key=lambda x: -x.score):
            lines.append(f"### {item.entity_type}: {item.qualified_name}")
            if item.file_path:
                lines.append(f"File: {item.file_path}")
            if item.description:
                lines.append(f"Description: {item.description}")
            if item.neighbors:
                lines.append(f"Related: {', '.join(item.neighbors[:5])}")
            lines.append("")

        return "\n".join(lines)
