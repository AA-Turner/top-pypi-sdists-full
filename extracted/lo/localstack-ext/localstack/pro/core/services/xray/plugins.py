from localstack.http.dispatcher import Handler as RouteHandler
from localstack.http.router import Router
from localstack.pro.core.runtime.plugin import PlatformPlugin
class XRayExtensionPlugin(PlatformPlugin):
	name='xray-extension'
	def update_gateway_routes(B,router):from localstack.pro.core.services.xray.routes import store_xray_records as A;router.add('/xray_records',A,methods=['POST'])