"""The interned-value cache's ceiling bounds the memory it PINS (lane M1, 2026-11-19).

Each entry keeps its live value alive. The ceiling used to count the value's interned form — a few KB of
references once its large children went by reference — so after a child's own entry was dropped its parent
still pinned it, uncounted: a 64 MB ceiling held ~105 MB of Python heap after a research read's pages went
through it (each page: raw HTML, link records, text renderings). Red before: retained ~1.6x the ceiling.
"""

from __future__ import annotations

import gc
import tracemalloc

from matrx_graph.checkpoint import values as V

LIMIT = 16 * 1024


def _page(i: int) -> dict:
    return {
        "url": f"https://example.com/{i}",
        "raw_html": ("<p>x%d</p>" % i) * 40_000,
        "link_records": [{"href": f"https://example.com/{i}/{j}", "text": "t" * 40} for j in range(3_000)],
        "ai_content": ("w%d " % i) * 30_000,
        **{f"field_{k}": ("m%d" % i) * 400 for k in range(40)},
    }


def test_a_full_cache_pins_no_more_than_its_ceiling(monkeypatch) -> None:
    ceiling = 8 * 1024 * 1024
    monkeypatch.setattr(V, "INTERNED_CACHE_MAX_BYTES", ceiling)
    V.clear_interned_cache()
    gc.collect()
    tracemalloc.start()
    try:
        base = tracemalloc.get_traced_memory()[0]
        for i in range(120):
            page = _page(i)
            V.intern_values(page, {}, LIMIT, V.InternMemo(committed=set()))
            del page
        gc.collect()
        pinned = tracemalloc.get_traced_memory()[0] - base
    finally:
        tracemalloc.stop()
        V.clear_interned_cache()
    assert V._interned_bytes <= ceiling
    assert pinned <= ceiling, f"the cache pins {pinned / 1e6:.1f} MB under a {ceiling / 1e6:.1f} MB ceiling"
