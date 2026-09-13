from __future__ import annotations


from bs4 import BeautifulSoup


class MainContentFinder:
    """
    Finds the main content block of a page.

    Strategy:
    1. Try known CSS selectors (main, article, #content, etc.)
    2. Fall back to scoring all div/section/article/main blocks by text length
    3. Fall back to body
    """

    _DEFAULT_SELECTORS = [
        "main",
        "article",
        "#content",
        "#main-content",
        "div.wrapper",
        "div.content",
        "div#main",
        "div.main-content",
        "section.main-content",
        "div.article-body",
    ]
    _DEFAULT_BLOCKS = ["div", "section", "article", "main"]

    def __init__(
        self,
        override: bool = False,
        add_selectors: list[str] | None = None,
        remove_selectors: list[str] | None = None,
        add_blocks: list[str] | None = None,
        remove_blocks: list[str] | None = None,
        clear_selectors: bool = False,
    ):
        self.override = override
        base_selectors = [] if clear_selectors else list(self._DEFAULT_SELECTORS)
        self.selectors = self._build_list(base_selectors, add_selectors, remove_selectors)
        self.blocks = self._build_list(list(self._DEFAULT_BLOCKS), add_blocks, remove_blocks)

    def _build_list(
        self, base: list[str], add: list[str] | None, remove: list[str] | None
    ) -> list[str]:
        if not self.override:
            return base
        result = list(base)
        if add:
            result.extend(item for item in add if item not in result)
        if remove:
            result = [item for item in result if item not in remove]
        return result or base

    def find_main_content(self, soup: BeautifulSoup) -> BeautifulSoup:
        selected = []
        for selector in self.selectors:
            for item in soup.select(selector):
                selected.append(item)
                item.extract()

        if selected:
            combined = "".join(str(el) for el in selected)
            return BeautifulSoup(combined, "lxml")

        return self._score_blocks(soup)

    def _score_blocks(self, soup: BeautifulSoup) -> BeautifulSoup:
        blocks = soup.find_all(self.blocks)
        if not blocks:
            return soup.body or soup

        best = max(blocks, key=lambda b: len(b.get_text(strip=True)))
        return BeautifulSoup(str(best), "lxml")


# --------------------------------------------------------------------------
# THE MAIN-CONTENT LAW
#
# A page is not its article. Nav, sponsor lines, staff bios, tag lists,
# newsletter prompts, donate CTAs and "related" rails are the SITE's furniture
# and they are noise to every consumer that asked "what does this page SAY?" —
# an LLM handed the whole page reliably learns the furniture (2026-09-12: a
# Masterwork body-of-work lane distilled 20 Marshall Project articles into 416
# draft rules, a large share of which described the site's chrome).
#
# So the parser produces main content ONCE, here, and every consumer inherits
# it. The full page is never destroyed — it remains `text_data` for the callers
# that genuinely want the whole document (SEO audits, crawl diffing).
#
# Conservative by construction: when the page is not article-like, or when the
# candidate would be thinner than a real article, this returns None and the
# caller keeps the full page. It never returns a half-page and calls it
# an article.
# --------------------------------------------------------------------------

import re

from bs4 import Tag

from .knobs import parser_knob

# The four thresholds below are `platform.feature_knob` rows (feature
# knowledge.scraper); each constant is the package's standalone default and the
# host binds the live row through configure_parser_knobs (see ./knobs.py).
#: Below this the "article" we found is not worth preferring over the page.
#: KNOB MIRROR of platform.feature_knob "knowledge.scraper" "min_article_chars"
MIN_ARTICLE_CHARS = 500
#: A headline block outside the article body is pulled in only when it is small
#: relative to the body — a headline + dek, never a second column of chrome.
#: KNOB MIRROR of platform.feature_knob "knowledge.scraper" "max_headline_block_ratio"
MAX_HEADLINE_BLOCK_RATIO = 0.3
#: KNOB MIRROR of platform.feature_knob "knowledge.scraper" "max_headline_block_chars"
MAX_HEADLINE_BLOCK_CHARS = 1500
#: A candidate whose text is mostly anchor text is a nav/rail, not an article.
#: KNOB MIRROR of platform.feature_knob "knowledge.scraper" "max_link_text_ratio"
MAX_LINK_TEXT_RATIO = 0.55
#: On a listing page the biggest <article> is one card among many.
LISTING_DOMINANCE = 0.5

