"""Collect provider state into an immutable PR snapshot."""

from __future__ import annotations

import logging
from dataclasses import replace
from typing import Protocol, runtime_checkable

from agentic_devtools.cli.ci.actionable_checks import get_actionable_check_names
from agentic_devtools.cli.ci.approver_preflight import ApproverPreflightResult
from agentic_devtools.cli.ci.models import PRMetadata, ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline import critique_snapshot
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_API_ERROR,
    CopilotGateVerdict,
    evaluate_copilot_gate_verdict,
    is_copilot_or_synthetic_review,
    is_suppressed_only_block,
)
from agentic_devtools.cli.ci.pipeline.snapshot_ci import (
    _count_commits,
    _count_commits_behind,
    _evaluate_ci_status,
    _is_copilot_review_pending,
)
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot
from agentic_devtools.cli.ci.pipeline.snapshot_review_comments import _count_effective_review_comments
from agentic_devtools.cli.ci.pipeline.snapshot_reviews import (
    _head_changed_since_effective_gate_review,
    get_effective_head_reviews,
)
from agentic_devtools.cli.ci.pipeline.snapshot_thread_count import count_unresolved_prior_threads
from agentic_devtools.cli.ci.pipeline.snapshot_utils import _raise_if_rate_limit, _supports_diff_fingerprint
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.ci.retry import _provider_rate_limit_error_from_retryable
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError

logger = logging.getLogger(__name__)


@runtime_checkable
class ApproverPreflightProvider(Protocol):
    """Optional read-only approver evidence, independent of CIPlatformProvider."""

    def get_approver_preflight(self, base_repo_full_name: str) -> ApproverPreflightResult:
        """Return evidence for the actual PR base repository."""


def _get_approver_preflight(provider: CIPlatformProvider, base_repo_full_name: str) -> ApproverPreflightResult | None:
    """Fail closed for supported providers, preserving the existing cooldown path."""
    if not isinstance(provider, ApproverPreflightProvider):
        return None
    try:
        result = provider.get_approver_preflight(base_repo_full_name)
        return result if isinstance(result, ApproverPreflightResult) else ApproverPreflightResult()
    except RetryableError as exc:
        if exc.is_rate_limit:
            raise _provider_rate_limit_error_from_retryable(exc) from exc
        raise
    except ProviderRateLimitError:
        raise
    except Exception:
        return ApproverPreflightResult()


def _get_head_author(provider: CIPlatformProvider, head_sha: str) -> str:
    """Resolve the head author login, failing open when the provider lookup fails."""
    try:
        raw_author = provider.get_commit_author_login(head_sha)
    except Exception as exc:
        _raise_if_rate_limit(exc)
        raw_author = ""
    return raw_author if isinstance(raw_author, str) else ""


def _resolve_base_sha(provider: CIPlatformProvider, pr_number: int, base_branch: str) -> tuple[str, dict[str, str]]:
    """Resolve a provider-supported base SHA and fail closed when it is unavailable."""
    get_ref_sha = getattr(provider, "get_ref_sha", None)
    base_sha = get_ref_sha(base_branch) if callable(get_ref_sha) else ""
    if not isinstance(base_sha, str):
        base_sha = ""
    get_ref_sha_func = getattr(get_ref_sha, "__func__", None)
    supported = (
        callable(get_ref_sha)
        and get_ref_sha_func is not None
        and get_ref_sha_func is not CIPlatformProvider.get_ref_sha
    )
    if supported and not base_sha:
        raise RuntimeError(f"PR #{pr_number}: base branch SHA unavailable for exact diff snapshot")
    return base_sha, {"base_sha": base_sha} if base_sha else {}


def _get_file_inventory(
    provider: CIPlatformProvider,
    pr_number: int,
    base_branch: str,
    head_sha: str,
    base_ref_kwargs: dict[str, str],
) -> list[str]:
    """Return a HEAD-pinned file list when supported, otherwise use the live PR list."""
    compute_diff_files = getattr(provider, "compute_diff_files", None)
    pinned_supported = (
        callable(compute_diff_files)
        and getattr(compute_diff_files, "__func__", None) is not CIPlatformProvider.compute_diff_files
    )
    if pinned_supported:
        assert callable(compute_diff_files)
        try:
            candidate_files = compute_diff_files(base_branch=base_branch, sha=head_sha, **base_ref_kwargs)
        except Exception as exc:
            _raise_if_rate_limit(exc)
            logger.warning(
                "PR #%d: Failed to compute diff files for HEAD %s: %s",
                pr_number,
                head_sha[:12],
                str(exc)[:200],
            )
            raise
        if candidate_files is None:
            raise RuntimeError(f"PR #{pr_number}: exact-HEAD file inventory unavailable for {head_sha}")
        return candidate_files
    return provider.list_pr_files(pr_number)


