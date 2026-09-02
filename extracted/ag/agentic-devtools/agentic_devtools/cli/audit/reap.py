"""Stale in-progress label reaper for the review feedback audit workflow.

Releases the ``review-feedback-audit-in-progress`` label from PRs that were
claimed for audit but never finalized (for example, the evaluation agent was
assigned but never pushed its output, so the apply phase never ran). Without
this recovery step those PRs keep the in-progress label indefinitely and are
permanently excluded from future audit batches (the prepare phase filters them
out).
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from agentic_devtools.cli.audit.config import LABEL_IN_PROGRESS
from agentic_devtools.cli.ci.provider import CIPlatformProvider

logger = logging.getLogger(__name__)

# Conservative default. Off-CI evaluation agents normally finish in minutes, so a
# label older than a day indicates a genuinely stuck batch rather than work in
# flight. A generous TTL avoids reaping a still-running batch, which could let the
# PR be reclaimed by a new batch and double-processed.
DEFAULT_MAX_AGE_HOURS = 24.0


def reap_stale_in_progress(
    provider: CIPlatformProvider,
    max_age_hours: float = DEFAULT_MAX_AGE_HOURS,
) -> dict:
    """Release the in-progress audit label from PRs stuck beyond ``max_age_hours``.

    For each PR currently carrying the in-progress label, the age is measured
    from the most recent time that label was applied. PRs whose label age cannot
    be determined are skipped (never reaped) to avoid removing a label from a PR
    that may still be actively processed.

    Args:
        provider: CI platform provider instance.
        max_age_hours: Minimum label age, in hours, before a PR is reaped.

    Returns:
        Summary dict with keys ``checked`` (int), ``reaped`` (list[int]), and
        ``skipped`` (list[int]).
    """
    if max_age_hours <= 0:
        raise ValueError(
            f"max_age_hours must be a positive number (> 0), got {max_age_hours!r}. "
            "A non-positive TTL would reap all in-progress labels immediately, "
            "including those on actively-running batches."
        )

    result: dict = {"checked": 0, "reaped": [], "skipped": []}

    pr_numbers = provider.list_prs_with_label(LABEL_IN_PROGRESS)
    now = datetime.now(tz=timezone.utc)

    for pr_number in pr_numbers:
        result["checked"] += 1
        applied_at = provider.get_label_applied_at(pr_number, LABEL_IN_PROGRESS)
        if applied_at is None:
            logger.warning(
                "PR #%d carries the in-progress label but its application time is unknown; skipping",
                pr_number,
            )
            result["skipped"].append(pr_number)
            continue

        if applied_at.tzinfo is None:
            logger.warning(
                "PR #%d: label application time has no timezone info; skipping to avoid "
                "potentially reaping an active batch. This may indicate a provider "
                "implementation issue — ensure get_label_applied_at() returns "
                "timezone-aware datetimes.",
                pr_number,
            )
            result["skipped"].append(pr_number)
            continue

        age_hours = (now - applied_at).total_seconds() / 3600.0
        if age_hours < max_age_hours:
            result["skipped"].append(pr_number)
            continue

        try:
            provider.remove_label(pr_number, LABEL_IN_PROGRESS)
        except Exception:
            logger.warning(
                "Failed to remove stale in-progress label from PR #%d",
                pr_number,
                exc_info=True,
            )
            result["skipped"].append(pr_number)
            continue

        logger.info("Reaped stale in-progress label from PR #%d (age %.1fh)", pr_number, age_hours)
        result["reaped"].append(pr_number)

    return result