#: Ordered by how strongly each says "this is the story".
ARTICLE_ROOT_SELECTORS = (
    "article",
    "[role=article]",
    "[itemprop=articleBody]",
    ".article-body",
    ".article__body",
    ".story-body",
    ".post-content",
    ".entry-content",
    "main",
    "[role=main]",
    "#content",
    "#main-content",
)

#: Tags that are furniture wherever they appear inside an article root.
FURNITURE_TAGS = ("nav", "aside", "footer", "form", "noscript")

#: class/id SEGMENTS that mark furniture. Matched segment-wise (split on
#: non-alphanumerics), so "tags" matches `class="article-tags"` but never
#: `class="tagsoup-body"`... and never a substring inside another word.
FURNITURE_MARKERS = frozenset(
    {
        "ad",
        "ads",
        "advert",
        "advertisement",
        "sponsor",
        "sponsored",
        "sponsorship",
        "promo",
        "promotion",
        "donate",
        "donation",
        "membership",
        "subscribe",
        "subscription",
        "newsletter",
        "signup",
        "share",
        "sharing",
        "social",
        "related",
        "recirc",
        "recirculation",
        "recommended",
        "recommendations",
        "morefrom",
        "readmore",
        "tags",
        "taxonomy",
        "breadcrumb",
        "breadcrumbs",
        "comments",
        "disqus",
        "bio",
        "bios",
        "biography",
        "contributor",
        "contributors",
        "paywall",
        "popup",
        "modal",
        "cta",
        "toolbar",
        "sidebar",
        "masthead",
        "skip",
        # Wiki/CMS chrome — references apparatus, navboxes, category links,
        # edit affordances, tables of contents.
        "navbox",
        "navboxes",
        "catlinks",
        "reflist",
        "references",
        "refbegin",
        "editsection",
        "hatnote",
        "sistersitebox",
        "toc",
        "printfooter",
    }
)
#: Multi-segment phrases, matched as consecutive segments.
FURNITURE_PHRASES = (
    ("author", "bio"),
    ("staff", "bio"),
    ("more", "from"),
    ("read", "more"),
    ("sign", "up"),
    ("email", "signup"),
    ("email", "sign", "up"),
    ("support", "us"),
    ("back", "to", "top"),
    ("authority", "control"),
    ("external", "links"),
)


def _segments(token: str) -> list[str]:
    return [s for s in re.split(r"[^a-zA-Z0-9]+", str(token).lower()) if s]


def _text_len(node: Tag | None) -> int:
    return len(node.get_text(" ", strip=True)) if node is not None else 0


def _link_text_len(node: Tag) -> int:
    return sum(len(a.get_text(" ", strip=True)) for a in node.find_all("a"))


def _paragraph_text_len(node: Tag) -> int:
    return sum(len(p.get_text(" ", strip=True)) for p in node.find_all(["p", "blockquote"]))


def _furniture_reason(element: Tag) -> tuple[str, str] | None:
    """``(match_type, trigger_value)`` when this element is the site's
    furniture, else None. The pair is recorded on every removal — the SAME
    vocabulary the noise remover and content filter use, so one reader reads
    all three passes."""
    if element.name in FURNITURE_TAGS:
        return "tag", element.name
    if element.get("role") in {"navigation", "banner", "complementary", "contentinfo", "search"}:
        return "role", str(element["role"])
    tokens: list[str] = []
    if element.has_attr("id"):
        tokens.append(str(element["id"]))
    if element.has_attr("class"):
        tokens.extend(str(c) for c in element["class"])
    for token in tokens:
        segs = _segments(token)
        hit = set(segs) & FURNITURE_MARKERS
        if hit:
            return "segment", f"{sorted(hit)[0]} (in {token})"
        for phrase in FURNITURE_PHRASES:
            n = len(phrase)
            for i in range(len(segs) - n + 1):
                if tuple(segs[i : i + n]) == phrase:
                    return "phrase", f"{'-'.join(phrase)} (in {token})"
    return None


