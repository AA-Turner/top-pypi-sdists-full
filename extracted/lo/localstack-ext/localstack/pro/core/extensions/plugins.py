from __future__ import annotations
import logging
from localstack.pro.core.runtime.plugin import ProPlatformPlugin
from rolo.routing import Router
from rolo.routing.handler import Handler as RouteHandler
EXTENSION_HOOK_PRIORITY=-1
LOG=logging.getLogger(__name__)
class ExtensionsPlugin(ProPlatformPlugin):
	priority=EXTENSION_HOOK_PRIORITY;name='extensions'
	def on_platform_start(H):from localstack.aws.handlers import run_custom_finalizers as B,run_custom_response_handlers as C,serve_custom_exception_handlers as D,serve_custom_service_request_handlers as E;from localstack.pro.core.extensions.manager import ExtensionsManager as F;from localstack.services import edge;A=F.get();G=A.load_all();LOG.info('loaded %s extensions',len(G));LOG.debug('calling extensions on_platform_start');A.call_on_platform_start();LOG.debug('calling extensions update_gateway_routes');A.call_update_gateway_routes(edge.ROUTER);LOG.debug('calling extensions update_request_handlers');A.call_update_request_handlers(E);LOG.debug('calling extensions update_response_handlers');A.call_update_response_handlers(C);LOG.debug('calling extensions update_exception_handlers');A.call_update_exception_handlers(D);LOG.debug('calling extensions update_finalizers');A.call_update_finalizers(B)
	def on_platform_ready(C):from localstack.pro.core.extensions.manager import ExtensionsManager as A;B=A.get();LOG.debug('calling extensions on_platform_ready');B.call_on_platform_ready()
	def on_platform_shutdown(C):from localstack.pro.core.extensions.manager import ExtensionsManager as A;B=A.get();LOG.debug('calling extensions on_platform_shutdown');B.call_on_platform_shutdown()
	def update_localstack_routes(B,router):from localstack.pro.core.extensions.resource import ExtensionsApi as A;router.add(A())