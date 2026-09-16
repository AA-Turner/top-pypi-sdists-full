"""Compact status comment and check-run projections."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Protocol

from agentic_devtools.cli.ci.reconciliation.models import QueueState
from agentic_devtools.cli.ci.reconciliation.views import project_pr_summary

STATUS_MARKER = "<!-- ai-pr-loop:status -->"


class StatusProvider(Protocol):
    """Provider operations needed to synchronize the status projection."""

    def find_comment(self, pr_number: int, marker: str) -> tuple[int, str] | None: ...  # pragma: no cover

    def update_comment(self, comment_id: int, body: str) -> None: ...  # pragma: no cover

    def post_comment(self, pr_number: int, body: str) -> int: ...  # pragma: no cover


def render_status_comment(state: QueueState, pr_number: int) -> str:
    """Render exactly one compact, self-identifying status comment."""
    summary = project_pr_summary(state, pr_number)
    envelope = state.pr_envelopes.get(pr_number)
    lineage = ",".join(summary.obligation_ids) or "none"
    dispositions = {
        value: 0
        for value in (
            "implement_suggestion",
            "implement_better_fix",
            "reject_with_evidence",
            "defer_with_followup",
        )
    }
    for finding in state.findings.values():
        if finding.pr_number == pr_number and finding.disposition in dispositions:
            dispositions[finding.disposition] += 1
    updated = state.last_updated_at or datetime.now(UTC)
    permits = summary.active_permit_count
    limit = envelope.round_limit if envelope is not None else 50
    return (
        f"{STATUS_MARKER}\n"
        f"**AI PR loop** · PR #{pr_number} · stage: `{summary.stage}` · lineage: `{lineage}`\n"
        f"rounds: `{summary.rounds_used}/{limit}` · active workers: `{permits}` · "
        f"dispositions: `suggestion={dispositions['implement_suggestion']}, "
        f"better_fix={dispositions['implement_better_fix']}, "
        f"reject={dispositions['reject_with_evidence']}, defer={dispositions['defer_with_followup']}`\n"
        f"last updated: `{updated.isoformat()}`"
    )


def sync_status_comment(provider: StatusProvider, state: QueueState, pr_number: int) -> int:
    """Update the marked status comment, or create it exactly once."""
    body = render_status_comment(state, pr_number)
    existing = provider.find_comment(pr_number, STATUS_MARKER)
    if existing is not None:
        provider.update_comment(existing[0], body)
        return existing[0]
    return provider.post_comment(pr_number, body)


def render_check_details(state: QueueState, pr_number: int) -> dict[str, object]:
    """Render title, summary, and text suitable for a GitHub check run."""
    summary = project_pr_summary(state, pr_number)
    return {
        "title": f"AI PR loop · PR #{pr_number}",
        "summary": f"Stage `{summary.stage}`; {summary.rounds_used}/{summary.round_limit} rounds used.",
        "text": (
            f"Obligations: {len(summary.obligation_ids)}; findings: {len(summary.finding_ids)}; "
            f"attempts: {summary.attempt_count}; active workers: {summary.active_permit_count}."
        ),
    }
