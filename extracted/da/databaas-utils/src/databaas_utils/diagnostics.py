"""Runtime checks for things that fail confusingly rather than loudly."""

from __future__ import annotations

import logging
from contextlib import suppress
from importlib.metadata import packages_distributions, version

log = logging.getLogger(__name__)

_state: dict[str, bool] = {"warned": False}


def obstore_distributions() -> list[str]:
    """Which installed distributions provide the top-level module `obstore`."""
    return sorted(packages_distributions().get("obstore", []))


def check_obstore(*, once: bool = True) -> list[str]:
    """Warn when more than one distribution provides `obstore`.

    `RemoteSignedS3Store` ships only in `obstore-databaas`, which shares the
    top-level module name with upstream `obstore`. pip does not error on the
    collision — it overwrites, and install order decides the winner. Nothing can
    be done about that from inside a wheel except say so.
    """
    dists = obstore_distributions()
    if len(dists) > 1 and not (once and _state["warned"]):
        _state["warned"] = True
        detail = ", ".join(f"{d} {_safe_version(d)}" for d in dists)
        log.warning(
            "Multiple distributions provide the `obstore` module (%s). They "
            "overwrite each other and install order decides which wins; only "
            "obstore-databaas carries RemoteSignedS3Store. Uninstall the other "
            "one if remote signing misbehaves.",
            detail,
        )
    return dists


def _safe_version(dist: str) -> str:
    with suppress(Exception):  # metadata lookup is best effort
        return version(dist)
    return "unknown"
