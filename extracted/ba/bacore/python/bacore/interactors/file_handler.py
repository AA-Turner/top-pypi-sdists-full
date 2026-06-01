"""File handling interactors."""

import subprocess as sup
from bacore.domain.responses import DeletedFilesR
from bacore.domain.protocols import SupportsRetrieveDict
from datetime import datetime, timedelta
from pathlib import Path
from pydantic import Field, validate_call
from typing import Annotated, Optional


def get_files_in_dir(directory: Path, recursive: bool, pattern: str = "*") -> list[Path]:
    """Get list of files as path objects from a directory matching a pattern.

    Args:
        `directory` (Path): The directory to search in.
        `recursive` (bool): Whether to search recursively.
        `pattern` (str): The pattern to match files against.

    Returns:
        `list[Path`: A list of Path objects for each file found.
    """
    find_function = directory.rglob if recursive else directory.glob

    return [file_path for file_path in find_function(pattern) if file_path.is_file()]


@validate_call
def delete_files(
    path: Path,
    pattern: str = "*",
    older_than_days: Annotated[int, Field(ge=0)] = 0,
    recursive: bool = False,
) -> DeletedFilesR:
    """Delete files older than x days.

    Args:
        path (`Path`): Path to search for files.
        pattern (`str`): Pattern to search for files.
        older_than_days (`int`): Delete files older than x dyas. Default is `0`. Negative values are not allowed.
        recursive (`bool`): Optionally delete files recursively. Default is `False`.
    """
    number_of_deleted_files = 0
    deleted_files = []
    now = datetime.now()
    files_matching_pattern = get_files_in_dir(directory=path, recursive=recursive, pattern=pattern)

    for file in files_matching_pattern:
        file_modification_time = file.stat().st_mtime

        if file_modification_time < (now - timedelta(days=older_than_days)).timestamp():
            file.unlink()
            deleted_files.append(file)
            number_of_deleted_files += 1

    return DeletedFilesR(
        path=path,
        pattern=pattern,
        older_than_days=older_than_days,
        recursive=recursive,
        number_of_deleted_files=number_of_deleted_files,
        deleted_files=deleted_files,
    )


def file_as_dict(file: SupportsRetrieveDict) -> dict:
    """Content as dictionary."""
    return file.data_to_dict()


def rsync_copy(source: Path, destination: Path, file_filter: Optional[str]):
    """Use rsync to mirror files and folders from src to dest."""
    command = ["rsync", "-av", "--delete", f"{source}/{file_filter}", str(destination)]
    try:
        sup.run(command, check=True)
    except FileNotFoundError:
        raise FileNotFoundError("Unable to find file or directory to copy.")
    except sup.CalledProcessError as e:
        raise RuntimeError(f"Rsync failed: {e}")
