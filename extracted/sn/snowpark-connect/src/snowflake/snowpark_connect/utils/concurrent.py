#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import threading
from collections.abc import Mapping
from copy import copy
from typing import Callable, TypeVar

K = TypeVar("K")
V = TypeVar("V")
T = TypeVar("T")


class SynchronizedDict(Mapping[K, V]):
    def __init__(self, in_dict: dict[K, V] | None = None) -> None:
        self._lock = ReadWriteLock()
        self._dict = in_dict if in_dict is not None else {}

    def get(self, key: K, default=None) -> V:
        with self._lock.reader():
            return self._dict.get(key, default)

    def set(self, key: K, value) -> None:
        with self._lock.writer():
            self._dict[key] = value

    def remove(self, key) -> V | None:
        with self._lock.writer():
            return self._dict.pop(key, None)

    def items(self) -> list[tuple[K, V]]:
        with self._lock.reader():
            return list(self._dict.items())

    def keys(self) -> list[K]:
        with self._lock.reader():
            return list(self._dict.keys())

    def values(self) -> list[V]:
        with self._lock.reader():
            return list(self._dict.values())

    def copy(self) -> dict[K, V]:
        with self._lock.reader():
            return copy(self._dict)

    def __getitem__(self, key: K) -> V:
        with self._lock.reader():
            return self._dict[key]

    def __setitem__(self, key: K, value: V) -> None:
        with self._lock.writer():
            self._dict[key] = value

    def __delitem__(self, key: K) -> None:
        with self._lock.writer():
            del self._dict[key]

    def __contains__(self, key: K) -> bool:
        with self._lock.reader():
            return key in self._dict

    def __len__(self) -> int:
        with self._lock.reader():
            return len(self._dict)

    def __iter__(self):
        with self._lock.reader():
            return iter(list(self._dict.items()))

    def clear(self) -> None:
        with self._lock.writer():
            self._dict.clear()


class SynchronizedList:
    def __init__(self, in_list: list[T] | None = None) -> None:
        self._lock = ReadWriteLock()
        self._list = in_list if in_list is not None else []

    def append(self, item: T) -> None:
        with self._lock.writer():
            self._list.append(item)

    def clear(self) -> None:
        with self._lock.writer():
            self._list.clear()

    def copy(self) -> list[T]:
        with self._lock.reader():
            return self._list.copy()

    def filter(self, predicate: Callable[[T], bool]) -> None:
        with self._lock.writer():
            self._list = [item for item in self._list if predicate(item)]

    def __len__(self) -> int:
        with self._lock.reader():
            return len(self._list)

    def __iter__(self):
        with self._lock.reader():
            return iter(self._list.copy())


class ReadWriteLock:
    class _Reader:
        def __init__(self, lock) -> None:
            self._lock = lock

        def __enter__(self) -> None:
            self._lock.acquire_read()

        def __exit__(self, exc_type, exc_val, exc_tb) -> None:
            self._lock.release_read()

    class _Writer:
        def __init__(self, lock) -> None:
            self._lock = lock

        def __enter__(self) -> None:
            self._lock.acquire_write()

        def __exit__(self, exc_type, exc_val, exc_tb) -> None:
            self._lock.release_write()

    def __init__(self) -> None:
        self._readers = 0
        self._is_writer = False
        self._lock = threading.Lock()
        self._read_ready = threading.Condition(self._lock)
        self._reader = self._Reader(self)
        self._writer = self._Writer(self)

    def reader(self) -> _Reader:
        return self._reader

    def writer(self) -> _Writer:
        return self._writer

    def acquire_read(self) -> None:
        with self._read_ready:
            while self._is_writer:
                self._read_ready.wait()
            self._readers += 1

    def release_read(self) -> None:
        with self._read_ready:
            self._readers -= 1
            if self._readers == 0:
                self._read_ready.notify_all()

    def acquire_write(self) -> None:
        with self._read_ready:
            while self._is_writer or self._readers > 0:
                self._read_ready.wait()
            self._is_writer = True

    def release_write(self) -> None:
        with self._read_ready:
            self._is_writer = False
            self._read_ready.notify_all()
