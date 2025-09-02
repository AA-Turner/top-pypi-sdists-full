#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import pathlib
import re
import unicodedata
from datetime import datetime, timezone

from pendingai import config


def format_filesize(num_bytes: int | float, suffix: str = "B") -> str:
    """
    Format a number of bytes into a human readable format.

    Args:
        num_bytes (int | float): Number of bytes to convert.
        suffix (str, optional): Suffix for output unit. Defaults to "B".

    Returns:
        str: Human readable filesize.
    """
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:3.1f}{unit}{suffix}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f}Yi{suffix}"


def format_filename(filename: str) -> str:
    """
    Format a filename into a sanitized string.

    Args:
        filename (str): File basename to sanitize.

    Returns:
        str: Sanitized filename.
    """
    filename = (
        unicodedata.normalize("NFKD", filename).encode("ascii", "ignore").decode("ascii")
    )
    filename = re.sub(r"[^\.\w\s-]", "", filename.lower())
    return re.sub(r"[-\.\s]+", "_", filename).strip("-_")


def localize_datetime(dt: datetime) -> datetime:
    """
    Localize a datetime timestamp into timezone-considerate UTC with
    offset +00:00 and then cast to the local timezone for the user.

    Args:
        dt (datetime): Datetime object.

    Returns:
        datetime: Datetime object with local timezone.
    """
    return dt.replace(tzinfo=timezone.utc).astimezone(config.TZ_LOCAL)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to be valid across Windows, macOS, and Linux.

    Args:
        filename (str): The filename to sanitize

    Returns:
        str: A sanitized filename that's safe to use on all platforms
    """
    # Normalize unicode characters
    filename = (
        unicodedata.normalize("NFKD", filename).encode("ascii", "ignore").decode("ascii")
    )

    # Replace characters that are invalid across platforms
    # Windows doesn't allow: \ / : * ? " < > |
    # macOS doesn't allow: : / (and files starting with .)
    # Linux doesn't technically restrict characters except / and null bytes
    invalid_chars: str = r'[\\/*?:"<>|]'
    filename = re.sub(invalid_chars, "-", filename)

    # Replace control characters and other problematic characters
    filename = re.sub(r"[\x00-\x1f\x7f]", "", filename)

    # Ensure the filename isn't just whitespace or dots
    filename = filename.strip(". \t\n\r")

    # If filename is empty after sanitization, provide a default
    if not filename:
        filename = "unnamed_file"

    return filename


def create_timestamped_filename(prefix: str, extension: str = ".json") -> pathlib.Path:
    """
    Creates a timestamped filename with proper sanitization.

    Args:
        prefix (str): Prefix for the filename
        extension (str): File extension (including the dot)

    Returns:
        pathlib.Path: A Path object with the sanitized filename
    """
    # Use hyphens instead of colons in the timestamp
    timestamp: str = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename: str = f"{prefix}_{timestamp}{extension}"
    return pathlib.Path(filename)
