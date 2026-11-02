"""GraphQL discovery strategy — wraps existing fetch_applicable_suggestions.

Thin adapter that calls the existing GraphQL-based suggestion discovery
and translates the result into the unified (list[SuggestedChange], DiscoveryAttempt)
interface expected by the orchestrator.
"""

from __future__ import annotations

import logging
import time

from agentic_devtools.cli.ci.pipeline.discovery.models import (
    DiscoveryAttempt,
    DiscoveryOutcome,
)
from agentic_devtools.cli.ci.pipeline.suggestions import (
    SuggestedChange,
    fetch_applicable_suggestions,
)
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

logger = logging.getLogger(__name__)


def graphql_discover(
    provider: CIPlatformProvider,
    pr_number: int,
) -> tuple[list[SuggestedChange], DiscoveryAttempt, str]:
    """Discover suggestions via GraphQL reviewThreads query.

    Wraps the existing ``fetch_applicable_suggestions`` function and captures
    timing and outcome diagnostics.

    Args:
        provider: CI platform provider for API interactions.
        pr_number: Pull request number.

    Returns:
        Tuple of (suggestions, discovery attempt record, PR node ID).
    """
    start = time.monotonic()
    try:
        suggestions, pr_node_id = fetch_applicable_suggestions(provider, pr_number)
    except ProviderRateLimitError:
        raise
    except Exception as exc:
        duration_ms = int((time.monotonic() - start) * 1000)
        logger.warning("GraphQL discovery failed: %s", exc)
        attempt = DiscoveryAttempt(
            method="graphql",
            outcome=DiscoveryOutcome.ERROR,
            duration_ms=duration_ms,
            error_message=str(exc),
        )
        return [], attempt, ""

    duration_ms = int((time.monotonic() - start) * 1000)

    if suggestions:
        # Tag discovery source on each suggestion
        for s in suggestions:
            s.discovery_source = "graphql"
        attempt = DiscoveryAttempt(
            method="graphql",
            outcome=DiscoveryOutcome.SUCCESS,
            suggestion_count=len(suggestions),
            duration_ms=duration_ms,
        )
    else:
        attempt = DiscoveryAttempt(
            method="graphql",
            outcome=DiscoveryOutcome.EMPTY,
            duration_ms=duration_ms,
        )

    return suggestions, attempt, pr_node_id
