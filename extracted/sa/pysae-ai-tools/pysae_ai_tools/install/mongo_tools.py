"""Install or update mongosh + MongoDB Database Tools.

Strategy: direct downloads on every platform, no native package manager.

- mongosh: GitHub release ZIP from ``mongodb-js/mongosh``.
- Database Tools: ZIP/TGZ from ``fastdl.mongodb.org``, version pinned via the
  official manifest at ``downloads.mongodb.org/tools/db/release.json`` (the
  ``mongodb/mongo-tools`` GitHub repo has no usable releases endpoint).

Users who prefer ``brew`` or APT can still use those manually.
"""

import tempfile
from pathlib import Path
from typing import Any

import httpx
import typer

from .common import binary, github, platform
from .common.base import BaseTool, InstallReport, ToolState
from .common.download import download, extract, install_binary

MONGOSH_BIN = "mongosh"
DBTOOLS_BIN = "mongodump"  # representative binary
DBTOOLS_ALL = (
    "mongodump",
    "mongorestore",
    "mongoimport",
    "mongoexport",
    "mongostat",
    "mongotop",
    "bsondump",
    "mongofiles",
)
TOOLS_MANIFEST = "https://downloads.mongodb.org/tools/db/release.json"
MONGOSH_RELEASES_API = "https://api.github.com/repos/mongodb-js/mongosh/releases/latest"


def _arch_token(plat: platform.Platform) -> str:
    return "x86_64" if plat.arch.value == "x86_64" else "arm64"


def _distro_token(plat: platform.Platform) -> str:
    """MongoDB tools archives are keyed by distro. Pick a sensible default per OS."""
    if plat.is_linux:
        return "ubuntu2404"
    if plat.is_macos:
        return "macos"
    if plat.is_windows:
        return "windows"
    return "ubuntu2404"


def latest_tools_version(timeout: float = 5.0) -> str:
    """Latest database-tools version from the official manifest."""
    r = httpx.get(TOOLS_MANIFEST, timeout=timeout, follow_redirects=True)
    r.raise_for_status()
    data = r.json()
    versions = data.get("versions") or []
    if not versions:
        return ""
    version = versions[0].get("version", "")
    return version if isinstance(version, str) else ""


def tools_archive_url(version: str, plat: platform.Platform) -> tuple[str, str]:
    """Return (url, archive extension)."""
    distro = _distro_token(plat)
    arch = _arch_token(plat)
    # macOS tools archives are distributed as .zip (like Windows); only Linux
    # uses .tgz. Requesting macos-*.tgz returns HTTP 403.
    if plat.is_windows or plat.is_macos:
        return (
            f"https://fastdl.mongodb.org/tools/db/mongodb-database-tools-{distro}-{arch}-{version}.zip",
            "zip",
        )
    return (
        f"https://fastdl.mongodb.org/tools/db/mongodb-database-tools-{distro}-{arch}-{version}.tgz",
        "tgz",
    )


def _mongosh_release(timeout: float = 5.0) -> dict[str, Any]:
    r = github.github_get(MONGOSH_RELEASES_API, timeout=timeout)
    data: dict[str, Any] = r.json()
    return data


def _mongosh_asset_name(plat: platform.Platform, version: str) -> str:
    """Return the GitHub release asset name for the current platform."""
    if plat.is_windows:
        return f"mongosh-{version}-win32-x64.zip"
    if plat.is_macos:
        suffix = "arm64" if plat.arch.value == "arm64" else "x64"
        return f"mongosh-{version}-darwin-{suffix}.zip"
    # Linux
    suffix = "arm64" if plat.arch.value == "arm64" else "x64"
    return f"mongosh-{version}-linux-{suffix}.tgz"


def _install_mongosh(plat: platform.Platform) -> tuple[str, str]:
    """Return (installed_version, error). Downloads the official ZIP/TGZ."""
    if binary.which(MONGOSH_BIN):
        # Already installed — let get_state surface the version separately.
        return "already-installed", ""
    try:
        release = _mongosh_release()
    except Exception as exc:  # noqa: BLE001
        return "", f"could not fetch mongosh version: {exc}"
    tag = release.get("tag_name", "")
    if not isinstance(tag, str) or not tag:
        return "", "mongosh release has no tag_name"
    version = tag.lstrip("v")

    asset_name = _mongosh_asset_name(plat, version)
    asset_url = ""
    for asset in release.get("assets", []) or []:
        if asset.get("name") == asset_name:
            url = asset.get("browser_download_url", "")
            if isinstance(url, str):
                asset_url = url
                break
    if not asset_url:
        return "", f"mongosh asset not found: {asset_name}"

    archive_ext = "zip" if asset_name.endswith(".zip") else "tgz"
    bin_name = "mongosh.exe" if plat.is_windows else "mongosh"

    with tempfile.TemporaryDirectory(prefix="pysae-mongosh-") as tmp_dir:
        tmp = Path(tmp_dir)
        archive = tmp / f"mongosh.{archive_ext}"
        try:
            download(asset_url, archive)
        except Exception as exc:  # noqa: BLE001
            return "", f"download failed for {asset_url}: {exc}"
        extract_dir = tmp / "extracted"
        try:
            extract(archive, extract_dir)
        except Exception as exc:  # noqa: BLE001
            return "", f"extract failed: {exc}"

        matches = list(extract_dir.rglob(bin_name))
        if not matches:
            return "", f"{bin_name} not found in archive"
        try:
            install_binary(matches[0], "mongosh")
        except Exception as exc:  # noqa: BLE001
            return "", f"install mongosh failed: {exc}"

    return version, ""


