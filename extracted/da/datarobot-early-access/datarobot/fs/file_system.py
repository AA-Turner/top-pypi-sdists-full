#
# Copyright 2026 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from collections import defaultdict
from contextlib import contextmanager
from datetime import datetime
from glob import has_magic
from http import HTTPStatus
import io
import math
import os
import tempfile
import time
from typing import (
    Any,
    Dict,
    Generator,
    Iterable,
    List,
    Literal,
    Match,
    Optional,
    Set,
    Tuple,
    Type,
    TypedDict,
    Union,
    cast,
    overload,
)

from fsspec import AbstractFileSystem
from fsspec.callbacks import DEFAULT_CALLBACK, Callback
from fsspec.implementations.local import LocalFileSystem, make_path_posix, trailing_sep
from fsspec.mapping import FSMap, maybe_convert
from fsspec.spec import AbstractBufferedFile
from fsspec.utils import common_prefix, glob_translate, other_paths, stringify_path
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from datarobot.enums import DEFAULT_MAX_WAIT, FilesOverwriteStrategy
from datarobot.errors import AsyncProcessUnsuccessfulError, ClientError
from datarobot.fs.utils import is_datarobot_url, supports_range_requests
from datarobot.models.files import (
    File,
    Files,
    FilesCatalogSearch,
    FilesDetails,
)


class FileInfo(TypedDict):
    """
    Information about a file or directory in DataRobot File System.

    Attributes
    ----------
    name:
        The path of the file or directory. Does not include the protocol prefix.
    size:
        The size of the file in bytes. For directories, this is 0.
    type:
        The type of the item, either 'file' or 'directory'.
    format:
        The file format (e.g., 'csv', 'pdf') if the item is a file; None for directories.
    created_at:
        The file creation timestamp if the item is a file; None for directories.
    """

    name: str
    size: int
    type: Literal["file", "directory"]
    format: Optional[str]
    created_at: Optional[datetime]


