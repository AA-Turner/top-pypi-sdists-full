import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests
from packaging.version import Version

from abstra_internals.consts.filepaths import CACHED_VERSIONS_DIR_PATH
from abstra_internals.logger import AbstraLogger

EXPIRE_PERIOD = 60 * 15  # 15 minutes
TIMEOUT = 5


def _read_cached_version(root_path: Path, package_name: str) -> Optional[Version]:
    cached_file = root_path / CACHED_VERSIONS_DIR_PATH / f"{package_name}.json"

    if not cached_file.exists():
        return None

    try:
        with open(cached_file, "r", encoding="utf-8") as f:
            cached_version = json.loads(f.readline())

        created_at = cached_version["created_at"]
        version = cached_version["version"]
    except Exception as e:
        AbstraLogger.capture_exception(e)
        return None

    if (
        isinstance(created_at, float)
        and version is not None
        and datetime.utcnow().timestamp() - created_at < EXPIRE_PERIOD
    ):
        return Version(version)

    return None


def get_cached_latest_version(root_path: Path, package_name="abstra", revalidate=False):
    if not revalidate:
        cached = _read_cached_version(root_path, package_name)
        if cached is not None:
            return cached

    try:
        response = requests.get(
            f"https://pypi.org/pypi/{package_name}/json", timeout=TIMEOUT
        )
        response.raise_for_status()
        latest_version = response.json()["info"]["version"]

        update_cached_latest_version(root_path, latest_version, package_name)

        return Version(latest_version)
    except Exception:
        # A revalidating pass skipped a possibly still-valid cache: fall back
        # to it so a network hiccup on manual refresh doesn't drop an existing
        # banner.
        if revalidate:
            return _read_cached_version(root_path, package_name)
        return None


def update_cached_latest_version(
    root_path: Path, version: Version, package_name="abstra"
):
    cached_file = root_path / CACHED_VERSIONS_DIR_PATH / f"{package_name}.json"

    if not cached_file.parent.exists():
        cached_file.parent.mkdir(parents=True)

    # Atomic write: the editor and the linter sidecar child share this cache.
    tmp_file = cached_file.with_suffix(".json.tmp")
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "version": str(version),
                "created_at": datetime.utcnow().timestamp(),
            },
            f,
        )
    os.replace(tmp_file, cached_file)
