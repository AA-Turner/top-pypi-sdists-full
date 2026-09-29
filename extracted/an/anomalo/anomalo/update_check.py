from __future__ import annotations

import os
import sys
import threading

import requests


DISABLE_ENV_VAR = "ANOMALO_DISABLE_UPDATE_CHECK"
# Airgapped networks often drop packets rather than refuse them, so every wait is
# bounded; the check runs beside the command and must never be what it waits on.
EXIT_WAIT_SECONDS = 1
PYPI_URL = "https://pypi.org/pypi/anomalo/json"
REQUEST_TIMEOUT_SECONDS = 3


def _parse(version: str) -> tuple[int, ...] | None:
    try:
        return tuple(int(part) for part in version.split("."))
    except ValueError:
        return None


def latest_release() -> str | None:
    try:
        response = requests.get(PYPI_URL, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        version = response.json()["info"]["version"]
    except (requests.RequestException, ValueError, KeyError, TypeError):
        # No route to PyPI is normal (proxies, airgapped installs), so the
        # check stays silent rather than reporting it.
        return None
    # A non-string version would raise in _parse, and the traceback would land on
    # stderr from the check's own thread instead of being skipped like the rest.
    return version if isinstance(version, str) else None


def newer_release(current: str) -> str | None:
    """The latest PyPI release if it is newer than `current`, otherwise None.

    Source and development installs report 0.0.0 and are never checked.
    """
    current_parts = _parse(current)
    if DISABLE_ENV_VAR in os.environ or not current_parts or not any(current_parts):
        return None
    latest = latest_release()
    latest_parts = _parse(latest) if latest else None
    if latest_parts is None or latest_parts <= current_parts:
        return None
    return latest


class UpdateNotice:
    """Looks up the latest release in the background and reports it on exit."""

    def __init__(self, current: str) -> None:
        self.current = current
        self._newer: str | None = None
        self._thread = threading.Thread(target=self._check, daemon=True)

    def _check(self) -> None:
        self._newer = newer_release(self.current)

    def start(self) -> UpdateNotice:
        self._thread.start()
        return self

    def report(self) -> None:
        self._thread.join(timeout=EXIT_WAIT_SECONDS)
        if self._newer:
            print(
                f"A newer anomalo CLI is available: {self._newer} (you have "
                f"{self.current}). Upgrade with `pip install -U anomalo`.",
                file=sys.stderr,
            )
