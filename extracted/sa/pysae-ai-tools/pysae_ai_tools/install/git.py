"""Install and verify git, and wire glab as the gitlab.com credential helper.

- Linux: uses the distro package manager (``apt``, ``dnf``, ``yum``, ``pacman``,
  ``apk``) via ``sudo``.
- macOS: ``brew install git`` when Homebrew is available, otherwise falls back
  to triggering ``xcode-select --install`` (the Xcode CLT bundles git).
- Windows: ``winget install Git.Git`` when winget is available, otherwise
  reports the Git for Windows download URL.

When glab is installed, the tool wires ``glab auth git-credential`` as the
credential helper for ``https://gitlab.com`` and tests end-to-end HTTPS access
by querying the credential chain.
"""

import shutil
import subprocess
from typing import Any

import typer

from .common import binary, platform
from .common.base import BaseTool, InstallReport, ToolState

GITLAB_HOST = "https://gitlab.com"
CREDENTIAL_KEY = f"credential.{GITLAB_HOST}.helper"
GLAB_HELPER_CMD = "!glab auth git-credential"

# Set globally by `git lfs install` — proves the smudge/clean filters are wired.
LFS_FILTER_KEY = "filter.lfs.process"
WINGET_GIT_LFS = "GitHub.GitLFS"


def _git_config_get(key: str) -> str:
    r = subprocess.run(
        ["git", "config", "--global", "--get", key],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        timeout=5,
    )
    return r.stdout.strip() if r.returncode == 0 else ""


def _git_config_get_all(key: str) -> list[str]:
    r = subprocess.run(
        ["git", "config", "--global", "--get-all", key],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        timeout=5,
    )
    if r.returncode != 0:
        return []
    return [line for line in r.stdout.splitlines() if line.strip() != ""] or ([""] if r.stdout else [])


def _glab_helper_configured() -> bool:
    """True when glab is set up as the credential helper for gitlab.com."""
    values = _git_config_get_all(CREDENTIAL_KEY)
    if not values:
        return False
    joined = " ".join(values)
    # Accept either the shell form (!glab ...) or a `git-credential-glab` binary shim.
    return "glab" in joined


def _configure_glab_helper() -> tuple[bool, str]:
    """Write the glab credential helper into ~/.gitconfig. Returns (ok, message)."""
    if not binary.which("glab"):
        return False, "glab not installed"
    # Reset any existing chain for gitlab.com, then install glab as the only helper.
    subprocess.run(
        ["git", "config", "--global", "--unset-all", CREDENTIAL_KEY],
        check=False,
        capture_output=True,
        timeout=5,
    )
    for value in ("", GLAB_HELPER_CMD):
        r = subprocess.run(
            ["git", "config", "--global", "--add", CREDENTIAL_KEY, value],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=5,
        )
        if r.returncode != 0:
            return False, r.stderr.strip() or "git config failed"
    return True, "configured"


def _check_gitlab_access() -> tuple[bool, str]:
    """Ask git to fill credentials for gitlab.com — proves the helper chain works."""
    if not binary.which("git"):
        return False, "git not installed"
    r = subprocess.run(
        ["git", "credential", "fill"],
        input="protocol=https\nhost=gitlab.com\n\n",
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        timeout=15,
    )
    if r.returncode != 0:
        return False, (r.stderr.strip().splitlines() or ["credential fill failed"])[-1]
    out = r.stdout
    if "username=" in out and "password=" in out:
        return True, "credentials available"
    return False, "no credentials returned"


# ---------------------------------------------------------------------------
# Platform-specific installers
# ---------------------------------------------------------------------------


def _install_linux_pkg(pkg: str) -> InstallReport:
    managers: list[tuple[str, list[str]]] = [
        ("apt-get", ["sudo", "apt-get", "update"]),
        ("apt-get", ["sudo", "apt-get", "install", "-y", pkg]),
        ("dnf", ["sudo", "dnf", "install", "-y", pkg]),
        ("yum", ["sudo", "yum", "install", "-y", pkg]),
        ("pacman", ["sudo", "pacman", "-S", "--noconfirm", pkg]),
        ("apk", ["sudo", "apk", "add", "--no-cache", pkg]),
    ]
    tried: list[str] = []
    for name, cmd in managers:
        if not shutil.which(name):
            continue
        tried.append(name)
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=False)
        if r.returncode != 0:
            # For apt, the update step may fail on sandboxed envs — keep going to install.
            if name == "apt-get" and cmd[-1] == "update":
                continue
            return InstallReport(error=f"{name}: {r.stderr.strip() or r.stdout.strip()}")
        # Skip ahead once a package manager has run the install step.
        if name == "apt-get" and cmd[-1] != pkg:
            continue
        return InstallReport(method=name)
    if not tried:
        return InstallReport(error="no supported package manager found (apt/dnf/yum/pacman/apk)")
    return InstallReport(error=f"install failed on {', '.join(tried)}")


