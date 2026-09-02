"""Browser-driven discovery strategy (opt-in, EMU/SSO).

Fourth, opt-in discovery tier that drives the GitHub PR Conversation page via
Playwright to detect Copilot autofix suggestions that the GraphQL/REST/HTML tiers
cannot recover inside an EMU/SSO tenant.

It mirrors the fail-open contract of ``html_strategy``: it **never returns a
populated suggestions list**. Instead it signals candidate presence via
``DiscoveryAttempt.outcome == SUCCESS`` and ``DiscoveryAttempt.suggestion_count``.

Gating on the ``ENABLE_BROWSER_APPLY_SUGGESTIONS`` env flag is performed by the
orchestrator (so it is never invoked when the flag is off). Playwright and pyotp
are imported lazily inside the driver; when they are missing this strategy
returns a clean EMPTY attempt so the pipeline proceeds exactly as before.
"""

from __future__ import annotations

import logging
import time

from agentic_devtools.cli.ci.pipeline.discovery.models import (
    DiscoveryAttempt,
    DiscoveryOutcome,
)
from agentic_devtools.cli.ci.pipeline.suggestions import SuggestedChange
from agentic_devtools.cli.ci.provider import CIPlatformProvider

logger = logging.getLogger(__name__)


def browser_discover(
    provider: CIPlatformProvider,
    pr_number: int,
    repo: str,
) -> tuple[list[SuggestedChange], DiscoveryAttempt]:
    """Detect Copilot autofix candidates by driving the PR Conversation page.

    **This strategy never returns a populated suggestions list.** It signals the
    presence of autofix candidates via ``DiscoveryAttempt.outcome == SUCCESS`` and
    ``DiscoveryAttempt.suggestion_count`` (mirroring ``html_discover``).

    Fail-open: any error is converted into a ``DiscoveryAttempt`` and never raised
    into the pipeline. Missing optional dependencies yield a clean EMPTY attempt.

    Args:
        provider: CI platform provider (reserved for future use).
        pr_number: Pull request number.
        repo: Repository in "owner/repo" format.

    Returns:
        Tuple of (always-empty suggestions list, discovery attempt record).
    """
    start = time.monotonic()

    if not repo:
        duration_ms = int((time.monotonic() - start) * 1000)
        return [], DiscoveryAttempt(
            method="browser-apply",
            outcome=DiscoveryOutcome.ERROR,
            duration_ms=duration_ms,
            error_message="Repository name could not be determined",
        )

    try:
        from agentic_devtools.cli.github.browser_apply_autofix import (
            BrowserAutofixUnavailable,
            BrowserCredentialError,
            count_browser_autofix_candidates,
        )
    except ImportError as exc:
        duration_ms = int((time.monotonic() - start) * 1000)
        return [], DiscoveryAttempt(
            method="browser-apply",
            outcome=DiscoveryOutcome.ERROR,
            duration_ms=duration_ms,
            error_message=f"Import error: {exc}",
        )

    try:
        candidate_count = count_browser_autofix_candidates(repo, pr_number)
    except BrowserAutofixUnavailable as exc:
        duration_ms = int((time.monotonic() - start) * 1000)
        logger.info("[BROWSER-APPLY] optional browser dependencies unavailable: %s", exc)
        return [], DiscoveryAttempt(
            method="browser-apply",
            outcome=DiscoveryOutcome.EMPTY,
            duration_ms=duration_ms,
            details={"reason": "browser dependencies not installed"},
        )
    except BrowserCredentialError as exc:
        duration_ms = int((time.monotonic() - start) * 1000)
        logger.info("[BROWSER-APPLY] browser credentials not configured: %s", exc)
        return [], DiscoveryAttempt(
            method="browser-apply",
            outcome=DiscoveryOutcome.EMPTY,
            duration_ms=duration_ms,
            details={"reason": "browser credentials not configured"},
        )
    except Exception as exc:
        duration_ms = int((time.monotonic() - start) * 1000)
        logger.warning("[BROWSER-APPLY] discovery exception: %s", exc)
        return [], DiscoveryAttempt(
            method="browser-apply",
            outcome=DiscoveryOutcome.ERROR,
            duration_ms=duration_ms,
            error_message=str(exc),
        )

    duration_ms = int((time.monotonic() - start) * 1000)
    if candidate_count > 0:
        return [], DiscoveryAttempt(
            method="browser-apply",
            outcome=DiscoveryOutcome.SUCCESS,
            suggestion_count=candidate_count,
            duration_ms=duration_ms,
        )
    return [], DiscoveryAttempt(
        method="browser-apply",
        outcome=DiscoveryOutcome.EMPTY,
        duration_ms=duration_ms,
    )
