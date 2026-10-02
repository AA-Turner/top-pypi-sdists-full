"""Rank notation — the one sentence every SERP position is reported as.

OPENSEO-TOOLS-SPEC §5.3. OpenSEO leaves the counting and the wording to the
agent ("count organic listings yourself", their ``seo-audit`` skill); an agent
that miscounts a featured snippet as position 1 tells a person a false rank.
Here code decides the words, from an organic rank that code counted
(``providers/dataforseo/serp_organic.py``):

* ``"#10 (page 1)"`` / ``"#11 (page 2)"`` — found, at this organic position;
* ``"not in the first 20 results"`` — the lookup worked and the target is not
  in the depth that was read (a statement about THAT depth, never "unranked");
  when fewer organic listings came back than the depth, the sentence names the
  count actually read (``"not in the first 15 organic results read (15 < 20)"``);
* ``"unknown"`` — the lookup itself failed, so nothing can be said.

Pure: no I/O, no knobs. ``results_per_page`` is Google's ten organic results per
page, the unit the provider bills in (``pricing.py`` ``serp_10_result``).
"""

from __future__ import annotations

UNKNOWN = "unknown"

#: Google's organic results per page — the provider's billing page, not a taste.
RESULTS_PER_PAGE = 10


def page_of(organic_rank: int, results_per_page: int = RESULTS_PER_PAGE) -> int:
    """The results page an organic rank sits on (1-based)."""
    if organic_rank < 1:
        raise ValueError(f"organic rank must be 1 or more, got {organic_rank}")
    return (organic_rank - 1) // results_per_page + 1


def rank_notation(
    organic_rank: int | None, depth: int, ok: bool, *, organic_read: int | None = None
) -> str:
    """The position sentence for one SERP lookup.

    ``ok`` is whether the lookup succeeded; a failed lookup is ``"unknown"``
    whatever else was passed. A successful lookup with no rank says what was
    actually read: ``depth`` results when at least that many organic listings
    came back, else the ``organic_read`` organic listings that did — a page of
    ads and features must never be reported as "the first 20 results".
    """
    if not ok:
        return UNKNOWN
    if organic_rank is None:
        if depth < 1:
            raise ValueError(f"depth must be 1 or more, got {depth}")
        if organic_read is not None and organic_read < depth:
            return (
                f"not in the first {organic_read} organic results read ({organic_read} < {depth})"
            )
        return f"not in the first {depth} results"
    return f"#{organic_rank} (page {page_of(organic_rank)})"


__all__ = ["RESULTS_PER_PAGE", "UNKNOWN", "page_of", "rank_notation"]
