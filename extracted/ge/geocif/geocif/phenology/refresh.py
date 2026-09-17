"""Refresh the rainfall inputs the season monitor reads (DESIGN.md section 5).

The monitor needs CHIRPS through yesterday and the newest CHIRPS-GEFS issue.
Rather than duplicate geoprepare's download logic, this module builds the *same*
``params`` object ``geoprepare.geodownload.run`` builds and hands it straight to
``geoprepare.datasets.CHIRPS.run`` / ``CHIRPS_GEFS.run``.

Two guards stop a monitor run from fighting the nightly pipeline:

1. ``pgrep -af geodownload.run`` -- another download is already in flight.
   ``pgrep`` does not exist on Windows; a missing binary is treated as
   "nothing is running", not as an error.
2. A lock file ``${PATHS:dir_intermed}/.season_monitor_refresh.lock`` younger
   than :data:`LOCK_MAX_AGE_HOURS`.

:func:`refresh_inputs` **never raises**. A failed refresh is logged and the
monitor proceeds on whatever data is already on disk -- stale rain is far better
than no run.

Units: none of this module touches pixel values; it only moves files.
"""

from __future__ import annotations

import datetime as _dt
import importlib
import logging
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any, Optional, Sequence

logger = logging.getLogger(__name__)

#: Lock file name under ``[PATHS] dir_intermed``.
LOCK_NAME: str = ".season_monitor_refresh.lock"

#: A lock younger than this (hours) means "someone else just refreshed".
LOCK_MAX_AGE_HOURS: float = 6.0

#: Dataset name -> module under ``geoprepare.datasets``.
DATASET_MODULES: dict[str, str] = {
    "CHIRPS": "geoprepare.datasets.CHIRPS",
    "CHIRPS-GEFS": "geoprepare.datasets.CHIRPS_GEFS",
}

#: Process-table pattern that means a geoprepare download is already running.
DOWNLOAD_PROCESS_PATTERN: str = "geodownload.run"


def _default_years(today: Optional[_dt.date] = None) -> list[int]:
    """Years to refresh: the current one, plus the previous one in Jan-Feb.

    In January and February the previous year's CHIRPS is still being finalised
    (and ``redo_last_year`` is true in geoprepare for the same reason), so both
    years are refreshed.

    Args:
        today: override for tests; defaults to :meth:`datetime.date.today`.

    Returns:
        Ascending list of calendar years.
    """
    today = today or _dt.date.today()
    if today.month <= 2:
        return [today.year - 1, today.year]
    return [today.year]


