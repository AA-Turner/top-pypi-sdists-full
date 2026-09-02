"""Verification node: run quality gates and track retry count.

Executes ``bash scripts/targeted-checks.sh`` and evaluates results.
On failure, increments retry count and returns an error. Routing back
to implementation (when retries remain) or to error_handler (when the
budget is exhausted) is handled by the graph routing functions in
``pilot_workflow.py``.
"""

from __future__ import annotations

from typing import Any

from agentic_devtools.orchestration.nodes._helpers import resolve_repo_root, run_command, utc_now
from agentic_devtools.orchestration.state_schema import WorkOnIssueState

# Maximum characters stored in state for verification output.
# Full output (which may include pytest traces and coverage reports) is
# truncated before persisting to avoid bloating checkpoints.
_MAX_STORED_OUTPUT_CHARS = 4000
# Prefix prepended to the stored tail when output is truncated.
_TRUNCATION_PREFIX = "[... truncated ...]\n"


def verification_node(state: WorkOnIssueState) -> dict[str, Any]:
    """Execute quality gates and evaluate pass/fail.

    Runs ``bash scripts/targeted-checks.sh`` in default check mode.
    Exit code 0 means all checks pass; exit 1-9 indicates failed check count.
    Skips execution and returns success when ``dry_run`` is active so a simulated
    setup worktree (which does not exist on disk) is never used as ``cwd``.
    """
    retry_count = _normalize_retry_count(state.get("retry_count", 0))

    if state.get("dry_run"):
        return {
            "step": "verification",
            "error": None,
            "retry_count": retry_count,
            "verification_output": "[dry run — quality gates skipped]",
            "events": [
                {
                    "event": "verification_skipped_dry_run",
                    "timestamp": utc_now(),
                }
            ],
        }

    repo_root = resolve_repo_root(state)

    # Guard: when setup_result checkpoints an explicit worktree path that is now
    # gone or invalid, resolve_repo_root returns None. Running quality gates with
    # cwd=None would use the process checkout and falsely report success for the
    # wrong repository. Treat an unresolved explicit worktree as a failure.
    _setup = state.get("setup_result") if isinstance(state, dict) else None
    if repo_root is None and _setup is not None and getattr(_setup, "worktree_path", None):
        _wt_path = _setup.worktree_path
        error_msg = f"Setup worktree '{_wt_path}' is no longer accessible; aborting verification"
        return {
            "step": "verification",
            "error": error_msg,
            "retry_count": retry_count,
            "verification_output": "",
            "events": [
                {
                    "event": "verification_failed",
                    "timestamp": utc_now(),
                    "signals": {"exit_code": -1, "reason": "worktree_unavailable"},
                }
            ],
        }

    # Execute quality gates
    result = run_command(
        ["bash", "scripts/targeted-checks.sh"],
        timeout=300,
        cwd=str(repo_root) if repo_root is not None else None,
    )

    full_output = result.stdout + result.stderr
    # Truncate for state storage; full output may include large pytest/coverage reports.
    # Prepend a marker so consumers can tell the output was clipped.
    if len(full_output) > _MAX_STORED_OUTPUT_CHARS:
        tail_chars = _MAX_STORED_OUTPUT_CHARS - len(_TRUNCATION_PREFIX)
        stored_output = _TRUNCATION_PREFIX + full_output[-tail_chars:]
    else:
        stored_output = full_output

    if result.returncode == 0:
        # All checks passed
        return {
            "step": "verification",
            "error": None,
            "retry_count": retry_count,
            "verification_output": stored_output,
            "events": [
                {
                    "event": "verification_passed",
                    "timestamp": utc_now(),
                    "signals": {"exit_code": 0},
                }
            ],
        }

    # Checks failed — increment retry count
    retry_count += 1
    error_msg = (
        f"Quality gate failed (exit code {result.returncode}). Retry {retry_count}.\nOutput:\n{stored_output[:2000]}"
    )

    return {
        "step": "verification",
        "error": error_msg,
        "retry_count": retry_count,
        "verification_output": stored_output,
        "events": [
            {
                "event": "verification_failed",
                "timestamp": utc_now(),
                "signals": {
                    "exit_code": result.returncode,
                    "retry_count": retry_count,
                },
            }
        ],
    }


def _normalize_retry_count(value: object) -> int:
    """Return retry_count as int, coercing non-int values to 0."""
    if isinstance(value, bool):
        return 0
    if not isinstance(value, int):
        return 0
    if value < 0:
        return 0
    return value
