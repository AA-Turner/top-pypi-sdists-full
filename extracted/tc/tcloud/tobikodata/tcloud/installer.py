from __future__ import annotations

import logging
import os
import shutil
import subprocess
import sys
import typing as t
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from urllib.parse import urlencode, urljoin

import httpx
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

import tobikodata.tcloud.constants as c
from tobikodata.tcloud import pip_helper as pip
from tobikodata.tcloud.auth import BearerAuth, TobikoAuth
from tobikodata.tcloud.config import TCloudProject
from tobikodata.tcloud.utils import get_unpack_path, get_unpacked_site_packages_path

logger = logging.getLogger(__name__)

PACKAGE_NAME = "sqlmesh-enterprise"
EXECUTORS_PEX_NAME = "executors_bin.pex"


@dataclass
class InstallationDetails:
    is_installed: bool
    """Whether sqlmesh-enterprise is installed."""
    extras: t.Set[str]
    """The extras that were previously installed."""
    upgrade_info: t.Dict[str, t.Union[str, t.List[str]]]
    """The upgrade info for the SQLMesh Enterprise package."""


def is_sqlmesh_enterprise_version_installed(
    project: TCloudProject, previous_extras: t.List[str]
) -> InstallationDetails:
    """
    Checks if the SQLMesh Enterprise package is installed and if the version is the same as the target version. Also returns
    the extras.
    """
    _configure_state_connection(project)

    # Use the package metadata to avoid importing the package.
    try:
        current_version = version(PACKAGE_NAME)
    except PackageNotFoundError:
        current_version = None

    upgrade_info = _get_enterprise_version_upgrade(project, current_version)
    target_version = upgrade_info["target_version"]
    # Check `upgrade_info` for extras in case the API supports this in the future
    extras = set((project.extras or []) + upgrade_info.get("extras", []))  # type: ignore
    return InstallationDetails(
        is_installed=current_version == target_version and extras.issubset(previous_extras),
        extras=extras,
        upgrade_info=upgrade_info,
    )


def install_sqlmesh_enterprise(project: TCloudProject, previous_extras: t.List[str]) -> bool:
    """Downloads and installs / upgrades the SQLMesh Enterprise package if needed.

    Args:
        project: The target project.
        previous_extras: The extras that were previously installed.

    Returns:
        True if the package was installed or upgraded, False otherwise.
    """
    installation_details = is_sqlmesh_enterprise_version_installed(project, previous_extras)
    if installation_details.is_installed:
        return False

    pip.install(
        PACKAGE_NAME,
        pip_executable=project.pip_executable,
        version=installation_details.upgrade_info["target_version"],  # type: ignore
        extra_index_url=installation_details.upgrade_info.get("extra_index_url"),  # type: ignore
        upgrade=True,
        extras=list(installation_details.extras),
    )
    return True


def install_executors(
    project: TCloudProject, tcloud_path: Path = c.TCLOUD_PATH
) -> t.Tuple[Path, Path]:
    """
    Returns a tuple of
    - the path to the executors PEX binary and
    - the path to the site packages directory unpacked from the PEX file
    """
    artifacts_path = tcloud_path / "artifacts"
    artifacts_path.mkdir(parents=True, exist_ok=True)

    current_version = None
    current_executors_bin_path = None

    version_folders = sorted(artifacts_path.iterdir(), reverse=True)
    if version_folders:
        current_version = version_folders[0].name
        current_executors_bin_path = version_folders[0] / EXECUTORS_PEX_NAME
        if not current_executors_bin_path.exists():
            current_version = None

    logger.info("The current executor version: '%s'", current_version)

    upgrade_info = _get_enterprise_version_upgrade(project, current_version)
    target_version = t.cast(str, upgrade_info["target_version"])

    logger.info("The target executor version: '%s'", target_version)

    unpacked_sites_location = get_unpacked_site_packages_path(target_version)
    if current_version == target_version and current_executors_bin_path:
        return current_executors_bin_path, unpacked_sites_location

    for old_version in version_folders:
        if old_version.name != target_version and old_version.is_dir():
            shutil.rmtree(old_version)

    if "executors_pex_url" not in upgrade_info:
        raise ValueError("The upgrade info does not contain the download URL.")

    token = t.cast(t.Optional[str], upgrade_info.get("token"))
    auth = BearerAuth(token) if token else None
    executors_pex_url = t.cast(str, upgrade_info["executors_pex_url"])

    target_version_path = artifacts_path / target_version
    target_version_path.mkdir(exist_ok=True)

    target_executors_bin_path = target_version_path / EXECUTORS_PEX_NAME
    logger.info(
        "Downloading the executors PEX binary from %s to %s",
        executors_pex_url,
        target_executors_bin_path,
    )

    with httpx.Client(auth=auth) as client:
        with client.stream(method="GET", url=executors_pex_url) as response:
            response.raise_for_status()
            with open(target_executors_bin_path, "wb") as fd:
                for chunk in response.iter_raw():
                    fd.write(chunk)

    logger.info("Finished downloading the executors PEX binary to %s", target_executors_bin_path)

    os.chmod(target_executors_bin_path, 0o744)

    unpack_location = get_unpack_path(target_version)
    # Unpack the PEX file
    unpack_executor(target_executors_bin_path, unpack_location)

    return target_executors_bin_path, unpacked_sites_location


