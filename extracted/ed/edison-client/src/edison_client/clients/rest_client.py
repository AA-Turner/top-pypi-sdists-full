# ruff: noqa: PLR0915
import ast
import asyncio
import atexit
import base64
import contextlib
import copy
import importlib.metadata
import inspect
import json
import logging
import os
import sys
import threading
import time
import warnings
from collections.abc import Collection
from http import HTTPStatus
from pathlib import Path
from types import ModuleType
from typing import Any, ClassVar, Literal, cast, overload
from uuid import UUID

import cloudpickle
import httpx_aiohttp
from aviary.functional import EnvironmentBuilder
from httpx import (
    AsyncClient,
    Client,
    CloseError,
    HTTPStatusError,
    Response,
    codes,
)
from ldp.agent import AgentConfig
from tenacity import (
    before_sleep_log,
    retry,
    stop_after_attempt,
    wait_exponential,
)
from tqdm import tqdm as sync_tqdm
from tqdm.asyncio import tqdm

from edison_client.clients.chat_methods import ChatMethods
from edison_client.clients.clone_methods import CloneMethods
from edison_client.clients.data_storage_methods import DataStorageMethods
from edison_client.clients.directive_methods import DirectiveMethods
from edison_client.clients.session_methods import SessionMethods
from edison_client.clients.state_blobs import (
    StateBlobDownloadError,
    amaterialize_state_blobs,
    materialize_state_blobs,
)
from edison_client.clients.workspace_methods import WorkspaceMethods
from edison_client.models.app import (
    AuthType,
    JobDeploymentConfig,
    JobNames,
    LiteTaskResponse,
    RuntimeConfig,
    Stage,
    TaskRequest,
    TaskResponse,
    TaskResponseVerbose,
    TrajectoryQueryParams,
)
from edison_client.models.data_storage_methods import (
    PermittedAccessors,
    ShareStatus,
)
from edison_client.models.job_event import (
    ExecutionType,
    JobEventBatchCreateRequest,
    JobEventBatchCreateResponse,
    JobEventCreateRequest,
    JobEventCreateResponse,
    JobEventUpdateRequest,
    JobEventUsageResponse,
)
from edison_client.models.rest import (
    ContentLocation,
    DiscoveryResponse,
    ExecutionStatus,
    SearchCriterion,
    SetWarmPoolResponse,
    WorldModel,
    WorldModelCreateResponse,
    WorldModelResponse,
    WorldModelSearchPayload,
)
from edison_client.utils.auth import RefreshingJWT
from edison_client.utils.general import (
    _BASE_CONNECTION_ERRORS,
    create_retry_if_connection_error,
    gather_with_concurrency,
    retry_if_connection_error_not_idempotent,
)
from edison_client.utils.module_utils import (
    OrganizationSelector,
    fetch_environment_function_docstring,
)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
TaskRequest.model_rebuild()

FILE_UPLOAD_IGNORE_PARTS = {
    ".ruff_cache",
    "__pycache__",
    ".git",
    ".pytest_cache",
    ".mypy_cache",
    ".venv",
}


class RestClientError(Exception):
    """Base exception for REST client errors."""


class TaskFetchError(RestClientError):
    """Raised when there's an error fetching a task."""


class JobFetchError(RestClientError):
    """Raised when there's an error fetching a job."""


class JobCreationError(RestClientError):
    """Raised when there's an error creating a job."""


class WorldModelFetchError(RestClientError):
    """Raised when there's an error fetching a world model."""


class WorldModelCreationError(RestClientError):
    """Raised when there's an error creating a world model."""


class WorldModelDeletionError(RestClientError):
    """Raised when there's an error deleting a world model."""


class ProjectError(RestClientError):
    """Raised when there's an error with trajectory group operations."""


class DiscoveryCreationError(RestClientError):
    """Raised when there's an error creating a discovery."""


class DiscoveryFetchError(RestClientError):
    """Raised when there's an error fetching a discovery."""


class InvalidTaskDescriptionError(Exception):
    """Raised when the task description is invalid or empty."""


class SandboxDeleteError(RestClientError):
    """Raised when there's an error deleting a sandbox."""


class FileUploadError(RestClientError):
    """Raised when there's an error uploading a file."""


class JobEventClientError(RestClientError):
    """Raised when there's an error with job event operations."""


class JobEventCreationError(JobEventClientError):
    """Raised when there's an error creating a job event."""


class JobEventUpdateError(JobEventClientError):
    """Raised when there's an error updating a job event."""


class JobEventBatchCreationError(JobEventClientError):
    """Raised when there's an error creating job events in batch."""


class JobEventFetchError(JobEventClientError):
    """Raised when there's an error reading job event usage."""


retry_if_connection_error = create_retry_if_connection_error(FileUploadError)

DEFAULT_AGENT_TIMEOUT: int = 2400  # seconds


