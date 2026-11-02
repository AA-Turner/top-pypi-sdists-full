"""CI and commit metadata helpers for PR snapshots."""

from __future__ import annotations

from agentic_devtools.cli.ci.models import CheckRunStatus, is_copilot_login
from agentic_devtools.cli.ci.provider import CIPlatformProvider

CODEQL_CHECK_NAMES = frozenset(
    {
        "Analyze (python)",
        "Analyze (actions)",
        "CodeQL",
        "Code scanning results / CodeQL",
        "CodeQL / Analyze (actions) (dynamic)",
        "CodeQL / Analyze (python) (dynamic)",
    }
)


def _evaluate_ci_status(
    check_runs: list[CheckRunStatus],
    actionable_check_names: frozenset[str],
    codeql_configured: bool = False,
) -> tuple[str, list[str]]:
    """Evaluate CI status, requiring success for completed configured CodeQL runs.

    Returns:
        Tuple of (status_string, list_of_failed_check_names).
    """
    actionable_checks: list[tuple[str, str]] = []
    codeql_seen = False

    for cr in check_runs:
        is_codeql_run, check_state = _classify_check_run(cr, actionable_check_names, codeql_configured)
        codeql_seen = codeql_seen or is_codeql_run
        if check_state is not None:
            actionable_checks.append((cr.name, check_state))
    failed_checks = [name for name, state in actionable_checks if state == "failing"]
    return _resolve_ci_status(actionable_checks, codeql_seen, codeql_configured, failed_checks)


def _resolve_ci_status(
    actionable_checks: list[tuple[str, str]],
    codeql_seen: bool,
    codeql_configured: bool,
    failed_checks: list[str],
) -> tuple[str, list[str]]:
    """Apply pipeline precedence to the classified actionable check states."""
    states = {state for _, state in actionable_checks}
    if codeql_configured and not codeql_seen:
        return "pending", failed_checks
    if not actionable_checks:
        return "pending", []
    if "pending" in states:
        return "pending", failed_checks
    if "failing" in states:
        return "failing", failed_checks
    if "unknown" in states:
        return "unknown", failed_checks
    return "passing", []


def _classify_check_run(
    check_run: CheckRunStatus,
    actionable_check_names: frozenset[str],
    codeql_configured: bool,
) -> tuple[bool, str | None]:
    """Classify a trusted check run as pending, failing, unknown, or successful."""
    is_codeql_run = check_run.name in CODEQL_CHECK_NAMES
    if is_codeql_run and check_run.app_slug not in {"github-advanced-security", "github-actions", ""}:
        return False, None
    if check_run.name not in actionable_check_names and not (codeql_configured and is_codeql_run):
        return is_codeql_run, None
    if check_run.status != "completed":
        return is_codeql_run, "pending"
    if check_run.conclusion == "failure" or (codeql_configured and is_codeql_run and check_run.conclusion != "success"):
        return is_codeql_run, "failing"
    if check_run.conclusion not in ("success", "neutral", "skipped"):
        return is_codeql_run, "unknown"
    return is_codeql_run, "passing"


def _is_copilot_review_pending(requested_reviewers: list[str]) -> bool:
    """Return True when Copilot is currently requested as a pending reviewer."""
    return any(is_copilot_login(reviewer) for reviewer in requested_reviewers)


def _count_commits(provider: CIPlatformProvider, *, base_branch: str, head_sha: str) -> int:
    """Return commit count above merge-base, or 1 when the provider lacks support.

    Raises:
        Exception: Propagated from the provider when commit counting is supported
            but fails. The caller should treat this as a metadata failure so the
            pipeline does not proceed with an unknown commit count.
    """
    counter = getattr(provider, "count_commits_above_merge_base", None)
    if not callable(counter):
        return 1
    count = counter(base_branch=base_branch, head_sha=head_sha)
    return int(count)


def _count_commits_behind(provider: CIPlatformProvider, *, pr_number: int, base_branch: str, head_branch: str) -> int:
    """Return how many commits head is behind base, or 0 when unsupported.

    Raises:
        Exception: Propagated from the provider when behind-counting is supported
            but fails. The caller should treat this as a metadata failure so the
            pipeline does not proceed with an unknown behind count.
    """
    counter = getattr(provider, "count_commits_behind", None)
    if not callable(counter):
        return 0
    return int(counter(pr_number=pr_number, base_branch=base_branch, head_branch=head_branch))
