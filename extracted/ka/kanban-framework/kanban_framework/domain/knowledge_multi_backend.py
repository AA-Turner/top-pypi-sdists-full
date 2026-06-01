"""Multi-backend knowledge adapter — RRF merge and dedup across backends."""
from __future__ import annotations


class MultiBackend:
    """Wraps 2+ backends, merges results with dedup. (#237)

    Local and shared knowledge bases coexist — search both, deduplicate
    by (title, domain), RRF-merge scores.
    """

    def __init__(self, primary, secondary=None):
        self._primary = primary
        self._secondary = secondary

    def _merge_dedup(self, primary_results, secondary_results, limit):
        """Merge two result lists with RRF (Reciprocal Rank Fusion). (#319)"""
        _RRF_K = 60

        seen = {}
        for rank, r in enumerate(primary_results):
            key = (r.get("title", "").strip(), r.get("domain", ""))
            r["_source"] = "local"
            r["_rrf_score"] = 1.0 / (_RRF_K + rank + 1)
            seen[key] = r

        if secondary_results:
            for rank, r in enumerate(secondary_results):
                key = (r.get("title", "").strip(), r.get("domain", ""))
                r["_source"] = "share"
                rrf_contrib = 1.0 / (_RRF_K + rank + 1)
                if key in seen:
                    seen[key]["_rrf_score"] += rrf_contrib
                else:
                    r["_rrf_score"] = rrf_contrib
                    seen[key] = r

        merged = sorted(seen.values(), key=lambda r: r.get("_rrf_score", 0), reverse=True)
        for r in merged:
            r.pop("_rrf_score", None)
        return merged[:limit]

    def search(self, keyword, limit=20):
        primary = self._primary.search(keyword, limit=limit) if self._primary else []
        secondary = self._secondary.search(keyword, limit=limit) if self._secondary else []
        return self._merge_dedup(primary, secondary, limit)

    def search_semantic(self, query, limit=20):
        primary = self._primary.search_semantic(query, limit=limit) if self._primary else []
        secondary = self._secondary.search_semantic(query, limit=limit) if self._secondary else []
        return self._merge_dedup(primary, secondary, limit)

    def search_hybrid(self, keyword, limit=20):
        primary = self._primary.search_hybrid(keyword, limit=limit) if self._primary else []
        secondary = self._secondary.search_hybrid(keyword, limit=limit) if self._secondary else []
        return self._merge_dedup(primary, secondary, limit)

    def add_entry(self, **kwargs):
        return self._primary.add_entry(**kwargs)

    def list_entries(self, domain=None, category=None, status="active", limit=50, offset=0):
        return self._primary.list_entries(domain=domain, category=category,
                                           status=status, limit=limit, offset=offset)

    def get_entry(self, entry_id):
        e = self._primary.get_entry(entry_id)
        if e is None and self._secondary:
            e = self._secondary.get_entry(entry_id)
        return e
