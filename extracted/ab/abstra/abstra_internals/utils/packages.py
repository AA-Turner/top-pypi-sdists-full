from importlib.metadata import PackageNotFoundError, distribution

from packaging.version import Version


def get_local_package_version(package_name="abstra"):
    try:
        return parse_version(distribution(package_name).version)
    except PackageNotFoundError:
        raise


def parse_version(version: str):
    return Version(version)


def _capture_running_version() -> str:
    try:
        return str(get_local_package_version("abstra"))
    except PackageNotFoundError:
        return "0.0.0"


# importlib.metadata reads dist-info from DISK, so after an in-place
# `pip install --upgrade` it reports the new version while this process still
# runs the old code. Captured at import (process boot) so it identifies the
# code actually running.
RUNNING_ABSTRA_VERSION = _capture_running_version()
