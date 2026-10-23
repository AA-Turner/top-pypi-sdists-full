"""The bot-wall / interstitial CENSUS — the fetcher's one challenge classifier.

Pure and light on purpose: ``enum`` and ``selectolax`` only, no network client, no
``load_dotenv``, no side effects at import. ``scraper`` (every fetch path) and
``seo_audit`` (the app-shell test) both read the census from here, so a wall is the
same wall everywhere and asking "is this a wall?" never imports the HTTP stack.
"""

from __future__ import annotations

import enum

from selectolax.parser import HTMLParser


class FailureReason(enum.StrEnum):
    NON_HTML_CONTENT = "non_html_content"
    LOW_TEXT_CONTENT = "low_text_content"
    BAD_STATUS = "bad_status"
    PARSE_ERROR = "parse_error"
    CLOUDFLARE_BLOCK = "cloudflare_block"
    BLOCKED = "blocked"
    #: The redirect chain came back to a URL it already visited. Persisted as
    #: `web.crawl_url.reason_code='redirect_loop'` with the chain (revisit last).
    REDIRECT_LOOP = "redirect_loop"
    REQUEST_ERROR = "request_error"
    PROXY_ERROR = "proxy_error"
    #: The address (or a redirect hop) resolves inside a private or internal
    #: network. WE refused it before sending anything; no retry, proxy, direct
    #: fallback or browser changes that.
    ADDRESS_REFUSED = "address_refused"


CLOUDFLARE_RETRY_CSS_SELECTORS = [
    '#turnstile-wrapper iframe[src^="https://challenges.cloudflare.com"]',
]

RETRY_CSS_SELECTORS = [
    *CLOUDFLARE_RETRY_CSS_SELECTORS,
    'div#infoDiv0 a[href*="//www.google.com/policies/terms/"]',
    'iframe[src*="_Incapsula_Resource"]',
]

# A bot-protection interstitial is a BLOCK, not a status code — and it can be
# served with ANY status. Whoever consumes `failed_primary_reason` (the crawler's
# browser escalation, the retry policy, the UI) needs the specific diagnosis, so
# these outrank every other reason regardless of append order.
CHALLENGE_FAILURE_REASONS = (
    FailureReason.CLOUDFLARE_BLOCK,
    FailureReason.BLOCKED,
)


CHALLENGE_TITLE_MARKERS = ("cloudflare", "attention required", "just a moment")

# THE CHALLENGE CENSUS (2026-09-26: a Reddit "Prove your humanity" page landed as a Source).
# Every interstitial below is a wall, whatever status it is served with. Titles are exact
# phrases a vendor's challenge page uses; body phrases are matched only on a SHORT page (a real
# article that happens to embed a captcha on its comment form is not a wall).
BLOCK_TITLE_MARKERS = (
    "prove your humanity",          # Reddit
    "verify you are human",         # Cloudflare Turnstile / generic
    "are you a robot",              # generic
    "robot or human",               # Walmart / PerimeterX variants
    "human verification",           # generic
    "pardon our interruption",      # Imperva / Distil
    "one more step",                # Cloudflare (legacy captcha)
    "checking your browser",        # Cloudflare (legacy) / DDoS-Guard
    "ddos-guard",                   # DDoS-Guard
    "access denied",                # Akamai edge refusal ("Reference #…")
    "security check",               # generic
    "the request could not be satisfied",  # AWS CloudFront 403 ("ERROR: The request could not be satisfied")
)
BLOCK_BODY_MARKERS = (
    "prove your humanity",
    "let us know you're a real person",
    "let us know you’re a real person",
    "verify you are human",
    "checking if the site connection is secure",   # Cloudflare
    "enable javascript and cookies to continue",   # Cloudflare
    "press & hold",                                # PerimeterX
    "please verify you are a human",               # PerimeterX
    "why have i been blocked",                     # Cloudflare block page
    "you don't have permission to access",         # Akamai "Access Denied … Reference #"
    "request unsuccessful. incapsula incident id", # Imperva
    "the request could not be satisfied",          # AWS CloudFront 403
    "please complete the security check",          # Cloudflare legacy captcha ("One more step")
    "completing the captcha proves you are a human",  # Cloudflare legacy captcha
    "let's confirm you are human",                 # generic "Human Verification"
    # Owner-approved wall phrases (advanced-reader design, 2026-10-16) — short pages only.
    "verifying you are not a robot",
    "verify you are not a robot",
    "are you human",
    "robot or human",
    "access denied",
    # Walls seen as SUCCESSFUL thin rows in scraper.scrape_parsed_page (2026-10-19 sweep).
    "activate and hold the button",                # Walmart / PerimeterX "Robot or human?"
    "you have been blocked",                       # Cloudflare "Sorry, you have been blocked"
    "request blocked. we can't connect",           # CloudFront 403 variant
    "click the button below to continue shopping", # Amazon bot interstitial
    "we are optimizing your request",              # generic wait screen
    "confirm you are human",                       # "Let's confirm you are human"
    "complete the security check",                 # "One more step" captcha
)
BLOCK_WIDGET_SELECTORS = (
    'iframe[src*="hcaptcha.com"]',
    "div.h-captcha",
    'iframe[src*="google.com/recaptcha"]',
    "div.g-recaptcha",
    "#px-captcha",                                  # PerimeterX
    'script[src*="captcha-delivery.com"]',          # DataDome
    'iframe[src*="captcha-delivery.com"]',
)
#: A page at or under this much visible text that shows a challenge phrase or widget is the
#: wall itself, not an article with a captcha somewhere on it.
SHORT_PAGE_CHARS = 2000


