r"""Contain corpus-wide, read-only inspection utilities: statistics,
duplicate/empty detection, and report printing.

Functions here consume an iterable of documents and never mutate or
return a new document list. For per-document predicates, see
``docculus.document``; for functions that produce a new document list
(dedup, filter, sort, format), see ``docculus.transform``.
"""

from __future__ import annotations

__all__ = [
    "ApproxContentStats",
    "ExactContentStats",
    "MetadataStats",
    "compute_content_stats_approx",
    "compute_content_stats_exact",
    "compute_metadata_stats",
    "find_duplicate_document_ids",
    "find_empty_document_ids",
    "find_empty_documents",
    "print_content_stats_report",
    "print_metadata_stats_report",
]

from docculus.analysis.content_approx import (
    ApproxContentStats,
    compute_content_stats_approx,
)
from docculus.analysis.content_exact import (
    ExactContentStats,
    compute_content_stats_exact,
)
from docculus.analysis.content_print import print_content_stats_report
from docculus.analysis.dedup import find_duplicate_document_ids
from docculus.analysis.empty import (
    find_empty_document_ids,
    find_empty_documents,
)
from docculus.analysis.metadata_print import print_metadata_stats_report
from docculus.analysis.metadata_stats import (
    MetadataStats,
    compute_metadata_stats,
)
