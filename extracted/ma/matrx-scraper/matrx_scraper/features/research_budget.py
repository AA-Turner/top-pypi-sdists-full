"""What one research condense is sent — pure functions, no I/O, no model call.

The research path (matrx-ai ``research_web``) and the single-page condense (``read_page``) both
prepare condenser input here, so there is one budget and one cut order:

1. **Group** the queries (``group_queries``): one condensed report per group.
2. **Clean** each page (``clean_page_text``): image markup out, repeated link URLs collapsed,
   blank runs collapsed.
3. **Dedupe** (``dedupe_pages``): one copy per canonical URL and per near-identical body.
4. **Rank** (``score_page``): term overlap with the group's queries and the instructions, plus
   search rank.
5. **Cap each page** (``cap_page_text``): the head is kept and the text says so.
6. **Fit the group budget** (``fit_group_budget``): lowest-ranked pages lose first (largest
   first among equals), each down to a floor before a higher-ranked page loses anything; a page
   at its floor may then be dropped to a listing-only line. Never the tail of assembled text.

Every reduction is recorded on the page record, so the run facts survive any later text cut.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit

# KNOB MIRROR — the standalone (no host) values; the host's ``agents.research_web`` knob rows
# carry the same numbers (resolved in matrx_ai.tools.implementations.web.research_budgets).
PAGE_MAX_CHARS = 20_000
CONDENSE_MAX_CHARS = 120_000
LISTINGS_MAX_CHARS = 30_000
FALLBACK_MAX_CHARS = 40_000
PAGE_FLOOR_CHARS = 2_000
LISTINGS_DETAIL = 1
PAGE_CHAR_COUNTS = 0

#: Each group holds at most this many queries (Arman, 2026-11-08: "up to 3 keywords could be in 1 report").
MAX_QUERIES_PER_GROUP = 3

NOT_READ_LABEL = "not read: search snippet only"

RUN_FACTS_OPEN = "=== RUN FACTS (what was done to this input; not page content) ==="
RUN_FACTS_CLOSE = "=== END RUN FACTS ==="


def group_queries(queries: list[str]) -> list[list[str]]:
    """1-3 queries are one group; above that balanced groups of at most 3, as few 3s as needed.

    4 → 2+2, 5 → 3+2, 6 → 3+3, 7 → 3+2+2, 8 → 3+3+2, 9 → 3+3+3, 10 → 3+3+2+2.
    """
    n = len(queries)
    if n <= MAX_QUERIES_PER_GROUP:
        return [list(queries)] if queries else []
    # The fewest groups (ceil(n/3)), every group 2 or 3, the 3s first.
    groups_count = -(-n // MAX_QUERIES_PER_GROUP)
    threes = n - 2 * groups_count
    sizes = [3] * threes + [2] * (groups_count - threes)
    out: list[list[str]] = []
    start = 0
    for size in sizes:
        out.append(list(queries[start : start + size]))
        start += size
    return out


# ── clean ──────────────────────────────────────────────────────────────────────

_IMAGE_MD = re.compile(r"!\[[^\]\n]*\]\([^)\n]*\)")
_IMAGE_HTML = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
_LINK_MD = re.compile(r"\[([^\]\n]*)\]\(([^)\s\n]+)(?:\s+\"[^\"\n]*\")?\)")
_BLANK_RUN = re.compile(r"\n[ \t]*(?:\n[ \t]*){2,}")
_TRAILING_WS = re.compile(r"[ \t]+\n")


def clean_page_text(text: str) -> str:
    """Image markup removed, a link URL shown once (later links keep their text), blank runs collapsed."""
    out = _IMAGE_HTML.sub("", _IMAGE_MD.sub("", text or ""))
    seen: set[str] = set()

    def _link(m: re.Match[str]) -> str:
        label, url = m.group(1), m.group(2)
        if url in seen:
            return label
        seen.add(url)
        return m.group(0)

    out = _LINK_MD.sub(_link, out)
    out = _TRAILING_WS.sub("\n", out)
    out = _BLANK_RUN.sub("\n\n", out)
    return out.strip()


# ── dedupe ─────────────────────────────────────────────────────────────────────

_TRACKING_PARAMS = re.compile(r"^(utm_[a-z]+|fbclid|gclid|mc_cid|mc_eid|ref|ref_src|amp|output)$", re.I)


def canonical_url(url: str) -> str:
    """One key per page: no scheme, no ``www.``, no ``/amp``, no tracking params, no trailing slash."""
    parts = urlsplit((url or "").strip())
    host = parts.netloc.lower()
    for prefix in ("www.", "amp."):
        if host.startswith(prefix):
            host = host[len(prefix) :]
    path = re.sub(r"/amp/?$", "", parts.path or "", flags=re.I)
    path = re.sub(r"\.amp(\.html?)?$", r"\1", path, flags=re.I).rstrip("/")
    query = urlencode(sorted((k, v) for k, v in parse_qsl(parts.query) if not _TRACKING_PARAMS.match(k)))
    return f"{host}{path}" + (f"?{query}" if query else "")


def body_fingerprint(text: str) -> str:
    """Near-identical bodies share this: lower-cased words only, hashed."""
    words = re.findall(r"[a-z0-9]+", (text or "").lower())
    return hashlib.sha1(" ".join(words).encode("utf-8")).hexdigest()


# ── page records ───────────────────────────────────────────────────────────────


@dataclass
class PagePlan:
    """One scraped page and everything done to it on its way to a condenser."""

    url: str
    title: str
    group: int
    query: str
    search_rank: int
    text: str
    date_info: str = ""
    chars_scraped: int = 0
    chars_clean: int = 0
    score: float = 0.0
    rank: int = 0
    capped: bool = False
    reduced: bool = False
    dropped: str | None = None
    duplicate_of: str | None = None
    #: The read judge's words when it could not settle the read ("possibly an interstitial (...)"): the page is
    #: kept and these words travel with it to the writer, the page record and the sources block.
    unsure: str = ""

    @property
    def chars_sent(self) -> int:
        return 0 if self.dropped else len(self.text)

    def record(self, counts: bool = True) -> dict[str, Any]:
        """The page's record; ``counts=False`` leaves the character counts out (the flags always stay)."""
        rec: dict[str, Any] = {
            "url": self.url,
            "title": self.title,
            "group": self.group,
            "rank_in_group": self.rank,
        }
        if counts:
            rec.update(
                chars_scraped=self.chars_scraped,
                chars_after_cleanup=self.chars_clean,
                chars_sent=self.chars_sent,
            )
        rec.update(
            capped=self.capped,
            reduced=self.reduced,
            full_text=f"web action='read' urls=['{self.url}']",
        )
        if self.dropped:
            rec["dropped"] = self.dropped
        if self.duplicate_of:
            rec["duplicate_of"] = self.duplicate_of
        if self.unsure:
            rec["unsure"] = self.unsure
        return rec


