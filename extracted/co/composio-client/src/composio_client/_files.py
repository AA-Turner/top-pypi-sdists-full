"""File helpers retained from the Stainless client surface."""

from __future__ import annotations

import os
from pathlib import Path

from ._types import FileTypes


def file_from_path(path: str) -> FileTypes:
    contents = Path(path).read_bytes()
    file_name = os.path.basename(path)
    return (file_name, contents)
