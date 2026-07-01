from importlib.metadata import version as pkg_version

PKG_NAME = "dlthub-client"
__version__ = pkg_version(PKG_NAME)
PKG_REQUIREMENT = f"{PKG_NAME}=={__version__}"
