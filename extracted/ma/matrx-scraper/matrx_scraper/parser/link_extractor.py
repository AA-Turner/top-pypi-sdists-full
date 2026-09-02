from __future__ import annotations

import urllib.parse
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup


EXTENSION_PACK = {
    # bmp/tiff are still shipped by scanners, CMS media libraries and older
    # sites; without them an image link fell through to "others" and vanished
    # from the images bucket.
    "image": ["jpg", "jpeg", "png", "gif", "svg", "webp", "bmp", "tiff", "tif"],
    "document": [
        "pdf",
        "doc",
        "docx",
        "xls",
        "xlsx",
        "ppt",
        "pptx",
        "txt",
        "rtf",
        "odt",
        "csv",
        "epub",
        "md",
    ],
    "audio": ["mp3", "wav", "aac", "flac", "ogg", "m4a", "wma", "aiff"],
    "video": ["mp4", "avi", "mkv", "mov", "wmv", "flv", "mpeg", "webm", "3gp", "mpg", "mts"],
    "archive": ["zip", "rar", "7z", "tar", "gz", "bz2", "iso", "dmg", "tgz", "xz"],
    "others": [
        "js",
        "tsx",
        "ts",
        "css",
        "scss",
        "less",
        "json",
        "xml",
        "woff",
        "woff2",
        "ttf",
        "otf",
        "eot",
        "map",
        "ico",
        "webmanifest",
        "yaml",
        "coffee",
    ],
}

_IMAGE_IGNORE_TAGS = {
    "iframe",
    "svg",
    "aside",
    "nav",
    "header",
    "footer",
    "sidebar",
    "script",
    "style",
    "meta",
    "link",
}

# Anchor records — page regions we can name from the DOM, most specific first.
# `_region_for` walks ancestors and reports the first one it meets, so a link
# inside <footer><nav> reports "nav" (the tighter container it actually lives in).
_REGION_TAGS = ("nav", "header", "footer", "aside", "main", "article")

# Anchor text longer than this is boilerplate (a whole card, a paragraph wrapped
# in an <a>), not a label — truncate at the same limit the SEO audit uses so the
# two link surfaces agree.
ANCHOR_TEXT_MAX_CHARS = 500

# Ceiling on anchor records per page. Matches seo_audit's cap: nav-heavy sites
# emit tens of thousands of anchors and the tail carries no new signal.
ANCHOR_RECORD_LIMIT = 2000


def _get_domain(url: str) -> str:
    """Extract the netloc (domain + port) from a URL for same-domain comparison."""
    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return ""


def _expand_url(base_url: str, url: str) -> str | None:
    if not url or url.startswith("#"):
        return None
    parsed = urlparse(url)._replace(fragment="")
    url = parsed.geturl()
    if not parsed.scheme:
        return urljoin(base_url, url)
    return url


def _determine_filetype(full_url: str) -> str | None:
    parsed = urllib.parse.urlsplit(full_url)
    path = parsed.path
    filename = path.split("/")[-1]
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    if ext in EXTENSION_PACK["image"]:
        return "image"
    # Archives are their OWN category — do not fold them into "document".
    # The archive check below must stay reachable: LinkExtractor.extract() fills
    # an "archives" bucket that crawler.py reads to emit kind="archive"
    # resources, and PageLinks.archives is part of the published TS contract.
    if ext in EXTENSION_PACK["document"]:
        return "document"
    if ext in EXTENSION_PACK["audio"]:
        return "audio"
    if ext in EXTENSION_PACK["video"]:
        return "video"
    if ext in EXTENSION_PACK["archive"]:
        return "archive"
    if ext in EXTENSION_PACK["others"]:
        return "other"
    return None


def _registrable_domain(host: str) -> str:
    """Last two labels of a host — the cheap `subdomain` test also used by
    `seo_audit.audit_html`. Deliberately not a public-suffix lookup: this runs
    on every anchor of every page and only feeds a coarse link_type label."""
    return ".".join(host.split(".")[-2:]) if host else ""


def _region_for(element) -> str:
    """Which named page region an anchor sits in — nav/header/footer/aside/
    main/article, or "body" when the page uses no landmark at all."""
    parent = element.find_parent(_REGION_TAGS)
    return parent.name.lower() if parent is not None else "body"


def _anchor_text_of(element) -> str:
    """Visible text of an anchor, collapsed to a single line.

    Image-only links legitimately have no text; the alt text of the image they
    wrap is the closest thing to a human label, so it is used as a fallback and
    the record says so via `text_source`."""
    raw = element.get_text(" ", strip=True) or ""
    return " ".join(raw.split())


