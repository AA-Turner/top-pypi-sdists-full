from __future__ import annotations

import json
import re
from collections.abc import Iterator
from typing import Any, Literal
from urllib.parse import urljoin, urlparse

from pydantic import BaseModel, Field
from selectolax.parser import HTMLParser, Node

from matrx_scraper.clean_content import looks_like_address, street_addresses_in
from matrx_scraper.events import PageSummary
from matrx_scraper.media_embed import video_embed_provider

CandidateCategory = Literal["media", "fact", "social", "link", "identity"]

_SOCIAL_HOSTS = {
    "instagram.com": "instagram",
    "facebook.com": "facebook",
    "x.com": "x",
    "twitter.com": "x",
    "tiktok.com": "tiktok",
    "youtube.com": "youtube",
    "youtu.be": "youtube",
    "linkedin.com": "linkedin",
    "pinterest.com": "pinterest",
    "pinterest.ca": "pinterest",
}
_EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
_PHONE_PATTERN = r"(?<!\w)(?:\+?1[ .-]?)?(?:\([2-9]\d{2}\)|[2-9]\d{2})[ .-]\d{3}[ .-]\d{4}(?!\w)"
_PHONE_RE = re.compile(_PHONE_PATTERN)
_FAX_RE = re.compile(
    rf"\b(?:fax|facsimile)(?:\s*(?:number|no\.?|#))?\s*[:\-]?\s*(?P<number>{_PHONE_PATTERN})",
    re.IGNORECASE,
)
_LOGO_HINTS = ("logo", "brand", "wordmark", "logomark")
_HERO_HINTS = ("hero", "banner", "masthead", "cover")
# A file or alt text that names itself a social-share card is never a logo.
_SHARE_HINTS = ("social-sharing", "social_sharing", "social-share", "social_share", "sharing-banner",
                "share-image", "share_image", "og-image", "og_image", "og-default", "opengraph", "open-graph",
                "twitter-card", "social-card", "social-media-image", "social_media_image")


def is_share_banner_shape(width: int | None, height: int | None) -> bool:
    """True for a social-share banner's shape (about 1.91:1, 1000px or wider): never a logo."""
    return bool(width and height and width >= 1000 and 1.7 <= width / height <= 2.1)


class DiscoveredCandidate(BaseModel):
    category: CandidateCategory
    guessed_kind: str
    url: str | None = None
    value: dict[str, Any] = Field(default_factory=dict)
    context: dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(ge=0, le=1)


class SiteIdentity(BaseModel):
    """Observed homepage identity persisted to ``web.site`` seconds into
    initialize (only-fill-nulls; the user's own edits are never overwritten)."""

    description: str | None = None
    favicon_url: str | None = None
    og_image_url: str | None = None
    logo_url: str | None = None


# A logo candidate below this confidence is left out of the identity write —
# the discovery inbox still receives every candidate. Admits schema.org logos
# (0.99) and header/nav or hint-matched logos (0.8+). The og:image / twitter:image
# share banner is never a logo candidate at all (it is its own og_image kind).
_IDENTITY_LOGO_MIN_CONFIDENCE = 0.8


def derive_site_identity(
    candidates: list[DiscoveredCandidate],
    *,
    summary: PageSummary,
) -> SiteIdentity:
    """Pick the best observed identity values from homepage candidates."""

    def best_url(category: str, kind: str, min_confidence: float = 0.0) -> str | None:
        matches = [
            candidate
            for candidate in candidates
            if candidate.category == category
            and candidate.guessed_kind == kind
            and candidate.url
            and candidate.confidence >= min_confidence
        ]
        if not matches:
            return None
        return max(matches, key=lambda candidate: candidate.confidence).url

    description = (summary.meta_description or "").strip() or None
    return SiteIdentity(
        description=description,
        favicon_url=best_url("media", "favicon"),
        og_image_url=best_url("media", "og_image"),
        logo_url=best_url("media", "logo", _IDENTITY_LOGO_MIN_CONFIDENCE),
    )


