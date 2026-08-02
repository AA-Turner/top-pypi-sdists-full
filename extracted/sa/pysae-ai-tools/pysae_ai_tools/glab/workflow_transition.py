"""Transition a GitLab issue's board column label.

Usage:
    pysae-ai-tools workflow_transition <ISSUE_IID> <LABEL>

Examples:
    pysae-ai-tools workflow_transition 123 Refinement
    pysae-ai-tools workflow_transition 123 Ready
    pysae-ai-tools workflow_transition 123 "workflow::In progress"
    pysae-ai-tools workflow_transition 456 "workflow::Under review"
    pysae-ai-tools workflow_transition 789 "workflow::To deploy"

Valid labels (exact or alias):
    Refinement, Ready, workflow::To Do, workflow::In progress,
    workflow::Under review, workflow::To deploy
    Aliases: "in progress", "under review", "to do", "to deploy",
    "review", "todo", "in_progress", etc.

The script:
1. Resolves the project ID (from detect_context or glab repo view)
2. Fetches the issue's current labels and assignees
3. Removes all existing board column labels
4. Adds the new workflow label
5. Makes the current user the sole assignee (taking the ticket over from whoever it was
   assigned to), unless --no-assign is passed or running in CI
6. Prints the resulting action or "skipped" if nothing changed
"""

import json
import os
from pathlib import Path
from typing import Annotated
from urllib.parse import quote

import typer

from ..common.glab.fetch_issues import get_current_user_id
from ..common.glab.runner import resolve_current_project, run_glab
from ..common.project_config import flag_enabled
from ..common.references.gitlab_labels import BoardLabel
from ..internal.detect_context.detect import DetectArgs, detect
from .deploy_branches import has_deploy_step

BOARD_LABELS: set[str] = set(BoardLabel)

# Aliases: lowercase key -> exact BoardLabel value
LABEL_ALIASES: dict[str, str] = {
    "refinement": BoardLabel.REFINEMENT,
    "ready": BoardLabel.READY,
    "to do": BoardLabel.TO_DO,
    "todo": BoardLabel.TO_DO,
    "to_do": BoardLabel.TO_DO,
    "in progress": BoardLabel.IN_PROGRESS,
    "in_progress": BoardLabel.IN_PROGRESS,
    "under review": BoardLabel.UNDER_REVIEW,
    "under_review": BoardLabel.UNDER_REVIEW,
    "review": BoardLabel.UNDER_REVIEW,
    "to deploy": BoardLabel.TO_DEPLOY,
    "to_deploy": BoardLabel.TO_DEPLOY,
}


def _run_glab(*args: str, timeout: int = 15, stdin_data: str | None = None) -> str | None:
    """Run a glab command, return stdout or None on failure."""
    res = run_glab(*args, timeout=timeout, stdin_data=stdin_data)
    return res.stdout if res.ok else None


def _get_project_id() -> str:
    """Get project ID from detect_context or glab."""
    # Try detect_context
    try:
        args = DetectArgs()
        ctx = detect(args)
        if ctx.project_id:
            return ctx.project_id
    except Exception:
        pass

    # Fallback to glab
    return resolve_current_project()[0]


def _resolve_label(label_input: str) -> str:
    """Resolve a label input to the exact BoardLabel value.

    Accepts exact labels (e.g. "workflow::In progress") or aliases (e.g. "in progress", "review").
    Returns the resolved label or empty string if invalid.
    """
    stripped = label_input.strip()

    # Exact match first
    if stripped in BOARD_LABELS:
        return stripped

    # Alias lookup (case-insensitive)
    lower = stripped.lower()
    if lower in LABEL_ALIASES:
        return LABEL_ALIASES[lower]

    return ""


def transition(issue_iid: str, new_label: str, project_id: str = "", assign_to: int | None = None) -> str:
    """Transition an issue's board label, optionally claiming it. Returns the action taken.

    When ``assign_to`` (a GitLab user id) is given, that user *becomes the sole assignee* —
    whoever was assigned before (typically the PM who filed the ticket, who stays its author)
    is replaced, so "my issues" filters and the board owner both point at the person doing the
    work. This runs even when the label is already correct, so re-picking a ticket already in
    the right column still claims it. ``assign_to=None`` (the default) is a pure label move,
    leaving assignees untouched, which is what the batch/reconciliation and post-merge callers
    rely on.

    Returns:
        "set:<label>" (label moved), "assigned:<label>" (only the assignee changed),
        "set:<label>+assigned" (both), "skipped:already-set" (nothing to do),
        "error:<reason>" on failure.
    """
    if not project_id:
        project_id = _get_project_id()
    if not project_id:
        return "error:no-project-id"

    resolved = _resolve_label(new_label)
    if not resolved:
        valid = ", ".join(b.value for b in BoardLabel)
        return f"error:invalid-label:{new_label} (valid: {valid})"

    # Fetch current labels and assignees in one call
    raw = _run_glab("api", f"projects/{project_id}/issues/{issue_iid}")
    if not raw:
        return "error:cannot-fetch-issue"

    try:
        issue_data = json.loads(raw)
        current_labels: list[str] = issue_data.get("labels", [])
        current_assignee_ids: list[int] = [a["id"] for a in issue_data.get("assignees", [])]
    except (json.JSONDecodeError, KeyError, TypeError):
        return "error:invalid-json"

    label_change = resolved not in current_labels
    assign_change = assign_to is not None and current_assignee_ids != [assign_to]

    if not label_change and not assign_change:
        return "skipped:already-set"

    # Arrays have to travel in a JSON body: `glab api -f 'assignee_ids[]=7'` sends the literal
    # key "assignee_ids[]", which GitLab drops silently (or rejects with HTTP 400 when it is the
    # only parameter). --input needs an explicit Content-Type, otherwise glab gets a 415.
    body: dict[str, object] = {}
    if label_change:
        to_remove = [lbl for lbl in current_labels if lbl in BOARD_LABELS]
        if to_remove:
            body["remove_labels"] = ",".join(to_remove)
        body["add_labels"] = resolved
    if assign_change:
        body["assignee_ids"] = [assign_to]

    api_args = [
        "api",
        "-X",
        "PUT",
        f"projects/{project_id}/issues/{issue_iid}",
        "--input",
        "-",
        "-H",
        "Content-Type: application/json",
    ]
    if _run_glab(*api_args, stdin_data=json.dumps(body)) is None:
        return "error:api-call-failed"
    if label_change and assign_change:
        return f"set:{resolved}+assigned"
    if label_change:
        return f"set:{resolved}"
    return f"assigned:{resolved}"


