"""
Approve a GitHub PR with built-in verification and retry.

Submits a PR approval via ``gh pr review --approve`` or, when an
expected head SHA is supplied, via the reviews API with ``commit_id``
pinned to that SHA. Resolves the authenticated user's login, verifies
the approval was registered by querying the reviews API, and retries
verification up to 2 times.

Returns structured JSON to stdout and writes state keys for downstream
commands.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from typing import Any

from ...state import get_value, set_value
from ..subprocess_utils import run_safe
from .repo_resolution import resolve_github_repo

_DEFAULT_APPROVAL_BODY = "Approved via agdt-gh-pr-approve"
_SHA40_RE = re.compile(r"[0-9a-f]{40}\Z")
_GH_COMMAND_TIMEOUT_SECONDS = 30


def _check_gh_available() -> None:
    """Verify ``gh`` CLI is installed, or exit with a helpful error."""
    if shutil.which("gh") is None:
        print(
            "Error: 'gh' CLI is not installed or not on PATH. Install from https://cli.github.com/",
            file=sys.stderr,
        )
        sys.exit(1)


def _resolve_current_user(env: dict[str, str] | None = None) -> str:
    """Resolve the authenticated GitHub user's login.

    Returns:
        The login string (e.g. ``"acmarsnik"``).

    Raises:
        SystemExit: If the user cannot be resolved.
    """
    try:
        result = run_safe(
            ["gh", "api", "user", "--jq", ".login"],
            capture_output=True,
            text=True,
            shell=False,
            timeout=_GH_COMMAND_TIMEOUT_SECONDS,
            env=env,
        )
    except subprocess.TimeoutExpired as exc:
        print(
            f"Error: Could not resolve current GitHub user. gh api timed out after {exc.timeout}s.",
            file=sys.stderr,
        )
        sys.exit(1)
    login = result.stdout.strip() if result.returncode == 0 else ""
    if not login:
        gh_error_detail = (result.stderr or result.stdout).strip()
        if gh_error_detail:
            print(
                "Error: Could not resolve current GitHub user. "
                f"Ensure 'gh auth login' has been run. gh error: {gh_error_detail}",
                file=sys.stderr,
            )
        else:
            print(
                "Error: Could not resolve current GitHub user. "
                "Ensure 'gh auth login' has been run. "
                f"gh exited with code {result.returncode}.",
                file=sys.stderr,
            )
        sys.exit(1)
    return login


def _submit_approval(
    pr_number: int,
    repo: str,
    body: str,
    expected_head: str | None = None,
    env: dict[str, str] | None = None,
) -> tuple[bool, str]:
    """Submit a PR approval via ``gh pr review --approve``.

    Args:
        pr_number: The pull request number.
        repo: ``owner/repo`` string.
        body: Approval comment body.
        expected_head: Optional full 40-character ``headRefOid``. When
            provided, the approval is posted through the reviews API with
            ``commit_id`` pinned to that SHA.

    Returns:
        ``(True, "")`` on success, ``(False, error_message)`` on failure.
    """
    try:
        if expected_head is None:
            result = run_safe(
                [
                    "gh",
                    "pr",
                    "review",
                    str(pr_number),
                    "--repo",
                    repo,
                    "--approve",
                    "--body",
                    body,
                ],
                capture_output=True,
                text=True,
                shell=False,
                timeout=_GH_COMMAND_TIMEOUT_SECONDS,
                env=env,
            )
        else:
            owner, repo_name = _validate_repo_format(repo)
            result = run_safe(
                [
                    "gh",
                    "api",
                    f"repos/{owner}/{repo_name}/pulls/{pr_number}/reviews",
                    "--method",
                    "POST",
                    "--input",
                    "-",
                ],
                capture_output=True,
                text=True,
                input=json.dumps(
                    {
                        "body": body,
                        "commit_id": expected_head,
                        "event": "APPROVE",
                    }
                ),
                shell=False,
                timeout=_GH_COMMAND_TIMEOUT_SECONDS,
                env=env,
            )
    except subprocess.TimeoutExpired as exc:
        command_name = "gh api" if expected_head is not None else "gh pr review"
        return False, f"{command_name} timed out after {exc.timeout}s"
    if result.returncode == 0:
        return (True, "")
    error_message = (result.stderr or result.stdout).strip()
    if not error_message:
        command_name = "gh api" if expected_head is not None else "gh pr review"
        error_message = f"{command_name} failed with exit code {result.returncode}"
    return (False, error_message)


def _validate_repo_format(repo: str) -> tuple[str, str]:
    """Validate and split ``owner/repo`` into its components.

    Args:
        repo: The ``owner/repo`` string to validate.

    Returns:
        ``(owner, repo_name)`` tuple.

    Raises:
        SystemExit: If *repo* is not in valid ``owner/repo`` format.
    """
    normalized_repo = repo.strip()
    if normalized_repo.endswith(".git"):
        normalized_repo = normalized_repo[:-4]

    if normalized_repo.count("/") != 1:
        print(
            f"Error: Invalid repo format '{repo}'. Expected 'owner/repo'.",
            file=sys.stderr,
        )
        sys.exit(1)

    owner, repo_name = (part.strip() for part in normalized_repo.split("/"))
    if not owner or not repo_name:
        print(
            f"Error: Invalid repo format '{repo}'. Expected 'owner/repo'.",
            file=sys.stderr,
        )
        sys.exit(1)
    return owner, repo_name


def _fetch_current_head_sha(pr_number: int, repo: str, env: dict[str, str] | None = None) -> tuple[str | None, str]:
    """Fetch the pull request's current head commit SHA via the GitHub API.

    Args:
        pr_number: The pull request number.
        repo: ``owner/repo`` string.

    Returns:
        ``(sha, "")`` on success, or ``(None, error_message)`` when the head
        SHA could not be resolved.
    """
    owner, repo_name = _validate_repo_format(repo)
    try:
        result = run_safe(
            ["gh", "api", f"repos/{owner}/{repo_name}/pulls/{pr_number}", "--jq", ".head.sha"],
            capture_output=True,
            text=True,
            shell=False,
            timeout=_GH_COMMAND_TIMEOUT_SECONDS,
            env=env,
        )
    except subprocess.TimeoutExpired as exc:
        return None, f"gh api timed out after {exc.timeout}s"
    sha = result.stdout.strip() if result.returncode == 0 else ""
    if sha:
        return sha, ""
    error_message = (result.stderr or result.stdout).strip()
    if not error_message:
        error_message = f"gh api exited with code {result.returncode}"
    return None, error_message


def _confirm_head_unchanged(
    pr_number: int,
    repo: str,
    expected_head: str,
    env: dict[str, str] | None = None,
) -> tuple[bool, str | None, str]:
    """Re-fetch the PR's current head and report whether it still matches *expected_head*.

    An initial head check (or an existing-approval lookup) can be followed
    by the PR head moving before an approval outcome is reported: GitHub can
    attach a review to a commit that is no longer the PR's current head, so
    a final re-check closes that check/use race before success is reported.

    Args:
        pr_number: The pull request number.
        repo: ``owner/repo`` string.
        expected_head: The full 40-character ``headRefOid`` the approval
            (existing or freshly submitted) was recorded against.

    Returns:
        A tuple of ``(still_current, current_head, error_message)``.
        ``still_current`` is ``True`` only when the current head could be
        fetched and matches *expected_head*. ``current_head`` is the fetched
        SHA, or ``None`` if the fetch failed. ``error_message`` carries the
        fetch failure detail, or ``""`` when the fetch succeeded.
    """
    env_kwargs: dict[str, Any] = {"env": env} if env is not None else {}
    current_head, head_error = _fetch_current_head_sha(pr_number, repo, **env_kwargs)
    if current_head is None:
        return False, None, head_error
    return current_head == expected_head, current_head, ""


def _verify_approval(
    pr_number: int,
    repo: str,
    user_login: str,
    expected_head: str | None = None,
    max_retries: int = 2,
    retry_delay: float = 5.0,
    env: dict[str, str] | None = None,
) -> tuple[dict | None, int, bool]:
    """Verify the approval was registered by querying the reviews API.

    Fetches all reviews for the PR, considers ``APPROVED`` and
    ``CHANGES_REQUESTED`` reviews by *user_login* (case-insensitive), and
    returns the latest review only when its state is ``APPROVED``.

    Args:
        pr_number: The pull request number.
        repo: ``owner/repo`` string.
        user_login: Expected approver login.
        expected_head: Optional full 40-character ``headRefOid``. When
            provided, only approvals recorded for that commit verify.
        max_retries: Number of additional verification attempts after
            the first failure (default 2, so 3 total attempts).
        retry_delay: Seconds to wait between retries.

    Returns:
        A tuple of ``(review_dict, retries_used, lookup_ok)``. *review_dict*
        is ``{"id": <int>, "submitted_at": <str>}`` if a matching review is
        found, or ``None`` after all attempts are exhausted. *retries_used*
        is the number of retry attempts performed (0 if matched on first
        attempt). *lookup_ok* is ``True`` when the final attempt reached the
        reviews API and got a well-formed response (so a ``None`` result can
        be trusted as a confirmed "no matching review"), and ``False`` when
        the final attempt failed outright (non-zero exit) or returned a
        response that could not be parsed at all, meaning a ``None`` result
        is inconclusive rather than a confirmed miss.
    """
    owner, repo_name = _validate_repo_format(repo)
    total_attempts = max_retries + 1
    lookup_ok = True

    for attempt in range(total_attempts):
        try:
            result = run_safe(
                [
                    "gh",
                    "api",
                    f"repos/{owner}/{repo_name}/pulls/{pr_number}/reviews",
                    "--paginate",
                    "--jq",
                    ".[]",
                ],
                capture_output=True,
                text=True,
                shell=False,
                timeout=_GH_COMMAND_TIMEOUT_SECONDS,
                env=env,
            )
        except subprocess.TimeoutExpired as exc:
            # A stalled `gh api` call must not block the detached approval
            # task (and `agdt-task-wait`) indefinitely: normalize it into the
            # same inconclusive-lookup shape as any other failed attempt so
            # the retry/reporting logic below handles it uniformly.
            result = subprocess.CompletedProcess(
                args=exc.cmd if exc.cmd is not None else [],
                returncode=1,
                stdout="",
                stderr=f"gh api timed out after {exc.timeout}s",
            )

        parse_errors = 0
        last_parse_error = ""
        reviews: list[dict] = []
        matching: list[dict] = []

        if result.returncode == 0 and result.stdout.strip():
            for line in result.stdout.strip().splitlines():
                line = line.strip()
                if line:
                    try:
                        reviews.append(json.loads(line))
                    except (json.JSONDecodeError, TypeError) as exc:
                        parse_errors += 1
                        last_parse_error = str(exc)

            # Select the latest decisive review by the current user
            # (case-insensitive). A later changes-requested review supersedes
            # an earlier approval for the same head.
            # Guard against user: null from the API by coercing falsey values
            # to an empty dict before reading the login field.
            decisive = [
                r
                for r in reviews
                if (
                    isinstance(r, dict)
                    and isinstance(r.get("user"), dict)
                    and isinstance(r["user"].get("login"), str)
                    and r["user"]["login"].lower() == user_login.lower()
                    and r.get("state") in {"APPROVED", "CHANGES_REQUESTED"}
                    and (expected_head is None or r.get("commit_id") == expected_head)
                )
            ]

            # Sort by submitted_at descending. Coerce non-string / null values
            # to "" so the sort key is always comparable.
            decisive.sort(
                key=lambda r: r.get("submitted_at") if isinstance(r.get("submitted_at"), str) else "",  # type: ignore[arg-type, return-value]
                reverse=True,
            )
            latest = decisive[0] if decisive else None
            matching[:] = [latest] if latest and latest.get("state") == "APPROVED" else []

            if matching and parse_errors == 0:
                latest_match = matching[0]
                latest_id = latest_match.get("id")
                latest_submitted_at = latest_match.get("submitted_at")
                if isinstance(latest_id, int) and isinstance(latest_submitted_at, str):
                    return (
                        {"id": latest_id, "submitted_at": latest_submitted_at},
                        attempt,
                        True,
                    )

        # Build a diagnostic reason for the failure, and track whether this
        # attempt reached the API and got a well-formed (if inconclusive)
        # response. A hard API failure, or a response so malformed it could
        # not be parsed at all, or a "match" whose fields are unusable means
        # we cannot trust a `None` result as a confirmed absence of an
        # existing review — the caller must treat that as a lookup failure
        # rather than "no matching review".
        if result.returncode != 0:
            last_error = (result.stderr or result.stdout).strip()
            if not last_error:
                last_error = f"gh api exited with code {result.returncode}"
            lookup_ok = False
        elif not result.stdout.strip():
            last_error = "empty API response"
            lookup_ok = True
        elif parse_errors > 0:
            if not reviews:
                last_error = f"all {parse_errors} NDJSON line(s) failed JSON parsing (last error: {last_parse_error})"
            elif matching:
                last_error = f"{parse_errors} NDJSON line(s) failed parsing; refusing to reuse matching approval"
            else:
                parts = ["no matching APPROVED review found"]
                if expected_head is not None:
                    parts.append(f"for commit {expected_head}")
                parts.append(f"{parse_errors} NDJSON line(s) failed parsing")
                last_error = "; ".join(parts)
            lookup_ok = False
        elif matching:
            last_error = (
                f"{len(matching)} matching APPROVED review(s) found but "
                f"with invalid fields (non-int id or non-str submitted_at)"
            )
            lookup_ok = False
        else:
            last_error = "no matching APPROVED review found"
            if expected_head is not None:
                last_error += f" for commit {expected_head}"
            lookup_ok = True

        # If not the last attempt, retry
        if attempt < total_attempts - 1:
            print(
                f"Verification attempt {attempt + 1}/{total_attempts} failed "
                f"({last_error}); retrying in {retry_delay}s...",
                file=sys.stderr,
            )
            time.sleep(retry_delay)

    return None, max_retries, lookup_ok


def _find_existing_approval(
    pr_number: int,
    repo: str,
    user_login: str,
    expected_head: str,
    env: dict[str, str] | None = None,
) -> tuple[dict | None, bool]:
    """Return an existing approval on the target head for this approver, if any.

    Returns:
        A tuple of ``(review_or_none, lookup_ok)``. ``lookup_ok`` is
        ``False`` when the preflight lookup itself failed (API error or
        unparseable response), meaning ``review_or_none`` being ``None``
        cannot be trusted as a confirmed "no existing approval" — callers
        must not treat that as license to submit a new review, since the
        lookup was inconclusive rather than a genuine miss.
    """
    env_kwargs: dict[str, Any] = {"env": env} if env is not None else {}
    review, _, lookup_ok = _verify_approval(
        pr_number,
        repo,
        user_login,
        expected_head=expected_head,
        max_retries=0,
        retry_delay=0.0,
        **env_kwargs,
    )
    return review, lookup_ok


def approve_pr(
    pr_number: int,
    repo: str,
    body: str | None = None,
    expected_head: str | None = None,
    persist_state: bool = True,
    env: dict[str, str] | None = None,
) -> dict:
    """Approve a GitHub PR with verification and retry.

    Args:
        pr_number: The pull request number.
        repo: ``owner/repo`` string.
        body: Optional approval comment body. Defaults to
            :data:`_DEFAULT_APPROVAL_BODY`.
        expected_head: Optional full 40-character ``headRefOid``. When
            provided, the current PR head is fetched and compared against it
            before any review is submitted (refusing a stale head with a
            ``stale_head``/``head_check_failed`` result), and the approval is
            then submitted and verified against that exact PR head SHA.
            Before submitting, an existing ``APPROVED`` review by the same
            approver (for the same commit when ``expected_head`` is set) is
            reused via an idempotent ``already_approved`` result rather than
            creating a duplicate review, so retries and reruns are safe. If
            that preflight lookup itself fails or returns an unparseable
            response, submission is refused with a ``lookup_failed`` result
            rather than risking a duplicate approval on a transient read
            failure. Finally, the PR head is re-checked immediately before
            reporting success — for both the reused-approval path and the
            freshly-submitted path — and a ``stale_head`` result is returned
            instead if the head moved during the check/use window.
        persist_state: When ``True`` (default), writes
            ``github.pr_approval_verified``/``github.pr_approval_review_id``
            to shared agent state for downstream single-invocation callers
            (e.g. ``agdt-gh-pr-approve``). Callers that snapshot and consume
            the returned result directly — such as concurrent background
            approval tasks — should pass ``False`` to avoid two tasks for
            different pull requests overwriting each other's shared state.
        env: Optional subprocess environment for ``gh`` commands.

    Returns:
        Structured result dict with approval details.

    Raises:
        ValueError: When ``expected_head`` is not a full 40-character
            lowercase hexadecimal SHA.
    """
    if body is None:
        body = _DEFAULT_APPROVAL_BODY
    if expected_head is not None and _SHA40_RE.fullmatch(expected_head) is None:
        raise ValueError(
            f"Invalid expected_head {expected_head!r}: "
            "must be exactly 40 lowercase hexadecimal characters (a full headRefOid)."
        )

    # Normalize repo once so both _submit_approval and _verify_approval
    # use the same cleaned value (strip whitespace, drop trailing .git,
    # validate owner/repo format).
    owner, repo_name = _validate_repo_format(repo)
    repo = f"{owner}/{repo_name}"

    _check_gh_available()
    env_kwargs: dict[str, Any] = {"env": env} if env is not None else {}
    user_login = _resolve_current_user(**env_kwargs)

    if expected_head is not None:
        current_head, head_error = _fetch_current_head_sha(pr_number, repo, **env_kwargs)
        if current_head is None:
            result = {
                "prNumber": pr_number,
                "repo": repo,
                "approved": False,
                "error": "head_check_failed",
                "message": f"Could not determine the current PR head; refusing to approve: {head_error}",
                "reviewId": None,
                "approver": user_login,
                "submittedAt": None,
                "verified": False,
                "retries": 0,
            }
            if persist_state:
                set_value("github.pr_approval_verified", False)
                set_value("github.pr_approval_review_id", None)
            return result
        if current_head != expected_head:
            result = {
                "prNumber": pr_number,
                "repo": repo,
                "approved": False,
                "error": "stale_head",
                "message": f"PR head is {current_head}, expected {expected_head}; refusing to approve a stale commit.",
                "reviewId": None,
                "approver": user_login,
                "submittedAt": None,
                "verified": False,
                "retries": 0,
            }
            if persist_state:
                set_value("github.pr_approval_verified", False)
                set_value("github.pr_approval_review_id", None)
            return result
        existing_review, lookup_ok = _find_existing_approval(pr_number, repo, user_login, expected_head, **env_kwargs)
        if existing_review is not None:
            still_current, post_check_head, recheck_error = _confirm_head_unchanged(
                pr_number, repo, expected_head, **env_kwargs
            )
            if not still_current:
                result = {
                    "prNumber": pr_number,
                    "repo": repo,
                    "approved": False,
                    "error": "stale_head",
                    "message": (
                        f"PR head is now {post_check_head or f'unknown ({recheck_error})'}, expected "
                        f"{expected_head}; the existing approval was recorded for a commit that is no "
                        "longer the PR's current head."
                    ),
                    "reviewId": existing_review["id"],
                    "approver": user_login,
                    "submittedAt": existing_review["submitted_at"],
                    "verified": False,
                    "retries": 0,
                }
                if persist_state:
                    set_value("github.pr_approval_verified", False)
                    set_value("github.pr_approval_review_id", None)
                return result
            result = {
                "prNumber": pr_number,
                "repo": repo,
                "approved": True,
                "status": "already_approved",
                "reviewId": existing_review["id"],
                "approver": user_login,
                "submittedAt": existing_review["submitted_at"],
                "verified": True,
                "retries": 0,
            }
            if persist_state:
                set_value("github.pr_approval_verified", True)
                set_value("github.pr_approval_review_id", existing_review["id"])
            return result
        if not lookup_ok:
            # A failed/inconclusive preflight lookup is indistinguishable from a
            # genuine "no existing approval" unless we track it explicitly. Treating
            # it as a miss would risk submitting a duplicate review on a transient
            # read failure, contrary to #4025's idempotency requirement — so abort
            # instead of falling through to submission.
            result = {
                "prNumber": pr_number,
                "repo": repo,
                "approved": False,
                "error": "lookup_failed",
                "message": (
                    "Could not reliably determine whether an approval already exists "
                    f"for {expected_head}; refusing to submit a new review to avoid "
                    "creating a duplicate approval."
                ),
                "reviewId": None,
                "approver": user_login,
                "submittedAt": None,
                "verified": False,
                "retries": 0,
            }
            if persist_state:
                set_value("github.pr_approval_verified", False)
                set_value("github.pr_approval_review_id", None)
            return result

    success, error_msg = _submit_approval(pr_number, repo, body, expected_head, **env_kwargs)

    if not success:
        result = {
            "prNumber": pr_number,
            "repo": repo,
            "approved": False,
            "error": "approval_failed",
            "message": error_msg,
            "reviewId": None,
            "approver": user_login,
            "submittedAt": None,
            "verified": False,
            "retries": 0,
        }
        if persist_state:
            set_value("github.pr_approval_verified", False)
            set_value("github.pr_approval_review_id", None)
        return result

    review, retries_used, _ = _verify_approval(
        pr_number,
        repo,
        user_login,
        expected_head=expected_head,
        **env_kwargs,
    )

    if review is not None and expected_head is not None:
        still_current, post_check_head, recheck_error = _confirm_head_unchanged(
            pr_number, repo, expected_head, **env_kwargs
        )
        if not still_current:
            result = {
                "prNumber": pr_number,
                "repo": repo,
                "approved": False,
                "error": "stale_head",
                "message": (
                    f"PR head is now {post_check_head or f'unknown ({recheck_error})'}, expected "
                    f"{expected_head}; the submitted approval was recorded for a commit that is no "
                    "longer the PR's current head."
                ),
                "reviewId": review["id"],
                "approver": user_login,
                "submittedAt": review["submitted_at"],
                "verified": False,
                "retries": retries_used,
            }
            if persist_state:
                set_value("github.pr_approval_verified", False)
                set_value("github.pr_approval_review_id", None)
            return result

    if review is not None:
        result = {
            "prNumber": pr_number,
            "repo": repo,
            "approved": True,
            "reviewId": review["id"],
            "approver": user_login,
            "submittedAt": review["submitted_at"],
            "verified": True,
            "retries": retries_used,
        }
    else:
        result = {
            "prNumber": pr_number,
            "repo": repo,
            "approved": True,
            "reviewId": None,
            "approver": user_login,
            "submittedAt": None,
            "verified": False,
            "retries": retries_used,
        }

    if persist_state:
        set_value("github.pr_approval_verified", result["verified"])
        set_value("github.pr_approval_review_id", result["reviewId"])
    return result


def pr_approve_command() -> None:
    """CLI entry point for ``agdt-gh-pr-approve``."""
    parser = argparse.ArgumentParser(
        description="Approve a GitHub PR with verification and retry.",
    )
    parser.add_argument("--pr", type=int, default=None, help="PR number")
    parser.add_argument("--repo", type=str, default=None, help="GitHub repo (owner/repo)")
    parser.add_argument("--body", type=str, default=None, help="Approval comment body")
    parser.add_argument(
        "--expected-head",
        type=str,
        default=None,
        dest="expected_head",
        help=(
            "Expected full headRefOid of the PR. When provided, approval is "
            "submitted and verified against that exact commit."
        ),
    )
    args = parser.parse_args()
    if args.expected_head is not None and _SHA40_RE.fullmatch(args.expected_head) is None:
        error_message = (
            "argument --expected-head: must be exactly 40 lowercase hexadecimal characters (a full headRefOid)"
        )
        parser.error(error_message)

    # Resolve PR number
    pr_number = args.pr
    if pr_number is None:
        state_pr = get_value("github.pull_request_number")
        if state_pr is not None:
            try:
                pr_number = int(state_pr)
            except ValueError, TypeError:
                print(
                    f"Error: github.pull_request_number in state must be an integer; "
                    f"got {state_pr!r}. Fix with: agdt-set github.pull_request_number 123",
                    file=sys.stderr,
                )
                sys.exit(1)

    if pr_number is None:
        print(
            "Error: PR number is required. Provide --pr or set github.pull_request_number in state.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Resolve repo
    repo = resolve_github_repo(args.repo)

    result = approve_pr(pr_number, repo, args.body, args.expected_head)
    print(json.dumps(result, indent=2))
