"""Keyword clusters by search-result overlap — pure, deterministic code, no model.

Two keywords belong together when Google answers them with the same pages: if
the top results of "hard drive shredding" and "hard drive destruction" share
enough URLs, one page can rank for both. This file decides that from stored SERP
snapshots only; it never fetches, buys or guesses.

Rules, each unit-tested (``tests/test_serp_clusters.py``):

* a Google click wrapper (``google.<tld>/url?q=<url>`` / ``url=``) is unwrapped to its
  target first; YouTube hosts (``youtu.be/<id>``, ``m.youtube.com``, ``www.``) are one
  host with ``t``/``si``/``feature`` dropped there only (elsewhere ``t=`` can name a
  different page); percent-encoding and a trailing ``/index.html`` are normalized
  (census 2026-10-22: no stored ORGANIC result is wrapped — DataForSEO and
  SerpAPI store the target — so this guards other providers and older payloads);
* a URL is compared after :func:`normalize_url` — scheme, ``www.``, default
  port, fragment, trailing slash and tracking parameters (``utm_*``, ``gclid``,
  ``srsltid`` …) are dropped; host is lower-cased; the remaining query is sorted;
* each keyword contributes its first ``top_n`` organic URLs, de-duplicated after
  normalization (a site listed twice counts once);
* every pair's shared-URL count and Jaccard index are computed through an
  inverted index (pairs that share nothing are never materialized);
* a pair LINKS when it clears the threshold: ``mode="count"`` needs at least
  ``min_shared`` shared URLs, ``mode="jaccard"`` needs ``jaccard >= min_jaccard``
  (and at least one shared URL);
* clusters are single-link (union-find): A–B and B–C linked puts A, B and C
  together even when A and C share nothing;
* the ``max_cluster_size`` guard: links are applied strongest first (score, then
  shared count, then ids); a link that would grow a cluster past the limit is
  refused and the refusal is reported on both keywords — never silently merged;
* the head of a cluster is its highest-volume keyword (unknown volume ranks
  last; ties by phrase, then id); the cluster id is a hash of its sorted members,
  so the same membership always gets the same id;
* a keyword with no stored snapshot is ``not_clustered`` with the reason
  "no stored results"; a snapshot without organic URLs says so too. Neither is
  ever placed in a cluster.
"""

from __future__ import annotations

import hashlib
import re
from collections import defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from typing import Any, Literal
from urllib.parse import parse_qsl, quote, unquote, urlencode, urlsplit

ClusterMode = Literal["count", "jaccard"]
KeywordStatus = Literal["clustered", "alone", "not_clustered"]

NO_STORED_RESULTS = "no stored results"
NO_ORGANIC_RESULTS = "the stored results have no organic URLs"

#: Query parameters that identify a click, not a page.
TRACKING_PARAMS: frozenset[str] = frozenset(
    {
        "gclid", "gclsrc", "dclid", "gbraid", "wbraid", "fbclid", "msclkid", "yclid",
        "mc_cid", "mc_eid", "_ga", "_gl", "igshid", "srsltid", "ref_src", "spm",
    }
)
TRACKING_PREFIXES: tuple[str, ...] = ("utm_", "pk_", "hsa_")


#: Hosts that serve the same YouTube pages (youtu.be is handled separately).
_YOUTUBE_HOSTS: frozenset[str] = frozenset({"youtube.com", "m.youtube.com", "music.youtube.com"})
#: On YouTube these name a playback position or the share, never a different video.
_YOUTUBE_TRACKING: frozenset[str] = frozenset({"t", "si", "feature", "pp", "start"})
#: A trailing default document is the directory itself.
_INDEX_PAGE = re.compile(r"/index\.(html?|php|aspx?)$", re.IGNORECASE)
_PATH_SAFE = "/:@!$&'()*+,;=-._~"


def _is_tracking(name: str) -> bool:
    low = name.lower()
    return low in TRACKING_PARAMS or low.startswith(TRACKING_PREFIXES)


_GOOGLE_HOST = re.compile(r"^(www\.)?google(\.[a-z]{2,3}){1,2}$")


