"""ProducerRegistry: each producer's sequence high-water, delivered tally, capture gaps and clean seal."""

from __future__ import annotations

#: How many capture-gap records a producer file keeps; `gap_count` keeps the total. The list
#: grew by one per dropped write and the file is rewritten on every drop: 6,000 drops made a
#: refused `log()` 16 ms -> 107 ms.
_GAPS_KEPT = 32
