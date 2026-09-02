"""Discovery orchestrator — priority-ordered strategy runner with retry logic.

Executes discovery strategies in strict priority order:
1. GraphQL (pullRequest.reviewThreads)
2. REST re-derivation (list_review_comments)
3. HTML scrape (react-partial.embeddedData)
4. Browser apply (opt-in, EMU/SSO) — Playwright-driven UI tier, gated by the
   ENABLE_BROWSER_APPLY_SUGGESTIONS flag and only attempted when the three
   tiers above return empty. When the flag is off it is skipped entirely.

Includes retry logic when all strategies return empty but evidence
suggests suggestions should exist (recent Copilot review with inline comments).
"""

from __future__ import annotations

import logging
import os
import time
from datetime import datetime, timezone

from agentic_devtools.cli.ci.pipeline.discovery.browser_strategy import browser_discover
from agentic_devtools.cli.ci.pipeline.discovery.graphql_strategy import graphql_discover
from agentic_devtools.cli.ci.pipeline.discovery.html_strategy import html_discover
from agentic_devtools.cli.ci.pipeline.discovery.models import (
    DiscoveryAttempt,
    DiscoveryOutcome,
)
from agentic_devtools.cli.ci.pipeline.discovery.rest_strategy import rest_discover
from agentic_devtools.cli.ci.pipeline.snapshot import PRStateSnapshot
from agentic_devtools.cli.ci.pipeline.suggestions import SuggestedChange
from agentic_devtools.cli.ci.provider import CIPlatformProvider

logger = logging.getLogger(__name__)

# Maximum total discovery time (NFR-001)
_TOTAL_TIMEOUT_SECONDS = 120

# Default retry delay when all strategies return empty but review evidence exists
_DEFAULT_RETRY_DELAY_SECONDS = 10

# Recency window: only retry if Copilot review submitted within this many seconds
_RECENCY_WINDOW_SECONDS = 300  # 5 minutes


def run_discovery(
    provider: CIPlatformProvider,
    snapshot: PRStateSnapshot,
    *,
    repo: str = "",
) -> tuple[list[SuggestedChange], list[DiscoveryAttempt], str]:
    """Execute all discovery strategies in priority order.

    Strategies are tried in order: GraphQL → REST → HTML → (opt-in) Browser.
    If a strategy returns suggestions, subsequent strategies are skipped.
    The opt-in browser tier fires only when ENABLE_BROWSER_APPLY_SUGGESTIONS is
    set, a repo is known, and all three preceding tiers returned empty.
    If all strategies return empty and a recent Copilot review with inline
    comments exists, retries once after a configurable delay.

    Args:
        provider: CI platform provider.
        snapshot: Current PR state snapshot.
        repo: Repository in "owner/repo" format (for HTML strategy).

    Returns:
        Tuple of (discovered suggestions, list of all attempt records, PR node ID).
    """
    attempts: list[DiscoveryAttempt] = []
    pr_node_id = ""
    start_time = time.monotonic()

    retry_delay = _get_retry_delay()
    max_retries = 1

    for attempt_num in range(max_retries + 1):  # pragma: no branch
        round_attempts: list[DiscoveryAttempt] = []
        if attempt_num > 0:
            # Check timeout before retry
            elapsed = time.monotonic() - start_time
            if elapsed + retry_delay > _TOTAL_TIMEOUT_SECONDS:
                logger.info(
                    "Discovery timeout cap reached (elapsed=%.1fs, retry_delay=%ds, cap=%ds)",
                    elapsed,
                    retry_delay,
                    _TOTAL_TIMEOUT_SECONDS,
                )
                break

            logger.info(
                "Discovery retry #%d: waiting %ds before re-attempting",
                attempt_num,
                retry_delay,
            )
            time.sleep(retry_delay)

        # Strategy 1: GraphQL
        suggestions, graphql_attempt, node_id = graphql_discover(provider, snapshot.pr_number)
        attempts.append(graphql_attempt)
        round_attempts.append(graphql_attempt)
        if node_id:
            pr_node_id = node_id

        if suggestions:
            return suggestions, attempts, pr_node_id

        # Strategy 2: REST re-derivation
        review_id = snapshot.copilot_review_id
        if review_id:
            rest_suggestions, rest_attempt = rest_discover(provider, snapshot.pr_number, review_id)
            attempts.append(rest_attempt)
            round_attempts.append(rest_attempt)
            if rest_suggestions:
                return rest_suggestions, attempts, pr_node_id

        # Strategy 3: HTML scrape
        if repo:
            html_suggestions, html_attempt = html_discover(provider, snapshot.pr_number, repo)
        else:
            html_suggestions = []
            html_attempt = DiscoveryAttempt(
                method="html-scrape",
                outcome=DiscoveryOutcome.EMPTY,
                details={"skipped": True, "reason": "repo missing"},
            )

        attempts.append(html_attempt)
        round_attempts.append(html_attempt)
        if html_suggestions:
            return html_suggestions, attempts, pr_node_id

        primary_tiers_empty = _all_attempts_empty(round_attempts)

        # Strategy 4: Browser apply (opt-in, EMU/SSO). Fires only when the
        # ENABLE_BROWSER_APPLY_SUGGESTIONS flag is on, a repo is known, and all
        # three existing tiers returned empty for this round. When the flag is
        # off this block is skipped entirely, leaving behavior unchanged.
        if _browser_tier_enabled() and repo and primary_tiers_empty:
            _, browser_attempt = browser_discover(provider, snapshot.pr_number, repo)
            attempts.append(browser_attempt)
            round_attempts.append(browser_attempt)

        # All primary strategies empty — check if retry is warranted
        if attempt_num < max_retries and primary_tiers_empty and _should_retry(snapshot):
            continue
        break

    # Emit diagnostic discrepancy if evidence suggests suggestions should exist
    if has_inline_evidence(snapshot):
        method_outcomes = [
            f"{a.method}={a.outcome.value}" + (f"({a.error_message})" if a.error_message else "") for a in attempts
        ]
        logger.warning(
            "[DISCOVERY-DISCREPANCY] review_state=%s, inline_comments=%d, discovered_suggestions=0, "
            "discovery_sources_attempted=[%s]",
            snapshot.review_state,
            snapshot.copilot_review_inline_count,
            ", ".join(method_outcomes),
        )

    return [], attempts, pr_node_id


def has_inline_evidence(snapshot: PRStateSnapshot) -> bool:
    """Return True when evidence suggests inline suggestions should exist.

    CHANGES_REQUESTED reviews have copilot_review_inline_count=0 by default
    (inline comments are only counted for COMMENTED reviews in the snapshot
    builder), so any CHANGES_REQUESTED Copilot review is treated as potential
    evidence.  For COMMENTED reviews, -1 (unknown, e.g. failed fetch) is
    treated as potential evidence to fail closed.  Only an explicit count of 0
    on a non-CHANGES_REQUESTED review confirms no inline suggestions.
    """
    if not snapshot.copilot_review_id:
        return False
    # CHANGES_REQUESTED: inline count is not tracked in the snapshot builder
    if snapshot.review_state == "CHANGES_REQUESTED":
        return True
    # -1 = unknown (fetch failed); fail closed → treat as potential evidence
    return snapshot.copilot_review_inline_count != 0


def _should_retry(snapshot: PRStateSnapshot) -> bool:
    """Determine if a discovery retry is warranted.

    Retry triggers when:
    - A Copilot review with inline evidence exists (CHANGES_REQUESTED reviews
      always qualify; COMMENTED reviews qualify when count > 0 or unknown)
    - The review was submitted recently (within recency window)
    """
    if not has_inline_evidence(snapshot):
        return False

    if not snapshot.reviews:
        return False

    # Find the Copilot or trusted synthetic review by ID and check recency
    from agentic_devtools.cli.ci.pipeline.gate_verdict import is_copilot_or_synthetic_review

    for review in snapshot.reviews:
        if review.id == snapshot.copilot_review_id and is_copilot_or_synthetic_review(review):
            if not review.submitted_at:
                logger.warning(
                    "Discovery retry: review %d has no submitted_at timestamp — skipping recency check",
                    review.id,
                )
                # Without timestamp, still retry when inline evidence exists
                return True
            try:
                submitted = datetime.fromisoformat(review.submitted_at.replace("Z", "+00:00"))
                age_seconds = (datetime.now(timezone.utc) - submitted).total_seconds()
                if age_seconds <= _RECENCY_WINDOW_SECONDS:
                    return True
                else:
                    logger.info(
                        "Discovery retry: review %d is %.0fs old (exceeds %ds window)",
                        review.id,
                        age_seconds,
                        _RECENCY_WINDOW_SECONDS,
                    )
                    return False
            except (ValueError, TypeError) as exc:
                logger.warning(
                    "Discovery retry: unable to parse submitted_at '%s': %s",
                    review.submitted_at,
                    exc,
                )
                return True

    return False


def _get_retry_delay() -> int:
    """Get retry delay from environment or use default."""
    env_val = os.environ.get("APPLY_SUGGESTIONS_RETRY_DELAY_SECONDS", "")
    if env_val:
        try:
            return max(1, int(env_val))
        except ValueError:
            pass
    return _DEFAULT_RETRY_DELAY_SECONDS


def _all_attempts_empty(attempts: list[DiscoveryAttempt]) -> bool:
    """Return True when every attempt outcome is empty."""
    return bool(attempts) and all(a.outcome is DiscoveryOutcome.EMPTY for a in attempts)


def _browser_tier_enabled() -> bool:
    """Return True when the opt-in browser apply tier is enabled via env flag.

    Distinct from ``ENABLE_AUTO_APPLY_SUGGESTIONS``; defaults to off so the
    pipeline is byte-for-byte unchanged unless explicitly enabled.
    """
    return os.environ.get("ENABLE_BROWSER_APPLY_SUGGESTIONS", "").strip().lower() in (
        "1",
        "true",
        "yes",
    )
