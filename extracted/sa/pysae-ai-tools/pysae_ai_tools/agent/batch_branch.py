"""Temp integration branch for ``code-autopilot-batch --batch-branch``.

Instead of merging each ticket straight into the default branch, the batch cuts a throwaway
``staging/autopilot-batch-<ts>`` branch, merges every ticket into it (no per-ticket CI), then
opens a single integration MR into the default branch and verifies its pipeline **once** — and,
only if green, merges that MR. The default branch is never touched until that final CI passes.

The final CI runs through an MR (not a bare branch push) on purpose: many repos gate pipelines
to ``merge_request_event`` in ``workflow.rules``, so a ``staging/*`` branch push yields no
pipeline at all — only the MR does. See :func:`finalize_integration_branch`.

glab helpers are module-level so tests patch them.
"""

import json
import logging
import time
from typing import Any
from urllib.parse import quote

from ..common.glab.runner import run_glab
from ..glab.workflow_transition import settle_issue_after_merge

logger = logging.getLogger(__name__)

PIPELINE_TERMINAL = frozenset({"success", "failed", "canceled", "skipped"})
DEFAULT_POLL_INTERVAL = 30


def _glab_api(path: str, *, method: str = "GET") -> Any:
    res = run_glab("api", "--method", method, path)
    if not res.ok:
        logger.warning("glab api %s %s failed: %s", method, path, res.stderr)
        return None
    return json.loads(res.stdout) if res.stdout else {}


def default_branch(project_path: str) -> str:
    data = _glab_api(f"projects/{quote(project_path, safe='')}")
    return str(data.get("default_branch", "main")) if isinstance(data, dict) else "main"


def create_integration_branch(project_path: str, stamp: str, *, base: str | None = None) -> str | None:
    """Create ``staging/autopilot-batch-<stamp>`` off the default branch; return its name (None on failure).

    ``stamp`` is a compact timestamp, e.g. ``20260711-143005`` (``%Y%m%d-%H%M%S``).
    """
    branch = f"staging/autopilot-batch-{stamp}"
    ref = base or default_branch(project_path)
    enc = quote(project_path, safe="")
    result = _glab_api(
        f"projects/{enc}/repository/branches?branch={quote(branch, safe='')}&ref={quote(ref, safe='')}", method="POST"
    )
    if not isinstance(result, dict) or not result.get("name"):
        logger.warning("could not create integration branch %s off %s", branch, ref)
        return None
    return branch


def _latest_branch_pipeline(project_path: str, branch: str) -> dict[str, Any] | None:
    enc = quote(project_path, safe="")
    data = _glab_api(f"projects/{enc}/pipelines?ref={quote(branch, safe='')}&per_page=1")
    return data[0] if isinstance(data, list) and data and isinstance(data[0], dict) else None


def _failed_named_jobs(project_path: str, pipeline_id: int, names: list[str]) -> list[str]:
    jobs = _glab_api(f"projects/{quote(project_path, safe='')}/pipelines/{pipeline_id}/jobs?per_page=100")
    wanted = set(names)
    if not isinstance(jobs, list):
        return []
    return [
        str(j.get("name"))
        for j in jobs
        if isinstance(j, dict) and j.get("name") in wanted and str(j.get("status")) in ("failed", "canceled")
    ]


def _verify_pipeline(
    project_path: str,
    fetch_latest: Any,
    label: str,
    selection: list[str] | None,
    *,
    timeout: int,
    poll_interval: int,
    sleep: Any,
    now: Any,
) -> tuple[bool, str]:
    """Wait for ``fetch_latest()`` to yield a pipeline and verify it per ``selection``.

    ``selection`` ``[]`` → nothing to verify (ok); ``None`` → the whole pipeline must be green;
    a list → the pipeline must be terminal and none of those named jobs failed. ``label`` names
    the watched target in the "no pipeline" message (a branch name, or ``!<mr_iid>`` for an MR).
    """
    if selection == []:
        return True, "no CI to verify"
    start = now()
    pipeline: dict[str, Any] | None = None
    while now() - start < timeout:
        pipeline = fetch_latest()
        if pipeline:
            break
        sleep(poll_interval)
    if not pipeline:
        return False, f"no pipeline for {label}"
    pid = int(pipeline["id"])
    while now() - start < timeout:
        current = _glab_api(f"projects/{quote(project_path, safe='')}/pipelines/{pid}")
        status = str(current.get("status", "")) if isinstance(current, dict) else ""
        if status in PIPELINE_TERMINAL:
            if selection is None:
                return (status == "success", f"pipeline {status}")
            failed = _failed_named_jobs(project_path, pid, selection)
            return (not failed, "ok" if not failed else f"failed: {', '.join(failed)}")
        sleep(poll_interval)
    return False, f"pipeline watch exceeded {timeout}s"


def verify_branch_ci(
    project_path: str,
    branch: str,
    selection: list[str] | None,
    *,
    timeout: int,
    poll_interval: int = DEFAULT_POLL_INTERVAL,
    sleep: Any = time.sleep,
    now: Any = time.monotonic,
) -> tuple[bool, str]:
    """Verify ``branch``'s own pipeline. Used for the report-only check on the default branch,
    which gets a pipeline on push; a temp ``staging/*`` branch may not (see :func:`finalize_integration_branch`).
    """
    return _verify_pipeline(
        project_path,
        lambda: _latest_branch_pipeline(project_path, branch),
        branch,
        selection,
        timeout=timeout,
        poll_interval=poll_interval,
        sleep=sleep,
        now=now,
    )


