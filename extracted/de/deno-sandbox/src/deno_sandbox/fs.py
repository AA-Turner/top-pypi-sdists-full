from __future__ import annotations

import base64
import os
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterable,
    BinaryIO,
    Iterable,
    Literal,
    Optional,
    TypedDict,
    Union,
    cast,
)

from re import Pattern

from .process import AbortSignal
from .stream import complete_stream, start_stream
from .utils import convert_to_camel_case, convert_to_snake_case

if TYPE_CHECKING:
    from .rpc import AsyncRpcClient
    from .bridge import AsyncBridge


class DirEntry(TypedDict):
    name: str
    """The file or directory name."""

    is_file: bool
    """Whether the entry is a file."""

    is_directory: bool
    """Whether the entry is a directory."""

    is_symlink: bool
    """Whether the entry is a symbolic link."""


class FileInfo(TypedDict):
    is_file: bool
    """Whether the path is a file."""

    is_directory: bool
    """Whether the path is a directory."""

    is_symlink: bool
    """Whether the path is a symbolic link."""

    size: int
    """The size of the file in bytes."""

    mtime: str
    """The last modification time of the file."""

    atime: str
    """The last access time of the file."""

    birthtime: str
    """The creation time of the file."""

    ctime: str
    """The last status change time of the file."""

    dev: int
    """The device ID."""

    ino: int
    """The inode number."""

    mode: int
    """The file mode."""

    nlink: int
    """The number of hard links pointing to this file."""

    uid: int
    """The user ID of the owner."""

    gid: int
    """The group ID of the owner."""

    rdev: int
    """The device ID of this file."""

    blksize: int
    """The block size for filesystem I/O."""

    blocks: int
    """The number of blocks allocated in 512-byte units"""

    is_block_device: bool
    """Whether the path is a block device."""

    is_char_device: bool
    """Whether the path is a character device."""

    is_fifo: bool
    """Whether the path is a FIFO."""

    is_socket: bool
    """Whether the path is a socket."""


class WalkEntry(TypedDict):
    path: str
    """The full path of the entry."""

    name: str
    """The file or directory name."""

    is_file: bool
    """Whether the entry is a file."""

    is_directory: bool
    """Whether the entry is a directory."""

    is_symlink: bool
    """Whether the entry is a symbolic link."""


class FsFileHandle(TypedDict):
    file_handle_id: int


