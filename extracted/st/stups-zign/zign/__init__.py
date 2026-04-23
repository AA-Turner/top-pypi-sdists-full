from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("stups-zign")
except PackageNotFoundError:
    __version__ = "dev"
