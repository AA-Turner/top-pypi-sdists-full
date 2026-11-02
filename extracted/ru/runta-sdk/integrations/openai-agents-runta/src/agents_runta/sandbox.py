from __future__ import annotations

import asyncio
import io
import posixpath
import uuid
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Literal
from urllib.parse import urlparse

from agents.sandbox.errors import (
    ErrorCode,
    ExecTransportError,
    ExposedPortUnavailableError,
    SandboxRuntimeError,
    WorkspaceArchiveReadError,
    WorkspaceArchiveWriteError,
    WorkspaceReadNotFoundError,
    WorkspaceStartError,
    WorkspaceStopError,
    WorkspaceWriteTypeError,
)
from agents.sandbox.manifest import Manifest
from agents.sandbox.session.base_sandbox_session import BaseSandboxSession
from agents.sandbox.session.sandbox_client import (
    BaseSandboxClient,
    BaseSandboxClientOptions,
)
from agents.sandbox.session.sandbox_session import SandboxSession
from agents.sandbox.session.sandbox_session_state import SandboxSessionState
from agents.sandbox.snapshot import SnapshotBase, SnapshotSpec, resolve_snapshot
from agents.sandbox.types import ExecResult, ExposedPortEndpoint, User
from pydantic import Field

from runta import ApiError, AsyncRunta, IngressSpec, RuntimeStatus


class RuntaSandboxClientOptions(BaseSandboxClientOptions):
    type: Literal["runta"] = "runta"
    endpoint: str | None = None
    token: str | None = Field(default=None, exclude=True)
    name_prefix: str = "agents"
    root: str = "/workspace"
    vcpus: int = 2
    memory_mib: int = 2048
    exposed_ports: tuple[int, ...] = ()
    pause_on_exit: bool = True
    idle_timeout_secs: int | None = None


class RuntaSandboxSessionState(SandboxSessionState):
    type: Literal["runta"] = "runta"
    runtime_id: str
    runtime_name: str
    root: str = "/workspace"
    endpoint: str | None = None
    pause_on_exit: bool = True
    ingress_urls: dict[int, str] = Field(default_factory=dict)


class RuntaSandboxClient(BaseSandboxClient[RuntaSandboxClientOptions]):
    backend_id = "runta"
    supports_default_options = True

    def __init__(
        self,
        *,
        runta: AsyncRunta | None = None,
        instrumentation: Any | None = None,
        dependencies: Any | None = None,
    ) -> None:
        self._runta = runta
        self._instrumentation = instrumentation
        self._dependencies = dependencies

    async def create(
        self,
        *,
        snapshot: SnapshotSpec | SnapshotBase | None = None,
        manifest: Manifest | None = None,
        options: RuntaSandboxClientOptions | None = None,
    ) -> SandboxSession:
        resolved_options = options or RuntaSandboxClientOptions()
        client = self._client(resolved_options)
        manifest = _resolve_manifest_root(manifest, resolved_options.root)

        session_id = uuid.uuid4()
        snapshot_instance = resolve_snapshot(snapshot, str(session_id))
        runtime_name = f"{resolved_options.name_prefix}-{uuid.uuid4().hex[:8]}"
        runtime = await client.runtimes.create(
            runtime_name,
            vcpus=resolved_options.vcpus,
            memory_mib=resolved_options.memory_mib,
            ingress_specs=[
                IngressSpec(protocol="http", runtime_port=port)
                for port in resolved_options.exposed_ports
            ],
            idle_suspend_after_secs=resolved_options.idle_timeout_secs,
        )

        state = RuntaSandboxSessionState(
            session_id=session_id,
            manifest=manifest,
            snapshot=snapshot_instance,
            exposed_ports=resolved_options.exposed_ports,
            runtime_id=runtime.id,
            runtime_name=runtime.name,
            root=manifest.root,
            endpoint=resolved_options.endpoint,
            pause_on_exit=resolved_options.pause_on_exit,
            ingress_urls=_extract_ingress_urls(runtime.cached_info),
        )
        inner = _RuntaSandboxSession(
            client=client,
            state=state,
            runtime=runtime,
            preserved_on_start=False,
        )
        return self._wrap_session(inner, instrumentation=self._instrumentation)

    async def delete(self, session: SandboxSession) -> SandboxSession:
        inner = session._inner
        if not isinstance(inner, _RuntaSandboxSession):
            raise TypeError("RuntaSandboxClient.delete expects a Runta sandbox session")
        runtime = await inner._runtime_handle()
        await runtime.delete()
        return session

    async def resume(self, state: SandboxSessionState) -> SandboxSession:
        if not isinstance(state, RuntaSandboxSessionState):
            raise TypeError(
                "RuntaSandboxClient.resume expects a RuntaSandboxSessionState"
            )
        client = self._client(None, endpoint=state.endpoint)
        inner = _RuntaSandboxSession(
            client=client,
            state=state,
            runtime=None,
            preserved_on_start=True,
        )
        return self._wrap_session(inner, instrumentation=self._instrumentation)

    def deserialize_session_state(
        self, payload: dict[str, object]
    ) -> SandboxSessionState:
        return RuntaSandboxSessionState.model_validate(payload)

    def _client(
        self,
        options: RuntaSandboxClientOptions | None,
        *,
        endpoint: str | None = None,
    ) -> AsyncRunta:
        if self._runta is not None:
            return self._runta
        return AsyncRunta(
            endpoint=options.endpoint if options else endpoint,
            token=options.token if options else None,
        )


