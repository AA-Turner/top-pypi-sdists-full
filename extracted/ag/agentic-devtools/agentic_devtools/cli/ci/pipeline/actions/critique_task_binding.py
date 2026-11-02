"""Bind confirmed Agent Task receipts to durable critique markers."""

from __future__ import annotations

import logging
import re
from collections.abc import Callable

from agentic_devtools.cli.ci.critique_adjudicator import (
    build_critique_task_comment,
    build_critique_task_id_marker,
    parse_critique_tasks,
)
from agentic_devtools.cli.ci.models import ReviewCommentInfo
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.repair_attempts import RepairAttemptTracker
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot
from agentic_devtools.cli.ci.provider import CIPlatformProvider, trusted_loop_comment_logins
from agentic_devtools.cli.ci.repair_accounting import RepairDispatchLedger, repair_work_key
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

logger = logging.getLogger(__name__)


def critique_task_id_from_receipt(receipt: int | str, repository_full_name: str) -> str | None:
    """Extract a validated Agent Task ID from its stable dispatch receipt."""
    if not isinstance(receipt, str):
        return None
    prefix = f"task:{repository_full_name}:"
    if not receipt.startswith(prefix):
        return None
    task_id = receipt[len(prefix) :]
    return task_id if re.fullmatch(r"[A-Za-z0-9_-]+", task_id) else None


def bind_critique_task_id(
    provider: CIPlatformProvider,
    snapshot: PRStateSnapshot,
    marker: tuple[int, int, int] | None,
    task_id: str,
) -> None:
    """Persist and verify the task ID against its pre-dispatch critique marker."""
    if marker is None:
        raise ValueError("critique task marker is required")
    comment_id, review_id, attempt = marker
    body = (
        build_critique_task_comment(snapshot.pr_number, snapshot.head_sha, review_id, attempt)
        + "\n"
        + build_critique_task_id_marker(task_id)
    )
    provider.update_comment_as_pr_token(comment_id, body)
    persisted = provider.find_comment(snapshot.pr_number, body.splitlines()[0])
    if persisted != (comment_id, body):
        raise RuntimeError("Critique task ID marker could not be verified")


def bind_dispatched_critique_task(
    provider: CIPlatformProvider,
    snapshot: PRStateSnapshot,
    marker: tuple[int, int, int] | None,
    receipt: int | str,
    action_name: str,
) -> ActionResult | None:
    """Bind a confirmed task receipt, retrying a transient marker write once."""
    if marker is None:
        return None
    task_id = critique_task_id_from_receipt(receipt, snapshot.base_repo_full_name)
    if task_id is None:
        return ActionResult(
            name=action_name,
            decision=ActionDecision.FAILED,
            error="Agent Tasks receipt did not contain a verifiable task ID",
            details="Repair dispatched but its critique task lifecycle marker could not be verified",
        )
    attempt = 0
    while True:
        try:
            bind_critique_task_id(provider, snapshot, marker, task_id)
            return None
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            if attempt:
                return ActionResult(
                    name=action_name,
                    decision=ActionDecision.FAILED,
                    error=str(exc),
                    details="Repair dispatched but its critique task lifecycle marker could not be verified",
                )
            attempt += 1


def record_receipt_and_bind_critique_task(
    ledger: RepairDispatchLedger,
    provider: CIPlatformProvider,
    snapshot: PRStateSnapshot,
    marker: tuple[int, int, int] | None,
    receipt: int | str,
    action_name: str,
    *,
    suppress_binding_errors: bool = False,
) -> tuple[Exception | None, ActionResult | None]:
    """Attempt durable receipt recording and task binding without discarding either failure."""
    accounting_error = None
    try:
        ledger.record(receipt)
    except Exception as exc:
        accounting_error = exc
        logger.error(
            "PR #%d: Confirmed repair receipt %s could not be persisted: %s",
            snapshot.pr_number,
            receipt,
            exc,
        )
    try:
        binding_failure = bind_dispatched_critique_task(provider, snapshot, marker, receipt, action_name)
    except Exception as exc:
        if not suppress_binding_errors:
            raise
        logger.error(
            "PR #%d: Confirmed repair receipt %s could not be bound to its critique marker: %s",
            snapshot.pr_number,
            receipt,
            exc,
        )
        binding_failure = None
    if binding_failure is not None:
        logger.error(
            "PR #%d: Confirmed repair receipt %s could not be bound to its critique marker: %s",
            snapshot.pr_number,
            receipt,
            binding_failure.error,
        )
    return accounting_error, binding_failure


