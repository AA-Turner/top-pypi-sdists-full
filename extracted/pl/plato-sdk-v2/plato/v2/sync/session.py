"""Plato SDK v2 - Synchronous Session Actor.

The Session class wraps a SessionSpec (from backend) with execution capabilities.
It acts like a Ray actor - the spec holds state, the class provides methods.
"""

from __future__ import annotations

import logging
import threading
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import httpx
import tenacity

if TYPE_CHECKING:
    from playwright.sync_api import Browser, BrowserContext, Page

from plato._generated.api.v2.artifacts import get_artifact
from plato._generated.api.v2.jobs import get_flows as jobs_get_flows
from plato._generated.api.v2.jobs import public_url as jobs_public_url
from plato._generated.api.v2.jobs import wait_for_ready as jobs_wait_for_ready
from plato._generated.api.v2.sessions import add_job as sessions_add_job
from plato._generated.api.v2.sessions import close as sessions_close
from plato._generated.api.v2.sessions import connect_network as sessions_connect_network
from plato._generated.api.v2.sessions import disk_snapshot as sessions_disk_snapshot
from plato._generated.api.v2.sessions import evaluate as sessions_evaluate
from plato._generated.api.v2.sessions import execute as sessions_execute
from plato._generated.api.v2.sessions import get_public_url as sessions_get_public_url
from plato._generated.api.v2.sessions import heartbeat as sessions_heartbeat
from plato._generated.api.v2.sessions import link_testcase as sessions_link_testcase
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
from plato.v2.sync.environment import Environment
from plato.v2.sync.flow_executor import FlowExecutor
from plato.v2.types import EnvFromArtifact, EnvFromResource, EnvFromSimulator

logger = logging.getLogger(__name__)


@dataclass
class LoginResult:
    """Result of login operation containing browser context and pages.

    Requires playwright to be installed.

    Attributes:
        context: The Playwright BrowserContext used for all pages.
        pages: Dict mapping env alias to the logged-in Page.
    """

    context: BrowserContext
    pages: dict[str, Page]


