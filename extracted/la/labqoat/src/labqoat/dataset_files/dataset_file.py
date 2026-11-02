"""Immutable membership of one dataset file."""

from dataclasses import dataclass

from labqoat.references import AssetRef
from labqoat.storage.verified_file import VerifiedFile


@dataclass(frozen=True, slots=True, kw_only=True)
class DatasetFile:
    """A safe relative path bound to exact immutable asset bytes."""

    path: str
    asset: AssetRef

    def __post_init__(self) -> None:
        """Reject paths that could escape a materialized dataset."""
        VerifiedFile.relative(self.path)
