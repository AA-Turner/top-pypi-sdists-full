"""dltHub platform SDK.

    import dlthub_sdk

    runtime = dlthub_sdk.connect(token="...")
    ws = runtime.workspaces.get(id="...")
    for job in ws.jobs.list():
        print(job.job_ref, job.paused)

The same calls, awaited, off ``connect_async``:

    runtime = dlthub_sdk.connect_async(token="...")
    ws = await runtime.workspaces.get(id="...")
    async for job in ws.jobs.list():
        print(job.job_ref, job.paused)

The entry point fixes the mode: nothing reached from ``connect`` returns an
awaitable, and everything reached from ``connect_async`` does.
"""

from __future__ import annotations

# Python internals
from typing import Mapping

# Current package
from dlthub_sdk._glue.context import Async, Sync, _Ctx
from dlthub_sdk._glue.keep import KEEP, Keep
from dlthub_sdk._glue.urls import DEFAULT_BASE_URL as _DEFAULT_BASE_URL
from dlthub_sdk.credentials import AsyncCredentials, Credentials
from dlthub_sdk.domain.caller import Caller, OrganizationMembership
from dlthub_sdk.domain.configurations import Configuration, Configurations
from dlthub_sdk.domain.dataplanes import Dataplane, Dataplanes
from dlthub_sdk.domain.deployments import Deployment, Deployments
from dlthub_sdk.domain.files import FileEntry
from dlthub_sdk.domain.job_runs import (
    CancelledRun,
    CancelReport,
    JobRun,
    JobRuns,
    JobRunStatus,
    PipelineRunSummary,
)
from dlthub_sdk.domain.jobs import (
    DeployManifest,
    DeployReport,
    Job,
    Jobs,
    JobType,
    TriggerResult,
    TriggerStatus,
)
from dlthub_sdk.domain.logs import LogLine
from dlthub_sdk.domain.organizations import (
    Membership,
    Organization,
    OrganizationCaller,
    Organizations,
)
from dlthub_sdk.domain.runtime import Runtime
from dlthub_sdk.domain.telemetry import (
    DatasetActivity,
    LoadPackage,
    PipelineActivity,
    PipelineRun,
    PipelineRuns,
    PipelineRunStatus,
    PipelineRunTrace,
    PipelineTable,
    Telemetry,
    TelemetryStatus,
)
from dlthub_sdk.domain.variables import (
    WORKSPACE_PROFILE,
    Variable,
    VariableChange,
    VariableChangeStatus,
    Variables,
    VariableScope,
)
from dlthub_sdk.domain.workspaces import (
    Workspace,
    WorkspaceCaller,
    WorkspaceMember,
    Workspaces,
)
from dlthub_sdk.errors import (
    ApiError,
    BadRequest,
    Conflict,
    ConnectionFailed,
    DlthubError,
    FieldError,
    InvalidResponse,
    NotAuthenticated,
    NotAuthorized,
    NotFound,
    ScopeMissing,
    ServerError,
    TransportError,
    TransportTimeout,
    UnboundEntity,
    WaitTimeout,
)


def connect(
    *,
    token: str | None = None,
    credentials: Credentials | None = None,
    base_url: str = _DEFAULT_BASE_URL,
    organization_id: str | None = None,
    verify_ssl: bool = True,
    headers: Mapping[str, str] | None = None,
) -> Runtime[Sync]:
    """Connect to the platform for blocking use.

    Args:
        token: An API key (``dlt_u_``/``dlt_sa_`` prefixed) or a user JWT, when
            the credential does not change. A JWT is not renewed, so a
            long-lived client should hold an API key or pass ``credentials``.
        credentials: Where to read the credential before each request, for one
            that rotates. Renewed once if the platform rejects it. Exactly one
            of this and ``token`` is required.
        base_url: Platform base URL. Override for local or staging.
        organization_id: Default organization, so ``workspaces.list()`` needs no
            argument.
        verify_ssl: Verify the platform's TLS certificate. Applies on both
            planes.
        headers: Sent with every request, on both planes.

    Returns:
        A blocking :class:`Runtime`.

    Raises:
        ValueError: Both ``token`` and ``credentials``, or neither.
    """
    # Current package
    from dlthub_sdk._glue.transport import HttpTransport  # noqa: PLC0415

    return Runtime(
        _Ctx[Sync](
            transport=HttpTransport(
                token,
                base_url=base_url,
                credentials=credentials,
                verify_ssl=verify_ssl,
                headers=headers,
            ),
            base_url=base_url,
            organization_id=organization_id,
        )
    )


def connect_async(
    *,
    token: str | None = None,
    credentials: AsyncCredentials | None = None,
    base_url: str = _DEFAULT_BASE_URL,
    organization_id: str | None = None,
    verify_ssl: bool = True,
    headers: Mapping[str, str] | None = None,
) -> Runtime[Async]:
    """Connect to the platform for awaited use.

    Args:
        token: As for :func:`connect`.
        credentials: As for :func:`connect`, awaited.
        base_url: Platform base URL. Override for local or staging.
        organization_id: Default organization, so ``workspaces.list()`` needs no
            argument.
        verify_ssl: As for :func:`connect`.
        headers: As for :func:`connect`.

    Returns:
        An awaiting :class:`Runtime`.

    Raises:
        ValueError: As for :func:`connect`.
    """
    # Current package
    from dlthub_sdk._glue.transport import AsyncHttpTransport  # noqa: PLC0415

    return Runtime(
        _Ctx[Async](
            transport=AsyncHttpTransport(
                token,
                base_url=base_url,
                credentials=credentials,
                verify_ssl=verify_ssl,
                headers=headers,
            ),
            base_url=base_url,
            organization_id=organization_id,
        )
    )


__all__ = [
    "KEEP",
    "WORKSPACE_PROFILE",
    "ApiError",
    "Async",
    "AsyncCredentials",
    "BadRequest",
    "Caller",
    "CancelReport",
    "CancelledRun",
    "Configuration",
    "Configurations",
    "Conflict",
    "ConnectionFailed",
    "Credentials",
    "Dataplane",
    "Dataplanes",
    "DatasetActivity",
    "DeployManifest",
    "DeployReport",
    "Deployment",
    "Deployments",
    "DlthubError",
    "FieldError",
    "FileEntry",
    "InvalidResponse",
    "Job",
    "JobRun",
    "JobRunStatus",
    "JobRuns",
    "JobType",
    "Jobs",
    "Keep",
    "LoadPackage",
    "LogLine",
    "Membership",
    "NotAuthenticated",
    "NotAuthorized",
    "NotFound",
    "Organization",
    "OrganizationCaller",
    "OrganizationMembership",
    "Organizations",
    "PipelineActivity",
    "PipelineRun",
    "PipelineRunStatus",
    "PipelineRunSummary",
    "PipelineRunTrace",
    "PipelineRuns",
    "PipelineTable",
    "Runtime",
    "ScopeMissing",
    "ServerError",
    "Sync",
    "Telemetry",
    "TelemetryStatus",
    "TransportError",
    "TransportTimeout",
    "TriggerResult",
    "TriggerStatus",
    "UnboundEntity",
    "Variable",
    "VariableChange",
    "VariableChangeStatus",
    "VariableScope",
    "Variables",
    "WaitTimeout",
    "Workspace",
    "WorkspaceCaller",
    "WorkspaceMember",
    "Workspaces",
    "connect",
    "connect_async",
]