#: Hosts whose landing page is a VENDOR's, never the brand's: link shorteners and branded-short-domain landings,
#: domain parking and for-sale marketplaces, and registrar placeholders. A site address that forwards to one of these
#: is never read as the brand's page, however the landing page names the brand (a "jmikes.co is for sale" page names
#: it too). Every other forward is judged by ``_landing_names_the_site``.
_VENDOR_LANDING_DOMAINS = frozenset({
    "bitly.com", "bit.ly", "tinyurl.com", "rebrandly.com", "rebrand.ly", "t.co", "ow.ly", "buff.ly", "short.io",
    "cutt.ly", "is.gd", "tiny.cc", "lnkd.in", "shorturl.at",
    "godaddy.com", "afternic.com", "sedo.com", "dan.com", "hugedomains.com", "namecheap.com", "bodis.com",
    "parkingcrew.net", "above.com", "undeveloped.com", "squadhelp.com", "atom.com", "brandbucket.com",
    "domainmarket.com", "uniregistry.com", "register.com", "networksolutions.com", "ionos.com", "hostgator.com",
    "bluehost.com", "wix.com", "squarespace.com", "weebly.com",
})

#: Hosts where one host carries many businesses, each at its own PATH (a directory listing, a link hub, a marketplace
#: storefront, a Google Site): a forward there lands on a page ABOUT the brand inside somebody else's site, whose
#: schema.org, logos and links are the platform's. Never read as the brand's site; the full address is recorded.
#: Kept in step with ``matrx_social.identity._SHARED_SITE_HOSTS`` (the identity side of the same class). Hosts that
#: give each tenant its own SUBDOMAIN (``acme.wixsite.com``, ``acme.square.site``) are the tenant's own site and are
#: not listed.
_PATH_TENANTED_DOMAINS = frozenset({
    "google.com", "g.page", "goo.gl", "linktr.ee", "linkin.bio", "beacons.ai", "about.me", "yelp.com", "etsy.com",
    "amazon.com", "apple.com", "github.com", "gitlab.com", "medium.com", "tripadvisor.com", "opentable.com",
    "doordash.com", "ubereats.com", "grubhub.com", "toasttab.com", "houzz.com", "angi.com", "thumbtack.com",
    "nextdoor.com", "bbb.org", "yellowpages.com", "mapquest.com", "calendly.com", "vagaro.com", "booksy.com",
    "mindbodyonline.com", "styleseat.com", "zocdoc.com", "healthgrades.com", "avvo.com", "upwork.com", "fiverr.com",
})

#: Subdomain words that name no brand (``www.``, ``shop.``…): never compared as the site's name.
_GENERIC_HOST_WORDS = frozenset({
    "www", "www2", "m", "mobile", "shop", "store", "app", "web", "home", "site", "online", "order", "booking", "book",
    "blog", "en", "us", "info", "secure", "my", "go", "get",
})

#: The shortest name compared by containment: shorter labels ("joe", "ab") match by accident.
_MIN_NAME = 4


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def _host_parts(url: str):
    import tldextract

    host = (urlparse(url if "://" in url else f"https://{url}").hostname or "").lower()
    if not host:
        return None
    return tldextract.extract(host)


def _site_label(url: str) -> tuple[str, str] | None:
    """(name label, registrable domain) of an address: ``https://www.bitly.com/x`` -> ``("bitly", "bitly.com")``."""
    ext = _host_parts(url)
    if ext is None or not ext.domain:
        return None
    return ext.domain, f"{ext.domain}.{ext.suffix}" if ext.suffix else ext.domain


def _site_names(url: str) -> set[str]:
    """The names an address can go by: its name label and every non-generic subdomain label, so a hosted site
    (``acme.wixsite.com``) is known as ``acme`` as well as ``wixsite``."""
    ext = _host_parts(url)
    if ext is None:
        return set()
    names = {_norm(ext.domain)} if ext.domain else set()
    names |= {_norm(part) for part in ext.subdomain.split(".") if part and part not in _GENERIC_HOST_WORDS}
    return {name for name in names if name}