def _unwrap_google_redirect(parts: Any) -> str | None:
    """The real target of a Google click wrapper (``google.<tld>/url?q=<url>`` or
    ``?url=<url>``), else ``None``. A Google SEARCH link (``/search?q=words``) is not
    a wrapper — its ``q`` is not a URL — and is left as it is."""
    host = (parts.hostname or "").lower()
    if not _GOOGLE_HOST.match(host) or parts.path != "/url":
        return None
    params = dict(parse_qsl(parts.query, keep_blank_values=True))
    for key in ("q", "url"):
        target = params.get(key, "")
        if target.lower().startswith(("http://", "https://")):
            return target
    return None


def normalize_url(raw: str | None) -> str | None:
    """``https://www.Example.com/a/?utm_source=x&b=2#top`` → ``example.com/a?b=2``.

    ``None`` when the input has no host. Path case is kept (paths are case
    sensitive); the host is lower-cased."""
    if not raw or not isinstance(raw, str):
        return None
    text = raw.strip()
    if not text:
        return None
    if "://" not in text:
        text = "http://" + text.lstrip("/")
    try:
        parts = urlsplit(text)
        target = _unwrap_google_redirect(parts)
        if target is not None:
            parts = urlsplit(target)
        host = (parts.hostname or "").strip(".").lower()
        port = parts.port
    except ValueError:
        return None
    if not host:
        return None
    host = host.removeprefix("www.")
    if port is not None and port not in (80, 443):
        host = f"{host}:{port}"
    # Percent-encoding normalized: %7E and ~ (or %2f-style case variants) are one path.
    # An encoded slash (%2F) is not a path separator, so it stays encoded.
    path = "%2F".join(
        quote(unquote(piece), safe=_PATH_SAFE) for piece in re.split(r"%2[fF]", parts.path or "")
    )
    params = parse_qsl(parts.query, keep_blank_values=True)
    youtube = host in _YOUTUBE_HOSTS
    if host == "youtu.be":
        # youtu.be/<id> is youtube.com/watch?v=<id>
        video = path.strip("/").split("/", 1)[0]
        youtube, host, path = True, "youtube.com", "/watch"
        if video:
            params = [("v", video), *[(k, v) for k, v in params if k != "v"]]
    elif youtube:
        host = "youtube.com"
    path = _INDEX_PAGE.sub("", path)
    while path.endswith("/"):
        path = path[:-1]
    query = sorted(
        (k, v)
        for k, v in params
        if not _is_tracking(k) and not (youtube and k.lower() in _YOUTUBE_TRACKING)
    )
    return host + path + (f"?{urlencode(query)}" if query else "")


@dataclass(frozen=True)
class KeywordSerp:
    """One keyword's stored evidence. ``urls`` are its organic result URLs in rank
    order; ``None`` means no stored snapshot exists (never an empty guess)."""

    keyword_id: str
    phrase: str
    urls: Sequence[str] | None
    search_volume: int | None = None
    snapshot_id: str | None = None
    observed_at: str | None = None


@dataclass(frozen=True)
class ClusterSettings:
    top_n: int = 10
    mode: ClusterMode = "count"
    min_shared: int = 3
    min_jaccard: float = 0.2
    max_cluster_size: int = 50

    def as_dict(self) -> dict[str, Any]:
        return {
            "top_n": self.top_n,
            "mode": self.mode,
            "min_shared": self.min_shared,
            "min_jaccard": self.min_jaccard,
            "max_cluster_size": self.max_cluster_size,
        }


@dataclass(frozen=True)
class PairOverlap:
    a: str
    b: str
    shared_urls: tuple[str, ...]
    jaccard: float

    @property
    def shared(self) -> int:
        return len(self.shared_urls)


@dataclass
class KeywordCluster:
    """One keyword's answer: its cluster (or why it has none) and the link that
    justifies it — the shared URLs with the keyword it is most strongly linked to."""

    keyword_id: str
    phrase: str
    status: KeywordStatus
    reason: str | None = None
    cluster_id: str | None = None
    head_keyword_id: str | None = None
    head_phrase: str | None = None
    cluster_size: int = 0
    linked_to: str | None = None
    linked_phrase: str | None = None
    shared_urls: tuple[str, ...] = ()
    shared_count: int = 0
    jaccard: float | None = None
    overlap_score: float | None = None
    links: int = 0
    refused_links: int = 0
    snapshot_id: str | None = None
    observed_at: str | None = None

    def as_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "keyword_id": self.keyword_id,
            "phrase": self.phrase,
            "status": self.status,
        }
        if self.reason:
            out["reason"] = self.reason
        if self.status == "clustered":
            out.update(
                cluster_id=self.cluster_id,
                head_phrase=self.head_phrase,
                head_keyword_id=self.head_keyword_id,
                cluster_size=self.cluster_size,
                linked_to=self.linked_phrase,
                linked_keyword_id=self.linked_to,
                shared_count=self.shared_count,
                jaccard=self.jaccard,
                overlap_score=self.overlap_score,
                shared_urls=list(self.shared_urls),
                links=self.links,
            )
        if self.refused_links:
            out["refused_links"] = self.refused_links
        if self.snapshot_id:
            out["snapshot_id"] = self.snapshot_id
            out["observed_at"] = self.observed_at
        return out


