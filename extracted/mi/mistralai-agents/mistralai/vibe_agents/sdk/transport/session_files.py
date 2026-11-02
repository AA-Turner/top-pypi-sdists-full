"""Session file policy, metadata catalog and immutable byte store."""

import asyncio
import hashlib
import math
import shutil
import tempfile
from collections.abc import AsyncIterator, Collection, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Protocol
from uuid import uuid4

import structlog
from pydantic import TypeAdapter

from mistralai.vibe.harness.app_server.session import SessionTerminatedError
from mistralai.vibe.harness.app_server.session.local_lifetime import finish_local_cleanup
from mistralai.vibe.harness.runtime.hosts.local.journal import replace_file_atomically

_STORE_PREFIX = "vibe-session-files-"
_WRITE_CHUNK_BYTES = 64 * 1024

logger = structlog.get_logger(__name__)


@dataclass(frozen=True, slots=True)
class SessionFilePolicy:
    max_files: int = 100
    read_timeout_seconds: float = 300
    staged_ttl_seconds: float = 3600

    def __post_init__(self) -> None:
        if self.max_files <= 0:
            raise ValueError("Session file count limit must be positive")
        for value in (self.read_timeout_seconds, self.staged_ttl_seconds):
            if not math.isfinite(value) or value <= 0:
                raise ValueError("Session file durations must be finite and positive")


DEFAULT_SESSION_FILE_POLICY = SessionFilePolicy()


@dataclass(frozen=True, slots=True)
class StoredFile:
    size: int
    sha256: str


class SessionFileStore(Protocol):
    """Authoritative immutable bytes keyed by Session File ID, independent of any sandbox."""

    @property
    def reference(self) -> str: ...

    async def write(self, file_id: str, chunks: AsyncIterator[bytes]) -> StoredFile: ...

    async def read(self, file_id: str) -> bytes: ...

    async def delete(self, file_id: str) -> None: ...

    async def close(self) -> None: ...


type SessionFileState = Literal["staged", "referenced"]


@dataclass(frozen=True, slots=True)
class SessionFileRecord:
    file_id: str
    uri: str
    name: str
    media_type: str
    size: int
    sha256: str
    state: SessionFileState
    expires_at: float | None


class SessionFileCatalog(Protocol):
    """Session-scoped records keyed by exact canonical URI; it never holds bytes."""

    def add(self, record: SessionFileRecord) -> None: ...

    def get(self, uri: str) -> SessionFileRecord | None: ...

    def replace(self, record: SessionFileRecord) -> None: ...

    def remove(self, uri: str) -> None: ...

    def records(self) -> Sequence[SessionFileRecord]: ...


class InMemorySessionFileCatalog:
    def __init__(self) -> None:
        self._records: dict[str, SessionFileRecord] = {}

    def add(self, record: SessionFileRecord) -> None:
        if record.uri in self._records:
            raise ValueError("A Session File URI is already registered")
        self._records[record.uri] = record

    def get(self, uri: str) -> SessionFileRecord | None:
        return self._records.get(uri)

    def replace(self, record: SessionFileRecord) -> None:
        if record.uri not in self._records:
            raise KeyError(record.uri)
        self._records[record.uri] = record

    def remove(self, uri: str) -> None:
        self._records.pop(uri, None)

    def records(self) -> Sequence[SessionFileRecord]:
        return tuple(self._records.values())


_RECORDS = TypeAdapter(list[SessionFileRecord])


