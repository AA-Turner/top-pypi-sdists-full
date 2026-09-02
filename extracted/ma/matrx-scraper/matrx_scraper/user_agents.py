"""The ONE definition of a crawl User-Agent override — value, validation, presets.

Why this exists as its own module: the override has to be identical in four
places that must not import each other — the request contract
(`web_crawl.contracts`), the crawler (`crawler`), the HTTP transport
(`scraper`), and the browser pool (`browser_pool`). A second copy of the
validation rule in any of them is how a UA that a request accepted becomes a
UA the browser silently drops.

THE CENTRAL INVARIANT — an override is either absent or complete:

    normalize_user_agent(None)   -> None   # use the platform default
    normalize_user_agent("")     -> None   # SAME THING, never an empty header
    normalize_user_agent("  ")   -> None
    normalize_user_agent("Bot/1") -> "Bot/1"

`None` means "send whatever we send today" at every layer. An empty string must
never survive as an override, because an empty `User-Agent:` header is not a
neutral default — it is a distinct, frequently blocked signal that makes a
crawl behave WORSE than sending nothing at all.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# CAPS — configuration lives in code, never in an env var (repo doctrine).
# ---------------------------------------------------------------------------

# Our honest self-identification. This is what a site owner should see in their
# access log when they ask "what is hitting my server?", and it is the value
# behind the "Our crawler" preset. It is NOT applied automatically: leaving the
# override unset preserves today's transport behaviour exactly (see FEATURE.md).
MATRX_CRAWLER_USER_AGENT = "MatrxCrawler/1.0 (+https://aimatrx.com/crawler)"

# A UA header longer than this is a defect, not a preference. Real-world agents
# top out near 200 chars; servers and CDNs commonly reject or truncate past 1KB,
# and an unbounded string is stored in `web.crawl_preset.config` forever.
MAX_USER_AGENT_LENGTH = 512


class InvalidUserAgentError(ValueError):
    """A UA override that cannot be sent as an HTTP header."""


# ---------------------------------------------------------------------------
# Named presets — the affordance a NON-TECHNICAL user actually picks from.
#
# The person configuring a crawl is a Subject Matter Expert, not a browser
# engineer: they know "I want to see what Google sees", never
# "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)".
# A raw text box is the ESCAPE HATCH, never the primary control. Any UI that
# surfaces this field renders THIS list as the primary affordance — it is
# served to clients so a second, drifting copy is never hand-typed into a
# frontend.
# ---------------------------------------------------------------------------


class UserAgentPreset:
    """One named, human-labelled UA choice."""

    __slots__ = ("key", "label", "description", "value")

    def __init__(self, key: str, label: str, description: str, value: str | None) -> None:
        self.key = key
        self.label = label
        self.description = description
        # `None` is a real, meaningful value here: the "Default" preset means
        # "do not override", which is NOT the same as sending our bot UA.
        self.value = value

    def as_dict(self) -> dict[str, str | None]:
        return {
            "key": self.key,
            "label": self.label,
            "description": self.description,
            "value": self.value,
        }


USER_AGENT_PRESETS: tuple[UserAgentPreset, ...] = (
    UserAgentPreset(
        key="default",
        label="Default (recommended)",
        description=(
            "Crawl the way a normal visitor's browser would. Best for seeing the "
            "page your real customers get."
        ),
        value=None,
    ),
    UserAgentPreset(
        key="matrx",
        label="Our crawler",
        description=(
            "Identify ourselves honestly in the site's server logs. Use this when "
            "the site owner wants to see our visits, or needs to allow us through."
        ),
        value=MATRX_CRAWLER_USER_AGENT,
    ),
    UserAgentPreset(
        key="googlebot",
        label="Googlebot",
        description=(
            "See the page the way Google's crawler sees it. Useful when a page "
            "ranks differently than it looks."
        ),
        value=("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"),
    ),
    UserAgentPreset(
        key="googlebot_mobile",
        label="Googlebot (mobile)",
        description=(
            "Google indexes most sites with its phone crawler. Use this to check "
            "what Google's mobile-first indexing actually reads."
        ),
        value=(
            "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile "
            "Safari/537.36 (compatible; Googlebot/2.1; "
            "+http://www.google.com/bot.html)"
        ),
    ),
    UserAgentPreset(
        key="bingbot",
        label="Bingbot",
        description="See the page the way Microsoft Bing's crawler sees it.",
        value=("Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"),
    ),
    UserAgentPreset(
        key="iphone_safari",
        label="iPhone Safari",
        description=(
            "Pretend to be a real iPhone. Use this when a site serves different content to phones."
        ),
        value=(
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 "
            "Safari/604.1"
        ),
    ),
    UserAgentPreset(
        key="chrome_desktop",
        label="Chrome on Windows",
        description="Pretend to be a desktop Chrome browser on Windows.",
        value=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        ),
    ),
)

PRESETS_BY_KEY: dict[str, UserAgentPreset] = {p.key: p for p in USER_AGENT_PRESETS}


def preset_value(key: str) -> str | None:
    """The UA string for a preset key. Raises on an unknown key — a typo must
    never silently degrade to "no override"."""
    try:
        return PRESETS_BY_KEY[key].value
    except KeyError:
        raise InvalidUserAgentError(
            f"unknown user_agent preset {key!r}; known: {sorted(PRESETS_BY_KEY)}"
        ) from None


def presets_payload() -> list[dict[str, str | None]]:
    """The preset list as a client sees it."""
    return [p.as_dict() for p in USER_AGENT_PRESETS]


# ---------------------------------------------------------------------------
# Validation / normalization
# ---------------------------------------------------------------------------


def normalize_user_agent(value: str | None) -> str | None:
    """The ONE gate every UA override passes through.

    Returns the cleaned override, or ``None`` meaning "no override — use the
    platform default". Raises `InvalidUserAgentError` for a value that cannot
    legally be sent as an HTTP header.
    """
    if value is None:
        return None
    if not isinstance(value, str):
        raise InvalidUserAgentError(f"user_agent must be a string, got {type(value).__name__}")

    cleaned = value.strip()
    if not cleaned:
        # Empty / whitespace-only is "use the default", NEVER an empty header.
        return None

    if len(cleaned) > MAX_USER_AGENT_LENGTH:
        raise InvalidUserAgentError(
            f"user_agent must be at most {MAX_USER_AGENT_LENGTH} characters, got {len(cleaned)}"
        )

    # Control characters are the real hazard here, not exotic text. A raw CR or
    # LF inside a header value is HTTP header injection; a NUL or other C0/C1
    # byte is rejected outright by httpx/curl and silently mangled by others.
    # Checked on the ORIGINAL value, not the stripped one, so an embedded
    # newline can never hide behind the strip().
    for index, char in enumerate(value):
        code = ord(char)
        if code < 0x20 or code == 0x7F or 0x80 <= code <= 0x9F:
            raise InvalidUserAgentError(
                f"user_agent must not contain control characters "
                f"(found U+{code:04X} at position {index})"
            )

    # Header values are latin-1 on the wire. A UA carrying an emoji or a
    # non-latin-1 character raises deep inside the transport, mid-crawl, per
    # URL — reject it once, here, where the caller can still fix it.
    try:
        cleaned.encode("latin-1")
    except UnicodeEncodeError as exc:
        raise InvalidUserAgentError(
            "user_agent must contain only latin-1 characters "
            f"(offending character at position {exc.start})"
        ) from None

    return cleaned
