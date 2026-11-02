"""HTML scrape discovery strategy with structured scrape diagnostics.

Wraps the existing HTML-based suggestion scraper from
``apply_thread_autofix.py`` and normalizes token/scrape failures into
structured discovery attempts.

This is the tertiary (lowest priority) discovery strategy — it activates
only when both GraphQL and REST strategies return empty.
"""

from __future__ import annotations

import logging
import os
import time

from agentic_devtools.cli.ci.pipeline.discovery.models import (
    DiscoveryAttempt,
    DiscoveryOutcome,
)
from agentic_devtools.cli.ci.pipeline.suggestions import SuggestedChange
from agentic_devtools.cli.ci.provider import CIPlatformProvider

logger = logging.getLogger(__name__)

# SAML/SSO indicators in response body (first 2KB checked)
_SAML_INDICATORS = ("SAMLRequest", "RelayState", "saml2/", "SingleSignOnService")


def _detect_saml_redirect(status_code: int, headers: dict, body_prefix: str) -> bool:
    """Check if a response indicates SAML/SSO redirect.

    Reserved for lower-level scraper integration when raw HTTP response
    details become available.

    Args:
        status_code: HTTP response status code.
        headers: Response headers (lowercase keys).
        body_prefix: First 2KB of response body.

    Returns:
        True if SAML/SSO redirect is detected.
    """
    # HTTP 403 with SAML indicators
    if status_code == 403:
        for indicator in _SAML_INDICATORS:
            if indicator in body_prefix:
                return True

    # Redirect to SSO endpoint
    location = headers.get("location", "")
    if location and any(sso in location for sso in ("saml2/", "sso/", "login/saml", "auth/saml")):
        return True

    # Body contains SAML form elements
    for indicator in _SAML_INDICATORS:
        if indicator in body_prefix:
            return True

    return False


def html_discover(
    provider: CIPlatformProvider,
    pr_number: int,
    repo: str,
) -> tuple[list[SuggestedChange], DiscoveryAttempt]:
    """Detect Copilot autofix candidates by scraping the PR page HTML.

    Wraps the existing HTML scraping logic from ``apply_thread_autofix``
    module, adding structured diagnostics around token acquisition and
    scrape execution.

    **This strategy never returns a populated suggestions list.**  It
    signals the presence of autofix candidates via
    ``DiscoveryAttempt.outcome == SUCCESS`` and
    ``DiscoveryAttempt.suggestion_count``.  The orchestrator treats a
    SUCCESS outcome as a cue to invoke the legacy
    ``_apply_copilot_autofix_suggestions`` fallback directly, rather than
    passing discrete ``SuggestedChange`` objects upstream.

    Args:
        provider: CI platform provider (not currently used; reserved for
            future lower-level scraper integration).
        pr_number: Pull request number.
        repo: Repository in "owner/repo" format.

    Returns:
        Tuple of (always-empty suggestions list, discovery attempt record).
        Callers must inspect ``attempt.outcome`` and
        ``attempt.suggestion_count`` rather than the suggestions list to
        determine whether autofix candidates were detected.
    """
    start = time.monotonic()

    if not repo:
        duration_ms = int((time.monotonic() - start) * 1000)
        return [], DiscoveryAttempt(
            method="html-scrape",
            outcome=DiscoveryOutcome.ERROR,
            duration_ms=duration_ms,
            error_message="Repository name could not be determined",
        )

    try:
        from agentic_devtools.cli.github.apply_thread_autofix import (
            _fetch_suggestions_from_page,
            _get_gh_token,
        )
    except ImportError as exc:
        duration_ms = int((time.monotonic() - start) * 1000)
        return [], DiscoveryAttempt(
            method="html-scrape",
            outcome=DiscoveryOutcome.ERROR,
            duration_ms=duration_ms,
            error_message=f"Import error: {exc}",
        )

    try:
        token = _get_gh_token()
    except (SystemExit, Exception) as exc:
        duration_ms = int((time.monotonic() - start) * 1000)
        github_token_present = bool(os.environ.get("GITHUB_TOKEN"))
        logger.warning(
            "[SCRAPE-FORMAT] Token acquisition failed (github_token_present=%s): %s",
            github_token_present,
            exc,
        )
        return [], DiscoveryAttempt(
            method="html-scrape",
            outcome=DiscoveryOutcome.ERROR,
            duration_ms=duration_ms,
            error_message=f"Token acquisition failed: {exc}",
        )

    try:
        raw_suggestions = _fetch_suggestions_from_page(repo, pr_number, token)
    except Exception as exc:
        duration_ms = int((time.monotonic() - start) * 1000)
        logger.warning(
            "[SCRAPE-FORMAT] HTML scrape exception: %s",
            exc,
        )
        return [], DiscoveryAttempt(
            method="html-scrape",
            outcome=DiscoveryOutcome.ERROR,
            duration_ms=duration_ms,
            error_message=str(exc),
        )

    duration_ms = int((time.monotonic() - start) * 1000)

    if not raw_suggestions:
        # Log diagnostic info for empty results
        logger.info(
            "[SCRAPE-FORMAT] HTML scrape returned 0 suggestions for PR #%d (repo=%s, duration_ms=%d)",
            pr_number,
            repo,
            duration_ms,
        )
        return [], DiscoveryAttempt(
            method="html-scrape",
            outcome=DiscoveryOutcome.EMPTY,
            duration_ms=duration_ms,
        )

    candidate_count = 0
    for raw in raw_suggestions:
        diff_entries = raw.get("diff_entries", [])
        for entry in diff_entries:
            if entry.get("path", ""):
                candidate_count += 1

    if candidate_count > 0:
        return [], DiscoveryAttempt(
            method="html-scrape",
            outcome=DiscoveryOutcome.SUCCESS,
            suggestion_count=candidate_count,
            duration_ms=duration_ms,
        )

    return [], DiscoveryAttempt(
        method="html-scrape",
        outcome=DiscoveryOutcome.EMPTY,
        duration_ms=duration_ms,
    )
