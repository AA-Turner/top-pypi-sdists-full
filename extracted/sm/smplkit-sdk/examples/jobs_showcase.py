"""
Demonstrates the smplkit management SDK for Smpl Jobs.

Prerequisites:
    - ``pip install smplkit-sdk``
    - A valid smplkit API key, provided via one of:
        - ``SMPLKIT_API_KEY`` environment variable
        - ``~/.smplkit`` configuration file (see SDK docs)

Usage::

    python examples/jobs_showcase.py
"""

import asyncio
import uuid

from smplkit import AsyncSmplManagementClient
from smplkit._errors import NotFoundError
from smplkit.management.jobs import HttpConfig


async def main() -> None:

    # create the client (use SmplManagementClient for synchronous use)
    async with AsyncSmplManagementClient() as manage:
        job_id = f"showcase-mgmt-{uuid.uuid4().hex[:8]}"

        try:
            # create a job
            job = manage.jobs.new(
                job_id,
                name="Nightly cache warm",
                description="Warms the product cache every night at 02:00 UTC.",
                schedule="0 2 * * *",  # 5-field cron, UTC
                enabled=False,
                configuration=HttpConfig(
                    method="POST",
                    url="https://api.example.com/cache/warm",
                    headers=[("Authorization", "Bearer s3cr3t")],
                    body='{"scope": "all"}',
                    timeout=30,
                ),
            )
            await job.save()
            assert job.version == 1
            print(f"Created job {job.id!r} (v{job.version})")

            # get a job
            fetched = await manage.jobs.get(job_id)
            assert fetched.configuration.url == "https://api.example.com/cache/warm"
            print(f"Fetched job {job_id!r}")

            # list jobs
            jobs = await manage.jobs.list(enabled=False)
            assert job_id in {j.id for j in jobs}
            print(f"Found job {job_id!r} and in the listing")

            # update a job
            job.name = "Nightly cache warm (v2)"
            job.schedule = "30 2 * * *"
            job.enabled = True
            await job.save()
            assert job.version == 2 and job.enabled is True
            print(f"Updated job to v{job.version}: schedule={job.schedule!r}")

            # trigger an immediate run (a MANUAL run)
            run = await manage.jobs.run(job_id)
            assert run.trigger == "MANUAL" and run.job == job_id
            print(f"Triggered run {run.id} (trigger={run.trigger}, status={run.status})")

            # read run history for this job, and fetch a single run
            runs = await manage.jobs.runs.list(job=job_id)
            assert any(r.id == run.id for r in runs)
            got = await manage.jobs.runs.get(run.id)
            assert got.id == run.id
            print(f"Listed {len(runs)} run(s); fetched run {got.id} (status={got.status})")

            # re-run from a prior run, then cancel it while it's still pending
            rerun = await manage.jobs.runs.rerun(run.id)
            assert rerun.trigger == "RERUN" and rerun.rerun_of == run.id
            canceled = await manage.jobs.runs.cancel(rerun.id)
            assert canceled.status == "CANCELED"
            print(f"Re-ran ({rerun.id}) then canceled it -> {canceled.status}")

            # delete a job
            await job.delete()
            assert job_id not in {j.id for j in await manage.jobs.list()}
            print(f"Deleted job {job_id!r} — management showcase complete.")
        finally:
            # tear-down: never leave the showcase job behind, even on failure
            try:
                await manage.jobs.delete(job_id)
            except NotFoundError:
                pass


if __name__ == "__main__":
    asyncio.run(main())
