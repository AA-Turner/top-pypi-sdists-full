"""Coordinate staged Session uploads and sandbox copies before message admission."""

import asyncio
import mimetypes
import posixpath
import time
from collections.abc import AsyncIterator, Callable, Sequence
from contextlib import aclosing, asynccontextmanager
from dataclasses import replace
from pathlib import Path
from urllib.parse import quote
from uuid import uuid4

from pydantic import JsonValue

from mistralai.vibe.harness.app_server.session import (
    SessionMessageRejectedError,
    SessionTerminatedError,
    UnsupportedSessionProcedureError,
)
from mistralai.vibe.harness.app_server.session.file_sources import iter_file_source, sanitize_filename
from mistralai.vibe.harness.app_server.session.models.content import ResourceLinkContentBlock
from mistralai.vibe.harness.core import protocol as core_protocol
from mistralai.vibe.harness.runtime.hosts.workflows import WorkflowSandboxResource
from mistralai.vibe.harness.runtime.hosts.workflows.sandbox_files import (
    FileSource,
    ResolvedFile,
    ResolvedFiles,
    WorkflowSandboxWriteFilesRequest,
    register_file_resolver,
)

from .session_files import (
    DEFAULT_SESSION_FILE_POLICY,
    InMemorySessionFileCatalog,
    JsonFileSessionFileCatalog,
    LocalSessionFileStore,
    SessionFileCatalog,
    SessionFilePolicy,
    SessionFileRecord,
    SessionFileStore,
)

SESSION_INPUTS_ROOT = "/session-inputs"
"""The logical sandbox root of uploaded Session Files; each driver declares where it lives."""

SESSION_FILE_RESOLVER = "agents-sdk-session-files"
_STORES: dict[str, SessionFileStore] = {}


async def _resolve_session_file(refs: JsonValue) -> ResolvedFiles:
    if not isinstance(refs, dict):
        raise ValueError("Session file references must be an object")
    store_reference, file_id, name = refs.get("store"), refs.get("file_id"), refs.get("name")
    if not isinstance(store_reference, str) or not isinstance(file_id, str) or not isinstance(name, str):
        raise ValueError("Session file references are incomplete")
    store = _STORES.get(store_reference)
    if store is None:
        raise RuntimeError("The Session file store is not open in this process")
    return ResolvedFiles(files=(ResolvedFile(path=posixpath.join(file_id, name), content=await store.read(file_id)),))


register_file_resolver(SESSION_FILE_RESOLVER, _resolve_session_file)


def session_file_uri(inputs_root: str, file_id: str, name: str) -> str:
    return _file_uri(posixpath.join(inputs_root, file_id, name))


def _file_uri(path: str) -> str:
    return "file://" + quote(path)


