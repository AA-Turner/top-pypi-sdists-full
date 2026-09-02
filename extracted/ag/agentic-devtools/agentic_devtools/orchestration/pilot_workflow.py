"""Routing helpers plus legacy compatibility stubs for the pilot workflow.

``build_work_on_issue_graph`` wires real node implementations from
``agentic_devtools.orchestration.nodes``. The node functions in this module are
kept only as lightweight compatibility shims for older direct imports and
legacy unit tests.
"""

from datetime import datetime, timezone

from .state_schema import WorkOnIssueState

MAX_RETRIES = 3  # Maximum number of verification retry loops before routing to error_handler


def _utc_now() -> str:
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


def _normalize_retry_count(value: object) -> int:
    """Return retry_count as int, coercing ``None``/non-int values to 0."""
    if not isinstance(value, int):
        return 0
    if isinstance(value, bool):
        return 0
    if value < 0:
        return 0
    return value


def _normalize_retry_budget(value: object) -> int:
    """Return retry_budget as int, falling back to :data:`MAX_RETRIES`."""
    if isinstance(value, bool):
        return MAX_RETRIES
    if not isinstance(value, int):
        return MAX_RETRIES
    if value < 0:
        return MAX_RETRIES
    return value


# ---------------------------------------------------------------------------
# Legacy compatibility node shims
# ---------------------------------------------------------------------------


def initiate_node(state: WorkOnIssueState) -> dict:
    """Entry point: set initial step and status (stub — no validation in Phase 1).

    Reads any pre-existing ``error`` (e.g., from a pre-flight check) and
    translates it into routing signals. The error is cleared so that
    ``route_after_initiate`` routes on signals, not raw error.
    """
    pre_flight_error = state.get("error")
    needs_setup = bool(pre_flight_error)
    issue_retrieved = not needs_setup
    return {
        "step": "initiate",
        "status": "active",
        "error": None,  # Clear pre-flight error; routing uses signals
        "issue_retrieved": issue_retrieved,
        "needs_setup": needs_setup,
        "events": [
            {
                "event": "initiate_completed",
                "timestamp": _utc_now(),
                "signals": {
                    "issue_retrieved": issue_retrieved,
                    "needs_setup": needs_setup,
                    "pre_flight_error": pre_flight_error,
                },
            }
        ],
    }


def setup_node(state: WorkOnIssueState) -> dict:
    """Handle worktree/branch setup when pre-flight checks fail."""
    return {
        "step": "setup",
        "error": None,
        "setup_complete": True,
        "events": [{"event": "setup_completed", "timestamp": _utc_now()}],
    }


def planning_node(state: WorkOnIssueState) -> dict:
    """Analyse the issue and prepare a plan."""
    return {
        "step": "planning",
        "plan": "Stub plan for " + state.get("issue_key", "UNKNOWN"),
        "plan_posted": True,
        "events": [
            {
                "event": "planning_completed",
                "timestamp": _utc_now(),
                "signals": {"plan_posted": True},
            }
        ],
    }


def checklist_creation_node(state: WorkOnIssueState) -> dict:
    """Create the implementation checklist."""
    return {
        "step": "checklist_creation",
        "checklist_created": True,
        "events": [{"event": "checklist_creation_completed", "timestamp": _utc_now()}],
    }


def implementation_node(state: WorkOnIssueState) -> dict:
    """Execute the implementation work.

    Clears any ``error`` carried over from a verification retry so that
    ``route_after_implementation`` routes to ``implementation_review`` rather
    than to ``error_handler``.
    """
    return {
        "step": "implementation",
        "error": None,
        "checklist_complete": True,
        "events": [
            {
                "event": "implementation_completed",
                "timestamp": _utc_now(),
                "signals": {"checklist_complete": True},
            }
        ],
    }


def implementation_review_node(state: WorkOnIssueState) -> dict:
    """Review the completed implementation."""
    return {
        "step": "implementation_review",
        "verification_ready": True,
        "events": [
            {
                "event": "implementation_review_completed",
                "timestamp": _utc_now(),
                "signals": {"verification_ready": True},
            }
        ],
    }


def verification_node(state: WorkOnIssueState) -> dict:
    """Run tests and quality gates.

    The stub preserves any existing ``error`` and increments ``retry_count``
    so that the downstream ``route_after_verify`` retry path is reachable
    during compiled-graph execution.
    """
    retry_count = _normalize_retry_count(state.get("retry_count", 0))
    existing_error = state.get("error")
    if existing_error:
        retry_count += 1
    return {
        "step": "verification",
        "error": existing_error,
        "retry_count": retry_count,
        "events": [
            {
                "event": "verification_completed",
                "timestamp": _utc_now(),
                "signals": {"error": existing_error, "retry_count": retry_count},
            }
        ],
    }