def _latest_mr_pipeline(project_path: str, mr_iid: int) -> dict[str, Any] | None:
    enc = quote(project_path, safe="")
    data = _glab_api(f"projects/{enc}/merge_requests/{mr_iid}/pipelines?per_page=1")
    return data[0] if isinstance(data, list) and data and isinstance(data[0], dict) else None


def open_integration_mr(project_path: str, branch: str, target: str | None = None) -> int | None:
    """Open (or reuse) the integration MR ``branch`` → default branch; return its iid (None on failure).

    Going through an MR — rather than pushing the branch and hoping a pipeline appears — is what
    makes the end-of-batch CI work on repos whose ``workflow.rules`` only build pipelines for
    ``merge_request_event``: a plain ``staging/*`` branch push produces no pipeline there, so a
    branch-only check would wait out its whole timeout and never merge.
    """
    enc = quote(project_path, safe="")
    tgt = target or default_branch(project_path)
    existing = _glab_api(
        f"projects/{enc}/merge_requests?state=opened"
        f"&source_branch={quote(branch, safe='')}&target_branch={quote(tgt, safe='')}"
    )
    if isinstance(existing, list) and existing and isinstance(existing[0], dict) and existing[0].get("iid"):
        return int(existing[0]["iid"])
    mr = _glab_api(
        f"projects/{enc}/merge_requests?source_branch={quote(branch, safe='')}"
        f"&target_branch={quote(tgt, safe='')}&title={quote('autopilot batch integration', safe='')}"
        "&remove_source_branch=true",
        method="POST",
    )
    if not isinstance(mr, dict) or not mr.get("iid"):
        logger.warning("could not open integration MR for %s → %s", branch, tgt)
        return None
    return int(mr["iid"])


def verify_mr_ci(
    project_path: str,
    mr_iid: int,
    selection: list[str] | None,
    *,
    timeout: int,
    poll_interval: int = DEFAULT_POLL_INTERVAL,
    sleep: Any = time.sleep,
    now: Any = time.monotonic,
) -> tuple[bool, str]:
    """Verify the integration MR's own ``merge_request_event`` pipeline."""
    return _verify_pipeline(
        project_path,
        lambda: _latest_mr_pipeline(project_path, mr_iid),
        f"!{mr_iid}",
        selection,
        timeout=timeout,
        poll_interval=poll_interval,
        sleep=sleep,
        now=now,
    )


def merge_open_mr(project_path: str, mr_iid: int) -> bool:
    enc = quote(project_path, safe="")
    merged = _glab_api(f"projects/{enc}/merge_requests/{mr_iid}/merge", method="PUT")
    return isinstance(merged, dict) and merged.get("state") == "merged"


def finalize_integration_branch(
    project_path: str,
    branch: str,
    selection: list[str] | None,
    *,
    merge: bool,
    timeout: int,
    poll_interval: int = DEFAULT_POLL_INTERVAL,
    sleep: Any = time.sleep,
    now: Any = time.monotonic,
) -> tuple[bool, bool, str]:
    """Open the integration MR, verify its CI, and (with ``merge``) merge it on green.

    Returns ``(ok, merged, reason)``. The default branch is never touched unless the MR's
    pipeline is green and ``merge`` is set.
    """
    mr_iid = open_integration_mr(project_path, branch)
    if mr_iid is None:
        return False, False, f"could not open integration MR for {branch}"
    ok, reason = verify_mr_ci(
        project_path, mr_iid, selection, timeout=timeout, poll_interval=poll_interval, sleep=sleep, now=now
    )
    if not ok or not merge:
        return ok, False, reason
    if merge_open_mr(project_path, mr_iid):
        _settle_staged_tickets(project_path, branch)
        return True, True, reason
    return False, False, f"CI green but merging !{mr_iid} failed"


def _linked_issue_iid(description: str) -> str:
    """First ``#N`` token of an MR description (the ``Closes #N`` link), or ''."""
    for token in (description or "").split():
        stripped = token.strip(".,;:()")
        if stripped.startswith("#") and stripped[1:].isdigit():
            return stripped[1:]
    return ""


def _settle_staged_tickets(project_path: str, branch: str) -> None:
    """Finalise the board for every ticket staged on ``branch``, now that it has merged into
    the default branch. The per-ticket merges targeted the staging branch, so ``pysae-ai-tools mr merge``
    left their column untouched (a merge into a non-default branch does not finalise) — this is
    where each ticket moves to ``To deploy`` / closes for real. Best-effort, idempotent (an
    already-settled ticket is a no-op). Orchestrator-agnostic: discovers the tickets from the
    MRs merged into the staging branch, so it runs no matter which batch path drove the merges.
    """
    enc = quote(project_path, safe="")
    data = _glab_api(f"projects/{enc}/merge_requests?target_branch={quote(branch, safe='')}&state=merged&per_page=100")
    if not isinstance(data, list):
        return
    settled: set[str] = set()
    for mr in data:
        if not isinstance(mr, dict):
            continue
        iid = _linked_issue_iid(str(mr.get("description") or ""))
        if not iid or iid in settled:
            continue
        settled.add(iid)
        summary = settle_issue_after_merge(iid, project_path=project_path)
        if summary:
            logger.info("board settle: %s", summary)
