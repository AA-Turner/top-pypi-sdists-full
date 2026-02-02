import asyncio
import atexit
import os
import platform
import subprocess
import sys
import threading
from importlib.metadata import Distribution, PackageNotFoundError
from json import JSONDecodeError
from typing import Any, Literal, cast

import click
from httpx import Client, HTTPError
from packaging.version import Version

from exponent import __version__  # Import the new version constant
from exponent.core.config import Settings, is_editable_install

_UPGRADE_TIMEOUT_SECONDS = 120


class _UpgradeState:
    thread: threading.Thread | None = None


def get_python_path() -> str:
    """Get the path to the Python interpreter."""
    try:
        return (
            subprocess.check_output(["which", "python"])
            .decode(errors="replace")
            .strip()
        )
    except Exception:
        return "unknown"


def get_sys_executable() -> str:
    """Get the path to the Python interpreter."""
    return str(sys.executable)


def get_installed_version() -> str | Literal["unknown"]:
    """Get the running version of exponent-run. Note this may be different from
    importlib version, if a new version is installed but we're running the old version."""
    return __version__


def get_installed_metadata() -> Any | Literal["unknown"]:
    """Get the installed metadata of exponent-run.

    Returns:
        The installed metadata of exponent-run if it can be determined, otherwise "unknown"
    """
    try:
        return Distribution.from_name("indent").metadata
    except PackageNotFoundError as e:
        click.echo(f"Error reading metadata: {e}", err=True)
        return "unknown"


def get_installer() -> str | Literal["unknown"]:
    """Get the installer of exponent-run.

    Returns:
        The installer of exponent-run if it can be determined, otherwise "unknown"
    """
    try:
        dist = Distribution.from_name("indent")
        # Try to read the INSTALLER file from the distribution
        installer_files = dist.read_text("INSTALLER")
        if installer_files:
            return installer_files.strip()
        return "unknown"
    except Exception:
        return "unknown"


def get_latest_pypi_exponent_version() -> str | None:
    """Get the latest version of Indent available on PyPI.

    Returns:
        The newest version of Indent available on PyPI, or None if an error occurred.
    """
    try:
        return cast(
            str,
            (
                Client()
                .get("https://pypi.org/pypi/indent/json")
                .json()["info"]["version"]
            ),
        )
    except (HTTPError, JSONDecodeError, KeyError):
        click.secho(
            "An unexpected error occurred communicating with PyPi, please check your network and try again.",
            fg="red",
        )
        return None


def check_exponent_version() -> tuple[str, str] | None:
    """Check if there is a newer version of Indent available on PyPI.

    Returns:
        None
    """

    if os.getenv("EXPONENT_TEST_AUTO_UPGRADE"):
        return "1.0.0", "1.0.1"
    installed_version = get_installed_version()
    if installed_version == "unknown":
        click.secho("Unable to determine current Indent version.", fg="yellow")
        return None

    if (latest_version := get_latest_pypi_exponent_version()) and Version(
        latest_version
    ) > Version(installed_version):
        return installed_version, latest_version

    return None


def _get_upgrade_command(version: str) -> list[str]:
    """Get the install command for exponent."""

    return [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--upgrade",
        f"indent=={version}",
    ]


def _get_upgrade_command_str(version: str) -> str:
    """Get the install command for exponent."""

    return f'{sys.executable} -m pip install --upgrade "indent=={version}"'


def _new_version_str(current_version: str, new_version: str) -> str:
    return f"\n{click.style('A new Indent version is available:', fg='cyan')} {new_version} (current: {current_version})\n"


def _windows_new_version_str(current_version: str, new_version: str) -> str:
    return f"{_new_version_str(current_version, new_version)}\n{click.style('Run this command to upgrade:', fg='cyan')}\n{click.style(_get_upgrade_command_str(new_version), fg='yellow')}\n"


