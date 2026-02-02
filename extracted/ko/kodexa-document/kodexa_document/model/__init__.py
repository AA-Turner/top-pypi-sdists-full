"""
Kodexa Document Model - Core document classes.

This module contains the core document model classes:
- Document: Main document container
- ContentNode: Tree nodes in the document
- ContentFeature: Features attached to nodes
- Tag: Tagged content
- TagInstance: Groups of nodes by tag UUID
- ContentException: Document-level exceptions
- DocumentMetadata: Auto-syncing metadata
- SourceMetadata: Document source information
- FindDirection, Traverse: Navigation enums
- Ref: Reference parsing for Kodexa objects
- Platform objects: ExecutionEvent, ContentObject, etc.
"""

from .document import Document
from .content_node import ContentNode
from .content_feature import ContentFeature
from .tag import Tag
from .tag_instance import TagInstance
from .content_exception import ContentException
from .document_metadata import DocumentMetadata
from .source_metadata import SourceMetadata
from .enums import FindDirection, Traverse
from .ref import Ref
from .processing import ProcessingStep

# Platform/API Pydantic models
from .objects import (
    ExecutionEvent,
    ContentObject,
    AssistantExecutionResponse,
    AssistantResponsePipeline,
    Status,
    ModelUsage,
    Pipeline,
    ExceptionDetails,
    Taxonomy,
    Taxon,
    Store,
    DocumentFamily,
    ContentEvent,
    AssistantEvent,
    ScheduledEvent,
    ChannelEvent,
    DocumentFamilyEvent,
    DataObjectEvent,
    WorkspaceEvent,
    TaskEvent,
    BaseEvent,
    ModelInteraction,
)

__all__ = [
    "Document",
    "ContentNode",
    "ContentFeature",
    "Tag",
    "TagInstance",
    "ContentException",
    "DocumentMetadata",
    "SourceMetadata",
    "FindDirection",
    "Traverse",
    "Ref",
    "ProcessingStep",
    # Platform objects
    "ExecutionEvent",
    "ContentObject",
    "AssistantExecutionResponse",
    "AssistantResponsePipeline",
    "Status",
    "ModelUsage",
    "Pipeline",
    "ExceptionDetails",
    "Taxonomy",
    "Taxon",
    "Store",
    "DocumentFamily",
    "ContentEvent",
    "AssistantEvent",
    "ScheduledEvent",
    "ChannelEvent",
    "DocumentFamilyEvent",
    "DataObjectEvent",
    "WorkspaceEvent",
    "TaskEvent",
    "BaseEvent",
    "ModelInteraction",
]
