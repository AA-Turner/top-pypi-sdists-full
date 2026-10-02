"""Coverage monitoring — pure logic. No DB, no HTTP, no LLM.

A **tracker** is a saved search: *"tell me when anyone writes about this brand,
and about these competitors."* A **mention** is one article that matched it.
This module owns everything about that relationship that can be decided without
touching the world: how a candidate is deduped (on the platform's one article
key, ``matrx_scraper.canonical.story_url_key``), whether an
article is about the brand or a competitor, what medium it is, and — once our
crawler and the analyst have done their work — how loud the mention is
(`hit_score`) and how the brand is doing against its competitors
(`share_of_voice`).

## The doctrines this module encodes

**ABSENCE IS NEVER LOSS.** A pass that returns nothing means the index had
nothing to say, not that coverage disappeared. Nothing here can mark a mention
gone, and no function infers a negative from silence.

**Discovery is not content.** GDELT hands us a URL and a headline. Every fact
with any weight — the body, the byline, the publication date, whether the piece
links to us — comes from our own crawl of the page. So a mention has a
`capture_status` lifecycle (`pending` → `captured`/`failed`/`blocked`) and its
analysis fields stay NULL until the page is actually read. NULL means
unmeasured; it never means zero.

**Podcasts and newsletters match on title/description only.** No transcript
vendor (Podscan is $5k/mo, D5) and no home-grown STT. A podcast episode page
whose title mentions the brand is a real, honest mention of the brand; claiming
to know what was said in the audio would not be.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from datetime import datetime
from typing import Literal
from urllib.parse import urlsplit

from matrx_scraper.canonical import story_url_key
from pydantic import BaseModel, ConfigDict, Field

from matrx_seo.identity import stable_hash

#: HOW we found the page — not where its content came from. Every weighted fact
#: on a mention comes from our own crawl regardless of the channel that surfaced
#: it: a news source (GDELT, Google News search, Brave news, a feed, Hacker News,
#: Reddit, X — the news engine's provider registry names which), a direct crawl, a
#: human paste, or an AI answer engine citing it (the AI-visibility panel, WP4
#: step 5). Exactly the ``seo.coverage_mention.source`` CHECK; a guard test keeps
#: the two equal (NEWS-ENGINE-SPEC §4.2).
MentionSource = Literal[
    "gdelt",
    "crawl",
    "manual",
    "ai_visibility",
    "google_news",
    "feed",
    "hackernews",
    "reddit",
    "brave",
    "x",
]
CaptureStatus = Literal["pending", "captured", "failed", "blocked", "skipped"]
Sentiment = Literal["positive", "neutral", "negative", "mixed"]
Prominence = Literal["headline", "lede", "body", "passing"]
Medium = Literal["news", "blog", "podcast", "newsletter", "video", "forum", "other"]

#: Substrings in a URL path/host that identify the MEDIUM of a page. Title and
#: description only — never a transcript, never an audio fetch (D5).
_PODCAST_MARKERS = (
    "podcasts.apple.com",
    "podcast",
    "/episode",
    "/episodes/",
    "spotify.com/episode",
    "buzzsprout",
    "libsyn",
    "megaphone.fm",
    "transistor.fm",
    "simplecast",
    "captivate.fm",
)
_NEWSLETTER_MARKERS = (
    "substack.com",
    "beehiiv.com",
    "ghost.io",
    "mailchi.mp",
    "campaign-archive.com",
    "buttondown",
    "/newsletter",
    "convertkit",
)
_VIDEO_MARKERS = ("youtube.com/watch", "youtu.be/", "vimeo.com/")
_FORUM_MARKERS = ("reddit.com/r/", "news.ycombinator.com", "quora.com", "/forum")
_BLOG_MARKERS = ("/blog/", "medium.com/", "dev.to/", "wordpress.com")

#: Hit score weights. Deterministic and explainable on purpose (D11): a PR score
#: nobody can read is a number nobody trusts. Every component is capped so no
#: single dimension can carry a score on its own.
HIT_PROMINENCE_POINTS: dict[str, int] = {
    "headline": 40,
    "lede": 28,
    "body": 14,
    "passing": 6,
}
HIT_SENTIMENT_POINTS: dict[str, int] = {
    "positive": 20,
    "mixed": 8,
    "neutral": 6,
    "negative": 0,
}
#: A piece that links to you is worth more than one that only names you — it is
#: the difference between a mention and an asset.
HIT_LINKED_POINTS = 20
#: Authority of the outlet, from the SAME Matrx Authority Score the prospecting
#: side uses (0-100 → 0-20). Unmeasured contributes nothing and never guesses.
HIT_AUTHORITY_MAX_POINTS = 20


def domain_of(url: str) -> str:
    """The article's host as a story key spells it (lower-cased, no ``www.``)."""
    return urlsplit(story_url_key(url)).hostname or ""