def _ask_continue_without_upgrading() -> None:
    if click.confirm("Continue without upgrading?", default=False):
        click.secho("Using outdated version.", fg="red")
    else:
        click.secho("Exiting due to outdated version", fg="red")
        sys.exit(1)


def upgrade_exponent(
    *,
    current_version: str,
    new_version: str,
    force: bool,
) -> None:
    """Upgrade Indent to the passed in version.

    Args:
        current_version: The current version of Indent.
        new_version: The new version of Indent.
        force: Whether to force the upgrade without prompting for confirmation.

    Returns:
        None
    """
    new_version_str = _new_version_str(current_version, new_version)
    upgrade_command = _get_upgrade_command(new_version)
    upgrade_command_str = _get_upgrade_command_str(new_version)

    if platform.system() == "Windows":
        click.echo(_windows_new_version_str(current_version, new_version))
        return

    if not force:
        click.echo(
            f"{new_version_str}\n{click.style('Upgrade command:', fg='cyan')}\n{upgrade_command_str}\n",
        )

        if not click.confirm("Upgrade now?", default=True):
            return
    else:
        click.echo(f"Current version: {current_version}")
        click.echo(f"New version available: {new_version}")

    click.secho("Upgrading...", bold=True, fg="yellow")
    result = subprocess.run(
        upgrade_command, capture_output=True, text=True, check=False
    )

    click.echo(result.stdout)
    click.echo(result.stderr)

    if result.returncode != 0:
        click.secho(
            "\nFailed to upgrade Indent. Reach out to team@indent.com for help.",
            fg="red",
        )
        sys.exit(2)

    click.secho(f"Successfully upgraded Indent to version {new_version}!", fg="green")

    click.echo("Re-run indent to use the latest version.")
    sys.exit(0)


def _wait_for_upgrade_thread() -> None:
    if _UpgradeState.thread is not None and _UpgradeState.thread.is_alive():
        _UpgradeState.thread.join(timeout=_UPGRADE_TIMEOUT_SECONDS)


def _upgrade_thread_worker(
    upgrade_command: list[str],
    current_version: str,
    new_version: str,
    settings: Settings,
) -> None:
    from exponent.core.remote_execution.session import send_exception_log

    try:
        result = subprocess.run(
            upgrade_command,
            capture_output=True,
            text=True,
            check=True,
            timeout=_UPGRADE_TIMEOUT_SECONDS,
        )

        if result.returncode != 0:
            raise Exception(
                f"Background upgrade from {current_version} to {new_version} failed with code {result.returncode}\nstdout: {result.stdout}\nstderr: {result.stderr}"
            )
    except Exception as e:
        asyncio.run(send_exception_log(e, session=None, settings=settings))


def upgrade_exponent_in_background(
    current_version: str,
    new_version: str,
    settings: Settings,
) -> None:
    """Upgrade Indent to the passed in version in a background thread."""

    if not settings.options.auto_upgrade:
        click.secho(
            "A new version of Indent is available, but automatic upgrades are disabled. Please upgrade manually using `indent upgrade`.\n",
            fg="yellow",
        )
        return

    if platform.system() == "Windows":
        click.echo(
            _windows_new_version_str(current_version, new_version),
        )
        _ask_continue_without_upgrading()
        return

    click.secho(
        f"\nUpgrading Indent from {current_version} to {new_version} (this will take effect next time)\n",
        fg="cyan",
        bold=True,
    )

    _UpgradeState.thread = threading.Thread(
        target=_upgrade_thread_worker,
        args=(
            _get_upgrade_command(new_version),
            current_version,
            new_version,
            settings,
        ),
    )
    atexit.register(_wait_for_upgrade_thread)
    _UpgradeState.thread.start()


def check_exponent_version_and_upgrade(settings: Settings) -> None:
    if not is_editable_install() and (result := check_exponent_version()):
        installed_version, latest_version = result
        upgrade_exponent_in_background(
            current_version=installed_version,
            new_version=latest_version,
            settings=settings,
        )
