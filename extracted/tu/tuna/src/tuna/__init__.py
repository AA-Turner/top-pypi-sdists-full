from . import cli
from .main import read_import_profile


def load_ipython_extension(_ipython):
    from . import magics  # noqa: F401, PLC0415


__all__ = [
    "cli",
    "read_import_profile",
]
