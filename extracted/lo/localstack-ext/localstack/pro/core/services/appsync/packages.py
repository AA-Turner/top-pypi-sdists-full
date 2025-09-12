import logging
from localstack.packages import Package,PackageInstaller
from localstack.packages.core import NodePackageInstaller
from localstack.pro.core import config as pro_config
LOG=logging.getLogger(__name__)
APPSYNC_UTILS_TARBALL_TEMPLATE='https://api.github.com/repos/localstack/appsync-utils/tarball/{ref}'
DEFAULT_APPSYNC_JS_LIBS_VERSION='v0.1.0'
class AppSyncUtilsPackage(Package):
	def __init__(B):
		A=pro_config.APPSYNC_JS_LIBS_VERSION.lower()or DEFAULT_APPSYNC_JS_LIBS_VERSION
		if A in{'latest','refresh'}:LOG.warning("Deprecated value for APPSYNC_JS_LIBS_VERSION: '%s', reverting to locked version '%s' instead. It is still possible to override this value by providing a tag version or a commit sha. ie `v0.1.0` or `6a1d4045f5cd6a31ae3023908802433f3802a2d0`",A,DEFAULT_APPSYNC_JS_LIBS_VERSION);A=DEFAULT_APPSYNC_JS_LIBS_VERSION
		super().__init__('AppSyncUtils',A)
	def get_versions(A):return[A.default_version]
	def _get_installer(A,version):return AppSyncUtilsPackageInstaller(version)
class AppSyncUtilsPackageInstaller(NodePackageInstaller):
	def __init__(B,version):A=version;super().__init__(package_name='@aws-appsync/utils',version=A,package_spec=f"@aws-appsync/utils@{APPSYNC_UTILS_TARBALL_TEMPLATE.format(ref=A)}",main_module='index.js')
appsync_utils_package=AppSyncUtilsPackage()