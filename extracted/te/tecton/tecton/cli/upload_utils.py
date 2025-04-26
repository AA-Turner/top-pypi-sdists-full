import math
from dataclasses import dataclass
from pathlib import Path
from typing import List


# boto3 defaults to 8MB for multi-part uploads using upload_file.
DEFAULT_UPLOAD_PART_SIZE_MB = 16

# 5 was arbitrarily selected. We want to be conservative as this will run in customer's environments
DEFAULT_MAX_WORKERS_THREADS = 5

MEGABYTE = 1024 * 1024
GIGABYTE = 1024 * MEGABYTE


@dataclass
class UploadPart:
    """
    Represents an individual part of a file that needs to be uploaded in chunks or parts.
    :param part_number (int): The 1-indexed number of the part to be uploaded.
    :param offset (int): The starting byte offset of this part in the file.
    :param part_size (int): The size of this part in bytes.
    """

    part_number: int
    offset: int
    part_size: int


def _calculate_part_count(file_size: int, part_size_mb: int) -> int:
    """Calculate the number of parts the file will be divided into for uploading.

    Args:
        file_size (int): The size of the file
        part_size_mb (int): The size of each part in megabytes.

    Returns:
        int: The total number of parts.
    """
    chunk_size = part_size_mb * 1024 * 1024
    return int(math.ceil(file_size / chunk_size))


def get_upload_parts(file_size: int) -> List[UploadPart]:
    """
    Calculate UploadPart for each part of a file to be uploaded, given total file size.
    It considers the DEFAULT_UPLOAD_PART_SIZE_MB as the maximum size of each part.

    Args:
        file_size (int): The total size of the file being uploaded in bytes.

    Returns:
        List[UploadPart]: An list of UploadPart representing all parts to be uploaded with its part number,
                    starting offset, and size in bytes.
    """
    total_parts = _calculate_part_count(file_size, DEFAULT_UPLOAD_PART_SIZE_MB)
    chunk_size = DEFAULT_UPLOAD_PART_SIZE_MB * MEGABYTE
    upload_parts = []
    for i in range(1, total_parts + 1):
        offset = chunk_size * (i - 1)
        bytes_remaining = file_size - offset
        # Adjust the size for the last part if the remaining bytes are less than the DEFAULT_UPLOAD_PART_SIZE_MB
        current_chunk_size = chunk_size if bytes_remaining > chunk_size else bytes_remaining
        upload_parts.append(UploadPart(part_number=i, offset=offset, part_size=current_chunk_size))
    return upload_parts


def _get_directory_size(directory: Path) -> int:
    """
    Compute the size of a directory in bytes.

    Args:
        directory (Path): The directory path for which to compute the size.

    Returns:
        int: The size of the directory in bytes.
    """
    return sum(f.stat().st_size for f in directory.rglob("*") if f.is_file())
