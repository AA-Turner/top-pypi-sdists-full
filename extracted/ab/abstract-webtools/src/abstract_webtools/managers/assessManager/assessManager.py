"""
assessManager — compact, LLM-ready webpage assessment.

Composes the shared fetch-once chain (urlManager -> requestManager -> soupManager,
which already tries Selenium first and falls back to requests) into a single
robust, token-budgeted entry point an LLM can consume directly.

Public API:
    assess_webpage(url, ...) -> dict   # full structured assessment
    prescreen_webpage(url, ...) -> dict # cheap relevance pre-screen (title+desc+lede)
"""
import logging

from ..soupManager.soupManager import soupManager, get_soup_mgr
from ..seleneumManager import get_selenium_source

# Below this many characters of extracted text we assume the cheap fetch hit a
# JS wall / bot block and a full browser render is worth the cost.
_EMPTY_RENDER_THRESHOLD = 200


def _meta_lookup(meta, *keys):
    """Return the first <meta> content whose name/property/itemprop matches keys."""
    wanted = {k.lower() for k in keys}
    for m in meta:
        for k in ("name", "property", "itemprop"):
            if str(m.get(k, "")).lower() in wanted and m.get("content"):
                return m["content"]
    return None


def _budget_text(sections, max_chars):
    """Dedup consecutive boilerplate and cap total length. Returns (text, truncated)."""
    parts, seen_last, total, truncated = [], None, 0, False
    for s in sections or []:
        s = (s or "").strip()
        if not s or s == seen_last:
            continue
        if total + len(s) + 1 > max_chars:
            truncated = True
            break
        parts.append(s)
        seen_last = s
        total += len(s) + 1
    return "\n".join(parts), truncated


def _build_soup(url, force_render):
    """
    Return (soup_mgr, sections, render_mode), hardened against empty renders.

    force_render=True skips the cheap path entirely. Otherwise we fetch cheaply,
    and only fall back to a forced Selenium render if the result is ~empty.
    """
    render = "selenium-forced" if force_render else "requests/selenium-auto"
    sm, sections = None, []

    if not force_render:
        try:
            sm = get_soup_mgr(url)
            sections = sm.extract_text_sections() or []
        except Exception as e:
            logging.warning(f"assess_webpage cheap fetch failed for {url}: {e}")

    if force_render or sum(len(s) for s in sections) < _EMPTY_RENDER_THRESHOLD:
        try:
            html = get_selenium_source(url, request_fallback=True)
            if html:
                sm = soupManager(url=url, source_code=html)
                sections = sm.extract_text_sections() or []
                render = "selenium-forced"
        except Exception as e:
            logging.warning(f"assess_webpage forced render failed for {url}: {e}")

    return sm, sections, render


def assess_webpage(url, *, max_chars=12000, max_links=50, force_render=False):
    """
    Fetch a page and return a compact, LLM-ready structured assessment.

    Args:
        url:          page to assess.
        max_chars:    hard cap on extracted body text (token budget guard).
        max_links:    max same-domain links to include.
        force_render: skip the cheap fetch and render with a full browser.

    Returns dict:
        {url, title, description, text, metadata, jsonld, links, truncated, render}
        On total failure, text/metadata/jsonld/links degrade to empty values and
        render == "failed".
    """
    sm, sections, render = _build_soup(url, force_render)

    if sm is None:
        return {
            "url": url, "title": None, "description": None, "text": "",
            "metadata": [], "jsonld": [], "links": [],
            "truncated": False, "render": "failed",
        }

    text, truncated = _budget_text(sections, max_chars)

    try:
        meta = sm.all_meta() or []
    except Exception:
        meta = []
    try:
        title = sm.soup.title.get_text(strip=True) if sm.soup and sm.soup.title else None
    except Exception:
        title = None
    try:
        jsonld = sm.all_jsonld() or []
    except Exception:
        jsonld = []
    try:
        links = (sm.get_all_website_links() or [])[:max_links]
    except Exception:
        links = []

    return {
        "url": url,
        "title": title,
        "description": _meta_lookup(meta, "description", "og:description", "twitter:description"),
        "text": text,
        "metadata": meta,
        "jsonld": jsonld,
        "links": links,
        "truncated": truncated,
        "render": render,
    }


def prescreen_webpage(url, *, max_chars=600, force_render=False):
    """
    Cheap relevance pre-screen: title + description + a short lede of body text.

    Ideal as a first pass — let the LLM decide "is this page worth a full read?"
    before paying for assess_webpage()'s larger payload.

    Returns dict: {url, title, description, lede, render}
    """
    page = assess_webpage(url, max_chars=max_chars, max_links=0, force_render=force_render)
    return {
        "url": url,
        "title": page["title"],
        "description": page["description"],
        "lede": page["text"],
        "render": page["render"],
    }
