"""Scoped local files for authored model and evaluation consumers."""

from collections.abc import Mapping
from contextlib import AbstractContextManager
from pathlib import Path
from typing import Protocol

from labqoat.references import AssetRef


class FileAccess(Protocol):
    """Protect exact bytes from cache eviction for the duration of consumption."""

    def local_file(self, reference: AssetRef | Mapping[str, object]) -> AbstractContextManager[Path]:
        """Acquire an immutable asset reference without retaining it beyond this scope."""
        ...
