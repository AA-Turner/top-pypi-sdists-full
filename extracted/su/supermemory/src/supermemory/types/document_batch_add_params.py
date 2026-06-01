# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["DocumentBatchAddParams", "DocumentsUnionMember0"]


class DocumentBatchAddParams(TypedDict, total=False):
    documents: Required[Union[Iterable[DocumentsUnionMember0], SequenceNotStr[str]]]

    container_tag: Annotated[str, PropertyInfo(alias="containerTag")]
    """Optional tag this document should be containerized by.

    This can be an ID for your user, a project ID, or any other identifier you wish
    to use to group documents.
    """

    container_tags: Annotated[SequenceNotStr[str], PropertyInfo(alias="containerTags")]
    """
    (DEPRECATED: Use containerTag instead) Optional tags this document should be
    containerized by. This can be an ID for your user, a project ID, or any other
    identifier you wish to use to group documents.
    """

    content: None

    entity_context: Annotated[str, PropertyInfo(alias="entityContext")]
    """Optional entity context for this container tag.

    Max 1500 characters. Used during document processing to guide memory extraction.
    """

    filepath: str
    """Optional file path for the document (e.g., '/documents/reports/file.pdf').

    Used by supermemoryfs to map documents to filesystem paths.
    """

    filter_by_metadata: Annotated[
        Dict[str, Union[str, float, bool, SequenceNotStr[str]]], PropertyInfo(alias="filterByMetadata")
    ]
    """
    Optional metadata filter scoping which existing memories are pulled as context
    during ingestion. Scalar values match exactly (AND across keys); array values
    match ANY (OR within key). Only memories whose source documents match this
    filter are used as context.
    """

    metadata: Dict[str, Union[str, float, bool, SequenceNotStr[str]]]
    """Optional metadata for the document.

    This is used to store additional information about the document. You can use
    this to store any additional information you need about the document. Metadata
    can be filtered through. Keys must be strings and are case sensitive. Values can
    be strings, numbers, or booleans. You cannot nest objects.
    """

    task_type: Annotated[Literal["memory", "superrag"], PropertyInfo(alias="taskType")]
    """
    Task type: "memory" (default) for full context layer with SuperRAG built in,
    "superrag" for managed RAG as a service.
    """


class DocumentsUnionMember0(TypedDict, total=False):
    content: Required[str]
    """The content to extract and process into a document.

    This can be a URL to a website, a PDF, an image, or a video.

    Plaintext: Any plaintext format

    URL: A URL to a website, PDF, image, or video

    We automatically detect the content type from the url's response format.
    """

    container_tag: Annotated[str, PropertyInfo(alias="containerTag")]
    """Optional tag this document should be containerized by.

    This can be an ID for your user, a project ID, or any other identifier you wish
    to use to group documents.
    """

    container_tags: Annotated[SequenceNotStr[str], PropertyInfo(alias="containerTags")]
    """
    (DEPRECATED: Use containerTag instead) Optional tags this document should be
    containerized by. This can be an ID for your user, a project ID, or any other
    identifier you wish to use to group documents.
    """

    custom_id: Annotated[str, PropertyInfo(alias="customId")]
    """Optional custom ID of the document.

    This could be an ID from your database that will uniquely identify this
    document.
    """

    entity_context: Annotated[str, PropertyInfo(alias="entityContext")]
    """Optional entity context for this container tag.

    Max 1500 characters. Used during document processing to guide memory extraction.
    """

    filepath: str
    """Optional file path for the document (e.g., '/documents/reports/file.pdf').

    Used by supermemoryfs to map documents to filesystem paths.
    """

    filter_by_metadata: Annotated[
        Dict[str, Union[str, float, bool, SequenceNotStr[str]]], PropertyInfo(alias="filterByMetadata")
    ]
    """
    Optional metadata filter scoping which existing memories are pulled as context
    during ingestion. Scalar values match exactly (AND across keys); array values
    match ANY (OR within key). Only memories whose source documents match this
    filter are used as context.
    """

    metadata: Dict[str, Union[str, float, bool, SequenceNotStr[str]]]
    """Optional metadata for the document.

    This is used to store additional information about the document. You can use
    this to store any additional information you need about the document. Metadata
    can be filtered through. Keys must be strings and are case sensitive. Values can
    be strings, numbers, or booleans. You cannot nest objects.
    """

    task_type: Annotated[Literal["memory", "superrag"], PropertyInfo(alias="taskType")]
    """
    Task type: "memory" (default) for full context layer with SuperRAG built in,
    "superrag" for managed RAG as a service.
    """
