"""Fresh PR diff evidence and initial-delivery classification."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import StrEnum

from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

logger = logging.getLogger(__name__)


class PRDiffEvidence(StrEnum):
    """Freshly observed PR file-diff evidence."""

    ZERO_DIFF = "ZERO_DIFF"
    NON_ZERO_DIFF = "NON_ZERO_DIFF"
    UNKNOWN = "UNKNOWN"


class InitialDeliveryOutcome(StrEnum):
    """Whether a completed initial task delivered changes to its PR."""

    DELIVERED = "DELIVERED"
    NO_DELIVERY = "NO_DELIVERY"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class InitialDeliveryEvidence:
    """Admission handoff from the initial-delivery observer, not from PR prose.

    The caller retains the original task and authoritative plan SHA across recovery
    runs, and supplies the classifier's typed outcome for the observed head.
    Missing admission remains ``None``; this contract does not normalize terminal
    signals or discover an initial-plan identity.
    """

    outcome: InitialDeliveryOutcome
    initial_task_id: str
    initial_plan_sha: str
    head_sha: str
    push_diagnostics: str = ""


def _read_pr_identity(provider: CIPlatformProvider, pr_number: int) -> tuple[str, str, str, int] | None:
    """Read PR base/head identity and the API-reported changed-file count."""
    metadata = provider.get_pr_metadata(pr_number)
    number = getattr(metadata, "number", None)
    base_branch = getattr(metadata, "base_branch", None)
    head_sha = getattr(metadata, "head_sha", None)
    changed_files = getattr(metadata, "changed_files", None)
    if (
        isinstance(number, bool)
        or not isinstance(number, int)
        or number != pr_number
        or not isinstance(base_branch, str)
        or not base_branch.strip()
        or not isinstance(head_sha, str)
        or not head_sha.strip()
        or isinstance(changed_files, bool)
        or not isinstance(changed_files, int)
        or changed_files < 0
    ):
        return None
    base_sha = provider.get_ref_sha(base_branch)
    if not isinstance(base_sha, str) or not base_sha.strip():
        return None
    return base_branch, base_sha, head_sha, changed_files


def _observe_pr_diff_evidence(provider: CIPlatformProvider, pr_number: int) -> tuple[PRDiffEvidence, str]:
    """Observe a complete file inventory between matching fresh base/head identities."""
    if isinstance(pr_number, bool) or not isinstance(pr_number, int) or pr_number <= 0:
        raise ValueError("pr_number must be a positive integer")
    try:
        before = _read_pr_identity(provider, pr_number)
        if before is None:
            logger.warning(
                "Unable to verify PR diff evidence for #%d: PR identity or file count is unavailable", pr_number
            )
            return PRDiffEvidence.UNKNOWN, ""
        list_complete_files = getattr(provider, "list_pr_files_complete", None)
        if not callable(list_complete_files):
            logger.warning(
                "Unable to verify PR diff evidence for #%d: provider cannot prove file inventory completeness",
                pr_number,
            )
            return PRDiffEvidence.UNKNOWN, ""
        files = list_complete_files(pr_number, before[3])
        if (
            not isinstance(files, list)
            or len(files) != before[3]
            or any(not isinstance(path, str) or not path.strip() for path in files)
        ):
            logger.warning("Unable to verify PR diff evidence for #%d: file inventory is incomplete", pr_number)
            return PRDiffEvidence.UNKNOWN, ""
        after = _read_pr_identity(provider, pr_number)
    except ProviderRateLimitError as exc:
        if exc.is_rate_limit:
            raise
        logger.warning("Unable to verify PR diff evidence for #%d: %s", pr_number, exc)
        return PRDiffEvidence.UNKNOWN, ""
    except Exception:
        logger.exception("Unable to verify PR diff evidence for #%d", pr_number)
        return PRDiffEvidence.UNKNOWN, ""
    if after is None or before != after:
        logger.warning("Unable to verify PR diff evidence for #%d: PR identity changed during inventory", pr_number)
        return PRDiffEvidence.UNKNOWN, ""
    evidence = PRDiffEvidence.NON_ZERO_DIFF if files else PRDiffEvidence.ZERO_DIFF
    return evidence, after[2]


def classify_pr_diff_evidence(provider: CIPlatformProvider, pr_number: int) -> PRDiffEvidence:
    """Classify a complete PR file inventory tied to unchanged fresh base/head identities.

    Missing metadata, base refs, malformed or incomplete inventories, provider errors,
    and any base/head change during observation are ``UNKNOWN``.
    """
    evidence, _head_sha = _observe_pr_diff_evidence(provider, pr_number)
    return evidence


def classify_initial_delivery_with_head(
    provider: CIPlatformProvider,
    pr_number: int,
    *,
    completion_confirmed: bool,
    initial_plan_sha: str | None,
) -> tuple[str, InitialDeliveryOutcome]:
    """Return ``(observed_head_sha, typed_outcome)`` for initial delivery.

    The head is the identity actually classified, or ``""`` when none was observed.
    Callers must not substitute a separately read head.
    """
    if completion_confirmed is not True:
        return "", InitialDeliveryOutcome.UNKNOWN
    evidence, fresh_head_sha = _observe_pr_diff_evidence(provider, pr_number)
    if evidence is PRDiffEvidence.NON_ZERO_DIFF:
        return fresh_head_sha, InitialDeliveryOutcome.DELIVERED
    if (
        evidence is PRDiffEvidence.ZERO_DIFF
        and isinstance(initial_plan_sha, str)
        and initial_plan_sha.strip()
        and fresh_head_sha == initial_plan_sha
    ):
        return fresh_head_sha, InitialDeliveryOutcome.NO_DELIVERY
    return fresh_head_sha, InitialDeliveryOutcome.UNKNOWN


def classify_initial_delivery(
    provider: CIPlatformProvider,
    pr_number: int,
    *,
    completion_confirmed: bool,
    initial_plan_sha: str | None,
) -> InitialDeliveryOutcome:
    """Classify delivery without substituting a current SHA for initial-plan identity.

    A non-empty diff is delivered after confirmed completion. An empty diff proves
    no delivery only when its fresh head equals an independently authoritative
    initial-plan SHA; the caller must pass ``None`` when no such source is known.
    """
    return classify_initial_delivery_with_head(
        provider,
        pr_number,
        completion_confirmed=completion_confirmed,
        initial_plan_sha=initial_plan_sha,
    )[1]


def has_verified_non_empty_pr_diff(provider: CIPlatformProvider, pr_number: int) -> bool:
    """Whether a stable, complete PR file inventory proves at least one changed file."""
    try:
        return classify_pr_diff_evidence(provider, pr_number) is PRDiffEvidence.NON_ZERO_DIFF
    except ValueError:
        return False
