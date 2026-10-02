r"""Contain per-document utilities.

Functions here operate on a single ``Document`` at a time. For utilities
that operate on a corpus (an iterable of documents), see
``docculus.analysis``.
"""

from __future__ import annotations

__all__ = [
    "generate_deterministic_id",
    "generate_id",
    "generate_random_id",
    "get_length",
    "get_lengths",
    "get_lengths_with_ids",
    "get_longest_document",
    "get_shortest_document",
    "is_empty",
    "is_whitespace_only",
]

from docculus.document.empty import is_empty, is_whitespace_only
from docculus.document.id import (
    generate_deterministic_id,
    generate_id,
    generate_random_id,
)
from docculus.document.length import (
    get_length,
    get_lengths,
    get_lengths_with_ids,
    get_longest_document,
    get_shortest_document,
)
