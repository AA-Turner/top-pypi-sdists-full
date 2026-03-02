"""Pydantic models for indexing API."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class IndexOptions(BaseModel):
    """Options for indexing operation."""

    incremental: bool = Field(
        default=False,
        description="Only index changed files"
    )
    changed_only: bool = Field(
        default=False,
        description="Detect and index only modified files"
    )
    skip_git: bool = Field(
        default=False,
        description="Skip git history analysis"
    )
    pr_limit: int = Field(
        default=100,
        description="Maximum PRs to fetch"
    )
    detect_communities: bool = Field(
        default=True,
        description="Run community detection"
    )
    skip_embeddings: bool = Field(
        default=False,
        description="Skip embedding generation"
    )


class IndexRequest(BaseModel):
    """Request to start indexing."""

    repo_path: str = Field(..., description="Path to repository")
    options: IndexOptions = Field(
        default_factory=IndexOptions,
        description="Indexing options"
    )


class IndexStats(BaseModel):
    """Statistics about indexed content."""

    files: int = Field(default=0, description="Number of files indexed")
    functions: int = Field(default=0, description="Number of functions")
    classes: int = Field(default=0, description="Number of classes")
    relationships: int = Field(default=0, description="Number of relationships")
    communities: int = Field(default=0, description="Number of communities detected")


class IndexStatus(BaseModel):
    """Status of indexing operation."""

    is_running: bool = Field(default=False, description="Whether indexing is in progress")
    last_indexed: Optional[datetime] = Field(
        default=None,
        description="Last successful index timestamp"
    )
    last_commit: Optional[str] = Field(
        default=None,
        description="Last indexed commit hash"
    )
    stats: IndexStats = Field(
        default_factory=IndexStats,
        description="Index statistics"
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message if failed"
    )
