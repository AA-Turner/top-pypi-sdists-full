"""emake - A Python module to replace Makefile workflows."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("emake")

except PackageNotFoundError:
    __version__ = "dev"
