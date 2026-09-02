from __future__ import annotations

import asyncio
import re
from typing import Any
from uuid import uuid4

import bs4
from bs4 import BeautifulSoup

from .element_extractor import ElementExtractor
from .extraction_rules import rules
from .link_extractor import LinkExtractor
from .noise_remover import NoiseRemover
from .noise_config import NoiseRemoverConfig
from .overrides import overrides
from .scrape_filter import ScrapeFilter
from .transform import HtmlTransformer

try:
    import extruct

    _EXTRUCT_AVAILABLE = True
except ImportError:
    _EXTRUCT_AVAILABLE = False


def _get_soup(obj) -> BeautifulSoup | None:
    if obj is None:
        return None
    if isinstance(obj, BeautifulSoup):
        return obj
    return BeautifulSoup(str(obj), "lxml")


def _remove_and_extract_wrapped(soup: BeautifulSoup, tag: str) -> tuple[BeautifulSoup, list[dict]]:
    """Remove all wrapper tags inserted by NoiseRemover / ScrapeFilter and collect removal details."""
    removal_info: list[dict] = []
    for element in soup.find_all(tag):
        if element.name and element.attrs:
            text = element.get_text()
            removal_info.append(
                {
                    "attribute": element.get("type"),
                    "match_type": element.get("match_type", ""),
                    "trigger_value": element.get("trigger_item", ""),
                    "text": text,
                    "html_length": len(str(element)),
                }
            )
        element.decompose()
    return soup, removal_info


