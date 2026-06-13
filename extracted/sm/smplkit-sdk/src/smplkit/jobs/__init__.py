"""Smpl Jobs SDK namespace.

Smpl Jobs runs an HTTP call on a schedule (a 5-field cron expression, a
one-off datetime, or ``now``) and records the run history for each fire —
the request sent, the response received, timing, and outcome.

Reachable as ``client.jobs`` on :class:`smplkit.SmplClient`, or constructed
directly via :class:`JobsClient` (sync) / :class:`AsyncJobsClient` (async)
for callers that only need jobs.

The shared dataclasses (:class:`Job`, :class:`AsyncJob`, :class:`Run`,
:class:`Usage`, :class:`HttpConfig`) are re-exported here.
"""

from smplkit.jobs.clients import (
    AsyncJob,
    AsyncRunsClient,
    HttpConfig,
    Job,
    Run,
    RunsClient,
    Usage,
)

__all__ = [
    "AsyncJob",
    "AsyncRunsClient",
    "HttpConfig",
    "Job",
    "Run",
    "RunsClient",
    "Usage",
]
