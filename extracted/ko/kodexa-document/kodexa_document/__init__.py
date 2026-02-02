"""
Kodexa Document Go Python Bindings

Python bindings for the Go-based Kodexa Document SDK using CFFI.
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("kodexa-document")
except PackageNotFoundError:
    __version__ = "0.0.0"  # Fallback for development installs

__author__ = "Kodexa"

# Model classes
from .model import (
    Document,
    ContentNode,
    ContentFeature,
    Tag,
    TagInstance,
    DocumentMetadata,
    SourceMetadata,
    ContentException,
    FindDirection,
    Traverse,
)
from .model.objects import DocumentKnowledgeFeature

# Extraction classes
from .extraction import (
    ExtractionEngine,
    Taxonomy,
    DataObject,
    DataAttribute,
    DataException,
    DocumentTaxonValidation,
)

# Processing classes
from .processing import ProcessingStep

# Error classes
from .errors import (
    DocumentError,
    DocumentNotFoundError,
    InvalidDocumentError,
    ExtractionError,
    MemoryError,
)

# Accessor classes
from .accessors import (
    DataAttributeAccessor,
    DataAttributeInput,
    DataObjectAccessor,
    DataObjectInput,
    AuditAccessor,
    NativeDocumentAccessor,
    NativeDocumentInput,
    NoteAccessor,
    NoteInput,
    NoteType,
)

# Utility functions (commonly used for compatibility)
from .utils import get_source

# Platform, Assistant, Steps, Spatial, and Utils classes are imported lazily
# to avoid requiring their dependencies at package import time.
# Import them explicitly when needed:
#   from kodexa_document.platform import KodexaClient, KodexaPlatform
#   from kodexa_document.assistant import Assistant, AssistantContext
#   from kodexa_document.steps import NodeTagger, RollupTransformer
#   from kodexa_document.spatial import overlaps_with
#   from kodexa_document.utils import safe_name

__all__ = [
    # Model
    "Document",
    "ContentNode",
    "ContentFeature",
    "Tag",
    "TagInstance",
    "DocumentMetadata",
    "SourceMetadata",
    "ContentException",
    "FindDirection",
    "Traverse",
    "DocumentKnowledgeFeature",
    # Extraction
    "ExtractionEngine",
    "Taxonomy",
    "DataObject",
    "DataAttribute",
    "DataException",
    "DocumentTaxonValidation",
    # Processing
    "ProcessingStep",
    # Errors
    "DocumentError",
    "DocumentNotFoundError",
    "InvalidDocumentError",
    "ExtractionError",
    "MemoryError",
    # Accessors
    "DataAttributeAccessor",
    "DataAttributeInput",
    "DataObjectAccessor",
    "DataObjectInput",
    "AuditAccessor",
    "NativeDocumentAccessor",
    "NativeDocumentInput",
    "NoteAccessor",
    "NoteInput",
    "NoteType",
    # Utility functions
    "get_source",
]
