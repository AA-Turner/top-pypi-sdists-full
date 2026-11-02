"""Label lifecycle management for audit batches.

Manages the label transitions during audit:
- Claim: add ``review-feedback-audit-in-progress``
- Finalize: remove ``in-progress``, add ``review-feedback-audited``
- Cleanup: remove ``in-progress`` from unprocessed PRs on failure
"""

from __future__ import annotations

import logging

from agentic_devtools.cli.audit.config import LABEL_AUDITED, LABEL_IN_PROGRESS
from agentic_devtools.cli.ci.provider import CIPlatformProvider

logger = logging.getLogger(__name__)


def finalize_batch_labels(provider: CIPlatformProvider, pr_numbers: list[int]) -> None:
    """Finalize labels after successful audit.

    For each PR in the batch:
    1. Remove ``review-feedback-audit-in-progress`` label
    2. Add ``review-feedback-audited`` label

    Both operations are idempotent — safe to retry.

    Args:
        provider: CI platform provider instance.
        pr_numbers: List of PR numbers to finalize.
    """
    for pr_number in pr_numbers:
        try:
            provider.remove_label(pr_number, LABEL_IN_PROGRESS)
        except Exception:
            logger.warning("Failed to remove in-progress label from PR #%d", pr_number)

        try:
            provider.add_label(pr_number, LABEL_AUDITED)
        except Exception:
            logger.warning("Failed to add audited label to PR #%d", pr_number)


def cleanup_failed_batch(
    provider: CIPlatformProvider,
    claimed_prs: list[int],
    processed_prs: list[int],
) -> None:
    """Clean up labels after a failed audit run.

    Removes the ``review-feedback-audit-in-progress`` label from PRs
    that were claimed but not successfully processed.

    Args:
        provider: CI platform provider instance.
        claimed_prs: All PR numbers that were claimed.
        processed_prs: PR numbers that were successfully processed.
    """
    unprocessed = set(claimed_prs) - set(processed_prs)
    for pr_number in unprocessed:
        try:
            provider.remove_label(pr_number, LABEL_IN_PROGRESS)
        except Exception:
            logger.warning(
                "Failed to remove in-progress label from unprocessed PR #%d",
                pr_number,
            )
