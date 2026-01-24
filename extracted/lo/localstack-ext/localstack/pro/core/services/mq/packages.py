_A='5.18.7'
import os
from localstack.packages import Package,PackageInstaller
from localstack.packages.core import ArchiveDownloadAndExtractInstaller
from localstack.packages.java import JavaInstallerMixin
ACTIVE_MQ_URL='https://archive.apache.org/dist/activemq/<ver>/apache-activemq-<ver>-bin.tar.gz'
class ActiveMQPackage(Package):
	def __init__(A):super().__init__('ActiveMQ',_A)
	def get_versions(A)->list[str]:return[_A]
	def _get_installer(A,version:str)->PackageInstaller:return ActiveMQPackageInstaller('active-mq',version)
class ActiveMQPackageInstaller(JavaInstallerMixin,ArchiveDownloadAndExtractInstaller):
	def _get_download_url(A)->str:return ACTIVE_MQ_URL.replace('<ver>',A.version)
	def _get_archive_subdir(A)->str|None:return f"apache-activemq-{A.version}"
	def _get_install_marker_path(A,install_dir:str)->str:return os.path.join(install_dir,f"apache-activemq-{A.version}",'bin','activemq')
active_mq_package=ActiveMQPackage()