def _install_dbtools(plat: platform.Platform) -> tuple[str, str]:
    """Return (installed_version, error)."""
    try:
        version = latest_tools_version()
    except Exception as exc:  # noqa: BLE001
        return "", f"could not fetch tools version: {exc}"

    url, ext = tools_archive_url(version, plat)

    with tempfile.TemporaryDirectory(prefix="pysae-mongo-tools-") as tmp_dir:
        tmp = Path(tmp_dir)
        archive = tmp / f"tools.{ext}"
        try:
            download(url, archive)
        except Exception as exc:  # noqa: BLE001
            return "", f"download failed for {url}: {exc}"
        extract_dir = tmp / "extracted"
        try:
            extract(archive, extract_dir)
        except Exception as exc:  # noqa: BLE001
            return "", f"extract failed: {exc}"

        # Find each binary in the extracted bin/ folder and install it
        bin_suffix = ".exe" if plat.is_windows else ""
        for tool in DBTOOLS_ALL:
            tool_name = f"{tool}{bin_suffix}"
            matches = list(extract_dir.rglob(tool_name))
            if not matches:
                continue
            try:
                install_binary(matches[0], tool)
            except Exception as exc:  # noqa: BLE001
                return "", f"install {tool} failed: {exc}"

    return version, ""


class MongoToolsTool(BaseTool):
    name = "mongo-tools"
    cli_help = "Install/update MongoDB CLI tools (mongosh, mongodump, ...)"

    def binary_names(self) -> tuple[str, ...]:
        return (MONGOSH_BIN, DBTOOLS_BIN)

    def get_state(self) -> ToolState:
        mongosh = binary.status(MONGOSH_BIN, version_arg="--version")
        dbtools = binary.status(DBTOOLS_BIN, version_arg="--version")
        try:
            latest = latest_tools_version()
        except Exception:  # noqa: BLE001
            latest = ""

        needs_install_mongosh = not mongosh.installed
        needs_install_dbtools = not dbtools.installed
        needs_update_dbtools = dbtools.installed and bool(latest) and binary.needs_update(dbtools.version, latest)

        return ToolState(
            needs_install=needs_install_mongosh or needs_install_dbtools,
            needs_update=needs_update_dbtools,
            extra={
                "mongosh": mongosh.to_dict(),
                "dbtools": dbtools.to_dict(),
                "latest_tools": latest,
            },
        )

    def do_install(self) -> InstallReport:
        try:
            plat = platform.detect()
        except ValueError as exc:
            return InstallReport(error=str(exc))

        # winget's MongoDB.Shell / MongoDB.DatabaseTools installs were failing
        # silently with empty output. Use direct downloads everywhere:
        # mongosh ZIP from GitHub, dbtools from fastdl.mongodb.org.
        method, err1 = _install_mongosh(plat)
        version, err2 = _install_dbtools(plat)
        if err1 and err2:
            return InstallReport(error=f"mongosh: {err1}; dbtools: {err2}")
        if err2:
            return InstallReport(
                extra={"mongosh_method": method},
                error=f"dbtools: {err2}",
            )
        if err1:
            return InstallReport(
                version=version,
                extra={"mongosh_error": err1, "dbtools_version": version},
                error=f"mongosh: {err1}",
            )
        return InstallReport(
            version=version,
            extra={"mongosh_method": method, "dbtools_version": version},
        )

    def format_check(self, state: ToolState) -> None:
        d = state.to_dict()
        mongosh = d.get("mongosh", {})
        dbtools = d.get("dbtools", {})
        latest = d.get("latest_tools", "n/a")
        mongosh_version = mongosh.get("version", "") if isinstance(mongosh, dict) else ""
        dbtools_version = dbtools.get("version", "") if isinstance(dbtools, dict) else ""
        typer.echo(f"mongosh: {mongosh_version or 'NOT installed'}")
        typer.echo(f"mongodump: {dbtools_version or 'NOT installed'} (latest tools {latest})")

    def format_install(self, report: InstallReport) -> None:
        if report.error:
            typer.echo(f"FAILED: {report.error}", err=True)
        else:
            method = report.extra.get("mongosh_method", "")
            version = report.extra.get("dbtools_version", "")
            typer.echo(f"installed mongosh ({method}) and tools v{version}")


tool = MongoToolsTool()
