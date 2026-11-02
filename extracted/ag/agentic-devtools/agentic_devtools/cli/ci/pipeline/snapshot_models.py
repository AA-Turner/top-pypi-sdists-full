"""Immutable PR snapshots and their mutable derived-state view."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from agentic_devtools.cli.ci.approver_preflight import ApproverPreflightResult
from agentic_devtools.cli.ci.models import CheckRunStatus, ReviewInfo
from agentic_devtools.cli.ci.pipeline.critique_snapshot import CritiqueSnapshotFields
from agentic_devtools.cli.ci.pipeline.delivery import InitialDeliveryEvidence
from agentic_devtools.cli.ci.pipeline.gate_verdict import CopilotGateVerdict


@dataclass(frozen=True)
class PRStateSnapshot(CritiqueSnapshotFields):
    """Immutable snapshot of all PR state gathered in one pass.

    Attributes:
        pr_number: The pull request number.
        pr_id: The pull request database ID when the provider exposes one.
        initial_delivery: Optional typed admission retaining the original task/plan identity.
        head_sha: Current HEAD commit SHA.
        base_branch: Target branch name.
        base_sha: Target branch commit SHA captured with the snapshot.
        head_branch: Source branch name.
        commit_count: Number of commits above merge-base.
        ci_status: Overall CI status ("passing", "failing", "pending", "unknown").
        ci_failed_checks: List of failed check run names.
        review_state: Latest genuine or trusted synthetic Copilot review state on
            HEAD (or empty string).
        copilot_review_id: ID of the latest genuine or trusted synthetic Copilot
            review on HEAD (0 if none).
        copilot_review_inline_count: Number of inline comments in the latest genuine
            or trusted synthetic Copilot review; `-1` indicates the count is unknown
            because review comments could not be fetched.
        effective_review_comment_count: Number of comments remaining after the same
            reply and thread-state filtering used by repair dispatch; ``None`` means
            the effective inventory could not be determined and callers must fail open.
        effective_review_comment_count_review_id: Review id whose comments produced
            ``effective_review_comment_count``. ``None`` means no source review was
            available (for example, when no current Copilot review targets HEAD).
        effective_review_comment_filter_applied: Whether at least one fetched
            positive-id review comment was removed by reply/thread-state filtering
            while deriving ``effective_review_comment_count``. ``None`` means the
            inventory was unknown.
        active_session: Whether a Copilot coding session is currently active.
        copilot_review_pending: Whether Copilot is pending as a reviewer.
        unresolved_threads: Number of unresolved Copilot review threads not owned by the
            gate verdict (i.e. from reviews whose ID differs from the verdict's effective
            ``review_id``). When the gate has no valid verdict (``review_id == 0``), all
            actionable threads are counted (fail-closed). When ``unresolved_threads_degraded``
            is True this holds a conservative
            blocking fallback value rather than a measured thread count.
        unresolved_threads_degraded: Whether the provider could not report review-thread
            state (capability missing/unimplemented, the lookup failed, the returned
            mapping omitted selected comments, or a review's comments could not be
            listed), so ``unresolved_threads`` is unknown. The gate fails closed on this signal and
            the run summary reports "degraded / unknown" instead of a fabricated integer.
        unresolved_threads_unknown_provenance: Whether the gate-verdict review ID could not be
            resolved when ``unresolved_threads`` was computed, so the count covers *all*
            actionable reviews (the conservative count-all floor) rather than being scoped
            to reviews whose ID differs from the verdict's owner. The count is still
            authoritative — it is the maximum possible value — but consumers can use this
            flag to emit extra diagnostics. No additional gate blocking is required: the
            count-all strategy is already the most conservative possible reading.
        repairable_threads: Number of all unresolved Copilot review threads from any
            actionable Copilot review (current or prior). Unlike ``unresolved_threads``,
            this is independent of the gate verdict and is used solely to determine if
            there is repairable work, decoupled from whether those threads are blocking.
        labels: List of labels on the PR.
        is_draft: Whether the PR is a draft.
        mergeable: Whether the PR is mergeable (None if unknown).
        mergeable_state: Fine-grained mergeability state reported by the provider
            (e.g. ``"clean"``, ``"dirty"``, ``"blocked"``, ``"behind"``, ``"unknown"``).
            ``"dirty"`` is the authoritative signal for a real base-branch conflict.
            Empty string when the provider does not report it.
        requested_reviewers: List of pending reviewer logins.
        has_approval_on_head: Whether an approval exists targeting the current HEAD.
        approver_login: GitHub login of the approver-PAT identity (resolved via
            ``GET /user`` with ``AGDT_PR_APPROVER_PAT``).  Empty string when the token
            is not configured or login resolution failed.  Used together with
            ``has_approver_approval_on_head`` for precise approve-action idempotency.
        approver_preflight: Read-only capability evidence for the actual base repository.
            ``None`` only for providers without the optional preflight capability.
        has_approver_approval_on_head: Whether the approver-PAT identity has already
            approved the current HEAD.  Computed from ``approver_login`` and the
            effective HEAD reviews — only ``True`` when ``approver_login`` is non-empty,
            a matching APPROVED review exists on HEAD, and that review carries a non-empty
            ``commit_sha`` (reviews with an unknown target SHA fail closed and are not
            treated as current).  Used as the idempotency guard for ``ApproveAction`` so
            that the loop skips the API call only when its own required approval is already
            present on HEAD, without treating incidental human approvals as the loop's own.
        title: PR title.
        head_repo_full_name: Full name of the head repository.
        base_repo_full_name: Full name of the base repository.
        files: List of files changed in the PR.
        diff_hash: Rebase-invariant patch fingerprint, when available.
        diff_hash_supported: Whether the provider supports diff fingerprinting.
        diff_hash_available: Whether fingerprinting returned a usable value.
        check_runs: All check run statuses.
        reviews: All reviews for the PR.
        has_changes: Whether the PR has file changes.
        commits_behind: Number of commits the head branch is behind the base branch.
        head_author_login: GitHub login of the HEAD commit's author ("" if unknown).
        copilot_gate_verdict: Structured Copilot gate verdict for the current HEAD.
            ``None`` when the verdict has not been evaluated (e.g. in unit tests that
            construct a snapshot directly without going through
            ``build_pr_state_snapshot``).  When set, ``approve`` and ``merge`` actions
            use this verdict instead of the legacy ``review_state`` + inline-count check.
        head_changed_since_review: Whether the Copilot review selected by the gate
            verdict targets a commit other than the current HEAD. When that effective
            review cannot be resolved to a commit SHA, this fails closed to ``True``.
            Used with ``repair_satisfied_review_id`` to safely clear an already-
            evaluated suppressed-comments block only while the reviewed code is
            unchanged.
        repair_satisfied_review_id: Review id from the most recent Copilot
            ``repair-satisfied`` marker (``None`` when absent). Populated only when the
            gate is blocked solely by suppressed comments on the current HEAD, so the
            approve/merge gate can recognise that those suppressed comments were already
            evaluated by the repair agent.
        suppressed_deferral_review_id: Review id recorded by the most recent active
            ``suppressed-deferral`` marker (``None`` when absent). Populated from the
            same ``issue_comments`` fetch as ``repair_satisfied_review_id`` — no extra
            API call — so the approve/merge gate can recognise a suppressed-only block
            that ``DeferSuppressedAction`` handed to a follow-up triage issue.
        suppressed_deferral_issue_number: Issue number of the deferral follow-up issue
            recorded in the most recent active ``suppressed-deferral`` marker (``None``
            when absent). Populated from the same ``issue_comments`` fetch as
            ``suppressed_deferral_review_id`` — no extra API call — so the post-merge
            dispatch in ``MergeAction`` can recover the issue number on any run, not
            only the run that filed the deferral.
    """

    pr_number: int = 0
    approver_preflight: ApproverPreflightResult | None = field(default=None, kw_only=True)
    pr_id: int | None = field(default=None, kw_only=True)
    initial_delivery: InitialDeliveryEvidence | None = field(default=None, kw_only=True)
    head_sha: str = ""
    base_branch: str = ""
    base_sha: str = ""
    head_branch: str = ""
    commit_count: int = 1
    ci_status: str = "unknown"
    ci_failed_checks: list[str] = field(default_factory=list)
    review_state: str = ""
    copilot_review_id: int = 0
    copilot_review_inline_count: int = 0
    effective_review_comment_count: int | None = None
    effective_review_comment_count_review_id: int | None = None
    effective_review_comment_filter_applied: bool | None = None
    active_session: bool = False
    copilot_review_pending: bool = False
    unresolved_threads: int = 0
    unresolved_threads_degraded: bool = False
    repairable_threads: int = 0
    unresolved_threads_unknown_provenance: bool = False
    labels: list[str] = field(default_factory=list)
    is_draft: bool = False
    mergeable: bool | None = None
    mergeable_state: str = ""
    requested_reviewers: list[str] = field(default_factory=list)
    has_approval_on_head: bool = False
    approver_login: str = ""
    has_approver_approval_on_head: bool = False
    title: str = ""
    head_repo_full_name: str = ""
    base_repo_full_name: str = ""
    files: list[str] = field(default_factory=list)
    diff_hash: str = ""
    diff_hash_supported: bool = False
    diff_hash_available: bool = False
    check_runs: list[CheckRunStatus] = field(default_factory=list)
    reviews: list[ReviewInfo] = field(default_factory=list)
    has_changes: bool = False
    commits_behind: int = 0
    head_author_login: str = ""
    author_login: str = ""
    required_codeowners: list[str] = field(default_factory=list)
    codeowner_logins: list[str] = field(default_factory=list)
    copilot_gate_verdict: CopilotGateVerdict | None = None
    head_changed_since_review: bool = False
    repair_satisfied_review_id: int | None = None
    suppressed_deferral_review_id: int | None = None
    suppressed_deferral_issue_number: int | None = None


class DerivedState:
    """Mutable proxy over a PR snapshot for sharing action updates."""

    def __init__(self, snapshot: PRStateSnapshot) -> None:
        self._snapshot = snapshot
        self._overrides: dict[str, Any] = {}

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(name)
        if name in self._overrides:
            return self._overrides[name]
        return getattr(self._snapshot, name)

    def set(self, name: str, value: Any) -> None:
        """Set a derived state override."""
        self._overrides[name] = value

    def get(self, name: str, default: Any = None) -> Any:
        """Get a derived state value with default fallback."""
        if name.startswith("_"):
            raise AttributeError(name)
        if name in self._overrides:
            return self._overrides[name]
        return getattr(self._snapshot, name, default)

    @property
    def snapshot(self) -> PRStateSnapshot:
        """Access the underlying immutable snapshot."""
        return self._snapshot