@dataclass
class Clustering:
    keywords: list[KeywordCluster]
    clusters: list[dict[str, Any]]
    settings: ClusterSettings
    refused_links: int = 0
    notices: list[str] = field(default_factory=list)

    def by_keyword(self) -> dict[str, KeywordCluster]:
        return {k.keyword_id: k for k in self.keywords}


def top_urls(urls: Iterable[str] | None, top_n: int) -> tuple[str, ...]:
    """The first ``top_n`` distinct normalized URLs, in rank order."""
    out: list[str] = []
    seen: set[str] = set()
    for raw in urls or ():
        url = normalize_url(raw)
        if url is None or url in seen:
            continue
        seen.add(url)
        out.append(url)
        if len(out) >= top_n:
            break
    return tuple(out)


def pairwise_overlaps(tops: dict[str, tuple[str, ...]]) -> list[PairOverlap]:
    """Every keyword pair sharing at least one URL, with the shared URLs in the
    first keyword's rank order and the Jaccard index. Pure."""
    by_url: dict[str, list[str]] = defaultdict(list)
    for kid in sorted(tops):
        for url in tops[kid]:
            by_url[url].append(kid)
    shared: dict[tuple[str, str], set[str]] = defaultdict(set)
    for url, kids in by_url.items():
        for i, a in enumerate(kids):
            for b in kids[i + 1:]:
                shared[(a, b)].add(url)
    out: list[PairOverlap] = []
    for (a, b), urls in sorted(shared.items()):
        union = len(set(tops[a]) | set(tops[b]))
        ordered = tuple(u for u in tops[a] if u in urls)
        out.append(PairOverlap(a, b, ordered, round(len(urls) / union, 4) if union else 0.0))
    return out


def _links(overlap: PairOverlap, settings: ClusterSettings) -> bool:
    if settings.mode == "jaccard":
        return overlap.shared >= 1 and overlap.jaccard >= settings.min_jaccard
    return overlap.shared >= settings.min_shared


def _score(overlap: PairOverlap, settings: ClusterSettings) -> float:
    return overlap.jaccard if settings.mode == "jaccard" else float(overlap.shared)


def _head_key(serp: KeywordSerp) -> tuple[Any, ...]:
    vol = serp.search_volume
    return (vol is None, -(vol or 0), serp.phrase.lower(), serp.keyword_id)


def cluster_id_for(member_ids: Iterable[str]) -> str:
    """A hash of the cluster's sorted member ids: the same membership always has the
    same id. Stable across runs only when every run clusters the SAME input set — the
    service always clusters all of a site's keywords with stored results in a market."""
    digest = hashlib.sha1("|".join(sorted(member_ids)).encode("utf-8")).hexdigest()
    return f"serp-{digest[:12]}"


