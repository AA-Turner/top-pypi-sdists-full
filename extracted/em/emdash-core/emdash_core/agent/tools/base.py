"""Base classes for agent tools."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class ToolCategory(Enum):
    """Categories of agent tools."""

    SEARCH = "search"
    TRAVERSAL = "traversal"
    ANALYTICS = "analytics"
    HISTORY = "history"
    PLANNING = "planning"
    LEARNING = "learning"
    FILE = "file"
    CODE = "code"
    COMMUNICATION = "communication"
    PROJECT = "project"
    OTHER = "other"


@dataclass
class ToolResult:
    """Standardized result from any tool execution."""

    success: bool
    data: dict = field(default_factory=dict)
    error: Optional[str] = None
    suggestions: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "suggestions": self.suggestions,
            "metadata": self.metadata,
        }

    @classmethod
    def success_result(
        cls,
        data: dict,
        suggestions: list[str] = None,
        metadata: dict = None,
    ) -> "ToolResult":
        """Create a successful result."""
        return cls(
            success=True,
            data=data,
            suggestions=suggestions or [],
            metadata=metadata or {},
        )

    @classmethod
    def error_result(
        cls,
        error: str,
        suggestions: list[str] = None,
    ) -> "ToolResult":
        """Create an error result."""
        return cls(
            success=False,
            error=error,
            suggestions=suggestions or [],
        )


class BaseTool(ABC):
    """Abstract base class for all agent tools."""

    name: str = ""
    description: str = ""
    category: ToolCategory = ToolCategory.SEARCH

    def __init__(self, connection=None):
        """Initialize the tool.

        Args:
            connection: Kuzu connection. If None, uses global read-only connection.
                       Pass False to explicitly skip database connection.
        """
        if connection is False:
            # Explicitly skip database connection
            self.connection = None
        elif connection is None:
            # Try to get database connection, but don't fail if unavailable
            try:
                from ...graph.connection import get_read_connection
                self.connection = get_read_connection()
            except Exception:
                self.connection = None
        else:
            self.connection = connection

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """Execute the tool with given parameters.

        Args:
            **kwargs: Tool-specific parameters

        Returns:
            ToolResult with success/data or error
        """
        pass

    @abstractmethod
    def get_schema(self) -> dict:
        """Return OpenAI function calling schema.

        Returns:
            Dict with name, description, and parameters following OpenAI format
        """
        pass

    def _make_schema(
        self,
        properties: dict,
        required: list[str] = None,
    ) -> dict:
        """Helper to construct OpenAI function schema.

        Args:
            properties: Parameter properties dict
            required: List of required parameter names

        Returns:
            Complete OpenAI function schema with type wrapper
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required or [],
                },
            },
        }
