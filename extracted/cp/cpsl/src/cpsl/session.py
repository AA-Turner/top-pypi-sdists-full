from __future__ import annotations

import asyncio
import hashlib
import json
import uuid
from collections.abc import AsyncIterator, Callable
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

from .constants import (
    KV_KEY_FIELD,
    SCOPE_FIELD_OWNER, SCOPE_FIELD_SESSION, SCOPE_FIELD_USER,
)
from .db import Collection, CollectionManager, ScopedDatabaseProxy, get_active_identity
from .integration import (
    IntegrationConfig,
    IntegrationCredentials,
    IntegrationLike,
    KNOWN_SECRET_INTEGRATIONS,
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


class _TrackedDict(dict):
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


def _track_data_value(value: Any, notify: Callable[[], None] | None) -> Any:
    if isinstance(value, _TrackedDict) or isinstance(value, _TrackedList):
        value._notify = notify
        return value
    if isinstance(value, dict):
        return _TrackedDict(value, notify)
    if isinstance(value, list):
        return _TrackedList(value, notify)
    return value


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
            delta = text[len(self._full):]
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

    __slots__ = ("user", "integrations", "authenticated", "request")

    def __init__(
        self,
        user: UserInfo,
        integrations: dict[str, IntegrationCredentials],
        authenticated: bool = False,
        request: Any = None,
    ) -> None:
        self.user = user
        self.integrations = integrations
        self.authenticated = authenticated
        self.request = request


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
                return await self._session._upload_local_file(temp_path, filename=name, content_type=content_type), content_type
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
                    content_type = mime_type or resp.headers.get("content-type", "").split(";")[0] or "application/octet-stream"
                    suffix = mimetypes.guess_extension(content_type) or ""
                    name = filename or _derive_media_filename(source, f"media-{uuid.uuid4().hex[:10]}{suffix}")
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
                        async for chunk in resp.content.iter_chunked(8192):
                            f.write(chunk)
                        temp_path = f.name
            try:
                return await self._session._upload_local_file(temp_path, filename=name, content_type=content_type), content_type
            finally:
                try:
                    os.unlink(temp_path)
                except OSError:
                    pass

        path = os.fspath(source)
        content_type = mime_type or mimetypes.guess_type(path)[0] or "application/octet-stream"
        name = filename or os.path.basename(path)
        return await self._session._upload_local_file(path, filename=name, content_type=content_type), content_type


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
                run["chunks"].append({
                    "stream": stream_name,
                    "text": text,
                    "timestamp": _now_ms(),
                    "seq": seq,
                })
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
        "_stream_reply_factory",
        "_notify_callback",
        "_block_callback",
        "_data_change_callback",
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
        self.history: list[Message] = history or []
        self.data: dict[str, Any] = _track_data_value(data or {}, self._notify_data_changed)
        self.integrations: dict[str, IntegrationCredentials] = integrations or {}
        self.media = SessionMedia(self)
        self._reply_callback: Any = None
        self._stream_callback: Any = None
        self._stream_write_callback: Any = None
        self._stream_reply_factory: Any = None
        self._notify_callback: Any = None
        self._block_callback: Any = None
        self._data_change_callback: Any = None
        self._db_proxy: ScopedDatabaseProxy | None = None
        self._collections_proxy: CollectionManager | None = None
        self._runner: Any = None
        self._runner_stub: Any = None
        self._session_stub: Any = None
        self._app_id: str = ""
        self._kv: Collection | None = None

    def _notify_data_changed(self) -> None:
        cb = self._data_change_callback
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
        return ReplyStream(self._stream_write_callback, self.history, self.channel.type)

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

    async def show_task(
        self, handle_or_id: Any, *, message: str | None = None
    ) -> None:
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

    async def show_step(
        self,
        label: str,
        *,
        status: str = "running",
        detail: str = "",
        step_id: str | None = None,
    ) -> str:
        """Render or update an inline step indicator in chat.

        Pass the same ``step_id`` (or the same ``label`` when no id is given)
        across calls to update a single step in place — for example, calling
        with ``status="running"`` then ``status="completed"`` shows one row
        that transitions, not two.

        Args:
            label: Short human-readable description ("Researching ICP").
            status: ``"running"``, ``"completed"``, ``"failed"``, or
                ``"skipped"``. Anything else is rendered as a generic step.
            detail: Optional secondary line ("Found 18 matching accounts").
            step_id: Stable identifier across calls. Defaults to a slug of
                ``label`` so passing the same label updates the same step.

        Returns:
            The resolved ``step_id`` so callers can chain updates without
            re-deriving it.
        """
        sid = step_id or _slugify_step_label(label)
        block_id = f"step_{sid}"
        await self.show(
            Block(
                id=block_id,
                type="step_status",
                payload={
                    "label": label,
                    "status": status,
                    "detail": detail,
                    "step_id": sid,
                },
            )
        )
        return sid

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

        await self.show(Block(
            type="file_upload",
            id=block_id,
            payload={
                "completed": True,
                "filename": resp.filename,
                "content_type": resp.content_type,
                "size": resp.size,
            },
        ))

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

        # Secret-based integrations pack field values as JSON in access_token.
        secret_fields: dict[str, str] = {}
        if is_secret and resp.credential.access_token:
            try:
                secret_fields = json.loads(resp.credential.access_token)
            except (json.JSONDecodeError, TypeError):
                pass

        cred = IntegrationCredentials(
            access_token="" if is_secret else resp.credential.access_token,
            token_type=resp.credential.token_type or "Bearer",
            scopes=list(resp.credential.scopes),
            expires_at=resp.credential.expires_at,
            fields=secret_fields,
        )
        self.integrations[integration_type] = cred

        if is_secret and secret_fields:
            await _activate_integration(integration_type, secret_fields)

        return cred

    def get_integration(self, integration: IntegrationLike) -> IntegrationCredentials | None:
        """Return connected credentials for an integration type/config, if present."""
        return self.integrations.get(normalize_integration_type(integration))

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
            log.warning("tailscale integration missing auth_key")
            return

        if shutil.which("tailscaled") is None:
            log.error("tailscaled binary not found — is Tailscale installed in the image?")
            return

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

        _sp.run(
            ["tailscale", "up", f"--authkey={auth_key}"],
            timeout=30,
            check=True,
            capture_output=True,
        )

        for _ in range(20):
            result = _sp.run(
                ["tailscale", "status", "--json"],
                capture_output=True,
                timeout=5,
            )
            if result.returncode == 0:
                try:
                    status = json.loads(result.stdout)
                    if status.get("BackendState") == "Running":
                        break
                except (json.JSONDecodeError, TypeError):
                    pass
            await asyncio.sleep(0.5)

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


def _slugify_step_label(label: str) -> str:
    """Derive a stable id from a step label.

    Used so callers can pass the same ``label`` across ``show_step`` updates
    and have a single inline row transition between states, rather than each
    call appending a new card.
    """
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
