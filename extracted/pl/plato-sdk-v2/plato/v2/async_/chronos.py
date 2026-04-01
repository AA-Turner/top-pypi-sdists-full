"""Plato SDK v2 - Asynchronous Chronos Client.

Provides high-level APIs for managing Chronos sessions and jobs programmatically.
"""

from __future__ import annotations

import asyncio
import logging
import os
from typing import Any

import httpx
from dotenv import load_dotenv

from plato.chronos.api.jobs import launch_job
from plato.chronos.api.sessions import (
    close_session,
    complete_session,
    get_session,
    get_session_envs,
    get_session_logs,
    get_session_status,
    get_session_trajectory,
    list_sessions,
    list_tags,
    update_session_tags,
)
from plato.chronos.models import (
    CompleteSessionRequest,
    LaunchJobRequest,
    LaunchJobResponse,
    SessionEnvsResponse,
    SessionListResponse,
    SessionLogsResponse,
    SessionResponse,
    SessionStatusResponse,
    SessionTrajectory,
    Status1,
    TagsListResponse,
    UpdateTagsRequest,
    WorldConfigInput,
)

load_dotenv()

logger = logging.getLogger(__name__)

DEFAULT_CHRONOS_URL = "https://chronos.plato.so"
DEFAULT_TIMEOUT = 120.0


class ChronosSession:
    """Wrapper for a Chronos session with convenient methods.

    Provides methods to check status, get logs, update tags, and stop the session.
    """

    def __init__(
        self,
        http_client: httpx.AsyncClient,
        api_key: str,
        session_id: str,
        plato_session_id: str | None = None,
    ):
        self._http = http_client
        self._api_key = api_key
        self._session_id = session_id
        self._plato_session_id = plato_session_id

    @property
    def session_id(self) -> str:
        """Get the Chronos session public ID."""
        return self._session_id

    @property
    def plato_session_id(self) -> str | None:
        """Get the underlying Plato session ID."""
        return self._plato_session_id

    async def get_status(self) -> SessionStatusResponse:
        """Get the current status of the session (lightweight).

        Returns:
            SessionStatusResponse with status and status_reason.
        """
        return await get_session_status.asyncio(
            client=self._http,
            public_id=self._session_id,
            x_api_key=self._api_key,
        )

    async def get_details(self) -> SessionResponse:
        """Get full session details including trajectory and world config.

        Returns:
            SessionResponse with full session details.
        """
        return await get_session.asyncio(
            client=self._http,
            public_id=self._session_id,
            x_api_key=self._api_key,
        )

    async def get_envs(self) -> SessionEnvsResponse:
        """Get environment information for this session.

        Returns:
            SessionEnvsResponse with list of environments.
        """
        return await get_session_envs.asyncio(
            client=self._http,
            public_id=self._session_id,
            x_api_key=self._api_key,
        )

    async def get_logs(
        self,
        limit: int = 10000,
        *,
        include_audit_events: bool = False,
    ) -> SessionLogsResponse:
        """Get logs for this session.

        Args:
            limit: Maximum number of log entries to return.
            include_audit_events: Include filesystem audit events keyed by span ID.

        Returns:
            SessionLogsResponse with log entries.
        """
        return await get_session_logs.asyncio(
            client=self._http,
            public_id=self._session_id,
            limit=limit,
            include_audit_events=include_audit_events,
            x_api_key=self._api_key,
        )

    async def get_trajectory(self) -> SessionTrajectory:
        """Get the session trajectory (world steps, agent traces, observations).

        The trajectory includes world step observations (e.g. artifact_ids)
        that are not included in get_details().

        Returns:
            SessionTrajectory with world steps and agent traces.
        """
        return await get_session_trajectory.asyncio(
            client=self._http,
            public_id=self._session_id,
            x_api_key=self._api_key,
        )

    async def update_tags(self, tags: list[str]) -> SessionResponse:
        """Update tags for this session.

        Args:
            tags: List of tags (use '.' for hierarchy, '_' instead of '-').

        Returns:
            Updated SessionResponse.
        """
        # Normalize tags
        normalized = [tag.replace("-", "_").replace(":", ".").replace(" ", "_") for tag in tags]
        request = UpdateTagsRequest(tags=normalized)
        return await update_session_tags.asyncio(
            client=self._http,
            public_id=self._session_id,
            body=request,
            x_api_key=self._api_key,
        )

    async def stop(self) -> SessionResponse:
        """Stop/cancel this session.

        Returns:
            Updated SessionResponse.
        """
        await close_session.asyncio(
            client=self._http,
            public_id=self._session_id,
            x_api_key=self._api_key,
        )
        return await get_session.asyncio(
            client=self._http,
            public_id=self._session_id,
            x_api_key=self._api_key,
        )

    async def complete(
        self,
        status: str = "completed",
        exit_code: int | None = None,
        error_message: str | None = None,
    ) -> SessionResponse:
        """Mark session as completed or failed.

        Args:
            status: Final status ('completed', 'failed', or 'cancelled').
            exit_code: Optional exit code from world runner.
            error_message: Error message if failed.

        Returns:
            Updated SessionResponse.
        """
        request = CompleteSessionRequest(
            status=Status1(status),
            exit_code=exit_code,
            error_message=error_message,
        )
        return await complete_session.asyncio(
            client=self._http,
            public_id=self._session_id,
            body=request,
            x_api_key=self._api_key,
        )

    async def close(self) -> None:
        """Close the Plato session (release VM resources).

        Note: This closes the underlying Plato session, not just the Chronos record.
        """
        await close_session.asyncio(
            client=self._http,
            public_id=self._session_id,
            x_api_key=self._api_key,
        )

    async def wait_until_complete(
        self,
        timeout: float = 3600.0,
        poll_interval: float = 5.0,
    ) -> SessionResponse:
        """Wait until the session reaches a terminal state.

        Args:
            timeout: Maximum time to wait in seconds.
            poll_interval: Time between status checks.

        Returns:
            Final SessionResponse. The ``result`` field contains the world's
            final observation data (e.g. artifact_ids, completion status) if
            the Chronos server supports it.

        Raises:
            TimeoutError: If session doesn't complete within timeout.
        """
        terminal_statuses = {"completed", "failed", "cancelled", "error"}
        elapsed = 0.0

        while elapsed < timeout:
            status_response = await self.get_status()
            if status_response.status in terminal_statuses:
                return await self.get_details()

            await asyncio.sleep(poll_interval)
            elapsed += poll_interval

        raise TimeoutError(f"Session {self._session_id} did not complete within {timeout} seconds")

    def __repr__(self) -> str:
        return f"ChronosSession(session_id={self._session_id!r})"


