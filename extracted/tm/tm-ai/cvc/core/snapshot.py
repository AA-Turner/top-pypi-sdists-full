from __future__ import annotations

import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field

class CVCSnapshot(BaseModel):
    """
    A lightweight representation of a CVC commit at a specific point in time.
    Used for UI summaries, fast-search indices, and external tool integrations.
    """
    
    # Pydantic v2 uses model_config instead of class Config
    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        extra='allow' # Allow extra fields for future-proofing
    )

    commit_hash: str = Field(..., description="Full SHA-256 hash of the cognitive commit.")
    short_hash: str = Field(..., description="Truncated 12-char hash for display.")
    branch: str = Field(default="main", description="Active branch when snapshot was taken.")
    timestamp: float = Field(default_factory=time.time, description="Unix timestamp (seconds).")
    message: str = Field(..., description="Commit message/summary.")
    
    # Metadata for filtering and categorisation
    author: str = Field(default="sofia", description="The agent or user who created the commit.")
    tags: List[str] = Field(default_factory=list, description="User-applied or auto-generated tags.")
    
    # Contextual overview (Tier 3/4 specific)
    summary_tokens: int = Field(default=0, description="Size of the distilled context summary.")
    is_anchor: bool = Field(default=False, description="Whether this is a full-state anchor.")
    
    # Arbitrary metadata for extensibility
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_json(self) -> str:
        """
        Serialize to JSON using Pydantic v2's model_dump_json.
        Note: Pydantic v1 used .json() - this is the v2 replacement.
        """
        return self.model_dump_json(indent=2)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary using Pydantic v2's model_dump.
        Note: Pydantic v1 used .dict() - this is the v2 replacement.
        """
        return self.model_dump()

    @classmethod
    def from_commit(cls, commit_hash: str, message: str, branch: str = "main") -> "CVCSnapshot":
        """Helper to create a snapshot from basic commit info."""
        return cls(
            commit_hash=commit_hash,
            short_hash=commit_hash[:12],
            branch=branch,
            message=message
        )
