"""The content-sanity gate — a scrape with nothing in it is never a success.

Three results in the 2026-09-17 block hunt came back HTTP-successful, with no
error of any kind, and **zero extracted characters**: a real text-native arXiv
PDF, a real Supreme Court opinion from CourtListener, and Scribd's SPA shell.
The human watching the screen saw "Untitled Page" and no red banner —
indistinguishable from "there was nothing there" when the truth was "we have
your document and extracted nothing from it". A fourth, Pinterest, answered a
request for one creator's profile with a *different* creator's empty profile
and called that a success too.

That is worse than an honest wall: an honest `cloudflare_block` tells a person
to try something else, while a silent empty tells them the source is worthless.

This module is the one place that decides whether a parsed result actually
carries content for the resource that was asked for. Every caller of
`orchestrator.scrape()` inherits it — it is not a property of one endpoint.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

#: Below this many characters of extracted text a page is REPORTED as thin.
#: Calibrated against the block hunt: the genuine successes bottomed out at
#: ~978 chars (a Hacker News thread) and ~1,679 (an Issuu category), while the
#: silent failures were 0, 34 and 38 chars (unrendered SPA templates). 200
#: sits in the empty gap between them, so a genuinely short page — a one-line
#: answer, a stub — is reported thin but NOT failed.
THIN_CONTENT_CHARS = 200

#: Reason names. Closed vocabulary — a caller may branch on these.
EMPTY_CONTENT = "empty_content"
THIN_CONTENT = "thin_content"
WRONG_RESOURCE = "wrong_resource"


@dataclass(frozen=True)
class SanityVerdict:
    """What the gate concluded. `failure_reason` None means "let it through"."""

    content_chars: int
    failure_reason: str | None = None
    #: Set even when the result is allowed through — honest, not fatal.
    warning: str | None = None
    #: Plain English, safe to show a non-technical person verbatim.
    message: str | None = None
    #: True when the server answered from a different path than was requested.
    redirected_off_requested_path: bool = False

    @property
    def is_failure(self) -> bool:
        return self.failure_reason is not None


def _normalize_path(url: str) -> tuple[str, str]:
    """(host, path) with the differences that are never a substitution
    removed: scheme, `www.`, case, and a trailing slash."""
    parsed = urlparse(url or "")
    host = (parsed.hostname or "").lower().removeprefix("www.")
    path = (parsed.path or "/").rstrip("/").lower() or "/"
    return host, path


def resource_changed(requested_url: str, response_url: str) -> bool:
    """Did we end up at a materially different resource than we asked for?

    Scheme upgrades, `www.` and trailing-slash normalisation are NOT changes.
    A request for `/abeautifulmess` answered from `/goldencoveco` is — that is
    the Pinterest decoy, and it must never pass as a plain success.
    """
    if not response_url or not requested_url:
        return False
    req_host, req_path = _normalize_path(requested_url)
    res_host, res_path = _normalize_path(response_url)
    if req_path == "/":
        # A bare homepage request lands wherever the site's front door leads.
        return req_host != res_host and bool(req_host) and bool(res_host)
    return (req_host, req_path) != (res_host, res_path)


def extracted_text_length(result: Any) -> int:
    """Longest real text the parse produced, across every field a consumer
    would read. Deliberately generous: the gate must only fire when NO field
    has content, never because one preferred field happened to be empty."""
    candidates = (
        getattr(result, "text_data", None),
        getattr(result, "ai_research_content", None),
        getattr(result, "ai_content", None),
        getattr(result, "markdown_renderable", None),
        getattr(result, "main_content_text", None),
        getattr(result, "raw_text", None),
    )
    best = 0
    for value in candidates:
        if isinstance(value, str):
            best = max(best, len(value.strip()))
    return best


def assess(result: Any, *, thin_chars: int = THIN_CONTENT_CHARS) -> SanityVerdict:
    """Judge a parsed `ScrapeResult`. Only ever downgrades, never upgrades."""
    chars = extracted_text_length(result)
    changed = resource_changed(
        getattr(result, "url", "") or "", getattr(result, "response_url", "") or ""
    )

    if not getattr(result, "success", False):
        # Already an honest failure — the gate adds evidence, not a verdict.
        return SanityVerdict(content_chars=chars, redirected_off_requested_path=changed)

    if chars == 0:
        if changed:
            return SanityVerdict(
                content_chars=0,
                failure_reason=WRONG_RESOURCE,
                redirected_off_requested_path=True,
                message=(
                    "The site answered with a different page than the one requested, "
                    "and that page had no readable content. The content you asked for "
                    "was not returned."
                ),
            )
        return SanityVerdict(
            content_chars=0,
            failure_reason=EMPTY_CONTENT,
            message=(
                "We reached this page successfully but could not read any text out of "
                "it. That usually means the content is drawn by the browser after the "
                "page loads, or the document is a scan we could not read."
            ),
        )

    if chars < thin_chars:
        return SanityVerdict(
            content_chars=chars,
            warning=THIN_CONTENT,
            redirected_off_requested_path=changed,
            message=(
                f"Only {chars} characters of text came back — this is very likely a "
                "page shell rather than the real content."
            ),
        )

    if changed:
        return SanityVerdict(
            content_chars=chars,
            warning=WRONG_RESOURCE,
            redirected_off_requested_path=True,
            message=(
                "The site answered from a different address than the one requested. "
                "Check that this is the content you meant."
            ),
        )

    return SanityVerdict(content_chars=chars, redirected_off_requested_path=False)
