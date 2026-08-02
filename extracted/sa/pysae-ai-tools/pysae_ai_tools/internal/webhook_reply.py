"""Post Claude response as a GitLab issue comment (3-phase flow).

Phase 1 (relay): posts placeholder ":hourglass: Demande en cours de traitement…"
Phase 2 (CI start): updates with job link — ``pysae-ai-tools internal webhook-reply start``
Phase 3 (CI end): updates with final result — ``pysae-ai-tools internal webhook-reply finish``

Required env vars:
    AI_TOOLS_WEBHOOK_PROJECT_ID      — numeric GitLab project ID
    AI_TOOLS_WEBHOOK_ISSUE_IID       — issue IID
    AI_TOOLS_WEBHOOK_REPLY_NOTE_ID   — note ID of the placeholder comment (from relay)
    CI_JOB_URL                       — link to the CI job (set by GitLab CI)

For ``finish`` only:
    CLAUDE_STATS_FILE                — path to Claude stats JSON (default: <tmpdir>/claude-stats.json)

Optional env vars:
    GLAB_TOKEN / GITLAB_TOKEN        — GitLab API token (falls back to glab CLI config)
"""

import json
import os
import sys

import typer

from ..common.glab.notes import GitLabNotesClient
from ..common.glab.runner import gitlab_token
from .parse_stream.parser import STATS_FILE_DEFAULT

app = typer.Typer(no_args_is_help=True, help="Update GitLab issue placeholder comment during webhook CI pipeline.")


def _get_token() -> str:
    """Resolve GitLab token from env or the glab CLI config."""
    return gitlab_token()


def _update_note(project_id: str, issue_iid: str, note_id: str, body: str, token: str) -> bool:
    """Update an existing GitLab issue note. Returns True on success."""
    ok = GitLabNotesClient(project_id, issue_iid, token).update_note(note_id, body)
    if ok:
        print(f"Note {note_id} updated", file=sys.stderr)
    else:
        print(f"Failed to update note {note_id}", file=sys.stderr)
    return ok


@app.command()
def start() -> None:
    """Phase 2: update the placeholder comment with the CI job link."""
    project_id = os.environ.get("AI_TOOLS_WEBHOOK_PROJECT_ID", "")
    issue_iid = os.environ.get("AI_TOOLS_WEBHOOK_ISSUE_IID", "")
    note_id = os.environ.get("AI_TOOLS_WEBHOOK_REPLY_NOTE_ID", "")
    job_url = os.environ.get("CI_JOB_URL", "")

    if not project_id or not issue_iid or not note_id:
        print("Missing project/issue/note ID, skipping.", file=sys.stderr)
        return

    token = _get_token()
    if not token:
        print("No GitLab token found, skipping.", file=sys.stderr)
        return

    if job_url:
        body = f":hourglass_flowing_sand: [Demande en cours de traitement…]({job_url})"
    else:
        body = ":hourglass_flowing_sand: Demande en cours de traitement…"

    _update_note(project_id, issue_iid, note_id, body, token)


@app.command()
def finish() -> None:
    """Phase 3: update the placeholder comment with the final status.

    When turns are posted in real-time via parse_stream, this just updates
    the placeholder with a completion status. Falls back to posting the
    full response if no turns were posted (CLAUDE_TURNS_DIR empty or unset).
    """
    project_id = os.environ.get("AI_TOOLS_WEBHOOK_PROJECT_ID", "")
    issue_iid = os.environ.get("AI_TOOLS_WEBHOOK_ISSUE_IID", "")
    note_id = os.environ.get("AI_TOOLS_WEBHOOK_REPLY_NOTE_ID", "")
    job_url = os.environ.get("CI_JOB_URL", "")
    stats_file = os.environ.get("CLAUDE_STATS_FILE", STATS_FILE_DEFAULT)

    if not project_id or not issue_iid or not note_id:
        print("Missing project/issue/note ID, skipping.", file=sys.stderr)
        return

    token = _get_token()
    if not token:
        print("No GitLab token found, skipping.", file=sys.stderr)
        return

    # Read stats for error status
    if os.path.isfile(stats_file):
        try:
            with open(stats_file) as f:
                stats = json.load(f)
            is_error = stats.get("is_error", False)
        except (json.JSONDecodeError, OSError):
            is_error = False
    else:
        # No stats file — check CI_JOB_STATUS (set by GitLab in after_script)
        # to detect job failures that occurred before Claude could run
        ci_status = os.environ.get("CI_JOB_STATUS", "")
        is_error = ci_status in ("failed", "canceled")

    # Build status message
    if is_error:
        status = "Session terminée avec erreur"
        icon = ":x:"
    else:
        status = "Session terminée"
        icon = ":white_check_mark:"

    if job_url:
        body = f"{icon} [{status}]({job_url})"
    else:
        body = f"{icon} {status}"

    _update_note(project_id, issue_iid, note_id, body, token)


if __name__ == "__main__":
    app()
