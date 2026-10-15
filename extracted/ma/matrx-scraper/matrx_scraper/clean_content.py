"""The ONE clean page text for AI models, from HTML already in hand (no fetch).

:func:`clean_page_content` is exactly what a scrape hands to models (``ScrapeResult.ai_research_content``:
the parser pipeline with its content filters — menus, footers, ads and boilerplate removed, structure
kept). Any caller that already holds a page's HTML (a direct GET, a cached copy) uses this instead of
re-cleaning it by hand, so every page text on the platform is the same text.

:func:`contact_footer_text` keeps the one thing that cleaning rightly drops but a business identity
needs: a footer that carries contact details (phone, email or street address) — where many small
businesses write them. ``None`` when the footer holds none.
"""

from __future__ import annotations

import re
from typing import Any

_PHONE = re.compile(r"(\+?1[\s.-]?)?\(?\b\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}\b")
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_STREET = re.compile(r"\b\d{1,6}\s+[A-Za-z0-9.' ]{2,40}\b(street|st|avenue|ave|road|rd|drive|dr|boulevard|blvd|lane|"
                     r"ln|way|suite|ste|court|ct|place|pl|parkway|pkwy|highway|hwy)\b", re.I)


def has_contact_details(text: str) -> bool:
    return bool(_PHONE.search(text or "") or _EMAIL.search(text or "") or _STREET.search(text or ""))


def clean_page_content(html: str, url: str | None = None) -> str:
    """The page's AI-ready clean text (``ai_research_content``), '' when the page has none. CPU-bound:
    async callers run it in a thread."""
    if not html:
        return ""
    from matrx_scraper.orchestrator import _parse_html_content

    out: dict[str, Any] = _parse_html_content(html, url, fast=True)
    text = str(out.get("ai_research_content") or "")
    # Runs of spaces inside a line are layout, never content (line breaks are kept).
    return "\n".join(re.sub(r"[ \t\u00a0]{2,}", " ", line).rstrip() for line in text.splitlines()).strip()


def contact_footer_text(html: str) -> str | None:
    """The footer's text (``<footer>`` / ``role=contentinfo``) when it carries contact details, else None."""
    import html as _html

    from selectolax.parser import HTMLParser

    tree = HTMLParser(html or "")
    for n in tree.css("script, style, noscript, template, svg"):
        n.decompose()
    parts: list[str] = []
    for node in tree.css("footer, [role=contentinfo]"):
        lines = [" ".join(x.split()) for x in (node.text(separator="\n") or "").splitlines()]
        text = _html.unescape("\n".join(line for line in lines if line))
        if text and text not in parts:
            parts.append(text)
    footer = "\n".join(parts)
    return footer if footer and has_contact_details(footer) else None
