"""Smpl Jobs SDK namespace.

Smpl Jobs runs an HTTP call on a schedule (a 5-field cron expression, a
one-off datetime, or ``now``) or on demand (a manual job with no schedule),
and records the run history for each fire — the request sent, the response
received, timing, and outcome.

Reachable as ``client.jobs`` on :class:`smplkit.SmplClient`, or constructed
directly via :class:`JobsClient` (sync) / :class:`AsyncJobsClient` (async)
for callers that only need jobs.

The shared dataclasses (:class:`Job`, :class:`AsyncJob`, :class:`Run`,
:class:`Usage`, :class:`HttpConfig`, :class:`RetryPolicy`, :class:`RetryOn`)
are re-exported here.
"""

from smplkit.jobs.clients import (
    AsyncJob,
    AsyncRetryPoliciesClient,
    AsyncRetryPolicy,
    AsyncRun,
    AsyncRunsClient,
    Backoff,
    HttpConfig,
    Job,
    JobEnvironment,
    JobKind,
    RetryOn,
    RetryPoliciesClient,
    RetryPolicy,
    RetryReason,
    Run,
    RunRetry,
    RunsClient,
    RunTrigger,
    Usage,
)

__all__ = [
    "AsyncJob",
    "AsyncRetryPoliciesClient",
    "AsyncRetryPolicy",
    "AsyncRun",
    "AsyncRunsClient",
    "Backoff",
    "HttpConfig",
    "Job",
    "JobEnvironment",
    "JobKind",
    "RetryOn",
    "RetryPoliciesClient",
    "RetryPolicy",
    "RetryReason",
    "Run",
    "RunRetry",
    "RunsClient",
    "RunTrigger",
    "Usage",
]