def cluster_keywords(serps: Sequence[KeywordSerp], settings: ClusterSettings | None = None) -> Clustering:
    """Group keywords whose stored top results overlap. Pure and deterministic:
    the same inputs and settings always give the same clusters and ids."""
    settings = settings or ClusterSettings()
    if settings.top_n < 1 or settings.max_cluster_size < 2:
        raise ValueError("top_n must be at least 1 and max_cluster_size at least 2")
    by_id: dict[str, KeywordSerp] = {}
    for serp in serps:
        by_id.setdefault(serp.keyword_id, serp)
    tops: dict[str, tuple[str, ...]] = {}
    results: dict[str, KeywordCluster] = {}
    for kid, serp in by_id.items():
        if serp.urls is None:
            results[kid] = KeywordCluster(kid, serp.phrase, "not_clustered", NO_STORED_RESULTS)
            continue
        top = top_urls(serp.urls, settings.top_n)
        if not top:
            results[kid] = KeywordCluster(
                kid, serp.phrase, "not_clustered", NO_ORGANIC_RESULTS,
                snapshot_id=serp.snapshot_id, observed_at=serp.observed_at,
            )
            continue
        tops[kid] = top

    candidates = [o for o in pairwise_overlaps(tops) if _links(o, settings)]
    candidates.sort(key=lambda o: (-_score(o, settings), -o.shared, o.a, o.b))

    parent = {kid: kid for kid in tops}
    size = {kid: 1 for kid in tops}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    best: dict[str, PairOverlap] = {}
    link_count: dict[str, int] = defaultdict(int)
    refused: dict[str, int] = defaultdict(int)
    refused_total = 0
    for overlap in candidates:
        ra, rb = find(overlap.a), find(overlap.b)
        if ra != rb:
            if size[ra] + size[rb] > settings.max_cluster_size:
                refused[overlap.a] += 1
                refused[overlap.b] += 1
                refused_total += 1
                continue
            if ra > rb:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
        for kid in (overlap.a, overlap.b):
            link_count[kid] += 1
            best.setdefault(kid, overlap)  # candidates are strongest first

    members: dict[str, list[str]] = defaultdict(list)
    for kid in tops:
        members[find(kid)].append(kid)

    clusters: list[dict[str, Any]] = []
    for root, kids in members.items():
        if len(kids) < 2:
            continue
        ordered = sorted(kids, key=lambda k: _head_key(by_id[k]))
        head = by_id[ordered[0]]
        cid = cluster_id_for(kids)
        clusters.append(
            {
                "cluster_id": cid,
                "head_phrase": head.phrase,
                "head_keyword_id": head.keyword_id,
                "size": len(kids),
                "members": [by_id[k].phrase for k in ordered],
            }
        )
        for kid in kids:
            overlap = best[kid]
            other = overlap.b if overlap.a == kid else overlap.a
            serp = by_id[kid]
            results[kid] = KeywordCluster(
                kid, serp.phrase, "clustered",
                cluster_id=cid, head_keyword_id=head.keyword_id, head_phrase=head.phrase,
                cluster_size=len(kids), linked_to=other, linked_phrase=by_id[other].phrase,
                shared_urls=overlap.shared_urls, shared_count=overlap.shared,
                jaccard=overlap.jaccard, overlap_score=_score(overlap, settings),
                links=link_count[kid], refused_links=refused.get(kid, 0),
                snapshot_id=serp.snapshot_id, observed_at=serp.observed_at,
            )
    for kid in tops:
        if kid not in results:
            serp = by_id[kid]
            results[kid] = KeywordCluster(
                kid, serp.phrase, "alone",
                reason=(
                    "linking it would pass the largest cluster size"
                    if refused.get(kid) else "no other keyword shares enough top results"
                ),
                refused_links=refused.get(kid, 0),
                snapshot_id=serp.snapshot_id, observed_at=serp.observed_at,
            )

    clusters.sort(key=lambda c: (-c["size"], c["head_phrase"].lower(), c["cluster_id"]))
    rank = {c["cluster_id"]: i for i, c in enumerate(clusters)}
    status_order = {"clustered": 0, "alone": 1, "not_clustered": 2}
    keywords = sorted(
        results.values(),
        key=lambda k: (
            status_order[k.status],
            rank.get(k.cluster_id or "", 0),
            k.keyword_id != k.head_keyword_id,
            _head_key(by_id[k.keyword_id]),
        ),
    )
    notices: list[str] = []
    if refused_total:
        notices.append(
            f"{refused_total} link(s) were refused because they would make a cluster larger than "
            f"{settings.max_cluster_size} keywords (the largest-cluster setting)."
        )
    return Clustering(keywords, clusters, settings, refused_total, notices)


__all__ = [
    "ClusterMode",
    "ClusterSettings",
    "Clustering",
    "KeywordCluster",
    "KeywordSerp",
    "NO_ORGANIC_RESULTS",
    "NO_STORED_RESULTS",
    "PairOverlap",
    "TRACKING_PARAMS",
    "cluster_id_for",
    "cluster_keywords",
    "normalize_url",
    "pairwise_overlaps",
    "top_urls",
]
