"""
"""

import contextlib
from bisect import bisect_right
from pathlib import Path
from typing import Generic
from typing import TypeVar

from ..config import Config
from .utils import read_map_files


T = TypeVar('T')


class RangeMap(Generic[T]):
    def __init__(self):
        self._starts: list[int] = []
        self._ranges: list[tuple[int, T]] = []
    def __setitem__(self, key: slice, value):
        i = bisect_right(self._starts, key.start)
        self._starts.insert(i, key.start)
        self._ranges.insert(i, (key.stop, value))
    def get(self, addr: int):
        i = bisect_right(self._starts, addr) - 1
        if i >= 0:
            end, value = self._ranges[i]
            if addr < end:
                return value


@contextlib.contextmanager
def unmap_capture(mmap_addrs: list[int]):
    rm: RangeMap[Path] = RangeMap()
    for range_str, path in read_map_files():
        start_hex, end_hex = range_str.split('-')
        rm[int(start_hex, 16):int(end_hex, 16)] = path
    tensor_files: set[Path] = set()
    for addr in mmap_addrs:
        if (path := rm.get(addr)) is not None:
            if path.match(Config.zerogpu_mmap_autoprune_pattern):
                tensor_files |= {path}
    unmapped_paths: list[Path] = []
    yield unmapped_paths
    for path in tensor_files - {path for _, path in read_map_files()}:
        unmapped_paths.append(path)
