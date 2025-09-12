import logging
from localstack import config
from localstack.aws.handlers import serve_custom_service_request_handlers
from localstack.config import SNAPSHOT_FLUSH_INTERVAL
from localstack.pro.core.runtime.plugin import ProPlatformPlugin
from localstack.runtime import shutdown
from localstack.utils.objects import singleton_factory
from rolo import Router
from rolo.routing.handler import Handler as RouteHandler
LOG=logging.getLogger(__name__)
@singleton_factory
def get_save_strategy():
	from localstack.pro.core.persistence.snapshot.api import SaveStrategy as A;B=A.SCHEDULED
	try:
		if config.SNAPSHOT_SAVE_STRATEGY:return A(config.SNAPSHOT_SAVE_STRATEGY)
	except ValueError as C:LOG.warning('Invalid save strategy, falling back to %s: %s',B,C)
	return B
@singleton_factory
def get_load_strategy():
	from localstack.pro.core.persistence.snapshot.api import LoadStrategy as A
	try:
		if config.SNAPSHOT_LOAD_STRATEGY:return A(config.SNAPSHOT_LOAD_STRATEGY)
	except ValueError as B:LOG.warning('Invalid load strategy, falling back to on_startup: %s',B)
	return A.ON_REQUEST
@singleton_factory
def get_service_state_manager():from localstack import config as A;from localstack.services.plugins import SERVICE_PLUGINS as B;from.manager import SnapshotManager as C;return C(B,A.dirs.data)
def register_state_load_strategy():
	B=get_load_strategy();from localstack.pro.core.persistence.snapshot.api import LoadStrategy as A;from localstack.pro.core.persistence.snapshot.manager import LoadOnRequestHandler as C
	match B:
		case A.ON_STARTUP:LOG.info('registering ON_STARTUP load strategy');return
		case A.ON_REQUEST:LOG.warning('registering ON_REQUEST load strategy: this strategy has known limitations to not restore state correctly for certain services');D=C(get_service_state_manager());serve_custom_service_request_handlers.append(D.on_request)
		case A.MANUAL:LOG.info('registering MANUAL load strategy (call /_localstack/state endpoints to load state)')
		case _:LOG.warning('Unknown load strategy %s',B)
def do_run_state_load_all():
	from localstack.pro.core.persistence.snapshot.api import LoadStrategy as A;B=get_load_strategy()
	if B!=A.ON_STARTUP and config.EAGER_SERVICE_LOADING:LOG.info('Overriding LoadStrategy to ON_STARTUP due to EAGER_SERVICE_LOADING being enabled');B=A.ON_STARTUP
	if B==A.ON_STARTUP:LOG.info('restoring state of all services on startup');get_service_state_manager().load_all()
def register_state_save_strategy():
	from localstack.aws.handlers import run_custom_response_handlers as C,serve_custom_service_request_handlers as D;from.api import SaveStrategy as A;from.manager import SaveOnRequestHandler as H,SaveStateScheduler as I;E=get_save_strategy();F=get_service_state_manager()
	match E:
		case A.ON_SHUTDOWN:LOG.info('registering ON_SHUTDOWN save strategy');shutdown.SHUTDOWN_HANDLERS.register(F.save_all)
		case A.ON_REQUEST:LOG.info('registering ON_REQUEST save strategy');G=H(get_service_state_manager());D.append(G.on_request);C.append(G.on_response)
		case A.SCHEDULED:LOG.info('registering SCHEDULED save strategy');B=I(F,period=SNAPSHOT_FLUSH_INTERVAL);shutdown.SHUTDOWN_HANDLERS.register(B.close);D.append(B.on_request);C.append(B.on_response);B.start()
		case A.MANUAL:LOG.info('registering MANUAL save strategy (call /_localstack/state endpoints to save state)')
		case _:LOG.warning('Unknown save strategy %s',E)
class SnapshotPlugin(ProPlatformPlugin):
	name='snapshot'
	def should_load(A):return config.PERSISTENCE and super().should_load()
	def on_platform_start(A):register_state_load_strategy();register_state_save_strategy()
	def on_platform_ready(A):do_run_state_load_all()
	def update_localstack_routes(B,router):from localstack.pro.core.persistence.snapshot.endpoints import StateResource as A;router.add(A(get_service_state_manager()))