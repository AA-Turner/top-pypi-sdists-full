import sys
from typing import Optional

from packaging import version
import requests

import anyscale
from anyscale.util import is_anyscale_cluster, is_anyscale_workspace


ANYSCALE_PYPI_PACKAGE = "anyscale"


def _get_latest_pypi_version(package_name: str) -> Optional[str]:
    """
    This method gets the latest version of a package from PyPI.
    If the request fails, it doesn't raise the execption since it shouldn't
    interrupt the CLI flow.
    """
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=2)
        data = response.json()
        return data["info"]["version"]
    except Exception:  # noqa: BLE001
        return None


def _is_upgrade_needed(
    local_anyscale_version: str, latest_version: Optional[str]
) -> bool:
    """
    This method checks the local Anyscale version against the latest version from pypi.
    If the local version is not the latest, it prints a warning message.
    """
    if local_anyscale_version == "0.0.0-dev":
        # This is using anyscale CLI from source. No need to check for updates.
        return False
    return latest_version is not None and version.parse(
        local_anyscale_version
    ) < version.parse(latest_version)


def log_warning_if_version_needs_upgrade() -> None:
    """
    Logs a warning if the local Anyscale version is not the latest.

    Note that the check is skipped for clusters/workspaces.
    """
    if is_anyscale_workspace() or is_anyscale_cluster():
        # If the command is run from clusters/workspaces, we don't do version checking
        # because the Anyscale CLI is bundled as a part of cluster envs.
        return

    local_anyscale_version = anyscale.__version__
    latest_version = _get_latest_pypi_version(ANYSCALE_PYPI_PACKAGE)

    if _is_upgrade_needed(local_anyscale_version, latest_version):
        print(
            "[WARNING] A newer version of the Anyscale CLI is available. "
            f"Your current version is {local_anyscale_version}. The latest version is {latest_version}. "
            "To avoid issues accessing Anyscale`s API, upgrade to the latest version by running `pip install --upgrade anyscale`.",
            file=sys.stderr,
        )
