# coding: utf-8

"""
Filesystem operations for Koyeb Sandbox instances
Using SandboxClient HTTP API
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List, Union

from .executor_client import AsyncSandboxClient, SandboxClient
from .utils import (
    SandboxError,
    check_error_message,
    escape_shell_arg,
)

if TYPE_CHECKING:
    from .exec import AsyncSandboxExecutor, SandboxExecutor
    from .sandbox import Sandbox


class SandboxFilesystemError(SandboxError):
    """Base exception for filesystem operations"""


class SandboxFileNotFoundError(SandboxFilesystemError):
    """Raised when file or directory not found"""


class SandboxFileExistsError(SandboxFilesystemError):
    """Raised when file already exists"""


@dataclass
class FileInfo:
    """File information"""

    content: Union[str, bytes]
    encoding: str


class SandboxFilesystem:
    """
    Synchronous filesystem operations for Koyeb Sandbox instances.
    Using SandboxClient HTTP API.

    For async usage, use AsyncSandboxFilesystem instead.
    """

    def __init__(self, sandbox: Sandbox) -> None:
        self.sandbox = sandbox
        self._executor = None

    def _get_client(self) -> SandboxClient:
        """Get or create SandboxClient instance, shared with the sandbox"""
        return self.sandbox._get_client()

    def _get_executor(self) -> "SandboxExecutor":
        """Get or create SandboxExecutor instance"""
        if self._executor is None:
            from .exec import SandboxExecutor

            self._executor = SandboxExecutor(self.sandbox)
        return self._executor

    def write_file(
        self, path: str, content: Union[str, bytes], encoding: str = "utf-8"
    ) -> None:
        """
        Write content to a file synchronously.

        Args:
            path: Absolute path to the file
            content: Content to write (string or bytes)
            encoding: File encoding (default: "utf-8"). Use "base64" for binary data.
        """
        import base64

        client = self._get_client()

        if isinstance(content, bytes):
            if encoding == "base64":
                content_str = base64.b64encode(content).decode("ascii")
            else:
                content_str = content.decode(encoding)
        else:
            content_str = content

        try:
            response = client.write_file(path, content_str)
            if response.get("error"):
                error_msg = response.get("error", "Unknown error")
                raise SandboxFilesystemError(f"Failed to write file: {error_msg}")
        except Exception as e:
            if isinstance(e, SandboxFilesystemError):
                raise
            raise SandboxFilesystemError(f"Failed to write file: {str(e)}") from e

    def read_file(self, path: str, encoding: str = "utf-8") -> FileInfo:
        """
        Read a file from the sandbox synchronously.

        Args:
            path: Absolute path to the file
            encoding: File encoding (default: "utf-8"). Use "base64" for binary data,
                      which will decode the base64 content and return bytes.

        Returns:
            FileInfo: Object with content (str or bytes if base64) and encoding
        """
        import base64 as base64_module

        client = self._get_client()

        try:
            response = client.read_file(path)
            if response.get("error"):
                error_msg = response.get("error", "Unknown error")
                if check_error_message(error_msg, "NO_SUCH_FILE"):
                    raise SandboxFileNotFoundError(f"File not found: {path}")
                raise SandboxFilesystemError(f"Failed to read file: {error_msg}")
            content_str = response.get("content", "")
            if encoding == "base64":
                content: Union[str, bytes] = base64_module.b64decode(content_str)
            else:
                content = content_str
            return FileInfo(content=content, encoding=encoding)
        except (SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            error_msg = str(e)
            if check_error_message(error_msg, "NO_SUCH_FILE"):
                raise SandboxFileNotFoundError(f"File not found: {path}") from e
            raise SandboxFilesystemError(f"Failed to read file: {error_msg}") from e

    def mkdir(self, path: str) -> None:
        """
        Create a directory synchronously.

        Note: Parent directories are always created automatically by the API.

        Args:
            path: Absolute path to the directory
        """
        client = self._get_client()

        try:
            response = client.make_dir(path)
            if response.get("error"):
                error_msg = response.get("error", "Unknown error")
                if check_error_message(error_msg, "FILE_EXISTS"):
                    raise SandboxFileExistsError(f"Directory already exists: {path}")
                raise SandboxFilesystemError(f"Failed to create directory: {error_msg}")
        except (SandboxFileExistsError, SandboxFilesystemError):
            raise
        except Exception as e:
            error_msg = str(e)
            if check_error_message(error_msg, "FILE_EXISTS"):
                raise SandboxFileExistsError(f"Directory already exists: {path}") from e
            raise SandboxFilesystemError(
                f"Failed to create directory: {error_msg}"
            ) from e

    def list_dir(self, path: str = ".") -> List[str]:
        """
        List contents of a directory synchronously.

        Args:
            path: Path to the directory (default: current directory)

        Returns:
            List[str]: Names of files and directories within the specified path.
        """
        client = self._get_client()

        try:
            response = client.list_dir(path)
            if response.get("error"):
                error_msg = response.get("error", "Unknown error")
                if check_error_message(error_msg, "NO_SUCH_FILE"):
                    raise SandboxFileNotFoundError(f"Directory not found: {path}")
                raise SandboxFilesystemError(f"Failed to list directory: {error_msg}")
            entries = response.get("entries", [])
            return entries
        except (SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            error_msg = str(e)
            if check_error_message(error_msg, "NO_SUCH_FILE"):
                raise SandboxFileNotFoundError(f"Directory not found: {path}") from e
            raise SandboxFilesystemError(
                f"Failed to list directory: {error_msg}"
            ) from e

    def delete_file(self, path: str) -> None:
        """
        Delete a file synchronously.

        Args:
            path: Absolute path to the file
        """
        client = self._get_client()

        try:
            response = client.delete_file(path)
            if response.get("error"):
                error_msg = response.get("error", "Unknown error")
                if check_error_message(error_msg, "NO_SUCH_FILE"):
                    raise SandboxFileNotFoundError(f"File not found: {path}")
                raise SandboxFilesystemError(f"Failed to delete file: {error_msg}")
        except (SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            error_msg = str(e)
            if check_error_message(error_msg, "NO_SUCH_FILE"):
                raise SandboxFileNotFoundError(f"File not found: {path}") from e
            raise SandboxFilesystemError(f"Failed to delete file: {error_msg}") from e

    def delete_dir(self, path: str) -> None:
        """
        Delete a directory synchronously.

        Args:
            path: Absolute path to the directory
        """
        client = self._get_client()

        try:
            response = client.delete_dir(path)
            if response.get("error"):
                error_msg = response.get("error", "Unknown error")
                if check_error_message(error_msg, "NO_SUCH_FILE"):
                    raise SandboxFileNotFoundError(f"Directory not found: {path}")
                if check_error_message(error_msg, "DIR_NOT_EMPTY"):
                    raise SandboxFilesystemError(f"Directory not empty: {path}")
                raise SandboxFilesystemError(f"Failed to delete directory: {error_msg}")
        except (SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            error_msg = str(e)
            if check_error_message(error_msg, "NO_SUCH_FILE"):
                raise SandboxFileNotFoundError(f"Directory not found: {path}") from e
            if check_error_message(error_msg, "DIR_NOT_EMPTY"):
                raise SandboxFilesystemError(f"Directory not empty: {path}") from e
            raise SandboxFilesystemError(
                f"Failed to delete directory: {error_msg}"
            ) from e

    def rename_file(self, old_path: str, new_path: str) -> None:
        """
        Rename a file synchronously.

        Args:
            old_path: Current file path
            new_path: New file path
        """
        # Use exec since there's no direct rename in SandboxClient
        # Properly escape paths to prevent shell injection
        executor = self._get_executor()
        old_path_escaped = escape_shell_arg(old_path)
        new_path_escaped = escape_shell_arg(new_path)
        result = executor(f"mv {old_path_escaped} {new_path_escaped}")

        if not result.success:
            if check_error_message(result.stderr, "NO_SUCH_FILE"):
                raise SandboxFileNotFoundError(f"File not found: {old_path}")
            raise SandboxFilesystemError(f"Failed to rename file: {result.stderr}")

    def move_file(self, source_path: str, destination_path: str) -> None:
        """
        Move a file to a different directory synchronously.

        Args:
            source_path: Current file path
            destination_path: Destination path
        """
        # Use exec since there's no direct move in SandboxClient
        # Properly escape paths to prevent shell injection
        executor = self._get_executor()
        source_path_escaped = escape_shell_arg(source_path)
        destination_path_escaped = escape_shell_arg(destination_path)
        result = executor(f"mv {source_path_escaped} {destination_path_escaped}")

        if not result.success:
            if check_error_message(result.stderr, "NO_SUCH_FILE"):
                raise SandboxFileNotFoundError(f"File not found: {source_path}")
            raise SandboxFilesystemError(f"Failed to move file: {result.stderr}")

    def write_files(self, files: List[Dict[str, str]]) -> None:
        """
        Write multiple files in a single operation synchronously.

        Args:
            files: List of dictionaries, each with 'path', 'content', and optional 'encoding'.
        """
        for file_info in files:
            path = file_info["path"]
            content = file_info["content"]
            encoding = file_info.get("encoding", "utf-8")
            SandboxFilesystem.write_file(self, path, content, encoding)

    def exists(self, path: str) -> bool:
        """Check if file/directory exists synchronously"""
        executor = self._get_executor()
        path_escaped = escape_shell_arg(path)
        result = executor(f"test -e {path_escaped}")
        return result.success

    def is_file(self, path: str) -> bool:
        """Check if path is a file synchronously"""
        executor = self._get_executor()
        path_escaped = escape_shell_arg(path)
        result = executor(f"test -f {path_escaped}")
        return result.success

    def is_dir(self, path: str) -> bool:
        """Check if path is a directory synchronously"""
        executor = self._get_executor()
        path_escaped = escape_shell_arg(path)
        result = executor(f"test -d {path_escaped}")
        return result.success

    def upload_file(
        self, local_path: str, remote_path: str, encoding: str = "utf-8"
    ) -> None:
        """
        Upload a local file to the sandbox synchronously.

        Args:
            local_path: Path to the local file
            remote_path: Destination path in the sandbox
            encoding: File encoding (default: "utf-8"). Use "base64" for binary files.

        Raises:
            SandboxFileNotFoundError: If local file doesn't exist
            UnicodeDecodeError: If file cannot be decoded with specified encoding
        """
        if not os.path.exists(local_path):
            raise SandboxFileNotFoundError(f"Local file not found: {local_path}")

        with open(local_path, "rb") as f:
            content_bytes = f.read()

        SandboxFilesystem.write_file(self, remote_path, content_bytes, encoding=encoding)

    def download_file(
        self, remote_path: str, local_path: str, encoding: str = "utf-8"
    ) -> None:
        """
        Download a file from the sandbox to a local path synchronously.

        Args:
            remote_path: Path to the file in the sandbox
            local_path: Destination path on the local filesystem
            encoding: File encoding (default: "utf-8"). Use "base64" for binary files.

        Raises:
            SandboxFileNotFoundError: If remote file doesn't exist
        """
        file_info = SandboxFilesystem.read_file(self, remote_path, encoding=encoding)

        if isinstance(file_info.content, bytes):
            content_bytes = file_info.content
        else:
            content_bytes = file_info.content.encode(encoding)

        with open(local_path, "wb") as f:
            f.write(content_bytes)

    def ls(self, path: str = ".") -> List[str]:
        """
        List directory contents synchronously.

        Args:
            path: Path to list

        Returns:
            List of file/directory names
        """
        return SandboxFilesystem.list_dir(self, path)

    def rm(self, path: str, recursive: bool = False) -> None:
        """
        Remove file or directory synchronously.

        Args:
            path: Path to remove
            recursive: Remove recursively
        """
        executor = self._get_executor()
        path_escaped = escape_shell_arg(path)

        if recursive:
            result = executor(f"rm -rf {path_escaped}")
        else:
            result = executor(f"rm {path_escaped}")

        if not result.success:
            if check_error_message(result.stderr, "NO_SUCH_FILE"):
                raise SandboxFileNotFoundError(f"File not found: {path}")
            raise SandboxFilesystemError(f"Failed to remove: {result.stderr}")

    def open(
        self, path: str, mode: str = "r", encoding: str = "utf-8"
    ) -> SandboxFileIO:
        """
        Open a file in the sandbox synchronously.

        Args:
            path: Path to the file
            mode: Open mode ('r', 'w', 'a', etc.)
            encoding: File encoding (default: "utf-8"). Use "base64" for binary data.

        Returns:
            SandboxFileIO: File handle
        """
        return SandboxFileIO(self, path, mode, encoding)


class AsyncSandboxFilesystem(SandboxFilesystem):
    """
    Async filesystem operations for Koyeb Sandbox instances.
    Uses native async I/O via AsyncSandboxClient.
    """

    def _get_async_client(self) -> AsyncSandboxClient:
        """Get AsyncSandboxClient instance from the sandbox."""
        return self.sandbox._get_async_client()

    def _get_async_executor(self) -> "AsyncSandboxExecutor":
        """Get or create AsyncSandboxExecutor instance."""
        if self._executor is None:
            from .exec import AsyncSandboxExecutor

            self._executor = AsyncSandboxExecutor(self.sandbox)
        return self._executor

    async def write_file(
        self, path: str, content: Union[str, bytes], encoding: str = "utf-8"
    ) -> None:
        """
        Write content to a file asynchronously.

        Args:
            path: Absolute path to the file
            content: Content to write (string or bytes)
            encoding: File encoding (default: "utf-8"). Use "base64" for binary data.
        """
        import base64

        client = self._get_async_client()

        if isinstance(content, bytes):
            if encoding == "base64":
                content_str = base64.b64encode(content).decode("ascii")
            else:
                content_str = content.decode(encoding)
        else:
            content_str = content

        try:
            response = await client.write_file(path, content_str)
            if response.get("error"):
                error_msg = response.get("error", "Unknown error")
                raise SandboxFilesystemError(f"Failed to write file: {error_msg}")
        except Exception as e:
            if isinstance(e, SandboxFilesystemError):
                raise
            raise SandboxFilesystemError(f"Failed to write file: {str(e)}") from e

    async def read_file(self, path: str, encoding: str = "utf-8") -> FileInfo:
        """
        Read a file from the sandbox asynchronously.

        Args:
            path: Absolute path to the file
            encoding: File encoding (default: "utf-8"). Use "base64" for binary data,
                      which will decode the base64 content and return bytes.

        Returns:
            FileInfo: Object with content (str or bytes if base64) and encoding
        """
        import base64 as base64_module

        client = self._get_async_client()

        try:
            response = await client.read_file(path)
            if response.get("error"):
                error_msg = response.get("error", "Unknown error")
                if check_error_message(error_msg, "NO_SUCH_FILE"):
                    raise SandboxFileNotFoundError(f"File not found: {path}")
                raise SandboxFilesystemError(f"Failed to read file: {error_msg}")
            content_str = response.get("content", "")
            if encoding == "base64":
                content: Union[str, bytes] = base64_module.b64decode(content_str)
            else:
                content = content_str
            return FileInfo(content=content, encoding=encoding)
        except (SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            error_msg = str(e)
            if check_error_message(error_msg, "NO_SUCH_FILE"):
                raise SandboxFileNotFoundError(f"File not found: {path}") from e
            raise SandboxFilesystemError(f"Failed to read file: {error_msg}") from e

    async def mkdir(self, path: str) -> None:
        """
        Create a directory asynchronously.

        Note: Parent directories are always created automatically by the API.

        Args:
            path: Absolute path to the directory
        """
        client = self._get_async_client()

        try:
            response = await client.make_dir(path)
            if response.get("error"):
                error_msg = response.get("error", "Unknown error")
                if check_error_message(error_msg, "FILE_EXISTS"):
                    raise SandboxFileExistsError(f"Directory already exists: {path}")
                raise SandboxFilesystemError(f"Failed to create directory: {error_msg}")
        except (SandboxFileExistsError, SandboxFilesystemError):
            raise
        except Exception as e:
            error_msg = str(e)
            if check_error_message(error_msg, "FILE_EXISTS"):
                raise SandboxFileExistsError(f"Directory already exists: {path}") from e
            raise SandboxFilesystemError(
                f"Failed to create directory: {error_msg}"
            ) from e

    async def list_dir(self, path: str = ".") -> List[str]:
        """
        List contents of a directory asynchronously.

        Args:
            path: Path to the directory (default: current directory)

        Returns:
            List[str]: Names of files and directories within the specified path.
        """
        client = self._get_async_client()

        try:
            response = await client.list_dir(path)
            if response.get("error"):
                error_msg = response.get("error", "Unknown error")
                if check_error_message(error_msg, "NO_SUCH_FILE"):
                    raise SandboxFileNotFoundError(f"Directory not found: {path}")
                raise SandboxFilesystemError(f"Failed to list directory: {error_msg}")
            entries = response.get("entries", [])
            return entries
        except (SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            error_msg = str(e)
            if check_error_message(error_msg, "NO_SUCH_FILE"):
                raise SandboxFileNotFoundError(f"Directory not found: {path}") from e
            raise SandboxFilesystemError(
                f"Failed to list directory: {error_msg}"
            ) from e

    async def delete_file(self, path: str) -> None:
        """
        Delete a file asynchronously.

        Args:
            path: Absolute path to the file
        """
        client = self._get_async_client()

        try:
            response = await client.delete_file(path)
            if response.get("error"):
                error_msg = response.get("error", "Unknown error")
                if check_error_message(error_msg, "NO_SUCH_FILE"):
                    raise SandboxFileNotFoundError(f"File not found: {path}")
                raise SandboxFilesystemError(f"Failed to delete file: {error_msg}")
        except (SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            error_msg = str(e)
            if check_error_message(error_msg, "NO_SUCH_FILE"):
                raise SandboxFileNotFoundError(f"File not found: {path}") from e
            raise SandboxFilesystemError(f"Failed to delete file: {error_msg}") from e

    async def delete_dir(self, path: str) -> None:
        """
        Delete a directory asynchronously.

        Args:
            path: Absolute path to the directory
        """
        client = self._get_async_client()

        try:
            response = await client.delete_dir(path)
            if response.get("error"):
                error_msg = response.get("error", "Unknown error")
                if check_error_message(error_msg, "NO_SUCH_FILE"):
                    raise SandboxFileNotFoundError(f"Directory not found: {path}")
                if check_error_message(error_msg, "DIR_NOT_EMPTY"):
                    raise SandboxFilesystemError(f"Directory not empty: {path}")
                raise SandboxFilesystemError(f"Failed to delete directory: {error_msg}")
        except (SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            error_msg = str(e)
            if check_error_message(error_msg, "NO_SUCH_FILE"):
                raise SandboxFileNotFoundError(f"Directory not found: {path}") from e
            if check_error_message(error_msg, "DIR_NOT_EMPTY"):
                raise SandboxFilesystemError(f"Directory not empty: {path}") from e
            raise SandboxFilesystemError(
                f"Failed to delete directory: {error_msg}"
            ) from e

    async def rename_file(self, old_path: str, new_path: str) -> None:
        """
        Rename a file asynchronously.

        Args:
            old_path: Current file path
            new_path: New file path
        """
        executor = self._get_async_executor()
        old_path_escaped = escape_shell_arg(old_path)
        new_path_escaped = escape_shell_arg(new_path)
        result = await executor(f"mv {old_path_escaped} {new_path_escaped}")

        if not result.success:
            if check_error_message(result.stderr, "NO_SUCH_FILE"):
                raise SandboxFileNotFoundError(f"File not found: {old_path}")
            raise SandboxFilesystemError(f"Failed to rename file: {result.stderr}")

    async def move_file(self, source_path: str, destination_path: str) -> None:
        """
        Move a file to a different directory asynchronously.

        Args:
            source_path: Current file path
            destination_path: Destination path
        """
        executor = self._get_async_executor()
        source_path_escaped = escape_shell_arg(source_path)
        destination_path_escaped = escape_shell_arg(destination_path)
        result = await executor(f"mv {source_path_escaped} {destination_path_escaped}")

        if not result.success:
            if check_error_message(result.stderr, "NO_SUCH_FILE"):
                raise SandboxFileNotFoundError(f"File not found: {source_path}")
            raise SandboxFilesystemError(f"Failed to move file: {result.stderr}")

    async def write_files(self, files: List[Dict[str, str]]) -> None:
        """
        Write multiple files in a single operation asynchronously.

        Args:
            files: List of dictionaries, each with 'path', 'content', and optional 'encoding'.
        """
        for file_info in files:
            path = file_info["path"]
            content = file_info["content"]
            encoding = file_info.get("encoding", "utf-8")
            await self.write_file(path, content, encoding)

    async def exists(self, path: str) -> bool:
        """Check if file/directory exists asynchronously"""
        executor = self._get_async_executor()
        path_escaped = escape_shell_arg(path)
        result = await executor(f"test -e {path_escaped}")
        return result.success

    async def is_file(self, path: str) -> bool:
        """Check if path is a file asynchronously"""
        executor = self._get_async_executor()
        path_escaped = escape_shell_arg(path)
        result = await executor(f"test -f {path_escaped}")
        return result.success

    async def is_dir(self, path: str) -> bool:
        """Check if path is a directory asynchronously"""
        executor = self._get_async_executor()
        path_escaped = escape_shell_arg(path)
        result = await executor(f"test -d {path_escaped}")
        return result.success

    async def upload_file(
        self, local_path: str, remote_path: str, encoding: str = "utf-8"
    ) -> None:
        """
        Upload a local file to the sandbox asynchronously.

        Args:
            local_path: Path to the local file
            remote_path: Destination path in the sandbox
            encoding: File encoding (default: "utf-8"). Use "base64" for binary files.

        Raises:
            SandboxFileNotFoundError: If local file doesn't exist
            UnicodeDecodeError: If file cannot be decoded with specified encoding
        """
        if not os.path.exists(local_path):
            raise SandboxFileNotFoundError(f"Local file not found: {local_path}")

        with open(local_path, "rb") as f:
            content_bytes = f.read()

        await self.write_file(remote_path, content_bytes, encoding=encoding)

    async def download_file(
        self, remote_path: str, local_path: str, encoding: str = "utf-8"
    ) -> None:
        """
        Download a file from the sandbox to a local path asynchronously.

        Args:
            remote_path: Path to the file in the sandbox
            local_path: Destination path on the local filesystem
            encoding: File encoding (default: "utf-8"). Use "base64" for binary files.

        Raises:
            SandboxFileNotFoundError: If remote file doesn't exist
        """
        file_info = await self.read_file(remote_path, encoding=encoding)

        if isinstance(file_info.content, bytes):
            content_bytes = file_info.content
        else:
            content_bytes = file_info.content.encode(encoding)

        with open(local_path, "wb") as f:
            f.write(content_bytes)

    async def ls(self, path: str = ".") -> List[str]:
        """
        List directory contents asynchronously.

        Args:
            path: Path to list

        Returns:
            List of file/directory names
        """
        return await self.list_dir(path)

    async def rm(self, path: str, recursive: bool = False) -> None:
        """
        Remove file or directory asynchronously.

        Args:
            path: Path to remove
            recursive: Remove recursively
        """
        executor = self._get_async_executor()
        path_escaped = escape_shell_arg(path)

        if recursive:
            result = await executor(f"rm -rf {path_escaped}")
        else:
            result = await executor(f"rm {path_escaped}")

        if not result.success:
            if check_error_message(result.stderr, "NO_SUCH_FILE"):
                raise SandboxFileNotFoundError(f"File not found: {path}")
            raise SandboxFilesystemError(f"Failed to remove: {result.stderr}")

    def open(
        self, path: str, mode: str = "r", encoding: str = "utf-8"
    ) -> AsyncSandboxFileIO:
        """
        Open a file in the sandbox asynchronously.

        Args:
            path: Path to the file
            mode: Open mode ('r', 'w', 'a', etc.)
            encoding: File encoding (default: "utf-8"). Use "base64" for binary data.

        Returns:
            AsyncSandboxFileIO: Async file handle
        """
        return AsyncSandboxFileIO(self, path, mode, encoding)


class SandboxFileIO:
    """Synchronous file I/O handle for sandbox files"""

    def __init__(
        self,
        filesystem: SandboxFilesystem,
        path: str,
        mode: str,
        encoding: str = "utf-8",
    ):
        self.filesystem = filesystem
        self.path = path
        self.mode = mode
        self.encoding = encoding
        self._closed = False

    def read(self) -> Union[str, bytes]:
        """Read file content synchronously"""
        if "r" not in self.mode:
            raise ValueError("File not opened for reading")

        if self._closed:
            raise ValueError("File is closed")

        file_info = self.filesystem.read_file(self.path, encoding=self.encoding)
        return file_info.content

    def write(self, content: Union[str, bytes]) -> None:
        """Write content to file synchronously"""
        if "w" not in self.mode and "a" not in self.mode:
            raise ValueError("File not opened for writing")

        if self._closed:
            raise ValueError("File is closed")

        if "a" in self.mode:
            try:
                existing = self.filesystem.read_file(self.path, encoding=self.encoding)
                if isinstance(existing.content, bytes) and isinstance(content, bytes):
                    content = existing.content + content
                elif isinstance(existing.content, str) and isinstance(content, str):
                    content = existing.content + content
                else:
                    raise TypeError("Cannot mix bytes and str content in append mode")
            except SandboxFileNotFoundError:
                pass

        self.filesystem.write_file(self.path, content, encoding=self.encoding)

    def close(self) -> None:
        """Close the file"""
        self._closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class AsyncSandboxFileIO:
    """Async file I/O handle for sandbox files"""

    def __init__(
        self,
        filesystem: AsyncSandboxFilesystem,
        path: str,
        mode: str,
        encoding: str = "utf-8",
    ):
        self.filesystem = filesystem
        self.path = path
        self.mode = mode
        self.encoding = encoding
        self._closed = False

    async def read(self) -> Union[str, bytes]:
        """Read file content asynchronously"""
        if "r" not in self.mode:
            raise ValueError("File not opened for reading")

        if self._closed:
            raise ValueError("File is closed")

        file_info = await self.filesystem.read_file(self.path, encoding=self.encoding)
        return file_info.content

    async def write(self, content: Union[str, bytes]) -> None:
        """Write content to file asynchronously"""
        if "w" not in self.mode and "a" not in self.mode:
            raise ValueError("File not opened for writing")

        if self._closed:
            raise ValueError("File is closed")

        if "a" in self.mode:
            try:
                existing = await self.filesystem.read_file(
                    self.path, encoding=self.encoding
                )
                if isinstance(existing.content, bytes) and isinstance(content, bytes):
                    content = existing.content + content
                elif isinstance(existing.content, str) and isinstance(content, str):
                    content = existing.content + content
                else:
                    raise TypeError("Cannot mix bytes and str content in append mode")
            except SandboxFileNotFoundError:
                pass

        await self.filesystem.write_file(self.path, content, encoding=self.encoding)

    def close(self) -> None:
        """Close the file"""
        self._closed = True

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()
