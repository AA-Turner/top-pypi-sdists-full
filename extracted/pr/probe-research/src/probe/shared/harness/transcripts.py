"""TranscriptLocator facet of HarnessIntegration: where one harness's transcripts live, which files are sessions, their id and cwd; env-var paths."""

from __future__ import annotations
import os
from pathlib import Path


def _env_path(name: str) -> Path | None:
    """An env var as a path, tilde expanded. None when unset or empty.

    `expanduser` because these are routinely set in a config file or quoted in
    a shell, where `~` arrives literally: without it the value becomes a
    RELATIVE path, `is_dir()` is false, and the honest "Looked in:" line would
    name a directory nothing ever searched.
    """
    raw = (os.environ.get(name) or "").strip()
    return Path(raw).expanduser() if raw else None
