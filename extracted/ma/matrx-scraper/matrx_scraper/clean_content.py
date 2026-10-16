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
_TYPES = (r"(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Way|Court|Ct|Place|Pl|Parkway|Pkwy|"
          r"Highway|Hwy|Circle|Cir|Trail|Trl|Terrace|Ter|Square|Sq)")
_DIR = r"(?:N|S|E|W|NE|NW|SE|SW|North|South|East|West|Northeast|Northwest|Southeast|Southwest)"
_NAME_TOKEN = r"(?:[A-Z][A-Za-z'\u2019-]*|\d{1,3}(?:st|nd|rd|th)|\d{1,3})"
#: A real street address: number, optional direction, 1-3 capitalised/ordinal name words, a street type. Case-sensitive
#: on the name words so a sentence ("541 West for 12 miles. Take County Road") is never one (MKT-086).
STREET_ADDRESS_RE = re.compile(
    rf"(?<![\w$#.,/-])\d{{1,6}}(?:-\d{{1,6}})?\s+(?:{_DIR}\.?\s+)?(?P<name>{_NAME_TOKEN}(?:\s{_NAME_TOKEN}){{0,2}})\s"
    rf"{_TYPES}\b\.?(?:\s+(?:{_DIR}\b\.?))?(?:,?\s+(?:Suite|Ste|Unit|Apt|#)\.?\s*[A-Za-z0-9-]+)?"
)
_PO_BOX_RE = re.compile(r"\bP\.?\s?O\.?\s+Box\s+\d+\b", re.I)
_CITY_STATE_ZIP_RE = re.compile(r"\b[A-Z][a-zA-Z.'-]+(?:\s[A-Z][a-zA-Z.'-]+){0,2},\s*[A-Z]{2}\s+\d{5}(?:-\d{4})?\b")
#: Words that open or fill a sentence, never a street's name.
_NOT_STREET_WORDS = frozenset(w.lower() for w in (
    "We", "Our", "Opened", "On", "In", "The", "For", "To", "Take", "Turn", "Miles", "Mile", "Follow", "Head", "And", "Or",
    "At", "From", "Is", "Are", "Was", "Were", "Then", "Go", "Continue", "Drive", "Exit", "Merge", "Stay", "Keep", "Left",
    "Right", "Past", "Until", "Years", "Year", "Open", "Call", "Visit", "Located", "About", "Over", "Than", "More",
    "Less", "Hours", "Days", "Minutes", "Min", "Feet", "Ft", "Ago", "By", "With", "Of", "A", "An", "I", "It", "You",
    "Your", "Address", "Phone", "Tel", "Fax", "Email", "Contact", "Has", "Have", "Had", "Be", "Not", "No", "All", "Only", "Just", "Since", "Until", "Til", "Today"))


def street_addresses_in(text: str) -> list[re.Match[str]]:
    """Every real street-address shape in ``text`` (and P.O. boxes); never driving directions or other sentences."""
    out: list[re.Match[str]] = []
    for m in STREET_ADDRESS_RE.finditer(text or ""):
        words = [w.lower() for w in m.group("name").split()]
        if any(w in _NOT_STREET_WORDS for w in words):
            continue
        out.append(m)
    out.extend(_PO_BOX_RE.finditer(text or ""))
    return sorted(out, key=lambda m: m.start())


def looks_like_address(text: str) -> bool:
    """True when ``text`` as a whole is a postal address shape: it holds a street address, a P.O. box, or a
    ``City, ST 12345``. Narration, driving directions and menu text are not (MKT-086)."""
    t = " ".join(str(text or "").split())
    if not t or len(t) > 200:
        return False
    return bool(street_addresses_in(t) or _CITY_STATE_ZIP_RE.search(t))


# ── page chrome (MKT-087) ───────────────────────────────────────────────────────────────────────

_CHROME_WORD = (r"(?:open|close|toggle|show|hide|skip|expand|collapse|go to)?\s*(?:the\s+)?(?:main\s+|mobile\s+|site\s+)?"
                r"(?:menu|navigation|nav|search|cart|basket|bag|content|to content|to main content|sidebar|"
                r"hamburger|account|login|log in|sign in|sign up|checkout|wishlist)")
_CHROME_TOKEN = re.compile(
    rf"^(?:{_CHROME_WORD}|(?:view\s+)?(?:cart|basket|bag)\s*[(\[]?\s*\d*\s*[)\]]?|\d{{1,3}}\s*(?:items?)?(?:\s+in\s+(?:your\s+)?(?:cart|bag|basket))?"
    rf"|(?:cart|basket|bag|items?)\s*[:(\[]?\s*\d{{1,3}}\s*[)\]]?|skip to (?:main )?content|[\W_]*)$", re.I)
