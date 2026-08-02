r"""Content approximate document statistics."""

from __future__ import annotations

__all__ = ["ApproxContentStats", "compute_content_stats_approx"]

import hashlib
import random
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from zenpyre.documents.length import get_document_length
from zenpyre.utils.bloom_filter import BloomFilter

if TYPE_CHECKING:
    from collections.abc import Iterable

    from langchain_core.documents import Document


@dataclass
class ApproxContentStats:
    """Streaming document health/analysis with APPROXIMATE duplicate
    detection and APPROXIMATE percentiles.

    Accumulates statistics one document at a time via ``update``, so it
    can be fed from a list, a generator, or any other iterable without
    requiring the full corpus to be held in memory at once. Call
    ``to_dict`` at the end to compute the final report.

    Unlike ``ExactDocContentStats``, memory usage here is fixed (O(1)
    per document, i.e. does not grow with the number of documents
    processed): duplicate detection uses a ``BloomFilter`` sized up
    front from an expected document count, and percentiles are
    estimated from a fixed-size reservoir sample of lengths rather than
    the full list. This trades a small, bounded amount of accuracy for
    a memory profile suitable for corpora too large to fit exact
    per-document data (hashes, lengths) in memory.

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
        approx_duplicate_count: Approximate number of documents whose
            exact ``page_content`` has already been seen earlier in the
            stream, as reported by the Bloom filter. Never
            undercounts by much; may slightly overcount due to the
            filter's false-positive rate.
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
    approx_duplicate_count: int = 0

    expected_doc_count: int = 1_000_000
    fp_rate: float = 0.01
    reservoir_size: int = 10_000

    _bloom: BloomFilter | None = field(default=None, repr=False)
    _reservoir: list[int] = field(default_factory=list, repr=False)
    _seen_for_reservoir: int = field(default=0, repr=False)

    def __post_init__(self) -> None:
        """Lazily construct the Bloom filter from the configured
        ``expected_doc_count`` and ``fp_rate`` if one wasn't
        supplied."""
        if self._bloom is None:
            self._bloom = BloomFilter(expected_items=self.expected_doc_count, fp_rate=self.fp_rate)

    def update(self, doc: Document) -> None:
        """Fold a single document into the running statistics.

        Updates all counters, the min/max character length (with the
        associated document id), the Bloom filter used for approximate
        duplicate detection, and the reservoir sample of lengths used
        later for approximate percentile and standard deviation
        calculations.

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
        assert self._bloom is not None  # noqa: S101 (set in __post_init__)
        if self._bloom.add_and_check(content_hash):
            self.approx_duplicate_count += 1

        length = get_document_length(doc)
        self.count += 1
        self.total_chars += length

        if self.min_chars is None or length < self.min_chars:
            self.min_chars, self.min_doc_id = length, doc_id
        if self.max_chars is None or length > self.max_chars:
            self.max_chars, self.max_doc_id = length, doc_id

        # Reservoir sampling (Algorithm R): keeps a uniform random sample
        # of up to `reservoir_size` lengths seen so far, in O(1) memory
        # relative to the total number of documents processed.
        self._seen_for_reservoir += 1
        if len(self._reservoir) < self.reservoir_size:
            self._reservoir.append(length)
        else:
            j = random.randint(0, self._seen_for_reservoir - 1)  # noqa: S311
            if j < self.reservoir_size:
                self._reservoir[j] = length

    def _percentile(self, sorted_lengths: list[int], p: float) -> float | None:
        """Estimate a percentile from a pre-sorted sample of lengths.

        Uses nearest-rank interpolation over the reservoir sample: the
        index into ``sorted_lengths`` is ``round(p / 100 * (n - 1))``.
        Since the sample is a uniform random subset of all lengths
        seen, this is an unbiased estimate of the true percentile, with
        accuracy improving as ``reservoir_size`` grows relative to
        ``count``.

        Args:
            sorted_lengths: A sample of document content lengths,
                sorted in ascending order.
            p: Percentile to compute, in the range ``[0, 100]``.

        Returns:
            The estimated length at the requested percentile, or
            ``None`` if ``sorted_lengths`` is empty.
        """
        if not sorted_lengths:
            return None
        k = round(p / 100 * (len(sorted_lengths) - 1))
        return sorted_lengths[k]

    def to_dict(self) -> dict[str, Any]:
        """Compute the final statistics report from the accumulated
        state.

        Derives the average from the exact running total, and the
        (population) standard deviation and 50th/90th/99th percentiles
        of content length from the reservoir sample of lengths. Safe to
        call multiple times and at any point during accumulation; it
        does not mutate any state and always reflects everything
        processed via ``update`` so far.

        Returns:
            A dict with the following keys:

            - ``count``: Total number of documents processed (exact).
            - ``total_chars``: Sum of all ``page_content`` lengths
              (exact).
            - ``avg_chars``: Mean ``page_content`` length (exact), or
              ``0`` if no documents were processed.
            - ``std_dev_chars``: Standard deviation of ``page_content``
              length, estimated from the reservoir sample; ``0`` if
              fewer than two documents were processed.
            - ``min_chars`` / ``max_chars``: Shortest/longest
              ``page_content`` length seen (exact), or ``None`` if
              empty.
            - ``min_doc_id`` / ``max_doc_id``: ``id`` of the
              shortest/longest document seen (exact), or ``None`` if
              empty.
            - ``p50_chars_approx`` / ``p90_chars_approx`` /
              ``p99_chars_approx``: Estimated 50th/90th/99th percentile
              of ``page_content`` length, or ``None`` if empty.
            - ``empty_count``: Number of documents with empty content
              (exact).
            - ``whitespace_only_count``: Number of documents with
              whitespace-only content (exact).
            - ``none_or_non_str_content_count``: Number of documents
              whose content was not a string (exact).
            - ``none_id_count``: Number of documents with a ``None``
              id (exact).
            - ``missing_metadata_count``: Number of documents with
              empty/missing metadata (exact).
            - ``approx_duplicate_count``: Approximate number of
              documents that duplicate the content of an earlier
              document, as reported by the Bloom filter.
            - ``duplicate_count_exact``: Always ``False``; marks this
              report as using approximate (not exact) deduplication.
            - ``percentiles_exact``: Always ``False``; marks the
              percentiles above as estimated (not exact) values.
            - ``bloom_filter_fp_rate``: The configured target
              false-positive rate of the Bloom filter used for
              duplicate detection, for reference when interpreting
              ``approx_duplicate_count``.
            - ``reservoir_sample_size``: The number of lengths actually
              held in the reservoir sample used for the standard
              deviation and percentile estimates (``min(count,
              reservoir_size)``).
        """
        n = self.count
        avg = self.total_chars / n if n else 0

        sample = self._reservoir
        if len(sample) > 1:
            sample_mean = sum(sample) / len(sample)
            variance = sum((length - sample_mean) ** 2 for length in sample) / len(sample)
            std_dev = variance**0.5
        else:
            std_dev = 0.0

        sorted_sample = sorted(sample)

        return {
            "count": n,
            "total_chars": self.total_chars,
            "avg_chars": avg,
            "std_dev_chars": std_dev,
            "min_chars": self.min_chars,
            "max_chars": self.max_chars,
            "min_doc_id": self.min_doc_id,
            "max_doc_id": self.max_doc_id,
            "p50_chars_approx": self._percentile(sorted_sample, 50),
            "p90_chars_approx": self._percentile(sorted_sample, 90),
            "p99_chars_approx": self._percentile(sorted_sample, 99),
            "empty_count": self.empty_count,
            "whitespace_only_count": self.whitespace_only_count,
            "none_or_non_str_content_count": self.none_or_non_str_content_count,
            "none_id_count": self.none_id_count,
            "missing_metadata_count": self.missing_metadata_count,
            "approx_duplicate_count": self.approx_duplicate_count,
            "duplicate_count_exact": False,
            "percentiles_exact": False,
            "bloom_filter_fp_rate": self.fp_rate,
            "reservoir_sample_size": len(sample),
        }