def mention_dedupe_key(tracker_id: str, normalized_url: str) -> str:
    """One row per tracker per article, whichever source found it first.

    Keyed on the tracker (not the site) because two trackers on one site can
    legitimately both want the same article — a brand tracker and a competitor
    tracker watching an outlet that covered both.
    """
    return f"coverage:{tracker_id}:{stable_hash(normalized_url)[:32]}"


def detect_medium(url: str, title: str = "") -> Medium:
    """What KIND of place published this. Title/description evidence only."""
    haystack = f"{url.lower()} {title.lower()}"
    if any(marker in haystack for marker in _PODCAST_MARKERS):
        return "podcast"
    if any(marker in haystack for marker in _NEWSLETTER_MARKERS):
        return "newsletter"
    if any(marker in haystack for marker in _VIDEO_MARKERS):
        return "video"
    if any(marker in haystack for marker in _FORUM_MARKERS):
        return "forum"
    if any(marker in haystack for marker in _BLOG_MARKERS):
        return "blog"
    return "news"


class CompetitorTerm(BaseModel):
    """A rival the tracker also watches, so share-of-voice has a denominator."""

    model_config = ConfigDict(extra="forbid")

    key: str
    terms: list[str] = Field(default_factory=list)


class TrackerSpec(BaseModel):
    """A saved search, reduced to what pure logic needs."""

    model_config = ConfigDict(extra="forbid")

    tracker_id: str
    brand_key: str
    brand_terms: list[str] = Field(default_factory=list)
    exclude_terms: list[str] = Field(default_factory=list)
    competitors: list[CompetitorTerm] = Field(default_factory=list)
    language: str | None = None
    country: str | None = None
    #: Domains the tracker should ignore entirely (the brand's own site is the
    #: usual one — a company writing about itself is not coverage).
    ignore_domains: list[str] = Field(default_factory=list)


class SourceMatch(BaseModel):
    """What the DISCOVERY source already matched, and on whose behalf.

    A discovery index searches the whole article; we only ever see a headline.
    This carries that fact forward so the classifier does not re-filter what has
    already been filtered — see `classify_candidate`.
    """

    model_config = ConfigDict(extra="forbid")

    terms: list[str] = Field(default_factory=list)
    #: None = the brand's own query returned it; otherwise the rival's key.
    competitor_key: str | None = None


class MentionCandidate(BaseModel):
    """A discovered article, before our crawler has read it."""

    model_config = ConfigDict(extra="forbid")

    tracker_id: str
    source: MentionSource
    url: str
    normalized_url: str
    domain: str
    title: str = ""
    language: str = ""
    medium: Medium = "news"
    discovered_at: datetime
    #: Which side of the share-of-voice ledger this lands on.
    is_competitor: bool = False
    competitor_key: str | None = None
    #: Which of the tracker's terms actually matched, for the evidence drawer.
    matched_terms: list[str] = Field(default_factory=list)
    dedupe_key: str = ""
    external_id: str | None = None


def _term_pattern(term: str) -> re.Pattern[str] | None:
    words = term.strip().split()
    if not words:
        return None
    # Whole words only, any run of whitespace between them: "Arman" never matches "Armani",
    # "Green" never matches "Greenpeace", and "All Green  Recycling" still matches itself.
    body = r"\s+".join(re.escape(w) for w in words)
    return re.compile(r"(?<!\w)" + body + r"(?!\w)", re.IGNORECASE)


def term_hits(haystack: str, terms: Iterable[str]) -> list[str]:
    """The tracked terms that appear in ``haystack`` as WHOLE WORDS, case-insensitively.

    The one term matcher for coverage. A substring test is how a founder-name term "Arman"
    came to match "Giorgio Armani" — word boundaries are the fix for the whole class.
    """
    hits: list[str] = []
    for term in terms:
        pattern = _term_pattern(str(term))
        if pattern is not None and pattern.search(haystack or ""):
            hits.append(term)
    return hits



