"""High-level Chronos SDK clients."""

from __future__ import annotations

import asyncio
import logging
import os
import time
from typing import Any

import httpx

from plato.chronos.api.events import list_session_events
from plato.chronos.api.jobs import launch_job
from plato.chronos.api.otel import (
    get_session_traces_api_otel_sessions__session_id__traces_get as get_traces_api,
)
from plato.chronos.api.sessions import (
    complete_session,
    get_session,
    get_session_artifact_download,
    get_session_envs,
    get_session_logs,
    get_session_status,
    get_session_trajectory,
    list_sessions,
)
from plato.chronos.models import (
    CompleteSessionRequest,
    LaunchJobRequest,
    LaunchJobResponse,
    LogsDownloadResponse,
    OTelSpan,
    OTelTraceResponse,
    SessionEnvsResponse,
    SessionListResponse,
    SessionLogsResponse,
    SessionResponse,
    SessionStatusResponse,
    SessionTrajectory,
    TrajectoryMetrics,
    WorldConfig,
    WorldRuntimeConfig,
)

logger = logging.getLogger(__name__)

_DEFAULT_CHRONOS_URL = "https://chronos.plato.so"


def _emit_child_session_span(session_id: str, package: str) -> None:
    """Emit an OTel span for a child session launch, if tracing is available."""
    try:
        from opentelemetry import trace

        tracer = trace.get_tracer("plato.chronos.sdk")
        with tracer.start_as_current_span("child_session.launch") as span:
            span.set_attribute("plato.child_session_id", session_id)
            span.set_attribute("plato.child_session.package", package)
    except Exception:
        pass  # OTel not available, skip silently


_TERMINAL_STATUSES = {"completed", "failed", "cancelled"}


def _normalize_tag(tag: str) -> str:
    return tag.replace("-", "_").replace(":", ".").replace(" ", "_")


