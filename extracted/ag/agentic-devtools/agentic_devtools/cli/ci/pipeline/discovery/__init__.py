"""Discovery package — priority-ordered suggestion discovery strategies.

Provides the orchestrator and strategy implementations for discovering
Copilot autofix suggestions through multiple API surfaces (GraphQL, REST,
HTML scrape) with diagnostic reporting.
"""

from __future__ import annotations

from agentic_devtools.cli.ci.pipeline.discovery.browser_strategy import browser_discover
from agentic_devtools.cli.ci.pipeline.discovery.models import (
    DiscoveryAttempt,
    DiscoveryOutcome,
)
from agentic_devtools.cli.ci.pipeline.discovery.orchestrator import (
    has_inline_evidence,
    run_discovery,
)

__all__ = [
    "DiscoveryAttempt",
    "DiscoveryOutcome",
    "browser_discover",
    "has_inline_evidence",
    "run_discovery",
]
