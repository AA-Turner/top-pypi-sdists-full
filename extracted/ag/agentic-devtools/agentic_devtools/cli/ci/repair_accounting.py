"""Confirmed repair receipts, independent of the canonical SHA ordinal budget.

The caller holds the existing per-PR workflow lock. Pending intent is durable
before crossing the provider boundary; an uncertain write never permits a
replacement merely because the successful-receipt write failed.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from agentic_devtools.cli.ci.comment_format import normalize_ai_pr_loop_comment
from agentic_devtools.cli.ci.models import CheckRunStatus, IssueCommentInfo, ReviewCommentInfo
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.ci.review_thread_state import fetch_review_thread_states
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

if TYPE_CHECKING:
    from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot


def repair_observation_key(provider: CIPlatformProvider, snapshot: PRStateSnapshot) -> str:
    """Fingerprint actionable inventory for narrowly suppressing exhausted wakeups."""
    from agentic_devtools.cli.ci.pipeline.actions.dispatch_repair import (
        _actionable_copilot_review_id,
        _declared_suppressed_counts_by_review,
        _filter_repair_comments,
        _list_repairable_copilot_reviews,
    )

    review_id = _actionable_copilot_review_id(snapshot)
    review_ids = sorted({review.id for review in _list_repairable_copilot_reviews(snapshot)} | {review_id} - {0})
    thread_states = fetch_review_thread_states(provider, snapshot.pr_number)
    if thread_states.degraded:
        raise RuntimeError("Cannot confirm unchanged exhausted work without thread inventory")
    resolved = {comment_id for comment_id, state in thread_states.states.items() if state[0]}
    work = []
    for source in review_ids:
        comments = _filter_repair_comments(provider.list_review_comments(snapshot.pr_number, source), resolved)
        work.append((source, repair_work_key(source, comments, [])))
    checks = [check for check in snapshot.check_runs if check.name in snapshot.ci_failed_checks]
    observation = [
        snapshot.head_sha,
        review_id,
        snapshot.copilot_review_id,
        snapshot.ci_status,
        sorted(set(snapshot.ci_failed_checks)),
        snapshot.repairable_threads,
        snapshot.effective_review_comment_count,
        work,
        sorted(_declared_suppressed_counts_by_review(snapshot, review_ids).items()),
        repair_work_key(0, [], checks),
    ]
    return hashlib.sha256(json.dumps(observation, separators=(",", ":")).encode()).hexdigest()


def repair_hold_observation_key(provider: CIPlatformProvider, snapshot: PRStateSnapshot) -> str:
    """Fingerprint available work identities when thread-state fingerprinting is degraded."""
    from agentic_devtools.cli.ci.pipeline.actions.dispatch_repair import _actionable_copilot_review_id

    reviews = {review.id: (review.state, review.body) for review in snapshot.reviews}
    review_ids = sorted((set(reviews) | {_actionable_copilot_review_id(snapshot)}) - {0})
    review_work = []
    for review_id in review_ids:
        roots = sorted(
            (
                comment.source_review_id or review_id,
                comment.id,
                comment.path,
                comment.body,
            )
            for comment in provider.list_review_comments(snapshot.pr_number, review_id)
            if comment.in_reply_to_id is None
        )
        review_work.append([review_id, reviews.get(review_id, ("", "")), roots])
    failed_check_names = set(snapshot.ci_failed_checks)
    checks = sorted(
        (check.app_slug, check.name, check.status, check.conclusion)
        for check in snapshot.check_runs
        if check.name in failed_check_names
    )
    observation = [
        snapshot.head_sha,
        _actionable_copilot_review_id(snapshot),
        snapshot.copilot_review_id,
        snapshot.review_state,
        snapshot.ci_status,
        sorted(failed_check_names),
        snapshot.effective_review_comment_count,
        review_work,
        checks,
    ]
    return hashlib.sha256(json.dumps(observation, separators=(",", ":")).encode()).hexdigest()


def exhausted_repair_is_unchanged(provider: CIPlatformProvider, pr_number: int, head_sha: str) -> bool:
    """Suppress only an authentic summary's unchanged exhausted work inventory."""
    from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
    from agentic_devtools.cli.ci.pipeline.summary import SUMMARY_SENTINEL

    comments = authentic_repair_comments(provider, pr_number, include_workflow_summaries=True)
    pattern = re.compile(r"<!-- repair-dispatch:exhausted:([^:]+):([a-f0-9]{64}) -->")
    hold_pattern = re.compile(r"<!-- repair-dispatch:exhausted-hold:([^:]+):([a-f0-9]{64}|unavailable) -->")
    for comment in sorted(comments, key=lambda item: item.id, reverse=True):
        if not comment.body.startswith(SUMMARY_SENTINEL):
            continue
        match = pattern.search(comment.body)
        if match is None:
            hold_match = hold_pattern.search(comment.body)
            if hold_match is None or hold_match.group(1) != head_sha:
                return False
            try:
                snapshot = build_pr_state_snapshot(provider, pr_number, promote_findings=False)
                if snapshot.head_sha != head_sha:
                    return False
                from agentic_devtools.cli.ci.pipeline.gate_verdict import copilot_review_gate_passed

                if (
                    not snapshot.unresolved_threads_degraded
                    and snapshot.ci_status != "failing"
                    and snapshot.repairable_threads == 0
                    and snapshot.unresolved_threads == 0
                    and copilot_review_gate_passed(snapshot, unresolved_threads=snapshot.unresolved_threads)
                ):
                    return False
                observation = repair_hold_observation_key(provider, snapshot)
                if hold_match.group(2) == "unavailable":
                    return False
                try:
                    repair_observation_key(provider, snapshot)
                except Exception as exc:
                    if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                        raise
                else:
                    return False
                return observation == hold_match.group(2)
            except Exception as exc:
                if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                    raise
                return True
        if match.group(1) != head_sha:
            return False
        snapshot = build_pr_state_snapshot(provider, pr_number, promote_findings=False)
        if snapshot.head_sha != head_sha:
            return False
        from agentic_devtools.cli.ci.pipeline.gate_verdict import copilot_review_gate_passed

        if (
            not snapshot.unresolved_threads_degraded
            and snapshot.ci_status != "failing"
            and snapshot.repairable_threads == 0
            and snapshot.unresolved_threads == 0
            and copilot_review_gate_passed(snapshot, unresolved_threads=snapshot.unresolved_threads)
        ):
            return False
        return repair_observation_key(provider, snapshot) == match.group(2)
    return False


