import datetime
from typing import Tuple

from semantic_version import Version

from tecton import _gen_version


def get_version() -> str:
    return _gen_version.VERSION


# Note that get_semantic_version() returns versions that don't exactly match PyPI, e.g. '0.8.0b34' instead of
# '0.8.0-b34'. If you want the same version string as PyPI, use get_version().
#
# NOTE(jake): It's not clear why get_semantic_version() is needed in addition to get_version().
def get_semantic_version() -> str:
    version = get_version()

    _semver = str(Version.coerce(version))
    return _semver


def get_status():
    try:
        from tecton._stamp import BUILD_STATUS

        return BUILD_STATUS
    except ImportError:
        return {}


def get_hash() -> str:
    status = get_status()
    return status.get("GIT_COMMIT", "n/a")


def get_summary() -> Tuple[str, str, str]:
    """Returns the version, git commit, and build datetime."""
    status = get_status()
    ts_seconds = status.get("BUILD_TIMESTAMP", None)
    ts = datetime.datetime.utcfromtimestamp(int(ts_seconds)).isoformat() if ts_seconds else "n/a"
    commit = status.get("GIT_COMMIT", "n/a")
    return get_version(), commit, ts


def summary():
    """Prints the version, git commit, and build datetime to the console."""
    (version_number, commit, build_datetime) = get_summary()
    print(f"Version: {version_number}")
    print(f"Git Commit: {commit}")
    print(f"Build Timestamp: {build_datetime}")