def confirmed_receipt_accounting_failure(
    action_name: str,
    receipt: int | str,
    accounting_error: Exception,
    binding_failure: ActionResult | None,
) -> ActionResult:
    """Return the failed accounting outcome after preserving the task binding result."""
    if isinstance(accounting_error, ProviderRateLimitError) and accounting_error.is_rate_limit:
        raise accounting_error
    details = (
        f"Repair dispatched (receipt={receipt}); accounting unresolved: {accounting_error}. "
        "Reconcile authentic task/trigger evidence before any replacement."
    )
    if binding_failure is not None:
        details += f" Critique task binding also needs reconciliation: {binding_failure.error}"
    return ActionResult(
        name=action_name,
        decision=ActionDecision.EXECUTE,
        error=str(accounting_error),
        details=details,
    )


def reconcile_dispatched_critique_task_binding(
    provider: CIPlatformProvider,
    snapshot: PRStateSnapshot,
    attempted: set[str],
    receipts: set[str],
    action_name: str,
) -> ActionResult | None:
    """Retry binding an unbound critique marker from its persisted task receipt."""
    from agentic_devtools.cli.ci.pipeline.actions.critique_dispatch import critique_headline

    critique = critique_headline(snapshot)
    if critique is None:
        return None
    review_id, _headline = critique
    attempts = {
        int(match[1]) for key in attempted if (match := re.fullmatch(rf"critique:{review_id}:([12])", key)) is not None
    }
    if not attempts:
        return None
    comments = provider.list_issue_comments(snapshot.pr_number)
    trusted_logins = trusted_loop_comment_logins(provider)
    tasks = parse_critique_tasks(
        comments,
        trusted_logins=trusted_logins,
        pr_number=snapshot.pr_number,
        head_sha=snapshot.head_sha,
    )
    matching_tasks = [task for task in tasks if task.review_id == review_id and task.attempt in attempts]
    unbound_tasks = [task for task in matching_tasks if not task.task_id]
    if not unbound_tasks:
        return None
    task_ids = {
        task_id
        for receipt in receipts
        if (task_id := critique_task_id_from_receipt(receipt, snapshot.base_repo_full_name)) is not None
    } - {task.task_id for task in matching_tasks if task.task_id}
    if not task_ids:
        return None
    if len(unbound_tasks) != 1 or len(task_ids) != 1:
        return ActionResult(
            name=action_name,
            decision=ActionDecision.FAILED,
            error="Could not uniquely reconcile the critique task receipt with its marker",
            details="Confirmed task receipts remain durable; retry reconciliation before any replacement dispatch",
        )
    task = unbound_tasks[0]
    marker_header = build_critique_task_comment(
        snapshot.pr_number,
        snapshot.head_sha,
        task.review_id,
        task.attempt,
    ).splitlines()[0]
    matching_comments = [
        comment
        for comment in comments
        if isinstance(getattr(comment, "author", None), str)
        and comment.author.casefold() in trusted_logins
        and isinstance(getattr(comment, "body", None), str)
        and comment.body.splitlines()[0:1] == [marker_header]
    ]
    if len(matching_comments) != 1 or type(getattr(matching_comments[0], "id", None)) is not int:
        return ActionResult(
            name=action_name,
            decision=ActionDecision.FAILED,
            error="Could not uniquely identify the persisted critique task marker",
            details="Confirmed task receipts remain durable; retry reconciliation before any replacement dispatch",
        )
    receipt = f"task:{snapshot.base_repo_full_name}:{next(iter(task_ids))}"
    return bind_dispatched_critique_task(
        provider,
        snapshot,
        (matching_comments[0].id, review_id, task.attempt),
        receipt,
        action_name,
    )


