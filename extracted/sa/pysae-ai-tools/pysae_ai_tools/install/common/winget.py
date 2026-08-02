"""Helper for installing packages via winget on Windows.

The framework calls :func:`install` from ``BinaryTool.install_binary`` when the
tool defines ``winget_package``. Returns ``None`` on non-Windows systems or
when winget is not available — callers should then fall through to the OS
hook (``install_windows``).

A non-zero exit from winget surfaces as ``InstallReport(error=...)`` rather
than ``None``: when winget is present we treat its failure as the real error
instead of silently retrying another path.
"""

import shutil
import subprocess

from ...common import winpath
from . import binary
from .base import InstallReport
from .platform import detect


def is_available() -> bool:
    """True when running on Windows and the ``winget`` binary is on PATH."""
    try:
        plat = detect()
    except ValueError:
        return False
    if not plat.is_windows:
        return False
    return shutil.which("winget") is not None


def install(
    package_id: str,
    *,
    binary_name: str | None = None,
    version_arg: str = "--version",
    version_timeout: int = 5,
) -> InstallReport | None:
    """Install ``package_id`` via winget. Returns ``None`` if winget unusable.

    Always passes ``--silent``, ``--accept-package-agreements`` and
    ``--accept-source-agreements`` for non-interactive automation.

    Quirks handled:

    - winget exits non-zero when the package is already installed with no
      upgrade available — treated as success (the binary is on disk).
    - winget exits 0 with no version change when its catalog is at parity
      with the installed copy (catalog can lag GitHub releases by hours
      or days). The English/French/Italian/... messages winget prints in
      that case are locale-translated, so we don't try to match them —
      instead we probe the binary version pre/post and mark the result
      as ``already up-to-date`` whenever it didn't move. ``binary_name``
      must be passed for that probe; without it we fall back to the
      stdout/stderr text scan.
    - After a successful install, the user-scope PATH (where winget often
      registers the package directory) is merged into the process PATH so
      ``shutil.which`` finds the binary without a shell restart.
    """
    if not is_available():
        return None
    pre_version = (
        binary.get_version(binary_name, version_arg=version_arg, timeout=version_timeout) if binary_name else ""
    )
    cmd = [
        "winget",
        "install",
        "--id",
        package_id,
        "-e",
        "--source",
        "winget",
        "--silent",
        "--accept-package-agreements",
        "--accept-source-agreements",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=False)
    output = f"{r.stdout}\n{r.stderr}".lower()
    already_installed = (
        "no available upgrade" in output or "no newer package versions" in output or "already installed" in output
    )
    if r.returncode != 0 and not already_installed:
        return InstallReport(error=f"winget: {r.stderr.strip() or r.stdout.strip()}")
    # Force-refresh: winget just extended the user PATH so we want the new
    # entry visible to sibling install steps in this same Python process,
    # even if the cache was already warmed earlier.
    winpath.refresh_process_path_from_registry(force=True)
    if not already_installed and binary_name and pre_version:
        post_version = binary.get_version(binary_name, version_arg=version_arg, timeout=version_timeout)
        if post_version and post_version == pre_version:
            already_installed = True
    method = "winget (already up-to-date)" if already_installed else "winget"
    return InstallReport(method=method)
