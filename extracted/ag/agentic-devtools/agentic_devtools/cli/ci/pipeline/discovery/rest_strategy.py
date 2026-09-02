"""REST re-derivation discovery strategy.

Fetches review comments via the REST API
(GET /repos/{owner}/{repo}/pulls/{pr}/reviews/{review_id}/comments)
and parses markdown suggestion blocks from comment bodies. This serves
as a fallback when the GraphQL strategy returns empty — particularly
important for Copilot autofix suggestions in private EMU repos where
the GraphQL ``reviewThreads`` query may not surface suggestion data.

The strategy also detects "anchored but no replacement" cases — where
a review comment is positioned on a file/line but contains no markdown
suggestion block. These cases are recorded in diagnostics for visibility.
"""

from __future__ import annotations

import logging
import re
import time

from agentic_devtools.cli.ci.pipeline.discovery.models import (
    DiscoveryAttempt,
    DiscoveryOutcome,
)
from agentic_devtools.cli.ci.pipeline.suggestions import SuggestedChange
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

logger = logging.getLogger(__name__)

# Match markdown suggestion fences, including indented closing fences.
_SUGGESTION_BLOCK_PATTERN = re.compile(r"(?m)^[ \t]*```suggestion(?::-?\d+(?:\+\d+)?)?(?:[ \t].*)?\r?$")
_SUGGESTION_CONTENT_PATTERN = re.compile(
    r"[ \t]*```suggestion(?::-?\d+(?:\+\d+)?)?(?:[ \t].*)?(?:\r?\n)(.*?)[ \t]*```",
    re.DOTALL,
)


def parse_suggestion_blocks(body: str) -> str | None:
    """Extract replacement content from a markdown suggestion block.

    Public helper that extracts the first ```suggestion ... ``` block
    from a comment body.

    Args:
        body: Full comment body text.

    Returns:
        The suggestion replacement text, empty string for a valid delete
        suggestion, or None if no complete block is found.
    """
    match = _SUGGESTION_CONTENT_PATTERN.search(body)
    if not match:
        return None
    return match.group(1)


def rest_discover(
    provider: CIPlatformProvider,
    pr_number: int,
    review_id: int,
) -> tuple[list[SuggestedChange], DiscoveryAttempt]:
    """Discover suggestions via REST review comments endpoint.

    Calls ``provider.list_review_comments(pr_number, review_id)`` to fetch
    inline comments from the specified Copilot review, then parses each
    comment body for markdown suggestion blocks.

    Args:
        provider: CI platform provider for API interactions.
        pr_number: Pull request number.
        review_id: ID of the Copilot review to fetch comments for.

    Returns:
        Tuple of (suggestions found, discovery attempt record).
    """
    start = time.monotonic()

    if not review_id:
        duration_ms = int((time.monotonic() - start) * 1000)
        return [], DiscoveryAttempt(
            method="rest-rederivation",
            outcome=DiscoveryOutcome.EMPTY,
            duration_ms=duration_ms,
            details={"reason": "No review_id provided"},
        )

    try:
        comments = provider.list_review_comments(pr_number, review_id)
    except ProviderRateLimitError:
        raise
    except Exception as exc:
        duration_ms = int((time.monotonic() - start) * 1000)
        logger.warning("REST discovery failed for review %d: %s", review_id, exc)
        return [], DiscoveryAttempt(
            method="rest-rederivation",
            outcome=DiscoveryOutcome.ERROR,
            duration_ms=duration_ms,
            error_message=str(exc),
        )

    suggestions: list[SuggestedChange] = []
    anchored_no_replacement = 0

    for comment in comments:
        body = getattr(comment, "body", "") or ""
        path = getattr(comment, "path", "") or ""
        comment_id = getattr(comment, "id", 0)
        line = getattr(comment, "line", None) or getattr(comment, "end_line", None) or 0
        start_line = getattr(comment, "start_line", None) or line

        if not path or not line:
            continue

        if _SUGGESTION_BLOCK_PATTERN.search(body):
            replacement = parse_suggestion_blocks(body)
            if replacement is None:
                logger.debug(
                    "REST: comment %d skipped (suggestion block without closing fence)",
                    comment_id,
                )
                continue

            suggestions.append(
                SuggestedChange(
                    suggestion_id=f"REST_{comment_id}",
                    outdated=False,
                    comment_database_id=comment_id,
                    thread_id="",
                    path=path,
                    start_line=start_line,
                    end_line=line,
                    replacement=replacement,
                    discovery_source="rest-rederivation",
                )
            )
        else:
            # Comment is anchored to a file/line but has no suggestion block
            anchored_no_replacement += 1

    duration_ms = int((time.monotonic() - start) * 1000)

    if suggestions:
        attempt = DiscoveryAttempt(
            method="rest-rederivation",
            outcome=DiscoveryOutcome.SUCCESS,
            suggestion_count=len(suggestions),
            duration_ms=duration_ms,
            details={"anchored_no_replacement": anchored_no_replacement},
        )
    elif anchored_no_replacement > 0:
        attempt = DiscoveryAttempt(
            method="rest-rederivation",
            outcome=DiscoveryOutcome.ANCHORED_NO_REPLACEMENT,
            duration_ms=duration_ms,
            details={"anchored_no_replacement": anchored_no_replacement},
        )
    else:
        attempt = DiscoveryAttempt(
            method="rest-rederivation",
            outcome=DiscoveryOutcome.EMPTY,
            duration_ms=duration_ms,
        )

    return suggestions, attempt
