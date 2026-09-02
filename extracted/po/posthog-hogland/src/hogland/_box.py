"""Per-box resource handles.

A :class:`Hogbox` is the in-memory view of a single hogbox bound to the
client that produced it. Method calls translate to one HTTP request
each — there is no client-side state worth syncing — but the handle
caches the most recent :class:`BoxView` so a quick ``box.status`` read
after ``client.create`` doesn't pay an extra round-trip.

Two parallel classes (:class:`Hogbox` / :class:`AsyncHogbox`) keep the
sync and async code paths from sharing an instance and accidentally
mixing event loops.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self
from urllib.parse import quote

import httpx
from httpx_sse import aconnect_sse, connect_sse

from ._http import raise_for_status
from ._models import BoxSpec, BoxView, ExecEvent, ExecResult, FileWriteResponse, SnapshotRecord
from ._sse import parse_event

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator
    from datetime import datetime
    from types import TracebackType

    from ._async import AsyncHogland
    from ._client import Hogland


class _BoxCommon:
    """State and small helpers shared by the sync + async handles."""

    view: BoxView

    def __init__(self, view: BoxView) -> None:
        self.view = view

    @property
    def id(self) -> str:
        return self.view.id

    @property
    def status(self) -> str:
        return self.view.status

    @property
    def spec(self) -> BoxSpec:
        return self.view.spec

    @property
    def expires_at(self) -> datetime | None:
        """When the reaper would tear this box down next, if no further
        activity bumps ``LastUsedAt``.

        ``None`` if the server didn't supply a TTL projection (older
        versions, or a box created before the TTL feature shipped). Cached
        — call ``client.get(box.id)`` to re-read the live value.
        """
        return self.view.expires_at

    def __repr__(self) -> str:
        return f"<{type(self).__name__} id={self.id!r} status={self.status!r}>"


def _exec_path(box_id: str) -> str:
    return f"/v1/hogboxes/{quote(box_id, safe='')}/exec"


def _stream_path(box_id: str) -> str:
    return f"/v1/hogboxes/{quote(box_id, safe='')}/exec/stream"


def _files_path(box_id: str) -> str:
    return f"/v1/hogboxes/{quote(box_id, safe='')}/files"


def _box_path(box_id: str) -> str:
    return f"/v1/hogboxes/{quote(box_id, safe='')}"


def _snapshots_path(box_id: str) -> str:
    return f"/v1/hogboxes/{quote(box_id, safe='')}/snapshots"


def _pause_path(box_id: str) -> str:
    return f"/v1/hogboxes/{quote(box_id, safe='')}/pause"


def _resume_path(box_id: str) -> str:
    return f"/v1/hogboxes/{quote(box_id, safe='')}/resume"


def _proxy_path(box_id: str, port: int, path: str = "") -> str:
    suffix = path.lstrip("/")
    base = f"/v1/hogboxes/{quote(box_id, safe='')}/proxy/{port}"
    return f"{base}/{suffix}" if suffix else f"{base}/"


def _build_exec_body(
    argv: list[str],
    *,
    timeout_seconds: int | None,
    env: dict[str, str] | None,
    workdir: str | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"argv": list(argv)}
    if timeout_seconds is not None:
        body["timeout_seconds"] = timeout_seconds
    if env is not None:
        body["env"] = env
    if workdir is not None:
        body["workdir"] = workdir
    return body


# Pad the client read timeout above the caller's timeout_seconds so the in-guest
# daemon can kill the process and report timed_out before httpx abandons the
# socket. Mirrors execTimeoutGrace on the server.
_EXEC_TIMEOUT_GRACE_SECONDS = 30

# The server's hard max for timeout_seconds. An explicit 0 on the batch
# endpoint means "run up to this max", so the read leg must cover it.
_MAX_EXEC_TIMEOUT_SECONDS = 6 * 60 * 60


def _exec_http_timeout(client_timeout: httpx.Timeout, timeout_seconds: int | None) -> httpx.Timeout:
    """Per-call timeout for a batch exec.

    The client's default read timeout is short (30s), so box.exec with a longer
    timeout_seconds would raise ReadTimeout before the command finishes. Extend
    only the read leg to cover the requested budget plus grace, inheriting the
    connect/write/pool legs from the client. An explicit 0 is the server's "run
    up to the 6h max", so the read leg extends to cover that whole budget. A
    missing timeout_seconds keeps the client default as the local bound, and a
    negative one is rejected server-side before any run starts.
    """
    if timeout_seconds is None or timeout_seconds < 0:
        return client_timeout
    effective = timeout_seconds if timeout_seconds > 0 else _MAX_EXEC_TIMEOUT_SECONDS
    # Copy the client's timeout (inheriting its connect/write/pool legs) and
    # extend only the read leg. Copying via the constructor avoids reading
    # httpx's object-typed leg attributes, which a strict type checker rejects.
    t = httpx.Timeout(client_timeout)
    t.read = float(effective) + _EXEC_TIMEOUT_GRACE_SECONDS
    return t


def _build_file_query(path: str, *, mode: str | None, mkdir: bool) -> dict[str, str]:
    params: dict[str, str] = {"path": path}
    if mode is not None:
        params["mode"] = mode
    if mkdir:
        params["mkdir"] = "true"
    return params


class Hogbox(_BoxCommon):
    """Sync handle to a single hogbox."""

    def __init__(self, view: BoxView, client: Hogland) -> None:
        super().__init__(view)
        self._client = client

    # ---- lifecycle --------------------------------------------------------

    def refresh(self) -> Self:
        """Re-fetch the box view from the server, updating cached state."""
        resp = self._client._http.get(_box_path(self.id))
        raise_for_status(resp)
        self.view = BoxView.model_validate(resp.json())
        return self

    def delete(self) -> None:
        """Terminate and delete the box. Idempotent — 404 is treated as success."""
        resp = self._client._http.delete(_box_path(self.id))
        if resp.status_code == 404:
            return
        raise_for_status(resp)

    def pause(self) -> Self:
        resp = self._client._http.post(_pause_path(self.id))
        raise_for_status(resp)
        return self.refresh()

    def resume(self) -> Self:
        resp = self._client._http.post(_resume_path(self.id))
        raise_for_status(resp)
        return self.refresh()

    def snapshot(self) -> SnapshotRecord:
        """Pause → sync → resume the box and return the snapshot record."""
        resp = self._client._http.post(_snapshots_path(self.id))
        raise_for_status(resp)
        return SnapshotRecord.model_validate(resp.json())

    # ---- exec -------------------------------------------------------------

    def exec(
        self,
        argv: list[str],
        *,
        timeout_seconds: int | None = None,
        env: dict[str, str] | None = None,
        workdir: str | None = None,
    ) -> ExecResult:
        """Run a command to completion and return captured stdout/stderr.

        ``argv`` is the program plus its arguments — first entry is the
        program. For shell expansion, pass ``["bash", "-c", "..."]``.
        """
        body = _build_exec_body(argv, timeout_seconds=timeout_seconds, env=env, workdir=workdir)
        resp = self._client._http.post(
            _exec_path(self.id),
            json=body,
            timeout=_exec_http_timeout(self._client._http.timeout, timeout_seconds),
        )
        raise_for_status(resp)
        return ExecResult.model_validate(resp.json())

    def exec_stream(
        self,
        argv: list[str],
        *,
        timeout_seconds: int | None = None,
        env: dict[str, str] | None = None,
        workdir: str | None = None,
    ) -> Iterator[ExecEvent]:
        """Run a command and yield :class:`ExecEvent` frames as they arrive.

        Returns a generator. The final yielded event always has
        ``kind == "exit"`` — read ``exit_code`` from there. Closing the
        generator early closes the underlying HTTP connection.
        """
        body = _build_exec_body(argv, timeout_seconds=timeout_seconds, env=env, workdir=workdir)
        with connect_sse(
            self._client._http,
            "POST",
            _stream_path(self.id),
            json=body,
        ) as event_source:
            raise_for_status(event_source.response)
            for sse in event_source.iter_sse():
                yield parse_event(sse)

    # ---- files ------------------------------------------------------------

    def read_file(self, path: str) -> bytes:
        """Read an absolute in-box path. Capped at 64 MiB server-side."""
        resp = self._client._http.get(_files_path(self.id), params={"path": path})
        raise_for_status(resp)
        # Server returns raw octet-stream (huma_exec.go: `Body []byte`),
        # despite the OpenAPI spec claiming base64+JSON. The spec is the
        # one that's wrong — Huma's `[]byte` schema reflection doesn't
        # match its emitted content-type.
        return resp.content

    def write_file(
        self,
        path: str,
        content: bytes,
        *,
        mode: str | None = None,
        mkdir: bool = False,
    ) -> FileWriteResponse:
        """Write raw bytes to an absolute in-box path. ≤ 64 MiB."""
        resp = self._client._http.put(
            _files_path(self.id),
            content=content,
            headers={"Content-Type": "application/octet-stream"},
            params=_build_file_query(path, mode=mode, mkdir=mkdir),
        )
        raise_for_status(resp)
        return FileWriteResponse.model_validate(resp.json())

    # ---- proxy ------------------------------------------------------------

    def proxy_url(self, port: int, path: str = "") -> str:
        """Return the hogplane URL that proxies into the box at ``port``.

        Hit the returned URL with the same credential you use for the rest
        of the SDK — the proxy reuses hogplane's auth middleware. No
        signed-URL system, no per-tunnel token. See
        ``docs/PYTHON_SDK_CODEGEN_RESEARCH.md`` §1d.
        """
        return f"{self._client.base_url}{_proxy_path(self.id, port, path)}"

    def web_url(self) -> str | None:
        """Return the box's HTTP-exposure URL (``https://<box>.<box-edge>/``).

        Non-empty only when the box was created with ``web_port=`` (HTTP
        exposed), is running, and the deployment has a box gateway host
        configured. Reads the server-computed ``web_url`` from a fresh box
        fetch — the typed BoxView drops it — so call it once the box is
        running. Returns ``None`` otherwise. Unlike ``proxy_url`` (the
        authenticated hogplane path proxy), this is the box's own per-box
        hostname, served by the box-front edge.
        """
        resp = self._client._http.get(_box_path(self.id))
        raise_for_status(resp)
        return resp.json().get("web_url") or None

    # ---- context manager --------------------------------------------------

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        # Best-effort cleanup so `with client.create(...) as box:` works
        # like the Modal SandboxBase pattern. Errors from the delete
        # don't shadow an exception already propagating from the body.
        try:
            self.delete()
        except Exception:
            if exc_type is None:
                raise


class AsyncHogbox(_BoxCommon):
    """Async handle to a single hogbox. Same shape as :class:`Hogbox`."""

    def __init__(self, view: BoxView, client: AsyncHogland) -> None:
        super().__init__(view)
        self._client = client

    async def refresh(self) -> Self:
        resp = await self._client._http.get(_box_path(self.id))
        raise_for_status(resp)
        self.view = BoxView.model_validate(resp.json())
        return self

    async def delete(self) -> None:
        resp = await self._client._http.delete(_box_path(self.id))
        if resp.status_code == 404:
            return
        raise_for_status(resp)

    async def pause(self) -> Self:
        resp = await self._client._http.post(_pause_path(self.id))
        raise_for_status(resp)
        return await self.refresh()

    async def resume(self) -> Self:
        resp = await self._client._http.post(_resume_path(self.id))
        raise_for_status(resp)
        return await self.refresh()

    async def snapshot(self) -> SnapshotRecord:
        resp = await self._client._http.post(_snapshots_path(self.id))
        raise_for_status(resp)
        return SnapshotRecord.model_validate(resp.json())

    async def exec(
        self,
        argv: list[str],
        *,
        timeout_seconds: int | None = None,
        env: dict[str, str] | None = None,
        workdir: str | None = None,
    ) -> ExecResult:
        body = _build_exec_body(argv, timeout_seconds=timeout_seconds, env=env, workdir=workdir)
        resp = await self._client._http.post(
            _exec_path(self.id),
            json=body,
            timeout=_exec_http_timeout(self._client._http.timeout, timeout_seconds),
        )
        raise_for_status(resp)
        return ExecResult.model_validate(resp.json())

    async def exec_stream(
        self,
        argv: list[str],
        *,
        timeout_seconds: int | None = None,
        env: dict[str, str] | None = None,
        workdir: str | None = None,
    ) -> AsyncIterator[ExecEvent]:
        body = _build_exec_body(argv, timeout_seconds=timeout_seconds, env=env, workdir=workdir)
        async with aconnect_sse(
            self._client._http,
            "POST",
            _stream_path(self.id),
            json=body,
        ) as event_source:
            raise_for_status(event_source.response)
            async for sse in event_source.aiter_sse():
                yield parse_event(sse)

    async def read_file(self, path: str) -> bytes:
        resp = await self._client._http.get(_files_path(self.id), params={"path": path})
        raise_for_status(resp)
        return resp.content

    async def write_file(
        self,
        path: str,
        content: bytes,
        *,
        mode: str | None = None,
        mkdir: bool = False,
    ) -> FileWriteResponse:
        resp = await self._client._http.put(
            _files_path(self.id),
            content=content,
            headers={"Content-Type": "application/octet-stream"},
            params=_build_file_query(path, mode=mode, mkdir=mkdir),
        )
        raise_for_status(resp)
        return FileWriteResponse.model_validate(resp.json())

    def proxy_url(self, port: int, path: str = "") -> str:
        return f"{self._client.base_url}{_proxy_path(self.id, port, path)}"

    async def web_url(self) -> str | None:
        """Async twin of :meth:`Hogbox.web_url` — the box's per-box
        ``https://<box>.<box-edge>/`` hostname, or ``None`` when the box
        isn't HTTP-exposed/running or the edge isn't configured.
        """
        resp = await self._client._http.get(_box_path(self.id))
        raise_for_status(resp)
        return resp.json().get("web_url") or None

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        try:
            await self.delete()
        except Exception:
            if exc_type is None:
                raise
