from __future__ import annotations

import asyncio
import logging
import time
import uuid
from collections.abc import AsyncIterator, Callable
from typing import TYPE_CHECKING, Any, TypeAlias, cast
from urllib.parse import urlencode

from capsule_sdk._errors import (
    CapsuleAllocationTimeoutError,
    CapsuleConnectionError,
    CapsuleNotFound,
    CapsuleOperationTimeoutError,
    CapsuleRateLimited,
    CapsuleRequestTimeoutError,
    CapsuleRunnerUnavailableError,
    CapsuleServiceUnavailable,
)
from capsule_sdk._http_async import AsyncHttpClient, RetryPolicy
from capsule_sdk._shell_async import AsyncShellSession
from capsule_sdk.async_runner_session import AsyncRunnerSession
from capsule_sdk.models.file import (
    FileListResult,
    FileMkdirResult,
    FileReadResult,
    FileRemoveResult,
    FileStatResult,
    FileUploadResult,
    FileWriteResult,
)
from capsule_sdk.models.layered_config import CreateConfigResponse, LayeredConfigDetail, StoredLayeredConfig
from capsule_sdk.models.runner import (
    AllocateRunnerResponse,
    ExecEvent,
    ForkResult,
    PauseResult,
    RewindResult,
    Runner,
    RunnerListResponse,
    RunnerStatus,
)
from capsule_sdk.models.workload import ResolvedWorkloadRef, WorkloadSummary

if TYPE_CHECKING:
    from capsule_sdk.resources.async_layered_configs import AsyncLayeredConfigs
    from capsule_sdk.runner_config import RunnerConfig

_RunnerList: TypeAlias = list[Runner]
_ExecArgv: TypeAlias = list[str]

_ALLOCATE_REQUEST_RETRY_POLICY = RetryPolicy(
    max_retries=0,
    retry_status_codes=frozenset(),
    retry_transport_errors=False,
    retry_timeouts=False,
)
_HOST_READ_RETRY_ERRORS = (
    CapsuleConnectionError,
    CapsuleRequestTimeoutError,
    CapsuleServiceUnavailable,
)
_WAIT_RETRY_ERRORS = (
    CapsuleConnectionError,
    CapsuleNotFound,
    CapsuleRateLimited,
    CapsuleRequestTimeoutError,
    CapsuleServiceUnavailable,
)
_TERMINAL_RUNNER_STATUSES = {"terminated", "unavailable", "quarantined", "suspended", "paused"}
logger = logging.getLogger(__name__)


