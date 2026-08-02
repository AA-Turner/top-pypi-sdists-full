"""Atomic label transitions on GitLab issues with retry on race."""

import logging
import os
import tempfile
import time
from datetime import datetime, timezone

from ..common.glab.runner import run_glab
from .models import Ticket

logger = logging.getLogger(__name__)

_RETRIES = 3
_BACKOFF_SECONDS = 1.0
PICKUP_MARKER = "[autopilot] pickup"


class LabelTransitionError(RuntimeError):
    """Raised when a label transition exhausts retries."""


class CommentPostError(RuntimeError):
    """Raised when posting a GitLab comment fails after retries."""


def _update_labels(project_path: str, iid: int, add: list[str], remove: list[str]) -> None:
    encoded = project_path.replace("/", "%2F")
    args = ["api", "-X", "PUT", f"projects/{encoded}/issues/{iid}"]
    if add:
        args += ["-f", f"add_labels={','.join(add)}"]
    if remove:
        args += ["-f", f"remove_labels={','.join(remove)}"]
    for attempt in range(_RETRIES):
        res = run_glab(*args, timeout=30)
        if res.ok:
            return
        logger.warning("label transition failed (attempt %s): %s", attempt + 1, res.stderr)
        time.sleep(_BACKOFF_SECONDS * (2**attempt))
    raise LabelTransitionError(f"label transition exhausted retries on {project_path}#{iid}")


def _post_comment(project_path: str, iid: int, body: str) -> None:
    """Post an issue comment. Body is written to a tmp file so newlines,
    `=`, and non-printable characters survive `glab api -F body=@<file>`
    (the `-f key=value` form chokes on multiline values)."""
    encoded = project_path.replace("/", "%2F")
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as fh:
        fh.write(body)
        body_path = fh.name
    try:
        args = ["api", f"projects/{encoded}/issues/{iid}/notes", "-F", f"body=@{body_path}"]
        for attempt in range(_RETRIES):
            res = run_glab(*args, timeout=30)
            if res.ok:
                return
            logger.warning("comment post failed (attempt %s): %s", attempt + 1, res.stderr)
            time.sleep(_BACKOFF_SECONDS * (2**attempt))
    finally:
        try:
            os.unlink(body_path)
        except OSError:
            pass
    raise CommentPostError(f"comment post exhausted retries on {project_path}#{iid}")


def mark_wip(ticket: Ticket) -> None:
    _update_labels(ticket.project_path, ticket.iid, add=["agent::wip"], remove=["agent::ready"])
    now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
    # Visible line renders with emoji + bold; hidden HTML comment keeps the
    # machine-readable marker that orphan reclaim (orphan.py:_PICKUP_RE) parses.
    body = f":robot_face: **Autopilot started** · `{now_iso}`\n" f"<!-- {PICKUP_MARKER} at={now_iso} -->"
    _post_comment(ticket.project_path, ticket.iid, body)


def mark_blocked(ticket: Ticket, reason: str, run_id: str) -> None:
    _update_labels(
        ticket.project_path,
        ticket.iid,
        add=["agent::blocked"],
        remove=["agent::wip", "agent::ready"],
    )
    # Mention the ticket author so GitLab sends them a notification.
    # Falls back to no mention if author wasn't captured (e.g. legacy
    # tickets pulled before the field existed).
    mention = f"@{ticket.author_username} — " if ticket.author_username else ""
    body = f"{mention}**Agent autopilot batch — escalade**\n\nRaison : {reason}\nRun ID : {run_id}\n"
    _post_comment(ticket.project_path, ticket.iid, body)


def post_advisory_note(ticket: Ticket, kind: str, body: str, run_id: str) -> None:
    """Post a non-blocking advisory comment on a GitLab issue.

    Unlike `mark_blocked`, leaves labels untouched: the ticket stays
    `agent::ready` and continues through the pipeline. Used to surface
    structural gaps (missing template sections) or spec gaps (missing edge
    cases from the Sonnet completeness audit) as soft warnings — the
    autopilot trusts the LLM to fill formal gaps and produce a useful MR
    most of the time, and a comment is cheaper to ignore than a hard block.
    """
    mention = f"@{ticket.author_username} — " if ticket.author_username else ""
    full_body = f"{mention}**Agent autopilot batch — note ({kind})**\n\n" f"{body}\n\n" f"Run ID : {run_id}\n"
    _post_comment(ticket.project_path, ticket.iid, full_body)


def clear_wip(ticket: Ticket) -> None:
    _update_labels(ticket.project_path, ticket.iid, add=[], remove=["agent::wip"])


def reopen_issue(project_path: str, iid: int) -> None:
    """Reopen a closed GitLab issue (used when post-merge deploy fails).

    On a project that closes the ticket at merge (``board.to_deploy=false``, or GitLab
    autoclose where enabled), a post-merge deploy failure makes the "merged = done" state
    wrong: the user cannot use the feature yet. Reopening makes the broken state visible on
    the board. A no-op when the ticket is already open (e.g. parked in ``To deploy``).

    Takes primitive args (not a Ticket) because callers at the post-merge
    stage only have the Outcome at hand.
    """
    encoded = project_path.replace("/", "%2F")
    args = ["api", "-X", "PUT", f"projects/{encoded}/issues/{iid}", "-f", "state_event=reopen"]
    for attempt in range(_RETRIES):
        res = run_glab(*args, timeout=30)
        if res.ok:
            return
        logger.warning("issue reopen failed (attempt %s): %s", attempt + 1, res.stderr)
        time.sleep(_BACKOFF_SECONDS * (2**attempt))
    raise LabelTransitionError(f"reopen exhausted retries on {project_path}#{iid}")
