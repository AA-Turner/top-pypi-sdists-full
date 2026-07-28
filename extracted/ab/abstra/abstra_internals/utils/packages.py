from importlib.metadata import PackageNotFoundError, distribution
from typing import Optional

from packaging.version import Version


def get_local_package_version(package_name="abstra"):
    try:
        return parse_version(distribution(package_name).version)
    except PackageNotFoundError:
        raise


def parse_version(version: str):
    return Version(version)


def _capture_running_version() -> Optional[str]:
    try:
        return str(get_local_package_version("abstra"))
    except PackageNotFoundError:
        return None


# importlib.metadata reads dist-info from DISK, so after an in-place
# `pip install --upgrade` it reports the new version while this process still
# runs the old code. Captured at import (process boot) so it identifies the
# code actually running.
#
# None means abstra's own metadata could not be located at boot (e.g. running
# from source without dist-info). Consumers must treat None as "unknown" — note
# that "0.0.0" is a legitimate dev/CI version, NOT a not-found marker.
RUNNING_ABSTRA_VERSION: Optional[str] = _capture_running_version()
