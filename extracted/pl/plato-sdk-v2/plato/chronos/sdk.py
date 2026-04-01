"""High-level Chronos SDK clients."""

from __future__ import annotations

import asyncio
import logging
import os
import shutil
import time
from pathlib import Path
from typing import Any

import httpx

from plato.chronos.analysis import (
    SessionAnalysis,
    analyze_session,
    fetch_all_spans,
    fetch_all_spans_async,
)
from plato.chronos.api.events import list_session_events
from plato.chronos.api.jobs import launch_job
from plato.chronos.api.otel import (
    get_session_metrics_api_otel_sessions__session_id__metrics_get as get_metrics_api,
)
from plato.chronos.api.otel import (
    get_session_traces_api_otel_sessions__session_id__traces_get as get_traces_api,
)
from plato.chronos.api.reviews import (
    create_annotation_api_annotations_post as create_annotation_api,
)
from plato.chronos.api.reviews import (
    create_review_api_reviews_post as create_review_api,
)
from plato.chronos.api.reviews import (
    list_annotations_api_annotations_get as list_annotations_api,
)
from plato.chronos.api.reviews import (
    list_reviews_api_reviews_get as list_reviews_api,
)
from plato.chronos.api.sessions import (
    close_session,
    complete_session,
    get_session,
    get_session_artifact_download,
    get_session_envs,
    get_session_logs,
    get_session_status,
    get_session_trajectory,
    list_sessions,
    update_session_notes,
)
from plato.chronos.api.workspace_repos import (
    audit_events_summary as audit_events_summary_api,
)
from plato.chronos.api.workspace_repos import (
    audit_file_history as audit_file_history_api,
)
from plato.chronos.api.workspace_repos import (
    list_audit_events as list_audit_events_api,
)
from plato.chronos.experiments import AsyncExperiments, Experiments
from plato.chronos.models import (
    AnnotationResponse,
    AuditEventsListResponse,
    AuditSummaryResponse,
    CompleteSessionRequest,
    CreateAnnotationRequest,
    CreateReviewRequest,
    LaunchJobRequest,
    LaunchJobResponse,
    LogsDownloadResponse,
    OTelSpanSchema,
    OTelTraceResponse,
    ReviewResponse,
    SessionEnvsResponse,
    SessionListResponse,
    SessionLogsResponse,
    SessionMetricsResponse,
    SessionNotesPayloadInput,
    SessionResponse,
    SessionStatusResponse,
    SessionTrajectory,
    Status,
    Status1,
    TrajectoryMetrics,
    UpdateNotesRequest,
    WorldConfigInput,
    WorldRuntimeConfig,
)
from plato.chronos.models import (
    AuthorType as _AuthorType,
)
from plato.chronos.models import (
    Kind6 as _Kind6,
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


_TERMINAL_STATUSES = {Status.completed, Status.failed, Status.cancelled}


def _normalize_tag(tag: str) -> str:
    return tag.replace("-", "_").replace(":", ".").replace(" ", "_")


# ---------------------------------------------------------------------------
# Shared base
# ---------------------------------------------------------------------------


class _ChronosBase:
    """Shared logic for sync and async Chronos clients."""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float = 60.0,
    ):
        self._base_url = (base_url or os.environ.get("CHRONOS_URL") or _DEFAULT_CHRONOS_URL).rstrip("/")
        self._api_key = api_key or os.environ.get("PLATO_API_KEY")
        self._timeout = timeout

    def _build_launch_body(
        self,
        package: str,
        config: dict[str, Any] | None,
        child_worlds: dict[str, Any] | None,
        tags: list[str] | None,
        runtime: dict[str, Any] | None,
        allow_prerelease: bool,
        parent_session_id: str | None,
        world_name: str | None = None,
    ) -> LaunchJobRequest:
        if parent_session_id is None:
            parent_session_id = os.environ.get("SESSION_ID")
        world_runtime = WorldRuntimeConfig(**runtime) if runtime else None
        return LaunchJobRequest(
            world=WorldConfigInput(package=package, config=config, runtime=world_runtime, world_name=world_name),
            child_worlds=child_worlds,
            tags=[_normalize_tag(t) for t in tags] if tags else None,
            allow_prerelease=allow_prerelease or None,
            parent_session_id=parent_session_id,
        )

    def _build_complete_body(
        self,
        status: str,
        result: dict[str, Any] | None,
        error_message: str | None,
    ) -> CompleteSessionRequest:
        body = CompleteSessionRequest(status=Status1(status), error_message=error_message)
        if result is not None:
            body.result = result  # extra="allow"
        return body

    def _build_pull_workspace_plan(
        self,
        refs: list[dict[str, Any]],
        repo_name: str | None,
        step_name: str | None,
    ) -> tuple[str, dict[str, Any]]:
        """Resolve refs and pick the target ref.

        Returns (repo_name, ref_dict).
        """
        if not refs:
            raise ValueError("No workspace refs found")

        if repo_name is None:
            repo_name = refs[0]["repo_name"]

        # Always filter to the target repo
        refs = [r for r in refs if r["repo_name"] == repo_name]
        if not refs:
            raise ValueError(f"No refs for repo '{repo_name}'")

        ref = None
        if step_name:
            for r in reversed(refs):
                if r["step_name"] == step_name:
                    ref = r
                    break
            if ref is None:
                available = [r["step_name"] for r in refs]
                raise ValueError(f"No ref for step '{step_name}'. Available: {available}")
        else:
            ref = refs[-1]

        dvc_files = ref.get("dvc_files") or {}
        if not dvc_files:
            raise ValueError(
                f"Ref '{ref['step_name']}' has no DVC files — data may not have been pushed for this checkpoint."
            )

        return repo_name, ref

    _PLATO_ROOT = Path.home() / ".plato"

    @staticmethod
    def _find_dvc_bin() -> str:
        dvc_bin = shutil.which("dvc")
        if not dvc_bin:
            raise RuntimeError("dvc not found. Install with: pip install 'dvc[s3]'")
        return dvc_bin

    def _repo_root(self, repo_name: str) -> Path:
        """Single DVC repo per workspace repo: ~/.plato/workspaces/{repo_name}

        All sessions share this repo so DVC's content-addressed cache is
        maximally reused (identical files across sessions are stored once).
        """
        return self._PLATO_ROOT / "workspaces" / repo_name

    def _resolve_pull_context(
        self,
        refs: list[dict[str, Any]],
        repo_name: str | None,
        step_name: str | None,
    ) -> tuple[str, dict[str, Any], dict[str, str]]:
        """Pick the target ref and return (repo_name, ref, dvc_files)."""
        repo_name, ref = self._build_pull_workspace_plan(refs, repo_name, step_name)
        dvc_files = ref.get("dvc_files") or {}
        return repo_name, ref, dvc_files