_CHROME_PHRASE = re.compile(rf"\b{_CHROME_WORD}\b(?:\s*[(\[]?\s*\d{{1,3}}\s*[)\]]?)?", re.I)
_CHROME_SPLIT = re.compile(r"\s*[\u00b7\u2022|\u2502/]\s*|\s{3,}")


def is_chrome_line(line: str) -> bool:
    """A line made only of navigation chrome: menu/cart/search toggles, a cart count, bare counters, separators."""
    t = " ".join((line or "").split())
    if not t:
        return False
    parts = [p for p in _CHROME_SPLIT.split(t) if p.strip()]
    if not parts:
        return True  # only separators
    for p in parts:
        if _CHROME_TOKEN.match(p.strip()):
            continue
        # Several chrome phrases run together ("Open Menu Close Menu"): drop each, what is left must be bare counters.
        rest = _CHROME_PHRASE.sub(" ", p)
        if _CHROME_PHRASE.search(p) and re.fullmatch(r"[\W\d_]{0,12}", rest):
            continue
        return False
    return True


def strip_chrome_text(text: str) -> str:
    """``text`` without its chrome lines (nav, menu, cart-count and toggle text). Every site text is cleaned here
    before it is used anywhere: About, facts, products and services evidence (MKT-087)."""
    return "\n".join(line for line in (text or "").splitlines() if not is_chrome_line(line)).strip()


_CHROME_ATTR = re.compile(
    r"(?:^|[\s_-])(?:nav|navbar|navigation|hamburger|burger|minicart|mini-cart|cart|cart-count|menu-toggle|nav-toggle|"
    r"mobile-menu|main-menu|site-menu|menu-button|menu-icon|menu-open|menu-close|skip-link|skip-to-content)(?:$|[\s_-])", re.I)


def drop_chrome_nodes(tree: Any) -> None:
    """Remove menu, cart and toggle elements from a parsed page (selectolax) in place. Short elements only for the
    attribute rules, so a wrapper that merely carries a menu class never takes the page's content with it."""
    for node in list(tree.css("nav, [role=navigation], [role=menu], [role=menubar]")):
        node.decompose()
    for node in list(tree.css("[aria-haspopup], [aria-expanded], [class], [id], [aria-label]")):
        if node.tag in ("body", "html", "main", "article"):
            continue
        text = " ".join((node.text() or "").split())
        if len(text) > 400:
            continue
        a = node.attributes
        blob = " ".join(str(a.get(k) or "") for k in ("class", "id", "aria-label"))
        toggle = a.get("aria-haspopup") is not None or a.get("aria-expanded") is not None
        if (_CHROME_ATTR.search(blob) and len(text) < 200) or (toggle and len(text) < 120) or (
                text and len(text) < 60 and is_chrome_line(text)):
            node.decompose()


def flatten_tel_links(tree: Any) -> None:
    """Replace ``<a href="tel:…">`` with plain text in place, so a number a site splits across several
    links (``<a>(</a><a>646) 559-4878</a>``) reads as one number, not as broken markdown links (MKT-071).
    A link whose own text is words ("Call us") keeps the dialled number beside it."""
    for node in list(tree.css('a[href^="tel:"], a[href^="TEL:"]')):
        label = node.text() or ""
        number = (node.attributes.get("href") or "")[4:].split(";", 1)[0].strip()
        if len(re.findall(r"[^\W\d_]", label)) >= 3 and not re.search(r"\d", label) and re.search(r"\d", number):
            label = f"{label.strip()} {number}".strip()
        node.replace_with(label)


def has_contact_details(text: str) -> bool:
    return bool(_PHONE.search(text or "") or _EMAIL.search(text or "") or street_addresses_in(text or ""))


def clean_page_content(html: str, url: str | None = None) -> str:
    """The page's AI-ready clean text (``ai_research_content``), '' when the page has none. CPU-bound:
    async callers run it in a thread."""
    if not html:
        return ""
    from selectolax.parser import HTMLParser

    from matrx_scraper.orchestrator import _parse_html_content

    tree = HTMLParser(html)
    flatten_tel_links(tree)  # before the chrome pass: a lone "(" link looks like chrome and would be dropped
    drop_chrome_nodes(tree)
    out: dict[str, Any] = _parse_html_content(tree.html or html, url, fast=True)
    text = strip_chrome_text(str(out.get("ai_research_content") or ""))
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
    footer = strip_chrome_text("\n".join(parts))
    return footer if footer and has_contact_details(footer) else None
