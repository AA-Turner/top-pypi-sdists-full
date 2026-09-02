"""Which platform is this host running, and how fast will it let us crawl?

**Arman, 2026-08-20**, rejecting the question "what should the default crawl
rate be":

    "The entire thing seems completely backwards to me. The first thing we need
    to do is try to detect the system. So if you're saying Shopify class has
    certain rules, well, then we better check if it's Shopify and if it is, then
    follow their rules. And I bet there are other known things as well."

So this module answers the FIRST question — *what is this host* — from evidence
we already collect on every fetch: response headers and the HTML body. It is
pure: no network, no DB, no sibling matrx imports beyond the URL helper. The
fetch lives in the crawler; the pacing decision lives in ``host_pacing.py``.

**Why a registry and not an if-chain.** "I bet there are other known things as
well" is a growth instruction. A profile is one frozen dataclass in
:data:`PLATFORM_PROFILES` — adding Ghost or BigCommerce is one entry and one
test row, never a branch in a fetch path. Detection scores every profile against
the same evidence and returns the best match with the signals that fired, so a
wrong answer is diagnosable instead of mysterious.

**Honesty about the numbers.** ``sustained_rps`` is what we will *hold a host
to* until the ramp proves otherwise, and ``basis`` says where it came from:

* ``published`` — the platform documents a rate we can cite. Treated as a real
  ceiling, not a starting guess.
* ``observed`` — no published crawl rate exists; this is the rate at which we
  have measured this platform class starting to throttle. A ceiling hint.
* ``conservative`` — nothing published, nothing measured yet. A polite opening
  rate ONLY; the ramp is expected to climb past it.

Never write a number here you cannot defend in ``basis``. An invented
"documented limit" is worse than no profile at all, because it stops the ramp
from ever discovering the truth.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

__all__ = [
    "PlatformProfile",
    "PlatformMatch",
    "PLATFORM_PROFILES",
    "detect_platform",
    "profile_for",
]


@dataclass(frozen=True)
class PlatformProfile:
    """One known hosting platform, its fingerprints, and its crawl budget."""

    name: str
    display_name: str
    # Sustained requests/second we hold this platform to. None = the platform is
    # identified but says nothing about rate (a CDN in front of an unknown
    # origin); the ramp owns the number entirely.
    sustained_rps: float | None
    basis: str  # "published" | "observed" | "conservative"
    # One sentence a non-technical user can read in the UI explaining the rate.
    rationale: str
    # Header fingerprints: (header-name-lowercase, compiled value pattern|None).
    # A None pattern means "presence of the header is the signal".
    header_signals: tuple[tuple[str, re.Pattern[str] | None], ...] = ()
    # Body fingerprints, matched case-insensitively against the raw HTML.
    html_signals: tuple[re.Pattern[str], ...] = ()
    # A fronting layer (CDN/WAF) rather than the origin platform. Fronting
    # matches never beat an origin match — Cloudflare in front of WordPress is
    # WordPress, and reporting "cloudflare" there would lose the real answer.
    is_fronting: bool = False
    doc_url: str = ""
    aliases: tuple[str, ...] = field(default_factory=tuple)


def _h(name: str, pattern: str | None = None) -> tuple[str, re.Pattern[str] | None]:
    return (name.lower(), re.compile(pattern, re.I) if pattern else None)


def _b(pattern: str) -> re.Pattern[str]:
    return re.compile(pattern, re.I)


# ---------------------------------------------------------------------------
# The registry. Add a platform = add an entry (+ a row in
# tests/test_host_platform.py). Never add a branch to a fetch path.
# ---------------------------------------------------------------------------

PLATFORM_PROFILES: tuple[PlatformProfile, ...] = (
    PlatformProfile(
        name="shopify",
        display_name="Shopify",
        sustained_rps=2.0,
        basis="published",
        rationale=(
            "Shopify meters clients at 2 requests per second sustained (a leaky "
            "bucket that refills at 2/s); storefronts throttle on the same budget."
        ),
        doc_url="https://shopify.dev/docs/api/usage/rate-limits",
        header_signals=(
            _h("x-shopid"),
            _h("x-shopify-stage"),
            _h("x-sorting-hat-shopid"),
            _h("powered-by", r"shopify"),
        ),
        html_signals=(
            _b(r"cdn\.shopify\.com"),
            _b(r"Shopify\.theme"),
            _b(r'<meta[^>]+content=["\'][^"\']*shopify'),
        ),
    ),
    PlatformProfile(
        name="wordpress",
        display_name="WordPress",
        sustained_rps=3.0,
        basis="observed",
        rationale=(
            "WordPress publishes no crawl rate. Most installs are PHP rendering "
            "each page, so we open at 3/s and let the ramp find the real ceiling."
        ),
        header_signals=(
            _h("x-powered-by", r"w3\s*total\s*cache|wp\s*engine"),
            _h("x-pingback"),
            _h("link", r"/wp-json/"),
        ),
        html_signals=(
            _b(r"/wp-content/"),
            _b(r"/wp-includes/"),
            _b(r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']WordPress'),
            _b(r"/wp-json/"),
        ),
        aliases=("woocommerce",),
    ),
    PlatformProfile(
        name="wix",
        display_name="Wix",
        sustained_rps=2.0,
        basis="observed",
        rationale=(
            "Wix publishes no crawl rate and rate-limits aggressively at its edge; "
            "2/s is the rate at which we stop seeing 429s."
        ),
        header_signals=(
            _h("x-wix-request-id"),
            _h("x-wix-published-version"),
            _h("server", r"^Pepyaka"),
        ),
        html_signals=(_b(r"static\.wixstatic\.com"), _b(r"wix-?code|_wixCIDX")),
    ),
    PlatformProfile(
        name="squarespace",
        display_name="Squarespace",
        sustained_rps=2.0,
        basis="observed",
        rationale=(
            "Squarespace publishes no crawl rate; its edge returns 429 well before "
            "typical crawl speeds, so we open at 2/s."
        ),
        header_signals=(_h("x-contextid"), _h("server", r"Squarespace")),
        html_signals=(
            _b(r"static1\.squarespace\.com"),
            _b(r'<meta[^>]+content=["\']Squarespace'),
        ),
    ),
    PlatformProfile(
        name="webflow",
        display_name="Webflow",
        sustained_rps=3.0,
        basis="observed",
        rationale="Webflow serves static pages from its CDN and tolerates moderate rates.",
        header_signals=(_h("x-wf-forwarded-proto"), _h("x-wf-page-id")),
        html_signals=(_b(r"<html[^>]+data-wf-(page|site)"), _b(r"assets\.website-files\.com")),
    ),
    PlatformProfile(
        name="hubspot",
        display_name="HubSpot CMS",
        sustained_rps=2.0,
        basis="observed",
        rationale="HubSpot-hosted pages throttle at its edge; 2/s stays under it.",
        header_signals=(_h("x-hs-cache-config"), _h("x-hs-hub-id")),
        html_signals=(_b(r"(cdn2?|js)\.hs-(scripts|banner|analytics)\.com"), _b(r"hs-sites\.com")),
    ),
    PlatformProfile(
        name="bigcommerce",
        display_name="BigCommerce",
        sustained_rps=2.0,
        basis="observed",
        rationale="BigCommerce storefronts throttle like other hosted commerce edges.",
        header_signals=(_h("x-bc-cache-status"), _h("x-bc-storefront")),
        html_signals=(_b(r"cdn\d*\.bigcommerce\.com"),),
    ),
    PlatformProfile(
        name="drupal",
        display_name="Drupal",
        sustained_rps=3.0,
        basis="observed",
        rationale="Drupal publishes no crawl rate; like WordPress it renders per request.",
        header_signals=(_h("x-generator", r"drupal"), _h("x-drupal-cache")),
        html_signals=(
            _b(r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']Drupal'),
            _b(r"/sites/(default|all)/(files|themes|modules)/"),
        ),
    ),
    PlatformProfile(
        name="ghost",
        display_name="Ghost",
        sustained_rps=3.0,
        basis="observed",
        rationale="Ghost serves cached pages from Node; moderate rates are safe.",
        header_signals=(_h("x-ghost-cache-status"),),
        html_signals=(_b(r'<meta[^>]+content=["\']Ghost\s'),),
    ),
    PlatformProfile(
        name="duda",
        display_name="Duda",
        sustained_rps=2.0,
        basis="observed",
        rationale="Duda-hosted sites rate-limit at the edge like other site builders.",
        header_signals=(_h("x-duda-site-id"),),
        html_signals=(_b(r"(irp|static)\.cdn-website\.com"), _b(r"windows\.dmAPI")),
    ),
    # --- Fronting layers -------------------------------------------------
    # These identify WHO IS IN FRONT, never the origin platform. They carry no
    # sustained_rps of their own: a CDN is not a rate, and pinning one here
    # would clamp every origin behind it to the same guess.
    PlatformProfile(
        name="cloudflare",
        display_name="Cloudflare",
        sustained_rps=None,
        basis="conservative",
        rationale=(
            "Cloudflare fronts this host. It sets no crawl rate of its own, but a "
            "site-owner rule can throttle or challenge at any moment, so the ramp "
            "climbs more cautiously behind it."
        ),
        is_fronting=True,
        header_signals=(_h("cf-ray"), _h("server", r"^cloudflare")),
    ),
    PlatformProfile(
        name="fastly",
        display_name="Fastly",
        sustained_rps=None,
        basis="conservative",
        rationale="Fastly fronts this host; the origin's own limit is what matters.",
        is_fronting=True,
        header_signals=(_h("x-served-by", r"cache-"), _h("x-fastly-request-id")),
    ),
    PlatformProfile(
        name="akamai",
        display_name="Akamai",
        sustained_rps=None,
        basis="conservative",
        rationale="Akamai fronts this host; the origin's own limit is what matters.",
        is_fronting=True,
        header_signals=(_h("x-akamai-transformed"), _h("server", r"AkamaiGHost")),
    ),
)

_BY_NAME: dict[str, PlatformProfile] = {}
for _profile in PLATFORM_PROFILES:
    _BY_NAME[_profile.name] = _profile
    for _alias in _profile.aliases:
        _BY_NAME[_alias] = _profile


def profile_for(name: str | None) -> PlatformProfile | None:
    """The profile registered under ``name`` (or one of its aliases)."""
    if not name:
        return None
    return _BY_NAME.get(name.strip().lower())


@dataclass(frozen=True)
class PlatformMatch:
    """What we concluded, and the exact evidence that got us there."""

    profile: PlatformProfile
    signals: tuple[str, ...]
    fronted_by: PlatformProfile | None = None

    @property
    def name(self) -> str:
        return self.profile.name

    def describe(self) -> str:
        front = f" behind {self.fronted_by.display_name}" if self.fronted_by else ""
        return f"{self.profile.display_name}{front} ({', '.join(self.signals)})"


# Body scanning is capped: the fingerprints we look for are in the head and the
# asset URLs, and regexing a 5 MB page on every fetch is a cost with no payoff.
_HTML_SCAN_BYTES = 200_000


def detect_platform(
    *,
    headers: dict[str, str] | None = None,
    html: str | None = None,
) -> PlatformMatch | None:
    """Identify the host's platform from one response.

    Returns the ORIGIN platform when one is identifiable, carrying any fronting
    layer alongside it — never the CDN in its place. ``None`` means "we could
    not tell", which is a legitimate answer that hands the whole decision to the
    ramp; it is never guessed at.
    """

    lowered_headers = {k.lower(): (v or "") for k, v in (headers or {}).items()}
    body = (html or "")[:_HTML_SCAN_BYTES]

    origin_hits: list[tuple[int, PlatformProfile, tuple[str, ...]]] = []
    fronting_hits: list[tuple[int, PlatformProfile, tuple[str, ...]]] = []

    for profile in PLATFORM_PROFILES:
        signals: list[str] = []
        for header_name, pattern in profile.header_signals:
            value = lowered_headers.get(header_name)
            if value is None:
                continue
            if pattern is None or pattern.search(value):
                signals.append(f"header:{header_name}")
        if body:
            for pattern in profile.html_signals:
                if pattern.search(body):
                    signals.append(f"body:{pattern.pattern[:40]}")
        if not signals:
            continue
        # A header fingerprint is a statement by the SERVER; a body fingerprint
        # can be any asset a page happens to embed (one Shopify buy-button on a
        # WordPress page is not a Shopify site). Headers therefore score double.
        score = sum(2 if s.startswith("header:") else 1 for s in signals)
        target = fronting_hits if profile.is_fronting else origin_hits
        target.append((score, profile, tuple(signals)))

    fronted_by = max(fronting_hits, key=lambda hit: hit[0])[1] if fronting_hits else None

    if origin_hits:
        score, profile, signals = max(origin_hits, key=lambda hit: hit[0])
        return PlatformMatch(profile=profile, signals=signals, fronted_by=fronted_by)

    if fronted_by is not None:
        best = max(fronting_hits, key=lambda hit: hit[0])
        # Nothing identified the origin — the fronting layer IS the answer we
        # have, and it is reported as itself rather than dressed up as a CMS.
        return PlatformMatch(profile=best[1], signals=best[2], fronted_by=None)

    return None
