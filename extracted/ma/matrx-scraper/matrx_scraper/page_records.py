"""A parsed page's links, images, videos and audio as records — one projection for every reader.

Research stores these on each capture (``rs_content.extracted_links`` / ``extracted_images``) and turns them into
gallery rows; ``scraper.scrape`` returns the same records so a workflow saves exactly what research code saves.
Inline ``data:`` images are dropped (they can be megabytes of base64) and counted.
"""

from __future__ import annotations

import re
from typing import Any

#: An ``<iframe>``'s real ``src`` (whitespace before the attribute, so a lazy-load ``data-src`` placeholder is not it).
_IFRAME_SRC = re.compile(r"<iframe[^>]*?\ssrc=[\"']([^\"']+)[\"']", re.I)


def _get(parsed: Any, key: str) -> Any:
    return parsed.get(key) if isinstance(parsed, dict) else getattr(parsed, key, None)


def page_text(parsed: Any) -> str:
    """The page's text written for an AI reader: the parse's ai_research_content, else its ai_content."""
    return str(_get(parsed, "ai_research_content") or "") or str(_get(parsed, "ai_content") or "")


def page_records(parsed: Any) -> tuple[list[dict], list[dict], list[dict], list[dict], int]:
    """(links, images, videos, audios, inline images dropped) of one parse."""
    links: list[dict] = []
    raw_links = _get(parsed, "links") or {}
    if isinstance(raw_links, dict):
        for category in ("external", "internal"):
            for link in raw_links.get(category, []) or []:
                if isinstance(link, dict):
                    links.append({"url": link.get("href", ""), "text": link.get("text", ""), "is_internal": category == "internal"})
                elif isinstance(link, str):
                    links.append({"url": link, "text": "", "is_internal": category == "internal"})
    images: list[dict] = []
    dropped = 0
    raw_images = _get(parsed, "images") or []
    if isinstance(raw_images, list):
        for img in raw_images:
            if isinstance(img, dict):
                src = str(img.get("src", "") or "").strip()
                if src.lower().startswith("data:"):
                    dropped += 1
                    continue
                images.append({"src": src, "alt": img.get("alt", ""), "caption": img.get("caption", ""),
                               "width": img.get("width", ""), "height": img.get("height", ""),
                               "title": img.get("title", ""), "srcset": img.get("srcset", [])})
            elif isinstance(img, str):
                if img.strip().lower().startswith("data:"):
                    dropped += 1
                    continue
                images.append({"src": img, "alt": "", "caption": "", "width": "", "height": "", "title": "", "srcset": []})
    raw_videos = _get(parsed, "videos") or []
    videos = [v for v in raw_videos if isinstance(v, dict)] if isinstance(raw_videos, list) else []
    raw_audios = _get(parsed, "audios") or []
    audios = [a for a in raw_audios if isinstance(a, dict)] if isinstance(raw_audios, list) else []
    return links, images, videos, audios, dropped


def iframe_sources(html: str | None) -> list[str]:
    """Every ``<iframe>`` ``src`` of a page's raw HTML, in page order (embedded players: the parse does not model them).

    The one reading: ``scraper.scrape`` returns it as a fact (``iframe_srcs``) so a step after it needs the sources,
    never the page's HTML; aidream's gallery (``page_media.extract_iframe_video_urls``) classifies the same list."""
    return _IFRAME_SRC.findall(html) if html else []