def detect_challenge_reasons(
    *,
    soup: HTMLParser | None = None,
    html: str | None = None,
    title: str | None = None,
) -> list[dict]:
    """Bot-protection signatures in a response — ONE classifier, every fetch path.

    The HTTP path passes its already-parsed soup; the crawler's browser capture
    passes raw HTML. A second hand-rolled copy of these checks is exactly how
    the browser path came to label every challenge `bad_status`.
    """
    if soup is None and html:
        try:
            soup = HTMLParser(html)
        except Exception:
            soup = None
    reasons: list[dict] = []
    if soup is not None:
        for selector in RETRY_CSS_SELECTORS:
            if soup.css_first(selector):
                reason = (
                    FailureReason.CLOUDFLARE_BLOCK
                    if selector in CLOUDFLARE_RETRY_CSS_SELECTORS
                    else FailureReason.BLOCKED
                )
                reasons.append({reason: f"Selector matched: {selector}"})
    if title and any(marker in title.lower() for marker in CHALLENGE_TITLE_MARKERS):
        reasons.append({FailureReason.CLOUDFLARE_BLOCK: f"Title indicates block: {title}"})
    elif title and any(marker in title.lower() for marker in BLOCK_TITLE_MARKERS):
        reasons.append({FailureReason.BLOCKED: f"Title is a bot challenge: {title}"})
    if not reasons and soup is not None:
        body = soup.body
        text = " ".join((body.text(separator=" ") if body is not None else "").split()).lower()
        if len(text) <= SHORT_PAGE_CHARS:
            phrase = next((m for m in BLOCK_BODY_MARKERS if m in text), None)
            if phrase:
                reasons.append({FailureReason.BLOCKED: f"Page is a bot challenge: {phrase!r}"})
            else:
                widget = next((sel for sel in BLOCK_WIDGET_SELECTORS if soup.css_first(sel)), None)
                if widget:
                    reasons.append({FailureReason.BLOCKED: f"Short page is a captcha: {widget}"})
    return reasons


def challenge_text_reason(*, title: str | None, text: str | None) -> str | None:
    """The same census over a page already reduced to TITLE + TEXT (no HTML kept).

    For consumers that stored only the extracted text of a capture — coverage keeps an
    excerpt, not the DOM. Only a SHORT page can be the wall itself: a long article whose
    title happens to contain "Access Denied" is an article.
    """
    body = " ".join((text or "").split()).lower().replace("\u2019", "'")
    if len(body) > SHORT_PAGE_CHARS:
        return None
    lowered_title = (title or "").strip().lower().replace("\u2019", "'")
    marker = next(
        (m for m in (*CHALLENGE_TITLE_MARKERS, *BLOCK_TITLE_MARKERS) if lowered_title and m in lowered_title),
        None,
    )
    if marker:
        return f"the page title is a bot or access wall ({title!s})"
    phrase = next((m for m in BLOCK_BODY_MARKERS if m in body), None)
    if phrase:
        return f"the page is a bot or access wall ({phrase!r})"
    return None


__all__ = [
    "BLOCK_BODY_MARKERS",
    "BLOCK_TITLE_MARKERS",
    "BLOCK_WIDGET_SELECTORS",
    "CHALLENGE_FAILURE_REASONS",
    "CHALLENGE_TITLE_MARKERS",
    "CLOUDFLARE_RETRY_CSS_SELECTORS",
    "FailureReason",
    "RETRY_CSS_SELECTORS",
    "SHORT_PAGE_CHARS",
    "challenge_text_reason",
    "detect_challenge_reasons",
]