def dedupe_pages(pages: list[PagePlan]) -> tuple[list[PagePlan], list[PagePlan]]:
    """``(kept, duplicates)``: one page per canonical URL and per body fingerprint, the longer kept."""
    by_key: dict[str, PagePlan] = {}
    order: list[str] = []
    duplicates: list[PagePlan] = []
    fingerprints: dict[str, str] = {}
    for page in pages:
        key = canonical_url(page.url)
        fp = body_fingerprint(page.text)
        if fp in fingerprints and fingerprints[fp] != key:
            key = fingerprints[fp]
        current = by_key.get(key)
        if current is None:
            by_key[key] = page
            order.append(key)
            fingerprints[fp] = key
            continue
        keep, lose = (page, current) if len(page.text) > len(current.text) else (current, page)
        if keep is page:
            page.group, page.query = min((current.group, current.query), (page.group, page.query))
            page.search_rank = min(current.search_rank, page.search_rank)
        by_key[key] = keep
        fingerprints[fp] = key
        lose.duplicate_of = keep.url
        lose.dropped = "duplicate"
        duplicates.append(lose)
    return [by_key[k] for k in order], duplicates


# ── rank ───────────────────────────────────────────────────────────────────────

_STOPWORDS = frozenset(
    "the and for with from that this what which about into your their have has are was were "
    "will can how why who when where any all each every list note quote site com www http https "
    "his her its our you they them than then also only more most other such like just over".split()
)


def query_terms(*texts: str) -> set[str]:
    """Distinct content words (3+ letters, no stopwords) of the group's queries and instructions."""
    terms: set[str] = set()
    for text in texts:
        for word in re.findall(r"[a-z0-9]+", (text or "").lower()):
            if len(word) >= 3 and word not in _STOPWORDS:
                terms.add(word)
    return terms