class _RuntaSandboxSession(BaseSandboxSession):
    state: RuntaSandboxSessionState

    def __init__(
        self,
        *,
        client: AsyncRunta,
        state: RuntaSandboxSessionState,
        runtime: Any | None,
        preserved_on_start: bool,
    ) -> None:
        self._client = client
        self.state = state
        self._runtime = runtime
        self._preserved_on_start = preserved_on_start
        self._running = False
        self._stopped_by_stop = False

    async def _runtime_handle(self) -> Any:
        if self._runtime is None:
            try:
                self._runtime = await self._client.runtimes.get(self.state.runtime_id)
            except ApiError as exc:
                raise SandboxRuntimeError(
                    message=f"runta runtime is not recoverable: {self.state.runtime_id}",
                    error_code=ErrorCode.SANDBOX_CONFIG_INVALID,
                    op="start",
                    context={
                        "runtime_id": self.state.runtime_id,
                        "runtime_name": self.state.runtime_name,
                    },
                    cause=exc,
                ) from exc
        return self._runtime

    async def _ensure_backend_started(self) -> None:
        runtime = await self._runtime_handle()
        self._set_start_state_preserved(
            self._preserved_on_start, system=self._preserved_on_start
        )
        await self._ensure_runtime_running(runtime)
        self.state.ingress_urls = {
            **self.state.ingress_urls,
            **_extract_ingress_urls(runtime.cached_info),
        }

    async def _prepare_backend_workspace(self) -> None:
        runtime = await self._runtime_handle()
        result = await runtime.exec(["mkdir", "-p", self.state.manifest.root])
        if int(result.exit_code) != 0:
            raise WorkspaceStartError(
                path=Path(self.state.manifest.root),
                context={
                    "runtime_id": self.state.runtime_id,
                    "stderr": _result_stderr(result),
                },
            )

    async def _after_start(self) -> None:
        self._running = True
        self._stopped_by_stop = False

    async def _after_start_failed(self) -> None:
        self._running = False

    def _wrap_start_error(self, error: Exception) -> Exception:
        if isinstance(error, SandboxRuntimeError):
            return error
        return WorkspaceStartError(path=Path(self.state.manifest.root), cause=error)

    def _wrap_stop_error(self, error: Exception) -> Exception:
        if isinstance(error, SandboxRuntimeError):
            return error
        return WorkspaceStopError(path=Path(self.state.manifest.root), cause=error)

    async def stop(self) -> None:
        await super().stop()
        runtime = await self._runtime_handle()
        try:
            if self.state.pause_on_exit:
                await runtime.pause()
            else:
                await runtime.shutdown()
        except Exception as exc:
            raise self._wrap_stop_error(exc) from exc
        self._running = False
        self._stopped_by_stop = True

    async def _shutdown_backend(self) -> None:
        if self._stopped_by_stop:
            return
        runtime = await self._runtime_handle()
        await runtime.shutdown()
        self._running = False

    async def _after_shutdown(self) -> None:
        self._running = False

    async def _exec_internal(
        self, *command: str | Path, timeout: float | None = None
    ) -> ExecResult:
        runtime = await self._runtime_handle()
        command_parts = [str(part) for part in command]
        deadline = asyncio.get_running_loop().time() + 15.0
        delay = 0.5
        while True:
            await self._ensure_runtime_ready_for_io(runtime)
            try:
                result = await runtime.exec(
                    command_parts,
                    timeout=timeout,
                    cwd=self.state.manifest.root,
                )
                break
            except ApiError as exc:
                if not _is_not_running_error(exc):
                    raise ExecTransportError(
                        command=command,
                        context={"runtime_id": self.state.runtime_id},
                        cause=exc,
                    ) from exc
                if asyncio.get_running_loop().time() >= deadline:
                    raise ExecTransportError(
                        command=command,
                        context={"runtime_id": self.state.runtime_id},
                        cause=exc,
                    ) from exc
                self._running = False
                await self._recover_runtime_after_not_running_error(runtime, exc)
                await asyncio.sleep(delay)
                delay = min(delay * 2, 2.0)
            except Exception as exc:
                raise ExecTransportError(
                    command=command,
                    context={"runtime_id": self.state.runtime_id},
                    cause=exc,
                ) from exc
        return ExecResult(
            stdout=_bytes(result.stdout),
            stderr=_bytes(result.stderr),
            exit_code=int(result.exit_code),
        )

    async def read(self, path: Path, *, user: str | User | None = None) -> io.IOBase:
        _ = user
        normalized = self.normalize_path(path)
        runtime = await self._runtime_handle()
        await self._ensure_runtime_ready_for_io(runtime)
        try:
            return io.BytesIO(await runtime.files.read(_sandbox_path(normalized)))
        except FileNotFoundError as exc:
            raise WorkspaceReadNotFoundError(path=normalized, cause=exc) from exc
        except ApiError as exc:
            if exc.status_code == 404:
                raise WorkspaceReadNotFoundError(path=normalized, cause=exc) from exc
            raise WorkspaceArchiveReadError(path=normalized, cause=exc) from exc

    async def write(
        self,
        path: Path,
        data: io.IOBase,
        *,
        user: str | User | None = None,
    ) -> None:
        _ = user
        normalized = self.normalize_path(path, for_write=True)
        payload = data.read()
        if isinstance(payload, str):
            raise WorkspaceWriteTypeError(path=normalized, actual_type="str")
        if not isinstance(payload, bytes):
            raise WorkspaceWriteTypeError(
                path=normalized, actual_type=type(payload).__name__
            )

        runtime = await self._runtime_handle()
        await self._ensure_runtime_ready_for_io(runtime)
        parent = posixpath.dirname(_sandbox_path(normalized))
        result = await self.exec("mkdir", "-p", parent, shell=False)
        if not result.ok():
            raise WorkspaceArchiveWriteError(
                path=normalized,
                context={"stderr": _decode(result.stderr)},
            )
        try:
            await runtime.files.write(_sandbox_path(normalized), payload)
        except Exception as exc:
            raise WorkspaceArchiveWriteError(path=normalized, cause=exc) from exc

    async def persist_workspace(self) -> io.IOBase:
        runtime = await self._runtime_handle()
        await self._ensure_runtime_ready_for_io(runtime)
        remote_tar = f"/tmp/agents-runta-{uuid.uuid4().hex}.tar"
        root = self.state.manifest.root
        try:
            result = await runtime.exec(["tar", "-C", root, "-cf", remote_tar, "."])
            if result.exit_code != 0:
                raise WorkspaceArchiveReadError(
                    path=Path(root),
                    context={"stderr": _result_stderr(result)},
                )
            return io.BytesIO(await runtime.files.read(remote_tar))
        except WorkspaceArchiveReadError:
            raise
        except Exception as exc:
            raise WorkspaceArchiveReadError(path=Path(root), cause=exc) from exc
        finally:
            try:
                await runtime.exec(["rm", "-f", remote_tar])
            except Exception:
                pass

    async def hydrate_workspace(self, data: io.IOBase) -> None:
        runtime = await self._runtime_handle()
        await self._ensure_runtime_ready_for_io(runtime)
        payload = data.read()
        if isinstance(payload, str):
            raise WorkspaceWriteTypeError(
                path=Path(self.state.manifest.root), actual_type="str"
            )
        if not isinstance(payload, bytes):
            raise WorkspaceWriteTypeError(
                path=Path(self.state.manifest.root),
                actual_type=type(payload).__name__,
            )

        remote_tar = f"/tmp/agents-runta-{uuid.uuid4().hex}.tar"
        root = self.state.manifest.root
        try:
            await runtime.files.write(remote_tar, payload)
            result = await runtime.exec(
                [
                    "sh",
                    "-lc",
                    'mkdir -p "$1" && tar -xf "$2" -C "$1"',
                    "_",
                    root,
                    remote_tar,
                ]
            )
            if result.exit_code != 0:
                raise WorkspaceArchiveWriteError(
                    path=Path(root),
                    context={"stderr": _result_stderr(result)},
                )
        except WorkspaceArchiveWriteError:
            raise
        except Exception as exc:
            raise WorkspaceArchiveWriteError(path=Path(root), cause=exc) from exc
        finally:
            try:
                await runtime.exec(["rm", "-f", remote_tar])
            except Exception:
                pass

    async def running(self) -> bool:
        try:
            runtime = await self._runtime_handle()
            status = await runtime.status()
        except Exception:
            return False
        return status == RuntimeStatus.RUNNING

    async def _resolve_exposed_port(self, port: int) -> ExposedPortEndpoint:
        url = self.state.ingress_urls.get(port)
        if not url:
            runtime = await self._runtime_handle()
            self.state.ingress_urls = {
                **self.state.ingress_urls,
                **_extract_ingress_urls(runtime.cached_info),
            }
            url = self.state.ingress_urls.get(port)
        if not url:
            raise ExposedPortUnavailableError(
                port=port,
                exposed_ports=self.state.exposed_ports,
                reason="endpoint_unavailable",
                context={"runtime_id": self.state.runtime_id},
            )
        return _endpoint_from_url(url)

    async def _ensure_runtime_running(self, runtime: Any) -> None:
        deadline = asyncio.get_running_loop().time() + 90.0
        while True:
            status = await runtime.status()
            if status == RuntimeStatus.RUNNING:
                return
            if asyncio.get_running_loop().time() >= deadline:
                raise SandboxRuntimeError(
                    message="timed out waiting for runta runtime to start",
                    error_code=ErrorCode.SANDBOX_CONFIG_INVALID,
                    op="start",
                    context={
                        "runtime_id": self.state.runtime_id,
                        "status": status.value,
                    },
                )
            if status in {RuntimeStatus.PAUSED, RuntimeStatus.SUSPENDED}:
                await runtime.resume()
            elif status == RuntimeStatus.SHUTDOWN:
                await runtime.boot()
            elif status in {
                RuntimeStatus.ERROR,
                RuntimeStatus.CRASHED,
                RuntimeStatus.DELETING,
            }:
                raise SandboxRuntimeError(
                    message=f"runta runtime is not startable: {status.value}",
                    error_code=ErrorCode.SANDBOX_CONFIG_INVALID,
                    op="start",
                    context={
                        "runtime_id": self.state.runtime_id,
                        "status": status.value,
                    },
                )
            await asyncio.sleep(1.0)

    async def _recover_runtime_after_not_running_error(
        self, runtime: Any, exc: ApiError
    ) -> None:
        message = str(exc).lower()
        if "paused" in message or "suspended" in message:
            await runtime.resume()
        elif "shutdown" in message:
            await runtime.boot()
        await self._ensure_runtime_running(runtime)

    async def _ensure_runtime_ready_for_io(self, runtime: Any) -> None:
        if self._running:
            return
        await self._ensure_runtime_running(runtime)
        self._running = True