def _get_diff_fingerprint(
    provider: CIPlatformProvider,
    pr_number: int,
    base_branch: str,
    head_sha: str,
    base_ref_kwargs: dict[str, str],
) -> tuple[str, bool, bool]:
    """Return the optional diff fingerprint, its capability, and availability."""
    supported = _supports_diff_fingerprint(provider)
    compute_diff_hash = getattr(provider, "compute_diff_hash", None)
    if not supported or not callable(compute_diff_hash):
        return "", supported, False
    try:
        candidate_hash = compute_diff_hash(base_branch=base_branch, sha=head_sha, **base_ref_kwargs)
    except Exception as exc:
        _raise_if_rate_limit(exc)
        logger.warning("PR #%d: Failed to compute diff fingerprint: %s", pr_number, str(exc)[:200])
        return "", supported, False
    if isinstance(candidate_hash, str) and candidate_hash:
        return candidate_hash, supported, True
    if candidate_hash == "":
        logger.warning("PR #%d: Ignoring empty diff fingerprint from provider", pr_number)
    elif candidate_hash is None:
        logger.warning("PR #%d: Provider returned None for diff fingerprint", pr_number)
    else:
        logger.warning(
            "PR #%d: Ignoring non-string diff fingerprint of type %s",
            pr_number,
            type(candidate_hash).__name__,
        )
    return "", supported, False


def _collect_diff_state(
    provider: CIPlatformProvider,
    pr_number: int,
    pr_meta: PRMetadata,
) -> tuple[list[str], str, str, bool, bool]:
    """Collect the base SHA, file inventory, and optional diff fingerprint."""
    base_sha, base_ref_kwargs = _resolve_base_sha(provider, pr_number, pr_meta.base_branch)
    files = _get_file_inventory(provider, pr_number, pr_meta.base_branch, pr_meta.head_sha, base_ref_kwargs)
    diff_hash, diff_hash_supported, diff_hash_available = _get_diff_fingerprint(
        provider, pr_number, pr_meta.base_branch, pr_meta.head_sha, base_ref_kwargs
    )
    return files, base_sha, diff_hash, diff_hash_supported, diff_hash_available


def _promote_findings(
    provider: CIPlatformProvider,
    pr_number: int,
    head_sha: str,
    base_sha: str,
    reviews: list[ReviewInfo],
    enabled: bool,
) -> str:
    """Promote CCR findings when supported, returning an error summary on failure."""
    promote = getattr(provider, "promote_ccr_findings", None)
    if not enabled or not callable(promote) or not callable(getattr(type(provider), "promote_ccr_findings", None)):
        return ""
    try:
        promote(pr_number=pr_number, commit_sha=head_sha, base_sha=base_sha, reviews=reviews)
    except Exception as exc:
        _raise_if_rate_limit(exc)
        logger.exception("PR #%d: CCR finding promotion failed; review evidence remains pending", pr_number)
        return str(exc)[:500] or type(exc).__name__
    return ""


def _get_approval_state(
    provider: CIPlatformProvider,
    pr_number: int,
    reviews: list[ReviewInfo],
    head_sha: str,
    preflight: ApproverPreflightResult | None = None,
) -> tuple[bool, str, bool]:
    """Return approval status on HEAD and the best-effort approver identity."""
    effective_reviews = get_effective_head_reviews(reviews, head_sha)
    has_approval = any(review.state == "APPROVED" for review in effective_reviews)
    try:
        raw_login = preflight.authenticated_login if preflight is not None else provider.get_approver_login()
        approver_login = raw_login if isinstance(raw_login, str) else ""
    except Exception as exc:
        _raise_if_rate_limit(exc)
        logger.debug("Failed to resolve approver login for PR %s", pr_number, exc_info=True)
        approver_login = ""
    has_approver_approval = bool(
        approver_login
        and any(
            review.state == "APPROVED"
            and isinstance(review.user, str)
            and review.user.casefold() == approver_login.casefold()
            and not is_copilot_or_synthetic_review(review)
            and review.commit_sha
            for review in effective_reviews
        )
    )
    return has_approval, approver_login, has_approver_approval


def _get_copilot_review(
    provider: CIPlatformProvider,
    pr_number: int,
    reviews: list[ReviewInfo],
    head_sha: str,
) -> tuple[ReviewInfo | None, str, int, int, list[ReviewCommentInfo] | None]:
    """Find the effective Copilot review and count its inline comments."""
    review = max(
        (
            item
            for item in reviews
            if is_copilot_or_synthetic_review(item) and (not item.commit_sha or item.commit_sha == head_sha)
        ),
        key=lambda item: (item.submitted_at if isinstance(item.submitted_at, str) else "", item.id),
        default=None,
    )
    if review is None:
        return None, "", 0, 0, None
    comments: list[ReviewCommentInfo] | None = None
    inline_count = 0
    if review.state in {"COMMENTED", "CHANGES_REQUESTED", "APPROVED"}:
        try:
            comments = provider.list_review_comments(pr_number, review.id)
            if review.state == "COMMENTED":
                inline_count = len(comments)
        except Exception as exc:
            _raise_if_rate_limit(exc)
            comments = None
            if review.state == "COMMENTED":
                inline_count = -1
    return review, review.state, review.id, inline_count, comments


