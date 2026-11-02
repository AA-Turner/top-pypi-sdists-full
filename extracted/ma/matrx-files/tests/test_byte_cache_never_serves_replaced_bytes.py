"""A replace on one server process must not leave another process serving the file's OLD bytes.

Live walk 3: Document properties saved a new version, then read back empty (the read hit this process's byte
cache, filled before the edit by a different process). The cache now misses when the row's current version or
size no longer matches what the cached bytes belong to.
"""

from matrx_files.cloud_sync.byte_cache import FileByteCache


def test_old_bytes_miss_once_the_row_moved_to_a_newer_version() -> None:
    cache = FileByteCache()
    cache.put("f1", bytes_=b"old pdf bytes", version=3)
    assert cache.get("f1", version=3) is not None
    assert cache.get("f1", version=4) is None  # the row is at v4 now: the cached v3 bytes are stale
    assert cache.get("f1", version=4) is None  # and they were dropped, not kept for the next reader


def test_old_bytes_miss_when_the_size_changed_even_without_a_version() -> None:
    cache = FileByteCache()
    cache.put("f2", bytes_=b"x" * 10)
    assert cache.get("f2", size_bytes=10) is not None
    assert cache.get("f2", size_bytes=11) is None


def test_a_caller_without_row_facts_still_hits() -> None:
    cache = FileByteCache()
    cache.put("f3", bytes_=b"abc", version=1)
    assert cache.get("f3") is not None
