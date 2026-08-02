"""Serial merge-gate for the parallel batch.

Takes one ``ready_to_merge`` outcome (MR approved + green from phase 1) and merges it,
re-validated against the **current** ``main``. Two strategies (``autopilot.merge_strategy``):

- ``rebase`` (default, universal): if the MR diverged from its target, rebase it, wait for the
  rebased head's pipeline to go green, then merge. A rebase conflict or a red post-rebase
  pipeline escalates the outcome (the other tickets keep going).
- ``train`` (opt-in): enqueue on the GitLab merge train (auto-merge when pipeline succeeds)
  and poll until the MR is merged or dropped.

Only ever merges **one MR at a time** — the caller serialises. GitLab API helpers are
module-level so tests patch them; ``sleep`` / ``now`` are injected for deterministic polling.
"""

import json
import logging
import time
from typing import Any
from urllib.parse import quote

from ..common.glab.runner import run_glab
from ..glab.workflow_transition import settle_issue_after_merge
from .models import Outcome, OutcomeStatus

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT_SECONDS = 1800  # 30 min: rebase + full re-CI + merge
DEFAULT_POLL_INTERVAL = 30
PIPELINE_TERMINAL = frozenset({"success", "failed", "canceled", "skipped"})

# Stable marker in escalation_reason when the plain server-side rebase hit a conflict.
# The command cannot resolve it (deterministic, no LLM); the orchestrator matches this to
# hand the MR to /mr-rebase (LLM conflict resolution) and re-invoke the merge-gate.
REBASE_CONFLICT_REASON = "merge-gate: rebase conflict"


def _glab_api(path: str, *, method: str = "GET") -> Any:
    res = run_glab("api", "--method", method, path)
    if not res.ok:
        raise RuntimeError(f"glab api {method} {path} failed (exit {res.returncode}): {res.stderr}")
    return json.loads(res.stdout) if res.stdout else {}


def _get_mr(project_path: str, iid: int) -> dict[str, Any]:
    data = _glab_api(f"projects/{quote(project_path, safe='')}/merge_requests/{iid}")
    return data if isinstance(data, dict) else {}


def _trigger_rebase(project_path: str, iid: int) -> None:
    _glab_api(f"projects/{quote(project_path, safe='')}/merge_requests/{iid}/rebase", method="PUT")


def _merge_mr(project_path: str, iid: int, *, auto: bool = False) -> dict[str, Any]:
    q = "?merge_when_pipeline_succeeds=true" if auto else ""
    data = _glab_api(f"projects/{quote(project_path, safe='')}/merge_requests/{iid}/merge{q}", method="PUT")
    return data if isinstance(data, dict) else {}


def _mr_head_pipeline(project_path: str, iid: int) -> dict[str, Any] | None:
    data = _glab_api(f"projects/{quote(project_path, safe='')}/merge_requests/{iid}/pipelines")
    return data[0] if isinstance(data, list) and data and isinstance(data[0], dict) else None


def _mr_head_pipeline_status(project_path: str, iid: int) -> str | None:
    pipeline = _mr_head_pipeline(project_path, iid)
    return str(pipeline.get("status", "")) if pipeline else None


def _failed_named_jobs(project_path: str, pipeline_id: int, names: list[str]) -> list[str]:
    """Named jobs of the pipeline that failed/were canceled (blocking). Absent/skipped/manual jobs
    do not block — only a real failure of a *listed* job does."""
    jobs = _glab_api(f"projects/{quote(project_path, safe='')}/pipelines/{pipeline_id}/jobs?per_page=100")
    wanted = set(names)
    if not isinstance(jobs, list):
        return []
    return [
        str(j.get("name"))
        for j in jobs
        if isinstance(j, dict) and j.get("name") in wanted and str(j.get("status")) in ("failed", "canceled")
    ]


def _ci_verdict(
    project: str,
    iid: int,
    selection: list[str] | None,
    start: float,
    *,
    timeout: int,
    poll_interval: int,
    sleep: Any,
    now: Any,
) -> str:
    """Pre-merge CI verdict for the head pipeline, honouring the ``ci_jobs`` selection.

    ``selection`` ``[]`` → no gate (``success``); ``None`` → the whole pipeline must be green;
    a list → the head pipeline must reach a terminal state and none of those named jobs failed.
    """
    if selection == []:
        return "success"
    status = _wait_pipeline(project, iid, start, timeout=timeout, poll_interval=poll_interval, sleep=sleep, now=now)
    if selection is None or status == "timeout":
        return status
    pipeline = _mr_head_pipeline(project, iid)
    if not pipeline:
        return "no_pipeline"
    failed = _failed_named_jobs(project, int(pipeline["id"]), selection)
    return f"failed ({', '.join(failed)})" if failed else "success"


