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
from datetime import datetime, timedelta

from smplkit import AsyncJobsClient, ConflictError
from smplkit.jobs import (
    Backoff,
    HttpConfig,
    JobKind,
    RetryOn,
    RetryReason,
    RunTrigger,
)

from setup.jobs_setup import cleanup_showcase, setup_showcase

RECURRING_JOB_ID = "showcase-recurring"
MANUAL_JOB_ID = "showcase-manual"
ONEOFF_JOB_ID = "showcase-oneoff"
RETRY_POLICY_ID = "showcase-retry"


async def main() -> None:

    # or SmplClient for synchronous use
    async with AsyncJobsClient() as jobs:
        await setup_showcase(jobs)
        try:
            # create a retry policy
            retry_policy = jobs.retry_policies.new(
                RETRY_POLICY_ID,
                name="Retry on server errors",
                max_retries=5,
                backoff=Backoff.EXPONENTIAL,
                delay_seconds=2,
                max_delay_seconds=60,
                retry_on=RetryOn(
                    statuses=[429, 503], reasons=[RetryReason.TIMEOUT]
                ),
            )
            await retry_policy.save()
            assert RETRY_POLICY_ID in {
                p.id for p in await jobs.retry_policies.list()
            }
            print(f"Created retry policy {retry_policy.id!r}")

            # create a recurring job
            job = jobs.new_recurring_job(
                RECURRING_JOB_ID,
                name="Nightly cache warm",
                description="Warms the product cache nightly.",
                schedule="0 2 * * *",
                configuration=HttpConfig(
                    method="POST",
                    url="https://httpbin.org/post",
                    headers=[("Authorization", "Bearer s3cr3t")],
                    body='{"scope": "all"}',
                    timeout=30,
                ),
            )
            job.set_enabled(True, environment="development")
            job.set_enabled(True, environment="production")
            job.set_schedule(
                "0 */6 * * *",
                timezone="America/New_York",
                environment="development",
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
            await job.save()
            assert job.is_recurring() is True
            assert job.is_enabled(environment="development") is True
            assert job.is_enabled(environment="production") is True
            assert (
                job.environments["development"].timezone == "America/New_York"
            )
            assert (
                job.get_configuration(environment="development").url
                == "https://development.example.com/cache/warm"
            )
            print(f"Created recurring job {job.id!r} (v{job.version})")

            # get a job
            fetched = await jobs.get(RECURRING_JOB_ID)
            assert (
                fetched.environments["development"].schedule == "0 */6 * * *"
            )
            print(f"Fetched job {RECURRING_JOB_ID!r}")

            # list jobs, filtered to recurring jobs
            listing = await jobs.list(kind=JobKind.RECURRING)
            assert RECURRING_JOB_ID in {j.id for j in listing}
            print(f"Found job {RECURRING_JOB_ID!r} in the listing")

            # update a job
            job.name = "Nightly cache warm (v2)"
            job.set_retry_policy(retry_policy, environment="production")
            job.set_schedule(
                "30 2 * * *",
                timezone="America/Los_Angeles",
                environment="production",
            )
            await job.save()
            assert job.version == 2
            print(f"Updated job to v{job.version}")

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

            # get the last completed run in production
            recent = await job.list_runs(
                environment="production", last_run_only=True
            )
            print(f"Last completed production run(s): {len(recent)}")

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

            # create a manual job (no schedule, runs only when triggered)
            manual = jobs.new_manual_job(
                MANUAL_JOB_ID,
                name="On-demand reindex",
                configuration=HttpConfig(
                    method="POST", url="https://httpbin.org/post"
                ),
            )
            manual.set_enabled(True, environment="production")
            await manual.save()
            assert manual.is_manual() is True
            manual_run = await manual.trigger(environment="production")
            assert manual_run.trigger == RunTrigger.MANUAL
            print(
                f"Created manual job {manual.id!r} and triggered it on demand"
            )

            # schedule a one-off job to run tomorrow
            tomorrow = datetime.now() + timedelta(days=1)
            oneoff = jobs.schedule(
                ONEOFF_JOB_ID,
                name="One-shot reindex",
                schedule=tomorrow,
                configuration=HttpConfig(
                    method="POST", url="https://httpbin.org/post"
                ),
                environment="development",
            )
            await oneoff.save()
            assert oneoff.is_one_off() is True
            assert oneoff.is_enabled(environment="development") is True
            assert oneoff.environments["development"].next_run_at is not None
            print(f"Created one-off job {oneoff.id!r} to run in development")

            # delete a job
            await job.delete()
            assert RECURRING_JOB_ID not in {j.id for j in await jobs.list()}

            # delete the retry policy
            await retry_policy.delete()
            print(
                f"Deleted job {RECURRING_JOB_ID!r} and retry policy — jobs showcase complete."
            )
        finally:
            await cleanup_showcase(jobs)


if __name__ == "__main__":
    asyncio.run(main())