def _get_copilot_gate_verdict(
    provider: CIPlatformProvider,
    pr_number: int,
    reviews: list[ReviewInfo],
    head_sha: str,
    base_branch: str,
    promotion_failure: str,
) -> CopilotGateVerdict:
    """Evaluate the Copilot gate, converting failures into a closed verdict."""
    try:
        verdict = evaluate_copilot_gate_verdict(
            reviews=reviews,
            head_sha=head_sha,
            pr_number=pr_number,
            provider=provider,
            base_branch=base_branch,
        )
    except Exception as exc:
        _raise_if_rate_limit(exc)
        logger.exception("PR #%d: Failed to evaluate gate verdict", pr_number)
        exc_summary = str(exc)[:200]
        verdict = CopilotGateVerdict(
            passed=False,
            reason=REASON_API_ERROR,
            details=f"Gate verdict evaluation raised an unexpected exception: {exc_summary}",
        )
    if promotion_failure:
        return CopilotGateVerdict(
            passed=False,
            reason=REASON_API_ERROR,
            details=f"CCR finding promotion is incomplete: {promotion_failure}",
        )
    return verdict


def build_pr_state_snapshot(
    provider: CIPlatformProvider,
    pr_number: int,
    *,
    actionable_check_names: frozenset[str] | None = None,
    promote_findings: bool = True,
) -> PRStateSnapshot:
    """Build a complete PR state snapshot in one pass.

    Gathers all required data from the provider to make a single immutable
    snapshot that the pipeline evaluates against. Set ``promote_findings=False``
    to skip side-effectful CCR finding promotion.
    """
    if actionable_check_names is None:
        actionable_check_names = get_actionable_check_names()
    pr_meta = provider.get_pr_metadata(pr_number)
    preflight = _get_approver_preflight(provider, pr_meta.base_repo_full_name)
    head_author_login = _get_head_author(provider, pr_meta.head_sha)
    files, base_sha, diff_hash, diff_hash_supported, diff_hash_available = _collect_diff_state(
        provider, pr_number, pr_meta
    )

    check_runs = provider.list_check_runs(pr_meta.head_sha)
    is_codeql_configured = getattr(provider, "is_codeql_configured", None)
    codeql_configured = callable(is_codeql_configured) and is_codeql_configured(base_branch=pr_meta.base_branch) is True
    ci_status, ci_failed_checks = _evaluate_ci_status(
        check_runs,
        actionable_check_names,
        codeql_configured=codeql_configured,
    )

    reviews = provider.list_reviews(pr_number)
    promotion_failure = _promote_findings(
        provider,
        pr_number,
        pr_meta.head_sha,
        base_sha,
        reviews,
        promote_findings,
    )
    has_approval_on_head, approver_login, has_approver_approval_on_head = _get_approval_state(
        provider,
        pr_number,
        reviews,
        pr_meta.head_sha,
        preflight,
    )
    copilot_review, copilot_review_state, copilot_review_id, copilot_review_inline_count, comments = (
        _get_copilot_review(
            provider,
            pr_number,
            reviews,
            pr_meta.head_sha,
        )
    )
    copilot_review_pending = _is_copilot_review_pending(pr_meta.requested_reviewers)
    commit_count = _count_commits(provider, base_branch=pr_meta.base_branch, head_sha=pr_meta.head_sha)
    commits_behind = _count_commits_behind(
        provider, pr_number=pr_number, base_branch=pr_meta.base_branch, head_branch=pr_meta.head_branch
    )

    copilot_gate_verdict = _get_copilot_gate_verdict(
        provider,
        pr_number,
        reviews,
        pr_meta.head_sha,
        pr_meta.base_branch,
        promotion_failure,
    )
    (
        unresolved_threads,
        repairable_threads,
        unresolved_threads_degraded,
        unresolved_threads_unknown_provenance,
    ) = count_unresolved_prior_threads(
        provider,
        pr_number,
        reviews,
        copilot_gate_verdict.review_id if copilot_gate_verdict.review_id > 0 else None,
        verdict=copilot_gate_verdict,
    )
    head_changed_since_review = _head_changed_since_effective_gate_review(
        reviews=reviews,
        current_head_sha=pr_meta.head_sha,
        verdict=copilot_gate_verdict,
    )

    effective_review_comment_count = None
    effective_review_comment_count_review_id: int | None = None
    effective_review_comment_filter_applied: bool | None = None
    if copilot_review is not None:
        effective_review_comment_count_review_id = copilot_review.id
        (
            effective_review_comment_count,
            effective_review_comment_filter_applied,
        ) = _count_effective_review_comments(provider, pr_number, copilot_review, comments)
    repair_satisfied_review_id, current_overview_headline, critique_fields = (
        critique_snapshot.initial_critique_snapshot_state(
            copilot_gate_verdict,
            reviews,
            pr_meta.head_sha,
            head_changed_since_review,
            effective_review_comment_count,
            effective_review_comment_count_review_id,
            effective_review_comment_filter_applied,
        )
    )
    suppressed_deferral_review_id: int | None = None
    suppressed_deferral_issue_number: int | None = None
    if (
        copilot_gate_verdict is not None
        and not head_changed_since_review
        and critique_snapshot.should_load_issue_comment_critique_state(copilot_gate_verdict, current_overview_headline)
        and (is_suppressed_only_block(copilot_gate_verdict) or bool(current_overview_headline))
    ):
        list_issue_comments = getattr(provider, "list_issue_comments", None)
        if callable(list_issue_comments):
            try:
                issue_comments = list_issue_comments(pr_number)
                pr_token_login: str | None = None
                get_pr_token_login = getattr(provider, "get_pr_token_login", None)
                if callable(get_pr_token_login):
                    try:
                        pr_token_login = get_pr_token_login()
                    except Exception as exc:
                        _raise_if_rate_limit(exc)
                extra_authors = frozenset({pr_token_login.casefold()}) if pr_token_login else None
                (
                    repair_satisfied_review_id,
                    suppressed_deferral_review_id,
                    suppressed_deferral_issue_number,
                    critique_fields,
                ) = critique_snapshot.load_issue_comment_critique_state(
                    provider,
                    pr_number,
                    issue_comments,
                    reviews,
                    pr_meta.head_sha,
                    copilot_gate_verdict,
                    current_overview_headline,
                    critique_fields.critique_headline_classification,
                    extra_authors,
                )
            except Exception as exc:
                _raise_if_rate_limit(exc)
                logger.warning(
                    "PR #%d: Failed to fetch issue comments for repair-satisfied marker: %s",
                    pr_number,
                    str(exc)[:200],
                )
                critique_fields = replace(critique_fields, critique_task_state_available=False)
        else:
            critique_fields = replace(critique_fields, critique_task_state_available=False)

    return PRStateSnapshot(
        approver_preflight=preflight,
        pr_number=pr_number,
        pr_id=pr_meta.pr_id,
        head_sha=pr_meta.head_sha,
        base_branch=pr_meta.base_branch,
        base_sha=base_sha,
        head_branch=pr_meta.head_branch,
        commit_count=commit_count,
        ci_status=ci_status,
        ci_failed_checks=ci_failed_checks,
        review_state=copilot_review_state,
        copilot_review_id=copilot_review_id,
        copilot_review_inline_count=copilot_review_inline_count,
        effective_review_comment_count=effective_review_comment_count,
        effective_review_comment_count_review_id=effective_review_comment_count_review_id,
        effective_review_comment_filter_applied=effective_review_comment_filter_applied,
        copilot_review_pending=copilot_review_pending,
        unresolved_threads=unresolved_threads,
        unresolved_threads_degraded=unresolved_threads_degraded,
        repairable_threads=repairable_threads,
        unresolved_threads_unknown_provenance=unresolved_threads_unknown_provenance,
        labels=list(pr_meta.labels),
        is_draft=pr_meta.is_draft,
        mergeable=pr_meta.mergeable,
        mergeable_state=pr_meta.mergeable_state,
        requested_reviewers=list(pr_meta.requested_reviewers),
        has_approval_on_head=has_approval_on_head,
        approver_login=approver_login,
        has_approver_approval_on_head=has_approver_approval_on_head,
        title=pr_meta.title,
        head_repo_full_name=pr_meta.head_repo_full_name,
        base_repo_full_name=pr_meta.base_repo_full_name,
        files=files,
        diff_hash=diff_hash,
        diff_hash_supported=diff_hash_supported,
        diff_hash_available=diff_hash_available,
        check_runs=check_runs,
        reviews=reviews,
        has_changes=bool(files),
        commits_behind=commits_behind,
        head_author_login=head_author_login,
        copilot_gate_verdict=copilot_gate_verdict,
        head_changed_since_review=head_changed_since_review,
        repair_satisfied_review_id=repair_satisfied_review_id,
        suppressed_deferral_review_id=suppressed_deferral_review_id,
        suppressed_deferral_issue_number=suppressed_deferral_issue_number,
        **critique_fields.as_kwargs(),
    )
