"""The installed ``dlthub-client`` version, which the SDK, CLI and MCP server share."""

# Python internals
from importlib.metadata import version as pkg_version

PKG_NAME = "dlthub-client"
__version__ = pkg_version(PKG_NAME)
USER_AGENT = f"dlthub-python-sdk/{__version__}"
