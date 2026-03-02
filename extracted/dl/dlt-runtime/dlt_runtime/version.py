from importlib.metadata import version as pkg_version

IMPORT_NAME = "dlt_runtime"
PKG_NAME = "dlt-runtime"
__version__ = pkg_version(PKG_NAME)
PKG_REQUIREMENT = f"{PKG_NAME}=={__version__}"
