"""Install the Bruno desktop application (open-source API client).

- Linux: download the AppImage from the latest GitHub release, install it as
  the `bruno` binary (sudo to /usr/local/bin, falls back to ~/.local/bin). The
  type-2 AppImage needs ``libfuse2`` at run time; it is declared as a
  ``system_deps`` entry and provisioned by the install framework.
- macOS: prefer Homebrew (cask), else download the mac zip and extract the
  `.app` to /Applications.
- Windows: winget `Bruno.Bruno`, else report manual install steps.
"""

import os
import plistlib
import shutil
import subprocess
import tempfile
from pathlib import Path

import typer

from .common import desktop, platform, syspkg
from .common.base import BaseTool, InstallReport, ToolState
from .common.download import download, extract, install_binary
from .common.github import latest_release

REPO = "usebruno/bruno"


def detect_status() -> dict[str, object]:
    """Cross-platform Bruno detection."""
    if shutil.which("bruno"):
        return {"installed": True, "path": shutil.which("bruno")}
    candidates = [
        Path("/Applications/Bruno.app"),
        Path.home() / ".local" / "bin" / "bruno",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "bruno" / "Bruno.exe",
    ]
    for c in candidates:
        if c.exists():
            return {"installed": True, "path": str(c)}
    return {"installed": False, "path": ""}


def _detect_version(path: str) -> str:
    """Read Bruno's version from the macOS bundle's Info.plist (best-effort)."""
    if not path:
        return ""
    plist = Path("/Applications/Bruno.app/Contents/Info.plist")
    if not plist.exists():
        return ""
    try:
        data = plistlib.loads(plist.read_bytes())
        return str(data.get("CFBundleShortVersionString", ""))
    except Exception:  # noqa: BLE001
        return ""


def _latest_version() -> str:
    """Latest Bruno version (tag without the leading ``v``)."""
    return latest_release(REPO).lstrip("v")