class Session:
    """Actor wrapper for SessionSpec - provides execution methods.

    The Session wraps a SessionSpec (which contains the runtime state) and adds
    methods to execute operations on the session. This is similar to a Ray actor
    pattern where the spec is the state and the class provides the interface.

    Usage:
        from plato.v2 import Plato, Env

        plato = Plato()
        session = plato.from_envs(envs=[Env.simulator("espocrm")])

        # Operations execute against the backend
        session.reset()
        state = session.get_state()
        result = session.execute("ls -la")

        session.close()
        plato.close()
    """

    def __init__(
        self,
        http_client: httpx.Client,
        api_key: str,
        context: SessionContext,
    ):
        """Initialize session actor.

        Args:
            http_client: HTTP client for API calls.
            api_key: API key for authentication.
            context: SessionContext from backend with session_id, envs, and task_public_id.
        """

        self._http = http_client
        self._api_key = api_key
        self._context = context
        self._closed = False
        self._heartbeat_thread: threading.Thread | None = None
        self._heartbeat_stop = threading.Event()
        self._heartbeat_interval = 30
        self._envs: list[Environment] | None = None
        self._network_requested = False
        self._network_connected = False
        self._network_result: dict[str, object] | None = None

    @property
    def session_id(self) -> str:
        """Get the session ID."""
        return self._context.session_id

    @property
    def task_public_id(self) -> str | None:
        """Get the task public ID if session was created from a task."""
        return self._context.task_public_id

    @classmethod
    def _make_session(
        cls,
        http_client: httpx.Client,
        api_key: str,
        request_body,
        timeout: int,
    ) -> Session:
        """Shared session creation: POST /make, check failures, wait for ready, start heartbeat.

        All creation paths (from_envs, from_testcase, from_artifacts) funnel through here.
        """
        response = sessions_make.sync(
            client=http_client,
            body=request_body,
            x_api_key=api_key,
        )

        failures = [e for e in response.envs if not e.success]
        if failures:
            try:
                sessions_close.sync(
                    client=http_client,
                    session_id=response.session_id,
                    x_api_key=api_key,
                )
            except Exception as close_err:
                logger.warning(f"Failed to close session after env creation failure: {close_err}")

            failure_details = ", ".join([f"{e.alias}: {e.error}" for e in failures])
            raise RuntimeError(f"Failed to create environments: {failure_details}")

        try:
            ready_response = sessions_wait_for_ready.sync(
                client=http_client,
                session_id=response.session_id,
                timeout=int(timeout),
                x_api_key=api_key,
            )
            context = cls._check_ready_response(ready_response, timeout)
        except (TimeoutError, RuntimeError):
            try:
                sessions_close.sync(
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
                        artifact_info = get_artifact.sync(
                            client=http_client,
                            artifact_id=env_ctx.artifact_id,
                            x_api_key=api_key,
                        )
                        env_ctx.simulator = artifact_info.simulator_name
                    except Exception:
                        pass

        logger.debug(f"All environments in session {response.session_id} are ready")
        session = cls(
            http_client=http_client,
            api_key=api_key,
            context=context,
        )
        session.start_heartbeat()

        desktop = session.desktop_env
        if desktop:
            try:
                desktop.sdk.status()
            except Exception:
                logger.warning("Desktop agent API not ready after session creation")

        return session

    @classmethod
    def from_envs(
        cls,
        http_client: httpx.Client,
        api_key: str,
        envs: list[EnvFromSimulator | EnvFromArtifact | EnvFromResource],
        *,
        timeout: int = 1800,
    ) -> Session:
        """Create a new session from environment configurations.

        Waits for all environments to be ready (RUNNING status) before returning.
        Does NOT automatically reset -- call ``session.reset()`` when ready.

        Args:
            http_client: The httpx client for making requests.
            api_key: API key for authentication.
            envs: List of environment configurations (from Env.simulator() or Env.artifact()).
            timeout: VM timeout in seconds (default: 1800).

        Returns:
            A new Session instance with all environments ready.

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
        )
        return cls._make_session(http_client, api_key, request_body, timeout)

    @classmethod
    def from_testcase(
        cls,
        http_client: httpx.Client,
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
            http_client: The httpx client for making requests.
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
        session = cls._make_session(http_client, api_key, request_body, timeout)

        sessions_reset.sync(
            client=http_client,
            session_id=session.session_id,
            body=ResetSessionRequest(),
            x_api_key=api_key,
        )
        logger.debug(f"Session {session.session_id} reset for mutation capture")
        return session

    @classmethod
    def from_artifacts(
        cls,
        http_client: httpx.Client,
        api_key: str,
        artifact_ids: list[str],
        *,
        timeout: int = 1800,
    ) -> Session:
        """Create a new session from artifact IDs.

        Convenience method that wraps each artifact ID into an EnvFromArtifact
        and delegates to from_envs(). Does NOT automatically reset -- call
        ``session.reset()`` when ready to begin mutation logging.

        Args:
            http_client: The httpx client for making requests.
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
        return cls.from_envs(http_client, api_key, envs, timeout=timeout)

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

    def wait_until_ready(
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
            RuntimeError: If any environment fails.
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
        def _poll_ready():
            response = sessions_wait_for_ready.sync(
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
                logger.debug(f"All environments in session {self.session_id} are ready")
                self._connect_network_if_requested()
                return

            raise NotReadyError("Environments not ready yet")

        try:
            _poll_ready()
        except NotReadyError:
            raise TimeoutError(f"Environments did not become ready within {timeout} seconds")

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
                    is_desktop=bool(ctx.is_desktop),
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

    def _has_networkable_envs(self) -> bool:
        env_contexts = self._context.envs or []
        return any(env.job_id for env in env_contexts)

    def _deferred_network_result(self) -> dict[str, object]:
        return {
            "success": True,
            "session_id": self.session_id,
            "subnet": None,
            "results": {},
            "deferred": True,
        }

    def _connect_network_if_requested(self) -> None:
        if self._network_requested and not self._network_connected and self._has_networkable_envs():
            self.connect_network()

    def reset(self, **kwargs) -> ResetSessionResponse:
        """Reset all environments in the session to initial state.

        Returns:
            ResetSessionResponse with results per job_id.
        """
        self._check_closed()

        request = ResetSessionRequest(**kwargs)
        return sessions_reset.sync(
            client=self._http,
            session_id=self.session_id,
            body=request,
            x_api_key=self._api_key,
        )

    def get_state(self) -> SessionStateResponse:
        """Get state from all environments in the session.

        Returns:
            SessionStateResponse with state per job_id.
        """
        self._check_closed()

        return sessions_state.sync(
            client=self._http,
            session_id=self.session_id,
            x_api_key=self._api_key,
        )

    def execute(
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
        return sessions_execute.sync(
            client=self._http,
            session_id=self.session_id,
            body=request,
            x_api_key=self._api_key,
        )

    def set_date(
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
        return sessions_set_date.sync(
            client=self._http,
            session_id=self.session_id,
            body=request,
            x_api_key=self._api_key,
        )

    def setup_sandbox(
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
        return sessions_setup_sandbox.sync(
            client=self._http,
            session_id=self.session_id,
            body=request,
            x_api_key=self._api_key,
        )

    def evaluate(self, value: dict | None = None) -> AppApiV2SchemasSessionEvaluateResponse:
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
        self.get_state()

        body = AppApiV2SchemasSessionEvaluateRequest(value=value)
        return sessions_evaluate.sync(
            client=self._http,
            session_id=self.session_id,
            body=body,
            x_api_key=self._api_key,
        )

    def get_public_url(self, port: int | None = None) -> dict[str, str]:
        """Get public URLs for all environments in the session.

        Returns browser-accessible URLs in format: {job_id}--{port}.sims.plato.so

        Args:
            port: Port number for the URLs. If not specified, uses the default port.

        Returns:
            Dict mapping alias to public URL.
        """
        self._check_closed()

        response = sessions_get_public_url.sync(
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

    def link_testcase(self, testcase_id: str) -> None:
        """Link a test case to this session.

        Associates the session with a test case so that :meth:`evaluate` can
        score it.  Useful for Chronos-created sessions that need
        testcase-driven scoring without creating a separate SDK session.

        Args:
            testcase_id: Public ID of the test case to link.
        """
        self._check_closed()

        body = LinkTestcaseRequest(testcase_id=testcase_id)
        sessions_link_testcase.sync(
            client=self._http,
            session_id=self.session_id,
            body=body,
            x_api_key=self._api_key,
        )

    def snapshot(self) -> AppApiV2SchemasSessionCreateSnapshotResponse:
        """Create a snapshot of all environments in the session.

        Returns:
            Snapshot response with info per job_id.
        """
        self._check_closed()

        return sessions_snapshot.sync(
            client=self._http,
            session_id=self.session_id,
            body=AppApiV2SchemasSessionCreateSnapshotRequest(),
            x_api_key=self._api_key,
        )

    def snapshot_store(
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

        return sessions_snapshot_store.sync(
            client=self._http,
            session_id=self.session_id,
            body=AppApiV2SchemasSessionCreateSnapshotRequest(
                override_service=override_service,
                override_version=override_version,
                override_dataset=override_dataset,
            ),
            x_api_key=self._api_key,
        )

    def disk_snapshot(
        self,
        override_service: str | None = None,
        override_version: str | None = None,
        override_dataset: str | None = None,
        target: str | None = None,
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
            target: Target domain for routing (e.g., "sims.plato.so").

        Returns:
            CreateDiskSnapshotResponse with artifact_id per job_id.
        """
        self._check_closed()

        return sessions_disk_snapshot.sync(
            client=self._http,
            session_id=self.session_id,
            body=CreateDiskSnapshotRequest(
                override_service=override_service,
                override_version=override_version,
                override_dataset=override_dataset,
                target=target,
            ),
            x_api_key=self._api_key,
        )

    def connect_network(self) -> dict:
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
        result = sessions_connect_network.sync(
            client=self._http,
            session_id=self.session_id,
            x_api_key=self._api_key,
        )
        self._network_connected = True
        self._network_result = result if isinstance(result, dict) else result.model_dump()
        return result

    def add_env(
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
        response = sessions_add_job.sync(
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

        # Wait for the job to be ready if requested
        mesh_ip: str | None = None
        if wait_for_ready:
            ready_response = jobs_wait_for_ready.sync(
                client=self._http,
                job_id=job_id,
                timeout=timeout,
                x_api_key=self._api_key,
            )

            if not ready_response.ready:
                error = ready_response.error or "Unknown error"
                raise TimeoutError(f"Job {job_id} did not become ready: {error}")
            mesh_ip = ready_response.mesh_ip

        # Update internal context with the new environment
        new_env_context = EnvironmentContext(
            job_id=job_id,
            alias=env.alias,
            artifact_id=response.env.artifact_id,
            simulator=getattr(env, "simulator", None),
            is_desktop=is_desktop,
        )

        # Add to context's envs list
        if self._context.envs is None:
            self._context.envs = []
        self._context.envs.append(new_env_context)

        # Reset cached envs to force rebuild
        self._envs = None
        if wait_for_ready:
            self._connect_network_if_requested()

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
        )

        logger.debug(f"Added job {job_id} (alias={env.alias}) to session {self.session_id}")
        return new_environment

    def remove_env(self, env: Environment | str) -> None:
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
        response = sessions_remove_job.sync(
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

        logger.debug(f"Removed job {job_id} (alias={alias}) from session {self.session_id}")

    def login(
        self,
        browser: Browser,
        dataset: str = "base",
        screenshots_dir: Path | None = None,
        port: int | None = None,
    ) -> LoginResult:
        """Login to all environments and return browser context with pages.

        Creates a single browser context and one page per environment.
        Navigates each page to the environment's public URL and executes
        the login flow using the v1 SyncFlowExecutor.

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
            RuntimeError: If login fails or session contains a desktop environment.
            ImportError: If playwright is not installed.
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
            raise ImportError("The login() method requires playwright. Install it with: pip install playwright")

        context = browser.new_context()
        pages: dict[str, Page] = {}

        for env in self.envs:
            page = context.new_page()
            pages[env.alias] = page

            # Get public URL for this job
            public_url_result = jobs_public_url.sync(
                client=self._http,
                job_id=env.job_id,
                port=port,
                x_api_key=self._api_key,
            )

            if public_url_result.error:
                context.close()
                raise RuntimeError(f"Failed to get public URL for {env.alias}: {public_url_result.error}")

            if not public_url_result.url:
                context.close()
                raise RuntimeError(f"No public URL returned for {env.alias}")

            page.goto(public_url_result.url)

            # Get flows for this environment using v2 endpoint
            try:
                flows_response = jobs_get_flows.sync(
                    client=self._http,
                    job_id=env.job_id,
                    x_api_key=self._api_key,
                )
            except Exception as e:
                context.close()
                raise RuntimeError(f"Failed to get flows for env {env.alias}: {e}") from e

            if not flows_response:
                context.close()
                raise RuntimeError(f"No flows found for env {env.alias}")

            flows_list = [Flow.model_validate(f) for f in flows_response]

            # Determine flow name based on dataset
            flow_name = "login" if dataset == "base" else dataset

            login_flow = next((flow for flow in flows_list if flow.name == flow_name), None)
            if not login_flow:
                error_msg = f"No flow named '{flow_name}' found for env {env.alias}"
                context.close()
                raise RuntimeError(error_msg)

            # Execute the login flow (raises FlowExecutionError on failure)
            flow_executor = FlowExecutor(
                page,
                login_flow,
                log=logger,
                screenshots_dir=screenshots_dir,
            )
            try:
                flow_executor.execute()
            except Exception as e:
                context.close()
                raise RuntimeError(f"Login failed for env {env.alias}: {e}") from e

        return LoginResult(context=context, pages=pages)

    def heartbeat(self) -> AppApiV2SchemasSessionHeartbeatResponse:
        """Send heartbeat to keep all environments alive.

        Returns:
            Heartbeat response with results per job_id.
        """
        self._check_closed()

        return sessions_heartbeat.sync(
            client=self._http,
            session_id=self.session_id,
            x_api_key=self._api_key,
        )

    # Heartbeat management

    def _heartbeat_loop(self) -> None:
        """Background thread that periodically sends heartbeats."""
        while not self._heartbeat_stop.wait(self._heartbeat_interval):
            try:
                self.heartbeat()
                logger.debug(f"Heartbeat sent for session {self.session_id}")
            except Exception as e:
                logger.error(f"Heartbeat error for session {self.session_id}: {e}")

    def start_heartbeat(self) -> None:
        """Start the heartbeat background thread."""
        self.stop_heartbeat()
        self._heartbeat_stop.clear()
        self._heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self._heartbeat_thread.start()

    def stop_heartbeat(self) -> None:
        """Stop the heartbeat background thread."""
        if self._heartbeat_thread and self._heartbeat_thread.is_alive():
            self._heartbeat_stop.set()
            self._heartbeat_thread.join(timeout=2)
            self._heartbeat_thread = None

    # Lifecycle

    def close(self) -> None:
        """Close the session and all its environments."""
        if self._closed:
            return

        self.stop_heartbeat()

        sessions_close.sync(
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
