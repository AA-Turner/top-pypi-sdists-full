"""Commit node: stage, rebase, commit, and push inside the issue worktree.

This node replaces the legacy subprocess-based ``agdt-git-save-work`` invocation
with direct git primitive calls so that:

- Every git operation runs in the issue worktree (``cwd=setup_result.worktree_path``)
  rather than the process CWD, which stays on the main checkout.
- Failures are returned as structured ``CommitResult`` with an embedded
  ``BlockedState`` rather than raising — LangGraph routing inspects the result
  to decide the next node.
- Smart amend detection re-uses :func:`~agentic_devtools.cli.git.operations.branch_has_commits_ahead_of_main`
  (the shared CWD-aware implementation) to avoid diverging logic.
- Stash-identity tracking (T043): the stash created before rebase is tagged with a
  unique token, resolved back to an exact stash commit SHA, restored by that SHA,
  and dropped only after ref re-verification so an unrelated concurrent stash cannot
  be consumed.

Fails fast when ``issue_key`` is missing so a corrupted/resumed checkpoint cannot
generate an invalid ``feat():`` commit.  When ``setup_result.worktree_path`` is
blank the node returns ``context_mismatch`` before any git command runs.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any
from uuid import uuid4

from agentic_devtools.cli.git.branch_naming import normalize_issue_key
from agentic_devtools.cli.git.core import GitError, run_git_capture, run_git_safe
from agentic_devtools.cli.git.operations import should_amend_instead_of_commit, stage_changes
from agentic_devtools.models.git_results import BlockedState, CommitResult, SetupResult
from agentic_devtools.orchestration.nodes._helpers import utc_now

# Push rejection patterns for classification.
_PROTECTION_PATTERNS = re.compile(r"protected branch|pre-receive hook declined|GH006|GH013", re.IGNORECASE)
_AUTH_PATTERNS = re.compile(
    r"authentication failed|permission denied|could not read Username"
    r"|remote: Repository not found|The requested URL returned error: 403",
    re.IGNORECASE,
)
_NON_FAST_FORWARD_PATTERNS = re.compile(r"non-fast-forward|rejected.*update|! \[rejected\]", re.IGNORECASE)

# Conventional commit types inferred from issue key prefix.
_JIRA_KEY_PATTERN = re.compile(r"^[A-Z][A-Z0-9]+-\d+$", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Internal helpers – probe
# ---------------------------------------------------------------------------


def _has_pending_changes(cwd: str | None) -> bool:
    """Return ``True`` when the worktree has unstaged/untracked changes."""
    result = run_git_capture(["status", "--porcelain"], cwd=cwd)
    return bool(result.stdout.strip())


def _has_staged_changes(cwd: str | None) -> bool:
    """Return ``True`` when there is at least one file in the index (staged).

    Raises:
        GitError: When ``git diff --cached --quiet`` exits with a code above ``1``,
            which signals an error (e.g. a corrupt index) rather than merely a
            "no differences" / "has differences" result.
    """
    result = run_git_capture(["diff", "--cached", "--quiet"], cwd=cwd)
    # exit code 0 → nothing staged; 1 → staged changes present; >1 → error.
    if result.returncode > 1:
        raise GitError(
            result.returncode,
            f"git diff --cached --quiet exited with code {result.returncode}: {result.stderr.strip()}",
            ["diff", "--cached", "--quiet"],
        )
    return result.returncode == 1


def _conflicting_files(cwd: str | None) -> list[str]:
    """Return the list of files with merge/rebase conflicts."""
    result = run_git_capture(["diff", "--name-only", "--diff-filter=U"], cwd=cwd)
    return [f for f in result.stdout.splitlines() if f.strip()]


# ---------------------------------------------------------------------------
# Internal helpers – stash identity (T043)
# ---------------------------------------------------------------------------


def _find_stash_commit(stash_token: str | None, cwd: str | None) -> str | None:
    """Return the stash commit SHA for the entry whose message ends with *stash_token*.

    A unique per-invocation token lets the caller identify the stash created by
    this workflow run without relying on the mutable ``stash@{0}`` index, which
    can shift if another process pushes a stash concurrently.
    """
    if stash_token is None:
        return None
    result = run_git_capture(["stash", "list", "--format=%H%x00%gs"], cwd=cwd)
    if result.returncode != 0:
        return None
    for line in result.stdout.splitlines():
        stash_sha, separator, subject = line.partition("\x00")
        if separator and subject.strip().endswith(stash_token):
            return stash_sha.strip() or None
    return None


def _drop_stash_by_commit(stash_sha: str | None, cwd: str | None) -> bool:
    """Drop the stash entry whose current ref still resolves to *stash_sha*.

    The helper maps the immutable stash commit SHA back to the current
    ``stash@{N}`` ref, re-verifies that the ref still points at the same SHA,
    then drops it.  Returns ``True`` on success, ``False`` when the stash
    cannot be identified or the ref no longer resolves to the expected SHA.

    The caller treats a ``False`` return as **best-effort** — the stash is
    safely retained in place rather than risking an identity-shifted drop that
    would remove an unrelated stash entry created by a concurrent process.
    """
    if stash_sha is None:
        return False
    result = run_git_capture(["stash", "list", "--format=%H%x00%gd"], cwd=cwd)
    if result.returncode != 0:
        return False
    for line in result.stdout.splitlines():
        listed_sha, separator, stash_ref = line.partition("\x00")
        if not separator or listed_sha.strip() != stash_sha:
            continue
        verified = run_git_capture(["rev-parse", stash_ref.strip()], cwd=cwd)
        if verified.returncode != 0 or verified.stdout.strip() != stash_sha:
            return False
        drop_result = run_git_capture(["stash", "drop", stash_ref.strip()], cwd=cwd)
        return drop_result.returncode == 0
    return False


# ---------------------------------------------------------------------------
# Internal helpers – repository ownership
# ---------------------------------------------------------------------------


def _validate_worktree_ownership(cwd: str) -> BlockedState | None:
    """Verify that *cwd* belongs to the same git repository as the caller process.

    Compares ``git rev-parse --git-common-dir`` executed in *cwd* against the
    same command run in the process's working directory (the main checkout).  A
    mismatch means the directory was replaced by an unrelated repository after
    setup was recorded in the checkpoint, which would cause this node to stage,
    commit, and push the wrong codebase.

    Returns ``None`` when ownership is confirmed, or a ``context_mismatch``
    :class:`~agentic_devtools.models.git_results.BlockedState` on any failure.
    """
    try:
        proc_result = run_git_capture(["rev-parse", "--git-common-dir"])
    except GitError as exc:
        return BlockedState(
            category="context_mismatch",
            message=(
                f"Cannot determine repository identity: 'git rev-parse --git-common-dir' failed in process CWD ({exc})"
            ),
        )
    if proc_result.returncode != 0:
        return BlockedState(
            category="context_mismatch",
            message=("Cannot determine repository identity: 'git rev-parse --git-common-dir' failed in process CWD"),
        )
    expected_common_dir = str(Path(proc_result.stdout.strip()).resolve())

    try:
        wt_result = run_git_capture(["rev-parse", "--git-common-dir"], cwd=cwd)
    except GitError as exc:
        return BlockedState(
            category="context_mismatch",
            message=(
                f"Cannot verify repository identity at {cwd!r}: 'git rev-parse --git-common-dir' could not run ({exc})"
            ),
        )
    if wt_result.returncode != 0:
        return BlockedState(
            category="context_mismatch",
            message=(
                f"Cannot verify repository identity at {cwd!r}: "
                "'git rev-parse --git-common-dir' failed — the path may not be inside a git repository"
            ),
        )
    wt_common_dir = str(Path(wt_result.stdout.strip()).resolve())

    if wt_common_dir != expected_common_dir:
        return BlockedState(
            category="context_mismatch",
            message=(
                f"Worktree at {cwd!r} belongs to a different repository "
                f"(git-common-dir: {wt_common_dir!r} != expected: {expected_common_dir!r}); "
                "refusing to stage/commit in a foreign repository"
            ),
        )
    return None


# ---------------------------------------------------------------------------
# Internal helpers – fetch and rebase
# ---------------------------------------------------------------------------


def _head_is_issue_commit(commit_msg: str, issue_key: str) -> bool:
    """Return ``True`` when *commit_msg* contains an exact conventional-commit reference to *issue_key*.

    Matches the conventional-commit scope ``(#key)`` / ``(key)`` **or** the
    footer token ``#key`` / ``key`` as a whole word.  The precise word-boundary
    test prevents false positives from version strings, line counts, or any
    other literal that shares digits or characters with the issue identifier.

    *issue_key* must already be normalized (no leading ``#``).
    """
    escaped = re.escape(issue_key)
    if issue_key.isdigit():
        # GitHub numeric key: scope (#42) or standalone footer token #42
        scope_pat = re.compile(rf"\(#{escaped}\)")
        footer_pat = re.compile(rf"(?<![A-Za-z0-9_])#{escaped}(?![A-Za-z0-9_])")
    else:
        # Jira key: scope (PROJECT-1234) or standalone footer token PROJECT-1234
        scope_pat = re.compile(rf"\({escaped}\)", re.IGNORECASE)
        footer_pat = re.compile(rf"(?<![A-Za-z0-9_\-]){escaped}(?![A-Za-z0-9_\-])", re.IGNORECASE)
    return bool(scope_pat.search(commit_msg)) or bool(footer_pat.search(commit_msg))


def _fetch_and_rebase(
    cwd: str | None,
    skip_rebase: bool,
    *,
    issue_key: str | None = None,
) -> tuple[bool, BlockedState | None]:
    """Fetch origin and optionally rebase the worktree branch onto origin/main.

    Returns a ``(origin_main_fresh, blocked)`` tuple.  ``origin_main_fresh`` is
    ``True`` when the fetch succeeded.  ``blocked`` is ``None`` on success or a
    :class:`~agentic_devtools.models.git_results.BlockedState` on fetch/rebase/stash
    failure.

    When the fetch fails, amend detection would fall back to local ``main``.  If
    local main lags ``origin/main``, upstream-only commits are counted as "ahead"
    and a fresh issue branch can be incorrectly amended (rewriting an upstream
    commit).  To avoid this, the function probes HEAD's commit message when the
    fetch fails; if the message does not contain *issue_key* the function returns a
    transient :class:`~agentic_devtools.models.git_results.BlockedState` instead of
    proceeding.  Pass ``issue_key`` to enable this guard.
    """
    # Step 1: fetch origin.
    fresh = True
    try:
        run_git_safe(["fetch", "origin"], cwd=cwd)
    except GitError as exc:
        fresh = False
        # Amend detection falls back to local ``main`` when the fetch is stale.
        # If local main lags origin/main, upstream commits are counted as
        # "ahead", causing a fresh issue branch to incorrectly execute
        # ``--amend`` and rewrite an upstream commit.  Guard: only proceed when
        # HEAD's commit message contains the issue key — that proves the branch
        # already has a prior issue commit, making amend safe.  Without that
        # proof, fail closed.
        last_msg_result = run_git_capture(["log", "-1", "--format=%B"], cwd=cwd)
        head_is_issue_commit = (
            issue_key is not None
            and last_msg_result.returncode == 0
            and _head_is_issue_commit(last_msg_result.stdout, issue_key)
        )
        if not head_is_issue_commit:
            return False, BlockedState(
                category="transient",
                message=(
                    "Fetch from origin failed and HEAD is not a confirmed prior issue commit; "
                    "refusing amend detection against potentially stale refs to avoid rewriting "
                    f"an upstream commit: {exc}"
                ),
            )

    if skip_rebase or not fresh:
        return fresh, None

    # Step 2: check whether origin/main exists.
    verify = run_git_capture(["rev-parse", "--verify", "origin/main"], cwd=cwd)
    if verify.returncode != 0:
        return fresh, None

    # Step 3: stash pending changes if any.
    stash_sha: str | None = None
    has_pending = _has_pending_changes(cwd)
    if has_pending:
        stash_token = f"agdt-rebase-stash:{uuid4().hex}"
        try:
            run_git_safe(["stash", "push", "--include-untracked", "-m", stash_token], cwd=cwd)
            stash_sha = _find_stash_commit(stash_token, cwd)
        except GitError as exc:
            return fresh, BlockedState(category="transient", message=f"Stashing pending changes failed: {exc}")

    # Step 4: rebase.
    rebase_result = run_git_capture(["rebase", "origin/main"], cwd=cwd)
    if rebase_result.returncode != 0:
        # Rebase failed — abort, then pop the stash only when abort succeeded.
        conflicting = _conflicting_files(cwd)
        abort_result = run_git_capture(["rebase", "--abort"], cwd=cwd)
        if abort_result.returncode != 0:
            # Abort failed — do NOT attempt stash restore into a broken rebase state.
            return fresh, BlockedState(
                category="corruption",
                message=(
                    f"Rebase onto origin/main produced conflicts and the abort also failed: "
                    f"{abort_result.stderr.strip()}.  "
                    f"Stash retained (SHA={stash_sha or 'unknown'}); manual recovery required."
                ),
                details=conflicting,
            )
        if has_pending:
            if stash_sha is None:
                return fresh, BlockedState(
                    category="transient",
                    message=(
                        "Rebase conflict aborted successfully but the stash identity could not be resolved; "
                        "stashed changes were not restored. Manual stash recovery is required."
                    ),
                    details=conflicting,
                )
            apply_result = run_git_capture(["stash", "apply", "--index", stash_sha], cwd=cwd)
            if apply_result.returncode != 0:
                return fresh, BlockedState(
                    category="transient",
                    message=(
                        f"Rebase conflict aborted successfully but restoring stashed changes failed: "
                        f"{apply_result.stderr.strip()}.  "
                        f"Stash retained (SHA={stash_sha})."
                    ),
                    details=conflicting,
                )
            # Best-effort drop: if the ref shifted due to a concurrent stash
            # push the entry is safely left in place rather than risking
            # removing an unrelated stash.
            _drop_stash_by_commit(stash_sha, cwd)
        return fresh, BlockedState(
            category="conflict",
            message="Rebase onto origin/main produced conflicts.",
            details=conflicting,
        )

    # Step 5: restore stash (rebase succeeded).
    if has_pending:
        if stash_sha is None:
            # The stash SHA cannot be resolved — block rather than popping an
            # unrelated stash entry that may have been pushed concurrently.
            return fresh, BlockedState(
                category="transient",
                message=(
                    "Rebase succeeded but the stash SHA could not be resolved; stashed changes were not restored."
                ),
            )
        apply_result = run_git_capture(["stash", "apply", "--index", stash_sha], cwd=cwd)
        if apply_result.returncode != 0:
            # Restore failed after a successful rebase — do NOT abort the rebase.
            return fresh, BlockedState(
                category="conflict",
                message=(
                    f"Rebase succeeded but restoring stashed changes failed: "
                    f"{apply_result.stderr.strip()}.  "
                    f"Stash retained (SHA={stash_sha}); manual recovery required."
                ),
            )
        # Best-effort drop: if the ref shifted due to a concurrent stash push
        # the entry is safely left in place rather than risking removing an
        # unrelated stash.
        _drop_stash_by_commit(stash_sha, cwd)

    return fresh, None


def _commit_result_field(result: Any, field: str) -> Any:
    """Return *field* from either a CommitResult-like object or a checkpoint dict."""
    if isinstance(result, dict):
        return result.get(field)
    return getattr(result, field, None)


def _retry_unpublished_push(previous_result: Any, cwd: str | None) -> CommitResult | None:
    """Retry publishing an existing local HEAD when the prior commit was not pushed."""
    if previous_result is None:
        return None
    previous_error = _commit_result_field(previous_result, "error")
    previous_sha = _commit_result_field(previous_result, "commit_sha")
    if (
        previous_error is None
        or _commit_result_field(previous_result, "push_succeeded") is True
        or _commit_result_field(previous_result, "no_op") is True
    ):
        return None
    # Prior blocked result has an error but no recorded SHA — the commit may never
    # have been created or SHA read-back failed.  Preserve the blocked state so
    # the caller does not silently fall through to no_op=True and skip the push.
    if not isinstance(previous_sha, str) or not previous_sha.strip():
        return CommitResult(
            push_succeeded=False,
            error=BlockedState(
                category="transient",
                message=(
                    "Prior commit blocked with no recorded SHA; cannot identify a local "
                    "commit to retry. "
                    f"Original error: {getattr(previous_error, 'message', str(previous_error))}"
                ),
            ),
        )
    head_sha_result = run_git_capture(["rev-parse", "--short", "HEAD"], cwd=cwd)
    if head_sha_result.returncode != 0 or not head_sha_result.stdout.strip():
        # Cannot confirm which commit is at HEAD — return a structured block so the
        # caller does not silently fall through to the no-op path and skip the push.
        return CommitResult(
            commit_sha=previous_sha.strip(),
            commit_message_title=_commit_result_field(previous_result, "commit_message_title"),
            is_amend=bool(_commit_result_field(previous_result, "is_amend")),
            push_succeeded=False,
            error=BlockedState(
                category="transient",
                message=(
                    "HEAD SHA probe failed during push retry; cannot confirm local commit identity. "
                    f"Prior commit SHA: {previous_sha.strip()!r}"
                ),
            ),
        )
    head_short = head_sha_result.stdout.strip()
    branch = run_git_capture(["rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd).stdout.strip()
    head_full = run_git_capture(["rev-parse", "HEAD"], cwd=cwd).stdout.strip()
    remote = run_git_capture(["ls-remote", "--heads", "origin", branch], cwd=cwd)
    remote_sha = remote.stdout.split()[0] if remote.returncode == 0 and remote.stdout.strip() else ""
    if head_short != previous_sha.strip():
        if remote_sha == head_full and head_full:
            return None
        return CommitResult(
            commit_sha=head_short,
            commit_message_title=_commit_result_field(previous_result, "commit_message_title"),
            is_amend=bool(_commit_result_field(previous_result, "is_amend")),
            push_succeeded=False,
            error=BlockedState(
                category="transient",
                message=(
                    "Prior unpublished commit SHA "
                    f"{previous_sha.strip()!r} no longer matches HEAD {head_short!r}, "
                    "and origin does not yet contain the current HEAD."
                ),
            ),
        )
    if remote_sha == head_full:
        return None
    push_blocked = _push(cwd, is_amend=bool(_commit_result_field(previous_result, "is_amend")))
    if push_blocked is not None:
        return CommitResult(
            commit_sha=previous_sha.strip(),
            commit_message_title=_commit_result_field(previous_result, "commit_message_title"),
            is_amend=bool(_commit_result_field(previous_result, "is_amend")),
            push_succeeded=False,
            error=push_blocked,
        )
    return CommitResult(
        commit_sha=previous_sha.strip(),
        commit_message_title=_commit_result_field(previous_result, "commit_message_title"),
        is_amend=bool(_commit_result_field(previous_result, "is_amend")),
        push_succeeded=True,
    )


# ---------------------------------------------------------------------------
# Internal helpers – push
# ---------------------------------------------------------------------------


def _classify_push_failure(stderr: str) -> BlockedState:
    """Classify a push rejection into a :class:`~agentic_devtools.models.git_results.BlockedState`."""
    if _PROTECTION_PATTERNS.search(stderr):
        return BlockedState(category="protection", message=f"Push rejected by branch protection: {stderr}")
    if _AUTH_PATTERNS.search(stderr):
        return BlockedState(category="auth", message=f"Push rejected due to auth failure: {stderr}")
    if _NON_FAST_FORWARD_PATTERNS.search(stderr):
        return BlockedState(category="conflict", message=f"Push rejected (non-fast-forward): {stderr}")
    return BlockedState(category="transient", message=f"Push rejected (unknown): {stderr}")


def _push(cwd: str | None, *, is_amend: bool) -> BlockedState | None:
    """Push the current branch to origin.

    Returns ``None`` on success or a :class:`~agentic_devtools.models.git_results.BlockedState`
    on rejection.
    """
    branch_result = run_git_capture(["rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd)
    branch = branch_result.stdout.strip()

    if is_amend:
        push_args = ["push", "--force-with-lease", "origin", branch]
    else:
        push_args = ["push", "--set-upstream", "origin", branch]

    result = run_git_capture(push_args, cwd=cwd)
    if result.returncode != 0:
        return _classify_push_failure(result.stderr)
    return None


# ---------------------------------------------------------------------------
# Internal helpers – commit message
# ---------------------------------------------------------------------------


def _generate_commit_message(
    issue_key: str,
    plan: Any,
    issue_data: Any,
    *,
    issue_provider: Any = None,
) -> str:
    """Build a conventional commit message for *issue_key*.

    Args:
        issue_key: Normalized issue key (e.g. ``"42"`` or ``"PROJECT-1234"``).
        plan: Optional plan text; its first non-empty line becomes the summary
            when no issue summary is available.
        issue_data: Issue data dict; ``issue_data["summary"]`` is used as the
            commit summary when it is a non-empty string.
        issue_provider: Explicit provider override (``"github"`` or ``"jira"``).
            When omitted or invalid, the provider is inferred from *issue_key*.

    Returns:
        A conventional commit message string with a footer repeating the issue
        reference.
    """
    # Normalize plan to string.
    plan_str = plan if isinstance(plan, str) else ""

    # Determine provider.
    inferred_provider = "jira" if (isinstance(issue_key, str) and _JIRA_KEY_PATTERN.match(issue_key)) else "github"
    if isinstance(issue_provider, str):
        provider = issue_provider
    else:
        provider = inferred_provider

    # Determine summary.
    summary = ""
    if isinstance(issue_data, dict):
        raw_summary = issue_data.get("summary", "")
        if isinstance(raw_summary, str):
            summary = raw_summary.strip()

    if not summary:
        # Try first line of the plan (only the literal first line, not subsequent ones).
        first_line = plan_str.split("\n")[0].strip() if plan_str else ""
        if first_line:
            summary = first_line.lower()

    if not summary:
        summary = "implement autonomous workflow"

    # Truncate to keep first line ≤ 72 chars after the prefix.
    is_numeric_key = isinstance(issue_key, str) and issue_key.isdigit()
    if is_numeric_key:
        prefix = f"feat(#{issue_key}):"
        footer = f"#{issue_key}"
    elif provider == "jira":
        prefix = f"feat({issue_key}):"
        footer = f"[{issue_key}](https://jira.swica.ch/browse/{issue_key})"
    else:
        prefix = f"feat({issue_key}):"
        footer = issue_key

    max_summary_len = 72 - len(prefix) - 1  # 1 for the space
    if len(summary) > max_summary_len:
        summary = summary[:max_summary_len]

    title = f"{prefix} {summary}"

    return f"{title}\n\n{footer}"


# ---------------------------------------------------------------------------
# Defensive guard
# ---------------------------------------------------------------------------


def _blocked(result: CommitResult) -> CommitResult:
    """Assert that *result* has a non-``None`` error field and return it.

    Raises :exc:`ValueError` when called with a success result — this is a
    programming error that should never reach production.
    """
    if result.error is None:
        raise ValueError("_blocked called with a CommitResult that has non-None error=None; must supply non-None error")
    return result


# ---------------------------------------------------------------------------
# Public node
# ---------------------------------------------------------------------------


def commit_node(state: dict[str, Any]) -> dict[str, Any]:
    """Stage, rebase, commit, and push inside the issue worktree.

    Reads from *state*:
        - ``issue_key`` (required, non-blank string)
        - ``setup_result`` (required, :class:`~agentic_devtools.models.git_results.SetupResult`)
        - ``commit_message`` (optional str; used verbatim when provided; falls back to
          auto-generation from ``issue_key``, ``plan``, and ``issue_data`` when absent or blank)
        - ``dry_run`` (optional bool, default ``False``)
        - ``skip_rebase`` (optional bool, default ``False``)
        - ``plan`` (optional str)
        - ``issue_data`` (optional dict)
        - ``issue_provider`` (optional str)

    Returns a dict with:
        - ``commit_result``: :class:`~agentic_devtools.models.git_results.CommitResult`
        - ``error``: ``None`` on success, human-readable message on failure
        - ``events``: list with a single event dict
        - ``commit_created``: ``True`` when a commit was created/amended
    """
    now = utc_now()

    # --- validate issue_key ---------------------------------------------------
    raw_key = state.get("issue_key")
    if not isinstance(raw_key, str) or not raw_key.strip():
        err_result = CommitResult(
            error=BlockedState(
                category="context_mismatch",
                message="issue_key is required and must be a non-empty string",
            )
        )
        return {
            "commit_result": err_result,
            "error": "issue_key is required and must be a non-empty string",
            "events": [{"event": "commit_failed", "timestamp": now}],
            "commit_created": False,
        }

    try:
        issue_key = normalize_issue_key(raw_key)
    except ValueError:
        issue_key = ""

    if not issue_key:
        err_result = CommitResult(error=BlockedState(category="context_mismatch", message="empty normalized key"))
        return {
            "commit_result": err_result,
            "error": "issue_key must normalize to a non-empty issue identifier",
            "events": [{"event": "commit_failed", "timestamp": now}],
            "commit_created": False,
        }

    # --- validate worktree_path -----------------------------------------------
    setup_result: SetupResult | None = state.get("setup_result")
    worktree_path: str | None = getattr(setup_result, "worktree_path", None)
    if not worktree_path or not worktree_path.strip():
        err_result = CommitResult(
            error=BlockedState(
                category="context_mismatch",
                message="worktree_path is missing or blank; cannot run git ops without a valid worktree_path",
            )
        )
        return {
            "commit_result": err_result,
            "error": "worktree_path is missing or blank from setup_result; commit aborted",
            "events": [{"event": "commit_failed", "timestamp": now}],
            "commit_created": False,
        }

    cwd = worktree_path.strip()
    dry_run: bool = bool(state.get("dry_run", False))
    skip_rebase: bool = bool(state.get("skip_rebase", False))
    plan: str = state.get("plan") or ""
    issue_data: dict | None = state.get("issue_data")
    issue_provider: str | None = state.get("issue_provider")

    # --- dry run --------------------------------------------------------------
    if dry_run:
        return {
            "commit_result": CommitResult(no_op=True),
            "error": None,
            "events": [{"event": "commit_skipped_dry_run", "timestamp": now}],
            "commit_created": False,
        }

    # --- stage ----------------------------------------------------------------
    # Before staging, verify (1) that the worktree directory belongs to the
    # same repository (guards against a removed-worktree path that was replaced
    # by a foreign repo), and (2) that the worktree is still on the expected
    # branch (guards against an external checkout switching branches after
    # setup).  A missing expected_branch (None or blank) is treated as
    # context_mismatch because we cannot verify isolation and must not
    # stage/commit blind.
    ownership_error = _validate_worktree_ownership(cwd)
    if ownership_error is not None:
        return {
            "commit_result": CommitResult(error=ownership_error),
            "error": ownership_error.message,
            "events": [{"event": "commit_blocked_wrong_repo", "timestamp": now}],
            "commit_created": False,
        }

    expected_branch: str | None = getattr(setup_result, "branch_name", None)
    if not expected_branch:
        branch_error = BlockedState(
            category="context_mismatch",
            message=("setup_result.branch_name is not set; refusing to stage/commit on an unverified branch"),
        )
        return {
            "commit_result": CommitResult(error=branch_error),
            "error": branch_error.message,
            "events": [{"event": "commit_blocked_wrong_branch", "timestamp": now}],
            "commit_created": False,
        }
    try:
        current_branch_result = run_git_capture(["rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd)
    except GitError as exc:
        probe_error = BlockedState(
            category="transient",
            message=f"Branch probe failed (worktree may have disappeared): {exc}",
        )
        return {
            "commit_result": CommitResult(error=probe_error),
            "error": probe_error.message,
            "events": [{"event": "commit_blocked_worktree_disappeared", "timestamp": now}],
            "commit_created": False,
        }
    current_branch = current_branch_result.stdout.strip()
    if current_branch != expected_branch:
        branch_error = BlockedState(
            category="context_mismatch",
            message=(
                f"Worktree at {cwd!r} is on branch {current_branch!r} but setup expected "
                f"{expected_branch!r}; refusing to stage/commit on the wrong branch"
            ),
        )
        return {
            "commit_result": CommitResult(error=branch_error),
            "error": branch_error.message,
            "events": [{"event": "commit_blocked_wrong_branch", "timestamp": now}],
            "commit_created": False,
        }

    try:
        stage_changes(False, cwd=cwd)
    except GitError as exc:
        err_result = CommitResult(error=BlockedState(category="transient", message=f"Staging failed: {exc}"))
        return {
            "commit_result": err_result,
            "error": f"Staging failed: {exc}",
            "events": [{"event": "commit_failed", "timestamp": now}],
            "commit_created": False,
        }

    # --- nothing staged -------------------------------------------------------
    try:
        has_staged = _has_staged_changes(cwd)
    except GitError as exc:
        index_err_msg = f"Index check failed: {exc}"
        err_result = CommitResult(error=BlockedState(category="transient", message=index_err_msg))
        return {
            "commit_result": err_result,
            "error": index_err_msg,
            "events": [{"event": "commit_failed", "timestamp": now}],
            "commit_created": False,
        }
    if not has_staged:
        try:
            retried_push = _retry_unpublished_push(state.get("commit_result"), cwd)
        except GitError as exc:
            err_result = CommitResult(
                error=BlockedState(category="transient", message=f"Push retry probe failed: {exc}")
            )
            return {
                "commit_result": err_result,
                "error": f"Push retry probe failed: {exc}",
                "events": [{"event": "commit_failed", "timestamp": now}],
                "commit_created": False,
            }
        if retried_push is not None:
            if retried_push.error is not None:
                return {
                    "commit_result": retried_push,
                    "error": retried_push.error.message,
                    "events": [{"event": "commit_failed", "timestamp": now}],
                    "commit_created": False,
                }
            return {
                "commit_result": retried_push,
                "error": None,
                "events": [{"event": "commit_pushed_existing", "timestamp": now}],
                "commit_created": False,
            }
        return {
            "commit_result": CommitResult(no_op=True),
            "error": None,
            "events": [{"event": "commit_skipped_no_changes", "timestamp": now}],
            "commit_created": False,
        }

    # --- fetch + rebase -------------------------------------------------------
    try:
        origin_main_fresh, rebase_blocked = _fetch_and_rebase(cwd, skip_rebase, issue_key=issue_key)
    except GitError as exc:
        git_err = BlockedState(
            category="transient",
            message=f"Fetch/rebase failed (worktree may have disappeared): {exc}",
        )
        return {
            "commit_result": CommitResult(error=git_err),
            "error": git_err.message,
            "events": [{"event": "commit_failed", "timestamp": now}],
            "commit_created": False,
        }
    if rebase_blocked is not None:
        err_result = CommitResult(error=rebase_blocked)
        return {
            "commit_result": err_result,
            "error": rebase_blocked.message,
            "events": [{"event": "commit_failed", "timestamp": now}],
            "commit_created": False,
        }

    # --- amend detection ------------------------------------------------------
    # Drive smart-amend through the shared single-commit policy helper (FR-004)
    # rather than calling branch_has_commits_ahead_of_main directly, so the CLI
    # and orchestration policy cannot drift. cwd is forwarded so the check runs
    # in the issue worktree.
    try:
        is_amend = should_amend_instead_of_commit(issue_key, origin_main_fresh=origin_main_fresh, cwd=cwd)
    except GitError as exc:
        amend_err = BlockedState(
            category="transient",
            message=f"Amend-detection probe failed (worktree may have disappeared): {exc}",
        )
        return {
            "commit_result": CommitResult(error=amend_err),
            "error": amend_err.message,
            "events": [{"event": "commit_failed", "timestamp": now}],
            "commit_created": False,
        }

    # --- commit message -------------------------------------------------------
    supplied_message = state.get("commit_message")
    if isinstance(supplied_message, str) and supplied_message.strip():
        commit_message = supplied_message
    else:
        commit_message = _generate_commit_message(issue_key, plan, issue_data, issue_provider=issue_provider)
    commit_message_title = commit_message.split("\n")[0]

    # --- commit ---------------------------------------------------------------
    try:
        if is_amend:
            run_git_safe(["commit", "--amend", "-m", commit_message], cwd=cwd)
        else:
            run_git_safe(["commit", "-m", commit_message], cwd=cwd)
    except GitError as exc:
        err_result = CommitResult(error=BlockedState(category="transient", message=f"Commit failed: {exc}"))
        return {
            "commit_result": err_result,
            "error": f"Commit failed: {exc}",
            "events": [{"event": "commit_failed", "timestamp": now}],
            "commit_created": False,
        }

    # --- read back SHA --------------------------------------------------------
    try:
        sha_result = run_git_capture(["rev-parse", "--short", "HEAD"], cwd=cwd)
    except GitError as exc:
        return {
            "commit_result": CommitResult(
                error=BlockedState(
                    category="transient",
                    message=f"Commit succeeded locally but SHA read-back raised GitError: {exc}",
                )
            ),
            "error": "Could not read commit SHA after successful commit",
            "events": [{"event": "commit_failed", "timestamp": now}],
            "commit_created": True,
        }
    if sha_result.returncode != 0 or not sha_result.stdout.strip():
        # The commit was created locally but we cannot read its SHA — block rather
        # than continuing with commit_sha=None, which would violate FR-011 and
        # leave downstream retry/PR logic without a commit identity.
        sha_err = sha_result.stderr.strip()
        return {
            "commit_result": CommitResult(
                error=BlockedState(
                    category="transient",
                    message=(
                        f"Commit succeeded locally but SHA read-back failed: {sha_err}"
                        if sha_err
                        else "Commit succeeded locally but rev-parse --short HEAD returned no output"
                    ),
                )
            ),
            "error": "Could not read commit SHA after successful commit",
            "events": [{"event": "commit_failed", "timestamp": now}],
            "commit_created": True,
        }
    commit_sha = sha_result.stdout.strip()

    # --- push -----------------------------------------------------------------
    try:
        push_blocked = _push(cwd, is_amend=is_amend)
    except GitError as exc:
        push_git_err = BlockedState(
            category="transient",
            message=f"Push failed (worktree may have disappeared): {exc}",
        )
        return {
            "commit_result": CommitResult(
                commit_sha=commit_sha,
                commit_message_title=commit_message_title,
                is_amend=is_amend,
                push_succeeded=False,
                error=push_git_err,
            ),
            "error": push_git_err.message,
            "events": [{"event": "commit_failed", "timestamp": now}],
            "commit_created": True,
        }
    if push_blocked is not None:
        err_result = CommitResult(
            commit_sha=commit_sha,
            commit_message_title=commit_message_title,
            is_amend=is_amend,
            push_succeeded=False,
            error=push_blocked,
        )
        return {
            "commit_result": err_result,
            "error": push_blocked.message,
            "events": [{"event": "commit_failed", "timestamp": now}],
            "commit_created": True,
        }

    # --- success --------------------------------------------------------------
    success_result = CommitResult(
        commit_sha=commit_sha,
        commit_message_title=commit_message_title,
        is_amend=is_amend,
        push_succeeded=True,
    )
    return {
        "commit_result": success_result,
        "error": None,
        "events": [{"event": "committed", "timestamp": now}],
        "commit_created": True,
    }