class DataRobotFileSystem(AbstractFileSystem):  # type: ignore[misc]
    """
    `fsspec <https://filesystem-spec.readthedocs.io/en/latest/index.html>`_ implementation
    of DataRobot's file system.

    File paths are of the form:
        ``dr://<catalog_item_id>/path/to/file.txt`` or ``<catalog_item_id>/path/to/file.txt``

    Attributes
    ----------
    protocol: str
        The protocol prefix for the DataRobot file system. Can be removed with :meth:`_strip_protocol`.
    root_marker: str
        The root path of the DataRobot file system.

    Examples
    --------
    .. code-block:: python

        >>> from datarobot.fs import DataRobotFileSystem
        >>> fs = DataRobotFileSystem()

    List all catalog items in the file system:

    .. code-block:: python

        >>> fs.ls("")
        ['696935d6d5a04a752419cf6d/', '69691fc3d5a04a752419cf5c/']

    Create a new catalog item to hold your files:

    .. code-block:: python

        >>> catalog_id = fs.create_catalog_item_dir()
        >>> fs.put_file("local/path/to/file.txt", f"dr://{catalog_id}/file.txt")
        >>> fs.ls(f"dr://{catalog_id}/")
        ['file.txt']

    Find all PDF files you've uploaded to your catalog item:

    .. code-block:: python

        >>> fs.glob(f"dr://{catalog_id}/**/*.pdf")
        ['696935d6d5a04a752419cf6d/file.pdf', '696935d6d5a04a752419cf6d/finance/fy-2024/budgets/Q2_budget_2024.pdf']

    Copy, move or delete your files:

    .. code-block:: python

        >>> fs.copy(f"dr://{catalog_id}/file.txt", f"dr://{catalog_id}/file_copy.txt")
        >>> fs.move(f"dr://{catalog_id}/file_copy.txt", f"dr://{catalog_id}/file_moved.txt")
        >>> fs.rm(f"dr://{catalog_id}/file_moved.txt")

    Open files for reading or writing:

    .. code-block:: python

        >>> with fs.open(f"dr://{catalog_id}/new_file.txt", mode="w") as f:
        ...     f.write("Hello, world!")

        >>> with fs.open(f"dr://{catalog_id}/new_file.txt", mode="r") as f:
        ...     data = f.read()
        ...     print(data)
        Hello, world!
    """

    protocol = "dr"
    root_marker = ""  # Root does not need leading slash (/)

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @classmethod
    def _strip_protocol(cls, path: str) -> str:
        """
        Turn path from fully-qualified to DR file system specific.

        Parameters
        ----------
        path:
            File path in the DataRobot file system.

        Returns
        -------
        str:
            Validated file path without the protocol prefix.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> DataRobotFileSystem._strip_protocol("dr://12345/path/to/file.txt")
            '12345/path/to/file.txt'
            >>> DataRobotFileSystem._strip_protocol("dr://12345/path/")
            '12345/path/'
            >>> DataRobotFileSystem._strip_protocol("dr:///12345/")
            '12345/'
            >>> DataRobotFileSystem._strip_protocol("dr://")
            ''
        """
        path = stringify_path(path)
        protos = (cls.protocol,) if isinstance(cls.protocol, str) else cls.protocol
        for protocol in protos:
            if path.startswith(protocol + "://"):
                path = path[len(protocol) + 3 :]
            elif path.startswith(protocol + "::"):
                path = path[len(protocol) + 2 :]
        if path.endswith("/"):
            path = path.rstrip("/") + "/"  # Normalize trailing slashes (/) to max 1
        path = path.lstrip("/")  # No leading slashes
        # use of root_marker to make minimum required path
        return path or cls.root_marker

    def _split_path(self, path: str) -> Tuple[str, str]:
        """
        Split the given path into catalog ID and internal file path.
        Internal paths can be empty.

        Parameters
        ----------
        path:
            File path in the DataRobot file system.

        Returns
        -------
        Tuple[str, str]:
            A tuple of catalog ID and the internal file path.

        Raises
        ------
        ValueError
            If the path format is invalid.

        Examples
        --------
        .. code-block:: python

            >>> fs = DataRobotFileSystem()
            >>> fs._split_path("dr://12345/path/to/file.txt")
            ('12345', 'path/to/file.txt')
            >>> fs._split_path("dr:///12345/")
            ('12345', '')
            >>> fs._split_path("12345/folder/")
            ('12345', 'folder/')
        """
        path_without_protocol = self._strip_protocol(path)
        if not path_without_protocol:
            raise ValueError(
                f"Invalid path '{path}'. Expected format: '{self.protocol}://<catalog_id>/path/to/file.txt'"
            )
        parts = path_without_protocol.split("/", 1)
        catalog_id = parts[0]
        internal_path = parts[1] if len(parts) > 1 else ""
        return catalog_id, internal_path

    @contextmanager
    def _try_convert_to_fsspec_exception(self) -> Generator[None, None, None]:
        """Convert exceptions from DataRobot client to fsspec exceptions where possible."""
        try:
            yield
        except ClientError as exc:
            if exc.status_code in {HTTPStatus.NOT_FOUND, HTTPStatus.GONE}:
                raise FileNotFoundError(str(exc.json.get("message", exc.json))) from exc
            elif exc.status_code == HTTPStatus.FORBIDDEN:
                raise PermissionError(str(exc.json.get("message", exc.json))) from exc
            elif exc.status_code == HTTPStatus.CONFLICT:
                raise FileExistsError(str(exc.json.get("message", exc.json))) from exc
            elif exc.status_code in {
                HTTPStatus.BAD_REQUEST,
                HTTPStatus.UNPROCESSABLE_ENTITY,
            }:
                message = str(exc.json.get("message", exc.json))
                if "errors" in exc.json:
                    message += f" {exc.json.get('errors', '')}"
                raise ValueError(message) from exc
            raise
        except AsyncProcessUnsuccessfulError as exc:
            if "Duplicate file name" in str(exc):
                raise FileExistsError(str(exc)) from exc
            raise

    @contextmanager
    def _swallow_not_found_errors(self) -> Generator[None, None, None]:
        """Silently ignore file not found and already deleted errors."""
        try:
            yield
        except ClientError as exc:
            if exc.status_code not in {HTTPStatus.NOT_FOUND, HTTPStatus.GONE}:
                raise
        except FileNotFoundError:
            pass

    def _format_path_details_for_files(
        self, catalog_id: str, files: List[File], show_details: bool
    ) -> Union[List[FileInfo], List[str]]:
        """Format path details for a list of files. Files can represent both files and directories."""
        if show_details:
            return [
                FileInfo(
                    name=f"{catalog_id}/{file.name}",
                    size=file.size,
                    type="directory" if file.type == "folder" else "file",
                    format=file.type if file.type != "folder" else None,
                    created_at=file.created_at,
                )
                for file in files
            ]

        return [f"{catalog_id}/{file.name}" for file in files]

    def _format_path_details_for_catalog_items(
        self, catalog_items: List[FilesCatalogSearch], show_details: bool
    ) -> Union[List[FileInfo], List[str]]:
        """Format path details for a list of catalog items. Catalog items are treated as top-level directories."""
        if show_details:
            return [
                FileInfo(
                    name=f"{item.id}/",
                    size=0,
                    type="directory",
                    format=None,
                    created_at=None,
                )
                for item in catalog_items
            ]
        return [f"{item.id}/" for item in catalog_items]

    def _get_files_wrapper_for_folder_id(self, catalog_id: str) -> Files:
        return Files(catalog_id, "", "", [], datetime.now(), "")

    def _remove_extra_paths_in_recursive_calls(self, paths1: List[str], paths2: List[str]) -> List[Tuple[str, str]]:
        """
        Removes extra paths in recursive calls to avoid duplication when targeting directories and files inside the
        same directory. This commonly occurs when invoking `expand_path` with `recursive=True`, as it returns paths
        for both directories and files. Assumes length of `paths1` and `paths2` are the same.

        This method tracks the source and target paths for the calls and removes both in the zipped list of paths
        returned.
        Returns paths in a sorted order by the source path.
        """
        paths = sorted(list(zip(paths1, paths2)), key=lambda x: x[0])
        deduped_paths = []
        parent_dirs: Set[str] = set()
        for p1, p2 in paths:
            current = p1.rstrip("/")
            while current != self.root_marker and f"{current}/" not in parent_dirs:
                current = self._parent(current)

            if current == self.root_marker:
                if p1.endswith("/"):
                    parent_dirs.add(p1)
                deduped_paths.append((p1, p2))
        return deduped_paths

    @overload
    def ls(self, path: str, detail: Literal[False], **kwargs: Any) -> List[str]: ...

    @overload
    def ls(self, path: str, detail: Literal[True], **kwargs: Any) -> List[FileInfo]: ...

    def ls(self, path: str, detail: bool = True, **kwargs: Any) -> Union[List[FileInfo], List[str]]:
        """
        List files and folders at the given directory path. Use
        :meth:`info() <datarobot.fs.file_system.DataRobotFileSystem.info>` for information about
        a specific file.

        If ``detail`` is True, returns a list of dictionaries with file details including name (path), size and type.
        If ``detail`` is False, returns a list of file and folder paths as strings.

        Parameters
        ----------
        path:
            Path in the DataRobot file system to list.
        detail:
            Whether to return detailed information.
        kwargs:
            Additional keyword arguments for future proofing.

        Other Parameters
        ----------------
        version_id: str
            Version ID of the catalog item to target. If not provided, the latest version is used.

        Returns
        -------
        paths: List[FileInfo] or List[str]
            List of dicts with file and folder details if `detail` is True, otherwise list of paths.

        Raises
        ------
        FileNotFoundError
            If the specified path does not exist.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> fs.ls("dr://", detail=False)
            ['696935d6d5a04a752419cf6d/', 'abcdef1234567890abcdef12/']
            >>> fs.ls("dr://696935d6d5a04a752419cf6d/finance/")
            [
                {
                    'name': '696935d6d5a04a752419cf6d/finance/fy-2024/',
                    'size': 0,
                    'type': 'directory',
                    'format': None
                },
                {
                    'name': '696935d6d5a04a752419cf6d/finance/employee-list.csv',
                    'size': 2048,
                    'type': 'file',
                    'format': 'csv'
                },
            ]

        See also
        --------
        :meth:`info() <datarobot.fs.file_system.DataRobotFileSystem.info>`

        :meth:`exists() <datarobot.fs.file_system.DataRobotFileSystem.exists>`
        """
        if self.unstrip_protocol(path) == f"{self.protocol}://":
            with self._try_convert_to_fsspec_exception():
                catalog_items = Files.search_catalog(limit=0)
            return self._format_path_details_for_catalog_items(catalog_items, detail)

        catalog_id, internal_path = self._split_path(path)
        prefix = f"{internal_path.rstrip('/')}/" if internal_path else None
        with self._try_convert_to_fsspec_exception():
            files = self._get_files_wrapper_for_folder_id(catalog_id).list_contained_files(
                limit=0,
                recursive=False,
                prefix=prefix,
                version_id=kwargs.get("version_id"),
            )
        path_details = self._format_path_details_for_files(catalog_id, files, detail)

        if internal_path and path_details == []:
            raise FileNotFoundError(f"No directory found at {path}")
        return path_details

    def info(self, path: str, **kwargs: Any) -> FileInfo:
        """
        Get details about a file or directory.

        For info about a directory path append a forward slash (/) at the end of the path.
        Paths without a trailing slash can return info about files or directories. If both
        a file and directory share the same path, the file info is returned.

        Parameters
        ----------
        path:
            Path in the DataRobot file system to get information about.
        version_id:
            Optional version ID of the catalog item to target. If not provided, the latest version is used.
        kwargs:
            Additional keyword arguments passed to
            :meth:`ls() <datarobot.fs.file_system.DataRobotFileSystem.ls>`.

        Returns
        -------
        info: :class:`FileInfo <datarobot.fs.file_system.FileInfo>`
            A dictionary with file or directory details including name (path), size and type.

        Raises
        ------
        FileNotFoundError
            If the specified path does not exist.
        ValueError
            If the path is invalid. Root path is not allowed.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> fs.info("dr://696935d6d5a04a752419cf6d/finance/employee-list.csv")
            {
                'name': '696935d6d5a04a752419cf6d/finance/employee-list.csv',
                'size': 2048,
                'type': 'file',
                'format': 'csv',
                'created_at': datetime.datetime(2026, 3, 6, 10, 5, 16, 805655)
            }
            >>> fs.info("dr://696935d6d5a04a752419cf6d/finance/")
            {
                'name': '696935d6d5a04a752419cf6d/finance/',
                'size': 0,
                'type': 'directory',
                'format': None,
                'created_at': None
            }
            >>> fs.info("dr://696935d6d5a04a752419cf6d/my_folder")
            {
                'name': '696935d6d5a04a752419cf6d/my_folder/',
                'size': 0,
                'type': 'directory',
                'format': None,
                'created_at': None
            }
        """
        self._split_path(path)  # Disallow info at root
        path_without_protocol = self._strip_protocol(path)
        out = self.ls(self._parent(path.rstrip("/")), detail=True, **kwargs)

        if path.endswith("/"):
            targets = [item for item in out if item["name"] == path_without_protocol and item["type"] == "directory"]
        else:
            targets = [item for item in out if item["name"].rstrip("/") == path_without_protocol.rstrip("/")]
            if len(targets) > 1:  # This should only ever be 2
                # Prefer files over directories for paths not ending with /
                targets = [item for item in targets if item["type"] == "file"]

        if targets:
            return targets[0]
        raise FileNotFoundError(f"No file or directory found at {path}")

    def created(self, path: str) -> datetime | None:
        """
        Return the created timestamp of a file as a :class:`datetime.datetime` object.

        Parameters
        ----------
        path:
            Path in the DataRobot file system to get information about.

        Returns
        -------
        datetime.datetime or None
            The timestamp of when the file was created or None if a directory.

        Raises
        ------
        FileNotFoundError
            If the specified path does not exist.
        ValueError
            If the path is invalid. Root path is not allowed.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> fs.created("dr://696935d6d5a04a752419cf6d/finance/employee-list.csv")
            datetime.datetime(2026, 3, 6, 10, 5, 16, 805655)
        """
        out = self.info(path)
        return out["created_at"]

    @overload
    def du(
        self,
        path: str,
        total: Literal[True] = ...,
        maxdepth: Optional[int] = ...,
        withdirs: bool = ...,
        **kwargs: Any,
    ) -> int: ...

    @overload
    def du(
        self,
        path: str,
        total: Literal[False] = ...,
        maxdepth: Optional[int] = ...,
        withdirs: bool = ...,
        **kwargs: Any,
    ) -> Dict[str, int]: ...

    def du(
        self,
        path: str,
        total: bool = True,
        maxdepth: Optional[int] = None,
        withdirs: bool = False,
        **kwargs: Any,
    ) -> Union[int, Dict[str, int]]:
        """
        Retrieve space used by files and optionally directories at a path.

        Notes
        -----
        Directory size does not include the size of its contents and is set to zero.

        Parameters
        ----------
        path:
            The path to retrieve file space usage for.
        total:
            Whether to sum all file sizes.
        maxdepth:
            Maximum number of directory levels to descend when searching for files. Use ``None`` for unlimited.
        withdirs:
            Whether to include directory paths in the output.
        kwargs:
            Additional keyword arguments passed to
            :meth:`find() <datarobot.fs.file_system.DataRobotFileSystem.find>`.

        Returns
        -------
        int or Dict[str, int]
            If `total` is True, the number of bytes of all files in the path.
            If `total` is False, a dictionary mapping paths to their size.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()

            >>> fs.du("dr://696935d6d5a04a752419cf6d/finance/yellow.txt")
            2048

            >>> fs.du("dr://696935d6d5a04a752419cf6d/", total=False)
            {'696935d6d5a04a752419cf6d/file.txt': 102, '696935d6d5a04a752419cf6d/finance/yellow.txt': 2048}

            >>> fs.du("dr://696935d6d5a04a752419cf6d/", total=False, maxdepth=1, withdirs=True)
            {'696935d6d5a04a752419cf6d/file.txt': 102, '696935d6d5a04a752419cf6d/finance/': 0}
        """
        return cast(
            Union[int, Dict[str, int]],
            super().du(path, total=total, maxdepth=maxdepth, withdirs=withdirs, **kwargs),
        )

    @overload
    def find(
        self,
        path: str,
        maxdepth: Optional[int] = None,
        withdirs: bool = False,
        detail: Literal[False] = ...,
        **kwargs: Any,
    ) -> List[str]: ...

    @overload
    def find(
        self,
        path: str,
        maxdepth: Optional[int] = None,
        withdirs: bool = False,
        detail: Literal[True] = ...,
        **kwargs: Any,
    ) -> Dict[str, FileInfo]: ...

    # SPDX-FileCopyrightText: 2018 Martin Durant
    # SPDX-License-Identifier: BSD-3-Clause
    # The following method is derived from fsspec (https://github.com/fsspec/filesystem_spec)
    def find(
        self,
        path: str,
        maxdepth: Optional[int] = None,
        withdirs: bool = False,
        detail: bool = False,
        **kwargs: Any,
    ) -> Union[List[str], Dict[str, FileInfo]]:
        """List all files below path. If `withdirs` is True, include directories as well.

        Like posix ``find`` command without conditions

        Parameters
        ----------
        path:
            The path to search from. Note that unlike the glob method, this method does not support glob patterns and
            treats the path as a literal directory path to search under or a filename to match.
        maxdepth:
            If not None, the maximum number of levels to descend
        withdirs:
            Whether to include directory paths in the output.
        kwargs:
            Passed to :meth:`ls <datarobot.fs.file_system.DataRobotFileSystem.walk>`

        Returns
        -------
        List[str] or Dict[str, Dict[str, FileInfo]]
            If `detail` is False, a list of file (and optionally directory) paths.
            If `detail` is True, a dictionary mapping paths to their info dictionaries.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> fs.find("dr://696935d6d5a04a752419cf6d/", withdirs=True)
            [
                '696935d6d5a04a752419cf6d/',
                '696935d6d5a04a752419cf6d/finance/',
                '696935d6d5a04a752419cf6d/finance/budgets/',
                '696935d6d5a04a752419cf6d/finance/budgets/Q2_budget_2024.pdf',
                '696935d6d5a04a752419cf6d/finance/employee-list.csv'
            ]

            >>> fs.find("dr://696935d6d5a04a752419cf6d/finance/", maxdepth=1)
            ['696935d6d5a04a752419cf6d/finance/employee-list.csv']

            >>> fs.find("dr://696935d6d5a04a752419cf6d/finance", maxdepth=1, withdirs=True, detail=True)
            {
                '696935d6d5a04a752419cf6d/finance/': {
                    'name': '696935d6d5a04a752419cf6d/finance/',
                    'size': 0,
                    'type': 'directory',
                    'format': None,
                    'created_at': None
                },
                '696935d6d5a04a752419cf6d/finance/employee-list.csv': {
                    'name': '696935d6d5a04a752419cf6d/finance/employee-list.csv',
                    'size': 2048,
                    'type': 'file',
                    'format': 'csv',
                    'created_at': datetime.datetime(2026, 3, 6, 10, 5, 16, 805655)
                },
                '696935d6d5a04a752419cf6d/finance/budgets/': {
                    'name': '696935d6d5a04a752419cf6d/finance/budgets/',
                    'size': 0,
                    'type': 'directory',
                    'format': None,
                    'created_at': None
                },
            }
        """
        # This is a copy of of AbstractFileSystem.find() method with slight modification
        path = self._strip_protocol(path)
        out: Dict[str, Any] = {}

        # Add the root directory if withdirs is requested
        # This is needed for posix glob compliance
        if withdirs and path != "" and self.isdir(path):
            path_info = self.info(path)
            out[path_info["name"]] = path_info

        for _, dirs, files in self.walk(path, maxdepth, detail=True, **kwargs):
            if withdirs:
                out.update({info["name"]: info for _, info in dirs.items()})
            out.update({info["name"]: info for _, info in files.items()})
        if not out and self.isfile(path):
            # walk works on directories, but find should also return [path]
            # when path happens to be a file
            if detail:
                out[path] = self.info(path)
            else:
                out[path] = {}
        names = sorted(out)
        if not detail:
            return names
        else:
            return {name: out[name] for name in names}

    @overload
    def glob(
        self,
        path: str,
        maxdepth: Optional[int] = None,
        detail: Literal[False] = ...,
        **kwargs: Any,
    ) -> List[str]: ...

    @overload
    def glob(
        self,
        path: str,
        maxdepth: Optional[int] = None,
        detail: Literal[True] = ...,
        **kwargs: Any,
    ) -> Dict[str, FileInfo]: ...

    # SPDX-FileCopyrightText: 2018 Martin Durant
    # SPDX-License-Identifier: BSD-3-Clause
    # The following method is derived from fsspec (https://github.com/fsspec/filesystem_spec)
    def glob(
        self,
        path: str,
        maxdepth: Optional[int] = None,
        detail: bool = False,
        **kwargs: Any,
    ) -> Union[List[str], Dict[str, FileInfo]]:
        """
        Find files by glob-matching.

        Pattern matching capabilities for finding files that match the given pattern.

        Parameters
        ----------
        path:
            The glob pattern to match against.
        maxdepth:
            Maximum depth for '\*\*' patterns. Applied on the first '\*\*' found.
            Must be at least 1 if provided.
        detail:
            Whether to return detailed information.
        kwargs:
            Additional arguments passed to ``find``.

        Returns
        -------
        List[str] or Dict[str, FileInfo]
            If `detail` is False, a list of file and directory paths.
            If `detail` is True, a dictionary mapping paths to their info dictionaries.

        Notes
        -----
        Supported patterns:

        - '\*': Matches any sequence of characters within a single directory level
        - '\*\*': Matches any number of directory levels (must be an entire path component)
        - '?': Matches exactly one character
        - '[:spelling:ignore:`abc`]': Matches any character in the set
        - '[a-z]': Matches any character in the range
        - '[!cat]': Matches any character NOT in the set {c, a, t}

        Special behaviors:

        - If the path ends with '/', only folders are returned
        - Consecutive '\*' characters are compressed into a single '\*'
        - Empty brackets '[]' never match anything
        - Negated empty brackets '[!]' match any single character
        - Special characters in character classes are escaped properly

        Limitations:

        - '\*\*' must be a complete path component (e.g., 'a/\*\*/b', not 'a\*\*b')
        - No brace expansion ('{a, b}.txt')
        - No extended glob patterns ('+(pattern)', '!(pattern)')

        See Also
        --------
        :meth:`find() <datarobot.fs.file_system.DataRobotFileSystem.find>`

        Examples
        --------
        Find all files and directories directly under the specified path.

        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> fs.glob("dr://696935d6d5a04a752419cf6d/finance/*", detail=False)
            [
                '696935d6d5a04a752419cf6d/finance/budgets/',
                '696935d6d5a04a752419cf6d/finance/employee-list.csv'
            ]

        Find only directories directly under the specified path.

        .. code-block:: python

            >>> fs.glob("dr://696935d6d5a04a752419cf6d/finance/*/", detail=False)
            ['696935d6d5a04a752419cf6d/finance/budgets/']

        Find any budget directories with a 4-digit year in their name.

        .. code-block:: python

            >>> fs.glob("dr://696935d6d5a04a752419cf6d/finance/budgets/*-202[0-9]/", detail=False)
            [
                '696935d6d5a04a752419cf6d/finance/budgets/fy-2024/',
                '696935d6d5a04a752419cf6d/finance/budgets/fy-2023/'
            ]

        Find all .csv files at a maximum depth of 2 levels.

        .. code-block:: python

            >>> fs.glob("dr://696935d6d5a04a752419cf6d/**/*.csv", maxdepth=2, detail=False)
            [
                '696935d6d5a04a752419cf6d/finance/employee-list.csv',
                '696935d6d5a04a752419cf6d/sales/data.csv'
            ]
        """
        # This is a copy of AbstractFileSystem.glob() method with slight modification
        if maxdepth is not None and maxdepth < 1:
            raise ValueError("maxdepth must be at least 1")

        import re

        seps = (os.path.sep, os.path.altsep) if os.path.altsep else (os.path.sep,)
        ends_with_sep = path.endswith(seps)
        path = self._strip_protocol(path)
        append_slash_to_dirname = ends_with_sep or path.endswith(tuple(sep + "**" for sep in seps))
        idx_star = path.find("*") if path.find("*") >= 0 else len(path)
        idx_qmark = path.find("?") if path.find("?") >= 0 else len(path)
        idx_brace = path.find("[") if path.find("[") >= 0 else len(path)

        min_idx = min(idx_star, idx_qmark, idx_brace)

        if not has_magic(path):
            if self.exists(path, **kwargs):
                if not detail:
                    return [path]
                else:
                    return {path: self.info(path, **kwargs)}
            elif not detail:
                return []  # glob of non-existent returns empty
            else:
                return {}
        elif "/" in path[:min_idx]:
            min_idx = path[:min_idx].rindex("/")
            root = path[: min_idx + 1]
            depth = path[min_idx + 1 :].count("/") + 1
        else:
            root = ""
            depth = path[min_idx + 1 :].count("/") + 1

        if "**" in path:
            if maxdepth is not None:
                idx_double_stars = path.find("**")
                depth_double_stars = path[idx_double_stars:].count("/") + 1
                depth = depth - depth_double_stars + maxdepth
            else:
                depth = None  # type: ignore[assignment]

        allpaths = self.find(root, maxdepth=depth, withdirs=True, detail=True, **kwargs)

        pattern = glob_translate(path + ("/" if ends_with_sep else ""))
        pattern = re.compile(pattern)

        def _has_pattern_match(path: str, info: FileInfo) -> Optional[Match[str]]:
            """
            Check whether the given path matches the glob pattern.
            Accounts for directory paths modifications required.
            """
            if info["type"] != "directory":
                return pattern.match(path)
            if append_slash_to_dirname:
                return pattern.match(path + "/")
            return pattern.match(path.rstrip("/"))

        out = {p: info for p, info in sorted(allpaths.items()) if _has_pattern_match(p, info)}
        if detail:
            return out
        else:
            return list(out)

    # SPDX-FileCopyrightText: 2018 Martin Durant
    # SPDX-License-Identifier: BSD-3-Clause
    # The following method is derived from fsspec (https://github.com/fsspec/filesystem_spec)
    def tree(
        self,
        path: str = "",
        recursion_limit: int = 2,
        max_display: int = 25,
        display_size: bool = False,
        prefix: str = "",
        is_last: bool = True,
        first: bool = True,
        indent_size: int = 4,
    ) -> str:
        """
        Return a tree-like structure string of the DataRobot file system from the given path.

        Parameters
        ----------
        path:
            Path in the DataRobot file system to display the tree from.
        recursion_limit:
            Maximum depth of directory traversal.
        max_display:
            Maximum number of items to display per directory.
        display_size:
            Whether to display file sizes.
        prefix:
            Current line prefix for visual tree structure.
        is_last:
            Whether the current item is last in its level.
        first:
            Whether this is the first call (displays root path).
        indent_size:
            Number of spaces by indent.

        Returns
        -------
        tree_str: str
            A string representing the tree structure of the file system.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> print(fs.tree("dr://696935d6d5a04a752419cf6d/", recursion_limit=5))
            696935d6d5a04a752419cf6d/
            └── finance/
                ├── fy-2024/
                │   └── budgets/
                │       └── Q2_budget_2024.pdf
                └── employee-list.csv

        See also
        --------
        :meth:`walk() <datarobot.fs.file_system.DataRobotFileSystem.walk>`
        """

        # This is a copy of AbstractFileSystem.tree() with slight modification
        def format_bytes(n: int) -> str:
            """Format bytes as text."""
            for pref, k in (
                ("P", 2**50),
                ("T", 2**40),
                ("G", 2**30),
                ("M", 2**20),
                ("k", 2**10),
            ):
                if n >= 0.9 * k:
                    return f"{n / k:.2f} {pref}b"
            return f"{n}B"

        result = []

        if first:
            if self.unstrip_protocol(path) == f"{self.protocol}://":
                result.append("")
            else:
                path_info = self.info(path)
                result.append(path_info["name"])  # Tweak top-level to use info name

        if recursion_limit:
            indent = " " * indent_size
            contents = self.ls(path, detail=True)
            contents.sort(key=lambda x: (x.get("type") != "directory", x.get("name", "")))

            if max_display is not None and len(contents) > max_display:
                displayed_contents = contents[:max_display]
                remaining_count = len(contents) - max_display
            else:
                displayed_contents = contents
                remaining_count = 0

            for i, item in enumerate(displayed_contents):
                is_last_item = (i == len(displayed_contents) - 1) and (remaining_count == 0)

                branch = "└" + ("─" * (indent_size - 2)) if is_last_item else "├" + ("─" * (indent_size - 2))
                branch += " "
                new_prefix = prefix + (indent if is_last_item else "│" + " " * (indent_size - 1))

                # Tweak name to handle trailing slashes for directories
                if item["type"] == "directory":
                    name = os.path.basename(item.get("name", "").rstrip("/")) + "/"
                else:
                    name = os.path.basename(item.get("name", ""))

                if display_size and item.get("type") == "directory":
                    sub_contents = self.ls(item.get("name", ""), detail=True)
                    num_files = sum(1 for sub_item in sub_contents if sub_item.get("type") == "file")
                    num_folders = sum(1 for sub_item in sub_contents if sub_item.get("type") == "directory")

                    if num_files == 0 and num_folders == 0:
                        size = " (empty folder)"
                    elif num_files == 0:
                        size = f" ({num_folders} subfolder{'s' if num_folders > 1 else ''})"
                    elif num_folders == 0:
                        size = f" ({num_files} file{'s' if num_files > 1 else ''})"
                    else:
                        suffix = "s" if num_folders > 1 else ""
                        size = f" ({num_files} file{'s' if num_files > 1 else ''}, {num_folders} subfolder{suffix})"
                elif display_size and item.get("type") == "file":
                    size = f" ({format_bytes(item.get('size', 0))})"
                else:
                    size = ""

                result.append(f"{prefix}{branch}{name}{size}")

                if item.get("type") == "directory" and recursion_limit > 0:
                    result.append(
                        self.tree(
                            path=item.get("name", ""),
                            recursion_limit=recursion_limit - 1,
                            max_display=max_display,
                            display_size=display_size,
                            prefix=new_prefix,
                            is_last=is_last_item,
                            first=False,
                            indent_size=indent_size,
                        )
                    )

            if remaining_count > 0:
                more_message = f"{remaining_count} more item(s) not displayed."
                result.append(f"{prefix}{'└' + ('─' * (indent_size - 2))} {more_message}")

        return "\n".join(_ for _ in result if _)

    def cat_file(
        self,
        path: str,
        start: Optional[int] = None,
        end: Optional[int] = None,
        **kwargs: Any,
    ) -> bytes:
        """
        Fetch a single file's contents.

        Parameters
        ----------
        path:
            File path in the DataRobot file system to read.
        start:
            Optional starting byte position to read from. If negative, counts from the end of the file.
        end:
            Optional ending byte position to read to. If negative, counts from the end of the file.
        kwargs:
            Keyword arguments passed to :meth:`DataRobotFileSystem.open()
            <datarobot.fs.file_system.DataRobotFileSystem.open>`.

        Returns
        -------
        bytes:
            The contents of the file as bytes.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> fs.cat_file("dr://696935d6d5a04a752419cf6d/finance/report.txt")
            b'Q2 Financial Report...'

        Read a range of bytes from a file:

        .. code-block:: python

            >>> fs.cat_file("dr://696935d6d5a04a752419cf6d/finance/report.txt", start=10, end=20)
            b'Financial Report...'

        """
        return cast(bytes, super().cat_file(path, start=start, end=end, **kwargs))

    # SPDX-FileCopyrightText: 2018 Martin Durant
    # SPDX-License-Identifier: BSD-3-Clause
    # The following method is derived from fsspec (https://github.com/fsspec/filesystem_spec)
    def cat(
        self,
        path: Union[str, List[str]],
        recursive: bool = False,
        on_error: Union[Literal["raise"], Literal["omit"], Literal["return"]] = "raise",
        **kwargs: Any,
    ) -> Union[bytes, Dict[str, Union[bytes, Exception]]]:
        """
        Fetch (potentially multiple) path's contents.

        Parameters
        ----------
        path:
            File or directory path(s) in the DataRobot file system to read. Can include glob patterns.
        recursive:
            If True, assume the path(s) are directories, and get contents of all contained files.
        on_error:
            If raise, an underlying exception will be raised (converted to KeyError
            if the type is in self.missing_exceptions); if omit, keys with exception
            will simply not be included in the output; if "return", all keys are
            included in the output, but the value will be bytes or an exception
            instance.
        kwargs:
            Additional keyword arguments passed to :meth:`cat_file()
            <datarobot.fs.file_system.DataRobotFileSystem.cat_file>`.

        Returns
        -------
        bytes or Dict[str, bytes] or Dict[str, Union[bytes, Exception]]
            If a single file path is provided, returns the file contents as bytes. If multiple paths are
            provided or the path is otherwise expanded, returns a dictionary mapping each path to its
            contents as bytes or an exception instance if on_error is set to "return".

        Examples
        --------
        Read a single file:

        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> fs.cat("dr://696935d6d5a04a752419cf6d/finance/report.txt")
            b'Q2 Financial Report...'

        Read multiple files and all files in a directory:

        .. code-block:: python

            >>> fs.cat(
            ...     ["dr://696935d6d5a04a752419cf6d/finance/summary.txt", "dr://696935d6d5a04a752419cf6d/reports/"],
            ...     recursive=True
            ... )
            {
                '696935d6d5a04a752419cf6d/finance/summary.txt': b'Summary...',
                '696935d6d5a04a752419cf6d/reports/report_2024.txt': b'2024 Report...',
                '696935d6d5a04a752419cf6d/reports/report_2025.txt': b'2025 Report...'
            }

        Read all CSV files matching a glob pattern:

        .. code-block:: python

            >>> fs.cat("dr://696935d6d5a04a752419cf6d/data/**/*.csv")
            {
                '696935d6d5a04a752419cf6d/data/sales.csv': b'date,amount\\n2024-01-01,1000\\n...',
                '696935d6d5a04a752419cf6d/data/archive/old_sales.csv': b'date,amount\\n2023-01-01,950\\n...'
            }
        """
        # This is a modified version of AbstractFileSystem.cat()
        paths = [p for p in self.expand_path(path, recursive=recursive) if not p.endswith("/")]

        if len(paths) == 0:
            raise FileNotFoundError(
                f"No files found at path: {path}. Please verify if using a directory path that recursive "
                "is set to True."
            )
        elif len(paths) > 1 or isinstance(path, list) or paths[0] != self._strip_protocol(path):
            out: Dict[str, Union[bytes, Exception]] = {}
            for target in paths:
                try:
                    out[target] = self.cat_file(target, **kwargs)
                except Exception as e:
                    if on_error == "raise":
                        raise
                    if on_error == "return":
                        out[target] = e
            return out

        return self.cat_file(paths[0], **kwargs)

    def sign(
        self,
        path: str,
        expiration: int = 100,
        version_id: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """
        Create a signed URL for the given file path. Optionally specify a version ID to retrieve a
        signed URL for an earlier version of the file from that version of the catalog directory.

        Parameters
        ----------
        path:
            File path in the DataRobot file system to sign.
        expiration:
            Number of seconds until the signed URL expires.
        version_id:
            Version ID of the catalog directory to target. If not provided, the latest version is used.
        kwargs:
            Additional keyword arguments for future proofing.

        Returns
        -------
        str:
            A signed URL granting temporary access to the file.

        Raises
        ------
        FileNotFoundError
            If the specified file does not exist.
        IsADirectoryError
            If the specified path is a directory.
        ValueError
            If the path format is invalid.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> signed_url = fs.sign(
            ...     "dr://696935d6d5a04a752419cf6d/finance/budgets/Q2_budget_2024.pdf",
            ...     expiration=300,
            ... )
        """
        if self.isdir(path):
            raise IsADirectoryError("Cannot create signed URL for a directory. Please provide a file path.")

        catalog_id, internal_path = self._split_path(path)
        with self._try_convert_to_fsspec_exception():
            signed_urls = self._get_files_wrapper_for_folder_id(catalog_id).generate_signed_urls(
                file_names=[internal_path],
                duration=expiration,
                version_id=version_id,
            )
            return signed_urls[0]["url"]

    def cp_file(
        self,
        path1: str,
        path2: str,
        overwrite_strategy: FilesOverwriteStrategy = FilesOverwriteStrategy.RENAME,
        max_wait: int = DEFAULT_MAX_WAIT,
        wait_for_completion: bool = True,
        **kwargs: Any,
    ) -> None:
        """
        Copy a file or directory from `path1` to `path2`.

        Copies directories recursively. Specify an overwrite strategy to handle file naming conflicts
        at the target location. Note that copying between catalog item directories is an asynchronous operation.
        Cannot create a new catalog item directory by copying files into a non-existent catalog item directory.

        Parameters
        ----------
        path1:
            Source file or directory path. Directory paths should end with a forward slash (/).
        path2:
            Target file or directory path. Directory paths should end with a forward slash (/).
        overwrite_strategy:
            Strategy to handle naming conflicts at the target location.
        max_wait:
            Maximum time in seconds to wait for the copy operation to complete when copying between
            catalog items.
        wait_for_completion:
            Whether to wait for the copy operation to complete before returning when copying between
            catalog items.
        kwargs:
            Additional keyword arguments for future proofing.

        Raises
        ------
        FileNotFoundError:
            If the source path does not exist or either catalog item directory does not exist.
        ValueError:
            If attempting to copy a directory to a file path.
        FileExistsError:
            If the target file or directory already exists and overwrite strategy is set to ERROR.

        Examples
        --------
        Copy a file to a new file path:

        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> from datarobot.enums import FilesOverwriteStrategy
            >>> fs = DataRobotFileSystem()
            >>> fs.cp_file(
            ...     "dr://696935d6d5a04a752419cf6d/fy-2024/budgets/Q2_budget_2024.pdf",
            ...     "dr://69691fc3d5a04a752419cf5/fy-2024/budgets-copy.pdf",
            ... )

        Copy file into a directory, replace existing file if present:

        .. code-block:: python

            >>> fs.cp_file(
            ...     "dr://696935d6d5a04a752419cf6d/fy-2024/budgets/Q2_budget_2024.pdf",
            ...     "dr://69691fc3d5a04a752419cf5/fy-2024/budgets/",
            ...     overwrite_strategy=FilesOverwriteStrategy.OVERWRITE,
            ... )

        Copy the contents of a directory into another directory:

        .. code-block:: python

            >>> fs.cp_file(
            ...     "dr://696935d6d5a04a752419cf6d/fy-2024/budgets/",
            ...     "dr://69691fc3d5a04a752419cf5/archive/budgets-2024/",
            ... )

        See also
        --------
        :meth:`copy() <datarobot.fs.file_system.DataRobotFileSystem.copy>`
        """
        source_catalog_id, source_internal_path = self._split_path(path1)
        target_catalog_id, target_internal_path = self._split_path(path2)

        if not source_internal_path and not target_internal_path:
            raise ValueError("Cannot copy catalog item folder to another catalog item folder. Use clone() instead.")
        elif source_internal_path and not target_internal_path:
            # Handle edge case to copy file or folder into root of target catalog item
            target_internal_path = os.path.basename(source_internal_path.rstrip("/")) + (
                "/" if source_internal_path.endswith("/") else ""
            )

        with self._try_convert_to_fsspec_exception():
            if source_catalog_id == target_catalog_id:
                self._get_files_wrapper_for_folder_id(catalog_id=source_catalog_id).copy_within_container(
                    source_path=source_internal_path,
                    target_path=target_internal_path,
                    overwrite=overwrite_strategy,
                )
            else:
                self._get_files_wrapper_for_folder_id(catalog_id=source_catalog_id).copy(
                    source_path=source_internal_path,
                    target=target_internal_path,
                    target_files=self._get_files_wrapper_for_folder_id(catalog_id=target_catalog_id),
                    overwrite=overwrite_strategy,
                    max_wait=max_wait,
                    wait_for_completion=wait_for_completion,
                )

    def cp_directory(
        self,
        path1: str,
        path2: str,
        overwrite_strategy: FilesOverwriteStrategy = FilesOverwriteStrategy.RENAME,
        max_wait: int = DEFAULT_MAX_WAIT,
        wait_for_completion: bool = True,
        **kwargs: Any,
    ) -> None:
        """
        Copy a directory recursively from `path1` to `path2`.

        Validates that both paths are directories by checking for trailing slashes (/).
        Calls :meth:`cp_file() <datarobot.fs.file_system.DataRobotFileSystem.cp_file>` internally.

        Parameters
        ----------
        path1:
            Source directory path. Must end with a forward slash (/).
        path2:
            Target directory path. Must end with a forward slash (/).
        overwrite_strategy:
            Strategy to handle naming conflicts at the target location.
        max_wait:
            Maximum time in seconds to wait for the copy operation to complete when copying between
            catalog items.
        wait_for_completion:
            Whether to wait for the copy operation to complete before returning when copying between
            catalog items.
        kwargs:
            Additional keyword arguments passed to
            :meth:`cp_file() <datarobot.fs.file_system.DataRobotFileSystem.cp_file>`.

        See also
        --------
        :meth:`cp_file() <datarobot.fs.file_system.DataRobotFileSystem.cp_file>`
        """
        if not path1.endswith("/") or not path2.endswith("/"):
            raise ValueError("To copy a directory, source and target paths must end with '/'.")
        self.cp_file(
            path1,
            path2,
            overwrite_strategy=overwrite_strategy,
            max_wait=max_wait,
            wait_for_completion=wait_for_completion,
            **kwargs,
        )

    # SPDX-FileCopyrightText: 2018 Martin Durant
    # SPDX-License-Identifier: BSD-3-Clause
    # The following method is derived from fsspec (https://github.com/fsspec/filesystem_spec)
    def copy(
        self,
        path1: Union[str, List[str]],
        path2: Union[str, List[str]],
        recursive: bool = False,
        maxdepth: Optional[int] = None,
        on_error: Optional[Literal["raise", "ignore"]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Copy files or directories between two locations in the DataRobot file system.

        Parameters
        ----------
        path1:
            Source file or directory path(s). Supports glob pattern. If specifying a directory,
            recursive should be ``True``.
        path2:
            Target file or directory path(s).
        recursive:
            Whether to copy directory contents recursively.
        maxdepth:
            Maximum depth to recurse when finding files to copy.
        on_error:
            If ``"raise"``, any file not found exceptions will be raised. If ``"ignore"``, any file not found
            exceptions will be skipped and ignored. Defaults to ``"raise"`` unless recursive is ``True``, where
            the default is ``"ignore"``.
        kwargs:
            Additional keyword arguments passed to
            :meth:`cp_file() <datarobot.fs.file_system.DataRobotFileSystem.cp_file>`.

        Other Parameters
        ----------------
        overwrite_strategy: FilesOverwriteStrategy
            Strategy to handle naming conflicts at the target location. Passed to
            :meth:`cp_file() <datarobot.fs.file_system.DataRobotFileSystem.cp_file>`.

        Raises
        ------
        FileNotFoundError
            If any of the source paths do not exist or cannot find files and ``on_error`` is ``"raise"``.

        Examples
        --------
        Copy a single file to a new path:

        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> fs.copy(
            ...     "dr://696935d6d5a04a752419cf6d/finance/employee-list.csv",
            ...     "dr://696935d6d5a04a752419cf6d/finance/employee-list-backup.csv",
            ... )

        Copy more than one file or directory:

        .. code-block:: python

            >>> fs.copy(
            ...     [
            ...         "dr://696935d6d5a04a752419cf6d/finance/employee-list.csv",
            ...         "dr://696935d6d5a04a752419cf6d/finance/employee-list-copy.csv",
            ...     ],
            ...     [
            ...         "dr://696935d6d5a04a752419cf6d/finance/employee-list-copy.csv",
            ...         "dr://696935d6d5a04a752419cf6d/finance/employee-list-copy-2.csv",
            ...     ],
            ... )

        Copy a single file into a directory:

        .. code-block:: python

            >>> fs.copy(
            ...     "dr://696935d6d5a04a752419cf6d/finance/report.pdf",
            ...     "dr://696935d6d5a04a752419cf6d/archive/",
            ... )

        Recursively copy the contents of a directory to another directory:

        .. code-block:: python

            >>> fs.copy(
            ...     "dr://696935d6d5a04a752419cf6d/budgets/",
            ...     "dr://696935d6d5a04a752419cf6d/archive/budgets-2024/",
            ...     recursive=True,
            ... )

        Copy all CSV files in a directory and its subdirectories up to a maximum depth of 2:

        .. code-block:: python

            >>> fs.copy(
            ...     "dr://696935d6d5a04a752419cf6d/data/**/*.csv",
            ...     "dr://696935d6d5a04a752419cf6d/archive/data-2024/",
            ...     recursive=True,
            ...     maxdepth=2,
            ... )

        Copy all text files in a directory into a new directory:

        .. code-block:: python

            >>> fs.copy(
            ...     "dr://696935d6d5a04a752419cf6d/data/*.txt",
            ...     "dr://696935d6d5a04a752419cf6d/archive/",
            ...     recursive=True,
            ... )

        Copy a directory recursively, skipping files that already exist at the target:

        .. code-block:: python

            >>> from datarobot.enums import FilesOverwriteStrategy
            >>> fs.copy(
            ...     "dr://696935d6d5a04a752419cf6d/budgets/",
            ...     "dr://696935d6d5a04a752419cf6d/archive/",
            ...     recursive=True,
            ...     overwrite_strategy=FilesOverwriteStrategy.SKIP,
            ... )
        """
        if on_error is None and recursive:
            on_error = "ignore"
        elif on_error is None:
            on_error = "raise"

        if isinstance(path1, list) and isinstance(path2, list):
            # No need to expand paths when both source and destination
            # are provided as lists
            paths1 = path1
            paths2 = path2
            cp_paths: Iterable[Tuple[str, str]] = zip(paths1, paths2)
        else:
            source_is_str = isinstance(path1, str)
            paths1 = self.expand_path(path1, recursive=recursive, maxdepth=maxdepth)

            # Non-recursive or limited depth only copy over files
            copy_only_files = not recursive or maxdepth is not None
            if copy_only_files:
                paths1 = [p for p in paths1 if not (trailing_sep(p) or self.isdir(p))]
                if not paths1:
                    if on_error == "raise":
                        error_path = path1 if source_is_str else ",".join(path1)
                        raise FileNotFoundError(
                            f"No files found for path(s): {error_path}. Please verify if using a directory path that "
                            "recursive is set to True."
                        )
                    return

            source_is_file = len(paths1) == 1
            dest_is_dir = isinstance(path2, str) and (trailing_sep(path2) or self.isdir(path2))

            if isinstance(path1, str):
                exists = (
                    (has_magic(path1) and source_is_file)
                    or (not has_magic(path1) and dest_is_dir and not trailing_sep(path1))
                    or (not has_magic(path1) and dest_is_dir and source_is_file and not trailing_sep(paths1[0]))
                )
            else:
                exists = False

            paths2 = self._map_paths_to_destinations(
                paths1,
                path2,
                exists=exists,
                flatten=not source_is_str,
            )
            cp_paths = (
                zip(paths1, paths2) if copy_only_files else self._remove_extra_paths_in_recursive_calls(paths1, paths2)
            )

        for p1, p2 in cp_paths:
            try:
                self.cp_file(p1, p2, **kwargs)
            except FileNotFoundError:
                if on_error == "raise":
                    raise

    def _rm(self, path: Union[str, List[str]], **kwargs: Any) -> None:
        """
        Prefer use :meth:`rm_file() <datarobot.fs.file_system.DataRobotFileSystem.rm_file>`.
        Implemented for backwards compatibility.

        Splits paths to target files/folders within catalog items or entire catalog items for deletion.
        All paths are deleted recursively.

        Parameters
        ----------
        path:
            Path(s) of the file(s) or folder(s) to delete.
        kwargs:
            Additional keyword arguments for future proofing.
        """
        paths = [path] if isinstance(path, str) else path

        paths_to_delete_per_catalog_id: Dict[str, Set[str]] = defaultdict(set)
        catalog_items_to_delete: Set[str] = set()
        for catalog_id, internal_path in (self._split_path(p) for p in paths):
            if internal_path:
                paths_to_delete_per_catalog_id[catalog_id].add(internal_path)
            else:
                catalog_items_to_delete.add(catalog_id)

        with self._try_convert_to_fsspec_exception():
            for catalog_id in catalog_items_to_delete:
                with self._swallow_not_found_errors():
                    Files.delete(catalog_id)
            for catalog_id, internal_paths in paths_to_delete_per_catalog_id.items():
                if catalog_id in catalog_items_to_delete:
                    continue  # Already deleted entire catalog item
                with self._swallow_not_found_errors():
                    self._get_files_wrapper_for_folder_id(catalog_id).delete_files(list(internal_paths))

    def rm_file(self, path: Union[str, List[str]], **kwargs: Any) -> None:
        """
        Delete a file or directory at the given path(s). Completes silently if the file does not exist.

        Parameters
        ----------
        path:
            Path(s) of the file(s) to delete. Paths ending with a forward slash (/) are treated
            as directories and deleted recursively.
        kwargs:
            Additional keyword arguments for future proofing.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> fs.rm_file("dr://696935d6d5a04a752419cf6d/finance/employee-list.csv")

            >>> fs.rm_file([
            ...     "dr://696935d6d5a04a752419cf6d/finance/employee-list.csv",
            ...     "dr://696935d6d5a04a752419cf6d/finance/fy-2024/budgets/Q2_budget_2024.pdf"
            ... ])
        """
        self._rm(path, **kwargs)

    def rm_directory(self, path: Union[str, List[str]], **kwargs: Any) -> None:
        """
        Recursively delete a directory at the given path(s). Completes silently if the directory does not exist.
        Uses :meth:`rm_file() <datarobot.fs.file_system.DataRobotFileSystem.rm_file>` internally.

        Soft-deletes catalog item directory when requested. Use :meth:`Files.un_delete()
        <datarobot.models.files.Files.un_delete>` if you need to restore a deleted catalog item.

        Parameters
        ----------
        path:
            One or more directory paths to delete recursively. Paths must end with a forward slash (/) to be treated
            as directories and deleted recursively.
        kwargs:
            Additional keyword arguments for future proofing.

        Raises
        ------
        ValueError:
            If any of the provided paths do not end with a forward slash (/).

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> fs.rm_directory("dr://696935d6d5a04a752419cf6d/finance/fy-2024/")

            >>> fs.rm_directory([
            ...     "dr://696935d6d5a04a752419cf6d/finance/fy-2024/",
            ...     "dr://696935d6d5a04a752419cf6d/"
            ... ])
        """
        path = [path] if isinstance(path, str) else path
        if not all(p.endswith("/") for p in path):
            raise ValueError("Paths must end with a forward slash '/' to recursively delete directories.")

        self.rm_file(path, **kwargs)

    def rm(
        self,
        path: Union[str, List[str]],
        recursive: bool = False,
        maxdepth: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        """
        Delete files or directories. Completes silently if the file or directory does not exist.

        Soft-deletes catalog item directory when requested. Use :meth:`Files.un_delete()
        <datarobot.models.files.Files.un_delete>` if you need to restore a deleted catalog item.
        If all files in a directory are deleted, the directory itself is also deleted implicitly
        as DataRobot file system does not support empty directories.

        Parameters
        ----------
        path:
            One or more file or directory paths to delete. Paths ending with a forward slash (/)
            are treated as directories.
        recursive:
            Whether to recurse into directories when targeting files to delete. If `False` only deletes files
            targeted.
        maxdepth:
            Depth to pass to :meth:`find() <datarobot.fs.file_system.DataRobotFileSystem.find>`
            and :meth:`glob() <datarobot.fs.file_system.DataRobotFileSystem.glob>` when targeting
            files for deletion. Used to limit recursion in directories when finding files to delete.
            If `None`, no limit is applied.
        kwargs:
            Additional keyword arguments for future proofing. Passed to :meth:`rm_file()
            <datarobot.fs.file_system.DataRobotFileSystem.rm_file>`.

        Examples
        --------
        Delete file:

        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> fs.rm("dr://696935d6d5a04a752419cf6d/finance/employee-list.csv")

        Delete directory recursively:

        .. code-block:: python

            >>> fs.rm("dr://696935d6d5a04a752419cf6d/finance/fy-2024/", recursive=True)

        Delete contents of catalog item folder recursively up to a maximum depth of 2:

        .. code-block:: python

            >>> fs.rm("dr://696935d6d5a04a752419cf6d/", recursive=True, maxdepth=2)

        Delete catalog item folder:

        .. code-block:: python

            >>> fs.rm("dr://696935d6d5a04a752419cf6d/")

        Delete .csv files in a directory and its subdirectories up to a maximum depth of 3:

        .. code-block:: python

            >>> fs.rm("dr://696935d6d5a04a752419cf6d/finance/**/*.csv", recursive=True, maxdepth=3)

        """
        path = [path] if isinstance(path, (str, os.PathLike)) else path

        out: List[FileInfo] = []
        for p in path:
            with self._swallow_not_found_errors():
                if has_magic(p):
                    out += self.glob(p, maxdepth=maxdepth, detail=True, **kwargs).values()
                elif recursive and maxdepth is not None:
                    out += self.find(p, maxdepth=maxdepth, withdirs=False, detail=True, **kwargs).values()
                else:
                    out.append(self.info(p, **kwargs))

        # Filter to just files if non recursive or maxdepth is set (prevents glob from targeting directories)
        if not recursive or maxdepth is not None:
            out = [item for item in out if item["type"] == "file"]

        self.rm_file([item["name"] for item in out], **kwargs)

    def create_catalog_item_dir(self, **kwargs: Any) -> str:
        """
        Create a new empty catalog item directory and return its id.

        Parameters
        ----------
        kwargs:
            Additional keyword arguments for future proofing.

        Returns
        -------
        str:
            The id of the newly created catalog item.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> catalog_id = fs.create_catalog_item_dir()
            >>> fs.ls(f"dr://{catalog_id}/")
            []
        """
        with self._try_convert_to_fsspec_exception():
            return Files.create_empty_catalog_item_dir().id

    def mv_file(
        self,
        path1: str,
        path2: str,
        *,
        overwrite_strategy: FilesOverwriteStrategy = FilesOverwriteStrategy.REPLACE,
        **kwargs: Any,
    ) -> None:
        """
        Move a single file or directory from path1 to path2.

        Parameters
        ----------
        path1:
            Source path. Format: ``dr://<catalog_id>/path``. Directories should end with /.
        path2:
            Destination path. Format: ``dr://<catalog_id>/path``. Directories should end with /.
        overwrite_strategy:
            Strategy for overwriting existing paths. Defaults to REPLACE, inline with fsspec.
        kwargs:
            Additional keyword arguments passed to :meth:`cp_file()
            <datarobot.fs.file_system.DataRobotFileSystem.cp_file>` and
            :meth:`rm_file() <datarobot.fs.file_system.DataRobotFileSystem.rm_file>`
            when moving across catalogs.
        """
        if self._strip_protocol(path1) == self._strip_protocol(path2):
            return
        source_catalog_id, source_internal = self._split_path(path1)
        target_catalog_id, target_internal = self._split_path(path2)
        if not source_internal and not target_internal:
            raise ValueError("Cannot move catalog root to another catalog root. Use clone_catalog_item_dir() instead.")
        elif not source_internal and target_internal:
            raise ValueError(
                "Cannot move catalog root into a subpath. Use clone_catalog_item_dir() to clone the catalog."
            )
        elif source_internal and not target_internal:
            target_internal = os.path.basename(source_internal.rstrip("/")) + (
                "/" if source_internal.endswith("/") else ""
            )
        if source_catalog_id != target_catalog_id:
            path2_resolved = f"{self.protocol}://{target_catalog_id}/{target_internal}"
            self.cp_file(path1, path2_resolved, overwrite_strategy=overwrite_strategy, **kwargs)
            self.rm_file(path1, **kwargs)
            return
        with self._try_convert_to_fsspec_exception():
            self._get_files_wrapper_for_folder_id(source_catalog_id).rename_files(
                source_internal,
                target_internal,
                overwrite=overwrite_strategy,
            )

    @staticmethod
    def _map_paths_to_destinations(
        paths: List[str],
        path2: Union[str, List[str]],
        exists: bool = False,
        flatten: bool = False,
    ) -> List[str]:
        """
        Map source paths to destination paths. Like fsspec other_paths but correctly
        handles directory paths (trailing slash): uses (p.rstrip("/") or p).split("/")[-1]
        for basename instead of p.split("/")[-1], which returns "" for paths like "a/".
        Also preserves trailing slashes on output for directories.
        """
        if isinstance(path2, list):
            # Match fsspec: truncate to the shorter list
            n = min(len(paths), len(path2))
            return path2[:n]

        dest_base = path2.rstrip("/")

        if flatten:
            result: List[str] = []
            for p in paths:
                base = (p.rstrip("/") or p).split("/")[-1]
                suffix = "/" if p.endswith("/") else ""
                result.append(f"{dest_base}/{base}{suffix}")
            return result

        cp = common_prefix(paths)
        if exists:
            cp = cp.rsplit("/", 1)[0]
        if not cp and all(not s.startswith("/") for s in paths):
            return ["/".join([dest_base, p]) for p in paths]
        return [p.replace(cp, dest_base, 1) for p in paths]

    def _compute_exists_for_mv(
        self,
        single_src: str,
        paths1: List[str],
        dest_is_dir: bool,
    ) -> bool:
        """Compute exists flag for _map_paths_to_destinations, aligned with copy logic.

        The exists flag controls how common_prefix is computed when mapping paths;
        True when the destination already exists and we should treat the source as a parent path.
        """
        source_is_file = len(paths1) == 1
        return bool(
            (has_magic(single_src) and source_is_file and dest_is_dir)
            or (not has_magic(single_src) and dest_is_dir and not trailing_sep(single_src))
            or (
                not has_magic(single_src)
                and dest_is_dir
                and source_is_file
                and len(paths1) > 0
                and not trailing_sep(paths1[0])
            )
        )

    def _resolve_mv_paths_for_single_source(
        self,
        single_src: str,
        single_dest: str,
        recursive: bool,
        maxdepth: Optional[int],
        **kwargs: Any,
    ) -> Tuple[List[str], List[str], bool]:
        """
        Resolve (paths1, paths2) for mv when source is a single path (string).
        Flow: expand -> filter dirs if not recursive -> compute paths2 -> dedupe if recursive.
        Returns (paths1, paths2, dest_is_dir).
        """
        # Expand: resolve globs and list matching files/dirs
        paths1 = self.expand_path(single_src, recursive=recursive, maxdepth=maxdepth, **kwargs)
        dest_is_dir = trailing_sep(single_dest) or self.isdir(single_dest)

        # Filter: when not recursive, keep only files (exclude dirs)
        if not recursive or maxdepth is not None:
            paths1 = [p for p in paths1 if not (p.endswith("/") or self.isdir(p))]
            if not paths1:
                return [], [], dest_is_dir

        # Compute paths2: map sources to destinations
        exists = self._compute_exists_for_mv(single_src, paths1, dest_is_dir)
        flatten = (dest_is_dir and any(p.endswith("/") for p in paths1)) or False
        if not dest_is_dir and len(paths1) == 1:
            paths2 = [single_dest]
        else:
            paths2 = self._map_paths_to_destinations(paths1, single_dest, exists=exists, flatten=flatten)

        # Dedupe: when recursive, remove redundant parent paths
        if recursive and maxdepth is None:
            deduped = self._remove_extra_paths_in_recursive_calls(paths1, paths2)
            paths1, paths2 = [p[0] for p in deduped], [p[1] for p in deduped]
        return paths1, paths2, dest_is_dir

    def _resolve_mv_paths_for_list_sources(
        self,
        path1_list: List[str],
        path2_list: List[str],
    ) -> Tuple[List[str], List[str], Optional[bool]]:
        """Resolve (paths1, paths2, dest_is_dir) for mv when source is a list.
        dest_is_dir is set only when path2_list has one element; otherwise None.
        """
        paths1 = path1_list
        single_dest = len(path2_list) == 1

        if single_dest:
            single_dest_path = path2_list[0]
            dest_is_dir = trailing_sep(single_dest_path) or self.isdir(single_dest_path)

            if dest_is_dir:
                # Single directory: map each source to dest/basename
                paths2 = self._map_paths_to_destinations(paths1, single_dest_path, exists=True, flatten=True)
            else:
                # Single file: one destination for all (valid only when len(paths1)==1)
                paths2 = path2_list
        else:
            # List of destinations: 1:1 mapping (zip truncates if lengths differ)
            paths2 = path2_list
            dest_is_dir = None
        return paths1, paths2, dest_is_dir if single_dest else None

    def mv(
        self,
        path1: Union[str, List[str]],
        path2: Union[str, List[str]],
        recursive: bool = False,
        maxdepth: Optional[int] = None,
        *,
        overwrite_strategy: FilesOverwriteStrategy = FilesOverwriteStrategy.REPLACE,
        **kwargs: Any,
    ) -> None:
        """
        Move files or directories from path1 to path2. path1 may contain glob patterns.

        Parameters
        ----------
        path1:
            Source path(s). Format: ``dr://<catalog_id>/path``. A string (file, directory, or glob
            pattern) or a list of explicit paths.
        path2:
            Destination path(s). Format: ``dr://<catalog_id>/path``. A single path when path1 is
            a string. When path1 is a list, either a single directory (ending with /; each
            source maps to path2/basename) or a
            list of paths. When both are lists, truncates to the shorter length (matches fsspec).
        recursive:
            If True, move directories recursively.
        maxdepth:
            If not None, maximum directory depth when resolving path1. None means no limit.
        overwrite_strategy:
            Strategy for overwriting existing paths. Defaults to REPLACE, inline with fsspec.
        kwargs:
            Additional keyword arguments passed to ``expand_path`` when resolving paths and
            to :meth:`mv_file() <datarobot.fs.file_system.DataRobotFileSystem.mv_file>`
            when performing the move.

        Raises
        ------
        ValueError:
            If multiple sources are moved to a single file destination (not a directory).
        """
        # Normalize inputs to lists
        source_is_str = isinstance(path1, str)
        path1_list = cast(List[str], [path1] if source_is_str else list(path1))
        path2_list = cast(List[str], [path2] if isinstance(path2, str) else list(path2))

        # Resolve (paths1, paths2): expand, filter, map, dedupe
        dest_is_dir: Optional[bool]
        if source_is_str:
            paths1, paths2, dest_is_dir = self._resolve_mv_paths_for_single_source(
                path1_list[0], path2_list[0], recursive, maxdepth, **kwargs
            )
        else:
            paths1, paths2, dest_is_dir = self._resolve_mv_paths_for_list_sources(path1_list, path2_list)

        # Early returns and validation
        if not paths1:
            return
        if dest_is_dir is not None and not dest_is_dir and len(paths1) > 1:
            raise ValueError(
                "Cannot move multiple sources to a single file destination. "
                "Provide a directory destination (e.g., ending with /) or a list of destinations."
            )

        # Move: zip truncates to shorter list when lengths differ (matches fsspec)
        with self._try_convert_to_fsspec_exception():
            for p1, p2 in zip(paths1, paths2):
                self.mv_file(p1, p2, overwrite_strategy=overwrite_strategy, **kwargs)

    def clone_catalog_item_dir(self, path_or_id: str, files_to_omit: Optional[List[str]] = None, **kwargs: Any) -> str:
        """
        Clone a catalog item directory (copy all contents) and return the ID of the cloned catalog item.

        Parameters
        ----------
        path_or_id:
            Path or ID of the catalog item directory to clone.
        files_to_omit:
            List of files to omit when cloning. Provide paths relative to the root of the catalog item directory.
        kwargs:
            Additional keyword arguments passed to :meth:`Files.clone() <datarobot.models.files.Files.clone>`.

        Returns
        -------
        str:
            The ID of the cloned catalog item.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> fs.ls("dr://696935d6d5a04a752419cf6d/", detail=False)
            ['696935d6d5a04a752419cf6d/folder/', '696935d6d5a04a752419cf6d/file.txt']
            >>> clone_id = fs.clone_catalog_item_dir("dr://696935d6d5a04a752419cf6d/")
            >>> clone_id
            "696935d6d5a04a752419cf6d-clone"
            >>> fs.ls(f"dr://{clone_id}/", detail=False)
            ['696935d6d5a04a752419cf6d-clone/folder/', '696935d6d5a04a752419cf6d-clone/file.txt']

        Clone a catalog item directory and omit a file:

        .. code-block:: python

            >>> fs.clone_catalog_item_dir("dr://696935d6d5a04a752419cf6d/", files_to_omit=["file.txt"])
            "696935d6d5a04a752419cf6d-clone"
            >>> fs.ls(f"dr://696935d6d5a04a752419cf6d-clone/", detail=False)
            ['696935d6d5a04a752419cf6d-clone/folder/']
        """
        catalog_id = self._strip_protocol(path_or_id).rstrip("/")
        with self._try_convert_to_fsspec_exception():
            return self._get_files_wrapper_for_folder_id(catalog_id).clone(omit=files_to_omit, **kwargs).id

    def put_from_url(
        self,
        path: str,
        url: str,
        unpack_archive_files: bool = True,
        overwrite_strategy: FilesOverwriteStrategy = FilesOverwriteStrategy.RENAME,
        *,
        upload_timeout: int = DEFAULT_MAX_WAIT,
        wait_for_completion: bool = True,
        **kwargs: Any,
    ) -> None:
        """
        Load file(s) from a URL into a directory in the DataRobot file system.


        Parameters
        ----------
        path:
            DataRobot path to the directory (catalog root or a folder inside it).
        url:
            The URL of the file or archive to load. Must be accessible by the DataRobot server.
        unpack_archive_files:
            If True, extract archive contents into the directory. If False, upload the
            file as-is. Defaults to True.
        upload_timeout:
            Maximum time in seconds to wait for the upload to complete.
        wait_for_completion:
            If True, block until the upload completes. Defaults to True.
        overwrite_strategy:
            How to handle name conflicts with existing files. Defaults to
            :meth:`FilesOverwriteStrategy.RENAME <datarobot.enums.FilesOverwriteStrategy.RENAME>`.
        kwargs:
            Additional keyword arguments for future proofing.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> catalog_id = fs.create_catalog_item_dir()
            >>> fs.put_from_url(f"dr://{catalog_id}/data/", "https://example.com/file.png")
            >>> fs.ls(f"dr://{catalog_id}/data/")
            [{'name': 'file.png', 'size': 12345, 'type': 'file', ...}]

        Raises
        ------
        AsyncTimeoutError
            If ``wait_for_completion`` is True and the upload takes longer than ``upload_timeout`` seconds.
        FileExistsError
            If ``overwrite_strategy`` is ``FilesOverwriteStrategy.ERROR`` and a file with the same name already exists.
        """
        catalog_id, internal_path = self._split_path(path)
        prefix = f"{internal_path.rstrip('/')}/" if internal_path else None
        with self._try_convert_to_fsspec_exception():
            files = self._get_files_wrapper_for_folder_id(catalog_id)
            files.upload_from_url(
                url=url,
                use_archive_contents=unpack_archive_files,
                overwrite=overwrite_strategy,
                max_wait=upload_timeout,
                wait_for_completion=wait_for_completion,
                prefix=prefix,
            )

    def put_from_data_source(
        self,
        path: str,
        data_source_id: str,
        credential_id: Optional[str] = None,
        credential_data: Optional[Dict[str, str]] = None,
        unpack_archive_files: bool = True,
        overwrite_strategy: FilesOverwriteStrategy = FilesOverwriteStrategy.RENAME,
        *,
        upload_timeout: int = DEFAULT_MAX_WAIT,
        wait_for_completion: bool = True,
        **kwargs: Any,
    ) -> None:
        """
        Upload one or more files from a data source into a directory in the DataRobot file system.

        Parameters
        ----------
        path:
            Directory path to upload files under. Cannot be root directory.
        data_source_id:
            The ID of the :class:`DataSource <datarobot.models.data_source.DataSource>` to use as the source of data.
        credential_id:
            The ID of the :class:`Credential <datarobot.models.credential.Credential>` to use for authentication.
        credential_data:
            The credentials to authenticate with the database, to use instead of credential ID.
        unpack_archive_files:
            Whether to unpack archive files (zip, tar, :spelling:ignore:`tar.gz`, :spelling:ignore:`tgz`) upon upload.
        overwrite_strategy:
            Strategy to handle naming conflicts when writing to a path where a file already exists. Use
            :meth:`FilesOverwriteStrategy.RENAME <datarobot.enums.FilesOverwriteStrategy.RENAME>` to rename
            and uploaded file using the "<filename> (n).ext" pattern. Use :meth:`FilesOverwriteStrategy.REPLACE
            <datarobot.enums.FilesOverwriteStrategy.REPLACE>` to overwrite the existing file. Use
            :meth:`FilesOverwriteStrategy.SKIP <datarobot.enums.FilesOverwriteStrategy.SKIP>` to skip uploading
            if a file already exists at the target path. Use :meth:`FilesOverwriteStrategy.ERROR
            <datarobot.enums.FilesOverwriteStrategy.ERROR>` to raise `FileExistsError` if a file already exists
            at the target path.
        upload_timeout:
            Maximum time in seconds to wait for the upload to complete.
        wait_for_completion:
            If True, block until the upload completes. If False, return after starting the upload.
        kwargs:
            Additional keyword arguments for future proofing.

        Raises
        ------
        ValueError
            If the directory path is invalid.
        FileNotFoundError
            If the directory path does not exist.
        AsyncTimeoutError
            If ``wait_for_completion`` is True and the upload takes longer than ``upload_timeout`` seconds.

        Examples
        --------
        Upload file or folder from Google Drive.

        Note: GDrive paths must use drive, folder and file IDs.
        Example: ``/<drive_id>/<folder_id>/<file_id>`` or ``/<drive_id>/<folder_id>`` if folder.

        .. code-block:: python

            >>> import datarobot as dr
            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> gcp_cred = dr.Credential.create_gcp(
            ...     name='GDrive Credentials',
            ...     gcp_key={  # Or load from keyfile
            ...         "type": "service_account",
            ...         "private_key_id": "...",
            ...         "private_key": "-----...",  # PKCS#8 formatted private key string with newlines replaced by \n
            ...         "client_email": "user@project.iam.gserviceaccount.com",
            ...         "client_id": "...",
            ...     },
            ... )
            >>> gdrive_connector = next(
            ...     c for c in dr.Connector.list() if c.connector_type == "gdrive"
            ... )
            >>> gdrive_datastore = dr.DataStore.create(
            ...     data_store_type=dr.enums.DataStoreTypes.DR_CONNECTOR_V1,
            ...     canonical_name='GDrive DataStore',
            ...     fields=[{'id': 'gdrive.drive_name', 'name': 'Drive Name', 'value': 'My Drive'}],
            ...     connector_id=gdrive_connector.id,
            ... )
            >>> path = "/<drive_id>/<folder_id>/<file_id>"  # or "/<drive_id>/<folder_id>" for a folder
            >>> gdrive_datasource = dr.DataSource.create(
            ...     data_source_type=dr.enums.DataStoreTypes.DR_CONNECTOR_V1,
            ...     canonical_name='GDrive DataSource for my documents',
            ...     params=dr.DataSourceParameters(data_store_id=gdrive_datastore.id, path=path),
            ... )
            >>> fs.put_from_data_source(
            ...     "dr://<catalog-id>/my_gdrive_documents/",
            ...     gdrive_datasource.id,
            ...     credential_id=gcp_cred.credential_id, # Can omit if using default credentials setup with DataStore
            ... )
            >>> print(fs.ls(f"dr://<catalog-id>/my_gdrive_documents/", detail=False))
            ['<catalog-id>/my_gdrive_documents/file.txt']

        Upload file or folder from AWS S3 bucket:

        .. code-block:: python

            >>> import datarobot as dr
            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> cred = dr.Credential.create_s3(
            ...     name="AWS S3 Credentials",
            ...     aws_access_key_id="...",
            ...     aws_secret_access_key="...",
            ...     aws_session_token="...",
            ... )
            >>> s3_connector = next(
            ...     c for c in dr.Connector.list() if c.connector_type == "s3"
            ... )
            >>> s3_datastore = dr.DataStore.create(
            ...     data_store_type=dr.enums.DataStoreTypes.DR_CONNECTOR_V1,
            ...     canonical_name='S3 DataStore',
            ...     fields=[
            ...         {"id": "fs.defaultFS", "name": "Bucket Name", "value": "my-bucket-name"},
            ...         {"id": "fs.rootDirectory", "name": "Prefix", "value": "/"},
            ...         {"id": "fs.s3.awsRegion", "name": "S3 Bucket Region", "value": "us-east-1"},
            ...     ],
            ...     connector_id=s3_connector.id,
            ... )
            >>> s3_datasource = dr.DataSource.create(
            ...     data_source_type=dr.enums.DataStoreTypes.DR_CONNECTOR_V1,
            ...     canonical_name='S3 DataSource for my files',
            ...     params=dr.DataSourceParameters(
            ...         data_store_id=s3_datastore.id,
            ...         path="path/to/my/file.txt",  # or "path/to/my/folder/"
            ...     ),
            ... )
            >>> fs.put_from_data_source(
            ...     "dr://<catalog-id>/my_s3_files/",
            ...     s3_datasource.id,
            ...     credential_id=cred.credential_id, # Can omit if using default credentials setup with DataStore
            ... )
            >>> print(fs.ls(f"dr://<catalog-id>/my_s3_files/", detail=False))
            ['<catalog-id>/my_s3_files/file.txt']

        Upload file or folder from SharePoint:

        Note: Sharepoint paths must use the following format:
        ``/<HOSTNAME>,<SITE_COLLECTION_ID>,<SITE_ID/WEB_ID>/<DRIVE_ID>/<FILE_OR_FOLDER_ITEM_ID>``.

        Example: ``/mydomain.sharepoint.com,4732d...8b01b0,eb0d3...e42f/b!8tQyRyn.....TowMA13__nTU/01MAJ...EYJTAOR6/``

        .. code-block:: python

            >>> import datarobot as dr
            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> cred = dr.Credential.create_azure_service_principal(
            ...     name="Azure Service Principal Credential for Sharepoint",
            ...     client_id="...",
            ...     client_secret="...",
            ...     azure_tenant_id="...",
            ... )
            >>> sharepoint_connector = next(
            ...     c for c in dr.Connector.list() if c.connector_type == "sharepoint"
            ... )
            >>> sharepoint_datastore = dr.DataStore.create(
            ...     data_store_type=dr.enums.DataStoreTypes.DR_CONNECTOR_V1,
            ...     canonical_name='Sharepoint DataStore',
            ...     fields=[],
            ...     connector_id=sharepoint_connector.id,
            ... )
            >>> path = "/<HOSTNAME>,<SITE_COLLECTION_ID>,<SITE_ID/WEB_ID>/<DRIVE_ID>/<FILE_OR_FOLDER_ITEM_ID>"
            >>> sharepoint_datasource = dr.DataSource.create(
            ...     data_source_type=dr.enums.DataStoreTypes.DR_CONNECTOR_V1,
            ...     canonical_name='Sharepoint DataSource',
            ...     params=dr.DataSourceParameters(
            ...         data_store_id=sharepoint_datastore.id,
            ...         path=path,
            ...     ),
            ... )
            >>> fs.put_from_data_source(
            ...     "dr://<catalog-id>/my_sharepoint_files/",
            ...     sharepoint_datasource.id,
            ...     credential_id=cred.credential_id,
            ... )
            >>> print(fs.ls(f"dr://<catalog-id>/my_sharepoint_files/", detail=False))
            ['<catalog-id>/my_sharepoint_files/my_file.txt']

        See Also
        --------
        :meth:`put_from_url() <datarobot.fs.file_system.DataRobotFileSystem.put_from_url>`

        :meth:`put_file() <datarobot.fs.file_system.DataRobotFileSystem.put_file>`
        """
        catalog_id, internal_path = self._split_path(path)
        prefix = f"{internal_path.rstrip('/')}/" if internal_path else None

        with self._try_convert_to_fsspec_exception():
            self._get_files_wrapper_for_folder_id(catalog_id).upload_from_data_source(
                data_source_id=data_source_id,
                credential_id=credential_id,
                credential_data=credential_data,
                prefix=prefix,
                use_archive_contents=unpack_archive_files,
                overwrite=overwrite_strategy,
                max_wait=upload_timeout,
                wait_for_completion=wait_for_completion,
            )

    def _open(
        self,
        path: str,
        mode: str = "rb",
        block_size: Optional[int] = None,
        autocommit: bool = True,
        cache_options: Optional[Dict[str, Any]] = None,
        overwrite_strategy: FilesOverwriteStrategy = FilesOverwriteStrategy.REPLACE,
        unpack_archive_files: bool = False,
        upload_timeout: int = DEFAULT_MAX_WAIT,
        **kwargs: Any,
    ) -> DataRobotFile:
        """Return a DataRobotFile object for the given path in the DataRobot file system."""
        return DataRobotFile(
            self,
            path,
            mode,
            block_size=block_size,
            autocommit=autocommit,
            cache_options=cache_options,
            overwrite_strategy=overwrite_strategy,
            unpack_archive_files=unpack_archive_files,
            upload_timeout=upload_timeout,
            **kwargs,
        )

    def open(
        self,
        path: str,
        mode: str = "rb",
        block_size: Optional[int] = None,
        cache_options: Optional[Dict[str, Any]] = None,
        compression: Optional[str] = None,
        overwrite_strategy: FilesOverwriteStrategy = FilesOverwriteStrategy.REPLACE,
        unpack_archive_files: bool = False,
        upload_timeout: int = DEFAULT_MAX_WAIT,
        **kwargs: Any,
    ) -> DataRobotFile:
        """
        Open a file in the DataRobot file system.
        Supports read modes 'r', ':spelling:ignore:`rb`' and write modes 'w', ':spelling:ignore:`wb`',
        ':spelling:ignore:`xb`'.

        Parameters
        ----------
        path:
            Path in the DataRobot file system to open.
        mode:
            Mode to open the file in. 'r' or ':spelling:ignore:`rb`' for reading, 'w', ':spelling:ignore:`wb`' or
            ':spelling:ignore:`xb`' for writing.
        block_size:
            Buffer size in bytes for reading and writing.
        cache_options:
            Extra arguments to pass through the cache.
        compression:
            If given, open file using compression codec. Can either be a compression
            name (a key in `fsspec.compression.compr`) or "infer" to guess the
            compression from the filename suffix.
        overwrite_strategy:
            Strategy to handle naming conflicts when writing to a path where a file already exists. Use
            :meth:`FilesOverwriteStrategy.RENAME <datarobot.enums.FilesOverwriteStrategy.RENAME>` to rename
            and uploaded file using the "<filename> (n).ext" pattern. Use :meth:`FilesOverwriteStrategy.REPLACE
            <datarobot.enums.FilesOverwriteStrategy.REPLACE>` to overwrite the existing file. Use
            :meth:`FilesOverwriteStrategy.SKIP <datarobot.enums.FilesOverwriteStrategy.SKIP>` to skip uploading
            if a file already exists at the target path. Use :meth:`FilesOverwriteStrategy.ERROR
            <datarobot.enums.FilesOverwriteStrategy.ERROR>` to raise `FileExistsError` if a file already exists
            at the target path.
        unpack_archive_files:
            If `True`, automatically unpack archive files (zip, tar, :spelling:ignore:`tar.gz`, :spelling:ignore:`tgz`)
            upon upload.
        upload_timeout:
            Maximum time in seconds to wait for file upload to complete.
        kwargs:
            Additional keyword arguments passed to :class:`DataRobotFile
            <datarobot.fs.file_system.DataRobotFile>` or :class:`TextFileWrapper
            <io.TextFileWrapper>`.

        Raises
        ------
        IsADirectoryError
            If attempting to open a directory for reading.
        FileNotFoundError
            If attempting to open a non-existent file for reading.
        ValueError
            If an unsupported file mode is provided, an invalid path is passed, or if file is too big to download.
        FileExistsError
            If attempting to write to a path where a file already exists and overwrite strategy is set to
            :meth:`FilesOverwriteStrategy.ERROR <datarobot.enums.FilesOverwriteStrategy.ERROR>` or mode is set
            to ':spelling:ignore:`xb`'.

        Returns
        -------
        DataRobotFile
            A file-like object for reading or writing.

        Examples
        --------
        Open a file for reading:

        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> with fs.open("dr://696935d6d5a04a752419cf6d/notes/agenda.txt", mode="r") as f:
            ...     data = f.read()

        Read first 20 bytes from a file then skip to byte 100 and read the next 30 bytes:

        .. code-block:: python

            >>> with fs.open("dr://696935d6d5a04a752419cf6d/figures/plot.png", mode="rb") as f:
            ...     first_20_bytes = f.read(20)
            ...     f.seek(100)
            ...     next_30_bytes = f.read(30)

        """
        return cast(
            DataRobotFile,
            super().open(
                path,
                mode=mode,
                block_size=block_size,
                cache_options=cache_options,
                compression=compression,
                overwrite_strategy=overwrite_strategy,
                unpack_archive_files=unpack_archive_files,
                upload_timeout=upload_timeout,
                **kwargs,
            ),
        )

    def touch(self, path: str, truncate: bool = True, **kwargs: Any) -> None:
        """
        Create an empty file at the given path.

        DataRobotFileSystem does not support updating timestamps of existing files.

        Parameters
        ----------
        path:
            Path to the file to create.
        truncate:
            Whether to replace the existing file with an empty one.  This must always be set to True.
        kwargs:
            Additional keyword arguments passed to
            :meth:`open() <datarobot.fs.file_system.DataRobotFileSystem.open>`.

        Raises
        ------
        NotImplementedError
            If attempting to update the timestamp of an existing file with truncate set to False.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> fs.touch("dr://696935d6d5a04a752419cf6d/notes/agenda.txt")
        """
        if truncate or not self.exists(path):
            with self.open(path, "wb", **kwargs):
                pass
        else:
            raise NotImplementedError("DataRobotFileSystem does not support updating file timestamps.")

    def read_block(
        self,
        fn: str,
        offset: int,
        length: Optional[int],
        delimiter: Optional[bytes] = None,
    ) -> bytes:
        """
        Read a block of bytes from a file.

        Starting at ``offset`` of the file, read ``length`` bytes.  If
        ``delimiter`` is set then we ensure that the read starts and stops at
        delimiter boundaries that follow the locations ``offset`` and ``offset
        + length``.  If ``offset`` is zero then we start at zero.  The
        bytestring returned WILL include the end delimiter string.

        If offset+length is beyond the eof, reads to eof.

        Parameters
        ----------
        fn:
            Filepath to read from.
        offset:
            Byte offset to start read from.
        length:
            Number of bytes to read. If None, read to end of file.
        delimiter:
            Ensure reading starts and stops at delimiter bytestring.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> fs.read_block("dr://696935d6d5a04a752419cf6d/data/file.txt", 0, 13)
            b'Alice, 100\\nBo'
            >>> fs.read_block("dr://696935d6d5a04a752419cf6d/data/file.txt", 0, 13, delimiter=b'\\n')
            b'Alice, 100\\nBob, 200\\n'

        Use ``length=None`` to read to the end of the file.

        .. code-block:: python

            >>> fs.read_block("dr://696935d6d5a04a752419cf6d/data/file.txt", 0, None, delimiter=b'\\n')
            b'Alice, 100\\nBob, 200\\nCharlie, 300'
        """
        return cast(bytes, super().read_block(fn, offset, length, delimiter=delimiter))

    def put_file(
        self,
        lpath: str,
        rpath: str,
        callback: Callback = DEFAULT_CALLBACK,
        mode: str = "overwrite",
        raise_error_on_directory: bool = True,
        **kwargs: Any,
    ) -> None:
        """
        Upload a single file from local to DataRobot file system.

        Parameters
        ----------
        lpath:
            Local file path.
        rpath:
            DataRobot file system path.
        callback:
            Callback to track progress of the file transfer. Not supported as DataRobotFileSystem
            does not support buffered uploads.
        mode:
            Mode to open the file in: 'overwrite' or 'create'.
        raise_error_on_directory:
            Whether to raise an exception if the local path is a directory. DataRobot file system does not support
            creating empty directories. If False, the function does nothing and returns silently.
        kwargs:
            Keyword arguments passed to
            :meth:`open() <datarobot.fs.file_system.DataRobotFileSystem.open>`.

        Raises
        ------
        FileExistsError
            If the file already exists and mode is set to 'create'.
        NotImplementedError
            If attempting to upload a directory and `raise_error_on_directory` is True.
        ValueError
            If attempting to upload a file to an invalid path.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> fs.put_file(
            ...     "/Users/username/local/path/to/file.txt",
            ...     "dr://696935d6d5a04a752419cf6d/my/new/file_copy.txt",
            ... )
        """
        if os.path.isdir(lpath):
            if raise_error_on_directory:
                raise NotImplementedError("Uploading directories is not supported for DataRobotFileSystem.")
            return
        if mode == "create" and self.exists(rpath):
            raise FileExistsError(f"File already exists: {rpath}")

        with open(lpath, "rb") as f1:
            size = f1.seek(0, 2)
            callback.set_size(size)
            f1.seek(0)

            with self.open(rpath, "wb", **kwargs) as f2:
                while f1.tell() < size:
                    data = f1.read(self.blocksize)
                    segment_len = f2.write(data)
                    if segment_len is None:
                        segment_len = len(data)
                    callback.relative_update(segment_len)

    # SPDX-FileCopyrightText: 2018 Martin Durant
    # SPDX-License-Identifier: BSD-3-Clause
    # The following method is derived from fsspec (https://github.com/fsspec/filesystem_spec)
    def put(
        self,
        lpath: Union[str, List[str]],
        rpath: Union[str, List[str]],
        recursive: bool = False,
        callback: Callback = DEFAULT_CALLBACK,
        maxdepth: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        """
        Upload local file(s) to DataRobot file system.

        Copies a specific file or tree of files (if `recursive=True`). If `rpath`
        ends with a "/", it will be assumed to be a directory, and target files
        will go within. If `lpath` ends with a "/", it will be assumed to be a directory
        and will target files inside the directory. Calls
        :meth:`put_file() <datarobot.fs.file_system.DataRobotFileSystem.put_file>`
        for each source path or uses
        :class:`FilesStage <datarobot.models.files.FilesStage>` to upload multiple files at once
        if upload can be optimized.

        Parameters
        ----------
        lpath:
            Local file path or list of local file paths to upload.
        rpath:
            DataRobot file system path or list of DataRobot file system paths to upload to.
        recursive:
            Whether to recursively target local files to upload.
        callback:
            Callback to track progress of the file transfer. Not supported as DataRobotFileSystem
            does not support buffered uploads.
        maxdepth:
            Maximum depth to recurse when targeting local files to upload.
        kwargs:
            Additional keyword arguments passed to
            :meth:`put_file() <datarobot.fs.file_system.DataRobotFileSystem.put_file>`.

        Other Parameters
        ----------------
        raise_error_on_directory:
            Whether to raise an exception for local directory paths. DataRobot file system does not support creating
            empty directories. Defaults to False so invocations of
            :meth:`put_file() <datarobot.fs.file_system.DataRobotFileSystem.put_file>` for local
            directory paths do nothing and return silently.
        overwrite_strategy:
            How to handle name conflicts with existing files. Defaults to
            :meth:`FilesOverwriteStrategy.RENAME <datarobot.enums.FilesOverwriteStrategy.RENAME>`.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> fs.put(
            ...     "/Users/username/local/path/to/file.txt",
            ...     "dr://696935d6d5a04a752419cf6d/my/new/file_copy.txt",

        Upload a directory recursively:

        .. code-block:: python

            >>> fs.put(
            ...     "/Users/username/local/path/to/directory",
            ...     "dr://696935d6d5a04a752419cf6d/my/new/directory/",
            ...     recursive=True,
            ... )

        Upload all PDF files in a directory:

        .. code-block:: python

            >>> fs.put(
            ...     "/Users/username/local/my/documents/**/*.pdf",
            ...     "dr://696935d6d5a04a752419cf6d/my-pdf-documents/",
            ...     recursive=True,
            ... )

        Upload multiple files at once:

        .. code-block:: python

            >>> fs.put(
            ...     ["/Users/username/local/path/to/file1.txt", "/Users/username/local/path/to/file2.txt"],
            ...     ["dr://696935d6d5a04a752419cf6d/my/new/file1.txt", "dr://696935d6d5a04a752419cf6d/my/new/file2.txt"],
            ... )
        """
        if isinstance(lpath, list) and isinstance(rpath, list):
            # No need to expand paths when both source and destination
            # are provided as lists
            rpaths = rpath
            lpaths = lpath
        else:
            source_is_str = isinstance(lpath, str)
            if source_is_str:
                lpath = make_path_posix(lpath)
            fs = LocalFileSystem()
            lpaths = fs.expand_path(lpath, recursive=recursive, maxdepth=maxdepth)
            if source_is_str and (not recursive or maxdepth is not None):
                # Non-recursive glob does not copy directories
                lpaths = [p for p in lpaths if not (trailing_sep(p) or fs.isdir(p))]
                if not lpaths:
                    return

            source_is_file = len(lpaths) == 1
            dest_is_dir = isinstance(rpath, str) and (trailing_sep(rpath) or self.isdir(rpath))

            rpath = self._strip_protocol(rpath) if isinstance(rpath, str) else [self._strip_protocol(p) for p in rpath]
            exists = source_is_str and (
                (has_magic(lpath) and source_is_file)  # type: ignore[arg-type]
                or (not has_magic(lpath) and dest_is_dir and not trailing_sep(lpath))  # type: ignore[arg-type]
            )
            rpaths = other_paths(
                lpaths,
                rpath,
                exists=exists,
                flatten=not source_is_str,
            )

        paths = list(zip(lpaths, rpaths))
        callback.set_size(len(paths))

        raise_error_on_directory = kwargs.pop("raise_error_on_directory", False)
        overwrite_strategy = kwargs.pop("overwrite_strategy", FilesOverwriteStrategy.RENAME)

        use_stage_optimization = False
        if isinstance(rpath, list) and len(paths) > 1:
            first_catalog_id = self._split_path(rpath[0])[0]
            use_stage_optimization = all(self._split_path(p)[0] == first_catalog_id for p in rpath)
        elif isinstance(rpath, str) and dest_is_dir and len(paths) > 1:
            use_stage_optimization = True

        if use_stage_optimization:
            catalog_id = self._split_path(rpaths[0])[0]
            with self._try_convert_to_fsspec_exception():
                stage = self._get_files_wrapper_for_folder_id(catalog_id=catalog_id).create_stage()

            for local_path, remote_path in callback.wrap(paths):
                if os.path.isdir(local_path):
                    if raise_error_on_directory:
                        raise NotImplementedError("Uploading directories is not supported for DataRobotFileSystem.")
                    continue

                with callback.branched(local_path, remote_path) as child:
                    file_size = os.path.getsize(local_path)
                    child.set_size(file_size)
                    _, internal_path = self._split_path(remote_path)
                    with self._try_convert_to_fsspec_exception():
                        stage.upload(source=local_path, file_name=internal_path)
                    child.relative_update(file_size)

            stage.apply(overwrite=overwrite_strategy)
            return

        for local_path, remote_path in callback.wrap(paths):
            with callback.branched(local_path, remote_path) as child:
                self.put_file(
                    local_path,
                    remote_path,
                    callback=child,
                    raise_error_on_directory=raise_error_on_directory,
                    overwrite_strategy=overwrite_strategy,
                    **kwargs,
                )

    def get_mapper(
        self,
        root: str = root_marker,
        missing_exceptions: Optional[Tuple[Type[Exception], ...]] = None,
    ) -> DataRobotFSMap:
        """
        Create a key/value mutable store based on this file-system.

        Creates a MutableMapping interface to the DataRobot file system at the given root path.

        Parameters
        ----------
        root:
            Path in the DataRobot file system to use as the root for the map.
        missing_exceptions:
            Exceptions to convert to KeyError if raised when working with the file system.

        Returns
        -------
        DataRobotFSMap:
            A key/value mutable store based on this file-system.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem, DataRobotFSMap
            >>> fs = DataRobotFileSystem()
            >>> root_map = fs.get_mapper()
            >>> map = fs.get_mapper("dr://696935d6d5a04a752419cf6d/")

        Retrieve file contents from file system using map:

        .. code-block:: python

            >>> map["file.txt"]
            b"Hello, world!"
            >>> "folder/path/file.txt" in map
            True
            >>> file_count = len(map)
            >>> file_count
            3
            >>> [file for file in map]
            ["file.txt", "folder/path/file.txt", "another/folder/file.txt"]
            >>> map.getitems(["file.txt", "folder/path/file.txt", "another/folder/file.txt"])
            {
                "file.txt": b"Hello, world!",
                "folder/path/file.txt": b"Hello, world!",
                "another/folder/file.txt": b"Hello, world!",
            }

        Set file contents in file system using map:

        .. code-block:: python

            >>> map["file.txt"] = b"Hello, world!"
            >>> map["folder/path/new_file.txt"] = b"This is a new file!"
            >>> map.setitems({
                "another/folder/file.txt": b"Hello, world!",
                "folder/path/new_file.txt": b"This is a new file!",
            })

        Delete files from file system using map:

        .. code-block:: python

            >>> del map["file.txt"]
            >>> map.delitems(["folder/path/new_file.txt", "another/folder/file.txt"])
            >>> map.pop("file.txt", "default_value_if_file_does_not_exist")
            b'Hello, world!'
            >>> map.pop("folder/path/non_existent_file.txt", "default_value_if_file_does_not_exist")
            'default_value_if_file_does_not_exist'

        Clear all files under the map root. This may have unintended consequences as
        DataRobot file system does not support empty directories:

        .. code-block:: python

            >>> map.clear()
            >>> len(map)
            0
        """
        return DataRobotFSMap(root, self, missing_exceptions)

    def pipe_file(self, path: str, value: bytes, mode: str = "overwrite", **kwargs: Any) -> None:
        """
        Set the bytes of a given file.

        Parameters
        ----------
        path:
            Path to the file to set the bytes of.
        value:
            Bytes to set the file to.
        mode:
            Mode to use when writing to the file. Defaults to "overwrite". Use create to only write if the file does not
            exist.
        kwargs:
            Additional keyword arguments passed to
            :meth:`open() <datarobot.fs.file_system.DataRobotFileSystem.open>`.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> fs.pipe_file("dr://696935d6d5a04a752419cf6d/my/new/file.txt", b"Hello, world!")
        """
        open_mode = "xb" if mode == "create" else "wb"
        with self.open(path, open_mode, **kwargs) as f:
            f.write(value)

    def pipe(self, path: Union[str, Dict[str, bytes]], value: Optional[bytes] = None, **kwargs: Any) -> None:
        """
        Put value into path.

        Counterpart to :meth:`cat() <datarobot.fs.file_system.DataRobotFileSystem.cat>`.
        Calls :meth:`put_file() <datarobot.fs.file_system.DataRobotFileSystem.put_file>`.

        Parameters
        ----------
        path:
            Path to write the value to. If a string, a single remote location to put ``value`` bytes. If a dict,
            a mapping of ``{path: bytesvalue}``.
        value:
            Value to put into the path. If using a single path, these are bytes to put there. Ignored if path is a dict.
        kwargs:
            Additional keyword arguments passed to
            :meth:`put_file() <datarobot.fs.file_system.DataRobotFileSystem.put_file>`.

        Raises
        ------
        ValueError
            If path is not a string or dict.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> fs.pipe("dr://696935d6d5a04a752419cf6d/my/new/file.txt", b"Hello, world!")
            >>> fs.pipe({"dr://696935d6d5a04a752419cf6d/my/new/file.txt": b"Hello, world!"})
            >>> fs.pipe({
            ...     "dr://696935d6d5a04a752419cf6d/my/new/file.txt": b"Hello, world!",
            ...     "dr://696935d6d5a04a752419cf6d/my/new/file2.txt": b"Hello, world2!",
            ... })
        """
        super().pipe(path, value=value, **kwargs)

    def checksum(self, path: str) -> int:
        """
        Unique value for the content of a file at the given path.

        If the checksum is the same from one moment to another, the contents
        are guaranteed to be the same. If the checksum changes, the contents
        *might* have changed.

        Parameters
        ----------
        path
            Path in the DataRobot file system to get the checksum of.

        Returns
        -------
        int
            The checksum of the file at the given path.
        """
        return cast(int, super().checksum(path))

    def expand_path(
        self, path: Union[str, List[str]], recursive: bool = False, maxdepth: Optional[int] = None, **kwargs: Any
    ) -> List[str]:
        """
        Turn one or more paths (can be globs or directory paths) into a list of all matching paths to files
        and directories.

        Parameters
        ----------
        path:
            Path or list of paths to expand.
        recursive:
            Whether to search recursively when expanding paths.
        maxdepth:
            Maximum depth to search when expanding paths.
        kwargs:
            Additional keyword arguments passed to :meth:`find() <datarobot.fs.file_system.DataRobotFileSystem.find>`
            or :meth:`glob() <datarobot.fs.file_system.DataRobotFileSystem.glob>`, which may in turn call
            :meth:`ls() <datarobot.fs.file_system.DataRobotFileSystem.ls>`.

        Returns
        -------
        List[str]
            List of all matching paths.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> fs.expand_path("dr://696935d6d5a04a752419cf6d/finance/", recursive=True, maxdepth=1)
            [
                'dr://696935d6d5a04a752419cf6d/finance/',
                'dr://696935d6d5a04a752419cf6d/finance/budgets/',
                'dr://696935d6d5a04a752419cf6d/finance/employee-list.csv',
            ]

        Expand a glob pattern with no max depth:

        .. code-block:: python

            >>> fs.expand_path("dr://696935d6d5a04a752419cf6d/finance/**/*.csv", recursive=True)
            [
                'dr://696935d6d5a04a752419cf6d/finance/employee-list.csv',
                'dr://696935d6d5a04a752419cf6d/finance/budgets/Q2_budget_2024.csv',
                'dr://696935d6d5a04a752419cf6d/finance/budgets/archive/Q3_budget_2000.csv',
            ]

        Expand a list of paths:

        .. code-block:: python

            >>> fs.expand_path([
            ...    "dr://696935d6d5a04a752419cf6d/finance/budgets/*.csv",
            ...    "dr://696935d6d5a04a752419cf6d/finance/employee-list.csv",
            ... ])
            [
                'dr://696935d6d5a04a752419cf6d/finance/budgets/Q2_budget_2024.csv',
                'dr://696935d6d5a04a752419cf6d/finance/employee-list.csv',
            ]
        """
        return cast(List[str], super().expand_path(path, recursive=recursive, maxdepth=maxdepth, **kwargs))

    def get(
        self,
        rpath: Union[str, List[str]],
        lpath: Union[str, List[str]],
        recursive: bool = False,
        callback: Callback = DEFAULT_CALLBACK,
        maxdepth: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        """
        Download file(s) from the DataRobot file system to the local file system.

        Copies a specific file or tree of files (if ``recursive``=True). If ``lpath``
        ends with a "/", it will be assumed to be a directory, and target files
        will go within. Can submit a list of paths, which may be glob-patterns
        and will be expanded.

        Calls :meth:`get_file() <datarobot.fs.file_system.DataRobotFileSystem.get_file>` for each file.

        Parameters
        ----------
        rpath:
            Path or list of paths to download from the DataRobot file system.
        lpath:
            Path or list of paths to download to the local file system.
        recursive:
            Whether to recursively target files to download inside directories.
        callback:
            Callback to track progress of the file transfer.
        maxdepth:
            Maximum depth to recurse when targeting files to download inside directories.
        kwargs:
            Additional keyword arguments passed to
            :meth:`get_file() <datarobot.fs.file_system.DataRobotFileSystem.get_file>`.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> fs.get(
            ...     "dr://696935d6d5a04a752419cf6d/finance/budgets/Q2_budget_2024.csv",
            ...     "/Users/username/local/path/to/download/Q2_budget_2024.csv",
            ... )

        Download a directory recursively:

        .. code-block:: python

            >>> fs.get(
            ...     "dr://696935d6d5a04a752419cf6d/finance/budgets/",
            ...     "/Users/username/local/path/to/download/budgets/",
            ...     recursive=True,
            ... )

        Download all PDF files in a directory:

        .. code-block:: python

            >>> fs.get(
            ...     "dr://696935d6d5a04a752419cf6d/finance/budgets/**/*.pdf",
            ...     "/Users/username/local/path/to/download/budgets/",
            ...     recursive=True,
            ... )

        Download multiple files at once:

        .. code-block:: python

            >>> fs.get(
            ...     [
            ...         "dr://696935d6d5a04a752419cf6d/finance/budgets/Q2_budget_2024.csv",
            ...         "dr://696935d6d5a04a752419cf6d/finance/employee-list.csv"
            ...     ],
            ...     [
            ...         "/Users/username/local/path/to/download/Q2_budget_2024.csv",
            ...         "/Users/username/local/path/to/download/employee-list.csv"
            ...     ],
            ... )
        """
        super().get(rpath, lpath, recursive=recursive, callback=callback, maxdepth=maxdepth, **kwargs)

    def get_file(
        self,
        rpath: str,
        lpath: str,
        callback: Callback = DEFAULT_CALLBACK,
        outfile: Optional[io.IOBase] = None,
        **kwargs: Any,
    ) -> None:
        """
        Download a single file from the DataRobot file system to the local file system.

        Parameters
        ----------
        rpath:
            Path to download from the DataRobot file system.
        lpath:
            Path to download to the local file system.
        callback:
            Callback to track progress of the file transfer.
        outfile:
            File-like object to write to. The user is responsible for closing it when they are done.
        kwargs:
            Additional keyword arguments passed to
            :meth:`open() <datarobot.fs.file_system.DataRobotFileSystem.open>`.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> fs.get_file(
            ...     "dr://696935d6d5a04a752419cf6d/finance/budgets/Q2_budget_2024.csv",
            ...     "/Users/username/local/path/to/download/Q2_budget_2024.csv",
            ... )

        .. code-block:: python

            >>> from datarobot.fs import DataRobotFileSystem
            >>> fs = DataRobotFileSystem()
            >>> with open("/Users/username/local/path/to/download/Q2_budget_2024.csv", "wb") as f:
            ...     fs.get_file("dr://696935d6d5a04a752419cf6d/finance/budgets/Q2_budget_2024.csv", f)
        """
        super().get_file(rpath, lpath, callback=callback, outfile=outfile, **kwargs)

    def mkdir(self, *args: Iterable[Any], **kwargs: Any) -> None:
        """Not supported as DataRobotFileSystem does not support empty directories."""
        raise NotImplementedError("mkdir is not supported for DataRobotFileSystem.")

    def makedirs(self, *args: Iterable[Any], **kwargs: Any) -> None:
        """Not supported as DataRobotFileSystem does not support empty directories."""
        raise NotImplementedError("makedirs is not supported for DataRobotFileSystem.")

    def rmdir(self, *args: Iterable[Any], **kwargs: Any) -> None:
        """Not supported as DataRobotFileSystem does not support empty directories."""
        raise NotImplementedError("rmdir is not supported for DataRobotFileSystem.")

    def modified(self, *args: Iterable[Any], **kwargs: Any) -> datetime:
        """DataRobotFileSystem does not currently expose file modification timestamp."""
        raise NotImplementedError("modified is not supported for DataRobotFileSystem.")


class DataRobotFile(AbstractBufferedFile):  # type: ignore[misc]
    """
    File-like object for reading and writing files in the DataRobot file system.

    Supports read modes 'r', ':spelling:ignore:`rb`' and write modes 'w', ':spelling:ignore:`wb`',
    ':spelling:ignore:`xb`'. DataRobot file system buffers writes in memory only before
    uploading on close.

    Attributes
    ----------
    path: str
        File path in the DataRobot file system.
    mode: str
        File mode, either ':spelling:ignore:`rb`', ':spelling:ignore:`wb`', or ':spelling:ignore:`xb`'.
    fs: :class:`DataRobotFileSystem <datarobot.fs.file_system.DataRobotFileSystem>`
        The DataRobot file system instance.
    blocksize: int
        Block size for reading files.
    autocommit: bool
        Whether to automatically commit changes on close.
    loc: int
        Current position in the file.
    closed: bool
        Whether the file is closed.
    forced: bool
        Whether the file is in forced mode.
    offset: Optional[int]
        Content length of the file.
    buffer: io.BytesIO
        In-memory buffer when writing.
    overwrite_strategy:
        Strategy to handle file naming conflicts when writing files.
    unpack_archive_files:
        Whether to unpack archive files (zip, tar, :spelling:ignore:`tar.gz`, :spelling:ignore:`tgz`) upon upload.
    upload_timeout:
        Maximum time in seconds to wait for file upload to complete.

    See Also
    --------
    :meth:`open() <datarobot.fs.file_system.DataRobotFileSystem.open>`
    """

    DOWNLOAD_CHUNK_SIZE_WITHOUT_RANGE_HEADERS = io.DEFAULT_BUFFER_SIZE
    SIGNED_URL_EXPIRATION_SECONDS = 100
    DEFAULT_UPLOAD_TIMEOUT = DEFAULT_MAX_WAIT

    READ_MODES = {"rb"}
    WRITE_MODES = {"wb", "xb"}

    def __init__(
        self,
        fs: DataRobotFileSystem,
        path: str,
        mode: str = "rb",
        block_size: Optional[int] = None,
        autocommit: bool = True,
        cache_options: Optional[Dict[str, Any]] = None,
        overwrite_strategy: FilesOverwriteStrategy = FilesOverwriteStrategy.REPLACE,
        unpack_archive_files: bool = False,
        upload_timeout: int = DEFAULT_UPLOAD_TIMEOUT,
        **kwargs: Any,
    ):
        """
        Parameters
        ----------
        fs:
            The DataRobot file system instance.
        path:
            File path in the DataRobot file system.
        mode:
            File mode, either ':spelling:ignore:`rb`', ':spelling:ignore:`wb`', or ':spelling:ignore:`xb`'.
        block_size:
            Block size for reading files. Optional.
        autocommit:
            Whether to automatically commit changes on close.
        cache_options:
            Cache options to use when reading.
        overwrite_strategy:
            Strategy to handle naming conflicts when writing to a path where a file already exists. Use
            :meth:`FilesOverwriteStrategy.RENAME <datarobot.enums.FilesOverwriteStrategy.RENAME>` to rename
            and uploaded file using the "<filename> (n).ext" pattern. Use :meth:`FilesOverwriteStrategy.REPLACE
            <datarobot.enums.FilesOverwriteStrategy.REPLACE>` to overwrite the existing file. Use
            :meth:`FilesOverwriteStrategy.SKIP <datarobot.enums.FilesOverwriteStrategy.SKIP>` to skip uploading
            if a file already exists at the target path. Use :meth:`FilesOverwriteStrategy.ERROR
            <datarobot.enums.FilesOverwriteStrategy.ERROR>` to raise `FileExistsError` if a file already exists
            at the target path. If mode is ':spelling:ignore:`xb`', this is always set to ERROR.
        unpack_archive_files:
            Whether to unpack archive files (zip, tar, :spelling:ignore:`tar.gz`, :spelling:ignore:`tgz`) upon upload
        upload_timeout:
            Maximum time in seconds to wait for file upload to complete.
        kwargs:
            Additional keyword arguments passed to `AbstractBufferedFile.__init__`.
        """
        catalog_id, internal_path = fs._split_path(path)

        if mode not in self.READ_MODES | self.WRITE_MODES:
            raise ValueError(f"Unsupported file mode '{mode}'. Supported modes are 'rb', 'wb', and 'xb'.")
        elif mode in self.WRITE_MODES and path.endswith("/"):
            raise ValueError("Invalid path. Cannot write to a directory path. Please provide a file path.")
        elif mode in self.WRITE_MODES and not internal_path:
            raise ValueError("Invalid path. Cannot write to root or overwrite catalog directory.")

        if "r" in mode and fs.isdir(path):
            raise IsADirectoryError(f"Is a directory: '{path}'")

        if mode == "rb":  # Lock file read to current version
            with fs._try_convert_to_fsspec_exception():
                self.version_id: Optional[str] = FilesDetails.get(catalog_id).version_id
                # Set details here instead of __init__ to avoid race condition with different version
                self.details = fs.info(path, version_id=self.version_id)
        else:
            self.version_id = None

        super().__init__(
            fs=fs,
            path=path,
            mode=mode,
            block_size=block_size,
            autocommit=autocommit,
            cache_options=cache_options,
            **kwargs,
        )
        # Always use ERROR strategy for 'xb' mode to prevent overwriting existing files
        self.overwrite_strategy = FilesOverwriteStrategy.ERROR if mode == "xb" else overwrite_strategy
        self.unpack_archive_files = unpack_archive_files
        self.upload_timeout = upload_timeout
        self._temp_file_cache_path: Optional[str] = None
        self._memory_file_cache: Optional[io.BytesIO] = None
        self._cached_url: Optional[str] = None
        self.__url_cache_expiry: float = 0.0
        self._supports_range_requests: Optional[bool] = None
        self._read_client: Optional[requests.Session] = None
        self._is_datarobot_url_for_read: Optional[bool] = None

        # Satisfy mypy types for inherited attributes
        self.fs: DataRobotFileSystem
        self.buffer: io.BytesIO
        self.forced: bool
        self.offset: Optional[int]

    def _fetch_range_with_range_headers(self, client: requests.Session, start: int, end: int) -> bytes:
        """Fetch byte range using HTTP Range headers."""
        with self.fs._try_convert_to_fsspec_exception():
            response = client.get(self.url, headers={"Range": f"bytes={start}-{end - 1}"}, stream=True)
            try:
                response.raise_for_status()
                return bytes(response.content)
            finally:
                response.close()  # Trigger close http streaming connection

    def _fetch_full_file_content(self, client: requests.Session, start: int, end: int) -> bytes:
        """Fetch full file content and cache in memory for small files."""
        if self._memory_file_cache is None:
            with self.fs._try_convert_to_fsspec_exception():
                response = client.get(self.url, stream=True)
                try:
                    response.raise_for_status()
                    cache = io.BytesIO()
                    for chunk in response.iter_content(chunk_size=self.DOWNLOAD_CHUNK_SIZE_WITHOUT_RANGE_HEADERS):
                        cache.write(chunk)
                finally:
                    response.close()  # Trigger close http streaming connection
            self._memory_file_cache = cache
        self._memory_file_cache.seek(start)
        return self._memory_file_cache.read(end - start)

    def _fetch_range_with_temp_file(self, client: requests.Session, start: int, end: int) -> bytes:
        """
        Fetch byte range and cache to temporary file.
        Used when file size exceeds blocksize and range requests are not supported.
        """
        if self._temp_file_cache_path is None:
            with tempfile.NamedTemporaryFile(suffix=".tmp", prefix="datarobot_", delete=False) as temp_file:
                with self.fs._try_convert_to_fsspec_exception():
                    response = client.get(self.url, stream=True)
                    try:
                        response.raise_for_status()
                        for chunk in response.iter_content(chunk_size=self.DOWNLOAD_CHUNK_SIZE_WITHOUT_RANGE_HEADERS):
                            temp_file.write(chunk)
                    finally:
                        response.close()  # Trigger close http streaming connection
                self._temp_file_cache_path = temp_file.name

        with open(self._temp_file_cache_path, "rb") as f:
            f.seek(start)
            return f.read(end - start)

    def _fetch_range(self, start: int, end: int) -> bytes:
        """
        Fetch a byte range from the file in the DataRobot file system.

        Parameters
        ----------
        start:
            Starting byte position (inclusive).
        end:
            Ending byte position (exclusive).

        Returns
        -------
        bytes
            The bytes in the specified range.
        """
        if self.use_range_headers:
            return self._fetch_range_with_range_headers(self.read_client, start, end)
        elif self.details["size"] <= self.blocksize:
            # If file size is less than blocksize, end <= blocksize, can fetch full content and cache it without worry.
            # Subsequent requests will pull from the cache without making a new request.
            return self._fetch_full_file_content(self.read_client, start, end)
        else:
            # For large files without range headers, download to temp file.
            # Subsequent requests will pull from the temp file without making a new request.
            return self._fetch_range_with_temp_file(self.read_client, start, end)

    def _initiate_upload(self) -> None:
        """DataRobot file system does not support buffered uploads. No need to initiate upload."""
        pass

    def _upload_chunk(self, final: bool = False) -> bool:
        """
        If `final` is True, upload the buffered data.

        DataRobot file system does not support multipart uploads, so
        :class:`DataRobotFile <datarobot.fs.file_system.DataRobotFile>` buffers the entire file in memory
        and only uploads when `final` is True.
        If the file size exceeds available memory, this may result in an out of memory error.

        Parameters
        ----------
        final:
            Whether this is the final chunk to upload.

        Returns
        -------
        bool
            True if the upload was executed complete, False otherwise.
        """
        if not final:
            return False

        self.buffer.seek(0)
        with self.fs._try_convert_to_fsspec_exception():
            catalog_id, internal_path = self.fs._split_path(self.path)
            dir_path, file_name = os.path.split(internal_path)
            self.fs._get_files_wrapper_for_folder_id(catalog_id).upload_file(
                file=self.buffer,
                prefix=f"{dir_path}/" if dir_path else None,
                use_archive_contents=self.unpack_archive_files,
                overwrite=self.overwrite_strategy,
                read_timeout=self.upload_timeout,
                max_wait=self.upload_timeout,
                wait_for_completion=True,
                file_name=file_name,
            )
        return True

    def write(self, data: bytes) -> int:
        """
        Write data to buffer.

        Parameters
        ----------
        data:
            Data to write as bytes.

        Returns
        -------
        int
            Number of bytes written.

        Raises
        ------
        ValueError
            If the file is not in write mode, is closed, or has been force-flushed.
        """
        if not self.writable():
            raise ValueError("File not in write mode")
        if self.closed:
            raise ValueError("I/O operation on closed file.")
        if self.forced:
            raise ValueError("This file has been force-flushed, can only close")
        out = self.buffer.write(data)
        self.loc += out
        return out

    def flush(self, force: bool = False) -> None:
        """
        Write the buffered data to the DataRobot file system if force is True.

        Notes
        -----
        Since DataRobot file system does not support multipart uploads,
        calling flush without force does not upload any data.

        Parameters
        ----------
        force:
            Whether to force flush and upload data. Disallows further writing to this file.

        Raises
        ------
        ValueError
            If the file is closed or if force flush has already been called.
        """
        if self.closed:
            raise ValueError("Flush on closed file")
        if force and self.forced:
            raise ValueError("Force flush cannot be called more than once")
        if force:
            self.forced = True

        if self.readable():
            # no-op to flush on read-mode
            return

        if self.offset is None:
            self.offset = 0

        if self._upload_chunk(final=force) is not False:
            self.offset += self.buffer.seek(0, 2)  # Add size of buffer to offset
            self.buffer = io.BytesIO()  # Reset buffer after upload

    def upload(self) -> None:
        """Alias of ``flush(force=True)``."""
        self.flush(force=True)

    def close(self) -> None:
        """Close file. Finalizes writes, discards cache."""
        try:
            super().close()
        finally:
            if self.mode in self.WRITE_MODES:
                self.buffer.close()

            if self._temp_file_cache_path is not None:
                try:
                    os.remove(self._temp_file_cache_path)
                except (OSError, FileNotFoundError):
                    pass  # File may already be deleted
            self._temp_file_cache_path = None

            if self._read_client is not None and not self.is_datarobot_url_for_read:
                self._read_client.close()

    def __del__(self) -> None:
        try:
            self.close()
        except Exception:
            pass  # Avoid raising exceptions during garbage collection

    @property
    def url(self) -> str:
        """A signed URL for the file."""
        now = time.time()
        if self._cached_url is None or now >= self.__url_cache_expiry:
            self._cached_url = self.fs.sign(
                self.path,
                expiration=self.SIGNED_URL_EXPIRATION_SECONDS,
                version_id=self.version_id,
            )
            self.__url_cache_expiry = now + math.floor(self.SIGNED_URL_EXPIRATION_SECONDS * 0.9)

        return self._cached_url

    @property
    def use_range_headers(self) -> bool:
        """Whether to use range headers when reading data from file URL."""
        if self._supports_range_requests is None:
            self._supports_range_requests = supports_range_requests(self.url, client=self.read_client)
        return self._supports_range_requests

    @property
    def is_datarobot_url_for_read(self) -> bool:
        """Whether the file URL is a DataRobot URL."""
        if self._is_datarobot_url_for_read is None:
            self._is_datarobot_url_for_read = is_datarobot_url(self.url)
        return self._is_datarobot_url_for_read

    @property
    def read_client(self) -> requests.Session:
        """
        Session client to use for reading data from file URL.
        Supports unauthenticated clients for URLs outside DataRobot with embedded authentication.
        """
        if self._read_client is None:
            if self.is_datarobot_url_for_read:
                self._read_client = Files._client
            else:
                client = requests.Session()
                retry_strategy = Retry(
                    total=3,
                    backoff_factor=0.5,
                    status_forcelist=[
                        500,
                        502,
                        503,
                        504,
                    ],  # Retry on these status codes
                    allowed_methods=["GET"],  # Only retry safe methods
                )
                adapter = HTTPAdapter(max_retries=retry_strategy)
                client.mount("http://", adapter)
                client.mount("https://", adapter)
                self._read_client = client
        return self._read_client


class DataRobotFSMap(FSMap):  # type: ignore[misc]
    """
    Wrap a :class:`DataRobotFileSystem <datarobot.fs.file_system.DataRobotFileSystem>`
    instance as a mutable mapping.

    The keys of the mapping become files under the given root, and the
    values (which must be bytes) the contents of those files.

    Parameters
    ----------
    root: str
        The root path in the DataRobot file system to create the mapper for.
    fs: :class:`DataRobotFileSystem <datarobot.fs.file_system.DataRobotFileSystem>`
        The DataRobot file system instance.
    missing_exceptions: Optional[Tuple[Type[Exception], ...]]
        Exceptions to convert to KeyError when accessing the file system.

    Examples
    --------
    .. code-block:: python

        >>> from datarobot.fs import DataRobotFileSystem, DataRobotFSMap
        >>> fs = DataRobotFileSystem()
        >>> map = DataRobotFSMap("dr://696935d6d5a04a752419cf6d/", fs)

    Retrieve file contents from file system using map:

    .. code-block:: python

        >>> map["file.txt"]
        b"Hello, world!"
        >>> "folder/path/file.txt" in map
        True
        >>> file_count = len(map)
        >>> file_count
        3
        >>> [file for file in map]
        ["file.txt", "folder/path/file.txt", "another/folder/file.txt"]
        >>> map.getitems(["file.txt", "folder/path/file.txt", "another/folder/file.txt"])
        {
            "file.txt": b"Hello, world!",
            "folder/path/file.txt": b"Hello, world!",
            "another/folder/file.txt": b"Hello, world!",
        }

    Set file contents in file system using map:

    .. code-block:: python

        >>> map["file.txt"] = b"Hello, world!"
        >>> map["folder/path/new_file.txt"] = b"This is a new file!"
        >>> map.setitems({
            "another/folder/file.txt": b"Hello, world!",
            "folder/path/new_file.txt": b"This is a new file!",
        })

    Delete files from file system using map:

    .. code-block:: python

        >>> del map["file.txt"]
        >>> map.delitems(["folder/path/new_file.txt", "another/folder/file.txt"])
        >>> map.pop("file.txt", "default_value_if_file_does_not_exist")
        b'Hello, world!'
        >>> map.pop("folder/path/non_existent_file.txt", "default_value_if_file_does_not_exist")
        'default_value_if_file_does_not_exist'

    Clear all files under the map root directory. This may have unintended consequences as
    DataRobot file system does not support empty directories:

    .. code-block:: python

        >>> map.clear()
        >>> len(map)
        0
    """

    def __init__(
        self,
        root: str,
        fs: DataRobotFileSystem,
        missing_exceptions: Optional[Tuple[Type[Exception], ...]] = None,
    ):
        super().__init__(
            root=root,
            fs=fs,
            check=False,  # Can write everywhere except root
            create=False,  # Cannot create empty directories
            missing_exceptions=missing_exceptions,
        )
        self.fs: DataRobotFileSystem
        self.root: str

    def clear(self) -> None:
        """
        Remove all keys below root. Empties out the mapping.

        Notes
        -----
        May delete more directories than expected as DataRobot
        file system does not support empty directories.
        """
        try:
            self.fs.rm(f"{self.root.rstrip('/')}/*", recursive=True)
        except Exception:
            pass

    def __setitem__(self, key: str, value: bytes) -> None:
        """Store value in key"""
        key = self._key_to_str(key)
        self.fs.pipe_file(key, maybe_convert(value))
