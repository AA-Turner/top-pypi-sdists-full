"""The outlet-logo ladder, resolved BEFORE any surgery.

Order (newsjack press-clip, T2 step 3): explicit ``logo_url`` → the article
page's masthead → the outlet home page's masthead → ``og:logo`` or the favicon
→ a text wordmark. The last rung is reported as ``text_wordmark`` and a clip
carrying it is NOT shippable — the source is always said out loud.

The detectors are injected so the order is testable without a browser; the
renderer passes closures over real pages.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Literal

LogoSource = Literal[
    "explicit", "article_masthead", "home_masthead", "og_logo_or_favicon", "text_wordmark"
]
Masthead = tuple[str, str]  # (image src, inline svg markup) — either may be ""


@dataclass
class LogoResolution:
    source: LogoSource
    url: str | None = None
    svg: str | None = None
    notes: list[str] = field(default_factory=list)


async def resolve_logo(
    *,
    explicit_url: str | None,
    article_masthead: Callable[[], Awaitable[Masthead]],
    home_masthead: Callable[[], Awaitable[Masthead]],
    fallback: Callable[[], Awaitable[str]],
) -> LogoResolution:
    if explicit_url and explicit_url.strip():
        return LogoResolution("explicit", url=explicit_url.strip())

    notes: list[str] = []
    src, svg = await article_masthead()
    if src or svg:
        return LogoResolution("article_masthead", url=src or None, svg=svg or None)

    try:
        src, svg = await home_masthead()
        if src or svg:
            return LogoResolution("home_masthead", url=src or None, svg=svg or None, notes=notes)
        notes.append("The outlet's home page has no masthead logo either.")
    except Exception as exc:  # noqa: BLE001 — the home page is best-effort, and says so
        notes.append(f"The outlet's home page could not be read for a logo: {exc}")

    url = await fallback()
    if url:
        return LogoResolution("og_logo_or_favicon", url=url, notes=notes)

    notes.append(
        "No logo was found on the article, the home page, og:logo or the favicon; the clip "
        "carries a text wordmark and is not shippable. Re-run with logo_url set to the "
        "outlet's real logo."
    )
    return LogoResolution("text_wordmark", notes=notes)


__all__ = ["LogoResolution", "LogoSource", "resolve_logo"]
