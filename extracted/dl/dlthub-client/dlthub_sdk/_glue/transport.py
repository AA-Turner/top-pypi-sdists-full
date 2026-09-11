"""Transport: the only layer that touches generated clients.

Each method wraps one generated operation and goes through :func:`_call` or
:func:`_acall`, which guard the network and unwrap the ``Response`` union, so
neither a generated error model nor an ``httpx`` error reaches a caller.
``domain`` reaches these through :class:`~dlthub_sdk._glue.context._Ctx`.
"""

from __future__ import annotations

# Python internals
import json
import time
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from http import HTTPStatus
from io import BytesIO
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncGenerator,
    AsyncIterator,
    Awaitable,
    BinaryIO,
    Callable,
    Generator,
    Generic,
    Iterable,
    Iterator,
    Mapping,
    Protocol,
    Sequence,
    TypeVar,
    cast,
)
from urllib.parse import urlparse
from uuid import UUID

# Other libraries
import httpx

# Current package
from dlthub_sdk._gen.api.api.configurations import (
    create_configuration,
    get_configuration,
    get_latest_configuration,
    list_configurations,
)
from dlthub_sdk._gen.api.api.dataplanes import list_dataplanes
from dlthub_sdk._gen.api.api.deployments import (
    create_deployment,
    get_deployment,
    get_latest_deployment,
    list_deployments,
)
from dlthub_sdk._gen.api.api.me import get_current_user, organization_me, workspace_me
from dlthub_sdk._gen.api.api.organizations import (
    get_organization,
    list_organizations,
    set_organization_region,
)
from dlthub_sdk._gen.api.api.runs import (
    bulk_cancel_runs,
    cancel_run,
    create_run,
    get_latest_run,
    get_run,
    list_runs,
)
from dlthub_sdk._gen.api.api.scripts import (
    disable_public_url,
    enable_public_url,
    get_script,
    list_scripts,
    pause_script,
    resume_script,
    trigger_jobs,
)
from dlthub_sdk._gen.api.api.workspaces import (
    create_workspace,
    deploy,
    get_workspace,
    get_workspace_dataplane_access_token,
    list_workspace_members,
    list_workspaces,
    update_workspace,
)
from dlthub_sdk._gen.api.client import AuthenticatedClient, Client
from dlthub_sdk._gen.api.models import (
    BulkCancelRequest,
    BulkCancelResponse,
    ConfigurationResponse,
    CreateRunRequest,
    CurrentUserResponse,
    DataplaneAccessTokenResponse,
    DataplaneInfo,
    DeployManifestRequest,
    DeployManifestResponse,
    DeploymentResponse,
    DetailedRunResponse,
    DetailedScriptResponse,
    ListConfigurationsResponse200,
    ListDeploymentsResponse200,
    ListOrganizationsResponse200,
    ListRunsResponse200,
    ListScriptsResponse200,
    ListWorkspaceMembersResponse200,
    ListWorkspacesResponse200,
    OrganizationMeResponse,
    OrganizationResponse,
    ScriptResponse,
    SetOrganizationRegionRequest,
    TJobDefinition,
    TriggeredJob,
    TriggerJobsRequest,
    TriggerJobsResponse,
    UploadInitiatedResponse,
    WorkspaceCreateRequest,
    WorkspaceMeResponse,
    WorkspaceResponse,
    WorkspaceUpdateRequest,
)
from dlthub_sdk._gen.api.types import UNSET as API_UNSET
from dlthub_sdk._gen.dataplane_api.api.files import (
    get_configuration_files_manifest,
    get_deployment_files_manifest,
)
from dlthub_sdk._gen.dataplane_api.api.uploads import (
    upload_configuration_bytes,
    upload_deployment_bytes,
)
from dlthub_sdk._gen.dataplane_api.api.variables import (
    change_workspace_variables,
    list_workspace_variables,
)
from dlthub_sdk._gen.dataplane_api.client import (
    AuthenticatedClient as DataplaneApiClient,
)
from dlthub_sdk._gen.dataplane_api.models import (
    ConfigurationResponse as DataplaneConfigurationResponse,
    DeploymentResponse as DataplaneDeploymentResponse,
    DeploymentUploadBody,
    PlainVariableUpsert,
    SecretVariableUpsert,
    TFilesManifest,
    UploadConfigurationBytesBody,
    VariablesChange,
    VariablesChangeResponse,
    WorkspaceVariablesResponse,
)
from dlthub_sdk._gen.dataplane_api.types import UNSET as DATAPLANE_UNSET, File
from dlthub_sdk._gen.logs.models import LogLine
from dlthub_sdk._gen.telemetry.api.default import (
    get_pipeline_run,
    get_pipeline_run_trace,
    get_telemetry_watermark,
    list_dataset_overview,
    list_pipeline_overview,
    list_pipeline_runs,
)
from dlthub_sdk._gen.telemetry.client import AuthenticatedClient as TelemetryClient
from dlthub_sdk._gen.telemetry.models import (
    GetPipelineRunTraceResponse200,
    ListDatasetOverviewResponse200,
    ListPipelineOverviewResponse200,
    ListPipelineRunsResponse200,
    PipelineRunDetailResponse,
    PipelineRunStatus as GenPipelineRunStatus,
    TelemetryWatermarkResponse,
)
from dlthub_sdk._gen.telemetry.types import UNSET as TELEMETRY_UNSET
from dlthub_sdk._glue.enums import EntityKind
from dlthub_sdk._glue.keep import KEEP, Keep
from dlthub_sdk._glue.urls import DEFAULT_BASE_URL, segment
from dlthub_sdk.credentials import AsyncCredentials, Credentials, _AsyncStatic, _Static
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
    ServerError,
    TransportError,
    TransportTimeout,
)

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
#: The error models an operation declares alongside its success model.
E = TypeVar("E")
#: What a reply parsed to, invariant so a mismatched _Op cannot type-check.
P = TypeVar("P")


class _Reply(Protocol[P]):
    """What :func:`_unwrap` reads off a generated response, on either plane.

    ``P`` is invariant on purpose: it is what makes a mismatched :class:`_Op`
    a type error rather than an ``InvalidResponse`` at runtime.
    """

    status_code: HTTPStatus
    content: bytes
    parsed: P


@dataclass
class _Minted:
    """A workspace's data-plane client and when its token stops being valid."""

    client: DataplaneApiClient
    expires_at: int


#: Re-mint this many seconds before expiry, so a call cannot race the deadline.
_TOKEN_MARGIN = 60


def _cached_dataplane(
    held: _Minted | None, *, remint: bool
) -> DataplaneApiClient | None:
    """The cache test both transports start with.

    Args:
        held: What the cache holds for this workspace, if anything.
        remint: Ignore a cached token, however fresh.

    Returns:
        The held client while its token is good for another `_TOKEN_MARGIN`
        seconds, else ``None``.
    """
    if held is None or remint:
        return None
    if held.expires_at <= time.time() + _TOKEN_MARGIN:
        return None
    return held.client


def _hold_dataplane(
    minted: DataplaneAccessTokenResponse,
    dataplane_url: str,
    verify_ssl: bool,
    headers: Mapping[str, str],
) -> _Minted:
    """Wrap a freshly minted token in the client that carries it.

    Args:
        minted: The token the platform just issued.
        dataplane_url: Data plane the client will reach.
        verify_ssl: The caller's TLS choice, which applies on both planes.
        headers: Sent with every request.

    Returns:
        The client to cache for this workspace.
    """
    return _Minted(
        client=DataplaneApiClient(
            base_url=dataplane_url,
            token=minted.token,
            verify_ssl=verify_ssl,
            headers=dict(headers),
        ),
        expires_at=minted.expires_at,
    )


def _as_telemetry(client: DataplaneApiClient) -> TelemetryClient:
    """Reuse the data plane's client for a telemetry call.

    Telemetry is another service on the same host behind the same
    `DataplaneUserJwt`, and its generated ops touch only `get_httpx_client`
    and `raise_on_unexpected_status`. The two generated `AuthenticatedClient`
    classes are identical in shape but not in name, so this narrows once
    rather than at every call.

    Args:
        client: The minted data-plane client.

    Returns:
        The same client, typed for the telemetry operations.
    """
    return cast(TelemetryClient, client)


def _logs_path(route: str, workspace_id: str, run_id: str) -> str:
    """Fill one of the log routes in, escaping both ids.

    Args:
        route: The route template.
        workspace_id: Whose logs to read.
        run_id: The run being read.

    Returns:
        The path to request.
    """
    return route.format(workspace_id=segment(workspace_id), run_id=segment(run_id))


def _bearer(request: httpx.Request, token: str) -> None:
    """Attach a credential to one request.

    Args:
        request: The request going out.
        token: The credential to present.
    """
    request.headers["Authorization"] = f"Bearer {token}"


@dataclass(frozen=True)
class _Op(Generic[T]):
    """One operation's success model and entity kind, shared by both transports."""

    model: type[T]
    kind: EntityKind


_ORGANIZATION: _Op[OrganizationResponse] = _Op(
    OrganizationResponse, EntityKind.ORGANIZATION
)
_ORGANIZATION_LIST: _Op[ListOrganizationsResponse200] = _Op(
    ListOrganizationsResponse200, EntityKind.ORGANIZATION
)
#: `/user` is gated to human principals, so an API key cannot reach it.
_CURRENT_USER: _Op[CurrentUserResponse] = _Op(
    CurrentUserResponse, EntityKind.ORGANIZATION
)
_ORGANIZATION_ME: _Op[OrganizationMeResponse] = _Op(
    OrganizationMeResponse, EntityKind.ORGANIZATION
)
_WORKSPACE_ME: _Op[WorkspaceMeResponse] = _Op(WorkspaceMeResponse, EntityKind.WORKSPACE)
_CONFIGURATION: _Op[ConfigurationResponse] = _Op(
    ConfigurationResponse, EntityKind.CONFIGURATION
)
_CONFIGURATION_LIST: _Op[ListConfigurationsResponse200] = _Op(
    ListConfigurationsResponse200, EntityKind.WORKSPACE
)
_CONFIGURATION_FILES: _Op[TFilesManifest] = _Op(
    TFilesManifest, EntityKind.CONFIGURATION
)
_DEPLOYMENT: _Op[DeploymentResponse] = _Op(DeploymentResponse, EntityKind.DEPLOYMENT)
#: The upload answers with the data plane's own class. Structurally identical to
#: the control plane's, and `isinstance` still tells them apart — so an upload
#: needs its own op or `_unwrap` rejects a perfectly good response.
_DP_DEPLOYMENT: _Op[DataplaneDeploymentResponse] = _Op(
    DataplaneDeploymentResponse, EntityKind.DEPLOYMENT
)
_DP_CONFIGURATION: _Op[DataplaneConfigurationResponse] = _Op(
    DataplaneConfigurationResponse, EntityKind.CONFIGURATION
)
_DEPLOYMENT_FILES: _Op[TFilesManifest] = _Op(TFilesManifest, EntityKind.DEPLOYMENT)
_DEPLOYMENT_LIST: _Op[ListDeploymentsResponse200] = _Op(
    ListDeploymentsResponse200, EntityKind.WORKSPACE
)
_BULK_CANCEL: _Op[BulkCancelResponse] = _Op(BulkCancelResponse, EntityKind.WORKSPACE)
#: The platform answers with a bare array, so the check is against ``list``.
_DATAPLANE_LIST: _Op[list[DataplaneInfo]] = _Op(list, EntityKind.DATAPLANE)
_RUN: _Op[DetailedRunResponse] = _Op(DetailedRunResponse, EntityKind.JOB_RUN)
_RUN_LIST: _Op[ListRunsResponse200] = _Op(ListRunsResponse200, EntityKind.WORKSPACE)
_DATAPLANE_TOKEN: _Op[DataplaneAccessTokenResponse] = _Op(
    DataplaneAccessTokenResponse, EntityKind.WORKSPACE
)
_TRIGGERED_JOB: _Op[TriggeredJob] = _Op(TriggeredJob, EntityKind.JOB)
_VARIABLE_CHANGE: _Op[VariablesChangeResponse] = _Op(
    VariablesChangeResponse, EntityKind.VARIABLE
)
_TELEMETRY_WATERMARK: _Op[TelemetryWatermarkResponse] = _Op(
    TelemetryWatermarkResponse, EntityKind.WORKSPACE
)
_PIPELINE_RUN: _Op[PipelineRunDetailResponse] = _Op(
    PipelineRunDetailResponse, EntityKind.PIPELINE_RUN
)
_PIPELINE_RUN_LIST: _Op[ListPipelineRunsResponse200] = _Op(
    ListPipelineRunsResponse200, EntityKind.WORKSPACE
)
_PIPELINE_RUN_TRACE: _Op[GetPipelineRunTraceResponse200] = _Op(
    GetPipelineRunTraceResponse200, EntityKind.PIPELINE_RUN
)
_PIPELINE_OVERVIEW: _Op[ListPipelineOverviewResponse200] = _Op(
    ListPipelineOverviewResponse200, EntityKind.WORKSPACE
)
_DATASET_OVERVIEW: _Op[ListDatasetOverviewResponse200] = _Op(
    ListDatasetOverviewResponse200, EntityKind.WORKSPACE
)
_VARIABLES: _Op[WorkspaceVariablesResponse] = _Op(
    WorkspaceVariablesResponse, EntityKind.WORKSPACE
)
_TRIGGERED_JOBS: _Op[TriggerJobsResponse] = _Op(
    TriggerJobsResponse, EntityKind.WORKSPACE
)
_WORKSPACE: _Op[WorkspaceResponse] = _Op(WorkspaceResponse, EntityKind.WORKSPACE)
_WORKSPACE_LIST: _Op[ListWorkspacesResponse200] = _Op(
    ListWorkspacesResponse200, EntityKind.ORGANIZATION
)
_WORKSPACE_MEMBER_LIST: _Op[ListWorkspaceMembersResponse200] = _Op(
    ListWorkspaceMembersResponse200, EntityKind.WORKSPACE
)
_SCRIPT_DETAIL: _Op[DetailedScriptResponse] = _Op(
    DetailedScriptResponse, EntityKind.JOB
)
_SCRIPT_LIST: _Op[ListScriptsResponse200] = _Op(
    ListScriptsResponse200, EntityKind.WORKSPACE
)
_SCRIPT: _Op[ScriptResponse] = _Op(ScriptResponse, EntityKind.JOB)
_LOG: _Op[LogLine] = _Op(LogLine, EntityKind.JOB_RUN)

