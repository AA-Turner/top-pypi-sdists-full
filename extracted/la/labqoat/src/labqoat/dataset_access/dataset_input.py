"""A locally pinned dataset and its immutable file inventory."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from labqoat.dataset_files import DatasetFileManifest
from labqoat.references import ResolvedDatasetRef

if TYPE_CHECKING:
    from labqoat.dataset_access.revision_files import RevisionFiles


@dataclass(frozen=True, slots=True)
class DatasetInput:
    """An explicit local directory carrying one exact dataset revision."""

    root: Path
    revision: RevisionFiles

    @property
    def reference(self) -> ResolvedDatasetRef[object]:
        """Retain the exact execution pin bound to these captured documents."""
        return self.revision.reference

    @property
    def manifest(self) -> DatasetFileManifest:
        """Expose only verified materialized part membership."""
        return self.revision.manifest
