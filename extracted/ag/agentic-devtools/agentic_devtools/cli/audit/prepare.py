"""Preparation phase for the audit workflow.

Implements the deterministic data collection pipeline that gathers all
PR review data, claims PRs for audit, and produces structured output
for the evaluation agent.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone

from agentic_devtools.cli.audit.config import LABEL_AUDITED, LABEL_IN_PROGRESS, resolve_batch_size
from agentic_devtools.cli.audit.instruction_resolver import resolve_instruction_files
from agentic_devtools.cli.audit.labeling import cleanup_failed_batch
from agentic_devtools.cli.audit.models import (
    AuditBatch,
    BatchOutput,
    ClaimResult,
    ClosedPRInfo,
    ReviewObservation,
)
from agentic_devtools.cli.audit.output_format import assign_category, write_batch_output
from agentic_devtools.cli.audit.staleness import detect_stale_comments
from agentic_devtools.cli.ci.provider import CIPlatformProvider

logger = logging.getLogger(__name__)


def prepare_audit_batch(
    provider: CIPlatformProvider,
    batch_size: int | None,
    repo_path: str,
) -> AuditBatch:
    """Execute the full preparation pipeline for an audit batch.

    Steps:
    1. Resolve batch size from CLI/config/default
    2. List newest closed PRs excluding already-audited and in-progress
    3. Claim PRs via label (skip if already claimed by concurrent run)
    4. For each claimed PR: fetch reviews and comments
    5. Assign categories to observations
    6. Run staleness detection
    7. Resolve instruction files
    8. Write structured output

    On failure, cleans up in-progress labels from PRs that were claimed but not processed.

    Args:
        provider: CI platform provider instance.
        batch_size: Explicit batch size (None to resolve from config).
        repo_path: Absolute path to the repository root.

    Returns:
        AuditBatch with metadata about the completed preparation.
    """
    resolved_batch_size = resolve_batch_size(batch_size, repo_path)
    batch_id = uuid.uuid4().hex
    now = datetime.now(tz=timezone.utc).isoformat()

    from agentic_devtools.state import get_state_dir

    state_dir = get_state_dir()
    output_dir = str(state_dir / "audit-batches" / batch_id)

    batch = AuditBatch(
        batch_id=batch_id,
        created_at=now,
        status="preparing",
        output_dir=output_dir,
    )

    claimed_prs: list[int] = []
    processed_prs: list[int] = []

    try:
        # Get eligible PRs (newest first)
        eligible_prs = provider.list_closed_prs(
            exclude_labels=[LABEL_AUDITED, LABEL_IN_PROGRESS],
            limit=resolved_batch_size * 2,  # Fetch extra in case of claim conflicts
            state="closed",
        )

        # Claim loop: try to claim up to batch_size PRs
        for pr_info in eligible_prs:
            if len(claimed_prs) >= resolved_batch_size:
                break

            result = provider.claim_pr_for_audit(pr_info.number, LABEL_IN_PROGRESS)
            if result == ClaimResult.CLAIMED:
                claimed_prs.append(pr_info.number)
            else:
                logger.debug("PR #%d already claimed, skipping", pr_info.number)

        if not claimed_prs:
            batch.status = "empty"
            batch.pr_numbers = []
            logger.info("No eligible PRs found for audit batch")
            return batch

        batch.pr_numbers = claimed_prs

        # Collect review data for each claimed PR
        all_observations: list[ReviewObservation] = []
        all_prs: list[ClosedPRInfo] = []
        all_file_paths: list[str] = []

        for pr_number in claimed_prs:
            pr_data = _collect_pr_data(provider, pr_number, eligible_prs)
            if pr_data:
                pr_info, observations, file_paths = pr_data
                all_prs.append(pr_info)
                all_observations.extend(observations)
                all_file_paths.extend(file_paths)
                processed_prs.append(pr_number)

        # Remove in-progress labels from PRs whose data collection failed,
        # and exclude them from the batch so they are not marked as audited.
        failed_prs = set(claimed_prs) - set(processed_prs)
        if failed_prs:
            logger.warning(
                "Releasing in-progress labels for %d PR(s) that failed data collection: %s",
                len(failed_prs),
                sorted(failed_prs),
            )
            cleanup_failed_batch(provider, list(failed_prs), [])
        batch.pr_numbers = processed_prs

        # Run staleness detection
        all_observations = detect_stale_comments(all_observations, repo_path)

        # Resolve instruction files
        unique_paths = sorted(set(all_file_paths))
        instruction_files = resolve_instruction_files(unique_paths, repo_path)

        # Build output
        batch_output = BatchOutput(
            batch_id=batch_id,
            prs=all_prs,
            observations=all_observations,
            instruction_files=instruction_files,
        )

        # Write structured output files
        write_batch_output(batch_output, output_dir)

        batch.status = "ready"
        logger.info(
            "Audit batch %s prepared: %d PRs, %d observations",
            batch_id,
            len(all_prs),
            len(all_observations),
        )
        return batch

    except Exception:
        # Clean up in-progress labels on failure
        cleanup_failed_batch(provider, claimed_prs, processed_prs)
        raise


def _collect_pr_data(
    provider: CIPlatformProvider,
    pr_number: int,
    eligible_prs: list[ClosedPRInfo],
) -> tuple[ClosedPRInfo, list[ReviewObservation], list[str]] | None:
    """Collect review data for a single PR.

    Returns:
        Tuple of (pr_info, observations, file_paths) or None on failure.
    """
    # Find PR info from eligible list
    pr_info = next((p for p in eligible_prs if p.number == pr_number), None)
    if pr_info is None:
        logger.warning("PR #%d not found in eligible list", pr_number)
        return None

    try:
        # Fetch all review comments
        comments = provider.list_all_review_comments(pr_number)
    except Exception:
        logger.warning("Failed to fetch review comments for PR #%d", pr_number, exc_info=True)
        return None

    observations: list[ReviewObservation] = []
    file_paths: list[str] = []

    for comment in comments:
        primary, secondary = assign_category(comment.body)
        obs = ReviewObservation(
            file_path=comment.path,
            line=comment.end_line or comment.line,
            body=comment.body,
            diff_hunk=comment.diff_hunk,
            resolved=False,  # Will be enriched if thread data available
            reviewer=comment.author_login,
            primary_category=primary,
            secondary_category=secondary,
            pr_number=pr_number,
        )
        observations.append(obs)
        if comment.path:
            file_paths.append(comment.path)

    return (pr_info, observations, file_paths)
