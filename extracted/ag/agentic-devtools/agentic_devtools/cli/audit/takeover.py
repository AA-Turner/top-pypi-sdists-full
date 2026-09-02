"""Scheduled takeover of Copilot review-feedback evaluation PRs.

The evaluation output for a review-feedback audit batch is produced by the
Copilot cloud coding agent on a ``copilot/**`` branch. GitHub does not start
workflow runs for Copilot/automation-origin pushes and PR events (they sit at
"Action required" awaiting manual approval), so ``audit-review-feedback-apply``
never fires on its own.

This module reclaims such evaluation PRs under a human identity — preferring a
**squash** (a clean single commit, the same mechanism the AI PR loop uses) and
falling back to a plain **takeover amend** if the squash fails. Either rewrites
HEAD under the human CI identity and force-pushes, which emits a ``synchronize``
event from a human pusher and un-gates the apply workflow.

Per-PR failures are logged and never abort the run, so a single bad PR cannot
fail the scheduled workflow.
"""

from __future__ import annotations

import logging
from typing import Any

from agentic_devtools.cli.ci.models import TAKEOVER_HEAD_AUTHOR_LOGINS
from agentic_devtools.cli.ci.pipeline.session_detector import is_copilot_session_active_via_agent_task
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.ci.scheduler import (
    AUDIT_AGENT_OUTPUT_PATH_PREFIX,
    AUDIT_AGENT_OUTPUT_PATH_SUBSTR,
)

logger = logging.getLogger(__name__)

_TAKEOVER_AUTHORS_CF = frozenset(login.casefold() for login in TAKEOVER_HEAD_AUTHOR_LOGINS)


def touches_agent_output(changed_files: list[str]) -> bool:
    """Return True when any changed file is an audit agent-output payload."""
    for file_path in changed_files:
        normalized = str(file_path).replace("\\", "/")
        if normalized.startswith(AUDIT_AGENT_OUTPUT_PATH_PREFIX) and AUDIT_AGENT_OUTPUT_PATH_SUBSTR in normalized:
            return True
    return False


def reclaim_one_eval_pr(
    provider: CIPlatformProvider,
    *,
    pr_number: int,
    base_branch: str,
    head_branch: str,
    head_sha: str,
) -> str:
    """Reclaim one eval PR under a human identity: squash first, takeover fallback.

    A successful squash rewrites the (multi-commit) eval branch into a single
    commit authored by the CI identity — clean *and* un-gating. If the squash
    raises (e.g. a force-with-lease race), fall back to the takeover amend, which
    also un-gates. Both re-emit a human ``synchronize`` event.

    Returns the outcome string: ``squashed``, ``takeover``, or ``failed``.
    """
    try:
        provider.squash_before_publish(
            pr_number=pr_number,
            base_branch=base_branch,
            head_branch=head_branch,
            head_sha=head_sha,
        )
        logger.info("PR #%d: squashed under human identity to un-gate apply", pr_number)
        return "squashed"
    except Exception as squash_exc:  # noqa: BLE001 - squash is best-effort; fall back to takeover
        logger.warning("PR #%d: squash failed (%s); falling back to takeover", pr_number, squash_exc)

    try:
        provider.reclaim_copilot_commit(
            pr_number=pr_number,
            head_branch=head_branch,
            head_sha=head_sha,
        )
        logger.info("PR #%d: reclaimed HEAD under human identity to un-gate apply", pr_number)
        return "takeover"
    except Exception as reclaim_exc:  # noqa: BLE001 - never fail the workflow on a single PR
        logger.error("PR #%d: takeover fallback failed: %s", pr_number, reclaim_exc)
        return "failed"


def takeover_eval_prs(provider: CIPlatformProvider, *, repo: str, max_prs: int = 1) -> dict[str, Any]:
    """Reclaim up to ``max_prs`` Copilot-authored audit evaluation PRs.

    For each open ``copilot/**`` PR (oldest first) that touches
    ``audit-batches/**/agent-output/**``, is still authored by Copilot/automation
    (the idempotency gate — a reclaimed PR is human-authored and thus skipped),
    and has no active Copilot session, reclaim it under a human identity via
    :func:`reclaim_one_eval_pr`.

    Per-PR errors are logged and never abort the run.

    Returns ``{"candidates": int, "processed": [{"pr_number": int,
    "outcome": str}, ...]}``.
    """
    briefs = provider.list_open_copilot_pr_briefs()
    processed: list[dict[str, Any]] = []
    for brief in briefs:
        if len(processed) >= max_prs:
            break

        try:
            pr_number = int(brief["number"])
        except (KeyError, TypeError, ValueError) as exc:
            logger.warning("Skipping malformed PR brief (%s): %r", exc, brief)
            continue

        try:
            files = provider.list_pr_files(pr_number)
        except Exception as exc:  # noqa: BLE001 - per-PR failure must not abort the run
            logger.warning("PR #%d: failed to list files (%s); skipping", pr_number, exc)
            continue
        if not touches_agent_output(files):
            continue

        try:
            meta = provider.get_pr_metadata(pr_number)
        except Exception as exc:  # noqa: BLE001 - per-PR failure must not abort the run
            logger.warning("PR #%d: failed to get metadata (%s); skipping", pr_number, exc)
            continue
        try:
            head_author = provider.get_commit_author_login(meta.head_sha)
        except Exception:  # noqa: BLE001 - unknown author → treat as not takeover-eligible
            head_author = ""
        if head_author.casefold() not in _TAKEOVER_AUTHORS_CF:
            logger.info(
                "PR #%d: HEAD authored by '%s' — already reclaimed; skipping",
                pr_number,
                head_author or "unknown",
            )
            continue

        if is_copilot_session_active_via_agent_task(repo, pr_number):
            logger.info("PR #%d: Copilot session active — deferring takeover", pr_number)
            continue

        outcome = reclaim_one_eval_pr(
            provider,
            pr_number=pr_number,
            base_branch=meta.base_branch,
            head_branch=meta.head_branch,
            head_sha=meta.head_sha,
        )
        processed.append({"pr_number": pr_number, "outcome": outcome})

    return {"candidates": len(briefs), "processed": processed}
