from __future__ import annotations

import fcntl
import logging
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from torch.utils.cpp_extension import _get_build_directory, load

logger = logging.getLogger(__name__)

_STALE_LOCK_MAX_AGE_SEC = 15 * 60
_LOCK_RACE_RETRY_COUNT = 5
_LOCK_RACE_RETRY_SEC = 0.2


def _build_dir(name: str) -> Path:
    return Path(_get_build_directory(name, verbose=False))


def _extension_path(name: str) -> Path:
    return _build_dir(name) / f"{name}.so"


def _is_partial_extension_import_error(name: str, exc: ImportError) -> bool:
    return "file too short" in str(exc) and str(_extension_path(name)) in str(exc)


@contextmanager
def _host_build_lock(name: str):
    build_dir = Path(_get_build_directory(name, verbose=False))
    build_dir.mkdir(parents=True, exist_ok=True)
    lock_path = build_dir / f"{name}.host.lock"
    with lock_path.open("w") as lock_handle:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)


def _maybe_clear_stale_lock(name: str) -> None:
    build_dir = _build_dir(name)
    lock_path = build_dir / "lock"
    if not lock_path.exists():
        return

    extension_path = _extension_path(name)
    if extension_path.exists():
        logger.warning(
            "Removing torch extension lock for %s at %s because compiled extension %s already exists",
            name,
            lock_path,
            extension_path,
        )
        lock_path.unlink(missing_ok=True)
        return
    try:
        lock_age_sec = time.time() - lock_path.stat().st_mtime
    except FileNotFoundError:
        return

    if lock_age_sec <= _STALE_LOCK_MAX_AGE_SEC:
        return

    logger.warning(
        "Removing old torch extension lock for %s at %s (age %.1fs)",
        name,
        lock_path,
        lock_age_sec,
    )
    lock_path.unlink(missing_ok=True)


def safe_load_extension(
    *,
    name: str,
    sources: list[str],
    extra_cflags: list[str] | None = None,
    extra_cuda_cflags: list[str] | None = None,
    extra_include_paths: list[str] | None = None,
    verbose: bool = False,
) -> Any:
    with _host_build_lock(name):
        for attempt in range(_LOCK_RACE_RETRY_COUNT):
            _maybe_clear_stale_lock(name)
            try:
                return load(
                    name=name,
                    sources=sources,
                    extra_cflags=extra_cflags,
                    extra_cuda_cflags=extra_cuda_cflags,
                    extra_include_paths=extra_include_paths,
                    build_directory=None,
                    verbose=verbose,
                )
            except FileNotFoundError as exc:
                if Path(exc.filename or "").name != "lock" or attempt + 1 >= _LOCK_RACE_RETRY_COUNT:
                    raise
                logger.warning(
                    "Retrying torch extension load for %s after transient lock-file race (%d/%d)",
                    name,
                    attempt + 1,
                    _LOCK_RACE_RETRY_COUNT,
                )
                time.sleep(_LOCK_RACE_RETRY_SEC)
            except ImportError as exc:
                if not _is_partial_extension_import_error(name, exc) or attempt + 1 >= _LOCK_RACE_RETRY_COUNT:
                    raise
                logger.warning(
                    "Retrying torch extension load for %s after partial extension import race (%d/%d)",
                    name,
                    attempt + 1,
                    _LOCK_RACE_RETRY_COUNT,
                )
                time.sleep(_LOCK_RACE_RETRY_SEC)
    raise AssertionError("safe_load_extension retry loop exited unexpectedly")


__all__ = ["safe_load_extension"]