def classify_candidate(
    spec: TrackerSpec,
    *,
    url: str,
    title: str,
    source: MentionSource,
    discovered_at: datetime,
    language: str = "",
    external_id: str | None = None,
    extra_text: str = "",
    source_matched: SourceMatch | None = None,
) -> MentionCandidate | None:
    """Turn a discovered article into a candidate, or decline it with silence.

    Declines when: the URL is unusable, the domain is on the tracker's ignore
    list, an exclude term appears, or nothing the tracker watches is present in
    the evidence we have.

    ## `source_matched` — why re-matching the headline was WRONG

    The first live pass discovered ten real articles and produced zero
    candidates, because the discovery index matched the tracker's terms against
    the FULL TEXT of each article and this function then demanded the terms
    appear again in the headline or the URL. That is double-filtering: it throws
    away exactly the coverage that mentions you in the second paragraph, which
    is most of it.

    So when the caller can say *"the source already applied these terms, and it
    was the brand query / this competitor's query that returned it"*, the
    candidate is ACCEPTED on that basis and a local headline hit only enriches
    `matched_terms`. The name-collision case — a different company with the same
    name — is settled later by the analyst reading the actual page
    (`is_about_brand`), which is the only place it can honestly be settled.

    With no `source_matched`, the strict local rule still applies: that is the
    right behaviour for a manually pasted URL, where nothing has filtered
    anything.
    """
    try:
        # One article identity for the whole platform: the story key a news
        # sighting, a coverage mention and a same-story cluster all agree on.
        normalized = story_url_key(url)
    except ValueError:
        return None
    domain = domain_of(normalized)
    if not domain:
        return None
    ignored = {d.strip().lower().removeprefix("www.") for d in spec.ignore_domains}
    if domain in ignored:
        return None

    haystack = f"{title} {url} {extra_text}"
    if term_hits(haystack, spec.exclude_terms):
        return None

    brand_hits = term_hits(haystack, spec.brand_terms)
    competitor_key: str | None = None
    competitor_hits: list[str] = []
    for competitor in spec.competitors:
        hits = term_hits(haystack, competitor.terms or [competitor.key])
        if hits:
            competitor_key = competitor.key
            competitor_hits = hits
            break

    # The brand wins a tie: an article naming both is OUR coverage that happens
    # to mention a rival, and counting it for the rival would understate us.
    if brand_hits:
        matched, is_competitor, competitor_key = brand_hits, False, None
    elif competitor_hits:
        matched, is_competitor = competitor_hits, True
    elif source_matched is not None:
        # The index matched the full text; the query that returned it decides
        # the side. `matched_terms` records what the SOURCE matched, so the
        # evidence drawer never implies we read something we did not.
        is_competitor = source_matched.competitor_key is not None
        competitor_key = source_matched.competitor_key
        matched = list(source_matched.terms)
    else:
        return None

    return MentionCandidate(
        tracker_id=spec.tracker_id,
        source=source,
        url=url.strip(),
        normalized_url=normalized,
        domain=domain,
        title=title.strip(),
        language=language.strip(),
        medium=detect_medium(normalized, title),
        discovered_at=discovered_at,
        is_competitor=is_competitor,
        competitor_key=competitor_key,
        matched_terms=matched,
        dedupe_key=mention_dedupe_key(spec.tracker_id, normalized),
        external_id=external_id,
    )


class HitScore(BaseModel):
    model_config = ConfigDict(extra="forbid")

    score: int
    #: One sentence a non-technical expert can act on, plus the parts.
    reason: str
    components: dict[str, int] = Field(default_factory=dict)


def hit_score(
    *,
    prominence: str | None,
    sentiment: str | None,
    links_to_site: bool,
    authority: int | None = None,
) -> HitScore:
    """PR-Hit-Score-style priority, 0-100, fully explainable.

    Unmeasured inputs contribute ZERO POINTS and say so — never a midpoint
    guess, and never a filter: this ORDERS a feed, it never hides a row.
    """
    components: dict[str, int] = {}
    parts: list[str] = []

    prominence_points = HIT_PROMINENCE_POINTS.get(prominence or "", 0)
    components["prominence"] = prominence_points
    parts.append(f"it is in the {prominence}" if prominence else "we have not read the page yet")

    sentiment_points = HIT_SENTIMENT_POINTS.get(sentiment or "", 0)
    components["sentiment"] = sentiment_points
    if sentiment:
        parts.append(f"the tone toward you is {sentiment}")

    link_points = HIT_LINKED_POINTS if links_to_site else 0
    components["links_to_site"] = link_points
    parts.append("it links to your site" if links_to_site else "it does not link to you")

    authority_points = 0
    if authority is not None:
        authority_points = round(HIT_AUTHORITY_MAX_POINTS * max(0, min(100, authority)) / 100)
        parts.append(f"the outlet scores {authority} on authority")
    components["authority"] = authority_points

    total = max(0, min(100, sum(components.values())))
    return HitScore(
        score=total,
        reason=f"Scored {total} of 100 because " + ", ".join(parts) + ".",
        components=components,
    )