def _is_valid_url(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    return bool(parsed.scheme and parsed.netloc)


def _should_include_image(element, min_width: int = 150, min_height: int = 150) -> bool:
    if element.name in _IMAGE_IGNORE_TAGS:
        return False
    if any(element.find_parent(tag) for tag in _IMAGE_IGNORE_TAGS):
        return False

    width = element.get("width")
    height = element.get("height")
    style = element.get("style", "")
    if not width and "width:" in style:
        width = style.split("width:")[-1].split(";")[0].strip()
    if not height and "height:" in style:
        height = style.split("height:")[-1].split(";")[0].strip()

    if not width and not height:
        return True

    def _parse_px(val) -> int | None:
        try:
            return int(str(val).replace("px", "").strip())
        except (ValueError, TypeError):
            return None

    w = _parse_px(width)
    h = _parse_px(height)

    if w is not None and w < min_width:
        return False
    if h is not None and h < min_height:
        return False
    return True


class LinkExtractor:
    """
    Extracts and categorises all links found in an HTML document.

    Returns a dict with keys:
        internal, external, images, documents, audio, videos, archives, others

    `extract()` answers "which URLs does this page point at" and its buckets are
    bare URL strings — that shape is persisted and read by several consumers and
    does not change. `extract_anchors()` answers the different question "how does
    this page LABEL what it points at", returning one record per <a href> with
    the anchor text, rel/nofollow and page region. Anchor text is the strongest
    human-authored label a link carries and is unrecoverable once discarded, so
    both are produced from the same parse.
    """

    def __init__(self, base_url: str, image_min_width: int = 150, image_min_height: int = 150):
        self.base_url = base_url
        self.base_domain = _get_domain(base_url)
        self.image_min_width = image_min_width
        self.image_min_height = image_min_height

    def extract(self, soup: str | BeautifulSoup) -> dict[str, list[str]]:
        if isinstance(soup, str):
            soup = BeautifulSoup(soup, "lxml")

        links: dict[str, set] = {
            "internal": set(),
            "external": set(),
            "images": set(),
            "documents": set(),
            "audio": set(),
            "videos": set(),
            "archives": set(),
            "others": set(),
        }

        lookup_attrs = ["src", "data-src", "nitro-lazy-src", "href"]

        for element in soup.find_all():
            for attr in lookup_attrs:
                raw = element.get(attr)
                if not raw:
                    continue
                expanded = _expand_url(self.base_url, raw)
                if expanded is None:
                    continue
                if not _is_valid_url(expanded):
                    links["others"].add(expanded)
                    continue

                filetype = _determine_filetype(expanded)
                if filetype == "image":
                    bucket = (
                        "images"
                        if _should_include_image(
                            element, self.image_min_width, self.image_min_height
                        )
                        else "others"
                    )
                elif filetype == "document":
                    bucket = "documents"
                elif filetype == "audio":
                    bucket = "audio"
                elif filetype == "video":
                    bucket = "videos"
                elif filetype == "archive":
                    bucket = "archives"
                elif filetype == "other":
                    bucket = "others"
                else:
                    bucket = "internal" if _get_domain(expanded) == self.base_domain else "external"

                links[bucket].add(expanded)

        return {k: sorted(v) for k, v in links.items()}

    def extract_anchors(self, soup: str | BeautifulSoup) -> list[dict[str, object]]:
        """One record per <a href> — url + how the page labels it.

        Record shape (key names match `seo_audit.LinkItem` / the `crawl_links`
        rows so a consumer reads one vocabulary):

            target_url  — absolute, fragment-stripped
            anchor_text — collapsed visible text ("" when there is none)
            text_source — "anchor" | "image_alt" | "" — where anchor_text came
                          from, so a consumer can weight real prose above the
                          alt text borrowed from an image-only link
            rel         — the raw rel attribute, or None
            nofollow    — rel contains nofollow
            link_type   — internal | subdomain | external
            region      — nav | header | footer | aside | main | article | body

        Duplicate (url, anchor text) pairs collapse — a nav repeated in a footer
        is one fact. The SAME url with DIFFERENT anchor text is kept as separate
        records: that variation is the signal.
        """
        if isinstance(soup, str):
            soup = BeautifulSoup(soup, "lxml")

        base_reg = _registrable_domain(self.base_domain)
        records: list[dict[str, object]] = []
        seen: set[tuple[str, str]] = set()

        for element in soup.find_all("a", href=True):
            expanded = _expand_url(self.base_url, element.get("href"))
            if expanded is None or not _is_valid_url(expanded):
                continue
            if not expanded.startswith(("http://", "https://")):
                continue

            text = _anchor_text_of(element)
            text_source = "anchor" if text else ""
            if not text:
                img = element.find("img")
                alt = " ".join((img.get("alt") or "").split()) if img is not None else ""
                if alt:
                    text = alt
                    text_source = "image_alt"
            if len(text) > ANCHOR_TEXT_MAX_CHARS:
                text = text[:ANCHOR_TEXT_MAX_CHARS]

            key = (expanded, text.lower())
            if key in seen:
                continue
            seen.add(key)

            host = _get_domain(expanded)
            if host == self.base_domain:
                link_type = "internal"
            elif base_reg and (host == base_reg or host.endswith("." + base_reg)):
                link_type = "subdomain"
            else:
                link_type = "external"

            rel = element.get("rel")
            if isinstance(rel, list):  # bs4 treats rel as a multi-valued attribute
                rel = " ".join(rel)

            records.append(
                {
                    "target_url": expanded,
                    "anchor_text": text,
                    "text_source": text_source,
                    "rel": rel or None,
                    "nofollow": bool(rel and "nofollow" in rel.lower()),
                    "link_type": link_type,
                    "region": _region_for(element),
                }
            )
            if len(records) >= ANCHOR_RECORD_LIMIT:
                break

        return records
