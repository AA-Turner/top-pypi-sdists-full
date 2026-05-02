"""
Task Storage.

Saving Tasks on different Storages (Filesystem, S3 buckets, databases, etc)
"""

from .filesystem import FileTaskStorage
from .database import DatabaseTaskStorage
from .row import RowTaskStorage
from .memory import MemoryTaskStorage


def __getattr__(name: str):
    if name == "GitTaskStorage":
        from .github import GitTaskStorage
        globals()["GitTaskStorage"] = GitTaskStorage
        return GitTaskStorage
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    "FileTaskStorage",
    "DatabaseTaskStorage",
    "RowTaskStorage",
    "GitTaskStorage",
    "MemoryTaskStorage",
)
