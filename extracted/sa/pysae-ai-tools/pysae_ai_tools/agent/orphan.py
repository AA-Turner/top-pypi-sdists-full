"""Detect WIP tickets orphaned by a crashed run."""

import logging
import re
from datetime import datetime, timezone

from ..common.glab.runner import glab_api
from .labels import PICKUP_MARKER
from .models import Ticket

logger = logging.getLogger(__name__)

_PICKUP_RE = re.compile(rf"{re.escape(PICKUP_MARKER)} at=([0-9T:+\-Z.]+)")


def _fetch_last_pickup_at(project_path: str, iid: int) -> datetime | None:
    """Return the most recent `[autopilot] pickup at=<iso>` marker, or None.

    Reading the marker from a comment is reliable because comments are
    immutable from the issue's perspective: a label change or a human note
    does not rewrite the marker, unlike `issue.updated_at` which moves on
    every mutation.
    """
    encoded = project_path.replace("/", "%2F")
    notes = glab_api(f"projects/{encoded}/issues/{iid}/notes?sort=desc&per_page=20")
    # glab_api returns None on a failed call, empty body, or invalid JSON (HTML
    # from a 502, corrupted Windows-locale bytes). Any of these degrades orphan
    # reclaim to the updated_at fallback rather than raising for the whole batch.
    if not isinstance(notes, list):
        logger.warning("fetch notes failed for %s#%s", project_path, iid)
        return None
    for note in notes:
        match = _PICKUP_RE.search(note.get("body", ""))
        if match:
            try:
                return datetime.fromisoformat(match.group(1).replace("Z", "+00:00"))
            except ValueError:
                continue
    return None


def find_orphans(wip_tickets: list[Ticket], timeout_seconds: int) -> list[Ticket]:
    """Return WIP tickets whose last autopilot pickup is older than timeout_seconds."""
    now = datetime.now(timezone.utc)
    orphans: list[Ticket] = []
    for t in wip_tickets:
        pickup = _fetch_last_pickup_at(t.project_path, t.iid) or t.updated_at
        if (now - pickup).total_seconds() >= timeout_seconds:
            orphans.append(t)
    return orphans