class AsyncChronos:
    """Asynchronous client for Chronos job management API.

    Provides high-level methods for launching jobs, managing sessions,
    and monitoring job status.

    Usage:
        from plato.v2.async_ import AsyncChronos

        async with AsyncChronos() as chronos:
            # Launch a job
            session = await chronos.launch(
                world_package="plato-world-computer-use",
                world_config={"task": "Navigate to google.com"},
                tags=["test", "project.my_project"],
            )

            # Wait for completion
            result = await session.wait_until_complete()
            print(f"Status: {result.status}")

            # Or poll manually
            while True:
                status = await session.get_status()
                if status.status in ("completed", "failed"):
                    break
                await asyncio.sleep(5)
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        """Initialize the Chronos client.

        Args:
            api_key: Plato API key. Falls back to PLATO_API_KEY env var.
            base_url: Chronos API base URL. Falls back to CHRONOS_URL env var.
            timeout: Request timeout in seconds.
        """
        resolved_api_key = api_key or os.environ.get("PLATO_API_KEY")
        if not resolved_api_key:
            raise ValueError("API key required. Set PLATO_API_KEY or pass api_key=")
        self._api_key: str = resolved_api_key

        url = base_url or os.environ.get("CHRONOS_URL", DEFAULT_CHRONOS_URL)
        self.base_url = url.rstrip("/")
        self.timeout = timeout

        self._http = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(timeout),
        )

    async def launch(
        self,
        world_package: str,
        world_config: dict[str, Any] | None = None,
        runtime_artifact_id: str | None = None,
        tags: list[str] | None = None,
    ) -> ChronosSession:
        """Launch a new Chronos job.

        Args:
            world_package: World package name with optional version
                (e.g., "plato-world-computer-use:0.1.0").
            world_config: Configuration passed to the world runner.
            runtime_artifact_id: Optional runtime artifact ID for cached environment.
            tags: Optional tags for organizing sessions (use '.' for hierarchy).

        Returns:
            ChronosSession for monitoring and managing the job.

        Example:
            session = await chronos.launch(
                world_package="plato-world-computer-use",
                world_config={
                    "task": "Navigate to google.com",
                    "agents": [{"name": "computer-use", "version": "latest"}],
                },
                tags=["project.my_project", "env.dev"],
            )
        """
        # Normalize tags
        normalized_tags = None
        if tags:
            normalized_tags = [tag.replace("-", "_").replace(":", ".").replace(" ", "_") for tag in tags]

        request = LaunchJobRequest(
            world=WorldConfigInput(
                package=world_package,
                config=world_config,
            ),
            tags=normalized_tags,
        )

        response: LaunchJobResponse = await launch_job.asyncio(
            client=self._http,
            body=request,
            x_api_key=self._api_key,
        )

        logger.info(f"Launched Chronos job: {response.session_id}")

        return ChronosSession(
            http_client=self._http,
            api_key=self._api_key,
            session_id=response.session_id,
            plato_session_id=response.plato_session_id,
        )

    async def get_session(self, session_id: str) -> ChronosSession:
        """Get a ChronosSession wrapper for an existing session.

        Args:
            session_id: The Chronos session public ID.

        Returns:
            ChronosSession for the specified session.
        """
        # Verify the session exists by fetching status
        await get_session_status.asyncio(
            client=self._http,
            public_id=session_id,
            x_api_key=self._api_key,
        )

        return ChronosSession(
            http_client=self._http,
            api_key=self._api_key,
            session_id=session_id,
        )

    async def list_sessions(
        self,
        tag: str | None = None,
    ) -> SessionListResponse:
        """List Chronos sessions.

        Args:
            tag: Filter by tag (fuzzy substring match).

        Returns:
            SessionListResponse with list of sessions.
        """
        return await list_sessions.asyncio(
            client=self._http,
            tag=tag,
            x_api_key=self._api_key,
        )

    async def list_tags(self) -> TagsListResponse:
        """List all unique tags across sessions.

        Returns:
            TagsListResponse with list of tags.
        """
        return await list_tags.asyncio(
            client=self._http,
            x_api_key=self._api_key,
        )

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._http.aclose()

    async def __aenter__(self) -> AsyncChronos:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
