"""CLI entry point for the round-robin PR scheduler."""

from __future__ import annotations

import json
import logging
import os
import shutil
import sys

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.logging_config import setup_logging
from agentic_devtools.cli.ci.scheduler import run_scheduler

logger = logging.getLogger(__name__)


def ai_pr_loop_scheduler_command() -> None:
    """CLI entry point: select and dispatch the next batch of PRs.

    Reads configuration from repository variables, applies round-robin
    scheduling, dispatches ai-pr-loop.yml for each selected PR, and
    persists the cursor.

    Exit codes:
        0: Success (dispatched or no eligible PRs)
        1: Fatal error (e.g., cannot list PRs, or one or more dispatch attempts failed)
        10: Missing dependency
    """
    setup_logging()

    if shutil.which("gh") is None:
        print("Error: 'gh' CLI not found on PATH.", file=sys.stderr)
        sys.exit(10)

    dry_run = os.environ.get("DRY_RUN", "").lower() in ("1", "true")
    provider = GitHubActionsProvider()

    try:
        result = run_scheduler(provider, dry_run=dry_run)
    except Exception as exc:
        logger.exception("Scheduler failed: %s", exc)
        sys.exit(1)

    # Write GITHUB_STEP_SUMMARY
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY", "")
    if summary_file:
        dispatched_label = "Would Dispatch" if result.run_mode == "dry_run" else "Dispatched"
        try:
            with open(summary_file, "a", encoding="utf-8") as f:
                f.write("## AI PR Loop Throttler — Round-Robin Scheduler\n\n")
                f.write("| Metric | Value |\n| --- | --- |\n")
                f.write(f"| {dispatched_label} | {result.dispatched_count} |\n")
                f.write(f"| PRs | {', '.join(f'#{pr}' for pr in result.dispatched_prs) or 'none'} |\n")
                f.write(f"| Mode | {result.run_mode} |\n")
                f.write(f"| Batch Size | {result.batch_size} |\n")
                f.write(f"| Pool Size | {result.pool_size} |\n")
                f.write(f"| Eligible (fetched) | {result.eligible_count} |\n")
        except OSError as exc:
            logger.warning("Could not write GITHUB_STEP_SUMMARY to %r: %s", summary_file, exc)

    # Structured output for downstream steps (always printed before any non-zero exit)
    output = {
        "run_mode": result.run_mode,
        "batch_size": result.batch_size,
        "pool_size": result.pool_size,
        "eligible_count": result.eligible_count,
        "dispatched_count": result.dispatched_count,
        "dispatched_prs": result.dispatched_prs,
        "cursor_before": result.cursor_before,
        "cursor_after": result.cursor_after,
        "cursor_persisted": result.cursor_persisted,
        "had_dispatch_error": result.had_dispatch_error,
        "status": result.status,
        "cooldown_key": result.cooldown_key,
        "cooldown_source": result.cooldown_source,
        "cooldown_resume_at": result.cooldown_resume_at,
        "cooldown_remaining_seconds": result.cooldown_remaining_seconds,
    }
    try:
        print(json.dumps(output))
    except (TypeError, ValueError) as exc:
        logger.error("Failed to serialize scheduler output: %s", exc)

    if result.had_dispatch_error:
        logger.error("One or more dispatch attempts failed — exiting with code 1")
        sys.exit(1)
