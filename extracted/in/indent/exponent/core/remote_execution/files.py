import os
from asyncio import to_thread
from typing import Final, cast

from anyio import Path as AsyncPath
from python_ripgrep import PySortMode, PySortModeKind, files, search

from exponent.core.remote_execution.cli_rpc_types import ErrorToolResult, GrepToolResult
from exponent.core.remote_execution.types import (
    FilePath,
    RemoteFile,
)
from exponent.core.remote_execution.utils import safe_read_file

MAX_MATCHING_FILES: Final[int] = 10
FILE_NOT_FOUND: Final[str] = "File {} does not exist"
MAX_FILES_TO_WALK: Final[int] = 10_000

GLOB_MAX_COUNT: Final[int] = 1000
GREP_MAX_RESULTS = 100


class FileCache:
    """A cache of the files in a working directory.

    Args:
        working_directory: The working directory to cache the files from.
    """

    def __init__(self, working_directory: str) -> None:
        self.working_directory = working_directory
        self._cache: list[str] | None = None

    async def get_files(self) -> list[str]:
        """Get the files in the working directory.

        Returns:
            A list of file paths in the working directory.
        """
        if self._cache is None:
            self._cache = await file_walk(self.working_directory)

        return self._cache


async def get_file_content(
    absolute_path: FilePath, offset: int | None = None, limit: int | None = None
) -> tuple[str, bool]:
    """Get the content of the file at the specified path.

    Args:
        absolute_path: The absolute path to the file.

    Returns:
        A tuple containing the content of the file and a boolean indicating if the file exists.
    """
    file = AsyncPath(absolute_path)
    exists = await file.exists()

    if not exists:
        return FILE_NOT_FOUND.format(absolute_path), False

    if await file.is_dir():
        return "File is a directory", True

    content = await safe_read_file(file)

    if offset or limit:
        offset = offset or 0
        limit = limit or -1

        content_lines = content.splitlines()
        content_lines = content_lines[offset:]
        content_lines = content_lines[:limit]

        content = "\n".join(content_lines)

    return content, exists


async def search_files(
    path_str: str,
    file_pattern: str | None,
    regex: str,
    working_directory: str,
    multiline: bool | None = None,
) -> GrepToolResult | ErrorToolResult:
    path = AsyncPath(working_directory) / path_str

    if not await path.exists():
        return ErrorToolResult(
            error_message=f"Path does not exist: {path_str}",
        )

    path_resolved = await path.resolve()
    globs = [file_pattern] if file_pattern else None

    if globs:
        matched_files = await to_thread(
            files,
            patterns=[],
            paths=[str(path_resolved)],
            globs=globs,
            max_count=1,
        )
        if not matched_files:
            return ErrorToolResult(
                error_message=f"No files matched the include glob pattern: {file_pattern} at {path_str}",
            )

    try:
        results = await to_thread(
            search,
            patterns=[regex],
            paths=[str(path_resolved)],
            globs=globs,
            after_context=3,
            before_context=5,
            heading=True,
            separator_field_context="|",
            separator_field_match="|",
            separator_context="\n...\n",
            multiline=multiline,
        )
    except ValueError as e:
        # python_ripgrep raises ValueError for invalid regex patterns
        return ErrorToolResult(
            error_message=f"Invalid regex pattern: {e}",
        )

    return GrepToolResult(
        matches=results[:GREP_MAX_RESULTS],
        truncated=bool(len(results) > GREP_MAX_RESULTS),
    )


