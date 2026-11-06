"""Cross-cluster migration jobs.

See :class:`~novita_sandbox.core.job.job_sync.Job` for the synchronous API and
:class:`~novita_sandbox.core.job.job_async.AsyncJob` for the asynchronous one.
"""

from .errors import (
    CancelTooLateError,
    JobCancelledError,
    JobFailedError,
    MigrationConflictError,
    MigrationNotSupportedError,
    ResourceAlreadyMigratingError,
    SharedDependencyError,
    TemplateAliasConflictError,
)
from .job_async import AsyncJob
from .job_sync import AliasArg, Job
from .types import (
    TERMINAL_JOB_STATUSES,
    JobPage,
    JobStatus,
    JobType,
    MigrationItemStatus,
    MigrationStatus,
)

__all__ = [
    "AliasArg",
    "AsyncJob",
    "CancelTooLateError",
    "Job",
    "JobCancelledError",
    "JobFailedError",
    "JobPage",
    "JobStatus",
    "JobType",
    "MigrationConflictError",
    "MigrationItemStatus",
    "MigrationNotSupportedError",
    "MigrationStatus",
    "ResourceAlreadyMigratingError",
    "SharedDependencyError",
    "TERMINAL_JOB_STATUSES",
    "TemplateAliasConflictError",
]
