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

from smplkit import AsyncJobsClient, ConflictError
from smplkit.jobs import HttpConfig

from setup.jobs_setup import cleanup_showcase, setup_showcase

RECURRING_JOB_ID = "showcase-recurring"
ONEOFF_JOB_ID = "showcase-oneoff"


async def main() -> None:

    # or SmplClient for synchronous use
    async with AsyncJobsClient() as jobs:
        await setup_showcase(jobs)
        try:
            # create a recurring job, enabled in production with a development override
            job = jobs.new(
                RECURRING_JOB_ID,
                name="Nightly cache warm",
                description="Warms the product cache every night at 02:00 UTC.",
                schedule="0 2 * * *",
                configuration=HttpConfig(
                    method="POST",
                    url="https://httpbin.org/post",
                    headers=[("Authorization", "Bearer s3cr3t")],
                    body='{"scope": "all"}',
                    timeout=30,
                ),
            )
            job.set_configuration(
                HttpConfig(
                    method="POST",
                    url="https://development.example.com/cache/warm",
                    headers=[("Authorization", "Bearer development-s3cr3t")],
                    body='{"scope": "all"}',
                ),
                environment="development",
            )
            job.set_enabled(False, environment="development")
            job.set_enabled(True, environment="production")
            await job.save()
            assert job.version == 1
            assert job.is_enabled(environment="development") is False
            assert job.is_enabled(environment="production") is True
            print(f"Created recurring job {job.id!r} (v{job.version})")

            # get a job
            fetched = await jobs.get(RECURRING_JOB_ID)
            assert fetched.is_enabled(environment="development") is False
            assert fetched.is_enabled(environment="production") is True
            assert (
                fetched.get_configuration(environment="development").url
                == "https://development.example.com/cache/warm"
            )
            print(f"Fetched job {RECURRING_JOB_ID!r}")

            # list jobs
            listing = await jobs.list()
            assert RECURRING_JOB_ID in {j.id for j in listing}
            print(f"Found job {RECURRING_JOB_ID!r} in the listing")

            # update a job (the schedule is environment-agnostic)
            job.name = "Nightly cache warm (v2)"
            job.set_schedule("30 2 * * *")
            job.set_enabled(True, environment="development")
            await job.save()
            assert (
                job.version == 2
                and job.is_enabled(environment="development") is True
            )
            print(
                f"Updated job to v{job.version}: now enabled in production and development"
            )

            # trigger an immediate run
            run = await job.trigger(environment="production")
            assert run.trigger == "MANUAL" and run.environment == "production"
            print(
                f"Triggered run {run.id} (trigger={run.trigger}, env={run.environment})"
            )

            # get this job's runs
            runs = await job.list_runs(environment="production")
            assert any(r.id == run.id for r in runs)
            print(f"Listed {len(runs)} production run(s)")

            # get a run
            run = await jobs.runs.get(run.id)
            assert run.environment == "production"
            print(f"Fetched run {run.id} (env={run.environment})")

            # re-run a prior run (inherits its environment)
            rerun = await run.rerun()
            assert (
                rerun.trigger == "RERUN"
                and rerun.environment == run.environment
            )
            print(f"Re-ran {run.id} -> {rerun.id} (env={rerun.environment})")

            # cancel a run (best-effort: a finished run can no longer be canceled)
            try:
                canceled = await rerun.cancel()
                print(f"Canceled run {canceled.id} -> {canceled.status}")
            except ConflictError:
                print(
                    f"Run {rerun.id} already finished before it could be canceled"
                )

            # create a one-off job, born in a single environment
            oneoff = jobs.new(
                ONEOFF_JOB_ID,
                name="One-shot reindex",
                schedule="now",
                configuration=HttpConfig(
                    method="POST", url="https://httpbin.org/post"
                ),
                environment="development",
            )
            await oneoff.save()
            assert (
                oneoff.version == 1
                and oneoff.is_enabled(environment="development") is True
            )
            print(f"Created one-off job {oneoff.id!r} born in development")

            # delete a job
            await job.delete()
            assert RECURRING_JOB_ID not in {j.id for j in await jobs.list()}
            print(
                f"Deleted job {RECURRING_JOB_ID!r} — jobs showcase complete."
            )
        finally:
            await cleanup_showcase(jobs)


if __name__ == "__main__":
    asyncio.run(main())
