_H='4.0.x.kraft'
_G='3.7.x.kraft'
_F='3.9.x.kraft'
_E='3.8.x.kraft'
_D='3.9.1'
_C='3.7.2'
_B='3.5.1'
_A=None
import functools,logging,os
from localstack.packages import Package,PackageInstaller
from localstack.packages.core import InstallTarget
from localstack.packages.java import JavaInstallerMixin
from localstack.pro.core.packages.core import MirrorArchiveInstaller
from packaging.version import Version
LOG=logging.getLogger(__name__)
KAFKA_SERVER_URL_MIRROR='https://mirror.lyrahosting.com/apache/kafka/{version}/kafka_{scala_version}-{version}.tgz'
KAFKA_SERVER_URL_ARCHIVE='https://archive.apache.org/dist/kafka/{version}/kafka_{scala_version}-{version}.tgz'
KAFKA_SERVER_URL_DLCDN='https://dlcdn.apache.org/kafka/{version}/kafka_{scala_version}-{version}.tgz'
DEFAULT_VERSION=os.getenv('MSK_DEFAULT_KAFKA_VERSION','').strip()or _B
DEPRECATED_MSK_VERSIONS={'1.1.1','2.1.0','2.2.1','2.3.1','2.4.1','2.4.1.1','2.5.1','2.6.0','2.6.1','2.6.2','2.6.3','2.7.0','2.7.1','2.7.2','2.8.0','2.8.1','2.8.2.tiered','3.1.1','3.2.0','3.3.1','3.3.2','3.6.0.1'}
ACTIVE_MSK_VERSIONS=['3.7.x','3.8.x',_E,_B,'3.6.0',_F,'3.9.x',_G,'3.4.0',_H]
KAFKA_VERSION_MAPPING:dict[str,str]={'3.4.1':'3.4.1',_B:'3.5.2','3.6.0':'3.6.2','3.7.x':_C,_G:_C,'3.8.x':'3.8.1',_E:'3.8.1','3.9.x':_D,_F:_D,_H:_D}
MSK_VERSIONS:set[str]=set(ACTIVE_MSK_VERSIONS)|DEPRECATED_MSK_VERSIONS
KAFKA_VERSIONS:set[str]=MSK_VERSIONS-set(KAFKA_VERSION_MAPPING.keys())|set(KAFKA_VERSION_MAPPING.values())
class KafkaPackage(Package):
	def __init__(A):super().__init__(name='Kafka',default_version=DEFAULT_VERSION)
	def get_versions(A)->list[str]:return sorted(KAFKA_VERSIONS)
	@functools.lru_cache
	def get_installer(self,version:str|_A=_A)->'KafkaPackageInstaller':
		A=version;B=_A
		if A:B=_get_kafka_version(A)
		return super().get_installer(B)
	def _get_installer(A,version:str)->PackageInstaller:return KafkaPackageInstaller('kafka',version)
class KafkaPackageInstaller(JavaInstallerMixin,MirrorArchiveInstaller):
	@property
	def scala_version(self)->str:
		if Version(self.version)>=Version('2.6.0'):return'2.13'
		elif Version(self.version)>Version('1.1.1'):return'2.12'
		else:return'2.11'
	@property
	def kafka_download_url(self)->str:
		if Version(self.version)>=Version(_C):return KAFKA_SERVER_URL_DLCDN
		return KAFKA_SERVER_URL_ARCHIVE
	def _get_archive_subdir(A)->str|_A:return f"kafka_{A.scala_version}-{A.version}"
	def _get_install_marker_path(A,install_dir:str)->str:return os.path.join(install_dir,f"kafka_{A.scala_version}-{A.version}",'bin')
	def _get_primary_url(A)->str:return A.kafka_download_url.format(version=A.version,scala_version=A.scala_version)
	def _get_mirror_url(A)->str:return KAFKA_SERVER_URL_MIRROR.format(version=A.version,scala_version=A.scala_version)
	def _get_checksum_url(A):B=A._get_primary_url();return f"{B}.sha512"
	def _setup_existing_installation(A,target:InstallTarget)->_A:A._prepare_installation(target)
def _get_kafka_version(requested_version:str)->str:
	A=requested_version
	if(B:=KAFKA_VERSION_MAPPING.get(A)):LOG.info('The specified MSK version %s is being mapped to %s. Note, that tiered storage and KRaft-based Kafka are currently unsupported.',A,B);A=B
	if A in KAFKA_VERSIONS:return A
	if A:LOG.info("Unable to install Kafka version '%s', falling back to default '%s'",A,DEFAULT_VERSION)
	return DEFAULT_VERSION
kafka_package=KafkaPackage()