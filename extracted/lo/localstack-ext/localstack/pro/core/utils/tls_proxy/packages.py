from localstack.constants import ARTIFACTS_REPO
from localstack.packages import Package,PackageInstaller
from localstack.packages.core import PermissionDownloadInstaller
from localstack.utils.platform import get_arch
DEFAULT_NGINX_VERSION='1.28.0'
NGINX_DOWNLOAD_URL=ARTIFACTS_REPO+'/raw/e965a2e7f05ca5ca357cc297163c00708660effd/nginx/{version}/{platform}/nginx'
class NginxPackage(Package):
	def __init__(A):super().__init__('nginx',DEFAULT_NGINX_VERSION)
	def get_versions(A):return[DEFAULT_NGINX_VERSION]
	def _get_installer(A,version):return NginxPackageInstaller(version)
class NginxPackageInstaller(PermissionDownloadInstaller):
	def __init__(A,version):super().__init__('nginx',version)
	def _get_download_url(A):return NGINX_DOWNLOAD_URL.format(version=A.version,platform=get_arch())
nginx_package=NginxPackage()