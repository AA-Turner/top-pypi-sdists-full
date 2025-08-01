import logging
from localstack.pro.core import config as pro_config
from localstack.pro.core.runtime.plugin.api import ProPlatformPlugin
from rolo import Router
from rolo.routing.handler import Handler as RouteHandler
LOG=logging.getLogger(__name__)
class PodsPlugin(ProPlatformPlugin):
	name='pods'
	@staticmethod
	def _register_auto_load_pod():
		import os;from localstack import config as D;from localstack.pro.core.config import AUTO_LOAD_POD as A;from localstack.pro.core.persistence.pods.auto_load import PodLoaderFromEnv as E,PodLoaderFromInitDir as F;B=os.path.normpath(os.path.join(D.dirs.config,'..','init-pods.d'))
		if(A or os.path.exists(B))and D.PERSISTENCE:LOG.debug('AUTO_LOAD_POD has not effect if PERSISTENCE is enabled.');return
		if os.path.exists(B):C=F(init_dir=B);C.load()
		if A:C=E(A);C.load()
	def update_localstack_routes(G,router):A=router;from localstack.pro.core.persistence.pods.api.pods_api import CloudPodsRestrictedApi as B;from localstack.pro.core.persistence.pods.endpoints import PublicPodsResource as C;from localstack.pro.core.persistence.pods.manager import PodStateManager as D;from localstack.pro.core.persistence.remotes.api import CloudPodsRemotesApi as E;from localstack.services.plugins import SERVICE_PLUGINS as F;A.add(C(D(F)));A.add(B());A.add(E())
	def on_platform_start(B):from localstack.pro.core.utils.cloud_pods.ci_run_manager import get_ci_run_manager as A;A().startup()
	def on_platform_ready(A):A._register_auto_load_pod()
	def on_platform_shutdown(B):from localstack.pro.core.utils.cloud_pods.ci_run_manager import get_ci_run_manager as A;A().shutdown()
class PodEncryptionPlugin(ProPlatformPlugin):
	name='pod-encryption'
	def on_platform_ready(B):from localstack.pro.core.persistence.utils.encryption import patch_create_and_pull_content as A;A()
	def should_load(A):
		if not super().should_load():return False
		return pro_config.POD_ENCRYPTION