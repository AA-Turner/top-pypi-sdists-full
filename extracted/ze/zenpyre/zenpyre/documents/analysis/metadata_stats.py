r"""Document metadata statistics."""

from __future__ import annotations

__all__ = ["MetadataStats", "compute_metadata_stats"]

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterable

    from langchain_core.documents import Document


@dataclass
class MetadataStats:
    """Streaming document metadata health/analysis.

    Accumulates statistics one document at a time via ``update``, so it
    can be fed from a list, a generator, or any other iterable without
    requiring the full corpus to be held in memory at once. Call
    ``to_dict`` at the end to compute the final report.

    Note:
        ``page_content`` is intentionally not inspected here (see
        ``compute_doc_content_stats`` for content statistics).

    Note:
        Once a key's sample of unique values has reached
        ``n_sample_values``, no further values for that key are added
        to the sample - the sample simply reflects the first
        ``n_sample_values`` distinct values encountered for that key,
        in document order. This makes the sample deterministic
        (independent of set iteration order) at the cost of not
        necessarily being a uniform sample over the whole corpus.

    Memory:
      - O(number of distinct metadata keys) for the per-key counters.
      - O(number of distinct keys x n_sample_values) for the sampled
        unique values, bounded by ``n_sample_values`` per key
        regardless of corpus size. If ``n_sample_values`` is ``None``,
        this becomes O(number of distinct keys x number of distinct
        values per key) instead, which can grow unbounded for
        high-cardinality keys (e.g. UUIDs).
    With a numeric ``n_sample_values``, this is effectively O(1) with
    respect to the number of documents, so it scales to corpora too
    large to fit in memory.

    Attributes:
        n_sample_values: Max number of unique sample values retained
            per metadata key, or ``None`` to retain all unique values
            for every key (no cap).
        count: Total number of documents processed.
        missing_metadata_count: Number of documents whose ``metadata``
            is empty or falsy.
        total_keys: Sum of the number of metadata keys across all
            documents processed.
        min_keys: Number of metadata keys on the document with the
            fewest keys seen so far, or ``None`` if no documents have
            been processed yet.
        max_keys: Number of metadata keys on the document with the
            most keys seen so far, or ``None`` if no documents have
            been processed yet.
    """

    n_sample_values: int | None = 3

    count: int = 0
    missing_metadata_count: int = 0
    total_keys: int = 0
    min_keys: int | None = None
    max_keys: int | None = None

    _key_counts: dict[str, int] = field(default_factory=dict)
    _key_none_counts: dict[str, int] = field(default_factory=dict)
    _key_types: dict[str, set[str]] = field(default_factory=dict)
    _key_values: dict[str, set[Any]] = field(default_factory=dict)
    _key_values_truncated: dict[str, bool] = field(default_factory=dict)

    def update(self, doc: Document) -> None:
        """Fold a single document's metadata into the running
        statistics.

        Updates the document-level counters (count, missing metadata,
        keys-per-document min/max/total) as well as the per-key
        counters, value-type sets, none/empty counts, and unique-value
        samples.

        Args:
            doc: The document to process. Its ``metadata`` is expected
                to be a mapping; a falsy/empty mapping is counted via
                ``missing_metadata_count`` and contributes zero keys.
        """
        metadata = doc.metadata or {}

        if not metadata:
            self.missing_metadata_count += 1

        n_keys = len(metadata)
        self.count += 1
        self.total_keys += n_keys

        if self.min_keys is None or n_keys < self.min_keys:
            self.min_keys = n_keys
        if self.max_keys is None or n_keys > self.max_keys:
            self.max_keys = n_keys

        for key, value in metadata.items():
            self._key_counts[key] = self._key_counts.get(key, 0) + 1
            self._key_types.setdefault(key, set()).add(type(value).__name__)

            if value is None or value == "":
                self._key_none_counts[key] = self._key_none_counts.get(key, 0) + 1

            if self._key_values_truncated.get(key, False):
                # Sample already capped for this key - do not add more values,
                # so the retained sample stays deterministic (first values seen).
                continue

            values = self._key_values.setdefault(key, set())
            try:
                if isinstance(value, (list, dict, set)):
                    # Unhashable/complex value -> stop sampling this key.
                    self._key_values_truncated[key] = True
                elif (
                    self.n_sample_values is not None
                    and len(values) >= self.n_sample_values
                    and value not in values
                ):
                    # Sample is full and this is a new value -> cap it here.
                    self._key_values_truncated[key] = True
                else:
                    values.add(value)
            except TypeError:
                self._key_values_truncated[key] = True

    def to_dict(self) -> dict[str, Any]:
        """Compute the final statistics report from the accumulated
        state.

        Safe to call multiple times and at any point during
        accumulation; it does not mutate any state and always reflects
        everything processed via ``update`` so far.

        Returns:
            A dict with the following keys:

            - ``count``: Total number of documents processed.
            - ``missing_metadata_count``: Number of documents with
              empty/missing metadata.
            - ``avg_keys``: Mean number of metadata keys per document,
              or ``0`` if no documents were processed.
            - ``min_keys`` / ``max_keys``: Fewest/most metadata keys
              seen on any single document, or ``None`` if empty.
            - ``distinct_keys_seen``: Number of distinct metadata keys
              observed across all documents.
            - ``per_key``: A dict mapping each metadata key to a dict
              with:

              - ``present_in_docs``: Number of documents containing
                the key.
              - ``missing_in_docs``: Number of documents not
                containing the key.
              - ``value_types``: Sorted list of ``type(value).__name__``
                seen for the key.
              - ``none_or_empty_count``: Number of documents where the
                key's value is ``None`` or the empty string.
              - ``unique_values_sample``: Sorted sample of unique
                values seen for the key, capped at ``n_sample_values``
                entries (or all of them, if ``n_sample_values`` is
                ``None``). Reflects the first distinct values
                encountered, in document order.
              - ``unique_values_sample_truncated``: ``True`` if not all
                unique values for the key could be retained (either
                because the sample cap was hit or because an
                unhashable value was encountered). Always ``False``
                when ``n_sample_values`` is ``None``, unless an
                unhashable value was seen.

            Percentages are intentionally omitted - compute them later
            from the raw counts (e.g. ``present_in_docs / count``)
            since they are trivially derived from this report.
        """
        n = self.count
        avg_keys = self.total_keys / n if n else 0

        per_key: dict[str, Any] = {}
        for key in sorted(self._key_counts):
            present = self._key_counts[key]
            per_key[key] = {
                "present_in_docs": present,
                "missing_in_docs": n - present,
                "value_types": sorted(self._key_types.get(key, set())),
                "none_or_empty_count": self._key_none_counts.get(key, 0),
                "unique_values_sample": sorted(self._key_values.get(key, set()), key=str),
                "unique_values_sample_truncated": self._key_values_truncated.get(key, False),
            }

        return {
            "count": n,
            "missing_metadata_count": self.missing_metadata_count,
            "avg_keys": avg_keys,
            "min_keys": self.min_keys,
            "max_keys": self.max_keys,
            "distinct_keys_seen": len(self._key_counts),
            "per_key": per_key,
        }


