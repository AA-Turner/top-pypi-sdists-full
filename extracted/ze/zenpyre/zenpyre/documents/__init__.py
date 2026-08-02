r"""Contain utilities for documents."""

from __future__ import annotations

__all__ = [
    "DocumentConsistencyError",
    "DocumentHasher",
    "assign_ids",
    "check_document_consistency",
    "copy_ids_to_metadata",
    "deduplicate_documents",
    "filter_by_metadata",
    "filter_by_metadata_range",
    "filter_by_metadata_values",
    "format_documents",
    "format_documents_as_json",
    "format_documents_as_markdown",
    "format_documents_as_xml",
    "get_document_id_lengths",
    "get_document_length",
    "get_document_lengths",
    "get_longest_document",
    "get_shortest_document",
    "hash_document",
    "hash_document_uuid",
    "hash_documents",
    "is_document_empty",
    "is_document_whitespace_only",
    "sort_by_metadata",
]

from zenpyre.documents.concatenation import (
    format_documents,
    format_documents_as_json,
    format_documents_as_markdown,
    format_documents_as_xml,
)
from zenpyre.documents.consistency import (
    DocumentConsistencyError,
    check_document_consistency,
)
from zenpyre.documents.dedup import deduplicate_documents
from zenpyre.documents.empty import is_document_empty, is_document_whitespace_only
from zenpyre.documents.filter import (
    filter_by_metadata,
    filter_by_metadata_range,
    filter_by_metadata_values,
)
from zenpyre.documents.hashing import (
    DocumentHasher,
    hash_document,
    hash_document_uuid,
    hash_documents,
)
from zenpyre.documents.id import assign_ids, copy_ids_to_metadata
from zenpyre.documents.length import (
    get_document_id_lengths,
    get_document_length,
    get_document_lengths,
    get_longest_document,
    get_shortest_document,
)
from zenpyre.documents.sort import sort_by_metadata
