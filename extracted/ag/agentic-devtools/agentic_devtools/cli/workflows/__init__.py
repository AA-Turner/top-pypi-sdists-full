"""
Workflow commands package.

Provides CLI commands for initiating and managing workflows with overrideable prompts.
"""

from __future__ import annotations

import sys
from pathlib import PurePath
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse

from .commands import (
    advance_pull_request_review_workflow,
    advance_work_on_jira_issue_workflow,
    create_checklist_cmd,
    initiate_apply_pull_request_review_suggestions_workflow,
    initiate_break_down_issue_into_subtasks_workflow,
    initiate_create_jira_epic_workflow,
    initiate_create_jira_issue_workflow,
    initiate_create_jira_subtask_workflow,
    initiate_optimize_issue_for_ai_agent_workflow,
    initiate_pr_merge_orchestrator_workflow,
    initiate_pull_request_review_workflow,
    initiate_update_jira_issue_workflow,
    initiate_work_on_jira_issue_workflow,
    setup_worktree_background_cmd,
    show_checklist_cmd,
    update_checklist_cmd,
)
from .manager import (
    NotifyEventResult,
    WorkflowEvent,
    get_next_workflow_prompt,
    get_next_workflow_prompt_cmd,
    notify_workflow_event,
)
from .orchestrator_commands import (
    audit_trio_async,
    audit_trio_cmd,
    orchestrate_finalize_async,
    orchestrate_finalize_cmd,
    orchestrate_init_async,
    orchestrate_init_cmd,
    orchestrate_step_async,
    orchestrate_step_cmd,
)


def advance_workflow_cmd() -> None:
    """
    CLI entry point for advancing a workflow to the next step.

    Usage:
        agdt-advance-workflow [step]
        agdt-advance-workflow --decision {approve|deny} --decision-id ID [--run-id RUN_ID]

    If step is not provided, advances to the next step automatically.
    The --decision flag is mutually exclusive with the positional step argument.
    """
    import argparse

    parser = argparse.ArgumentParser(
        prog="agdt-advance-workflow",
        description="Advance a workflow to the next step or resolve a pending decision.",
    )
    parser.add_argument(
        "step",
        nargs="?",
        default=None,
        help="Target step to advance to (optional).",
    )
    parser.add_argument(
        "--decision",
        choices=["approve", "deny"],
        default=None,
        help="Resolve a pending decision (mutually exclusive with positional step).",
    )
    parser.add_argument(
        "--decision-id",
        default=None,
        help="UUID of the pending decision to resolve.",
    )
    parser.add_argument(
        "--run-id",
        default=None,
        help="Run ID for decision resolution (defaults to agdt_run_id in state).",
    )

    args = parser.parse_args()

    # Mutual exclusivity check
    if args.decision is not None and args.step is not None:
        print("ERROR: --decision and positional [step] are mutually exclusive.", file=sys.stderr)
        sys.exit(1)

    # Decision mode
    if args.decision is not None:
        _handle_decision_mode(args)
        return

    # Standard workflow advancement (backward-compatible)
    step = args.step

    from ...state import get_state_dir, get_workflow_state, refresh_pin_file_ttl

    workflow = get_workflow_state()
    if not workflow:
        state_dir = get_state_dir()
        print("ERROR: No active workflow found.", file=sys.stderr)
        print(f"State directory checked: {state_dir.resolve()}", file=sys.stderr)
        if step:
            print(f"Requested step: {step}", file=sys.stderr)
        print(
            "\nNo re-initiation will be attempted. Use agdt-get-workflow or agdt-show to inspect state.",
            file=sys.stderr,
        )
        sys.exit(1)

    workflow_name = workflow.get("active", "")
    if workflow_name == "work-on-jira-issue":
        advance_work_on_jira_issue_workflow(step)
    elif workflow_name == "pull-request-review":
        advance_pull_request_review_workflow(step)
    else:
        print(f"ERROR: Workflow '{workflow_name}' does not support manual advancement.", file=sys.stderr)
        sys.exit(1)

    # Refresh pin file TTL after successful advancement (FR-010)
    if workflow_name == "pull-request-review":
        try:
            refresh_pin_file_ttl()
        except OSError as exc:
            print(f"WARNING: Pin file TTL refresh failed: {exc}", file=sys.stderr)


def _handle_decision_mode(args: argparse.Namespace) -> None:
    """Handle --decision flag for resolving pending decisions."""
    from ...state import get_state_dir, get_value

    decision = getattr(args, "decision", None)
    decision_id = getattr(args, "decision_id", None)
    run_id = getattr(args, "run_id", None)

    # Validate decision_id: reject None, empty, or whitespace-only
    if decision_id is not None:
        decision_id = str(decision_id).strip()
    if not decision_id:
        print("ERROR: --decision-id is required when using --decision.", file=sys.stderr)
        sys.exit(1)

    # Resolve run_id: prefer CLI arg, fall back to state; reject empty/whitespace
    if run_id is None:
        run_id = get_value("agdt_run_id")
    if run_id is not None:
        run_id = str(run_id).strip()
    if not run_id:
        print(
            "ERROR: --run-id not provided and 'agdt_run_id' not found in state.\n"
            "Set it with: agdt-set agdt_run_id <run-id>",
            file=sys.stderr,
        )
        sys.exit(1)
    if _run_id_looks_like_path(run_id):
        print("ERROR: --run-id must be a run identifier, not a file path.", file=sys.stderr)
        sys.exit(1)

    state_dir = get_state_dir()
    approved = decision == "approve"

    from agentic_devtools.orchestration.execution.decision_gate import resolve_decision

    try:
        resolved = resolve_decision(state_dir, run_id, decision_id, approved=approved)
        status_word = "approved" if approved else "denied"
        print(f"Decision {decision_id} {status_word} (action: {resolved.action_name})")
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


def _run_id_looks_like_path(run_id: str) -> bool:
    """Return True when run_id appears to be a filesystem path."""
    if "/" in run_id or "\\" in run_id or ":" in run_id:
        return True
    path = PurePath(run_id)
    return path.is_absolute() or any(part == ".." for part in path.parts)


__all__ = [
    "initiate_pull_request_review_workflow",
    "initiate_work_on_jira_issue_workflow",
    "initiate_create_jira_issue_workflow",
    "initiate_create_jira_epic_workflow",
    "initiate_create_jira_subtask_workflow",
    "initiate_update_jira_issue_workflow",
    "initiate_apply_pull_request_review_suggestions_workflow",
    "initiate_optimize_issue_for_ai_agent_workflow",
    "initiate_break_down_issue_into_subtasks_workflow",
    "initiate_pr_merge_orchestrator_workflow",
    "setup_worktree_background_cmd",
    "advance_workflow_cmd",
    "get_next_workflow_prompt",
    "get_next_workflow_prompt_cmd",
    "notify_workflow_event",
    "NotifyEventResult",
    "WorkflowEvent",
    "create_checklist_cmd",
    "update_checklist_cmd",
    "show_checklist_cmd",
    "orchestrate_init_cmd",
    "orchestrate_step_cmd",
    "orchestrate_finalize_cmd",
    "audit_trio_cmd",
    "orchestrate_init_async",
    "orchestrate_step_async",
    "orchestrate_finalize_async",
    "audit_trio_async",
]
