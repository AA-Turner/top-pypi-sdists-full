# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["ClientAddParams"]


class ClientAddParams(TypedDict, total=False):
    content: Required[str]
    """The content to extract and process into a document.

    This can be a URL to a website, a PDF, an image, or a video.
    """

    container_tag: Annotated[str, PropertyInfo(alias="containerTag")]
    """Optional tag this document should be containerized by.

    Max 100 characters, alphanumeric with hyphens, underscores, and dots only.
    """

    container_tags: Annotated[SequenceNotStr[str], PropertyInfo(alias="containerTags")]

    custom_id: Annotated[str, PropertyInfo(alias="customId")]
    """Optional custom ID of the document.

    Max 100 characters, alphanumeric with hyphens, underscores, and dots only.
    """

    document_date: Annotated[str, PropertyInfo(alias="documentDate")]
    """When this document's content is from, as opposed to when it was uploaded.

    Accepts YYYY-MM-DD or a full ISO 8601 timestamp. Memory extraction resolves
    relative dates against this instead of the ingestion time, and documents in a
    batch are processed oldest-first so newer facts correctly supersede older ones.
    Set this whenever you backfill historical content.
    """

    dreaming: Literal["instant", "dynamic"]
    """Processing mode.

    "dynamic" (default) groups related documents together so memories form from
    coherent, logical units rather than one isolated entry at a time. "instant"
    processes each document on its own right away, and bills one extra operation per
    document.
    """

    entity_context: Annotated[str, PropertyInfo(alias="entityContext")]
    """Optional entity context for this container tag.

    Max 1500 characters. Used during document processing to guide memory extraction.
    """

    filepath: str
    """Optional file path for the document.

    Used by supermemoryfs to store the full path of the file.
    """

    filter_by_metadata: Annotated[
        Dict[str, Union[str, float, bool, SequenceNotStr[str]]], PropertyInfo(alias="filterByMetadata")
    ]
    """
    Optional metadata filter to apply when pulling related memories and profile
    during ingestion. Only memories matching these filters will be used as context.
    """

    metadata: Dict[str, Union[str, float, bool, SequenceNotStr[str]]]
    """Optional metadata for the document."""

    task_type: Annotated[Literal["memory", "superrag"], PropertyInfo(alias="taskType")]
    """
    Task type: "memory" (default) for full context layer with SuperRAG built in,
    "superrag" for managed RAG as a service.
    """
