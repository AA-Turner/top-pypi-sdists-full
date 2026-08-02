"""Post-merge deploy watcher with auto-retry on flaky failures.

After the batch merges an MR, the post-merge pipeline on main is not covered by
the in-MR CI (a deploy job only runs on push to main, not on MR pipelines). This
module polls that pipeline, watches the configured deploy job, and retries it via
the GitLab API on transient failures (ArgoCD races, runner system errors, slow pod
scheduling). The job name is supplied by the caller (from ``autopilot.post_merge_ci_jobs``);
no job name is special-cased here. A repo with no deploy job never reaches this module.
"""

import logging
import time
from dataclasses import dataclass
from typing import Any, Literal
from urllib.parse import quote

from ..common.glab.runner import glab_api

logger = logging.getLogger(__name__)

DeployStatus = Literal["success", "failed", "timeout", "no_pipeline", "no_deploy_job"]

DEFAULT_TIMEOUT_SECONDS = 1200  # 20 min
DEFAULT_MAX_RETRIES = 3
DEFAULT_POLL_INTERVAL = 30
RETRY_BACKOFFS = (60, 180, 420)
TERMINAL_STATUSES = frozenset({"success", "failed", "canceled", "skipped"})


@dataclass
class DeployOutcome:
    status: DeployStatus
    reason: str = ""
    retries: int = 0
    pipeline_url: str = ""
    job_url: str = ""

    @property
    def is_success(self) -> bool:
        return self.status == "success"


def _glab_api(path: str, *, method: str = "GET") -> Any:
    # The poll/retry loop needs a hard failure signal, so raise on a failed call
    # rather than adopting the socle helper's return-None-on-error contract.
    data = glab_api(path, method="" if method == "GET" else method)
    if data is None:
        raise RuntimeError(f"glab api {method} {path} failed")
    return data


def _find_main_pipeline_for_sha(project_path: str, sha: str) -> dict[str, Any] | None:
    encoded = quote(project_path, safe="")
    pipelines = _glab_api(f"projects/{encoded}/pipelines?ref=main&sha={sha}&per_page=5")
    if isinstance(pipelines, list) and pipelines:
        first = pipelines[0]
        return first if isinstance(first, dict) else None
    return None


def _get_pipeline(project_path: str, pipeline_id: int) -> dict[str, Any] | None:
    encoded = quote(project_path, safe="")
    pipeline = _glab_api(f"projects/{encoded}/pipelines/{pipeline_id}")
    return pipeline if isinstance(pipeline, dict) else None


def _find_job_in_pipeline(project_path: str, pipeline_id: int, name: str) -> dict[str, Any] | None:
    encoded = quote(project_path, safe="")
    jobs = _glab_api(f"projects/{encoded}/pipelines/{pipeline_id}/jobs?per_page=100")
    if isinstance(jobs, list):
        for j in jobs:
            if isinstance(j, dict) and j.get("name") == name:
                return j
    return None


def _retry_job(project_path: str, job_id: int) -> dict[str, Any]:
    encoded = quote(project_path, safe="")
    result = _glab_api(f"projects/{encoded}/jobs/{job_id}/retry", method="POST")
    return result if isinstance(result, dict) else {}