def unpack_executor(exector: Path, lib_path: Path) -> None:
    command = [
        sys.executable,
        str(exector),
        "venv",
        "--compile",
        str(lib_path),
    ]
    result = subprocess.run(
        command,
        capture_output=True,
        env={
            "PEX_TOOLS": "1",
        },
    )
    if result.returncode != 0:
        logger.error("Failed to unpack the executors PEX binary, with code %s", result.returncode)
        logger.error("Output: %s", result.stdout)
        logger.error("Error: %s", result.stderr)
        raise subprocess.CalledProcessError(
            returncode=result.returncode,
            cmd=command,
            stderr=result.stderr,
        )
    logger.info("Finished unpacking the executors PEX binary to %s", lib_path)


def is_executor_installed_and_unpacked(
    project: TCloudProject, tcloud_path: Path = c.TCLOUD_PATH
) -> t.Optional[t.Tuple[Path, Path]]:
    upgrade_info = _get_enterprise_version_upgrade(project, None)
    if "executors_pex_url" not in upgrade_info:
        return None
    target_version = upgrade_info["target_version"]
    if not isinstance(target_version, str):
        raise TypeError(
            f"Expected target_version to be a string, got {type(target_version).__name__}"
        )
    artifacts_path = tcloud_path / "artifacts"
    version_folders = sorted(artifacts_path.iterdir(), reverse=True)
    if version_folders:
        current_version = version_folders[0].name
        current_executors_bin_path = version_folders[0] / EXECUTORS_PEX_NAME
        if current_version == target_version and current_executors_bin_path.exists():
            logger.info("Executor is installed")
            unpacked_path = get_unpack_path(target_version)
            if unpacked_path.exists():
                return (current_executors_bin_path, unpacked_path)

    return None


def retry_on_httpx_exception(exception: BaseException) -> bool:
    if isinstance(exception, httpx.TimeoutException):
        return True
    if (
        isinstance(exception, httpx.HTTPStatusError)
        and exception.response
        and exception.response.status_code >= 500
    ):
        return True
    if isinstance(exception, httpx.NetworkError):
        return True
    return False


@retry(
    retry=retry_if_exception(retry_on_httpx_exception),
    stop=stop_after_attempt(5),
    wait=wait_exponential(min=1, max=10),
    reraise=True,
)
def _get_enterprise_version_upgrade(
    project: TCloudProject, current_version: t.Optional[str]
) -> t.Dict[str, t.Union[str, t.List[str]]]:
    url = project.url
    if not url.endswith("/"):
        url += "/"

    def fetch_version_upgrade(path: str) -> httpx.Response:
        upgrade_url = urljoin(url, path)
        if current_version:
            url_params = urlencode({"current_version": current_version})
            upgrade_url += f"?{url_params}"
        with httpx.Client(auth=TobikoAuth(project.token)) as client:
            return client.get(url=upgrade_url)

    response = fetch_version_upgrade("api/state-sync/enterprise-version/upgrade")
    if response.status_code == httpx.codes.NOT_FOUND:
        # Fallback to previous URL
        response = fetch_version_upgrade("state_sync/enterprise_version/upgrade")
    response.raise_for_status()
    return response.json()


def _configure_state_connection(project: TCloudProject) -> None:
    if not project.gateway:
        raise ValueError("The gateway must be set.")

    state_connection_env_prefix = f"SQLMESH__GATEWAYS__{project.gateway.upper()}__STATE_CONNECTION"
    os.environ[f"{state_connection_env_prefix}__TYPE"] = "cloud"
    os.environ[f"{state_connection_env_prefix}__URL"] = project.url
    if project.token:
        os.environ[f"{state_connection_env_prefix}__TOKEN"] = project.token
    os.environ["SQLMESH__DEFAULT_GATEWAY"] = project.gateway
