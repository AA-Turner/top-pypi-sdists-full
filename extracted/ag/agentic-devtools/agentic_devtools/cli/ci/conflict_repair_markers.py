"""Conflict-repair marker formats and builders."""

from __future__ import annotations

import re
from datetime import UTC, datetime

# Marker format: <!-- agdt:conflict-repair:{base_sha}:{head_sha}:{iso8601_utc} -->
CONFLICT_REPAIR_MARKER_PREFIX = "<!-- agdt:conflict-repair:"
_CONFLICT_REPAIR_MARKER_RE = re.compile(r"<!-- agdt:conflict-repair:([0-9a-f]+):([0-9a-f]+):([^>]+) -->")

# Deliberately distinct from CONFLICT_REPAIR_MARKER_PREFIX: escalation comments
# are never mistaken for dispatch markers or counted as attempts.
CONFLICT_REPAIR_ESCALATION_MARKER_PREFIX = "<!-- agdt:conflict-repair-escalation:"


def build_conflict_repair_marker(*, base_sha: str, head_sha: str) -> str:
    """Return a new conflict-repair idempotency marker with the current UTC time.

    Args:
        base_sha: Full SHA of the base-branch tip at dispatch time.
        head_sha: Full HEAD SHA of the PR branch at dispatch time.

    Returns:
        HTML comment string suitable for embedding in a PR comment body.
    """
    now = datetime.now(UTC).isoformat()
    return f"<!-- agdt:conflict-repair:{base_sha}:{head_sha}:{now} -->"


def build_conflict_repair_escalation_marker(*, head_sha: str) -> str:
    """Return the idempotency marker for a conflict-repair escalation notice.

    Args:
        head_sha: Full HEAD SHA of the PR branch the escalation applies to.

    Returns:
        HTML comment string suitable for embedding in a PR comment body.
    """
    return f"{CONFLICT_REPAIR_ESCALATION_MARKER_PREFIX}{head_sha} -->"
