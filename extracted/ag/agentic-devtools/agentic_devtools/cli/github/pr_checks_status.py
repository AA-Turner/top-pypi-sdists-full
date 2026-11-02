"""
PR CI/status check verification via ``gh pr checks`` and effective required checks.

Provides ``get_pr_checks_status()`` for programmatic use and
``pr_checks_status_command()`` as the CLI entry point for
``agdt-gh-pr-checks-status``.
"""

from __future__ import annotations

import argparse
import json
import sys
import time

from ...state import get_value, set_value
from ..subprocess_utils import run_safe
from ._pr_check_requirements import _resolve_required_checks
from .pr_state import get_pr_state
from .repo_resolution import resolve_github_repo

_GH_PR_CHECKS_JSON_FIELDS = "name,state,bucket,workflow,completedAt,description"
_MAX_RETRIES = 2
_RETRY_DELAY_SECONDS = 10.0


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _fetch_pr_checks(pr_number: int, repo: str) -> list[dict]:
    """Fetch structured check results via ``gh pr checks --json``.

    Retries up to *_MAX_RETRIES* times on failure.  Calls ``sys.exit(1)``
    when all retries are exhausted.
    """
    cmd = [
        "gh",
        "pr",
        "checks",
        str(pr_number),
        "--repo",
        repo,
        "--json",
        _GH_PR_CHECKS_JSON_FIELDS,
    ]

    last_error = ""
    for attempt in range(_MAX_RETRIES + 1):
        try:
            result = run_safe(cmd, capture_output=True, text=True, shell=False)
        except FileNotFoundError:
            print(
                "Error: 'gh' CLI is not installed or not on PATH. Install from https://cli.github.com/",
                file=sys.stderr,
            )
            sys.exit(1)
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                if isinstance(data, list):
                    return data
                last_error = f"Unexpected JSON type: {type(data).__name__}"
            except json.JSONDecodeError as exc:
                last_error = f"JSON parse error: {exc}"
        else:
            last_error = (result.stderr or "").strip() or f"exit code {result.returncode}"

        if attempt < _MAX_RETRIES:
            print(
                f"Warning: gh pr checks failed (attempt {attempt + 1}/{_MAX_RETRIES + 1}): "
                f"{last_error}. Retrying in {_RETRY_DELAY_SECONDS}s …",
                file=sys.stderr,
            )
            time.sleep(_RETRY_DELAY_SECONDS)

    print(
        f"Error: gh pr checks failed after {_MAX_RETRIES + 1} attempts: {last_error}",
        file=sys.stderr,
    )
    sys.exit(1)


def _classify_checks(checks: list[dict]) -> dict:
    """Classify checks by their ``bucket`` field.

    Returns a dict with counts and lists of failed/pending check names.
    """
    passed = 0
    failed = 0
    pending = 0
    skipped = 0
    cancelled = 0
    failed_checks: list[str] = []
    pending_checks: list[str] = []

    for check in checks:
        bucket = check.get("bucket", "")
        name = check.get("name", "unknown")
        if bucket == "pass":
            passed += 1
        elif bucket == "fail":
            failed += 1
            failed_checks.append(name)
        elif bucket == "pending":
            pending += 1
            pending_checks.append(name)
        elif bucket == "skipping":
            skipped += 1
        elif bucket == "cancel":
            cancelled += 1
        # Unknown bucket values are silently ignored (not counted)

    return {
        "passed": passed,
        "failed": failed,
        "pending": pending,
        "skipped": skipped,
        "cancelled": cancelled,
        "total": len(checks),
        "failedChecks": failed_checks,
        "pendingChecks": pending_checks,
    }


def _normalize_repo(repo: str) -> str:
    """Validate and normalize a *owner/repo* string.

    Strips whitespace and a trailing ``.git`` suffix, then verifies the
    value contains exactly one ``/`` separator.  Calls ``sys.exit(1)``
    with a user-facing message when the format is invalid.
    """
    repo = repo.strip()
    if repo.endswith(".git"):
        repo = repo[: -len(".git")]
    if "/" not in repo or repo.count("/") != 1:
        print(
            f"Error: invalid repo format '{repo}'. Expected 'owner/repo' "
            "(for example: agdt-set github.repo myorg/myrepo).",
            file=sys.stderr,
        )
        sys.exit(1)
    owner, name = repo.split("/", 1)
    if not owner or not name:
        print(
            f"Error: invalid repo format '{repo}'. Both owner and repo name "
            "must be non-empty (for example: agdt-set github.repo myorg/myrepo).",
            file=sys.stderr,
        )
        sys.exit(1)
    return repo