def compute_metadata_stats(
    documents: Iterable[Document], n_sample_values: int | None = 3
) -> dict[str, Any]:
    """Compute metadata health/statistics over a stream of documents.

    Streaming health/stat check over a list, generator, or any iterable
    of Documents. Documents are consumed one at a time, so this works
    with iterators or generators whose full contents cannot fit in
    memory — only per-key aggregates are retained (see
    ``DocMetadataStats`` for the memory profile).

    Args:
        documents: A list, generator, or other iterable of
            ``langchain_core.documents.Document`` objects. Consumed
            exactly once; if a generator/iterator is passed in, it will
            be exhausted by this call.
        n_sample_values: Max number of unique sample values to retain
            per metadata key. Defaults to 3. Pass ``None`` to track
            every unique value for every key instead of a bounded
            sample - useful for smaller corpora or low-cardinality
            metadata, but memory usage is then unbounded with respect
            to the number of distinct values per key.

    Returns:
        A dict of statistics as described in
        ``DocMetadataStats.to_dict``. For an empty input, returns a
        report with ``count`` of ``0`` and ``None``/``0``/empty values
        for the remaining fields.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents.analysis import compute_metadata_stats
        >>> docs = [
        ...     Document(page_content="a", metadata={"source": "a.pdf"}),
        ...     Document(page_content="b", metadata={"source": "b.pdf", "page": 1}),
        ... ]
        >>> analysis = compute_metadata_stats(docs)
        >>> analysis["count"]
        2

        ```
    """
    stats = MetadataStats(n_sample_values=n_sample_values)
    for doc in documents:
        stats.update(doc)
    return stats.to_dict()