def repair_work_key(
    review_id: int,
    comments: list[ReviewCommentInfo],
    checks: list[CheckRunStatus],
    shortfalls: dict[int, int] | None = None,
) -> str:
    """Hash canonical root/source pairs and stable check identities, not run IDs."""
    roots = sorted(
        {
            (comment.source_review_id or review_id, comment.in_reply_to_id or comment.id)
            for comment in comments
            if comment.in_reply_to_id is None
        }
    )
    failures = sorted({(check.app_slug, check.name) for check in checks})
    payload = [roots, failures, sorted((shortfalls or {}).items())]
    return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


def authentic_repair_comments(
    provider: CIPlatformProvider, pr_number: int, *, include_workflow_summaries: bool = False
) -> list[IssueCommentInfo]:
    """Use the resolved dispatch credential identity; unknown identity fails closed."""
    login = provider.get_pr_token_login()
    if not isinstance(login, str) or not login:
        raise RuntimeError("Cannot authenticate repair accounting identity")
    return [
        comment
        for comment in provider.list_issue_comments(pr_number)
        if comment.author.casefold() == login.casefold()
        or (
            include_workflow_summaries
            and comment.author.casefold() == "github-actions[bot]"
            and comment.body.startswith("<!-- agdt:ai-pr-loop-summary -->")
        )
    ]