def _reconcile_results(classification: dict, required_checks: dict) -> dict:
    """Determine final status and build output dict."""
    if classification["pending"] > 0:
        status = "pending"
    elif classification["failed"] > 0:
        status = "failed"
    elif classification["cancelled"] > 0:
        status = "cancelled"
    else:
        status = "all-pass"

    if status == "all-pass" and not required_checks.get("ready"):
        runs = required_checks.get("checkRuns")
        if not required_checks.get("complete") or not isinstance(runs, list):
            status = "pending"
        else:
            pending = any(not isinstance(run, dict) or run.get("status") != "completed" for run in runs)
            completed = [run for run in runs if isinstance(run, dict) and run.get("status") == "completed"]
            cancelled = any(run.get("conclusion") == "cancelled" for run in completed)
            failed = any(
                run.get("conclusion") not in ("success", "neutral", "skipped", "cancelled") for run in completed
            )
            status = "pending" if pending else "failed" if failed else "cancelled" if cancelled else "pending"

    return {
        "status": status,
        "totalChecks": classification["total"],
        "passed": classification["passed"],
        "failed": classification["failed"],
        "pending": classification["pending"],
        "skipped": classification["skipped"],
        "cancelled": classification["cancelled"],
        "failedChecks": classification["failedChecks"],
        "pendingChecks": classification["pendingChecks"],
        "requiredChecksDiagnostics": required_checks.get("diagnostics", []),
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def get_pr_checks_status(
    pr_number: int,
    repo: str,
    head_sha: str | None = None,
    base_branch: str | None = None,
) -> dict:
    """Fetch, classify, resolve applicable checks, and reconcile PR status.

    Writes ``github.pr_checks_status``, ``github.pr_checks_failed``, and
    ``github.pr_checks_pending`` to state.

    Returns the full structured result dict.
    """
    repo = _normalize_repo(repo)
    checks = _fetch_pr_checks(pr_number, repo)
    classification = _classify_checks(checks)

    if base_branch is None:
        pr_snapshot = get_pr_state(pr_number, repo)
        if head_sha is None:
            head_sha = pr_snapshot.get("headRefOid")
        elif head_sha != pr_snapshot.get("headRefOid"):
            head_sha = ""
        base_branch = pr_snapshot.get("baseRefName")

    base = base_branch if isinstance(base_branch, str) else ""
    head = head_sha if isinstance(head_sha, str) else ""
    required_checks = _resolve_required_checks(repo, base, head)
    result = _reconcile_results(classification, required_checks)
    result["prNumber"] = pr_number
    result["repo"] = repo

    # Persist to state for downstream commands
    set_value("github.pr_checks_status", result["status"])
    set_value("github.pr_checks_failed", result["failedChecks"])
    set_value("github.pr_checks_pending", result["pendingChecks"])

    return result


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def pr_checks_status_command() -> None:
    """CLI entry point for ``agdt-gh-pr-checks-status``."""
    parser = argparse.ArgumentParser(
        description="Check CI/status check results for a GitHub PR.",
    )
    parser.add_argument("--pr", type=int, default=None, help="Pull request number")
    parser.add_argument(
        "--repo",
        type=str,
        default=None,
        help="Repository in owner/repo format",
    )
    parser.add_argument(
        "--head-sha",
        type=str,
        default=None,
        help="Head commit SHA for required-check verification",
    )
    args = parser.parse_args()

    # Resolve PR number
    pr_number = args.pr
    if pr_number is None:
        pr_number = get_value("github.pull_request_number")
    if pr_number is None:
        print(
            "Error: PR number required. Provide --pr or set github.pull_request_number in state (via agdt-set).",
            file=sys.stderr,
        )
        sys.exit(1)
    try:
        pr_number = int(pr_number)
    except TypeError, ValueError:
        print(
            "Error: PR number must be an integer. Provide --pr <number> or set "
            "github.pull_request_number to a valid integer (for example: "
            "agdt-set github.pull_request_number 123).",
            file=sys.stderr,
        )
        sys.exit(1)

    # Resolve repo
    repo = resolve_github_repo(args.repo)

    # Resolve head SHA (optional — graceful degradation)
    head_sha = args.head_sha
    if head_sha is None:
        head_sha = get_value("github.head_ref_oid")
        if head_sha is not None:
            head_sha = str(head_sha)
    if head_sha is None:
        print(
            "Notice: head_ref_oid not available in state — current PR head/base will be resolved "
            "for required-check verification.",
            file=sys.stderr,
        )

    result = get_pr_checks_status(pr_number, repo, head_sha)
    print(json.dumps(result, indent=2))
