"""Install or update AWS CLI v2."""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import typer

from ..common import winpath
from .common import binary, github, platform
from .common.base import BinaryTool, InstallReport
from .common.download import download, extract

# AWS CLI v2's documented symlink location on Linux and macOS. Used only as a
# fallback when the freshly installed binary isn't yet on the process PATH.
_POSIX_AWS_PATH = "/usr/local/bin/aws"


class AwsCliTool(BinaryTool):
    name = "aws"
    binary_name = "aws"
    cli_help = "Install/update the AWS CLI and configure SSO profiles"
    winget_package = "Amazon.AWSCLI"
    # Post-configure: the values are written via `aws configure`, which needs the
    # binary on PATH. Resolved AFTER install.
    env_post_configure = ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_DEFAULT_REGION")
    env_help = {
        "AWS_ACCESS_KEY_ID": "saisi en interactif via `aws configure`, persisté dans ~/.aws/credentials",
        "AWS_SECRET_ACCESS_KEY": "saisi avec AWS_ACCESS_KEY_ID (paire), persisté dans ~/.aws/credentials",
        "AWS_DEFAULT_REGION": "écrite par `aws configure` dans ~/.aws/config (défaut Pysae : eu-west-3)",
    }
    # No brew_package on purpose: Homebrew's awscli trails the official release
    # (e.g. 2.34.39 vs AWS's 2.35.1), so `brew install awscli` looks like a
    # silent no-op against AWS's own latest and trips the version gate. Use the
    # official AWSCLIV2.pkg via install_macos() instead.

    def fetch_latest_version(self) -> str:
        r = github.github_get("https://api.github.com/repos/aws/aws-cli/tags?per_page=1", timeout=5.0)
        data = r.json()
        if isinstance(data, list) and data:
            name = data[0].get("name", "")
            return str(name) if isinstance(name, str) else ""
        return ""

    def check_auth(self) -> dict[str, Any] | None:
        if not binary.which(self.binary_name):
            return {"auth_ok": False, "auth_message": "aws not installed", "profiles": []}
        try:
            r = subprocess.run(
                [self.binary_name, "sts", "get-caller-identity"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=10,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return {"auth_ok": False, "auth_message": f"sts get-caller-identity failed: {exc}", "profiles": []}
        try:
            profiles_r = subprocess.run(
                [self.binary_name, "configure", "list-profiles"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=5,
            )
            profiles = [line.strip() for line in profiles_r.stdout.splitlines() if line.strip()]
        except (OSError, subprocess.TimeoutExpired):
            profiles = []
        return {
            "auth_ok": r.returncode == 0,
            "auth_message": (r.stdout + r.stderr).strip(),
            "profiles": profiles,
        }

    def _finalize(self, path: str) -> InstallReport:
        if sys.platform != "win32":
            shutil.which(self.binary_name)
        installed_v = binary.get_version(self.binary_name, version_arg="--version")
        return InstallReport(version=installed_v, path=path)

    def install_linux(self, plat: platform.Platform) -> InstallReport:
        with tempfile.TemporaryDirectory(prefix="pysae-aws-") as tmp_dir:
            tmp = Path(tmp_dir)
            arch_token = "x86_64" if plat.arch.value == "x86_64" else "aarch64"
            url = f"https://awscli.amazonaws.com/awscli-exe-linux-{arch_token}.zip"
            archive = tmp / "awscliv2.zip"
            try:
                download(url, archive)
                extract(archive, tmp / "awscli")
            except Exception as exc:  # noqa: BLE001
                return InstallReport(error=f"download/extract failed: {exc}")
            installer = tmp / "awscli" / "aws" / "install"
            installer.chmod(0o755)
            r = subprocess.run(
                ["sudo", str(installer), "--update"], capture_output=True, text=True, encoding="utf-8", check=False
            )
            if r.returncode != 0:
                r = subprocess.run(
                    ["sudo", str(installer)], capture_output=True, text=True, encoding="utf-8", check=False
                )
            if r.returncode != 0:
                return InstallReport(error=r.stderr.strip() or r.stdout.strip())
        # The installer symlinks aws into /usr/local/bin; make sure it is on the
        # process PATH so in-process `aws` calls later in the same run (e.g.
        # `current_aws_username` during `install all`) find the fresh binary
        # without a shell restart — mirrors the macOS branch below.
        os.environ["PATH"] = f"/usr/local/bin{os.pathsep}{os.environ.get('PATH', '')}"
        return self._finalize(binary.which(self.binary_name) or _POSIX_AWS_PATH)

    def install_macos(self, plat: platform.Platform) -> InstallReport:
        with tempfile.TemporaryDirectory(prefix="pysae-aws-") as tmp_dir:
            pkg = Path(tmp_dir) / "AWSCLIV2.pkg"
            try:
                download("https://awscli.amazonaws.com/AWSCLIV2.pkg", pkg)
            except Exception as exc:  # noqa: BLE001
                return InstallReport(error=f"download failed: {exc}")
            r = subprocess.run(
                ["sudo", "installer", "-pkg", str(pkg), "-target", "/"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            if r.returncode != 0:
                return InstallReport(error=r.stderr.strip() or r.stdout.strip())
        # The pkg symlinks aws into /usr/local/bin; make sure it wins over any
        # pre-existing aws (e.g. a Homebrew one under /opt/homebrew/bin, which
        # precedes /usr/local/bin in PATH on Apple Silicon) when we read the
        # version back — otherwise the install looks like a no-op update.
        os.environ["PATH"] = f"/usr/local/bin{os.pathsep}{os.environ.get('PATH', '')}"
        return self._finalize(binary.which(self.binary_name) or _POSIX_AWS_PATH)

    def install_windows(self, plat: platform.Platform) -> InstallReport:
        with tempfile.TemporaryDirectory(prefix="pysae-aws-") as tmp_dir:
            msi = Path(tmp_dir) / "AWSCLIV2.msi"
            try:
                download("https://awscli.amazonaws.com/AWSCLIV2.msi", msi)
            except Exception as exc:  # noqa: BLE001
                return InstallReport(error=f"download failed: {exc}")
            r = subprocess.run(
                # Per-user install: lands under %LOCALAPPDATA% and extends the
                # *user* PATH — no admin needed, nothing touches the machine PATH.
                ["msiexec", "/i", str(msi), "/qn", "/norestart", "MSIINSTALLPERUSER=1", "ALLUSERS=2"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            if r.returncode != 0:
                return InstallReport(error=f"msiexec exited {r.returncode}: {r.stderr.strip() or r.stdout.strip()}")
            # The MSI extended the registry PATH; merge it into this process so
            # the version read-back below finds the freshly installed aws.exe.
            winpath.refresh_process_path_from_registry(force=True)
            local_app = os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local"))
            default = Path(local_app) / "Programs" / "Amazon" / "AWSCLIV2" / "aws.exe"
        return self._finalize(binary.which(self.binary_name) or str(default))

    def extract_identity(self, state: dict[str, Any]) -> list[tuple[str, str | None]]:
        lines: list[tuple[str, str | None]] = []
        msg = str(state.get("auth_message", ""))
        m = re.search(r'"Arn":\s*"arn:aws:iam::(\d+):user/([^"]+)"', msg)
        if m:
            lines.append((f"{m.group(2)} (account {m.group(1)})", typer.colors.BRIGHT_BLACK))
        for p in state.get("profiles", []):
            lines.append((f"  profile: {p}", typer.colors.BRIGHT_BLACK))
        return lines


tool = AwsCliTool()