async def get_all_file_contents(
    working_directory: str,
) -> list[list[str]]:
    path_resolved = await AsyncPath(working_directory).resolve()

    results = await to_thread(
        search,
        patterns=[".*"],
        paths=[str(path_resolved)],
        globs=["!**/poetry.lock", "!**/pnpm-lock.yaml"],
        heading=True,
        line_number=False,
    )

    result_sizes = [len(result) for result in results]
    total_size = sum(result_sizes)
    batch_size = total_size // 10

    batches = []
    current_batch: list[str] = []
    current_size = 0

    for i, result in enumerate(results):
        if current_size + result_sizes[i] > batch_size:
            batches.append(current_batch)
            current_batch = []
            current_size = 0

        current_batch.append(result)
        current_size += result_sizes[i]

    batches.append(current_batch)

    return batches


async def normalize_files(
    working_directory: str, file_paths: list[FilePath]
) -> list[RemoteFile]:
    """Normalize file paths to be relative to the working directory.

    Args:
        working_directory: The working directory to normalize the file paths against.
        file_paths: A list of file paths to normalize.

    Returns:
        A list of RemoteFile objects with normalized file paths.
    """
    working_path = await AsyncPath(working_directory).resolve()
    normalized_files = []

    for file_path in file_paths:
        path = AsyncPath(file_path)

        if path.is_absolute():
            path = path.relative_to(working_path)

        normalized_files.append(
            RemoteFile(
                file_path=str(path),
                working_directory=working_directory,
            )
        )

    return sorted(normalized_files)


def _format_ignore_globs(ignore_extra: list[str] | None) -> list[str]:
    if ignore_extra is None:
        return []

    return [f"!**/{ignore}" for ignore in ignore_extra]


async def file_walk(
    directory: str,
    ignore_extra: list[str] | None = None,
    max_files: int = MAX_FILES_TO_WALK,
) -> list[str]:
    """
    Walk through a directory and return all file paths, respecting .gitignore and additional ignore patterns.

    Args:
        directory: The directory to walk through
        ignore_extra: Additional directory paths to ignore, follows the gitignore format.
        max_files: The maximal number of files to return

    Returns:
        A list of file paths in the directory.
    """
    working_path = str(await AsyncPath(directory).resolve())

    results: list[str] = await to_thread(
        files,
        patterns=[""],
        paths=[working_path],
        globs=_format_ignore_globs(ignore_extra),
        sort=PySortMode(kind=PySortModeKind.Path),
        max_count=max_files,
    )

    # Create relative paths using os.path functions which handle platform differences
    relative_results = []
    for result in results:
        # Check if the path is inside the working directory
        if os.path.commonpath([working_path, result]) == working_path:
            # Create relative path
            rel_path = os.path.relpath(result, working_path)
            relative_results.append(rel_path)
        else:
            # Fallback to just using the filename
            relative_results.append(os.path.basename(result))

    return relative_results


async def get_all_non_ignored_files(working_directory: str) -> list[RemoteFile]:
    file_paths = await file_walk(working_directory, ignore_extra=DEFAULT_IGNORES)

    return await normalize_files(working_directory, cast(list[FilePath], file_paths))


async def glob(
    path: str,
    glob_pattern: str,
) -> list[str]:
    return await to_thread(
        files,
        patterns=[],
        paths=[path],
        globs=[glob_pattern],
        sort=PySortMode(kind=PySortModeKind.Path),
        max_count=GLOB_MAX_COUNT,
    )


DEFAULT_IGNORES = [
    "**/.git/",
    ".venv/",
    ".mypy_cache",
    ".pytest_cache",
    "node_modules/",
    "venv/",
    ".pyenv",
    "__pycache__",
    ".ipynb_checkpoints",
    ".vercel",
    "__pycache__/",
    "*.py[cod]",
    "*$py.class",
    ".env",
    "*.so",
    ".Python",
    "build/",
    "develop-eggs/",
    "dist/",
    "downloads/",
    "eggs/",
    ".eggs/",
    "lib/",
    "lib64/",
    "parts/",
    "sdist/",
    "var/",
    "wheels/",
    "pip-wheel-metadata/",
    "share/python-wheels/",
    "*.egg-info/",
    ".installed.cfg",
    "*.egg",
    "MANIFEST",
]
