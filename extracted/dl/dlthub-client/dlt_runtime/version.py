# Python internals
from importlib.metadata import version as pkg_version

PKG_NAME = "dlthub-client"
__version__ = pkg_version(PKG_NAME)
PKG_REQUIREMENT = f"{PKG_NAME}=={__version__}"
USER_AGENT = f"dlthub-cli/{__version__}"
