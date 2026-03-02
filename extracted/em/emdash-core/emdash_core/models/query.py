"""Pydantic models for query API."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EntityType(str, Enum):
    """Types of code entities."""

    FILE = "File"
    CLASS = "Class"
    FUNCTION = "Function"
    METHOD = "Method"
    MODULE = "Module"


class SearchType(str, Enum):
    """Types of search operations."""

    SEMANTIC = "semantic"
    TEXT = "text"
    GREP = "grep"


class SearchFilters(BaseModel):
    """Filters for search results."""

    entity_types: list[EntityType] = Field(
        default_factory=list,
        description="Filter by entity types"
    )
    limit: int = Field(default=20, description="Maximum results to return")
    min_score: float = Field(default=0.0, description="Minimum similarity score")
    file_patterns: list[str] = Field(
        default_factory=list,
        description="Glob patterns to filter files"
    )


class SearchRequest(BaseModel):
    """Request for search endpoint."""

    query: str = Field(..., description="Search query")
    type: SearchType = Field(default=SearchType.SEMANTIC, description="Search type")
    filters: SearchFilters = Field(
        default_factory=SearchFilters,
        description="Search filters"
    )


class SearchResult(BaseModel):
    """A single search result."""

    qualified_name: str = Field(..., description="Fully qualified name")
    name: str = Field(..., description="Short name")
    type: EntityType = Field(..., description="Entity type")
    file_path: str = Field(..., description="File path relative to repo")
    line_number: Optional[int] = Field(default=None, description="Line number")
    score: float = Field(..., description="Relevance score (0-1)")
    snippet: Optional[str] = Field(default=None, description="Code snippet")


class SearchResponse(BaseModel):
    """Response from search endpoint."""

    results: list[SearchResult] = Field(default_factory=list)
    total: int = Field(..., description="Total number of matches")
    query: str = Field(..., description="Original query")


class ExpandRequest(BaseModel):
    """Request to expand a node."""

    node_type: EntityType = Field(..., description="Type of node to expand")
    identifier: str = Field(..., description="Qualified name or identifier")
    max_hops: int = Field(default=2, description="Maximum traversal depth")
    include_source: bool = Field(default=True, description="Include source code")


class CallersRequest(BaseModel):
    """Request to get callers of a function."""

    qualified_name: str = Field(..., description="Qualified name of function")
    max_depth: int = Field(default=1, description="Maximum call depth")


class CalleesRequest(BaseModel):
    """Request to get callees of a function."""

    qualified_name: str = Field(..., description="Qualified name of function")
    max_depth: int = Field(default=1, description="Maximum call depth")


class HierarchyRequest(BaseModel):
    """Request to get class hierarchy."""

    class_name: str = Field(..., description="Qualified name of class")
    direction: str = Field(
        default="both",
        description="Direction: 'up' (parents), 'down' (children), 'both'"
    )


class DependenciesRequest(BaseModel):
    """Request to get file dependencies."""

    file_path: str = Field(..., description="File path to analyze")
    direction: str = Field(
        default="both",
        description="Direction: 'imports', 'imported_by', 'both'"
    )