def _names_relate(a: str, b: str, path_words: set[str]) -> bool:
    """One site name is the other's, carries it, or splits into a shared lead plus a word the landing path names
    (``acmereno`` -> ``acmeplumbing.com/locations/reno``)."""
    if a == b:
        return True
    short, long = sorted((a, b), key=len)
    if len(short) >= _MIN_NAME and short in long:
        return True
    lead = 0
    while lead < min(len(a), len(b)) and a[lead] == b[lead]:
        lead += 1
    if lead >= _MIN_NAME:
        rest = a[lead:]
        if len(rest) >= 3 and any(rest == word or (len(word) >= _MIN_NAME and word in rest) for word in path_words):
            return True
    return False


def _landing_names_the_site(root_url: str, final_url: str, page_names: tuple[str, ...]) -> bool:
    """True when the place a site forwards to is plainly the same brand: its new domain carries the old name
    (``acmeplumbing.com`` -> ``acmeplumbingandair.com``), a franchise parent's page names the location
    (``acmereno.com`` -> ``acmeplumbing.com/locations/reno``), a hosted site moved to its own domain
    (``acme.wixsite.com`` -> ``acme.com``), or the landing page's own title or site name carries the site's name
    (a sale page saying ``joesbakery.com is for sale`` does not count: it names the address, not the business)."""
    root_names = {name for name in _site_names(root_url) if len(name) >= 3}
    landing = _site_names(final_url)
    path = urlparse(final_url if "://" in final_url else f"https://{final_url}").path or ""
    path_words = {_norm(word) for word in re.split(r"[/\-_.]+", path) if word}
    path_words.discard("")
    for root in root_names:
        for name in landing | {word for word in path_words if len(word) >= _MIN_NAME}:
            if _names_relate(root, name, path_words):
                return True
    root_domain = (_site_label(root_url) or ("", ""))[1]
    for raw in page_names:
        text = (raw or "").lower()
        if not text or (root_domain and root_domain in text):
            continue
        said = _norm(text)
        if any(len(root) >= _MIN_NAME and root in said for root in root_names):
            return True
    return False


SOCIAL_LANDING = "social"
PLATFORM_LANDING = "platform"
VENDOR_LANDING = "vendor"


def offsite_landing(root_url: str, final_url: str, *, page_names: tuple[str, ...] = ()) -> str | None:
    """How a site's homepage LANDED somewhere else, when its page must not be read as the brand's; else None.

    * ``"vendor"`` — the forward went to a short-link, parking or registrar vendor (``jmikes.co`` ->
      ``bitly.com/pages/landing/...``, CH-04 2026-10-24: that page's name, logos and schema.org ``sameAs`` are the
      vendor's, and reading them filed Bitly's Facebook, Instagram and X as the brand's accounts), or to a host
      whose name has nothing to do with the site's.
    * ``"platform"`` — the forward went to a page inside a many-business platform (a Yelp listing, a Linktree, a
      Google Site): the page is about the brand, but its schema.org, logos and links are the platform's.
    * ``"social"`` — the forward went to a social profile (``joesbakery.com`` -> ``facebook.com/joesbakery``): the
      profile is the brand's account, but the platform's page is not the brand's website.

    None (read the page as the brand's) for the site's own domain and subdomains, the same name under another suffix
    (``brand.com`` -> ``brand.co.uk``), and a forward that plainly stays the same brand (``_landing_names_the_site``:
    a new domain carrying the name, a franchise parent's location page, a hosted site's own domain, a landing page
    titled with the site's name). ``page_names`` are the landing page's title and site name. Pure.
    """
    root = _site_label(root_url)
    landed = _site_label(final_url)
    if root is None or landed is None:
        return None
    if root[1] == landed[1] or root[0] == landed[0]:
        return None
    if landed[1] in _VENDOR_LANDING_DOMAINS:
        return VENDOR_LANDING
    if _social_kind(final_url):
        return SOCIAL_LANDING
    if landed[1] in _PATH_TENANTED_DOMAINS:
        return PLATFORM_LANDING
    if _landing_names_the_site(root_url, final_url, page_names):
        return None
    return VENDOR_LANDING


