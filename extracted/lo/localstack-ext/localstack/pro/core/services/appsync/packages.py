_A='latest'
import logging
from typing import List
from localstack.packages import InstallTarget,Package,PackageInstaller
from localstack.packages.core import NodePackageInstaller
from localstack.pro.core import config as config_ext
from localstack.utils.run import run
LOG=logging.getLogger(__name__)
APPSYNC_UTILS_TARBALL_TEMPLATE='https://github.com/localstack/appsync-utils/archive/{ref}.tar.gz'
class AppSyncUtilsPackage(Package):
	def __init__(A):super().__init__('AppSyncUtils',config_ext.APPSYNC_JS_LIBS_VERSION.lower()or _A)
	def get_versions(A):return[A.default_version]
	def _get_installer(A,version):return AppSyncUtilsPackageInstaller(version)
class AppSyncUtilsPackageInstaller(NodePackageInstaller):
	force_refresh:bool=False
	def __init__(C,version):
		A=version
		if A=='refresh':C.force_refresh=True;A=_A
		B=APPSYNC_UTILS_TARBALL_TEMPLATE.format(ref='refs/heads/main')
		if A!=_A:
			if A.startswith('v'):B=APPSYNC_UTILS_TARBALL_TEMPLATE.format(ref=f"refs/tags/{A}")
			else:B=APPSYNC_UTILS_TARBALL_TEMPLATE.format(ref=A)
		super().__init__(package_name='@aws-appsync/utils',version=A,package_spec=f"@aws-appsync/utils@{B}",main_module='index.js')
	def _setup_existing_installation(A,target):
		if not A.force_refresh:return
		LOG.debug('updating @aws-appsync/utils installation');B=A._get_install_dir(target);run(['npm','install','--update','--prefix',B])
appsync_utils_package=AppSyncUtilsPackage()