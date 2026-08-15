# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "ProfileResponse",
    "Profile",
    "SearchResults",
    "SearchResultsResult",
    "SearchResultsResultChunk",
    "SearchResultsResultContext",
    "SearchResultsResultContextChild",
    "SearchResultsResultContextParent",
    "SearchResultsResultContextRelated",
    "SearchResultsResultDocument",
]


class Profile(BaseModel):
    buckets: Optional[Dict[str, List[str]]] = None
    """Per-bucket memory lists, keyed by bucket key"""

    dynamic: Optional[List[str]] = None
    """Dynamic profile information (recent memories)"""

    static: Optional[List[str]] = None
    """Static profile information that remains relevant long-term"""


class SearchResultsResultChunk(BaseModel):
    content: str
    """Content of the chunk"""

    document_id: str = FieldInfo(alias="documentId")
    """ID of the document this chunk belongs to"""

    position: float
    """Position of chunk in the document (0-indexed)"""


class SearchResultsResultContextChild(BaseModel):
    memory: str
    """The contextual memory content"""

    relation: Literal["updates", "extends", "derives"]
    """Relation type between this memory and its parent/child"""

    updated_at: str = FieldInfo(alias="updatedAt")
    """Contextual memory last update date"""

    metadata: Optional[Dict[str, object]] = None
    """Contextual memory metadata"""

    version: Optional[float] = None
    """
    Relative version distance from the primary memory (+1 for direct child, +2 for
    grand-child, etc.)
    """


class SearchResultsResultContextParent(BaseModel):
    memory: str
    """The contextual memory content"""

    relation: Literal["updates", "extends", "derives"]
    """Relation type between this memory and its parent/child"""

    updated_at: str = FieldInfo(alias="updatedAt")
    """Contextual memory last update date"""

    metadata: Optional[Dict[str, object]] = None
    """Contextual memory metadata"""

    version: Optional[float] = None
    """
    Relative version distance from the primary memory (-1 for direct parent, -2 for
    grand-parent, etc.)
    """


class SearchResultsResultContextRelated(BaseModel):
    memory: str
    """The related memory content"""

    relation: Literal["extends", "derives"]
    """Relation type"""

    updated_at: str = FieldInfo(alias="updatedAt")
    """Related memory last update date"""

    metadata: Optional[Dict[str, object]] = None
    """Related memory metadata"""


class SearchResultsResultContext(BaseModel):
    """
    Object containing version history (parents/children via updates) and related memories (extends/derives)
    """

    children: Optional[List[SearchResultsResultContextChild]] = None

    parents: Optional[List[SearchResultsResultContextParent]] = None

    related: Optional[List[SearchResultsResultContextRelated]] = None


class SearchResultsResultDocument(BaseModel):
    id: str
    """Document ID"""

    created_at: str = FieldInfo(alias="createdAt")
    """Document creation date"""

    updated_at: str = FieldInfo(alias="updatedAt")
    """Document last update date"""

    metadata: Optional[Dict[str, object]] = None
    """Document metadata (only included when documents=true)"""

    summary: Optional[str] = None
    """Document summary (only included when summaries=true)"""

    title: Optional[str] = None
    """Document title (only included when documents=true)"""

    type: Optional[str] = None
    """Document type (only included when documents=true)"""


class SearchResultsResult(BaseModel):
    id: str
    """Memory entry ID or chunk ID"""

    metadata: Optional[Dict[str, object]] = None
    """Memory metadata"""

    similarity: float
    """Similarity score between the query and memory entry"""

    updated_at: str = FieldInfo(alias="updatedAt")
    """Memory last update date"""

    chunk: Optional[str] = None
    """The chunk content (only present for chunk results from hybrid search)"""

    chunks: Optional[List[SearchResultsResultChunk]] = None
    """Relevant chunks from associated documents (only included when chunks=true)"""

    context: Optional[SearchResultsResultContext] = None
    """
    Object containing version history (parents/children via updates) and related
    memories (extends/derives)
    """

    documents: Optional[List[SearchResultsResultDocument]] = None
    """Associated documents for this memory entry"""

    filepath: Optional[str] = None
    """Filepath of the source document this memory or chunk came from"""

    is_aggregated: Optional[bool] = FieldInfo(alias="isAggregated", default=None)
    """Indicates if this memory was created by aggregating multiple source memories"""

    memory: Optional[str] = None
    """The memory content (only present for memory results)"""

    root_memory_id: Optional[str] = FieldInfo(alias="rootMemoryId", default=None)
    """ID of the root (first version) memory entry this one descends from.

    Null for memories that have never been superseded. Only present on memory
    results, not on standalone chunk results.
    """

    version: Optional[float] = None
    """Version number of this memory entry"""


class SearchResults(BaseModel):
    """Search results if a search query was provided"""

    results: List[SearchResultsResult]
    """Search results for the provided query"""

    timing: float
    """Search timing in milliseconds"""

    total: float
    """Total number of search results"""


class ProfileResponse(BaseModel):
    profile: Profile

    search_results: Optional[SearchResults] = FieldInfo(alias="searchResults", default=None)
    """Search results if a search query was provided"""
