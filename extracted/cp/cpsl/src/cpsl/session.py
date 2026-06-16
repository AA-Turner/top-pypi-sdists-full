from __future__ import annotations

import asyncio
import datetime
import hashlib
import json
import math
import uuid
from collections.abc import AsyncIterator, Callable
from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
from typing import Any, MutableMapping
from urllib.parse import urlparse

from .constants import (
    KV_KEY_FIELD,
    SCOPE_FIELD_OWNER,
    SCOPE_FIELD_SESSION,
    SCOPE_FIELD_USER,
)
from .db import Collection, CollectionManager, ScopedDatabaseProxy, get_active_identity
from .integration import (
    IntegrationConfig,
    IntegrationCredentials,
    IntegrationLike,
    KNOWN_SECRET_INTEGRATIONS,
    credentials_from_wire,
    integration_type as normalize_integration_type,
)
from .clients.capsule import CompleteOnboardingRequest
from .msg import Message


def _now_ms() -> int:
    import time

    return int(time.time() * 1000)


async def _run_blocking(fn: Callable[[], Any]) -> Any:
    return await asyncio.get_running_loop().run_in_executor(None, fn)


def _is_remote_url(value: str) -> bool:
    return value.startswith(("http://", "https://", "data:"))


class _TrackedList(list):
    def __init__(self, values=(), notify: Callable[[], None] | None = None):
        self._notify = notify
        super().__init__(_track_data_value(v, notify) for v in values)

    def _changed(self) -> None:
        if self._notify:
            self._notify()

    def append(self, item):
        super().append(_track_data_value(item, self._notify))
        self._changed()

    def extend(self, values):
        super().extend(_track_data_value(v, self._notify) for v in values)
        self._changed()

    def insert(self, index, item):
        super().insert(index, _track_data_value(item, self._notify))
        self._changed()

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            value = [_track_data_value(v, self._notify) for v in value]
        else:
            value = _track_data_value(value, self._notify)
        super().__setitem__(key, value)
        self._changed()

    def __delitem__(self, key):
        super().__delitem__(key)
        self._changed()

    def clear(self):
        super().clear()
        self._changed()

    def pop(self, *args):
        value = super().pop(*args)
        self._changed()
        return value

    def remove(self, value):
        super().remove(value)
        self._changed()

    def sort(self, *args, **kwargs):
        super().sort(*args, **kwargs)
        self._changed()

    def reverse(self):
        super().reverse()
        self._changed()


SESSION_DATA_REVISION_KEY = "__cpsl_session_rev"
SESSION_DATA_CHECKSUM_KEY = "__cpsl_session_checksum"
SESSION_DATA_NONCE_KEY = "__cpsl_session_nonce"


