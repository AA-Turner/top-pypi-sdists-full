"""Copilot gate verdict evaluation for the AI PR pipeline.

Ports the review-verdict logic from ``.github/workflows/copilot-review-gate.yml``
into the Python pipeline so the loop blocks approval/merge under the same conditions.

The evaluation is fail-closed: any ambiguous, unparseable, or API-error case
produces a blocking verdict.

Public API
----------
- :class:`CopilotGateVerdict` — structured verdict returned by the evaluator.
- :data:`REASON_*` — string constants for verdict reason codes.
- :func:`evaluate_copilot_gate_verdict` — main entry point; safe to call from
  ``build_pr_state_snapshot`` (does **not** call ``sys.exit``).
- :func:`is_suppressed_only_block` — ``True`` when a verdict is blocked solely by
  suppressed/low-confidence comments (no real posted inline comments).
- :func:`suppressed_comments_evaluated` — narrowly scoped, fail-closed predicate
  used by approve/merge to clear a suppressed-only block once the repair agent has
  evaluated the suppressed comments (``repair-satisfied`` marker for the review id,
  HEAD unchanged, no real unresolved threads).
- :func:`suppressed_deferral_eligible` — fail-closed ten-condition predicate for
  deferring a specs-only suppressed-only review round to a follow-up issue, with
  :func:`suppressed_deferral_snapshot_eligible` as its snapshot-only subset and
  :func:`suppressed_deferral_recorded` as the approve/merge bypass for a review
  whose suppressed comments were already deferred.
- :func:`is_review_clean` — legacy clean-review predicate used when no gate verdict
  is available.
- :func:`copilot_review_gate_passed` — the single shared "the review has gone clean
  on HEAD" predicate shared by approve, merge and the deferred squash gate.
- :func:`select_prior_actionable_reviews` — the single shared "which reviews count
  as prior" selector used by the snapshot's thread counter, thread resolution and
  repair dispatch. Scoped by the gate verdict's ``review_id`` (fails closed to
  count-all when ``review_id <= 0``), not by HEAD commit SHA.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

from agentic_devtools.cli.ci.models import ReviewInfo, is_copilot_login
from agentic_devtools.cli.github.ccr_review_format import (
    VERDICT_NOT_APPROVE,
    extract_suppressed_comment_entries,
    parse_reported_comment_count,
    parse_suppressed_count,
    parse_verdict,
    unrecovered_suppression_signal,
)
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

if TYPE_CHECKING:
    from agentic_devtools.cli.ci.pipeline.snapshot import PRStateSnapshot
    from agentic_devtools.cli.ci.provider import CIPlatformProvider

# ---------------------------------------------------------------------------
# Trusted synthetic review users & marker
# ---------------------------------------------------------------------------

#: Users whose reviews bearing the synthetic marker are treated as Copilot reviews.
TRUSTED_SYNTHETIC_USERS: frozenset[str] = frozenset({"AMARSNIK_swica"})
_TRUSTED_SYNTHETIC_USERS_CASEFOLDED: frozenset[str] = frozenset(user.casefold() for user in TRUSTED_SYNTHETIC_USERS)

#: HTML comment marker injected by the synthetic-copilot-review workflow.
SYNTHETIC_MARKER: str = "<!-- synthetic-copilot-review -->"

#: Submitted review states that carry actionable feedback for a prior commit.
_ACTIONABLE_PRIOR_REVIEW_STATES: frozenset[str] = frozenset({"CHANGES_REQUESTED", "COMMENTED"})

# ---------------------------------------------------------------------------
# Verdict reason constants
# ---------------------------------------------------------------------------

#: Review is clean — no comments, passes gate.
REASON_CLEAN = "clean"

#: No fresh Copilot review exists for the current HEAD.
REASON_AWAITING_FRESH = "awaiting_fresh_copilot_review"

#: Copilot's review body reports posted comments > 0.
REASON_HAS_COMMENTS = "copilot_review_has_comments"

#: Copilot's review body reports suppressed/low-confidence comments > 0.
REASON_SUPPRESSED_COMMENTS = "copilot_review_suppressed_comments"

#: Body advertises suppressed comments the structured parser could not recover.
REASON_UNPARSED_SUPPRESSION = "copilot_review_unparsed_suppression"

#: New CCR format review body has a "Not ready to approve" verdict heading.
REASON_NEW_CCR_NOT_APPROVED = "copilot_review_new_format_not_approved"

#: PR diff content changed since the prior-commit review.
REASON_CONTENT_CHANGED = "copilot_review_content_changed_since_review"

#: Synthetic review has ``parse_failed=true``.
REASON_SYNTHETIC_PARSE_FAILED = "synthetic_review_parse_failed"

#: Synthetic review is missing ``intended_comments``/``inline_posted`` metadata.
REASON_SYNTHETIC_MISSING_METADATA = "synthetic_review_missing_metadata"

#: Synthetic review intended comments but posted none inline.
REASON_SYNTHETIC_COMMENTS_NOT_POSTED = "synthetic_review_comments_not_posted"

#: Synthetic review metadata says comments were posted but API returned 0.
REASON_SYNTHETIC_INLINE_MISMATCH = "synthetic_review_inline_mismatch"

#: Synthetic review has unresolved inline comments.
REASON_SYNTHETIC_HAS_INLINE = "synthetic_review_has_inline_comments"

#: API error during verdict evaluation — failing closed.
REASON_API_ERROR = "copilot_review_api_error"


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CopilotGateVerdict:
    """Structured result of the Copilot gate verdict evaluation.

    Attributes:
        passed: ``True`` when the gate is satisfied (review is clean and fresh).
        reason: One of the ``REASON_*`` constants describing the outcome.
        review_id: ID of the Copilot review that was evaluated (0 when unknown).
        body_comment_count: Self-reported comment count from the review body
            (``None`` when the body could not be parsed).
        suppressed_count: Self-reported suppressed/low-confidence comment count
            parsed from the review body.
        synthetic: ``True`` when the review was posted by a trusted synthetic user.
        details: Human-readable explanation for logging.
        carried_over_sha: Commit SHA of the prior-commit review that was carried
            over to the current HEAD because the PR diff content hash is unchanged
            (rebase/squash-only change). Empty string when the evaluated review
            targets HEAD directly or when no review could be carried over. Consumers
            must pair a non-empty value with ``passed`` before acting on it — a
            carried-over review may still be blocking.
    """

    passed: bool
    reason: str
    review_id: int = 0
    body_comment_count: int | None = None
    suppressed_count: int = 0
    synthetic: bool = False
    details: str = ""
    carried_over_sha: str = ""


# ---------------------------------------------------------------------------
# Suppressed-comment evaluation bypass
# ---------------------------------------------------------------------------


def is_suppressed_only_block(verdict: CopilotGateVerdict) -> bool:
    """Return ``True`` when *verdict* is blocked **solely** by suppressed comments.

    This is the case when the only reason the gate failed is suppressed /
    low-confidence comments with **no** real posted inline comments:

    - a legacy/standard ``REASON_SUPPRESSED_COMMENTS`` verdict (posted count is
      guaranteed 0 for that reason), or
    - a new-CCR ``REASON_NEW_CCR_NOT_APPROVED`` verdict whose self-reported posted
      comment count is 0 (``body_comment_count == 0``) — i.e. the "Not ready to
      approve" heading is driven only by suppressed comments, not real ones.

    In both cases at least one suppressed comment must be present
    (``suppressed_count > 0``).  A ``None`` ``body_comment_count`` (unparseable
    body) is treated conservatively as *not* suppressed-only so the fail-closed
    gate keeps blocking.
    """
    if verdict.suppressed_count <= 0:
        return False
    if verdict.reason == REASON_SUPPRESSED_COMMENTS:
        return True
    if verdict.reason == REASON_NEW_CCR_NOT_APPROVED:
        return verdict.body_comment_count == 0
    return False


def suppressed_comments_evaluated(
    verdict: CopilotGateVerdict | None,
    *,
    repair_satisfied_review_id: int | None,
    head_changed_since_review: bool,
    unresolved_threads: int,
) -> bool:
    """Return ``True`` when a suppressed-only gate block was already evaluated.

    The AI PR loop dispatches a repair agent when a review is blocked only by
    suppressed/low-confidence comments.  Those suppressed comments are recovered
    as synthetic negative-ID entries with **no** real GitHub review threads, so
    the normal thread-resolution path can never clear them.  Instead the repair
    agent posts a ``repair-satisfied`` marker (carrying the evaluated ``review-id``)
    once it has evaluated the suppressed comments and found no changes needed.

    This predicate lets the approve/merge gate proceed **only** under a narrowly
    scoped, fail-closed set of conditions:

    - a blocking verdict exists and it is a suppressed-only block
      (:func:`is_suppressed_only_block`);
    - the reviewed commit is still HEAD (``not head_changed_since_review``);
    - there are no real unresolved inline review threads
      (``unresolved_threads == 0``);
    - the verdict identifies a concrete review (``review_id > 0``); and
    - a ``repair-satisfied`` marker is present for **exactly** that review id.

    Any other blocking reason (real posted comments, unresolved real threads,
    content-changed/freshness, a genuine un-evaluated "Not ready to approve",
    a HEAD change since review, or a review-id mismatch) returns ``False`` so the
    gate keeps blocking exactly as it does today.
    """
    if verdict is None or verdict.passed:
        return False
    if not is_suppressed_only_block(verdict):
        return False
    if head_changed_since_review:
        return False
    if unresolved_threads != 0:
        return False
    if verdict.review_id <= 0:
        return False
    return repair_satisfied_review_id == verdict.review_id


# ---------------------------------------------------------------------------
# Specs-only suppressed-review deferral
# ---------------------------------------------------------------------------

#: Repo-relative path prefixes classified as **executable** code.  A suppressed
#: finding on any of these — or an executable file anywhere in the PR diff —
#: makes the PR ineligible for deferral.
EXECUTABLE_PATH_PREFIXES: tuple[str, ...] = ("agentic_devtools/", "scripts/", ".github/")

#: Label carried by a deferral follow-up issue and propagated onto its PR.  A PR
#: carrying it (directly or via a linked issue) may never defer again — the
#: one-generation cap.
SUPPRESSED_FOLLOW_UP_LABEL = "suppressed-comment-follow-up"

#: A recovered suppressed-comment "path" is only trusted when it looks like a
#: repo-relative file path: at least one ``/``-free segment carrying a file
#: extension, optionally followed by a ``:line`` anchor.  This deliberately
#: rejects the non-path strings CCR emits for unattributed findings
#: (``get_issue_types()``, ``--dry-run``, ``Acceptance Scenarios``), which would
#: otherwise pass a naive "does not start with an executable prefix" test.
_WELL_FORMED_PATH_RE = re.compile(r"^[\w.@+-]+(?:/[\w.@+-]+)*\.[A-Za-z0-9]+(?::\d+(?:-\d+)?)?$")


def is_executable_path(path: str) -> bool:
    """Return ``True`` when *path* points at executable (non-specs) code.

    "Executable" is ``agentic_devtools/**`` ∪ ``scripts/**`` ∪ ``.github/**``.
    A leading ``./`` or ``/`` is normalised away first so a differently rendered
    path cannot slip past the prefix test.
    """
    normalized = path.strip().lstrip("/")
    if normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized.startswith(EXECUTABLE_PATH_PREFIXES)


def is_well_formed_path(path: str) -> bool:
    """Return ``True`` when *path* is a plausible repo-relative file path.

    Fail-closed: anything that is not a ``dir/file.ext`` (optionally ``:line``)
    string — including :data:`~agentic_devtools.cli.github.ccr_review_format.UNKNOWN_FILE`,
    function names such as ``get_issue_types()`` and flags such as ``--dry-run``
    — returns ``False``.  An unattributed finding is **not** provably
    non-executable, so it must never be deferred.
    """
    candidate = path.strip().lstrip("/")
    if candidate.startswith("./"):
        candidate = candidate[2:]
    if not candidate or ".." in candidate:
        return False
    return bool(_WELL_FORMED_PATH_RE.match(candidate))


def suppressed_deferral_snapshot_eligible(
    verdict: CopilotGateVerdict | None,
    *,
    head_changed_since_review: bool,
    unresolved_threads: int,
    suppressed_paths: Sequence[str],
    changed_files: Sequence[str],
    pr_labels: Sequence[str],
) -> bool:
    """Return ``True`` for the snapshot-only subset of the deferral conditions.

    Covers conditions 1-6 and 10, plus the PR-label half of condition 9 — every
    condition that can be decided from the PR state snapshot alone, without an
    extra API call.  Used as the cheap pre-check in ``DeferSuppressedAction.evaluate``;
    :func:`suppressed_deferral_eligible` is the authoritative predicate and calls
    this one first.

    Args:
        verdict: The Copilot gate verdict for the current HEAD.
        head_changed_since_review: Whether HEAD moved since the evaluated review.
        unresolved_threads: Effective unresolved review-thread count.
        suppressed_paths: Recovered suppressed-comment paths for this round.
        changed_files: The PR's changed-file list **as reported by the PR API**
            (not parsed from finding paths — the two disagree).
        pr_labels: Labels currently on the PR.

    Returns:
        ``True`` only when every covered condition holds.
    """
    # 1 — suppressed-only block (also excludes REASON_UNPARSED_SUPPRESSION)
    if verdict is None or verdict.passed or not is_suppressed_only_block(verdict):
        return False
    # 2 — a concrete review to attribute the deferral to
    if verdict.review_id <= 0:
        return False
    # 3 / 4 — the reviewed code is still HEAD and no real thread is outstanding
    if head_changed_since_review or unresolved_threads != 0:
        return False
    # 5 — reconciliation gate: every declared suppressed comment was recovered
    if len(suppressed_paths) != verdict.suppressed_count:
        return False
    # 6 — every recovered entry is an attributed, well-formed, non-executable path.
    # The list is guaranteed non-empty here: condition 1 requires
    # ``suppressed_count > 0`` and condition 5 pins the recovered count to it.
    for path in suppressed_paths:
        if not is_well_formed_path(path) or is_executable_path(path):
            return False
    # 10 — the diff itself contains no executable file, so no *future* round can
    # raise an executable-path finding either.  An empty file list means the PR
    # API view is unusable, which fails closed.
    if not changed_files:
        return False
    if any(is_executable_path(changed) for changed in changed_files):
        return False
    # 9 (PR half) — one generation only
    return SUPPRESSED_FOLLOW_UP_LABEL not in pr_labels


def suppressed_deferral_eligible(
    verdict: CopilotGateVerdict | None,
    *,
    head_changed_since_review: bool,
    unresolved_threads: int,
    suppressed_paths: Sequence[str],
    changed_files: Sequence[str],
    prior_executable_posted_findings: int,
    pr_labels: Sequence[str],
    linked_issue_labels: Sequence[str],
    open_deferral_count: int,
    max_open_deferrals: int,
) -> bool:
    """Return ``True`` when a suppressed-only review round may be deferred.

    Fail-closed: returns ``False`` unless **all ten** trigger conditions hold.

    1. the verdict is a suppressed-only block (no posted comments this round);
    2. ``verdict.review_id > 0``;
    3. HEAD has not changed since the evaluated review;
    4. there are no unresolved review threads;
    5. the recovered suppressed entries reconcile with the declared count;
    6. every recovered path is attributed, well-formed and non-executable;
    7. no prior round produced a posted finding on executable code;
    8. fewer than *max_open_deferrals* deferral issues are open;
    9. neither the PR nor any linked issue carries
       :data:`SUPPRESSED_FOLLOW_UP_LABEL` — the one-generation cap;
    10. the PR's changed-file list (from the PR API) contains no executable file.

    Condition 10 is what makes the executable-path guarantee structural rather
    than empirical: CCR can only comment on the diff, so an executable-free diff
    cannot produce an executable-path finding in any later round either.

    Args:
        verdict: The Copilot gate verdict for the current HEAD.
        head_changed_since_review: Whether HEAD moved since the evaluated review.
        unresolved_threads: Effective unresolved review-thread count.
        suppressed_paths: Recovered suppressed-comment paths for this round.
        changed_files: The PR's changed-file list as reported by the PR API.
        prior_executable_posted_findings: Number of posted (non-suppressed)
            findings on executable paths raised on this PR so far.
        pr_labels: Labels currently on the PR.
        linked_issue_labels: Labels on the PR's linked (closing) issues.
        open_deferral_count: Number of deferral issues currently open.
        max_open_deferrals: Circuit-breaker ceiling for open deferral issues.

    Returns:
        ``True`` only when all ten conditions hold.
    """
    if not suppressed_deferral_snapshot_eligible(
        verdict,
        head_changed_since_review=head_changed_since_review,
        unresolved_threads=unresolved_threads,
        suppressed_paths=suppressed_paths,
        changed_files=changed_files,
        pr_labels=pr_labels,
    ):
        return False
    # 7 — this PR has never produced a posted finding on executable code
    if prior_executable_posted_findings != 0:
        return False
    # 8 — circuit breaker on the open deferral backlog
    if max_open_deferrals <= 0 or open_deferral_count >= max_open_deferrals:
        return False
    # 9 (linked-issue half) — label propagation runs a cycle behind PR creation,
    # so the PR's own labels are not sufficient to detect a follow-up PR.
    return SUPPRESSED_FOLLOW_UP_LABEL not in linked_issue_labels


def suppressed_deferral_recorded(
    verdict: CopilotGateVerdict | None,
    *,
    deferred_review_id: int | None,
    head_changed_since_review: bool,
    unresolved_threads: int,
) -> bool:
    """Return ``True`` when a suppressed-only block was deferred to a follow-up issue.

    Mirrors :func:`suppressed_comments_evaluated` exactly — same fail-closed
    shape, same retained guards (``head_changed_since_review`` is ``False`` and
    ``unresolved_threads == 0``) — but clears the block on a recorded *deferral*
    for the evaluated review instead of a ``repair-satisfied`` marker.  The
    ``repair-satisfied`` evidence gate is unaffected and stays reachable for
    every suppressed-only block that was not deferred.
    """
    if verdict is None or verdict.passed:
        return False
    if not is_suppressed_only_block(verdict):
        return False
    if head_changed_since_review:
        return False
    if unresolved_threads != 0:
        return False
    if verdict.review_id <= 0:
        return False
    return deferred_review_id == verdict.review_id


def is_review_clean(snapshot: PRStateSnapshot) -> bool:
    """Return ``True`` when the Copilot review on HEAD is clean (not actionable).

    Legacy fallback used when ``snapshot.copilot_gate_verdict`` is ``None``
    (e.g. in unit tests that construct snapshots directly).

    Clean means: ``APPROVED``, or ``COMMENTED`` with 0 inline comments.
    """
    if snapshot.review_state == "APPROVED":
        return True
    if snapshot.review_state == "COMMENTED" and snapshot.copilot_review_inline_count == 0:
        return True
    return False


def copilot_review_gate_passed(
    snapshot: PRStateSnapshot,
    *,
    unresolved_threads: int,
    deferred_review_id: int | None = None,
) -> bool:
    """Return ``True`` when the Copilot review gate is satisfied on the current HEAD.

    This is the **single** definition of "the review has gone clean", so that every
    consumer evaluates exactly the same condition ``ApproveAction`` uses before it
    submits its approval:

    - when ``snapshot.copilot_gate_verdict`` is set (production path), the verdict's
      ``passed`` flag decides, with the narrowly scoped, fail-closed
      :func:`suppressed_comments_evaluated` bypass for a suppressed-only block the
      repair agent already evaluated, and the equally scoped
      :func:`suppressed_deferral_recorded` bypass for a suppressed-only block
      handed to a follow-up triage issue;
    - when the verdict is ``None`` (legacy / direct snapshot construction in tests),
      fall back to :func:`is_review_clean`.

    Args:
        snapshot: The PR state snapshot to evaluate.
        unresolved_threads: Effective unresolved review-thread count (pass the
            derived-state value so same-run thread resolution is visible).
        deferred_review_id: Review id of a recorded suppressed-comment deferral.
            Pass the derived-state value so a deferral filed in the same run is
            visible; defaults to the snapshot field when omitted.

    Returns:
        ``True`` when the gate passes; ``False`` when it still blocks.
    """
    verdict = snapshot.copilot_gate_verdict
    if verdict is None:
        return is_review_clean(snapshot)
    if verdict.passed:
        return True
    if suppressed_comments_evaluated(
        verdict,
        repair_satisfied_review_id=snapshot.repair_satisfied_review_id,
        head_changed_since_review=snapshot.head_changed_since_review,
        unresolved_threads=unresolved_threads,
    ):
        return True
    if deferred_review_id is None:
        deferred_review_id = snapshot.suppressed_deferral_review_id
    return suppressed_deferral_recorded(
        verdict,
        deferred_review_id=deferred_review_id,
        head_changed_since_review=snapshot.head_changed_since_review,
        unresolved_threads=unresolved_threads,
    )


def select_prior_actionable_reviews(reviews: list[ReviewInfo], verdict_review_id: int | None) -> list[ReviewInfo]:
    """Return actionable Copilot/synthetic reviews not already owned by the gate verdict.

    This is the **single** definition of the "which reviews count as prior" predicate.
    It is shared by the snapshot's unresolved-thread counter, the thread-resolution
    action and the repair-dispatch action so the three can never drift apart — a
    divergence there stalls the loop permanently (the snapshot would count threads
    that thread resolution never processes, so the count never reaches zero).

    Provenance is scoped to the Copilot gate verdict's ``review_id`` rather than to
    HEAD. A review is selected when it is a genuine or trusted synthetic Copilot
    review, was submitted as ``CHANGES_REQUESTED`` or ``COMMENTED``, and its id
    differs from *verdict_review_id* (the review the gate verdict already accounts
    for). This is HEAD-independent: a HEAD move that does not touch any review or
    thread (e.g. ``squash``/``takeover`` minting a new commit SHA) does not change
    the selection, unlike a HEAD-commit-SHA comparison.

    Fails closed: when provenance is unknown (``verdict_review_id`` is ``None`` or
    ``<= 0``) every actionable review is treated as prior — i.e. this degenerates
    to counting all of them, never fewer. Input order is preserved.
    """
    if verdict_review_id is None or verdict_review_id <= 0:
        return [r for r in reviews if is_copilot_or_synthetic_review(r) and r.state in _ACTIONABLE_PRIOR_REVIEW_STATES]
    return [
        r
        for r in reviews
        if is_copilot_or_synthetic_review(r)
        and r.id != verdict_review_id
        and r.state in _ACTIONABLE_PRIOR_REVIEW_STATES
    ]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def is_copilot_or_synthetic_review(review: ReviewInfo) -> bool:
    """Return ``True`` if *review* is a genuine or trusted synthetic Copilot review."""
    if is_copilot_login(review.user):
        return True
    if not isinstance(review.user, str):
        return False
    return review.user.casefold() in _TRUSTED_SYNTHETIC_USERS_CASEFOLDED and SYNTHETIC_MARKER in review.body


def _select_latest_head_review(reviews: list[ReviewInfo], head_sha: str) -> ReviewInfo | None:
    """Return the most recent Copilot/synthetic review on *head_sha*, or ``None``."""
    candidates = [r for r in reviews if r.commit_sha == head_sha and is_copilot_or_synthetic_review(r)]
    if not candidates:
        return None
    return max(candidates, key=lambda r: (r.submitted_at, r.id))


def _select_latest_prior_review(reviews: list[ReviewInfo], head_sha: str) -> ReviewInfo | None:
    """Return the most recent Copilot/synthetic review on *any commit other than* head_sha."""
    candidates = [r for r in reviews if r.commit_sha and r.commit_sha != head_sha and is_copilot_or_synthetic_review(r)]
    if not candidates:
        return None
    return max(candidates, key=lambda r: (r.submitted_at, r.id))


def _evaluate_synthetic_review(
    review: ReviewInfo,
    provider: CIPlatformProvider,
    pr_number: int,
) -> CopilotGateVerdict:
    """Evaluate a synthetic (``<!-- synthetic-copilot-review -->``) review.

    The synthetic review body contains machine-readable metadata:
    ``<!-- intended_comments=N inline_posted=N parse_failed=true/false -->``

    Fails closed on every ambiguous case, mirroring the gate workflow.
    """
    body = review.body

    # parse_failed=true → inconclusive, block.
    if re.search(r"parse_failed=true", body):
        return CopilotGateVerdict(
            passed=False,
            reason=REASON_SYNTHETIC_PARSE_FAILED,
            review_id=review.id,
            synthetic=True,
            details="Synthetic review has parse_failed=true — agent-task log parsing failed",
        )

    m_intended = re.search(r"intended_comments=(\d+)", body)
    m_inline = re.search(r"inline_posted=(\d+)", body)

    # Missing metadata → fail closed (format may have drifted).
    if not m_intended or not m_inline:
        return CopilotGateVerdict(
            passed=False,
            reason=REASON_SYNTHETIC_MISSING_METADATA,
            review_id=review.id,
            synthetic=True,
            details=(
                "Synthetic review is missing intended_comments/inline_posted metadata; "
                "re-request a Copilot review or re-run the synthetic-copilot-review workflow"
            ),
        )

    intended_comments = int(m_intended.group(1))
    inline_posted_meta = int(m_inline.group(1))

    # Intended > 0 but inline_posted == 0 → inline attachment failed, block.
    if intended_comments > 0 and inline_posted_meta == 0:
        return CopilotGateVerdict(
            passed=False,
            reason=REASON_SYNTHETIC_COMMENTS_NOT_POSTED,
            review_id=review.id,
            synthetic=True,
            details=(
                f"Synthetic review intended {intended_comments} comment(s) "
                "but posted 0 inline — inline attachment may have failed"
            ),
        )

    # Verify via API how many inline comments were actually posted.
    try:
        inline_comments = provider.list_review_comments(pr_number, review.id)
        inline_count = len(inline_comments)
    except ProviderRateLimitError:
        raise
    except Exception as exc:
        return CopilotGateVerdict(
            passed=False,
            reason=REASON_API_ERROR,
            review_id=review.id,
            synthetic=True,
            details=f"Failed to fetch inline comments for synthetic review {review.id}: {exc}",
        )

    # Metadata says comments posted but API returns 0 → possible deletion, fail closed.
    if inline_posted_meta > 0 and inline_count == 0:
        return CopilotGateVerdict(
            passed=False,
            reason=REASON_SYNTHETIC_INLINE_MISMATCH,
            review_id=review.id,
            synthetic=True,
            details=(f"Synthetic review reports inline_posted={inline_posted_meta} but API returned 0 inline comments"),
        )

    if inline_count > 0:
        return CopilotGateVerdict(
            passed=False,
            reason=REASON_SYNTHETIC_HAS_INLINE,
            review_id=review.id,
            synthetic=True,
            body_comment_count=inline_count,
            details=f"Synthetic review has {inline_count} inline comment(s) remaining",
        )

    return CopilotGateVerdict(
        passed=True,
        reason=REASON_CLEAN,
        review_id=review.id,
        synthetic=True,
        body_comment_count=0,
        details="Synthetic review: 0 inline comments — clean",
    )


def _evaluate_standard_review(
    review: ReviewInfo,
    provider: CIPlatformProvider,
    pr_number: int,
) -> CopilotGateVerdict:
    """Evaluate a standard (non-synthetic) Copilot review.

    Handles both the legacy CCR body format (``"generated N comments"``,
    ``"Suppressed (N)"``) and the new-style CCR private-preview format with a
    ``### <emoji> <verdict>`` heading and ``**Comments generated:** N new``
    metrics footer.  When the body format is unrecognised, falls back to the
    API inline comment count (fail-closed).
    """
    body = review.body

    # --- New CCR format: check verdict heading first ---
    # "### 🟡 Not ready to approve" → block immediately regardless of comment counts.
    # "### ✅ Ready to approve"      → proceed with comment-count checks below.
    new_ccr_verdict = parse_verdict(body)
    parsed_suppressed_count = parse_suppressed_count(body)
    extracted_suppressed_entries = extract_suppressed_comment_entries(body)
    extracted_suppressed_count = len(extracted_suppressed_entries)
    parsed_suppressed_without_entries = parsed_suppressed_count > 0 and extracted_suppressed_count == 0
    if new_ccr_verdict == VERDICT_NOT_APPROVE:
        suppressed_count = max(parsed_suppressed_count, extracted_suppressed_count)
        has_unrecovered_suppression = unrecovered_suppression_signal(body)
        # Also parse the self-reported posted-comment count so downstream logic can
        # distinguish a "Not ready to approve" that is blocked *solely* by suppressed
        # comments (0 posted) from one that also has real posted inline comments.
        body_comment_count = parse_reported_comment_count(body)

        # API fallback: when the body format doesn't expose a comment count (returns
        # None), use the same API inline-count fallback as the standard body-parse path.
        # This ensures is_suppressed_only_block can distinguish "0 posted" from
        # "unknown" for new-CCR reviews with unparseable metrics.
        if body_comment_count is None:
            from agentic_devtools.cli.ci.models import COPILOT_COMMENT_LOGINS  # noqa: PLC0415

            try:
                comments = provider.list_review_comments(pr_number, review.id)
                fallback_count = 0
                for c in comments:
                    cid = getattr(c, "id", None)
                    if isinstance(cid, int) and cid < 0:
                        continue  # Skip synthetic suppressed entries recovered from the review body
                    author = (getattr(c, "author_login", "") or "").strip()
                    if not author or author in COPILOT_COMMENT_LOGINS:
                        fallback_count += 1
                body_comment_count = fallback_count
            except ProviderRateLimitError:
                raise
            except Exception as exc:
                if (suppressed_count == 0 and has_unrecovered_suppression) or parsed_suppressed_without_entries:
                    return CopilotGateVerdict(
                        passed=False,
                        reason=REASON_UNPARSED_SUPPRESSION,
                        review_id=review.id,
                        body_comment_count=None,
                        suppressed_count=0,
                        details=(
                            "Review heading indicates 'Not ready to approve'; API inline-count fallback failed; "
                            "body advertises suppressed comments that could not be parsed — refusing to dispatch "
                            "repair with zero findings"
                        ),
                    )
                detail_parts = [
                    "Copilot review heading indicates 'Not ready to approve'",
                    f"API inline-count fallback failed: {exc}",
                ]
                if suppressed_count > 0:
                    detail_parts.append(f"{suppressed_count} suppressed/low-confidence comment(s)")
                return CopilotGateVerdict(
                    passed=False,
                    reason=REASON_NEW_CCR_NOT_APPROVED,
                    review_id=review.id,
                    body_comment_count=None,
                    suppressed_count=suppressed_count,
                    details="; ".join(detail_parts),
                )

        detail_parts = ["Copilot review heading indicates 'Not ready to approve'"]
        if suppressed_count > 0:
            detail_parts.append(f"{suppressed_count} suppressed/low-confidence comment(s)")
        if body_comment_count == 0 and (
            (suppressed_count == 0 and has_unrecovered_suppression) or parsed_suppressed_without_entries
        ):
            return CopilotGateVerdict(
                passed=False,
                reason=REASON_UNPARSED_SUPPRESSION,
                review_id=review.id,
                body_comment_count=body_comment_count,
                suppressed_count=0,
                details=(
                    "Review heading indicates 'Not ready to approve' and body advertises "
                    "suppressed comments that could not be parsed — refusing to dispatch repair with zero findings"
                ),
            )
        return CopilotGateVerdict(
            passed=False,
            reason=REASON_NEW_CCR_NOT_APPROVED,
            review_id=review.id,
            body_comment_count=body_comment_count,
            suppressed_count=suppressed_count,
            details="; ".join(detail_parts),
        )

    body_comment_count = parse_reported_comment_count(body)
    suppressed_count = max(parsed_suppressed_count, extracted_suppressed_count)

    if body_comment_count is None:
        # Body format unrecognised — fall back to the API inline count.
        # Count only Copilot-authored (or missing-author) comments so human replies
        # on the same review don't incorrectly block the gate.
        from agentic_devtools.cli.ci.models import COPILOT_COMMENT_LOGINS  # noqa: PLC0415

        try:
            comments = provider.list_review_comments(pr_number, review.id)
            fallback_count = 0
            for c in comments:
                cid = getattr(c, "id", None)
                if isinstance(cid, int) and cid < 0:
                    continue  # Skip synthetic suppressed entries recovered from the review body
                author = (getattr(c, "author_login", "") or "").strip()
                if not author or author in COPILOT_COMMENT_LOGINS:
                    fallback_count += 1
        except ProviderRateLimitError:
            raise
        except Exception as exc:
            return CopilotGateVerdict(
                passed=False,
                reason=REASON_API_ERROR,
                review_id=review.id,
                details=(
                    f"Could not parse review body and failed to fetch inline "
                    f"comment count for review {review.id}: {exc}"
                ),
            )
        posted_count = fallback_count
    else:
        posted_count = body_comment_count

    total = posted_count + suppressed_count

    if total == 0 and unrecovered_suppression_signal(body):
        # The body advertises suppressed comments in a wrapper the structured
        # parser does not recognise.  Refuse to conclude clean (fail closed)
        # rather than merging with unaddressed findings.
        return CopilotGateVerdict(
            passed=False,
            reason=REASON_UNPARSED_SUPPRESSION,
            review_id=review.id,
            body_comment_count=body_comment_count,
            suppressed_count=0,
            details=(
                "Review body advertises suppressed comments that could not be parsed — refusing to conclude clean"
            ),
        )

    if parsed_suppressed_without_entries and posted_count == 0:
        return CopilotGateVerdict(
            passed=False,
            reason=REASON_UNPARSED_SUPPRESSION,
            review_id=review.id,
            body_comment_count=body_comment_count,
            suppressed_count=0,
            details=(
                "Review body declares suppressed comments but no recoverable suppressed entries were found — "
                "refusing to dispatch repair with zero findings"
            ),
        )

    if total == 0:
        return CopilotGateVerdict(
            passed=True,
            reason=REASON_CLEAN,
            review_id=review.id,
            body_comment_count=body_comment_count,
            suppressed_count=0,
            details="Review reports 0 comments — clean",
        )

    if suppressed_count > 0 and posted_count == 0:
        return CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=review.id,
            body_comment_count=body_comment_count,
            suppressed_count=suppressed_count,
            details=(
                f"Review has {suppressed_count} suppressed/low-confidence comment(s) "
                "that must be addressed before merge"
            ),
        )

    return CopilotGateVerdict(
        passed=False,
        reason=REASON_HAS_COMMENTS,
        review_id=review.id,
        body_comment_count=body_comment_count,
        suppressed_count=suppressed_count,
        details=(f"Review reports {posted_count} comment(s) posted (suppressed: {suppressed_count})"),
    )


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def evaluate_copilot_gate_verdict(
    reviews: list[ReviewInfo],
    head_sha: str,
    pr_number: int,
    provider: CIPlatformProvider,
    base_branch: str = "main",
) -> CopilotGateVerdict:
    """Evaluate the Copilot gate verdict for a pull request.

    Implements the same safety logic as ``.github/workflows/copilot-review-gate.yml``.
    Fails closed on every ambiguous, unparseable, or API-error case.

    Algorithm:

    1. Look for the latest trusted Copilot review on *head_sha* (trivially fresh).
    2. If none on HEAD: look for a prior-commit review and verify the PR diff
       content-hash has not changed (``origin/{base}...{sha}``).  If hashes match,
       treat the prior review as the effective review and record its commit SHA in
       the verdict's ``carried_over_sha``.  If they differ or the comparison fails,
       block.
    3. Parse the effective review body for posted comment count and suppressed count.
    4. Handle synthetic reviews via their machine-readable metadata.
    5. Return a :class:`CopilotGateVerdict` — ``passed=True`` means clean; any
       other outcome blocks approval/merge.

    Args:
        reviews: All reviews for the PR (e.g., from ``provider.list_reviews``).
        head_sha: Current HEAD commit SHA.
        pr_number: Pull request number.
        provider: CI platform provider; must expose ``list_review_comments``.
            Optionally exposes ``compute_diff_hash(base_branch, sha)`` for the
            content-hash freshness check.
        base_branch: Base branch for the diff comparison (default: ``"main"``).

    Returns:
        A :class:`CopilotGateVerdict` with ``passed=True`` when the gate is
        satisfied, or ``passed=False`` with a diagnostic ``reason`` and ``details``.
    """
    # --- Step 1: find the latest trusted review on HEAD ---
    head_review = _select_latest_head_review(reviews, head_sha)
    carried_over_sha = ""

    if head_review is None:
        # --- Step 2: content-hash freshness check on prior reviews ---
        prior_review = _select_latest_prior_review(reviews, head_sha)

        if prior_review is None:
            return CopilotGateVerdict(
                passed=False,
                reason=REASON_AWAITING_FRESH,
                details="No Copilot review found for this PR — request a review from Copilot",
            )

        approved_sha = prior_review.commit_sha
        if not re.match(r"^[0-9a-fA-F]{40}$", approved_sha, re.IGNORECASE):
            return CopilotGateVerdict(
                passed=False,
                reason=REASON_AWAITING_FRESH,
                details=(f"Unable to verify review freshness — invalid reviewed commit SHA: {approved_sha!r}"),
            )

        # Use the optional compute_diff_hash provider method.
        compute_diff_hash = getattr(provider, "compute_diff_hash", None)
        if not callable(compute_diff_hash):
            return CopilotGateVerdict(
                passed=False,
                reason=REASON_AWAITING_FRESH,
                details=(
                    f"No Copilot review on HEAD ({head_sha[:12]}) and provider "
                    "does not support diff-hash comparison — request a new review"
                ),
            )

        try:
            approved_hash: str | None = compute_diff_hash(base_branch=base_branch, sha=approved_sha)
            head_hash: str | None = compute_diff_hash(base_branch=base_branch, sha=head_sha)
        except Exception as exc:
            return CopilotGateVerdict(
                passed=False,
                reason=REASON_API_ERROR,
                details=f"Failed to compute diff hashes for freshness check: {exc}",
            )

        if approved_hash is None or head_hash is None:
            return CopilotGateVerdict(
                passed=False,
                reason=REASON_AWAITING_FRESH,
                details="Could not compute diff hashes for freshness check — request a new review",
            )

        if approved_hash != head_hash:
            return CopilotGateVerdict(
                passed=False,
                reason=REASON_CONTENT_CHANGED,
                review_id=prior_review.id,
                details=(
                    f"PR diff content changed since Copilot review on "
                    f"{approved_sha[:12]} — code was modified; request a new review"
                ),
            )

        # Content hash matches — the prior review is still valid (rebase-only change).
        head_review = prior_review
        carried_over_sha = approved_sha

    # --- Step 3 & 4: evaluate the effective review ---
    is_synthetic = is_copilot_or_synthetic_review(head_review) and not is_copilot_login(head_review.user)

    if is_synthetic:
        verdict = _evaluate_synthetic_review(head_review, provider, pr_number)
    else:
        verdict = _evaluate_standard_review(head_review, provider, pr_number)

    if carried_over_sha:
        # Record that the evaluated review targets a prior commit whose diff content is
        # identical to HEAD, so consumers (e.g. RequestReviewAction) can tell an
        # unchanged-diff carry-over apart from a review submitted against HEAD.
        return replace(verdict, carried_over_sha=carried_over_sha)
    return verdict
