"""CLI entry points for audit commands.

Provides ``agdt-audit-prepare``, ``agdt-audit-dispatch-evaluation``,
``agdt-audit-apply``, ``agdt-audit-takeover-eval-prs``, ``agdt-audit-reap-stale``,
and ``agdt-audit-on-pr-close`` commands.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys

from agentic_devtools.cli.github.repo_resolution import resolve_github_repo

logger = logging.getLogger(__name__)


def _write_step_summary(markdown: str) -> None:
    """Append a Markdown block to the GitHub Actions job summary, when available.

    Writes to the file named by ``$GITHUB_STEP_SUMMARY``. Outside GitHub Actions
    (env var unset/empty) this is a no-op. Write failures are logged but never
    raised, so a summary problem cannot mask or change the command's outcome.
    """
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY", "").strip()
    if not summary_path:
        return
    try:
        with open(summary_path, "a", encoding="utf-8") as fh:
            fh.write(markdown + "\n")
    except OSError:
        logger.warning("Failed to write GitHub step summary to %s", summary_path, exc_info=True)


def audit_prepare_command() -> None:
    """CLI entry point for agdt-audit-prepare.

    Runs the preparation phase synchronously. Collects all PR
    review data and produces structured Markdown output for the
    evaluation agent.

    Args (CLI):
        --batch-size: Number of PRs to include in the batch (default: from config or 10).
        --repo: Repository identifier (owner/repo). Falls back to GITHUB_REPOSITORY env var.
    """
    parser = argparse.ArgumentParser(description="Prepare audit batch data")
    parser.add_argument("--batch-size", type=int, default=None, help="Number of PRs in batch")
    parser.add_argument("--repo", type=str, default=None, help="Repository (owner/repo)")
    args = parser.parse_args()

    from agentic_devtools.cli.audit.prepare import prepare_audit_batch
    from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider

    repo = resolve_github_repo(args.repo or os.environ.get("GITHUB_REPOSITORY"))
    provider = GitHubActionsProvider(repo=repo)
    repo_path = os.environ.get("GITHUB_WORKSPACE", os.getcwd())

    try:
        batch = prepare_audit_batch(provider, args.batch_size, repo_path)
        print(
            json.dumps(
                {
                    "batch_id": batch.batch_id,
                    "status": batch.status,
                    "pr_count": len(batch.pr_numbers),
                    "pr_numbers": batch.pr_numbers,
                    "output_dir": batch.output_dir,
                }
            )
        )
    except Exception as e:
        logger.error("Audit preparation failed: %s", e, exc_info=True)
        sys.exit(1)


def audit_apply_command() -> None:
    """CLI entry point for agdt-audit-apply.

    Reads agent evaluation output, applies changes, and creates
    a draft instruction-update PR.

    Args (CLI):
        --batch-id: Audit batch identifier.
        --output-dir: Path to the batch output directory.
        --repo: Repository identifier (owner/repo).
    """
    parser = argparse.ArgumentParser(description="Apply audit evaluation results")
    parser.add_argument("--batch-id", type=str, required=True, help="Batch identifier")
    parser.add_argument("--output-dir", type=str, required=True, help="Batch output directory")
    parser.add_argument("--pr-numbers", type=str, default="", help="Comma-separated PR numbers")
    parser.add_argument("--repo", type=str, default=None, help="Repository (owner/repo)")
    parser.add_argument(
        "--tracking-issue",
        type=int,
        required=True,
        help=(
            "GitHub issue number to use as the commit scope (e.g. 2029, without '#'). "
            "The commit message and PR title follow the repo "
            "Conventional Commits convention with a plain #NNN issue reference."
        ),
    )
    parser.add_argument(
        "--base-sha",
        type=str,
        default="",
        help=(
            "Commit SHA the evaluation was based on (from batch-meta.json). When "
            "provided, the instruction-update PR is branched off this base so its "
            "diff is just the eval delta and the AI PR loop's rebase performs a "
            "3-way merge that integrates concurrent instruction changes."
        ),
    )
    parser.add_argument(
        "--eval-pr-branch",
        type=str,
        default="",
        help="Head branch of the evaluation PR; deleted on success to close the eval PR.",
    )
    args = parser.parse_args()

    from agentic_devtools.cli.audit.apply import (
        apply_audit_results,
        apply_result_is_failure,
        render_apply_summary,
    )
    from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider

    repo = resolve_github_repo(args.repo or os.environ.get("GITHUB_REPOSITORY"))
    provider = GitHubActionsProvider(repo=repo)
    repo_path = os.environ.get("GITHUB_WORKSPACE", os.getcwd())

    try:
        pr_numbers = [int(n.strip()) for n in args.pr_numbers.split(",") if n.strip()]
        result = apply_audit_results(
            provider=provider,
            batch_id=args.batch_id,
            output_dir=args.output_dir,
            pr_numbers=pr_numbers,
            repo_path=repo_path,
            tracking_issue=args.tracking_issue,
            github_repo=repo,
            base_sha=args.base_sha,
            eval_pr_branch=args.eval_pr_branch,
        )
    except Exception as e:
        logger.error("Audit apply failed: %s", e, exc_info=True)
        sys.exit(1)

    _write_step_summary(render_apply_summary(result))
    print(json.dumps(result))
    if apply_result_is_failure(result):
        sys.stderr.write(
            "::error::Audit apply did not produce an instruction-update PR "
            f"(outcome={result.get('outcome')}). See the job log for details.\n"
        )
        sys.exit(1)


def audit_dispatch_evaluation_command() -> None:
    """CLI entry point for agdt-audit-dispatch-evaluation.

    Performs audit write/dispatch wiring after prepare:
    - creates a per-batch tracking issue
    - writes ``batch-meta.json`` under the batch output directory
    - pushes the prepared batch to ``audit/batch-<id>``
    - assigns the coding agent to start evaluation
    """
    parser = argparse.ArgumentParser(description="Dispatch review feedback audit evaluation")
    parser.add_argument("--batch-id", type=str, required=True, help="Batch identifier")
    parser.add_argument("--output-dir", type=str, required=True, help="Batch output directory")
    parser.add_argument("--pr-numbers", type=str, default="", help="Comma-separated PR numbers")
    parser.add_argument("--repo", type=str, default=None, help="Repository (owner/repo)")
    args = parser.parse_args()

    from agentic_devtools.cli.audit.dispatch import dispatch_audit_evaluation
    from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider

    repo = resolve_github_repo(args.repo or os.environ.get("GITHUB_REPOSITORY"))
    provider = GitHubActionsProvider(repo=repo)
    repo_path = os.environ.get("GITHUB_WORKSPACE", os.getcwd())

    try:
        pr_numbers = [int(n.strip()) for n in args.pr_numbers.split(",") if n.strip()]
        result = dispatch_audit_evaluation(
            provider=provider,
            batch_id=args.batch_id,
            output_dir=args.output_dir,
            pr_numbers=pr_numbers,
            repo_path=repo_path,
            github_repo=repo,
        )
        print(json.dumps(result))
    except Exception as e:
        logger.error("Audit evaluation dispatch failed: %s", e, exc_info=True)
        sys.exit(1)


def audit_reap_stale_command() -> None:
    """CLI entry point for agdt-audit-reap-stale.

    Releases the ``review-feedback-audit-in-progress`` label from PRs that were
    claimed for audit but never finalized, so they become eligible for a future
    audit batch again. Intended to run on a schedule as a recovery step.

    Args (CLI):
        --repo: Repository identifier (owner/repo). Falls back to GITHUB_REPOSITORY.
        --max-age-hours: Minimum in-progress label age (hours) before reaping.
            Defaults to the reap module's conservative default.
    """
    parser = argparse.ArgumentParser(description="Reap stale in-progress audit labels")
    parser.add_argument("--repo", type=str, default=None, help="Repository (owner/repo)")
    parser.add_argument(
        "--max-age-hours",
        type=float,
        default=None,
        help="Minimum in-progress label age (hours) before reaping",
    )
    args = parser.parse_args()

    from agentic_devtools.cli.audit.reap import DEFAULT_MAX_AGE_HOURS, reap_stale_in_progress
    from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider

    repo = resolve_github_repo(args.repo or os.environ.get("GITHUB_REPOSITORY"))
    provider = GitHubActionsProvider(repo=repo)
    max_age_hours = args.max_age_hours if args.max_age_hours is not None else DEFAULT_MAX_AGE_HOURS

    try:
        result = reap_stale_in_progress(provider, max_age_hours=max_age_hours)
        print(json.dumps(result))
    except Exception as e:
        logger.error("Audit reap failed: %s", e, exc_info=True)
        sys.exit(1)


def audit_takeover_eval_prs_command() -> None:
    """CLI entry point for agdt-audit-takeover-eval-prs.

    Reclaims Copilot-authored audit evaluation PRs under the human CI identity so
    the gated ``audit-review-feedback-apply`` workflow fires. Prefers a squash
    (clean single commit) and falls back to a takeover amend. Processes at most
    ``--max-prs`` PRs (default 1) and never fails on a single-PR error.

    Args (CLI):
        --repo: Repository identifier (owner/repo). Falls back to GITHUB_REPOSITORY.
        --max-prs: Maximum number of eval PRs to reclaim in one run (default 1).
    """
    parser = argparse.ArgumentParser(description="Reclaim Copilot audit evaluation PRs under a human identity")
    parser.add_argument("--repo", type=str, default=None, help="Repository (owner/repo)")
    parser.add_argument("--max-prs", type=int, default=1, help="Max eval PRs to reclaim per run")
    args = parser.parse_args()

    from agentic_devtools.cli.audit.takeover import takeover_eval_prs
    from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider

    repo = resolve_github_repo(args.repo or os.environ.get("GITHUB_REPOSITORY"))
    provider = GitHubActionsProvider(repo=repo)

    try:
        result = takeover_eval_prs(provider, repo=repo, max_prs=args.max_prs)
        print(json.dumps(result))
    except Exception as e:
        logger.error("Audit evaluation PR takeover failed: %s", e, exc_info=True)
        sys.exit(1)
