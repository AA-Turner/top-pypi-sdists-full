"""Longevity tracking for context items.

Tracks which entities appear repeatedly across reranking calls.
Items that keep appearing are likely important and get boosted.

This uses an in-memory cache that resets on process restart.
For persistence, the cache could be stored in the graph database.
"""

import math
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class LongevityRecord:
    """Track an entity's appearance history."""

    qualified_name: str
    appearance_count: int = 0
    first_seen: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)

    def record_appearance(self) -> None:
        """Record a new appearance of this entity."""
        self.appearance_count += 1
        self.last_seen = time.time()

    def get_longevity_score(self, now: Optional[float] = None) -> float:
        """Calculate longevity score based on appearance count.

        Longevity = items that have appeared in context frame more than once.
        No time-based decay - if it keeps appearing, it's important.

        Score formula (log scale for diminishing returns):
        - 1 appearance = 0.0 (first time, no longevity yet)
        - 2 appearances = 0.37
        - 3 appearances = 0.50
        - 5 appearances = 0.62
        - 10 appearances = 0.77
        - 20 appearances = 0.90

        Args:
            now: Current timestamp (unused, kept for API compatibility)

        Returns:
            Score between 0.0 and 1.0
        """
        if self.appearance_count <= 1:
            return 0.0  # First appearance = no longevity

        # Log scale for diminishing returns
        # Subtract 1 so first repeat (count=2) starts contributing
        return min(1.0, math.log(self.appearance_count) / 3)


class LongevityTracker:
    """Tracks entity appearances across reranking calls."""

    def __init__(self, max_entries: int = 1000):
        """Initialize the tracker.

        Args:
            max_entries: Maximum number of entities to track (LRU eviction)
        """
        self._records: dict[str, LongevityRecord] = {}
        self._max_entries = max_entries

    def record_appearance(self, qualified_name: str) -> None:
        """Record that an entity appeared in reranking.

        Args:
            qualified_name: The entity's qualified name
        """
        if qualified_name in self._records:
            self._records[qualified_name].record_appearance()
        else:
            # Evict oldest entries if at capacity
            if len(self._records) >= self._max_entries:
                self._evict_oldest()

            self._records[qualified_name] = LongevityRecord(
                qualified_name=qualified_name,
                appearance_count=1,
            )

    def record_batch(self, qualified_names: list[str]) -> None:
        """Record appearances for multiple entities.

        Args:
            qualified_names: List of entity qualified names
        """
        for qname in qualified_names:
            self.record_appearance(qname)

    def get_longevity_score(self, qualified_name: str) -> float:
        """Get the longevity score for an entity.

        Args:
            qualified_name: The entity's qualified name

        Returns:
            Score between 0.0 and 1.0 (0.0 if never seen)
        """
        record = self._records.get(qualified_name)
        if record is None:
            return 0.0
        return record.get_longevity_score()

    def get_appearance_count(self, qualified_name: str) -> int:
        """Get how many times an entity has appeared.

        Args:
            qualified_name: The entity's qualified name

        Returns:
            Number of appearances (0 if never seen)
        """
        record = self._records.get(qualified_name)
        return record.appearance_count if record else 0

    def _evict_oldest(self) -> None:
        """Evict the oldest (least recently seen) entries."""
        if not self._records:
            return

        # Sort by last_seen and remove bottom 10%
        sorted_records = sorted(
            self._records.items(),
            key=lambda x: x[1].last_seen,
        )

        evict_count = max(1, len(sorted_records) // 10)
        for qname, _ in sorted_records[:evict_count]:
            del self._records[qname]

    def clear(self) -> None:
        """Clear all longevity records."""
        self._records.clear()

    def get_stats(self) -> dict:
        """Get statistics about the tracker.

        Returns:
            Dictionary with tracker statistics
        """
        if not self._records:
            return {
                "total_entities": 0,
                "total_appearances": 0,
                "avg_appearances": 0,
                "max_appearances": 0,
            }

        appearances = [r.appearance_count for r in self._records.values()]
        return {
            "total_entities": len(self._records),
            "total_appearances": sum(appearances),
            "avg_appearances": sum(appearances) / len(appearances),
            "max_appearances": max(appearances),
        }


# Global tracker instance (shared across reranking calls)
_global_tracker: Optional[LongevityTracker] = None


def get_longevity_tracker() -> LongevityTracker:
    """Get the global longevity tracker (creates if needed)."""
    global _global_tracker
    if _global_tracker is None:
        _global_tracker = LongevityTracker()
    return _global_tracker


def record_reranked_items(qualified_names: list[str]) -> None:
    """Record that items appeared in a reranking result.

    Call this after reranking to update longevity scores.

    Args:
        qualified_names: List of qualified names that were reranked
    """
    get_longevity_tracker().record_batch(qualified_names)


def get_longevity_score(qualified_name: str) -> float:
    """Get the longevity score for an entity.

    Args:
        qualified_name: The entity's qualified name

    Returns:
        Score between 0.0 and 1.0
    """
    return get_longevity_tracker().get_longevity_score(qualified_name)