class LocalSessionFileManager:
    """Coordinate one root Session's file store, metadata catalog and sandbox copies.

    Uploads snapshot bytes in the store and register metadata in the catalog,
    returning links without creating sandbox files. Before message admission,
    referenced links are looked up in the catalog and their stored bytes are
    copied into the sandbox. Accepted messages retain the snapshots for reuse.

    The manager limits the number of uploads and removes expired staged snapshots.
    Children share the root's file state and sandbox. Files survive client detach
    and idle unload; Session disposal closes the store, which removes its snapshots
    unless the store is saved for a later process (see ``for_saved_sandbox``).
    """

    def __init__(
        self,
        sandbox: WorkflowSandboxResource,
        inputs_root: str,
        *,
        policy: SessionFilePolicy = DEFAULT_SESSION_FILE_POLICY,
        store: SessionFileStore | None = None,
        catalog: SessionFileCatalog | None = None,
        clock: Callable[[], float] | None = None,
    ) -> None:
        self._inputs_root = inputs_root
        self._policy = policy
        self._store = store if store is not None else LocalSessionFileStore()
        self._catalog = catalog if catalog is not None else InMemorySessionFileCatalog()
        self._clock = clock or (lambda: time.monotonic())
        self._sandbox = sandbox
        self._lock = asyncio.Lock()
        self._uploads: set[asyncio.Task[ResourceLinkContentBlock]] = set()
        self._reserved_files = 0
        self._prepared: dict[str, int] = {}
        self._closed = False
        _STORES[self._store.reference] = self._store

    @classmethod
    def for_sandbox(
        cls, sandbox: WorkflowSandboxResource, policy: SessionFilePolicy = DEFAULT_SESSION_FILE_POLICY
    ) -> "LocalSessionFileManager | None":
        """Use disk staging when the driver declares a writable destination."""
        inputs_root = sandbox.resolve_files_root(SESSION_INPUTS_ROOT)
        if inputs_root is None:
            return None
        return cls(sandbox, inputs_root, policy=policy)

    @classmethod
    async def for_saved_sandbox(
        cls,
        sandbox: WorkflowSandboxResource,
        directory: Path,
        policy: SessionFilePolicy = DEFAULT_SESSION_FILE_POLICY,
    ) -> "LocalSessionFileManager | None":
        """Keep the files that messages linked in ``directory``, so a later process can reopen them.

        A reopened Session runs in a new sandbox while its history still links the earlier
        paths, so each saved file is copied into ``sandbox`` again.
        """
        inputs_root = sandbox.resolve_files_root(SESSION_INPUTS_ROOT)
        if inputs_root is None:
            return None
        catalog = JsonFileSessionFileCatalog(directory / "catalog.json")
        store = LocalSessionFileStore(directory / "bytes")
        manager = cls(sandbox, inputs_root, policy=policy, store=store, catalog=catalog)
        try:
            records = catalog.records()
            await store.retain({record.file_id for record in records})
            for record in records:
                # A sandbox that declares another root cannot serve the paths in the history.
                if manager._is_managed(record.uri):
                    await manager._materialize(record)
        except BaseException:
            await manager.close()
            raise
        return manager

    @property
    def inputs_root(self) -> str:
        return self._inputs_root

    async def upload(
        self,
        source: str | Path | bytes | AsyncIterator[bytes],
        *,
        name: str | None,
        media_type: str | None,
        validate_session: Callable[[], None],
    ) -> ResourceLinkContentBlock:
        filename = name or (Path(source).name if isinstance(source, str | Path) else None)
        if not filename:
            raise ValueError("A filename is required for byte and stream uploads")
        mime = (media_type or mimetypes.guess_type(filename)[0] or "application/octet-stream").lower()
        self._ensure_open()
        # The upload runs in a task this object owns, so close() cancels it and never the caller.
        task = asyncio.create_task(self._upload(source, sanitize_filename(filename), mime, validate_session))
        self._uploads.add(task)
        task.add_done_callback(self._uploads.discard)
        try:
            return await asyncio.shield(task)
        except asyncio.CancelledError:
            current = asyncio.current_task()
            if current is not None and current.cancelling():
                task.cancel()
                await asyncio.gather(task, return_exceptions=True)
                raise
            raise SessionTerminatedError("The Session files were closed during the upload") from None

    async def _upload(
        self,
        source: str | Path | bytes | AsyncIterator[bytes],
        filename: str,
        mime: str,
        validate_session: Callable[[], None],
    ) -> ResourceLinkContentBlock:
        validate_session()
        async with self._lock:
            self._ensure_open()
            await self._expire_staged()
            records = self._catalog.records()
            if len(records) + self._reserved_files >= self._policy.max_files:
                raise ValueError("Session file count limit exceeded")
            self._reserved_files += 1
        file_id = f"sf_{uuid4().hex}"
        uri = session_file_uri(self._inputs_root, file_id, filename)
        try:
            async with asyncio.timeout(self._policy.read_timeout_seconds):
                async with aclosing(iter_file_source(source)) as chunks:
                    stored = await self._store.write(file_id, chunks)
            record = SessionFileRecord(
                file_id=file_id,
                uri=uri,
                name=filename,
                media_type=mime,
                size=stored.size,
                sha256=stored.sha256,
                state="staged",
                expires_at=self._clock() + self._policy.staged_ttl_seconds,
            )
            validate_session()
            async with self._lock:
                self._ensure_open()
                self._catalog.add(record)
        except BaseException:
            await self._store.delete(file_id)
            raise
        finally:
            async with self._lock:
                self._reserved_files -= 1
        return ResourceLinkContentBlock(uri=uri, name=filename, media_type=mime, size=stored.size)

    @asynccontextmanager
    async def prepare(self, content: Sequence[core_protocol.ContentBlock]) -> AsyncIterator[Callable[[], None]]:
        """Restore managed files without promoting them; protect pending admission from expiry."""
        managed = tuple(
            dict.fromkeys(
                block.uri
                for block in content
                if isinstance(block, core_protocol.ResourceLinkContentBlock) and self._is_managed(block.uri)
            )
        )
        if not managed:
            yield lambda: None
            return
        records: list[SessionFileRecord] = []
        async with self._lock:
            self._ensure_open()
            await self._expire_staged()
            for uri in managed:
                record = self._catalog.get(uri)
                if record is None:
                    raise SessionMessageRejectedError(f"Unknown or expired Session file: {uri}")
                records.append(record)
            for uri in managed:
                self._prepared[uri] = self._prepared.get(uri, 0) + 1
        try:
            # TODO: Remove newly projected staged files on materialization failure or
            # definitive rejected/busy admission, preserving accepted files and concurrent
            # preparations. Distinguish rejection from errors after acceptance.
            for record in records:
                await self._materialize(record)

            def promote() -> None:
                # No await separates accepted admission from reference retention.
                for record in records:
                    self._catalog.replace(replace(record, state="referenced", expires_at=None))

            yield promote
        finally:
            async with self._lock:
                for uri in managed:
                    self._prepared[uri] -= 1
                    if self._prepared[uri] == 0:
                        del self._prepared[uri]

    async def close(self) -> None:
        self._closed = True
        for task in tuple(self._uploads):
            task.cancel()
        await asyncio.gather(*self._uploads, return_exceptions=True)
        async with self._lock:
            try:
                await self._store.close()
            finally:
                _STORES.pop(self._store.reference, None)

    def _is_managed(self, uri: str) -> bool:
        return uri.startswith(_file_uri(self._inputs_root) + "/")

    async def _materialize(self, record: SessionFileRecord) -> None:
        source = FileSource(
            resolver=SESSION_FILE_RESOLVER,
            refs={"store": self._store.reference, "file_id": record.file_id, "name": record.name},
        )
        written = await self._sandbox.write_files(
            WorkflowSandboxWriteFilesRequest(root=SESSION_INPUTS_ROOT, source=source)
        )
        if written.root != self._inputs_root:
            raise RuntimeError("The Session file could not be projected into the sandbox")

    async def _expire_staged(self) -> None:
        now = self._clock()
        for record in self._catalog.records():
            if (
                record.uri not in self._prepared
                and record.state == "staged"
                and record.expires_at is not None
                and record.expires_at <= now
            ):
                self._catalog.remove(record.uri)
                await self._store.delete(record.file_id)

    def _ensure_open(self) -> None:
        if self._closed:
            raise SessionTerminatedError("The Session files are closed")


def unsupported_upload(reason: str) -> UnsupportedSessionProcedureError:
    return UnsupportedSessionProcedureError(method="upload_file", backend="local", reason=reason)


__all__ = [
    "SESSION_FILE_RESOLVER",
    "SESSION_INPUTS_ROOT",
    "LocalSessionFileManager",
    "session_file_uri",
]
