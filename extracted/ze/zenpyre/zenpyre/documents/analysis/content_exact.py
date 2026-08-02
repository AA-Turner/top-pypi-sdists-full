r"""Content exact document statistics."""

from __future__ import annotations

__all__ = ["ExactContentStats", "compute_content_stats_exact"]

import hashlib
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from zenpyre.documents.length import get_document_length

if TYPE_CHECKING:
    from collections.abc import Iterable

    from langchain_core.documents import Document


@dataclass
class ExactContentStats:
    """Streaming document health/analysis with EXACT duplicate detection
    and EXACT percentiles.

    Accumulates statistics one document at a time via ``update``, so it
    can be fed from a list, a generator, or any other iterable without
    requiring the full corpus to be held in memory at once. Call
    ``to_dict`` at the end to compute the final report.

    Memory:
      - O(n) ints for lengths (8 bytes each -> ~800MB for 100M docs)
      - O(unique docs) hashes for dedup (32 bytes each -> ~1.6GB for 50M
        unique docs)
    Both are much cheaper than storing the raw text itself, but this is
    NOT O(1) memory overall — use the approximate variant if the corpus
    is too large for this to fit.

    Attributes:
        count: Total number of documents processed.
        total_chars: Sum of ``page_content`` lengths across all
            documents processed.
        min_chars: Length, in characters, of the shortest
            ``page_content`` seen so far, or ``None`` if no documents
            have been processed yet.
        max_chars: Length, in characters, of the longest
            ``page_content`` seen so far, or ``None`` if no documents
            have been processed yet.
        min_doc_id: ``id`` of the document with the shortest
            ``page_content`` seen so far (first one seen, in case of a
            tie), or ``None`` if no documents have been processed yet.
        max_doc_id: ``id`` of the document with the longest
            ``page_content`` seen so far (first one seen, in case of a
            tie), or ``None`` if no documents have been processed yet.
        empty_count: Number of documents whose ``page_content`` is the
            empty string (or was coerced to it, e.g. ``None`` content).
        whitespace_only_count: Number of documents whose
            ``page_content`` is non-empty but contains only whitespace.
        none_or_non_str_content_count: Number of documents whose
            ``page_content`` was not a string (e.g. ``None`` or another
            type). Such content is treated as an empty string for all
            other statistics.
        none_id_count: Number of documents whose ``id`` is ``None``.
        missing_metadata_count: Number of documents whose ``metadata``
            is empty or falsy.
        duplicate_count: Number of documents whose exact
            ``page_content`` (by content hash) has already been seen
            earlier in the stream. The first occurrence of any given
            content is not counted as a duplicate.
    """

    count: int = 0
    total_chars: int = 0
    min_chars: int | None = None
    max_chars: int | None = None
    min_doc_id: Any | None = None
    max_doc_id: Any | None = None

    empty_count: int = 0
    whitespace_only_count: int = 0
    none_or_non_str_content_count: int = 0
    none_id_count: int = 0
    missing_metadata_count: int = 0
    duplicate_count: int = 0

    _seen_hashes: set[bytes] = field(default_factory=set)
    _lengths: list[int] = field(default_factory=list)

    def update(self, doc: Document) -> None:
        """Fold a single document into the running statistics.

        Updates all counters, the min/max character length (with the
        associated document id), the exact-duplicate hash set, and the
        stored list of lengths used later for percentile and standard
        deviation calculations.

        Args:
            doc: The document to process. Its ``id`` is assumed to
                always be present as an attribute (though its value may
                be ``None``). Its ``page_content`` is expected to be a
                string; non-string content (including ``None``) is
                counted via ``none_or_non_str_content_count`` and
                treated as an empty string for length, emptiness, and
                duplicate calculations. Its ``metadata`` is expected to
                be a mapping; a falsy/empty mapping is counted via
                ``missing_metadata_count``.
        """
        doc_id = doc.id  # always present per assumption, may be None
        if doc_id is None:
            self.none_id_count += 1

        content = doc.page_content
        if not isinstance(content, str):
            self.none_or_non_str_content_count += 1
            content = ""

        if content == "":
            self.empty_count += 1
        elif content.strip() == "":
            self.whitespace_only_count += 1

        if not doc.metadata:
            self.missing_metadata_count += 1

        content_hash = hashlib.sha256(content.encode("utf-8", errors="ignore")).digest()
        if content_hash in self._seen_hashes:
            self.duplicate_count += 1
        else:
            self._seen_hashes.add(content_hash)

        length = get_document_length(doc)
        self.count += 1
        self.total_chars += length
        self._lengths.append(length)

        if self.min_chars is None or length < self.min_chars:
            self.min_chars, self.min_doc_id = length, doc_id
        if self.max_chars is None or length > self.max_chars:
            self.max_chars, self.max_doc_id = length, doc_id

    def _percentile(self, sorted_lengths: list[int], p: float) -> float | None:
        """Compute an exact percentile from a pre-sorted list of
        lengths.

        Uses nearest-rank interpolation: the index into
        ``sorted_lengths`` is ``round(p / 100 * (n - 1))``.

        Args:
            sorted_lengths: Document content lengths, sorted in
                ascending order.
            p: Percentile to compute, in the range ``[0, 100]``.

        Returns:
            The length at the requested percentile, or ``None`` if
            ``sorted_lengths`` is empty.
        """
        if not sorted_lengths:
            return None
        k = round(p / 100 * (len(sorted_lengths) - 1))
        return sorted_lengths[k]

    def to_dict(self) -> dict[str, Any]:
        """Compute the final statistics report from the accumulated
        state.

        Derives the average, (population) standard deviation, and the
        50th/90th/99th percentiles of content length from the stored
        list of lengths. Safe to call multiple times and at any point
        during accumulation; it does not mutate any state and always
        reflects everything processed via ``update`` so far.

        Returns:
            A dict with the following keys:

            - ``count``: Total number of documents processed.
            - ``total_chars``: Sum of all ``page_content`` lengths.
            - ``avg_chars``: Mean ``page_content`` length, or ``0`` if
              no documents were processed.
            - ``std_dev_chars``: Population standard deviation of
              ``page_content`` length, or ``0`` if fewer than two
              documents were processed.
            - ``min_chars`` / ``max_chars``: Shortest/longest
              ``page_content`` length seen, or ``None`` if empty.
            - ``min_doc_id`` / ``max_doc_id``: ``id`` of the
              shortest/longest document seen, or ``None`` if empty.
            - ``p50_chars`` / ``p90_chars`` / ``p99_chars``: Exact
              50th/90th/99th percentile of ``page_content`` length, or
              ``None`` if empty.
            - ``empty_count``: Number of documents with empty content.
            - ``whitespace_only_count``: Number of documents with
              whitespace-only content.
            - ``none_or_non_str_content_count``: Number of documents
              whose content was not a string.
            - ``none_id_count``: Number of documents with a ``None``
              id.
            - ``missing_metadata_count``: Number of documents with
              empty/missing metadata.
            - ``duplicate_count``: Number of documents that exactly
              duplicate the content of an earlier document.
            - ``duplicate_count_exact``: Always ``True``; marks this
              report as using exact (not approximate) deduplication.
            - ``percentiles_exact``: Always ``True``; marks the
              percentiles above as exact (not sampled/approximate)
              values.
        """
        n = self.count
        avg = self.total_chars / n if n else 0

        if n > 1:
            variance = sum((length - avg) ** 2 for length in self._lengths) / n
            std_dev = variance**0.5
        else:
            std_dev = 0.0

        sorted_lengths = sorted(self._lengths)

        return {
            "count": n,
            "total_chars": self.total_chars,
            "avg_chars": avg,
            "std_dev_chars": std_dev,
            "min_chars": self.min_chars,
            "max_chars": self.max_chars,
            "min_doc_id": self.min_doc_id,
            "max_doc_id": self.max_doc_id,
            "p50_chars": self._percentile(sorted_lengths, 50),
            "p90_chars": self._percentile(sorted_lengths, 90),
            "p99_chars": self._percentile(sorted_lengths, 99),
            "empty_count": self.empty_count,
            "whitespace_only_count": self.whitespace_only_count,
            "none_or_non_str_content_count": self.none_or_non_str_content_count,
            "none_id_count": self.none_id_count,
            "missing_metadata_count": self.missing_metadata_count,
            "duplicate_count": self.duplicate_count,
            "duplicate_count_exact": True,
            "percentiles_exact": True,
        }


