from localstack.pro.core.bootstrap.licensingv2 import LicensedPluginLoaderGuard
from localstack.pro.core.runtime.plugin import ProPlatformPlugin
from localstack.pro.core.utils.container.registry_strategies import CustomizableRegistryStrategy
from localstack.utils.objects import singleton_factory
from plux import Plugin,PluginLifecycleListener,PluginManager
class ContainerRuntimePlugin(Plugin):namespace='localstack.container.runtime'
class DockerContainerRuntimePlugin(ContainerRuntimePlugin):
	name='docker'
	def load(B,*C,**D):from localstack.pro.core.utils.container.docker_container import DockerContainer as A;return A
class KubernetesContainerRuntimePlugin(ContainerRuntimePlugin):
	name='kubernetes';requires_license=True
	def load(B,*C,**D):from localstack.pro.core.utils.container.kubernetes_container import KubernetesContainer as A;return A
class CustomizableRegistryStrategyPlugin(ProPlatformPlugin):
	name='customizable_registry_strategy';requires_license=False
	def on_platform_start(B):from localstack.utils.docker_utils import DOCKER_CLIENT as A;A.registry_resolver_strategy=CustomizableRegistryStrategy()
class ContainerRuntimePluginManager(PluginManager):
	def __init__(A,listener=None):super().__init__(ContainerRuntimePlugin.namespace,listener=listener)
	@staticmethod
	@singleton_factory
	def get():return ContainerRuntimePluginManager(LicensedPluginLoaderGuard())