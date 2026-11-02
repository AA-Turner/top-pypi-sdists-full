"""Agent Platform API Client"""

from importlib.metadata import PackageNotFoundError, version

from .api import APIClient, APIError, get_client
from .config import Config, ConfigurationError, get_config
from .exporter import ExportSummary

try:
    __version__ = version("ap-client")
except PackageNotFoundError:
    __version__ = "0+unknown"

__all__ = [
    "APIClient",
    "APIError",
    "Config",
    "ConfigurationError",
    "ExportSummary",
    "__version__",
    "get_client",
    "get_config",
]
