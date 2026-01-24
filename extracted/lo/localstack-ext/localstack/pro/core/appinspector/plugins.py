import localstack.pro.core.config as config
from localstack.http import Router
from localstack.http.dispatcher import Handler as RouteHandler
from localstack.pro.core.runtime.plugin import ProPlatformPlugin
class AppInspectorPlugin(ProPlatformPlugin):
	name='appinspector'
	def should_load(B)->bool:
		if not config.APPINSPECTOR_DEV_ENABLE:return False
		from localstack.pro.core.appinspector.utils import APPINSPECTOR_LOG as A;A.debug('AppInspectorPlugin is enabled via APPINSPECTOR_DEV_ENABLE');return super().should_load()
	def update_localstack_routes(B,router:Router[RouteHandler]):from localstack.pro.core.appinspector.api.router import AppInspectorRouter as A;A(router).register_routes()
	def on_platform_ready(F):from localstack.pro.core.appinspector.database.database import get_appinspector_db_manager as A;from localstack.pro.core.appinspector.sql_span_exporter import register_sql_span_exporter as B;from localstack.pro.core.appinspector.utils import APPINSPECTOR_LOG as C;from localstack.pro.core.tracing.opentelemetry.plugin import OpenTelemetryInstrumentationPluginManager as D;A().initialize_db();E=D.get();E.enable_instrumentation();B();C.info('AppInspector platform ready: database initialized, OpenTelemetry instrumentation enabled (including IAM policy capture), combined span and event exporter registered')
	def on_platform_shutdown(D):from localstack.pro.core.appinspector.database.database import get_appinspector_db_manager as A;from localstack.pro.core.tracing.opentelemetry.plugin import OpenTelemetryInstrumentationPluginManager as B;A().shutdown_database();C=B.get();C.disable_instrumentation()