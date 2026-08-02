"""Design-lane label transitions, reusing the low-level helpers from ``agent.labels``.

The design lane has no MR/merge. Idempotence + "already processed" is carried by
these labels (the candidate pull excludes tickets that already have one):
- ``design::wip``     — picked up, generation in flight (with a pickup marker for orphan reclaim)
- ``design::review``  — proto rendered, PM gate pending (terminal-success)
- ``design::blocked`` — escalated / failed
"""

from datetime import datetime, timezone

from ..labels import PICKUP_MARKER, _post_comment, _update_labels
from ..models import Ticket

DESIGN_WIP = "design::wip"
DESIGN_REVIEW = "design::review"
DESIGN_BLOCKED = "design::blocked"


def mark_design_wip(ticket: Ticket) -> None:
    """Add design::wip and post a pickup marker (reused by ``orphan.find_orphans``)."""
    _update_labels(ticket.project_path, ticket.iid, add=[DESIGN_WIP], remove=[])
    now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
    body = f":art: **Design autopilot démarré** · `{now_iso}`\n<!-- {PICKUP_MARKER} at={now_iso} -->"
    _post_comment(ticket.project_path, ticket.iid, body)


def mark_design_review(ticket: Ticket, preview_url: str, run_id: str) -> None:
    """Proto ready: swap design::wip → design::review and post the preview URL."""
    _update_labels(ticket.project_path, ticket.iid, add=[DESIGN_REVIEW], remove=[DESIGN_WIP])
    link = preview_url or "(URL Pages indisponible, voir la branche design/<iid>)"
    body = f":art: **Proto prêt pour revue PM** (run `{run_id}`)\nRendu : {link}\nMême lien pour le user-test."
    _post_comment(ticket.project_path, ticket.iid, body)


def mark_design_blocked(ticket: Ticket, reason: str, run_id: str) -> None:
    """Escalation: swap design::wip → design::blocked and post the reason."""
    _update_labels(ticket.project_path, ticket.iid, add=[DESIGN_BLOCKED], remove=[DESIGN_WIP])
    body = f":warning: **Design autopilot bloqué** (run `{run_id}`)\n{reason}"
    _post_comment(ticket.project_path, ticket.iid, body)