class AsyncFsFile:
    def __init__(self, rpc: AsyncRpcClient, fd: int):
        self._rpc = rpc
        self._fd = fd

    async def write(self, data: bytes) -> int:
        """Write data to the file. Returns number of bytes written."""

        result = await self._rpc.call(
            "fileWrite",
            {"data": base64.b64encode(data).decode("ascii"), "fileHandleId": self._fd},
        )
        return result["bytes_written"]

    async def truncate(self, size: Optional[int]) -> None:
        """Truncate the file to the given size. If size is None, truncate to 0."""

        await self._rpc.call("fileTruncate", {"size": size, "fileHandleId": self._fd})

    async def read(self, size: int) -> bytes:
        """Read up to size bytes from the file. Returns the data read."""

        result = await self._rpc.call(
            "fileRead", {"length": size, "fileHandleId": self._fd}
        )
        return base64.b64decode(result["data"])

    async def seek(self, offset: int, whence: int) -> int:
        """Seek to a position in the file. Returns the new position."""

        result = await self._rpc.call(
            "fileSeek", {"offset": offset, "whence": whence, "fileHandleId": self._fd}
        )
        return result["position"]

    async def stat(self) -> FileInfo:
        """Get file information."""

        result = await self._rpc.call("fileStat", {"fileHandleId": self._fd})
        return cast(FileInfo, result)

    async def sync(self) -> None:
        """Flushes any pending data and metadata operations of the given file stream to disk."""

        await self._rpc.call("fileSync", {"fileHandleId": self._fd})

    async def sync_data(self) -> None:
        """Sync the file's data to disk."""

        await self._rpc.call("fileSyncData", {"fileHandleId": self._fd})

    async def utime(self, atime: float, mtime: float) -> None:
        """Update the file's access and modification times."""

        await self._rpc.call(
            "fileUtime",
            {"atime": atime, "mtime": mtime, "fileHandleId": self._fd},
        )

    async def lock(self, exclusive: Optional[bool]) -> None:
        """Lock the file. If exclusive is True, acquire an exclusive lock."""

        await self._rpc.call(
            "fileLock", {"exclusive": exclusive, "fileHandleId": self._fd}
        )

    async def unlock(self) -> None:
        """Unlock the file."""

        await self._rpc.call("fileUnlock", {"fileHandleId": self._fd})

    async def close(self) -> None:
        """Close the file."""

        await self._rpc.call("fileClose", {"fileHandleId": self._fd})

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class FsFile:
    def __init__(self, rpc: AsyncRpcClient, bridge: AsyncBridge, fd: int):
        self._rpc = rpc
        self._bridge = bridge
        self._async = AsyncFsFile(rpc, fd)

    def write(self, data: bytes) -> int:
        """Write data to the file. Returns number of bytes written."""
        return self._bridge.run(self._async.write(data))

    def truncate(self, size: Optional[int]) -> None:
        """Truncate the file to the given size. If size is None, truncate to 0."""
        return self._bridge.run(self._async.truncate(size))

    def read(self, size: int) -> bytes:
        """Read up to size bytes from the file. Returns the data read."""
        return self._bridge.run(self._async.read(size))

    def seek(self, offset: int, whence: int) -> int:
        """Seek to a position in the file. Returns the new position."""
        return self._bridge.run(self._async.seek(offset, whence))

    def stat(self) -> FileInfo:
        """Get file information."""
        return self._bridge.run(self._async.stat())

    def sync(self) -> None:
        """Flushes any pending data and metadata operations of the given file stream to disk."""
        return self._bridge.run(self._async.sync())

    def sync_data(self) -> None:
        """Sync the file's data to disk."""
        return self._bridge.run(self._async.sync_data())

    def utime(self, atime: int, mtime: int) -> None:
        """Update the file's access and modification times."""
        return self._bridge.run(self._async.utime(atime, mtime))

    def lock(self, exclusive: Optional[bool]) -> None:
        """Lock the file. If exclusive is True, acquire an exclusive lock."""
        return self._bridge.run(self._async.lock(exclusive))

    def unlock(self) -> None:
        """Unlock the file."""
        return self._bridge.run(self._async.unlock())

    def close(self) -> None:
        """Close the file."""
        return self._bridge.run(self._async.close())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class AsyncSandboxFs:
    """Filesystem operations inside the sandbox."""

    def __init__(self, rpc: AsyncRpcClient):
        self._rpc = rpc

    async def read_file(
        self,
        path: str,
        *,
        signal: Optional[AbortSignal] = None,
    ) -> bytes:
        """Reads the entire contents of a file as bytes.

        Args:
            path: The path to the file to read.
            signal: An optional abort signal to cancel the operation.
        """
        params: dict[str, Any] = {"path": path}
        options: dict[str, Any] = {}
        if signal is not None:
            options["signal"] = signal
        if options:
            params["options"] = convert_to_camel_case(options)

        result = await self._rpc.call("readFile", params)

        # Server returns base64-encoded data
        return base64.b64decode(result)

    async def write_file(
        self,
        path: str,
        data: Union[bytes, AsyncIterable[bytes], Iterable[bytes], BinaryIO],
        *,
        create: Optional[bool] = None,
        append: Optional[bool] = None,
        create_new: Optional[bool] = None,
        mode: Optional[int] = None,
    ) -> None:
        """Write bytes to file. Accepts bytes, async/sync iterables, or file objects.

        Args:
            path: The path to the file to write.
            data: The data to write to the file.
            create: Create file if it doesn't already exist.
            append: Append content instead of overwriting existing contents.
            create_new: Fail if the file already exists.
            mode: Set the file permission mode.
        """
        if isinstance(data, bytes):
            streamable = iter([data])
        else:
            streamable = data

        stream_id, writer = await start_stream(self._rpc)

        params: dict[str, Any] = {"path": path, "contentStreamId": stream_id}
        options: dict[str, Any] = {}
        if create is not None:
            options["create"] = create
        if append is not None:
            options["append"] = append
        if create_new is not None:
            options["create_new"] = create_new
        if mode is not None:
            options["mode"] = mode
        if options:
            params["options"] = convert_to_camel_case(options)

        # Send data concurrently with the RPC call to avoid deadlock:
        # the server waits for stream data before responding to writeFile.
        async def _send() -> None:
            try:
                await complete_stream(writer, streamable)
            except Exception as e:
                await writer.error(str(e))

        task = self._rpc._loop.create_task(_send())
        try:
            await self._rpc.call("writeFile", params)
        finally:
            await task

    async def read_text_file(
        self,
        path: str,
        *,
        signal: Optional[AbortSignal] = None,
    ) -> str:
        """Reads the entire contents of a file as an UTF-8 decoded string.

        Args:
            path: The path to the file to read.
            signal: An optional abort signal to cancel the operation.
        """
        params: dict[str, Any] = {"path": path}
        options: dict[str, Any] = {}
        if signal is not None:
            options["signal"] = signal
        if options:
            params["options"] = convert_to_camel_case(options)

        result = await self._rpc.call("readTextFile", params)

        return result

    async def write_text_file(
        self,
        path: str,
        content: str,
        *,
        create: Optional[bool] = None,
        append: Optional[bool] = None,
        create_new: Optional[bool] = None,
        mode: Optional[int] = None,
    ) -> None:
        """Write text to file. Creates a new file if needed. Existing files will be overwritten.

        Args:
            path: The path to the file to write.
            content: The text content to write.
            create: Create file if it doesn't already exist.
            append: Append content instead of overwriting existing contents.
            create_new: Fail if the file already exists.
            mode: Set the file permission mode.
        """
        params: dict[str, Any] = {"path": path, "content": content}
        options: dict[str, Any] = {}
        if create is not None:
            options["create"] = create
        if append is not None:
            options["append"] = append
        if create_new is not None:
            options["create_new"] = create_new
        if mode is not None:
            options["mode"] = mode
        if options:
            params["options"] = convert_to_camel_case(options)

        await self._rpc.call("writeTextFile", params)

    async def read_dir(self, path: str) -> list[DirEntry]:
        """Read the directory entries at the given path."""

        params = {"path": path}
        result = await self._rpc.call("readDir", params)

        return result

    async def remove(
        self,
        path: str,
        *,
        recursive: Optional[bool] = None,
    ) -> None:
        """Remove the file or directory at the given path.

        Args:
            path: The path to the file or directory to remove.
            recursive: Whether to remove directories recursively. Default: false.
        """
        params: dict[str, Any] = {"path": path}
        options: dict[str, Any] = {}
        if recursive is not None:
            options["recursive"] = recursive
        if options:
            params["options"] = convert_to_camel_case(options)

        await self._rpc.call("remove", params)

    async def mkdir(
        self,
        path: str,
        *,
        recursive: Optional[bool] = None,
        mode: Optional[int] = None,
    ) -> None:
        """Create a new directory at the specified path.

        Args:
            path: The path to the directory to create.
            recursive: If true, parent directories will be created if they do not already exist.
            mode: Permissions to use for the new directory.
        """
        params: dict[str, Any] = {"path": path}
        options: dict[str, Any] = {}
        if recursive is not None:
            options["recursive"] = recursive
        if mode is not None:
            options["mode"] = mode
        if options:
            params["options"] = convert_to_camel_case(options)

        await self._rpc.call("mkdir", params)

    async def rename(self, old_path: str, new_path: str) -> None:
        """Rename (move) a file or directory."""

        params = {"oldPath": old_path, "newPath": new_path}
        await self._rpc.call("rename", params)

    async def stat(self, path: str) -> FileInfo:
        """Return file information about a file or directory."""

        params = {"path": path}
        result = await self._rpc.call("stat", params)

        raw_result = convert_to_snake_case(result)
        return cast(FileInfo, raw_result)

    async def chmod(self, path: str, mode: int) -> None:
        """Change the permission mode of a file or directory."""

        params = {"path": path, "mode": mode}
        await self._rpc.call("chmod", params)

    async def chown(
        self, path: str, uid: Optional[int] = None, gid: Optional[int] = None
    ) -> None:
        """Change the owner user ID and group ID of a file or directory."""

        params = {"path": path, "uid": uid, "gid": gid}
        await self._rpc.call("chown", params)

    async def copy_file(self, from_path: str, to_path: str) -> None:
        """Copy a file from a source path to a destination path."""

        params = {"fromPath": from_path, "toPath": to_path}
        await self._rpc.call("copyFile", params)

    async def walk(
        self,
        path: str,
        *,
        max_depth: Optional[int] = None,
        include_files: Optional[bool] = None,
        include_dirs: Optional[bool] = None,
        include_symlinks: Optional[bool] = None,
        follow_symlinks: Optional[bool] = None,
        canonicalize: Optional[bool] = None,
        exts: Optional[list[str]] = None,
        match: Optional[list[Pattern]] = None,
        skip: Optional[list[Pattern]] = None,
    ) -> list[WalkEntry]:
        """Recursively walk a directory tree.

        Args:
            path: The path to the directory to walk.
            max_depth: The maximum depth to traverse. Default: Infinity.
            include_files: Whether to include files in the results. Default: true.
            include_dirs: Whether to include directories in the results. Default: true.
            include_symlinks: Whether to include symbolic links in the results. Default: true.
            follow_symlinks: Whether to follow symbolic links. Default: false.
            canonicalize: Whether to return canonicalized paths. This option works only if `follow_symlinks` is not `false`. Default: false.
            exts: If provided, only files with the specified extensions will be included. Example: ['.ts', '.js']
            match: List of regular expression patterns used to filter entries. If specified, entries that do not match the patterns specified by this option are excluded.
            skip: List of regular expression patterns used to filter entries. If specified, entries that match the patterns specified by this option are excluded.
        """
        params: dict[str, Any] = {"path": path}
        options: dict[str, Any] = {}
        if max_depth is not None:
            options["max_depth"] = max_depth
        if include_files is not None:
            options["include_files"] = include_files
        if include_dirs is not None:
            options["include_dirs"] = include_dirs
        if include_symlinks is not None:
            options["include_symlinks"] = include_symlinks
        if follow_symlinks is not None:
            options["follow_symlinks"] = follow_symlinks
        if canonicalize is not None:
            options["canonicalize"] = canonicalize
        if exts is not None:
            options["exts"] = exts
        if match is not None:
            options["match"] = match
        if skip is not None:
            options["skip"] = skip
        if options:
            params["options"] = convert_to_camel_case(options)

        result = await self._rpc.call("walk", params)

        return result

    async def expand_glob(
        self,
        glob: str,
        *,
        root: Optional[str] = None,
        exclude: Optional[list[str]] = None,
        include_dirs: Optional[bool] = None,
        follow_symlinks: Optional[bool] = None,
        canonicalize: Optional[bool] = None,
        extended: Optional[bool] = None,
        globstar: Optional[bool] = None,
        case_insensitive: Optional[bool] = None,
    ) -> list[str]:
        """Expand a glob pattern to a list of paths.

        Args:
            glob: The glob pattern to expand.
            root: The root directory from which to expand the glob pattern. Default is the current working directory.
            exclude: An array of glob patterns to exclude from the results.
            include_dirs: Whether to include directories in the results. Default: true.
            follow_symlinks: Whether to follow symbolic links. Default: false.
            canonicalize: Whether to return canonicalized paths. This option works only if `follow_symlinks` is not `false`. Default: true.
            extended: Whether to enable extended glob syntax, see https://www.linuxjournal.com/content/bash-extended-globbing. Default: true.
            globstar: Globstar syntax. See https://www.linuxjournal.com/content/globstar-new-bash-globbing-option. If false, `**` is treated like `*`. Default: true.
            case_insensitive: Whether the glob matching should be case insensitive. Default: false.
        """
        params: dict[str, Any] = {"glob": glob}
        options: dict[str, Any] = {}
        if root is not None:
            options["root"] = root
        if exclude is not None:
            options["exclude"] = exclude
        if include_dirs is not None:
            options["include_dirs"] = include_dirs
        if follow_symlinks is not None:
            options["follow_symlinks"] = follow_symlinks
        if canonicalize is not None:
            options["canonicalize"] = canonicalize
        if extended is not None:
            options["extended"] = extended
        if globstar is not None:
            options["globstar"] = globstar
        if case_insensitive is not None:
            options["case_insensitive"] = case_insensitive
        if options:
            params["options"] = convert_to_camel_case(options)

        result = await self._rpc.call("expandGlob", params)

        return result

    async def link(self, target: str, path: str) -> None:
        """Create a hard link pointing to an existing file."""

        params = {"target": target, "path": path}
        await self._rpc.call("link", params)

    async def lstat(self, path: str) -> FileInfo:
        """Return file information about a file or directory symlink."""

        params = {"path": path}
        result = await self._rpc.call("lstat", params)

        raw_result = convert_to_snake_case(result)
        return cast(FileInfo, raw_result)

    async def make_temp_dir(
        self,
        *,
        dir: Optional[str] = None,
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
    ) -> str:
        """Create a new temporary directory.

        Args:
            dir: The directory where the temporary directory should be created.
            prefix: The prefix for the temporary directory name.
            suffix: The suffix for the temporary directory name.
        """
        params: dict[str, Any] = {}
        options: dict[str, Any] = {}
        if dir is not None:
            options["dir"] = dir
        if prefix is not None:
            options["prefix"] = prefix
        if suffix is not None:
            options["suffix"] = suffix
        if options:
            params["options"] = convert_to_camel_case(options)

        result = await self._rpc.call("makeTempDir", params)

        return result

    async def make_temp_file(
        self,
        *,
        dir: Optional[str] = None,
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
    ) -> str:
        """Create a new temporary file.

        Args:
            dir: The directory where the temporary file should be created.
            prefix: The prefix for the temporary file name.
            suffix: The suffix for the temporary file name.
        """
        params: dict[str, Any] = {}
        options: dict[str, Any] = {}
        if dir is not None:
            options["dir"] = dir
        if prefix is not None:
            options["prefix"] = prefix
        if suffix is not None:
            options["suffix"] = suffix
        if options:
            params["options"] = convert_to_camel_case(options)

        result = await self._rpc.call("makeTempFile", params)

        return result

    async def read_link(self, path: str) -> str:
        """Read the target of a symbolic link."""

        params = {"path": path}
        result = await self._rpc.call("readLink", params)

        return result

    async def real_path(self, path: str) -> str:
        """Return the canonicalized absolute pathname."""

        params = {"path": path}
        result = await self._rpc.call("realPath", params)

        return result

    async def symlink(
        self,
        target: str,
        path: str,
        *,
        type: Optional[Literal["file", "dir", "junction"]] = None,
    ) -> None:
        """Create a symbolic link.

        Args:
            target: The target path of the symbolic link.
            path: The path where the symbolic link should be created.
            type: The type of the symbolic link (file, dir, or junction).
        """
        params: dict[str, Any] = {"target": target, "path": path}
        options: dict[str, Any] = {}
        if type is not None:
            options["type"] = type
        if options:
            params["options"] = convert_to_camel_case(options)

        await self._rpc.call("symlink", params)

    async def truncate(self, name: str, length: Optional[int] = None) -> None:
        """Truncate or extend the specified file to reach a given size."""

        params = {"name": name, "length": length}
        await self._rpc.call("truncate", params)

    async def umask(self, mask: Optional[int] = None) -> int:
        """Sets the process's file mode creation mask."""

        params = {"mask": mask}
        result = await self._rpc.call("umask", params)

        return result

    async def utime(self, path: str, atime: str, mtime: str) -> None:
        """Change the access and modification times of a file."""

        params = {"path": path, "atime": atime, "mtime": mtime}
        await self._rpc.call("utime", params)

    async def upload(self, local_path: str, sandbox_path: str) -> None:
        """Upload a file, directory, or symlink from local filesystem to the sandbox.

        Recursively uploads directories and their contents.
        Preserves symlinks by creating corresponding symlinks in the sandbox.
        """
        await self._upload_item(local_path, sandbox_path)

    async def _upload_item(self, local_path: str, sandbox_path: str) -> None:
        """Internal method to upload a single item (file, directory, or symlink)."""
        if os.path.islink(local_path):
            # It's a symlink - read the target and create a symlink in sandbox
            target = os.readlink(local_path)
            await self.symlink(target, sandbox_path)
        elif os.path.isdir(local_path):
            # It's a directory - create it and recursively upload contents
            await self.mkdir(sandbox_path, recursive=True)
            for entry in os.listdir(local_path):
                entry_local_path = os.path.join(local_path, entry)
                entry_sandbox_path = f"{sandbox_path}/{entry}"
                await self._upload_item(entry_local_path, entry_sandbox_path)
        elif os.path.isfile(local_path):
            # It's a file - stream it to write_file
            with open(local_path, "rb") as f:
                await self.write_file(sandbox_path, f)
        else:
            raise FileNotFoundError(f"Local path does not exist: {local_path}")

    async def download(self, local_path: str, sandbox_path: str) -> None:
        """Download a file or directory from the sandbox."""

        params = {"localPath": local_path, "sandboxPath": sandbox_path}
        await self._rpc.call("download", params)

    async def create(self, path: str) -> AsyncFsFile:
        """Create a new, empty file at the specified path."""

        params = {"path": path}
        result = await self._rpc.call("create", params)

        raw_result = convert_to_snake_case(result)
        handle = cast(FsFileHandle, raw_result)

        return AsyncFsFile(self._rpc, handle["file_handle_id"])

    async def open(
        self,
        path: str,
        *,
        read: Optional[bool] = None,
        write: Optional[bool] = None,
        append: Optional[bool] = None,
        truncate: Optional[bool] = None,
        create: Optional[bool] = None,
        create_new: Optional[bool] = None,
        mode: Optional[int] = None,
    ) -> AsyncFsFile:
        """Open a file and return a file descriptor.

        Args:
            path: The path to the file to open.
            read: Sets the option for read access. This option, when `true`, means that the file should be read-able if opened. Default: true.
            write: Sets the option for write access. This option, when `true`, means that the file should be write-able if opened. Default: false.
            append: Sets the option for append mode. This option, when `true`, means that writes to the file will always append to the end. Default: false.
            truncate: If `true`, and the file already exists and is a regular file, it will be truncated to length 0 when opened. Default: false.
            create: If `true`, the file will be created if it does not already exist. Default: false.
            create_new: If `true`, the file will be created if it does not already exist. Default: false.
            mode: The permission mode to use when creating the file.
        """
        params: dict[str, Any] = {"path": path}
        options: dict[str, Any] = {}
        if read is not None:
            options["read"] = read
        if write is not None:
            options["write"] = write
        if append is not None:
            options["append"] = append
        if truncate is not None:
            options["truncate"] = truncate
        if create is not None:
            options["create"] = create
        if create_new is not None:
            options["create_new"] = create_new
        if mode is not None:
            options["mode"] = mode
        if options:
            params["options"] = convert_to_camel_case(options)

        result = await self._rpc.call("open", params)

        raw_result = convert_to_snake_case(result)
        handle = cast(FsFileHandle, raw_result)

        return AsyncFsFile(self._rpc, handle["file_handle_id"])


