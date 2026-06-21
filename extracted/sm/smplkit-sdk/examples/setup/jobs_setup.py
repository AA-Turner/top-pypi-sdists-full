"""Setup / cleanup helpers for ``jobs_showcase.py``."""

from __future__ import annotations

from smplkit import AsyncJobsClient, NotFoundError

# Every job and retry policy the jobs showcase creates. Start-of-run cleanup
# removes residue from a prior run; the matching ``finally`` cleanup tears them
# down even when it fails mid-way, so a failed run never leaves orphans behind.
_DEMO_JOB_IDS = ["showcase-recurring", "showcase-manual", "showcase-oneoff"]
_DEMO_RETRY_POLICY_IDS = ["showcase-retry"]


async def setup_showcase(jobs: AsyncJobsClient) -> None:
    await cleanup_showcase(jobs)


async def cleanup_showcase(jobs: AsyncJobsClient) -> None:
    # Jobs first, then the policies they reference.
    for job_id in _DEMO_JOB_IDS:
        try:
            await jobs.delete(job_id)
        except NotFoundError:
            pass
    for policy_id in _DEMO_RETRY_POLICY_IDS:
        try:
            await jobs.retry_policies.delete(policy_id)
        except NotFoundError:
            pass
