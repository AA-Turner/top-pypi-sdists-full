"""Explicit failure when authored code lacks file access capabilities."""

from collections.abc import Mapping
from contextlib import AbstractContextManager
from pathlib import Path

from labqoat.references import AssetRef


class UnavailableFileAccess:
    """Keep default offline contexts cheap and free of implicit credential lookup."""

    def local_file(self, reference: AssetRef | Mapping[str, object]) -> AbstractContextManager[Path]:
        """Require the execution host to inject an authorized file provider."""
        del reference
        raise ValueError("File access is unavailable in this context")
