"""
Kodexa Extraction Module - Data extraction engine.

This module contains classes for extracting structured data from documents:
- ExtractionEngine: Main extraction processor
- Taxonomy: Taxonomy definition loader
- DataObject: Extracted data container
- DataAttribute: Individual data attributes
- DataException: Extraction exceptions
- DocumentTaxonValidation: Validation results
"""

from .extraction import (
    ExtractionEngine,
    Taxonomy,
    DataObject,
    DataAttribute,
    DataException,
    DocumentTaxonValidation,
)

# Re-export ContentException for backward compatibility
from ..model.content_exception import ContentException

__all__ = [
    "ExtractionEngine",
    "Taxonomy",
    "DataObject",
    "DataAttribute",
    "DataException",
    "DocumentTaxonValidation",
    "ContentException",
]
