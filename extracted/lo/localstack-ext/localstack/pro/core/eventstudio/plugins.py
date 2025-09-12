import localstack.pro.core.config as config
from localstack.http import Router
from localstack.http.dispatcher import Handler as RouteHandler
from localstack.pro.core.eventstudio.database.database import get_eventstudio_db_manager
from localstack.pro.core.eventstudio.sql_span_exporter import register_sql_span_exporter
from localstack.pro.core.eventstudio.utils import EVENTSTUDIO_LOG
from localstack.pro.core.runtime.plugin import ProPlatformPlugin
from localstack.pro.core.tracing.opentelemetry.plugin import OpenTelemetryInstrumentationPluginManager
class EventStudioPlugin(ProPlatformPlugin):
	name='eventstudio'
	def should_load(A):
		if not config.EVENTSTUDIO_DEV_ENABLE:return False
		EVENTSTUDIO_LOG.debug('EventStudioPlugin is enabled via EVENTSTUDIO_DEV_ENABLE');return super().should_load()
	def update_localstack_routes(B,router):from localstack.pro.core.eventstudio.api.router import EventStudioRouter as A;A(router).register_routes()
	def on_platform_ready(B):get_eventstudio_db_manager().initialize_db();A=OpenTelemetryInstrumentationPluginManager.get();A.enable_instrumentation();register_sql_span_exporter()
	def on_platform_shutdown(B):get_eventstudio_db_manager().shutdown_database();A=OpenTelemetryInstrumentationPluginManager.get();A.disable_instrumentation()