#: The logs service is reached on the workspace's own data plane, so its reads go
#: through the client already minted for that plane rather than a second one.
_LOGS_READ = "/logs/v1/workspaces/{workspace_id}/runs/{run_id}/logs"
_LOGS_STREAM = _LOGS_READ + "/stream"
_NDJSON = "application/x-ndjson"
_SSE = "text/event-stream"

#: A live stream is idle between lines, so only the connect half may time out.
_STREAM_TIMEOUT = httpx.Timeout(30.0, read=None)

#: Not following means "replay what is there and stop", and the platform never
#: says where the replay ends — a gap this long is what stands in for it.
_REPLAY_TIMEOUT = httpx.Timeout(30.0, read=1.0)

#: A workspace can be large and the server parses the tarball before answering.
_UPLOAD_TIMEOUT = httpx.Timeout(300.0, connect=30.0)

_TAR_MIME = "application/x-tar"
_JSON_MIME = "application/json"

_DEPLOY_REPORT: _Op[DeployManifestResponse] = _Op(
    DeployManifestResponse, EntityKind.JOB
)
_DEPLOYMENT_UPLOAD: _Op[UploadInitiatedResponse] = _Op(
    UploadInitiatedResponse, EntityKind.DEPLOYMENT
)
_CONFIGURATION_UPLOAD: _Op[UploadInitiatedResponse] = _Op(
    UploadInitiatedResponse, EntityKind.CONFIGURATION
)


C = TypeVar("C")


def _one_credential(
    token: str | None, credentials: C | None, wrap: Callable[[str], C]
) -> C:
    """Resolve the two ways of naming a credential down to one.

    Args:
        token: A static token, if that is how the caller named it.
        credentials: A rotating credential, if that is how they named it.
        wrap: Turns a static token into the same shape.

    Returns:
        Whichever was given.

    Raises:
        ValueError: Both were given, or neither.
    """
    if token is not None and credentials is not None:
        raise ValueError(
            "pass token or credentials, not both — credentials already say "
            "where the token comes from"
        )
    if credentials is not None:
        return credentials
    if token is None:
        raise ValueError("pass a token, or credentials that supply one")
    return wrap(token)


class _CredentialsAuth(httpx.Auth):
    """Attaches the caller's credential, and renews it once if it is rejected.

    The control-plane twin of the data plane's re-mint-once-on-401: the SDK owns
    the client either way, and only where the token comes from differs.
    """

    def __init__(self, credentials: Credentials) -> None:
        self._credentials = credentials

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        _bearer(request, self._credentials.token())
        response = yield request
        if response.status_code != HTTPStatus.UNAUTHORIZED:
            return
        fresh = self._credentials.refreshed()
        if fresh is None:
            # _unwrap turns the 401 the caller still holds into NotAuthenticated.
            return
        _bearer(request, fresh)
        yield request


class _AsyncCredentialsAuth(httpx.Auth):
    """The awaited twin of :class:`_CredentialsAuth`.

    ``async_auth_flow`` is implemented rather than inherited: httpx would
    otherwise run the sync flow in a worker thread and await nothing.
    """

    def __init__(self, credentials: AsyncCredentials) -> None:
        self._credentials = credentials

    async def async_auth_flow(
        self, request: httpx.Request
    ) -> AsyncGenerator[httpx.Request, httpx.Response]:
        _bearer(request, await self._credentials.token())
        response = yield request
        if response.status_code != HTTPStatus.UNAUTHORIZED:
            return
        fresh = await self._credentials.refreshed()
        if fresh is None:
            return
        _bearer(request, fresh)
        yield request


class Transport(Protocol):
    """What ``domain`` may ask of the network. Fake this in tests."""

    def get_organization(self, *, organization_id: str) -> OrganizationResponse: ...

    def get_current_user(self) -> CurrentUserResponse: ...

    def organization_me(self, *, organization_id: str) -> OrganizationMeResponse: ...

    def workspace_me(self, *, workspace_id: str) -> WorkspaceMeResponse: ...

    def list_organizations(
        self, *, limit: int, offset: int
    ) -> ListOrganizationsResponse200: ...

    def set_organization_region(
        self, *, organization_id: str, dataplane_id: str
    ) -> OrganizationResponse: ...

    def create_workspace(
        self, *, organization_id: str, name: str, description: str | None
    ) -> WorkspaceResponse: ...

    def enable_public_url(
        self, *, workspace_id: str, job_ref: str
    ) -> ScriptResponse: ...

    def disable_public_url(
        self, *, workspace_id: str, job_ref: str
    ) -> ScriptResponse: ...

    def trigger_jobs(
        self,
        *,
        workspace_id: str,
        job_refs: Sequence[str] | None,
        selectors: Sequence[str] | None,
        profile: str | None | Keep,
        refresh: bool,
        dry_run: bool,
    ) -> TriggerJobsResponse: ...

    def create_run(
        self,
        *,
        workspace_id: str,
        job_ref: str,
        trigger: str,
        profile: str | None | Keep,
        refresh: bool,
        skip_freshness: bool,
    ) -> TriggeredJob: ...

    def change_variables(
        self,
        *,
        workspace_id: str,
        dataplane_url: str,
        profile: str | None,
        plain: Mapping[str, str],
        secret: Mapping[str, str],
        deletes: Sequence[str],
    ) -> VariablesChangeResponse: ...

    def list_variables(
        self,
        *,
        workspace_id: str,
        dataplane_url: str,
        profile: str | Keep,
        workspace: bool,
    ) -> WorkspaceVariablesResponse: ...

    def get_workspace(self, *, workspace_id: str) -> WorkspaceResponse: ...

    def list_workspaces(
        self, *, organization_id: str, limit: int, offset: int
    ) -> ListWorkspacesResponse200: ...

    def list_workspace_members(
        self, *, workspace_id: str, limit: int, offset: int
    ) -> ListWorkspaceMembersResponse200: ...

    def update_workspace(
        self, *, workspace_id: str, name: str | Keep, description: str | None | Keep
    ) -> WorkspaceResponse: ...

    def list_dataplanes(self) -> list[DataplaneInfo]: ...

    def get_run(self, *, workspace_id: str, run_id: str) -> DetailedRunResponse: ...

    def get_latest_run(
        self, *, workspace_id: str, job_id: str | None
    ) -> DetailedRunResponse: ...

    def list_runs(
        self, *, workspace_id: str, job_id: str | None, limit: int, offset: int
    ) -> ListRunsResponse200: ...

    def cancel_run(self, *, workspace_id: str, run_id: str) -> DetailedRunResponse: ...

    def cancel_runs(
        self, *, workspace_id: str, job_refs: Sequence[str], dry_run: bool
    ) -> BulkCancelResponse: ...

    def get_telemetry_watermark(
        self, *, workspace_id: str, dataplane_url: str
    ) -> TelemetryWatermarkResponse: ...

    def get_pipeline_run(
        self, *, workspace_id: str, dataplane_url: str, pipeline_run_id: str
    ) -> PipelineRunDetailResponse: ...

    def get_pipeline_run_trace(
        self, *, workspace_id: str, dataplane_url: str, pipeline_run_id: str
    ) -> GetPipelineRunTraceResponse200: ...

    def list_pipeline_overview(
        self,
        *,
        workspace_id: str,
        dataplane_url: str,
        start: datetime,
        end: datetime,
        pipeline_name: str | None,
        latest_status: str | None,
        latest_destination_name: str | None,
        limit: int,
        offset: int,
    ) -> ListPipelineOverviewResponse200: ...

    def list_dataset_overview(
        self,
        *,
        workspace_id: str,
        dataplane_url: str,
        start: datetime,
        end: datetime,
        dataset_name: str | None,
        latest_status: str | None,
        latest_destination_name: str | None,
        limit: int,
        offset: int,
    ) -> ListDatasetOverviewResponse200: ...

    def list_pipeline_runs(
        self,
        *,
        workspace_id: str,
        dataplane_url: str,
        start: datetime,
        end: datetime,
        job_run_id: str | None,
        pipeline_name: str | None,
        status: str | None,
        dataset_name: str | None,
        destination_name: str | None,
        is_empty_run: bool | None,
        limit: int,
        offset: int,
    ) -> ListPipelineRunsResponse200: ...

    def get_configuration_files(
        self, *, workspace_id: str, dataplane_url: str, configuration_id: str
    ) -> TFilesManifest: ...

    def get_deployment_files(
        self, *, workspace_id: str, dataplane_url: str, deployment_id: str
    ) -> TFilesManifest: ...

    def get_configuration(
        self, *, workspace_id: str, version: int
    ) -> ConfigurationResponse: ...

    def get_latest_configuration(
        self, *, workspace_id: str
    ) -> ConfigurationResponse: ...

    def list_configurations(
        self, *, workspace_id: str, limit: int, offset: int
    ) -> ListConfigurationsResponse200: ...

    def get_deployment(
        self, *, workspace_id: str, version: int
    ) -> DeploymentResponse: ...

    def get_latest_deployment(self, *, workspace_id: str) -> DeploymentResponse: ...

    def list_deployments(
        self, *, workspace_id: str, limit: int, offset: int
    ) -> ListDeploymentsResponse200: ...

    def get_script(
        self, *, workspace_id: str, job_ref: str
    ) -> DetailedScriptResponse: ...

    def list_scripts(
        self, *, workspace_id: str, limit: int, offset: int, archived: bool | Keep
    ) -> ListScriptsResponse200: ...

    def pause_script(self, *, workspace_id: str, job_ref: str) -> ScriptResponse: ...

    def resume_script(self, *, workspace_id: str, job_ref: str) -> ScriptResponse: ...

    def upload_deployment(
        self,
        *,
        workspace_id: str,
        code: bytes | BinaryIO,
        requirements: bytes | BinaryIO,
    ) -> DataplaneDeploymentResponse: ...

    def upload_configuration(
        self, *, workspace_id: str, data: bytes | BinaryIO
    ) -> DataplaneConfigurationResponse: ...

    def deploy_manifest(
        self,
        *,
        workspace_id: str,
        jobs: Sequence[Mapping[str, Any]],
        manifest_hash: str,
        engine_version: int,
        module: str | None,
        description: str | None | Keep,
        dry_run: bool,
    ) -> DeployManifestResponse: ...

    def read_logs(
        self, *, workspace_id: str, dataplane_url: str, run_id: str
    ) -> Iterator[LogLine]: ...

    def stream_logs(
        self, *, workspace_id: str, dataplane_url: str, run_id: str, follow: bool
    ) -> Iterator[LogLine]: ...

    def close(self) -> None: ...