class Chronos:
    """Synchronous high-level Chronos client."""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float = 60.0,
    ):
        self._base_url = (base_url or os.environ.get("CHRONOS_URL") or _DEFAULT_CHRONOS_URL).rstrip("/")
        self._api_key = api_key or os.environ.get("PLATO_API_KEY")
        self._client = httpx.Client(
            base_url=self._base_url,
            timeout=timeout,
            headers={"X-API-Key": self._api_key} if self._api_key else {},
        )

    # -- Jobs --

    def launch(
        self,
        package: str,
        config: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        runtime: dict[str, Any] | None = None,
        allow_prerelease: bool = False,
        parent_session_id: str | None = None,
    ) -> LaunchJobResponse:
        if parent_session_id is None:
            parent_session_id = os.environ.get("SESSION_ID")
        world_runtime = WorldRuntimeConfig(**runtime) if runtime else None
        body = LaunchJobRequest(
            world=WorldConfig(package=package, config=config, runtime=world_runtime),
            tags=[_normalize_tag(t) for t in tags] if tags else None,
            allow_prerelease=allow_prerelease or None,
            parent_session_id=parent_session_id,
        )
        resp = launch_job.sync(self._client, body=body)
        _emit_child_session_span(resp.session_id, package)
        return resp

    # -- Sessions --

    def get_session(self, session_id: str) -> SessionResponse:
        return get_session.sync(self._client, public_id=session_id)

    def get_status(self, session_id: str) -> SessionStatusResponse:
        return get_session_status.sync(self._client, public_id=session_id)

    def list_sessions(
        self,
        tag: str | None = None,
        status: str | None = None,
        limit: int = 50,
    ) -> SessionListResponse:
        return list_sessions.sync(self._client, tag=tag, status=status, limit=limit)

    def wait_for_completion(
        self,
        session_id: str,
        poll_interval: float = 5.0,
        timeout: float | None = None,
    ) -> SessionResponse:
        start = time.monotonic()
        while True:
            status_resp = self.get_status(session_id)
            if status_resp.status in _TERMINAL_STATUSES:
                return self.get_session(session_id)
            if timeout is not None and (time.monotonic() - start) >= timeout:
                raise TimeoutError(f"Session {session_id} did not complete within {timeout}s")
            time.sleep(poll_interval)

    def complete(
        self,
        session_id: str,
        status: str = "completed",
        result: dict[str, Any] | None = None,
        error_message: str | None = None,
    ) -> SessionResponse:
        body = CompleteSessionRequest(status=status, error_message=error_message)
        if result is not None:
            body.result = result  # extra="allow"
        return complete_session.sync(self._client, public_id=session_id, body=body)

    def stop(self, session_id: str) -> SessionResponse:
        body = CompleteSessionRequest(status="cancelled", error_message="User cancelled")
        return complete_session.sync(self._client, public_id=session_id, body=body)

    def get_logs(self, session_id: str) -> SessionLogsResponse:
        return get_session_logs.sync(self._client, public_id=session_id)

    def get_envs(self, session_id: str) -> SessionEnvsResponse:
        return get_session_envs.sync(self._client, public_id=session_id)

    # -- Artifacts --

    def get_artifact_download(self, session_id: str, key: str = "artifact") -> LogsDownloadResponse:
        return get_session_artifact_download.sync(self._client, public_id=session_id, key=key)

    # -- OTel --

    def get_traces(self, session_id: str) -> OTelTraceResponse:
        return get_traces_api.sync(self._client, session_id=session_id)

    def get_events(self, session_id: str) -> list[OTelSpan]:
        return list_session_events.sync(self._client, session_public_id=session_id).events

    # -- Trajectory --

    def get_trajectory(self, session_id: str) -> SessionTrajectory:
        return get_session_trajectory.sync(self._client, public_id=session_id)

    def get_metrics(self, session_id: str) -> TrajectoryMetrics:
        """Get aggregated cost and token metrics for a session."""
        return self.get_trajectory(session_id).total_metrics

    # -- Checkpoints --

    def get_checkpoint_info(self, session_id: str) -> dict[str, Any]:
        """Get checkpoint metadata including available workspace snapshots.

        Returns dict with: session_id, workspaces, snapshots, resumable_steps, state_keys.
        """
        resp = self._client.get(f"/api/sessions/{session_id}/checkpoint-info")
        resp.raise_for_status()
        return resp.json()

    # -- Lifecycle --

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Chronos:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncChronos:
    """Asynchronous high-level Chronos client."""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float = 60.0,
    ):
        self._base_url = (base_url or os.environ.get("CHRONOS_URL") or _DEFAULT_CHRONOS_URL).rstrip("/")
        self._api_key = api_key or os.environ.get("PLATO_API_KEY")
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=timeout,
            headers={"X-API-Key": self._api_key} if self._api_key else {},
        )

    # -- Jobs --

    async def launch(
        self,
        package: str,
        config: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        runtime: dict[str, Any] | None = None,
        allow_prerelease: bool = False,
        parent_session_id: str | None = None,
    ) -> LaunchJobResponse:
        if parent_session_id is None:
            parent_session_id = os.environ.get("SESSION_ID")
        world_runtime = WorldRuntimeConfig(**runtime) if runtime else None
        body = LaunchJobRequest(
            world=WorldConfig(package=package, config=config, runtime=world_runtime),
            tags=[_normalize_tag(t) for t in tags] if tags else None,
            allow_prerelease=allow_prerelease or None,
            parent_session_id=parent_session_id,
        )
        resp = await launch_job.asyncio(self._client, body=body)
        _emit_child_session_span(resp.session_id, package)
        return resp

    # -- Sessions --

    async def get_session(self, session_id: str) -> SessionResponse:
        return await get_session.asyncio(self._client, public_id=session_id)

    async def get_status(self, session_id: str) -> SessionStatusResponse:
        return await get_session_status.asyncio(self._client, public_id=session_id)

    async def list_sessions(
        self,
        tag: str | None = None,
        status: str | None = None,
        limit: int = 50,
    ) -> SessionListResponse:
        return await list_sessions.asyncio(self._client, tag=tag, status=status, limit=limit)

    async def wait_for_completion(
        self,
        session_id: str,
        poll_interval: float = 5.0,
        timeout: float | None = None,
    ) -> SessionResponse:
        start = time.monotonic()
        while True:
            status_resp = await self.get_status(session_id)
            elapsed = int(time.monotonic() - start)
            logger.info("Session %s: status=%s (elapsed=%ds)", session_id, status_resp.status, elapsed)
            if status_resp.status in _TERMINAL_STATUSES:
                return await self.get_session(session_id)
            if timeout is not None and (time.monotonic() - start) >= timeout:
                raise TimeoutError(f"Session {session_id} did not complete within {timeout}s")
            await asyncio.sleep(poll_interval)

    async def stop(self, session_id: str) -> SessionResponse:
        body = CompleteSessionRequest(status="cancelled", error_message="User cancelled")
        return await complete_session.asyncio(self._client, public_id=session_id, body=body)

    async def get_logs(self, session_id: str) -> SessionLogsResponse:
        return await get_session_logs.asyncio(self._client, public_id=session_id)

    async def get_envs(self, session_id: str) -> SessionEnvsResponse:
        return await get_session_envs.asyncio(self._client, public_id=session_id)

    # -- Artifacts --

    async def get_artifact_download(self, session_id: str, key: str = "artifact") -> LogsDownloadResponse:
        return await get_session_artifact_download.asyncio(self._client, public_id=session_id, key=key)

    # -- OTel --

    async def get_traces(self, session_id: str) -> OTelTraceResponse:
        return await get_traces_api.asyncio(self._client, session_id=session_id)

    async def get_events(self, session_id: str) -> list[OTelSpan]:
        resp = await list_session_events.asyncio(self._client, session_public_id=session_id)
        return resp.events

    # -- Trajectory --

    async def get_trajectory(self, session_id: str) -> SessionTrajectory:
        return await get_session_trajectory.asyncio(self._client, public_id=session_id)

    async def get_metrics(self, session_id: str) -> TrajectoryMetrics:
        """Get aggregated cost and token metrics for a session."""
        traj = await self.get_trajectory(session_id)
        return traj.total_metrics

    # -- Checkpoints --

    async def get_checkpoint_info(self, session_id: str) -> dict[str, Any]:
        """Get checkpoint metadata including available workspace snapshots.

        Returns dict with: session_id, workspaces, snapshots, resumable_steps, state_keys.
        """
        resp = await self._client.get(f"/api/sessions/{session_id}/checkpoint-info")
        resp.raise_for_status()
        return resp.json()

    # -- Lifecycle --

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> AsyncChronos:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