class ArticleContentFinder:
    """Readability-style main-content extraction for article-like pages.

    ``find(soup)`` returns a NEW soup holding the headline block plus the
    article body with its furniture stripped, or ``None`` when the page is not
    article-like. It never mutates the soup it is given.
    """

    def __init__(
        self,
        min_article_chars: int | None = None,
        selectors: tuple[str, ...] = ARTICLE_ROOT_SELECTORS,
    ):
        # None = the live knob (or the mirrored default standalone); a caller
        # that passes a number is deliberately overriding it for one find.
        self.min_article_chars = (
            int(parser_knob("min_article_chars", MIN_ARTICLE_CHARS))
            if min_article_chars is None
            else min_article_chars
        )
        self.selectors = selectors
        #: Populated by `find` — what was dropped and why, in the same shape the
        #: noise remover and content filter record, so nothing is silent.
        self.removal_details: list[dict[str, str | int]] = []
        self.root_selector: str | None = None

    # -- public ---------------------------------------------------------
    def find(self, soup: BeautifulSoup) -> BeautifulSoup | None:
        self.removal_details = []
        self.root_selector = None
        if soup is None:
            return None
        working = BeautifulSoup(str(soup), "lxml")
        root, selector = self._pick_root(working)
        if root is None:
            return None
        self._strip_furniture(root)
        if _text_len(root) < self.min_article_chars:
            return None
        headline = self._headline_block(working, root)
        self.root_selector = selector
        parts = ([str(headline)] if headline is not None else []) + [str(root)]
        return BeautifulSoup(f"<div>{''.join(parts)}</div>", "lxml")

    # -- internals ------------------------------------------------------
    def _pick_root(self, soup: BeautifulSoup) -> tuple[Tag | None, str | None]:
        body = soup.body or soup
        best: tuple[int, Tag, str] | None = None
        for selector in self.selectors:
            try:
                candidates = soup.select(selector)
            except Exception:
                continue
            scored = [(self._score(c), c) for c in candidates if isinstance(c, Tag)]
            scored = [(s, c) for s, c in scored if s >= self.min_article_chars]
            if not scored:
                continue
            score, candidate = max(scored, key=lambda pair: pair[0])
            if len(scored) > 1:
                total = sum(s for s, _ in scored)
                # Many similar candidates = a listing page, not one story.
                if total and score / total < LISTING_DOMINANCE:
                    continue
            if best is None or score > best[0]:
                best = (score, candidate, selector)
            # `article` winning outright is the strongest signal there is.
            if selector == "article":
                break
        if best is None:
            return None, None
        _score, candidate, selector = best
        # A root that spans the whole body is still the right root — the
        # furniture pass below works inside it (Wikipedia's `main` IS the body
        # once nav is gone, and its references, navboxes and category links are
        # exactly what a distiller must not read as the writing).
        _ = body
        return candidate, selector

    def _score(self, candidate: Tag) -> int:
        text_len = _text_len(candidate)
        if not text_len:
            return 0
        if _link_text_len(candidate) / text_len > float(
            parser_knob("max_link_text_ratio", MAX_LINK_TEXT_RATIO)
        ):
            return 0
        paragraphs = _paragraph_text_len(candidate)
        return paragraphs or 0

    def _strip_furniture(self, root: Tag) -> None:
        root_len = _text_len(root) or 1
        for element in list(root.find_all(True)):
            if element.decomposed or element is root:
                continue
            reason = _furniture_reason(element)
            if reason is None:
                continue
            own = _text_len(element)
            # Never let a marker eat the article: an element carrying most of
            # the root's text is the body, whatever it calls itself.
            if own * 2 > root_len:
                continue
            match_type, trigger_value = reason
            self.removal_details.append(
                {
                    "attribute": element.name,
                    "match_type": match_type,
                    "trigger_value": trigger_value,
                    "text": element.get_text(" ", strip=True),
                    "html_length": len(str(element)),
                }
            )
            element.decompose()

    def _headline_block(self, soup: BeautifulSoup, root: Tag) -> Tag | None:
        """The headline + dek when they live outside the article body."""
        if root.find(["h1"]) is not None:
            return None
        root_len = _text_len(root) or 1
        limit = min(
            int(parser_knob("max_headline_block_chars", MAX_HEADLINE_BLOCK_CHARS)),
            int(
                root_len * float(parser_knob("max_headline_block_ratio", MAX_HEADLINE_BLOCK_RATIO))
            ),
        )
        for h1 in soup.find_all("h1"):
            node: Tag | None = h1
            chosen: Tag | None = None
            while node is not None and node.name not in {"body", "html", "[document]"}:
                if node is root or node in root.parents:
                    break
                if _text_len(node) <= limit:
                    chosen = node
                    node = node.parent
                    continue
                break
            if chosen is not None:
                block = BeautifulSoup(str(chosen), "lxml")
                inner = block.body.find(True) if block.body else None
                if inner is not None and _furniture_reason(inner) is None:
                    return inner
        return None


__all__ = ["ArticleContentFinder", "MainContentFinder", "ARTICLE_ROOT_SELECTORS"]