# ---------------------------------------------------------------------------
# Synchronous client
# ---------------------------------------------------------------------------


class Chronos(_ChronosBase):
    """Synchronous high-level Chronos client."""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float = 60.0,
    ):
        super().__init__(base_url, api_key, timeout)
        self._client = httpx.Client(
            base_url=self._base_url,
            timeout=timeout,
            headers={"X-API-Key": self._api_key} if self._api_key else {},
        )
        self.experiments = Experiments(client=self._client)

    # -- Jobs --

    def launch(
        self,
        package: str,
        config: dict[str, Any] | None = None,
        child_worlds: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        runtime: dict[str, Any] | None = None,
        allow_prerelease: bool = False,
        parent_session_id: str | None = None,
        world_name: str | None = None,
    ) -> LaunchJobResponse:
        body = self._build_launch_body(
            package, config, child_worlds, tags, runtime, allow_prerelease, parent_session_id, world_name=world_name
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
            elapsed = int(time.monotonic() - start)
            logger.info("Session %s: status=%s (elapsed=%ds)", session_id, status_resp.status, elapsed)
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
        body = self._build_complete_body(status, result, error_message)
        return complete_session.sync(self._client, public_id=session_id, body=body)

    def stop(self, session_id: str) -> SessionResponse:
        close_session.sync(self._client, public_id=session_id)
        return self.get_session(session_id)

    def update_notes(
        self,
        session_id: str,
        notes: SessionNotesPayloadInput | None,
    ) -> SessionResponse:
        """Update the structured notes JSON on a session."""
        return update_session_notes.sync(
            self._client,
            public_id=session_id,
            body=UpdateNotesRequest(notes=notes),
        )

    def get_logs(
        self,
        session_id: str,
        *,
        include_audit_events: bool = False,
    ) -> SessionLogsResponse:
        return get_session_logs.sync(
            self._client,
            public_id=session_id,
            include_audit_events=include_audit_events,
        )

    def get_envs(self, session_id: str) -> SessionEnvsResponse:
        return get_session_envs.sync(self._client, public_id=session_id)

    def get_audit_events(
        self,
        session_id: str,
        *,
        step_name: str | None = None,
        repo_name: str | None = None,
        path: str | None = None,
        trace_id: str | None = None,
        span_id: str | None = None,
        agent_name: str | None = None,
        operation: str | None = None,
        limit: int = 500,
        offset: int | None = None,
    ) -> AuditEventsListResponse:
        """Query filesystem audit events for a session."""
        return list_audit_events_api.sync(
            self._client,
            session_public_id=session_id,
            step_name=step_name,
            repo_name=repo_name,
            path=path,
            trace_id=trace_id,
            span_id=span_id,
            agent_name=agent_name,
            operation=operation,
            limit=limit,
            offset=offset,
        )

    def get_audit_summary(self, session_id: str) -> AuditSummaryResponse:
        """Get aggregated filesystem audit summary for a session."""
        return audit_events_summary_api.sync(
            self._client,
            session_public_id=session_id,
        )

    def get_audit_file_history(
        self,
        session_id: str,
        *,
        path: str,
        repo_name: str,
    ) -> AuditEventsListResponse:
        """Get all audit events for a specific file across all steps."""
        return audit_file_history_api.sync(
            self._client,
            session_public_id=session_id,
            path=path,
            repo_name=repo_name,
        )

    # -- Artifacts --

    def get_artifact_download(self, session_id: str, key: str = "artifact") -> LogsDownloadResponse:
        return get_session_artifact_download.sync(self._client, public_id=session_id, key=key)

    # -- OTel --

    def get_traces(
        self,
        session_id: str,
        atif_only: bool = False,
        errors_only: bool = False,
        search: str | None = None,
    ) -> OTelTraceResponse:
        return get_traces_api.sync(
            self._client,
            session_id=session_id,
            atif_only=atif_only,
            errors_only=errors_only,
            search=search,
        )

    def get_all_traces(self, session_id: str) -> list[OTelSpanSchema]:
        """Auto-paginated: fetches ALL spans for a session."""
        return fetch_all_spans(self._client, session_id)

    def get_session_analysis(self, session_id: str) -> SessionAnalysis:
        """One-call comprehensive session analysis."""
        spans = self.get_all_traces(session_id)
        return analyze_session(spans, session_id)

    def get_session_metrics(
        self,
        session_id: str,
        env_alias: str | None = None,
    ) -> SessionMetricsResponse:
        """Get VM metrics (CPU, memory, etc.) for a session."""
        return get_metrics_api.sync(
            self._client,
            session_id=session_id,
            env_alias=env_alias,
        )

    def get_events(self, session_id: str) -> list[OTelSpanSchema]:
        return list_session_events.sync(self._client, session_public_id=session_id).events

    # -- Trajectory --

    def get_trajectory(self, session_id: str) -> SessionTrajectory:
        return get_session_trajectory.sync(self._client, public_id=session_id)

    def get_metrics(self, session_id: str) -> TrajectoryMetrics:
        """Get aggregated cost and token metrics for a session."""
        return self.get_trajectory(session_id).total_metrics

    # -- State --

    def save_state(self, session_id: str, state_data: dict[str, Any]) -> bool:
        """Save world state JSON to the DB."""
        resp = self._client.put(f"/api/sessions/{session_id}/state", json=state_data)
        return resp.status_code == 200

    def get_state(self, session_id: str) -> dict[str, Any] | None:
        """Get world state JSON from the DB. Returns None if not found."""
        resp = self._client.get(f"/api/sessions/{session_id}/state")
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.json()

    # -- Checkpoints --

    def get_checkpoint_info(self, session_id: str) -> dict[str, Any]:
        """Get checkpoint metadata including available workspace snapshots."""
        resp = self._client.get(f"/api/sessions/{session_id}/checkpoint-info")
        resp.raise_for_status()
        return resp.json()

    # -- Workspaces --

    def get_workspace_refs(
        self,
        session_id: str,
        repo_name: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get all workspace refs for a session."""
        params: dict[str, str] = {}
        if repo_name:
            params["repo_name"] = repo_name
        resp = self._client.get(
            f"/api/workspace-repos/sessions/{session_id}/workspace-refs",
            params=params,
        )
        resp.raise_for_status()
        return resp.json().get("refs", [])

    def resolve_workspace_repo(self, repo_name: str) -> dict[str, Any]:
        """Resolve a workspace repo name to S3 bucket/prefix and repo ID."""
        resp = self._client.post(
            "/api/workspace-repos/resolve",
            json={"name": repo_name},
        )
        resp.raise_for_status()
        return resp.json()

    def get_workspace_credentials(self, repo_id: str) -> dict[str, str]:
        """Get STS credentials for accessing a workspace repo's S3 data."""
        resp = self._client.post(
            f"/api/workspace-repos/{repo_id}/credentials",
        )
        resp.raise_for_status()
        data = resp.json()
        return {
            "AWS_ACCESS_KEY_ID": data["aws_access_key_id"],
            "AWS_SECRET_ACCESS_KEY": data["aws_secret_access_key"],
            "AWS_SESSION_TOKEN": data["aws_session_token"],
            "AWS_DEFAULT_REGION": data.get("region", "us-east-1"),
        }

    def pull_workspace(
        self,
        session_id: str,
        repo_name: str | None = None,
        step_name: str | None = None,
    ) -> Path:
        """Pull a workspace snapshot via DVC.

        Data is stored at ~/.plato/workspaces/{repo_name}/{session_id}/.
        A single DVC repo per workspace repo means all sessions share the
        same content-addressed cache — identical files are downloaded once.

        Args:
            session_id: Session to pull from.
            repo_name: Workspace name (e.g. "webclone/recordings"). If None,
                       uses the first repo found in the session's refs.
            step_name: Checkpoint to restore (e.g. "step.2.stage.annotate").
                       If None, uses the latest checkpoint.

        Returns:
            Path to the session's data directory.
        """
        import subprocess

        # Resolve ref and credentials
        refs = self.get_workspace_refs(session_id, repo_name=repo_name)
        repo_name, ref, dvc_files = self._resolve_pull_context(refs, repo_name, step_name)
        repo_info = self.resolve_workspace_repo(repo_name)
        creds = self.get_workspace_credentials(repo_info["repo_id"])

        repo_root = self._repo_root(repo_name)
        repo_root.mkdir(parents=True, exist_ok=True)
        session_dir = repo_root / session_id
        session_dir.mkdir(parents=True, exist_ok=True)

        env = {**os.environ, **creds, "GIT_DISCOVERY_ACROSS_FILESYSTEM": "1"}
        dvc_bin = self._find_dvc_bin()
        remote_url = f"s3://{repo_info['s3_bucket']}/{repo_info['s3_prefix']}/dvc-cache"

        def _run(*args: str) -> None:
            result = subprocess.run(args, cwd=str(repo_root), env=env, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"Command {args} failed:\n{result.stderr}")

        # Init single DVC repo for this workspace (shared across sessions)
        if not (repo_root / ".git").is_dir():
            _run("git", "init")
            _run("git", "config", "user.email", "plato@plato.so")
            _run("git", "config", "user.name", "plato")
        if not (repo_root / ".dvc").is_dir():
            _run(dvc_bin, "init")
            _run(dvc_bin, "remote", "add", "-d", "s3", remote_url)
            _run("git", "add", ".")
            _run("git", "commit", "-m", "init dvc")

        # Write .dvc pointer files under session subdir
        for name, content in dvc_files.items():
            dvc_path = session_dir / f"{name}.dvc"
            dvc_path.write_text(content)
        _run("git", "add", ".")
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(repo_root),
            env=env,
            capture_output=True,
            text=True,
        )
        if status.stdout.strip():
            _run("git", "commit", "-m", f"{session_id}: {ref['step_name']}")

        logger.info("Pulling workspace '%s' session=%s (step=%s) ...", repo_name, session_id[:8], ref["step_name"])
        _run(dvc_bin, "pull", "--force")

        data_dirs = list(dvc_files.keys())
        return session_dir / data_dirs[0] if data_dirs else session_dir

    # -- Lifecycle --

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Chronos:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


# ---------------------------------------------------------------------------
# Asynchronous client
# ---------------------------------------------------------------------------


class AsyncChronos(_ChronosBase):
    """Asynchronous high-level Chronos client."""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float = 60.0,
    ):
        super().__init__(base_url, api_key, timeout)
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=timeout,
            headers={"X-API-Key": self._api_key} if self._api_key else {},
        )
        self.experiments = AsyncExperiments(client=self._client)

    # -- Jobs --

    async def launch(
        self,
        package: str,
        config: dict[str, Any] | None = None,
        child_worlds: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        runtime: dict[str, Any] | None = None,
        allow_prerelease: bool = False,
        parent_session_id: str | None = None,
        world_name: str | None = None,
    ) -> LaunchJobResponse:
        body = self._build_launch_body(
            package, config, child_worlds, tags, runtime, allow_prerelease, parent_session_id, world_name=world_name
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

    async def complete(
        self,
        session_id: str,
        status: str = "completed",
        result: dict[str, Any] | None = None,
        error_message: str | None = None,
    ) -> SessionResponse:
        body = self._build_complete_body(status, result, error_message)
        return await complete_session.asyncio(self._client, public_id=session_id, body=body)

    async def stop(self, session_id: str) -> SessionResponse:
        await close_session.asyncio(self._client, public_id=session_id)
        return await self.get_session(session_id)

    async def update_notes(
        self,
        session_id: str,
        notes: SessionNotesPayloadInput | None,
    ) -> SessionResponse:
        """Update the structured notes JSON on a session."""
        return await update_session_notes.asyncio(
            self._client,
            public_id=session_id,
            body=UpdateNotesRequest(notes=notes),
        )

    async def get_logs(
        self,
        session_id: str,
        *,
        include_audit_events: bool = False,
    ) -> SessionLogsResponse:
        return await get_session_logs.asyncio(
            self._client,
            public_id=session_id,
            include_audit_events=include_audit_events,
        )

    async def get_envs(self, session_id: str) -> SessionEnvsResponse:
        return await get_session_envs.asyncio(self._client, public_id=session_id)

    async def get_audit_events(
        self,
        session_id: str,
        *,
        step_name: str | None = None,
        repo_name: str | None = None,
        ref_public_id: str | None = None,
        path: str | None = None,
        trace_id: str | None = None,
        span_id: str | None = None,
        agent_name: str | None = None,
        operation: str | None = None,
        limit: int = 500,
        offset: int | None = None,
    ) -> AuditEventsListResponse:
        """Query filesystem audit events for a session."""
        return await list_audit_events_api.asyncio(
            self._client,
            session_public_id=session_id,
            step_name=step_name,
            repo_name=repo_name,
            ref_public_id=ref_public_id,
            path=path,
            trace_id=trace_id,
            span_id=span_id,
            agent_name=agent_name,
            operation=operation,
            limit=limit,
            offset=offset,
        )

    async def get_audit_summary(self, session_id: str) -> AuditSummaryResponse:
        """Get aggregated filesystem audit summary for a session."""
        return await audit_events_summary_api.asyncio(
            self._client,
            session_public_id=session_id,
        )

    async def get_audit_file_history(
        self,
        session_id: str,
        *,
        path: str,
        repo_name: str,
    ) -> AuditEventsListResponse:
        """Get all audit events for a specific file across all steps."""
        return await audit_file_history_api.asyncio(
            self._client,
            session_public_id=session_id,
            path=path,
            repo_name=repo_name,
        )

    # -- Artifacts --

    async def get_artifact_download(self, session_id: str, key: str = "artifact") -> LogsDownloadResponse:
        return await get_session_artifact_download.asyncio(self._client, public_id=session_id, key=key)

    # -- OTel --

    async def get_traces(
        self,
        session_id: str,
        atif_only: bool = False,
        errors_only: bool = False,
        search: str | None = None,
    ) -> OTelTraceResponse:
        return await get_traces_api.asyncio(
            self._client,
            session_id=session_id,
            atif_only=atif_only,
            errors_only=errors_only,
            search=search,
        )

    async def get_all_traces(self, session_id: str) -> list[OTelSpanSchema]:
        """Auto-paginated: fetches ALL spans for a session."""
        return await fetch_all_spans_async(self._client, session_id)

    async def get_session_analysis(self, session_id: str) -> SessionAnalysis:
        """One-call comprehensive session analysis."""
        spans = await self.get_all_traces(session_id)
        return analyze_session(spans, session_id)

    async def get_session_metrics(
        self,
        session_id: str,
        env_alias: str | None = None,
    ) -> SessionMetricsResponse:
        """Get VM metrics (CPU, memory, etc.) for a session."""
        return await get_metrics_api.asyncio(
            self._client,
            session_id=session_id,
            env_alias=env_alias,
        )

    async def get_events(self, session_id: str) -> list[OTelSpanSchema]:
        resp = await list_session_events.asyncio(self._client, session_public_id=session_id)
        return resp.events

    # -- Trajectory --

    async def get_trajectory(self, session_id: str) -> SessionTrajectory:
        return await get_session_trajectory.asyncio(self._client, public_id=session_id)

    async def get_metrics(self, session_id: str) -> TrajectoryMetrics:
        """Get aggregated cost and token metrics for a session."""
        traj = await self.get_trajectory(session_id)
        return traj.total_metrics

    # -- Reviews & Annotations --

    async def create_review(
        self,
        session_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        tags: list[str] | None = None,
        review_type: str | None = None,
        author_type: str = "agent",
        analyzer_session_id: str | None = None,
        scores: dict[str, float] | None = None,
    ) -> ReviewResponse:
        """Create a review on a session."""
        from plato.chronos.models import ReviewType as _ReviewType

        body = CreateReviewRequest(
            session_id=session_id,
            name=name,
            description=description,
            tags=tags,
            review_type=_ReviewType(review_type) if review_type else None,
            author_type=_AuthorType(author_type),
            analyzer_session_id=analyzer_session_id,
            scores=scores,
        )
        return await create_review_api.asyncio(self._client, body=body)

    async def update_review(
        self,
        review_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        tags: list[str] | None = None,
        scores: dict[str, float] | None = None,
    ) -> ReviewResponse:
        """Update an existing review."""
        from plato.chronos.api.reviews import (
            update_review_api_reviews__review_public_id__put as update_review_api,
        )
        from plato.chronos.models import UpdateReviewRequest

        body = UpdateReviewRequest(
            name=name,
            description=description,
            tags=tags,
            scores=scores,
        )
        return await update_review_api.asyncio(self._client, review_public_id=review_id, body=body)

    async def list_reviews(
        self,
        session_id: str,
        *,
        tags: list[str] | None = None,
        author_type: str | None = None,
        analyzer_session_id: str | None = None,
    ) -> list[ReviewResponse]:
        """List reviews for a session."""
        resp = await list_reviews_api.asyncio(
            self._client,
            session_id=session_id,
            tags=tags,
            author_type=author_type,
            analyzer_session_id=analyzer_session_id,
        )
        return resp.reviews if hasattr(resp, "reviews") else []

    async def create_annotation(
        self,
        session_id: str,
        *,
        kind: str = "observation",
        content: str = "",
        review_id: str | None = None,
        signal: str | None = None,
        tags: list[str] | None = None,
        span_ids: list[str] | None = None,
        data: dict[str, Any] | None = None,
        author_type: str = "agent",
    ) -> AnnotationResponse:
        """Create an annotation on a session."""
        from plato.chronos.models import AnnotationTarget
        from plato.chronos.models import Type as _TargetType

        targets = [AnnotationTarget(type=_TargetType.span, span_id=sid) for sid in (span_ids or [])]
        body = CreateAnnotationRequest(
            session_id=session_id,
            kind=_Kind6(kind),
            content=content,
            review_id=review_id,
            signal=signal,
            tags=tags or [],
            targets=targets or None,
            data=data,
            author_type=_AuthorType(author_type),
        )
        return await create_annotation_api.asyncio(self._client, body=body)

    async def list_annotations(
        self,
        session_id: str,
        *,
        review_id: str | None = None,
    ) -> list[AnnotationResponse]:
        """List annotations for a session, optionally filtered by review."""
        params: dict[str, str] = {"session_id": session_id}
        if review_id:
            params["review_id"] = review_id
        resp = await list_annotations_api.asyncio(self._client, **params)
        return resp.annotations if hasattr(resp, "annotations") else []

    # -- State --

    async def save_state(self, session_id: str, state_data: dict[str, Any]) -> bool:
        """Save world state JSON to the DB."""
        resp = await self._client.put(f"/api/sessions/{session_id}/state", json=state_data)
        return resp.status_code == 200

    async def get_state(self, session_id: str) -> dict[str, Any] | None:
        """Get world state JSON from the DB. Returns None if not found."""
        resp = await self._client.get(f"/api/sessions/{session_id}/state")
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.json()

    # -- Checkpoints --

    async def get_checkpoint_info(self, session_id: str) -> dict[str, Any]:
        """Get checkpoint metadata including available workspace snapshots."""
        resp = await self._client.get(f"/api/sessions/{session_id}/checkpoint-info")
        resp.raise_for_status()
        return resp.json()

    # -- Workspaces --

    async def get_workspace_refs(
        self,
        session_id: str,
        repo_name: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get all workspace refs for a session."""
        params: dict[str, str] = {}
        if repo_name:
            params["repo_name"] = repo_name
        resp = await self._client.get(
            f"/api/workspace-repos/sessions/{session_id}/workspace-refs",
            params=params,
        )
        resp.raise_for_status()
        return resp.json().get("refs", [])

    async def resolve_workspace_repo(self, repo_name: str) -> dict[str, Any]:
        """Resolve a workspace repo name to S3 bucket/prefix and repo ID."""
        resp = await self._client.post(
            "/api/workspace-repos/resolve",
            json={"name": repo_name},
        )
        resp.raise_for_status()
        return resp.json()

    async def get_workspace_credentials(self, repo_id: str) -> dict[str, str]:
        """Get STS credentials for accessing a workspace repo's S3 data."""
        resp = await self._client.post(
            f"/api/workspace-repos/{repo_id}/credentials",
        )
        resp.raise_for_status()
        data = resp.json()
        return {
            "AWS_ACCESS_KEY_ID": data["aws_access_key_id"],
            "AWS_SECRET_ACCESS_KEY": data["aws_secret_access_key"],
            "AWS_SESSION_TOKEN": data["aws_session_token"],
            "AWS_DEFAULT_REGION": data.get("region", "us-east-1"),
        }

    async def pull_workspace(
        self,
        session_id: str,
        repo_name: str | None = None,
        step_name: str | None = None,
    ) -> Path:
        """Pull a workspace snapshot via DVC.

        Data is stored at ~/.plato/workspaces/{repo_name}/{session_id}/.
        A single DVC repo per workspace repo means all sessions share the
        same content-addressed cache — identical files are downloaded once.

        Args:
            session_id: Session to pull from.
            repo_name: Workspace name (e.g. "webclone/recordings"). If None,
                       uses the first repo found in the session's refs.
            step_name: Checkpoint to restore (e.g. "step.2.stage.annotate").
                       If None, uses the latest checkpoint.

        Returns:
            Path to the session's data directory.
        """
        # Resolve ref and credentials
        refs = await self.get_workspace_refs(session_id, repo_name=repo_name)
        repo_name, ref, dvc_files = self._resolve_pull_context(refs, repo_name, step_name)
        repo_info = await self.resolve_workspace_repo(repo_name)
        creds = await self.get_workspace_credentials(repo_info["repo_id"])

        repo_root = self._repo_root(repo_name)
        repo_root.mkdir(parents=True, exist_ok=True)
        session_dir = repo_root / session_id
        session_dir.mkdir(parents=True, exist_ok=True)

        env = {**os.environ, **creds, "GIT_DISCOVERY_ACROSS_FILESYSTEM": "1"}
        dvc_bin = self._find_dvc_bin()
        remote_url = f"s3://{repo_info['s3_bucket']}/{repo_info['s3_prefix']}/dvc-cache"

        async def _run(*args: str) -> None:
            proc = await asyncio.create_subprocess_exec(
                *args,
                cwd=str(repo_root),
                env=env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            _, stderr = await proc.communicate()
            if proc.returncode != 0:
                raise RuntimeError(f"Command {args} failed:\n{stderr.decode()}")

        # Init single DVC repo for this workspace (shared across sessions)
        if not (repo_root / ".git").is_dir():
            await _run("git", "init")
            await _run("git", "config", "user.email", "plato@plato.so")
            await _run("git", "config", "user.name", "plato")
        if not (repo_root / ".dvc").is_dir():
            await _run(dvc_bin, "init")
            await _run(dvc_bin, "remote", "add", "-d", "s3", remote_url)
            await _run("git", "add", ".")
            await _run("git", "commit", "-m", "init dvc")

        # Write .dvc pointer files under session subdir
        for name, content in dvc_files.items():
            dvc_path = session_dir / f"{name}.dvc"
            dvc_path.write_text(content)
        await _run("git", "add", ".")

        # Only commit if there are changes
        proc = await asyncio.create_subprocess_exec(
            "git",
            "status",
            "--porcelain",
            cwd=str(repo_root),
            env=env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await proc.communicate()
        if stdout.decode().strip():
            await _run("git", "commit", "-m", f"{session_id}: {ref['step_name']}")

        logger.info("Pulling workspace '%s' session=%s (step=%s) ...", repo_name, session_id[:8], ref["step_name"])
        await _run(dvc_bin, "pull", "--force")

        data_dirs = list(dvc_files.keys())
        return session_dir / data_dirs[0] if data_dirs else session_dir

    # -- Lifecycle --

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> AsyncChronos:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
