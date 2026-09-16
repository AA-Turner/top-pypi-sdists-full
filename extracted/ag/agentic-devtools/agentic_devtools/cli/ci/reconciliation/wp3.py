"""Verified disposition and durable external effects for AI PR Loop WP3."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol


class Disposition(StrEnum):
    """Canonical finding dispositions."""

    IMPLEMENT_SUGGESTION = "implement_suggestion"
    IMPLEMENT_BETTER_FIX = "implement_better_fix"
    REJECT_WITH_EVIDENCE = "reject_with_evidence"
    DEFER_WITH_FOLLOWUP = "defer_with_followup"


@dataclass(frozen=True)
class DispositionEvidence:
    """Immutable, independently verified facts for one finding."""

    disposition: Disposition
    finding_id: str
    head_sha: str
    source_revision: str
    verified: bool
    code_changed: bool = False
    evidence: str = ""
    blocking: bool = False
    followup_issue_id: int | None = None


@dataclass(frozen=True)
class DispositionDecision:
    """Conservative disposition decision."""

    disposition: Disposition | None
    accepted: bool
    reason: str


def evaluate_disposition(
    evidence: DispositionEvidence,
    *,
    current_head_sha: str,
    current_source_revision: str,
) -> DispositionDecision:
    """Accept a disposition only when its independent evidence is current."""
    if not isinstance(evidence, DispositionEvidence):
        raise TypeError("typed disposition evidence is required")
    if not evidence.verified:
        return DispositionDecision(None, False, "independent verification is missing")
    if not all(
        isinstance(value, str) and value.strip()
        for value in (evidence.finding_id, evidence.head_sha, evidence.source_revision)
    ):
        return DispositionDecision(None, False, "disposition evidence is malformed")
    if evidence.head_sha != current_head_sha or evidence.source_revision != current_source_revision:
        return DispositionDecision(None, False, "disposition evidence is stale")
    if evidence.disposition is Disposition.DEFER_WITH_FOLLOWUP and evidence.blocking:
        return DispositionDecision(None, False, "blocking findings cannot be deferred")
    if evidence.disposition is Disposition.REJECT_WITH_EVIDENCE and not evidence.evidence.strip():
        return DispositionDecision(None, False, "rejection evidence is missing")
    if (
        evidence.disposition
        in {
            Disposition.IMPLEMENT_SUGGESTION,
            Disposition.IMPLEMENT_BETTER_FIX,
        }
        and not evidence.code_changed
    ):
        return DispositionDecision(None, False, "implementation disposition lacks a code change")
    if evidence.disposition is Disposition.DEFER_WITH_FOLLOWUP and evidence.followup_issue_id is not None:
        if evidence.followup_issue_id <= 0:
            return DispositionDecision(None, False, "follow-up issue identifier is invalid")
    return DispositionDecision(evidence.disposition, True, "verified")


class EffectProvider(Protocol):
    """Provider operations required by the controller-owned effect coordinator."""

    def find_followup_issue(self, finding_id: str) -> int | None:  # pragma: no cover
        ...

    def create_followup_issue(self, title: str, body: str, finding_id: str) -> int:  # pragma: no cover
        ...

    def find_thread_reply(self, thread_id: str, marker: str) -> int | None:  # pragma: no cover
        ...

    def post_thread_reply(self, thread_id: str, body: str) -> int:  # pragma: no cover
        ...

    def resolve_thread(self, thread_id: str) -> None:  # pragma: no cover
        ...


@dataclass(frozen=True)
class EffectReceipt:
    """Receipt recorded only after an external mutation is observed."""

    effect_id: str
    status: str
    remote_id: int | None = None


class IssueEffectCoordinator:
    """Run deferral issue and reply/resolve effects with replay-safe ordering."""

    def __init__(self, provider: EffectProvider) -> None:
        if not all(
            callable(getattr(provider, name, None))
            for name in (
                "find_followup_issue",
                "create_followup_issue",
                "find_thread_reply",
                "post_thread_reply",
                "resolve_thread",
            )
        ):
            raise ValueError("provider lacks WP3 effect capabilities")
        self._provider = provider
        self._receipts: dict[str, EffectReceipt] = {}

    @staticmethod
    def effect_id(finding_id: str, thread_id: str) -> str:
        """Return a stable effect identity."""
        if not finding_id.strip() or not thread_id.strip():
            raise ValueError("finding_id and thread_id are required")
        return hashlib.sha256(f"{finding_id}:{thread_id}".encode()).hexdigest()

    def defer(
        self,
        *,
        finding_id: str,
        thread_id: str,
        pr_url: str,
        title: str,
        body: str,
        marker: str,
    ) -> EffectReceipt:
        """Create/reuse an issue, then reply and resolve only after receipt."""
        effect_id = self.effect_id(finding_id, thread_id)
        existing = self._receipts.get(effect_id)
        if existing is not None and existing.status == "settled":
            self._provider.resolve_thread(thread_id)
            return existing
        issue_id = self._provider.find_followup_issue(finding_id)
        if issue_id is None:
            issue_id = self._provider.create_followup_issue(
                title,
                f"{body}\n\nOriginal comment: {pr_url}",
                finding_id,
            )
        reply = self._provider.find_thread_reply(thread_id, marker)
        if reply is None:
            self._provider.post_thread_reply(
                thread_id,
                f"Deferred for follow-up in #{issue_id}. {pr_url} [{marker}]",
            )
        receipt = EffectReceipt(effect_id, "settled", issue_id)
        self._receipts[effect_id] = receipt
        self._provider.resolve_thread(thread_id)
        return receipt

    def receipt(self, effect_id: str) -> EffectReceipt | None:
        """Return a previously settled receipt."""
        return self._receipts.get(effect_id)


class DescriptionProvider(Protocol):
    """Provider operations required for guarded PR description edits."""

    def get_pr_description(self, pr_number: int) -> str:  # pragma: no cover
        ...

    def update_pr_description(self, pr_number: int, body: str, expected_hash: str) -> None:  # pragma: no cover
        ...


def description_hash(body: str) -> str:
    """Return the optimistic-concurrency hash for a PR description."""
    return hashlib.sha256(body.encode()).hexdigest()


def update_description_guarded(
    provider: DescriptionProvider,
    *,
    pr_number: int,
    edit: str,
    expected_hash: str,
) -> str:
    """Apply a targeted edit only when the remote description is unchanged."""
    if pr_number <= 0 or not isinstance(edit, str) or not isinstance(expected_hash, str):
        raise ValueError("valid PR number, edit, and expected hash are required")
    current = provider.get_pr_description(pr_number)
    actual_hash = description_hash(current)
    if actual_hash != expected_hash:
        raise RuntimeError("pull request description changed concurrently")
    updated = current + edit
    if updated == current:
        return "no_change"
    provider.update_pr_description(pr_number, updated, expected_hash)
    return "updated"