class HttpTransport:
    """`Transport` over the generated sync clients."""

    def __init__(
        self,
        token: str | None = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        credentials: Credentials | None = None,
        verify_ssl: bool = True,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        """Hold the clients this transport calls through.

        Exactly one of ``token`` and ``credentials`` says how to authenticate
        the control plane.

        Args:
            token: A credential that does not change. Wrapped so there is one
                credential path.
            base_url: Control-plane base URL.
            credentials: Where to read the credential before each request, for
                one that rotates. Renewed once if the platform rejects it.
            verify_ssl: Applied to every client this transport builds, the
                per-workspace and per-upload data-plane ones included, so a
                caller's TLS choice cannot be confined to one plane.
            headers: Applied the same way.

        Raises:
            ValueError: Both ``token`` and ``credentials``, or neither.
        """
        self._credentials = _one_credential(token, credentials, _Static)
        self._api = Client(
            base_url=base_url,
            verify_ssl=verify_ssl,
            headers=dict(headers or {}),
            httpx_args={"auth": _CredentialsAuth(self._credentials)},
        )
        self._base_url = base_url
        self._verify_ssl = verify_ssl
        self._headers = dict(headers or {})
        self._dataplane_clients: dict[str, _Minted] = {}

    def __repr__(self) -> str:
        # Never repr a client: they hold raw tokens, the minted ones included.
        return f"<HttpTransport base_url={self._base_url!r} token='***'>"

    def close(self) -> None:
        """Close every connection this transport opened, on either plane."""
        _shut(self._api)
        for held in self._dataplane_clients.values():
            _shut(held.client)
        self._dataplane_clients.clear()

    def _dataplane_client(
        self, workspace_id: str, dataplane_url: str, *, remint: bool = False
    ) -> DataplaneApiClient:
        """Return a data-plane client for one workspace, minting a token as needed.

        Keyed by workspace, since one token covers every capability the
        caller's role allows. Concurrent callers may both mint; last write wins.

        Args:
            workspace_id: Whose data plane to reach.
            dataplane_url: That data plane's base URL.
            remint: Ignore a cached token, however fresh.

        Returns:
            A client carrying an unexpired token.
        """
        held = self._dataplane_clients.get(workspace_id)
        cached = _cached_dataplane(held, remint=remint)
        if cached is not None:
            return cached
        minted = _unwrap(
            get_workspace_dataplane_access_token.sync_detailed(
                UUID(workspace_id), client=self._api
            ),
            _DATAPLANE_TOKEN,
            workspace_id,
        )
        fresh = _hold_dataplane(minted, dataplane_url, self._verify_ssl, self._headers)
        if held is not None:
            _shut(held.client)
        self._dataplane_clients[workspace_id] = fresh
        return fresh.client

    def _dataplane_call(
        self,
        fetch: Callable[[DataplaneApiClient], _Reply[T | E]],
        op: _Op[T],
        ref: str | None,
        *,
        workspace_id: str,
        dataplane_url: str,
    ) -> T:
        """Perform one data-plane call, re-minting once if the token is rejected.

        Args:
            fetch: Performs the generated call against the data-plane client.
            op: The operation's success model and entity kind.
            ref: The id or name being addressed.
            workspace_id: Whose data plane to reach.
            dataplane_url: That data plane's base URL.

        Returns:
            The parsed success model.
        """
        with _transport_errors(op.kind, ref):
            resp = fetch(self._dataplane_client(workspace_id, dataplane_url))
            if resp.status_code == HTTPStatus.UNAUTHORIZED:
                # The SDK minted this token, so a rejection may just mean it
                # aged out mid-flight; the caller's own credential is untouched.
                resp = fetch(
                    self._dataplane_client(workspace_id, dataplane_url, remint=True)
                )
        return _unwrap(resp, op, ref)

    def _dataplane_logs(
        self,
        path: str,
        *,
        workspace_id: str,
        dataplane_url: str,
        run_id: str,
        sse: bool,
        follow: bool = True,
    ) -> Iterator[LogLine]:
        """Read one log body off the data plane, re-minting once if rejected.

        Hand-built rather than generated: the spec declares the success body as
        ``application/x-ndjson``, which openapi-python-client does not parse, so
        both log operations generate with no usable model.

        Args:
            path: The logs route, already formatted.
            workspace_id: Whose data plane to reach.
            dataplane_url: That data plane's base URL.
            run_id: The run being read.
            sse: Whether the body is SSE rather than NDJSON.
            follow: Keep the stream open. False replays what is already there
                and stops, which the platform marks only by going quiet.

        Yields:
            One generated model per log line.
        """
        with _transport_errors(EntityKind.JOB_RUN, run_id):
            remint = False
            while True:
                client = self._dataplane_client(
                    workspace_id, dataplane_url, remint=remint
                )
                with client.get_httpx_client().stream(
                    "GET",
                    path,
                    headers={"Accept": _SSE if sse else _NDJSON},
                    timeout=_stream_timeout(sse, follow),
                ) as resp:
                    if resp.status_code == HTTPStatus.UNAUTHORIZED and not remint:
                        remint = True
                        continue
                    if resp.status_code != HTTPStatus.OK:
                        resp.read()
                        _unwrap(
                            _StreamReply(HTTPStatus(resp.status_code), resp.content),
                            _LOG,
                            run_id,
                        )
                    yield from _log_rows(resp.iter_lines(), run_id, sse)
                    return

    def read_logs(
        self, *, workspace_id: str, dataplane_url: str, run_id: str
    ) -> Iterator[LogLine]:
        return self._dataplane_logs(
            _logs_path(_LOGS_READ, workspace_id, run_id),
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
            run_id=run_id,
            sse=False,
        )

    def stream_logs(
        self, *, workspace_id: str, dataplane_url: str, run_id: str, follow: bool
    ) -> Iterator[LogLine]:
        return self._dataplane_logs(
            _logs_path(_LOGS_STREAM, workspace_id, run_id),
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
            run_id=run_id,
            sse=True,
            follow=follow,
        )

    def list_dataplanes(self) -> list[DataplaneInfo]:
        return _call(
            lambda: list_dataplanes.sync_detailed(client=self._api),
            _DATAPLANE_LIST,
            None,
        )

    def get_run(self, *, workspace_id: str, run_id: str) -> DetailedRunResponse:
        return _call(
            lambda: get_run.sync_detailed(
                UUID(workspace_id), UUID(run_id), client=self._api
            ),
            _RUN,
            run_id,
        )

    def get_latest_run(
        self, *, workspace_id: str, job_id: str | None
    ) -> DetailedRunResponse:
        return _call(
            lambda: get_latest_run.sync_detailed(
                UUID(workspace_id),
                client=self._api,
                script_id=UUID(job_id) if job_id else API_UNSET,
            ),
            _RUN,
            "latest",
        )

    def list_runs(
        self, *, workspace_id: str, job_id: str | None, limit: int, offset: int
    ) -> ListRunsResponse200:
        return _call(
            lambda: list_runs.sync_detailed(
                UUID(workspace_id),
                client=self._api,
                limit=limit,
                offset=offset,
                script_id=UUID(job_id) if job_id else API_UNSET,
            ),
            _RUN_LIST,
            workspace_id,
        )

    def cancel_run(self, *, workspace_id: str, run_id: str) -> DetailedRunResponse:
        return _call(
            lambda: cancel_run.sync_detailed(
                UUID(workspace_id), UUID(run_id), client=self._api
            ),
            _RUN,
            run_id,
        )

    def cancel_runs(
        self, *, workspace_id: str, job_refs: Sequence[str], dry_run: bool
    ) -> BulkCancelResponse:
        body = BulkCancelRequest(job_refs=list(job_refs), dry_run=dry_run)
        return _call(
            lambda: bulk_cancel_runs.sync_detailed(
                UUID(workspace_id), client=self._api, body=body
            ),
            _BULK_CANCEL,
            workspace_id,
        )

    def list_pipeline_overview(
        self,
        *,
        workspace_id: str,
        dataplane_url: str,
        start: datetime,
        end: datetime,
        pipeline_name: str | None,
        latest_status: str | None,
        latest_destination_name: str | None,
        limit: int,
        offset: int,
    ) -> ListPipelineOverviewResponse200:
        return self._dataplane_call(
            lambda dp: list_pipeline_overview.sync_detailed(
                UUID(workspace_id),
                client=_as_telemetry(dp),
                start=start,
                end=end,
                tz="UTC",
                limit=limit,
                offset=offset,
                pipeline_name=[pipeline_name] if pipeline_name else TELEMETRY_UNSET,
                latest_status=(
                    [GenPipelineRunStatus(latest_status)]
                    if latest_status
                    else TELEMETRY_UNSET
                ),
                latest_destination_name=(
                    [latest_destination_name]
                    if latest_destination_name
                    else TELEMETRY_UNSET
                ),
            ),
            _PIPELINE_OVERVIEW,
            workspace_id,
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
        )

    def list_dataset_overview(
        self,
        *,
        workspace_id: str,
        dataplane_url: str,
        start: datetime,
        end: datetime,
        dataset_name: str | None,
        latest_status: str | None,
        latest_destination_name: str | None,
        limit: int,
        offset: int,
    ) -> ListDatasetOverviewResponse200:
        return self._dataplane_call(
            lambda dp: list_dataset_overview.sync_detailed(
                UUID(workspace_id),
                client=_as_telemetry(dp),
                start=start,
                end=end,
                tz="UTC",
                limit=limit,
                offset=offset,
                dataset_name=[dataset_name] if dataset_name else TELEMETRY_UNSET,
                latest_status=(
                    [GenPipelineRunStatus(latest_status)]
                    if latest_status
                    else TELEMETRY_UNSET
                ),
                latest_destination_name=(
                    [latest_destination_name]
                    if latest_destination_name
                    else TELEMETRY_UNSET
                ),
            ),
            _DATASET_OVERVIEW,
            workspace_id,
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
        )

    def get_pipeline_run_trace(
        self, *, workspace_id: str, dataplane_url: str, pipeline_run_id: str
    ) -> GetPipelineRunTraceResponse200:
        return self._dataplane_call(
            lambda dp: get_pipeline_run_trace.sync_detailed(
                UUID(workspace_id),
                UUID(pipeline_run_id),
                client=_as_telemetry(dp),
            ),
            _PIPELINE_RUN_TRACE,
            pipeline_run_id,
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
        )

    def get_pipeline_run(
        self, *, workspace_id: str, dataplane_url: str, pipeline_run_id: str
    ) -> PipelineRunDetailResponse:
        return self._dataplane_call(
            lambda dp: get_pipeline_run.sync_detailed(
                UUID(workspace_id),
                UUID(pipeline_run_id),
                client=_as_telemetry(dp),
            ),
            _PIPELINE_RUN,
            pipeline_run_id,
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
        )

    def list_pipeline_runs(
        self,
        *,
        workspace_id: str,
        dataplane_url: str,
        start: datetime,
        end: datetime,
        job_run_id: str | None,
        pipeline_name: str | None,
        status: str | None,
        dataset_name: str | None,
        destination_name: str | None,
        is_empty_run: bool | None,
        limit: int,
        offset: int,
    ) -> ListPipelineRunsResponse200:
        return self._dataplane_call(
            lambda dp: list_pipeline_runs.sync_detailed(
                UUID(workspace_id),
                client=_as_telemetry(dp),
                start=start,
                end=end,
                tz="UTC",
                limit=limit,
                offset=offset,
                job_run_id=[UUID(job_run_id)] if job_run_id else TELEMETRY_UNSET,
                pipeline_name=[pipeline_name] if pipeline_name else TELEMETRY_UNSET,
                status=([GenPipelineRunStatus(status)] if status else TELEMETRY_UNSET),
                dataset_name=[dataset_name] if dataset_name else TELEMETRY_UNSET,
                destination_name=(
                    [destination_name] if destination_name else TELEMETRY_UNSET
                ),
                is_empty_run=is_empty_run
                if is_empty_run is not None
                else TELEMETRY_UNSET,
            ),
            _PIPELINE_RUN_LIST,
            workspace_id,
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
        )

    def get_telemetry_watermark(
        self, *, workspace_id: str, dataplane_url: str
    ) -> TelemetryWatermarkResponse:
        return self._dataplane_call(
            lambda dp: get_telemetry_watermark.sync_detailed(
                UUID(workspace_id), client=_as_telemetry(dp)
            ),
            _TELEMETRY_WATERMARK,
            workspace_id,
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
        )

    def get_configuration_files(
        self, *, workspace_id: str, dataplane_url: str, configuration_id: str
    ) -> TFilesManifest:
        return self._dataplane_call(
            lambda dp: get_configuration_files_manifest.sync_detailed(
                UUID(workspace_id), UUID(configuration_id), client=dp
            ),
            _CONFIGURATION_FILES,
            configuration_id,
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
        )

    def get_deployment_files(
        self, *, workspace_id: str, dataplane_url: str, deployment_id: str
    ) -> TFilesManifest:
        return self._dataplane_call(
            lambda dp: get_deployment_files_manifest.sync_detailed(
                UUID(workspace_id), UUID(deployment_id), client=dp
            ),
            _DEPLOYMENT_FILES,
            deployment_id,
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
        )

    def change_variables(
        self,
        *,
        workspace_id: str,
        dataplane_url: str,
        profile: str | None,
        plain: Mapping[str, str],
        secret: Mapping[str, str],
        deletes: Sequence[str],
    ) -> VariablesChangeResponse:
        body = _variables_change(profile, plain, secret, deletes)
        return self._dataplane_call(
            lambda dp: change_workspace_variables.sync_detailed(
                UUID(workspace_id), client=dp, body=body
            ),
            _VARIABLE_CHANGE,
            workspace_id,
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
        )

    def list_variables(
        self,
        *,
        workspace_id: str,
        dataplane_url: str,
        profile: str | Keep,
        workspace: bool,
    ) -> WorkspaceVariablesResponse:
        # Mutually exclusive on the wire; `domain` is what keeps them so.
        return self._dataplane_call(
            lambda dp: list_workspace_variables.sync_detailed(
                UUID(workspace_id),
                client=dp,
                profile=_wire(profile, DATAPLANE_UNSET),
                workspace=True if workspace else DATAPLANE_UNSET,
            ),
            _VARIABLES,
            workspace_id,
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
        )

    def get_organization(self, *, organization_id: str) -> OrganizationResponse:
        return _call(
            lambda: get_organization.sync_detailed(
                UUID(organization_id), client=self._api
            ),
            _ORGANIZATION,
            organization_id,
        )

    def get_current_user(self) -> CurrentUserResponse:
        return _call(
            lambda: get_current_user.sync_detailed(client=self._api),
            _CURRENT_USER,
            None,
        )

    def organization_me(self, *, organization_id: str) -> OrganizationMeResponse:
        return _call(
            lambda: organization_me.sync_detailed(
                UUID(organization_id), client=self._api
            ),
            _ORGANIZATION_ME,
            organization_id,
        )

    def workspace_me(self, *, workspace_id: str) -> WorkspaceMeResponse:
        return _call(
            lambda: workspace_me.sync_detailed(UUID(workspace_id), client=self._api),
            _WORKSPACE_ME,
            workspace_id,
        )

    def list_organizations(
        self, *, limit: int, offset: int
    ) -> ListOrganizationsResponse200:
        return _call(
            lambda: list_organizations.sync_detailed(
                client=self._api, limit=limit, offset=offset
            ),
            _ORGANIZATION_LIST,
            # Addresses no particular organization: it lists what the caller can see.
            None,
        )

    def set_organization_region(
        self, *, organization_id: str, dataplane_id: str
    ) -> OrganizationResponse:
        body = SetOrganizationRegionRequest(dataplane_id=dataplane_id)
        return _call(
            lambda: set_organization_region.sync_detailed(
                UUID(organization_id), client=self._api, body=body
            ),
            _ORGANIZATION,
            organization_id,
        )

    def create_workspace(
        self, *, organization_id: str, name: str, description: str | None
    ) -> WorkspaceResponse:
        body = WorkspaceCreateRequest(name=name, description=description)
        return _call(
            lambda: create_workspace.sync_detailed(
                UUID(organization_id), client=self._api, body=body
            ),
            _WORKSPACE,
            name,
        )

    def enable_public_url(self, *, workspace_id: str, job_ref: str) -> ScriptResponse:
        return _call(
            lambda: enable_public_url.sync_detailed(
                UUID(workspace_id), job_ref, client=self._api
            ),
            _SCRIPT,
            job_ref,
        )

    def disable_public_url(self, *, workspace_id: str, job_ref: str) -> ScriptResponse:
        return _call(
            lambda: disable_public_url.sync_detailed(
                UUID(workspace_id), job_ref, client=self._api
            ),
            _SCRIPT,
            job_ref,
        )

    def trigger_jobs(
        self,
        *,
        workspace_id: str,
        job_refs: Sequence[str] | None,
        selectors: Sequence[str] | None,
        profile: str | None | Keep,
        refresh: bool,
        dry_run: bool,
    ) -> TriggerJobsResponse:
        body = TriggerJobsRequest(
            job_refs=list(job_refs) if job_refs is not None else API_UNSET,
            selectors=list(selectors) if selectors is not None else API_UNSET,
            profile=_wire(profile, API_UNSET),
            refresh=refresh,
            dry_run=dry_run,
        )
        return _call(
            lambda: trigger_jobs.sync_detailed(
                UUID(workspace_id), client=self._api, body=body
            ),
            _TRIGGERED_JOBS,
            workspace_id,
        )

    def create_run(
        self,
        *,
        workspace_id: str,
        job_ref: str,
        trigger: str,
        profile: str | None | Keep,
        refresh: bool,
        skip_freshness: bool,
    ) -> TriggeredJob:
        body = CreateRunRequest(
            script_id_or_ref=job_ref,
            trigger=trigger,
            profile=_wire(profile, API_UNSET),
            refresh=refresh,
            skip_freshness=skip_freshness,
        )
        return _call(
            lambda: create_run.sync_detailed(
                UUID(workspace_id), client=self._api, body=body
            ),
            _TRIGGERED_JOB,
            job_ref,
        )

    def get_workspace(self, *, workspace_id: str) -> WorkspaceResponse:
        return _call(
            lambda: get_workspace.sync_detailed(UUID(workspace_id), client=self._api),
            _WORKSPACE,
            workspace_id,
        )

    def list_workspaces(
        self, *, organization_id: str, limit: int, offset: int
    ) -> ListWorkspacesResponse200:
        return _call(
            lambda: list_workspaces.sync_detailed(
                UUID(organization_id), client=self._api, limit=limit, offset=offset
            ),
            _WORKSPACE_LIST,
            organization_id,
        )

    def list_workspace_members(
        self, *, workspace_id: str, limit: int, offset: int
    ) -> ListWorkspaceMembersResponse200:
        return _call(
            lambda: list_workspace_members.sync_detailed(
                UUID(workspace_id), client=self._api, limit=limit, offset=offset
            ),
            _WORKSPACE_MEMBER_LIST,
            workspace_id,
        )

    def update_workspace(
        self, *, workspace_id: str, name: str | Keep, description: str | None | Keep
    ) -> WorkspaceResponse:
        body = WorkspaceUpdateRequest(
            name=_wire(name, API_UNSET),
            description=_wire(description, API_UNSET),
        )
        return _call(
            lambda: update_workspace.sync_detailed(
                UUID(workspace_id), client=self._api, body=body
            ),
            _WORKSPACE,
            workspace_id,
        )

    def upload_deployment(
        self,
        *,
        workspace_id: str,
        code: bytes | BinaryIO,
        requirements: bytes | BinaryIO,
    ) -> DataplaneDeploymentResponse:
        """Two generated operations, because the second is addressed by the first.

        The create call mints an id, a URL and a token scoped to this one
        upload; nothing else can supply them, so the pair is one method.

        Args:
            workspace_id: Workspace to deploy into.
            code: The package archive.
            requirements: The requirements manifest.

        Returns:
            The stored deployment, as the data plane wrote it back.
        """
        initiated = _call(
            lambda: create_deployment.sync_detailed(
                UUID(workspace_id), client=self._api
            ),
            _DEPLOYMENT_UPLOAD,
            workspace_id,
        )
        client, deployment_id = _upload_target(
            initiated,
            initiated.deployment_id,
            "deployments",
            EntityKind.DEPLOYMENT,
            self._verify_ssl,
            self._headers,
        )
        body = DeploymentUploadBody(
            files=_as_file(code, "workspace.tar.gz", _TAR_MIME),
            requirements=_as_file(requirements, "requirements.json", _JSON_MIME),
        )
        try:
            return _call(
                lambda: upload_deployment_bytes.sync_detailed(
                    deployment_id, client=client, body=body
                ),
                _DP_DEPLOYMENT,
                str(deployment_id),
            )
        finally:
            _shut(client)

    def upload_configuration(
        self, *, workspace_id: str, data: bytes | BinaryIO
    ) -> DataplaneConfigurationResponse:
        """The configuration twin of ``upload_deployment``.

        Args:
            workspace_id: Workspace to store the configuration in.
            data: The configuration archive.

        Returns:
            The stored configuration, as the data plane wrote it back.
        """
        initiated = _call(
            lambda: create_configuration.sync_detailed(
                UUID(workspace_id), client=self._api
            ),
            _CONFIGURATION_UPLOAD,
            workspace_id,
        )
        client, configuration_id = _upload_target(
            initiated,
            initiated.configuration_id,
            "configurations",
            EntityKind.CONFIGURATION,
            self._verify_ssl,
            self._headers,
        )
        body = UploadConfigurationBytesBody(
            file=_as_file(data, "configurations.tar.gz", _TAR_MIME)
        )
        try:
            return _call(
                lambda: upload_configuration_bytes.sync_detailed(
                    configuration_id, client=client, body=body
                ),
                _DP_CONFIGURATION,
                str(configuration_id),
            )
        finally:
            _shut(client)

    def deploy_manifest(
        self,
        *,
        workspace_id: str,
        jobs: Sequence[Mapping[str, Any]],
        manifest_hash: str,
        engine_version: int,
        module: str | None,
        description: str | None | Keep,
        dry_run: bool,
    ) -> DeployManifestResponse:
        body = _manifest_body(
            jobs, manifest_hash, engine_version, module, description, dry_run
        )
        return _call(
            lambda: deploy.sync_detailed(
                UUID(workspace_id), client=self._api, body=body
            ),
            _DEPLOY_REPORT,
            workspace_id,
        )

    def get_configuration(
        self, *, workspace_id: str, version: int
    ) -> ConfigurationResponse:
        return _call(
            lambda: get_configuration.sync_detailed(
                UUID(workspace_id), version, client=self._api
            ),
            _CONFIGURATION,
            str(version),
        )

    def get_latest_configuration(self, *, workspace_id: str) -> ConfigurationResponse:
        return _call(
            lambda: get_latest_configuration.sync_detailed(
                UUID(workspace_id), client=self._api
            ),
            _CONFIGURATION,
            "latest",
        )

    def list_configurations(
        self, *, workspace_id: str, limit: int, offset: int
    ) -> ListConfigurationsResponse200:
        return _call(
            lambda: list_configurations.sync_detailed(
                UUID(workspace_id), client=self._api, limit=limit, offset=offset
            ),
            _CONFIGURATION_LIST,
            workspace_id,
        )

    def get_deployment(self, *, workspace_id: str, version: int) -> DeploymentResponse:
        return _call(
            lambda: get_deployment.sync_detailed(
                UUID(workspace_id), version, client=self._api
            ),
            _DEPLOYMENT,
            str(version),
        )

    def get_latest_deployment(self, *, workspace_id: str) -> DeploymentResponse:
        return _call(
            lambda: get_latest_deployment.sync_detailed(
                UUID(workspace_id), client=self._api
            ),
            _DEPLOYMENT,
            "latest",
        )

    def list_deployments(
        self, *, workspace_id: str, limit: int, offset: int
    ) -> ListDeploymentsResponse200:
        return _call(
            lambda: list_deployments.sync_detailed(
                UUID(workspace_id), client=self._api, limit=limit, offset=offset
            ),
            _DEPLOYMENT_LIST,
            workspace_id,
        )

    def get_script(self, *, workspace_id: str, job_ref: str) -> DetailedScriptResponse:
        return _call(
            lambda: get_script.sync_detailed(
                UUID(workspace_id), job_ref, client=self._api
            ),
            _SCRIPT_DETAIL,
            job_ref,
        )

    def list_scripts(
        self, *, workspace_id: str, limit: int, offset: int, archived: bool | Keep
    ) -> ListScriptsResponse200:
        return _call(
            lambda: list_scripts.sync_detailed(
                UUID(workspace_id),
                client=self._api,
                limit=limit,
                offset=offset,
                archived=_wire(archived, API_UNSET),
            ),
            _SCRIPT_LIST,
            workspace_id,
        )

    def pause_script(self, *, workspace_id: str, job_ref: str) -> ScriptResponse:
        return _call(
            lambda: pause_script.sync_detailed(
                UUID(workspace_id), job_ref, client=self._api
            ),
            _SCRIPT,
            job_ref,
        )

    def resume_script(self, *, workspace_id: str, job_ref: str) -> ScriptResponse:
        return _call(
            lambda: resume_script.sync_detailed(
                UUID(workspace_id), job_ref, client=self._api
            ),
            _SCRIPT,
            job_ref,
        )


class AsyncTransport(Protocol):
    """The async twin of `Transport`. Same operations, awaited."""

    async def get_organization(
        self, *, organization_id: str
    ) -> OrganizationResponse: ...

    async def get_current_user(self) -> CurrentUserResponse: ...

    async def organization_me(
        self, *, organization_id: str
    ) -> OrganizationMeResponse: ...

    async def workspace_me(self, *, workspace_id: str) -> WorkspaceMeResponse: ...

    async def list_organizations(
        self, *, limit: int, offset: int
    ) -> ListOrganizationsResponse200: ...

    async def set_organization_region(
        self, *, organization_id: str, dataplane_id: str
    ) -> OrganizationResponse: ...

    async def create_workspace(
        self, *, organization_id: str, name: str, description: str | None
    ) -> WorkspaceResponse: ...

    async def enable_public_url(
        self, *, workspace_id: str, job_ref: str
    ) -> ScriptResponse: ...

    async def disable_public_url(
        self, *, workspace_id: str, job_ref: str
    ) -> ScriptResponse: ...

    async def trigger_jobs(
        self,
        *,
        workspace_id: str,
        job_refs: Sequence[str] | None,
        selectors: Sequence[str] | None,
        profile: str | None | Keep,
        refresh: bool,
        dry_run: bool,
    ) -> TriggerJobsResponse: ...

    async def create_run(
        self,
        *,
        workspace_id: str,
        job_ref: str,
        trigger: str,
        profile: str | None | Keep,
        refresh: bool,
        skip_freshness: bool,
    ) -> TriggeredJob: ...

    async def change_variables(
        self,
        *,
        workspace_id: str,
        dataplane_url: str,
        profile: str | None,
        plain: Mapping[str, str],
        secret: Mapping[str, str],
        deletes: Sequence[str],
    ) -> VariablesChangeResponse: ...

    async def list_variables(
        self,
        *,
        workspace_id: str,
        dataplane_url: str,
        profile: str | Keep,
        workspace: bool,
    ) -> WorkspaceVariablesResponse: ...

    async def get_workspace(self, *, workspace_id: str) -> WorkspaceResponse: ...

    async def list_workspaces(
        self, *, organization_id: str, limit: int, offset: int
    ) -> ListWorkspacesResponse200: ...

    async def list_workspace_members(
        self, *, workspace_id: str, limit: int, offset: int
    ) -> ListWorkspaceMembersResponse200: ...

    async def update_workspace(
        self, *, workspace_id: str, name: str | Keep, description: str | None | Keep
    ) -> WorkspaceResponse: ...

    async def list_dataplanes(self) -> list[DataplaneInfo]: ...

    async def get_run(
        self, *, workspace_id: str, run_id: str
    ) -> DetailedRunResponse: ...

    async def get_latest_run(
        self, *, workspace_id: str, job_id: str | None
    ) -> DetailedRunResponse: ...

    async def list_runs(
        self, *, workspace_id: str, job_id: str | None, limit: int, offset: int
    ) -> ListRunsResponse200: ...

    async def cancel_run(
        self, *, workspace_id: str, run_id: str
    ) -> DetailedRunResponse: ...

    async def cancel_runs(
        self, *, workspace_id: str, job_refs: Sequence[str], dry_run: bool
    ) -> BulkCancelResponse: ...

    async def get_telemetry_watermark(
        self, *, workspace_id: str, dataplane_url: str
    ) -> TelemetryWatermarkResponse: ...

    async def get_pipeline_run(
        self, *, workspace_id: str, dataplane_url: str, pipeline_run_id: str
    ) -> PipelineRunDetailResponse: ...

    async def get_pipeline_run_trace(
        self, *, workspace_id: str, dataplane_url: str, pipeline_run_id: str
    ) -> GetPipelineRunTraceResponse200: ...

    async def list_pipeline_overview(
        self,
        *,
        workspace_id: str,
        dataplane_url: str,
        start: datetime,
        end: datetime,
        pipeline_name: str | None,
        latest_status: str | None,
        latest_destination_name: str | None,
        limit: int,
        offset: int,
    ) -> ListPipelineOverviewResponse200: ...

    async def list_dataset_overview(
        self,
        *,
        workspace_id: str,
        dataplane_url: str,
        start: datetime,
        end: datetime,
        dataset_name: str | None,
        latest_status: str | None,
        latest_destination_name: str | None,
        limit: int,
        offset: int,
    ) -> ListDatasetOverviewResponse200: ...

    async def list_pipeline_runs(
        self,
        *,
        workspace_id: str,
        dataplane_url: str,
        start: datetime,
        end: datetime,
        job_run_id: str | None,
        pipeline_name: str | None,
        status: str | None,
        dataset_name: str | None,
        destination_name: str | None,
        is_empty_run: bool | None,
        limit: int,
        offset: int,
    ) -> ListPipelineRunsResponse200: ...

    async def get_configuration_files(
        self, *, workspace_id: str, dataplane_url: str, configuration_id: str
    ) -> TFilesManifest: ...

    async def get_deployment_files(
        self, *, workspace_id: str, dataplane_url: str, deployment_id: str
    ) -> TFilesManifest: ...

    async def get_configuration(
        self, *, workspace_id: str, version: int
    ) -> ConfigurationResponse: ...

    async def get_latest_configuration(
        self, *, workspace_id: str
    ) -> ConfigurationResponse: ...

    async def list_configurations(
        self, *, workspace_id: str, limit: int, offset: int
    ) -> ListConfigurationsResponse200: ...

    async def get_deployment(
        self, *, workspace_id: str, version: int
    ) -> DeploymentResponse: ...

    async def get_latest_deployment(
        self, *, workspace_id: str
    ) -> DeploymentResponse: ...

    async def list_deployments(
        self, *, workspace_id: str, limit: int, offset: int
    ) -> ListDeploymentsResponse200: ...

    async def get_script(
        self, *, workspace_id: str, job_ref: str
    ) -> DetailedScriptResponse: ...

    async def list_scripts(
        self, *, workspace_id: str, limit: int, offset: int, archived: bool | Keep
    ) -> ListScriptsResponse200: ...

    async def pause_script(
        self, *, workspace_id: str, job_ref: str
    ) -> ScriptResponse: ...

    async def resume_script(
        self, *, workspace_id: str, job_ref: str
    ) -> ScriptResponse: ...

    async def upload_deployment(
        self,
        *,
        workspace_id: str,
        code: bytes | BinaryIO,
        requirements: bytes | BinaryIO,
    ) -> DataplaneDeploymentResponse: ...

    async def upload_configuration(
        self, *, workspace_id: str, data: bytes | BinaryIO
    ) -> DataplaneConfigurationResponse: ...

    async def deploy_manifest(
        self,
        *,
        workspace_id: str,
        jobs: Sequence[Mapping[str, Any]],
        manifest_hash: str,
        engine_version: int,
        module: str | None,
        description: str | None | Keep,
        dry_run: bool,
    ) -> DeployManifestResponse: ...

    def read_logs(
        self, *, workspace_id: str, dataplane_url: str, run_id: str
    ) -> AsyncIterator[LogLine]: ...

    def stream_logs(
        self, *, workspace_id: str, dataplane_url: str, run_id: str, follow: bool
    ) -> AsyncIterator[LogLine]: ...

    async def aclose(self) -> None: ...


class AsyncHttpTransport:
    """`AsyncTransport` over the generated asyncio clients."""

    def __init__(
        self,
        token: str | None = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        credentials: AsyncCredentials | None = None,
        verify_ssl: bool = True,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        """Hold the clients this transport calls through.

        Exactly one of ``token`` and ``credentials`` says how to authenticate
        the control plane.

        Args:
            token: A credential that does not change. Wrapped so there is one
                credential path.
            base_url: Control-plane base URL.
            credentials: Where to read the credential before each request, for
                one that rotates. Renewed once if the platform rejects it.
            verify_ssl: Applied to every client this transport builds, the
                per-workspace and per-upload data-plane ones included, so a
                caller's TLS choice cannot be confined to one plane.
            headers: Applied the same way.

        Raises:
            ValueError: Both ``token`` and ``credentials``, or neither.
        """
        self._credentials = _one_credential(token, credentials, _AsyncStatic)
        self._api = Client(
            base_url=base_url,
            verify_ssl=verify_ssl,
            headers=dict(headers or {}),
            httpx_args={"auth": _AsyncCredentialsAuth(self._credentials)},
        )
        self._base_url = base_url
        self._verify_ssl = verify_ssl
        self._headers = dict(headers or {})
        self._dataplane_clients: dict[str, _Minted] = {}

    def __repr__(self) -> str:
        # Never repr a client: they hold raw tokens, the minted ones included.
        return f"<AsyncHttpTransport base_url={self._base_url!r} token='***'>"

    async def aclose(self) -> None:
        """Close every connection this transport opened, on either plane."""
        await _ashut(self._api)
        for held in self._dataplane_clients.values():
            await _ashut(held.client)
        self._dataplane_clients.clear()

    async def _dataplane_client(
        self, workspace_id: str, dataplane_url: str, *, remint: bool = False
    ) -> DataplaneApiClient:
        """The awaiting twin of ``HttpTransport._dataplane_client``.

        Args:
            workspace_id: Whose data plane to reach.
            dataplane_url: That data plane's base URL.
            remint: Ignore a cached token, however fresh.

        Returns:
            A client carrying an unexpired token.
        """
        held = self._dataplane_clients.get(workspace_id)
        cached = _cached_dataplane(held, remint=remint)
        if cached is not None:
            return cached
        minted = _unwrap(
            await get_workspace_dataplane_access_token.asyncio_detailed(
                UUID(workspace_id), client=self._api
            ),
            _DATAPLANE_TOKEN,
            workspace_id,
        )
        fresh = _hold_dataplane(minted, dataplane_url, self._verify_ssl, self._headers)
        if held is not None:
            await _ashut(held.client)
        self._dataplane_clients[workspace_id] = fresh
        return fresh.client

    async def _dataplane_call(
        self,
        fetch: Callable[[DataplaneApiClient], Awaitable[_Reply[T | E]]],
        op: _Op[T],
        ref: str | None,
        *,
        workspace_id: str,
        dataplane_url: str,
    ) -> T:
        """The awaiting twin of ``HttpTransport._dataplane_call``.

        Args:
            fetch: Performs the generated call against the data-plane client.
            op: The operation's success model and entity kind.
            ref: The id or name being addressed.
            workspace_id: Whose data plane to reach.
            dataplane_url: That data plane's base URL.

        Returns:
            The parsed success model.
        """
        with _transport_errors(op.kind, ref):
            resp = await fetch(
                await self._dataplane_client(workspace_id, dataplane_url)
            )
            if resp.status_code == HTTPStatus.UNAUTHORIZED:
                resp = await fetch(
                    await self._dataplane_client(
                        workspace_id, dataplane_url, remint=True
                    )
                )
        return _unwrap(resp, op, ref)

    async def _dataplane_logs(
        self,
        path: str,
        *,
        workspace_id: str,
        dataplane_url: str,
        run_id: str,
        sse: bool,
        follow: bool = True,
    ) -> AsyncIterator[LogLine]:
        """The awaiting twin of ``HttpTransport._dataplane_logs``.

        Args:
            path: The logs route, already formatted.
            workspace_id: Whose data plane to reach.
            dataplane_url: That data plane's base URL.
            run_id: The run being read.
            sse: Whether the body is SSE rather than NDJSON.
            follow: Keep the stream open. False replays what is already there
                and stops, which the platform marks only by going quiet.

        Yields:
            One generated model per log line.
        """
        with _transport_errors(EntityKind.JOB_RUN, run_id):
            remint = False
            while True:
                client = await self._dataplane_client(
                    workspace_id, dataplane_url, remint=remint
                )
                async with client.get_async_httpx_client().stream(
                    "GET",
                    path,
                    headers={"Accept": _SSE if sse else _NDJSON},
                    timeout=_stream_timeout(sse, follow),
                ) as resp:
                    if resp.status_code == HTTPStatus.UNAUTHORIZED and not remint:
                        remint = True
                        continue
                    if resp.status_code != HTTPStatus.OK:
                        await resp.aread()
                        _unwrap(
                            _StreamReply(HTTPStatus(resp.status_code), resp.content),
                            _LOG,
                            run_id,
                        )
                    reader = _Sse()
                    async for line in resp.aiter_lines():
                        row = _log_row(reader, line, run_id, sse)
                        if row is not None:
                            yield row
                    return

    def read_logs(
        self, *, workspace_id: str, dataplane_url: str, run_id: str
    ) -> AsyncIterator[LogLine]:
        return self._dataplane_logs(
            _logs_path(_LOGS_READ, workspace_id, run_id),
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
            run_id=run_id,
            sse=False,
        )

    def stream_logs(
        self, *, workspace_id: str, dataplane_url: str, run_id: str, follow: bool
    ) -> AsyncIterator[LogLine]:
        return self._dataplane_logs(
            _logs_path(_LOGS_STREAM, workspace_id, run_id),
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
            run_id=run_id,
            sse=True,
            follow=follow,
        )

    async def list_dataplanes(self) -> list[DataplaneInfo]:
        return await _acall(
            lambda: list_dataplanes.asyncio_detailed(client=self._api),
            _DATAPLANE_LIST,
            None,
        )

    async def get_run(self, *, workspace_id: str, run_id: str) -> DetailedRunResponse:
        return await _acall(
            lambda: get_run.asyncio_detailed(
                UUID(workspace_id), UUID(run_id), client=self._api
            ),
            _RUN,
            run_id,
        )

    async def get_latest_run(
        self, *, workspace_id: str, job_id: str | None
    ) -> DetailedRunResponse:
        return await _acall(
            lambda: get_latest_run.asyncio_detailed(
                UUID(workspace_id),
                client=self._api,
                script_id=UUID(job_id) if job_id else API_UNSET,
            ),
            _RUN,
            "latest",
        )

    async def list_runs(
        self, *, workspace_id: str, job_id: str | None, limit: int, offset: int
    ) -> ListRunsResponse200:
        return await _acall(
            lambda: list_runs.asyncio_detailed(
                UUID(workspace_id),
                client=self._api,
                limit=limit,
                offset=offset,
                script_id=UUID(job_id) if job_id else API_UNSET,
            ),
            _RUN_LIST,
            workspace_id,
        )

    async def cancel_run(
        self, *, workspace_id: str, run_id: str
    ) -> DetailedRunResponse:
        return await _acall(
            lambda: cancel_run.asyncio_detailed(
                UUID(workspace_id), UUID(run_id), client=self._api
            ),
            _RUN,
            run_id,
        )

    async def cancel_runs(
        self, *, workspace_id: str, job_refs: Sequence[str], dry_run: bool
    ) -> BulkCancelResponse:
        body = BulkCancelRequest(job_refs=list(job_refs), dry_run=dry_run)
        return await _acall(
            lambda: bulk_cancel_runs.asyncio_detailed(
                UUID(workspace_id), client=self._api, body=body
            ),
            _BULK_CANCEL,
            workspace_id,
        )

    async def list_pipeline_overview(
        self,
        *,
        workspace_id: str,
        dataplane_url: str,
        start: datetime,
        end: datetime,
        pipeline_name: str | None,
        latest_status: str | None,
        latest_destination_name: str | None,
        limit: int,
        offset: int,
    ) -> ListPipelineOverviewResponse200:
        return await self._dataplane_call(
            lambda dp: list_pipeline_overview.asyncio_detailed(
                UUID(workspace_id),
                client=_as_telemetry(dp),
                start=start,
                end=end,
                tz="UTC",
                limit=limit,
                offset=offset,
                pipeline_name=[pipeline_name] if pipeline_name else TELEMETRY_UNSET,
                latest_status=(
                    [GenPipelineRunStatus(latest_status)]
                    if latest_status
                    else TELEMETRY_UNSET
                ),
                latest_destination_name=(
                    [latest_destination_name]
                    if latest_destination_name
                    else TELEMETRY_UNSET
                ),
            ),
            _PIPELINE_OVERVIEW,
            workspace_id,
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
        )

    async def list_dataset_overview(
        self,
        *,
        workspace_id: str,
        dataplane_url: str,
        start: datetime,
        end: datetime,
        dataset_name: str | None,
        latest_status: str | None,
        latest_destination_name: str | None,
        limit: int,
        offset: int,
    ) -> ListDatasetOverviewResponse200:
        return await self._dataplane_call(
            lambda dp: list_dataset_overview.asyncio_detailed(
                UUID(workspace_id),
                client=_as_telemetry(dp),
                start=start,
                end=end,
                tz="UTC",
                limit=limit,
                offset=offset,
                dataset_name=[dataset_name] if dataset_name else TELEMETRY_UNSET,
                latest_status=(
                    [GenPipelineRunStatus(latest_status)]
                    if latest_status
                    else TELEMETRY_UNSET
                ),
                latest_destination_name=(
                    [latest_destination_name]
                    if latest_destination_name
                    else TELEMETRY_UNSET
                ),
            ),
            _DATASET_OVERVIEW,
            workspace_id,
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
        )

    async def get_pipeline_run_trace(
        self, *, workspace_id: str, dataplane_url: str, pipeline_run_id: str
    ) -> GetPipelineRunTraceResponse200:
        return await self._dataplane_call(
            lambda dp: get_pipeline_run_trace.asyncio_detailed(
                UUID(workspace_id),
                UUID(pipeline_run_id),
                client=_as_telemetry(dp),
            ),
            _PIPELINE_RUN_TRACE,
            pipeline_run_id,
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
        )

    async def get_pipeline_run(
        self, *, workspace_id: str, dataplane_url: str, pipeline_run_id: str
    ) -> PipelineRunDetailResponse:
        return await self._dataplane_call(
            lambda dp: get_pipeline_run.asyncio_detailed(
                UUID(workspace_id),
                UUID(pipeline_run_id),
                client=_as_telemetry(dp),
            ),
            _PIPELINE_RUN,
            pipeline_run_id,
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
        )

    async def list_pipeline_runs(
        self,
        *,
        workspace_id: str,
        dataplane_url: str,
        start: datetime,
        end: datetime,
        job_run_id: str | None,
        pipeline_name: str | None,
        status: str | None,
        dataset_name: str | None,
        destination_name: str | None,
        is_empty_run: bool | None,
        limit: int,
        offset: int,
    ) -> ListPipelineRunsResponse200:
        return await self._dataplane_call(
            lambda dp: list_pipeline_runs.asyncio_detailed(
                UUID(workspace_id),
                client=_as_telemetry(dp),
                start=start,
                end=end,
                tz="UTC",
                limit=limit,
                offset=offset,
                job_run_id=[UUID(job_run_id)] if job_run_id else TELEMETRY_UNSET,
                pipeline_name=[pipeline_name] if pipeline_name else TELEMETRY_UNSET,
                status=([GenPipelineRunStatus(status)] if status else TELEMETRY_UNSET),
                dataset_name=[dataset_name] if dataset_name else TELEMETRY_UNSET,
                destination_name=(
                    [destination_name] if destination_name else TELEMETRY_UNSET
                ),
                is_empty_run=is_empty_run
                if is_empty_run is not None
                else TELEMETRY_UNSET,
            ),
            _PIPELINE_RUN_LIST,
            workspace_id,
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
        )

    async def get_telemetry_watermark(
        self, *, workspace_id: str, dataplane_url: str
    ) -> TelemetryWatermarkResponse:
        return await self._dataplane_call(
            lambda dp: get_telemetry_watermark.asyncio_detailed(
                UUID(workspace_id), client=_as_telemetry(dp)
            ),
            _TELEMETRY_WATERMARK,
            workspace_id,
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
        )

    async def get_configuration_files(
        self, *, workspace_id: str, dataplane_url: str, configuration_id: str
    ) -> TFilesManifest:
        return await self._dataplane_call(
            lambda dp: get_configuration_files_manifest.asyncio_detailed(
                UUID(workspace_id), UUID(configuration_id), client=dp
            ),
            _CONFIGURATION_FILES,
            configuration_id,
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
        )

    async def get_deployment_files(
        self, *, workspace_id: str, dataplane_url: str, deployment_id: str
    ) -> TFilesManifest:
        return await self._dataplane_call(
            lambda dp: get_deployment_files_manifest.asyncio_detailed(
                UUID(workspace_id), UUID(deployment_id), client=dp
            ),
            _DEPLOYMENT_FILES,
            deployment_id,
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
        )

    async def change_variables(
        self,
        *,
        workspace_id: str,
        dataplane_url: str,
        profile: str | None,
        plain: Mapping[str, str],
        secret: Mapping[str, str],
        deletes: Sequence[str],
    ) -> VariablesChangeResponse:
        body = _variables_change(profile, plain, secret, deletes)
        return await self._dataplane_call(
            lambda dp: change_workspace_variables.asyncio_detailed(
                UUID(workspace_id), client=dp, body=body
            ),
            _VARIABLE_CHANGE,
            workspace_id,
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
        )

    async def list_variables(
        self,
        *,
        workspace_id: str,
        dataplane_url: str,
        profile: str | Keep,
        workspace: bool,
    ) -> WorkspaceVariablesResponse:
        # Mutually exclusive on the wire; `domain` is what keeps them so.
        return await self._dataplane_call(
            lambda dp: list_workspace_variables.asyncio_detailed(
                UUID(workspace_id),
                client=dp,
                profile=_wire(profile, DATAPLANE_UNSET),
                workspace=True if workspace else DATAPLANE_UNSET,
            ),
            _VARIABLES,
            workspace_id,
            workspace_id=workspace_id,
            dataplane_url=dataplane_url,
        )

    async def get_organization(self, *, organization_id: str) -> OrganizationResponse:
        return await _acall(
            lambda: get_organization.asyncio_detailed(
                UUID(organization_id), client=self._api
            ),
            _ORGANIZATION,
            organization_id,
        )

    async def get_current_user(self) -> CurrentUserResponse:
        return await _acall(
            lambda: get_current_user.asyncio_detailed(client=self._api),
            _CURRENT_USER,
            None,
        )

    async def organization_me(self, *, organization_id: str) -> OrganizationMeResponse:
        return await _acall(
            lambda: organization_me.asyncio_detailed(
                UUID(organization_id), client=self._api
            ),
            _ORGANIZATION_ME,
            organization_id,
        )

    async def workspace_me(self, *, workspace_id: str) -> WorkspaceMeResponse:
        return await _acall(
            lambda: workspace_me.asyncio_detailed(UUID(workspace_id), client=self._api),
            _WORKSPACE_ME,
            workspace_id,
        )

    async def list_organizations(
        self, *, limit: int, offset: int
    ) -> ListOrganizationsResponse200:
        return await _acall(
            lambda: list_organizations.asyncio_detailed(
                client=self._api, limit=limit, offset=offset
            ),
            _ORGANIZATION_LIST,
            None,
        )

    async def set_organization_region(
        self, *, organization_id: str, dataplane_id: str
    ) -> OrganizationResponse:
        body = SetOrganizationRegionRequest(dataplane_id=dataplane_id)
        return await _acall(
            lambda: set_organization_region.asyncio_detailed(
                UUID(organization_id), client=self._api, body=body
            ),
            _ORGANIZATION,
            organization_id,
        )

    async def create_workspace(
        self, *, organization_id: str, name: str, description: str | None
    ) -> WorkspaceResponse:
        body = WorkspaceCreateRequest(name=name, description=description)
        return await _acall(
            lambda: create_workspace.asyncio_detailed(
                UUID(organization_id), client=self._api, body=body
            ),
            _WORKSPACE,
            name,
        )

    async def enable_public_url(
        self, *, workspace_id: str, job_ref: str
    ) -> ScriptResponse:
        return await _acall(
            lambda: enable_public_url.asyncio_detailed(
                UUID(workspace_id), job_ref, client=self._api
            ),
            _SCRIPT,
            job_ref,
        )

    async def disable_public_url(
        self, *, workspace_id: str, job_ref: str
    ) -> ScriptResponse:
        return await _acall(
            lambda: disable_public_url.asyncio_detailed(
                UUID(workspace_id), job_ref, client=self._api
            ),
            _SCRIPT,
            job_ref,
        )

    async def trigger_jobs(
        self,
        *,
        workspace_id: str,
        job_refs: Sequence[str] | None,
        selectors: Sequence[str] | None,
        profile: str | None | Keep,
        refresh: bool,
        dry_run: bool,
    ) -> TriggerJobsResponse:
        body = TriggerJobsRequest(
            job_refs=list(job_refs) if job_refs is not None else API_UNSET,
            selectors=list(selectors) if selectors is not None else API_UNSET,
            profile=_wire(profile, API_UNSET),
            refresh=refresh,
            dry_run=dry_run,
        )
        return await _acall(
            lambda: trigger_jobs.asyncio_detailed(
                UUID(workspace_id), client=self._api, body=body
            ),
            _TRIGGERED_JOBS,
            workspace_id,
        )

    async def create_run(
        self,
        *,
        workspace_id: str,
        job_ref: str,
        trigger: str,
        profile: str | None | Keep,
        refresh: bool,
        skip_freshness: bool,
    ) -> TriggeredJob:
        body = CreateRunRequest(
            script_id_or_ref=job_ref,
            trigger=trigger,
            profile=_wire(profile, API_UNSET),
            refresh=refresh,
            skip_freshness=skip_freshness,
        )
        return await _acall(
            lambda: create_run.asyncio_detailed(
                UUID(workspace_id), client=self._api, body=body
            ),
            _TRIGGERED_JOB,
            job_ref,
        )

    async def get_workspace(self, *, workspace_id: str) -> WorkspaceResponse:
        return await _acall(
            lambda: get_workspace.asyncio_detailed(
                UUID(workspace_id), client=self._api
            ),
            _WORKSPACE,
            workspace_id,
        )

    async def list_workspaces(
        self, *, organization_id: str, limit: int, offset: int
    ) -> ListWorkspacesResponse200:
        return await _acall(
            lambda: list_workspaces.asyncio_detailed(
                UUID(organization_id), client=self._api, limit=limit, offset=offset
            ),
            _WORKSPACE_LIST,
            organization_id,
        )

    async def list_workspace_members(
        self, *, workspace_id: str, limit: int, offset: int
    ) -> ListWorkspaceMembersResponse200:
        return await _acall(
            lambda: list_workspace_members.asyncio_detailed(
                UUID(workspace_id), client=self._api, limit=limit, offset=offset
            ),
            _WORKSPACE_MEMBER_LIST,
            workspace_id,
        )

    async def update_workspace(
        self, *, workspace_id: str, name: str | Keep, description: str | None | Keep
    ) -> WorkspaceResponse:
        body = WorkspaceUpdateRequest(
            name=_wire(name, API_UNSET),
            description=_wire(description, API_UNSET),
        )
        return await _acall(
            lambda: update_workspace.asyncio_detailed(
                UUID(workspace_id), client=self._api, body=body
            ),
            _WORKSPACE,
            workspace_id,
        )

    async def upload_deployment(
        self,
        *,
        workspace_id: str,
        code: bytes | BinaryIO,
        requirements: bytes | BinaryIO,
    ) -> DataplaneDeploymentResponse:
        """The awaiting twin of ``HttpTransport.upload_deployment``.

        Args:
            workspace_id: Workspace to deploy into.
            code: The package archive.
            requirements: The requirements manifest.

        Returns:
            The stored deployment, as the data plane wrote it back.
        """
        initiated = await _acall(
            lambda: create_deployment.asyncio_detailed(
                UUID(workspace_id), client=self._api
            ),
            _DEPLOYMENT_UPLOAD,
            workspace_id,
        )
        client, deployment_id = _upload_target(
            initiated,
            initiated.deployment_id,
            "deployments",
            EntityKind.DEPLOYMENT,
            self._verify_ssl,
            self._headers,
        )
        body = DeploymentUploadBody(
            files=_as_file(code, "workspace.tar.gz", _TAR_MIME),
            requirements=_as_file(requirements, "requirements.json", _JSON_MIME),
        )
        try:
            return await _acall(
                lambda: upload_deployment_bytes.asyncio_detailed(
                    deployment_id, client=client, body=body
                ),
                _DP_DEPLOYMENT,
                str(deployment_id),
            )
        finally:
            await _ashut(client)

    async def upload_configuration(
        self, *, workspace_id: str, data: bytes | BinaryIO
    ) -> DataplaneConfigurationResponse:
        """The awaiting twin of ``HttpTransport.upload_configuration``.

        Args:
            workspace_id: Workspace to store the configuration in.
            data: The configuration archive.

        Returns:
            The stored configuration, as the data plane wrote it back.
        """
        initiated = await _acall(
            lambda: create_configuration.asyncio_detailed(
                UUID(workspace_id), client=self._api
            ),
            _CONFIGURATION_UPLOAD,
            workspace_id,
        )
        client, configuration_id = _upload_target(
            initiated,
            initiated.configuration_id,
            "configurations",
            EntityKind.CONFIGURATION,
            self._verify_ssl,
            self._headers,
        )
        body = UploadConfigurationBytesBody(
            file=_as_file(data, "configurations.tar.gz", _TAR_MIME)
        )
        try:
            return await _acall(
                lambda: upload_configuration_bytes.asyncio_detailed(
                    configuration_id, client=client, body=body
                ),
                _DP_CONFIGURATION,
                str(configuration_id),
            )
        finally:
            await _ashut(client)

    async def deploy_manifest(
        self,
        *,
        workspace_id: str,
        jobs: Sequence[Mapping[str, Any]],
        manifest_hash: str,
        engine_version: int,
        module: str | None,
        description: str | None | Keep,
        dry_run: bool,
    ) -> DeployManifestResponse:
        body = _manifest_body(
            jobs, manifest_hash, engine_version, module, description, dry_run
        )
        return await _acall(
            lambda: deploy.asyncio_detailed(
                UUID(workspace_id), client=self._api, body=body
            ),
            _DEPLOY_REPORT,
            workspace_id,
        )

    async def get_configuration(
        self, *, workspace_id: str, version: int
    ) -> ConfigurationResponse:
        return await _acall(
            lambda: get_configuration.asyncio_detailed(
                UUID(workspace_id), version, client=self._api
            ),
            _CONFIGURATION,
            str(version),
        )

    async def get_latest_configuration(
        self, *, workspace_id: str
    ) -> ConfigurationResponse:
        return await _acall(
            lambda: get_latest_configuration.asyncio_detailed(
                UUID(workspace_id), client=self._api
            ),
            _CONFIGURATION,
            "latest",
        )

    async def list_configurations(
        self, *, workspace_id: str, limit: int, offset: int
    ) -> ListConfigurationsResponse200:
        return await _acall(
            lambda: list_configurations.asyncio_detailed(
                UUID(workspace_id), client=self._api, limit=limit, offset=offset
            ),
            _CONFIGURATION_LIST,
            workspace_id,
        )

    async def get_deployment(
        self, *, workspace_id: str, version: int
    ) -> DeploymentResponse:
        return await _acall(
            lambda: get_deployment.asyncio_detailed(
                UUID(workspace_id), version, client=self._api
            ),
            _DEPLOYMENT,
            str(version),
        )

    async def get_latest_deployment(self, *, workspace_id: str) -> DeploymentResponse:
        return await _acall(
            lambda: get_latest_deployment.asyncio_detailed(
                UUID(workspace_id), client=self._api
            ),
            _DEPLOYMENT,
            "latest",
        )

    async def list_deployments(
        self, *, workspace_id: str, limit: int, offset: int
    ) -> ListDeploymentsResponse200:
        return await _acall(
            lambda: list_deployments.asyncio_detailed(
                UUID(workspace_id), client=self._api, limit=limit, offset=offset
            ),
            _DEPLOYMENT_LIST,
            workspace_id,
        )

    async def get_script(
        self, *, workspace_id: str, job_ref: str
    ) -> DetailedScriptResponse:
        return await _acall(
            lambda: get_script.asyncio_detailed(
                UUID(workspace_id), job_ref, client=self._api
            ),
            _SCRIPT_DETAIL,
            job_ref,
        )

    async def list_scripts(
        self, *, workspace_id: str, limit: int, offset: int, archived: bool | Keep
    ) -> ListScriptsResponse200:
        return await _acall(
            lambda: list_scripts.asyncio_detailed(
                UUID(workspace_id),
                client=self._api,
                limit=limit,
                offset=offset,
                archived=_wire(archived, API_UNSET),
            ),
            _SCRIPT_LIST,
            workspace_id,
        )

    async def pause_script(self, *, workspace_id: str, job_ref: str) -> ScriptResponse:
        return await _acall(
            lambda: pause_script.asyncio_detailed(
                UUID(workspace_id), job_ref, client=self._api
            ),
            _SCRIPT,
            job_ref,
        )

    async def resume_script(self, *, workspace_id: str, job_ref: str) -> ScriptResponse:
        return await _acall(
            lambda: resume_script.asyncio_detailed(
                UUID(workspace_id), job_ref, client=self._api
            ),
            _SCRIPT,
            job_ref,
        )


#: Either transport flavour.
AnyTransport = Transport | AsyncTransport


@dataclass
class _StreamReply:
    """A streamed response, shaped so :func:`_unwrap` can classify its status."""

    status_code: HTTPStatus
    content: bytes
    parsed: Any = None


def _log_line(raw: str, run_id: str) -> LogLine:
    """Parse one serialized log line.

    Args:
        raw: The JSON object, from an NDJSON line or an SSE ``data:`` field.
        run_id: The run being read, for the error message.

    Returns:
        The generated model.

    Raises:
        InvalidResponse: The line was not a readable log line.
    """
    try:
        return LogLine.from_dict(json.loads(raw))
    except (ValueError, KeyError, TypeError) as e:
        raise InvalidResponse(f"unreadable log line for run {run_id!r}: {e}") from e


class _Sse:
    """Reassembles an SSE stream, which sends one ``data:`` line per event."""

    def __init__(self) -> None:
        self._event = "message"

    def feed(self, line: str, run_id: str) -> LogLine | None:
        """Take one line of the stream.

        Args:
            line: The raw line, without its newline.
            run_id: The run being followed, for the error message.

        Returns:
            The log line the event carried, or ``None`` for a comment, a
            keep-alive, or an event kind this SDK version does not know.

        Raises:
            ApiError: The platform sent an ``error`` event. It reports these in
                band, on an otherwise successful response.
        """
        if line.startswith("event:"):
            self._event = line[len("event:") :].strip()
            return None
        if not line.startswith("data:"):
            return None
        payload = line[len("data:") :].strip()
        # Blank lines are dropped before they reach here, so the event name is
        # cleared on its data line instead of at the dispatch boundary.
        event, self._event = self._event, "message"
        if event == "error":
            raise ApiError(_sse_error(payload, run_id), status=200)
        return _log_line(payload, run_id) if event == "log" else None


def _sse_error(payload: str, run_id: str) -> str:
    """Read the message out of an SSE error event, however malformed.

    Args:
        payload: The event's ``data:`` field.
        run_id: The run being followed, for the fallback message.

    Returns:
        What the platform said, or a generic message when it said nothing usable.
    """
    try:
        body = json.loads(payload)
    except ValueError:
        body = None
    reported = body.get("error") if isinstance(body, dict) else None
    if isinstance(reported, str) and reported:
        return reported
    return f"the log stream for run {run_id!r} failed"


def _stream_timeout(
    sse: bool, follow: bool
) -> httpx.Timeout | httpx._client.UseClientDefault:
    if not sse:
        return httpx.USE_CLIENT_DEFAULT
    return _STREAM_TIMEOUT if follow else _REPLAY_TIMEOUT


def _log_row(reader: _Sse, line: str, run_id: str, sse: bool) -> LogLine | None:
    """One line of a log body, or ``None`` when it carries no log.

    Both transports read the body the same way; only how they obtain the lines
    differs, so this is where the parsing lives.

    Args:
        reader: Carries SSE state across lines. Unused for NDJSON.
        line: One line of the body, possibly blank.
        run_id: The run being read.
        sse: Whether the body is SSE rather than NDJSON.

    Returns:
        The parsed line, or ``None`` for a blank line or a non-log event.
    """
    if not line:
        return None
    return reader.feed(line, run_id) if sse else _log_line(line, run_id)


def _log_rows(lines: Iterable[str], run_id: str, sse: bool) -> Iterator[LogLine]:
    """Turn a decoded response body into log lines.

    Args:
        lines: The body's lines, blank ones included.
        run_id: The run being read.
        sse: Whether the body is SSE rather than NDJSON.

    Yields:
        One generated model per line the body carried.
    """
    reader = _Sse()
    for line in lines:
        row = _log_row(reader, line, run_id, sse)
        if row is not None:
            yield row


# Read off the attribute, not the getter, which would build a client to close it.
def _shut(client: Client | AuthenticatedClient | DataplaneApiClient) -> None:
    held = client._client
    if held is not None:
        held.close()


async def _ashut(client: Client | AuthenticatedClient | DataplaneApiClient) -> None:
    held = client._async_client
    if held is not None:
        await held.aclose()


def _as_file(content: bytes | BinaryIO, name: str, mime: str) -> File:
    """Wrap what the caller handed over as a multipart part.

    Args:
        content: The bytes, or a binary file object to stream from.
        name: Part filename. The server reads the archive, not this.
        mime: Part content type.

    Returns:
        The generated file wrapper.
    """
    return File(
        payload=BytesIO(content) if isinstance(content, bytes) else content,
        file_name=name,
        mime_type=mime,
    )


def _upload_target(
    initiated: UploadInitiatedResponse,
    entity_id: object,
    collection: str,
    kind: EntityKind,
    verify_ssl: bool = True,
    headers: Mapping[str, str] | None = None,
) -> tuple[DataplaneApiClient, UUID]:
    """Build the client for the upload the platform just authorised.

    The token is scoped to this one upload, so the client is built per call and
    never cached beside the workspace's own.

    Args:
        initiated: What the create call answered.
        entity_id: The id it minted, which the generated route takes.
        collection: The route's collection segment.
        kind: What is being uploaded.
        verify_ssl: The transport's TLS setting, which this client shares.
        headers: The transport's headers, which this client shares.

    Returns:
        A client for that data plane, and the id to address.

    Raises:
        InvalidResponse: The platform authorised no id, or pointed at a URL this
            SDK version will not post to.
    """
    if not isinstance(entity_id, UUID):
        raise InvalidResponse(f"the platform authorised an upload with no {kind} id")
    parsed = urlparse(initiated.upload_url)
    expected = f"/api/v1/{collection}/{entity_id}/upload"
    if parsed.path != expected:
        raise InvalidResponse(
            f"the platform wants the {kind} posted to {parsed.path!r}, not the "
            f"{expected!r} this SDK version builds"
        )
    # A plane may legitimately be plain http: DATAPLANE_API_URL_SCHEME is config.
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise InvalidResponse(
            f"the platform pointed the {kind} upload at {initiated.upload_url!r}, "
            "which is not an http(s) URL"
        )
    client = DataplaneApiClient(
        base_url=f"{parsed.scheme}://{parsed.netloc}",
        token=initiated.upload_token,
        timeout=_UPLOAD_TIMEOUT,
        verify_ssl=verify_ssl,
        headers=dict(headers or {}),
    )
    return client, entity_id


def _manifest_body(
    jobs: Sequence[Mapping[str, Any]],
    manifest_hash: str,
    engine_version: int,
    module: str | None,
    description: str | None | Keep,
    dry_run: bool,
) -> DeployManifestRequest:
    """Build a deploy request, leaving the job definitions opaque.

    Args:
        jobs: Job definitions, as the manifest carries them.
        manifest_hash: Content hash of the manifest they came from.
        engine_version: Manifest engine version they were written for.
        module: Deployment module, or ``None`` for an ad-hoc deploy.
        description: Workspace description, or KEEP to leave it as it is.
        dry_run: Report the plan without persisting it.

    Returns:
        The generated request body.

    Raises:
        BadRequest: A definition the manifest schema does not accept. Caught
            here because the generated model reports it as a plain ``KeyError``.
    """
    try:
        definitions = [TJobDefinition.from_dict(job) for job in jobs]
    except (KeyError, TypeError, ValueError) as e:
        raise BadRequest(
            f"a job definition is not one the platform accepts: {e}"
        ) from e
    return DeployManifestRequest(
        job_definition_engine_version=engine_version,
        job_definition_hash=manifest_hash,
        jobs=definitions,
        deployment_module=module,
        description=_wire(description, API_UNSET),
        dry_run=dry_run,
    )


def _subject(kind: EntityKind, ref: str | None) -> str:
    return f"{kind} {ref!r}" if ref is not None else f"{kind}s"


def _variables_change(
    profile: str | None,
    plain: Mapping[str, str],
    secret: Mapping[str, str],
    deletes: Sequence[str],
) -> VariablesChange:
    """Build a change body, omitting the halves the caller left empty.

    Args:
        profile: The scope to write to; ``None`` is the workspace-level one.
        plain: Names and values to store as plain text.
        secret: Names and values to store as secrets.
        deletes: Names to remove.

    Returns:
        The generated request body.
    """
    upserts: list[PlainVariableUpsert | SecretVariableUpsert] = [
        PlainVariableUpsert(name=name, type_="plain", value=value)
        for name, value in plain.items()
    ]
    upserts += [
        SecretVariableUpsert(name=name, type_="secret", value=value)
        for name, value in secret.items()
    ]
    return VariablesChange(
        profile=profile,
        upserts=upserts or DATAPLANE_UNSET,
        deletes=list(deletes) or DATAPLANE_UNSET,
    )


def _wire(value: V | Keep, unset: U) -> V | U:
    """Map an argument onto the three states a service reads from a body.

    The sentinel is a parameter because each generated package has its own, and
    checks ``isinstance`` against that one.

    Args:
        value: What the caller passed, or :data:`KEEP` if they passed nothing.
        unset: The receiving package's own ``UNSET``.

    Returns:
        ``unset`` for :data:`KEEP`, and the value otherwise — so ``None`` stays
        ``None`` and reaches the platform as a null.
    """
    return unset if value is KEEP else value


def _call(fetch: Callable[[], _Reply[T | E]], op: _Op[T], ref: str | None) -> T:
    """Run one generated sync operation and return its success model.

    Args:
        fetch: Performs the generated call.
        op: The operation's success model and entity kind.
        ref: The id or name being addressed.

    Returns:
        The parsed success model.
    """
    with _transport_errors(op.kind, ref):
        resp = fetch()
    return _unwrap(resp, op, ref)


async def _acall(
    fetch: Callable[[], Awaitable[_Reply[T | E]]], op: _Op[T], ref: str | None
) -> T:
    """Await one generated async operation and return its success model.

    Args:
        fetch: Starts the generated call.
        op: The operation's success model and entity kind.
        ref: The id or name being addressed.

    Returns:
        The parsed success model.
    """
    with _transport_errors(op.kind, ref):
        resp = await fetch()
    return _unwrap(resp, op, ref)


@contextmanager
def _transport_errors(kind: EntityKind, ref: str | None) -> Iterator[None]:
    """Map a failure that produced no usable response onto the public tree.

    Args:
        kind: What the call addresses.
        ref: The id or name being addressed.

    Yields:
        Nothing; the generated call runs inside.

    Raises:
        TransportTimeout: The request timed out.
        ConnectionFailed: The platform could not be reached.
        TransportError: Any other httpx failure, a malformed base URL included.
        InvalidResponse: The body was not JSON.
        BadRequest: An argument the generated call could not build a request
            from, such as an id that is not a uuid.
    """
    try:
        yield
    except DlthubError:
        raise
    except httpx.TimeoutException as e:
        raise TransportTimeout(f"request for {_subject(kind, ref)} timed out") from e
    except httpx.TransportError as e:
        raise ConnectionFailed(
            f"could not reach the platform for {_subject(kind, ref)}: {e}"
        ) from e
    except (httpx.HTTPError, httpx.InvalidURL) as e:
        raise TransportError(f"request for {_subject(kind, ref)} failed: {e}") from e
    except json.JSONDecodeError as e:
        raise InvalidResponse(
            f"the platform's response for {_subject(kind, ref)} was not JSON"
        ) from e
    except ValueError as e:
        # Must stay below JSONDecodeError, which is a ValueError too. Reaching a
        # generated call with an unusable argument never touches the network.
        raise BadRequest(f"invalid argument for {_subject(kind, ref)}: {e}") from e


def _field_errors(resp: _Reply[Any]) -> tuple[FieldError, ...]:
    """Read the per-field reasons the platform put in ``extra``.

    A rejected request names only the request itself in ``detail``; ``extra``
    holds which field was at fault and why. Read from the raw body: the spec
    types ``extra`` as an object, so the generated model mangles the list a
    validation failure actually sends.

    Args:
        resp: The generated response, parsed or not.

    Returns:
        One entry per reason the platform named, empty when it named none.
    """
    try:
        body = json.loads(resp.content)
    except (ValueError, UnicodeDecodeError):
        return ()
    extra = body.get("extra") if isinstance(body, dict) else None
    reasons: list[FieldError] = []
    for item in extra if isinstance(extra, list) else [extra]:
        if isinstance(item, str):
            reasons.append(FieldError(None, item))
            continue
        if not isinstance(item, dict):
            continue
        message = item.get("message") or item.get("detail")
        if isinstance(message, str):
            key = item.get("key")
            reasons.append(FieldError(key if isinstance(key, str) else None, message))
    return tuple(reasons)


def _unwrap(resp: _Reply[T | E], op: _Op[T], ref: str | None) -> T:
    """Return the success model from a generated response, or raise.

    Args:
        resp: The generated ``Response``, carrying both the status and the parsed
            union of success and error models.
        op: The operation's success model and entity kind.
        ref: The id or name that was addressed.

    Returns:
        The parsed success model.

    Raises:
        NotFound: The platform returned 404.
        NotAuthenticated: The platform returned 401.
        NotAuthorized: The platform returned 403.
        Conflict: The platform returned 409.
        BadRequest: The platform returned 400.
        ServerError: The platform returned 5xx.
        InvalidResponse: A success status whose body did not parse.
        ApiError: Any other status.
    """
    parsed = resp.parsed
    if isinstance(parsed, op.model):
        return parsed

    # Every generated error model carries the same code/detail shape, so the
    # status alone picks the class.
    kind = op.kind
    status = int(resp.status_code)
    code = _text(parsed, "code")
    detail = _text(parsed, "detail")
    fields = _field_errors(resp)

    if status == 404:
        raise NotFound(kind, ref, code=code, status=status, fields=fields)
    if status == 401:
        raise NotAuthenticated(
            detail or "not authenticated", code=code, status=status, fields=fields
        )
    if status == 403:
        raise NotAuthorized(
            detail or f"not authorized for {_subject(kind, ref)}",
            code=code,
            status=status,
            fields=fields,
        )
    if status == 409:
        raise Conflict(
            detail or f"{_subject(kind, ref)} is not in a state that allows this",
            code=code,
            status=status,
            fields=fields,
        )
    if status == 400:
        raise BadRequest(
            detail or f"the request for {_subject(kind, ref)} was rejected",
            code=code,
            status=status,
            fields=fields,
        )
    if status >= 500:
        raise ServerError(
            detail
            or f"the platform failed to handle the request for {_subject(kind, ref)}",
            code=code,
            status=status,
            fields=fields,
        )
    if status < 300:
        raise InvalidResponse(
            f"unusable response for {_subject(kind, ref)}",
            code=code,
            status=status,
            fields=fields,
        )
    raise ApiError(
        detail or f"unexpected response for {_subject(kind, ref)}",
        code=code,
        status=status,
        fields=fields,
    )


def _text(parsed: Any, name: str) -> str | None:
    value = getattr(parsed, name, None)
    return value if isinstance(value, str) else None


if TYPE_CHECKING:

    def _protocols_match_the_concrete_transports(
        sync: HttpTransport, asynchronous: AsyncHttpTransport
    ) -> None:
        """Bind each concrete transport to its protocol, so drift fails mypy.

        Args:
            sync: The blocking transport.
            asynchronous: The awaiting transport.
        """
        _sync: Transport = sync
        _async: AsyncTransport = asynchronous
        del _sync, _async


__all__ = [
    "DEFAULT_BASE_URL",
    "AnyTransport",
    "AsyncHttpTransport",
    "AsyncTransport",
    "HttpTransport",
    "Transport",
]