def compute_content_stats_approx(
    documents: Iterable[Document],
    *,
    expected_doc_count: int = 1_000_000,
    fp_rate: float = 0.01,
    reservoir_size: int = 10_000,
) -> dict[str, Any]:
    """Compute approximate content health/statistics over a stream of
    documents, using fixed (O(1)) memory regardless of corpus size.

    Streaming health/stat check over a list, generator, or any iterable
    of Documents, with APPROXIMATE duplicate detection (via a Bloom
    filter) and APPROXIMATE percentiles (via reservoir sampling).
    Documents are consumed one at a time, so this works with iterators
    or generators whose full contents cannot fit in memory. Unlike
    ``compute_doc_content_stats_exact``, memory usage here does not
    grow with the number of documents processed, only with the
    configured ``expected_doc_count``, ``fp_rate``, and
    ``reservoir_size`` — making this the appropriate choice for corpora
    too large for exact per-document hashes/lengths to fit in memory.

    Args:
        documents: A list, generator, or other iterable of
            ``langchain_core.documents.Document`` objects. Consumed
            exactly once; if a generator/iterator is passed in, it will
            be exhausted by this call.
        expected_doc_count: Rough estimate of the total number of
            documents (or, more precisely, unique documents) that will
            be processed. Used to size the Bloom filter for the
            requested ``fp_rate``. Safe to overestimate; underestimating
            causes the effective false-positive rate to rise above
            ``fp_rate`` as more documents are processed than planned
            for.
        fp_rate: Target false-positive probability for duplicate
            detection, once approximately ``expected_doc_count``
            unique documents have been added. The Bloom filter never
            produces false negatives, so ``approx_duplicate_count``
            never undercounts true duplicates by more than this rate
            would suggest, though it may overcount slightly.
        reservoir_size: Number of lengths to retain in the reservoir
            sample used to estimate the standard deviation and
            percentiles. Larger values improve estimate accuracy at
            the cost of more memory; the memory cost is still fixed
            (independent of the number of documents processed).

    Returns:
        A dict of statistics as described in
        ``ApproxDocContentStats.to_dict``. For an empty input, returns
        a report with ``count`` of ``0`` and ``None``/``0`` values for
        the length-based fields.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents.analysis import compute_content_stats_approx
        >>> docs = [
        ...     Document(id="a", page_content="hello"),
        ...     Document(id="b", page_content="hello world"),
        ... ]
        >>> analysis = compute_content_stats_approx(docs, expected_doc_count=1000)
        >>> analysis["count"]
        2

        ```

    See Also:
        ``compute_doc_content_stats_exact``: an exact variant using a
        hash set for duplicate detection and a full sorted list of
        lengths for percentiles, with memory usage that grows with
        corpus size but produces exact (non-approximate) results.
    """
    stats = ApproxContentStats(
        expected_doc_count=expected_doc_count,
        fp_rate=fp_rate,
        reservoir_size=reservoir_size,
    )
    for doc in documents:
        stats.update(doc)
    return stats.to_dict()
