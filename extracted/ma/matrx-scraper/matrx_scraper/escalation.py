"""When a plain HTTP fetch fails, hand the URL to the server browser.

Arman spent nine months on the scraper and three more on a browser that runs on
the server and scrapes when scrapers fail. On 2026-09-17 a hunt proved the
browser works — Zillow went from `bad_status` to **1,061 real listings with
prices and addresses** the moment someone pointed the browser at it by hand —
and proved that nothing was wired to do that automatically: browser rescue
existed in exactly two narrow pipelines (the research auto-scraper's ingest and
the site crawler), and the one screen a human actually uses re-ran the same
non-browser fetch.

This module is the missing policy, and it lives at the level every caller
inherits (`orchestrator.scrape()`), not in an endpoint. Three rules:

1. **Escalate on a named class of failure**, never on everything — a 404 is a
   404 in any engine, and each browser render holds one of a handful of pooled
   browsers shared with live crawls.
2. **Announce it.** The result always says which engine produced it and, when
   it escalated, why. A silent engine switch is the automation that fails
   quietly, which is the thing the owner has asked us not to build.
3. **A setting controls it**, with a default that serves the common case.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

#: Engine names carried on every result. Closed vocabulary.
ENGINE_HTTP = "http"
ENGINE_BROWSER = "browser"
ENGINE_CACHE = "cache"

#: Failure/warning reasons a rendering browser can plausibly beat. Each one is
#: here because the hunt saw the browser (or a human's own browser) succeed
#: where the HTTP client did not.
ESCALATABLE_REASONS: frozenset[str] = frozenset(
    {
        # The site's edge refused our HTTP client (403/429/999/bot-wall status).
        "bad_status",
        # A WAF interstitial — a real browser runs the challenge script.
        "cloudflare_block",
        # HTML arrived but the text is a JS shell (Airbnb, Reddit, Best Buy,
        # Scribd, Crunchyroll all landed here with 0–38 characters).
        "low_text_content",
        "empty_content",
        "thin_content",
        # The transport itself broke. `proxy_error` stays OUT: it is our own
        # infrastructure, it is already rescued by a direct connection in
        # `scraper.fetch_normally_with_proxy`, and spending a pooled browser on
        # our vendor's outage would hide the outage instead of reporting it.
        "request_error",
    }
)

#: Content types a headless browser cannot help with — it renders pages, and
#: pointing it at a 40 MB PDF costs a pooled browser for nothing.
NON_RENDERABLE_CONTENT_TYPES: frozenset[str] = frozenset(
    {"pdf", "json", "xml", "txt", "image", "unknown"}
)

_TRUE = {"1", "true", "yes", "on"}
_FALSE = {"0", "false", "no", "off"}


@dataclass(frozen=True)
class EscalationPolicy:
    """Whether, and on what, a failed HTTP scrape reaches for the browser."""

    enabled: bool = True
    reasons: frozenset[str] = ESCALATABLE_REASONS

    @classmethod
    def from_env(cls) -> EscalationPolicy:
        """`SCRAPER_BROWSER_ESCALATION` — the deployment-level knob.

        Default ON: the whole point of owning a server browser is that the
        person asking for a page does not have to know it exists. An operator
        who needs to protect the browser pool (or reproduce a raw HTTP result)
        turns it off in one place, and every caller follows.
        """
        raw = (os.getenv("SCRAPER_BROWSER_ESCALATION") or "").strip().lower()
        if raw in _FALSE:
            return cls(enabled=False)
        return cls(enabled=True)

    def wants(self, reason: str | None) -> bool:
        return bool(self.enabled and reason and reason in self.reasons)


def can_render(content_type: str | None) -> bool:
    """Is this the kind of resource a browser render could improve?"""
    return (content_type or "").lower() not in NON_RENDERABLE_CONTENT_TYPES


def escalation_sentence(reason: str) -> str:
    """One plain-English line a non-technical person can read on a screen."""
    return {
        "bad_status": (
            "The site refused our normal request, so we opened the page in our "
            "server browser instead."
        ),
        "cloudflare_block": (
            "The site showed a bot check to our normal request, so we opened the "
            "page in our server browser instead."
        ),
        "low_text_content": (
            "The page arrived empty because its content is drawn by the browser, "
            "so we rendered it in our server browser."
        ),
        "empty_content": (
            "The page arrived empty because its content is drawn by the browser, "
            "so we rendered it in our server browser."
        ),
        "thin_content": (
            "Almost no text came back on the first try, so we rendered the page in "
            "our server browser to get the rest."
        ),
        "request_error": (
            "The normal connection to the site failed, so we opened the page in our "
            "server browser instead."
        ),
    }.get(reason, "The normal fetch did not work, so we used our server browser instead.")
