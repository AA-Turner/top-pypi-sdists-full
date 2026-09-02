"""LangGraph state schema definitions for AGDT orchestration workflows."""

import operator
from typing import Annotated, Any, TypedDict

from typing_extensions import NotRequired


class WorkOnIssueEvent(TypedDict):
    """A single event entry in the workflow audit trail."""

    event: str
    timestamp: str
    signals: NotRequired[dict[str, Any]]


class WorkOnIssueState(TypedDict, total=False):
    """State schema for the work-on-jira-issue workflow.

    Uses LangGraph's Annotated channel pattern:
    - ``events`` uses ``operator.add`` reducer for append-only logging.
    - All other fields use default last-writer-wins semantics.

    Since ``TypedDict`` does not support default values, node functions
    must use ``.get()`` to handle missing keys gracefully.
    """

    issue_key: str
    step: str
    status: str
    plan: str
    error: str | None
    retry_count: int
    events: Annotated[list[WorkOnIssueEvent], operator.add]
    agent_context: dict[str, Any]
    affected_paths: list[str]

    # Routing signal fields — set by nodes, read by conditional edge functions
    issue_retrieved: bool
    needs_setup: bool
    plan_posted: bool
    checklist_complete: bool
    verification_ready: bool
    commit_created: bool
    branch_pushed: bool
    pr_created: bool

    # Additional checkpoint-compatibility routing fields (not part of the 8 primary signals)
    setup_complete: bool
    checklist_created: bool
    dry_run: bool
    dry_run_skipped: bool
    completion_comment_posted: bool

    # Issue provider and data fields (FR-002, FR-004)
    issue_provider: str  # "jira" or "github"
    issue_data: dict[str, Any]  # Normalized issue details

    # Checklist and implementation tracking (FR-001, FR-005)
    checklist_items: list[dict[str, Any]]  # Structured checklist entries
    implementation_log: list[dict[str, Any]]  # Per-item TDD results

    # Quality gate and verification (FR-006)
    verification_output: str  # Last quality gate output
    retry_budget: int  # Configured verification retry budget for routing

    # PR and commit metadata (FR-007, FR-008)
    pr_url: str  # Created PR URL
    commit_message: str  # Generated commit message
    pr_title: str  # Generated PR title

    # Structured worktree/commit node results (feature #1900)
    setup_result: Any  # SetupResult from the setup node
    commit_result: Any  # CommitResult from the commit node
    source_branch: str  # Branch created/resumed by setup, consumed by the PR node
    skip_rebase: bool  # When True, the commit node skips the rebase sub-step

    # Token usage tracking (NFR-002)
    token_usage_prompt: int  # Cumulative prompt tokens
    token_usage_completion: int  # Cumulative completion tokens

    # Blocked state detection (FR-004)
    blocked_reason: str | None  # Structured explanation for blocked state

    # Node status tracking for checkpoint/resume (FR-002, FR-010)
    _node_statuses: dict[str, Any]

    # Workflow run identifier — persisted in graph state so it survives
    # checkpoint/resume (SqliteSaver does not preserve configurable values).
    run_id: str