def watch_deploy_job(
    project_path: str,
    merge_sha: str,
    job_name: str,
    *,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    max_retries: int = DEFAULT_MAX_RETRIES,
    poll_interval: int = DEFAULT_POLL_INTERVAL,
    sleep: Any = time.sleep,
    now: Any = time.monotonic,
) -> DeployOutcome:
    """Poll the post-merge pipeline; retry `job_name` on failure up to N times.

    Returns `no_deploy_job` when the pipeline reaches a terminal state without ever
    exposing `job_name` (conditional/manual/absent job) — a benign outcome, not a
    failure. `sleep` and `now` are injectable to keep tests fast/deterministic.
    """
    start = now()
    retries = 0
    pipeline_url = ""

    # Phase 1: wait for the main pipeline to appear (GitLab webhook can lag)
    pipeline: dict[str, Any] | None = None
    while now() - start < timeout:
        pipeline = _find_main_pipeline_for_sha(project_path, merge_sha)
        if pipeline:
            pipeline_url = pipeline.get("web_url", "")
            break
        sleep(poll_interval)
    if not pipeline:
        return DeployOutcome(
            status="no_pipeline",
            reason=f"no main pipeline appeared for sha {merge_sha[:8]} within {timeout}s",
        )

    pipeline_id = int(pipeline["id"])

    # Phase 2: poll the deploy job until terminal status; retry on failure with backoff
    while now() - start < timeout:
        job = _find_job_in_pipeline(project_path, pipeline_id, job_name)
        if not job:
            # The job may not have materialised yet — but if the pipeline itself has
            # reached a terminal state without it, it never will (conditional/manual/absent):
            # a benign no-op, not a deploy failure.
            pipeline = _get_pipeline(project_path, pipeline_id)
            if pipeline and str(pipeline.get("status", "")) in TERMINAL_STATUSES:
                return DeployOutcome(
                    status="no_deploy_job",
                    reason=f"'{job_name}' absent from terminal pipeline {pipeline_id}",
                    retries=retries,
                    pipeline_url=pipeline_url,
                )
            sleep(poll_interval)
            continue

        job_status = str(job.get("status", ""))
        job_url = str(job.get("web_url", ""))

        if job_status not in TERMINAL_STATUSES:
            sleep(poll_interval)
            continue

        if job_status == "success":
            return DeployOutcome(
                status="success",
                retries=retries,
                pipeline_url=pipeline_url,
                job_url=job_url,
            )

        if retries >= max_retries:
            return DeployOutcome(
                status="failed",
                reason=f"{job_name} {job_status} after {retries} retries",
                retries=retries,
                pipeline_url=pipeline_url,
                job_url=job_url,
            )

        backoff = RETRY_BACKOFFS[min(retries, len(RETRY_BACKOFFS) - 1)]
        logger.info(
            "%s %s; retry %d/%d after %ds",
            job_name,
            job_status,
            retries + 1,
            max_retries,
            backoff,
        )
        sleep(backoff)
        try:
            _retry_job(project_path, int(job["id"]))
        except RuntimeError as exc:
            return DeployOutcome(
                status="failed",
                reason=f"retry API call failed: {exc}",
                retries=retries,
                pipeline_url=pipeline_url,
                job_url=job_url,
            )
        retries += 1

    return DeployOutcome(
        status="timeout",
        reason=f"watch exceeded {timeout}s",
        retries=retries,
        pipeline_url=pipeline_url,
    )


def watch_deploy_pipeline(
    project_path: str,
    merge_sha: str,
    *,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    poll_interval: int = DEFAULT_POLL_INTERVAL,
    sleep: Any = time.sleep,
    now: Any = time.monotonic,
) -> DeployOutcome:
    """Wait for the **whole** post-merge main pipeline to go green (``post_merge_ci_jobs`` = all).

    Unlike :func:`watch_deploy_job` (a single named job with retries), this waits for the
    pipeline's overall status — success, else failed. No per-job retry.
    """
    start = now()
    pipeline: dict[str, Any] | None = None
    while now() - start < timeout:
        pipeline = _find_main_pipeline_for_sha(project_path, merge_sha)
        if pipeline:
            break
        sleep(poll_interval)
    if not pipeline:
        return DeployOutcome(status="no_pipeline", reason=f"no main pipeline for sha {merge_sha[:8]}")
    pipeline_id = int(pipeline["id"])
    pipeline_url = str(pipeline.get("web_url", ""))
    while now() - start < timeout:
        current = _get_pipeline(project_path, pipeline_id)
        status = str(current.get("status", "")) if current else ""
        if status in TERMINAL_STATUSES:
            if status == "success":
                return DeployOutcome(status="success", pipeline_url=pipeline_url)
            return DeployOutcome(status="failed", reason=f"main pipeline {status}", pipeline_url=pipeline_url)
        sleep(poll_interval)
    return DeployOutcome(status="timeout", reason=f"watch exceeded {timeout}s", pipeline_url=pipeline_url)


def fetch_merge_commit_sha(project_path: str, mr_iid: int) -> str | None:
    """Fetch the merge commit SHA of a merged MR via glab API."""
    encoded = quote(project_path, safe="")
    try:
        data = _glab_api(f"projects/{encoded}/merge_requests/{mr_iid}")
    except RuntimeError as exc:
        logger.warning("failed to fetch MR %d: %s", mr_iid, exc)
        return None
    if isinstance(data, dict):
        sha = data.get("merge_commit_sha") or data.get("squash_commit_sha")
        return str(sha) if sha else None
    return None
