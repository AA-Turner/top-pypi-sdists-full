"""``pysae-ai-tools agent watch-deploy`` — post-merge deploy watch + demote.

Reads a merged :class:`~pysae_ai_tools.agent.models.Outcome` on stdin, watches
the post-merge deploy for its merge commit and, on failure, demotes the outcome
to escalated and reopens the issue. Emits the (possibly demoted) outcome as JSON.
"""

import json
import logging
import sys
from typing import Annotated

import typer

from .autopilot_config import load_autopilot, resolve_ci_selection
from .common import parse_duration_seconds
from .deploy_watcher import fetch_merge_commit_sha, watch_deploy_job, watch_deploy_pipeline
from .labels import LabelTransitionError, reopen_issue
from .models import Outcome, OutcomeStatus, RunConfig

logger = logging.getLogger(__name__)

# Deploy outcomes that must NOT demote the merged outcome: the deploy succeeded, or the
# repo simply has no such job in its post-merge pipeline (conditional/manual/absent).
_BENIGN_DEPLOY_STATUSES = frozenset({"success", "no_deploy_job"})


def _watch_deploy_and_demote_on_failure(outcome: Outcome, cfg: RunConfig) -> Outcome:
    """Watch post-merge deploy; on failure escalate the outcome and label.

    Wrapped in a broad exception handler: any unexpected error (transient glab API failure,
    network blip, malformed response) is logged and the outcome is left as-is. Best-effort by
    design — the MR was already merged, so a watch failure shouldn't reverse that signal.
    """
    if not outcome.mr_iid:
        return outcome
    try:
        return _watch_deploy_inner(outcome, cfg)
    except Exception as exc:
        logger.warning(
            "deploy watch crashed for MR !%d (%s): %s — leaving outcome as success",
            outcome.mr_iid,
            outcome.project_path,
            exc,
        )
        return outcome


def _demote_after_deploy(outcome: Outcome, reason: str) -> Outcome:
    outcome.status = OutcomeStatus.ESCALATED
    outcome.escalation_reason = reason[:300]
    # Pysae repos disable autoclose_referenced_issues, so the issue stays open after merge.
    # Reopen is a no-op in the common case but stays as a safety net for repos that do
    # autoclose; either way it ensures the board reflects the broken deploy. Best-effort.
    try:
        reopen_issue(outcome.project_path, outcome.ticket_iid)
    except LabelTransitionError as exc:
        logger.warning("cannot reopen issue %s#%s after deploy fail: %s", outcome.project_path, outcome.ticket_iid, exc)
    return outcome


def _watch_deploy_inner(outcome: Outcome, cfg: RunConfig) -> Outcome:
    selection = resolve_ci_selection(load_autopilot(outcome.project_path).post_merge_ci_jobs)
    if selection == []:  # explicitly disabled (False / [])
        logger.info("post_merge_ci_jobs disabled for %s; skipping post-merge CI watch", outcome.project_path)
        return outcome

    sha = fetch_merge_commit_sha(outcome.project_path, outcome.mr_iid) if outcome.mr_iid else None
    if not sha:
        logger.warning("could not fetch merge commit SHA for MR !%d; skipping deploy watch", outcome.mr_iid)
        return outcome

    if selection is None:  # all → the whole post-merge main pipeline
        deploy = watch_deploy_pipeline(outcome.project_path, sha, timeout=cfg.deploy_watch_timeout_seconds)
        outcome.deploy_status = deploy.status
        if deploy.status in _BENIGN_DEPLOY_STATUSES:
            return outcome
        return _demote_after_deploy(outcome, f"post-merge CI {deploy.status}: {deploy.reason}")

    for job_name in selection:  # explicit subset of named jobs
        deploy = watch_deploy_job(
            outcome.project_path,
            sha,
            job_name,
            timeout=cfg.deploy_watch_timeout_seconds,
            max_retries=cfg.deploy_watch_max_retries,
        )
        outcome.deploy_status = deploy.status
        outcome.deploy_retries = deploy.retries
        outcome.deploy_job_url = deploy.job_url
        if deploy.status in _BENIGN_DEPLOY_STATUSES:
            continue
        reason = f"post-merge {job_name} {deploy.status}: {deploy.reason}"
        if deploy.job_url:
            reason = f"{reason} (job: {deploy.job_url})"
        return _demote_after_deploy(outcome, reason)

    return outcome


def main(
    timeout: Annotated[str | None, typer.Option("--timeout")] = None,
    max_retries: Annotated[int | None, typer.Option("--max-retries")] = None,
) -> None:
    """Watch the post-merge deploy jobs for the outcome on stdin; emit the updated outcome.

    Timeout and retries default to the outcome's repo config (``autopilot.deploy_watch_timeout``
    / ``deploy_watch_max_retries``); ``--timeout`` / ``--max-retries`` override per invocation.
    """
    try:
        outcome = Outcome.model_validate(json.loads(sys.stdin.read()))
    except (json.JSONDecodeError, ValueError) as exc:
        typer.echo(f"invalid Outcome JSON on stdin: {exc}", err=True)
        raise typer.Exit(code=1) from None
    autopilot = load_autopilot(outcome.project_path)
    cfg = RunConfig(
        projects=[],
        deploy_watch_timeout_seconds=parse_duration_seconds(
            timeout if timeout is not None else autopilot.deploy_watch_timeout
        ),
        deploy_watch_max_retries=max_retries if max_retries is not None else autopilot.deploy_watch_max_retries,
    )
    typer.echo(_watch_deploy_and_demote_on_failure(outcome, cfg).model_dump_json())
