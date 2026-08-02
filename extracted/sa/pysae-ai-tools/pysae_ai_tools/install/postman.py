"""Install Postman desktop application.

- Linux: download tarball from dl.pstmn.io, extract to /opt/Postman, symlink to /usr/local/bin.
- macOS: prefer Homebrew (cask), else download zip and extract to /Applications.
- Windows: report manual install steps (GUI installer cannot be silenced reliably).
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import typer

from .common import desktop, platform
from .common.base import BaseTool, InstallReport, ToolState
from .common.download import download, extract


def detect_status() -> dict[str, object]:
    """Cross-platform Postman detection."""
    if shutil.which("postman"):
        return {"installed": True, "path": shutil.which("postman")}
    candidates = [
        Path("/opt/Postman/Postman"),
        Path("/Applications/Postman.app"),
        Path(os.environ.get("LOCALAPPDATA", "")) / "Postman" / "Postman.exe",
    ]
    for c in candidates:
        if c.exists():
            return {"installed": True, "path": str(c)}
    return {"installed": False, "path": ""}


def _detect_version(path: str) -> str:
    """Read Postman version from its embedded package.json (no UI launch)."""
    if not path:
        return ""
    import json

    resolved = Path(path).resolve()
    base = resolved.parent if resolved.name in ("Postman", "Postman.exe") else resolved
    candidates = [
        base / "app" / "resources" / "app" / "package.json",  # Linux /opt/Postman/
        base / "resources" / "app" / "package.json",  # Linux /opt/Postman/app/
        base / "Contents" / "Resources" / "app" / "package.json",  # macOS .app
    ]
    for c in candidates:
        if c.exists():
            try:
                data = json.loads(c.read_text(encoding="utf-8"))
                return str(data.get("version", ""))
            except Exception:  # noqa: BLE001
                pass
    return ""


def _install_linux(arch: str) -> InstallReport:
    arch_token = "linux_64" if arch == "x86_64" else "linux_arm64"
    url = f"https://dl.pstmn.io/download/latest/{arch_token}"
    with tempfile.TemporaryDirectory(prefix="pysae-postman-") as tmp_dir:
        tmp = Path(tmp_dir)
        archive = tmp / "postman.tar.gz"
        try:
            download(url, archive)
        except Exception as exc:  # noqa: BLE001
            return InstallReport(error=f"download failed: {exc}")

        # Extract to /opt/Postman via sudo
        try:
            subprocess.run(["sudo", "rm", "-rf", "/opt/Postman"], check=True, capture_output=True)
            subprocess.run(["sudo", "tar", "-xzf", str(archive), "-C", "/opt/"], check=True, capture_output=True)
            subprocess.run(
                ["sudo", "ln", "-sf", "/opt/Postman/Postman", "/usr/local/bin/postman"],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as exc:
            err = exc.stderr.decode() if exc.stderr else str(exc)
            return InstallReport(error=f"install failed: {err}")

    # Desktop entry. Declare the postman:// URL scheme (MimeType + %u) so the
    # OAuth2 "Authorize using browser" flow can return the auth code to the app,
    # and StartupWMClass so the running window groups with this launcher.
    apps_dir = Path.home() / ".local" / "share" / "applications"
    apps_dir.mkdir(parents=True, exist_ok=True)
    (apps_dir / "postman.desktop").write_text(
        "[Desktop Entry]\n"
        "Type=Application\n"
        "Name=Postman\n"
        "Icon=/opt/Postman/app/resources/app/assets/icon.png\n"
        "Exec=/opt/Postman/Postman %u\n"
        "Categories=Development;\n"
        "Terminal=false\n"
        "StartupWMClass=Postman\n"
        "MimeType=x-scheme-handler/postman;\n",
        encoding="utf-8",
        errors="replace",
    )
    scheme = desktop.register_url_scheme(apps_dir, "postman.desktop", "postman")
    return InstallReport(method="tarball", path="/opt/Postman/Postman", extra={"url_scheme": scheme})


def _install_macos(arch: str) -> InstallReport:
    if shutil.which("brew"):
        r = subprocess.run(
            ["brew", "install", "--cask", "postman"], capture_output=True, text=True, encoding="utf-8", check=False
        )
        if r.returncode == 0:
            return InstallReport(method="brew", path="/Applications/Postman.app")
        # Brew may refuse to overwrite an existing install — fall through to manual zip
    arch_token = "osx_arm64" if arch == "arm64" else "osx_64"
    url = f"https://dl.pstmn.io/download/latest/{arch_token}"
    with tempfile.TemporaryDirectory(prefix="pysae-postman-") as tmp_dir:
        tmp = Path(tmp_dir)
        archive = tmp / "Postman.zip"
        try:
            download(url, archive)
            extract(archive, Path("/Applications"))
        except Exception as exc:  # noqa: BLE001
            return InstallReport(error=f"install failed: {exc}")
    return InstallReport(method="zip", path="/Applications/Postman.app")


def _install_windows() -> InstallReport:
    from .common import winget

    r = winget.install("Postman.Postman")
    if r is not None:
        return r
    return InstallReport(
        extra={
            "manual": (
                "Postman on Windows requires the GUI installer. Download from "
                "https://www.postman.com/downloads/ or run `winget install Postman.Postman`."
            ),
        },
    )


class PostmanTool(BaseTool):
    name = "postman"
    cli_help = "Install the Postman desktop application"

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
            typer.echo(f"postman:{version_str} installed at {path}")
        else:
            typer.echo("postman: NOT installed")

    def format_install(self, report: InstallReport) -> None:
        if report.error:
            typer.echo(f"FAILED: {report.error}", err=True)
        elif report.method:
            typer.echo(f"installed postman via {report.method} at {report.path}")
            scheme = report.extra.get("url_scheme")
            if scheme and scheme != "registered":
                typer.echo(
                    "  note: could not register the postman:// URL scheme"
                    f" ({scheme}) — OAuth2 'Authorize using browser' may not return the token",
                    err=True,
                )
        else:
            manual = report.extra.get("manual", "")
            if manual:
                typer.echo(str(manual))


tool = PostmanTool()
