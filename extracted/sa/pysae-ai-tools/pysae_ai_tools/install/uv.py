"""Install or update uv (Astral's Python package & toolchain manager).

uv is bootstrapped by ``install.sh`` / ``install.ps1`` before this package
is even installed, so on a properly bootstrapped machine ``uv`` is already
on PATH. This tool covers two cases:

- A user installed pysae-ai-tools through some other channel (CI image,
  manual ``uv tool install``) and uv happens not to be present here.
- uv is present but outdated relative to the latest GitHub release.

Updates go through ``uv self update`` when uv is installed via Astral's
official installer (which we use), otherwise we re-run the official
installer to refresh in place. Both paths are idempotent.

Configuration carries the GitLab PyPI index credential, so ``uv tool install``
and ``pip install`` reach private Python packages without further setup.
"""

import subprocess
from typing import Any

from . import registry_credential
from .common import binary, github, platform
from .common.base import BinaryTool, InstallReport, ToolState

UV_REPO = "astral-sh/uv"
UV_INSTALL_URL_UNIX = "https://astral.sh/uv/install.sh"
UV_INSTALL_URL_WIN = "https://astral.sh/uv/install.ps1"


def _self_update() -> tuple[bool, str]:
    """Run ``uv self update``. Returns ``(ok, message)``."""
    try:
        r = subprocess.run(
            ["uv", "self", "update"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=180,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, f"uv self update failed: {exc}"
    if r.returncode != 0:
        return False, (r.stderr or r.stdout).strip()[:500] or "uv self update failed"
    return True, (r.stdout or r.stderr).strip()[:500]


def _curl_install_unix() -> InstallReport:
    try:
        r = subprocess.run(
            ["bash", "-c", f"curl -fsSL {UV_INSTALL_URL_UNIX} | sh"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=180,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return InstallReport(error=f"uv installer failed: {exc}")
    if r.returncode != 0:
        return InstallReport(error=(r.stderr or r.stdout).strip()[:500])
    return InstallReport(method="curl|sh")


def _ps_install_windows() -> InstallReport:
    try:
        r = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                f"irm {UV_INSTALL_URL_WIN} | iex",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=300,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return InstallReport(error=f"uv installer failed: {exc}")
    if r.returncode != 0:
        return InstallReport(error=(r.stderr or r.stdout).strip()[:500])
    return InstallReport(method="irm|iex")


class UvCliTool(BinaryTool):
    name = "uv"
    binary_name = "uv"
    cli_help = "Install/update uv (Astral Python toolchain) and authenticate the GitLab PyPI index"
    # Optional, never pre-configure: uv is REQUIRED, so a developer without a
    # registry PAT must still get uv installed rather than skipped.
    env_optional = (registry_credential.TOKEN_VAR,)

    def fetch_latest_version(self) -> str:
        try:
            tag = github.latest_release(UV_REPO)
        except Exception:  # noqa: BLE001
            return ""
        return tag.lstrip("v")

    def install_linux(self, plat: platform.Platform) -> InstallReport:
        return self._do(plat)

    def install_macos(self, plat: platform.Platform) -> InstallReport:
        return self._do(plat)

    def install_windows(self, plat: platform.Platform) -> InstallReport:
        return self._do(plat)

    def _do(self, plat: platform.Platform) -> InstallReport:
        if binary.which(self.binary_name):
            # uv already in place — prefer the in-place self-update path.
            ok, msg = _self_update()
            if ok:
                return InstallReport(method="uv self update", extra={"message": msg})
            # If self-update is unavailable (e.g. uv installed via Homebrew),
            # fall through to the official installer which is idempotent.

        if plat.is_windows:
            return _ps_install_windows()
        return _curl_install_unix()

    def get_state(self) -> ToolState:
        return registry_credential.augment_state(self.name, super().get_state())

    def do_configure(self) -> InstallReport:
        return registry_credential.configure_report(self.name)

    def do_uninstall(self, *, dry_run: bool = False) -> InstallReport:
        return registry_credential.uninstall_report(self.name, dry_run=dry_run)

    def extract_identity(self, state: dict[str, Any]) -> list[tuple[str, str | None]]:
        return registry_credential.identity_lines(state)


tool = UvCliTool()