class JsonFileSessionFileCatalog(InMemorySessionFileCatalog):
    """Save the referenced records in a JSON file, so a reopened Session finds the files it linked.

    Staged records stay in memory only: their expiry uses this process's monotonic clock, and no
    accepted message links them.
    """

    def __init__(self, path: Path) -> None:
        super().__init__()
        self._path = path
        if path.exists():
            for record in _RECORDS.validate_json(path.read_bytes()):
                super().add(record)

    def add(self, record: SessionFileRecord) -> None:
        super().add(record)
        if record.state == "referenced":
            self._save()

    def replace(self, record: SessionFileRecord) -> None:
        previous = self.get(record.uri)
        super().replace(record)
        if "referenced" in (record.state, previous.state if previous is not None else None):
            self._save()

    def remove(self, uri: str) -> None:
        previous = self.get(uri)
        super().remove(uri)
        if previous is not None and previous.state == "referenced":
            self._save()

    def _save(self) -> None:
        # Synchronous: promotion must not await between admission and retention.
        referenced = [record for record in self.records() if record.state == "referenced"]
        try:
            replace_file_atomically(self._path, _RECORDS.dump_json(referenced).decode())
        except OSError:
            logger.warning("local_session_file_catalog_save_failed", path=str(self._path), exc_info=True)


class LocalSessionFileStore(SessionFileStore):
    """A folder owned by one root Session.

    Without ``root``, the folder is private and temporary, and close() removes it. With ``root``,
    the bytes stay after close(), so a later process that reopens the Session reads them.
    """

    def __init__(self, root: Path | None = None) -> None:
        self._persistent = root is not None
        if root is None:
            root = Path(tempfile.mkdtemp(prefix=_STORE_PREFIX))
        else:
            root.mkdir(parents=True, exist_ok=True)
        self._root = root
        self._reference = uuid4().hex
        self._closed = False

    @property
    def reference(self) -> str:
        return self._reference

    @property
    def root(self) -> Path:
        return self._root

    async def write(self, file_id: str, chunks: AsyncIterator[bytes]) -> StoredFile:
        self._ensure_open()
        target = self._path(file_id)
        digest = hashlib.sha256()
        size = 0
        try:
            with target.open("xb") as handle:
                async for chunk in chunks:
                    if not isinstance(chunk, bytes):
                        raise ValueError("File sources must yield bytes")
                    size += len(chunk)
                    digest.update(chunk)
                    for offset in range(0, len(chunk), _WRITE_CHUNK_BYTES):
                        # Cancellation cannot stop worker I/O; finish it before closing the handle.
                        await finish_local_cleanup(
                            asyncio.create_task(
                                asyncio.to_thread(handle.write, chunk[offset : offset + _WRITE_CHUNK_BYTES])
                            )
                        )
            target.chmod(0o400)
        except BaseException:
            await self.delete(file_id)
            raise
        return StoredFile(size=size, sha256=digest.hexdigest())

    async def read(self, file_id: str) -> bytes:
        self._ensure_open()
        return await asyncio.to_thread(self._path(file_id).read_bytes)

    async def delete(self, file_id: str) -> None:
        await finish_local_cleanup(asyncio.create_task(asyncio.to_thread(self._path(file_id).unlink, missing_ok=True)))

    async def retain(self, file_ids: Collection[str]) -> None:
        """Delete every stored file not in ``file_ids``, such as an earlier process's staged uploads."""
        for path in await asyncio.to_thread(lambda: list(self._root.iterdir())):
            if path.name not in file_ids:
                await asyncio.to_thread(path.unlink, missing_ok=True)

    async def close(self) -> None:
        self._closed = True
        if not self._persistent:
            await asyncio.to_thread(shutil.rmtree, self._root, True)

    def _path(self, file_id: str) -> Path:
        if not file_id.startswith("sf_") or not file_id[3:].isalnum():
            raise ValueError("Invalid Session File ID")
        return self._root / file_id

    def _ensure_open(self) -> None:
        if self._closed:
            raise SessionTerminatedError("The Session file store is closed")


__all__ = [
    "DEFAULT_SESSION_FILE_POLICY",
    "InMemorySessionFileCatalog",
    "JsonFileSessionFileCatalog",
    "LocalSessionFileStore",
    "SessionFileCatalog",
    "SessionFilePolicy",
    "SessionFileRecord",
    "SessionFileStore",
    "StoredFile",
]
