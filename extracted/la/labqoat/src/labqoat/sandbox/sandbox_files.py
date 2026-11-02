"""Files and directories of one sandbox."""

from collections.abc import Iterator
from pathlib import Path
from typing import ClassVar, Literal, overload

from labqoat.sandbox.directory_archive import DirectoryArchive
from labqoat.sandbox.sandbox_executor import SandboxExecutor
from labqoat.sandbox.sandbox_file import SandboxFile
from labqoat.sandbox.sandbox_file_not_found_error import SandboxFileNotFoundError
from labqoat.sandbox.sandbox_listing import SandboxListing
from labqoat.sandbox.sandbox_request import SandboxRequest
from labqoat.sandbox.sandbox_response import SandboxResponse
from labqoat.sandbox.sandbox_transfer_error import SandboxTransferError
from labqoat.sandbox.sandbox_write_error import SandboxWriteError


class SandboxFiles(SandboxExecutor):
    """Move whole files and directory trees, open files like local ones, and list, create and remove paths.

    Every path inside the sandbox is absolute. Large transfers travel in pieces of at most 64 MiB.
    """

    LIST: ClassVar[str] = 'cd -- "$1" && ls -1A'
    REMOVE: ClassVar[str] = 'if [ -d "$1" ] && [ ! -L "$1" ]; then rmdir -- "$1"; else rm -- "$1"; fi'

    def write_file(self, path: str, data: bytes | Path) -> None:
        """Replace the file at ``path`` with bytes, or with a local file streamed from disk."""
        for request in self._write_requests(path, data):
            self.transport.send(request)

    async def write_file_async(self, path: str, data: bytes | Path) -> None:
        """Write a file without blocking the event loop; see ``write_file``."""
        for request in self._write_requests(path, data):
            await self.transport.send_async(request)

    def read_file(self, path: str) -> bytes:
        """Return the bytes of the file at ``path``; ``open(path, "rb")`` reads a large one without holding it."""
        return self.transport.send(self._read_request(path))

    async def read_file_async(self, path: str) -> bytes:
        """Read a file without blocking the event loop; see ``read_file``."""
        return await self.transport.send_async(self._read_request(path))

    @overload
    def open(self, path: str, mode: Literal["r", "w", "a"] = "r") -> SandboxFile[str]: ...

    @overload
    def open(self, path: str, mode: Literal["rb", "wb", "ab"]) -> SandboxFile[bytes]: ...

    def open(self, path: str, mode: str = "r") -> SandboxFile[str] | SandboxFile[bytes]:
        """Open the file at ``path`` like a local file; ``SandboxFile`` describes the modes."""
        if "b" in mode:
            return SandboxFile(self.transport, self._files, path, mode, bytes).prepare()
        return SandboxFile(self.transport, self._files, path, mode, str).prepare()

    @overload
    async def open_async(self, path: str, mode: Literal["r", "w", "a"] = "r") -> SandboxFile[str]: ...

    @overload
    async def open_async(self, path: str, mode: Literal["rb", "wb", "ab"]) -> SandboxFile[bytes]: ...

    async def open_async(self, path: str, mode: str = "r") -> SandboxFile[str] | SandboxFile[bytes]:
        """Open a file without blocking the event loop; see ``open``."""
        if "b" in mode:
            return await SandboxFile(self.transport, self._files, path, mode, bytes).prepare_async()
        return await SandboxFile(self.transport, self._files, path, mode, str).prepare_async()

    def ls(self, path: str) -> list[str]:
        """Return the names in the directory at ``path``, hidden ones included."""
        return self._listed(path, *self._completed(["sh", "-c", self.LIST, "sh", path]))

    async def ls_async(self, path: str) -> list[str]:
        """List a directory without blocking the event loop; see ``ls``."""
        return self._listed(path, *await self._completed_async(["sh", "-c", self.LIST, "sh", path]))

    def scandir(self, path: str) -> SandboxListing:
        """Return the entries of the directory at ``path`` with their kinds, sizes and modification times."""
        return SandboxResponse.decoded(self.transport.send(self._scan_request(path)), SandboxListing.decode)

    async def scandir_async(self, path: str) -> SandboxListing:
        """List a directory's entries without blocking the event loop; see ``scandir``."""
        return SandboxResponse.decoded(await self.transport.send_async(self._scan_request(path)), SandboxListing.decode)

    def mkdir(self, path: str, parents: bool = False) -> None:
        """Create the directory at ``path``, and with ``parents`` every missing one above it."""
        self._changed(f"create {path}", *self._completed(self._mkdir_command(path, parents)))

    async def mkdir_async(self, path: str, parents: bool = False) -> None:
        """Create a directory without blocking the event loop; see ``mkdir``."""
        self._changed(f"create {path}", *await self._completed_async(self._mkdir_command(path, parents)))

    def rm(self, path: str, recursive: bool = False) -> None:
        """Remove the file or empty directory at ``path``, or with ``recursive`` the directory and its contents."""
        self._changed(f"remove {path}", *self._completed(self._rm_command(path, recursive)))

    async def rm_async(self, path: str, recursive: bool = False) -> None:
        """Remove a path without blocking the event loop; see ``rm``."""
        self._changed(f"remove {path}", *await self._completed_async(self._rm_command(path, recursive)))

    def upload_dir(self, local_dir: str | Path, remote_dir: str) -> None:
        """Copy a local directory's contents into a sandbox directory, creating it when missing."""
        archive = DirectoryArchive.remote_path()
        self.write_file(archive, DirectoryArchive.pack(Path(local_dir)))
        unpacked = self._completed(DirectoryArchive.unpack_command(archive, remote_dir))
        self._transferred(f"Sandbox {self.id} could not unpack {remote_dir}", *unpacked)

    async def upload_dir_async(self, local_dir: str | Path, remote_dir: str) -> None:
        """Upload a directory without blocking the event loop; see ``upload_dir``."""
        archive = DirectoryArchive.remote_path()
        await self.write_file_async(archive, DirectoryArchive.pack(Path(local_dir)))
        unpacked = await self._completed_async(DirectoryArchive.unpack_command(archive, remote_dir))
        self._transferred(f"Sandbox {self.id} could not unpack {remote_dir}", *unpacked)

    def download_dir(self, remote_dir: str, local_dir: str | Path) -> None:
        """Copy a sandbox directory's contents into a local directory, creating it when missing."""
        archive = DirectoryArchive.remote_path()
        packed = self._completed(DirectoryArchive.pack_command(remote_dir, archive))
        self._transferred(f"Sandbox {self.id} could not pack {remote_dir}", *packed)
        content = self.read_file(archive)
        self._completed(["rm", "-f", archive])
        DirectoryArchive.extract(content, Path(local_dir))

    async def download_dir_async(self, remote_dir: str, local_dir: str | Path) -> None:
        """Download a directory without blocking the event loop; see ``download_dir``."""
        archive = DirectoryArchive.remote_path()
        packed = await self._completed_async(DirectoryArchive.pack_command(remote_dir, archive))
        self._transferred(f"Sandbox {self.id} could not pack {remote_dir}", *packed)
        content = await self.read_file_async(archive)
        await self._completed_async(["rm", "-f", archive])
        DirectoryArchive.extract(content, Path(local_dir))

    @property
    def _files(self) -> str:
        """Address this sandbox's files in the host's API."""
        return f"{self._path}/files"

    def _write_requests(self, path: str, data: bytes | Path) -> Iterator[SandboxRequest]:
        """Replace the file in pieces: the first piece replaces it and every later one is added to its end."""
        size = data.stat().st_size if isinstance(data, Path) else len(data)
        for start in range(0, max(size, 1), SandboxFile.PIECE_BYTES):
            query = {"path": path, **({"append": "true"} if start else {})}
            length = min(SandboxFile.PIECE_BYTES, size - start)
            yield (
                SandboxRequest("PUT", self._files, query, source=data, source_start=start, source_length=length)
                if isinstance(data, Path)
                else SandboxRequest("PUT", self._files, query, content=data[start : start + length])
            )

    def _scan_request(self, path: str) -> SandboxRequest:
        """Ask the host to list one directory."""
        return SandboxRequest("GET", f"{self._path}/directory", {"path": path})

    def _read_request(self, path: str) -> SandboxRequest:
        """Ask for one file's bytes."""
        return SandboxRequest("GET", self._files, {"path": path}, timeout=self.TRANSFER_SECONDS)

    @staticmethod
    def _mkdir_command(path: str, parents: bool) -> list[str]:
        """Create one directory, or the whole chain."""
        return ["mkdir", *(["-p"] if parents else []), "--", path]

    def _rm_command(self, path: str, recursive: bool) -> list[str]:
        """Remove a tree, or exactly one file or empty directory."""
        return ["rm", "-r", "--", path] if recursive else ["sh", "-c", self.REMOVE, "sh", path]

    def _listed(self, path: str, exit_code: int, output: str) -> list[str]:
        """Return a listing's names; a path that is not a directory has none to list."""
        if exit_code != 0:
            raise SandboxFileNotFoundError(f"Sandbox {self.id} has no directory {path}: {output.strip()}")
        return output.splitlines()

    def _changed(self, action: str, exit_code: int, output: str) -> None:
        """Raise when a command that changes the file system did not."""
        if exit_code != 0:
            raise SandboxWriteError(f"Sandbox {self.id} could not {action} (exit code {exit_code}): {output.strip()}")

    @staticmethod
    def _transferred(message: str, exit_code: int, output: str) -> None:
        """Turn a failed archive command into an error: a half-copied directory is not a result."""
        if exit_code != 0:
            raise SandboxTransferError(message, exit_code, output)
