"""Pure site-wide near-duplicate clustering over stored content fingerprints."""

from __future__ import annotations

from dataclasses import dataclass, field

from matrx_scraper.parser.hashing import simhash64_hamming
from matrx_scraper.seo_audit import normalized_url_key

SIMHASH_BITS = 64
NEAR_DUPLICATE_SIMILARITY = 0.90
NEAR_DUPLICATE_MAX_DISTANCE = int(SIMHASH_BITS * (1 - NEAR_DUPLICATE_SIMILARITY))
EVIDENCE_CLUSTER_LIMIT = 20
EVIDENCE_PAGE_LIMIT = 20
EVIDENCE_PAIR_LIMIT = 50


@dataclass(frozen=True)
class NearDuplicatePage:
    page_id: str
    url: str
    fingerprint_version: int | None
    simhash64: str | None
    canonical_url: str | None = None
    indexable: bool | None = True


@dataclass(frozen=True)
class NearDuplicatePair:
    left_page_id: str
    right_page_id: str
    hamming_distance: int

    @property
    def similarity_percent(self) -> float:
        return round(100 * (1 - self.hamming_distance / SIMHASH_BITS), 2)


@dataclass
class NearDuplicateCluster:
    pages: list[NearDuplicatePage]
    pairs: list[NearDuplicatePair]


@dataclass
class NearDuplicateReport:
    indexable_pages: int
    fingerprinted_pages: int
    pages_without_fingerprint: int
    pages_without_indexability: int
    near_duplicate_pages: int
    canonical_pairs_excluded: int
    score: int | None
    clusters: list[NearDuplicateCluster] = field(default_factory=list)

    def evidence(self) -> dict[str, object]:
        clusters = []
        for cluster in self.clusters[:EVIDENCE_CLUSTER_LIMIT]:
            page_urls = [page.url for page in cluster.pages]
            pairs_by_id = {page.page_id: page.url for page in cluster.pages}
            clusters.append(
                {
                    "page_count": len(cluster.pages),
                    "pages": page_urls[:EVIDENCE_PAGE_LIMIT],
                    "pages_omitted": max(0, len(page_urls) - EVIDENCE_PAGE_LIMIT),
                    "matching_pairs": [
                        {
                            "left_page_id": pair.left_page_id,
                            "left_url": pairs_by_id[pair.left_page_id],
                            "right_page_id": pair.right_page_id,
                            "right_url": pairs_by_id[pair.right_page_id],
                            "hamming_distance": pair.hamming_distance,
                            "similarity_percent": pair.similarity_percent,
                        }
                        for pair in cluster.pairs[:EVIDENCE_PAIR_LIMIT]
                    ],
                    "pairs_omitted": max(0, len(cluster.pairs) - EVIDENCE_PAIR_LIMIT),
                }
            )
        return {
            "threshold_percent": NEAR_DUPLICATE_SIMILARITY * 100,
            "indexable_pages": self.indexable_pages,
            "fingerprinted_pages": self.fingerprinted_pages,
            "pages_without_fingerprint": self.pages_without_fingerprint,
            "pages_without_indexability": self.pages_without_indexability,
            "near_duplicate_pages": self.near_duplicate_pages,
            "canonical_pairs_excluded": self.canonical_pairs_excluded,
            "clusters_total": len(self.clusters),
            "clusters_returned": len(clusters),
            "clusters_omitted": max(0, len(self.clusters) - len(clusters)),
            "clusters": clusters,
        }


def _canonical_identity(page: NearDuplicatePage) -> str:
    canonical = page.canonical_url
    if canonical and canonical.startswith(("http://", "https://")):
        return normalized_url_key(canonical)
    return normalized_url_key(page.url)


def _canonical_consolidated(left: NearDuplicatePage, right: NearDuplicatePage) -> bool:
    left_url = normalized_url_key(left.url)
    right_url = normalized_url_key(right.url)
    left_identity = _canonical_identity(left)
    right_identity = _canonical_identity(right)
    return left_identity == right_identity and (
        left_identity != left_url or right_identity != right_url
    )


def build_near_duplicate_report(pages: list[NearDuplicatePage]) -> NearDuplicateReport:
    """Cluster indexable pages connected by a stored >=90%-similar SimHash pair."""

    pages_without_indexability = sum(page.indexable is None for page in pages)
    indexable = [page for page in pages if page.indexable is True]
    fingerprinted = [
        page
        for page in indexable
        if page.fingerprint_version is not None and page.simhash64 is not None
    ]
    adjacency: dict[str, set[str]] = {page.page_id: set() for page in fingerprinted}
    pairs: list[NearDuplicatePair] = []
    canonical_pairs_excluded = 0

    for position, left in enumerate(fingerprinted):
        for right in fingerprinted[position + 1 :]:
            if left.fingerprint_version != right.fingerprint_version:
                continue
            distance = simhash64_hamming(left.simhash64 or "", right.simhash64 or "")
            if distance > NEAR_DUPLICATE_MAX_DISTANCE:
                continue
            if _canonical_consolidated(left, right):
                canonical_pairs_excluded += 1
                continue
            adjacency[left.page_id].add(right.page_id)
            adjacency[right.page_id].add(left.page_id)
            pairs.append(NearDuplicatePair(left.page_id, right.page_id, distance))

    pages_by_id = {page.page_id: page for page in fingerprinted}
    pairs_by_page: dict[str, list[NearDuplicatePair]] = {page.page_id: [] for page in fingerprinted}
    for pair in pairs:
        pairs_by_page[pair.left_page_id].append(pair)
        pairs_by_page[pair.right_page_id].append(pair)

    clusters: list[NearDuplicateCluster] = []
    visited: set[str] = set()
    for start in sorted(adjacency):
        if start in visited or not adjacency[start]:
            continue
        pending = [start]
        members: set[str] = set()
        while pending:
            page_id = pending.pop()
            if page_id in members:
                continue
            members.add(page_id)
            pending.extend(adjacency[page_id] - members)
        visited.update(members)
        cluster_pairs = {
            pair
            for page_id in members
            for pair in pairs_by_page[page_id]
            if pair.left_page_id in members and pair.right_page_id in members
        }
        clusters.append(
            NearDuplicateCluster(
                pages=sorted((pages_by_id[page_id] for page_id in members), key=lambda p: p.url),
                pairs=sorted(
                    cluster_pairs,
                    key=lambda pair: (
                        pair.hamming_distance,
                        pair.left_page_id,
                        pair.right_page_id,
                    ),
                ),
            )
        )
    clusters.sort(key=lambda cluster: (-len(cluster.pages), cluster.pages[0].url))
    near_duplicate_pages = sum(len(cluster.pages) for cluster in clusters)
    score = (
        round(100 * (1 - near_duplicate_pages / len(indexable)))
        if indexable and not pages_without_indexability and len(fingerprinted) == len(indexable)
        else None
    )
    return NearDuplicateReport(
        indexable_pages=len(indexable),
        fingerprinted_pages=len(fingerprinted),
        pages_without_fingerprint=len(indexable) - len(fingerprinted),
        pages_without_indexability=pages_without_indexability,
        near_duplicate_pages=near_duplicate_pages,
        canonical_pairs_excluded=canonical_pairs_excluded,
        score=score,
        clusters=clusters,
    )


__all__ = [
    "NEAR_DUPLICATE_MAX_DISTANCE",
    "NearDuplicatePage",
    "NearDuplicateReport",
    "build_near_duplicate_report",
]