def compute_content_stats_exact(documents: Iterable[Document]) -> dict[str, Any]:
    """Compute exact content health/statistics over a stream of
    documents.

    Streaming health/stat check over a list, generator, or any iterable
    of Documents, with EXACT duplicate detection and EXACT percentiles.
    Documents are consumed one at a time, so this works with iterators
    or generators whose full contents cannot fit in memory — only the
    per-document lengths and content hashes are retained (see
    ``ExactDocContentStats`` for the memory profile).

    Args:
        documents: A list, generator, or other iterable of
            ``langchain_core.documents.Document`` objects. Consumed
            exactly once; if a generator/iterator is passed in, it will
            be exhausted by this call.

    Returns:
        A dict of statistics as described in
        ``ExactDocContentStats.to_dict``. For an empty input, returns a
        report with ``count`` of ``0`` and ``None``/``0`` values for
        the length-based fields.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents.analysis import compute_content_stats_exact
        >>> docs = [
        ...     Document(id="a", page_content="hello"),
        ...     Document(id="b", page_content="hello world"),
        ... ]
        >>> analysis = compute_content_stats_exact(docs)
        >>> analysis["count"]
        2

        ```

    See Also:
        ``compute_doc_stats_approx``: an approximate variant using a
        Bloom filter for duplicate detection and reservoir sampling for
        percentiles, with fixed (O(1)) memory usage, better suited to
        corpora too large for the exact hash set and length list to fit
        in memory.
    """
    stats = ExactContentStats()
    for doc in documents:
        stats.update(doc)
    return stats.to_dict()