def download_running(pattern: str = DOWNLOAD_PROCESS_PATTERN) -> bool:
    """True when ``pgrep -af <pattern>`` finds a live geoprepare download.

    A missing ``pgrep`` (Windows) or any failure to run it is reported as
    ``False`` -- we refuse to block a monitor run on an unanswerable question.

    Args:
        pattern: the process-table substring to look for.

    Returns:
        ``True`` only when pgrep ran and matched at least one process.
    """
    if shutil.which("pgrep") is None:
        logger.info("pgrep unavailable on this host; skipping the download-in-flight check")
        return False
    try:
        proc = subprocess.run(
            ["pgrep", "-af", pattern],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except Exception as exc:  # noqa: BLE001 - the guard must never be fatal
        logger.warning(f"pgrep check failed ({exc}); assuming no download is running")
        return False

    if proc.returncode == 0 and proc.stdout.strip():
        logger.warning(
            f"A geoprepare download is already running; skipping refresh:\n{proc.stdout.strip()}"
        )
        return True
    return False


def lock_path(parser) -> Path:
    """Path of the refresh lock file under ``[PATHS] dir_intermed``."""
    return Path(parser.get("PATHS", "dir_intermed")) / LOCK_NAME


def lock_is_fresh(path: Path, max_age_hours: float = LOCK_MAX_AGE_HOURS) -> bool:
    """True when ``path`` exists and was touched less than ``max_age_hours`` ago."""
    try:
        if not path.is_file():
            return False
        age_hours = (time.time() - path.stat().st_mtime) / 3600.0
    except OSError as exc:
        logger.warning(f"Could not stat the refresh lock {path} ({exc}); treating as stale")
        return False
    if age_hours < max_age_hours:
        logger.warning(
            f"Refresh lock {path} is {age_hours:.2f} h old "
            f"(< {max_age_hours} h); skipping refresh"
        )
        return True
    return False


def _touch_lock(path: Path) -> None:
    """Create/update the lock file, logging (not raising) on failure."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"season_monitor refresh started {_dt.datetime.now().isoformat(timespec='seconds')}\n",
            encoding="utf-8",
        )
    except OSError as exc:  # noqa: BLE001
        logger.warning(f"Could not write the refresh lock {path} ({exc}); continuing")


def build_params(cfg_list: Sequence[Any], years: Optional[Sequence[int]] = None) -> Any:
    """Build the geoprepare ``params`` object the dataset modules expect.

    Reproduces the attribute set ``geoprepare.geodownload.run`` assembles for
    the CHIRPS and CHIRPS-GEFS branches:

    * ``fill_value``, ``version``, ``disagg``, ``prelim``, ``final`` from
      ``[CHIRPS]``;
    * ``data_dir`` from ``[CHIRPS-GEFS]``;
    * ``process_only`` from ``[DEFAULT]``;
    * ``redo_last_year`` (set by ``GeoDownload.parse_config``: true before
      March 1);
    * ``start_year`` / ``end_year`` restricted to ``years``.

    Args:
        cfg_list: the 4-file config list (geobase, countries, crops, geocif).
        years: years to restrict the download to; ``None`` uses
            :func:`_default_years`.

    Returns:
        The configured ``GeoDownload`` instance.
    """
    geodownload = importlib.import_module("geoprepare.geodownload")
    params = geodownload.GeoDownload(list(cfg_list))
    params.parse_config("DEFAULT")

    parser = params.parser
    params.fill_value = parser.getint("CHIRPS", "fill_value", fallback=-2147483648)
    params.version = parser.get("CHIRPS", "version", fallback="v2")
    params.disagg = parser.get("CHIRPS", "disagg", fallback="sat")
    params.prelim = parser.get("CHIRPS", "prelim", fallback="")
    params.final = parser.get("CHIRPS", "final", fallback="")
    params.data_dir = parser.get("CHIRPS-GEFS", "data_dir", fallback="")
    params.process_only = parser.getboolean("DEFAULT", "process_only", fallback=False)
    if not hasattr(params, "redo_last_year"):
        params.redo_last_year = _dt.date.today().month < 3

    span = sorted(int(y) for y in (years if years else _default_years()))
    params.start_year = span[0]
    params.end_year = span[-1]
    return params


def refresh_inputs(
    cfg_list: Sequence[Any],
    datasets: Sequence[str] = ("CHIRPS", "CHIRPS-GEFS"),
    years: Optional[Sequence[int]] = None,
    logger: Optional[logging.Logger] = None,
) -> dict[str, dict[str, Any]]:
    """Refresh CHIRPS and/or CHIRPS-GEFS before a season-monitor run.

    Args:
        cfg_list: the 4-file config list (geobase, countries, crops, geocif).
        datasets: dataset names to refresh; an empty sequence disables the
            refresh entirely. Unknown names are reported as errors, not raised.
        years: calendar years to restrict the download to. ``None`` refreshes
            the current year, plus the previous one during January/February.
        logger: logger to use; defaults to this module's logger.

    Returns:
        ``{dataset: {"ok": bool, "seconds": float, "error": str | None,
        "skipped": bool}}`` -- one entry per requested dataset. When a guard
        fires, every entry is ``ok=False, skipped=True`` and ``error`` carries
        the reason.
    """
    log = logger or globals()["logger"]
    names = [str(d) for d in datasets]
    if not names:
        log.info("refresh_inputs: no datasets requested; nothing to do")
        return {}

    def _skip_all(reason: str) -> dict[str, dict[str, Any]]:
        return {
            name: {"ok": False, "seconds": 0.0, "error": reason, "skipped": True}
            for name in names
        }

    # Guard 1: another geoprepare download is in flight.
    try:
        if download_running():
            return _skip_all("another geoprepare download is running")
    except Exception as exc:  # noqa: BLE001
        log.warning(f"refresh_inputs: process guard failed ({exc}); continuing")

    # Build params before the lock check: we need `dir_intermed` from it and a
    # config error should be reported as a failure, not silently skipped.
    try:
        params = build_params(cfg_list, years)
    except Exception as exc:  # noqa: BLE001 - a refresh must never kill the monitor
        log.error(f"refresh_inputs: could not build the geoprepare params ({exc})")
        return {
            name: {"ok": False, "seconds": 0.0, "error": f"config: {exc}", "skipped": False}
            for name in names
        }

    # Guard 2: a recent lock file.
    path_lock = lock_path(params.parser)
    try:
        if lock_is_fresh(path_lock):
            return _skip_all(f"lock {path_lock} younger than {LOCK_MAX_AGE_HOURS} h")
    except Exception as exc:  # noqa: BLE001
        log.warning(f"refresh_inputs: lock guard failed ({exc}); continuing")

    _touch_lock(path_lock)
    log.info(
        f"refresh_inputs: {names} for years {params.start_year}-{params.end_year} "
        f"(process_only={params.process_only})"
    )

    results: dict[str, dict[str, Any]] = {}
    for name in names:
        module_name = DATASET_MODULES.get(name)
        if module_name is None:
            log.error(f"refresh_inputs: unknown dataset {name}; known: {sorted(DATASET_MODULES)}")
            results[name] = {
                "ok": False,
                "seconds": 0.0,
                "error": f"unknown dataset {name}",
                "skipped": False,
            }
            continue

        started = time.time()
        try:
            # importlib (not a top-level import) so tests can inject a stub into
            # sys.modules and so a missing geoprepare is a logged failure.
            module = importlib.import_module(module_name)
            module.run(params)
            elapsed = time.time() - started
            results[name] = {"ok": True, "seconds": elapsed, "error": None, "skipped": False}
            log.info(f"refresh_inputs: {name} ok in {elapsed:.1f} s")
        except Exception as exc:  # noqa: BLE001 - never raise out of a refresh
            elapsed = time.time() - started
            results[name] = {
                "ok": False,
                "seconds": elapsed,
                "error": str(exc),
                "skipped": False,
            }
            log.error(f"refresh_inputs: {name} FAILED after {elapsed:.1f} s: {exc}")

    return results