def score_page(title: str, text: str, search_rank: int, terms: set[str]) -> float:
    """Share of the terms the title and body carry (title weighs triple) plus a search-rank bonus."""
    if not terms:
        return 1.0 / (1 + search_rank)
    title_words = set(re.findall(r"[a-z0-9]+", (title or "").lower()))
    body_words: dict[str, int] = {}
    for word in re.findall(r"[a-z0-9]+", (text or "").lower()):
        if word in terms:
            body_words[word] = body_words.get(word, 0) + 1
    hits = 0.0
    for term in terms:
        if term in title_words:
            hits += 3.0
        count = body_words.get(term, 0)
        if count:
            hits += min(count, 5) / 5.0
    return hits / (4.0 * len(terms)) + 0.5 / (1 + search_rank)


# ── cap + budget ───────────────────────────────────────────────────────────────


def cap_marker(kept: int, total: int) -> str:
    return f"[Page capped: {kept:,} of {total:,} characters kept]"


def reduce_marker(kept: int, total: int) -> str:
    return f"[Page reduced to fit this report's budget: {kept:,} of {total:,} characters kept]"


def cap_page_text(text: str, limit: int) -> tuple[str, bool]:
    """The head of the page within ``limit`` characters, the marker line saying so; ``(text, capped)``."""
    if len(text) <= limit:
        return text, False
    return f"{text[:limit].rstrip()}\n{cap_marker(limit, len(text))}", True


def fit_group_budget(pages: list[PagePlan], budget: int, floor: int) -> list[dict[str, Any]]:
    """Bring the group's page text within ``budget`` by the declared cut order; return the reductions.

    Cut order: lowest score first, largest first among equal scores; each page to ``floor``
    before a higher-ranked page loses anything; then pages are dropped to listing-only, lowest
    score first. Never a cut of the assembled text's tail.
    """
    reductions: list[dict[str, Any]] = []
    live = [p for p in pages if not p.dropped]
    total = sum(len(p.text) for p in live)
    if total <= budget:
        return reductions
    cut_order = sorted(live, key=lambda p: (p.score, -len(p.text)))
    for page in cut_order:
        if total <= budget:
            break
        size = len(page.text)
        if size <= floor:
            continue
        original = page.chars_clean or size
        # The marker line rides inside the page's share, so the cut makes room for it too.
        marker_room = len(reduce_marker(size, original)) + 1
        target = max(floor - marker_room, size - (total - budget) - marker_room)
        if target >= size - marker_room:
            continue
        kept = page.text[:target].rstrip()
        page.text = f"{kept}\n{reduce_marker(len(kept), original)}"
        page.reduced = True
        total += len(page.text) - size
        reductions.append({"url": page.url, "action": "reduced", "from_chars": size, "to_chars": len(page.text)})
    for page in cut_order:
        if total <= budget:
            break
        total -= len(page.text)
        reductions.append({"url": page.url, "action": "dropped_to_listing", "from_chars": len(page.text), "to_chars": 0})
        page.dropped = "over the report budget: listing only"
    return reductions


# ── listings ───────────────────────────────────────────────────────────────────


def build_listings(
    queries_with_results: list[tuple[str, dict[str, Any] | None]],
    read_urls: set[str],
) -> list[dict[str, Any]]:
    """One entry per query: its results in search order, each saying whether it was read in full."""
    read_keys = {canonical_url(u) for u in read_urls}
    listings: list[dict[str, Any]] = []
    for query, result in queries_with_results:
        result = result or {}
        combined = (result.get("web") or {}).get("results", []) + (result.get("news") or {}).get("results", [])
        rows: list[dict[str, Any]] = []
        for idx, r in enumerate(combined, 1):
            url = r.get("url")
            if not url:
                continue
            snippet = " ".join(
                s for s in [r.get("description") or "", *(r.get("extra_snippets") or [])] if isinstance(s, str) and s
            )
            row: dict[str, Any] = {
                "rank": idx,
                "title": r.get("title") or "",
                "url": url,
                "snippet": re.sub(r"<[^>]+>", "", snippet),
                "read": "read in full" if canonical_url(url) in read_keys else NOT_READ_LABEL,
            }
            if r.get("age") or r.get("page_age"):
                row["age"] = r.get("age") or r.get("page_age")
            rows.append(row)
        listings.append({"query": query, "result_count": len(rows), "results": rows})
    return listings


