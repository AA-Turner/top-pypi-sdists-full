"""Response models."""
from pathlib import Path
from pydantic import BaseModel


class DeletedFilesR(BaseModel):
    """Deleted files summary."""

    path: Path
    pattern: str
    older_than_days: int
    recursive: bool
    number_of_deleted_files: int
    deleted_files: list[Path]