def reconcile_existing_critique_task_binding(
    provider: CIPlatformProvider,
    snapshot: PRStateSnapshot,
    attempted: set[str],
    ledger: RepairDispatchLedger,
    action_name: str,
) -> ActionResult | None:
    """Load persisted receipts only when an eligible critique attempt needs reconciliation."""
    from agentic_devtools.cli.ci.pipeline.actions.critique_dispatch import critique_headline

    if critique_headline(snapshot) is None or not any(
        re.fullmatch(r"critique:[1-9]\d*:[12]", key) for key in attempted
    ):
        return None
    receipts, _pending, _comment_id = ledger.read()
    return reconcile_dispatched_critique_task_binding(provider, snapshot, attempted, receipts, action_name)


def reconcile_ledger_task_binding(
    provider: CIPlatformProvider,
    snapshot: PRStateSnapshot,
    attempted: set[str],
    ledger: RepairDispatchLedger,
    action_name: str,
) -> ActionResult | None:
    """Reconcile accounting before retrying a persisted critique task binding."""
    ledger.reconcile()
    return reconcile_existing_critique_task_binding(provider, snapshot, attempted, ledger, action_name)


def reconcile_before_attempt_skip(
    provider: CIPlatformProvider,
    snapshot: PRStateSnapshot,
    attempted: set[str],
    review_id: int,
    unresolved_comments: list[ReviewCommentInfo],
    unresolved_shortfall: int,
    body_only_work: bool,
    action_name: str,
) -> ActionResult | None:
    """Reconcile a prior critique receipt before an attempt-planning early exit."""
    from agentic_devtools.cli.ci.pipeline.actions.critique_dispatch import critique_headline

    critique = critique_headline(snapshot)
    if (
        not body_only_work
        or critique is None
        or critique[0] != review_id
        or not any(re.fullmatch(rf"critique:{review_id}:[12]", key) for key in attempted)
    ):
        return None
    author_count = sum(comment.id < 0 for comment in unresolved_comments) + unresolved_shortfall
    shortfalls = {review_id: author_count} if author_count > 0 else {}
    work_key = repair_work_key(review_id, unresolved_comments, [], shortfalls)
    ledger = RepairDispatchLedger(provider, snapshot.pr_number, snapshot.head_sha, review_id, work_key)
    return reconcile_ledger_task_binding(provider, snapshot, attempted, ledger, action_name)


def register_attempt_and_reconcile(
    provider: CIPlatformProvider,
    snapshot: PRStateSnapshot,
    attempted: set[str],
    review_id: int,
    body_only_work: bool,
    stuck_prior_threads: bool,
    attempts_tracker: RepairAttemptTracker,
    review_keys: set[str],
    finding_aware: bool,
    shortfall: int,
    duplicate_trigger: Callable[..., bool],
    unresolved_comments: list[ReviewCommentInfo],
    unresolved_shortfall: int,
    action_name: str,
) -> tuple[ActionResult | None, int]:
    """Register review work and reconcile a critique task before returning an early result."""
    from agentic_devtools.cli.ci.pipeline.actions.critique_dispatch import register_review_attempt

    attempt_result, shortfall = register_review_attempt(
        action_name,
        snapshot,
        review_id,
        body_only_work,
        stuck_prior_threads,
        attempts_tracker,
        review_keys,
        provider,
        finding_aware,
        shortfall,
        duplicate_trigger,
    )
    if attempt_result is None:
        return None, shortfall
    binding_failure = reconcile_before_attempt_skip(
        provider,
        snapshot,
        attempted,
        review_id,
        unresolved_comments,
        unresolved_shortfall,
        body_only_work,
        action_name,
    )
    return (binding_failure if binding_failure is not None else attempt_result), shortfall