class AsyncRunners:
    """Async runner management: control plane + host agent operations."""

    def __init__(
        self,
        http: AsyncHttpClient,
        layered_configs: AsyncLayeredConfigs | None = None,
    ) -> None:
        self._http = http
        self._layered_configs = layered_configs
        self._host_cache: dict[str, str] = {}

    def set_host_cache(self, session_id: str, host_address: str) -> None:
        self._host_cache[session_id] = host_address

    async def allocate(
        self,
        workload: (
            str
            | CreateConfigResponse
            | StoredLayeredConfig
            | LayeredConfigDetail
            | RunnerConfig
            | WorkloadSummary
            | ResolvedWorkloadRef
        ),
        *,
        request_id: str | None = None,
        labels: dict[str, str] | None = None,
        session_id: str | None = None,
        network_policy_preset: str | None = None,
        network_policy_json: str | None = None,
        proxy_token: str | None = None,
        startup_timeout: float | None = None,
        retry_poll_interval: float = 1.0,
    ) -> AllocateRunnerResponse:
        workload_ref = await self._resolve_workload_ref(workload)
        workload_key = workload_ref.workload_key
        if not workload_key:
            raise CapsuleNotFound("Could not resolve workload key for runner allocation.")
        stable_request_id = request_id or str(uuid.uuid4())
        body: dict[str, Any] = {
            "workload_key": workload_key,
            "request_id": stable_request_id,
        }
        if workload_ref.config_id:
            body["config_id"] = workload_ref.config_id
        if labels:
            body["labels"] = labels
        if session_id:
            body["session_id"] = session_id
        if network_policy_preset:
            body["network_policy_preset"] = network_policy_preset
        if network_policy_json:
            body["network_policy_json"] = network_policy_json
        if proxy_token:
            body["proxy_token"] = proxy_token

        budget = self._resolve_startup_timeout(startup_timeout)

        data = await self._http.post(
            "/api/v1/runners/allocate",
            json_body=body,
            request_id=stable_request_id,
            retry_policy=_ALLOCATE_REQUEST_RETRY_POLICY,
        )
        resp = AllocateRunnerResponse.model_validate(data)
        if resp.host_address and resp.session_id:
            self._host_cache[resp.session_id] = resp.host_address
        _ = budget
        return resp

    async def status(self, runner_id: str | None = None, *, session_id: str | None = None) -> RunnerStatus:
        params: dict[str, str] = {}
        if session_id:
            params["session_id"] = session_id
        elif runner_id:
            params["runner_id"] = runner_id
        else:
            raise ValueError("runner_id or session_id is required")
        data = await self._http.get("/api/v1/runners/status", params=params)
        result = RunnerStatus.model_validate(data)
        if result.host_address:
            key = session_id or result.runner_id
            self._host_cache[key] = result.host_address
        return result

    async def list(self) -> _RunnerList:
        data = await self._http.get("/api/v1/runners")
        return RunnerListResponse.model_validate(data).runners

    async def release(self, runner_id: str | None = None, *, session_id: str | None = None) -> bool:
        body: dict[str, str] = {}
        if session_id:
            body["session_id"] = session_id
        elif runner_id:
            body["runner_id"] = runner_id
        else:
            raise ValueError("runner_id or session_id is required")
        data = await self._http.post("/api/v1/runners/release", json_body=body)
        cache_key = session_id or runner_id or ""
        self._host_cache.pop(cache_key, None)
        return bool(data.get("success", False))

    async def pause(
        self,
        runner_id: str | None = None,
        *,
        sync_fs: bool = False,
        session_id: str | None = None,
    ) -> PauseResult:
        body: dict[str, Any] = {}
        if session_id:
            body["session_id"] = session_id
        elif runner_id:
            body["runner_id"] = runner_id
        else:
            raise ValueError("runner_id or session_id is required")
        if sync_fs:
            body["sync_fs"] = True
        data = await self._http.post("/api/v1/runners/pause", json_body=body)
        return PauseResult.model_validate(data)

    async def fork(
        self,
        source_session_id: str,
        turn_id: int,
        *,
        fork_session_id: str | None = None,
        request_id: str | None = None,
    ) -> ForkResult:
        body: dict[str, Any] = {
            "source_session_id": source_session_id,
            "turn_id": turn_id,
        }
        if fork_session_id:
            body["fork_session_id"] = fork_session_id
        if request_id:
            body["request_id"] = request_id
        data = await self._http.post("/api/v1/runners/fork", json_body=body)
        return ForkResult.model_validate(data)

    async def rewind(
        self,
        session_id: str,
        turn_id: int,
        *,
        request_id: str | None = None,
    ) -> RewindResult:
        body: dict[str, Any] = {
            "session_id": session_id,
            "turn_id": turn_id,
        }
        if request_id:
            body["request_id"] = request_id
        data = await self._http.post("/api/v1/runners/rewind", json_body=body)
        return RewindResult.model_validate(data)

    async def quarantine(
        self,
        runner_id: str,
        *,
        reason: str | None = None,
        block_egress: bool = True,
        pause_vm: bool = True,
    ) -> dict[str, Any]:
        params: dict[str, str] = {"runner_id": runner_id}
        if reason:
            params["reason"] = reason
        params["block_egress"] = str(block_egress).lower()
        params["pause_vm"] = str(pause_vm).lower()
        return await self._http.post("/api/v1/runners/quarantine?" + urlencode(params))

    async def unquarantine(
        self,
        runner_id: str,
        *,
        unblock_egress: bool = True,
        resume_vm: bool = True,
    ) -> dict[str, Any]:
        params: dict[str, str] = {
            "runner_id": runner_id,
            "unblock_egress": str(unblock_egress).lower(),
            "resume_vm": str(resume_vm).lower(),
        }
        return await self._http.post("/api/v1/runners/unquarantine?" + urlencode(params))

    async def wait_ready(
        self,
        runner_id: str,
        *,
        timeout: float | None = None,
        poll_interval: float = 2.0,
    ) -> RunnerStatus:
        budget = self._resolve_startup_timeout(timeout)
        deadline = time.monotonic() + budget
        attempt = 0
        last_error: Exception | None = None

        while time.monotonic() < deadline:
            try:
                result = await self.status(runner_id)
            except _WAIT_RETRY_ERRORS as exc:
                last_error = exc
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    break
                delay = min(self._retry_delay(exc, attempt, poll_interval), remaining)
                logger.debug(
                    "Retrying wait_ready for runner %s after %r (attempt=%s, delay=%.2fs)",
                    runner_id,
                    exc,
                    attempt + 1,
                    delay,
                )
                await asyncio.sleep(delay)
                attempt += 1
                continue

            if result.status == "ready":
                return result
            if result.error:
                raise CapsuleRunnerUnavailableError(
                    result.error,
                    runner_id=runner_id,
                    status=result.status,
                )
            if result.status in _TERMINAL_RUNNER_STATUSES:
                raise CapsuleRunnerUnavailableError(
                    f"Runner {runner_id} entered terminal state {result.status!r}",
                    runner_id=runner_id,
                    status=result.status,
                )
            await asyncio.sleep(poll_interval)
        detail = f" Last error: {last_error}" if last_error else ""
        raise CapsuleOperationTimeoutError(
            f"Runner {runner_id} did not become ready within {budget}s.{detail}",
            runner_id=runner_id,
            timeout=budget,
            operation="wait_ready",
        )

    async def allocate_ready(
        self,
        workload: (
            str
            | CreateConfigResponse
            | StoredLayeredConfig
            | LayeredConfigDetail
            | RunnerConfig
            | WorkloadSummary
            | ResolvedWorkloadRef
        ),
        *,
        request_id: str | None = None,
        labels: dict[str, str] | None = None,
        session_id: str | None = None,
        network_policy_preset: str | None = None,
        network_policy_json: str | None = None,
        proxy_token: str | None = None,
        startup_timeout: float | None = None,
        poll_interval: float = 2.0,
    ) -> AsyncRunnerSession:
        workload_ref = await self._resolve_workload_ref(workload)
        workload_key = workload_ref.workload_key
        if not workload_key:
            raise CapsuleNotFound("Could not resolve workload key for runner allocation.")
        budget = self._resolve_startup_timeout(startup_timeout)
        deadline = time.monotonic() + budget
        alloc = await self.allocate(
            workload_ref,
            request_id=request_id,
            labels=labels,
            session_id=session_id,
            network_policy_preset=network_policy_preset,
            network_policy_json=network_policy_json,
            proxy_token=proxy_token,
            startup_timeout=max(deadline - time.monotonic(), 0.0),
            retry_poll_interval=min(1.0, poll_interval),
        )
        session = AsyncRunnerSession(
            self,
            alloc.runner_id,
            host_address=alloc.host_address,
            session_id=alloc.session_id,
            request_id=alloc.request_id,
        )
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise CapsuleAllocationTimeoutError(
                f"Timed out before runner {alloc.runner_id} became ready.",
                workload_key=workload_key,
                request_id=alloc.request_id,
                timeout=budget,
            )
        try:
            await session.wait_ready(timeout=remaining, poll_interval=poll_interval)
        except CapsuleOperationTimeoutError as exc:
            raise CapsuleAllocationTimeoutError(
                f"Timed out waiting for runner {alloc.runner_id} to become ready.",
                workload_key=workload_key,
                request_id=alloc.request_id,
                timeout=budget,
            ) from exc
        return session

    async def resume(
        self,
        session_id: str,
        *,
        proxy_token: str | None = None,
        startup_timeout: float | None = None,
        poll_interval: float = 2.0,
    ) -> AsyncRunnerSession:
        """Resume a previously paused session.

        The control plane looks up the session's workload_key from
        session_snapshots, so the caller doesn't need to provide a config
        or workload key.

        Args:
            session_id: Session ID from a previous pause.
            proxy_token: QE-minted credential broker sandbox token.
            startup_timeout: Max seconds to wait for the runner to be ready.
            poll_interval: Polling interval for readiness check.

        Returns:
            AsyncRunnerSession connected to the resumed runner.
        """
        budget = self._resolve_startup_timeout(startup_timeout)
        deadline = time.monotonic() + budget

        stable_request_id = str(uuid.uuid4())
        body: dict[str, Any] = {
            "session_id": session_id,
            "request_id": stable_request_id,
        }
        if proxy_token:
            body["proxy_token"] = proxy_token

        data = await self._http.post(
            "/api/v1/runners/allocate",
            json_body=body,
            request_id=stable_request_id,
            retry_policy=_ALLOCATE_REQUEST_RETRY_POLICY,
        )
        resp = AllocateRunnerResponse.model_validate(data)
        if resp.host_address and resp.session_id:
            self._host_cache[resp.session_id] = resp.host_address

        session = AsyncRunnerSession(
            self,
            resp.runner_id,
            host_address=resp.host_address,
            session_id=resp.session_id,
            request_id=resp.request_id,
        )
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise CapsuleAllocationTimeoutError(
                f"Timed out before resumed runner {resp.runner_id} became ready.",
                workload_key="",
                request_id=resp.request_id,
                timeout=budget,
            )
        try:
            await session.wait_ready(timeout=remaining, poll_interval=poll_interval)
        except CapsuleOperationTimeoutError as exc:
            raise CapsuleAllocationTimeoutError(
                f"Runner {resp.runner_id} resumed but did not become ready within {budget}s.",
                workload_key="",
                request_id=resp.request_id,
                timeout=budget,
            ) from exc
        return session

    async def from_config(
        self,
        workload: (
            str
            | CreateConfigResponse
            | StoredLayeredConfig
            | LayeredConfigDetail
            | RunnerConfig
            | WorkloadSummary
            | ResolvedWorkloadRef
        ),
        *,
        request_id: str | None = None,
        labels: dict[str, str] | None = None,
        session_id: str | None = None,
        network_policy_preset: str | None = None,
        network_policy_json: str | None = None,
        proxy_token: str | None = None,
        startup_timeout: float | None = None,
        wait_ready: bool = True,
        poll_interval: float = 2.0,
    ) -> AsyncRunnerSession:
        if wait_ready:
            return await self.allocate_ready(
                workload,
                request_id=request_id,
                labels=labels,
                session_id=session_id,
                network_policy_preset=network_policy_preset,
                network_policy_json=network_policy_json,
                proxy_token=proxy_token,
                startup_timeout=startup_timeout,
                poll_interval=poll_interval,
            )

        alloc = await self.allocate(
            workload,
            request_id=request_id,
            labels=labels,
            session_id=session_id,
            network_policy_preset=network_policy_preset,
            network_policy_json=network_policy_json,
            proxy_token=proxy_token,
            startup_timeout=startup_timeout,
        )
        return AsyncRunnerSession(
            self,
            alloc.runner_id,
            host_address=alloc.host_address,
            session_id=alloc.session_id,
            request_id=alloc.request_id,
        )

    async def file_download(self, session_id: str, path: str) -> bytes:
        return await self._with_host_read_retry(
            session_id,
            lambda host, hdrs: self._http.get_bytes(
                f"/api/v1/sessions/{session_id}/files/download",
                base_url=host,
                params={"path": path},
                extra_headers=hdrs,
            ),
        )

    async def file_upload(
        self,
        session_id: str,
        path: str,
        data: bytes,
        *,
        mode: str = "overwrite",
        perm: str | None = None,
    ) -> FileUploadResult:
        host, hdrs = await self._resolve_host_route(session_id)
        params: dict[str, str] = {"path": path, "mode": mode}
        if perm is not None:
            params["perm"] = perm
        return FileUploadResult.model_validate(
            await self._http.post_bytes(
                f"/api/v1/sessions/{session_id}/files/upload",
                data=data,
                base_url=host,
                params=params,
                extra_headers=hdrs,
            )
        )

    async def file_read(
        self,
        session_id: str,
        path: str,
        *,
        offset: int = 0,
        limit: int | None = None,
    ) -> FileReadResult:
        body: dict[str, Any] = {"path": path, "offset": offset}
        if limit is not None:
            body["limit"] = limit
        return FileReadResult.model_validate(
            await self._with_host_read_retry(
                session_id,
                lambda host, hdrs: self._http.post_to_host(
                    f"/api/v1/sessions/{session_id}/files/read",
                    json_body=body,
                    base_url=host,
                    extra_headers=hdrs,
                ),
            )
        )

    async def file_write(
        self,
        session_id: str,
        path: str,
        content: str,
        *,
        mode: str = "overwrite",
    ) -> FileWriteResult:
        host, hdrs = await self._resolve_host_route(session_id)
        return FileWriteResult.model_validate(
            await self._http.post_to_host(
                f"/api/v1/sessions/{session_id}/files/write",
                json_body={"path": path, "content": content, "mode": mode},
                base_url=host,
                extra_headers=hdrs,
            )
        )

    async def file_list(self, session_id: str, path: str, *, recursive: bool = False) -> FileListResult:
        return FileListResult.model_validate(
            await self._with_host_read_retry(
                session_id,
                lambda host, hdrs: self._http.post_to_host(
                    f"/api/v1/sessions/{session_id}/files/list",
                    json_body={"path": path, "recursive": recursive},
                    base_url=host,
                    extra_headers=hdrs,
                ),
            )
        )

    async def file_stat(self, session_id: str, path: str) -> FileStatResult:
        return FileStatResult.model_validate(
            await self._with_host_read_retry(
                session_id,
                lambda host, hdrs: self._http.post_to_host(
                    f"/api/v1/sessions/{session_id}/files/stat",
                    json_body={"path": path},
                    base_url=host,
                    extra_headers=hdrs,
                ),
            )
        )

    async def file_remove(self, session_id: str, path: str, *, recursive: bool = False) -> FileRemoveResult:
        host, hdrs = await self._resolve_host_route(session_id)
        return FileRemoveResult.model_validate(
            await self._http.post_to_host(
                f"/api/v1/sessions/{session_id}/files/remove",
                json_body={"path": path, "recursive": recursive},
                base_url=host,
                extra_headers=hdrs,
            )
        )

    async def file_mkdir(self, session_id: str, path: str) -> FileMkdirResult:
        host, hdrs = await self._resolve_host_route(session_id)
        return FileMkdirResult.model_validate(
            await self._http.post_to_host(
                f"/api/v1/sessions/{session_id}/files/mkdir",
                json_body={"path": path},
                base_url=host,
                extra_headers=hdrs,
            )
        )

    def shell(
        self,
        session_id: str,
        *,
        command: str | None = None,
        cols: int = 80,
        rows: int = 24,
    ) -> AsyncShellSession:
        query: dict[str, int | str] = {"cols": cols, "rows": rows}
        if command:
            query["command"] = command
        return AsyncShellSession(
            connect_url_factory=lambda: self._build_shell_ws_url(session_id, query),
            reconnect_url_factory=lambda: self._refresh_shell_ws_url(session_id, query),
            connect_timeout=self._http.operation_timeout,
        )

    async def exec(
        self,
        session_id: str,
        command: _ExecArgv,
        *,
        env: dict[str, str] | None = None,
        working_dir: str | None = None,
        timeout_seconds: int | None = None,
        proxy_token: str | None = None,
    ) -> AsyncIterator[ExecEvent]:
        body: dict[str, Any] = {"command": command}
        if env:
            body["env"] = env
        if working_dir:
            body["working_dir"] = working_dir
        if timeout_seconds:
            body["timeout_seconds"] = timeout_seconds
        if proxy_token:
            body["proxy_token"] = proxy_token

        async for event in self._exec_with_host_retry(session_id, body):
            yield event

    async def _resolve_host(self, session_id: str) -> str:
        if session_id in self._host_cache:
            return self._http.ensure_scheme(self._host_cache[session_id])
        result = await self.status(session_id=session_id)
        if result.host_address:
            self._host_cache[session_id] = result.host_address
            return self._http.ensure_scheme(result.host_address)
        raise CapsuleServiceUnavailable(f"No host address available for session {session_id}")

    async def _resolve_host_route(self, session_id: str) -> tuple[str, dict[str, str]]:
        """Return (base_url, extra_headers) for data plane calls."""
        host = await self._resolve_host(session_id)
        return self._http.resolve_data_plane_target(host)

    async def _exec_with_host_retry(self, session_id: str, body: dict[str, Any]) -> AsyncIterator[ExecEvent]:
        host, hdrs = await self._resolve_host_route(session_id)
        url = f"/api/v1/sessions/{session_id}/exec"

        received_any = False
        try:
            async for event_dict in self._http.post_stream_ndjson(
                url,
                json_body=body,
                base_url=host,
                extra_headers=hdrs,
            ):
                received_any = True
                yield ExecEvent.model_validate(event_dict)
            return
        except CapsuleServiceUnavailable:
            if received_any:
                raise
            self._host_cache.pop(session_id, None)
            new_host, new_hdrs = await self._resolve_host_route(session_id)
            async for event_dict in self._http.post_stream_ndjson(
                url,
                json_body=body,
                base_url=new_host,
                extra_headers=new_hdrs,
            ):
                yield ExecEvent.model_validate(event_dict)

    def _resolve_startup_timeout(self, timeout: float | None) -> float:
        return self._http.startup_timeout if timeout is None else timeout

    async def _resolve_workload_ref(
        self,
        workload: (
            str
            | CreateConfigResponse
            | StoredLayeredConfig
            | LayeredConfigDetail
            | RunnerConfig
            | WorkloadSummary
            | ResolvedWorkloadRef
        ),
    ) -> ResolvedWorkloadRef:
        if isinstance(workload, ResolvedWorkloadRef):
            return workload

        if hasattr(workload, "leaf_workload_key"):
            value = cast(Any, workload).leaf_workload_key
            if isinstance(value, str) and value:
                return ResolvedWorkloadRef(
                    display_name=cast(Any, workload).display_name if hasattr(workload, "display_name") else None,
                    config_id=cast(Any, workload).config_id if hasattr(workload, "config_id") else None,
                    workload_key=value,
                )

        if self._layered_configs is None:
            if isinstance(workload, str):
                return ResolvedWorkloadRef(display_name=workload, workload_key=workload)
            raise CapsuleNotFound(
                "This runner client cannot resolve workload references without layered config support."
            )

        try:
            return await self._layered_configs.resolve_workload_ref(workload)
        except CapsuleNotFound:
            if isinstance(workload, str):
                return ResolvedWorkloadRef(display_name=workload, workload_key=workload)
            raise

    async def _with_host_read_retry(self, session_id: str, op: Callable[[str, dict[str, str]], Any]) -> Any:
        host, hdrs = await self._resolve_host_route(session_id)
        try:
            result = op(host, hdrs)
            if asyncio.isfuture(result) or hasattr(result, "__await__"):
                return await result
            return result
        except _HOST_READ_RETRY_ERRORS:
            self._host_cache.pop(session_id, None)
            logger.debug("Retrying host read operation after refreshing host for session %s", session_id)
            host2, hdrs2 = await self._resolve_host_route(session_id)
            retry_result = op(host2, hdrs2)
            if asyncio.isfuture(retry_result) or hasattr(retry_result, "__await__"):
                return await retry_result
            return retry_result

    def _retry_delay(self, exc: Exception, attempt: int, poll_interval: float) -> float:
        retry_after = getattr(exc, "retry_after", None)
        if isinstance(retry_after, int | float) and retry_after > 0:
            return float(retry_after)
        return max(poll_interval, min(5.0, poll_interval * (2**attempt)))

    async def _build_shell_ws_url(self, session_id: str, query: dict[str, int | str]) -> str:
        host = await self._resolve_host(session_id)
        qs = urlencode(query)
        scheme = "wss" if host.startswith("https://") else "ws"
        host_addr = host.replace("https://", "").replace("http://", "")
        return f"{scheme}://{host_addr}/api/v1/sessions/{session_id}/pty?{qs}"

    async def _refresh_shell_ws_url(self, session_id: str, query: dict[str, int | str]) -> str:
        self._host_cache.pop(session_id, None)
        return await self._build_shell_ws_url(session_id, query)
