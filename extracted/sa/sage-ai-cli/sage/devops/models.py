"""Shared models for SAGE DevOps modules."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any


class PipelineStatus(Enum):
    """Status of a CI/CD pipeline."""

    PENDING = auto()
    RUNNING = auto()
    SUCCESS = auto()
    FAILED = auto()
    CANCELLED = auto()
    UNKNOWN = auto()


class JobStatus(Enum):
    """Status of a CI/CD job."""

    PENDING = auto()
    RUNNING = auto()
    SUCCESS = auto()
    FAILED = auto()
    SKIPPED = auto()
    CANCELLED = auto()


@dataclass
class CIJob:
    """A CI/CD job."""

    name: str
    status: JobStatus
    duration_seconds: float | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    logs_url: str | None = None
    error_message: str | None = None


@dataclass
class CIPipeline:
    """A CI/CD pipeline run."""

    id: str
    status: PipelineStatus
    branch: str
    commit_sha: str
    jobs: list[CIJob] = field(default_factory=list)
    started_at: datetime | None = None
    finished_at: datetime | None = None
    url: str | None = None
    conclusion: str | None = None
    workflow_name: str = "unknown"
    head_branch: str = "unknown"

    @property
    def is_complete(self) -> bool:
        """Check if pipeline is complete."""
        return self.status in (
            PipelineStatus.SUCCESS,
            PipelineStatus.FAILED,
            PipelineStatus.CANCELLED,
        )

    @property
    def is_running(self) -> bool:
        """Check if pipeline is running."""
        return self.status == PipelineStatus.RUNNING

    @property
    def failed_jobs(self) -> list[CIJob]:
        """Get list of failed jobs."""
        return [j for j in self.jobs if j.status == JobStatus.FAILED]

    @property
    def jobs_failed(self) -> int:
        """Get count of failed jobs."""
        return len(self.failed_jobs)

    @property
    def head_sha(self) -> str:
        """Alias for commit_sha for backward compatibility."""
        return self.commit_sha


@dataclass
class GitStatus:
    """Git repository status."""

    branch: str
    is_clean: bool
    staged_files: list[str] = field(default_factory=list)
    modified_files: list[str] = field(default_factory=list)
    untracked_files: list[str] = field(default_factory=list)
    ahead: int = 0
    behind: int = 0

    @property
    def staged(self) -> list[str]:
        """Alias for staged_files."""
        return self.staged_files

    @property
    def modified(self) -> list[str]:
        """Alias for modified_files."""
        return self.modified_files

    @property
    def untracked(self) -> list[str]:
        """Alias for untracked_files."""
        return self.untracked_files


@dataclass
class GitCommit:
    """A git commit."""

    sha: str
    message: str
    author: str
    date: str


@dataclass
class GitResult:
    """Result of a git operation."""

    success: bool
    output: str = ""
    error: str = ""
    data: Any | None = None


@dataclass
class TestResult:
    """A test result."""

    name: str
    passed: bool
    duration_seconds: float | None = None
    error_message: str | None = None
    file_path: str | None = None
    line_number: int | None = None


@dataclass
class TestSummary:
    """Summary of test results."""

    total: int
    passed: int
    failed: int
    skipped: int
    duration_seconds: float | None = None
    results: list[TestResult] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Get test success rate as percentage."""
        if self.total == 0:
            return 100.0
        return (self.passed / self.total) * 100
