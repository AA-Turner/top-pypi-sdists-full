_A='latest'
from localstack.packages import InstallTarget,Package,PackageInstaller
from localstack.pro.core.packages import OSPackageInstaller
class RedisPackage(Package):
	def __init__(A):super().__init__('Redis',_A)
	def get_versions(A)->list[str]:return[_A]
	def _get_installer(A,version:str)->PackageInstaller:return RedisPackageInstaller(version)
class RedisPackageInstaller(OSPackageInstaller):
	def __init__(A,version:str):super().__init__('redis',version)
	def _debian_get_install_dir(A,target:InstallTarget):return'/etc/redis'
	def _debian_get_install_marker_path(A,install_dir:str)->str:return'/usr/bin/redis-server'
	def _debian_packages(A)->list[str]:return['redis-server']
redis_package=RedisPackage()