def _install_linux() -> InstallReport:
    return _install_linux_pkg("git")


def _install_macos() -> InstallReport:
    from .common import brew

    r = brew.install("git")
    if r is not None:
        return r
    # Trigger the Xcode Command Line Tools installer (shows a GUI dialog).
    subprocess.run(["xcode-select", "--install"], capture_output=True, text=True, encoding="utf-8", check=False)
    return InstallReport(
        extra={
            "manual": (
                "Xcode Command Line Tools installer was triggered. Accept the dialog, "
                "then re-run `pysae-ai-tools tools install git`. Alternatively, install "
                "Homebrew (https://brew.sh) and run `brew install git`."
            ),
        },
    )


def _install_windows() -> InstallReport:
    from .common import winget

    r = winget.install("Git.Git", binary_name="git")
    if r is not None:
        return r
    return InstallReport(
        extra={
            "manual": (
                "Install Git for Windows from https://git-scm.com/download/win, or run "
                "`winget install --id Git.Git -e --source winget` from an elevated shell."
            ),
        },
    )


# ---------------------------------------------------------------------------
# git-lfs
# ---------------------------------------------------------------------------


def _git_lfs_configured() -> bool:
    """True when `git lfs install` has wired the global smudge/process filters."""
    return bool(_git_config_get(LFS_FILTER_KEY))


def _install_git_lfs(plat: platform.Platform) -> tuple[bool, str]:
    """Install the git-lfs binary if missing. Returns (ok, message)."""
    if binary.which("git-lfs"):
        return True, "already installed"

    if plat.is_linux:
        report = _install_linux_pkg("git-lfs")
    elif plat.is_macos:
        from .common import brew

        report = brew.install("git-lfs") or InstallReport(
            error="Homebrew not found — install git-lfs manually (https://git-lfs.com)",
        )
    elif plat.is_windows:
        from .common import winget

        report = winget.install(WINGET_GIT_LFS, binary_name="git-lfs") or InstallReport(
            error="winget not found — install git-lfs manually (https://git-lfs.com)",
        )
    else:
        return False, f"unsupported OS: {plat.os}"

    if report.error:
        return False, report.error
    return True, report.method or "installed"


