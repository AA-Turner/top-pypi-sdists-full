from __future__ import annotations

from datetime import datetime
from typing import Any

from spec_kitty_tracker.models import CanonicalStatus


def parse_datetime(value: Any) -> datetime | None:
    """Parse an ISO 8601 datetime string, handling the 'Z' suffix.

    Shared utility used by all connectors to avoid duplicating
    the same parsing logic across every connector module.
    """
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def github_state_to_status(state: str) -> CanonicalStatus:
    return CanonicalStatus.DONE if state == "closed" else CanonicalStatus.TODO


def status_to_github_state(status: CanonicalStatus) -> str:
    if status in (CanonicalStatus.DONE, CanonicalStatus.CANCELED):
        return "closed"
    return "open"


def linear_priority_to_canonical(priority: int | None) -> int | None:
    if priority is None:
        return None
    mapping = {0: 4, 1: 0, 2: 1, 3: 2, 4: 3}
    return mapping.get(priority, 4)


def canonical_to_linear_priority(priority: int | None) -> int:
    if priority is None:
        return 0
    mapping = {4: 0, 0: 1, 1: 2, 2: 3, 3: 4}
    return mapping.get(priority, 0)