def _coerce_revision(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def session_data_revision(data: MutableMapping[str, Any]) -> int:
    """Return the server-assigned session data revision."""
    return _coerce_revision(data.get(SESSION_DATA_REVISION_KEY))


def _without_session_metadata(data: MutableMapping[str, Any]) -> dict[str, Any]:
    return {
        str(key): value
        for key, value in data.items()
        if key not in {SESSION_DATA_REVISION_KEY, SESSION_DATA_CHECKSUM_KEY, SESSION_DATA_NONCE_KEY}
    }


def session_data_payload_json(data: MutableMapping[str, Any]) -> str:
    """Encode session data without server-owned metadata."""
    return session_data_json(_without_session_metadata(data))


def _go_json_escape(payload: str) -> str:
    """Match Go encoding/json's default string escaping for checksums."""
    return (
        payload.replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def _session_data_checksum_json(data: MutableMapping[str, Any]) -> str:
    payload = json.dumps(
        _json_safe_value(_without_session_metadata(data)),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return _go_json_escape(payload)


def session_data_checksum(data: MutableMapping[str, Any]) -> str:
    """Return the checksum for the canonical session data payload."""
    payload = _session_data_checksum_json(data)
    return "sha256:" + hashlib.sha256(payload.encode()).hexdigest()


def session_data_base_checksum(data: MutableMapping[str, Any]) -> str:
    """Return the server-assigned checksum, computing one for legacy snapshots."""
    raw = data.get(SESSION_DATA_CHECKSUM_KEY)
    if isinstance(raw, str) and raw:
        return raw
    return session_data_checksum(data)


class SessionData(dict):
    """Persistent per-session data.

    Mutating this dictionary saves the new state after the handler returns.
    ``set`` is async so app code can write ``await session.data.set(...)`` and
    make the persistence/broadcast behavior explicit.
    """

    def __init__(self, values=(), notify: Callable[[], None] | None = None, **kwargs):
        self._notify = notify
        initial = dict(values, **kwargs)
        super().__init__((k, _track_data_value(v, notify)) for k, v in initial.items())

    def _changed(self) -> None:
        if self._notify:
            self._notify()

    def __setitem__(self, key, value):
        super().__setitem__(key, _track_data_value(value, self._notify))
        self._changed()

    def __delitem__(self, key):
        super().__delitem__(key)
        self._changed()

    def clear(self):
        super().clear()
        self._changed()

    def pop(self, *args):
        value = super().pop(*args)
        self._changed()
        return value

    def popitem(self):
        value = super().popitem()
        self._changed()
        return value

    def setdefault(self, key, default=None):
        if key not in self:
            self[key] = default
        return self[key]

    def update(self, *args, **kwargs):
        for key, value in dict(*args, **kwargs).items():
            super().__setitem__(key, _track_data_value(value, self._notify))
        self._changed()

    async def set(self, key: str, value: Any) -> Any:
        """Persist a named session data value and broadcast realtime updates."""
        super().__setitem__(key, _track_data_value(value, self._notify))
        if self._notify:
            owner = getattr(self._notify, "__self__", None)
            notify_async = getattr(owner, "_notify_data_changed_async", None)
            if callable(notify_async):
                await notify_async()
            else:
                result = self._notify()
                if asyncio.iscoroutine(result):
                    await result
        return self[key]


def _track_data_value(value: Any, notify: Callable[[], None] | None) -> Any:
    if isinstance(value, SessionData) or isinstance(value, _TrackedList):
        value._notify = notify
        return value
    if isinstance(value, dict):
        return SessionData(value, notify)
    if isinstance(value, list):
        return _TrackedList(value, notify)
    return value


def _json_safe_value(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, Enum):
        return _json_safe_value(value.value)
    if isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
        return value.isoformat()
    if isinstance(value, bytes):
        return value.decode(errors="replace")

    dump = getattr(value, "model_dump", None)
    if callable(dump):
        try:
            return _json_safe_value(dump(mode="json"))
        except TypeError:
            return _json_safe_value(dump())

    if is_dataclass(value) and not isinstance(value, type):
        return _json_safe_value(asdict(value))

    if isinstance(value, dict):
        return {str(key): _json_safe_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, SessionData, _TrackedList)):
        return [_json_safe_value(item) for item in value]

    return str(value)


def session_data_json(data: Any) -> str:
    """Encode session data through the SDK's durable JSON boundary."""
    return json.dumps(_json_safe_value(data), ensure_ascii=False, separators=(",", ":"))


@dataclass
class Block:
    """Structured inline message sent over the chat transport.

    `type` picks the renderer on the client side (e.g. ``task_card``,
    ``integration_prompt``). ``payload`` is an arbitrary JSON-serializable
    dict. An ``id`` is auto-generated if not supplied.
    """

    type: str
    payload: dict[str, Any]
    id: str = ""

    def to_envelope(self) -> dict[str, Any]:
        return {
            "id": self.id or f"blk_{uuid.uuid4().hex[:12]}",
            "type": self.type,
            "payload": self.payload,
        }


@dataclass
class FileUpload:
    """Result of a user file upload prompted via ``session.prompt_file()``.

    Attributes:
        name: Original filename.
        content_type: MIME type (e.g. ``"image/png"``).
        url: Presigned download URL (valid for 7 days).
        size: File size in bytes.
        path: Local path if the file was auto-downloaded (when ``path``
            was passed to ``prompt_file``), otherwise ``None``.
    """

    name: str
    content_type: str
    url: str
    size: int
    path: str | None = None

    async def download(self, path: str) -> str:
        """Download the file to a local path. Returns the path."""
        import aiohttp

        async with aiohttp.ClientSession() as http:
            async with http.get(self.url) as resp:
                resp.raise_for_status()
                with open(path, "wb") as f:
                    async for chunk in resp.content.iter_chunked(8192):
                        f.write(chunk)
        self.path = path
        return path


@dataclass
class SessionChannel:
    """Describes the transport a session message arrived on (chat, telegram, etc.)."""

    type: str


@dataclass
class UserInfo:
    """Identity of the authenticated user.

    ``id`` identifies the individual. ``org_id`` stores the bare
    organization id when the user belongs to an organization.
    ``scope="user"`` always filters by ``id``.
    """

    id: str
    email: str | None = None
    org_id: str | None = None

    @staticmethod
    def org_id_from_owner_id(owner_id: str | None) -> str | None:
        """Extract the bare org id from a runtime owner key."""
        if not owner_id or not owner_id.startswith("org:"):
            return None
        return owner_id[4:]

    @property
    def is_org_member(self) -> bool:
        """True when this user belongs to an app organization."""
        return bool(self.org_id)

    @property
    def owner_id(self) -> str:
        """Runtime scoping key for ``scope="owner"`` collections.

        Organization owners use the runtime key ``org:<org_id>`` while solo
        users use their hashed user id directly.
        """
        if self.org_id:
            return self.org_id if self.org_id.startswith("org:") else f"org:{self.org_id}"
        return self.id


class ReplyStream:
    """Async context manager for streaming incremental text to the UI.

    Each ``write()`` call sends a chunk immediately so the user sees
    tokens as they arrive. On exit the accumulated text is saved to
    session history.

    Obtain via ``session.stream_reply()``.
    """

    __slots__ = ("_write_cb", "_done_cb", "_history", "_channel_type", "_full")

    def __init__(
        self,
        write_cb: Callable[[str], None],
        history: list[Message],
        channel_type: str,
        done_cb: Callable[[], None] | None = None,
    ) -> None:
        self._write_cb = write_cb
        self._done_cb = done_cb
        self._history = history
        self._channel_type = channel_type
        self._full: str = ""

    async def __aenter__(self) -> ReplyStream:
        return self

    async def __aexit__(self, *exc: Any) -> None:
        if self._full:
            self._history.append(
                Message(text=self._full, sender="app", channel_type=self._channel_type)
            )
        if self._done_cb:
            self._done_cb()

    @property
    def text(self) -> str:
        """The full accumulated text written so far."""
        return self._full

    def write(self, text: str) -> None:
        """Send a text chunk to the client immediately.

        Handles both delta and cumulative (snapshot) text: if *text*
        starts with everything written so far it is treated as a
        cumulative snapshot and only the new suffix is forwarded.
        """
        if not text:
            return
        if text.startswith(self._full):
            delta = text[len(self._full) :]
        else:
            delta = text
        if delta:
            self._write_cb(delta)
        self._full += delta


class RequestContext:
    """Context for data source and endpoint handlers.

    Provides the calling user's identity and connected integrations
    without requiring a chat session. Obtain automatically by declaring
    ``ctx: cpsl.RequestContext`` as the first parameter of an
    ``@app.data()`` or ``@app.endpoint()`` handler.
    """

    __slots__ = (
        "user",
        "integrations",
        "authenticated",
        "request",
        "_session_stub",
        "_app_id",
        "_env",
    )

    def __init__(
        self,
        user: UserInfo,
        integrations: dict[str, IntegrationCredentials],
        authenticated: bool = False,
        request: Any = None,
        session_stub: Any = None,
        app_id: str = "",
        env: str = "",
    ) -> None:
        self.user = user
        self.integrations = integrations
        self.authenticated = authenticated
        self.request = request
        self._session_stub = session_stub
        self._app_id = app_id
        self._env = env

    def pipedream(self, integration: IntegrationLike):
        """Return a requests-like session for a Pipedream-backed integration."""
        from .pipedream import PipedreamProxySession

        if self._session_stub is None:
            raise RuntimeError(
                f"no gateway connection available for Pipedream integration '{normalize_integration_type(integration)}'"
            )
        return PipedreamProxySession(
            stub=self._session_stub,
            app_id=self._app_id,
            user_email=self.user.email or "",
            owner_id=self.user.owner_id,
            integration=integration,
            env=self._env,
        )


class SessionMedia:
    """Helpers for turning generated media into persistent gallery items."""

    __slots__ = ("_session",)

    def __init__(self, session: "Session") -> None:
        self._session = session

    async def image(
        self,
        source: str | bytes | bytearray,
        *,
        caption: str = "",
        alt: str = "",
        filename: str | None = None,
        mime_type: str | None = None,
        copy_remote: bool = False,
    ) -> dict[str, Any]:
        return await self._item(
            "image",
            source,
            caption=caption,
            alt=alt,
            filename=filename,
            mime_type=mime_type,
            copy_remote=copy_remote,
        )

    async def video(
        self,
        source: str | bytes | bytearray,
        *,
        poster: str | bytes | bytearray | None = None,
        caption: str = "",
        alt: str = "",
        filename: str | None = None,
        mime_type: str | None = None,
        copy_remote: bool = False,
    ) -> dict[str, Any]:
        item = await self._item(
            "video",
            source,
            caption=caption,
            alt=alt,
            filename=filename,
            mime_type=mime_type,
            copy_remote=copy_remote,
        )
        if poster is not None:
            poster_item = await self.image(
                poster,
                filename=_derive_media_filename(poster, "poster"),
                copy_remote=copy_remote,
            )
            item["poster"] = poster_item["src"]
        return item

    async def _item(
        self,
        media_type: str,
        source: str | bytes | bytearray,
        *,
        caption: str,
        alt: str,
        filename: str | None,
        mime_type: str | None,
        copy_remote: bool,
    ) -> dict[str, Any]:
        src, content_type = await self._persist_source(
            source,
            filename=filename,
            mime_type=mime_type,
            copy_remote=copy_remote,
        )
        item: dict[str, Any] = {
            "type": media_type,
            "src": src,
            "download_url": src,
        }
        if caption:
            item["caption"] = caption
        if alt:
            item["alt"] = alt
        if content_type:
            item["mime_type"] = content_type
        return item

    async def _persist_source(
        self,
        source: str | bytes | bytearray,
        *,
        filename: str | None,
        mime_type: str | None,
        copy_remote: bool,
    ) -> tuple[str, str]:
        import mimetypes
        import os
        import tempfile

        if isinstance(source, (bytes, bytearray)):
            content_type = mime_type or "application/octet-stream"
            suffix = mimetypes.guess_extension(content_type) or ""
            name = filename or f"media-{uuid.uuid4().hex[:10]}{suffix}"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
                f.write(bytes(source))
                temp_path = f.name
            try:
                return await self._session._upload_local_file(
                    temp_path, filename=name, content_type=content_type
                ), content_type
            finally:
                try:
                    os.unlink(temp_path)
                except OSError:
                    pass

        if _is_remote_url(source) and not copy_remote:
            return source, mime_type or ""

        if _is_remote_url(source) and copy_remote:
            import aiohttp

            async with aiohttp.ClientSession() as http:
                async with http.get(source) as resp:
                    resp.raise_for_status()
                    content_type = (
                        mime_type
                        or resp.headers.get("content-type", "").split(";")[0]
                        or "application/octet-stream"
                    )
                    suffix = mimetypes.guess_extension(content_type) or ""
                    name = filename or _derive_media_filename(
                        source, f"media-{uuid.uuid4().hex[:10]}{suffix}"
                    )
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
                        async for chunk in resp.content.iter_chunked(8192):
                            f.write(chunk)
                        temp_path = f.name
            try:
                return await self._session._upload_local_file(
                    temp_path, filename=name, content_type=content_type
                ), content_type
            finally:
                try:
                    os.unlink(temp_path)
                except OSError:
                    pass

        path = os.fspath(source)
        content_type = mime_type or mimetypes.guess_type(path)[0] or "application/octet-stream"
        name = filename or os.path.basename(path)
        return await self._session._upload_local_file(
            path, filename=name, content_type=content_type
        ), content_type


@dataclass(slots=True)
class TerminalResult:
    """Completed command result returned by ``Terminal.shell`` and ``exec``."""

    exit_code: int
    stdout: str
    stderr: str
    status: str
    command: str
    argv: list[str] | None = None
    timed_out: bool = False

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and not self.timed_out

    def __bool__(self) -> bool:
        return self.ok

    def __int__(self) -> int:
        return self.exit_code

    def __str__(self) -> str:
        return self.stdout or self.stderr or f"exit {self.exit_code}"


class Terminal:
    """Durable terminal transcript attached to a session.

    Create or reopen handles with ``session.terminal("name")``. The name is
    stable across message handlers and tasks; the SDK derives the underlying
    chat block id from it.
    """

    __slots__ = (
        "_session",
        "name",
        "title",
        "cwd",
        "env",
        "block_id",
        "_runs",
        "_revision",
        "_shown",
    )

    def __init__(
        self,
        session: "Session",
        name: str,
        *,
        title: str = "",
        cwd: str | None = None,
        env: dict[str, str] | None = None,
    ) -> None:
        clean_name = (name or "").strip()
        if not clean_name:
            raise ValueError("terminal name must not be empty")
        self._session = session
        self.name = clean_name
        self.title = title or clean_name
        self.cwd = cwd
        self.env = dict(env or {})
        self.block_id = _terminal_block_id(session.id, clean_name)
        self._runs: list[dict[str, Any]] = self._load_runs_from_history()
        self._revision = self._load_revision_from_history()
        self._shown = self._revision > 0 or bool(self._runs)

    def _load_runs_from_history(self) -> list[dict[str, Any]]:
        for msg in reversed(self._session.history):
            if msg.sender != "block" or not msg.text:
                continue
            try:
                envelope = json.loads(msg.text)
            except (TypeError, json.JSONDecodeError):
                continue
            if envelope.get("id") != self.block_id or envelope.get("type") != "terminal":
                continue
            payload = envelope.get("payload") or {}
            runs = payload.get("runs")
            if isinstance(runs, list):
                restored = [r for r in runs if isinstance(r, dict)]
                for run in restored:
                    if run.get("status") == "running":
                        run["status"] = "disconnected"
                        run["ended_at"] = run.get("ended_at") or _now_ms()
                return restored
        return []

    def _load_revision_from_history(self) -> int:
        for msg in reversed(self._session.history):
            if msg.sender != "block" or not msg.text:
                continue
            try:
                envelope = json.loads(msg.text)
            except (TypeError, json.JSONDecodeError):
                continue
            if envelope.get("id") != self.block_id or envelope.get("type") != "terminal":
                continue
            payload = envelope.get("payload") or {}
            revision = payload.get("revision")
            return int(revision) if isinstance(revision, (int, float)) else 0
        return 0

    async def _emit(self) -> None:
        if not self._shown:
            return
        self._revision += 1
        await self._session.show(
            Block(
                id=self.block_id,
                type="terminal",
                payload={
                    "name": self.name,
                    "title": self.title,
                    "cwd": self.cwd or "",
                    "revision": self._revision,
                    "runs": self._runs,
                },
            )
        )

    async def show(self, *, title: str | None = None) -> "Terminal":
        """Render the terminal block without starting a command."""
        if title is not None:
            self.title = title
        self._shown = True
        await self._emit()
        return self

    async def shell(
        self,
        command: str,
        *,
        cwd: str | None = None,
        env: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> TerminalResult:
        """Run a shell command string and append output to this terminal."""
        if not command.strip():
            raise ValueError("shell command must not be empty")
        return await self._run(
            mode="shell",
            command=command,
            argv=None,
            cwd=cwd,
            env=env,
            timeout=timeout,
        )

    async def exec(
        self,
        cmd: str,
        *args: str,
        cwd: str | None = None,
        env: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> TerminalResult:
        """Run a structured argv command and append output to this terminal."""
        if not cmd.strip():
            raise ValueError("exec command must not be empty")
        return await self._run(
            mode="exec",
            command=" ".join([cmd, *args]),
            argv=[cmd, *args],
            cwd=cwd,
            env=env,
            timeout=timeout,
        )

    async def _run(
        self,
        *,
        mode: str,
        command: str,
        argv: list[str] | None,
        cwd: str | None,
        env: dict[str, str] | None,
        timeout: float | None,
    ) -> TerminalResult:
        import os

        run_env = os.environ.copy()
        run_env.update(self.env)
        if env:
            run_env.update(env)
        run_cwd = cwd or self.cwd or None
        run: dict[str, Any] = {
            "id": f"run_{uuid.uuid4().hex[:12]}",
            "mode": mode,
            "command": command,
            "cwd": run_cwd or "",
            "status": "running",
            "started_at": _now_ms(),
            "chunks": [],
        }
        if argv is not None:
            run["argv"] = list(argv)
        self._runs.append(run)
        await self._emit()

        if mode == "shell":
            proc = await asyncio.create_subprocess_shell(
                command,
                cwd=run_cwd,
                env=run_env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        else:
            assert argv is not None
            proc = await asyncio.create_subprocess_exec(
                *argv,
                cwd=run_cwd,
                env=run_env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

        seq = 0
        stdout_parts: list[str] = []
        stderr_parts: list[str] = []

        async def read_stream(stream_name: str, stream: asyncio.StreamReader | None) -> None:
            nonlocal seq
            if stream is None:
                return
            while True:
                chunk = await stream.read(4096)
                if not chunk:
                    return
                text = chunk.decode(errors="replace")
                if stream_name == "stderr":
                    stderr_parts.append(text)
                else:
                    stdout_parts.append(text)
                run["chunks"].append(
                    {
                        "stream": stream_name,
                        "text": text,
                        "timestamp": _now_ms(),
                        "seq": seq,
                    }
                )
                seq += 1
                await self._emit()

        readers = [
            asyncio.create_task(read_stream("stdout", proc.stdout)),
            asyncio.create_task(read_stream("stderr", proc.stderr)),
        ]
        timed_out = False
        try:
            if timeout is None:
                exit_code = await proc.wait()
            else:
                exit_code = await asyncio.wait_for(proc.wait(), timeout=timeout)
        except asyncio.TimeoutError:
            timed_out = True
            proc.kill()
            exit_code = await proc.wait()
        await asyncio.gather(*readers, return_exceptions=True)

        run["exit_code"] = int(exit_code)
        run["ended_at"] = _now_ms()
        run["status"] = "timeout" if timed_out else ("completed" if exit_code == 0 else "failed")
        await self._emit()
        return TerminalResult(
            exit_code=int(exit_code),
            stdout="".join(stdout_parts),
            stderr="".join(stderr_parts),
            status=str(run["status"]),
            command=command,
            argv=list(argv) if argv is not None else None,
            timed_out=timed_out,
        )


TerminalBlock = Terminal


class Session:
    """Per-user conversation context, persisted across messages.

    Concurrency: handlers for the same session are serialized via an
    ``asyncio.Lock``. Handlers across *different* sessions may run
    concurrently. Avoid mutating shared app-instance state without your
    own synchronization.

    Attributes:
        id:      Unique session identifier.
        user:    Identity of the user — ``UserInfo(id, email)``.
        channel: Channel this session is on (chat, api, etc.).
        history: Recent messages, rehydrated from the backing store.
        data:    Persistent key-value dict, saved automatically after each message.
    """

    __slots__ = (
        "id",
        "user",
        "channel",
        "history",
        "data",
        "integrations",
        "media",
        "_reply_callback",
        "_stream_callback",
        "_stream_write_callback",
        "_stream_done_callback",
        "_stream_reply_factory",
        "_notify_callback",
        "_block_callback",
        "_data_change_callback",
        "_data_flush_callback",
        "_db_proxy",
        "_collections_proxy",
        "_runner",
        "_runner_stub",
        "_session_stub",
        "_app_id",
        "_kv",
    )

    def __init__(
        self,
        id: str,
        user: UserInfo,
        channel: SessionChannel,
        history: list[Message] | None = None,
        data: dict[str, Any] | None = None,
        integrations: dict[str, IntegrationCredentials] | None = None,
    ) -> None:
        self.id = id
        self.user = user
        self.channel = channel
        self._reply_callback: Any = None
        self._stream_callback: Any = None
        self._stream_write_callback: Any = None
        self._stream_done_callback: Any = None
        self._stream_reply_factory: Any = None
        self._notify_callback: Any = None
        self._block_callback: Any = None
        self._data_change_callback: Any = None
        self._data_flush_callback: Any = None
        self._db_proxy: ScopedDatabaseProxy | None = None
        self._collections_proxy: CollectionManager | None = None
        self._runner: Any = None
        self._runner_stub: Any = None
        self._session_stub: Any = None
        self._app_id: str = ""
        self._kv: Collection | None = None
        self.history: list[Message] = history or []
        self.data: SessionData = SessionData(data or {}, self._notify_data_changed)
        self.integrations: dict[str, IntegrationCredentials] = integrations or {}
        self.media = SessionMedia(self)

    def _notify_data_changed(self) -> None:
        cb = getattr(self, "_data_change_callback", None)
        if cb is None:
            return
        try:
            result = cb()
            if asyncio.iscoroutine(result):
                try:
                    loop = asyncio.get_running_loop()
                    loop.create_task(result)
                except RuntimeError:
                    pass
        except Exception:
            pass

    async def _notify_data_changed_async(self) -> None:
        cb = getattr(self, "_data_change_callback", None)
        if cb is None:
            return
        try:
            result = cb()
            if asyncio.iscoroutine(result):
                await result
        except Exception:
            pass

    @property
    def db(self) -> ScopedDatabaseProxy:
        """Scoped database proxy — collections auto-filtered by user/team/session identity."""
        if self._db_proxy is None:
            raise RuntimeError("session.db not available (database not configured)")
        return self._db_proxy

    @property
    def collections(self) -> CollectionManager:
        """Dynamic collection manager for scoped runtime collection schemas."""
        if self._collections_proxy is None:
            raise RuntimeError("session.collections not available (database not configured)")
        return self._collections_proxy

    async def publish(self, key: str, value: Any) -> Any:
        """Set a session data value and immediately publish a snapshot.

        Use this for intentional intermediate UI states. Plain
        ``session.data.set`` calls are batched and published once when the
        handler completes.
        """
        setter = getattr(self.data, "set", None)
        if setter is not None:
            result = await setter(key, value)
        else:
            self.data[key] = value
            result = self.data[key]
        await self.flush_data()
        return result

    async def flush_data(self) -> None:
        """Persist and broadcast the current session data snapshot immediately."""
        cb = getattr(self, "_data_flush_callback", None)
        if cb is None:
            return
        result = cb()
        if asyncio.iscoroutine(result):
            await result

    async def emit(self, event: str, payload: dict[str, Any] | None = None) -> None:
        """Emit a transient session event to subscribed clients."""
        cb = self._block_callback
        if cb is None:
            return
        block = Block("session_event", {"event": event, "payload": payload or {}})
        result = cb(json.dumps(block.to_envelope()))
        if asyncio.iscoroutine(result):
            await result

    # -- key-value store -----------------------------------------------------

    def _require_kv(self) -> Collection:
        if self._kv is None:
            raise RuntimeError("session KV not available (database not configured)")
        return self._kv

    def _kv_filter(self, key: str, scope: str) -> dict:
        filt: dict[str, Any] = {KV_KEY_FIELD: key}
        if scope == "session":
            filt[SCOPE_FIELD_SESSION] = self.id
        elif scope == "owner":
            filt[SCOPE_FIELD_OWNER] = self.user.owner_id or self.user.id
        elif scope == "user":
            filt[SCOPE_FIELD_USER] = self.user.id
        return filt

    async def get(self, key: str, default: Any = None, *, scope: str = "session") -> Any:
        """Read a value from the persistent KV store.

        Args:
            key: The key to look up.
            default: Returned when the key does not exist.
            scope: ``"session"`` (this chat thread, default), ``"owner"``
                (org/team), ``"user"`` (this user), or ``"app"`` (global).
        """
        doc = await self._require_kv().find_one(self._kv_filter(key, scope))
        return doc.get("value", default) if doc else default

    async def set(self, key: str, value: Any, *, scope: str = "session") -> None:
        """Write a value to the persistent KV store (upsert).

        Args:
            key: The key to store under.
            value: Any JSON-serializable value.
            scope: ``"session"`` (default), ``"owner"``, ``"user"``, or ``"app"``.
        """
        filt = self._kv_filter(key, scope)
        await self._require_kv().update_one(filt, {"$set": {"value": value, **filt}}, upsert=True)

    async def delete(self, key: str, *, scope: str = "session") -> None:
        """Remove a key from the persistent KV store.

        Args:
            key: The key to delete.
            scope: ``"session"`` (default), ``"owner"``, ``"user"``, or ``"app"``.
        """
        await self._require_kv().delete_one(self._kv_filter(key, scope))

    async def complete_onboarding(self) -> None:
        """Mark this app user's onboarding flow complete."""
        stub = self._session_stub
        if stub is None:
            runner = _get_runner_for_session(self)
            if runner is not None:
                stub = runner._session_stub
        if stub is None:
            raise RuntimeError("complete_onboarding requires an active session")
        await _run_blocking(
            lambda: stub.complete_onboarding(CompleteOnboardingRequest(session_id=self.id))
        )
        await self.show(Block(type="onboarding_complete", payload={"completed": True}))

    # -- messaging -----------------------------------------------------------

    async def reply(self, text: str) -> None:
        """Send a complete message back to the user."""
        msg = Message(text=text, sender="app", channel_type=self.channel.type)
        self.history.append(msg)
        if self._reply_callback:
            await self._reply_callback(msg)

    async def notify(self, text: str, *, detail: str = "") -> None:
        """Send a lightweight, transient status pill to the user.

        In chat, ``notify`` renders as an ephemeral indicator that is replaced
        by the next ``notify`` and cleared as soon as a real reply arrives.
        The text never gets baked into the assistant's message bubble, so
        calling ``notify("Thinking...")`` before streaming a response will
        not show "Thinking..." inline with that response.

        Args:
            text: One-line headline shown in the pill.
            detail: Optional longer body — multi-line content, structured
                progress, traceback excerpts, etc. The pill stays compact
                and the user expands it on demand.

        Channel adapters that prefer an in-band system message (e.g. Slack,
        Telegram) override this via ``_notify_callback``.
        """
        text = (text or "").strip()
        if not text and not detail:
            return
        if self._notify_callback:
            body = f"{text}\n\n{detail}".strip() if detail else text
            msg = Message(text=body, sender="system", channel_type=self.channel.type)
            await self._notify_callback(msg)
            return
        if self._block_callback is None:
            return
        payload: dict[str, Any] = {"text": text or "Working..."}
        if detail:
            payload["detail"] = detail
        # Single, replace-in-place pill per session — keeps the bubble clean.
        await self.show(
            Block(
                id=f"notify_{self.id}",
                type="notification",
                payload=payload,
            )
        )

    async def stream(self, chunks: AsyncIterator[str]) -> None:
        """Pipe an async iterator of text chunks to the client as a streaming reply.

        Each yielded string is sent immediately and displayed incrementally
        in the UI. For most use cases, prefer :meth:`stream_reply` (context
        manager) or :meth:`stream_reply_from` (one-liner for LLM streams).

        Args:
            chunks: Async iterator yielding text fragments.
        """
        if self._stream_callback:
            await self._stream_callback(chunks)

    def stream_reply(self) -> ReplyStream:
        """Open a streaming reply that sends chunks to the UI in real time.

        Usage::

            async with session.stream_reply() as s:
                s.write("## Report\\n\\n")
                async for token in llm_stream:
                    s.write(token)

        Each ``write`` sends text to the client immediately. The accumulated
        text is appended to session history when the block exits. Multiple
        ``stream_reply`` blocks can be used within a single handler.
        """
        if self._stream_reply_factory:
            return self._stream_reply_factory()
        if not self._stream_write_callback:
            raise RuntimeError("stream_reply is only available inside a message handler")
        return ReplyStream(
            self._stream_write_callback,
            self.history,
            self.channel.type,
            done_cb=self._stream_done_callback,
        )

    def chat_messages(self, current: Message, *, cls: Any = None) -> list:
        """Build a role-merged message list from history plus the current message.

        Maps ``sender="app"`` to ``role="assistant"`` and everything else
        to ``role="user"``.  Consecutive same-role entries are merged so
        the result always alternates roles (required by most LLM APIs).

        Pass ``cls=ChatMessage`` (or any type accepting ``role`` and
        ``content`` keyword arguments) to get back typed objects instead
        of plain dicts.
        """
        merged: list[dict[str, str]] = []
        for m in [*self.history, current]:
            role = "user" if m.sender == "user" else "assistant"
            if merged and merged[-1]["role"] == role:
                merged[-1]["content"] += m.text
            else:
                merged.append({"role": role, "content": m.text})
        if cls is not None:
            return [cls(**m) for m in merged]
        return merged

    async def stream_reply_from(self, stream: Any) -> str:
        """Pipe an async-iterable LLM stream through :meth:`stream_reply`.

        Handles cumulative snapshots (like BAML) and pure deltas equally
        because :class:`ReplyStream.write` auto-detects the format.
        Returns the full accumulated text.

        Usage::

            stream = b.stream.Chat(
                messages=session.chat_messages(msg, cls=ChatMessage),
                system_prompt=SYSTEM_PROMPT,
            )
            full_text = await session.stream_reply_from(stream)
        """
        async with self.stream_reply() as reply:
            async for partial in stream:
                if partial is not None:
                    reply.write(partial)
        return reply.text

    async def show(self, block: Block) -> None:
        """Render a structured block inline in the chat transport.

        The block is delivered as a one-shot chunk on the session's SSE
        stream and persisted in history so it replays on page reload. The
        block itself is stateless — renderers fetch live data (e.g.
        ``task_card`` re-reads ``/tasks/:id``).
        """
        if self._notify_callback and _is_external_channel(self.channel.type):
            if fallback := _external_block_fallback(block):
                await self._notify_callback(
                    Message(text=fallback, sender="system", channel_type=self.channel.type)
                )
        if not self._block_callback:
            return
        envelope = block.to_envelope()
        await self._block_callback(json.dumps(envelope))

    def terminal(
        self,
        name: str,
        *,
        title: str = "",
        cwd: str | None = None,
        env: dict[str, str] | None = None,
    ) -> Terminal:
        """Create or reopen a durable terminal transcript for this session."""
        return Terminal(self, name, title=title, cwd=cwd, env=env)

    async def show_terminal(
        self,
        *,
        title: str | None = None,
        name: str | None = None,
        terminal: Terminal | None = None,
        cwd: str | None = None,
        env: dict[str, str] | None = None,
    ) -> Terminal:
        """Render a terminal transcript and return its handle.

        Pass ``terminal=`` to show an existing named handle created with
        ``session.terminal("name")``. Without ``terminal=``, this creates a
        fresh one-off terminal unless ``name=`` is provided.
        """
        if terminal is not None:
            if terminal._session is not self:
                raise ValueError("terminal belongs to a different session")
            return await terminal.show(title=title)
        term = self.terminal(
            name or f"terminal_{uuid.uuid4().hex[:8]}",
            title=title or "Terminal",
            cwd=cwd,
            env=env,
        )
        return await term.show()

    async def show_task(self, handle_or_id: Any, *, message: str | None = None) -> None:
        """Render an inline card that tracks the given task's live state.

        Accepts a ``TaskHandle`` or raw task-id string. The card polls
        the task endpoint client-side, so we only have to name the task
        here — no payload snapshot is captured.

        ``message`` sets the card's headline (e.g. "Generating report…").
        When omitted, the card falls back to a humanized task name.
        """
        task_id = getattr(handle_or_id, "task_id", None) or str(handle_or_id)
        if not task_id:
            return
        payload: dict[str, Any] = {"task_id": task_id}
        if message:
            payload["message"] = message
        await self.show(Block(type="task_card", payload=payload))

    async def show_integration(self, integration_type: str, *, reason: str = "") -> None:
        """Render an inline Connect-Integration card without blocking.

        Useful when a handler wants to hint that an integration would
        unlock more functionality but can still proceed without it.
        """
        await self.show(
            Block(
                type="integration_prompt",
                payload={"type": integration_type, "reason": reason, "blocking": False},
            )
        )

    async def trigger_action(self, name: str, payload: dict[str, Any] | None = None) -> Any:
        """Run a named action inline using this session.

        Use this from a message, workflow start, or workflow message handler
        when a branch of logic should delegate to an existing action handler
        without creating another session or another transport request.

        Resolution matches the UI click path: workflow-backed sessions try
        the current workflow's ``@workflow.action(...)`` handlers first, then
        app-level ``@app.action(...)`` handlers. Regular chat sessions go
        straight to app actions.

        The action is awaited in the current handler lifecycle. Replies,
        streams, blocks, and ``session.data`` writes are emitted and persisted
        as part of the same turn.

        Args:
            name: Registered action name.
            payload: Optional JSON-like dict passed to the action.

        Returns:
            The action handler's return value, if any.
        """
        action_name = str(name or "").strip()
        if not action_name:
            raise ValueError("trigger_action requires a non-empty action name")
        if payload is not None and not isinstance(payload, dict):
            raise TypeError("trigger_action payload must be a dict")

        runner = _get_runner_for_session(self)
        dispatcher = getattr(runner, "_trigger_action", None) if runner is not None else None
        if dispatcher is None:
            raise RuntimeError("session.trigger_action requires an active runner session")
        result = dispatcher(self, action_name, dict(payload or {}))
        if asyncio.iscoroutine(result):
            return await result
        return result

    async def show_suggestions(self, suggestions: Any, *, title: str = "") -> None:
        """Show clickable next-step buttons in the current chat.

        Suggestions are persisted as an inline structured block, so they
        remain visible when the session history reloads. Clicking a prompt
        suggestion sends that prompt to the same session. Clicking an action
        suggestion posts the action to the same session and shows the normal
        chat thinking indicator until the action finishes.

        Accepted values:
            - ``"Research Acme"`` for a prompt suggestion.
            - ``cpsl.Suggestion("Approve", action="approve", payload={...})``.
            - Dicts using the frontend action shape:
              ``{"label": "...", "target": "prompt"|"action", "value": "..."}``.

        Args:
            suggestions: One suggestion or a list/tuple of suggestions.
            title: Optional short label shown above the buttons.
        """
        items = _serialize_chat_suggestions(suggestions)
        if not items:
            return
        payload: dict[str, Any] = {"suggestions": items}
        if title:
            payload["title"] = title
        await self.show(Block(type="suggestions", payload=payload))

    async def show_step(
        self,
        label: str,
        *,
        status: str = "running",
        detail: str = "",
        step_id: str | None = None,
        links: list[dict[str, Any]] | None = None,
        fields: dict[str, Any] | None = None,
        expanded: bool = False,
    ) -> str:
        """Render or update an inline step indicator in chat.

        Calls without ``step_id`` append a fresh timeline row, even when the
        label matches an earlier step. To update a row in place, keep the
        returned ``step_id`` and pass it back on the next call.

        Args:
            label: Short human-readable description ("Researching ICP").
            status: ``"running"``, ``"completed"``, ``"failed"``, or
                ``"skipped"``. Anything else is rendered as a generic step.
            detail: Optional expandable detail text.
            step_id: Stable identifier for updating an existing row. Omit it
                to append a new row.
            links: Optional list of ``{"label": str, "url": str}`` links.
            fields: Optional key/value metadata shown in expanded details.
            expanded: Whether rich details should start open.

        Returns:
            The resolved ``step_id``. Store it when you want later calls to
            update this same row.
        """
        sid = step_id or _timeline_item_id(label)
        block_id = f"step_{sid}"
        payload: dict[str, Any] = {
            "label": label,
            "status": status,
            "detail": detail,
            "step_id": sid,
            "expanded": bool(expanded),
        }
        normalized_links = _normalize_timeline_links(links)
        normalized_fields = _normalize_timeline_fields(fields)
        if normalized_links:
            payload["links"] = normalized_links
        if normalized_fields:
            payload["fields"] = normalized_fields
        await self.show(
            Block(
                id=block_id,
                type="step_status",
                payload=payload,
            )
        )
        return sid

    async def show_activity(
        self,
        label: str,
        *,
        detail: str = "",
        links: list[dict[str, Any]] | None = None,
        fields: dict[str, Any] | None = None,
        icon: str = "",
        activity_id: str | None = None,
        expanded: bool = False,
    ) -> str:
        """Render an append-only activity row with optional rich details.

        Use activities for completed observations such as "Opened source",
        "Stored graph", or "Found matching company" where there is no
        running/completed status transition. Calls without ``activity_id``
        append a fresh row. Reuse ``activity_id`` only when intentionally
        replacing a previous activity.

        Args:
            label: Short human-readable activity title.
            detail: Optional expandable detail text.
            links: Optional list of ``{"label": str, "url": str}`` links.
            fields: Optional key/value metadata shown in expanded details.
            icon: Optional icon name or short glyph for the row.
            activity_id: Stable identifier for replacing an existing row.
            expanded: Whether rich details should start open.

        Returns:
            The resolved ``activity_id``.
        """
        aid = activity_id or _timeline_item_id(label)
        payload: dict[str, Any] = {
            "label": label,
            "detail": detail,
            "activity_id": aid,
            "expanded": bool(expanded),
        }
        normalized_links = _normalize_timeline_links(links)
        normalized_fields = _normalize_timeline_fields(fields)
        if icon:
            payload["icon"] = str(icon)
        if normalized_links:
            payload["links"] = normalized_links
        if normalized_fields:
            payload["fields"] = normalized_fields
        await self.show(Block(id=f"activity_{aid}", type="activity", payload=payload))
        return aid

    async def show_browser(
        self,
        *,
        port: int = 0,
        url: str = "",
        title: str = "",
        path: str = "/",
        mode: str = "split",
    ) -> None:
        """Open a browser preview pane alongside the chat.

        The UI splits to show an iframe next to the conversation.
        Specify either ``port`` (proxied through the sandbox) or
        ``url`` (loaded directly in the iframe).

        When ``port`` is specified the runner registers a catch-all
        proxy so the UI can load the sandbox tunnel URL directly --
        every request that isn't a known runner API route gets forwarded
        to ``localhost:{port}`` transparently, avoiding path-prefix
        rewriting issues with dev servers like Vite.

        Args:
            port: Local port inside the sandbox to proxy.
            url: External URL to display.
            title: Toolbar label for the pane.
            path: Initial path appended to the proxied URL (port mode).
            mode: Layout mode -- ``"split"`` (50/50), ``"copilot"``
                (wide preview, chat narrow — the agent assists while
                you work in the browser), or ``"preview"`` (narrow
                preview, chat dominant — just a peek at the output).
        """
        if mode not in ("split", "copilot", "preview"):
            raise ValueError(f"mode must be 'split', 'copilot', or 'preview', got {mode!r}")
        payload: dict[str, Any] = {"title": title, "path": path, "mode": mode}
        if port:
            runner = _get_runner_for_session(self)
            if runner is not None:
                runner.set_preview_port(port)
            payload["port"] = port
        elif url:
            payload["url"] = url
        else:
            raise ValueError("show_browser requires either port= or url=")
        await self.show(Block(type="browser_preview", payload=payload))

    async def hide_browser(self) -> None:
        """Close the browser preview pane."""
        runner = _get_runner_for_session(self)
        if runner is not None:
            runner.set_preview_port(None)
        await self.show(Block(type="browser_preview", payload={"close": True}))

    async def show_table(
        self,
        table: Any = None,
        *,
        collection: Any = None,
        rows: list[dict[str, Any]] | None = None,
        data: str | None = None,
        columns: list[Any] | None = None,
        title: str = "",
        label: str | None = None,
        scope: str | None = None,
        sortable: bool = False,
        filterable: bool = False,
        paginate: int = 0,
        mode: str = "split",
    ) -> None:
        """Display tabular data inline or in a side pane.

        ``table`` may be a ``cpsl.ui.Table``/``TableBrowser``, a collection
        name/ref/dynamic collection, or a list of row dictionaries. Use
        ``mode="inline"`` to render directly in the chat. The ``"split"``,
        ``"copilot"``, and ``"preview"`` modes open the table on the right
        using the same layout ratios as :meth:`show_browser`.
        """
        if mode not in ("inline", "split", "copilot", "preview"):
            raise ValueError(
                f"mode must be 'inline', 'split', 'copilot', or 'preview', got {mode!r}"
            )

        widget = _table_widget_from_source(
            table,
            collection=collection,
            rows=rows,
            data=data,
            columns=columns,
            label=label,
            scope=scope,
            sortable=sortable,
            filterable=filterable,
            paginate=paginate,
        )
        payload: dict[str, Any] = {
            "title": title or _table_widget_title(widget),
            "mode": mode,
            "table": widget,
        }
        block_id = "" if mode == "inline" else _preview_block_id(self.id, "table_preview")
        await self.show(Block(type="table_preview", id=block_id, payload=payload))

    async def hide_table(self) -> None:
        """Close the table preview pane."""
        await self.show(
            Block(
                type="table_preview",
                id=_preview_block_id(self.id, "table_preview"),
                payload={"close": True},
            )
        )

    async def show_ui(
        self,
        ui: Any = None,
        *,
        component: str | None = None,
        page: str | None = None,
        props: dict[str, Any] | None = None,
        packages: list[str] | None = None,
        title: str = "",
        key: str = "",
        mode: str = "split",
    ) -> None:
        """Display a custom UI surface inline or in the split preview pane.

        ``ui`` may be a Python DSL widget (anything with ``to_dict()``) or
        a widget dict. Pass ``component=`` for a TSX component path, or
        ``page=`` for an existing app page name/route.
        """
        if mode not in ("inline", "split", "copilot", "preview"):
            raise ValueError(
                f"mode must be 'inline', 'split', 'copilot', or 'preview', got {mode!r}"
            )

        payload = _ui_preview_payload(
            ui,
            component=component,
            page=page,
            props=props,
            packages=packages,
            title=title,
            key=key,
            mode=mode,
        )
        await self.show(Block(type="ui_preview", payload=payload))

    async def hide_ui(self, key: str = "") -> None:
        """Close the custom UI preview pane."""
        payload: dict[str, Any] = {"close": True}
        if key:
            payload["key"] = key
        await self.show(Block(type="ui_preview", payload=payload))

    async def set_title(self, title: str) -> None:
        """Set the session title displayed in the sidebar.

        Can be called at any time — typically from a ``@workflow.start()``
        handler to give the run a human-readable name based on its inputs.
        """
        await self.show(Block(type="session_title", payload={"title": title}))

    async def show_image(
        self,
        source: str,
        *,
        alt: str = "",
        width: int | None = None,
    ) -> None:
        """Display an image inline in the chat.

        Args:
            source: URL (``http://``, ``https://``, ``data:``) or local
                file path. Local paths are auto-uploaded through the
                gateway and converted to presigned URLs.
            alt: Alt text for the image.
            width: Optional display width in pixels.
        """
        url = source
        if not source.startswith(("http://", "https://", "data:")):
            url = await self._upload_local_file(source)

        payload: dict[str, Any] = {"url": url}
        if alt:
            payload["alt"] = alt
        if width is not None:
            payload["width"] = width
        await self.show(Block(type="image", payload=payload))

    async def prompt_approval(
        self,
        message: str,
        *,
        approve_label: str = "Approve",
        reject_label: str = "Reject",
        timeout: float = 300.0,
    ) -> bool:
        """Block until the user approves or rejects a request.

        Shows an inline approval prompt in chat and returns ``True`` only
        when the user explicitly approves. Rejection and timeout return
        ``False``.
        """
        block_id = f"ap_{uuid.uuid4().hex[:12]}"
        prompt_text = (message or "").strip()
        await self.show(
            Block(
                type="approval_prompt",
                id=block_id,
                payload={
                    "message": prompt_text,
                    "approve_label": approve_label,
                    "reject_label": reject_label,
                    "blocking": True,
                    "session_id": self.id,
                },
            )
        )

        stub = self._session_stub
        if stub is None:
            runner = _get_runner_for_session(self)
            if runner is not None:
                stub = runner._session_stub
        if stub is None:
            return False

        from .clients.capsule import WaitForApprovalRequest

        req = WaitForApprovalRequest(
            session_id=self.id,
            block_id=block_id,
            timeout_seconds=int(timeout),
        )

        resp = await _run_blocking(lambda: stub.wait_for_approval(req))
        approved = bool(resp.approved) and not bool(resp.timed_out)

        await self.show(
            Block(
                type="approval_prompt",
                id=block_id,
                payload={
                    "message": prompt_text,
                    "approve_label": approve_label,
                    "reject_label": reject_label,
                    "completed": True,
                    "approved": approved,
                    "timed_out": bool(resp.timed_out),
                },
            )
        )
        return approved

    async def _upload_local_file(
        self,
        path: str,
        *,
        filename: str | None = None,
        content_type: str | None = None,
    ) -> str:
        """Read a local file and upload it via the runner's UploadFile gRPC."""
        import mimetypes
        import os

        stub = self._runner_stub
        app_id = self._app_id
        if stub is None:
            runner = _get_runner_for_session(self)
            if runner is not None:
                stub = runner._runner_stub
                app_id = getattr(runner, "_app_id", "") or ""
        if stub is None:
            raise RuntimeError("no gateway connection available for file upload")

        filename = filename or os.path.basename(path)
        content_type = content_type or mimetypes.guess_type(path)[0] or "application/octet-stream"

        with open(path, "rb") as f:
            data = f.read()

        from .clients.capsule import UploadFileRequest

        def _call():
            return stub.upload_file(
                UploadFileRequest(
                    app_id=app_id,
                    session_id=self.id,
                    filename=filename,
                    content_type=content_type,
                    data=data,
                )
            )

        resp = await asyncio.get_running_loop().run_in_executor(None, _call)
        return resp.url

    async def prompt_file(
        self,
        *,
        message: str = "Please upload a file",
        accept: str = "",
        path: str | None = None,
        timeout: float = 300.0,
    ) -> FileUpload:
        """Block until the user uploads a file, then return its metadata.

        Shows an inline upload widget in the chat. The handler suspends
        until the user selects and uploads a file or the timeout elapses.

        Args:
            message: Prompt text shown above the upload widget.
            accept: Comma-separated file type filter (e.g. ``"image/*,.pdf"``).
            path: If provided, the uploaded file is automatically downloaded
                to this local path (or directory). When *path* is a directory
                the original filename is appended. The resulting path is
                available on the returned ``FileUpload.path``.
            timeout: Seconds to wait before raising ``FileUploadTimeout``.

        Returns:
            A :class:`FileUpload` with ``name``, ``content_type``, ``url``,
            ``size``, and ``path`` (when auto-downloaded).

        Raises:
            FileUploadTimeout: The user did not upload a file in time.
        """
        import os

        block_id = f"fu_{uuid.uuid4().hex[:12]}"
        payload: dict[str, Any] = {
            "message": message,
            "blocking": True,
            "session_id": self.id,
        }
        if accept:
            payload["accept"] = accept

        await self.show(Block(type="file_upload", id=block_id, payload=payload))

        stub = self._session_stub
        app_id = self._app_id
        if stub is None:
            runner = _get_runner_for_session(self)
            if runner is not None:
                stub = runner._session_stub
                app_id = getattr(runner, "_app_id", "") or ""
        if stub is None:
            raise RuntimeError("no gateway connection available for file upload prompt")

        from .clients.capsule import WaitForFileUploadRequest

        req = WaitForFileUploadRequest(
            app_id=app_id,
            session_id=self.id,
            block_id=block_id,
            timeout_seconds=int(timeout),
        )

        resp = await _run_blocking(lambda: stub.wait_for_file_upload(req))

        if resp.timed_out:
            raise FileUploadTimeout("timed out waiting for file upload")

        upload = FileUpload(
            name=resp.filename,
            content_type=resp.content_type,
            url=resp.url,
            size=resp.size,
        )

        await self.show(
            Block(
                type="file_upload",
                id=block_id,
                payload={
                    "completed": True,
                    "filename": resp.filename,
                    "content_type": resp.content_type,
                    "size": resp.size,
                },
            )
        )

        if path is not None:
            dest = path
            if os.path.isdir(dest):
                dest = os.path.join(dest, upload.name)
            os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
            await upload.download(dest)

        return upload

    async def prompt_integration(
        self,
        integration_type: str | IntegrationConfig,
        *,
        reason: str = "",
        message: str | None = None,
        timeout: float = 300.0,
    ) -> IntegrationCredentials:
        """Block until the user connects an integration, then return credentials.

        For OAuth integrations the user completes a redirect flow. For
        secret-based integrations (``tailscale``, ``aws``, …) the user
        fills in a credential form and the sandbox environment is configured
        automatically before this returns.

        Idempotent — returns immediately if already connected.
        """
        from .clients.capsule import WaitForIntegrationRequest

        integration_type = normalize_integration_type(integration_type)

        existing = self.integrations.get(integration_type)
        if existing:
            return existing

        is_secret = integration_type in KNOWN_SECRET_INTEGRATIONS
        prompt_message = reason if message is None else message
        if prompt_message:
            await self.reply(prompt_message)

        await self.show(
            Block(
                type="integration_prompt",
                payload={
                    "type": integration_type,
                    "reason": "" if prompt_message == reason else reason,
                    "blocking": True,
                    "mode": "secret" if is_secret else "oauth",
                },
            )
        )

        stub = self._session_stub
        app_id = self._app_id
        if stub is None:
            runner = _get_runner_for_session(self)
            if runner is not None:
                stub = runner._session_stub
                app_id = getattr(runner, "_app_id", "") or ""
        if stub is None:
            raise IntegrationDeclined(
                f"no gateway connection available to prompt for '{integration_type}'"
            )

        req = WaitForIntegrationRequest(
            app_id=app_id,
            user_id=self.user.email or self.user.id or "",
            integration_type=integration_type,
            timeout_seconds=int(timeout),
        )

        def _call():
            return stub.wait_for_integration(req)

        resp = await asyncio.get_running_loop().run_in_executor(None, _call)

        if resp.timed_out:
            raise IntegrationTimeout(f"timed out waiting for '{integration_type}' connection")
        if not resp.connected:
            raise IntegrationDeclined(f"user did not connect '{integration_type}'")

        cred = credentials_from_wire(
            integration_type=integration_type,
            access_token=resp.credential.access_token,
            token_type=resp.credential.token_type,
            scopes=list(resp.credential.scopes),
            expires_at=resp.credential.expires_at,
        )
        self.integrations[integration_type] = cred

        if is_secret and cred.fields:
            await _activate_integration(integration_type, cred.fields)

        return cred

    def get_integration(self, integration: IntegrationLike) -> IntegrationCredentials | None:
        """Return connected credentials for an integration type/config, if present."""
        return self.integrations.get(normalize_integration_type(integration))

    def pipedream(self, integration: IntegrationLike):
        """Return a requests-like session for a Pipedream-backed integration."""
        from .pipedream import PipedreamProxySession

        stub = self._session_stub
        app_id = self._app_id
        env = ""
        if stub is None:
            runner = _get_runner_for_session(self)
            if runner is not None:
                stub = runner._session_stub
                app_id = getattr(runner, "_app_id", "") or ""
                env = getattr(runner, "_version_type", "") or ""
        if stub is None:
            raise RuntimeError(
                f"no gateway connection available for Pipedream integration '{normalize_integration_type(integration)}'"
            )
        return PipedreamProxySession(
            stub=stub,
            app_id=app_id,
            user_email=self.user.email or "",
            owner_id=self.user.owner_id,
            integration=integration,
            env=env,
        )

    async def require_integration(
        self,
        integration: IntegrationLike,
        *,
        reason: str = "",
        message: str | None = None,
        timeout: float = 300.0,
    ) -> IntegrationCredentials:
        """Return credentials, prompting the user to connect when missing."""
        existing = self.get_integration(integration)
        if existing:
            return existing
        return await self.prompt_integration(
            normalize_integration_type(integration),
            reason=reason,
            message=message,
            timeout=timeout,
        )


class IntegrationTimeout(TimeoutError):
    """Raised when ``session.prompt_integration`` times out."""


class IntegrationDeclined(RuntimeError):
    """Raised when the user explicitly declines an integration prompt."""


def _table_widget_from_source(
    table: Any = None,
    *,
    collection: Any = None,
    rows: list[dict[str, Any]] | None = None,
    data: str | None = None,
    columns: list[Any] | None = None,
    label: str | None = None,
    scope: str | None = None,
    sortable: bool = False,
    filterable: bool = False,
    paginate: int = 0,
) -> dict[str, Any]:
    from . import ui as _ui

    collection_source = collection
    row_source = rows

    if table is not None:
        to_dict = getattr(table, "to_dict", None)
        if callable(to_dict):
            widget = to_dict()
            if not isinstance(widget, dict) or widget.get("type") not in {
                "table",
                "table_browser",
            }:
                raise TypeError(
                    "show_table accepts cpsl.ui.Table or cpsl.ui.TableBrowser widgets"
                )
            return _json_safe_value(widget)
        if isinstance(table, (list, tuple)):
            if rows is not None:
                raise ValueError("pass rows either positionally or with rows=, not both")
            row_source = list(table)
        else:
            if collection is not None:
                raise ValueError(
                    "pass a collection either positionally or with collection=, not both"
                )
            collection_source = table

    if collection_source is not None and (row_source is not None or data is not None):
        raise ValueError("show_table accepts one data source: collection, rows, or data")
    if row_source is not None and data is not None:
        raise ValueError("show_table accepts one data source: rows or data")

    if collection_source is not None:
        collection_arg, inferred_scope = _table_collection_arg(collection_source)
        widget = _ui.Table(
            collection_arg,
            columns=columns,
            label=label,
            scope=scope or inferred_scope,
            sortable=sortable,
            filterable=filterable,
            paginate=paginate,
        ).to_dict()
        return _json_safe_value(widget)

    if row_source is not None or data is not None:
        widget = _ui.Table(
            data=data,
            rows=list(row_source) if row_source is not None else None,
            columns=columns,
            label=label,
            sortable=sortable,
            filterable=filterable,
            paginate=paginate,
        ).to_dict()
        return _json_safe_value(widget)

    raise ValueError("show_table requires a table widget, collection, data source, or rows")


def _table_collection_arg(source: Any) -> tuple[Any, str | None]:
    from .db import CollectionRef

    if isinstance(source, (str, CollectionRef)):
        return source, None

    name = getattr(source, "name", None)
    if isinstance(name, str) and name:
        scope = getattr(source, "scope", None)
        return name, scope if isinstance(scope, str) else None

    raw_name = getattr(source, "_name", None)
    if isinstance(raw_name, str) and raw_name:
        return raw_name, None

    inner = getattr(source, "_inner", None)
    inner_name = getattr(inner, "_name", None)
    if isinstance(inner_name, str) and inner_name:
        scope_filter = getattr(source, "_scope_filter", None)
        inferred_scope = None
        if isinstance(scope_filter, dict):
            if SCOPE_FIELD_SESSION in scope_filter:
                inferred_scope = "session"
            elif SCOPE_FIELD_OWNER in scope_filter:
                inferred_scope = "owner"
            elif SCOPE_FIELD_USER in scope_filter:
                inferred_scope = "user"
        return inner_name, inferred_scope

    raise TypeError(
        "collection must be a name, CollectionRef, DynamicCollection, or collection handle"
    )


def _table_widget_title(widget: dict[str, Any]) -> str:
    explicit = widget.get("title") or widget.get("label")
    if explicit:
        return str(explicit)
    if widget.get("type") == "table_browser":
        return "Tables"
    source = widget.get("collection") or widget.get("collection_ref") or widget.get("data")
    if isinstance(source, str) and source:
        return source.replace("_", " ").replace("-", " ").title()
    return "Table"


def _ui_preview_payload(
    ui: Any = None,
    *,
    component: str | None = None,
    page: str | None = None,
    props: dict[str, Any] | None = None,
    packages: list[str] | None = None,
    title: str = "",
    key: str = "",
    mode: str = "split",
) -> dict[str, Any]:
    sources = [ui is not None, component is not None, page is not None]
    if sum(1 for present in sources if present) != 1:
        raise ValueError("show_ui accepts exactly one source: ui, component, or page")

    payload: dict[str, Any] = {"mode": mode}
    if title:
        payload["title"] = title
    if key:
        payload["key"] = key
    if props is not None:
        payload["props"] = _json_safe_value(props)

    if ui is not None:
        widget = _ui_widget_from_source(ui)
        payload["kind"] = "widget"
        payload["widget"] = widget
        if "title" not in payload:
            payload["title"] = _ui_widget_title(widget)
        return payload

    if component is not None:
        component_path = component.strip()
        if not component_path:
            raise ValueError("show_ui component path must not be empty")
        payload["kind"] = "component"
        payload["component"] = component_path
        if packages:
            payload["packages"] = [str(pkg) for pkg in packages if str(pkg).strip()]
        if "title" not in payload:
            payload["title"] = component_path.rsplit("/", 1)[-1].rsplit(".", 1)[0] or "Custom UI"
        return payload

    page_name = (page or "").strip()
    if not page_name:
        raise ValueError("show_ui page must not be empty")
    payload["kind"] = "page"
    payload["page"] = page_name
    if "title" not in payload:
        payload["title"] = page_name
    return payload


def _ui_widget_from_source(ui: Any) -> dict[str, Any]:
    to_dict = getattr(ui, "to_dict", None)
    if callable(to_dict):
        widget = to_dict()
    elif isinstance(ui, dict):
        widget = ui
    else:
        raise ValueError("show_ui ui must be a cpsl.ui widget or widget dict")

    if not isinstance(widget, dict) or not isinstance(widget.get("type"), str):
        raise ValueError("show_ui widget must serialize to a widget dict with a type")
    return _json_safe_value(widget)


def _ui_widget_title(widget: dict[str, Any]) -> str:
    explicit = widget.get("title") or widget.get("label")
    if explicit:
        return str(explicit)
    typ = str(widget.get("type") or "UI")
    if typ == "page":
        return "Custom UI"
    return typ.replace("_", " ").replace("-", " ").title()


def _serialize_chat_suggestions(value: Any) -> list[dict[str, Any]]:
    """Normalize ``session.show_suggestions`` input for the chat block.

    Chat suggestions intentionally support only same-session operations:
    prompt sends and action clicks. Home-only navigation targets are rejected
    here so a chat button never silently navigates away from the current
    workflow or conversation.
    """
    if value is None:
        return []
    values = value if isinstance(value, (list, tuple)) else [value]
    out: list[dict[str, Any]] = []
    allowed = {
        "label",
        "target",
        "value",
        "description",
        "icon",
        "image",
        "accent",
        "primary",
        "payload",
    }
    for item in values:
        if isinstance(item, str):
            text = item.strip()
            if text:
                out.append({"label": text, "target": "prompt", "value": text})
            continue

        to_dict = getattr(item, "to_dict", None)
        if callable(to_dict) and not isinstance(item, dict):
            raw = to_dict()
        elif isinstance(item, dict):
            raw = dict(item)
        else:
            raise TypeError(
                f"suggestion must be a string, Suggestion, or dict, got {type(item).__name__}"
            )
        if not isinstance(raw, dict):
            raise TypeError("suggestion to_dict() must return a dict")

        target = str(raw.get("target") or "").strip()
        label = str(raw.get("label") or "").strip()
        action_value = str(raw.get("value") or "").strip()
        if target not in {"prompt", "action"}:
            raise ValueError("session.show_suggestions supports target='prompt' or target='action'")
        if not label or not action_value:
            raise ValueError("suggestion requires non-empty label and value")

        suggestion = {key: _json_safe_value(raw[key]) for key in allowed if key in raw}
        suggestion["target"] = target
        suggestion["label"] = label
        suggestion["value"] = action_value
        if "payload" in suggestion and not isinstance(suggestion["payload"], dict):
            raise ValueError("suggestion payload must be a dict")
        out.append(suggestion)
    return out


class FileUploadTimeout(TimeoutError):
    """Raised when ``session.prompt_file`` times out."""


def _is_external_channel(channel_type: str) -> bool:
    return channel_type not in ("", "chat", "api")


def _external_block_fallback(block: Block) -> str:
    payload = block.payload or {}
    typ = block.type

    if typ == "file_upload":
        if payload.get("completed"):
            filename = payload.get("filename") or "file"
            return f"File upload received: {filename}"
        message = payload.get("message") or "Please upload a file."
        return (
            f"{message}\n\n"
            "If you're using Telegram, send the file here as your next message. "
            "You can also open the web chat to use the upload widget."
        )

    if typ == "integration_prompt":
        integration = payload.get("type") or "the requested integration"
        reason = payload.get("reason") or ""
        prefix = f"{reason}\n\n" if reason else ""
        action = "connect this integration" if payload.get("blocking") else "connect it"
        return (
            f"{prefix}Open the web app to {action}: {integration}. "
            "Telegram cannot complete this connection inline."
        )

    if typ == "approval_prompt":
        if payload.get("completed"):
            if payload.get("timed_out"):
                return "Approval timed out."
            return "Approved." if payload.get("approved") else "Not approved."
        message = payload.get("message") or "Approval requested."
        approve = payload.get("approve_label") or "Approve"
        reject = payload.get("reject_label") or "Reject"
        return (
            f"{message}\n\n"
            f"Open the web app to choose {approve} or {reject}. "
            "Telegram cannot complete this approval inline."
        )

    if typ == "task_card":
        message = payload.get("message") or "Task started."
        return str(message)
    if typ == "terminal":
        return str(payload.get("title") or "Terminal output is available in the web app.")
    if typ == "table_preview":
        if payload.get("close"):
            return "Table preview closed."
        return str(payload.get("title") or "Table is available in the web app.")
    if typ == "ui_preview":
        if payload.get("close"):
            return "UI preview closed."
        return str(payload.get("title") or "Custom UI is available in the web app.")

    return ""


async def _activate_integration(integration_type: str, fields: dict[str, str]) -> None:
    """Configure the sandbox environment for a secret-based integration.

    Called both mid-turn (after ``prompt_integration``) and at boot (for
    already-connected integrations). The caller is responsible for supplying
    the decrypted field values.
    """
    import logging
    import os
    import shutil
    import subprocess as _sp

    log = logging.getLogger("cpsl.integration")

    if integration_type == "tailscale":
        auth_key = fields.get("auth_key", "")
        if not auth_key:
            raise RuntimeError("tailscale integration missing auth_key")

        if shutil.which("tailscaled") is None or shutil.which("tailscale") is None:
            raise RuntimeError("tailscale binaries not found")

        log.info("starting tailscaled (userspace networking)")
        _sp.Popen(
            [
                "tailscaled",
                "--tun=userspace-networking",
                "--socks5-server=localhost:1080",
                "--state=mem:",
            ],
            stdout=_sp.DEVNULL,
            stderr=_sp.DEVNULL,
        )

        await asyncio.sleep(1)

        up_cmd = ["tailscale", "up", f"--authkey={auth_key}"]
        advertise_tags = fields.get("advertise_tags", "")
        if advertise_tags:
            up_cmd.append(f"--advertise-tags={advertise_tags}")

        _sp.run(
            up_cmd,
            timeout=30,
            check=True,
            capture_output=True,
        )

        ready = False
        last_status = ""
        for _ in range(20):
            result = _sp.run(
                ["tailscale", "status", "--json"],
                capture_output=True,
                timeout=5,
            )
            if result.returncode == 0:
                last_status = result.stdout.decode("utf-8", errors="replace")
                try:
                    status = json.loads(last_status)
                    if status.get("BackendState") == "Running":
                        ready = True
                        break
                except (json.JSONDecodeError, TypeError):
                    pass
            await asyncio.sleep(0.5)

        if not ready:
            raise RuntimeError(
                "tailscale integration did not reach Running state"
                + (f": {last_status}" if last_status else "")
            )

        os.environ["ALL_PROXY"] = "socks5://localhost:1080"
        os.environ["HTTP_PROXY"] = "socks5://localhost:1080"
        os.environ["HTTPS_PROXY"] = "socks5://localhost:1080"
        log.info("tailscale tunnel ready — SOCKS5 proxy on :1080")

    elif integration_type == "aws":
        if fields.get("access_key_id"):
            os.environ["AWS_ACCESS_KEY_ID"] = fields["access_key_id"]
        if fields.get("secret_access_key"):
            os.environ["AWS_SECRET_ACCESS_KEY"] = fields["secret_access_key"]
        if fields.get("region"):
            os.environ["AWS_DEFAULT_REGION"] = fields["region"]
        log.info("aws credentials injected into environment")

    else:
        log.debug("no activation handler for integration type %r", integration_type)


def _get_runner_for_session(session: "Session"):
    """Return the active ``Runner``, avoiding a circular import."""
    return getattr(session, "_runner", None)


def _timeline_item_id(label: str) -> str:
    return f"{_slugify_step_label(label)}_{uuid.uuid4().hex[:8]}"


def _normalize_timeline_links(links: list[dict[str, Any]] | None) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for item in links or []:
        if not isinstance(item, dict):
            continue
        label = str(item.get("label") or item.get("title") or item.get("url") or "").strip()
        url = str(item.get("url") or item.get("href") or "").strip()
        if label and url:
            out.append({"label": label, "url": url})
    return out


def _normalize_timeline_fields(fields: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(fields, dict):
        return {}
    return {str(key): _json_safe_value(value) for key, value in fields.items()}


def _slugify_step_label(label: str) -> str:
    """Derive the readable prefix used in generated timeline ids."""
    out: list[str] = []
    for ch in (label or "").lower():
        if ch.isalnum():
            out.append(ch)
        elif out and out[-1] != "_":
            out.append("_")
    slug = "".join(out).strip("_")
    return slug or uuid.uuid4().hex[:10]


def _terminal_block_id(session_id: str, name: str) -> str:
    raw = f"{session_id}:{name}".encode()
    return "term_" + hashlib.sha1(raw).hexdigest()[:16]


def _preview_block_id(session_id: str, name: str) -> str:
    raw = f"{session_id}:{name}".encode()
    return "preview_" + hashlib.sha1(raw).hexdigest()[:16]


def _derive_media_filename(source: Any, fallback: str) -> str:
    if isinstance(source, str):
        path = urlparse(source).path if _is_remote_url(source) else source
        name = path.rsplit("/", 1)[-1]
        if name:
            return name
    return fallback


def current_session() -> Session | None:
    """Return the active handler session, if the current context has one.

    Message handlers return the live chat/API session. Scheduled handlers and
    background tasks without a bound chat session return a synthetic runtime
    session with owner-scoped identity and integrations, but no reply target.
    """
    identity = get_active_identity()
    return identity if isinstance(identity, Session) else None


def pipedream(integration: IntegrationLike):
    """Return a requests-like session for the active Capsule identity."""
    identity = get_active_identity()
    if hasattr(identity, "pipedream"):
        return identity.pipedream(integration)
    raise RuntimeError("no active Capsule session")