def commit_node(state: WorkOnIssueState) -> dict:
    """Stage and commit changes."""
    return {
        "step": "commit",
        "commit_created": True,
        "branch_pushed": True,
        "events": [
            {
                "event": "commit_completed",
                "timestamp": _utc_now(),
                "signals": {"commit_created": True, "branch_pushed": True},
            }
        ],
    }


def pull_request_node(state: WorkOnIssueState) -> dict:
    """Create or update the pull request."""
    return {
        "step": "pull_request",
        "pr_created": True,
        "events": [
            {
                "event": "pull_request_completed",
                "timestamp": _utc_now(),
                "signals": {"pr_created": True},
            }
        ],
    }


def completion_node(state: WorkOnIssueState) -> dict:
    """Mark the workflow as complete."""
    return {
        "step": "completion",
        "status": "completed",
        "events": [{"event": "completion_completed", "timestamp": _utc_now()}],
    }


def error_handler_node(state: WorkOnIssueState) -> dict:
    """Terminal error handler: log context and mark workflow as failed or blocked.

    Preserves ``status="blocked"`` when the incoming state already carries that
    status (e.g., from ``planning_node``), so callers can distinguish a blocked
    issue from a hard failure.  Also derives ``"blocked"`` from a non-``None``
    ``error`` field on ``setup_result`` or ``commit_result``, since those nodes
    embed ``BlockedState`` in the result object rather than setting the top-level
    ``status`` key directly.
    """
    incoming_status = state.get("status")
    if incoming_status != "blocked":
        # Derive blocked status from structured node results.
        setup_result = state.get("setup_result")
        commit_result = state.get("commit_result")
        if getattr(setup_result, "error", None) is not None or getattr(commit_result, "error", None) is not None:
            incoming_status = "blocked"
    final_status = "blocked" if incoming_status == "blocked" else "failed"
    return {
        "step": "error_handler",
        "status": final_status,
        "error": state.get("error"),
        "events": [
            {
                "event": "error_handler_invoked",
                "timestamp": _utc_now(),
                "signals": {
                    "error": state.get("error"),
                    "failed_step": state.get("step"),
                },
            }
        ],
    }


# ---------------------------------------------------------------------------
# Conditional edge functions
# ---------------------------------------------------------------------------


def route_after_initiate(state: WorkOnIssueState) -> str:
    """Route based on initiate node outcome signals.

    Priority: error → setup. ``initiate_node`` only performs pre-flight
    validation; it does not fetch the issue. Setup must run before retrieval so
    branch validation/creation is always applied, and can no-op when the branch
    already targets the issue. ``issue_retrieved`` is deliberately NOT consulted
    here — it is owned by ``retrieve_node`` and read by ``route_after_retrieve``.
    """
    if state.get("error"):
        return "error_handler"
    return "setup"


def route_after_plan(state: WorkOnIssueState) -> str:
    """Route to ``checklist_creation`` once a plan has been produced.

    Planning-comment delivery is best-effort (``plan_posted`` reports actual
    delivery and is ``False`` in dry-run or on a failed post), so routing keys
    off ``error`` only — a skipped or failed comment post must not halt the
    workflow. Routes to ``error_handler`` when an error is present, otherwise
    to ``checklist_creation``.
    """
    if state.get("error"):
        return "error_handler"
    return "checklist_creation"


def route_after_setup(state: WorkOnIssueState) -> str:
    """Route to ``retrieve`` when setup completes successfully.

    Prefers the structured ``setup_result`` (a :class:`SetupResult`): a
    non-``None`` ``error`` routes to ``error_handler``; a result with a
    non-blank ``worktree_path``, non-blank ``branch_name``, and a valid
    ``mode`` (``"created"`` or ``"resumed"``) routes to ``retrieve``; any
    other result (partial/corrupt checkpoint) routes to ``error_handler``.
    Falls back to the legacy ``error``/``setup_complete`` booleans for
    pre-refactor checkpoints.
    """
    setup_result = state.get("setup_result")
    if setup_result is not None:
        if getattr(setup_result, "error", None) is not None:
            return "error_handler"
        worktree_path = getattr(setup_result, "worktree_path", None)
        branch_name = getattr(setup_result, "branch_name", None)
        mode = getattr(setup_result, "mode", None)
        if worktree_path and branch_name and mode in ("created", "resumed"):
            return "retrieve"
        return "error_handler"
    if state.get("error"):
        return "error_handler"
    if state.get("setup_complete"):
        return "retrieve"
    if "setup_complete" not in state:
        return "retrieve"
    return "error_handler"