def _resolve_manifest_root(manifest: Manifest | None, root: str) -> Manifest:
    if manifest is None:
        return Manifest(root=root)
    if manifest.root == "/workspace" and root != "/workspace":
        return manifest.model_copy(update={"root": root}, deep=True)
    return manifest


def _extract_ingress_urls(info: Any) -> dict[int, str]:
    candidates = []
    for attr in ("ingress_urls", "public_ingress_urls", "ingress_endpoints"):
        value = getattr(info, attr, None)
        if value:
            candidates.append(value)

    urls: dict[int, str] = {}
    for value in candidates:
        if isinstance(value, Mapping):
            for port, url in value.items():
                try:
                    urls[int(port)] = str(url)
                except (TypeError, ValueError):
                    continue
        elif isinstance(value, list):
            for item in value:
                if (
                    isinstance(item, Mapping)
                    and "runtime_port" in item
                    and "url" in item
                ):
                    try:
                        urls[int(item["runtime_port"])] = str(item["url"])
                    except (TypeError, ValueError):
                        continue
    return urls


def _is_not_running_error(exc: ApiError) -> bool:
    message = str(exc).lower()
    return exc.status_code == 409 and "not running" in message


def _endpoint_from_url(url: str) -> ExposedPortEndpoint:
    parsed = urlparse(url)
    if not parsed.hostname:
        raise ValueError(f"invalid Runta ingress URL: {url}")
    tls = parsed.scheme in {"https", "wss"}
    port = parsed.port or (443 if tls else 80)
    return ExposedPortEndpoint(
        host=parsed.hostname, port=port, tls=tls, query=parsed.query
    )


def _sandbox_path(path: Path) -> str:
    return path.as_posix()


def _bytes(value: Any) -> bytes:
    if isinstance(value, bytes):
        return value
    if value is None:
        return b""
    return str(value).encode()


def _decode(value: bytes) -> str:
    return value.decode("utf-8", errors="replace")


def _result_stderr(result: Any) -> str:
    stderr_text = getattr(result, "stderr_text", None)
    if stderr_text is not None:
        return str(stderr_text)
    return _decode(_bytes(getattr(result, "stderr", b"")))