class ParserOrchestrator:
    """
    Full pipeline orchestrator — mirrors scraper/logic/parse/orchestrator.py.

    Pipeline:
        1. HtmlTransformer  — normalise HTML
        2. NoiseRemover     — strip structural junk (nav, scripts, hidden elements …)
        3. ScrapeFilter     — remove noise from content
        4. ElementExtractor — extract typed content blocks

    Plus: metadata extraction (extruct: JSON-LD, OpenGraph), link extraction,
    and hashing (MinHash + SimHash) when libraries are available.
    """

    def __init__(
        self,
        soup=None,
        url: str | None = None,
        content_filter_overrides=None,
        noise_remover_config: NoiseRemoverConfig | None = None,
    ):
        self.soup: BeautifulSoup | None = _get_soup(soup)
        self.url = url
        self.uuid = str(uuid4())
        self.page_title = ""
        self.website = ""
        self.full_domain = ""
        self.unique_page_name = ""

        self.noise_remover = NoiseRemover(config=noise_remover_config)
        self.scrape_filter = ScrapeFilter()
        self.element_extractor = ElementExtractor()
        self.content_filter_overrides = content_filter_overrides or overrides

        self._noise_removed_soup: BeautifulSoup | None = None
        self._filtered_soup: BeautifulSoup | None = None
        self.noise_remover_removal_details: list[dict] = []
        self.content_filter_removal_details: list[dict] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def parse_content(
        self,
        soup: bs4.BeautifulSoup | str | None = None,
        url: str | None = None,
        content_filter_overrides=None,
        skip_links: bool = False,
        skip_hashes: bool = False,
    ) -> dict[str, Any]:
        if soup is not None:
            self.soup = _get_soup(soup)
        if url is not None:
            self.url = url
        if content_filter_overrides is not None:
            self.content_filter_overrides = content_filter_overrides

        if not self.soup:
            raise ValueError("No HTML provided to parse.")

        # ---- Stage 0: URL metadata ----
        self._init_url_meta()

        # ---- Stage 1: HTML normalisation ----
        transformer = HtmlTransformer(self.soup)
        self.soup = transformer.process()

        # ---- Stage 2: NoiseRemover ----
        wrapped_noise = self.noise_remover.remove_noise(self.soup, remove=False)
        self._noise_removed_soup, self.noise_remover_removal_details = _remove_and_extract_wrapped(
            wrapped_noise, "NoiseRemover"
        )

        # ---- Stage 3: ScrapeFilter ----
        wrapped_filter = self.scrape_filter.filter_soup(
            self._noise_removed_soup,
            remove=False,
            content_filter_config=self.content_filter_overrides,
        )
        self._filtered_soup, self.content_filter_removal_details = _remove_and_extract_wrapped(
            wrapped_filter, "ContentFilter"
        )

        # ---- Stage 4: Element extraction ----
        extracted = self.element_extractor.extract_content(self._filtered_soup, url=self.url)

        page_dict = extracted.get("organized_data")
        # `extract_content` returns exactly {organized_data, metadata, hashes}
        # (element_extractor.extract_content). `structured_data` used to be read
        # from it here and was therefore None on every page ever parsed, while
        # the real JSON-LD sat one level down in `overview.metadata` — it is now
        # taken from `rich_metadata` below, after stage 6 computes it (AD192).
        # `outline` is the SAME dead read and is deliberately still empty: the
        # only consumer is `compute_simhash_from_outline`, whose "H2: heading"
        # key format cannot be reconstructed without inventing a fingerprint
        # shape, and that fingerprint is compared across crawls. AD192 stays
        # open for it — do not "fix" this by guessing the key format.
        outline = extracted.get("outline", {})
        extraction_meta = extracted.get("metadata", {})

        # ---- Stage 5: Text / char count ----
        text_data = self._build_text_data(page_dict)
        char_count = len(text_data)
        char_count_formatted = len(self._build_text_data_with_markers(page_dict))

        # ---- Stage 6: Metadata (extruct + meta tags) ----
        rich_metadata = self._get_metadata()
        main_image = rich_metadata.pop("main_image", None)
        # NOT popped: `metadata["structured_data"]` is the key every existing
        # consumer already reads. This only stops the top-level field lying.
        structured_data = rich_metadata.get("structured_data")

        # ---- Stage 7: Links (skippable for fast/research mode) ----
        # Two products of the same extractor: `links` (URL buckets — the
        # long-lived persisted shape) and `link_records` (per-anchor rows that
        # carry the anchor TEXT, unrecoverable once the parse is thrown away).
        links = {} if skip_links else self._extract_links()
        link_records = [] if skip_links else self._extract_link_records()

        # ---- Stage 8: Hashing (skippable for fast/research mode) ----
        hashes = {} if skip_hashes else self._compute_hashes(text_data, outline)

        # ---- Build overview ----
        table_count = extraction_meta.get("table_count", 0) or 0
        code_count = extraction_meta.get("code_block_count", 0) or 0
        list_count = extraction_meta.get("list_count", 0) or 0

        overview = {
            "uuid": self.uuid,
            "website": self.website,
            "url": self.url,
            "metadata": rich_metadata,
            "unique_page_name": self.unique_page_name,
            "page_title": self.page_title,
            "has_structured_content": bool(table_count or code_count or list_count),
            "table_count": table_count,
            "code_block_count": code_count,
            "list_count": list_count,
            "outline": outline,
            "char_count": char_count,
            "char_count_formatted": char_count_formatted,
        }

        return {
            "overview": overview,
            "structured_data": structured_data,
            "organized_data": page_dict,
            "text_data": text_data,
            "main_image": main_image,
            "hashes": hashes,
            "links": links,
            "link_records": link_records,
            "content_filter_removal_details": self.content_filter_removal_details,
            "noise_remover_removal_details": self.noise_remover_removal_details,
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _init_url_meta(self) -> None:
        if not self.url:
            return
        try:
            from urllib.parse import urlparse
            import tldextract

            parsed = urlparse(self.url)
            ext = tldextract.extract(parsed.netloc)
            self.website = f"{ext.domain}.{ext.suffix}" if ext.suffix else ext.domain
            subdomain = ext.subdomain
            self.full_domain = f"{subdomain}.{self.website}" if subdomain else self.website
            path = parsed.path.rstrip("/") if parsed.path != "/" else ""
            combined = self.full_domain + path
            self.unique_page_name = re.sub(r"[^a-zA-Z0-9]", "_", combined)
        except Exception:
            pass

        title_tag = self.soup.find("title") if self.soup else None
        if title_tag:
            self.page_title = title_tag.get_text(strip=True)

    def _build_text_data(self, page_dict: Any) -> str:
        """The page as readable text.

        Rendering belongs to `OrganizedData.to_text()` — see the reasoning in
        its docstring. This used to hand the `OrganizedData` OBJECT to a
        dict/list-only flattener, which silently produced "" for every page.
        No `except: return ""` here for that reason: an unrenderable page must
        be loud, not quietly report zero characters.
        """
        if page_dict is None:
            return ""
        return page_dict.to_text()

    def _build_text_data_with_markers(self, page_dict: Any) -> str:
        """Same as _build_text_data but retains AI-chunking markers for char_count_formatted."""
        if page_dict is None:
            return ""
        return page_dict.to_text(add_markers=True)

    def _get_metadata(self) -> dict[str, Any]:
        if not self.soup:
            return {}

        json_ld: list = []
        opengraph: dict = {}

        if _EXTRUCT_AVAILABLE and self.url:
            try:
                extracted = extruct.extract(
                    str(self.soup), base_url=self.url, syntaxes=["json-ld", "opengraph"]
                )
                json_ld = extracted.get("json-ld", [])
                opengraph_list = extracted.get("opengraph", [])
                if isinstance(opengraph_list, list) and opengraph_list:
                    opengraph = opengraph_list[0]
                elif isinstance(opengraph_list, dict):
                    opengraph = opengraph_list
            except Exception:
                pass

        meta_tags = self._extract_meta_tags()
        canonical_url = self._extract_canonical_url()
        robots = self._extract_robots()
        structured_data = self._extract_json_ld_scripts()
        main_image = self._extract_main_image(json_ld, opengraph, meta_tags)

        return {
            "json-ld": json_ld,
            "opengraph": opengraph,
            "meta_tags": meta_tags,
            "canonical_url": canonical_url,
            "structured_data": structured_data,
            "robots_directives": robots,
            "main_image": main_image,
        }

    def _extract_meta_tags(self) -> dict[str, Any]:
        meta_dict: dict[str, Any] = {}
        for meta in self.soup.find_all("meta"):
            key = meta.get("name") or meta.get("property") or "unknown"
            content = (meta.get("content") or "").strip()
            if key in meta_dict:
                existing = meta_dict[key]
                if isinstance(existing, list):
                    existing.append(content)
                else:
                    meta_dict[key] = [existing, content]
            else:
                meta_dict[key] = content
        return meta_dict

    def _extract_canonical_url(self) -> str | None:
        tag = self.soup.find("link", {"rel": "canonical"})
        return tag["href"] if tag and tag.get("href") else None

    def _extract_robots(self) -> str | None:
        tag = self.soup.find("meta", {"name": "robots"})
        return tag["content"] if tag and tag.get("content") else None

    def _extract_json_ld_scripts(self) -> list[str]:
        scripts = self.soup.find_all("script", {"type": "application/ld+json"})
        return [s.string.strip() for s in scripts if s.string]

    def _extract_main_image(self, json_ld: list, opengraph: dict, meta_tags: dict) -> str | None:
        if isinstance(opengraph, dict):
            img = opengraph.get("og:image") or opengraph.get("image")
            if img:
                return img

        for item in json_ld:
            if not isinstance(item, dict):
                continue
            for field in ("image", "thumbnailUrl"):
                val = item.get(field)
                if isinstance(val, str):
                    return val
                if isinstance(val, dict):
                    url = val.get("contentUrl") or val.get("url")
                    if url:
                        return url
                if isinstance(val, list) and val:
                    first = val[0]
                    if isinstance(first, str):
                        return first
                    if isinstance(first, dict):
                        url = first.get("contentUrl") or first.get("url")
                        if url:
                            return url

        # Raw <meta> fallbacks, in descending trust. `og:image` appears here as
        # well as in `opengraph` above on purpose: the opengraph dict comes from
        # extruct, which is an OPTIONAL extra — without it that branch is empty
        # and a perfectly ordinary og:image page would have reported no main
        # image at all. The last three are the long-tail tags real sites still
        # ship when they carry no OpenGraph block.
        for key in (
            "og:image",
            "twitter:image",
            "image",
            "thumbnail",
            "msapplication-TileImage",
        ):
            val = meta_tags.get(key)
            if not val:
                continue
            resolved = val[0] if isinstance(val, list) else val
            if resolved:
                return resolved

        return None

    def _extract_links(self) -> dict[str, list[str]]:
        if not self.url or not self.soup:
            return {}
        try:
            extractor = LinkExtractor(base_url=self.url)
            return extractor.extract(self.soup)
        except Exception:
            return {}

    def _extract_link_records(self) -> list[dict[str, Any]]:
        if not self.url or not self.soup:
            return []
        try:
            extractor = LinkExtractor(base_url=self.url)
            return extractor.extract_anchors(self.soup)
        except Exception:
            return []

    def _compute_hashes(self, text_data: str, outline: Any) -> dict:
        try:
            from .hashing import compute_hashes

            return compute_hashes(text_data, outline if isinstance(outline, dict) else None)
        except Exception:
            return {}


def _parse_html_sync(html_content: str, page_url: str | None = None) -> dict[str, Any]:
    parser = ParserOrchestrator()
    result = parser.parse_content(str(html_content), page_url)
    organized_data = result.get("organized_data")
    extracted = organized_data.extract(rules=rules) if organized_data is not None else {}
    extracted["links"] = result.get("links", {})
    extracted["link_records"] = result.get("link_records", [])
    return extracted


async def parse_html(html_content: str, page_url: str | None = None) -> dict[str, Any]:
    """
    Convenience async wrapper — returns the extraction-rules dict
    (compatible with the old API).  Also now includes a ``links`` key.
    """
    return await asyncio.to_thread(_parse_html_sync, html_content, page_url)


def extract_text_by_selector(html_content: str, selector: str) -> str:
    """Run a CSS selector against raw HTML and return the concatenated text.

    Used for per-domain "real content" extraction when raw text length is
    misleading (endless-scroll feeds, sidebars, nav-heavy pages). Returns
    an empty string if the selector matches nothing or parsing fails — the
    caller decides what that means (typically: fail the quality check).

    Multiple comma-separated selectors are supported via BeautifulSoup's
    `.select()` semantics, e.g.
    `[role=main] [data-testid=post_message], [role=main] article`.
    """
    if not html_content or not selector:
        return ""
    try:
        soup = BeautifulSoup(str(html_content), "lxml")
    except Exception:
        return ""
    try:
        nodes = soup.select(selector)
    except Exception:
        return ""
    if not nodes:
        return ""
    parts = [n.get_text(" ", strip=True) for n in nodes]
    return "\n".join(p for p in parts if p)
