"""open_files: this process's RLIMIT_NOFILE, raised once by the processes that hold many files."""

from probe.foundation.open_files.open_files import MAX_OPEN_FILES, raise_open_files

__all__ = ["MAX_OPEN_FILES", "raise_open_files"]