def route_after_retrieve(state: WorkOnIssueState) -> str:
    """Route to ``planning`` when issue retrieval succeeds.

    Checks the ``issue_retrieved`` signal set by the retrieve node.
    """
    if state.get("error"):
        return "error_handler"
    if state.get("issue_retrieved"):
        return "planning"
    if "issue_retrieved" not in state:
        return "planning"
    return "error_handler"


def route_after_checklist_creation(state: WorkOnIssueState) -> str:
    """Route to ``implementation`` when checklist creation succeeds."""
    if state.get("error"):
        return "error_handler"
    if state.get("checklist_created"):
        return "implementation"
    if "checklist_created" not in state:
        return "implementation"
    return "error_handler"


def route_after_implementation(state: WorkOnIssueState) -> str:
    """Route to ``implementation_review`` when checklist is complete.

    Legacy fallback: when ``checklist_complete`` is absent, route to
    ``implementation_review`` (the pre-refactor default successor).
    """
    if state.get("error"):
        return "error_handler"
    if state.get("checklist_complete"):
        return "implementation_review"
    # Legacy checkpoint fallback
    if "checklist_complete" not in state:
        return "implementation_review"
    return "error_handler"


def route_after_implementation_review(state: WorkOnIssueState) -> str:
    """Route to ``verification`` when implementation review signals readiness.

    Legacy fallback: when ``verification_ready`` is absent, route to
    ``verification`` (the pre-refactor default successor).
    """
    if state.get("error"):
        return "error_handler"
    if state.get("verification_ready"):
        return "verification"
    # Legacy checkpoint fallback
    if "verification_ready" not in state:
        return "verification"
    return "error_handler"


def route_after_verify(state: WorkOnIssueState) -> str:
    """Route back to ``implementation`` on retryable error, otherwise ``commit``.

    Caps retry loops at the policy-provided ``retry_budget`` when present,
    otherwise falls back to :data:`MAX_RETRIES` for checkpoint compatibility.
    Routes to ``error_handler`` when retries are exhausted.
    """
    retry_count = _normalize_retry_count(state.get("retry_count", 0))
    retry_budget = _normalize_retry_budget(state.get("retry_budget", MAX_RETRIES))
    if state.get("error") and retry_count < retry_budget:
        return "implementation"
    if state.get("error") and retry_count >= retry_budget:
        return "error_handler"
    return "commit"


def route_after_commit(state: WorkOnIssueState) -> str:
    """Route to ``pull_request`` when the commit succeeds (including no-ops).

    Prefers the structured ``commit_result`` (a :class:`CommitResult`): a
    non-``None`` ``error`` routes to ``error_handler``; a result where
    ``push_succeeded`` or ``no_op`` is ``True`` routes to ``pull_request``;
    any other result (partial/corrupt checkpoint) routes to
    ``error_handler``. Falls back to the legacy ``commit_created``/
    ``branch_pushed`` booleans for pre-refactor checkpoints.
    """
    commit_result = state.get("commit_result")
    if commit_result is not None:
        if getattr(commit_result, "error", None) is not None:
            return "error_handler"
        push_succeeded = getattr(commit_result, "push_succeeded", False)
        no_op = getattr(commit_result, "no_op", False)
        if push_succeeded or no_op:
            return "pull_request"
        return "error_handler"
    if state.get("error"):
        return "error_handler"
    if state.get("commit_created") and state.get("branch_pushed"):
        return "pull_request"
    # Legacy checkpoint fallback
    if "commit_created" not in state and "branch_pushed" not in state:
        return "pull_request"
    return "error_handler"


def route_after_pull_request(state: WorkOnIssueState) -> str:
    """Route to ``completion`` when PR is created.

    Legacy fallback: when ``pr_created`` is absent, route to ``completion``
    (the pre-refactor default successor).
    """
    if state.get("error"):
        return "error_handler"
    if state.get("pr_created"):
        return "completion"
    # Legacy checkpoint fallback
    if "pr_created" not in state:
        return "completion"
    return "error_handler"


# ---------------------------------------------------------------------------
# Mermaid diagram helper
# ---------------------------------------------------------------------------


def get_mermaid_diagram() -> str:
    """Build the pilot workflow graph and return its Mermaid diagram string."""
    from .graph_builder import build_work_on_issue_graph

    compiled = build_work_on_issue_graph()
    return compiled.get_graph().draw_mermaid()
