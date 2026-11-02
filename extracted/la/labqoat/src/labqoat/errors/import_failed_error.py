"""A terminal dataset import failure before publication admission."""

from labqoat._generated.dataset_import import DatasetImport
from labqoat.errors.api_error import ApiError


class ImportFailedError(ApiError):
    """Retain the import identity, pinned source and structured failure evidence."""

    def __init__(self, record: DatasetImport) -> None:
        """Expose the failed import so callers can inspect its preparation failure."""
        super().__init__(f"Dataset import {record.id} failed: {record.failure}")
        self.record = record
