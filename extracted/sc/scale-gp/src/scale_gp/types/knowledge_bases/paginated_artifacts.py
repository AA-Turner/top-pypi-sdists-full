# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["PaginatedArtifacts", "Item", "ItemChunksStatus"]


class ItemChunksStatus(BaseModel):
    chunks_completed: int

    chunks_failed: int

    chunks_pending: int


class Item(BaseModel):
    artifact_id: str

    artifact_name: str

    artifact_uri: str

    chunks_status: ItemChunksStatus

    source: Literal[
        "S3",
        "SharePoint",
        "SharePointPage",
        "LocalFile",
        "LocalChunks",
        "GoogleDrive",
        "AzureBlobStorage",
        "GoogleCloudStorage",
        "Confluence",
        "Slack",
        "Snowflake",
        "Databricks",
        "SQLDatabase",
        "MongoDB",
    ]

    status: Literal["Pending", "Chunking", "Uploading", "Completed", "Failed", "Deleting", "Canceled", "Embedding"]

    artifact_uri_public: Optional[str] = None

    created_at: Optional[datetime] = None

    status_reason: Optional[str] = None

    tags: Optional[Dict[str, object]] = None

    updated_at: Optional[datetime] = None


class PaginatedArtifacts(BaseModel):
    current_page: int
    """The current page number."""

    items: List[Item]
    """The data returned for the current page."""

    items_per_page: int
    """The number of items per page."""

    total_item_count: int
    """The total number of items of the query"""
