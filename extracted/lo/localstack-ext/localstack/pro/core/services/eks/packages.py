_A='velero'
import os.path
from localstack.packages import Package,PackageInstaller
from localstack.packages.core import ArchiveDownloadAndExtractInstaller,GitHubReleaseInstaller,SystemNotSupportedException
from localstack.utils.platform import get_arch,is_linux,is_mac_os
DEFAULT_K3D_VERSION='v5.8.3'
DEFAULT_VELERO_VERSION='v1.17.0'
VELERO_ZIP_URL='https://github.com/vmware-tanzu/velero/releases/download/{version}/velero-{version}-linux-{arch}.tar.gz'
class K3DPackage(Package):
	def __init__(A):super().__init__('K3D',DEFAULT_K3D_VERSION)
	def get_versions(A)->list[str]:return[DEFAULT_K3D_VERSION]
	def _get_installer(A,version:str)->PackageInstaller:return K3DPackageInstaller('k3d',version)
class K3DPackageInstaller(GitHubReleaseInstaller):
	def __init__(A,name,version):super().__init__(name,version,'rancher/k3d')
	def _get_github_asset_name(C)->str:
		A='linux'if is_linux()else'darwin'if is_mac_os()else None;B=get_arch()
		if not A:raise SystemNotSupportedException('Unsupported operating system (currently only Linux/MacOS are supported)')
		return f"k3d-{A}-{B}"
class VeleroPackage(Package):
	def __init__(A):super().__init__('Velero',DEFAULT_VELERO_VERSION)
	def get_versions(A)->list[str]:return[DEFAULT_VELERO_VERSION]
	def _get_installer(A,version:str)->PackageInstaller:return VeleroPackageInstaller(_A,version)
class VeleroPackageInstaller(ArchiveDownloadAndExtractInstaller):
	def __init__(A,name,version):super().__init__(name,version,True)
	def _get_install_marker_path(A,install_dir:str)->str:return os.path.join(install_dir,_A)
	def _get_download_url(A)->str:return VELERO_ZIP_URL.format(version=A.version,arch=get_arch())
k3d_package=K3DPackage()
velero_package=VeleroPackage()