def run_merge_gate(
    outcome: Outcome,
    *,
    strategy: str = "rebase",
    ci_jobs: list[str] | None = None,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    poll_interval: int = DEFAULT_POLL_INTERVAL,
    sleep: Any = time.sleep,
    now: Any = time.monotonic,
) -> Outcome:
    """Merge the ready_to_merge ``outcome``; return it as ``success`` (merged) or ``escalated``.

    ``ci_jobs`` is the resolved pre-merge selection: ``None`` = the whole head pipeline must be
    green, a list = only those jobs, ``[]`` = no CI gate (merge without re-CI).
    """
    if outcome.mr_iid is None:
        return _escalate(outcome, "merge-gate: no mr_iid on ready_to_merge outcome")
    project, iid = outcome.project_path, outcome.mr_iid
    if strategy == "train":
        return _run_train(outcome, project, iid, timeout=timeout, poll_interval=poll_interval, sleep=sleep, now=now)
    return _run_rebase(
        outcome, project, iid, ci_jobs=ci_jobs, timeout=timeout, poll_interval=poll_interval, sleep=sleep, now=now
    )


def _run_rebase(
    outcome: Outcome,
    project: str,
    iid: int,
    *,
    ci_jobs: list[str] | None,
    timeout: int,
    poll_interval: int,
    sleep: Any,
    now: Any,
) -> Outcome:
    start = now()
    mr = _get_mr(project, iid)
    rebased = int(mr.get("diverged_commits_count", 0) or 0) > 0
    if rebased:
        # Diverged from target → rebase; the phase-1 CI is now stale.
        _trigger_rebase(project, iid)
        while now() - start < timeout:
            mr = _get_mr(project, iid)
            if mr.get("merge_error"):
                return _escalate(outcome, f"{REBASE_CONFLICT_REASON} — {mr['merge_error']}")
            if not mr.get("rebase_in_progress"):
                break
            sleep(poll_interval)
        else:
            return _escalate(outcome, "merge-gate: rebase did not finish in time")
    # Require the pre-merge CI (per `ci_jobs`) to be green before merging — covers the phase-1
    # pipeline (no divergence), our own rebase, AND an external resolve+push by /mr-rebase
    # (diverged_commits_count == 0 yet resolved changes need re-validation). `ci_jobs == []`
    # skips the gate (merge without re-CI). Caveat: reads the latest head pipeline; a just-pushed
    # branch whose new pipeline hasn't registered yet could momentarily show the previous one.
    status = _ci_verdict(
        project, iid, ci_jobs, start, timeout=timeout, poll_interval=poll_interval, sleep=sleep, now=now
    )
    if status != "success":
        return _escalate(outcome, f"merge-gate: pipeline {status} {'after rebase' if rebased else 'before merge'}")
    return _finalise_merge(outcome, project, iid)


def _finalise_merge(outcome: Outcome, project: str, iid: int) -> Outcome:
    merged = _merge_mr(project, iid)
    if merged.get("state") == "merged":
        outcome.status = OutcomeStatus.SUCCESS
        outcome.escalation_reason = None
        _settle_linked_issue(outcome, project)
        return outcome
    reason = merged.get("detailed_merge_status") or merged.get("merge_status") or "unknown"
    return _escalate(outcome, f"merge-gate: merge blocked ({reason})")


def _settle_linked_issue(outcome: Outcome, project: str) -> None:
    """Move the merged ticket off ``Under review`` — the API merge above doesn't, unlike
    ``pysae-ai-tools mr merge``. Honours ``board.to_deploy`` (To deploy, else close). Best-effort."""
    try:
        summary = settle_issue_after_merge(str(outcome.ticket_iid), project_path=project)
    except Exception as exc:  # noqa: BLE001 — board settle is never worth failing a merge over
        logger.warning("cannot settle issue %s#%s after merge: %s", project, outcome.ticket_iid, exc)
        return
    if summary:
        logger.info("board settle: %s", summary)


def _run_train(
    outcome: Outcome, project: str, iid: int, *, timeout: int, poll_interval: int, sleep: Any, now: Any
) -> Outcome:
    start = now()
    _merge_mr(project, iid, auto=True)  # enqueue on the train (auto-merge when pipeline succeeds)
    while now() - start < timeout:
        mr = _get_mr(project, iid)
        if mr.get("state") == "merged":
            outcome.status = OutcomeStatus.SUCCESS
            outcome.escalation_reason = None
            _settle_linked_issue(outcome, project)
            return outcome
        if mr.get("state") == "opened" and not mr.get("merge_when_pipeline_succeeds"):
            return _escalate(outcome, "merge-gate: dropped from merge train (auto-merge cleared)")
        sleep(poll_interval)
    return _escalate(outcome, "merge-gate: merge train did not merge in time")


def _wait_pipeline(
    project: str, iid: int, start: float, *, timeout: int, poll_interval: int, sleep: Any, now: Any
) -> str:
    while now() - start < timeout:
        status = _mr_head_pipeline_status(project, iid)
        if status in PIPELINE_TERMINAL:
            return status or "unknown"
        sleep(poll_interval)
    return "timeout"


def _escalate(outcome: Outcome, reason: str) -> Outcome:
    outcome.status = OutcomeStatus.ESCALATED
    outcome.escalation_reason = reason[:300]
    return outcome
