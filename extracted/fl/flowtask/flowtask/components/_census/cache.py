"""
Parquet-backed disk cache for Census API responses.

Cache layout::

    ~/.flowtask/cache/census/<year>/<dataset>/<table>_<geo>[_<state>].parquet

Writes are atomic (write-to-temp then ``os.replace``).  On non-writable
directories the write is silently skipped (warning logged).  On corrupted
parquet files the file is deleted and ``None`` is returned (warning logged).
"""

from __future__ import annotations

import logging
import os
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from flowtask.components._census.resolver import CacheKey

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def default_cache_dir() -> Path:
    """Return the default Census cache directory.

    Returns:
        ``~/.flowtask/cache/census`` as a :class:`pathlib.Path`.
    """
    return Path.home() / ".flowtask" / "cache" / "census"


def cache_path(key: "CacheKey", cache_dir: Path) -> Path:
    """Compute the parquet file path for a given cache key.

    Args:
        key: A :class:`~flowtask.components._census.resolver.CacheKey` instance.
        cache_dir: The root cache directory.

    Returns:
        The full path to the parquet file, e.g.
        ``<cache_dir>/2024/acs/acs5/profile/DP05_zcta.parquet`` or
        ``<cache_dir>/2024/acs/acs5/profile/DP05_county_06.parquet``.
    """
    # Encode the dataset path (slashes become directory separators).
    dataset_parts = key.dataset.replace("/", os.sep)
    filename_parts = [key.table, key.geography]
    if key.state is not None:
        filename_parts.append(key.state)
    filename = "_".join(filename_parts) + ".parquet"
    return cache_dir / str(key.year) / dataset_parts / filename


def cache_read(
    key: "CacheKey",
    cache_dir: Path,
    logger: logging.Logger,
) -> pd.DataFrame | None:
    """Read a cached DataFrame from disk.

    Args:
        key: The cache key identifying the shard.
        cache_dir: The root cache directory.
        logger: A logger instance for warning messages.

    Returns:
        The cached :class:`pandas.DataFrame`, or ``None`` if the cache file
        does not exist or is corrupted (in which case the corrupted file is
        deleted).
    """
    path = cache_path(key, cache_dir)
    if not path.exists():
        return None

    try:
        return pd.read_parquet(path, engine="pyarrow")
    except Exception as exc:  # noqa: BLE001
        logger.warning(
            "Corrupted cache file '%s': %s.  Deleting and re-fetching.",
            path,
            exc,
        )
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass
        return None


def cache_write(
    df: pd.DataFrame,
    key: "CacheKey",
    cache_dir: Path,
    logger: logging.Logger,
) -> None:
    """Write a DataFrame to the parquet cache atomically.

    The file is written to a temporary path first and then renamed into place
    so that partially-written files cannot poison future reads.

    If the target directory is not writable, a warning is logged and the
    function returns without raising.

    Args:
        df: The DataFrame to cache.
        key: The cache key identifying the shard.
        cache_dir: The root cache directory.
        logger: A logger instance for warning messages.
    """
    path = cache_path(key, cache_dir)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        logger.warning(
            "Cannot create cache directory '%s': %s.  Cache write skipped.",
            path.parent,
            exc,
        )
        return

    # Write atomically: temp file → rename.
    tmp_path: Path | None = None
    try:
        fd, tmp_str = tempfile.mkstemp(
            dir=path.parent,
            prefix=path.stem + ".",
            suffix=".tmp.parquet",
        )
        os.close(fd)
        tmp_path = Path(tmp_str)
        df.to_parquet(tmp_path, engine="pyarrow", index=False)
        os.replace(tmp_path, path)
        logger.debug("Cache written: %s", path)
    except OSError as exc:
        logger.warning(
            "Cannot write cache file '%s': %s.  Cache write skipped.",
            path,
            exc,
        )
        if tmp_path is not None and tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass
    except Exception as exc:  # noqa: BLE001
        logger.warning(
            "Unexpected error writing cache '%s': %s.  Cache write skipped.",
            path,
            exc,
        )
        if tmp_path is not None and tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass
