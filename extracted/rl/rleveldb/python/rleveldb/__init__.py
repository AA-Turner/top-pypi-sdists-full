"""
rleveldb — High-performance LevelDB reader.

Rust core with Python bindings via PyO3, similar to orjson's architecture.
Drop-in replacement for ccl_leveldb with significantly better performance.
"""

from rleveldb._rleveldb import (
    RawLevelDb,
    Record,
    KeyState,
    FileType,
)

__version__ = "1.0.0"
__all__ = [
    "RawLevelDb",
    "Record",
    "KeyState",
    "FileType",
]
