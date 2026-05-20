import platform
from importlib import metadata


class TunaError(Exception):
    pass


def get_version_text():
    try:
        _version = metadata.version("tuna")
    except metadata.PackageNotFoundError:
        _version = "unknown"

    return f"tuna {_version} [Python {platform.python_version()}]"
