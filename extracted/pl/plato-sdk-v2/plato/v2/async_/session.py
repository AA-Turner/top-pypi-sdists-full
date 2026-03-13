"""Plato SDK v2 - Asynchronous Session Actor.

The Session class wraps a SessionSpec (from backend) with execution capabilities.
It acts like a Ray actor - the spec holds state, the class provides methods.
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import httpx
import tenacity
from pydantic import BaseModel

if TYPE_CHECKING:
    from playwright.async_api import Browser, BrowserContext, Page

from plato._generated.api.v2.jobs import get_flows as jobs_get_flows
from plato._generated.api.v2.jobs import public_url as jobs_public_url
from plato._generated.api.v2.jobs import wait_for_ready as jobs_wait_for_ready
from plato._generated.api.v2.sessions import add_job as sessions_add_job
from plato._generated.api.v2.sessions import add_ssh_key as sessions_add_ssh_key
from plato._generated.api.v2.sessions import close as sessions_close
from plato._generated.api.v2.sessions import connect_network as sessions_connect_network
from plato._generated.api.v2.sessions import disk_snapshot as sessions_disk_snapshot
from plato._generated.api.v2.sessions import evaluate as sessions_evaluate
from plato._generated.api.v2.sessions import execute as sessions_execute
from plato._generated.api.v2.sessions import get_public_url as sessions_get_public_url
from plato._generated.api.v2.sessions import heartbeat as sessions_heartbeat
from plato._generated.api.v2.sessions import make as sessions_make
from plato._generated.api.v2.sessions import remove_job as sessions_remove_job
from plato._generated.api.v2.sessions import reset as sessions_reset
from plato._generated.api.v2.sessions import set_date as sessions_set_date
from plato._generated.api.v2.sessions import setup_sandbox as sessions_setup_sandbox
from plato._generated.api.v2.sessions import snapshot as sessions_snapshot
from plato._generated.api.v2.sessions import snapshot_store as sessions_snapshot_store
from plato._generated.api.v2.sessions import state as sessions_state
from plato._generated.api.v2.sessions import wait_for_ready as sessions_wait_for_ready
from plato._generated.models import (
    AddJobRequest,
    AddSSHKeyRequest,
    AddSSHKeyResponse,
    AppApiV2SchemasSessionCreateSnapshotRequest,
    AppApiV2SchemasSessionCreateSnapshotResponse,
    AppApiV2SchemasSessionEvaluateRequest,
    AppApiV2SchemasSessionEvaluateResponse,
    AppApiV2SchemasSessionHeartbeatResponse,
    AppApiV2SchemasSessionSetupSandboxRequest,
    AppApiV2SchemasSessionSetupSandboxResponse,
    CreateDiskSnapshotRequest,
    CreateDiskSnapshotResponse,
    CreateSessionFromEnvs,
    CreateSessionFromTestCase,
    EnvironmentContext,
    Envs,
    ExecuteCommandRequest,
    ExecuteCommandResponse,
    Flow,
    HeartbeatTimeout,
    RemoveJobRequest,
    ResetSessionRequest,
    ResetSessionResponse,
    RunSessionSource,
    SessionContext,
    SessionStateResponse,
    SetDateRequest,
    SetDateResponse,
    WaitForReadyResponse,
)
from plato.v2.async_.environment import Environment
from plato.v2.async_.flow_executor import FlowExecutor
from plato.v2.types import EnvFromArtifact, EnvFromResource, EnvFromSimulator
from plato.v2.utils.models import (
    EnvironmentInfo,
    SessionCleanupResult,
)

logger = logging.getLogger(__name__)


@dataclass
class LoginResult:
    """Result of login operation containing browser context and pages.

    Requires playwright to be installed.
    """

    context: BrowserContext
    pages: dict[str, Page]


class SerializedEnv(BaseModel):
    """Serialized environment context."""

    job_id: str
    alias: str
    artifact_id: str | None = None
    simulator: str | None = None


class SerializedSession(BaseModel):
    """Serialized session state for persistence and restoration."""

    session_id: str
    task_public_id: str | None = None
    envs: list[SerializedEnv]
    api_key: str
    base_url: str | None = None
    closed: bool = False


class Session:
    """Actor wrapper for SessionSpec - provides async execution methods.

    The Session wraps a SessionSpec (which contains the runtime state) and adds
    methods to execute operations on the session. This is similar to a Ray actor
    pattern where the spec is the state and the class provides the interface.

    Usage:
        from plato.v2 import AsyncPlato, Env

        plato = AsyncPlato()
        session = await plato.from_envs(envs=[Env.simulator("espocrm")])

        # Operations execute against the backend
        await session.reset()
        state = await session.get_state()
        result = await session.execute("ls -la")

        await session.close()
        await plato.close()
    """

    def __init__(
        self,
        http_client: httpx.AsyncClient,
        api_key: str,
        context: SessionContext,
    ):
        """Initialize session actor.

        Args:
            http_client: Async HTTP client for API calls.
            api_key: API key for authentication.
            context: SessionContext from backend with session_id, envs, and task_public_id.
        """

        self._http = http_client
        self._api_key = api_key
        self._context = context
        self._closed = False
        self._started = False
        self._heartbeat_task: asyncio.Task | None = None
        self._heartbeat_interval = 30
        self._envs: list[Environment] | None = None

    @property
    def session_id(self) -> str:
        """Get the session ID."""
        return self._context.session_id

    @property
    def task_public_id(self) -> str | None:
        """Get the task public ID if session was created from a task."""
        return self._context.task_public_id

    @classmethod
    async def _make_session(
        cls,
        http_client: httpx.AsyncClient,
        api_key: str,
        request_body,
        timeout: int,
        *,
        wait: bool = True,
    ) -> Session:
        """Shared session creation: POST /make, check failures, wait for ready, start heartbeat.

        All creation paths (from_envs, from_testcase, from_artifacts) funnel through here.

        Args:
            wait: If False, return immediately after creation without waiting for ready.
                  The caller must ``await session.wait_until_ready()`` before using envs.
        """
        response = await sessions_make.asyncio(
            client=http_client,
            body=request_body,
            x_api_key=api_key,
        )

        failures = [e for e in response.envs if not e.success]
        if failures:
            try:
                await sessions_close.asyncio(
                    client=http_client,
                    session_id=response.session_id,
                    x_api_key=api_key,
                )
            except Exception as close_err:
                logger.warning(f"Failed to close session after env creation failure: {close_err}")

            failure_details = ", ".join([f"{e.alias}: {e.error}" for e in failures])
            raise RuntimeError(f"Failed to create environments: {failure_details}")

        logger.info(f"Session created: {response.session_id}, envs: {[e.alias for e in response.envs]}")

        if not wait:
            context = SessionContext(
                session_id=response.session_id,
                envs=[EnvironmentContext(job_id="", alias=e.alias or "") for e in response.envs if e.success],
            )
            return cls(http_client=http_client, api_key=api_key, context=context)

        try:
            ready_response = await sessions_wait_for_ready.asyncio(
                client=http_client,
                session_id=response.session_id,
                timeout=int(timeout),
                x_api_key=api_key,
            )
            logger.info(f"wait_for_ready returned ready={ready_response.ready}")
            context = cls._check_ready_response(ready_response, timeout)
        except (TimeoutError, RuntimeError):
            try:
                await sessions_close.asyncio(
                    client=http_client,
                    session_id=response.session_id,
                    x_api_key=api_key,
                )
            except Exception as close_err:
                logger.warning(f"Failed to close session after ready timeout: {close_err}")
            raise

        logger.info(f"All environments in session {response.session_id} are ready")
        session = cls(
            http_client=http_client,
            api_key=api_key,
            context=context,
        )
        session._started = True
        await session.start_heartbeat()
        return session

    @classmethod
    async def from_envs(
        cls,
        http_client: httpx.AsyncClient,
        api_key: str,
        envs: list[EnvFromSimulator | EnvFromArtifact | EnvFromResource],
        *,
        timeout: int = 1800,
        agent_artifact_id: str | None = None,
        wait: bool = True,
    ) -> Session:
        """Create a new session from environment configurations.

        Does NOT automatically reset -- call ``await session.reset()`` when ready.

        Args:
            http_client: The httpx async client.
            api_key: API key for authentication.
            envs: List of environment configurations (from Env.simulator() or Env.artifact()).
            timeout: VM timeout in seconds (default: 1800).
            agent_artifact_id: Optional agent artifact ID to associate with the session.
            wait: If True (default), wait for all environments to be ready before
                returning. If False, return immediately after session creation — the
                caller must call ``await session.wait_until_ready()`` before using
                environments.

        Returns:
            A new Session instance. When ``wait=False`` the environments may not be
            ready yet.

        Raises:
            RuntimeError: If any environment fails to create or become ready.
            TimeoutError: If environments don't become ready within timeout.
            ValueError: If duplicate aliases are provided.
        """
        seen_aliases: set[str] = set()
        for env in envs:
            if env.alias is not None:
                if env.alias in seen_aliases:
                    raise ValueError(f"Duplicate alias provided: '{env.alias}'")
                seen_aliases.add(env.alias)

        for env in envs:
            if env.alias is None:
                unique_alias = f"env-{uuid.uuid4().hex[:8]}"
                while unique_alias in seen_aliases:
                    unique_alias = f"env-{uuid.uuid4().hex[:8]}"
                env.alias = unique_alias
                seen_aliases.add(unique_alias)

        request_body = CreateSessionFromEnvs(
            envs=[Envs(root=env) for env in envs],
            timeout=timeout,
            source=RunSessionSource.SDK,
            agent_artifact_id=agent_artifact_id,
        )
        return await cls._make_session(http_client, api_key, request_body, timeout, wait=wait)

    @classmethod
    async def from_testcase(
        cls,
        http_client: httpx.AsyncClient,
        api_key: str,
        testcase_id: str,
        *,
        timeout: int = 1800,
    ) -> Session:
        """Create a new session from a test case.

        Derives environments from the test case's artifacts, waits for all
        VMs to be ready, and automatically resets them to set up mutation
        logging. The returned session is fully ready for agent interaction.

        Args:
            http_client: The httpx async client.
            api_key: API key for authentication.
            testcase_id: Test case public ID.
            timeout: VM timeout in seconds (default: 1800).

        Returns:
            A new Session with all environments ready and reset.

        Raises:
            RuntimeError: If any environment fails to create or become ready.
            TimeoutError: If environments don't become ready within timeout.
        """
        request_body = CreateSessionFromTestCase(
            testcase_id=testcase_id,
            timeout=timeout,
            source=RunSessionSource.SDK,
        )
        session = await cls._make_session(http_client, api_key, request_body, timeout)

        await sessions_reset.asyncio(
            client=http_client,
            session_id=session.session_id,
            body=ResetSessionRequest(),
            x_api_key=api_key,
        )
        logger.info(f"Session {session.session_id} reset for mutation capture")
        return session

    @classmethod
    async def from_artifacts(
        cls,
        http_client: httpx.AsyncClient,
        api_key: str,
        artifact_ids: list[str],
        *,
        timeout: int = 1800,
    ) -> Session:
        """Create a new session from artifact IDs.

        Convenience method that wraps each artifact ID into an EnvFromArtifact
        and delegates to from_envs(). Does NOT automatically reset -- call
        ``await session.reset()`` when ready to begin mutation logging.

        Args:
            http_client: The httpx async client.
            api_key: API key for authentication.
            artifact_ids: List of simulator artifact public IDs.
            timeout: VM timeout in seconds (default: 1800).

        Returns:
            A new Session with all environments ready (not reset).

        Raises:
            RuntimeError: If any environment fails to create or become ready.
            TimeoutError: If environments don't become ready within timeout.
        """
        envs = [EnvFromArtifact(artifact_id=aid) for aid in artifact_ids]
        return await cls.from_envs(http_client, api_key, envs, timeout=timeout)

    @staticmethod
    def _check_ready_response(response: WaitForReadyResponse, timeout: float) -> SessionContext:
        """Check the wait_for_ready response and return the SessionContext.

        Args:
            response: WaitForReadyResponse from the API.
            timeout: Timeout value for error messages.

        Returns:
            SessionContext with environment details.

        Raises:
            TimeoutError: If environments didn't become ready.
            RuntimeError: If any environment failed or context is missing.
        """
        if not response.ready:
            errors = []
            if response.results:
                for job_id, result in response.results.items():
                    if not result.ready:
                        error = result.error or "Unknown error"
                        errors.append(f"{job_id}: {error}")

            if errors:
                raise RuntimeError(f"Environments failed to become ready: {', '.join(errors)}")
            else:
                raise TimeoutError(f"Environments did not become ready within {timeout} seconds")

        if not response.context:
            raise RuntimeError("Backend did not return session context")

        return response.context

    async def wait_until_ready(
        self,
        timeout: float = 300.0,
        poll_interval: float = 2.0,
    ) -> None:
        """Wait until all environments are ready (RUNNING status).

        Polls the backend wait_for_ready API until all environments are ready.

        Args:
            timeout: Maximum time to wait in seconds (default: 300).
            poll_interval: Time between polls in seconds (default: 2.0).

        Raises:
            TimeoutError: If environments don't become ready within timeout.
            RuntimeError: If any environment fails or is cancelled.
        """
        self._check_closed()

        class NotReadyError(Exception):
            pass

        @tenacity.retry(
            stop=tenacity.stop_after_delay(timeout),
            wait=tenacity.wait_fixed(poll_interval),
            retry=tenacity.retry_if_exception_type(NotReadyError),
            reraise=True,
        )
        async def _poll_ready():
            response = await sessions_wait_for_ready.asyncio(
                client=self._http,
                session_id=self.session_id,
                timeout=int(poll_interval * 2),
                x_api_key=self._api_key,
            )

            # Check for fatal errors
            if response.results:
                for job_id, result in response.results.items():
                    if result.error and "failed" in result.error.lower():
                        raise RuntimeError(f"Environment {job_id} failed: {result.error}")

            if response.ready and response.context:
                self._context = response.context
                self._envs = None  # Reset cached envs
                logger.info(f"All environments in session {self.session_id} are ready")
                return

            raise NotReadyError("Environments not ready yet")

        try:
            await _poll_ready()
        except NotReadyError:
            raise TimeoutError(f"Environments did not become ready within {timeout} seconds")

    async def wait(
        self,
        timeout: float = 7200.0,
        connect_network: bool = True,
    ) -> None:
        """Complete deferred session setup after ``create(wait=False)``.

        Waits for all environments to be ready, starts the heartbeat, and
        optionally connects the WireGuard network. This is the counterpart to
        ``create(wait=False)`` — call it once before using the session.

        If the session was already fully started (created with ``wait=True``),
        this is a no-op.

        Args:
            timeout: Maximum time to wait for environments in seconds (default: 7200).
            connect_network: If True (default), connect VMs to WireGuard network.

        Raises:
            TimeoutError: If environments don't become ready within timeout.
            RuntimeError: If any environment fails.
        """
        if self._started:
            return

        await self.wait_until_ready(timeout=timeout)
        await self.start_heartbeat()
        if connect_network:
            await self.connect_network()
        self._started = True

    @property
    def envs(self) -> list[Environment]:
        """Get all environments in this session.

        Returns:
            List of Environment actor objects.
        """
        if self._envs is None:
            env_contexts = self._context.envs or []
            self._envs = [
                Environment(
                    session=self,
                    job_id=ctx.job_id,
                    alias=ctx.alias,
                    artifact_id=ctx.artifact_id,
                    simulator=ctx.simulator,
                    status="running",  # Environments are running after from_envs completes
                )
                for ctx in env_contexts
            ]
        return self._envs

    def get_env(self, alias: str) -> Environment | None:
        """Get an environment by alias.

        Args:
            alias: The environment alias.

        Returns:
            The Environment actor or None if not found.
        """
        for env in self.envs:
            if env.alias == alias:
                return env
        return None

    async def reset(self, **kwargs) -> ResetSessionResponse:
        """Reset all environments in the session to initial state.

        Returns:
            ResetSessionResponse with results per job_id.
        """
        self._check_closed()

        request = ResetSessionRequest(**kwargs)
        return await sessions_reset.asyncio(
            client=self._http,
            session_id=self.session_id,
            body=request,
            x_api_key=self._api_key,
        )

    async def get_state(self) -> SessionStateResponse:
        """Get state from all environments in the session.

        Returns:
            SessionStateResponse with state per job_id.
        """
        self._check_closed()

        return await sessions_state.asyncio(
            client=self._http,
            session_id=self.session_id,
            x_api_key=self._api_key,
        )

    async def execute(
        self,
        command: str,
        timeout: int = 30,
    ) -> ExecuteCommandResponse:
        """Execute a command on all environments in the session.

        Args:
            command: Shell command to execute.
            timeout: Command timeout in seconds.

        Returns:
            ExecuteCommandResponse with execution results per job_id.
        """
        self._check_closed()

        request = ExecuteCommandRequest(
            command=command,
            timeout=timeout,
        )
        return await sessions_execute.asyncio(
            client=self._http,
            session_id=self.session_id,
            body=request,
            x_api_key=self._api_key,
        )

    async def set_date(
        self,
        dt: datetime,
        timeout: int = 30,
    ) -> SetDateResponse:
        """Set the system date on all environments in the session.

        Args:
            dt: The datetime to set.
            timeout: Command timeout in seconds.

        Returns:
            SetDateResponse with results per job_id.
        """
        self._check_closed()

        request = SetDateRequest(
            datetime=dt.isoformat(),
            timeout=timeout,
        )
        return await sessions_set_date.asyncio(
            client=self._http,
            session_id=self.session_id,
            body=request,
            x_api_key=self._api_key,
        )

    async def setup_sandbox(
        self,
        timeout: int = 120,
    ) -> AppApiV2SchemasSessionSetupSandboxResponse:
        """Setup sandbox environment with Docker overlay on all environments.

        This configures the VMs for Docker usage with overlay2 storage driver,
        which is significantly faster than the default vfs driver. Should be called
        after session creation and before pulling Docker images.

        The setup includes:
        - Mounting /dev/vdb to /mnt/docker for Docker storage
        - Configuring Docker with overlay2 storage driver
        - Setting up ECR and Docker Hub authentication
        - Creating a docker-user service for non-root Docker access

        Args:
            timeout: Setup timeout in seconds (default: 120).

        Returns:
            SetupSandboxResponse with results per job_id.
        """
        self._check_closed()

        request = AppApiV2SchemasSessionSetupSandboxRequest(timeout=timeout)
        return await sessions_setup_sandbox.asyncio(
            client=self._http,
            session_id=self.session_id,
            body=request,
            x_api_key=self._api_key,
        )

    async def evaluate(self, value: dict | None = None) -> AppApiV2SchemasSessionEvaluateResponse:
        """Evaluate the session against its linked test case scoring config.

        For mutation-only scoring, call with no arguments. For output scoring,
        pass the agent's output as ``value``.

        Args:
            value: Optional output data for OUTPUT scoring. Not needed for
                   mutation-only test cases.

        Returns:
            Evaluation results including score and per-SIM results.
        """
        self._check_closed()

        # Flush cached mutations from simulator VMs so they are
        # in the DB before the evaluate endpoint reads them.
        await self.get_state()

        body = AppApiV2SchemasSessionEvaluateRequest(value=value)
        return await sessions_evaluate.asyncio(
            client=self._http,
            session_id=self.session_id,
            body=body,
            x_api_key=self._api_key,
        )

    async def snapshot(self) -> AppApiV2SchemasSessionCreateSnapshotResponse:
        """Create a snapshot of all environments in the session.

        Returns:
            Snapshot response with info per job_id.
        """
        self._check_closed()

        return await sessions_snapshot.asyncio(
            client=self._http,
            session_id=self.session_id,
            body=AppApiV2SchemasSessionCreateSnapshotRequest(),
            x_api_key=self._api_key,
        )

    async def snapshot_store(
        self,
        override_service: str | None = None,
        override_version: str | None = None,
        override_dataset: str | None = None,
    ) -> AppApiV2SchemasSessionCreateSnapshotResponse:
        """Create a snapshot-store snapshot of all environments in the session.

        Uses the snapshot-store pipeline for chunk-based deduplication and
        efficient storage. This is the preferred method for new base snapshots.

        Args:
            override_service: Override simulator/service name in artifact metadata.
            override_version: Override version/git_hash in artifact metadata.
            override_dataset: Override dataset name in artifact metadata.

        Returns:
            Snapshot response with info per job_id.
        """
        self._check_closed()

        return await sessions_snapshot_store.asyncio(
            client=self._http,
            session_id=self.session_id,
            body=AppApiV2SchemasSessionCreateSnapshotRequest(
                override_service=override_service,
                override_version=override_version,
                override_dataset=override_dataset,
            ),
            x_api_key=self._api_key,
        )

    async def disk_snapshot(
        self,
        override_service: str | None = None,
        override_version: str | None = None,
        override_dataset: str | None = None,
    ) -> CreateDiskSnapshotResponse:
        """Create a disk-only snapshot of all environments in the session.

        Disk snapshots capture only the disk state (no memory). On resume, the VM
        will do a fresh boot with the preserved disk state. This is faster to
        create and smaller to store than full snapshots.

        Uses snapshot-store backend for chunk-based deduplication and efficient storage.

        Args:
            override_service: Override simulator/service name in artifact metadata.
            override_version: Override version/git_hash in artifact metadata.
            override_dataset: Override dataset name in artifact metadata.

        Returns:
            CreateDiskSnapshotResponse with artifact_id per job_id.
        """
        self._check_closed()

        return await sessions_disk_snapshot.asyncio(
            client=self._http,
            session_id=self.session_id,
            body=CreateDiskSnapshotRequest(
                override_service=override_service,
                override_version=override_version,
                override_dataset=override_dataset,
            ),
            x_api_key=self._api_key,
        )

    async def get_public_url(self, port: int | None = None) -> dict[str, str]:
        """Get public URLs for all environments in the session.

        Returns browser-accessible URLs in format: {job_id}--{port}.sims.plato.so

        Args:
            port: Port number for the URLs. If not specified, uses the default port.

        Returns:
            Dict mapping alias to public URL.
        """
        self._check_closed()

        response = await sessions_get_public_url.asyncio(
            client=self._http,
            session_id=self.session_id,
            port=port,
            x_api_key=self._api_key,
        )

        # Map job_id to alias for easier access
        urls = {}
        if response and response.results:
            for job_id, result in response.results.items():
                alias = next((env.alias for env in self.envs if env.job_id == job_id), job_id)
                url = result.url if hasattr(result, "url") else str(result)
                urls[alias] = url

        return urls

    async def get_connect_url(self, port: int | None = None) -> dict[str, str]:
        """Get connect URLs for all environments in the session.

        Returns direct connect URLs in format: https://{job_id}--{port}.connect.plato.so
        or https://{job_id}.connect.plato.so if port is None.

        Args:
            port: Port number for the URLs (optional). If None, returns URL without port.

        Returns:
            Dict mapping alias to connect URL.
        """
        self._check_closed()

        from plato._generated.api.v2.sessions import get_connect_url as sessions_get_connect_url

        response = await sessions_get_connect_url.asyncio(
            client=self._http,
            session_id=self.session_id,
            port=port,
            x_api_key=self._api_key,
        )

        # Map job_id to alias for easier access
        urls = {}
        if response and response.results:
            for job_id, result in response.results.items():
                alias = next((env.alias for env in self.envs if env.job_id == job_id), job_id)
                url = result.url if hasattr(result, "url") else str(result)
                urls[alias] = url

        return urls

    async def connect_network(self) -> dict:
        """Connect all VMs in this session to a WireGuard network.

        Creates a full mesh WireGuard network between all VMs in the session.
        Must be called after all environments are ready. This method is idempotent -
        calling it multiple times will not reconnect already-connected VMs.

        Returns:
            Dict with:
                - success: bool - True if all VMs connected successfully
                - session_id: str - The session ID
                - subnet: str - The network subnet (e.g., "10.100.0.0/24")
                - results: dict[str, bool] - Success status per job_id

        Raises:
            RuntimeError: If session is closed or network connection fails.
        """
        self._check_closed()

        # Server returns 500 with error detail if network connection fails
        result = await sessions_connect_network.asyncio(
            client=self._http,
            session_id=self.session_id,
            x_api_key=self._api_key,
        )

        return result

    async def add_env(
        self,
        env: EnvFromSimulator | EnvFromArtifact | EnvFromResource,
        *,
        timeout: int = 1800,
        heartbeat_timeout: int | None = None,
        wait_for_ready: bool = True,
    ) -> Environment:
        """Add a new environment to this session.

        The new environment will:
        1. Become part of the session's job group
        2. Be matched to an available VM via the resource matcher
        3. Automatically join the session's WireGuard network if one exists

        Args:
            env: Environment configuration (from Env.simulator(), Env.artifact(), or Env.resource()).
            timeout: VM timeout in seconds (default: 1800).
            heartbeat_timeout: Per-VM heartbeat timeout. None=use default (300s), 0=disabled.
            wait_for_ready: If True, wait for the job to be ready before returning (default: True).

        Returns:
            Environment object for the new job.

        Raises:
            RuntimeError: If session is closed or job creation fails.
            TimeoutError: If wait_for_ready=True and the job doesn't become ready within timeout.
        """
        self._check_closed()

        # Auto-generate alias if not set
        if env.alias is None:
            existing_aliases = {e.alias for e in self.envs}
            unique_alias = f"env-{uuid.uuid4().hex[:8]}"
            while unique_alias in existing_aliases:
                unique_alias = f"env-{uuid.uuid4().hex[:8]}"
            env.alias = unique_alias

        # Build request
        request = AddJobRequest(
            env=env,
            timeout=timeout,
            heartbeat_timeout=HeartbeatTimeout(heartbeat_timeout) if heartbeat_timeout is not None else None,
        )

        # Call the add_job API
        response = await sessions_add_job.asyncio(
            client=self._http,
            session_id=self.session_id,
            body=request,
            x_api_key=self._api_key,
        )

        # Check for failures
        if not response.env.success:
            raise RuntimeError(f"Failed to add job: {response.env.error}")

        if not response.env.job_id:
            raise RuntimeError("Backend did not return job_id for new environment")

        job_id = response.env.job_id

        # Wait for the job to be ready if requested
        if wait_for_ready:
            ready_response = await jobs_wait_for_ready.asyncio(
                client=self._http,
                job_id=job_id,
                timeout=timeout,
                x_api_key=self._api_key,
            )

            if not ready_response.ready:
                error = ready_response.error or "Unknown error"
                raise TimeoutError(f"Job {job_id} did not become ready: {error}")

        # Update internal context with the new environment
        new_env_context = EnvironmentContext(
            job_id=job_id,
            alias=env.alias,
            artifact_id=response.env.artifact_id,
            simulator=getattr(env, "simulator", None),
        )

        # Add to context's envs list
        if self._context.envs is None:
            self._context.envs = []
        self._context.envs.append(new_env_context)

        # Reset cached envs to force rebuild
        self._envs = None

        # Create and return the Environment object
        new_environment = Environment(
            session=self,
            job_id=job_id,
            alias=env.alias,
            artifact_id=response.env.artifact_id,
            simulator=getattr(env, "simulator", None),
            status="running",  # Newly added environments are running
        )

        logger.info(f"Added job {job_id} (alias={env.alias}) to session {self.session_id}")
        return new_environment

    async def remove_env(self, env: Environment | str) -> None:
        """Remove an environment from this session.

        This will:
        1. Remove the job from the session's network (if connected)
        2. Shut down the VM associated with the job
        3. Cancel the job in the system

        Args:
            env: Environment object or alias string to remove.

        Raises:
            RuntimeError: If session is closed or removal fails.
            ValueError: If environment not found in session.
        """
        self._check_closed()

        # Resolve to job_id
        if isinstance(env, str):
            # Find by alias
            found_env = self.get_env(env)
            if not found_env:
                raise ValueError(f"Environment with alias '{env}' not found in session")
            job_id = found_env.job_id
            alias = env
        else:
            job_id = env.job_id
            alias = env.alias

        # Call the remove_job API
        request = RemoveJobRequest(job_id=job_id)
        response = await sessions_remove_job.asyncio(
            client=self._http,
            session_id=self.session_id,
            body=request,
            x_api_key=self._api_key,
        )

        if not response.success:
            raise RuntimeError(f"Failed to remove job {job_id}")

        # Update internal context - remove the environment
        if self._context.envs:
            self._context.envs = [e for e in self._context.envs if e.job_id != job_id]

        # Reset cached envs to force rebuild
        self._envs = None

        logger.info(f"Removed job {job_id} (alias={alias}) from session {self.session_id}")

    async def cleanup_databases(self) -> SessionCleanupResult:
        """Clean up database audit logs for all environments.

        For each environment:
        1. Gets DB config from the environment's artifact
        2. Connects to each database via proxy tunnel
        3. Finds and truncates audit_log tables
        4. Calls get_state to clear in-memory mutation cache

        This should be called before snapshot() to ensure clean state.
        Environments and databases are cleaned up in parallel for efficiency.

        Requires the 'db-cleanup' optional dependencies:
            pip install plato-sdk-v2[db-cleanup]

        Returns:
            SessionCleanupResult with results for each environment.

        Raises:
            ImportError: If sqlalchemy/asyncpg dependencies are not installed.
        """
        self._check_closed()

        # Lazy import to avoid requiring sqlalchemy for users who don't use this feature
        try:
            from plato.v2.utils.db_cleanup import DatabaseCleaner
        except ImportError as e:
            raise ImportError(
                "Database cleanup requires optional dependencies. Install them with: pip install plato-sdk-v2[db-cleanup]"
            ) from e

        # Build EnvironmentInfo objects
        env_infos = [
            EnvironmentInfo(
                job_id=env.job_id,
                alias=env.alias,
                artifact_id=env.artifact_id,
                get_state_fn=env.get_state,
            )
            for env in self.envs
        ]

        cleaner = DatabaseCleaner()
        return await cleaner.cleanup_session(
            envs=env_infos,
            http_client=self._http,
            api_key=self._api_key,
        )

    async def login(
        self,
        browser: Browser,
        dataset: str = "base",
        screenshots_dir: Path | None = None,
        port: int | None = None,
    ) -> LoginResult:
        """Login to all environments and return browser context with pages.

        Creates a single browser context and one page per environment.
        Navigates each page to the environment's public URL and executes
        the login flow.

        Requires playwright to be installed:
            pip install playwright

        Args:
            browser: Playwright Browser instance.
            dataset: Dataset name for login flow (default: "base" uses "login" flow).
            screenshots_dir: Optional directory to save screenshots during login.
            port: Optional port for public URL (default uses standard port).

        Returns:
            LoginResult containing the browser context and a dict mapping
            environment alias to its logged-in Page.

        Raises:
            RuntimeError: If login fails.
            ImportError: If playwright is not installed.
        """
        self._check_closed()

        import importlib.util

        if importlib.util.find_spec("playwright") is None:
            raise ImportError("The login() method requires playwright. Install it with: pip install playwright")

        context = await browser.new_context()
        pages: dict[str, Page] = {}

        for env in self.envs:
            page = await context.new_page()
            pages[env.alias] = page

            # Get public URL for this job
            public_url_result = await jobs_public_url.asyncio(
                client=self._http,
                job_id=env.job_id,
                port=port,
                x_api_key=self._api_key,
            )

            if public_url_result.error:
                await context.close()
                raise RuntimeError(f"Failed to get public URL for {env.alias}: {public_url_result.error}")

            if not public_url_result.url:
                await context.close()
                raise RuntimeError(f"No public URL returned for {env.alias}")

            await page.goto(public_url_result.url)

            # Get flows for this environment using v2 endpoint
            try:
                flows_response = await jobs_get_flows.asyncio(
                    client=self._http,
                    job_id=env.job_id,
                    x_api_key=self._api_key,
                )
            except Exception as e:
                await context.close()
                raise RuntimeError(f"Failed to get flows for env {env.alias}: {e}") from e

            if not flows_response:
                await context.close()
                raise RuntimeError(f"No flows found for env {env.alias}")

            flows_list = [Flow.model_validate(f) for f in flows_response]

            # Determine flow name based on dataset
            flow_name = "login" if dataset == "base" else dataset

            login_flow = next((flow for flow in flows_list if flow.name == flow_name), None)
            if not login_flow:
                error_msg = f"No flow named '{flow_name}' found for env {env.alias}"
                await context.close()
                raise RuntimeError(error_msg)

            # Execute the login flow (raises FlowExecutionError on failure)
            flow_executor = FlowExecutor(
                page,
                login_flow,
                log=logger,
                screenshots_dir=screenshots_dir,
            )
            try:
                await flow_executor.execute()
            except Exception as e:
                await context.close()
                raise RuntimeError(f"Login failed for env {env.alias}: {e}") from e

        return LoginResult(context=context, pages=pages)

    async def heartbeat(self) -> AppApiV2SchemasSessionHeartbeatResponse:
        """Send heartbeat to keep all environments alive.

        Returns:
            Heartbeat response with results per job_id.
        """
        self._check_closed()

        return await sessions_heartbeat.asyncio(
            client=self._http,
            session_id=self.session_id,
            x_api_key=self._api_key,
        )

    # Heartbeat management

    async def _heartbeat_loop(self) -> None:
        """Background task that periodically sends heartbeats."""
        try:
            while True:
                try:
                    await self.heartbeat()
                    logger.debug(f"Heartbeat sent for session {self.session_id}")
                except Exception as e:
                    logger.error(f"Heartbeat error for session {self.session_id}: {e}")
                await asyncio.sleep(self._heartbeat_interval)
        except asyncio.CancelledError:
            pass

    async def start_heartbeat(self) -> None:
        """Start the heartbeat background task."""
        await self.stop_heartbeat()
        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())

    async def stop_heartbeat(self) -> None:
        """Stop the heartbeat background task."""
        if self._heartbeat_task and not self._heartbeat_task.done():
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass
            self._heartbeat_task = None

    # SSH

    async def add_ssh_key(self, public_key: str, username: str = "root") -> AddSSHKeyResponse:
        """Add an SSH public key to all VMs in this session.

        This allows SSH access to all environments in the session using the
        corresponding private key.

        Args:
            public_key: The SSH public key content (e.g., from id_ed25519.pub).
            username: The user to add the key for (default: root).

        Returns:
            AddSSHKeyResponse with success status.

        Example:
            # Generate a keypair
            subprocess.run(["ssh-keygen", "-t", "ed25519", "-f", "key", "-N", ""])
            public_key = Path("key.pub").read_text()

            # Add to session
            await session.add_ssh_key(public_key)

            # Now SSH works for all envs
            for env in session.envs:
                ssh_info = env.get_ssh_info("key")
                subprocess.run(ssh_info.ssh_command("ls -la"))
        """
        request = AddSSHKeyRequest(public_key=public_key, username=username)
        return await sessions_add_ssh_key.asyncio(
            client=self._http,
            session_id=self.session_id,
            body=request,
            x_api_key=self._api_key,
        )

    # Lifecycle

    async def close(self) -> None:
        """Close the session and all its environments."""
        if self._closed:
            return

        await self.stop_heartbeat()

        await sessions_close.asyncio(
            client=self._http,
            session_id=self.session_id,
            x_api_key=self._api_key,
        )

        self._closed = True

    def _check_closed(self) -> None:
        if self._closed:
            raise RuntimeError("Session is closed")

    def __repr__(self) -> str:
        env_count = len(self._context.envs) if self._context.envs else 0
        return f"Session(session_id={self.session_id!r}, envs={env_count})"

    # Serialization / Deserialization

    def dump(self) -> SerializedSession:
        """Serialize the session for persistence.

        The session can be restored using Session.load().
        Note: The heartbeat task is NOT serialized - it will be restarted
        when the session is loaded.

        Returns:
            SerializedSession containing session state.
        """
        return SerializedSession(
            session_id=self._context.session_id,
            task_public_id=self._context.task_public_id,
            envs=[
                SerializedEnv(
                    job_id=env.job_id,
                    alias=env.alias,
                    artifact_id=env.artifact_id,
                    simulator=env.simulator,
                )
                for env in (self._context.envs or [])
            ],
            api_key=self._api_key,
            base_url=str(self._http.base_url) if self._http.base_url else None,
            closed=self._closed,
        )

    @classmethod
    async def load(
        cls,
        data: SerializedSession,
        *,
        http_client: httpx.AsyncClient | None = None,
        start_heartbeat: bool = True,
    ) -> Session:
        """Restore a session from serialized state.

        Creates a new Session instance from previously serialized state.
        By default, starts the heartbeat background task.

        Args:
            data: SerializedSession from Session.dump().
            http_client: Optional HTTP client. If not provided, a new one is created
                        using the base_url from the serialized data.
            start_heartbeat: Whether to start the heartbeat task (default: True).

        Returns:
            A restored Session instance.
        """
        # Create HTTP client if not provided
        # Use 600s timeout to match the main client (needed for long-polling like wait_for_ready)
        if http_client is None:
            timeout = httpx.Timeout(600.0)
            http_client = (
                httpx.AsyncClient(base_url=data.base_url, timeout=timeout)
                if data.base_url
                else httpx.AsyncClient(timeout=timeout)
            )

        # Rebuild context from serialized envs
        from plato._generated.models import EnvironmentContext

        env_contexts = [
            EnvironmentContext(
                job_id=env.job_id,
                alias=env.alias,
                artifact_id=env.artifact_id,
                simulator=env.simulator,
            )
            for env in data.envs
        ]

        context = SessionContext(
            session_id=data.session_id,
            task_public_id=data.task_public_id,
            envs=env_contexts,
        )

        session = cls(
            http_client=http_client,
            api_key=data.api_key,
            context=context,
        )
        session._closed = data.closed
        session._started = True  # Loaded sessions are already fully initialized

        # Start heartbeat if requested and session isn't closed
        if start_heartbeat and not session._closed:
            await session.start_heartbeat()
            logger.info(f"Session {session.session_id} restored with heartbeat started")
        else:
            logger.info(f"Session {session.session_id} restored (heartbeat not started)")

        return session
