"""Cold-start installation of dependencies deferred from the function bundle."""

from __future__ import annotations

import os
import shutil
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from collections.abc import Mapping


def reset_directories(deps_dir: str, scratch_dir: str) -> None:
    """Empty the install target and the scratch directory uv works in.

    An install that was killed leaves its scratch files behind, and can leave
    packages that uv counts as installed although most of their files are
    missing. Installing on top of either fills the disk or yields an
    environment that cannot be imported.
    """
    for path in (deps_dir, scratch_dir):
        if os.path.lexists(path):
            shutil.rmtree(path)
        os.makedirs(path)


def sync_environment(deps_dir: str, scratch_dir: str) -> dict[str, str]:
    """Return the environment ``uv sync`` runs in.

    ``scratch_dir`` holds everything uv writes outside ``deps_dir``, so that
    it can be removed. It must be on the same filesystem as ``deps_dir`` for
    the hardlinks ``sync_command`` asks for.
    """
    return {
        "PATH": os.environ.get("PATH", ""),
        "VIRTUAL_ENV": deps_dir,
        "TMPDIR": scratch_dir,
        "UV_PYTHON_DOWNLOADS": "never",
        # Skip writing INSTALLER, REQUESTED, and direct_url.json: they are
        # never read at runtime.
        "UV_NO_INSTALLER_METADATA": "1",
    }


def sync_command(uv_path: str, config: Mapping[str, object]) -> list[str]:
    """Return the ``uv sync`` command that installs the deferred dependencies.

    ``config`` is the bundle's ``_uv/_runtime_config.json``. Packages already
    in the bundle are skipped, and a uv workspace member installs its own
    dependencies rather than those of the workspace root project.
    """
    # --inexact avoids removing packages already present in _vendor (bundled
    # deps). --link-mode hardlink lets the temporary download cache and the
    # target venv share inode blocks on /tmp, reducing peak disk usage on
    # Lambda's limited ephemeral storage.
    command = [
        uv_path,
        "sync",
        "--inexact",
        "--active",
        "--frozen",
        "--no-dev",
        "--no-editable",
        "--no-install-project",
        "--no-build",
        "--no-cache",
        "--no-progress",
        "--link-mode",
        "hardlink",
    ]
    bundled_packages = config.get("bundledPackages", [])
    if isinstance(bundled_packages, list):
        for package in cast("list[object]", bundled_packages):
            if isinstance(package, str):
                command.extend(["--no-install-package", package])
    workspace_package = config.get("workspacePackage")
    if isinstance(workspace_package, str) and workspace_package:
        command.extend(["--package", workspace_package])
    return command