@dataclass
class RepairDispatchLedger:
    """One HEAD/effective-review/work scope, persisted as a receipt set.

    Legacy trigger comments without a work digest are not imported because they
    cannot be attributed to a modern work scope.
    """

    provider: CIPlatformProvider
    pr_number: int
    head_sha: str
    review_id: int
    work_key: str
    _pending_after: int = field(default=0, init=False)
    _trigger: str = field(default="", init=False)
    _comment_ids: list[int] = field(default_factory=list, init=False)

    @property
    def scope(self) -> str:
        return f"{self.head_sha}:{self.review_id}:{self.work_key}"

    @property
    def marker(self) -> str:
        return f"<!-- repair-dispatch:v2:{self.scope} -->"

    def read(self, comments: list[IssueCommentInfo] | None = None) -> tuple[set[str], bool, int | None]:
        """Read authentic receipts and unresolved intent without any provider write."""
        if comments is None:
            comments = authentic_repair_comments(self.provider, self.pr_number)
        receipts: set[str] = set()
        pending = False
        comment_id = None
        self._pending_after = 0
        self._trigger = ""
        self._comment_ids = []
        for comment in sorted(comments, key=lambda item: item.id):
            if comment.body.startswith(self.marker + "\n"):
                lines = comment.body.split("\n", 2)
                data = json.loads(lines[1])
                if (
                    not isinstance(data, dict)
                    or set(data) != {"receipts", "pending", "after"}
                    or not isinstance(data["receipts"], list)
                    or any(not isinstance(value, str) or not value for value in data["receipts"])
                    or type(data["pending"]) is not bool
                    or type(data["after"]) is not int
                ):
                    raise RuntimeError("Invalid repair accounting record; reconcile before dispatch")
                receipts.update(data["receipts"])
                pending = pending or data["pending"]
                self._pending_after = max(self._pending_after, data["after"])
                self._trigger = lines[2] if len(lines) > 2 else self._trigger
                self._comment_ids.append(comment.id)
                comment_id = comment.id
            # Embedded evidence belongs to the *created repair comment*, not a
            # quoted marker or an optional bookkeeping reply.
            normalized_body = normalize_ai_pr_loop_comment(comment.body)
            if (
                normalized_body is not None
                and normalized_body.startswith("@copilot")
                and normalized_body.rstrip().splitlines()[-1:] == [self.evidence_marker]
            ):
                receipts.add(f"comment-{comment.id}")
        return receipts, pending, comment_id

    @property
    def evidence_marker(self) -> str:
        return f"<!-- repair-dispatch:work:{self.scope} -->"

    @property
    def no_creation_marker(self) -> str:
        return f"<!-- repair-dispatch:no-creation:v1:{self.scope} -->"

    def _write(self, receipts: set[str], pending: bool, comment_id: int | None) -> None:
        body = (
            self.marker
            + "\n"
            + json.dumps(
                {
                    "receipts": sorted(receipts),
                    "pending": pending,
                    "after": (
                        max(
                            (comment.id for comment in authentic_repair_comments(self.provider, self.pr_number)),
                            default=0,
                        )
                        if pending
                        else 0
                    ),
                },
                sort_keys=True,
            )
        )
        if receipts and self.review_id > 0:
            trigger = (
                self._trigger
                if pending
                else f"<!-- copilot-trigger:{self.review_id}:{datetime.now(UTC).isoformat()} -->"
            )
            body += f"\n{trigger}"
        if comment_id is None:
            self.provider.post_comment_as_pr_token(self.pr_number, body)
        else:
            for duplicate_id in self._comment_ids:
                self.provider.update_comment_as_pr_token(duplicate_id, body)

    def begin(self) -> None:
        """Persist intent before creation; unresolved intent must be reconciled first."""
        receipts, pending, comment_id = self.read()
        for comment in authentic_repair_comments(self.provider, self.pr_number):
            if comment.body.startswith("<!-- repair-dispatch:v2:") and not comment.body.startswith(self.marker):
                other = json.loads(comment.body.split("\n", 2)[1])
                if not isinstance(other, dict) or other.get("pending") is not False:
                    raise RuntimeError("Unresolved prior repair scope; reconcile creation evidence before retry")
        if pending:
            raise RuntimeError("Unresolved repair creation; reconcile authentic task/trigger evidence before retry")
        self._write(receipts, True, comment_id)
        _, persisted, _ = self.read()
        if not persisted:
            raise RuntimeError("Repair intent persistence could not be confirmed")

    def record(self, receipt: int | str) -> int:
        """Record one confirmed creation, idempotently, after the provider returns."""
        if isinstance(receipt, bool) or not isinstance(receipt, (int, str)) or not receipt:
            raise ValueError("A confirmed repair creation receipt is required")
        if isinstance(receipt, int) and receipt < 1:
            raise ValueError("A confirmed repair creation receipt is required")
        identity = f"comment-{receipt}" if isinstance(receipt, int) else receipt
        receipts, pending, comment_id = self.read()
        if identity in receipts and not pending:
            return len(receipts)
        receipts.add(identity)
        self._write(receipts, False, comment_id)
        persisted, still_pending, _ = self.read()
        if not receipts <= persisted or still_pending:
            raise RuntimeError("Confirmed repair creation accounting persistence failed; reconcile before retry")
        return len(persisted)

    def retire_pending(self) -> None:
        """Clear intent after a confirmed pre-creation failure."""
        receipts, pending, comment_id = self.read()
        if not pending:
            return
        comments = authentic_repair_comments(self.provider, self.pr_number)
        if not any(
            comment.id > self._pending_after and comment.body == self.no_creation_marker for comment in comments
        ):
            self.provider.post_comment_as_pr_token(self.pr_number, self.no_creation_marker)
            comments = authentic_repair_comments(self.provider, self.pr_number)
            if not any(
                comment.id > self._pending_after and comment.body == self.no_creation_marker for comment in comments
            ):
                raise RuntimeError("Confirmed no-creation evidence could not be persisted")
        self._write(receipts, False, comment_id)
        _, pending, _ = self.read()
        if pending:
            raise RuntimeError("Pre-creation repair intent retirement could not be confirmed")

    def reconcile(self) -> None:
        """Reconcile authentic pending scopes before considering a replacement."""
        pattern = re.compile(r"^<!-- repair-dispatch:v2:([^:]+):(\d+):([^ >]+) -->\n")
        comments = authentic_repair_comments(self.provider, self.pr_number)
        for comment in comments:
            match = pattern.match(comment.body)
            if match is not None and comment.body.split("\n", 1)[0] != self.marker:
                prior = RepairDispatchLedger(
                    self.provider, self.pr_number, match.group(1), int(match.group(2)), match.group(3)
                )
                _, pending, _ = prior.read(comments)
                if pending:
                    prior._reconcile_pending()
        _, pending, _ = self.read(comments)
        if pending:
            self._reconcile_pending()

    def _reconcile_pending(self) -> None:
        """Retire intent only with new authentic scoped creation or no-creation evidence."""
        receipts, pending, comment_id = self.read()
        if not pending:
            return
        comments = authentic_repair_comments(self.provider, self.pr_number)
        if any(comment.id > self._pending_after and comment.body == self.no_creation_marker for comment in comments):
            self._write(receipts, False, comment_id)
            _, still_pending, _ = self.read()
            if still_pending:
                raise RuntimeError("Confirmed no-creation reconciliation persistence failed")
            return
        evidence = {
            f"comment-{comment.id}"
            for comment in comments
            if comment.id > self._pending_after
            and (normalized_body := normalize_ai_pr_loop_comment(comment.body)) is not None
            and normalized_body.startswith("@copilot")
            and normalized_body.rstrip().splitlines()[-1:] == [self.evidence_marker]
        }
        if not evidence:
            raise RuntimeError("Unresolved repair creation; inspect task/trigger evidence before human recovery")
        self._write(receipts | evidence, False, comment_id)
        _, pending, _ = self.read()
        if pending:
            raise RuntimeError("Repair creation reconciliation persistence failed")
