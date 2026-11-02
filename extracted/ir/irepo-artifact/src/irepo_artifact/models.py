"""Public download result types."""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from .errors import ArtifactError


@dataclass(frozen=True)
class DownloadTarget:
    url: str = field(repr=False)
    expires_in: float | None = None


@dataclass(frozen=True)
class DownloadResult:
    job_id: str
    job_dir: Path
    archive_path: Path | None
    files_dir: Path | None
    files: tuple[Path, ...]
    channel: Literal['oss', 'proxy'] | None
    status: Literal['success', 'missing', 'no_match', 'failed']
    error: ArtifactError | None = None

    artifacts_response: dict | None = field(default=None, repr=False)
    manifest_response: dict | None = field(default=None, repr=False)