def _configure_git_lfs() -> tuple[bool, str]:
    """Run `git lfs install` to register the global smudge/clean filters."""
    if not binary.which("git-lfs"):
        return False, "git-lfs not installed"
    r = subprocess.run(
        ["git", "lfs", "install", "--skip-repo"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        timeout=10,
    )
    if r.returncode != 0:
        return False, r.stderr.strip() or r.stdout.strip() or "git lfs install failed"
    return True, "configured"


# ---------------------------------------------------------------------------
# Tool
# ---------------------------------------------------------------------------


class GitTool(BaseTool):
    name = "git"
    cli_help = "Install git, wire glab as the gitlab.com credential helper, and verify access"

    def get_state(self) -> ToolState:
        bin_status = binary.status("git", version_arg="--version")
        installed = bin_status.installed

        user_name = _git_config_get("user.name") if installed else ""
        user_email = _git_config_get("user.email") if installed else ""
        helper_ok = _glab_helper_configured() if installed else False
        glab_installed = bool(binary.which("glab"))

        lfs_installed = bool(binary.which("git-lfs"))
        lfs_configured = installed and lfs_installed and _git_lfs_configured()

        if installed:
            access_ok, access_msg = _check_gitlab_access()
        else:
            access_ok, access_msg = False, "git not installed"

        # Needs work when: git missing, OR glab is available but helper isn't set,
        # OR helper is set but access still fails, OR git-lfs is missing or not
        # registered as a global filter.
        needs_config = installed and (
            (glab_installed and (not helper_ok or not access_ok)) or not lfs_installed or not lfs_configured
        )

        return ToolState(
            needs_install=not installed,
            needs_update=needs_config,
            extra={
                "binary": bin_status.to_dict(),
                "user_name": user_name,
                "user_email": user_email,
                "glab_installed": glab_installed,
                "gitlab_credential_helper": helper_ok,
                "gitlab_access_ok": access_ok,
                "gitlab_access_message": access_msg,
                "git_lfs_installed": lfs_installed,
                "git_lfs_configured": lfs_configured,
            },
        )

    def do_install(self) -> InstallReport:
        try:
            plat = platform.detect()
        except ValueError as exc:
            return InstallReport(error=str(exc))

        # Install git binary if missing.
        report: InstallReport
        if not binary.which("git"):
            if plat.is_linux:
                report = _install_linux()
            elif plat.is_macos:
                report = _install_macos()
            elif plat.is_windows:
                report = _install_windows()
            else:
                return InstallReport(error=f"unsupported OS: {plat.os}")
            if report.error:
                return report
        else:
            report = InstallReport(action="configure", method="already installed")

        # Configure glab credential helper (best-effort — only when glab is present).
        if binary.which("glab"):
            ok, msg = _configure_glab_helper()
            report.extra["credential_helper"] = "configured" if ok else f"failed — {msg}"
        else:
            report.extra["credential_helper"] = "skipped — glab not installed"

        # Install git-lfs and register the global smudge/clean filters.
        # git-lfs ships as a separate binary that registers itself as a git
        # subcommand once `git lfs install` writes the filter config.
        lfs_ok, lfs_msg = _install_git_lfs(plat)
        if lfs_ok:
            cfg_ok, cfg_msg = _configure_git_lfs()
            report.extra["git_lfs"] = f"installed ({lfs_msg}); {cfg_msg}" if cfg_ok else f"installed but {cfg_msg}"
        else:
            report.extra["git_lfs"] = f"failed — {lfs_msg}"

        # Verify access end-to-end.
        access_ok, access_msg = _check_gitlab_access()
        report.extra["gitlab_access"] = "ok" if access_ok else f"failed — {access_msg}"

        installed_v = binary.get_version("git", version_arg="--version")
        if installed_v:
            report.version = installed_v
        path = binary.which("git")
        if path:
            report.path = path
        return report

    def format_check(self, state: ToolState) -> None:
        d = state.to_dict()
        bin_info = d.get("binary", {})
        installed = isinstance(bin_info, dict) and bin_info.get("installed", False)
        if not installed:
            typer.echo("git: NOT installed")
            return
        version = bin_info.get("version", "n/a") if isinstance(bin_info, dict) else "n/a"
        typer.echo(f"git: {version}")
        user_name = d.get("user_name", "")
        user_email = d.get("user_email", "")
        if user_name or user_email:
            typer.echo(f"  user: {user_name} <{user_email}>")
        else:
            typer.echo("  user: NOT configured")
        if d.get("glab_installed"):
            helper_ok = d.get("gitlab_credential_helper", False)
            typer.echo(f"  gitlab helper (glab): {'OK' if helper_ok else 'NOT configured'}")
        access_ok = d.get("gitlab_access_ok", False)
        access_msg = d.get("gitlab_access_message", "")
        typer.echo(f"  gitlab access: {'OK' if access_ok else f'FAILED — {access_msg}'}")
        lfs_installed = d.get("git_lfs_installed", False)
        lfs_configured = d.get("git_lfs_configured", False)
        if lfs_installed and lfs_configured:
            typer.echo("  git-lfs: OK")
        elif lfs_installed:
            typer.echo("  git-lfs: installed but NOT configured (run `git lfs install`)")
        else:
            typer.echo("  git-lfs: NOT installed")

    def format_install(self, report: InstallReport) -> None:
        if report.error:
            typer.echo(f"FAILED: {report.error}", err=True)
            return
        line = "git installed" if report.method and report.method != "already installed" else "git already installed"
        if report.version:
            line += f" ({report.version})"
        if report.method and report.method != "already installed":
            line += f" via {report.method}"
        typer.echo(line)
        for key in ("credential_helper", "git_lfs", "gitlab_access", "manual"):
            value = report.extra.get(key)
            if value:
                typer.echo(f"  {key.replace('_', ' ')}: {value}")

    def extract_identity(self, state: dict[str, Any]) -> list[tuple[str, str | None]]:
        lines: list[tuple[str, str | None]] = []
        user_name = state.get("user_name", "")
        user_email = state.get("user_email", "")
        if user_name or user_email:
            label = f"{user_name} <{user_email}>".strip()
            lines.append((label, typer.colors.BRIGHT_BLACK))
        if state.get("glab_installed"):
            helper_ok = state.get("gitlab_credential_helper", False)
            icon = "✓" if helper_ok else "✗"
            color = typer.colors.GREEN if helper_ok else typer.colors.YELLOW
            lines.append((f"{icon} glab credential helper", color))
        access_ok = state.get("gitlab_access_ok", False)
        icon = "✓" if access_ok else "✗"
        color = typer.colors.GREEN if access_ok else typer.colors.RED
        msg = state.get("gitlab_access_message", "")
        suffix = "" if access_ok else f" — {msg}"
        lines.append((f"{icon} gitlab.com access{suffix}", color))
        lfs_installed = state.get("git_lfs_installed", False)
        lfs_configured = state.get("git_lfs_configured", False)
        lfs_ok = lfs_installed and lfs_configured
        icon = "✓" if lfs_ok else "✗"
        color = typer.colors.GREEN if lfs_ok else typer.colors.YELLOW
        if not lfs_installed:
            label = "git-lfs (not installed)"
        elif not lfs_configured:
            label = "git-lfs (not configured)"
        else:
            label = "git-lfs"
        lines.append((f"{icon} {label}", color))
        return lines


tool = GitTool()