def landing_page_names(summary: PageSummary | None) -> tuple[str, ...]:
    """The landing page's own names (title, og:site_name, og:title) for ``offsite_landing``."""
    if summary is None:
        return ()
    tags = summary.og_tags or {}
    names = [summary.title or ""]
    for key in ("og:site_name", "site_name", "og:title", "title"):
        value = tags.get(key)
        if isinstance(value, str):
            names.append(value)
    return tuple(name for name in names if name)


def forwarded_candidates(final_url: str, *, root_url: str) -> list[DiscoveredCandidate]:
    """What an address that forwards off-site says about the brand: only WHERE it forwards, at its FULL address
    (``facebook.com/joesbakery``, never ``facebook.com/``). A social profile is an account finding; anything else is
    one website finding the person answers (a renamed brand's new domain Belongs; a vendor's page is Not). Nothing on
    the landing page is read as the brand's (``offsite_landing``)."""
    context = {"where": "the site address forwards here", "forwarded_from": root_url, "landed_on": final_url}
    kind = _social_kind(final_url)
    if kind:
        url = clean_social_url(final_url)
        if not (urlparse(url).path or "").strip("/"):
            return []  # the platform's front door (a login wall) names no account
        return [DiscoveredCandidate(category="social", guessed_kind=kind, url=url, context=context, confidence=0.6)]
    return [
        DiscoveredCandidate(
            category="link",
            guessed_kind="website",
            url=final_url,
            value={"text": final_url},
            context=context,
            confidence=0.5,
        )
    ]


def _absolute_http_url(raw: str | None, base_url: str) -> str | None:
    if not raw:
        return None
    value = raw.strip()
    if not value:
        return None
    resolved = urljoin(base_url, value)
    parsed = urlparse(resolved)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    return resolved


#: Query parameters that NAME a social page (a video ``?v=``, a Facebook ``profile.php?id=``). Everything else on a
#: social link is junk to the account (``view_as=subscriber``, ``utm_*``, ``fbclid``, ``si``, ``hl``…) and is cut
#: before the link is stored, so one account is one address (live defect 2026-10-15: a brand's YouTube carried
#: ``?view_as=subscriber`` into its stored profile).
_SOCIAL_IDENTIFYING_PARAMS = frozenset({"v", "id", "fbid", "story_fbid", "list"})


def clean_social_url(url: str) -> str:
    """``url`` without its fragment and every query parameter that does not name the page."""
    from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

    parts = urlsplit(url)
    keep = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=False) if k.lower() in _SOCIAL_IDENTIFYING_PARAMS]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(keep), ""))


def _social_kind(url: str) -> str | None:
    host = (urlparse(url).hostname or "").lower()
    host = host.removeprefix("www.")
    for domain, kind in _SOCIAL_HOSTS.items():
        if host == domain or host.endswith(f".{domain}"):
            return kind
    return None