def close_issue(issue_iid: str, project_id: str = "") -> str:
    """Close an issue and strip its board column label(s) in one call.

    Symmetric to :func:`transition`. Returns ``"closed"`` on success,
    ``"skipped:already-closed"`` if already closed, or ``"error:<reason>"``.
    """
    if not project_id:
        project_id = _get_project_id()
    if not project_id:
        return "error:no-project-id"

    raw = _run_glab("api", f"projects/{project_id}/issues/{issue_iid}")
    if not raw:
        return "error:cannot-fetch-issue"
    try:
        issue_data = json.loads(raw)
    except json.JSONDecodeError:
        return "error:invalid-json"
    if issue_data.get("state") == "closed":
        return "skipped:already-closed"

    to_remove = [lbl for lbl in issue_data.get("labels", []) if lbl in BOARD_LABELS]
    api_args = ["api", "-X", "PUT", f"projects/{project_id}/issues/{issue_iid}", "-f", "state_event=close"]
    if to_remove:
        api_args.extend(["-f", f"remove_labels={','.join(to_remove)}"])
    return "closed" if _run_glab(*api_args) is not None else "error:api-call-failed"


def settle_issue_after_merge(issue_iid: str, *, project_path: str = "", project_id: str = "") -> str:
    """Board move for a ticket whose fixing MR just merged, per the project's deploy topology.

    - a deployment step remains → ``workflow::To deploy`` (the ticket waits for the prod
      shipment; issue-workflow-update closes it once shipped).
    - none remains → close the ticket and strip its board column: GitLab autoclose is off on
      Pysae repos, so nothing else would close it. That covers both a repo opting out of the
      column (``board.to_deploy: false``) and one with no deploy branch at all — an infra repo
      whose CI applies from the MR pipeline is already deployed by the time it merges.

    :func:`deploy_branches.has_deploy_step` owns that decision, shared with
    ``issue-workflow-update`` so the live path and the reconciliation never disagree.

    Shared by ``pysae-ai-tools mr merge`` (manual) and the autopilot batch merge-gate so both paths
    settle the board identically. Returns a human-readable summary (``#123 → workflow::To
    deploy`` / ``#123 → Closed``), or ``""`` when there is no linked issue or the call fails.
    """
    if not issue_iid:
        return ""
    if not project_id and project_path:
        project_id = quote(project_path, safe="")
    if has_deploy_step(project_id, project_path):
        if transition(issue_iid, str(BoardLabel.TO_DEPLOY), project_id).startswith("set:"):
            return f"#{issue_iid} → {BoardLabel.TO_DEPLOY.value}"
        return ""
    if close_issue(issue_iid, project_id) == "closed":
        return f"#{issue_iid} → Closed"
    return ""


def main(
    issue_iid: Annotated[str, typer.Argument(help="Issue IID to transition")],
    label: Annotated[list[str], typer.Argument(help="New workflow label (supports multi-word labels)")],
    assign: Annotated[
        bool,
        typer.Option(
            "--assign/--no-assign",
            help="Make the current user the issue's sole assignee on transition (skipped in CI).",
        ),
    ] = True,
) -> None:
    """Transition a GitLab issue's board column label, taking the ticket over."""
    new_label = " ".join(label)

    # Honour the per-repo board flags: a repo off the board (board.enabled=false) or
    # with auto-advance disabled (board.sync=false) gets no workflow:: transition.
    root = Path.cwd()
    if not flag_enabled(root, "board", "enabled"):
        print("skipped:board.enabled disabled")
        return
    if not flag_enabled(root, "board", "sync"):
        print("skipped:board.sync disabled")
        return

    # Take the ticket over for whoever moves it — but never in CI, where the glab token is a
    # service account and self-assigning would pin every ticket on the bot.
    assign_to = get_current_user_id() if assign and not os.environ.get("CI") else None

    result = transition(issue_iid, new_label, assign_to=assign_to)
    print(result)

    if result.startswith("error:"):
        raise typer.Exit(code=1)
