"""Install or update the Helm CLI from get.helm.sh."""

from .common import github, platform
from .common.base import ArchiveBinaryTool


class HelmTool(ArchiveBinaryTool):
    name = "helm"
    binary_name = "helm"
    version_arg = "version"
    cli_help = "Install/update the Helm CLI"
    winget_package = "Helm.Helm"
    brew_package = "helm"

    def fetch_latest_version(self) -> str:
        return github.latest_release("helm/helm")

    def archive_info(self, version: str, plat: platform.Platform) -> tuple[str, str | None]:
        ver = f"v{version}" if not version.startswith("v") else version
        arch = "amd64" if plat.arch.value == "x86_64" else plat.arch.value
        if plat.is_windows:
            return f"https://get.helm.sh/helm-{ver}-windows-{arch}.zip", f"windows-{arch}/helm.exe"
        os_name = plat.os.value
        return f"https://get.helm.sh/helm-{ver}-{os_name}-{arch}.tar.gz", f"{os_name}-{arch}/helm"


tool = HelmTool()
