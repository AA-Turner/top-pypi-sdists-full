from importlib import metadata

try:
    __version__ = metadata.version("msmart-ng")
except metadata.PackageNotFoundError:
    __version__ = "UNKNOWN"