def _install_icons(appimage: Path) -> int:
    """Extract Bruno's hicolor icons from the AppImage into the user icon theme.

    Without this the ``.desktop`` file's ``Icon=bruno`` resolves to nothing and
    the launcher shows a generic icon. The AppImage ships ``bruno.png`` at every
    hicolor size; copying them under ``~/.local/share/icons/hicolor`` makes the
    themed name resolve at the right resolution everywhere. Returns the count
    installed (0 if extraction failed).
    """
    icons_root = Path.home() / ".local" / "share" / "icons" / "hicolor"
    count = 0
    with tempfile.TemporaryDirectory(prefix="pysae-bruno-icon-") as tmp:
        try:
            subprocess.run(
                [str(appimage), "--appimage-extract", "usr/share/icons/*"],
                cwd=tmp,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                stdin=subprocess.DEVNULL,
                check=False,
            )
        except (FileNotFoundError, OSError):
            return 0
        src_root = Path(tmp) / "squashfs-root" / "usr" / "share" / "icons" / "hicolor"
        for png in src_root.glob("*/apps/bruno.png"):
            dest = icons_root / png.parent.parent.name / "apps" / "bruno.png"
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(png, dest)
            count += 1
    if count and shutil.which("gtk-update-icon-cache"):
        subprocess.run(
            ["gtk-update-icon-cache", "-f", "-t", str(icons_root)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdin=subprocess.DEVNULL,
            check=False,
        )
    return count


def _install_linux(arch: str) -> InstallReport:
    arch_token = "x86_64" if arch == "x86_64" else "arm64"
    try:
        version = _latest_version()
    except Exception as exc:  # noqa: BLE001
        return InstallReport(error=f"could not resolve latest release: {exc}")
    asset = f"bruno_{version}_{arch_token}_linux.AppImage"
    url = f"https://github.com/{REPO}/releases/download/v{version}/{asset}"
    with tempfile.TemporaryDirectory(prefix="pysae-bruno-") as tmp_dir:
        appimage = Path(tmp_dir) / asset
        try:
            download(url, appimage)
            target = install_binary(appimage, "bruno")
        except Exception as exc:  # noqa: BLE001
            return InstallReport(error=f"install failed: {exc}")

    icons = _install_icons(target)

    apps_dir = Path.home() / ".local" / "share" / "applications"
    apps_dir.mkdir(parents=True, exist_ok=True)
    # Use the themed name when icons were installed, else fall back to the binary
    # (some launchers show nothing rather than a generic icon for a missing name).
    icon = "bruno" if icons else str(target)
    # Mirror the .desktop Bruno ships inside the AppImage: --no-sandbox (needed on
    # kernels that restrict unprivileged user namespaces, else Electron crashes at
    # launch), StartupWMClass so the window groups with this launcher, and the
    # bruno:// URL scheme for the browser OAuth2 flow.
    (apps_dir / "bruno.desktop").write_text(
        "[Desktop Entry]\n"
        "Type=Application\n"
        "Name=Bruno\n"
        "Comment=Opensource API client for exploring and testing APIs\n"
        f"Icon={icon}\n"
        f"Exec={target} --no-sandbox %U\n"
        "Categories=Development;\n"
        "Terminal=false\n"
        "StartupWMClass=Bruno\n"
        "MimeType=x-scheme-handler/bruno;\n",
        encoding="utf-8",
        errors="replace",
    )
    scheme = desktop.register_url_scheme(apps_dir, "bruno.desktop", "bruno")
    return InstallReport(
        method="appimage", path=str(target), extra={"version": version, "icons": icons, "url_scheme": scheme}
    )


def _install_macos(arch: str) -> InstallReport:
    if shutil.which("brew"):
        r = subprocess.run(
            ["brew", "install", "--cask", "bruno"], capture_output=True, text=True, encoding="utf-8", check=False
        )
        if r.returncode == 0:
            return InstallReport(method="brew", path="/Applications/Bruno.app")
        # Brew may refuse to overwrite an existing install — fall through to manual zip
    arch_token = "arm64" if arch == "arm64" else "x64"
    try:
        version = _latest_version()
    except Exception as exc:  # noqa: BLE001
        return InstallReport(error=f"could not resolve latest release: {exc}")
    asset = f"bruno_{version}_{arch_token}_mac.zip"
    url = f"https://github.com/{REPO}/releases/download/v{version}/{asset}"
    with tempfile.TemporaryDirectory(prefix="pysae-bruno-") as tmp_dir:
        archive = Path(tmp_dir) / asset
        try:
            download(url, archive)
            extract(archive, Path("/Applications"))
        except Exception as exc:  # noqa: BLE001
            return InstallReport(error=f"install failed: {exc}")
    return InstallReport(method="zip", path="/Applications/Bruno.app", extra={"version": version})


def _install_windows() -> InstallReport:
    from .common import winget

    r = winget.install("Bruno.Bruno")
    if r is not None:
        return r
    return InstallReport(
        extra={
            "manual": (
                "Bruno on Windows requires the GUI installer. Download from "
                "https://www.usebruno.com/downloads or run `winget install Bruno.Bruno`."
            ),
        },
    )


class BrunoTool(BaseTool):
    name = "bruno"
    cli_help = "Install the Bruno desktop application (open-source API client)"

    @property
    def system_deps(self) -> list[syspkg.SystemDep]:
        # The type-2 AppImage needs libfuse2 to mount at run time (Linux only;
        # macOS/Windows ship a native app bundle with no such dependency).
        try:
            if platform.detect().is_linux:
                return [syspkg.LIBFUSE2]
        except ValueError:
            pass
        return []

    def get_state(self) -> ToolState:
        status = detect_status()
        path = str(status.get("path", ""))
        installed = bool(status.get("installed"))
        version = _detect_version(path)
        return ToolState(
            needs_install=not installed,
            extra={
                "installed": installed,
                "path": path,
                "version": version,
            },
        )

    def do_install(self) -> InstallReport:
        try:
            plat = platform.detect()
        except ValueError as exc:
            return InstallReport(error=str(exc))
        if plat.is_linux:
            return _install_linux(plat.arch.value)
        if plat.is_macos:
            return _install_macos(plat.arch.value)
        if plat.is_windows:
            return _install_windows()
        return InstallReport(error=f"unsupported OS: {plat.os}")

    def format_check(self, state: ToolState) -> None:
        d = state.to_dict()
        installed = d.get("installed", False)
        if installed:
            version = d.get("version", "")
            path = d.get("path", "")
            version_str = f" {version}" if version else ""
            typer.echo(f"bruno:{version_str} installed at {path}")
        else:
            typer.echo("bruno: NOT installed")

    def format_install(self, report: InstallReport) -> None:
        if report.error:
            typer.echo(f"FAILED: {report.error}", err=True)
        elif report.method:
            typer.echo(f"installed bruno via {report.method} at {report.path}")
        else:
            manual = report.extra.get("manual", "")
            if manual:
                typer.echo(str(manual))


tool = BrunoTool()
