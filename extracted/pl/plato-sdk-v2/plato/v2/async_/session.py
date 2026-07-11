"""Plato SDK v2 - Asynchronous Session Actor.

The Session class wraps a SessionSpec (from backend) with execution capabilities.
It acts like a Ray actor - the spec holds state, the class provides methods.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import multiprocessing
import signal
import time
import uuid
from collections.abc import AsyncIterator, Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

import httpx
import tenacity
from pydantic import BaseModel

if TYPE_CHECKING:
    from playwright.async_api import Browser, BrowserContext, Page

from plato._generated.api.v2.artifacts import get_artifact
from plato._generated.api.v2.jobs import get_flows as jobs_get_flows
from plato._generated.api.v2.jobs import get_job_info as jobs_get_job_info
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
from plato._generated.api.v2.sessions import link_testcase as sessions_link_testcase
from plato._generated.api.v2.sessions import list_jobs as sessions_list_jobs
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
    JobInfo,
    LinkTestcaseRequest,
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
from plato.v2._wait_for_ready import (
    JobTerminalStatusError,
    is_terminal_status,
    poll_until_ready_async,
)
from plato.v2.async_.cdp_bridge import (
    CDP_PORT_BASE,
    kill_agent_browser_daemon,
    resolve_cdp_ws_url,
    shared_cdp_chromium,
)
from plato.v2.async_.environment import Environment
from plato.v2.async_.flow_backends import (
    CLAUDE_CODE_SSH_SHELL_PREFIX,
    make_ssh_run_cmd,
)
from plato.v2.async_.flow_executor import FlowExecutor
from plato.v2.env_utils import is_proctor_env
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
    # Carried so a reattached session keeps the SSH login user (plato for
    # Windows/QEMU) and can reach the VM without re-fetching job info.
    provider: str | None = None
    mesh_ip: str | None = None


class SerializedSession(BaseModel):
    """Serialized session state for persistence and restoration."""

    session_id: str
    task_public_id: str | None = None
    envs: list[SerializedEnv]
    api_key: str
    base_url: str | None = None
    closed: bool = False


def _heartbeat_worker(
    base_url: str | None,
    api_key: str,
    session_id: str,
    interval: int,
) -> None:
    """Run in a child process — sends heartbeats via sync HTTP, immune to event-loop blocking."""
    # Ignore SIGINT so Ctrl-C in the parent doesn't kill the heartbeat mid-request.
    # Handle SIGTERM gracefully so parent shutdown doesn't cause noisy tracebacks.
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    stop = False

    def _handle_term(signum: int, frame: object) -> None:
        nonlocal stop
        stop = True

    signal.signal(signal.SIGTERM, _handle_term)

    timeout = httpx.Timeout(30.0, connect=10.0)
    from plato._generated.api.v2.sessions import heartbeat as _hb_mod

    with httpx.Client(base_url=base_url or "", timeout=timeout) as client:
        while not stop:
            try:
                _hb_mod.sync(
                    client=client,
                    session_id=session_id,
                    x_api_key=api_key,
                )
            except Exception:
                # Errors are non-fatal; next heartbeat will retry.
                pass
            # Sleep in small increments so we notice stop flag quickly
            for _ in range(interval * 10):
                if stop:
                    break
                time.sleep(0.1)


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
        self._heartbeat_process: multiprocessing.Process | None = None
        self._heartbeat_task: asyncio.Task | None = None
        self._heartbeat_interval = 30
        self._envs: list[Environment] | None = None
        self._network_requested = False
        self._network_connected = False
        self._network_result: dict[str, Any] | None = None

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

        logger.debug(f"Session created: {response.session_id}, envs: {[e.alias for e in response.envs]}")

        if not wait:
            context = SessionContext(
                session_id=response.session_id,
                envs=[EnvironmentContext(job_id="", alias=e.alias or "") for e in response.envs if e.success],
            )
            return cls(http_client=http_client, api_key=api_key, context=context)

        try:
            ready_response = await poll_until_ready_async(
                lambda per_call: sessions_wait_for_ready.asyncio(
                    client=http_client,
                    session_id=response.session_id,
                    timeout=per_call,
                    x_api_key=api_key,
                ),
                timeout=int(timeout),
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

        # Resolve simulator names from artifact metadata for artifact-based envs
        if context.envs:
            for env_ctx in context.envs:
                if not env_ctx.simulator and env_ctx.artifact_id:
                    try:
                        artifact_info = await get_artifact.asyncio(
                            client=http_client,
                            artifact_id=env_ctx.artifact_id,
                            x_api_key=api_key,
                        )
                        env_ctx.simulator = artifact_info.simulator_name
                    except Exception:
                        pass

        logger.info(f"All environments in session {response.session_id} are ready")
        session = cls(
            http_client=http_client,
            api_key=api_key,
            context=context,
        )
        session._started = True
        await session.start_heartbeat()

        desktop = session.desktop_env
        if desktop:
            try:
                await desktop.sdk.status()
            except Exception:
                logger.warning("Desktop agent API not ready after session creation")

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
        shutdown_callback_url: str | None = None,
        shutdown_callback_token: str | None = None,
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

        extra_kwargs: dict[str, Any] = {}
        if shutdown_callback_url is not None:
            extra_kwargs["shutdown_callback_url"] = shutdown_callback_url
        if shutdown_callback_token is not None:
            extra_kwargs["shutdown_callback_token"] = shutdown_callback_token
        request_body = CreateSessionFromEnvs(
            envs=[Envs(root=env) for env in envs],
            timeout=timeout,
            source=RunSessionSource.SDK,
            agent_artifact_id=agent_artifact_id,
            **extra_kwargs,
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

            # Aggregate session status: ``failed`` means at least one job is
            # in a terminal state — surface a permanent failure rather than a
            # timeout, even if the budget hasn't been exhausted.
            if is_terminal_status(response):
                detail = ", ".join(errors) if errors else "session reported terminal failure status"
                raise JobTerminalStatusError(
                    f"Environments failed to become ready: {detail}",
                    job_id=None,
                    status=response.status.value,
                    backend_error=detail,
                )
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
                await self._connect_network_if_requested()
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
                    status="running",
                    mesh_ip=ctx.mesh_ip,
                    is_desktop=bool(ctx.is_desktop),
                    provider=ctx.provider,
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

    @property
    def desktop_env(self) -> Environment | None:
        """The desktop VM environment, or None."""
        for env in self.envs:
            if env.is_desktop:
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
            value: Optional agent output data. Used for both OUTPUT scoring and
                   PEX output-dimension scoring. Not needed for mutation-only
                   test cases.

        Returns:
            Evaluation results including score and per-SIM results. For PEX
            (proctor) test cases, the proctor scoring package is surfaced on
            ``pex_result``.
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

    async def link_testcase(self, testcase_id: str) -> None:
        """Link a test case to this session.

        Associates the session with a test case so that :meth:`evaluate` can
        score it.  Useful for Chronos-created sessions that need
        testcase-driven scoring without creating a separate SDK session.

        Args:
            testcase_id: Public ID of the test case to link.
        """
        self._check_closed()

        body = LinkTestcaseRequest(testcase_id=testcase_id)
        await sessions_link_testcase.asyncio(
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
        self._network_requested = True
        if self._network_connected:
            return self._network_result or self._deferred_network_result()
        if not self._has_networkable_envs():
            logger.debug("Deferring network connection for session %s until environments exist", self.session_id)
            return self._deferred_network_result()

        # Server returns 500 with error detail if network connection fails
        result = await sessions_connect_network.asyncio(
            client=self._http,
            session_id=self.session_id,
            x_api_key=self._api_key,
        )
        self._network_connected = True
        self._network_result = result if isinstance(result, dict) else result.model_dump()
        return result

    async def add_env(
        self,
        env: EnvFromSimulator | EnvFromArtifact | EnvFromResource,
        *,
        timeout: int = 1800,
        ready_timeout: int = 600,
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
            timeout: VM lifetime in seconds (default: 1800). Sent to the backend as
                ``AddJobRequest.timeout`` — the backend kills the VM after this elapses.
            ready_timeout: Maximum seconds the client polls ``wait_for_ready`` before
                raising ``TimeoutError`` (default: 600). Independent of VM lifetime so
                a long-lived VM does not force a long readiness wait when something has
                gone wrong. Always clamped to ``timeout`` so the polling deadline never
                outlives the VM.
            heartbeat_timeout: Per-VM heartbeat timeout. None=use default (300s), 0=disabled.
            wait_for_ready: If True, wait for the job to be ready before returning (default: True).

        Returns:
            Environment object for the new job.

        Raises:
            RuntimeError: If session is closed or job creation fails.
            TimeoutError: If wait_for_ready=True and the job doesn't become ready
                within ``ready_timeout``.
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
        is_desktop = bool(response.env.is_desktop)

        # provider isn't carried on the add-job (EnvInfo) or wait-for-ready
        # (WaitForReadyResult) responses, so it comes from the job-info round
        # trip below; mesh_ip comes from wait-for-ready.
        provider: str | None = None
        mesh_ip: str | None = None
        if wait_for_ready:
            poll_budget = min(ready_timeout, timeout)
            ready_response = await poll_until_ready_async(
                lambda per_call: jobs_wait_for_ready.asyncio(
                    client=self._http,
                    job_id=job_id,
                    timeout=per_call,
                    x_api_key=self._api_key,
                ),
                timeout=poll_budget,
            )
            if not ready_response.ready:
                error = ready_response.error or "Unknown error"
                if is_terminal_status(ready_response):
                    status_value = ready_response.status.value
                    raise JobTerminalStatusError(
                        f"Job {job_id} reached terminal status '{status_value}' before becoming ready: {error}",
                        job_id=job_id,
                        status=status_value,
                        backend_error=ready_response.error,
                    )
                raise TimeoutError(f"Job {job_id} did not become ready: {error}")
            mesh_ip = ready_response.mesh_ip
            # provider may ride the ready response (read defensively — the
            # generated WaitForReadyResult doesn't declare it yet); the
            # job-info fetch below is the fallback when it doesn't.
            provider = provider or getattr(ready_response, "provider", None)
            if not mesh_ip:
                logger.warning(
                    "wait_for_ready returned no mesh_ip for job %s (ready=%s, response=%s)",
                    job_id,
                    ready_response.ready,
                    ready_response.model_dump(),
                )

        # provider drives desktop/qemu detection (it gates the SDK client's
        # _is_qemu, which picks the Windows PowerShell vs ubuntu bash chrome
        # launch path). When the ready response didn't carry it, fall back to
        # the job-info round trip — but only for artifact-backed VMs
        # (resource/runtime envs have no provider).
        if provider is None and response.env.artifact_id:
            # Best-effort: get_job_info raises on a non-2xx response, so guard
            # the whole call — a transient backend error must not fail add_env.
            # provider only drives desktop/qemu detection; leaving it None just
            # means we don't treat the env as a qemu desktop.
            try:
                job_info = await jobs_get_job_info.asyncio(
                    client=self._http,
                    job_id=job_id,
                    x_api_key=self._api_key,
                )
                provider = job_info.provider if job_info is not None else None
            except Exception as exc:
                logger.warning(
                    "get_job_info failed for job %s; skipping provider detection: %s",
                    job_id,
                    exc,
                )

        # Update internal context with the new environment
        new_env_context = EnvironmentContext(
            job_id=job_id,
            alias=env.alias,
            artifact_id=response.env.artifact_id,
            simulator=getattr(env, "simulator", None),
            is_desktop=is_desktop,
            mesh_ip=mesh_ip,
            provider=provider,
        )

        # Add to context's envs list
        if self._context.envs is None:
            self._context.envs = []
        self._context.envs.append(new_env_context)

        # Reset cached envs to force rebuild
        self._envs = None
        if wait_for_ready:
            await self._connect_network_if_requested()

        # Create and return the Environment object
        new_environment = Environment(
            session=self,
            job_id=job_id,
            alias=env.alias,
            artifact_id=response.env.artifact_id,
            simulator=getattr(env, "simulator", None),
            status="running",  # Newly added environments are running
            mesh_ip=mesh_ip,
            is_desktop=is_desktop,
            provider=provider,
        )

        logger.debug(f"Added job {job_id} (alias={env.alias}) to session {self.session_id}")
        return new_environment

    async def list_jobs(self) -> list[JobInfo]:
        """List every job in this session with its live backend status.

        Unlike ``envs`` (built from the locally cached context, which goes
        stale across processes), this asks the backend — it sees jobs added
        or removed by other processes and reports their current status.
        """
        self._check_closed()
        response = await sessions_list_jobs.asyncio(
            client=self._http,
            session_id=self.session_id,
            x_api_key=self._api_key,
        )
        return list(response.jobs)

    async def remove_job(self, job_id: str) -> bool:
        """Remove a job from this session by id (network + VM + cancel).

        Thin wrapper over the remove-job API for jobs that are not in the
        locally cached env context (e.g. leaked by another process); use
        ``remove_env`` for environments this session object created itself.
        """
        self._check_closed()
        request = RemoveJobRequest(job_id=job_id)
        response = await sessions_remove_job.asyncio(
            client=self._http,
            session_id=self.session_id,
            body=request,
            x_api_key=self._api_key,
        )
        return bool(response.success)

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
            env_obj = found_env
            job_id = found_env.job_id
            alias = env
        else:
            env_obj = env
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

        # Forget this VM's SSH host→user entries so a later VM reusing the mesh
        # IP / host string can't inherit a stale login user.
        env_obj._unregister_ssh_user()

        # Update internal context - remove the environment
        if self._context.envs:
            self._context.envs = [e for e in self._context.envs if e.job_id != job_id]

        # Reset cached envs to force rebuild
        self._envs = None

        logger.debug(f"Removed job {job_id} (alias={alias}) from session {self.session_id}")

    async def cleanup_databases(
        self,
        aliases: Iterable[str] | None = None,
    ) -> SessionCleanupResult:
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

        Args:
            aliases: Optional iterable of env aliases to limit cleanup to. When
                provided, only envs whose alias is in the set are cleaned;
                others (e.g. infrastructure VMs added during the session) are
                skipped. ``None`` cleans every env in the session.

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

        alias_filter = set(aliases) if aliases is not None else None

        # Build EnvironmentInfo objects
        env_infos = [
            EnvironmentInfo(
                job_id=env.job_id,
                alias=env.alias,
                artifact_id=env.artifact_id,
                get_state_fn=env.get_state,
            )
            for env in self.envs
            if alias_filter is None or env.alias in alias_filter
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
        flow: str = "login",
        screenshots_dir: Path | None = None,
        port: int | None = None,
        *,
        env_alias: str | None = None,
        context: BrowserContext | None = None,
        retries: int = 0,
        retry_delay_ms: int = 0,
    ) -> LoginResult:
        """Login to environments and return browser context with pages.

        Creates a single browser context (unless ``context`` is provided) and
        one page per target environment. Navigates each page to the env's
        public URL and executes the login flow.

        Requires playwright to be installed:
            uv add playwright

        Args:
            browser: Playwright Browser instance.
            flow: Name of the flow to run (default: "login").
            screenshots_dir: Optional directory to save screenshots during login.
            port: Optional port for public URL (default uses standard port).
            env_alias: If set, only log into this single env. ``None`` iterates
                all envs in ``self.envs``.
            context: Reuse an existing BrowserContext (useful for CDP callers
                that want to keep stray default-context tabs). When ``None``,
                a fresh context is created.
            retries: Per-env retries on flow-execution failure. Between
                attempts the page is re-navigated to the public URL.
            retry_delay_ms: Delay between retries in milliseconds.

        Returns:
            LoginResult containing the browser context and a dict mapping
            environment alias to its logged-in Page.

        Raises:
            RuntimeError: If login fails.
            ImportError: If playwright is not installed.
            RuntimeError: If session contains a desktop environment.
        """
        self._check_closed()

        if self.desktop_env is not None:
            raise RuntimeError(
                "This session contains a desktop environment. "
                "Use desktop.sdk.login(session) instead of session.login(browser). "
                "See desktop_env property for details."
            )

        import importlib.util

        if importlib.util.find_spec("playwright") is None:
            raise ImportError("The login() method requires playwright. Install it with: uv add playwright")

        owns_context = context is None
        if context is None:
            context = await browser.new_context()

        pages: dict[str, Page] = {}
        if env_alias:
            target_envs = [e for e in self.envs if e.alias == env_alias]
        else:
            target_envs = []
            for e in self.envs:
                if is_proctor_env(e):
                    logger.info("Skipping login for %s (proctor service)", e.alias)
                    continue
                target_envs.append(e)
        if env_alias and not target_envs:
            if owns_context:
                await context.close()
            raise RuntimeError(f"No env with alias '{env_alias}' in session")

        try:
            for env in target_envs:
                page = await context.new_page()
                pages[env.alias] = page

                public_url = await self._public_url(env, port=port)
                login_flow = await self._fetch_login_flow(env, flow)

                flow_executor = FlowExecutor(
                    page,
                    login_flow,
                    log=logger,
                    screenshots_dir=screenshots_dir,
                )

                last_error: Exception | None = None
                for attempt in range(1 + retries):
                    try:
                        await page.goto(public_url)
                        await flow_executor.execute()
                        last_error = None
                        break
                    except Exception as e:
                        last_error = e
                        if attempt < retries:
                            logger.warning(
                                "Login flow failed for %s (attempt %d/%d), retrying in %dms: %s",
                                env.alias,
                                attempt + 1,
                                1 + retries,
                                retry_delay_ms,
                                e,
                            )
                            await asyncio.sleep(retry_delay_ms / 1000)
                if last_error is not None:
                    raise RuntimeError(f"Login failed for env {env.alias}: {last_error}") from last_error
        except Exception:
            if owns_context:
                await context.close()
            raise

        return LoginResult(context=context, pages=pages)

    async def _fetch_login_flow(self, env: Environment, flow_name: str) -> Flow:
        """Fetch the flow named ``flow_name`` for ``env``."""
        try:
            flows_response = await jobs_get_flows.asyncio(
                client=self._http,
                job_id=env.job_id,
                x_api_key=self._api_key,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to get flows for env {env.alias}: {e}") from e

        if not flows_response:
            raise RuntimeError(f"No flows found for env {env.alias}")

        flows_list = [Flow.model_validate(f) for f in flows_response]
        match = next((f for f in flows_list if f.name == flow_name), None)
        if not match:
            raise RuntimeError(f"No flow named '{flow_name}' found for env {env.alias}")
        return match

    async def _public_url(self, env: Environment, port: int | None = None) -> str:
        """Fetch a public URL for ``env`` with uniform error handling."""
        result = await jobs_public_url.asyncio(
            client=self._http,
            job_id=env.job_id,
            port=port,
            x_api_key=self._api_key,
        )
        if result.error:
            raise RuntimeError(f"Failed to get public URL for {env.alias}: {result.error}")
        if not result.url:
            raise RuntimeError(f"No public URL returned for {env.alias}")
        return result.url

    @contextlib.asynccontextmanager
    async def connect_cdp(self, cdp_url: str, *, ready_timeout: float = 60.0) -> AsyncIterator[Browser]:
        """Connect Playwright to a CDP endpoint and yield the Browser.

        Polls ``/json/version`` until Chrome is ready (``ready_timeout`` seconds,
        default 60) then fetches + rewrites the WS URL so callers on a
        different host than the Chrome instance don't hit the
        ``ws://localhost:9225`` bug. The browser is closed automatically when
        the ``async with`` block exits.

        Example::

            async with session.connect_cdp(f"http://{host}:9224") as browser:
                result = await session.login(browser=browser, env_alias="env1")
                # use result.pages["env1"] for post-login work
        """
        self._check_closed()

        import importlib.util

        if importlib.util.find_spec("playwright") is None:
            raise ImportError("connect_cdp() requires playwright. Install with: uv add playwright")

        from playwright.async_api import async_playwright

        ws_url = await resolve_cdp_ws_url(cdp_url, ready_timeout=ready_timeout)
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(ws_url)
            try:
                yield browser
            finally:
                with contextlib.suppress(Exception):
                    await browser.close()

    async def _stabilize_post_login(
        self,
        result: LoginResult,
        log: logging.Logger,
    ) -> None:
        """Reload login pages at ``networkidle``, close stray tabs, surface login page.

        Shared by :meth:`login_via_cdp` and :meth:`login_via_agent_browser`:
        both hand the Chromium off to an external consumer (a world driving
        the browser; an agent-browser daemon) that attaches immediately
        after login. SPAs like Mattermost / Docmost finish JWT / token /
        workspace-hydration setup *after* the form submit promise resolves,
        so the consumer can race that setup. Reloading each logged-in page
        with ``wait_until="networkidle"`` pins the SPA in its post-auth
        steady state; closing leftover ``about:blank`` tabs keeps the
        consumer from picking one as the active page; ``bring_to_front``
        makes the login page the focused tab.
        """
        login_pages = set(result.pages.values())
        for page in list(result.pages.values()):
            await asyncio.sleep(2)
            with contextlib.suppress(Exception):
                await page.reload(wait_until="networkidle", timeout=15000)
            await asyncio.sleep(1)
            log.info("Post-login page URL: %s", page.url)
        for tab in list(result.context.pages):
            if tab not in login_pages and tab.url == "about:blank":
                with contextlib.suppress(Exception):
                    await tab.close()
        primary = next(iter(result.pages.values()), None)
        if primary is not None:
            with contextlib.suppress(Exception):
                await primary.bring_to_front()

    async def login_via_cdp(
        self,
        cdp_url: str,
        flow: str = "login",
        screenshots_dir: Path | None = None,
        port: int | None = None,
        *,
        env_alias: str | None = None,
        retries: int = 0,
        retry_delay_ms: int = 0,
        ready_timeout: float = 60.0,
        log: logging.Logger | None = None,
    ) -> None:
        """Log in via a CDP-attached Chromium, closing the browser when done.

        Logs into each env, then (because the typical caller is a world that
        will hand the same Chrome to a downstream agent) reloads each
        logged-in page with ``networkidle``, closes stray ``about:blank``
        tabs left in the default context, and brings the logged-in page to
        the front. Apps like Mattermost finish JWT/token setup *after* form
        submission — an agent that attaches before the reload can race it.

        For raw login without the post-login cleanup, use
        :meth:`connect_cdp` + :meth:`login` directly.
        """
        active_log = log or logger
        async with self.connect_cdp(cdp_url, ready_timeout=ready_timeout) as browser:
            result = await self.login(
                browser=browser,
                context=browser.contexts[0],
                flow=flow,
                screenshots_dir=screenshots_dir,
                port=port,
                env_alias=env_alias,
                retries=retries,
                retry_delay_ms=retry_delay_ms,
            )
            await self._stabilize_post_login(result, active_log)

    async def login_via_agent_browser(
        self,
        *,
        hostname: str,
        ssh_key_path: Path,
        extra_ssh_opts: list[tuple[str, str]] | None = None,
        shell_prefix: str = CLAUDE_CODE_SSH_SHELL_PREFIX,
        flow: str = "login",
        env_alias: str | None = None,
        port: int | None = None,
        screenshots_dir: Path | None = None,
        retries: int = 0,
        retry_delay_ms: int = 0,
        log: logging.Logger | None = None,
    ) -> list[str]:
        """Log in to envs, then hand each browser to an agent-browser daemon.

        For each env we launch a long-lived chromium on the remote VM with a
        CDP port, tunnel the port back, run the env's Playwright login flow
        against it through :class:`FlowExecutor`, and then attach an
        ``agent-browser --session <env.alias>`` daemon to the same chromium
        via ``connect <port>``. The daemon inherits cookies, storage, and the
        post-login tab — so later ``agent-browser --session <alias>`` calls
        from the agent run on an already-authenticated browser.

        The flow runs under Playwright (not the agent-browser CLI), so any
        selector Playwright supports — including ``:has-text()`` — works
        without translation.

        Parameters
        ----------
        hostname, ssh_key_path, extra_ssh_opts, shell_prefix:
            Forwarded to :func:`make_ssh_run_cmd`. ``shell_prefix`` defaults
            to the claude-code/gemini-cli/codex base image layout; override for
            other images.
        flow:
            Name of the flow to run (default: ``"login"``).
        env_alias:
            Optional env alias to log into. When omitted, logs into every
            artifact env in the session.
        port:
            Optional port for the env's public URL.
        retries:
            Number of retries per env on flow-execution failure. Total attempts
            per env is ``1 + retries``. Defaults to ``0``. Between attempts we
            re-navigate to the public URL so flows that mutated page state
            start from a clean slate.
        retry_delay_ms:
            Delay between retries in milliseconds. Ignored when ``retries == 0``.
        log:
            Optional logger; defaults to the module logger.

        Returns
        -------
        list[str]
            Aliases of envs that logged in successfully, in input order.
        """
        self._check_closed()

        import importlib.util

        if importlib.util.find_spec("playwright") is None:
            raise ImportError("login_via_agent_browser requires playwright. Install it with: uv add playwright")
        from playwright.async_api import async_playwright

        active_log = log or logger
        run_cmd = make_ssh_run_cmd(
            ssh_key_path=ssh_key_path,
            hostname=hostname,
            shell_prefix=shell_prefix,
            extra_opts=extra_ssh_opts,
        )

        logged_in: list[str] = []
        for idx, env in enumerate(self.envs):
            if not env.artifact_id:
                # Resource/compute envs have no login flow — skip cleanly so
                # callers can pass ``session.envs`` without pre-filtering.
                continue
            if env_alias is not None and env.alias != env_alias:
                continue
            if env_alias is None and is_proctor_env(env):
                active_log.info("Skipping login for %s (proctor service)", env.alias)
                continue

            cdp_port = CDP_PORT_BASE + idx
            profile_dir = f"/tmp/plato-ab-{env.alias}-{self.session_id}"

            last_error: Exception | None = None
            for attempt in range(1 + retries):
                if attempt > 0:
                    # Tear down the previous attempt's daemon so the next
                    # ``connect`` call attaches a fresh one. The previous
                    # ``shared_cdp_chromium`` ctx has already exited, so the
                    # next iteration's ``kill_stale_chromium`` will kill the
                    # old chromium and rm its profile dir before respawning.
                    await kill_agent_browser_daemon(run_cmd, alias=env.alias, log=active_log)
                    await asyncio.sleep(retry_delay_ms / 1000)

                active_log.info(
                    "agent-browser login: env=%s flow=%s cdp_port=%d attempt=%d/%d",
                    env.alias,
                    flow,
                    cdp_port,
                    attempt + 1,
                    1 + retries,
                )

                try:
                    async with shared_cdp_chromium(
                        run_cmd=run_cmd,
                        ssh_key_path=ssh_key_path,
                        hostname=hostname,
                        extra_ssh_opts=extra_ssh_opts,
                        port=cdp_port,
                        profile_dir=profile_dir,
                        log=active_log,
                    ) as local_cdp_url:
                        # Attach the agent-browser daemon BEFORE Playwright
                        # drives login so it's ready to inherit cookies once
                        # the SPA finishes its post-auth setup.
                        rc, _, err = await run_cmd(
                            [
                                "agent-browser",
                                "--session",
                                env.alias,
                                "connect",
                                str(cdp_port),
                            ]
                        )
                        if rc != 0:
                            raise RuntimeError(
                                f"agent-browser --session {env.alias} connect {cdp_port} failed: rc={rc} stderr={err[-400:]!r}"
                            )

                        async with async_playwright() as pw:
                            browser = await pw.chromium.connect_over_cdp(local_cdp_url)
                            try:
                                # Route through ``self.login()`` so
                                # FlowExecutor is wired identically to
                                # ``login_via_cdp``: ``screenshots_dir``
                                # threaded through, no spurious ``base_url``.
                                # Inner ``retries=0`` — the outer loop owns
                                # retry semantics so a failure throws away
                                # chromium + profile + daemon for a clean
                                # reset, rather than ``self.login`` only
                                # re-navigating the page in-place.
                                context = browser.contexts[0] if browser.contexts else None
                                result = await self.login(
                                    browser=browser,
                                    context=context,
                                    flow=flow,
                                    screenshots_dir=screenshots_dir,
                                    port=port,
                                    env_alias=env.alias,
                                    retries=0,
                                    retry_delay_ms=0,
                                )
                                await self._stabilize_post_login(result, active_log)
                            finally:
                                # Disconnect the Playwright client only. The
                                # remote chromium stays alive and the agent-
                                # browser daemon keeps its CDP attachment.
                                with contextlib.suppress(Exception):
                                    await browser.close()
                    last_error = None
                    break
                except Exception as exc:
                    last_error = exc
                    if attempt < retries:
                        active_log.warning(
                            "agent-browser login: env=%s attempt %d/%d failed (%s); "
                            "tearing down chromium + profile + daemon and retrying",
                            env.alias,
                            attempt + 1,
                            1 + retries,
                            exc,
                        )

            if last_error is not None:
                raise RuntimeError(
                    f"agent-browser login failed for env {env.alias} after {1 + retries} attempt(s): {last_error}"
                ) from last_error

            logged_in.append(env.alias)

        if env_alias is not None and not logged_in:
            raise RuntimeError(f"No artifact env found for env_alias={env_alias!r}")

        return logged_in

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
        """Background asyncio task that periodically sends heartbeats."""
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

    async def start_heartbeat(self, *, use_process: bool = False) -> None:
        """Start the heartbeat background loop.

        Args:
            use_process: If True, run heartbeat in a child process (immune to
                event-loop blocking by sync code). If False (default), use an
                asyncio task.
        """
        await self.stop_heartbeat()
        if use_process:
            base_url = str(self._http.base_url) if self._http.base_url else None
            self._heartbeat_process = multiprocessing.Process(
                target=_heartbeat_worker,
                args=(base_url, self._api_key, self.session_id, self._heartbeat_interval),
                daemon=True,
                name=f"heartbeat-{self.session_id[:8]}",
            )
            self._heartbeat_process.start()
            logger.debug(f"Heartbeat process started (pid={self._heartbeat_process.pid}) for session {self.session_id}")
        else:
            self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())

    async def stop_heartbeat(self) -> None:
        """Stop the heartbeat (process or task)."""
        # Stop process if running (join in executor to avoid blocking the event loop)
        proc = self._heartbeat_process
        if proc is not None and proc.is_alive():
            proc.terminate()
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, proc.join, 5)
            if proc.is_alive():
                proc.kill()
                await loop.run_in_executor(None, proc.join, 2)
            logger.debug(f"Heartbeat process stopped for session {self.session_id}")
        self._heartbeat_process = None

        # Stop task if running
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

        # Forget this session's SSH host→user entries so they don't linger in a
        # long-lived process. Only built Environments ever registered anything.
        for env in self._envs or []:
            env._unregister_ssh_user()

        self._closed = True

    def _check_closed(self) -> None:
        if self._closed:
            raise RuntimeError("Session is closed")

    def _has_networkable_envs(self) -> bool:
        env_contexts = self._context.envs or []
        return any(env.job_id for env in env_contexts)

    def _deferred_network_result(self) -> dict[str, Any]:
        return {
            "success": True,
            "session_id": self.session_id,
            "subnet": None,
            "results": {},
            "deferred": True,
        }

    async def _connect_network_if_requested(self) -> None:
        if self._network_requested and not self._network_connected and self._has_networkable_envs():
            await self.connect_network()

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
                    provider=getattr(env, "provider", None),
                    mesh_ip=getattr(env, "mesh_ip", None),
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
        data: SerializedSession | Mapping[str, object],
        *,
        http_client: httpx.AsyncClient | None = None,
        start_heartbeat: bool = True,
        heartbeat_use_process: bool = False,
    ) -> Session:
        """Restore a session from serialized state.

        Creates a new Session instance from previously serialized state.
        By default, starts the heartbeat background task.

        Args:
            data: SerializedSession from Session.dump(), or its JSON-decoded mapping form.
            http_client: Optional HTTP client. If not provided, a new one is created
                        using the base_url from the serialized data.
            start_heartbeat: Whether to start the heartbeat task (default: True).
            heartbeat_use_process: If True, run heartbeat in a child process.

        Returns:
            A restored Session instance.
        """
        serialized = SerializedSession.model_validate(data)

        # Create HTTP client if not provided
        # Use 600s timeout to match the main client (needed for long-polling like wait_for_ready)
        if http_client is None:
            timeout = httpx.Timeout(600.0)
            http_client = (
                httpx.AsyncClient(base_url=serialized.base_url, timeout=timeout)
                if serialized.base_url
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
                provider=env.provider,
                mesh_ip=env.mesh_ip,
            )
            for env in serialized.envs
        ]

        context = SessionContext(
            session_id=serialized.session_id,
            task_public_id=serialized.task_public_id,
            envs=env_contexts,
        )

        session = cls(
            http_client=http_client,
            api_key=serialized.api_key,
            context=context,
        )
        session._closed = serialized.closed
        session._started = True  # Loaded sessions are already fully initialized

        # Start heartbeat if requested and session isn't closed
        if start_heartbeat and not session._closed:
            await session.start_heartbeat(use_process=heartbeat_use_process)
            logger.debug(f"Session {session.session_id} restored with heartbeat started")
        else:
            logger.debug(f"Session {session.session_id} restored (heartbeat not started)")

        return session
