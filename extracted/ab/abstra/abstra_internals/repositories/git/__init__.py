from .native import NativeGitRepository
from .types import (
    AheadBehindInfo,
    CleanupResult,
    GitCommit,
    GitRepositoryInterface,
    GitStatus,
    GitStatusResponse,
    LargeFileInfo,
    MaintenanceResult,
    RemoteGitStatus,
)


def create_git_repository(working_directory) -> GitRepositoryInterface:
    return NativeGitRepository(working_directory)


__all__ = [
    "AheadBehindInfo",
    "CleanupResult",
    "GitCommit",
    "GitRepositoryInterface",
    "GitStatus",
    "GitStatusResponse",
    "LargeFileInfo",
    "MaintenanceResult",
    "NativeGitRepository",
    "RemoteGitStatus",
    "create_git_repository",
]
