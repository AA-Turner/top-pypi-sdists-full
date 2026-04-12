from importlib import metadata
from sys import version_info as vi


class TunaError(Exception):
    pass


def get_version_text():
    try:
        _version = metadata.version("tuna")
    except metadata.PackageNotFoundError:
        _version = "unknown"

    return f"quadpy {_version} [Python {vi.major}.{vi.minor}.{vi.micro}]"
