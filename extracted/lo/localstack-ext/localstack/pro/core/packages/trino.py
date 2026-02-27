_B='440.post1'
_A=None
import os
from localstack.constants import MAVEN_REPO_URL
from localstack.packages import InstallTarget,Package
from localstack.packages.core import ArchiveDownloadAndExtractInstaller
from localstack.pro.core import config as pro_config
from localstack.pro.core.packages.bigdata_common import bigdata_jar_cache_dir,download_and_cache_jar_file
from localstack.pro.core.packages.cve_fixes import CVEFix,FixStrategyDelete,fix_cves_in_jar_files
from localstack.utils.files import cp_r,save_file
TRINO_URL={_B:f"{MAVEN_REPO_URL}/io/trino/trino-server/440/trino-server-440.tar.gz"}
TRINO_DEFAULT_VERSION=_B
TRINO_VERSIONS=[TRINO_DEFAULT_VERSION]
JAVA_VERSION='21'
TRINO_JVM_CONFIG='\n-server\n-Xmx2G\n-XX:+UseG1GC\n-XX:+UseGCOverheadLimit\n-XX:+ExplicitGCInvokesConcurrent\n-XX:+HeapDumpOnOutOfMemoryError\n-XX:+ExitOnOutOfMemoryError\n-XX:ReservedCodeCacheSize=150M\n-Duser.timezone=UTC\n-Djdk.attach.allowAttachSelf=true\n-Djdk.nio.maxCachedBufferSize=2000000\n'
TRINO_CONFIG_PROPS='\nnode.id=trino-master\nnode.environment=test\ncoordinator=true\nnode-scheduler.include-coordinator=true\nhttp-server.http.port={trino_port}\nquery.max-memory=1GB\nquery.max-memory-per-node=1GB\ndiscovery-server.enabled=true\ndiscovery.uri=http://localhost:{trino_port}\nprotocol.v1.alternate-header-name=Trino\ncatalog.management=dynamic\n'
class TrinoInstaller(ArchiveDownloadAndExtractInstaller):
	def __init__(A,version:str):super().__init__(name='trino',version=version,extract_single_directory=True)
	def _get_install_marker_path(A,install_dir:str)->str:return os.path.join(install_dir,'bin','launcher')
	def _get_download_url(A):return TRINO_URL.get(A.version)
	def _prepare_installation(D,target:InstallTarget)->_A:A=target;from localstack.packages.java import java_package as B;from localstack.pro.core.packages.spark import spark_common_driver_package as C;C.install(target=A);B.install(version=JAVA_VERSION,target=A)
	def _post_process(A,target:InstallTarget)->_A:B=target;A._download_iceberg_jar(target=B);A._apply_cve_fixes(target=B)
	def _download_iceberg_jar(B,target:InstallTarget)->_A:
		from localstack.pro.core.packages.hive import ICEBERG_JAR_URL as C;from localstack.pro.core.packages.spark import spark_common_driver_package as D;E=B.get_trino_lib_dir();F=D.get_installed_dir();G=bigdata_jar_cache_dir(target=target);H=download_and_cache_jar_file(jar_url=C,cache_dir=G,target_dir=F);A=os.path.join(E,'iceberg.jar')
		if not os.path.exists(A):cp_r(H,A)
	def _get_trino_subdir(B,subdir:str)->str|_A:
		A=B.get_installed_dir()
		if not A:return
		return os.path.join(A,subdir)
	def get_trino_lib_dir(A)->str|_A:return A._get_trino_subdir('lib')
	def get_trino_etc_dir(A)->str|_A:return A._get_trino_subdir('etc')
	def write_trino_config(B,additional_configs:dict[str,str])->_A:A=B.get_trino_etc_dir();C=os.path.join(A,'config.properties');D=TRINO_CONFIG_PROPS.format(trino_port=pro_config.PORT_TRINO_SERVER);save_file(C,D);E=os.path.join(A,'jvm.config');save_file(E,TRINO_JVM_CONFIG)
	def _apply_cve_fixes(B,target:InstallTarget)->_A:A=CVEFix(paths=['trino/440.post1/plugin/pinot/helix-core-1.0.4.jar'],strategy=FixStrategyDelete());fix_cves_in_jar_files(target,fixes=[A])
	def get_java_home(B):from localstack.packages.java import java_package as A;return A.get_installer(JAVA_VERSION).get_java_home()
class TrinoPackage(Package):
	def __init__(A,default_version:str=TRINO_DEFAULT_VERSION):super().__init__(name='Trino',default_version=default_version)
	def get_versions(A)->list[str]:return TRINO_VERSIONS
	def _get_installer(A,version):return TrinoInstaller(version)
trino_package=TrinoPackage()