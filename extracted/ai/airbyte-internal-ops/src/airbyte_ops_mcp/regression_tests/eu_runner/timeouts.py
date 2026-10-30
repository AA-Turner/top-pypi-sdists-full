# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""Cloud Batch duration helpers."""


def max_run_duration_seconds(
    github_timeout_minutes: int, elapsed_seconds: int, margin_minutes: int = 10
) -> int:
    """Return the Batch deadline: what the GitHub job has left, less a margin.

    A Batch job that outlives the GitHub job is never read: the run is
    cancelled, nothing downloads its verdict, and the cleanup step deletes it.
    The margin covers the VM's provisioning, which the deadline does not
    count, and the steps after the job ends: the next poll, the verdict
    download, the summary and Finalize.
    """
    deadline = (github_timeout_minutes - margin_minutes) * 60 - elapsed_seconds
    if deadline <= 0:
        raise ValueError(
            f"The GitHub job has no time left for a Batch job: {elapsed_seconds}s "
            f"of its {github_timeout_minutes} minutes are gone, and the last "
            f"{margin_minutes} are kept for reading the result"
        )
    return deadline
