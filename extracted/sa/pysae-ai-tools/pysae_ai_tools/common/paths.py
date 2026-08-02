"""Portable filesystem paths for runtime scratch files."""

import tempfile
from pathlib import Path


def temp_path(name: str) -> Path:
    """Return ``name`` under the system temp directory.

    Uses ``tempfile.gettempdir()`` (honours ``TMPDIR`` and resolves to a valid
    location on every OS) instead of a hardcoded ``/tmp`` prefix, which does
    not exist on Windows.
    """
    return Path(tempfile.gettempdir()) / name
