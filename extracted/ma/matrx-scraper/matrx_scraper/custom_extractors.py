"""Custom extractors — Screaming-Frog-style "Custom Extraction".

Per-host, named CSS / XPath / regex / json-ld extractors that pull arbitrary
fields out of every crawled page. Output is a JSONB-ready dict keyed by
extractor name, carried on the crawl's page payload.

Examples:
    {
        "name": "product_price",
        "host_pattern": "shop.example.com",
        "extractor_type": "css",
        "expression": ".product-price",
        "attribute": "text",
        "multiple": false
    }
    {
        "name": "publish_date",
        "host_pattern": ".medium.com",
        "extractor_type": "json_ld",
        "expression": "datePublished",
        "multiple": false
    }
    {
        "name": "phone_numbers",
        "host_pattern": "raymarcleaners.com",
        "extractor_type": "regex",
        "expression": "\\b\\d{3}-\\d{3}-\\d{4}\\b",
        "multiple": true
    }

Standalone — no sibling matrx imports.
"""

from __future__ import annotations

import json
import logging
import re
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

from selectolax.parser import HTMLParser

logger = logging.getLogger(__name__)


@dataclass
class Extractor:
    id: str
    name: str
    host_pattern: str
    extractor_type: str  # 'css' | 'xpath' | 'regex' | 'json_ld'
    expression: str
    attribute: str | None = None  # for css: text/href/src/...
    multiple: bool = False
    enabled: bool = True


def _matches_host(extractor: Extractor, host: str) -> bool:
    if not extractor.enabled:
        return False
    pat = extractor.host_pattern.lower().strip()
    h = host.lower().strip()
    if pat == h:
        return True
    if pat.startswith(".") and h.endswith(pat):
        return True
    return False


def find_for_url(extractors: Sequence[Extractor], url: str) -> list[Extractor]:
    host = urlparse(url).netloc.lower()
    if not host:
        return []
    return [e for e in extractors if _matches_host(e, host)]


def run_extractor(html: str, extractor: Extractor) -> Any:
    """Run a single extractor against raw HTML, return its output.

    Output shape:
      - css with attribute='text': string (or list of strings if multiple)
      - css with attribute='href'/'src'/etc: same — attribute value(s)
      - regex: matched string (or list of strings if multiple)
      - json_ld: pulled out of any application/ld+json blob by key path
    """
    if not html:
        return None
    t = (extractor.extractor_type or "").lower()
    try:
        if t == "css":
            return _run_css(html, extractor)
        if t == "regex":
            return _run_regex(html, extractor)
        if t == "json_ld":
            return _run_json_ld(html, extractor)
        if t == "xpath":
            # selectolax doesn't support full XPath; for now we accept
            # css-like xpath and degrade. Real XPath would need lxml.
            logger.info("xpath extractor %s — falling back to CSS interpretation", extractor.name)
            return _run_css(html, extractor)
    except Exception:
        logger.exception("extractor %s failed", extractor.name)
        return None
    return None


def _run_css(html: str, e: Extractor) -> Any:
    tree = HTMLParser(html)
    nodes = tree.css(e.expression)
    if not nodes:
        return None
    attr = (e.attribute or "text").lower().strip()

    def _val(node) -> str | None:
        if attr == "text":
            v = node.text(deep=True, separator=" ").strip()
            return v or None
        if attr == "html":
            try:
                return node.html
            except Exception:
                return None
        return node.attributes.get(attr)

    if e.multiple:
        return [v for v in (_val(n) for n in nodes) if v is not None][:200]
    return _val(nodes[0])


def _run_regex(html: str, e: Extractor) -> Any:
    try:
        rx = re.compile(e.expression)
    except re.error as exc:
        logger.info("regex extractor %s has invalid pattern: %s", e.name, exc)
        return None
    if e.multiple:
        return rx.findall(html)[:200]
    m = rx.search(html)
    return m.group(0) if m else None


def _run_json_ld(html: str, e: Extractor) -> Any:
    """Pull a field by key-path out of any application/ld+json blob.

    `expression` is a dot-separated key path: e.g. "datePublished",
    "offers.price", "aggregateRating.ratingValue".
    """
    tree = HTMLParser(html)
    blocks: list[dict[str, Any]] = []
    for s in tree.css('script[type="application/ld+json"]'):
        raw = (s.text(deep=True) or "").strip()
        if not raw:
            continue
        try:
            payload = json.loads(raw)
        except Exception:
            continue
        if isinstance(payload, list):
            blocks.extend([p for p in payload if isinstance(p, dict)])
        elif isinstance(payload, dict):
            blocks.append(payload)

    keys = [k for k in (e.expression or "").split(".") if k]
    found: list[Any] = []
    for block in blocks:
        cur: Any = block
        for k in keys:
            if isinstance(cur, dict):
                cur = cur.get(k)
            elif isinstance(cur, list) and cur:
                cur = cur[0].get(k) if isinstance(cur[0], dict) else None
            else:
                cur = None
                break
        if cur is not None:
            found.append(cur)
    if not found:
        return None
    return found if e.multiple else found[0]


def run_all(html: str, url: str, extractors: Sequence[Extractor]) -> dict[str, Any]:
    """Run every extractor that matches `url`'s host. Returns a name → value
    dict suitable for direct JSONB storage on the crawl's page payload.
    """
    matching = find_for_url(extractors, url)
    if not matching:
        return {}
    out: dict[str, Any] = {}
    for ex in matching:
        out[ex.name] = run_extractor(html, ex)
    return out


__all__ = ["Extractor", "find_for_url", "run_extractor", "run_all"]
