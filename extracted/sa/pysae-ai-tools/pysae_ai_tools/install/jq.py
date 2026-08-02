"""Install or update jq from GitHub releases."""

import shutil
from pathlib import Path

from .common import binary, github, platform
from .common.base import BinaryTool, InstallReport

GITHUB_REPO = "jqlang/jq"


class JqTool(BinaryTool):
    name = "jq"
    binary_name = "jq"
    cli_help = "Install/update jq (command-line JSON processor)"
    winget_package = "jqlang.jq"
    # No brew_package on purpose: Homebrew trails jq's GitHub releases (e.g. brew
    # ships 1.8.1 while jqlang/jq tagged 1.8.2), so `brew install jq` looks like a
    # no-op against our latest-version gate ("version did not change"). Use the
    # official GitHub binary on macOS too (install_macos → _install_from_github),
    # exactly like Linux/Windows, so the installed version always matches latest.

    def fetch_latest_version(self) -> str:
        # jq tags look like "jq-1.7.1" — strip the prefix so the version
        # comparison in BinaryTool.get_state() works against `jq --version`
        # which prints "jq-1.7.1".
        tag = github.latest_release(GITHUB_REPO)
        return tag.removeprefix("jq-")

    def _install_from_github(self, plat: platform.Platform) -> InstallReport:
        try:
            version = self.fetch_latest_version()
        except Exception as exc:  # noqa: BLE001
            return InstallReport(error=f"could not fetch latest version: {exc}")

        arch = "amd64" if plat.arch.value == "x86_64" else plat.arch.value
        if plat.is_linux:
            asset = f"jq-linux-{arch}"
        elif plat.is_macos:
            asset = f"jq-macos-{arch}"
        elif plat.is_windows:
            asset = f"jq-windows-{arch}.exe"
        else:
            return InstallReport(error=f"unsupported OS: {plat.os}")

        url = f"https://github.com/{GITHUB_REPO}/releases/download/jq-{version}/{asset}"

        from .common.download import download_and_install_binary

        try:
            path = download_and_install_binary(url, self.binary_name)
        except Exception as exc:  # noqa: BLE001
            return InstallReport(error=f"download/install failed: {exc}")
        self._make_installed_jq_win(path)
        installed_v = binary.get_version(self.binary_name, version_arg=self.version_arg)
        return InstallReport(version=installed_v or version, path=str(path))

    def _make_installed_jq_win(self, installed: Path) -> None:
        """Ensure the jq just installed is the one PATH resolves.

        On macOS Apple Silicon a Homebrew jq in ``/opt/homebrew/bin`` (ahead of
        ``/usr/local/bin`` on PATH) shadows our install, so ``jq --version`` keeps
        reporting Homebrew's older build and the latest-version gate fails. Replace
        whatever ``jq`` currently resolves to with our freshly downloaded binary so the
        GitHub release wins — leaving Homebrew's Cellar untouched (we overwrite the shim,
        not its target). Best-effort: the standard install already put jq on PATH.
        """
        resolved = shutil.which(self.binary_name)
        if not resolved:
            return
        resolved_path = Path(resolved)
        try:
            if resolved_path.resolve() == installed.resolve():
                return
            if resolved_path.is_symlink() or resolved_path.exists():
                resolved_path.unlink()
            shutil.copyfile(installed, resolved_path)
            resolved_path.chmod(0o755)
        except OSError:
            pass

    def install_linux(self, plat: platform.Platform) -> InstallReport:
        return self._install_from_github(plat)

    def install_macos(self, plat: platform.Platform) -> InstallReport:
        return self._install_from_github(plat)

    def install_windows(self, plat: platform.Platform) -> InstallReport:
        return self._install_from_github(plat)


tool = JqTool()
