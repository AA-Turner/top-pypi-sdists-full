from localstack.pro.core.bootstrap.licensingv2 import LicensedPluginLoaderGuard
from localstack.utils.objects import singleton_factory
from plux import Plugin,PluginLifecycleListener,PluginManager
class GlueJobExecutorRuntimePlugin(Plugin):namespace='localstack.glue.job_executor'
class GlueLocalJobExecutorRuntimePlugin(GlueJobExecutorRuntimePlugin):
	name='local'
	def load(B,*C,**D):from localstack.pro.core.services.glue.executor.local import LocalJobExecutor as A;return A
class GlueDockerJobExecutorRuntimePlugin(GlueJobExecutorRuntimePlugin):
	name='docker'
	def load(B,*C,**D):from localstack.pro.core.services.glue.executor.docker import DockerJobExecutor as A;return A
class GlueKubernetesJobExecutorRuntimePlugin(GlueJobExecutorRuntimePlugin):
	name='kubernetes';requires_license=True
	def load(B,*C,**D):from localstack.pro.core.services.glue.executor.kubernetes import KubernetesJobExecutor as A;return A
class GlueJobExecutorRuntimePluginManager(PluginManager):
	def __init__(A,listener=None):super().__init__(GlueJobExecutorRuntimePlugin.namespace,listener=listener)
	@staticmethod
	@singleton_factory
	def get():return GlueJobExecutorRuntimePluginManager(LicensedPluginLoaderGuard())