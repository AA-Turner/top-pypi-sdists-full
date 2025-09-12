_J='4.0.x.kraft'
_I='3.9.x.kraft'
_H='3.8.x.kraft'
_G='3.7.x.kraft'
_F='2.8.2.tiered'
_E='3.6.0.1'
_D='2.4.1.1'
_C='3.9.1'
_B='3.7.2'
_A='3.6.0'
import functools,logging,os
from localstack.packages import Package,PackageInstaller
from localstack.packages.core import ArchiveDownloadAndExtractInstaller
from localstack.packages.java import JavaInstallerMixin
from packaging.version import Version
LOG=logging.getLogger(__name__)
KAFKA_SERVER_URL_ARCHIVE='https://archive.apache.org/dist/kafka/<version>/kafka_<scala_version>-<version>.tgz'
KAFKA_SERVER_URL_DLCDN='https://dlcdn.apache.org/kafka/<version>/kafka_<scala_version>-<version>.tgz'
DEFAULT_VERSION=os.getenv('MSK_DEFAULT_KAFKA_VERSION','').strip()or'3.5.1'
DEPRECATED_MSK_VERSIONS={'1.1.1','2.1.0','2.2.1','2.3.1','2.4.1',_D,'2.5.1',_E}
ACTIVE_MSK_VERSIONS={'2.6.0','2.6.1','2.6.2','2.6.3','2.7.0','2.7.1','2.7.2','2.8.0','2.8.1',_F,'3.1.1','3.2.0','3.3.1','3.3.2','3.4.0','3.5.1',_A,'3.7.x',_G,'3.8.x',_H,'3.9.x',_I,_J}
KAFKA_VERSION_MAPPING={_F:'2.8.2',_D:'2.4.1',_E:_A,'3.6.1':_A,'3.7.x':_B,_G:_B,'3.8.x':'3.8.1',_H:'3.8.1','3.9.x':_C,_I:_C,_J:_C}
MSK_VERSIONS=ACTIVE_MSK_VERSIONS|DEPRECATED_MSK_VERSIONS
KAFKA_VERSIONS=MSK_VERSIONS-set(KAFKA_VERSION_MAPPING.keys())|set(KAFKA_VERSION_MAPPING.values())
class KafkaPackage(Package):
	def __init__(A):super().__init__(name='Kafka',default_version=DEFAULT_VERSION)
	def get_versions(A):return sorted(KAFKA_VERSIONS)
	@functools.lru_cache
	def get_installer(self,version=None):
		A=version;B=None
		if A:B=_get_kafka_version(A)
		return super().get_installer(B)
	def _get_installer(A,version):return KafkaPackageInstaller('kafka',version)
class KafkaPackageInstaller(JavaInstallerMixin,ArchiveDownloadAndExtractInstaller):
	@property
	def scala_version(self):
		if Version(self.version)>=Version('2.6.0'):return'2.13'
		elif Version(self.version)>Version('1.1.1'):return'2.12'
		else:return'2.11'
	@property
	def kafka_download_url(self):
		if Version(self.version)>=Version(_B):return KAFKA_SERVER_URL_DLCDN
		return KAFKA_SERVER_URL_ARCHIVE
	def _get_download_url(A):return A.kafka_download_url.replace('<version>',A.version).replace('<scala_version>',A.scala_version)
	def _get_archive_subdir(A):return f"kafka_{A.scala_version}-{A.version}"
	def _get_install_marker_path(A,install_dir):return os.path.join(install_dir,f"kafka_{A.scala_version}-{A.version}",'bin')
def _get_kafka_version(requested_version):
	A=requested_version
	if(B:=KAFKA_VERSION_MAPPING.get(A)):LOG.info('The specified MSK version %s is being mapped to %s. Note, that tiered storage and KRaft-based Kafka are currently unsupported.',A,B);A=B
	if A in KAFKA_VERSIONS:return A
	if A:LOG.info("Unable to install Kafka version '%s', falling back to default '%s'",A,DEFAULT_VERSION)
	return DEFAULT_VERSION
kafka_package=KafkaPackage()