from localstack.pro.core.runtime.plugin import ProPlatformPlugin
from rolo import Router
from rolo.routing.handler import Handler as RouteHandler
class StateResetPlugin(ProPlatformPlugin):
	name='state-reset'
	def update_localstack_routes(C,router):from localstack.pro.core.persistence.reset.endpoints import StateResetResource as A;from localstack.services.plugins import SERVICE_PLUGINS as B;router.add(A(B))