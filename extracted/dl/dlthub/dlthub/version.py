from importlib.metadata import version as pkg_version
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from types import ModuleType

IMPORT_NAME = "dlthub"
PKG_NAME = "dlthub"
__version__ = pkg_version(PKG_NAME)
PKG_REQUIREMENT = f"{PKG_NAME}=={__version__}"


def _ensure_dlt_installed(pkg_name: str, dlt_extra: str) -> "ModuleType":
    """Ensures that dlt is installed.

    Args:
        pkg_name: Name of the plugin package (e.g., "dlthub")
        dlt_extra: The dlt extra to install the plugin (e.g., "hub")

    Returns:
        The imported dlt module

    Raises:
        ImportError: If dlt is not installed
    """
    try:
        import dlt

        return dlt
    except ModuleNotFoundError as mod_ex:
        raise ImportError(
            f"{str(mod_ex)}\n`{pkg_name}` is a `dlt` plugin and must be installed together with "
            "`dlt`. We recommend to use `{dlt_extra}` extra to install right versions "
            "combination:\n\n"
            f'pip install "dlt[{dlt_extra}]"'
        )


def ensure_dlt_version() -> None:
    """Ensures that dlt is installed and version matches plugin version."""
    dlt = _ensure_dlt_installed(PKG_NAME, "hub")

    # not with dlt installed we can use it to verify plugin version
    from dlt.common.runtime.run_context import ensure_plugin_version_match

    ensure_plugin_version_match(PKG_NAME, dlt.__version__, __version__, "dlthub", "hub")