class RestClient(  # noqa: PLR0904
    DataStorageMethods,
    ChatMethods,
    DirectiveMethods,
    SessionMethods,
    WorkspaceMethods,
    CloneMethods,
):
    REQUEST_TIMEOUT: ClassVar[float] = 30.0  # sec - for general API calls
    FILE_UPLOAD_TIMEOUT: ClassVar[float] = 600.0  # 10 minutes - for file uploads
    # Above the server's own warm pool wait budget, so a wait that runs to its
    # deadline still returns a ready count instead of timing out client-side.
    WARMPOOL_READY_TIMEOUT: ClassVar[float] = 330.0  # sec
    MAX_RETRY_ATTEMPTS: ClassVar[int] = 3
    RETRY_MULTIPLIER: ClassVar[int] = 1
    MAX_RETRY_WAIT: ClassVar[int] = 10
    DEFAULT_POLLING_TIME: ClassVar[int] = 5  # seconds
    CHUNK_SIZE: ClassVar[int] = 16 * 1024 * 1024  # 16MB chunks

    def __init__(  # noqa: PLR0917
        self,
        stage: str | Stage = Stage.PROD,
        service_uri: str | None = None,
        organization: str | None = None,
        auth_type: AuthType = AuthType.API_KEY,
        api_key: str | None = None,
        jwt: str | None = None,
        headers: dict[str, str] | None = None,
        verbose_logging: bool = False,
        cleanup_on_exit: bool = True,
    ):
        if verbose_logging:
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.WARNING)

        self.stage = stage if isinstance(stage, Stage) else Stage[stage.upper()]
        self.base_url = service_uri or self.stage.value
        self.auth_type = auth_type
        self.api_key = api_key or os.environ.get("EDISON_PLATFORM_API_KEY")
        self._clients: dict[str, Client | AsyncClient] = {}
        self.headers = headers or {}
        self.jwt = jwt
        self._closed = False
        # _close_lock protects us from double closing the client
        # in multi-thread concurrency
        self._close_lock = threading.Lock()
        self._organization = organization
        self._organizations: list[str] | None = None
        # _organizations_lock collapses concurrent first accesses into one fetch
        self._organizations_lock = threading.Lock()
        # because atexit is sync, we can only close
        # sync clients, and "fire and forget" attempts to close
        # the async clients
        if cleanup_on_exit:
            atexit.register(self.close)

    @property
    def organizations(self) -> list[str]:
        """Organizations the caller belongs to, fetched on first access and then cached.

        Raises a ValueError if the `organization` given to the constructor is not one of them.
        """
        with self._organizations_lock:
            if self._organizations is None:
                self._organizations = self._filter_orgs(self._organization)
            return self._organizations

    def check_credentials(self) -> None:
        """Check the credentials against the platform, and the `organization` if one was given.

        Constructing a client makes no request, so call this to fail early on a
        bad API key or JWT instead of on the first real API call.
        """
        _ = self.organizations

    @property
    def client(self) -> Client:
        """Authenticated HTTP client for regular API calls."""
        return self.get_client("application/json", authenticated=True)

    @property
    def async_client(self) -> AsyncClient:
        """Authenticated async HTTP client for regular API calls."""
        return self.get_client(
            "application/json", authenticated=True, async_client=True
        )

    @property
    def unauthenticated_client(self) -> Client:
        """Unauthenticated HTTP client for auth operations."""
        return self.get_client("application/json", authenticated=False)

    @property
    def multipart_client(self) -> Client:
        """Authenticated HTTP client for multipart uploads."""
        return self.get_client(None, authenticated=True)

    @property
    def file_upload_client(self) -> Client:
        """Authenticated HTTP client with extended timeout for file uploads."""
        return self.get_client(
            "application/json", authenticated=True, timeout=self.FILE_UPLOAD_TIMEOUT
        )

    @property
    def async_file_upload_client(self) -> AsyncClient:
        """Authenticated async HTTP client with extended timeout for file uploads."""
        return self.get_client(
            "application/json",
            authenticated=True,
            async_client=True,
            timeout=self.FILE_UPLOAD_TIMEOUT,
        )

    @overload
    def get_client(
        self,
        content_type: str | None = "application/json",
        authenticated: bool = True,
        async_client: Literal[False] = False,
        timeout: float | None = None,
    ) -> Client: ...

    @overload
    def get_client(
        self,
        content_type: str | None = "application/json",
        authenticated: bool = True,
        *,
        async_client: Literal[True],
        timeout: float | None = None,
    ) -> AsyncClient: ...

    def get_client(
        self,
        content_type: str | None = "application/json",
        authenticated: bool = True,
        async_client: bool = False,
        timeout: float | None = None,
    ) -> Client | AsyncClient:
        """Return a cached HTTP client or create one if needed.

        Args:
            content_type: The desired content type header. Use None for multipart uploads.
            authenticated: Whether the client should include authentication.
            async_client: Whether to use an async client.
            timeout: Custom timeout in seconds. Uses REQUEST_TIMEOUT if not provided.

        Returns:
            An HTTP client configured with the appropriate headers.
        """
        if self._closed:
            raise RuntimeError("RestClient has been closed")

        client_timeout = timeout or self.REQUEST_TIMEOUT
        key = f"{content_type or 'multipart'}_{authenticated}_{async_client}_{client_timeout}"

        if key not in self._clients:
            headers = copy.deepcopy(self.headers)
            auth = None

            if authenticated:
                auth = RefreshingJWT(
                    # authenticated=False will always return a synchronous client
                    auth_client=self.get_client(
                        "application/json", authenticated=False
                    ),
                    auth_type=self.auth_type,
                    api_key=self.api_key,
                    jwt=self.jwt,
                )

            if content_type:
                headers["Content-Type"] = content_type

            headers["x-client"] = "sdk"

            self._clients[key] = (
                httpx_aiohttp.HttpxAiohttpClient(
                    base_url=self.base_url,
                    headers=headers,
                    timeout=client_timeout,
                    auth=auth,
                )
                if async_client
                else Client(
                    base_url=self.base_url,
                    headers=headers,
                    timeout=client_timeout,
                    auth=auth,
                )
            )

        return self._clients[key]

    def __del__(self):
        """Remove sync httpx clients."""
        if getattr(self, "_closed", True):
            return

        # Only close sync clients in __del__
        # Async clients will show warnings but that's unavoidable from __del__
        for client in getattr(self, "_clients", {}).values():
            if isinstance(client, Client):
                try:
                    client.close()
                except Exception as e:
                    logger.debug(
                        "Error closing sync client in __del__: %s", e, exc_info=True
                    )

    def close(self):
        """Explicitly close all cached clients (sync clients immediately, async best-effort)."""
        with self._close_lock:
            if self._closed:
                return
            self._closed = True

            # Take ownership of clients dict
            clients_to_close = self._clients
            self._clients = {}

        # Close outside the lock
        for client in clients_to_close.values():
            if isinstance(client, Client):
                with contextlib.suppress(RuntimeError, CloseError):
                    client.close()
            elif isinstance(client, AsyncClient):
                # Best-effort async close from sync context
                self._schedule_async_close(client)

    def _schedule_async_close(self, client: AsyncClient):
        """Schedule async client close - best effort from sync context."""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop is not None and loop.is_running():
            # There's a running loop - schedule the close as a task
            # This won't block and the task will run when the loop gets to it
            _ = loop.create_task(self._safe_aclose(client))
        else:
            # No running loop - try to create one just for cleanup
            with contextlib.suppress(RuntimeError):
                asyncio.run(self._safe_aclose(client))

    async def aclose(self):
        """Asynchronously close all cached clients."""
        with self._close_lock:
            if self._closed:
                return
            self._closed = True

            clients_to_close = self._clients
            self._clients = {}

        # Separate sync and async clients
        async_close_tasks = []
        for client in clients_to_close.values():
            if isinstance(client, AsyncClient):
                async_close_tasks.append(self._safe_aclose(client))
            elif isinstance(client, Client):
                with contextlib.suppress(RuntimeError, CloseError):
                    client.close()

        # Close all async clients concurrently
        # return_exceptions=True will act as suppression here for errors
        if async_close_tasks:
            await asyncio.gather(*async_close_tasks, return_exceptions=True)

    @staticmethod
    async def _safe_aclose(client: AsyncClient) -> None:
        """Safely close an async client, suppressing common errors."""
        with contextlib.suppress(RuntimeError, CloseError):
            await client.aclose()

    def _filter_orgs(self, organization: str | None = None) -> list[str]:
        filtered_orgs = [
            org
            for org in self._fetch_my_orgs()
            if (org == organization or organization is None)
        ]
        if not filtered_orgs:
            raise ValueError(f"Organization '{organization}' not found.")
        return filtered_orgs

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def _check_job(self, name: str, organization: str) -> dict[str, Any]:
        response = self.client.get(f"/v0.1/crows/{name}/organizations/{organization}")
        response.raise_for_status()
        return response.json()

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def _fetch_my_orgs(self) -> list[str]:
        response = self.client.get(f"/v0.1/organizations?filter={True}")
        response.raise_for_status()
        orgs = response.json()
        return [org["name"] for org in orgs]

    @staticmethod
    def _validate_module_path(path: Path) -> None:
        """Validates that the given path exists and is a directory.

        Args:
            path: Path to validate

        Raises:
            JobFetchError: If the path is not a directory

        """
        if not path.is_dir():
            raise JobFetchError(f"Path {path} is not a directory.")

    @staticmethod
    def _validate_template_path(template_path: str | os.PathLike) -> None:
        """
        Validates that a template path exists and is a file.

        Args:
            template_path: Path to validate

        Raises:
            FileNotFoundError: If the template path doesn't exist
            ValueError: If the path exists but isn't a file
        """
        template_path = Path(template_path)
        if not template_path.exists():
            raise FileNotFoundError(
                f"Markdown template file not found: {template_path}"
            )
        if not template_path.is_file():
            raise ValueError(
                f"Markdown template path exists but is not a file: {template_path}"
            )

    @staticmethod
    def _validate_files(files: list, path: str | os.PathLike) -> None:
        """Validates that files were found in the given path.

        Args:
            files: List of collected files
            path: Path that was searched for files

        Raises:
            TaskFetchError: If no files were found

        """
        if not files:
            raise TaskFetchError(f"No files found in {path}.")

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def get_task(
        self,
        task_id: str | None = None,
        history: bool = False,
        verbose: bool = False,
        lite: bool = False,
    ) -> TaskResponse | TaskResponseVerbose | LiteTaskResponse:
        """Get details for a specific task.

        Args:
            task_id: Task to fetch. Defaults to this client's trajectory_id.
            history: Include every historical agent_state instead of just
                the latest. Dramatically increases the response size.
            verbose: Return the full `TaskResponseVerbose` rather than the
                job-specific response model.
            lite: Return only id / status / query.

        A caller without view access to the task gets a `PermissionError`.

        Raises:
            TaskFetchError: If a state blob could not be downloaded.
        """
        task_id = task_id or self.trajectory_id

        data = self._fetch_task_payload(
            f"/v0.2/trajectories/{task_id}",
            task_id,
            params={"history": history, "lite": lite},
        )

        if not lite:
            try:
                materialize_state_blobs(data)
            except StateBlobDownloadError as e:
                raise TaskFetchError(f"Error getting task {task_id}: {e}") from e

        return self._build_task_response(data, verbose=verbose, lite=lite)

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aget_task(
        self,
        task_id: str | None = None,
        history: bool = False,
        verbose: bool = False,
        lite: bool = False,
    ) -> TaskResponse | TaskResponseVerbose | LiteTaskResponse:
        """Get details for a specific task asynchronously.

        See `get_task` for argument and error semantics.
        """
        task_id = task_id or self.trajectory_id

        data = await self._afetch_task_payload(
            f"/v0.2/trajectories/{task_id}",
            task_id,
            params={"history": history, "lite": lite},
        )

        if not lite:
            try:
                await amaterialize_state_blobs(data)
            except StateBlobDownloadError as e:
                raise TaskFetchError(f"Error getting task {task_id}: {e}") from e

        return self._build_task_response(data, verbose=verbose, lite=lite)

    def _fetch_task_payload(
        self,
        url: str,
        task_id: str,
        *,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        with self.client.stream("GET", url, params=params) as response:
            if response.status_code in {codes.UNAUTHORIZED, codes.FORBIDDEN}:
                raise PermissionError(
                    f"Error getting task: Permission denied for task {task_id}"
                )
            if response.status_code >= codes.BAD_REQUEST:
                # ``raise_for_status`` on a streamed response leaves the body
                # unread, but the route-absent check needs ``detail`` — and a
                # read body also makes the raised error inspectable.
                response.read()
            response.raise_for_status()
            data = json.loads("".join(response.iter_text(chunk_size=1024)))

        if "id" not in data:
            data["id"] = task_id
        return data

    async def _afetch_task_payload(
        self,
        url: str,
        task_id: str,
        *,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        """Async counterpart of `_fetch_task_payload`."""
        async with self.async_client.stream("GET", url, params=params) as response:
            if response.status_code in {codes.UNAUTHORIZED, codes.FORBIDDEN}:
                raise PermissionError(
                    f"Error getting task: Permission denied for task {task_id}"
                )
            if response.status_code >= codes.BAD_REQUEST:
                await response.aread()
            response.raise_for_status()
            data = json.loads("".join([chunk async for chunk in response.aiter_text()]))

        if "id" not in data:
            data["id"] = task_id
        return data

    @staticmethod
    def _build_task_response(
        data: dict[str, Any], *, verbose: bool, lite: bool
    ) -> TaskResponse | TaskResponseVerbose | LiteTaskResponse:
        if lite:
            return LiteTaskResponse(**data)

        verbose_response = TaskResponseVerbose(**data)
        if verbose:
            return verbose_response
        return JobNames.get_response_object_from_job(verbose_response.job_name)(**data)

    # ------------------------------------------------------------------
    # Inline v0.1 reads. Reached only through the deprecated ``_v0d1``
    # hatches below — nothing falls back here on its own.
    # ------------------------------------------------------------------

    def _get_task_inline(
        self, task_id: str, *, history: bool, verbose: bool, lite: bool
    ) -> TaskResponse | TaskResponseVerbose | LiteTaskResponse:
        """Read a task from v0.1, which inlines state blobs server-side."""
        data = self._fetch_task_payload(
            f"/v0.1/trajectories/{task_id}",
            task_id,
            params={"history": history, "lite": lite},
        )
        return self._build_task_response(data, verbose=verbose, lite=lite)

    async def _aget_task_inline(
        self, task_id: str, *, history: bool, verbose: bool, lite: bool
    ) -> TaskResponse | TaskResponseVerbose | LiteTaskResponse:
        """Async counterpart of `_get_task_inline`."""
        data = await self._afetch_task_payload(
            f"/v0.1/trajectories/{task_id}",
            task_id,
            params={"history": history, "lite": lite},
        )
        return self._build_task_response(data, verbose=verbose, lite=lite)

    # ------------------------------------------------------------------
    # Deprecated; will be removed once all
    # deployments have v0.2 support and we've confirmed no callers
    # are pinning to these paths.
    # ------------------------------------------------------------------

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def _get_task_v0d1(
        self,
        task_id: str | None = None,
        history: bool = False,
        verbose: bool = False,
        lite: bool = False,
    ) -> TaskResponse | TaskResponseVerbose | LiteTaskResponse:
        """Deprecated: read the task from the inline v0.1 endpoint."""
        warnings.warn(
            "_get_task_v0d1 is deprecated; use get_task.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._get_task_inline(
            task_id or self.trajectory_id, history=history, verbose=verbose, lite=lite
        )

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def _aget_task_v0d1(
        self,
        task_id: str | None = None,
        history: bool = False,
        verbose: bool = False,
        lite: bool = False,
    ) -> TaskResponse | TaskResponseVerbose | LiteTaskResponse:
        """Deprecated: read the task from the inline v0.1 endpoint."""
        warnings.warn(
            "_aget_task_v0d1 is deprecated; use aget_task.",
            DeprecationWarning,
            stacklevel=2,
        )
        return await self._aget_task_inline(
            task_id or self.trajectory_id, history=history, verbose=verbose, lite=lite
        )

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def cancel_task(self, task_id: str | None = None) -> bool:
        """Cancel a specific task/trajectory."""
        task_id = task_id or self.trajectory_id
        url = f"/v0.1/trajectories/{task_id}/cancel"

        get_task_response = self.get_task(task_id, lite=True)
        # cancel unless the task already reached a terminal state (queued + in progress)
        if get_task_response.status not in ExecutionStatus.terminal_states():
            response = self.client.post(url)
            try:
                response.raise_for_status()

            except HTTPStatusError as e:
                if e.response.status_code in {
                    HTTPStatus.UNAUTHORIZED,
                    HTTPStatus.FORBIDDEN,
                }:
                    raise PermissionError(
                        f"Error canceling task: Permission denied for task {task_id}"
                    ) from e
                if e.response.status_code == HTTPStatus.NOT_FOUND:
                    raise TaskFetchError(
                        f"Error canceling task: Trajectory not found for task {task_id}"
                    ) from e
                raise

            get_task_response = self.get_task(task_id, lite=True)
            return get_task_response.status == ExecutionStatus.CANCELLED.value
        return False

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def acancel_task(self, task_id: str | None = None) -> bool:
        """Cancel a specific task/trajectory asynchronously."""
        task_id = task_id or self.trajectory_id
        url = f"/v0.1/trajectories/{task_id}/cancel"

        get_task_response = await self.aget_task(task_id, lite=True)
        # cancel unless the task already reached a terminal state (queued + in progress)
        if get_task_response.status not in ExecutionStatus.terminal_states():
            response = await self.async_client.post(url)
            try:
                response.raise_for_status()

            except HTTPStatusError as e:
                if e.response.status_code in {
                    HTTPStatus.UNAUTHORIZED,
                    HTTPStatus.FORBIDDEN,
                }:
                    raise PermissionError(
                        f"Error canceling task: Permission denied for task {task_id}"
                    ) from e
                if e.response.status_code == HTTPStatus.NOT_FOUND:
                    raise TaskFetchError(
                        f"Error canceling task: Trajectory not found for task {task_id}"
                    ) from e
                raise

            get_task_response = await self.aget_task(task_id, lite=True)
            return get_task_response.status == ExecutionStatus.CANCELLED.value
        return False

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def create_task(
        self,
        task_data: TaskRequest | dict[str, Any],
        files: list[str] | None = None,
    ):
        """Create a new futurehouse task.

        Args:
            task_data: The task request data
            files: Optional list of data_entry URIs to attach as files (e.g., ['data_entry:uuid'])
        """
        if isinstance(task_data, dict):
            task_data = TaskRequest.model_validate(task_data)

        self._validate_and_add_file_uris(files, task_data)

        if isinstance(task_data.name, JobNames):
            task_data.name = task_data.name.from_stage(
                task_data.name.name,
                self.stage,
            )

        response = self.client.post(
            "/v0.1/crows", json=task_data.model_dump(mode="json", by_alias=True)
        )
        if response.status_code in {401, 403}:
            raise PermissionError(
                f"Error creating task: Permission denied for task {task_data.name}."
            )
        response.raise_for_status()
        trajectory_id = response.json()["trajectory_id"]
        self.trajectory_id = trajectory_id  # pylint: disable=attribute-defined-outside-init
        return trajectory_id

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def acreate_task(
        self,
        task_data: TaskRequest | dict[str, Any],
        files: list[str] | None = None,
    ):
        """Create a new futurehouse task.

        Args:
            task_data: The task request data
            files: Optional list of data_entry URIs to attach as files (e.g., ['data_entry:uuid'])
        """
        if isinstance(task_data, dict):
            task_data = TaskRequest.model_validate(task_data)

        self._validate_and_add_file_uris(files, task_data)

        if isinstance(task_data.name, JobNames):
            task_data.name = task_data.name.from_stage(
                task_data.name.name,
                self.stage,
            )

        response = await self.async_client.post(
            "/v0.1/crows", json=task_data.model_dump(mode="json", by_alias=True)
        )
        if response.status_code in {401, 403}:
            raise PermissionError(
                f"Error creating task: Permission denied for task {task_data.name}."
            )
        response.raise_for_status()
        trajectory_id = response.json()["trajectory_id"]
        self.trajectory_id = trajectory_id  # pylint: disable=attribute-defined-outside-init
        return trajectory_id

    def _warmpool_request(
        self, crow_key: str, replicas: int, wait: bool, timeout: float | None
    ) -> tuple[str, dict[str, Any], float]:
        """URL, body and effective client timeout for a warm pool resize."""
        return (
            f"/v0.1/crows/{crow_key}/warmpool",
            {"replicas": replicas, "wait": wait},
            timeout or (self.WARMPOOL_READY_TIMEOUT if wait else self.REQUEST_TIMEOUT),
        )

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def set_crow_warmpool(
        self,
        crow_key: str,
        replicas: int,
        wait: bool = False,
        timeout: float | None = None,
    ) -> SetWarmPoolResponse:
        """Resize a crow's sandbox warm pool. Requires maintainer access.

        The pool is not scaled back down automatically; the caller owns that.

        Args:
            crow_key: The crow whose warm pool to resize.
            replicas: Target number of warm sandbox pods.
            wait: Block until that many pods report Ready, or the server's wait
                budget elapses. A wait that runs out still returns 200 with the
                observed count and `timed_out=True`.
            timeout: Client-side timeout override. Defaults to
                `WARMPOOL_READY_TIMEOUT` when waiting, `REQUEST_TIMEOUT` otherwise,
                because a wait outlives the general request timeout.
        """
        url, payload, client_timeout = self._warmpool_request(
            crow_key, replicas, wait, timeout
        )
        client = self.get_client(
            "application/json", authenticated=True, timeout=client_timeout
        )
        response = client.post(url, json=payload)
        response.raise_for_status()
        return SetWarmPoolResponse.model_validate(response.json())

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aset_crow_warmpool(
        self,
        crow_key: str,
        replicas: int,
        wait: bool = False,
        timeout: float | None = None,
    ) -> SetWarmPoolResponse:
        """Resize a crow's sandbox warm pool. Requires maintainer access.

        See `set_crow_warmpool` for the argument semantics.
        """
        url, payload, client_timeout = self._warmpool_request(
            crow_key, replicas, wait, timeout
        )
        client = self.get_client(
            "application/json",
            authenticated=True,
            async_client=True,
            timeout=client_timeout,
        )
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return SetWarmPoolResponse.model_validate(response.json())

    @staticmethod
    def _validate_and_add_file_uris(files, task_data):
        if files:
            # Add files into environment_config if provided
            if task_data.runtime_config is None:
                task_data.runtime_config = RuntimeConfig()
            if task_data.runtime_config.environment_config is None:
                task_data.runtime_config.environment_config = {}

            if task_data.runtime_config.environment_config.get(
                "data_storage_uris", None
            ):
                raise ValueError(
                    "Please provide file uris either in the files parameter or within the environment configuration, not both."
                )

            task_data.runtime_config.environment_config["data_storage_uris"] = files

    async def arun_tasks_until_done(
        self,
        task_data: (
            TaskRequest
            | dict[str, Any]
            | Collection[TaskRequest]
            | Collection[dict[str, Any]]
        ),
        *,
        verbose: bool = False,
        progress_bar: bool = False,
        concurrency: int = 10,
        timeout: float | None = DEFAULT_AGENT_TIMEOUT,
        files: list[str] | None = None,
    ) -> list[LiteTaskResponse | TaskResponse | TaskResponseVerbose]:
        # Convert single task to collection
        is_single_task = isinstance(task_data, dict) or not isinstance(
            task_data, Collection
        )
        all_tasks: Collection[TaskRequest | dict[str, Any]] = (
            cast(Collection[TaskRequest | dict[str, Any]], [task_data])
            if is_single_task
            else cast(Collection[TaskRequest | dict[str, Any]], task_data)
        )

        trajectory_ids = await gather_with_concurrency(
            concurrency,
            [self.acreate_task(task, files=files) for task in all_tasks],
            progress=progress_bar,
        )

        start_time = time.monotonic()
        completed_tasks: dict[str, LiteTaskResponse | TaskResponse] = {}

        if progress_bar:
            progress = tqdm(
                total=len(trajectory_ids), desc="Waiting for tasks to finish", ncols=0
            )

        while timeout is None or (time.monotonic() - start_time) < timeout:
            task_results = await gather_with_concurrency(
                concurrency,
                [
                    self.aget_task(task_id, verbose=verbose, lite=True)
                    for task_id in trajectory_ids
                    if task_id not in completed_tasks
                ],
            )

            for task in task_results:
                task_id = str(task.task_id)
                if (
                    task_id not in completed_tasks
                    and ExecutionStatus(task.status).is_terminal_state()
                ):
                    # on completion fetches the full state and messages of the task
                    completed_tasks[task_id] = await self.aget_task(
                        task_id=task_id,
                        lite=False,
                        verbose=verbose,
                    )
                    if progress_bar:
                        progress.update(1)

            all_done = len(completed_tasks) == len(trajectory_ids)

            if all_done:
                break
            await asyncio.sleep(self.DEFAULT_POLLING_TIME)

        else:
            logger.warning(
                f"Timed out waiting for tasks to finish after {timeout} seconds. Returning with {len(completed_tasks)} completed tasks and {len(trajectory_ids)} total tasks."
            )

        if progress_bar:
            progress.close()

        return [
            completed_tasks.get(task_id)
            or (await self.aget_task(task_id, verbose=verbose))
            for task_id in trajectory_ids
        ]

    def run_tasks_until_done(
        self,
        task_data: (
            TaskRequest
            | dict[str, Any]
            | Collection[TaskRequest]
            | Collection[dict[str, Any]]
        ),
        verbose: bool = False,
        progress_bar: bool = False,
        timeout: float | None = DEFAULT_AGENT_TIMEOUT,
        files: list[str] | None = None,
    ) -> list[LiteTaskResponse | TaskResponse | TaskResponseVerbose]:
        """Run multiple tasks and wait for them to complete.

        Args:
            task_data: A single task or collection of tasks to run
            verbose: Whether to return verbose task responses
            progress_bar: Whether to display a progress bar
            timeout: Maximum time to wait for task completion in seconds,
                or wait indefinitely if None.
            files: Optional list of data_entry URIs to attach as files (only for single task)

        Returns:
            A list of completed task responses
        """
        # Convert single task to collection
        is_single_task = isinstance(task_data, dict) or not isinstance(
            task_data, Collection
        )
        all_tasks: Collection[TaskRequest | dict[str, Any]] = (
            cast(Collection[TaskRequest | dict[str, Any]], [task_data])
            if is_single_task
            else cast(Collection[TaskRequest | dict[str, Any]], task_data)
        )

        # If files are provided and it's a single task, pass files to create_task
        trajectory_ids = [self.create_task(task, files=files) for task in all_tasks]

        start_time = time.monotonic()
        completed_tasks: dict[str, LiteTaskResponse | TaskResponse] = {}

        if progress_bar:
            progress = sync_tqdm(
                total=len(trajectory_ids), desc="Waiting for tasks to finish", ncols=0
            )

        while timeout is None or (time.monotonic() - start_time) < timeout:
            all_done = True

            for task_id in trajectory_ids:
                if task_id in completed_tasks:
                    continue

                task = self.get_task(task_id, verbose=verbose, lite=True)

                if not ExecutionStatus(task.status).is_terminal_state():
                    all_done = False
                elif task_id not in completed_tasks:
                    completed_tasks[task_id] = self.get_task(
                        task_id=task_id,
                        lite=False,
                        verbose=verbose,
                    )
                    if progress_bar:
                        progress.update(1)

            if all_done:
                break
            time.sleep(self.DEFAULT_POLLING_TIME)

        else:
            logger.warning(
                f"Timed out waiting for tasks to finish after {timeout} seconds. Returning with {len(completed_tasks)} completed tasks and {len(trajectory_ids)} total tasks."
            )

        if progress_bar:
            progress.close()

        return [
            completed_tasks.get(task_id) or self.get_task(task_id, verbose=verbose)
            for task_id in trajectory_ids
        ]

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def get_build_status(self, build_id: UUID | None = None) -> dict[str, Any]:
        """Get the status of a build."""
        build_id = build_id or self.build_id
        response = self.client.get(f"/v0.1/builds/{build_id}")
        response.raise_for_status()
        return response.json()

    # TODO: [PLA-1156] Refactor later so we don't have to ignore PLR0915
    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def create_job(self, config: JobDeploymentConfig) -> dict[str, Any]:  # noqa: PLR0914
        """Creates a futurehouse job deployment from the environment and environment files.

        Args:
            config: Configuration object containing all necessary parameters for job deployment.

        Returns:
            A response object containing metadata of the build.

        """
        task_description: str = config.task_description or str(
            fetch_environment_function_docstring(
                config.environment,
                config.path,  # type: ignore[arg-type]
                "from_task",
            )
            if config.functional_environment is None
            else config.functional_environment.start_fn.__doc__
        )
        if not task_description or not task_description.strip():
            raise InvalidTaskDescriptionError(
                "Task description cannot be None or empty. Ensure your from_task environment function has a valid docstring."
                " If you are deploying with your Environment as a dependency, "
                "you must add a `task_description` to your `JobDeploymentConfig`.",
            )
        selected_org = OrganizationSelector.select_organization(self.organizations)
        if selected_org is None:
            return {
                "status": "cancelled",
                "message": "Organization selection cancelled",
            }
        try:
            try:
                job_status = self._check_job(config.job_name, selected_org)
                if job_status["exists"]:
                    if config.force:
                        logger.warning(
                            f"Overwriting existing deployment '{job_status['name']}'"
                        )
                    else:
                        user_response = input(
                            f"A deployment named '{config.job_name}' already exists. Do you want to proceed? [y/N]: "
                        )
                        if user_response.lower() != "y":
                            logger.info("Deployment cancelled.")
                            return {
                                "status": "cancelled",
                                "message": "User cancelled deployment",
                            }
            except Exception:
                logger.warning("Unable to check for existing deployment, proceeding.")
            encoded_pickle = None
            if config.functional_environment is not None:
                # TODO(remo): change aviary fenv code to have this happen automatically.
                for t in config.functional_environment.tools:
                    t._force_pickle_fn = True
                pickled_env = cloudpickle.dumps(config.functional_environment)
                encoded_pickle = base64.b64encode(pickled_env).decode("utf-8")
            files = []
            ignore_parts = set(FILE_UPLOAD_IGNORE_PARTS) | set(config.ignore_dirs or [])
            for file_path in Path(config.path).rglob("*") if config.path else []:
                if any(ignore in file_path.parts for ignore in ignore_parts):
                    continue

                if file_path.is_file():
                    relative_path = (
                        f"{config.module_name}/{file_path.relative_to(config.path)}"  # type: ignore[arg-type]
                    )
                    files.append(
                        (
                            "files",
                            (
                                relative_path,
                                file_path.read_bytes(),
                                "application/octet-stream",
                            ),
                        ),
                    )
            if (
                config.functional_environment is not None
                and config.requirements is not None
            ):
                requirements_content = "\n".join(config.requirements)
                files.append(
                    (
                        "files",
                        (
                            f"{config.environment}/requirements.txt",
                            requirements_content.encode(),
                            "text/plain",
                        ),
                    ),
                )
            if config.requirements_path:
                requirements_path = Path(config.requirements_path)
                files.append(
                    (
                        "files",
                        (
                            f"{config.module_name}/{requirements_path.name}",
                            requirements_path.read_bytes(),
                            "application/octet-stream",
                        ),
                    ),
                )
            if config.path:
                self._validate_files(files, config.path)
            markdown_template_file = None
            if config.markdown_template_path:
                self._validate_template_path(config.markdown_template_path)
                template_path = Path(config.markdown_template_path)
                markdown_template_file = (
                    "files",
                    (
                        "markdown_template",
                        template_path.read_bytes(),
                        "application/octet-stream",
                    ),
                )
            logger.debug(f"Sending files: {[f[1][0] for f in files]}")
            data = {
                "agent": (
                    config.agent.model_dump_json()
                    if isinstance(config.agent, AgentConfig)
                    else config.agent
                ),
                "job_name": config.job_name,
                "organization": selected_org,
                "environment": config.environment,
                "functional_environment_pickle": encoded_pickle,
                "python_version": config.python_version,
                "task_description": task_description,
                "environment_variables": (
                    json.dumps(config.environment_variables)
                    if config.environment_variables
                    else None
                ),
                "container_config": (
                    config.container_config.model_dump_json()
                    if config.container_config
                    else None
                ),
                "timeout": config.timeout,
                "frame_paths": (
                    json.dumps(
                        [fp.model_dump() for fp in config.frame_paths],
                    )
                    if config.frame_paths
                    else None
                ),
                "task_queues_config": (
                    config.task_queues_config.model_dump_json()
                    if config.task_queues_config
                    else None
                ),
                "user_input_config": (
                    json.dumps([
                        entity.model_dump() for entity in config.user_input_config
                    ])
                    if config.user_input_config
                    else None
                ),
                "cache_strategy": config.cache_strategy,
                "is_chat": str(config.is_chat).lower(),
                "push_to": json.dumps([r.value for r in config.push_to]),
            }
            if config.sandbox_infra_manager_image:
                data["sandbox_infra_manager_image"] = config.sandbox_infra_manager_image
            # Include git metadata for deployment tracking if provided
            if config.commit_hash:
                data["commit_hash"] = config.commit_hash
            if config.git_patch:
                data["git_patch"] = config.git_patch
            if config.branch_name:
                data["branch_name"] = config.branch_name
            if config.git_status:
                data["git_status"] = config.git_status
            if config.image_uri:
                data["image_uri"] = config.image_uri
            response = self.multipart_client.post(
                "/v0.1/builds",
                data=data,
                files=(
                    [*files, markdown_template_file]
                    if markdown_template_file
                    else files
                ),
                headers={"Accept": "application/json"},
                params={"internal-deps": config.requires_aviary_internal},
            )
            try:
                response.raise_for_status()
                build_context = response.json()
                self.build_id = build_context["build_id"]  # pylint: disable=attribute-defined-outside-init
            except HTTPStatusError as e:
                error_detail = response.json()
                error_message = error_detail.get("detail", str(e))
                raise JobCreationError(
                    f"Server validation error: {error_message}."
                ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise JobCreationError(f"Error generating docker image: {e!r}.") from e
        return build_context

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def upload_file(  # noqa: PLR0917
        self,
        file_path: str | os.PathLike,
        name: str | None = None,
        description: str | None = None,
        project_id: UUID | None = None,
        dataset_id: UUID | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        embedding: list[float] | None = None,
    ) -> str:
        """Upload a file or directory using the data storage service.

        Args:
            file_path: The local path to the file or directory to upload.
            name: Name for the data storage entry (defaults to filename).
            description: Optional description of the file.
            project_id: ID of the project this file belongs to.
            dataset_id: ID of the dataset this file belongs to.
            metadata: Optional metadata for the file.
            tags: Optional tags for the file.
            embedding: Optional embedding vector for the file content.

        Returns:
            Data entry URI in format "data_entry:{uuid}" for use in
            runtime_config.data_storage_uris when submitting tasks.

        Raises:
            FileNotFoundError: If the file or directory does not exist.
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File or directory not found: {file_path}")

        if name is None:
            name = file_path.name

        # Use the data storage methods from the mixin
        response = self.store_file_content(
            name=name,
            file_path=file_path,
            description=description,
            project_id=project_id,
            dataset_id=dataset_id,
            metadata=metadata,
            tags=tags,
            embedding=embedding,
        )

        logger.info(
            f"Successfully uploaded {file_path} as data_entry:{response.data_storage.id}"
        )
        return f"data_entry:{response.data_storage.id}"

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def list_files(
        self,
        trajectory_id: str,
    ) -> dict[str, Any]:
        """List files associated with a trajectory using the provenance API.

        Args:
            trajectory_id: The specific trajectory id to list files from.

        Returns:
            Dict of data storage provenance entries with full entry details.
            Each entry contains provenance info and the associated data_storage object.

        Raises:
            RestClientError: If there is an error listing the files.
        """
        try:
            url = "/v0.1/data-storage/provenance/data-entries"
            params = self._list_files_params(trajectory_id)

            # provenance/data-entries returns a StreamingResponse. We consume it here.
            with self.client.stream("GET", url, params=params) as response:
                response.raise_for_status()
                json_data = "".join(response.iter_text(chunk_size=self.CHUNK_SIZE))
            return json.loads(json_data)
        except HTTPStatusError as e:
            logger.exception(
                f"Error listing files for trajectory {trajectory_id}: {e.response.text}"
            )
            raise RestClientError(
                f"Error listing files: {e.response.status_code} - {e.response.text}."
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            logger.exception(f"Error listing files for trajectory {trajectory_id}")
            raise RestClientError(f"Error listing files: {e!r}.") from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def alist_files(
        self,
        trajectory_id: str,
    ) -> dict[str, Any]:
        """List files associated with a trajectory using the provenance API.

        Args:
            trajectory_id: The specific trajectory id to list files from.

        Returns:
            Dict of data storage provenance entries with full entry details.
            Each entry contains provenance info and the associated data_storage object.

        Raises:
            RestClientError: If there is an error listing the files.
        """
        try:
            url = "/v0.1/data-storage/provenance/data-entries"
            params = self._list_files_params(trajectory_id)

            # provenance/data-entries returns a StreamingResponse. We consume it here.
            async with self.async_client.stream("GET", url, params=params) as response:
                response.raise_for_status()
                json_data = "".join([chunk async for chunk in response.aiter_text()])
            return json.loads(json_data)
        except HTTPStatusError as e:
            logger.exception(
                f"Error listing files for trajectory {trajectory_id}: {e.response.text}"
            )
            raise RestClientError(
                f"Error listing files: {e.response.status_code} - {e.response.text}."
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            logger.exception(f"Error listing files for trajectory {trajectory_id}")
            raise RestClientError(f"Error listing files: {e!r}.") from e

    @staticmethod
    def _list_files_params(trajectory_id: str) -> dict[str, list[str] | bool]:
        # Note: Backend uses aliases - actor_ids -> actor_id, operations -> operation
        return {
            "actor_id": [trajectory_id],  # List format for Query alias
            "operation": [
                "create"
            ],  # Lowercase: create, update, delete, read, download
            "include_entry_data": True,
        }

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def get_world_model(
        self,
        world_model_id: UUID | None = None,
        name: str | None = None,
        timeout: float | None = None,
    ) -> WorldModelResponse:
        """Get a world model snapshot by its ID or name.

        Args:
            world_model_id: The unique ID of the world model snapshot.
            name: The name of the world model to get the latest version of.
            timeout: Custom timeout in seconds. Uses REQUEST_TIMEOUT if not provided.

        Returns:
            The requested world model snapshot.

        Raises:
            ValueError: If neither or both `world_model_id` and `name` are provided.
            WorldModelFetchError: If the API call fails or the model is not found.
        """
        if not (world_model_id or name) or (world_model_id and name):
            raise ValueError("Provide either 'world_model_id' or 'name', but not both.")

        try:
            identifier = str(world_model_id) if world_model_id else name
            kwargs: dict[str, Any] = {}
            if timeout is not None:
                kwargs["timeout"] = timeout
            response = self.client.get(f"/v0.1/world-models/{identifier}", **kwargs)
            response.raise_for_status()
            return WorldModelResponse.model_validate(response.json())
        except HTTPStatusError as e:
            if e.response.status_code == codes.NOT_FOUND:
                raise WorldModelFetchError(
                    "World model not found with the specified identifier."
                ) from e
            raise WorldModelFetchError(
                f"Error fetching world model: {e.response.status_code} - {e.response.text}."
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise WorldModelFetchError(f"An unexpected error occurred: {e!r}.") from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aget_world_model(
        self,
        world_model_id: UUID | None = None,
        name: str | None = None,
        timeout: float | None = None,
    ) -> WorldModelResponse:
        """Asynchronously get a world model snapshot by its ID or name.

        Args:
            world_model_id: The unique ID of the world model snapshot.
            name: The name of the world model to get the latest version of.
            timeout: Custom timeout in seconds. Uses REQUEST_TIMEOUT if not provided.

        Returns:
            The requested world model snapshot.

        Raises:
            ValueError: If neither or both `world_model_id` and `name` are provided.
            WorldModelFetchError: If the API call fails or the model is not found.
        """
        if not (world_model_id or name) or (world_model_id and name):
            raise ValueError("Provide either 'world_model_id' or 'name', but not both.")

        try:
            identifier = str(world_model_id) if world_model_id else name
            kwargs: dict[str, Any] = {}
            if timeout is not None:
                kwargs["timeout"] = timeout
            response = await self.async_client.get(
                f"/v0.1/world-models/{identifier}", **kwargs
            )
            response.raise_for_status()
            return WorldModelResponse.model_validate(response.json())
        except HTTPStatusError as e:
            if e.response.status_code == codes.NOT_FOUND:
                raise WorldModelFetchError(
                    "World model not found with the specified identifier."
                ) from e
            raise WorldModelFetchError(
                f"Error fetching world model: {e.response.status_code} - {e.response.text}."
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise WorldModelFetchError(f"An unexpected error occurred: {e!r}.") from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
    )
    def list_world_models(
        self,
        name: str | None = None,
        project_id: UUID | str | None = None,
        limit: int = 150,
        offset: int = 0,
        sort_order: str = "asc",
    ) -> list[WorldModelResponse]:
        """List world models with different behavior based on filters.

        When filtering by name: returns only the latest version for that name.
        When filtering by project_id (without name): returns all versions for that project.
        When no filters: returns latest version of each world model.

        Args:
            name: Filter by world model name.
            project_id: Filter by project ID.
            limit: The maximum number of models to return.
            offset: Number of results to skip for pagination.
            sort_order: Sort order 'asc' or 'desc'.

        Returns:
            A list of world model dictionaries.
        """
        try:
            params: dict[str, str | int] = {
                "limit": limit,
                "offset": offset,
                "sort_order": sort_order,
            }
            if name:
                params["name"] = name
            if project_id:
                params["project_id"] = str(project_id)

            response = self.client.get("/v0.1/world-models", params=params)
            response.raise_for_status()
            return response.json()
        except HTTPStatusError as e:
            raise WorldModelFetchError(
                f"Error listing world models: {e.response.status_code} - {e.response.text}"
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise WorldModelFetchError(f"An unexpected error occurred: {e!r}.") from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
    )
    def search_world_models(
        self,
        criteria: list[SearchCriterion] | None = None,
        size: int = 10,
        project_id: UUID | str | None = None,
        search_all_versions: bool = False,
    ) -> list[WorldModelResponse]:
        """Search world models using structured criteria.

        Args:
            criteria: List of SearchCriterion objects with field, operator, and value.
            size: The number of results to return.
            project_id: Optional filter by project ID.
            search_all_versions: Whether to search all versions or just latest.

        Returns:
            A list of world model responses.

        Example:
            from edison_client.models.rest import SearchCriterion, SearchOperator
            criteria = [
                SearchCriterion(field="name", operator=SearchOperator.CONTAINS, value="chemistry"),
                SearchCriterion(field="email", operator=SearchOperator.CONTAINS, value="tyler"),
            ]
            results = client.search_world_models(criteria=criteria, size=20)
        """
        try:
            payload = WorldModelSearchPayload(
                criteria=criteria or [],
                size=size,
                project_id=project_id,
                search_all_versions=search_all_versions,
            )

            response = self.client.post(
                "/v0.1/world-models/search",
                json=payload.model_dump(mode="json"),
            )
            response.raise_for_status()
            return response.json()
        except HTTPStatusError as e:
            raise WorldModelFetchError(
                f"Error searching world models: {e.response.status_code} - {e.response.text}"
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise WorldModelFetchError(f"An unexpected error occurred: {e!r}.") from e

    @staticmethod
    # This is temporary until we migrate fully and merge #1798
    def _parse_world_model_create_response(
        response_data: dict | str,
    ) -> WorldModelCreateResponse:
        """Parse world model create response, handling both new and legacy formats.

        Args:
            response_data: Either a dict with 'id' field (new format) or a UUID string (legacy).

        Returns:
            WorldModelCreateResponse with the world model ID.
        """
        if isinstance(response_data, dict):
            return WorldModelCreateResponse.model_validate(response_data)
        # Legacy format: server returns just the UUID string
        return WorldModelCreateResponse(id=UUID(response_data))

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def create_world_model(self, payload: WorldModel) -> UUID:
        """Create a new, immutable world model snapshot.

        For content_location="data_storage":
        - Stores content and metadata in GCS via presigned URL
        - Updates DSS entry status to active after upload

        Args:
            payload: An instance of WorldModel with the snapshot's data.

        Returns:
            The UUID of the newly created world model.

        Raises:
            WorldModelCreationError: If the API call fails.
        """
        try:
            if payload.content_location == ContentLocation.DATA_STORAGE:
                return self._create_world_model_with_dss(payload)

            response = self.client.post(
                "/v0.1/world-models", json=payload.model_dump(mode="json")
            )
            response.raise_for_status()
            result = self._parse_world_model_create_response(response.json())
        except HTTPStatusError as e:
            if e.response.status_code == codes.BAD_REQUEST:
                raise WorldModelCreationError(
                    f"Invalid payload for world model creation: {e.response.text}."
                ) from e
            raise WorldModelCreationError(
                f"Error creating world model: {e.response.status_code} - {e.response.text}."
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise WorldModelCreationError(
                f"An unexpected error occurred during world model creation: {e!r}."
            ) from e
        return result.id

    def _create_world_model_with_dss(self, payload: WorldModel) -> UUID:
        """Create a world model with content stored in DSS.

        Uploads the content to the presigned URL with a single PUT, which
        works identically on GCS and S3.

        Args:
            payload: The world model payload with content_location="data_storage".

        Returns:
            The UUID of the created world model.
        """
        # Store original content and metadata for GCS upload
        dss_content = {
            "content": payload.content,
            "metadata": payload.model_metadata,
        }

        # Create modified payload without content/metadata for the API call
        api_payload = payload.model_dump(mode="json")
        api_payload["content"] = ""  # API requires content field but we don't need it
        api_payload["model_metadata"] = None

        # Create the world model (returns signed URL for upload)
        response = self.client.post("/v0.1/world-models", json=api_payload)
        response.raise_for_status()
        result = WorldModelCreateResponse.model_validate(response.json())

        if not result.signed_url or not result.data_storage_id:
            raise WorldModelCreationError(
                "Expected signed_url and data_storage_id for DATA_STORAGE content location"
            )

        content_bytes = json.dumps(dss_content).encode("utf-8")
        with Client(timeout=60) as upload_client:
            upload_response = upload_client.put(
                result.signed_url,
                content=content_bytes,
                headers={"Content-Type": "application/json"},
            )
            upload_response.raise_for_status()

        # Update DSS entry status to active
        status_response = self.client.patch(
            f"/v0.1/data-storage/data-entries/{result.data_storage_id}",
            json={"status": "active"},
        )
        status_response.raise_for_status()

        logger.debug(
            f"Created world model {result.id} with DSS content "
            f"({len(content_bytes):,} bytes)"
        )
        return result.id

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def acreate_world_model(self, payload: WorldModel) -> UUID:
        """Asynchronously create a new, immutable world model snapshot.

        For content_location="data_storage":
        - Stores content and metadata in GCS via presigned URL
        - Updates DSS entry status to active after upload

        Args:
            payload: An instance of WorldModel with the snapshot's data.

        Returns:
            The UUID of the newly created world model.

        Raises:
            WorldModelCreationError: If the API call fails.
        """
        try:
            if payload.content_location == ContentLocation.DATA_STORAGE:
                return await self._acreate_world_model_with_dss(payload)

            response = await self.async_client.post(
                "/v0.1/world-models", json=payload.model_dump(mode="json")
            )
            response.raise_for_status()
            result = self._parse_world_model_create_response(response.json())
        except HTTPStatusError as e:
            if e.response.status_code == codes.BAD_REQUEST:
                raise WorldModelCreationError(
                    f"Invalid payload for world model creation: {e.response.text}."
                ) from e
            raise WorldModelCreationError(
                f"Error creating world model: {e.response.status_code} - {e.response.text}."
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise WorldModelCreationError(
                f"An unexpected error occurred during world model creation: {e!r}."
            ) from e
        return result.id

    async def _acreate_world_model_with_dss(self, payload: WorldModel) -> UUID:
        """Asynchronously create a world model with content stored in DSS.

        Uploads the content to the presigned URL with a single PUT, which
        works identically on GCS and S3.

        Args:
            payload: The world model payload with content_location="data_storage".

        Returns:
            The UUID of the created world model.
        """
        # Store original content and metadata for GCS upload
        dss_content = {
            "content": payload.content,
            "metadata": payload.model_metadata,
        }

        # Create modified payload without content/metadata for the API call
        api_payload = payload.model_dump(mode="json")
        api_payload["content"] = ""  # API requires content field but we don't need it
        api_payload["model_metadata"] = None

        # Create the world model (returns signed URL for upload)
        response = await self.async_client.post("/v0.1/world-models", json=api_payload)
        response.raise_for_status()
        result = WorldModelCreateResponse.model_validate(response.json())

        if not result.signed_url or not result.data_storage_id:
            raise WorldModelCreationError(
                "Expected signed_url and data_storage_id for DATA_STORAGE content location"
            )

        content_bytes = json.dumps(dss_content).encode("utf-8")
        async with AsyncClient(timeout=60) as upload_client:
            upload_response = await upload_client.put(
                result.signed_url,
                content=content_bytes,
                headers={"Content-Type": "application/json"},
            )
            upload_response.raise_for_status()

        # Update DSS entry status to active
        status_response = await self.async_client.patch(
            f"/v0.1/data-storage/data-entries/{result.data_storage_id}",
            json={"status": "active"},
        )
        status_response.raise_for_status()

        logger.debug(
            f"Created world model {result.id} with DSS content "
            f"({len(content_bytes):,} bytes)"
        )
        return result.id

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
    )
    async def delete_world_model(self, world_model_id: UUID) -> None:
        """Delete a world model snapshot by its ID.

        Args:
            world_model_id: The unique ID of the world model snapshot to delete.

        Raises:
            WorldModelDeletionError: If the API call fails.
        """
        try:
            response = await self.async_client.delete(
                f"/v0.1/world-models/{world_model_id}"
            )
            response.raise_for_status()
        except HTTPStatusError as e:
            raise WorldModelDeletionError(
                f"Error deleting world model: {e.response.status_code} - {e.response.text}"
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise WorldModelDeletionError(f"An unexpected error occurred: {e}") from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
    )
    def get_project_by_name(
        self,
        name: str,
        limit: int = 2,
        persona_id: UUID | None = None,
    ) -> UUID | list[UUID]:
        """Get a project UUID by name.

        Args:
            name: The name of the project to find
            limit: Maximum number of projects to return
            persona_id: When set, search only workstream projects owned
                by this persona project.

        Returns:
            UUID of the project as a string or a list of UUIDs if multiple projects are found
        """
        try:
            path = (
                f"/v0.1/personas/{persona_id}/projects"
                if persona_id is not None
                else "/v0.1/projects"
            )
            response = self.client.get(
                path,
                params={"limit": limit, "name": name},
            )
            response.raise_for_status()
            projects = response.json()
        except HTTPStatusError as e:
            raise ProjectError(
                f"Error getting project by name: {e.response.status_code} - {e.response.text}"
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise ProjectError(f"Error getting project by name: {e}") from e
        if len(projects) == 0:
            raise ProjectError(f"No project found with name '{name}'")
        if len(projects) > 1:
            logger.warning(
                f"Multiple projects found with name '{name}'. Found {len(projects)} projects."
            )

        ids = [UUID(project["id"]) for project in projects]
        return ids[0] if len(ids) == 1 else ids

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
    )
    async def aget_project_by_name(
        self,
        name: str,
        limit: int = 2,
        persona_id: UUID | None = None,
    ) -> UUID | list[UUID]:
        """Asynchronously get a project UUID by name.

        Args:
            name: The name of the project to find
            limit: Maximum number of projects to return
            persona_id: When set, search only workstream projects owned
                by this persona project.

        Returns:
            UUID of the project as a string or a list of UUIDs if multiple projects are found
        """
        try:
            path = (
                f"/v0.1/personas/{persona_id}/projects"
                if persona_id is not None
                else "/v0.1/projects"
            )
            response = await self.async_client.get(
                path,
                params={"limit": limit, "name": name},
            )
            response.raise_for_status()
            projects = response.json()
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise ProjectError(f"Error getting project by name: {e}") from e
        if len(projects) == 0:
            raise ProjectError(f"No project found with name '{name}'")
        if len(projects) > 1:
            logger.warning(
                f"Multiple projects found with name '{name}'. Found {len(projects)} projects."
            )

        ids = [UUID(project["id"]) for project in projects]
        return ids[0] if len(ids) == 1 else ids

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
    )
    def list_persona_owned_projects(
        self,
        persona_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        name: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> list[dict[str, Any]]:
        """List workstream projects owned by a persona project."""
        try:
            params: dict[str, Any] = {
                "limit": limit,
                "offset": offset,
                "sort_by": sort_by,
                "sort_order": sort_order,
            }
            if name is not None:
                params["name"] = name
            response = self.client.get(
                f"/v0.1/personas/{persona_id}/projects",
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except HTTPStatusError as e:
            raise ProjectError(
                f"Error listing persona projects: {e.response.status_code} - {e.response.text}"
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise
        except Exception as e:
            raise ProjectError(f"Error listing persona projects: {e}") from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
    )
    async def alist_persona_owned_projects(
        self,
        persona_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        name: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> list[dict[str, Any]]:
        """Async variant of ``list_persona_owned_projects``."""
        try:
            params: dict[str, Any] = {
                "limit": limit,
                "offset": offset,
                "sort_by": sort_by,
                "sort_order": sort_order,
            }
            if name is not None:
                params["name"] = name
            response = await self.async_client.get(
                f"/v0.1/personas/{persona_id}/projects",
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except _BASE_CONNECTION_ERRORS:
            raise
        except Exception as e:
            raise ProjectError(f"Error listing persona projects: {e}") from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error_not_idempotent,
        reraise=True,
    )
    def create_project(  # noqa: PLR0917
        self,
        name: str,
        share_status: ShareStatus = ShareStatus.PRIVATE,
        permitted_accessors: PermittedAccessors | None = None,
        metadata: dict | None = None,
        description: str | None = None,
        persona_id: UUID | None = None,
        handoff_message: str | None = None,
        job_name: str | None = None,
    ) -> UUID:
        """Create a new project.

        Args:
            name: The name for the project
            share_status: Share status for the project (private, shared, or public)
            permitted_accessors: Permitted accessors for the project (only valid when share_status is SHARED)
            metadata: Metadata for the project
            description: Description for the project. Ideally 1-2 sentences.
            persona_id: When set, the new project is owned by this
                persona and excluded from the default ``/v0.1/projects``
                listing. The persona must be enabled and owned by the caller.
            handoff_message: Optional context handed off to the new project's
                agent at creation. Requires ``persona_id``.
            job_name: Job for the new project's intro session. Requires
                ``persona_id``. When omitted, the owning persona's job is used.

        Returns:
            UUID of the created project.

        Raises:
            ProjectError: If there's an error creating the project
        """
        if persona_id is None:
            if handoff_message is not None:
                raise ValueError("handoff_message requires persona_id")
            if job_name is not None:
                raise ValueError("job_name requires persona_id")
        try:
            request_metadata = dict(metadata) if metadata else {}
            if description is not None:
                request_metadata["description"] = description

            data: dict[str, Any] = {
                "name": name,
                "share_status": share_status,
                "metadata": request_metadata,
            }
            if permitted_accessors is not None:
                data["permitted_accessors"] = permitted_accessors.model_dump()
            if handoff_message is not None:
                data["handoff_message"] = handoff_message
            if job_name is not None:
                data["job_name"] = job_name
            if persona_id is not None:
                response = self.client.post(
                    f"/v0.1/personas/{persona_id}/projects", json=data
                )
                response.raise_for_status()
                return UUID(response.json()["id"])
            response = self.client.post("/v0.1/projects", json=data)
            response.raise_for_status()
            return UUID(response.json())
        except HTTPStatusError as e:
            raise ProjectError(
                f"Error creating project: {e.response.status_code} - {e.response.text}"
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise ProjectError(f"Error creating project: {e}") from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
    )
    def add_task_to_project(self, project_id: UUID, trajectory_id: str) -> None:
        """Add a task to a project. Use this to assign or reassign a task to a project.

        Args:
            project_id: The UUID of the project
            trajectory_id: The UUID of the task to add

        Raises:
            ProjectError: If there's an error adding the task to the project
        """
        try:
            data = {"trajectory_id": trajectory_id}
            response = self.client.post(
                f"/v0.1/projects/{project_id}/trajectories", json=data
            )
            response.raise_for_status()
        except HTTPStatusError as e:
            if e.response.status_code == codes.NOT_FOUND:
                raise ProjectError(
                    f"Project {project_id} or task {trajectory_id} not found"
                ) from e
            if e.response.status_code == codes.FORBIDDEN:
                raise ProjectError(
                    f"Permission denied to add task to project {project_id}"
                ) from e
            raise ProjectError(
                f"Error adding task to project: {e.response.status_code} - {e.response.text}"
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise ProjectError(f"Error adding trajectory to project: {e}") from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error_not_idempotent,
        reraise=True,
    )
    async def acreate_project(  # noqa: PLR0917
        self,
        name: str,
        share_status: ShareStatus = ShareStatus.PRIVATE,
        permitted_accessors: PermittedAccessors | None = None,
        metadata: dict | None = None,
        description: str | None = None,
        persona_id: UUID | None = None,
        handoff_message: str | None = None,
        job_name: str | None = None,
    ) -> UUID:
        """Async variant of ``create_project``. See it for arg semantics."""
        if persona_id is None:
            if handoff_message is not None:
                raise ValueError("handoff_message requires persona_id")
            if job_name is not None:
                raise ValueError("job_name requires persona_id")
        try:
            request_metadata = dict(metadata) if metadata else {}
            if description is not None:
                request_metadata["description"] = description

            data: dict[str, Any] = {
                "name": name,
                "share_status": share_status,
                "metadata": request_metadata,
            }
            if permitted_accessors is not None:
                data["permitted_accessors"] = permitted_accessors.model_dump()
            if handoff_message is not None:
                data["handoff_message"] = handoff_message
            if job_name is not None:
                data["job_name"] = job_name
            if persona_id is not None:
                response = await self.async_client.post(
                    f"/v0.1/personas/{persona_id}/projects", json=data
                )
                response.raise_for_status()
                return UUID(response.json()["id"])
            response = await self.async_client.post("/v0.1/projects", json=data)
            response.raise_for_status()
            return UUID(response.json())
        except HTTPStatusError as e:
            raise ProjectError(
                f"Error creating project: {e.response.status_code} - {e.response.text}"
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise ProjectError(f"Error creating project: {e}") from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
    )
    async def aadd_task_to_project(self, project_id: UUID, trajectory_id: str) -> None:
        """Asynchronously add a trajectory to a project. Use this to assign or reassign a task to a project.

        Args:
            project_id: The UUID of the project
            trajectory_id: The UUID of the task to add

        Raises:
            ProjectError: If there's an error adding the trajectory to the project
        """
        try:
            data = {"trajectory_id": trajectory_id}
            response = await self.async_client.post(
                f"/v0.1/projects/{project_id}/trajectories", json=data
            )
            response.raise_for_status()
        except HTTPStatusError as e:
            if e.response.status_code == codes.NOT_FOUND:
                raise ProjectError(
                    f"Project {project_id} or trajectory {trajectory_id} not found"
                ) from e
            if e.response.status_code == codes.FORBIDDEN:
                raise ProjectError(
                    f"Permission denied to add trajectory to project {project_id}"
                ) from e
            raise ProjectError(
                f"Error adding trajectory to project: {e.response.status_code} - {e.response.text}"
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise ProjectError(f"Error adding trajectory to project: {e}") from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
    )
    async def aget_project(self, project_id: UUID | str) -> dict[str, Any]:
        """Asynchronously get a project by id.

        Args:
            project_id: The UUID of the project to fetch.

        Returns:
            The project row as a dict (includes ``id``, ``name``, ``metadata``,
            ``owner``, ``share_status``, timestamps, ...).

        Raises:
            ProjectError: If the project does not exist or access is denied.
        """
        try:
            response = await self.async_client.get(f"/v0.1/projects/{project_id}")
            response.raise_for_status()
            return response.json()
        except HTTPStatusError as e:
            if e.response.status_code == codes.NOT_FOUND:
                raise ProjectError(f"Project {project_id} not found") from e
            if e.response.status_code == codes.FORBIDDEN:
                raise ProjectError(
                    f"Permission denied to view project {project_id}"
                ) from e
            raise ProjectError(
                f"Error getting project: {e.response.status_code} - {e.response.text}"
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise ProjectError(f"Error getting project: {e}") from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
    )
    async def aupdate_project(
        self,
        project_id: UUID | str,
        *,
        name: str | None = None,
        metadata: dict | None = None,
    ) -> None:
        """Asynchronously update a project's name and/or metadata.

        Args:
            project_id: The UUID of the project to update.
            name: New display name for the project. None leaves it unchanged.
            metadata: Full replacement metadata dict. None leaves it unchanged.
        """
        try:
            data: dict[str, Any] = {}
            if name is not None:
                data["name"] = name
            if metadata is not None:
                data["metadata"] = metadata
            response = await self.async_client.patch(
                f"/v0.1/projects/{project_id}", json=data
            )
            response.raise_for_status()
        except HTTPStatusError as e:
            if e.response.status_code == codes.NOT_FOUND:
                raise ProjectError(f"Project {project_id} not found") from e
            if e.response.status_code == codes.FORBIDDEN:
                raise ProjectError(
                    f"Permission denied to update project {project_id}"
                ) from e
            raise ProjectError(
                f"Error updating project: {e.response.status_code} - {e.response.text}"
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise ProjectError(f"Error updating project: {e}") from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
    )
    def delete_project(
        self, project_id: UUID, delete_trajectories: bool = True
    ) -> None:
        """Delete a project.

        Args:
            project_id: The UUID of the project to delete
            delete_trajectories: If true, soft-delete all trajectories associated with this project (default: True)

        Raises:
            ProjectError: If there's an error deleting the project
        """
        try:
            params = {"delete_trajectories": delete_trajectories}
            response = self.client.delete(f"/v0.1/projects/{project_id}", params=params)
            response.raise_for_status()
        except HTTPStatusError as e:
            if e.response.status_code == codes.NOT_FOUND:
                raise ProjectError(f"Project {project_id} not found") from e
            if e.response.status_code == codes.FORBIDDEN:
                raise ProjectError(
                    f"Permission denied to delete project {project_id}"
                ) from e
            raise ProjectError(
                f"Error deleting project: {e.response.status_code} - {e.response.text}"
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise ProjectError(f"Error deleting project: {e}") from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
    )
    async def adelete_project(
        self, project_id: UUID, delete_trajectories: bool = True
    ) -> None:
        """Asynchronously delete a project.

        Args:
            project_id: The UUID of the project to delete
            delete_trajectories: If true, soft-delete all trajectories associated with this project (default: True)

        Raises:
            ProjectError: If there's an error deleting the project
        """
        try:
            params = {"delete_trajectories": delete_trajectories}
            response = await self.async_client.delete(
                f"/v0.1/projects/{project_id}", params=params
            )
            response.raise_for_status()
        except HTTPStatusError as e:
            if e.response.status_code == codes.NOT_FOUND:
                raise ProjectError(f"Project {project_id} not found") from e
            if e.response.status_code == codes.FORBIDDEN:
                raise ProjectError(
                    f"Permission denied to delete project {project_id}"
                ) from e
            raise ProjectError(
                f"Error deleting project: {e.response.status_code} - {e.response.text}"
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise ProjectError(f"Error deleting project: {e}") from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
    )
    def delete_trajectory(self, trajectory_id: UUID) -> None:
        """Delete a trajectory (soft delete - marks as hidden).

        Args:
            trajectory_id: The UUID of the trajectory to delete

        Raises:
            TaskFetchError: If there's an error deleting the trajectory
        """
        try:
            response = self.client.delete(f"/v0.1/trajectories/{trajectory_id}")
            response.raise_for_status()
        except HTTPStatusError as e:
            if e.response.status_code == codes.NOT_FOUND:
                raise TaskFetchError(f"Trajectory {trajectory_id} not found") from e
            if e.response.status_code == codes.FORBIDDEN:
                raise TaskFetchError(
                    f"Permission denied to delete trajectory {trajectory_id}"
                ) from e
            raise TaskFetchError(
                f"Error deleting trajectory: {e.response.status_code} - {e.response.text}"
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise TaskFetchError(f"Error deleting trajectory: {e}") from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
    )
    async def adelete_trajectory(self, trajectory_id: UUID) -> None:
        """Asynchronously delete a trajectory (soft delete - marks as hidden).

        Args:
            trajectory_id: The UUID of the trajectory to delete

        Raises:
            TaskFetchError: If there's an error deleting the trajectory
        """
        try:
            response = await self.async_client.delete(
                f"/v0.1/trajectories/{trajectory_id}"
            )
            response.raise_for_status()
        except HTTPStatusError as e:
            if e.response.status_code == codes.NOT_FOUND:
                raise TaskFetchError(f"Trajectory {trajectory_id} not found") from e
            if e.response.status_code == codes.FORBIDDEN:
                raise TaskFetchError(
                    f"Permission denied to delete trajectory {trajectory_id}"
                ) from e
            raise TaskFetchError(
                f"Error deleting trajectory: {e.response.status_code} - {e.response.text}"
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise TaskFetchError(f"Error deleting trajectory: {e}") from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
    )
    async def adelete_sandbox(self, claim_name: str, trajectory_id: str) -> None:
        """Delete a sandbox by claim name.

        Signals crow-service to delete the SandboxClaim from Kubernetes.
        Called by the sandbox itself when a job completes, fails, or is cancelled,
        enabling fire-and-forget job dispatch (the job cleans up its own sandbox).

        Args:
            claim_name: The name of the SandboxClaim to delete
            trajectory_id: The trajectory ID for authorization verification

        Raises:
            SandboxDeleteError: If there's an error deleting the sandbox
        """
        try:
            response = await self.async_client.delete(
                f"/v0.1/sandboxes/{claim_name}",
                params={"trajectory_id": trajectory_id},
            )
            response.raise_for_status()
        except HTTPStatusError as e:
            raise SandboxDeleteError(
                f"Error deleting sandbox {claim_name}: {e.response.status_code} - {e.response.text}"
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise SandboxDeleteError(f"Error deleting sandbox {claim_name}: {e}") from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def get_tasks(
        self,
        query_params: TrajectoryQueryParams | None = None,
        *,
        project_id: UUID | None = None,
        name: str | None = None,
        user: str | None = None,
        limit: int = 50,
        offset: int = 0,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        tags: str | None = None,
    ) -> list[dict[str, Any]]:
        """Fetches trajectories with applied filtering.

        Args:
            query_params: Optional TrajectoryQueryParams model with all parameters
            project_id: Optional project ID to filter trajectories by
            name: Optional name filter for trajectories
            user: Optional user email filter for trajectories
            limit: Maximum number of trajectories to return (default: 50, max: 200)
            offset: Number of trajectories to skip for pagination (default: 0)
            sort_by: Field to sort by, either "created_at" or "name" (default: "created_at")
            sort_order: Sort order, either "asc" or "desc" (default: "desc")
            tags: Optional tag filter for trajectories

        Returns:
            List of trajectory dictionaries

        Raises:
            TaskFetchError: If there's an error fetching trajectories
        """
        try:
            if query_params is not None:
                params = query_params.to_query_params()
            else:
                params_model = TrajectoryQueryParams(
                    project_id=project_id,
                    name=name,
                    user=user,
                    limit=limit,
                    offset=offset,
                    sort_by=sort_by,
                    sort_order=sort_order,
                    tags=tags,
                )
                params = params_model.to_query_params()

            response = self.client.get("/v0.1/trajectories", params=params)
            response.raise_for_status()
            return response.json()
        except HTTPStatusError as e:
            if e.response.status_code in {401, 403}:
                raise PermissionError(
                    "Error getting trajectories: Permission denied"
                ) from e
            raise TaskFetchError(
                f"Error getting trajectories: {e.response.status_code} - {e.response.text}"
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise TaskFetchError(f"Error getting trajectories: {e!r}") from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aget_tasks(
        self,
        query_params: TrajectoryQueryParams | None = None,
        *,
        project_id: UUID | None = None,
        name: str | None = None,
        user: str | None = None,
        limit: int = 50,
        offset: int = 0,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        tags: str | None = None,
    ) -> list[dict[str, Any]]:
        """Asynchronously fetch trajectories with applied filtering.

        Args:
            query_params: Optional TrajectoryQueryParams model with all parameters
            project_id: Optional project ID to filter trajectories by
            name: Optional name filter for trajectories
            user: Optional user email filter for trajectories
            limit: Maximum number of trajectories to return (default: 50, max: 200)
            offset: Number of trajectories to skip for pagination (default: 0)
            sort_by: Field to sort by, either "created_at" or "name" (default: "created_at")
            sort_order: Sort order, either "asc" or "desc" (default: "desc")
            tags: Optional tag filter for trajectories

        Returns:
            List of trajectory dictionaries

        Raises:
            TaskFetchError: If there's an error fetching trajectories
        """
        try:
            if query_params is not None:
                params = query_params.to_query_params()
            else:
                params_model = TrajectoryQueryParams(
                    project_id=project_id,
                    name=name,
                    user=user,
                    limit=limit,
                    offset=offset,
                    sort_by=sort_by,
                    sort_order=sort_order,
                    tags=tags,
                )
                params = params_model.to_query_params()

            response = await self.async_client.get("/v0.1/trajectories", params=params)
            response.raise_for_status()
            return response.json()
        except HTTPStatusError as e:
            if e.response.status_code in {401, 403}:
                raise PermissionError(
                    "Error getting trajectories: Permission denied"
                ) from e
            raise TaskFetchError(
                f"Error getting trajectories: {e.response.status_code} - {e.response.text}"
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise TaskFetchError(f"Error getting trajectories: {e!r}") from e

    def create_discovery(  # noqa: PLR0917
        self,
        project_id: UUID,
        world_model_id: UUID,
        dataset_id: UUID,
        description: str,
        associated_trajectories: list[UUID],
        validation_level: int,
    ) -> UUID:
        """Create a new discovery.

        Args:
            project_id: The ID of the project the discovery is associated with.
            world_model_id: The ID of the world model the discovery is associated with.
            dataset_id: The ID of the dataset the discovery is associated with.
            description: The description of the discovery.
            associated_trajectories: The IDs of the trajectories to associate with the discovery.
            validation_level: The validation level of the discovery.

        Returns:
            The ID of the created discovery.

        Raises:
            DiscoveryCreationError: If there's an error creating the discovery.
        """
        try:
            data = {
                "project_id": str(project_id),
                "world_model_id": str(world_model_id),
                "dataset_id": str(dataset_id),
                "description": description,
                "associated_trajectories": [
                    str(trajectory) for trajectory in associated_trajectories
                ],
                "validation_level": validation_level,
            }
            response = self.client.post("/v0.1/discoveries", json=data)
            response.raise_for_status()
            return UUID(response.json())
        except HTTPStatusError as e:
            raise DiscoveryCreationError(
                f"Error creating discovery: {e.response.status_code} - {e.response.text}"
            ) from e
        except Exception as e:
            raise DiscoveryCreationError(f"Error creating discovery: {e!r}") from e

    def get_discovery(self, discovery_id: UUID) -> DiscoveryResponse:
        """Get a discovery by its ID.

        Args:
            discovery_id: The ID of the discovery to get.

        Returns:
            The discovery.

        Raises:
            DiscoveryFetchError: If there's an error fetching the discovery.
        """
        try:
            response = self.client.get(f"/v0.1/discoveries/{discovery_id}")
            response.raise_for_status()
            return DiscoveryResponse.model_validate(response.json())
        except HTTPStatusError as e:
            raise DiscoveryFetchError(
                f"Error fetching discovery: {e.response.status_code} - {e.response.text}"
            ) from e
        except Exception as e:
            raise DiscoveryFetchError(f"Error fetching discovery: {e!r}") from e

    def list_discoveries_for_project(
        self, project_id: UUID, limit: int = 50, offset: int = 0
    ) -> list[DiscoveryResponse]:
        """List discoveries for a specific project.

        Args:
            project_id: The ID of the project to get discoveries for.
            limit: The maximum number of discoveries to return.
            offset: The number of discoveries to skip.

        Returns:
            A list of discoveries for the specified project.

        Raises:
            DiscoveryFetchError: If there's an error fetching the discoveries.
        """
        try:
            response = self.client.get(
                f"/v0.1/projects/{project_id}/discoveries",
                params={"limit": limit, "offset": offset},
            )
            response.raise_for_status()
            data = response.json()
            return [DiscoveryResponse.model_validate(d) for d in data]
        except HTTPStatusError as e:
            raise DiscoveryFetchError(
                f"Error fetching discoveries for project: {e.response.status_code} - {e.response.text}"
            ) from e
        except Exception as e:
            raise DiscoveryFetchError(
                f"Error fetching discoveries for project: {e!r}"
            ) from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def create_job_event(
        self, request: JobEventCreateRequest
    ) -> JobEventCreateResponse:
        """Create a new job event.

        Args:
            request: Job event creation request

        Returns:
            Job event creation response

        Raises:
            JobEventCreationError: If the API call fails
        """
        try:
            response = self.client.post(
                "/v0.1/job-events",
                json=request.model_dump(exclude_none=True, mode="json"),
            )
            response.raise_for_status()
            return JobEventCreateResponse(**response.json())
        except HTTPStatusError as e:
            if e.response.status_code == codes.BAD_REQUEST:
                raise JobEventCreationError(
                    f"Invalid job event creation request: {e.response.text}."
                ) from e
            if e.response.status_code == codes.NOT_FOUND:
                raise JobEventCreationError(
                    f"Execution not found for job event creation: {e.response.text}."
                ) from e
            raise JobEventCreationError(
                f"Error creating job event: {e.response.status_code} - {e.response.text}."
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise JobEventCreationError(
                f"An unexpected error occurred during job event creation: {e!r}."
            ) from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def acreate_job_event(
        self, request: JobEventCreateRequest
    ) -> JobEventCreateResponse:
        """Asynchronously create a new job event.

        Args:
            request: Job event creation request

        Returns:
            Job event creation response

        Raises:
            JobEventCreationError: If the API call fails
        """
        try:
            response = await self.async_client.post(
                "/v0.1/job-events",
                json=request.model_dump(exclude_none=True, mode="json"),
            )
            response.raise_for_status()
            return JobEventCreateResponse(**response.json())
        except HTTPStatusError as e:
            if e.response.status_code == codes.BAD_REQUEST:
                raise JobEventCreationError(
                    f"Invalid job event creation request: {e.response.text}."
                ) from e
            if e.response.status_code == codes.NOT_FOUND:
                raise JobEventCreationError(
                    f"Execution not found for job event creation: {e.response.text}."
                ) from e
            raise JobEventCreationError(
                f"Error creating job event: {e.response.status_code} - {e.response.text}."
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise JobEventCreationError(
                f"An unexpected error occurred during job event creation: {e!r}."
            ) from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def update_job_event(
        self, job_event_id: UUID, request: JobEventUpdateRequest
    ) -> None:
        """Update an existing job event.

        Args:
            job_event_id: ID of the job event to update
            request: Job event update request

        Raises:
            JobEventUpdateError: If the API call fails
        """
        try:
            response = self.client.patch(
                f"/v0.1/job-events/{job_event_id}",
                json=request.model_dump(exclude_none=True, mode="json"),
            )
            response.raise_for_status()
        except HTTPStatusError as e:
            if e.response.status_code == codes.NOT_FOUND:
                raise JobEventUpdateError(
                    f"Job event with ID {job_event_id} not found."
                ) from e
            if e.response.status_code == codes.BAD_REQUEST:
                raise JobEventUpdateError(
                    f"Invalid job event update request: {e.response.text}."
                ) from e
            raise JobEventUpdateError(
                f"Error updating job event: {e.response.status_code} - {e.response.text}."
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise JobEventUpdateError(
                f"An unexpected error occurred during job event update: {e!r}."
            ) from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aupdate_job_event(
        self, job_event_id: UUID, request: JobEventUpdateRequest
    ) -> None:
        """Asynchronously update an existing job event.

        Args:
            job_event_id: ID of the job event to update
            request: Job event update request

        Raises:
            JobEventUpdateError: If the API call fails
        """
        try:
            response = await self.async_client.patch(
                f"/v0.1/job-events/{job_event_id}",
                json=request.model_dump(exclude_none=True, mode="json"),
            )
            response.raise_for_status()
        except HTTPStatusError as e:
            if e.response.status_code == codes.NOT_FOUND:
                raise JobEventUpdateError(
                    f"Job event with ID {job_event_id} not found."
                ) from e
            if e.response.status_code == codes.BAD_REQUEST:
                raise JobEventUpdateError(
                    f"Invalid job event update request: {e.response.text}."
                ) from e
            raise JobEventUpdateError(
                f"Error updating job event: {e.response.status_code} - {e.response.text}."
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise JobEventUpdateError(
                f"An unexpected error occurred during job event update: {e!r}."
            ) from e

    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=30),
        stop=stop_after_attempt(3),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def acreate_job_events_batch(
        self, request: JobEventBatchCreateRequest
    ) -> JobEventBatchCreateResponse:
        """Asynchronously create multiple job events in a single batch operation.

        Args:
            request: Batch job event creation request

        Returns:
            Job event batch creation response

        Raises:
            JobEventBatchCreationError: If the API call fails
        """
        try:
            response = await self.async_client.post(
                "/v0.1/job-events/batch",
                json=request.model_dump(exclude_none=True, mode="json"),
            )
            response.raise_for_status()
            return JobEventBatchCreateResponse(**response.json())
        except HTTPStatusError as e:
            if e.response.status_code == codes.BAD_REQUEST:
                raise JobEventBatchCreationError(
                    f"Invalid batch job event creation request: {e.response.text}."
                ) from e
            if e.response.status_code == codes.NOT_FOUND:
                raise JobEventBatchCreationError(
                    f"Execution not found for batch job event creation: {e.response.text}."
                ) from e
            raise JobEventBatchCreationError(
                f"Error creating batch job events: {e.response.status_code} - {e.response.text}."
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise  # Let tenacity handle retries for transient errors
        except Exception as e:
            raise JobEventBatchCreationError(
                f"An unexpected error occurred during batch job event creation: {e!r}."
            ) from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def get_job_event_usage(
        self, execution_id: UUID, execution_type: ExecutionType
    ) -> JobEventUsageResponse:
        """Read LLM token counts and USD cost for one trajectory or session."""
        return self._parse_job_event_usage(
            self.client.get(
                "/v0.1/job-events/usage",
                params={
                    "execution_id": str(execution_id),
                    "execution_type": execution_type.value,
                },
            )
        )

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aget_job_event_usage(
        self, execution_id: UUID, execution_type: ExecutionType
    ) -> JobEventUsageResponse:
        """Read LLM token counts and USD cost for one trajectory or session."""
        return self._parse_job_event_usage(
            await self.async_client.get(
                "/v0.1/job-events/usage",
                params={
                    "execution_id": str(execution_id),
                    "execution_type": execution_type.value,
                },
            )
        )

    @staticmethod
    def _parse_job_event_usage(response: Response) -> JobEventUsageResponse:
        try:
            response.raise_for_status()
            return JobEventUsageResponse.model_validate(response.json())
        except HTTPStatusError as e:
            raise JobEventFetchError(
                "Error reading job event usage: "
                f"{e.response.status_code} - {e.response.text}."
            ) from e
        except _BASE_CONNECTION_ERRORS:
            raise
        except Exception as e:
            raise JobEventFetchError(
                f"An unexpected error occurred reading job event usage: {e!r}."
            ) from e


def get_installed_packages() -> dict[str, str]:
    """Returns a dictionary of installed packages and their versions."""
    return {
        dist.metadata["Name"].lower(): dist.version
        for dist in importlib.metadata.distributions()
    }


def get_global_imports(global_scope: dict) -> dict[str, str]:
    """Retrieve global imports from the global scope, mapping aliases to full module names."""
    return {
        name: obj.__name__
        for name, obj in global_scope.items()
        if isinstance(obj, ModuleType)
    }


def get_referenced_globals_from_source(source_code: str) -> set[str]:
    """Extract globally referenced symbols from the source code."""
    parsed = ast.parse(source_code)
    return {
        node.id
        for node in ast.walk(parsed)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }


def get_used_global_imports(
    func,
    global_imports: dict[str, str],
    global_scope: dict,
    visited=None,
) -> set[str]:
    """Retrieve global imports used by a function."""
    if visited is None:
        visited = set()
    if func in visited:
        return set()
    visited.add(func)
    used_imports: set[str] = set()
    source_code = inspect.getsource(func)
    referenced_globals = get_referenced_globals_from_source(source_code)
    used_imports.update(
        global_imports[name] for name in referenced_globals if name in global_imports
    )
    parsed = ast.parse(source_code)
    for node in ast.walk(parsed):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            ref_func = global_scope.get(node.func.id)
            if callable(ref_func):
                used_imports.update(
                    get_used_global_imports(
                        ref_func,
                        global_imports,
                        global_scope,
                        visited,
                    ),
                )
    return used_imports


def get_used_modules(env_builder: EnvironmentBuilder, global_scope: dict) -> set[str]:
    """Retrieve globally imported modules referenced by the start_fn and tools."""
    if not isinstance(env_builder, EnvironmentBuilder):
        raise TypeError("The provided object is not an instance of EnvironmentBuilder.")
    global_imports = get_global_imports(global_scope)
    used_imports = get_used_global_imports(
        env_builder.start_fn,
        global_imports,
        global_scope,
    )
    for tool in env_builder.tools:
        used_imports.update(
            get_used_global_imports(tool._tool_fn, global_imports, global_scope),
        )
    return used_imports


def generate_requirements(
    env_builder: EnvironmentBuilder,
    global_scope: dict,
) -> list[str]:
    """Generates a list of modules to install based on loaded modules."""
    used_modules = get_used_modules(env_builder, global_scope)
    used_modules.add("cloudpickle")
    installed_packages = get_installed_packages()
    pip_modules = {module for module in used_modules if module in installed_packages}
    return [f"{module}=={installed_packages[module]}" for module in sorted(pip_modules)]