class SandboxFs:
    """Filesystem operations inside the sandbox."""

    def __init__(self, rpc: AsyncRpcClient, bridge: AsyncBridge):
        self._rpc = rpc
        self._bridge = bridge
        self._async = AsyncSandboxFs(rpc)

    def read_file(
        self,
        path: str,
        *,
        signal: Optional[AbortSignal] = None,
    ) -> bytes:
        """Reads the entire contents of a file as bytes.

        Args:
            path: The path to the file to read.
            signal: An optional abort signal to cancel the operation.
        """
        return self._bridge.run(self._async.read_file(path, signal=signal))

    def write_file(
        self,
        path: str,
        data: Union[bytes, Iterable[bytes], BinaryIO],
        *,
        create: Optional[bool] = None,
        append: Optional[bool] = None,
        create_new: Optional[bool] = None,
        mode: Optional[int] = None,
    ) -> None:
        """Write bytes to file. Accepts bytes, sync iterables, or file objects.

        Args:
            path: The path to the file to write.
            data: The data to write to the file.
            create: Create file if it doesn't already exist.
            append: Append content instead of overwriting existing contents.
            create_new: Fail if the file already exists.
            mode: Set the file permission mode.
        """
        self._bridge.run(
            self._async.write_file(
                path,
                data,
                create=create,
                append=append,
                create_new=create_new,
                mode=mode,
            )
        )

    def read_text_file(
        self,
        path: str,
        *,
        signal: Optional[AbortSignal] = None,
    ) -> str:
        """Reads the entire contents of a file as an UTF-8 decoded string.

        Args:
            path: The path to the file to read.
            signal: An optional abort signal to cancel the operation.
        """
        return self._bridge.run(self._async.read_text_file(path, signal=signal))

    def write_text_file(
        self,
        path: str,
        content: str,
        *,
        create: Optional[bool] = None,
        append: Optional[bool] = None,
        create_new: Optional[bool] = None,
        mode: Optional[int] = None,
    ) -> None:
        """Write text to file. Creates a new file if needed. Existing files will be overwritten.

        Args:
            path: The path to the file to write.
            content: The text content to write.
            create: Create file if it doesn't already exist.
            append: Append content instead of overwriting existing contents.
            create_new: Fail if the file already exists.
            mode: Set the file permission mode.
        """
        self._bridge.run(
            self._async.write_text_file(
                path,
                content,
                create=create,
                append=append,
                create_new=create_new,
                mode=mode,
            )
        )

    def read_dir(self, path: str) -> list[DirEntry]:
        """Read the directory entries at the given path."""
        return self._bridge.run(self._async.read_dir(path))

    def remove(
        self,
        path: str,
        *,
        recursive: Optional[bool] = None,
    ) -> None:
        """Remove the file or directory at the given path.

        Args:
            path: The path to the file or directory to remove.
            recursive: Whether to remove directories recursively. Default: false.
        """
        self._bridge.run(self._async.remove(path, recursive=recursive))

    def mkdir(
        self,
        path: str,
        *,
        recursive: Optional[bool] = None,
        mode: Optional[int] = None,
    ) -> None:
        """Create a new directory at the specified path.

        Args:
            path: The path to the directory to create.
            recursive: If true, parent directories will be created if they do not already exist.
            mode: Permissions to use for the new directory.
        """
        self._bridge.run(self._async.mkdir(path, recursive=recursive, mode=mode))

    def rename(self, old_path: str, new_path: str) -> None:
        """Rename (move) a file or directory."""
        self._bridge.run(self._async.rename(old_path, new_path))

    def stat(self, path: str) -> FileInfo:
        """Return file information about a file or directory."""
        return self._bridge.run(self._async.stat(path))

    def chmod(self, path: str, mode: int) -> None:
        """Change the permission mode of a file or directory."""
        self._bridge.run(self._async.chmod(path, mode))

    def chown(
        self, path: str, uid: Optional[int] = None, gid: Optional[int] = None
    ) -> None:
        """Change the owner user ID and group ID of a file or directory."""
        self._bridge.run(self._async.chown(path, uid, gid))

    def copy_file(self, from_path: str, to_path: str) -> None:
        """Copy a file from a source path to a destination path."""
        self._bridge.run(self._async.copy_file(from_path, to_path))

    def walk(
        self,
        path: str,
        *,
        max_depth: Optional[int] = None,
        include_files: Optional[bool] = None,
        include_dirs: Optional[bool] = None,
        include_symlinks: Optional[bool] = None,
        follow_symlinks: Optional[bool] = None,
        canonicalize: Optional[bool] = None,
        exts: Optional[list[str]] = None,
        match: Optional[list[Pattern]] = None,
        skip: Optional[list[Pattern]] = None,
    ) -> list[WalkEntry]:
        """Recursively walk a directory tree.

        Args:
            path: The path to the directory to walk.
            max_depth: The maximum depth to traverse. Default: Infinity.
            include_files: Whether to include files in the results. Default: true.
            include_dirs: Whether to include directories in the results. Default: true.
            include_symlinks: Whether to include symbolic links in the results. Default: true.
            follow_symlinks: Whether to follow symbolic links. Default: false.
            canonicalize: Whether to return canonicalized paths. This option works only if `follow_symlinks` is not `false`. Default: false.
            exts: If provided, only files with the specified extensions will be included. Example: ['.ts', '.js']
            match: List of regular expression patterns used to filter entries. If specified, entries that do not match the patterns specified by this option are excluded.
            skip: List of regular expression patterns used to filter entries. If specified, entries that match the patterns specified by this option are excluded.
        """
        return self._bridge.run(
            self._async.walk(
                path,
                max_depth=max_depth,
                include_files=include_files,
                include_dirs=include_dirs,
                include_symlinks=include_symlinks,
                follow_symlinks=follow_symlinks,
                canonicalize=canonicalize,
                exts=exts,
                match=match,
                skip=skip,
            )
        )

    def expand_glob(
        self,
        glob: str,
        *,
        root: Optional[str] = None,
        exclude: Optional[list[str]] = None,
        include_dirs: Optional[bool] = None,
        follow_symlinks: Optional[bool] = None,
        canonicalize: Optional[bool] = None,
        extended: Optional[bool] = None,
        globstar: Optional[bool] = None,
        case_insensitive: Optional[bool] = None,
    ) -> list[str]:
        """Expand a glob pattern to a list of paths.

        Args:
            glob: The glob pattern to expand.
            root: The root directory from which to expand the glob pattern. Default is the current working directory.
            exclude: An array of glob patterns to exclude from the results.
            include_dirs: Whether to include directories in the results. Default: true.
            follow_symlinks: Whether to follow symbolic links. Default: false.
            canonicalize: Whether to return canonicalized paths. This option works only if `follow_symlinks` is not `false`. Default: true.
            extended: Whether to enable extended glob syntax, see https://www.linuxjournal.com/content/bash-extended-globbing. Default: true.
            globstar: Globstar syntax. See https://www.linuxjournal.com/content/globstar-new-bash-globbing-option. If false, `**` is treated like `*`. Default: true.
            case_insensitive: Whether the glob matching should be case insensitive. Default: false.
        """
        return self._bridge.run(
            self._async.expand_glob(
                glob,
                root=root,
                exclude=exclude,
                include_dirs=include_dirs,
                follow_symlinks=follow_symlinks,
                canonicalize=canonicalize,
                extended=extended,
                globstar=globstar,
                case_insensitive=case_insensitive,
            )
        )

    def link(self, target: str, path: str) -> None:
        """Create a hard link pointing to an existing file."""
        self._bridge.run(self._async.link(target, path))

    def lstat(self, path: str) -> FileInfo:
        """Return file information about a file or directory symlink."""
        return self._bridge.run(self._async.lstat(path))

    def make_temp_dir(
        self,
        *,
        dir: Optional[str] = None,
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
    ) -> str:
        """Create a new temporary directory.

        Args:
            dir: The directory where the temporary directory should be created.
            prefix: The prefix for the temporary directory name.
            suffix: The suffix for the temporary directory name.
        """
        return self._bridge.run(
            self._async.make_temp_dir(dir=dir, prefix=prefix, suffix=suffix)
        )

    def make_temp_file(
        self,
        *,
        dir: Optional[str] = None,
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
    ) -> str:
        """Create a new temporary file.

        Args:
            dir: The directory where the temporary file should be created.
            prefix: The prefix for the temporary file name.
            suffix: The suffix for the temporary file name.
        """
        return self._bridge.run(
            self._async.make_temp_file(dir=dir, prefix=prefix, suffix=suffix)
        )

    def read_link(self, path: str) -> str:
        """Read the target of a symbolic link."""
        return self._bridge.run(self._async.read_link(path))

    def real_path(self, path: str) -> str:
        """Return the canonicalized absolute pathname."""
        return self._bridge.run(self._async.real_path(path))

    def symlink(
        self,
        target: str,
        path: str,
        *,
        type: Optional[Literal["file", "dir", "junction"]] = None,
    ) -> None:
        """Create a symbolic link.

        Args:
            target: The target path of the symbolic link.
            path: The path where the symbolic link should be created.
            type: The type of the symbolic link (file, dir, or junction).
        """
        self._bridge.run(self._async.symlink(target, path, type=type))

    def truncate(self, name: str, length: Optional[int] = None) -> None:
        """Truncate or extend the specified file to reach a given size."""
        self._bridge.run(self._async.truncate(name, length))

    def umask(self, mask: Optional[int] = None) -> int:
        """Sets the process's file mode creation mask."""
        return self._bridge.run(self._async.umask(mask))

    def utime(self, path: str, atime: str, mtime: str) -> None:
        """Change the access and modification times of a file."""
        self._bridge.run(self._async.utime(path, atime, mtime))

    def upload(self, local_path: str, sandbox_path: str) -> None:
        """Upload a file, directory, or symlink from local filesystem to the sandbox."""
        self._bridge.run(self._async.upload(local_path, sandbox_path))

    def download(self, local_path: str, sandbox_path: str) -> None:
        """Download a file or directory from the sandbox."""
        self._bridge.run(self._async.download(local_path, sandbox_path))

    def create(self, path: str) -> FsFile:
        """Create a new, empty file at the specified path."""
        async_file = self._bridge.run(self._async.create(path))
        return FsFile(self._rpc, self._bridge, async_file._fd)

    def open(
        self,
        path: str,
        *,
        read: Optional[bool] = None,
        write: Optional[bool] = None,
        append: Optional[bool] = None,
        truncate: Optional[bool] = None,
        create: Optional[bool] = None,
        create_new: Optional[bool] = None,
        mode: Optional[int] = None,
    ) -> FsFile:
        """Open a file and return a file descriptor.

        Args:
            path: The path to the file to open.
            read: Sets the option for read access. This option, when `true`, means that the file should be read-able if opened. Default: true.
            write: Sets the option for write access. This option, when `true`, means that the file should be write-able if opened. Default: false.
            append: Sets the option for append mode. This option, when `true`, means that writes to the file will always append to the end. Default: false.
            truncate: If `true`, and the file already exists and is a regular file, it will be truncated to length 0 when opened. Default: false.
            create: If `true`, the file will be created if it does not already exist. Default: false.
            create_new: If `true`, the file will be created if it does not already exist. Default: false.
            mode: The permission mode to use when creating the file.
        """
        async_file = self._bridge.run(
            self._async.open(
                path,
                read=read,
                write=write,
                append=append,
                truncate=truncate,
                create=create,
                create_new=create_new,
                mode=mode,
            )
        )
        return FsFile(self._rpc, self._bridge, async_file._fd)
