"""Install or update Terraform from releases.hashicorp.com."""

import httpx

from .common import platform
from .common.base import ArchiveBinaryTool


class TerraformTool(ArchiveBinaryTool):
    name = "terraform"
    binary_name = "terraform"
    version_arg = "version"
    cli_help = "Install/update the Terraform CLI"
    winget_package = "Hashicorp.Terraform"
    # No brew_package on purpose: Homebrew moved terraform to the
    # hashicorp/tap (the core formula is gone, `brew install terraform` fails
    # with "No available formula"). The direct releases.hashicorp.com download
    # in archive_info() works on every OS, so we always use it on macOS.

    def fetch_latest_version(self) -> str:
        r = httpx.get("https://checkpoint-api.hashicorp.com/v1/check/terraform", timeout=5.0, follow_redirects=True)
        r.raise_for_status()
        v = r.json().get("current_version", "")
        return str(v) if v else ""

    def archive_info(self, version: str, plat: platform.Platform) -> tuple[str, str | None]:
        ver = version.lstrip("v")
        arch = "amd64" if plat.arch.value == "x86_64" else plat.arch.value
        member = "terraform.exe" if plat.is_windows else "terraform"
        return f"https://releases.hashicorp.com/terraform/{ver}/terraform_{ver}_{plat.os.value}_{arch}.zip", member


tool = TerraformTool()
