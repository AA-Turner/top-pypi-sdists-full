"""Dispatch helpers for the review feedback audit workflow."""

from __future__ import annotations

import json
import logging
import os
import subprocess
from pathlib import Path

from agentic_devtools.cli.audit.config import batch_branch_name
from agentic_devtools.cli.audit.labeling import cleanup_failed_batch
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.git.remote_push import commit_and_push_branch

logger = logging.getLogger(__name__)


def _read_required_speckit_token() -> str:
    """Read SPECKIT_PR_TOKEN from environment or raise a clear error."""
    token = os.environ.get("SPECKIT_PR_TOKEN", "").strip()
    if not token:
        raise RuntimeError("SPECKIT_PR_TOKEN is required for audit write/dispatch operations.")
    return token


def _resolve_base_sha(repo_path: str) -> str:
    """Return the current HEAD commit SHA (the instructions baseline), or "".

    Recorded in ``batch-meta.json`` so the apply phase can branch the
    instruction-update PR off the exact commit whose ``copilot-instructions.md``
    the evaluation agent read. Best-effort: any git failure yields "" and the
    apply phase falls back to branching off current main.
    """
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            shell=False,
        )
    except OSError:
        return ""
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def _push_batch_branch(
    *,
    repo_path: str,
    github_repo: str,
    batch_branch: str,
    batch_id: str,
    output_dir: str,
) -> None:
    """Commit and push prepared batch data to a dedicated batch branch."""
    token = _read_required_speckit_token()
    repo_root = Path(repo_path).resolve()
    output_path = Path(output_dir).resolve()
    output_rel = output_path.relative_to(repo_root)

    token_remote = f"https://x-access-token:{token}@github.com/{github_repo}.git"

    try:
        commit_and_push_branch(
            repo_path=repo_path,
            branch=batch_branch,
            add_paths=[str(output_rel)],
            commit_message=f"chore: persist audit batch {batch_id[:8]}",
            force=True,
            allow_empty=True,
            token_remote_url=token_remote,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Failed to push audit batch branch '{batch_branch}': {exc.stderr}") from exc


def dispatch_audit_evaluation(
    *,
    provider: CIPlatformProvider,
    batch_id: str,
    output_dir: str,
    pr_numbers: list[int],
    repo_path: str,
    github_repo: str,
) -> dict:
    """Create tracking issue, persist batch branch, and dispatch evaluation agent."""
    if not batch_id:
        raise ValueError("batch_id must not be empty")

    output_path = Path(output_dir)
    if not output_path.is_absolute():
        output_path = Path(repo_path) / output_path
    output_path = output_path.resolve()
    if not output_path.is_dir():
        raise FileNotFoundError(f"Batch output directory not found: {output_dir}")

    repo_root = Path(repo_path).resolve()
    if not output_path.is_relative_to(repo_root):
        raise ValueError("output_dir must be inside repo_path")

    # Use POSIX separators so the persisted output_dir matches across OSes and the
    # apply workflow's `audit-batches/{batch_id}` validation (which expects "/").
    output_rel = output_path.relative_to(repo_root).as_posix()
    batch_branch = batch_branch_name(batch_id)

    # The PRs in this batch were already claimed (labeled in-progress) during the
    # prepare phase. Once we begin the post-claim flow, any failure must release
    # those labels so the batch can be retried; otherwise the claimed PRs are
    # permanently excluded from future batches (prepare filters them out).
    try:
        tracking_issue = provider.create_audit_tracking_issue(batch_id=batch_id, pr_numbers=pr_numbers)

        meta_path = output_path / "batch-meta.json"
        meta = {
            "batch_id": batch_id,
            "pr_numbers": pr_numbers,
            "tracking_issue": tracking_issue,
            "batch_branch": batch_branch,
            "output_dir": output_rel,
            "repo": github_repo,
            "base_sha": _resolve_base_sha(repo_path),
        }
        meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        _push_batch_branch(
            repo_path=repo_path,
            github_repo=github_repo,
            batch_branch=batch_branch,
            batch_id=batch_id,
            output_dir=str(output_path),
        )

        assignment_result = provider.dispatch_audit_evaluation(
            tracking_issue=tracking_issue,
            batch_id=batch_id,
            batch_branch=batch_branch,
            batch_dir=output_rel,
            pr_numbers=pr_numbers,
        )
    except Exception:
        logger.exception(
            "Audit batch %s: dispatch failed after PRs were claimed; releasing in-progress labels for retry",
            batch_id,
        )
        cleanup_failed_batch(provider, pr_numbers, [])
        raise

    return {
        "batch_id": batch_id,
        "tracking_issue": tracking_issue,
        "batch_branch": batch_branch,
        "dispatch_method": assignment_result.method,
        "dispatch_task_id": assignment_result.task_id,
        "dispatch_task_url": assignment_result.task_url,
        "dispatch_session_confirmed": assignment_result.session_confirmed,
        "batch_meta_path": meta_path.relative_to(repo_root).as_posix(),
    }