def _schema_nodes(value: Any, path: str = "$") -> Iterator[tuple[str, Any]]:
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _schema_nodes(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _schema_nodes(child, f"{path}[{index}]")


def _schema_url(value: Any, base_url: str) -> str | None:
    if isinstance(value, str):
        return _absolute_http_url(value, base_url)
    if isinstance(value, dict):
        for key in ("url", "contentUrl", "@id"):
            resolved = _absolute_http_url(value.get(key), base_url)
            if resolved:
                return resolved
    return None


def _int_attr(node: Node, name: str) -> int | None:
    raw = (node.attributes.get(name) or "").strip().lower().removesuffix("px")
    try:
        return int(float(raw))
    except ValueError:
        return None


def _ancestor_is_header_or_nav(node: Node) -> bool:
    parent = node.parent
    for _ in range(6):
        if parent is None:
            return False
        if parent.tag in {"header", "nav"}:
            return True
        parent = parent.parent
    return False


# A logo wall ("our clients", "partners", "as seen on", "sponsors"…) shows OTHER brands' marks. An image in one is
# never the brand's own logo, however it is named (``/images/logos/red-robin.png`` in ``section.logos``).
_LOGO_WALL_WORDS = ("logos", "logo-grid", "logo-wall", "logo-strip", "logo-list", "logo-carousel", "logo-slider",
                    "client", "partner", "sponsor", "customer", "press-", "in-the-press", "featured-in", "as-seen", "seen-on",
                    "trusted", "testimonial", "award", "accredit", "certif", "affiliat", "member", "brands",
                    "marquee", "ticker")
# A container this close to the image holding at least this many distinct images is a strip of marks.
LOGO_WALL_MIN_IMAGES = 3
_LOGO_WALL_DEPTH = 3
_HEADER_CLASS_WORDS = ("header", "navbar", "nav-", "-nav", "masthead", "site-brand", "w-nav")


def _in_site_header(node: Node) -> bool:
    """The image sits in the site header / nav bar (a tag, or a container named like one)."""
    parent = node.parent
    for _ in range(8):
        if parent is None or parent.tag in {"body", "html"}:
            return False
        if parent.tag in {"header", "nav"}:
            return True
        named = f"{parent.attributes.get('class') or ''} {parent.attributes.get('id') or ''}".lower()
        if any(word in named for word in _HEADER_CLASS_WORDS):
            return True
        parent = parent.parent
    return False


_SOCIAL_ICON_RE = re.compile(
    r"(?<![a-z])(facebook|instagram|linkedin|twitter|youtube|tiktok|pinterest|yelp|threads|whatsapp)(?![a-z])"
)


def names_social_icon(hints: str) -> bool:
    """A file / alt / class naming a social network is that network's icon (a link to an account), never a logo."""
    return bool(_SOCIAL_ICON_RE.search(hints.lower()))


def is_logo_wall_image(node: Node) -> bool:
    """True when ``node`` (an ``img``) sits in a strip/grid of other brands' marks — a clients, partners, press or
    sponsors section — rather than being the site's own brand mark. Images in the site header/nav never are."""
    if _in_site_header(node):
        return False
    root = node
    while root.parent is not None:
        root = root.parent
    first_image = root.css_first("img")
    # The page's first image is where a header-less site puts its own mark; only a named wall unseats it.
    count_rule = not (first_image is not None and first_image.mem_id == node.mem_id)
    parent = node.parent
    for depth in range(6):
        if parent is None or parent.tag in {"body", "html", "main"}:
            return False
        named = f"{parent.attributes.get('class') or ''} {parent.attributes.get('id') or ''}".lower()
        if any(word in named for word in _LOGO_WALL_WORDS):
            return True
        if count_rule and depth < _LOGO_WALL_DEPTH:
            sources = {
                (img.attributes.get("src") or img.attributes.get("data-src") or "").split("?")[0]
                for img in parent.css("img")
            }
            sources.discard("")
            if len(sources) >= LOGO_WALL_MIN_IMAGES:
                return True
        parent = parent.parent
    return False


def _surrounding(text: str, start: int, length: int) -> str:
    return text[max(0, start - 80) : min(len(text), start + length + 80)].strip()


def extract_homepage_candidates(
    html: str,
    *,
    base_url: str,
    summary: PageSummary,
) -> list[DiscoveredCandidate]:
    tree = HTMLParser(html)
    candidates: list[DiscoveredCandidate] = []

    def add(
        category: CandidateCategory,
        guessed_kind: str,
        *,
        url: str | None = None,
        value: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
        confidence: float,
    ) -> None:
        payload = value or {}
        if url is None and not any(item not in (None, "", [], {}) for item in payload.values()):
            return
        candidates.append(
            DiscoveredCandidate(
                category=category,
                guessed_kind=guessed_kind,
                url=url,
                value=payload,
                context=context or {},
                confidence=confidence,
            )
        )

    for link in tree.css("link[href]"):
        rel = (link.attributes.get("rel") or "").lower()
        if "icon" not in rel:
            continue
        url = _absolute_http_url(link.attributes.get("href"), base_url)
        add(
            "media",
            "favicon",
            url=url,
            context={"where": "head link", "rel": rel},
            confidence=0.98,
        )
    for path, node in _schema_nodes(summary.schema_org):
        if not isinstance(node, dict):
            continue
        for key, raw in node.items():
            lowered = key.lower()
            schema_path = f"{path}.{key}"
            if lowered == "logo":
                add(
                    "media",
                    "logo",
                    url=_schema_url(raw, base_url),
                    context={"where": "schema.org", "schema_path": schema_path},
                    confidence=0.99,
                )
            elif lowered == "sameas":
                values = raw if isinstance(raw, list) else [raw]
                for item in values:
                    url = _schema_url(item, base_url)
                    kind = _social_kind(url) if url else None
                    if url and kind:
                        add(
                            "social",
                            kind,
                            url=clean_social_url(url),
                            context={"where": "schema.org sameAs", "schema_path": schema_path},
                            confidence=0.98,
                        )
            elif lowered in {"telephone", "phone"} and isinstance(raw, str):
                add(
                    "fact",
                    "phone",
                    value={"text": raw.strip()},
                    context={"where": "schema.org", "schema_path": schema_path},
                    confidence=0.98,
                )
            elif lowered in {"faxnumber", "fax"} and isinstance(raw, str):
                add(
                    "fact",
                    "fax",
                    value={"text": raw.strip()},
                    context={"where": "schema.org", "schema_path": schema_path},
                    confidence=0.99,
                )
            elif lowered == "email" and isinstance(raw, str):
                add(
                    "fact",
                    "email",
                    value={"text": raw.strip().removeprefix("mailto:")},
                    context={"where": "schema.org", "schema_path": schema_path},
                    confidence=0.98,
                )
            elif lowered == "address" and isinstance(raw, str | dict) and (
                isinstance(raw, dict) and any(raw.get(k) for k in ("streetAddress", "postalCode", "addressLocality"))
                or isinstance(raw, str) and looks_like_address(raw)
            ):
                add(
                    "fact",
                    "address",
                    value={"address": raw},
                    context={"where": "schema.org", "schema_path": schema_path},
                    confidence=0.97,
                )

    og_image = _absolute_http_url(str(summary.og_tags.get("og:image") or ""), base_url)
    twitter_image = _absolute_http_url(str(summary.twitter_tags.get("twitter:image") or ""), base_url)
    share_urls = {u for u in (og_image, twitter_image) if u}

    for image in tree.css("img"):
        attrs = image.attributes
        raw_src = attrs.get("src") or attrs.get("data-src")
        url = _absolute_http_url(raw_src, base_url)
        if not url:
            continue
        alt = (attrs.get("alt") or "").strip()
        class_name = attrs.get("class") or ""
        element_id = attrs.get("id") or ""
        hints = " ".join((raw_src or "", alt, class_name, element_id)).lower()
        context = {
            "where": "header/nav image" if _ancestor_is_header_or_nav(image) else "page image",
            "alt": alt,
            "class": class_name,
            "id": element_id,
        }
        width = _int_attr(image, "width")
        height = _int_attr(image, "height")
        # The share image (og:image / twitter:image) and anything shaped or named like one is stored as its
        # own kind, never as a logo candidate.
        is_share = (
            url in share_urls
            or any(hint in hints for hint in _SHARE_HINTS)
            or is_share_banner_shape(width, height)
        )
        in_header = _ancestor_is_header_or_nav(image)
        named_logo = any(hint in hints for hint in ("logo", "wordmark", "logomark"))
        in_wall = is_logo_wall_image(image) or names_social_icon(hints)
        if not is_share and not in_wall and (in_header or named_logo or any(hint in hints for hint in _LOGO_HINTS)):
            # Real logo signals rank: named logo in the header > named logo or header image > "brand" only.
            confidence = 0.9 if (in_header and named_logo) else 0.85 if (in_header or named_logo) else 0.8
            add("media", "logo", url=url, context=context, confidence=confidence)
        if any(hint in hints for hint in _HERO_HINTS) or (
            width is not None and height is not None and width >= 800 and height >= 300
        ):
            add(
                "media",
                "hero_image",
                url=url,
                context={**context, "width": width, "height": height},
                confidence=0.82,
            )

    if og_image:
        add("media", "og_image", url=og_image, context={"where": "og:image"}, confidence=0.99)
    add(
        "media",
        "twitter_image",
        url=twitter_image,
        context={"where": "twitter:image"},
        confidence=0.98,
    )

    for selector in ("video[src]", "video source[src]"):
        for node in tree.css(selector):
            url = _absolute_http_url(node.attributes.get("src"), base_url)
            if url:
                add(
                    "media",
                    "video",
                    url=url,
                    context={
                        "where": selector,
                        "provider": "html_video",
                        "title": node.attributes.get("title") or "",
                    },
                    confidence=0.85,
                )

    for node in tree.css("iframe[src]"):
        url = _absolute_http_url(node.attributes.get("src"), base_url)
        provider = video_embed_provider(url) if url else None
        if url and provider:
            add(
                "media",
                "video",
                url=url,
                context={
                    "where": "iframe[src]",
                    "provider": provider,
                    "title": node.attributes.get("title") or "",
                },
                confidence=0.95,
            )

    for link in summary.links:
        kind = _social_kind(link.target_url)
        if kind:
            add(
                "social",
                kind,
                url=clean_social_url(link.target_url),
                context={"where": "homepage link", "anchor_text": link.anchor_text},
                confidence=0.92,
            )

    body = tree.body
    visible_text = (body.text(deep=True, separator=" ") if body else tree.text()) or ""
    visible_text = re.sub(r"\s+", " ", visible_text).strip()

    fax_matches = list(_FAX_RE.finditer(visible_text))
    for match in fax_matches:
        number = match.group("number")
        add(
            "fact",
            "fax",
            value={"text": number.strip()},
            context={
                "where": "homepage text",
                "surrounding_text": _surrounding(visible_text, match.start(), len(match.group(0))),
            },
            confidence=0.96,
        )

    for regex, kind, confidence in (
        (_EMAIL_RE, "email", 0.9),
        (_PHONE_RE, "phone", 0.82),
        (None, "address", 0.72),
    ):
        matches = street_addresses_in(visible_text) if kind == "address" else list(regex.finditer(visible_text))
        for match in matches:
            if kind == "phone" and any(
                match.start() >= fax.start("number") and match.end() <= fax.end("number")
                for fax in fax_matches
            ):
                continue
            add(
                "fact",
                kind,
                value={"text": match.group(0).strip()},
                context={
                    "where": "homepage text",
                    "surrounding_text": _surrounding(
                        visible_text, match.start(), len(match.group(0))
                    ),
                },
                confidence=confidence,
            )

    add(
        "identity",
        "title",
        value={"text": summary.title},
        context={"where": "title"},
        confidence=0.99,
    )
    add(
        "identity",
        "description",
        value={"text": summary.meta_description},
        context={"where": "meta description"},
        confidence=0.98,
    )
    add(
        "identity",
        "site_name",
        value={"text": summary.og_tags.get("og:site_name")},
        context={"where": "og:site_name"},
        confidence=0.98,
    )

    deduped: dict[tuple[str, str, str, str], DiscoveredCandidate] = {}
    for candidate in candidates:
        key = (
            candidate.category,
            candidate.guessed_kind,
            candidate.url or "",
            json.dumps(candidate.value, sort_keys=True, separators=(",", ":")),
        )
        current = deduped.get(key)
        if current is None or candidate.confidence > current.confidence:
            deduped[key] = candidate
    return list(deduped.values())


__all__ = [
    "CandidateCategory",
    "DiscoveredCandidate",
    "SiteIdentity",
    "derive_site_identity",
    "extract_homepage_candidates",
    "forwarded_candidates",
    "landing_page_names",
    "offsite_landing",
]