def render_listings_text(listings: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for entry in listings:
        parts.append(f'## "{entry["query"]}" ({entry.get("result_count", len(entry["results"]))} results)\n')
        for row in entry["results"]:
            age = f" ({row['age']})" if row.get("age") else ""
            parts.append(
                f"{row['rank']}. Title: {row['title']}{age}\nURL: {row['url']}\n[{row['read']}]\n{row.get('snippet', '')}\n"
            )
    return "\n".join(parts)


def compact_listings(listings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The listings the result carries by default: rank, title, link and the read label, no snippet or age."""
    return [
        {
            **{k: v for k, v in e.items() if k != "results"},
            "results": [{k: r[k] for k in ("rank", "title", "url", "read") if k in r} for r in e["results"]],
        }
        for e in listings
    ]


def listings_chars(listings: list[dict[str, Any]]) -> int:
    return len(render_listings_text(listings))


def trim_listings(listings: list[dict[str, Any]], limit: int) -> tuple[list[dict[str, Any]], int]:
    """Listings within ``limit`` rendered characters: lowest rank removed first, per query in turn.

    Returns ``(trimmed copy, results removed)``; the input is never mutated.
    """
    out = [{**e, "results": list(e["results"])} for e in listings]
    removed = 0
    while listings_chars(out) > limit and any(e["results"] for e in out):
        # The query holding the most results gives up its lowest-ranked one.
        entry = max(out, key=lambda e: len(e["results"]))
        entry["results"].pop()
        removed += 1
    return out, removed


# ── a group's condenser input ──────────────────────────────────────────────────

#: The fixed characters of one page's header in ``GroupPlan.scraped_content``.
_PAGE_HEADER_CHARS = len("[Page 100]\nTitle: \nUrl: \nContent:\n\n\n---\n") + 1


@dataclass
class GroupPlan:
    """One condense: its queries, its pages in rank order, and what was done to fit them."""

    index: int
    queries: list[str]
    pages: list[PagePlan] = field(default_factory=list)
    reductions: list[dict[str, Any]] = field(default_factory=list)
    listings: list[dict[str, Any]] = field(default_factory=list)
    listings_removed: int = 0
    #: ``(url, reason)`` of every page of the run that failed to load; told to the writer, listed in the report.
    failed_sources: list[tuple[str, str]] = field(default_factory=list)

    def scraped_content(self, *, with_run_facts: bool = True) -> str:
        """The pages sent, best first; led by the run-facts block (the condenser agents declare no
        separate variable for it yet, so it rides here, delimited, never mixed into page text)."""
        parts: list[str] = []
        if with_run_facts:
            parts.append(f"{RUN_FACTS_OPEN}\n{self.run_facts()}\n{RUN_FACTS_CLOSE}\n")
        for page in self.pages:
            if page.dropped:
                continue
            parts.append(
                f"{page_marker(page.rank)}\nTitle: {page.title}\nUrl: {page.url}\n{page.date_info}Content:\n{page.text}\n\n---\n"
            )
        return "\n".join(parts)

    def search_results(self) -> str:
        return render_listings_text(self.listings)

    def run_facts(self) -> str:
        """What the condenser must know about its own input: capped, reduced and listing-only pages."""
        lines = [f"Report group {self.index}: queries {', '.join(repr(q) for q in self.queries)}."]
        lines.append(f"{sum(1 for p in self.pages if not p.dropped)} page(s) sent in full or in part.")
        for page in self.pages:
            if page.dropped:
                lines.append(f"- NOT SENT ({page.dropped}): {page.url}")
            elif page.reduced:
                lines.append(f"- REDUCED to {len(page.text):,} of {page.chars_clean:,} characters: {page.url}")
            elif page.capped:
                lines.append(f"- CAPPED to {len(page.text):,} of {page.chars_clean:,} characters: {page.url}")
            if page.unsure and not page.dropped:
                lines.append(f"- UNSURE READ, {page.unsure}: {page.url} (say so if you rely on it)")
        for url, reason in unique_failed(self.failed_sources):
            lines.append(f"- FAILED TO LOAD, nothing was read from it ({reason}): {url}")
        if self.failed_sources:
            lines.append(
                "Nothing may be attributed to a page that failed to load, or to that site's community, forum, "
                "comments or benchmarks: no claim, quote, statistic or paraphrase. If a failed source matters "
                "to the question, say plainly that it could not be read."
            )
        if self.listings_removed:
            lines.append(f"- {self.listings_removed} lowest-ranked search listing(s) left out for size.")
        lines.append(
            "Search listings marked 'not read: search snippet only' were never opened: never present a "
            "snippet as a page that was read. Say when a capped or reduced page may hold more."
        )
        return "\n".join(lines)

    def chars(self) -> dict[str, int]:
        return {
            "scraped_content": len(self.scraped_content()),
            "pages_only": len(self.scraped_content(with_run_facts=False)),
            "search_results": len(self.search_results()),
        }

    def record(self, counts: bool = True) -> dict[str, Any]:
        rec: dict[str, Any] = {
            "group": self.index,
            "queries": self.queries,
            "pages_sent": sum(1 for p in self.pages if not p.dropped),
            "pages_listing_only": sum(1 for p in self.pages if p.dropped),
        }
        if counts:
            rec["chars_sent"] = self.chars()
            rec["reductions"] = self.reductions
        rec["listings_left_out"] = self.listings_removed
        return rec


@dataclass
class Budgets:
    page_max_chars: int = PAGE_MAX_CHARS
    condense_max_chars: int = CONDENSE_MAX_CHARS
    listings_max_chars: int = LISTINGS_MAX_CHARS
    fallback_max_chars: int = FALLBACK_MAX_CHARS
    page_floor_chars: int = PAGE_FLOOR_CHARS
    #: How much of the search listings the RESULT carries: 0 none, 1 compact, 2 full (the condenser always gets full).
    listings_detail: int = LISTINGS_DETAIL
    #: 1 puts per-page and per-cut character counts in the result; 0 leaves them out.
    page_char_counts: int = PAGE_CHAR_COUNTS

    def record(self) -> dict[str, int]:
        return dict(self.__dict__)


def plan_groups(
    *,
    queries: list[str],
    instructions: str,
    listings: list[dict[str, Any]],
    pages: list[dict[str, Any]],
    budgets: Budgets,
    max_pages_per_query: int | None = None,
) -> tuple[list[GroupPlan], list[PagePlan]]:
    """The condenser input for every group, and every page record (sent, reduced, dropped, duplicate).

    ``pages`` are scraper page dicts (``url``, ``title``, ``content``, ``date_info``, optional
    ``query``). A page belongs to the group of the first query (caller's order) whose listing
    holds it; a page no listing holds stays with the query that scraped it.
    """
    groups = [GroupPlan(index=i + 1, queries=g) for i, g in enumerate(group_queries(queries))]
    group_of_query = {q: g.index for g in groups for q in g.queries}
    first_listing: dict[str, tuple[str, int]] = {}
    for q in queries:
        for entry in listings:
            if entry["query"] != q:
                continue
            for row in entry["results"]:
                first_listing.setdefault(canonical_url(row["url"]), (q, row["rank"]))

    plans: list[PagePlan] = []
    for raw in pages:
        url = raw.get("url") or raw.get("requested_url") or ""
        found = first_listing.get(canonical_url(url)) or first_listing.get(canonical_url(raw.get("requested_url") or ""))
        query, search_rank = found if found else (raw.get("query") or (queries[0] if queries else ""), 99)
        content = raw.get("content") or ""
        cleaned = clean_page_text(content)
        plans.append(
            PagePlan(
                url=url,
                title=raw.get("title") or "",
                group=group_of_query.get(query, 1),
                query=query,
                search_rank=search_rank,
                text=cleaned,
                date_info=raw.get("date_info") or "",
                chars_scraped=len(content),
                chars_clean=len(cleaned),
                unsure=raw.get("unsure") or "",
            )
        )

    kept, duplicates = dedupe_pages(plans)
    for g in groups:
        terms = query_terms(*g.queries, instructions)
        members = [p for p in kept if p.group == g.index]
        for p in members:
            p.score = score_page(p.title, p.text, p.search_rank, terms)
        members.sort(key=lambda p: (-p.score, p.search_rank))
        limit = max_pages_per_query * len(g.queries) if max_pages_per_query else None
        for i, p in enumerate(members, 1):
            p.rank = i
            if limit is not None and i > limit:
                p.dropped = "over the page count for this research depth: listing only"
                continue
            p.text, p.capped = cap_page_text(p.text, budgets.page_max_chars)
        g.pages = members
        group_listings = [e for e in listings if e["query"] in g.queries]
        g.listings, g.listings_removed = trim_listings(group_listings, budgets.listings_max_chars)
        # The budget bounds the rendered scraped_content: page headers and the run-facts block
        # count too. Fit the pages, then shrink their share by whatever is still over (the facts
        # grow with each reduction they name) — a few passes settle it.
        overhead = sum(_PAGE_HEADER_CHARS + len(p.title) + len(p.url) + len(p.date_info) for p in members if not p.dropped)
        page_budget = max(budgets.condense_max_chars - overhead, 0)
        g.reductions = fit_group_budget(members, page_budget, budgets.page_floor_chars)
        for _ in range(4):
            over = len(g.scraped_content()) - budgets.condense_max_chars
            if over <= 0:
                break
            page_budget = max(page_budget - over, 0)
            g.reductions += fit_group_budget(members, page_budget, budgets.page_floor_chars)
    return groups, kept + duplicates


def fallback_pages(group: GroupPlan, limit: int) -> list[dict[str, Any]]:
    """A failed group's top-ranked page text within ``limit`` characters, in rank order."""
    out: list[dict[str, Any]] = []
    room = limit
    for page in group.pages:
        if page.dropped or room <= 0:
            continue
        text, cut = cap_page_text(page.text, room)
        out.append({"url": page.url, "title": page.title, "text": text, "cut_to_fit": cut})
        room -= len(text)
    return out


# ── the report's citations, checked against what was read ──────────────────────
#
# The pages handed to the writer are labelled BY CODE with ONE distinctive marker (``⟦P3⟧``), the writer is
# asked (by the condenser agents' own definitions) to cite with exactly that marker, and the code rewrites
# ONLY that marker form (plus the two legacy literal spellings an owner saw: ``[Page N]`` and ``[cite: N]``)
# to an inline URL. Nothing else in the text is ever touched: no bare ``[N]``, ``^N``, ``(Page N)``, no
# spelled-out number. Guessing citation shapes in free prose silently corrupted maths and code ("20 m^2",
# "array[1]"), so that mechanism is gone (fix round 2, 2026-11-17).
#
#   a. a marker of a page this run read becomes an inline URL; a marker of a page NOT read is removed WITH a note;
#   b. a URL (or markdown link) in the text that was not read is replaced by a removal note;
#   c. the writer is told at writing time which sources failed to load (``GroupPlan.run_facts``);
#   d. the sources block is written once per tool result by code (:func:`sources_block`).

#: Why ``⟦P3⟧`` is collision-safe: U+27E6 / U+27E7 (mathematical white square brackets) appear in no ordinary
#: prose, source code, shell, markup or the plain maths this tool reports (``m^2``, ``E=mc^2``, ``a[1]``, ``(Page 1)``);
#: the ``P`` + digits inside them is a form no denotation-bracket use writes; and the characters are not in any
#: URL, so the unread-URL check never sees one.
MARKER_OPEN = "\u27e6"
MARKER_CLOSE = "\u27e7"


def page_marker(rank: int) -> str:
    """The one marker form that labels page ``rank`` and that the writer cites it by."""
    return f"{MARKER_OPEN}P{rank}{MARKER_CLOSE}"

_DIGITS = r"[0-9]+"
#: A page number as the code writes it: no leading zero (``[Page 007]`` is ordinary text, never page 7).
_PAGE_NO = r"[1-9][0-9]*"
_LIST = rf"{_PAGE_NO}(?:\s*,\s*{_PAGE_NO})*"
#: The marker (any digits: a marker the code did not assign, ``\u27e6P01\u27e7``, is removed with a note), then the two
#: legacy literal spellings (exactly these; N digits, optional comma list).
_ONE_MARKER = rf"{MARKER_OPEN}P{_DIGITS}{MARKER_CLOSE}"
_ONE_LEGACY = rf"\[Page {_LIST}\]|\[cite: {_LIST}\]"
_ONE_CITATION = rf"(?:{_ONE_MARKER}|{_ONE_LEGACY})"
#: A run of adjacent citations (only spaces between them) becomes ONE inline citation, so a
#: repeated marker never yields ``(url)(url)``.
_CITATION_RUN = re.compile(rf"{_ONE_CITATION}(?: *{_ONE_CITATION})*")
_MARKER_RUN = re.compile(rf"{_ONE_MARKER}(?: *{_ONE_MARKER})*")
_RUN_PART = re.compile(rf"{MARKER_OPEN}P({_DIGITS}){MARKER_CLOSE}|\[Page ({_LIST})\]|\[cite: ({_LIST})\]")
#: Quotation the writer copied (where a page's own "[Page 2]" can appear): code fences, inline code, blockquote
#: lines and one-line double-quoted spans. The legacy literal forms are rewritten only OUTSIDE these; the
#: code-assigned marker is rewritten everywhere (no page text carries it).
_QUOTED = re.compile(r"```.*?```|`[^`\n]*`|^[ \t]*>[^\n]*|\"[^\"\n]*\"|\u201c[^\u201d\n]*\u201d", re.S | re.M)
_URL = re.compile(r"https?://[^\s)\]>\"']+")
_MD_LINK = re.compile(r"\[([^\]\n]*)\]\((https?://[^)\s\n]+)(?:\s+\"[^\"\n]*\")?\)")
#: Sites whose pages are written by their users, never by the vendor of the product discussed. A fact about
#: who authors a site's pages, used only to LABEL a source, never to remove or rewrite anything: not an
#: organization's judgment call, so not a knob (it errs open: a site missing here is simply not labelled).
_USER_CONTENT_HOSTS = frozenset({"reddit", "quora", "stackoverflow", "stackexchange", "medium", "ycombinator", "wikipedia"})
_TWO_PART_SUFFIXES = frozenset({"co", "com", "org", "net", "gov", "ac"})


def host_label(url: str) -> str:
    """The name part of a URL's host: ``old.reddit.com`` -> ``reddit``, ``bbc.co.uk`` -> ``bbc``."""
    host = (urlsplit((url or "").strip()).hostname or "").lower()
    parts = [p for p in host.split(".") if p]
    if len(parts) >= 3 and parts[-2] in _TWO_PART_SUFFIXES and len(parts[-1]) == 2:
        return parts[-3]
    return parts[-2] if len(parts) >= 2 else (parts[0] if parts else "")


def is_vendor_source(url: str, terms_text: str) -> bool:
    """True when the page's site is the publisher of something the queries or instructions discuss."""
    label = host_label(url)
    if len(label) < 4 or label in _USER_CONTENT_HOSTS:
        return False
    words = set(re.findall(r"[a-z0-9]+", (terms_text or "").lower()))
    return label in words or (len(label) >= 6 and any(label in w for w in words))


def _numbers(raw: str) -> list[int]:
    """Every page number a marker body names (``1, 2`` is 1 and 2)."""
    return [int(n) for n in re.findall(_DIGITS, raw)]


def _run_numbers(run: str) -> list[tuple[str, int | None]]:
    """``(as written, page number)`` for each page a citation run names; ``None`` for a marker the code never
    assigns (a leading zero), so it is removed with a note rather than guessed."""
    out: list[tuple[str, int | None]] = []
    for m in _RUN_PART.finditer(run):
        if m.group(1) is not None:
            raw = m.group(1)
            out.append((raw, int(raw) if raw == str(int(raw)) else None))
        else:
            out += [(n, int(n)) for n in re.findall(_DIGITS, m.group(2) or m.group(3))]
    return out


def unique_failed(failed: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """One row per URL, first reason kept, in order."""
    seen: set[str] = set()
    out: list[tuple[str, str]] = []
    for url, why in failed:
        if url and canonical_url(url) not in seen:
            seen.add(canonical_url(url))
            out.append((url, why))
    return out


def sources_block(
    read: list[tuple[str, bool]] | list[tuple[str, bool, str]],
    failed: list[tuple[str, str]],
) -> str:
    """The deterministic block every report ends with: ``read`` is ``(url, vendor_authored[, unsure words])``,
    ``failed`` is ``(url, reason)``. Written by code from the run's facts, never by the model."""
    lines = ["---", f"Sources read ({len(read)}):"]
    for row in read:
        url, vendor, unsure = (*row, "")[:3]
        notes = [n for n in ("vendor-authored" if vendor else "", unsure) if n]
        lines.append(f"- {url}{''.join(f' ({n})' for n in notes)}")
    if not read:
        lines.append("- none")
    lines.append(f"Sources that failed to load ({len(failed)}):")
    lines += [f"- {u} ({why})" if why else f"- {u}" for u, why in failed] or ["- none"]
    return "\n".join(lines)


def verify_report(
    report: str,
    *,
    read_pages: list[PagePlan],
    terms_text: str,
    run_read_urls: list[str] | None = None,
) -> tuple[str, dict[str, Any]]:
    """The report with every citation an inline URL checked against what this run read.

    ``read_pages`` are the group's pages the condenser was sent (their ``rank`` is the ``Page N`` it saw);
    ``run_read_urls`` every page read anywhere in the run (defaults to the group's); ``terms_text`` the queries and instructions, which
    name the product a vendor page may be about.

    1. Every page marker (``⟦P3⟧``, and the legacy ``[Page 3]`` / ``[cite: 3, 4]``) becomes ``(url)``
       (``(url, vendor-authored)`` for a page written by the vendor of what is discussed); a marker of a page
       that was not read becomes a visible removal note. No other text is read as a citation.
    2. A URL (or markdown link) in the text that was not read is replaced by a removal note.
    The sources block is NOT added here: it is written once per tool result (:func:`sources_block`).
    Prose is never judged: no sentence is removed for what it says. Returns ``(text, record)``.
    """
    by_rank = {p.rank: p for p in read_pages if not p.dropped}
    read_keys = {canonical_url(p.url) for p in read_pages if not p.dropped}
    read_keys |= {canonical_url(u) for u in (run_read_urls or [])}
    record: dict[str, Any] = {
        "removed_citations": [], "vendor_sources": [], "cited": [],
    }

    def _cite(run: str) -> str:
        urls: list[str] = []
        notes: list[str] = []
        for raw, n in _run_numbers(run):
            page = by_rank.get(n) if n is not None else None
            if page is None:
                record["removed_citations"].append({"cited": raw, "marker": run})
                note = f"[citation removed: page {raw} was not read in this run]"
                if note not in notes:
                    notes.append(note)
                continue
            vendor = is_vendor_source(page.url, terms_text)
            if vendor and page.url not in record["vendor_sources"]:
                record["vendor_sources"].append(page.url)
            if page.url not in record["cited"]:
                record["cited"].append(page.url)
            label = f"{page.url}, vendor-authored" if vendor else page.url
            if label not in urls:
                urls.append(label)
        return " ".join(([f"({'; '.join(urls)})"] if urls else []) + notes)

    # Legacy literal forms only outside quotation; the code-assigned marker everywhere.
    pieces: list[str] = []
    last = 0
    for q in _QUOTED.finditer(report):
        pieces.append(_CITATION_RUN.sub(lambda m: _cite(m.group(0)), report[last:q.start()]))
        pieces.append(_MARKER_RUN.sub(lambda m: _cite(m.group(0)), q.group(0)))
        last = q.end()
    pieces.append(_CITATION_RUN.sub(lambda m: _cite(m.group(0)), report[last:]))
    report = "".join(pieces)

    def _removed(url: str, marker: str, text: str = "") -> str:
        record["removed_citations"].append({"cited": url, "marker": marker})
        return f"{text + ' ' if text else ''}[citation removed: {urlsplit(url).hostname or url} was not read in this run]"

    def _link(m: re.Match[str]) -> str:
        url = m.group(2).rstrip(".,;:")
        return m.group(0) if canonical_url(url) in read_keys else _removed(url, m.group(0), m.group(1).strip())

    report = _MD_LINK.sub(_link, report)

    def _url(m: re.Match[str]) -> str:
        raw = m.group(0)
        url = raw.rstrip(".,;:")
        if canonical_url(url) in read_keys:
            return raw
        return _removed(url, url) + raw[len(url):]

    report = _URL.sub(_url, report)
    report = report.rstrip()
    record["coverage"] = citation_coverage(report, read_keys)
    return report, record


def citation_coverage(report: str, read_keys: set[str]) -> dict[str, int]:
    """The two plain facts a consumer can test without interpretation: how many DISTINCT pages read in this run the
    report cites (``read_pages_cited``, counted on the checked report, where every resolved citation is an inline URL)
    and how many pages were read (``pages_read``). Prose is never judged, so nothing is said about which sentences
    carry a source."""
    cited = {canonical_url(m.group(0).rstrip(".,;:")) for m in _URL.finditer(report or "")} & read_keys
    return {"read_pages_cited": len(cited), "pages_read": len(read_keys)}


def citation_notice(coverage: dict[str, int]) -> str:
    """The line written by code at the top of a report that cites none of the pages read, or ``""``."""
    if coverage.get("read_pages_cited") == 0:
        return "[Uncited report: it cites none of the pages read in this run, so no statement below is tied to a source.]"
    return ""