class VoiceShare(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str
    label: str
    mentions: int
    share_pct: float
    linked_mentions: int = 0
    avg_hit_score: int | None = None
    is_brand: bool = False


class ShareOfVoice(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_mentions: int
    entries: list[VoiceShare] = Field(default_factory=list)

    @property
    def brand_share_pct(self) -> float:
        return next((e.share_pct for e in self.entries if e.is_brand), 0.0)


#: Coverage verdicts that say a row is NOT a mention of whoever it was filed for: a different
#: entity with the same name, a junk page (a bot wall, an error page, a job listing), or a page we
#: could not read and so cannot confirm. Share of voice and every "stories about you" count exclude
#: them. A row with NO verdict yet is counted: competitor rows are never read by design (counted
#: from the index answer, cheapest-first), so excluding unjudged rows would count one side only.
NOT_A_MENTION_VERDICTS = frozenset({"wrong_entity", "junk", "uncertain"})


def counts_as_mention(verdict: str | None) -> bool:
    """Whether a coverage row counts as a real mention in share of voice and the tiles."""
    return (verdict or None) not in NOT_A_MENTION_VERDICTS


class VoiceRow(BaseModel):
    """The mention fields a rollup needs. Deliberately not the whole row."""

    model_config = ConfigDict(extra="forbid")

    is_competitor: bool
    competitor_key: str | None = None
    links_to_site: bool = False
    hit_score: int | None = None
    #: The row's coverage verdict; a not-a-mention verdict keeps the row out of the rollup.
    verdict: str | None = None


def share_of_voice(
    rows: list[VoiceRow], *, brand_key: str, brand_label: str | None = None
) -> ShareOfVoice:
    """Brand mentions vs each tracked competitor over the SAME window.

    A rollup, never a table (D-W4-1). Percentages are of the tracked set, and
    the tracked set is exactly what the user declared — this number answers
    "am I being written about more than them", not "what is my share of all
    news", which nobody can measure.
    """
    # Only real mentions: a wrong-entity match, a junk page or an unconfirmable page is not
    # someone writing about you, so it can never raise your share (or a rival's).
    rows = [row for row in rows if counts_as_mention(row.verdict)]
    buckets: dict[str, list[VoiceRow]] = {brand_key: []}
    for row in rows:
        key = (row.competitor_key or "unattributed") if row.is_competitor else brand_key
        buckets.setdefault(key, []).append(row)

    total = len(rows)
    entries: list[VoiceShare] = []
    for key, bucket in buckets.items():
        scored = [r.hit_score for r in bucket if r.hit_score is not None]
        entries.append(
            VoiceShare(
                key=key,
                label=(brand_label or brand_key) if key == brand_key else key,
                mentions=len(bucket),
                share_pct=round(100 * len(bucket) / total, 1) if total else 0.0,
                linked_mentions=sum(1 for r in bucket if r.links_to_site),
                avg_hit_score=round(sum(scored) / len(scored)) if scored else None,
                is_brand=key == brand_key,
            )
        )
    entries.sort(key=lambda e: (not e.is_brand, -e.mentions, e.key))
    return ShareOfVoice(total_mentions=total, entries=entries)


__all__ = [
    "HIT_AUTHORITY_MAX_POINTS",
    "HIT_LINKED_POINTS",
    "HIT_PROMINENCE_POINTS",
    "HIT_SENTIMENT_POINTS",
    "CaptureStatus",
    "CompetitorTerm",
    "HitScore",
    "Medium",
    "MentionCandidate",
    "MentionSource",
    "NOT_A_MENTION_VERDICTS",
    "Prominence",
    "Sentiment",
    "ShareOfVoice",
    "SourceMatch",
    "TrackerSpec",
    "VoiceRow",
    "VoiceShare",
    "classify_candidate",
    "counts_as_mention",
    "detect_medium",
    "domain_of",
    "hit_score",
    "mention_dedupe_key",
    "share_of_voice",
    "term_hits",
]
